#!/usr/bin/env python3
"""anchor_digest_check.py — every `sha256 <hex>` claim in `corpus/SOURCES.md` must resolve.

Built for kengaku round 37 from the round-36 non-author spot-check routed item 1
(`corpus/lessons/round-36-verifier-spotcheck.md` §5): row S110's anchor cell carried 63 hex digits
because one `0` was dropped in transcription, and nothing in the lane compared a row's digest with the
capture manifest, so no counter could see it. This check does that comparison for every row, and is shown
able to fail and to pass (`.ufo/waves/round-37/build/R37AnchorSweep.md`, five mutants and two controls).

Read-only; stdlib only; writes no file. Git subprocesses inherit the environment, so TMPDIR is honoured.

Usage: python3 anchor_digest_check.py [--lane DIR] [--evidence-ref head|index] [--verbose]
Exit: 0 no defects · 1 defects found · 2 usage error (bad args, missing lane, absent SOURCES.md, no git).

## What is checked

Row set — the census shape (`plans/round37_c2_verify.py` SOURCE_ROW, `^ {0,3}\\|\\s*(S\\d{3,})\\s*\\|`),
so this check and the census agree on what a row is. Cells are the row stripped of its outer pipes and
split on `|`; an 11-cell row is `id, source, kind, tier, scope, anchor, teaches, status, opened,
recheck, used-by`, so the **anchor is cell 6** (index 5). A row that matches the census regex but does not
have 11 cells is a `row-malformed` defect: its anchor cannot be located.

Token — `sha256` plus whitespace plus a hex run, optionally backtick-quoted and optionally followed by
`…` or `...` (S070 writes ``sha256 `45dd…` ``; S036 writes `sha256 afaae9dd…`; both are claims and both
are scanned). Tokens are collected from the whole row, not only the anchor cell.

Allowed digest set A — built from **committed** bytes only: the sha256 of every blob under
`corpus/evidence/` plus every 64-hex digest listed in a `SHA256SUMS*` file there (`git ls-tree -r HEAD`
then `git cat-file --batch`). Working-tree files under `corpus/evidence/` are never hashed and working-tree
manifests are never read: an uncommitted file cannot launder a digest into A (control C6 in the report: a
fabricated `SHA256SUMS` added to the fixture clone without staging it does not silence the defect it
names). `--evidence-ref head` (default) reads HEAD blobs, so an unpromoted capture never counts;
`--evidence-ref index` reads the index blobs (`git cat-file :<path>`), identical to HEAD in a clean tree,
and exists so a seat that may not commit (round-37 fixture seats are index-only) can demonstrate the
green state of a tree whose captures are staged. `--verbose` prints the mode and its totals.

Per token:

  * a token outside the anchor cell is `token-outside-anchor` — always a defect, whatever its value. A
    digest claim anywhere but the anchor cell is unverifiable registry data (the mutant "token moved to
    the teaches cell" exists because the cheapest wrong fix for S110 would be "paste it elsewhere").
  * an anchor token followed by an ellipsis is an abbreviation: a defect (`abbrev-unresolved`) unless its
    hex is 8-63 lowercase hex digits and a prefix of some member of A. S036's `sha256 afaae9dd…` is
    therefore checked, not excused: the prefix is the head of the committed
    `corpus/evidence/attrib-r23-stream.log` digest. An abbreviation makes no full-digest claim, so it is
    not required to be 64 hex — but it must resolve.
  * any other anchor token must be exactly 64 lowercase hex digits (`digest-short`, `digest-long`,
    `digest-uppercase` otherwise) and must be a member of A (`digest-unknown` otherwise).

Erratum exemption (append-only repair, `corpus/QUALITY.md` Q6). A line in a committed
`corpus/lessons/*.md` beginning `Erratum (round 37): S<id> anchor sha256` is read; lessons are read from
the working tree for paths committed at HEAD, so a seat's erratum counts before it is committed while the
digest it cites still has to be committed. An erratum for S<id> exempts that row's anchor token from
*every* anchor class above when it carries the row's exact wrong token and at least one other token that
is 64 lowercase hex and in A. The erratum line is itself checked: no 64-hex token on it may be outside A
unless it is the cited wrong token of the row it names (`erratum-digest-unresolved`), and an erratum with
no 64-hex token in A corrects nothing (`erratum-incomplete`). An erratum whose row has since been repaired
stays valid — errata are append-only and are not rewritten when the row is fixed, so no stale-erratum
defect is raised.

Deliberate strictness, stated as a limit: an uppercase 64-hex digest is a defect even though it denotes
the same bytes, because every manifest in `corpus/evidence/` writes lowercase and a case-insensitive
comparison would hide a manifest written in another case; a 63-hex token is a defect even when it is a
prefix of a real digest, because that is precisely the S110 defect shape. A digest that is *true* but has
no committed capture under `corpus/evidence/` is `digest-unknown` too: the claim cannot be re-checked from
the lane's own bytes, which is the failure round 36 recorded ("a receipt is evidence only if something
here re-runs it").
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import subprocess
import sys

ROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
TOKEN = re.compile(r"sha256[ \t]+`?([0-9A-Fa-f]+)`?([ \t]*(?:…|\.\.\.))?")
ERRATUM = re.compile(r"^ {0,3}Erratum \(round 37\): (S\d{3,}) anchor sha256\b")
SUMS_NAME = re.compile(r"(?:^|/)SHA256SUMS[^/]*$")
HEX64 = re.compile(r"[0-9a-f]{64}")
HEX64_ANY = re.compile(r"[0-9A-Fa-f]{64}")
ANCHOR_CELL = 5  # id source kind tier scope | anchor | teaches status opened recheck used-by
NCELLS = 11
EVIDENCE = "corpus/evidence"
LESSONS = "corpus/lessons"


class Usage(Exception):
    pass


def git(lane, *args, data=None):
    try:
        r = subprocess.run(["git", "-C", str(lane), *args], input=data, capture_output=True)
    except OSError as e:
        raise Usage(f"cannot run git: {e}")
    if r.returncode != 0:
        msg = r.stderr.decode("utf-8", "replace").strip().splitlines()
        raise Usage(f"git {' '.join(args)} failed: {msg[0][:160] if msg else r.returncode}")
    return r.stdout


def tree_paths(lane, root):
    out = git(lane, "ls-tree", "-r", "--name-only", "-z", "HEAD", "--", root)
    return [p for p in out.decode("utf-8", "surrogateescape").split("\0") if p]


def evidence_paths(lane, ref):
    if ref == "head":
        return tree_paths(lane, EVIDENCE)
    out = git(lane, "ls-files", "--cached", "-z", "--", EVIDENCE)
    return [p for p in out.decode("utf-8", "surrogateescape").split("\0") if p]


def spec_for(ref, path):
    return (":" if ref == "index" else "HEAD:") + path


def blobs(lane, specs):
    """Return {spec: bytes} for `git cat-file --batch` specs such as `HEAD:corpus/x`."""
    if not specs:
        return {}
    out = git(lane, "cat-file", "--batch", data="".join(s + "\n" for s in specs).encode())
    res, i = {}, 0
    for s in specs:
        nl = out.find(b"\n", i)
        if nl < 0:
            raise Usage(f"cat-file: truncated batch output at {s}")
        header = out[i:nl].decode("utf-8", "replace").split()
        if len(header) != 3 or header[1] != "blob":
            raise Usage(f"cat-file: {s} is not a blob ({' '.join(header)[:80]})")
        size = int(header[2])
        res[s] = out[nl + 1:nl + 1 + size]
        i = nl + 1 + size + 1
    return res


def allowed_digests(lane, ref):
    """(file_digests, manifest_digests) from committed (or staged) bytes under corpus/evidence only."""
    paths = evidence_paths(lane, ref)
    if not paths:
        raise Usage(f"no {'committed' if ref == 'head' else 'staged'} file under {EVIDENCE}/ — "
                    f"cannot resolve any digest")
    specs = [spec_for(ref, p) for p in paths]
    data = blobs(lane, specs)
    files, manifests = {}, {}
    for p, s in zip(paths, specs):
        b = data[s]
        files.setdefault(hashlib.sha256(b).hexdigest(), p)
        if SUMS_NAME.search(p):
            for line in b.decode("utf-8", "replace").splitlines():
                m = re.match(r"\s*([0-9A-Fa-f]{64})\s+\*?\S", line)
                if m:
                    manifests.setdefault(m.group(1).lower(), p)
    return files, manifests


def load_errata(lane):
    """[(path, lineno, sid, tokens)] for erratum lines in committed lessons, read from the working tree."""
    out = []
    for p in tree_paths(lane, LESSONS):
        if not p.endswith(".md"):
            continue
        f = lane / p
        if not f.is_file():
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            m = ERRATUM.match(line)
            if m:
                out.append((p, n, m.group(1),
                            [(t.group(1), bool(t.group(2))) for t in TOKEN.finditer(line)]))
    return out


def parse_rows(lane):
    """[{sid, lineno, cells, atoks, rtoks}] for every census-shaped row."""
    rows = []
    text = (lane / "corpus/SOURCES.md").read_text(encoding="utf-8", errors="replace")
    for lineno, line in enumerate(text.splitlines(), 1):
        m = ROW.match(line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rtoks = [(i, t.group(1), bool(t.group(2)))
                 for i, c in enumerate(cells) for t in TOKEN.finditer(c)]
        atoks = [t for i, t, _ in rtoks if i == ANCHOR_CELL]
        rows.append({"sid": m.group(1), "lineno": lineno, "cells": cells,
                     "atoks": atoks, "rtoks": rtoks})
    return rows


def check(lane, verbose, ref):
    files, manifests = allowed_digests(lane, ref)
    allowed = set(files) | set(manifests)
    by_example = {**files, **manifests}
    rows = parse_rows(lane)
    anchor_tokens = {}
    for r in rows:
        anchor_tokens.setdefault(r["sid"], set()).update(r["atoks"])

    notes, defects = [f"EVIDENCE ref={ref} files={len(files)} manifest_digests={len(manifests)} "
                      f"rows={len(rows)}"], []

    # erratum lines are their own subject, and an exemption source for the row they name.
    exempt = {}
    for path, lineno, sid, toks in load_errata(lane):
        supported = [t for t, _ in toks if HEX64.fullmatch(t) and t in allowed]
        cited_wrong = [t for t, _ in toks if t in anchor_tokens.get(sid, ())]
        for t, _ in toks:
            if HEX64_ANY.fullmatch(t) and t not in allowed and t not in cited_wrong:
                defects.append(f"DEFECT {sid} erratum token={t} class=erratum-digest-unresolved "
                               f"detail=64-hex-nor-in-committed-evidence-nor-the-row-s-anchor "
                               f"loc={path}:{lineno}")
        if not supported:
            defects.append(f"DEFECT {sid} erratum token=- class=erratum-incomplete "
                           f"detail=no-64-hex-digest-in-committed-evidence loc={path}:{lineno}")
        elif cited_wrong:
            exempt.setdefault(sid, (path, lineno, cited_wrong[0], supported[0]))
        if verbose:
            notes.append(f"ERRATUM {sid} loc={path}:{lineno} cited_wrong={cited_wrong} "
                         f"correction={supported[:1]}")

    ntokens = 0
    for r in rows:
        sid, lineno = r["sid"], r["lineno"]
        ntokens += len(r["rtoks"])
        if len(r["cells"]) != NCELLS:
            defects.append(f"DEFECT {sid} anchor token=- class=row-malformed "
                           f"detail=cells={len(r['cells'])}-expected={NCELLS} loc=corpus/SOURCES.md:{lineno}")
            continue
        ex = exempt.get(sid)
        if ex and verbose:
            notes.append(f"EXEMPT {sid} anchor={r['atoks'][0] if r['atoks'] else '-'} "
                         f"by={ex[0]}:{ex[1]} correction={ex[3]}")
        for cell_idx, tok, ell in r["rtoks"]:
            if cell_idx != ANCHOR_CELL:
                defects.append(f"DEFECT {sid} anchor token={tok} class=token-outside-anchor "
                               f"detail=sha256-claim-in-cell-{cell_idx + 1}-of-{NCELLS} "
                               f"loc=corpus/SOURCES.md:{lineno}")
                continue
            if ex:
                continue
            if ell:
                if not (8 <= len(tok) <= 63 and tok == tok.lower()):
                    defects.append(f"DEFECT {sid} anchor token={tok} class=abbrev-unresolved "
                                   f"detail=prefix-needs-8-63-lowercase-hex loc=corpus/SOURCES.md:{lineno}")
                elif not any(d.startswith(tok) for d in allowed):
                    defects.append(f"DEFECT {sid} anchor token={tok} class=abbrev-unresolved "
                                   f"detail=no-committed-digest-starts-with-this-prefix "
                                   f"loc=corpus/SOURCES.md:{lineno}")
                elif verbose:
                    notes.append(f"ABBREV {sid} prefix={tok} "
                                 f"matches={sorted(d for d in allowed if d.startswith(tok))[0]}")
                continue
            if not HEX64.fullmatch(tok):
                if len(tok) != 64:
                    cls, why = ("digest-short" if len(tok) < 64 else "digest-long"), f"{len(tok)}-hex"
                else:
                    cls, why = "digest-uppercase", "64-hex-but-not-lowercase"
                defects.append(f"DEFECT {sid} anchor token={tok} class={cls} detail={why} "
                               f"loc=corpus/SOURCES.md:{lineno}")
            elif tok not in allowed:
                defects.append(f"DEFECT {sid} anchor token={tok} class=digest-unknown "
                               f"detail=not-committed-evidence-and-not-in-a-SHA256SUMS "
                               f"loc=corpus/SOURCES.md:{lineno}")
            elif verbose:
                notes.append(f"RESOLVED {sid} digest={tok} via={by_example[tok]}")

    if verbose:
        for n in notes:
            print(n)
    for d in defects:
        print(d)
    print(f"rows={len(rows)} tokens={ntokens} defects={len(defects)}")
    return 0 if not defects else 1


def main(argv):
    ap = argparse.ArgumentParser(add_help=True, description="check every SOURCES anchor sha256 claim")
    ap.add_argument("--lane", default=".")
    ap.add_argument("--evidence-ref", choices=("head", "index"), default="head")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args(argv)
    lane = pathlib.Path(a.lane).resolve()
    try:
        if not lane.is_dir():
            raise Usage(f"lane is not a directory: {lane}")
        if not (lane / "corpus/SOURCES.md").is_file():
            raise Usage(f"no corpus/SOURCES.md under {lane}")
        if not (lane / ".git").exists():
            raise Usage(f"no git work tree at {lane}; committed evidence cannot be established")
        return check(lane, a.verbose, a.evidence_ref)
    except Usage as e:
        print(f"USAGE: {e}", file=sys.stderr)
        return 2
    except Exception as e:  # a check that cannot run is never a pass
        print(f"USAGE: {type(e).__name__}: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
