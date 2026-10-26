# F37CritNoHarmDiff — no-harm audit by diff (append-only, scores, axes)

Round 37 / hyaku run 8 / wave 2 (falsify). Seat target: `git diff 3ea9a1d9 357dece` restricted to
`SCORECARD.md`, `LOG.md`, `corpus/README.md`, `corpus/QUALITY.md`, `SKILL.md`, `PROVINCE.md`,
`corpus/SOURCES.md`, `corpus/knowledge/`.

Axes attacked: **append-only integrity** (removed / rewritten lines), **score authority** (a score raised
without a counter, an axis silently raised or lowered), **disclosure** (a landed retraction with no round-record
line), **single authority** (a normative sentence left live and contradicted by the tree it ships in).

Base identity checked first: `3ea9a1d9` is the immediate parent of the round-37 chain
(`git merge-base --is-ancestor` → ANCESTOR_YES; `git log --oneline 3ea9a1d9..357dece` → 10 commits,
`ca79046` first). The diff is exactly the round-37 work, not a wider window.

## 1. Headline: zero removed lines, zero rewrites, no score moved

```
$ git diff 3ea9a1d9 357dece --numstat | awk '$2!=0' | wc -l          → 0
$ git diff 3ea9a1d9 357dece --numstat | wc -l                        → 71
$ git diff 3ea9a1d9 357dece --numstat | awk '{s+=$1} END{print s}'   → 8323
$ git diff 3ea9a1d9 357dece --numstat | awk '{s+=$2} END{print s}'   → 0
$ git diff 3ea9a1d9 357dece | grep -c '^-[^-]'                       → 0
$ git diff 3ea9a1d9 357dece --name-status | cut -c1 | sort | uniq -c → 63 A, 8 M
$ git diff 3ea9a1d9 357dece --diff-filter=DRM --name-status          → 8 lines, all M
```

**Every `-` line in the whole diff: none.** 71 files, 8323 insertions, 0 deletions, 0 renames, 0 file
deletions. The 8 modified files are pure appends (new table rows after the last row, new sections at EOF).

Per-file counts for the audited tree (all `-0`):

| file | + | − |
|---|---|---|
| `SCORECARD.md` | 50 | 0 |
| `LOG.md` | 33 | 0 |
| `corpus/README.md` | 11 | 0 |
| `corpus/QUALITY.md` | 72 | 0 |
| `SKILL.md` | 72 | 0 |
| `PROVINCE.md` | 28 | 0 |
| `corpus/SOURCES.md` | 4 | 0 |
| `corpus/knowledge/tb2-git-webserver-grader.md` (new) | 291 | 0 |
| `corpus/knowledge/tb2-regex-log-grader.md` | 53 | 0 |

### Scores: none raised, none lowered

- Round-37 table (`SCORECARD.md`): C1 **`8 → 8 held`** — "No score raise: the denominator is the lane's own
  mutant list"; C2 **`7 → 7 held` (L0 cap)**. Both carry a before→after command and its literal output.
- `SCORECARD.md` round-37 also states "Other axes held: novelty 7, depth 9, operability 8, freshness 8,
  adjacency 8" — numerically identical to the round-36 closing line at base `SCORECARD.md:1224`, so no axis
  was silently raised, lowered or claimed improved.
- `LOG.md:1082` declares "Declared C1 calibration (8)" — consistent with the `8 → 8 held` cell; no drift
  between LOG and SCORECARD.
- The only additions that could be read as score-adjacent are two **capability-catalog rows**
  (`gate-mutation-harness`, `service-grader-probe`), which are table entries with a command and a literal
  expected line, not axis scores. Both are new rows; no existing row was edited.
- No added line in the audited tree states an axis harmed or reduced (`grep -iE 'harmed|lowered|downgrade|
  reduced to|score down'` over added lines: only my own task prompt text inside the dispatch JSON).

## 2. Findings

### F1 — the landing ships a registry sentence that contradicts its own tree, and calls a pre-landing commit "the lane tip" (medium)

**Counterexample.** `SKILL.md:608-610` (landed in `357dece`) reads: "on the lane tip `44b7298` its draft prints
`rows=103 tokens=11 defects=5` and exits 1 … so this row records a red state, not a green one."

**Measured on a clean clone of the pushed tip** (`toplevel=/fast/scratch/.../fx/lane`, `git rev-parse HEAD`
= `357dece…`):

```
$ python3 plans/anchor_digest_check.py --lane .
rows=107 tokens=15 defects=0
exit=0
```

`357dece` is the landing tip; `44b7298` is five commits behind it, and the erratum
(`corpus/lessons/round-37.md:32`) plus `corpus/evidence/round37/anchor-captures/` both landed inside this same
window (`c138da2`). So at the tip the tool is green — and the landing says so twice elsewhere:
`SCORECARD.md:1285` ("clears to 0 after the appended erratum and four captures") and the landing's own receipt
`integrate/measure-final.txt:151` (`rows=107 tokens=15 defects=0`).

Three documents of one landing (`SCORECARD.md`, the receipt, the tool's measured output) say green; the
normative registry paragraph says "red state" and attaches the words "lane tip" to a non-final commit. The
registry row the paragraph describes is `SKILL.md:580` (`anchor-digest-check`), whose self-test column says
"none at runtime — read-only `git ls-tree`" and therefore invites the reader to trust this prose.

**Impacted axes:** none numerically — calibration and coverage are held, and the C1/C2 predicates are
unaffected by `SKILL.md`. Impact is on **single authority / provenance**: an operator reading the registry at
the tip is told the shipped checker is red. This is a pure append defect (nothing was removed); the round-36
addendum was correctly left alone; the new paragraph overreached by asserting a present-tense state.

**Smallest safe correction:** append one sentence to the round-37 SKILL addendum — "Measured at the landing
tip `357deceb`: `rows=107 tokens=15 defects=0`, exit 0; the `44b7298` figures above are the pre-erratum state."
No rewrite of either paragraph.

### F2 — a live round-36 clause is contradicted by the round-37 append with no supersede marker (low)

`SKILL.md:596` (unchanged, correctly append-only) says the round-36 battery left "the gate's clauses …
untested beyond wave-1 candidates and the battery". `SKILL.md:602-606` (new) reports 50 of 55 advertised
clauses undemonstrated at freeze and demonstrated at landing. Both statements are live in the same registry.

The lane's own convention marks this: `QUALITY.md` Q26 carries "Supersedes: none", Q27 carries "Supersedes
Q24's middle clause", `PROVINCE.md` R37-P1 carries "supersedes three clauses". The SKILL round-37 addendum
carries no supersede marker (grep over added lines: the only `supersede` hits in the audited docs are
`PROVINCE.md:4181`, `QUALITY.md:4403/4446`).

**Impacted axes:** single authority only; position resolves it for a whole-file reader, and a `grep`-level
reader gets a false negative about gate coverage.

**Smallest safe correction:** prefix that sentence with "Supersedes the round-36 addendum's 'the gate's
clauses are untested beyond wave-1 candidates and the battery'".

### F3 — a landed retraction of a round-36 admitted entry has no line in the round record (low)

`corpus/knowledge/tb2-regex-log-grader.md` +53 appends an `## Errata (round 37)` block that withdraws
receipt-backing from the round-36 entry's `What decides it` column ("11 of its 16 failing cases carry a
byte-identical `assertion=` string") and adds two further S110 errata (digest, and span: this file's `1–11` and
the row's `instruction.md:1-19` are both not the requirement-bullet span).

`LOG.md` round-37 and `SCORECARD.md` round-37 mention neither:

```
$ git show 357dece:LOG.md        | sed -n '/## Round 37/,/^$/p' | grep -icE 'regex|errata'   → 0
$ git show 357dece:SCORECARD.md  | sed -n '/## Round 37/,$p'    | grep -icE 'regex|errata'   → 0
```

The retraction is disclosed only in `PROVINCE.md` R37-P1 ("establishes no regex or log-parsing correctness")
and inside the errata block itself. No numeric axis moved, and I verified the errata's own provenance claims
are true (§3), so this is a disclosure gap, not a false claim.

**Impacted axes:** disclosure; coverage stays 7 held, so nothing is silently scored.

**Smallest safe correction:** one LOG round-37 bullet naming the errata (S110 digest + span, the
`What decides it` column's loss of receipt-backing) and pointing at `R37R36Absorb`.

### F4 — append-only consequence, not a violation: the S110 span correction is unenforced (informational)

`corpus/SOURCES.md:125` still carries the 63-hex token and `instruction.md:1-19` at the tip (verified:
`grep -o 'sha256 [0-9a-f]*'` → 63 chars). Rewriting the row would break the append-only rule, so leaving it is
correct. The digest half *is* mechanically re-checked — `plans/anchor_digest_check.py:80` matches
`^ {0,3}Erratum \(round 37\): (S\d{3,}) anchor sha256` in `corpus/lessons/*.md` and exempts the row only when
the erratum's own 64-hex token resolves (`:55-58`), which is why the tip prints `defects=0`. The **span** is
not covered by Q26 (it governs `sha256` tokens only) or by any other counter, so the errata's span correction
can regress unnoticed. Named gap for round 38; no action needed in this landing.

## 3. No-harm checks that came back clean (evidence)

- **The gate was not edited**, so C1's "unedited gate" leg holds: `plans/pkg_gate.py` is absent from the diff
  (`--name-only … | wc -l` → 0) and `sha256sum plans/pkg_gate.py` =
  `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`, equal to Q27's pin.
- **Registry arithmetic claims corroborated by the tool**, not just asserted: SCORECARD's "103 → 107 rows" vs
  measured `rows=107 tokens=15`; the capability row's `BATTERY fixtures=64` vs the receipt's 64 `FIXTURE`
  lines (`measure-final.txt:5-68`, 14 round-36 + 50 across the 9 `plans/battery37/` modules).
- **Errata provenance is true:** `sha256sum -c corpus/evidence/round36/tb2-regex-log/SHA256SUMS` → 5/5 `OK`;
  the corrected 64-hex token equals `sha256sum corpus/evidence/round36/tb2-regex-log/instruction.md`.
- **Declared supersessions are accurately scoped:** Q27 supersedes only Q24's middle clause ("every
  single-property junk mutant must be rejected") and explicitly preserves Q24's ordering rule and its
  `unevaluated` leg — Q24's text at `QUALITY.md:299-341` contains exactly that middle clause, so the scoping
  is correct, not over-broad.
- **No criterion-number collision:** base has 25 `Q` criteria, tip has 27, and `sort | uniq -c | awk '$1>1'`
  over `**Q<n>` is empty — Q26/Q27 are fresh numbers.
- **PROVINCE's three-clause supersession is a narrowing, not a silent gain:** R37-P1 reduces what the
  round-36 paragraph establishes ("no regex or log-parsing correctness") and re-reads "other 88 TB2 tasks" as
  "86 of TB2's 89"; the round-35/36 paragraphs are left byte-identical, exactly as their own text promised.
- **No file outside the lane's own surfaces was touched:** the 8 modified files are the 8 audited docs; no
  `AXES.md`, `SHONEN.md`, harness or sibling-lane path appears in the diff.

Receipts for the measured claims: `.ufo/waves/round-37/falsify/F37CritNoHarmDiff/receipts.txt`.
Scratch `/fast/scratch/hyaku/kengaku-r37/F37CritNoHarmDiff` removed after copying receipts; no lane file was
edited; no mutating git command was run in the lane.

VERDICT: no-harm-removed-lines-0
