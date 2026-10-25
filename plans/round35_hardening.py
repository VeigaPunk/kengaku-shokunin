#!/usr/bin/env python3
"""Round-35 POST-HOC hardening checks — NOT the rule of either frozen claim.

Written after wave-1 seats showed false greens in the frozen counters (R35CritControls: a junk
package passes plans/round35_c1_verify.py; R35CritC2: labelled-but-false D4/D5 lines pass
plans/defect_ledger.py; R35MutC1Quotes: unparsed quote rows are skipped). The frozen predicates stay
as declared in plans/round-35-claims.md; this script is the round's `## Mistakes` fix, shown able to
fail on those seats' counterexamples, and the candidate rule for the next round's counters.

  H1 frozen instruments unchanged: probe/counter/ledger bytes equal their blobs at the freeze commit
  H2 every `## Located quotes` table row parses; >=8 distinct quotes of >=3 words at >=8 distinct lines
  H3 S105-S107 teaches cells carry >=8 words
  H4 D4 correction is directional: each citation is followed in the same clause by its own token
  H5 D5 erratum asserts `is present` (never `not present`) and the capture matches its manifest digest
  H6 the lane workspace has no untracked file at all (D1 class, whole tree)
Usage: round35_hardening.py --lane <dir> [--freeze 11d6453...] [--skip H6]
"""
import argparse
import hashlib
import pathlib
import re
import subprocess
import sys

FREEZE = "11d64530179b78e33ba6074fc77d63d36ee7ac31"
FROZEN = ["plans/tb2_grader_probe.py", "plans/round35_c1_verify.py", "plans/defect_ledger.py"]
ENTRY = "corpus/knowledge/tb2-protein-assembly-grader.md"
L34 = ".ufo/waves/round-34/"


def git(lane, *a):
    return subprocess.run(["git", "-C", str(lane), *a], capture_output=True, text=True)


def h1(lane, repo):
    bad = []
    for p in FROZEN:
        blob = subprocess.run(["git", "-C", str(repo), "show", f"{FREEZE}:{p}"], capture_output=True).stdout
        f = lane / p
        if not f.is_file() or f.read_bytes() != blob:
            bad.append(p)
    return (not bad, f"changed_since_freeze={bad or 0}")


def h2(lane, _repo):
    t = (lane / ENTRY).read_text()
    sec = re.search(r"^## Located quotes\n(.*?)(?=^## |\Z)", t, re.S | re.M)
    if not sec:
        return (False, "no section")
    rows = [l for l in sec.group(1).splitlines() if l.startswith("|") and not re.match(r"^\|[\s|:-]+\|$", l)]
    rows = rows[1:]  # header
    pat = re.compile(r"^\|[^|]*\|\s*“(.+?)”\s*\|\s*`([^`:]+):(\d+)(?:-(\d+))?`\s*\|\s*$")
    parsed = [pat.match(r) for r in rows]
    unparsed = sum(m is None for m in parsed)
    ok = [m for m in parsed if m and len(m.group(1).split()) >= 3]
    quotes = {m.group(1) for m in ok}
    locs = {(m.group(2), m.group(3)) for m in ok}
    good = unparsed == 0 and len(quotes) >= 8 and len(locs) >= 8
    return (good, f"rows={len(rows)} unparsed={unparsed} distinct_quotes={len(quotes)} distinct_lines={len(locs)}")


def h3(lane, _repo):
    short = []
    for line in (lane / "corpus/SOURCES.md").read_text().splitlines():
        m = re.match(r"^ {0,3}\|\s*(S10[5-7])\s*\|", line)
        if m:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != 11 or len(cells[6].split()) < 8:
                short.append(m.group(1))
    return (not short, f"short_teaches={short or 0}")


def h4(lane, _repo):
    corr = [l for l in (lane / "SCORECARD.md").read_text().splitlines()
            if l.startswith("- **D4 correction (round 34 C2):**")]
    if len(corr) != 1:
        return (False, f"correction_lines={len(corr)}")
    c = corr[0]
    a = re.search(r"R34C2CounterDraft\.md:8\W{0,3}\s+records\s+\W?SELFTEST cases=10 failed=0", c)
    b = re.search(r"R34MutC2Harness\.md:12\W{0,3}[^;]{0,80}?SELFTEST green failed", c)
    green = re.search(r"counter draft's selftest was green", c)
    return (bool(a and b and green), f"draft_clause={bool(a)} harness_clause={bool(b)} green_word={bool(green)}")


def h5(lane, _repo):
    l34 = (lane / "corpus/lessons/round-34.md").read_text().splitlines()
    err = [l for l in l34 if l.startswith("Erratum (round 35):")]
    if len(err) != 1:
        return (False, f"erratum_lines={len(err)}")
    e = err[0]
    directional = "is present" in e and "not present" not in e
    cap = lane / (L34 + "assimilation/captures/nec-s091-reopen.html")
    sums = (lane / (L34 + "assimilation/captures/quarantine-SHA256SUMS")).read_text()
    dig = hashlib.sha256(cap.read_bytes()).hexdigest()
    pinned = any(l.split()[0] == dig and l.split()[-1].endswith("nec-s091-reopen.html") for l in sums.splitlines() if l.strip())
    return (directional and pinned, f"directional={directional} capture_pinned={pinned}")


def h6(lane, _repo):
    out = git(lane, "ls-files", "--others", "--exclude-standard").stdout.split("\n")
    n = len([x for x in out if x])
    return (n == 0, f"untracked_anywhere={n}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--repo", default=None, help="git repo holding the freeze commit (default: --lane)")
    ap.add_argument("--skip", action="append", default=[])
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    repo = pathlib.Path(a.repo).resolve() if a.repo else lane
    bad = 0
    run = 0
    for name, fn in (("H1", h1), ("H2", h2), ("H3", h3), ("H4", h4), ("H5", h5), ("H6", h6)):
        if name in a.skip:
            print(f"{name} skipped")
            continue
        run += 1
        try:
            ok, note = fn(lane, repo)
        except Exception as e:
            ok, note = False, f"error {type(e).__name__}: {e}"
        bad += not ok
        print(f"{name} {'ok' if ok else 'FAIL'} {note}")
    print(f"hardening run={run} failed={bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
