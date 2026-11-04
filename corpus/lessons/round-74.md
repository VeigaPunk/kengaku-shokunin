# Round 74 — kengaku (2026-11-04 UTC)

Base `b7910802549978404218937d4be6a75acae0e020` (round-73 verifier spot-check).
R74-C1 targets coverage: decoupled advertised instrument discovery without circular self-advertising.
R74-C2 targets calibration: hardened registry audit pricing malformed rows, unbacked entry flags, self-test scripts, and errata revision consistency.

## Gate

- **S250 admitted for Python argparse command-line flag and argument specification contracts.**
  URL opened live by L1 KengakuR74 this round: `https://docs.python.org/3/library/argparse.html#name-or-flags`.
  Access date: 2026-11-04 UTC. Title: Python 3.15.2 argparse documentation.
  Capture: `corpus/evidence/round74/sources/argparse-docs.html`, HTTP 200, 334994 bytes.
  SHA256: `ad9095cdaa99c953046f510d6cd86cd6f7a1086c5aa35743c26e3fa41e4b5b8d`.
  Located anchor quote, capture line 908:
  **“The add_argument() method must know whether an optional argument, like -f or --foo, or a positional argument, like a list of filenames, is expected.”** (24 words).
  Fetch details and anchor notes: `corpus/evidence/round74/sources/argparse-anchor.md`.
  Kind docs, tier A for command-line argument and option string specification.
  Registry change: absent → S250 mined, recheck on-release, used-by `corpus/lessons/round-74.md, corpus/knowledge/registry-argv-and-flag-audit.md`.
- **Reject candidate:** “Presence of a flag string in a script body proves `argparse` acceptance.”
  Same source explicitly distinguishes argument strings from positional arguments and parser actions; string matching does not verify option registration, parser configuration, or runtime execution.
  Flip: controlled execution with `--help` / `--<flag>` or AST verification of `parser.add_argument()`.
- **Held knowledge candidate:** `corpus/knowledge/registry-argv-and-flag-audit.md` (admission: hold).
- **Earlier held candidates remain held:** `corpus/knowledge/instrument-registry-derivation.md` (round 73), `corpus/knowledge/tb2-hf-model-inference-offline.md` and `corpus/knowledge/tb2-hf-model-inference-provenance.md` (rounds 71/72).
- **Assimilation: none.** No staged shokuknow rows appended. Open L0 `kengaku | round-54` carried.

## Mistakes

| id / class | evidence pointer | captured-by | fix / disposition |
|---|---|---|---|
| M74-1 survivor — malformed table lines silently dropped by parser | `corpus/evidence/round73/w1/c2-blindspots.md` C10, C11; `plans/round73_c2_registry_audit.py:85` | Q46, Q49 | In `round74_c2_registry_audit.py`, table lines starting with `\|` with columns != 8 are reported as named `MALFORMED-ROW` defect lines rather than skipped. |
| M74-2 unbacked — entry command flags not verified against script body | `corpus/evidence/round73/w1/c2-blindspots.md` C14 | Q46 | `command_flags(entry)` is now evaluated in `price_row`, verifying all declared flags exist in script text (`entry:unbacked-flag:<flag>`). |
| M74-3 erratum — contradictory revision ignored if first item matches | `corpus/evidence/round73/w1/c2-blindspots.md` C16 | Q50 | `check_errata` checks every item mentioning `label`, flagging `ERRATA:contradictory-revision` if any matching item carries a contradictory revision. |
| M74-4 vacuous — registry table self-advertises in registry gate | `plans/round52_c2_registry.py:45` | Q46, Q54 | `self_assessment_files` in `round74_c1_registry.py` scans `SKILL.md` strictly outside the `## Gate/probe registry` block, decoupling discovery from registration. |
| M74-5 reference-drift — regex failed to match hyphenated directories | `plans/round52_c2_registry.py:36` `[A-Za-z0-9_]+` | Q46 | Regex updated to `[A-Za-z0-9_.-]+` so that hyphenated directories (e.g. `round13-coverage/coverage_census.py`) are captured. |
| M74-6 reference-drift — claims-doc Before prose contradicted committed receipt | `plans/round-74-claims.md` Before bullet vs `corpus/evidence/round74/c1-before.txt` | Q50 | Amendment A1 (74e2e15) corrects the Before description to the receipt's actual legacy numbers; predicate unchanged. |
| M74-7 fidelity — control receipt evidenced weaker case than frozen sentence | `.ufo/waves/round-74/w1/C1DecoupledAuditR74.md` MEDIUM finding | Q46/Q49 | Regenerated `c1-control-decoupled.txt` from a plans/*.md-only advertisement fixture: decoupled MISSING 1 rc 1 vs legacy MISSING 0 PREDICATE R52-C2 pass (false green). |

## Wave integration (w1, 16 seats)

WAVE-DONE received; `w1-results.json` carries 16 results, of which 4 seats returned full reports and 12 settled with empty output (dead seats, recorded honestly): C1CriticR74, C2AuditReplayR74, C2BlindSpotR74, C2CriticR74, SourcesArgparseR74, KnowledgeEntryR74, LessonR74, SiblingConnectorR74, CredentialSentinelR74, RoundStateScoutR74, C1FixtureControlR74, C2FixtureControlR74.

- **C1GateReplayR74** (executor): independently re-ran all three frozen C1 commands at tip 74e2e15 — byte-identical to `c1-after.txt`, `c1-selftest.txt` and `c1-before.txt`; confirmed A1 resolves the prose/receipt drift.
- **C1DecoupledAuditR74** (reviewer): 4/4 audit items PASS (block exclusion byte-equality, phantom no-self-advertise, row-removal MISSING 1, hyphenated paths); MEDIUM receipt-fidelity finding (M74-7, fixed above); LOW residual notes (hardcoded lone hyphenated evidence path; `\n## ` block-boundary fence hazard; rows advertised only via plans/round-74-claims.md).
- **RegistryReviewerR74** (reviewer): 8-field matrix PASS for both new rows; executed both selftests and the 7-mutant matrix; confirmed landing-tip predicates on the working tree and the discriminating red at committed tip cea7ebf3 (rows not yet landed).
- **EntryFalsifyR74** (reviewer): all four held entries confirmed `admission: hold`; LOW findings fixed in-tree (Q1 triad added to the round-74 candidate and the writer line added to the round-73 candidate; round-74 lesson earlier-held line now names the provenance entry).

The 12 dead seats leave the C2 blind-spot battery, sentinel scan and sibling scan un-re-run by seats; the L1 re-ran the C2 discriminating fixture and both selftests/mutants directly as integration evidence (`c2-controls.txt`, `c2-red-before.txt`), and the freeze-time receipts cover the rest.

## Measurements and controls

- C1 Before: `corpus/evidence/round74/c1-before.txt` (`plans/round74_c1_registry.py --universe legacy` exits 1,
  `MISSING 5`, `PREDICATE R74-C1 fail`).
  **Correction (round 75, 2026-11-04, R74-D2):** the committed receipt prints `ADVERTISED total=115`,
  `REGISTERED total=115 rows=116`, `MISSING 0`, `PREDICATE R52-C2 pass`, `PREDICATE R74-C1 fail`, rc 1 — not
  `MISSING 5`. The `MISSING 5` figure was the round-73-era legacy state, and Amendment A1 already corrected
  the claims doc; this line is the surviving copy. The substantive before-state (legacy cannot see dropped
  unreferenced rows and never scans `plans/*.md`) is unchanged; see `corpus/lessons/round-75.md` M75-7.
- C1 After: `corpus/evidence/round74/c1-after.txt` (`plans/round74_c1_registry.py --lane .` exits 0, `MISSING 0`, `PREDICATE R74-C1 pass`).
- C1 Control: `corpus/evidence/round74/c1-control-decoupled.txt` (a dropped registry row in decoupled mode raises MISSING 1; legacy counter falsely remains green).
- C2 Before: `corpus/evidence/round74/c2-red-before.txt` (round-73 audit exits 0 on 9-cell malformed row; round-74 audit exits 1 with `MALFORMED-ROW columns=9`).
- C2 After: `corpus/evidence/round74/c2-after.txt` (`plans/round74_c2_registry_audit.py --lane .` exits 0, `MISMATCH 0`, `PREDICATE R74-C2 pass`).
- C2 Control: `corpus/evidence/round74/c2-control-malformed-tuple.txt` (discriminating fixture).

## Census

Census validate command at both ends:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`.
Before: 241 rows, exit 0, 25 W04 warnings (`corpus/evidence/round74/census-before.txt`).
After: 242 rows, exit 0, 25 W04 warnings (`corpus/evidence/round74/census-after.txt`).
Row count verified: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` -> 242.
