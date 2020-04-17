:mod:`gym_acnportal.gym_acnsim.envs.base_env`
=============================================

.. py:module:: gym_acnportal.gym_acnsim.envs.base_env

.. autoapi-nested-parse::

   This module contains an abstract gym environment that wraps an ACN-Sim
   Simulation.



Module Contents
---------------


.. py:class:: BaseSimEnv(interface: Optional[GymTrainedInterface])

   Bases: :class:`gym.Env`

   Abstract base class meant to be inherited from to implement
   new ACN-Sim Environments.

   Subclasses must implement the following methods:
       action_to_schedule
       observation_from_state
       reward_from_state
       done_from_state

   Subclasses must also specify observation_space and action_space,
   either as class or instance variables.

   Optionally, subclasses may implement info_from_state, which here
   returns an empty dict.

   Subclasses may override __init__, step, and reset functions.

   Currently, no render function is implemented, though this function
   is not required for internal functionality.

   Attributes:
       _interface (GymTrainedInterface): An interface to a simulation to be
           stepped by this environment, or None. If None, an interface must
           be set later.
       _init_snapshot (GymTrainedInterface): A deep copy of the initial
           interface, used for environment resets.
       _prev_interface (GymTrainedInterface): A deep copy of the interface
           at the previous time step; used for calculating action
           rewards.
       _action (object): The action taken by the agent in this
           agent-environment loop iteration.
       _schedule (Dict[str, List[number]]): Dictionary mapping
           station ids to a schedule of pilot signals.
       _observation (np.ndarray): The observation given to the agent in
           this agent-environment loop iteration.
       _done (object): An object representing whether or not the
           execution of the environment is complete.
       _info (object): An object that gives info about the environment.

   .. attribute:: _interface
      :annotation: :Optional[GymTrainedInterface]

      

   .. attribute:: _init_snapshot
      :annotation: :GymTrainedInterface

      

   .. attribute:: _prev_interface
      :annotation: :GymTrainedInterface

      

   .. attribute:: _action
      :annotation: :Optional[np.ndarray]

      

   .. attribute:: _schedule
      :annotation: :Dict[str, List[float]]

      

   .. attribute:: _observation
      :annotation: :Optional[np.ndarray]

      

   .. attribute:: _reward
      :annotation: :Optional[float]

      

   .. attribute:: _done
      :annotation: :Optional[bool]

      

   .. attribute:: _info
      :annotation: :Optional[Dict[Any, Any]]

      

   .. method:: interface(self)
      :property:



   .. method:: prev_interface(self)
      :property:



   .. method:: action(self)
      :property:



   .. method:: schedule(self)
      :property:



   .. method:: observation(self)
      :property:



   .. method:: reward(self)
      :property:



   .. method:: done(self)
      :property:



   .. method:: info(self)
      :property:



   .. method:: update_state(self)


      Update the state of the environment. Namely, the
      observation, reward, done, and info attributes of the
      environment.

      Returns:
          None.


   .. method:: store_previous_state(self)


      Store the previous state of the simulation in the
      _prev_interface environment attribute.

      Returns:
          None.


   .. method:: step(self, action: np.ndarray)


      Step the simulation one timestep with an agent's action.

      Accepts an action and returns a tuple (observation, reward,
      done, info).

      Implements gym.Env.step()

      Args:
          action (object): an action provided by the agent

      Returns:
          observation (np.ndarray): agent's observation of the current
              environment
          reward (float) : amount of reward returned after previous
              action
          done (bool): whether the episode has ended, in which case
              further step() calls will return undefined results
          info (dict): contains auxiliary diagnostic information
              (helpful for debugging, and sometimes learning)


   .. method:: reset(self)


      Resets the state of the simulation and returns an initial
      observation. Resetting is done by setting the interface to the
      simulation to an interface to the simulation in its initial
      state.

      Implements gym.Env.reset()

      Returns:
          observation (np.ndarray): the initial observation.


   .. method:: render(self, mode='human')
      :abstractmethod:


      Renders the environment. Implements gym.Env.render(). 


   .. method:: action_to_schedule(self)
      :abstractmethod:


      Convert an agent action to a schedule to be input to the
      simulator.

      Returns:
          schedule (Dict[str, List[float]]): Dictionary mapping
              station ids to a schedule of pilot signals.


   .. method:: observation_from_state(self)
      :abstractmethod:


      Construct an environment observation from the state of the
      simulator

      Returns:
          observation (Dict[str, np.ndarray]): an environment
              observation generated from the simulation state


   .. method:: reward_from_state(self)
      :abstractmethod:


      Calculate a reward from the state of the simulator

      Returns:
          reward (float): a reward generated from the simulation
          state


   .. method:: done_from_state(self)
      :abstractmethod:


      Determine if the simulation is done from the state of the
      simulator

      Returns:
          done (bool): True if the simulation is done, False if not


   .. method:: info_from_state(self)
      :abstractmethod:


      Give information about the environment using the state of
      the simulator

      Returns:
          info (dict): dict of environment information



