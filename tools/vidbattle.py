import sys; sys.path.insert(0,'.')
import battle2
from battle2 import *
from recorder import Recorder
seed=int(sys.argv[1]); out=sys.argv[2]
gref={}
orig=LGame.__init__
def init(self,*a,**k):
    orig(self,*a,**k); gref['g']=self; self.rec=Recorder(out)
LGame.__init__=init
try:
    r=battle(seed)[0]; print(r)
    g=gref['g']; g.checking=False; g.run(50*8)
except Crash as e:
    print('CRASH',e.args[0])
    g=gref['g']; g.checking=False
    print('crash at video frame', g.rec.n, 'seconds', g.rec.n/25)
    g.run(50*15)
g.rec.close(); print('frames',g.rec.n)
