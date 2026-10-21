# FDisclosure — Round 27 population-disclosure review

Axes: calibration; frozen-population transparency.
Identity: KengakuR27.FDisclosure, **not** candidate writer KengakuR27. Observed scratch base: `b5f62e5e637b34a1549e3475fc58b4227ed87e5a` in `/tmp/kengaku-r27-FDisclosure`.
Read the whole `plans/round-27-claims.md`, including Amendment 1, and the complete draft `.ufo/waves/round-27/drafts/extraction-policy-comparison.md`. Its proposed canonical destination is `corpus/knowledge/extraction-policy-comparison.md`; that file is absent in the pinned clone, so this is not a canonical-entry reread or admission claim.
LSP status: unavailable. `read xd://lsp` returned “No such tool: xd://lsp”; no references/definition/diagnostics requests could be made. No install/update performed.

## Finding — Medium: all summary OUT_OF_POPULATION disclosures can disappear while stock checks pass

Evidence: `plans/state_check.py:3363-3377` renders the summary; its selftest controls at `:3759-3781` assert internal `Assertion` records, not rendered output. `plans/round27_census.sh:66-83` saves only the summary's first line and counts P4 IDs from JSON; it does not census summary disclosure lines.

On the private clone only, I applied the prior M3 mutation at `plans/state_check.py:3369`: removed `OUT_OF_POPULATION` from the `print_summary` emission set while leaving assertion generation and counts unchanged. Then:

- `PYTHONDONTWRITEBYTECODE=1 python3 -B plans/state_check.py --selftest` → **exit 0**; final line: `[selftest] ALL PASS (canonical seed, pointers, out-of-population box, pointer-only, R25–R29-E exact-token supersession, P2/P3 R27/R29 corrections, P4 R27-only supersession, P2e/P3c OUT_OF_POPULATION retention, P3a–P3e and P4a–P4e red mutations)`.
- `PYTHONDONTWRITEBYTECODE=1 sh plans/round27_census.sh` → **exit 0**; it still reported `c2_state_check_first_line=assertions=327 match=318 mismatch=0 superseded=6 offline_unverifiable=3`, `c2_p4_assertions=48`, `c2_p4_mismatch=0`, `c2_exit=0`.
- `set -o pipefail; PYTHONDONTWRITEBYTECODE=1 python3 -B plans/state_check.py --summary --root /tmp/kengaku-r27-FDisclosure | awk '/^OUT_OF_POPULATION:/ { n++ } END { printf "out_of_population_lines=%d\\n", n }'` → **exit 0**, `out_of_population_lines=0`; the same count on the unmutated candidate tree was `24`.

Thus the existing summary currently emits disclosures, but the stock selftest and round-27 census do not detect total suppression. Add a stdout assertion/census (ideally compare emitted disclosure IDs/counts to JSON), or this regression remains green. This reproduces the M3 survivor described in `.ufo/waves/round-27/build/MutStateCheckSupersede.md:33-39`; it is not a live-tree mutation.

## Checked population and extension

- Frozen projection control: `PYTHONDONTWRITEBYTECODE=1 python3 -B plans/fixtures/r27/p23_preservation.py --old /tmp/kengaku-r27-FDisclosure/base-b5719440/plans/state_check.py --new /tmp/kengaku-r27-FDisclosure/plans/state_check.py --root /tmp/kengaku-r27-FDisclosure/base-b5719440` → **exit 0**, `compared: ids=298 record_pairs=298 differences=0 order=same`; both sides retain `P2=255 P3=43`, including 20 `OUT_OF_POPULATION` records on the frozen tree.
- On the candidate tree the v4 checker emits 24 P2/P3 `OUT_OF_POPULATION` records. Relative to the frozen tree, the four additional disclosures are `P2e.out-of-population.row.lessons/round-27.md@97`, plus file records for `evidence/round27-calibration/`, `evidence/round27-sources/`, and `lessons/round-27.md`. The three P2a capability-row disclosures remain present. These additions are out of the frozen P2/P3 population, not silently admitted.
- Base v3 JSON has `base_p4_assertions=0`; candidate JSON has `p4_total=49 inventory=MATCH`, classes `P4a:9 P4b:8 P4c:11 P4d:14 P4e:6`, `p4_mismatches=0 superseded=1` (48 comparable assertions plus the inventory assertion). The integrated census reports its intentionally P4a–P4e-only count: `c2_p4_assertions=48`, `c2_p4_mismatch=0`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -B plans/fixtures/r27/p4_mutate.py --checker plans/state_check.py --repo /tmp/kengaku-r27-FDisclosure --base b5719440e5eee46c1886fddbdf7bdc1624829454` → **exit 0**, `VERDICT: 5/5 mutants red for their own class`. P4 selftest also accepts a full R27-E correction and rejects R29-E (`state_check.py:3736-3757`).

## Supersession-range survivor

I narrowed only the scratch `SUPERSEDE_RE` at `plans/state_check.py:204` from `R2[5-9]-E` to `R2[5-6]-E`. `PYTHONDONTWRITEBYTECODE=1 python3 -B plans/state_check.py --selftest` → **exit 1**, `selftest: sources-registry expected SUPERSEDED, got MISMATCH`. The selftest has explicit P2 R27/R29 cases at `:3874-3879` and P3 R27/R29 cases at `:4073-4079`, so this kills the M1 narrowing mutant; the original regex was restored in the scratch clone.

## Residual risk and verification gaps

- The integrated census run also emitted `q13_round27_lesson_exit=1`; Q13/Q15 gate authority is outside this population-disclosure slice and was not investigated here.
- This is an offline Python checker, so runtime routing, same-identity rerouting, and saturation behavior are not applicable. No live/runtime requests were made.

VERDICT: **RECOMMEND HOLD on the disclosure-regression guard** — the R27–R29 narrowing survivor is killed and the P2/P3/P4 frozen populations are represented, but total suppression of summary OUT_OF_POPULATION output survives both stock selftest and `round27_census.sh`.

## Follow-up (same seat, appended 2026-10-21) — M3 recheck against the rendering redcheck

Author claim: live `plans/state_check.py` sha256 `5db1eb787d0724405fda8d747957b5ad84122c5410571c9b8cac3c2f6d9ac30c` (the `5db1…c30c` cited by KengakuR27) adds an actual `print_summary` OUT_OF_POPULATION rendering redcheck. I copied the live bytes over the checker in my private clone `/tmp/kengaku-r27-FDisclosure` (no lane edit) and re-ran the exact M3 mutant — removing `OUT_OF_POPULATION` from the `print_summary` emission set, leaving generation and counting unchanged:

- Pristine control: `PYTHONDONTWRITEBYTECODE=1 python3 -B plans/state_check.py --selftest` → **exit 0**, final line `[selftest] ALL PASS (…)` and new line `selftest ok OUT_OF_POPULATION: summary renders disclosed entries` (redcheck implementation at `plans/state_check.py:4111-4117`: captures `print_summary(p2_oop)` via `contextlib.redirect_stdout` into `io.StringIO` and requires the rendered `OUT_OF_POPULATION: {id}` line).
- Mutant: same command → **exit 1**, stderr/stdout ends `selftest FAIL OUT_OF_POPULATION: summary disclosure was removed`. **KILLED.**
- Census under the same mutant: `PYTHONDONTWRITEBYTECODE=1 sh plans/round27_census.sh` → still **exit 0** with a green first line; `round27_census.sh` alone remains blind to disclosure suppression (unchanged tool), so the redcheck's authority rests on `--selftest`.
- Restoration: exact reverse edit; `sha256sum` → `5db1eb78…c30c` (byte-identical to live); `--selftest` → **exit 0** again.
- Keyed preservation: `PYTHONDONTWRITEBYTECODE=1 python3 -B plans/fixtures/r27/p23_preservation.py --old /tmp/kengaku-r27-FDisclosure/base-b5719440/plans/state_check.py --new /tmp/kengaku-r27-FDisclosure/plans/state_check.py --root /tmp/kengaku-r27-FDisclosure/base-b5719440` → **exit 0**, `compared: ids=298 record_pairs=298 differences=0 order=same`, both sides `P2=255 P3=43`; new checker summary `assertions=329 … offline_unverifiable=5`.

VERDICT: **RECOMMEND CLOSE the prior HOLD** — the exact M3 stdout-suppression mutant is now killed by `--selftest` (exit 1) with the pristine control green and byte-exact restoration; P2/P3 keyed preservation remains 298/298 identical. Residual: `plans/round27_census.sh` by itself still does not census rendered disclosures (mutant census exit 0), so detection depends on `--selftest` staying in the admitted detector chain.