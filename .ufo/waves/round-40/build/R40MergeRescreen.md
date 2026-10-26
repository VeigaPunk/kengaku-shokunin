# R40MergeRescreen — merge/kengaku re-screen (round 40, wave 1)

Seat: scout, read-only. `/home/vgpnk/Projects/shokuknow/merge/kengaku/` and the register were only read. Nothing adopted; no lane file edited. Writes: this report and `.ufo/waves/round-40/build/R40MergeRescreen/{reg-ids,staged-ids,collisions,quarantine-slice,entry-map.tsv,entry-verdicts.tsv,entry-collide.tsv,scratch-reg.md,scratch-collisions}`. Scratch `/fast/scratch/hyaku/kengaku-r40/R40MergeRescreen` held the guard-proof fixtures; removed. Tooling installed: none.

## 1. Changed since round 39? No (bytes identical)

```
$ git -C /home/vgpnk/Projects/shokuknow log -1 --format='%H %cI' -- merge/kengaku
ba6779f0160d12dd7373627e00291d6d5e3ba7ee 2026-10-24T10:50:02-03:00
$ sha256sum SOURCES.append.md MERGE-REPORT.json knowledge/corpus/knowledge/grader-predicate-input-types.md
a46458851f933edb352c517cb36fe97ad830054e1f0139bdc0a32cbf6c3eb73b  SOURCES.append.md
c47fbe68ceacf0d21258dad9938146e325e4c7e68752928ef6644c23f53dff23  MERGE-REPORT.json
350e2677f920dc5779d4f4a6e14d283f1b9e89d2a3432708021e235a0f11fed0  grader-predicate-input-types.md
$ stat -c '%y' ...   # all 2026-10-24 23:33:20 -0300 (unchanged)
$ git -C shokuknow log -1 --format='%h %ci'          # 8b94c5c1 2026-10-24 11:02:02 -0300 (unchanged)
$ git status --short merge/kengaku | awk '{print $1}' | sort | uniq -c    # 19 ??, 3 M
$ find knowledge -type f | wc -l                      # 65
$ find merge/kengaku -type f -newer <r39 entry-map.tsv>   # (no output)
```

- Commit, all three sha256, mtimes, shokuknow HEAD, 65 entry files: identical to `R39MergeRescreen.md` §1. The entry-name set equals round 39's `entry-map.tsv` (`diff` → names-same). `staged-ids` sha256 `2df53989…5e1c` equals round 39's (`diff` → same).
- Round-39 caveat stands: the screened identity is the sha256, not `ba6779f0`; rounds 13–16 staging is uncommitted in shokuknow (3 ` M`, 19 `??`).

## 2. id-collision check (0–3 leading spaces)

Guard: `.ufo/waves/round-36/assimilation/id-collision-check.sh` (anchor `^ {0,3}\|[[:space:]]*S[0-9]{3,}`; exit 3 = collisions, 2 = input absent/anchor-silent), `A=` pointed at this seat's dir:

```
$ A=.ufo/waves/round-40/build/R40MergeRescreen sh id-collision-check.sh
reg-ids=113 staged-ids=175 collisions=37        (exit=3, as designed)
```

sha256: `reg-ids` 9f55e6b5…b94d (113), `staged-ids` 2df53989…5e1c (175), `collisions` 033d6806…958b (37).

- vs round 39 (`diff`): `staged-ids` same; `reg-ids` 109 → 113, added exactly **S117, S118, S119, S120**; `collisions` 33 → 37, added exactly **S117, S118, S119, S120**. Round 39 predicted S117/S118 (its own claims); S119/S120 are this round's frozen C2 rows (tb2-db-wal-recovery grader `tests/test_outputs.py`, `instruction.md`) — **lane-authored, unrelated to staged S119/S120**. Prediction in R39 "35 collisions once S117/S118 land" → with S119/S120, 37, confirmed.
- [OBSERVED] The lane's `corpus/SOURCES.md` is ` M` (uncommitted working tree; `git status --short corpus/SOURCES.md`). Last commit `34158b0` (round 39) ended at S118; S119/S120 rows are the L1's in-tree draft (`grep -E 'S119|S120' corpus/SOURCES.md` → both db-wal-recovery rows). Committed-state collisions would be 35.
- Full collision set: S077–S086, S090–S094, S097, S100–S120 (10+5+1+21 = 37). Staged ids reach S251. **Floor for any later staged-row adoption: renumber past S120** (round 39 said S118; r38 S116; r37 S113; r36 S110).
- Guard proof (the script's own `--selftest` hard-codes `mktemp -d /tmp/…`, forbidden by scratch directive, so the same fixture was built under scratch and run through the real script with `REG=`/`STAGED=`/`A=`):

```
$ printf '  | S002 | indented collision bait | code |\n| S900 | control | code |\n' > reg.md
$ printf '| S002 | staged twin | code |\n| S901 | no twin | code |\n' > staged.md
$ printf '    | S003 | four-space | code |\n   | S004 | three-space | code |\n' > indent.md
$ A=a REG=reg.md STAGED=staged.md sh id-collision-check.sh
reg-ids=2 staged-ids=2 collisions=1   (exit=3)      a/collisions → S002
$ grep -oE '^[|][[:space:]]*S[0-9]{3,}' reg.md | grep -oE 'S[0-9]+'      # bare ^| anchor → S900 only; S002 missed
$ A=a REG=indent.md STAGED=staged.md sh id-collision-check.sh
reg-ids=1 staged-ids=2 collisions=0   (exit=0)      a/reg-ids → S004 (3-space parses, 4-space S003 does not)
$ A=a REG=nope STAGED=staged.md sh id-collision-check.sh
REFUSED: input absent: …/nope         (exit=2)
```

The indented `  | S002 |` row collides under the 0–3-space anchor and is invisible to the bare anchor; a missing registry refuses rather than reporting 0. Copies: `scratch-reg.md`, `scratch-collisions` (= `S002`).

## 3. Quarantine slice (`absent-defect-register.md`, lane `kengaku`, data rows only)

Register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`: sha256 `5afe1810…d833` (equals round 39), last commit `d4ab45f2` (equals). Sections (`grep -nE '^## '`): Totals 16, Rows 25, By lane 232, NEVER CHECKED 256.

```
$ grep -cE '^\| `[a-z0-9_-]+` \| round[0-9]+ \| S[0-9]{3,} \|' register          # 194
$ grep -E '^\| `kengaku` \| round[0-9]+ \| S[0-9]{3,} \|' register | awk -F'|' '{…}'
S091 round2 payload-absent
S105 round3 payload-absent
$ diff round-39/…/quarantine-slice quarantine-slice     # same
```

- By-lane line 252 `| \`kengaku\` | 2 |` agrees with the 2 data rows. NEVER CHECKED section (256–375) names no kengaku row (`sed -n 256,375p | grep -i -E 'kengaku|S091|S105'` → none).
- Slice is staged S091 (NEC techrep) and S105 (archived METI GENIAC page; "quote" is the page's error text). Entries citing them: `cjk-eval-journal-access` (S091), `cjk-benchmark-governance-2026-10-23` (S105). Neither bears on SQLite/WAL or mutation testing.

## 4. Fit to round 40 (SQLite/WAL, database recovery, mutation testing)? No staged entry fits

```
$ cd merge/kengaku && grep -rliE 'sqlite|write-ahead|\bWAL\b|db-wal|crash.recover|database recover|mutation test|mutation-test|mutmut|mutant|pragma|checkpoint' .
(no output)   rc=1
```

A looser first grep (`wal|journal|recover|mutation`) matched 11 files, all on word fragments: "journal" (NEC techrep journal-access entries), "recover" in disclosure/OSF prose, "walk"-class substrings. The word-bounded grep above is empty over entries, `SOURCES.append.md`, `MERGE-REPORT.md/.json`. Nothing staged supplies a SQLite/WAL, database-recovery or mutation-testing fact; C2 stays self-sourced (S119/S120 lane-authored), C1 (tripwire mutants) has no staged input. Round 39's git-leak grep likewise empty.

## 5. Verdicts — per entry (65); `entry-verdicts.tsv` copied unchanged from round 39 (package bytes identical)

`entry-verdicts.tsv` tally: `cut -f2 | sort | uniq -c` → ADMIT-candidate 2, HOLD 42, REFUSE 21 (= 65). Per-entry collision recount against the new `reg-ids` is in `entry-collide.tsv` (18 entries cite ≥1 colliding id; 47 cite none).

| Verdict | Entries | Reason / flip condition |
|---|---|---|
| **ADMIT-candidate (2)** | `benchmark-card-field-schema-2026-10-23` (S122–S124); `benchmark-card-adoption` (S135–S139; after the first) | In scope only for the "contamination transparency cards" frontier (`PROVINCE.md:122-127`); public sources only, no own-work row, not in quarantine, zero id collisions vs the registry (both rows 0 in `entry-collide.tsv`). **Fits no round-40 claim** (neither C1 nor C2 is a card), so not landable this wave. Flip: rows renumbered past S120, quotes re-run in-lane at the pins, dated PROVINCE paragraph. |
| **HOLD (42)** | card/maintainer/OSF/post-5G family (27, unchanged list), `grader-predicate-input-types` (S143/S144; sha `350e2677…` unchanged, round-36 defects stand), `benchmark-grader-integrity-models-2026-10-23` and `…23b` (S101/S102/S107/S108 burned in lane), `judge-calibration-thresholds`, `judge-meta-evaluation-2026-10-23` and `…23b`, CJK/GENIAC/disclosure (9) | Unchanged from round 39 §4 (same reasons, same flip conditions). New fact: S117–S120 are now also lane-burned, widening collisions for `cjk-benchmark-governance-2026-10-23c` (S115–S117), `cjk-dataset-documentation-standard-2026-10-23` (S118/S119), `contamination-mitigation-comparative-evidence-2026-10-23` (S120) — all already HOLD/REFUSE, no verdict moves. |
| **REFUSE (21)** | already-adopted-in-adapted-form (4): `benchmark-grader-semantics`, `benchmark-task-validity-checklist`, `benchmark-verifier-execution-model`, `contamination-transparency-card`; quarantine (2): `cjk-eval-journal-access`, `cjk-benchmark-governance-2026-10-23`; Toolathlon own-work (2): `toolathlon-grader-contract-2026-10-23`, `toolathlon-grader-behaviour-probe-2026-10-23`; Toolathlon own-work lineage (9); `terminal-bench-release-identity`; shokuknow-internal own-work (3): `osf-registration-camera-ready-r15`, `post5g-archive-coverage-r14`, `programme-side-disclosure-record-r15` | Unchanged from round 39 §4. `terminal-bench-release-identity` cites S092/S100 only (lane-held); it is the nearest TB2-adjacent entry and still adds no ground for `db-wal-recovery`. |

## 6. What changed for the L1 vs round 39

1. Package bytes: unchanged (three sha256, `staged-ids`, 65 entry names, mtimes).
2. id floor: lane registry S001–S120 in the working tree (S117/S118 round-39 committed; S119/S120 round-40 draft). Collisions 33 → 37, exactly S117–S120. Renumber past **S120** for any later staged adoption.
3. Quarantine slice: unchanged — S091, S105.
4. Verdicts: admit 2 / hold 42 / refuse 21, per entry unchanged.
5. Nothing staged is about SQLite/WAL, database recovery, or mutation testing; nothing here supports C1 or C2.

Unresolved: the guard's `--selftest` mode writes under `/tmp` (hard-coded), so the equivalent fixture was reproduced under scratch. Live fetches of S122–S124 (round 39) were not repeated since neither admit candidate fits a round-40 claim.

VERDICT: merge-rescreen-admit-2-hold-42-refuse-21
