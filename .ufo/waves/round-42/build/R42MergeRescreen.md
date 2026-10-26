# R42MergeRescreen — merge/kengaku re-screen (round 42, wave 1)

Seat: scout, read-only. `/home/vgpnk/Projects/shokuknow/merge/kengaku/` and the absent-defect register were only read. Nothing adopted; no lane file edited. Writes: this report and `.ufo/waves/round-42/build/R42MergeRescreen/{reg-ids,staged-ids,collisions,quarantine-slice,entry-map.tsv,entry-verdicts.tsv,entry-collide.tsv,scratch-reg.md,scratch-collisions}`. Scratch `/fast/scratch/hyaku/kengaku-r42/R42MergeRescreen` held the guard-proof fixtures and was removed (`ls /fast/scratch/hyaku/kengaku-r42 | grep -c R42MergeRescreen` → 0). Tooling installed: none.

Envelope (Q32): `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent sh $S/run.sh` (run.sh = the guard runs of §2). `date +%T` 17:27:14 → 17:28:14. `ls -A /home/vgpnk/.local/bin | sha256sum` before = after = `436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18`.

## 1. Changed since round 41? No — package bytes identical

```
$ git -C /home/vgpnk/Projects/shokuknow log -1 --format='%H %cI' -- merge/kengaku
ba6779f0160d12dd7373627e00291d6d5e3ba7ee 2026-10-24T10:50:02-03:00          (same as r41)
$ sha256sum SOURCES.append.md MERGE-REPORT.json knowledge/corpus/knowledge/grader-predicate-input-types.md
a46458851f933edb352c517cb36fe97ad830054e1f0139bdc0a32cbf6c3eb73b  SOURCES.append.md
c47fbe68ceacf0d21258dad9938146e325e4c7e68752928ef6644c23f53dff23  MERGE-REPORT.json
350e2677f920dc5779d4f4a6e14d283f1b9e89d2a3432708021e235a0f11fed0  grader-predicate-input-types.md
$ stat -c '%y' SOURCES.append.md MERGE-REPORT.json MERGE-REPORT.md | sort -u   # 2026-10-24 23:33:20 -0300 (3 lines, same second)
$ git -C shokuknow log -1 --format='%h %ci'                                    # 8b94c5c1 2026-10-24 11:02:02 -0300
$ git -C shokuknow status --short merge/kengaku | awk '{print $1}' | sort | uniq -c   # 19 ??, 3 M
$ find knowledge -type f | wc -l                                               # 65
```

All identical to `R41MergeRescreen.md` §1 (three sha256, mtimes, HEAD, 19 ??/3 M, 65 files). `diff` of `staged-ids` vs round 41 → `staged-same` (sha256 `2df53989…5e1c`). Per-entry `source:` header ids recomputed from the 65 entry files equal round 41's `entry-map.tsv` source column (65/65 equal). Caveat carried: the screened identity is the sha256, not `ba6779f0`; rounds 13–16 staging is uncommitted in shokuknow.

## 2. id-collision check (0–3 leading spaces), real run

Guard `.ufo/waves/round-36/assimilation/id-collision-check.sh`, anchor `^ {0,3}\|[[:space:]]*S[0-9]{3,}`, `A=` = this seat's dir, registry `corpus/SOURCES.md` (`git status --short corpus/SOURCES.md | wc -l` → 0, committed; last commit `53b9e4e` 2026-10-26T16:34:15-03:00, round-41 wave-2 close; round-41 landing `74513c0` added S122–S124):

```
$ A=.ufo/waves/round-42/build/R42MergeRescreen sh id-collision-check.sh
reg-ids=117 staged-ids=175 collisions=41        exit=3 (as designed)
```

sha256: `reg-ids` `5c62f2a6366bf33e569adc67f4f31d6a54db2476ce9e07eff8f65137bf7594ad` (117), `staged-ids` `2df53989ae5ab5c4f698f7ed459310a9a376cd970240e7483aeed40c3cdf5e1c` (175), `collisions` `558cc5a80c568a2d292542a049db42b5476eb1bae5e36fd36eda0b095c9d745b` (41).

vs round 41 (`diff`): `staged-ids` same; `reg-ids` 114 → 117, added exactly **S122 S123 S124** (round-41 C2 package); `collisions` 38 → 41, added exactly S122 S123 S124 — the forward-look in `R41MergeRescreen.md` §2 came true. Full set: S077–S086, S090–S094, S097, S100–S124 (10+5+1+25 = 41). Lane max S124; staged max S251.

- **Round-42 forward-look** (`plans/round-42-claims.md:67-70`, C2 rows S125 test_outputs.py, S126 instruction.md, S127 sim.c): staged S125/S126/S127 exist (`comm -12 staged-ids <(S122..S127)` → all six; `comm -12 reg-ids <(S125 S126 S127)` → none yet). Staged S125 = Samaritan SWE-bench Verified review, S126 = "Evaluation Cards" arXiv 2606.09809, S127 = post-5G R&D plan PDF (`SOURCES.append.md:55-57`). When the lane rows land collisions go 41 → **44**. **Floor for any later staged-row adoption: renumber past S127** (S124 in r41, S120 in r40).
- Entries citing colliding ids: `entry-collide.tsv` (source ids vs `reg-ids`; col 4 vs `reg-ids ∪ {S125,S126,S127}`): 19 entries now (r41: 18 + `benchmark-card-field-schema-2026-10-23`, now S122–S124 = 3 collisions), 21 after C2 lands (adds `geniac-phase2-terms-2026-10-23` via S127 and `per-benchmark-contamination-verdicts-2026-10-23` via S125+S126; both already HOLD).
- Guard proof (the script's `--selftest` hard-codes `/tmp`; identical fixture under scratch through the real script):

```
$ printf '  | S002 | indented collision bait | code |\n| S900 | control | code |\n' > reg.md
$ printf '| S002 | staged twin | code |\n| S901 | no twin | code |\n' > staged.md
$ printf '    | S003 | four-space | code |\n   | S004 | three-space | code |\n' > indent.md
$ A=a REG=reg.md STAGED=staged.md sh id-collision-check.sh
reg-ids=2 staged-ids=2 collisions=1        exit=3      a/collisions → S002
$ grep -oE '^[|][[:space:]]*S[0-9]{3,}' reg.md | grep -oE 'S[0-9]+'     # bare ^| anchor
S900                                                                   # S002 missed
$ A=a REG=indent.md STAGED=staged.md sh id-collision-check.sh
reg-ids=1 staged-ids=2 collisions=0        exit=0      a/reg-ids → S004 (3-space parses, 4-space S003 does not)
$ A=a REG=nope STAGED=staged.md sh id-collision-check.sh
REFUSED: input absent: …/nope              exit=2
```

The indented `  | S002 |` row collides under the 0–3-space anchor and is invisible to the bare anchor; a missing registry refuses instead of reporting 0. Copies: `scratch-reg.md`, `scratch-collisions` (= `S002`).

## 3. Quarantine slice (`absent-defect-register.md`, lane `kengaku`, data rows only)

Register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`: sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833` (r41 `5afe1810a6c3…d833`, equal), last commit `d4ab45f2` (equal).

```
$ grep -cE '^\| `[a-z0-9_-]+` \| round[0-9]+ \| S[0-9]{3,} \|' register          → 194 (equals r41)
$ grep -E '^\| `kengaku` \| round[0-9]+ \| S[0-9]{3,} \|' register | awk -F'|' '{…}'
S091 round2 `payload-absent`
S105 round3 `payload-absent`
$ cmp r41/quarantine-slice r42/quarantine-slice → identical
$ grep -n kengaku register → lines 101, 102 (the two data rows) and 252 (`| kengaku | 2 |` count row)
```

Slice = staged **S091** (NEC techrep) and **S105** (archived METI GENIAC page), unchanged. Both are also in `collisions` (S091, S105): burned twice. Entries citing them: `cjk-eval-journal-access` (S091), `cjk-benchmark-governance-2026-10-23` (S105) — both REFUSE.

## 4. Fit to round 42 (logic-circuit/simulator graders, benchmark-grader audits, mutation testing)

```
$ grep -rliE 'logic.circuit|gate.?level|netlist|verilog|\bvhdl\b|simulator|circuit|fibonacci|isqrt|integer square|gates\.txt|\bsim\.c\b|circuit-fibsqrt|\bgcc\b|\bC program|lookup table|hardcod|hard-cod' .   → (no output)
$ grep -rliE 'mutation test|mutation-test|mutmut|mutant|mutation score|mutat' .                                   → cjk-eval-journal-access.md, SOURCES.append.md
$ grep -rliE 'grader audit|audit of .*grader|false.pass|false.positive|tripwire|verifier|test_outputs|reward hack|shortcut|cheat|tb2|terminal.bench' .
    → benchmark-grader-integrity-models-2026-10-23, benchmark-task-validity-checklist, benchmark-verifier-execution-model,
      cjk-eval-venue-access, judge-calibration-thresholds, terminal-bench-release-identity, MERGE-REPORT.json/.md, SOURCES.append.md
```

- **Logic-circuit / simulator / gate-list graders: none.** No staged file mentions a circuit, simulator, netlist, `gates.txt`, `sim.c`, Fibonacci/isqrt or a hard-coded lookup shape. C2 (`circuit-fibsqrt`, S125–S127) stays self-sourced; the staged S125–S127 are unrelated rows that would collide with it.
- **Benchmark-grader audits: nearest entries are already adopted-in-adapted-form or held.** `benchmark-verifier-execution-model`, `benchmark-task-validity-checklist` (REFUSE, already adopted adapted); `benchmark-grader-integrity-models-2026-10-23` / `…23b` (HOLD; S101/S102/S107/S108 lane-burned, S094 in `…23b`); `terminal-bench-release-identity` (REFUSE; cites lane-held S092/S100, nothing on circuit-fibsqrt). None gives a fact about the sim.c grader, the 28-value table, or the shape gaps in `fibsqrt-probe.txt`.
- **Mutation testing: still one hit, unchanged.** Staged row **S095** (`SOURCES.append.md:25`, 软件学报 2024 test-set-validity review; mutation score as a test-set validity metric), cited only by `cjk-eval-journal-access.md` (which also cites S091, quarantine). S095 ∉ `collisions` (`grep -cx S095 collisions` → 0) and ∉ quarantine slice, but its sole entry is REFUSE and the text is conceptual, not a fact about the 14 C1 mutants or the C1 tools; [INFERENCE] adjacency prose, not support for either frozen predicate. Not landable this wave.
- Net: **nothing staged fits this round's claims.** C1 (tool-mutant calibration) and C2 (circuit-fibsqrt) are sourced entirely from lane-local frozen artefacts and the pinned TB2 captures.

## 5. Verdicts — per entry (65), `entry-verdicts.tsv` = r41's (package bytes identical)

`cut -f2 entry-verdicts.tsv | tail -n +2 | sort | uniq -c` → ADMIT-candidate 2, HOLD 42, REFUSE 21 (= 65).

| Verdict | Entries | Reason / flip condition |
|---|---|---|
| **ADMIT-candidate (2)** | `benchmark-card-field-schema-2026-10-23`; `benchmark-card-adoption` | Only for the "contamination transparency cards" frontier (`PROVINCE.md:122-127`); public sources, not quarantined. `benchmark-card-adoption` (S135–S139) 0 collisions; `…field-schema…` (S122–S124) collides 3/3 with the landed round-41 C2 rows → renumber past S127 (not S124) first. **Fits no round-42 claim** (C1 tool calibration, C2 circuit-fibsqrt): not landable this wave. Flip: renumbered rows, quotes re-run in-lane at the pins, dated PROVINCE paragraph. |
| **HOLD (42)** | card/maintainer/OSF/post-5G family (27), `grader-predicate-input-types` (S143/S144; sha `350e2677…` unchanged, round-36 defects stand), `benchmark-grader-integrity-models-2026-10-23` / `…23b`, `judge-calibration-thresholds`, `judge-meta-evaluation-2026-10-23` / `…23b`, CJK/GENIAC/disclosure (9) | Unchanged. Burned ids now run to S124 (S127 after C2); `geniac-phase2-terms-2026-10-23` (S127) and `per-benchmark-contamination-verdicts-2026-10-23` (S125, S126) newly collide when C2 lands; both already HOLD, no verdict moves. |
| **REFUSE (21)** | already-adopted-adapted (4): `benchmark-grader-semantics`, `benchmark-task-validity-checklist`, `benchmark-verifier-execution-model`, `contamination-transparency-card`; quarantine (2): `cjk-eval-journal-access` (S091, S095 quote), `cjk-benchmark-governance-2026-10-23` (S105); Toolathlon own-work (2) + lineage (9); `terminal-bench-release-identity`; shokuknow-internal own-work (3): `osf-registration-camera-ready-r15`, `post5g-archive-coverage-r14`, `programme-side-disclosure-record-r15` | Unchanged. Full per-entry rows: `entry-verdicts.tsv` (entry, verdict, reason); per-entry collision counts: `entry-collide.tsv`. |

Tally: admit 2 (both "candidate", none admitted this round; none fits a frozen claim), hold 42, refuse 21.

## 6. What changed for the L1 vs round 41

1. Package bytes: unchanged.
2. id floor: lane registry S001–S124 committed; round-42 C2 adds S125–S127 → collisions 41 → 44; renumber past **S127** for any later staged-row adoption. The `benchmark-card-field-schema` admit-candidate's own ids (S122–S124) are now consumed by the landed round-41 rows.
3. Quarantine slice: unchanged — S091, S105.
4. Verdicts: unchanged, admit 2 / hold 42 / refuse 21.
5. Nothing staged concerns logic-circuit/simulator graders; the only mutation-testing text remains S095 inside the REFUSEd `cjk-eval-journal-access`.

Unresolved: the guard's `--selftest` writes under `/tmp` (hard-coded), so the fixture was reproduced under scratch. No live fetch of S095 or card rows was run (nothing is landable this wave). Entry-level verdict reasons were carried from round 40/41's line-by-line pass, not re-read per entry (bytes identical).

VERDICT: merge-rescreen-admit-2-hold-42-refuse-21
