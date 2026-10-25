# FSimplify — round 27 v4 / C1 extension duplication review

Seat: KengakuR27.FSimplify. Base observed: `b5f62e5e637b34a1549e3475fc58b4227ed87e5a` (scratch `/tmp/kengaku-r27-FSimplify`). No production edits. LSP unavailable (`ExecStateCheckV4.md:25`); semantic reachability via ripgrep + scratch mutants only.

## Axes (godspeed)

| Axis | Simplifier lens |
|---|---|
| **novelty (C1)** | Independent oracle + hand fixtures must stay parallel to the instrument; do not merge extract paths. |
| **calibration (C2/P4)** | Frozen assertion ids, R27-E supersession regex, P4a–P4e red selftests, keyed P2/P3 projection. |
| **operability** | One authoritative table per concern; avoid twin fixture corpora that drift. |
| **separability** | `policy_oracle.py` must not import `grader.py` / `parser_policy_compare.py` extractors. |

## Safe deletions (scratch-verified)

1. **`plans/state_check.py:1954-1957`** — duplicate `P4_CORRECTION_LINE_RE = re.compile(...)` identical to `:433-436`. Second binding is dead weight (module-level reassign). **Evidence:** removed on scratch; `python3 plans/state_check.py --selftest --root /tmp/kengaku-r27-FSimplify` → exit 0, tail line `[selftest] ALL PASS (... P4a–P4e red mutations)`. **References:** grep shows uses only at `:1973`, `:1979` (single name after delete). **Preserves:** P4 correction parsing, R27-E acceptance, P4 red mutations.

2. **`plans/parser_policy_compare.py:409-415`** `_mutant_e0_no_bare_fallback` — byte-identical to `e5_fence_only` (`:92-98`). **Replace** `MUTANTS["E0"]` target with `e5_fence_only` at `:444`. **Evidence:** scratch edit; `python3 plans/parser_policy_compare.py --selftest --root /tmp/kengaku-r27-FSimplify` → `killed=9 failures=0`. **Preserves:** seeded E0 mutant kill (`bad-last-fence-to-bare`), hand_cases=58, pin-rejection.

## Deletion candidates — do **not** delete without contract change

| Candidate | Why retained |
|---|---|
| **`PROBES` dict (`parser_policy_compare.py:355-406`)** | Overlaps `policy_cases.CASES` on only **1/31** probe rows (same raw+expected); **30/31** probe-only. Mutant kill uses `PROBES[pid]` only — E6 mutant **not** killed by any E6 row in `policy_cases` (needs ` ```python\n{"a":1}\n```\n{"b":2}` style row; probe `any-label-fence-wins`). Merging tables requires new E6 hand row + selftest refactor. |
| **`policy_oracle.py` extract stack (`:17-110`)** | Pre-registration independent oracle; duplicates `FENCE`/`BARE_RE`/decode logic by design. Deleting = breaks separability / Q15 cross-check. |
| **`policy_cases.py` vs `PROBES`** | 58 vs 31 rows; different naming and coverage. Collapsing improves operability but is a small rewrite, not a line delete. |
| **Per-policy functions E0/E1/E5/E6 fence blocks** | Shared shape but distinct frozen semantics; factoring saves lines, not authorities. |

## Maintainability: grouped tables vs ad-hoc regex

- **P4 v4 (`state_check.py`)** — Frozen ids as tuples (`P4A_ASSERTION_IDS`, `P4D_FAMILY_ORDER`, `P4E_SOURCE_IDS`) plus small regexes (`P4_CORRECTION_ID_RE`, `P4_CITATION_RE`) scale better than scattering assertion strings in check bodies. The duplicate `P4_CORRECTION_LINE_RE` is the main v4 hygiene defect; P3 already uses the same line shape with `P3_CORRECTION_LINE_RE` (`:267-269`) — **not** mergeable without widening P4’s R27-only id gate.
- **C1 instrument** — Regex constants at top (`FENCE_ANY`, `gp.FENCED_RE`, `gp.BARE_RE`) match the pre-reg table; **grouped dispatch** in the oracle (`fenced_policy`, `decode_scan`) is easier to audit than nine copy-pasted blocks, but the main instrument keeps explicit `e0_lane`…`e8_decode_last` for readable mutants (`MUTANTS` references `e0_lane`, `e2_bare_last`, etc.). **Risk:** `PROBES` + `policy_cases` double-maintain edge semantics (Amendment 1 E1/E2/E6/E8); prefer one table with `(policy, name, raw, expected, probe_for_mutant?)` over growing a third regex-only path.
- **Ad-hoc regex growth** — Contained in three sites (`grader_perturb.FENCED_RE`/`BARE_RE`, `parser_policy_compare.FENCE_ANY`, oracle `FENCE`/`ANY_LABEL_FENCE`). Any label change in claims must touch all three; that is intentional redundancy, not deletable duplication.

## Preserved contract (unchanged by above deletions)

- P4: 49 frozen ids, `--selftest` P4a–P4e reds, R27-E supersession, P2/P3 byte-identical projection on base tree (`ExecStateCheckV4.md:18-23`).
- C1: E0 baseline on 1964, `--selftest` mutant kills, `policy_cases` 58, pin-before-policy.
- Red controls: `plans/fixtures/r27/p4_mutate.py` untouched; no lane file writes.

## Installs

None.

VERDICT: **Two line-level deletions** (duplicate P4 regex; E0 mutant alias to `e5_fence_only`) improve operability without harming novelty/calibration axes. **Do not delete** oracle duplicate extractors or `PROBES` without adding E6 hand coverage and refactoring selftest. Primary maintainability win is consolidating `PROBES` into `policy_cases` (future), not regex dedup across oracle/instrument.
