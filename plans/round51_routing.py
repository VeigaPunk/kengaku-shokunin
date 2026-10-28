#!/usr/bin/env python3
"""Round-51 C2 counter — every routed finding names an owner and a disposition.

Frozen predicate (plans/round-51-claims.md §C2, written before any data):

    python3 plans/round51_routing.py --lane . --run-checks
    -> exit 0 and a final line `PREDICATE R51-C2 pass`
    iff every row of corpus/routed-findings.jsonl carries the full field set,
        every `owner` names a fleet lane (or `unowned:integrator`),
        every `disposition` is one of the frozen values,
        every `source` pointer resolves in the lane,
        every `check` is a non-empty command,
        every `disposition=fixed-verified` row's check exits 0 in this run,
        every `disposition=fixed-historical` row's `close` names a commit/ref
        that resolves in the lane's git object database,
        and every `disposition=routed|referral` row names a non-kengaku owner
        plus a `next` field.

The adjacency axis is what this measures: cross-domain evidence is *named with
its owner and routed*, never silently absorbed. Before the round the ledger has
no `owner`/`disposition` field at all, so no row is attributed.

Stdlib only; honours TMPDIR and --scratch; no hardcoded /tmp.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FIELDS = ("id", "class", "source", "opened_round", "status", "owner",
          "disposition", "close", "blocker", "check", "note")
STATUSES = {"open", "closed", "refused", "blocked"}
DISPOSITIONS = {"fixed-verified", "fixed-historical", "routed", "referral",
                "accepted-risk", "refused-out-of-scope"}
FALLBACK_OWNERS = {"kengaku", "kama", "kagi", "kake", "kasegi", "kumitate",
                   "kotoba", "kaidoku", "kumitate", "souji", "tabi", "mori",
                   "chousa", "kotodama", "kumitate", "tameshi", "protocol",
                   "aggregator", "unowned:integrator"}


def load_owners(fleet: Path) -> set[str]:
    """Owner universe: the curated fallback set, the LANES rows of shokunin.conf
    (`id|repo|axes`), and every `*-shokunin` lane directory on disk."""
    owners = set(FALLBACK_OWNERS)
    conf = fleet / "shokunin.conf"
    if conf.is_file():
        for line in conf.read_text(errors="replace").split("\n"):
            m = re.match(r"\s*([a-z][a-z0-9-]{1,15})\s*\|", line)
            if m:
                owners.add(m.group(1))
    try:
        for d in fleet.glob("*-shokunin"):
            if d.is_dir():
                owners.add(d.name[: -len("-shokunin")])
    except OSError:
        pass
    return owners


def rows_of(path: Path) -> list[dict]:
    out = []
    for n, line in enumerate(path.read_text().split("\n"), 1):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as exc:
            out.append({"_parse_error": "%s line %d: %s" % (path.name, n, exc)})
    return out


def check(lane: Path, ledger: Path, run_checks: bool, scratch: Path | None) -> int:
    rows = rows_of(ledger)
    fleet = lane.parent
    owners = load_owners(fleet)
    print("LEDGER %s rows=%d" % (ledger.relative_to(lane), len(rows)))

    p: dict[str, list[str]] = {k: [] for k in (
        "FIELDS", "OWNER", "DISPOSITION", "SOURCE", "CHECK", "CHECK_FAILED",
        "CLOSE_REF", "NEXT", "PARSE")}

    tmp = scratch or Path(tempfile.mkdtemp(prefix="r51route-"))
    tmp.mkdir(parents=True, exist_ok=True)
    ran = passed = 0
    for r in rows:
        if "_parse_error" in r:
            p["PARSE"].append(r["_parse_error"])
            continue
        rid = r.get("id", "?")
        missing = [f for f in FIELDS if f not in r]
        if missing:
            p["FIELDS"].append("%s missing %s" % (rid, ",".join(missing)))
        owner = r.get("owner")
        if not owner:
            p["OWNER"].append("%s has no owner" % rid)
        elif owner not in owners:
            p["OWNER"].append("%s owner %r not a fleet lane" % (rid, owner))
        disp = r.get("disposition")
        if not disp:
            p["DISPOSITION"].append("%s has no disposition" % rid)
        elif disp not in DISPOSITIONS:
            p["DISPOSITION"].append("%s disposition %r not frozen value" % (rid, disp))
        st = r.get("status")
        if st not in STATUSES:
            p["DISPOSITION"].append("%s status %r not in %s" % (rid, st, sorted(STATUSES)))
        src = (r.get("source") or "").split(":")[0]
        if not src or not (lane / src).exists():
            p["SOURCE"].append("%s source %r does not resolve" % (rid, r.get("source")))
        cmd = r.get("check")
        if not cmd or not str(cmd).strip():
            p["CHECK"].append("%s has no check command" % rid)
        if disp in ("routed", "referral"):
            if owner == "kengaku":
                p["NEXT"].append("%s is %s but owned by kengaku (absorbed, not routed)" % (rid, disp))
            if not (r.get("next") or "").strip():
                p["NEXT"].append("%s is %s with no next field" % (rid, disp))
        if disp == "fixed-verified" and cmd and run_checks:
            ran += 1
            try:
                out = subprocess.run(["bash", "-lc", cmd], cwd=str(lane),
                                     capture_output=True, text=True, timeout=90,
                                     env={**os.environ, "TMPDIR": str(tmp),
                                          "LANE": str(lane)})
                ok = out.returncode == 0
            except subprocess.TimeoutExpired:
                ok = False
            if ok:
                passed += 1
            else:
                p["CHECK_FAILED"].append("%s fixed-verified but check exits nonzero" % rid)
        if disp == "fixed-historical":
            close = (r.get("close") or "").strip()
            tok = close.split()[0] if close else ""
            tok = tok.strip(",")
            ok = False
            if tok:
                if re.fullmatch(r"[0-9a-f]{7,40}", tok):
                    ok = subprocess.run(
                        ["git", "-C", str(lane), "cat-file", "-e", tok + "^{commit}"],
                        capture_output=True).returncode == 0
                else:
                    ok = (lane / tok).exists()
            if not ok:
                p["CLOSE_REF"].append("%s close %r does not resolve" % (rid, close[:60]))

    print("FIELDS complete=%d incomplete=%d" % (len(rows) - len(p["FIELDS"]), len(p["FIELDS"])))
    print("OWNERS attributed=%d unattributed=%d" % (len(rows) - len(p["OWNER"]), len(p["OWNER"])))
    print("DISPOSITIONS set=%d bad=%d" % (len(rows) - len(p["DISPOSITION"]), len(p["DISPOSITION"])))
    print("SOURCES resolved=%d missing=%d" % (len(rows) - len(p["SOURCE"]), len(p["SOURCE"])))
    print("CHECKS present=%d absent=%d" % (len(rows) - len(p["CHECK"]), len(p["CHECK"])))
    print("VERIFIED ran=%d passed=%d failed=%d" % (ran, passed, ran - passed))
    print("CLOSE_REFS resolved=%d missing=%d" % (
        sum(1 for r in rows if r.get("disposition") == "fixed-historical") - len(p["CLOSE_REF"]),
        len(p["CLOSE_REF"])))
    print("NEXT violations=%d" % len(p["NEXT"]))

    ok = True
    for key in ("PARSE", "FIELDS", "OWNER", "DISPOSITION", "SOURCE", "CHECK",
                "CHECK_FAILED", "CLOSE_REF", "NEXT"):
        if p[key]:
            ok = False
            for line in p[key]:
                print("  DETAIL %s %s" % (key, line))
    print("PREDICATE R51-C2 %s" % ("pass" if ok else "fail"))
    if scratch is None:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0 if ok else 1


def _selftest(tmp: Path) -> int:
    lane = tmp / "lane"
    (lane / "corpus/lessons").mkdir(parents=True, exist_ok=True)
    (lane / "corpus/lessons/x.md").write_text("e\n")
    (lane / "corpus/routed-findings.jsonl").parent.mkdir(parents=True, exist_ok=True)
    (tmp / "shokunin.conf").write_text("lanes:\n  kengaku: { cwd: x, axes: y }\n  kama: { cwd: z, axes: w }\n")

    def row(**kw):
        base = {"id": "R1", "class": "c", "source": "corpus/lessons/x.md:1",
                "opened_round": 1, "status": "closed", "owner": "kama",
                "disposition": "fixed-verified", "close": "receipt",
                "blocker": None, "check": "true", "note": None}
        base.update(kw)
        return base

    cases, fails = 0, []

    def run(rows, expect_ok, run_checks=True):
        nonlocal cases
        cases += 1
        (lane / "corpus/routed-findings.jsonl").write_text(
            "".join(json.dumps(r) + "\n" for r in rows))
        code = check(lane, lane / "corpus/routed-findings.jsonl", run_checks, tmp / "work")
        if expect_ok and code != 0:
            fails.append("case %d expected pass got %d" % (cases, code))
        if not expect_ok and code == 0:
            fails.append("case %d expected fail got pass" % cases)

    run([row()], True)
    run([{k: v for k, v in row().items() if k != "owner"}], False)
    run([row(owner="nope-lane")], False)
    run([row(disposition="whenever")], False)
    run([row(source="corpus/absent.md:3")], False)
    run([row(check="")], False)
    run([row(check="false")], False)
    run([row(owner="kengaku", disposition="routed", next=None)], False)
    run([row(owner="kama", disposition="routed", next="round 52, kama")], True)
    run([row(disposition="fixed-historical", close="corpus/absent.md")], False)
    run([row(disposition="fixed-historical", close="corpus/lessons/x.md")], True)
    print("[selftest] cases=%d failures=%d" % (cases, len(fails)))
    for f in fails:
        print("[selftest] FAIL %s" % f)
    print("[selftest] %s" % ("ALL PASS" if not fails else "FAILED"))
    return 0 if not fails else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--ledger")
    ap.add_argument("--run-checks", action="store_true")
    ap.add_argument("--scratch")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    lane = Path(args.lane).resolve()
    if args.selftest:
        tmp = Path(tempfile.mkdtemp(prefix="r51route-st-"))
        try:
            return _selftest(tmp)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    ledger = Path(args.ledger).resolve() if args.ledger else lane / "corpus/routed-findings.jsonl"
    scratch = Path(args.scratch) if args.scratch else None
    return check(lane, ledger, args.run_checks, scratch)


if __name__ == "__main__":
    sys.exit(main())
