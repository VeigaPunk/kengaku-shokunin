# R34MutC2Harness — mutation-test report (kengaku round 34, hyaku run 7)

Seat: `R34MutC2Harness` (mutation tester). Target: round-34 mutation harness draft
`.ufo/waves/round-34/build/R34MutateDraft/round34_mutate.py` (sha256 `44156300…bd1f2`,
unchanged before and after this seat's work). Counter under test:
`.ufo/waves/round-34/build/R34C2CounterDraft/round34_defects.py` (sha256 `d8af348c…bab550`).
All scratch work lives in `.ufo/waves/round-34/build/R34MutC2Harness/`; no lane file outside
it was touched.

## 1. Baseline (pristine harness, real bytes) — RED

- `python3 round34_mutate.py --selftest` → exit 1, green gate fails:
  `SELFTEST green failed (1)` with `DEFECT N3 … .ufo/reports/round-31/kengaku.md is
  unreadable`, `DEFECT N4 … .ufo/reports/round-32/kengaku.md is unreadable`, `DEFECT N7 …
  round-33 lesson has no dated correction stating ledger sum 36+53=89`, `checks=8 defects=3`.
- `python3 round34_mutate.py` (end-to-end) → exit 1, aborts at the clean gate:
  `CLEAN exit=1` with the same three defects; `MUTANTS` line never reached.
- Root cause verified against the frozen tree `adaf25d`:
  - `git ls-tree -r --name-only HEAD` contains only `.ufo/reports/round-17/kengaku.md` —
    **no** `.ufo/reports/round-31|32/kengaku.md` (and none on disk: `.ufo/reports/` holds
    only `round-17/`). The counter's N3/N4 targets (`round34_defects.py:12-13`) do not exist
    in any archived sandbox → permanently red on pristine archive.
  - N7 is red because at HEAD the round-33 lesson lacks the dated `36+53=89` correction the
    counter requires (`round34_defects.py:121-127`).
- Consequence (standard mutation-testing rule): every real-bytes run — pristine or mutated —
  fails at the same green gate, so **real-bytes kills are inconclusive by baseline failure**.

## 2. Four harness mutants (bytes)

| id | file | edit | before → after sha256 |
|----|------|------|-----------------------|
| HM1 | `h1_wrongfile.py` | M1 target changed from `corpus/knowledge/provider-selfreport-eval-limits.md` (fallback first knowledge md) to `SKILL.md` (lines 53-55) | `44156300…` → `27413051…` |
| HM3 | `h3_nonempty_body.py` | M3 inserted section gains a non-empty body: `'## Round 33\n\n'` → `'## Round 33\n\none\ntwo\n'` (line 66) | `44156300…` → `8c163e60…` |
| HM5 | `h5_nowrap.py` | M5 replacement string equals the search string → no-op, no wrap (line 79) | `44156300…` → `44adce6a…` |
| HM7 | `h7_shorttoken.py` | M7 injected token shortened: `'x' * 350` → `'x' * 100` (total 110 chars < 300) (line 89) | `44156300…` → `4b336689…` |

Restoration: the draft file was never modified (hash identical before/after); scratch copies
are disposable per tasking; each copy's pristine hash is recorded above.

## 3. Detectors run

1. **Real bytes** `--selftest` on all four mutants: identical output to baseline
   (green fails N3/N4/N7, exit 1) — different code, same trace ⇒ no differential signal.
2. **Real bytes** end-to-end: identical to baseline (aborts at CLEAN; mutants never reached).
3. **Reduced-environment probe** `probe_mutants.py` (same scratch dir): builds a synthetic lane
   passing all eight N-checks (`GREEN LANE: exit=0 checks=8 defects=0`), then for each harness
   copy and each mutant `n=1..8` applies `mutate(sandbox, n)` and runs the counter, asserting
   exit 1 + `DEFECT N<k>` with the harness's own mapping (1/2→N8, 3→N2, 4→N7, 5→N5,
   6→N6, 7→N3, 8→N4). This lifts the archive-baseline failure and exposes per-mutant
   behavior conclusively.

Probe results (per harness, `MUTANTS total=8` line):

| harness | detected | crashes | undetected |
|---------|----------|---------|------------|
| pristine `round34_mutate.py` | M1 M2 M3 (3) | M5 M6 (NameError `replace_once`) | M4 (N2 fires, N7 expected), M7, M8 |
| `h1_wrongfile.py` | M2 M3 (2) | M1 (FileNotFoundError SKILL.md), M5 M6 | M4, M7, M8 |
| `h3_nonempty_body.py` | M1 M2 (2) | M5 M6 | M3 (N2 stays green), M4, M7, M8 |
| `h5_nowrap.py` | M1 M2 M3 (3) | M5 M6 | M4, M7, M8 |
| `h7_shorttoken.py` | M1 M2 M3 (3) | M5 M6 | M4, M7, M8 |

## 4. Verdicts (per mutant, vs pristine under the healthy-lane detector)

- **HM1 (wrong file) — KILLED.** M1 no longer reddens N8 (deletes an unchecked file; in the
  synthetic lane it crashes on missing `SKILL.md`, in the real archived lane it would delete
  a file no check reads). Harness gate on this op goes from DETECTED → UNDETECTED/crash.
- **HM3 (non-empty body) — KILLED.** M3 no longer reddens N2 (the inserted Round-33 section
  now has two content lines, which N2 accepts). DETECTED → UNDETECTED.
- **HM5 (no wrap) — SURVIVOR.** Detector output identical to pristine: both crash on M5 with
  `NameError: name 'replace_once' is not defined` before any file write. The wrap/no-wrap
  behavior is unobservable because `replace_once` is never defined in the harness (AST scan:
  function definitions are only `counter_path`, `run_counter`, `archive_tree`, `mutate`,
  `selftest`, `main`; usages at lines 79/82 reference an undefined name). No differential signal.
- **HM7 (short token) — SURVIVOR.** Detector output identical to pristine: M7 writes into
  `.ufo/waves/round-31/falsify/<first md>` (`round34_mutate.py:84-89`), but N3 reads
  `.ufo/reports/round-31/kengaku.md` (`round34_defects.py:12,70`) — the mutant never touches
  the file the check reads, so long and short tokens are equally UNDETECTED (exit 0,
  `checks=8 defects=0`). No differential signal.

Verdict: 2/4 killed, 2/4 survivors.

## 5. Additional coverage findings (harness cannot self-certify even with a green lane)

1. **M4 maps to the wrong check.** Blanking the Round-32 section fires `N2`
   (`Round 32 has fewer than two non-heading content lines`), never N7; harness expects N7
   (`round34_mutate.py:141`). Pristine harness therefore reports M4 as UNDETECTED on a
   healthy lane.
2. **M5/M6 are non-runnable** (`replace_once` undefined) — both crash the harness.
3. **M7/M8 target mismatches** — falsify copies under `waves/round-31|32/falsify/` are not
   the reports N3/N4 read (`reports/round-31|32/kengaku.md`); both mutants are invisible to
   the counter.
4. Net: on a fully green synthetic lane the pristine harness detects **3/8** (M1, M2, M3).
   The C2 acceptance `MUTANTS total=8 detected=8` is not satisfiable by this draft even after
   fixing the archive-baseline red (missing `reports/round-31|32/kengaku.md`, round-33 dated
   correction at HEAD).

Evidence commands and outputs are captured verbatim in §1/§3; per-file hashes in §2.

VERDICT: mut-c2harness (killed 2/4 — h1,h3 — survivors h5,h7; baseline red N3/N4/N7 on
archived HEAD + replace_once undefined + M4/M7/M8 mapping/target mismatches make real-bytes
runs inconclusive; healthy-lane probe: pristine harness detects 3/8, cannot reach 8/8)
