# Draft — `## Round69 criterion` (Q50) for `corpus/QUALITY.md`

Target: `corpus/QUALITY.md`, appended after the round-64 criterion block (the file's last line is `:1205`).
Closes R69-C2 **E2** (`plans/round69_c2_routed_defects.py:169-181`): exactly one line strip-equal to
`## Round69 criterion`, and that section's text must contain `Q50`, `corpus/lessons/round-68.md` and
`corpus/lessons/round-68-verifier-spotcheck.md`.

**Heading constraint (measured, not assumed).** `section()` and `count_section()`
(`plans/round69_c2_routed_defects.py:78-96`) match with `ln.strip() == heading`, so the heading must be the
bare string `## Round69 criterion`. A round-63-style title after an em dash
(`## Round63 criterion — a frozen predicate …`, `corpus/QUALITY.md:1174`) would not match and E2 would
print `headings=0`. The house-voice title therefore goes in the lead sentence, below the bare heading.

**Paste only the block between the markers** — the `# Draft —` title above is this file's, not QUALITY.md's.

<!-- paste-start -->
## Round69 criterion

A report citation is re-hashed from the committed bytes before it is written.

- **Q50 — a report cites a digest, a count or a revision-bound claim only after re-deriving it from the committed bytes at citation time, and the citation carries the command that re-derives it.**
  Round 68 cited a probe sha (`32bacf1d…`) that the committed file does not carry (`03793f4f…`) and counted 8 killed A1 mutants where the committed tally shows 7 refused plus 1 accepted by design — both `captured-by: none` in `corpus/lessons/round-68.md` `## Mistakes` rows 1–2, routed by `corpus/lessons/round-67-verifier-spotcheck.md` §5 items 1–2. The same round's C2 receipt pair named the pre-landing `SKILL.md` (`3fe9a6d0…`) while the landing tree carries `544ad892…` (`corpus/lessons/round-68-verifier-spotcheck.md` §5 item 3), and its w1 attack line counted 6/12 over a wider role set than the run-15 definition's 3/12 (§5 item 5). Admission: `sha256sum <path>` for a digest, the counting command for a count, and `git show <rev>:<path>` at both revisions for a revision-bound claim; a mismatch is a dated erratum, never an in-place edit. First instance: `corpus/evidence/round69/c2-receipts/provenance-erratum.txt` (`TREE 27f649f8`, `LANDING 1ec2e60a`, every bound input's sha256 at both revisions, `DIFFERS SKILL.md`), re-derived by gate E3 of `plans/round69_c2_routed_defects.py`.
  Source: `corpus/lessons/round-68.md` `## Mistakes` rows 1–3; `corpus/lessons/round-68-verifier-spotcheck.md` §5 items 3 and 5. This criterion does not rewrite the Q-series criteria above.
<!-- paste-end -->

## Grounding

| claim in the text | source |
|---|---|
| wrong sha `32bacf1d…` vs committed `03793f4f…` | `corpus/lessons/round-68.md` `## Mistakes` row 1; `plans/round68_c2_correction_gate.py:36-37` pins both |
| 8 killed vs `7 refused` + `1 accepted by design` | `corpus/lessons/round-68.md` `## Mistakes` row 2 |
| pre-landing `SKILL.md` `3fe9a6d0…` vs landing `544ad892…` | `corpus/lessons/round-68-verifier-spotcheck.md` §5 item 3; the two shas are the `at-tree=`/`at-landing=` values in `corpus/evidence/round69/c2-receipts/provenance-erratum.txt` |
| w1 `6/12` vs strict `3/12` | `corpus/lessons/round-68-verifier-spotcheck.md` §5 item 5 |
| `captured-by: none` on rows 1–3 | `corpus/lessons/round-68.md` `## Mistakes`, column 3 |
| `TREE 27f649f8`, `LANDING 1ec2e60a`, `DIFFERS SKILL.md` | `plans/round69_c2_routed_defects.py:56-57,183-225`; the committed erratum file |
| `section()`/`count_section()` strip-equality | `plans/round69_c2_routed_defects.py:78-96` |

## Unverifiable here

- The claim "no criterion caught it" rests on the `captured-by: none` cells, which the lesson itself
  writes; I did not audit whether some other criterion covered the same class by implication. The
  round-68 spot-check §4 states the same thing ("`QUALITY.md` was not extended this round", §5 item 2),
  which is the strongest available grounding.
- Row numbering "1–3" is the lesson's own table order (`corpus/lessons/round-68.md:85-93`); rows 4–9 are
  other classes and are not cited.
