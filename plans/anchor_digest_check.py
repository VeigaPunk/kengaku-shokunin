#!/usr/bin/env python3
"""anchor_digest_check.py — every `sha256 <hex>` claim in `corpus/SOURCES.md` must resolve to the capture
its own row names.

Fixed copy written by seat `R38AnchorBind` (kengaku round 38) from `plans/anchor_digest_check.py` as landed
on `2c5f4e0` (built in round 37). Round 37's finding `F37A-1`
(`.ufo/waves/round-37/falsify/F37AnchorRerun.md` §4) recorded the hole: the shipped tool tests the digest as
membership in ONE global set A of every committed `corpus/evidence/` digest, so a row's anchor may carry
another row's real committed digest and still pass (its mutants M4b and M5: S111 carrying S108's digest,
`defects=0`, exit 0). This copy binds each token to the capture **the row itself names**, so cross-row
substitution is a defect while every tip state that was green under the global test stays green.

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

### Binding — which capture a row's token must match

A capture is a **named file** under `corpus/evidence/`: its committed path, plus the entry naming that same
filename in a `SHA256SUMS*` file committed in the same directory (the digest that entry lists, and the
digest of the committed file bytes, are both accepted views of that one capture — verified equal in every
task directory of this lane at `2c5f4e0`). A capture's accepted digest set is those views unioned.

The row's own text supplies the binding, first source that yields a capture winning:

  1. **Provenance row** — a committed markdown under `corpus/evidence/` whose table line carries this row's
     id and a filename that resolves beside it. `corpus/evidence/round37/anchor-captures/PROVENANCE.md`
     binds S070/S072/S073/S074 that way (its table names the pinned URL, the local file and the digest).
  2. **Upstream URL** — a `raw.githubusercontent.com/<owner>/<repo>/<commit>/<subpath>` or
     `github.com/<owner>/<repo>/blob/<commit>/<subpath>` URL anywhere in the row. The task component of
     `<subpath>` is matched **exactly** against the `name = "<org>/<task>"` a committed `task.toml` gives
     for an evidence directory; the capture is that directory plus the URL's basename. So S111's
     `configure-git-webserver/tests/test_outputs.py` binds
     `corpus/evidence/round37/tb2-git-webserver/test_outputs.py` and nothing else, while S108's
     `regex-log/tests/test_outputs.py` binds `corpus/evidence/round36/tb2-regex-log/test_outputs.py`. A
     provenance URL (an evidence markdown naming the same `<repo>/<subpath>`) is consulted when the
     `task.toml` route finds nothing, which covers captures that are not whole task directories.
  3. **Explicit lane path** — a `corpus/evidence/…` path written in the row (S036's source cell,
     S114's anchor cell). It binds that committed file only; a row that names a directory, or a path with
     no committed file, binds nothing and is reported `anchor-unbound`.

A row whose token cannot be bound this way is `anchor-unbound` (detail says why): a digest claim nobody
can tie to a capture is unverifiable registry data, which is the failure shape round 36 recorded.

Digest ownership is therefore row-scoped, not global. Allowed digest set A survives only for two things:
distinguishing `digest-wrong-capture` (a real committed capture that is not this row's) from
`digest-unknown` (no committed capture anywhere), and the fallback below.

`--evidence-ref head` (default) reads HEAD blobs, so an unpromoted capture never counts;
`--evidence-ref index` reads the index blobs (`git cat-file :<path>`), identical to HEAD in a clean tree,
and exists so a seat that may not commit (round-37 fixture seats are index-only) can demonstrate the
green state of a tree whose captures are staged. `--verbose` prints the mode, the bindings and the
resolutions.

Per token:

  * a token outside the anchor cell is `token-outside-anchor` — always a defect, whatever its value. A
    digest claim anywhere but the anchor cell is unverifiable registry data (the mutant "token moved to
    the teaches cell" exists because the cheapest wrong fix for S110 would be "paste it elsewhere").
  * an anchor token followed by an ellipsis is an abbreviation: a defect (`abbrev-unresolved`) unless its
    hex is 8-63 lowercase hex digits and a prefix of a digest of the capture this row names. S036's
    `sha256 afaae9dd…` is therefore checked, not excused: the prefix is the head of the committed
    `corpus/evidence/attrib-r23-stream.log` digest its source cell names.
  * any other anchor token must be exactly 64 lowercase hex digits (`digest-short`, `digest-long`,
    `digest-uppercase` otherwise) and must be a digest of the capture this row names. A 64-hex token that
    is a committed capture but not this row's is `digest-wrong-capture` (the round-37 M4b/M5 shape: one
    row carrying another row's real digest); a token that is no committed capture at all is
    `digest-unknown`.

Erratum exemption (append-only repair, `corpus/QUALITY.md` Q6). A line in a committed
`corpus/lessons/*.md` beginning `Erratum (round 37): S<id> anchor sha256` is read; lessons are read from
the working tree for paths committed at HEAD, so a seat's erratum counts before it is committed while the
digest it cites still has to be committed. An erratum for S<id> exempts that row's anchor token from
*every* anchor class above when it carries the row's exact wrong token and at least one other token that
is 64 lowercase hex and a digest **of the capture that row names** (global A when the row binds nothing —
the exemption inherits the same row scoping, so an erratum cannot launder by citing a sibling row's real
digest). The erratum line is itself checked: no 64-hex token on it may be outside A unless it is the cited
wrong token of the row it names (`erratum-digest-unresolved`), and an erratum with no 64-hex token in A
corrects nothing (`erratum-incomplete`). An erratum whose row has since been repaired stays valid — errata
are append-only and are not rewritten when the row is fixed, so no stale-erratum defect is raised.

Deliberate strictness, stated as a limit: an uppercase 64-hex digest is a defect even though it denotes
the same bytes, because every manifest in `corpus/evidence/` writes lowercase and a case-insensitive
comparison would hide a manifest written in another case; a 63-hex token is a defect even when it is a
prefix of a real digest, because that is precisely the S110 defect shape. A digest that is *true* but has
no committed capture under `corpus/evidence/` is `digest-unknown` too: the claim cannot be re-checked from
the lane's own bytes, which is the failure round 36 recorded ("a receipt is evidence only if something
here re-runs it").

Binding limits, stated as a limit: the binding is only as good as the row's own locator. A row that
rewrites its locator *and* its digest together (points its URL at another task, or adds a provenance
table line naming another capture) passes, because the lane then has no independent record of which
upstream file the row is about. What this copy closes is substitution that leaves the row's locator
alone — the S110/M5 shape, reachable in round 37 as `defects=0`.
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
SUMS_LINE = re.compile(r"\s*([0-9A-Fa-f]{64})\s+\*?(\S+)")
TOML_NAME = re.compile(r'^\s*name\s*=\s*"([^"]+)"', re.M)
URL_RAW = re.compile(r"https?://raw\.githubusercontent\.com/([^/\s|`)\]]+)/([^/\s|`)\]]+)"
                      r"/([0-9A-Fa-f]{7,40})/([^\s|`)\]]+)")
URL_BLOB = re.compile(r"https?://github\.com/([^/\s|`)\]]+)/([^/\s|`)\]]+)/blob/"
                      r"([0-9A-Fa-f]{7,40})/([^\s|`)\]]+)")
LANE_PATH = re.compile(r"corpus/evidence/[A-Za-z0-9_./-]*[A-Za-z0-9_-]")
TICKED = re.compile(r"`([^`]+)`")
ROWID = re.compile(r"\b(S\d{3,})\b")
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


def evidence_index(lane, ref):
    """Committed (or staged) evidence under corpus/evidence, indexed for row-scoped binding.

    Returns a dict:
      file_digest   {path: sha256 of its blob}
      dir_entries   {(dir, filename): manifest-listed digest}
      manifest      {digest: manifest path}      (first listing wins; A for diagnostics only)
      examples      {digest: path}               (path a digest was first seen at)
      slugs         {dir: task slug}             (from `<dir>/task.toml` name = "<org>/<task>")
      prov_sid      {sid: [(capture path, evidence markdown)]}
      prov_url      {(repo, subpath): capture path}
      all_digests   set of every committed evidence digest (files + manifest entries)
    """
    paths = evidence_paths(lane, ref)
    if not paths:
        raise Usage(f"no {'committed' if ref == 'head' else 'staged'} file under {EVIDENCE}/ — "
                    f"cannot resolve any digest")
    specs = [spec_for(ref, p) for p in paths]
    data = blobs(lane, specs)
    file_digest, dir_entries, manifest, examples, slugs = {}, {}, {}, {}, {}
    for p, s in zip(paths, specs):
        file_digest[p] = hashlib.sha256(data[s]).hexdigest()
        examples.setdefault(file_digest[p], p)
    for p, s in zip(paths, specs):
        b = data[s]
        d, base = p.rsplit("/", 1) if "/" in p else ("", p)
        if SUMS_NAME.search(p):
            for line in b.decode("utf-8", "replace").splitlines():
                m = SUMS_LINE.match(line)
                if m:
                    name = m.group(2)
                    while name.startswith("./"):
                        name = name[2:]
                    dig = m.group(1).lower()
                    dir_entries.setdefault((d, name), dig)
                    manifest.setdefault(dig, p)
                    examples.setdefault(dig, p)
        if base == "task.toml":
            names = TOML_NAME.findall(b.decode("utf-8", "replace"))
            pick = next((n for n in names if "/" in n), names[0] if names else None)
            if pick:
                slugs[d] = pick.rsplit("/", 1)[-1]

    prov_sid, prov_url = {}, {}
    for p, s in zip(paths, specs):
        d, base = p.rsplit("/", 1) if "/" in p else ("", p)
        if base != "PROVENANCE.md":
            continue
        for line in data[s].decode("utf-8", "replace").splitlines():
            if "|" not in line:
                continue
            cands = []
            for t in TICKED.findall(line):
                rel = t.strip()
                if not rel or "://" in rel:
                    continue
                while rel.startswith("./"):
                    rel = rel[2:]
                full = f"{d}/{rel}" if d else rel
                if full in file_digest or (d, rel) in dir_entries:
                    cands.append(full)
            if not cands:
                continue
            cap = cands[0]
            for sid in dict.fromkeys(ROWID.findall(line)):
                prov_sid.setdefault(sid, []).append((cap, p))
            for m in list(URL_RAW.finditer(line)) + list(URL_BLOB.finditer(line)):
                prov_url.setdefault((m.group(2), m.group(4)), cap)

    all_digests = set(file_digest.values()) | set(dir_entries.values())
    return {"file_digest": file_digest, "dir_entries": dir_entries, "manifest": manifest,
            "examples": examples, "slugs": slugs, "prov_sid": prov_sid, "prov_url": prov_url,
            "all_digests": all_digests}


def upstream_files(text):
    """[(owner, repo, commit, subpath)] for every pinned-file URL in `text`."""
    out = []
    for m in URL_RAW.finditer(text):
        out.append((m.group(1), m.group(2), m.group(3), m.group(4)))
    for m in URL_BLOB.finditer(text):
        out.append((m.group(1), m.group(2), m.group(3), m.group(4)))
    return out


def capture_digests(idx, path):
    """{digest: label} for one named capture: committed bytes and the manifest entry for that name."""
    d, base = path.rsplit("/", 1) if "/" in path else ("", path)
    got = {}
    if path in idx["file_digest"]:
        got[idx["file_digest"][path]] = path
    if (d, base) in idx["dir_entries"]:
        got.setdefault(idx["dir_entries"][(d, base)], f"{d}/SHA256SUMS:{base}")
    return got


def bind_row(row, idx):
    """(bindings [(capture path, how)], reason-if-unbound)."""
    sid = row["sid"]
    text = " ".join(row["cells"])

    got = [(cap, "provenance-row") for cap, _ in idx["prov_sid"].get(sid, [])]
    if got:
        return got, None

    urls = upstream_files(text)
    slugs = set(idx["slugs"].values())
    for _, repo, _, subpath in urls:
        comps = [c for c in subpath.split("/") if c]
        if not comps:
            continue
        base = comps[-1]
        # the task component is the DEEPEST path component a committed task.toml names, so a URL like
        # `owner/repo/sha/a/b/tests/x` cannot be claimed by several task directories at once.
        hits = [c for c in comps[:-1] if c in slugs]
        if not hits:
            continue
        owners = sorted(d for d, slug in idx["slugs"].items() if slug == hits[-1])
        if len(owners) != 1:
            continue  # ambiguous: two evidence dirs claim the same task slug; bind nothing
        d = owners[0]
        p = f"{d}/{base}"
        if p in idx["file_digest"] or (d, base) in idx["dir_entries"]:
            got.append((p, "url-task"))
    if not got:
        for _, repo, _, subpath in urls:
            if (repo, subpath) in idx["prov_url"]:
                got.append((idx["prov_url"][(repo, subpath)], "provenance-url"))
    if got:
        return got, None

    named = []
    for m in LANE_PATH.finditer(text):
        p = m.group(0).rstrip(".,;:")
        if p and p not in named:
            named.append(p)
    for p in named:
        if p in idx["file_digest"] or (p.rsplit("/", 1)[0] if "/" in p else "",
                                       p.rsplit("/", 1)[-1]) in idx["dir_entries"]:
            got.append((p, "row-path"))
    if got:
        return got, None

    if named:
        dirish = any(p.rstrip("/") != p or p.rsplit("/", 1)[-1].find(".") < 0 for p in named)
        reason = ("names-a-directory-not-a-capture-file" if dirish
                  else "named-capture-not-committed-under-" + EVIDENCE)
        return [], reason + ":" + named[0]
    if urls:
        _, repo, _, subpath = urls[0]
        comps = [c for c in subpath.split("/") if c]
        base = comps[-1] if comps else "?"
        task = comps[-2] if len(comps) > 1 else "?"
        return [], f"no-capture-for-upstream-{'/'.join(comps[:-1]) or '?'}/{base}-task={task}"
    return [], "row-carries-no-capture-locator"


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
    idx = evidence_index(lane, ref)
    allowed = idx["all_digests"]
    rows = parse_rows(lane)
    anchor_tokens = {}
    for r in rows:
        anchor_tokens.setdefault(r["sid"], set()).update(r["atoks"])

    bound, unbound = {}, {}
    for r in rows:
        caps, reason = bind_row(r, idx)
        if caps:
            digs = {}
            for path, how in caps:
                for dig, label in capture_digests(idx, path).items():
                    digs.setdefault(dig, (path, how, label))
            bound[r["sid"]] = digs
        else:
            unbound[r["sid"]] = reason

    notes, defects = [f"EVIDENCE ref={ref} files={len(set(idx['file_digest'].values()))} "
                      f"manifest_digests={len(idx['manifest'])} rows={len(rows)} "
                      f"paths={len(idx['file_digest'])} bound_rows={len(bound)} "
                      f"unbound_rows={len(unbound)}"], []

    if verbose:
        for r in rows:
            caps, reason = bind_row(r, idx)
            if caps:
                notes.append(f"BIND {r['sid']} capture={caps[0][0]} by={caps[0][1]}")
            elif r["atoks"]:
                notes.append(f"UNBOUND {r['sid']} reason={reason}")

    # erratum lines are their own subject, and an exemption source for the row they name.
    exempt = {}
    for path, lineno, sid, toks in load_errata(lane):
        row_scope = bound.get(sid)
        supported = [t for t, _ in toks if HEX64.fullmatch(t)
                     and (t in row_scope if row_scope is not None else t in allowed)]
        cited_wrong = [t for t, _ in toks if t in anchor_tokens.get(sid, ())]
        for t, _ in toks:
            if HEX64_ANY.fullmatch(t) and t not in allowed and t not in cited_wrong:
                defects.append(f"DEFECT {sid} erratum token={t} class=erratum-digest-unresolved "
                               f"detail=64-hex-nor-in-committed-evidence-nor-the-row-s-anchor "
                               f"loc={path}:{lineno}")
        if not supported:
            unmet = ("no-64-hex-digest-of-the-capture-this-row-names" if row_scope is not None
                     else "no-64-hex-digest-in-committed-evidence")
            defects.append(f"DEFECT {sid} erratum token=- class=erratum-incomplete "
                           f"detail={unmet} loc={path}:{lineno}")
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
        row_scope = bound.get(sid)
        if ex and verbose:
            notes.append(f"EXEMPT {sid} anchor={r['atoks'][0] if r['atoks'] else '-'} "
                         f"by={ex[0]}:{ex[1]} correction={ex[3]}")
        for cell_idx, tok, ell in r["rtoks"]:
            if cell_idx != ANCHOR_CELL:
                defects.append(f"DEFECT {sid} anchor token={tok} class=token-outside-anchor "
                               f"detail=sha256-claim-in-cell-{cell_idx + 1}-of-{NCELLS} "
                               f"loc=corpus/SOURCES.md:{lineno}")
                continue
            if not row_scope:
                defects.append(f"DEFECT {sid} anchor token={tok} class=anchor-unbound "
                               f"detail={unbound.get(sid, 'no-capture-derivable-from-this-row')} "
                               f"loc=corpus/SOURCES.md:{lineno}")
                continue
            if ex:
                continue
            names = sorted({v[0] for v in row_scope.values()})
            if ell:
                if not (8 <= len(tok) <= 63 and tok == tok.lower()):
                    defects.append(f"DEFECT {sid} anchor token={tok} class=abbrev-unresolved "
                                   f"detail=prefix-needs-8-63-lowercase-hex loc=corpus/SOURCES.md:{lineno}")
                elif not any(d.startswith(tok) for d in row_scope):
                    defects.append(f"DEFECT {sid} anchor token={tok} class=abbrev-unresolved "
                                   f"detail=no-digest-of-the-capture-this-row-names-starts-with-this-prefix "
                                   f"capture={','.join(names)} loc=corpus/SOURCES.md:{lineno}")
                elif verbose:
                    notes.append(f"ABBREV {sid} prefix={tok} "
                                 f"matches={sorted(d for d in row_scope if d.startswith(tok))[0]}")
                continue
            if not HEX64.fullmatch(tok):
                if len(tok) != 64:
                    cls, why = ("digest-short" if len(tok) < 64 else "digest-long"), f"{len(tok)}-hex"
                else:
                    cls, why = "digest-uppercase", "64-hex-but-not-lowercase"
                defects.append(f"DEFECT {sid} anchor token={tok} class={cls} detail={why} "
                               f"loc=corpus/SOURCES.md:{lineno}")
            elif tok not in row_scope:
                if tok in allowed:
                    other = idx["examples"].get(tok, "?")
                    defects.append(f"DEFECT {sid} anchor token={tok} class=digest-wrong-capture "
                                   f"detail=committed-capture-belonging-to-another-capture"
                                   f"-{other}-not-the-capture-this-row-names-{','.join(names)} "
                                   f"loc=corpus/SOURCES.md:{lineno}")
                else:
                    defects.append(f"DEFECT {sid} anchor token={tok} class=digest-unknown "
                                   f"detail=not-committed-evidence-and-not-in-a-SHA256SUMS "
                                   f"loc=corpus/SOURCES.md:{lineno}")
            elif verbose:
                path, how, label = row_scope[tok]
                notes.append(f"RESOLVED {sid} digest={tok} via={path} bind={how} listed={label}")

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
