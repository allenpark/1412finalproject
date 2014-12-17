def twoAction(stack1, stack2, deck):
    player1 = 0
    player2 = 0
    low = 11
    deck = [k+1 for k in xrange(10)]
    for c in stack1:
        player1 += 2**(c-1)
        if c < low:
            low = c
        deck[c-1] -= 1
    for c in stack2:
        player2 += 2**(c-1)
        if c < low:
            low = c
        deck[c-1] -= 1
    return Configuration(deck, player1, player2, low).action()    

class Configuration:
    udict = dict()
    c = 0
    #####!!!!!IMPORTANT TO CHANGE m and n!!!!!#####
    n = 10 #number of ranks in deck
    m = 2 #number of players, should always be 2
    num_stages = 5
    def __init__(self,deck,stack1,stack2,low,recursionDepth=0):
        self.deck = deck
        self.stack1 = stack1
        self.stack2 = stack2
        self.low = low
        self.rd = recursionDepth

    def __repr__(self):
        return '(' + str(self.deck) + ',' + bin(self.stack1)[2:].zfill(Configuration.n)[::-1] + ',' + bin(self.stack2)[2:].zfill(Configuration.n)[::-1] + ')'

    def hit(self,j):
        newDeck = self.deck[:]
        newDeck[j-1] -= 1
        return Configuration(newDeck, self.stack2, self.stack1 | 2**(j-1), min(self.low,j), self.rd+1)

    def ufold(self):
        return - self.low

    def uhit(self):
        Configuration.c += 1
        if not Configuration.c % 10000: print Configuration.c, '2Processing:', self
        s = bin(self.stack1)[2:].zfill(Configuration.n)
        p = 0 #the payoff to return
        z = 0 #the limiting payoff
        h = [] #the values requiring recursion
        for j in xrange(1,Configuration.n+1):
            if s[-j] == '1':
                p += j*self.deck[j-1]
                z += 1*self.deck[j-1]
            else:
                if self.deck[j-1]: h.append(j)
                z += 2*self.deck[j-1]
        if -p <= -z*self.low: return -float("inf")
        for j in h:
            p += self.hit(j).umax()*self.deck[j-1]
        return - float(p) / sum(self.deck)

    def umax(self):
        s = str(self.deck) + str(self.stack1).zfill(Configuration.n/2) + str(self.stack2).zfill(Configuration.n/2)
        if s in Configuration.udict: return Configuration.udict[s]
        elif self.rd >= Configuration.num_stages: return self.use_heuristic()
        elif sum(self.deck) <= 5: return self.use_heuristic()
        else:
            u = max(self.uhit(),self.ufold())
            if self.rd < Configuration.num_stages - 0:
                Configuration.udict[s] = u
            return u

    def use_heuristic(self):
        '''
        limit = 31
        hand = bin(self.stack1)[2:].zfill(Configuration.n)[::-1]
        wa = sum([(i+1)*self.deck[i]*int(hand[i]) for i in xrange(len(hand))]) / sum(self.deck)
        if self.score + self.low >= limit:
            return wa
        a = sum(self.hand) / len(self.hand)
        if self.score + a >= limit:
            return self.low
        if self.score > 18 * self.low:
            return self.low
        return wa
        '''
        hand = bin(self.stack1)[2:].zfill(Configuration.n)[::-1]
        ws = sum([(i+1)*self.deck[i]*int(hand[i]) for i in xrange(len(hand))])
        wa = ws / sum(self.deck)
        return max(wa, self.ufold())

    def action(self):
        if self.umax() == self.ufold(): return 'Fold'
        else: return 'Hit'

if __name__ == "__main__":
    for (i,j) in [(i,j) for i in xrange(Configuration.n) for j in xrange(Configuration.n) if i < j]:
        a = [k+1 for k in xrange(Configuration.n)]
        a[i] -= 1
        a[j] -= 1
        #print (a,2**i,2**j,i+1)
        Configuration(a,2**i,2**j,i+1).umax()
    print 'Done'
