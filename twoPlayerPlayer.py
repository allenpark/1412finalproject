from randomPlayer import RandomPlayer
from twoPlayerStrategy import twoAction

class TwoPlayerPlayer(RandomPlayer):
    def decide(self, players, deck):
        if len(players) != 2:
            print "NUMBER OF PLAYERS FOR TWO PLAYER PLAYER IS NOT 2"
            return
        action = twoAction(players[self.pid].hand, players[1 - self.pid].hand, deck)
        return action == "Hit"
