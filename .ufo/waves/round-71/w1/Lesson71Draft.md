# Lesson71Draft — round-71 lesson scribe (wave w1)

Seat: `Lesson71Draft` (scribe, leaf; no subagent dispatch). Lane
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`, branch `master`; lane tip read with
`git rev-parse master` → `d8a77d3f2b4c8747dbc3a5bcf458b23160a459e0` (freeze commit on base
`1cb49cac`). Wrote only `corpus/lessons/round-71.md` (new) and the two round-71 additions to
`corpus/README.md`; no commit, no battery, no port lock taken, no tool installed or upgraded.

## What I ran (commands + rc)

| # | command | rc / result |
|---|---|---|
| 1 | `read plans/round-71-claims.md`, `corpus/lessons/round-70.md`, `corpus/QUALITY.md`, `corpus/ledgers…` (README, LOG, spot-check) | read |
| 2 | `git rev-parse master` | `d8a77d3f…59e0` |
| 3 | `git log --oneline 1cb49ca..master` | 1 commit: `d8a77d3f round-71: freeze …` |
| 4 | `git diff --stat 1cb49ca master` | 19 files, +2118/−2; LOG +8, README +4/−2, round-70 lesson +8, nginx entry +7 |
| 5 | `git cat-file -e d8a77d3:.ufo/waves/round-71/c1-control.txt` | **rc 128**, `fatal: path … exists on disk, but not in 'd8a77d3'` |
| 6 | `git ls-tree -r --name-only d8a77d3 -- .ufo/waves/round-71/` | `c2-red-before.txt`, `census-before.txt`, `w1-spec.json`, `w1-validate.*`; no `c1-control.txt` |
| 7 | `curl -sS -o /tmp/r71hf/instruction.md -w '%{http_code}' <pin>/hf-model-inference/instruction.md` | HTTP 200, 1264 B, 28 lines, sha256 `29151c5b2306f522f38fa905de3d34566865829355e5ca0895f4fca04d51dcc1` |
| 8 | `curl … <pin>/hf-model-inference/tests/test_outputs.py` | HTTP 200, 4239 B, 107 lines, sha256 `61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857` |
| 9 | `curl … <pin>/hf-model-inference/tests/test.sh` | HTTP 200, 295 B, 13 lines, sha256 `6528c4c4…42e8f` |
| 10 | `curl … <pin>/hf-model-inference/task.toml` | HTTP 200, 943 B |
| 11 | `cmp /tmp/r71hf/tests/test_outputs.py corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py` | identical (rc 0) |
| 12 | `sha256sum corpus/evidence/round71/hf/instruction.md` | `29151c5b…d1cc1` = the live fetch |
| 13 | `git show d8a77d3f:plans/round71_c1_hf_probe.py \| sha256sum` | `d5ce2fa5871bb3d2b7b956f9f92d6e23ee21b7508b5da6dc113f6c3a2c1aa82e` = receipt `PROBE`/`PROBE_BLOB` |
| 14 | `sh scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` (before, from the committed capture) | rc 0; 236 data rows; 25 `W04`; sha256 `5bbde4ee…9fcde` |
| 15 | same command, after S245/S246 + the entry landed | rc 0; 238 data rows; 25 `W04`; stdout sha256 `5bbde4ee…9fcde` (byte-identical to #14) |
| 16 | `grep -cE '^\|[[:space:]]*S[0-9](3,)[[:space:]]*\|' corpus/SOURCES.md` (the item's literal pattern) | `0`, rc 1 |
| 17 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `238`, rc 0 |
| 18 | `grep -c 'executed 3 of 8' SKILL.md` / `… 'executed 4 of 8' …` | `0` / `1` (row `SKILL.md:78`) |
| 19 | `grep -nE '^\|[[:space:]]*S24[56][[:space:]]*\|' corpus/SOURCES.md` | rows at `:260` (S245) and `:261` (S246), status `mined`, used-by `corpus/knowledge/tb2-hf-model-inference-offline.md` |
| 20 | `sed -n '1p' merge/…/grader-predicate-input-types.md \| od -c` | line 1 is `\n` (blank) |
| 21 | `git ls-files \| grep -c 'lanes/kengaku'` | `0` (the entry's own-work path is not held) |
| 22 | `grep -rn 'setup=[1-9]' corpus/evidence/round71 /fast/scratch/hyaku/kengaku-r71` | no round-71 receipt with a nonzero setup count |
| 23 | `grep … 'SUMMARY cases=8 legs=32 mismatches=0 setup=0$'` vs prefix | `0` / `1` (the writer emits `… exc=2`; the checker recomputes the field) |
| 24 | read seat reports: `HfBatteryR71`, `ReceiptReview71`, `LegPricing`, `LegWitnessAudit`, `DefectGateReverify`, `DepthGateRerun`, `CaseTableAudit71`, `SourceOpen71`/`SourceOpen71-rows.txt` | read |

No battery and no gate was executed by this seat; the receipt, checker, gate, selftest and
mutant outputs are cited from the seats that ran them (`HfBatteryR71.md` §1 `CHECK_RC=0`;
`ReceiptReview71.md` §2 rc 0; `DefectGateReverify.md` tip/selftest/mutants rc 0).

## What I found

### Delivered lesson (the item)

`corpus/lessons/round-71.md` — 183 lines, sections `## Gate` (18), `## Mistakes` (73),
`## Census` (92), `## Verdicts` (110), `## Limits` (155).

- **Gate.** S245 admit (instruction: live 2026-11-03, HTTP 200, 1264 B, 28 lines, sha256
  `29151c5b…d1cc1`, `cmp` = committed capture, 16-word quote at line 3); S246 admit (grader:
  HTTP 200, 4239 B, 107 lines, sha256 `61a686d6…f87857`, `cmp` = committed capture, 8-word
  quote lines 29-30). `merge/kengaku` `grader-predicate-input-types.md` **reject** on three
  grounds of its own bytes: triad offset (blank line 1, `source:` `:2-3`, `recheck:` `:5`),
  id collision (`S143`/`S144` here are `feal-linear-cryptanalysis` README/solve.sh at
  `corpus/SOURCES.md:160-161`, not Toolathlon), and an unheld own-work artefact
  (`lanes/kengaku/round7/…` → `git ls-files` count 0), with a flip that names the exact rows
  and artefact to stage. Assimilation: none. Census before→after: 236 → 238 rows, rc 0 both,
  25 `W04` both, stdout byte-identical.
- **Mistakes.** Five data rows, each with command-level evidence and a captured-by:
  1. dispatched census pattern `S[0-9](3,)` prints `0` vs `{3,}` → `236` (DepthGateRerun §Census;
     re-run by me, commands 16-17);
  2. `E2a`'s `SUPERSEDED_SENTENCE = "states the same bodies"` (`plans/round71_c2_routed_defects.py:169`)
     accepted for the claims' "verbatim" condition; the original sentence is at nginx entry
     `:14-15` and the first erratum at `:92-95` (DefectGateReverify §P2), closed by the appended
     `E-D2a` at `:96-99`;
  3. red-before run with an instrument absent at base (`python3 …/base.NFi4/plans/round71_c2_routed_defects.py`
     → rc 2, `[Errno 2]`; DefectGateReverify §P3);
  4. the do-nothing control is labelled "committed at freeze" (`plans/round-71-claims.md:59`)
     but is absent from `d8a77d3` (command 5, rc 128) — its content is correct, its claimed
     commit is not;
  5. leg-level `LEG-COVERAGE` read at assert-site granularity: 6 of 19 asserts priced, 13 not,
     `:107` unreachable under the frozen modes (LegPricing §4b; CaseTableAudit71 §Leg-coverage
     arithmetic and ADD-ONE K9).
  One candidate **refused for lack of observation**: no receipt in the lane or scratch records
  a nonzero `setup` count, and the frozen probe sets `SO_REUSEADDR` at
  `plans/round71_c1_hf_probe.py:327-338` — the suggested five-`SETUP` first run is not in this
  round's bytes.
- **Census.** Commands 14-15, plus the corrected counter (17) and the mid-landing `E11` capture
  history (the L1 re-captured at 22:28; both captures now sha `5bbde4ee…9fcde`).
- **Verdicts.** R71-C1 admitted on its frozen sentence (8/8 `agree=True`, `:34`
  `LEG-COVERAGE legs=4 seen_p=4 seen_f=4`, `:35` `SUMMARY … mismatches=0 setup=0 exc=2`, `:36`
  pass, checker rc 0, control refuses, replicate identical, counters 0/1) with the leg-vs-assert
  calibration stated; R71-C2 admitted on its frozen predicate (`DEFECTS n=6` → `n=0`, selftest
  4/4, mutants 4/4) with the E2a fragment gap and the red-data red-before named.

### README (the item)

- `corpus/README.md:567` — round-71 lesson index row (gate decisions, five Mistakes rows plus
  one refused candidate, census 236 → 238, both verdicts).
- `corpus/README.md:807-814` — `## Round-71 supporting artifacts (2026-11-03)` block (knowledge
  entry, lesson, S245/S246 + census, evidence paths, counters, wave).

### Findings routed to the L1 (reported, nothing edited outside my two files)

1. **`corpus/QUALITY.md` Q53's count inverts the seats' tally.** Q53 reads "`CaseTableAudit71`
   found six of the grader's nineteen assert sites without a negative witness"; `LegPricing` §4b
   counts **six with** a witness (`:13`, `:22`, `:31`, `:77`, `:86`, `:103`) and thirteen
   without, and `CaseTableAudit71` reports exactly one reachable-but-unpriced line (`:107`). The
   criterion's example and K9 proposal match the audit; the "six … without" is the line to
   reconcile. Q53 cites `corpus/lessons/round-71.md` `## Mistakes`, which now carries this row.
2. **`c1-control.txt` was not in the freeze commit** (command 5) while the claims call it
   "committed at freeze"; committing it with the landing makes the sentence true of the round.
3. **`corpus/evidence/round71/census-after.txt` was red mid-landing** (25 `W04` + 2 `E11`, rc 1,
   22:24) before the knowledge entry existed; refreshed at 22:28 to the green byte-identical
   capture. Recorded in the lesson so the transient is not read as the after-state.

## Files written (mine only)

- `corpus/lessons/round-71.md` (new; L1 commits)
- `corpus/README.md` (two insertions: the `:567` lesson row and the `:807-814` block; the
  `:95` knowledge row is `KnowledgeEntryDraft`'s)

## Verdict

**The lesson item is complete**: Gate (two tier-A admits with live date/bytes/sha256/quotes, one
`merge/kengaku` reject with reason and flip, census before→after), five evidence-backed Mistakes
rows plus one candidate refused as unobserved, Census with commands and rc, and one Verdict line
per claim with the calibration gaps named rather than smoothed. The claims' own verdicts stand
as the seats measured them (R71-C1 and R71-C2 both admitted on their frozen sentences); the
three L1 items above are corrections to prose/state, not to any predicate, vector, digest, kill
rule or target.

## Out of scope / limits

- Did not commit, push or run any mutating git/jj; did not edit `SOURCES.md`, `SCORECARD.md`,
  `LOG.md`, `QUALITY.md`, the report, `plans/`, `scripts/` or any sibling lane.
- Did not execute the C1 battery or either gate/selftest/mutant battery; those are cited from
  the seats' reports and re-derived only where a read-only command suffices (digests, counters,
  census, commit-tree probes).
- The live fetches used `/tmp/r71hf/` (files < 50 MB); no scratch directory was left behind.
- No tool was installed or upgraded.
