# coding=utf-8
"""
This module extends the acnportal.acnsim Interface class with Interfaces
that RL agents and gym environments use to obtain information about a
Simulator.
"""
import warnings
from copy import deepcopy
from typing import List, Dict, Optional, Tuple

import numpy as np

from acnportal.acnsim import Interface


class GymTrainedInterface(Interface):
    """ Interface between OpenAI Environments and the ACN Simulation
     Environment.
    """

    # TODO (sunash): The return type of this should actually be the type
    #  of cls.
    @classmethod
    def from_interface(cls, interface: Interface) -> "GymTrainedInterface":
        """
        Generates an instance of this class from an Interface-like
        object. Note that the _simulator of the input interface is not
        copied into the new GymTrainedInterface-like object generated
        here, so changes from elsewhere to the _simulator will be
        reflected in this object's _simulator.

        Args:
            interface (Interface):

        Returns:
            GymTrainedInterface:

        """
        # To make a new interface from an old one, we must access the
        # old Interface's Simulator even if the _simulator attribute is
        # protected.
        # noinspection PyProtectedMember
        gym_interface = cls(interface._simulator)
        return gym_interface

    @property
    def station_ids(self) -> List[str]:
        """ Return a list of space ids of stations the in the network.

        Returns:
            List[str]: List of station ids in the network.
        """
        return self._simulator.network.station_ids

    @property
    def active_station_ids(self) -> List[str]:
        """ Returns a list of active EVSE station ids for use by the
        algorithm.

        Returns:
            List[str]: List of EVSE station ids with an EV plugged in
                that is not finished charging.
        """
        return self._simulator.network.active_station_ids

    @property
    def is_done(self) -> bool:
        """ Returns if the simulation is complete (i.e. event queue is
        empty).

        Returns:
            bool: True if simulation is complete.
        """
        return self._simulator.event_queue.empty()

    @property
    def charging_rates(self) -> np.ndarray:
        """ Returns the charging_rates of the simulator at all times.

        Returns:
            np.ndarray: numpy array of all charging rates. Each row
                represents the charging rates of a station; each column
                represents the charging rates at an iteration.
        """
        return deepcopy(self._simulator.charging_rates)

    def is_feasible_evse(self, load_currents: Dict[str, List[float]]) -> bool:
        """
        Return if each EVSE in load_currents can accept the pilots
        assigned to it.

        Args:
            load_currents (Dict[str, List[number]]): Dictionary mapping
                load_ids to schedules of charging rates.

        Returns: bool: True if all pilots are valid for the EVSEs to
            which they are sent.
        """
        evse_satisfied = True
        for station_id in load_currents:
            # Check that each EVSE in the schedule is actually in the
            # network.
            if station_id not in self.station_ids:
                raise KeyError(
                    f"Station {station_id} in schedule but not found " f"in network."
                )
            # Check that none of the EVSE pilot signal limits are
            # violated.
            evse_is_continuous, evse_allowable_pilots = self.allowable_pilot_signals(
                station_id
            )
            if evse_is_continuous:
                min_rate = evse_allowable_pilots[0]
                max_rate = evse_allowable_pilots[1]
                evse_satisfied = np.all(
                    np.array(
                        [
                            (min_rate <= pilot <= max_rate) or pilot == 0
                            for pilot in load_currents[station_id]
                        ]
                    )
                )
            else:
                evse_satisfied = np.all(
                    np.isin(
                        np.array(load_currents[station_id]),
                        np.array(evse_allowable_pilots),
                    )
                )
            if not evse_satisfied:
                break
        return evse_satisfied

    def is_feasible(
        self,
        load_currents: Dict[str, List[float]],
        linear: bool = False,
        violation_tolerance: Optional[float] = None,
        relative_tolerance: Optional[float] = None,
    ) -> bool:
        """ Overrides Interface.is_feasible with extra feasibility
        checks. These include:

        - Checking for stations in a schedule but not in the network.
        - Checking that the schedule doesn't violate any constraints on
        EVSE charging rates.
        """
        # Check if conditions of standard Interface.is_feasible are
        # violated.
        constraints_satisfied = super().is_feasible(
            load_currents,
            linear=linear,
            violation_tolerance=violation_tolerance,
            relative_tolerance=relative_tolerance,
        )

        evse_satisfied = self.is_feasible_evse(load_currents)

        return constraints_satisfied and evse_satisfied

    def last_energy_delivered(self) -> float:
        """ Return the actual energy delivered in the last period, in
        amp-periods.

        TODO: This is known to produce a warning in acnportal 0.2.2

        Returns:
            float: Total energy delivered in the last period, in
                amp-periods.
        """
        return sum([ev.current_charging_rate for ev in self._active_evs])

    # TODO: Docs and typing for this function.
    def current_constraint_currents(self, input_schedule: object) -> object:
        """
        TODO
        Args:
            input_schedule:

        Returns:

        """
        return abs(
            self._simulator.network.constraint_current(input_schedule, time_indices=[0])
        )


class GymTrainingInterface(GymTrainedInterface):
    """ Interface between OpenAI Environments and the ACN Simulation
     Environment.

    This class of interface facilitates training by allowing an agent
    to step the Simulator by a single iteration.
    """

    def step(
        self, new_schedule: Dict[str, List[float]], force_feasibility: bool = True
    ) -> Tuple[bool, bool]:
        """ Step the simulation using the input new_schedule until the
        simulator requires a new charging schedule. If the provided
        schedule is infeasible, steps the simulation only if
        `force_feasibility` is `False`, otherwise doesn't step the
        simulation.

        Args:
            new_schedule (Dict[str, List[float]]): Dictionary mapping
            station ids to a schedule of pilot signals.
            force_feasibility (bool): If True, do not allow an

        Returns:
            bool: True if the simulation is completed
            bool: True if the schedule was feasible

        Warns:
            UserWarning: If the length of the new schedule is less than
                the Simulator's `max_recompute` parameter. This warning
                is raised because stepping the Simulator with a schedule
                of length less than `max_recompute` could cause the
                pilot signals to be updated with 0's after the schedule
                runs out of entries.
        """
        # Check that length of new schedules is not less than
        # max_recompute.
        if (
            len(new_schedule) == 0
            or self._simulator.max_recompute is None
            or len(list(new_schedule.values())[0]) < self._simulator.max_recompute
        ):
            warnings.warn(
                f"Length of schedules is less than this simulation's "
                f"max_recompute parameter "
                f"{self._simulator.max_recompute}. Pilots may be "
                f"updated with zeros."
            )

        # If max_recompute is not 1, resolve will need to be set manually to False
        # to initiate the while loop in step().
        if self._simulator._resolve:
            self._simulator._resolve = False

        schedule_is_feasible = self.is_feasible(new_schedule)
        if force_feasibility and not schedule_is_feasible:
            warnings.warn(
                "Passing an infeasible schedule to environment while "
                "force_feasibility=True.Environment will not progress."
            )
            return self._simulator.event_queue.empty(), schedule_is_feasible
        return self._simulator.step(new_schedule), schedule_is_feasible
