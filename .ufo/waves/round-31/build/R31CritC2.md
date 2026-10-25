# R31CritC2 — can `round31_defects.py` print `defects=0` without repairing anything?

Seat: UFO-FSD critic (leaf). No production edits: the only lane file written is this report. Fixtures live
in `/tmp/r31-R31CritC2/` (19 MB). Read-only sources: `plans/round-31-claims.md`,
`plans/round31_defects.py` (two revisions, below), `.ufo/waves/round-31/claims/defects-before.txt`,
`corpus/lessons/round-30.md`, `corpus/knowledge/contamination-transparency-card.md`, `corpus/SOURCES.md`,
`.ufo/waves/round-30/**`, `git show 0883e72:<path>`, and the read-only staged package under
`/home/vgpnk/Projects/shokuknow/merge/kengaku/`. No tool was installed or upgraded.

Access date for every source read here: **2026-10-25**.

## 0. What was judged, and the moving target

The counting command changed **while this seat was running**, so every result below is pinned to bytes:

| rev | sha256 | mtime | what I did with it |
|---|---|---|---|
| v1 | `de5c7917ec67c6d2d7fc9d04ae24a60bf3a5b2dfa32b0c3bff14d1e205f29f9c` | present 05:47–05:50 | read in full; receipt reproduction; first survivor sweep |
| v2 | `2c320d58dab609d7041318980354d0369cde437eef5ddf8a75012a0a7d4f3234` | 05:56:12 | re-ran **every** survivor; this is the table's verdict column |

`plans/round31_defects.py` was edited by another seat at 05:56:12 (R2 `flat()` on the tail, R6
document-key URL normalisation + a number parse, R7 word-ban + required sentences). My judgement of the
*frozen* artifact is the v1 column; my judgement of *what will print `defects=0`* is the v2 column. Both
are reported because a critic that only tests the version it was handed is testing a file that no longer
exists.

**Pre-repair tree used for every fixture** (`/tmp/r31-R31CritC2/base`): the four data files taken from
`git show 0883e72:` (they were clean at HEAD when the receipt reproduced) plus the five round-30 seat
reports at their pre-repair *worktree* bytes over a commit of their HEAD bytes, so R9 is red for the same
reason as the receipt. On that tree:

- v1 prints the ten `DEFECT` lines and `checks=10 defects=10`, exit 1 — **byte-identical to
  `.ufo/waves/round-31/claims/defects-before.txt`** (`diff` empty).
- v2 prints `checks=10 defects=10`, exit 1, but **two messages differ** (see §3.1).

## 1. Receipt verification (asked for explicitly)

```
$ python3 plans/round31_defects.py --lane .        # 05:50:56, live lane, v1 bytes
... ten DEFECT lines ...
checks=10 defects=10
EXIT=1
$ diff .ufo/waves/round-31/claims/defects-before.txt /tmp/r31-R31CritC2/live-today.txt
(no output — identical)
```

**The receipt reproduces today: `defects=10`, exit 1, ten lines, byte-for-byte.** Caveat that matters for
the after-run: the lane entry was repaired in the worktree at 05:51:57 (after this run), and the counter
itself was rewritten at 05:56:12. So the *before* half of C2's `10 → 0` pair was produced by different
counter bytes than the *after* half will be.

## 2. Survivor table — the cheapest edit that prints clean

Every row was executed against the v2 bytes (`2c320d58…`) on the pre-repair tree; "still red" rows are
shown because they mark where v2 actually tightened. Fixture directories are named.

| # | Check | Cheapest edit (exact bytes) | v1 | v2 | Underlying mismatch still present |
|---|---|---|---|---|---|
| R1 | log-delta-correction | append 3 lines (below) that contain the word `correction`, the superseded phrase, and the admitted phrase | green | **green** | `LOG.md:792-793` still reads `declared the delta (two new / fields, one new value set)` |
| R1′ | same, append-only violation | prepend a 4-line decoy quoting the superseded phrase twice, then rewrite `:792` in place to the admitted wording | green | **green** | the round-30 record itself is rewritten; the check never compares against a blob |
| R2 | lesson-q6-basis | append `### Erratum log` + one sentence beginning `No erratum is required for Q6:` | green | **green** | `round-30.md:66-67` still states the Q6 pass on `one field, one placement, one value set` |
| R3 | lesson-q2-tier-cell | append `- Tier note (2026-10-25): the registry records S086 B; this lesson's Q2 tier set is unchanged.` | green | **green** | `round-30.md:60-61` still lists `S085 B, S086 A` |
| R4 | entry-duplicated-sentence | insert U+200B before the space of the 2nd copy: `reconciled\u200b truth` | green | **green** | both copies remain; the line renders identically (`what each stated, not a reconciled truth.`) |
| R4′ | same, no invisible bytes | reword the 2nd copy: `not a reconciled account` | green | **green** | the redundancy remains in two adjacent lines |
| R5 | entry-falsifier-clause | insert U+200B inside the 2nd clause: `populated (not "unknown\u200b")` | green | **green** | `:138-139` still repeats the clause |
| R6 | entry-staged-source-count | leave `:41` (`three source rows are not in this lane's registry`) **and** append `See the mapping note: two of its three source rows are not in this lane's registry.` | red¹ | **green** | the false sentence at `:41` survives verbatim |
| R6′ | v1-only registry route | append `<!-- https://aclanthology.org/2026.gem-main.50.pdf -->` to `SOURCES.md` + insert one word at `:41` (`not in` → `not present in`) | green | red | `:41` still asserts three |
| R7 | entry-s2-only-field | `tri-state` → `four-valued` everywhere + append `Its values are not new. The registry's card-level vocabulary is outside this entry's scope.` | green² | **green (partial)** | `S2's four-valued integrity flag is the only new field` survives; the check no longer tests that phrase |
| R8 | entry-licence-adjective | append `<!-- CC0 -->` to `corpus/SOURCES.md` | green | **green** | `entry:139` still says `a decision rule the CC0 card cannot supply on its own`; no row records a CC0 licence |
| R9 | seat reports committed | `git checkout -- <four seats>` (revert to `0883e72`) and commit only `R30DraftGate.md` | green | **green** | the four seat reports lose their round-30 corrections — the exact revert the claim's kill rule forbids |
| R9′ | same, stub route | five 122-line stubs (`# seat report` / `Pass 9` / 120 × `padding line`) committed | green | **green** | the seat substance is deleted; `len(lines) < 100` is the only stub test |
| R10 | lesson-round-shape | append `- The round's report lists 33 falsify seats; the figure in the header above is unchanged.` | green | **green** | `round-30.md:3` still says `(36 build, 34 falsify)` |
| R10′ | same, rewrite route | rewrite `:3` to `33 falsify` + append `Erratum: "34 falsify" corrected to 33 falsify (36 build, 33 falsify).` | green | **green** | committed lesson bytes rewritten in place; no blob comparison |

¹ Under v1 R6 was **unsatisfiable** for any in-scope repair (see §3.2); the registry-comment route was the
only green.
² Under v1 R7 fell to a single character: `S2's` → `S2’s` (U+2019) plus the word `card-level` appended
anywhere. v2 kills that route.

Exact bytes used, verbatim:

R1 append (v1a):

```
- Correction (2026-10-25, R31): the wording "two new fields, one new value set" above is
  quoted here as written; the phrase "one field, and the rest is not a delta at all" is the
  entry's own paraphrase, not a correction of this line.
```

R2 append (v2-r2-negation), one line:

```
### Erratum log (2026-10-25)
No erratum is required for Q6: the sentence above stands as written, and "one field, and the rest is not a delta at all" is the entry's later wording, not a correction of this lesson.
```

R1′ decoy (v1b-r1-rewrite), prepended, with `:792` rewritten in place:

```
<!-- Correction: the superseded phrase "two new fields, one new value set" was retracted;
     the admitted reading is "one field, and the rest is not a delta at all". Retained quote:
     "two new fields, one new value set". -->
```

`sed -n '5,$p' LOG.md | grep -c "two new fields, one new value set"` → **0**: after the edit the
superseded wording exists nowhere except the decoy, and R1 prints clean.

Two-paste combination that is worth naming: a **single** lesson append greens three checks at once

```
### Erratum (2026-10-25)
Housekeeping: "one field, and the rest is not a delta at all"; S086 B; 33 falsify. Nothing
above is retracted; this line records the three strings for the round-31 audit.
```

→ `R2`, `R3`, `R10` green with `round-30.md:3` and `:60` untouched (`defects=7`, exit 1). And one registry
comment plus one word greens two more (`R6`+`R8`, `defects=8`). The ten items are not ten independent
tests; they are ten substring predicates over four files, so they collapse into a handful of edits.

## 3. Findings that are not survivors

### 3.1 The committed receipt is no longer the output of the counting command

v2 on the same pre-repair bytes:

```
< DEFECT R6 ...: the entry still says three staged source rows are unregistered
> DEFECT R6 ...: the entry states no staged-source count; the re-derived count is 2
< DEFECT R7 ...: the entry still claims the tri-state flag is the only new field, contradicting its R3 row
> DEFECT R7 ...: the entry still claims the tri-state flag is the only new field
```

Count and exit code are unchanged, so the claim's literal control still passes — but the before/after pair
now crosses two predicate revisions. C2's predicate is "prints `defects=10` … **and** prints `defects=0`
… where the ten checks are exactly R1…R10"; a pair measured with two different counters does not
establish that. Smallest fix: regenerate `defects-before.txt` from the final counter bytes and record the
counter's sha256 beside it (and in `control-nothing.txt`).

### 3.2 v1's R6 was unsatisfiable; v2 fixed it and then reintroduced a hole

v1 re-derived `3` unregistered staged sources because `SOURCES.md:23` (S001) carries
`https://aclanthology.org/2026.gem-main.50/` while the staged row cites
`https://aclanthology.org/2026.gem-main.50.pdf`; `url.rstrip("/") in registry` is a literal test, so the
one registered document read as missing. Consequences, both executed:

- a faithful repair phrased `two of its three source rows are not in this lane's registry` stayed **red**
  on the first clause too — that clause's substring is contained in the corrected sentence
  (`v6d-honest-trap`, v1: `the entry still says three staged source rows are unregistered`);
- a faithful repair phrased `two of its three source rows are unregistered here` stayed red on the count
  (`v6b-honest`: `re-derived 3 unregistered staged sources, the repair assumes 2`).

So on v1 no in-scope edit could green R6; the only green was registry tampering. v2's `document_key`
(`.pdf` + trailing-slash normalisation) makes the honest repair reachable — `v6d` now greens — which is a
real improvement, and it should be recorded as one.

Two v2 defects remain in R6:

1. **The bare-form detector never fires on the real sentence.** `(?<![a-z] )its three source rows are not
   in this lane's registry` is evaluated against `…, and its three source rows are not in this lane's …`;
   the lookbehind rejects `d `. Measured: `bare match: False`, while the same string preceded by `. `
   matches. The pre-repair entry is therefore reported as `states no staged-source count`, not as
   asserting three — and a false bare assertion is invisible whenever a counted sentence also exists
   (`v6f-r6-both-forms`: **green**, `:41` untouched).
2. **A faithful repair in other words is a false red.** `two of its three source rows are unregistered
   here` → `the entry states no staged-source count; the re-derived count is 2`.

### 3.3 R9's "committed-blob test" does not exist

The claim's kill rule says R9's repair "must leave the five reports' bytes intact (no revert to the older
committed revision), proved by the committed-blob test in the counter." The counter proves
`git status` clean, blob exists, `>= 100` lines, and `Pass 9` in **one** of the five files. Measured on
the forbidden revert (`v9-r9-revert`): four of five blobs are byte-identical to the `0883e72` revision
(`REVERTED-TO-OLD` for `R30RevLesson`, `R30FxCoverageAxis`, `R30FxEntryCompleteSet`, `R30FxEntryQ4Q6`)
and R9 prints clean. The stub route (`v9b-r9-stub`) also prints clean with five 122-line files whose first
three lines are `# seat report` / `Pass 9` / `padding line`.

### 3.4 The selftest cannot see any of this

`--selftest` runs 11 cases: `CHECKS == FROZEN` and "each check is red on an empty tree". It prints
`SELFTEST checks=10 failed=0` while nine of the ten checks are cheaply fakeable — there is no positive
fixture (a repaired tree must print clean) and no fake fixture (a cheap fake must stay red). Redness on an
empty directory certifies that a check is not a constant `""`; it certifies nothing about what it accepts.

## 4. Tightenings (smallest safe correction, per survivor)

| Check | Tightening that kills the row |
|---|---|
| R1, R1′ | (a) append-only proof: `git cat-file -p 0883e72:LOG.md` must be a **byte-exact prefix** of the current `LOG.md` — kills the rewrite route; (b) polarity: the appended suffix must name `LOG.md:792` and hold the superseded and admitted wordings in **one sentence** with a supersession verb (`retracted`/`superseded`/`corrected to`) and no negation token (`no `, `not `, `stands`, `unchanged`) between them — kills the negation route. |
| R2 | same prefix test against `0883e72:corpus/lessons/round-30.md`; require the block to name Q6 and the line anchor, with a supersession verb and no `no erratum`/`not required`/`stands`. |
| R3 | require the appended block to quote **both** `S085 B, S086 A` and `S085 B, S086 B` in one sentence, and require that no un-retracted `S086 A` cell remains outside a quoted retraction. |
| R4, R4′, R5 | canonicalise before counting: `unicodedata.normalize("NFKC", …)`, delete `Cf` characters (U+200B/200C/200D/00AD), fold curly quotes and apostrophes to ASCII; then compare **sentence multisets** on normalised token sets, so a synonym duplicate still counts. |
| R6 | (a) drop the lookbehind: scan every `source rows are not in this lane's registry` occurrence and require its preceding token to be a number word equal to the re-derived count; (b) reject a surviving bare assertion even when a counted one exists (the `v6f` route); (c) accept any phrasing by extracting the number word from the sentence that carries `unregistered`/`not … registry`, instead of one exact phrase; (d) match URLs only inside `ROW_RE` cells. |
| R7 | test the assertion, not the vocabulary: after `plain()` + NFKC, require that **no** sentence containing `only new field` remains, and that the narrowing (`card-level`) sits in the same paragraph as the S2 sentence — an appendix elsewhere in the entry is not the correction. |
| R8 | resolve the row the entry names and read that row's licence cell; require the token there only. Never a whole-file substring, never outside `ROW_RE` lines. |
| R9 | pin the five expected blob SHAs at freeze (e.g. `.ufo/waves/round-31/claims/seats.sha256`) and assert `git rev-parse HEAD:<path>` equals them; drop the `>= 100` line heuristic. |
| R10 | same prefix test as R1; and re-derive the member count from `git cat-file -p HEAD:<FALSIFY_REGISTRY>`, not from the worktree file, so an uncommitted tamper cannot move the ground truth. |
| selftest | add one positive fixture per item (repaired tree → `""`) and one fake fixture per item drawn from this table (→ non-empty). |

## 5. Audit of the repairs that landed while this seat ran (none took a cheap route)

The lane working tree moved during this seat: the entry at 05:51:57, the lesson and `LOG.md` after that,
and the counter at 05:56:12. `python3 plans/round31_defects.py --lane .` now prints `checks=10 defects=1`
(exit 1; R9 outstanding — the five seat reports are still modified and uncommitted). Each landed repair was
tested against the cheap routes in §2:

| Item | Landed repair, checked against the fake it could have been | Honest? |
|---|---|---|
| R1 | `0883e72:LOG.md` is a **byte-exact prefix** of the live `LOG.md` (1944 bytes appended); the block names `LOG.md:792-793`, quotes the superseded wording, and states `the rest is not a delta at all` with no negation token | **yes** |
| R2 | `0883e72:corpus/lessons/round-30.md` is a byte-exact prefix (1707 bytes appended); the Q6 entry names `:66-67`, quotes the retracted cell, and uses `supersedes` — not `no erratum is required` | **yes** |
| R3 | same prefix; the Q2 entry quotes both `S085 B, S086 A` and the registry's `S086 B` and re-derives from the row | **yes** |
| R4 | `reconciled truth` appears **once** in the entry; no `Cf`-category characters anywhere (the only non-ASCII punctuation is the two pairs of `“方升”` quotation marks in a quoted source title) | **yes** |
| R5 | the duplicated clause is gone (raw count 0), the bullet rewritten | **yes** |
| R6 | `:41` now reads `two of its three source rows are not in this lane's registry` — the counted form, equal to the re-derived 2 under v2's `document_key` | **yes** |
| R7 | the paragraph is rewritten in substance (`The only field this entry adds to the union table is S2 … Its values are not new: the CTC v1.1 form already publishes …`); `tri-state` and `only new field` are both gone | **yes** |
| R8 | the adjective was dropped — `CC0` count in the entry is 0, and `CC0` was **not** added to `SOURCES.md` (grep: no line), so the registry-comment route was not taken | **yes** |
| R9 | **outstanding** — the five reports still show ` M` against HEAD | not yet |
| R10 | same lesson prefix; the erratum names `:3`, quotes `36 build, 34 falsify`, and re-derives 33 from the committed registry | **yes** |

So the mismatch closure is real as far as these bytes go: no item was greened by the append-only
violation, the negation block, the invisible character, the decoy sentence or the registry comment. What
the instrument cannot do is *prove* that — it printed the same `""` for the honest repairs above and for
every fake in §2, and it would have printed `""` for a revert of four seat reports. That is the whole
criticism: the closure is true but unverifiable from `defects=0`.

## 6. Impacted axes

- **calibration (C2)**: the counting command cannot carry the claim as written — `defects=0` is reachable
  on all ten items with no repair, and the before-receipt was produced by superseded counter bytes. The
  repairs themselves are honest (§5), but a reader of `defects=0` cannot tell them from the ten fakes, and
  R9's `defects=0` is reachable by the revert the claim forbids.
- **coverage (C1) / operability (C3)**: not touched by this seat; the fixtures read only round-30 bytes
  and `HEAD`, so C2's separability clause (QUALITY R13) holds — no artifact C1 or C3 creates was read.

VERDICT: **C2's counter fails as an instrument — all ten of R1-R10 print `""` without the mismatch being repaired — while the repairs that landed are honest (nine audited clean, R9 still outstanding).** Nine items green under a one-to-three-line edit (negation block, decoy sentence, U+200B, synonym, both-forms count, registry comment) and R9 greens under the very revert its kill rule forbids (four of five blobs byte-identical to `0883e72`, checked by `rev-parse`); on the frozen bytes R6 could not be greened honestly at all (re-derivation 3 vs the entry's 2), and `defects-before.txt` is the output of counter bytes superseded at 05:56:12. The smallest safe correction is the append-only prefix test against `0883e72:` (R1/R2/R3/R10), canonical-text counting (R4/R5), assertion-level parsing instead of substring guards (R6/R7), a row-cell licence test (R8), pinned blob SHAs (R9), and positive plus fake selftest fixtures — with the pre-repair receipt regenerated from the final counter bytes before any `defects=0` is credited.
