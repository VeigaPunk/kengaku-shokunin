# R35MutC1Quotes — V3 counter-check mutation report (round 35 wave 1)

Seat: R35MutC1Quotes (executor, leaf). Target: C1 counter check V3
(`plans/round35_c1_verify.py` v3) — entry structure and located-quotes validation.

## What was done

1. Read frozen claims (`plans/round-35-claims.md`) and the V1–V6 verifier source; pinned
   capture files under `corpus/evidence/round35/tb2-eval/` read before the probe.
2. Built a fixture clone per the lane fixture rule (sparse checkout of the surfaces V3 touches,
   plus capture files and probe script copied in; `rev-parse --show-toplevel` verified before any
   write; no commits; clone removed after evidence was captured):
   ```
   D=/tmp/k35-WOMG; git clone -q --no-checkout --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"
   git -C "$D/lane" sparse-checkout set --no-cone 'corpus/evidence/round35/tb2-eval' \
     'corpus/evidence/round35/tb2-grader-probe.txt' 'corpus/knowledge' 'corpus/SOURCES.md' \
     'corpus/README.md' 'plans/round35_c1_verify.py' 'plans/tb2_grader_probe.py'
   git -C "$D/lane" checkout -q master
   top=/tmp/k35-WOMG/lane   # git rev-parse --show-toplevel
   cp -rf <lane>/corpus/evidence/round35/tb2-eval/. "$D/lane/corpus/evidence/round35/tb2-eval/"
   cp <lane>/corpus/evidence/round35/tb2-grader-probe.txt "$D/lane/corpus/evidence/round35/"
   cp <lane>/plans/tb2_grader_probe.py "$D/lane/plans/"
   ```
3. Wrote a minimal entry at `corpus/knowledge/tb2-protein-assembly-grader.md` in the clone:
   triad `source:` lines for S105/S106/S107 (each carrying its pinned URL), `verified-at: 2026-10-25`,
   `recheck: on-release`, `## Negative space` containing "falsifiable", `## Located quotes` with
   12 rows (8 from `test_outputs.py`, 2 from `test.sh`, 2 from `instruction.md`), all quotes ≤25
   words and byte-exact substrings of the cited capture lines, plus the probe receipt summary line
   verbatim. Variant entries preserved under
   `.ufo/waves/round-35/build/R35MutC1Quotes/<mutant>.entry.md` (scratch).
4. For each mutant, wrote the variant over the entry and ran
   `python3 plans/round35_c1_verify.py --lane .` (cwd = clone). Baseline run: `V1 ok V2 DEFECT
   S105 present 0 times V3 ok V4 DEFECT index row absent or missing S105/S106/S107 V5 ok
   V6 DEFECT census exit 1, checks=6 defects=3, PREDICATE C1 fail` (V2/V4/V6 red only because the
   L1 has not yet integrated SOURCES.md/README/census surfaces — the live lane is read-only for
   this seat; V3 is the target check and passes).

## Mutant matrix (one property changed per mutant, from the same passing baseline)

| # | Property mutated | V3 outcome | Verifier line |
|---|---|---|---|
| baseline | — | pass | `V3 ok` |
| M1 | quote off by one line (`test_outputs.py:19` → `:20`, single-line cite) | **caught** | `V3 DEFECT quote not on test_outputs.py:20-20: Invalid number of lines in gblock.txt.` |
| M2 | quote with one changed char (`….` → `…!`) | **caught** | `V3 DEFECT quote not on test_outputs.py:19-19: Invalid number of lines in gblock.txt!` |
| M3 | 26-word quote (26 whitespace tokens) | **caught** | `V3 DEFECT quote over 25 words: Invalid number of lines in gblock.txt. T…` |
| M4 | curly → straight double quotes on one row | **SURVIVES (false green)** | `V3 ok` |
| M5 | missing falsifier ("falsifiable" → "testable") | **caught** | `V3 DEFECT negative space absent or has no falsifier` |
| M6 | verified-at date changed to 2026-10-24 | **caught** | `V3 DEFECT line 4 is not verified-at: 2026-10-25` |
| M7 | S106 source line swapped into S105's position | **caught** | `V3 DEFECT line 1 is not the S105 source line with its pinned URL` |
| M8 | recheck without date/cadence (`recheck: none`) | **caught** | `V3 DEFECT line 5 recheck lacks date/cadence` |
| M9 | quote cites a file outside the capture dir (`plans/round35_c1_verify.py:33`) | **caught** | `V3 DEFECT quote cites missing capture plans/round35_c1_verify.py` |

Result: **8 of 9 mutants caught; 1 survivor (M4).**

## Boundary probes (context, not part of the 9)

| Probe | V3 outcome |
|---|---|
| M4b: all rows straight-quoted | caught (`only 0 located quotes`) |
| M1b: `test_outputs.py:42-44` → `:41-44` (multi-line span still includes line 43) | **SURVIVES** (`V3 ok`) |
| M1c: `:42-44` → `:43-44` (same) | **SURVIVES** (`V3 ok`) |
| M1d: `:42-44` → `:45-46` (span excludes line 43) | caught (`quote not on test_outputs.py:45-46…`) |
| cite beyond EOF (`:999`) | caught (`quote not on test_outputs.py:999-999…`) |
| empty range (`:19-18`) | caught (`quote not on test_outputs.py:19-18…`) |

## Findings

- **False-green #1 (the 9-mutant finding): straight quotes are invisible.** The row regex
  (`^\|[^|]*\|\s*“(.+?)”\s*\|\s*`([^`:]+):(\d+)(?:-(\d+))?`\s*\|\s*$`) requires curly
  `“ ”`; a row written with ASCII `"` is silently skipped, not flagged. With ≥8 other valid rows
  the table still passes (12-row table → 11 counted → `V3 ok`). A fully straight-quoted table is
  caught, but a single corrupted row is not. V3 cannot distinguish "row in a different quoting
  convention" from "row missing".
- **False-green #2: off-by-one on a multi-line span survives whenever the span still overlaps the
  real line** (M1b/M1c). V3 checks substring membership over the joined span, so only shifts that
  exclude the quoted line are detected; single-line citations are the strict case (M1 caught).
- Caught set is otherwise precise: changed char, 26-word length, missing falsifier, verified-at,
  source-line order, cadence, out-of-capture file, beyond-EOF/empty ranges.
- Note: quote matching is substring-based, so a partial-line quote (e.g. a leading fragment of a
  source line) passes by design; and exactly 25 words passes (limit is `> 25`).

## Verdict

V3 catches 8 of the 9 specified single-property mutants. The straight-vs-curly-quote mutant (M4)
survives — a false-green finding — plus the multi-line span-shift family (M1b/M1c).

VERDICT: v3-mutants-8/9
