# F42CritScorecard — calibration count, round-42 wave 2 (falsify)

Seat: F42CritScorecard (critic, leaf). Target: every claim in `SCORECARD.md` §Round 42,
`LOG.md` §Round 42 and `SHONEN.md`, checked against repo state at `508434ad55c709337065611691c426f05875492d`
(clone in `/fast/scratch/hyaku/kengaku-r42/F42CritScorecard/lane`). Method: resolve each pointer; re-run each
cheap command; quote outputs. Full landing measurement `integrate/measure-final.txt` (clean clone of
`ff14d76d`) and baseline `integrate/measure-baseline.txt` (at `fda71ae0`) were read whole and diffed.

## 1. Claim-by-claim verification

### 1.1 Commit/recipe pointers (SCORECARD §Round42 opening, LOG opening)
| Claim | Evidence |
|---|---|
| baseline as read `d69452cf…`; freeze `bc856d80…`; first recorded probe run `523b2780…`; wave-1 dispatch `fda71ae0…`; landing `ff14d76d…` | `git cat-file -t` → all five are commits; `ORDER receipt_commit=523b2780…`, `ORDER freeze=bc856d80…` in `measure-final.txt`; `TIP fda71ae0…` baseline / `TIP ff14d76d…` final. `git log ff14d76d..508434ad` → exactly one commit (docs). `git diff --stat ff14d76d 508434ad -- plans/` → empty (plans untouched post-landing). |
| frozen prereg `plans/round-42-claims.md` | exists; `sha256sum -c .ufo/waves/round-42/claims/frozen-digests.txt` at 508434ad → all `OK` (rc 0), incl. both counters, probe, witnesses; same digest block passes in baseline and final. |
| lesson `corpus/lessons/round-42.md`; QUALITY Q33/Q34; PROVINCE round-42 paragraph | all present; Q33 (`QUALITY.md:692`) and Q34 (`:761`) carry the round-42 text; PROVINCE paragraph at `:552-575` states “8 of 89 read” and the unowned digital-logic/C-simulator semantics routing. |
| axis state carried: calibration 8, coverage 7 (capped by L0 `kengaku \| round-33`), novelty 7, depth 9, operability 8, freshness 8, adjacency 8; coverage chosen (frozen tie-break) | `plans/round-42-claims.md:15-17` states exactly this, including “Coverage is chosen … tie-break as in rounds 35–41”. |

### 1.2 C1 (calibration)
| Claim | Evidence |
|---|---|
| “before”: `BATTERY fixtures=0`, `MUTANTS total=14 killed=0 survived=14`, `anchor=0/9 order=0/5`, `PREDICATE C1 fail`, exit 1 | `.ufo/waves/round-42/claims/control-c1-nothing.txt` (envelope, exit=1) and `measure-baseline.txt` identical to the sentence. |
| 14 directional round-40 near-variants, anchor 9 / order 5; 13 `direct`, 1 `indirect` | baseline+final `ADVERTISED direct=13 indirect=1 none=0`; `MUTANTS-BY-TOOL anchor=9/9 order=5/5` final. |
| XO5/XO6 relabelled `rc-mirror` | final lines: `MUTANT XO5 order rc-mirror killed=…`, `MUTANT XO6 order rc-mirror killed=…`. |
| “after”: `BATTERY fixtures=29 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=14 killed=14 survived=0 invalid=0 null_detected=0 unattributed=0`, `PINS total=2 mismatched=0`, `PREDICATE C1 pass`, exit 0 | `measure-final.txt` (29 FIXTURE rows: a_class 6, a_route 6, a_row 6, o_clause 5, o_scan 6). |
| kills counted only when attributed; span-forced control `control-c1-attribution.txt` → `killed=0 unattributed=14`, fail | control file exact; attribution lines carry `attributed=L318 hits=2 …` etc.; `MUTANTS … unattributed=14` + `PREDICATE C1 fail`, exit=1. |
| battery42 carries no `config/gpg/signature/worktree` key | `grep -in 'config\|gpg\|signature\|worktree' plans/battery42/*.py` → no match (exit 1); 5 modules present (`a_class.py a_route.py a_row.py o_clause.py o_scan.py`). |
| direction-mislabel control fails | `control-c1-direction-mislabel.txt`: XO5/XO6 `SURVIVED exhibits=0>1,rc-mirror`, `killed=12 survived=2`, `PREDICATE C1 fail`, exit=1. |
| “five wave-1 executors wrote battery42 (29 fixtures)” | fixture count 29 verified; executor count is a wave-1 provenance claim, no in-tree per-author artifact at this commit. |

### 1.3 C2 (coverage)
| Claim | Evidence |
|---|---|
| “before”: `checks=9 defects=6` (V2 V3 V4 V7 V8 V9), exit 1 | `control-c2-nothing.txt` exact (`checks=9 defects=6`, V2/V3/V4/V7/V8/V9 DEFECT, exit=1). |
| at `fda71ae0` `defects=5`, V8 ok once receipt landed | `measure-baseline.txt` exact (`defects=5`, `V8 ok order_exit=0 result=PASS`). |
| “after”: `checks=9 defects=0`, `PREDICATE C2 pass`, exit 0 | `measure-final.txt` exact (V1–V10 all ok; P10 `probe_rerun=byte-equal bytes=4212`). |
| pinned TB2 `circuit-fibsqrt` @ `2fd12b88`; S125 (tier A) `tests/test_outputs.py`, S126 (A) `instruction.md`, S127 (A) `tests/sim.c`, S128 (B) OpenAgents #9645 | `SOURCES.md:140-143` rows S125–S128, tiers A,A,A,B; entry `corpus/knowledge/tb2-circuit-fibsqrt-grader.md:1-3` pins `2fd12b88`; capture digests in receipt match row sha256s (test_outputs.py `6117b8ed…`, instruction.md `a7f50026…`, sim.c `700645ac…`). |
| probe `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, `regrade cases=16 differ=0` | `corpus/evidence/round42/fibsqrt-probe.txt` tail exact; byte-equal re-run: `measure-final.txt` `fibsqrt_probe exit=0 byte_equal=yes`. |
| observations: 1195-line lookup passes 3/3 printing 0 for examples 208/20000; 31999 pass / 32000 fail size only; comments, reversed order, CRLF pass; trailing space fails; planted `/app/sim` overwritten; verifier cwd `/app`; `gates.txt` directory passes existence only | all match the receipt cases (`lookup-28`, `lookup-28-padded-31999/-32000`, `lookup-28-comment-lines`, `-reversed-lines`, `-crlf`, `-trailing-space`, `fake-sim-script`, `gates-is-directory`) and `PROVINCE.md:552-555`/README index row `:75`. |

### 1.4 No-harm / envelope claims
- `diff` of signature lines (TIP, PREDICATE, BATTERY, MUTANTS, anchor rows, receipts=, routed_open=, ROWS, registry_rows/knowledge_files/index_rows, ORDER RESULT, exits, SENTINEL, untracked) between baseline and final shows ONLY: TIP, C1 red→green, C2 red→green, anchor `rows=117 tokens=24` → `rows=121 tokens=27`, `routed_open=5` → `10` (ROWS 10→16), `registry_rows=117 knowledge_files=48 index_rows=48` → `121/49/49`. `tip_receipts.py` doc cell for fibsqrt changes (`plans/fibsqrt_probe.py:4+plans/round-42-claims.md:77` → `SKILL.md:600+SKILL.md:600`) — a registry-row consequence. `receipts=28 byte_equal=8 differ=0 skipped=20` both. `order_check` round 38 FAIL exit=1 (`ORDER HIT … gate-p10 … probe-executed-before-receipt`), rounds 39–42 PASS exit=0. `round_close.py --round 41/42` exit 0 both; census exit 0, 15 W04 both; frozen-digests rounds 39–42 OK both.
- Envelope v1 note: `measure-baseline-v1.txt` exists; P10 fails with `stderr='error: Could not acquire lock … Could not create temporary file'` (uv cache) under read-only home; header shows v2 overlays `~/.cache` from scratch (`--bind …L1/home-cache /home/vgpnk/.cache`).

### 1.5 Capability rows (SCORECARD)
| Claim | Evidence |
|---|---|
| `attributed-mutant-kills`: counter → `unattributed=0`, pass; control → `killed=0 unattributed=14`, fail | 1.2 above. |
| `compiled-simulator-grader-probe`: probe → `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, byte-equal re-run; pytest parity 16/16 | receipt + byte-equal verified; **pytest parity 16/16 is a wave-1 observation (`R42CritPytest`) whose report file is not in the tree at 508434ad — not independently re-runnable here** (would require rebuilding the terminal-bench sandbox probe). |
| `scratch-root-guard`: `--selftest` → `SELFTEST ok=36/36`; `check /fast/scratch/hyaku/kengaku-r42` → `SENTINEL … round=42` | **live re-run this seat (receipt in §3)**: 36/36 ok, rc 0; `CHECK ok round=42 want=* seats=40`, rc 0. |

### 1.6 Frontier/routed/assimilation (SCORECARD + LOG)
- Registry rows `round42-c1-mutants`, `round42-c2`, `fibsqrt-probe` + addendum present (`SKILL.md:599-601,675`); §Simulator-executed data-artefact TB2 grader — round 42 at `SKILL.md:1160`.
- README index row (`:75`), coverage bullet (`:271`), §Frontier “8 of 89” (`:374`).
- `corpus/routed-findings.jsonl`: 16 lines total (was 10), 9 open, `routed_open=10 oldest_round=39` (matches `routed_open.py` output; min `opened_round` among open rows = 39).
- `merge/kengaku/` unchanged since 2026-10-24: `git log --since='2026-10-24' --all -- merge/kengaku/` → empty.
- `round_close.py --selftest` re-run fix: `integrate/r5-round-close-check.txt` shows `CHECK PASS rc=0 twice, identical output, no nested copy` (`run1_rc=0 run2_rc=0`, `SELFTEST checks=5 ok=5 failed=0` twice).

### 1.7 SHONEN.md pointers
- SKILL.md contains real decision tables: `SKILL.md:23,53,844,900,954,1023,1103,1182`.
- end-to-end task logged at `LOG.md:7` = round-4 “executed first authored eval (closes SHONEN "end-to-end task" checkbox)”.
- `corpus/lessons/round-8-aggregator-box3-coldrun.md:48` exists (Box-3 verdict); `PROVINCE.md:129` exists (### Adjacent).

## 2. Mismatches

**M1 (minor, overstatement).** SCORECARD §Round42 “Envelope note: under the v1 envelope (home read-only)
every C2-class counter went red on `uv`'s cache lock” — `measure-baseline-v1.txt` shows six C2 counters red on the
uv lock **but `round36_c2_verify.py` passes** (`PREDICATE C2 pass`, `checks=6 defects=0`; that gate predates the
uv-using P10/P2 machinery).
Corrected: “under the v1 envelope (home read-only) every C2-class counter that invokes `uv` went red on `uv`'s cache lock”.
Location of claim: `SCORECARD.md` §Round42, Envelope note sentence (line ~1765). Evidence: `measure-baseline-v1.txt`
lines: `PREDICATE C2 fail` at 51/161/239/386/522/669 (rounds 42/41/40/39/38/37), `PREDICATE C2 pass` at 679 (round 36).

**Non-counted notes (pointer resolution).**
1. Wave-1 report `.md` files named in the wave framing (`R42CritC1Counter`, `R42CritAttribution`,
   `R42SentinelCounter`, `R42RevMutRows`, `R42MutC1Counter`, `R42CritPytest`, `R42ScoutPriorArt` …) are **not
   present at 508434ad** — `.ufo/waves/round-42/build/` holds only `swarm-registry.json` at this commit; the report
   files arrive with 445e81f (after this wave was cut). The round-42 docs reference those findings narratively; I
   verified everything locally checkable, but the wave-1 findings themselves (pytest parity 16/16, vacuous spans
   8/14, three substitute fixtures) are not independently re-runnable from this commit.
2. `measure-final.txt` envelope tail reports `local_bin_listing_before=763032563d3739aa after=77408cab9a10361a CHANGED`
   — the landing measurement's own `~/.local/bin` listing changed during the run. Transparently recorded in the
   receipt; not a document claim, but surfaced for the L1 per the PATH-shim rule.
3. All “after” numbers were read from the official `measure-final.txt` (clean clone of `ff14d76d`); I re-ran the
   cheap subset (scratch_guard selftest/check, counts, digests) at 508434ad with identical results.

## 3. Receipt (live runs this seat)
Envelope: `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>` (TMPDIR=$S inside).
- `BEFORE 18:05:54`; `ls -A /home/vgpnk/.local/bin | sha256sum` → `8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52`.
- `python3 …/plans/scratch_guard.py --selftest` → `SELFTEST ok=36/36`, rc 0; `python3 …/plans/scratch_guard.py check /fast/scratch/hyaku/kengaku-r42` → `SENTINEL .ROUND-ROOT-SENTINEL round=42 … CHECK ok round=42 want=* seats=40`, rc 0.
- `AFTER 18:05:54`; sha256sum → `8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52` (unchanged).

VERDICT: scorecard-mismatches-1
