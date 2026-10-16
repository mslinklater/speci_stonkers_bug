import sys,struct
d=open(sys.argv[1],'rb').read()
i=0;n=0
while i<len(d):
    L=struct.unpack('<H',d[i:i+2])[0]
    blk=d[i+2:i+2+L]
    flag=blk[0]
    x=0
    for b in blk: x^=b
    if flag==0:
        t=blk[1];name=blk[2:12];dl,p1,p2=struct.unpack('<HHH',blk[12:18])
        print(n,'HDR type',t,name,'len',dl,'p1',p1,'p2',p2,'xor',x)
    else:
        print(n,'DATA len',L-2,'flag',flag,'xor',x, 'offset',i+3)
    i+=2+L;n+=1
