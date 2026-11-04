# Sibling-Overlap Scan & Connector Report — Round 84 (w1)

**Seat:** ConnectorR84  
**Role:** connector (read-only sibling-overlap scan & cross-proposal synthesis)  
**Lane:** kengaku-shokunin  
**Base revision:** `4087b2f8369fb0c317a8460725a607681ff2fd7f`  
**Freeze commit:** `b12a9d46806cb8d69fe48fac0f4efff0b266e4c2`  
**Date:** 2026-11-04  

---

## 1. Search Scope and Methodology

Per the canonical seat assignment, a comprehensive read-only search was conducted across:
1. Sibling lanes: `/home/vgpnk/Projects/shokunin/*-shokunin/corpus` and `/home/vgpnk/Projects/shokunin/*-shokunin/plans` (20 sibling lanes, 31 search roots).
2. Backlog staging: `/home/vgpnk/Projects/shokuknow/merge/kengaku/` (65 knowledge entries, 175 staged rows).
3. In-lane province definitions: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md` and `/home/vgpnk/Projects/shokunin/kengaku-shokunin/PROVINCE.md`.
4. In-lane corpus & plans: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus` and `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans`.

Search terms examined:
- `gcode-to-text`
- `code-from-image`
- `tb2-code-from-image`
- `gcode` (including word boundary check `\bgcode\b`)

---

## 2. Table of Search Hits

### Table 2.1: Sibling Lanes (`*-shokunin` excluding `kengaku-shokunin`)

| Path | Line(s) | Term Matched | What It Asserts / Nature of Hit |
|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/kotodama-shokunin/corpus/lessons/supplement-opencode-1/sources/ottoman.json` | 26–27 | `gcode` (substring) | Glottolog 5.3 reference record 549915 for Ottoman Turkish bibliographic metadata; matches string `lgcode` ("lgcode field" and `lgcode = {Ottoman Turkish = Turkish [tur]}`). Completely unrelated to G-code, CNC, 3D printing, or Terminal-Bench. |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/recheck-r32/S058-difftree.src` | 4486, 5072 | `gcode` (substring) | Scraped HTML documentation for `git-diff-tree`; substring match inside CSS class `<dt class="hdlist1" id="Documentation/git-diff-tree.txt-spanclasssynopsiscode--encodingcodeemltencodinggtemspan">` (`encodingcode`). Unrelated to G-code or Terminal-Bench. |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/recheck-r32/S058.src` | 3453, 3632, 3655, 3734, 4654, 4808, 5513 | `gcode` (substring) | Scraped HTML documentation for `git-rev-list`; substring match inside HTML class names like `-gcodespan` (`-g` flag formatted with `<code>`) and `encodingcode`. Unrelated to G-code or Terminal-Bench. |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/recheck-r33/S058-difftree-r33.src` | 4486, 5072 | `gcode` (substring) | Scraped HTML documentation for `git-diff-tree` recheck; same CSS class substring match. Unrelated to G-code or Terminal-Bench. |

*Exact whole-word search (`\bgcode\b`) across all sibling lanes:* **0 hits**.  
*Search for `gcode-to-text`, `code-from-image`, `tb2-code-from-image` across all sibling lanes:* **0 hits**.  
*Search for `terminal-bench` / `terminal-bench-2` across all sibling lanes:* **0 hits**.

---

### Table 2.2: Staged Knowledge Backlog (`shokuknow/merge/kengaku/`)

| Path | Line(s) | Term Matched | What It Asserts |
|---|---|---|---|
| `/home/vgpnk/Projects/shokuknow/merge/kengaku/*` | — | None | **0 matches** for all four terms. Confirms `plans/round-84-claims.md` §Frontier and wave contract: *“Assimilation: none. `merge/kengaku/` (175 staged rows, 65 knowledge entries) is not drawn on by these frozen claims; it remains unadopted backlog.”* |

---

### Table 2.3: In-Lane Scope & Evidence (`kengaku-shokunin`)

| Path | Line(s) | Term Matched | What It Asserts |
|---|---|---|---|
| `corpus/evidence/round52/graders/SHA256SUMS` | 66, 67 | `gcode-to-text` | SHA256 checksum of captured grader `gcode-to-text/tests/test_outputs.py` (`6b049dc626aa103b20d165552e5cb39ba02c6803b04ba06a43d79435b5f701a6`) and `tests/test.sh` (`4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334`). |
| `corpus/evidence/round52/graders/all_tasks.lst` | 32 | `gcode-to-text` | Roster entry in 89-task population inventory. |
| `corpus/evidence/round52/graders/unexec.lst` | 22 | `gcode-to-text` | Listed among unexecuted population tasks in round 52. |
| `corpus/evidence/round53/pin-tree-2fd12b88.json` | 1595–1635 | `gcode-to-text` | Tree listing of `gcode-to-text` task files at upstream pin `2fd12b88`. |
| `corpus/evidence/round53/tests-index.json` | 1003–1014 | `gcode-to-text` | Indexes captured test functions: `test_hello_file_exists` and `test_hello_file_content`. |
| `corpus/evidence/round53/fetched/C1PriceScoutE-tb2audit-20260120-audit.txt` | 1307–1335 | `gcode-to-text`, `gcode` | Task audit report noting flag format: `flag{gc0d3_iz_ch4LLenGiNg}`. |
| `corpus/evidence/round62/class-survey.txt` | 7 | `gcode-to-text` | Classifies `gcode-to-text` as a member of `file-artifact` class (76 total members). |
| `corpus/evidence/round79/c1-before.txt` | 33 | `gcode-to-text` | Census check identifying `DEFECT MEMBER-UNACCOUNTED gcode-to-text`. |
| `corpus/evidence/round80/gates-clean.txt` | 40 | `gcode-to-text` | Population accounting: `MEMBER gcode-to-text unexecuted classes=file-artifact evidence=unattempted`. |
| `corpus/evidence/round81/c1-after.txt` | 40 | `gcode-to-text` | Population accounting: `MEMBER gcode-to-text unexecuted classes=file-artifact evidence=unattempted`. |
| `corpus/evidence/round83/population-after.txt` | 40 | `gcode-to-text` | Population accounting at round-83 closure: `MEMBER gcode-to-text unexecuted classes=file-artifact evidence=unattempted`. |
| `plans/grader-population-ledger.json` | 343–347 | `gcode-to-text` | BASE state: `{"classes": ["file-artifact"], "evidence": "no-blocker: tests/test_outputs.py sha256=6b049dc626aa103b", "reason": "unattempted", "status": "unexecuted"}`. |
| `plans/grader-population-ledger.json` | 177–183 | `code-from-image` | Admitted round 83 state: `{"classes": ["file-artifact"], "receipt": "corpus/evidence/round83/code-from-image-probe.txt", "round": 83, "status": "executed", "subject": "tb2-header", "verdict": "predicate"}`. |
| `corpus/knowledge/tb2-code-from-image-offline.md` | 1–3 | `code-from-image`, `tb2-code-from-image` | Admitted knowledge entry carrying round-83 admission-bar debt (Q1 missing recheck date/cadence, Q21 missing pin, Q13 missing Gate report citation). |
| `corpus/lessons/round-83.md` | 14 | `code-from-image` | Gate row for S267 admitting grader semantics. |
| `corpus/lessons/round-83-verifier-spotcheck.md` | 74, 93 | `code-from-image`, `tb2-code-from-image` | Outside verification spot-check routing defects R83-V1 (Q13 admission timing) and R83-V2 (Q1/Q21 freshness/recheck pin debt). |
| `corpus/SOURCES.md` | 283 | `code-from-image`, `tb2-code-from-image` | Row S267: Terminal-Bench 2.0 `code-from-image` pinned grader at `2fd12b88`. |
| `corpus/README.md` | 297, 946 | `code-from-image`, `tb2-code-from-image` | Coverage map entry and knowledge index row for `tb2-code-from-image-offline.md`. |
| `PROVINCE.md` | 1134 | `code-from-image`, `tb2-code-from-image` | Scopes `code-from-image` member replay within file-artifact class; explicitly confirms TB2 grader replay is within lane province, while model capability and image solving are refused. |
| `plans/round-84-claims.md` | 9–88 | `gcode-to-text`, `code-from-image`, `tb2-code-from-image` | Frozen claims for round 84: R84-C1 (`gcode-to-text` offline replay) and R84-C2 (`tb2-code-from-image-offline.md` admission debt repair). |

---

## 3. Verdict and Consequence for Claims

**Verdict:** `overlap: none`

### Consequence for Claims:
1. **No Sibling Execution:** No sibling lane executes, replays, cites, or asserts ownership over `gcode-to-text`, `code-from-image`, or any Terminal-Bench 2.0 grader.
2. **Clean Population Increment (R84-C1):** In `kengaku-shokunin`'s BASE state (`4087b2f8369fb0c317a8460725a607681ff2fd7f`), `gcode-to-text` is recorded as `"status": "unexecuted"`, `"reason": "unattempted"`. Replaying its captured grader offline advances the population figures cleanly:
   - Executed members: `27 → 28`
   - Unexecuted members: `61 → 60`
   - File-artifact class executed: `19 of 76 → 20 of 76`
   R84-C1 is undeniably a **new member** for this lane's ledger, without duplication or overlap.
3. **Clean Admission Debt Repair (R84-C2):** The debt in `corpus/knowledge/tb2-code-from-image-offline.md` stems strictly from outside spot-check findings R83-V1 and R83-V2 in `corpus/lessons/round-83-verifier-spotcheck.md`. There is no conflicting external claim or concurrent modification in any sibling lane.

---

## 4. Adjacency Analysis

Any sibling lane material belonging to this lane's province or adjacent to it must be flagged for the adjacency axis rather than absorbed:

1. **Domain & CNC / G-code Semantics (Adjacent / Unowned):**
   - The task `gcode-to-text` contains an input artifact `text.gcode.gz` representing G-code toolpaths (e.g. 3D printer / CNC motion commands: G0, G1, tool positions).
   - What G-code commands actually mean, how a CNC controller or slicer parses them, and reverse-engineering toolpath geometry into text characters belong to CAD/manufacturing or reverse-engineering domains (`kaidoku-shokunin` / domain).
   - Per `kengaku-shokunin/PROVINCE.md`: *“This lane owns what the captured grader checks and what passes it — nothing else.”*
   - The captured grader `test_outputs.py` checks only `/app/out.txt` presence and exact string equality `assert hello_path.read_text().strip() == "flag{gc0d3_iz_ch4LLenGiNg}"`.
   - Any claim about G-code semantics, CNC machine control, or solving the reverse-engineering task from toolpaths is strictly adjacent and out of scope; it must not be absorbed.
2. **Methodological Adjacencies:**
   - **chousa-shokunin:** Citation chain and `SOURCES.md` tier/scope contracts belong to chousa.
   - **tameshi-shokunin:** Reusable mutation testing and fixture generation methodology belong to tameshi.
   - **kumitate-shokunin:** Bubblewrap sandboxing primitives and multi-agent wave orchestration belong to kumitate.
   - **kama-shokunin:** Serving plane and live endpoint identity belong to kama.

---

## 5. Non-Obvious Move & Cross-Proposal Synthesis (UFO-FSD Connector)

### 5.1 Evidence Across Seats
- **Reviewer2R84 (`Reviewer2R84/q13-probe.txt`):** Demonstrated that `plans/gate_timing_check.py` rejects citation paths in `.ufo/waves/round-84/w1/` because `is_second_wave("w1")` evaluates to `False`. The check requires directory `falsify` or `wave2`.
- **AdmitR84 (`AdmitR84/probe-gate-layout.txt`):** Confirmed in isolated fixture tests that:
  - `w1 citation (.md, w1 registry) === exit=1` (fails with `missing: no .ufo/waves/round-84/falsify/ report exists`).
  - `falsify citation + falsify registry === exit=0`.
- **Reviewer2R84 (`Reviewer2R84/attack-run.txt`):** Verified 8/8 frozen cases in bubblewrap (`cases=8 mismatches=0 setup_defects=0`), but showed that exploratory non-UTF8 and directory inputs raise `UnicodeDecodeError` and `IsADirectoryError`, which count as setup defects rather than red witnesses.
- **MutationR84 (`MutationR84/mutants.md`):** Proved that Q1 and Q21 detectors cleanly kill all 7 entry mutants plus the always-true instrument mutant m8, provided BASE sensitivity is enforced.

### 5.2 Affected Axes
- **Calibration (R84-C2):** The Q13 rule requires that the successor admission in `corpus/lessons/round-84.md` `## Gate` cites, by repo-relative path, a second-seat re-read report that passes `plans/gate_timing_check.py` with exit 0.
- **Coverage (R84-C1):** Hermetic bubblewrap replay of `gcode-to-text`.

### 5.3 Contradiction Stated Explicitly
The round contract in `plans/round-84-claims.md` establishes:
> *“Shape: ONE v1 wave, 12 seats, policy `scripts/hyaku/ufo-wave-policy.json` (band 8–16). Attack seats (reviewer ×2, critic, mutation-tester) = 4/12 (≥25 %).”*

And the dispatch placed all 12 seats in `.ufo/waves/round-84/w1/`.  
However, `plans/gate_timing_check.py` lines 241–243 hardcode:
```python
def is_second_wave(directory: str | None) -> bool:
    return bool(directory and (directory.casefold() == "falsify"
                               or re.fullmatch(r"wave[-_ ]?0*2", directory, re.IGNORECASE)))
```
Because `w1` is neither `falsify` nor `wave2`, `gate_timing_check.py` treats `w1` as a first/build wave, finds zero valid second-seat reports, and exits with code 1 (`reasons: no cited, existing, returned second-seat report for this round`).  
If unaddressed at integration, this contradiction between the single-wave dispatch substrate and the historical two-wave directory assumption in `gate_timing_check.py` will spuriously kill R84-C2 on Q13, failing the round's calibration axis.

### 5.4 Proposed Bounded Move
1. **Calibration (R84-C2 / Q13):**  
   The L1 integrator should adapt `plans/gate_timing_check.py`'s `is_second_wave` function to recognize single-wave round layouts (e.g. `w1` or `wave1`) when `swarm-registry.json` specifies allowed second-seat roles (`reviewer`, `critic`, `scout`, `sentinel`, `revenger`) whose declared writer differs from the candidate writer.  
   *Alternative:* If `gate_timing_check.py` is frozen against modification, the admitting commit must provide a `.ufo/waves/round-84/falsify/` directory containing `ReviewerR84.md` and an accompanying `swarm-registry.json`.  
   Furthermore, the Gate row in `corpus/lessons/round-84.md` must cite the 5-component path `.ufo/waves/round-84/w1/ReviewerR84.md` (not a subfolder path like `ReviewerR84/report.txt`, which violates the path-length contract).
2. **Coverage (R84-C1):**  
   Retain the 8 frozen test vectors in `plans/round84-cases.json` without incorporating non-UTF8 or directory cases, ensuring that no setup exceptions (`UnicodeDecodeError`, `IsADirectoryError`) pollute the zero-defect receipt.

### 5.5 Risks and Verification
- **Risk:** Modifying `gate_timing_check.py` could accidentally break the historical exclusion of `build` waves in multi-wave rounds.  
  *Mitigation:* Retain the explicit check that `build` waves remain excluded; run `python3 plans/gate_timing_check.py --selftest` to ensure all 7 built-in test suites pass cleanly.
- **Verification:**  
  1. `python3 plans/gate_timing_check.py --selftest` → exit 0.  
  2. `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-84.md --commit REV` → exit 0.  
  3. `python3 plans/round84_c1_replay.py --lane . --work DIR` → exit 0 (`cases=8 mismatches=0 defects=0`).  
  4. `python3 plans/round84_c2_admission.py --lane . --work DIR` → exit 0 (`entries=1 q1=0 q21=0 q13=0 defects=0`).
