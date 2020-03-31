import enum
import random

#from dlgo.agent import Agent

__all__ = [
    'RandomAgent',
]

# tag::random-agent[]
class RandomAgent():#Agent):
    def select_move(self, game_state):
        return random.choice(game_state.legal_moves())
# end::random-agent[]

