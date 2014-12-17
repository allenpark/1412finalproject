from pairs import Pairs
from pairsPlayer import PairsPlayer
from randomPlayer import RandomPlayer
from twoPlayerPlayer import TwoPlayerPlayer
from nPlayerPlayer import NPlayerPlayer
from heuristicPlayer import HeuristicPlayer
from weightedHeuristicPlayer import WeightedHeuristicPlayer
from nPlayerHeuristicPlayer import NPlayerHeuristicPlayer

pairs = Pairs()
players = [NPlayerPlayer, HeuristicPlayer, HeuristicPlayer]
losses = [0]*len(players)
for x in xrange(10000):
    if (x+1) % 1000 == 0: print "Playing", (x+1)
    loser = pairs.play(players, False)
    losses[loser] += 1
print losses
