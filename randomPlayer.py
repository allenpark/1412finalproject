import random
from pairsPlayer import PairsPlayer

class RandomPlayer(PairsPlayer):
    def decide(self, center, players, played, round_num):
        return random.choice(self.hand)
