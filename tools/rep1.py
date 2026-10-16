import sys,json; sys.path.insert(0,'.')
import battle
battle.SNAP=True
seed=int(sys.argv[1])
try: print(battle.battle(seed))
except battle.Crash as e: print('CRASH',e.args[0])
print('snapshot t', open('work/snap_%d.t'%seed).read())
