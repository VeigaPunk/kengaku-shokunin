# F35SimplifyLanded — simplifier review of the landed round-35 instruments (kengaku r35 wave 2, falsify)

Seat: F35SimplifyLanded (simplifier, leaf; no subagents). Lane tip: `dfee6fff631ebc5f623ba4506e5c7992a215401c` (master).
Scope: `plans/tb2_grader_probe.py`, `plans/round35_c1_verify.py`, `plans/defect_ledger.py` — dead code / needless
complexity; diffs proposed with old-vs-new output cmp proof; bugs flagged separately.
No lane file was written; all artifacts live in `.ufo/waves/round-35/falsify/F35SimplifyLanded/` (diff files, variants,
run outputs) and fixture clones under `/tmp`.

## 0. Landed state verified first (falsification substrate)

- Instruments are byte-identical between the freeze commit `11d64530` and the landing tip: `git diff --stat 11d64530 dfee6fff -- plans/{round35_c1_verify,tb2_grader_probe,defect_ledger}.py` → empty.
- Working tree == tip blobs: `git status --porcelain -- plans/...` empty; `sha256sum` of each working-tree file equals `git show dfee6fff:<path> | sha256sum` (defect_ledger `4e386677…`, round35_c1_verify `05a6137d…`, tb2_grader_probe `acd7d38d…`).
- Frozen counters run green at the tip, in the live lane and in a full fixture clone (sparse checkout of corpus/ plans/ .ufo/waves/round-34/ SCORECARD.md, toplevel verified == clone root):

```
$ python3 plans/defect_ledger.py --lane .
R34-D1 status=closed observed=pass agree=yes untracked=0
R34-D2 status=closed observed=pass agree=yes committed_mirror_paths=0
R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
R34-D4 status=closed observed=pass agree=yes correction_lines=1
R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
rows=5 closed=5 observed_pass=5 mismatches=0
PREDICATE C2 pass        # exit 0

$ python3 plans/round35_c1_verify.py --lane .
V1 ok … V6 ok
checks=6 defects=0
PREDICATE C1 pass        # exit 0
```

The C2 "before (freeze)" control (`rows=5 closed=0 observed_pass=0 … PREDICATE C2 fail`) is now green because the
round-34 committed-scratch mirrors were removed at the tip (D2 `committed_mirror_paths=0`). V5 green means the fresh run
of the probe is byte-equal to the committed receipt `corpus/evidence/round35/tb2-grader-probe.txt` (`cases=18
observed_pass=5 observed_fail=13 mismatches=0`).

## 1. Dead code — none found (confirmed by tool + manual census)

- `uvx --from ruff ruff check --select F,E9` on all three instruments → `All checks passed!` (no unused imports, no
  unused locals, no syntax issues). ruff 0.17.2 (already present via uv at `~/.local/bin/ruff`; no install/upgrade
  performed — my `uv tool install ruff` attempt was refused as "Executable already exists").
- Manual identifier census: every module-level constant and function has at least one call site — c1 `PIN/RAW/ENTRY/CAP/RECEIPT/FILES/ROW_RE`, `sha/rows/v1…v6`; probe `CODONS/gc/windows_ok/back_translate/components/fusion/build_cases/run_grader` (18/18 cases; `max_nt` and `wins` are printed diagnostics, not dead); ledger `BRANCH/R34/R34_QUOTE/CHECKS`, `git/r34_d1…d5`. Underscore-unpacked cells in `v2` are required for unpacking.

## 2. Needless complexity — 4 output-neutral diffs proposed

Diffs apply with `patch -p0` against the landed files; each was verified old-vs-new at the green tip:

| # | Diff file | Change | Stdout cmp | Stderr cmp | Exit old/new |
|---|---|---|---|---|---|
| 1 | `01-probe-drop-sorted.diff` | probe `back_translate`: drop redundant `sorted(CODONS[res])` — both key callables already end in the codon string `c`, so ordering cannot influence `min`/`max`, | identical (3399 B) | identical | 0/0 |
| 2 | `02-c1-v3-single-read-sections.diff` | c1 `v3`: read entry once; unify the two byte-identical section-extraction regexes into one `section(text, heading)` helper | identical (73 B) | identical | 0/0 |
| 3 | `03-ledger-d1-splitlines.diff` | ledger `r34_d1`: `split("\n")` + empty-filter → `splitlines()` inline | identical (418 B) | identical | 0/0 |
| 4 | `04-ledger-d2-splitlines.diff` | ledger `r34_d2`: same splitlines simplification (keeps the two git-output parses symmetric) | identical (418 B) | identical | 0/0 |

Run matrix (each pair executed from the lane with the frozen invocation; stdout/stderr captured separately, then `cmp`):

```
$ uv run --no-project --with biopython==1.85 python3 probe_old.py --lane <lane> > probe.old.out 2>probe.old.err   # exit 0
$ uv run --no-project --with biopython==1.85 python3 probe_new.py --lane <lane> > probe.new.out 2>probe.new.err   # exit 0
$ cmp probe.old.out probe.new.out && cmp probe.old.err probe.new.err     # IDENTICAL; probe.new.out == committed receipt (byte-equal)
$ python3 c1_old.py --lane <lane> > c1.old.out 2>c1.old.err; python3 c1_new.py --lane <lane> > c1.new.out 2>c1.new.err
$ cmp c1.old.out c1.new.out && cmp c1.old.err c1.new.err                # IDENTICAL (green: checks=6 defects=0, PREDICATE C1 pass)
$ python3 ledger_old.py --lane <lane> …; python3 ledger_new.py / ledger_new_d2.py --lane <lane> …
$ cmp ledger.old.out ledger.new.out && cmp ledger.old.err ledger.new.err  # IDENTICAL (rows=5 closed=5 observed_pass=5 mismatches=0)
```

Intermediate draft bug (mine, fixed before evidence): first c1 variant still used `sec.group(1)` after `section()` returned a
string → `V3 DEFECT error AttributeError: 'str' object has no attribute 'group'`. This was caught by the cmp matrix; the
final variant prints byte-identical green output. Not a bug in the landed instrument.

## 3. Bugs flagged (separate from simplification; all present in the landed tip)

- **B1 — c1 V5 ambient-Biopython version skew** (`round35_c1_verify.py:164-168`). V5 uses `[sys.executable] + probe`
  whenever `import Bio` succeeds, whatever its version; the probe prints `biopython={Bio.__version__}`. Receipt was
  captured under the pinned shim (1.85). Demonstrated: fresh venv with Biopython 1.88 →
  ```
  $ /tmp/k35b1-venv/bin/python3 round35_c1_verify.py --lane <lane>
  V5 DEFECT fresh probe output differs from receipt (exit 0)
  checks=6 defects=1   PREDICATE C1 fail   # exit 1
  ```
  A checker host with any Bio ≠ 1.85 spuriously fails the counter although the grader verdict is identical. Fix: always
  take the `uv run --no-project --with biopython==1.85` shim, or assert `Bio.__version__ == "1.85"` first.
- **B2 — ledger JSONL parse outside the per-row try** (`defect_ledger.py:119`). The list comprehension runs before any
  `try`; a malformed line or a missing `corpus/defects.jsonl` crashes with a traceback and **no `rows=` line** — the
  frozen predicate sentence silently disappears instead of reporting an observed-fail row. Demonstrated on a green
  fixture clone:
  ```
  # malformed line appended
  json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 17 (char 16)
  # file removed
  FileNotFoundError: [Errno 2] No such file or directory: '…/corpus/defects.jsonl'
  ```
  both exit 1 with no `rows=…`/`PREDICATE C2 …` output. Move the parse inside the per-row handling.
- **B3 — ledger D4 hardcoded line indices** (`defect_ledger.py:76-77`): observation reads `draft[7]` and `harness[11:13]`.
  Any harmless edit above those lines silently changes what is observed (false pass/false fail). Anchor on content, not indices.
- **B4 — probe `run_grader` catches only `AssertionError`** (`tb2_grader_probe.py:127-131`). A non-assertion exception
  inside the grader escapes and crashes the whole probe. Demonstrated with a synthetic grader module whose
  `test_gblock()` raises `KeyError`: traceback, exit 1, no case-level `observed=fail` row (V5 then reports a byte
  mismatch instead of an actionable failing case).

Corroborated minor notes (already documented by wave-1 seats; re-confirmed by code read):
- Unknown check names agree on `open` rows (`defect_ledger.py:122-124,132`): `fn is None → ok=False` counts as agreement
  for an open row, masking a broken ledger reference.
- Duplicate row ids are silently accepted; the `rows=5` pin lives only in the frozen claims sentence, not in the script
  (a drifted all-passing ledger would print `PREDICATE C2 pass` / exit 0 with `rows≠5`).
- Ledger D3 reads `SHA256SUMS` without an `is_file()` guard — a missing manifest surfaces as `error FileNotFoundError`.

## 4. Boundaries honored

No lane file touched (`git status --porcelain` before/after identical: only the falsify scratch dir untracked); no
`git`/`jj` mutations in the lane; fixture clones disposed (`rm -rf`); writes only under `.ufo/waves/round-35/falsify/F35SimplifyLanded/` and `/tmp/k35*`. Tooling: no new install (ruff 0.17.2 already present via uv; used `uvx --from ruff`).

VERDICT: simplify-4-diffs-4-bugs
