from load import *
import copy
R={n:list(v[2]) for n,v in rows.items()}

# --- correction 1: round46-c3 --filler claim was false (measured checks=7 defects=6, exit 1)
c=R['`round46-c3`']
old="`checks=7 defects=0` under `--filler`, which runs V3, V4, V6, V7, V9, V10, V12)"
assert old in c[3]
c[3]=c[3].replace(old,"under `--filler` it runs V3, V4, V6, V7, V9, V10, V12 against the do-nothing control package and is expected red — measured `checks=7 defects=6` (V3 ok; V4, V6, V7, V9, V10, V12 DEFECT), `PREDICATE C3 fail`, exit 1; a green `--filler` run would mean the content legs admit a do-nothing package)")
# --- correction 2: round35-hardening stale live-lane number
c=R['`round35-hardening`']
old="on the live lane `H6 FAIL untracked_anywhere=2`, exit 1)"
assert old in c[6]
c[6]=c[6].replace(old,"on a lane carrying untracked wave files H6 fails, exit 1 — measured `H6 FAIL untracked_anywhere=2` in wave 1 and `untracked_anywhere=881` on the live lane during wave 2)")

# --- two new rows for the round-52 counters
R['`round52-c1`']=["`round52-c1`","gate",
"`python3 plans/round52_c1_grader_audit.py --lane .` (lane root; `--selftest`) — the whole-benchmark grader-vacuity triage for Terminal-Bench 2.0: classifies each of the 89 frozen tasks' primary grader and prices the confirmations",
"`0` `PREDICATE R52-C1 pass`: `CAPTURES expected=184 present=184 mismatched=0`, `TASKS total=89 records=89 classified=89`, `CONFIRMED new>=2`, `PRIOR-ART ok=True` (>=3 distinct URLs) · `1` fail on the literal frozen predicate, with every leg printed first (`TASKS`, `CAPTURES`, `CLASS V1 V4 V2 V3 V0`, `TESTCLASS`, `CANDIDATES` then one `  CANDIDATE` line each, `CONFIRMED` with a `  REJECTED <task> <reason>` line per refused receipt, `PRIOR-ART`, `LABELS agree=<a> of <t>` which is evidence and not a leg) — measured on the live lane at HEAD `87301ba` before `confirmations.json`, `prior-art.md` and `labels.json` existed: `TASKS total=89 records=89 classified=88`, `CAPTURES expected=184 present=183 mismatched=0`, `CLASS V1=2 V4=0 V2=53 V3=31 V0=3`, `TESTCLASS presence_only_tests=33 tasks_with_presence_only=27`, `CANDIDATES total=29`, `CONFIRMED new=0`, `PRIOR-ART ok=False urls=0`, `PREDICATE R52-C1 fail`, exit 1; with `sanitize-git-repo/tests/test_outputs.py` operator-excluded (Amendment A5) the literal predicate cannot pass at this tip, and the additive trailer lines `A5 EXCLUDED listed=1 digest_pinned=1`, `A5 CAPTURES present+pinned_excluded=184 of 184`, `A5 TASKS classified+excluded=89 of 89`, `PREDICATE R52-C1-A5 pass` or `fail` price that exclusion but never change the exit code, which follows the literal `PREDICATE R52-C1` line · `2` setup: `SETUP plans/round52-tasks.json missing` (measured with `--lane /nonexistent`); argparse usage also exits 2",
"`python3 plans/round52_c1_grader_audit.py --selftest` (measured `SELFTEST classify cases=4 failures=0`, `SELFTEST classify_test cases=4 failures=0`, `SELFTEST cases=6 failures=0`, exit 0; covers the file-level classes V1–V4 on four bodies, the per-test classes P1/P3/P2/P0 on four blocks, and the prior-art leg's absent-file and three-URL cases; limit: it does not exercise the capture count, the digest check, the CONFIRMED hardening (new-task, candidate and verbatim-quote checks) or the A5 trailer, which are re-derived only by the live run and by the round-52 controls `c1-control-*` under `.ufo/waves/round-52/claims/`)",
"population `plans/round52-tasks.json` (repo `harbor-framework/terminal-bench-2`, pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, `task_count` 89, `capture_file_count` 184) and the per-capture digests in `corpus/evidence/round52/graders/SHA256SUMS` (184 lines); frozen marker regexes `PRESENCE`, `CONTENT`, `BEHAVIOUR`, `VALUE`, `BEHAV_T` in code; candidate = a task with at least one P1 test or a V1/V4 file class; thresholds `CONFIRMED new>=2` and `PRIOR-ART urls>=3`; the never-read set is derived from the 12 `corpus/knowledge/tb2-*-grader.md` filenames (`git-webserver` mapped to `configure-git-webserver`); receipts read: `corpus/evidence/round52/confirmations.json`, `prior-art.md`, `labels.json`; A5 exclusion `graders/EXCLUDED.md` naming sha256 `57e4904177acac5807b51f7c32444bde1968ba0445855fa4333d9eb73865b59e` for the one absent capture",
"none — reads committed lane bytes only and writes nothing; no network, no git call, no subprocess; `--selftest` writes only a `tempfile.TemporaryDirectory` that it removes",
"kengaku round 52"]

R['`round52-c2`']=["`round52-c2`","gate",
"`python3 plans/round52_c2_registry.py --lane .` (lane root; `--selftest`) — every advertised verdict instrument has a registry row: the four legs MISSING, INCOMPLETE, ENTRY-MISSING, SELFTEST-UNBACKED",
"`0` `PREDICATE R52-C2 pass`: `MISSING 0`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 0` (measured on the live lane at HEAD `87301ba` with the 28 wave-1 rows in `SKILL.md`: `ADVERTISED total=72`, `REGISTERED total=72 rows=74`, exit 0; `rows` counts the header line and the unparsed `coverage-census` row too, so it exceeds `REGISTERED`) · `1` fail, each defect on its own line (`  MISSING <path>`, `  INCOMPLETE-ROW <name>`, `  ENTRY-MISSING <path>`, `  SELFTEST-UNBACKED <name>`) then `PREDICATE R52-C2 fail` — measured at the base tip `30801b47`: `ADVERTISED total=72`, `REGISTERED total=44 rows=46`, `MISSING 28`, `SELFTEST-UNBACKED 1` (`order-check`, the Amendment A3 false positive), exit 1 · `2` setup: `SETUP no SKILL.md under <lane>` (measured with `--lane /nonexistent`); argparse usage also exits 2 · limits read off the code and measured: a table line is kept only if splitting it on every pipe character yields exactly 8 cells, so a row carrying an escaped pipe (the pre-round-52 `gate-flip-check` row has one in its verdict cell, between `fired` and `not fired`) is dropped without a message; the entry regex needs a `python3 plans/<name>.py`, `python3 corpus/evidence/<dir>/<name>.py` or `python3 grader.py` token with `[A-Za-z0-9_]` only, so a script under a hyphenated evidence directory (`coverage_census.py` under `round13-coverage/`) is outside the advertised universe",
"`python3 plans/round52_c2_registry.py --selftest` (measured `SELFTEST ok clean-fixture`, `SELFTEST ok missing-fixture`, `SELFTEST ok incomplete-fixture`, `SELFTEST cases=3 failures=0`, exit 0: three temp trees — a clean registry passes, a dropped row raises MISSING, a blank cell raises INCOMPLETE; limit: no fixture exercises ENTRY-MISSING or SELFTEST-UNBACKED, which are exercised only by the live run and by the round-52 controls `c2-control-*` under `.ufo/waves/round-52/claims/`)",
"frozen universe in code: command regex `python3` followed by `plans/<name>.py`, `corpus/evidence/<dir>/<name>.py` or `grader.py`, depth 1 under `plans/`; scanned files `SCORECARD.md`, `SKILL.md`, `LOG.md`, `corpus/README.md` and every `corpus/knowledge/*.md`; registry block = `SKILL.md` from the heading `## Gate/probe registry` to the next `## `; eight cells per row with none empty; a self-test cell counts as unbacked only when it names exactly one script and a `--flag` that script's bytes lack, and a flag negated by `no … --flag` within 24 characters is ignored (Amendment A3); base-tip receipt `.ufo/waves/round-52/claims/c2-before.txt`",
"none — reads committed lane bytes only and writes nothing; no network, no git call, no subprocess; `--selftest` writes only a `tempfile.TemporaryDirectory` that it removes",
"kengaku round 52"]

# validate
import re
for n,r in R.items():
    assert len(r)==8, n
    assert all(x.strip() for x in r), n
    assert not any('|' in x for x in r), (n,[i for i,x in enumerate(r) if '|' in x])
def script(r):
    m=re.search(r"(?:plans|corpus)/[A-Za-z0-9_/]+\.py",r[2]); return m.group(0)
order=sorted(R.items(), key=lambda kv: script(kv[1]))
hdr=["| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |","|---|---|---|---|---|---|---|---|"]
lines=hdr+["| "+" | ".join(r)+" |" for n,r in order]
open('registry-rows.md','w').write("\n".join(lines)+"\n")
print(len(order)); print([script(r) for n,r in order])
