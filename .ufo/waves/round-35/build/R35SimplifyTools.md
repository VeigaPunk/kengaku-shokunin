# R35SimplifyTools — simplifier review (kengaku r35 wave 1)

Reviewed (at freeze commit `11d64530179b78e33ba6074fc77d63d36ee7ac31`):
`plans/round35_c1_verify.py`, `plans/tb2_grader_probe.py`, `plans/defect_ledger.py`.

Method: all runs happened in a fixture clone (`mktemp -d /tmp/k35-APzK` → `/tmp/k35-APzK/lane`,
git clone `--no-checkout --shared`, sparse checkout of `plans/ corpus/ scripts/ SCORECARD.md`
and the two round-34 build files, `checkout master`, toplevel verified; uncommitted lane files
copied in per fixture rule: `corpus/evidence/round35/**`, `corpus/knowledge/tb2-protein-assembly-grader.md`,
`corpus/{SOURCES,README,QUALITY,defects.jsonl}.md|jsonl`, `corpus/lessons/round-34.md`, `round-35.md`,
`SCORECARD.md`, `.ufo/waves/round-34/assimilation/captures/{tb2-eval,nec-s091-reopen.html}`).
Clone removed at the end; live lane untouched throughout (no writes, no git/jj mutations;
`git status --porcelain | wc -l` unchanged at 109432). No tool installs needed (uv 0.13.0,
patch present; nothing recorded under the operator channel rule).

## Baseline (old code, in clone)

- `python3 plans/round35_c1_verify.py --lane . --fleet /home/vgpnk/Projects/shokunin` → exit 1
  ```
  V1 ok
  V2 ok
  V3 ok
  V4 DEFECT knowledge files=41 index rows=42 (want 42/42)
  V5 ok
  V6 ok
  checks=6 defects=1
  PREDICATE C1 fail
  ```
- `python3 plans/defect_ledger.py --lane .` → exit 1
  ```
  R34-D1 status=open observed=pass agree=NO untracked=0
  R34-D2 status=open observed=fail agree=yes committed_mirror_paths=109413
  R34-D3 status=open observed=pass agree=NO listed=6 evaluator_listed=True bad=0
  R34-D4 status=open observed=pass agree=NO correction_lines=1
  R34-D5 status=open observed=fail agree=yes erratum_lines=1 r35_mistake_row=False
  rows=5 closed=0 observed_pass=3 mismatches=3
  PREDICATE C2 fail
  ```

These are the freeze snapshot pre-repair (V4 red because the entry is untracked at freeze;
D2/D5 observed-fail). Expected state, not code defects. V5 passed: fresh probe run byte-matched
the receipt (biopython=1.85 via the `uv run --no-project --with biopython==1.85` shim; base
python 3.14.8 has no Bio, so the shim path is deterministic here).

## Findings

### Dead code — none
Every constant, helper, import, and parameter is exercised: c1 `PIN/RAW/ENTRY/CAP/RECEIPT/FILES/ROW_RE`,
`sha/rows` and all six v-functions; probe `CODONS/gc/windows_ok/back_translate/components/fusion/
build_cases/run_grader` (18/18 cases, incl. `max_nt` which is printed, not dead); ledger
`BRANCH/R34/R34_QUOTE/CHECKS` and all five checks. No unused imports, no unreachable branches,
no dead variables. Underscore-unpacked cells in `v2` are required for unpacking, not dead.

### Duplicated logic
- c1 `v3` had two byte-identical section-extraction regexes (`## Negative space`, `## Located quotes`)
  → unified into `section(text, heading)` (Diff 2).
- Deliberate cross-file duplication left alone (independent instruments; unifying would create a
  new shared convention): the SHA256SUMS parse regex in c1 `v1` vs ledger D3; the grader digest
  `44a05a24…` in c1 `FILES` vs probe `GRADER_SHA256`.
- Probe `windows_ok` re-states the grader's sliding-GC rule — intentional independent restatement, kept.

### Needless complexity
- c1 `v3` read the entry file twice; single read (Diff 1).
- Ledger D1 built a list then filtered empties; `splitlines()` inline (Diff 3).
- Probe: no worthwhile simplification found; already lean (documented above).

## Proposed diffs (3 — all verified byte-identical)

Each diff is in `…/.ufo/waves/round-35/build/R35SimplifyTools/`; each applies cleanly with
`patch -p0` (verified: re-applied copies `cmp` identical to the built "new" variants).

1. **c1_v3_single_read.diff** — `v3`: `lines = p.read_text().splitlines()` →
   `text = p.read_text()` once, `head = text.splitlines()[:5]`; delete the second
   `text = p.read_text()`. Same bytes on disk → same parsed data → identical output.
2. **c1_v3_sections.diff** — module-level `section(text, heading)` helper; the two searches use
   the same regex strings and search semantics, so identical matches/defect strings.
3. **ledger_d1_splitlines.diff** — `r34_d1`: `git(...).split("\n")` + empty-filter →
   `[x for x in git(...).splitlines() if x]`. Both drop only the trailing empty string; same list.

Run matrix (clone cwd, identical args; stdout/stderr captured, exit codes recorded):

| variant | stdout | stderr | exit |
|---|---|---|---|
| c1 old (`plans/round35_c1_verify.py`) | 123 B | 0 B | 1 |
| c1 new (`c1_step2.py`) | 123 B | 0 B | 1 |
| ledger old (`plans/defect_ledger.py`) | 411 B | 0 B | 1 |
| ledger new (`ledger_step.py`) | 411 B | 0 B | 1 |

`cmp` confirms stdout and stderr byte-identical for both tools; exit codes equal (1/1).
Frozen predicate lines (`checks=…`, `PREDICATE …`), row formats, docstrings, and predicate
sentences are untouched.

## Bug flags (flagged, not simplified — behavior-changing)

- **B1 — c1 V5 ambient-Biopython version skew.** `v5` picks `[sys.executable] + probe` whenever
  `import Bio` succeeds, whatever its version; the probe prints `biopython={Bio.__version__}`.
  The receipt was captured under the pinned shim (1.85). A checker environment with any other Bio
  version would yield a different header → spurious `DEFECT` though the grader result is identical.
  Recommend: always use the `uv run --no-project --with biopython==1.85` shim, or assert
  `Bio.__version__ == "1.85"` before trusting the local interpreter.
- **B2 — ledger JSONL parse outside the per-row try.** The list comprehension
  `[json.loads(l) for l in … if l.strip()]` runs before the per-row `try`; a malformed line
  crashes the whole ledger (traceback, exit 1) with no `rows=` line — the frozen predicate output
  silently disappears instead of reporting an observed failure row. Move the parse inside the
  per-row handling/try.
- **B3 — ledger D4 hardcoded line indices.** The observation reads `draft[7]` and
  `harness[11:13]` (exact line positions). Any harmless edit above those lines silently changes
  what is observed (false pass or false fail). Anchor on content, not indices.
- **B4 — probe `run_grader` catches only `AssertionError`.** A non-assertion exception inside the
  grader (`KeyError`/`IndexError`/…) escapes and crashes the entire probe (traceback, exit 1)
  instead of producing a case-level `observed=fail` row; the counter's V5 then reports a byte
  mismatch rather than an actionable failing case.

Minor note: ledger D3 reads `SHA256SUMS` without an `is_file()` guard; a missing manifest surfaces
as a generic `error FileNotFoundError` note (acceptable, but slightly less precise than D1's
"untracked=…" style).

## Notes
- No changes proposed to `tb2_grader_probe.py` (no dead code, no safe simplification found; see B4).
- The three diffs are each output-neutral in isolation (verified jointly; each change is
  independently byte-identical by construction).
- No diff touches frozen behavior: predicates, output lines, exit codes, docstrings all unchanged.

## VERDICT: simplify-3-diffs-4-bugs
