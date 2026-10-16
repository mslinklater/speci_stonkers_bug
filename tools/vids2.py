import sys; sys.path.insert(0,'.')
from demo import *
from recorder import Recorder
out=sys.argv[1]
rec=Recorder(out)
ev,g=demo(['SW']*40, rec=rec, after=50*25)
print(ev, 'video seconds at end of demo loop', rec.n/25)
g.run(50*12)
rec.close(); print('total seconds', rec.n/25)
