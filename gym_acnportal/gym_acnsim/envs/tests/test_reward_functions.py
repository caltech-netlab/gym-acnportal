# coding=utf-8
""" Tests for reward functions. """
import unittest
from typing import Callable, Dict, List
from unittest.mock import create_autospec, Mock, patch

import numpy as np
from acnportal.acnsim import Simulator, ChargingNetwork, EVSE, Current, FiniteRatesEVSE
from acnportal.acnsim.network.sites import simple_acn
from gym import spaces

from ...interfaces import GymTrainingInterface, GymTrainedInterface
from .. import reward_functions as rf, CustomSimEnv
from ..action_spaces import SimAction


class TestRewardFunction(unittest.TestCase):
    simulator: Simulator

    # noinspection PyMissingOrEmptyDocstring
    def setUp(self) -> None:
        self.simulator: Simulator = create_autospec(Simulator)
        self.interface: GymTrainingInterface = GymTrainingInterface(self.simulator)
        # Set mock's deepcopy to return input (a dict of already copied
        # attributes).
        self.simulator.__deepcopy__ = lambda x: x
        self.sim_action_space_function: Callable[
            [GymTrainedInterface], spaces.Space
        ] = lambda x: spaces.Space()
        self.sim_action_function: Callable[
            [GymTrainedInterface, np.ndarray], Dict[str, List[float]]
        ] = lambda x, y: {"a": [0]}
        self.env: CustomSimEnv = CustomSimEnv(
            self.interface,
            [],
            SimAction(
                self.sim_action_space_function, self.sim_action_function, "stub_action"
            ),
            [],
        )
        self.simulator.network = ChargingNetwork()


class TestEVSEViolation(TestRewardFunction):
    # noinspection PyMissingOrEmptyDocstring
    def setUp(self) -> None:
        super().setUp()

    def test_evse_violation_key_error(self) -> None:
        self.env.schedule = {"TS-001": [0], "TS-002": [0]}
        with self.assertRaises(KeyError):
            _ = rf.evse_violation(self.env)

    def _add_placeholder_constraint(self) -> None:
        """ Adds a non-binding constraint to the network. Call this after registering
        EVSEs."""
        self.simulator.network.add_constraint(
            Current(self.simulator.network.station_ids), float("inf")
        )

    def _continuous_evse_helper(self) -> None:
        self.simulator.network.register_evse(EVSE("TS-001", max_rate=32), 208, 0)
        self.simulator.network.register_evse(
            EVSE("TS-002", max_rate=16, min_rate=6), 208, 0
        )
        self.simulator.network.register_evse(
            EVSE("TS-003", max_rate=32, min_rate=6), 208, 0
        )
        self._add_placeholder_constraint()

    def test_evse_violation_continuous_violation(self) -> None:
        self._continuous_evse_helper()
        self.env.schedule = {"TS-001": [34, 31], "TS-002": [4, 5], "TS-003": [0, 0]}
        self.assertEqual(rf.evse_violation(self.env), -5)

    def test_evse_violation_continuous_no_violation(self) -> None:
        self._continuous_evse_helper()
        self.env.schedule = {"TS-001": [31, 16], "TS-002": [7, 16], "TS-003": [0, 0]}
        self.assertEqual(rf.evse_violation(self.env), 0)

    def _discrete_evse_helper(self) -> None:
        self.simulator.network.register_evse(
            FiniteRatesEVSE("TS-001", [8, 16, 24, 32]), 208, 0
        )
        self.simulator.network.register_evse(FiniteRatesEVSE("TS-002", [6, 16]), 208, 0)
        self.simulator.network.register_evse(
            FiniteRatesEVSE("TS-003", list(range(1, 32))), 208, 0
        )
        self._add_placeholder_constraint()

    def test_evse_violation_non_continuous_violation(self) -> None:
        self._discrete_evse_helper()
        self.env.schedule = {"TS-001": [4, 19], "TS-002": [8, 18], "TS-003": [0, 0]}
        self.assertEqual(rf.evse_violation(self.env), -11)

    def test_evse_violation_non_continuous_no_violation(self) -> None:
        self._discrete_evse_helper()
        self.env.schedule = {"TS-001": [8, 24], "TS-002": [6, 16], "TS-003": [0, 0]}
        self.assertEqual(rf.evse_violation(self.env), 0)


class TestUnpluggedEVViolation(TestRewardFunction):
    # noinspection PyMissingOrEmptyDocstring
    def setUp(self) -> None:
        super().setUp()
        self.env.schedule = {"TS-001": [8, 24], "TS-002": [6, 16]}
        # Overwrite simulator network with a Mock
        self.simulator.network = create_autospec(ChargingNetwork)

    def test_unplugged_ev_violation_empty_schedules(self) -> None:
        self.env.schedule = {"TS-001": [], "TS-002": []}
        self.assertEqual(rf.unplugged_ev_violation(self.env), 0)

    def test_unplugged_ev_violation_all_unplugged(self) -> None:
        self.simulator.network.active_station_ids = ["TS-003"]
        self.assertEqual(rf.unplugged_ev_violation(self.env), -14)

    def test_unplugged_ev_violation_some_unplugged(self) -> None:
        self.simulator.network.active_station_ids = ["TS-002", "TS-003"]
        self.assertEqual(rf.unplugged_ev_violation(self.env), -8)

    def test_unplugged_ev_violation_none_unplugged(self) -> None:
        self.simulator.network.active_station_ids = ["TS-001", "TS-002", "TS-003"]
        self.assertEqual(rf.unplugged_ev_violation(self.env), 0)


class TestConstraintViolation(TestRewardFunction):
    # noinspection PyMissingOrEmptyDocstring
    def setUp(self) -> None:
        super().setUp()
        self.simulator.network = simple_acn(
            ["TS-001", "TS-002", "TS-003"], aggregate_cap=10
        )

    def test_constraint_violation_no_action(self) -> None:
        self.env.action = None
        self.assertEqual(rf.current_constraint_violation(self.env), 0)

    def test_constraint_violation_with_violating_action_matrix(self) -> None:
        self.env.action = np.array([[32, 16], [16, 0], [20, 0]])
        self.assertAlmostEqual(rf.current_constraint_violation(self.env), -59.7692308)

    def test_constraint_violation_no_violation_action_matrix(self) -> None:
        self.env.action = np.array([[16, 32], [0, 16], [0, 20]])
        self.assertAlmostEqual(rf.current_constraint_violation(self.env), 0)

    def test_constraint_violation_with_violating_action_vector(self) -> None:
        self.env.action = np.array([32, 16, 20])
        self.assertAlmostEqual(rf.current_constraint_violation(self.env), -59.7692308)

    def test_constraint_violation_no_violation_action_vector(self) -> None:
        self.env.action = np.array([16, 0, 0])
        self.assertAlmostEqual(rf.current_constraint_violation(self.env), 0)


class TestSoftChargingReward(TestRewardFunction):
    # noinspection PyMissingOrEmptyDocstring
    def setUp(self) -> None:
        super().setUp()

    def test_soft_charging_reward(self) -> None:
        self.simulator.charging_rates = np.array([[1, 1, 2], [1, 0, 1], [0, 0, 0]])
        self.prev_simulator = create_autospec(Simulator)
        self.prev_simulator.charging_rates = np.array([[1, 1, 0], [1, 0, 0], [0, 0, 0]])
        self.env.interface = GymTrainingInterface(self.simulator)
        self.env.prev_interface = GymTrainingInterface(self.prev_simulator)
        self.assertEqual(rf.soft_charging_reward(self.env), 3)


if __name__ == "__main__":
    unittest.main()
