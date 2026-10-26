import sys
def fib(n):
    a,b=0,1
    for _ in range(n): a,b=b,a+b
    return a
def isqrt(n):
    import math; return math.isqrt(n)
base=[1,4,8,12,41,42,107,220,209,366]
cases=base+[x*x for x in (12,41,42,107,220,209)]+[x*x-1 for x in (12,41,42,107,220,209)]+[x*x+1 for x in (12,41,42,107,220,209)]
cases=sorted(set(cases))
lines=[]; idx=[0]
def new(expr):
    n=len(lines); lines.append(f"out{n} = {expr}"); return n
for i in range(32): new(f"out{i}")            # 0..31 inputs held
nin=[new(f"~out{i}") for i in range(32)]      # 32..63
eqs=[]
for c in cases:
    lit=[ (i if (c>>i)&1 else nin[i]-0) for i in range(32)]
    acc=lit[0]
    for l in lit[1:]: acc=new(f"out{acc} & out{l}")
    eqs.append((c,acc))
outs=[]
for j in range(32):
    sel=[acc for c,acc in eqs if (fib(isqrt(c))%(2**32))>>j &1]
    if not sel: outs.append(new("0")); continue
    acc=sel[0]
    for s in sel[1:]: acc=new(f"out{acc} | out{s}")
    outs.append(acc)
# final 32 signals = copies of outs
for j in range(32): new(f"out{outs[j]}")
open(sys.argv[1],'w').write("\n".join(lines)+"\n")
print("lines",len(lines),"cases",len(cases))
