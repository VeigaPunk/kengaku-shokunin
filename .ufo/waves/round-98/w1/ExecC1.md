# ExecC1 — R98-C1 independent re-measurement

Lane: kengaku-shokunin, round 98. BASE 49a1c4f1097db7c923da56d4213cad75772ed1c0; T 8e37fc65d5649bb37166fdd6b1657445a8cb55b9. Seat: ExecC1 (leaf). Scratch /fast/scratch/hyaku/kengaku-r98/ExecC1 (removed after copying receipts). No production edits, no commits, no mutating git in lane.

## Tooling

Installed via uv (host pacman PAUSED per seat spec):
`uv venv -p 3.13 G && uv pip install --python G/bin/python pytest==8.4.1 chess==1.11.2`
Verified in-venv: python 3.13.16, chess 1.11.2, pytest 8.4.1. No other tools installed.

## What was independently exercised

1. **Frozen counter at T** (clone-T, detached at T, own grader venv G):
   `python3 plans/round98_c1_replay.py --lane . --rev 8e37fc65... --work SCRATCH/w-c1-T --grader-venv SCRATCH/G` → rc=0.
   Output: `LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass L10=pass`
   `TARGET executed_rows=42 member=regex-chess cells=file-artifact:33,serialization-schema:8 set_equals_base_plus_member=1 located=1 executed=1 cases=12 legs=60 mismatches=0 new_rows=8 new_rows_flagged=0 defects=0`
   `PREDICATE R98-C1 pass` — matches frozen predicate exactly. `set_equals_base_plus_member=1` with executed 41→42 and cells 32→33 / 7→8. Evidence: `ExecC1/c1-T.txt`.

2. **Frozen counter at BASE** (same clone, `--rev 49a1c4f1...`):
   rc=1 (as expected for a fail). All 10 legs fail (`L1=fail ... L10=fail`), `TARGET executed_rows=41 ... cells=file-artifact:32,serialization-schema:7 set_equals_base_plus_member=0 located=0 executed=0 cases=0 legs=0 mismatches=0 new_rows=0 new_rows_flagged=0 defects=10`, `PREDICATE R98-C1 fail`. Evidence: `ExecC1/c1-BASE.txt`.

3. **Probe run twice from `git archive` of T** (archive-T, in-sandbox via bwrap, own venv):
   `G/bin/python plans/round98_regexchess_probe.py --work SCRATCH/w-probe{1,2} --grader-venv G` → rc=0 both, `mismatches 0`.
   Extracted `OBSERVATIONS_BEGIN...OBSERVATIONS_END` blocks (24 lines: 12 CASE + 12 DETAIL) — identical to committed `corpus/evidence/round98/regexchess-probe.txt` for both runs (run1, run2, committed OBSERVATIONS all equal byte-for-byte; header differs only in `LANE_TIP HEAD` vs `e1a3afd9...`, which is expected from an archive checkout and is not part of OBSERVATIONS). Evidence: `ExecC1/probe-run1.txt`, `ExecC1/probe-run2.txt`.

4. **Hand rebuild of all 12 DETAIL digests** (outside probe, from archive-T bytes): decompressed solve.sh base64/gzip output, applied each probe transform, `json.dumps`, sha256[:16]. All 12 committed DETAIL lines reproduced exactly (C01 raw 19dbeb84…, C03 4f53cda1…, C04 5d122949…, C05 eb37c9e3…, C06 f8b4b080…, C07 1dfb1292…, C08 f454bd60…, C09 dae5c342…, C10 1c6a66f8…, C11 ab8236d5…, C12 4dc7986c…; C02 absent trivial). Independent evidence that committed DETAIL digests are valid for the frozen captures/transforms.

5. **Frozen-hash check at T**: all 13 frozen-instrument hashes + 4 candidate-bytes hashes from `plans/round-98-claims.md` recomputed in archive-T — all OK.

6. **Hand pytest runs outside probe** (path-rewritten `test_outputs.py` with absolute `/app/re.json` → scratch path, real pytest 8.4.1):
   - C04 (dup-first-drop-second): **4 passed, rc=0, 573s**. `pytest-C04.txt`
   - C07 (invented-ep): **4 passed, rc=0, 568s**. `pytest-C07.txt`
   - C09 (lookup-table): **4 passed, rc=0, 0.34s**. `pytest-C09.txt`

## Gap-case mechanism (hand-constructed)

Solver output for the first tested position (startpos `rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1`) has 20 lines = 20 legal successors. Line 0 is g1h3 (`...7N...`), line 1 is g1f3 (Nf3, `...5N2...`).

### C04 — dup-first-drop-second

Appended pair `\\A([^\\n]*)\\n[^\\n]*` → `\\1\\n\\1` replaces `line0 \n line1` with `line0 \n line0`. Result: 20 lines, each entry legal (per-line membership check passes), count check passes (20==20), but set inequality: **the missing legal move is g1f3 (Nf3)** — trimmed FEN `rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R b KQkq -` — duplicated instead is g1h3. Grader performs membership-per-line + length equality, never set equality, so it passes. Hand pytest rc=0 confirms.

### C07 — invented-ep

Appended `(?m)^(\\S+ b \\S+) - ` → `\\1 h6 ` rewrites every true `-` ep field to `h6`. The grader's fallback `x.rpartition(" ")[0]+" -" in python_chess_moves` maps any invented ep square back to `-`, so every forged line passes membership. Verified by executing `run_solution` on startpos under C07 pairs: first output ends `b KQkq h6`, `forgiven=True`. Hand pytest rc=0 confirms. C08 negative also verified by inspection: castling-forced `-` is not forgiven because `x.rpartition(" ")[0]+" -"` replaces the *ep* field only; dropping KQkq → `-` yields a trimmed string `... b - -` that is neither in legal nor in its rpartition image.

### C09 — lookup table

Builder imports the captured grader module, hooks `verify_legal_moves` to record FENs called during the first 3 games (108 recorded, 103 unique), and writes one anchored literal `\\A<re.escape(fen)>\\Z` pair per tested position with the board's true `b.fen()` output for every legal (non-underpromotion) move. No move generation — each tested FEN matches exactly one literal. C10 (minus last entry) → that Naroditsky-Ivanchuk position falls through, `run_solution` returns the white-to-move input unchanged, fails only that game. Hand pytest rc=0 (0.34s, since anchored literals short-circuit the 40k-pair regex chain).

## Verdict

**R98-C1 met; independently corroborated.** At T the frozen counter passes with the exact frozen TARGET line (`executed_rows` 42, set equality 41+1, cells 33/8, 60 legs, 0 mismatches, 8 unflagged new rows, 0 defects); at BASE it fails. All 12 committed DETAIL digests independently recomputed and matched. Probe OBSERVATIONS reproduced identically in two fresh runs. The three gap cases were hand-rebuilt and pass the real captured grader under real pytest, with C04 missing **g1f3 (Nf3)** on the first tested position. No defects found in the counter/probe/replay path; no frozen instrument changed. C2 was not in seat scope beyond reading the claims (frozen gate hash and PROVENANCE.md candidate hash verified at T).

## Findings / risks

- Both probe re-runs and the C1 counter pass. The counter's own L6 re-run (inside `round98_c1_replay.py`) is one of the three probe executions observed; my two standalone probe runs match it and the committed OBSERVATIONS.
- `result > pass` ambiguity: none — `PREDICATE R98-C1 pass` printed verbatim at T.
- The solve solution itself emits ep-signal lines for double pushes; C07's forgery exploits the same `rpartition` fallback that legitimately forgives those — worth noting that the fallback cannot distinguish a real ep square from an invented one.

## Blockers

None. All required commands ran in scratch; scratch was removed after copying receipts into `.../w1/ExecC1/`.

Report: .ufo/waves/round-98/w1/ExecC1.md
