import sys
toks={}
names=r"RND INKEY$ PI FN POINT SCREEN$ ATTR AT TAB VAL$ CODE VAL LEN SIN COS TAN ASN ACS ATN LN EXP INT SQR SGN ABS PEEK IN USR STR$ CHR$ NOT BIN OR AND <= >= <> LINE THEN TO STEP DEF\ FN CAT FORMAT MOVE ERASE OPEN\ # CLOSE\ # MERGE VERIFY BEEP CIRCLE INK PAPER FLASH BRIGHT INVERSE OVER OUT LPRINT LLIST STOP READ DATA RESTORE NEW BORDER CONTINUE DIM REM FOR GO\ TO GO\ SUB INPUT LOAD LIST LET PAUSE NEXT POKE PRINT PLOT RUN SAVE RANDOMIZE IF CLS DRAW CLEAR RETURN COPY".replace('\\ ','_').split()
for k,nm in enumerate(names): toks[0xA5+k]=nm.replace('_',' ')
d=open(sys.argv[1],'rb').read()
i=0
while i<len(d):
    ln=d[i]*256+d[i+1]; L=d[i+2]|d[i+3]<<8; body=d[i+4:i+4+L]; i+=4+L
    s='';j=0
    while j<len(body):
        c=body[j]
        if c==0x0e: j+=6; continue
        if c==0x0d: break
        if c>=0xa5: s+=' '+toks[c]+' '
        elif c>=32 and c<127: s+=chr(c)
        else: s+='{%02x}'%c
        j+=1
    print(ln,s)
