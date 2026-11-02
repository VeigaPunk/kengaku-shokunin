#!/usr/bin/env python3
"""Receipt self-consistency gate (kengaku round 59, C2).

Class closed: a receipt whose own cross-checkable fields contradict each other — the
round-58 closure's finding (b): `.ufo/waves/round-58/recon/esc-falsifier-fixed-checker.txt`
prints `exit=0` under the fx-red and fx-words sections whose ANCHORLINE lines carry
`live=1` (the anchor checker's exit map is 1 iff any live defect), while the same file's
selftest lines record `rc=1 want_rc=1 ok` for both classes. The payload was correct, the
labels were a capture bug, and only a human reader caught it. This gate catches the class
mechanically.

Population: every committed receipt file under `.ufo/waves/` and `corpus/evidence/` with a
`.txt` or `.log` suffix. Read from the worktree — on a clean tree these are the committed
bytes (run on a clean clone or a clean worktree; a dirty tree is refused, exit 2).

Rules (each compares two fields the receipt itself carries):
  R1 exit-vs-payload — a bare `exit=<n>` label line must agree with the nearest preceding
     `ANCHORLINE … live=<k>` line in the same file: n == 1 iff k > 0. A bare `exit=` line
     with no preceding ANCHORLINE in the file is an `unanchored` defect (a label nothing in
     the file supports).
  R2 selftest-label — a `SELFTEST <id> rc=<a> want_rc=<b> <label>` line must carry `ok`
     only when a == b, and `FAIL` only when a != b.
  R3 selftest-summary — a `SELFTEST pass` summary line is a defect when any SELFTEST
     rc/want line since the previous summary is R2-inconsistent (the summary whitewashes a
     contradicting line — counted once, the line's own R2 defect still stands), or when no
     such line precedes it at all (a vacuous pass).

Erratum discipline (R1/Q26 house form — corrections are appended, never rewritten): a file
carrying a dated erratum marker that names this gate — a `===`-delimited block containing
both the string `ERRATUM (round` and the token `receipt_consistency_check` — has its
defects counted as `errata=<n>` instead of `defects=<n>`: declared, dated, still printed.
Exit 0 iff undeclared defects == 0. A foreign `===` block without the token converts
nothing. The erratum must carry the wrong label, the right value and the reason; the gate
counts, it does not judge prose.

Verdict lines:
  files=<scanned> anchored-exit-pairs=<pairs> selftest-lines=<lines> defects=<d> errata=<e>
  PREDICATE R59-C2 pass|fail
Exit codes: 0 pass · 1 fail · 2 setup (dirty tree, not a git work tree).

Run as:
  python3 plans/receipt_consistency_check.py --lane .
  python3 plans/receipt_consistency_check.py --selftest
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

POPS = (".ufo/waves", "corpus/evidence")
SUFFIXES = (".txt", ".log")
ANCHOR_RE = re.compile(r"^ANCHORLINE\b.*?\blive=(\d+)\b", re.M)
EXIT_RE = re.compile(r"^[ \t]+exit=(\d+)[ \t]*$")
SELF_RE = re.compile(r"^SELFTEST\s+(\S+)\s+rc=(\d+)\s+want_rc=(\d+)\s+(ok|FAIL)\b")
PASS_RE = re.compile(r"^SELFTEST pass[ \t]*$")
SEGMENT_RE = re.compile(r"^===.*$", re.M)


def file_state(text: str):
    """Returns a list of (description, kind) defects; kind in
    {exit-vs-payload, unanchored, selftest-label, selftest-summary}."""
    defects = []
    last_live = None
    seen_self = []          # (rc, want, label, lineno) since last summary
    saw_any_since_summary = False
    for lineno, ln in enumerate(text.splitlines(), 1):
        a = ANCHOR_RE.match(ln)
        if a:
            last_live = int(a.group(1))
            continue
        e = EXIT_RE.match(ln)
        if e:
            if last_live is None:
                defects.append((f"line {lineno}: bare exit={e.group(1)} with no preceding "
                                f"ANCHORLINE (unanchored label)", "unanchored"))
            else:
                want = 1 if last_live > 0 else 0
                if int(e.group(1)) != want:
                    defects.append((f"line {lineno}: exit={e.group(1)} after ANCHORLINE "
                                    f"live={last_live} (exit map wants {want})",
                                    "exit-vs-payload"))
                last_live = None
            continue
        s = SELF_RE.match(ln)
        if s:
            rc, want, lab = int(s.group(2)), int(s.group(3)), s.group(4)
            if (rc == want) != (lab == "ok"):
                defects.append((f"line {lineno}: SELFTEST rc={rc} want_rc={want} {lab} "
                                f"(label contradicts the fields)", "selftest-label"))
            seen_self.append((rc, want, lab))
            saw_any_since_summary = True
            continue
        if PASS_RE.match(ln):
            inconsistent = any((rc == want) != (lab == "ok") for (rc, want, lab) in seen_self)
            if inconsistent:
                defects.append((f"line {lineno}: 'SELFTEST pass' summary under a "
                                f"contradicting selftest line", "selftest-summary"))
            elif not saw_any_since_summary:
                defects.append((f"line {lineno}: 'SELFTEST pass' summary with no "
                                f"rc/want line before it (vacuous pass)", "selftest-summary"))
            seen_self = []
            saw_any_since_summary = False
    return defects


def has_erratum_marker(text: str) -> bool:
    """True when some ===-delimited block names both an ERRATUM (round N) and this gate."""
    matches = list(SEGMENT_RE.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        seg = text[m.start():end]
        if "ERRATUM (round" in seg and "receipt_consistency_check" in seg:
            return True
    return False


def collect(lane: pathlib.Path):
    files = []
    for pop in POPS:
        d = lane / pop
        if d.is_dir():
            files += sorted(p for p in d.rglob("*")
                            if p.is_file() and p.suffix in SUFFIXES)
    return files


def scan(files, lane: pathlib.Path, lines: list[str]):
    tot_d = tot_e = pairs = selfs = 0
    for p in files:
        try:
            text = p.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            text = p.read_bytes().decode("utf-8", errors="replace")
        d = file_state(text)
        if has_erratum_marker(text):
            e, d = d, []
        else:
            e = []
        if d or e:
            rel = p.relative_to(lane)
            lines.append(f"FILE {rel} defects={len(d)} errata={len(e)}"
                         + ("".join(" :: " + x[0] for x in d + e)))
        tot_d += len(d)
        tot_e += len(e)
        pairs += len(ANCHOR_RE.findall(text))
        selfs += len(SELF_RE.findall(text))
    return tot_d, tot_e, len(files), pairs, selfs


def verdict(lane: pathlib.Path, lines: list[str]) -> int:
    st = subprocess.run(["git", "-C", str(lane), "status", "--porcelain"],
                        capture_output=True, text=True)
    if st.returncode != 0:
        lines.append(f"SETUP not a git work tree: {lane}")
        return 2
    if st.stdout.strip():
        lines.append("SETUP dirty work tree — run on a clean clone or commit first")
        return 2
    tot_d, tot_e, nfiles, pairs, selfs = scan(collect(lane), lane, lines)
    lines.append(f"files={nfiles} anchored-exit-pairs={pairs} selftest-lines={selfs} "
                 f"defects={tot_d} errata={tot_e}")
    ok = tot_d == 0
    lines.append(f"PREDICATE R59-C2 {'pass' if ok else 'fail'}")
    return 0 if ok else 1


def selftest() -> int:
    """Eight fixtures in a temp tree: consistent receipts pass; each broken class fails;
    a gate-naming erratum converts its defects to errata; a foreign === block does not."""
    fails = 0
    import tempfile

    OK1 = ("ANCHORLINE rows=1 cited=1 captured=1 uncaptured=0 defective=0 repaired=0 "
           "live=0 cells=0\n   exit=0\n")
    OK2 = ("ANCHORLINE rows=1 cited=1 captured=1 uncaptured=0 defective=1 repaired=0 "
           "live=1 cells=1\n   exit=1\n")
    BAD1 = ("ANCHORLINE rows=1 cited=1 captured=1 uncaptured=0 defective=1 repaired=0 "
            "live=1 cells=1\n   exit=0\n")
    BAD2 = ("ANCHORLINE rows=1 cited=1 captured=1 uncaptured=0 defective=0 repaired=0 "
            "live=0 cells=0\n   exit=1\n")
    UNANCHORED = "some other receipt line\n   exit=0\n"
    SELF_OK = "SELFTEST A rc=1 want_rc=1 ok\nSELFTEST pass\n"
    SELF_BAD = "SELFTEST B rc=0 want_rc=1 ok\nSELFTEST pass\n"
    SELF_LABELED = "SELFTEST C rc=0 want_rc=0 ok\nSELFTEST C rc=1 want_rc=1 FAIL\nSELFTEST pass\n"
    ERRATUM = ("=== ERRATUM (round 59, 2026-11-02) — the exit= label under fx-x above is "
               "WRONG, recorded for plans/receipt_consistency_check.py ===\n" + BAD1)

    with tempfile.TemporaryDirectory() as td:
        t = pathlib.Path(td)
        (t / ".ufo" / "waves").mkdir(parents=True)

        def make(body):
            (t / ".ufo" / "waves" / "a.txt").write_text(body)

        def run():
            lines = []
            tot_d, tot_e, nfiles, pairs, selfs = scan(collect(t), t, lines)
            summ = (f"files={nfiles} anchored-exit-pairs={pairs} selftest-lines={selfs} "
                    f"defects={tot_d} errata={tot_e}")
            return (0 if tot_d == 0 else 1), summ, lines

        # 1. clean receipts pass (a.txt ok pair; the previous case's b.log is absent — fresh tree)
        make(OK1 + OK2)
        rc, summ, _ = run()
        if rc != 0 or "defects=0 errata=0" not in summ:
            print(f"SELFTEST FAIL clean: rc={rc} {summ}")
            fails += 1
        else:
            print("SELFTEST ok clean")
        # 2. exit-vs-payload both directions fail
        make(BAD1)
        rc, summ, _ = run()
        if rc != 1 or "defects=1 errata=0" not in summ:
            print(f"SELFTEST FAIL bad1: rc={rc} {summ}")
            fails += 1
        else:
            print("SELFTEST ok bad1 (live=1 exit=0)")
        make(BAD2)
        rc, summ, _ = run()
        if rc != 1 or "defects=1 errata=0" not in summ:
            print(f"SELFTEST FAIL bad2: rc={rc} {summ}")
            fails += 1
        else:
            print("SELFTEST ok bad2 (live=0 exit=1)")
        # 3. unanchored exit label fails
        make(UNANCHORED)
        rc, summ, _ = run()
        if rc != 1 or "defects=1 errata=0" not in summ:
            print(f"SELFTEST FAIL unanchored: rc={rc} {summ}")
            fails += 1
        else:
            print("SELFTEST ok unanchored")
        # 4. selftest label contradiction: line defect + whitewashing summary = 2
        make(SELF_BAD)
        rc, summ, _ = run()
        if rc != 1 or "defects=2 errata=0" not in summ:
            print(f"SELFTEST FAIL self-bad: rc={rc} {summ}")
            fails += 1
        else:
            print("SELFTEST ok self-bad (rc=0 want_rc=1 ok + summary)")
        # 5. consistent-fields-FAIL label + summary = 2
        make(SELF_LABELED)
        rc, summ, _ = run()
        if rc != 1 or "defects=2 errata=0" not in summ:
            print(f"SELFTEST FAIL self-labeled: rc={rc} {summ}")
            fails += 1
        else:
            print("SELFTEST ok self-labeled (FAIL line + summary)")
        # 6. a gate-naming erratum converts defects to errata and passes
        make(ERRATUM)
        rc, summ, _ = run()
        if rc != 0 or "defects=0 errata=1" not in summ:
            print(f"SELFTEST FAIL erratum: rc={rc} {summ}")
            fails += 1
        else:
            print("SELFTEST ok erratum")
        # 7. a foreign === block without this gate's token converts nothing
        make("=== ERRATUM (round 40) about something else ===\n" + BAD1)
        rc, summ, _ = run()
        if rc != 1 or "defects=1 errata=0" not in summ:
            print(f"SELFTEST FAIL erratum-scope: rc={rc} {summ}")
            fails += 1
        else:
            print("SELFTEST ok erratum-scope (foreign erratum does not launder)")
        # 8. a vacuous pass summary fails
        make("SELFTEST pass\n")
        rc, summ, _ = run()
        if rc != 1 or "defects=1 errata=0" not in summ:
            print(f"SELFTEST FAIL vacuous: rc={rc} {summ}")
            fails += 1
        else:
            print("SELFTEST ok vacuous pass")

    print(f"SELFTEST cases=8 failures={fails}")
    return 0 if fails == 0 else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    lines = []
    rc = verdict(pathlib.Path(a.lane), lines)
    print("\n".join(lines))
    return rc


if __name__ == "__main__":
    sys.exit(main())
