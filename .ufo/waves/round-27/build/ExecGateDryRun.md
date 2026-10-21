# ExecGateDryRun — round-27 Gate timing dry run (WRITER, sandbox only)

Base 11a7fc8c64dc5d634331be24ccf5936f84a11f03 (= lane master, observed). Sandbox /tmp/kengaku-r27-ExecGateDryRun (branch r27-ExecGateDryRun, retained for re-run). Lane tree, index, jj state, fleet and config untouched; this report is the only lane write.
Checker: sandbox copy of plans/gate_timing_check.py, sha256 1b748e52a35a5bd900462cd34d0cc3660d06a770b8d06cf05e22b348c4b3f69d (identical to lane copy). Tools: git 2.56.0, Python 3.14.8; no installs. Run with PYTHONDONTWRITEBYTECODE=1 from the sandbox.

## Sandbox commits
(a) b2ea736c4bb4af773cb8d257a87d3c241cccabb2: corpus/lessons/round-27.md + corpus/knowledge/extraction-policy-comparison.md. Round-27 wave files in tree: 0.
(b) a1cf2b4a02b941e2dd949c8e64de9f480fb28ac9: adds falsify/SynthReviewerA.md (role reviewer), falsify/SynthScoutB.md (role scout), falsify/swarm-registry.json. Lesson and candidate blobs identical to (a) (4aa5d8ec9e91eb430c9f981dc540f9b7ea4d81c4, fb653ac4020c194ebdfe404871ad24674cdf245d). New files mode 100644, sizes 237/231/181.

## Exact outputs
$ python3 plans/gate_timing_check.py --lesson corpus/lessons/round-27.md --commit b2ea736c4bb4af773cb8d257a87d3c241cccabb2 --repo /tmp/kengaku-r27-ExecGateDryRun
FAIL line 10 Gate admit: candidate='corpus/knowledge/extraction-policy-comparison.md'
  cell[reason]: Re-reads returned at `.ufo/waves/round-27/falsify/SynthReviewerA.md` and `.ufo/waves/round-27/falsify/SynthScoutB.md`; each names the candidate and carries a VERDICT line.
  cited seat-report paths: '.ufo/waves/round-27/falsify/SynthReviewerA.md', '.ufo/waves/round-27/falsify/SynthScoutB.md'
  invalid cited second-seat report: .ufo/waves/round-27/falsify/SynthReviewerA.md (absent from commit tree)
  invalid cited second-seat report: .ufo/waves/round-27/falsify/SynthScoutB.md (absent from commit tree)
  missing: no .ufo/waves/round-27/falsify/ report exists in commit b2ea736c4bb4af773cb8d257a87d3c241cccabb2
  reasons: no cited, existing, returned second-seat report for this round; one or more cited second-seat reports fail identity/return checks
gate_timing_check: commit=b2ea736c4bb4af773cb8d257a87d3c241cccabb2 lesson=corpus/lessons/round-27.md admissions=1 passed=0 failed=1 second-seat-reports=0
exit=1
$ python3 plans/gate_timing_check.py --lesson corpus/lessons/round-27.md --commit a1cf2b4a02b941e2dd949c8e64de9f480fb28ac9 --repo /tmp/kengaku-r27-ExecGateDryRun
PASS line 10 Gate admit: candidate='corpus/knowledge/extraction-policy-comparison.md'
  cited seat-report paths: '.ufo/waves/round-27/falsify/SynthReviewerA.md', '.ufo/waves/round-27/falsify/SynthScoutB.md'
  existing returned second-seat report(s): .ufo/waves/round-27/falsify/SynthReviewerA.md, .ufo/waves/round-27/falsify/SynthScoutB.md
gate_timing_check: commit=a1cf2b4a02b941e2dd949c8e64de9f480fb28ac9 lesson=corpus/lessons/round-27.md admissions=1 passed=1 failed=0 second-seat-reports=2
exit=0

## Structural requirements for the real round-27 admission (code at base; line refs)
R1 Lesson `corpus/lessons/round-27.md`: round from path component `round-27.md` (:49, :387-398); must exist at --commit (:635-640).
R2 `## Gate` heading (level 1-6; title `Gate` + word boundary or —:-; :150-161). Header cells candidate/decision/reason, case-insensitive (:169-172). Admit = decision matching `^admit(ted)?\b` after stripping `` ` * _ `` (:138-139, :185); `admit-pending` also counts.
R3 Candidate cell must be a committed blob as written or as `corpus/<cell>` (:312-318). Round-26 used `knowledge/...`; both forms work.
R4 writer field: candidate needs a column-0 `writer:` line; first match wins; token stops at whitespace, backtick or # (:53, :250-254); missing → FAIL (:348-349). QUALITY Q1 (:15-19) separately needs source:/verified-at:/recheck: on lines 1-3; round-26 writer sat on line 4 (checker-neutral).
R5 Registry path: `.ufo/waves/round-27/falsify/swarm-registry.json`, exact basename, in the same wave dir as the reports (:290). Other names (falsify-registry.json, top-level build-registry.json) are never read → "not in the committed wave registry" (:344-345).
R6 Registry shape: object with `members` object (:298-302); key = report stem, case-sensitive; value an object; `role` string compared after casefold() with no strip (:303-306); `agentId` string or null, string equal to writer → FAIL (:307, :352). Extra keys ignored; lane ufo-swarm-registry-v1 files fit (round-26 falsify at d4dfdb0: 64 members keyed by seat; round-27 build/swarm-registry.json same schema, observed).
R7 Role allowlist, exact after casefold: reviewer, scout, critic, sentinel, revenger (:22-24, :346-347). Round-26 falsify registry (d4dfdb0): 50/64 qualify (39 reviewer, 7 scout, 4 critic); 14 do not (10 mutation-tester, 2 executor, 2 connector). Selftest role rejects at :566-574 (code only; not run).
R8 Cited report (full path, relative `falsify/X.md`, or bare `X.md` unique across ALL round-27 wave dirs incl. build/; :257-279) must be in the --commit tree, mode 100644, size>0 (:340-343). Build-only cites are ignored (:277-278) → no support (:366-367). One invalid cited second-wave report fails the row (:368-369).
R9 Report identity: stem ≠ writer, casefold (:350); column-0 `writer:`/`author:` in report ≠ writer exactly (:354-355); report contains the Gate candidate cell text or resolved path (:356-357); column-0 `VERDICT: <text>` (:358-359).
R10 Reason cell: no generic refs outside citation spans ("wave-2 seats", "falsify seats/reports/wave", "by wave-N", "second seat(s)", "rest of the falsify wave") (:39-48, :372-373).
R11 Timing is tree-only: the checker reads only --commit's tree (:647-665) and cannot find the commit that first added the row. Observed: (a) row without reports → 1; (b) same unchanged row plus reports → 0. Admission timing needs the check on the first row-introducing commit; same-commit precedent is recreate.sh case C (:62-72; expected PASS at :92). Matches round-26 M39.
R12 Gate scope: any heading whose title starts "Gate", at any level, opens a scope; deeper headings stay inside until a heading of level ≤ it (:154-161). Keep erratum/addendum titles from starting with "Gate", or their admit rows get audited.

## Additional findings (code-derived; not run)
F1 Bare-name collision: lane round-27 build/ already contains CritPredictionsHonesty.md (observed); a falsify seat with that stem must be cited by full path or the bare cite is unresolved → FAIL (:257-279, :370-371).
F2 Role strip: "reviewer " with trailing space is rejected (:306).
F3 Not checked here: Q1 triad, Q7 index/coverage rows, truth of findings (Q9/Q10), reject rows (non-admit rows not audited). Connector seats never count (Q14); per Main's notice, connector routing is down (429 / cascade).
--selftest not run (outside assignment).

## Files written in sandbox (sha256)
51783d40e06d3f235ec5b3f2ba3dfe70ca1ca88f7e812293de206e30cb97d6e8  corpus/lessons/round-27.md
720681cf726a607fc43c07507580f1be4d04cf951fc57a9b775d939ca3beec8b  corpus/knowledge/extraction-policy-comparison.md
fa55cd5d30fb16906c842a4ed85a27c72acda62aec5abfb6b7dc4c6702691043  .ufo/waves/round-27/falsify/SynthReviewerA.md
f90f71d1b83462c5bd361e37120b94a3c5198e9d24d563a61860669715ef7e29  .ufo/waves/round-27/falsify/SynthScoutB.md
62110838096cad2ede8b11eca1e4e1b54fce882c366cc9b593050cfdc22d6cfc  .ufo/waves/round-27/falsify/swarm-registry.json

Installs/updates: none. No live model requests, no pacman, no labrat.
VERDICT: Sandbox dry run gives 1 then 0 as expected; because the checker reads only the --commit tree, the (b) PASS does not prove admission timing, so the real round-27 Gate row and its reports must land in one commit and be checked on that commit.
Follow-up assignment (supersedes line 46): `plans/gate_timing_check.py --selftest` now builds a temporary Git pair with identical lesson bytes; it asserts early report inventory=0/fail, later inventory=1/pass. Source sha256 7c8b498ea501a1d4ec67283d51ac0a0d7d57a293e3180a85218dbd2930f284f1.
Clone follow-up files: 7c8b498ea501a1d4ec67283d51ac0a0d7d57a293e3180a85218dbd2930f284f1 `plans/gate_timing_check.py`; 276807c6862ce3517a1041b3c4dbc860879d554fee10231487949cf517a93e19 `plans/fixtures/r27/gate-timing-worktree-restored.txt`.
167d850db737ef5b6cf36cee94ae06984a50d3577ab05dc1192e723d0edd14e3 `plans/fixtures/r27/gate-timing-worktree-mutant.txt`. Mutant selftest exits 1 (early inventory=1, expected 0); restored exits 0 (early=0/later=1, lesson unchanged); exact red/green outputs retained in receipts.
VERDICT: The new selftest rejects the working-copy inventory leak and passes with commit-tree inventory; original dry-run result unchanged. No installs.
