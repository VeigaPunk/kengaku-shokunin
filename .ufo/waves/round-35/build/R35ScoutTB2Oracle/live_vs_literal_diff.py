import urllib.request, difflib
def get(u): return urllib.request.urlopen(u, timeout=25).read().decode()
def fasta_seq(pid):
    lines=[l.strip() for l in get(f"https://www.rcsb.org/fasta/entry/{pid}/download").split("\n")]
    if len(lines)>3: return None, len(lines)
    return lines[1], len(lines)
def stripM(s): return s[1:] if s.startswith("M") else s
cases = {
 "5WJ2(donor)": ("GSSHHHHHHSSGENLYFQGHMVSKGEELFTGVVPILVELDGDVNGHKFSVRGEGEGDATNGKLTLKFICTTGKLPVPWPTLVTTFGYGVACFSRYPDHMKQHDFFKSAMPEGYVQERTISFKDDGTYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNFNSHNVYITADKQKNGIKANFKIRHNVEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSHQSALSKDPNEKRDHMVLLEFVTAAGITHGMDELYK",
   "MGSSHHHHHHSSGENLYFQGHMVSKGEELFTGVVPILVELDGDVNGHKFSVRGEGEGDATNGKLTLKFICTTGKLPVPWPTLVTTFGYGVACFSRYPDHMKQHDFFKSAMPEGYVQERTISFKDDGTYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNFNSHNVYITADKQKNGIKANFKIRHNVEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSHQSALSKDPNEKRDHMVLLEFVTAAGITHGMDELYK"),
 "2H5Q(acceptor)": ("VSKGEEDNMAIIKEFMRFKVHMEGSVNGHEFEIEGEGEGRPYEGTQTAKLKVTKGGPLPFAWDILSPQFMYGSKAYVKHPADIPDYLKLSFPEGFKWERVMNFEDGGVVTVTQDSSLQDGEFIYKVKLRGTNFPSDGPVMQKKTMGWEASSERMYPEDGALKGEIKQRLKLKDGGHYDAEVKTTYKAKKPVQLPGAYNVNIKLDITSHNEDYTIVEQYERAEGRHSTGGMDELYK",
   "MVSKGEEDNMAIIKEFMRFKVHMEGSVNGHEFEIEGEGEGRPYEGTQTAKLKVTKGGPLPFAWDILSPQFMYGSKAYVKHPADIPDYLKLSFPEGFKWERVMNFEDGGVVTVTQDSSLQDGEFIYKVKLRGTNFPSDGPVMQKKTMGWEASSERMYPEDGALKGEIKQRLKLKDGGHYDAEVKTTYKAKKPVQLPGAYNVNIKLDITSHNEDYTIVEQYERAEGRHSTGGMDELYK"),
}
for label,(lit, live) in cases.items():
    s = stripM(live)
    print("== %s lit_len=%d live_len=%d live_stripM_len=%d equal=%s"%(label,len(lit),len(live),len(s),s==lit))
    if s!=lit:
        # find first mismatch
        n=min(len(s),len(lit))
        for i in range(n):
            if s[i]!=lit[i]:
                print("   first mismatch at %d: live=%r lit=%r"%(i,s[i],lit[i]))
                print("   live ctx: %r"%s[max(0,i-20):i+20])
                print("   lit  ctx: %r"%lit[max(0,i-20):i+20])
                break
        else:
            print("   common prefix identical; length differs (live=%d lit=%d)"%(len(s),len(lit)))
            print("   live tail: %r"%s[n:n+40]); print("   lit tail: %r"%lit[n:n+40])
# verify against live API (not my hardcoded copy)
for pid, lit, lbl in [("5WJ2",cases["5WJ2(donor)"][0],"donor"),("2H5Q",cases["2H5Q(acceptor)"][0],"acceptor")]:
    live,nl = fasta_seq(pid)
    print("%s live fetch: lines=%d len=%d stripM_match=%s"%(pid,nl,len(live),stripM(live)==lit))
