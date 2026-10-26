#!/usr/bin/env python3
"""Round close: the order gate and the registry census, invoked together by one command.

Mined from the round-39 closure item F39CritQ30 (`corpus/QUALITY.md` Q30): the order class
"a frozen probe must not run before its receipt is committed" is recorded as *closed by a gate*,
and `plans/order_check.py` is that gate — but nothing in the lane invoked it. Round 39's ordering
held because the seat happened to commit the receipt second, not because a command checked. A gate
nothing calls is a claim, not a gate.

This is the caller. Given `--lane . --round N` it

  1. reads `plans/round-N-claims.md` (the round's frozen claims);
  2. resolves the receipt(s) the claims name (three rules, below);
  3. runs `plans/order_check.py --lane <lane> --claims ... --receipt ...` once per receipt;
  4. runs the fleet sources census in `validate` mode against the lane's `corpus/SOURCES.md`;
  5. exits 0 only when every leg passes.

Exit: 0 every leg passed · 1 a leg FAILED (order broken, or the census reported an E-code)
· 2 setup (a leg could not be evaluated: no claims file, no order tool, no census script, an
unreadable receipt, bad arguments). A leg that cannot be evaluated is never a pass.

Receipt resolution. The claims file names its own probe; the receipt is that probe's recorded run.
The lane has written the name three ways, so all three are read, deduplicated in this order:

  (a) an explicit mention on one line, `Receipt: `corpus/evidence/round37/...-probe.txt``
      (rounds 36 and 37 write it this way);
  (b) a backticked `corpus/evidence/roundN/...-probe.txt` path for this round
      (round 37's C2 surface paragraph);
  (c) derived from a `plans/<stem>_probe.py` the claims name, as
      `corpus/evidence/roundN/<stem with _ -> ->.txt` (rounds 38-40 name only the probe script,
      e.g. `plans/db_wal_probe.py` -> `corpus/evidence/round40/db-wal-probe.txt`).

A candidate that is neither a file in the lane nor committed in HEAD is reported as
`note=skipped-unreadable-receipt` and dropped; if no candidate survives, the round has no receipt
to gate and the run is a setup error (2), never a silent pass.

Self-test (`--selftest`, needs `--lane` for the tool and registry bytes): five two-commit fixture
repos in a temp dir, each differing only in where the receipt and one `P10` line sit — excused
`P10` detail -> 0, executed `P10` detail -> 1, receipt committed first -> 1, receipt on disk but
never committed -> 2, claims naming no receipt -> 2.

Read-only: the only git commands are the ones `plans/order_check.py` itself issues, plus one
`rev-parse` and `cat-file -e` here; the census script reads `corpus/SOURCES.md` and prints TSV.
Nothing is written, no network is touched, no probe, gate or counter is imported or executed.
`--selftest` writes only inside its own temp dir.

Limits named:
  * The census leg uses `--file <lane>/corpus/SOURCES.md`, not `--root <fleet> <lane-id>`. Both
    modes resolve E11 against the lane root and print the same findings; they differ only in the
    lane label of the TSV (`file` instead of `kengaku`), so `--file` needs no fleet roster and
    works unchanged on a clone. Measured on the live lane, 2026-10-26: identical 15 W04 + 2 E11.
    The script is found from `--census`, else `$SHOKUNIN_ROOT` (the census's own root contract),
    else the lane's parents; a clone that has neither is a setup error, never a skipped leg.
  * Census W-codes are warnings by the census contract ("0 clean or warnings") and do not fail the
    leg; their count is printed so a warning storm stays visible.
  * The census leg validates the work tree; the order leg reads commits only. Run this on a clean
    clone of the tip for a measurement that does not mix the two — an uncommitted registry row is
    invisible to the clone and visible (as E11/E12) to the work tree.
  * `--lane` must be the git work-tree top: `order_check.py` resolves its `--claims`/`--receipt`
    against the work-tree root, so a subdirectory lane would silently mean different paths.
  * It gates one round, not the round series: a round whose claims file was never committed is a
    setup error (2), and this tool does not scan earlier rounds.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shlex
import subprocess
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

CLAIMS = "plans/round-{round}-claims.md"
ORDER_TOOL = "plans/order_check.py"
SOURCES = "corpus/SOURCES.md"
CENSUS_REL = Path("scripts/sources-census.sh")

# (a) `Receipt: `path.txt`` on one line -- the token must look like a repo path.
EXPLICIT_RECEIPT = re.compile(r"(?i)\breceipts?\b[^\n]*?`([^`\s]*?/[^`\s]*?\.txt)`")
# (b) a backticked evidence path for this round whose name ends in `-probe.txt`
#     (`-probe-first-run.txt` and `-dry-cases-freeze.txt` are deliberately not receipts).
EVIDENCE_RECEIPT = re.compile(r"`(corpus/evidence/round(\d+)/[^`\s]*?-probe\.txt)`")
# (c) a probe script the claims name
PROBE_SCRIPT = re.compile(r"plans/([A-Za-z0-9_.-]+?)\.py")


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_ok(lane: Path, *args: str) -> bool:
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True).returncode == 0


def norm_repo_path(lane: Path, token: str) -> str | None:
    """A token as a repo-relative posix path, or None when it points outside the lane."""
    p = Path(token)
    p = p if p.is_absolute() else (lane / p)
    try:
        return p.resolve().relative_to(lane).as_posix()
    except ValueError:
        return None


def resolve_receipts(lane: Path, text: str, round_no: int) -> tuple[list[str], list[str]]:
    """The receipts the claims name, in rule order, and the candidates that were unreadable."""
    found: list[str] = []

    def add(rel: str | None) -> None:
        if rel and rel not in found:
            found.append(rel)

    for m in EXPLICIT_RECEIPT.finditer(text):
        add(norm_repo_path(lane, m.group(1)))
    for m in EVIDENCE_RECEIPT.finditer(text):
        if int(m.group(2)) == round_no:
            add(norm_repo_path(lane, m.group(1)))
    for m in PROBE_SCRIPT.finditer(text):
        stem = m.group(1)
        if stem.endswith("_probe"):
            add(f"corpus/evidence/round{round_no}/{stem.replace('_', '-')}.txt")

    keep: list[str] = []
    dropped: list[str] = []
    for rel in found:
        if (lane / rel).is_file() or git_ok(lane, "cat-file", "-e", f"HEAD:{rel}"):
            keep.append(rel)
        else:
            dropped.append(rel)
    return keep, dropped


def find_census(lane: Path, given: str) -> Path | None:
    if given:
        p = Path(given).resolve()
        return p if p.is_file() else None
    # the census script's own contract: SHOKUNIN_ROOT, else the script's parent of parent
    env_root = os.environ.get("SHOKUNIN_ROOT", "").strip()
    if env_root and (Path(env_root) / CENSUS_REL).is_file():
        return (Path(env_root) / CENSUS_REL).resolve()
    for parent in [lane, *lane.parents][:6]:
        cand = parent / CENSUS_REL
        if cand.is_file():
            return cand
    return None


def gate(lane: Path, round_no: int, census: Path, out=sys.stdout) -> int:
    """Run both legs for one round; print the receipt; return the composite exit code."""

    def say(line: str = "") -> None:
        print(line, file=out)

    def setup(msg: str) -> int:
        print(f"ROUND-CLOSE ERROR {msg}", file=sys.stderr)
        say("ROUND-CLOSE RESULT ERROR")
        return 2

    if not lane.is_dir():
        return setup(f"not a directory: {lane}")
    top = subprocess.run(["git", "-C", str(lane), "rev-parse", "--show-toplevel"], capture_output=True)
    if top.returncode != 0:
        return setup(f"not a git work tree: {lane}")
    if Path(top.stdout.decode().strip()).resolve() != lane:
        return setup(f"--lane must be the work-tree top: {lane} (top is {top.stdout.decode().strip()})")

    claims_rel = CLAIMS.format(round=round_no)
    claims_path = lane / claims_rel
    if not claims_path.is_file():
        return setup(f"no claims file: {claims_rel}")
    order_path = lane / ORDER_TOOL
    if not order_path.is_file():
        return setup(f"no order gate: {ORDER_TOOL}")
    if not census.is_file():
        return setup(f"no census script ({CENSUS_REL}); pass --census PATH")
    if not (lane / SOURCES).is_file():
        return setup(f"no registry: {SOURCES}")

    say(f"ROUND-CLOSE lane={lane} round={round_no}")
    say(f"ROUND-CLOSE claims={claims_rel} sha256={sha256_of(claims_path)}")
    say(f"ROUND-CLOSE order-tool={ORDER_TOOL} sha256={sha256_of(order_path)}")

    receipts, dropped = resolve_receipts(lane, claims_path.read_text(encoding="utf-8", errors="replace"), round_no)
    for rel in dropped:
        say(f"ROUND-CLOSE note=skipped-unreadable-receipt {rel}")
    if not receipts:
        return setup(f"the claims name no readable receipt for round {round_no}")
    say(f"ROUND-CLOSE receipts={len(receipts)}")

    status = 0
    for rel in receipts:
        cmd = [sys.executable, str(order_path), "--lane", str(lane), "--claims", claims_rel, "--receipt", rel]
        r = subprocess.run(cmd, capture_output=True, text=True)
        out.write(r.stdout if r.stdout.endswith("\n") or not r.stdout else r.stdout + "\n")
        if r.stderr.strip():
            print(r.stderr.strip(), file=sys.stderr)
        verdict = {0: "PASS", 1: "FAIL"}.get(r.returncode, "ERROR")
        say(f"ROUND-CLOSE order receipt={rel} exit={r.returncode} verdict={verdict}")
        status = max(status, 2 if verdict == "ERROR" else (1 if verdict == "FAIL" else 0))

    cmd = [str(census), "validate", "--file", str(lane / SOURCES)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    out.write(r.stdout)
    if r.stderr.strip():
        print(r.stderr.strip(), file=sys.stderr)
    warnings = sum(1 for line in r.stdout.splitlines() if re.search(r"\tW\d\d\t", line))
    verdict = {0: "PASS", 1: "FAIL"}.get(r.returncode, "ERROR")
    say(f"ROUND-CLOSE census tool={census} sha256={sha256_of(census)} cmd={shlex.join(cmd)}")
    say(f"ROUND-CLOSE census exit={r.returncode} warnings={warnings} verdict={verdict}")
    status = max(status, 2 if verdict == "ERROR" else (1 if verdict == "FAIL" else 0))

    say(f"ROUND-CLOSE RESULT {('PASS', 'FAIL', 'ERROR')[status]} exit={status}")
    return status


# --- self-test: five two-commit fixtures, each differing only in where the receipt and one P10
# line sit. `expect` is the composite exit code the frozen order rule implies.
SELFTEST = (
    # id, control-file body, shape, expect
    ("A-excused-p10", "gate: P10 DEFECT receipt unreadable", "receipt-last", 0),
    ("B-executed-p10", "gate: P10 DEFECT fresh probe output is not byte-equal to the receipt", "receipt-last", 1),
    ("C-receipt-first", "gate: P10 DEFECT receipt unreadable", "receipt-first", 1),
    ("D-receipt-uncommitted", "gate: P10 DEFECT receipt unreadable", "receipt-uncommitted", 2),
    ("E-no-receipt-named", None, "no-probe", 2),
)
FIXTURE_CLAIMS = "# Round 39 — selftest claims\n\n**Probe (frozen):** `plans/git_leak_probe.py`.\n"
FIXTURE_CLAIMS_BARE = "# Round 39 — selftest claims\n\nNo probe and no receipt is named here.\n"
FIXTURE_RECEIPT = "CASE c01 observed=PASS predicted=PASS\n"


def build_fixture(root: Path, lane: Path, control: str | None, shape: str) -> None:
    """A minimal lane-shaped repo whose only difference between cases is commit order."""

    def commit(msg: str) -> None:
        for args in (["add", "-A"], ["commit", "-q", "-m", msg]):
            subprocess.run(["git", "-C", str(root), "-c", "user.name=fixture",
                            "-c", "user.email=fixture@localhost", *args], check=True, capture_output=True)

    def write_claims() -> None:
        claims = FIXTURE_CLAIMS_BARE if shape == "no-probe" else FIXTURE_CLAIMS
        (root / "plans/round-39-claims.md").write_text(claims, encoding="utf-8")
        if control is not None:
            (root / ".ufo/waves/round-39/claims/control-c2-nothing.txt").write_text(control + "\n", encoding="utf-8")

    for sub in ("plans", ".ufo/waves/round-39/claims", "corpus/evidence/round39"):
        (root / sub).mkdir(parents=True, exist_ok=True)
    (root / ORDER_TOOL).write_bytes((lane / ORDER_TOOL).read_bytes())
    (root / SOURCES).write_bytes((lane / SOURCES).read_bytes())
    for extra in ("corpus/knowledge", "corpus/lessons"):  # the census leg's E11 used-by targets
        src = lane / extra
        if src.is_dir():
            subprocess.run(["cp", "-a", str(src), str(root / extra)], check=True)

    receipt = root / "corpus/evidence/round39/git-leak-probe.txt"
    subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
    if shape == "receipt-first":  # the receipt lands before the claims: inverted pre-registration
        receipt.write_text(FIXTURE_RECEIPT, encoding="utf-8")
        commit("receipt")
        write_claims()
        commit("freeze")
    elif shape == "receipt-uncommitted":  # on disk, never in HEAD: setup error, not a pass
        write_claims()
        commit("freeze")
        receipt.write_text(FIXTURE_RECEIPT, encoding="utf-8")
    else:  # receipt-last (the compliant order) and no-probe
        write_claims()
        commit("freeze")
        if shape != "no-probe":
            receipt.write_text(FIXTURE_RECEIPT, encoding="utf-8")
            commit("receipt")


def selftest(lane: Path, census: Path, work: Path | None) -> int:
    base = work or Path(tempfile.mkdtemp(prefix="round-close-selftest-"))
    base.mkdir(parents=True, exist_ok=True)
    failed = 0
    for cid, control, shape, expect in SELFTEST:
        root = base / cid
        build_fixture(root, lane, control, shape)
        buf = StringIO()
        with redirect_stdout(buf), redirect_stderr(buf):
            got = gate(root.resolve(), 39, census, out=buf)
        ok = got == expect
        failed += 0 if ok else 1
        print(f"SELFTEST case={cid} shape={shape} expect={expect} got={got} verdict={'ok' if ok else 'FAIL'}")
        if not ok:
            sys.stderr.write(buf.getvalue())
    print(f"SELFTEST checks={len(SELFTEST)} ok={len(SELFTEST) - failed} failed={failed}")
    return 0 if failed == 0 else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="round close: order gate + sources census for one round")
    ap.add_argument("--lane", default=".", help="lane git work tree (its top level); read-only")
    ap.add_argument("--round", type=int, default=None, help="round number N: plans/round-N-claims.md")
    ap.add_argument("--census", default="",
                    help=f"the fleet's {CENSUS_REL} (default: $SHOKUNIN_ROOT, then the lane's parents)")
    ap.add_argument("--selftest", action="store_true", help="build five fixture repos and check the verdict map")
    ap.add_argument("--work", default="", help="--selftest scratch parent (default: a fresh temp dir)")
    args = ap.parse_args(argv)

    lane = Path(args.lane).resolve()
    census = find_census(lane, args.census)
    if args.selftest:
        if census is None:
            print(f"ROUND-CLOSE ERROR no census script ({CENSUS_REL}); pass --census PATH", file=sys.stderr)
            return 2
        if not (lane / ORDER_TOOL).is_file():
            print(f"ROUND-CLOSE ERROR no order gate: {ORDER_TOOL}", file=sys.stderr)
            return 2
        return selftest(lane, census, Path(args.work).resolve() if args.work else None)
    if args.round is None:
        ap.error("--round is required unless --selftest")
    if census is None:
        print(f"ROUND-CLOSE ERROR no census script ({CENSUS_REL}); pass --census PATH", file=sys.stderr)
        print("ROUND-CLOSE RESULT ERROR")
        return 2
    return gate(lane, args.round, census)


if __name__ == "__main__":
    sys.exit(main())
