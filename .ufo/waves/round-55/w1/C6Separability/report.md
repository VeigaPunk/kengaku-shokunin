# C6Separability — seat report

Role: critic. Task: causal-separability audit of the three frozen R55 claims. Read-only; I wrote
only files under `.ufo/waves/round-55/w1/C6Separability*` plus scratch
`/fast/scratch/hyaku/kengaku-r55/C6Separability/`.

## What I ran

| Command | Cwd / args | Exit |
|---|---|---|
| `python3 -c "…"` | read `plans/round54-entrytruth.json` rows | 0 |
| `git log --oneline -8`; `git status --short`; `git show HEAD:<file>` (×several) | lane, read-only | 0 |
| `grep`/`awk`/`sed -n` reads of `plans/round52_c2_registry.py`, `round54_c2_entrytruth.py`, `round55_c2_entryargv.py`, `round55_c3_chess_probe.py`, `round55_c2_controls.py`, `round54_c1_anchor.py`, `SKILL.md`, `AXES.md`, prior `round-5{0,1,2}-claims.md`, `w1-spec.json` | read-only | 0 |
| `python3 plans/round55_c2_entryargv.py --lane . --dry` | lane (static legs only; **executes nothing**) | 1 |
| `python3 -c "import Bio"` (host) | check | 1 (ImportError) |
| `grep -c -- "--selftest"` on the five scripts | flag presence check | 0 |

The `--dry` run is safe and read-only by construction (`DRY static legs only: no predicate`; the
RUN/`--jobs` hermetic path is skipped; nothing is executed). Its legs read only `SKILL.md` and
`plans/round54-entrytruth.json`, both byte-clean at HEAD, so the dirty WIP tree does not perturb
the result. Receipt: `dry-static-legs-wip.txt`.

## Files I wrote (all inside my named outputs)

- `.ufo/waves/round-55/w1/C6Separability/analysis.md` — the analysis + verdict.
- `.ufo/waves/round-55/w1/C6Separability/report.md` — this file.
- `.ufo/waves/round-55/w1/C6Separability/dry-static-legs-wip.txt` — evidence receipt.
- `.ufo/waves/round-55/w1/C6Separability.md` — scoped-findings trailer (lane-relative path).

## Ruling (headline)

- **Separability verdict: PASS under the lane's operative reading** — the r52-standard
  "predicate reads disjoint inputs; each verifies and attributes its own verdict." All three
  counters are independently runnable; none can pass on a broken sibling state (the dependence
  surfaces as `LAUNDERED`/`MISSING`/`ENTRY-MISSING`/`extra` failures, never as a laundered pass).
- **But it is NOT pass-in-isolation for C1/C2** (only C3 passes alone). The coupling map is a
  declared premise of the freeze ("R55-C1's repair restores its true exit 0"), so report it as a
  precondition, not a discovered defect — provided the report names it.
- **Q2 (instrument disjointness): verified.** `round55_c3_chess_probe.py` shares no code and no
  read-surface with the C1/C2 instruments; the only edge is one-way (C1 advertises/registers the
  probe script; C2 re-executes its ledger entry).

## Defects found (report, do not fix — owned by the L1/E1/E4)

1. **C2 after-predicate unreachable at HEAD as scoped.** `--dry` reports `argv_defect=17
   wrapper_defect=1` while the frozen predicate requires `0/0`. The 17 are pre-existing rows
   whose registry entry cells document *generic* argv (`<expect.json>`, `DIR`, `REV`, `[--rerun]`,
   `PATH…`) vs the ledger's concrete argv — L1 demands token-equality. Neither E1 (5 new rows
   only) nor E4 (`round35-c1-coverage` + 5 rows only) is scoped to reconcile them.
2. **`tb2-grader-probe` has no truthful non-wrapper argv.** Its honest entry is
   `uv run … python3 plans/tb2_grader_probe.py` (`argv[0]='uv'` → `WRAPPER-DEFECT`) and there is
   no `python3` form (host `import Bio` → ImportError; the hermetic worker would match it).
   Deleting the registry row does not help: the script stays `ADVERTISED` inside the `uv run`
   text, so C1's gate then reports `MISSING`. Resolution needs either a truthful re-declaration
   `python3 …` red (degrades a working probe) or a freeze amendment to L2 — both are L1
   decisions, not seat fixes.
3. **`round54_c1_anchor.py` self-test trap for E1.** Its self-test is subcommand `selftest`
   (`:568`), *no* `--selftest` flag in the body. If E1 writes `--selftest` in that cell, the
   `selftest_unbacked` leg greps the body, finds none → `SELFTEST-UNBACKED 1` → C1 fails and a
   false cell lands. (E1's spec already warns; flagging the concrete trap.)
4. **Harm vectors are all partial-landing.** See `analysis.md` §4; the smallest correction is
   atomic integration (C1 rows + entryargv + probe + ledger rows + cell reconciliations in one
   measured-after tip, or revert the unmatched halves).

## Dead ends

- `AXES.md` is at the **fleet root** (`/home/vgpnk/Projects/shokunin/AXES.md`), not the lane —
  found via `find`, not a lane path guess.
- Sibling seats write both `w1/<Seat>.md` and `w1/<Seat>/` — confirmed the convention and
  matched it.
- Installs: none (no tools needed). Scratch `/fast/scratch/hyaku/kengaku-r55/C6Separability/`
  used only to stage a spec extraction; removed on exit.
