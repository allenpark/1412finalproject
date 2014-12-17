from randomPlayer import RandomPlayer

class HeuristicPlayer(RandomPlayer):
    def decide(self, players, deck):
        limit = (60 / len(players)) + 1
        all_cards = [y for x in players for y in x.hand]
        lowest = min(all_cards)
        if self.score + lowest >= limit:
            return True
        a = sum(self.hand) / len(self.hand)
        if self.score + a >= limit:
            return False
        if self.score > 18 * lowest:
            return False
        return True
