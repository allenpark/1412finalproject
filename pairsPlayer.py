class PairsPlayer:
    def __init__(self, pid):
        self.type = "Default Player"
        self.pid = pid
        self.hand = []
        self.score = 0
        self.scored = []

    def move(self, players):
        decision = self.decide(players)
        return decision

    def insert_into_hand(self, cards):
        new_cards = [x for x in cards]
        new_hand = []
        while len(self.hand) > 0 or len(new_cards) > 0:
            if len(self.hand) == 0:
                new_hand += new_cards
                break
            if len(new_cards) == 0:
                new_hand += self.hand
                break
            if self.hand[0] <= new_cards[0]:
                new_hand.append(self.hand.pop(0))
            else:
                new_hand.append(new_cards.pop(0))
        self.hand = new_hand

    # Returns the pid of the player you want to steal from
    # The player must have lowest in their hand
    def handle_fold(self, lowest, players):
        # OVERRIDE THIS IF YOU DEFINE A NEW PLAYER
        print
        for pid in xrange(len(players)):
            print "Player " + str(pid) + " has hand " + str(players[pid].hand)
        print "You are player " + str(self.pid) + " taking a " + str(lowest)
        x = int(raw_input("Which player will you take from? "))
        while lowest not in players[x].hand:
            print "Player " + str(x) + " does not have " + str(lowest)
            x = int(raw_input("Which player will you take from? "))
        return x

    # Returns true if hit and false if fold
    def decide(self, players):
        # OVERRIDE THIS IF YOU DEFINE A NEW PLAYER
        print
        print "Player " + str(self.pid) + "'s hand is " + str(self.hand)
        ans = raw_input("Will you hit or fold? (h/f) ")
        while len(ans) == 0:
            print "That's not an answer."
            ans = raw_input("Will you hit or fold? (h/f) ")
        return ans[0] == 'h'
