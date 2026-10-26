# R41BatSrcModes — battery41 module for sources_adopt.py mode-exclusivity guards (S01, S04, S08, S09)

kengaku round 41, wave 1 (2026-10-26). Executor seat. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`,
clone `/fast/scratch/hyaku/kengaku-r41/R41BatSrcModes/lane` (`git rev-parse --show-toplevel` = the clone),
scratch removed before hand-off.

Frozen inputs read, never modified: `plans/round-41-claims.md` (claims), `plans/round41_c1_verify.py`
(MUTANTS S01/S04/S08/S09 + contract), `plans/sources_adopt.py` (the tool under test). Pins verified in the
clone before every measurement: `PINS total=2 mismatched=0`, with
`sha256 sources_adopt.py = 38492bf175e0c619596c69911954e3b3c247166bdc240f8c1d44a02b7f4103e0` and
`sha256 tip_receipts.py = e4f49714299ca1f2a93303c59ac07e691cc45d6126ccf24e5eecab93733f88f3`, the counter's
`PINS` literals. Every counter, battery build and fixture run went through the host envelope
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000
--proc /proc --unshare-pid --die-with-parent`. Nothing was written to any shared PATH directory, `/usr`,
`/etc`, `$HOME`, the lane, the fleet root, or the lane's Git index.

## Deliverable

`battery/s_modes.py` (this directory) — stdlib only, **zero imports**, no file reads of its own, 8 fixtures,
every fixture id starts `s_modes-`.

```
sha256 1023433bbc173d1db9d42729b527dbbc1a602c6860efd6c06c3896690ec6bdd1  battery/s_modes.py
```

The staged copy in the clone (`"$S/lane/plans/battery41/s_modes.py"`) hashes to the same value.
Integrator: `cp .ufo/waves/round-41/build/R41BatSrcModes/battery/s_modes.py plans/battery41/s_modes.py`.

## Fixture inventory (one behaviour per fixture, two independent triggers per guard)

| fid | mutant | behaviour demonstrated | shape (differs from the pre-freeze witness) | ref rc | mutant rc |
|---|---|---|---|---|---|
| `s_modes-s01-quote-plus-package` | S01 | quote mode + `--package` must refuse at the exclusivity guard | package side; realistic `corpus/` tree; decoy-first capture **directory** (witness: registry only, single-file artifact, bare tree) | 2 | 0 |
| `s_modes-s01-quote-plus-registry-and-package` | S01 | quote mode + `--registry` + `--package`, plus a `--url-map` that binds the quote correctly, must still refuse | both flags; a map that *would* pass binding | 2 | 0 |
| `s_modes-s04-url-map-with-adopt` | S04 | `--url-map` in registry mode with a complete adopt request (`--admit-ids/--entries/--access-date`) must refuse, not schedule | adopt path (witness: bare check) | 2 | 0 |
| `s_modes-s04-url-map-with-check-only` | S04 | `--url-map` with a clean check and no `--admit-ids` must refuse | two-row package, no `--admit-ids` | 2 | 0 |
| `s_modes-s08-quote-file-without-artifact` | S08 | `--quote-file` without `--artifact` must refuse (pairing guard) | rows file + a *readable* `--url-map` present | 2 | 1 |
| `s_modes-s08-artifact-without-quote-file` | S08 | the other side of the pair: `--artifact` without `--quote-file` must refuse | artifact side (witness: quote-file side) | 2 | 1 |
| `s_modes-s09-url-map-nested-shape` | S09 | an unreadable `--url-map` (nested object: `{"b-capture.txt": {"url": …}}`) must refuse before the quote is judged | JSON-shape problem (witness: `absent.json` = OSError) | 2 | 9 |
| `s_modes-s09-url-map-directory` | S09 | an unreadable `--url-map` naming a **directory** (OSError) must refuse; unguarded, the empty map leaves the located quote unmapped | filesystem-error branch | 2 | 9 |

All `defects` are `[]` (the sources tool's class set is always empty by contract), all `expect` are `error`
(exit 2: every one of the four guards is a usage/refusal refusal — `SKILL.md:573` "`2` usage error or
unreadable quote artifact").

Source lines the fixtures bind to (the counter's own `old` strings, `plans/sources_adopt.py`):
`:1019` `parser.error("--quote-file and --artifact must be given together")`; `:1022-1023`
`if args.registry or args.package:` / `parser.error("--quote-file/--artifact cannot be combined with
--registry/--package")`; `:1039-1040` `if args.url_map:` / `parser.error("--url-map needs --quote-file and
--artifact")`; `:1026-1029` `url_map, problem = load_url_map(...)` / `if problem:` / `print(f"QUOTE
problem={problem}")` / `return EXIT_QUOTE_UNREADABLE`.

Each build() fills the empty fixture dir with a lane-shaped tree (`corpus/SOURCES.md`,
`corpus/SOURCES.append.md`, `corpus/knowledge/`, `corpus/evidence/r41-captures/` with an `a-notes.md` decoy
that sorts before the `b-capture.txt` that holds the quote) and returns only absolute paths inside `d`.

## Proof in the clone (pasted output)

Command (envelope above):

```
python3 <lane>/plans/round41_c1_verify.py --lane "$S/lane" \
  --battery-dir <build>/R41BatSrcModes/battery --only S01,S04,S08,S09 --work "$S/wr1"
```

`receipts/only-run.txt`:

```
PINS total=2 mismatched=0
FIXTURE s_modes-s01-quote-plus-package tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_modes-s01-quote-plus-registry-and-package tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_modes-s04-url-map-with-adopt tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_modes-s04-url-map-with-check-only tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_modes-s08-quote-file-without-artifact tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_modes-s08-artifact-without-quote-file tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_modes-s09-url-map-nested-shape tool=sources expect=error declared=- observed_rc=2 observed=- ok
FIXTURE s_modes-s09-url-map-directory tool=sources expect=error declared=- observed_rc=2 observed=- ok
MUTANT S01 sources 2>0 killed by=s_modes-s01-quote-plus-package -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1020-1021 '# Exclusive: before this
MUTANT S04 sources 2>0 killed by=s_modes-s04-url-map-with-adopt -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1035-1036 '`--url-map` alone reache
MUTANT S08 sources 2>1 killed by=s_modes-s08-quote-file-without-artifact -- SKILL.md:573 '`2` usage error'; plans/sources_adopt.py:1019 '--quote-file and --artifact m
MUTANT S09 sources 2>9 killed by=s_modes-s09-url-map-nested-shape -- SKILL.md:573 '`2` usage error or unreadable quote artifact'; plans/sources_adopt.py:1028 '
BATTERY fixtures=8 wrong=0 tampered=0 sidechannel=0
MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=0/0 sources=4/4
ADVERTISED direct=4 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
rc=0
```

The mutant exit codes are not inferred: `exhibits()` for a digit pair requires `want == A and ref[0] == A and
mut[0] == B` (`plans/round41_c1_verify.py`, `exhibits`), so each `killed by=` line *is* the measurement
`2>0`, `2>0`, `2>1`, `2>9`. S08's unguarded run reaches the quote check with no artifact and dies on it
(rc 1); S09's unguarded run drops the map problem and reports the located quote `unmapped` (rc 9); S01's and
S04's unguarded runs complete the mode they were combined with (rc 0).

## Load-bearing table (`receipts/load-bearing.txt`)

**A. Attribute each fixture on its own** (8 modules of one fixture, same `--only` set): every fixture kills
exactly its own mutant and nothing else — no cross-kill, so every kill above is attributable.

```
alone=s_modes-s01-quote-plus-package: MUTANT S01 ... killed by=s_modes-s01-quote-plus-package | (S04, S08, S09 SURVIVED exhibits=none)
alone=s_modes-s01-quote-plus-registry-and-package: MUTANT S01 ... killed by=s_modes-s01-quote-plus-registry-and-package | (S04, S08, S09 SURVIVED)
alone=s_modes-s04-url-map-with-adopt: MUTANT S04 ... killed by=s_modes-s04-url-map-with-adopt | (S01, S08, S09 SURVIVED)
alone=s_modes-s04-url-map-with-check-only: MUTANT S04 ... killed by=s_modes-s04-url-map-with-check-only | (S01, S08, S09 SURVIVED)
alone=s_modes-s08-quote-file-without-artifact: MUTANT S08 ... killed by=s_modes-s08-quote-file-without-artifact | (S01, S04, S09 SURVIVED)
alone=s_modes-s08-artifact-without-quote-file: MUTANT S08 ... killed by=s_modes-s08-artifact-without-quote-file | (S01, S04, S09 SURVIVED)
alone=s_modes-s09-url-map-nested-shape: MUTANT S09 ... killed by=s_modes-s09-url-map-nested-shape | (S01, S04, S08 SURVIVED)
alone=s_modes-s09-url-map-directory: MUTANT S09 ... killed by=s_modes-s09-url-map-directory | (S01, S04, S08 SURVIVED)
```

**B. One fixture removed in turn** (8 runs): **no mutant flips to SURVIVED**. Each guard has two
independent triggers, so a single removal is absorbed by its sibling; the kill line simply changes owner,
e.g. removing `s_modes-s01-quote-plus-package` leaves
`MUTANT S01 sources 2>0 killed by=s_modes-s01-quote-plus-registry-and-package`. Every one of the 8 runs
printed `BATTERY fixtures=7 wrong=0 tampered=0 sidechannel=0` and no `SURVIVED` line.

**C. Both fixtures of one guard removed** (4 runs) — the load-bearing measurement:

```
removed-both=s_modes-s01-* -> MUTANT S01 sources 2>0 SURVIVED exhibits=none
removed-both=s_modes-s04-* -> MUTANT S04 sources 2>0 SURVIVED exhibits=none
removed-both=s_modes-s08-* -> MUTANT S08 sources 2>1 SURVIVED exhibits=none
removed-both=s_modes-s09-* -> MUTANT S09 sources 2>9 SURVIVED exhibits=none
```

So each mutant's kill is carried by its own guard's fixtures, and no fixture's removal silently leaves the
module green for a behaviour it no longer demonstrates.

## Full default counter (module staged at `plans/battery41/s_modes.py`)

Command: `python3 <lane>/plans/round41_c1_verify.py --lane "$S/lane" --work "$S/w2"`
(`receipts/full-run.txt`), one run of the whole frozen mutant list against this module:

```
PINS total=2 mismatched=0
MUTANT S01 sources 2>0 killed by=s_modes-s01-quote-plus-package -- ...
MUTANT S02 sources 2>1 SURVIVED exhibits=none -- ...
MUTANT S03 sources 2>5 SURVIVED exhibits=none -- ...
MUTANT S04 sources 2>0 killed by=s_modes-s04-url-map-with-adopt -- ...
MUTANT S05 sources 2>0 SURVIVED exhibits=none -- ...
MUTANT S06 sources 2>0 SURVIVED exhibits=none -- ...
MUTANT S07 sources 3>0 SURVIVED exhibits=none -- ...
MUTANT S08 sources 2>1 killed by=s_modes-s08-quote-file-without-artifact -- ...
MUTANT S09 sources 2>9 killed by=s_modes-s09-url-map-nested-shape -- ...
MUTANT S11 sources 5>0 SURVIVED exhibits=none -- ...
BATTERY fixtures=8 wrong=0 tampered=0 sidechannel=0
MUTANTS total=23 killed=4 survived=19 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=0/13 sources=4/10
ADVERTISED direct=21 indirect=2 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
rc=1
```

Expected for one seat's module: this module carries only the four sources CLI guards it was assigned;
`receipts=0/13` and S02/S03/S05/S06/S07/S11 survive because their fixtures belong to other battery41
modules. Nothing in this module is a no-op against the others: no fixture cross-kills a mutant it was not
built for (section A), and no `wrong`, `tampered`, `sidechannel` or `null_detected` count is nonzero.

## Isolation and hygiene evidence

- `SIDECHANNEL` scan of the module source (same token list, case-folded over the whole file):
  `hits: []`.
- The module imports nothing, opens nothing, and calls only `ctx.write` / `ctx.sh`-free builders plus
  `str(d / …)` joins; it never names, imports, copies or reads the witness modules
  (`.ufo/waves/round-41/claims/witness/w_sources.py`) nor any lane file at run time. Builds and tool runs
  were executed by the counter inside its own nested `bwrap` sandboxes (lane hidden for builds, fixed system
  PATH, no `uv`), inside the host envelope above.
- Fixture trees were fingerprinted by the counter before and after every run: `tampered=0`; every second
  unmodified run was byte-identical: `null_detected=0`; the two pinned tools were unchanged before and after:
  `PINS-AFTER mismatched=0`.
- No writes outside this report directory and the scratch dir; scratch `/fast/scratch/hyaku/kengaku-r41/R41BatSrcModes`
  removed. `crit_git_shim.py` / `crit_ledger_selfread.py` untouched and unused; no shim was installed.

## Risks and limits (named, not hidden)

1. A kill is a *result difference in the declared direction*, not proof of intent (the counter's own stated
   limit). S08's rc 1 in the mutant is an uncaught exception after the guard is bypassed, not a clean
   refusal — the measurement is exact, the mutant's behaviour is a crash. S09's mutant is a *silent*
   downgrade: rc 9 with `unmapped` rather than 2, i.e. the caller's broken map is misreported as a citation
   gap.
2. Each guard's two fixtures are redundant kill paths by design (B), so a reviewer who deletes one fixture
   still sees `killed=4`; only the pair removal (C) proves the module carries the behaviour.
3. Coverage boundary of this seat: S02, S03, S05, S06, S07, S11 (other `main()` guards) and the receipts
   tool are untouched; S10 is not frozen. The full-run `receipts=0/13 sources=4/10` is the measured
   remainder for the other modules.
4. `--battery-dir` development runs print `PREDICATE C1 n/a`; the predicate is only meaningful on the merged
   `plans/battery41/` at the landing tip, which the L1 owns.

VERDICT: battery41-s_modes-killed-4/4-wrong-0
