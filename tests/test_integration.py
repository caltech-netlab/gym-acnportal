# coding=utf-8
"""
Integration tests using gym_acnsim.
"""
# TODO: This test suite copies a lot of code from acnportal as the tests
#  module isn't part of acnportal. Maybe put integration tests in a
#  different repo?
import json
import os
from copy import deepcopy
from datetime import datetime
from typing import Dict, List
import unittest

import numpy as np
import pytz
from acnportal.acnsim.interface import SessionInfo

from acnportal import acnsim
from acnportal.acnsim import EV, sites, acndata_events, Simulator
from acnportal.algorithms import BaseAlgorithm

from gym_acnportal.algorithms import SimRLModelWrapper, GymTrainedAlgorithm
from gym_acnportal.gym_acnsim import make_default_sim_env
from gym_acnportal.gym_acnsim.interfaces import GymTrainedInterface


class EarliestDeadlineFirstAlgoStateful(BaseAlgorithm):
    """ See EarliestDeadlineFirstAlgo in tutorial 2 of acnportal.
    This is a stateful version that occasionally records charging
    rates and pilot signals to test the last_applied_pilot_signals
    and last_actual_charging_rate functions in Interface.
    """

    def __init__(self, increment: int = 1) -> None:
        super().__init__()
        self._increment = increment
        self.polled_pilots = {}
        self.polled_charging_rates = {}
        self.max_recompute = 1

    def schedule(self, active_sessions: List[SessionInfo]) -> Dict[str, List[float]]:
        """ Schedule EVs by first sorting them by departure time, then
        allocating them their maximum feasible rate.

        Implements abstract method schedule from BaseAlgorithm.

        See class documentation for description of the algorithm.

        This version stores the current pilot signals and charging rates
        every 100 timesteps.

        Args:
            active_sessions (List[SessionInfo]): see BaseAlgorithm

        Returns:
            Dict[str, List[float]]: see BaseAlgorithm
        """
        schedule = {ev.station_id: [0] for ev in active_sessions}

        sorted_evs = sorted(active_sessions, key=lambda x: x.departure)

        for ev in sorted_evs:
            schedule[ev.station_id] = [self.interface.max_pilot_signal(ev.station_id)]

            while not self.interface.is_feasible(schedule):
                schedule[ev.station_id][0] -= self._increment

                if schedule[ev.station_id][0] < 0:
                    schedule[ev.station_id] = [0]
                    break
        if not self.interface.current_time % 100:
            self.polled_pilots[
                str(self.interface.current_time)
            ] = self.interface.last_applied_pilot_signals
            self.polled_charging_rates[
                str(self.interface.current_time)
            ] = self.interface.last_actual_charging_rate
        return schedule


class EDFWrapper(SimRLModelWrapper):
    """
    A model wrapper that mimics the behavior of the earliest deadline
    first (EDF) algorithm from the sorted_algorithms module. Instead of
    using the observation to generate the schedule, this algorithm
    instead directly uses the interface contained in the info parameter.
    """

    def __init__(self, model: object = None) -> None:
        super().__init__(model)
        self.edf_algo = EarliestDeadlineFirstAlgoStateful()
        self.polled_pilots = {}
        self.polled_charging_rates = {}

    def predict(
        self,
        observation: Dict[str, np.ndarray],
        reward: float,
        done: bool,
        info: Dict[str, GymTrainedInterface] = None,
    ) -> np.ndarray:
        """ Implements SimRLModelWrapper.predict() """
        # Generally, predictions in an OpenAI workflow do not use the
        # info returned after stepping the environment. We use the info
        # here to avoid having to rewrite the EDF algorithm in a way
        # that does not use the interface.
        if info is None:
            raise ValueError(
                "EDFStepped model wrapper requires an "
                "info argument containing an Interface to "
                "run."
            )
        self.edf_algo.register_interface(info["interface"])
        schedule: Dict[str, List[float]] = self.edf_algo.run()
        if not info["interface"].current_time % 100:
            self.polled_pilots[str(info["interface"].current_time)] = info[
                "interface"
            ].last_applied_pilot_signals
            self.polled_charging_rates[str(info["interface"].current_time)] = info[
                "interface"
            ].last_actual_charging_rate
        return (
            np.array(
                [
                    schedule[station_id][0] if station_id in schedule else 0
                    for station_id in self.edf_algo.interface.station_ids
                ]
            )
            - 16
        )


def to_array_dict(list_dict: Dict[str, List[float]]) -> Dict[str, np.ndarray]:
    """ Converts a dictionary of strings to lists to a dictionary of
    strings to numpy arrays.
    """
    return {key: np.array(value) for key, value in list_dict.items()}


class TestIntegration(unittest.TestCase):
    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def setUpClass(cls) -> None:
        timezone = pytz.timezone("America/Los_Angeles")
        start = timezone.localize(datetime(2018, 9, 5))
        end = timezone.localize(datetime(2018, 9, 6))
        period = 5  # minute
        voltage = 220  # volts
        default_battery_power = 32 * voltage / 1000  # kW
        site = "caltech"

        cn = sites.caltech_acn(basic_evse=True, voltage=voltage)

        api_key = "DEMO_TOKEN"
        events = acndata_events.generate_events(
            api_key, site, start, end, period, voltage, default_battery_power
        )

        cls.sch = GymTrainedAlgorithm()
        cls.sch.register_model(EDFWrapper())
        cls.env = make_default_sim_env()
        cls.sch.register_env(cls.env)
        required_interface = GymTrainedInterface

        cls.sim = Simulator(
            deepcopy(cn),
            cls.sch,
            deepcopy(events),
            start,
            period=period,
            verbose=False,
            interface_type=required_interface,
        )
        cls.sim.run()

        with open(
            os.path.join(
                os.path.dirname(__file__), "edf_algo_true_analysis_fields.json"
            )
        ) as infile:
            cls.edf_algo_true_analysis_dict = json.load(infile)

        with open(
            os.path.join(
                os.path.dirname(__file__), "edf_algo_true_datetimes_array.json"
            )
        ) as infile:
            cls.edf_algo_true_datetimes_array = json.load(infile)

        with open(
            os.path.join(os.path.dirname(__file__), "edf_algo_true_info_fields.json")
        ) as infile:
            cls.edf_algo_true_info_dict = json.load(infile)

    def test_aggregate_current(self) -> None:
        np.testing.assert_allclose(
            acnsim.aggregate_current(self.sim),
            np.array(self.edf_algo_true_analysis_dict["aggregate_current"]),
        )

    def _compare_array_dicts(self, array_dict1, array_dict2) -> None:
        self.assertEqual(
            sorted(list(array_dict1.keys())), sorted(list(array_dict2.keys()))
        )
        for key in array_dict1.keys():
            np.testing.assert_allclose(array_dict1[key], array_dict2[key])

    def test_constraint_currents_all_magnitudes(self) -> None:
        self._compare_array_dicts(
            acnsim.constraint_currents(self.sim),
            to_array_dict(
                self.edf_algo_true_analysis_dict["constraint_currents_all_linear"]
            ),
        )

    def test_constraint_currents_some_magnitudes(self) -> None:
        self._compare_array_dicts(
            acnsim.constraint_currents(
                self.sim, constraint_ids=["Primary A", "Secondary C"]
            ),
            to_array_dict(
                self.edf_algo_true_analysis_dict["constraint_currents_some_linear"]
            ),
        )

    def test_proportion_of_energy_delivered(self) -> None:
        self.assertEqual(
            acnsim.proportion_of_energy_delivered(self.sim),
            self.edf_algo_true_analysis_dict["proportion_of_energy_delivered"],
        )

    def test_proportion_of_demands_met(self) -> None:
        self.assertEqual(
            acnsim.proportion_of_demands_met(self.sim),
            self.edf_algo_true_analysis_dict["proportion_of_demands_met"],
        )

    def test_current_unbalance_nema_error(self) -> None:
        with self.assertRaises(ValueError):
            acnsim.current_unbalance(
                self.sim, ["Primary A", "Primary B", "Primary C"], unbalance_type="ABC"
            )

    def test_current_unbalance_nema_warning(self) -> None:
        with self.assertWarns(DeprecationWarning):
            acnsim.current_unbalance(
                self.sim, ["Primary A", "Primary B", "Primary C"], type="NEMA"
            )

    def test_current_unbalance_nema(self) -> None:
        # A RuntimeWarning is expected to be raised in this test case as
        # of acnportal v.1.0.3. See Github issue #57 for a discussion of
        # why this occurs.
        with self.assertWarns(RuntimeWarning):
            np.testing.assert_allclose(
                acnsim.current_unbalance(
                    self.sim, ["Primary A", "Primary B", "Primary C"]
                ),
                np.array(
                    self.edf_algo_true_analysis_dict["primary_current_unbalance_nema"]
                ),
                atol=1e-6,
            )
        with self.assertWarns(RuntimeWarning):
            np.testing.assert_allclose(
                acnsim.current_unbalance(
                    self.sim, ["Secondary A", "Secondary B", "Secondary C"]
                ),
                np.array(
                    self.edf_algo_true_analysis_dict["secondary_current_unbalance_nema"]
                ),
                atol=1e-6,
            )

    def test_datetimes_array_tutorial_2(self) -> None:
        np.testing.assert_equal(
            acnsim.datetimes_array(self.sim),
            np.array(
                [
                    np.datetime64(date_time)
                    for date_time in self.edf_algo_true_datetimes_array
                ]
            ),
        )

    def test_tutorial_2(self) -> None:
        old_evse_keys = list(self.edf_algo_true_info_dict["pilot_signals"].keys())
        new_evse_keys = self.sim.network.station_ids
        self.assertEqual(sorted(new_evse_keys), sorted(old_evse_keys))

        edf_algo_new_info_dict = {
            field: self.sim.__dict__[field]
            for field in self.edf_algo_true_info_dict.keys()
        }
        edf_algo_new_info_dict["charging_rates"] = {
            self.sim.network.station_ids[i]: list(
                edf_algo_new_info_dict["charging_rates"][i]
            )
            for i in range(len(self.sim.network.station_ids))
        }
        edf_algo_new_info_dict["pilot_signals"] = {
            self.sim.network.station_ids[i]: list(
                edf_algo_new_info_dict["pilot_signals"][i]
            )
            for i in range(len(self.sim.network.station_ids))
        }

        for evse_key in new_evse_keys:
            len_pilots: int = len(
                self.edf_algo_true_info_dict["pilot_signals"][evse_key]
            )
            true_ps: np.ndarray = np.array(
                self.edf_algo_true_info_dict["pilot_signals"][evse_key]
            )
            curr_ps: np.ndarray = np.array(
                edf_algo_new_info_dict["pilot_signals"][evse_key]
            )
            np.testing.assert_allclose(true_ps, curr_ps[:len_pilots])

            len_cr: int = len(self.edf_algo_true_info_dict["charging_rates"][evse_key])
            true_cr: np.ndarray = np.array(
                self.edf_algo_true_info_dict["charging_rates"][evse_key]
            )
            curr_cr: np.ndarray = np.array(
                edf_algo_new_info_dict["charging_rates"][evse_key]
            )
            np.testing.assert_allclose(true_cr, curr_cr[:len_cr])

        self.assertEqual(
            edf_algo_new_info_dict["peak"], self.edf_algo_true_info_dict["peak"]
        )

    def test_lap_interface_func(self) -> None:
        with open(
            os.path.join(os.path.dirname(__file__), "edf_algo_pilot_signals.json")
        ) as infile:
            self.edf_algo_true_lap = json.load(infile)

        if isinstance(self.sch.model, EDFWrapper):
            self.assertDictEqual(self.edf_algo_true_lap, self.sch.model.polled_pilots)

    def test_cr_interface_func(self) -> None:
        with open(
            os.path.join(os.path.dirname(__file__), "edf_algo_charging_rates.json")
        ) as infile:
            self.edf_algo_true_cr = json.load(infile)

        self.assertDictEqual(
            self.edf_algo_true_cr, self.sch.model.polled_charging_rates
        )


if __name__ == "__main__":
    unittest.main()
