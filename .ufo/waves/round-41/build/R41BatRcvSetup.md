# R41BatRcvSetup — battery41 module `r_setup` (tip-receipts setup refusals, T01/T02/T05/T07)

Seat: executor, wave 1. Lane under test: clone of `/home/vgpnk/Projects/shokunin/kengaku-shokunin` at
`/fast/scratch/hyaku/kengaku-r41/R41BatRcvSetup/lane` (toplevel verified). Frozen inputs never edited.

## Deliverable

- Module: `.ufo/waves/round-41/build/R41BatRcvSetup/battery/r_setup.py` (118 lines, stdlib only, no imports)
- **sha256 `a693fc515268469816ffe7078a861dfa0419638adbba624bd2bdd7d0df9a9c1d`** (identical on the copy staged
  into `plans/battery41/` in the clone: `sha256sum` of both paths printed the same digest)
- 8 fixtures, all `tool=receipts`, all `expect=error`, all `defects=[]` (a setup refusal prints only `SETUP: …`
  and exits 2 before any `receipt …`/`control …` line, so the class set is empty by construction).
- No witness module is imported, copied or read: the module carries no reference to `w_receipts`/`w_sources`
  (`grep -n "witness\|w_receipts\|w_sources" battery/r_setup.py` → no match), and every fixture tree is built
  from `ctx` alone.

## Fixtures (one per refusal branch + a second shape per mutant)

| fid | branch in `plans/tip_receipts.py` | shape |
|---|---|---|
| `r_setup-t01-lane-absent` | `--lane` is not a directory (`:121`) | path that does not exist |
| `r_setup-t01-not-a-repo` | `git rev-parse` fails inside `lane_root` → `die` (`git()`, `:118-121`) | layout present, no work tree |
| `r_setup-t02-no-evidence` | `:241-242` | lane-shaped root, no `corpus/evidence` |
| `r_setup-t02-evidence-is-file` | `:241-242` (same guard, second trigger) | `corpus/evidence` is a regular file, so `.is_dir()` is false |
| `r_setup-t05-tamper-absent` | `:336-337` | `--tamper` names a path that is no receipt |
| `r_setup-t05-tamper-unmapped` | `:336-337` | `--tamper` names a **committed candidate** the mapping leaves unmapped (`bar-probe.log`) |
| `r_setup-t07-lane-subdir` | `:123-124` | lane is a subdirectory of the work tree, evidence inside it |
| `r_setup-t07-nested-lane` | `:123-124` | lane two levels inside a lane-shaped tree, both carrying `corpus/evidence` |

Mutant-kill mapping (declared direction `error`, i.e. ref rc 2 → mutant rc ∈ {0,1}):

- **T01** `raise SystemExit(2)` → `(0)` in `die()`: every refusal prints and exits 0.
- **T02** `if not (lane / EVIDENCE).is_dir():` → `if False:`: the guard falls through, `--list` prints `tip` +
  `note` and exits 0.
- **T05** `if unknown:` → `if False:`: the unknown id is used as a control key, `results[rel]` raises `KeyError`,
  traceback exit 1.
- **T07** `if not top or pathlib.Path(top).resolve() != lane.resolve():` → `if False:`: a subdirectory is
  accepted as a lane; `rev-parse HEAD`, `ls-tree` and `--list` all succeed from it, exit 0.

## Counter evidence — development run (envelope-wrapped)

Command (verbatim, `$S=/fast/scratch/hyaku/kengaku-r41/R41BatRcvSetup`):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
  --proc /proc --unshare-pid --die-with-parent python3 \
  /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round41_c1_verify.py --lane "$S/lane" \
  --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-41/build/R41BatRcvSetup/battery \
  --only T01,T02,T05,T07 --work "$S/w"
```

Output (`only-run.txt`, exit 0), verbatim:

```
PINS total=2 mismatched=0
FIXTURE r_setup-t01-lane-absent tool=receipts expect=error declared=- observed_rc=2 observed=- ok
FIXTURE r_setup-t01-not-a-repo tool=receipts expect=error declared=- observed_rc=2 observed=- ok
FIXTURE r_setup-t02-no-evidence tool=receipts expect=error declared=- observed_rc=2 observed=- ok
FIXTURE r_setup-t02-evidence-is-file tool=receipts expect=error declared=- observed_rc=2 observed=- ok
FIXTURE r_setup-t05-tamper-absent tool=receipts expect=error declared=- observed_rc=2 observed=- ok
FIXTURE r_setup-t05-tamper-unmapped tool=receipts expect=error declared=- observed_rc=2 observed=- ok
FIXTURE r_setup-t07-lane-subdir tool=receipts expect=error declared=- observed_rc=2 observed=- ok
FIXTURE r_setup-t07-nested-lane tool=receipts expect=error declared=- observed_rc=2 observed=- ok
MUTANT T01 receipts error killed by=r_setup-t01-lane-absent -- plans/tip_receipts.py:30-32 '2 usage/setup (lane not a git work-tree root, no `corpus/evid
MUTANT T02 receipts error killed by=r_setup-t02-no-evidence -- plans/tip_receipts.py:30-31 '2 usage/setup (..., no `corpus/evidence/`, ...)'
MUTANT T05 receipts error killed by=r_setup-t05-tamper-absent -- plans/tip_receipts.py:31-32 '2 usage/setup (..., unknown `--tamper` id)'
MUTANT T07 receipts error killed by=r_setup-t07-lane-subdir -- plans/tip_receipts.py:30-31 '2 usage/setup (lane not a git work-tree root, ...)'
BATTERY fixtures=8 wrong=0 tampered=0 sidechannel=0
MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=4/4 sources=0/0
ADVERTISED direct=4 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

`wrong=0 tampered=0 sidechannel=0`, `null_detected=0`, `PINS-AFTER mismatched=0`.

## Load-bearing table

Method: a scratch copy of the module with fixture(s) removed from `FIXTURES`, run with the same `--only`
set. Verbatim summary line per removal (`MUTANTS total=4 …`).

Single-fixture removal (8 runs): **no mutant flips to SURVIVED** in any single removal — each mutant has a
second-shape sibling that still exhibits the same direction. The `killed by=` attribution moves to the sibling:

| removed | re-attributed killer | survivors |
|---|---|---|
| `r_setup-t01-lane-absent` | T01 → `r_setup-t01-not-a-repo` | 0 |
| `r_setup-t01-not-a-repo` | T01 → `r_setup-t01-lane-absent` | 0 |
| `r_setup-t02-no-evidence` | T02 → `r_setup-t02-evidence-is-file` | 0 |
| `r_setup-t02-evidence-is-file` | T02 → `r_setup-t02-no-evidence` | 0 |
| `r_setup-t05-tamper-absent` | T05 → `r_setup-t05-tamper-unmapped` | 0 |
| `r_setup-t05-tamper-unmapped` | T05 → `r_setup-t05-tamper-absent` | 0 |
| `r_setup-t07-lane-subdir` | T07 → `r_setup-t07-nested-lane` | 0 |
| `r_setup-t07-nested-lane` | T07 → `r_setup-t07-lane-subdir` | 0 |

Pair removal (both fixtures of one mutant; 4 runs) — every one of T02/T05/T07 flips, naming the pair that is
load-bearing:

| removed pair | flipped mutant | evidence line |
|---|---|---|
| T01 pair | none (T01 still killed by `r_setup-t02-no-evidence`) | `killed=4 survived=0` |
| T02 pair | **T02** | `MUTANT T02 receipts error SURVIVED exhibits=none` / `killed=3 survived=1` |
| T05 pair | **T05** | `MUTANT T05 receipts error SURVIVED exhibits=none` / `killed=3 survived=1` |
| T07 pair | **T07** | `MUTANT T07 receipts error SURVIVED exhibits=none` / `killed=3 survived=1` |

T01 is the exception, and it is structural, not a defect: T01 replaces `die()`'s exit code, so **every** refusal
path kills it (all 8 fixtures do). Emptying the battery dir (`--battery-dir` on an empty directory, the frozen
do-nothing shape) makes all four survive: `MUTANTS total=4 killed=0 survived=4 invalid=0 null_detected=0`, each
printed `SURVIVED exhibits=none`. So T01's kill is redundant but real; T02/T05/T07 depend on their own pairs.

## Full default counter with the module staged

`cp battery/r_setup.py "$S/lane/plans/battery41/r_setup.py"` (clone only), then:

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
  --proc /proc --unshare-pid --die-with-parent python3 \
  /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round41_c1_verify.py --lane "$S/lane" --work "$S/w2"
```

`full-run.txt`, exit **1** (expected: the other 19 frozen mutants have no fixture in this module; the predicate
floors need 13 receipts + 10 sources). MUTANT and summary lines, verbatim:

```
MUTANT T01 receipts error killed by=r_setup-t01-lane-absent -- plans/tip_receipts.py:30-32 '2 usage/setup (lane not a git work-tree root, no `corpus/evid
MUTANT T02 receipts error killed by=r_setup-t02-no-evidence -- plans/tip_receipts.py:30-31 '2 usage/setup (..., no `corpus/evidence/`, ...)'
MUTANT T03 receipts rc-silence SURVIVED exhibits=none -- plans/tip_receipts.py:30 '1 a `differ`, a failed control, or a probe that did not complete
MUTANT T04 receipts rc-mirror SURVIVED exhibits=none -- plans/tip_receipts.py:21-23 'absolute mkdtemp paths are masked on both sides, so equality
MUTANT T05 receipts error killed by=r_setup-t05-tamper-absent -- plans/tip_receipts.py:31-32 '2 usage/setup (..., unknown `--tamper` id)'
MUTANT T06 receipts rc-silence SURVIVED exhibits=none -- plans/tip_receipts.py:29-30 '0 every mapped receipt reproduces ... and the control reports
MUTANT T07 receipts error killed by=r_setup-t07-lane-subdir -- plans/tip_receipts.py:30-31 '2 usage/setup (lane not a git work-tree root, ...)'
MUTANT T08 receipts rc-mirror SURVIVED exhibits=none -- plans/tip_receipts.py:19-21 'A mapped receipt whose script is gone, whose dependency is ab
MUTANT T09 receipts silence SURVIVED exhibits=none -- plans/tip_receipts.py:13-14 'if its own basename resolves to exactly one committed `plans/
MUTANT T10 receipts silence SURVIVED exhibits=none -- plans/tip_receipts.py:15-16 'with non-alphanumerics dropped and case folded, the receipt s
MUTANT T11 receipts silence SURVIVED exhibits=none -- plans/tip_receipts.py:13-14 'A file enters the byte-comparison if the RECEIPTS table maps
MUTANT T12 receipts silence SURVIVED exhibits=none -- plans/tip_receipts.py:12 'Population, stated mechanically: committed files `corpus/evidenc
MUTANT T13 receipts rc-mirror SURVIVED exhibits=none -- plans/tip_receipts.py:26-27 'the comparator must answer `differ`. ... A control that answe
MUTANT S01 sources 2>0 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1020-1021 '# Exclusive: before this
MUTANT S02 sources 2>1 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1042 '--registry and --package are
MUTANT S03 sources 2>5 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1053 '--access-date must be an ISO
MUTANT S04 sources 2>0 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1035-1036 '`--url-map` alone reache
MUTANT S05 sources 2>0 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1051 '--entries is required when --
MUTANT S06 sources 2>0 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1059 '--recheck must be an ISO date
MUTANT S07 sources 3>0 SURVIVED exhibits=none -- SKILL.md:573 '`3` staged/registry id collision'
MUTANT S08 sources 2>1 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1019 '--quote-file and --artifact m
MUTANT S09 sources 2>9 SURVIVED exhibits=none -- SKILL.md:573 '`2` usage error or unreadable quote artifact'; plans/sources_adopt.py:1028 '
MUTANT S11 sources 5>0 SURVIVED exhibits=none -- SKILL.md:573 '`5` requested id absent' (main() also refuses a requested row that is not `m
BATTERY fixtures=8 wrong=0 tampered=0 sidechannel=0
MUTANTS total=23 killed=4 survived=19 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=4/13 sources=0/10
ADVERTISED direct=21 indirect=2 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
```

The 8 `FIXTURE` lines in `full-run.txt` are all `ok`; `grep -c '^FIXTURE' full-run.txt` → `8`.

## Host-safety compliance

- Every counter run (development, load-bearing, full) was wrapped in the mandated envelope:
  `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent …`.
- Nothing was written to `~/.local/bin`, `/usr`, `/etc`, `$HOME`, the fleet root, the lane's `corpus/`, `plans/`,
  ledgers or jj/git index. The only lane writes were `plans/battery41/r_setup.py` inside the throwaway clone.
- No `crit_git_shim.py` / `crit_ledger_selfread.py` touched; no `git`/`python3` shim planted; no environment
  variable honoured by git (`GIT_CONFIG_COUNT` keys are set by the counter and only disable fsmonitor/hooks).
- Module token scan (the counter's own list, case-insensitive): `tokens_present={}` and the counter's
  `sidechannel=0` agree.
- Scratch `S=/fast/scratch/hyaku/kengaku-r41/R41BatRcvSetup` removed with `rm -rf` after copying receipts
  (`only-run.txt`, `full-run.txt`) into this report dir. No installs or upgrades were needed
  (`bwrap`, `git`, `python3` already present); no package manager was run.
- No writes outside this report dir; no timestamps needed elsewhere.

## Risks / limits

- A kill records a result difference in the declared direction, not intent: T01 is killed by all eight fixtures
  because `die()` is the shared exit path, so its attribution (`killed by=` first match) is conventional.
- `r_setup-t02-evidence-is-file` and `r_setup-t05-tamper-unmapped` rely on git listing a `corpus/evidence` pathspec
  from a work-tree root; both were exercised under the frozen PATH and were byte-stable across the null rerun
  (`null_detected=0`).
- `r_setup-t07-nested-lane` does not depend on whether `ls-tree` prints paths relative to the cwd or the root: the
  mutant exits 0 either way (`--list` with no candidate is still rc 0), which is why the kill is stable.
- This module covers 4 of 23 frozen mutants; the full predicate still needs the other receipts (T03,T04,T06,
  T08-T13) and all 10 sources mutants from sibling modules.

VERDICT: battery41-r_setup-killed-4/4-wrong-0
