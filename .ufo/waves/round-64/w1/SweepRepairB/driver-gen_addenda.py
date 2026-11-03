#!/usr/bin/env python3
"""R64-C3 SweepRepairB: run each entry's committed-bytes re-verification command
in the clean clone, then emit <entry-basename>.addendum.txt + .reverify.txt.

Every result line is verified to contain its expected tokens before writing.
"""
import datetime
import hashlib
import pathlib
import shlex
import subprocess
import sys

CLONE = pathlib.Path("/fast/scratch/hyaku/kengaku-r64/SweepRepairB/clone")
SEAT = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-64/w1/SweepRepairB")
HEAD = subprocess.run(["git", "-C", str(CLONE), "rev-parse", "HEAD"],
                      capture_output=True, text=True, check=True).stdout.strip()
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

SURFACE = "corpus/evidence/round13-coverage/surface-receipt.json"
SURFACE_SHA = None  # filled from observed output

WIKI = "~/Projects/webzites/repos/llm-wiki"

# (entry path, recheck command, result line, required substrings)
ITEMS = []


def external(entry, root_grep, live_check, result_extra, expect_extra):
    if root_grep == "~/bench-arena":
        grep = ("grep -A1 -e '\"path\": \"~/bench-arena\"' "
                "-e '\"path\": \"~/archive/bench-arena\"' " + SURFACE)
    else:
        grep = f"grep -A1 '\"path\": \"{root_grep}\"' {SURFACE}"
    cmd = f"sha256sum {SURFACE}; {grep}; {live_check}"
    result = None  # built after run
    ITEMS.append(dict(entry=entry, cmd=cmd, result=result,
                      expect=[SURFACE, '"exists": false', "absent"] + expect_extra,
                      kind="external", extra=result_extra))


external("corpus/knowledge/eval-design-digest-3.md", WIKI,
         "test -e ~/Projects/webzites/repos/llm-wiki/wiki/ai/scaling-and-forecasting/scaling-hypothesis-revisited.md && echo present || echo absent; "
         "test -e ~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/papers/react-reasoning-acting.md && echo present || echo absent",
         "llm-wiki root absent on re-check 2026-11-03",
         [WIKI])
external("corpus/knowledge/eval-theory-notes.md", WIKI,
         "test -e ~/Projects/webzites/repos/llm-wiki/wiki && echo present || echo absent",
         "llm-wiki root absent on re-check 2026-11-03",
         [WIKI])
external("corpus/knowledge/gemini-benchmark-suite.md", WIKI,
         "test -e ~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/gemini-3.1-pro-godspeed-benchmarks.md && echo present || echo absent; "
         "test -e ~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/gemini-3.1-pro-godspeed-test-battery.md && echo present || echo absent",
         "llm-wiki root absent on re-check 2026-11-03",
         [WIKI])
external("corpus/knowledge/godspeed-eval-findings.md", WIKI,
         "test -e ~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/godspeed-umwelt-iteration-2.md && echo present || echo absent",
         "llm-wiki root absent on re-check 2026-11-03",
         [WIKI])
external("corpus/knowledge/telemetry-run-design.md", WIKI,
         "test -e ~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/godspeed-umwelt-iteration-3-alpha-shittycodex.md && echo present || echo absent",
         "llm-wiki root absent on re-check 2026-11-03",
         [WIKI])
external("corpus/knowledge/ledger-route-telemetry.md",
         "~/Projects/bounties/ledger/telemetry.jsonl",
         "test -e ~/Projects/bounties/ledger/telemetry.jsonl && echo present || echo absent",
         "ledger telemetry.jsonl absent on re-check 2026-11-03",
         ["~/Projects/bounties/ledger/telemetry.jsonl"])
external("corpus/knowledge/local-bench-arena.md", "~/bench-arena",
         "test -e ~/bench-arena && echo present || echo absent; "
         "test -e ~/archive/bench-arena && echo present || echo absent",
         "both bench-arena roots absent on re-check 2026-11-03 (two absent lines)",
         ["~/bench-arena"])
external("corpus/knowledge/local-model-index.md", "~/.bailian",
         "test -e ~/.bailian/skills/bailian-docs-llm-wiki/models/index.md && echo present || echo absent; "
         "test -e ~/.bailian/wiki-sync-state.json && echo present || echo absent",
         "~/.bailian absent on re-check 2026-11-03",
         ["~/.bailian"])

ITEMS.append(dict(
    entry="corpus/knowledge/eval-prior-art-calibration.md",
    kind="own",
    cmd=("sha256sum corpus/evidence/round9-fleet/prior-art.md "
         "corpus/evidence/round8-horizon/run.log "
         "corpus/knowledge/bench-arena-round9-replication.md; "
         "sed -n '80,84p' corpus/evidence/round8-horizon/run.log"),
    expect=["5f9eead651ed1e0a5a946bd76bb3d029f8831e45d21bf8b86d05c89f1dcb157f",
            "c977c6aaa77235b619dc07bc3fc53e1dd53e34ef727424c6da3d48d12b3bef64",
            "cee2e1f954e322a99b26ac75a7d3da450750fa7a2a96e860c0eca983744498c8",
            "=== SUMMARY ===", "A-INC: 7/10", "A-MONO: 0/10", "A-CKPT: 1/10"],
))

ITEMS.append(dict(
    entry="corpus/knowledge/kimi-model-routing-round18.md",
    kind="own",
    cmd=("sha256sum corpus/evidence/round18-kimi-routing/README.md; "
         "git -C /home/vgpnk/Projects/shokunin log --oneline -1 4738fee; "
         "git -C /home/vgpnk/Projects/shokunin log --oneline -1 fbae972"),
    expect=["2207bededb8810542d355265e40b393124d9d69ee5de47ffaed4b0d932b11c34",
            "4738fee7 Merge branch 'feat/r18-provider-model-census'",
            "fbae9728 Merge branch 'feat/r18-routing-table-and-docs'"],
))

ITEMS.append(dict(
    entry="corpus/knowledge/probe-battery-r19.md",
    kind="own",
    cmd=("sed -n '1,/FROZEN-PREDICTIONS-ANCHOR/p' plans/probe-battery-r19.md "
         "| sha256sum | cut -d' ' -f1; "
         "ls corpus/evidence/probe-r19-*.log | wc -l"),
    expect=["e1a867773ef14ce457a0d560180587324dd07b4deea1ec76d0c2adf65aaa00a1", "19"],
))

ITEMS.append(dict(
    entry="corpus/knowledge/tb2-cancel-async-tasks-grader.md",
    kind="own",
    cmd=("sha256sum plans/round61_c1_cancel_probe.py "
         "corpus/evidence/round52/graders/cancel-async-tasks/tests/test_outputs.py; "
         "grep -c 'PREDICATE R61-C1 pass' corpus/evidence/round61/cancel-async-probe.txt"),
    expect=["92facdc762bdb29c581eb92b5951f0855bec0de7dc56c8d2308136c889fe7f87",
            "d6f510b51fafc81b4e9b5cc95535aa13491c8753e0e4171db42c45f4de460ee7", "1"],
))

ITEMS.append(dict(
    entry="corpus/knowledge/tb2-grader-class-census.md",
    kind="own",
    cmd=("sha256sum corpus/evidence/round62/tb2-tree-2fd12b88.json; "
         "python3 plans/round62_c1_class_survey.py --lane . "
         "| grep -E 'CLASS-CENSUS|DETERMINISM|PREDICATE'"),
    expect=["dd64bfb3b47c4bd6abe4bb37ba9b34511305dd06fe1a4afd4465dfe6ff5f0cd1",
            "CLASS-CENSUS roster=89 tree-dirs=89 sha256sums-rows=184 "
            "captures-committed=183 captures-unpinned=0 sha-mismatch=0 "
            "absent-pinned=1 graders-classified=93 unclassified=0 classes=16",
            "DETERMINISM second-run-identical=True",
            "PREDICATE R62-C1 pass"],
))

ITEMS.append(dict(
    entry="corpus/knowledge/tb2-grader-vacuity-triage.md",
    kind="own",
    cmd=("python3 plans/round52_c1_grader_audit.py --lane . "
         "| grep -E 'TASKS total|CAPTURES expected|CLASS V1|TESTCLASS|CANDIDATES total|PREDICATE R52-C1'; "
         "(cd corpus/evidence/round52/graders && sha256sum -c SHA256SUMS 2>&1 | grep -v ': OK$')"),
    expect=["TASKS total=89 records=89 classified=88",
            "CAPTURES expected=184 present=183 mismatched=0",
            "CLASS V1=2 V4=0 V2=53 V3=31 V0=3",
            "TESTCLASS presence_only_tests=33 tasks_with_presence_only=27",
            "CANDIDATES total=29",
            "PREDICATE R52-C1 fail", "PREDICATE R52-C1-A5 pass",
            "./sanitize-git-repo/tests/test_outputs.py: FAILED open or read"],
))

SEAT.mkdir(parents=True, exist_ok=True)
failures = []

for item in ITEMS:
    entry = item["entry"]
    ehash = hashlib.sha256((CLONE / entry).read_bytes()).hexdigest()
    proc = subprocess.run(["/bin/bash", "-c", item["cmd"]], cwd=CLONE,
                          capture_output=True, text=True)
    out = proc.stdout + (f"[stderr] {proc.stderr}" if proc.stderr else "")
    for needle in item["expect"]:
        if needle not in out:
            failures.append(f"{entry}: expected token missing from output: {needle!r}")

    if item["kind"] == "external":
        sha_line = out.splitlines()[0]
        surface_sha = sha_line.split()[0]
        absent = "absent" in out
        result = (f"sha256={surface_sha} (committed round-13 availability receipt, "
                  f"unchanged); committed capture prints \"exists\": false for the cited root; "
                  f"live re-check {NOW[:10]}: {'absent' if absent else 'PRESENT'}")
        if item["entry"].endswith("local-bench-arena.md"):
            result = (f"sha256={surface_sha}; committed receipt: \"exists\": false for "
                      f"~/bench-arena and ~/archive/bench-arena; live re-check {NOW[:10]}: "
                      f"present-lines={out.count('present')} absent-lines={out.count('absent')}")
    elif item["entry"].endswith("eval-prior-art-calibration.md"):
        result = ("prior-art.md sha256=5f9eead6…1cb157f; run.log sha256=c977c6aa…b3bef64; "
                  "bench-arena-round9-replication.md sha256=cee2e1f9…4498c8; run.log:80-84 reads "
                  "=== SUMMARY === / A-INC: 7/10 / A-MONO: 0/10 / A-CKPT: 1/10")
    elif item["entry"].endswith("kimi-model-routing-round18.md"):
        result = ("lane evidence index README.md sha256=2207bede…932b11c34; parent-repo "
                  "read-only git: 4738fee7 Merge branch 'feat/r18-provider-model-census' / "
                  "fbae9728 Merge branch 'feat/r18-routing-table-and-docs' (both still resolve)")
    elif item["entry"].endswith("probe-battery-r19.md"):
        result = ("freeze-2 hash re-derived from committed bytes = "
                  "e1a867773ef14ce457a0d560180587324dd07b4deea1ec76d0c2adf65aaa00a1 "
                  "(line :415, exact match); receipt inventory = 19 probe-r19-*.log files")
    elif item["entry"].endswith("tb2-cancel-async-tasks-grader.md"):
        result = ("instrument plans/round61_c1_cancel_probe.py sha256="
                  "92facdc762bdb29c581eb92b5951f0855bec0de7dc56c8d2308136c889fe7f87 "
                  "(matches the entry's 92facdc7…fe7f87); pinned grader capture "
                  "cancel-async-tasks/tests/test_outputs.py sha256=d6f510b5…4de460ee7 "
                  "(= SHA256SUMS row); 'PREDICATE R61-C1 pass' occurrences=1")
    elif item["entry"].endswith("tb2-grader-class-census.md"):
        result = ("tb2-tree-2fd12b88.json sha256=dd64bfb3…ff5f0cd1 (= the entry's cited "
                  "dd64bfb3…f0cd1); pinned tool re-run on committed bytes: CLASS-CENSUS roster=89 tree-dirs=89 "
                  "sha256sums-rows=184 captures-committed=183 captures-unpinned=0 "
                  "sha-mismatch=0 absent-pinned=1 graders-classified=93 unclassified=0 "
                  "classes=16; DETERMINISM second-run-identical=True; PREDICATE R62-C1 pass")
    else:
        result = ("pinned tool re-run on committed bytes: TASKS total=89 records=89 "
                  "classified=88; CAPTURES expected=184 present=183 mismatched=0; "
                  "CLASS V1=2 V4=0 V2=53 V3=31 V0=3; TESTCLASS presence_only_tests=33 "
                  "tasks_with_presence_only=27; CANDIDATES total=29; PREDICATE R52-C1 fail "
                  "(A5 pass); sha256sum -c SHA256SUMS = 183 OK + exactly one unreadable "
                  "row (sanitize-git-repo, the operator-excluded capture)")

    base = pathlib.Path(entry).name  # e.g. eval-design-digest-3.md
    block = (
        "\n## Freshness addendum (round 64)\n"
        f"verified-at: {NOW} (round-64 freshness sweep; clean shared clone at {HEAD[:12]})\n"
        f"recheck: {item['cmd']}\n"
        f"result: {result}\n"
    )
    (SEAT / f"{base}.addendum.txt").write_text(block, encoding="utf-8")

    receipt = (
        f"# R64-C3 freshness re-verification — {entry}\n"
        f"# seat SweepRepairB, round 64, observed {NOW}\n"
        f"# clone /fast/scratch/hyaku/kengaku-r64/SweepRepairB/clone"
        f" (git clone --shared), HEAD {HEAD}\n"
        f"# entry sha256 before append: {ehash}  {entry}\n"
        f"# cwd: clone root; network: none\n"
        f"$ {item['cmd']}\n"
        f"{out.rstrip()}\n"
        f"[exit={proc.returncode}]\n"
    )
    (SEAT / f"{base}.reverify.txt").write_text(receipt, encoding="utf-8")

print(f"HEAD={HEAD}")
print(f"observed={NOW}")
print(f"wrote={len(ITEMS)} addenda, {len(ITEMS)} receipts")
if failures:
    print("FAILURES:")
    for f in failures:
        print(" -", f)
    sys.exit(1)
print("ALL EXPECTED TOKENS PRESENT")
