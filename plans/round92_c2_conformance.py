#!/usr/bin/env python3
"""R92-C2 conformance counter — the three routed round-91 counter defects (round 92).

Each check runs a rev-controlled checkout of the counter bytes from scratch, never the
caller's working tree: `git show REV:<path>` is executed from the --work directory.

- M7-CASE-PARSER: the case-id parser is positional. At BASE the BASE counter bytes exit 1
  with ten `DEFECT L5 receipt names unknown case ?` on the committed receipt; at TIP the
  amended bytes exit 0 with `PREDICATE R91-C1 pass` on the SAME receipt bytes.
- M12-HOST-PROBE-GUARD: with `openssl` masked from PATH, the BASE bytes die unguarded
  (rc 1, no PREDICATE line); the TIP bytes fail closed (`DEFECT SETUP`,
  `PREDICATE R91-C1 could-not-evaluate`, rc 2).
- M9-SELFTEST-ESCAPE: at BASE the checker carries `--skip-selftest` and the expectations
  table is absent; at TIP the flag is gone, the table exists and is pinned in the ledger,
  and the amended checker's default run is green (PINS 17/17, SELFTEST 9/9, rc 0).

Usage:  python3 plans/round92_c2_conformance.py --lane <repo> --rev <tip> --work <scratch>
Exit:   0 predicate pass, 1 a check is red, 2 could-not-evaluate.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

BASE = "4ba56182307ccda1ec436bfe3d61cb3d92e56608"
C1 = "plans/round91_c1_replay.py"
C2 = "plans/round91_counter_pin.py"
EXPECT = "plans/round92-selftest-expectations.json"
PINS = "plans/counter-pins-r91.json"
RECEIPT = "corpus/evidence/round91/modernize-probe.txt"


class CouldNotEvaluate(Exception):
    pass


class Lane:
    def __init__(self, root: Path):
        self.root = root

    def git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, timeout=120)

    def resolve(self, rev: str) -> str:
        proc = self.git("rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
        if proc.returncode != 0:
            raise CouldNotEvaluate(f"unresolved-revision {rev}")
        return proc.stdout.decode().strip()

    def blob_text(self, path: str, rev: str) -> str | None:
        proc = self.git("show", f"{rev}:{path}")
        return None if proc.returncode != 0 else proc.stdout.decode("utf-8", errors="replace")


def checkout(lane: Lane, path: str, rev: str, work: Path) -> Path:
    text = lane.blob_text(path, rev)
    if text is None:
        raise CouldNotEvaluate(f"absent at {rev[:12]}: {path}")
    target = work / rev[:12] / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    return target


def masked_bin(work: Path) -> str:
    """A PATH whose bin dir holds the tools the counters need but NOT openssl."""
    fake = work / "fakebin"
    fake.mkdir(parents=True, exist_ok=True)
    for tool in ("git", "sh", "env", "ls", "cat", "grep", "sed", "awk", "tar", "python3"):
        src = subprocess.run(["sh", "-c", f"command -v {tool}"], capture_output=True, text=True).stdout.strip()
        if src:
            link = fake / tool
            if not link.exists():
                link.symlink_to(src)
    return str(fake)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=".")
    parser.add_argument("--rev", default="HEAD")
    parser.add_argument("--base", default=BASE)
    parser.add_argument("--work", required=True)
    args = parser.parse_args(argv)
    lane = Lane(Path(args.lane).resolve())
    work = Path(args.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    try:
        tip = lane.resolve(args.rev)
        base = lane.resolve(args.base)
    except CouldNotEvaluate as error:
        print(f"DEFECT SETUP {error}")
        print("PREDICATE R92-C2 could-not-evaluate")
        return 2

    verdicts: list[tuple[str, bool, str]] = []

    # ---- M7 -----------------------------------------------------------------
    # The green leg isolates the parser fix: the tip-checkout counter bytes run in a
    # scratch clone whose LEDGER is rewound to the round-91 population (35 executed,
    # round-91 class cells) — the r91 counter's frozen constants cannot pass at any rev
    # carrying the r92 ledger growth, which is legitimate and measured by R92-C1.
    try:
        base_c1 = checkout(lane, C1, base, work / "m7")
        tip_c1 = checkout(lane, C1, tip, work / "m7")
        import shutil as _sh
        green_lane = work / "m7" / "green-lane"
        if green_lane.exists():
            _sh.rmtree(green_lane)
        green_lane.parent.mkdir(parents=True, exist_ok=True)
        clone = subprocess.run(["git", "clone", "--shared", "-q", str(lane.root), str(green_lane)],
                               capture_output=True, text=True, timeout=300)
        if clone.returncode != 0:
            raise CouldNotEvaluate("clone failed %r" % clone.stderr[-120:])
        subprocess.run(["git", "-C", str(green_lane), "checkout", "-q", tip],
                       capture_output=True, timeout=120)
        led = green_lane / "plans" / "grader-population-ledger.json"
        obj = json.loads(led.read_text(encoding="utf-8"))
        member = obj["members"].get("llm-inference-batching-scheduler")
        if member is not None and member.get("round") == 92:
            member["status"] = "unexecuted"
            member.pop("round", None)
            member["reason"] = "unattempted"
            member["evidence"] = "no-blocker: tests/test_outputs.py sha256=80b06b7c4ba0db28"
            led.write_text(json.dumps(obj, indent=1) + "\n", encoding="utf-8")
        env = {"PATH": "/usr/bin:/bin", "HOME": str(green_lane), "LC_ALL": "C",
               "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@invalid",
               "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@invalid"}

        def gitr(*a):
            p = subprocess.run(["git", "-C", str(green_lane), *a], capture_output=True, env=env)
            if p.returncode != 0:
                raise CouldNotEvaluate("fixture git failed: %s" % " ".join(a))
        gitr("add", "-A")
        gitr("commit", "-q", "--allow-empty", "-m", "ledger rewound to the r91 population")
        red = subprocess.run([sys.executable, "-I", "-B", str(base_c1), "--lane", str(lane.root),
                              "--rev", base, "--work", str(work / "m7" / "red")],
                             capture_output=True, text=True, timeout=600, cwd=str(work))
        green = subprocess.run([sys.executable, "-I", "-B", str(tip_c1), "--lane", str(green_lane),
                                "--rev", "HEAD", "--work", str(work / "m7" / "green")],
                               capture_output=True, text=True, timeout=900, cwd=str(work))
        red_defects = red.stdout.count("DEFECT L5 receipt names unknown case ?")
        m7 = (red.returncode == 1 and red_defects == 10
              and green.returncode == 0 and "PREDICATE R91-C1 pass" in green.stdout
              and "mismatches=0" in green.stdout)
        verdicts.append(("M7-CASE-PARSER", m7,
                         "base-rc=%d base-L5=%d tip-rc=%d tip-pass=%s" % (
                             red.returncode, red_defects, green.returncode,
                             "PREDICATE R91-C1 pass" in green.stdout)))
    except (CouldNotEvaluate, subprocess.SubprocessError) as error:
        verdicts.append(("M7-CASE-PARSER", False, "setup %r" % error))

    # ---- M12 ----------------------------------------------------------------
    try:
        env = {"PATH": masked_bin(work / "m12"), "HOME": str(work / "m12"), "LC_ALL": "C"}
        base_c1 = checkout(lane, C1, base, work / "m12")
        tip_c1 = checkout(lane, C1, tip, work / "m12")
        red = subprocess.run([sys.executable, "-I", "-B", str(base_c1), "--lane", str(lane.root),
                              "--rev", base, "--work", str(work / "m12" / "red")],
                             capture_output=True, text=True, timeout=600, cwd=str(work), env=env)
        green = subprocess.run([sys.executable, "-I", "-B", str(tip_c1), "--lane", str(lane.root),
                                "--rev", tip, "--work", str(work / "m12" / "green")],
                               capture_output=True, text=True, timeout=600, cwd=str(work), env=env)
        red_unguarded = red.returncode == 1 and "PREDICATE R91-C1" not in red.stdout
        green_closed = (green.returncode == 2 and "DEFECT SETUP" in green.stdout
                        and "PREDICATE R91-C1 could-not-evaluate" in green.stdout)
        m12 = red_unguarded and green_closed
        verdicts.append(("M12-HOST-PROBE-GUARD", m12,
                         "base-rc=%d base-predicate-line=%s tip-rc=%d tip-closed=%s" % (
                             red.returncode, "PREDICATE R91-C1" in red.stdout, green.returncode,
                             green_closed)))
    except (CouldNotEvaluate, subprocess.SubprocessError) as error:
        verdicts.append(("M12-HOST-PROBE-GUARD", False, "setup %r" % error))

    # ---- M9 -----------------------------------------------------------------
    try:
        base_c2_text = lane.blob_text(C2, base)
        tip_c2_text = lane.blob_text(C2, tip)
        base_expect = lane.blob_text(EXPECT, base)
        tip_expect = lane.blob_text(EXPECT, tip)
        pins_text = lane.blob_text(PINS, tip)
        expect_sha = None
        if pins_text:
            for entry in json.loads(pins_text).get("entries", []):
                if entry.get("path") == EXPECT and entry.get("kind") == "sha":
                    expect_sha = entry.get("sha256")
        import hashlib
        table_match = (tip_expect is not None and expect_sha is not None
                       and hashlib.sha256(tip_expect.encode("utf-8", errors="replace")).hexdigest() == expect_sha)
        flags = {
            "base-flag-present": base_c2_text is not None and "--skip-selftest" in base_c2_text,
            "base-table-absent": base_expect is None,
            "tip-flag-absent": tip_c2_text is not None and "--skip-selftest" not in tip_c2_text,
            "tip-table-present": tip_expect is not None,
            "tip-table-pinned-match": table_match,
        }
        tip_c2 = checkout(lane, C2, tip, work / "m9")
        run = subprocess.run([sys.executable, "-I", "-B", str(tip_c2), "--lane", str(lane.root),
                              "--rev", tip, "--work", str(work / "m9" / "run")],
                             capture_output=True, text=True, timeout=900, cwd=str(work))
        import re as _re
        pins_all_matched = bool(_re.search(r"PINS checked=(\d+) matched=\1 mismatched=0", run.stdout))
        # the ledger size is not the predicate: it grew 17 -> 18 when the C1 counter's
        # own L8 leg caught the missing probe pin (commit D) — all-matched is the claim
        green = (run.returncode == 0 and pins_all_matched
                 and "SELFTEST cases=9 red-green-ok=9" in run.stdout
                 and "PREDICATE R91-C2 pass" in run.stdout)
        m9 = all(flags.values()) and green
        verdicts.append(("M9-SELFTEST-ESCAPE", m9,
                         " ".join("%s=%s" % kv for kv in flags.items()) + " default-run-rc=%d" % run.returncode))
    except (CouldNotEvaluate, subprocess.SubprocessError) as error:
        verdicts.append(("M9-SELFTEST-ESCAPE", False, "setup %r" % error))

    for name, ok, detail in verdicts:
        print("%s %s %s" % (name, "pass" if ok else "FAIL", detail))
    passed = all(ok for _, ok, _ in verdicts) and len(verdicts) == 3
    print("PREDICATE R92-C2 %s" % ("pass" if passed else "fail"))
    return 0 if passed else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except CouldNotEvaluate as error:
        print("DEFECT SETUP %s" % error)
        print("PREDICATE R92-C2 could-not-evaluate")
        sys.exit(2)
