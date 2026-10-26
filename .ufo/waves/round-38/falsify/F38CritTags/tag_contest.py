#!/usr/bin/env python3
"""Round-38 wave-2 seat F38CritTags: contest the frozen `violates=` tags of
corpus/evidence/round38/build-pmars-dry-cases-freeze.txt against instruction.md's text, and recompute the
requirement-map labels (the counter's own `derive` rule) under the strongest alternative taxonomy.

Read-only over a clone of the landing tip. Nothing here edits the lane, the frozen table, the probe or the entry:
the frozen tags stay (limit), this script only prices the alternative.

Readings it distinguishes:
  FROZEN        the tags as committed (probe module TAGS/Semantics: "does not do what the instruction asks").
  ALT-LOCATION  `extract-to-app` charged to the clause's destination only (L3 "Extract the source to `/app`"),
                because the identity of the tree is already charged to `debian-source`/`from-source`.
  ALT-LITERAL   ALT-LOCATION plus a literal reading of L7 ("This should output \"Results: X Y Z\" where X, Y, Z
                are integers"): a third integer followed by extra words does not violate the stated line, and a
                negative integer is still an integer, so `results-trailing-text` and `results-negative` are
                grader-lenience / grader-strictness controls, not violated requirements.
  ALT-SENS      ALT-LITERAL plus dropping `no-x11` from `canned-x11-dlopen` (the wave-1 objection: the rig calls
                no X11 symbol). Sensitivity only: this script upholds the frozen tag with an strace receipt.
  ALT-IP        ALT-LITERAL plus dropping `install-path` from `silent-binary` (the file is at the named path; its
                silence is a from-source/results/debugger defect) and adding it to `canned-script` (a shell
                script is not "the binary"). Sensitivity: expected to move no label.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import re
import sys

TAG_LINE = re.compile(r"^TAG (\S+) (instruction\.md:\d+)$")
CASE_LINE = re.compile(r"^CASE (\S+) predicted=(pass|fail) tests=([PF]{4}) violates=(\S*) -- .*$")
RCPT_LINE = re.compile(r"^CASE (\S+) predicted=(pass|fail) observed=(pass|fail) tests=([PF]{4}) .*?\bviolates=(\S*)")
# L7 as written: three integers ("-1" is an integer), then anything.
RESULTS_LITERAL = re.compile(r"^Results: -?\d+ -?\d+ -?\d+(?:\s.*)?$")


def load_counter(lane):
    spec = importlib.util.spec_from_file_location("c2", lane / "plans/round38_c2_verify.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules["c2"] = m
    spec.loader.exec_module(m)
    return m


def load_probe(lane):
    spec = importlib.util.spec_from_file_location("probe", lane / "plans/build_pmars_probe.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules["probe"] = m
    spec.loader.exec_module(m)
    return m


def frozen(lane):
    tags, order, viol = {}, [], {}
    for line in (lane / "corpus/evidence/round38/build-pmars-dry-cases-freeze.txt").read_text().splitlines():
        m = TAG_LINE.match(line)
        if m:
            tags[m.group(1)] = m.group(2)
            continue
        m = CASE_LINE.match(line)
        if m:
            order.append(m.group(1))
            viol[m.group(1)] = set(filter(None, m.group(4).split(",")))
    return tags, order, viol


def observed(lane):
    out, sets, letters = {}, {}, {}
    for line in (lane / "corpus/evidence/round38/build-pmars-probe.txt").read_text().splitlines():
        m = RCPT_LINE.match(line)
        if m:
            out[m.group(1)] = m.group(3)
            sets[m.group(1)] = set(filter(None, m.group(5).split(",")))
            letters[m.group(1)] = m.group(4)
    return out, sets, letters


def entry_rows(lane, mod):
    entry = (lane / "corpus/knowledge/tb2-build-pmars-grader.md").read_text()
    sec = re.search(r"^## Requirement map\n(.*?)(?=^## |\Z)", entry, re.S | re.M)
    rows = {}
    for line in sec.group(1).splitlines():
        m = mod.MAP_ROW.match(line)
        if m:
            rows[m.group(2)] = {"line": m.group(1), "label": m.group(3),
                                "cited": re.findall(r"`([a-z0-9-]+)`", m.group(4))}
    return rows


def labels(sets, obs, mod, tags):
    out = {}
    for tag in tags:
        carriers = {cid: obs[cid] for cid, v in sets.items() if tag in v}
        out[tag] = (carriers, mod.derive(set(carriers.values())))
    return out


def result_text(art_case):
    """The last line of the documented command's output, as the case stages it."""
    if art_case.art.kind == "absent":
        return None
    return art_case.art.battle.rstrip("\n").splitlines()[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    mod = load_counter(lane)
    probe = load_probe(lane)
    tags, order, fviol = frozen(lane)
    obs, rviol, letters = observed(lane)
    rows = entry_rows(lane, mod)
    judged = json.loads((pathlib.Path(__file__).with_name("adjudication.json")).read_text())
    cases = {c.cid: c for c in probe.CASES}
    bad = []

    print("# frozen inputs")
    print(f"tags={len(tags)} cases={len(order)} receipt_cases={len(obs)}")
    if set(order) != set(obs):
        bad.append("dry/receipt case ids differ")
    if any(fviol[c] != rviol.get(c) for c in order):
        bad.append("dry violates= differs from receipt violates=")
    for cid in order:
        unknown = sorted(fviol[cid] - set(tags))
        if unknown:
            bad.append(f"{cid}: unknown tags {unknown}")
    print(f"case_ids_and_sets_agree={not bad}")

    base = labels(fviol, obs, mod, tags)
    print("\n# frozen tags: derived labels (counter derive rule) vs the entry")
    for tag, (carriers, lab) in base.items():
        e = rows.get(tag, {})
        flag = "" if e.get("label") == lab else " ENTRY-MISMATCH"
        print(f"FROZEN {tag} line={tags[tag]} carriers={len(carriers)} "
              f"fail={sum(v == 'fail' for v in carriers.values())} pass={sum(v == 'pass' for v in carriers.values())} "
              f"label={lab} entry={e.get('label')}{flag}")
    groups = {}
    for tag, (carriers, lab) in base.items():
        groups.setdefault((frozenset(carriers), lab), []).append(tag)
    print("\n# carrier-set degeneracy under the frozen tags")
    for (cs, lab), ts in groups.items():
        if len(ts) > 1:
            print(f"DEGENERATE identical_set_and_label label={lab} n={len(cs)} tags={sorted(ts)}")
    print(f"distinct_carrier_sets={len(groups)} of {len(tags)} tags")

    # null case: is empty-tree load-bearing for any label? (it charges all seven tags vacuously)
    no_null = {cid: set(v) for cid, v in fviol.items()}
    no_null["empty-tree"].clear()
    null_lab = labels(no_null, obs, mod, tags)
    moved = {t: (base[t][1], null_lab[t][1]) for t in tags if base[t][1] != null_lab[t][1]}
    print(f"NULLCASE empty-tree dropped: labels_moved={len(moved)} {moved or 'none'}")
    print(f"charged_pairs={sum(len(v) for v in fviol.values())} of {len(order) * len(tags)} case-tag slots")

    # ---------------- ALT-LOCATION ----------------
    alt = {cid: set(v) for cid, v in fviol.items()}
    for cid, c in cases.items():
        top = {rel.split("/")[0] for _k, rel in c.app}
        if any(t.startswith("pmars-") for t in top):
            alt[cid].discard("extract-to-app")  # destination satisfied; identity is debian-source's clause
    # ---------------- executed proof for the destination clause ----------------
    # test_debian_source_used (index 2) and test_built_from_source (index 3) both assert the one-level
    # /app/pmars-* glob is non-empty, so a P in either position is a receipt-backed witness that the source
    # tree exists at /app. Every case this seat drops extract-to-app from must show such a P.
    glob_ids = [cid for cid in order if "extract-to-app" in fviol[cid] and "extract-to-app" not in alt[cid]]
    glob_proof = [cid for cid in glob_ids if letters[cid][2] == "P" or letters[cid][3] == "P"]
    print(f"\nGLOB_EVIDENCE destination_satisfied={len(glob_proof)}/{len(glob_ids)} "
          f"letters={{{', '.join(f'{c}:{letters[c]}' for c in glob_ids)}}}")
    if len(glob_proof) != len(glob_ids):
        bad.append(f"no shape-test proof for {sorted(set(glob_ids) - set(glob_proof))}")
    for cid in ("empty-tree", "pmars-dir-elsewhere"):
        if letters[cid][2] == "P" or letters[cid][3] == "P":
            bad.append(f"{cid} contradicts the destination charge")
    print(f"GLOB_EVIDENCE destination_violated=empty-tree:{letters['empty-tree']} "
          f"pmars-dir-elsewhere:{letters['pmars-dir-elsewhere']} (both shape tests F)")

    # ---------------- ALT-LITERAL ----------------
    for cid, c in cases.items():
        text = result_text(c)
        ok = text is not None and RESULTS_LITERAL.match(text)
        if ok:
            alt[cid].discard("results-format")
    # ---------------- ALT-IP (destination clause only; no label expected to move) ----------------
    alt["silent-binary"].discard("install-path")
    alt["canned-script"].add("install-path")
    loc = labels(alt, obs, mod, tags)
    print("\n# ALT-LOCATION + ALT-LITERAL (the strongest alternative this seat argues for)")
    changed, cite_bad, diff = [], [], []
    for tag in tags:
        carriers, lab = loc[tag]
        e = rows.get(tag, {})
        cites_bad = [c for c in e.get("cited", []) if c not in carriers]
        frozen_set = {cid for cid in order if tag in fviol[cid]}
        alt_set = {cid for cid in order if tag in alt[cid]}
        if frozen_set != alt_set:
            diff.append((tag, sorted(frozen_set - alt_set), sorted(alt_set - frozen_set)))
        print(f"ALT {tag} line={tags[tag]} carriers={len(carriers)} "
              f"fail={sum(v == 'fail' for v in carriers.values())} pass={sum(v == 'pass' for v in carriers.values())} "
              f"label={lab} entry={e.get('label')} label_moves={'yes' if e.get('label') != lab else 'no'}")
        if e.get("label") != lab:
            changed.append(tag)
        if cites_bad:
            cite_bad.append((tag, cites_bad))
    print("\n# per-tag case-set differences vs frozen")
    for tag, dropped, added in diff:
        print(f"DIFF {tag} dropped_from={dropped} added_to={added}")
    print(f"\nALT labels_change={len(changed)} rows={changed}")
    print(f"ALT rows_needing_a_new_citation={len(cite_bad)} rows={cite_bad}")
    print(f"contested_set_edits_drop={sum(len(d) for _t, d, _a in diff)} add=1 (canned-script:install-path)")

    # ---------------- ALT-SENS: dlopen no-x11 ----------------
    sens = {cid: set(v) for cid, v in alt.items()}
    sens["canned-x11-dlopen"].discard("no-x11")
    sens_lab = labels(sens, obs, mod, tags)
    print("\n# ALT-SENS: additionally drop no-x11 from canned-x11-dlopen (upheld below by strace)")
    for tag in ("no-x11",):
        carriers, lab = sens_lab[tag]
        print(f"SENS {tag} carriers={len(carriers)} fail={sum(v == 'fail' for v in carriers.values())} "
              f"pass={sum(v == 'pass' for v in carriers.values())} label={lab} entry={rows[tag]['label']} "
              f"label_moves={'yes' if rows[tag]['label'] != lab else 'no'}")
    print(f"SENS labels_change_total={len(changed) + (rows['no-x11']['label'] != sens_lab['no-x11'][1])}")

    # ---------------- SENS2: behaviour-only debugger-works (the alternative this seat rejects) ----------------
    sens2 = {cid: set(v) for cid, v in alt.items()}
    for cid, c in cases.items():
        if c.art.kind != "absent" and c.art.debug == probe.DEBUG_OK:
            sens2[cid].discard("debugger-works")  # a well-formed transcript would count as a working debugger
    s2 = labels(sens2, obs, mod, tags)["debugger-works"]
    print(f"SENS2 debugger-works carriers={sorted(s2[0])} fail={sum(v == 'fail' for v in s2[0].values())} "
          f"pass={sum(v == 'pass' for v in s2[0].values())} label={s2[1]} entry={rows['debugger-works']['label']} "
          f"label_moves={'yes' if rows['debugger-works']['label'] != s2[1] else 'no'} (rejected below: a "
          f"transcript is not a debugger that works properly)")
    print(f"SENS2 labels_change_total={len(changed) + (rows['debugger-works']['label'] != s2[1])}")

    # ---------------- adjudication consistency ----------------
    c_drop = {(i["cid"], i["tag"]) for i in judged if i["verdict"] == "C" and i["kind"] == "drop"}
    c_add = {(i["cid"], i["tag"]) for i in judged if i["verdict"] == "C" and i["kind"] == "add"}
    computed_drop = {(cid, tag) for cid in order for tag in fviol[cid] if tag not in alt[cid]}
    computed_add = {(cid, tag) for cid in order for tag in alt[cid] if tag not in fviol[cid]}
    if c_drop != computed_drop or c_add != computed_add:
        bad.append(f"adjudication C entries disagree with computed ALT edits: "
                   f"missing={sorted(c_drop - computed_drop)} extra={sorted(computed_drop - c_drop)} "
                   f"add_missing={sorted(c_add - computed_add)} add_extra={sorted(computed_add - c_add)}")
    print(f"\nADJUDICATION_EDITS_MATCH_ALT={c_drop == computed_drop and c_add == computed_add}")
    print("\n# per-case tag adjudication (non-defensible and upheld-contest entries only)")
    for item in judged:
        print(f"JUDGE {item['cid']} {item['tag']} {item['verdict']} {item['kind']} :: {item['why']}")
    print(f"JUDGE contested_deletions={len(c_drop)} contested_additions={len(c_add)} "
          f"upheld_contests={sum(1 for i in judged if i['verdict'] == 'U')} "
          f"weak={sum(1 for i in judged if i['verdict'] == 'W')}")

    order_tags = ["from-source", "no-x11", "debian-source", "extract-to-app", "install-path",
                  "results-format", "debugger-works"]
    print("\n# matrix: C=charged-but-contested  +=contested-add  d=charged,defensible  .=not charged")
    print("CASE observed " + " ".join(t[:4] for t in order_tags))
    for cid in order:
        cells = []
        for t in order_tags:
            if (cid, t) in c_drop:
                cells.append("C")
            elif (cid, t) in c_add:
                cells.append("+")
            elif t in fviol[cid]:
                cells.append("d")
            else:
                cells.append(".")
        print(f"{cid} {obs[cid]} " + "    ".join(cells))
    print(f"charged_pairs_defensible={sum(1 for cid in order for t in order_tags if t in fviol[cid]) - len(c_drop)} "
          f"charged_pairs_contested={len(c_drop)} adds={len(c_add)}")

    print(f"\nTAGS_CONTESTED={len(c_drop) + len(c_add)} LABELS_CHANGE={len(changed)}")
    print("TAGS-CONTEST OK" if not bad else f"TAGS-CONTEST SETUP-BAD {bad}")
    return 0 if not bad else 2


if __name__ == "__main__":
    sys.exit(main())
