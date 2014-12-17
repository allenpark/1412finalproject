def nAction(stacks, deck):
    players = []
    low = 11
    deck = [k+1 for k in xrange(10)]
    for stack in stacks:
        players.append(0)
        for c in stack:
            players[-1] += 2**(c-1)
            deck[c-1] -= 1
            if c < low:
                low = c
    return Configuration(deck, players, low).action()

class Configuration:
    udict = dict()
    c = 0
    #####!!!!!IMPORTANT TO CHANGE m and n!!!!!#####
    n = 10 #number of ranks in deck
    m = 3 #number of players
    
    def __init__(self,deck,stacks,low):
        self.deck = deck
        self.stacks = stacks
        self.low = low

    def __repr__(self):
        return '(' + str(self.deck) + ',' + ','.join(map(lambda x: bin(x)[2:].zfill(Configuration.n)[::-1],self.stacks)) + ')'

    def hit(self,j):
        newDeck = self.deck[:]
        newDeck[j-1] -= 1
        newStacks = self.stacks[1:] + [self.stacks[0] | 2**(j-1)]
        return Configuration(newDeck, newStacks, min(self.low,j))

    def ufold(self):
        p = [self.low] * Configuration.m
        p[0] += -Configuration.m*self.low
        return p

    def uhit(self):
        Configuration.c += 1
        if not Configuration.c % 10000: print Configuration.c, 'nProcessing:', self
        s = bin(self.stacks[0])[2:].zfill(Configuration.n)
        p = [0]*Configuration.m #the payoff to return
        z = float(sum(self.deck)) #normalization
        for j in xrange(1,Configuration.n+1):
            if self.deck[j-1] == 0: continue
            if s[-j] == '1':
                p[0] += -Configuration.m*j*self.deck[j-1]/z
                for i in xrange(Configuration.m): p[i] += j*self.deck[j-1]/z
            else:
                q = self.hit(j).umax()
                for i in xrange(Configuration.m): p[i] += q[i-1]*self.deck[j-1]/z
        return p

    def umax(self):
        s = str(self.deck) + ''.join(map(lambda x: str(x).zfill(Configuration.n/2),self.stacks))
        if s in Configuration.udict: return Configuration.udict[s]
        else:
            u = max(self.uhit(),self.ufold())
            Configuration.udict[s] = u
            return u

    def action(self):
        if self.umax() == self.ufold(): return 'Fold'
        else: return 'Hit'

if __name__ == "__main__":
    for (i,j,k) in [(i,j,k) for i in xrange(Configuration.n) for j in xrange(Configuration.n) for k in xrange(Configuration.n) if i < j and j < k]:
        a = [z+1 for z in xrange(Configuration.n)]
        a[i] -= 1
        a[j] -= 1
        a[k] -= 1
        #print (a,[2**i,2**j,2**k],i+1)
        Configuration(a,[2**i,2**j,2**k],i+1).umax()
    print 'Done'
