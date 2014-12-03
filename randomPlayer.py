import random
from pairsPlayer import PairsPlayer

class RandomPlayer(PairsPlayer):
    def decide(self, players):
        return random.random() < 0.5

    def handle_fold(self, lowest, players):
        eligible = [i for i in xrange(len(players)) if lowest in players[i].hand]
        return random.choice(eligible)
