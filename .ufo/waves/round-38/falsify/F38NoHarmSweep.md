# F38NoHarmSweep — no-harm sweep at the landed tip `8c7422d7` (kengaku round 38, wave 2 falsify)

Seat: executor (leaf), measure-only. No lane file was edited; nothing was committed; the lane's Git index and
jj state were not touched. Every number below was produced by a command run with `cwd` = a clean clone of the
assigned tip. Receipts: `.ufo/waves/round-38/falsify/F38NoHarmSweep/receipts/` (+ `receipts-baseline/`).

## 0. Setup, and what "compare" means here

- Scratch `S=/fast/scratch/hyaku/kengaku-r38/F38NoHarmSweep`, `export TMPDIR="$S"`; scratch deleted before
  this report was finalised (receipts copied out first).
- Tip clone: `git clone -q --no-local <lane> "$S/lane"` + `git checkout -q 8c7422d7a646515d80af44844e8ecc8a1fc1d30a`;
  verified `rev-parse --show-toplevel` = `$S/lane`, `rev-parse HEAD` = `8c7422d7…` (`git status --porcelain
  --untracked-files=all | wc -l` = `0` before and after every run; after all runs still `0`, only ignored
  `__pycache__/` entries under `--ignored`).
- **Baseline clone**: second clone at the freeze parent `21e6251bfebf87ecf09f7b0a6df98b5c6179d0e9`, same
  command set, so "new red" is a measured rc/last-line comparison, not a guess from prose. (Registry rows that
  postdate the freeze — `build-pmars-probe`, `round38-c1-mutants`, `round38-c2`, `mutant-direction-check`,
  `tip-receipts` — have no baseline and are reported separately.)
- Host: `python3 -V` → `Python 3.14.8`; `nproc` → `32`; `ls -l /usr/bin/bwrap` → present (service-class probes
  runnable). No tool was installed or upgraded; pacman was not touched; no host service restarted.
- Runner: `driver.py` + `jobsA.json` / `jobsB.json` (tip) and `jobsA-baseline-fast.json` /
  `jobsB-baseline.json` (freeze parent), 5–6 way parallel; per-command log, `receipts/no-harm-matrix.tsv`.

## 1. Result

**All 31 entries that were green at the freeze parent are green at `8c7422d7`: 0 new red.** That covers
**18/18 registry rows that existed at `21e6251b`** (as 31 command entries, including every `--selftest` and
both batteries) plus every command in `integrate/measure-before.txt` and `integrate/measure.sh`.
The one entry red at the freeze parent (`ledger-tip`, routed D4) is now **green** at the tip. Seven entries
did not exist at the freeze parent: four are green, three are red — and all three reds are the frozen,
already-filed state (`round38-c1-mutants` N21 survivor; `mutant-direction-check` N21 mislabel), or are
by-design-or-documented below (O-1). Every delta against the baseline is **additive**: new round-38 files
raising a count, never a lost pass.

The wave-1 delta against `measure-before.txt` (pre-landing, TIP `2c5f4e0b`) is the intended one and is
reproduced exactly: C1 `killed=0 survived=22` → `killed=21 survived=1`; C2 `checks=7 defects=4` →
`checks=7 defects=0`; `round37-c1` `55/55` unchanged; `round37-c2` `defects=0` unchanged;
anchor `rows=107 tokens=15` → `rows=109 tokens=17`; `registry_rows=107 knowledge_files=44 index_rows=44` →
`109/45/45`.

## 2. Per-entry table (baseline = clone of `21e6251b`, tip = `8c7422d7`)

Baseline-green set — 31/31 still green, rc identical on all 31:

| # | registry row / ticket item | command (abridged) | base rc | tip rc | baseline key line → tip key line |
|---|---|---|---|---|---|
| 01 | hermetic-grader | `python3 grader.py` | 0 | 0 | `VERDICT: PASS — stored evidence fully re-derives offline` (identical) |
| 02 | hermetic-grader | `grader.py --selftest` | 0 | 0 | `[selftest] ALL PASS` |
| 03 | coverage-census | `corpus/evidence/round13-coverage/coverage_census.py` | 0 | 0 | knowledge `files/indexed 44` → `45`; evidence `31` → `32`; lessons `50` → `51`; `dangling=[]`, `duplicate_rows=[]` both |
| 04 | interval-reverdict | `plans/attrib_calibration.py --summary` | 0 | 0 | `files=9 … scored_trials=92 correct=92 incorrect=0 … ` (byte-identical) |
| 05 | interval-reverdict | `attrib_calibration.py --selftest` | 0 | 0 | `selftest: 18 checks, 0 failed` |
| 06 | state-assertion-check | `plans/state_check.py --summary` | 0 | 0 | `assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5` both; `VERDICT: PASS` |
| 07 | state-assertion-check | `state_check.py --selftest` | 0 | 0 | `[selftest] ALL PASS (…)` |
| 08 | grader-perturb | `plans/grader_perturb.py --summary` | 0 | 0 | `population=1964 excluded=0 audited_verdicts=15168 policy_checks=909` |
| 09 | grader-perturb | `grader_perturb.py --selftest` | 0 | 0 | `families=10 branch_cases=10 failed=0` |
| 10 | gate-timing | `--lesson corpus/lessons/round-26.md --commit HEAD` | 0 | 0 | `admissions=1 passed=1 failed=0 second-seat-reports=53` |
| 11 | gate-timing | same, `--commit b571944` | 0 | 0 | identical summary |
| 12 | gate-timing | `gate_timing_check.py --selftest` | 0 | 0 | `[selftest] ALL PASS (five allowed roles; …)`; inner commit hashes differ (O-4) |
| 13 | benchmark-spec-audit | `plans/benchmark_spec_audit.py --summary` | 0 | 0 | `task_count=812 distinct_task_ids=812 … findings=0 exit=0` |
| 14 | benchmark-spec-audit | `--selftest` | 0 | 0 | `SELFTEST clean cases=67` |
| 15 | registry-reference-check | `plans/registry_check.py --summary` | 0 | 0 | `source_rows_checked=13 knowledge_files_expected=35 … finding_count=0` |
| 16 | registry-reference-check | `--selftest` | 0 | 0 | `SELFTEST clean cases=15` |
| 17 | config-projection | `plans/config_projection.py --summary` | 0 | 0 | `TOTAL findings=0 exit=0` |
| 18 | config-projection | `--selftest` | 0 | 0 | `SELFTEST clean cases=31` |
| 19 | config-projection (witness) | `plans/fixtures/r29/mutation_witness.py` | 0 | 0 | JSON report, byte-identical |
| 20 | sources-adopt | `plans/sources_adopt.py` (bare) | 2 | 2 | `error: --registry and --package are required unless --selftest` (documented usage) |
| 21 | sources-adopt | `--selftest` | 0 | 0 | `SELFTEST cases=17 failed=0` |
| 22 | round36-c1-battery | `plans/round36_c1_verify.py --lane .` | 0 | 0 | `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0`; `rows=4 closed=4 observed_pass=4 mismatches=0`; `PREDICATE C1 pass` |
| 23 | regex-log-probe self-test | `plans/round36_c2_verify.py --lane .` | 0 | 0 | `W1…W6 ok`, `checks=6 defects=0`, `PREDICATE C2 pass` |
| 24 | anchor-digest-check | `plans/anchor_digest_check.py --lane .` | 0 | 0 | `rows=107 tokens=15 defects=0` → `rows=109 tokens=17 defects=0` |
| 25 | census (ticket) | `scripts/sources-census.sh validate --file corpus/SOURCES.md` | 0 | 0 | same 15 `W04` duplicate-url warnings + `ok <clone>/corpus/SOURCES.md` |
| 27 | freeze identity | `sha256sum plans/{pkg_gate.py,pkg-spec-r35.json,round37_c1_verify.py,round37_c2_verify.py,anchor_digest_check.py}` | 0 | 0 | `pkg_gate.py ea638822…` and both counters unchanged; `anchor_digest_check.py` `6d7afcd5…` → `98847e89…` (O-5) |
| 28 | regex-log-probe | `plans/regex_log_probe.py --lane .` + `cmp` vs receipt | 0 | 0 | `cases=24 observed_pass=8 observed_fail=16 mismatches=0`, `CMP byte-equal`, receipt `439101fa…` both |
| 29 | package-gate | `pkg_gate.py package --root . --spec plans/pkg-spec-r35.json --rerun --require-clean-tree` | 0 | 0 | `P1 ok pinned=3 … P10 ok probe_rerun=byte-equal bytes=3399`, `defects=0`; only `P8 index_rows 44→45` |
| 31 | git-webserver-probe | `plans/git_webserver_probe.py --lane . --work …` | 0 | 0 | `cases=22 observed_pass=9 observed_fail=13 mismatches=0` (52.8 s tip); fresh bytes `cmp`-equal to the receipt, sha256 `83550712…` (control 44) |
| 32 | round37-c1-mutants | `plans/round37_c1_verify.py --lane . --work …` | 0 | 0 | `GATE plans/pkg_gate.py sha256=frozen`; `BATTERY fixtures=64 wrong=0 renamed_disagree=0`; `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0`; `PREDICATE C1 pass` |
| 33 | round37-c2 | `plans/round37_c2_verify.py --lane . --work …` | 0 | 0 | `V1…V7 ok`, `checks=7 defects=0`, `PREDICATE C2 pass`; only `V1 gate: P8 index_rows 44→45` |

Baseline-red entry, now green (round-37 routed D4):

| # | entry | base rc | tip rc | evidence |
|---|---|---|---|---|
| 34 | ledger-tip | **1** — `rows=9 closed=9 observed_pass=7 mismatches=2`, both `agree=NO … 'git ls-tree … refs/heads/master' returned non-zero exit status 128` | **0** — `rows=9 closed=9 observed_pass=9 mismatches=0`, plus `REF BIND ref=refs/heads/master rev=8c7422d7… source_ref=10d2e977… why=clone-lacks-ref` | `receipts-baseline/34-ledger-tip.log`, `receipts/40-ledger-tip-fresh.log` |

Entries with no freeze-parent baseline (7 — four green, three red; each red is the filed state):

| # | entry | rc | key line | status |
|---|---|---|---|---|
| 26 | ticket: frozen digests | 0 | 8 × `OK` (`plans/pkg_gate.py` … `round37_c2_verify.py`) | green |
| 35 | round38-c1-mutants | **1** | `PINS total=14 mismatched=0`; `BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0`; `MUTANT N21 D5 silence SURVIVED`; `MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0`; `PREDICATE C1 fail` | frozen honest stop — reproduced, not relabelled (O-2) |
| 36 | round38-c2 | 0 | `V1 ok listed=5`; `gate: P2 ok receipt_sha256=pinned`; `V2 ok spec=frozen gate=frozen gate_exit=0`; `V4 ok cases=22 mismatches_named=0/0`; `V7 ok rows=7 tags=7 bad=0`; `checks=7 defects=0`; `PREDICATE C2 pass` | green |
| 37 | mutant-direction-check | **1** | `DIR N21 D5 declared=silence observed=mirror MISLABELLED`, all 21 others `ok`, `DIRECTIONS total=22 mislabelled=1` | documented red (row `SKILL.md:585`) |
| 38 | build-pmars-probe | 0 | `cases=22 observed_pass=7 observed_fail=15 mismatches=0`; fresh stdout `cmp`-equal to `corpus/evidence/round38/build-pmars-probe.txt`, both sha256 `2408b477…` (control 41) | green |
| 39 | tip-receipts | 0 | `compared=4 declared_bounded=1 no_command=19`, `control … verdict=differ`, `receipts=24 byte_equal=4 differ=0 skipped=20` | green |
| 30 | package-gate on `pkg-spec-r38.json` | **1** | `P2 DEFECT receipt_sha256=2408b477b0299e13…`, `P10 ok probe_rerun=byte-equal bytes=5537`, `defects=1` | O-1 below (by design per the counter; read as a reject by the row's verdict map) |

Delta lines reproduced verbatim from `measure-final.txt` at the tip (all match, so the landing receipt is
still current at `8c7422d7`): `rows=109 tokens=17 defects=0`; `rows=9 closed=9 observed_pass=9 mismatches=0`;
`receipts=24 byte_equal=4 differ=0 skipped=20`; `registry_rows=109 knowledge_files=45 index_rows=45`.

## 3. Observations (freshness / operability — no action taken, no lane file touched)

**O-1 (operability) — `plans/pkg-spec-r38.json` ships `receipt_sha256: null`, so the round-38 package is
red at P2 for anyone running the documented gate entry instead of the counter.**
`python3 plans/pkg_gate.py package --root . --spec plans/pkg-spec-r38.json --rerun --require-clean-tree` →
`P2 DEFECT receipt_sha256=2408b477b0299e1339064b4b3df968a00174b3a5999016073b5fe4fd8cbb4ef9`, `P10 ok
probe_rerun=byte-equal bytes=5537`, `defects=1`, rc 1 (`receipts/30-pkg-gate-r38-rerun.log`). Cause:
`git show e0a3785:d… plans/pkg-spec-r38.json | …["receipt_sha256"]` → `None` at the freeze, at `d93b7d6` and at
`8c7422d7`; `plans/round38_c2_verify.py:16-18` states the counter "fills `receipt_sha256` with the digest of the
receipt it finds, so P2 is a presence check". Authenticity is not affected — I reproduced the receipt
independently: fresh `build_pmars_probe.py` stdout is `cmp` byte-equal and sha256 `2408b477…` on both sides
(`receipts/41-buildpmars-cmp.log`). The mismatch is between the spec as shipped and the `package-gate` row's
map, where `1` reads "reject (a hardened check fails)". The row itself names `pkg-spec-r35.json`, so no
baseline-green entry regressed; the gap is that "the gate accepts the round-38 package" cannot be reproduced
with the spec file committed at the tip.

**O-2 (freshness) — the `round38-c1-mutants` row's `0` clause is unreachable at the tip and the row does not
say so.** `SKILL.md:583` maps `0` to `killed=22 survived=0 … PREDICATE C1 pass`; the measured tip state is
`killed=21 survived=1`, rc 1 (`receipts/35-round38-c1.log`). The red *is* declared elsewhere —
`corpus/lessons/round-38.md:70` ("killed=21 survived=1`, `PREDICATE C1 fail` (N21 the survivor) — the round
reports C1 as an honest stop") and `integrate/measure-final.txt:114-115` — and the sibling row
`mutant-direction-check` (`SKILL.md:585`) does name its own red. Only the registry row is silent, so the
round-37 precedent (the addendum that recorded `anchor-digest-check` as "a red state, not a green one") is
not applied to this row.

**O-3 (operability, carried forward from round-37 N2) — an absent `--work` path still exits 1, not 2.**
Seven of nine slow entries failed with `FileNotFoundError … k37-c1-… / k37-c2-… / k37-cgw-… / k38-c1-… /
k38-c2-… / k38-dir-… / k38-bpm-…` when `--work` did not exist (`receipts/summaryB-nowork.tsv`), and
`ledger_tip.py` refuses a reused work dir with `REFUSE will not reuse … remove it first`, rc 2. With the
directory pre-created every entry ran its declared predicate. Unchanged behaviour, not a regression.

**O-4 (freshness) — `gate_timing_check.py --selftest` is not byte-stable across commits.** Its inner cases name
commits reachable from `HEAD`; the same two cases print `d3ee19d6…/26e180a9…` at `21e6251b` and
`b1c6a1ff…/7a47acc7…` at `8c7422d7`, with identical verdicts (`passed=0 failed=1`, `passed=1 failed=0`) and
`[selftest] ALL PASS` both times. Any future receipt that byte-compares this selftest would age with history.

**O-5 (freshness) — the landed `anchor_digest_check.py` has no pin at its new digest.** `sha256sum` →
`98847e8930304a23ab3e10dd27cfc3501738467b8871d8b725d24908e6c1f0b2` at the tip vs
`6d7afcd56a95c59f835be04a16263d43db4840cc8a4b111350be4d7cb8d9a323` at the freeze parent (D3 per-row
binding). `grep -rn '6d7afcd5\|98847e89'` over the lane returns only round-37 `build/`+`falsify/` prose, so the
round-37 draft digest is now stale prose and the shipped file's digest is named nowhere. The row claims no
self-test and no in-code constants, so nothing fails; the check's red direction is still reachable (below).

## 4. Red-direction controls (does anything still bite?)

| control | command | observed |
|---|---|---|
| anchor check sees a wrong digest | scratch copy, one hex digit of the S115 anchor token flipped (`d9d2796d…` → `09d2796d…`), committed in the copy's own repo | `DEFECT S115 anchor token=09d2796d… class=digest-unknown detail=not-committed-evidence-and-not-in-a-SHA256SUMS loc=corpus/SOURCES.md:130`, `rows=109 tokens=17 defects=1`, rc 1; pristine copy first gave `defects=0`, rc 0 (`receipts/43-anchor-red-control.log`) |
| probe refuses a moved receipt | `build_pmars_probe.py` fresh stdout vs committed receipt | `CMP receipt byte-equal`, sha256 `2408b477…` both (`receipts/41-buildpmars-cmp.log`) |
| git-webserver receipt reproduced | `git_webserver_probe.py --lane .` fresh stdout vs receipt | `CMP byte-equal`, sha256 `83550712…` both (`receipts/44-gitws-cmp.log`) |
| ledger-tip still fails a broken clone | (round-37 controls, not re-run here) | — ; the tip's `REF BIND … why=clone-lacks-ref` line is the mechanism that removed the false red |

## 5. No-harm invariants

1. **Tree unchanged:** `git -C $S/lane status --porcelain --untracked-files=all | wc -l` = `0` before the
   sweep and `0` after all 39 entries plus 4 controls; `--ignored` lists only `__pycache__/*.pyc` created by
   the runs. The anchored red control ran in a copy under `$S`, never in the clone or the lane.
2. **Lane untouched:** no `git add/commit/stash/checkout/reset/push/pull` and no jj command in the lane; no
   lane file edited; the only writes are under this seat's `falsify/` dir and `$S` (deleted).
3. **Wave-1 wrote no lane implementation file:** `git diff --stat d93b7d6 8c7422d -- . ':!.ufo'` →
   `LOG.md`, `SCORECARD.md`, `corpus/lessons/round-38.md` only (3 files, 153 insertions). `git diff --stat
   8c7422d 10d2e97 -- . ':!.ufo'` → empty, i.e. the falsify spec and the post-hoc N21 diagnostic are `.ufo`-only,
   so master's extra commits cannot alter any measured predicate.
4. **All reads are of committed bytes:** `P9 ok untracked=0` and `V1 gate: P9 ok untracked=0` held at a clean
   tree; `sha256sum -c .ufo/waves/round-38/claims/frozen-digests.txt` → 8 × `OK`.
5. **Source repo** `/home/vgpnk/Projects/shokuknow` was never read or written; no campaign tool ran.

## 6. Evidence inventory (under `falsify/F38NoHarmSweep/`)

- `receipts/` — 39 entry logs + controls `40-ledger-tip-fresh.log`, `41-buildpmars-cmp.log`,
  `43-anchor-red-control.log`, `44-gitws-cmp.log`, `42-census-line.log`; `buildpmars-fresh.txt`,
  `gitws-fresh.txt`, `regexprobe-fresh.txt`; `no-harm-matrix.tsv`, `SHA256SUMS`.
- `receipts-baseline/` — the same command set at `21e6251b` (28 fast + 4 slow logs, `regexprobe-fresh.txt`).
- `driver.py`, `jobsA.json`, `jobsB.json`, `jobsA-baseline.json`, `jobsA-baseline-fast.json`,
  `jobsB-baseline.json` — the exact argv sets, replayable verbatim.

VERDICT: no-harm-31/31-new-red-0
