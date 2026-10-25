# R29DraftLesson — round-29 draft lesson and mistake report

Seat: KengakuR28.R29DraftLesson-2 (leaf member, no subagent dispatch). Actual writer: this seat.
Lane root: /home/vgpnk/Projects/shokunin/kengaku-shokunin. Scope: draft only, drafts/lesson-and-mistake.md.
Baseline ed26bdf5d924755697cd6812129be2fa441c42a3; preregistration 31934e5660f1814326c6472eefdfa0c41e642a2f.

## Behavior

Wrote one draft: `.ufo/waves/round-29/drafts/lesson-and-mistake.md` (11066 bytes). It contains:
- a principal (source-versus-derived attribution in a control) tied to r28 M74, M75, M81, with each prior
  fix kept credited to r28 and not re-credited;
- a provisional proposed mistake row, labelled M85 (proposed) with L1 to assign the final id;
- a source-opening record structure, candidate generator anchors, and a list of unopened sources;
- a gate table (admit/defer/reject) with reasons and flip conditions;
- five hand witnesses W1–W5, each with an expected output stated before execution. None were executed.

No production lesson, QUALITY, SOURCES, knowledge, plan, or fixture file was edited. No S-row was written.

## Commands and outputs (observed this seat)

1. `sha256sum plans/fixtures/r29/generate_test_data.py plans/fixtures/r29/profiles.json plans/fixtures/r29/manifest.json`
   - 45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd generator (matches manifest)
   - 90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018 profiles.json (matches manifest)
   - f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87 manifest.json (matches the pinned manifest digest)
   - Note: the manifest's own per-file entry for profiles.json records the same sha256; the manifest itself is pinned by the digest above.
2. `grep -n "" plans/fixtures/r29/generate_test_data.py` — 27 lines; replacements at lines 11–16; `json.loads` at line 20;
   enumerate at line 21; filename at line 22; wildcard import at line 5. Byte size 838, matching the manifest.
3. Python word counts (`len(q.split())`) on candidate quotes: docstring line 1 = 9; line 11 = 4; line 20 = 3;
   line 21 = 5; line 22 = 5; line 5 = 4. These counts are programmatic and are not inferred.
4. Reads of `plans/round-29-claims.md`, `corpus/lessons/round-28.md` (rows M74–M84 and the Gate section),
   `corpus/QUALITY.md` (Q3, Q10, Q13), `corpus/SOURCES.md` (S064–S069), and `plans/fixtures/r29/manifest.json`
   and `profiles.json`.

Not run: any projection, any witness, any test, any build, any linter, any network request, any upstream code import.
Upstream `scripts/generate_test_data.py` was treated only as inert text. Its wildcard import was not executed.

## Sources and locations

- Generator text: `plans/fixtures/r29/generate_test_data.py`, lines 1–27 (local pinned copy). Live URL not re-opened by this seat.
- Round-28 lesson: `corpus/lessons/round-28.md`, mistake table rows M74 (line ~165), M75 (~166), M81 (~172), and Gate section.
- Plan: `plans/round-29-claims.md` (sections on frozen inputs, projection order, and frontier/admission).
- Quality bar: `corpus/QUALITY.md` Q3 (quote containment), Q10 (second-seat re-read), Q13 (second-seat landing).
- Source registry: `corpus/SOURCES.md` S064–S069 (existing rows; no new row written).

## Gate summary

- Lesson principle (control must reproduce source unit): defer.
- M85 proposed mistake row: defer until witness W1 or W2 is observed to fail for the negative-control oracle.
- Reuse of r28 M74/M75 as r29 credit: reject (double credit).
- 812 × 3 benign projection as benchmark behaviour: reject (synthetic profiles; offline scope only).
- index == task_id as output-mapping correctness: reject as general claim; the shuffled witness W4 is the control.
- Novelty-score increase: reject (no distinct construct).
- Writing S070+ before opening sources: reject (procedure).
- Admission this round: defer to L1.

## Unknowns and boundaries

- All §4 witness outputs are predictions, not observations.
- Whether the pinned `test.raw.json` has placeholders in non-URL fields is unobserved ([INFERENCE] from generator text).
- Source-versus-runtime: the generator is source text. Nothing here observes a runtime config, a deployment, or task validity.
- The Python `json` docs and the workflow README/prepare caller were not opened; no row cites them.
- No credentials, env values, cookies, profiles, or private URLs were read or recorded.

## Tooling

No install or update was performed by this seat.

VERDICT: PASS
Scope: draft artifact written and bounded; witnesses proposed, not executed; no admission, no canonical edit, no round-level approval.
