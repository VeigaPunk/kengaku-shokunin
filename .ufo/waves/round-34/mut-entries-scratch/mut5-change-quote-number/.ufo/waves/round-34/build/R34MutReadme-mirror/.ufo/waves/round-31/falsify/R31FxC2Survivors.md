# R31FxC2Survivors — the ten C2 survivors re-run against the CURRENT `plans/round31_defects.py`

Seat: UFO-FSD mutation tester (leaf). Falsify goal. Access date for every source read: **2026-10-25**.
No tool was installed or upgraded (system `git`/`python3` only). The lane repo was touched in no way
except writing this report; all git operations were read-only or inside the scratch clones.

## 0. What was tested, and the pinned bytes

The counter under test is the current `plans/round31_defects.py` bytes, snapshotted at 06:05:
`sha256 c06ddc1e01eb6c6bb8edfdd58cf0ee6c7239dac57314a4a4353db580a81afd04`
(copy at `/tmp/r31fx-C2Survivors/counter.current.py`; live lane file had the same hash at snapshot time).
This is neither the critic's v1 (`de5c7917…`) nor v2 (`2c320d58…`); `diff -u` against the critic's v2
shows the L1 tightened since: `append_only()` wired into R1/R2/R3/R10, `INVISIBLES` stripping in
`plain()`, the R6 lookbehind replaced by the unified optional-group regex, R8 made row-cell-only, and a
R9 length guard added.

**Pre-repair tree (base)** — `/tmp/r31fx-C2Survivors/trim-base`: `git clone --shared` of the lane,
HEAD at `dbb07364`, with the nine files the checks read overwritten by their `0883e72` bytes
(`git show 0883e72:<path>`), staged (`git add`) so git-diff semantics match a real checkout; the five
seat reports are therefore dirty-vs-HEAD exactly as in the receipt's before-tree (R9 red). The staged
package `…/merge/kengaku/knowledge/corpus/knowledge/benchmark-card-field-schema-2026-10-23.md`
(3 `source:` URLs) and `swarm-registry.json` (33 members, from `dbb07364`) are present.

Control on the base reproduces the frozen before-state: `checks=10 defects=10`, exit 1, all ten
`DEFECT` lines (messages differ from the v1 receipt on R6/R7 — the before/after pair still crosses
predicate revisions). Base file hashes (all equal the `0883e72` blobs): `LOG.md
efb6d16d…`, `round-30.md 291c90581b…`, entry `f51951d327f…`, `SOURCES.md dec033bf982c…`,
gate `1b582050fdb…`, `R30RevLesson.md 010944f1c30…`, `R30FxCoverageAxis.md be5cc396c42…`,
`R30FxEntryCompleteSet.md 4561030d0cac…`, `R30FxEntryQ4Q6.md 37f7fdd39e161…`.

## 1. Survivor/kill table — cheapest no-repair edit per item, current counter

Every row: apply the exact bytes below to a copy of the base, then run
`python3 /tmp/r31fx-C2Survivors/counter.current.py --lane <dir>` (output cached at
`/tmp/r31fx-C2Survivors/evidence/results.txt`; fixtures live at `/tmp/r31fx-C2Survivors/t-<route>`).
"GREEN" = that item's `DEFECT` line is absent (all other items stay red; count 10→9).

| Route | Exact edit (bytes) | Verdict | Counter line when killed |
|---|---|---|---|
| R1 append | `LOG.md` += `- Correction (2026-10-25, R31): the wording "two new fields, one new value set" above is\n  quoted here as written; the phrase "one field, and the rest is not a delta at all" is the\n  entry's own paraphrase, not a correction of this line.` | **SURVIVED** (numstat `3 0`, R1 green) | — |
| R1′ rewrite | prepend 4-line decoy quoting the superseded phrase twice, then rewrite `LOG.md:792-793` `two new\n  fields, one new value set` → `one field, and the rest is not a delta at all` | **KILLED** | `LOG.md deletes 2 lines against 0883e72…: append-only forbids rewriting` |
| R2 append | `round-30.md` += `### Erratum log (2026-10-25)\nNo erratum is required for Q6: the sentence above stands as written, and "one field, and the rest is not a delta at all" is the entry's later wording, not a correction of this lesson.` | **SURVIVED** (numstat `2 0`) | — |
| R3 append | `round-30.md` += `- Tier note (2026-10-25): the registry records S086 B; this lesson's Q2 tier set is unchanged.` | **SURVIVED** (numstat `1 0`) | — |
| R4 U+200B | entry line 126 `what each stated, not a reconciled truth.` → `what each stated, not a reconciled\u200b truth.` | **KILLED** | `carries the 'reconciled truth' sentence 2 times` (raw U+200B present, count 1; `plain()` strips Cf chars → still 2) |
| R4′ reword | entry line 126 `not a reconciled truth` → `not a reconciled account` | **SURVIVED** | — |
| R5 U+200B | entry line 138 2nd `(not "unknown")` → `(not "unknown\u200b")` | **KILLED** | `repeats 'populated (not "unknown")' 2 times` (same canonicalisation) |
| R5′ reword | entry line 138 2nd `(not "unknown")` → `(not "unknown" instead)` | **SURVIVED** | — |
| R6 append | entry += `See the mapping note: two of its three source rows are not in this lane's registry.` (entry `:41` bare assertion untouched) | **KILLED** | `the entry asserts all three staged source rows are unregistered; 2 are` (bare `:41` match is parsed first) |
| R6 reword+append | entry `:40-41` `its three source rows are not in this lane's registry` → `its three source rows are not present in this lane's registry` + same appended counted sentence | **SURVIVED** | — |
| R6′ comment+reword | `SOURCES.md` += `<!-- https://aclanthology.org/2026.gem-main.50.pdf -->`; entry `:41` `not in` → `not present in` | **KILLED** | `the entry states no staged-source count; the re-derived count is 2` |
| R7 four-valued | entry `:71` `tri-state` → `four-valued` (only occurrence), + `Its values are not new. The registry's card-level vocabulary is outside this entry's scope.` | **SURVIVED** | — |
| R8 comment | `SOURCES.md` += `<!-- CC0 -->` | **KILLED** | `the entry names a CC0 licence no registry row records` (comments are not row cells) |
| R8 row-cell | `SOURCES.md:23` S001 kind cell `paper` → `paper CC0` | **SURVIVED** | — |
| R9 revert | `git checkout 0883e72 -- <R30RevLesson, R30FxCoverageAxis, R30FxEntryCompleteSet, R30FxEntryQ4Q6>`; gate restored to `dbb07364` bytes (keeps `Pass 9`); commit all five | **SURVIVED** | — (four HEAD blobs byte-identical to `0883e72`: revs `19db7a0993/cb8a5bed49/ac328eb1ca/07cce4f9da`; gate `c554fdd6e3`; status clean) |
| R9′ stub | five committed 122-line stubs (`# seat report` / `Pass 9` / 120 × `padding line`) | **KILLED** | `HEAD:…R30DraftGate.md is shorter than at 0883e72 (122 < 199 lines): a revert is not the repair` (baseline lengths 199/1023/368/338/388) |
| R10 append | `round-30.md` += `- The round's report lists 33 falsify seats; the figure in the header above is unchanged.` | **SURVIVED** (numstat `1 0`) | — |
| R10′ rewrite | `round-30.md:3` `34 falsify` → `33 falsify` + append `Erratum: "34 falsify" corrected to 33 falsify (36 build, 33 falsify).` | **KILLED** | `corpus/lessons/round-30.md deletes 1 lines … append-only forbids rewriting` |

Post-edit hashes of every touched file are recorded in the fixture dirs (list in
`/tmp/r31fx-C2Survivors/evidence/` run output); base-vs-edit pairs differ for every row, so each edit
was applied and each response is the counter's byte-for-byte verdict on it.

## 2. What the current counter killed vs the critic's v2 table

Killed (were green under v2): R1′ rewrite, R4/R5 U+200B, R6 leave-:41-append, R6′ comment+reword,
R8 comment, R9′ stub, R10′ rewrite. Each corresponds one-to-one with a v2→current tightening in §0.
Surviving fakes remain on **all ten items**: R1/R2/R3/R10 (append+substring, no append-only prefix
test), R4′/R5′ (synonym duplicates survive canonicalisation), R6 (reword+append), R7 (vocabulary
rewrite), R8 (row-cell injection), R9 (the exact revert the kill rule forbids — the length guard
cannot see byte-identical blobs). So `defects=0` is still reachable on every item with no repair; the
literal control cannot distinguish the honest closure from the fakes, and R9's green is the forbidden
revert.

VERDICT: **All ten items R1–R10 survive as cheaply fakeable under the current counter
(`c06ddc1e…`): each still prints `""` without repairing its mismatch — R9 by the exact revert its kill
rule forbids (four of five seat blobs byte-identical to `0883e72`) — while the v2-era routes that died
are R1′/R4/R5 zwsp/R6 append/R6′/R8 comment/R9′ stub/R10′ rewrite. C2's closure is true but still
unverifiable from `defects=0`.**
