:mod:`gym_acnportal.gym_acnsim.envs.reward_functions`
=====================================================

.. py:module:: gym_acnportal.gym_acnsim.envs.reward_functions

.. autoapi-nested-parse::

   Module containing definitions of various reward functions for use with
   gym_acnsim environments.

   All reward functions have signature

       acnportal.acnsim.gym_acnsim.envs.env.BaseSimEnv -> Number

   That is, reward functions take in an environment instance
   and return a number (reward) based on the characteristics of that
   environment; namely, the previous state, previous action, and current
   state.



Module Contents
---------------


.. function:: evse_violation(env: BaseSimEnv) -> float

   If a single EVSE constraint was violated by the last schedule, a
   negative reward equal to the magnitude of the violation is added to
   the total reward.

   Raises:
       KeyError: If a station_id in the last schedule is not found in
           the ChargingNetwork.


.. function:: unplugged_ev_violation(env: BaseSimEnv) -> float

   If charge is attempted to be delivered to an EVSE with no EV, or to
   an EVSE with an EV that is done charging, the charging rate is
   subtracted from the reward. This penalty is only applied to the
   schedules for the current iteration.


.. function:: current_constraint_violation(env: BaseSimEnv) -> float

   If a network constraint is violated, a negative reward equal to the
   norm of the total constraint violation, times the number of EVSEs,
   is added. Only penalizes for actions in the current timestep.


.. function:: soft_charging_reward(env: BaseSimEnv) -> float

   Rewards for charge delivered in the last timestep.


.. function:: hard_charging_reward(env: BaseSimEnv) -> float

   Rewards for charge delivered in the last timestep, but only
   if constraint and evse violations are 0.


