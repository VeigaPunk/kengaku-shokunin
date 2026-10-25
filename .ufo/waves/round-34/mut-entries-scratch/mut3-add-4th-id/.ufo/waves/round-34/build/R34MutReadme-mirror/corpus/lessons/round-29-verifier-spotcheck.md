author: hyaku closure (non-author integrator, @m_flash)
round: kengaku 29 (attempt 2, hyaku run 6)
date: 2026-10-25
scope: non-author verification of `.ufo/reports/round-29/kengaku.md`; no lane-authored file was edited

# Round 29 — non-author verifier spot-check

I did not author this round. Baseline `1f3b0f1ec41ec297130e8944ff97968d32324632`; lane tip
`2ff4b6f864fe852a6268055f684ae5b6e3428b09`. Every number below is a command I ran myself over
committed bytes; no lane gate or selftest was executed (PROTOCOL §Gate standard, Closure
consequence — a sibling's gate is evidence-verified, never run by the integrator).

## 1. Step-1 conformance

| item | result |
|---|---|
| report committed by the lane identity | **pass** — `git log --format='%an %ae %H' -- .ufo/reports/round-29/kengaku.md` → `kengaku-shokunin kengaku@shokunin.local`, head `d4090261` (three report commits: `1c83bc10`, `da034dc2`, `d4090261`) |
| `SHONEN` heading, one line per box | **pass** — `SHONEN.md` has 4 boxes (`grep -cE '^- \[' SHONEN.md` → 4); the report's §SHONEN has 4 lines, each `[~]` with a resolvable pointer |
| every cited lane commit exists and is an ancestor of the branch | **pass** — 14/14 hashes (`8c14a5d…`, `8cf7b60…`, `ff476d0…`, `4b82ff7…`, `7bc2aaf…`, `c88310f…`, `5fd54a4…`, `30ee3b5…`, `8a25d9e…`, `1515617…`, `9df6226…`, `96c9d8f…`, `2ff4b6f…`, `1f3b0f1…`) → `git cat-file -e` OK and `git merge-base --is-ancestor <h> master` OK |
| pushed, no uncommitted round work | **partial** — `jj-lane.sh state …` → `local=remote=2ff4b6f… ahead=0 behind=0`; but `git status --porcelain` → ` M .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md` (+22 lines, mtime 04:05, a critic-seat addendum appended after the final commit). Uncommitted wave evidence only; no production byte |
| prompt carries the template contract | **pass** — `.ufo/prompts/kengaku-round-29.md` headings `## 1. MISSION / AXES binding` … `## 5. Commit, push scope` match `templates/round-prompt.md` 1:1, plus `## 6. Campaign addendum — hyaku` |
| marker test | **not a marker** — the report names committed work, evidence pointers and all required sections |

Report defects named above are status-neutral; none of them makes the report a marker.

## 2. Claim re-checks

### C1 — shokuknow assimilation (coverage), declared `entries 0 → 1`

| measurement (mine) | before `1f3b0f1` | after `2ff4b6f` | report says |
|---|---|---|---|
| knowledge entry present | `git cat-file -e 1f3b0f1:corpus/knowledge/benchmark-task-validity-checklist.md` → absent | present, frontmatter carries 5 `source:` lines (S077–S080, S090) | entry built and landed |
| registry rows | `git show 1f3b0f1:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` → **76** | same → **82** | 76 → 82 |
| knowledge files | `git ls-tree -r --name-only <rev> corpus/knowledge \| wc -l` → **37** | → **38** | 37 → 38 |
| knowledge index rows | `git show 1f3b0f1:corpus/README.md \| grep -cE '^\| \`knowledge/'` → **37** | → **38** | 37 → 38 |
| the six new rows' cells | n/a (ids absent) | S077/S078/S090 → `status=mined opened=2026-10-25 recheck=180d used-by=corpus/knowledge/benchmark-task-validity-checklist.md`; same shape for S079, S080; S091 `used-by` lists the lesson plus the entry | mined, use-by projected |
| no existing row touched | `git diff --numstat 1f3b0f1 2ff4b6f -- corpus/SOURCES.md` → `7 0` (seven insertions, zero deletions) | | "no existing row changed" |
| fleet census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → 14 `W04` + `ok`, **exit 0** | matches `census-after.txt` (15 lines) | exit 0, 14 W04 |

The frozen counter's own line is **evidence-verified, not executed**: `corpus/evidence/round29-attempt2/adoption-measured.txt`
→ `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok`. The
do-nothing control line the report quotes (`entries=0 … census=skipped`, exit 1) is **not** at the
cited `corpus/evidence/round29-attempt2/control-nothing.txt` — that path does not exist. The bytes do
exist, committed, at `.ufo/waves/round-29/attempt2/control.nothing.txt` (plus `verified_at=0`), and
reproduce the quoted values; the frozen expectation file `adoption-expect.json` exists with keys
`access_date/attempt/entries/round`. Value verified, pointer wrong (see §5 D1).

### C2 — standing source-adoption gate (operability), capability acquisition

| measurement (mine) | before | after |
|---|---|---|
| tool present | `git cat-file -e 1f3b0f1:plans/sources_adopt.py` → **exit 128**; `plans/adoption_check.py` → **exit 128** | both present (478 + 134 lines at tip) |
| selftest tally (committed) | — | `corpus/evidence/round29-attempt2/gate-selftest.txt` → 10 `CASE … PASS` lines + `SELFTEST cases=10 failed=0` |
| strict real-package run (committed) | — | `gate-strict.txt` header → `registry=82 staged=173 collisions=6 malformed=2 duplicates=0 defects=167 prose=167`, collisions named `S077 … S091`; report says exit 3 on the declared map |
| targeted pre-append run (committed) | — | `gate-scoped.txt` header → `registry=76 staged=173 collisions=0 malformed=0 duplicates=0 defects=0 prose=5`, `attested:` line present, five-row block |
| post-append re-run (committed) | — | `.ufo/waves/round-29/attempt2/gate-postappend-rerun.txt` → `registry=81 … collisions=5`, which backs SCORECARD's `collisions=5` |
| capability row | absent | SCORECARD §Round 29 attempt 2 capabilities table carries `source-adoption-gate`, first-working round 29 |

Claim-term deviations disclosed by the lane and ruled on: (a) a prose `recheck` normalizes to `180d`
with `opened=2026-10-25` rather than the frozen access date — mechanism as frozen, value changed and
recorded; (b) clause 4 (global refusal) ships as strict-default-plus-`--scope-to-admit` — the
stronger global refusal is explicitly not claimed. Both are written into
`plans/round-29-attempt2-claims.md` §Scope clarification, which first appears in `8cf7b60` (absent
at freeze `8c14a5d`); "before any seat scored" is therefore **unprovable from bytes**, but the
deviation is disclosed rather than silently redefined, and no seat report scores the unscoped
variant. **Ruling: both claims verify as measured; the two deviations are disclosed scope
clarifications, not post-hoc target narrowing** (the targets — one entry, one gate — did not move).

### No-harm

`git diff 1f3b0f1 2ff4b6f -- SCORECARD.md` is **additive only** (a new §Round 29 attempt 2 section,
no prior row edited, no score lowered). `git diff --numstat 1f3b0f1 2ff4b6f | awk '$2>0'` → exactly
one deletion, `plans/round28_census.py` 1/1 (the row anchor widened to the census's own 0–3-space
form, which the strict-mode receipts re-derive). Nothing changed outside
`corpus/ plans/ .ufo/ LOG.md SCORECARD.md PROVINCE.md considerthese/`. The four no-harm re-runs
(grader 733/0 PASS, `round28_census.py` rows 82, `config_projection.py` findings 0, census exit 0)
are **evidence-verified** from `…/build/R29a2Regression.md` and
`corpus/evidence/round29-attempt2/round28-census-after.txt`; I did not execute the lane's gates.
Wave accounting re-derived: `build/*.md` = **36**, `residual/*.md` = **4**, `.ufo/waves/yield.tsv`
round-29 rows = **40** with **27** `yes` — matches the report.

## 3. Discernment spot-check (LEARNING.md, non-author sample)

| item | decision | re-opened source | agree / disagree | reason |
|---|---|---|---|---|
| S077 Terminal-Bench/Harbor task-review automation (adopt) | admit | `https://raw.githubusercontent.com/harbor-framework/terminal-bench/e67a2cb7db4d9795c212909b3395d8c22ad60aec/docs/TASK_REVIEW_AUTOMATION.md` fetched live 2026-10-25 | **agree** | HTTP 200, 41842 bytes, sha256 `b0a7cb1495a08a4429d957904dd724db08293627dfba040c2df7c09929278b61` = the lesson's `b0a7cb14…78b61`; line 95 carries the 15-word quote verbatim; lines 29/31 are the two pipeline rows the entry cites |
| S078 SWE-bench Pro V2 release notes (adopt) | admit | `https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766bba642462d4bbe5479e83f91f9211862/v2/README.md` fetched live | **agree** | HTTP 200, 6858 bytes, sha256 `dde4168fed17ca1ea00b26a93aca78dad43c7b3f981b93a2872428259428231f` = `dde4168f…8231f`; line 99 is `731 -> 642 tasks: 89 dropped after review.`; line 75 opens with the locked-sandbox sentence |
| S079 Terminal-Bench 2.0 task tree count (re-derived, `92 root = 89 dirs + 3 files`) | admit (entry's corrected count) | `git init` + `git fetch --depth 1 --filter=blob:none https://github.com/laude-institute/terminal-bench-2 2fd12b88…`, then `git ls-tree FETCH_HEAD` | **agree** | 92 entries, 89 `040000` trees, 3 blobs — the entry's corrected unit reproduces; the package's "92 task directories" is the wrong unit, as the round says |
| `judge-calibration-thresholds.md` (reject on premise) | reject | `corpus/QUALITY.md:82` (Q11 interval-gated pass bar), `corpus/knowledge/attribution-interval-calibration.md:10-14`, `corpus/knowledge/llm-judge-calibration.md:7-13`, `git grep -n 'kappa' corpus/knowledge` | **agree, one wording defect** | Q11 exists and is interval-gated; the attribution file holds the pre-registered PASS/FAIL/INDETERMINATE rule; the judge file already states the bias+uncertainty claim the candidate offers. The reject's measurement `grep -rn 'kappa' corpus/knowledge/*.md` → 0 hits reproduces, but the lesson renders it "0 hits **in the lane**", and a lane-wide `git grep -ni kappa` → **65 files** at tip (63 at baseline: round-12 Greek-letter token vocabulary and one round-26 wave report). D2 |
| S090 row's A-vs-B tier call (adopt, tier override) | admit at tier A | `SOURCES.md` S090 cells + the round's `R29a2RevQuoteS090.md` | **agree with the direction, unverified date** | the row is `mined | 2026-10-25 | 180d` with a first-party maintainer statement; I did not re-fetch the publisher index that dates the post 2025-11-07, so the "dated, therefore tier A" half rests on the seat's receipt alone |
| ≤25-word quote in a newly written `SOURCES.md` row | — | S077 row quote `"Prevents training data contamination by ensuring a unique canary string is present in task files."`; S078 row quote `"731 -> 642 tasks: 89 dropped after review."` | **agree** | both are byte substrings of the live fetches above (15 and 8 words, both ≤25); the lesson table prices the S078 line-75 quote at 9 words where the registry says 8 — the quote is exact, the count is off by one in the lesson (D3) |

## 4. Axis verdicts

| axis | verdict | basis |
|---|---|---|
| coverage | **improved** | measured 0 → 1 admitted entry and 0 → 5 cited/registered rows on frontier ground the lane did not hold; the canonical score stays 7 because the round-25 L0 cap is untouched, which the report states |
| operability | **improved** | capability row added; gate + counter are absent at baseline (exit 128) and present, demonstrated on the real package in both modes, with 10/10 selftest and two declared-exit receipts committed |
| depth | unchanged | no new depth claim; SCORECARD's 9 untouched, and the diff is additive |
| novelty | unchanged | prior art priced (S091, ABC), INCREMENTAL, no novelty credit taken — the honest outcome, verified by row S091 existing with that `used-by` |
| freshness | unchanged | census exit 0 at both ends with the same 14 W04; no row's recheck moved on an existing source |
| adjacency | unchanged | three staged entries rejected on named properties with flip conditions; no sibling-lane surface touched |
| calibration | unchanged | two disclosed corrections (M92 fixture conflation, M94 count unit) plus three calibration repairs in `96c9d8fd`; the round does not claim a calibration move |

No axis is harmed: the only deletion in the round diff is the census anchor widening, and the
SCORECARD diff is additive.

## 5. Trend verdicts and routed defects

- **expansion: improved** — entry + 6 rows + a new coverage-map bullet + the `primary specs` half of
  frontier bullet 1 discharged (`corpus/README.md` diff, 12 insertions).
- **quality: improved** — a ten-case gate with four killed mutants and three closed gaming paths,
  eight self-found defects repaired in-round, and receipts that reproduce byte-for-byte under my own
  commands; bounded, and the gate still has no quote/word validation.
- **discernment: improved** — the outside sample above agrees on three admits, one tree count and one
  reject's premise; the only disagreements are wording (D2, D3), not fabricated evidence.

Routed defects the lane must fix next round (all status-neutral; none harms an axis):

- **D1** `.ufo/reports/round-29/kengaku.md` cites
  `corpus/evidence/round29-attempt2/control-nothing.txt` twice; no such path is committed. The bytes
  are at `.ufo/waves/round-29/attempt2/control.nothing.txt` (which also carries `verified_at=0`, a
  field the report's quoted line omits). Commit the receipt under the cited name or cite the wave
  path.
- **D2** `corpus/lessons/round-29.md` §Rejected candidates renders the kappa sweep as "0 hits **in
  the lane**"; the scan's own command is `corpus/knowledge/*.md`, and a lane-wide grep finds 65
  files. Narrow the sentence to the scope the command measured.
- **D3** §Sources opened this round prices S078's line-75 quote at 9 words; the row and the registry
  say 8, and 8 is correct. Correct the table cell.
- **D4** ` M .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md` (+22-line critic addendum) is
  uncommitted round evidence in the lane worktree; commit it as wave evidence or record why it is
  advisory-only.
- **D5** S091 is `used-by` the entry in `SOURCES.md`, but the entry's `source:` block does not cite
  it, so the frozen counter cannot see the relation the registry asserts. Either cite it in the
  entry's prior-art section as a source, or record the asymmetry in `adoption-expect.json`.

Promotion stays operator-owned: the four `SHONEN.md` boxes are now checkable by a non-author
(§1 has the pointers), so this round reports them `[~]` rather than `[x]` — which is the correct
lane-side posture and needs no change from the lane.
