author: hyaku closure (non-author integrator, @m_zfl)

# Kengaku round 93 — non-author verifier spot-check

Reviewed lane tip: `7b8719f3eefb3f560add5dd3367b67b7a50a45da` (BASE `28e9f8bf4e8a68b1a34babfa71be9de595b78c4e`; P1 `17cb9337`; P2 `0e77e98f`; freeze F `d8d0a4b8`; measured tip T = C `22972a317185216596b3dfe1c189e98d1eb86787`). Report: `.ufo/reports/round-93/kengaku.md` (fleet commit `c1b084df3abd69700803182e53438b6436469979`, author `kengaku-shokunin <kengaku@shokunin.local>`, 2026-11-05 18:41:53 -0300). Driver digest (`.ufo/watchdog.log`, copied 2026-11-05): `2026-11-05T17:42:10-03:00 launch kengaku round=93 pgid=1634505 driver=hyaku-inline attempt=1`; `2026-11-05T18:42:36-03:00 complete kengaku round=93; hyaku-inline attempt=1`.

Method. Plain measurements over committed bytes (`git show`, `git log`, `git merge-base --is-ancestor`, `sha256sum`, `jq`, census CLI) plus live re-fetches of four upstream files. Lane counters, the freeze-integrity gate and its battery were **not executed** by this integrator (PROTOCOL §Gate standard, "Closure consequence"); their committed receipts under `.ufo/waves/round-93/` were read and graded evidence-verified.

## 1. Step-1 conformance

| check | command (observed) | result |
|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-93/kengaku.md` → `kengaku-shokunin c1b084df…` | pass |
| `SHONEN` heading, one line per box | report `## SHONEN` with 4 `[~]` lines; `grep -c '^- \[' SHONEN.md` → 4 | pass |
| cited commits exist and are ancestors of `master` | `git merge-base --is-ancestor <h> master` for 28e9f8bf, 17cb9337, 0e77e98f, d8d0a4b8, 22972a31, fb79ef74, 5cc54ef5, 7b8719f3 → all `anc` | pass |
| lane pushed, clean | `jj-lane.sh state` → `local=remote=7b8719f3… ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` → empty; `ls-remote origin refs/heads/master` → `7b8719f3…` | pass |
| report filed after its commits | lane tip committed 18:40:22, report 18:41:53, completion line 18:42:36 | pass |
| prompt carries template contract | `.ufo/prompts/kengaku-round-93.md` (fleet `135bb880`, 892 lines): §1 MISSION/AXES, §2 claims + admission, §2b frontier, §3 L2 floor, §4 report contract (SHONEN), §5 commit scope, §6 hyaku addendum, §7 scratch | pass |
| marker? | real report, 7 lane commits with checkable work | not a marker → status `ok` |

Conformance defects (status-neutral, routed in §6): (a) the new `freeze-integrity gate` has **no registry row** at the lane's registry home (`SKILL.md` gate table at `SKILL.md:594`; `grep -n freeze.integrity SKILL.md` → none) — per §Gate standard "Delivery" it is not graded conformant until that row exists; (b) the capability row sits in the round-93 SCORECARD section ("enters the table only if the closure admits C2"), not yet in `## Capabilities` (`SCORECARD.md:553`); (c) the report and SCORECARD quote `SELFTEST cases=10 ok=10` for W3, but `c2-tip.txt` carries only `W3 pass` (the counter consumes the line, `round93_c2_counter.py:157-159`, without echoing it) — the tally is evidence-verified through the frozen counter, not a quoted line; (d) dead seat ReviewerC1 and ScoutSources without `report.md` (disclosed).

## 2. Claims — re-derivation

### R93-C1 — coverage (eleventh offline replay, `schemelike-metacircular-eval`)

| item | command | observed | reported | match |
|---|---|---|---|---|
| ledger executed | `git show <rev>:plans/grader-population-ledger.json \| jq '[.members[]\|select(.status=="executed")]\|length'` | BASE 36 of 88 → tip 37 of 88 | 36 → 37 | yes |
| class cells (executed/total) | jq group-by over `.members[].classes[]` | timing-wall 3/9→4/9; subprocess-exec 13/45→14/45; stdout-inspection 11/29→12/29; file-artifact 27/76→28/76 | same | yes |
| ledger diff BASE→tip | `git diff 28e9f8bf 7b8719f3 -- plans/grader-population-ledger.json` | exactly one member flipped `unexecuted`→`executed`, `round: 93`, receipt pointer added | one-member flip | yes |
| receipt | `cat corpus/evidence/round93/scheme-probe.txt` | 8 CASE lines all `ok=True`, `mismatches 0`; `TOOL_SHA 6fad5d52…`, `CASE_TABLE_SHA 078b04d2…` equal the frozen table; `LANE_TIP d8d0a4b8` (F) | 8/8, mismatches 0 | yes |
| capture bytes | `sha256sum tests/test_outputs.py tests/interp.py` in the capture; test programs `find tests/test -name '*.scm' \| wc -l` | `fbb84e3c…be7ed` = receipt SUBJECT_SHA; `efb8b5cd…ea2c1` = INTERP_SHA; 32 in test/ (+31 shadow = 63) | same | yes |
| counter verdict at T | committed `.ufo/waves/round-93/L1/c1-tip.txt` | `LEGS L1..L9=pass`, `TARGET executed_rows=37 … cases=8 legs=40 mismatches=0 defects=0`, `PREDICATE R93-C1 pass`, `rc=0` | same | evidence-verified |
| controls | `controls/c1-base.txt`, `c1-forgery-ledger-only.txt`, `c1-sandbox-red.txt` | fail rc 1; fail rc 1; could-not-evaluate rc 2 | same | evidence-verified |

Verdict: **verifies** (re-measured: ledger, cells, receipt, capture hashes, upstream bytes; evidence-verified: counter legs/rc and controls).

### R93-C2 — calibration + capability `freeze-integrity gate`

| item | command | observed | reported | match |
|---|---|---|---|---|
| frozen table holds at F, T and tip | for each row of the ` ```frozen-instruments ` block: `git show <rev>:<path> \| sha256sum` at d8d0a4b8, 22972a31, 7b8719f3 | 9/9 `ok` at all three revisions | W4 summary=(9, 9, 0) | yes |
| no tabled instrument touched after F (incl. edit-then-revert) | `git log d8d0a4b8..7b8719f3 -- <9 instruments> plans/round-93-claims.md` | empty; `git diff --stat d8d0a4b8 7b8719f3 -- plans` → only the ledger | touched=0 ×9 | yes |
| nor between P1 and F (controls ran frozen bytes) | `git log 17cb9337..d8d0a4b8 -- <instruments>` | empty | — | yes |
| W1 on round-92 history (F `f0018773` → tip `1df76536`) | `git log --format=%h f0018773..1df76536 -- <p> \| wc -l` + byte compare | round92_c1_replay.py 0/same; round92_c2_conformance.py 4/diff; round92_burndown.py 3/diff; round91_counter_pin.py 1/diff → intact 1, broken 3 | `summary=(4, 1, 3)`, intact=[round92_c1_replay.py] | yes |
| counter verdict at T and at final tip | committed `L1/c2-tip.txt`, `L1/c2-final-tip.txt` | W1 pass, W2 5/5 fixtures ok, W3 pass, W4 pass (9,9,0), `TARGET legs_passed=4 of 4`, `PREDICATE R93-C2 pass`, `rc=0` (both) | same | evidence-verified |
| controls | `controls/c2-base.txt`; four `c2-forgery-*.txt`; `c2-real-at-P1.txt` | fail rc 1 ×5; positive W1–W3 pass, W4 `claims-absent` (expected) | same | evidence-verified |
| self-test tally | gate prints `SELFTEST cases={len(bat)} ok={bat_ok}` (`round93_freeze_integrity.py:260`); counter W3 requires `^SELFTEST cases=10 ok=10$` twice | W3 pass ⇒ 10/10 at T | 10/10 | evidence-verified (see §1 c) |

Wave scope limits (W-1 three seat-built forgeries pass the counter 4/4; W-4 mutants m06/m13 survive, 18/25 killed; W-2 TREESAME merge false-intact; W-3 second table block ignored) bound the counter's forgery discrimination and the gate's generality, but none flips T: F..T and the W1 window contain no merges, the claims file has one table block, and the gate's numbers were independently re-derived above by plain git. Verdict: **verifies**, capability scoped as the lane states (linear history, one table block).

### Harm check

`git diff 28e9f8bf 7b8719f3 -- SCORECARD.md` → append-only round-93 section (+44 lines, 0 deletions); novelty 8, depth 10, operability 10, freshness 10, adjacency 9 held; coverage held at L0 cap 7; calibration held at ceiling 10. Whole-round diff: 322 files, +23024/−3 (the −3 are the ledger member's three old fields). Spot reads: `corpus/QUALITY.md:1385-1386` (Q73 grounded in round-92 M8, Q74 in round-93 M1), lesson `corpus/lessons/round-93.md` (Gate, M1–M4, W-1…W-9). No owned axis harmed.

## 3. Per-axis verdicts (this closure)

| axis | verdict | basis |
|---|---|---|
| coverage | improved | ledger executed 36→37 of 88, timing-wall 3→4 of 9 (re-measured); score held at L0 cap 7 |
| calibration | improved | freeze-integrity gate counts the lane's past self-assessment mismatches (r92: broken=3, re-derived) and this round's (0); score held at ceiling 10 |
| novelty | unchanged | no claim; score 8 held |
| depth | unchanged | no claim; score 10 held |
| operability | unchanged | no claim; score 10 held |
| freshness | unchanged | no claim; score 10 held |
| adjacency | unchanged | no claim; score 9 held |

## 4. Discernment spot-check (LEARNING.md — from outside)

Re-fetched 2026-11-05 from `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/…` with `curl -w '%{http_code}'`.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S290 `schemelike-metacircular-eval/tests/test_outputs.py` | admit (A) | HTTP 200, 6823 B, sha256 `fbb84e3c…be7ed`; `:121` = `def test_interp():`, `:220` = `    assert failed == 0` | agree | bytes identical to capture and receipt SUBJECT_SHA; the quote and its line hold; it is the single graded function |
| S292 `solution/solve.sh` | admit (A) | HTTP 200, 11910 B, sha256 `e2c5b0ac…712510`; `:4` = `cat <<'EOF' > eval.scm` | agree | identical to capture `solution/solve.sh`; corrected digest tail (W-7) now right |
| S294 `tests/test.sh` | reject | HTTP 200, 608 B, sha256 `4770437e…c334`; `:3` `# Install curl`, `:5` `apt-get install -y curl`, `:8` `curl -LsSf https://astral.sh/uv/0.9.5/install.sh \| sh`, `:18` `uvx` | agree | network installs are incompatible with an offline replay; no grader semantics beyond S290 |
| S296 `large-scale-text-editing/tests/test_outputs.py` | reject | HTTP 200, 8935 B, sha256 `f5e69f4f…cd43`; `:170` quote holds; `vim` invoked in `test_apply_macros_runs` (`:170`) and `test_macros_nonempty_and_efficient` (`:202`) = 2 of 5 `def test_` | agree | `command -v vim vi` → none on this host (`/usr/bin/nvim` exists, but the grader execs literal `vim`); with pacman paused the member is not replayable |

SOURCES row re-opened: S290 (`corpus/SOURCES.md:306`) — quote “def test_interp():” is 2 words (≤25), located at the stated line in the live bytes; S296 (`:312`) quote is 10 words, located at `:170`. Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → `kengaku ok`, exit 0 (30 pre-existing W04 duplicate-url warnings, none on S290–S296); rows 281 at BASE → 288 at tip (`grep -c '^| \?S[0-9]\+ '`).

Result: 2 admits + 2 rejects sampled, 4/4 agree.

## 5. Trend verdicts (this closure)

- **expansion: improved** — population frontier 36→37 of 88 with a class-cell move (timing-wall 3→4/9), 4 admitted tier-A rows (S290–S293) on a member the corpus did not hold, and the freeze-integrity capability admitted with this closure.
- **quality: unchanged** — no admitted `knowledge/` entry was superseded or re-verified this round; the in-round corrections (W-7) fixed rows written this same round. The new gate strengthens verification machinery, but the LEARNING quality observable did not move.
- **discernment: improved** — outside spot-check agrees on admits and rejects (4/4); Q74 is a new criterion grounded in lesson M1, and Q73 in round-92 M8; the lane's own past self-assessment mismatches are now counted by a command whose numbers this closure re-derived.

## 6. Routed defects the lane must fix next round (round 94)

1. Add the `freeze-integrity gate` registry row at `SKILL.md` (name, gate, entry command, verdict map incl. rc 2, self-test spelling = in-process battery, pinned-value path, write scope, owner) — §Gate standard "Registry"/"Delivery".
2. Move the admitted capability row into `SCORECARD.md` `## Capabilities`.
3. W-1/W-4/M4: committed controls for the three seat-built forgeries and mutants m06/m13 (two-commit window with `--rev` below HEAD, post-freeze table rewrite, rc-2 leg) under a new frozen predicate.
4. W-2: `git rev-list --full-history` (TREESAME-merge false intact); W-3: reject or read a second `frozen-instruments` block; W-6: duplicate rows / freeze selector / W3 comment.
5. W-5: C1 L7 checks aggregates only — compare the member set, not counts.
6. Have the counter echo the `SELFTEST` line into its receipt so the W3 tally is quotable.
7. Carried from round 92: #2 override vacuity `plans/round92_burndown.py:306-329`, #3 marker skip `:445`/`:558`, #4 round-92 counters unpinned, #6 `cost_model_for_tests.py` guard.

Operator note: the four SHONEN boxes carry committed evidence pointers a non-author can check (SKILL tables, LOG end-to-end entry with receipt, re-run counting commands, PROVINCE/ConnectorOverlap); promotion is operator-owned.
