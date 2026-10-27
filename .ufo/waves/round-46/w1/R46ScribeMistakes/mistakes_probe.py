#!/usr/bin/env python3
"""mistakes_probe.py — red/green legs for the round-45 mistake classes routed into the round-46 lesson.

Seat R46ScribeMistakes, scratch only. Reads the lane read-only; writes nothing outside --work.
Each leg prints `MISTAKE-LEG <name> <red|green> <measurement>`: `red` = the check refuses the round-45
artifact (the defect instance), `green` = the same check accepts the fixed fixture (the fix's shape).
No lane file is written; the LOG correction entry exists only as the fixture text below.
"""
import json
import pathlib
import re
import subprocess
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
WORK = pathlib.Path(sys.argv[1])
WORK.mkdir(parents=True, exist_ok=True)
assert WORK == WORK.resolve() and str(WORK).startswith("/fast/scratch/hyaku/kengaku-r46/R46ScribeMistakes"), WORK

OLD_HEAD = ("## Round 45 (hyaku run 9, 2026-10-26) — advertised fixture fence closed (10/10 refused, "
            "104 honest admitted); eleventh TB2 grader executed (second F1 exemplar)")
OLD_AB = "(A/B runs byte-equal)"

CORRECTION = '''### Round 45 LOG correction (round 46, 2026-10-27) — two round-45 lines rewritten in place; superseded bytes restored here (closure D1)

`corpus/lessons/round-45-verifier-spotcheck.md` D1: commit `3d9ea54` rewrote two lines of the round-45 entry that
`4290d64` committed. LOG.md is append-only (QUALITY R1) and the rewrite is left standing in the history — this entry
restores the superseded bytes as text, so `grep -c` on them returns 1 again. Diff command and both hunks:

```
git diff -U0 fbad1c5 3d9ea54 -- LOG.md
```

Old heading (committed `4290d64`, rewritten `3d9ea54`; LOG.md:1374):

```
## Round 45 (hyaku run 9, 2026-10-26) — advertised fixture fence closed (10/10 refused, 104 honest admitted); eleventh TB2 grader executed (second F1 exemplar)
```

Current heading (LOG.md:1374):

```
## Round 45 (hyaku run 9, 2026-10-26/27) — fixture fence landed, its frozen counter also passed by a path-keyed control (C1 not admitted); eleventh TB2 grader executed (second F1 exemplar; C2 predicate met, routed defects)
```

Old line (committed `4290d64`, rewritten `3d9ea54`; LOG.md:1388):

```
  counter `checks=11 defects=0`, `PREDICATE C2 pass` (A/B runs byte-equal); V11 `states=48 grader_pass=18
```

Current line (LOG.md:1388):

```
  counter `checks=11 defects=0`, `PREDICATE C2 pass` (A/B runs equal on every non-`ENVELOPE` line; not byte-equal — envelope scratch dirs/times differ; corrected attempt 3); V11 `states=48 grader_pass=18
```

The appended attempt-3 note at LOG.md:1393 names the old heading only in truncated form ("advertised fixture fence
closed (10/10 refused …)") and the round-45 lesson records both corrections again; neither restores the bytes.
'''


def leg(name, ok, measure):
    print(f"MISTAKE-LEG {name} {'green' if ok else 'red'} {measure}")


def log_leg():
    tip = (LANE / "LOG.md").read_text()
    red = (tip.count(OLD_HEAD), tip.count(OLD_AB))
    ok_red = red == (0, 0)
    leg("log-appendonly", False, f"red_fixture=today_log old_heading={red[0]} old_ab={red[1]}")
    fixed = tip + "\n" + CORRECTION
    green = (fixed.count(OLD_HEAD), fixed.count(OLD_AB),
             "git diff -U0 fbad1c5 3d9ea54 -- LOG.md" in fixed)
    leg("log-appendonly", green == (1, 1, True),
        f"green_fixture=log+correction old_heading={green[0]} old_ab={green[1]} diff_cmd={green[2]}")
    return ok_red, green == (1, 1, True)


def gate_rows(text):
    i = text.find("\n## Gate\n")
    if i < 0:
        return []
    j = text.find("\n## ", i + 3)
    sec = text[i:j if j > 0 else len(text)]
    rows = []
    for l in sec.splitlines():
        if not l.startswith("|"):
            continue
        cells = [c.strip() for c in l.strip("|").split("|")]
        if len(cells) >= 3 and cells[1] == "admit":
            rows.append(cells)
    return rows


def gate_ok(cells):
    reason = cells[-1]
    quotes = re.findall(r'"([^"]{1,400})"', reason) + re.findall(r"\u201c([^\u201d]{1,400})\u201d", reason)
    loc = re.search(r":\d+(-\d+)?", reason)
    return bool(loc) and any(1 <= len(q.split()) <= 25 for q in quotes)


def gate_leg():
    rows = gate_rows((LANE / "corpus/lessons/round-45.md").read_text())
    bad = [c[0] for c in rows if not gate_ok(c)]
    leg("gate-per-row-quote", False, f"red_fixture=round-45.md admit_rows={len(rows)} without_quote_and_line={len(bad)}")
    fixture = "\n## Gate\n\n| Candidate | Verdict | Reason and flip condition |\n|---|---|---|\n" + (
        '| `tests/test.sh` (S153) | admit | `test.sh:26 "echo 1 > /logs/verifier/reward.txt" (6 words)`; flips on digest change |\n'
        '| `task.toml` (S156) | admit | `task.toml:34 "allow_internet = true" (3 words)`; flips on digest change |\n')
    frows = gate_rows(fixture)
    fbad = [c[0] for c in frows if not gate_ok(c)]
    leg("gate-per-row-quote", len(frows) == 2 and not fbad,
        f"green_fixture=two_quoted_rows admit_rows={len(frows)} without_quote_and_line={len(fbad)}")
    return len(bad) == len(rows), len(frows) == 2 and not fbad


REV = re.compile(r"^REV [0-9a-f]{40}$", re.M)


def receipt_leg():
    paths = [LANE / ".ufo/waves/round-45/integrate" / n
             for n in ("measure-final.txt", "a3-tip-c1.txt", "a3-tip-c2.txt")]
    counts = {p.name: len(REV.findall(p.read_text())) for p in paths}
    leg("receipt-names-revision", False,
        "red_fixture=round-45 receipts " + " ".join(f"{k}={v}" for k, v in counts.items()))
    fixture = "ENVELOPE start 00:00:00 cwd=/x\nREV " + "0" * 40 + "\nPINS total=33 mismatched=0\n"
    leg("receipt-names-revision", len(REV.findall(fixture)) == 1, "green_fixture=one_rev_line rev_lines=1")
    return sum(counts.values()) == 0, len(REV.findall(fixture)) == 1


def amend_leg():
    commits = subprocess.run(["git", "-C", str(LANE), "rev-list", "b4fcd35..HEAD", "--",
                              "plans/round-45-claims.md"], capture_output=True, text=True, check=True).stdout.split()
    text = (LANE / "plans/round-45-claims.md").read_text()
    unnamed = [c for c in commits if c[:7] not in text]
    leg("claims-amendment-named", False,
        f"red_fixture=round-45_claims post_freeze_commits={len(commits)} unnamed={len(unnamed)}"
        + (f" first={unnamed[0][:7]}" if unnamed else ""))
    fixed = (text + "\n\n**Freeze amendments.** Post-freeze edits `52d7486` (rows S149-S156) and `9271dda` "
             "(re-pinned instruments) are named here.\n")
    remain = [c for c in commits if c[:7] not in fixed]
    leg("claims-amendment-named", not remain,
        f"green_fixture=claims+naming sentence unnamed={len(remain)}")
    return bool(unnamed), not remain


def reports_leg():
    wave = LANE / ".ufo/waves/round-45/a3w1"
    seats = json.loads((LANE / ".ufo/waves/round-45/a3w1-results.json").read_text())["results"]
    missing = [s["name"] for s in seats if not (wave / f"{s['name']}.md").is_file()]
    leg("seat-report-present", False,
        f"red_fixture=a3w1 seats={len(seats)} without_report={len(missing)}" + (f" first={missing[0]}" if missing else ""))
    d = WORK / "green-wave"
    d.mkdir(exist_ok=True)
    for n in ("A", "B"):
        (d / f"{n}.md").write_text("# report\n")
    fixture_missing = [n for n in ("A", "B") if not (d / f"{n}.md").is_file()]
    leg("seat-report-present", not fixture_missing, f"green_fixture=two_reports without_report={len(fixture_missing)}")
    return len(missing) > 0, not fixture_missing


def teaches_leg():
    rows = [l for l in (LANE / "corpus/SOURCES.md").read_text().splitlines() if l.startswith("| S154 ")]
    cells = [c.strip() for c in rows[0].strip("|").split("|")]
    teaches = cells[6]
    old = re.findall(r"'([^']{1,200})'", teaches)[0]
    cap = (LANE / "corpus/evidence/round45/tb2-password-recovery/README.md").read_text()
    leg("teaches-quote-verbatim", False,
        f"red_fixture=S154 teaches_quote={old!r} in_capture={old in cap} capture_lines={len(cap.splitlines())}")
    new = "is among the recovered passwords"
    leg("teaches-quote-verbatim", new in cap, f"green_fixture=S154_superseding_quote in_capture={new in cap}")
    return old not in cap, new in cap


def main():
    results = []
    for fn in (log_leg, gate_leg, receipt_leg, amend_leg, reports_leg, teaches_leg):
        results.append(fn())
    print(f"MISTAKE-LEGS total={len(results)} red_ok={sum(1 for r in results if r[0])} green_ok={sum(1 for r in results if r[1])}")
    return 0 if all(r[0] and r[1] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
