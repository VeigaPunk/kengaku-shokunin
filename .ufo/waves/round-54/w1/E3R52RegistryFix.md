# E3R52RegistryFix — carried R52 C2 repair

## Deliverables

- Patched counter: `.ufo/waves/round-54/w1/E3R52RegistryFix/round52_c2_registry.py`
- Committed control fixtures and red expectations: `fixture-k5.md`, `fixture-k7.md`, and `controls.json` in the same directory.
- Run receipts: `old-selftest.txt`, `patched-selftest.txt`, `old-lane.txt`, `patched-lane.txt`; source delta: `delta.diff`.

## Bug and repair

The old `selftest_unbacked` searched for any `no … --flag` phrase in the entire self-test cell and returned `False` for the whole cell. A negation about one flag (for example, no `--selftest`) therefore disabled checking of every other flag advertised in that cell. This let a distinct unsupported option in the advertised span escape the `SELFTEST-UNBACKED` finding; on the current lane, the old counter misses `order-check`. The patch identifies the locally negated flag and excludes only that flag from the advertised flag set. Other flags stay subject to the existing absent-from-script check.

## Red-before / green-after evidence

Red-before command (unmodified counter on lane):

```sh
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round52_c2_registry.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin
```

Output (exit 0):

```text
ADVERTISED total=77
REGISTERED total=77 rows=79
MISSING 0
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 0
DUPLICATE 0
PREDICATE R52-C2 pass
```

Patched command:

```sh
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-54/w1/E3R52RegistryFix/round52_c2_registry.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin
```

Output (exit 1):

```text
ADVERTISED total=77
REGISTERED total=77 rows=79
MISSING 0
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 1
  SELFTEST-UNBACKED `order-check`
DUPLICATE 0
PREDICATE R52-C2 fail
```

The focused patched regression self-test returns exit 0, `SELFTEST ok span-scoped-negation-fixture`, and `SELFTEST cases=6 failures=0`; K5 and K7 checks also report `SELFTEST ok`. Old selftest: exit 0, `SELFTEST cases=3 failures=0`. Full outputs retained in the named receipt files. The K7 fixture's expected red state is an absent `plans/ghost_tool.py`, `ENTRY-MISSING 1`, predicate fail, exit 1; K5's expected red state is the moved registry row, `MISSING 1`, predicate fail, exit 1. K5/K7 control descriptions are durable files, not changes to frozen R52/R53 artifacts.

## Scope and delta

`delta.diff` records the source comparison. Its only changes are the span-local negation correction and the selftest additions for the span case plus K5/K7 controls; no predicate threshold or prior artifact was edited. No builds, linters, formatters, or git/jj mutations were run. No tools installed. No external state changed.

Risk: the repaired lane run now correctly exposes the pre-existing unbacked `order-check` registry self-test declaration, so integration has a red live-lane result to resolve separately; this seat does not edit the registry. The lane run reports 77 advertised scripts / 79 rows as observed on the current checkout.

Report: `.ufo/waves/round-54/w1/E3R52RegistryFix.md`