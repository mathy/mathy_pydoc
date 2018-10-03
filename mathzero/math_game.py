import random
import math
import numpy
import time
from alpha_zero_general.Game import Game
from .core.expressions import (
    MathExpression,
    ConstantExpression,
    MultiplyExpression,
    PowerExpression,
    STOP,
    AddExpression,
    VariableExpression,
)
from .core.problems import ProblemGenerator
from .core.parser import ExpressionParser
from .core.util import (
    termsAreLike,
    isAddSubtract,
    getTerms,
    getTerm,
    isPreferredTermForm,
    has_like_terms,
)
from .core.rules import (
    BaseRule,
    AssociativeSwapRule,
    CommutativeSwapRule,
    DistributiveFactorOutRule,
    DistributiveMultiplyRule,
    ConstantsSimplifyRule,
    VariableMultiplyRule,
)
from .core.profiler import profile_start, profile_end
from .environment_state import EnvironmentState
from multiprocessing import cpu_count


class MathGame(Game):
    """
    Implement a math solving game where players win by executing the right sequence 
    of actions to reduce a math expression to its most basic representation before the 
    other player.
    """

    width = 128
    verbose = False
    draw = 0.0001
    max_moves = 25

    def __init__(self):
        self.parser = ExpressionParser()
        self.problems = ProblemGenerator()
        self.available_rules = [
            ConstantsSimplifyRule(),
            DistributiveFactorOutRule(),
            DistributiveMultiplyRule(),
            CommutativeSwapRule(),
            AssociativeSwapRule(),
            VariableMultiplyRule(),
        ]
        self.expression_str = "unset"

    def get_initial_state(self, problem: str = None):
        """return a numpy encoded version of the input expression"""
        if problem is None:
            problem = self.problems.simplify_multiple_terms(max_terms=4)
            # problem = self.problems.most_basic_add_like_terms()
            # problem = self.problems.variable_multiplication(3)
        # TODO: Remove this stateful variable that is used mostly for printing out "{from} -> {to}" at game end
        # NOTE: If we store a plane for history per user we could do something like [first_state, last_n-2, last_n-1, last_n, current]
        # problem = "(((10z + 8) + 11z * 4) + 1z) + 9z"
        self.expression_str = problem
        # self.expression_str = "4x * 8 * 2"
        if MathGame.verbose:
            print("\n\n\t\tNEXT: {}".format(problem))
        if len(list(problem)) > MathGame.width:
            raise ValueError(
                'Expression "{}" is too long for the current model to process. Max width is: {}'.format(
                    problem, MathGame.width
                )
            )
        env_state = EnvironmentState(MathGame.width).encode_board(problem)

        # NOTE: This is called for each episode, so it can be thought of like "onInitEpisode()"
        return env_state

    def write_draw(self, state):
        """Help spot errors in win conditons by always writing out draw values for review"""
        with open("draws.txt", "a") as file:
            file.write("{}\n".format(state))
        if MathGame.verbose:
            print(state)

    def get_agent_actions_count(self):
        """Return number of all possible actions"""
        return len(self.available_rules) * self.width

    def get_next_state(self, env_state, player, action, searching=False):
        """
        Input:
            env_state:     current env_state
            player:    current player (1 or -1)
            action:    action taken by current player
            searching: boolean set to True when called by MCTS

        Returns:
            next_state: env_state after applying action
            next_player: player who plays in the next turn (should be -player)
        """
        b = EnvironmentState(MathGame.width)
        features, move_count, _ = b.decode_player(env_state, player)
        expression = self.parser.parse_features(features)

        # Figure out the token index of the selected action
        token_index = action % self.width
        # And the action at that token
        action_index = int(action / (self.width - token_index))
        token = self.getFocusToken(expression, token_index)
        operation = self.available_rules[action_index]

        # If you get maximum recursion errors, it can mean that you're not
        # hitting a terminal state. Force the searching var off here to get
        # more verbose logging if your crash is occurring before the first verbose
        # output.
        # searching = False

        # Enforce constraints to keep training time and complexity down?
        # - can't commutative swap immediately to return to previous state.
        # NOTE: leaving these ideas here, but optimization made them less necessary
        # NOTE: Also adding constraints caused actions to be avoided and others to be
        #       repeated in odd ways. Assume repetition is part of training.
        # NOTE: Maybe this is solved by something like Actor/Critic updates?
        if isinstance(operation, BaseRule) and operation.canApplyTo(token):
            change = operation.applyTo(token.rootClone())
            root = change.end.getRoot()
            out_features = self.parser.make_features(str(root))
            if not searching and MathGame.verbose and player == 1:
                print("[{}] {}".format(move_count, change.describe()))
            out_board = b.encode_player(env_state, player, out_features, move_count + 1)
        else:
            print(
                "action is {}, token_index is {}, and token is {}".format(
                    action, token_index, str(token)
                )
            )
            raise Exception(
                "\n\nPlayer: {}\n\tExpression: {}\n\tFocus: {}\n\tIndex: {}\n\tinvalid move selected: {}, {}".format(
                    player, expression, token, token_index, action, type(operation)
                )
            )

        return out_board, player * -1

    def getFocusToken(
        self, expression: MathExpression, focus_index: int
    ) -> MathExpression:
        """Get the token that is `focus_index` from the left of the expression"""
        count = 0
        result = None

        def visit_fn(node, depth, data):
            nonlocal result, count
            result = node
            if count == focus_index:
                return STOP
            count = count + 1

        expression.visitPreorder(visit_fn)
        return result

    def getValidMoves(self, env_state, player):
        """
        Input:
            env_state: current env_state
            player: current player

        Returns:
            validMoves: a binary vector of length self.get_agent_actions_count(), 1 for
                        moves that are valid from the current env_state and player,
                        0 for invalid moves
        """
        b = EnvironmentState(MathGame.width)
        features, _, _ = b.decode_player(env_state, player)
        expression = self.parser.parse_features(features)

        actions = self.get_actions_for_expression(expression)
        # NOTE: Below is verbose output showing which actions are valid.
        # if not searching:
        #     print_list = self.available_actions + self.available_rules
        #     [
        #         print(
        #             "Player{} action[{}][{}] = {}".format(
        #                 player, i, bool(a), type(print_list[i]) if a != 0 else ""
        #             )
        #         )
        #         for i, a in enumerate(actions)
        #     ]
        return actions

    def get_actions_for_expression(self, expression: MathExpression):
        actions = [0] * self.get_agent_actions_count()

        # Properties of numbers and common simplifications
        for rule_index, rule in enumerate(self.available_rules):
            nodes = rule.findNodes(expression)
            for node in nodes:
                token_index = node.r_index
                action_index = (self.width * rule_index) + token_index
                actions[action_index] = 1

                # print(
                #     "[action_index={}={}] can apply to [token_index={}, {}]".format(
                #         action_index, rule.name, node.r_index, str(node)
                #     )
                # )

        return actions

    def getGameEnded(self, env_state, player, searching=False):
        """
        Input:
            env_state:     current env_state
            player:    current player (1 or -1)
            searching: boolean that is True when called by MCTS simulation

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.
               
        """
        b = EnvironmentState(MathGame.width)
        features, move_count, _ = b.decode_player(env_state, player)
        expression = self.parser.parse_features(features)

        # Check for simplification removes all like terms
        root = expression.getRoot()

        if not has_like_terms(root):
            term_nodes = getTerms(root)
            is_win = True
            for term in term_nodes:
                if not isPreferredTermForm(term):
                    is_win = False
            if is_win:
                if not searching and MathGame.verbose:
                    print(
                        "\n[Player{}][NOLIKEWIN] {} => {}!".format(
                            player, self.expression_str, expression
                        )
                    )
                return 1

        # Check the turn count last because if the previous move that incremented
        # the turn over the count resulted in a win-condition, we want it to be honored.
        if move_count > MathGame.max_moves:
            f2, move_count_other, _ = b.decode_player(env_state, player * -1)
            if searching or move_count_other > MathGame.max_moves:
                if not searching:
                    e2 = self.parser.parse_features(f2)
                    draw_time = int(round(time.time() * 1000))
                    self.write_draw(
                        "[time={}][DRAW] ENDED WITH:\n\t input: {}\n\t 1: {}\n\t 2: {}\n".format(
                            draw_time, self.expression_str, expression, e2
                        )
                    )
                return MathGame.draw

        # The game continues
        return 0

    def getCanonicalForm(self, env_state, player):
        """
        Input:
            env_state: current env_state
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of env_state. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            env_state as is. When the player is black, we can invert
                            the colors and return the env_state.
        """
        # print("gcf: {}".format(player))
        return EnvironmentState(MathGame.width).get_canonical_board(env_state, player)

    def get_agent_state_size(self):
        """return shape (x,y) of agent state dimensions"""
        # 2 columns per player, the first for turn data, the second for text inputs
        return (4, MathGame.width)

    def getSymmetries(self, env_state, pi):
        """
        Input:
            env_state: current env_state
            pi: policy vector of size self.get_agent_actions_count()

        Returns:
            symmForms: a list of [(env_state,pi)] where each tuple is a symmetrical
                       form of the env_state and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        return [(env_state, pi)]

    def to_hash_key(self, env_state):
        """conversion of env_state to a string format, required by MCTS for hashing."""
        b = EnvironmentState(MathGame.width)
        # This is always called for the canonical env_state which means the
        # current player is always in player1 slot:
        features, move_count, _ = b.decode_player(env_state, 1)
        features_key = ",".join([str(f) for f in features])
        return "[{}, {}]".format(move_count, features_key)


_parser = None


def display(env_state, player):
    global _parser
    if _parser is None:
        _parser = ExpressionParser()
    b = EnvironmentState(MathGame.width)
    features = b.decode_player(env_state, player)[0]
    expression = _parser.parse_features(features)
    expression_len = len(str(expression))
    width = 100
    if player == 1:
        buffer = " " * int(width / 2 - expression_len)
    elif player == -1:
        buffer = " " * int(width - expression_len)
    else:
        raise ValueError("invalid player index: {}".format(player))
    print("{}{}".format(buffer, expression))
