# SimpStateCheckGrowth — P4a–P4e minimal growth advisory

**Godspeed axes:** calibration (primary), operability (CLI/exit unchanged), novelty (no duplicate oracle logic), depth (assertion granularity vs maintenance).

## Reuse verbatim (no fork)

| Helper | `state_check.py` | P4 use |
|---|---|---|
| `p3_compare_groups`, `p3_record`, `regex_groups`, `regex_group_matches`, `receipt_exit` | :1295–1349, :1268–1293, :1527–1529 | P4a claim↔receipt numerics; P4d k/n and totals |
| `p3a_unclassified_numeric_tokens` + `P3A_NUMERIC_*` pattern | :264–274, :1368–1383 | P4a tail audit on SCORECARD :752–810 only |
| `p3_superseding_tokens`, `SUPERSEDE_RE`, `P3_CORRECTION_*` | :197–262, :554–593 | All P4 classes; R27-E already matches `R2[5-9]-E` |
| `check_p3e` loop shape + `path_exists`, `readme_index_rows` | :1209–1214, :1775–1797 | P4b row↔file / file→row; **not** full `README_INDEX_PATHS` |
| `section_bounds`, `table_rows`, `code_spans`, `named_table_row`, `add`, `read_repo_text` | :1048+, :388–426, :1144–1190 | Slice parsers for frozen docs |
| `CommandRunner` + receipt reads (prefer over live re-run) | :432–487, P3A paths :206–210 | P4a: `grader-perturb-final.txt`, `state-check-{base,final}.txt`, `round26-census-after.txt`, `sources-census-final.txt`, `gate-timing-actual-commit.txt` |

**Do not** call live `state_check.py` inside P4a (recursive); pin frozen receipts named in SCORECARD :786–808.

## Per-class minimal add

- **P4a** (~90–120 LOC): `P4A_CLAIMS` table `(id, line, claim_regex, receipt_rel, receipt_regex, token_names)`; one loop calling `p3_compare_groups`; extend `P3A_NUMERIC_FIELD_PATTERNS` for round-26 fields; floor `SCORECARD.md` stays :730 (R26-E lines :748+ valid).
- **P4b** (~55–75 LOC): freeze six paths from `corpus/README.md` :266–273 at `b5719440`; `section_bounds(..., "## Round-26 supporting artifacts", ...)`. Generalize `check_p3e` with `P4B_*` tuples; normalize `` `../plans/...` `` → `plans/...`. **Covers** counts: data row `(path_prefix, claimed_range_or_count)` — e.g. count `corpus/evidence/round26-sources/*` vs “S043–S047” prose (:268), not ad-hoc regex in checker body.
- **P4c** (~70–95 LOC): **new** `git_ls_tree(root, rev, prefix) -> list[str]` (~15 LOC, mirror `gate_timing_check.py` ls-tree usage). **Data table** of `(lesson_line, metric, rev, tree_prefix, filter_fn, expected)` for build 72/role mix, falsify 64/11 dead, 136/139, 0/82/87 vs 0/83/88 (`lessons/round-26.md` :87–123). Wave JSON under `.ufo/waves/round-26/` for role mix only if cheaper than parsing assignments JSON once.
- **P4d** (~45–65 LOC): `P4D_METRICS` from `grader-perturbation-audit.md` :26–36, :62–73, :77–87; truth from `grader-perturb-final.txt` + `perturb-oracle-final.txt` via existing regex helpers; optional single `json.loads` subprocess only if summary lines insufficient.
- **P4e** (~35–50 LOC): freeze S043–S048 `used-by` at base; **data table** `P4E_USED_BY`; observed = scan `corpus/` + `plans/` for `\bS04[3-8]\b` (reuse `read_repo_text` walk, not shell grep in instrument).

Wire: `check_p4` → `check_all` after `check_p3` (:1819); docstring v4 (:2–20). **Selftest** (~100–130 LOC): clone P3 pattern `P4_SELFTEST_ASSERTION_IDS` (:278–331) + one mutation/class (fixtures under `plans/fixtures/r27/`).

## Estimate

| Slice | LOC (assertions + data) | LOC (+ selftest) |
|---|---:|---:|
| P4a | 90–120 | +25 |
| P4b | 55–75 | +20 |
| P4c | 70–95 | +30 |
| P4d | 45–65 | +20 |
| P4e | 35–50 | +15 |
| glue + floors | 25–35 | +20 |
| **Total** | **~320–440** | **~455–565** |

## Better as data than code

- P4a full metric↔receipt mapping (~25–35 rows).
- P4b frozen path list + Covers re-derive rules per row.
- P4c wave/git expectations (revisions `8ea41f9`, `8239a56`, `9d8a00d`, `d4dfdb0…`).
- P4d population splits + family k/n table.
- P4e S043–S048 expected citers.

Keep logic in existing helpers; tables live beside `P3C_PINS` / `P3E_ROW_PATHS` (:218–248).

## Flags (pre-registration gaps)

- SCORECARD :754 glued `novelty7`; :760 glued digits (`across9`, `plus909`); :786–790 comma-glued counts — **normalize in claim_regex**, not “scan all `\d+`”.
- P4c “role mix” needs explicit seat→role map source (assignments JSON vs prose).
- P4b `plans/fixtures/r26/` both-directions: enumerate fixture files at base, not only table row existence.
- Extend `P3_CORRECTION_FLOORS` with `corpus/lessons/round-26.md` and `corpus/knowledge/grader-perturbation-audit.md`; optional `corpus/SOURCES.md` if corrections append.

## Evidence

- Pre-registration P4 defs: `plans/round-27-claims.md` :104–124.
- P3 patterns: `plans/state_check.py` :1268–1797, :1800–1819.
- Receipt pins exist: `corpus/evidence/round26-calibration/grader-perturb-final.txt` :25–27; `state-check-final.txt` present (glob).

**Installs:** none.

**VERDICT:** Add ~320–440 LOC by table-driving five `check_p4*` functions that call existing P3 comparison/supersession/README helpers; only P4c needs a small git ls-tree helper; avoid live command re-runs and full README index reuse.

---

## Append — scoped review `ExecStateCheckV4` clone (4342 LOC, +1789 vs lane v3)

**Subprocess / recursion:** `P4Evidence.COMMANDS` (:1914–1918) runs only `grader_perturb.py --summary|--json` and `perturb_oracle.py`; **no** `state_check.py` subprocess — direct recursion absent. Cost: each full `--summary` run pays **3×** instrument work (P4a summary + P4d json + oracle) with cache (:1924–1950).

**Historical vs live (main correctness risk):**
- P4a C1 / outcomes / revision C1 audited* truth is **live** `grader_summary` stdout (:2119–2120, :2235–2264, :2325–2339), not `corpus/evidence/round26-calibration/grader-perturb-final.txt` (never read). SCORECARD pins are receipt-era; live replay can drift if instrument/population changes post-receipt.
- P4a C2 / gate / sources / census kv use **frozen receipt files** (:2110–2118, :2348–2437) — consistent with content-pin intent.
- P4d family counts truth is **live** json + oracle (:3066–3223), not final calibration receipts.
- P4c wave seats/reports use **live** `.ufo/waves/round-26/*` (:2694–2706); falsify raw/md triples use **git ls-tree at named revs** (:2917–2953) — mixed model is intentional but `p4_git_repo` (:2649–2658) walking `cwd`/parents can attach to **fleet** `.git` when `--root` is a partial export → wrong tree counts or OFFLINE_UNVERIFIABLE.

**Avoidable duplication:**
- `P4_CORRECTION_LINE_RE` defined twice (:432–435, :1953–1956).
- `p4_record` / `p4_superseding_tokens` (:1959–2011) parallel `p3_record` / `p3_superseding_tokens` (:1268–1293, :554–593) without SCORECARD fallback.
- `p4_groups` (:2024–2028) duplicates `regex_groups` (:1295–1299).
- Second subprocess wrapper `P4Evidence` vs `CommandRunner` (:432–487) — could extend allowlist + shared cache.
- `p4_numbered_line(...)` invoked **twice** per assertion in P4d (:3144–3145, :3158–3159, :3183–3184) — redundant work.
- `check_p4a` ~330 LOC monolith (:2106–2438) vs advisory table-driven loop; selftest copies full lane tree (:3502–3603) inflates file ~+800 LOC beyond checker need.

**Other notes:**
- `P4.population.assertion-inventory` (:3304–3308) uses `sorted()` equality — duplicate assertion ids would not be detected.
- P4a score-held checks use `p4_round24_scores` novelty/calibration (:2050–2065, :2152–2158) not Round-26 axis prose — verify still 7/8 at base.
- P4b source Covers SUPERSEDED path (:2598–2601) hardcodes base range `043–047` vs six-id derived tokens — correct for erratum story, easy to break if anchor text shifts.

**Installs:** none.

**VERDICT (clone):** No state_check recursion; fix **live-vs-receipt** split for P4a/P4d (prefer pinned `*-final.txt` or document live as authoritative); pin git to lane root; dedupe P3/P4 helpers before merge — else ~+1400 LOC vs ~400 LOC advisory.
