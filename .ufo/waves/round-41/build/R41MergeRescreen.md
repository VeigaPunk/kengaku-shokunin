# R41MergeRescreen — merge/kengaku re-screen (round 41, wave 1)

Seat: scout, read-only. `/home/vgpnk/Projects/shokuknow/merge/kengaku/` and the absent-defect register were only read. Nothing adopted; no lane file edited. Writes: this report and `.ufo/waves/round-41/build/R41MergeRescreen/{reg-ids,staged-ids,collisions,quarantine-slice,entry-map.tsv,entry-verdicts.tsv,entry-collide.tsv,scratch-reg.md,scratch-collisions}`. Scratch `/fast/scratch/hyaku/kengaku-r41/R41MergeRescreen` held the guard-proof fixtures; removed (`ls … | grep -c R41MergeRescreen` → 0). Tooling installed: none.

## 1. Changed since round 40? No (package bytes identical)

```
$ git -C /home/vgpnk/Projects/shokuknow log -1 --format='%H %cI' -- merge/kengaku
ba6779f0160d12dd7373627e00291d6d5e3ba7ee 2026-10-24T10:50:02-03:00
$ sha256sum SOURCES.append.md MERGE-REPORT.json knowledge/corpus/knowledge/grader-predicate-input-types.md
a46458851f933edb352c517cb36fe97ad830054e1f0139bdc0a32cbf6c3eb73b  SOURCES.append.md
c47fbe68ceacf0d21258dad9938146e325e4c7e68752928ef6644c23f53dff23  MERGE-REPORT.json
350e2677f920dc5779d4f4a6e14d283f1b9e89d2a3432708021e235a0f11fed0  grader-predicate-input-types.md
$ stat -c '%y' SOURCES.append.md MERGE-REPORT.json MERGE-REPORT.md | sort -u     # all 2026-10-24 23:33:20 -0300
$ git -C shokuknow log -1 --format='%h %ci'                                        # 8b94c5c1 2026-10-24 11:02:02 -0300
$ git -C shokuknow status --short merge/kengaku | awk '{print $1}' | sort | uniq -c   #  19 ??, 3 M
$ find knowledge -type f | wc -l                                                    # 65
$ find . -type f -newer <r40 entry-map.tsv>                                         # (no output)
```

- Commit, the three sha256, mtimes, shokuknow HEAD, 65 files: identical to `R40MergeRescreen.md` §1. Entry-name set equals round 40's `entry-map.tsv` (`diff` → `names-same`). `staged-ids` sha256 `2df53989…5e1c` equals round 40's (`diff` → `staged-same`).
- Caveat carried: the screened identity is the sha256, not `ba6779f0`; rounds 13–16 staging is uncommitted in shokuknow (3 ` M`, 19 `??`).

## 2. id-collision check (0–3 leading spaces)

Guard: `.ufo/waves/round-36/assimilation/id-collision-check.sh`, anchor `^ {0,3}\|[[:space:]]*S[0-9]{3,}` (exit 3 = collisions, 2 = input absent / anchor-silent), `A=` pointed at this seat's dir, registry `corpus/SOURCES.md` (lane tree; `git status --short corpus/SOURCES.md` empty → committed, last commit `ec17216` 2026-10-26T14:14:43-03:00 round-40 close):

```
$ A=.ufo/waves/round-41/build/R41MergeRescreen sh id-collision-check.sh
reg-ids=114 staged-ids=175 collisions=38        (exit=3, as designed)
```

sha256: `reg-ids` `e8c6244ae374b097256ac1f29282cef4e50cb3042a78d7437877b1e7a3b8728f` (114), `staged-ids` `2df53989ae5ab5c4f698f7ed459310a9a376cd970240e7483aeed40c3cdf5e1c` (175), `collisions` `affb8b52deb6…1608` (38; full `affb8b52deb6a4b635c248f46d0ded970f1464fb6243af83c703fc7e9b6a1608`).

- vs round 40 (`diff`): `staged-ids` same; `reg-ids` 113 → 114, added exactly **S121**; `collisions` 37 → 38, added exactly **S121**. Lane S121 = "Terminal-Bench 2.1 pull request #3 … db-wal-recovery" (`corpus/SOURCES.md:136`, round-40 lane row); staged S121 = "The Emperor's New Clothes in Benchmarking?" (`SOURCES.append.md:51`, used by `contamination-mitigation-comparative-evidence-2026-10-23`). Different sources, same id → true collision, lane-authored side.
- Full collision set: S077–S086, S090–S094, S097, S100–S121 (10+5+1+22 = 38). Staged ids reach S251.
- **Round 41 forward-look [INFERENCE from the frozen claims brief]:** the C2 package takes S122 (tests/test_outputs.py), S123 (instruction.md), S124 (TB2.1 PR #245). Staged ids S122/S123/S124 exist (`comm -12 staged-ids <(S122 S123 S124)` → all three), so collisions go 38 → **41** the moment those rows land, and the staged card entry `benchmark-card-field-schema-2026-10-23` (S122–S124) goes from 0 to 3 colliding ids. **Floor for any later staged-row adoption: renumber past S124** (was S120 in r40, S118 in r39).
- Guard proof (the script's `--selftest` hard-codes `mktemp -d /tmp/…`, forbidden by the scratch directive, so the identical fixture was built under scratch and run through the real script with `REG=`/`STAGED=`/`A=`):

```
$ printf '  | S002 | indented collision bait | code |\n| S900 | control | code |\n' > reg.md
$ printf '| S002 | staged twin | code |\n| S901 | no twin | code |\n' > staged.md
$ printf '    | S003 | four-space | code |\n   | S004 | three-space | code |\n' > indent.md
$ A=a REG=reg.md STAGED=staged.md sh id-collision-check.sh
reg-ids=2 staged-ids=2 collisions=1                 (exit=3)      a/collisions → S002
$ grep -oE '^[|][[:space:]]*S[0-9]{3,}' reg.md | grep -oE 'S[0-9]+'   # bare ^| anchor → S900 only; S002 missed
S900
$ A=a REG=indent.md STAGED=staged.md sh id-collision-check.sh
reg-ids=1 staged-ids=2 collisions=0                 (exit=0)      a/reg-ids → S004 (3-space parses, 4-space S003 does not)
$ A=a REG=nope STAGED=staged.md sh id-collision-check.sh
REFUSED: input absent: nope                         (exit=2)
```

The indented `  | S002 |` row collides under the 0–3-space anchor and is invisible to the bare anchor; a missing registry refuses rather than reporting 0. Copies: `scratch-reg.md`, `scratch-collisions` (= `S002`).

## 3. Quarantine slice (`absent-defect-register.md`, lane `kengaku`, data rows only)

Register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`: sha256 `5afe1810a6c3…d833` (equals r40), last commit `d4ab45f2` (equals).

```
$ grep -cE '^\| `[a-z0-9_-]+` \| round[0-9]+ \| S[0-9]{3,} \|' register      # 194 data rows (equals r40)
$ grep -E '^\| `kengaku` \| round[0-9]+ \| S[0-9]{3,} \|' register | awk -F'|' '{…}'
S091 round2 `payload-absent`
S105 round3 `payload-absent`
$ sed -n 256,400p register | grep -ciE 'kengaku|S091|S105'                   # 0 (NEVER CHECKED section names no kengaku row)
```

- Slice = staged **S091** (NEC techrep) and **S105** (archived METI GENIAC page). Same as r40 (only the backtick quoting of the reason differs: r40's awk stripped them). Entries citing them: `cjk-eval-journal-access` (S091), `cjk-benchmark-governance-2026-10-23` (S105).
- Register rows for S091/S095 under other lanes (`game-dev-2d`, `chousa`, `revenger`…) are other lanes' ids, not kengaku's; they do not affect this slice.

## 4. Fit to round 41 (scheduling/calendar graders, benchmark-grader audits, mutation testing)

```
$ cd merge/kengaku && grep -rliE 'sqlite|write-ahead|\bWAL\b|db-wal|crash.recover|database recover|mutation test|mutation-test|mutmut|mutant|pragma|checkpoint' .      → (no output) rc=1
$ grep -rliE 'calendar|schedul|icalendar|rfc ?5545|\.ics|vevent|constraints-scheduling|meeting' .   → 4 files, all the string "annual_meeting" in anlp.jp URLs (word fragment); no scheduling/calendar content
$ grep -rlE 'constraints' .                                                                          → (no output)
$ grep -rliE 'terminal-bench|terminal bench|tb2' .   → benchmark-task-validity-checklist, benchmark-verifier-execution-model, terminal-bench-release-identity, benchmark-grader-integrity-models-2026-10-23, SOURCES.append.md, MERGE-REPORT.md/.json
$ grep -rnoiE '.{40}(grader audit|…|false.pass|false.positive|tripwire|mutat).{40}' .                → false-positive (contamination detectors, S086), "mutation score" (S095, below)
```

- **Scheduling / calendar graders: none.** No staged entry mentions iCalendar, RFC 5545, `constraints-scheduling`, VEVENT or any calendar task. C2 stays self-sourced (S122/S123/S124 lane-authored).
- **Benchmark grader audits: the nearest are already adopted or held.** `benchmark-verifier-execution-model`, `benchmark-task-validity-checklist`, `benchmark-grader-semantics` (REFUSE, already adopted in adapted form); `benchmark-grader-integrity-models-2026-10-23`/`…23b` (HOLD; S101/S102/S107/S108 lane-burned, 3+1 id collisions); `terminal-bench-release-identity` (REFUSE; cites S092/S100, no `constraints-scheduling`, no TB2.1 PR #245). None supplies a fact about the `constraints-scheduling` grader's behaviour.
- **Mutation testing: one real hit that round 40's grep missed** (its pattern needed `mutation test|mutant`, not `mutation score`). Staged row **S095** (`SOURCES.append.md:25`, 软件学报 2024 test-set-validity review) quotes 「覆盖率和变异得分是两个最重要和最广泛使用的测试集有效性度量」 (coverage and mutation score are the two most important validity metrics) and 「现有研究存在不一致的结论」 (existing research reaches inconsistent conclusions). Only entry citing it: `cjk-eval-journal-access.md:3,38-46`, which says mutation score "asks whether the tests would catch a deliberate defect" — a conceptual neighbour of C1's 23-mutant kill calibration. It supports no fact about the C1 tools' behaviour (C1 is calibrated on frozen mutants + `round41_c1_verify.py`, not on literature).
  - Entry verdict stays **REFUSE**: it also cites S091 (register `payload-absent`, quarantine slice), and `entry-verdicts.tsv` row 24 says so. S095 itself is not in the kengaku quarantine slice and is not a collision (S095 ∉ `collisions`; S090–S094 and S097 are, S095 is not), so a stand-alone in-lane row **could** be lifted later, renumbered past S124, quote re-run at the live page. It is not required for any frozen C1/C2 claim, so it is **not landable this wave**: [INFERENCE] it would be adjacency prose, not support for a predicate.

## 5. Verdicts — per entry (65)

`entry-verdicts.tsv` copied unchanged from round 40 (package bytes identical; see §1): `cut -f2 | tail -n +2 | sort | uniq -c` → ADMIT-candidate 2, HOLD 42, REFUSE 21 (= 65). `entry-collide.tsv` recounts each entry's cited ids against the new `reg-ids` (col 2) and against `reg-ids ∪ {S122,S123,S124}` (col 3): 18 entries cite ≥1 colliding id now, 19 once the C2 rows land (the added one is `benchmark-card-field-schema-2026-10-23`, 0 → 3). `entry-map.tsv` = r40's, unchanged.

| Verdict | Entries | Reason / flip condition |
|---|---|---|
| **ADMIT-candidate (2)** | `benchmark-card-field-schema-2026-10-23`; `benchmark-card-adoption` | In scope only for the "contamination transparency cards" frontier (`PROVINCE.md:122-127`); public sources only, not quarantined, no own-work row. `benchmark-card-adoption` (S135–S139) has 0 collisions; **`benchmark-card-field-schema-2026-10-23` (S122–S124) now collides with the lane's new C2 rows (3 ids)** and would need renumbering past S124 before any admit. **Fits no round-41 claim** (C1 = tool mutant calibration, C2 = constraints-scheduling grader): not landable this wave. Flip: rows renumbered past S124, quotes re-run in-lane at the pins, dated PROVINCE paragraph. |
| **HOLD (42)** | card/maintainer/OSF/post-5G family (27), `grader-predicate-input-types` (S143/S144; sha `350e2677…` unchanged, round-36 defects stand), `benchmark-grader-integrity-models-2026-10-23` / `…23b` (S101/S102/S107/S108 burned in lane), `judge-calibration-thresholds`, `judge-meta-evaluation-2026-10-23` / `…23b`, CJK/GENIAC/disclosure (9) | Unchanged from r40 §5. Lane-burned ids now run to S121 (S124 after C2): `contamination-mitigation-comparative-evidence-2026-10-23` additionally collides on S121 (staged S121 = "Emperor's New Clothes", lane S121 = TB2.1 PR #3); all already HOLD/REFUSE, no verdict moves. |
| **REFUSE (21)** | already-adopted-in-adapted-form (4): `benchmark-grader-semantics`, `benchmark-task-validity-checklist`, `benchmark-verifier-execution-model`, `contamination-transparency-card`; quarantine (2): `cjk-eval-journal-access` (S091; also carries the S095 mutation-score quote, §4), `cjk-benchmark-governance-2026-10-23` (S105); Toolathlon own-work (2) + lineage (9); `terminal-bench-release-identity`; shokuknow-internal own-work (3): `osf-registration-camera-ready-r15`, `post5g-archive-coverage-r14`, `programme-side-disclosure-record-r15` | Unchanged from r40 §5. `terminal-bench-release-identity` is the nearest TB2-adjacent entry; cites S092/S100 only (lane-held), nothing on `constraints-scheduling`. |

Tally: admit-candidate 2 → reported as **admit 2**, hold 42, refuse 21. None of the 2 is admitted this round; none fits a frozen claim.

## 6. What changed for the L1 vs round 40

1. Package bytes: unchanged (three sha256, `staged-ids`, 65 entry names, mtimes).
2. id floor: lane registry S001–S121 committed (`ec17216`); C2 will add S122–S124. Collisions 37 → 38 now (S121), → 41 after S122–S124 land. Renumber past **S124** for any later staged adoption. The `benchmark-card-field-schema-2026-10-23` admit-candidate's own ids (S122–S124) are consumed by this round's C2 rows.
3. Quarantine slice: unchanged — S091, S105.
4. Verdicts: admit 2 / hold 42 / refuse 21, per entry unchanged.
5. Nothing staged is about scheduling/calendar graders or the `constraints-scheduling` task; the only mutation-testing-adjacent text is S095's two quotes in the REFUSEd `cjk-eval-journal-access` (correction to r40 §4, which reported none because its grep omitted "mutation score").

Unresolved: the guard's `--selftest` writes under `/tmp` (hard-coded), so the fixture was reproduced under scratch. Live fetches of S095 / card rows were not run: nothing here is landable this wave. The C2 S122–S124 forward-look rests on the brief's wording, not on a read of `plans/round-41-claims.md` by this seat.

VERDICT: merge-rescreen-admit-2-hold-42-refuse-21
