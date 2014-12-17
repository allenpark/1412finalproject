import random

class Pairs:
    def __init__(self, debug=True):
        self.debug = debug

    def dbg(self, msg):
        if self.debug:
            print msg

    def init_game(self, clses):
        # initialising the deck
        self.deck = []
        self.deckCount = []
        for i in xrange(1, 11):
            self.deck += [i]*i
            self.deckCount.append(i)
        random.shuffle(self.deck)
        self.discards = []
        # initialising players
        self.players = []
        for i in xrange(len(clses)):
            self.players.append(clses[i](i))
        return self.init_round()

    def init_round(self):
        self.dbg("")
        # discarding all cards in play
        for i in xrange(len(self.players)):
            p = self.players[i]
            self.discards += p.hand
            self.players[i].hand = []
            self.dbg("Player " + str(i) + " score: " + str(p.score) + " and scored: " + str(p.scored))
        self.dbg("")
        # dealing initial hand
        lowest = []
        lowest_card = 11
        for i in xrange(len(self.players)):
            hand = self.pop_from_deck(1)
            self.players[i].insert_into_hand(hand)
            if hand[0] < lowest_card:
                lowest = [i]
                lowest_card = hand[0]
            elif hand[0] == lowest_card:
                lowest.append(i)
            self.dbg("Player " + str(i) + " is dealt " + str(hand[0]))
        # determining first player
        self.dbg("Lowest is players " + str(lowest) + " with card " + str(lowest_card))
        while len(lowest) > 1:
            lowest_again = []
            lowest_card_again = 11
            for i in lowest:
                another = self.pop_from_deck(1)
                self.dbg("Player " + str(i) + " is dealt " + str(another[0]))
                inLoopAlready = False
                while another[0] in self.players[i].hand:
                    inLoopAlready = True
                    self.dbg("This is a duplicate! Discarded.")
                    self.discards.append(another[0]);
                    another = self.pop_from_deck(1)
                    self.dbg("Player " + str(i) + " is dealt " + str(another[0]))
                self.players[i].insert_into_hand(another)
                if another[0] < lowest_card_again:
                    lowest_again = [i]
                    lowest_card_again = another[0]
                elif another[0] == lowest_card_again:
                    lowest_again.append(i)
            lowest = lowest_again
            self.dbg("Lowest is players " + str(lowest) + " with card " + str(lowest_card_again))
        self.dbg("Player " + str(lowest[0]) + " goes first.")
        return lowest[0]

    def pop_from_deck(self, n):
        r = []
        for i in xrange(n):
            while len(self.deck) <= 5:
                if len(self.discards) == 0:
                    print "ERROR: discards is empty while reshuffling"
                self.dbg("Reshuffling!")
                self.deck += self.discards
                self.discards = []
                random.shuffle(self.deck)
                self.deckCount = [0]*10
                for c in self.deck:
                    self.deckCount[c-1] += 1
            r.append(self.deck.pop())
            self.deckCount[r[-1]-1] -= 1
        return r
    
    def play(self, clses, dbg=True):
        self.debug = dbg
        pid = self.init_game(clses)
        limit = (60 / len(clses)) + 1
        while True:
            p = self.players[pid]
            mv = p.decide(self.players, self.deckCount)
            self.dbg("")
            if mv:
                # hit
                deal = self.pop_from_deck(1)[0]
                if deal in p.hand:
                    # you got a pair
                    p.score += deal
                    p.scored.append(deal)
                    self.dbg("Player " + str(pid) + " has hit for " + str(deal) + " and got a pair!")
                    if p.score >= limit:
                        break
                    pid = self.init_round()
                    continue
                else:
                    p.insert_into_hand([deal])
                    self.dbg("Player " + str(pid) + " has hit for " + str(deal) + " and now has " + str(p.hand))
            else:
                # fold
                all_cards = [y for x in self.players for y in x.hand]
                lowest = min(all_cards)
                steal_from = p.handle_fold(lowest, self.players)
                if lowest in self.players[steal_from].hand:
                    self.players[steal_from].hand.remove(lowest)
                    p.score += lowest
                    p.scored.append(lowest)
                    self.dbg("Player " + str(pid) + " has folded and taken a " + str(lowest) + " from player " + str(steal_from) + "'s hand")
                    if p.score >= limit:
                        break
                    pid = self.init_round()
                    continue
                else:
                    print "------------------------------------------------------------------"
                    print "ERROR: Lowest " + str(lowest) + " not in player " + str(steal_from) + "'s hand " + str(self.players[steal_from].hand)
                    print "------------------------------------------------------------------"

            pid = (pid + 1) % len(self.players)
        self.dbg("")
        self.dbg("Player " + str(pid) + " has lost!")
        self.dbg("")
        self.dbg("Final scores:")
        for i in xrange(len(self.players)):
            p = self.players[i]
            self.dbg("Player " + str(i) + " score: " + str(p.score) + " and scored: " + str(p.scored))
        return pid
