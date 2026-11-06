#!/usr/bin/env python3
"""R100-C2 counter — path-matched provenance bindings for wrongly bound TB2 grader rows, with a
row-level census, a three-cell line contract and a live re-fetch receipt (round 100).

Successor of plans/round99_c2_rowscoped_bind.py (not edited, Q79). Round-99 routed defects 3 and 4:
K7 there was finding-level only (CriticClaims F6/F7, MutC2 M17: deleting an outside row with no gate
output passed); a fabricated id (M08) and a fourth column (M11/M12) passed.

Population (claim-local, one rule, derived at BASE and frozen below as POP): a SOURCES row present at
BASE such that
  (a) the BASE gate prints a DEFECT line for it of class `digest-wrong-capture` or `anchor-unbound`
      whose token T is 64 hex;
  (b) the row's first pinned Terminal-Bench 2.0 raw URL is
      `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/<commit>/<task>/<rel>`;
  (c) a file committed under `corpus/evidence/` at BASE has sha256 T and its path ends with
      `/<task>/<rel>` or `/tb2-<task>/<rel>` (the capture IS the upstream file the row names —
      ConnectorOverlap r99 CO-11 risk 2: a token that equals a DIFFERENT file's bytes, as S298's
      `tests/original-decomp.c` row carrying `environment/decomp.c`'s digest, is not bound);
  (d) no committed PROVENANCE.md at BASE names the row id.
The expected capture is the lexicographically first such path. (S300 enters on its full 64-hex
`01550b7d…` token only; its other two findings are outside this claim and must not move — K5.)

The change binds each POP row through the gate's provenance-row rule with NEW three-column
`corpus/evidence/round<N>/PROVENANCE.md` files (row, file here, sha256; no URL), built by
`plans/round100_provenance_build.py`. No gate byte, SOURCES row, capture or existing provenance file
changes.

Each revision is checked out in a `git clone --shared` fixture under --work and the BASE bytes of
`plans/anchor_digest_check.py` run there with --verbose.

Legs (every input read at the revision):
  K1  `plans/anchor_digest_check.py` at --rev hashes to GATE_SHA, and this counter's own bytes at --rev
      hash to the frozen-instruments row for it in the round-100 freeze (the single commit that added
      plans/round-100-claims.md); before that freeze exists the self leg fails
  K2  the population re-derived at BASE by the rule above equals POP (ids, tokens, capture paths)
  K3  every PROVENANCE.md absent at BASE carries no `://`, and every one of its table lines (a line
      starting with `|`, header and separator excluded) has EXACTLY three cells; every PROVENANCE.md
      present at BASE is byte-identical at --rev
  K4  across ALL committed PROVENANCE.md files at --rev, each POP id appears on exactly ONE table line,
      in `corpus/evidence/round<N>/PROVENANCE.md` of the capture's round, whose first resolving
      backticked path is the POP capture and whose sha column equals the capture blob's sha256 at
      --rev and the POP token; and every row id named in a PROVENANCE.md absent at BASE is a POP id
      (no fabricated or extra id — MutC2 M08)
  K5  at --rev the gate prints no DEFECT line carrying a POP row's POP token; the row's verbose notes
      are exactly `BIND <sid> capture=<POP capture> by=provenance-row` and one
      `RESOLVED <sid> digest=<POP token> via=<POP capture> …`; and the TOKEN SET of the row's OTHER
      DEFECT lines is equal at REF and --rev (none cleared, none added; a class that sharpens once the
      row is bound is printed `RECLASS …` — amendment 1, S300 `fa53d657`)
  K6  every POP row's SOURCES.md line and every POP capture blob at --rev is byte-identical to BASE
  K7  symmetric finding-level census over every row id present at BASE and NOT in POP: DEFECT lines
      and verbose notes (loc removed) EQUAL at REF and --rev

REF (amendment 1, before the freeze) is the freeze commit's parent: the last pre-freeze tree, which
already holds this round's P0 capture. That capture re-binds outside row S295 (a round-93 rejection of
this very member) by url-task and clears its finding (gate 33 -> 32 at P1); C2 neither makes nor owns
that change, so its censuses start from REF, printed as `REF <hash>`. Without a freeze K7 fails.
  K8  row-level census: every SOURCES row line present at BASE is present and byte-identical at --rev
      (deletions and rewrites of rows that carry no gate output now fail — CriticClaims F6/F7)
  K9  the live re-fetch receipt LIVE (committed before the freeze, its sha in the frozen table) has
      exactly one `LIVE <sid> http=200 bytes=<n> sha256=<hex> url=<url>` line per POP id and no other
      id; each sha256 equals the POP token and each url is the row's pinned URL (the upstream file
      was re-opened this round and still hashes to the row's digest)
  K10 file set: every path that differs between the freeze commit F and --rev is in the frozen
      `candidate-bytes` table or is the C1 probe receipt, and every C2-owned candidate (the new
      PROVENANCE.md files) differs F..rev and hashes at --rev to its table sha

The first output line is `REV <full hash>`.

Usage:  python3 plans/round100_c2_rowcensus_bind.py --lane <repo> --rev <rev> --work <dir> [--derive]
Exit:   0 predicate pass, 1 a leg failed, 2 could-not-evaluate.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

BASE = "7846037679de77d050141c785996471801e5a19a"
GATE = "plans/anchor_digest_check.py"
GATE_SHA = "11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2"
SELF = "plans/round100_c2_rowcensus_bind.py"
CLAIMS = "plans/round-100-claims.md"
SOURCES = "corpus/SOURCES.md"
LIVE = ".ufo/waves/round-100/L1/c2-live-refetch.txt"
C1_RECEIPT = "corpus/evidence/round100/fdp-probe.txt"
DEFECT = re.compile(r"^DEFECT (S\d{3,}) \S+ token=(\S+) class=(\S+) detail=(\S+)")
NOTE = re.compile(r"^(BIND|BIND\+|UNBOUND|RESOLVED|ABBREV|EXEMPT|CAPTURES|ERRATUM) (S\d{3,})\b")
LOC = re.compile(r" loc=corpus/SOURCES\.md:\d+")
ROWID = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
LINE_ID = re.compile(r"\b(S\d{3,})\b")
TICKED = re.compile(r"`([^`]+)`")
HEX64 = re.compile(r"[0-9a-f]{64}")
ROWSHA = re.compile(r"^([0-9a-f]{64})  (\S+)$")
ROUND_DIR = re.compile(r"^(corpus/evidence/round\d+)/")
TB2_URL = re.compile(r"https://raw\.githubusercontent\.com/harbor-framework/terminal-bench-2/([0-9a-f]{40})/"
                     r"([A-Za-z0-9_.-]+)/([A-Za-z0-9_./-]*[A-Za-z0-9_-])")
LIVE_LINE = re.compile(r"^LIVE (S\d{3,}) http=(\d+) bytes=(\d+) sha256=([0-9a-f]{64}) url=(\S+)$")
OWN_CLASSES = ("digest-wrong-capture", "anchor-unbound")
# sid -> (token, capture path, pinned url); frozen from the BASE derivation (P1 receipt .ufo/waves/round-100/L1/c2-pop.txt)
POP: dict[str, tuple[str, str, str]] = {
    "S210": ("02bca54db4849b7c911253fb92f941e21db8b1eea13261a7e5a9871fca68b4ed",
             "corpus/evidence/round52/graders/distribution-search/tests/test_outputs.py",
             "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/distribution-search/tests/test_outputs.py"),
    "S211": ("19daaee18d534f36679854b0ba5727290df389ee023ebb67846cb89579d38bbe",
             "corpus/evidence/round58/tb2-distribution-search/solution/solve.sh",
             "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/distribution-search/solution/solve.sh"),
    "S219": ("90970bb3c372e8e7fb6bb9ac5f649ba73eb38e1a5ea2e922a9057a72b6b4192d",
             "corpus/evidence/round52/graders/openssl-selfsigned-cert/tests/test_outputs.py",
             "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/openssl-selfsigned-cert/tests/test_outputs.py"),
    "S228": ("82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c",
             "corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py",
             "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/pypi-server/tests/test_outputs.py"),
    "S232": ("b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b",
             "corpus/evidence/round52/graders/sqlite-with-gcov/tests/test_outputs.py",
             "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sqlite-with-gcov/tests/test_outputs.py"),
    "S279": ("2754ba6c5c5f75c9db5ed2c5729d9f5d7e21cb7fdb18aa0c65abdc3e7e85c149",
             "corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py",
             "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/merge-diff-arc-agi-task/tests/test_outputs.py"),
    "S281": ("0c24195ff46527764c7f8ceda9c608a189ab4a01619282942fcd27a2ea02a977",
             "corpus/evidence/round52/graders/modernize-scientific-stack/tests/test_outputs.py",
             "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/modernize-scientific-stack/tests/test_outputs.py"),
    "S298": ("7f8d9ef66943f912a217aa48f4ef5efc967b44c2b21d0f56df029b5ab413f62a",
             "corpus/evidence/round94/graders/write-compressor/tests/original-decomp.c",
             "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/write-compressor/tests/original-decomp.c"),
    "S300": ("01550b7de7ab1320b1898eae055226bb7c73bee259c75102d2240c974a730409",
             "corpus/evidence/round94/graders/write-compressor/solution/solve.sh",
             "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/write-compressor/solution/solve.sh"),
}


class CouldNotEvaluate(Exception):
    pass


def git(root: Path, *args: str, timeout: int = 300) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=timeout)


def blob(root: Path, rev: str, path: str) -> bytes | None:
    proc = git(root, "show", f"{rev}:{path}")
    return proc.stdout if proc.returncode == 0 else None


def sha(data: bytes | None) -> str:
    return hashlib.sha256(data).hexdigest() if data is not None else "absent"


def ls(root: Path, rev: str, prefix: str) -> list[str]:
    out = git(root, "ls-tree", "-r", "--name-only", rev, prefix)
    if out.returncode != 0:
        raise CouldNotEvaluate(f"ls-tree {rev} failed")
    return [p for p in out.stdout.decode(errors="surrogateescape").splitlines() if p]


def freeze_commit(root: Path, rev: str) -> str | None:
    added = [x for x in git(root, "log", "--diff-filter=A", "--format=%H", rev, "--", CLAIMS).stdout.decode().split() if x]
    return added[0] if len(added) == 1 else None


def fenced(root: Path, commit: str | None, name: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    if not commit:
        return rows
    inside = False
    for line in (blob(root, commit, CLAIMS) or b"").decode(errors="replace").splitlines():
        if not inside and line.strip() == "```" + name:
            inside = True
            continue
        if inside and line.strip() == "```":
            break
        m = ROWSHA.match(line.strip()) if inside else None
        if m:
            rows[m.group(2)] = m.group(1)
    return rows


def checkout(lane: Path, rev: str, dest: Path) -> Path:
    if dest.exists():
        shutil.rmtree(dest)
    proc = subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", str(lane), str(dest)],
                          capture_output=True, timeout=300)
    if proc.returncode != 0:
        raise CouldNotEvaluate(f"clone failed {proc.stderr.decode(errors='replace')[-200:]}")
    if git(dest, "-c", "advice.detachedHead=false", "checkout", "-q", rev).returncode != 0:
        raise CouldNotEvaluate(f"checkout {rev} failed")
    if git(dest, "rev-parse", "--show-toplevel").stdout.decode().strip() != str(dest):
        raise CouldNotEvaluate(f"fixture toplevel is not {dest}")
    return dest


def run_gate(gate: Path, lane: Path, rev: str, dest: Path) -> list[str]:
    tree = checkout(lane, rev, dest)
    try:
        proc = subprocess.run([sys.executable, "-I", "-B", str(gate), "--lane", str(tree), "--verbose"],
                              capture_output=True, text=True, timeout=1200, cwd=str(tree))
    finally:
        shutil.rmtree(tree, ignore_errors=True)
    if proc.returncode not in (0, 1):
        raise CouldNotEvaluate(f"gate rc={proc.returncode} {proc.stderr.strip()[-200:]}")
    return proc.stdout.splitlines()


def per_sid(lines: list[str]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """({sid: sorted DEFECT lines without loc}, {sid: sorted verbose note lines without loc})."""
    defects: dict[str, list[str]] = {}
    notes: dict[str, list[str]] = {}
    for line in lines:
        m = DEFECT.match(line)
        if m:
            defects.setdefault(m.group(1), []).append(LOC.sub("", line))
            continue
        m = NOTE.match(line)
        if m:
            notes.setdefault(m.group(2), []).append(LOC.sub("", line))
    return ({k: sorted(v) for k, v in defects.items()}, {k: sorted(v) for k, v in notes.items()})


def row_lines(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        m = ROWID.match(line)
        if m:
            out.setdefault(m.group(1), line)
    return out


def provenance_files(lane: Path, rev: str) -> list[str]:
    return [p for p in ls(lane, rev, "corpus/evidence") if p.rsplit("/", 1)[-1] == "PROVENANCE.md"]


def table_lines(text: str) -> list[str]:
    """Data lines of every markdown table (header and separator rows excluded)."""
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells) or cells[:1] == ["row"]:
            continue
        out.append(line)
    return out


def derive(lane: Path, defects: dict[str, list[str]]) -> dict[str, tuple[str, str, str]]:
    by_sha: dict[str, list[str]] = {}
    for p in ls(lane, BASE, "corpus/evidence"):
        by_sha.setdefault(sha(blob(lane, BASE, p)), []).append(p)
    named = set()
    for p in provenance_files(lane, BASE):
        for line in table_lines((blob(lane, BASE, p) or b"").decode("utf-8", "replace")):
            named.update(LINE_ID.findall(line))
    rows = row_lines((blob(lane, BASE, SOURCES) or b"").decode(errors="replace"))
    pop: dict[str, tuple[str, str, str]] = {}
    for sid, ds in defects.items():
        if sid in named or sid not in rows:
            continue
        m_url = TB2_URL.search(rows[sid])
        if not m_url:
            continue
        task, rel = m_url.group(2), m_url.group(3)
        for d in ds:
            m = DEFECT.match(d)
            token, cls = m.group(2), m.group(3)
            if cls not in OWN_CLASSES or not HEX64.fullmatch(token):
                continue
            paths = sorted(p for p in by_sha.get(token, [])
                           if p.endswith(f"/{task}/{rel}") or p.endswith(f"/tb2-{task}/{rel}"))
            if paths:
                pop[sid] = (token, paths[0], m_url.group(0))
                break
    return pop


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--work", required=True)
    ap.add_argument("--derive", action="store_true", help="print the BASE population and exit (P1 only)")
    a = ap.parse_args(argv)
    lane = Path(a.lane).resolve()
    if Path.cwd().resolve() != lane:
        raise CouldNotEvaluate(f"cwd {Path.cwd().resolve()} is not the lane root {lane}")
    work = Path(a.work).resolve()
    if work == lane or lane in work.parents:
        raise CouldNotEvaluate(f"--work inside the lane {work}")
    work.mkdir(parents=True, exist_ok=True)
    proc = git(lane, "rev-parse", "--verify", "--quiet", f"{a.rev}^{{commit}}")
    if proc.returncode != 0:
        raise CouldNotEvaluate(f"unresolved-revision {a.rev}")
    rev = proc.stdout.decode().strip()
    print(f"REV {rev}")
    gate_base = blob(lane, BASE, GATE)
    if gate_base is None or sha(gate_base) != GATE_SHA:
        raise CouldNotEvaluate("BASE gate bytes absent or not GATE_SHA")
    gate = work / "gate-base.py"
    gate.write_bytes(gate_base)

    base_def, base_notes = per_sid(run_gate(gate, lane, BASE, work / "tree-base"))
    derived = derive(lane, base_def)
    if a.derive:
        for sid in sorted(derived, key=lambda s: int(s[1:])):
            print(f"POP {sid} {derived[sid][0]} {derived[sid][1]} {derived[sid][2]}")
        print(f"POP_COUNT {len(derived)}")
        return 0
    rev_def, rev_notes = per_sid(run_gate(gate, lane, rev, work / "tree-rev"))
    defects: list[str] = []

    fcommit = freeze_commit(lane, rev)
    frozen = fenced(lane, fcommit, "frozen-instruments")
    candidates = fenced(lane, fcommit, "candidate-bytes")
    # census reference (amendment 1): the freeze commit's parent, i.e. the last pre-freeze tree, which
    # already holds this round's P0/P1 bytes; C1's P0 capture re-binds outside row S295 by url-task
    # (33 -> 32 at P1, controls dry run), a change C2 neither makes nor may be blamed for
    ref_proc = git(lane, "rev-parse", "--verify", "--quiet", f"{fcommit}~1") if fcommit else None
    if ref_proc is None or ref_proc.returncode != 0:
        ref = BASE
        defects.append("K7 no freeze commit: census reference falls back to BASE")
    else:
        ref = ref_proc.stdout.decode().strip()
    print(f"REF {ref}")
    ref_def, ref_notes = (base_def, base_notes) if ref == BASE else per_sid(run_gate(gate, lane, ref, work / "tree-ref"))
    self_sha = sha(blob(lane, rev, SELF))
    k1_gate = sha(blob(lane, rev, GATE)) == GATE_SHA
    k1_self = bool(frozen.get(SELF)) and frozen.get(SELF) == self_sha
    k1 = k1_gate and k1_self
    if not k1:
        defects.append(f"K1 gate_equal={k1_gate} self={'unfrozen' if not frozen.get(SELF) else self_sha[:12] + ' vs frozen ' + frozen[SELF][:12]}")

    k2 = bool(POP) and derived == POP
    if not k2:
        defects.append(f"K2 derived={len(derived)} pop={len(POP)} only_derived={sorted(set(derived) - set(POP))} "
                       f"only_pop={sorted(set(POP) - set(derived))} differ={sorted(s for s in POP if s in derived and derived[s] != POP[s])}")

    base_prov = set(provenance_files(lane, BASE))
    rev_prov = set(provenance_files(lane, rev))
    new_prov = sorted(rev_prov - base_prov)
    url_files = sorted(p for p in new_prov if b"://" in (blob(lane, rev, p) or b""))
    bad_cells = []
    new_ids: set[str] = set()
    for p in new_prov:
        for line in table_lines((blob(lane, rev, p) or b"").decode("utf-8", "replace")):
            new_ids.update(LINE_ID.findall(line))
            if len(line.strip().strip("|").split("|")) != 3:
                bad_cells.append(p)
    changed_old = sorted(p for p in base_prov if blob(lane, rev, p) != blob(lane, BASE, p))
    k3 = not url_files and not changed_old and not bad_cells
    if not k3:
        defects.append(f"K3 new_provenance_with_url={url_files or '-'} not_three_cells={sorted(set(bad_cells)) or '-'} "
                       f"old_provenance_changed={changed_old or '-'}")

    plines = [(p, line) for p in sorted(rev_prov)
              for line in table_lines((blob(lane, rev, p) or b"").decode("utf-8", "replace"))]
    rev_files = set(ls(lane, rev, "corpus/evidence"))
    k4_bad = []
    for sid, (token, cap, _url) in POP.items():
        hits = [(p, line) for p, line in plines if sid in LINE_ID.findall(line)]
        if len(hits) != 1:
            k4_bad.append(f"{sid}:lines={len(hits)}")
            continue
        p, line = hits[0]
        d = p.rsplit("/", 1)[0]
        rd = ROUND_DIR.match(cap)
        if not rd or d != rd.group(1):
            k4_bad.append(f"{sid}:file={p}")
            continue
        cands = []
        for t in TICKED.findall(line):
            rel = t.strip()
            while rel.startswith("./"):
                rel = rel[2:]
            if rel and "://" not in rel and f"{d}/{rel}" in rev_files:
                cands.append(f"{d}/{rel}")
        shas = [t for t in TICKED.findall(line) if HEX64.fullmatch(t.strip())]
        cap_sha = sha(blob(lane, rev, cap))
        if not cands or cands[0] != cap:
            k4_bad.append(f"{sid}:binds={cands[0] if cands else '-'}")
        elif shas != [token] or cap_sha != token:
            k4_bad.append(f"{sid}:sha_col={shas} capture={cap_sha[:12]}")
    extra_ids = sorted(new_ids - set(POP), key=lambda s: int(s[1:]))
    if extra_ids:
        k4_bad.append(f"ids_not_in_pop={','.join(extra_ids)}")
    k4 = bool(POP) and not k4_bad
    if not k4:
        defects.append("K4 " + (" ".join(k4_bad) or "empty-pop"))

    still = sorted((s for s, (token, _c, _u) in POP.items()
                    if any(DEFECT.match(x).group(2) == token for x in rev_def.get(s, []))), key=lambda s: int(s[1:]))
    k5_bad = []
    for sid, (token, cap, _url) in POP.items():
        notes = rev_notes.get(sid, [])
        binds = [n for n in notes if n.startswith("BIND")]
        resolved = [n for n in notes if n.startswith("RESOLVED ")]
        # amendment 1: the row's OTHER findings keep their token set (none cleared, none added); a class
        # may sharpen once the row is bound (S300 fa53d657: anchor-unbound -> abbrev-unresolved)
        other_ref = sorted(DEFECT.match(x).group(2) for x in ref_def.get(sid, []) if DEFECT.match(x).group(2) != token)
        other_rev = sorted(DEFECT.match(x).group(2) for x in rev_def.get(sid, []) if DEFECT.match(x).group(2) != token)
        for x in rev_def.get(sid, []):
            if DEFECT.match(x).group(2) != token and x not in ref_def.get(sid, []):
                print(f"RECLASS {x}")
        if binds != [f"BIND {sid} capture={cap} by=provenance-row"] or len(resolved) != 1 \
                or not resolved[0].startswith(f"RESOLVED {sid} digest={token} via={cap} ") \
                or other_ref != other_rev:
            k5_bad.append(sid)
    k5 = bool(POP) and not still and not k5_bad
    if not k5:
        defects.append(f"K5 still_defective={','.join(still) or '-'} bind_resolve_or_other_wrong={','.join(sorted(k5_bad)) or '-'}")

    base_rows = row_lines((blob(lane, BASE, SOURCES) or b"").decode(errors="replace"))
    rev_rows = row_lines((blob(lane, rev, SOURCES) or b"").decode(errors="replace"))
    rows_changed = sorted(s for s in POP if base_rows.get(s) != rev_rows.get(s))
    caps_changed = sorted(s for s, (_, cap, _u) in POP.items() if blob(lane, rev, cap) != blob(lane, BASE, cap))
    k6 = not rows_changed and not caps_changed
    if not k6:
        defects.append(f"K6 rows_changed={rows_changed or '-'} captures_changed={caps_changed or '-'}")

    outside = sorted((s for s in base_rows if s not in POP), key=lambda s: int(s[1:]))
    removed = added = rebound = 0
    moved = []
    for s in outside:
        bd, rd_ = set(ref_def.get(s, [])), set(rev_def.get(s, []))
        bn, rn = set(ref_notes.get(s, [])), set(rev_notes.get(s, []))
        removed += len(bd - rd_)
        added += len(rd_ - bd)
        if bn != rn:
            rebound += 1
        if bd != rd_ or bn != rn:
            moved.append(s)
    k7 = not moved and bool(fcommit)
    if moved:
        defects.append(f"K7 outside rows moved={','.join(moved)}")

    base_set = set(base_rows.values())
    rev_set_lines = set((blob(lane, rev, SOURCES) or b"").decode(errors="replace").splitlines())
    row_missing = sorted((s for s, line in base_rows.items() if line not in rev_set_lines), key=lambda s: int(s[1:]))
    k8 = bool(base_set) and not row_missing
    if not k8:
        defects.append(f"K8 base_rows_not_byte_equal={','.join(row_missing)}")

    live_bytes = blob(lane, rev, LIVE)
    live_ok = bool(frozen.get(LIVE)) and sha(live_bytes) == frozen.get(LIVE)
    live: dict[str, list[tuple[str, str, str, str]]] = {}
    for line in (live_bytes or b"").decode(errors="replace").splitlines():
        m = LIVE_LINE.match(line)
        if m:
            live.setdefault(m.group(1), []).append((m.group(2), m.group(3), m.group(4), m.group(5)))
    live_bad = [s for s, (token, _c, url) in POP.items()
                if len(live.get(s, [])) != 1 or live[s][0][0] != "200" or live[s][0][2] != token or live[s][0][3] != url]
    live_extra = sorted(set(live) - set(POP))
    k9 = bool(POP) and live_ok and not live_bad and not live_extra
    if not k9:
        defects.append(f"K9 receipt_frozen={live_ok} bad={','.join(sorted(live_bad)) or '-'} extra={','.join(live_extra) or '-'}")

    if fcommit:
        diff = git(lane, "diff", "--name-only", "--no-renames", fcommit, rev)
        changed = set(diff.stdout.decode().split()) if diff.returncode == 0 else {"<diff-failed>"}
    else:
        changed = {"<no-freeze>"}
    outside_table = sorted(p for p in changed if p not in candidates and p != C1_RECEIPT)
    own = [p for p in new_prov]
    own_bad = sorted(p for p in own if p not in changed or candidates.get(p) != sha(blob(lane, rev, p)))
    k10 = bool(fcommit) and bool(own) and not outside_table and not own_bad
    if not k10:
        defects.append(f"K10 freeze={'yes' if fcommit else 'absent'} outside_table={outside_table or '-'} own_unbound={own_bad or ('-' if own else 'none')}")

    cleared = len(POP) - len(still)
    legs = [k1, k2, k3, k4, k5, k6, k7, k8, k9, k10]
    ok = all(legs)
    base_total = sum(len(v) for v in base_def.values())
    rev_total = sum(len(v) for v in rev_def.values())
    ref_total = sum(len(v) for v in ref_def.values())
    print(f"GATE defects base={base_total} ref={ref_total} rev={rev_total}")
    print("LEGS " + " ".join(f"K{i + 1}={'pass' if v else 'fail'}" for i, v in enumerate(legs)))
    print(f"TARGET pop={len(POP)} cleared={cleared} still={len(still)} outside_rows={len(outside)} "
          f"outside_removed={removed} outside_added={added} outside_rebound={rebound} "
          f"base_rows={len(base_rows)} base_rows_not_equal={len(row_missing)} "
          f"new_provenance_files={len(new_prov)} url_channel_files={len(url_files)} not_three_cells={len(set(bad_cells))} "
          f"ids_not_in_pop={len(extra_ids)} live_rows={len(live)} rows_changed={len(rows_changed)} captures_changed={len(caps_changed)}")
    for d in defects:
        print("DEFECT " + d)
    print("PREDICATE R100-C2 " + ("pass" if ok else "fail"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except CouldNotEvaluate as error:
        print(f"DEFECT SETUP {error}")
        print("PREDICATE R100-C2 could-not-evaluate")
        sys.exit(2)
