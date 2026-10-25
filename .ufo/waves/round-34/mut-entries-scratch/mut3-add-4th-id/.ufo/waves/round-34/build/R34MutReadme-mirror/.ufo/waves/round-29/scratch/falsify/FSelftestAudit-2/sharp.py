#!/usr/bin/env python3
"""Sharper mutants + test the concurrent WORKTREE version against the same survivors."""
import subprocess, sys, re, shutil
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
HERE = Path(LANE + "/.ufo/waves/round-29/scratch/falsify/FSelftestAudit-2")
HEAD = HERE / "head/config_projection.py"
WORKTREE = Path(LANE + "/plans/config_projection.py")
W = HERE / "sharp"; shutil.rmtree(W, ignore_errors=True); W.mkdir(parents=True)

TXT = HEAD.read_text()
lines = TXT.splitlines()
appends = [(i+1, l.strip()) for i, l in enumerate(lines) if "cases.append" in l]
def case_for(n):
    c = None
    for ln, t in appends:
        if ln <= n: c = (ln, t)
    return c

SHARP = {
 "S1_escape_backslash_kept_literal": (
  '''    text, steps = raw_text, []
    for name in ORDER:
        token = "__%s__" % name
        steps.append({"name": name, "token": token, "applied_replacements": text.count(token)})
        text = text.replace(token, values[name])
    return text, steps''',
  '''    text, steps = raw_text, []
    for name in ORDER:
        token = "__%s__" % name
        steps.append({"name": name, "token": token, "applied_replacements": text.count(token)})
        text = text.replace(token, values[name].replace("\\\\", "\\\\\\\\"))
    return text, steps'''),
 "S2_url_only_reported_leaves_only": (
  '''        changed, problems = [], []
        diff(original, projected, (), changed, problems)''',
  '''        changed, problems = [], []
        _u = json.loads(json.dumps(original))
        def _ru(node):
            if isinstance(node, dict):
                for _k, _v in list(node.items()):
                    if _k in ("start_url", "reference_url", "url") and isinstance(_v, str):
                        for _n in ORDER:
                            _v = _v.replace("__%s__" % _n, profile["values"][_n])
                        node[_k] = _v
                    elif isinstance(_v, (dict, list)):
                        _ru(_v)
            elif isinstance(node, list):
                for _i in node:
                    _ru(_i)
        _ru(_u)
        diff(original, _u, (), changed, problems)'''),
 "S3_category_always_url": (
  '"category": "url_field" if template(path) in URL_FIELD_TEMPLATES else "non_url_field",',
  '"category": "url_field",'),
 "S4_category_always_non_url": (
  '"category": "url_field" if template(path) in URL_FIELD_TEMPLATES else "non_url_field",',
  '"category": "non_url_field",'),
}

def run(p):
    return subprocess.run([sys.executable, str(p), "--selftest", "--root", LANE],
                          capture_output=True, text=True, timeout=900)

print("=== SHARP mutants against pinned HEAD ===")
for name, (old, new) in sorted(SHARP.items()):
    if old not in TXT:
        print("%-38s PATCH-FAILED" % name); continue
    p = W / ("m_%s.py" % name); p.write_text(TXT.replace(old, new, 1))
    r = run(p)
    if r.returncode == 0:
        print("%-38s SURVIVED" % name); continue
    fr = re.findall(r'File "([^"]+)", line (\d+), in (\S+)', r.stderr)
    inst = [(f, int(l), fn) for f, l, fn in fr if f.endswith(p.name)]
    if not inst:
        print("%-38s KILLED (no frame) %s" % (name, (r.stderr.strip().splitlines() or [""])[-1][:80])); continue
    f, ln, fn = inst[-1]; c = case_for(ln)
    print("%-38s KILLED L%-4d %-12s -> %s" % (name, ln, fn, c[1] if c else "?"))

print()
print("=== concurrent WORKTREE version vs my key survivors ===")
WT = WORKTREE.read_text()
WT_MUT = {
 "url_templates_only_start_url": ('URL_FIELD_TEMPLATES = frozenset({"start_url", "eval.reference_url", "eval.program_html[].url"})',
   'URL_FIELD_TEMPLATES = frozenset({"start_url"})'),
 "audit_always_exit0": ('    return result, int(bool(findings))', '    return result, 0'),
 "drop_leaf_change_unexplained": ('        if unexplained or (not problems and carriers != len(changed)):', '        if False:'),
 "drop_projection_count_invalid": ('    if result["population"]["task_profile_projections"] != POPULATION * len(STIMULUS):\n        findings.append({"id": "projection_count_invalid"})', '    if False:\n        findings.append({"id": "projection_count_invalid"})'),
}
for name, (old, new) in sorted(WT_MUT.items()):
    if old not in WT:
        print("  %-34s PATCH-FAILED (worktree changed)" % name); continue
    p = W / ("wt_%s.py" % name); p.write_text(WT.replace(old, new, 1))
    r = run(p)
    print("  %-34s %s exit=%d" % (name, "SURVIVED" if r.returncode == 0 else "KILLED", r.returncode))
