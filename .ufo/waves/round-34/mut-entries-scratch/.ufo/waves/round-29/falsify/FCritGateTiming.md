writer: KengakuR29-2.FCritGateTiming-2
# FCritGateTiming — attack on the round-29 Q13–Q16 admission package plan

Seat FCritGateTiming (critic), registry agentId `KengakuR29-2.FCritGateTiming-2`. The actual writer is this seat.
Candidate under admission: `corpus/knowledge/webarena-config-projection.md`, currently the draft
`.ufo/waves/round-29/drafts/webarena-config-projection.md` with sha256
`7006b93dcacff38736cb49f2153e2b3960591887576b3e8c2ddc3519565653dc` (observed with `sha256sum`; it matches candidate-freeze-v1.json).
This seat did not review the candidate's content. It reviewed only the admission-gate mechanics around it.

Source reading: I read `plans/gate_timing_check.py` in full, because it is the attacked instrument. I did **not** read
`plans/config_projection.py` source. Tool installs or updates: none (stdlib python3 and the system git only; no pacman).
Lane writes: only this report and `.ufo/waves/round-29/scratch/falsify/FCritGateTiming/`. All Git writes went to
throwaway repositories under `/tmp`, which were removed after the run (`ls /tmp | grep -c fcrit-gate` gives 0).

## Observed baseline facts

| fact | command / location | observed value |
|---|---|---|
| lane HEAD | `git rev-parse HEAD` | `56fd949a6478342531e61f4feecb4a685d831640` |
| checker digest | `sha256sum plans/gate_timing_check.py` | `51c18a9e…0a2a`; same digest pinned in `plans/fixtures/r27/gate-timing-v3-restored.txt` and the r27 byte proof; last touched by commit 6356b0b |
| Q15/Q16 selftest | `python3 plans/gate_timing_check.py --selftest` (cwd /tmp) | exit0; output ends with the line "ALL PASS (five allowed roles; …)" (`/tmp/fcrit-gt-selftest.txt`) |
| r28 precedent at its admitting commit | `corpus/evidence/round28-calibration/actual-gate.txt` | df33fc83 had exit1. FFullEntry.md had "no anchored VERDICT line" |
| r28 report bytes changed after admission | `git show <c>:.ufo/waves/round-28/falsify/FFullEntry.md \| sha256sum` | df33fc8 `6650422a…` → 78e6df8 `67b51428…` |
| r28 FContractEntry verdict lines at df33fc8 | `grep -n '^VERDICT'` | line 240 PARTIAL, line 305 PARTIAL, line 361 PASS. The checker accepted it |
| round-29 falsify registry tracked? | `git status --short` (16:53:03Z) | `?? .ufo/waves/round-29/falsify/`, i.e. the registry and every report are untracked |
| registry composition | `.ufo/waves/round-29/falsify/swarm-registry.json` | 77 members. All 77 agentIds start with `KengakuR29-2.`, and none equals `KengakuR29-2`. 16 seats have ineligible roles: 8 executor (FOracleText/Leaf/Provenance/Index, FMutCategoryShape/Markers/PinReread/SourceContract), 4 mutation-tester (FMutIndexById/Normalize/Order/UrlOnly), 2 connector, 2 simplifier |
| candidate `writer:` line | draft line 4 | `writer: KengakuR29-2` at column 0 (WRITER_RE matches) |
| canonical entry / Gate present? | `ls`, Read | the canonical entry is absent. The working-tree `corpus/lessons/round-29.md` (sha256 `98999171…`, 25 lines) has no Gate section yet |
| returned falsify reports at 16:53Z | scan script (inline python, output above in session) | 29 `.md`. Only `FReopenS070.md` contains `knowledge/webarena-config-projection.md`. None contains the 7006b93 digest |
| reread prompts | `falsify-spec.json` items | FEntryNumbers and FEntrySources (both reviewer) are told to include the full digest and the canonical path. FEntryScope and FEntryQuality (critic) are not told to include the canonical path |

## Sandbox attack (unchanged checker, synthetic admitting trees)

Script: `.ufo/waves/round-29/scratch/falsify/FCritGateTiming/gate_attack.py` (sha256 `15277beb…`). Output: `gate_attack.out` (27 JSON
lines, sha256 `41a852d2…`). Each scenario is its own `/tmp` repo. The base tree has the draft bytes at the canonical path, the
real untracked falsify registry, and synthetic reports for FEntryNumbers and FEntrySources. Those reports name the canonical path and digest
and end with `VERDICT: PASS`. The lesson is `corpus/lessons/round-29.md`, and the checker runs with `--commit <sandbox HEAD>`.

| scenario | exit | checker reason (verbatim fragment) |
|---|---|---|
| A two eligible full-path reports | 0 | both "existing returned second-seat report(s)" |
| B cited report `VERDICT: FAIL` | **0** | accepted |
| B2 cited report `VERDICT: PARTIAL` | **0** | accepted |
| C + executor `falsify/FOracleText.md` | 1 | "seat role 'executor' is not an allowed read-only reviewer" |
| D + mutation-tester `falsify/FMutUrlOnly.md` | 1 | "seat role 'mutation-tester' …" |
| E4 bare `SOURCES.md` mid-sentence | 1 | "unresolved bare report reference(s): SOURCES.md" |
| E5 backticked `README.md` | 1 | "unresolved … README.md" |
| E6 bare `SCORECARD.md` | 1 | "unresolved … SCORECARD.md" |
| E/E3 the same names followed by "." | 0 | not detected (BARE_REPORT_RE lookahead) |
| E2 `corpus/SOURCES.md` | 0 | path form is safe |
| F "second seat" (space) | 1 | "generic seat reference(s) … 'second seat'" |
| F2 "second-seat" (hyphen) | 0 | — |
| F3 "falsify reports" | 1 | generic |
| G report names only the drafts path | 1 | "report does not name the admitted candidate path" |
| H falsify registry not committed | 1 | "seat is not in the committed wave registry" (both) |
| I report contains a column-0 line `writer: KengakuR29-2` (quoted header) | 1 | "report writer/author declaration equals candidate writer" |
| J extra Gate row `S070–S073 \| admit` | 1 | "admitted candidate is absent from the commit tree" |
| K decision `admit-pending` | 0 | parsed as an admit (`is_admit`, line 140) |
| L entry bytes ≠ 7006b93 (appended text) | **0** | digest not checked |
| M candidate cell `corpus/knowledge/…`, report has only `knowledge/…` | 1 | candidate path not named |
| N heading-form `## VERDICT: PASS` (r28 M85 repeat) | 1 | "no anchored VERDICT line" |
| P admission table under `## Admission decision` | 1 | "no ## Gate section" |
| P2 column named `rationale` | 1 | "no admit rows in ## Gate" |
| R + `build/R29DraftEntry.md` | 0 | build citation silently ignored |
| U relative `falsify/X.md` + bare `FEntrySources.md` | 0 | — |
| V canonical entry absent | 1 | "candidate has no committed writer: field" |

Real returned bytes: `gate_real_reports.py` copies the actual `FReopenS070/S072/S073.md` (sha256 `1389885a…`, `aae7dbbb…`, `ea2bc1e4…`)
into a sandbox and cites all three. The result is exit1 (`gate_real_reports.out`): S072 and S073 fail with "report does not name the admitted candidate path".
Citing only FReopenS070 gives **exit0** (`gate_real_s070.out`). Its only mention of the candidate, at line 90, is a statement that the file is absent:
“`corpus/knowledge/webarena-config-projection.md` does not exist” (4 words, `len(q.split())`).

## Objections

1. **Q13 accepts FAIL/PARTIAL and stale-digest support. The prereg's PASS+digest condition has no instrument.** Fixable defect in the plan (the checker's narrow scope is a documented tradeoff).
   Evidence: `gate_timing_check.py:360` only tests `VERDICT_RE.findall(content)`, and line 56 accepts any value. Scenarios B, B2 and L exit0.
   In the r28 precedent, a report with PARTIAL, PARTIAL, PASS verdicts passed. The prereg (lines 93–94) requires “until complete eligible second-seat source/number re-reads return on exact final bytes, writer differs,
   plain anchored VERDICT: PASS exists” (18 words) and line 95 “Q13 is structural only; digest/actual-commit proof separate.” (7 words).
   Nothing under `plans/` implements that separate proof: r28's `actual-admission-byte-proof.json` came from no committed script (`rg` over plans finds none).
   Impacted axes: novelty (admission integrity), calibration of the gate claim.
   Smallest safe correction: add a stdlib one-shot, run read-only against the prospective and the actual commit, and retain its output. It must check that, for every cited path,
   (a) the last column-0 `VERDICT:` line is exactly `VERDICT: PASS…`,
   (b) the report contains the full 64-hex digest of the candidate blob at that commit, and
   (c) that blob's digest equals the freeze file in the same tree.
   Do not change `gate_timing_check.py` (its Q13–Q16 receipts are pinned).

2. **A negative mention satisfies "names the candidate".** Fixable defect in the Gate plan; the checker has a known substring tradeoff.
   Evidence: line 358 uses substring `in content`. Real FReopenS070 passes as the only support even though it did not review the candidate and
   contains no candidate digest. QUALITY.md:105 promises only “a candidate mention and a final verdict” (7 words).
   Smallest safe correction: the admit reason cell cites only FEntryNumbers and FEntrySources. Their prompts require the canonical path and digest,
   so they meet correction 1. Source-reopen scouts (FReopenS07x) belong in the source-opening table, which is not a candidate/decision/reason
   table and so is not graded.

3. **The falsify registry and reports are untracked, which is fatal if missed.** Fixable defect.
   Evidence: `git status` shows `?? .ufo/waves/round-29/falsify/`. Scenario H gives exit1 for every cited seat. The registry is
   rewritten as seats spawn (`updatedAt` 16:47:14.661Z), so it must be committed in its final form.
   Correction: stage the whole `falsify/` directory plus `falsify-*.json/txt` dispatch evidence in the admitting commit. r28 df33fc8 did this for all 64 reports.

4. **Citing the independent oracle or mutation witnesses in the admit cell turns Gate red.** This is a tradeoff the Rust judge must accept: oracle agreement is
   C1 evidence, not Q10 reread support.
   Evidence: scenarios C and D, and the 16 ineligible seats include all 4 FOracle* executors and all 8 FMut* seats. QUALITY Q14 (lines 111–114) excludes these roles.
   Correction: report oracle and mutation agreement in a non-Gate paragraph or a table without the candidate/decision/reason header.

5. **Gate-cell lexical traps.** Fixable; author discipline.
   Bare `SOURCES.md`, `README.md` or `SCORECARD.md` (E4–E6) make the row red. The space form "second seat" and "falsify reports/seats/wave" (F, F3) are generic.
   Any other `admit…` decision (J, K, including `admit-pending`/`admitted`) is graded and fails unless it is a resolvable entry.
   A heading not starting with "Gate" (P) or a column not named `reason` (P2) yields zero admissions.
   Correction: use `corpus/`-prefixed paths, the hyphenated "second-seat", and exactly one admit row. Source-row, mistake and lesson decisions use `mined`/`recorded`/`defer`.

6. **Self-declaration trap in reports.** Fixable defect, low likelihood.
   Scenario I: any report that reproduces the candidate header line `writer: KengakuR29-2` at column 0 is rejected as self-review (line 356).
   The current 29 returned reports have 0 such lines (scan).
   Correction: before the prospective check, grep the cited reports for `^(writer|author):\s*KengakuR29-2\s*$`.

7. **Timing: the r28 precedent landed red and then mutated a cited report after admission.** This is a process defect that r26 and r27 had already solved.
   Evidence: r28 lesson line 278 says “First admitting commit df33fc83764975fd808b0945097b5d0c7aca3901 had two observed red checks” (9 words).
   FFullEntry bytes changed 6650422a→67b51428 in 78e6df8, so the admit at df33fc8 cited a report whose return marker was not yet valid. The r28 Gate
   cell (line 263) still asserts “both final VERDICT: PASS for SHA256” (6 words) for that tree.
   r26 (LOG.md:371) and r27 (LOG.md:454, round-27.md:223) ran a prospective sandbox admission first. The r28 lesson has no prospective record (`rg -n prospective` gives 0 hits).
   Smallest safe correction:
   - Build the exact admitting tree in a `/tmp` clone and run both the Q13 CLI and correction 1 there. Land only on exit0.
   - Then record `git rev-parse <admit>^{tree}` equal to the prospective tree hash.
   - Record the actual-commit Q13 and byte-proof receipts in a follow-up commit. A commit cannot contain a receipt naming its own hash. This timing is the r28 78e6df8 pattern, minus the red.
   - Never edit a cited report after the admit commit.

8. **Identity lineage is author-side, not independent.** Tradeoff to disclose, not a defect.
   Candidate writer `KengakuR29-2` differs as a string from every `KengakuR29-2.<Seat>-2` agentId (line 354 equality only). Those seats are children of the writer's session.
   QUALITY Q14 already states that identity means the registered seat, not proof of authorship. The writer also changed from the prereg's KengakuR28 to KengakuR29-2.
   The working-tree lesson (lines 3–5) discloses that change, and no round-29 falsify seat carries either identity, so no self-review hole was found.
   The draft's own line 14 discloses that R29DraftEntry (build scribe `KengakuR28.R29DraftEntry-2`) drafted the first scope. That seat is not in the falsify registry.

9. **Committed draft lesson ID drift (non-blocking).** `.ufo/waves/round-29/drafts/lesson-and-mistake.md:26` says “the next free number after M84 is M85” (8 words).
   That is false: `corpus/lessons/round-28.md:281` (M85) and `:285` (M86) already use those numbers. The working-tree lesson already uses M87–M89, so the canonical text is correct.
   Keep the draft as historical evidence. Do not copy its M85 label.

## Exactly what the admitting commit must contain for `corpus/knowledge/webarena-config-projection.md`

1. `corpus/knowledge/webarena-config-projection.md` must be byte-identical to the digest every cited report reviewed, currently `7006b93d…53dc`.
   If the candidate changes, it needs a new freeze plus same-identity rereads. It must keep the column-0 `writer: KengakuR29-2` line.
2. The matching freeze file, `.ufo/waves/round-29/candidate-freeze-v<N>.json` (v1 is already committed for 7006b93).
3. `corpus/lessons/round-29.md` with a heading whose title starts with `Gate`, containing a pipe table with header `candidate | decision | reason`
   and exactly one `admit` row. The row needs:
   - the candidate `knowledge/webarena-config-projection.md`;
   - a reason that cites `.ufo/waves/round-29/falsify/FEntryNumbers.md` and `.ufo/waves/round-29/falsify/FEntrySources.md` by full path, once those seats have returned;
   - no generic phrase, no bare uppercase `*.md`, and no ineligible-role or source-reopen report.
4. `.ufo/waves/round-29/falsify/swarm-registry.json` committed with those seat keys (reviewer roles), plus every returned falsify report
   as a nonempty 100644 file and the round's `falsify-*` dispatch evidence.
5. Each cited report must:
   - name `corpus/knowledge/webarena-config-projection.md`;
   - contain the full reviewed digest;
   - have no column-0 writer/author line equal to `KengakuR29-2`;
   - have a final column-0 `VERDICT: PASS`.
   Prior PARTIAL sections may remain if they name earlier digests.
6. `corpus/README.md` gets an index row whose first cell is `` `knowledge/webarena-config-projection.md` `` (the census regex at `plans/round28_census.py:43` counts only first-column rows),
   with no duplicate, plus a coverage-map row.
7. `corpus/SOURCES.md` S070–S073 move status `queued` → `mined`, and used-by `—` → `corpus/lessons/round-29.md, corpus/knowledge/webarena-config-projection.md`.
   S068 used-by gains `corpus/knowledge/webarena-config-projection.md` only after its round-29 reopen (prereg line 88). The admitting lesson records the exact old → new cells, following the r28 lines 265–270 pattern.
8. Recommended, following r28 precedent: `.ufo/waves/round-29/returned-report-pins.json` with the sha256 of every cited report at the admitting tree.
9. These are **not** in that commit: the actual-commit Q13 receipt and the correction-1 byte proof, which go in the next commit after a passing prospective sandbox run.
   The lesson must not claim their results before they exist.

## Scope of this verdict

The checker itself behaves as documented, and its selftest is green. The plan as currently stated would let a FAIL-verdict, stale-digest
or negative-mention report support the admit. It also cannot pass at all until the falsify directory is committed.
These are fixable. The admission can still be correct if corrections 1–3 and 7 are applied.

VERDICT: PARTIAL
