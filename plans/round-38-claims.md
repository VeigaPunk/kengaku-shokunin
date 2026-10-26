# Round 38 — frozen claims (kengaku, hyaku run 8, 2026-10-26)

Baseline lane tip `fc1174f52b150999bef91f2e81da78732ca0eb9f` (the round-37 non-author spot-check). L1 `KengakuR38`
holds the canonical planner seat. Written and frozen before any battery38 fixture exists and before the first
recorded run of `plans/build_pmars_probe.py` (apart from the discarded control-time run disclosed below, only `--dry`
and `--smoke`, which run no grader, were executed).

**Disclosure (written before this file was committed):** the C2 skip-control's V2 step ran the gate with
`--rerun`, and the gate's P10 executed the frozen probe once inside the scratch clone at control time
(`control-c2-skip.txt` keeps only `P10 DEFECT fresh probe output is not byte-equal to the receipt`). That run's
output was discarded unread; it is not the first recorded run and is not evidence. The probe was already at its
frozen digest (`frozen-digests.txt`). This repeats round 37's order-of-operations mistake (`corpus/lessons/round-37.md`
§Mistakes row 3) and is mined in this round's lesson. Also known at freeze: V7 alone is satisfiable by a
hand-typed receipt whose observed verdicts copy the predictions (`control-c2-skip.txt`: `V7 ok`); V2's P10
fresh-run byte compare is what makes such a receipt red.
Controls are committed with this file under `.ufo/waves/round-38/claims/`.

Axis state carried (SCORECARD round 37): calibration 8, coverage 7, novelty 7, depth 9, operability 8,
freshness 8, adjacency 8. Lowest non-retired: coverage 7 tied with novelty 7. Coverage is chosen (tie-break as in
rounds 35–37: a pinned local source and an offline sandbox exist; the round-37 planning seat priced every novelty
candidate as published, `.ufo/waves/round-37/build/R37PlanNext.md` §4). Coverage stays capped at 7 by the open L0
question `kengaku | round-33`, so C2 is judged on its counter, not on a score move. No stagnation waiver.

## C1 — calibration: advertised gate behaviours the round-37 battery does not demonstrate

- **Surface:** `plans/pkg_gate.py` (unedited, digest `ea638822…`) and what the lane advertises about it — the gate
  docstring, `corpus/QUALITY.md` Q24/Q27, the SCORECARD capability rows `package-gate` and `gate-mutation-harness`.
- **Self-assessment vs observed state (the calibration count):** the number of frozen mutants N01–N22 (each one
  advertised behaviour, sentence named in its `adv` cell) that no battery fixture kills ATTRIBUTABLY. Sources:
  13 non-equivalent survivors of round-37 wave 2 (`.ufo/waves/round-37/falsify/F37XMut*.md`), one wave-2 diagnostic
  survivor (F37XMutP7 D1), and the shapes the round-37 freeze excluded or never executed (R37PlanNext §3.2:
  B1, B2, B5, B6, B7, B8). Mirror mutants (N02, N08, N15) test the false-red direction the round-37 list lacked.
- **Counter:** `python3 plans/round38_c1_verify.py --lane .` (docstring = the full rule; pins 14 inputs by digest;
  attributed kill rule; side-channel token scan of battery38 sources).
- **Frozen predicate:** C1 passes iff `python3 plans/round38_c1_verify.py --lane .` prints `PINS total=14
  mismatched=0`, then `BATTERY fixtures=<n> wrong=0 renamed_disagree=0 sidechannel=0`, then `MUTANTS total=22
  killed=22 survived=0 invalid=0 null_detected=0`, then `PREDICATE C1 pass`, exit 0, measured on a clean clone of
  the landing tip.
- **Before (do-nothing control, this freeze):** `.ufo/waves/round-38/claims/control-c1-nothing.txt` — the same
  command on the freeze tree (no `plans/battery38`).
- **Work:** `plans/battery38/*.py` single-purpose fixtures (wave 1 executors).
- **Kill rule:** any survivor, invalid mutant, null detection, `wrong>0`, `renamed_disagree>0`, `sidechannel>0` or a
  pin mismatch at landing → C1 not admitted, reported as an honest stop. A mutant later shown equivalent is reported
  as a limit, never removed from the list. The round-37 counter, battery and mutant list are not edited; the
  round-37 counter must still print `PREDICATE C1 pass` at the landing tip (no-harm check).
- **Limits named now:** the attribution rule ties a kill to the mutant's own clause and direction, not to the
  fixture's intent; the side-channel scan is a token heuristic (`/proc`, `ppid`, `cmdline`, `psutil`, `environ`), so
  battery38 code review by a non-author seat remains part of admission. A battery38 fixture may own its spec
  (shapes B1/B6/B8 need it); the counter only checks that the spec path is inside the fixture dir.

## C2 — coverage: the pinned TB2 `build-pmars` grader, a fourth grader class (build provenance)

- **Surface:** `corpus/knowledge/` (new entry `tb2-build-pmars-grader.md`), `corpus/SOURCES.md` (S115
  `tests/test_outputs.py`, S116 `instruction.md`, terminal-bench-2 @ `2fd12b88aafdd04a52c298e3940bcb189f9766d6`,
  opened 2026-10-26; upstream `main` byte-equal at freeze for both), README index + coverage bullet, PROVINCE
  paragraph; one §Frontier TB2 sub-bullet narrowed by one task. Edge class new to the lane: the graded state is a
  built artefact plus a source tree, checked by presence, an `ldd` string scan, directory shape and a regex over
  program output.
- **Probe (frozen):** `plans/build_pmars_probe.py` (digest `32f0771c…`), 22 cases, predictions and `violates=` tags
  in `corpus/evidence/round38/build-pmars-dry-cases-freeze.txt` (digest `93b4b60c…`; `cases=22 predicted_pass=7
  predicted_fail=15`). Captures `corpus/evidence/round38/tb2-build-pmars/` (5 files + `SHA256SUMS`).
- **Counter:** `python3 plans/round38_c2_verify.py --lane .` (V1–V7, docstring). New against round 37: the spec
  template, gate, probe, dry table and captures are pinned inside the counter (round-37 routed D7); V3 binds each
  anchor token to its own row's pin (D3); V7 derives every requirement-map label from ALL receipt cases violating
  the tag (D2).
- **Frozen predicate:** C2 passes iff `python3 plans/round38_c2_verify.py --lane .` prints `checks=7 defects=0`,
  then `PREDICATE C2 pass`, exit 0, measured on a clean clone of the landing tip.
- **Before (do-nothing control, this freeze):** `.ufo/waves/round-38/claims/control-c2-nothing.txt` →
  `checks=7 defects=4` (V2, V3, V4, V7), exit 1.
- **Skip-control:** `.ufo/waves/round-38/claims/control-c2-skip.txt` — junk entry/rows/README with correct anchors
  and a hand-typed receipt copied from `--dry` with `observed=predicted` must stay red.
- **Kill rule:** predicate not met at landing → not admitted. Prediction mismatches are allowed only when each
  `match=NO` case is named in the entry (V4); they are reported, never edited out of the table.
- **Limits named now:** the probe runs the grader, never the task image or the oracle; host bash stands in for
  Debian dash; host glibc `ldd`; canned artefacts are compiled on the host. The finding class ("the unenforced half
  of the instruction passes") is published (R37ScoutPriorArt); the entry claims a probed instance only. Prior
  upstream report: TB2 issue #59 (`build-pmars` oracle pins fail) — about the oracle, not the grader; to be
  re-opened and rowed or refused by a wave-1 seat.

## Separability

C1 reads only the gate, the round-35 spec, the round-36/37 counters and batteries and `plans/battery38`; C2 reads
only its captures, spec, probe, receipt, entry, SOURCES and README. Neither counter reads the other's work
product: C1 can pass with C2 absent and vice versa. The gate digest is shared and frozen for both.

## Frontier step (not a claim)

- Sourced claim: C2 (S115/S116 opened this round).
- Mined mistake: round-37 closure D2 — a requirement-map label chosen from one witness case
  (`tb2-git-webserver-grader.md` row `instruction.md:9 | enforced` beside `token-in-body observed=pass`). Fix:
  C2 V7's derived-label rule (shown able to fail by a wave-2 control on a relabelled map) + QUALITY criterion +
  an appended erratum on the round-37 entry.
- Routed items carried: D1 (commit round-37 wave-2 outputs), D3 (anchor check binds to any committed digest),
  D4 (`ledger-tip` red in detached clones), D6 (sibling prior art uncited).
- Assimilation: `considerthese/2026-10-25.md` proposal 2(c) (tip-receipt validator); `merge/kengaku/` re-screen.
