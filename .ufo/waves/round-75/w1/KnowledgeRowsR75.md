# KnowledgeRowsR75 — scoped findings

## Behavior and axes

Coverage: drafted three knowledge index rows without changing production files. Calibration: separated indexing, recorded admission, triad presence and Q1 compliance. Frozen claims were read in full before any shell command; neither claim was reinterpreted or executed.

## Evidence and operations actually performed

All paths below are relative to `/home/vgpnk/Projects/shokunin/kengaku-shokunin` unless explicitly absolute. `read`/`grep` are tool operations with returned lines, not shell executions; no shell exit code is claimed for them.

- `read plans/round-75-claims.md` returned lines 1–128, including Amendment A1.
- `grep` of `corpus/README.md` with `instrument-registry-derivation|registry-argv-and-flag-audit|tb2-torch-tensor-parallel-offline|knowledge/.*\|` returned actual table rows at 920–922, as well as prose references at 768, 832 and 851. Therefore the requested missing set is historical, not missing in the inspected working copy.
- Shell command actually run, cwd lane root: `git show 43255758:corpus/README.md`, exit 0. Full captured output: `artifact://59656` (865 lines). A subsequent `grep` tool operation against that artifact using `^\| `knowledge/(instrument-registry-derivation|registry-argv-and-flag-audit|tb2-torch-tensor-parallel-offline)\.md`` returned `No matches found`. Thus all three exact table-row entries are absent at A1 despite existing prose references. Backticks in this displayed regex are literal pattern characters.
- `read` opened each of the three knowledge files from line 1, plus `grep` with `source:|verified-at:|recheck:|admission:|S235|S236|S237|S249|S250` over those files. Returned locations are recorded below.
- `grep corpus/QUALITY.md` for `Q1|source:|verified-at:|recheck:|admission` returned Q1 at 15–18: first three lines must be source, verified-at, recheck; recheck requires date/cadence and action. It also located Q21 at 237–246 requiring a pinned-source recheck to name its pin or repinning cadence.
- `grep` over `corpus/lessons/round-66.md` and `corpus/SOURCES.md` located S183 and the tensor lifecycle; a second, single-file lesson grep exposed the explicit admission text at 87 and R66-C1 landing verdict at 326. `read corpus/SOURCES.md:198:raw` returned the full S183 row.
- `grep corpus/SOURCES.md` returned S236 at 251 (SQLite amalgamation) and S237 at 252 (kv-store-grpc), neither a tensor grader source. The live README tensor row at 922 instead says `S235–S237`; this citation mismatch was sent directly to the integration owner.

## Per-file admission and triad findings

| File under `corpus/knowledge/` | Recorded admission | Triad presence and Q1 boundary |
|---|---|---|
| `instrument-registry-derivation.md` | Held: line 6 explicitly says `admission: hold`; line 10 says not an admission attestation. | All three fields occupy lines 1–3 in required order. Source S249 includes URL/anchors; verified-at gives ISO date and explicitly limits its revision statement; recheck includes `on-release` and concrete actions. Opening-triad structural requirements present; no independent source-opening certification claimed. |
| `registry-argv-and-flag-audit.md` | Held: line 11 says `admission: hold`, reiterated at 37. | All three fields exist, but verified-at/recheck are lines 8–9 and source is line 16; first three lines are YAML delimiter/title/branch, not the Q1 triad. `recheck: on-release` supplies cadence but no action. Hence triad fields present, Q1 placement/action requirements not met. |
| `tb2-torch-tensor-parallel-offline.md` | Recorded admitted, not newly admitted by this seat: no `admission:` marker returned anywhere in the file; round-66 lesson line 87 calls it “the new knowledge entry admitted above,” and line 326 records R66-C1 admitted on the amended counter. These are recorded decisions, not an independent Q10/Q13/Q14 audit. | All three fields occupy lines 1–3 in required order. Source S183 names the pinned URL and exact anchors. Recheck line 3 is only a command: no date/cadence (Q1), and no pin/repinning cadence (Q21). Thus the triad is present but not full Q1/Q21 compliance. |

A README row indexes `instrument-registry-derivation.md` and does not admit it.
A README row indexes `registry-argv-and-flag-audit.md` and does not admit it.
A README row indexes `tb2-torch-tensor-parallel-offline.md` and does not admit it.

## Findings and integration disposition

1. **Live-state conflict:** all three requested table rows are already present in the observed README (920–922); append would duplicate them. Use the proposal as a comparison/replacement, not a second set of rows. A1 absence was separately checked from committed bytes.
2. **Wrong primary-source attribution:** observed README row 922 cites `S235–S237`; tensor entry line 1 and SOURCES row 198 identify S183. Proposed tensor row uses S183 plus the pinned grader anchors. S236 and S237 describe unrelated sources.
3. **Held status must survive indexing:** explicit holds on the two registry candidates are retained in the proposed primary-source cells.
4. **Triad presence is weaker than Q1 compliance:** argv candidate fails placement/action; tensor entry lacks recheck date/cadence and pinned revision. No knowledge-file repairs were authorized or attempted.

## Gates, touched surfaces and limits

Written only:
- `.ufo/waves/round-75/w1/index-rows-knowledge.md` — three proposed rows and indexing/admission disclaimers.
- `.ufo/waves/round-75/w1/KnowledgeRowsR75.md` — this report.

No product edits, commits, pushes, git/jj mutations, installs, runtime launches, fixture creation, or subagents. No scratch directory was created, so none remains from this seat. R75-C1/R75-C2 gates, source fetches, receipt replay and admission-commit review were not run; this report supplies no passing gate or fresh execution evidence. README observations name inspected working-copy lines, not a clean revision-bound receipt. Source and admission defects are reported for the canonical judge without changing frozen predicates.

## Self-evaluation

Accuracy 4/5: evidence distinguishes recorded admission from independent certification; live README was not revision-stamped. Completeness 5/5: three rows, three admission/triad assessments and three non-admission sentences supplied. Clarity 4/5: evidence ledger is longer than the proposal because it separates A1 from live state. Actionability 5/5: replacement-ready rows avoid duplication and correct S183 attribution. Conciseness 4/5: exact evidence adds length. Mean 4.4/5. Highest-impact improvement is an integration-owner revision-stamped gate run after landing; this seat does not claim one. User-agreement self-check: the scoped deliverables and known limits are explicit.
