import enum
import random
import copy

__all__ = [
    'MCTSAgent',
]

NUM_ROLLOUTS = 100

# tag::mcts-agent[]
class MCTSAgent():#Agent):
    # simulates NUM_ROLLOUT of rollouts for each candidate move, count the number of wins for each move, select the
    # move with the most number of wins.
    def select_move(self, game_state):
        best_value = 0
        best_move = []

        for candidate_move in game_state.legal_moves():
            # apply the candidate move
            next_state = game_state.apply_move(candidate_move)
            rollout_value = 0

            for rollout in range (0, NUM_ROLLOUTS):
                # make a copy of the next game state
                rollout_game = copy.deepcopy(next_state)
                while not rollout_game.is_over():
                    # play the game through to the end by choosing random moves. The GameState class is setup such
                    # that the next player to move automatically switches back and forth.
                    rollout_game = rollout_game.apply_move(random.choice(rollout_game.legal_moves()))

                # increment rollout value if the agent wins this rollout
                if rollout_game.winner() == game_state.get_next_player():
                    rollout_value += 1

            # compare this rollout value with the best value found so far. If better, update the best move by the
            # current candidate move. But if the value is the same as the best value so far, then add the move to
            # a list of good moves (in case there are moves that equally good or tie in value). Update the best value
            if rollout_value >= best_value:
                if rollout_value > best_value:
                    best_move = []
                    best_value = rollout_value
                best_move.append(candidate_move)

        # return a random move from the list of best move found
        return random.choice(best_move)
# end::mcts-agent[]

