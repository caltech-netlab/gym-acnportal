:mod:`gym_acnportal.gym_acnsim.envs.tests.test_observation`
===========================================================

.. py:module:: gym_acnportal.gym_acnsim.envs.tests.test_observation

.. autoapi-nested-parse::

   Tests for SimObservation and observation generating functions. 



Module Contents
---------------


.. py:class:: TestSimObservation(methodName='runTest')

   Bases: :class:`unittest.TestCase`

   .. method:: setUpClass(cls)
      :classmethod:



   .. method:: test_correct_on_init_sim_observation_name(self)



   .. method:: test_get_space(self)



   .. method:: test_get_schedule(self)




.. py:class:: TestEVObservationClass(methodName='runTest')

   Bases: :class:`unittest.TestCase`

   .. method:: setUpClass(cls)
      :classmethod:



   .. method:: test_space_function(self)



   .. method:: test_correct_on_init_name(self)




.. py:class:: TestArrivalObservation(methodName='runTest')

   Bases: :class:`gym_acnportal.gym_acnsim.envs.tests.test_observation.TestEVObservationClass`

   .. method:: setUpClass(cls)
      :classmethod:



   .. method:: test_arrival_observation(self)




.. py:class:: TestDepartureObservation(methodName='runTest')

   Bases: :class:`gym_acnportal.gym_acnsim.envs.tests.test_observation.TestEVObservationClass`

   .. method:: setUpClass(cls)
      :classmethod:



   .. method:: test_departure_observation(self)




.. py:class:: TestDemandObservation(methodName='runTest')

   Bases: :class:`gym_acnportal.gym_acnsim.envs.tests.test_observation.TestEVObservationClass`

   .. method:: setUpClass(cls)
      :classmethod:



   .. method:: test_departure_observation(self)




.. py:class:: TestConstraintObservation(methodName='runTest')

   Bases: :class:`unittest.TestCase`

   .. attribute:: interface
      :annotation: :Any

      

   .. method:: setUpClass(cls)
      :classmethod:



   .. method:: test_space_function(self)



   .. method:: test_correct_on_init_name(self)




.. py:class:: TestConstraintMatrixObservation(methodName='runTest')

   Bases: :class:`gym_acnportal.gym_acnsim.envs.tests.test_observation.TestConstraintObservation`

   .. method:: setUpClass(cls)
      :classmethod:



   .. method:: test_constraint_matrix_observation(self)




.. py:class:: TestMagnitudesObservation(methodName='runTest')

   Bases: :class:`gym_acnportal.gym_acnsim.envs.tests.test_observation.TestConstraintObservation`

   .. method:: setUpClass(cls)
      :classmethod:



   .. method:: test_constraint_matrix_observation(self)




.. py:class:: TestTimestepObservation(methodName='runTest')

   Bases: :class:`unittest.TestCase`

   .. method:: setUpClass(cls)
      :classmethod:



   .. method:: test_space_function(self)



   .. method:: test_correct_on_init_name(self)



   .. method:: test_timestep_observation(self)




