:mod:`gym_acnportal.gym_acnsim.envs.tests.test_action_spaces`
=============================================================

.. py:module:: gym_acnportal.gym_acnsim.envs.tests.test_action_spaces

.. autoapi-nested-parse::

   Tests for SimAction and action space functions. 



Module Contents
---------------


.. py:class:: TestSimAction(methodName='runTest')

   Bases: :class:`unittest.TestCase`

   .. method:: setUpClass(cls)
      :classmethod:



   .. method:: test_correct_on_init_sim_action_name(self)



   .. method:: test_get_space(self)



   .. method:: test_get_schedule(self)




.. py:class:: TestSingleChargingSchedule(methodName='runTest')

   Bases: :class:`unittest.TestCase`

   .. attribute:: max_rate
      :annotation: :float = 16.0

      

   .. attribute:: min_rate
      :annotation: :float = 0.0

      

   .. attribute:: negative_rate
      :annotation: :float

      

   .. attribute:: deadband_rate
      :annotation: :float = 6.0

      

   .. method:: setUpClass(cls)
      :classmethod:



   .. method:: test_correct_on_init_single_name(self)



   .. method:: _test_space_function_helper(self, interface: GymTrainedInterface, min_rate: float, max_rate: float)



   .. method:: test_single_space_function(self)



   .. method:: test_single_space_function_negative_min(self)



   .. method:: test_single_space_function_deadband_min(self)



   .. method:: test_single_to_schedule(self)



   .. method:: test_single_to_bad_schedule(self)



   .. method:: test_single_error_schedule(self)




.. py:class:: TestZeroCenteredSingleChargingSchedule(methodName='runTest')

   Bases: :class:`gym_acnportal.gym_acnsim.envs.tests.test_action_spaces.TestSingleChargingSchedule`

   .. method:: setUpClass(cls)
      :classmethod:



   .. method:: test_correct_on_init_single_name(self)



   .. method:: test_single_space_function(self)



   .. method:: test_single_space_function_negative_min(self)



   .. method:: test_single_space_function_deadband_min(self)



   .. method:: test_single_to_bad_schedule(self)



   .. method:: test_single_to_schedule(self)




