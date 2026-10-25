ATTACKS: `sources-census.sh` E08/E09 validation of round-25 SOURCES additions S027–S037.

## Findings
- No actionable E08/E09 finding. The 11 new registry rows are `corpus/SOURCES.md:49–59`; all use `opened=2026-10-20`. Rechecks are `on-release` (S027–S028), `180d` (S029–S035), or `90d` (S036–S037), all accepted date/cadence forms. The live results emitted no E08/E09 rows.
- Validator contract observed: `scripts/sources-census.sh:90,660–666` derives today in UTC, flags invalid/future opened dates as E08, and rejects malformed/impossible ISO rechecks or unsupported cadence forms as E09.

## Runs
Commands used the fleet script, once with TZ unset and once with `TZ=UTC`:
- `validate --root /home/vgpnk/Projects/shokunin kengaku` (TZ unset): `kengaku\tok\t/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md`; exit 0.
- Same live command (`TZ=UTC`): same output; exit 0.
- `validate /tmp/k25w2-RevValidator` (TZ unset), where the directory is a `git archive 8ea41f9ed` pristine copy: `k25w2-RevValidator\tok\t/tmp/k25w2-RevValidator/corpus/SOURCES.md`; exit 0.
- Same pristine-copy command (`TZ=UTC`): same output; exit 0.

## Residual risk and verification gaps
- This establishes census-format/date/cadence cleanliness only; it does not independently authenticate source access dates or re-open the cited sources.
- No tools installed or updated.

VERDICT: SURVIVES — targeted E08/E09 check found no counterexample; live and pristine validations pass in both timezone settings.