# Round 67 verifier spot-check — kengaku (hyaku run 15, attempt 1)

author: hyaku closure (non-author integrator, @m_zfl)

Date: 2026-11-03. Lane repo: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Report:
`.ufo/reports/round-67/kengaku.md` (fleet commit `0c76ea7b`, author `kengaku-shokunin
<kengaku@shokunin.local>`, 2026-11-03 19:18:41 -03:00 — before the driver completion line
19:19:43). Lane HEAD before the round `4bc29fd8c8b260df419a23d590c5c7963986a3fb`; after
`f600c6d3f03a8bc4f10e624897a65b520ec81a6f`. I did not author the round; every command below
was run by me at closure time. Per PROTOCOL §Gate standard (Closure consequence) I verified
the lane's committed gate evidence and did not execute the lane's probes.

## 1. Step-1 conformance — PASS

- Report attribution: `git log --format='%an <%ae> %H %ad' --date=iso -- .ufo/reports/round-67/kengaku.md`
  → `kengaku-shokunin <kengaku@shokunin.local> 0c76ea7b… 2026-11-03 19:18:41 -03:00`. Lane identity, landed before driver completion.
- SHONEN heading: `grep -c '^## SHONEN' .ufo/reports/round-67/kengaku.md` → `1`; four `- [~]` lines,
  one per box of `SHONEN.md` (4 boxes). No `[x]` written by the lane — correct (non-author verification pending).
- Cited lane commits exist and are ancestors of the branch ref (jj-colocated; tested against `master`, not `@{u}`):
  `git cat-file -t` + `git merge-base --is-ancestor <h> master` → `4bc29fd8…` yes, `dcc39ea3` yes,
  `69ccfd04` yes, `f600c6d3…` yes. (`f44b7283…`/`27e8b41f…`/`32bacf1d…` in the report are file-content
  sha256s, not commits — verified as file hashes in §2.)
- Lane pushed and clean: `scripts/hyaku/jj-lane.sh state <lane>` → `branch=master
  local=f600c6d3… remote=f600c6d3… ahead=0 behind=0`; `git status --porcelain` → only six untracked
  driver markers (`.ufo/waves/round-63|64|66|67/w1.ready*`), no uncommitted round work.
- Prompt fidelity: `.ufo/prompts/kengaku-round-67.md` sections 1–5 are line-aligned with
  `templates/round-prompt.md` (same headings at the same lines 3/9/42/80/99/131) plus the hyaku
  addendum §6 (run-15 binding) and §7. All five child-lane items present (report path, commit-before-report,
  SHONEN heading, commit-hash citation, write scope).
- Watchdog digest (copied verbatim from `.ufo/watchdog.log`):
  `2026-11-03T18:46:24-03:00 launch kengaku round=67 pgid=113848 driver=hyaku-inline attempt=1` /
  `2026-11-03T19:19:43-03:00 complete kengaku round=67; hyaku-inline attempt=1`.
- Not a marker: the report names two declared claims, landed changes with hashes, counting commands,
  and resolvable evidence pointers throughout.

## 2. Per-claim re-check

### R67-C1 — coverage / capability `offline-torch-pipeline-parallel-grader-probe` — evidence-verified, ADMITTED

Re-measured before-state at `4bc29fd8` (my own runs):

- `git show 4bc29fd8:corpus/evidence/round52/graders/executed17.lst | grep -c torch-pipeline-parallelism` → `0`.
- `git cat-file -e 4bc29fd8:corpus/evidence/round67/pipe/receipt.txt` → absent (no receipt for this grader).

After-state at `f600c6d3` — committed-evidence verification (the probe is a lane-owned gate; not executed):

- `sha256sum plans/round67_c1_pipeline_probe.py` → `03793f4f9e184e8f829916ef848e0f0d41d94b1bef8ed17eda0fe3c28b0a9f1e`
  = the `PROBE sha256=` line inside `corpus/evidence/round67/pipe/receipt.txt` (the receipt binds the committed instrument).
- Case binding, my own hashing vs the receipt's `case_sha256=` values: q1-ref `5aab7e05…`, q3-stub `324da1b5…`,
  q4-hooks-noop `815ad9bf…`, q5-full-model `b1cb96c8…`, q6-unscaled-loss `0bb52dd1…` — all five match
  (`q2-none` has `case_sha256=none` and no case dir, matching "empty /app").
- Junit binding, my own hashing vs the receipt's `junit_sha256=` values: all six files under
  `corpus/evidence/round67/pipe/receipt.junit/` match exactly.
- VECTOR table in the receipt: q1-ref PPPP, q2-none FFFF, q3-stub PPFF, q4-hooks-noop PFPP,
  q5-full-model PPPF, q6-unscaled-loss PPFF, all `frozen=match` — identical to the report and SCORECARD.
- Red-after for the A1 counter: `corpus/evidence/round67/pipe/a1-mutants.txt` — base rc 0; mutants
  m02, m11, m12, v3, v4, v6, x all rc 1 with named `CHECK defect:` lines; v1 (line reorder) rc 0 by design.
- Capability row entered SCORECARD (`offline-torch-pipeline-parallel-grader-probe`, first working round 67);
  coverage held at 7 (L0 cap `kengaku | round-25/33/51`).

### R67-C2 — operability / `--strict` mode on the R65 sqlite receipt gate — evidence-verified, ADMITTED

- Strict mode present in the committed probe: `git show f600c6d3:plans/round65_c1_sqlite_probe.py | grep -c -- '--strict'` → `1`
  (clause block `# --- strict gate (R67-C2: clauses s1-s6)` at line 799); at the freeze `dcc39ea3` the same grep → `0` (mode absent, re-measured).
- Landed byte-for-byte: `cmp plans/round65_c1_sqlite_probe.py .ufo/waves/round-67/w1/StrictGateBuild/proposed/round65_c1_sqlite_probe.py`
  → identical; `sha256sum` of both → `27e8b41ffb36cf0b1e4c55055edf0129e3cab13c4c1093ce7121275968e3d857` (the cited proposal sha).
- Committed evidence files: `before-strict-absent.txt` (usage error, `unrecognized arguments: --strict`);
  `fabricated-strict.txt` — my count `grep -c 'CHECK defect:'` → `24`, `PREDICATE R65-C1 strict-fail`;
  `committed-strict.txt` → `PREDICATE R65-C1 strict-pass`; `fixture-runner.txt` → `RESULT fixtures=11 mismatches=0`
  (11 `PASS`, 0 `FAIL`); `cmp committed-default-before.txt committed-default-after.txt` → identical (default mode unchanged).
- Named gap verified in the attack evidence: `.ufo/waves/round-67/w1/ClaimFalsifier/falsify.md` A3 —
  `forge1-env-version.txt` (ENV value forged) → ACCEPT under strict; stated as found, not patched after data.
- Score held at 10; kill rules a/b/c not triggered (no red gate, no fabricated admission, no default-mode change).

### Counter A1 (R67-C1 instrument) — evidence-verified

`corpus/evidence/round67/pipe/a1-mutants.txt`: 8 mutants, 7 refused (rc 1) + 1 accepted by design
(line order is not in the predicate). The A1 amendment is dated in `plans/round-67-claims.md:74-77`.
The diff `dcc39ea3 → 69ccfd04` of the probe adds exactly the A1 enforcement (duplicates, unknown cases,
label agreement, rc equality, whole GRADER line, unreadable junit, refuse-overwrite).

### Axis harm — none

`git diff 4bc29fd8 f600c6d3 -- SCORECARD.md` is a pure append of the round-67 section (one hunk at
line 2912+; no earlier line touched). All seven scores held (coverage 7, operability 10, calibration 10,
depth 10, freshness 10, adjacency 9, novelty 8). `git diff 4bc29fd8 f600c6d3 -- PROVINCE.md` → empty.

## 3. Discernment spot-check (LEARNING.md)

The round's `## Gate` admits two sources and records no rejection, so the reject sample is empty this
round (noted below); both admits were re-opened.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S238 — TB2 `torch-pipeline-parallelism` grader `tests/test_outputs.py` @ pin `2fd12b88` | admit (tier A, code) | live `curl` of the raw.githubusercontent URL → HTTP 200, sha256 `23574246a407163a8e6581c84287cc2f1eb745efbaad2a317a5a28c39958c64f` = recorded sha = committed capture `corpus/evidence/round67/sources/torch-pipeline-parallelism-test_outputs.py` | agree | primary source (the grader's own assertions), scope-exact for R67-C1; located quote verified at line 157: `AFAB violation: found forward after backward at {key}` (8 words, ≤25) |
| S239 — TB2 `torch-pipeline-parallelism` `instruction.md` @ same pin | admit (tier A, docs) | live `curl` → HTTP 200, sha256 `989bfcf0c54baf6c8cdc391743dbb2f9e858c5779dd85112536875d4d1b2dcd2` = recorded sha = committed capture | agree | the task statement itself, the right authority for the schedule/hook legs; quote verified at line 18: `Run forward passes for all microbatches first, then run backward passes.` (11 words, ≤25) |
| reject sample | — | — | n/a | the round's Gate records zero rejections; nothing to sample. Observation, not a defect: both candidates presented were admitted on verified primary evidence. |

Registry: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 231 at the tip,
229 at `4bc29fd8` (`git show` + same grep) — matches the report. S238/S239 rows at
`corpus/SOURCES.md:253-254` with URLs, tier A, scope, anchor pin.
Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` →
`kengaku ok …/corpus/SOURCES.md`, rc 0 (pre-existing W04 duplicate-url warnings, status-neutral, predate this round).

## 4. Trend verdicts (closure, with evidence)

- **expansion: improved** — verified: second executed `process-environment` member (SKILL.md:81 now
  `executed 2 of 3`), two live-opened tier-A registry rows (S238/S239, re-opened by me), one knowledge
  entry with the provenance trio (`corpus/knowledge/tb2-torch-pipeline-parallel-offline.md`), capability
  row entered SCORECARD.
- **quality: improved** — verified: the R65 gate's strict mode refuses the fabricated fixture (24 defects,
  rc 1) and accepts the committed receipt (rc 0); the R67 counter's mutation-found gaps closed by A1 with
  red→green evidence; census rc 0 at both ends; default mode byte-identical.
- **discernment: unchanged** — agreed: no exploratory claim, so no `unprovable-but-better` verdict is
  available; the two overclaims the non-author seats found (A3, A4) are mined as lesson rows 8 and 10
  rather than smoothed; my spot-check agrees with both gate admits.

## 5. Routed defects for round 68 (status-neutral; admission not barred)

1. **Wrong instrument sha cited (report + evidence header).** The report (Amendment A1 bullet) and the
   `a1-mutants.txt` header cite `PROBE sha 32bacf1d…` as the amended counter; `32bacf1d` is the
   pre-A1 frozen probe at `dcc39ea3`. The receipt of record and the committed probe bind
   `03793f4f9e184e8f…` (verified by my own sha256sum). The mutant results themselves are consistent
   with the amended counter's behavior (the A1 checks exist only in `03793f4f`), so the substance
   stands; the citation is wrong. Fix: dated erratum naming `03793f4f…`.
2. **Mutant count drift.** Report and LOG.md say A1 mutants "8 killed, 1 accepted"; the committed file
   shows 7 refused (rc 1) + 1 accepted by design = 8 mutants. Fix: dated correction (number-drift class).
3. **Self-test tally not committed.** The report/LOG quote `SELFTEST green_rc=0 red_rc=1 ok` for the
   round-67 probe, but no committed file records that tally (grep over the repo finds no round-67
   SELFTEST receipt). The `--selftest` mode exists in the committed probe (line 357). Fix: commit the
   self-test tally next round (Gate standard: committed self-test evidence).
4. **Registry rows stale.** SKILL.md's registry has no row for the new `round67_c1_pipeline_probe`
   gate, and the `round65-c1-sqlite-probe` row (SKILL.md:686) was not updated for the new `--strict`
   flag or its verdict codes. Gate standard: a gate is conformant only with its registry row at the
   registry home. Fix: add/update both rows.
5. **SKILL-row before-value misstated.** The report's R67-C1 before-state says "process-environment
   executed 1 of 3"; the committed bytes at `4bc29fd8` read `recipe-unexecuted` (round 66 executed the
   tensor-parallelism member but never updated the row; no committed file says "executed 1 of 3"). The
   true delta is `recipe-unexecuted → executed 2 of 3`, which is larger, so the claim's substance is
   unaffected. Fix: dated correction; also note the round-66 row-update omission.
6. **Wave results.json carries no seat outputs.** All 13 entries have `output: null` with the note
   "orchestrator kernel restarted mid-wave … read the seat report file in the wave dir". The seat
   outputs survive as committed per-seat files (all 13 seat dirs + `.md` reports present and nonempty),
   so the report's "13 of 13 seats settled" is supported by those files, not by results.json.
   Conformance-neutral; recorded so a later reader does not treat results.json as the output record.

## 6. SHONEN note for the operator

All four boxes are `[~]` with resolvable pointers, and this spot-check resolved every one of them
(SKILL.md:81 row verified; LOG.md Round 67 entry verified; knowledge entry with provenance trio
verified; PROVINCE.md untouched with the ConnectorOverlap report consistent). They look fully
checkable by a non-author verifier; promotion is operator-owned and not acted on here.

## Commands run (closure session, 2026-11-03)

git log/cat-file/merge-base over the four cited commits; jj-lane.sh state; git status --porcelain
(lane and fleet); sha256sum over the probe, five case files, six junit files, both source captures,
the landed strict probe and its proposal; grep counts over executed17.lst, SOURCES.md, the strict
evidence files, a1-mutants.txt, fixture-runner.txt; cmp of proposal vs landed probe and of the two
default-mode receipts; two live curls of S238/S239 with sha256 and line-located quote checks;
sources-census.sh validate (rc 0); SCORECARD and PROVINCE diffs `4bc29fd8..f600c6d3`.
