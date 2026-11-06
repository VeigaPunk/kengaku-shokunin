#!/usr/bin/env python3
"""MutTesterC1 (round 95) byte-level mutant generator for plans/round95_c1_replay.py.

Usage: gen_mutants.py <pristine counter> <out dir>
Each mutant is one or more exact (old -> new) substitutions; every `old` must occur exactly once
in the pristine bytes, otherwise generation aborts. Writes <out>/<id>.py and <out>/MUTANTS.tsv
(id, after-sha256, applied-substitution count, description).
"""
import hashlib
import pathlib
import sys

MUTANTS = [
    # --- round-94 survivors re-applied to the round-95 counter (analogues) ---
    ("m01", "L7 member-set check dropped (set_ok = True)",
     [('set_ok = bool(base_set) and MEMBER not in base_set and rev_set == base_set | {MEMBER}', 'set_ok = True')]),
    ("m02", "L7 BASE-ledger-absent fail-open (set_ok = not base_bytes or ...)",
     [('set_ok = bool(base_set) and', 'set_ok = not base_bytes or')]),
    ("m03", "L5 both coverage clauses dropped (seen-set and count)",
     [('and seen == set(predicted) and len(receipt["cases"]) == len(predicted)', '')]),
    ("m03a", "L5 seen-set clause dropped (count kept)",
     [('and seen == set(predicted) and len(receipt["cases"]) == len(predicted)',
       'and len(receipt["cases"]) == len(predicted)')]),
    ("m03b", "L5 count clause dropped (seen-set kept)",
     [('and seen == set(predicted) and len(receipt["cases"]) == len(predicted)', 'and seen == set(predicted)')]),
    ("m04", "L6 compares observation COUNTS not lines",
     [('rerun_obs == receipt["obs"] and stamps_equal', 'len(rerun_obs) == len(receipt["obs"]) and stamps_equal')]),
    ("m05", "L4 frozen table read at --rev, not at the adding commit",
     [('text = blob(root, added[0], CLAIMS)', 'text = blob(root, rev, CLAIMS)')]),
    ("m06", "L9 stamps skipped (l9 = True or ...)",
     [('l9 = (f.get("TOOL_SHA")', 'l9 = True or (f.get("TOOL_SHA")')]),
    ("m07", "L2 checks only the grader pin",
     [('for p, want in PINS.items())', 'for p, want in PINS.items() if p == "tests/test_outputs.py")')]),
    ("m08", "sandbox branch could-not-evaluate/rc2 -> fail/rc1",
     [('        print("PREDICATE R95-C1 could-not-evaluate")\n        return 2\n    tool_at_rev',
       '        print("PREDICATE R95-C1 fail")\n        return 1\n    tool_at_rev')]),
    ("m09", "L1 receipt-absent accepted (l1 = True)",
     [('l1 = receipt_bytes is not None', 'l1 = True')]),
    ("m10", "L3 ancestor check dropped",
     [(' and git(lane, "merge-base", "--is-ancestor", tip, rev).returncode == 0', '')]),
    ("m11", "L8 probe-sha pin dropped",
     [('l8 = bool(frozen.get(TOOL)) and sha(tool_bytes) == frozen.get(TOOL)', 'l8 = bool(frozen.get(TOOL))')]),
    ("m12", "exit-code collapse (return 0 always)",
     [('return 0 if ok else 1', 'return 0')]),
    ("m13", "__main__ could-not-evaluate handler -> fail/rc1",
     [('        print("PREDICATE R95-C1 could-not-evaluate")\n        sys.exit(2)',
       '        print("PREDICATE R95-C1 fail")\n        sys.exit(1)')]),
    ("m03+m04", "interaction: m03 and m04 together",
     [('and seen == set(predicted) and len(receipt["cases"]) == len(predicted)', ''),
      ('rerun_obs == receipt["obs"] and stamps_equal', 'len(rerun_obs) == len(receipt["obs"]) and stamps_equal')]),
    # --- new mutants on this round's additions and remaining legs ---
    ("n01", "L6 stamps_equal dropped",
     [('rerun_obs == receipt["obs"] and stamps_equal', 'rerun_obs == receipt["obs"]')]),
    ("n02", "L7 legacy_ok dropped (receipt/subject/verdict fields unchecked)",
     [('and set_ok and legacy_ok)', 'and set_ok)')]),
    ("n03", "L2 UPSTREAM_BOTTLE_SHA receipt pin dropped",
     [('\n          and receipt["fields"].get("UPSTREAM_BOTTLE_SHA") == UPSTREAM_SHA)', ')')]),
    ("n04", "--work-inside-lane guard dropped",
     [('if work == lane or lane in work.parents:', 'if False:')]),
    ("n05", "L5 frozen-vector comparison dropped (obs != pred only)",
     [('elif obs != pred or pred != predicted[cid]:', 'elif obs != pred:')]),
    ("n06", "L7 member classes check dropped",
     [('and member.get("classes") == MEMBER_CLASSES and exec_total', 'and exec_total')]),
    ("n07", "L7 executed total and class cells dropped",
     [('and exec_total == EXECUTED_AFTER and cells == AFTER_CELLS', '')]),
    ("n08", "L3 merge-base arguments reversed",
     [('"merge-base", "--is-ancestor", tip, rev)', '"merge-base", "--is-ancestor", rev, tip)')]),
    ("n09", "L4 table pin dropped (l4 = frozen row present only)",
     [('l4 = bool(frozen.get(TABLE)) and sha(table_bytes) == frozen.get(TABLE)', 'l4 = bool(frozen.get(TABLE))')]),
    ("n10", "L9 HOST_SED stamp dropped",
     [('\n          and f.get("HOST_SED") == host_tool(["/usr/bin/sed", "--version"]))', ')')]),
    ("n11", "L9 HOST_BASH stamp dropped",
     [('\n          and f.get("HOST_BASH") == host_tool(["/usr/bin/bash", "--version"])', '')]),
    ("n12", "L9 HOST_PYTHON stamp dropped",
     [('\n          and f.get("HOST_PYTHON") == host_tool(["/usr/bin/python3", "-V"])', '')]),
    ("n13", "rerun ignores injected sandbox (--bwrap not passed to probe rerun)",
     [('"--work", str(work / "rerun"), "--bwrap", a.bwrap],', '"--work", str(work / "rerun")],')]),
    ("n14", "parse_receipt drops CASE lines (cases always empty)",
     [('if line.startswith("CASE "):', 'if False:')]),
    ("n15", "L6 probe rerun return-code check dropped",
     [('l6 = rerun.returncode == 0 and bool(receipt["obs"])', 'l6 = bool(receipt["obs"])')]),
    ("n16", "L6 receipt-stamp presence check dropped (equality only)",
     [('stamps_equal = all(bool(receipt["fields"].get(k)) and rerun_parsed', 'stamps_equal = all(rerun_parsed')]),
]


def main() -> int:
    src = pathlib.Path(sys.argv[1]).read_bytes().decode()
    out = pathlib.Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    rows = [f"pristine\t{hashlib.sha256(src.encode()).hexdigest()}\t0\tpristine counter"]
    for mid, desc, subs in MUTANTS:
        text = src
        for old, new in subs:
            n = text.count(old)
            if n != 1:
                raise SystemExit(f"{mid}: anchor occurs {n} times: {old!r}")
            text = text.replace(old, new)
        if text == src:
            raise SystemExit(f"{mid}: no change")
        dst = out / f"{mid}.py"
        dst.write_text(text)
        rows.append(f"{mid}\t{hashlib.sha256(text.encode()).hexdigest()}\t{len(subs)}\t{desc}")
    (out / "MUTANTS.tsv").write_text("\n".join(rows) + "\n")
    print("\n".join(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
