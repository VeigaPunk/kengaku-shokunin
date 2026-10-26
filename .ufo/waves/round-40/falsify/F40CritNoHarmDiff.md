# F40CritNoHarmDiff — removed/rewritten doc lines at the r40 landing (kengaku r40 wave 2)

Seat: critic. Target: `git -C <lane> diff d3a6277f ec1005a2a28bc5cfdde7723374368ed4cc956eed -- SCORECARD.md LOG.md SKILL.md PROVINCE.md SHONEN.md corpus/`.
Attacks: the "no harm / append-only" claim for the L1 landing.

Scratch clone (fixture rule): `/fast/scratch/hyaku/kengaku-r40/F40CritNoHarmDiff/lane`, `git -C "$S/lane" rev-parse --show-toplevel` →
`/fast/scratch/hyaku/kengaku-r40/F40CritNoHarmDiff/lane`, HEAD `ec1005a2a28bc5cfdde7723374368ed4cc956eed`.
Lineage check: `git merge-base --is-ancestor d3a6277f ec1005a2… && echo ANCESTOR=yes` → `ANCESTOR=yes` (real ancestor; not a tree-vs-tree compare).
Lane tip has since advanced to `c9c793ca` (`round-40: wave-2 spec and dispatch (35 seats, policy v1)`); all numbers below are measured at `ec1005a2` as instructed.

## 1. Inventory — every removed / rewritten line in the scoped paths

`git -C "$S/lane" diff --numstat … | awk '{a+=$1;d+=$2} END{print "TOTAL_ADD="a" TOTAL_DEL="d}'` → `TOTAL_ADD=1099 TOTAL_DEL=2`.
So the whole scoped landing removes exactly **two** lines. Both are in `corpus/SOURCES.md`:

| # | file:line (landed) | what it was | what it became |
|---|---|---|---|
| 1 | corpus/SOURCES.md:68 (S046) | anchor cell ended `… special sequence backslash-s; opened 2026-10-21` | same text + `; rechecked 2026-10-26 on Python 3.15.2 docs (R40SourcesRecheck)` |
| 2 | corpus/SOURCES.md:74 (S052) | anchor cell `Python 3.15.0 documentation, JSONDecoder.raw_decode` | same text + `; rechecked 2026-10-26 on Python 3.15.2 docs (R40SourcesRecheck)` |

Per-file `git diff --numstat` (deletions only; every other scoped file is 0-del):

```
0 del  105 add  corpus/evidence/round40/tb2-db-wal-recovery/solve.sh
0 del   36 add  LOG.md           0 del   50 add  SCORECARD.md
0 del   51 add  PROVINCE.md      0 del   99 add  SKILL.md
0 del   89 add  corpus/lessons/round-40.md      0 del  357 add  corpus/knowledge/tb2-db-wal-recovery-grader.md
2 del    5 add  corpus/SOURCES.md
```

`SHONEN.md`: `git diff --stat … -- SHONEN.md` printed nothing → untouched, no removal to judge.
`git diff --name-status --diff-filter=DR …` printed nothing → no scoped file was deleted or renamed.

## 2. Judgment on the two rewrites — is either a harm?

**Field-level isolation.** Splitting both rows on `|` before and after
(`git show d3a6277f:corpus/SOURCES.md` vs `…ec1005a2…:corpus/SOURCES.md`, `python3 …` field loop) →
`fields 13 13` / `col6 CHANGED` only, on both rows. Header is
`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` (SOURCES.md:21), so col6 is **anchor**:
id, source URL, kind `docs`, tier `A`, scope, `teaches`, `status=mined`, `opened=2026-10-21`, `recheck=on-release` and `used-by` are byte-identical.
No identity, tier, status, cadence or used-by change → the authority of both rows is untouched.

**False-provenance test (strongest counterexample I had).** The note asserts a *"Python 3.15.2"* docs version on 2026-10-26; the
local interpreter index offers only 3.15.0 (`uv python list` → `cpython-3.15.0-linux-x86_64-gnu <download available>`), and 3.15.2
looked impossible this soon after 3.15.0. Refuted by independent re-fetch today:

```
curl -sSL https://docs.python.org/3/library/re.html   → HTTP=200 SIZE=257706
  <title>re — Regular expression operations &#8212; Python 3.15.2 documentation</title>
  sha256 a99c3e85983a8aba2073827e0e34ee3b0925ddd57b4251584da7a8e9a46877cd
curl -sSL https://docs.python.org/3/library/json.html → HTTP=200 SIZE=116112
  <title>json — JSON encoder and decoder &#8212; Python 3.15.2 documentation</title>
  sha256 1af0ba1d859bb4134d23b26446bb53735d0b48769a6947d36958ff1937aec8b7
```

Both digests and byte counts reproduce **exactly** the values the wave-1 seat recorded
(`build/R40SourcesRecheck.md`: `a99c3e85983a8aba…` 257,706 B and `1af0ba1d859bb413…` 116,112 B). The claim is true and reproducible;
not fabricated. The S046 anchor's own quote also still holds live: `grep -o 'Matches Unicode whitespace characters[^<]*' re.html`
→ `Matches Unicode whitespace characters (as defined by …` (the `\r` sentence is the continuation).

**R1 ("corrections are appended, never rewritten", QUALITY.md:161) — the one contestable point.**
R1's letter says "the old line stays byte-identical"; these two lines were edited in place (git sees delete+add). R1's *executable
check* is value-based, and it passes:

```
grep -c 'Python 3.15.0 docs, Regular expression syntax, special sequence backslash-s; opened 2026-10-21' corpus/SOURCES.md → 1
grep -c 'Python 3.15.0 documentation, JSONDecoder.raw_decode'                                          corpus/SOURCES.md → 1
grep -c 'rechecked 2026-10-26 on Python 3.15.2 docs (R40SourcesRecheck)'                              corpus/SOURCES.md → 2
```

The superseded anchor text survives verbatim as a prefix of the new cell, so nothing was lost, and R1's subject ("a corrected
*count or verdict*") is not in play: no count and no verdict changed (status `mined`, `recheck on-release`, tier `A` all identical).
Judgment: **not a harm** — and appending inside the anchor cell is the round-37-sanctioned shape, since Q26 keeps the anchor cell as
"the bytes I read" and round-37 preferred appended notes over row rewrites (QUALITY.md:381-399).

**Contract checks still green after the rewrite** (both run in the scratch clone under bwrap):
`python3 plans/anchor_digest_check.py --lane .` → `rows=114 tokens=21 defects=0`, `EXIT=0` (Q26 unaffected: no sha256 token added or
moved). `bash scripts/sources-census.sh validate --root <fleet> kengaku` → `kengaku ok …/corpus/SOURCES.md`; the only `W04` lines name
`S067 S068 S069 S071 S075 S076 S100` — pre-existing duplicate-URL warnings, none on S046/S052/S119-121.

**Smallest safe correction (precision, not a harm):** the landed note records *that* a recheck happened, not its *outcome*. Wave-1's
draft was `… rechecked 2026-10-26 against Python 3.15.2 docs, same text`; the landed text dropped `same text`. Appending `, same text`
would make each dated entry self-describing, which is what R1 asks of an appended record. Optional; nothing depends on it today.

## 3. SOURCES.md — appends plus exactly the two anchor notes

`git diff … -- corpus/SOURCES.md | grep -c '^@@'` → `2` hunks only:

```
@@ -65,13 +65,13 @@   ← the two S046/S052 anchor rewrites (2-/2+)
@@ -131,6 +131,9 @@   ← 3 appended registry rows (+3, 0-)
```

Arithmetic closes: `5 insertions = 2 rewrites + 3 new rows`, `2 deletions = the two superseded anchor cells`. Nothing else in the file changed.

The three appends sit at the registry end, immediately after `S118` and before `## Paths` (SOURCES.md:134-136), and are well-formed:

```
awk -F'|' '{print "fields="NF" id="$2" tier="$5" status="$9" recheck="$11}'
fields=13  id= S119  tier= A  status= mined  recheck= 180d
fields=13  id= S120  tier= A  status= mined  recheck= 180d
fields=13  id= S121  tier= B  status= mined  recheck= 90d
```

`grep -oE '^\| S[0-9]{3} ' … | sort | uniq -d` → empty (no duplicate ids); row count `111 → 114` (+3).
Tiers/status are in-contract (`community` never tier A: S121 is `docs`/`B`).

Byte-provenance of the appends — capture files match both the rows and upstream at the pinned commit:

```
sha256sum corpus/evidence/round40/tb2-db-wal-recovery/{test_outputs.py,instruction.md}
  88dc5c2a3abba75bca0e0f9136223ae5bb585d5984b8d9eba51a7829c1d2ba49  test_outputs.py
  5a20375162921b8911c67035d1905df7fd335d1bed03044271e608b2c3c93b26  instruction.md
raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88…/db-wal-recovery/<same files> → HTTP=200, same two digests
```

`SHA256SUMS` lists all eight captured files with digests consistent with the two spot-checked ones (`main.db 68cb288e…`,
`main.db-wal.encrypted 68753bdc…`, `solve.sh ed8530c9…`, `task.toml 1cdc2c61…`, `test.sh 4770437e…`, `Dockerfile 63a26053…`).
So the appends are genuine captures, not forged fixtures.

Cross-reference accuracy: `corpus/lessons/round-40.md:32` describes the landed shape correctly — "the anchor ended at the 3.15.0 docs
reference → the same text plus that note". (It says "the same text", i.e. the outcome the anchor cell itself no longer spells out.)

## 4. Residuals (not caused by these two lines; named so the close is not overclaimed)

1. **Three Python-docs versions now coexist in the registry.** S046/S052 pins still say `3.15.0`, the new notes say `3.15.2`, and
   `S065` anchor reads `Python3.15.1, Infinite and NaN Number Values paragraph and examples; opened2026-10-21` (SOURCES.md, verified by
   `awk -F'|' '{print "ANCHOR="$7}'`) while the live page is 3.15.2. Wave-1 flagged S065 as optional and L1 skipped it. No check reads it.
2. **`on-release` rechecks are unenforceable.** `scripts/sources-census.sh` (header: "`recheck` carries cadence") prints symbolic
   cadences as `cadence`, never `overdue`; a release-triggered recheck therefore lives only in prose. Pre-existing design, not introduced here.
3. Out of scope for this item, flagged for its owner: `plans/tip_receipts.py` is the only other file with deletions in the round range
   (`44 add / 8 del` over the same base — docstring and RECEIPTS-map refactor). Doc-scope verdict below excludes it.

## 5. Impacted axes

- freshness — *improved*: two drift-risk rows now carry a dated, seat-tagged recheck that independently reproduces.
- calibration — *unchanged/no harm*: provenance string verified true; no tier/status/verdict drift.
- coverage — *improved*: +3 registry rows (S119-S121) with byte-verified captures.
- operability — *unchanged*: `anchor_digest_check` `defects=0`, census `validate … ok`.
- depth, adjacency — untouched by these two lines.

## 6. Verdict

Two removed lines, both the same surgical change (anchor-cell suffix) on two rows whose other twelve fields are byte-identical; the
claim each appends is independently reproducible today; the R1 executable check still returns 1/1/2; the file's other 5 insertions are
pure appends with byte-verified captures. No regressions, no duplicate authority, no identity change, no false provenance found in
the scoped diff.

VERDICT: removed-lines-2-harms-0
