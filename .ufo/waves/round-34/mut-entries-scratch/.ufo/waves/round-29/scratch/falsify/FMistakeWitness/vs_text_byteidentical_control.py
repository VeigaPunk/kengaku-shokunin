"""SHARPEST TEST: a VALUE-SHAPE derived control implemented at TEXT level (byte surgery, no
re-serialization). On the frozen data it is BYTE-IDENTICAL to the production projection.
Question: does --selftest kill it? And does --summary stay findings=0 exit=0?"""
import hashlib,json,os,re,shutil,subprocess,sys
BASE="/tmp/fm-witness-2/base"; W="/tmp/fm-witness-2/workB"
shutil.rmtree(W,ignore_errors=True); os.makedirs(W)
def run(a,c):
    p=subprocess.run([sys.executable,"plans/config_projection.py","--root","."]+a,cwd=c,capture_output=True,text=True)
    return p.returncode,p.stdout,p.stderr
SRC=open(os.path.join(BASE,"plans/config_projection.py"),encoding="utf-8").read()
helper='''
def _vs_text_project(raw_text, values):
    """MUTANT (value-shape URL-only, TEXT level): splice tokens only inside string literals whose
    ORIGINAL decoded value starts with a known token. Byte surgery: no re-serialization."""
    spans = []
    for m in re.finditer(r'"(?:[^"\\\\]|\\\\.)*"', raw_text):
        try:
            decoded = json.decoder.scanstring(m.group(0), 1)[0]
        except ValueError:
            continue
        if any(decoded.startswith("__%s__" % n) for n in ORDER):
            spans.append((m.start(), m.end()))
    out, prev = [], 0
    for a, b in sorted(spans):
        seg = raw_text[a:b]
        for n in ORDER:
            seg = seg.replace("__%s__" % n, values[n])
        out.append(raw_text[prev:a]); out.append(seg); prev = b
    out.append(raw_text[prev:])
    return "".join(out)
'''
s=SRC.replace('def string_spans(text):', helper.strip()+"\n\ndef string_spans(text):")
anchor='        projected_text, steps = project(raw_text, profile["values"])'
assert anchor in s
s=s.replace(anchor, anchor+'\n        projected_text = _vs_text_project(raw_text, profile["values"])\n        steps = [{"name": n, "token": "__%s__" % n, "applied_replacements": raw_text.count("__%s__" % n)} for n in ORDER]')
d=os.path.join(W,"vs_text"); shutil.copytree(BASE,d)
open(os.path.join(d,"plans/config_projection.py"),"w").write(s)
st=run(["--selftest"],d); sm=run(["--summary"],d); j=run(["--json"],d)
open(os.path.join(W,"vs_summary.txt"),"w").write(sm[1]); open(os.path.join(W,"vs.json"),"w").write(j[1])
print("VALUE-SHAPE TEXT-LEVEL CONTROL:")
print("  selftest_exit:", st[0])
print("  selftest stderr tail:", (st[2].strip().splitlines()[-1] if st[2].strip() else ""))
frames=re.findall(r'File "([^"]+)", line (\d+), in (\S+)', st[2])
lines=open(os.path.join(d,"plans/config_projection.py"),encoding="utf-8").read().split("\n")
for f,l,fn in frames:
    if fn=="selftest": print("  kill_site line",l,":",lines[int(l)-1].strip()[:110])
print("  summary_exit:", sm[0], "|", sm[1].strip().splitlines()[-1])
# compare against control
d2=os.path.join(W,"ctl"); shutil.copytree(BASE,d2)
sm2=run(["--summary"],d2)[1]; j2=run(["--json"],d2)[1]
open(os.path.join(W,"ctl_summary.txt"),"w").write(sm2)
print("  summary identical to control:", sm2==sm[1])
import difflib
print("  --- summary diff (control vs value_shape_text) ---")
for l in difflib.unified_diff(sm2.splitlines(), sm[1].splitlines(), "control","vs_text", lineterm="", n=0): print("   ",l)
a=json.loads(j2); b=json.loads(j[1])
print("  JSON differing top keys:", [k for k in a if a[k]!=b.get(k)])
for p in a["profiles"]:
    print("   profile",p,"differing:",[k for k in a["profiles"][p] if a["profiles"][p][k]!=b["profiles"][p].get(k)])
