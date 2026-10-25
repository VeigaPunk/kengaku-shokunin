# FRegistryS058 — independent falsification of registry row S058 (round 28)

Seat: KengakuR28.FRegistryS058 (author-side revenger, leaf member). Scope: **row S058 only**, under the frozen13/35 literal contract. No whole-registry truth claim and no whole-current-tree claim is made; S038/S050 material appears only as the disclosed separation scaffolding that bounds S058's environment.

## Inputs and identity

| Item | Value |
|---|---|
| Lane root | `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (read-only for this seat, except scratch + this report) |
| Baseline revision | `b9b24796277020d1b9b01923b45313d6a565e664` (object verified via `git cat-file -t`) |
| Current HEAD | `18b192266389e8d6c74d0e1f1f2db337739e63dd` |
| Population | `plans/fixtures/r28/registry/population.json`, sha256 `1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014` (independently recomputed; matches the checker's pin) |
| Contract | 13 source rows × 35 frozen knowledge paths, regex `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])`, raw-text literal counting, set-of-files semantics |
| Candidate | canonical `corpus/knowledge/webarena-task-spec-audit.md` is NOT admitted and is not among the 35 frozen paths — outside C2 and outside this seat's verdict |

Method: independent derivation with my own parser/regex (no import of `registry_check.py` or any production/alternate oracle); baseline rows and files read via read-only `git show b9b2479:…`. Delivered checker then run read-only (`--json`, `PYTHONDONTWRITEBYTECODE=1`) on production, on a full baseline export tree, and on scratch-mutated sandboxes. Scratch evidence: `.ufo/waves/round-28/scratch/KengakuR28.FRegistryS058/` (`derived-map.json`, `delivered-current.json`, `B1/B2/B3-*.json`, `E*v-verified.json`, sandbox dirs). No tool installs were needed (system `python3` + `git` only); no production bytes were mutated.

## Expected-before / current-after for S058

The S058 row is `corpus/SOURCES.md` line 80 in both trees and is **byte-identical baseline→final** (all 11 cells; immutable-cell delta ∅, mutable-cell delta ∅):

```
| S058 | inspect_ai pattern() no-match reasons (corrects S050 blanket reason) — https://github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py | code | A | … | pattern :86,:119–124 and scorer/_common.py:16–30; independent reread FSourceS050 | … | mined | 2026-10-21 | 2027-01-19 | corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md |
```

| Dimension | Expected-before (b9b2479) | Current-after (18b1922) |
|---|---|---|
| status / tier / kind | mined / A / code | mined / A / code (unchanged) |
| opened / recheck | 2026-10-21 / 2027-01-19 | 2026-10-21 / 2027-01-19 (unchanged) |
| used_by (parsed set) | `corpus/knowledge/extraction-policy-comparison.md`, `corpus/lessons/round-27.md` | identical (unchanged) |
| citing frozen files (my census) | `corpus/knowledge/extraction-policy-comparison.md` (mentions at lines 1, 18; 0 fenced) | same file; mentions now at lines 1, 18, 123, 126 (0 fenced) — the round28 errata lines add mentions inside an already-citing file, a set-level no-op |
| missing_used_by | ∅ | ∅ |
| per-row findings (my derivation) | ∅ | ∅ |
| per-row findings (delivered checker) | ∅ (inside baseline export B1: exit 1 driven solely by S038 `cited_not_mined`+`missing_used_by` and S050 `missing_used_by`; mismatch_sources=2; S058 clean) | ∅ (production run exit 0, mismatch_sources=0, finding_count=0) |
| delivered vs derived S058 map | identical on every field (status, citing_files, used_by, missing_used_by) | identical |

S058 was **not** one of the baseline-red rows, contributed no part of the S050 corrective-index reversal (its row never changed), and contributes nothing to the S038 drift (already disclosed in round27 — treated as given, not rediscovered). The B1→B2→B3 separation replay on scratch exports confirms the S058 slice: baseline red on exactly {S038, S050}; +S050-delta still red on S038; +S038-delta exit 0 — with S058 findings ∅ at every step and `reference_links=12` throughout.

## Exact effective denominator

- Per run: `source_rows_checked=13`, `knowledge_files_expected=35` → **455 row×file scans**; `reference_links=12` (S038: 1; S049–S059: 1 each; S060: 0 — uncited rejected, permitted).
- S058 specifically: 35 frozen files scanned for its row; **exactly 1 citing file** (4 of the 12 total links belong to other rows' sets; S058 contributes 1). 4 literal standalone mentions in the current citing file (2 at baseline), none inside code fences, none in the round28 lesson or any new round28 knowledge (those are outside the frozen 35 by contract).

## One row-specific falsifier (headline result)

**F-S058 — used-by overclaim invisibility.** In a scratch sandbox (population bytes verbatim, all used-by targets materialized), I deleted every literal S058 mention from the sole citing frozen file (`extraction-policy-comparison.md`, `S058`→`S958`, 4→0 mentions verified on disk). Delivered checker result: **exit=0, S058 `citing_files=[]`, `reference_links` 12→11, zero findings — while S058's used_by cell still asserts that exact file.** The S058 edge is therefore enforced one-directionally only: citations ⊆ used-by (violable, see below), never used-by ⊆ citations. A stale or overclaiming S058 used-by entry is unverifiable by construction. This is a declared contract boundary ("additional used-by paths permitted… not required to match exactly"), so it is recorded as a scoped limitation of what S058's green state proves — not a defect in the delivered instrument and not a repair request.

Counter-probes proving the green is failure-capable and matches the contract (each with on-disk precondition verification):

- **E2v** — S058 status `mined`→`queued`: `cited_not_mined` fires for S058 only; exit 1.
- **E3v** — S058 used_by drops the citing knowledge file: `missing_used_by` fires for S058 only; exit 1.
- **E5v** — the corrective S058 mention wrapped in a code fence (```` ```text ```` at line 18, verified on disk): the mention is **still counted** (citing set preserved, exit 0) — fence-inclusive literal counting confirmed live on the S058 edge, per the declared contract.

Anomaly disclosure: my first batch experiment cell produced stale outputs for the E4/E5 steps (all later outputs byte-identical to E1; B3's identity with E1 is legitimately expected because the checker output is set-based and the grafted baseline's reference sets coincide with current, but E4's was not). Those batch results are discarded and superseded by the isolated, on-disk-verified reruns above; B1–B3 remain as delivered-instrument outputs on faithful era-correct exports.

## Boundary statements

- S050's used-by addition is a literal corrective-reference index only; it reverses round27's lesson-only indexing decision without reviving S050 as source support. From the S058 side: the controlling row S058 is byte-unchanged, its single evidence edge pre-existed at baseline, and the errata block (lines 123–126) itself restates S058 as the authority. S058's clean state is independent of that reversal.
- No S058 evidence derives from S038's repair or from any dead-seat output; the S038 drift used here is the already-disclosed round27 fact, not a new discovery.
- No exploitation, browser action, network contact, or upstream-code execution occurred; upstream source identity inside row cells was not re-opened by this seat (the row records the independent reread by FSourceS050).

## VERDICT: PASS

Falsification of S058 produced no row defect: row bytes are immutable baseline→final; the single citing frozen file is covered by used-by in both trees; status/tier/kind enums are valid; no missing/corrective/code-reference finding exists in either direction (baseline and current); the delivered per-row output matches my independently derived map exactly; and the check is demonstrably failure-capable for S058's mutable cells. The one genuine boundary found (F-S058, used-by overclaim invisibility) is contract-declared and does not weaken any claim S058's green state makes. This verdict covers the S058 row slice only — not the candidate `corpus/knowledge/webarena-task-spec-audit.md`, not whole-registry truth, and not whole-current-tree consistency.
