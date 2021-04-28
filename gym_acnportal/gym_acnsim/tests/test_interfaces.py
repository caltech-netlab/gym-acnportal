# coding=utf-8
"""
Tests for Interfaces to Simulators used by gym_acnsim environments.
"""
import unittest
from typing import Any, Dict, List, Callable
from unittest.mock import create_autospec, Mock, patch

import numpy as np
from acnportal.acnsim import EV, EventQueue, FiniteRatesEVSE, EVSE, DeadbandEVSE
from acnportal.acnsim.tests.test_interface import TestInterface

from gym_acnportal.gym_acnsim.interfaces import GymTrainedInterface, \
    GymTrainingInterface


class TestGymTrainedInterface(TestInterface):
    # noinspection PyMissingOrEmptyDocstring
    def setUp(self) -> None:
        super().setUp()
        self.interface: GymTrainedInterface = GymTrainedInterface.from_interface(
            self.interface
        )
        self.evse1 = self.network._EVSEs["PS-001"]
        self.evse2 = self.network._EVSEs["PS-002"]
        self.evse3 = self.network._EVSEs["PS-003"]

    def test_station_ids(self) -> None:
        self.assertEqual(
            self.interface.station_ids, ["PS-001", "PS-003", "PS-002", "PS-004"]
        )

    def test_active_station_ids(self) -> None:
        # Auto-specs are of type Any as typing does not support Mocks.
        ev1: Any = create_autospec(EV)
        ev2: Any = create_autospec(EV)
        ev1.station_id = "PS-001"
        ev2.station_id = "PS-002"
        ev1.fully_charged = True
        ev2.fully_charged = False
        self.network.plugin(ev1)
        self.network.plugin(ev2)
        self.assertEqual(self.interface.active_station_ids, ["PS-002"])

    def test_is_done(self) -> None:
        event_queue: EventQueue = EventQueue()
        event_queue.empty = create_autospec(event_queue.empty)
        self.simulator.event_queue = event_queue
        _ = self.interface.is_done
        event_queue.empty.assert_called_once()

    def test_charging_rates(self) -> None:
        self.simulator.charging_rates = np.eye(2)
        np.testing.assert_equal(self.interface.charging_rates, np.eye(2))

    def test_is_feasible_evse_key_error(self) -> None:
        with self.assertRaises(KeyError):
            self.interface.is_feasible_evse({"PS-001": [1], "PS-000": [0]})

    def _open_evse_registration(func: Callable) -> Callable:
        """Temporarily removes constraints so new EVSEs can be registered."""
        def _inner_open_evse_registration(self: "TestGymTrainedInterface"):
            self.network.constraint_matrix = None
            self.network.magnitudes = np.array([])
            self.network.constraint_index = []
            func(self)
            self.network.constraint_matrix = np.eye(len(self.network._EVSEs))
            self.network.magnitudes = np.ones((len(self.network._EVSEs), 1))
            self.network.constraint_index = [
                f"C{i+1}" for i in range(len(self.network._EVSEs))
            ]

        return _inner_open_evse_registration

    @_open_evse_registration
    def _continuous_evse_helper(self) -> None:
        evse1 = EVSE("PS-001-ub", max_rate=32)
        self.network.register_evse(evse1, 120, -30)
        evse2 = EVSE("PS-002-lb", min_rate=6)
        evse3 = DeadbandEVSE("PS-003-db")
        self.network.register_evse(evse3, 360, 150)
        self.network.register_evse(evse2, 240, 90)

    def test_is_feasible_evse_continuous_infeasible(self) -> None:
        self._continuous_evse_helper()
        schedule: Dict[str, List[float]] = {
            "PS-001-ub": [34, 31],
            "PS-002-lb": [4, 5],
            "PS-003-db": [0, 0],
        }
        self.assertFalse(self.interface.is_feasible_evse(schedule))

    def test_is_feasible_evse_continuous_feasible(self) -> None:
        self._continuous_evse_helper()
        schedule: Dict[str, List[float]] = {
            "PS-001-ub": [31, 16],
            "PS-002-lb": [7, 16],
            "PS-003-db": [0, 0],
        }
        self.assertTrue(self.interface.is_feasible_evse(schedule))

    @_open_evse_registration
    def _discrete_evse_helper(self) -> None:
        self.evse1: FiniteRatesEVSE = FiniteRatesEVSE("PS-001-fr", [8, 16, 24, 32])
        self.evse2: FiniteRatesEVSE = FiniteRatesEVSE("PS-002-fr", [6, 16])
        self.evse3: FiniteRatesEVSE = FiniteRatesEVSE("PS-003-fr", list(range(1, 32)))
        self.network.register_evse(self.evse1, 120, -30)
        self.network.register_evse(self.evse3, 360, 150)
        self.network.register_evse(self.evse2, 240, 90)

    def test_is_feasible_evse_discrete_infeasible(self) -> None:
        self._discrete_evse_helper()
        schedule: Dict[str, List[float]] = {
            "PS-001-fr": [4, 19],
            "PS-002-fr": [8, 18],
            "PS-003-fr": [0, 0],
        }
        self.assertFalse(self.interface.is_feasible_evse(schedule))

    def test_is_feasible_evse_discrete_feasible(self) -> None:
        self._discrete_evse_helper()
        schedule: Dict[str, List[float]] = {
            "PS-001-fr": [8, 24],
            "PS-002-fr": [6, 16],
            "PS-003-fr": [0, 0],
        }
        self.assertTrue(self.interface.is_feasible_evse(schedule))

    # TODO: Clarify why is_feasible is patched here and at other points.
    @patch("acnportal.acnsim.Interface.is_feasible", return_value=True)
    def test_is_feasible(self, mocked_is_feasible) -> None:
        self.interface.is_feasible_evse = Mock()
        self.interface.is_feasible_evse.return_value = True
        self.assertTrue(self.interface.is_feasible({}))
        mocked_is_feasible.assert_called_once_with(
            {}, linear=False, violation_tolerance=None, relative_tolerance=None
        )
        # PyCharm inspector flags these references as nonexistent in
        # type 'function' as PyCharm doesn't know these are Mocks.
        self.interface.is_feasible_evse.assert_called_once_with({})

    def test_last_energy_delivered(self) -> None:
        ev1: Any = create_autospec(EV)
        ev2: Any = create_autospec(EV)
        ev1.current_charging_rate = 32
        ev2.current_charging_rate = 16
        self.simulator.get_active_evs = Mock()
        self.simulator.get_active_evs.return_value = [ev1, ev2]
        self.assertEqual(self.interface.last_energy_delivered(), 48)

    @patch("acnportal.acnsim.ChargingNetwork.constraint_current", return_value=4 - 3j)
    def test_current_constraint_currents(self, mocked_constraint_current) -> None:
        self.assertEqual(self.interface.current_constraint_currents({}), 5)
        mocked_constraint_current.assert_called_once_with({}, time_indices=[0])


class TestGymTrainingInterface(TestGymTrainedInterface):
    # noinspection PyMissingOrEmptyDocstring
    def setUp(self) -> None:
        super().setUp()
        self.interface: GymTrainingInterface = GymTrainingInterface.from_interface(
            self.interface
        )
        self.simulator.step = Mock()
        self.simulator.step.return_value = True
        self.simulator.max_recompute = 2

    def _step_helper(self) -> Dict[str, List[float]]:
        schedule: Dict[str, List[float]] = {
            "PS-001": [34, 31],
            "PS-002": [4, 5],
            "PS-003": [0, 0],
        }
        event_queue: EventQueue = EventQueue()
        event_queue.empty = create_autospec(event_queue.empty)
        event_queue.empty.return_value = True
        self.simulator.event_queue = event_queue
        return schedule

    def test_step_warning_no_schedules(self) -> None:
        with self.assertWarns(UserWarning):
            self.interface.step({})

    def test_step_warning_short_schedule(self) -> None:
        schedule = self._step_helper()
        self.simulator.max_recompute = 4
        with self.assertWarns(UserWarning):
            self.interface.step(schedule)

    # TODO: Should Interface.is_feasible be patched instead?
    @patch(
        "gym_acnportal.gym_acnsim.GymTrainingInterface.is_feasible", return_value=False
    )
    def test_step_infeasible_schedule(self, mocked_is_feasible) -> None:
        schedule: Dict[str, List[float]] = self._step_helper()
        self.assertEqual(self.interface.step(schedule), (True, False))
        self.simulator.event_queue.empty.assert_called_once()
        mocked_is_feasible.assert_called_once_with(schedule)
        self.simulator.step.assert_not_called()

    @patch(
        "gym_acnportal.gym_acnsim.GymTrainingInterface.is_feasible", return_value=True
    )
    def test_step_feasible_schedule(self, mocked_is_feasible) -> None:
        schedule: Dict[str, List[float]] = self._step_helper()
        self.assertEqual(self.interface.step(schedule), (True, True))
        self.simulator.event_queue.empty.assert_not_called()
        mocked_is_feasible.assert_called_once_with(schedule)
        self.simulator.step.assert_called_once_with(schedule)

    @patch(
        "gym_acnportal.gym_acnsim.GymTrainingInterface.is_feasible", return_value=False
    )
    def test_step_infeasible_schedule_no_force_feasibility(
        self, mocked_is_feasible
    ) -> None:
        schedule: Dict[str, List[float]] = self._step_helper()
        self.assertEqual(
            self.interface.step(schedule, force_feasibility=False), (True, False)
        )
        self.simulator.event_queue.empty.assert_not_called()
        mocked_is_feasible.assert_called_once_with(schedule)
        self.simulator.step.assert_called_once_with(schedule)


if __name__ == "__main__":
    unittest.main()
