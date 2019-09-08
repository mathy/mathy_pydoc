from gym.envs.registration import register

from ...envs.binomial_distribution import MathyBinomialDistributionEnv
from ...types import MathyEnvDifficulty, MathyEnvProblemArgs
from ..mathy_gym_env import MathyGymEnv


class GymBinomialDistribution(MathyGymEnv):
    def __init__(self, difficulty: MathyEnvDifficulty, **kwargs):
        super(GymBinomialDistribution, self).__init__(
            env_class=MathyBinomialDistributionEnv,
            env_problem_args=MathyEnvProblemArgs(difficulty=difficulty),
            **kwargs
        )


class BinomialsEasy(GymBinomialDistribution):
    def __init__(self, **kwargs):
        super(BinomialsEasy, self).__init__(
            difficulty=MathyEnvDifficulty.easy, **kwargs
        )


class BinomialsNormal(GymBinomialDistribution):
    def __init__(self, **kwargs):
        super(BinomialsNormal, self).__init__(
            difficulty=MathyEnvDifficulty.normal, **kwargs
        )


class BinomialsHard(GymBinomialDistribution):
    def __init__(self, **kwargs):
        super(BinomialsHard, self).__init__(
            difficulty=MathyEnvDifficulty.hard, **kwargs
        )


register(id="mathy-binomial-easy-v0", entry_point="mathy.gym.envs:BinomialsEasy")
register(id="mathy-binomial-normal-v0", entry_point="mathy.gym.envs:BinomialsNormal")
register(id="mathy-binomial-hard-v0", entry_point="mathy.gym.envs:BinomialsHard")