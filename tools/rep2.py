import sys, pickle; sys.path.insert(0,'.')
import battle2
from battle2 import *
seed=int(sys.argv[1])
gref={}
orig=LGame.__init__
def init(self,*a,**k):
    orig(self,*a,**k); gref['g']=self
LGame.__init__=init
try:
    print(battle(seed, snapfile='work/cp_%d.z80'%seed)[0])
except Crash as e:
    info=e.args[0]; print('CRASH',info)
    g=gref['g']
    acts=g.actions[info['snapidx']:]
    pickle.dump(acts,open('work/cp_%d.acts'%seed,'wb'))
    print('actions since checkpoint:',len(acts))
