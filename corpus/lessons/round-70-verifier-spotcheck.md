# kengaku round 70 — outside spot-check (non-author)

author: hyaku closure (non-author integrator, @m_zfl)
Date: 2026-11-03. Lane: `kengaku-shokunin`, branch `master`. Base `502893ad`; after
`cf32a9c4b247a6e041d8574e8c0e89a30fe8fe4c`.

## 1. Step-1 conformance

- **Report attribution.** `git log --format='%an %H' -- .ufo/reports/round-70/kengaku.md`
  → `kengaku-shokunin <kengaku@shokunin.local> c8d1aad8a39121bb7a816247d351143851293100`
  ("round-70: kengaku report", 139 lines). Landed by the lane identity, after the lane
  commit. ✓
- **`SHONEN` heading.** `grep -c '^## SHONEN'` → 1; the section carries four `[~]` lines,
  matching the four boxes in `SHONEN.md` (`grep -cE '^- \[[ x~]\]'` → 4). ✓
- **Cited commits.** `git cat-file -e` and `git merge-base --is-ancestor <full> master` →
  ancestor for all five: base `502893ad`, freeze `384e9c76`, A2 `0ef40526`, landing
  `3fc7bd75`, receipts `cf32a9c4`. ✓
- **Lane clean and pushed.** `jj-lane.sh state` → `branch=master local=cf32a9c4
  remote=cf32a9c4 ahead=0 behind=0 head=detached tracked=0 untracked=0`;
  `git status --porcelain` → empty. ✓
- **Prompt fidelity.** `diff <(sed -n '1,140p' templates/round-prompt.md)
  <(sed -n '1,140p' .ufo/prompts/kengaku-round-70.md)` → 42 lines, every one a `{{…}}`
  substitution (lane, round, fleet root, report path); sections 1–5 therefore carry the
  round-level contract (mission/axes, L2 floor, commit-then-push, push scope, L0) and the
  five child-lane items (report path, commit-before-report ordering, `SHONEN` heading,
  hash-citation rule, lane write scope) verbatim. Addendum §6–§9 carries the run-15
  directives. The quoted route map (reviewer `@m_zfl`, every other role `@m_flash`) matches
  `~/.omp/agent/config.yml` `task.agentModelOverrides` (reviewer `@m_zfl`; all other roles
  `@m_flash`) and MISSION §L2's advisory role buckets. ✓
- **Wave.** `.ufo/waves/round-70/w1-results.json`: `seats=14`, `results=14`, every result
  carries non-empty output; roles executor 4 / reviewer 3 / mutation-tester 2 / scribe 2 /
  critic 1 / scout 1 / connector 1 = 14; attack roles {reviewer, critic, mutation-tester}
  = 6/14 (43 %); connector 1; L2 floor ≥8 met inside the one v1 wave; run-15 band 8–16.
- **Dispatch/complete digest** (`.ufo/watchdog.log` is mutable; copied here):
  `2026-11-03T21:33:01-03:00 launch kengaku round=70 pgid=2304126 driver=hyaku-inline attempt=1`
  `2026-11-03T22:04:33-03:00 complete kengaku round=70; hyaku-inline attempt=1`
- **Conformance notes (status-neutral).** (a) The fleet-repo prompt commit `82f9985d` is
  authored by the lane identity although PROTOCOL gives prompt-commit duty to the
  integrator; the prompt is durable and only attribution is affected. (b) The
  `Mistakes`-row count drifts across lane files — see routed defect R70-D1.

## 2. Claim re-checks

Both claims were re-derived against committed bytes at `cf32a9c4`. Lane-owned gates were
**evidence-verified, never executed** (PROTOCOL §Gate standard — Closure consequence);
plain counters (`git show | grep -c`, hashes, tree probes) were run directly.

### R70-C1 — coverage (lowest non-retired axis, L0-capped at 7)

| measurement | command | base `502893ad` | tip `cf32a9c4` |
|---|---|---|---|
| receipt absent→present | `git cat-file -e 502893ad:corpus/evidence/round70/nginx/receipt.txt` | rc 128 | present |
| SKILL `executed 2 of 8` | `git show <rev>:SKILL.md \| grep -c 'executed 2 of 8'` | 1 | 0 |
| SKILL `executed 3 of 8` | `git show <rev>:SKILL.md \| grep -c 'executed 3 of 8'` | 0 | 1 |
| S242 row | `git show <rev>:corpus/SOURCES.md \| grep -cE '^\|[[:space:]]*S242[[:space:]]*\|'` | 0 | 1 |

Observed in `corpus/evidence/round70/nginx/receipt.txt` at `cf32a9c4`: seven
`VECTOR … agree=True` (`PPPPPPPP`, `PPFPPPPP`, `PPPPPPFF`, `PPPPPFPP`, `FPPPFPPP`,
`PFFFPPFF`, `PPPFPPPP`), `LEG-COVERAGE legs=8 seen_p=8 seen_f=8`,
`SUMMARY cases=7 legs=56 mismatches=0 setup=0`, `PREDICATE R70-C1 pass`.
`check.txt`: `REV 3fc7bd75…`, `CHECK ok cases=7 legs=8 seen_p=8 seen_f=8`,
`CHECK stored-predicate=pass derived=pass`, rc 0. Digest bindings recomputed:
`plans/round70_c1_nginx_probe.py` sha256 `9c9effeb004a4207…dbb43c4b` at both `3fc7bd75`
and `cf32a9c4` = the receipt's `PROBE`/`PROBE_BLOB`;
`corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py` sha256
`045cc716c14efde3…a4acda0`, 5947 B, 178 lines. `selftest.txt`: `red_refused=7/7
green_ok=1 accept_ok=1 ok=True`, plus `PATH-INDEPENDENT sha_equal=True` and
`STAGED-STATE changes_on_byte=True`. Seven per-case sandbox captures are committed under
`corpus/evidence/round70/nginx/sandbox/`. **Verdict: pass** (counters re-measured; receipt,
checker and selftest evidence-verified).

### R70-C2 — calibration (held at ceiling 10, exercised)

Before: `.ufo/waves/round-70/c2-red-before.txt` (committed; `.ufo/waves/round-70/`):
`DEFECTS n=8`, `PREDICATE R70-C2 fail`, eight enumerated defects E1–E8. After:
`corpus/evidence/round70/c2-green.txt` — `REV 3fc7bd75…`, `GATE-BLOB-SHA256 367ce58e…`,
eight `E1..E8 ok` lines (re-counted: `grep -cE '^E[1-8] ok'` → 8), `DEFECTS n=0`,
`PREDICATE R70-C2 pass`, rc 0. The gate file's sha256, recomputed from
`git show 3fc7bd75:plans/round70_c2_routed_defects.py`, is `367ce58e41799a75…c35a36fb` —
equal to the receipt binding at both `3fc7bd75` and `cf32a9c4`.
`corpus/evidence/round70/c2-controls.txt`: `defects-in-fake=8 want=8 all-fail=True`,
`e2-byte-flip-red=True`, `SELFTEST ok=True`, `MUTANTS total=8 killed=8`.
`corpus/evidence/round70/c2/a4-usedby-arm.txt`: both `used-by` clauses fire on blanked
cells.

Eight routed defects re-opened in committed bytes:

| D | correction present |
|---|---|
| D1 | `corpus/evidence/round70/c2/depth-gate-provenance.txt` labels `TREE-CAPTURE … PRE-CLASS-ROW` / `LANDING-COPY`, both sha256s, `LINE-DIFF … total=33 … -> … total=34` |
| D2 | `corpus/evidence/round70/gates/trio-nginx.txt` → `TRIO pass corpus/knowledge/tb2-nginx-request-logging-offline.md` |
| D3 | S242 row (`mined`, used-by the nginx entry); entry `source:` anchor `instruction.md:6-11,15-18`; errata `E-D3` |
| D4 | S243 row, `teaches` opens `supersedes S241 —`; S241 kept as written (append-only) |
| D5 | `corpus/README.md:564` round-69 lesson row + block at `:790` |
| D6 | `corpus/evidence/round70/gates/r69-c2-landing.txt` → `REV 4038bb11`, `E1..E7 ok`, `DEFECTS n=0`, `PREDICATE R69-C2 pass`, `RC 0` |
| D7 | lesson `## Gate` carries the S244 reject with reason and flip |
| D8 | `.ufo/waves/round-70/w1-validate.rc` = `0`, `w1-validate.out` dispatch JSON, `w1-validate.stderr` |

**Verdict: pass** (gate evidence-verified; correction presence and gate digest re-derived).

### No axis harmed

`git diff 502893ad cf32a9c4 -- SCORECARD.md` appends one Round 70 section; no earlier score
is edited (coverage 7, calibration 10, operability 10, depth 10, freshness 10, adjacency 9,
novelty 8 all held; this round's two moves are carried by evidence, not by a number).
`git diff … -- corpus/SOURCES.md` → 0 deletions, 3 additions (S242, S243, S244).
`PROVINCE.md` only corrects the stale "nginx blocked" clause; `SKILL.md` changes the
`network-service` class row and its evidence; the nginx knowledge entry gains an appended
round-70 addendum + errata. No owned axis harmed.

## 3. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| coverage | improved | class row `executed 2 of 8` → `3 of 8` on a passing frozen predicate (`LEG-COVERAGE legs=8 seen_p=8 seen_f=8`); the nginx member moves from blocked/frontier into the executed class; score held at its L0 cap 7 |
| calibration | improved | eight routed defects D1–D8 closed by a re-deriving gate `n=8` → `n=0`, killed 8/8; score held at ceiling 10, so the move is evidence-carried |
| depth | unchanged | entry addendum + S242/S243; depth gate `ROWS n=16 … paths total=34 resolved=34 share=1.00`, `PREDICATE R63-C2 pass`; score 10 held |
| operability | unchanged | two instruments run (`--check-receipt`, `--selftest`, `--mutants`); no new capability row; score 10 held |
| freshness | unchanged | S242 opened live at the pin (HTTP 200, 1882 B, sha256 `26a7ac98…9edf99`); stale PROVINCE clause corrected; score 10 held |
| adjacency | unchanged | `SiblingOverlap70` reports term-level hits only, none absorbed; PROVINCE accurate; score 9 held |
| novelty | unchanged | no new instrument-level construct claimed; score 8 held |

## 4. Discernment spot-check (LEARNING.md, non-author)

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kengaku` → exit 0, `ok …/corpus/SOURCES.md`, 25 W04 warnings;
data rows `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 236 (base 233).

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S242 — TB2 nginx task instruction at pin `2fd12b88` | admit (tier A, docs) | `curl` of the row URL this round: HTTP 200, 1882 B, 24 lines, sha256 `26a7ac98aced6107f147206790ada77bbf8ed3c25fb360cf323d5fc6889edf99`; line 16 is `"Welcome to the benchmark webserver"` | **agree** | live bytes equal the row's anchor digest and the located quote; the instruction does state the body literals and the four unchecked clauses the entry records |
| S243 — the same pinned grader, corrected leg map | admit (tier A, code) | committed capture `corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py`: sha256 `045cc716…4acda0`, 5947 B; line 61 prints `result = subprocess.run(["nginx", "-t"], capture_output=True, text=True)` | **agree** | the quote is exact at the stated line; leg 5 is a subprocess, not a file read, so the supersession of S241's summary cell is grounded |
| S244 — `merge/kengaku` entry `grader-fixture-coverage` | reject (tier C) | `/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/grader-fixture-coverage.md` (2869 B): line 1 blank, `source:` at `:2`, `recheck:` at `:4`; lane `S155` at `corpus/SOURCES.md:170` is the password-recovery `solve.sh`; `git ls-files \| grep -c 'toolathlon-grader-fixture-probe2'` → 0; wave copy 7033 B, sha256 `3b9a4902…42ee` | **agree** | the triad is offset by a leading blank line (Q1), the cited `S155` is a different source in this lane, and the probe script/receipt the transcript invokes is not held here, so the tier-A own-work claim is not re-derivable (Q2); reason and flip are recorded |

The round's `## Gate` carries three sourced decisions with ≥1 admit and ≥1 reject, so both
halves of the gate were exercised — closing the round-69 D7 zero-reject gap.

## 5. Trend verdicts

- **expansion: improved** — the `network-service` coverage-map row moves `executed 2 of 8`
  → `3 of 8` on a passing frozen predicate (frontier ground entered: the nginx member is
  now counted), and two new tier-A rows (S242, S243) are cited by the admitted knowledge
  entry (`used-by` resolves to
  `corpus/knowledge/tb2-nginx-request-logging-offline.md`); census 233 → 236.
- **quality: improved** — S243 supersedes S241's false leg-5 summary cell (append-only,
  old text kept); the nginx entry is re-verified with a round-70 addendum and errata; the
  eight routed defects close with a gate that moves `n=8` → `n=0` and is killed 8/8 under
  single-check deletion; Q52 enters with its lesson.
- **discernment: improved** — the outside spot-check re-opened the round's two admits and
  one reject and agrees on all three (LEARNING's improved condition), and the gate now
  exercises rejection taste that round 69 lacked. The lane's report graded this `unchanged`;
  the closure grades the observable, and does not claim a QUALITY criterion it lacks.

## 6. Routed defects the lane must fix next round

1. **R70-D1 — `Mistakes`-row count drift (evidence standard, correction sweep).** The
   lesson `corpus/lessons/round-70.md` carries eight `## Mistakes` data rows
   (`sed -n '/^## Mistakes/,$p' … | grep -cE '^\|'` → 10 lines = header + separator + 8
   rows). Three sites disagree: `LOG.md` Round 70 says "five rows"; `corpus/README.md:799`
   says "six Mistakes rows"; `corpus/README.md:565` says "eight Mistakes rows" but
   enumerates only six (staged-digest, self-unreadable-receipt, C2 argument order,
   exception-red, case-note isolation, freeze-doc overclaim — missing the dead-check-clause
   and unre-derived-prose rows). The lesson's last row claims the README was corrected "in
   the same commit"; the sweep did not reach `LOG.md` or `README.md:799`, and the
   enumeration at `:565` was not updated. Fix: append a `LOG.md` correction entry
   (append-only) naming the superseded "five rows" text, and correct both README mentions
   to eight with all eight names, logging old→new.
2. **R70-D2 — D3 residual citation in the entry body.** In
   `corpus/knowledge/tb2-nginx-request-logging-offline.md:15` the sentence "The instruction
   at the same pin states the same bodies, the rate-limit zone location and the log path
   (`instruction.md:6-11`)" cites `:6-11` for the bodies, but the body literals are at
   `:15-18` (re-opened live this round: line 16 index body, line 18 404 body). The
   `source:` anchor and errata `E-D3` carry the corrected `instruction.md:6-11,15-18`; the
   sentence was not swept. Fix: an erratum naming the superseded sentence with the full
   range, or the corrected citation, per the corpus append-only norm.

Neither defect changes a claim verdict: R70-C2's predicate is E1–E8, and the claim's own
gate is green on committed bytes; both are evidence-standard/conformance defects.
