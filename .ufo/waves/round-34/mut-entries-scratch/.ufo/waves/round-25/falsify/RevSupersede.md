ATTACKS: R25-E1 S001–S026 census and SUPERSEDED verdict

HIGH — Weak correction tokens can falsely turn a bad census into SUPERSEDED/PASS.
- `plans/state_check.py:390-423` takes backticked correction spans and checks only substring membership in the observed census; any nonempty token list with no missing substring yields `SUPERSEDED`. It does not require all census fields or exact values.
- In `/tmp/k25w2-RevSupersede`, changed S026 from `rejected` to `queued` and replaced R25-E1 with `now `rows 2``. `python3 plans/state_check.py --summary` still reported `observed: rows 26; malformed 0; A=24 C=2; mined=18 queued=6 rejected=2`, `correction_tokens: ["rows 2"]`, `correction_missing: []`, `SUPERSEDED`, `mismatch=0`, and `VERDICT: PASS`. Thus the stale assertion is accepted despite the correction omitting—and the registry violating—the claimed status counts.

MEDIUM — The base census implementation does not establish that the IDs are exactly S001–S026.
- `plans/state_check.py:364-387` counts matching rows with numeric ID <=26; it does not detect duplicates or require the ID set to equal 1..26. In `/tmp/k25w2-RevSupersede/idtest`, changed S026 to a duplicate S025. State check still returned the original census and `mismatch=0` / `VERDICT: PASS`; `scripts/sources-census.sh validate --file .../idtest/corpus/SOURCES.md` correctly returned `E03 S025 duplicate id` (exit 1).

Landed-tip result: the reported census itself is correct at 8ea41f9ed. `corpus/SOURCES.md:23-48` lists S001 through S026 consecutively; the base rows yield 26, malformed 0, A=24/C=2, mined=18/queued=5/rejected=3. Pristine `python3 plans/state_check.py --summary` reported that exact observed value and one SUPERSEDED assertion, no mismatches; `--selftest` reported ALL PASS. The read-only canonical validator returned `file ok` for the landed registry (all 38 rows: A=35, B=1, C=2; mined=26, queued=9, rejected=3).

Installs: none.
VERDICT: BREAKS — landed counts are true, but the SUPERSEDED fallback accepts weak tokens and can conceal an incorrect census.