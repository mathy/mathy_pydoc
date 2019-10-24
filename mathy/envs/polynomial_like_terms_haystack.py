from typing import Any, List, Optional, Type, Union, Dict

from numpy import random
from numpy.random import randint
from tf_agents.trajectories import time_step
from ..helpers import get_term_ex, get_terms, TermEx

from ..state import MathyEnvState, MathyObservation, MathyEnvTimeStep
from ..rules.rule import BaseRule
from ..core.expressions import MathExpression
from ..mathy_env import MathyEnvProblem
from ..problems import (
    combine_terms_in_place,
    get_rand_term_templates,
    mathy_term_string,
    get_rand_vars,
    maybe_int,
    maybe_power,
    rand_bool,
    rand_op,
    rand_var,
    split_in_two_random,
)
from ..util import GameRewards
from ..types import MathyEnvDifficulty, MathyEnvProblemArgs
from .polynomial_simplification import MathyPolynomialSimplificationEnv


class MathyPolynomialLikeTermsHaystackEnv(MathyPolynomialSimplificationEnv):
    """Act on any node in the expression that has another term like it
    somewhere else. For example in the problem:

    2x + 8 + 13.2y + z^2 + 5x
    ^^---------------------^^

    Applying any rule to one of those nodes is a win. The idea here is that
    in order to succeed at this task, the model must build a representation
    that can identify like terms in a large expression tree.
    """

    def transition_fn(
        self,
        env_state: MathyEnvState,
        expression: MathExpression,
        features: MathyObservation,
    ) -> Optional[time_step.TimeStep]:
        """If all like terms are siblings."""
        agent = env_state.agent
        if len(agent.history) == 0:
            return None

        last_timestep: MathyEnvTimeStep = agent.history[-1]

        action_node = self.get_token_at_index(expression, last_timestep.focus)
        touched_term = get_term_ex(action_node)
        term_nodes = get_terms(expression)
        # We have the token_index of the term that was acted on, now we have to see
        # if that term has any like siblings (not itself). We do this by ignoring the
        # term with a matching r_index to the node the agent acted on.
        #
        # find_nodes updates the `r_index` value on each node which is the token index
        BaseRule().find_nodes(expression)

        like_counts: Dict[str, int] = {}
        all_indices: Dict[str, List[int]] = {}
        max_index = 0
        for term_node in term_nodes:
            max_index = max(max_index, term_node.r_index)
            ex: Optional[TermEx] = get_term_ex(term_node)
            if ex is None:
                continue

            key = mathy_term_string(variable=ex.variable, exponent=ex.exponent)
            if key not in like_counts:
                like_counts[key] = 1
            else:
                like_counts[key] += 1
            if key not in all_indices:
                all_indices[key] = [term_node.r_index]
            else:
                all_indices[key].append(term_node.r_index)

        like_indices: Optional[List[int]] = None
        for key in all_indices.keys():
            if len(all_indices[key]) > 1:
                like_indices = all_indices[key]
        assert (
            like_indices is not None and len(like_indices) > 1
        ), "must have at least one group of like terms"

        if action_node is not None and touched_term is not None:
            touched_key = mathy_term_string(
                variable=touched_term.variable, exponent=touched_term.exponent
            )
            if touched_key in like_counts and like_counts[touched_key] > 1:
                action_node.all_changed()
                return time_step.termination(features, self.get_win_signal(env_state))

        distances = []
        for index in like_indices:
            distances.append(abs(index - action_node.r_index))  # type:ignore
        loss_magnitude = min(distances) / max_index
        lose_signal = GameRewards.LOSE - loss_magnitude
        return time_step.termination(features, lose_signal)

    def get_env_namespace(self) -> str:
        return "mathy.polynomials.haystack.like.terms"

    def make_problem(
        self,
        min_terms: int,
        max_terms: int,
        like_terms: int,
        exponent_probability: float,
    ) -> str:
        assert min_terms <= max_terms, "min cannot be greater than max"
        assert like_terms < min_terms, "must have atleast one term that is not like"
        out_terms = []
        total_terms = random.randint(min_terms, max_terms)
        num_diff_terms = total_terms - like_terms
        diff_term_tpls = get_rand_term_templates(
            num_diff_terms + 1, exponent_probability=exponent_probability
        )
        like_term_tpl = diff_term_tpls[-1]
        diff_term_tpls = diff_term_tpls[:-1]

        for i in range(like_terms):
            out_terms.append(like_term_tpl.make())

        for tpl in diff_term_tpls:
            out_terms.append(tpl.make())
        random.shuffle(out_terms)
        problem = f" + ".join(out_terms)
        return problem

    def problem_fn(self, params: MathyEnvProblemArgs) -> MathyEnvProblem:
        if params.difficulty == MathyEnvDifficulty.easy:
            text = self.make_problem(
                min_terms=3, max_terms=6, like_terms=2, exponent_probability=0.3
            )
        elif params.difficulty == MathyEnvDifficulty.normal:
            text = self.make_problem(
                min_terms=4, max_terms=7, like_terms=2, exponent_probability=0.5
            )
        elif params.difficulty == MathyEnvDifficulty.hard:
            text = self.make_problem(
                min_terms=5, max_terms=12, like_terms=2, exponent_probability=0.4
            )
        else:
            raise ValueError(f"Unknown difficulty: {params.difficulty}")
        return MathyEnvProblem(text, 1, self.get_env_namespace())
