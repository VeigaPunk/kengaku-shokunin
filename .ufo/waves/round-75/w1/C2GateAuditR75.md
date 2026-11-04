# C2GateAuditR75 — adversarial instrument review

Axes: coverage (all five assigned attack legs), calibration (attribution, nulls, stamps, derived tallies). Recommendation: do not treat the A1 instrument's green as sufficient evidence of the frozen C2 claim. This is a review recommendation, not admission or judgment.

## Scope and method

Frozen claims were read in full before the first command. Tests use the actual instrument and inherited fixture builder extracted with read-only `git show 43255758:plans/<name>`; full revision resolved as `43255758ed7d74ea05c8e03686dd9ad37837f0cd`. No clone, git mutation, production edit, tool installation, subagent, or alternate orchestration runtime was used. Fixtures and the driver lived only under `/fast/scratch/hyaku/kengaku-r75/C2GateAuditR75/`.

Semantic tooling was unavailable: reading `xd://lsp` returned `No such tool`. References, definitions, and diagnostics could therefore not be requested. Text fallback was explicit: `grep` device searches covered the C2 definition/call sites (`bool(declared)`, keyword values, stamp search, `join(defs)`, tally formatting), inherited builder and `extra_row` replacement, and frozen contract. Grep is not semantic proof; executable fixtures below supply behavioral evidence.

Commands exercised:

* `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff e462a64 43255758 -- plans/round75_c2_registry_audit.py`, rc 0: A1 moves stamping before dispatch.
* `python3 /fast/scratch/hyaku/kengaku-r75/C2GateAuditR75/probe.py`, rc 0: all flag, stamp, real-arm recount, and isolated tally probes below. Driver rc 0 means it executed, not that the instrument passed these attacks.
* Each full flag audit used `python3 <scratch>/round75_c2_registry_audit.py --lane <scratch>/<case> --work <scratch>/cli-work`. Its script comparison used `python3 <scratch>/<case>/plans/probe.py --strict`.
* `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff 43255758 -- plans/round75_c2_registry_audit.py`, rc 0: observed subsequent worktree changes limited to unknown-tip/empty-receipt rejection and a whitespace-only null. These changes do not modify the flag, attribution, or tally defects below. A2's text at `plans/round-75-claims.md:130-146` describes those changes. No frozen predicate was reopened.

References below use **A1 line numbers** unless explicitly marked live.

## Findings, by severity

### High — keyword metadata can declare a nonexistent option; add_argument existence is misclassified

`plans/round75_c2_registry_audit.py:64-79,82-104` scans every string-valued argument, including keyword metadata, for option-like substrings. It returns `bool(declared)` rather than whether an `add_argument` call exists. Thus metadata can manufacture a flag, and positional/dynamic-only argparse CLIs silently fall back to string presence.

All fixtures share `import argparse; p=argparse.ArgumentParser()`, the body below, and `p.parse_args()`. Their registry entry is `python3 plans/probe.py --strict`, generated with `R74.build_fixture(..., extra_row=R74.row_text('probe', 'plans/probe.py --strict'))`.

| Case and body | Actual argparse rc | Audit rc / printed evidence |
|---|---:|---|
| `kw={'dest':'value','help':'--strict'}; p.add_argument(**kw)` | 2 | 0; `TEXT-FALLBACK n=1`, `FLAGS ok n=0`, `PREDICATE R75-C2 pass` |
| `p.add_argument('--lane',dest='--strict')` | 2 | 0; `TEXT-FALLBACK n=0`, `FLAGS ok n=0`, `PREDICATE R75-C2 pass` |
| `p.add_argument('value'); p.set_defaults(note='--strict')` | 2 | 0; `TEXT-FALLBACK n=1`, `PREDICATE R75-C2 pass` |

All three green cases printed `MISMATCH 0`, `DEFECTS n=0`; none accepts `--strict`. The keyword `dest` case printed actual `probe.py: error: unrecognized arguments: --strict`. These directly contradict the entry-flag declaration requirement, not merely provenance expectations.

Additional requested controls:

* `vars={'name':'--strict'}; p.add_argument('--lane',dest=vars['name'])`: argparse rc 2, audit rc 1, `DEFECT \`probe\`:entry:flag-not-declared:--strict` — correctly refused.
* `p.add_argument('--strict','-s',action='store_true')`: argparse rc 0, audit rc 0 — correctly accepted.
* `p.add_argument('--lane'); p.set_defaults(note='--strict')`: argparse rc 2, audit rc 1 — correctly refused when another literal option makes `has_cli` true. Same set_defaults text is falsely accepted without that literal option.
* `kw={'action':'store_true'}; p.add_argument('--strict',**kw)`: argparse rc 0, audit rc 0 — correctly accepted; **kwargs itself is not universally rejected.

Actionable boundary: detect calls separately from extracted options; keyword help/dest/default strings are not option declarations.

### High — wrong-id kills match expected-id text embedded in a row name

`plans/round75_c2_registry_audit.py:277,301,318` attributes by `exp in ' '.join(defs)`, not the finding-id field. A real inherited fixture uses:

```python
R74.build_fixture(root, extra_row=R74.row_text(
    'carrier:entry:unbacked-flag:', 'plans/missing.py'))
```

Actual `R74.run_checks` produced:

```text
SUBSTRING ['SCRIPT-MISSING plans/missing.py', '`carrier:entry:unbacked-flag:`:entry:script-absent:plans/missing.py'] matched=True
```

Expected id was `:entry:unbacked-flag:`; both findings concern an absent script, not an unbacked flag. The unrelated row-name payload suffices.

To exercise the canonical tally branch without changing production code, the driver injected that actual result tuple through an in-memory `mutate` seam, stubbed `audit_verdict` to an empty result, and supplied a fixed `lane_tip`. This is an **isolated main-branch test**, not a full lane/frozen-command run:

```text
MUTANTS real=1 expected_matched=1 wrong_id=0 survived=0 null_arms=1 null_survived=1 total=2
PREDICATE R75-C2 pass
main_rc=0
```

The green is false attribution. Parse/represent finding ids separately from names and payloads; the same substring operation also affects selftest and control scoring.

### Medium — wrong_id and survived are the same complement, not separate observations

`plans/round75_c2_registry_audit.py:318-324` prints both as `len(results)-len(matched)`. It never distinguishes a survivor with zero defects from a kill with the wrong defect. `:303` similarly conflates all unmatched control arms with wrong-id kills. `null_arms=1` and the `+1` total are literal assumptions, although `null_survived` is computed from the measured null defect list.

Isolated canonical main-branch tests, with the same documented seams as above:

```text
# defs=[]: genuinely survives
MUTANTS real=1 expected_matched=0 wrong_id=1 survived=1 null_arms=1 null_survived=1 total=2
PREDICATE R75-C2 fail
main_rc=1
# defs=['different:defect']: killed, wrong id, not survived
MUTANTS real=1 expected_matched=0 wrong_id=1 survived=1 null_arms=1 null_survived=1 total=2
PREDICATE R75-C2 fail
main_rc=1
```

Correct `(wrong_id,survived)` is `(0,1)` then `(1,0)`. Both cases still fail, so this is incorrect calibration/diagnostics rather than a new false-green by itself. The fixed nine-arm matrix masks the problem because every arm presently matches.

### Medium — first stamp-looking line wins, including fenced examples and contradictory receipts

`plans/round75_c2_registry_audit.py:59-60,132-161` searches the whole receipt with `STAMP.search`; it neither requires a header nor detects duplicates. Using `T=43255758ed7d74ea05c8e03686dd9ad37837f0cd`, each case is a separate directory containing `receipt.txt`, passed to `check_stamps(lane, directory, '43255758')`:

* ` ```text\nLANE_TIP T\n```\nVERDICT invented\n ` — accepted.
* `LANE_TIP T\nWORKTREE clean\nLANE_TIP 0000000000000000000000000000000000000000\n` — accepted despite the second unresolvable stamp.
* `LANE_TIP T\nVERDICT ok\n` — accepted without WORKTREE.
* `LANE_TIP T\nWORKTREE dirty\nVERDICT ok\n` — also accepted; cleanliness is not validated.

Each printed `STAMPS files=1 stamped=1 unstamped=0 unresolved=0 not_ancestor=0` and returned `[]`. Reversing the conflicting stamp order correctly rejects the file: `stamped=0 ... unresolved=1`, `REVISION:unresolvable receipt.txt 000000000000`.

The unresolvable second stamp is a concrete false green under the refusal requirement; fenced/header and WORKTREE cases describe the additional structural blind spots. WORKTREE validation/cleanliness is not represented as an independently frozen stamp counter. A2's observed diff leaves this search unchanged.

### Medium, historical A1 / changed by observed A2 — no ancestry proof when measured tip cannot resolve

A1 `:153` gates ancestry checking on `tip != 'unknown'`. Calling `check_stamps(lane, stamp_elsewhere_dir, 'no-such-measured-branch-c2audit')` accepted a valid A1 receipt stamp:

```text
STAMPS files=1 stamped=1 unstamped=0 unresolved=0 not_ancestor=0 []
```

That cannot prove ancestor-of-an-unresolved-tip. The observed worktree diff adds `TIPTAG:unresolved`; this finding is historical A1 evidence, **not an assertion that the subsequently changed code still accepts it**. The changed path was not executed by this seat.

## Requested attacks without an additional present defect

### Null arm

A1 `:211-215` passes a replacement row named `tool-n`, not a new additional row. Inherited `round74_c2_registry_audit.py:285-288` substitutes `extra_row` for `tool-b`; trailing pinned whitespace is stripped. Thus A1 is not bytewise/cosmetic no-op: it renames an identifier. It does not add a third registry row or skip the audit.

Executed comparison:

```text
NULL-COMPARISON baseline rows=2 scripts=2 parsed=2 defects=[]
NULL-COMPARISON null rows=2 scripts=2 parsed=2 defects=[]
```

Both parse the same scripts; parsed second-row name changes from `` `tool-b` `` to `` `tool-n` ``. No different checker path was observed. The subsequent A2 diff replaces this with whitespace-only edits to the existing tool-b row, resolving the non-cosmetic delta by inspection; not executed here. Do not describe A1's rename as whitespace-only.

### Tree object stamp

`git rev-parse 43255758^{tree}` returned tree `7e49b4584b37...`. A receipt stamping that tree is correctly rejected by the actual `^{commit}` resolution:

```text
STAMPS files=1 stamped=0 unstamped=0 unresolved=1 not_ancestor=0
['REVISION:unresolvable receipt.txt 7e49b4584b37']
```

### Independent tally recount

The unmodified A1 `mutate(lane, work)` returned nine real arms and an empty null defect list. Independently counted `killed=bool(defects)`, `wrong_id=bool(defects) and no expected match`, `survived=not defects`:

```text
RECOUNT real=9 killed=9 expected_matched=9 wrong_id=0 survived=0 null_survived=1
```

All M1–M9 currently match their expected token. M9 also emits an unrelated `:self-test:unbacked-flag:--selftest` finding in addition to the expected owner finding; it is not single-defect isolated. The nine-arm recount agrees with the claimed numbers on this matrix but does not validate the broken general classification or literal null-arm count.

## Residual risk and verification gaps

A valid ancestry stamp is not a content/provenance binding. Fixture `LANE_TIP T\nWORKTREE clean\nORIGIN elsewhere; numbers not measured here\nMISMATCH 0\nDEFECTS n=0\n` was accepted with `files=1 stamped=1`, zero defects. This exposes no cryptographic/authenticity guarantee: the frozen stamp rule only resolves ancestry, so authenticity is a residual limitation rather than an extra invented acceptance criterion. Similarly `lane_tip` stamps the requested revision while checks read lane paths; the stamp does not itself prove those bytes were the committed tree.

No full landing-tip frozen counting command, full A2 selftest, non-ancestor branch fixture, or semantic diagnostics run was performed. No conclusion about those unrun checks is implied. The actual A1 nine-arm matrix and all assigned flag/stamp edge categories were exercised as above. Subsequent worktree edits were inspected only to distinguish historical from still-applicable findings.

Cleanup: `rm -rf -- /fast/scratch/hyaku/kengaku-r75/C2GateAuditR75 && test ! -e /fast/scratch/hyaku/kengaku-r75/C2GateAuditR75`, rc 0. No scratch tree remains. Only this report was written in the lane.
