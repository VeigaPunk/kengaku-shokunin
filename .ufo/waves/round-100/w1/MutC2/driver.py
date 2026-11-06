#!/usr/bin/env python3
"""R100-C2 mutation driver (MutC2). One mutant per invocation.

Builds a fixture clone of the lane at T under $S/mut/<id>, rewrites the claims file so that the
freeze commit F' is a fixture-only commit whose parent is P2 (the counter's REF) and whose tree is
the mutant tree minus the new PROVENANCE.md files (so F'..rev is exactly the C2 candidate bytes),
then runs plans/round100_c2_rowcensus_bind.py from the fixture root.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
T = "dbe0cefa607cf57f7f58346fce64bcc127144ca0"
P2 = "5220b71d337a3703eaba4cdf6b85eaf343497ae0"
ROOT = Path("/fast/scratch/hyaku/kengaku-r100/MutC2")
SELF = "plans/round100_c2_rowcensus_bind.py"
CLAIMS = "plans/round-100-claims.md"
C1_RECEIPT = "corpus/evidence/round100/fdp-probe.txt"
ROWSHA = re.compile(r"^([0-9a-f]{64})  (\S+)$")
FROZEN_BLOCK = "frozen-instruments"
CAND_BLOCK = "candidate-bytes"

# ---------------------------------------------------------------- mutant table
# kind: counter = single-point edit of the counter; tree = single-point edit of the fixture tree.
# expect: the leg(s) the mutation is aimed at.
MUTANTS: dict[str, dict] = {}


def M(mid, kind, expect, desc, **kw):
    MUTANTS[mid] = dict(id=mid, kind=kind, expect=expect, desc=desc, **kw)


# ---- no-op positive control: the same fixture construction with no mutation
M("M00", "tree", "PASS", "no-op control (fixture harness itself)", tree="none", expect_pass=True)

# ---- counter mutants (single-point edits of plans/round100_c2_rowcensus_bind.py)
M("C01", "counter", "K2", "derive: OWN_CLASSES drops anchor-unbound",
  old='OWN_CLASSES = ("digest-wrong-capture", "anchor-unbound")',
  new='OWN_CLASSES = ("digest-wrong-capture",)')
M("C02", "counter", "K2", "derive: capture suffix drops the rel component",
  old='if p.endswith(f"/{task}/{rel}") or p.endswith(f"/tb2-{task}/{rel}")',
  new='if p.endswith(f"/{task}/") or p.endswith(f"/tb2-{task}/")')
M("C03", "counter", "K2", "derive: drop the BASE-provenance 'named' exclusion",
  old="if sid in named or sid not in rows:", new="if sid not in rows:")
M("C04", "counter", "K2", "derive: last capture path instead of lexicographically first",
  old="pop[sid] = (token, paths[0], m_url.group(0))",
  new="pop[sid] = (token, paths[-1], m_url.group(0))")
M("C05", "counter", "K2", "derive: drop the 64-hex token requirement",
  old="if cls not in OWN_CLASSES or not HEX64.fullmatch(token):",
  new="if cls not in OWN_CLASSES:")
M("C06", "counter", "K2", "derive: TB2 URL regex names another repo",
  old="terminal-bench-2/([0-9a-f]{40})", new="terminal-bench-9/([0-9a-f]{40})")
M("C07", "counter", "K2", "derive: task used as rel in the capture suffix",
  old="task, rel = m_url.group(2), m_url.group(3)",
  new="task, rel = m_url.group(2), m_url.group(2)")
M("C08", "counter", "K3", "K3: cell count accepts four cells",
  old='if len(line.strip().strip("|").split("|")) != 3:',
  new='if len(line.strip().strip("|").split("|")) not in (3, 4):')
M("C09", "counter", "K3", "K3: no :// scan of new provenance files",
  old='url_files = sorted(p for p in new_prov if b"://" in (blob(lane, rev, p) or b""))',
  new="url_files = []")
M("C10", "counter", "K3", "K3: BASE provenance files may change",
  old="changed_old = sorted(p for p in base_prov if blob(lane, rev, p) != blob(lane, BASE, p))",
  new="changed_old = []")
M("C11", "counter", "K4", "K4: a POP id may appear on zero or many lines",
  old="if len(hits) != 1:", new="if len(hits) < 1:")
M("C12", "counter", "K4", "K4: binding file need not be the capture's round",
  old="if not rd or d != rd.group(1):", new="if not rd:")
M("C13", "counter", "K4", "K4: first ticked path need not be the POP capture",
  old="if not cands or cands[0] != cap:", new="if not cands:")
M("C14", "counter", "K4", "K4: capture blob sha not compared to the token",
  old="elif shas != [token] or cap_sha != token:", new="elif shas != [token]:")
M("C15", "counter", "K4", "K4: extra sha cells tolerated (token membership only)",
  old="elif shas != [token] or cap_sha != token:",
  new="elif token not in shas or cap_sha != token:")
M("C16", "counter", "K4", "K4: fabricated ids in new provenance files tolerated",
  old="extra_ids = sorted(new_ids - set(POP), key=lambda s: int(s[1:]))",
  new="extra_ids = []")
M("C17", "counter", "K5", "K5: any BIND line accepted, capture not compared",
  old='if binds != [f"BIND {sid} capture={cap} by=provenance-row"] or len(resolved) != 1 \\',
  new="if not binds or len(resolved) != 1 \\")
M("C18", "counter", "K5", "K5: other-finding token SET relaxed to its cardinality",
  old="or other_ref != other_rev:", new="or len(other_ref) != len(other_rev):")
M("C19", "counter", "K5", "K5: a POP row may stay defective",
  old='    still = sorted((s for s, (token, _c, _u) in POP.items()\n'
      '                    if any(DEFECT.match(x).group(2) == token for x in rev_def.get(s, []))), key=lambda s: int(s[1:]))',
  new="    still = []")
M("C20", "counter", "K6", "K6: POP captures may change",
  old="caps_changed = sorted(s for s, (_, cap, _u) in POP.items() if blob(lane, rev, cap) != blob(lane, BASE, cap))",
  new="caps_changed = []")
M("C21", "counter", "K7", "K7: outside-row notes ignored, DEFECT lines only",
  old="if bd != rd_ or bn != rn:", new="if bd != rd_:")
M("C22", "counter", "K8", "K8: BASE row byte equality not checked",
  old="row_missing = sorted((s for s, line in base_rows.items() if line not in rev_set_lines), key=lambda s: int(s[1:]))",
  new="row_missing = []")
M("C23", "counter", "K9", "K9: LIVE sha256 not compared to the POP token",
  old='if len(live.get(s, [])) != 1 or live[s][0][0] != "200" or live[s][0][2] != token or live[s][0][3] != url]',
  new='if len(live.get(s, [])) != 1 or live[s][0][0] != "200" or live[s][0][3] != url]')
M("C24", "counter", "K9", "K9: LIVE ids outside POP tolerated",
  old="live_extra = sorted(set(live) - set(POP))", new="live_extra = []")
M("C25", "counter", "K9", "K9: duplicate LIVE lines tolerated",
  old='if len(live.get(s, [])) != 1 or live[s][0][0] != "200"',
  new='if len(live.get(s, [])) < 1 or live[s][0][0] != "200"')
M("C26", "counter", "K10", "K10: changed paths outside the candidate table tolerated",
  old="outside_table = sorted(p for p in changed if p not in candidates and p != C1_RECEIPT)",
  new="outside_table = []")
M("C27", "counter", "K10", "K10: C2-owned candidates need not differ F..rev",
  old="own_bad = sorted(p for p in own if p not in changed or candidates.get(p) != sha(blob(lane, rev, p)))",
  new="own_bad = []")
M("C28", "counter", "K1", "K1: counter bytes need not match the frozen row",
  old="k1_self = bool(frozen.get(SELF)) and frozen.get(SELF) == self_sha",
  new="k1_self = True")
M("C29", "counter", "K4", "K4: resolving files looked up at BASE instead of rev",
  old='rev_files = set(ls(lane, rev, "corpus/evidence"))',
  new='rev_files = set(ls(lane, BASE, "corpus/evidence"))')
M("C30", "counter", "K7", "K7: census reference not required to exist",
  old="k7 = not moved and bool(fcommit)", new="k7 = not moved")
M("C31", "counter", "K2", "K2: derived population not compared to POP",
  old="k2 = bool(POP) and derived == POP", new="k2 = bool(POP)")
M("C32", "counter", "K6", "K6: POP SOURCES rows may change",
  old="rows_changed = sorted(s for s in POP if base_rows.get(s) != rev_rows.get(s))",
  new="rows_changed = []")
M("C33", "counter", "K10", "K10: C1 receipt no longer exempt from the candidate table",
  old='outside_table = sorted(p for p in changed if p not in candidates and p != C1_RECEIPT)',
  new='outside_table = sorted(p for p in changed if p not in candidates)')
M("C34", "counter", "K5", "K5: RESOLVED line not required",
  old='if binds != [f"BIND {sid} capture={cap} by=provenance-row"] or len(resolved) != 1 \\',
  new='if binds != [f"BIND {sid} capture={cap} by=provenance-row"] or len(resolved) < 0 \\')

# ---- tree mutants (single-point edits of the fixture tree)
M("T01", "tree", "K8", "SOURCES: silent outside row S001 rewritten (one extra space)",
  tree="sources_space", arg="S001")
M("T02", "tree", "K8", "SOURCES: silent outside row S002 deleted", tree="sources_delete", arg="S002")
M("T03", "tree", "K3", "round52 PROVENANCE: fourth cell on the S228 line", tree="prov_fourth", arg="S228")
M("T04", "tree", "K4", "round52 PROVENANCE: fabricated id S999 line", tree="prov_fake_id")
M("T05", "tree", "K9", "LIVE: S228 sha256 forged to zeros (frozen row re-frozen)", tree="live_sha_zero", arg="S228")
M("T06", "tree", "K4", "round52 PROVENANCE: second binding line for S210", tree="prov_dup", arg="S210")
M("T07", "tree", "K10", "extra file corpus/evidence/round52/NOTES.md", tree="extra_file",
  f_excludes_extra=["corpus/evidence/round52/NOTES.md"])
M("T08", "tree", "K3", "round52 PROVENANCE: URL channel line for S180", tree="prov_url")
M("T09", "tree", "K4", "S210 binding moved from round52 to round58", tree="prov_wrong_round", arg="S210")
M("T10", "tree", "K4", "S210 binds the pypi-server capture instead of its own", tree="prov_wrong_path", arg="S210")
M("T11", "tree", "K6", "POP capture round52/pypi-server bytes edited", tree="capture_append")
M("T12", "tree", "K10", "new PROVENANCE files identical F'..rev (pre-freeze commit)", tree="none", f_excludes=[])
M("T13", "tree", "K1", "frozen-instruments row for the counter removed", tree="none", drop_frozen=[SELF])
M("T14", "tree", "K9", "LIVE: extra id S999 line", tree="live_extra_id")
M("T15", "tree", "K9", "LIVE: S228 http=404", tree="live_404", arg="S228")
M("T16", "tree", "K6", "SOURCES: POP row S210 rewritten", tree="sources_space", arg="S210")
M("T17", "tree", "K7", "outside row S236 rebound by a round94 provenance line", tree="prov_outside_rebind")
M("T18", "tree", "K4", "S210 sha cell carries a second ticked sha", tree="prov_extra_sha", arg="S210")
M("T19", "tree", "K6", "POP capture round52/pypi-server deleted", tree="capture_delete")
M("T20", "tree", "K10", "C1 receipt added after the freeze (allowed change)", tree="none",
  f_excludes="DEFAULT_PLUS_RECEIPT", expect_pass=True)
M("T21", "tree", "K8", "SOURCES: silent outside row S001 duplicated", tree="sources_dup", arg="S001")
M("T22", "tree", "K3", "round58 PROVENANCE: S211 line reduced to two cells", tree="prov_two_cells", arg="S211")
M("T23", "tree", "K4", "round52 PROVENANCE: S219 sha cell zeroed", tree="prov_sha_zero", arg="S219")
M("T24", "tree", "K4", "round58 PROVENANCE emptied of table lines", tree="prov_truncate")
M("T25", "tree", "K4", "round58 PROVENANCE renamed to round59", tree="prov_rename")
M("T26", "tree", "K9", "LIVE: second line for S228", tree="live_dup", arg="S228")
M("T27", "tree", "K6", "POP capture round52/pypi-server replaced by another file's bytes", tree="capture_copy")
M("T28", "tree", "K4", "round52 PROVENANCE: S210 line binds a path that does not exist", tree="prov_missing_path", arg="S210")


M("T29", "tree", "K3", "BASE provenance round50 gets a non-table comment line", tree="base_prov_comment")
M("T30", "tree", "K7", "no freeze commit at all (claims file absent)", tree="no_claims")

# ---- phase 2: counter mutant x the forgery aimed at its leg
def P(pid, counter, tree, expect, desc):
    base = dict(MUTANTS[counter])
    spec = dict(id=pid, kind="combo", expect=expect, desc=desc,
                old=base["old"], new=base["new"])
    spec.update({k: v for k, v in MUTANTS[tree].items()
                 if k in ("tree", "arg", "f_excludes", "f_excludes_extra", "drop_frozen")})
    MUTANTS[pid] = spec

P("P01", "C09", "T08", "K3", "C09 (no :// scan) x URL-channel line")
P("P02", "C11", "T06", "K4", "C11 (zero-or-many lines) x duplicate S210 line")
P("P03", "C12", "T09", "K4", "C12 (no round check) x S210 moved to round58")
P("P04", "C13", "T10", "K4", "C13 (no binds check) x S210 binds the wrong capture")
P("P05", "C14", "T11", "K4", "C14 (no capture sha) x POP capture edited")
P("P06", "C15", "T18", "K4", "C15 (token membership) x second ticked sha")
P("P07", "C16", "T04", "K4", "C16 (no extra-id check) x fabricated S999")
P("P08", "C17", "T10", "K5", "C17 (any BIND) x S210 binds the wrong capture")
P("P09", "C19", "T24", "K5", "C19 (row may stay defective) x round58 emptied")
P("P10", "C20", "T11", "K6", "C20 (captures may change) x POP capture edited")
P("P11", "C22", "T01", "K8", "C22 (no row equality) x silent row S001 rewritten")
P("P12", "C23", "T05", "K9", "C23 (no LIVE sha) x LIVE sha forged")
P("P13", "C24", "T14", "K9", "C24 (LIVE extra ids) x LIVE S999")
P("P14", "C25", "T26", "K9", "C25 (duplicate LIVE) x second S228 line")
P("P15", "C26", "T07", "K10", "C26 (no outside-table) x post-freeze extra file")
P("P16", "C28", "T13", "K1", "C28 (self not frozen) x SELF frozen row removed")
P("P17", "C32", "T16", "K6", "C32 (POP rows may change) x S210 row rewritten")
P("P18", "C33", "T20", "K10", "C33 (receipt not exempt) x receipt added after freeze")
P("P19", "C30", "T30", "K7", "C30 (no freeze needed) x claims file absent")
P("P20", "C10", "T29", "K3", "C10 (BASE prov may change) x BASE provenance comment")
P("P21", "C08", "T03", "K3", "C08 (four cells allowed) x fourth cell")
P("P22", "C27", "T12", "K10", "C27 (own need not differ) x prov identical F'..rev")

# ---------------------------------------------------------------- helpers
def run(cmd, cwd, check=True, timeout=1800):
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, timeout=timeout)
    if check and p.returncode != 0:
        raise SystemExit(f"{' '.join(map(str, cmd))} failed: {p.stderr.decode(errors='replace')[-400:]}")
    return p


def git(repo, *args, check=True):
    return run(["git", "-C", str(repo), *args], cwd=repo, check=check)


def blob(repo, rev, path):
    p = subprocess.run(["git", "-C", str(repo), "show", f"{rev}:{path}"], capture_output=True)
    return p.stdout if p.returncode == 0 else None


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest() if b is not None else "absent"


def sha_file(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else "absent"


def edit(path: Path, old: str, new: str):
    t = path.read_text()
    n = t.count(old)
    if n != 1:
        raise SystemExit(f"edit anchor count {n} != 1 in {path}: {old[:80]!r}")
    path.write_text(t.replace(old, new, 1))


def rewrite_claims(text, frozen_sha, cand_sha, drop_frozen=(), cand_add=None):
    out, block = [], None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("```"):
            name = s[3:].strip()
            prev, block = block, (name if name in (FROZEN_BLOCK, CAND_BLOCK) else None)
            if prev == CAND_BLOCK and cand_add:
                for path, digest in cand_add:
                    out.append(f"{digest}  {path}")
            out.append(line)
            continue
        m = ROWSHA.match(s)
        if block and m:
            path = m.group(2)
            if block == FROZEN_BLOCK:
                if path in drop_frozen:
                    continue
                if path in frozen_sha:
                    out.append(f"{frozen_sha[path]}  {path}")
                    continue
            else:
                if path in cand_sha:
                    out.append(f"{cand_sha[path]}  {path}")
                    continue
        out.append(line)
    return "\n".join(out) + "\n"


def prov_at(repo: Path):
    return sorted(str(p.relative_to(repo)) for p in (repo / "corpus/evidence").rglob("PROVENANCE.md"))


def apply_tree(repo: Path, spec: dict):
    arg = spec.get("arg")
    kind = spec["tree"]
    if kind == "none":
        return
    if kind == "sources_space":
        p = repo / "corpus/SOURCES.md"
        lines = p.read_text().splitlines(keepends=True)
        idx = [i for i, ln in enumerate(lines) if re.match(rf"^ {{0,3}}\|\s*{arg}\s*\|", ln)]
        assert len(idx) == 1, (arg, idx)
        i = idx[0]
        assert " | " in lines[i]
        lines[i] = lines[i].replace(" | ", " |  ", 1)
        p.write_text("".join(lines))
        return
    if kind == "sources_delete":
        p = repo / "corpus/SOURCES.md"
        lines = p.read_text().splitlines(keepends=True)
        idx = [i for i, ln in enumerate(lines) if re.match(rf"^ {{0,3}}\|\s*{arg}\s*\|", ln)]
        assert len(idx) == 1, (arg, idx)
        del lines[idx[0]]
        p.write_text("".join(lines))
        return
    if kind == "sources_dup":
        p = repo / "corpus/SOURCES.md"
        lines = p.read_text().splitlines(keepends=True)
        idx = [i for i, ln in enumerate(lines) if re.match(rf"^ {{0,3}}\|\s*{arg}\s*\|", ln)]
        assert len(idx) == 1, (arg, idx)
        lines.insert(idx[0] + 1, lines[idx[0]])
        p.write_text("".join(lines))
        return
    if kind == "prov_fourth":
        p = repo / "corpus/evidence/round52/PROVENANCE.md"
        lines = p.read_text().splitlines(keepends=True)
        idx = [i for i, ln in enumerate(lines) if re.match(rf"^\|\s*{arg}\s*\|", ln)]
        assert len(idx) == 1, (arg, idx)
        lines[idx[0]] = lines[idx[0]].rstrip("\n") + " extra |\n"
        p.write_text("".join(lines))
        return
    if kind == "prov_fake_id":
        p = repo / "corpus/evidence/round52/PROVENANCE.md"
        p.write_text(p.read_text() +
                     "| S999 | `graders/pypi-server/tests/test_outputs.py` | "
                     "`82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c` |\n")
        return
    if kind == "prov_dup":
        p = repo / "corpus/evidence/round52/PROVENANCE.md"
        lines = p.read_text().splitlines(keepends=True)
        idx = [i for i, ln in enumerate(lines) if re.match(rf"^\|\s*{arg}\s*\|", ln)]
        assert len(idx) == 1, (arg, idx)
        lines.insert(idx[0] + 1, lines[idx[0]])
        p.write_text("".join(lines))
        return
    if kind == "prov_url":
        p = repo / "corpus/evidence/round52/PROVENANCE.md"
        p.write_text(p.read_text() +
                     "| S180 | `sources/tb2-readme.md` | "
                     "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
                     "2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md |\n")
        return
    if kind == "prov_wrong_round":
        src = repo / "corpus/evidence/round52/PROVENANCE.md"
        dst = repo / "corpus/evidence/round58/PROVENANCE.md"
        lines = src.read_text().splitlines(keepends=True)
        idx = [i for i, ln in enumerate(lines) if re.match(rf"^\|\s*{arg}\s*\|", ln)]
        assert len(idx) == 1, (arg, idx)
        moved = lines.pop(idx[0])
        src.write_text("".join(lines))
        dst.write_text(dst.read_text() + moved)
        return
    if kind == "prov_wrong_path":
        p = repo / "corpus/evidence/round52/PROVENANCE.md"
        lines = p.read_text().splitlines(keepends=True)
        idx = [i for i, ln in enumerate(lines) if re.match(rf"^\|\s*{arg}\s*\|", ln)]
        assert len(idx) == 1, (arg, idx)
        lines[idx[0]] = re.sub(r"`graders/distribution-search/tests/test_outputs\.py`",
                               "`graders/pypi-server/tests/test_outputs.py`", lines[idx[0]])
        p.write_text("".join(lines))
        return
    if kind == "prov_extra_sha":
        p = repo / "corpus/evidence/round52/PROVENANCE.md"
        lines = p.read_text().splitlines(keepends=True)
        idx = [i for i, ln in enumerate(lines) if re.match(rf"^\|\s*{arg}\s*\|", ln)]
        assert len(idx) == 1, (arg, idx)
        lines[idx[0]] = re.sub(r"`([0-9a-f]{64})`", r"`\1` `" + "0" * 64 + "`", lines[idx[0]], count=1)
        p.write_text("".join(lines))
        return
    if kind == "prov_two_cells":
        p = repo / "corpus/evidence/round58/PROVENANCE.md"
        lines = p.read_text().splitlines(keepends=True)
        idx = [i for i, ln in enumerate(lines) if re.match(rf"^\|\s*{arg}\s*\|", ln)]
        assert len(idx) == 1, (arg, idx)
        cells = [c.strip() for c in lines[idx[0]].strip().strip("|").split("|")]
        lines[idx[0]] = f"| {cells[0]} | {cells[1]} |\n"
        p.write_text("".join(lines))
        return
    if kind == "prov_sha_zero":
        p = repo / "corpus/evidence/round52/PROVENANCE.md"
        lines = p.read_text().splitlines(keepends=True)
        idx = [i for i, ln in enumerate(lines) if re.match(rf"^\|\s*{arg}\s*\|", ln)]
        assert len(idx) == 1, (arg, idx)
        lines[idx[0]] = re.sub(r"`[0-9a-f]{64}`", "`" + "0" * 64 + "`", lines[idx[0]], count=1)
        p.write_text("".join(lines))
        return
    if kind == "prov_truncate":
        p = repo / "corpus/evidence/round58/PROVENANCE.md"
        head = [ln for ln in p.read_text().splitlines(keepends=True) if not ln.lstrip().startswith("|")]
        p.write_text("".join(head))
        return
    if kind == "prov_rename":
        src = repo / "corpus/evidence/round58/PROVENANCE.md"
        dst = repo / "corpus/evidence/round59/PROVENANCE.md"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src.read_bytes())
        src.unlink()
        return
    if kind == "prov_missing_path":
        p = repo / "corpus/evidence/round52/PROVENANCE.md"
        lines = p.read_text().splitlines(keepends=True)
        idx = [i for i, ln in enumerate(lines) if re.match(rf"^\|\s*{arg}\s*\|", ln)]
        assert len(idx) == 1, (arg, idx)
        lines[idx[0]] = re.sub(r"`graders/distribution-search/tests/test_outputs\.py`",
                               "`graders/distribution-search/tests/absent_outputs.py`", lines[idx[0]])
        p.write_text("".join(lines))
        return
    if kind == "prov_outside_rebind":
        p = repo / "corpus/evidence/round94/PROVENANCE.md"
        p.write_text(p.read_text() +
                     "| S236 | `graders/write-compressor/solution/solve.sh` | "
                     "`01550b7de7ab1320b1898eae055226bb7c73bee259c75102d2240c974a730409` |\n")
        return
    if kind == "capture_append":
        p = repo / "corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py"
        p.write_bytes(p.read_bytes() + b"\n# forged after freeze\n")
        return
    if kind == "capture_delete":
        (repo / "corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py").unlink()
        return
    if kind == "capture_copy":
        src = repo / "corpus/evidence/round94/graders/write-compressor/tests/original-decomp.c"
        dst = repo / "corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py"
        dst.write_bytes(src.read_bytes())
        return
    if kind == "base_prov_comment":
        p = repo / "corpus/evidence/round50/PROVENANCE.md"
        p.write_text(p.read_text() + "\n# forged after freeze\n")
        return
    if kind == "no_claims":
        (repo / CLAIMS).unlink(missing_ok=True)
        return
    if kind == "extra_file":
        (repo / "corpus/evidence/round52/NOTES.md").write_text("stray\n")
        return
    if kind == "live_sha_zero":
        p = repo / ".ufo/waves/round-100/L1/c2-live-refetch.txt"
        lines = p.read_text().splitlines(keepends=True)
        idx = [i for i, ln in enumerate(lines) if ln.startswith(f"LIVE {arg} ")]
        assert len(idx) == 1, (arg, idx)
        lines[idx[0]] = re.sub(r"sha256=[0-9a-f]{64}", "sha256=" + "0" * 64, lines[idx[0]])
        p.write_text("".join(lines))
        return
    if kind == "live_404":
        p = repo / ".ufo/waves/round-100/L1/c2-live-refetch.txt"
        lines = p.read_text().splitlines(keepends=True)
        idx = [i for i, ln in enumerate(lines) if ln.startswith(f"LIVE {arg} ")]
        assert len(idx) == 1, (arg, idx)
        lines[idx[0]] = lines[idx[0]].replace("http=200", "http=404", 1)
        p.write_text("".join(lines))
        return
    if kind == "live_extra_id":
        p = repo / ".ufo/waves/round-100/L1/c2-live-refetch.txt"
        p.write_text(p.read_text() +
                     "LIVE S999 http=200 bytes=1 sha256=" + "0" * 64 +
                     " url=https://example.invalid/not-a-row\n")
        return
    if kind == "live_dup":
        p = repo / ".ufo/waves/round-100/L1/c2-live-refetch.txt"
        lines = p.read_text().splitlines(keepends=True)
        idx = [i for i, ln in enumerate(lines) if ln.startswith(f"LIVE {arg} ")]
        assert len(idx) == 1, (arg, idx)
        lines.insert(idx[0] + 1, lines[idx[0]])
        p.write_text("".join(lines))
        return
    raise SystemExit(f"unknown tree op {kind}")


def main(mid: str) -> int:
    spec = MUTANTS[mid]
    repo = ROOT / "mut" / mid
    work = ROOT / "work" / mid
    for d in (repo, work):
        if d.exists():
            shutil.rmtree(d)
    work.mkdir(parents=True)
    run(["git", "clone", "-q", "--shared", "--no-checkout", str(LANE), str(repo)], cwd=ROOT)
    git(repo, "-c", "advice.detachedHead=false", "checkout", "-q", P2)
    git(repo, "checkout", "-q", T, "--", ".")
    if "old" in spec:
        edit(repo / SELF, spec["old"], spec["new"])
    if "tree" in spec:
        apply_tree(repo, spec)

    frozen_block_paths = []
    claims_orig = blob(repo, T, CLAIMS)
    assert claims_orig is not None
    block = None
    for line in claims_orig.decode().splitlines():
        s = line.strip()
        if s.startswith("```"):
            name = s[3:].strip()
            block = name if name in (FROZEN_BLOCK, CAND_BLOCK) else None
            continue
        m = ROWSHA.match(s)
        if block == FROZEN_BLOCK and m:
            frozen_block_paths.append(m.group(2))
    frozen_sha = {p: sha_file(repo / p) for p in frozen_block_paths}
    drop = set(spec.get("drop_frozen", ()))
    base_prov = set()
    p = subprocess.run(["git", "-C", str(repo), "ls-tree", "-r", "--name-only", "7846037679de77d050141c785996471801e5a19a", "corpus/evidence"],
                       capture_output=True, text=True)
    for ln in p.stdout.splitlines():
        if ln.rsplit("/", 1)[-1] == "PROVENANCE.md":
            base_prov.add(ln)
    rev_prov = set(prov_at(repo))
    new_prov = sorted(rev_prov - base_prov)
    cand_sha = {p: sha_file(repo / p) for p in new_prov}
    cand_add = [(p, cand_sha[p]) for p in new_prov
                if f"  {p}" not in claims_orig.decode()]

    if spec.get("tree") == "no_claims":
        (repo / CLAIMS).unlink(missing_ok=True)
    else:
        claims_new = rewrite_claims(claims_orig.decode(), frozen_sha, cand_sha, drop, cand_add)
        (repo / CLAIMS).write_text(claims_new)

    git(repo, "add", "-A")
    tree_rev = git(repo, "write-tree").stdout.decode().strip()
    git(repo, "read-tree", tree_rev)
    if spec.get("f_excludes") == "DEFAULT_PLUS_RECEIPT":
        excl = new_prov + [C1_RECEIPT]
    elif "f_excludes" in spec:
        excl = list(spec["f_excludes"])
    else:
        excl = list(new_prov)
    excl += list(spec.get("f_excludes_extra", []))
    if excl:
        git(repo, "rm", "--cached", "-q", "--", *excl)
    tree_f = git(repo, "write-tree").stdout.decode().strip()
    ident = ["-c", "user.name=mut", "-c", "user.email=mut@local"]
    fcommit = git(repo, *ident, "commit-tree", tree_f, "-p", P2, "-m", f"F fixture {mid}").stdout.decode().strip()
    rev = git(repo, *ident, "commit-tree", tree_rev, "-p", fcommit, "-m", f"rev fixture {mid}").stdout.decode().strip()
    git(repo, "update-ref", "refs/heads/mut", rev)
    git(repo, "checkout", "-f", "-q", "mut")
    assert git(repo, "rev-parse", "--show-toplevel").stdout.decode().strip() == str(repo)

    proc = subprocess.run([sys.executable, "plans/round100_c2_rowcensus_bind.py", "--lane", ".",
                           "--rev", "HEAD", "--work", str(work)],
                          cwd=str(repo), capture_output=True, text=True, timeout=1800)
    out = proc.stdout + proc.stderr
    legs = {}
    m = re.search(r"^LEGS (.*)$", out, re.M)
    if m:
        for tok in m.group(1).split():
            k, v = tok.split("=")
            legs[k] = v
    pred = re.search(r"^PREDICATE R100-C2 (\S+)$", out, re.M)
    record = dict(id=mid, kind=spec["kind"], expect=spec["expect"], desc=spec["desc"],
                  rc=proc.returncode, predicate=pred.group(1) if pred else "missing",
                  legs=legs, defects=[ln for ln in out.splitlines() if ln.startswith("DEFECT ")],
                  rev=rev, fcommit=fcommit, tree_rev=tree_rev,
                  counter_sha=sha_file(repo / SELF), new_prov=new_prov,
                  out=out)
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results" / f"{mid}.json").write_text(json.dumps(record, indent=1))
    print(f"{mid} rc={proc.returncode} pred={record['predicate']} "
          f"fail={','.join(k for k, v in legs.items() if v == 'fail') or '-'}")
    if not os.environ.get("KEEP"):
        shutil.rmtree(work, ignore_errors=True)
        shutil.rmtree(repo, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
