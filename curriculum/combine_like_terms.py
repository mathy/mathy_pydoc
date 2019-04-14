from mathzero.training.problems import (
    MODE_SIMPLIFY_POLYNOMIAL,
    combine_multiple_like_add_terms,
    rand_int,
    rand_var,
)
from mathzero.training.lessons import build_lesson_plan, LessonExercise
import random


def two_variable_terms():
    variable = rand_var()
    problem = "{}{} + {}{}".format(rand_int(), variable, rand_int(), variable)
    return problem, 2


def two_variable_terms_separated_by_constant():
    variable = rand_var()
    problem = "{}{} + {} + {}{}".format(
        rand_int(), variable, const, rand_int(), variable
    )
    return problem, 3


def three_variable_terms():
    return combine_multiple_like_add_terms(3)


def four_variable_terms():
    return combine_multiple_like_add_terms(4)


def five_variable_terms():
    return combine_multiple_like_add_terms(5)


def six_variable_terms():
    return combine_multiple_like_add_terms(6)


lessons = build_lesson_plan(
    "Combine Like Terms",
    [
        # LessonExercise(
        #     lesson_name="Two terms",
        #     problem_count=200,
        #     problem_fn=two_variable_terms,
        #     problem_type=MODE_SIMPLIFY_POLYNOMIAL,
        #     max_turns=7,
            # num_exploration_moves=20,
        #     mcts_sims=250,
        # ),
        # LessonExercise(
        #     lesson_name="Three variable terms",
        #     problem_count=100,
        #     problem_fn=three_variable_terms,
        #     problem_type=MODE_SIMPLIFY_POLYNOMIAL,
        #     max_turns=15,
            # num_exploration_moves=20,
        #     mcts_sims=300,
        # ),
        LessonExercise(
            lesson_name="Four variable terms",
            problem_count=24,
            problem_fn=four_variable_terms,
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            max_turns=25,
            num_exploration_moves=10,
            mcts_sims=250,
        ),
        LessonExercise(
            lesson_name="Five variable terms",
            problem_count=8,
            problem_fn=five_variable_terms,
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            num_exploration_moves=12,
            max_turns=25,
            mcts_sims=250,
        ),
        LessonExercise(
            lesson_name="Six variable terms",
            problem_count=4,
            problem_fn=six_variable_terms,
            problem_type=MODE_SIMPLIFY_POLYNOMIAL,
            max_turns=25,
            num_exploration_moves=12,
            mcts_sims=250,
        ),
    ],
)