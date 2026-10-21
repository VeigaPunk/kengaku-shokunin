# FReviewAstContract — source_contract() AST extraction strictness (round-29 POST-CRASH FALSIFY)

writer: KengakuR29-2.FReviewAstContract-2

Scope of this item only: `source_contract()` in
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py` — AST extraction
strictness (order/names/literals, json.loads-before-enumerate, filename template, star import
recorded and never executed) and the attack question: *can a semantically different generator
still pass?*

**I did read the production source** (`plans/config_projection.py`, all 548 lines). This item's
contract explicitly permits it. I did not read or import `plans/config_projection.py` for any
oracle derivation — this item is a code-contract review, not an oracle item; the oracle items are
separate seats (FOracleText/Leaf/Provenance/Index).

No credential, cookie, auth-state content, host env value or private URL was read. The only
execution of generator-shaped code was of **my own mutants** in `/tmp`, against a synthetic stub
`browser_env.env_config` containing `*.invalid` values; the upstream module was never present,
never imported from the network, and no host environment value was consulted.

## Attack

1. Read `source_contract()` and enumerated every statement class it consumes and every class it
   silently ignores.
2. Built **14 well-formed mutants** of the pinned generator bytes
   (`plans/fixtures/r29/generate_test_data.py`, sha256 `45ddba7b…`): each preserves the shape the
   extractor looks for but changes the generator's *semantics*.
3. Fed each mutant to `source_contract()` and classified ACCEPT/REJECT.
4. For every ACCEPTed mutant, **executed the mutant generator** in a `/tmp` sandbox (stub
   `browser_env.env_config` with synthetic `*.invalid` values, pinned raw file as
   `config_files/test.raw.json`) and recorded the observable artifacts: exit code, number of
   per-index files written, `config_files/0.json`'s `task_id`, error text.
5. Separately re-derived the *strong* properties of the **pinned** generator by AST, to separate
   "the extractor is weak" from "the pinned numbers are wrong".

Harness (my scratch, not production):
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FReviewAstContract-2/probe3.py`
(also `probe.py`, `probe2.py`, `final-battery.json`, `semantic-results.json`, `audit.json`).

### Result of the attack — headline

```
TOTAL_MUTANTS 14 ACCEPTED 14 REJECTED 0
```

**Answer to the item's question: YES — a semantically different generator passes.** All 14
semantics-changing mutants were ACCEPTed by `source_contract()`; none of the six
`source_contract_unrecognized` raise sites (`:64`, `:68`, `:76`, `:78`, `:85`, `:88`) fired.

## Findings, by severity

### F1 — HIGH: the "per-task filename template" is not bound to any `open()`/`write()` call

- Location: `plans/config_projection.py:86` collects f-strings from anywhere in the enumerate loop;
  `:87-88` compares the collected list to one literal; `:91` publishes
  `"per_task_filename_template": "config_files/{idx}.json"`.
- The check proves only that **some** f-string with that literal text exists **somewhere** in the
  loop body. It is never tied to an `open()` argument, and it never checks that a per-index file is
  written at all.
- Mismatch, exact values:
  - M01 (f-string assigned to a local `name`, no per-task file written): **ACCEPT**; the published
    contract still says `per_task_filename_template = "config_files/{idx}.json"`. Execution witness:
    `per_index_files_written = 0`, `exit_code = 0`, `config_files_entries = 2`.
  - M02 (all tasks written into one `config_files/all.json`): **ACCEPT**; same published template.
    Execution witness: `per_index_files_written = 0`, `config_files_entries = 3`.
  - Control (unmutated generator) for contrast: `per_index_files_written = 812`.
- The instrument nevertheless reports 812 per-index artifacts per profile (`output_filename` at
  `:330`, `would_be_file_sha256` at `:333`), and `LIMITS` `:46` asserts a count of
  `813 would-be artifacts per profile`. That sentence is not established by the extractor.
- Impact: `per_task_filename_template` is a published, machine-readable fact about the generator
  that the extractor does not establish.

### F2 — HIGH: `data` may be mutated between `json.loads` and `enumerate`; the output-index mapping is not established

- Location: `:80-81` detects the parse by exact unparse; `:82-83` detects the loop by exact unparse
  of target and iterator. No constraint on bindings of `data` in between; `:91` publishes
  `"output_index": "enumerate position, not item task_id"`; `:330-334` and `:344` use it.
- Mismatch, exact values:
  - M07 (`data = [d for d in data if d["task_id"] % 2 == 0]` inserted before the loop): **ACCEPT**.
    Execution witness: `per_index_files_written = 406` (not 812), `config_files_entries = 408`,
    exit 0. The instrument still reports `task_profile_projections = 2436` and 812 tasks per profile.
  - M08 (`data = list(reversed(data))`): **ACCEPT**. Execution witness: the generator's
    `config_files/0.json` holds `task_id = 811`, while the instrument reports
    `output_filename = "config_files/0.json"` bound to `task_id = 0` with
    `index_equals_task_id = True`, and the instrument's own run reports
    `index_equals_task_id = 812`, `violations = 0`.
  - A reversed input therefore breaks the published index↔task-id mapping while the guard passes.

### F3 — HIGH: statements other than the six recognised `replace` calls are silently ignored; `raw` may be mutated arbitrarily

- Location: `:70-83` consumes only three statement shapes (recognised `raw.replace` assign, the
  exact-unparse parse assign, the exact-unparse `for` loop). Every other top-level statement of
  `main` is skipped **without any finding**. `:77-78` ("replace after parse") fires only for
  recognised replace steps.
- Mismatch, exact values (all **ACCEPT**):
  - M03 `raw = raw[:100]` → execution: `exit_code = 1`,
    `json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 8 column 5 (char 100)`,
    `per_index_files_written = 0`. The generator cannot produce the 812 artifacts at all; the
    instrument still projects 812 tasks per profile.
  - M04 `raw = raw.upper()` → execution: `exit_code = 1`,
    `json.decoder.JSONDecodeError: Expecting value: line 7 column 22 (char 90)`, 0 files.
  - M05 `raw = raw + " "` → accepted; only `config_files/test.json` differs from the pinned shape.
  - M06 `raw = raw + " "` placed **after** `json.loads` → accepted; the "replace after parse" guard
    at `:77-78` does not see it.
- Impact: the extractor's own stated purpose — that the six ordered replacements are the whole
  transformation — is not enforced.

### F4 — MEDIUM: "json.loads before enumerate" is not enforced

- Location: `parse_line` is set at `:80-81`, `loop` at `:82-83`, both published at `:90`. The two
  line numbers are never compared; only *replace-after-parse* is guarded (`:77-78`).
- Mismatch: M11 (the enumerate loop moved before `data = json.loads(raw)`): **ACCEPT**. The
  published contract is `parse_line = 23`, `enumerate_loop_line = 20` — i.e. the parse is reported
  *after* the enumerate. Execution witness: `exit_code = 1`,
  `UnboundLocalError: cannot access local variable 'data' where it is not associated with a value`.
- The named prereg dimension (parse before enumerate) therefore has no guard at all.

### F5 — MEDIUM: the star import is recorded but neither its level nor its binding to the six names is checked

- Location: `:65` selects `ast.ImportFrom` nodes with `node.module == "browser_env.env_config"` and
  `names == ["*"]`; `node.level` is never inspected. `:89` publishes
  `"env_config_star_import_line": star[0]`. Nothing binds the six replaced names to that import.
- Mismatch, exact values:
  - M09 (`from .browser_env.env_config import *`, level 1): **ACCEPT**; the contract still reports
    `env_config_star_import_line = 5`. Execution witness: `exit_code = 1`,
    `ImportError: attempted relative import with no known parent package`.
  - M10 (module-level `GITLAB = "http://shadowed.invalid"` after the star import): **ACCEPT**;
    contract still reports `env_config_star_import_line = 5`. Execution witness:
    `shadowed_value_occurrences_in_written_files = 770` — the shadowing binding, not the
    `env_config` value, is what the real generator substitutes.
- Note: the "never executed" half of this axis **is** solid — see Verified below.

### F6 — MEDIUM: the input file path and the entry point are never extracted

- Location: `:70-83` inspects `ast.Assign`/`ast.For` only; the `with open(...)` statement is an
  `ast.With`, and `if __name__ == "__main__": main()` is an `ast.If`; neither is inspected.
- Mismatch, exact values:
  - M12 (reads `config_files/other.raw.json`): **ACCEPT**. Execution witness: `exit_code = 1`,
    `FileNotFoundError: [Errno 2] No such file or directory: 'config_files/other.raw.json'`.
  - M13 (`main()` never invoked): **ACCEPT**. Execution witness: `exit_code = 0`,
    `per_index_files_written = 0`, `config_files_entries = 1` — the generator does nothing, and
    the contract still certifies the six replacements and the per-index filename template.

### F7 — LOW: the selftest's source-contract battery covers only four shapes

- Location: `plans/config_projection.py:459-473`. The four mutants are `order_swap`,
  `literal_rhs`, `extra_step`, `id_filename` — all four are the "obvious" shapes and all four are
  genuinely rejected.
- Observed selftest output (`python3 plans/config_projection.py --selftest`, exit 0):
  `SELFTEST clean cases=20 …,source_order_swap,source_literal_rhs,source_extra_step,source_id_filename,…`
- The prereg forbids claiming exhaustive mutation coverage, so this is context, not a prereg
  violation — but the 4-case battery is the only in-repo evidence that the extractor rejects
  different generators, and 14 mutants outside those four pass silently.

## Verified as genuinely strict (so the finding is not overstated)

- Token/order/name/literal check `:84-85` is strict: the `(token, name)` pair sequence must equal
  the pinned `ORDER`; a swap, a literal right-hand side, an extra recognised replace step and an
  `item['task_id']` filename are all rejected (confirmed by the four `source_*` selftest cases).
- The generator bytes are **never executed**: `plans/config_projection.py` contains no `exec(`,
  `eval(`, `__import__`, `importlib` or `spec_from_file`; the generator is only `ast.parse`d at
  `:63`. `subprocess` is used only at `:482` to re-run the instrument itself on a `/tmp` scratch
  copy. The `browser_env.env_config` import is never performed, so no credential-bearing module is
  touched.
- **The pinned generator satisfies the stronger properties** that the extractor fails to check
  (re-derived by AST from the pinned bytes): the loop's single `JoinedStr` **is** the first
  argument of the loop's only `open()` call; the only binding of `data` is `data = json.loads(raw)`;
  the only bindings of `raw` are the six `replace` calls; there are no module-level name bindings;
  the star import has `level = 0`; `main` is invoked under `__main__`.
- The pinned generator bytes are sha256-pinned by the manifest, whose own sha256 is hardcoded at
  `:24`, so a substituted generator is rejected earlier by `snapshot_tampered` (`:112`) /
  `manifest_tampered` (`:101`). Execution of the unmutated generator reproduced the instrument's
  shape exactly: 812 per-index files, `config_files/0.json` with `task_id = 0`.
- **Therefore round-29's measured numbers are not refuted by this item.** The instrument's own run
  (`python3 plans/config_projection.py --json`, exit 0) reports `findings = []`,
  `input_task_count = 812`, `profile_count = 3`, `task_profile_projections = 2436`,
  `index_equals_task_id = 812`, `violations = 0`, and the contract
  `parse_line = 20`, `enumerate_loop_line = 21`, `env_config_star_import_line = 5`,
  `per_task_filename_template = config_files/{idx}.json`.

## What would close each finding (no code written; this is a leaf review)

- F1: require the f-string to be the first argument of an `open()` call inside the loop, and require
  the loop body to contain exactly one such `open()`.
- F2: require that `data` has no binding other than the parsed assign between the parse and the
  enumerate loop.
- F3: require that every top-level statement of `main` that binds `raw` or `data` is one of the
  recognised shapes; raise `source_contract_unrecognized` otherwise.
- F4: require `parse_line < enumerate_loop_line`.
- F5: require `node.level == 0` and require no module-level binding of the six names.
- F6: extract and pin the input path literal and the `__main__` invocation.

## Residual risk and verification gaps

- [INFERENCE] The weak extractor is a latent gate weakness, not a current numeric error: with the
  manifest sha256 pins in place, a substituted generator is caught earlier
  (`snapshot_tampered`). The exposure is that the published `source_contract` fields and the
  `LIMITS` `:46` artifact-count sentence assert facts the extractor does not establish; a future
  re-pin of a *different* upstream revision would be certified by this weaker guard.
- [INFERENCE] `LIMITS` `:46` (one whole `test.json` per profile, 813 would-be artifacts) is asserted
  from reading the pinned generator, not from the extractor; my mutants show the extractor cannot
  support that sentence for any other generator.
- Verification gap: my mutants are constructed, not exhaustive; other unrecognised statement shapes
  (e.g. `with`/`try`/`if` bodies inside `main`) are likewise unexamined by the extractor and were
  not separately probed here beyond the `ast.With`/`ast.If` cases in F6.
- Verification gap: the stub `env_config` values in my sandbox differ from the frozen profiles
  (`:1`–`:6` ports vs `10101`–`10306`), so my execution witnesses compare *structure and counts*,
  not the projected digest values.
- No claim is made here about the sibling falsify items (case/field/profile/oracle items) or about
  round-29 admission.

## Tooling

No installs or upgrades were needed; stdlib only. `python3` 3.14.8 (GCC 16.2.1) was already
present. No pacman transaction was run (host-wide pacman is paused). No host service was
restarted. All experiments ran on copies under `/tmp/freview-astcontract/`.

## Files written by this seat

- this report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/falsify/FReviewAstContract.md`
- scratch (mine only): `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FReviewAstContract-2/`
  (`probe3.py`, `probe.py`, `probe2.py`, `semantic.py`, `final-battery.json`, `semantic-results.json`, `audit.json`)

No production, fixture, corpus, SOURCES, SCORECARD, candidate, lane Git index or sibling-lane file
was modified.

VERDICT: FAIL
