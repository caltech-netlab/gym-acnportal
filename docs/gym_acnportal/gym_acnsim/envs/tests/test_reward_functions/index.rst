:mod:`gym_acnportal.gym_acnsim.envs.tests.test_reward_functions`
================================================================

.. py:module:: gym_acnportal.gym_acnsim.envs.tests.test_reward_functions

.. autoapi-nested-parse::

   Tests for reward functions. 



Module Contents
---------------


.. py:class:: TestRewardFunction(methodName='runTest')

   Bases: :class:`unittest.TestCase`

   .. attribute:: simulator
      :annotation: :Simulator

      

   .. method:: setUp(self)




.. py:class:: TestEVSEViolation(methodName='runTest')

   Bases: :class:`gym_acnportal.gym_acnsim.envs.tests.test_reward_functions.TestRewardFunction`

   .. method:: setUp(self)



   .. method:: test_evse_violation_key_error(self)



   .. method:: _continuous_evse_helper(self)



   .. method:: test_evse_violation_continuous_violation(self)



   .. method:: test_evse_violation_continuous_no_violation(self)



   .. method:: _discrete_evse_helper(self)



   .. method:: test_evse_violation_non_continuous_violation(self)



   .. method:: test_evse_violation_non_continuous_no_violation(self)




.. py:class:: TestUnpluggedEVViolation(methodName='runTest')

   Bases: :class:`gym_acnportal.gym_acnsim.envs.tests.test_reward_functions.TestRewardFunction`

   .. method:: setUp(self)



   .. method:: test_unplugged_ev_violation_empty_schedules(self)



   .. method:: test_unplugged_ev_violation_all_unplugged(self)



   .. method:: test_unplugged_ev_violation_some_unplugged(self)



   .. method:: test_unplugged_ev_violation_none_unplugged(self)




.. py:class:: TestConstraintViolation(methodName='runTest')

   Bases: :class:`gym_acnportal.gym_acnsim.envs.tests.test_reward_functions.TestRewardFunction`

   .. method:: setUp(self)



   .. method:: test_constraint_violation_no_action(self)



   .. method:: test_constraint_violation_with_violating_action_matrix(self)



   .. method:: test_constraint_violation_no_violation_action_matrix(self)



   .. method:: test_constraint_violation_with_violating_action_vector(self)



   .. method:: test_constraint_violation_no_violation_action_vector(self)




.. py:class:: TestSoftChargingReward(methodName='runTest')

   Bases: :class:`gym_acnportal.gym_acnsim.envs.tests.test_reward_functions.TestRewardFunction`

   .. method:: setUp(self)



   .. method:: test_soft_charging_reward(self)




