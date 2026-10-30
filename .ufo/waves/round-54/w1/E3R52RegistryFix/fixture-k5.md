# K5 decoy-table control fixture

Apply in a disposable copy of the lane: remove the `round28-census` registry row from the `## Gate/probe registry` section, then append this decoy table under a separate `## Decoy inventory (not the registry)` heading:

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| `round28-census` | gate | `python3 plans/round28_census.py --root . --revision REV` | `0` ok | none | none | read-only | kengaku |

Expected counter output: `MISSING 1`, `PREDICATE R52-C2 fail`, exit 1. This detects registry-block extraction accidentally accepting tables outside the named section.