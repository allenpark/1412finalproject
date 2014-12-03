class PairsPlayer:
    def __init__(self, pid, hand):
        self.type = "Default Player"
        self.pid = pid
        self.hand = sorted(hand)
        self.history = []

    def move(self, center, players, played, round_num):
        decision = self.decide(center, players, played, round_num)
        while decision not in self.hand:
            print "Don't be a dumbass"
            decision = self.decide(center, players, played, round_num)
        self.hand.remove(decision)
        self.history.append(decision)
        return decision

    def insert_into_hand(self, new_cards):
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

    def decide(self, center, players, played, round_num):
        # OVERRIDE THIS IF YOU DEFINE A NEW PLAYER
        print "Player " + str(self.pid) + "'s hand is " + str(self.hand)
        return int(raw_input("What card will player " + str(self.pid) + " play? "))
