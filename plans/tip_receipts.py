#!/usr/bin/env python3
"""Tip receipts (kengaku round 38, assimilation of considerthese/2026-10-25 proposal 2(c)).

  python3 tip_receipts.py --lane DIR [--work DIR] [--list] [--tamper REL[,REL]] [--only SUBSTR] [--jobs N]

A receipt is only evidence if something re-runs it at the tip. This tool enumerates the committed probe
receipts under the lane's `corpus/evidence/`, resolves each one's committed re-run command from the probe
script's own `Run as:` line (the same line SKILL.md's gate/probe registry and corpus/README.md quote),
clones the lane at HEAD into a scratch directory, re-runs every probe inside that clone and byte-compares
its stdout with the receipt blob as committed at HEAD.

Population, stated mechanically: committed files `corpus/evidence/**/*probe*.{txt,log}`. A file enters the
byte-comparison if the RECEIPTS table maps it to a committed probe script, or — the table being an override
list, not a census — if its own basename resolves to exactly one committed `plans/*.py` probe: with
non-alphanumerics dropped and case folded, the receipt stem `git-leak-probe` and the script stem
`git_leak_probe` are the same token. A derived mapping is strict (`kind=byte`) and `--list` prints
`origin=derived` for it, so a round's new receipt is re-run without a table edit and the table stays the
place where a declared-bounded kind is written. Every other file is printed on its own `skip
reason=no-committed-re-run-command` line, so nothing is dropped silently. A mapped receipt whose script is
gone, whose dependency is absent, or whose divergence is declared and bounded is printed as `skip` with the
reason. A receipt that declares embedded scratch paths (`temp-paths`) is still re-run: absolute mkdtemp
paths are masked on both sides, so equality after masking is a reproducibility claim up to those paths, and
any other difference is still `differ`.

Controls: `--tamper REL` (repeatable, comma-splittable) flips one byte of that receipt's committed bytes
and re-compares the same fresh output: the comparator must answer `differ`. With no `--tamper`, one control
runs automatically on the cheapest byte-equal receipt. A control that answers `equal` exits 1.

Exit codes: 0 every mapped receipt reproduces (equal, or declared-bounded skip) and the control reports
`differ`; 1 a `differ`, a failed control, or a probe that did not complete (exit != 0); 2 usage/setup
(lane not a git work-tree root, no `corpus/evidence/`, absent git, clone or cleanup failure,
unknown `--tamper` id).

Write scope: the lane is read only (`git ls-tree`, `git show`, `git rev-parse`); every probe runs in the
scratch clone with TMPDIR/TEMP/TMP inside the work directory (--work, else the environment's TMPDIR, else
the platform temp dir) and the work directory is removed on exit. No receipt is ever written.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import os
import pathlib
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

EVIDENCE = "corpus/evidence"
CANDIDATE_RE = re.compile(r"probe.*\.(?:txt|log)$", re.IGNORECASE)
# Absolute scratch dirs created by tempfile.mkdtemp (…/tmpXXXXXXXX). Masked on both sides for receipts
# declared `temp-paths`: their divergence is exactly a recorded mkdtemp path.
MASK_RE = re.compile(rb"(?:/[A-Za-z0-9._+-]+)*/tmp[A-Za-z0-9_]{6,}")

# receipt -> (committed probe script, kind). kind "byte" must reproduce exactly; kind "temp-paths"
# declares embedded mkdtemp paths (round-36 claims: the first run kept its own /tmp/… in two assertion
# strings; the amended receipt masks them, so the first-run record is reproducible only up to them).
RECEIPTS = {
    "corpus/evidence/round35/tb2-grader-probe.txt": ("plans/tb2_grader_probe.py", "byte"),
    "corpus/evidence/round36/regex-log-probe.txt": ("plans/regex_log_probe.py", "byte"),
    "corpus/evidence/round36/regex-log-probe-first-run.txt": ("plans/regex_log_probe.py", "temp-paths"),
    "corpus/evidence/round37/git-webserver-probe.txt": ("plans/git_webserver_probe.py", "byte"),
    "corpus/evidence/round38/build-pmars-probe.txt": ("plans/build_pmars_probe.py", "byte"),
}
# Fallback argv tails, used only when a script's `Run as:` line cannot be parsed.
FALLBACK = {
    "plans/tb2_grader_probe.py": ["uv", "run", "--no-project", "--with", "biopython==1.85", "python3",
                                  "plans/tb2_grader_probe.py", "--lane", "."],
    "plans/regex_log_probe.py": ["python3", "plans/regex_log_probe.py", "--lane", "."],
    "plans/git_webserver_probe.py": ["python3", "plans/git_webserver_probe.py", "--lane", "."],
    "plans/build_pmars_probe.py": ["python3", "plans/build_pmars_probe.py", "--lane", "."],
}
DOC_SOURCES = ("SKILL.md", "README.md", "corpus/README.md")
DOC_GLOBS = ("plans/*.py", "plans/*.md", "plans/*.json", "corpus/knowledge/*.md")

# Receipt stem == script stem once non-alphanumerics are dropped and case folded. Exact match only: a
# `-first-run` sibling or a `probe-r19-*` log resolves to nothing, and a stem two scripts share resolves
# to nothing either — the receipt then stays unmapped and keeps its printed reason.
STEM_RE = re.compile(r"[^a-z0-9]+")


def stem(name: str) -> str:
    return STEM_RE.sub("", name.lower())


def derive_map(lane: pathlib.Path) -> dict[str, tuple[str, str, str]]:
    """receipt -> (script, "byte", "derived") for candidates the RECEIPTS table does not name."""
    by_stem: dict[str, list[str]] = {}
    for rel in git(lane, "ls-tree", "-r", "HEAD", "--name-only", "plans").decode().splitlines():
        rel = rel.strip()
        if rel.startswith("plans/") and rel.endswith(".py") and "/" not in rel[len("plans/"):]:
            by_stem.setdefault(stem(pathlib.Path(rel).stem), []).append(rel)
    out: dict[str, tuple[str, str, str]] = {}
    for rel in candidates(lane):
        if rel in RECEIPTS:
            continue
        hit = by_stem.get(stem(pathlib.Path(rel).stem), [])
        if len(hit) == 1:
            out[rel] = (hit[0], "byte", "derived")
    return out


def die(msg: str) -> "NoReturn":  # noqa: F821
    print(f"SETUP: {msg}")
    raise SystemExit(2)


def git(lane: pathlib.Path, *argv: str, check: bool = True) -> bytes:
    r = subprocess.run(["git", "-C", str(lane), *argv], capture_output=True)
    if check and r.returncode != 0:
        die(f"git {' '.join(argv)} failed: {r.stderr.decode(errors='replace').strip()[:200]}")
    return r.stdout


def lane_root(lane: pathlib.Path) -> pathlib.Path:
    if shutil.which("git") is None:
        die("git not found on PATH")
    if not lane.is_dir():
        die(f"--lane {lane} is not a directory")
    top = git(lane, "rev-parse", "--show-toplevel").decode().strip()
    if not top or pathlib.Path(top).resolve() != lane.resolve():
        die(f"--lane {lane} is not a git work-tree root (rev-parse says {top or 'nothing'})")
    return lane.resolve()


def candidates(lane: pathlib.Path) -> list[str]:
    out = git(lane, "ls-tree", "-r", "HEAD", "--name-only", EVIDENCE)
    rels = [p for p in out.decode().splitlines() if p.strip()]
    return sorted(p for p in rels if CANDIDATE_RE.search(p.rsplit("/", 1)[-1]))


def committed_bytes(clone: pathlib.Path, rel: str) -> bytes:
    return git(clone, "show", f"HEAD:{rel}")


def usage_argv(clone: pathlib.Path, script: str) -> tuple[list[str], str]:
    """The script's own `Run as:` line, split; fallback table otherwise."""
    path = clone / script
    if not path.is_file():
        return [], "script-absent"
    base = path.name
    for line in path.read_text(errors="replace").splitlines():
        s = line.strip()
        if s.startswith(("python3 ", "uv run ")) and base in s:
            # docstrings pad the command with 2+ spaces before a prose description: keep only the command
            try:
                argv = shlex.split(re.split(r"\s{2,}", s)[0])
            except ValueError:
                break
            if "--lane" not in argv:
                argv += ["--lane", "."]
            return argv, "docstring"
    if script in FALLBACK:
        return list(FALLBACK[script]), "fallback"
    return [], "no-command"


def provenance(lane: pathlib.Path, receipt: str, script: str) -> str:
    """Where the lane's committed text names both the script and this receipt (file:line[:line])."""
    receipt_hits: list[str] = []
    script_hits: list[str] = []
    files = [lane / n for n in DOC_SOURCES] + [
        p for g in DOC_GLOBS for p in sorted(lane.glob(g))
    ]
    for path in files:
        try:
            if not path.is_file() or path.stat().st_size > 2_000_000:
                continue
        except OSError:
            continue
        rel = path.relative_to(lane).as_posix()
        for n, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
            if script in line:
                script_hits.append(f"{rel}:{n}")
            if receipt.rsplit("/", 1)[-1] in line:
                receipt_hits.append(f"{rel}:{n}")
    if script_hits and receipt_hits:
        return f"{script_hits[0]}+{receipt_hits[0]}"
    if script_hits:
        return f"command={script_hits[0]},receipt=undocumented"
    return "undocumented"


def first_diff(a: bytes, b: bytes) -> str:
    n = min(len(a), len(b))
    for i in range(n):
        if a[i] != b[i]:
            line = a.count(b"\n", 0, i) + 1
            return f"byte {i} (line {line})"
    if len(a) != len(b):
        return f"length {len(a)} != {len(b)}"
    return "-"


def mask(data: bytes) -> bytes:
    return MASK_RE.sub(b"<tmp>", data)


def run_probe(clone: pathlib.Path, argv: list[str], tmpdir: pathlib.Path, timeout: int) -> dict:
    tmpdir.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env.update(TMPDIR=str(tmpdir), TEMP=str(tmpdir), TMP=str(tmpdir), PYTHONDONTWRITEBYTECODE="1")
    try:
        r = subprocess.run(argv, cwd=str(clone), env=env, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"exit": "timeout", "out": b"", "err": f"timeout after {timeout}s"}
    except FileNotFoundError:
        return {"exit": "missing", "out": b"", "err": f"{argv[0]}: not found"}
    return {"exit": r.returncode, "out": r.stdout, "err": r.stderr.decode(errors="replace")}


def tamper_one_byte(data: bytes) -> tuple[bytes, int, int, int]:
    """Flip one byte in the middle of the receipt, preferring a non-newline, non-space byte."""
    if not data:
        return data, 0, 0, 0
    start = len(data) // 2
    for off in list(range(start, len(data))) + list(range(start - 1, -1, -1)):
        b = data[off]
        if b not in (0x0A, 0x0D, 0x20, 0x09):
            nb = b ^ 0x01
            return data[:off] + bytes([nb]) + data[off + 1:], off, b, nb
    b = data[start]
    nb = b ^ 0x01
    return data[:start] + bytes([nb]) + data[start + 1:], start, b, nb


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0], add_help=True)
    ap.add_argument("--lane", default=".", help="lane work-tree root (default: .)")
    ap.add_argument("--work", default=None, help="scratch parent (default: TMPDIR/mkdtemp)")
    ap.add_argument("--list", action="store_true", help="classify receipts and print commands; run nothing")
    ap.add_argument("--tamper", action="append", default=[], help="receipt rel path(s) for the control")
    ap.add_argument("--only", default=None, help="restrict to receipts whose rel path contains this")
    ap.add_argument("--jobs", type=int, default=4, help="probes run in parallel (default: 4)")
    ap.add_argument("--timeout", type=int, default=1800, help="per-probe timeout seconds (default: 1800)")
    args = ap.parse_args()

    lane = lane_root(pathlib.Path(args.lane))
    if not (lane / EVIDENCE).is_dir():
        die(f"--lane {lane} has no {EVIDENCE} directory: not a kengaku lane?")
    tip = git(lane, "rev-parse", "HEAD").decode().strip()
    found = candidates(lane)
    plan: dict[str, tuple[str, str, str]] = {r: (s, k, "table") for r, (s, k) in RECEIPTS.items()}
    plan.update(derive_map(lane))
    mapped = [r for r in found if r in plan]
    unmapped = [r for r in found if r not in plan]
    if args.only:
        mapped = [r for r in mapped if args.only in r]
        unmapped = [r for r in unmapped if args.only in r]

    if args.list:
        print(f"tip {tip}")
        for rel in mapped:
            script, kind, origin = plan[rel]
            print(f"receipt {rel} kind={kind} script={script} origin={origin} "
                  f"provenance={provenance(lane, rel, script)}")
        for rel in unmapped:
            print(f"receipt {rel} skip reason=no-committed-re-run-command")
        return 0

    work_parent = pathlib.Path(args.work).resolve() if args.work else None
    if work_parent is not None:
        work_parent.mkdir(parents=True, exist_ok=True)
    ws = pathlib.Path(tempfile.mkdtemp(prefix="tip-receipts-", dir=str(work_parent) if work_parent else None))
    results: dict[str, dict] = {}
    try:
        clone = ws / "tip"
        subprocess.run(["git", "clone", "-q", "--shared", str(lane), str(clone)], check=True)
        top = git(clone, "rev-parse", "--show-toplevel").decode().strip()
        if pathlib.Path(top).resolve() != clone.resolve():
            die(f"clone toplevel {top} != {clone}")
        head = git(clone, "rev-parse", "HEAD").decode().strip()
        if head != tip:
            die(f"clone HEAD {head} != lane tip {tip}")

        # Resolve commands from the clone's committed scripts before any run.
        for rel in mapped:
            script, kind, _origin = plan[rel]
            argv, origin = usage_argv(clone, script)
            results[rel] = {
                "kind": kind, "script": script, "argv": argv, "origin": origin,
                "prov": provenance(lane, rel, script),
                "blob": committed_bytes(clone, rel) if (clone / rel).exists() else None,
            }
            if not (clone / script).is_file():
                results[rel].update(skip=f"probe-script-absent:{script}")
            elif not argv:
                results[rel].update(skip=f"no-committed-re-run-command:{origin}")
            elif shutil.which(argv[0]) is None:
                results[rel].update(skip=f"dependency-missing:{argv[0]}")
            if "skip" in results[rel]:
                results[rel].update(verdict="skip", why=results[rel]["skip"])

        todo = [rel for rel in mapped if "skip" not in results[rel]]
        jobs = max(1, min(args.jobs, len(todo) or 1))
        with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
            futs = {
                pool.submit(run_probe, clone, results[rel]["argv"],
                            ws / "tmp" / re.sub(r"[^A-Za-z0-9]+", "-", rel), args.timeout): rel
                for rel in todo
            }
            for fut, rel in ((f, futs[f]) for f in concurrent.futures.as_completed(futs)):
                results[rel]["run"] = fut.result()

        for rel in mapped:
            res = results[rel]
            if "skip" in res:
                continue
            run = res["run"]
            fresh, blob = run["out"], res["blob"]
            res["fresh"] = fresh
            if run["exit"] != 0:
                res["verdict"] = "differ"
                res["why"] = f"probe exit={run['exit']} ({run['err'].strip().splitlines()[-1][:120] if run['err'].strip() else 'no stderr'})"
                continue
            if res["kind"] == "temp-paths":
                if mask(fresh) == mask(blob):
                    res["verdict"] = "skip"
                    res["why"] = "declared-nonreproducible-absolute-scratch-paths (equal after masking)"
                else:
                    res["verdict"] = "differ"
                    res["why"] = "masked bytes differ: " + first_diff(mask(fresh), mask(blob))
                continue
            if fresh == blob:
                res["verdict"] = "equal"
            else:
                res["verdict"] = "differ"
                res["why"] = "first_diff=" + first_diff(fresh, blob)

        # Control: one byte flipped in the receipt must be reported differ.
        tamper = [t for spec in args.tamper for t in spec.split(",") if t]
        if tamper:
            unknown = [t for t in tamper if t not in results]
            if unknown:
                die(f"--tamper {','.join(unknown)} is not a mapped receipt")
            controls = tamper
        else:
            equal = [r for r in mapped if results[r].get("verdict") == "equal"]
            controls = [min(equal, key=lambda r: len(results[r]["blob"]))] if equal else []
        control_lines = []
        control_ok = True
        for rel in controls:
            res = results[rel]
            if "fresh" not in res or not res["blob"]:
                control_lines.append(f"control receipt={rel} verdict=unavailable")
                control_ok = False
                continue
            bad, off, ob, nb = tamper_one_byte(res["blob"])
            same = mask(res["fresh"]) == mask(bad) if res["kind"] == "temp-paths" else res["fresh"] == bad
            control_lines.append(
                f"control receipt={rel} flip=byte {off} 0x{ob:02x}->0x{nb:02x} verdict={'equal' if same else 'differ'}"
            )
            control_ok = control_ok and not same
    finally:
        shutil.rmtree(ws, ignore_errors=True)

    print(f"tip {tip}")
    for rel in unmapped:
        print(f"receipt {rel} skip reason=no-committed-re-run-command")
    for rel in mapped:
        res = results[rel]
        if res["verdict"] == "equal":
            print(f"receipt {rel} equal bytes={len(res['blob'])} exit=0 doc={res['prov']}")
        elif res["verdict"] == "skip":
            print(f"receipt {rel} skip reason={res['why']} doc={res['prov']}")
        else:
            print(f"receipt {rel} differ {res['why']} exit={res['run']['exit']} doc={res['prov']}")
    for line in control_lines:
        print(line)

    n = len(mapped) + len(unmapped)
    strict = [r for r in mapped if results[r]["kind"] == "byte"]
    no_cmd = len(unmapped) + sum(
        1 for r in mapped if str(results[r].get("why", "")).startswith("no-committed-re-run-command"))
    print(f"note compared={len(strict)} declared_bounded={len(mapped) - len(strict)} "
          f"no_command={no_cmd}")
    k = sum(1 for r in mapped if results[r].get("verdict") == "equal")
    d = sum(1 for r in mapped if results[r].get("verdict") == "differ")
    s = n - k - d
    print(f"receipts={n} byte_equal={k} differ={d} skipped={s}")
    return 0 if d == 0 and control_ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:  # `| head` must not print a traceback
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        sys.exit(0)
