import sys
from skoolkit import CSimulator
from skoolkit.simulator import Simulator
from skoolkit.snapshot import Snapshot, write_snapshot
from skoolkit.simutils import from_snapshot, PC, T, get_state
from skoolkit.pagingtracer import PagingTracer

FRAME=69888
# key name -> (row, bit)
KEYS={}
rows=[['CS','Z','X','C','V'],['A','S','D','F','G'],['Q','W','E','R','T'],['1','2','3','4','5'],
      ['0','9','8','7','6'],['P','O','I','U','Y'],['EN','L','K','J','H'],['SP','SS','M','N','B']]
for r,ks in enumerate(rows):
    for b,k in enumerate(ks): KEYS[k]=(r,b)

class Tr(PagingTracer):
    def __init__(self):
        self.keyboard=[0]*8
        self.writes=[]; self.border=0; self.outfe=0; self.out7ffd=0; self.outfffd=0; self.ay=[0]*16
    def read_port(self, registers, port):
        if port % 2 == 0:
            h=(port//256)^0xFF; v=0x40; i=0
            while h:
                if h%2: v|=self.keyboard[i]
                h//=2; i+=1
            return v^0xFF
        return 0xFF
    def write_port(self, registers, port, value, offset=0):
        pass

class Game:
    def __init__(self, sna):
        import os
        if os.environ.get('STONK')=='fixed' and sna=='work/stonk.z80': sna='work/stonk_fixed.z80'
        self.snap=Snapshot.get(sna)
        self.sim=from_snapshot(CSimulator or Simulator, self.snap, {}, {}, {'fast_djnz':False,'fast_ldir':False}, None)
        self.tr=Tr(); self.sim.set_tracer(self.tr)
        self.mem=self.sim.memory; self.reg=self.sim.registers
        self.emap=set()
    def press(self,*keys):
        kb=[0]*8
        for k in keys:
            r,b=KEYS[k]; kb[r]|=1<<b
        self.tr.keyboard[:]=kb
    rec=None; fcount=0
    def run(self, frames=1, stop=-1, emap=True):
        if frames>=1 and float(frames).is_integer():
            for i in range(int(frames)):
                self._run1(1, stop, emap)
                self.fcount+=1
                if self.rec is not None and self.fcount%2==0: self.rec.frame(self.mem, self.fcount)
            return 0
        return self._run1(frames, stop, emap)
    def _run1(self, frames=1, stop=-1, emap=True):
        t=self.reg[T]+int(frames*FRAME)
        cond,ops=self.sim.trace(self.reg[PC], stop, 0, t, 1, None, self.emap if emap else None, None, None, None)
        return cond
    def tap(self,key,frames=3,after=3):
        self.press(key); self.run(frames); self.press(); self.run(after)
    def save(self,fn):
        ram,regs,state,machine=get_state(self.sim); write_snapshot(fn,ram,regs,state,machine)
    def savemap(self,fn):
        open(fn,'w').write(''.join(f'${a:04X}\n' for a in sorted(self.emap)))
    def start_game(self):
        self.run(800); self.tap('SP',5,100); self.run(150); self.tap('SP',5,20); self.run(200); self.tap('SP',5,20); self.run(300)
    def screenshot(self,fn):
        from skoolkit.snapshot import Snapshot
        import subprocess
        # write raw 48K memory as .sna-like via bin2sna? simpler: write scr and use sna2img on .scr
        open(fn+'.scr','wb').write(bytes(self.mem[16384:23296]))
        subprocess.run([sys.prefix+'/bin/sna2img.py','-s','2',fn+'.scr',fn],check=True)

def montage(files, out, cols=3):
    import subprocess
    rows=[files[i:i+cols] for i in range(0,len(files),cols)]
    rfs=[]
    for k,r in enumerate(rows):
        rf=out+f'.row{k}.png'; subprocess.run(['magick',*r,'+append','-resize','50%',rf],check=True); rfs.append(rf)
    subprocess.run(['magick',*rfs,'-append',out],check=True)

def shots(g,n,step,name):
    fs=[]
    for i in range(n):
        g.run(step); f=f'work/{name}_{i}.png'; g.screenshot(f); fs.append(f)
    montage(fs,f'work/{name}.png')
