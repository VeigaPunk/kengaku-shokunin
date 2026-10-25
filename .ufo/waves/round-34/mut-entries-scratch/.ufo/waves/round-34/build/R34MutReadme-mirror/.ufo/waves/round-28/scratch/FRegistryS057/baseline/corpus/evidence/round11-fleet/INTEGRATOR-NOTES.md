# Round-11 fleet — integrator notes (L1)

Wave 1: 9 L2s in ONE batched `task` call (MISSION.md ≥8 rule): CriticDesign
(critic), ScoutGranularity + ScoutPrereg (scout), ConnectorFleet (connector),
ReviewerBaseline (reviewer), ExecutorGrader + ExecutorRecompute (executor),
ScribeReport (scribe), LabratMock (labrat). Wave 2 (post-run): CriticLanded
(critic), MutationGrader (mutation-tester), ReviewerIndex (reviewer). Routes
per MISSION.md buckets. No L2 wrote a shared file; single integration owner:
L1. L2 artifacts committed verbatim; corrections/deltas recorded here
(round-9/10 convention).

## Integration deltas (L1 changes to L2-drafted code — failing-before recorded)

1. **run_r11.py missing `import json`** (L1-authored runner, LabratMock
   caught it pre-run): the task-literal smoke command exited 1 with NameError
   at the first record; failing-before evidence preserved by LabratMock
   (`r11-mock-smoke.md`, unshimmed traceback at `/tmp/r11-mock/run.log.unshimmed`
   — ephemeral, quoted in the md). Fixed by adding the import; post-fix script
   hashes appended to `ordering.log` (`run-script-hash 2026-09-28T23:28:37Z …`)
   BEFORE the first main-run request (`descriptors` `request_ts=23:28:57Z`), so
   the ordering proof covers the exact bytes that ran. Mock re-smoke (N=1)
   after the fix: exit 0, census 24/24 per plan §4 scaled, 0 errors.
2. **grader_r11_draft.py promoted by byte-exact assembly**: merged grader.py
   segments verified `diff`-identical to their sources (head 1–783, tail
   784–936 of the round-10 grader; draft slices 145–191, 348–354, 370–474,
   481–1010) — no hand transcription. ONE deviation from the draft: the
   `r11.ordering.first_request_is_descriptors` check as drafted required ALL
   records at the minimum `request_ts` to be descriptors; real bytes tie
   (second-resolution ts; descriptors + first filler + first ack share
   `23:28:57Z` at ~5 req/s) → the draft form FAILED on the landed run
   (failing-before: `CHECKS n=280 mismatches=1`, this check only). Fixed to
   the granularity-independent causal form (JSONL is append-ordered;
   `descriptors()` issues the process's first request): first stamped record
   in FILE ORDER must be descriptors and carry the min ts. Verified against
   the bytes: descriptors is record index 0 with ts == min. The draft stays
   untouched (append-only discipline); the fix lives in grader.py with an
   in-code comment pointing here.
3. **selftest basename collision** (draft integration note, step 6): r8 and
   r11 runlogs share basename `run.log`; `run_selftest`'s tmp-copy loop now
   names copies `<key>__<basename>`. S0 control passes.
4. **recompute_r11_draft.py promoted verbatim** to
   `round11-power/recompute_r11.py` (selftest 58 checks / 0 failures before
   and after promotion; deterministic md5 under PYTHONHASHSEED 0/7/999 per
   ExecutorRecompute).
5. **Wiring added by L1** (draft header steps 2–5): DEFAULTS/PINS r11 keys
   (md5s from the landing), main() argparse + sidecar checks + grade_r11 +
   check_r11_ordering, selftest S4 (r11 ok-flip → `r11.replay.A-CKPT4710.ok`),
   S5 (r11 SUMMARY edit → `r11.summary.A-CKPT4710`), S6 (stats anchors via
   `selftest_stats()`), r11 args threaded through every selftest scenario.

## Critic design-review adjudications (CriticDesign: 0 FATAL, 1 conditional MAJOR, 6 MINOR)

- **Conditional MAJOR — void rule**: never materialized; the run landed
  0 error records, so §5's hardcoded n=64/df=63/0-error lines are true as
  stored. Vacuous; recorded per the critic's landing-block condition.
- **MINOR (a) power-table ceil**: d=0.35 exact n=64.0735 → the table's 64
  breaks the ceil convention of its sibling rows; power at n=64 is 0.79955,
  not ≥0.80. RULING: n=64 stands (hashed pre-registration; the deficit is
  0.05pp and the honest statement is "≈80% (0.7996)"). Recorded here and in
  LOG.md; power_analysis_r11.md NOT edited in place (hashed bundle).
- **MINOR (b) Φ(2.191) vs 2.192**: typo in power_analysis_r11.md; the value
  0.9858 is unchanged (Φ(2.192)=0.9858). Bundle is hashed → erratum recorded
  here + LOG, not edited.
- **MINOR (c) severity-diff error units**: the scoring table's `/64` header
  applies to the count rows only; the severity-diff row's abs error is in
  mean-`nwrong` units. Pinned by recompute's D1 convention and stated in
  analysis_r11.md's footnote line.
- **MINOR (d) degenerate verdict cases**: diff=0 falls in branch 3
  (FALSIFIED, `diff ≤ 0`), p=0.05 exactly falls in branch 2 (`p ≥ 0.05`) —
  mechanical as written; `r11_verdict` implements it without judgment.
- **MINOR (e) append-mode/OUT reuse**: probe_r11.py's import-time `LOGF`
  creates a stray empty `results.jsonl` (r8 name) in OUT; main run used a
  fresh dir (`/tmp/kengaku-r11-main`, rm -rf before launch); only
  `results-r11.jsonl` + `run.log` were landed, byte-identical (`cmp` at
  landing; md5s in PINS + LOG).
- **MINOR (f) void-rule wording vs GET-before-gen_problem**: the seed-failure
  void branch is vacuous — `prereg-precheck.log` (pre-hash) proves all 64
  seeds generate before any request existed.
- **Recommendation adopted**: run-time script hashes appended to ordering.log
  (probe_r11.py `cf754d78…`, run_r11.py `f012ab6e…` post-fix) so the
  ordering chain covers the code that ran, not just the predictions.

## Landing record

- Main run: 2026-09-28T23:28:57Z first request → 259.1 s wall, 1409
  requests, 1473 records, census exact vs plan §4 (1/64/320/960/128/0),
  finish=length 0/320, parse fails 0/320, SUMMARY `A-CKPT4710: 29/64`,
  `A-CKPT710: 21/64`.
- Landed md5s: results-r11.jsonl `c42fe3d10b6d7a1ed14c4485af03357b`, run.log
  `281cb530702995854f162e807ee66ff3`, analysis_r11.md
  `146633599d66257d47320fbc8a6bf4f4` (generated, then pinned).
- Gate after integration: `python3 grader.py` → exit 0, `CHECKS n=280
  mismatches=0 errata_pinned=1`; `--selftest` → exit 0, S0–S6 ALL PASS;
  output byte-identical under PYTHONHASHSEED 1/99/unset.
- Preregistered verdict: **ESTABLISHED** (paired diff +0.352, t=+3.431,
  df=63, p=0.0011, CI [+0.147,+0.556]; sign 26/7/31 p=0.0013, direction
  agrees → no downgrade). Severity-diff prediction abs error 0.002; Brier
  0.153; McNemar b=13 c=5 p=0.0963 (no pass-rate dose finding).

## Wave-2 findings + pre-commit wording corrections (CriticLanded §12)

- CriticLanded `LANDED VERDICT: CLEAN` — all ten landed-number/verdict/
  ordering/raw-byte re-derivations REPRODUCE under a fresh independent
  implementation (40/40 raw re-parse spot check; grader exit 0 n=280 and
  selftest S0–S6 re-confirmed).
- Four wording findings, all applied PRE-COMMIT to this round's own uncommitted
  files (knowledge entry, lessons #3, README coverage line) — append-only
  discipline untouched, no committed-round text edited:
  - (b) exhaustive negative "no source manipulates emission DENSITY…" →
    scoped to the search set ("no source was FOUND (~45 queries, 50 fetched
    sources)…").
  - (c) "the PAIRED contrast replicated / contrasts travel across batches" →
    "the r11 paired contrast reproduced the r9 direction on fresh problems at
    the preregistered power; claim paired contrasts only within this stack".
  - (d) "q4_0 KV measurably perturbs outputs" → explicitly framed as fetched
    prior-art method context (PR #21038 PPL/KLD tables), not an r11
    measurement.
  - (a) ADJUDICATED PARTLY VALID: the critic objected to the C3
    NOVEL-instrument ruling citing ScoutPrereg's M1 guidance — but M1 prices
    the preregistration composition (= C4, already labelled INCREMENTAL in the
    entry). C3's verdict is ScoutGranularity's own over its search set and
    stands; the entry now attributes the verdict and its search scope
    explicitly. No verdict change.
