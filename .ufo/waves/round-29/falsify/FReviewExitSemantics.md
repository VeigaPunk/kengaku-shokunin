writer: KengakuR29-2.FReviewExitSemantics-2

# FReviewExitSemantics — exit 0/1/2 mapping in `plans/config_projection.py`

Scope of this item (as assigned): the exit 0/1/2 mapping in `main()`/`audit()` — which findings
exist, could-not-evaluate vs invariant finding, mutual exclusivity of the CLI modes and usage
exit 2, and whether the exception catch-all masks real bugs as `input_invalid`.

**Production source read: YES.** This is a review item, so I read
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py` in full (548 lines).
I did not read or import it as an oracle (that constraint applies to oracle/re-derivation items);
no oracle/agreement claim is made here.

## Attack

Exit-code semantics are the instrument's only machine-readable verdict channel, so I attacked the
mapping from four directions:

1. Every CLI invocation shape reachable from a shell (no flag, each flag, illegal flag
   combinations, unknown flag, bad `--root`).
2. Every exception class the instrument can raise, injected at the `audit()` call boundary with a
   /tmp copy of the module (no production file touched), observing the resulting exit code and the
   stdout/stderr split.
3. The internal `assert` mechanism of the hand-rolled JSON scanner (`string_spans`) versus
   `json.loads`, to see what the catch-all actually labels.
4. The prereg-declared exit contract versus the implemented one, including which finding ids are
   actually reachable through the CLI at all.

Prereg contract under test — `plans/round-29-claims.md:53-55`:
`Exit0 = audit completed with expected structural identities; exit1 = projection/invariant finding; exit2 = could-not-evaluate ... CLI usage2.`
(the quoted sentence spans lines 53-55 and is 18 words, within the 25-word cap).

All probes ran on copies under `/tmp` (or by importing the module read-only and patching
`cp.audit` in-process); no production, fixture, corpus or Git state was mutated. Probe scripts are
copied to `.ufo/waves/round-29/scratch/falsify/FReviewExitSemantics/`.

## Environment

- `python3 -V` → `Python 3.14.8` (preinstalled; **no tool was installed or upgraded** — no pacman
  transaction was attempted; the host-wide pacman pause was respected).
- `/home/vgpnk/.omp/agent/RULES.md` read before probing.
- No REA MCP devices used.

## Baseline (observed)

| command | exit | stdout bytes | stderr bytes |
|---|---|---|---|
| `python3 config_projection.py` | 0 | 6914 | 0 |
| `python3 config_projection.py --summary` | 0 | 6914 | 0 |
| `python3 config_projection.py --json` | 0 | 3881050 | 0 |
| `python3 config_projection.py --selftest` | 0 | 1 line `SELFTEST clean cases=...` | 0 |

`diff noarg.out sum.out` → identical (no output from diff).

## Findings (by severity)

### F1 — HIGH — exit 1 (the "projection/invariant finding" code) is also the code for every uncaught crash

`main()` (`config_projection.py:524-544`) wraps only `audit(args.root)` (line 535) in `try`.
The `print` calls (lines 541 and 543) and the `--selftest` call (lines 532-533) are **outside** the
`try`, and the `except` tuple at line 538 is a closed list of six classes. Every other exception
class escapes `main()` as an unhandled traceback, which the interpreter turns into exit 1 with an
empty stdout.

Observed, injecting each exception class at the `audit()` boundary (module imported read-only,
`cp.audit` replaced; scratch script `uncaught_all.py`, one subprocess per class, real
`main()` call, exception left to escape):

```
AttributeError    exit=1 stdout_bytes=0 stderr_bytes=470
RecursionError    exit=1 stdout_bytes=0 stderr_bytes=462
RuntimeError      exit=1 stdout_bytes=0 stderr_bytes=432
NameError         exit=1 stdout_bytes=0 stderr_bytes=453
ZeroDivisionError exit=1 stdout_bytes=0 stderr_bytes=449
MemoryError       exit=1 stdout_bytes=0 stderr_bytes=425
StopIteration     exit=1 stdout_bytes=0 stderr_bytes=427
```

Real-CLI stderr shape for the first row:

```
Traceback (most recent call last):
  File ".../config_projection.py", line 535, in main
    result, code = audit(args.root)
AttributeError: 'NoneType' object has no attribute 'get'
```

Two further reachable exit-1-with-empty-stdout cases, no injection needed:

- **Broken pipe.** `python3 config_projection.py --json | head -c 100 >/dev/null` →
  `BrokenPipeError` raised at `config_projection.py:541` (the `print(json.dumps(...))`), `PIPESTATUS[0]=1`.
  `BrokenPipeError` is an `OSError` subclass, but the `print` is outside the `try`, so it is not
  caught. A 3.8 MB JSON stream truncated by `head` is reported as an invariant finding.
- **Selftest cannot run.** `python3 config_projection.py --selftest --root /tmp/exitprobe/emptyroot`
  → exit 1, stdout 0 bytes, stderr `FileNotFoundError` for
  `.../plans/fixtures/r29/hand/cascade-order.case.json`. `selftest()` is called at line 533, outside
  the `try`, so a could-not-evaluate condition (missing fixture) is reported as exit 1.

Consequence: exit 1 is ambiguous between "the projection produced a finding" (which prints
`FINDING ...` lines, or `findings[]` in JSON) and "the tool crashed". A consumer that branches on
the exit code alone will read a crash as a finding. Note the instrument's own contract sentence
(`exit1 = projection/invariant finding`) is violated by the crash path.

[INFERENCE] The intended contract likely wants crashes to be exit 2 (could-not-evaluate) with a
machine-readable finding, and the selftest to have its own code space; the current code has neither.

### F2 — HIGH — the catch-all at line 538 blames the input for the tool's own faults (`input_invalid`, exit 2)

```python
538    except (OSError, ValueError, KeyError, TypeError, AssertionError, IndexError) as error:
539        result, code = {"findings": [{"id": "input_invalid", "detail": repr(error)}], "limitations": LIMITS}, 2
```

`AssertionError` is this instrument's own internal-invariant mechanism: `string_spans` asserts the
JSON grammar at lines 177, 186, 192 and 196. Those asserts can fire on input that `json.loads`
already accepted, because `json.loads` (line 269) permits the non-standard literals `NaN`,
`Infinity` and `-Infinity` while `string_spans` (lines 186-192) only accepts `true`/`false`/`null`
and `NUMBER_RE`.

Observed (probe `probe2.py`, calling `audit_text` directly):

```
label=nan_literal      raised=AssertionError  msg=48
label=infinity_literal raised=AssertionError  msg=21
```

Through `main()` the same condition is reported as an input verdict, not an invariant verdict:

```
{"findings":[{"detail":"AssertionError(48)","id":"input_invalid"}], "limitations":[...]}   exit=2
```

So an internal parser limitation is published as "the input is invalid" — a claim about the frozen
input that is false — and it lands in the exit-2 (could-not-evaluate) bucket instead of the
exit-1 (invariant) bucket the prereg reserves for projection/invariant findings. The same holds
for `KeyError`/`TypeError`/`IndexError`, which in a Python program are the canonical signatures of
a coding bug, e.g. `TypeError: bug: str vs int` → `{"id":"input_invalid"}` exit 2 (observed).

Consequence: exit 2 degrades from "could-not-evaluate (missing/tampered/unrecognized)" into "anything
went wrong", and the `detail` field carries `repr(error)`, so the true fault class is preserved but
its *category* is mislabelled as an input problem.

### F3 — MEDIUM — exit 2 is overloaded across three incompatible output contracts

Observed id/stream behaviour of exit 2:

| trigger | stdout | stderr |
|---|---|---|
| usage error (`--summary --json`) | 0 bytes | 191 bytes of argparse usage text |
| usage error (`--bogus`) | 0 bytes | argparse usage text |
| could-not-evaluate (`--root /tmp/does-not-exist-xyz`) | JSON `{"findings":[{"id":"input_missing",...}],"limitations":[...]}` | 0 bytes |
| catch-all (`--root /etc/hostname`) | JSON `{"findings":[{"id":"input_invalid",...}],"limitations":[...]}` | 0 bytes |

Two concrete consequences:

1. **Exit 2 does not determine the stdout shape.** A consumer that does `json.loads(stdout)` on
   exit 2 crashes with `JSONDecodeError` when the cause was a mistyped flag. The instrument's own
   helper relies on the opposite convention: `selftest`'s `cli()` (line 483) asserts
   `json.loads(output.stdout)["findings"][0]["id"]` for exit-2 cases, so a usage error inside
   `cli()` would raise `JSONDecodeError` instead of failing on the real cause.
2. **The exit-2 JSON document is not a subset of the exit-0/1 document.** Observed key sets:
   - success (`--json`): `['findings','index_mapping','inputs','limitations','manifest_sha256','occurrence_provenance','population','profiles','raw_text_sha256','source_contract','upstream_revision']` (11 keys)
   - failure (`--root /tmp/nope --json`): `['findings','limitations']` (2 keys)

   A consumer that reads `result["population"]` or `result["index_mapping"]` raises `KeyError` on the
   exit-2 path. The `--summary` path has the same asymmetry: on exit 2 the output contains only
   `LIMIT ...`, `FINDING ...` and `TOTAL findings=1 exit=2` lines — the `POPULATION`/`INDEX` sections
   are simply absent with no marker saying so.

`CLI usage2` is prereg-sanctioned (`round-29-claims.md:55`), so the exit *value* is not the defect;
the defect is that one exit value carries three different stdout contracts with no discriminator.

### F4 — MEDIUM — `--summary` is an inert flag, and the mutual exclusion forbids a satisfiable request

`mode.add_argument("--summary", action="store_true")` is at line 528, but `args.summary` is never
read: `grep -n "args.summary"` over the file returns **no match**; the only mode consumer is
`if args.json:` at line 540.

Observed: `--summary` stdout is byte-identical to the no-flag stdout (6914 bytes each; `diff`
produced no output), and `--summary --json` is rejected with exit 2 and the argparse message
`not allowed with argument --summary`.

Consequence: the documented CLI surface (`--summary | --json | --selftest`, prereg line 51-52)
advertises three modes but only two exist; `--summary` selects the default branch, and the
mutually exclusive group (line 527) turns a request that is semantically satisfiable (and would
change nothing) into a usage error with exit 2.

### F5 — MEDIUM — a missing/unreadable pinned input is reported as `input_invalid`, not the prereg's stable `input_missing`

`read_pinned` (lines 94-113) catches only `FileNotFoundError` (lines 98 and 109). Any other
filesystem error on a pinned path escapes to the catch-all and becomes `input_invalid`:

```
$ python3 config_projection.py --root /etc/hostname --json
{"findings":[{"detail":"NotADirectoryError(20, 'Not a directory')","id":"input_invalid"}], ...}   exit=2
```

The prereg requires stable findings for missing input (`round-29-claims.md:59-60`). Here the id is
unstable: the same missing input yields `input_missing` when the parent directory is absent
(`--root /tmp/does-not-exist-xyz` → `{"id":"input_missing","path":"plans/fixtures/r29/manifest.json"}`)
and `input_invalid` when the root is a file. The same applies to `PermissionError` and
`IsADirectoryError` (a pinned path replaced by a directory).

### F6 — MEDIUM — the exit-1 invariant `leaf_change_unexplained` (lines 316-318) fires on a self-consistent projection

```python
316        carriers = sum(1 for text in string_values(original) if any(token in text for token in tokens))
317        if unexplained or (not problems and carriers != len(changed)):
318            findings.append({"id": "leaf_change_unexplained", ...})
```

`carriers` counts ORIGINAL leaves that contain a token; `len(changed)` counts leaves whose projected
value differs. When a profile value equals the token itself, the projection is a no-op: the leaf is
unchanged, `carriers=1`, `changed=0`, and a finding is emitted whose own payload says
`"unexplained": 0`. Observed (`probe2.py`):

```
label=degenerate_value_equals_token
findings=["leaf_change_unexplained","known_token_remaining"]
detail=[{"changed":0,"id":"leaf_change_unexplained","profile":"distinct_origins","token_leaves":1,"unexplained":0}, ...]
```

The finding id claims "unexplained change" while its unexplained counter is 0 and nothing changed:
a false invariant finding that would drive exit 1 for a projection that broke nothing. The rule
should test "no changed leaf lacks a carrying token" (`unexplained == 0`) and not compare
carriers against the changed count.

Reachability: not through the CLI with the frozen fixtures, because `profiles.json` is hash-pinned
(see F8) — but the rule is the exit-1 trigger, and it is exercised by `audit_text`, which the
selftest drives directly.

### F7 — MEDIUM — the exit-1 path has zero test coverage, and exit 1 is unreachable via the CLI with the frozen pins

`selftest`'s CLI helper (lines 481-483) asserts `returncode == code` with `code=2` as the default
for all four CLI cases (`cli_snapshot_tampered`, `cli_input_missing`, `cli_coherent_rebinding`,
`cli_manifest_tampered`); the only other exit assertion in the file is line 515
(`code == 0` on a direct `audit()` call). No case asserts exit 1, and no case drives a
findings-producing audit through `main()` — I confirmed the intended exit-1 path works by
injecting a finding (`TOTAL findings=1 exit=1`, exit code 1), but the instrument never tests it.
The prereg requires `test findings and exits checked` (`round-29-claims.md:74-78`).

### F8 — LOW — most declared could-not-evaluate ids are unreachable through the CLI

`read_pinned` verifies the manifest digest first (lines 100-101, `MANIFEST_SHA256` hard-coded at
line 25) and then every pinned file digest (line 111-112) **before** `source_contract(...)`
(line 349) and `check_profiles(...)` (line 351) run. Therefore any change to the generator, the
profiles or the raw file is rejected as `manifest_tampered` / `snapshot_tampered`, and the
following declared ids can never be emitted by the CLI:
`source_contract_unrecognized` (lines 64, 68, 76, 78, 85, 88), `manifest_contract_mismatch`
(line 104), `profile_missing`/`profile_unexpected` (line 122), `profile_invalid_type` (lines 119,
126, 135), `profile_missing_key` (line 133), `profile_unexpected_key` (line 137).

Observed CLI-reachable exit-2 ids across every invocation I made: `input_missing`,
`manifest_tampered`, `snapshot_tampered` (via the instrument's own selftest cases),
`input_invalid`. The prereg asks for stable findings including `profile_missing_key/type`
(`round-29-claims.md:59-60`); those ids are reachable only through direct library calls, as the
selftest does at line 430.

[INFERENCE] This is a deliberate pin-first design, so it is a coverage/publishing defect rather
than a logic error: the prereg's "stable findings" list overstates what the CLI can publish.

### F9 — LOW — input-level defects split across exit 1 and exit 2

`task_population_invalid` (line 275) describes a property of the *input* (population ≠ 812, or
task_ids ≠ 0..811) and is emitted as an ordinary finding → exit 1 (the "projection/invariant
finding" code). The equivalent input-contract defect for profiles (`profile_missing_key`,
`profile_invalid_type`, lines 133/135) is raised as `Unevaluable` → exit 2 (could-not-evaluate).
Observed: `audit_text('[{"task_id": 7}]', ..., expected_population=812)` →
`["task_population_invalid","projection_population_changed"]`.

[INFERENCE] Under the prereg wording, an input-level population defect reads as could-not-evaluate
(exit 2) while a projection-level count defect (`projection_population_changed`, line 339) reads as
exit 1; the current split is the other way round for the first of the two.

## Complete finding-id inventory (observed from source, with the exit code each produces)

Exit 1 (invariant/projection findings, `audit_text`/`audit`):
`task_population_invalid` (275), `token_outside_string_value` (287), `projection_json_invalid` (299),
`projection_structure_changed` (306), `leaf_change_unexplained` (318), `known_token_remaining` (337),
`projection_population_changed` (339), `projection_count_invalid` (355).

Exit 2 (could-not-evaluate, `Unevaluable` → line 537):
`source_contract_unrecognized` (64, 68, 76, 78, 85, 88), `input_missing` (99, 110),
`manifest_tampered` (101), `manifest_contract_mismatch` (104), `profile_invalid_type` (119, 126, 135),
`profile_missing`/`profile_unexpected` (122), `profile_missing_key` (133),
`profile_unexpected_key` (137).

Exit 2 (catch-all → line 539): `input_invalid` with `detail = repr(error)`.

Exit 1 without any finding published: every exception class outside the line-538 tuple, the
selftest crash path, and a broken pipe (F1).

## Residual risk / verification gaps

- The exception-injection probes replace `cp.audit` in-process; they exercise the real `main()`
  code path (lines 534-544) but not the real `audit()` body. That is intentional: the defect is in
  `main()`'s classification, not in `audit()`.
- `source_contract` and `check_profiles` are read but not re-derived here; F8's unreachability claim
  follows from the pin order at lines 100-112 and the observed CLI ids, not from an exhaustive
  enumeration of CLI states.
- I did not test the instrument against a non-frozen `--root` tree (the manifest pin makes any
  variation exit 2 anyway); F5/F6/F9 rest on direct calls into `audit_text`/`check_values`.
- No claim is made about the projection's substantive correctness (other falsify items cover that);
  my verdict is scoped to the exit-code and CLI-surface semantics only.
- Tooling: nothing installed or upgraded; `python3 3.14.8` preinstalled. No pacman transaction.

## Reproduction artifacts

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FReviewExitSemantics/`:
`drive.py` (exception-class → exit-code table), `probe2.py` (audit_text internals),
`uncaught_cli.py` (real-CLI uncaught-exception shape), `exit1_demo.py` (intended exit-1 path),
plus captured stdout/stderr byte counts quoted above.

VERDICT: FAIL
