#!/usr/bin/env python3
"""Round-96 C1 mutation seat: additional single-point mutants (M27..M41).

Each mutant = pristine T bytes with exactly ONE substring replaced (asserted count==1).
Pristine sha256 asserted against the frozen-instruments table.
"""
import hashlib
import json
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

MUTANTS = {
    "M27-L2-drop-testsh": ('          and receipt["fields"].get("TEST_SH_SHA") == TEST_SH_SHA)',
                           '          and True)'),
    "M28-L2-drop-subjectsha": ('          and receipt["fields"].get("SUBJECT_SHA") == SUBJECT_SHA\n',
                               '          and True\n'),
    "M29-L5-pred-only": ('        elif obs != pred or pred != predicted[cid]:',
                         '        elif obs != pred:'),
    "M30-L7-drop-receiptfield": ('    legacy_ok = (member.get("receipt") == RECEIPT and member.get("subject") == "tb2-header"',
                                 '    legacy_ok = (member.get("subject") == "tb2-header"'),
    "M31-L7-drop-verdict": ('                 and member.get("verdict") == "cases")',
                            '                 and True)'),
    "M32-L9-drop-tablesha": ('f.get("TOOL_SHA") == sha(tool_bytes) and f.get("CASE_TABLE_SHA") == sha(table_bytes)',
                             'f.get("TOOL_SHA") == sha(tool_bytes) and True'),
    "M33-L6-drop-obseq": ('l6 = rerun.returncode == 0 and bool(receipt["obs"]) and rerun_obs == receipt["obs"] and stamps_equal',
                          'l6 = rerun.returncode == 0 and bool(receipt["obs"]) and True and stamps_equal'),
    "M34-L6-drop-rc": ('l6 = rerun.returncode == 0 and', 'l6 = True and'),
    "M35-L3-drop-booltip": ('l3 = bool(tip) and git(lane,', 'l3 = git(lane,'),
    "M36-L7-round-ge": ('member.get("round") == 96', 'member.get("round") >= 96'),
    "M37-L7-classes-superset": ('member.get("classes") == MEMBER_CLASSES',
                                'set(MEMBER_CLASSES) <= set(member.get("classes") or [])'),
    "M38-L6-stamps-drop-envside": ('RERUN_STAMPS = ("TOOL_SHA", "CASE_TABLE_SHA", "ENV_SIDE", "GRADER_SIDE")',
                                   'RERUN_STAMPS = ("TOOL_SHA", "CASE_TABLE_SHA", "GRADER_SIDE")'),
    "M39-parse-observed-fallback": ('parts.get("observed", "?")', 'parts.get("predicted", "?")'),
    "M40-L5-drop-len": (' and len(receipt["cases"]) == len(predicted)', ''),
    "M41-rerun-rc2-mapping": ('        if rerun.returncode == 2:', '        if rerun.returncode == 3:'),
    "M42-L2-drop-solvesha": ('          and receipt["fields"].get("SOLVE_SHA") == SOLVE_SHA\n',
                             '          and True\n'),
}

manifest = json.loads((S / "mutants.json").read_text())
for name, (old, new) in MUTANTS.items():
    n = orig.count(old)
    if n != 1:
        sys.exit(f"{name}: anchor count {n} != 1 for {old!r}")
    text = orig.replace(old, new, 1)
    p = OUT / f"{name}.py"
    p.write_text(text)
    manifest[name] = {"anchor": old, "sha256": hashlib.sha256(text.encode()).hexdigest()}

(S / "mutants.json").write_text(json.dumps(manifest, indent=1))
print(f"wrote {len(MUTANTS)} new mutants; manifest now {len(manifest)} entries")
