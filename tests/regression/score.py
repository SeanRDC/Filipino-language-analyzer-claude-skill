"""Score a cleaned transcript table (| mm:ss | line | conf |) against a reference by word alignment.

Usage: python -I tests/regression/score.py <reference.md> <cleaned.md> [skip-ids]
Env HYPSKIP="22-30,..." drops output rows whose start second is in [a,b) (stretches the reference does not cover).
"""
import re, sys, unicodedata
def secs(t): m,s=t.split(':')[:2]; return int(m)*60+int(s)
def norm(s):
    s=unicodedata.normalize('NFKC',s).lower()
    s=re.sub(r'\([^)]*\)|\[[^\]]*\]','',s)            # stage notes
    s=re.sub(r'(^|/)\s*[a-z]{1,8}:\s',r'\1 ',s)         # speaker labels
    s=s.replace('’',"'").replace('-','')
    s=re.sub(r"'",'',s)
    s=re.sub(r'[^a-z0-9ñ ]+',' ',s)
    w=s.split()
    alias={'noong':'nung','ganoon':'ganun','ganon':'ganun','diyan':'dyan','nandiyan':'nandyan','niya':'nya','siya':'sya','ito':'to','iyon':'yon','yun':'yon','ako':'ko','okay':'ok'}
    alias.update({'nun':'nung','noon':'nung','noong':'nung','don':'dun','doon':'dun','gano':'gaano','nasan':'nasaan','ingles':'english','inglesingles':'englishenglish','plastik':'plastic','kaagad':'agad','yung':'yon_','iyong':'yon_'})
    w=[alias.get(x,x) for x in w]
    out=[]
    for x in w:
        if out and out[-1]=='sa' and x in ('kin','yo','kanya'): out[-1]='sa'+x; continue
        out.append(x)
    return out
def ed(a,b):
    d=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        p,d[0]=d[0],i
        for j,y in enumerate(b,1):
            p,d[j]=d[j],min(d[j]+1,d[j-1]+1,p+(x!=y))
    return d[-1]
ref=[]
for l in open(sys.argv[1],encoding='utf-8'):
    m=re.match(r'(L\d+) \| ([\d:]+)\S* \| (.) \| (.*)',l)
    if m: ref.append((m[1],secs(m[2]),m[3]=='*',m[4]))
hyp=[]
for l in open(sys.argv[2],encoding='utf-8'):
    m=re.match(r'\|\s*\**(\d{1,2}:\d{2})[^|]*\|(.*?)\|',l)
    if m: hyp.append((secs(m[1]),m[2]))
skip=set(sys.argv[3].split(',')) if len(sys.argv)>3 else set()
R=[];tag=[]
for lid,t,fx,r in ref:
    for w in norm(r): R.append(w); tag.append(lid)
import os
rng=[tuple(map(int,r.split('-'))) for r in os.environ.get('HYPSKIP','').split(',') if r]
H=[w for ht,x in hyp if not any(a<=ht<b for a,b in rng) for w in norm(x)]
n1,n2=len(R),len(H)
D=[[0]*(n2+1) for _ in range(n1+1)]
for i in range(n1+1): D[i][0]=i
for j in range(n2+1): D[0][j]=j
for i in range(1,n1+1):
    Di,Dp,ri=D[i],D[i-1],R[i-1]
    for j in range(1,n2+1):
        Di[j]=min(Dp[j]+1,Di[j-1]+1,Dp[j-1]+(ri!=H[j-1]))
err={};got={}
i,j=n1,n2
while i>0 or j>0:
    if i>0 and j>0 and D[i][j]==D[i-1][j-1]+(R[i-1]!=H[j-1]):
        l=tag[i-1]; err[l]=err.get(l,0)+(R[i-1]!=H[j-1]); got.setdefault(l,[]).append(H[j-1]); i-=1;j-=1
    elif i>0 and D[i][j]==D[i-1][j]+1:
        l=tag[i-1]; err[l]=err.get(l,0)+1; i-=1
    else:
        l=tag[i] if i<n1 else tag[-1]; err[l]=err.get(l,0)+1; got.setdefault(l,[]).append('+'+H[j-1]); j-=1
n=ok=fn=fok=tw=te=0; out=[]
for lid,t,fx,r in ref:
    if lid in skip: continue
    e=err.get(lid,0); L=len(norm(r)); n+=1; tw+=L; te+=e; ok+=e==0
    if fx: fn+=1; fok+=e==0
    if e: out.append(f"{lid} err={e}/{L}\n  REF: {r}\n  HYP: {' '.join(reversed(got.get(lid,[])))}")
print(f"lines exact: {ok}/{n} = {ok/n:.0%} | Sean-fixed lines exact: {fok}/{fn} | word accuracy: {1-te/tw:.1%}")
print('\n'.join(out))
