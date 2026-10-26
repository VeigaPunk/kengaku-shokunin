# R38BatP7 — C1 battery38 module for N11, N12

Seat: executor, round 38 wave 1. Lane `kengaku-shokunin` (read-only for me; drafts only under
`.ufo/waves/round-38/build/R38BatP7/`). Scratch: `/fast/scratch/hyaku/kengaku-r38/R38BatP7` (clone
`git -C "$S/lane" rev-parse --show-toplevel` = `$S/lane`, HEAD `2c5f4e0ba8e2865af4b71e337f3cde86eaf0702e`),
removed at the end (`ls /fast/scratch/hyaku/kengaku-r38 | grep -c R38BatP7` → `0`).

## Files changed (both new, nothing else written)

| Path | sha256 |
|---|---|
| `.ufo/waves/round-38/build/R38BatP7/battery/p7m.py` | `5e6f943f15ec65b278649bbbd25fb975cd6339603c923f9b893c6f2db241dbf5` |
| `.ufo/waves/round-38/build/R38BatP7/counter-n11-n12.txt` (full stdout, 72 lines) | `d4ebc12ad42820494ecc1de88df6d0cb088a0ddfcc12b5a78364bd4597ba4056` |
| `.ufo/waves/round-38/build/R38BatP7/load-bearing.txt` (isolation runs) | — |

Stdlib only (`pathlib` is not even imported; the module is constants + two builders). No `--spec`
is passed, so the counter appends the frozen `plans/pkg-spec-r35.json`; no tool installs were needed
(python3 3.14 in the host path; no pacman/uv/npx transaction).

## Behaviour: two fixtures, one branch each

Both start from `ctx.genuine_package(d)`, edit only `corpus/knowledge/tb2-protein-assembly-grader.md`,
then `ctx.git_add(d)` so P9 stays green. Declared defect set is `["P7"]` on both — the exact set the
unmodified gate prints (`observed_defects=P7`, `observed_rc=1`).

- `p7m-n11-empty-recheck` → N11 (`^recheck:\s*\S` → `^recheck:`). The genuine `recheck:` line
  (`corpus/knowledge/tb2-protein-assembly-grader.md:5`) is removed and an empty `recheck:` is appended as
  the **last line** of the entry. The EOF placement is load-bearing: `\s*` can cross newlines, so an
  empty `recheck:` followed by any later non-blank line still satisfies the reference regex
  (`pkg_gate.py:224`). Reference → `P7 DEFECT` ("recheck line absent"), mutant → P7 `ok`, exit 0.
- `p7m-n12-first-row-url` → N12 (`rows.items()` → `rows.items()[1:]`). The **first** registry row's
  source URL is changed: `protein-assembly/tests/test_outputs.py` → `…/test_other_outputs.py` on
  `corpus/knowledge/tb2-protein-assembly-grader.md:1` (S105 — first row in the spec's row order
  S105,S106,S107). battery37 `p7` defaces S106; N12 skips S105, so only S105 exposes it.
  Reference → `P7 DEFECT` (`S105: source line not the pinned url`), mutant (S105 skipped, S106/S107
  still match) → P7 `ok`.

`_only_once` guards both edits (needle count must be exactly 1 — `grep -c 'protein-assembly/tests/test_outputs\.py'`
on the entry = `1`; `grep -c '^recheck:'` = `1`), so a future entry rewrite fails loudly instead of
silently defacing the wrong line.

## Exact command and output (ticket command, verbatim)

```
$ python3 plans/round38_c1_verify.py --lane "$S/lane" \
    --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-38/build/R38BatP7/battery \
    --only N11,N12 --work "$S/w"
PINS total=14 mismatched=0
FIXTURE p7m-n11-empty-recheck expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
FIXTURE p7m-n12-first-row-url expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
BATTERY fixtures=66 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N11 P7 silence killed by=p7m-n11-empty-recheck -- a recheck line must carry a value [F37XMutP7 X4]
MUTANT N12 P7 silence killed by=p7m-n12-first-row-url -- the first registry row's source line is checked too [F37XMutP7 D1]
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
exit=0
```

`fixtures=66` = 16 round-36 + 48 battery37 + 2 battery38 (my two `p7m-*` lines are the ones shown;
all 64 pre-existing fixtures stay `ok`, `wrong=0`). Second invocation compared byte-equal
(`cmp` → `RUN2_BYTE_EQUAL`), so `renamed_disagree=0`/`null_detected=0` are stable, not luck.
`sidechannel=0` (token scan clean; `grep -nE '/proc|ppid|cmdline|psutil|environ' p7m.py` → no matches).

## Load-bearing table (each fixture removed in turn)

Module copies in scratch: `bat1` = minus the n12 entry, `bat2` = minus the n11 entry.

| Battery dir | N11 | N12 |
|---|---|---|
| full (`battery/`) | `killed by=p7m-n11-empty-recheck` | `killed by=p7m-n12-first-row-url` |
| minus `p7m-n11-empty-recheck` | **SURVIVED** | killed by `p7m-n12-first-row-url` |
| minus `p7m-n12-first-row-url` | killed by `p7m-n11-empty-recheck` | **SURVIVED** |

Counters in each isolation run: `BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0`,
`MUTANTS total=2 killed=1 survived=1 invalid=0 null_detected=0`. Raw text: `load-bearing.txt`; the
matching `FIXTURE p7m-* … ok` line for the surviving partner is present in each run.

## Counterfactual: why the empty `recheck:` must end the file

`bat3` = same module with the emptied `recheck:` left in place (line 5, original position):

```
FIXTURE p7m-n11-empty-recheck expect=reject declared=P7 observed_rc=0 observed_defects=- WRONG
MUTANT N11 P7 silence SURVIVED -- a recheck line must carry a value [F37XMutP7 X4]
```

The reference accepted the package: `^recheck:\s*\S` matched across the newline into the following
blank-line/later content. So a fixture built from the natural hint shape ("`recheck:` with nothing after")
is a **false fixture** — it declares a defect the gate does not print. The EOF form is the only shape
that makes N11's removed `\S` observable.

## Risks / notes for the L1

- My fixtures declare only `P7`; both also print nothing else, so integration with other seats'
  modules cannot shift the `defects` comparison. `attributed()` requires the subcommand family
  `package` (satisfied) and reference/mutant exit in `{0,1}` (mutant exits 0 on both).
- Fixture ids are `p7m-` prefixed and unique; the counter's duplicate-id guard is untouched.
- The N11 fixture deliberately writes the empty `recheck:` line *inside* the trailing `## Errata`
  section (`\Z`-terminated). That is inert for P7's Negative-space regex (`pkg_gate.py:226`,
  `(?=^## |\Z)`) — observed: only P7 defects, no P8/P3/P4 side effects — but a later entry rewrite
  that relies on the recheck line's position would break the *fixture's* premise loudly
  (`RuntimeError: expected exactly one line starting 'recheck:'` or the EOF property failing as a
  `WRONG` line), never silently.
- Scope: wave-1 calibration only. I did not run the full 22-mutant predicate (other seats own the
  remaining 20 mutants; battery38 is incomplete until they land), did not touch the lane tree, and
  did not judge the gate.
- No blockers. One lane-tree note for the L1: my clone's HEAD `2c5f4e0` printed
  `PINS total=14 mismatched=0`, i.e. the frozen inputs still match at that tip.

VERDICT: battery38-p7m-killed-2/2-wrong-0
