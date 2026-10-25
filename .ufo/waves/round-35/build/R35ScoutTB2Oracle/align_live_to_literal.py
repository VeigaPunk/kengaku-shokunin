import urllib.request, difflib
def get(u): return urllib.request.urlopen(u, timeout=25).read().decode()
def fasta_seq(pid):
    lines=[l.strip() for l in get(f"https://www.rcsb.org/fasta/entry/{pid}/download").split("\n")]
    return lines[1]
def stripM(s): return s[1:] if s.startswith("M") else s
grad = {
 "5WJ2": "GSSHHHHHHSSGENLYFQGHMVSKGEELFTGVVPILVELDGDVNGHKFSVRGEGEGDATNGKLTLKFICTTGKLPVPWPTLVTTFGYGVACFSRYPDHMKQHDFFKSAMPEGYVQERTISFKDDGTYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNFNSHNVYITADKQKNGIKANFKIRHNVEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSHQSALSKDPNEKRDHMVLLEFVTAAGITHGMDELYK",
 "2H5Q": "VSKGEEDNMAIIKEFMRFKVHMEGSVNGHEFEIEGEGEGRPYEGTQTAKLKVTKGGPLPFAWDILSPQFMYGSKAYVKHPADIPDYLKLSFPEGFKWERVMNFEDGGVVTVTQDSSLQDGEFIYKVKLRGTNFPSDGPVMQKKTMGWEASSERMYPEDGALKGEIKQRLKLKDGGHYDAEVKTTYKAKKPVQLPGAYNVNIKLDITSHNEDYTIVEQYERAEGRHSTGGMDELYK",
}
for pid,g in grad.items():
    live = stripM(fasta_seq(pid))
    print("== %s grad_len=%d live_len=%d"%(pid,len(g),len(live)))
    sm = difflib.SequenceMatcher(None, g, live, autojunk=False)
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag!="equal":
            print("   %-8s grader[%d:%d]=%r  live[%d:%d]=%r"%(tag,i1,i2,g[i1:i2],j1,j2,live[j1:j2]))
