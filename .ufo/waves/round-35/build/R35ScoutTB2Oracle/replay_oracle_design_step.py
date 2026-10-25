import re, sys, random
from Bio.Seq import Seq
from dnachisel import CodonOptimize, DnaOptimizationProblem, EnforceGCContent, EnforceTranslation
from dnachisel.biotools import reverse_translate
exec(open('/tmp/k35_replay.py').read().split('if __name__')[0].split('# literals')[0].split('import re, sys')[1].replace('from Bio.Seq import Seq','').replace('from dnachisel import','#'),globals()) if False else None
donor_aa = "GSSHHHHHHSSGENLYFQGHMVSKGEELFTGVVPILVELDGDVNGHKFSVRGEGEGDATNGKLTLKFICTTGKLPVPWPTLVTTFGYGVACFSRYPDHMKQHDFFKSAMPEGYVQERTISFKDDGTYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNFNSHNVYITADKQKNGIKANFKIRHNVEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSHQSALSKDPNEKRDHMVLLEFVTAAGITHGMDELYK"
dhfr_aa = "ISLIAALAVDRVIGMENAMPWNLPADLAWFKRNTLNKPVIMGRHTWESIGRPLPGRKNIILSSQPGTDDRVTWVKSVDEAIAACGDVPEIMVIGGGRVYEQFLPKAQKLYLTHIDAEVEGDTHFPDYEPDDWESVFSEFHDADAQNSHSYCFEILERR"
acceptor_aa = "VSKGEEDNMAIIKEFMRFKVHMEGSVNGHEFEIEGEGEGRPYEGTQTAKLKVTKGGPLPFAWDILSPQFMYGSKAYVKHPADIPDYLKLSFPEGFKWERVMNFEDGGVVTVTQDSSLQDGEFIYKVKLRGTNFPSDGPVMQKKTMGWEASSERMYPEDGALKGEIKQRLKLKDGGHYDAEVKTTYKAKKPVQLPGAYNVNIKLDITSHNEDYTIVEQYERAEGRHSTGGMDELYK"
snap_aa = "GPGSDKDCEMKRTTLDSPLGKLELSGCEQGLHEIIFLGKGTSAADAVEVPAPAAVLGGPEPLMQATAWLNAYFHQPEAIEEFPVPALHHPVFQQESFTRQVLWKLLKVVKFGEVISYSHLAALAGNPAATAAVKTALSGNPVPILIPCHRVVQGDLDVGGYEGGLAVKEWLLAHEGHRLGKR"
flag="DYKDDDDK"
def stripM(s): return s[1:] if s.startswith("M") else s
def windows_gc(s):
    g=s.lower(); return [sum(c in "gc" for c in g[i:i+50]) for i in range(len(g)-49)]
def grade(gb):
    errs=[]
    with open(gb) as f: lines=[l.rstrip() for l in f]
    if len(lines)!=1: return ["line count %d"%len(lines)],None
    g=lines[0].lower()
    if not re.fullmatch(r"[atcg]+",g): errs.append("alphabet")
    if len(g)>3000: errs.append("len")
    aa=str(Seq(g).translate())
    fi=aa.find(flag); di=aa.find(donor_aa); hi=aa.find(dhfr_aa); ai=aa.find(acceptor_aa); si=aa.find(snap_aa)
    if not(fi<di<hi<ai<si): errs.append("order %d %d %d %d %d"%(fi,di,hi,ai,si))
    if fi!=0: errs.append("flag@%d"%fi)
    for st,en in [(fi+8,di),(di+len(donor_aa),hi),(hi+len(dhfr_aa),ai),(ai+len(acceptor_aa),si)]:
        l=aa[st:en]
        if not re.fullmatch(r"[GS]+",l): errs.append("linker-alphabet")
        if not(5<=len(l)<=20): errs.append("linker-len %d"%len(l))
    if si+len(snap_aa)!=len(aa): errs.append("snap-end")
    w=windows_gc(g)
    if w and not all(15<=x<=35 for x in w): errs.append("gc range %d..%d"%(min(w),max(w)))
    return errs,w
res=[]
for seed in range(30):
    random.seed(seed); 
    import numpy as np; np.random.seed(seed)
    donor,acceptor,snap,dhfr = map(stripM,(donor_aa,acceptor_aa,snap_aa,dhfr_aa))
    gl="GGGGS"*3
    fusion=f"{flag}{gl}{donor}{gl}{dhfr}{gl}{acceptor}{gl}{snap}"
    p=DnaOptimizationProblem(sequence=reverse_translate(fusion,randomize_codons=False),
        constraints=[EnforceTranslation(translation=fusion),EnforceGCContent(mini=0.3,maxi=0.7,window=50)],
        objectives=[CodonOptimize(species="e_coli")])
    p.resolve_constraints(); p.optimize()
    seq=str(p.sequence); open("/tmp/k35_gb_%d.txt"%seed,"w").write(seq)
    errs,w=grade("/tmp/k35_gb_%d.txt"%seed)
    at15=sum(1 for x in w if x==15); at35=sum(1 for x in w if x==35)
    print("seed%02d nt=%d aa=%d gcmin=%d gcmax=%d windows=%d at15=%d at35=%d grade=%s %s"%(seed,len(seq),len(fusion),min(w),max(w),len(w),at15,at35,"PASS" if not errs else "FAIL","; ".join(errs[:3])))
    res.append(not errs)
print("SUMMARY seeds=%d grader_pass=%d"%(len(res),sum(res)))
