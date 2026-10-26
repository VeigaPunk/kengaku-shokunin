# R38MergeRescreen — merge/kengaku re-screen (round 38, wave 1)

Seat: scout, read-only. `/home/vgpnk/Projects/shokuknow/merge/kengaku/` was only read. Nothing adopted; no lane file edited. Only writes: this report and `.ufo/waves/round-38/build/R38MergeRescreen/{reg-ids,staged-ids,collisions,c2-ids,c2-collisions}`. Scratch `/fast/scratch/hyaku/kengaku-r38/R38MergeRescreen` was used for two live fetches and removed. Tooling installed: none.

Axes: (a) did the package change since the round-37 screen; (b) id-space collision; (c) quarantine slice; (d) per-entry verdict against PROVINCE.

## 1. Did the package change since round 37? No (bytes identical).

```
$ git -C /home/vgpnk/Projects/shokuknow log -1 --format='%H %ci %s' -- merge/kengaku
ba6779f0160d12dd7373627e00291d6d5e3ba7ee 2026-10-24 10:50:02 -0300 Round 12 complete: 32/32 members, 119 rows, 77 entries, 263 quotes with 0 absent
$ git -C … log --format='%h' -- merge/kengaku   # 8 commits, newest ba6779f0, oldest d9583b5a (round-6 campaign)
$ stat -c '%y %n' SOURCES.append.md MERGE-REPORT.md MERGE-REPORT.json   # all 2026-10-24 23:33:20
$ sha256sum SOURCES.append.md MERGE-REPORT.json knowledge/corpus/knowledge/grader-predicate-input-types.md
a46458851f933edb352c517cb36fe97ad830054e1f0139bdc0a32cbf6c3eb73b  SOURCES.append.md
c47fbe68ceacf0d21258dad9938146e325e4c7e68752928ef6644c23f53dff23  MERGE-REPORT.json
350e2677f920dc5779d4f4a6e14d283f1b9e89d2a3432708021e235a0f11fed0  grader-predicate-input-types.md
```
All three digests are byte-equal to `R37ScoutMergePkg.md` §6 (this closes the round-37 "[INFERENCE: unchanged]", which had no digest baseline for round 36 but now has one for round 37). `staged-ids` sha256 `2df53989…14d3` equals round 37's (`diff` → `staged-same-as-r37`). Shokuknow HEAD is `8b94c5c1` (2026-10-24 11:02); no commit touches `merge/kengaku` after `ba6779f0`.

**New observation (not in the r37 report):** the committed state is the round-12 package. The round-13..16 staging is **uncommitted** in shokuknow's working tree: `git status --short merge/kengaku` → 3 ` M` (`MERGE-REPORT.json/.md`, `SOURCES.append.md`; `git diff --stat`: 288 insertions, 5 deletions) and 19 `??` knowledge files (65 files total under `knowledge/`). So `git log -1 -- merge/kengaku` names a commit that does not contain the bytes screened. The package identity for this screen is therefore the sha256 above, not the commit hash. Also `MERGE-REPORT.md` still says "lane registry currently holds **76** rows; first staged id is S077" — stale; the lane now holds S001–S114.

## 2. id-collision check (0–3 leading spaces)

Guard script: `.ufo/waves/round-36/assimilation/id-collision-check.sh` (anchor `^ {0,3}\|[[:space:]]*S[0-9]{3,}`), run with `A=` pointed at my dir.

```
$ sh id-collision-check.sh --selftest
SELFTEST reg=[S002 S900 ] staged=[S002 S901 ] indent=[S004 ] collisions=[S002 ] bad-anchor-collisions=0
SELFTEST guard-ok
$ A=…/R38MergeRescreen sh id-collision-check.sh
reg-ids=107 staged-ids=175 collisions=31        (script exit 3 = collisions present, as designed)
```
sha256: `reg-ids` 458c1c70…9a49a59 (107), `staged-ids` 2df53989…be14d3 (175), `collisions` 474fab5b…9ad0ae2 (31), `c2-collisions` 512037e2…0bc4.

- vs round 37: reg-ids 103 → 107 (+S111 S112 S113 S114 — the round-37 C2 rows S111–S113 and the lane's TB2.1 issue-133 row S114); collisions 27 → 31, the four new ones being exactly S111–S114 (`diff` of reg-ids and collisions each shows only those 4 added). Full collision set: S077–S086, S090–S094, S097, S100–S114.
- Staged S111–S114 are different documents from the lane's: staged S111/S115/S116 are GENIAC phase-2 METI/archive rows, staged S114 is own-work `lanes/kengaku/round5/toolathlon-grader-tabulation.md`; lane S111–S113 are TB2 configure-git-webserver rows, lane S114 the TB2.1 issue #133.
- **Round-38 C2 ids collide with staged rows.** The seat brief reserves S115/S116 for the build-pmars rows. `comm -12 c2-ids staged-ids` → **S115, S116** (both present in staged). `grep -cE '^ {0,3}\|[[:space:]]*S11[56]' corpus/SOURCES.md` → 0, so there is no *registry* collision at landing (C2 rows are lane-authored; the staged package is never appended wholesale). Consequence: any later adoption of staged rows must renumber past **S116** (round 37 said S113; round 36 said S110). Renumbering is already the lane practice (`benchmark-grader-semantics.md` records "ids renumbered round 33 — the staged package's S094→S103").

## 3. Quarantine slice (`corpus-expansion-1/absent-defect-register.md`, lane `kengaku`)

Register: 375 lines, mtime 2026-10-24 08:37, sha256 `5afe1810…d833`, last commit `d4ab45f2`; totals "rows with at least one ABSENT quote: 194", "ABSENT quotes: 324" (lines 16-18). `kengaku` count = **2** (line 252 `| \`kengaku\` | 2 |`; `awk -F'|' '$2 ~ /kengaku/'` shows 2 rows). Slice (identical to `round-36/assimilation/quarantine-slice`: `S091`, `S105`):

| staged id | round | class | source | quote probe | entry that cites it |
|---|---|---|---|---|---|
| S091 | round2 | `payload-absent` | `https://jpn.nec.com/techrep/journal/g23/n02/230212.html` | register line 101: the checked span is a `python` extractor over `/tmp/keng_s091.html`, not a quote | `cjk-eval-journal-access.md` (sole `source:` first line S091) |
| S105 | round3 | `payload-absent` | `web.archive.org/web/20251118034714/…geniac/selection_1/result_1/index.html` | register line 102: `指定されたページまたはファイルは存在しません` ("page does not exist") | `cjk-benchmark-governance-2026-10-23.md` (`source: S105`, line 3; section "S105 — the hold-out protocol", line 62) |

Both quarantined rows share ids with held lane rows that are unrelated documents (lane S091 = ABC checklist arXiv 2507.02825; lane S105 = TB2 protein-assembly `test_outputs.py`). The register's section 3 (NEVER CHECKED) names no kengaku row (`grep -n -i -E 'kengaku|S091|S105'` over lines 256-375 → none). **No C2-relevant row is in the slice.** Slice rows are not adoptable as staged: S105's "quote" is an error page for a withdrawn METI page.

## 4. Verdicts (65 staged entries; grouped where the facts are identical)

Source-kind breakdown computed over each entry's `source:` ids (python over `SOURCES.append.md`): rows by kind docs 64, paper 36, code 21, own-work 20, tool 14, dataset 11, spec 9. C2 search over the whole package: `grep -rli -E 'pmars|build-pmars|dlopen|\bldd\b|libX11|X11' .` → no hit. Nothing staged supplies a C2 fact; C2 stays self-sourced (S115/S116 are lane-authored).

| # | Entry (staged rows) | Verdict | PROVINCE scope reason (observed) | Flip condition |
|---|---|---|---|---|
| 1 | `benchmark-card-field-schema-2026-10-23.md` (S122, S123, S124) | **ADMIT-candidate** (not this round) | In scope: PROVINCE Frontier names "contamination transparency cards" (`PROVINCE.md:123-127`); the lane already holds the amendment entry `contamination-transparency-card.md`, and this entry is its published-forms ground. Sources are public: AI Alliance template page, a commit-pinned GitHub spec (`4dba1ed9…`), GEM 2026 PDF; no own-work row; not in the quarantine slice; no lane `S122–S124`. Static reading of published maintainer artefacts, same shape as the round29-attempt-2 clause (`PROVINCE.md:215-222`). | Rows renumbered past S116; quotes re-run in-lane at the pins (not copied); a new dated PROVINCE paragraph in the form of round35-37 saying it records published designs only, not contamination measurement or hosted judges. A claim must name it (r38 claims are frozen to C1/C2). |
| 2 | `benchmark-card-adoption.md` (S135–S139) | **ADMIT-candidate** (after #1) | In scope, same frontier line. Live check today, outside the frozen claims: `curl -sS -L …/evaluations/langfair/` → HTTP 200, 23083 bytes; the S136 recheck span `not as a benchmark or evidence of clinical readiness` and the pin `afd6dc0` both present; `…/evaluations/evaluations/` → 200, 22329 bytes, `LangFair Evaluation Card` ×2 and `Benchmark Card Template` ×3 (S135 recheck expects 1 for the former — grep counted occurrences, not lines). Public rows only except S139 (arXiv HTML, tier B). Its `ground:` line narrows round-6 claim N19 ("adoption is unproven"), which lives in #1's family, so it lands after #1. | As #1, plus S137/S138/S139 quotes re-run (not fetched today) and the 180d `recheck` date re-based. |
| 3 | Remaining card/maintainer/OSF/post-5G family (`card-*`, `author-approved-*`, `benchmark-card-{maintenance,author-approval,shape}*`, `maintainer-*`, `osf-*`, `post5g-*`, `programme-side-*`, `preregistration-*`, `contamination-mitigation-*`, `per-benchmark-contamination-*`: ~35 files) | **HOLD** | Same card frontier, but they build on #1/#2 chains (`-r13…r16` are re-checks of earlier entries) and mix in own-work rows (`grep` kinds: 20 own-work rows total, e.g. `benchmark-card-maintenance-r14` has 2, `programme-side-disclosure-record-r15` has 2). `per-benchmark-contamination-verdicts` and `contamination-mitigation-*` edge into contamination *measurement*, which PROVINCE refuses (`PROVINCE.md:238-240`). Not screened line by line. | #1/#2 land first; each entry then needs its own in-lane quote run and a PROVINCE sentence; own-work rows replaced by in-lane receipts. |
| 4 | `grader-predicate-input-types.md` (S143, S144) | **HOLD** (unchanged bytes) | sha256 `350e2677…` identical to round 37; the three round-36 defects stand (row-cell "never bare strings", `23 of 38` denominator, `compare_rating` narrative). S144 is own-work. No r38 claim names it. | Reconciled amendment with the lane's own receipt on the denominator. |
| 5 | `benchmark-grader-integrity-models-2026-10-23{,b}.md` (S101, S102, S107, S108) | **HOLD** | Nearest to TB2 (M1 shared-environment verification), but its ids are burned in the lane: lane S101/S102 are `REJECTED: duplicate id` markers and lane S107/S108 are TB2 rows. Collisions confirmed in `collisions`. Overlaps held `benchmark-verifier-execution-model.md`. | A claim opening the Harbor/SWE-bench Pro/Toolathlon sources at pins, rows re-ided past S116. |
| 6 | `judge-calibration-thresholds.md`, `judge-meta-evaluation-2026-10-23{,b}.md` (S078, S103, S110) | **HOLD** | PROVINCE says hosted judges stay open and applies "judge calibration" only to the lane's own outputs (`PROVINCE.md:125-127,239-240`); staged S078/S103/S110 collide with lane TB2 rows. | A claim that applies the calibration thresholds to a lane artefact. |
| 7 | CJK/GENIAC/disclosure entries (`cjk-*`, `geniac-*`, `eastern-*`, `japanese-*`, `disclosure-vocabulary-bilingual`: ~12 files) | **HOLD**, except below | Evaluation-venue and governance material for Chinese/Japanese programmes; no PROVINCE surface or frontier line names it; third-party programme governance, not the lane's measured-eval domain. `cjk-eval-journal-access.md` and `cjk-benchmark-governance-2026-10-23.md` are **REFUSE** (row 9). | A claim naming CJK governance as lane scope, plus a PROVINCE paragraph. |
| 8 | `toolathlon-grader-contract-2026-10-23.md` (S114), `toolathlon-grader-behaviour-probe-2026-10-23.md` (S130) | **REFUSE** (unchanged r36/r37) | Sole source is own-work in shokuknow (`lanes/kengaku/round5…6`); campaign tools forbidden (`§10`); S130 denominator 38 vs rows 13+23+1 = 37. | In-lane re-derivation from the pinned tree with the lane's receipt. |
| 9 | `cjk-eval-journal-access.md` (S091), `cjk-benchmark-governance-2026-10-23.md` (S105) | **REFUSE** (**new this screen**) | Each cites a row in the quarantine slice (§3): S091 `payload-absent`, S105 an archived METI "page does not exist" error. A quote the checker could not find cannot anchor an entry. | The row's quote re-found at a live or archived source, with a new id. |
| 10 | Own-work grader lineage: `grader-fixture-probe-stage3`, `grader-fixture-coverage`, `spreadsheet-grader-fixtures`, `grader-sheet-checks-real-pandas-r16`, `grader-candidate-coverage{,-r13,-r14,-r15}`, `grader-candidate-reconstruction` (S155–S247 range) | **REFUSE** (unchanged) | Own-work locators `lanes/kengaku/round8…16` inside shokuknow; Toolathlon-only; no TB2 or service fact; supersession chain (stage 3 → 4). | In-lane re-runs with in-lane receipts, per entry. |
| 11 | `terminal-bench-release-identity.md` (S092, S100) | **REFUSE** (unchanged) | Cites S092 and S100, both held; adds no ground. | A release-identity fact no held entry states, with a located quote at the pin. |
| 12 | `benchmark-grader-semantics.md`, `benchmark-task-validity-checklist.md`, `benchmark-verifier-execution-model.md`, `contamination-transparency-card.md` | **REFUSE** (already adopted, adapted) | **Corrects the r37 INFERENCE.** r37 said lane files are "supersets" of the staged ones; a line test says otherwise: `grep -vxFf lane staged` → staged lines absent from lane file: 72/95, 57/73, 63/87, 70/92. Headings and source counts show these are rewrites: same `source:` counts (3/5/3/6) and the lane file says "ids renumbered round 33 — the staged package's S094→S103". They are adopted with renumbered rows, so adopting the staged copy would fork them. | A staged section the held file lacks, shown by section-level diff. |

Totals over the 12 verdict rows: **admit 2 (rows 1–2), hold 5 (rows 3–7), refuse 5 (rows 8–12)**. Refuse rows 8 and 11 are unchanged from round 37; row 9 and the correction in row 12 are new this screen; admit is new relative to round 37, which gave 0 admits (`R37ScoutMergePkg.md` §4).

Admit means *candidate for a later round*, not landing now: the round-38 claims are frozen to C1/C2 and neither names a card entry, so nothing is appended this wave.

## 5. What changed for the L1 vs round 37

1. Package bytes: unchanged (three sha256 equal; staged-ids equal). Only new fact about the package: its round-13..16 content is uncommitted in shokuknow, and its report's "76 rows" is stale.
2. id floor: C2's S115/S116 are themselves in the staged package (`c2-collisions` = S115 S116). The flip floor for adopting staged rows moves from "past S113" to "past **S116**". Collisions 27 → 31.
3. Quarantine: lane `kengaku` slice is 2 rows (S091, S105), unchanged; each is cited by exactly one staged entry, both now REFUSE.
4. First admit candidates (card family, rows 1–2), with the live S135/S136 span check as evidence.
5. Round-37 inference on the four same-path entries is replaced by evidence (row 12).

VERDICT: merge-rescreen-admit-2-hold-5-refuse-5
