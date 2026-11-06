import re, subprocess, io, tokenize, json
LANE="/fast/scratch/hyaku/kengaku-r97/ExecHarm/laneT"; TIP="f1083da60e7ff6b88f7420aae7424f7762d14700"
def show(rev,path):
    p=subprocess.run(["git","-C",LANE,"show",f"{rev}:{path}"],capture_output=True)
    return p.stdout.decode(errors="replace") if p.returncode==0 else None
def rows(text):
    lines=text.splitlines(); i=next(j for j,l in enumerate(lines) if l.startswith("## Gate/probe registry"))
    out={}
    for ln in lines[i+1:]:
        if ln.startswith("## "): break
        if not ln.startswith("|"): continue
        cells=[c.strip() for c in re.split(r"(?<!\\)\|",ln)[1:-1]]
        if len(cells)<3 or cells[1] not in ("gate","probe"): continue
        out[cells[0].strip("` ")]=cells
    return out
SCRIPT=re.compile(r"([\w./-]+\.(?:py|sh|mjs))")
SPELL=re.compile(r"add_argument\(\s*[\"']--self-?test[\"']|add_parser\(\s*[\"']self-?test[\"']|[\"']--self-?test[\"']\s*(?:in|==|not in)\b|(?:\bin|==)\s*\(?[\"']--self-?test[\"']|def run_selftest\b|(?:==|\bin)\s*\(?[\"']self-?test[\"']")
def classify(src):
    """Return list of (lineno, kind) for each SPELL match: kind in code|comment|string-doc|string-arg."""
    out=[]
    try:
        toks=list(tokenize.generate_tokens(io.StringIO(src).readline))
    except Exception as e:
        return [(0,"tokenize-error:"+type(e).__name__)]
    # map token spans
    for m in SPELL.finditer(src):
        line=src[:m.start()].count("\n")+1
        kind="code"
        for t in toks:
            if t.type in (tokenize.COMMENT, tokenize.STRING):
                (sl,sc),(el,ec)=t.start,t.end
                # position of match
                ml=m.start(); 
                # convert match offset to (line,col)
                pre=src[:ml]; mline=pre.count("\n")+1; mcol=len(pre.rsplit("\n",1)[-1])
                if (mline,mcol) >= (sl,sc) and (mline,mcol) < (el,ec):
                    if t.type==tokenize.COMMENT: kind="comment"
                    else:
                        # docstring if the string token starts a logical line (prev significant token is NEWLINE/INDENT/DEDENT/ENCODING)
                        idx=toks.index(t); prev=None
                        for q in reversed(toks[:idx]):
                            if q.type in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.ENCODING, tokenize.COMMENT): continue
                            prev=q; break
                        kind = "string-doc" if prev is None or prev.type in (tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT) else "string-arg"
                    break
        out.append((line,kind))
    return out
t=rows(show(TIP,"SKILL.md"))
gates=[n for n,c in t.items() if c[1]=="gate"]
print("gate rows",len(gates))
prose_only=[]; code_ok=[]
for n in gates:
    m=SCRIPT.search(t[n][2]); path=m.group(1)
    src=show(TIP,path)
    if src is None: prose_only.append((n,path,"absent")); continue
    cls=classify(src)
    kinds={k for _,k in cls}
    if kinds & {"code","string-arg"}: code_ok.append(n)
    else: prose_only.append((n,path,sorted(kinds),cls[:3]))
print("gate rows with a CODE-level spelling:",len(code_ok))
print("gate rows whose only spellings are prose/comment:",len(prose_only))
for x in prose_only: print("  PROSE-ONLY",x)
json.dump({"prose_only":[list(map(str,x)) for x in prose_only]},open("/fast/scratch/hyaku/kengaku-r97/ExecHarm/an/spelling_classify.json","w"),indent=1)
