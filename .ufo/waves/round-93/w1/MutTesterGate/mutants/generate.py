#!/usr/bin/env python3
"""Generate byte-level mutants of plans/round93_freeze_integrity.py (read at T).

Each mutant = exact-substring substitutions; every `old` must occur exactly once in the
source or generation aborts (so no mutant silently degenerates to the null mutant).
Usage: gen.py SRC OUTDIR
"""
import hashlib
import json
import sys
from pathlib import Path

SRC = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
text = SRC.read_bytes().decode()

MUTANTS = [
    ("m01-null", "unchanged copy (must pass)", []),
    ("m02-drop-touched", "drop the touched-after-freeze check",
     [("        if touched:\n", "        if False:\n")]),
    ("m03-rev-compared-to-freeze", "compare freeze bytes instead of rev bytes",
     [("        elif sha(at_t) != want:\n", '        elif sha(at_f or b"") != want:\n')]),
    ("m04-drop-touched-and-rev", "drop touched check AND rev-bytes comparison",
     [("        if touched:\n", "        if False:\n"),
      ("        elif sha(at_t) != want:\n", "        elif False:\n")]),
    ("m05-absent-at-rev-intact", "treat absent-at-rev as intact (reason suppressed)",
     [('            reasons.append("absent-at-rev")\n', "            pass\n")]),
    ("m06-cne-exit0-pass", "could-not-evaluate printed as PREDICATE pass, rc 0",
     [('    except CouldNotEvaluate as error:\n        print(f"DEFECT SETUP {error}")\n'
       '        print("PREDICATE freeze-integrity could-not-evaluate")\n        return 2\n',
       '    except CouldNotEvaluate as error:\n        print(f"DEFECT SETUP {error}")\n'
       '        print("PREDICATE freeze-integrity pass")\n        return 0\n')]),
    ("m07-battery-skipped", "battery list emptied (no in-path battery)",
     [("        bat = battery(bat_dir)\n", "        bat = []\n")]),
    ("m08-battery-nonfatal", "battery red no longer fails the PREDICATE",
     [("    passed = not broken and bat_ok == len(bat)\n", "    passed = not broken\n")]),
    ("m09-battery-b02-weakened", "battery case B02 expectation made always-true",
     [('lambda v: len(v) == 1 and "rev-bytes-differ" in v[0] and "touched-after-freeze=1" in v[0])',
       "lambda v: True)")]),
    ("m10-range-freeze-included", "rev-list range off by one: f^..t includes the freeze commit",
     [('f"{f}..{t}", "--", p)', 'f"{f}^..{t}", "--", p)')]),
    ("m11-range-reversed", "rev-list range reversed (t..f): touched always 0",
     [('f"{f}..{t}", "--", p)', 'f"{t}..{f}", "--", p)')]),
    ("m12-range-three-dot-equivalent", "rev-list symmetric range f...t (equivalent: f is ancestor of t)",
     [('f"{f}..{t}", "--", p)', 'f"{f}...{t}", "--", p)')]),
    ("m13-table-read-at-rev", "parse the frozen table at --rev instead of --freeze",
     [("        text = blob(root, f, claims)\n", "        text = blob(root, t, claims)\n")]),
    ("m14-table-row-prefix", "drop the last table row from evaluation",
     [("    for want, p in table:\n", "    for want, p in table[:-1]:\n")]),
    ("m15-freeze-bytes-unchecked", "freeze-bytes-vs-table comparison removed",
     [("        if at_f is None or sha(at_f) != want:\n", "        if at_f is None:\n")]),
    ("m16-touched-pathspec-dropped", "touched counts every commit in range (pathspec dropped)",
     [('f"{f}..{t}", "--", p)\n        touched', 'f"{f}..{t}")\n        touched')]),
    ("m17-verdict-always-intact", "verdict forced to intact",
     [('"verdict": "intact" if not reasons else "broken:" + "+".join(reasons)',
       '"verdict": "intact"')]),
    ("m18-verdict-always-broken", "verdict forced to broken",
     [('"verdict": "intact" if not reasons else "broken:" + "+".join(reasons)',
       '"verdict": "broken:forced"')]),
    ("m19-ancestry-check-removed", "freeze-is-ancestor check disabled",
     [('    if git(root, "merge-base", "--is-ancestor", f, t).returncode != 0:\n',
       "    if False:\n")]),
    ("m20-reason-text-only", "absent-at-rev reason renamed (text only, verdict still broken)",
     [('            reasons.append("absent-at-rev")\n', '            reasons.append("gone-at-rev")\n'),
      ('lambda v: len(v) == 1 and "absent-at-rev" in v[0])',
       'lambda v: len(v) == 1 and "gone-at-rev" in v[0])')]),
    ("m21-comment-only-equivalent", "trailing comment appended (equivalent)",
     [("\n\nif __name__", "\n\n# mutation probe: comment only\nif __name__")]),
    ("m22-ancestry-args-swapped", "is-ancestor arguments swapped",
     [('"--is-ancestor", f, t).returncode', '"--is-ancestor", t, f).returncode')]),
    ("m23-broken-filter-inverted", "broken list counts intact rows instead",
     [('broken = [r for r in rows if r["verdict"] != "intact"]',
       'broken = [r for r in rows if r["verdict"] == "intact"]')]),
    ("m25-battery-b02-forced-red", "battery case B02 forced red (fatal): kill control",
     [('lambda v: len(v) == 1 and "rev-bytes-differ" in v[0] and "touched-after-freeze=1" in v[0])',
       "lambda v: False)")]),
    ("m26-battery-b02-red-nonfatal", "battery case B02 forced red AND battery non-fatal",
     [('lambda v: len(v) == 1 and "rev-bytes-differ" in v[0] and "touched-after-freeze=1" in v[0])',
       "lambda v: False)"),
      ("    passed = not broken and bat_ok == len(bat)\n", "    passed = not broken\n")]),
    ("m24-empty-table-accepted", "empty frozen-instruments table accepted (no CNE)",
     [('    if not rows:\n        raise CouldNotEvaluate("frozen-instruments table absent or empty")\n',
       "    if not rows:\n        pass\n")]),
]

manifest = []
for name, desc, subs in MUTANTS:
    body = text
    for old, new in subs:
        n = body.count(old)
        if n != 1:
            raise SystemExit(f"{name}: old string occurs {n} times, need 1: {old[:70]!r}")
        body = body.replace(old, new)
    path = OUT / f"{name}.py"
    path.write_bytes(body.encode())
    manifest.append({"id": name, "desc": desc, "subs": len(subs),
                     "sha256": hashlib.sha256(body.encode()).hexdigest(),
                     "identical_to_source": body == text})
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
for m in manifest:
    print(f"{m['id']} subs={m['subs']} identical={m['identical_to_source']} {m['sha256'][:12]}")
