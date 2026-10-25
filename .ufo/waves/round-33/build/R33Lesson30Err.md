# R33Lesson30Err — round-30 lesson errata (routed defect N6)

Seat: `R33Lesson30Err` (scribe, leaf). Lane: `kengaku-shokunin`, tip read `7895588`
(`round-33: C2 routed-defect repairs (N2 scorecard section, N5/N6 lesson errata), Q22, defects-after receipt`).
Target: `corpus/lessons/round-30.md`. No production edit made by this seat; this file is the deliverable.

## 1. Premise checks in committed bytes

### 1a. `:66` groups S083/S086 as peer-reviewed

`corpus/lessons/round-30.md:66` (whole line, sha256 of file `a1eea054c3f803365ba4b22fb4bc355923992ade14c5d16653b9cdd6c1baf231`):

> `  S085 a self-report, S081/S082 preprints vs S083/S086 peer-reviewed); Q6 pass (§Extends names both`

Counter-claim, `corpus/SOURCES.md:110` (S086 row, extensional cell):

> `... the paper's own contamination-detection method and its false-positive caveat for code benchmarks, in Japanese; the society publishes these proceedings **without peer review**`

`S086` is the only registry row carrying `without peer review` (`grep -c "without peer review" corpus/SOURCES.md` → `1`).
So `:66` is wrong on S086 as charged: the society (言語処理学会) publishes these proceedings without peer review.
(S083, ACL Findings, is genuinely peer-reviewed; the defect is the grouping of S086 with it, not the S083 half.)

### 1b. The round-30 erratum's `:78-81` entry locator

`corpus/lessons/round-30.md:197`:

> `  (\`corpus/knowledge/contamination-transparency-card.md:78-81\`): the delta is **one field, and the rest`

Observed entry bytes (`corpus/knowledge/contamination-transparency-card.md`, numbered):

- `:72` — `So the delta is one field, and the rest is not a delta at all. **The only field this entry adds to the`
- `:82-83` — `is the authoritative status. Two earlier readings of this paragraph ("two new fields", then "one field, one` / `placement, one value set") overclaimed; this is the corrected one, and it is why the amendme…`
- `:78-81` — `it is filed, and this lane cannot settle it without reading that form, which it has not admitted. R1's` … `strata are carried by the CTC v1.1 form (\`strata_reported\`) and are absent from the other two tabulated` … `designs, while also being present in S081's own four-field protocol (F1, strata) — so strata is a value` … `set this entry inherits from two cited-or-tabulated sources, not a discovery, and the mapping row above`

Programmatic read of those spans: `:78-81` contains neither `overclaim` nor `corrected`; `:82-83` contains both;
`:72` opens the corrected paragraph. The retraction sentence therefore lives at `:72` and `:82-83`, not `:78-81`.
Both premises as filed in the assignment are confirmed against committed bytes.

## 2. Verbatim append block — `## Errata (round 33)` for the END of round-30.md

Bytes (sha256 `6d9404ecdd03743d98440046cac4577dbe4a22e649072c8207b5f923dfc7906f`, 304 bytes, trailing newline):

```markdown
## Errata (round 33)

- Correction (round 33, appended): the Q6 erratum at :197 cites the entry at :78-81; the landed lines are :72 and 82-83 — corrected, stale refs kept.
- Erratum (round 33, appended): :66 groups "S083/S086 peer-reviewed"; the registry records S086 as published without peer review.
```

Append-only invariant held: `:78-81` (at `round-30.md:197`) and `peer-reviewed` (at `:66`) both stay in the file;
the block supersedes without rewriting filed cells.

## 3. Counter evidence

`python3 plans/round33_defects.py --lane .` → `checks=6 defects=0`, exit `0` (run at tip `7895588`).

`check_n6` sub-predicates evaluated against the block above, standalone (`near(...,300)` / `near(...,250)`, `re.I`):

| sub-check | result |
|---|---|
| stale `:78-81` still present | pass |
| `:72` and `82-83` both present | pass (both) |
| `:72` … `82-83` within 300 chars | pass |
| `:72` labelled `corrected`/`superseded` within 300 | pass (`corrected`) |
| `peer-reviewed` still present | pass |
| `S086` … `without peer review` within 250 | pass |
| `S086` … `erratum`/`correction` within 250 | pass (`erratum`) |

In-memory simulation of both integration shapes on the current file text: append-after-EOF and
replace-landed-section both satisfy all seven sub-checks. No bytes were written to `corpus/`.

## 4. Finding — the wave has already landed a non-verbatim block (integration hazard)

Commit `7895588` appended 9 lines to `corpus/lessons/round-30.md` (`git show --stat`: `corpus/lessons/round-30.md | 9 +++++++++`)
under the heading `## Errata (round 33, appended — the filed bytes above stand as written)`, with prose whose substance
matches both notes (N6a: "the landed entry's lines are `:72` and `82-83` — corrected, with the `:78-81` reference superseded";
N6b: "the registry's S086 row records the society as publishing without peer review … Erratum: S086 is published without peer review").
That block is *not* the verbatim text this item specifies, and the counter is green on it.

Consequence for the L1:

- **Append-verbatim without removal** yields two `## Errata (round 33…` headings and duplicated content (section count 2). N6 still passes.
- **Recommended:** replace the landed appended section with the §2 block (single heading, section count 1, still green) —
  append-only protects the *filed* cells above `:189`, not a round-33 appended block, so adjusting the round-33 block is not a rewrite of the record.
- If the landed wording is preferred, N6 is already satisfied and this item reduces to a wording reconciliation, not a repair.

Nothing else in the file diverges: `git diff 7895588^ 7895588 -- corpus/lessons/round-30.md` is a pure 9-line insertion at EOF.

## 5. Bounds and provenance

- Writes: this file only. Scratch: `/tmp/r33-R33Lesson30Err/` (< 1 KB). No write to `corpus/`, `plans/`, fleet repo, `shokuknow`, lane Git index.
- Git use: read-only (`log`, `show`, `diff`-free inspection). No add/commit/checkout/reset/push, no jj mutation.
- Tools installed/upgraded: none (system `python3` and coreutils sufficed); no pacman transaction attempted.
- Model: none passed. `agent://all`: not called. No subagents/background jobs spawned (leaf).
- Access date 2026-10-25 applies to sources; no network fetch was needed for this item (all evidence is committed bytes in-lane).

## 6. Falsifiers

- If `corpus/SOURCES.md`'s S086 row ever changes to a peer-reviewed venue, note 2's erratum becomes false and must be retracted, not softened.
- If `contamination-transparency-card.md` is reflowed so that `:72` / `:82-83` no longer carry the retraction, note 1's line refs go stale and N6's locator check would pass on a wrong file position — recheck by text ("overclaimed; this is the corrected one") before trusting line numbers.
- If a round-33-appended block is later treated as filed record, the append-only argument in §4 no longer licenses replacing it; then only the landed wording stands.

VERDICT: lesson30-errata-drafted
