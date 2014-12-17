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
    return Configuration(deck, players, 10, len(stacks), low).action()

class Configuration:
    udict = dict()
    c = 0
    
    def __init__(self,deck,stacks,n,m,low,check=False,recursionDepth=0):
        self.deck = deck
        self.stacks = stacks
        self.n = n
        self.m = m
        self.low = low
        if check: assert self.isvalid()
        self.rd = recursionDepth

    def __repr__(self):
        return '(' + str(self.deck) + ',' + ','.join(map(lambda x: bin(x)[2:].zfill(self.n)[::-1],self.stacks)) + ')'

    def hit(self,j):
        newDeck = self.deck[:]
        newDeck[j-1] -= 1
        newStacks = self.stacks[1:] + [self.stacks[0] | 2**(j-1)]
        return Configuration(newDeck, newStacks, self.n, self.m, min(self.low,j), recursionDepth=self.rd+1)

    def ufold(self):
        p = [self.low] * self.m
        p[0] += -self.m*self.low
        return p

    def uhit(self):
        Configuration.c += 1
        if not Configuration.c % 10000: print Configuration.c, 'Processing:', self
        s = bin(self.stacks[0])[2:].zfill(self.n)
        p = [0]*self.m #the payoff to return
        z = float(sum(self.deck)) #normalization
        for j in xrange(1,self.n+1):
            if self.deck[j-1] == 0: continue
            if s[-j] == '1':
                p[0] += -self.m*j*self.deck[j-1]/z
                for i in xrange(self.m): p[i] += j*self.deck[j-1]/z
            else:
                q = self.hit(j).umax()
                for i in xrange(self.m): p[i] += q[i-1]*self.deck[j-1]/z
        return p

    def umax(self):
        s = str(self.deck) + ':'.join(map(str,self.stacks))
        if s in Configuration.udict: return Configuration.udict[s]
        elif self.rd > 3:
            return self.ufold()
        else:
            u = max(self.uhit(),self.ufold())
            if self.rd < 2:
                Configuration.udict[s] = u
            #assert self.action(True) == self.action(False)
            return u

    def action(self, heur=True):
        if heur:
            s = map(lambda x: bin(x)[2:].zfill(self.n), self.stacks)
            q = map(lambda x: 1-sum([self.deck[j-1] for j in xrange(1,self.n+1) if x[-j]=='1'])/float(sum(self.deck)), s[1:])
            p = 1
            for px in q: p = p*px
            if sum([j*self.deck[j-1] for j in xrange(1,self.n+1) if s[0][-j] == '1']) < (1-p)*sum(self.deck)*self.low: return 'Hit'
        if self.umax() == self.ufold(): return 'Fold'
        else: return 'Hit'

    def isvalid(self):
        return len(self.deck) == self.n and \
               len(self.stacks) == self.m and \
               not any(map(lambda x: x % 2**(self.low-1),self.stacks)) and \
               any(map(lambda x: x % 2**self.low,self.stacks))


n = 10
m = 3
for (i,j,k) in [(i,j,k) for i in xrange(n) for j in xrange(n) for k in xrange(n) if i < j and j < k]:
    break
    a = [z+1 for z in xrange(n)]
    a[i] -= 1
    a[j] -= 1
    a[k] -= 1
    Configuration(a,[2**i,2**j,2**k],10,3,i+1).umax()
print 'Done'

if True:
    x = Configuration([1,2,3,4,5],[28,4],5,2,3)
