udict = dict()

c = 0
class Configuration:
    def __init__(self,deck,stack1,stack2,low):
        self.deck = deck
        self.stack1 = stack1
        self.stack2 = stack2
        self.low = low

    def __repr__(self):
        return '(' + str(self.deck) + ',' + bin(self.stack1)[2:].zfill(n)[::-1] + ',' + bin(self.stack2)[2:].zfill(n)[::-1] + ')'

    def hit(self,j):
        newDeck = self.deck[:]
        newDeck[j-1] -= 1
        return Configuration(newDeck, self.stack2, self.stack1 | 2**(j-1), min(self.low,j))

    def ufold(self):
        return - self.low

    def uhit(self):
        global c
        c += 1
        if not c % 10000: print c, 'Processing:', self
        s = bin(self.stack1)[2:].zfill(n)
        p = 0 #the payoff to return
        z = 0 #the limiting payoff
        h = [] #the values requiring recursion
        for j in xrange(1,n+1):
            if s[-j] == '1':
                p += j*self.deck[j-1]
                z += 1*self.deck[j-1]
            else:
                if self.deck[j-1]: h.append(j)
                z += 2*self.deck[j-1]
        if -p <= -z*self.low: return -1000
        for j in h:
            p += self.hit(j).umax()*self.deck[j-1]
        return - float(p) / sum(self.deck)

    def umax(self):
        s = str(self.deck) + str(self.stack1).zfill(n/2) + str(self.stack2).zfill(n/2)
        if s in udict: return udict[s]
        else:
            u = max(self.uhit(),self.ufold())
            udict[s] = u
            return u

    def action(self):
        if self.umax() == self.ufold(): return 'Fold'
        else: return 'Hit'

#####!!!!!IMPORTANT TO CHANGE m and n!!!!!#####
n = 10 #number of ranks in deck
m = 2 #number of players, should always be 2
for (i,j) in [(i,j) for i in xrange(n) for j in xrange(n) if i < j]:
    a = [k+1 for k in xrange(n)]
    a[i] -= 1
    a[j] -= 1
    #print (a,2**i,2**j,i+1)
    Configuration(a,2**i,2**j,i+1).umax()
print 'Done'

if False:
    n = 5
    m = 2
    x = Configuration([1,2,3,4,5],28,4,3)
