import re, hashlib, pathlib, subprocess, json, sys
lane = pathlib.Path("cloneT")
sources_lines = (lane/"corpus/SOURCES.md").read_text(errors="replace").splitlines()
rows = ["S173","S174","S175","S176","S177","S180","S220","S225","S270","S285","S293","S306"]
def token_for(row):
    toks=[]
    for line in sources_lines:
        if f"| {row} |" in line:
            toks += re.findall(r'sha256\s+([0-9a-f]{64})', line)
    return toks
prov_files = ["corpus/evidence/round50/PROVENANCE.md","corpus/evidence/round59/PROVENANCE.md","corpus/evidence/round61/PROVENANCE.md","corpus/evidence/round79/PROVENANCE.md","corpus/evidence/round82/PROVENANCE.md","corpus/evidence/round92/PROVENANCE.md","corpus/evidence/round93/PROVENANCE.md","corpus/evidence/round95/PROVENANCE.md"]
results=[]
all_prov_lines=[]
url_hits=[]
for pf in prov_files:
    text=(lane/pf).read_text(errors="replace")
    # URL check: no http:// https:// in the file? PROVENANCE.md itself contains no URL columns; check for http
    if "http://" in text or "https://" in text:
        url_hits.append(pf)
    for line in text.splitlines():
        if line.strip().startswith("|") and "S" in line:
            # parse | Sxxx | `file` | `sha` |
            m=re.match(r'\|\s*(S\d+)\s*\|\s*`([^`]+)`\s*\|\s*`([0-9a-f]{64})`\s*\|',line.strip())
            if m:
                all_prov_lines.append((pf,m.group(1),m.group(2),m.group(3)))
            else:
                results.append(f"UNPARSED provenance line in {pf}: {line}")
for row in rows:
    toks=token_for(row)
    matched=[x for x in all_prov_lines if x[1]==row]
    if len(matched)!=1:
        results.append(f"{row} count={len(matched)} !=1 token={toks} matched={matched}")
        continue
    pf,file_rel,sha = matched[0][0],matched[0][2],matched[0][3]
    # bound capture path: dir of prov + file_rel
    cap = lane/pathlib.Path(pf).parent/file_rel
    if not cap.exists():
        results.append(f"{row} capture missing {cap}")
        continue
    actual=hashlib.sha256(cap.read_bytes()).hexdigest()
    ok_token = (toks==[sha]==[actual]) or (sha in toks and sha==actual)
    # exact: sha256 of bound capture equals row anchor token AND PROVENANCE sha column
    if actual!=sha or sha not in toks:
        results.append(f"{row} FAIL actual={actual} prov={sha} token={toks} cap={cap}")
    else:
        results.append(f"{row} PASS cap={cap.relative_to(lane)} actual={actual} prov={sha} token={toks[0]}")
print("\n".join(results))
print("URL_HITS", url_hits)
print("PROV_LINES", len(all_prov_lines))
for x in all_prov_lines: print(x)
