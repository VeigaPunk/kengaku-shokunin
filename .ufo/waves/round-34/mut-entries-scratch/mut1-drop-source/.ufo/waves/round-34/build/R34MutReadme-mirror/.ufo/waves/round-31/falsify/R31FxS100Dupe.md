# R31FxS100Dupe — attack on the S100↔S079 duplicate-URL disposition

Seat: `L1Kengaku31.R31FxS100Dupe` (critic, leaf) — round 31 wave 2 falsify, lane
`kengaku-shokunin`, landing commit `dbb07364`, baseline `0883e72`.
Read-only; scratch under `/tmp/r31fx-s100dupe/` (8 KB). No tools installed.

## What was attacked

The landed row S100 (`corpus/SOURCES.md:113`) cites the same repository at the same
pinned commit as the pre-existing row S079 (`corpus/SOURCES.md:101`):
`https://github.com/laude-institute/terminal-bench-2` @ `2fd12b88aafdd04a52c298e3940bcb189f9766d6`.
The fleet census flags `S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes`
as the 15th `W04`. Question set: are the scopes genuinely different; is the census
classification a warning or an error; does CORPUS.md rule 2 demand a `supersedes`
row instead; what must the report disclose so a reader is not misled about a 91-row
registry with 15 duplicate warnings.

## Evidence

### 1. The two rows

- S079 (`SOURCES.md:101`): kind `spec`, scope "the authored fields of a Terminal-Bench
  2.0 task package at a pinned commit — schema version, difficulty category, human
  expert and junior time baselines, verifier timeout — read from the task tree itself";
  teaches = task-package field semantics for validity audits; used-by
  `corpus/knowledge/benchmark-task-validity-checklist.md`. Anchor already contains the
  root-count fact: "92 root entries at that commit, of which 89 are task directories
  carrying a task.toml (re-derived 2026-10-25)".
- S100 (`SOURCES.md:113`): kind `dataset`, scope "the Terminal-Bench 2.0 task tree at a
  pinned commit — its top-level entry count (release identity) and its per-task
  manifests and test scripts as read for verifier execution, not for task-package
  schema (that is S079, the same repository read for its authored fields)"; teaches =
  tree identity/count and rename/tag provenance; used-by
  `corpus/knowledge/benchmark-verifier-execution-model.md`.

**Are the scopes genuinely different?** Yes — in the contract's own sense (scope = "the
claim or topic the tier applies to", `CORPUS.md:98`). The two rows teach different
claims over one document at one pin: S079 is about authored field semantics inside
per-task `task.toml` files; S100 is about the whole-tree fan-out, the alias/redirect,
the absence of tags, and the README dataset line. They feed different knowledge
entries. S100 explicitly bounds its scope away from S079's ("not for task-package
schema (that is S079…)"), so the distinction is disclosed in-cell.

**Overlap that weakens the distinction:** S079's *anchor* already carries the same
count fact S100 teaches (92 root entries / 89 task dirs). The central number is not a
new S100 contribution; it was re-derived for S079 the same day
(2026-10-25). S100 adds the 301-alias, the zero-tags fact, and the README:46 dataset
line — those are the genuinely new bytes. So the pair is "one new claim + one shared
fact", not two cleanly disjoint scopes.

### 2. Census classification: warning, not error

- `W04` emit rule (`scripts/sources-census.sh:644-645`): fires when a URL was seen in
  an earlier row and this exact URL+scope-string pair is new.
- `E04` (error) rule (`:646-649`): fires only when the URL **and the scope string are
  identical**, both rows are non-rejected, and `teaches` carries no `supersedes S###`
  marker. S100/S079 scope strings differ, so no E04.
- Header comment (`:33`): "W04 same URL across scopes (**warnings do not affect clean
  lanes**)". Selftest `W04-does-not-fail-validation` asserts exit 0 (`:361-364`).
- Observed run (re-run this seat):
  `sh scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`
  → 15 `W04` lines, last one `kengaku W04 S100 duplicate url
  github.com/laude-institute/terminal-bench-2 across scopes`, then `kengaku ok …`,
  **exit 0**. So the disposition is a warning; the round stays clean.

### 3. CORPUS.md rule 2: no supersedes row is required

Rule 2 (`CORPUS.md:116-118`): "Only `status`, `recheck` and `used-by` change in place …
A correction is a new row whose `teaches` opens `supersedes S0NN —`."

- S100 does not correct S079: it asserts no error in S079 and keeps S079 accurate for
  its own scope. The supersedes mechanism is for corrections; forcing one here would
  falsely imply S079 was wrong.
- Append-only actually **forces** the new-row route: expanding S079's scope in place is
  prohibited (scope is not a mutable cell), so the only compliant way to land the new
  claim was a new row — which is what wave 1 did (`git diff 0883e72 dbb07364 -- corpus/SOURCES.md`
  shows exactly +3 rows, S092/S093/S100, zero in-place edits).
- Precedent for live (non-supersedes) same-URL pairs already exists in the registry:
  S044↔S057 (arXiv 2405.11874), S053↔S059 (RFC 8259), S052↔S065↔S071 (Python json docs)
  are all mined, non-supersedes second reads. S100/S079 is not a new species.
- So: rule 2 does **not** require a supersedes row. It does require that the second row
  be a *claim*, not a re-teach — and the count clause of S100 is partly a re-teach of
  S079's anchor (see §1), which the row should cross-reference rather than repeat.

### 4. What the 91-row / 15-warning picture hides

Re-derived from `corpus/SOURCES.md` with the census's own URL normalization
(`url_of`, `:600-605`):

- 91 rows = 85 URL-bearing rows + 6 own-work rows without URLs.
- 32 rows sit in **14 repeated normalized-URL groups** (2× terminal-bench-2, 2× ACL
  2020, 2× RFC8259, 2× xFinder, 3× Reiczigel, 2× WebArena raw, 2× JAMA, 2× Scale,
  2× WebArena evaluators, 2× CommonMark, 5× Python json docs, 2× inspect_ai pattern,
  2× PPI, 2× Lang&Reiczigel) → distinct URL identities ≈ **73**, not 91.
- The W04 count is an **occurrence** count (second-or-later row per URL), not a pair
  count and not a defect count. Of the 15 W04, 10 are members of rule-2 supersedes
  chains (S040/S048/S058/S064/S066/S067/S068/S069/S075/S076) and only 5 are live
  second reads (S057, S059, S065, S071, S100).
- The census's normalization **misses** same-source reuse when the URL string changes
  host: S078 (`raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766…/v2/README.md`)
  and S093 (`github.com/scaleapi/SWE-bench_Pro-os`, same pin 66f92766) are the same
  repository read at the same commit, yet no W04 fires. Own-work path aliases are also
  invisible: S025↔S036 share `corpus/evidence/attrib-r23-stream.log`, S037↔S047 share
  `plans/attrib_calibration.py`. So "15 duplicate warnings" **understates** same-source
  reuse (≈17 aliased pairs total).
- Therefore a reader told "91 rows, 15 W04" cannot infer 91 distinct sources, nor 15
  defects. The landing discloses the S100 pair specifically (`LOG.md:912`, `SCORECARD.md:1062`,
  `corpus/lessons/round-31.md:117-121`), but nowhere is the effective distinct-source
  count stated.

### 5. Count reproducibility (independent)

This seat re-fetched the pinned root via `gh api "repos/laude-institute/terminal-bench-2/contents/?ref=2fd12b88…"`
→ `{entries: 92, dirs: 89, files: 3, names: [.gitignore, LICENSE, README.md, 89 task dirs]}`;
first entry URL resolves to `harbor-framework/terminal-bench-2` (the alias target) at the
same ref. Matches S100's anchor and the committed scout receipt (`R31SrcS100a.md:35-73`,
which additionally bound the ETag to the commit's tree sha `ec7c02c7…`, confirming the
listing is the pinned commit's tree, not a branch tip). The count claim is true.

### 6. The open question the landing left un-adjudicated

`R31SrcS100a.md:148-152` (wave-1 seat) explicitly flagged: "S100 and S079 are the same
document at the same pin … C1's predicate needs 'three distinct' ids, which the ids are —
but a reviewer should decide whether a second row over one document at one commit is an
admissible distinct source or a split row." The landing (LOG/SCORECARD/lesson) asserts
the warning is disclosed but never answers the question. My adjudication: admissible as
a distinct claim (rule 2 does not bar it; precedent exists), provided the shared count
fact is cross-referenced and the effective distinct-source count is stated.

## Findings

1. Scopes genuinely differ as claims (task-package schema vs release identity/verifier-
   execution tree reading), with one shared fact (the 92/89 root count) present in both
   rows' anchors.
2. Census classifies the disposition as **W04, a warning**: exit 0, clean lane; E04
   (error) does not apply because the scope strings differ.
3. CORPUS.md rule 2 does **not** require a supersedes row: S100 is not a correction, and
   append-only leaves a new row as the only compliant route. A supersedes row would be
   the wrong mechanism.
4. Disclosure needed and currently missing: 91 rows ≈ 73 distinct URL identities
   (≈71 counting own-work aliases); 15 W04 are occurrences, not defects (10/15 are
   supersedes-chain members); the census misses the S078↔S093 same-repo-same-pin pair
   and the S025↔S036 / S037↔S047 own-work aliases, so the warning count understates
   same-source reuse.

## VERDICT

SURVIVED: the S100↔S079 pair is a legitimate distinct-claim second read (warning, exit 0;
no rule-2 supersedes obligation; count reproducible at the pin; disclosure present in the
row's scope cell, LOG.md:912, SCORECARD.md:1062 and lesson round-31.md:117-121; C1's
frozen predicate — `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3
usedby_ok=1 census=ok`, exit 0 — is unaffected and still holds).

FELL: (a) the "91-row registry" is presented without an effective distinct-source count
(≈71-73), so "91 rows" misleads a reader into inferring 91 unique sources; (b) "15
duplicate warnings" is an occurrence count, not a defect count, and it understates same-
source reuse (S078↔S093 invisible to W04 due to host normalization; S025↔S036 and
S037↔S047 invisible own-work aliases); (c) the shared 92/89 count fact is re-taught in
S100 instead of cross-referenced to S079; (d) S100's scope cell ("per-task manifests and
test scripts as read for verifier execution") overstates the row's own evidence — the
row's anchor carries no per-task test-script bytes; those reads live in wave seats
`R31DraftEntry` / `R31SrcS100b`.

## Smallest safe correction

1. `corpus/SOURCES.md:113` (S100): keep the row; replace the duplicated root-count
   recount with a cross-reference — "top-level entry count as re-derived in S079; the
   new facts here are the 301 alias, zero git tags and README:46" — and add to the
   teaches: "same repository, same pin as S079; distinct claim, not a correction, so no
   supersedes row under rule 2".
2. Round report / `SCORECARD.md`: append the effective distinct-source figure (91 rows →
   ≈73 URL identities, ≈71 including own-work aliases) and name the census normalization
   blind spots (raw.githubusercontent.com↔github.com; own-work path aliases), so a
   reader of the 15-W04 line is not misled.
3. No code change to `sources-census.sh`: W04's warning semantics are correct; the gap
   is reporting, not the detector.

## Commands run (all read-only)

- `sh scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → exit 0, 15 W04.
- `python3 plans/adoption_check.py --expect .ufo/waves/round-31/adoption-expect.json --census` → `entries=1 … census=ok`, exit 0.
- `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 91.
- awk (url_of clone) over `corpus/SOURCES.md` → 14 groups / 32 rows / ≈73 identities.
- `git diff 0883e72 dbb07364 -- corpus/SOURCES.md` → +3 rows only, no in-place edits.
- `gh api "repos/laude-institute/terminal-bench-2/contents/?ref=2fd12b88…"` → 92 entries / 89 dirs / 3 files, alias to harbor-framework confirmed.
- `python3 plans/registry_check.py --summary` → `mismatch_sources=0 finding_count=0 exit=0`.

Report: .ufo/waves/round-31/falsify/R31FxS100Dupe.md
