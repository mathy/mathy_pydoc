from typing import Optional, Type, List

import gym
from ...mathy_env import MathyEnv
from ...rules.rule import ExpressionChangeRule
from ...core.expressions import MathExpression
from ...state import (
    MathyEnvState,
    MathyObservation,
    RNNStatesFloatList,
    rnn_placeholder_state,
)
from ...types import MathyEnvProblemArgs
from ...util import is_terminal_transition
from .masked_discrete import MaskedDiscrete
import numpy as np
import math


class MathyGymEnv(gym.Env):
    """A small wrapper around Mathy envs to allow them to work with OpenAI Gym. The
    agents currently use this env wrapper, but it could be dropped in the future."""

    default_rnn_size = 128
    metadata = {"render.modes": ["terminal", "attention"]}
    mathy: MathyEnv
    state: Optional[MathyEnvState]
    problem: Optional[str]
    env_class: Type[MathyEnv]
    env_problem_args: Optional[MathyEnvProblemArgs]
    last_action: int
    last_reward: float
    last_change: Optional[ExpressionChangeRule]

    def __init__(
        self,
        env_class: Type[MathyEnv] = MathyEnv,
        env_problem_args: Optional[MathyEnvProblemArgs] = None,
        **env_kwargs,
    ):
        self.mathy = env_class(**env_kwargs)
        self.env_class = env_class
        self.env_problem_args = env_problem_args
        if self.env_problem_args is not None and not isinstance(
            self.env_problem_args, MathyEnvProblemArgs
        ):
            raise ValueError("Problem args must be a MathyEnvProblemArgs instance")

        self.last_action = -1
        self.last_change = None
        self.last_reward = 0.0
        max_nodes = 1024
        max_actions = self.mathy.action_size
        vector_width = 1  # a single number
        self.state = None
        self.problem = None
        self.vectors_shape = (max_nodes, vector_width)
        self.action_space = MaskedDiscrete(max_actions, [1] * max_actions)

    @property
    def action_size(self) -> int:
        if self.state is not None:
            return self.mathy.get_agent_actions_count(self.state)
        return self.mathy.action_size

    def step(self, action):
        self.state, transition, change = self.mathy.get_next_state(self.state, action)
        observation = self._observe(self.state)
        info = {"transition": transition}
        done = is_terminal_transition(transition)
        self.last_action = action
        self.last_change = change
        self.last_reward = round(float(transition.reward), 4)
        return observation, transition.reward, done, info

    def reset(self, rnn_size=default_rnn_size):
        self.rnn_size = rnn_size
        self.last_action = -1
        self.last_change = None
        self.last_reward = 0.0
        # If the episode is being reset because it ended, assert the validity
        # of the last problem outcome
        if self.state is not None:
            self.mathy.finalize_state(self.state)
        self.state, self.problem = self.mathy.get_initial_state(self.env_problem_args)
        return self._observe(self.state)

    def initial_state(self):
        """return a batch of n-step observations for initializing the env"""
        state, _ = self.mathy.get_initial_state(self.env_problem_args)
        return state.to_empty_batch()

    def start_observation(self, rnn_state: RNNStatesFloatList):
        """return an n-step set of observations for initializing the env"""
        state, _ = self.mathy.get_initial_state(self.env_problem_args)
        return state.to_start_observation(rnn_state)

    def initial_window(self, rnn_size: int):
        """return an n-step set of observations for initializing the env"""
        state, _ = self.mathy.get_initial_state(self.env_problem_args)
        return state.to_empty_window(1, rnn_size)

    def _observe(self, state: MathyEnvState) -> MathyObservation:
        """Observe the environment at the given state, updating the observation
        space and action space for the given state. """
        action_mask = self.mathy.get_valid_moves(state)
        observation = self.mathy.state_to_observation(state, rnn_size=self.rnn_size)
        self.action_space.n = self.mathy.get_agent_actions_count(state)
        self.action_space.mask = action_mask
        return observation

    def render(self, mode="terminal", data=None):
        if mode == "attention" and self.last_change is not None:
            assert data is not None, "attention weights required for this render mode"
            attention_layers = [d.numpy() for d in data]
            nodes = self.last_change.result.toList()
            for layer in attention_layers:
                multi_head_layer = np.array(layer)
                # NOTE: this is kind of gross, but I'm not sure how to print all the
                # layer<->heads without interaction to conditionally show them or
                # massive output spam. If you were looking at one state it would be
                # fine, but as a sequence of states in solving a problem, it's really
                # spammy.
                #
                # TODO: As a hack we mean the whole thing along two axes :shrug:
                mean_weights = multi_head_layer.mean(axis=0).mean(axis=0)
                # Parse the expression, and associate the weights with it
                for i, node in enumerate(nodes):
                    if i < len(mean_weights):
                        node.set_weight(mean_weights[i])
                    else:
                        node.set_weight(0.0)

        action_name = "initial"
        token_index = -1
        if self.last_action != -1 and self.last_change is not None:
            action_index, token_index = self.mathy.get_action_indices(self.last_action)
            action_name = self.mathy.rules[action_index].name
        else:
            print(f"Problem: {self.state.agent.problem}")
        self.mathy.print_state(
            self.state,
            action_name[:25].lower(),
            token_index,
            change=self.last_change,
            change_reward=self.last_reward,
        )