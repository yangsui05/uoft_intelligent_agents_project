import enum
import random

#from dlgo.agent import Agent

__all__ = [
    'MinimaxAgent',
]

TARGET_MOVES = 2

# tag::gameresult-enum[]
class GameResult(enum.Enum):
    loss = 1
    draw = 2
    win = 3
# end::gameresult-enum[]


def reverse_game_result(game_result):
    if game_result == GameResult.loss:
        return game_result.win
    if game_result == GameResult.win:
        return game_result.loss
    return GameResult.draw


# tag::minimax-signature[]
def best_result(game_state):
# end::minimax-signature[]
# tag::minimax-base-case[]
    if game_state.is_over():
        # Game is already over.
        if game_state.winner() == game_state.next_player:
            # We win!
            return GameResult.win
        elif game_state.winner() is None:
            # A draw.
            return GameResult.draw
        else:
            # Opponent won.
            return GameResult.loss
# end::minimax-base-case[]

# tag::minimax-recursive-case[]
    best_result_so_far = GameResult.loss

    # only play up to TARGET_MOVES moves through to the end (to prune/reduce search space)
    num_legal_moves = len(game_state.legal_moves())

    for candidate_move in game_state.legal_moves():
        if random.random() < TARGET_MOVES/num_legal_moves:
            next_state = game_state.apply_move(candidate_move)     # <1>
            opponent_best_result = best_result(next_state)         # <2>
            our_result = reverse_game_result(opponent_best_result) # <3>
            if our_result.value > best_result_so_far.value:        # <4>
                best_result_so_far = our_result
    return best_result_so_far
# end::minimax-recursive-case[]
        # See what the board would look like if we play this move.
        # Find out our opponent's best move.
        # Whatever our opponent wants, we want the opposite.
        # See if this result is better than the best we've seen so far.


# tag::minimax-agent[]
class MinimaxAgent():#Agent):
    def select_move(self, game_state):
        winning_moves = []
        draw_moves = []
        losing_moves = []

        num_legal_moves = len(game_state.legal_moves())

        # Loop over all legal moves.
        for possible_move in game_state.legal_moves():
            # only pick a few legal moves to play through to the end (prune/reduce search space)
            # The target number of moves to play through is set in TARGET_MOVES.
            # each legal move has a probability of being played through. The probabiliy is calculated based on the
            # total number of legal moves. E.g. if there are 6 total legal moves, each move has a 3/6=0.5 chance of
            # being chosen to play through. If there are 3 or less legal moves, the agent will play through all of them
            if random.random() < TARGET_MOVES/num_legal_moves:
                # Calculate the game state if we select this move.
                next_state = game_state.apply_move(possible_move)
                # Since our opponent plays next, figure out their best
                # possible outcome from there.
                opponent_best_outcome = best_result(next_state)
                # Our outcome is the opposite of our opponent's outcome.
                our_best_outcome = reverse_game_result(opponent_best_outcome)
                # Add this move to the appropriate list.
                if our_best_outcome == GameResult.win:
                    winning_moves.append(possible_move)
                elif our_best_outcome == GameResult.draw:
                    draw_moves.append(possible_move)
                else:
                    losing_moves.append(possible_move)

        if winning_moves:
            return random.choice(winning_moves)
        if draw_moves:
            return random.choice(draw_moves)
        if losing_moves:
            return random.choice(losing_moves)
        return random.choice(game_state.legal_moves())
# end::minimax-agent[]
