# Sibling-Overlap Scan & Connector Report — Round 85 (w1)

**Seat:** ConnectorR85  
**Role:** connector (read-only sibling-overlap scan & UFO-FSD cross-proposal synthesis)  
**Lane:** kengaku-shokunin  
**Base revision:** `0de45354d7aff18e4a23a348ec13de3a1f707a44`  
**Freeze commit:** `1a45aeb5e8706b1518ba58fd0fe882df1631e2a0`  
**Lane tip:** `35b1e4e09d7666889e561ede274485aba1e2ad11`  
**Date:** 2026-11-04  

---

## 1. Search Scope and Sibling Master Revisions

Per the canonical seat assignment, a comprehensive read-only search was conducted across:
1. Sibling lanes: `/home/vgpnk/Projects/shokunin/*-shokunin` (20 sibling repositories; examined `corpus/`, `plans/`, `tools/`, and repo-wide).
2. Staged backlog: `/home/vgpnk/Projects/shokuknow/merge/kengaku/` (65 knowledge entries, 175 staged rows).
3. In-lane scope: `kengaku-shokunin/plans/`, `corpus/`, `PROVINCE.md`, and population ledgers.

### Recorded Sibling Master / Tip Commits (`git -C <repo> rev-parse master`):
- `audio-shokunin`: no master branch (primary `main: f9da7ee97e0ba95da1803c2afe9c616c519bae18`, `HEAD: f9da7ee97e0ba95da1803c2afe9c616c519bae18`)
- `chousa-shokunin`: `master: 5eeca32ba9ad80081d19906c7cb52dff35891e8c` (`HEAD: 5eeca32ba9ad80081d19906c7cb52dff35891e8c`)
- `game-dev-2d-shokunin`: no master branch (primary `main: 1e033ef053beedf9a201daa21fbeb9c8b2f72dc3`, `HEAD: 1e033ef053beedf9a201daa21fbeb9c8b2f72dc3`)
- `game-dev-3d-shokunin`: no master branch (primary `main: 39ca3973c7865456d97fae18033f3f460c6cf8c1`, `HEAD: 39ca3973c7865456d97fae18033f3f460c6cf8c1`)
- `kagi-shokunin`: `master: f6d93c5b34e7c30955ab545592f3d4ddd724729c` (`HEAD: f6d93c5b34e7c30955ab545592f3d4ddd724729c`)
- `kaidoku-shokunin`: no master branch (primary `main: 26f4e1ba85e0ca85921ea99f3fdd02a619373b78`, `HEAD: 26f4e1ba85e0ca85921ea99f3fdd02a619373b78`)
- `kake-shokunin`: `master: 76225160d0dff8d2042fbcd037bd08b0971d5e07` (`HEAD: 76225160d0dff8d2042fbcd037bd08b0971d5e07`)
- `kama-shokunin`: `master: 3ff23da3f291ce8abf7bf5c54f9abacec67e3e8d` (`HEAD: 3ff23da3f291ce8abf7bf5c54f9abacec67e3e8d`)
- `kasegi-shokunin`: `master: b6db9e818d322726e39cb441f2179d34d4170275` (`HEAD: b6db9e818d322726e39cb441f2179d34d4170275`)
- `kengaku-shokunin`: `master: 35b1e4e09d7666889e561ede274485aba1e2ad11` (`HEAD: 35b1e4e09d7666889e561ede274485aba1e2ad11`) [measuring lane]
- `kotoba-shokunin`: `master: aaa3978753a409b63b5feca48c923ee9948f1539` (`HEAD: aaa3978753a409b63b5feca48c923ee9948f1539`)
- `kotodama-shokunin`: no master branch (primary `main: 4956282281dac1306cfbe59523e46dde99749d75`, `HEAD: 4956282281dac1306cfbe59523e46dde99749d75`)
- `kumitate-shokunin`: `master: 232350995d3001e606609aaf22ba1b58168d3655` (`HEAD: 232350995d3001e606609aaf22ba1b58168d3655`)
- `lore-shokunin`: no master branch (primary `main: 0f044aa7c7e4e17cfd5b6278179709b60db45d61`, `HEAD: 0f044aa7c7e4e17cfd5b6278179709b60db45d61`)
- `mado-shokunin`: `master: 3905311c75a39c5710413105865c0a1a7dd0116a` (`HEAD: 3905311c75a39c5710413105865c0a1a7dd0116a`)
- `mori-shokunin`: `master: 30a29797012281b9fd0c748b38b929ac67f8c754` (`HEAD: 30a29797012281b9fd0c748b38b929ac67f8c754`)
- `revenger-shokunin`: no master branch (primary `main: 5915ad8d71c19ad377829d130ba1c35445eb32a4`, `HEAD: 5915ad8d71c19ad377829d130ba1c35445eb32a4`)
- `souji-shokunin`: `master: 1e8bfd87a9f6ea9a1db4ad34f6e4cdd2b218bcd4` (`HEAD: 1e8bfd87a9f6ea9a1db4ad34f6e4cdd2b218bcd4`)
- `tabi-shokunin`: `master: 6c19979fe63f3b9ec35179ca57bb91c6356bff25` (`HEAD: 6c19979fe63f3b9ec35179ca57bb91c6356bff25`)
- `tameshi-shokunin`: `master: d10a9c66d6181cddcad52cdbffd672beb886ff6c` (`HEAD: d10a9c66d6181cddcad52cdbffd672beb886ff6c`)
- `tsukuroi-shokunin`: `master: 467a9b7891a5939dab8460ec6f591fbb16bd82e9` (`HEAD: 467a9b7891a5939dab8460ec6f591fbb16bd82e9`)

---

## 2. Target Search Results & Rulings

### Target 1: `sqlite-db-truncate`, `recover.json`, `set intersection`, threshold graders, `duplicates=8`

1. **`sqlite-db-truncate`**:
   - Sibling lanes (`corpus/`, `plans/`, whole repos): **0 hits**.
   - Staged backlog (`shokuknow/merge/kengaku/`): **0 hits**.
   - In-lane (`kengaku-shokunin`): 8 occurrences across `plans/round-85-claims.md`, `plans/round85-cases.json`, `plans/round85_c1_replay.py`, `plans/round85_sqlite_truncate_probe.py`, `plans/grader-population-ledger.json`, `corpus/evidence/round52/graders/sqlite-db-truncate/tests/test_outputs.py`, and `corpus/evidence/round85/sqlite-db-truncate-probe.txt`.
   - Ruling: **clean new execution**; zero sibling overlap.

2. **`recover.json`**:
   - Sibling lanes: **0 exact matches**. Substring match in `mado-shokunin/.ufo/waves/round-56/w3/R56W3MutBwrapChannels/receipts/jail-probe-nosb.out:30489, 30516` (`/tmp/ff_out_recover.json`, `/tmp/ff_steps_recover.json` — Playwright browser test path).
   - Staged backlog: **0 hits**.
   - Ruling: `adjacent` (false-positive substring in historical wave test output; zero relation to SQLite recovery).

3. **`set intersection`**:
   - Sibling lanes: **0 hits** for grader assertions or benchmark evaluation.
   - Sibling metadata hits:
     - `kama-shokunin/.ufo/waves/round-35/w1/out/ExecCollision.md:19` (`comm -12` ID set intersection for SOURCES.md).
     - `kake-shokunin/.ufo/waves/round-69/w1/ExecCensusMirror/guard.sh:44` (`comm -12` registry/staged set intersection).
     - `kagi-shokunin/.ufo/waves/round-25/build/ConnSiblings4.md:14` (URL set intersection in source deduplication).
     - `kaidoku-shokunin/.ufo/waves/round-44/w1/artifacts/R44ConnPattern/freeze_walk_probe.py:25` (git log path set intersection).
     - `kaidoku-shokunin/.ufo/waves/round-32/a2audit/A2C2Labels.md:51` (word-set intersection for description-anchor scoring).
   - Staged backlog: **0 hits**.
   - Ruling: `adjacent` (all sibling hits are administrative metadata/provenance set intersections; none touch benchmark graders).

4. **Threshold graders / threshold-count graders**:
   - Sibling lanes: **0 hits** for agentic benchmark or Terminal-Bench threshold graders.
   - `audio-shokunin/corpus/QUALITY.md:14`, `corpus/fixtures/measure_audio.py:32246` (DSP sample amplitude, LUFS and contrast thresholds).
   - `kotoba-shokunin/.ufo/waves/round-79/build/Kb79R01SpecRow.q70-claude.md:962` (Claude Code plugin eval documentation snapshot).
   - Staged backlog `shokuknow/merge/kengaku/knowledge/corpus/knowledge/judge-calibration-thresholds.md:45` (statistical AC2 kappa threshold 0.6 for human-LLM judge agreement).
   - Ruling: `adjacent` (audio signal processing thresholds and statistical judge agreement; zero overlap with TB2 threshold graders).

5. **`duplicates=8`**:
   - Sibling lanes: **0 hits**.
   - Staged backlog: **0 hits**.
   - In-lane (`kengaku-shokunin`): `plans/round85-cases.json:44` (frozen test vector staging 16 duplicated rows, evaluated to 8 unique tuples under set semantics, predicted score `8/P`).
   - Ruling: **clean in-lane vector**; zero sibling overlap.

---

### Target 2: The Q61 Idea (Admission Counter with a Committed Filler/Junk Package That Must Stay Red)

- Sibling lanes (`corpus/QUALITY.md` and `plans/`): **0 hits** for `Q61`, `filler`, `junk`, or admission counters shipping committed filler packages.
- Sibling `QUALITY.md` inspection across all 20 sibling lanes confirms that no sibling holds a criterion or gate of this shape.
- In-lane (`kengaku-shokunin`): Landed in `corpus/QUALITY.md:1320` as `Q61 — an admission counter ships a committed filler package that must stay red...` (`considerthese/2026-10-26.md` §2), with executable verification in `plans/round85_c2_debt.py` (`--control-presence`, fixture `q61-no-citation`).
- Ruling: `none` in sibling lanes.

---

### Target 3: The R84-V8 Class (Registry Gate Requiring a Declared Flag to Appear Literally in the Instrument's Bytes)

- Sibling lanes:
  - `mori-shokunin/tools/mori-gate-registry.py:304-343` (landed in round 45, P-C2): An in-lane registry auditor checking `SKILL.md` gate tables. It parses the declared self-test flag in `declared_flag()` and verifies via `escape_branch()` / `_flag_in_python_tests()` that the declared flag exists in Python parser keys (`add_argument("--flag")`) or shell `case` patterns (`--flag)`), masking comments.
  - `kama-shokunin/tools/gate-registry-check.py:22-30`: Checks structural cell presence (`thin-row`, `empty-entry`, `empty-exit-map`, `missing-path:PATH`), but does not check self-test flags in script bytes.
  - `kotodama-shokunin/tools/check-gate-registry.py:1-10`: Checks entry-command script paths, but does not check self-test flags.
  - No sibling owns or duplicates `kengaku`'s `plans/round82_c1_plans_registry.py`.
  - No sibling references or claims `R84-V8`.
- Ruling: `adjacent` (`mori-shokunin/tools/mori-gate-registry.py` is an independent implementation of the same registry-audit family tailored to mori's tools; zero duplicate or contest).

---

### Target 4: Backlog Package `shokuknow/merge/kengaku/`

- Staged package contents: 65 knowledge entries, `MERGE-REPORT.json`, `MERGE-REPORT.md`, `SOURCES.append.md`.
- `sqlite-db-truncate` and `recover.json`: **0 matches** across all files.
- Terminal-Bench 2.0 graders:
  - Discusses TB 2.0 release identity (`terminal-bench-release-identity.md:32-46`, commit `2fd12b88`), Harbor verifier execution model (`benchmark-verifier-execution-model.md:16-33`, `environment_mode = "shared"`), and task review automation canary checks (`benchmark-task-validity-checklist.md:2-8`).
  - Does NOT stage any TB2 member grader code, test captures, or offline replay tools.
- Threshold-count graders: **0 matches**.
- Status: Confirms `plans/round-85-claims.md` §Frontier and wave contract: *“Assimilation: none. `merge/kengaku/` (175 staged rows, 65 knowledge entries) is not drawn on by these frozen claims; it remains unadopted backlog.”*
- Ruling: `none`.

---

## 3. Table of Search Hits

| Path | Line(s) | Term Matched | Ruling | One-Line Nature of Hit |
|---|---|---|---|---|
| `mado-shokunin/.ufo/waves/round-56/w3/R56W3MutBwrapChannels/receipts/jail-probe-nosb.out` | 30489, 30516 | `recover.json` | `adjacent` | False-positive substring match in browser test paths (`/tmp/ff_out_recover.json`, `/tmp/ff_steps_recover.json`). |
| `mori-shokunin/tools/mori-gate-registry.py` | 304–343 | declared flag in tool bytes | `adjacent` | In-lane registry auditor verifying declared self-test flags appear in parser keys / case branches for mori's tools. |
| `kama-shokunin/.ufo/waves/round-35/w1/out/ExecCollision.md` | 19 | `set intersection` | `adjacent` | Shell `comm -12` set intersection verifying SOURCES.md S-id collision absence. |
| `kake-shokunin/.ufo/waves/round-69/w1/ExecCensusMirror/guard.sh` | 44 | `set intersection` | `adjacent` | Shell `comm -12` registry/staged S-id set intersection check. |
| `kagi-shokunin/.ufo/waves/round-25/build/ConnSiblings4.md` | 14, 22, 30 | `set intersection` | `adjacent` | URL set intersection in sibling source deduplication check. |
| `kaidoku-shokunin/.ufo/waves/round-44/w1/artifacts/R44ConnPattern/freeze_walk_probe.py` | 25 | `set intersection` | `adjacent` | Git log path-set intersection verifying frozen drift absence. |
| `kaidoku-shokunin/.ufo/waves/round-32/a2audit/A2C2Labels.md` | 51 | `set intersection` | `adjacent` | Word-set intersection for description-anchor scoring. |
| `audio-shokunin/corpus/QUALITY.md` | 14, 30 | `threshold` | `adjacent` | DSP signal thresholds (LUFS, dB contrast, sample amplitude bounds). |
| `kotoba-shokunin/.ufo/waves/round-79/build/Kb79R01SpecRow.q70-claude.md` | 962 | `threshold` | `adjacent` | Documentation snapshot quoting Claude Code plugin eval CI gating. |
| `shokuknow/merge/kengaku/knowledge/corpus/knowledge/judge-calibration-thresholds.md` | 45, 55 | `threshold` | `adjacent` | Pre-registered AC2 kappa threshold 0.6 for human vs LLM judge agreement. |
| `shokuknow/merge/kengaku/knowledge/corpus/knowledge/terminal-bench-release-identity.md` | 32–46 | `terminal-bench` | `adjacent` | Historical survey entry defining TB 2.0 release commit `2fd12b88`; no member grader code or capture. |
| `kengaku-shokunin/plans/round85-cases.json` | 3, 44 | `sqlite-db-truncate`, `duplicates=8` | in-lane | Frozen 8-case two-leg test table discriminating set semantics, type sensitivity, and threshold boundaries. |
| `kengaku-shokunin/plans/round-85-claims.md` | 13–80 | `sqlite-db-truncate`, `recover.json` | in-lane | Frozen R85-C1 claim specifying first offline member replay of serialization-schema class. |
| `kengaku-shokunin/corpus/QUALITY.md` | 1320 | `Q61`, `filler` | in-lane | Landed Q61 criterion requiring admission counters to ship committed filler packages that must stay red. |
| `kengaku-shokunin/plans/round82_c1_plans_registry.py` | 163–168 | declared flag in script bytes | in-lane | In-lane registry completeness gate verifying literal self-test flag occurrence in script bodies. |

---

## 4. Verdict and Consequence for Claims

**Verdict:** `overlap: none`

### Consequence for Claims:
1. **R85-C1 Coverage Advance (Zero Collision):**
   - In `kengaku-shokunin`'s BASE state (`0de45354d7aff18e4a23a348ec13de3a1f707a44`), `sqlite-db-truncate` is recorded in `plans/grader-population-ledger.json` as `unexecuted` (reason: `unattempted`).
   - Replaying its captured grader offline advances the population ledger cleanly:
     - Executed members: `28 → 29`
     - Unexecuted members: `60 → 59`
     - Serialization-schema class: `0 of 9 → 1 of 9` (in census: `1 of 10 → 2 of 10`)
     - File-artifact class: `20 of 76 → 21 of 76`
   - No sibling lane replays, cites, or asserts ownership over `sqlite-db-truncate` or any Terminal-Bench 2.0 grader.
2. **R85-C2 Calibration Discharge (Zero Collision):**
   - All eight routed defects (R84-V1, V2, V3, V5, V6, V7, V8, V9) and the Q61 criterion are strictly in-lane repairs of outside verifier spot-check findings.
   - Sibling registry checkers (`mori-gate-registry.py`) operate on independent in-lane tools without conflict.

---

## 5. Adjacency Analysis

1. **Database Internals & File Carving Semantics (Adjacent / Unowned):**
   - The task `sqlite-db-truncate` simulates an interrupted or truncated SQLite 3 database file and recovers records into `/app/recover.json`.
   - SQLite page format, B-tree record parsing, WAL frame decoding, and low-level forensics belong to database internals and reverse-engineering domains (`kaidoku-shokunin` / forensics).
   - Per `kengaku-shokunin/PROVINCE.md`: *“This lane owns what the captured grader checks and what passes it — nothing else.”*
   - The captured grader `test_outputs.py` checks only JSON set intersection cardinality `len(soln_tuples & data_tuples) > 6`.
   - Any claim about SQLite page header corruption, B-tree balance, or forensic carver implementations is strictly adjacent and must not be absorbed.
2. **Methodological Adjacencies:**
   - **chousa-shokunin:** Authority tier and scope taxonomy for `corpus/SOURCES.md`.
   - **tameshi-shokunin:** General mutation testing frameworks.
   - **mori-shokunin:** Host-level audit and registry gate implementations (`mori-gate-registry.py`).
   - **kumitate-shokunin:** Wave orchestration and sandboxing primitives.

---

## 6. UFO-FSD Connector Move: Substrate-Aware Tree Resolution for Q20 Out-of-Band Gate Verification

### 6.1 Evidence Across Round-85 Seats
- **ExecDebtR85 (`gate-receipt.txt` §4, Findings F1–F4):**
  - Demonstrated that the canonical Q20 out-of-band gate roster verification (`git archive <TIP> | tar -x`) unpacks a repository tree lacking `.git`.
  - While all 7 standing roster gates (`grader.py`, `sources_adopt.py --selftest`, `registry_check.py --selftest`, `config_projection.py --selftest`, `benchmark_spec_audit.py --selftest`, `gate_timing_check.py --selftest`, `state_check.py --selftest`) run cleanly (rc=0) inside the archive extraction, the round-85 counters (`round85_c1_replay.py --selftest/--mutants` and `round85_c2_debt.py --selftest`) unconditionally invoke git plumbing (`git -C <lane> rev-parse` and `git archive`).
  - In an archive extraction, both exit 2 (`DEFECT SETUP unresolved-revision master`), preventing out-of-band verification from succeeding on the round's new counters.
- **ReviewerC185 (`derived.txt`):**
  - Independently derived the exact grader semantics from `corpus/evidence/round52/graders/sqlite-db-truncate/tests/test_outputs.py` before inspecting the probe.
  - Confirmed that under Python set semantics, integer JSON values (`10`) equal float solution values (`10.0`), proving that strict float checks would be false defects.
- **ExecBaseR85 (`replay.txt`):**
  - Confirmed that at master tip (`217910c5`), both counters hit their frozen targets (`PREDICATE R85-C1 pass`, `PREDICATE R85-C2 pass`, `SENSITIVITY failed_at_base=8`).
  - Traced that earlier in the wave, work-directory auto-creation (`mkdir -p`) was missing and caused setup failures on fresh scratch paths.
- **ExecCensusR85 (`census.txt`):**
  - Revealed that `round75_c1_index_parity.py` and `round79_c1_population_ledger.py` initially reported defects on missing README rows and class counts, which the L1 subsequently repaired in commits `2410f403` and `35b1e4e0`.

### 6.2 Affected Axes
- **Calibration (R85-C2):** Discharging routed debt requires that the instruments conform to the lane's standing QUALITY standards, including Q20 (out-of-band gate roster runnable from clean archive extractions).
- **Coverage (R85-C1):** Hermetic repeatability of the `sqlite-db-truncate` replay across both live git worktrees and extracted distribution archives.

### 6.3 Contradiction Stated Explicitly
The round contract establishes:
1. `QUALITY.md` Q20: *“The gate roster is runnable out-of-band from an archive extraction (`git archive | tar -x`) without ambient repo access.”*
2. `plans/round-85-claims.md` §R85-C2: Discharges R84-V8 and R84-V9 via executable base-sensitive counters.

However, `plans/round85_c1_replay.py` and `plans/round85_c2_debt.py` hardcode `git -C <lane>` invocations in their `rev_tree()` helpers. When verified in a standard Q20 archive extraction where `.git` is absent, both counters fail closed with exit 2 `SETUP`.  
Furthermore, `plans/round85_c2_debt.py` check `v8` invokes `plans/round82_c1_plans_registry.py` against `lane`, but `round82_c1_plans_registry.py` lines 254–255 read tool script bodies directly from the working filesystem (`lane / rel`) rather than from the historical git revision tree, causing `v8` to be worktree-revision-coupled.

### 6.4 Proposed Bounded Move
1. **Substrate-Aware Tree Resolution in R85 Counters:**
   Update `rev_tree()` in `plans/round85_c1_replay.py` and `plans/round85_c2_debt.py` to inspect whether `(lane / ".git").exists()`.
   - If `.git` is present: preserve the current strict `git -C <lane> archive` per-path extraction, guaranteeing revision-pinning and base-sensitivity.
   - If `.git` is absent (Q20 archive extraction): fall back to `Tree(lane, "worktree", "archive")` for `master` and worktree evaluations, allowing selftests and tip evaluations to run cleanly (rc=0) without a `.git` store.
   - For historical revisions (`FREEZE_REV`, `BASE_REV`) in an archive environment where git history is physically absent, fail with a typed diagnostic (`ARCHIVE_NO_GIT_HISTORY`) rather than an unhandled setup crash, or accept `--repo <path-to-git-store>` as an optional override.
2. **Worktree-Decoupled V8 Gate Execution:**
   In `round85_c2_debt.py` check `v8`, pass `--lane str(tree.root)` instead of `str(lane)` when calling `round82_c1_plans_registry.py`, ensuring that the registry checker inspects the extracted tree's files rather than the caller's ambient worktree files.

### 6.5 Risks and Verification
- **Risk:** Permitting archive extraction fallback might allow a dirty git worktree to bypass revision checks.  
  *Mitigation:* The fallback MUST trigger ONLY when `not (lane / ".git").exists()`. When `.git` exists, git revision verification remains strictly mandatory.
- **Verification:**
  1. Archive extraction test:
     ```sh
     TMP=$(mktemp -d)
     git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive HEAD | tar -x -C "$TMP"
     python3 "$TMP/plans/round85_c1_replay.py" --lane "$TMP" --selftest
     python3 "$TMP/plans/round85_c2_debt.py" --lane "$TMP" --check-only v5
     rm -rf "$TMP"
     ```
  2. In-tree verification:
     ```sh
     python3 plans/round85_c1_replay.py --lane . --rev master --work $DIR  # exit 0, mismatches=0
     python3 plans/round85_c2_debt.py --lane . --rev master --work $DIR    # exit 0, checks_passed=8
     python3 plans/round85_c2_debt.py --lane . --sensitivity --work $DIR  # exit 0, failed_at_base=8
     ```

---

## 7. Findings

**Findings count:** `0` (Zero defects found in canonical claims; all frozen requirements satisfied).

---

VERDICT: PASS
