# FP4Preservation — round 28 author-side falsification report (state-preservation lane)

Seat/writer: `KengakuR28.FP4Preservation` (revenger, read-only over production). Leaf member; no
subagents, no delegation, no installs/updates (tooling directive: nothing installed; all pacman
transactions respected as paused). No production, clone, Git index, jj state, baseline fixture, source,
candidate or code byte was written. All writes were to this seat's scratch
`.ufo/waves/round-28/scratch/FP4Preservation/` and to this report.

Scope: run `plans/state_check.py --json` once, bytecode disabled, on the current worktree and compare
EVERY keyed assertion/disclosure ID verdict and summary against the frozen round-27 receipt
`corpus/evidence/round27-calibration/state-final-json.json`. Require the exact historical tuple, the 26
old OUT_OF_POPULATION IDs preserved with new disclosures enumerated, P4 exactly 51 with
48 MATCH/1 SUPERSEDED/2 offline, no in-place rewrite converting old superseded to MATCH, the known
match-before-correction limitation described (not fixed), full projection, exact receipts and hashes.

## 1. Execution receipt (single completed run; one earlier invocation died at exec)

- Invocation A (disclosed for exactness): `PYTHONDONTWRITEBYTECODE=1 /usr/bin/time -v python3 -B
  plans/state_check.py --json` → **exit 127 before any checker process started** (`/usr/bin/time` does
  not exist on this host); stdout 0 bytes. Not a checker run.
- Invocation B — **the one completed checker execution**:
  - cwd `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
  - command `PYTHONDONTWRITEBYTECODE=1 python3 -B plans/state_check.py --json` (bytecode disabled
    in-process via `-B` and inherited by every child the checker spawned via its environment)
  - **exit 0**; stderr empty (0 bytes, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`)
  - stdout saved: `.ufo/waves/round-28/scratch/FP4Preservation/state-check-round28-run1.json`,
    185,301 bytes, **sha256 `46670654146294ca4a1a1f2a0c2dc3299e84d6cb921e96b59d8de11fb9f3ff19`**
- Bytecode hygiene: no new `__pycache__` appeared under `plans/`, `corpus/`, `knowledge/`; the only two
  that exist (`plans/__pycache__` 2026-10-21 08:54:16, `plans/fixtures/r26/__pycache__` 04:51:13) predate
  the run (the run happened after the 10:37:39 pin commit).
- No-mutation proof: `git hash-object` of `plans/state_check.py SCORECARD.md PROVINCE.md
  corpus/README.md corpus/SOURCES.md` after the run returned byte-identical blob ids to the pre-run
  values (`fb31d417…, 1463bbd6…, 13fff7d6…, fe28d99d…, 39c28cf5…`).

Comparator: `.ufo/waves/round-28/scratch/FP4Preservation/compare_projection.py` → full result at
`comparison-result.json` in the same scratch dir. It compares id sets, verdicts, and full assertion
payloads (id, source_line, check, observed, verdict), not just mismatch count.

## 2. Inputs and pins

| Item | Value |
|---|---|
| b9b2479 resolved | `b9b24796277020d1b9b01923b45313d6a565e664` (2026-10-21 10:37:39 -0300, "round-27: retain clean-revision census and final path/misroot evidence") |
| Git HEAD | `18b192266389e8d6c74d0e1f1f2db337739e63dd` (round-28 build sits uncommitted in the worktree relative to HEAD; worktree blobs of the five protected files equal the index blobs) |
| Baseline receipt | `corpus/evidence/round27-calibration/state-final-json.json` sha256 `6f4bcd6c044802472b1844e7c67112e3e25a33bda2a1dc640c2961b8d0b8d0cc` (355 IDs: 329 checked + 26 out-of-population) |
| Checker bytes | worktree sha256 `5db1eb787d0724405fda8d747957b5ad84122c5410571c9b8cac3c2f6d9ac30c`; git blob `fb31d417704fae8b7447b79aec90d18253205270` — **identical at b9b2479 and current** (`git ls-tree b9b2479` = `git ls-files -s` = `git hash-object`) |
| File blobs b9b2479 → current | `SCORECARD.md a06c9869…→1463bbd6…`, `corpus/README.md 63887207…→fe28d99d…`, `corpus/SOURCES.md e16d3878…→39c28cf5…`, `PROVINCE.md 13fff7d6…→13fff7d6… (unchanged)` |

## 3. Summary projection — exact historical tuple holds

| summary field | round-27 baseline | round-28 run | equal |
|---|---|---|---|
| assertions | 329 | 329 | yes |
| match | 318 | 318 | yes |
| mismatch | 0 | 0 | yes |
| superseded | 6 | 6 | yes |
| offline_unverifiable | 5 | 5 | yes |
| out_of_population | 26 | **28** | no — +2, enumerated below (disclosed growth, not a regression) |

Exit 0 with mismatch=0 is internally consistent with the run's own verdict table.

## 4. Full per-ID projection (not merely mismatch=0)

- ID set: run 357 vs baseline 355. `base_only` = **0** — every one of the 355 baseline IDs is present in
  the run. `run_only` = exactly the 2 new OUT_OF_POPULATION disclosures (§5). No duplicate IDs in
  either document.
- **Verdict diffs: 0** across all 355 common IDs.
- **Full-payload diffs: 1** (benign, disclosed): `P2c.box.2.pointer.1` — pointer `LOG.md:7`, anchor
  `[7,7]` resolves in both; only `target_lines` moved 438 → 510 because round 28 appended log lines to
  `LOG.md`. Verdict MATCH unchanged. No other `observed`/`check`/`source_line` field differs anywhere.

## 5. OUT_OF_POPULATION — 26 old preserved, 2 new enumerated

All 26 old IDs preserved with identical verdicts and payloads; `lost_old_ids=[]`, `old_changed_verdict=[]`:

`P2a.out-of-population.grader-perturbation-audit`, `P2a.out-of-population.interval-reverdict`,
`P2a.out-of-population.state-assertion-check`,
`P2e.out-of-population.file.evidence/round25-calibration/`,
`P2e.out-of-population.file.evidence/round25-sources/`,
`P2e.out-of-population.file.evidence/round26-calibration/`,
`P2e.out-of-population.file.evidence/round26-sources/`,
`P2e.out-of-population.file.evidence/round27-calibration/`,
`P2e.out-of-population.file.evidence/round27-sources/`,
`P2e.out-of-population.file.knowledge/attribution-interval-calibration.md`,
`P2e.out-of-population.file.knowledge/extraction-policy-comparison.md`,
`P2e.out-of-population.file.knowledge/grader-perturbation-audit.md`,
`P2e.out-of-population.file.lessons/round-25-verifier-spotcheck.md`,
`P2e.out-of-population.file.lessons/round-25.md`,
`P2e.out-of-population.file.lessons/round-26.md`,
`P2e.out-of-population.file.lessons/round-27.md`,
`P2e.out-of-population.row.evidence/round25-calibration/@173`,
`P2e.out-of-population.row.evidence/round25-sources/@172`,
`P2e.out-of-population.row.knowledge/attribution-interval-calibration.md@61`,
`P2e.out-of-population.row.knowledge/extraction-policy-comparison.md@63`,
`P2e.out-of-population.row.knowledge/grader-perturbation-audit.md@62`,
`P2e.out-of-population.row.lessons/round-24-verifier-spotcheck.md@94`,
`P2e.out-of-population.row.lessons/round-25-verifier-spotcheck.md@96`,
`P2e.out-of-population.row.lessons/round-25.md@95`,
`P2e.out-of-population.row.lessons/round-26.md@97`,
`P2e.out-of-population.row.lessons/round-27.md@98`.

New disclosures (2, both `check`: "on-disk index-scope path outside frozen 6180e4f population; not
checked", `source_line`: null):

1. `P2e.out-of-population.file.evidence/round28-calibration/` — observed `evidence/round28-calibration/`
2. `P2e.out-of-population.file.lessons/round-28.md` — observed `lessons/round-28.md`

28 total at this run. These are exactly the round-28 build's measurement receipt directory and lesson
file entering the index scope — natural growth, correctly disclosed as OUT_OF_POPULATION rather than
silently admitted to P2e.

## 6. P4 family — exact 51 with 48 MATCH / 1 SUPERSEDED / 2 offline

- Total P4-prefixed assertion IDs: **51** — 48 MATCH, 1 SUPERSEDED, 2 OFFLINE_UNVERIFIABLE, 0 MISMATCH.
- The single superseded P4 ID remains **SUPERSEDED**: `P4b.readme.covers.round26-sources`.
- The two P4 offline groups remain **OFFLINE_UNVERIFIABLE** (MATCH-impossible by construction):
  `P4a.scorecard.score-tokens-unverifiable`, `P4d.unmapped-numerics`.
- No conversion of either offline group or of the superseded ID; P4 boundaries preserved exactly.

## 7. The six SUPERSEDED and five OFFLINE — named, sets equal to baseline

- SUPERSEDED (run set == baseline set): `P2a.capability.sources-registry`,
  `P3a.capability.interval-reverdict.selftest-checks`,
  `P3a.capability.state-assertion-check.base-mismatch`,
  `P3b.province.public-literature-registry.rows`, `P3b.province.round25-correction.rows`,
  `P4b.readme.covers.round26-sources`.
- OFFLINE_UNVERIFIABLE (run set == baseline set): `P2d.surface.Model catalogs.url`,
  `P2d.surface.Public literature.url`, `P2d.surface.Served local model.availability`,
  `P4a.scorecard.score-tokens-unverifiable`, `P4d.unmapped-numerics`.
- MISMATCH: none.

## 8. b9b2479 vs current — protected historical cells and checker bytes: no in-place rewrite

Byte receipts (worktree current vs `git show b9b2479:…`, ranges as named by
`.ufo/waves/round-28/build/CritPriorLimitations.md` step 2):

- `corpus/README.md:270-274` (stale range cell at :272, still `S043–S047`): **IDENTICAL**.
- `corpus/README.md:285-291` (base erratum at :287-289, `superseded by **S043–S048**…`): **IDENTICAL**.
- `SCORECARD.md:555-561` (capability rows :557 `sources-registry`, :558 `interval-reverdict`, :559
  `state-assertion-check` with their stale counts): **IDENTICAL**.
- `PROVINCE.md` whole file: git blob `13fff7d6…` identical at b9b2479, index, and worktree — byte-identical.
- `corpus/SOURCES.md`: zero `+`/`−` diff lines matching `\| *S04[3-8] *\|` — the S043–S048 used-by rows
  the P4e window reads are untouched; the file's change is elsewhere (round-28 registry rows).
- Change shape of the two modified cell files is append-only at their round-28 sections:
  `git diff b9b2479 -- SCORECARD.md` is one hunk appended after the old :884 context; `corpus/README.md`
  one hunk appended after the old :308 context. The S038 status/used-by delta lives in those appends,
  not in any historical stale cell.
- The conversion counterexample did **not** happen: `corpus/README.md:272` still reads S043–S047 (so
  `P4b.readme.covers.round26-sources` correctly stays SUPERSEDED, per run verdict), and `S043–S048`
  appears only in the erratum lines :287-288.
- `plans/state_check.py` bytes: git blob `fb31d417704fae8b7447b79aec90d18253205270` identical at
  b9b2479 and current → **no checker rewrite, no supersession-aware fix, no historical-cell byte pin
  added**. The verdicts above were produced by the exact pinned bytes.

## 9. Known match-before-correction limitation — described, not fixed

As established by `.ufo/waves/round-28/build/CritPriorLimitations.md` and re-verified by this seat in the
exact bytes that ran: all six SUPERSEDED IDs are reached only through a MATCH-first branch order.

- `check_p4b` (visible at `plans/state_check.py:2605-2625` in the running bytes): `if expanded ==
  source_ids and source_ids == expected_ids: … "MATCH"` is consulted **before** `elif
  exact_base_correction: … "SUPERSEDED"`. Editing the historical stale cell `corpus/README.md:272` in
  place from `S043–S047` to `S043–S048` would therefore flip `P4b.readme.covers.round26-sources` from
  SUPERSEDED to MATCH with `mismatch=0`, exit 0.
- `p3_record` (`:1398-1410`) and `p4_record` (`:2012-2024`): `verdict = "MATCH" if check else
  "MISMATCH"`; supersession is consulted only when the check **fails**. The same in-place conversion
  applies to `P2a.capability.sources-registry`, `P3a.capability.interval-reverdict.selftest-checks`,
  `P3a.capability.state-assertion-check.base-mismatch`, `P3b.province.public-literature-registry.rows`,
  `P3b.province.round25-correction.rows`.
- Consequence: this run's `mismatch=0`/exit 0 alone cannot detect such a conversion; that is why this
  report's preservation evidence is the per-ID projection (§4) plus the byte receipts (§8), both of
  which would catch it. Today neither conversion occurred.
- Per assignment and per the critic's step 3, this limitation is **disclosed, not repaired**: checker
  bytes are identical to the b9b2479 pin; no supersession-aware ordering or historical-cell pin was
  added by this seat.

## 10. Verdict

**VERDICT: PASS**

Every required observation held on the single completed run: summary exactly `329/318/0/6/5`; all 355
baseline IDs present with 0 verdict diffs and full-payload equality except one benign `target_lines`
drift (`P2c.box.2.pointer.1`, LOG.md append) and the two enumerated new OUT_OF_POPULATION disclosures
(28 total); all 26 old OUT_OF_POPULATION IDs preserved; P4 exactly 51 = 48 MATCH + 1 SUPERSEDED
(`P4b.readme.covers.round26-sources`) + 2 OFFLINE (`P4a.scorecard.score-tokens-unverifiable`,
`P4d.unmapped-numerics`); protected historical range/count cells byte-identical to b9b2479; checker
bytes identical to the b9b2479 pin, so the match-before-correction limitation remains live and is
described here without repair. Findings only; L1 resolves.

### Receipt index (scratch: `.ufo/waves/round-28/scratch/FP4Preservation/`)

- `state-check-round28-run1.json` — the run's stdout, sha256 `46670654146294ca4a1a1f2a0c2dc3299e84d6cb921e96b59d8de11fb9f3ff19`
- `state-check-run1.stderr` — 0 bytes
- `compare_projection.py` / `comparison-result.json` — full projection comparator and its machine result
- `b9b2479-README-270-274.txt`, `b9b2479-README-285-291.txt`, `b9b2479-SCORECARD-555-561.txt`,
  `b9b2479-PROVINCE-110-121.txt` — pinned cell extracts diffed IDENTICAL against current
