# R8CounterSoundness — R55-C2 entry-argv counter: FALSE-PASS route hunt

Hunt target: `plans/round55_c2_entryargv.py` (landed in the live lane tree during this
seat's bounded wait, 12:38, untracked sibling build; selftest 4/4 PASS at probe time).
All fixtures below are complete and runnable: registry SKILL.md row + gate script +
`plans/round54-entrytruth.json` ledger row, committed as a git fixture, run through
`mod.evaluate(root, root, work, 1, 60, False)`. Drivers and raw outputs:
`receipts/r55-probe-results.txt` (copied from scratch before cleanup); driver sources
are reproduced in `report.md`.

Every route was run against the landed counter. Verdicts:

| # | route | counter verdict | kill-rule false pass? |
|---|-------|-----------------|----------------------|
| F1b | worker-layout + hermetic-env fingerprint | **SURVIVES (PREDICATE pass, exit 0)** | **YES — strongest candidate** |
| F1  | hermetic-env fingerprint only | **SURVIVES (exit 0)** | conditional (plain-env ground truth only) |
| F2  | evidence-fragment self-spoof (red row) | **SURVIVES (exit 0)** | no (reason is false, observation true) |
| F3  | unicode homoglyph script path | FAILS — ARGV-DEFECT | no |
| F4a | runtime-built flag abbreviation | SURVIVES L3 (l3=0) | no (cell form truthful) |
| F4b | `--mod=value` equals-form abbreviation | SURVIVES L3 (l3=0) | no (truthful) |
| F4c | argparse builtin `-h/--help` abbreviation | SURVIVES L3 (l3=0) | no (truthful) |
| F5  | registry-cell tokenizer edge forms | all fail-closed or consistent | no |
| W1  | wrapper inventory beyond {uv,pipx,poetry,npx,uvx} | FAILS by construction | no |
| W2  | absolute interpreter path / `env` / `exec -a` | FAILS — ARGV-DEFECT | no |
| C1  | canonical ledger-argv tampering | FAILS — twice (L1 + exec uses REG) | no |

## F1b — worker-layout + hermetic-env fingerprint laundering  **SURVIVES**

The counter executes each row via `m.run_row` in a per-worker clone at
`<work>/w<i>/src` with `hermetic_env` (unchanged r54 module). A gate can fingerprint
exactly that environment and exit 0 only there. The frozen ground-truth methodology in
`round55_c2_controls.py` (r54 branch) runs the truth as `hermetic_env` + `cwd=<fixture
root>` — which this fingerprint ALSO distinguishes from the counter run. So the
counter passes a green row whose declared entry exits 1 under the controls' own truth
methodology.

Fixture (complete):
- `SKILL.md` row: `` | `fixture-gate` | gate | `python3 plans/fixture_gate.py` | `0` ok · `1` bad | none | none | none | kengaku | ``
- `plans/fixture_gate.py`:
  ```python
  #!/usr/bin/env python3
  import os, re, sys
  hermetic = (os.environ.get("GIT_CONFIG_NOSYSTEM") == "1"
              and os.path.basename(os.environ.get("GIT_CONFIG_GLOBAL", "")) == "empty-gitconfig"
              and os.environ.get("GIT_TERMINAL_PROMPT") == "0")
  cwd = os.getcwd()
  in_worker = (os.path.basename(cwd) == "src"
               and re.fullmatch(r"w\d+", os.path.basename(os.path.dirname(cwd))) is not None)
  if hermetic and in_worker:
      print("selftest ok"); sys.exit(0)
  print("entry failed: fixture gate is broken on purpose"); sys.exit(1)
  ```
- ledger row: `{"entry_argv": ["python3", "plans/fixture_gate.py"], "entry_exit": 0, "entry_state": "green", "timeout_s": 60}`

Observed (r55 counter): `ROWS ... argv_defect=0 wrapper_defect=0 abbrev_defect=0 bad_decl=0`,
`BINDING l1=0 l2=0 l3=0`, `RUN executed=1 timeout=0 mismatched=0 evidence_missing=0 laundered=0`,
`TIPSTATE declared green == observed green`, `PREDICATE R55-C2 pass`, **exit 0**.
Ground truth of `python3 plans/fixture_gate.py`:
plain env, cwd=root → **exit 1**; hermetic env, cwd=root (controls style) → **exit 1**;
hermetic env, cwd=`w0/src` clone (counter style) → exit 0.

Kill-rule assessment: all static legs clean + counter passes + declared entry truly
exits otherwise under the controls' hermetic ground truth → meets the frozen kill-rule
letter ("a soundness break, not a documentation rewrite": no registry/ledger text is
rewritten; the registry cell and the ledger argv are truthful). The inherited r54
execution environment (worker-clone cwd + marker env) is the laundering channel, not
the binding legs. Countermeasure options for the L1/integration: execute each row a
second time from the repo-root cwd and require exit-code agreement, or ground-truth
rows from the repo-root cwd rather than the worker clone.

## F1 — hermetic-env fingerprint only  **SURVIVES (weaker)**

Same gate without the `in_worker` term. Counter: `PREDICATE R55-C2 pass`, exit 0.
Truth: plain env → exit 1; **hermetic env, cwd=root → exit 0** (env markers are
layout-independent). Kill status: fires only if "truly exits otherwise" is judged in a
non-hermetic environment; under the controls' hermetic truth it does not fire. F1b is
the strictly stronger form.

## F2 — evidence-fragment self-spoof on a red row  **SURVIVES (not a kill)**

L4 checks red rows by substring: `sp.get("evidence") not in r["out"]` over the
script's own combined stdout+stderr. A row can declare a fragment the script prints on
its normal failing path while the `reason` claims a failure mode that was never
exercised.

Fixture: gate prints `error: config file missing: freeze.json`, exit 1. Ledger row:
`entry_exit=1, entry_state="red"`, `evidence="error: config file missing"`,
`reason="… exits 1 claiming a registry-vs-ledger row mismatch that was never
exercised; the fragment is a generic substring of its own output"`.
Counter: `PREDICATE R55-C2 pass`, exit 0; truth exit 1 both envs.
Assessment: the observation (red) is true, so this is **not** a kill-rule false pass;
it is an L4 hardness gap — the counter can verify fragment presence, never fragment
provenance. This is the same class the frozen claims already manage as data
(`round35-c1-coverage` evidence re-derivation, correction (a)).

## F3 — unicode homoglyph in the script-path token  **FAILS (caught)**

Fixture: `plans/gate.py` (exit 1) and `plans/gаte.py` — Cyrillic small a U+0430 in
place of Latin `a` (bytes `67 43 30 74 65 …`, visually identical) — exit 0. Registry
cell declares the ASCII path; ledger `entry_argv` uses the homoglyph path.
Counter: `ARGV-DEFECT fixture-gate: script mismatch` (r54 `entry_mode_ok` byte
comparison), `PREDICATE R55-C2 fail`, exit 1; row excluded from execution.
L1 comparison is exact list equality (`led != reg`), so r55's binding leg catches it
too had r54 not fired first. Verdict: fails-with-evidence; survives only under a
normalizing comparison, which the landed counter does not do.

## F4a — runtime-built flag name (L3 enumeration gap)  **SURVIVES L3 (not a kill)**

Gate: `LONG = "--se" + "lftest"; p.add_argument(LONG, action="store_true")` — the
literal string `--selftest` appears nowhere in the source. `BODY_FLAG` regex over the
body yields `{--se}`; token `--selft` is not a proper prefix of any body flag →
`abbrev_defect=0`. Cell declares `python3 plans/fixture_gate.py --selft`; ledger binds
it (L1 clean); execution: argparse `allow_abbrev` default → selftest ok → exit 0.
Counter: `BINDING l3=0`, `PREDICATE R55-C2 pass`, exit 0. Truth of the cell form:
exit 0 in both envs → observation equals truth → **not a kill**. Documented as a real
defense-in-depth gap in L3 (exactly the "flags built at runtime" class the seat spec
names), fail-closed only behind L1's exact binding.

## F4b — `--mod=value` equals-form abbreviation  **SURVIVES L3 (not a kill)**

Gate defines `--mode` (value); cell declares `python3 plans/fixture_gate.py
--mod=selftest`. Token `--mod=selftest` is not a strict prefix of `--mode`
(`f.startswith(t)` fails), so `abbrev_defect=0`; argparse accepts the abbreviation
with an explicit value → exit 0. Counter: `PREDICATE R55-C2 pass`, exit 0; truth of
the cell form exit 0 → not a kill. L3 completeness note: an equals-suffix defeats the
strict-prefix test even for statically visible flags.

## F4c — argparse builtin `-h/--help` abbreviation  **SURVIVES L3 (not a kill)**

Cell declares `python3 plans/fixture_gate.py --hel`; body flags from source regex are
`{--selftest}` (builtin `--help` is runtime-added by argparse, absent from the source
text) → `abbrev_defect=0`; argparse resolves `--hel` → help text, exit 0. Counter:
`PREDICATE R55-C2 pass`, exit 0; truth exit 0 → not a kill. Same class as F4a: L3's
body-flag set is source-text-only.

## F5 — registry-cell tokenizer edge forms  **no false pass**

`registry_entry_argv` = first backtick span in the entry cell **starting with
`python3`**, `shlex.split`. Characterization (all observed on the landed counter):

- plain span → `['python3', 'plans/fixture_gate.py']`
- quoted path `` `python3 'plans/fixture_gate.py'` `` → quotes stripped, same tokens
- two python3 spans → first wins
- prose with backticked flags after the span → ignored (span-only)
- unbalanced quote → `shlex.ValueError` → `None` → row is ARGV-DEFECT (fail-closed)
- `` `python plans/…` `` (no 3) → `None` → ARGV-DEFECT (fail-closed; effectively
  python3-only entries can ever be clean)
- `` `Python3 …` `` → `None` → fail-closed
- `` `uv run python3 …` `` → no span starts with python3 → `None` → fail-closed
- `` ` python3 …` `` (leading space) → `.strip()` → parses

No crafted cell made the parser emit an argv that executes differently from the cell's
plain reading while keeping L1 clean: any span the parser accepts, an auditor reads
the same way, and `shlex` semantics match list-exec semantics. Residual risk stays
with the counter's parser choices (first-span, shlex), not a demonstrated route.

## W1 — wrapper forms beyond the frozen inventory  **FAILS by construction**

`WRAPPERS = {uv, pipx, poetry, npx, uvx}`; `INTERPRETERS = (python3, python)`.
Candidates `pip run`, `hatch run`, `pdm run`, `conda run`, `mise exec`, `asdf exec`
cannot reach execution: a cell whose span does not **start with python3** parses to
`None` → L1 flags the row; and any wrapper behind a python3 argv[0] is a non-interpreter
first token → both L1 and L2 reject. `-c` attached (`-cprint(1)`) and separate
(`-c print(1)`) are both caught by `t.startswith("-c")` (probe: both WRAPPER-DEFECT).
No false pass found. (Benign note: `--config` is correctly NOT flagged — the `-c`
test needs `-c` literally, second char `c`.)

## W2 — absolute interpreter path / `env` / `exec -a`  **FAILS**

L1 is exact token equality against the cell; the cell's span starts with the literal
token `python3`. `["/usr/bin/python3", "plans/gate.py"]` ≠ `["python3",
"plans/gate.py"]` → ARGV-DEFECT; `env python3 …` has argv[0]=`env` → L2
`argv[0] not in INTERPRETERS`; `exec -a` requires a shell first token → L1/L2 reject.
`python3 -` (stdin program) is rejected upstream by r54's `entry_mode_ok` (`script is
None` → "argv shape"). All fail-closed.

## C1 — canonical ledger-argv tampering  **FAILS (doubly)**

The r54-class attacks (`--selft` added by the ledger; `uv run … -c …` decoy) are the
two frozen fixtures; both are killed by the landed counter with their attributed lines
(`ARGV-DEFECT` / `WRAPPER-DEFECT` naming the case, `PREDICATE R55-C2 fail`, exit 1 —
reproduced by this seat via `plans/round55_c2_controls.py --case … --against r55`,
"ROUTE kill demonstrated"). Beyond them: any ledger argv that differs from the parsed
cell is ARGV-DEFECT, and independently **execution ignores the ledger argv** —
`run_row` is fed `spec["entry_argv"] = registry_entry_argv(s["rows"][n])` — so even a
hypothetical L1 miss would still execute the registry form.

## Residual summary

- Binding legs L1–L3 are sound on the argv/wrapper/abbreviation channels; the canonical
  laundering class is closed (twice).
- One kill-rule candidate survives: **F1b environment/cwd fingerprinting** (and its
  weaker form F1) — the counter's inherited hermetic worker-clone execution is
  detectable by the measured script; recommend the L1 consider a repo-root-cwd
  re-execution leg or ground-truth from the repo-root cwd.
- L4 hardness gaps that are not kills: evidence-fragment self-spoofing (F2) and L3
  source-only flag enumeration (F4a/F4b/F4c) — all leave observation equal to the
  declared cell form's truth.
