# R43MergeRescreen — merge/kengaku re-screen (round 43, wave 1)

Seat: scout, read-only. `/home/vgpnk/Projects/shokuknow/merge/kengaku/` and the absent-defect register were only read. Nothing adopted; no lane file edited. Writes: this report and `.ufo/waves/round-43/build/R43MergeRescreen/{reg-ids,staged-ids,collisions,quarantine-slice,entry-collide.tsv,scratch-reg.md,scratch-collisions}`. Scratch `/fast/scratch/hyaku/kengaku-r43/R43MergeRescreen` held the guard-proof fixtures and the guard's working files (the envelope mounts $HOME read-only, so the guard's `A=` pointed at scratch and the receipts were copied out). Tooling installed: none.

Envelope (Q32), both runs: `.ufo/waves/round-43/claims/envelope.sh $S/env sh run.sh`. Run 1 `start 19:13:04 … end 19:13:05 exit=0`, run 2 `start 19:13:15 … end 19:13:17 exit=0`; both `local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`. (Run 1's first guard call hit `Read-only file system` writing into the home-mounted report dir and printed `REFUSED: anchor matched no row` / exit 2 — an envelope artefact, not a result; run 2 is the measurement.)

## 1. Changed since round 42 (and since 2026-10-24)? No — package bytes identical

```
$ sha256sum SOURCES.append.md MERGE-REPORT.json MERGE-REPORT.md knowledge/corpus/knowledge/grader-predicate-input-types.md
a46458851f933edb352c517cb36fe97ad830054e1f0139bdc0a32cbf6c3eb73b  SOURCES.append.md
c47fbe68ceacf0d21258dad9938146e325e4c7e68752928ef6644c23f53dff23  MERGE-REPORT.json
807b8451f86f5a94e4f8dba62ff84738f6a1d2216adcf3175b3b014537c89906  MERGE-REPORT.md
350e2677f920dc5779d4f4a6e14d283f1b9e89d2a3432708021e235a0f11fed0  grader-predicate-input-types.md
$ stat -c '%y' SOURCES.append.md MERGE-REPORT.json MERGE-REPORT.md | sort -u
2026-10-24 23:33:20.057709921 -0300 / .059108750 / .059190400        # all three, same second
$ find merge/kengaku -newermt '2026-10-24 23:33:21' | wc -l      → 0
$ find merge/kengaku -type f | wc -l                              → 68   (65 knowledge entries + 3 top-level; one mtime second for all 68: `find -printf '%TT' | uniq -c` → 68 2026-10-24 23:33:20)
$ git -C shokuknow log -1 --format='%H %cI' -- merge/kengaku      → ba6779f0160d12dd7373627e00291d6d5e3ba7ee 2026-10-24T10:50:02-03:00
$ git -C shokuknow log -1 --format='%h %ci'                       → 8b94c5c1 2026-10-24 11:02:02 -0300
$ git -C shokuknow status --short merge/kengaku | awk '{print $1}' | sort | uniq -c   →  19 ??   3 M
```

- Nothing is newer than the single 2026-10-24 23:33:20 stamp: no file changed since 2026-10-24 (MERGE-REPORT.md included: sha256 `807b8451…9906`, 175 rows accepted / 65 entries, "first staged id is S077").
- Three sha256 equal `R42MergeRescreen.md` §1 (`a4645885…`, `c47fbe68…`, `350e2677…`); commit, shokuknow HEAD, 19 ??/3 M, 65 entries identical. Per-entry verdicts carried from r42 (bytes identical): admit-candidate 2, hold 42, refuse 21 (= 65).
- Caveat carried: the screened identity is the sha256, not `ba6779f0` — rounds 13-16 staging is uncommitted in shokuknow.

## 2. id-collision check (0-3 leading spaces), real run

Guard `.ufo/waves/round-36/assimilation/id-collision-check.sh` (anchor `^ {0,3}\|[[:space:]]*S[0-9]{3,}`; exit 3 = collisions, 2 = input absent/anchor-silent), registry `corpus/SOURCES.md` (`git status --short corpus/SOURCES.md | wc -l` → 0, committed; last commit `ff14d76` 2026-10-26T17:42:26-03:00, round-42 landing, S125-S128):

```
$ A=$S/A LANE=<lane> sh id-collision-check.sh
reg-ids=121 staged-ids=175 collisions=45        exit=3 (as designed)
```

sha256: `reg-ids` `192787e49ee690ae3604561b89a0d5c9cdec74604b339d06115fa61619d90161` (121), `staged-ids` `2df53989ae5ab5c4f698f7ed459310a9a376cd970240e7483aeed40c3cdf5e1c` (175; equals r42), `collisions` `ef8a818bd43186fba88effec13e5b0c86356ce6ee3918f77e05cbb545d5fe679` (45).

- vs round 42 (`comm -13`): `reg-ids` 117 → 121, added exactly **S125 S126 S127 S128**; `collisions` 41 → 45, added exactly the same four. (r42 forward-look said 44 — it counted only S125-S127; the landed round-42 package also took **S128**, circuit-fibsqrt row, and staged S128 exists.) Set: S077-S086, S090-S094, S097, S100-S128 (10+5+1+29 = 45). Lane max S128; staged max S251; reg-only = S001-S076.
- **Round-43 forward-look** ([INFERENCE] from the frozen claims: C2 rows S129-S134, `grep -cE 'S129|S13[0-4]' plans/round-43-claims.md` → 3 lines): `comm -12 staged-ids <(S129..S134)` → all six staged; `comm -12 reg-ids <(S129..S134) | wc -l` → 0 now. Staged S129 = GB/T 高质量数据集 draft standard, S130 = Toolathlon grader probe (own-work), S131-S134 = contamination taxonomy / Contamination Disclosure spec rows (`SOURCES.append.md:59-64`) — unrelated to the TB2 feal grader. When the lane rows land collisions go 45 → **51**. **Floor for any later staged-row adoption: renumber past S134** (S127 in r42, S124 in r41).
- Entries citing a colliding id (`entry-collide.tsv`, source ids from r42's entry-map vs `reg-ids`): 22 of 65 now; 24 after C2 lands (adds `card-design-arbitration` S131-S134 ×4, `toolathlon-grader-behaviour-probe-2026-10-23` S130; `cjk-dataset-standard-status-2026-10-23` goes 1 → 2). All three already HOLD/REFUSE — no verdict moves. Admit-candidates: `benchmark-card-field-schema-2026-10-23` (S122-S124) still 3/3 colliding; `benchmark-card-adoption` (S135-S139) 0 collisions with S129-S134 landed.
- Guard proof (the script's `--selftest` hard-codes `/tmp`, not usable; the identical fixture built under scratch and run through the real script):

```
$ printf '  | S002 | indented collision bait | code |\n| S900 | control | code |\n' > reg.md
$ printf '| S002 | staged twin | code |\n| S901 | no twin | code |\n' > staged.md
$ printf '    | S003 | four-space | code |\n   | S004 | three-space | code |\n' > indent.md
$ A=a REG=reg.md STAGED=staged.md sh id-collision-check.sh
reg-ids=2 staged-ids=2 collisions=1                 exit=3        a/collisions → S002
$ grep -oE '^[|][[:space:]]*S[0-9]{3,}' reg.md | grep -oE 'S[0-9]+'     # bare ^| anchor
S900                                                                    # S002 missed
$ A=a REG=indent.md STAGED=staged.md sh id-collision-check.sh
reg-ids=1 staged-ids=2 collisions=0                 exit=0        a/reg-ids → S004 (3-space parses; 4-space S003 does not)
$ A=a REG=nope STAGED=staged.md sh id-collision-check.sh
REFUSED: input absent: nope                         exit=2
```

`scratch-collisions` nonempty (= `S002`); the indented row collides under the 0-3-space anchor and is invisible to the bare one; a missing registry refuses, never reports 0.

## 3. Quarantine slice (`absent-defect-register.md`, lane `kengaku`, data rows only)

Register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`: sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833` (equals r42), last commit `d4ab45f2` (equals), mtime 2026-10-24 08:37.

```
$ grep -cE '^\| `[a-z0-9_-]+` \| round[0-9]+ \| S[0-9]{3,} \|' register      → 194
$ grep -E '^\| `kengaku` \| round[0-9]+ \| S[0-9]{3,} \|' register | awk -F'|' '{...}'
S091 round2 `payload-absent`
S105 round3 `payload-absent`
$ cmp <that output> round-42/…/quarantine-slice   → identical
```

Slice = staged **S091** (NEC techrep) and **S105** (archived METI GENIAC page), unchanged; both are also in `collisions`. Entries citing them: `cjk-eval-journal-access` (S091), `cjk-benchmark-governance-2026-10-23` (S105) — REFUSE.

## 4. PROVINCE scope and uncovered ground vs round 43 (TB2 feal-differential-cryptanalysis grader; tool-mutant calibration)

PROVINCE `### Frontier` (`PROVINCE.md:121-127`) names "agentic benchmark task-spec audits (Terminal-Bench 2.0 / Toolathlon / SWE-bench Pro primary specs)" — round-43 C2 is squarely in scope; the staged package has no entry on it. Greps over `merge/kengaku` (all, `-rli`):

```
feal|cryptanaly|differential|cipher|chosen.plaintext|block cipher|crypto                → (no output) rc=1
build_ext|c extension|sys.path|sys.modules|os._exit|__eq__|monkey.?patch|srand|time limit|exit status|hijack
    → benchmark-task-validity-checklist, benchmark-verifier-execution-model, grader-sheet-checks-real-pandas-r16, SOURCES.append.md
    -oiE '.{0,70}(…).{0,70}' context scan over the same files → one line only: grader-sheet-checks-real-pandas-r16.md:16 `sys.modules.setdefault("pandas", _pandas_stub())`
mutation test|mutmut|mutant|mutation score|settrace|trace|calibrat.*(tool|checker)
    → benchmark-task-validity-checklist, benchmark-grader-semantics, cjk-eval-journal-access, cjk-benchmark-governance-2026-10-23, card-publication-contracts, grader-candidate-coverage-r15, SOURCES.append.md   (all 'trace'/'traceability' fragments, plus S095 'mutation score' in cjk-eval-journal-access)
terminal-bench-2|2fd12b88|differential-crypt|feal
    → only the already-adopted-adapted Terminal-Bench identity/task-schema rows (S079, S100 at 2fd12b88): benchmark-task-validity-checklist, benchmark-verifier-execution-model, terminal-bench-release-identity
```

- **Feal / cryptanalysis / C-extension import / sys.path / exit-status graders: none staged.** The only `sys.modules` hit is a pandas-stub fact inside `grader-sheet-checks-real-pandas-r16` (Toolathlon-lineage sheet grader, HOLD), not about an agent module imported into the grader's interpreter. The frozen C2 facts (test_outputs.py:20-30, feal_module.c:51 `get_keys`, test.sh:25 exit-status reward, the 5 passing cheats / 4 failing cases) are uncovered by staged text and sourced entirely from the pinned TB2 captures.
- **Tool-mutant calibration (C1): none.** Sole mutation-testing text remains S095 (软件学报 test-set validity review, `SOURCES.append.md:25`), not in `collisions`, not quarantined, but cited only by REFUSE `cjk-eval-journal-access`; conceptual, not support for the 9 frozen mutants or the traced attribution legs [INFERENCE].
- TB2-grader neighbours already in the lane: `benchmark-verifier-execution-model` and `benchmark-task-validity-checklist` (REFUSE, adopted adapted), `terminal-bench-release-identity` (REFUSE; release identity only). None speaks of the feal task, its grader, or the reward semantics.
- Staged S129-S134 are *not* TB2 rows (see §2): the frozen C2 ids would collide with unrelated staged sources. C2's rows are self-sourced from the pinned capture; nothing staged would be displaced or supported.

## 5. Verdicts — per entry (65), carried (bytes identical)

`cut -f5 entry-collide.tsv | sort | uniq -c` equivalent (Python Counter on r42's `entry-verdicts.tsv`): **ADMIT-candidate 2, HOLD 42, REFUSE 21**.

| Verdict | Entries | Reason |
|---|---|---|
| ADMIT-candidate (2) | `benchmark-card-field-schema-2026-10-23` (S122-S124, still 3/3 collide); `benchmark-card-adoption` (S135-S139, 0 collide) | Only for the "contamination transparency cards" frontier (`PROVINCE.md:122-127`); fits neither round-43 claim. Flip: a frozen claim on the card family; renumber past S134 first. |
| HOLD (42) | card/maintainer/OSF/post-5G family, `grader-predicate-input-types` (sha `350e2677…`, round-36 defects stand), grader-integrity models, judge-calibration/meta-evaluation, CJK/GENIAC/disclosure | Unchanged; burned ids now to S128 (S134 after C2). |
| REFUSE (21) | adopted-adapted (4), quarantine (2: S091/S105 entries), Toolathlon own-work/lineage (11), `terminal-bench-release-identity`, shokuknow-internal own-work (3) | Unchanged. |

## 6. Recommendation: none (adopt nothing)

1. Package bytes unchanged since 2026-10-24 23:33:20 (three sha256 equal r42); the "changed?" answer is no, so no new evidence to admit.
2. Nothing staged covers feal-differential-cryptanalysis (no hit for feal/cryptanaly/differential/cipher) or tool-mutant calibration; C1/C2 are lane-local and pinned-capture sourced.
3. The two admit-candidates serve a different frontier (cards), and any row adoption must first renumber past **S134** (45 current collisions, 51 once C2's S129-S134 land).
4. Quarantine S091/S105 stays out; both entries citing them stay REFUSE.

## 7. Delta for the L1 vs round 42

- Package: unchanged. Collisions 41 → 45 (S125-S128 landed); → 51 after C2. Renumber floor S127 → **S134**.
- Entries touched by C2's ids: `card-design-arbitration`, `toolathlon-grader-behaviour-probe-2026-10-23`, `cjk-dataset-standard-status-2026-10-23` (no verdict change).
- Quarantine slice: unchanged (S091, S105). Verdict tally: unchanged (2/42/21).
- Corrected r42's forward count (44): the landed round-42 package also took S128, so the live collision count is 45.

Unresolved: guard `--selftest` still writes under `/tmp`; entry-level reasons are carried from the round-40/41 line-by-line pass (bytes identical), and the per-entry source-id columns reuse r42's `entry-map.tsv`. No live fetch run (nothing landable).

VERDICT: merge-unchanged-collisions-45-recommend-none
