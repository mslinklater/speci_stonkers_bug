import sys, json; sys.path.insert(0,'.')
from endings import *
def run2(kind, video=None):
    g=base()
    if video: g.rec=Recorder(video)
    g.run(100); setup(kind,g)
    events=[]; state='play'; tend=None
    for f in range(0,50*120,5):
        g.emap=set(); g.run(5)
        sus=suspicious(g.emap); sp=g.reg[SP]; pc=g.reg[PC]
        if state=='play' and 0xC518 in g.emap: events.append(('end-sequence',f)); state='ending'; tend=f
        if state=='ending' and f-tend==50*12:
            g.screenshot('work/endscr_%s.png'%kind)
            g.tap('SP',5,20); events.append(('key',f))
        if 0xC1AD in g.emap and state=='ending': events.append(('restart',f)); state='restarted'
        if state=='restarted' and 0xC2EC in g.emap and ('next-battle-running' not in [e[0] for e in events]):
            events.append(('next-battle-running',f))
        if sus or not (0x5E00<=sp<=0x5FF2) or pc<0x4000:
            events.append(('CRASH',f,'pc %04x sp %04x'%(pc,sp),' '.join('%04x'%a for a in sus[:8]))); break
        if state=='restarted' and f%(50*10)==0 and 0xC2EC not in g.emap:
            # maybe waiting at title/menus: press space
            g.tap('SP',5,20)
    g.screenshot('work/endfinal_%s.png'%kind)
    if video: g.run(100); g.rec.close()
    return kind, events
if __name__=='__main__':
    print(run2(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else None))
