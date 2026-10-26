# F37CritCalibStatements — round-37 self-assessment, number by number

Seat: critic (calibration audit). Target commit: `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`
(integration tip). Scratch: `/fast/scratch/hyaku/kengaku-r37/F37CritCalibStatements` (removed at close).
All counter runs are on my own clone of that commit (`git clone --no-local … && git checkout 357deceb`),
plus two worktrees at `3ea9a1d9` (baseline) and `7d1fa691` for the baseline-state claims.

Scope: SCORECARD.md round-37 section (`:1266-1312`), LOG.md round-37 section (`:1082-1113`),
`corpus/lessons/round-37.md` (112 lines), and the two capability rows (`SCORECARD.md:566-567`).

## Headline

60 statements checked, **3 mismatches**. Two are evidence-pointer defects inside the lesson (a quoted
receipt line the named file no longer contains; a pending check whose stated expectation the bytes
contradict). One is in LOG: a freshness sentence attributes a 25-check sweep to a tip receipt that runs
8 checks and does not include `grader.py`. All headline predicate numbers are exact — C1 and C2 both
reproduce `pass` on my clone of the tip.

## Predicates on a clean clone of 357deceb (my runs)

```
$ python3 plans/round37_c1_verify.py --lane .
BATTERY fixtures=64 wrong=0 renamed_disagree=0
MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass
exit=0

$ python3 plans/round37_c2_verify.py --lane .
V1 ok listed=6 bad=0 extra=0
V2 ok gate_exit=0
V3 ok rows=3 bad=0
V4 ok cases=22 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=4 bad=0
checks=7 defects=0
exit=0

$ python3 plans/anchor_digest_check.py --lane .
rows=107 tokens=15 defects=0
```
Receipts of these three runs: `.ufo/waves/round-37/falsify/F37CritCalibStatements/c1-run.txt`,
`c2-run.txt`, `anchor-run.txt`.

Note, not a mismatch: `.ufo/waves/round-37/integrate/measure-final.txt` was measured at
`TIP 5c7d5d75…` (the landing commit), not at `357deceb`. `5c7d5d75` is an ancestor of `357deceb`
(`git merge-base --is-ancestor 5c7d5d75 357deceb` → exit 0), and my runs at `357deceb` print the same
lines.

## Checked statements (60)

Commands abbreviated: `C1` = `python3 plans/round37_c1_verify.py --lane .`; `C2` =
`python3 plans/round37_c2_verify.py --lane .`; `ANC` = `python3 plans/anchor_digest_check.py --lane <L>`;
receipts are relative to the clone root.

| # | location | statement | command / evidence | result |
|---|---|---|---|---|
| 1 | SCORECARD:1268 | baseline `3ea9a1d9…`, freeze `ca790460…`, first probe run `5c7b34e9…` resolve and are ancestral | `git cat-file -t` on each; `git log -1` subjects | match |
| 2 | SCORECARD:1269 | lowest non-retired axis coverage 7, tied with novelty 7 | SCORECARD current axis table (`:620-626`): novelty 7, coverage 7, depth 9, operability 8, freshness 8, adjacency 8 | match |
| 3 | SCORECARD:1276 | 55 frozen mutants; gate at freeze digest `ea638822…`, unedited | `grep -oE "M[0-9]{2}" plans/round37_c1_verify.py \| sort -u \| wc -l` → 55; `sha256sum plans/pkg_gate.py` → `ea63882240e6…edd41` | match |
| 4 | SCORECARD:1276 | before: `fixtures=14`, `killed=5 survived=50 invalid=0 null_detected=0`, `fail`, exit 1 | `claims/control-c1-nothing.txt`: `BATTERY fixtures=14 wrong=0 renamed_disagree=0`; `MUTANTS total=55 killed=5 survived=50 invalid=0 null_detected=0`; `PREDICATE C1 fail`; `exit=1` | match |
| 5 | SCORECARD:1276 | same on committed bytes at `44b7298a` | `claims/measure-before-committed.txt`: `TIP 44b7298a…`, `BATTERY fixtures=14 …`, `MUTANTS … killed=5 survived=50`, exit 1 | match |
| 6 | SCORECARD:1276 | after: `fixtures=64`, `killed=55 survived=0 invalid=0 null_detected=0`, `pass`, exit 0 | my `C1` at 357deceb (above) | match |
| 7 | SCORECARD:1277 | C2 before `checks=7 defects=4` = V2,V3,V4,V7, exit 1 | `claims/control-c2-nothing.txt`: `checks=7 defects=4`; `V2 DEFECT`, `V3 DEFECT`, `V4 DEFECT`, `V7 DEFECT` | match |
| 8 | SCORECARD:1277 | C2 after `checks=7 defects=0`, `pass`, exit 0 | my `C2` at 357deceb | match |
| 9 | SCORECARD:1277 | probe `cases=22 observed_pass=9 observed_fail=13 mismatches=0` | `corpus/evidence/round37/git-webserver-probe.txt` summary line; `grep -c observed=pass` → 9, `-c observed=fail` → 13 | match |
| 10 | SCORECARD:1277,1280 | knowledge files / index rows 43/43 → 44/44 | base worktree `3ea9a1d9`: `ls corpus/knowledge/*.md \| wc -l` → 43, README index `grep -cE` → 43; tip → 44/44 | match |
| 11 | SCORECARD:1277,1280 | SOURCES rows 103 → 107 | base `grep -cE '^ {0,3}\|…S[0-9]{3,}…\|' corpus/SOURCES.md` → 103; tip → 107 | match |
| 12 | SCORECARD:1280 | other axes held: novelty 7, depth 9, operability 8, freshness 8, adjacency 8 | current axis table `:620-626` | match |
| 13 | SCORECARD:1280 | registry +4 = tier A +3, tier B +1 | `corpus/SOURCES.md:126-129`: S111/S112/S113 tier `A`, S114 tier `B` | match |
| 14 | SCORECARD:1280,1289 | census exit 0 before and after; 15 W04, same set | `claims/census-before.txt` (15 W04 lines, `ok`, `exit=0`); `integrate/measure-final.txt` census section (same 15); ids identical to round-36 receipt | match |
| 15 | SCORECARD:1282 | `ledger_tip.py`: `rows=9 closed=9 observed_pass=9 mismatches=0` | `integrate/measure-final.txt`: R34 5 rows + R35 4 rows, then `rows=9 closed=9 observed_pass=9 mismatches=0` | match |
| 16 | SCORECARD:1284 | merge re-screen: 0 admit, 3 hold, 7 refuse | `build/R37ScoutMergePkg.md:57` "0 admit, 7 refuse (#4–#10), 3 hold (#1–#3)"; `:81` `VERDICT: package-0-admit-7-refuse-3-hold` | match |
| 17 | SCORECARD:1285 | S110 63-hex; at `3ea9a1d9` `rows=103 tokens=11 defects=5`; four ids S070/S072-S074 | my `ANC` on the `3ea9a1d9` worktree: `DEFECT S070 … S072 … S073 … S074 … digest-unknown`, `DEFECT S110 … digest-short detail=63-hex`, `rows=103 tokens=11 defects=5` | match |
| 18 | SCORECARD:1286 | anchor clears to 0 at the tip (`measure-final.txt`) | my `ANC` at 357deceb: `rows=107 tokens=15 defects=0` | match |
| 19 | SCORECARD:1295-1299 | landed attribution `ATTRIBUTED 55/55 UNATTRIBUTED=0`; hostile `ATTRIBUTED 6/55 UNATTRIBUTED=49` | `integrate/c1-attribution.txt` last lines; `integrate/c1-attribution-hostile.txt`: same predicate plus `ATTRIBUTED 6/55 UNATTRIBUTED=49`; `build/R37CritC1Battery/receipts/attr-honest.txt` → `UNATTRIBUTED=0` | match |
| 20 | SCORECARD:1300 | four case labels weaker than they read | `build/R37CritCases.md:25,38,39,45` = static-file-no-git, wrong-port-8081, token-in-body, wget-token-in-body, all `confounded` | match |
| 21 | SCORECARD:1304 | spec equals its freeze digest at the tip | `integrate/measure-final.txt` `sha256sum … plans/pkg-spec-r37.json` → `4c61d103…c9b6`; `claims/frozen-digests.txt` entry identical | match |
| 22 | LOG:1084 | declared C1 calibration (8) | axis table calibration 8 (`:621`); round-37 C1 verdict "8 → 8 held" | match |
| 23 | LOG:1084-1087 | 55 mutants; 22-case probe; S111-S113 @ `2fd12b88` | as rows 3, 9; `corpus/SOURCES.md:126-128` all pin `2fd12b88aafdd04…` | match |
| 24 | LOG:1089 | freeze `killed=5 survived=50`; ids M01 M05 M40 M47 M54 | `claims/control-c1-nothing.txt` `killed by=` lines: exactly those five | match |
| 25 | LOG:1089 | nine wave-1 executor seats wrote `plans/battery37/` | `ls plans/battery37/*.py` → 9 (d4, d5, p23, p4, p5, p6, p7, p8, p910); build reports `R37Bat{D4,D5,P23,P4,P5,P6,P7,P8,P910}` | match |
| 26 | LOG:1089 | 50 single-defect fixtures, one module per clause group; battery commit `a3163e67` | AST count of `FIXTURES` per module: 3+7+6+4+7+8+6+5+4 = 50; `git show --stat a3163e67` = 9 modules, `1277 insertions`, message "9 modules, 50 single-defect fixtures" | match |
| 27 | LOG:1090-1091 | landing `fixtures=64`, `killed=55 survived=0 invalid=0 null_detected=0`, `pass` | my `C1`; `integrate/measure-final.txt` same | match |
| 28 | LOG:1092 | `cases=22 observed_pass=9 observed_fail=13 mismatches=0` | probe receipt summary | match |
| 29 | LOG:1093 | `test_outputs.py:13` reads a stdout substring that `verify.sh:62,68` fill with the body | `sed -n 13p test_outputs.py` → `assert "TEST PASSED" in result.stdout, "Did not pass test"`; `verify.sh:62` `echo "Content: $CONTENT"`, `:68` `echo "Got: '$CONTENT'"` | match |
| 30 | LOG:1094 | independent re-implementation agreed 22/22 and 3/3 extra | `build/R37IndepVerdicts.md:28-29` `INDEP agree=22/22 extra=3/3` | match |
| 31 | LOG:1094 | critic ran 4 more cases, 4/4 matched | `build/R37CritCases.md:11,179` `uncovered_extra matched=4/4`; `VERDICT: …-4-uncovered-extra-4/4` | match |
| 32 | LOG:1097-1098 | baseline `defects=5`; erratum + four captures clear it | rows 17-18; `build/R37AnchorSweep/fixture-receipt.txt` `CASE F0 … defects=5/5 ids=S070,S072,S073,S074,S110`, `CASE F2-erratum-plus-captures … defects=0/0 exit=0 ok`; four capture digests equal the SOURCES tokens | match |
| 33 | LOG:1098 | Q26 and Q27 added | `corpus/QUALITY.md:383,409` both present with round-37 headings | match |
| 34 | LOG:1099-1100 | `rows=9 closed=9 observed_pass=9 mismatches=0` | row 15 | match |
| 35 | LOG:1101-1102 | six captures re-fetched at the pin, 6/6 identical, `main` not drifted | `corpus/evidence/round37/tb2-git-webserver/SHA256SUMS` = 6 files, `sha256sum -c` → 6 OK; `build/R37ReopenPins.md:214-218` `reopen-6/6`, `drift-no` | match |
| 36 | LOG:1101-1103 | round-36 counters, `grader.py` and every registry gate green on the pre-landing sweep (25/25) **and at the landing tip** (`measure-final.txt`) | `build/R37TipSweep.md` 25 rows incl. `grader.py` and `grader.py --selftest` (`:20-21`); `integrate/measure.sh` runs only c1, c2, anchor, round36-c1, round36-c2, census, sha256sum, ledger_tip = **8** groups; `grep -n "grader.py" integrate/measure-final.txt` → no output | **MISMATCH** |
| 37 | LOG:1104 | biopython 1.85 via `uv run --with` | `build/R37BatP910.md:152` `uv run --no-project --with biopython==1.85 …`; `:43` receipt carries `biopython=1.85` | match |
| 38 | LOG:1104 | bubblewrap 0.13.1 | `bwrap --version` → `bubblewrap 0.13.1` | match |
| 39 | LOG:1105 | image `alexgshaw/configure-git-webserver:20251031` pulled and removed | `build/R37DockerOracle.md:12,193` pull digest and `docker rmi` | match |
| 40 | lesson:1-4 | baseline/freeze/probe-run commits; `11/11 MATCH` for the frozen digests | row 1; `git show ca790460:<path> \| sha256sum` for all 11 lines of `claims/frozen-digests.txt` → 11 MATCH, 0 mismatch | match |
| 41 | lesson:8-10 | control C1: `fixtures=14`, `killed=5 survived=50`, fail, exit 1 | row 4 | match |
| 42 | lesson:10-13 | `control-c2-nothing` 7/4 (V2/V3/V4/V7); gate-edited `invalid=55`; mislabel `wrong=1`; example `M08 alone` | receipts: `checks=7 defects=4`; `MUTANTS … invalid=55`; `BATTERY fixtures=15 wrong=1 …`; example `fixtures=15` `killed=6` = frozen five + M08 via `ex-p3-two-word-quote` | match |
| 43 | lesson:24-27 | S111 line 13, S112 line 62, S113 line 9 quotes with digests `526aee3d…46b37`, `1dc44c92…3d05`, `62151b73…1d97`; S113 lines 1–6 git half, 7–9 served | `sed -n` on the captures (quotes verbatim); `sha256sum` + `SHA256SUMS` (all OK); instruction.md lines 1–6 clone/push, 7–9 served output | match |
| 44 | lesson:28 | S114 body line 39, digest `c217d372…4193`, opened 2026-07-14 | `sed -n 39p` → "But the script has no `set -e` / explicit failure check on the clone/push."; `sha256sum` → `c217d37253…4c64193`; meta `created_at 2026-07-14T06:32:15Z`, `state open` | match |
| 45 | lesson:31 | 22-case receipt `22/9/13/0`; dry table `cases=22 predicted_pass=9 predicted_fail=13` | probe summary; `grep -c predicted=pass` → 9 | match |
| 46 | lesson:79-82 | sweep fixtures `F0 defects=5`, `F2 defects=0 exit=0` | row 32 receipt | match |
| 47 | lesson:45 | `CASE M1-… defects=3/1 … WRONG`, `CASE M2-… defects=2/1 … WRONG` from `build/R37AnchorSweep/fixture-receipt.txt` | `grep -n "M1-erratum-wrong-correction\|M2-correction-not-in-manifest\|WRONG" build/R37AnchorSweep/fixture-receipt.txt` → `:26 … defects=3/3 … ok`, `:32 … defects=2/2 … ok`, no `WRONG`; `grep -c "defects=3/1"` → 0; the 3/1 and 2/1 lines survive only in `build/R37LessonDraft.md:52-53` and the lesson draft | **MISMATCH** |
| 48 | lesson:41 | round-36 counter printed `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0` at `7d1fa691` | worktree at `7d1fa691`: `python3 plans/round36_c1_verify.py --lane .` → exactly that line, `PREDICATE C1 pass` | match |
| 49 | lesson:43 | per-seat primary blocks sum to 50 new + 5 frozen | AST counts 3,7,6,4,7,8,6,5,4 = 50; `grep -rhoE "MUTANT M[0-9]{2} [A-Z0-9]+ killed by=" build/` unique ids → 55 | match |
| 50 | lesson:57 | drafting `killed by=` for 55 of 55 ids; landing `killed=55` | same grep at the live build tree → 55; `measure-final` `killed=55` | match |
| 51 | lesson:86 | `control-c2-skip.txt`: `V2 DEFECT gate_exit=1`, `V3 ok rows=3 bad=0`, `checks=7 defects=1`, exit 1 | receipt lines 8,10,17,19 | match |
| 52 | lesson:36 | S110 erratum: wrong token 63 hex, corrected 64 hex with the `0` restored | `len(wrong)=63`, `len(corrected)=64`, `corrected == 4f7ac05e70cf9220ea0f…`; `corpus/evidence/round36/tb2-regex-log/SHA256SUMS` carries the 64-hex value | match |
| 53 | lesson:38 | round-36 spot-check `72–82` is off by one: `expected_dates = [` at 71, nine literals 72–80, `]` at 81; `round-36.md:18` "71-81" right | `grep -n "expected_dates" capture → :71`; `sed -n 71,82p` shows 9 literals then `]`; spot-check `:68,91` say "72–82"; `round-36.md:18` says "lines 71-81" | match |
| 54 | lesson:39 | S110 requirement span is `instruction.md:1-10` | regex-log capture: requirements 1–4 and 6–10, example block starts at 11; `build/R37R36Absorb.md:16,114-115` same | match |
| 55 | lesson:99 | census 15 W04, same set as round 36 | diff of the two receipts' W04 id lists → identical (15 lines each) | match |
| 56 | lesson:100-107 | drafting 103/43/43, landing 107/44/44; entry and index row in one commit `c138da2b` | base vs tip counts (rows 10-11); `git show --stat c138da2b` lists `corpus/README.md` and `corpus/knowledge/tb2-git-webserver-grader.md` | match |
| 57 | lesson:108 | Spot-check 6: "the S110 63-hex cell must be gone" | `sed -n 125p corpus/SOURCES.md \| grep -oE "[0-9a-f]{40,}"` → still a 63-hex token; `QUALITY.md` Q26 states "the rows themselves are not rewritten (R1)" and the erratum is the correction; `anchor_digest_check.py` is green only because of the erratum (`CASE F1-erratum-only defects=4`) | **MISMATCH** |
| 58 | lesson:78,90 | disposition: freeze `killed=5 survived=50`; landing `killed=55`; `renamed_disagree=0` in every quoted receipt | rows 4, 6, 27 | match |
| 59 | SCORECARD:566 | capability `gate-mutation-harness`: `fixtures=64`, `55/55`, freeze control `killed=5`, first round 37 | rows 3, 4, 6; row ends `| 37 |` | match |
| 60 | SCORECARD:567 | capability `service-grader-probe`: `22/9/13/0`, first round 37 | row 9; row ends `| 37 |` | match |

## Mismatches, with corrected values

**M1 — LOG:1101-1103, freshness attribution.**
Stated: "the round-36 counters, `grader.py` and every registry gate stayed green … at the landing tip
(`integrate/measure-final.txt`)".
Observed: `measure.sh`, the script that produced the receipt, runs 8 command groups (round37 C1, round37 C2,
anchor, round36 C1, round36 C2, census, `sha256sum` of five files, `ledger_tip`). `grep -n "grader.py"
integrate/measure-final.txt` → no output; `registry_check.py`, `benchmark_spec_audit.py`,
`config_projection.py`, `sources_adopt.py`, `grader_perturb.py`, `state_check.py`, `gate_timing_check.py`
are absent too. They appear only in `build/R37TipSweep.md`, whose own text says row 22 changes *after* landing
(`:82`), i.e. the sweep predates the landing.
Corrected: at the landing tip 8 checks are recorded (`c1`, `c2`, `anchor`, `round36_c1`, `round36_c2`,
`census`, `sha256sum`, `ledger_tip`); `grader.py` and the other registry gates are measured on the pre-landing
sweep only (25/25), not re-run in the tip receipt.

**M2 — lesson:45 (`## Mistakes`, "count" row), receipt quote.**
Stated: `build/R37AnchorSweep/fixture-receipt.txt` prints `CASE M1-erratum-wrong-correction … defects=3/1 …
WRONG` and `CASE M2-correction-not-in-manifest … defects=2/1 … WRONG`.
Observed: that file at the tip prints `:26 … defects=3/3 ids=S110 classes=digest-short,erratum-digest-unresolved,erratum-incomplete exit=1 ok`
and `:32 … defects=2/2 … exit=1 ok`; `grep -c "defects=3/1"` → 0 and `WRONG` appears nowhere in the directory
except as a format string inside `fixture_matrix.py`. The pre-fix lines survive only as prose in
`build/R37LessonDraft.md:52-53` and in the lesson draft's own row.
The row's fix column already says the receipt is "the seat's final receipt … (eleven falsifier cases `ok` after
the matrix fix)", so the row quotes output its own cited path has overwritten.
Corrected: `defects=3/3 … ok` and `defects=2/2 … ok` in the named receipt; the `3/1`/`2/1` pair and the
`WRONG` markers are not reproducible from any file under `.ufo/waves/round-37/` (only from the drafting text).

**M3 — lesson:108 (Spot-check item 6), expected state.**
Stated: after the erratum, "the S110 63-hex cell must be gone".
Observed: `corpus/SOURCES.md:125` still carries `sha256 4f7ac05e70cf922ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c`
(63 hex) at the tip; `QUALITY.md` Q26 says a wrong token "is corrected only by an appended `Erratum (round 37)`
lesson line" and "the rows themselves are not rewritten (R1)". The green `defects=0` comes from the erratum
exemption, not from a repaired cell: the sweep's `CASE F1-erratum-only` shows S110 leaving the defect list with
the cell untouched.
Corrected: the S110 cell remains 63 hex by design; the check to run is that `anchor_digest_check.py` reports
`rows=107 tokens=15 defects=0` with the erratum present — not that the cell is gone.

## Adjacent observations (not counted)

- `.ufo/waves/round-37/build/` is **untracked at 357deceb** (`git cat-file -e 357deceb:.ufo/waves/round-37/build`
  → fatal: does not exist); 40 `.md` reports plus their receipts exist only in the live working tree, which is
  where I checked them. Every SCORECARD/lesson pointer into `build/` therefore resolves against uncommitted
  bytes. The numbers reproduce, but a clone of the tip alone cannot check them.
- The C1/C2 predicates reproduce identically at `5c7d5d75` (receipt) and `357deceb` (my clone), so the post-hoc
  attribution-audit commit did not disturb the frozen instruments.
- `plans/anchor_digest_check.py` at the tip is green partly by construction (erratum exemption). This is the
  documented contract (Q26/R1), but it means "defects=0" is not evidence that the registry token is correct —
  a distinction the lesson's Spot-check item 6 gets backwards (M3).

VERDICT: statements-60-mismatches-3
