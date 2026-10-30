# YAGNI proposals — `plans/round55_c2_entryargv.py` (seat SP1CounterScope, r55 w1)

Propose-only pass. The target was **never edited**; every removal below was applied to a
scratch copy and proven behavior-preserving on a 7-fixture matrix + the counter's own
selftest (`evidence/tx-*.txt`). Target analyzed as landed in the working tree (untracked at
analysis time, lane HEAD `248a42b8c73b…`, frozen base tip `798f5e9ef30e…`),
sha256 `2bf9e66ce3d5bace914cdd3402f43333edf81eb05c12819d6e819fe199c6ea74`, 431 lines.

Lab matrix (all fixtures toplevel-guarded git fixtures built in scratch, never the lane):

| case | ledger/registry state | expected killer |
|---|---|---|
| F1 abbreviated-selftest | frozen controls case: ledger adds `--selft`, registry plain | L1 + L3 |
| F2 uv-decoy-script | frozen controls case: ledger `uv run … -c…`, registry plain | L1 + L2 |
| FA consistent-abbrev | ledger token-equal to registry cell `python3 … --selft` | **L3 only** |
| FB consistent-inline | both sides `python3 plans/fixture_gate.py -cprint(inline)` | **L2 only** |
| FC name-collision | rows `X` and `X:`; ledger row `X:` non-dict | exercises bad_decl skip + sp-dict guard |
| FD non-dict row | ledger row is a list | exercises sp-dict guard |
| FL1 extra-token | ledger adds flag-shaped `--quiet` (prefix of no body flag) | **L1 only** |

Observed sole-firer lines on pristine: FL1 `BINDING l1=1 l2=0 l3=0`; FB
`BINDING l1=0 l2=1 l3=0`; FA `BINDING l1=0 l2=0 l3=1`. L4 is the sole observer of truth in
every green run (selftest case 1 passes only because the executed exit matches the
declaration; static legs alone cannot produce `RUN executed=1 … PREDICATE pass`).

## Per-leg ruling (acceptance)

- **L1 — KEEP.** The binding core and the kill-rule surface (ledger-side tampering). Sole
  firer on FL1 (extra flag-shaped token: `--quiet` prefixes no body flag so L3 is silent,
  no wrapper/`-c` so L2 is silent). Neither L2 nor L3 compares ledger argv to the registry
  cell. Removal also breaks the frozen ROWS line (`argv_defect=` covers L1 entries by
  design) and both frozen fixture kills (each prints an `ARGV-DEFECT`).
- **L2 — KEEP.** Not implied by L1+L3. FB proves sole teeth: a registry cell that *itself*
  declares an inline `-c` token passes L1 (consistency) and L3 (`-cprint(inline)` is not a
  prefix of any body flag) and is caught only by L2 (`WRAPPER-DEFECT … (-c)`). Like L3, L2
  guards the registry cell itself once L1 makes ledger==registry. Removal breaks the frozen
  `wrapper_defect=` field and the uv-decoy kill attribution.
- **L3 — KEEP.** Not implied by L1+L2 — this answers the seat question directly. L1 only
  enforces ledger↔registry *equality*; a registry cell declaring `--selft` on both sides is
  perfectly consistent (L1 clean) and wrapper-free (L2 clean); only L3's body-flag prefix
  check fires (FA: `l1=0 l2=0 l3=1`, sole firer). "L3 is dead once L1 enforces token
  equality" is false: token equality binds the ledger to the cell, it says nothing about the
  cell's own flags. L3 is also explicitly frozen ("defense in depth behind L1") and its
  `abbrev_defect=` field is part of the frozen after-predicate output.
- **L4 — KEEP.** The only observational leg; no static leg can observe an exit code or an
  evidence fragment. The frozen predicate requires `RUN executed=<n_reg> timeout=0
  mismatched=0 evidence_missing=0 laundered=0` and TIPSTATE declared==observed.

No leg is redundant given the others; each has a fixture on which it is the only firer.

## Removal proposals (behavior-preserving, proven on the matrix)

### P1 (APPLY) — drop dead `import time`
Line 47. `time.` has zero references in the module (the r54 `run_row` owns the clock; this
file calls it via `m.run_row`). Proof: `evidence/tx-V1-no-time.txt` byte-identical to
`tx-pristine.txt` (modulo the variant tag line) over all 7 cases + selftest.
```diff
-import time
```

### P2 (APPLY) — drop the four write-only rebound globals
Lines 56–59 (`REGISTRY`/`LEDGER`/`SCHEMA`/`MIN_REASON_WORDS = None`), the `global`
statement at line 68, and the four rebinds at lines 78–81. All four are write-only: grep
shows no read after assignment; the code uses everything through `m.*`; the only external
loader (`plans/round55_c2_controls.py::_load`) reads just `mod.evaluate`. Keep `_R54` — it
is the memo-cache and is load-bearing. Resulting `_load_r54` body:
```diff
-REGISTRY = None   # r54.REGISTRY_HEADING
-LEDGER = None     # r54.LEDGER  (plans/round54-entrytruth.json)
-SCHEMA = None     # r54.SCHEMA  (r54-entrytruth-v1)
-MIN_REASON_WORDS = None  # r54.MIN_REASON_WORDS
 ...
 def _load_r54():
     """Import the unchanged round-54 module (same pattern as round55_c2_controls.py::_load)."""
-    global _R54, REGISTRY, LEDGER, SCHEMA, MIN_REASON_WORDS
+    global _R54
     ...
     _R54 = mod
-    REGISTRY = mod.REGISTRY_HEADING
-    LEDGER = mod.LEDGER
-    SCHEMA = mod.SCHEMA
-    MIN_REASON_WORDS = mod.MIN_REASON_WORDS
     return mod
```
(Also refresh the two comment lines that speak of "Rebound … constants" to say "imported";
the constants comment at lines 54–55 is the only prose touched.) Proof:
`evidence/tx-V2-no-rebound-globals.txt` identical to pristine. Note `_mk_fixture` already
writes the schema string `"r54-entrytruth-v1"` literally (as does controls), so nothing
else references the removed names.

### P3 (APPLY, recommended) — dedup `_keep` into the borrowed r54 helper
Delete the local `_keep` (lines 178–180, byte-identical to `r54._keep`) and call
`m._keep(work, r)` at the two call sites (lines 281, 286) — `m` is in scope in `evaluate`.
Proof: `evidence/tx-V4-dedup-keep.txt` identical to pristine.
```diff
-def _keep(work: Path, r: dict) -> None:
-    (work / f"disagreed-{re.sub(r'[^A-Za-z0-9_.-]', '_', r['name'])}.txt").write_text(
-        f"exit={r['rc']} sec={r['sec']}\n{r['out']}")
 ...
-                _keep(work, r)
+                m._keep(work, r)
```

### P3b (REJECTED dedup, keep the local `HEAD_ROW`)
Deleting the local `HEAD_ROW` and using `m.HEAD_ROW` inside `_mk_fixture` raises
`NameError: name 'm' is not defined` — `_mk_fixture` has no `m` in scope
(`evidence/tx-V4b-headrow-rejected.err.txt`). A `_load_r54()` call inside a fixture builder
trades 4 lines for an import dance. Keep the local constant.

## Keep rulings for things that *look* deletable (with proof they are not)

### P4 (KEEP — latent dead code, removal NOT behavior-preserving)
In `binding_static_legs`, the half-clause
`or any(d.startswith(f"{n}:") for d in s["bad_decl"])` never matches r54's `bad_decl`
format: r54 appends **bare names** (`res["bad_decl"].append(n)`) while the clause matches
`"name:"`-prefixed strings (only `argv_defect` uses that format). It is a no-op for every
realistic input. It must nevertheless stay byte-for-byte: the FC fixture (rows `X` and `X:`,
ledger row `X:` non-dict so `bad_decl == ["X:"]`) makes `"X:".startswith("X:")` true, and
pristine then *skips row X's binding legs entirely* (`LAUNDERED X declared green`,
`evidence/tx-pristine.txt`), while a clause-removed variant raises the ARGV-DEFECT instead.
Contrived but reachable ⇒ removing it changes behavior. "Fixing" it to `n in s["bad_decl"]`
would also change behavior (dict-valued rows in `bad_decl` currently still receive L1–L3
checks). Keep as-is; if L1 touches this function for other reasons, a comment noting the
two r54 formats is the only safe change.

### P5 (KEEP — load-bearing)
`if not isinstance(sp, dict): continue` in `binding_static_legs` is the *actual* protection
for non-dict ledger rows, precisely because P4's filter never skips them. Removing it
crashes with `AttributeError: 'str' object has no attribute 'get'` (FC) and
`'list' object has no attribute 'get'` (FD) instead of the clean
`BAD-DECL … PREDICATE R55-C2 fail` (delta receipt: `evidence/tx-V5-no-spdict-guard.txt`,
exactly 2 exception blocks, all other cases byte-identical).

### P6 (KEEP — provably unreachable defense-in-depth)
L2's argv-shape guard, L3's `isinstance(argv, list)` early-out, and the `"python"` entry in
`INTERPRETERS` can never fire/never be exercised: every row reaching L2/L3 already passed
r54 `entry_mode_ok` (list[str], len ≥ 2, argv[0] ∈ {python3, uv}) after P5's skip, and
r54 rejects `python`/other interpreters before L2 runs. Removal would preserve behavior
today but couples the private helpers' correctness to a *sibling frozen module's* filter
for a 3-line saving; the file's own design language is defense-in-depth (L3 is documented
as such). Keep.

### P7 (KEEP — documented intent, not dead weight)
`job()` re-derives `spec["entry_argv"] = registry_entry_argv(s["rows"][n])` although it is
provably equal to the ledger argv for every executed row (L1-clean ⇒ equality; L1-defective
rows are filtered from `names`). The recompute *is* the L4 docstring's contract ("executed
hermetically with the REGISTRY cell argv"). Keep.

## Integration risks found while statically probing the real lane (read-only; data items for L1, not counter defects)

1. **17 registry cells can never pass L1 as written.** Their entry cells contain usage
   placeholders (`<lesson.md>`, `DIR`, `[--verbose]`, `REV`, `PATH...`, `<scratch>`, …)
   which can never token-equal the ledger's concrete argv: adoption-check, anchor-digest-
   check, coverage-census, gate-flip-check, gate-timing, ledger-tip, mutant-direction-check,
   package-gate, round-close-check, round28-census, round50-c1, round53-c2, scratch-root-
   guard, sources-adopt, stage-scan, tb2-grader-probe, tip-receipts. Unless the cells are
   normalized to concrete canonical argv before the after-run, the frozen predicate fails
   statically with 17 `ARGV-DEFECT` lines. (Registry/ledger counts today: 78/83; the 5
   ledger-extra rows are the planned round-55 ledger additions.)
2. **`tb2-grader-probe` is unpassable under frozen L1+L2.** Its entry cell is
   `` `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .` ``
   → `registry_entry_argv` returns None ⇒ L1 raises "registry entry cell has no python3
   command", and no ledger argv can token-equal None; any wrapper-bearing ledger row is
   separately a WRAPPER-DEFECT by L2. Needs a dated amendment (cell rewrite to a plain
   `python3 …` entry with the biopython requirement relocated, or a verdict-map change)
   before the after-run.
