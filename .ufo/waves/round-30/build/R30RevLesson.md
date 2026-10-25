# R30RevLesson — Q8 / Q9 / Q13 review of the drafted round-30 Gate block

Two passes: pass 1 is against the draft as first written (`7586e1c3…`), pass 2 (at the end of this
file) against the rebuilt draft (`a4f60e21…`) **and** the committed lesson
`corpus/lessons/round-30.md`. Pass 2 supersedes pass 1 wherever they differ; pass 1's four Q13
blockers and its Q8/Q9 cell findings are closed in both artifacts, and pass 1's own arithmetic
correction is recorded in pass 2 §Q8-L2.

Seat `L1Kengaku30.R30RevLesson` (leaf, reviewer). Date 2026-10-25. Scope: the drafted
`## Gate` block only, against `corpus/QUALITY.md` Q8 (`:61-65`), Q9 (`:67-73`) and Q13
(`:97-109`), with the round-29 Gate sections (`corpus/lessons/round-29.md:175-186`,
`:216-243`) as the shape precedent. No production file was written; the only lane file
written is this report. Scratch: `/tmp/r30-RevLesson/`.

Draft identity as reviewed: `/tmp/r30-DraftGate/gate.md`, sha256
`7586e1c38ae6930c0d3079ae71b660559a43baf00110cbb632f31775cc9c8637`, 13 443 B, 60 lines.
Row 11 = the admit row; rows 12-18 = judge-calibration-thresholds, card-publication-contracts,
the package's validity-checklist copy, benchmark-grader-semantics, the register slice, the
bulk deferral, the `considerthese` proposal.

Two source-of-record notes before the findings:

- The seat's IRC described a revision (six `R30SrcS081`…`S086` receipts cited in the pointer
  column, five preconditions, `CG1–CG8` labels). Those bytes are **not** in the file at the
  hash the seat itself named: `grep -n 'R30SrcS08\|CG1' /tmp/r30-DraftGate/gate.md` → no match.
  The reviewed file has three precondition bullets (lines 28-42) and no source receipts.
- `/tmp/r30-R30DraftGate/` exists but is empty (`ls -la` → `.` and `..` only), so the claimed
  byte-identical copy does not exist. Nothing below depends on it.

## Verdicts

| criterion | verdict | where it fails |
|---|---|---|
| **Q8 — rejections are kept** | **PASS on form, FAIL on two cells** | line 17 count "69 remaining staged entries"; line 14 flip cell "nothing to flip" |
| **Q9 — reason follows from evidence** | **FAIL** | line 11 Q6/label/pointer cells; line 12 Q6 half; line 15 property conflation; line 16 fleet pointer |
| **Q13 — second-seat re-read in the landing tree** | **FAIL on four independent blockers** | line 11 candidate cell; line 11 reason cell; `build/` is not a second-wave directory; no anchored `VERDICT:` line in the three cited reports |

Q8's structural requirement — at least one admit and at least one reject from the same
assimilation set — **holds**: the admit is a package entry (`corpus/knowledge/contamination-transparency-card.md`,
`source:` S081–S086) and four reject rows (12, 13, 14, 15) plus the bulk and `considerthese`
rows are all package/round candidates. Every non-admit row carries a flip-condition cell.
The two Q8 failures are cell-level, not structural.

## Q13 — the block does not satisfy the check as it exists today

All probes below are executable: `python3 /tmp/r30-RevLesson/make_fixture.py` builds a
throwaway repo and runs `plans/gate_timing_check.py` against thirteen Gate-table shapes.
The mechanism that matters is `plans/gate_timing_check.py:328-370`:
`audit_admission` reads **only `admission.reason`** (one cell of the admit row), the citation
must resolve under `.ufo/waves/round-<N>/falsify/` or `wave[-_ ]?0*2` (`:242-243`,
`is_second_wave`), the candidate must resolve inside the commit tree (`:320-326`), the entry
must carry `writer:` (`:355`), and each report must contain the literal candidate path
(`:358`) and a line matching `^VERDICT:\s*\S` (`:56`, `:360`).

### Q13-1 — the candidate cell carries the source-id list, so the candidate is unresolvable

Failing cell, line 11 col 1:

> `corpus/knowledge/contamination-transparency-card.md` (S081, S082, S083, S084, S085, S086)

`plain_cell` (`:126-127`) strips backticks and stars but not the parenthetical, so the
resolved candidate string is `corpus/knowledge/contamination-transparency-card.md (S081, …)`
and `resolve_candidate_path` (`:320-326`) tries two nonexistent paths. Probe M reproduces the
draft's exact shape:

```
FAIL line 7 Gate admit: candidate='corpus/knowledge/contamination-transparency-card.md (S081, S082, S083, S084, S085, S086)'
  reasons: admitted candidate is absent from the commit tree; … exit=1
```

Round-29's admit row had the same shape (`corpus/lessons/round-29.md:178`), so this defect is
inherited, not invented; it still fails.

**Corrected wording (col 1):**
`| `corpus/knowledge/contamination-transparency-card.md` | **admit**, as an amendment to the lane's tabulated card designs |`
— the ids move out of col 1. Keep them where they are read for other purposes: the reason is
the right home (append "sources S081–S086, all six rows appended in this commit").

### Q13-2 — the admit row's reason cell cites no report; the citation is in col 5

Failing cell, line 11 col 3 — 162 words, none of them a report path:

> the entry asks for the one thing round 29's reject demanded: it is framed as an amendment
> that names what it extends, not as a fourth rival design, …

and line 11 col 5 holds `corpus/lessons/round-29.md:180,223-227,242-244`; … plus the
`### Second seat` paragraph (lines 44-48) which names the three reports. The checker never
reads col 5 or the paragraph. Probe D, which is the draft's column layout verbatim:

```
### D  citation only in the read-pointer column  exit=1
FAIL line 7 Gate admit: … cited seat-report paths: none
  reasons: no cited, existing, returned second-seat report for this round
```

**Corrected wording (append to line 11 col 3, after the existing sentence):**
` Second-seat re-reads for this admission: `.ufo/waves/round-30/falsify/R30RevEntryQ1Q6.md` (VERDICT: PASS) and `.ufo/waves/round-30/falsify/R30RevEntryQ7Q9.md` (VERDICT: PASS); the registry-row audit `.ufo/waves/round-30/falsify/R30RevRows.md` supports the six rows, not the source claims.`
Do not write "second seats", "wave-2 reports", "falsify reports" or "by wave 2" in that cell:
`GENERIC_RE` (`:41-50`) treats them as non-evidence (probe C: `reasons: generic seat
references are not report evidence`, exit 1).

### Q13-3 — `build/` is not a second-wave directory, so the three cited reports support nothing

Failing text, lines 44-46:

> The Q10/Q13 re-read for this admission is `.ufo/waves/round-30/build/R30RevEntryQ1Q6.md` and
> `.ufo/waves/round-30/build/R30RevEntryQ7Q9.md`, both non-author seats; the registry-row audit
> is `.ufo/waves/round-30/build/R30RevRows.md`.

`is_second_wave` (`:242-243`) accepts only a directory named `falsify` or matching
`wave[-_ ]?0*\d`, so a `build/` path resolves but is dropped (`:276-279`). Probe B:

```
### B  build/ path inside the reason cell  exit=1
  cited seat-report paths: '.ufo/waves/round-30/build/R30RevEntryQ1Q6.md'
  missing: Gate does not name a valid second-seat report by path; the commit has 1 second-seat report(s)
  reasons: no cited, existing, returned second-seat report for this round
```

Existence in the commit tree is necessary but not sufficient — which is exactly what the
draft's own sentence ("so this paragraph lands only with those three reports in the same commit
tree") assumes is sufficient.

**Corrected wording (lines 44-46 replacement):**
> The Q10/Q13 re-read for this admission is `.ufo/waves/round-30/falsify/R30RevEntryQ1Q6.md` and
> `.ufo/waves/round-30/falsify/R30RevEntryQ7Q9.md`, and the row audit is
> `.ufo/waves/round-30/falsify/R30RevRows.md`; all three are read from the admitting commit, and
> `plans/gate_timing_check.py` resolves cited reports only under this round's `falsify/` wave
> (`is_second_wave`), so the `build/` copies are working copies and never the citation.

and land, in the same commit, `.ufo/waves/round-30/falsify/swarm-registry.json`:

```json
{"schema": 1, "wave": "falsify", "members": {
  "R30RevEntryQ1Q6": {"role": "reviewer", "agentId": "L1Kengaku30.R30RevEntryQ1Q6"},
  "R30RevEntryQ7Q9": {"role": "reviewer", "agentId": "L1Kengaku30.R30RevEntryQ7Q9"},
  "R30RevRows":     {"role": "reviewer", "agentId": "L1Kengaku30.R30RevRows"}}}
```

Probe A shows this shape green:

```
### A  falsify/ path inside the reason cell  exit=0
PASS line 7 Gate admit: …
  existing returned second-seat report(s): .ufo/waves/round-30/falsify/R30RevEntry.md
gate_timing_check: … admissions=1 passed=1 failed=0 second-seat-reports=1
```

The registry member key must be the report's file stem (`:331-332`), and a bare report name is
only accepted when exactly one file of that name exists in the round's second-wave dirs — probe
F, two same-named files: `reasons: … one or more bare report references do not resolve uniquely`,
exit 1. Cite full paths, never bare names.

### Q13-4 — none of the three cited reports has an anchored `VERDICT:` line

Measured on the current bytes:

```
$ grep -n '^VERDICT:' .ufo/waves/round-30/build/R30RevEntryQ1Q6.md → no match
$ grep -n '^VERDICT:' .ufo/waves/round-30/build/R30RevEntryQ7Q9.md → no match
$ grep -n '^VERDICT:' .ufo/waves/round-30/build/R30RevRows.md     → no match
```

`R30RevEntryQ7Q9.md:172` even *asks the Gate seat* for "A plain final `VERDICT: PASS|PARTIAL|FAIL`
line naming the candidate" — the requirement is stated in the report but not met by it.
Probe J (`Verdict: PASS`, mid-capitalisation) is red: `report has no anchored VERDICT line;
return is not established`. `VERDICT_RE` (`:56`) is `^VERDICT:` with `MULTILINE` and no
`IGNORECASE`.

**Corrected wording (append as the final line of each report):**

- `R30RevEntryQ1Q6.md` → `VERDICT: PASS — Q1–Q6 conformant at corpus/knowledge/contamination-transparency-card.md`
- `R30RevEntryQ7Q9.md` → `VERDICT: PASS — Q7–Q9 conformant at corpus/knowledge/contamination-transparency-card.md`
- `R30RevRows.md` → `VERDICT: PASS — six proposed rows, cell-level findings listed above`

The candidate-path half is already satisfied — occurrence counts of the literal
`corpus/knowledge/contamination-transparency-card.md` are 1 / 4 / 4 in those three files, and
probe I shows a report that names only `knowledge/…` is refused (`report does not name the
admitted candidate path`).

### Q13-5 — the header note states the opposite of what Q13 enforces

Failing text, lines 2-4:

> Column 5 is new this round. Q8 already requires a rejected candidate to carry its reason and
> flip condition, and Q13 requires the Gate cell to name each second-seat report by
> repo-relative path; adding the read pointer per row lets a later seat re-derive a verdict
> without re-running the round. Round 29's verdict rows carried their pointers inside the reason
> cell; this round keeps them addressable.

The last sentence records the move that breaks the check. **Corrected wording (lines 2-4):**

> Column 5 is new this round and carries files-and-lines only. Q8 requires a rejected candidate
> to carry its reason and flip condition; Q13 requires the **admit row's reason cell** to name
> each second-seat report by repo-relative path under this round's `falsify/` wave — the pointer
> column and the second-seat paragraph are not scanned — and the cited report must exist in the
> admitting commit tree with an anchored `VERDICT:` line. Round 29 carried its pointers inside
> the reason cell for that reason; the admit row below keeps the seat-report citation there.

## Q8 — two cells to correct

### Q8-1 — the bulk row's entry count is not the count the package records

Failing cell, line 17 col 1: `169 remaining staged rows and 69 remaining staged entries`, with
line 17 col 5 asserting the provenance:

> `MERGE-REPORT.md` (175 staged rows, 70 entries by `used-by`, first staged id S077)

The package records **65** entries, not 70: `MERGE-REPORT.md:7` — "proposed knowledge entries:
**65**"; `MERGE-REPORT.json` → `accepted` 175, `entries` 65, `existing_rows` 76. There is no
"70 entries by `used-by`" figure in either file. The row count is right: 175 − 6 rows appended
at round 29 = 169 (`corpus/lessons/round-29.md:204`, "Registry 76 → 82 rows").

**Corrected wording (line 17 col 1):**
`169 remaining staged rows and 63 remaining staged entries (65 proposed, 2 held: the round-29 validity checklist and this round's card)`

**Corrected wording (line 17 col 5, first clause):**
`MERGE-REPORT.md:7` and `MERGE-REPORT.json` (`accepted` 175, `entries` 65, `existing_rows` 76);
175 − 6 appended rows = 169, 65 − 2 held entries = 63

### Q8-2 — "nothing to flip" is not a flip condition

Failing cell, line 14 col 4:

> nothing to flip — the file is held. A future amendment arrives as an appended dated section,
> never as a replacement

Q8 requires each recorded candidate to carry "reason and flip condition"; the trigger is present
but is introduced as its own negation, which reads as "no condition".

**Corrected wording (line 14 col 4):**
`flip: a dated amendment section appended to `corpus/knowledge/benchmark-task-validity-checklist.md` that names the row it extends (Q6); a replacement copy is never the flip`

## Q9 — the cells whose reason does not follow from the property or the bytes

### Q9-1 — the admit row's Q6 sentence is narrower than the flip it discharges

Failing text, line 11 col 3:

> Q6 is satisfied by naming `contamination-detection-and-transparency.md` as the entry extended
> — the gap is recorded in the frontier bullet at `corpus/README.md:272`, which names that
> entry, and its own §Extends already points at `benchmark-selection.md`, so the card sits
> downstream of a held chain rather than beside it

Three defects in one sentence: (a) round-29's flip (a) requires naming **both** the lane entry
and the round-6 tabulation — `.ufo/waves/round-29/attempt2/build/R29a2RejectScan.md` §1, quoted at
`.ufo/waves/round-30/build/R30RevFlip.md:51-53` — and the landed entry already does name both (`corpus/knowledge/contamination-transparency-card.md:126-133`, "… and the union
table of the campaign's round-6 staging file `benchmark-card-field-schema-2026-10-23.md`
(continued, not re-derived; its rows are staged, not in this lane's registry)") — the Gate cell
under-reports its own evidence; (b) the pointer is to the **staged** copy (`_staged_
knowledge/corpus/knowledge/contamination-transparency-card.md:1-6,8-9,90`) while the entry now
exists at `corpus/knowledge/contamination-transparency-card.md` (14 955 B, sha256 `bf83bf47…`);
(c) `corpus/README.md:272` is the task-spec bullet — the card bullet is `:274` (see Q9-3).

**Corrected wording (line 11 col 3, replace that sentence):**
`Q6 is satisfied by the landed entry's §Extends (`corpus/knowledge/contamination-transparency-card.md:126-133`), which names both objects round 29's flip required — `contamination-detection-and-transparency.md` and the round-6 union table `benchmark-card-field-schema-2026-10-23.md`, continued with its staged provenance stated — and the frontier bullet it discharges is `corpus/README.md:274`.`

### Q9-2 — the admit reason repeats the retired colliding gate label

Failing text, line 11 col 3:

> Its Q1–Q8 gate is a procedure a maintainer can answer without publishing live items, …

Round-29's flip (c) is "the gate labels move off `Q1–Q8`" (`R30RevFlip.md:55`, from
`.ufo/waves/round-29/attempt2/build/R29a2RejectScan.md` §1; the surviving collision is recorded
at `R30RevFlip.md:126-131`). The landed entry did move them:
`corpus/knowledge/contamination-transparency-card.md:69` — "## The card gate — CG1–CG8" — and
`:71-72` explains the rename; `corpus/README.md:274` records the same ("labelled **CG1–CG8** in
the landed entry so they cannot be confused with `QUALITY.md` Q1–Q8"). The Gate cell asserts a
label the entry no longer carries.

**Corrected wording:**
`Its CG1–CG8 gate (`corpus/knowledge/contamination-transparency-card.md:69-72`) is a procedure a maintainer can answer without publishing live items, which is the design rule S082 forces and S083's split (public engine, hidden implementations) demonstrates.`

### Q9-3 — `corpus/README.md:272` is the wrong line

`grep -n 'Contamination transparency cards' corpus/README.md` → `274`. Line 272 is
`- **Agentic benchmark task-spec audits**…`. Any cell pointing at 272 for the card bullet names
a line that does not contain the claim. **Corrected wording:** `corpus/README.md:274` (both in
line 11 col 3 per Q9-1 and wherever else the pointer appears).

### Q9-4 — an unlabelled pointer to a file that is not in the lane tree

Failing text, line 11 col 5:

> `benchmark-card-field-schema-2026-10-23.md:65-71`

`ls corpus/knowledge/benchmark-card-field-schema-2026-10-23.md` → absent; the file exists only
in the package (`/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/`).
Every other staged pointer in the same cell is prefixed `staged`; this one is not, so it reads
as an in-tree lane path. **Corrected wording:**
`staged knowledge/corpus/knowledge/benchmark-card-field-schema-2026-10-23.md:65-71` (and, for the
lane-side relation, `corpus/knowledge/contamination-transparency-card.md:126-133`).

`lanes/kengaku/round6/DOMAIN.md:44-46` in the same cell is a read-only sibling-repo path; the
lines are correct (lines 43-46 open "So the lane's own `contamination-transparency-card.md`
should be rewritten as an **amendment to published designs**…"), but the path needs its
provenance stated the way the staged pointers have it. **Corrected wording:**
`campaign lanes/kengaku/round6/DOMAIN.md:43-46 (read-only shokuknow tree)`.

### Q9-5 — the judge row's Q6 half is the wrong property and is false in-tree

Failing text, line 12 col 3:

> Q3, and Q6 as secondary. … Q6: it and the card both name S081 in `used-by`, and one row cannot
> serve two entries when one entry lands.

Two problems. First, Q6 (`corpus/QUALITY.md:50-55`) is "extends, never duplicates or overwrites —
the entry names the existing entry or coverage row it extends"; `used-by` multiplicity is a
registry-cell relation, not Q6's property. Second, the assertion is false in this repo:
`corpus/SOURCES.md:27` (S005) has a `used-by` cell naming **two** knowledge entries plus a lesson
— `corpus/knowledge/agent-time-horizon-and-task-validity.md, corpus/lessons/round-28.md,
corpus/knowledge/webarena-task-spec-audit.md`. A rejected candidate may not be rejected on a
premise the corpus contradicts.

The Q3 half of that row is sound and stays: the 0.46 / 0.84 figures sit at staged
`judge-calibration-thresholds.md:40-42` ("Pooling raises kappa to **0.46** … against a
single-coder test–retest ceiling of **0.84**"), and no lane row for S078/S081/S087 carries kappa
in its anchor cell (`grep` count 0 for each).

**Corrected wording (line 12 col 3, replace the Q6 sentence and the lead-in):**
`Q3, and Q6 as the duplication half. Q3: … (unchanged). Q6: the entry's transferable point duplicates `corpus/knowledge/llm-judge-calibration.md:7-13` (the calibrated-judge claim the lane already holds), which is Q6's "never duplicates", not a registry relation. Registry note, not a rejection ground: S081's appended `used-by` cell names the card entry only (`corpus/SOURCES.md` S081 row, 11 cells, `status=mined`), so a second citing entry simply makes it a two-name cell — `corpus/SOURCES.md:27` (S005) already carries a three-name `used-by`, so multiplicity alone rejects nothing.`

**Corrected wording (line 12 col 4, replace "plus S081's `used-by` corrected to the single entry that lands"):**
`plus S081's `used-by` naming the card entry (the judge entry's name leaves the cell when this candidate is rejected); multiplicity itself is legal — `corpus/SOURCES.md:27``

### Q9-6 — the grader row files a row-schema defect under Q3

Failing text, line 15 col 3:

> Q3, and the row condition Q8's record rests on: round 29 rejected the state-based/tolerance
> reading as contradicted by the package's own later tabulation (16 of 108 graders reference a
> tolerance). This round re-measured the row the entry would stand on: S093 still splits into
> **12** cells with an escaped pipe (`S101` into **15**), so there is still no appendable
> registry row…

Q3 (`corpus/QUALITY.md:31-35`) is "claim stays inside its quote (≤25 words, with location)"; an
escaped pipe and a 12-cell row are the SOURCES row schema (11 columns, contract v1), which is
what round-29's reject already separated (`corpus/lessons/round-29.md:237-241`: Q3 = the 16/108
contradiction; "a schema-malformed staged row (`package-gate.txt` → `S093:escaped-pipe`)" as its
own clause). The cell merges the two under one label. The cell's measurements are correct — I
re-derived them: `SOURCES.append.md` S093 splits naively into 12 cells (11 + 1 escaped pipe),
S101 into 15 (11 + 4).

**Corrected wording (line 15 col 3, first two sentences):**
`Q3 unchanged from round 29: the state-based/tolerance reading is contradicted by the package's own later tabulation (16 of 108 graders reference a tolerance, `corpus/lessons/round-29.md:237-240`). Row schema, re-measured this round: S093 still splits into **12** cells with an escaped pipe (`S101` into **15**), so there is still no appendable registry row and the strongest half of the entry still has no home.`

### Q9-7 — the register row cites a fleet-repo path as if it were lane-relative

Failing text, line 16 col 5:

> `.ufo/waves/round-30/assimilation/quarantine-slice:1-2`; `corpus/lessons/round-29.md:182-183`;
> `.ufo/reports/round-29/kengaku.md:58-63`; …

The lane's `.ufo/reports/` holds `round-17` only; the cited file is
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-29/kengaku.md`, in the fleet repo. Its lines
58-63 say exactly what col 3 claims ("`kengaku round2 S091` → **quote-present** … real anchor at
byte 43351 … `kengaku round3 S105` → **quote-present**; the quoted Japanese text is METI's WAF
error shell…"), so only the path spelling is wrong. **Corrected wording:**
`fleet ../.ufo/reports/round-29/kengaku.md:58-63`.

The rest of that row checks out: lane `S091` is the ABC paper (`corpus/SOURCES.md` S091 row,
arXiv 2507.02825) and staged register `S091` is the NEC 技報 row (`SOURCES.append.md:21`) — the
"verdict read against the wrong row would be a false accusation" sentence is well founded.

## What the draft gets right (kept as-is)

- **Q8 structure.** One admit plus four same-package rejects, the register-slice row, the bulk
  deferral and the `considerthese` row; every non-admit row has a flip cell. Bulk deferral at
  169 rows matches 175 − 6.
- **Row 13 (card-publication-contracts) Q9 mapping is exact.** I re-verified every claim against
  the staged bytes: S126 is tier B (`arxiv.org/abs/2606.09809`), S167 tier C
  (`alphaxiv.org/zh/abs/2606.09809`), S165/S166 tier A; the quoted sentence sits at staged
  `card-publication-contracts.md:40-41` ("The Chinese channel therefore reaches the same
  structural conclusion as the English one"); and the triad's `recheck:` names S165 and S166 only
  (`:7`). Reason and flip both address Q2/Q1.
- **Row 15's cell counts** (12 / 15) are correct and reproducible by naive pipe split.
- **Row 12's Q3 measurement**: no lane anchor for S078/S081/S087 contains kappa; the figures are
  at staged `:40-42`.
- **Row 11 col 4** quotes round-29's flip verbatim: "for the card, land it as an amendment to the
  tabulated designs rather than a new design" (`corpus/lessons/round-29.md:242-243`).
- **Q13 prerequisites the worktree already meets**: the entry carries `writer: KengakuR30`
  (`corpus/knowledge/contamination-transparency-card.md:9`, and the seat ids in Q13-3's registry
  are all different), `verified-at: 2026-10-25` (`:8`), and six S081-S086 rows are in
  `corpus/SOURCES.md`.

## Residual risk and verification gaps

- **Q8 has no executable check.** No `plans/*` script parses `Rejected:` lines or Gate flip
  cells; my Q8 verdict is prose review against `corpus/QUALITY.md:61-65`, and the count defects
  (Q8-1) are exactly the class no tool would catch.
- **The reason-cell-only scan is a design limit, not a draft bug.** If the lane wants read-pointer
  columns or a second-seat paragraph to count, `plans/gate_timing_check.py` must change (a
  QUALITY change, outside this round's three claims). Until then the citation belongs in the
  reason cell.
- **"Returned" is not verifiable from bytes.** I checked existence, shape (`VERDICT:` line,
  candidate mention), registry role and writer distinctness in the *worktree*; whether a seat's
  re-read actually completed is its own claim.
- **No green run exists yet.** Everything above is worktree state at 04:35; the admitting commit
  has not been created, so Q13's commit-tree path is untested end to end. My green proof (probe A)
  is a fixture, not the lane tree.
- **Red-before/red-after pair for the lane**: after the fixes, a single run
  `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-30.md --commit <admitting commit>`
  must exit 0; the pre-fix bytes of the draft are the red state, reproduced by probes B, D, J, M.
- **CJK bound.** The draft's own limitation note is correct: S084/S085/S086 anchors tokenise to
  1-3 whitespace words, so a ≤25-*word* rule cannot bound them; sentence location is the only
  binding requirement there. Nothing in Q8/Q9/Q13 changes that.

Tool installs: none. No package manager transaction was run (pacman is paused host-wide); the
review used `git`, `grep`, `python3` and the lane's own `plans/gate_timing_check.py` in read-only
mode, with all fixtures under `/tmp/r30-RevLesson/`.

## Probe receipts

`python3 /tmp/r30-RevLesson/make_fixture.py` (repo `/tmp/r30-RevLesson/repo`, one commit per case):

| case | shape | exit |
|---|---|---|
| A | falsify-wave report path inside the reason cell | 0 |
| B | `build/` report path inside the reason cell | 1 |
| C | reason + "and the rest of the falsify wave" | 1 |
| D | citation only in a 5th read-pointer column | 1 |
| E | entry without `writer:` | 1 |
| F | bare report name, two same-named files | 1 |
| G | reject-only table | 1 |
| H | bare candidate filename | 1 |
| I | report names `knowledge/…` without `corpus/` | 1 |
| J | `Verdict: PASS` not anchored | 1 |
| K | header column `verdict` instead of `decision` | 1 |
| L | `**admit as amendment**` + a register row in the same table | 0 |
| M | candidate cell carrying `(S081 … S086)` (the draft's shape) | 1 |

Case K is worth keeping in mind for the edited table: `parse_gate_admissions` requires the header
to contain the three literal cells `candidate`, `decision`, `reason` (`:150-153`); renaming
`decision` to `verdict` makes the checker see **no admit rows at all**
(`FAIL: no admit rows in ## Gate`), which would mask every other fix.

---

# Pass 2 — the revised draft (`a4f60e21…`) and the committed lesson Gate

Second review pass, 2026-10-25, after the draft seat rebuilt the block against the landed tree.
Reviewed: `/tmp/r30-DraftGate/gate.md`, sha256
`a4f60e21dc25a8966087cd26ee7eb76206725c7a3bb438612fa5df49421fe174`, 11 341 B (the copy at
`/tmp/r30-R30DraftGate/gate.md` now holds the same 11 341 B; my 04:27 listing of that directory
was empty at the time, so pass 1's "copy absent" note described that instant, not a missing
write), **and** `corpus/lessons/round-30.md` as it now stands (124 lines, its own `## Gate` at
`:6`, the admit row at `:17`). The lesson is the artifact Q13 grades; where draft and lesson
differ, both are reported.

Landed-tree facts I re-derived before judging (all hold): entry `corpus/knowledge/contamination-transparency-card.md`
15 947 B with `CG1–CG8` at `:73` and `writer: KengakuR30`; `corpus/SOURCES.md` 88 rows with
S081 at `:107` and S086 at `:112`; `corpus/README.md` index row `:65`, card bullet `:274`,
discharge `:275`; `QUALITY.md` Q20 at `:198`; `.ufo/waves/round-30/falsify/` holds 10 reports
and a 33-member `swarm-registry.json` (roles: 12 scout, 8 reviewer, 5 critic, 5 executor,
1 mutation-tester, 1 revenger, 1 connector; `agentId: null` on all 33); `.ufo/waves/round-30/build/`
holds 35 reports.

| criterion | draft (`gate.md`) | committed lesson (`corpus/lessons/round-30.md`) |
|---|---|---|
| **Q8** | PASS on structure; row 23's count is right for its own row set (60 of 65); one stale flip cell (`nothing to flip`) | **FAIL** — the Gate table has no flip-condition cell at all; row 21's count matches neither its own rows nor the draft |
| **Q9** | PASS except the S086 FAIL citation, which the draft also carries | **FAIL** — S086 FAIL cited as support; S105 verdict contradicts the record; S091's "re-read this round" has no receipt |
| **Q13** | not gradeable (draft file); its citations name the same paths the lesson fails on | **FAIL, measured**: `admissions=1 passed=0 failed=1` on a lane-copy commit of the current bytes |

The four pass-1 Q13 blockers are genuinely closed in both artifacts: col 1 is the path alone
(`| `corpus/knowledge/contamination-transparency-card.md` |`), the admit row's **reason** cell
carries the falsify paths, the reports live under `falsify/`, and the parser's mechanism is now
described correctly ("only an **admit row's reason cell** is scanned for citations
(`audit_admission`, `:330`)"). What remains is coverage, return and substance.

## Q8-L1 — the committed Gate has no flip condition (structural, all reject rows)

Lesson header, `:15-16`:

```
|candidate|decision|reason|read|
|---|---|---|---|
```

Every non-admit row in the lesson therefore carries a reason and a reading pointer but **no flip
condition** — e.g. `:19`:

> `|card-publication-contracts.md` (package) | reject this round | a load-bearing claim rests on a tier-C mirror of a row the staging campaign already holds at tier B (Q2 tier floor) | `.ufo/waves/round-30/build/R30DraftGate.md` |`

Q8 (`corpus/QUALITY.md:61-65`) requires "reason **and flip condition**"; round 29's table had the
column (`corpus/lessons/round-29.md:177`), and the draft still has it (its header
`:14`: `| candidate | decision | reason | flip condition | read pointers |`). The lesson is a
regression against both.

**Corrected wording (lesson `:15`):**
`|candidate|decision|reason|flip condition|read|`

and the flip cells to paste, verbatim from the draft where it is already right:

- judge row: `a row carrying the kappa and ceiling figures with a located ≤25-word quote (a coder-agreement paper is the likely home); then it is a candidate for a round whose theme is judge calibration, not this one`
- contamination-mitigation row: `cite the held S001 row instead of appending a second row for one document, open S121's own bytes, and land the correction as an errata section on the held contamination entry`
- card-publication-contracts row: `cite S126 for the claim, or establish the Chinese-channel reading on its own row, and put S167 inside the re-check action`
- bulk row: `one entry per round with its own re-opened rows; the gate refuses a nonempty collision set and counts an unrequested malformed row, never appends it`
- `considerthese` row: `n/a — the criterion is landed; a workflow that satisfies it is still open`
- register rows: `a re-fetch of S105 that returns the article rather than the error shell; an actual page failure, or the anchor text disappearing from the article, for S091` (pass-1 wording, still the right one)

## Q8-L2 — the bulk row's entry count matches neither the lesson's rows nor the draft's

Lesson `:21`:

> `|remaining 63 staged entries and 169 staged rows | reject this round | …`

The lesson's own table records four of the 65 package entries outside the bulk row: the card
(admit, `:17`), judge-calibration (`:18`), contamination-mitigation (`:19`),
card-publication-contracts (`:20`). 65 − 4 = **61**, not 63. The draft records **five** — it keeps
the package's `benchmark-task-validity-checklist.md` fold row — and states "60 of the 65 staged
entries", which is right for five. 169 rows is correct (175 − the 6 appendix rows).

Correction to my pass-1 report: my "63" was the two-record subtraction (65 − round-29's checklist
− this round's card) and did not subtract this round's reject rows; the pass-1 finding (that "69"
was unsupported) stands, but the fix value depends on how many candidates the Gate records.

**Corrected wording (lesson `:21`, col 1):**
`169 remaining staged rows and 61 of the 65 staged entries (65 − 1 admitted − 3 rejected)`

— and decide explicitly whether the package's validity-checklist fold is a recorded candidate
(the draft says yes; Q8 wants it kept). If it is restored as a fifth row, the same cell reads
`60 of the 65 staged entries (65 − 1 admitted − 4 rejected)`.

**Also `:21` col 4:** `.ufo/waves/round-30/assimilation/{reg-ids,staged-ids,collisions}` is a shell
brace expression, not a path a reader or a tool resolves. Spell three paths:
`.ufo/waves/round-30/assimilation/reg-ids`, `…/staged-ids`, `…/collisions`
(the "6 id collisions" claim checks out against `collisions`, 6 lines).

## Q9-L1 — the admit row cites a report whose verdict is FAIL

Lesson `:17` (reason cell):

> … Second-seat re-reads for this admission: `.ufo/waves/round-30/falsify/R30FxEntryCompleteSet.md`
> (VERDICT line), `.ufo/waves/round-30/falsify/R30FxEntryQ1Q3.md`, … and the six per-source re-reads
> `.ufo/waves/round-30/falsify/R30FxSrcS081.md` … `.ufo/waves/round-30/falsify/R30FxSrcS086.md` …

`R30FxSrcS086.md`'s anchored verdict, `:149`:

> `VERDICT: FAIL — `corpus/knowledge/contamination-transparency-card.md` line 6 misstates its own S086 evidence (caveat measured at 30 CJK characters, stated as 23; the quoted clause sits at text-layer lines 80–81, not 78–81), and it contradicts the `S086` row of `corpus/SOURCES.md`, which states 30.`

Q13's own text forecloses leaning on presence: "Presence is not endorsement: Q9/Q10 still require
all cited findings resolved" (`corpus/QUALITY.md:108-109`). Q10 is the criterion the row claims to
discharge, so citing this report as a re-read while its findings are open is a Q9 failure, not a
formatting one.

State of the two named defects, measured now:

- **character count** — repaired: entry `:6` reads `… (1 whitespace token, 30 CJK characters,
  text-layer lines 80-81, located only on newline-unwrapped extraction)`. The "stated as 23" defect
  is gone.
- **line range** — repaired in the entry, **not** in the registry: `corpus/SOURCES.md` S086 (`:112`)
  still reads `spans extraction lines 78-81, so it is reported as located but not byte-contiguous`,
  which the FAIL says is the wrong range. This is the round-29 M97 class again — entry corrected,
  registry row not.

**Corrected wording (append to the admit row's reason cell, or to the `## Round 30 admission`
bullets):**
`R30FxSrcS086.md's FAIL (`:149`) is resolved as to the count (entry `:6` states 30 CJK characters) and open as to the line range: the entry reads 80-81 while corpus/SOURCES.md S086 still reads 78-81, so the row correction lands with the entry or the finding stays open.`

Until the row is corrected, the honest cell reads "… and the six per-source re-reads, of which
`R30FxSrcS086.md` returns FAIL on one unresolved locator (`:149`)".

## Q9-L2 — the S105 row re-decides against the record it depends on, without naming it

Lesson `:23`:

> `|register `kengaku round3 S105` (payload-absent) | unverifiable, not a fabrication | the payload is a Japanese page whose quoted text reads like a fetch-failure render; `unreachable` is not the fabrication class, and the lane appends nothing for it | `.ufo/waves/round-30/assimilation/quarantine-slice` |`

The round-29 fleet hand-check records the opposite: `fleet ../.ufo/reports/round-29/kengaku.md:60-62`
— "`kengaku round3 S105` → **quote-present**; the quoted Japanese text is METI's WAF error shell
returned to a bare client, and the row's hold-out quote is present in the 200 snapshot." The
revised draft already carries the corrected cell (`|register `kengaku round3 S105` (`payload-absent`)
| **quote-present in the archived snapshot**, not a fabrication; …|`), so the committed lesson is
the stale side. Q6's errata rule and Q9 both bite here: a re-decision must name the record it
supersedes and point at it.

**Corrected wording (lesson `:23` cols 2-4):**
`| **quote-present in the archived snapshot**, not a fabrication; supersedes round 29's "unverifiable" render | fleet ../.ufo/reports/round-29/kengaku.md:60-62; .ufo/waves/round-30/assimilation/quarantine-slice |`

## Q9-L3 — "re-read this round" for S091 has no this-round receipt

Lesson `:20`:

> `|register `kengaku round2 S091` (payload-absent) | quote-present, not a fabrication | re-opened in round 29 and re-read this round; …`

No round-30 seat re-read the register slice: `grep -rl 'kengaku round2 S091' .ufo/waves/round-30/`
returns only `.ufo/waves/round-30/build/R30DraftGate.md` and this report. The claim is unbacked in
the round it is made. **Corrected wording:** delete "and re-read this round", or name the seat and
its report path.

## Q13-L2 — measured on the real bytes: the admit row fails today

I copied the current lesson, entry and `falsify/` tree into a throwaway repo (`/tmp/r30-RevLesson/lane`,
commit `e09bc82`) and ran the checker with `--repo`, so this is the lesson's own row and the
wave's own reports, not a fixture:

```
FAIL line 17 Gate admit: candidate='corpus/knowledge/contamination-transparency-card.md'
  existing returned second-seat report(s): …/R30FxSrcS081.md, …/R30FxSrcS086.md
  invalid cited second-seat report: …/R30FxEntryCompleteSet.md (absent from commit tree)
  invalid cited second-seat report: …/R30FxEntryQ1Q3.md (absent from commit tree)
  invalid cited second-seat report: …/R30FxEntryQ4Q6.md (absent from commit tree)
  invalid cited second-seat report: …/R30FxQuotes.md (report has no anchored VERDICT line; return is not established)
  reasons: one or more cited second-seat reports fail identity/return checks
gate_timing_check: … admissions=1 passed=0 failed=1 second-seat-reports=10
```

Two of the six paths the reason cell cites qualify (`R30FxSrcS081.md`, `R30FxSrcS086.md`); the four
that fail are the three absent reports and `R30FxQuotes.md` without an anchored verdict. The
`## Round 30 admission` bullets additionally claim `.ufo/waves/round-30/falsify/R30FxEntryQ7Q9.md`
and `.ufo/waves/round-30/falsify/R30FxRowsCensus.md` as re-reads; neither file exists in the wave
either (`ls .ufo/waves/round-30/falsify/*.md` → 10 files, neither name among them), so the prose
makes the same claim the table cannot support. The lane's own audit says
the same thing independently — `.ufo/waves/round-30/falsify/R30FxDeadSeats.md:210` (A7): "at T6
(04:40:59) 1 of 8 exists … Independently, nothing of round 30 is committed, so
`plans/gate_timing_check.py` reports 'absent from commit tree' for each of the eight — file
presence alone does not discharge the citation."

Seats, not reports, are the blocker's other half: every cited stem **is** registered with an
allowed role (`R30FxEntryCompleteSet/Q1Q3/Q4Q6/Q7Q9` → `reviewer`, `R30FxQuotes`, `R30FxRowsCensus`,
`R30FxSrcS081`, `R30FxSrcS086` → `scout`), and `agentId: null` passes the identity test
(`member.agent_id == writer` is false; `:352-354`). So the wave can pass as soon as the reports
exist and return.

**Corrected wording / actions (either path works):**

1. land `R30FxEntryCompleteSet.md`, `R30FxEntryQ1Q3.md`, `R30FxEntryQ4Q6.md` and
   `R30FxRowsCensus.md` under `.ufo/waves/round-30/falsify/`, and append an anchored
   `VERDICT: PASS — corpus/knowledge/contamination-transparency-card.md` final line to
   `R30FxQuotes.md`; **or**
2. trim the admit row's reason cell to the reports that return today —
   `.ufo/waves/round-30/falsify/R30FxSrcS081.md` and `.ufo/waves/round-30/falsify/R30FxSrcS086.md` —
   and move the rest to the `## Round 30 admission` bullets as pending (they are not citations
   then, and the row passes on the two that returned).

Either way: spell `R30FxSrcS086.md` as a full path. The reason cell currently ends with a bare
`R30FxSrcS086.md`, which resolves only because exactly one file of that name exists
(`resolve_citations`, `:264-274`); a second one makes it `unresolved_bare` and red.

One caution on path 2: `R30FxSrcS086.md` is the FAIL report (Q9-L1). Citing it as one of only two
returning re-reads makes the unresolved locator the row's own evidence — resolve Q9-L1 first.

## Pass-2 residual risk

- The checker proves structure, never truth: a report with an anchored `VERDICT: PASS` and a
  candidate mention passes even if its content is wrong. Q9/Q10 judgement stays with the seats.
- My lane-copy commit is not the admitting commit; the numbers above are the worktree at 04:44
  (`falsify/` had 10 reports then; `R30FxDeadSeats.md` recorded 1 of 8 at 04:40:59). A later
  landing changes them again — re-run the command in Q13-L2 against the real commit.
- Out of my scope but adjacent, from the lane's own falsify audit and worth a seat's attention:
  `R30FxDeadSeats.md:203` (A2) finds the lesson's "Wave 2 (falsify) 34 seats" falsified by five
  independent artifacts (33), and A7's "1 of 8 exists" note above; both are lesson-body claims,
  not Gate cells, so I record them as pointers, not verdicts.

---

# Pass 3 — the axis-language claims raised by `R30FxCoverageAxis`

Triggered by the coverage-axis falsify seat (`.ufo/waves/round-30/falsify/R30FxCoverageAxis.md`,
18 374 B). Its four items are SCORECARD/claims wording, not Gate cells; I re-derived every byte it
cites, recorded the one in-scope consequence, and left the SCORECARD edits to their owner (I make
no production edits).

## What I verified (byte state at this writing)

| claim | measured |
|---|---|
| `SCORECARD.md:1022` axis cell | `**coverage** (lowest non-retired, tie-break)` — no sub-row named |
| `SCORECARD.md:1022` verdict cell | `**7 → 7 held** — real expansion on ground the lane did not hold (frontier bullet 2 *unopened lead* → amendment + CG1–CG8 gate), but the canonical coverage score stays 7 while the round-25 L0 coverage cap is open.` |
| `PROVINCE.md` round-30 section | none — `grep -n 'Round 30\|round-30' PROVINCE.md` → no match, so the rubric's "PROVINCE enumerates surfaces that resolve" leg did not move |
| `plans/round-30-claims.md:22-23` | `Frontier bullet 2 (`corpus/README.md` §Frontier, "Contamination transparency cards") moves from *unopened lead* to *core*.` |
| `corpus/README.md:275` | `*Partly discharged round 30 (2026-10-25):* … supplies the card format and the CG1–CG8 gate as an amendment to …` — no "core"; the bullet's hidden-test-governance lead stays unopened |
| counts the seat lists | registry 88 rows (tier A 79, B 7, C 2); `corpus/knowledge/` 39 files; README index rows 39 — all reproduce |
| `SCORECARD.md:1026-1031` depth clause | `depth 9 (the entry adds a field mapping against a published union table, no new instrument claim)` — "no new instrument claim" is novelty's criterion, not depth's; `SKILL.md` is unmodified (`git status` clean for `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`) |

## In-scope consequence: none in the Gate block, one errata line missing from the lesson

The Gate cells never use "core" and never claim a PROVINCE movement — `grep -n 'core\|PROVINCE'
corpus/lessons/round-30.md` has no real hit (`:85`'s match is "score") — so no Q8/Q9 cell needs
changing for this axis. What is missing is the round's own record: the frozen claim keeps a word
the landing did not earn, and the lesson carries no correction for it. That is the Q6 errata class
the lane already applies, and a frozen claim cannot be edited, so the lesson is the right surface.

**Drop-in errata (append to the lesson's `## Mistakes`, or as a `## Corrections` bullet):**

> - **Class: a frozen claim keeping a word the landing did not earn.** `plans/round-30-claims.md:22-23`
>   says frontier bullet 2 "moves from *unopened lead* to *core*"; the landed `corpus/README.md:275`
>   says "*Partly discharged round 30*", and `PROVINCE.md` has no round-30 section
>   (`grep -n 'Round 30\|round-30' PROVINCE.md` → no match, 2026-10-25), so "core" has no landed
>   referent. **Captured-by:** the coverage-axis falsify seat
>   (`.ufo/waves/round-30/falsify/R30FxCoverageAxis.md:174` — "PASS on the number; FAIL on the
>   currency word"), not the round. **Fix:** the SCORECARD C1 row reads "7 → 7 held — improved
>   (counts)" with the count list; no downstream artifact uses "core"; drop-ins at
>   `.ufo/waves/round-30/falsify/R30FxCoverageAxis.md:223-250`.

## Out of my lane, recorded so the owner can paste

- Axis cell → `**coverage (surfaces)** — lowest non-retired, tie-break; held by the open round-25 L0 cap`
  (the present cell leaves the sub-row unstated, so the row takes expansion language from
  coverage/constructs and its hold reason from coverage/surfaces).
- Verdict cell → `**7 → 7 held — improved (counts)**, number held by the open round-25 L0 coverage
  cap (still unruled)`, followed by the counts: registry 82 → 88 (tier A 76→79, B 4→7), knowledge
  files 38 → 39, index rows 38 → 39 with 39/39 parity. Keep the counts inside the cell — the
  present parenthetical is the row's only counting surface.
- Depth clause → `depth 9 (held on the depth rubric's own legs: SKILL.md is unchanged, so "a reader
  can act on SKILL.md alone" is not met, and citation resolution is unchanged; instrument criteria
  belong to novelty)`.
- Two phrases the round must not carry downstream: **"core"** (item above) and **"real expansion on
  ground the lane did not hold"** (replaced by "improved (counts)" plus the list).

These are the seat's own drop-in texts at `R30FxCoverageAxis.md:223-250`, verified against the tree;
I neither edit SCORECARD nor adjudicate the rubric — I record that the numbers behind the
replacement reproduce and that nothing in the Gate block depends on the disputed wording.
