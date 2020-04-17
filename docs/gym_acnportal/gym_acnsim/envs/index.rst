:mod:`gym_acnportal.gym_acnsim.envs`
====================================

.. py:module:: gym_acnportal.gym_acnsim.envs

.. autoapi-nested-parse::

   This package contains environments for training RL agents to schedule EV
   charging.



Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 3

   tests/index.rst


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   action_spaces/index.rst
   base_env/index.rst
   custom_envs/index.rst
   observation/index.rst
   reward_functions/index.rst


Package Contents
----------------


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



.. py:class:: CustomSimEnv(interface: Optional[GymTrainedInterface], observation_objects: List[SimObservation], action_object: SimAction, reward_functions: List[Callable[[BaseSimEnv], float]])

   Bases: :class:`gym_acnportal.gym_acnsim.envs.base_env.BaseSimEnv`

   A simulator environment with customizable observations, action
   spaces, and rewards.

   Observations are specified as objects, where each object specifies a
   function to generate a space from a simulation interface and a
   function to generate an observation from a simulation interface.

   Action spaces are specified as functions that generate a space from
   a simulation interface.

   Rewards are specified as functions that generate a number (reward)
   from an environment.

   Users may define their own objects/functions to input to this
   environment, use the objects/functions defined in the gym_acnsim
   package, or use an environment factory function defined in the
   sim_prototype_env module.

   .. attribute:: observation_objects
      :annotation: :List[SimObservation]

      

   .. attribute:: observation_space
      :annotation: :spaces.Dict

      

   .. attribute:: action_object
      :annotation: :SimAction

      

   .. attribute:: action_space
      :annotation: :spaces.Space

      

   .. attribute:: reward_functions
      :annotation: :List[Callable[[BaseSimEnv], float]]

      

   .. method:: interface(self)
      :property:



   .. method:: render(self, mode='human')
      :abstractmethod:


      Renders the environment. Implements gym.Env.render(). 


   .. method:: action_to_schedule(self)


      Convert an agent action to a schedule to be input to the
      simulator.

      Returns:
          schedule (Dict[str, List[float]]): Dictionary mapping
              station ids to a schedule of pilot signals.


   .. method:: observation_from_state(self)


      Construct an environment observation from the state of the
      simulator using the environment's observation construction
      functions.

      Returns:
          observation (Dict[str, np.ndarray]): An environment
              observation generated from the simulation state


   .. method:: reward_from_state(self)


      Calculate a reward from the state of the simulator

      Returns:
          reward (float): a reward generated from the simulation
              state


   .. method:: done_from_state(self)


      Determine if the simulation is done from the state of the
      simulator

      Returns:
          done (bool): True if the simulation is done, False if not


   .. method:: info_from_state(self)


      Give information about the environment using the state of
      the simulator. In this case, all the info about the simulator
      is given by returning a dict containing the simulator's
      interface.

      Returns:
          info (Dict[str, GymTrainedInterface]): The interface between
              the environment and Simulator.



.. py:class:: RebuildingEnv(interface: Optional[GymTrainedInterface], observation_objects: List[SimObservation], action_object: SimAction, reward_functions: List[Callable[[BaseSimEnv], float]], interface_generating_function: Optional[Callable[[], GymTrainedInterface]] = None)

   Bases: :class:`gym_acnportal.gym_acnsim.envs.custom_envs.CustomSimEnv`

   A simulator environment that subclasses CustomSimEnv, with
   the extra property that the entire simulation is rebuilt within 
   the environment when __init__ or reset are called

   This is especially useful if the network or event queue have 
   stochastic elements.

   .. method:: from_custom_sim_env(cls, env: CustomSimEnv, interface_generating_function: Optional[Callable[[], GymTrainedInterface]] = None)
      :classmethod:



   .. method:: reset(self)


      Resets the state of the simulation and returns an initial 
      observation. Resetting is done by setting the interface to 
      the simulation to an interface to the simulation in its 
      initial state.

      Returns:
          observation (np.ndarray): the initial observation.


   .. method:: render(self, mode='human')
      :abstractmethod:


      Renders the environment. Implements gym.Env.render(). 



.. function:: make_default_sim_env(interface: Optional[GymTrainedInterface] = None) -> CustomSimEnv

   A simulator environment with the following characteristics:

   The action and observation spaces are continuous.

   An action in this environment is a pilot signal for each EVSE,
   within the minimum and maximum EVSE rates.

   An observation is a dict consisting of fields (times are 1-indexed
   in the observations):
       arrivals: arrival time of the EV at each EVSE (or 0 if there's
            no EV plugged in)
       departures: departure time of the EV at each EVSE (or 0 if
           there's no EV plugged in)
       demand: energy demand of the EV at each EVSE (unoccupied
           EVSEs have demand 0)
       constraint_matrix: matrix of aggregate current coefficients
       magnitudes: magnitude vector constraining aggregate currents
       timestep: timestep of the simulation

   The reward is calculated as follows:
       If no constraints (on the network or on the EVSEs) were
           violated by the action,
       a reward equal to the total charge delivered (in A) is
           returned
       If any constraint violation occurred, a negative reward equal
           to the magnitude of the violation is returned.
       Network constraint violations are scaled by the number of EVs
       Finally, a user-input reward function is added to the total
           reward.

   The simulation is considered done if the event queue is empty.


.. function:: make_rebuilding_default_sim_env(interface_generating_function: Optional[Callable[[], GymTrainedInterface]]) -> RebuildingEnv

   A simulator environment with the same characteristics as the
   environment returned by make_default_sim_env except on every reset,
   the simulation is completely rebuilt using interface_generating_function.

   See make_default_sim_env for more info.


.. data:: default_observation_objects
   :annotation: :List[SimObservation]

   

.. data:: default_action_object
   :annotation: :SimAction

   

.. data:: default_reward_functions
   :annotation: :List[Callable[[BaseSimEnv], float]]

   

