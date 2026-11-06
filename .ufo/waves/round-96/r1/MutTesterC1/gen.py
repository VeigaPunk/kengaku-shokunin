#!/usr/bin/env python3
"""Generate single-point mutants of plans/round96_c1_replay.py into $S/mut/.

Each mutant = pristine bytes with exactly ONE substring replaced (asserted count==1).
Pristine bytes are the T worktree file; sha256 asserted against the frozen-instruments table.
"""
import hashlib
import pathlib
import sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r96/MutTesterC1")
SRC = S / "lane/plans/round96_c1_replay.py"
OUT = S / "mut"
FROZEN_SHA = "0752287902145fe1adc49f985978905244dc906f1015eb88874b39182bf8940c"

orig = SRC.read_text()
got = hashlib.sha256(orig.encode()).hexdigest()
if got != FROZEN_SHA:
    sys.exit(f"pristine sha mismatch: {got}")

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "M00-orig.py").write_text(orig)

MUTANTS = {
    # each leg's condition dropped (9)
    "M01-L1-true": ("l1 = receipt_bytes is not None", "l1 = True"),
    "M02-L2-true": ("l2 = (all(", "l2 = True or (all("),
    "M03-L3-true": ("l3 = bool(tip)", "l3 = True or bool(tip)"),
    "M04-L4-true": ("l4 = bool(frozen.get(TABLE))", "l4 = True or bool(frozen.get(TABLE))"),
    "M05-L5-true": ("l5 = bool(predicted)", "l5 = True or bool(predicted)"),
    "M06-L6-true": ("l6 = rerun.returncode == 0 and", "l6 = True or (rerun.returncode == 0) and"),
    "M07-L7-true": ('l7 = (member.get("status") == "executed"', 'l7 = True or (member.get("status") == "executed"'),
    "M08-L8-true": ("l8 = bool(frozen.get(TOOL))", "l8 = True or bool(frozen.get(TOOL))"),
    "M09-L9-true": ('l9 = (f.get("TOOL_SHA")', 'l9 = True or (f.get("TOOL_SHA")'),
    # named in the tasking
    "M10-set-ge-eq": ("rev_set >= base_set | {MEMBER}", "rev_set == base_set | {MEMBER}"),
    "M11-cwd-flip": ("if Path.cwd().resolve() != lane:", "if Path.cwd().resolve() == lane:"),
    "M12-rc-flip": ("return 0 if ok else 1", "return 1 if ok else 0"),
    "M13a-target-rows": ("% (exec_total, MEMBER,", "% (len(members), MEMBER,"),
    "M13b-target-member": ('% (exec_total, MEMBER,', '% (exec_total, "wrong-member",'),
    # further single-point probes
    "M14-ancestor-dir": ('"merge-base", "--is-ancestor", tip, rev)', '"merge-base", "--is-ancestor", rev, tip)'),
    "M15-l5-seen-subset": ("seen == set(predicted)", "seen <= set(predicted)"),
    "M16-round-95": ('member.get("round") == 96', 'member.get("round") == 95'),
    "M17-drop-notinbase": ("MEMBER not in base_set and rev_set >=", "rev_set >="),
    "M18-drop-legacy": ("set_ok and legacy_ok)", "set_ok)"),
    "M19-pins-first-only": ("for p, want in PINS.items())", "for p, want in list(PINS.items())[:1])"),
    "M20-l9-drop-hostbash": ('          and f.get("HOST_BASH") == host_tool(["/usr/bin/bash", "--version"]))', "          and True)"),
    "M21-stamps-drop-graderside": ('RERUN_STAMPS = ("TOOL_SHA", "CASE_TABLE_SHA", "ENV_SIDE", "GRADER_SIDE")', 'RERUN_STAMPS = ("TOOL_SHA", "CASE_TABLE_SHA", "ENV_SIDE")'),
    "M22-work-guard-weaken": ("if work == lane or lane in work.parents:", "if work == lane:"),
    "M23-drop-rev-guard": ('        raise CouldNotEvaluate(f"unresolved-revision {a.rev}")', "        pass  # mutant: unresolved-revision guard dropped"),
    "M24-drop-bwrap-check": ("    if not (Path(a.bwrap).is_file() and os.access(a.bwrap, os.X_OK)):", "    if False and not (Path(a.bwrap).is_file() and os.access(a.bwrap, os.X_OK)):"),
    "M25-all-any": ("ok = all(legs)", "ok = any(legs)"),
    "M26-exit2-to-0": ("        sys.exit(2)", "        sys.exit(0)"),
}

manifest = {}
for name, (old, new) in MUTANTS.items():
    n = orig.count(old)
    if n != 1:
        sys.exit(f"{name}: anchor count {n} != 1 for {old!r}")
    text = orig.replace(old, new, 1)
    p = OUT / f"{name}.py"
    p.write_text(text)
    manifest[name] = {"anchor": old, "sha256": hashlib.sha256(text.encode()).hexdigest()}

import json
(S / "mutants.json").write_text(json.dumps(manifest, indent=1))
print(f"generated {len(manifest)} mutants + pristine (M00-orig)")
