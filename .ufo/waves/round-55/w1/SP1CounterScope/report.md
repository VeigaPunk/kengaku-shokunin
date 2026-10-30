# SP1CounterScope — report (kengaku r55, w1, v2)

YAGNI pass over `plans/round55_c2_entryargv.py` (bounded-wait; propose, never edit).
Read-only against the lane plus my wave dir. No subagents. No tool installs.

## What the counter is and when it landed

The target appeared in the working tree during my watch (untracked `??` at analysis time;
lane HEAD `248a42b8c73b6415963f16b13127a9aa6d4c997c`; frozen claims at `80afa61314fa…`,
base tip `798f5e9ef30e…`). Analyzed bytes:
sha256 `2bf9e66ce3d5bace914cdd3402f43333edf81eb05c12819d6e819fe199c6ea74`, 431 lines.

## What I ran (commands → exit codes)

All scratch under `/fast/scratch/hyaku/kengaku-r55/SP1CounterScope/` (deleted before
yield; receipts copied to `evidence/`).

| check | command (cwd) | exit |
|---|---|---|
| baseline selftest | `python3 plans/round55_c2_entryargv.py --selftest --work $S/baseline/st` (lane) | 0, `4/4 PASS` |
| frozen before-state | `python3 plans/round55_c2_controls.py --case abbreviated-selftest --against r54` | 0 (`PREDICATE R54-C2 pass`, true entry exit=1 — laundering demonstrated) |
| frozen before-state | `--case uv-decoy-script --against r54` | 0 (same shape) |
| frozen fixture kills | `--case <both> --against r55` | 0 each (`ARGV-DEFECT` + `ABBREV-DEFECT` / `WRAPPER-DEFECT`, `PREDICATE R55-C2 fail`, counter rc=1) |
| lab baseline | `prove.py pristine` (lab) | 0 |
| variants | `derive.py` (V1 no-time, V2 no-rebound-globals, V4 dedup-_keep, V5 no-spdict-guard) | 0 |
| rejected dedup receipt | `derive_v4b.py` (HEAD_ROW → m.HEAD_ROW) | 1, `NameError: name 'm' is not defined` (expected) |
| identity diffs | `diff <(tail -n +2 tx-pristine.txt) <(tail -n +2 tx-V*.txt)` | V1/V2/V4 IDENTICAL; V5 differs only by 2 EXCEPTION blocks (FC, FD) |
| real-lane static probe | inline python: r54 registry_rows/load_ledger + r55 registry_entry_argv over the lane tree | 78 registry rows, 83 ledger rows, 17 L1 mismatches, 1 unpassable uv cell |

Lab matrix (toplevel-guarded git fixtures in scratch): F1/F2 frozen controls cases, FA
consistent-abbrev, FB consistent-inline, FC name-collision `X`/`X:`, FD non-dict ledger
row, FL1 extra-token `--quiet`, plus the counter's own selftest per variant.

## Findings (full detail: `SP1CounterScope/proposals.md`)

Per-leg ruling — **keep all four legs**, each has an empirical sole-firer fixture:
- L1 sole firer on FL1 (`BINDING l1=1 l2=0 l3=0`).
- L2 sole firer on FB (`l1=0 l2=1 l3=0`): a registry cell that itself declares `-cprint(inline)`.
- L3 sole firer on FA (`l1=0 l2=0 l3=1`): the seat question "is L3 dead once L1 enforces
  token equality" is answered **no** — L1 binds ledger↔registry *equality*; a registry cell
  declaring `--selft` on both sides is consistent (L1 clean) and wrapper-free (L2 clean);
  only L3's body-flag prefix check catches it. L3 guards the registry cell itself.
- L4 is the only observational leg (exit codes, evidence fragments).

Removal proposals proven behavior-preserving (byte-identical transcripts, 7 cases + selftest):
- **P1** drop `import time` (zero `time.` references).
- **P2** drop write-only rebound globals `REGISTRY/LEDGER/SCHEMA/MIN_REASON_WORDS`
  (+ `global` shrink + rebinds). Only external loader (controls) reads `mod.evaluate`.
- **P3** dedup `_keep` → `m._keep` (bodies byte-identical; `m` in scope at both call sites).
  The analogous `HEAD_ROW` dedup was tried and **rejected with a receipt**: `_mk_fixture`
  has no `m` in scope → NameError.

Keep rulings for look-alike dead weight (each with disproof of safe removal):
- bad_decl half-clause (`d.startswith(f"{n}:")`): never matches r54's bare-name bad_decl
  format (latent no-op) BUT removal demonstrably changes behavior on name-collision rows
  (pristine swallows row X's binding checks → `LAUNDERED X`; clause-less variant raises
  ARGV-DEFECT). Keep byte-for-byte.
- `isinstance(sp, dict)` guard: **load-bearing** — without it FC/FD crash
  (`AttributeError: 'str'/'list' object has no attribute 'get'`) instead of clean BAD-DECL.
- L2/L3 shape guards and `INTERPRETERS`' `"python"`: provably unreachable today (r54
  entry_mode_ok filters first) — kept as zero-cost defense-in-depth per the file's design.
- `job()`'s registry-argv recompute: provably equal to ledger argv post-filter; kept as the
  documented L4 contract.

Defects/risks found (data items for L1, NOT counter defects; I touched nothing):
1. **17 registry cells can never token-equal their ledger argv** (usage placeholders
   `<lesson.md>`, `DIR`, `[--verbose]`, `REV`, …): adoption-check, anchor-digest-check,
   coverage-census, gate-flip-check, gate-timing, ledger-tip, mutant-direction-check,
   package-gate, round-close-check, round28-census, round50-c1, round53-c2,
   scratch-root-guard, sources-adopt, stage-scan, tb2-grader-probe, tip-receipts. The
   frozen after-predicate fails statically unless cells are normalized before the after-run.
2. **`tb2-grader-probe` is unpassable under frozen L1+L2**: cell is
   `uv run --no-project --with biopython==1.85 python3 …` → `registry_entry_argv` → None →
   L1 "no python3 command" is unfixable ledger-side; wrapper argv is L2-killed. Needs a
   dated amendment before the after-run.
3. Ledger has 5 rows the registry lacks (round54-c1, round54-c2, round55-c2,
   round55-c2-controls, round55-c3) — the planned ledger additions; counter prints EXTRA 5 today.

## Files written

- `.ufo/waves/round-55/w1/SP1CounterScope/proposals.md` (the deliverable diffs + rulings)
- `.ufo/waves/round-55/w1/SP1CounterScope/report.md` (this file)
- `.ufo/waves/round-55/w1/SP1CounterScope.md` (scoped findings summary)
- `.ufo/waves/round-55/w1/SP1CounterScope/evidence/` — tx-pristine, tx-V1, tx-V2,
  tx-V4-dedup-keep, tx-V5, tx-V4b-headrow-rejected.err, base-r54/r55-{abbreviated-selftest,
  uv-decoy-script}.txt

Nothing else in the lane was created, modified, or deleted. No git/jj mutation anywhere
(fixture git-init/commit ran only inside scratch fixture dirs with toplevel guards).

## Dead ends

- First `uv-decoy`-style L2-only fixture used the raw token `-cprint('inline')` in the
  ledger; shlex-splitting of the registry cell strips the quotes, so L1 fired before L2 —
  rebuilt the fixture with the shlex-split token to isolate L2.
- HEAD_ROW dedup (P3b): NameError, rejected, receipt kept.
- Re-running fixtures over pre-existing dirs failed at `git commit` ("nothing to commit");
  fixture builder now wipes its dir first. No impact on results.
- Note: the first r55-abbreviated kill run and this report's baseline runs happened while
  the target was still untracked; if L1 amends the file before commit, the diffs here
  re-anchor by the sha256/line anchors recorded in proposals.md.

## Installs

None.
