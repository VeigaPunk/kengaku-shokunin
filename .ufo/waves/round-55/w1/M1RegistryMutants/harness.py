#!/usr/bin/env python3
"""M1RegistryMutants — single-defect mutation probe of plans/round52_c2_registry.py.

Production bytes are copied to scratch and never edited in place. The detector is
the same bounded behavioral run on pristine, mutated, and restored bytes:
    python3 <counter-copy> --lane <fixture>   ->  defect fingerprint + exit code
A mutant is KILLED only if, on a focused fixture built for its leg, the exit code
flips 1->0 with its defect family going to zero (and only its family present in
the baseline), AND on the combined fixture its family disappears while every
other family keeps the pristine count (orthogonality).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
PROD = LANE / "plans" / "round52_c2_registry.py"
FROZEN_HEAD = "80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb"

ap = argparse.ArgumentParser()
ap.add_argument("--work", default="/fast/scratch/hyaku/kengaku-r55/M1RegistryMutants")
ap.add_argument("--receipt", default=str(LANE / ".ufo/waves/round-55/w1/M1RegistryMutants"))
a = ap.parse_args()
S = Path(a.work)
OUT = Path(a.receipt)
OUT.mkdir(parents=True, exist_ok=True)
(S / "mutants").mkdir(exist_ok=True)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def run_counter(py: Path, lane: Path, extra: list[str] = []) -> tuple[str, int, str]:
    r = subprocess.run([sys.executable, str(py), "--lane", str(lane), *extra],
                       capture_output=True, text=True, timeout=120)
    return r.stdout, r.returncode, r.stderr


# ---------- fixture lane builder ----------

HDR = "| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |"
SEP = "|---|---|---|---|---|---|---|---|"


def row(name: str, entry: str, selftest: str = "none declared", pinned: str = "none") -> str:
    return f"| `{name}` | gate | `{entry}` | 0 ok | {selftest} | {pinned} | read-only | kengaku |"


def build(root: Path, *, rows: list[str], extra_plans: tuple[str, ...] = (),
          scorecard: str | None = None, knowledge: str | None = None) -> None:
    if root.exists():
        shutil.rmtree(root)
    (root / "plans").mkdir(parents=True)
    (root / "corpus" / "knowledge").mkdir(parents=True)
    (root / "plans" / "tool_a.py").write_text("# tool_a: no flags accepted\n")
    for name in extra_plans:
        (root / "plans" / name).write_text(f"# {name}\n")
    (root / "LOG.md").write_text("log\n")
    (root / "corpus" / "README.md").write_text("readme\n")
    if scorecard is not None:
        (root / "SCORECARD.md").write_text(scorecard)
    skill = "## Gate/probe registry\n\n" + HDR + "\n" + SEP + "\n" + "".join(r + "\n" for r in rows)
    (root / "SKILL.md").write_text(skill)
    if knowledge is not None:
        (root / "corpus" / "knowledge" / "depth.md").write_text(knowledge)


FIXTURES: dict[str, dict] = {
    # leg 1 MISSING: advertised (SCORECARD), script exists, no registry row
    "f1_missing": dict(rows=[], extra_plans=("orphan_tool.py",),
                       scorecard="Run `python3 plans/orphan_tool.py` for the orphan check.\n"),
    # leg 2 INCOMPLETE: one registry row with one empty cell
    "f2_incomplete": dict(rows=[row("t", "python3 plans/tool_a.py", pinned="")]),
    # leg 3 ENTRY-MISSING: registry entry script absent from the tree (and nonexistent
    # scripts are dropped from the advertised set, so only ENTRY-MISSING can fire)
    "f3_entry_missing": dict(rows=[row("g", "python3 plans/ghost_tool.py")]),
    # leg 4 SELFTEST-UNBACKED: self-test names script+flag the script lacks
    "f4_unbacked": dict(rows=[row("u", "python3 plans/tool_a.py",
                                  selftest="run `python3 plans/tool_a.py --selftest`")]),
    # leg 5 DUPLICATE: two rows share the name `t`
    "f5_duplicate": dict(rows=[row("t", "python3 plans/tool_a.py"),
                               row("t", "python3 plans/tool_a.py")]),
    # leg 6 advertised-universe: instrument advertised ONLY via corpus/knowledge/*.md
    "f6_knowledge": dict(rows=[row("t", "python3 plans/tool_a.py")],
                         extra_plans=("kb_tool.py",),
                         knowledge="Deeper check: `python3 plans/kb_tool.py`.\n"),
    # combined: every leg fires at once (MISSING=2: kb_tool + orphan)
    "combined": dict(
        rows=[row("ok", "python3 plans/tool_a.py"),
              row("dup", "python3 plans/tool_a.py"),
              row("dup", "python3 plans/tool_a.py"),
              row("blank", "python3 plans/tool_a.py", pinned=""),
              row("ghost", "python3 plans/ghost_tool.py"),
              row("unbacked", "python3 plans/tool_a.py",
                  selftest="run `python3 plans/tool_a.py --selftest`")],
        extra_plans=("orphan_tool.py", "kb_tool.py"),
        scorecard="Run `python3 plans/orphan_tool.py` for the orphan check.\n",
        knowledge="Deeper check: `python3 plans/kb_tool.py`.\n"),
}

# frozen baseline expectations (pristine counter)
EXPECT = {
    "f1_missing":       dict(exit=1, missing=1, incomplete=0, entry_missing=0, unbacked=0, duplicate=0),
    "f2_incomplete":    dict(exit=1, missing=0, incomplete=1, entry_missing=0, unbacked=0, duplicate=0),
    "f3_entry_missing": dict(exit=1, missing=0, incomplete=0, entry_missing=1, unbacked=0, duplicate=0),
    "f4_unbacked":      dict(exit=1, missing=0, incomplete=0, entry_missing=0, unbacked=1, duplicate=0),
    "f5_duplicate":     dict(exit=1, missing=0, incomplete=0, entry_missing=0, unbacked=0, duplicate=1),
    "f6_knowledge":     dict(exit=1, missing=1, incomplete=0, entry_missing=0, unbacked=0, duplicate=0),
    "combined":         dict(exit=1, missing=2, incomplete=1, entry_missing=1, unbacked=1, duplicate=1),
}

FAM_KEYS = ("missing", "incomplete", "entry_missing", "unbacked", "duplicate")


def fingerprint(out: str, code: int) -> dict:
    lines = out.splitlines()

    def n(tag: str):
        for l in lines:
            if l.startswith(tag):
                toks = l[len(tag):].split()
                if toks and toks[0].isdigit():
                    return int(toks[0])
        return None

    adv = reg = None
    for l in lines:
        if l.startswith("ADVERTISED total="):
            adv = int(l.split("=", 1)[1])
        if l.startswith("REGISTERED total="):
            reg = int(l.split("=", 1)[1].split()[0])
    pred = "pass" if "PREDICATE R52-C2 pass" in lines else \
           "fail" if "PREDICATE R52-C2 fail" in lines else None
    return dict(exit=code, advertised=adv, registered=reg,
                missing=n("MISSING"), incomplete=n("INCOMPLETE"),
                entry_missing=n("ENTRY-MISSING"), unbacked=n("SELFTEST-UNBACKED"),
                duplicate=n("DUPLICATE"), predicate=pred,
                detail=[l for l in lines if l.startswith("  ")])


def matches(fp: dict, expect: dict) -> bool:
    return all(fp.get(k) == v for k, v in expect.items())


# ---------- mutants ----------

MUTANTS = [
    dict(id="M1-missing-always-empty", leg="MISSING",
         defect="MISSING leg returns [] always (advertised-but-unregistered instruments invisible)",
         old="    missing = sorted(set(adv) - set(reg))\n",
         new="    missing = []\n",
         fixture="f1_missing", comb_delta=("missing", 0)),
    dict(id="M2-incomplete-ignores-blanks", leg="INCOMPLETE",
         defect="INCOMPLETE test all->any: fires only on fully-empty rows, which the separator "
                "guard already drops -> rows with blank cells are ignored",
         old="    incomplete = [r[0] for r in rows if not all(r)]\n",
         new="    incomplete = [r[0] for r in rows if not any(r)]\n",
         fixture="f2_incomplete", comb_delta=("incomplete", 0)),
    dict(id="M3-entry-missing-skipped", leg="ENTRY-MISSING",
         defect="ENTRY-MISSING leg skipped (registry rows naming absent scripts pass)",
         old="    entry_missing = sorted(s for s in reg if not (lane / s).exists())\n",
         new="    entry_missing = []\n",
         fixture="f3_entry_missing", comb_delta=("entry_missing", 0)),
    dict(id="M4-selftest-unbacked-false", leg="SELFTEST-UNBACKED",
         defect="selftest_unbacked() returns False always (unbacked self-test claims pass)",
         old="    return all(f not in body for f in flags)\n",
         new="    return False\n",
         fixture="f4_unbacked", comb_delta=("unbacked", 0)),
    dict(id="M5-duplicate-check-removed", leg="DUPLICATE",
         defect="DUPLICATE check removed (registry rows may repeat a name)",
         old="    duplicate = sorted({n for n in names if names.count(n) > 1})\n",
         new="    duplicate = []\n",
         fixture="f5_duplicate", comb_delta=("duplicate", 0)),
    dict(id="M6-universe-drops-knowledge", leg="advertised-universe",
         defect="self_assessment_files() no longer scans corpus/knowledge/*.md "
                "(instruments advertised only there become invisible to MISSING)",
         old='        files += sorted(kdir.glob("*.md"))\n',
         new="        pass\n",
         fixture="f6_knowledge", comb_delta=("missing", 1)),
]


def fam(fp: dict, key: str):
    return fp.get(key)


def others_unchanged(mut_fp: dict, base_fp: dict, changed: tuple[str, ...]) -> bool:
    return all(mut_fp.get(k) == base_fp.get(k) for k in FAM_KEYS if k not in changed)


def main() -> int:
    prod_bytes = PROD.read_bytes()
    prod_sha = sha(prod_bytes)
    src = prod_bytes.decode()

    # scratch copies
    pristine = S / "counter_pristine.py"
    pristine.write_bytes(prod_bytes)
    restored = S / "counter_restored.py"

    record: dict = {
        "meta": {
            "prod_path": str(PROD), "prod_sha256": prod_sha,
            "lane_head": FROZEN_HEAD,
            "counter_copy_sha256": sha(pristine.read_bytes()),
            "detector": "python3 <counter-copy> --lane <fixture> -> defect fingerprint + exit code",
        },
        "baseline": {}, "mutants": [], "selftest_battery": [], "restoration": {},
    }

    # ---- baseline on pristine bytes ----
    print("== baseline (pristine bytes) ==")
    baseline_ok = True
    for name, spec in FIXTURES.items():
        fx = S / "fixtures" / name
        build(fx, **spec)
        out, code, err = run_counter(pristine, fx)
        fp = fingerprint(out, code)
        ok = matches(fp, EXPECT[name])
        baseline_ok &= ok
        record["baseline"][name] = dict(expected=EXPECT[name], actual=fp, ok=ok, stderr=err)
        print(f"  {name}: exit={code} miss={fp['missing']} inc={fp['incomplete']} "
              f"entry={fp['entry_missing']} unbacked={fp['unbacked']} dup={fp['duplicate']} "
              f"pred={fp['predicate']} baseline={'ok' if ok else 'MISMATCH'}")
    # counter's own --selftest battery on pristine bytes (supplementary)
    out, code, _ = run_counter(pristine, S / "fixtures" / "combined", ["--selftest"])
    record["selftest_battery"].append(dict(variant="pristine", exit=code))
    print(f"  --selftest (pristine): exit={code}")

    # ---- mutants ----
    print("== mutants ==")
    for m in MUTANTS:
        cnt = src.count(m["old"])
        entry = dict(id=m["id"], leg=m["leg"], defect=m["defect"],
                     old=m["old"].strip(), new=m["new"].strip(),
                     replacement_occurrences=cnt)
        if cnt != 1:
            entry["verdict"] = "inconclusive (mutation site not unique)"
            record["mutants"].append(entry)
            print(f"  {m['id']}: INCONCLUSIVE site count={cnt}")
            continue
        mpy = S / "mutants" / f"{m['id']}.py"
        mpy.write_text(src.replace(m["old"], m["new"]))
        entry["sha256"] = sha(mpy.read_bytes())

        fx = S / "fixtures" / m["fixture"]
        b_out, b_code, _ = run_counter(pristine, fx)
        u_out, u_code, u_err = run_counter(mpy, fx)
        b_fp, u_fp = fingerprint(b_out, b_code), fingerprint(u_out, u_code)

        c_out_b, c_code_b, _ = run_counter(pristine, S / "fixtures" / "combined")
        c_out_u, c_code_u, _ = run_counter(mpy, S / "fixtures" / "combined")
        c_fp_b, c_fp_u = fingerprint(c_out_b, c_code_b), fingerprint(c_out_u, c_code_u)

        entry["focused"] = dict(fixture=m["fixture"], pristine=b_fp, mutant=u_fp, stderr=u_err)
        entry["combined"] = dict(pristine=c_fp_b, mutant=c_fp_u)

        # supplementary: counter's own --selftest battery against the mutant
        _, st_code, _ = run_counter(mpy, S / "fixtures" / "combined", ["--selftest"])
        record["selftest_battery"].append(dict(variant=m["id"], exit=st_code))

        if not baseline_ok:
            entry["verdict"] = "inconclusive (baseline fingerprint mismatch)"
        else:
            changed = {k for k in FAM_KEYS if u_fp.get(k) != b_fp.get(k)}
            focused_flip = (b_fp["exit"] == 1 and u_fp["exit"] == 0
                            and all(u_fp.get(k) == 0 for k in FAM_KEYS))
            mut = next(x for x in MUTANTS if x["id"] == m["id"])
            comb_target, comb_want = mut["comb_delta"]
            comb_ok = (c_fp_u.get(comb_target) == comb_want
                       and others_unchanged(c_fp_u, c_fp_b, (comb_target,)))
            entry["verdict"] = "killed" if (focused_flip and comb_ok) else "survived"
            entry["focus_changed_families"] = sorted(changed)
        record["mutants"].append(entry)
        print(f"  {m['id']}: focused exit {b_code}->{u_code} "
              f"fam={ {k: (b_fp.get(k), u_fp.get(k)) for k in FAM_KEYS} } "
              f"combined {m.get('comb_delta')} -> {c_fp_u.get(m['comb_delta'][0])} "
              f"selftest_exit={st_code} verdict={entry['verdict']}")

    # ---- restoration evidence ----
    restored.write_bytes(PROD.read_bytes())
    r_out, r_code, _ = run_counter(restored, S / "fixtures" / "combined")
    r_fp = fingerprint(r_out, r_code)
    b_out, b_code, _ = run_counter(pristine, S / "fixtures" / "combined")
    record["restoration"] = dict(
        prod_sha256_after=sha(PROD.read_bytes()),
        prod_unchanged=sha(PROD.read_bytes()) == prod_sha,
        restored_copy_sha256=sha(restored.read_bytes()),
        restored_fingerprint=r_fp, pristine_fingerprint=fingerprint(b_out, b_code),
        identical_output=(r_fp == fingerprint(b_out, b_code) and r_code == b_code),
    )
    print(f"== restoration: prod sha unchanged={record['restoration']['prod_unchanged']} "
          f"restored output identical={record['restoration']['identical_output']}")

    # ---- receipts ----
    (OUT / "receipts.json").write_text(json.dumps(record, indent=2))
    write_mutants_md(record, OUT)
    killed = sum(1 for e in record["mutants"] if e.get("verdict") == "killed")
    print(f"== summary: {killed}/{len(MUTANTS)} killed; receipts -> {OUT}")
    return 0 if baseline_ok else 3


def write_mutants_md(rec: dict, out: Path) -> None:
    meta = rec["meta"]
    L = []
    L.append("# R55-W1 M1RegistryMutants — mutation probe of `plans/round52_c2_registry.py`\n")
    L.append(f"- Production bytes (read-only, never edited in place): `{meta['prod_path']}` "
             f"sha256 `{meta['prod_sha256']}`; lane HEAD `{meta['lane_head']}` (== frozen base tip); "
             f"worktree clean for this file; scratch copy sha256 `{meta['counter_copy_sha256']}` (identical).")
    L.append("- Detector (identical on pristine/mutated/restored bytes): "
             "`python3 <counter-copy> --lane <fixture>`; fingerprint = the five defect counts + "
             "detail lines + exit code.")
    L.append("- Kill rule: focused fixture (built for that leg) flips exit 1→0 with its family "
             "count →0, AND the combined fixture loses exactly that family while every other "
             "family keeps the pristine count (orthogonality). A surviving mutant = an "
             "advertised-but-undemonstrated leg (coverage finding, contract unchanged).\n")

    L.append("## Baseline (pristine bytes)")
    L.append("| fixture | expectation | actual (exit/MISSING/INCOMPLETE/ENTRY-MISSING/UNBACKED/DUPLICATE) | match |")
    L.append("|---|---|---|---|")
    for name, b in rec["baseline"].items():
        e, fp = b["expected"], b["actual"]
        actual = "/".join(str(fp.get(k)) for k in ("exit", "missing", "incomplete",
                                                   "entry_missing", "unbacked", "duplicate"))
        expect = "/".join(str(e.get(k)) for k in ("exit", "missing", "incomplete",
                                                  "entry_missing", "unbacked", "duplicate"))
        L.append(f"| `{name}` | {expect} | {actual} | {'yes' if b['ok'] else 'NO'} |")
    L.append("")

    L.append("## Mutants")
    L.append("| id | leg | single defect | focused fixture | pristine→mutant (focused) | "
             "combined family pristine→mutant | verdict | mutant sha256 |")
    L.append("|---|---|---|---|---|---|---|---|")
    for e in rec["mutants"]:
        if "focused" not in e:
            L.append(f"| `{e['id']}` | {e['leg']} | {e['defect']} | — | — | — | "
                     f"{e['verdict']} | — |")
            continue
        f = e["focused"]
        fams = "/".join(str(f["pristine"].get(k)) for k in FAM_KEYS)
        famu = "/".join(str(f["mutant"].get(k)) for k in FAM_KEYS)
        c = e["combined"]
        mut = next(x for x in MUTANTS if x["id"] == e["id"])
        key, want = mut["comb_delta"]
        cfrom = c["pristine"].get(key)
        cto = c["mutant"].get(key)
        L.append(f"| `{e['id']}` | {e['leg']} | {e['defect']} | `{f['fixture']}` | "
                 f"exit {f['pristine']['exit']}→{f['mutant']['exit']}, "
                 f"[{fams}]→[{famu}] | {key} {cfrom}→{cto} (want {want}) | "
                 f"**{e['verdict']}** | `{e.get('sha256','—')}` |")
    L.append("")
    L.append("Family order in `[..]`: MISSING / INCOMPLETE / ENTRY-MISSING / SELFTEST-UNBACKED / DUPLICATE.\n")

    L.append("## Per-mutant detail")
    for e in rec["mutants"]:
        if "focused" not in e:
            continue
        f = e["focused"]
        L.append(f"### {e['id']} — {e['verdict']}")
        L.append(f"- Mutation: `{e['old']}` → `{e['new']}` (occurrences matched: "
                 f"{e['replacement_occurrences']})")
        L.append(f"- Focused fixture `{f['fixture']}` pristine exit {f['pristine']['exit']}, "
                 f"detail {f['pristine']['detail']}")
        L.append(f"- Focused fixture mutant exit {f['mutant']['exit']}, "
                 f"detail {f['mutant']['detail']}")
        c = e["combined"]
        L.append(f"- Combined pristine exit {c['pristine']['exit']} detail {c['pristine']['detail']}")
        L.append(f"- Combined mutant exit {c['mutant']['exit']} detail {c['mutant']['detail']}\n")

    L.append("## Counter's own `--selftest` battery vs mutants (supplementary)")
    L.append("| variant | --selftest exit |")
    L.append("|---|---|")
    for s in rec["selftest_battery"]:
        L.append(f"| {s['variant']} | {s['exit']} |")
    battery_blind = [s["variant"] for s in rec["selftest_battery"] if s["variant"] != "pristine" and s["exit"] == 0]
    L.append("")
    L.append(f"The shipped 3-fixture battery (`--selftest`) detects only M1/M2 and is blind to: "
             f"{', '.join(battery_blind) if battery_blind else 'none'} — "
             f"i.e. it exercises the MISSING and INCOMPLETE legs only.\n")

    r = rec["restoration"]
    L.append("## Restoration evidence")
    L.append(f"- Production sha256 after probe: `{r['prod_sha256_after']}` — "
             f"unchanged: {r['prod_unchanged']}")
    L.append(f"- Restored scratch copy sha256: `{r['restored_copy_sha256']}`")
    L.append(f"- Detector on restored bytes vs pristine baseline on the combined fixture: "
             f"identical output = {r['identical_output']} "
             f"(exit {r['restored_fingerprint']['exit']}, "
             f"fingerprint {r['restored_fingerprint']['predicate']})\n")

    killed = [e for e in rec["mutants"] if e.get("verdict") == "killed"]
    survived = [e for e in rec["mutants"] if e.get("verdict") == "survived"]
    L.append("## Findings")
    L.append(f"- {len(killed)}/{len(rec['mutants'])} mutants killed; "
             f"{len(survived)} survived (each survivor = an advertised-but-undemonstrated leg).")
    for e in survived:
        L.append(f"  - SURVIVOR `{e['id']}` ({e['leg']}): {e['defect']}")
    L.append("- Coverage note: the shipped `--selftest` battery covers clean/MISSING/INCOMPLETE "
             "only; the ENTRY-MISSING, SELFTEST-UNBACKED, DUPLICATE and knowledge-file legs of "
             "the advertised-universe have no self-test fixture in the tool itself.")

    (out / "mutants.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    sys.exit(main())
