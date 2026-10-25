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

## Re-check at dbcecded (follow-up)

**writer: KengakuR29-2.FReviewExitSemantics-2** — follow-up re-check, same seat and same item; not a
new assignment. Earlier bytes of this report are unchanged; the prior scoped verdict line
(`VERDICT: FAIL`) stays where it was and this section carries its own final verdict.

### Object of the re-check

Lane master `dbcecded4a04247cf6fd12919327af973da10bdd` (`git rev-parse HEAD` → that value;
`git log --oneline -1` → `dbcecde round-29: repair falsify findings, persist mutation witness, add
S074, freeze candidate v2`). The repaired file was read again (production source read: YES — same
review item as before). Repair delta inspected with `git show 56fd949:plans/config_projection.py`
against the working-tree file (read-only git commands only; no git index, lane, jj or corpus
mutation). Working tree at re-check time carried only untracked scratch entries
(`git status --porcelain` shows `?? .ufo/waves/round-29/scratch/...` only), so the bytes reviewed
are the committed bytes.

Probes: read-only CLI runs of the committed file, plus an in-process driver that imports the module
and replaces `cp.audit` (script kept as `recheck.py` in my scratch dir). No production, fixture,
corpus or report byte was modified; /tmp copies were deleted after the run.

### Status summary

| finding | status at dbcecded | one-line basis |
|---|---|---|
| F1 exit 1 is also the crash code | **PARTIAL** | audit-internal crashes are now exit 2 `internal_error`; print, selftest and rendering failures still exit 1 with an empty stdout |
| F2 catch-all masked internal bugs as `input_invalid` | **RESOLVED** | `except Exception` → `internal_error` exit 2 (645-646); `input_invalid` no longer exists |
| F3 exit 2 carries three stdout contracts | **REMAINS** | usage error still stdout 0 bytes; exit-2 JSON still 2 keys vs 12 on success |
| F4 `--summary` is an inert flag | **REMAINS** | `args.summary` still never read; `--summary --json` still a usage error |
| F5 missing input reported as `input_invalid` | **RESOLVED** | `read_pinned` catches `OSError` → `input_missing` (131-132, 142-143) |
| F6 `leaf_change_unexplained` mis-specified | **RESOLVED** | rule split into `leaf_change_unexplained` (count) and `token_leaf_unchanged` (357-360) |
| F7 exit-1 path had zero coverage | **RESOLVED** | new selftest case `exit_mapping` (565-573) |
| F8 most could-not-evaluate ids CLI-unreachable | **REMAINS** | `read_pinned` still precedes `source_contract`/`check_profiles` (403-406) |
| F9 input-level defects split across exit 1/2 | **REMAINS** | id renamed `input_population_mismatch` (310) and still published as an ordinary finding → exit 1 |

### F1 — PARTIALLY RESOLVED

Resolved part: the closed exception tuple is gone. `main()` now has

```
641        try:
642            result, code = audit(args.root)
643        except Unevaluable as error:
644            result, code = {"findings": [error.finding], "limitations": LIMITS}, 2
645        except Exception as error:
646            result, code = {"findings": [{"id": "internal_error", "detail": repr(error)}], "limitations": LIMITS}, 2
```

Measured (each class injected at the `audit()` boundary, real `main()` call, exception left to
escape `audit()`):

```
RuntimeError       exit=2 ids=['internal_error'] stdout_bytes=1764 uncaught=None
AttributeError     exit=2 ids=['internal_error'] stdout_bytes=1804 uncaught=None
AssertionError     exit=2 ids=['internal_error'] stdout_bytes=1789 uncaught=None
KeyError           exit=2 ids=['internal_error'] stdout_bytes=1773 uncaught=None
ValueError         exit=2 ids=['internal_error'] stdout_bytes=1790 uncaught=None
OSError            exit=2 ids=['internal_error'] stdout_bytes=1759 uncaught=None
RecursionError     exit=2 ids=['internal_error'] stdout_bytes=1794 uncaught=None
MemoryError        exit=2 ids=['internal_error'] stdout_bytes=1757 uncaught=None
```

No traceback, no exit 1, a machine-readable finding on stdout. That part of F1 is fixed.

Residual part — the `try` still covers only lines 641-646, so three reachable paths still exit 1
with an empty stdout and a raw traceback (i.e. exit 1 remains ambiguous with a finding):

1. **Broken pipe.** `python3 config_projection.py --json | head -c 100 >/dev/null` →
   `BrokenPipeError` at line 648 (the `print`), `PIPESTATUS[0]=1`, stderr 446 bytes.
2. **Selftest that cannot run.** `--selftest --root /tmp/exitprobe/emptyroot` → exit 1, stdout
   0 bytes, stderr 956 bytes, `FileNotFoundError` for `.../plans/fixtures/r29/hand`. `selftest()`
   is called at line 639, outside the `try`.
3. **Rendering failures after the `try`.** Injected results that the emitters cannot render:
   `summary_lines` → `KeyError: 'distinct_task_ids'` → exit 1, stdout 0 bytes; `json.dumps` →
   `TypeError: Object of type set is not JSON serializable` → exit 1, stdout 0 bytes. Lines 648 and
   650 are outside the `try`.

### F2 — RESOLVED

`input_invalid` no longer exists. Every exception inside `audit()` is now `internal_error` exit 2
(lines 645-646), so an internal fault is no longer published as a verdict about the input. The
specific trigger from my first report is also gone: `string_spans` now accepts the non-standard
literals (line 221 `for literal in ("true", "false", "null", "NaN", "Infinity", "-Infinity")`).
Re-probe of the same inputs:

```
nan_literal       findings=['projection_structure_changed']   payload={"count":1,"id":"projection_structure_changed","paths":["/0/x"],"profile":"p"}
infinity_literal  findings=[]
```

No `AssertionError`, no `input_invalid`.

### F3 — REMAINS (untouched by the repair)

- Usage error still exits 2 with a different stdout contract: `--summary --json` → exit 2,
  stdout 0 bytes, stderr 191 bytes (argparse text).
- The exit-2 JSON document is still not a subset of the success document. Measured key sets at
  dbcecded: success `--json` → 12 keys `['findings','index_mapping','inputs','limitations',
  'manifest_sha256','occurrence_provenance','population','profiles','raw_text_sha256',
  'source_contract','upstream_revision','witnesses']`; error (`--root /tmp/nope`) → 2 keys
  `['findings','limitations']`; `python -O` → 2 keys `['findings','limitations']`. A consumer that
  reads `result["population"]` still raises `KeyError` on every exit-2 path.
- The repair added a third exit-2 id (`assertions_disabled`, line 637) with the same 2-key shape,
  so exit 2 is internally consistent but still does not determine the stdout shape.

### F4 — REMAINS (untouched by the repair)

`grep -c "args.summary"` over the repaired file → **0** matches: the flag is still never read;
line 632 only adds the help string `human-readable lines (the default)`. Measured:
no-flag run → exit 0, stdout 8068 bytes; `--summary` → exit 0, stdout 8068 bytes; `cmp` reports
the two files identical. `--summary --json` → exit 2, stdout 0 bytes, stderr 191 bytes.

### F5 — RESOLVED

`read_pinned` now catches `OSError` on both pinned reads (lines 131-132 and 142-143) and raises
`Unevaluable("input_missing", path=..., detail=type(error).__name__)`. Measured:

```
$ python3 config_projection.py --root /etc/hostname --json
{"findings":[{"id":"input_missing","path":"plans/fixtures/r29/manifest.json","detail":"NotADirectoryError"}], ...}   exit=2
```

The prereg's stable `input_missing` id is now published for every filesystem failure on a pinned
path, not only for `FileNotFoundError`.

### F6 — RESOLVED

The exit-1 rule is split (lines 357-360): `leaf_change_unexplained` now fires only on a non-zero
`unexplained` count (payload `{"count": N}`), and the carriers/changed comparison moved to a
separate finding `token_leaf_unchanged`. Re-probe of my exact degenerate case (profile value equal
to the token):

```
degenerate_value_equals_token findings=['token_leaf_unchanged','known_token_remaining']
   payload: {"changed":0,"id":"token_leaf_unchanged","profile":"p","token_leaves":1}
   payload: {"id":"known_token_remaining","profile":"p"}
```

No finding now claims an unexplained change while its own counter reads 0.

### F7 — RESOLVED

New selftest case `exit_mapping` (lines 565-573) drives `main()` three ways: a findings-bearing
audit → exit 1 with `findings[0].id == "x"`; `Unevaluable` → exit 2 with `snapshot_tampered`;
`RuntimeError` → exit 2 with `internal_error`. Verified in the run: `--selftest` exit 0, stdout
contains `exit_mapping` (and the new `cli_optimized_refused`). The exit-1 branch that my first
report found uncovered is now covered.

### F8 — REMAINS

`audit()` still reads the pinned inputs first (line 403 `read_pinned`) and only then runs the
contract checks (line 404 `source_contract`, line 406 `check_profiles`), so any change to the
generator, the profiles or the raw file is still rejected by the digest layer before those checks
run. `source_contract_unrecognized`, `manifest_contract_mismatch`, `profile_missing`,
`profile_unexpected`, `profile_missing_key`, `profile_invalid_type` and `profile_unexpected_key`
remain unreachable from the CLI.

[INFERENCE] The repair made `source_contract` strictly stronger (exact statement match against
`EXPECTED_STATEMENTS`), which raises the value of that check for direct callers, but it does not
change its CLI reachability, so the prereg's "stable findings" list still overstates what the CLI
can publish.

### F9 — REMAINS, and is now sharper

The input-level finding was renamed and is still published as an ordinary finding: line 310
`findings.append({"id": "input_population_mismatch"})` → exit 1, while the equivalent profile
contract defects stay `Unevaluable` → exit 2. Measured:

```
population_mismatch findings=['input_population_mismatch','projection_population_changed']
   payload: {"id":"input_population_mismatch"}
```

The rename makes the input-level nature of the finding explicit while the exit code it carries is
the one the prereg reserves for projection/invariant findings, so the taxonomy split my first
report described is unchanged.

### New observations from the repair (in scope)

- **N1 — the `-O` refusal works and is a real mitigation.** `python3 -O config_projection.py --json`
  → exit 2, stdout 1785 bytes, `{"findings":[{"id":"assertions_disabled","detail":"python -O strips
  load-bearing checks"}], ...}`. The guard sits at line 636, after `parse_args`, so a usage error
  under `-O` still exits 2 with argparse's stderr text — the same stdout-contract ambiguity as F3.
- **N2 — `json.dumps` lost `sort_keys=True`.** Line 648 now uses `separators=(",", ":")` only. The
  success JSON is still deterministic (dict insertion order), but its bytes changed relative to the
  reviewed version, so the earlier build receipt `build-json-sha256.txt` no longer describes the
  current output. Outside my item's scope; flagged for the receipt owner. [INFERENCE]
- **N3 — isolation improvements do not close F1(b).** The selftest now runs its CLI child with
  `-I -S` and an empty environment and writes only under `/tmp` (lines 576-583), and the hand
  fixtures are authenticated by SHA-256 before use; the selftest's own top-level failure still
  exits 1 with a traceback and an empty stdout.

### Residual risk / verification gaps (re-check)

- Exception-injection probes replace `cp.audit` in-process: they exercise `main()` lines 641-651 as
  written, not `audit()`'s body.
- F8's unreachability rests on the call order in `audit()` (403-406) plus the CLI-reachable id set,
  not on exhaustive CLI enumeration.
- F3's key-set counts are single runs of the committed file at dbcecded.
- I did not re-derive the projection semantics; only the exit mapping and CLI surface are in scope.
- Tooling: nothing installed or upgraded; `python3 3.14.8` preinstalled; no pacman transaction
  attempted (host-wide pacman pause respected). /tmp copies deleted after the re-check.

VERDICT: PARTIAL
