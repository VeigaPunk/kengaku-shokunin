#!/usr/bin/env python3
"""C1MutClassifier: merge every pass into one kill matrix and write the deliverables.

Inputs (all produced by this seat, under scratch):
  results.json         class-level matrix (D1 selftest, D2 adv cases, D3 population)
  attribution.json     reason-level diffs (R1 selftest, R2 adv, R3 population)
  counter-oracle.json  the counter's own ORACLE leg per mutant
  reachability.json    line-hit counts of each mutated site
  join-pairs.json      the join() lattice pairs actually used
  witnesses.json / fuzz-witnesses.json / witnesses2.json   witness cases
  counter-mutants.json / f1-probe.json                     counter-side probes

Outputs:
  kill-matrix.md       the matrix as markdown
  kill-matrix.json     the matrix as JSON
  survivors.md         every survivor with the case that should have killed it

usage: matrix.py
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

RES = json.loads((HERE / "results.json").read_text())
ATTR = {r["mutant"]: r for r in json.loads((HERE / "attribution.json").read_text())}
COR = {r["mutant"]: r for r in json.loads((HERE / "counter-oracle.json").read_text())}
REACH = json.loads((HERE / "reachability.json").read_text())
WIT = {}
for f in ("witnesses.json", "fuzz-witnesses.json", "witnesses2.json"):
    d = json.loads((HERE / f).read_text())
    for k, v in d.items():
        if v and k not in WIT:
            WIT[k] = v
JOINP = json.loads((HERE / "join-pairs.json").read_text())

FAMILY_LABEL = {
    "join-lattice": "join lattice",
    "constant-check": "constant / known-value check",
    "exist-query": "existence query",
    "list-query": "listing query",
    "comparison": "comparison",
    "assertion": "assertion",
    "control-flow": "control flow",
    "write-vs-read": "write vs read",
    "universality": "universality",
    "async-vs-sync": "async vs sync",
    "decorators": "decorators",
    "parametrize": "parametrize",
    "element-kind": "element kind",
    "subscript": "subscript",
    "helper-visit": "helper visit",
}

# mutants whose mutation site is provably never executed (structural equivalence)
STRUCTURAL = {
    "M05-is_num_const-accepts-bool":
        "assign_name() tests is_bool_const(vnode) FIRST (elif chain), so is_num_const() never sees a bool; "
        "the mutant's removed guard is unreachable",
    "M23-decorators-as-body":
        "exec_stmts() dispatches on the statement type; a decorator is an ast.Call/ast.Attribute, not a statement, "
        "and Run has no s_Call handler, so a decorator in the body list is silently ignored",
}


def reach_for(mutant: str) -> tuple[int, int]:
    """(hits, cases) for the mutant's mutated site."""
    for k, ln in REACH["lines"].items():
        if k.startswith(mutant.split("-")[0] + "-"):
            return REACH["totals"][k], REACH["cases"][k]
    return -1, -1


def main():
    rows = []
    for r in RES:
        name = r["mutant"]
        if name == "PRISTINE":
            continue
        a = ATTR.get(name, {})
        c = COR.get(name, {})
        hits, cases = reach_for(name)
        d1 = r["killed"]["d1"]
        d2 = r["killed"]["d2"]
        d3 = r["killed"]["d3"]
        moved = r["d3_population"]["moved"]
        disagree = r["d3_population"]["oracle_disagree"]
        leg_breaks = r["d3_population"]["oracle_leg_breaks"]
        wit = WIT.get(name, [])
        rows.append({
            "mutant": name, "family": r["family"], "note": r["note"],
            "D1_selftest": "K" if d1 else "s",
            "D2_adv": "K" if d2 else "s",
            "D3_population": "K" if d3 else "s",
            "population_moved": moved,
            "oracle_disagree": disagree,
            "oracle_leg_breaks": leg_breaks,
            "counter_leg_ok": c.get("oracle_ok"),
            "R1_selftest_reasons": a.get("r1_selftest_cases_differing", 0),
            "R2_adv_reasons": a.get("r2_adv_cases_differing", 0),
            "R3_pop_reasons": a.get("r3_pop_ids_differing", 0),
            "site_hits": hits, "site_cases": cases,
            "killed_by_any": r["killed_by_any"],
            "witness": wit[0] if wit else None,
            "witness_count": len(wit),
            "structural_equivalence": STRUCTURAL.get(name),
            "first_selftest_case": (a.get("r1_first") or [{}])[0].get("case"),
            "first_adv_case": (a.get("r2_first") or [{}])[0].get("case"),
            "first_pop_id": (a.get("r3_first") or [{}])[0].get("id"),
        })

    def sortkey(x):
        return (0 if x["killed_by_any"] else 1, x["mutant"])

    rows.sort(key=sortkey)
    survivors = [x for x in rows if not x["killed_by_any"]]
    killed = [x for x in rows if x["killed_by_any"]]

    # ---------------------------------------------------------------- markdown
    L = []
    L.append("# C1MutClassifier — kill matrix (42 single-edit mutants of the frozen classifier)")
    L.append("")
    L.append("Target: `plans/round53_c1_classify.py` sha256 `935db122897149a6013ca06d0001feaba4da04d606adc8197c9ff1acf8f1d0e6` "
             "(copy in scratch; the lane file was never edited).")
    L.append("")
    L.append("Detectors:")
    L.append("")
    L.append("- **D1** — the classifier's own `--selftest` (83 frozen cases), killed when `failures != 0` or the run raises.")
    L.append("- **D2** — `python3 .ufo/waves/round-53/w1/C1ExecAdvCases/check.py <mutant>` (90 adversarial cases / 371 tests), "
             "killed when `case_fail != 0` or the run raises.")
    L.append("- **D3** — the population class of the 305 `corpus/evidence/round53/tests-index.json` ids, killed when any id's "
             "P1/P0 class moves (capture bytes read from a scratch copy of `corpus/evidence/round52/graders`, sha256-verified "
             "identical to the lane's 185 files).")
    L.append("")
    L.append("Reason-level columns (R1/R2/R3) count cases where the mutant's `classify_detail()` **reasons** differ from the "
             "pristine's, even when the class does not move — the class verdict is what the claim is scored on, but the reason "
             "text is what the reports quote.")
    L.append("")
    L.append("`site_hits` is the number of times the mutated line executes over the union of the three corpora "
             "(measured by `sys.settrace` on the pristine classifier).")
    L.append("")
    L.append(f"**Totals: {len(killed)} of {len(rows)} mutants killed by at least one detector; "
             f"{len(survivors)} survive all three.**")
    L.append("")
    L.append("| mutant | family | D1 | D2 | D3 | moved | disagree | oracle leg | R1 | R2 | R3 | site hits |")
    L.append("|---|---|---|---|---|--:|--:|---|--:|--:|--:|--:|")
    for x in rows:
        leg = "break" if x["oracle_leg_breaks"] else ("ok" if x["counter_leg_ok"] else "?")
        L.append(f"| `{x['mutant']}` | {FAMILY_LABEL.get(x['family'], x['family'])} | {x['D1_selftest']} | {x['D2_adv']} | "
                 f"{x['D3_population']} | {x['population_moved']} | {x['oracle_disagree']} | {leg} | {x['R1_selftest_reasons']} | "
                 f"{x['R2_adv_reasons']} | {x['R3_pop_reasons']} | {x['site_hits']} |")
    L.append("")
    L.append("`K` = killed by that detector, `s` = survived it.")
    L.append("")
    L.append("## The counter's own ORACLE leg, run per mutant")
    L.append("")
    L.append("`plans/round53_c1_triage.py:leg_oracle()` was imported and run in-process with the classifier redirected to each "
             "mutant — the numbers are the frozen counter's, not a re-implementation.")
    L.append("")
    L.append("| mutant | counter ORACLE leg | disagree | limit |")
    L.append("|---|---|--:|--:|")
    for x in rows:
        L.append(f"| `{x['mutant']}` | {'FAIL' if x['oracle_leg_breaks'] else 'pass'} | {x['oracle_disagree']} | 9.2 |")
    L.append("")
    L.append("Four mutants break the ORACLE leg (M08, M32, M34, M36). The leg's disagreement budget is 3 % of 305 decided "
             "tests = 9.2, so a mutant that moves 1–9 population classes stays inside the leg.")
    L.append("")
    L.append("## join() lattice — the pairs the classifier actually uses")
    L.append("")
    L.append(f"`join()` is called {JOINP['total_calls']} times over the three corpora. The pairs "
             f"`{', '.join(JOINP['never_joined'])}` are never joined, which is why M01/M02/M03 are equivalent mutants "
             "on this corpus (each still has a witness outside it — see the survivors table).")
    L.append("")
    for k, v in JOINP["pairs"].items():
        L.append(f"- `{k}`: {v}")
    L.append("")
    (HERE / "kill-matrix.md").write_text("\n".join(L) + "\n")
    (HERE / "kill-matrix.json").write_text(json.dumps(rows, indent=1))

    # ---------------------------------------------------------------- survivors
    S = []
    S.append("# C1MutClassifier — survivors (mutants no detector killed)")
    S.append("")
    S.append(f"{len(survivors)} of {len(rows)} mutants survive all three detectors. Each entry names the case that should "
             "have killed it.")
    S.append("")
    for x in survivors:
        S.append(f"## `{x['mutant']}` — {FAMILY_LABEL.get(x['family'], x['family'])}")
        S.append("")
        S.append(f"- mutation: {x['note']}")
        S.append(f"- mutated site executes **{x['site_hits']} times** over the three corpora (in {x['site_cases']} cases)")
        if x["structural_equivalence"]:
            S.append(f"- **structurally equivalent** (not a coverage gap): {x['structural_equivalence']}")
        if x["witness"]:
            w = x["witness"]
            desc = w.get("desc") or w.get("template", "fuzzer grid") + " " + str(w.get("frags", ""))
            S.append(f"- the case that should have killed it — **{'CLASS moves' if w['class_moved'] else 'REASON only'}**: "
                     f"{desc}")
            S.append("")
            S.append("```python")
            S.append(w["src"].rstrip())
            S.append("```")
            S.append("")
            S.append(f"  - pristine: `{w['pristine']}` reasons {list(w['pristine_reasons'].values())}")
            S.append(f"  - mutant:   `{w['mutant']}` reasons {list(w['mutant_reasons'].values())}")
        else:
            S.append("- **no witness found**: no source in the corpus (or in the fuzzer's grid) separates the pristine from "
                     "the mutant. This mutant is an equivalent mutant on everything measured.")
        if x["R1_selftest_reasons"] or x["R2_adv_reasons"] or x["R3_pop_reasons"]:
            S.append(f"- reason-level diffs the class-level detectors cannot see: "
                     f"R1={x['R1_selftest_reasons']} selftest cases, R2={x['R2_adv_reasons']} adversarial cases, "
                     f"R3={x['R3_pop_reasons']} population ids")
        S.append("")
    (HERE / "survivors.md").write_text("\n".join(S) + "\n")
    print(f"killed {len(killed)}/{len(rows)}; survivors {len(survivors)}")
    for x in survivors:
        print(f"  {x['mutant']:38s} hits={x['site_hits']:5d} witness={'yes' if x['witness'] else 'NO'} "
              f"structural={'yes' if x['structural_equivalence'] else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
