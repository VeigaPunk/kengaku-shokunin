# R1C1BeforeRepro — scoped findings (R55-C1 before-state falsifier)

**Verdict: before receipt REPRODUCED; no falsification; no scan gap.**

## Reproduction

Fresh clean shared clone at frozen base `798f5e9ef30ef39291295565209b65a17343c00e`
(scratch: `/fast/scratch/hyaku/kengaku-r55/R1C1BeforeRepro/clone`, tree clean, detached HEAD at base).
Frozen command `python3 plans/round52_c2_registry.py --lane <clone>` (run from the lane, read-only):

- exit **1**
- `ADVERTISED total=79`, `REGISTERED total=77 rows=79` — matches receipt
- `MISSING 2` = exactly `plans/round54_c1_anchor.py`, `plans/round54_c2_entrytruth.py` — matches receipt
- `INCOMPLETE 0 / ENTRY-MISSING 0 / SELFTEST-UNBACKED 0 / DUPLICATE 0`, `PREDICATE R52-C2 fail` — matches receipt

Diff vs committed `.ufo/waves/round-55/claims/c1-before.txt`: **byte-equal except line 2**, the
`COMMAND` clone path (`…/c1before/clone` vs `…/R1C1BeforeRepro/clone`). Evidence:
`w1/R1C1BeforeRepro/receipt-diff.txt`, `w1/R1C1BeforeRepro/c1-before-repro.txt`.

## Scan-completeness (advertised universe cannot miss an advertisement)

Counter scans command-form mentions only in `SCORECARD.md`, `SKILL.md`, `LOG.md`,
`corpus/README.md`, `corpus/knowledge/*.md` (62 files at base). Independent re-derivation with the
frozen regex reproduces `ADVERTISED total=79`; for **all 79** advertised scripts every advertiser
file lies inside the scanned set (zero outside — `w1/R1C1BeforeRepro/scan-advertisers.json`).

Picked-script confirmation:

| advertised script | advertiser files (scanned set) | in scanned set? |
|---|---|---|
| `plans/round54_c1_anchor.py` | `SCORECARD.md` | yes |
| `plans/round52_c2_registry.py` | `SCORECARD.md`, `SKILL.md` | yes |

Corroboration: `plans/round54_c2_entrytruth.py` ← `SCORECARD.md`;
`plans/round53_c2_tipstate.py` ← `LOG.md`, `SCORECARD.md`, `SKILL.md`. The r54 regression vector
(LOG.md advertisement without registry row) is inside the scanned surface — which is why the
counter reports it.

## Defects / residual risk

- None found. Command-form mentions also exist in `.ufo/` wave receipts and `plans/round-54-claims.md`,
  but those are not lane self-assessment files and the counter's bounded scope is documented in its
  header comment; not a gap against the frozen predicate.
- Receipt is honest; R55-C1's before-state stands as frozen.
