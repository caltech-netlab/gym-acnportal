# coding=utf-8
"""
Open AI Gym plugin for ACN-Sim. Provides several customizable
environments for training reinforcement learning (RL) agents. See
tutorial X for examples of usage.
"""
from typing import List, Dict

from gym.envs import registry
from gym.envs.registration import register, EnvSpec
from .interfaces import GymTrainedInterface, GymTrainingInterface
from .envs import *

all_envs: List[EnvSpec] = list(registry.all())
env_ids = [env_spec.id for env_spec in all_envs]
gym_env_dict: Dict[str, str] = {
    "custom-acnsim-v0": "gym_acnportal.gym_acnsim.envs:CustomSimEnv",
    "default-acnsim-v0": "gym_acnportal.gym_acnsim.envs:make_default_sim_env",
    "rebuilding-acnsim-v0": "gym_acnportal.gym_acnsim.envs:RebuildingEnv",
    "default-rebuilding-acnsim-v0": "gym_acnportal.gym_acnsim.envs:make_rebuilding_default_sim_env",
}
for env_name, env_entry_point in gym_env_dict.items():
    if env_name not in env_ids:
        register(id=env_name, entry_point=env_entry_point)
del register, registry, all_envs, gym_env_dict, List, Dict
