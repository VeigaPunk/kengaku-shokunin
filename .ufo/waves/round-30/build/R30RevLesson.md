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

---

# Pass 4 — third revision (`d9699050…446c`): Q13 now passes, two statements are stale

Reviewed `/tmp/r30-DraftGate/gate.md`, sha256
`d969905086f36444029081b4efb289c12266432ce5608564b75c13493c4b446c`, 12 457 B, 5-column table
(`| candidate | decision | reason | flip condition | read pointers |`), nine data rows.

## Q13 — PASS, by the CLI, on the current wave

I took the draft's own header, separator and admit row verbatim, copied the current
`corpus/knowledge/contamination-transparency-card.md` and the current
`.ufo/waves/round-30/falsify/` (31 reports) into a throwaway repo (`/tmp/r30-RevLesson/lane2`,
commit `be475eb`), and ran the checker:

```
PASS line 7 Gate admit: candidate='corpus/knowledge/contamination-transparency-card.md'
  cited seat-report paths: '…/R30FxSrcS081.md', '…/R30FxSrcS082.md', '…/R30FxSrcS083.md', '…/R30FxSrcS084.md', '…/R30FxSrcS085.md'
  existing returned second-seat report(s): … (the same five)
gate_timing_check: … admissions=1 passed=1 failed=0 second-seat-reports=31
```

No generic reference, no bare name, candidate a valid repo path, five full-path citations, all five
seats `scout` with `agentId: null` ≠ `KengakuR30`. The four pass-1 Q13 blockers and pass-2's
coverage failure are closed on these bytes. Each cited report's verdict and candidate mention, as I
measure them independently:

| report cited | candidate-path mentions | verdict line |
|---|---|---|
| `R30FxSrcS081.md` | 3 | `VERDICT: PASS …` |
| `R30FxSrcS082.md` | 2 | `VERDICT: PASS — …` |
| `R30FxSrcS083.md` | 3 | `VERDICT: PASS — …` |
| `R30FxSrcS084.md` | 3 | `VERDICT: PASS` |
| `R30FxSrcS085.md` | 2 | `VERDICT: PASS — …` |

and the exclusions are correct as stated: `R30FxSrcS086.md` FAIL, `R30FxEntryCompleteSet.md` absent,
`R30FxEntryQ1Q3.md` / `R30FxEntryQ4Q6.md` / `R30FxEntryQ7Q9.md` FAIL, `R30FxQuotes.md` no anchored
verdict, `R30FxC3Gate.md` PASS but 0 candidate-path mentions. The draft's own discovery — that
naming a failing report in prose "as not cited" still registers it as a citation — matches the
checker's `extract_citations` (`:203-222`), which has no negative context; keeping the S086 path out
of the cell is the correct fix, and the repair note belongs in the admission bullets instead.

## Q9-12 — the S086 repair note now describes an entry that no longer exists

Draft, admit-row reason cell:

> … it repairs a number and a line range, not a quote — the entry's S086 line states 23 CJK
> characters and lines 78–81 where the seat measured 30 characters and text-layer lines 80–81, and
> `corpus/SOURCES.md:112` repeats 78–81, so the row lands only once those three cells agree.

Measured now:

- `corpus/knowledge/contamination-transparency-card.md:6` — `… (1 whitespace token, 30 CJK
  characters, text-layer lines 80-81, located only on newline-unwrapped extraction)` — **already
  repaired**; it does not say 23, and it does not say 78-81.
- `corpus/SOURCES.md` S086 (`:112`) — `… (1 whitespace token, 30 CJK characters) spans extraction
  lines 78-81, so it is reported as located but not byte-contiguous` — still the pre-repair range.

So two of the three cells already agree, and the row's own sentence would make a reader (or a later
fixer) regress the entry to 23 / 78-81. That is a Q9 failure of the reason against the evidence it
cites, and it is the only stale statement left in the row.

**Corrected wording (replace that sentence in the admit-row reason cell):**
`The sixth source's seat returned FAIL and is not cited: it repairs one locator, not a quote — the entry's S086 line already states 30 CJK characters and text-layer lines 80-81, while corpus/SOURCES.md:112 still records "spans extraction lines 78-81", so the admission lands with that row corrected to 80-81; C1's kill rule is not triggered for S086 because the FAIL report locates both quoted spans on p.1 / printed 797.`

## Q9-13 — "`used-by` names this entry alone" is false

Same cell:

> Registry delta 82 → 88: six `mined` rows at `opened=2026-10-25` whose `used-by` names this entry
> alone, no existing row changed.

Measured, all six rows: `used-by` = `corpus/knowledge/contamination-transparency-card.md,
corpus/lessons/round-30.md` — two paths each, and all 11 cells, `status=mined`, `opened=2026-10-25`.
Multiplicity is legal in this corpus (`corpus/SOURCES.md:27`, S005 names two entries and a lesson),
and C1's counter tests *contains*, so the registry delta still holds; only the word "alone" is
wrong.

**Corrected wording:**
`Registry delta 82 → 88: six `mined` rows at `opened=2026-10-25` whose `used-by` names this entry (with `corpus/lessons/round-30.md` as the second user — multiplicity is the S005 shape), no existing row changed.`

## Q10 coverage gap the row now has a candidate for

`R30FxRowsCensus.md` has landed since pass 2 and passes every test: `scout` seat, anchored
`VERDICT: PASS — S081–S086 all pass the reg…`, 8 candidate-path mentions. The row cites five
per-source seats and no schema seat, so the six-row census re-read that the lesson's
`## Round 30 admission` bullets already claim is not represented in the citation set.

**Either** add it — `.ufo/waves/round-30/falsify/R30FxRowsCensus.md` — to the reason cell (the
checker will pass; six citations, six valid), **or** state in the admission bullets why a
rows-census re-read is not a Q10 source/number re-read. Leaving the bullets citing it while the row
does not is the same split Q13 punishes.

## Pass-4 credit

- Flip cells are nonempty on all nine rows (`:17-25`), including the two register rows and the
  `considerthese` landing (`n/a — the criterion is landed; a workflow that satisfies it is still open`).
  The `nothing to flip` phrasing from pass 1 is gone.
- The counts are self-consistent for this row set: `175 − 6 = 169` rows; `65 − 1 admitted − 4 rejected
  = 60` entries, with the explicit note that the lesson's four-row set yields 61 — that is the right
  way to state a pairing requirement (pass 2's Q8-L2 fix, applied).
- Both register rows carry supersession pointers: S105 → `quote-present in the archived snapshot`
  (which matches `fleet ../.ufo/reports/round-29/kengaku.md:60-62`), S091 → re-read this round
  (still needs the seat that read it, pass 2 Q9-L3).
- The six-of-six kill-rule claim is supported by the FAIL report's own closing sentence ("Both
  quoted spans are themselves verbatim and located on p.1 / printed 797 … C1's kill rule is not
  triggered for S086").

## Pass-4 residual risk

- Every number above is a point-in-time measurement: the falsify wave grew 10 → 31 reports during
  this review, and my PASS run copies the wave as it stood. Re-run
  `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-30.md --commit <admitting sha>`
  against the commit; a later report cannot invalidate a passing row, but a later *deletion* or a
  re-run of a cited seat can.
- The checker still proves structure only. Two of the five cited PASSes could later be revised by
  their own seats; Q10 substance stays with the seats.
- The lesson is still the pass-2 bytes (4-column table, `:21` = 63, `:23` S105 unverifiable). Until
  the lesson takes this row and the flip column, the committed artifact remains the failing one, not
  the draft.

---

# Pass 5 — fourth revision (`1a74b245…abe4`): PASS, and one label the cited census inherits

Reviewed `/tmp/r30-DraftGate/gate.md`, sha256
`1a74b24584219659becde65927cb213a62a50c7280b475dee8e8001c0a04abe4`, 13 120 B measured (the seat
quoted 13 049 B; the hash is the identity that matters). Same probe as pass 4: the draft's header,
separator and admit row verbatim, the landed entry and the current 32-report `falsify/` wave in a
throwaway repo (`/tmp/r30-RevLesson/lane3`, commit `61dc33f`):

```
PASS line 7 Gate admit: candidate='corpus/knowledge/contamination-transparency-card.md'
  cited seat-report paths: '…/R30FxSrcS081.md', '…/R30FxSrcS082.md', '…/R30FxSrcS083.md', '…/R30FxSrcS084.md', '…/R30FxSrcS085.md', '…/R30FxRowsCensus.md'
  existing returned second-seat report(s): … (the same six)
gate_timing_check: … admissions=1 passed=1 failed=0 second-seat-reports=32
```

Six citations, all valid, no generic reference, no bare name. **Q13 passes on these bytes.**

The three pass-4 items are closed, verified against the tree rather than the description:

1. **S086 sentence** — the cell now reads "the entry's S086 line already states 30 CJK characters and
   text-layer lines 80-81, while `corpus/SOURCES.md:112` still records 'spans extraction lines 78-81',
   so the admission lands with that row corrected to 80-81" and credits the FAIL report with locating
   both spans ("p.1 / printed 797"). That matches the bytes I measured (`entry:6`, `SOURCES:112`), and
   it no longer proposes the regression the pass-4 wording would have caused.
2. **`used-by`** — the cell no longer says "alone": "names this entry and this lesson (a two-entry
   cell of the shape lane S005 already carries, so the counter's contains-test holds)". All six rows
   measured: two paths, 11 cells, `mined`, `opened=2026-10-25`.
3. **Census** — `R30FxRowsCensus.md` is cited and qualifies (scout, anchored `VERDICT: PASS —`, 8
   candidate-path mentions, `agentId: null`). The row and the lesson's census claim now cite the same
   artifact.

## Q9-14 — the newly cited census repeats a false label about S086

Raised by the entry's Q4/Q6 falsify seat (`R30FxEntryQ4Q6.md` §2.2). I verified the in-tree
surfaces below, and re-fetched the external byte myself rather than quoting the seat:

```
$ curl -sSL -w 'http=%{http_code} bytes=%{size_download}\n' https://www.anlp.jp/nlp2026/submit.html
http=200 bytes=31923
$ grep -c 'This work is published without peer review' …/anlp2026-submit.html
1
```

tag-stripped text, char offset 4 754 — "This work is published without peer review and is licensed
by the author(s) under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)." The negative side
also reproduces first-hand: `curl -sSL https://www.anlp.jp/nlp2025/submit.html | grep -c '査読'` →
`0`, and the same for `https://www.anlp.jp/proceedings/annual_meeting/2025/` → `0`. (The seat
reported char offset 8 970 for the same sentence; 4 754 is the tag-stripped-text offset and 16 012
is the raw-byte offset, so the three numbers differ by normalisation, not content.)

| surface | bytes |
|---|---|
| lesson Q5 cell, `corpus/lessons/round-30.md:66-67` | `Q5 pass (S082 labelled a working paper, S084 vendor documentation, S085 a self-report, S081/S082 preprints vs S083/S086 peer-reviewed)` |
| `.ufo/waves/round-30/falsify/R30FxRowsCensus.md:167` | `| S086 | A | peer-reviewed proceedings paper for its own method and caveat | **yes** |` |
| `corpus/SOURCES.md` S086 row | makes **no** review claim — cell 2 is the venue (`言語処理学会 第31回年次大会`), cell 3 `paper`, cell 4 `A`; the label is not in the registry |

Two consequences for this review:

- The Gate's admit row now cites `R30FxRowsCensus.md` as the schema re-read. Q13 is structural and
  passes, but Q10 is substantive: the cited report mislabels the review status of one of the six
  rows it audits. Citing it is still right (it is the only schema re-read that returns), provided the
  label is corrected in the same landing.
- The lesson's own `Q5 pass` claim is false as written for S086, and the peer's evidence
  (`anlp.jp/nlp2026/submit.html`: "This work is published without peer review"; no 査読 hit on the
  NLP2025 site) is the reason. Q5 is the bar row; a Gate whose reason cites a "Q5 pass" that a reader
  can falsify from the venue's own page is a Q9 failure regardless of the checker's green.

**Corrected wording (lesson Q5 cell):**
`Q5 pass (S082 labelled a working paper, S084 vendor documentation, S085 a self-report, S081/S082 preprints, S083 peer-reviewed findings paper, S086 a non-peer-reviewed annual-meeting proceedings paper — its venue publishes without review)`

**Corrected wording (`R30FxRowsCensus.md:167`, third cell):**
`non-peer-reviewed annual-meeting proceedings paper for its own method and caveat`

Neither surface is mine to edit; the lesson Q5 cell belongs to the lesson owner and the census cell
to its authoring seat. I record the bytes, the exact replacements, and the fact that the correction
must land with the admission — a later round cannot retract a label the citing report published at
landing time.

## Pass-5 residual risk

- Still point-in-time: the wave grew 31 → 32 reports between passes; re-run the CLI against the
  admitting commit (`python3 plans/gate_timing_check.py --lesson corpus/lessons/round-30.md --commit
  <sha>`).
- The checker cannot see a wrong label, a wrong number or a wrong locator; every Q5/Q9/Q10 statement
  above rests on bytes I read or on a cited seat's measurement, and I say which is which.
- The lesson remains the pass-2 bytes; the draft's paste table is the vehicle, and it now covers
  `:17`, `:21`, `:22`, `:23` and the fifth column.

---

# Pass 6 — live-byte re-verification after the owners' edits

Tree moved while this review ran (HEAD `bdcd7be`; entry sha256 `ba0465d1…`; falsify wave 33
reports). Re-measured everything my passes asserted, so the report is not a snapshot of a tree that
no longer exists.

## Q13 on live bytes: still PASS

Same probe (draft row verbatim, live entry, live wave; `/tmp/r30-RevLesson/lane4`, commit
`069d545`): `PASS … admissions=1 passed=1 failed=0 second-seat-reports=33`, six citations valid,
no generic reference, no bare name. The `writer:` line survives the entry's later edits
(`:9` = `writer: KengakuR30`).

## The four residues the coverage seat names are live — with one refinement

| # | surface | measured now |
|---|---|---|
| 1 | `plans/round-30-claims.md:22-24` | still `moves from *unopened lead* to *core*` — frozen text; `corpus/lessons/round-30.md` still has no errata (`grep -n 'Partly discharged\|core\b'` → only `:85`, the S081 URL's "score") |
| 2 | `SCORECARD.md:1026` | still `depth 9 (the entry adds a field mapping against a published union table, no new instrument claim)` — novelty's criterion holding a depth score |
| 3 | `SCORECARD.md:1022` | **verdict cell fixed** (`**7 → 7 held — improved (counts)**; axis *coverage (surfaces)*, held by the open round-25 L0 cap …`), **axis cell not** (`**coverage** (lowest non-retired, tie-break)`): the row still names two different things |
| 4 | `corpus/knowledge/contamination-transparency-card.md:120` | `- **- **Agreement is not established.**` — doubled list marker, live |

Item 1 needs one distinction: the errata line is wording I owe, not an edit. I supply the drop-in
(pass 3 §"In-scope consequence"); the lesson is not mine to write and this seat's contract forbids
production edits.

**Drop-in for item 4** (the entry's owner applies it): replace
`- **- **Agreement is not established.**` with `- **Agreement is not established.**` — the sentence
that follows is the S081 test–retest-ceiling point and reads correctly once the marker is single.

## What pass 6 changes in this review's own record

Nothing in the verdicts: Q13 passes on live bytes, Q8's remaining work is the lesson's table shape
(the draft's five-column form), Q9's remaining work is the lesson's `:21`/`:23` cells plus the
`R30FxRowsCensus.md:167` review-status label from pass 5. The residual risk from pass 5 stands
unchanged — a later wave edit can only be detected by re-running the CLI against the admitting
commit.

---

# Pass 7 — fifth revision (`0821c7e1…237d`) and the verified errata set

## Q13: PASS again, on an unchanged citation cell

`/tmp/r30-DraftGate/gate.md`, sha256 `0821c7e154965b523d70…`, 13 898 B measured (seat quoted
13 815 B). The admit row is **byte-identical** to the pass-5 row (compared programmatically), so the
green result carries over by construction; re-run to be sure (`/tmp/r30-RevLesson/lane5`, commit
`2e0b35a`):

```
gate_timing_check: … admissions=1 passed=1 failed=0 second-seat-reports=33
```

Six citations valid (SrcS081–S085, RowsCensus), no generic reference. The new bytes add one
obligation paragraph and three paste rows outside the reason cell; `R30FxEntryQ4Q6.md` appears only
in prose, which is right — a mention inside the cell would register as a failing citation.

## The label correction is mine to word and now first-hand

I re-fetched the publisher page (pass 5 records the command): `http=200 bytes=31923`, one occurrence
of "This work is published without peer review and is licensed by the author(s) under CC BY 4.0";
the 2025 call and the 2025 proceedings index contain `0` occurrences of 査読. The seat's caveat
travels with it: the stamped sentence is the **2026 (第32回)** call, so applying it to 第31回 is
series continuity, not a direct byte — and Q5 fails on either footing, because nothing in this round
supports the "peer-reviewed" label.

## Errata set the round owes — all verified in the current entry (`ba0465d1…`)

None of these is a Gate cell; every one of them is a sentence the Gate's "pass" language would
otherwise carry into the corpus. Quoted from the entry as it stands:

| # | surface | current bytes | contradiction | drop-in |
|---|---|---|---|---|
| 1 | `plans/round-30-claims.md:22-24` | `moves from *unopened lead* to *core*` | `corpus/README.md:275` says "*Partly discharged*"; no PROVINCE round-30 section | lesson errata line (pass 3 §"In-scope consequence") |
| 2 | lesson `:66` + `R30FxRowsCensus.md:167` | `S081/S082 preprints vs S083/S086 peer-reviewed`; `peer-reviewed proceedings paper …` | the venue publishes without review (pass 5 evidence) | pass 5 §Q9-14 |
| 3 | entry `:41` vs `:158` | `its three source rows are not in this lane's registry (the GEM 2026 review … is the one exception …)` vs `two of its three source rows are staged and not in this …` | the exception clause and "three" cannot both hold; `corpus/SOURCES.md:23` is S001, the GEM 2026 review, tier A, `mined` | `:41` → `two of its three source rows are not in this lane's registry (the GEM 2026 review it tabulates is the exception: registered here at tier A as S001, corpus/SOURCES.md:23)` |
| 4 | entry `:75` vs `:69` | `strata are absent from all three *tabulated* designs but present in S081's own four-field protocol` vs the R1 row's CTC v1.1 cell = `` `strata_reported` `` and its own delta cell "**already a column in one of three**" | the entry contradicts its own table two lines above | `:75` → `strata are absent from two of the three *tabulated* designs (AI Alliance, GEM § 7) but carried as `strata_reported` in CTC v1.1 and present in S081's own four-field protocol` |
| 5 | entry `:127` / `:184` vs `:144` | `no document number, no measurements, no data release`; `a programme's self-description with no measurements` | the report does carry measurement numbers — `/tmp/r30-R30SrcS085/caict.txt:1151` reads `25.8 分，但 Qwen1.5-7B 的分数却显著提升至 51.8 分`, and `:144` already qualifies it correctly | `:127` → `no document number, no data release, and no contamination measurement (it does report model scores)`; `:184` → `a programme's self-description with no contamination measurement` |
| 6 | entry `:124-125` | `card records what each stated, not a reconciled truth. Two coders filling this card need not agree; the card records` / `what each stated, not a reconciled truth.` | the phrase occurs twice in two consecutive lines; the second is a duplication fragment | keep `:124` as `… the card records what each stated, not a reconciled truth.` and delete `:125`, or rewrite it as the intended second sentence |
| 7 | entry `:120` | `- **- **Agreement is not established.**` | doubled list marker | `- **Agreement is not established.**` |

Items 3-6 are the entry owner's to fix and the entry reviewers' to re-check; 1-2 are lesson/seat
surfaces. I verified each contradiction against the current file and, for item 5, against the source
seat's own extraction (`/tmp/r30-R30SrcS085/caict.txt`), which is where the numbers are; the entry
does not quote them, so the honest statement is "no contamination measurement", not "no
measurements".

## Why this belongs in a Q8/Q9/Q13 review at all

The lesson's per-criterion cells (`:60-70`) claim `Q3 pass`, `Q4 pass`, `Q5 pass`, `Q6 pass`, and the
Gate's admit row adopts that language ("it discharges both round-29 flips at once"). A reader who
checks item 4 or 6 against the entry can falsify the "pass" without leaving the file, and Q9's rule —
a verdict whose reason does not follow from the evidence — applies to the round's own gate as much
as to a rejection. Q13's checker is green either way, which is exactly why the errata have to be
written down rather than inferred.

---

# Pass 8 — sixth revision (`2f1ac9dc…7dc6`) and a re-measured residue table

## Q13: PASS, third consecutive revision

`/tmp/r30-DraftGate/gate.md`, sha256 `2f1ac9dcb4296f26778f…`, 14 578 B (the seat's earlier 13 815 B
was `len(str)` — characters, not bytes; the 83-byte gap is the cell's CJK). The admit row compares
byte-identical to the `0821c7e1` row; probe `/tmp/r30-RevLesson/lane6`, commit `29d4b99`:

```
gate_timing_check: … admissions=1 passed=1 failed=0 second-seat-reports=33
```

## Residue table, re-measured on the entry as it now stands (`f51951d3…`)

The entry has moved three times during this review (`ba0465d1` → `a78eb18a` → `f51951d3`), so the
seats' residue lists are stale in both directions. Measured now:

| previous item | state | bytes |
|---|---|---|
| label, entry surface | **CLOSED** | `:150` — `S086 is a 言語処理学会 2025 paper that the society publishes **without peer review** (its own stamp on …`; `:152` — `non-peer-reviewed proceedings paper, not a peer-reviewed result` |
| strata (`:75` vs `:69`) | **CLOSED** | `:75` — `strata are carried by the CTC v1.1 form (`strata_reported`) and are absent from the other two tabulated …` |
| `:120` doubled marker | **CLOSED** | the line is ordinary prose now (`one genuinely new field (S2) is *not* one its source validated …`) |
| S085 "no measurements" | **CLOSED** | `grep -n 'no measurements'` → no match; `:150` carries the qualified form `numbers and score tables, but no contamination measurement, no document number and no data release` |
| label, lesson + census | **LIVE** | lesson `:66` `S083/S086 peer-reviewed`; `R30FxRowsCensus.md:167` `peer-reviewed proceedings paper …` |
| registry count `:41` vs `:160` | **LIVE** | `:41-43` `three source rows are not in this lane's registry (the GEM 2026 review it tabulates is the one exception: this lane registers that review at tier A)` against `:160` `two of its three source rows are staged and not in this …` — the exception clause and "three" cannot both stand; `corpus/SOURCES.md:23` is S001, tier A, `mined` |
| duplicated clause | **LIVE, moved one line** | `:125-126` — `… the card records what each stated, not a reconciled truth. Two coders filling this card need not agree; the card records` / `what each stated, not a reconciled truth.` |
| `plans/round-30-claims.md:22-24` "*core*" | **LIVE** | frozen text; lesson errata still owed (pass 3 wording) |

Residue count therefore drops from seven to four, and the entry's own surface is down to two cells
(`:41` and `:125-126`). The Gate block is unaffected: it cites no cell from that list, and its
admit-row language ("it discharges both round-29 flips", the counts, the six citations) is supported
by bytes I measured.

**Drop-in for `:41` (now the only numeric contradiction left):**
`two of its three source rows are not in this lane's registry (the GEM 2026 review it tabulates is the exception: this lane registers that review at tier A, corpus/SOURCES.md:23)`

---

# Pass 9 — a historical Q13 claim re-measured and corrected in mechanism

The coverage-axis seat's final report states: "at `623c1fc` the lesson cited two reports absent from
that tree, and `gate_timing_check.py` exits 0 because it parses Gate rows only." The count is right;
the mechanism is wrong, and the difference is the whole point of Q13.

Re-measured against the commit itself (`--commit` reads that tree, not the worktree):

```
$ python3 plans/gate_timing_check.py --lesson corpus/lessons/round-30.md --commit 623c1fc
PASS line 17 Gate admit: candidate='corpus/knowledge/contamination-transparency-card.md'
  cited seat-report paths: …/R30FxSrcS081.md … …/R30FxSrcS086.md   (six)
  existing returned second-seat report(s): … (the same six)
gate_timing_check: commit=623c1fc lesson=corpus/lessons/round-30.md admissions=1 passed=1 failed=0 second-seat-reports=28
```

and the citation/tree comparison at that commit:

| | count |
|---|---|
| `R30Fx*.md` names cited anywhere in the lesson | 12 |
| reports present in `623c1fc:.ufo/waves/round-30/falsify/` | 28 |
| cited names absent from the tree | **2** — `R30FxEntryCompleteSet.md`, `R30FxRowsCensus.md` |

So the two absences are real, and the checker is green because **those two names sit in the prose**
(`## Round 30 admission` bullets), while the admit row's reason cell cites six files that all exist.
`audit_admission` (`:328-370`) reads one cell, not the section. A report absent *from the cell* does
make it exit 1 — proved in pass 1 (probes B/E/I/J/M) and measured on real bytes in pass 2
(`absent from commit tree`, exit 1).

**Corrected statement for any lesson or report citing this:** at `623c1fc` the lesson cited two
reports absent from its own tree, and the checker was green because those citations were in prose —
the gate audits only the admit row's reason cell, so a citation outside that cell is not a citation
at all. Not "because it parses Gate rows only": parsing Gate rows is the precondition that makes a
missing in-cell report fail.

This is the same defect class as `R30FxDeadSeats.md:210` (A7), and it is why the pass-2 fix — move
the citation into the reason cell — was the only fix that mattered. It also means a lesson can carry
prose citations to reports that do not exist and still print a green gate; Q10's substance, not the
checker, is what catches that.

---

# Pass 10 — seventh revision (`1df94043…f44e`) and a closing rule

`/tmp/r30-DraftGate/gate.md`, sha256 `1df94043989020511d15…`, 14 656 B. The admit row is again
byte-identical to the previous revision's (compared programmatically; 2 754 characters), so the run
is the same probe with a new tree (`/tmp/r30-RevLesson/lane7`, commit `2606d27`):

```
gate_timing_check: … admissions=1 passed=1 failed=0 second-seat-reports=33
```

Live entry unchanged at `f51951d3…`, so the two entry cells stay live as pass 8 recorded: `:41`
("three source rows … (the GEM 2026 review … is the one exception …)" against `:160` "two of its
three") and `:125-126` (duplicated "not a reconciled truth"). Wave 33 reports; the six cited ones
still qualify.

**Closing rule for this review.** Three consecutive revisions (`2f1ac9dc`, `1df94043`, and the one
before) changed only text below the Gate table. My verdict is a function of two objects — the admit
row's reason cell and the cited reports in the tree — so any further revision needs from this seat
only: (a) the file hash and byte size, (b) proof that the reason cell is byte-identical, (c) the wave
size. If (b) fails, it needs a full CLI run. That is what Q13 grades; the prose below the table is
graded by Q8/Q9 against the lesson once it takes the row.

One bookkeeping note, since it recurred twice in this thread: the seat's stale `1a74b245` in its
artifact list and its `len(str)` size were both values measured differently from what they were
named as (bytes vs characters; current vs earlier revision). That is the lane's M99/target-drift
class, not a Gate defect — the fix is to record the measurement command beside each number, which is
what this review does for every figure it states.

---

# Pass 11 — identity triple verified; review closed

The draft seat closed with three identifiers and offered the cell digest as the cheaper identity
proof. I recomputed all three rather than accepting them:

```
$ sha256sum /tmp/r30-DraftGate/gate.md
1df94043989020511d156e581e318df9654377804cbb63484d46159ff91df44e  gate.md
row  chars 2754  sha256 651298ef48f0e28a…
cell chars 2061  sha256 a2396695d60e8445820a8bd7259a639778013137c28e1eb2c69cf3bf4c2c0799
```

All three match. The cell digest is comparable to the checker's own reading for a precise reason:
`split_table_row` (`plans/gate_timing_check.py:110-135`) strips each cell, so the digest must be
taken over the stripped cell — my unstripped extraction is 2 063 characters, two more, and a future
seat comparing against 2 061 without stripping would "disagree" with a digest that is right.

**Review closed for this seat.** Final state, in the terms my criteria use:

| criterion | state at close |
|---|---|
| **Q13** | PASS on the draft's admit row: live-byte probes at `069d545`, `2e0b35a`, `29d4b99`, `2606d27`, six citations (SrcS081–S085, RowsCensus) valid, no generic reference, no bare name, candidate a valid repo path, `writer: KengakuR30` in the entry |
| **Q8** | the draft's table is the correct shape (five columns, flips on all nine rows, counts 175−6=169 and 65−1−4=60 with the 61-note); the committed lesson still holds the pass-2 four-column table and `:21` = 63 |
| **Q9** | draft green except what it cannot fix from where it sits: lesson `:21`/`:23`/`:66`, `R30FxRowsCensus.md:167`, claims `:22-24` "*core*", and the entry's `:41` / `:125-126` |

Two things this review established that no checker could: a cited report with an anchored
`VERDICT: FAIL` cannot be presented as a re-read (Q13's own "presence is not endorsement"), and a
report named only in prose is never parsed as a citation — the second is why the pass-2 fix had to be
"move it into the reason cell", not "name it somewhere".

---

# Pass 12 — digest pair verified, entry status at `f51951d3`, one new lesson cell, one self-correction

## Identity pair, both verified

```
unstripped reason-cell slice  2 063 chars  sha256 5aff5d51b521284d7550ab12afaa32bc07cb7d862eb37adf5ad825c061b164c9
stripped   reason cell        2 061 chars  sha256 a2396695d60e8445820a8bd7259a639778013137c28e1eb2c69cf3bf4c2c0799
```

The 2 061 / `a2396695…` object is the one `split_table_row` (`:110-135`) passes to
`audit_admission`; the 2 063 / `5aff5d51…` slice is the same cell with the two padding spaces. Both
digests reproduce, so a future seat can tell a moved cell from its own padding.

## Entry status at the settled tip (`f51951d3…`, 194 lines)

| errata item | state | bytes |
|---|---|---|
| #4 strata | **CLOSED** | `:75` "strata are carried by the CTC v1.1 form (`strata_reported`) and are absent from the other two tabulated …" |
| #5 S085 "no measurements" | **CLOSED** | `:127-129` "carries programme numbers and score tables (p.38 prints its own figures), but no document number, no contamination measurement and no data release" |
| #7 `- **- **` marker | **CLOSED** | `:120` is ordinary prose |
| #2 review label, entry side | **CLOSED** | `:150-152` "… the society publishes **without peer review** … labelled a non-peer-reviewed proceedings paper"; the row's tier moved A → **B**, which still clears Q2's A-or-B floor |
| #3 registry count | softened, entry owner's call | `:41-42` carries the exception inline ("its three source rows are not in this lane's registry (the GEM 2026 review it tabulates is the one exception …)"); the "two non-GEM source rows" clause is at `:134`, not `:132` as reported |
| #6 duplicated clause | **LIVE** | `:125-126` repeats "Two coders filling this card need not agree; the card records what each stated, not a reconciled truth." |
| #1 claims "*core*" | **LIVE** | frozen text; lesson errata still owed |

## New lesson cell defect, and a correction to my own pass-3 figure

The lesson's Q2 cell, `:60-61`, lists the six tiers as `(S081 B, S082 B, S083 A, S084 A, S085 B,
S086 A)`. The registry says S086 is **B**:

```
$ for id in S081..S086: row tier cell
S081 B  S082 B  S083 A  S084 A  S085 B  S086 B
```

and the same lesson says so itself at `:93` — "tier A 76 → 78, tier B 4 → 8". Q2 still passes (tier
B clears the A-or-B floor), so nothing collapses; but a cell whose evidence list contradicts both the
registry and the lesson's own count sentence is a Q9 defect, and it is the kind a reader spots first.

**Drop-in (lesson `:61`):** `S085 B, S086 B)` replacing `S085 B, S086 A)`.

**Self-correction:** my pass-3 table records "registry 88 rows (tier A 79, B 7, C 2) — all
reproduce". That was measured before S086 was re-tiered and is no longer true; the current split is
**A 78 / B 8 / C 2 = 88**, which `:93` matches exactly. The coverage-axis seat's message carried the
same pre-re-tier figures (A79/B7/C2); the measurement was right when taken, the tree moved after it.
My pass-3 verdict (that the replacement wording's numbers reproduce) is unaffected — files 39 and
index rows 39 both still hold.

---

# Pass 13 — the Q6 FAIL, verified first-hand from the form

The entry's Q4/Q6 seat reports **Q6 FAIL** on two claims (S2 "only new field"; R5's mapped column)
and states its four verdicts hold. I re-derived the form evidence myself rather than crediting it:

```
$ curl -sSL https://raw.githubusercontent.com/Jangulo7/contamination-disclosure-paper/\
4dba1ed9b2ace8b71a2edcd5fa6ce0337cf08ba6/templates/disclosure.yaml
http=200 bytes=2181        # the commit the package's S123 cites
```

| form line | bytes | what it settles |
|---|---|---|
| `:2` | `# CC BY 4.0. Filled-in forms are yours; no attribution required …` | the form is **CC BY 4.0**, not CC0 — a "CC0 card" label is wrong on the artefact's own header |
| `:14` | `evaluation_date: ""  # YYYY-MM-DD` | the field R5 maps to exists, but it is the **run** date; benchmark currency is a different property |
| `:36` | `direct: "unknown"  # controlled \| not_controlled \| unknown \| n/a` | the four-value enum the entry calls "valid values" |
| `:46-47` | `boundary_integrity_monitored: ""` / `notes: ""` | the run-side integrity state is a published field |
| `:49-51` | `regeneration:` … `procedure_published: false` | R4's regeneration block exists as R4 says |
| `:38-45` | `acquired`, `network_access_during_eval`, `environment_sanitised`, `transcripts_reviewed` | the "card integrity" surface is carried by four declared fields plus a free-text `notes` |

Consequences for the lesson's cells (mine to word):

- **`:67` `Q6 pass (§Extends names both objects; the delta is stated as one field, one placement, one
  value set)`** — the §Extends half is true (entry `:126-133` for the earlier revision's numbering,
  `:158-160` now), but "one field" is the claim the form falsifies: `boundary_integrity_monitored`,
  `notes`, `acquired`, `network_access_during_eval`, `environment_sanitised`, `transcripts_reviewed`
  are all declared, and `evaluation_date` is not a currency date. Narrowing drop-in:
  `Q6 pass on the extension property (§Extends names both objects); the delta claim is narrowed to S2's tri-state reading of a run-side integrity state, which the CTC v1.1 form already declares via `boundary_integrity_monitored` + `notes` — no new field is claimed`
- **`:65` R5** — "already a column in two of three" is true of the *table* (AI Alliance carries release
  date / change log; GEM's cell is absent), but the CTC cell is populated with a **run** date
  (`evaluation_date`), so the row reads as currency when it is not. The distinction matters and I keep
  it separate from R4: the R4 row (`:66`) maps to the dedicated `regeneration:` block and is correct;
  R5's defect is the property of a populated cell, not a missing column. The artefact settles it —
  `grep -n 'date\|YYYY'` over the form returns exactly two lines, `:3` (a "Validate with" comment) and
  `:14` (`evaluation_date: ""  # YYYY-MM-DD`), and the `regeneration:` block (`:49-52`:
  `procedure_published`, `procedure_url`, `artifact_only`, `notes`) carries **no date field at all**.
  So neither R4's block nor R5's cell can supply "the date of the benchmark's last substantive
  update", and the "R4 already covers it" reply fails on the artefact. Entry-side wording, owner's
  call; I record the byte.
- **`:61` S086 A → B** from pass 12 stands; nothing here changes admission (S086 is tier B, Q2's
  floor is A-or-B).

**Blob identity, two independent fetches.** The Q4/Q6 seat fetched the same form and recorded the
digest; mine reproduces it exactly:

```
$ sha256sum ctc-disclosure.yaml
05131be9f72b333a479046a0df4510d48fd5389192d40c595869e718b5c90d0f   (2 181 bytes)
```

So the Q6 finding now rests on two seats against one artefact, not one seat's measurement — the same
standard I applied to the anlp label (pass 5).

**Citation addresses in this report are pinned.** Lesson and entry line numbers move between reviews
(the entry went `ba0465d1` → `a78eb18a` → `f51951d3` inside this thread). Every lesson/entry cell
quoted above is *as read at* commit `2dcf06c` (entry `f51951d3…`); where a later tip renumbers a cell,
the quote is the identity, not the line.

Nothing in this pass touches the Gate block: the admit row cites none of the FAIL reports, which is
correct, and its own claims are the flip discharge, the counts and the six citations — all measured.
The Q6/Q5 substance lives in the lesson's per-criterion cells, which is where the paste table already
sends corrections.
