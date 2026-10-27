# R45PlanNext — round-46 data walk (scout, wave 1): `round_close.py` survivors as a third-tool claim, TB2 coverage candidates, the F1 census draft

Seat `R45PlanNext` (leaf, read-only on the lane; nothing frozen touched). Lane clone `$S/lane` (`$S=/fast/scratch/hyaku/kengaku-r45/R45PlanNext`) at `05b02e2b7894a9c83219685f2374905e11c1beda`
(`git -C $S/lane rev-parse --show-toplevel` = `$S/lane`). Pins: `plans/round_close.py` sha256 `cd581f8a…8144`, `plans/round44_c1_verify.py` `6cf05323…e48ad` — both unchanged since round 44.
Every run went through `claims/envelope.sh "$S/env" <cmd>`; `local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged` at every boundary (7 runs, 23:28–23:32 -03).
Receipts (all < 15 KB, `SHA256SUMS.txt`) in `.ufo/waves/round-45/w1/R45PlanNext/`. `R45ScoutTB2.md` was delivered while I worked; I walked the task list independently first and cross-checked.

## Headline for the L1

1. **Calibration (third tool = `round_close.py`): re-measured today, identical to R44PlanNext.** Round-44 scratch counter (`counter.diff` applied to the frozen `round44_c1_verify.py`) + the 15-fixture `rc_close.py` battery (stub order tool, stub census): `MUTANTS total=26 killed=22 survived=4 invalid=0 null_detected=0 unattributed=0`, `PINS total=3 mismatched=0`, `BATTERY fixtures=15 wrong=0 tampered=0 sidechannel=0`. Of the 33 selftest-survivors: **21 killable by exit-code direction, 7 stream-only, 4 unreachable (1 env-gated `SHOKUNIN_ROOT`, 3 counter-gated `--work` reuse), 1 equivalent (L180)**. The do-nothing control (Q37) is measured: each standing battery alone, and all three, kill **0 of 26** (29+42+33 = 104 fixtures, `killed=0 survived=26`).
2. **Coverage: `polyglot-c-py` first** (new graded-state class: one agent file run by the grader in two interpreters, directory-listing precondition). Oracle measured offline today: PASS on host gcc 16.2.1. Runners-up: `sqlite-db-truncate` / `count-dataset-tokens` (F1 variants, low novelty), `prove-plus-comm` (no `coqc` on host).
3. **Novelty: the attempt-1 F1 census draft is NOT claim-ready; it is viable next round only as a repaired instrument with its own controls, and it DOES need a do-nothing control.** Run today: the draft instrument crashes (TypeError) on first execution; after a one-token scratch fix it measures `grader_literal=12 nt_any=14 derivable=7 spec_mismatches=5` against a frozen spec and counter that demand `14/14/≥5/0`. A do-nothing "echo" instrument prints `spec_mismatches=0` and satisfies the C3 counter's V3/V4/V8 string/count tests. Prior art is closer than R44 priced.

## 1. Calibration — `round_close.py` survivors as a third-tool claim

### 1.1 Commands and results (this seat, this round)

```
S=/fast/scratch/hyaku/kengaku-r45/R45PlanNext; export TMPDIR=$S
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane          # 05b02e2
patch -s -o $S/ctr/c1_rc.py $S/lane/plans/round44_c1_verify.py .ufo/waves/round-44/wave/R44PlanNext/counter.diff   # scratch counter, outside the lane
cp .ufo/waves/round-44/wave/R44PlanNext/rc_close.py $S/bat/
envelope.sh $S/env python3 $S/ctr/c1_rc.py --lane $S/lane --battery-dir $S/bat --work $S/w        # run 23:28:46→23:29:01 exit 1 (dev mode, PREDICATE n/a)
```
```
PINS total=3 mismatched=0
BATTERY fixtures=15 wrong=0 tampered=0 sidechannel=0
MUTANTS total=26 killed=22 survived=4 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/0 order=0/0 round_close=22/26
ADVERTISED direct=26 indirect=0 none=0
```
(`rc-26-mutants.out`.) The four survivors, verbatim: `C145b … env-gated: SHOKUNIN_ROOT`, `C243a/b/c … counter-gated: reused --work` (all `SURVIVED exhibits=none`).

Do-nothing control, standing batteries as the battery under the same 26 mutants (23:29:26→23:29:42, three runs, `--battery-dir lane/plans/battery4{2,3,4}`):
`fixtures=29 … killed=0 survived=26`; `fixtures=42 … killed=0 survived=26`; `fixtures=33 … killed=0 survived=26` (29+42+33 = 104, the honest-fixture count of the frozen C1 counter). A flat copy of all three into one dir gives `fixtures=95` (same-named modules overwrite each other: `a_row.py`, `o_scan.py`; my measurement artefact, not a counter finding) and also `killed=0`. Use the per-directory form.

Stream-only recheck (`tx.py`, direct ref-vs-mutant, 23:29:44→23:29:51): `REF-STABLE True`; the 7 stream-only rows reproduce exactly (L116 dup-receipt stdout; L165 `--lane <file>` stderr; L200a/L200b stdout; L201/L210 stderr; L300 selftest stderr), each rc-equal (`0>0`, `2>2`, `1>1`).

### 1.2 Class table (33 selftest survivors of `round_close.py`, R43PlanNext §A.3 → R44PlanNext §A → today)

| class | n | which | counter price |
|---|---|---|---|
| rc-directional, killed from nothing (22 mutants = 21 sites + L170 `!=→==` extra) | 21 | L98×2, L122×2, L132, L145 `and→or`, L149, L168, L170, L175, L178, L182, L319–L331 selftest/census guards, L326 `is→is not`, L326 `round is None` | one `TOOLS` + `PINS` entry, one argv-shape branch (exact `--lane/--round/--census/--work/--selftest`), 26 `MUTANTS` rows, `FLOORS` becomes `{anchor:4, order:1, round_close:21}`; counter delta is 10 KB, ~13 s/run |
| stream-only (reachable, rc-equal) | 7 | L116, L165, L200×2, L201, L210, L300 | a stdout/stderr direction the counter lacks: keep `r.stderr`, a scratch-path normaliser, one `exhibits` branch, ~15 lines (R44PlanNext §A.3) |
| unreachable | 4 | L145 `env_root` (env-gated); L243×3 `--work` reuse (counter-gated) | none; name as limits (not provable for every fixture) |
| equivalent | 1 | L180 `find_census` returns only existing files | name |

### 1.3 What changed since R44PlanNext (the planning-relevant delta)

- **Fence dependency is real and unresolved.** Round 45's `plans/fixture_fence.py` does not exist at `05b02e2` (`ls plans/fixture_fence.py` → no such file). The round_close battery is the first battery whose fixtures put a repo at `d/lane` (nested), use `--lane .` over a non-repo, and a `--lane d/lane/sub` inside a repo. The frozen round-45 honest leg admits only battery42/43/44 (104). **Whether the new fence admits `rc_close.py`'s 15 fixtures is unmeasured** — run it through `breach()` once `fixture_fence.py` lands, before round 46 freezes. R44PlanNext A.4 (F6: `lane_breach` without a ceiling is environment-dependent for L168) is exactly the class the round-45 fence's "`.git` ABOVE d up to the module build root" leg decides.
- **Order tool is a stub, so this prices the gate's legs only** (R44PlanNext A.4, unchanged): `order_check.py` itself is already priced by U14c etc. Leg `order_argv_breach` does not apply to a third tool.
- **`adv` quotes are still placeholders** (the scratch counter's `adv` cells); a freeze needs real quoted sentences with file:line from `plans/round_close.py` docstring (`:18-20`, `:25-31`, `:33-35`, `:37-40`, `:52-53` per R44PlanNext) — the L168/L170 rows map to the Limits bullet.
- Routed ledger today: `ROWS total=60 open=23 blocked=1 closed=34 refused=2`, `routed_open=24 oldest_round=39` (`R45NoHarmBaseline/m4-routed.txt`); `R45DistillRouted` groups 24 → 9.

### 1.4 Price and recommendation

A third-tool C1 claim is cheap (~10 KB counter delta + one 6 KB module, 15 fixtures, ~13 s) and a "fixture fence + battery for a gate the fence now covers" is a natural round-46 pairing with the round-45 fence. Calibration count to state before the freeze: **advertised-vs-demonstrated: 33 survivors, 21 demonstrable → 0 demonstrated by any landed battery today (standing batteries 0/26)**; counted after: `killed=22/26` with the 4 survivors named. Required before freezing: (1) fixture_fence.py landed; (2) the 15 fixtures admitted by it with zero outside opens; (3) decide L168 (keep it only if the fence's ceiling makes the fixture environment-independent; else 20 environment-independent mutants); (4) real `adv` quotes; (5) the stream direction only if the 7 are to be counted, otherwise carry them as a named limit. Carry rather than claim is also defensible: the novelty/coverage axes are the capped ones (calibration is 8).

## 2. Coverage candidates (task list walked independently; cross-checked with `R45ScoutTB2.md`)

Denominator check: `GET api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88…?recursive=1` → `truncated=False`, 1446 entries, 92 top-level names (89 task dirs + 3 root files). Lane has 10 `tb2-*-grader.md` files; with password-recovery (S149–S156) **11 of 89, 78 unread**. Class histogram (R43ConsiderThese, `:15-25`): F1 14 (2 read after r45), F2 18 (4), P1 26 (1), M1 7 (1), B1 6 (1), S1 7 (1), V1 3, G1 3 (1), D1 1, W1 2, O1 2. Largest unread mass: **P1 25/26 unread**, F2 14/18, F1 12/14.

Host check (`command -v`): gcc `/usr/bin/gcc` (16.2.1 20260810), python3, rustc, openssl present; `coqc` NONE, `R` NONE, `pandas` absent, `pytest` absent from system python (use `uvx`).

| rank | task | class | bytes (grader / task) | offline | why / limit |
|---|---|---|---|---|---|
| 1 | **polyglot-c-py** | P1 (new shape: one agent file executed by the grader as two languages; listing precondition) | test 1564 / 8 files | **measured**: `solve.sh` (relative `mkdir -p polyglot`, run with cwd = remapped `/app`) → `GRADER oracle PASS` on gcc 16.2.1 (`polyglot-run.sh`, 23:32:13→23:32:15); gcc warns `missing terminating " character` (`main.py.c:44`) | `instruction.md` says python 3.12.3 / gcc 13.2.0; image is ubuntu:24.04 → name the toolchain divergence. Grader quirk **observed**: `os.listdir("/app/polyglot") == ["main.py.c"]` runs before the gcc build, and the build leaves `cmain`; re-grading the same state fails (second grade listed `['main.py.c','cmain','x.c']`) — a non-idempotent grader and an unsorted listing compare (`test_outputs.py:17-19,23-25`). No network |
| 2 | sqlite-db-truncate | F1 (threshold set-intersection `> 6` of 8) | 1097 / 4096 B db | measured by R44PlanNext B.3 (oracle pass; 6/8 FAIL, 7/8 pass; duplicates FAIL) | python stdlib only; sibling of #6 db-wal-recovery, low novelty |
| 3 | count-dataset-tokens | F1 (substring of 5-digit constant) | 467 / 5016 | not measured; instruction forbids spaces/commas, grader doesn't check (`R45ScoutTB2` §2a) | same family as feal-linear's substring; one more F1 variant at most |
| 4 | prove-plus-comm | P1 (compiler verdict + text lint) | 1147 / 5900 | **blocked on host**: `coqc` NONE (pacman paused) → textual legs only, unless an official binary is installed into `~/.local/bin` outside any bwrap run | `"admit" not in content` is lower-case only `[INFERENCE: not run]` |
| 5 | openssl-selfsigned-cert | F2 (6 tests; openssl subprocess checks) | 160 lines | untried; openssl on host | untested candidate from my walk, not in R44/R45 scouts |
| not recommended | pytorch-model-recovery (10 MB `.pt`), train-fasttext (11.5 MB tar), query-optimize (50.6 MB DB), qemu-* (no emulator), break-filter-js-from-html (pinned older CPython + selenium wheels; R44PlanNext B.4: oracle FAILS on 3.13.16, passes 3.13.5/8), fix-ocaml-gc (network at grade time) | | | | policy/download blockers unchanged |

Worth adding to the Frontier mined-mistake rows from this walk (routing only): (a) polyglot-c-py's non-idempotent listing check above; (b) dead-assert family now at 4 members — `password-recovery` `len(guesses) > 0`, `code-from-image` `startswith("bee26a")` subsumed by equality, `vulnerable-secret` format asserts (`R45ScoutTB2` §4) — and count-dataset-tokens' instruction↔grader drift.

## 3. Novelty — the F1 answer-leak census (attempt-1 draft)

Draft files: `.ufo/waves/round-45/attempt1-unclaimed/plans/{f1_leak_census.py,census-spec-r45.json,round45_c3_verify.py}`, 13 task captures (972 KB, 107 `SHA256SUMS` lines). Spec: 14 tasks; census captures cover 12 tasks, with feal-linear (`corpus/evidence/round44/…`) and password-recovery (`corpus/evidence/round45/tb2-password-recovery`) coming from the existing captures.

### 3.1 Is it a viable claim next round? — not as drafted; viable as a repaired instrument

Run (scratch overlay `$S/c3/lane` = lane `corpus`+`plans` + the draft's files + the R44 receipts; envelope 23:30:27→23:30:36):

1. `python3 plans/f1_leak_census.py --lane …` → **`TypeError: unsupported operand type(s) for -: 'list' and 'set'`** (`f1_leak_census.py:127`, `channels - {"derivable"}` with `channels` a sorted list). The draft was never executed before the attempt died.
2. After one scratch fix (`set(channels) - {"derivable"}`, scratch only; `c3-draft-run.out`): `census tasks=14 grader_literal=12 nt_any=14 derivable=7 no_leak=0 spec_mismatches=5`, exit 1. The C3 counter's V8 requires `grader_literal==14`, `nt_any==14`, `derivable>=5`, `no_leak==0`, `spec_mismatches==0`. Per task (measured vs the frozen spec's `channels`):
   - `chess-best-move`: measured adds `instruction` (spec: derivable, environment, readme);
   - `feal-linear-cryptanalysis`: measured `derivable,other`, spec `derivable,environment` (the capture dir is flat — `gen.py` at the root, not `environment/`);
   - `password-recovery`: measured adds `solution` (spec omits it);
   - `fix-git`, `sqlite-db-truncate`: `decide_ok False` (the `tokens_decide` `md5` / the 8-line `decide_lines` do not sit on the spec'd lines) → the two missing `grader_literal`.
   So the spec was stipulated, not measured; the instrument is sensitive (see 3.2) and disagrees with it on 5 of 14 rows. The spec must be re-derived from the instrument or the instrument's channel rule corrected, and re-frozen with the true counts — the count `14/14` is the R44 labrat's claim, not what the instrument prints.

### 3.2 Does it need a do-nothing control? Yes — and the draft counter has none

- **Echo control (measured).** `echo_census.py` reads only `census-spec-r45.json` and prints the expected table with `spec_match=yes`: its last line is `census tasks=14 grader_literal=14 nt_any=14 derivable=7 no_leak=0 spec_mismatches=0` and `grep -c "spec_mismatches=0"` → 1. C3's V3 is `rc == 0 and "spec_mismatches=0" in out`, V4 is byte-equal to the receipt, V8 reads the summary line — the echo satisfies V3/V4/V8, so those three would be green for an instrument that measures nothing. V1/V2/V5/V9 test digests and file existence. The counter therefore only passes a measuring instrument by virtue of V3–V4 not being separable from the echo.
- **Mutation control (measured, the one that discriminates).** Deleting `count-dataset-tokens/README.md` from the scratch capture flips that row to `channels=none spec_match=NO` and the summary to `nt_any=13 no_leak=1 spec_mismatches=6`; restoring it returns `spec_mismatches=5`. So a claim needs a hostile capture control (planted/removed channel per channel class) and an echo control; both are cheap.
- Also needed: a Q37 do-nothing "before": before `plans/f1_leak_census.py` exists the receipt is absent (V3/V4 read nothing). State it as `checks=9 defects=…` on a clean clone before the instrument lands, like C2's `control-c2-nothing.txt`.

### 3.3 Prior art — closer than R44ScoutPriorArt priced

- R44ScoutPriorArt (`wave/R44ScoutPriorArt.md:31-35`): substring/constant-compare graders as a class `published` (Berkeley RDI "Weak String Matching", etc.); the feal instance `not found`.
- Today's `web_search` (two queries, 2026-10-26 ~23:30 -03; **synthesised answers, not primary sources — do not cite**) both assert README answer disclosure: `code-from-image/README.md` complete expected hash, and (second query) `password-recovery`, `crack-7z-hash`, `gcode-to-text` READMEs. Primary check I ran: `curl` on `raw.githubusercontent.com/harbor-framework/terminal-bench-2/main/code-from-image/README.md` → **HTTP 200, 1 hit** for `bee26a133f`; the two TB1 `archive/…/README.md` URLs the synthesis cited → **HTTP 404** (wrong/moved paths). So at least one per-task README leak is in public view; a per-task 14-row census is **not found** in my two searches, but the dated receipt (`corpus/evidence/round45/prior-art.txt` per V9) was never produced and the novelty sentence cannot go in before it is. Expect "partly published (class + instances), census unpublished" with no stronger claim.
- Value as a lane capability: the lane's novelty axis is 7 and stalls on assimilation of published ideas. A **census** is a finding, not a capability; the capability version is a re-runnable **leak lint**: for any pinned TB2 task dir, decide mechanically which published non-test channels carry the grader's answer tokens (README / instruction / environment / solution / task-deps / generator), with the channel enum, a decide-line extractor, and hostile + echo controls. That composes with the lane's grader-entry package and gives each future S-row a computed "leak surface" field.

### 3.4 Verdict on the draft

Viable next round only after: (1) fix the crash and the channel rule (flat vs `environment/` captures, nested channel dirs); (2) re-derive the spec from the instrument, not the labrat's table; (3) add echo + capture-mutation controls, and a Q37 before count; (4) produce the dated prior-art receipt; (5) retire `derivable` as a spec-cited receipt path unless each receipt is itself re-run (today it counts the existence of five R44 receipt files — a file check, not a measurement; the R44PlanNext oracle runs measured four more: password-recovery, sqlite-db-truncate, vulnerable-secret (`-std=gnu99`), code-from-image); (6) reuse the already-landed password-recovery capture (now S149–S156) instead of re-capturing.

## 4. Round-46 candidate list (for `### Planned (round 46)`)

| # | axis | claim | before → after (counting command) | cost / blocker |
|---|---|---|---|---|
| 1 | calibration | round_close as third tool of the battery counter: 21 rc-directional survivors killed with attribution, 7 stream + 4 unreachable + 1 equivalent named | before `killed=0 survived=26` standing (measured, 3 batteries); after `killed=22 survived=4` (measured today in scratch) via the next round's counter | needs `fixture_fence.py` landed and the 15 fixtures admitted by it; real `adv` quotes; L168 decision |
| 2 | calibration (alt) | stream direction (~15 lines) to add the 7 | 22/26 → 29/33 | counter edit; named limit otherwise |
| 3 | coverage | `polyglot-c-py` admitted (P1 new shape), ~12–16 case probe incl. extra file, leftover `cmain`, C-only / Python-only, non-idempotent re-grade | 11 → 12 of 89 | gcc divergence (16.2.1 vs 13.2.0) is a named limit; ~1 h, no network |
| 4 | coverage (alt) | `sqlite-db-truncate` (F1 threshold) or `count-dataset-tokens` (substring) | 11 → 12 of 89 | low class novelty |
| 5 | novelty | F1 **leak lint** (repaired census) with echo + capture-mutation controls and a dated prior-art receipt | before: instrument crashes (`TypeError`), C3 counter unrunnable (`FROZEN-FILL` pins); after: instrument runs, `spec_mismatches=0` from measurement | prior art partly published; needs the receipt before any novelty sentence; do-nothing control required |
| 6 | routed | land the drafted rider fixes (R39-R2, R42-R3-26/27, R42-R6) / envelope v3 | `routed_open=24 oldest_round=39` | carried from the round-44 plan; `R45DistillRouted` groups 24 → 9 |

## Limits

- The round_close measurement uses a scratch counter (the R44PlanNext `counter.diff` on the frozen round-44 counter), not a landed or frozen one; `adv` cells are placeholders; no fixture of this seat is offered as battery material.
- Whether the round-45 fence admits the 15 round_close fixtures was not measured (the fence does not exist at `05b02e2`).
- The census run is in a scratch overlay with a one-token fix; the draft files in `attempt1-unclaimed/` are untouched. Prior-art web results are search syntheses plus one primary `curl` (HTTP 200) and two 404s; no primary check of TB1 archive READMEs.
- The polyglot probe ran the grader's single test function through a path-remapped import (no pytest, `/app` → scratch), host gcc 16.2.1 not the image's gcc; two cases (oracle, extra-file/leftover-`cmain` re-grade), not a case table.
- openssl-selfsigned-cert was read only by `def test_` names and imports, not executed.
- No subagents; no lane file edited; scratch removed with `scratch_guard.py safe-rm`.

VERDICT: r46-candidates-6
