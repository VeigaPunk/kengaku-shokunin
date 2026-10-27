# R46W2C1HoConfig — held-out Git configuration surfaces

Axes: calibration (primary); coverage of parser/config edge cases (secondary).

## Counterexample and outcome

Authored three novel module files (duplicate allowed key, case-folded section/key, and config comments with trailing comment syntax) in a scratch-only held-out directory. Their intended fixture altered the generated `.git/config` after `ctx.init`, then ran an order fixture. These are new surfaces, not copies of either frozen module list.

They were **not admitted to execution**: all three failed the counter's module-builder contract because my `build()` returned a list where `build_module_child` requires the module's `build()` to return fixture metadata in the expected form. The counter therefore reports `BUILD-ERROR` for each; none can be classified LEAKED/READ/clean/HUNG. Counts: written=3, admitted=0, read=0. This is a harness construction failure, not evidence that the fence handles these cases. No hostile finding survives.

Evidence receipt: `R46W2C1HoConfig/counter.txt`. Command used the required envelope:

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/claims/envelope.sh /fast/scratch/hyaku/kengaku-r46/R46W2C1HoConfig/env /usr/bin/python3 /fast/scratch/hyaku/kengaku-r46/R46W2C1HoConfig/lane/plans/round46_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r46/R46W2C1HoConfig/lane --work /fast/scratch/hyaku/kengaku-r46/R46W2C1HoConfig --refusals /fast/scratch/hyaku/kengaku-r46/R46W2C1HoConfig/held --sealed /fast/scratch/hyaku/kengaku-r46/R46W2C1HoConfig/held-empty`

Receipt output: `PINS total=65 mismatched=0`; each of the three `BUILD-ERROR refusal held/...`; `REFUSALS total=3 clean=0 leaked=0 read=0 hung=0 build_errors=3`; `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`; `CALIBRATION advertised=3 contradicted=3`; `PREDICATE C1 fail`; envelope ended `exit=1 ... unchanged`. The receipt's initial ENVELOPE line records the sandbox command and scratch path.

Pinned clone evidence (also in receipt context): `git rev-parse --show-toplevel` = `/fast/scratch/hyaku/kengaku-r46/R46W2C1HoConfig/lane`; `git rev-parse HEAD` = `42d5043afac952fcb43bf4798757785dd258cf85`.

Smallest safe correction: fix the hostile modules' `build()` return contract using the actual `round44_c1_verify.py` `Ctx`/`builder_source` expectations, then rerun within the envelope. No lane files were changed. No tools installed.

VERDICT: heldout-config-3-admitted-0-read-0