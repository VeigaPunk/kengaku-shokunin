# Round 37 — advertised gate classes made demonstrable, and a third TB2 grader executed (2026-10-26, hyaku run 8)

Baseline `3ea9a1d9005cc07d0a5ce69f4ebf53a81fbcecdd` (the round-36 verifier spot-check); frozen claims
`plans/round-37-claims.md` (freeze `ca790460e9b74d4dc5870c878affd13cc9c4437a`; first recorded probe run
`5c7b34e9223f460a440596e3a76bdae8bfdd37d8`). Ancestry checked at drafting with
`git merge-base --is-ancestor`: baseline → freeze → probe run → wave-1 dispatch `44b7298a`, all exit 0.
Controls are red before any battery fixture beyond the API example and before any recorded probe run:
`control-c1-nothing.txt` (`BATTERY fixtures=14 wrong=0 renamed_disagree=0`, `MUTANTS total=55 killed=5
survived=50`, `PREDICATE C1 fail`, exit 1), `control-c2-nothing.txt` (`checks=7 defects=4`, V2/V3/V4/V7 red),
`control-c1-gate-edited.txt` (`invalid=55`), `control-c1-mislabel.txt` (`wrong=1`) and the one-fixture
example `control-c1-example.txt` (M08 alone). The eleven frozen digests in
`.ufo/waves/round-37/claims/frozen-digests.txt` all equal the bytes at the freeze commit — `git show
ca790460:<path> | sha256sum`, 11/11 `MATCH` — so the round-36 number-drift class does not recur in this
freeze. Landing-time predicate numbers below are measured on a clean clone of the landing tip (`.ufo/waves/round-37/integrate/measure-final.txt`); every other open number names the
seat that owes it.

## Gate

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| `knowledge/tb2-git-webserver-grader.md` (C2) | **Admitted** | Drafted in wave 1 (`build/R37PkgDraft/entry.md`, the drafting seat ran the frozen counter in its own clone: `checks=7 defects=0`) and integrated with the scope critic's wording fixes F1–F5, F7, F8 (`build/R37CritScope/dropins.md`), the case-independence limits of `build/R37CritCases.md` §2 and a prior-art section citing S114. Rests on the 22-case receipt `corpus/evidence/round37/git-webserver-probe.txt` (`cases=22 observed_pass=9 observed_fail=13 mismatches=0`, predictions frozen in `git-webserver-dry-cases-freeze.txt` before the first recorded run) and on the frozen C2 counter at the landing tip (`.ufo/waves/round-37/integrate/measure-final.txt`). The counter is weak by its own critic: `build/R37CritC2Counter.md` built a filler package that scores `checks=7 defects=0` (see Mistakes), so admission also rests on the wave-2 non-author re-reads. Flip to refused: any V red at the landing tip, or a re-read falsifying an entry claim. |
| S111 `tests/test_outputs.py` @ `2fd12b88` | **Admitted (mined)** | Opened 2026-10-26 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/tests/test_outputs.py`; quote, line 13: “assert "TEST PASSED" in result.stdout, "Did not pass test"”; capture `corpus/evidence/round37/tb2-git-webserver/test_outputs.py`, sha256 `526aee3d…46b37`; re-opened live by `R37ReopenPins` (`IDENTICAL`, `sha256sum -c` OK). Flip: the capture's digest leaves the pin. |
| S112 `tests/verify.sh` @ `2fd12b88` | **Admitted (mined)** | Opened 2026-10-26 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/tests/verify.sh`; quote, line 62: “echo "Content: $CONTENT"”; capture sha256 `1dc44c92…3d05`. The helper whose stdout is the assertion's whole input; it echoes the served body into that stdout. Flip: the capture's digest leaves the pin. |
| S113 `instruction.md` @ `2fd12b88` | **Admitted (mined)** | Opened 2026-10-26 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/instruction.md`; quote, line 9: “then I see the output "hello world".”; capture sha256 `62151b73…1d97`. Lines 1–6 ask for the git half, 7–9 for the served output. Flip: the capture's digest leaves the pin. |
| S114 TB2.1 issue #133 | **Admitted (mined, tier B)** | Opened 2026-10-26 via `gh api repos/harbor-framework/terminal-bench-2-1/issues/133` (URL `https://github.com/harbor-framework/terminal-bench-2-1/issues/133`, opened 2026-07-14, open at access); quote, body line 39: “But the script has no `set -e` / explicit failure check on the clone/push.”; body captured at `corpus/evidence/round37/prior-art/tb21-issue-133-body.md` (sha256 `c217d372…4193`). Tier B, not A: it is a report about the TB2.1 file by the image packager, with reproduction detail, not the pinned file itself. It makes the static-file case a replication. Flip: the issue is withdrawn or shown wrong about the TB2.1 file. |
| `tests/test.sh`, `task.toml`, `solution/solve.sh` @ `2fd12b88` (captured) | **Captured, not rows** | `test.sh` is the same pytest-exit → reward mechanism the registry already holds as S109; `task.toml` is manifest metadata read only for declared timeouts, image name and internet policy (named limits in the entry); `solve.sh` is the oracle, never executed by the frozen probe, so a row would dress it as evidence. Flip: a claim that needs one of them as its source. |
| Real-image run of the task (`build/R37DockerOracle.md`: oracle path, static-file and token-body states, `reward.txt = 1` through `test.sh`) | **Refused for the corpus; routed** | Outside the admitted instrument: `PROVINCE.md` refuses running the task image and task-validity verdicts (round-35/36 paragraphs), and the frozen claims never measured it (`build/R37CritScope.md` §2.2, F13). It stays wave evidence and is reported as a routed observation with its own limits (one run per scenario, apt-mutated containers, `/tests` copied, `/logs/verifier` hand-made, `--cpus 1` not enforced). Flip: a later round that freezes a real-image claim under its own PROVINCE paragraph. |
| Package `grader-predicate-input-types.md` (merge/kengaku; S143, S144) | **Held (unchanged)** | `build/R37ScoutMergePkg.md` §4 row 1: package bytes unchanged since round 36, its three text defects still present, no round-37 claim names it. Flip: a claim that re-opens S143 at its pin and repairs the three defects. |
| Package grader-fixture family (`spreadsheet-grader-fixtures.md`, `grader-candidate-coverage*.md`, …) and `terminal-bench-release-identity.md` (merge/kengaku) | **Refused** | `build/R37ScoutMergePkg.md` §4 rows 4–10: own-work locators not re-runnable here, duplicate ground (S100/S092 already used), or same-named files the lane holds. Flip: as recorded per row there. |
| Assimilation: `considerthese/2026-10-25.md` proposal 2(a) (read 2026-10-26) | **Mined; landed as `plans/ledger_tip.py`** | Proposal 2 (`considerthese/2026-10-25.md:39-45`) asks for a checker that “(a) re-runs every closed defect's check at tip forever”. `plans/ledger_tip.py` (`build/R37LedgerTip/`) re-runs all nine ledger rows on a clean clone of the tip: `rows=9 closed=9 observed_pass=9 mismatches=0` at `44b7298a` (`build/R37LedgerTip/ledger-tip-run1.txt`); its controls show each check can bite (`control-ctl*.txt`). 2(b) and 2(c) stay unbuilt. |

Erratum (round 37): S110 anchor sha256 4f7ac05e70cf922ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c is 63 hex digits (the `0` before `ea0f` was dropped in transcription); the capture's digest is sha256 4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c (corpus/evidence/round36/tb2-regex-log/SHA256SUMS, instruction.md).

Erratum (round 37) to the round-36 spot-check (a non-author file this lane does not edit): its “72–82” correction at `corpus/lessons/round-36-verifier-spotcheck.md:68,91` is itself off by one — `expected_dates = [` is `test_outputs.py:71`, the nine literals are 72–80 and `]` is 81, so `corpus/lessons/round-36.md:18` (“71-81”) was right. Its S110 span note is real; the exact requirement span is `instruction.md:1-10` (`build/R37R36Absorb.md` §5).

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| reference-drift / transcription — anchor digests that do not resolve: one hex digit dropped (S110) and four rows whose digest matches no committed capture or manifest (S070, S072, S073, S074) | `corpus/lessons/round-36-verifier-spotcheck.md:71`: "the row's anchor sha256 is 63 hex digits (`4f7ac05e70cf922ea0f…`) … so the counter cannot catch it"; §5 item 1 at `:88` | the round-36 non-author spot-check (a seat the lane dispatched) — no counter of that round read S110's anchor | two moves this round, one demonstrated. General sweep: `R37AnchorSweep` (`build/R37AnchorSweep/anchor_digest_check.py`) over the lane as it stands prints `rows=103 tokens=11 defects=5` — S110 `digest-short detail=63-hex` plus S070/S072/S073/S074 `digest-unknown` (`build/R37AnchorSweep/fixture-receipt.txt`, `CASE F0-lane-as-is`) — and `defects=0 exit=0` once the erratum and the four captures are staged (`CASE F2-erratum-plus-captures`). The sweep's own matrix is not green yet: `M1`/`M2` print `WRONG` although their id and class sets match, because `fixture_matrix.py:138` sets `want = len(expect_ids)` while the checker prints one line per defect — three lines for one id cannot equal one. So the sweep's receipt is the seat's final receipt `build/R37AnchorSweep.md` §5 (eleven falsifier cases `ok` after the matrix fix), and the four `digest-unknown` rows are new routing. C2-local: `plans/round37_c2_verify.py:108-119` (V3) requires each of S111-S113 to carry exactly one `sha256 <64 hex>` equal to its spec pin, and I showed it able to fail at drafting: on a scratch clone with the three rows and exact digests, `v3 ok=True rows=3 bad=0`; with S111's digest short by one hex character, `v3 ok=False rows=3 bad=['S111:anchor_digest']` (`build/R37LessonDraft/v3-falsifier.txt`). **Not yet closed:** the round-37 baseline still carries the bad cell — `corpus/SOURCES.md:125` reads `sha256 4f7ac05e…2e96f9c` (63 hex), and `grep -o "sha256 [0-9a-f]*" corpus/SOURCES.md \| awk '{print length($2)}' \| sort \| uniq -c` shows `1 63` beside `8 64`. A routed item and its fix in the same round is progress, not closure: the sweep must land before this row can say closed. |
| vacuous — the frozen round-36 battery demonstrated 5 of the 55 advertised gate classes | `.ufo/waves/round-37/claims/control-c1-nothing.txt` (`MUTANTS total=55 killed=5 survived=50 invalid=0 null_detected=0`; M01 M05 M40 M47 M54 killed, the other 50 `SURVIVED`); the round-36 counter printed `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0` at `7d1fa691` | none — the round-36 battery was built from a junk list, not from the gate's clause list; the round-36 spot-check routed "gameable" (§5 item 2) without counting survivors | `plans/battery37/*.py`: one single-branch fixture per survivor, each declaring its exact `DEFECT` set, plus the counter's renamed run (a gate must not key on a fixture's name). At drafting the wave's receipts carry a `killed by=` line for all 55 ids: P2/P3 6/6 (M02-M08, `build/R37BatP23/receipts/`), P4 4/4 (M09-M12), P5 7/7 (M13-M19), P6 8/8 (M20-M27), P7 6/6 (M28-M33), P8 5/5 (M34-M38), P9/P10 4/4 (M39, M41-M43, `build/R37BatP910/receipts/dev-run.txt`), D4 3/3 (M44-M46), D5 7/7 (M48-M53, M55) — 50 new plus the frozen 5. That is per-seat evidence, not the predicate: the single admissible total is one `MUTANTS total=55 killed=55 survived=0` line from a clean clone, at landing `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0` on a clean clone (`integrate/measure-final.txt`). |
| order-of-operations — the C2 skip-control executed the frozen probe before the first recorded run | `plans/round-37-claims.md:3-10` (disclosure): the skip-control's P10 clause "executed the frozen probe once inside a scratch clone at control time"; `control-c2-skip.txt` keeps only `P10 DEFECT fresh probe output is not byte-equal to the receipt` | the claims header itself — self-disclosed at freeze; no seat's receipt records the discarded execution | the discarded run cannot become evidence and the disclosure is the right shape, but the write-up must not be the only artefact. The probe was at its frozen digest `63cb75cf…5eedf` before that run and is re-pinned every run by C2 V5 (digest + `--dry` byte-equality) and by V2's `P10` fresh-run compare, so a hand-typed receipt is caught; the first recorded run is `5c7b34e9` and the second run's byte-equality is confirmed by `R37ProbeRerun` (`probe-deterministic-yes`, also under the gate's uv path). Rule forward: a control that executes a frozen instrument keeps the run as a receipt. |
| derived-number — two different totals are readable from the wave's own receipts for the same mutant id | `build/R37BatP5/receipt-primary-counter.txt` (`MUTANT M13 P5 killed by=p5-manifest-absent …`, `MUTANTS total=7 killed=7`) beside `build/R37BatP5/receipt-removal-table.txt` (`MUTANT M13 P5 SURVIVED …`, `MUTANTS total=7 killed=6 survived=1`) and `build/R37BatP8/receipts/p8-ablation.txt` (`killed=0 survived=1`); a grep for `killed by=` over `build/` counted 51 ids at 01:44 and 55 at 01:46 as the last seat's receipts landed, while the per-seat primary blocks sum to 50 new + 5 frozen | none — the wave has no canonical receipt index; each seat writes its own runs, and ablation runs are the falsifier that the fixture is load-bearing | the agreement above is a property of a complete wave, not of the format, and it moved while I measured it. Rule the lesson records: the only admissible C1 number is the frozen predicate line measured on a clean clone; a per-seat number is quoted from that seat's primary block and labelled as such, never by grepping `killed by=`. |

| count — a fixture matrix measured its expectation in ids while the checker answered in lines | `build/R37AnchorSweep/fixture-receipt.txt` `CASE M1-erratum-wrong-correction … defects=3/1 … WRONG` and `CASE M2-correction-not-in-manifest … defects=2/1 … WRONG`, whose `expect ids=S110` and observed classes match; `build/R37AnchorSweep/fixture_matrix.py:138` `want = len(expect_ids)` | none — the mismatch is invisible in the printed receipt (both `n` and `want` are small integers) and only the code shows why | the sweep must declare defects per line, or count distinct ids in its output, before its `ok`/`WRONG` column can be read; until then the receipt is the seat's final receipt `build/R37AnchorSweep.md` §5 (eleven falsifier cases `ok` after the matrix fix). Same class as the gate's distinct-quote vs distinct-line counters: a count is only meaningful with its unit named. |

| vacuous — the frozen C2 counter admits an informed filler package and reads an unpinned spec | `.ufo/waves/round-37/build/R37CritC2Counter.md` variants v1 (verbatim quotes, filler claims, one-row map: `checks=7 defects=0`) and v4 (`probe_cmd` in `plans/pkg-spec-r37.json` replaced by a cat of the receipt: `checks=7 defects=0`) | none — V7 was written against the cheapest filler (labels not tied to verdicts) and stops it, but nothing ties a map row to the instruction line it names, and the counter pins the probe and dry table but not the spec template it hands to the gate | not repaired inside the frozen counter (kill rule); at the landing tip `sha256sum plans/pkg-spec-r37.json` equals its freeze digest (`claims/frozen-digests.txt`), and admission also rests on the wave-2 re-reads; round 38's counter must pin every input it reads |
| vacuous — the frozen C1 counter counts a kill without attributing it | `.ufo/waves/round-37/build/R37CritC1Battery.md` §Headline: a two-module hostile battery whose `--rerun` probe reads which gate copy is running (via `/proc`) and changes its output prints the same `MUTANTS total=55 killed=55` and `PREDICATE C1 pass` (`receipts/predicate3.txt`); a SIGKILL shim counts as a kill (`receipts/crash.txt`) | none — the freeze defined a kill as any change of (exit code, DEFECT set) and never tied the changed clause to the mutant's clause or the fixture's subcommand; fixture code runs with the counter's privileges | not repaired inside the frozen counter (kill rule). The same critic's attribution audit over the LANDED battery prints `UNATTRIBUTED=0`: each of the 55 kills removes the mutant's own clause from the reference DEFECT set on a fixture of the matching subcommand (`receipts/attr-honest.txt`), while the hostile battery prints `UNATTRIBUTED=49` (`receipts/attr-hostile.txt`); the L1's re-built audit `plans/round37_c1_attribution.py` reproduces both (`integrate/c1-attribution.txt` `ATTRIBUTED 55/55`; `integrate/c1-attribution-hostile.txt` `ATTRIBUTED 6/55 UNATTRIBUTED=49` under a frozen `PREDICATE C1 pass`). The landing therefore rests on that audit plus the code review of `plans/battery37/`, not on the counter alone; round 38's counter must attribute kills, interleave null runs and hash the gate copies after each run |
Note on a gate property the battery had to absorb (not a mistake): silencing one branch changes the
observable *set*, not always one id — `build/R37BatP23.md:50` records M04 moving `(1, {P3,P4})` to
`(1, {P4})`. A single-defect fixture therefore declares every clause id its branch prints, which is why
the counter's kill criterion is the pair (exit code, clause set).

### Round-37 disposition of the seven routed items (`corpus/lessons/round-36-verifier-spotcheck.md` §5)

| §5 item | round-37 disposition | measurement |
|---|---|---|
| 1. S110 anchor digest truncated (63 hex) | **Closed (frontier fix).** `plans/anchor_digest_check.py` landed; `R37AnchorSweep` (the census's 15 warnings are all duplicate-URL lines, none about a digest); C2 V3 covers S111-S113 and was shown able to fail. | at drafting `corpus/SOURCES.md:125` still 63 hex; the sweep finds **five** unresolvable anchors (`F0` `defects=5`) and clears to 0 only with the erratum and four staged captures (`F2` `defects=0 exit=0`); V3 pair in `build/R37LessonDraft/v3-falsifier.txt`; sweep receipt at landing `defects=0` (`integrate/measure-final.txt`) |
| 2. Frozen battery gameable and clause-incomplete | **Closing (C1).** Frozen 55-mutant list, one single-branch fixture per survivor, renamed run required by the counter. | freeze `killed=5 survived=50`; drafting `killed by=` for 55 of 55 ids across nine seats; aggregate predicate landing `killed=55` (`integrate/measure-final.txt`) |
| 3. The C2 counter admitted a junk package | **Closing (C2).** V2 runs the package gate with its quote-support clauses (verbatim on the cited line, distinct, 3-25 words, ≥8 lines); V3 pins anchors; V7 ties every requirement-map label to an executed verdict. The skip-control is built at freeze and is red. | `control-c2-skip.txt`: `V2 DEFECT gate_exit=1`, `V3 ok rows=3 bad=0` with the *right* digests, `checks=7 defects=1`, exit 1 — junk quotes now fail V2; landing `checks=7 defects=0`; an informed filler still passes (Mistakes, last row) for the landing run |
| 4. Wave-1 round-36 findings not absorbed (R36CritScope F3–F6, F8, F10; two non-independent probe cases; anchor drift) | **Partly closed.** `R37R36Absorb`. | appended errata in `corpus/knowledge/tb2-regex-log-grader.md` §Errata (round 37) and PROVINCE correction R37-P1; R36CritScope F3–F5 entry wording left open |
| 5. Amendment 1 ruling on the L0 queue | **Carried, operator-owned.** No claim this round depends on the ruling. | `.ufo/l0-questions.md` |
| 6. Spot-check debt (round-36 `## Spot-check` "Pending"; items 3-4 unexecuted) | **Partly answered.** Item 4 (fixture-name keying) is now mechanical: the counter re-runs every fixture under another directory name and prints `renamed_disagree`. Item 3 (hand-run the line fixtures) is this round's `## Spot-check` item 4. | `BATTERY … renamed_disagree=0` in every receipt quoted here |
| 7. SHONEN (for the operator) | **Carried, operator-owned.** No box ticked by this round's scribes. | `SHONEN.md` |

## Census

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`.
Before (freeze): exit 0, `kengaku ok`, 15 W04 — duplicate-URL warnings on S040, S048, S057, S058, S059,
S064, S065, S066, S067, S068, S069, S071, S075, S076, S100 (`.ufo/waves/round-37/claims/census-before.txt`:
15 W04 lines, then `kengaku ok /…/corpus/SOURCES.md`, then `exit=0`). The set is the same as round 36's: no new duplicate.

At drafting time: registry rows `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`
→ `103`; knowledge files `ls corpus/knowledge/*.md | wc -l` → `43`; README index rows
`grep -cE '^\| `knowledge/[^`]+` \|' corpus/README.md` → `43`. S111-S113 and the prior-report row S114 add four
rows and the entry adds one knowledge file, so at landing the counts are `107/44/44` — the state C1's genuine
fixture is sensitive to (claims §Separability): entry and index row landed in one commit (`c138da2b`), the
consistent state.

After: exit 0, the same 15 W04 duplicate-URL warnings and no new one (`.ufo/waves/round-37/integrate/measure-final.txt`,
census section).

## Spot-check

Pending — the non-author closure for this round follows the report (LEARNING.md: a seat the lane dispatched
is still the lane). Cheapest failing check first:

1. `python3 plans/round37_c1_verify.py --lane .` on a **clean clone** of the landing tip (no untracked
   files) and record `BATTERY …`, `MUTANTS …`, `PREDICATE C1 …` verbatim. One command; fails loudest.
2. `python3 plans/round37_c2_verify.py --lane .` and record `checks=7 …`, `PREDICATE C2 …`.
3. `grep -nE 'k36-|p23-|p4-|p5-|p6-|p7-|p8-|d4-|d5-|git-webserver' plans/pkg_gate.py` → expect empty:
   no gate path may name a fixture, a battery module or this round's evidence.
4. Hand-run one mutant outside the counter: apply one frozen `old → new` replacement to a scratch copy of
   `plans/pkg_gate.py`, run it on that mutant's fixture by hand, and confirm the clause set moves. This is
   the check round 36's spot-check left unexecuted (§5 item 6) — it proves the counter is not the only thing
   that can see the branch.
5. Recompute the probe's prediction/observation join from committed bytes: parse `CASE` ids from
   `corpus/evidence/round37/git-webserver-dry-cases-freeze.txt` and `…-probe.txt`, require the same 22 ids in
   the same order, 9 `predicted=pass` vs 9 `observed=pass`, and 0 disagreements (my drafting run: exactly
   that). Then read every `match=NO` id and confirm the entry names it.
6. Anchor sweep by hand: `grep -o "sha256 [0-9a-f]*" corpus/SOURCES.md`, keep only 64-hex tokens, and compare
   each with the capture it cites; the S110 63-hex cell must be gone.
7. Re-open S111-S113 live at the pin: `curl -s <url> | sha256sum` equals the row anchor, and `sed -n <line>p`
   equals the row quote. Three rows, three digests.
8. Re-read the claims' disclosure (`plans/round-37-claims.md:3-10`) beside `control-c2-skip.txt` and confirm
   the probe digest was frozen before the discarded run (`frozen-digests.txt`).
9. Confirm no `corpus/` or `plans/` copy, and no lane mirror, sits under `.ufo/waves/round-37/build/`
   (`find .ufo/waves/round-37/build -maxdepth 2 -name corpus -o -name plans`).

## Close

Wave 2 (falsify, 37 seats, `.ufo/waves/round-37/falsify-dispatch.json`, against `357deceb`) was handed to the dispatcher after
wave 1 settled (40/40 reports, 0 dead). The L1 closed the round under the run's request budget before wave 2 returned, so no
wave-2 finding is integrated here: every verdict above rests on wave-1 attacks, the landing measurement
(`.ufo/waves/round-37/integrate/measure-final.txt`) and the post-hoc attribution audit. The non-author closure should read
`.ufo/waves/round-37/falsify/*.md` when they land.

### Wave 2 outcome (appended after WAVE-DONE falsify; 37 seats, 37 reports, `.ufo/waves/round-37/falsify-results.json`)

- Re-measures agree: C1 re-run `killed=55/55` (`F37C1Rerun`), same under Python 3.12/3.13 and two hash seeds (`F37C1RerunPy313`);
  C2 re-run pass and probe byte-equal (`F37C2Rerun`, `F37ProbeOnTip` 3/3 adversarial environments); S111-S113 re-opened live
  3/3 with quotes 3/3 (`F37ReopenRows`); battery code review 0 defects (`F37RevBatteryCode`); no line removed anywhere
  (`F37CritNoHarmDiff`); C2 landed-package mutants 10/10 caught (`F37MutC2Counter`); probe-case mutants 14/14 as predicted.
- Limits found (reported, nothing frozen edited): 36 non-frozen extra gate mutants, 23 killed / 13 survived across the nine
  modules (`F37XMut*`) — the frozen 55 are demonstrated, near-variants of the same clauses often are not; an overfit gate can
  match every battery declaration with 2 cues (`F37CritOverfit`) and the renamed run carries 5 content cues (`F37CritRenamed`);
  6 of the 55 mutant labels have no advertising sentence in the self-assessment texts (`F37CritC1Axis`); the anchor tool
  misses 4 of 5 code mutants of itself and 1 of 4 data mutants (`F37MutAnchorTool`, `F37AnchorRerun`); the attribution audit
  catches 1 of 4 of its own mutants (`F37MutAttribution`); `ledger_tip.py` false-reds (exit 1, not 2) when the source clone
  has no local `master` ref, because two pin checks hardcode `refs/heads/master` (`F37NoHarmSweep` N1; green on the
  measurement clone, `integrate/measure-final.txt`).
- Wording defects found, not yet repaired: requirement map 2/4 rows disputed (`F37CritC2Map`), 13 overclaim sentences
  (`F37CritC2Overclaim`), 3 quote claim cells and 4 prose sentences unsupported in the entry (`F37RevEntryQuotes`; no quote
  fabricated or mislocated), lesson 5 / QUALITY 6 / SCORECARD-LOG 2 / SKILL-README 1 / PROVINCE 1 defects, 3 of 60 self-assessment
  statements mismatched (`F37CritCalibStatements`), 20 wave-1 findings unaddressed (`F37ConnCrossCheck`). They are routed to
  round 38; the frozen predicates are unaffected.
