:mod:`gym_acnportal.gym_acnsim.interfaces`
==========================================

.. py:module:: gym_acnportal.gym_acnsim.interfaces

.. autoapi-nested-parse::

   This module extends the acnportal.acnsim Interface class with Interfaces
   that RL agents and gym environments use to obtain information about a
   Simulator.



Module Contents
---------------


.. py:class:: GymTrainedInterface(simulator)

   Bases: :class:`acnportal.acnsim.Interface`

   Interface between OpenAI Environments and the ACN Simulation
   Environment.

   .. method:: from_interface(cls, interface: Interface)
      :classmethod:


      Generates an instance of this class from an Interface-like
      object. Note that the _simulator of the input interface is not
      copied into the new GymTrainedInterface-like object generated
      here, so changes from elsewhere to the _simulator will be
      reflected in this object's _simulator.

      Args:
          interface (Interface):

      Returns:
          GymTrainedInterface:


   .. method:: station_ids(self)
      :property:


      Return a list of space ids of stations the in the network.

      Returns:
          List[str]: List of station ids in the network.


   .. method:: active_station_ids(self)
      :property:


      Returns a list of active EVSE station ids for use by the
      algorithm.

      Returns:
          List[str]: List of EVSE station ids with an EV plugged in
              that is not finished charging.


   .. method:: is_done(self)
      :property:


      Returns if the simulation is complete (i.e. event queue is
      empty).

      Returns:
          bool: True if simulation is complete.


   .. method:: charging_rates(self)
      :property:


      Returns the charging_rates of the simulator at all times.

      Returns:
          np.ndarray: numpy array of all charging rates. Each row
              represents the charging rates of a station; each column
              represents the charging rates at an iteration.


   .. method:: is_feasible_evse(self, load_currents: Dict[str, List[float]])


      Return if each EVSE in load_currents can accept the pilots
      assigned to it.

      Args:
          load_currents (Dict[str, List[number]]): Dictionary mapping
              load_ids to schedules of charging rates.

      Returns: bool: True if all pilots are valid for the EVSEs to
          which they are sent.


   .. method:: is_feasible(self, load_currents: Dict[str, List[float]], linear: bool = False, violation_tolerance: Optional[float] = None, relative_tolerance: Optional[float] = None)


      Overrides Interface.is_feasible with extra feasibility
      checks. These include:

      - Checking for stations in a schedule but not in the network.
      - Checking that the schedule doesn't violate any constraints on
      EVSE charging rates.


   .. method:: last_energy_delivered(self)


      Return the actual energy delivered in the last period, in
      amp-periods.

      Returns:
          float: Total energy delivered in the last period, in
              amp-periods.


   .. method:: current_constraint_currents(self, input_schedule: object)


      TODO
      Args:
          input_schedule:

      Returns:



.. py:class:: GymTrainingInterface(simulator)

   Bases: :class:`gym_acnportal.gym_acnsim.interfaces.GymTrainedInterface`

   Interface between OpenAI Environments and the ACN Simulation
    Environment.

   This class of interface facilitates training by allowing an agent
   to step the Simulator by a single iteration.

   .. method:: step(self, new_schedule: Dict[str, List[float]], force_feasibility: bool = True)


      Step the simulation using the input new_schedule until the
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



