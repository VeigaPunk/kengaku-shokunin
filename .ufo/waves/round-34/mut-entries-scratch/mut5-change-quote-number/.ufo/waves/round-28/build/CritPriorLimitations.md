# CritPriorLimitations — round 28 author-side critic report

Seat/writer: `KengakuR28.CritPriorLimitations-2` (critic, read-only). Author-side advice only; not outside
non-author closure. No production, clone, Git index or jj state touched; no subagents; no installs or updates.

Scope: round-27's carried C2 limitations (two P4 offline groups, one superseded P4 ID) and the whole
round-27 `plans/state_check.py` summary `329/318/0/6/5`, as they bear on round-28's promise
(`plans/round-28-claims.md:3` and `:10`): no MATCH conversion of those groups, and "preserve all P2–P4
boundaries". C1 (WebArena) is not reviewed here. No source openings were made, so no URL quotes apply.

Dated boundary for all historical claims: the committed receipt
`corpus/evidence/round27-calibration/state-final-json.json` (sha256
`6f4bcd6c044802472b1844e7c67112e3e25a33bda2a1dc640c2961b8d0b8d0cc`) at prereg revision
`f0ba09be0f3066daba2134b943d973ad1588f34a` (commit date 2026-10-21). Round-27 admission revision `6356b0ba…`
is named at `SCORECARD.md:873`. Code line numbers refer to `plans/state_check.py` at `f0ba09be`.

## Strongest falsifiable objection

**Round 28 promises "no MATCH conversion, P2–P4 boundaries preserved", but neither the prereg nor the
delivered checker can detect a conversion.** All six SUPERSEDED IDs in the 329-tuple, including the single
superseded P4 ID, turn into MATCH if someone edits the historical stale cell in place. After that edit the
checker still reports `mismatch=0` and exit 0.

The concrete counterexample: change `corpus/README.md:272` from `Located S043–S047 …` to `Located S043–S048 …`.

- `check_p4b` (`:2612-2619`) tests `expanded == source_ids and source_ids == expected_ids` **before** the
  `exact_base_correction` branch. The receipt's observation for `P4b.readme.covers.round26-sources` is
  `claimed_range ["043","047"]`, `SOURCES_ids [43..48]` and `base_erratum_exact true`. That means the cell
  range is the only thing currently failing the MATCH branch.
- The edit therefore yields MATCH. The base erratum at `README.md:287` becomes orphaned, and no assertion
  checks that the erratum's target still says S047. The selftest (`:4027-4085`) covers a removed, wrong-range
  or partial erratum and R27/R29 lines, but never an in-place edit of the historical row.
- `p3_record` (`:1401-1406`) and `p4_record` (`:2015-2020`) share the same order: if the current text passes
  the check, the verdict is MATCH, and supersession is only consulted when it fails. So the same in-place
  conversion applies to the other superseded IDs that use these functions:
  - `P3b.province.public-literature-registry.rows` at `PROVINCE.md:112`;
  - `P3b.province.round25-correction.rows` at `PROVINCE.md:119`;
  - `P3a.capability.*` at `SCORECARD.md:558-559`;
  - `P2a.capability.sources-registry` at `SCORECARD.md:557`. This one is checked in `check_sources_registry`
    (`:726-748`): a missing-token match takes priority over the full-restatement supersession [INFERENCE from
    the visible branch order].
- Predicted outcome [INFERENCE, static; not executed because no mutation probe was assigned to this seat]:
  the summary moves from `329/318/0/6/5` to `329/319/0/5/5` with exit 0. Any reviewer gating on
  `mismatch=0`/exit 0 passes it.
- The prereg names no preservation measurement. It has no expected whole-checker tuple and no per-ID
  comparison. Its only revert tests cover the C1 and C2 counters (`round-28-claims.md:10`). A search of the
  non-worktree `.ufo/waves/round-28/` files finds no `state_check` or `329` reference. Round-27 had
  `p23-final-preservation.txt`; round 28 has nothing equivalent.

Impacted axis: calibration8, specifically the C2 boundary statement. C1 and coverage/constructs are not
impacted. This is a **fixable defect in measurement, not a tradeoff the judge must reject**. Nothing shows
the conversion has happened: at `f0ba09be`, `README.md:272` still reads S043–S047. The problem is that the
promise is unverifiable as written.

## Prior limitations checked and found honest (no objection)

| Limitation | Evidence | Result |
|---|---|---|
| P4 offline group `P4a.scorecard.score-tokens-unverifiable` (`SCORECARD.md:760`) | `:2455`: `"OFFLINE_UNVERIFIABLE" if score_token_shape_ok else "MISMATCH"` | Cannot become MATCH by construction |
| P4 offline group `P4d.unmapped-numerics` (audit line 64) | `:3452`: `"OFFLINE_UNVERIFIABLE" if unmapped_tokens else "MISMATCH"` | Cannot become MATCH; deleting the numerics fails loudly |
| Three P2d offline surfaces (`PROVINCE.md:14,17,20`) | receipt IDs | Not P4; these are live surface rows, outside this seat's attack |
| Does the S038 allowed-cell repair reach P2–P4? | P3b only counts ID presence ≤ S042 (`:1601-1624`); P4e window is S043–S048 (`:2516`, `P4E_SOURCE_IDS`); P3e is the README index only (`:244-256`) | No path reaches S038 cells |
| Can new round-28 knowledge enter P4e? | `P4E_CITATION_FILES` is frozen at b5719440 (`:3470-3483`) | No |

Secondary latent trap (lower severity): P4e requires exact set equality between the live `used-by` cell and
the frozen citing paths (`:3505-3506`). If round 28 lists a new round-28 file in the `used-by` cell of any of
S043–S048 (for example S044, xFinder), P4e reports MISMATCH. Round-28's C2 contract instead allows extra
lesson `used-by` paths (`round-28-claims.md:27`). These are two authorities over the same cells with
incompatible rules. Keep round-28 citations off S043–S048, or disclose the conflict.

## Smallest safe correction (integration measurement; no checker edit, per prereg `:10`)

Before admission, L1 should record a per-ID preservation receipt:

1. Run `python3 plans/state_check.py --json` on the final tree. Require that its `(id, verdict)` multiset
   equals the one in `corpus/evidence/round27-calibration/state-final-json.json` (sha `6f4bcd6c…`) for all
   329 checked and 26 out-of-population IDs. This must cover by name the six SUPERSEDED IDs
   (`P2a.capability.sources-registry`, `P3a.capability.interval-reverdict.selftest-checks`,
   `P3a.capability.state-assertion-check.base-mismatch`, `P3b.province.public-literature-registry.rows`,
   `P3b.province.round25-correction.rows`, `P4b.readme.covers.round26-sources`) and the five OFFLINE IDs.
   The expected tuple is `329/318/0/6/5`.
2. Require byte-identity, versus `b9b24796`, of the historical stale cells and their errata:
   `corpus/README.md:272` and `:287-289`, `SCORECARD.md:557-559`, and `PROVINCE.md:112` and `:119`.
   Use content matching, not line numbers, if appended text shifts lines.
3. Disclose that the checker's MATCH-before-supersession order is a known limitation. Any checker fix
   (supersession-aware ordering or historical-cell byte pins) belongs in a separately disclosed later repair,
   not in round 28.

The correction is falsifiable: the README:272 edit above fails step 1 (the P4b verdict changes and the
tuple's superseded count drops to 5) and fails step 2.

## Commands observed (all read-only)

- `sha256sum` and a stdlib `json.load` that extracts verdicts from `state-final-json.json`.
- `git rev-parse b9b24796… f0ba09be…`, `git log -1`, `git show f0ba09be:corpus/README.md`, and
  `git diff --stat b9b24796 f0ba09be -- plans/state_check.py corpus/README.md corpus/SOURCES.md` (empty).
- `sed -n` on `SCORECARD.md`/`PROVINCE.md`, `ls`, and `rg` over `.ufo/waves/round-28` excluding worktrees.
- `state_check.py` was **not** executed on any tree.

Limitations: static code reading only. The runtime tuple `329/319/0/5/5` is inferred, not observed. The
`P2a.sources-registry` branch order was read only around `:726-748`. P2d surface semantics and C1 were not
audited.

## Verdict

**PARTIAL (scoped to round-28 C2's carried-limitation and P2–P4 preservation promise).**

- The carried limitations are honestly stated, and the two P4 offline groups cannot become MATCH.
- The "no MATCH conversion / preserve P2–P4" promise has no preregistered measurement, and the round-27
  checker cannot detect an in-place conversion of the superseded P4 ID or the other five superseded IDs.
- This becomes PASS once correction steps 1 and 2 are recorded.
- This is not a blanket round verdict.
