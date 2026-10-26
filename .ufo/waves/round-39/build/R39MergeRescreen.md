# R39MergeRescreen — merge/kengaku re-screen (round 39, wave 1)

Seat: scout, read-only. `/home/vgpnk/Projects/shokuknow/merge/kengaku/` and the register were only read. Nothing adopted; no lane file edited. Writes: this report and `.ufo/waves/round-39/build/R39MergeRescreen/{reg-ids,staged-ids,collisions,quarantine-slice,entry-map.tsv,entry-verdicts.tsv,live-fetch.txt,scratch-reg.md,scratch-collisions}`. Scratch `/fast/scratch/hyaku/kengaku-r39/R39MergeRescreen` held a classifier script, scratch-registry fixtures and live-fetch bodies; removed by trap. Tooling installed: none.

Axes: (a) did the package change since round 38; (b) id-space collision; (c) quarantine slice; (d) per-entry verdict against PROVINCE.

## 1. Did the package change since round 38? No (bytes identical)

```
$ git -C /home/vgpnk/Projects/shokuknow log -1 --format='%H %cI' -- merge/kengaku
ba6779f0160d12dd7373627e00291d6d5e3ba7ee 2026-10-24T10:50:02-03:00
$ sha256sum SOURCES.append.md MERGE-REPORT.json knowledge/corpus/knowledge/grader-predicate-input-types.md
a46458851f933edb352c517cb36fe97ad830054e1f0139bdc0a32cbf6c3eb73b  SOURCES.append.md
c47fbe68ceacf0d21258dad9938146e325e4c7e68752928ef6644c23f53dff23  MERGE-REPORT.json
350e2677f920dc5779d4f4a6e14d283f1b9e89d2a3432708021e235a0f11fed0  …/grader-predicate-input-types.md
$ stat -c '%y %n' SOURCES.append.md MERGE-REPORT.md MERGE-REPORT.json    # all 2026-10-24 23:33:20 -0300
$ git -C shokuknow log -1 --format='%h %ci'                              # 8b94c5c1 2026-10-24 11:02:02 -0300
$ git status --short merge/kengaku | awk '{print $1}' | sort | uniq -c   # 19 ??, 3 M
$ git diff --stat -- merge/kengaku | tail -1                             # 3 files changed, 288 insertions(+), 5 deletions(-)
$ find merge/kengaku/knowledge -type f | wc -l                           # 65
```

- Same commit `ba6779f0` and same three sha256 as `R38MergeRescreen.md` §1 (a46458…, c47fbe…, 350e26…); `staged-ids` sha256 `2df53989…cdf5e1c` equals round 38's (`diff` shows `same`). Mtimes did not move; shokuknow HEAD did not move.
- The round-38 caveat stands unchanged: the committed state is the round-12 package; round 13–16 staging is uncommitted in the shokuknow tree (3 ` M`, 19 `??`). The identity of the screened package is the sha256, not `ba6779f0`. `MERGE-REPORT.md`'s "76 rows / first staged id S077" is still stale.
- 65 entry files, 175 staged rows, every staged row cited by at least one entry (`entry-map.tsv`: 65 entries; rows cited 175; rows total 175; uncited 0).

## 2. id-collision check (0–3 leading spaces)

Guard: `.ufo/waves/round-36/assimilation/id-collision-check.sh` (anchor `^ {0,3}\|[[:space:]]*S[0-9]{3,}`; exit 3 = collisions, 2 = input absent/anchor-silent), run with `A=` pointed at this seat's dir:

```
$ A=…/round-39/build/R39MergeRescreen sh id-collision-check.sh
reg-ids=109 staged-ids=175 collisions=33        (exit=3, as designed)
```

sha256: `reg-ids` 47113e4b…c20cc7 (109), `staged-ids` 2df53989…5e1c (175), `collisions` 761e161c…55b9bd (33).

- vs round 38 (`diff` of each file): `staged-ids` same; `reg-ids` 107 → 109, added exactly **S115, S116**; `collisions` 31 → 33, added exactly **S115, S116**. Those are the lane's round-38 build-pmars rows (`tb2-build-pmars-grader.md`, PROVINCE round-38 paragraph) — lane-authored, a different document from staged S115 (GENIAC METI row) and S116. Round 38 had predicted this pair (`c2-collisions`).
- Full collision set: S077–S086, S090–S094, S097, S100–S116 (10+5+1+17 = 33). The lane registry's highest id is S116 (`grep -oE` over `corpus/SOURCES.md`, tail: S112–S116; `git status --short corpus/SOURCES.md` clean). **Floor for any later staged-row adoption: renumber past S118**, because round 39's own claims reserve S117 (`tests/test_outputs.py`) and S118 (`instruction.md`) for the git-leak-recovery grader. Round 38 said S116; round 37 S113; round 36 S110. [INFERENCE: S117/S118 are not yet in the registry — `reg-ids` ends at S116 — so the check will show 35 collisions once the L1 lands them; staged ids reach S251, so S117, S118 will collide with staged S117, S118.]
- Guard proof on a scratch registry with an indented row (the script's own `--selftest` hard-codes `mktemp -d /tmp/…`, forbidden by the scratch directive, so it was not run; the same fixture was built under the scratch dir and fed through the real script via `REG=`/`STAGED=`/`A=`):

```
$ printf '  | S002 | indented collision bait | code |\n| S900 | control | code |\n' > $S/reg.md
$ printf '| S002 | staged twin | code |\n| S901 | no twin | code |\n' > $S/staged.md
$ printf '    | S003 | four-space | code |\n   | S004 | three-space | code |\n' > $S/indent.md
$ A=$S/a REG=$S/reg.md STAGED=$S/staged.md sh id-collision-check.sh
reg-ids=2 staged-ids=2 collisions=1        (exit=3)         $S/a/collisions → S002
$ grep -oE '^[|][[:space:]]*S[0-9]{3,}' $S/reg.md | grep -oE 'S[0-9]+'   # anchor WITHOUT indent allowance → S900 only: S002 missed
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' $S/indent.md                  # → "   | S004" (3-space parses; 4-space S003 does not)
$ REG=$S/nope A=$S/a sh id-collision-check.sh
REFUSED: input absent: …/nope   (exit=2)
```

The indented `  | S002 |` row collides under the 0–3-space anchor and would have been false-green under the bare `^\|` anchor; a missing registry refuses rather than reporting 0 collisions. Copies: `scratch-reg.md`, `scratch-collisions` (= `S002`).

## 3. Quarantine slice (`absent-defect-register.md`, lane `kengaku`, data rows only)

Register: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`, 375 lines, mtime 2026-10-24 08:37:00, sha256 `5afe1810…d833`, last commit `d4ab45f2` — identical to round 38. Section headings (`grep -nE '^## '`): Totals 16, Rows 25, By lane 232, NEVER CHECKED 256.

```
$ grep -cE '^\| `[a-z0-9_-]+` \| round[0-9]+ \| S[0-9]{3,} \|' register     # 194  (= register "rows with at least one ABSENT quote: 194")
$ grep -E '^\| `kengaku` \| round[0-9]+ \| S[0-9]{3,} \|' register | awk …   # → quarantine-slice
S091 round2 payload-absent
S105 round3 payload-absent
```

- By-lane table line 252 `| \`kengaku\` | 2 |` agrees with the data-row derivation (2). Slice ids equal `round-36/assimilation/quarantine-slice` (`slice-ids-same-as-r36`).
- Section 3 (NEVER CHECKED, lines 256–375) names no kengaku row (`grep -n -i -E 'kengaku|S091|S105'` over those lines → none).
- Staged S091 = NEC techrep page (the checked "quote" is a python extractor over `/tmp/keng_s091.html`, register line 101); staged S105 = archived METI GENIAC page whose "quote" is the error text `指定されたページまたはファイルは存在しません` (line 102). Lane S091 (ABC checklist arXiv 2507.02825) and lane S105 (TB2 protein-assembly `test_outputs.py`) are unrelated held rows (`grep` over `corpus/SOURCES.md` lines 104, 120). Entries citing the slice: `cjk-eval-journal-access.md` (S091), `cjk-benchmark-governance-2026-10-23.md` (S105).
- **No git-leak-recovery-relevant row is in the slice.**

## 4. Verdicts — per entry (65), reproducible in `entry-verdicts.tsv`

Method: each entry's `source:` first-lines (`entry-map.tsv`: sources, kind, collision, quarantine, own-work count) joined to the staged row kinds; verdicts from PROVINCE scope. C2 search over the whole package: `grep -rli -E 'git-leak|leak-recovery|reflog|git gc|git filter|filter-branch|dangling|secret' merge/kengaku` → no output, rc=1. Nothing staged supplies a git-leak-recovery fact; C2 stays self-sourced (S117/S118 lane-authored). Own-work rows by entry-source lines: 20 (same as round 38).

Counts: **admit 2, hold 42, refuse 21** (= 65). Round 38 counted by verdict group rows (2/5/5); the same groups hold now (admit rows 1–2, hold rows 3–7, refuse rows 8–12) — the only change inside them is the three-entry move below.

| Verdict | Entries | PROVINCE scope reason (observed) | Flip condition |
|---|---|---|---|
| **ADMIT-candidate (2)** | `benchmark-card-field-schema-2026-10-23` (S122–S124); `benchmark-card-adoption` (S135–S139; after the first) | In scope: PROVINCE Frontier names "contamination transparency cards" (`PROVINCE.md:122-127`); public sources only, no own-work row, none in the quarantine slice, none cited id collides. Live today outside the frozen claims: S122 page HTTP 200, 25177 bytes, `Benchmark Card Template` present (7 occurrences); S123 pin `4dba1ed9…` HTTP 200, 2181 bytes, `Contamination Disclosure v1.1` ×1; S124 GEM PDF HTTP 200, 819775 bytes (`live-fetch.txt`; PDF text not extracted). Candidate for a later round only: neither round-39 claim names a card entry. | Rows renumbered past S118; quotes re-run in-lane at the pins; a dated PROVINCE paragraph in the round35–38 form. |
| **HOLD (42)** | Card/maintainer/OSF/post-5G family (27): `author-approved-benchmark-cards`, `benchmark-card-author-approval-r15`, `benchmark-card-maintenance-r13`, `-r14`, `benchmark-card-shape-and-pending-outputs-r15`, `card-authorship-and-attachment`, `card-completeness-and-verification`, `card-design-arbitration`, `card-provenance-and-preregistration`, `card-publication-contracts`, `contamination-mitigation-comparative-evidence-2026-10-23`, `maintainer-contamination-disclosure`, `maintainer-disclosure-record-r13`, `-r14`, `maintainer-protocol-and-archived-listing`, `osf-registration-camera-ready-status`, `osf-registration-page-r13`, `-r14`, `osf-registration-publication-state`, `per-benchmark-contamination-verdicts-2026-10-23`, `post5g-archive-coverage-r13`, `post5g-archive-coverage`, `post5g-plan-addresses`, `post5g-plan-archive-coverage`, `post5g-plan-current-revision`, `post5g-revision-attestation-r15`, `preregistration-and-osf-identifier` | Same card frontier, but they build on the two admit-candidates (r13–r16 re-checks of earlier entries). `-maintenance-r14` and `-shape-and-pending-outputs-r15` carry own-work rows (S218/S219; S242). `contamination-mitigation-*` and `per-benchmark-contamination-verdicts` edge into contamination *measurement*, which PROVINCE refuses (`PROVINCE.md:238-240`). Not screened line by line, as in round 38. | Admit-candidates land first; each entry's own-work rows replaced by public rows; measurement edge removed or scoped. |
| | `grader-predicate-input-types` (S143, S144) | sha256 `350e2677…` unchanged; the round-36 defects stand (row-cell "never bare strings", `23 of 38` denominator, `compare_rating` narrative); S144 own-work. | Reconciled amendment with the lane's own receipt. |
| | `benchmark-grader-integrity-models-2026-10-23`, `…23b` (S101, S102, S107, S108) | Nearest to TB2 verifier-environment ground, but all four ids are burned in the lane (lane S101/S102 are `REJECTED: duplicate id` markers; S107/S108 TB2 rows); overlaps held `benchmark-verifier-execution-model.md`. | A claim opening the Harbor/SWE-bench Pro/Toolathlon sources at pins; rows re-ided past S118. |
| | `judge-calibration-thresholds`, `judge-meta-evaluation-2026-10-23`, `…23b` (S078, S081, S087, S103, S110) | PROVINCE keeps hosted judges open and applies "judge calibration" only to the lane's own outputs (`PROVINCE.md:124-127`); S078/S081/S103/S110 collide with lane rows. | A claim applying the thresholds to a lane artefact. |
| | CJK/GENIAC/disclosure (9): `cjk-benchmark-governance-2026-10-23b`, `…23c`, `cjk-dataset-documentation-standard-2026-10-23`, `cjk-dataset-standard-status-2026-10-23`, `cjk-eval-venue-access`, `disclosure-vocabulary-bilingual`, `eastern-conflict-of-interest-guidance-r16`, `geniac-phase2-terms-2026-10-23`, `japanese-model-card-governance-r16` | Third-party evaluation-programme governance for Chinese/Japanese venues; no PROVINCE surface or frontier line names it. (`cjk-eval-venue-access` cites S084–S086, which collide with lane rows.) | A claim naming CJK governance as lane scope plus a PROVINCE paragraph. |
| **REFUSE (21)** | Already adopted in adapted form (4): `benchmark-grader-semantics`, `benchmark-task-validity-checklist`, `benchmark-verifier-execution-model`, `contamination-transparency-card` | Same file names as lane entries; the lane copies are rewrites under renumbered ids (round 38 line test: staged lines absent from lane 72/95, 57/73, 63/87, 70/92); adopting the staged copy forks them. Collisions in `collisions` (S077–S080, S090, S092–S094, S097, S100, S081–S086). | A staged section the lane file lacks, shown by section-level diff. |
| | Quarantine (2): `cjk-eval-journal-access` (S091), `cjk-benchmark-governance-2026-10-23` (S105) | Each cites a row in the §3 slice (`payload-absent`); a quote the checker could not find cannot anchor an entry. | Quote re-found at a live or archived source, new id. |
| | Toolathlon own-work (2): `toolathlon-grader-contract-2026-10-23` (S114), `toolathlon-grader-behaviour-probe-2026-10-23` (S130) | Sole source is own-work inside shokuknow (`lanes/kengaku/round5…6`); campaign tools forbidden; S130 denominator 38 vs rows 13+23+1 = 37. | In-lane re-derivation from the pinned tree with the lane's receipt. |
| | Own-work Toolathlon lineage (9): `grader-candidate-coverage`, `-r13`, `-r14`, `-r15`, `grader-candidate-reconstruction`, `grader-fixture-coverage`, `grader-fixture-probe-stage3`, `spreadsheet-grader-fixtures`, `grader-sheet-checks-real-pandas-r16` | Locators `lanes/kengaku/round8…16` inside shokuknow; Toolathlon-only; no TB2 or service fact; supersession chain. | In-lane re-runs with in-lane receipts, per entry. |
| | `terminal-bench-release-identity` (S092, S100) | Cites only S092/S100, both lane-held; adds no ground. | A release-identity fact no held entry states, with a located quote at the pin. |
| | **Moved from HOLD (round 38 group row 3) — 3 entries:** `osf-registration-camera-ready-r15` (S239), `post5g-archive-coverage-r14` (S231), `programme-side-disclosure-record-r15` (S243, S244) | New this screen: every `source:` row is kind `own-work`, a saved artefact under `/home/vgpnk/Projects/shokuknow/lanes/kengaku/round14…15/` (rows S231, S239, S243, S244 locators, `SOURCES.append.md`). Same rule as the Toolathlon refusals above: a shokuknow-internal file is not a lane-fetchable source. | Public source re-fetched in-lane, new row, entry re-derived. |

## 5. What changed for the L1 vs round 38

1. Package bytes: unchanged (three sha256 and `staged-ids` equal). Same uncommitted-working-tree caveat; same stale "76 rows".
2. id floor: lane registry now S001–S116 with two lane-authored collisions added (S115, S116; collisions 31 → 33). With round 39's reserved S117/S118, any later adoption of staged rows renumbers past **S118**.
3. Quarantine slice: unchanged, S091 and S105, derived from data rows only (register sha256 identical).
4. Verdicts, per entry: admit 2 / hold 42 / refuse 21. Group verdicts equal round 38's; per-entry refinement moves three own-work-only entries hold → refuse. Admit candidates still not landable this wave.
5. No staged fact supports git-leak-recovery (C2 grep empty); nothing here bears on C1.

Unresolved: the `--selftest` mode of the guard writes under `/tmp` (hard-coded), so the equivalent fixture was reproduced under scratch rather than running that mode. S124's PDF body was not text-extracted (status/size only).

VERDICT: merge-rescreen-admit-2-hold-42-refuse-21
