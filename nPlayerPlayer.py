from randomPlayer import RandomPlayer
from nPlayerStrategyHeuristic import Configuration
from nPlayerStrategyHeuristic import nAction

class NPlayerPlayer(RandomPlayer):
    def decide(self, players, deck):
        Configuration.m = len(players)
        hands = [players[(i+self.pid)%len(players)].hand for i in xrange(len(players))]
        action = nAction(hands, deck)
        return action == "Hit"
