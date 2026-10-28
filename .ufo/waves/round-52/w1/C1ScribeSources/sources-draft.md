# round-52 SOURCES draft — three candidate rows (seat C1ScribeSources)

Status: DRAFT. The L1 is the only integration owner; nothing here is applied to
`kengaku-shokunin/corpus/SOURCES.md`.

Base registry state, measured 2026-10-28 before drafting (command in the wave report):

- 171 rows, `tier.A=147 tier.B=22 tier.C=2`, `status.mined=155 queued=8 rejected=8`
- last id in use `S178`; unused gaps `S87–S89`, `S95–S96`, `S98–S99` (never reused)
- next unused id = **S179**

Column note: contract v1's registry table has **11 logical columns**
(`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`).
The census parser counts **NF=13** because splitting `| a | b | … |` on `|` yields two empty edge
fields. The seat brief's "13 columns" therefore means NF=13 / 11 logical cells — a row written as
13 logical columns would be NF=15 and fail `E01`.

---

## Candidate A — id `S179` (the grader-file population at the pin)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S179 | Terminal-Bench 2.0 grader-file population at the pinned tree (184 capture files over 89 tasks) — https://github.com/harbor-framework/terminal-bench-2 | code | A | the grader-file population of the Terminal-Bench 2.0 tree at a pinned commit — which files the round-52 C1 audit must capture, how many of each kind, and the task directories they hang from; not the task-package schema (S079) and not verifier execution (S100) | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, one recursive tree API call for that ref (document `sha` 2fd12b88…, `"truncated": false`, 1446 entries): 92 top-level entries = 89 task directories plus .gitignore, LICENSE, README.md; 94 test_outputs.py (89 under `<task>/tests/`, 5 also under `<task>/environment/tests/`), 89 test.sh, 1 verify.sh = 184 capture files; fetched document sha256 b5d86dfe49ca75383d6e87d36e7fadcfd60d99bc5ae18c79fbc14d272278f362 (2026-10-28) | the grader population is 184 files over 89 tasks, not 89: every task carries `tests/test_outputs.py` and `tests/test.sh`, five also carry an `environment/tests/test_outputs.py`, and one task's shell verifier is `verify.sh`, so a capture that reads only `tests/test_outputs.py` sees 89 of 184 files | mined | 2026-10-28 | 180d | corpus/lessons/round-52.md |

Overlap disclosure (why this is not row inflation): S079 registers the same pin for the
**task-package schema** (`task.toml` fields) and S100 registers it for the **top-level entry count
and verifier execution**. Neither enumerates the grader-file population or its per-kind counts.
S179's scope is the population the C1 predicate's `CAPTURES expected=184` leg reads. S100's anchor
already records that `github.com/laude-institute/terminal-bench-2` 301-redirects to
`harbor-framework/terminal-bench-2`, which is why the same commit appears under two owner names;
S179 cites the canonical (redirect-target) name, so the census URL keys differ from S079/S100 and
no `W04`/`E04` fires.

## Candidate B — id `S180` (the raw `build-pmars/tests/test_outputs.py` capture)

**Verdict: do not create S180. Re-open S115 instead.** The row is drafted below only so the
disposition is auditable.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S180 | Terminal-Bench 2.0 build-pmars task grader, raw capture of tests/test_outputs.py at the pin — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/build-pmars/tests/test_outputs.py | code | A | the executed scoring predicate of this one TB2 task at a pinned commit, as captured byte-exact for the round-52 C1 population: four pytest functions over an installed binary's debugger and battle output, an ldd string scan and a one-level /app source tree | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, test_outputs.py:1-85 (2938 bytes), :82 `assert src_dir.exists(), "No src directory found"` (8 words); sha256 d9d2796ddc19cf8159670567e174ea377e2bce675bf3451d5951c045b01f4e85 (re-fetched 2026-10-28, byte-identical to S115's anchor) | the build-provenance test asserts only that a one-level `/app/pmars-*` directory holds a `src/` entry, so an empty source tree satisfies it — presence, not compilation | mined | 2026-10-28 | 180d | corpus/lessons/round-52.md |

Collision evidence (measured, not inferred):

- S115 (registry line 130) already carries this **exact URL**, kind `code`, tier A, status
  `mined`, used-by `corpus/knowledge/tb2-build-pmars-grader.md`, and the same anchor sha256
  `d9d2796ddc19cf8159670567e174ea377e2bce675bf3451d5951c045b01f4e85`.
- My independent fetch: 2938 bytes, 85 lines, sha256 `d9d2796d…`, and the pinned tree's blob entry
  for the same path reports `size: 2938`. Byte-identical to S115's row.
- `E04` (duplicate URL within scope) fires only when the new row's `scope` cell is **string-equal**
  to the earlier row's; a reworded scope yields `W04` (warning, exit 0) instead. So a new S180 would
  either fail the census (verbatim scope) or pass while registering the same bytes a second time
  (reworded scope). Both are wrong; the bytes did not change, so nothing can be superseded.
- `corpus/knowledge/tb2-build-pmars-grader.md` exists at the base tip, which also means
  `build-pmars` **cannot** be a `CONFIRMED new` task under R52-C1 leg 3 ("never read by this lane
  before this round"). The capture is still required for `CAPTURES present=184`; it is not a new
  finding.

Correct disposition: a re-open of S115 logged in the round lesson (`old → new`; expected
`unchanged` for all three mutable cells), or no registry change at all.

## Candidate C — id `S181` (prior-art primary, PLACEHOLDER SHAPE ONLY)

No URL, title, kind or anchor is known at draft time and none is invented here. `__PRIOR_ART_ROW__`
marks the seat that must fill the row. Claims leg 4 requires **≥3 distinct URLs**, so this shape
repeats as `S181`, `S182`, `S183`, … — one per fetched primary.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S181 | __PRIOR_ART_ROW__ — prior-art primary for one confirmed C1 finding: title, canonical URL and access date supplied by the scout seat; no URL is invented in this draft | __PRIOR_ART_KIND__ | A | the phenomenon the primary does or does not document, stated no wider than the fetched bytes | __PRIOR_ART_ANCHOR__ — section or page plus revision, and a ≤25-word quote that grounds the verdict cell | __PRIOR_ART_TEACHES__ — must state whether this finding is phenomenon-known (already documented here) or phenomenon-new (not documented in any fetched primary) | mined | 2026-10-28 | 180d | corpus/lessons/round-52.md |

Rules the filling seat must satisfy: `kind` from the v1 enum (`spec docs paper code tool dataset
talk book community own-work`); tier `A` only if the row is primary for its own scope (a paper or
official docs page usually is; a `community` page never is); `opened` = the ISO date the primary was
actually fetched; `recheck` an ISO date, `NNd`, or a symbolic cadence; no `|` inside any cell.

---

## Census column rules this draft could not satisfy as literally briefed

1. **"13 columns".** Written as 11 logical cells → `NF=13` (see the column note above). A literal
   13-cell row is `NF=15` and fails `E01`.
2. **Candidate B cannot be a new row without a false `supersedes`.** `E04` demands
   `teaches` opening `supersedes S### —` for a same-URL/same-scope re-registration; the bytes are
   identical, so the honest `teaches` cannot carry it, and `W04` (reworded scope) is only a
   warning — the parser has no "same URL and same digest, already mined" rule.
3. **`used-by` must name a path that exists when the census runs.** `E11` checks every non-`—`
   `used-by` path against disk for *all* statuses, not only `mined`. All three drafts therefore cite
   `corpus/lessons/round-52.md`, which the round contract already requires to exist (frontier steps
   2–3). If the L1 prefers the C1 knowledge entry as the citing artefact, that file must be on disk
   before the end-of-round census or the run exits 1.
