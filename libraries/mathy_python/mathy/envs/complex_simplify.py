from typing import Any, Dict, List, Optional, Type

from ..mathy_env import MathyEnvProblem
from ..problems import simplify_multiple_terms
from ..rules import (
    AssociativeSwapRule,
    ConstantsSimplifyRule,
    VariableMultiplyRule,
)
from ..core.rule import BaseRule
from ..state import MathyEnvState
from ..types import MathyEnvDifficulty, MathyEnvProblemArgs
from .poly_simplify import PolySimplify
from numpy.random import randint, uniform


class ComplexSimplify(PolySimplify):
    """A Mathy environment for simplifying complex terms (e.g. 4x^3 * 7y) inside of
    expressions. The goal is to simplify the complex term within the allowed number
    of environment steps.
    """

    def get_env_namespace(self) -> str:
        return "mathy.monomials.complex_simplify"

    def max_moves_fn(
        self, problem: MathyEnvProblem, config: MathyEnvProblemArgs
    ) -> int:
        return problem.complexity * 3

    def problem_fn(self, params: MathyEnvProblemArgs) -> MathyEnvProblem:
        """Given a set of parameters to control term generation, produce
        a complex term that has a simple representation that must be found.
        - "4x * 2y^2 * 7q"
        - "7j * 2z^6"
        - "x * 2y^7 * 8z * 2x"
        """

        if params.difficulty == MathyEnvDifficulty.easy:
            num_terms = randint(2, 6)
            scaling = uniform(0.5, 0.9)
            text, complexity = simplify_multiple_terms(
                num_terms,
                op="*",
                optional_var=True,
                inner_terms_scaling=scaling,
                powers_probability=0.4,
                noise_probability=0.2,
            )
        elif params.difficulty == MathyEnvDifficulty.normal:
            num_terms = randint(3, 6)
            scaling = uniform(0.5, 0.85)
            text, complexity = simplify_multiple_terms(
                num_terms,
                op="*",
                optional_var=True,
                inner_terms_scaling=scaling,
                powers_probability=0.6,
            )
        elif params.difficulty == MathyEnvDifficulty.hard:
            num_terms = randint(4, 8)
            scaling = uniform(0.2, 0.6)
            text, complexity = simplify_multiple_terms(
                num_terms,
                op="*",
                shuffle_probability=0.5,
                powers_probability=0.8,
                inner_terms_scaling=scaling,
            )
        else:
            raise ValueError(f"Unknown difficulty: {params.difficulty}")
        return MathyEnvProblem(text, complexity, self.get_env_namespace())