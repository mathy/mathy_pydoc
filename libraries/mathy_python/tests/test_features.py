from typing import List, Tuple

import pytest

from ..mathy.envs.polynomial_simplification import MathyPolynomialSimplificationEnv
from ..mathy.state import MathyEnvState, rnn_placeholder_state


def test_mathy_features_from_state():
    with pytest.raises(ValueError):
        state = MathyEnvState()
    state = MathyEnvState(problem="4x+2x")
    assert state.to_observation([]) is not None


def test_mathy_features_hierarchy():
    """Verify that the observation generated encodes hierarchy properly
    so the model can determine the precise nodes to act on"""

    diff_pairs: List[Tuple[str, str]] = [
        ("4x + (3u + 7x + 3u) + 4u", "4x + 3u + 7x + 3u + 4u"),
        ("7c * 5", "7 * (c * 5)"),
        ("5v + 20b + (10v + 7b)", "5v + 20b + 10v + 7b"),
        ("5s + 60 + 12s + s^2", "5s + 60 + (12s + s^2)"),
    ]
    env = MathyPolynomialSimplificationEnv()
    rnn_state = rnn_placeholder_state(128)

    for one, two in diff_pairs:
        state_one = MathyEnvState(problem=one)
        obs_one = state_one.to_observation(env.get_valid_moves(state_one), rnn_state)

        state_two = MathyEnvState(problem=two)
        obs_two = state_two.to_observation(env.get_valid_moves(state_two), rnn_state)

        assert obs_one.nodes != obs_two.nodes