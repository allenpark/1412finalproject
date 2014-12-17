from randomPlayer import RandomPlayer
from nPlayerStrategyHeuristic import Configuration
from nPlayerStrategyHeuristic import nAction

class NPlayerHeuristicPlayer(RandomPlayer):
    def decide(self, players, deck):
        Configuration.m = len(players)
        action = nAction([p.hand for p in players], deck)
        return action == "Hit"
