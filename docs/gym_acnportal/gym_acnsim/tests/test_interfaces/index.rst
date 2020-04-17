:mod:`gym_acnportal.gym_acnsim.tests.test_interfaces`
=====================================================

.. py:module:: gym_acnportal.gym_acnsim.tests.test_interfaces

.. autoapi-nested-parse::

   Tests for Interfaces to Simulators used by gym_acnsim environments.



Module Contents
---------------


.. py:class:: TestGymTrainedInterface(methodName='runTest')

   Bases: :class:`acnportal.acnsim.tests.test_interface.TestInterface`

   .. method:: setUp(self)



   .. method:: test_station_ids(self)



   .. method:: test_active_station_ids(self)



   .. method:: test_is_done(self)



   .. method:: test_charging_rates(self)



   .. method:: test_is_feasible_evse_key_error(self)



   .. method:: _continuous_evse_helper(self)



   .. method:: test_is_feasible_evse_continuous_infeasible(self)



   .. method:: test_is_feasible_evse_continuous_feasible(self)



   .. method:: _discrete_evse_helper(self)



   .. method:: test_is_feasible_evse_discrete_infeasible(self)



   .. method:: test_is_feasible_evse_discrete_feasible(self)



   .. method:: test_is_feasible(self, mocked_is_feasible)



   .. method:: test_last_energy_delivered(self)



   .. method:: test_current_constraint_currents(self, mocked_constraint_current)




.. py:class:: TestGymTrainingInterface(methodName='runTest')

   Bases: :class:`gym_acnportal.gym_acnsim.tests.test_interfaces.TestGymTrainedInterface`

   .. method:: setUp(self)



   .. method:: test_step_warning_no_schedules(self)



   .. method:: test_step_warning_short_schedule(self)



   .. method:: _step_helper(self)



   .. method:: test_step_infeasible_schedule(self, mocked_is_feasible)



   .. method:: test_step_feasible_schedule(self, mocked_is_feasible)



   .. method:: test_step_infeasible_schedule_no_force_feasibility(self, mocked_is_feasible)




