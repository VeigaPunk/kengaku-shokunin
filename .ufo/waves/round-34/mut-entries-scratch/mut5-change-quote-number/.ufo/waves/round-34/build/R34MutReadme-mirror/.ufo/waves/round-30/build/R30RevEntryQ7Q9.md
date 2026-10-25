# R30RevEntryQ7Q9 — the amendment entry against QUALITY Q7, Q8, Q9 and the Q10 second-seat rule

Seat: `L1Kengaku30.R30RevEntryQ7Q9` (reviewer, leaf). Access date for every source named here: 2026-10-25.
Scope: Q7 (landed + discoverable in one commit, nothing on `/tmp`), Q8 (rejections kept with reason **and**
flip), Q9 (a rejection's reason addresses the property it rejects), and the Q10 second-seat rule (what the
report must contain, and whether the current drafts satisfy it). Not re-scored here: Q1–Q6 (seat
`R30RevEntryQ1Q6`), Q11–Q19, and the C2/C3 predicates.

Draft source actually read: `/tmp/r30-DraftEntry/entry.md` **does not exist**
(`ls /tmp/r30-DraftEntry/` → `No such file or directory`), so the fallback was used:
`/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/contamination-transparency-card.md`
(92 lines, read-only). Line numbers below are that file's.

## Verdicts

| criterion | verdict | one-line ground |
|---|---|---|
| **Q7** entry + index row + coverage row in one commit, nothing on `/tmp` | **FAIL (nothing landed)** | entry absent from the lane, index row 0, no coverage-map row, S081–S086 absent from `SOURCES.md`; the only re-grounding receipts are untracked and point at `/tmp` |
| **Q8** rejections kept with reason and flip | **FAIL (no round-30 Gate exists)**, inherited round-29 record is compliant but carries two incompatible flip wordings | `corpus/lessons/round-29.md:180` + `:223-242` keep the rejection with reason and flip; there is no `corpus/lessons/round-30.md`, so the admission, the flip discharge and this round's re-screen are unrecorded |
| **Q9** reason addresses the property rejected | **PASS** for the inherited round-29 rejection (bytes verified on host); **not yet demonstrated** for round 30 | round-29's reason is a Q6 *design-standing* reason and it cites the campaign's own ruling, i.e. the same property; the amendment framing exists only in `plans/round-30-claims.md:18-22`, not in the entry bytes |
| **Q10** second seat re-reads every location and number | **FAIL (no complete-set report; one hard finding returned and unresolved)** | two single-source reports exist (S082, S084), untracked; the S082 report proves the entry's line 3 anchor is wrong and the cited URL cannot carry the quote |

## Q7 — landed and discoverable in the same commit

Measured now, on the lane tree (`/home/vgpnk/Projects/shokunin/kengaku-shokunin`, HEAD `363a4eb`):

```
$ python3 plans/adoption_check.py --lane . --expect .ufo/waves/round-30/adoption-expect.json --census
entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok
exit=1
```

Per-clause:

1. **Entry file** — absent: `ls corpus/knowledge/contamination-transparency-card.md` → *No such file*.
   The counter's `entries=0` is that fact, not a tool failure (`present` counts existing entry paths,
   `plans/adoption_check.py:72-74`).
2. **Index row** — absent: `grep -c '^| `knowledge/contamination-transparency-card.md` |' corpus/README.md`
   → `0`. The counter's `indexed` is anchored to exactly that table shape (`adoption_check.py:76-78`).
3. **Coverage-map row** — absent. `corpus/README.md:240` is the round-24 *detection-and-transparency* row;
   the Frontier bullet at `:272` ("Contamination transparency cards") still reads as an unopened lead with
   no discharge annotation (contrast the round-29 form at `:271`). C1's own surface sentence requires
   bullet 2 to move from *unopened lead* to *core*; Q7 requires the coverage-map row. Both are still owed.
4. **Registry rows** — S081–S086 are not in `corpus/SOURCES.md` (82 rows, last ids S077–S080 at lines
   100-103, S090 `:104`, S091 `:106`). So `rows_present` cannot exceed 0 this round, and `usedby_ok`
   cannot be 1 (`adoption_check.py:90-98` requires every `sources[]` id of the expectation to carry the
   entry path in its `used-by` cell).
5. **Nothing rests on `/tmp`, `local://`, or an unlanded working copy** — violated in the support layer,
   not in the entry:
   - the two re-grounding receipts that exist
     (`R30SrcS082.md:4` "Scratch + saved bytes: `/tmp/r30-R30SrcS082/`" and
     `R30SrcS084.md:12` "local path `/tmp/r30-R30SrcS084/s084.html` (scratch, outside the lane)")
     rest on `/tmp` artifacts;
   - both receipts live in `.ufo/waves/round-30/build/`, which is untracked (`git status --porcelain` →
     `?? .ufo/waves/round-30/`), and `corpus/evidence/round30/` holds only `census-before.txt`;
   - `.ufo/reports/round-30/` does not exist yet.
   Round-29's pattern is the one to copy: `corpus/evidence/round29-attempt2/` carries the committed
   counter line and the gate selftest, and each source row states URL + sha256 + quote so the digest is
   reproducible from the URL alone.

**Counter blind spot that matters for Q7.** The frozen counting command can only see the index row; it
never looks at the coverage map or the Frontier bullet (`adoption_check.py:64-80`). A tree that prints
`entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok` can still fail Q7 on
clause 3. Q7 therefore needs its own recorded check; the Gate cannot point at the C1 line as proof of Q7.

## Q8 — rejections are kept

The inherited record is compliant, and I verified it rather than trusting the claims file:

- `corpus/lessons/round-29.md:180` — Gate row, four columns, `contamination-transparency-card.md`
  (S081–S086) / `reject this round` / reason / flip `open S081–S086 in a later round as its own theme and
  pass QUALITY Q1–Q8 then`.
- `corpus/lessons/round-29.md:223-242` — `### Rejected candidates`, three candidates each with the property
  rejected on, and a closing flip paragraph: `:241-242` "for the card, land it as an amendment to the
  tabulated designs rather than a new design".

Two defects stand in the way of a clean round-30 discharge:

1. **The flip is recorded twice in two different wordings** — Gate column (`:180`) says *its own theme plus
   Q1–Q8*; the closing paragraph (`:241-242`) says *amendment, not a new design*. Round 30 satisfies both
   (S081–S086 are opened in a later round and Q1–Q8 is the card's own gate; the entry is landed as an
   amendment), but a Gate that cites only one wording leaves the other undischarged on the record. The
   round-30 Gate must name both loci and show each clause met — and must not edit `round-29.md:180` (R1:
   corrections are appended by a new dated entry naming the superseded line).
2. **Nothing is recorded yet.** There is no `corpus/lessons/round-30.md` (`ls corpus/lessons/ | tail -8`
   ends at `round-9.md` alphabetically; no round-30 file), hence no `## Gate` with the round-30 admission
   row. Q8 fires on every candidate *screened and not admitted* this round, and this round screens a large
   set: `.ufo/waves/round-30/assimilation/staged-ids` has 175 ids against 82 registered
   (`.ufo/waves/round-30/assimilation/collisions` = 6, `quarantine-slice` = the S091/S105
   `payload-absent` pair), i.e. the same *168 staged rows / 64 staged entries* population round 29 rejected
   at `:181`. The round-30 Gate needs a row for that population with reason and flip, or an explicit
   pointer that round-29's row stands and why nothing about it changed this round.

**Registry-side trap inside the staged rows.** The six staged rows
(`/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md:11-16`, 11 cells each) name five
`used-by` targets at cell 10, of which two **do not exist in this lane**:

```
judge-calibration-thresholds.md            ABSENT
cjk-eval-venue-access.md                   ABSENT
```

`judge-calibration-thresholds.md` is precisely a round-29 *rejected* candidate (`round-29.md:225-232`).
Appending the rows verbatim would land a registry assertion that a rejected entry uses S081/S084/S085/S086 —
a Q8 honesty defect (a rejection that survives in the registry as a use) and a literal-reference defect of
the Q17 class. Cell 10 must be trimmed to the admitted entry (plus any *existing* admitted entry that really
does quote the row).

## Q9 — a rejection's reason follows from its evidence

Verified against host bytes, not against the claims file's paraphrase:

- `lanes/kengaku/round6/DOMAIN.md:43-45` (read-only, `shokuknow`) reads: "So the lane's own
  `contamination-transparency-card.md` should be rewritten as an **amendment to published designs** rather
  than as a rival invention."
- `merge/kengaku/knowledge/corpus/knowledge/benchmark-card-field-schema-2026-10-23.md:65-71` states "Six
  rounds of searching have now produced three published designs" and opens the three-column comparison
  table at line 71.

The round-29 reason asserts a **Q6 design-standing** property ("fourth card design … amendment, not a
rival") and cites evidence about exactly that property. This is not M21's shape (contamination evidence
produced against a validity claim); the property matches. **Q9 passes for the inherited rejection**, with
one locator nit: the pointer `benchmark-card-field-schema-2026-10-23.md:71` lands on the table header,
while the phrase "three published designs" is at 68-69. Pointer precision, not property mismatch.

**Where round 30 can still fail Q9.** The reason for *admitting* must address the property the rejection
rejected. Two facts make that a live risk:

- The amendment framing exists **only** in `plans/round-30-claims.md:18-22`. The entry bytes do not claim
  it: line 90 says the "admission of the card against the lane's existing
  `knowledge/contamination-detection-and-transparency.md` vocabulary is the lane's call, not this entry's",
  and the only other mention of that entry is the quoted frontier gap at line 13. Nothing in the file says
  "this amends `contamination-detection-and-transparency.md`".
- A Gate reason of the form "six sources were re-opened 2026-10-25" answers the *secondary* round-29
  objection (stale campaign `opened` dates) and not the primary one (design standing). Recording that as
  the discharge would be a correct verdict with a reason that does not address the rejected property —
  the Q9 failure mode itself. The Gate reason must state the design-standing clause *and* the re-opening,
  or the entry must carry the amendment sentence so the reason has bytes to point at.

## Q10 — what the second-seat report must contain for this admission

Q10 is a content rule; Q13/Q14/Q15/Q16 are the landing rules that decide whether a report counts. For this
admission, one qualifying report (or a set that is explicitly stitched into one complete re-read) must
contain all of:

1. **Identity.** A registered seat id, not the entry's writer; role in exactly `reviewer`, `scout`,
   `critic`, `sentinel`, `revenger` (Q14); a `writer:` line naming the candidate's writer that differs from
   the seat; no author/writer declaration equal to the entry writer (Q14 rejects the report otherwise).
2. **Candidate binding.** The SHA256 (and path) of the **final** entry bytes it read, so a later byte change
   voids it. Round-29's precedent bound `c4412f67…` in `FEntrySources.md` / `FEntryNumbers.md` and treated
   earlier PARTIAL/PASS sections as historical. Because this amendment must change `verified-at:`,
   `recheck:`, line 3's locator and the amendment sentence, **any re-read taken today binds bytes that will
   be edited** — the report must be re-taken after the last edit.
3. **Every cited source re-opened by that seat, on 2026-10-25**: S081, S082, S083, S084, S085, S086 — plus
   S077 if the entry keeps it (see 5). Per source: URL actually fetched, HTTP status, byte count, sha256,
   the quoted run as a **byte substring** with its location (section/table/line/byte offset), and the
   whitespace word count ≤25.
4. **Every number re-derived against the source**, exact cells or a stated range (never "~"). For these
   bytes that means at minimum: S081's field ids `F1`–`F4` and type ids `t1`–`t4`/`t5`; S083's DOI
   `10.18653/v1/2026.findings-eacl.353` and the EACL 2026 Findings venue; S084's version `0.4.0`, the
   two documented methods and the five named datasets (GSM8K; C-Eval, MMLU, HellaSwag, ARC); S085's
   `2024年6月`, the "three parts" decomposition (`测试数据标签化管理、动态测试数据库和高质量测试数据抽样算法`); S086's
   `第31回` and `p. 797`; and the entry's own source-role arithmetic at lines 16-18 ("one formal protocol …
   one governance argument … one maintainer-engineering example … two detector implementations" = five of
   the six, with S085 handled separately at lines 79-88).
5. **The seventh-source question answered.** Line 54 cites **S077** ("canary, per task") in the body. It is
   not on a `source:` line, so `adoption_check.py`'s `SOURCE_LINE_RE` (`:34`) will still print
   `cited_rows=6` — the counter cannot see it. Q10 says "each cited source": either the report re-opens
   S077 too (and the admitting commit adds the entry to S077's `used-by`, which is this round's D5 shape,
   the S091 asymmetry), or the parenthetical is dropped. Silence here means a cited source with no Q10
   coverage while the Gate claims `cited_rows=6`.
6. **A plain final `VERDICT: PASS|PARTIAL|FAIL` line naming the candidate**, with each finding either
   resolved in the entry or routed with a line reference — presence is not endorsement (Q13), Q9/Q10
   require the findings resolved.
7. **Landing.** The report is a nonempty regular file, at a repo-relative path, present **in the admitting
   commit's own tree**, and named exactly by that path in the Gate cell (Q13/Q14: a generic reference
   supports nothing; Q15/Q16: a working-copy-only report cannot make the commit count; a report added in a
   later commit does not count). Reports under `.ufo/waves/round-30/build/` become citable only once
   committed with the admission.
8. **Two reports are allowed** — one for locations, one for numbers — but each must be a *complete* set
   read. Six per-source scout reports are not a substitute unless a stitched report covers every quote
   location **and** every number; Q14's wording ("a connector's overlap advice or a mutation test is not
   the complete source/number re-read") is the family this falls into.

### Does the current draft satisfy Q10?

**No.** Measured:

- No complete-set report exists. Two single-source reports have landed —
  `.ufo/waves/round-30/build/R30SrcS082.md` and `R30SrcS084.md` — each covering its own source only, each
  untracked. Four of six sources have no returned report at all.
- **The S082 report returns a hard finding the entry has not absorbed.** Entry line 3 cites
  `https://arxiv.org/abs/2607.01254` with anchor `` `# Benchmark Governance` ``. The seat's section map
  (§1–§9, `R30SrcS082.md:18`) contains no section of that name, and the abstract page contains **zero**
  occurrences of `transparency` (`R30SrcS082.md:92-103`, the `transparency` row at `:102`), so the cited URL
  cannot carry either body quote.
  The quotes live in `https://arxiv.org/html/2607.01254v2` at lines 855 and 901 (`R30SrcS082.md:34-71`,
  sections 3 and 4),
  PDF pages 20 and 23. Q10's "every quote location" is therefore **unconfirmed for S082** until line 3 is
  corrected. This is the class of defect Q10 exists to catch (round-24 M22).
- The S084 report **confirms** all three S084 quotes as single-occurrence byte substrings (offsets 17813,
  25836, 13768) and independently flags the `verified-at: 2026-10-23` line (`R30SrcS084.md:73`) — i.e. it
  agrees with the Q7 finding above. It also warns that the full target-(b) sentence straddles an inline
  `<a>` tag and would fail a byte-substring gate, and that tag-stripped text is needed on the C3 side
  (`R30SrcS084.md:71`) — relayed here because it is C3-adjacent fact, not my verdict.
- Neither report is bound to a candidate SHA256 of the entry bytes, and both read the *staged* copy, so
  neither can serve as the admission-time re-read even after the anchor fix.

## What the admitting commit must still add

Ordered; every item is a Q7/Q8/Q10 gate item, and all of them must be in **one** commit.

1. `corpus/knowledge/contamination-transparency-card.md` — the card bytes, amended so that:
   a. line 3 cites the full-text artefact that actually carries the quotes
      (`https://arxiv.org/html/2607.01254v2`, §7.3 line 855 / §8.2 line 901, or PDF p. 20 / p. 23);
   b. `verified-at: 2026-10-25` and `recheck: … (ran 2026-10-25)` (line 8-9 now read `2026-10-23`);
   c. one sentence names the extent: this entry **amends** `knowledge/contamination-detection-and-transparency.md`
      and the Frontier bullet it grew from — the sentence the round-29 flip asked for, currently missing
      (line 90 defers it);
   d. the S077 decision from §5 of this report is applied;
   e. no `/tmp`, `local://` or external-repo path appears in the silence.
2. `corpus/SOURCES.md` — six rows S081–S086 appended before the entry is cited: `status=mined`,
   `opened=2026-10-25` (the staged cells say `2026-10-23`, `SOURCES.append.md:11-16` cell 8), `recheck` with
   the 2026-10-25 run date, anchors replaced by the located quote forms, and `used-by
   corpus/knowledge/contamination-transparency-card.md` **only** — the staged cell 10's
   `judge-calibration-thresholds.md` and `cjk-eval-venue-access.md` are both ABSENT in this lane and the
   first is a round-29 rejected candidate.
3. `corpus/README.md` — the index row in the knowledge table, exactly
   `` | `knowledge/contamination-transparency-card.md` | … | S081–S086 … | `` (the shape the counter's
   `:76-78` regex requires, and the shape of `:56`/`:64`).
4. `corpus/README.md` — the **coverage-map row** (Q7's third artefact; the counter cannot see it) plus the
   dated "partly discharged round 30" sub-bullet under Frontier bullet 2 (`:272`), in the form used at
   `:271`.
5. `corpus/evidence/round30-sources/` — per-source receipts for S081–S086 with URL, access date
   2026-10-25, HTTP status, byte count, sha256, the located quote, and its location/offset. Support must be
   reproducible from the URL and digest, not from a `/tmp` file (the two existing receipts' `/tmp` paths
   are exactly what Q7 forbids).
6. The Q10 second-seat report(s) from §Q10 items 1–6, at a repo-relative path, cited by that path in the
   Gate cell, with the S082 anchor finding marked resolved.
7. `corpus/lessons/round-30.md` with `## Gate`, four columns (`candidate | decision | reason | flip
   condition`), containing: the amendment admission whose reason states the design-standing clause **and**
   the 2026-10-25 re-opening; an explicit discharge line naming both round-29 flip loci (`round-29.md:180`
   and `:241-242`); and rows for every candidate screened this round and not admitted — at minimum the
   175-id / 168-row staged population (`.ufo/waves/round-30/assimilation/staged-ids`, `collisions`,
   `quarantine-slice`) and any re-screen of `judge-calibration-thresholds.md` /
   `benchmark-grader-semantics.md` — each with reason and flip condition.
8. A Q7 check the frozen counter cannot perform, recorded in the Gate: anchored greps proving the index row
   and the coverage-map row exist in the same tree as the entry
   (`grep -c '^| `knowledge/contamination-transparency-card.md` |' corpus/README.md` → 1, and the coverage
   bullet), since `adoption_check.py` only proves `indexed`.
9. One commit for 1–8, with no round-owned path left untracked (R2), and no rewrite of `round-29.md:180`
   (R1).

## Residual risk and verification gaps

- I did not fetch S081–S086 myself. My Q9 property-match uses host bytes (campaign `DOMAIN.md`, the staged
  entry, the staged rows, the round-29 lesson) and the two seat reports; Q10's byte-level confirmation is
  the designated seat's job, not mine. Four of six sources have no returned re-read at the time of this
  report, so their quote locations are **unrun**, i.e. not passed.
- Q7's "same commit" can only be settled at commit time. My verdict is a pre-landing FAIL with the adds
  enumerated above; a later tree cannot retroactively make an early commit compliant (Q15/Q16).
- The round-29 flip's two wordings may be intended as one condition split across a table cell and a
  paragraph. I recorded them as two loci to discharge rather than resolving the authorial intent; the
  Gate's discharge line is where that must be settled.
- Deadlines and tooling: no installs or upgrades were performed for this seat; `curl`, `python3`, `grep`
  from the host were sufficient, and no pacman transaction was attempted. Scratch, if any, under
  `/tmp/r30-R30RevEntryQ7Q9/`; this file is my only lane write.
