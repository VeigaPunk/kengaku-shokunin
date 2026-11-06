#!/usr/bin/env python3
"""R99-C2 counter — row-scoped provenance bindings with a symmetric outside-population census (round 99).

Population (claim-local, one rule, derived at BASE and frozen below as POP): a SOURCES row present at
BASE whose `anchor-digest-check` output at BASE is exactly ONE DEFECT line, of class `anchor-unbound`,
with a 64-hex token, and for which at least one file committed under `corpus/evidence/` at BASE has
sha256 equal to that token. The expected capture is the lexicographically first such path. The gate
reports these rows unbound although their digest names committed bytes: their locator is a live URL
the gate cannot map to the capture's directory, or no locator at all.

The change (R99-C2) binds each POP row through the gate's provenance-row rule with NEW
`PROVENANCE.md` files, one per top-level round directory holding a capture
(`corpus/evidence/round<N>/PROVENANCE.md`), each line `| <sid> | `<path relative to that dir>` |
`<sha256>` |` — three columns, NO URL. Round-98 lesson M4 / ReviewC2 F1-F3: a URL column feeds the
gate's `prov_url` fallback and re-binds rows outside the population; this claim closes that channel
by construction (K3) and proves it by a symmetric census (K7). No gate byte, SOURCES row, capture or
existing provenance file changes.

Each revision is checked out in a `git clone --shared` fixture under --work and the BASE bytes of
`plans/anchor_digest_check.py` run there with --verbose (the gate reads SOURCES.md from the work tree
and evidence from HEAD).

Legs (every input read at the revision):
  K1 `plans/anchor_digest_check.py` at --rev hashes to GATE_SHA, and this counter's own bytes at --rev
     hash to the frozen-instruments row for it in the round-99 freeze (the single commit that added
     plans/round-99-claims.md); before that freeze exists the self leg reports `self=unfrozen` and fails
  K2 the population re-derived at BASE by the rule above equals POP (ids, tokens, capture paths)
  K3 every `PROVENANCE.md` under corpus/evidence absent at BASE carries no `://` (no URL channel), and
     every one present at BASE is byte-identical at --rev
  K4 across ALL committed PROVENANCE.md files at --rev, each POP row id appears on exactly ONE table
     line (round-98 MutC2 M11/M16: a second line binding a byte-identical copy), that line lies in
     `corpus/evidence/round<N>/PROVENANCE.md` of the capture's round, its first resolving backticked
     path is the POP capture, and its sha256 column equals both the capture blob's sha256 at --rev
     and the POP token (round-98 MutC2 M05/M18: the sha column was unread)
  K5 at --rev the gate prints no DEFECT line for any POP row, and its verbose notes for the row are
     exactly `BIND <sid> capture=<POP capture> by=provenance-row` (no BIND+) and one `RESOLVED`
  K6 every POP row's SOURCES.md line and every POP capture blob at --rev is byte-identical to BASE
  K7 symmetric census over every row id present at BASE and NOT in POP: its DEFECT lines and its
     verbose notes (BIND, BIND+, UNBOUND, RESOLVED, ABBREV, EXEMPT, CAPTURES, ERRATUM), with the
     `loc=corpus/SOURCES.md:<line>` suffix removed, are EQUAL at BASE and --rev — removals and
     additions both count (round-98 K7 saw only additions)

The first output line is `REV <full hash>`.

Usage:  python3 plans/round99_c2_rowscoped_bind.py --lane <repo> --rev <rev> --work <dir> [--derive]
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

BASE = "2233a66195e3d3d85856248fb8f66c1d8127cede"
GATE = "plans/anchor_digest_check.py"
GATE_SHA = "11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2"
SELF = "plans/round99_c2_rowscoped_bind.py"
CLAIMS = "plans/round-99-claims.md"
SOURCES = "corpus/SOURCES.md"
EVID = "corpus/evidence/"
DEFECT = re.compile(r"^DEFECT (S\d{3,}) \S+ token=(\S+) class=(\S+) detail=(\S+)")
NOTE = re.compile(r"^(BIND|BIND\+|UNBOUND|RESOLVED|ABBREV|EXEMPT|CAPTURES|ERRATUM) (S\d{3,})\b")
LOC = re.compile(r" loc=corpus/SOURCES\.md:\d+")
ROWID = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
LINE_ID = re.compile(r"\b(S\d{3,})\b")
TICKED = re.compile(r"`([^`]+)`")
HEX64 = re.compile(r"[0-9a-f]{64}")
ROWSHA = re.compile(r"^([0-9a-f]{64})  (\S+)$")
ROUND_DIR = re.compile(r"^(corpus/evidence/round\d+)/")
# sid -> (token, capture path); frozen from the BASE derivation (P1 receipt .ufo/waves/round-99/L1/c2-pop.txt)
POP: dict[str, tuple[str, str]] = {
    "S173": ("39ce8d137a30e1fd80eeae146b1c424e56f688f4ddd001259eb98543d3209439", "corpus/evidence/round50/gitrepository-layout.adoc"),
    "S174": ("123096436d7d47b718483fdfbc1660446474a77b2a5b33212f5360af89ca2f95", "corpus/evidence/round50/git-init.adoc"),
    "S175": ("ee8a368564ace74a07e4a034e080b26fb1c3b35d17ef1fe41dcbfcc5595fe8dc", "corpus/evidence/round50/git-worktree.adoc"),
    "S176": ("3f61be3f0ea0426cf1e075929819b9a6bce240c6955cfd25d99fb2c974640631", "corpus/evidence/round50/git-replace.adoc"),
    "S177": ("fd225a09cb7bdb687cff4ba161cb1f337f2523eac5f83db5dbbbb1ef216fa41e", "corpus/evidence/round50/git-fetch.adoc"),
    "S180": ("7dfa9992c45c7e30744cda7ce659ba77309f43120a0990fce033eb8afd972364", "corpus/evidence/round79/sources/tb2-readme.md"),
    "S220": ("58cf3c844e907745cd81fb4bd75efb3d080e2f0e82b589c56c954ae6e1756510", "corpus/evidence/round59/tb2-openssl-selfsigned-cert/solution/solve.sh"),
    "S225": ("2c5fa192d566f92b8b9e6e116255b1f94016b4ece5b9dacb3b98be70b8c60795", "corpus/evidence/round61/whatwg-windows1252/index-windows-1252.txt"),
    "S270": ("d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed", "corpus/evidence/round82/fetch/candidate_pyproject.toml"),
    "S285": ("8b3cf1e2b06074162038064dd2c114abe308acd32cec7d365ee63ee81978f7de", "corpus/evidence/round92/graders/llm-inference-batching-scheduler/environment/task_file/input_data/requests_bucket_1.jsonl"),
    "S293": ("2623000a742c63d50ae1851854826247caee129c7d1613be6c7131d21f26a6ad", "corpus/evidence/round93/graders/schemelike-metacircular-eval/tests/test/01-factorial.scm"),
    "S306": ("abf643683b4870e07500f8a035d1a076d4bf0bbf98eb2fb5180fbc3ef8fad802", "corpus/evidence/round95/graders/fix-code-vulnerability/upstream-bottle/bottle.py"),
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


def frozen_table(root: Path, rev: str) -> dict[str, str]:
    added = [x for x in git(root, "log", "--diff-filter=A", "--format=%H", rev, "--", CLAIMS).stdout.decode().split() if x]
    if len(added) != 1:
        return {}
    rows: dict[str, str] = {}
    inside = False
    for line in (blob(root, added[0], CLAIMS) or b"").decode(errors="replace").splitlines():
        if not inside and line.strip() == "```frozen-instruments":
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
    """({sid: sorted DEFECT lines without loc}, {sid: sorted verbose note lines})."""
    defects: dict[str, list[str]] = {}
    notes: dict[str, list[str]] = {}
    for line in lines:
        m = DEFECT.match(line)
        if m:
            defects.setdefault(m.group(1), []).append(LOC.sub("", line))
            continue
        m = NOTE.match(line)
        if m:
            notes.setdefault(m.group(2), []).append(line)
    return ({k: sorted(v) for k, v in defects.items()}, {k: sorted(v) for k, v in notes.items()})


def row_lines(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        m = ROWID.match(line)
        if m:
            out.setdefault(m.group(1), line)
    return out


def derive(lane: Path, defects: dict[str, list[str]]) -> dict[str, tuple[str, str]]:
    by_sha: dict[str, list[str]] = {}
    for p in ls(lane, BASE, "corpus/evidence"):
        by_sha.setdefault(sha(blob(lane, BASE, p)), []).append(p)
    pop: dict[str, tuple[str, str]] = {}
    for sid, ds in defects.items():
        if len(ds) != 1:
            continue
        m = DEFECT.match(ds[0])
        token, cls = m.group(2), m.group(3)
        if cls != "anchor-unbound" or not HEX64.fullmatch(token) or token not in by_sha:
            continue
        pop[sid] = (token, sorted(by_sha[token])[0])
    return pop


def provenance_lines(lane: Path, rev: str) -> list[tuple[str, str]]:
    """[(provenance file path, table line)] for every committed PROVENANCE.md under corpus/evidence."""
    out = []
    for p in ls(lane, rev, "corpus/evidence"):
        if p.rsplit("/", 1)[-1] != "PROVENANCE.md":
            continue
        for line in (blob(lane, rev, p) or b"").decode("utf-8", "replace").splitlines():
            if "|" in line:
                out.append((p, line))
    return out


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
            print(f"POP {sid} {derived[sid][0]} {derived[sid][1]}")
        print(f"POP_COUNT {len(derived)}")
        return 0
    rev_def, rev_notes = per_sid(run_gate(gate, lane, rev, work / "tree-rev"))
    defects: list[str] = []

    frozen = frozen_table(lane, rev)
    self_sha = sha(blob(lane, rev, SELF))
    k1_gate = sha(blob(lane, rev, GATE)) == GATE_SHA
    k1_self = bool(frozen.get(SELF)) and frozen.get(SELF) == self_sha
    k1 = k1_gate and k1_self
    if not k1:
        defects.append(f"K1 gate_equal={k1_gate} self={'unfrozen' if not frozen.get(SELF) else self_sha[:12] + ' vs frozen ' + frozen[SELF][:12]}")

    k2 = derived == POP
    if not k2:
        defects.append(f"K2 derived={len(derived)} pop={len(POP)} only_derived={sorted(set(derived) - set(POP))} "
                       f"only_pop={sorted(set(POP) - set(derived))} differ={sorted(s for s in POP if s in derived and derived[s] != POP[s])}")

    base_prov = {p for p in ls(lane, BASE, "corpus/evidence") if p.rsplit("/", 1)[-1] == "PROVENANCE.md"}
    rev_prov = {p for p in ls(lane, rev, "corpus/evidence") if p.rsplit("/", 1)[-1] == "PROVENANCE.md"}
    url_files = sorted(p for p in rev_prov - base_prov if b"://" in (blob(lane, rev, p) or b""))
    changed_old = sorted(p for p in base_prov if blob(lane, rev, p) != blob(lane, BASE, p))
    k3 = not url_files and not changed_old
    if not k3:
        defects.append(f"K3 new_provenance_with_url={url_files or '-'} old_provenance_changed={changed_old or '-'}")

    plines = provenance_lines(lane, rev)
    rev_files = set(ls(lane, rev, "corpus/evidence"))
    k4_bad = []
    for sid, (token, cap) in POP.items():
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
    k4 = not k4_bad
    if not k4:
        defects.append("K4 " + " ".join(k4_bad))

    still = sorted((s for s in POP if rev_def.get(s)), key=lambda s: int(s[1:]))
    k5_bad = []
    for sid, (token, cap) in POP.items():
        notes = rev_notes.get(sid, [])
        binds = [n for n in notes if n.startswith("BIND")]
        resolved = [n for n in notes if n.startswith("RESOLVED ")]
        if binds != [f"BIND {sid} capture={cap} by=provenance-row"] or len(resolved) != 1 \
                or not resolved[0].startswith(f"RESOLVED {sid} digest={token} via={cap} "):
            k5_bad.append(sid)
    k5 = not still and not k5_bad
    if not k5:
        defects.append(f"K5 still_defective={','.join(still) or '-'} bind_or_resolve_wrong={','.join(sorted(k5_bad)) or '-'}")

    base_rows = row_lines((blob(lane, BASE, SOURCES) or b"").decode(errors="replace"))
    rev_rows = row_lines((blob(lane, rev, SOURCES) or b"").decode(errors="replace"))
    rows_changed = sorted(s for s in POP if base_rows.get(s) != rev_rows.get(s))
    caps_changed = sorted(s for s, (_, cap) in POP.items() if blob(lane, rev, cap) != blob(lane, BASE, cap))
    k6 = not rows_changed and not caps_changed
    if not k6:
        defects.append(f"K6 rows_changed={rows_changed or '-'} captures_changed={caps_changed or '-'}")

    outside = sorted((s for s in base_rows if s not in POP), key=lambda s: int(s[1:]))
    removed = added = rebound = 0
    moved = []
    for s in outside:
        bd, rd_ = set(base_def.get(s, [])), set(rev_def.get(s, []))
        bn, rn = set(base_notes.get(s, [])), set(rev_notes.get(s, []))
        removed += len(bd - rd_)
        added += len(rd_ - bd)
        if bn != rn:
            rebound += 1
        if bd != rd_ or bn != rn:
            moved.append(s)
    k7 = not moved
    if not k7:
        defects.append(f"K7 outside rows moved={','.join(moved)}")

    cleared = len(POP) - len(still)
    legs = [k1, k2, k3, k4, k5, k6, k7]
    ok = all(legs)
    base_total = sum(len(v) for v in base_def.values())
    rev_total = sum(len(v) for v in rev_def.values())
    print(f"GATE defects base={base_total} rev={rev_total}")
    print("LEGS " + " ".join(f"K{i + 1}={'pass' if v else 'fail'}" for i, v in enumerate(legs)))
    print(f"TARGET pop={len(POP)} cleared={cleared} still={len(still)} outside_rows={len(outside)} "
          f"outside_removed={removed} outside_added={added} outside_rebound={rebound} "
          f"url_channel_files={len(url_files)} rows_changed={len(rows_changed)} captures_changed={len(caps_changed)}")
    for d in defects:
        print("DEFECT " + d)
    print("PREDICATE R99-C2 " + ("pass" if ok else "fail"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except CouldNotEvaluate as error:
        print(f"DEFECT SETUP {error}")
        print("PREDICATE R99-C2 could-not-evaluate")
        sys.exit(2)
