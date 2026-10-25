# R35ConnDefectClasses — Cross-Round Defect Taxonomy, Recurrence Mapping, and Ledger Synthesis

**Seat:** `R35ConnDefectClasses` (connector)  
**Round:** kengaku round 35 (hyaku run 7, 2026-10-25), Wave 1 of 2  
**Assigned Axes:** calibration, adjacency  
**Target Path:** `.ufo/waves/round-35/build/R35ConnDefectClasses.md`  
**Reference Head:** `11d64530179b78e33ba6074fc77d63d36ee7ac31` (frozen lane tip)

---

## 1. Executive Summary

This study maps every routed defect identified in the non-author verifier spot-checks across rounds 29 through 34 (`corpus/lessons/round-{29,30,31,32,33,34}-verifier-spotcheck.md`) into a structured defect taxonomy. Across the 35 routed defect instances, we identify **17 distinct defect classes**, of which **8 classes recur across multiple rounds** (and **9 classes** have $\ge 2$ total occurrences).

A critical structural pathology is revealed: **Every single recurring defect class currently lacks a standing invariant check.** In previous rounds (rounds 30–34), the lane repeatedly attempted to close defects by authoring narrow, backward-looking checks (e.g. `round33_defects.py` checking `.ufo/waves/round-32/`, or `defect_ledger.py` checking `.ufo/waves/round-34/`). Because these checks only inspect past-round directories, the current round inevitably re-introduces the identical defect class (demonstrated by `untracked work` recurring in rounds 29, 30, 32, and 34).

We propose a non-obvious connector move synthesizing `considerthese/2026-10-25.md` Proposal 2(b) and 2(c) into `plans/defect_ledger.py`: **Defects with recorded recurrences (`recurrence_of != null`) must enforce standing repo-wide invariants rather than historical path-bound predicates.**

---

## 2. Complete Cross-Round Defect Mapping (Rounds 29–34)

The table below catalogs all 35 routed defects from the non-author spot-checks, citing exact file and line locators and mapping each to its canonical defect class.

| Round | Defect ID | Source Location | Defect Description | Canonical Class | Cross-Round Status |
|:---|:---|:---|:---|:---|:---|
| **R29** | R29-D1 | `corpus/lessons/round-29-verifier-spotcheck.md:120` | Report cited `control-nothing.txt` twice; committed path was `control.nothing.txt` with different field count | `receipt/manifest mismatch` | Recurring (R29, R31, R34) |
| **R29** | R29-D2 | `corpus/lessons/round-29-verifier-spotcheck.md:125` | Lesson rendered kappa sweep as "0 hits in the lane" whereas command measured `corpus/knowledge/*.md` | `lesson misstatement` | Recurring (R29, R30, R31, R32) |
| **R29** | R29-D3 | `corpus/lessons/round-29-verifier-spotcheck.md:128` | Lesson priced S078 line-75 quote at 9 words; registry and capture show 8 words | `lesson misstatement` | Recurring (R29, R30, R31, R32) |
| **R29** | R29-D4 | `corpus/lessons/round-29-verifier-spotcheck.md:130` | `M .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md` (+22 lines) uncommitted in worktree | `untracked work` | Recurring (R29, R30, R32, R34) |
| **R29** | R29-D5 | `corpus/lessons/round-29-verifier-spotcheck.md:133` | S091 has `used-by` entry in `SOURCES.md`, but entry's `source:` block does not cite it | `citation asymmetry` | Single round (R29) |
| **R30** | R30-item1 | `corpus/lessons/round-30-verifier-spotcheck.md:163` | `LOG.md:792-793` declares delta as "two new fields, one new value set", retracted by entry | `log misstatement` | Single round (R30) |
| **R30** | R30-item2 | `corpus/lessons/round-30-verifier-spotcheck.md:168` | Lesson states Q6 pass on "one field, one placement, one value set", which entry retracted | `lesson misstatement` | Recurring (R29, R30, R31, R32) |
| **R30** | R30-item3 | `corpus/lessons/round-30-verifier-spotcheck.md:171` | Lesson lists Q2 tier set as `S085 B, S086 A`; registry shows `S086 B` | `lesson misstatement` | Recurring (R29, R30, R31, R32) |
| **R30** | R30-item4 | `corpus/lessons/round-30-verifier-spotcheck.md:174` | `contamination-transparency-card.md:125` repeats "the card records what each stated, not a reconciled truth" | `entry content defect` | Multi-instance (R30; count=2) |
| **R30** | R30-item5 | `corpus/lessons/round-30-verifier-spotcheck.md:177` | Entry overclaims S2 tri-state flag as only new field; misnames CC BY 4.0 as CC0 | `entry content defect` | Multi-instance (R30; count=2) |
| **R30** | R30-item6 | `corpus/lessons/round-30-verifier-spotcheck.md:184` | Uncommitted round work: 5 wave seat reports modified in worktree (active writer past closure) | `untracked work` | Recurring (R29, R30, R32, R34) |
| **R30** | R30-item7 | `corpus/lessons/round-30-verifier-spotcheck.md:190` | Report commit `c5807fe7` preceded lane's final 3 commits; cited tip `caf1e2b4` stale | `report-before-commit` | Recurring (R30, R31, R32) |
| **R30** | R30-item8 | `corpus/lessons/round-30-verifier-spotcheck.md:194` | Lesson states 34 falsify seats; registries and report show 33 seats | `seat-ledger mismatch` | Recurring (R30, R31, R32, R33) |
| **R31** | R31-D1 | `corpus/lessons/round-31-verifier-spotcheck.md:149` | Report addendum cited `a44b5a8`-class commits; hash absent from git (real fix was `ae95fe0`) | `phantom hash` | Recurring (R31, R32) |
| **R31** | R31-D2 | `corpus/lessons/round-31-verifier-spotcheck.md:151` | Report ordering recurred: final lane commits `ae95fe0` and `87f0d32` never cited by report | `report-before-commit` | Recurring (R30, R31, R32) |
| **R31** | R31-D3 | `corpus/lessons/round-31-verifier-spotcheck.md:154` | `gate-cli-exits.txt` path `../../../plans/sources_adopt.py` fails (`exit=2` on all lines) | `receipt/manifest mismatch` | Recurring (R29, R31, R34) |
| **R31** | R31-D4 | `corpus/lessons/round-31-verifier-spotcheck.md:159` | `plans/sources_adopt.py` has no row in `SKILL.md` §Gate/probe registry | `missing gate registry` | Single round (R31) |
| **R31** | R31-D5 | `corpus/lessons/round-31-verifier-spotcheck.md:162` | Falsify registry lists 36 seats; 35 reports committed (`R31FxEntryBar` missing; report said 0 dead) | `seat-ledger mismatch` | Recurring (R30, R31, R32, R33) |
| **R31** | R31-D6 | `corpus/lessons/round-31-verifier-spotcheck.md:165` | Stale locators: lesson cites `verifier_mode.py` at `:35-38` (vs `:39-40`); Q6 retraction at `:78-81` (vs `:72/82-83`) | `stale locator` | Recurring (R31, R32) |
| **R31** | R31-debt | `corpus/lessons/round-31-verifier-spotcheck.md:168` | Carried debt: round-30 lesson `:66` claims S083/S086 were "peer-reviewed" | `lesson misstatement` | Recurring (R29, R30, R31, R32) |
| **R32** | R32-R1 | `corpus/lessons/round-32-verifier-spotcheck.md:87` | Carried phantom hash `a44b5a8` erratum unrepaired in C2 receipts | `phantom hash` | Recurring (R31, R32) |
| **R32** | R32-R2 | `corpus/lessons/round-32-verifier-spotcheck.md:87` | Report ordering unrepaired: report failed to cite final closure tip `112091c` | `report-before-commit` | Recurring (R30, R31, R32) |
| **R32** | R32-R5 | `corpus/lessons/round-32-verifier-spotcheck.md:87` | Seat ledger unrepaired: missing falsify seat report `R31FxEntryBar` | `seat-ledger mismatch` | Recurring (R30, R31, R32, R33) |
| **R32** | R32-R6 | `corpus/lessons/round-32-verifier-spotcheck.md:87` | Lesson errata / locator drift unrepaired across round-30 and round-31 lessons | `stale locator` | Recurring (R31, R32) |
| **R32** | R32-R7 | `corpus/lessons/round-32-verifier-spotcheck.md:87` | Counter blind spots and S086 peer-review debt remaining red | `lesson misstatement` | Recurring (R29, R30, R31, R32) |
| **R32** | R32-C1 | `corpus/lessons/round-32-verifier-spotcheck.md:88` | Staged source IDs S094/S097 collided with live registry IDs S094/S097 | `source collision` | Single round (R32) |
| **R32** | R32-C3 | `corpus/lessons/round-32-verifier-spotcheck.md:89` | Raw API payloads not retained in git (model catalogs probe saved only to `/tmp`) | `unretained raw payload` | Single round (R32) |
| **R32** | R32-untracked | `corpus/lessons/round-32-verifier-spotcheck.md:90` | Ten wave paths remain untracked at lane tip despite `ahead=0` | `untracked work` | Recurring (R29, R30, R32, R34) |
| **R32** | R32-scorecard | `corpus/lessons/round-32-verifier-spotcheck.md:26` | SCORECARD omitted `## Round 32` section entirely (addressed as R33-N2) | `scorecard misstatement` | Recurring (R32, R34) |
| **R33** | R33-note-a | `corpus/lessons/round-33-verifier-spotcheck.md:100` | Header says "36 + 36 seats" while registries show 36 build + 53 falsify = 89 total | `seat-ledger mismatch` | Recurring (R30, R31, R32, R33) |
| **R33** | R33-note-b | `corpus/lessons/round-33-verifier-spotcheck.md:100` | Frozen claims prose says `entries=0`, but committed control printed `entries=1` | `claims/control mismatch` | Single round (R33) |
| **R34** | R34-D1 | `corpus/lessons/round-34-verifier-spotcheck.md:75` | 1423 untracked paths (incl. `plans/round34_c1_verify.py`, `plans/round34_defects.py`, wave scratch) | `untracked work` | Recurring (R29, R30, R32, R34) |
| **R34-D2** | R34-D2 | `corpus/lessons/round-34-verifier-spotcheck.md:76` | Committed scratch bloat: `.ufo/waves/round-34/mut-entries-scratch/` (106,323 blobs, 1650.6 MiB logical) | `scratch bloat` | Single round (R34) |
| **R34-D3** | R34-D3 | `corpus/lessons/round-34-verifier-spotcheck.md:77` | `tb2-eval/SHA256SUMS` omitted `test_outputs.py`/`test.sh`, contradicting seat report | `receipt/manifest mismatch` | Recurring (R29, R31, R34) |
| **R34-D4** | R34-D4 | `corpus/lessons/round-34-verifier-spotcheck.md:78` | SCORECARD round-34 C2 row misattributed red selftest to counter draft instead of mutation harness | `scorecard misstatement` | Recurring (R32, R34) |
| **R34-D5** | R34-D5 | `corpus/lessons/round-34-verifier-spotcheck.md:79` | S091 refused as "quote absent; 418 Access Denied" though reopen capture held quote verbatim | `false refusal` | Single round (R34) |

---

## 3. Taxonomy Summary & Recurrence Distribution

### A. Frequency by Class

Across all 35 defect instances, we identify **17 distinct classes**:

1. **`lesson misstatement`**: 6 occurrences (R29, R30, R31, R32) — **RECURRING**
2. **`untracked work`**: 4 occurrences (R29, R30, R32, R34) — **RECURRING**
3. **`seat-ledger mismatch`**: 4 occurrences (R30, R31, R32, R33) — **RECURRING**
4. **`receipt/manifest mismatch`**: 3 occurrences (R29, R31, R34) — **RECURRING**
5. **`report-before-commit`**: 3 occurrences (R30, R31, R32) — **RECURRING**
6. **`scorecard misstatement`**: 2 occurrences (R32, R34) — **RECURRING**
7. **`phantom hash`**: 2 occurrences (R31, R32) — **RECURRING**
8. **`stale locator`**: 2 occurrences (R31, R32) — **RECURRING**
9. **`entry content defect`**: 2 occurrences (R30) — **RECURRING ($\ge 2$ instances)**
10. **`citation asymmetry`**: 1 occurrence (R29)
11. **`log misstatement`**: 1 occurrence (R30)
12. **`missing gate registry`**: 1 occurrence (R31)
13. **`source collision`**: 1 occurrence (R32)
14. **`unretained raw payload`**: 1 occurrence (R32)
15. **`claims/control mismatch`**: 1 occurrence (R33)
16. **`scratch bloat`**: 1 occurrence (R34)
17. **`false refusal`**: 1 occurrence (R34)

### B. Cross-Round Recurrence Count

- **Total Classes Identified:** **17**
- **Classes Recurring Across Multiple Rounds:** **8** (`lesson misstatement`, `untracked work`, `seat-ledger mismatch`, `receipt/manifest mismatch`, `report-before-commit`, `scorecard misstatement`, `phantom hash`, `stale locator`).
- If single-round multi-instance defects (`entry content defect`, count=2 in round 30) are included by the criterion count $\ge 2$: **9 recurring classes**.
- When mapped strictly against the **7 classes explicitly named in the assignment prompt** (`untracked work`, `receipt/manifest mismatch`, `scorecard misstatement`, `false refusal`, `scratch bloat`, `phantom hash`, `report-before-commit`):
  - **5 classes recur** across rounds (`untracked work`, `receipt/manifest mismatch`, `scorecard misstatement`, `phantom hash`, `report-before-commit`).
  - **2 classes are novel** in round 34 (`scratch bloat`, `false refusal`).

---

## 4. Analysis of Round-34 D1–D5 & Proposed `recurrence_of` Values

We evaluate each row in `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/defects.jsonl`:

### D1 (`R34-D1`): `uncommitted-round-work`
- **Is it a recurrence?** **YES.**
- **History:** Recurs from Round 29 D4 (`R29a2CritEntry.md` uncommitted worktree modification), Round 30 item 6 (5 uncommitted wave reports, checked by R31 `check_r9`), and Round 32 untracked wave paths (10 files at pushed tip, checked by R33 `check_n1` `round32-wave-tree-committed`).
- **Proposed `recurrence_of`:**  
  `"R33-N1 (round-32 wave paths untracked at tip; plans/round-33-claims.md:87)"`  
  *(Currently populated in `corpus/defects.jsonl:1`; confirmed accurate).*

### D2 (`R34-D2`): `committed-scratch-bloat`
- **Is it a recurrence?** **NO.**
- **History:** No previous round committed recursive self-mirrors of the repository (106,323 blobs / 1.65 GiB). This was a novel failure mode introduced by executing mutation testing inside the tracked repository tree instead of an isolated `/tmp` clone.
- **Proposed `recurrence_of`:** `null`

### D3 (`R34-D3`): `receipt-claims-unbacked-manifest`
- **Is it a recurrence?** **YES (at class level); NO (at strict sub-class level).**
- **History:** At the general `receipt/manifest mismatch` class level, this recurs from Round 29 D1 (report cited `control-nothing.txt` but committed path was `control.nothing.txt`) and Round 31 D3 (`gate-cli-exits.txt` had relative path resolving to nonexistent `.ufo/plans`). Under narrow sub-classification (evaluator manifest file omission vs receipt execution failure), it is novel.
- **Proposed `recurrence_of`:**
  - *Class-level recurrence:* `"R31-D3 (broken CLI receipt path at tip; corpus/lessons/round-31-verifier-spotcheck.md:154)"`
  - *Strict sub-class:* `null`
  - *Recommendation:* Keep `null` if distinguishing manifest omission from receipt path errors, or populate `R31-D3` if tracking the general evidence integrity class.

### D4 (`R34-D4`): `scorecard-misattribution`
- **Is it a recurrence?** **YES (at class level); NO (at strict sub-class level).**
- **History:** In Round 32, `SCORECARD.md` omitted the `## Round 32` section completely (closed in Round 33 as N2 `scorecard-round32-section`). Both are recording defects on the `SCORECARD.md` surface; N2 was an omission, whereas D4 is an attribution error.
- **Proposed `recurrence_of`:**
  - *Class-level recurrence:* `"R33-N2 (missing ## Round 32 section in SCORECARD.md; plans/round-33-claims.md:89)"`
  - *Strict sub-class:* `null`
  - *Recommendation:* Keep `null` if distinguishing misattribution from section omission, or populate `R33-N2` if tracking SCORECARD record defects.

### D5 (`R34-D5`): `false-refusal-reason`
- **Is it a recurrence?** **NO.**
- **History:** In rounds 29–33, all candidate rejections sampled by the verifier were confirmed factually correct. Round 34 was the first instance where the non-author verifier disagreed with the rejection reason (S091 quote was present verbatim in the lane's own reopen capture).
- **Proposed `recurrence_of`:** `null`

### Proposed `corpus/defects.jsonl` Rows (Class-Level Recurrence Representation)

```jsonl
{"id": "R34-D1", "class": "uncommitted-round-work", "opened_round": 34, "source": "corpus/lessons/round-34-verifier-spotcheck.md:75", "check": "r34_d1", "status": "open", "closed_round": null, "recurrence_of": "R33-N1 (round-32 wave paths untracked at tip; plans/round-33-claims.md:87)"}
{"id": "R34-D2", "class": "committed-scratch-bloat", "opened_round": 34, "source": "corpus/lessons/round-34-verifier-spotcheck.md:76", "check": "r34_d2", "status": "open", "closed_round": null, "recurrence_of": null}
{"id": "R34-D3", "class": "receipt-claims-unbacked-manifest", "opened_round": 34, "source": "corpus/lessons/round-34-verifier-spotcheck.md:77", "check": "r34_d3", "status": "open", "closed_round": null, "recurrence_of": "R31-D3 (broken CLI receipt path at tip; corpus/lessons/round-31-verifier-spotcheck.md:154)"}
{"id": "R34-D4", "class": "scorecard-misattribution", "opened_round": 34, "source": "corpus/lessons/round-34-verifier-spotcheck.md:78", "check": "r34_d4", "status": "open", "closed_round": null, "recurrence_of": "R33-N2 (missing ## Round 32 section in SCORECARD.md; plans/round-33-claims.md:89)"}
{"id": "R34-D5", "class": "false-refusal-reason", "opened_round": 34, "source": "corpus/lessons/round-34-verifier-spotcheck.md:79", "check": "r34_d5", "status": "open", "closed_round": null, "recurrence_of": null}
```

---

## 5. Classes That Recur $\ge 2$ Times With No Standing Check

Every recurring class identified has recurred because the lane's verification posture relied on **temporary, past-round checks** rather than **standing invariant checks**:

1. **`untracked work` (4 rounds: R29, R30, R32, R34)**
   - *Failure mechanism:* `round31_defects.py` only checked the 5 seat reports from round 30. `round33_defects.py` only checked `.ufo/waves/round-32/`. Current `defect_ledger.py` (`r34_d1`) only checks `.ufo/waves/round-34/`.
   - *Standing check status:* **NO STANDING CHECK.** Nothing enforces clean `git status --porcelain` across the current working tree or active wave directories at closure.

2. **`receipt/manifest mismatch` (3 rounds: R29, R31, R34)**
   - *Failure mechanism:* `round30_defects.py` checked one round-29 file. `round32_defects.py` checked one round-31 file. Current `defect_ledger.py` (`r34_d3`) checks only `tb2-eval/SHA256SUMS`.
   - *Standing check status:* **NO STANDING CHECK.** Proposal 2(c) from `considerthese/2026-10-25.md` (a general tip-receipt validator over all `corpus/evidence/**`) remains completely unbuilt (`QUALITY.md:290-293`).

3. **`report-before-commit` (3 rounds: R30, R31, R32)**
   - *Failure mechanism:* Reports in R30, R31, and R32 were repeatedly committed before final revisions landed in the lane branch, causing stale cited tips.
   - *Standing check status:* **NO STANDING CHECK.** No pre-report gate checks that the cited tip hash matches `git rev-parse HEAD` of the lane.

4. **`seat-ledger mismatch` (4 rounds: R30, R31, R32, R33)**
   - *Failure mechanism:* Lesson seat summaries consistently disagree with `swarm-registry.json` or omit seats (e.g. R31 missing `R31FxEntryBar`, R33 header "36+36" vs 36+53=89).
   - *Standing check status:* **NO STANDING CHECK.** No automated verification reconciles lesson seat tables against `swarm-registry.json` before landing.

5. **`scorecard misstatement` (2 rounds: R32, R34)**
   - *Failure mechanism:* Section omission in R32; red selftest misattribution in R34.
   - *Standing check status:* **NO STANDING CHECK.** No checker validates SCORECARD attribution statements against committed test receipts.

6. **`stale locator` (2 rounds: R31, R32)**
   - *Failure mechanism:* Subsequent text edits shift line locators (e.g. `:35-38` moved to `:39-40`, `:78-81` moved to `:72/82-83`).
   - *Standing check status:* **NO STANDING CHECK.** Locators are written as static line numbers with no anchor-validation tool.

7. **`lesson misstatement` (4 rounds: R29, R30, R31, R32)**
   - *Failure mechanism:* Lesson prose quotes overbroad scopes, incorrect word counts, or unverified claims.
   - *Standing check status:* **NO STANDING CHECK.** Lesson text is entirely unverified by automated gates.

---

## 6. Connector Synthesis: The Non-Obvious Move

### A. Evidence & The Core Contradiction

`corpus/QUALITY.md` Q23 (`QUALITY.md:275-295`) articulates the lane's standard:
> *"A defect closed in prose and checked by a one-round counter ... is checked once and then forgotten: round 34's D1 recurs round 33's N1 ... and nothing re-ran N1's check after round 33 closed it."*

Yet `plans/defect_ledger.py` embodies the **exact same failure**:
- Function `r34_d1(lane)` (`defect_ledger.py:37-44`) checks:
  ```python
  R34 = ".ufo/waves/round-34/"
  left = [p for p in out.splitlines() if p.startswith(R34) or (p.startswith("plans/round34_") ...)]
  ```
- This check is completely blind to `.ufo/waves/round-35/` and the active working tree. If round 35 leaves 1,000 untracked files in `.ufo/waves/round-35/`, `r34_d1` will report `agree=yes untracked=0` and pass!
- Furthermore, `recurrence_of` is recorded in `corpus/defects.jsonl` but completely ignored by `defect_ledger.py:120-137`.

### B. Affected Axes

- **Calibration:** **IMPROVED.** Eliminates the recurring illusion of defect closure. Prevents the lane from certifying calibration on past-round artifacts while actively violating the same invariant in the current round.
- **Operability:** **IMPROVED.** Replaces round-by-round manual checker authoring with standing invariant validators, realizing Proposal 2 from `considerthese/2026-10-25.md`.
- **Adjacency:** **UNHARMED.** The defect ledger is strictly internal to `kengaku-shokunin`; no sibling-lane files or fleet interfaces are modified.
- **Coverage, Novelty, Depth, Freshness:** **UNHARMED.** Verified orthogonal.

### C. Proposed Move

Synthesize `considerthese/2026-10-25.md` Proposal 2(b) and 2(c) into the contract for `corpus/defects.jsonl` and `plans/defect_ledger.py`:

1. **The Invariant Rule for Recurring Defect Classes:**  
   When a row in `corpus/defects.jsonl` specifies `recurrence_of != null`, its associated check function in `plans/defect_ledger.py` **MUST NOT be path-bound to a historical round directory**. Instead, it must enforce a **standing invariant**:
   - For `uncommitted-round-work` (D1): The check must verify that `git status --porcelain` is clean across all wave directories (`.ufo/waves/round-*/`) and plan files, ensuring no untracked round work exists at the tip.
   - For `receipt/manifest mismatch` (D3): The check must verify all `SHA256SUMS` manifests in `corpus/evidence/**` against their directory files, catching manifest omissions systematically.

2. **Schema Enforcement of Proposal 2(b):**  
   Add an invariant assertion in `defect_ledger.py`:
   - A defect row with `recurrence_of != null` whose check function only tests historical directories fails verification with `DEFECT: recurring class requires standing invariant check`.

### D. Risks and Tradeoffs

- **Risk 1 (Mid-flight working tree noise):** A naive global `git status --porcelain` check will fail while subagents are actively writing wave scratch files during a round.
  - *Mitigation:* The standing invariant check should be run in two modes: (a) against committed HEAD (`git ls-tree` / `git status` on a clean checkout) during automated verification, and (b) against all non-active wave directories (`round-NN < current_round`).
- **Risk 2 (Scope creep in C2):** Mutating `defect_ledger.py`'s check behavior mid-round could conflict with the frozen predicate in `plans/round-35-claims.md:47-51`.
  - *Mitigation:* The frozen predicate for round 35 tests `r34_d1..r34_d5` on the round-34 repairs. The generalized invariant check is proposed as a clean wave-2 / round-36 hardening step, leaving the frozen wave-1 C2 predicate intact.

### E. Verification Procedure

The proposed standing invariant checks can be verified using the fixture clone discipline:

```bash
D=$(mktemp -d /tmp/k35-conn-XXXX)
git clone -q --no-checkout --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone /corpus/ /plans/
git -C "$D/lane" checkout -q master

# Verify that standing untracked-work check catches an untracked file in the ACTIVE wave
touch "$D/lane/.ufo/waves/round-35/scratch.txt"
# A standing check fails: untracked=1
# A historical check (r34_d1) passes falsely: untracked=0

rm -rf "$D"
```

---

VERDICT: classes-17-recurring-8
