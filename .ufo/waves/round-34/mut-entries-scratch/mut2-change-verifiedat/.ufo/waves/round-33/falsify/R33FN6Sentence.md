# R33FN6Sentence — N6 one-sentence aggregation (round 33 falsify, 2026-10-25)

Seat: `KengakuR33.R33FN6Sentence` (executor / leaf). Lane: `kengaku-shokunin`.
Target: `check_n6` in `plans/round33_defects.py:139-163` against the frozen N6 clause of
`plans/round-33-claims.md:97-99`.
Attack: supply every N6 token from **one unrelated appended sentence** in a `/tmp` fixture.

Bounds honoured: no lane or fleet byte edited, staged, or committed; no git command run in the lane or
fleet (I called `check_n6` by import, and `check_n6` shells out to nothing); no subagent; no pacman, no
tool installed; all fixtures under `/tmp/r33n6-sentence/`.

## 1. The frozen clause under attack (verbatim)

`plans/round-33-claims.md:97-99`:

> N6 `corpus/lessons/round-30.md` still contains `:78-81` (or `78–81`) and carries a
> labelled correction note pointing the Q6 retraction at entry lines `:72` and
> `82-83`, and carries a labelled erratum recording S086 as published without peer review.

## 2. The counter under attack (verbatim, `plans/round33_defects.py:139-163`)

```python
def check_n6(lane: Path) -> str:
    path = lane / LESSON30
    if not path.is_file():
        return f"{LESSON30} is unreadable"
    text = read(path)
    if ":78-81" not in text and "78–81" not in text:
        return "the round-30 lesson erratum's stale :78-81 reference is gone: append-only forbids rewriting it"
    if ":72" not in text or "82-83" not in text:
        return "no appended correction updates the round-30 erratum's entry line refs to :72 / :82-83"
    if not near(text, ":72", "82-83", width=300) or (
        not near(text, ":72", "corrected", width=300)
        and not near(text, ":72", "superseded", width=300)
    ):
        return "the round-30 lesson correction note is not labelled"
    if "peer-reviewed" not in text:
        return "the round-30 lesson's peer-reviewed grouping is gone: append-only forbids rewriting it"
    if not near(text, "S086", "without peer review", width=250) and not near(
        text, "S086", "not peer-reviewed", width=250
    ):
        return "no appended erratum records S086 as published without peer review"
    if not near(text, "S086", "erratum", width=250) and not near(
        text, "S086", "correction", width=250
    ):
        return "the S086 peer-review erratum is not labelled"
    return ""
```

`near` (`:60-64`) is `re.search(a + ".{0,width}" + b)` **without `re.DOTALL`**, so every co-occurrence
clause is same-line only.

## 3. Fixtures and the single sentence

Harness: `/tmp/r33n6-sentence/harness.py` (imports the lane module read-only, writes only under
`/tmp/r33n6-sentence/lanes/<name>/corpus/lessons/round-30.md`).

The one sentence, semantically about an orchard rota and a seed catalogue — nothing to do with the Q6
retraction or the registry's S086 peer-review status:

> By the way, the orchard's irrigation rota was peer-reviewed and corrected, moving the hose reel from
> :78-81 to :72 and the sprayer to 82-83, while the seed catalogue's S086 erratum says the plum variety
> was published without peer review.

Token geometry inside it (237 chars, one line): `peer-reviewed`@46, `corrected`@64, `:78-81`@101,
`:72`@111, `82-83`@134, `S086`@168, `erratum`@173, `without peer review`@217 — every pair the counter
binds is within 300/250 chars on the same line.

## 4. Results (exact command and output)

`cd /tmp/r33n6-sentence && python3 harness.py` → exit 0:

```
== F0-seed-only
   note      : real lesson bytes with the round-33 errata section removed
   check_n6  : RED: no appended correction updates the round-30 erratum's entry line refs to :72 / :82-83
== F1-seed-plus-one-sentence
   note      : same seed, plus the single unrelated sentence appended
   check_n6  : GREEN (no defect reported)
== F2-stub-plus-one-sentence
   note      : no lesson content at all: one prose line plus the single unrelated sentence
   check_n6  : GREEN (no defect reported)
== F3-sentence-inserted-midfile
   note      : sentence injected after the title instead of appended
   check_n6  : GREEN (no defect reported)
== F6-keyword-salad
   note      : one line of keywords, not even a sentence
   check_n6  : GREEN (no defect reported)
== F4-substring-182-830
   note      : locator satisfied by the page number 182-830, not by 82-83
   check_n6  : GREEN (no defect reported)
== F7-contradiction
   note      : sentence asserts the erratum and the correction are both false
   check_n6  : GREEN (no defect reported)
== F5-stale-token-rewritten
   note      : round-31 erratum rewritten (append-only violated); only the new sentence still says :78-81
   check_n6  : GREEN (no defect reported)
```

`diff -u lanes/F0/... lanes/F1/...` shows the whole delta between red and green is one added sentence
plus the blank separator (3 added lines, 20902 → 21141 bytes, +239 B). F2's entire file is 322 bytes:

```
# Round 30 - lesson

Prose that carries no locator, no source id, no review token.

By the way, the orchard's irrigation rota was peer-reviewed and corrected, moving the hose reel from :78-81 to :72 and the sprayer to 82-83, while the seed catalogue's S086 erratum says the plum variety was published without peer review.
```

`find lanes/F2 -type f` → `lanes/F2/corpus/lessons/round-30.md` only: the fixture contains **no
`corpus/knowledge/` directory at all**, yet the counter is green.

The variant sentences:

- F6 salad: `corrected :72 82-83 S086 erratum without peer review peer-reviewed :78-81`
- F4 substring: `... moving the hose reel from :78-81 to :72 and the sprayer to page 182-830, ...`
- F7 contradiction: `The S086 erratum says it was not peer-reviewed, but that is false: S086 is
  peer-reviewed, and the :78-81 locator was never corrected to :72 or 82-83.`

## 5. Findings

**A1 — one unrelated sentence satisfies all N6 clauses (the assigned attack).** F0 red → F1 green with
one appended sentence. The sentence names an orchard and a seed catalogue; it does not point the Q6
retraction anywhere and does not record S086's peer-review status. `check_n6` returns `""`.

**A2 — the counter never opens the cited artifact.** F2 (322 bytes, no entry file) is green, so the
clauses "entry lines `:72`" and "`82-83`" are never verified against
`corpus/knowledge/contamination-transparency-card.md`. A wrong or stale locator is indistinguishable
from a right one.

**A3 — "appended" is not tested.** F3 injects the same sentence after the title; still green. Nothing
binds the tokens to the end of the file, so the predicate's append-only shape is unenforced.

**A4 — not even a sentence is needed.** F6, a single line of keywords, is green.

**A5 — `82-83` is matched as a raw substring.** F4's `page 182-830` contains `82-83` and passes, so a
locator-shaped token can be satisfied by an unrelated number.

**A6 — a sentence that denies the required content passes.** F7 asserts that the erratum is false, that
S086 *is* peer-reviewed, and that the correction never happened; every token the counter looks for is
present, so it is green. The predicate's "recording S086 as published without peer review" and
"correction note pointing ... at `:72` and `82-83`" are satisfied by their negation.

**A7 — the append-only guard is defeatable by the same sentence.** F5 rewrites the round-31 erratum
(`card.md:78-81` → `:72` and `82-83`) — an append-only violation — and stays green because the new
sentence still prints `:78-81`. So "still contains `:78-81`" does not establish that the original bytes
survive.

**A8 — the check is also brittle in the honest direction.** A semantically correct note wrapped across a
line break reddens (`F8`: `the round-30 lesson correction note is not labelled`), because `near` lacks
`DOTALL`:

```
near same-line  : True
near split-lines: False
near 299 x's    : True   # distance 299 <= window
near 300 x's    : True   # distance 300 <= window (inclusive)
```

So prose is pushed toward one crammed line — exactly the shape A1/A4 exploit.

**A9 — the shipped selftest cannot distinguish the counter from token presence.** A `/tmp` mutant
(`/tmp/r33n6-sentence/mutant/mutant.py`) whose `check_n6` is only "file exists + these tokens present"
(no proximity, no labels) passes the shipped selftest unchanged:

```
CASE N6-red-on-empty PASS
CASE N6-green-corrected PASS
SELFTEST checks=14 failed=0
```

and agrees with the original on 8 of 9 fixtures (only F8 differs, where the mutant is *more*
permissive); the real lane is green under both (`''` vs `''`). The selftest's own green fixture
(`plans/round33_defects.py:221-226`) is a three-line crammed string whose Correction and Erratum notes
each sit on one line, so no case presents a file that is *semantically* wrong but token-rich.

## 6. What is still true (scoping the finding)

The real artifact is substantively right; the defect is that the counter would accept an artifact that
is not.

- `corpus/lessons/round-30.md:211-217` carries the two labelled notes; N6a reads "the landed entry's
  lines are `:72` and `82-83` — corrected, with the `:78-81` reference superseded rather than
  rewritten", N6b reads "Erratum: S086 is published without peer review". `check_n6(real lane)` →
  `''`.
- The cited entry does carry the corrected text: line 72 opens "So the delta is one field, and the rest
  is not a delta at all…"; lines 82-83 carry "Two earlier readings … overclaimed; this is the corrected
  one".
- `corpus/SOURCES.md:110` (S086 row) has tier cell `B` and cell 5 "the society publishes these
  proceedings **without peer review**", so N6b's factual basis holds and lesson line 66's
  "S083/S086 peer-reviewed" grouping was the wrong cell.
- `:78-81` and `peer-reviewed` are present in the pre-round-33 bytes (`:197`, `:66`), so the stale
  tokens were load-bearing at freeze — as a *token*, not as protected bytes (A7).

## 7. Verdict

**VERDICT: uncaught** — `check_n6` accepts a single unrelated appended sentence (F1), a 322-byte stub
with no cited artifact (F2), a keyword salad (F6), a substring `182-830` (F4), a sentence denying the
erratum (F7), and a rewritten stale token (F5); and it rejects an honest wrapped note (F8). The N6
clause of C2 is true of the landed bytes but is **not established by the counting command**: the same
command is green on artifacts that would falsify the clause. Any N6 closure receipt that cites only
`checks=6 defects=0` carries no evidence for N6's content.

Advisory (no remediation performed, per lane bounds): bind the correction to an appended section
heading and to the cited file's actual lines, require the two notes to be separate labelled entries,
use `DOTALL`-free but line-anchored matching on a labelled block, and add a selftest case whose file is
token-rich but semantically wrong.

## 8. Not exercised

- The aggregate `python3 plans/round33_defects.py --lane .` was not run: `check_n1` shells `git -C
  <lane>`, and lane Git state is off-limits for this seat. Every statement above is about `check_n6`
  called directly (read-only file access).
- No mutation of the lane's lesson or of any fleet report; no check of N1-N5 (sibling seats).
- Fixtures used no git at all, so no repository state exists under `/tmp/r33n6-sentence/`.
