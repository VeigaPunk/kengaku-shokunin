# ScribeR84 — scoped findings

Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Base `4087b2f8369fb0c317a8460725a607681ff2fd7f`, freeze `b12a9d46806cb8d69fe48fac0f4efff0b266e4c2`. 2026-11-04 UTC. Axes: coverage, calibration. Role: scribe, leaf seat (no subagent dispatch). Full report: `.ufo/waves/round-84/w1/ScribeR84/report.txt`.

Drafts written (all under `.ufo/waves/round-84/w1/ScribeR84/`), for the L1 to install:

| Draft | Lines | What it carries |
|---|---|---|
| `round-84.md` | 49 | the lesson body: header, `## Gate` (S271 source row + the successor-admission row for `tb2-code-from-image-offline.md`), `## Corrections (R83-V1, R83-V2)`, `## Mistakes`, `## Sources and frontier`, `## Frontier mining` |
| `scorecard-append.md` | 13 | `## Round 84 (hyaku run 15, attempt 1, 2026-11-04)`, the R84-C1/R84-C2 claim rows, and `### Planned (next steered round)` with two named gaps |
| `log-append.md` | 9 | the LOG.md round-84 entry, pointing at `plans/round-84-claims.md` and `.ufo/waves/round-84/w1/` |
| `readme-rows.md` | 46 | the `lessons/round-84.md` index row, the `corpus/evidence/round84/` bullet, the S271 knowledge-tie analysis, the `## Frontier` shape note |
| `report.txt` | — | the four drafts above with their line counts, plus the findings below |

No numeric result from a measurement appears in any draft, and no outcome is described as achieved; the figures are the L1's to fill from the committed receipts. The frozen claims doc's predicate, target, case table, control set and kill rule are untouched.

Findings that bear on the L1's integration:

1. **The Q13 checker's path rule is stricter than a `.md` suffix.** `plans/gate_timing_check.py` extracts a citation only from a five-component `.ufo/waves/round-<N>/<wave>/<name>.md` path, and counts it as a second-seat report only when the wave directory is `falsify` or matches `wave[-_ ]?0*2`. Measured in a scratch fixture: a cell citing `.ufo/waves/round-84/w1/ReviewerR84/report.md` extracts zero citations; a cell citing `.ufo/waves/round-84/w1/ReviewerR84.md` extracts the citation but is rejected because `w1` is not a second-wave directory; the same row exits 0 in a fixture whose second-wave directory is `falsify` with a registry naming the seat as `reviewer`. The lesson cites the L1's `.md` paths and adds a gate-timing note telling the installer to place the two reports where the committed checker resolves them.
2. **The checker needs the entry's `writer:` field and rejects a report that declares the candidate writer as its own.** Removing the entry's line-start `writer:` flips the admit to FAIL ("candidate has no committed writer: field"); a report containing `writer: KengakuR84` is rejected ("report writer/author declaration equals candidate writer"). The draft states that this round's repair adds `writer: KengakuR84` at entry line 4, and asks the re-read seats to declare the candidate writer in a field that is not a bare `writer:` line.
3. **R82-F1's blind shape is wider than its routed row's four rows.** A read-only pass with the lane's own parser finds 61 of 262 rows whose anchor cell carries a quote character that `QUOTE_RE` does not parse, including the round-83 rows `S267`–`S270`; the lane check still exits 0 with `live=0 cells=0`, green because blind. The SCORECARD planned item requires the repaired counter's red-before to be measured on the widened set.
4. **The next file-artifact member's ledger "no-blocker" cell is not an offline-replayability claim.** `git-multibranch` is the next unattempted file-artifact member in the ledger's own order; its captured grader needs a live git server and a live HTTPS service, so the blocker check is whether the ledger evidence is true. `fix-ocaml-gc` is named as the offline-reachable alternative.
5. **The S271 knowledge-tie is not a README row.** Round 84 admits no new knowledge entry, so a `knowledge/<file>.md` index row for S271 would be an orphan row under the parity gate; the tie lands on the S271 row's `used-by` cell in `corpus/SOURCES.md`.

No production file was edited, no counter, probe, selftest or mutant was run, no build/lint/test suite was executed, no git mutation was performed in the lane or the fleet root, and no tool was installed. The only lane tools run here were read-only inspections of committed bytes.
