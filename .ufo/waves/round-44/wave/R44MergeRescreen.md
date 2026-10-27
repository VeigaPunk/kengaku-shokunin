# R44MergeRescreen — merge/kengaku re-screen (round 44, wave)

Scout, read-only. `/home/vgpnk/Projects/shokuknow/` only read; no lane file edited; nothing installed. Receipts in `.ufo/waves/round-44/wave/R44MergeRescreen/`: `run.sh` (driver), `run1.txt` (envelope run), `reg-ids`, `staged-ids`, `collisions`, `scratch-reg.md`, `scratch-collisions`. Scratch `/fast/scratch/hyaku/kengaku-r44/R44MergeRescreen` removed at the end.

Envelope (Q32), one run: `envelope.sh $S/env sh $S/run.sh` → `ENVELOPE start 20:35:51 … end 20:35:53 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`.

## 1. Changed since 2026-10-24? No

```
$ cd /home/vgpnk/Projects/shokuknow/merge/kengaku; sha256sum SOURCES.append.md MERGE-REPORT.json MERGE-REPORT.md knowledge/corpus/knowledge/grader-predicate-input-types.md
a46458851f933edb352c517cb36fe97ad830054e1f0139bdc0a32cbf6c3eb73b  SOURCES.append.md
c47fbe68ceacf0d21258dad9938146e325e4c7e68752928ef6644c23f53dff23  MERGE-REPORT.json
807b8451f86f5a94e4f8dba62ff84738f6a1d2216adcf3175b3b014537c89906  MERGE-REPORT.md
350e2677f920dc5779d4f4a6e14d283f1b9e89d2a3432708021e235a0f11fed0  grader-predicate-input-types.md
$ find . -type f | wc -l → 68      $ find . -newermt '2026-10-24 23:33:21' | wc -l → 0
$ find . -type f -printf '%TT\n' | cut -c1-8 | sort | uniq -c → 68 23:33:20
$ git -C shokuknow log -1 --format='%H %cI' -- merge/kengaku → ba6779f0160d12dd7373627e00291d6d5e3ba7ee 2026-10-24T10:50:02-03:00
$ git -C shokuknow log -1 --format='%h %ci' → 8b94c5c1 2026-10-24 11:02:02 -0300
$ git -C shokuknow status --short merge/kengaku | awk '{print $1}' | sort | uniq -c → 19 ??   3 M
```

All four sha256 equal `round-43/build/R43MergeRescreen.md` §1 (and r42); all 68 files carry one mtime second; no later file; shokuknow HEAD and the 19 ??/3 M uncommitted state identical. Package bytes unchanged. `register` also unchanged: `absent-defect-register.md` sha256 `5afe1810…d833`, last commit `d4ab45f2` (both equal r43).

## 2. id-collision check (0-3-space anchor), real run

Guard `.ufo/waves/round-36/assimilation/id-collision-check.sh` (anchor `^ {0,3}\|[[:space:]]*S[0-9]{3,}`, then `comm -12` on sorted-unique ids; exit 3 = collisions, 2 = input absent/anchor-silent). Registry `corpus/SOURCES.md` committed (`git status --short corpus/SOURCES.md | wc -l` → 0; last commit `77ea425` 2026-10-26T19:24:42-03:00, round-43 landing, S129-S137).

```
$ A=$S/A LANE=<lane> sh id-collision-check.sh
reg-ids=130 staged-ids=175 collisions=54        exit=3 (as designed)
```
sha256: `reg-ids` `3c3cc9da6bb37869b9b24262f024b4fa7ffb450299dd25c61e041f5221edd92d` (130); `staged-ids` `2df53989…5e1c` (175; **equal to r43's**); `collisions` `ac79f6b7ce358e559d3d75198d7f33302df455d62dc22824d14ca60811e3b9dd` (54).

- Delta vs round 43 (`comm -13` on r43 receipts): `reg-ids` 121 → 130, added exactly **S129-S137**; `collisions` 45 → 54, the same nine. Lane max S137; staged max S251; reg-only = S001-S076.
- Staged ids at those numbers are unrelated to what the lane landed: lane S135-S137 are Terminal-Bench circuit-fibsqrt / feal-differential rows (`corpus/SOURCES.md:150-152`); staged S135-S137 are AI Alliance card pages (`SOURCES.append.md:65-67`).
- **Round-44 forward look** [INFERENCE from the frozen claims: C2 takes S138-S146]: staged S138-S146 all exist (`SOURCES.append.md:68-76`: AI Alliance Atlas Nexus, FDE-Bench, contamination review, NEDO/METI, Toolathlon comparison/probe, 基准污染 deep-dive, EvalEval Quickstart); `comm` of reg-ids with S138-S146 → 0 now. When the lane rows land: collisions 54 → **63**. **Renumber floor for any later staged-row adoption: past S146** (S134 in r43, S127 in r42).
- Entries citing a colliding id: 28 of 65 (any `S\d{3,}` in the entry body ∩ `collisions`; coarse, counts mentions). All carry HOLD/REFUSE verdicts from r40-r43; no verdict moves.

### Guard proof (indented `  | S002 |` row), in the envelope

```
$ printf '  | S002 | indented collision bait | code |\n| S900 | control | code |\n' > reg.md
$ printf '| S002 | staged twin | code |\n| S901 | no twin | code |\n' > staged.md
$ printf '    | S003 | four-space | code |\n   | S004 | three-space | code |\n' > indent.md
$ A=a REG=reg.md STAGED=staged.md sh id-collision-check.sh
reg-ids=2 staged-ids=2 collisions=1        exit=3      collisions → S002
$ grep -oE '^[|][[:space:]]*S[0-9]{3,}' reg.md | grep -oE 'S[0-9]+'     (bare anchor)
S900                                                    S002 missed
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' reg.md | grep -oE 'S[0-9]+'   (0-3-space anchor)
S002
S900
$ A=b REG=indent.md STAGED=staged.md sh id-collision-check.sh → reg-ids=1 staged-ids=2 collisions=0 exit=0   b/reg-ids → S004 (3-space parses, 4-space S003 does not)
$ A=c REG=nope STAGED=staged.md sh id-collision-check.sh → REFUSED: input absent: nope   exit=2
```
Receipts: `run1.txt`, `scratch-reg.md`, `scratch-collisions` (= `S002`). The indented row collides under the 0-3-space anchor and is invisible to the bare one; a missing registry refuses rather than reporting 0.

## 3. Quarantine slice

`grep -E '^\| `kengaku` \| round[0-9]+ \| S[0-9]{3,} \|' absent-defect-register.md` → **S091** (round2, `payload-absent`) and **S105** (round3, `payload-absent`), identical to r43's slice; register sha256 unchanged. Both stay out (entries `cjk-eval-journal-access`, `cjk-benchmark-governance-2026-10-23` REFUSE).

## 4. PROVINCE scope, uncovered ground (LLM eval / benchmark graders)

PROVINCE Frontier (`PROVINCE.md:121-127`): agentic benchmark task-spec audits (Terminal-Bench 2.0 / Toolathlon / SWE-bench Pro), contamination transparency cards, judge calibration, non-karpathy wiki topics. Round-44 C2 (TB2 `feal-linear-cryptanalysis` grader, S138-S146) is in scope. Greps over `merge/kengaku` (`-rli`, all 68 files):

```
feal|cryptanaly|differential|cipher|chosen.plaintext|crypto            → (no output) rc=1
terminal-bench-2|2fd12b88|feal-linear|harbor-framework                 → benchmark-task-validity-checklist, benchmark-verifier-execution-model, terminal-bench-release-identity, SOURCES.append.md (release/schema rows only, already adopted-adapted as S079/S100)
substring|in data|exit status|test\.sh|reward                           → benchmark-task-validity-checklist, benchmark-verifier-execution-model, benchmark-grader-semantics, benchmark-grader-integrity-models-2026-10-23, SOURCES.append.md (general grader-semantics prose; none on a substring-containment grader or pytest-exit-status reward on a feal task)
mutation test|mutmut|mutant|settrace|attributed kill                   → (no output); only `mutation score` at cjk-eval-journal-access.md:44,55 / S095 (SOURCES.append.md:25), a REFUSE entry, conceptual
```

- No staged entry covers the feal-linear grader, its public-key/hash-chain/constant-copy passes, or tool-mutant calibration (C1). Both frozen claims stay sourced entirely from the pinned TB2 captures plus own measurements.
- 26 of 65 entries mention grader/verifier; none addresses the feal task. TB2 neighbours already in the lane (`benchmark-verifier-execution-model`, `benchmark-task-validity-checklist`, `terminal-bench-release-identity`) do not speak to this task's reward semantics.
- Admit-candidates (2, from r42 per-entry pass, bytes identical): `benchmark-card-field-schema-2026-10-23` (S122-S124, 3/3 collide with lane) and `benchmark-card-adoption` (cites S135-S139; **now 3/5 collide** — S135-S137 landed in r43 as TB2 rows — and 5/5 once S138-S146 land). Both serve the contamination-cards frontier, not round 44's claims; adoption needs renumbering past S146 first and is no longer free of collisions (r43: 0).

## 5. Verdict tally (carried; bytes identical)
ADMIT-candidate 2, HOLD 42, REFUSE 21 (=65). No entry changed bytes, so no verdict re-derived.

## 6. Recommendation: none

1. Package unchanged since 2026-10-24 23:33:20 (four sha256 equal r42/r43).
2. Nothing staged covers feal/cryptanalysis graders or tool-mutant calibration; the two admit-candidates are card-family, out of round 44's frozen claims.
3. Any future staged-row adoption must renumber past **S146**; `benchmark-card-adoption` has now lost its zero-collision status.

Delta for the L1 vs round 43: package unchanged; collisions 45 → 54 (S129-S137 landed; → 63 after S138-S146); renumber floor S134 → **S146**; quarantine slice unchanged (S091, S105); verdict tally unchanged. Unresolved: guard `--selftest` still hard-codes `/tmp` (I ran the identical fixture through the real script instead); entry-level verdicts are carried not re-read; no live fetch.

VERDICT: merge-unchanged-collisions-54-recommend-none
