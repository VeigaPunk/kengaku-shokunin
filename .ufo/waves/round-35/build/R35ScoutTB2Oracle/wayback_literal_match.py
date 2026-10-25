import urllib.request, urllib.parse, json, difflib
grad_donor = "GSSHHHHHHSSGENLYFQGHMVSKGEELFTGVVPILVELDGDVNGHKFSVRGEGEGDATNGKLTLKFICTTGKLPVPWPTLVTTFGYGVACFSRYPDHMKQHDFFKSAMPEGYVQERTISFKDDGTYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNFNSHNVYITADKQKNGIKANFKIRHNVEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSHQSALSKDPNEKRDHMVLLEFVTAAGITHGMDELYK"
grad_acc = "VSKGEEDNMAIIKEFMRFKVHMEGSVNGHEFEIEGEGEGRPYEGTQTAKLKVTKGGPLPFAWDILSPQFMYGSKAYVKHPADIPDYLKLSFPEGFKWERVMNFEDGGVVTVTQDSSLQDGEFIYKVKLRGTNFPSDGPVMQKKTMGWEASSERMYPEDGALKGEIKQRLKLKDGGHYDAEVKTTYKAKKPVQLPGAYNVNIKLDITSHNEDYTIVEQYERAEGRHSTGGMDELYK"
def get(u): return urllib.request.urlopen(u, timeout=40).read().decode(errors="replace")
def cdx(url):
    q = urllib.parse.urlencode({"url":url,"output":"json","limit":"20","from":"2024"})
    r = json.loads(get("http://web.archive.org/cdx/search/cdx?"+q))
    return r[1:] if len(r)>1 else []
def wbseq(ts, pid):
    u = f"https://web.archive.org/web/{ts}id_/https://www.rcsb.org/fasta/entry/{pid}/download"
    txt = get(u)
    lines = txt.split("\n")
    for l in lines:
        if l.startswith(">") or not l.strip(): continue
        return l.strip()
    return None
def stripM(s): return s[1:] if s.startswith("M") else s
for pid, grad, lbl in (("5WJ2", grad_donor, "donor"), ("2H5Q", grad_acc, "acceptor")):
    snaps = cdx(f"rcsb.org/fasta/entry/{pid}/download")
    print("== %s (%s): %d wayback snapshot(s)" % (pid, lbl, len(snaps)))
    for row in snaps:
        ts = row[1]
        try: s = wbseq(ts, pid)
        except Exception as e: print("   %s fetch-fail %s"%(ts,e)); continue
        if not s: print("   %s no-seq"%ts); continue
        sm = stripM(s)
        print("   %s len=%d X=%d  stripM==grader_literal: %s" % (ts, len(s), s.count("X"), sm == grad))
