#!/usr/bin/env python3
"""C2MutCounter (round 53 wave 1): mutation driver for plans/round53_c2_tipstate.py --selftest.

Each mutant is written into its own scratch directory under the scratch clone of the lane; the lane tree is never
written. The selftest runs there with an isolated TMPDIR. Killed iff the exit code or the `SELFTEST cases=` line differs
from the pristine baseline (a compile error or crash also counts as killed, and is recorded as such).
Predicted column = the hand prediction made before running: K killed, S survives, E equivalent, S-diag survives on
verdict but changes diagnostics only. The measured column is authoritative.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SCRATCH = Path("/fast/scratch/hyaku/kengaku-r53/C2MutCounter")
PRISTINE = Path(os.environ.get("C2_SOURCE") or str(SCRATCH / "lane" / "plans" / "round53_c2_tipstate.py"))
TAG = os.environ.get("C2_TAG", "")
SEAT = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2MutCounter")
RELPATH = "plans/round53_c2_tipstate.py"
TIMING = {}
CASES = re.compile(r"^SELFTEST cases=\d+ failures=\d+$", re.M)

M = [
    ("M00", "NL", "null: comment appended, no behaviour change", None, "\n# null mutant: appended comment\n", "S"),
    ("M01", "SL", "ledger absent: missing list emptied", 'res["missing"] = sorted(rows)', 'res["missing"] = []', "S"),
    ("M02", "SL", "argv length floor 2 -> 1", 'len(argv) < 2', 'len(argv) < 1', "S"),
    ("M03", "SL", "argv length floor 2 -> 3", 'len(argv) < 2', 'len(argv) < 3', "K"),
    ("M04", "SL", "argv all-str check disabled", 'all(isinstance(a, str) for a in argv)', 'True', "S"),
    ("M05", "SL", "script-None guard removed", 'script is None or script not in argv', 'script not in argv', "E"),
    ("M06", "SL", "entry-script membership inverted", 'script not in argv):', 'script in argv):', "K"),
    ("M07", "SL", "exit bool exclusion removed", 'or isinstance(ex, bool) or st not in', 'or st not in', "S"),
    ("M08", "SL", "state domain check removed", 'st not in ("green", "red") or ', '', "S"),
    ("M09", "SL", "state/exit consistency test removed", 'or (st == "green") != (ex == 0)', 'or False', "K"),
    ("M10", "SL", "state/exit consistency operator != -> ==", '(st == "green") != (ex == 0)', '(st == "green") == (ex == 0)', "K"),
    ("M11", "SL", "kind domain check removed", 'or sp.get("kind") not in ("entry", "selftest", "help")', 'or False', "S"),
    ("M12", "SL", "red-reason branch keyed on green", 'if st == "red":', 'if st == "green":', "K"),
    ("M13", "SL", "reason word floor < -> <=", 'len(reason.split()) < MIN_REASON_WORDS', 'len(reason.split()) <= MIN_REASON_WORDS', "S"),
    ("M14", "SL", "MIN_REASON_WORDS 10 -> 9", 'MIN_REASON_WORDS = 10', 'MIN_REASON_WORDS = 9', "S"),
    ("M15", "SL", "MIN_REASON_WORDS 10 -> 17", 'MIN_REASON_WORDS = 10', 'MIN_REASON_WORDS = 17', "K"),
    ("M16", "SL", "MIN_REASON_WORDS 10 -> 1", 'MIN_REASON_WORDS = 10', 'MIN_REASON_WORDS = 1', "K"),
    ("M17", "SL", "evidence floor 6 -> 5", 'len(ev.strip()) < 6', 'len(ev.strip()) < 5', "S"),
    ("M18", "SL", "evidence floor 6 -> 9", 'len(ev.strip()) < 6', 'len(ev.strip()) < 9', "K"),
    ("M19", "SL", "evidence strip() dropped", 'len(ev.strip()) < 6', 'len(ev) < 6', "S"),
    ("M20", "SL", "evidence str-type check removed", 'not isinstance(ev, str) or len(ev.strip())', 'len(ev.strip())', "S"),
    ("M21", "SL", "help limit <= -> <", 'help_ok = kinds["help"] <= MAX_HELP_FRACTION * max(1, n_reg)',
     'help_ok = kinds["help"] < MAX_HELP_FRACTION * max(1, n_reg)', "S"),
    ("M22", "SL", "MAX_HELP_FRACTION 0.10 -> 0.50", 'MAX_HELP_FRACTION = 0.10', 'MAX_HELP_FRACTION = 0.50', "S"),
    ("M23", "EV", "help count reads entry kind", 'help_ok = kinds["help"]', 'help_ok = kinds["entry"]', "K"),
    ("M24", "EV", "kind-count guard removed", 'if k in kinds:', 'if True:', "S"),
    ("M25", "EV", "static_ok: missing term removed", 'not (s["missing"] or s["extra"] or', 'not (s["extra"] or', "S"),
    ("M26", "EV", "static_ok: extra term removed", 's["extra"] or s["entry_mismatch"]', 's["entry_mismatch"]', "K"),
    ("M27", "EV", "static_ok: entry_mismatch term removed", 's["entry_mismatch"] or s["bad_decl"]', 's["bad_decl"]', "S"),
    ("M28", "EV", "static_ok: bad_decl term removed", 's["bad_decl"] or s["bad_reason"]', 's["bad_reason"]', "S"),
    ("M29", "EV", "static_ok: bad_reason term removed", 'or s["bad_reason"]', '', "K"),
    ("M30", "EV", "static_ok: dups term removed", 'or s["dups"] or s["ledger_err"]', 'or s["ledger_err"]', "S"),
    ("M31", "EV", "static_ok: ledger_err term removed", 'or s["dups"] or s["ledger_err"])', 'or s["dups"])', "S"),
    ("M32", "EV", "static_ok: help_ok and -> or", 'static_ok = help_ok and not (', 'static_ok = help_ok or not (', "K"),
    ("M33", "EV", "static_ok: help_ok dropped", 'static_ok = help_ok and not (', 'static_ok = not (', "K"),
    ("M34", "SL", "extra computed as intersection", 'res["extra"] = sorted(set(lr) - set(rows))',
     'res["extra"] = sorted(set(lr) & set(rows))', "K"),
    ("M35", "SL", "missing computed as intersection", 'res["missing"] = sorted(set(rows) - set(lr))',
     'res["missing"] = sorted(set(rows) & set(lr))', "K"),
    ("M36", "RV", "row entry cell index 2 -> 1", 'entry = cells[2] if len(cells) > 2 else ""',
     'entry = cells[1] if len(cells) > 2 else ""', "K"),
    ("M37", "RV", "entry regex loses corpus/grader prefixes", '(?:plans|corpus|grader)[A-Za-z0-9_./-]*',
     '(?:plans)[A-Za-z0-9_./-]*', "S"),
    ("M38", "RV", "duplicate names not recorded", 'dup.append(n)', 'pass', "S"),
    ("M39", "RV", "duplicate names: first-wins", 'rows[n] = line', 'rows.setdefault(n, line)', "S"),
    ("M40", "RV", "ledger schema check removed", 'd.get("schema") != SCHEMA', 'False', "S"),
    ("M41", "EV", "dry-run exit inverted", 'return (0 if static_ok else 1), lines', 'return (1 if static_ok else 0), lines', "S"),
    ("M42", "EV", "predicate fail exit 1 -> 2", 'return (0 if ok else 1), lines', 'return (0 if ok else 2), lines', "K"),
    ("M43", "EV", "help limit max(1,n_reg) -> n_reg", 'help_ok = kinds["help"] <= MAX_HELP_FRACTION * max(1, n_reg)',
     'help_ok = kinds["help"] <= MAX_HELP_FRACTION * n_reg', "E"),
    ("M44", "EV", "clean test rewritten as is-not-False", 'clean in (True, None)', 'clean is not False', "E"),
    ("M45", "EV", "clean test widened to admit dirty clone", 'clean in (True, None)', 'clean in (True, None, False)', "S"),
    ("M46", "EV", "executed == n_reg relaxed to >=", 'executed == n_reg and', 'executed >= n_reg and', "E"),
    ("M47", "EV", "executed == n_reg dropped", 'executed == n_reg and tmo', 'tmo', "E"),
    ("M48", "EV", "tmo == 0 dropped", 'tmo == 0 and mism', 'mism', "K"),
    ("M49", "EV", "mism == 0 dropped", 'mism == 0 and evmiss', 'evmiss', "K"),
    ("M50", "EV", "evmiss == 0 dropped", 'evmiss == 0 and clean', 'clean', "K"),
    ("M51", "EV", "only-is-None term dropped", 'and (only is None)))', '))', "S"),
    ("M52", "EV", "only-is-None inverted", 'and (only is None)))', 'and (only is not None)))', "K"),
    ("M53", "EV", "only filter disabled", 'if only:', 'if False:', "S"),
    ("M54", "EV", "entry_mismatch filter dropped from names", 'and n not in s["entry_mismatch"]', 'and True', "S-diag"),
    ("M55", "EV", "bad_decl filter dropped from names", 'and n not in s["bad_decl"]', 'and True', "K"),
    ("M56", "EV", "TIMEOUT branch disabled", 'if r["rc"] == "TIMEOUT":', 'if False:', "K"),
    ("M57", "EV", "timeout ignores per-row timeout_s", 't = int(spec.get("timeout_s") or default_timeout)',
     't = int(default_timeout)', "S"),
    ("M58", "EV", "evidence containment inverted", 'sp["evidence"] not in r["out"]', 'sp["evidence"] in r["out"]', "K"),
    ("M59", "EV", "evidence gate keyed on green", 'if sp["state"] == "red" and sp["evidence"]',
     'if sp["state"] == "green" and sp["evidence"]', "K"),
    ("M60", "EV", "rc mismatch test inverted", 'if rc != sp["exit"]:', 'if rc == sp["exit"]:', "K"),
    ("M61", "EV", "observed-green counter inverted", 'if rc == 0:', 'if rc != 0:', "S"),
    ("M62", "EV", "declared-green count reads red", '["state"] == "green")', '["state"] == "red")', "S"),
    ("M63", "EV", "executed counter not incremented", 'executed += 1', 'pass', "K"),
    ("M64", "SX", "selftest: want_out check removed", 'and all(w not in text for w in want_out)', '', "S"),
    ("M65", "SX", "selftest: want_in check removed", 'all(w in text for w in want_in)', 'True', "S"),
    ("M66", "SX", "selftest exit always 0", 'return 0 if not fails else 1', 'return 0', "S"),
    ("M67", "SX", "selftest cases line constant changed", 'print(f"SELFTEST cases=', 'print(f"SELFTEST cases=1', "K"),
    ("M68", "SX", "selftest: rc check made vacuous", 'ok = rc == want_rc and', 'ok = True and', "S"),
]


def run_selftest(tag: str, mutant_src: str):
    d = SCRATCH / "m" / tag
    if d.exists():
        shutil.rmtree(d)
    (d / "plans").mkdir(parents=True)
    f = d / RELPATH
    f.write_text(mutant_src)
    tmp = SCRATCH / "tmp" / tag
    tmp.mkdir(parents=True)
    import resource
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    t0 = time.time()
    try:
        compile(mutant_src, str(f), "exec")
        p = subprocess.run([sys.executable, RELPATH, "--selftest"], cwd=d, capture_output=True, text=True,
                           timeout=900, env={**os.environ, "TMPDIR": str(tmp)})
        rc, out, err = p.returncode, p.stdout, p.stderr
    except SyntaxError as e:
        rc, out, err = "SYNTAX", "", str(e)
    shutil.rmtree(tmp, ignore_errors=True)
    shutil.rmtree(d, ignore_errors=True)
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    TIMING[tag] = {"wall_s": round(time.time() - t0, 2), "child_user_s_delta_approx": round(r1.ru_utime - r0.ru_utime, 2)}
    cases = (CASES.findall(out) or [None])[-1]
    return rc, cases, out, err


def main() -> int:
    SEAT.mkdir(parents=True, exist_ok=True)
    (SEAT / f"mutants{TAG}").mkdir(exist_ok=True)
    src = PRISTINE.read_text()
    sha_before = subprocess.run(["sha256sum", str(PRISTINE)], capture_output=True, text=True).stdout.split()[0]

    base_rc, base_cases, base_out, base_err = run_selftest("baseline", src)
    print(f"BASELINE rc={base_rc} line={base_cases}")

    def one(row):
        mid, grp, desc, old, new, pred = row
        if old is None:
            mut = src + new
            n = None
        else:
            n = src.count(old)
            if n < 1:
                return {"id": mid, "group": grp, "desc": desc, "predicted": pred,
                        "error": f"old string occurs {n} times, expected 1"}
            mut = src.replace(old, new, 1)
        rc, cases, out, err = run_selftest(mid, mut)
        killed = (rc != base_rc) or (cases != base_cases)
        verdict = "KILLED" if killed else "SURVIVED"
        (SEAT / f"mutants{TAG}" / f"{mid}.txt").write_text(f"rc={rc}\nline={cases}\n--- stdout\n{out}--- stderr\n{err}")
        return {"id": mid, "group": grp, "desc": desc, "predicted": pred, "rc": rc, "cases": cases,
                "verdict": verdict, "wall_s": TIMING.get(mid, {}).get("wall_s"), "stdout_identical_to_baseline": out == base_out,
                "crash": bool(err.strip()) and rc != base_rc,
                "crash_tail": (err.strip().splitlines() or [""])[-1][:160]}

    with ThreadPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(one, M))

    sha_after = subprocess.run(["sha256sum", str(PRISTINE)], capture_output=True, text=True).stdout.split()[0]
    restored_rc, restored_cases, _, _ = run_selftest("restored", PRISTINE.read_text())
    result = {"baseline": {"rc": base_rc, "cases": base_cases}, "restored": {"rc": restored_rc, "cases": restored_cases},
              "pristine_sha256_before": sha_before, "pristine_sha256_after": sha_after,
              "pristine_unchanged": sha_before == sha_after, "mutants": rows}
    result["timing"] = TIMING
    (SEAT / f"mutation-results{TAG}.json").write_text(json.dumps(result, indent=2) + "\n")
    killed = sum(1 for r in rows if r.get("verdict") == "KILLED")
    surv = sum(1 for r in rows if r.get("verdict") == "SURVIVED")
    err = sum(1 for r in rows if "error" in r)
    print(f"MUTANTS total={len(rows)} killed={killed} survived={surv} driver_errors={err}")
    print(f"RESTORED rc={restored_rc} line={restored_cases} pristine_unchanged={sha_before == sha_after}")
    for r in rows:
        if "error" in r:
            print(f"{r['id']} ERROR {r['error']}")
        else:
            print(f"{r['id']} {r['group']} pred={r['predicted']} {r['verdict']} rc={r['rc']} line={r['cases']} :: {r['desc']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
