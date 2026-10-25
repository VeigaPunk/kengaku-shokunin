# FFreezeBytes — Q10 byte-binding process attack on the round-28 candidate

writer: FFreezeBytes (seat; registry agentId `KengakuR28.FFreezeBytes`, role `critic`, wave `falsify`)
Canonical candidate: `corpus/knowledge/webarena-task-spec-audit.md` (NOT admitted; absent from commit `18b19226` and from the working tree).
Frozen draft read: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, sha256
`77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8`, git blob `ccbae5acda570650b46e43057a2a6c543a3ffc30`, 146 lines / 12405 bytes.
The candidate's frontmatter writer field is `KengakuR28`, which is distinct from this seat.
Scope: author-side process critique of how reviewed bytes are bound to admitted bytes. This is **not** a Q10 complete
source/number re-read. L1 MUST NOT cite this report as Q10 support. Its role (`critic`), candidate-path mention and
anchored VERDICT would make `gate_timing_check.py` count it structurally (see finding 2).
Inputs: `plans/round-28-claims.md` (sha256 `d406d222…`, incl. Amendment 1 §2/§6), `corpus/lessons/round-28.md` (sha256
`19ccfe2c…`), `.ufo/waves/round-28/candidate-freeze.json`, `build-dead-seats.json`, `build-outcomes.json`,
`build/` and `falsify/swarm-registry.json`, `falsify-spec.json`, `plans/gate_timing_check.py` (sha256 `51c18a9e…`, unchanged
from commit), `corpus/QUALITY.md:75-144`, `corpus/README.md:258,310-324`, `build/CritGateTiming.md`.
Commands: read-only `sha256sum`, `git show/ls-tree/rev-parse/hash-object/log`, `rg`, and stdlib JSON census. One scratch probe,
`scratch/FFreezeBytes/probe_gate.py`, imports `gate_timing_check` and calls `audit_admission` on in-memory fixtures. It uses no Git,
runs with bytecode disabled, and its output is in `probe_gate.out`. Neither the checker CLI nor its selftest was run, and no
build/test was run. No external source was opened. Installs: none.

## What holds (verified)

| check | observed |
|---|---|
| frozen draft digest = assigned digest | working tree `77e19d5b…` = `git show 18b19226:<draft>` `77e19d5b…` = `candidate-freeze.json` `candidate_sha256` |
| freeze record itself is committed | `candidate-freeze.json` worktree = commit `bf5990dc…`; landed only in `18b19226` |
| instrument pins in freeze = commit = worktree | `benchmark_spec_audit.py` `f72a8569…`, `registry_check.py` `41561dfb…`, `state_check.py` `5db1eb78…` |
| C1 inputs transitively pinned | instrument hardcodes `MANIFEST_SHA256` `c78b1478…` and `SELECTION_SHA256` `5f7eea2e…` (lines 15–16, checked at 184–193). On-disk `manifest.json` and `selected-task-ids.json` hash to exactly these. The freeze → instrument → manifest → snapshot chain is closed |
| writer identity is the actual author | draft writer field `KengakuR28`; Amendment 1 §2 and lesson M69 state that both scribes (`DraftKnowledge-2`, `DraftMistake-2`) and all 3 executors died (429/capacity, `build-dead-seats.json`) and were not replaced. No build file exists for any dead seat name |
| no dead/placeholder build support | all 29 build reports named by the draft or lesson exist, are committed and nonempty, and belong to registered live seats (scout/reviewer/critic/connector). None is a dead seat |
| no premature admission | lesson Gate row is `deferred`. `corpus/README.md:323` states the candidate remains a draft. The Frontier line `README.md:258` is not discharged. The canonical path is absent at the commit and in the worktree. `falsify/` currently holds only `swarm-registry.json` (0 returned reports), so any admit now would cite unreturned seats |
| falsify registry identity | 64 members. No seat stem or agentId equals `KengakuR28`. The 2 assigned Q10 seats, `FFullEntry` and `FContractEntry`, are role `reviewer` (allowed). `FConnector`, `FMutMissing`, `FMutPin`, `FMutSchema` and `FMutStatus` have disallowed roles and can never be Q10 support |
| build-wave CritGateTiming fixes adopted | correction 1: numbers measured before the freeze. Correction 3: the Q10 prompts require the sha256 of the exact bytes plus an S061/S062/S063 table. Correction 4: the writer field names the final-byte author. **Correction 2, the digest comparison against the admitting commit, is still prose only** (Amendment 1 §6) |

## Counterexamples (strongest first)

1. **Byte binding exists only as an L1 obligation, not as any mechanism. Observed, not inferred.** The probe ran
   `audit_admission` with the real draft as the committed canonical blob and a `reviewer` falsify report:
   - **C:** the report records a digest of 64 zeros, not `77e19d5b…`. Result: `ok=True`.
   - **D:** the admitted blob is mutated after review (`812 /812` → `813 /813`, sha256 `4d615d75…`) while the report still cites
     `77e19d5b…`. Result: `ok=True`.

   Q13–Q16 are structural, as QUALITY says ("Presence is not endorsement"). Exit 0 therefore says nothing about Q10 byte
   identity. CritGateTiming inferred this from code; this run observes it.
2. **A returned FAIL/PARTIAL verdict counts as structural support.** Probe B: report `VERDICT: FAIL` gives `ok=True`, because
   `VERDICT_RE` accepts any token (`:56`, `:360`). "Returned" ≠ "passed". L1 must read the final verdict of each cited report.
   This report (PARTIAL, critic, candidate path named) would itself pass structurally if cited.
3. **Returned report bytes are not pinned at return.** The integrator (L1, the candidate writer) commits the falsify reports.
   No receipt records a report's sha256 at return time: `falsify-registry-record.txt` holds only registry state, and round 27
   followed the same pattern (`6356b0b` admitted with 47 falsify paths and no report digests). Nothing distinguishes the report
   bytes a seat returned from the report bytes that land. This is a hidden-provenance gap of the same shape as finding 1, one
   level up.
4. **Fail-closed traps that would block a genuine admit.** None of these is unsafe, but each would lead to a "fix the checker"
   temptation, which is out of bounds:
   - **E:** a Q10 report that quotes the draft frontmatter with `writer: KengakuR28` at line start is rejected as "report
     writer/author declaration equals candidate writer" (`REPORT_AUTHOR_RE`, `:57`, `:356`). Reviewers recording the
     frontmatter verbatim would self-invalidate.
   - **F:** the current Gate candidate cell is `knowledge/webarena-task-spec-audit.md draft`. Flipping only the decision to
     `admit` gives "admitted candidate is absent from the commit tree".
   - **G:** a report naming only the `.ufo/.../drafts/` path, not `knowledge/webarena-task-spec-audit.md`, gives "report does
     not name the admitted candidate path".
   - **H:** a reason cell containing "second seats" is generic and red. The current deferred cell's hyphenated
     "second-seat" does not match.
5. **Thin support base.** Exactly 2 Q10 complete-re-read seats were dispatched, with no replacement policy. This wave already
   lost 5 build seats to provider capacity. If either Q10 seat dies, or returns with findings that change candidate bytes,
   admission needs a same-identity re-read that may be unobtainable. Admission must then stay deferred; one surviving seat
   must not be read as "complete".

Impacted axes: calibration (structural exit 0 or a "returned" report could be presented as Q10 byte-identity coverage) and
novelty/coverage (the C1 entry could land with unreviewed bytes). Classification: fixable process defects, closed by L1's final
checks below. No judge-level tradeoff. No checker change proposed.

## Exact final check L1 owes on the actual admitting commit C (cannot be claimed before C exists)

1. `git show C:corpus/knowledge/webarena-task-spec-audit.md | sha256sum` gives exactly `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8`
   (equivalently `git rev-parse C:corpus/knowledge/webarena-task-spec-audit.md` = `ccbae5acda570650b46e43057a2a6c543a3ffc30`).
   Any other value means the frozen review does not apply, and fresh same-identity re-reads are required first.
2. Every cited Q10 report in C, at minimum `.ufo/waves/round-28/falsify/FFullEntry.md` and `FContractEntry.md`, must:
   - record that same digest;
   - name `corpus/knowledge/webarena-task-spec-audit.md`;
   - have a final anchored `VERDICT: PASS`, or every non-PASS finding resolved without changing candidate bytes;
   - contain no line-start writer/author declaration equal to `KengakuR28`.
3. At the time each report returns, before integration, record its sha256 in a wave receipt. At C, compare
   `git show C:<report> | sha256sum` with that receipt.
4. The Gate row candidate cell must be exactly `knowledge/webarena-task-spec-audit.md` (drop " draft"). Its reason names each
   report by path, and only `falsify/` reports with roles reviewer, scout, critic, sentinel or revenger. Keep any generic phrase
   out of the reason cell, and state the digest in the reason cell.
5. At C, `candidate-freeze.json` and the three instrument digests must be unchanged. Otherwise rerun the counters at C before
   making any numeric claim.
6. `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-28.md --commit C` exits 0. This is structural gate
   evidence only, never truth or byte identity.
7. C cannot contain its own hash. Record actual-commit authority in a later pin, as in the round-27 precedent `93f4fde`
   ("pin actual admission"), naming C and repeating check 1's digest. Until then, no actual-commit authority is claimed.

VERDICT: PARTIAL — the pre-admission freeze is sound. The candidate digest `77e19d5b…` is verified in the working tree, in
commit `18b19226` and in the freeze record. The instrument and input pin chain is closed. The writer field truthfully names
KengakuR28, and no dead or placeholder seat supports anything. Nothing has been admitted prematurely. However, the reviewed →
admitted byte binding and returned-report integrity rest only on L1's unexecuted final checks 1–7. Before commit C exists, no
actual-commit authority can be claimed.
