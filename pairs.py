import random

class Sweep:
    def __init__(self, dbg=True):
        self.debug = dbg

    def debug(self, msg):
        if self.debug:
            print msg

    def init_game(self, clses):
        self.deck = []
        for i in xrange(1, 11):
            self.deck += [i]*i
        random.shuffle(self.deck)
        self.players = []
        for i in xrange(len(clses)):
            cls = clses[i]
            hand = self.pop_from_deck(5)
            self.players.append(cls(i, hand))
        return True

    def pop_from_deck(self, n):
        if n >= len(self.deck):
            x = self.deck
            self.deck = []
            return x
        r = []
        for i in xrange(n):
            r.append(self.deck.pop())
        return r

    def take_highest_from_center(self):
        h = self.center[-1]
        r = []
        while len(self.center) > 0 and self.center[-1] == h:
            r.append(self.center.pop())
        return r

    def take_lower_from_center(self, card):
        r = []
        while len(self.center) > 0 and self.center[0] < card:
            r.append(self.center.pop(0))
        return r

    def insert_into_center(self, card):
        for i in xrange(len(self.center)):
            if self.center[i] >= card:
                self.center.insert(i, card)
                return
        self.center.append(card)
    
    def play(self, clses, dbg=True):
        self.debug = dbg
        if not self.init_game(clses):
            return
        round_num = 0
        last_capture = 0
        while len(self.deck) > 0:
            self.center = sorted(self.pop_from_deck(5))
            # playing phase
            played = []
            print
            print "PLAYING:"
            print "Center is " + str(self.center)
            for i in xrange(len(self.players)):
                pid = (i + last_capture) % len(self.players)
                mv = self.players[pid].move(self.center, self.players, played, round_num)
                print "Player " + str(pid) + " played " + str(mv)
                played.append([pid, mv])
            # capturing phase
            # TODO: detect and implement ties
            print
            print "CAPTURING:"
            played = sorted(played, key=lambda x: x[1])
            first_pid = played[0][0]
            highest = self.take_highest_from_center()
            print "Player " + str(first_pid) + " played " + str(played[0][1]) + " and took " + str(highest)
            self.players[first_pid].insert_into_hand(highest)
            self.insert_into_center(played[0][1])
            for i in xrange(1, len(played)):
                pid = played[i][0]
                lower = self.take_lower_from_center(played[i][1])
                print "Player " + str(pid) + " played " + str(played[i][1]) + " and took " + str(lower)
                self.players[pid].insert_into_hand(lower)
                self.insert_into_center(played[i][1])
            last_capture = played[-1][0]
            round_num += 1
        # scoring phase
        scores = [0] * len(self.players)
        for card in xrange(1, 11):
            most_cards = 1
            most_players = []
            for i in xrange(len(self.players)):
                hand = self.players[i].hand
                num_cards = 0
                for j in xrange(len(hand)):
                    if hand[j] == card:
                        num_cards += 1
                if num_cards == most_cards:
                    most_players.append(i)
                elif num_cards > most_cards:
                    most_cards = num_cards
                    most_players = [i]
            for i in xrange(len(most_players)):
                scores[most_players[i]] += card
        print
        print "SCORING:"
        for i in xrange(len(self.players)):
            print "Player " + str(i) + " has score " + str(scores[i]) + " and hand " + str(self.players[i].hand)
