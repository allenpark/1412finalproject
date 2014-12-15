udict = dict()

c = 0
class Configuration:
    def __init__(self,deck,stacks,low):
        self.deck = deck
        self.stacks = stacks
        self.low = low

    def __repr__(self):
        return '(' + str(self.deck) + ',' + ','.join(map(lambda x: bin(x)[2:].zfill(n)[::-1],self.stacks)) + ')'

    def hit(self,j):
        newDeck = self.deck[:]
        newDeck[j-1] -= 1
        newStacks = self.stacks[1:] + [self.stacks[0] | 2**(j-1)]
        return Configuration(newDeck, newStacks, min(self.low,j))

    def ufold(self):
        p = [self.low] * m
        p[0] += -m*self.low
        return p

    def uhit(self):
        global c
        c += 1
        if not c % 10000: print c, 'Processing:', self
        s = bin(self.stacks[0])[2:].zfill(n)
        p = [0]*m #the payoff to return
        z = float(sum(self.deck)) #normalization
        for j in xrange(1,n+1):
            if self.deck[j-1] == 0: continue
            if s[-j] == '1':
                p[0] += -m*j*self.deck[j-1]/z
                for i in xrange(m): p[i] += j*self.deck[j-1]/z
            else:
                q = self.hit(j).umax()
                for i in xrange(m): p[i] += q[i-1]*self.deck[j-1]/z
        return p

    def umax(self):
        s = str(self.deck) + ''.join(map(lambda x: str(x).zfill(n/2),self.stacks))
        if s in udict: return udict[s]
        else:
            u = max(self.uhit(),self.ufold())
            udict[s] = u
            return u

    def action(self):
        if self.umax() == self.ufold(): return 'Fold'
        else: return 'Hit'

#####!!!!!IMPORTANT TO CHANGE m and n!!!!!#####
n = 8 #number of ranks in deck
m = 3 #number of players
for (i,j,k) in [(i,j,k) for i in xrange(n) for j in xrange(n) for k in xrange(n) if i < j and j < k]:
    break
    a = [z+1 for z in xrange(n)]
    a[i] -= 1
    a[j] -= 1
    a[k] -= 1
    #print (a,[2**i,2**j,2**k],i+1)
    Configuration(a,[2**i,2**j,2**k],i+1).umax()
print 'Done'

if False:
    n = 5
    m = 2
    x = Configuration([1,2,3,4,5],[28,4],3)
