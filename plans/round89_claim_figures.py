#!/usr/bin/env python3
"""R89-C2 counter — Q66 executable half, hardened on the four round-88 attack findings.

Every frozen before-figure in the claims corpus is extracted from claim bytes (never hand-copied),
its claim's own counter is re-run at that claim's own BASE, and the result is compared. Changes from
`plans/round88_claim_figures.py` (which is not edited):

  (a) the KNOWN check compares (claim, key, claimed, measured): a doctored claimed value is UNEXPECTED
  (b) the extracted record multiset is compared with the pinned table `plans/round89-q66-records.json`:
      a deleted before-figure or a doctored claimed value is a defect (round-88 findings 2 and 3)
  (c) the selftest battery runs inside the predicate path (round-88 finding 5)
  (d) `--controls` runs the frozen control fixtures (doctored claimed value, deleted before-figure,
      doctored key, selftest failure injected into the predicate path) and the unmodified tip; the
      four controls must be red and the tip green

Population (frozen): `plans/round-8{0..7}-claims.md`. Record kinds, extraction and counter re-runs are
unchanged from round 88 (see that file's docstring for the marker grammar).

Predicate (frozen): pass iff every extracted record is checked, every re-run completed, the record
multiset equals the pinned table, the mismatch set equals the frozen KNOWN set exactly, and the selftest
battery exits 0. Exit: 0 predicate pass, 1 at least one defect, 2 could not evaluate.

Usage:  python3 plans/round89_claim_figures.py --lane <repo> --rev <rev> --work <dir>
        python3 plans/round89_claim_figures.py --lane <repo> --rev <rev> --work <dir> --controls
        python3 plans/round89_claim_figures.py --lane <repo> --rev <rev> --work <dir> --selftest
        python3 plans/round89_claim_figures.py --lane <repo> --rev <rev> --work <dir> --freeze-records
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

LANE_DEFAULT = Path(".")
RECORD_TABLE = "plans/round89-q66-records.json"

# ---------------------------------------------------------------- frozen table
BASES = {
    80: "dce7c275381c669e6489f1b795b1505d0824c262",
    81: "4e833e9fee8022d24559535178c6fe32b2cd62f1",
    82: "a3a03ac31451e58f1742b9bccb73b72c2d90a95c",
    83: "614f00559c75155ec100e945b3e8257b14fb7496",
    84: "4087b2f8369fb0c317a8460725a607681ff2fd7f",
    85: "0de45354d7aff18e4a23a348ec13de3a1f707a44",
    86: "88651a72ef112ed9f5361e1c8c197babec691f96",
    87: "b9be687774e6b559470f5b0d9b936315b51ff311",
}
CLAIMS = {
    "R80-C1": ("plans/round-80-claims.md", "plans/round80_c1_located_replay.py",
               "rev", ["--lane", "{LANE}", "--rev", "{BASE}", "--work", "{WORK}"]),
    "R80-C2": ("plans/round-80-claims.md", "plans/round80_c2_spotcheck_debt.py",
               "rev", ["--lane", "{LANE}", "--rev", "{BASE}", "--work", "{WORK}"]),
    "R81-C1": ("plans/round-81-claims.md", "plans/round81_c1_new_members.py",
               "rev", ["--lane", "{LANE}", "--rev", "{BASE}", "--work", "{WORK}"]),
    "R81-C2": ("plans/round-81-claims.md", "plans/round81_c2_spotcheck_debt.py",
               "rev", ["--lane", "{LANE}", "--rev", "{BASE}", "--work", "{WORK}"]),
    "R82-C1": ("plans/round-82-claims.md", "plans/round82_c1_plans_registry.py",
               "tree", ["--lane", "{LANE}", "--tip", "HEAD", "--base", "HEAD"]),
    "R82-C2": ("plans/round-82-claims.md", "plans/round82_c2_closure_debt.py",
               "tree", ["--lane", "{LANE}", "--work", "{WORK}"]),
    "R82-C3": ("plans/round-82-claims.md", None, "prose", []),
    "R83-C1": ("plans/round-83-claims.md", "plans/round83_c1_replay.py",
               "rev", ["--lane", "{LANE}", "--rev", "{BASE}", "--work", "{WORK}"]),
    "R83-C2": ("plans/round-83-claims.md", "plans/round83_c2_debt.py",
               "rev", ["--lane", "{LANE}", "--rev", "{BASE}", "--work", "{WORK}"]),
    "R84-C1": ("plans/round-84-claims.md", "plans/round84_c1_replay.py",
               "rev", ["--lane", "{LANE}", "--rev", "{BASE}", "--work", "{WORK}"]),
    "R84-C2": ("plans/round-84-claims.md", "plans/round84_c2_admission.py",
               "rev", ["--lane", "{LANE}", "--rev", "{BASE}", "--work", "{WORK}"]),
    "R85-C1": ("plans/round-85-claims.md", "plans/round85_c1_replay.py",
               "rev", ["--lane", "{LANE}", "--rev", "{BASE}", "--work", "{WORK}"]),
    "R85-C2": ("plans/round-85-claims.md", "plans/round85_c2_debt.py",
               "rev", ["--lane", "{LANE}", "--rev", "{BASE}", "--work", "{WORK}"]),
    "R86-C1": ("plans/round-86-claims.md", "plans/round86_c1_replay.py",
               "rev", ["--lane", "{LANE}", "--rev", "{BASE}", "--work", "{WORK}"]),
    "R86-C2": ("plans/round-86-claims.md", "plans/round86_c2_repin.py",
               "rev", ["--lane", "{LANE}", "--rev", "{BASE}", "--work", "{WORK}"]),
    "R87-C1": ("plans/round-87-claims.md", "plans/round87_c1_replay.py",
               "rev", ["--lane", "{LANE}", "--rev", "{BASE}", "--work", "{WORK}"]),
    "R87-C2": ("plans/round-87-claims.md", "plans/round87_c2_wording.py",
               "rev", ["--lane", "{LANE}", "--rev", "{BASE}"]),
}
TREE_OVERLAY = {
    "plans/round82_c1_plans_registry.py": "82fe89d5dd29fa4c1bb8d85399d9e43442d1b862",
    "plans/round82_c2_closure_debt.py": "82fe89d5dd29fa4c1bb8d85399d9e43442d1b862",
    "plans/round82_c2_checks.py": "82fe89d5dd29fa4c1bb8d85399d9e43442d1b862",
}
PROSE_ABSENT = {
    "R82-C3": ["plans/round82_c3_sweep.py", "plans/round82-sweep-map.json",
               "corpus/evidence/round82/sweep.txt"],
}
# frozen expected mismatch set: (claim, key, claimed, measured) — exact, including the claimed value
KNOWN = {
    ("R87-C1", "kv:defects", "claimed==7", 3),
}
CLAIMS_FILES = [f"plans/round-{n}-claims.md" for n in range(80, 88)]

# ---------------------------------------------------------------- extraction (unchanged from round 88)
BEFORE_RE = re.compile(r"(?i)(?<!-)\bbefore\b(?!-)|\bat BASE\b")
SPAN_END_RE = re.compile(r"PREDICATE|\bfail\b|\bpass\b|\bAfter\b|exit 0|measured tip|\*\*After")
FAIL_RE = re.compile(r"fail|exit 1|could-not-evaluate")
CONVO_RE = re.compile(r"TARGET |DEFECTS |PREDICATE |located=|executed=|"
                      r"reproduced=|ledger_flipped=|mismatches=|indexed=|"
                      r"state_mismatches=|DEFECT |q\d+=")
KV_RE = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*(=>=|>=|=)\s*(\d+)\b")
DEF_RE = re.compile(r"DEFECTS\s+n\s*(=>=|>=|=)\s*(\d+)")
CODE_RE = re.compile(r"\b(\d+|[a-z]+)\s+`?([A-Z][A-Z0-9][A-Z0-9-]{2,})`?")
CODE2_RE = re.compile(r"`([A-Z][A-Z0-9][A-Z0-9-]{2,})\s+(\d+)`")
NUMWORD = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
           "seven": 7, "eight": 8, "nine": 9, "ten": 10}
STOP_CODES = {"PASS", "FAIL", "EXIT", "CASE", "TARGET", "PREDICATE", "DEFECT",
              "DEFECTS", "BASE", "REV", "LANE", "HEAD", "TRUE", "FALSE"}
ID_CODE_RE = re.compile(r"^(R\d+-[A-Z]?\d+|V\d+|S\d+|W\d+)$")


def claim_spans(text: str) -> list[tuple[str, str, str]]:
    sections = re.split(r"(?m)^(##\s+R\d+-C\d+.*)$", text)
    spans: list[tuple[str, str, str]] = []
    for i in range(1, len(sections), 2):
        head = sections[i]
        body = sections[i + 1] if i + 1 < len(sections) else ""
        m = re.match(r"##\s+(R\d+-C\d+)", head)
        if not m:
            continue
        cid = m.group(1)
        for mm in BEFORE_RE.finditer(body):
            marker = mm.group(0)
            if marker.lower() == "before":
                tail = body[mm.end():]
                end = SPAN_END_RE.search(tail)
                cut = end.start() if end else len(tail)
                span = tail[:cut]
                for stop in ("\n## ", "\n- ", "\n* ", "\n|", "\n**After"):
                    idx = span.find(stop)
                    if idx != -1:
                        span = span[:idx]
                        cut = min(cut, idx)
                window = tail[:cut + 300]
                if not FAIL_RE.search(window) or not CONVO_RE.search(span):
                    continue
                spans.append((cid, "before", marker + span))
            else:
                prefix = body[:mm.start()][-1200:]
                cuts = [prefix.rfind(";"), prefix.rfind(". "), prefix.rfind(".\n"),
                        prefix.rfind("\n\n"), prefix.rfind("\n- "), prefix.rfind("\n|")]
                boundary = max(cuts)
                span = prefix[boundary + 1:] if boundary >= 0 else prefix
                span = span.strip()
                if "exit 1" not in span or not CONVO_RE.search(span):
                    continue
                spans.append((cid, "atbase", span + " " + marker))
    return spans


def extract_records_from_text(text: str) -> tuple[list[dict], int]:
    records: list[dict] = []
    seen: set[tuple] = set()
    prose = 0

    def add(rec: dict) -> None:
        key = (rec["claim"], rec["kind"], rec["key"], rec["op"], rec["claimed"])
        if key not in seen:
            seen.add(key)
            records.append(rec)

    for cid, _kind, span in claim_spans(text):
        found = False
        for op, num in DEF_RE.findall(span):
            add({"claim": cid, "kind": "deftotal", "key": "defects",
                 "op": ">=" if op in (">=", "=>=") else "=", "claimed": int(num),
                 "span": span[:160]})
            found = True
        for key, op, num in KV_RE.findall(span):
            if key in ("n",):
                continue
            add({"claim": cid, "kind": "kv", "key": key,
                 "op": ">=" if op in (">=", "=>=") else "=", "claimed": int(num),
                 "span": span[:160]})
            found = True
        for token, code in CODE_RE.findall(span):
            code = code.upper().replace("_", "-")
            if code in STOP_CODES or ID_CODE_RE.match(code):
                continue
            n = int(token) if token.isdigit() else NUMWORD.get(token, -1)
            if n < 0:
                continue
            add({"claim": cid, "kind": "code", "key": code.lower(),
                 "op": "=", "claimed": n, "span": span[:160]})
            found = True
        for code, num in CODE2_RE.findall(span):
            code = code.upper().replace("_", "-")
            if code in STOP_CODES or ID_CODE_RE.match(code):
                continue
            add({"claim": cid, "kind": "code", "key": code.lower(),
                 "op": "=", "claimed": int(num), "span": span[:160]})
            found = True
        for m in re.finditer(r"`?(INDEX-MISSING|indexed=no)`?", span):
            add({"claim": cid, "kind": "code", "key": m.group(1).lower(),
                 "op": "present", "claimed": 1, "span": span[:160]})
            found = True
        if not found:
            prose += 1
    return records, prose


# ---------------------------------------------------------------- counter runs
def git(lane: Path, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(cwd or lane), *args],
                          capture_output=True, text=True, timeout=120)


def run_rev(lane: Path, counter: str, base: str, work: Path) -> tuple[int, str]:
    spec = next(s for c, s in CLAIMS.items() if s[1] == counter)
    argv = [a.replace("{LANE}", str(lane)).replace("{BASE}", base)
            .replace("{WORK}", str(work)) for a in spec[3]]
    cmd = [sys.executable, str(lane / counter)] + argv
    proc = subprocess.run(cmd, cwd=str(lane), capture_output=True, text=True,
                          timeout=900, env={"PATH": "/usr/bin", "TMPDIR": str(work)})
    return proc.returncode, proc.stdout + proc.stderr


def run_tree(lane: Path, counter: str, base: str, work: Path) -> tuple[int, str]:
    tree = Path(tempfile.mkdtemp(prefix="q66-tree-", dir=work))
    proc = subprocess.run(["git", "-C", str(lane), "archive", base],
                          capture_output=True, timeout=300)
    if proc.returncode != 0:
        return 2, f"archive-failed {base}"
    import tarfile, io
    with tarfile.open(fileobj=io.BytesIO(proc.stdout)) as tf:
        tf.extractall(tree, filter="data")
    for rel, rev in TREE_OVERLAY.items():
        blob = git(lane, "show", f"{rev}:{rel}")
        if blob.returncode == 0:
            dest = tree / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(blob.stdout.encode())
    git(tree, "init", "-q", ".")
    git(tree, "add", "-A")
    git(tree, "-c", "user.name=q66", "-c", "user.email=q66@scratch", "commit", "-qm", "base")
    spec = next(s for c, s in CLAIMS.items() if s[1] == counter)
    argv = [a.replace("{LANE}", ".").replace("{BASE}", "HEAD")
            .replace("{WORK}", str(work / "inner")) for a in spec[3]]
    cmd = [sys.executable, counter] + argv
    proc = subprocess.run(cmd, cwd=str(tree), capture_output=True, text=True,
                          timeout=900, env={"PATH": "/usr/bin", "TMPDIR": str(work)})
    return proc.returncode, proc.stdout + proc.stderr


def run_prose(lane: Path, claim: str, base: str) -> tuple[int, str]:
    paths = PROSE_ABSENT.get(claim, [])
    present = []
    for rel in paths:
        proc = git(lane, "cat-file", "-e", f"{base}:{rel}")
        if proc.returncode == 0:
            present.append(rel)
    if present:
        return 1, f"PROSE-ABSENT-FAIL present={present}"
    return 0, f"PROSE-ABSENT-OK paths={len(paths)}"


# ---------------------------------------------------------------- measurement
def parse_target(output: str) -> dict[str, str]:
    kv: dict[str, str] = {}
    for line in output.splitlines():
        if line.startswith("TARGET "):
            for m in re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)=([^\s]+)", line):
                kv[m.group(1)] = m.group(2)
    return kv


def parse_defects(output: str) -> tuple[int | None, dict[str, int]]:
    total = None
    codes: dict[str, int] = {}
    for line in output.splitlines():
        m = re.match(r"DEFECTS n=(\d+)", line)
        if m:
            total = int(m.group(1))
        m = re.match(r"DEFECT ([A-Z][A-Z0-9-]+)\b", line)
        if m:
            code = m.group(1).lower()
            codes[code] = codes.get(code, 0) + 1
    return total, codes


def check_record(rec: dict, output: str) -> tuple[str, str]:
    """Return (verdict, detail): 'match' | 'mismatch' | 'unparsed'."""
    target = parse_target(output)
    deftotal, codes = parse_defects(output)
    kind, key, op, claimed = rec["kind"], rec["key"], rec["op"], rec["claimed"]
    if kind == "kv":
        measured = target.get(key)
        if measured is None:
            return "unparsed", f"{key} absent from TARGET"
        mv = int(measured) if measured.lstrip("-").isdigit() else None
        if mv is None:
            return "unparsed", f"{key}={measured!r} not an int"
        ok = mv >= claimed if op == ">=" else mv == claimed
        return ("match" if ok else "mismatch"), f"{key} claimed {op}{claimed} measured {mv}"
    if kind == "deftotal":
        if deftotal is None:
            return "unparsed", "no DEFECTS line"
        ok = deftotal >= claimed if op == ">=" else deftotal == claimed
        return ("match" if ok else "mismatch"), f"defects claimed {op}{claimed} measured {deftotal}"
    if kind == "code":
        if op == "present":
            if key == "indexed=no":
                found = 1 if re.search(r"(^|\s)indexed=no(\s|$)", output) else 0
            else:
                found = 1 if (key in codes and codes[key] > 0) else 0
            ok = found == claimed
            return ("match" if ok else "mismatch"), f"{key} present={found} claimed {claimed}"
        measured = codes.get(key, 0)
        ok = measured == claimed
        return ("match" if ok else "mismatch"), f"{key} claimed {claimed} measured {measured}"
    return "unparsed", f"kind {kind}"


# ---------------------------------------------------------------- collection and predicate
_COUNTER_CACHE: dict[tuple[str, str], tuple[int, str]] = {}


def claims_text(lane: Path, rev: str, rel: str, overrides: dict[str, str] | None) -> str | None:
    if overrides and rel in overrides:
        return overrides[rel]
    blob = git(lane, "show", f"{rev}:{rel}")
    return blob.stdout if blob.returncode == 0 else None


def collect(lane: Path, rev: str, work: Path, overrides: dict[str, str] | None = None
            ) -> tuple[list[dict], int, dict[str, list[dict]], list[str]]:
    """Extract every record from the claims bytes at rev (or the override bytes)."""
    defects: list[str] = []
    all_records: list[dict] = []
    prose_total = 0
    for rel in CLAIMS_FILES:
        proc = git(lane, "cat-file", "-e", f"{rev}:{rel}")
        if proc.returncode != 0 and not (overrides and rel in overrides):
            defects.append(f"F1-corpus {rel} absent at {rev[:12]}")
    for rel in CLAIMS_FILES:
        text = claims_text(lane, rev, rel, overrides)
        if text is None:
            continue
        records, prose = extract_records_from_text(text)
        all_records.extend(records)
        prose_total += prose
    by_claim: dict[str, list[dict]] = {}
    for rec in all_records:
        by_claim.setdefault(rec["claim"], []).append(rec)
    return all_records, prose_total, by_claim, defects


def pinned_records(lane: Path, rev: str) -> list[tuple] | None:
    blob = git(lane, "show", f"{rev}:{RECORD_TABLE}")
    if blob.returncode != 0:
        return None
    rows = json.loads(blob.stdout)
    return sorted((r["claim"], r["kind"], r["key"], r["op"], r["claimed"]) for r in rows)


def run_counters(lane: Path, rev: str, work: Path, by_claim: dict[str, list[dict]],
                 defects: list[str]) -> dict[str, tuple[int, str]]:
    outputs: dict[str, tuple[int, str]] = {}
    for cid in sorted(set(by_claim) | set(CLAIMS)):
        spec = CLAIMS.get(cid)
        if spec is None:
            defects.append(f"F2-claim {cid} has no frozen counter entry")
            continue
        _file, counter, mode, _argv = spec
        base = BASES[int(cid.split("-")[0][1:])]
        if mode == "prose":
            outputs[cid] = run_prose(lane, cid, base)
            if outputs[cid][0] != 0:
                defects.append(f"F3-prose {cid} {outputs[cid][1]}")
            continue
        if counter is None:
            defects.append(f"F2-claim {cid} no counter")
            continue
        cache_key = (cid, base)
        if cache_key in _COUNTER_CACHE:
            outputs[cid] = _COUNTER_CACHE[cache_key]
            if "PREDICATE" not in outputs[cid][1]:
                defects.append(f"F3-nopredicate {cid} rc={outputs[cid][0]}")
            continue
        work_c = work / cid
        work_c.mkdir(parents=True, exist_ok=True)
        try:
            if mode == "rev":
                rc, out = run_rev(lane, counter, base, work_c)
            elif mode == "tree":
                rc, out = run_tree(lane, counter, base, work_c)
            else:
                defects.append(f"F2-mode {cid} {mode}")
                continue
        except subprocess.TimeoutExpired:
            defects.append(f"F3-timeout {cid}")
            continue
        outputs[cid] = (rc, out)
        _COUNTER_CACHE[cache_key] = (rc, out)
        if "PREDICATE" not in out:
            defects.append(f"F3-nopredicate {cid} rc={rc}")
    return outputs


def selftest_defects(lane: Path, rev: str, work: Path) -> list[str]:
    """Able-to-fail battery, run from the predicate path. Prints SELFTEST lines."""
    defects: list[str] = []

    def check(tid: str, ok: bool, detail: str) -> None:
        print(f"SELFTEST {tid} {'pass' if ok else 'fail'} {detail}")
        if not ok:
            defects.append(tid)

    blob = git(lane, "show", f"{rev}:plans/round-87-claims.md")
    if blob.returncode != 0:
        check("T1-doctored", False, "cannot read round-87 claims at rev")
    else:
        doctored = blob.stdout.replace("defects=7", "defects=9", 1)
        tmp = Path(tempfile.mkdtemp(prefix="q66-selftest-", dir=work)) / "claims.md"
        tmp.write_text(doctored)
        records, _prose = extract_records_from_text(doctored)
        kv = [r for r in records if r["kind"] == "kv" and r["key"] == "defects"
              and r["claim"] == "R87-C1"]
        check("T1-doctored-extract", any(r["claimed"] == 9 for r in kv),
              f"records={[(r['key'], r['claimed']) for r in kv]}")
        rc, out = run_rev(lane, "plans/round87_c1_replay.py", BASES[87], work / "T1")
        mism = [r for r in kv if r["claimed"] == 9]
        verdict = check_record(mism[0], out)[0] if mism else "unparsed"
        check("T1-doctored-mismatch", verdict == "mismatch",
              f"verdict={verdict} (doctored figure must not match BASE output)")

    neg = ("## R99-C9 fixture\n"
           "The red-before run's failure text is committed.\n"
           "The C2 before-revision is an existing revision (BASE).\n"
           "The receipts are 25 before and 26 after.\n"
           "Universe: section 6 at BASE; no newest-file selection.\n")
    check("T2-marker-negatives", len(claim_spans(neg)) == 0, f"spans={len(claim_spans(neg))}")

    fwd = ("## R99-C9 fixture\n"
           "**Target.** `defects=7`, `located=0`, `PREDICATE R99-C9 fail`, exit 1 at BASE.\n")
    spans = claim_spans(fwd)
    ok = (len(spans) == 1 and "defects=7" in spans[0][2]
          and "located=0" in spans[0][2] and "at BASE" in spans[0][2])
    check("T3-atbase-backward", ok, f"spans={spans}")

    dup = ("## R99-C9 fixture\n"
           "- **Before (BASE):** `TARGET defects=7 located=0`, "
           "`PREDICATE R99-C9 fail`, exit 1.\n"
           "- **Do-nothing control:** the counter at BASE must report "
           "`defects=7` (exit 1).\n")
    records, _prose = extract_records_from_text(dup)
    d7 = [r for r in records if r["kind"] == "kv" and r["key"] == "defects"
          and r["claimed"] == 7]
    check("T4-dedupe", len(d7) == 1, f"defects=7 records={len(d7)}")
    return defects


def run_check(lane: Path, rev: str, work: Path, overrides: dict[str, str] | None = None,
              selftest_fn=None, quiet: bool = False) -> tuple[int, list[str]]:
    """The predicate. Returns (rc, defect lines). Prints the report unless quiet."""
    out_lines: list[str] = []

    def emit(line: str) -> None:
        out_lines.append(line)
        if not quiet:
            print(line)

    all_records, prose_total, by_claim, defects = collect(lane, rev, work, overrides)
    outputs = run_counters(lane, rev, work, by_claim, defects)

    # (b) the record multiset equals the pinned table
    pinned = pinned_records(lane, rev)
    current = sorted((r["claim"], r["kind"], r["key"], r["op"], r["claimed"]) for r in all_records)
    if pinned is None:
        defects.append(f"F7-table-absent {RECORD_TABLE} at {rev[:12]}")
    else:
        for row in sorted(set(pinned) - set(current)):
            defects.append(f"F7-record-missing {row}")
        for row in sorted(set(current) - set(pinned)):
            defects.append(f"F7-record-extra {row}")
        if pinned != current and set(pinned) == set(current):
            defects.append("F7-record-count multiset differs with equal support")

    mismatches: list[tuple[str, str, str, int]] = []
    checked = matched = 0
    for cid, recs in by_claim.items():
        entry = outputs.get(cid)
        if entry is None:
            continue
        rc, out = entry
        if not recs:
            _f, _c, mode, _a = CLAIMS[cid]
            if mode in ("rev", "tree") and (rc == 0 or "PREDICATE" not in out):
                defects.append(f"F6-norecords {cid} rc={rc} (before-state must fail at BASE)")
            continue
        for rec in recs:
            verdict, detail = check_record(rec, out)
            checked += 1
            key = f"{rec['kind']}:{rec['key']}"
            if verdict == "match":
                matched += 1
            elif verdict == "mismatch":
                measured_m = re.search(r"measured (\d+)", detail)
                measured_v = int(measured_m.group(1)) if measured_m else -1
                mismatches.append((cid, key, f"claimed=={rec['claimed']}" if rec["op"] == "="
                                   else f"claimed>={rec['claimed']}", measured_v))
            else:
                defects.append(f"F4-unparsed {cid}:{key} {detail}")

    # (a) the KNOWN check compares (claim, key, claimed, measured)
    for cid, key, claimed, measured in mismatches:
        status = "KNOWN" if (cid, key, claimed, measured) in KNOWN else "UNEXPECTED"
        emit(f"MISMATCH {status} {cid} {key} {claimed} measured {measured}")
    for row in sorted(set(mismatches) - KNOWN):
        defects.append(f"F5-unexpected {row[0]} {row[1]} {row[2]} measured {row[3]}")
    for row in sorted(KNOWN - set(mismatches)):
        defects.append(f"F5-missing-known {row[0]} {row[1]} {row[2]} measured {row[3]}")

    work.mkdir(parents=True, exist_ok=True)
    st = selftest_fn(lane, rev, work) if selftest_fn else selftest_defects(lane, rev, work)
    for tid in st:
        defects.append(f"F8-selftest {tid}")

    emit(f"RECORDS claims=17 files={len(CLAIMS_FILES)} records={len(all_records)} "
         f"checked={checked} matched={matched} mismatches={len(mismatches)} prose={prose_total}")
    for d in defects:
        emit(f"DEFECT {d}")
    emit(f"DEFECTS n={len(defects)}")
    emit(f"TARGET claims=17 records={len(all_records)} checked={checked} "
         f"matched={matched} mismatches={len(mismatches)} defects={len(defects)}")
    emit(f"PREDICATE R89-C2 {'pass' if not defects else 'fail'}")
    return (0 if not defects else 1), defects


# ---------------------------------------------------------------- controls (d)
def control_overrides(lane: Path, rev: str) -> dict[str, dict]:
    r87 = git(lane, "show", f"{rev}:plans/round-87-claims.md").stdout
    r85 = git(lane, "show", f"{rev}:plans/round-85-claims.md").stdout
    return {
        "doctored-claimed": {"overrides": {"plans/round-87-claims.md": r87.replace("defects=7", "defects=9", 1)}},
        "deleted-figure": {"overrides": {"plans/round-85-claims.md": _drop_before(r85)}},
        "doctored-key": {"overrides": {"plans/round-87-claims.md": r87.replace("defects=7", "defect=7", 1)}},
        "selftest-in-path": {"selftest_fn": lambda lane_, rev_, work_: ["T-injected-failure"]},
    }


def _drop_before(text: str) -> str:
    """Remove the first R85-C1 Before sentence line that carries a counter TARGET figure."""
    out, dropped = [], False
    section = ""
    for line in text.splitlines(keepends=True):
        if line.startswith("## "):
            section = line
        if (not dropped and section.startswith("## R85-C1") and "Before (BASE" in line
                and "TARGET" in line):
            dropped = True
            continue
        out.append(line)
    return "".join(out)


def controls(lane: Path, rev: str, work: Path) -> int:
    results: list[str] = []
    vacuous = False
    for name, spec in control_overrides(lane, rev).items():
        for rel, text in (spec.get("overrides") or {}).items():
            original = git(lane, "show", f"{rev}:{rel}").stdout
            if text == original:
                vacuous = True
                print(f"CONTROL {name} vacuous fixture equals {rel} at {rev[:12]}")
        rc, defects = run_check(lane, rev, work / name, quiet=True, **spec)
        verdict = "red" if rc != 0 else "green"
        results.append(verdict)
        print(f"CONTROL {name} {verdict} rc={rc} defects={len(defects)} "
              f"first={defects[0] if defects else 'none'}")
    rc, defects = run_check(lane, rev, work / "tip", quiet=True)
    tip_verdict = "green" if rc == 0 else "red"
    print(f"CONTROL tip {tip_verdict} rc={rc} defects={len(defects)}")
    ok = all(v == "red" for v in results) and tip_verdict == "green" and not vacuous
    print(f"PREDICATE R89-C2-CONTROLS {'pass' if ok else 'fail'} red={results.count('red')} "
          f"of {len(results)} tip={tip_verdict}")
    return 0 if ok else 1


def freeze_records(lane: Path, rev: str, work: Path) -> int:
    records, _prose, _by, _d = collect(lane, rev, work)
    rows = sorted(({"claim": r["claim"], "kind": r["kind"], "key": r["key"], "op": r["op"],
                    "claimed": r["claimed"]} for r in records),
                  key=lambda r: (r["claim"], r["kind"], r["key"], r["op"], r["claimed"]))
    print(json.dumps(rows, indent=1))
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=str(LANE_DEFAULT))
    parser.add_argument("--rev", required=True)
    parser.add_argument("--work", required=True)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--controls", action="store_true")
    parser.add_argument("--freeze-records", action="store_true")
    args = parser.parse_args(argv)
    lane = Path(args.lane).resolve()
    work = Path(args.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    proc = git(lane, "rev-parse", "--verify", "--quiet", f"{args.rev}^{{commit}}")
    if proc.returncode != 0:
        print(f"DEFECT SETUP unresolved-revision {args.rev}")
        print("PREDICATE R89-C2 could-not-evaluate")
        return 2
    rev = proc.stdout.strip()
    if args.freeze_records:
        return freeze_records(lane, rev, work)
    if args.selftest:
        st = selftest_defects(lane, rev, work)
        print(f"DEFECTS n={len(st)}")
        print(f"PREDICATE R89-C2-SELFTEST {'fail' if st else 'pass'}")
        return 1 if st else 0
    if args.controls:
        return controls(lane, rev, work)
    rc, _defects = run_check(lane, rev, work)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
