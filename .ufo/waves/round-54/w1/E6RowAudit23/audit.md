# R54-C2 independent entry-row audit

Clone: `/fast/scratch/hyaku/kengaku-r54/E6RowAudit23/lane`, `HEAD=62e9bba5e4a0bed376890299aa6a09039db7e68e`.

Each command below was executed in the clone with `cwd=clone`, timeout 600 seconds, and an environment returned by importing `hermetic_env` from `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round54_c2_entrytruth.py`. Per-row temp directories (including TMPDIR) are under `/fast/scratch/hyaku/kengaku-r54/E6RowAudit23/tmp/`. All argv passed `entry_mode_ok` (no forbidden selftest/help/dry/version mode) and each script path exists in the clone. All completed in 0.1s; none timed out.

## Verdicts

| name | declared | observed | fragment-match | verdict |
|---|---:|---:|---|---|
| round51-surfaces | 1 | 1 | false | NOT CONFIRMED |
| round52-c1 | 1 | 1 | true | CONFIRMED |
| round52-c2 | 0 | 0 | N/A (green row has no evidence fragment) | CONFIRMED |

## Exact entry commands

```sh
python3 plans/round51_surfaces.py --lane .
python3 plans/round52_c1_grader_audit.py --lane .
python3 plans/round52_c2_registry.py --lane .
```

## Finding: round51-surfaces evidence fragment absent

Declared fragment: `REV 17f90355c3ec17dcf15f7980d83f1943ae428fe5`

Observed output tail (exit 1; declared exit 1):

```text
RESOLVE observed_present=12 floor=13 verdict=violated
PREDICATE R51-C1 fail
```

The actual output starts with `REV 62e9bba5e4a0bed376890299aa6a09039db7e68e`; thus the declared fragment does not occur. Exit agrees, but fragment mismatch means NOT CONFIRMED.

## round52-c1 evidence

Declared fragment `TASKS total=89 records=89 classified=88` occurs verbatim in output. Exit 1 equals declared 1. Output ends:

```text
A5 CAPTURES present+pinned_excluded=184 of 184
A5 TASKS classified+excluded=89 of 89
PREDICATE R52-C1-A5 pass
```

## round52-c2

No evidence fragment is declared for this green row. Exit 0 equals declared 0. Output tail:

```text
SELFTEST-UNBACKED 0
DUPLICATE 0
PREDICATE R52-C2 pass
```
