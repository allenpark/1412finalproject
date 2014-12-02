import random
from sweepPlayer import SweepPlayer

class RandomPlayer(SweepPlayer):
    def decide(self, center, players, played, round_num):
        return random.choice(self.hand)
