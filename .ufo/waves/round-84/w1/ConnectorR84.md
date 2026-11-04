# Connector Report: Sibling Overlap & Cross-Proposal Synthesis (Round 84)

**writer:** ConnectorR84  
**role:** connector  
**lane:** kengaku-shokunin  
**round:** 84  
**wave:** w1  
**base_commit:** 4087b2f8369fb0c317a8460725a607681ff2fd7f  
**freeze_commit:** b12a9d46806cb8d69fe48fac0f4efff0b266e4c2  

---

## 1. Scoped Task and Executive Summary

Seat `ConnectorR84` performed a read-only sibling-overlap scan across all sibling shokunin lanes, the unadopted backlog in `shokuknow/merge/kengaku/`, and in-lane province documents (`PROVINCE.md`, `corpus/README.md`, population ledgers).

### Verdict
`overlap: none`

### Key Conclusions:
1. **Zero Sibling Collision:** No sibling lane executes, replays, or claims `gcode-to-text`, `code-from-image`, or any Terminal-Bench 2.0 grader. Sibling hits for the string `gcode` are entirely false-positive substring matches in bibliographic records (`lgcode` in `kotodama-shokunin`) and git manpage HTML documentation (`encodingcode` and `-gcodespan` in `mori-shokunin`).
2. **Backlog Unassimilated:** `shokuknow/merge/kengaku/` contains 0 hits for all search terms, confirming that its 65 knowledge entries and 175 staged rows remain unadopted backlog.
3. **New Member for Lane Ledger (R84-C1):** In `kengaku-shokunin`, `gcode-to-text` is recorded in `plans/grader-population-ledger.json` as `unexecuted` (reason: `unattempted`). Replaying its captured grader offline in R84-C1 advances the population ledger (executed 27 → 28, unexecuted 61 → 60, file-artifact class 19/76 → 20/76) with zero sibling duplication.
4. **Adjacency Identified:** G-code toolpaths, CNC G0/G1 parsing, and 3D printer slicing belong to manufacturing/reverse-engineering domains (`kaidoku-shokunin` / domain). Per `PROVINCE.md`, `kengaku-shokunin` owns only what the captured grader checks (`/app/out.txt` exact string). CNC/G-code semantics are strictly adjacent and must not be absorbed.
5. **Cross-Proposal Synthesis (UFO-FSD Move):** Synthesized findings from `Reviewer2R84/q13-probe.txt` and `AdmitR84/probe-gate-layout.txt` against `plans/gate_timing_check.py`. Demonstrated that `gate_timing_check.py` line 241 hardcodes `is_second_wave` to require directory `falsify` or `wave2`, rejecting `w1`. Recommended that the L1 integrator adapt `gate_timing_check.py` for single-wave rounds where `swarm-registry.json` specifies allowed reviewer roles, preventing a spurious Q13 failure on the calibration axis.

---

## 2. Evidence Table: Search Hits

| Path | Line(s) | Term | Category | What It Asserts |
|---|---|---|---|---|
| `kotodama-shokunin/corpus/lessons/supplement-opencode-1/sources/ottoman.json` | 26–27 | `gcode` (in `lgcode`) | Sibling | Bibliographic metadata for Ottoman Turkish in Glottolog 5.3; unrelated to G-code. |
| `mori-shokunin/corpus/evidence/recheck-r32/S058-difftree.src` | 4486, 5072 | `gcode` (in `encodingcode`) | Sibling | HTML git manpage CSS classes; unrelated to G-code. |
| `mori-shokunin/corpus/evidence/recheck-r32/S058.src` | 3453–5513 | `gcode` (in `-gcodespan`, `encodingcode`) | Sibling | HTML git manpage CSS classes; unrelated to G-code. |
| `mori-shokunin/corpus/evidence/recheck-r33/S058-difftree-r33.src` | 4486, 5072 | `gcode` (in `encodingcode`) | Sibling | HTML git manpage CSS classes; unrelated to G-code. |
| `shokuknow/merge/kengaku/*` | — | None | Backlog | 0 matches across 65 knowledge entries and merge reports. |
| `kengaku-shokunin/corpus/evidence/round52/graders/SHA256SUMS` | 66, 67 | `gcode-to-text` | In-lane | Checksum pin of captured grader `test_outputs.py` (`6b049dc626aa103b`). |
| `kengaku-shokunin/corpus/evidence/round62/class-survey.txt` | 7 | `gcode-to-text` | In-lane | Classifies member in `file-artifact` class (76 total members). |
| `kengaku-shokunin/plans/grader-population-ledger.json` | 343–347 | `gcode-to-text` | In-lane | BASE state: `status: unexecuted`, `reason: unattempted`. |
| `kengaku-shokunin/plans/grader-population-ledger.json` | 177–183 | `code-from-image` | In-lane | Round-83 state: `status: executed`, `receipt: corpus/evidence/round83/code-from-image-probe.txt`. |
| `kengaku-shokunin/corpus/knowledge/tb2-code-from-image-offline.md` | 1–3 | `code-from-image` | In-lane | Round-83 knowledge entry carrying Q1/Q21/Q13 admission debt. |
| `kengaku-shokunin/corpus/lessons/round-83-verifier-spotcheck.md` | 74, 93 | `code-from-image` | In-lane | Outside verifier spot-check routing defects R83-V1 and R83-V2. |
| `kengaku-shokunin/PROVINCE.md` | 1134 | `code-from-image` | In-lane | Defines offline replay scope for file-artifact class members. |
| `kengaku-shokunin/corpus/README.md` | 297, 946 | `code-from-image` | In-lane | Indexes `code-from-image` member replay and knowledge entry. |
| `kengaku-shokunin/plans/round-84-claims.md` | 9–88 | `gcode-to-text`, `code-from-image` | In-lane | Frozen claims for round 84 (R84-C1 replay and R84-C2 debt repair). |

---

## 3. Adjacency Boundary

- **Toolpath & G-code Semantics (Adjacent / Unowned):** Parsing G-code commands (G0, G1, tool coordinates, feedrates) and converting toolpaths to visual or textual representations belongs to CAD/manufacturing or reverse-engineering domains.
- **kengaku-shokunin Boundary:** This lane evaluates only the captured grader assertions (`/app/out.txt` presence and `flag{gc0d3_iz_ch4LLenGiNg}` string match). G-code toolpath interpretation, 3D printing simulation, and model capability are refused and flagged for the adjacency axis.

---

## 4. UFO-FSD Connector Move: Resolving Single-Wave Verification Contradiction

### 4.1 Diagnosis
- In `plans/round-84-claims.md`, round 84 is defined as `ONE v1 wave, 12 seats` (all dispatched into `.ufo/waves/round-84/w1/`).
- In `plans/gate_timing_check.py:241-243`, `is_second_wave()` checks:
  `directory.casefold() == "falsify" or re.fullmatch(r"wave[-_ ]?0*2", directory, re.IGNORECASE)`
- As proven by `Reviewer2R84/q13-probe.txt` and `AdmitR84/probe-gate-layout.txt`, `gate_timing_check.py` rejects any report in `w1/` with exit code 1 (`reasons: no cited, existing, returned second-seat report for this round`).
- If unaddressed, this causes R84-C2 Q13 to fail spuriously, triggering the round's kill rule.

### 4.2 Move
1. **L1 Integrator Action:** Enable single-wave round recognition in `plans/gate_timing_check.py` for directories matching `w1` / `wave1`, looking up member roles in `swarm-registry.json` to verify that the seat role is in `ALLOWED_REPORT_ROLES` (`reviewer`, `critic`, `scout`, `sentinel`, `revenger`) and that writer != candidate writer.
2. **Gate Citation Format:** The Gate row in `corpus/lessons/round-84.md` must cite `.ufo/waves/round-84/w1/ReviewerR84.md` (exact 5-component path).
3. **Verification:**
   - `python3 plans/gate_timing_check.py --selftest` → exit 0.
   - `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-84.md --commit REV` → exit 0.
   - `python3 plans/round84_c2_admission.py --lane . --work $S` → exit 0 (`defects=0`).

VERDICT: PASS
