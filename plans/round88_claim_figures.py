#!/usr/bin/env python3
"""R88-C2 counter — Q66 executable half: every frozen before-figure in the claims
corpus is re-derived by its own counter at its own BASE, mechanically.

Population (frozen): `plans/round-8?-claims.md` for rounds 80–87 — the eight
claims files this instrument was written against. For each file the instrument
extracts every before-figure record from the claim text (never hand-copied),
re-runs the claim's counter at the claim's BASE revision, and compares.

Record kinds extracted from claim bytes:
  KV        `key=value` / `key>=value` inside a Before/at-BASE span -> compared
            against the counter's `TARGET` line k=v (exact or lower bound)
  CODE      `<n|number-word> <DEFECT-CODE>` -> compared against the count of
            `DEFECT <CODE>` lines in the counter's output
  DEFTOTAL  `DEFECTS n=<n>` / `DEFECTS n>=<n>` -> compared against the
            `DEFECTS n=` line (exact or lower bound)
  PROSE     a before-span with no machine-checkable figure -> reported, never
            silently dropped

Re-run modes (frozen table CLAIMS below):
  rev   — counter supports `--rev <base>`; every lane read goes through git
          objects at that revision (verified per counter before freeze)
  tree  — counter reads live-lane state (newest spotcheck, exclusions file);
          reproduced by materialising the BASE tree as a fresh repo, overlaying
          the counter bytes from the commit that introduced them, and running
          the counter's frozen argv inside it
  prose — no counter re-run; the before-state is verified by path absence at
          BASE (R82-C3: gate, map and receipt absent)

Predicate (frozen): pass iff every extracted record is checked, every re-run
completed, and the set of mismatched records equals the frozen KNOWN set
exactly — a figure that was wrong when frozen stays wrong on the record, a
figure that was right must still measure right, and any NEW disagreement is a
defect. The known set is named in `plans/round-88-claims.md`.

Usage:  python3 plans/round88_claim_figures.py --lane <repo> --rev <rev> --work <dir>
Exit:   0 predicate pass, 1 at least one defect, 2 could not evaluate.
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

# ---------------------------------------------------------------- frozen table
# claim -> (claims file, counter path, base rev, mode, argv template)
# argv templates use {LANE} {WORK} {BASE}
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
# tree-mode counters: bytes overlaid from the commit that introduced them
TREE_OVERLAY = {
    "plans/round82_c1_plans_registry.py": "82fe89d5dd29fa4c1bb8d85399d9e43442d1b862",
    "plans/round82_c2_closure_debt.py": "82fe89d5dd29fa4c1bb8d85399d9e43442d1b862",
    "plans/round82_c2_checks.py": "82fe89d5dd29fa4c1bb8d85399d9e43442d1b862",
}
# prose-mode absence checks: path -> must be absent at BASE
PROSE_ABSENT = {
    "R82-C3": ["plans/round82_c3_sweep.py", "plans/round82-sweep-map.json",
               "corpus/evidence/round82/sweep.txt"],
}
# the frozen expected mismatch set: (claim, record-key) -> (claimed, measured)
KNOWN = {
    ("R87-C1", "defects"): (7, 3),
}
CLAIMS_FILES = [f"plans/round-{n}-claims.md" for n in range(80, 88)]

# ---------------------------------------------------------------- extraction
# before-markers: 'before'/'Before' (any case, not hyphenated: 'red-before',
# 'before-revision' are not markers) and 'at BASE' (suffix style: figures
# PRECEDE it — 'exit 1 at BASE.'). 'BASE_REV'/'(BASE'/'BASE `' are prose
# references inside 'Before (...)' phrases already covered by 'Before'.
BEFORE_RE = re.compile(r"(?i)(?<!-)\bbefore\b(?!-)|\bat BASE\b")
# end-markers: first hit terminates a before-span so after-figures never leak
SPAN_END_RE = re.compile(r"PREDICATE|\bfail\b|\bpass\b|\bAfter\b|exit 0|measured tip|\*\*After")
# a legitimate before-state always fails: the span must contain a failure marker
FAIL_RE = re.compile(r"fail|exit 1|could-not-evaluate")
# a legitimate before-span quotes counter output — prose 'before'/'after'
# narration never carries these tokens
CONVO_RE = re.compile(r"TARGET |DEFECTS |PREDICATE |located=|executed=|"
                      r"reproduced=|ledger_flipped=|mismatches=|indexed=|"
                      r"state_mismatches=|DEFECT |q\d+=")
KV_RE = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*(=>=|>=|=)\s*(\d+)\b")
DEF_RE = re.compile(r"DEFECTS\s+n\s*(=>=|>=|=)\s*(\d+)")
CODE_RE = re.compile(r"\b(\d+|[a-z]+)\s+`?([A-Z][A-Z0-9][A-Z0-9-]{2,})`?")
# backtick-quoted code-then-number: '`MISSING 4`', '`UNCLASSIFIED 2`'
CODE2_RE = re.compile(r"`([A-Z][A-Z0-9][A-Z0-9-]{2,})\s+(\d+)`")
NUMWORD = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
           "seven": 7, "eight": 8, "nine": 9, "ten": 10}
STOP_CODES = {"PASS", "FAIL", "EXIT", "CASE", "TARGET", "PREDICATE", "DEFECT",
              "DEFECTS", "BASE", "REV", "LANE", "HEAD", "TRUE", "FALSE"}
# id-like tokens that are not defect counts
ID_CODE_RE = re.compile(r"^(R\d+-[A-Z]?\d+|V\d+|S\d+|W\d+)$")


def claim_spans(text: str) -> list[tuple[str, str, str]]:
    """Yield (claim-id, marker-kind, before-span-text) triples.

    Two marker directions exist in the corpus:
      'before'  — figures FOLLOW the marker ('Before (BASE): `TARGET ...`')
      'atbase'  — figures PRECEDE the marker ('`defects=7` ... exit 1 at BASE.')

    Forward spans close at the first end-marker or list/section boundary;
    the FAIL_RE check looks 300 chars past the cut so 'fail`, exit 1' still
    counts. Backward spans open at the last clause boundary (';' / '. ' /
    '.\\n' / paragraph) before the marker and must contain 'exit 1'. Both
    directions require CONVO_RE (counter-output vocabulary) in the span.
    """
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
                # backward: figures precede 'at BASE'
                prefix = body[:mm.start()][-1200:]
                # clause boundary: last ';' / '. ' / '.\n' / blank line / list row
                cuts = [prefix.rfind(";"), prefix.rfind(". "), prefix.rfind(".\n"),
                        prefix.rfind("\n\n"), prefix.rfind("\n- "), prefix.rfind("\n|")]
                boundary = max(cuts)
                span = prefix[boundary + 1:] if boundary >= 0 else prefix
                span = span.strip()
                if "exit 1" not in span or not CONVO_RE.search(span):
                    continue
                spans.append((cid, "atbase", span + " " + marker))
    return spans


def extract_records(claims_path: Path) -> tuple[list[dict], int]:
    """Extract before-figure records from one claims file. Returns (records, prose_count).

    Records are deduplicated on (claim, kind, key, op, claimed): the same
    before-figure restated in a Before bullet and a do-nothing control is one
    record, not two.
    """
    text = claims_path.read_text(encoding="utf-8")
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
        # DEFECTS n bound
        for op, num in DEF_RE.findall(span):
            add({"claim": cid, "kind": "deftotal", "key": "defects",
                 "op": ">=" if op in (">=", "=>=") else "=", "claimed": int(num),
                 "span": span[:160]})
            found = True
        # k=v figures — skip keys that are not counter TARGET outputs
        for key, op, num in KV_RE.findall(span):
            if key in ("n",):  # 'DEFECTS n=' handled above; bare n= is deftotal
                continue
            add({"claim": cid, "kind": "kv", "key": key,
                 "op": ">=" if op in (">=", "=>=") else "=", "claimed": int(num),
                 "span": span[:160]})
            found = True
        # code counts: 'six `DEBT-UNREGISTERED`', 'MISSING 4', 'UNCLASSIFIED 2'
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
        # backtick-quoted code-then-number: '`MISSING 4`', '`UNCLASSIFIED 2`'
        for code, num in CODE2_RE.findall(span):
            code = code.upper().replace("_", "-")
            if code in STOP_CODES or ID_CODE_RE.match(code):
                continue
            add({"claim": cid, "kind": "code", "key": code.lower(),
                 "op": "=", "claimed": int(num), "span": span[:160]})
            found = True
        # 'INDEX-MISSING' / 'indexed=no' prose-code forms
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
    """Materialise BASE tree as a fresh repo, overlay counter bytes, run inside."""
    tree = Path(tempfile.mkdtemp(prefix="q66-tree-", dir=work))
    proc = subprocess.run(["git", "-C", str(lane), "archive", base],
                          capture_output=True, timeout=300)
    if proc.returncode != 0:
        return 2, f"archive-failed {base}"
    import tarfile, io
    with tarfile.open(fileobj=io.BytesIO(proc.stdout)) as tf:
        tf.extractall(tree, filter="data")
    # overlay counter bytes from their introducing commit
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
            # 'indexed=no' appears in TARGET lines; 'index-missing' is a DEFECT code
            if key == "indexed=no":
                found = 1 if re.search(r"(^|\s)indexed=no(\s|$)", output) else 0
            else:
                found = 1 if (key in codes and codes[key] > 0) else 0
            ok = found == claimed
            return ("match" if ok else "mismatch"), f"{key} present={found} claimed {claimed}"
        else:
            measured = codes.get(key, 0)
            ok = measured == claimed
            return ("match" if ok else "mismatch"), f"{key} claimed {claimed} measured {measured}"
    return "unparsed", f"kind {kind}"


def run_check(lane: Path, rev: str, work: Path) -> int:
    defects: list[str] = []
    all_records: list[dict] = []
    prose_total = 0
    # F1: every claims file exists at the measured revision
    for rel in CLAIMS_FILES:
        proc = git(lane, "cat-file", "-e", f"{rev}:{rel}")
        if proc.returncode != 0:
            defects.append(f"F1-corpus {rel} absent at {rev[:12]}")
    # extract from the MEASURED tree's claims bytes (rev), not the worktree
    for rel in CLAIMS_FILES:
        blob = git(lane, "show", f"{rev}:{rel}")
        if blob.returncode != 0:
            continue
        tmp = Path(tempfile.mkdtemp(prefix="q66-claims-", dir=work)) / "claims.md"
        tmp.write_text(blob.stdout)
        records, prose = extract_records(tmp)
        all_records.extend(records)
        prose_total += prose
    # group by claim; EVERY frozen claim's counter runs — a claim whose
    # before-state is pure prose still gets its counter re-run and must exit
    # nonzero at BASE (the before-state fails by construction)
    by_claim: dict[str, list[dict]] = {}
    for rec in all_records:
        by_claim.setdefault(rec["claim"], []).append(rec)
    for cid in CLAIMS:
        by_claim.setdefault(cid, [])
    mismatches: list[tuple[str, str, str, str]] = []
    checked = matched = 0
    outputs: dict[str, tuple[int, str]] = {}
    for cid in sorted(by_claim):
        spec = CLAIMS.get(cid)
        if spec is None:
            defects.append(f"F2-claim {cid} has no frozen counter entry")
            continue
        _file, counter, mode, _argv = spec
        if mode == "prose":
            rc, out = run_prose(lane, cid, BASES[int(cid.split("-")[0][1:])])
            outputs[cid] = (rc, out)
            if rc != 0:
                defects.append(f"F3-prose {cid} {out}")
            continue
        if counter is None:
            defects.append(f"F2-claim {cid} no counter")
            continue
        work_c = work / cid
        work_c.mkdir(parents=True, exist_ok=True)
        base = BASES[int(cid.split("-")[0][1:])]
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
        if "PREDICATE" not in out:
            defects.append(f"F3-nopredicate {cid} rc={rc}")
    # compare every record against its claim's output; a counter-mode claim
    # with zero extracted records must still have failed at BASE
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
                mismatches.append((cid, key, f"claimed={rec['op']}{rec['claimed']}", detail))
            else:
                defects.append(f"F4-unparsed {cid}:{key} {detail}")
    # F5: the mismatch set must equal the frozen KNOWN set exactly.
    # Mismatch keys are 'kind:key' scoped by claim; KNOWN holds (claim, key)
    # pairs for kind='kv' records, normalised here to 'claim:kv:key'.
    measured_pairs = {(cid, key) for cid, key, _c, _d in mismatches}
    known_pairs = {(c, f"kv:{k}") for (c, k) in KNOWN}
    unexpected = measured_pairs - known_pairs
    missing_known = known_pairs - measured_pairs
    for cid, key, claimed, detail in mismatches:
        status = "KNOWN" if (cid, key) in known_pairs else "UNEXPECTED"
        print(f"MISMATCH {status} {cid} {key} {claimed} {detail}")
    for cid, key in sorted(unexpected):
        defects.append(f"F5-unexpected {cid} {key}")
    for cid, key in sorted(missing_known):
        defects.append(f"F5-missing-known {cid} {key}")
    # value check on known mismatches: measured must equal the frozen measured value
    for (cid, key), (claimed_v, measured_v) in KNOWN.items():
        for m_cid, m_key, m_claimed, m_detail in mismatches:
            if m_cid == cid and m_key == f"kv:{key}":
                mm = re.search(r"measured (\d+)", m_detail)
                if mm and int(mm.group(1)) != measured_v:
                    defects.append(f"F5-known-value {cid}:{key} frozen-measured={measured_v} now={mm.group(1)}")
    print(f"RECORDS claims={len(CLAIMS)} files={len(CLAIMS_FILES)} records={len(all_records)} "
          f"checked={checked} matched={matched} mismatches={len(mismatches)} prose={prose_total}")
    for d in defects:
        print(f"DEFECT {d}")
    print(f"DEFECTS n={len(defects)}")
    print(f"TARGET claims={len(CLAIMS)} records={len(all_records)} checked={checked} "
          f"matched={matched} mismatches={len(mismatches)} defects={len(defects)}")
    verdict = "pass" if not defects else "fail"
    print(f"PREDICATE R88-C2 {verdict}")
    return 0 if not defects else 1


def selftest(lane: Path, rev: str, work: Path) -> int:
    """Prove the instrument can fail: doctored claims, marker negatives,
    backward-span direction, dedupe. Each check prints SELFTEST <id> pass|fail.
    """
    defects: list[str] = []

    def check(tid: str, ok: bool, detail: str) -> None:
        print(f"SELFTEST {tid} {'pass' if ok else 'fail'} {detail}")
        if not ok:
            defects.append(tid)

    # T1 doctored claims: flip the frozen R87-C1 before-figure defects=7 -> 9
    # in a scratch copy of the real claims bytes; extraction must yield the
    # doctored claim and the record must MISMATCH the real BASE counter output.
    blob = git(lane, "show", f"{rev}:plans/round-87-claims.md")
    if blob.returncode != 0:
        check("T1-doctored", False, "cannot read round-87 claims at rev")
    else:
        doctored = blob.stdout.replace("defects=7", "defects=9", 1)
        tmp = Path(tempfile.mkdtemp(prefix="q66-selftest-", dir=work)) / "claims.md"
        tmp.write_text(doctored)
        records, _prose = extract_records(tmp)
        kv = [r for r in records if r["kind"] == "kv" and r["key"] == "defects"
              and r["claim"] == "R87-C1"]
        check("T1-doctored-extract", any(r["claimed"] == 9 for r in kv),
              f"records={[(r['key'], r['claimed']) for r in kv]}")
        rc, out = run_rev(lane, "plans/round87_c1_replay.py",
                          BASES[87], work / "T1")
        (work / "T1").mkdir(parents=True, exist_ok=True)
        mism = [r for r in kv if r["claimed"] == 9]
        verdict = check_record(mism[0], out)[0] if mism else "unparsed"
        check("T1-doctored-mismatch", verdict == "mismatch",
              f"verdict={verdict} (doctored figure must not match BASE output)")

    # T2 marker negatives: hyphenated/prose 'before' must not open spans
    neg = ("## R99-C9 fixture\n"
           "The red-before run's failure text is committed.\n"
           "The C2 before-revision is an existing revision (BASE).\n"
           "The receipts are 25 before and 26 after.\n"
           "Universe: section 6 at BASE; no newest-file selection.\n")
    spans = claim_spans(neg)
    check("T2-marker-negatives", len(spans) == 0, f"spans={len(spans)}")

    # T3 backward direction: 'at BASE' takes figures that PRECEDE it
    fwd = ("## R99-C9 fixture\n"
           "**Target.** `defects=7`, `located=0`, `PREDICATE R99-C9 fail`, "
           "exit 1 at BASE.\n")
    spans = claim_spans(fwd)
    ok = (len(spans) == 1 and "defects=7" in spans[0][2]
          and "located=0" in spans[0][2] and "at BASE" in spans[0][2])
    check("T3-atbase-backward", ok, f"spans={spans}")

    # T4 dedupe: the same before-figure stated twice is one record
    dup = ("## R99-C9 fixture\n"
           "- **Before (BASE):** `TARGET defects=7 located=0`, "
           "`PREDICATE R99-C9 fail`, exit 1.\n"
           "- **Do-nothing control:** the counter at BASE must report "
           "`defects=7` (exit 1).\n")
    tmp = Path(tempfile.mkdtemp(prefix="q66-selftest-", dir=work)) / "dup.md"
    tmp.write_text(dup)
    records, _prose = extract_records(tmp)
    d7 = [r for r in records if r["kind"] == "kv" and r["key"] == "defects"
          and r["claimed"] == 7]
    check("T4-dedupe", len(d7) == 1, f"defects=7 records={len(d7)}")

    print(f"DEFECTS n={len(defects)}")
    print(f"PREDICATE R88-C2-SELFTEST {'fail' if defects else 'pass'}")
    return 1 if defects else 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=str(LANE_DEFAULT))
    parser.add_argument("--rev", required=True)
    parser.add_argument("--work", required=True)
    parser.add_argument("--selftest", action="store_true",
                        help="run the able-to-fail fixture battery instead of the corpus check")
    args = parser.parse_args(argv)
    lane = Path(args.lane).resolve()
    work = Path(args.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    proc = git(lane, "rev-parse", "--verify", "--quiet", f"{args.rev}^{{commit}}")
    if proc.returncode != 0:
        print(f"DEFECT SETUP unresolved-revision {args.rev}")
        print("PREDICATE R88-C2 could-not-evaluate")
        return 2
    if args.selftest:
        return selftest(lane, proc.stdout.strip(), work)
    return run_check(lane, proc.stdout.strip(), work)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
