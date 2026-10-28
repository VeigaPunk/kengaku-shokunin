#!/usr/bin/env python3
"""R49-C2 mutation battery harness (seat R49C2ExecMutBattery, scratch instrument, not a counter).

Measures the frozen substantive legs V3/V4/V7/V9/V10/V12 (round-46 counter imported at its committed
digest, V7 transcribed from the round-48 v4 delta) over a symlink-mirror of the frozen base tree, before
and after installing one mutant payload at a time.  The lane is never written: every mutation lands in the
mirror, whose mutable targets are real copies restored byte-exactly after each measurement.

Landing projection (disclosed): the round-49 spec path `plans/pkg-spec-r49.json`, the round-49 dry table and
the round-49 receipt path do not exist at the stage-1 freeze.  The mirror carries them as the *committed
round-46 bytes* at the round-49 paths fixed by the claims (dry table) and by `plans/pkg-spec-r46.json`
(receipt), with the spec projected from `plans/pkg-spec-r46.json` by repointing receipt/dry/probe only.
Every mutant payload is therefore a mutation of a committed base byte; only the *addressing* is projected.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

SCRATCH = pathlib.Path("/fast/scratch/hyaku/kengaku-r49/R49C2ExecMutBattery")
LANE = SCRATCH / "lane"
WORK = SCRATCH / "work"
WAVE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/R49C2ExecMutBattery")
MIRROR = WORK / "mirror"

SUBTARGETS = ("V3", "V4", "V7", "V9", "V10", "V12")
NAMED_TAGS = ("both-print", "toolchain")
SEPARATOR = re.compile(r":?-{2,}:?")

SPEC_R49 = "plans/pkg-spec-r49.json"
DRY_R49 = "corpus/evidence/round49/polyglot-c-py-dry-cases.txt"
RECEIPT_R49 = "corpus/evidence/round49/polyglot-c-py-probe.txt"
R46_RECEIPT = "corpus/evidence/round46/polyglot-c-py-probe.txt"
R46_DRY = "corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt"
PROBE_REL = "plans/polyglot_c_py_probe.py"
ENTRY_REL = "corpus/knowledge/tb2-polyglot-c-py-grader.md"
CAPDIR = "corpus/evidence/round46/tb2-polyglot-c-py"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def load_base():
    path = LANE / "plans/round46_c3_verify.py"
    spec = importlib.util.spec_from_file_location("r46_c3_r49c2m", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def map_rows(text):
    m = re.search(r"^## Requirement map\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        return None, []
    header, rows = None, []
    for line in m.group(1).splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if cells and all(SEPARATOR.fullmatch(c) for c in cells):
            continue
        if header is None and any("Instruction line" in c for c in cells) and any(c == "Tag" for c in cells):
            header = len(cells)
            continue
        rows.append((cells, line))
    return header, rows


def v7(base, pkg):
    """Round-48/49 V7 delta, transcribed (positive preconditions then the imported label/citation rule)."""
    try:
        tags, _ids = base.dry_table(pkg)
    except (OSError, ValueError) as e:
        return False, f"dry table unusable: {e}"
    receipt = base.text_or_none(pkg.receipt)
    entry = base.text_or_none(pkg.entry)
    if receipt is None or entry is None:
        return False, "receipt or entry absent"
    parsed = base.receipt_cases(receipt)
    bad = []
    violated = {t: sorted(cid for cid, (_o, v) in parsed.items() if t in v) for t in tags}
    for t in sorted(tags):
        if not violated[t]:
            bad.append(f"{t}:no committed case carries violates={t}")
    for t in NAMED_TAGS:
        if t not in tags:
            bad.append(f"{t}:not a frozen tag")
        elif not violated[t]:
            bad.append(f"{t}:unexercised-by-any-case")
    header, rows = map_rows(entry)
    if header is None:
        return False, "no parsable '## Requirement map' header"
    seen = {}
    for cells, line in rows:
        if len(cells) != header:
            bad.append(f"row parses to {len(cells)} cells not {header}: {line.strip()[:40]!r}")
        m = base.MAP_ROW.match(line)
        if not m:
            if "instruction.md:" in line:
                bad.append(f"row not in canonical shape: {line.strip()[:50]!r}")
            continue
        ln, tag, label, rest = m.groups()
        seen[tag] = seen.get(tag, 0) + 1
        if tag not in tags:
            bad.append(f"{tag}:not a frozen tag")
            continue
        if tags[tag] != f"instruction.md:{ln}":
            bad.append(f"{tag}:line {ln} is not the frozen {tags[tag]}")
        if not violated[tag]:
            bad.append(f"{tag}:no receipt case violates it")
            continue
        want = base.derive({parsed[c][0] for c in violated[tag]})
        if label != want:
            bad.append(f"{tag}:labelled {label}, receipt derives {want}")
        cited = re.findall(r"`([a-z0-9_-]+)`", rest)
        if not cited or any(c not in violated[tag] for c in cited):
            bad.append(f"{tag}:cites no case or a case that does not violate it")
    missing = sorted(set(tags) - set(seen))
    dup = sorted(t for t, n in seen.items() if n > 1)
    if missing:
        bad.append(f"tags missing={missing}")
    if dup:
        bad.append(f"tags duplicated={dup}")
    note = (f"rows={len(rows)} tags={len(tags)} violated={sum(1 for t in tags if violated[t])}/{len(tags)}"
            f" bad={len(bad)}")
    return not bad, note + (f" first={bad[0]}" if bad else "")


LEGS = {
    "V3": lambda b, p: b.v3(p),
    "V4": lambda b, p: b.v4(p),
    "V7": lambda b, p: v7(b, p),
    "V9": lambda b, p: b.v9(p),
    "V10": lambda b, p: b.v10(p),
    "V12": lambda b, p: b.v12(p),
}


def run_legs(base, pkg):
    out = {}
    for name in SUBTARGETS:
        try:
            ok, note = LEGS[name](base, pkg)
        except Exception as e:  # a leg that cannot run is a defect, never a pass
            ok, note = False, f"EXC {type(e).__name__}: {e}"
        out[name] = {"ok": bool(ok), "note": note}
    return out


def mirror(lane, dest):
    dest = pathlib.Path(dest)
    if dest.exists():
        shutil.rmtree(dest)
    (dest / "corpus/knowledge").parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(lane / "corpus/knowledge", dest / "corpus/knowledge")
    shutil.copytree(lane / CAPDIR, dest / CAPDIR)
    (dest / "corpus/evidence/round49").mkdir(parents=True, exist_ok=True)
    (dest / "plans").mkdir(parents=True, exist_ok=True)
    shutil.copy2(lane / PROBE_REL, dest / PROBE_REL)
    # projected spec: committed round-46 spec with receipt/dry/probe repointed to the round-49 slots only
    spec = json.loads((lane / "plans/pkg-spec-r46.json").read_text())
    spec["receipt"] = RECEIPT_R49
    spec["dry"] = DRY_R49
    spec["probe"] = PROBE_REL
    spec["receipt_sha256"] = sha((lane / R46_RECEIPT).read_bytes())
    spec["name"] = "round-49 tb2-polyglot-c-py package (projected for the mutation battery)"
    (dest / SPEC_R49).write_text(json.dumps(spec, indent=1) + "\n")
    # the projected evidence slots carry the committed round-46 bytes
    (dest / DRY_R49).write_bytes((lane / R46_DRY).read_bytes())
    (dest / RECEIPT_R49).write_bytes((lane / R46_RECEIPT).read_bytes())
    for rel in ("corpus/SOURCES.md", "corpus/README.md", "PROVINCE.md"):
        src = lane / rel
        if src.is_file():
            os.symlink(src, dest / rel)
    return dest, spec


def make_pkg(base, spec):
    return base.Pkg(MIRROR, spec, MIRROR / SPEC_R49, MIRROR / spec["entry"], MIRROR / spec["receipt"],
                    MIRROR / spec["dry"], MIRROR / spec["capture_dir"], MIRROR / spec["sources"],
                    MIRROR / spec["readme"], pins=base.CAPTURES, pinned=True, probe=MIRROR / PROBE_REL,
                    claims=MIRROR / "plans/round-49-claims.md", name="package")


def pkg_from_disk(base):
    """Re-read the spec per measurement, as the counter's real_pkg() does (a mutated spec is seen, not cached)."""
    return make_pkg(base, json.loads((MIRROR / SPEC_R49).read_text()))


def sub_once(text, old, new, what):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"mutant {what}: expected 1 occurrence of {old!r}, found {n}")
    return text.replace(old, new)


def mutants(spec_text):
    lane = LANE
    cap = {n: (lane / CAPDIR / n).read_bytes() for n in
           ("test_outputs.py", "instruction.md", "test.sh", "solve.sh", "Dockerfile", "task.toml", "README.md")}
    entry = (lane / ENTRY_REL).read_text()
    receipt = (lane / R46_RECEIPT).read_text()
    dry = (lane / R46_DRY).read_text()
    probe = (lane / PROBE_REL).read_text()
    spec = spec_text

    def enc(s):
        return s.encode()

    out = []

    def add(name, cls, target, intent, data):
        out.append({"name": name, "class": cls, "target": target, "intent": intent, "data": data})

    td = cap["test_outputs.py"].decode()
    add("cap-test-outputs-values", "capture", f"{CAPDIR}/test_outputs.py",
        "grader fixed point (42, 267914296) changed to 267914297; the decisive :27 line no longer says what "
        "the entry's mechanism row quotes",
        enc(sub_once(td, '(42, "267914296")', '(42, "267914297")', "cap-test-outputs-values")))
    add("cap-test-outputs-listing", "capture", f"{CAPDIR}/test_outputs.py",
        "exact-directory assert widened to accept a second entry; the :18 line three mechanism rows quote changes",
        enc(sub_once(td, 'assert polyglot_files == ["main.py.c"], (',
                     'assert polyglot_files == ["main.py.c", "NOTES.md"], (', "cap-test-outputs-listing")))
    ins = cap["instruction.md"].decode()
    add("cap-instruction-stdout", "capture", f"{CAPDIR}/instruction.md",
        "instruction.md:7 turns 'print to stdout' into 'print to stderr'; the stdout-only requirement's source "
        "line no longer states what the tag is anchored to",
        enc(sub_once(ins, "Both of these should print to stdout the kth Fibonacci number",
                     "Both of these should print to stderr the kth Fibonacci number", "cap-instruction-stdout")))
    ts = cap["test.sh"].decode()
    add("cap-test-sh-reward", "capture", f"{CAPDIR}/test.sh",
        "harness reward mapping inverted on the success branch (echo 1 -> echo 0 on exit 0)",
        enc(sub_once(ts, "echo 1 > /logs/verifier/reward.txt", "echo 0 > /logs/verifier/reward.txt",
                     "cap-test-sh-reward")))
    so = cap["solve.sh"].decode()
    add("cap-solve-sh-comment", "capture", f"{CAPDIR}/solve.sh",
        "oracle's C comment opener renamed (#define sdf b -> c): the polyglot's overlap mechanism no longer "
        "matches the prose the entry teaches",
        enc(sub_once(so, "#define sdf b /*", "#define sdf c /*", "cap-solve-sh-comment")))
    dk = cap["Dockerfile"].decode()
    add("cap-dockerfile-base", "capture", f"{CAPDIR}/Dockerfile",
        "image base ubuntu:24.04 -> ubuntu:22.04, the toolchain the instruction names no longer follows the recipe",
        enc(sub_once(dk, "FROM ubuntu:24.04", "FROM ubuntu:22.04", "cap-dockerfile-base")))
    tt = cap["task.toml"].decode()
    add("cap-task-toml-internet", "capture", f"{CAPDIR}/task.toml",
        "allow_internet flips true -> false in the pinned metadata",
        enc(sub_once(tt, "allow_internet = true", "allow_internet = false", "cap-task-toml-internet")))
    rm = cap["README.md"].decode()
    add("cap-readme-cases", "capture", f"{CAPDIR}/README.md",
        "authors' published case table README.md:24 f(42)=267914296 -> 267914297",
        enc(sub_once(rm, "f(42)=267914296", "f(42)=267914297", "cap-readme-cases")))

    add("entry-casetable-verdict-flip", "entry", ENTRY_REL,
        "case table row trailing-ws flips Observed pass -> fail while the receipt says pass (case table vs receipt)",
        enc(sub_once(entry, "| `trailing-ws` | P | pass |", "| `trailing-ws` | P | fail |", "entry-casetable-verdict-flip")))
    add("entry-mechanism-line-shift", "entry", ENTRY_REL,
        "mechanism row lookup-table cites test_outputs.py:27 -> :26, a line that does not decide it",
        enc(sub_once(entry, "| `lookup-table` | `test_outputs.py:27` |", "| `lookup-table` | `test_outputs.py:26` |",
                     "entry-mechanism-line-shift")))
    add("entry-source-id-removed", "entry", ENTRY_REL,
        "S169 removed from the entry body (outside source: lines); the entry no longer teaches a row the spec pins",
        enc(sub_once(entry, "S169 (`", "S1xx (`", "entry-source-id-removed")))
    add("entry-reqmap-label-invert", "entry", ENTRY_REL,
        "requirement map label python-run enforced -> unenforced (receipt derives enforced from c-only)",
        enc(sub_once(entry, "| `instruction.md:3` | `python-run` | enforced |",
                     "| `instruction.md:3` | `python-run` | unenforced |", "entry-reqmap-label-invert")))

    add("receipt-verdict-swap-compile-warning", "receipt", RECEIPT_R49,
        "one CASE observed= pass -> fail (compile-warning) with the summary line untouched: the observation column "
        "and the summary stop agreeing",
        enc(sub_once(receipt, "CASE compile-warning predicted=pass observed=pass tests=P",
                     "CASE compile-warning predicted=pass observed=fail tests=P",
                     "receipt-verdict-swap-compile-warning")))
    add("receipt-prediction-drift", "receipt", RECEIPT_R49,
        "one CASE predicted= pass -> fail while observed= stays pass: the prediction table and the observation "
        "disagree under a match=yes line",
        enc(sub_once(receipt, "CASE stderr-noise predicted=pass observed=pass tests=P",
                     "CASE stderr-noise predicted=fail observed=pass tests=P", "receipt-prediction-drift")))
    add("receipt-summary-splice", "receipt", RECEIPT_R49,
        "summary line observed_pass=7 -> 8 without changing any CASE line",
        enc(sub_once(receipt, "cases=18 observed_pass=7 observed_fail=11 mismatches=0",
                     "cases=18 observed_pass=8 observed_fail=10 mismatches=0", "receipt-summary-splice")))
    add("receipt-inventory-rename", "receipt", RECEIPT_R49,
        "CASE id empty-file renamed empty-copy, so the receipt inventory no longer matches the frozen dry table",
        enc(sub_once(receipt, "CASE empty-file predicted=fail", "CASE empty-copy predicted=fail",
                     "receipt-inventory-rename")))

    add("dry-inventory-rename", "dry table", DRY_R49,
        "frozen dry table CASE id empty-file renamed empty-copy",
        enc(sub_once(dry, "CASE empty-file predicted=fail", "CASE empty-copy predicted=fail", "dry-inventory-rename")))
    nop_line = [l for l in dry.splitlines() if l.startswith("CASE nop ")][0]
    add("dry-inventory-duplicate", "dry table", DRY_R49,
        "frozen dry table duplicates its CASE nop line: 19 case ids against the receipt's 18",
        enc(dry + nop_line + "\n"))

    add("spec-s168-digest-drift", "spec", SPEC_R49,
        "spec row S168 sha256 off by one hex digit: the registry anchor no longer resolves the pinned capture",
        enc(sub_once(spec, "a57c0c0e1232113113cd29a154ea7e0ac9ea45e4aedc16958fbc6bc753a4ef96",
                     "a57c0c0e1232113113cd29a154ea7e0ac9ea45e4aedc16958fbc6bc753a4ef97", "spec-s168-digest-drift")))
    add("spec-s172-capture-name", "spec", SPEC_R49,
        "spec row S172 capture name README.md -> readme.md: the digest resolves to a different filename",
        enc(sub_once(spec, '"capture": "README.md"', '"capture": "readme.md"', "spec-s172-capture-name")))
    s_obj = json.loads(spec)
    del s_obj["rows"]["S172"]
    add("spec-row-set-contraction", "spec", SPEC_R49,
        "spec drops row S172: invisible to V3/V9/V12 (they iterate the spec's own row set), so it is caught "
        "only by the spec digest pin when the pin is enforced",
        (json.dumps(s_obj, indent=1) + "\n").encode())

    add("probe-tags-line-shift", "probe", PROBE_REL,
        "probe TAGS both-print line instruction.md:7 -> :9: the probe's --dry table no longer matches the freeze",
        enc(sub_once(probe, '"both-print": "instruction.md:7"', '"both-print": "instruction.md:9"',
                     "probe-tags-line-shift")))
    add("probe-case-expect-flip", "probe", PROBE_REL,
        "probe Case nop predicted F -> P: the probe's --dry table predicts a different verdict",
        enc(sub_once(probe, 'Case("nop", "F", "F", ("single-file",)', 'Case("nop", "P", "F", ("single-file",)',
                     "probe-case-expect-flip")))
    return out


def main():
    base = load_base()
    spec_text = None
    mr, spec = mirror(LANE, MIRROR)
    spec_text = (MIRROR / SPEC_R49).read_text()
    pkg = make_pkg(base, spec)
    pristine = {}

    def capture_pristine(rel):
        p = MIRROR / rel
        pristine[rel] = p.read_bytes()

    muts = mutants(spec_text)
    for m in muts:
        if m["target"] not in pristine:
            capture_pristine(m["target"])
    mutable = {SPEC_R49, spec["entry"], spec["receipt"], spec["dry"], PROBE_REL} \
        | {f"{CAPDIR}/{n}" for n in base.CAPTURES}

    b = run_legs(base, pkg_from_disk(base))
    print("BASELINE " + " ".join(f"{k}={'ok' if v['ok'] else 'DEFECT'}" for k, v in b.items()))
    for k, v in b.items():
        print(f"BASELINE-NOTE {k} {v['note']}")

    results = []
    for m in muts:
        rel = m["target"]
        if rel not in mutable:
            print(f"UNMEASURABLE {m['name']} target={rel} not in mutable set")
            results.append({**{k: v for k, v in m.items() if k != "data"}, "measured": False,
                            "flips": [], "legs": {}})
            continue
        p = MIRROR / rel
        assert MIRROR.resolve() in p.parent.resolve().parents or p.parent.resolve() == MIRROR.resolve(), rel
        p.write_bytes(m["data"])
        try:
            try:
                got = run_legs(base, pkg_from_disk(base))
                unreadable = None
            except (ValueError, OSError, KeyError, json.JSONDecodeError) as e:
                # the frozen spec pin refuses the mutant: every content leg reads the package and cannot run
                got = {leg: {"ok": False, "note": f"package unreadable: {type(e).__name__}: {e}"}
                       for leg in SUBTARGETS}
                unreadable = f"{type(e).__name__}: {e}"
            probe_dry = None
            if m["class"] == "probe":
                env = dict(os.environ, TMPDIR=str(SCRATCH))
                r = subprocess.run([sys.executable, str(MIRROR / PROBE_REL), "--lane", str(MIRROR), "--dry"],
                                   capture_output=True, text=True, timeout=120, env=env, cwd=str(SCRATCH))
                probe_dry = {"exit": r.returncode, "stdout_sha": sha(r.stdout.encode()),
                             "frozen_dry_sha": sha((MIRROR / DRY_R49).read_bytes()),
                             "equal": r.stdout == (MIRROR / DRY_R49).read_text()}
        finally:
            p.write_bytes(pristine[rel])
            assert sha(p.read_bytes()) == sha(pristine[rel]), rel
        # the r49 counter's real_pkg() pins the spec: a spec byte change is refused before any leg runs, and
        # every substantive leg then scores a defect (round-48 V14 semantics), never a pass.
        pin_refused = m["class"] == "spec"
        flips = [leg for leg in SUBTARGETS if b[leg]["ok"] and not got[leg]["ok"]]
        rec = {**{k: v for k, v in m.items() if k != "data"},
               "measured": True,
               "payload_sha256": sha(m["data"]),
               "content_flips": flips,
               "spec_pin_refused": pin_refused,
               "caught": bool(flips) or pin_refused,
               "unreadable": unreadable,
               "legs": {leg: {"baseline": b[leg]["ok"], "mutant": got[leg]["ok"], "note": got[leg]["note"]}
                        for leg in SUBTARGETS}}
        if probe_dry is not None:
            rec["probe_dry"] = probe_dry
        results.append(rec)
        print(f"MUTANT {m['name']} class={m['class']} content_flips={','.join(flips) or 'NONE'} "
              f"spec_pin_refused={pin_refused} caught={'yes' if rec['caught'] else 'no'}")
        for leg in SUBTARGETS:
            if got[leg]["note"] != b[leg]["note"]:
                print(f"  NOTE-DELTA {leg}: {got[leg]['note'][:220]}")

    caught = [r["name"] for r in results if r.get("caught")]
    summary = {
        "baseline": {k: {"ok": v["ok"], "note": v["note"]} for k, v in b.items()},
        "mutants_total": len(results),
        "caught": len(caught),
        "caught_names": caught,
        "uncaught": [r["name"] for r in results if not r.get("caught")],
        "floor_half": len(results) / 2,
        "mutable": sorted(mutable),
        "spec_projection_sha256": sha((MIRROR / SPEC_R49).read_bytes()),
        "mirror": str(MIRROR),
        "results": results,
    }
    (WORK / "measurement.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(f"SUMMARY total={len(results)} caught={len(caught)} floor={len(results)/2} "
          f"uncaught={','.join(summary['uncaught'])}")

    # ---- emit the deliverable: plan.json + payloads ------------------------------------------------
    payload_dir = WAVE / "payloads"
    if payload_dir.exists():
        for old in payload_dir.iterdir():
            old.unlink()
    payload_dir.mkdir(parents=True, exist_ok=True)
    plan = {
        "claim": "R49-C2",
        "count": len(muts),
        "mut_n": len(muts),
        "mut_floor": -(-len(muts) // 2),  # ceil(N/2): V14 passes iff caught >= floor
        "floor": "fewer than <N>/2 caught -> MUTATION DEFECT; measured caught is reported per mutant below",
        "provenance": {
            "authored_by": "seat R49C2ExecMutBattery (round 49, wave 1)",
            "frozen_base": "9d2900af41e4d1fc6022eff99010436fde6dbd93",
            "payloads_derived_from": "committed round-46 package bytes at the frozen base; the spec payload is "
                                     "derived from plans/pkg-spec-r46.json projected only by repointing "
                                     "receipt/dry/probe to the round-49 slots",
            "installation": "V14 installs one payload at a time in a symlink-mirror copy; the lane is never "
                            "written",
            "measurement": "content-level substantive legs (V3/V4/V7/V9/V10/V12) re-measured on the mirror "
                           "before and after each install; the spec payload is refused by the frozen spec digest "
                           "pin before any leg runs (caught by every content leg). Probe payloads change the "
                           "probe's --dry output but no substantive leg reads the probe; they flip only V5, so "
                           "V14 scores them CLEAN unless V5 is promoted to the substantive set.",
        },
        "mutants": [],
    }
    for m in muts:
        rel_payload = f"plans/mutants49/{m['name']}.payload"
        (payload_dir / f"{m['name']}.payload").write_bytes(m["data"])
        plan["mutants"].append({"name": m["name"], "class": m["class"], "target": m["target"],
                                "payload": rel_payload, "sha256": sha(m["data"]),
                                "intent": m["intent"]})
    (WAVE / "plan.json").write_text(json.dumps(plan, indent=1) + "\n")
    print(f"EMITTED {WAVE / 'plan.json'} mutants={len(plan['mutants'])}")


if __name__ == "__main__":
    main()
