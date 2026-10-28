# R50FRScribeMistake — `## Mistakes` rows for `corpus/lessons/round-50.md`

Seat: `R50FRScribeMistake` (scribe). Axes served: **novelty (R50-C1)** and **calibration (R50-C2)** — the rows are
pointer-bearing artifacts under the C2 surface, and row 3 bears on whether the C1 predicate certifies the property
it names.

- `REV d6f2fce9889f429162c12f851bae41891bedf5cd` (lane tip at measurement; `branch=master`).
- Freeze-ancestry check before any measurement:
  `git merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD` → exit 0, `FREEZE_IS_ANCESTOR=yes`.
- Measured tree: `git clone --shared` of the lane at the tip, at
  `/fast/scratch/hyaku/kengaku-r50/R50FRScribeMistake/lane`; `git rev-parse --show-toplevel` printed that path.
  No lane write, no commit/push/stash/checkout, no production file touched.
- Wall-clock of the wave snapshot: `2026-10-28 17:43 UTC` (the wave was still running — see row 5's limit).

## 1. Commands run (exact, in order)

```
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && git rev-parse HEAD
git merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
git log --format='%h %ad %s' --date=iso 71f5f5f..HEAD
git log --all --oneline -- plans/round49_c1_verify.py        # 0 commits (same for round49_c2/round48_c1/round48_c2)
git show d6f2fce:plans/fixture_fence.py | sha256sum          # 57adce4a…
for r in 3b02d57 c3372a9 6db0279 d6f2fce; do git show $r:plans/round50_c1_verify.py | sha256sum; done
git diff --stat f7281bc 3b02d57 -- plans/                   # empty: identical plans tree
python3 plans/round50_c2_audit.py --lane .                  # inside the clone, cwd=scratch
python3 -c '…json.load(open("plans/mutants50/c1-mutants.json"))…'   # count/mutants/dropped_unwitnessed
wc -l plans/honest50/population.txt; sha256sum plans/honest50/population.txt
git config --get-all credential.helper
env GIT_CONFIG_GLOBAL=/dev/null git config --get-all credential.helper
env GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git config --get-all credential.helper
grep -rn 'External git program failed' .
ls .ufo/waves/round-50/ ; ls .ufo/waves/round-49/
python3 -c '…w1-spec.json items/roles; w1-dispatch.json counts; report-file attrition…'
```

Verbatim evidence (selected):

```
d6f2fce9889f429162c12f851bae41891bedf5cd
FREEZE_IS_ANCESTOR=yes
d6f2fce 2026-10-28 14:38:49 -0300 round-50: mutant battery frozen at the 15 witnessed rows; seven unwitnessed rows dropped and listed
6db0279 2026-10-28 14:25:30 -0300 round-50: S3 fence repair (five documented git shapes resolved by containment), sealed50 hostile set, re-derived mutant battery, Q41 lesson
c3372a9 2026-10-28 14:24:13 -0300 round-50: C1 counter open-window repair (module attribution keyed by path, not basename); predicate unchanged
822f3b7 2026-10-28 14:24:13 -0300 round-50: C2 corrections (12 pointers resolved append-only), git-doc sources S173-S177, honest-geometry knowledge entry
5c56819 2026-10-28 14:20:47 -0300 round-50: w1 v2 wave spec + dispatch evidence (72 seats, 34 attack, policy v2 accepted)
3b02d57 2026-10-28 14:18:09 -0300 round-50: C1 four-control receipts and C2 before/selftest receipts (pre-data)
f7281bc 2026-10-28 14:15:28 -0300 round-50: stage-1 freeze of C1 (honest-geometry instrument, 126-fixture population, controls) and C2 (pointer audit)
```

```
TIP d6f2fce9889f429162c12f851bae41891bedf5cd branch=master
POINTERS total=277 paths=218 hashes=59 resolved=277 exists=206 superseded=3 never-landed=9 unresolved=0
EXIT=0
```

```
# credential helper visible
/usr/lib/git-core/git-credential-libsecret
# env GIT_CONFIG_GLOBAL=/dev/null git config --get-all credential.helper
(empty)   rc=1
# env GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git config --get-all credential.helper
(empty)   rc=1
```

```
plans/round49_c1_verify.py                    0 commits
plans/round49_c2_verify.py                    0 commits
plans/round49_population.txt                  0 commits
plans/honest49/population.txt                 0 commits
plans/round48_c1_verify.py                    0 commits
plans/round48_c2_verify.py                    0 commits
```

```
counter digests: 3b02d57 f9b9873e… | c3372a9 d8787b34… | 6db0279 d8787b34… | d6f2fce d8787b34…
fence at d6f2fce: 57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1  (== receipt FENCE sha256)
population: 130 lines, sha256 b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69
mutants: count=15 mutants=15 dropped=7 (c50-10-inside-prefix, c50-11-config-cr, c50-12-config-include,
         c50-13-no-symlink-leg, c50-20-argv-no-containment, c50-22-store-requirements-none, c50-24-log-any-name)
```

```
corpus/evidence/round50/c1-receipt.txt
REV d6f2fce9889f429162c12f851bae41891bedf5cd
TREE dirty=0
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=18 clean=18 leaked=0 build_errors=0
MUTANTS total=15 caught=15 broken=0 floor=12 verdict=met
PREDICATE R50-C1 pass
# exit=0
```

```
.ufo/waves/round-50/: build_spec.py claims w1 w1-dispatch.json w1-spec.json w1.ready w1.ready.partial
.ufo/waves/round-49/:  build_spec.py w1 w1-dispatch.json w1-results.json w1-run.err w1-spec.json w1.ready w1.ready.dispatched
w1-spec.json items=72; roles: executor 21, critic 20, reviewer 9, scribe 8, scout 6, mutation-tester 5,
connector 1, simplifier 1, revenger 1  → attack (reviewer+critic+mutation-tester) = 34
w1-dispatch.json counts: {"spawn": 72, "resume": 0, "total": 72}
w1: 41 top-level *.md seat reports, 12 seat subdirs; 31 of 72 named seats have no report file at measurement
```

## 2. Drafted rows — `corpus/lessons/round-50.md` §Mistakes

Rows 1, 2 and 6 exist in the landed file (`corpus/lessons/round-50.md:13-15`, committed at `6db0279`) and are
reproduced here **refined against measured evidence** (row 1's pointer did not resolve; row 2 gains the r49-specific
history check and the "what changed" column). Rows 3–5 are new, mined from seat reports in this wave. Paste under
the existing table header (`| class | evidence pointer | captured-by | fix |`).

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **landing** — a fixture test shell `export`ed `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null` into the shared shell; the lane's git credential helper lives in the global config, so every `jj-lane.sh` push failed with the opaque `External git program failed:` and exit 3 until the variables were unset | mechanism re-witnessed 2026-10-28 at `d6f2fce`: `git config --get-all credential.helper` → `/usr/lib/git-core/git-credential-libsecret`; `env GIT_CONFIG_GLOBAL=/dev/null git config --get-all credential.helper` → empty, rc=1. Rule carried into every seat: `.ufo/waves/round-50/build_spec.py:41` (in `w1-spec.json` context). **No push-attempt receipt exists in the lane** (`grep -rn 'External git program failed' .` matches only this lesson row); timeline anchors are `f7281bc` authored 14:15:28, `claims/*.txt` mtime 14:17, `3b02d57` 14:18:09 | none — no criterion covered shell hygiene; re-witnessed by `R50FRScribeMistake` | fixture git env is set per command (`env VAR=… git …`) or in a subshell, never `export`ed; the wave context carries the warning. Shown able to fail: the helper list is non-empty with the host config and empty with `GIT_CONFIG_GLOBAL=/dev/null`, so a push needing that helper cannot authenticate |
| **landing** — rounds 48 and 49 froze counters in a "counting command" cell that no commit ever held, so their verdicts were unverifiable at the tip for two rounds; r49 additionally rebuilt its 124-fixture population but never measured a repair against it | `git log --all --oneline -- plans/round49_c1_verify.py` → 0 commits (same 0 for `round49_c2_verify.py`, `round48_c1_verify.py`, `round48_c2_verify.py`); `SCORECARD.md:2113` (r49 row, "counting command / measured revision" cell); `corpus/lessons/round-49.md` ("the committed MUTANTS floor and C1 stage-2 counter were not landed"). What round 50 changed: committed counter at `f7281bc` (`f9b9873e…`), one recorded open-window repair `c3372a9` (`d8787b34…`, old→new row in `plans/round-50-claims.md`), population pinned `b5197f94…` (sha256 re-checked at `d6f2fce`), scored receipt `corpus/evidence/round50/c1-receipt.txt` at `REV d6f2fce…`, C2 audit re-run at the tip by this seat: `unresolved=0`, exit 0 | QUALITY Q41 (`corpus/QUALITY.md:1112`), added this round because of exactly this class | every counter a row names exists at the tip before the row lands; `python3 plans/round50_c2_audit.py --lane .` is the gate. Shown able to fail: the same audit at `71f5f5f` printed `unresolved=12`, exit 1 (`.ufo/waves/round-50/claims/c2-before.txt`), `unresolved=0` after the corrections block |
| **instrument / false clean** — a fence that keys on names or patches the counter in-process forges `PREDICATE R50-C1 pass`; the wave recommended out-of-process scoring plus provenance-free fixture paths, and at `d6f2fce` **neither is landed**, so a passing receipt is not proof against a name-keyed fence | `R50C1CritPredicate.md` Findings 2, 7 and Receipt D (measured at `3b02d57`); `R50C1CritDoNothing.md` VERDICT (`admit_all.py` prints `pass`, exit 0, when the hostile battery dirs are absent from `--lane` and `--skip-mutants` is set); code at the tip: `plans/round50_c1_verify.py:86` + `:210` (fence loaded by `importlib` in-process), `:112` (`gen = work / f"m{i:03d}-{tag}"`, tag carries battery/module stem), `:156-157` (`--skip-mutants`, `--allow-dirty` ungated), `:268` (`ok` not touched by the skipped mutant leg), hostile leg skipped when a dir is absent (`if not d.is_dir(): continue`); counter digest `d8787b34…` unchanged from `c3372a9` to `d6f2fce`, and the claims' open-window table records exactly one repair (attribution keyed on path, not basename) | `R50C1CritPredicate`, `R50C1CritDoNothing`; QUALITY Q39 (`corpus/QUALITY.md:1061`) states the requirement the counter does not meet | score the fence out of process, build every fixture under an opaque path with no module/battery stem, and make scored mode reject `--skip-mutants`/`--allow-dirty`/`--fence` unless `--testing` is given, requiring `MUTANTS … broken=0 caught>=floor` for `pass`. **Status: not applied at `d6f2fce`** — open finding for the L1; the `SCORECARD.md:2178` sentence "decides, in separate processes with Q39 name hiding" overstates the code |
| **hygiene / landing** — production files were written into the live lane while the wave ran, so seats measured a moving target rather than the announced freeze | `R50C1CritBlind3.md:337` ("`M corpus/QUALITY.md` was already dirty before my first command, and `M plans/mutants50/c1-mutants.json`, `?? plans/sealed50/`, … appeared afterwards"); `R50C1ExecMutAttrib.md` §4 (witness target `ae47fc3e` → `6df6a2a3` → `9baedf13`, `ROWS total=19 stable=19 dropped=0`); commit times `c3372a9`/`822f3b7` 14:24:13, `6db0279` 14:25:30, `d6f2fce` 14:38:49 — all after dispatch `5c56819` 14:20:47 | `R50C1CritBlind3`, `R50C1ExecMutAttrib` (no criterion forbade mid-wave production writes; the wave context only makes seats read-only) | the L1 integrates between waves (or in a worktree); every seat binds its receipts to the `REV` it measured, and a seat whose tree moves re-reports the revision rather than reusing stale numbers — both seats did this correctly, at the cost of duplicate measurement |
| **conformance** — the round was closed and both claims scored while the wave had no `WAVE-DONE` marker, no results file, and fewer reports than named seats | `ls .ufo/waves/round-50/` → no `w1-results.json`, no `w1.ready.dispatched`; round 49 has both (`w1-results.json`, `w1.ready.dispatched`). `w1.ready.partial` 2300 B, mtime 14:40; `w1-spec.json` items=72, `w1-dispatch.json` `{"spawn":72,"resume":0,"total":72}`; at 17:43 UTC only 41 top-level seat reports exist for 72 named seats (31 names with none) and peers are still live. LOG §Round 50 already records "no `WAVE-DONE` marker was written" | the L1's own close note (`LOG.md` §Round 50); no criterion required a results file | write `w1-results.json` and the `WAVE-DONE` marker before closing a round, and record the per-seat disposition (settled / no report / still running) in the lesson — round 49 did this for its 3 empty seats; a wave that closes before it settles cannot support a "falsification wave" reading |
| **survivor / scope** — the carried r49 mutant battery (23 inline diffs against the r49 candidate) is not a battery for the repaired fence: on the shipped repair 4 of 23 change the verdict vector and 7 do not apply | `.ufo/waves/round-50/w1/R50C1ExecMutRebase-witness.tsv`; `plans/mutants50/c1-mutants.json` at `d6f2fce`: `count=15 mutants=15 dropped_unwitnessed=7` (names listed in the file); `git show --stat d6f2fce` = `-71/+10` lines; receipt `MUTANTS total=15 caught=15 broken=0 floor=12 verdict=met` | `R50C1ExecMutRebase` then the L1 re-derivation (`d6f2fce`); QUALITY Q38 (`corpus/QUALITY.md:1027`) | the frozen battery holds only rows whose kill is witnessed on the shipped fence; unwitnessed rows are dropped **and listed**. Shown able to fail: the carried 23-row battery prints `caught=4 … verdict=unmet` on the repair (`.ufo/waves/round-50/w1/R50C1ExecMutRebase-carried23-on-final.txt`) |

## 3. Findings for the L1 (calibration surface) — not claim admissions

- **F1 (pointer, row 1).** The landed row 13 cites "push attempts 14:16–14:18" in `claims/` and "first landed
  `f7281bc` at 14:19". `claims/` holds six control/C2 receipts only (mtime 14:17); `f7281bc`'s commit time is
  14:15:28; no push log exists in the lane. The row's *mechanism* is re-witnessed (credential helper invisible),
  but its *timeline* rests on the L1's account. Either add the receipt or mark the timeline as an account.
- **F2 (SCORECARD vs code, `SCORECARD.md:2178`).** "decides, in separate processes with Q39 name hiding" is not
  what `plans/round50_c1_verify.py` does at `d6f2fce`: the fence is `importlib`-loaded in-process (`:86`, `:210`)
  and fixture directories carry the battery/module stem (`:112`). The `keyed_names` control fails, but on
  honesty/hostility legs (3 honest refused, 29 hostile leaked), not because names are hidden — so it does not
  demonstrate the property Q39 asks for. Reconcile the sentence or land the isolation repair.
- **F3 (open window).** The claims' open-window table records one repair. Three seat findings recommend repairs that
  were neither landed nor recorded as declined: `R50C1CritDoNothing` (leg-presence + `--skip-mutants` gating),
  `R50C1CritPredicate` (isolation, neutral paths), `R50C1CritIdent` (population identity blind to the masked
  `.git/index`, 125/126 fixtures, and to `__pycache__` subtrees). The claims' own rule is "a measured defect …
  every repair records old→new digest"; a declined repair needs the same explicitness.
- **F4 (control receipts' description).** All four receipts in `.ufo/waves/round-50/claims/` say `REV f7281bc…` and
  `TREE dirty=1`, and their command lines carry no `--allow-dirty`, although `plans/round-50-claims.md` says the
  controls were "run through the same counter with `--allow-dirty` on the stage-1 tree". `git diff --stat f7281bc
  3b02d57 -- plans/` is empty (fence `05d5fe03…`, counter `f9b9873e…`, population `b5197f94…` identical), so the
  content is sound; the claims file's description and the receipt bytes disagree.
- **F5 (stale docstring inside the instrument).** `plans/round50_c1_verify.py:16` still prints the frozen predicate
  as `MUTANTS total=23 caught>=12`; the shipped battery is 15 rows and the receipt prints `MUTANTS total=15`. The
  docstring inside the scored instrument contradicts the scored run.
- **F6 (C2 denominator).** Three numbers describe one command: claims §C2 "before" `total=271 paths=213 hashes=58`;
  `SCORECARD.md:2171` `total=275`; my tip run `total=277 paths=218 hashes=59`. Two different "before" values at
  `71f5f5f` cannot both be right. I did not re-measure at `71f5f5f`: `plans/round50_c2_audit.py` has no `--rev`
  flag (`:139-140`) and a checkout is forbidden to this seat. The L1 should settle which number the command
  printed, or record that the two before-values have different definitions (e.g. rows appended mid-round).

## 4. Limits

- The wave was **live** during measurement (72 named seats, 41 reports, peers still running at 17:43 UTC). Row 5's
  attrition figure is a snapshot, not a verdict on the final wave; the settled fact is the missing
  `w1-results.json` / `WAVE-DONE` at the close revision `d6f2fce`.
- I did not run the C1 counter (slow mutant leg not needed for a scribe item); the `PREDICATE pass` figures quoted
  are the committed receipt's, not my run. My own run is the C2 audit at the tip (`unresolved=0`, exit 0).
- I could not re-measure the C2 "before" value at `71f5f5f` (no `--rev`; checkout forbidden).
- Commit **times** are author dates from `git log`; push times are not recorded anywhere in the lane, so row 1's
  push timeline stays an account.
- No claim admission is made here, for R50-C1 or R50-C2; no production file, SCORECARD/LOG/corpus row was edited.
- Scratch `/fast/scratch/hyaku/kengaku-r50/R50FRScribeMistake` (including the `git clone --shared`) is removed
  before yield; this report is the only citable artifact from this seat.
- No tool installed, no package manager touched, no lane mutation, no commit/push/stash/checkout.

## VERDICT

**DONE — six `## Mistakes` rows drafted with resolved evidence pointers** (three landed rows refined: the row-1
pointer is unrecorded and its 14:19 push time is unverified; the r49 counter/population never-landed fact is
confirmed by `git log --all` = 0 commits per path; three new rows from seat reports: instrument false clean
unlanded, mid-wave lane writes, missing `WAVE-DONE`). Measured at `REV d6f2fce…`; C2 audit re-run at the tip
`unresolved=0` exit 0. Six calibration findings routed to the L1 (F1 pointer, F2 SCORECARD sentence vs code,
F3 unlanded/undeclined open-window repairs, F4 control-receipt description, F5 stale docstring, F6 C2 before-value
disagreement). Scratch removed. No axis is claimed to have moved by this seat.
