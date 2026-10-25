# R31 defect R9 — five round-30 seat reports modified in the worktree and uncommitted

Seat: UFO-FSD reviewer, leaf. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Access date 2026-10-25. Read-only: no write command was run against the lane; the only file written
is this report. Scratch: `/tmp/r31-R31DefR9/` (five `git diff` dumps, 845 lines, < 100 KB).

Lane tip at review: `0883e72ef8474ca42ac1a54eb0273079f1507035` (`## HEAD (no branch)`).

Routed defect (R9 of `plans/round31_defects.py`): *five round-30 wave seat reports are modified in the
worktree and uncommitted.* Counter state at review time — the measurement, not a relay:

```
$ python3 plans/round31_defects.py --lane .
DEFECT R1 log-delta-correction: no appended correction quotes the superseded delta wording (only the original occurrence exists)
DEFECT R2 lesson-q6-basis: no appended erratum states the admitted Q6 basis after the retracted one
DEFECT R6 entry-staged-source-count: the entry still says three staged source rows are unregistered
DEFECT R9 round30-seat-reports-committed: .ufo/waves/round-30/build/R30DraftGate.md still differs from HEAD: M .ufo/waves/round-30/build/R30DraftGate.md
checks=10 defects=4
EXIT=1
```

`check_r9` (`plans/round31_defects.py:230-247`; its `SEAT_REPORTS` tuple is at `:54-60`) walks
`SEAT_REPORTS` in order and returns on the **first** dirty path, so the counter names
`R30DraftGate.md` even though all five are dirty; R9 stays red until all five are committed. Its
committed-blob test additionally requires the string `Pass 9` inside
`HEAD:.ufo/waves/round-30/build/R30DraftGate.md`.

## 0. Whole-diff facts

```
$ git -C . status --porcelain
 M .ufo/waves/round-30/build/R30DraftGate.md
 M .ufo/waves/round-30/build/R30RevLesson.md
 M .ufo/waves/round-30/falsify/R30FxCoverageAxis.md
 M .ufo/waves/round-30/falsify/R30FxEntryCompleteSet.md
 M .ufo/waves/round-30/falsify/R30FxEntryQ4Q6.md
 M corpus/knowledge/contamination-transparency-card.md      <- not mine: C2 repair in flight
 M plans/sources_adopt.py                                   <- not mine: C3 repair in flight
?? .ufo/waves/round-31/ … ?? corpus/evidence/round31/ ?? plans/round-31-claims.md ?? plans/round31_defects.py
```

`git diff --cached --numstat` is empty: nothing is staged. `git diff --numstat` over the five:

| path | + | − | HEAD blob (lines, bytes) | worktree blob (lines, bytes) |
|---|---|---|---|---|
| `build/R30DraftGate.md` | 56 | 12 | `1b582050…` (199, 18 452) | `3712b4d9…` (243, 21 442) |
| `build/R30RevLesson.md` | 258 | 0 | `010944f1…` (1023, 66 844) | `6abe86bf…` (1281, 83 625) |
| `falsify/R30FxCoverageAxis.md` | 105 | 56 | `be5cc396…` (368, 26 384) | `de7711fa…` (417, 29 656) |
| `falsify/R30FxEntryCompleteSet.md` | 59 | 1 | `4561030d…` (338, 32 121) | `e11974a8…` (396, 36 796) |
| `falsify/R30FxEntryQ4Q6.md` | 87 | 28 | `37f7fdd3…` (388, 32 126) | `1d2cef2a…` (447, 38 236) |

Common shape: RevLesson is a pure append (passes 8–13); the other four are in-place revisions of the
same seat's own report, re-pinned to later entry blobs. Two of them carry an explicit revision note
(`R30FxCoverageAxis.md`, "Revision note … appended in place because this report's own claims must be
true of the byte it describes"; `R30FxEntryQ4Q6.md` §0 "Bytes audited, and the drift I watched").

**Every report's new pin reproduces.** All five name the entry at `sha256
f51951d327fa0d4e9ff4157f07b012f70e175b8501c388716746dd4bac8b86eb`, 194 lines:

```
$ git show HEAD:corpus/knowledge/contamination-transparency-card.md | sha256sum
f51951d327fa0d4e9ff4157f07b012f70e175b8501c388716746dd4bac8b86eb  -
$ git show HEAD:corpus/knowledge/contamination-transparency-card.md | wc -l
194
```

So the added bytes describe the **committed** entry blob, not a worktree state — the pin is honest at
commit time even though `corpus/knowledge/contamination-transparency-card.md` has since moved in the
worktree (`eb8dacfd…`, C2's R6 repair at `:40-43`). A hash-pinned report going stale one cell later is
this lane's stated convention ("findings are pinned by blob hash, never by line").

## 1. Findings, by severity

### H1 — one unmarked cross-report divergence on the Q13 mechanism (HIGH for the round's record; not a reason to revert)

`falsify/R30FxCoverageAxis.md` (added bytes, §"Axis-adjacent integrity item") states the checker is
green on a lesson citing two absent reports **"because the tool parses Gate rows only, not the Q10
row."** `build/R30RevLesson.md` pass 9 and `build/R30DraftGate.md` pass 9 both state the narrower and
different mechanism: the two names sit in **prose outside the admit row's reason cell**, and an absent
report *inside* the cell does make the checker fail.

I settled it from the code rather than from either seat:

- `audit_admission` (`plans/gate_timing_check.py:322-385`) calls `extract_citations(admission.reason)`
  — the reason cell is the only text searched; `meta is None` → `invalid[path] = "absent from commit
  tree"` (`:343`); `ok = bool(existing) and not invalid and …` (`:379`).
- `split_table_row` (`:102-131`) `.strip()`s every cell (`:118`, `:123`), so the seats' "stripped
  cell" digest argument is mechanically correct.

Consequence: parsing Gate rows is what makes a missing in-cell report fatal; the coverage seat's causal
clause is imprecise while the outcome it reports is right. Two of the three reports carry the corrected
form, and RevLesson pass 9 names the coverage report as the object it corrects — but the coverage
report itself still carries the imprecise clause. **Committing lands a documented correction beside an
uncorrected claim.** Resolution belongs in round-31's lesson/SCORECARD (where pass 9 already puts it),
not in a post-hoc edit to another seat's verdict record.

### H2 — `R30FxEntryQ4Q6.md` §4 promises four graded states and tabulates three (MEDIUM)

Line 393: "Graded at four states: the admitted commit `623c1fc` … the intermediate worktree
`ba0465d1…`, commit `9af639c` … and the settled tip `caf1e2b`". Line 398: `| finding | 623c1fc |
ba0465d1 | tip 9af639c (a78eb18a) |` — three state columns, no `caf1e2b` column; the `caf1e2b` state
appears only inside two cells (`:403`, `:410`). The column headed `9af639c (a78eb18a)` therefore
conflates two blobs.

Related loss, not falsehood: the **committed** VERDICT asserted H4 live at `a78eb18a` (`:127`/`:184`),
and that assertion is true of that blob — `git show 9af639c:corpus/knowledge/contamination-transparency-card.md`
line 127 reads "no document number, no measurements, no data release" and line 184 "with no
measurements", so the committed report measured correctly and the revision simply stops reporting it.
The worktree's S085 row puts `—` in that column and reports closure at `caf1e2b` (`:410`). The
measurement is dropped without a supersession note, so a reader of the committed file cannot recover
that H4 was still live one blob earlier.

### H3 — two stale tree-state sentences land as committed bytes (MEDIUM, inherited)

- `falsify/R30FxEntryQ4Q6.md:39`: "The lesson itself is uncommitted (`M corpus/lessons/round-30.md`)."
  The lesson is committed and clean at HEAD (last commit touching it: `9af639c`); `git status` shows
  no `M corpus/lessons/round-30.md`. Inherited from the committed body, not introduced here, and not
  corrected by the revision.
- `build/R30DraftGate.md:139`: "The entry moved twice while this ran (`ba0465d1` → `a78eb18a`)" — under
  a section header that now pins `f51951d3` (three moves: `ba0465d1` → `a78eb18a` → `f51951d3`). This
  is the file's own named M99 target-drift class ("a value measured differently from the thing it is
  named as") reappearing in the sentence that introduces the fixed table.

Neither changes a verdict; both are record defects a reader hits before the substance.

### H4 — Q13 identity proofs rest on artifacts no reader can reach (MEDIUM, verification gap)

`build/R30DraftGate.md` and `build/R30RevLesson.md` pin the draft block's identity to
`/tmp/r30-DraftGate/gate.md` — `sha256 1df94043989020511d156e581e318df9654377804cbb63484d46159ff91df44e`,
14 656 B, row 2 754 chars `651298ef48f0e28a…`, stripped reason cell 2 061 chars
`a2396695d60e8445820a8bd7259a639778013137c28e1eb2c69cf3bf4c2c0799`, unstripped 2 063 chars
`5aff5d51…` — and to probe commits `29d4b99`, `2606d27`, `069d545`, `2e0b35a`, `be475eb`.

```
$ sha256sum /tmp/r30-DraftGate/gate.md
sha256sum: /tmp/r30-DraftGate/gate.md: No such file or directory
$ git cat-file -e 29d4b99   # likewise 2606d27 069d545 2e0b35a be475eb
absent  (all five)
```

Every digest and probe commit named by the Q13 PASS is now unreachable: the tmpfs artifact is deleted
and the probe clones are not in the lane's history. The bytes are not wrong — they are unverifiable at
review time, and a commit freezes them as the record's only proof.

### H5 — `M8`'s third grep names a file the lane does not hold (LOW; substance verified)

`falsify/R30FxEntryCompleteSet.md` §5c and `R30FxCoverageAxis.md` Addendum 2 run
`grep -c 'strata_reported|network_access_during_eval|regeneration' benchmark-card-field-schema-2026-10-23.md`
by bare relative path. No such file exists anywhere in the lane (`find . -name … -not -path "./.git/*"`
→ no result); it lives only in the read-only staged package. Re-run there:

```
$ S=/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/benchmark-card-field-schema-2026-10-23.md
$ sha256sum $S
66651007989a7fb5df4671f5f86e69ab1436517025a821afe8c451641a3533b9   (6041 B)  # = the entry's own :39 citation
strata_reported 0 | network_access_during_eval 0 | regeneration 0 | procedure_published 0
contamination_controls 1 | evaluation_date 1
```

The counts reproduce exactly as the reports state them, so M8's substance stands; only the path is
non-reproducible from the lane.

### H6 — minor citation drift (LOW)

`build/R30DraftGate.md` and `build/R30RevLesson.md` cite `split_table_row` as
`plans/gate_timing_check.py:110-135`; the function spans `:102-131` (both `cells.append("".join(cell)
.strip())` calls at `:118` and `:123`). Mechanism correct, range off by eight lines.

## 2. Per-file findings — (a) status, (b) numstat, (c) claim, (d) contradiction, (e) commit vs revert

### 2.1 `.ufo/waves/round-30/build/R30DraftGate.md`

- **(a)** ` M .ufo/waves/round-30/build/R30DraftGate.md` (unstaged; `git diff --cached` empty).
- **(b)** `56 12 .ufo/waves/round-30/build/R30DraftGate.md`.
- **(c)** The scribe's own report, revised. Claims: a **fourth** Q13 PASS on revision `2f1ac9dc`
  (probe `29d4b99`, 33 reports) in which the admit row is byte-identical to the `0821c7e1` row; final
  block `1df94043…f44e`, 14 656 B, wave 33; the pass-7 residue table re-measured at `f51951d3` with
  **4 of 7 closed** (entry label `:150-152`, strata `:75`, doubled marker `:120`, S085 "no
  measurements") and 5 live (lesson `:66`, `R30FxRowsCensus.md:167`, entry `:41-43` vs `:160`, entry
  `:125-126`, `plans/round-30-claims.md:22-24`); identity digests (row 2 754 / cell 2 061 stripped);
  a closing rule (hash + size + row/cell digests + wave size, full CLI only if the cell digest moves);
  two self-corrections (the `len(str)` figure quoted as bytes; a stale `1a74b245` in the artifact
  list); and **pass 9**, which corrects the coverage seat's mechanism claim.
  **Authorship: lane-authored evidence, not scratch** — a tracked wave seat report whose numbers I
  re-derived below. Its *identity proofs* are scratch-dependent (H4).
- **(d)** No contradiction of a committed claim that survives as a live assertion; the committed table
  (pinned `a78eb18a`) is superseded by a table pinned `f51951d3`, and the committed header's "three
  times" becomes "a fourth". Verified against bytes: entry `:150-152` carries "publishes **without peer
  review** … non-peer-reviewed proceedings paper"; `:75` "strata are carried by the CTC v1.1 form
  (`strata_reported`)"; `:125-126` still the duplicated "not a reconciled truth"; `:41` "three
  source rows are not in this lane's registry (the GEM 2026 review it tabulates is the" vs `:160`
  "two of its three source rows are staged" — the dual count is real at the pinned blob. Two internal
  defects: H3 (stale "moved twice") and H6.
- **(e)** **Commit.** The committed blob contains **zero** occurrences of `Pass 9` (`git show
  HEAD:…R30DraftGate.md | grep -c "Pass 9"` → `0`), so reverting leaves `check_r9`'s committed-blob
  test red and R9 unsatisfiable; and the worktree table is the only statement of the settled pin.

### 2.2 `.ufo/waves/round-30/build/R30RevLesson.md`

- **(a)** ` M .ufo/waves/round-30/build/R30RevLesson.md`.
- **(b)** `258 0 .ufo/waves/round-30/build/R30RevLesson.md`.
- **(c)** Pure append, passes 8–13: Q13 PASS on the third consecutive revision (`2f1ac9dc`, then
  `1df94043` at probe `2606d27`, both 33 reports); residue 7 → 4 with a drop-in for entry `:41`;
  **pass 9** correcting the coverage seat's mechanism; pass 11 recomputing the identity triple
  independently; pass 12 the digest pair, entry status at `f51951d3`, a new lesson defect (Q2 cell
  `:61` prints `S086 A` where the registry says `B`) and a **self-correction** of its own pass-3 tier
  figure (`A 79 / B 7 / C 2` → `A 78 / B 8 / C 2`); pass 13 re-deriving the Q6 FAIL first-hand from
  the pinned form (`HTTP 200`, 2 181 B, `sha256 05131be9…`) with form-line anchors (`:2` CC BY 4.0,
  `:14` `evaluation_date`, `:36` four-value enum, `:46-47` boundary keys, `:49-51` regeneration) and
  narrowing drop-ins for lesson `:67` (Q6) and `:65` (R5).
  **Authorship: lane-authored evidence** (reviewer's record), corroborated by the Q4/Q6 seat's
  independent fetch of the same blob — the two-seat standard the pass claims.
- **(d)** It **contradicts its own committed body** in exactly one place, and says so: committed
  `:674` reads "registry 88 rows (tier A 79, B 7, C 2) … all reproduce". Current registry:
  `A 78 / B 8 / C 2`, 88 rows (`awk -F'|' '/^\| S[0-9]{3} /' corpus/SOURCES.md`), matching lesson
  `:93` "tier A 76 → 78, tier B 4 → 8". The append corrects the figure with its reason (S086 was
  re-tiered at `9af639c`). This is a **marked** self-correction, not an unmarked contradiction — and
  it is an argument for committing: reverting leaves a false figure as the lane's last word.
  Verified independently: `S086` row `corpus/SOURCES.md:110` cell 5 = `B`; lesson `:61` still
  "S085 B, S086 A)". No other committed claim is contradicted.
- **(e)** **Commit.** Same reason as 2.1, plus the committed body's now-false tier figure is corrected
  only here.

### 2.3 `.ufo/waves/round-30/falsify/R30FxCoverageAxis.md`

- **(a)** ` M .ufo/waves/round-30/falsify/R30FxCoverageAxis.md`.
- **(b)** `105 56 .ufo/waves/round-30/falsify/R30FxCoverageAxis.md`.
- **(c)** The coverage seat's verdict is re-based from present-tense live to pinned-at-attack:
  "FAIL at the byte this seat attacked (`f01b7cd2…`, commit `623c1fc`) … **Live status: those cells
  were repaired**"; residue re-pinned to `caf1e2b` / entry `f51951d3`; the addendum re-derived with
  R1 strata, S1, R4 and S085 closed and `:41` vs `:160`, `:125-126`, `:74` open; **Addendum 2** — the
  CTC column's provenance (M8) with three greps; and a historical Q13 item at `623c1fc`.
  **Authorship: lane-authored evidence** (falsify seat), and its pass number reproduces:
  `python3 plans/adoption_check.py --expect .ufo/waves/round-30/adoption-expect.json --census` →
  `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok`, exit 0.
  Its historical Q13 numbers reproduce too: at `623c1fc` the lesson cites **12** distinct `R30Fx*.md`
  names, the tree holds **28** `.md` reports (+ `swarm-registry.json`), and
  `gate_timing_check.py --lesson corpus/lessons/round-30.md --commit 623c1fc` prints
  `admissions=1 passed=1 failed=0 second-seat-reports=28`, exit 0; `git cat-file -e
  623c1fc:.ufo/waves/round-30/falsify/R30FxEntryCompleteSet.md` (and `…R30FxRowsCensus.md`) fails,
  while the lesson cites them at `:31`/`:35` — in prose, outside the admit row.
- **(d)** No contradiction of a committed verdict: the committed head ("the entry's amendment delta is
  still overstated … S1's characterisation is contradicted by that form's own header") is a live
  present-tense claim about bytes that have since been repaired, and the revision converts it to a
  pinned past-tense record with a live-status line. One residual divergence: H1's mechanism clause,
  which the other two reports correct without this file being updated.
- **(e)** **Commit** (the H1 clause with it). The alternative — hold this file back until the clause is
  reworded — would keep R9 red and would leave the round's only provenance finding (M8/Addendum 2)
  unlanded; the correction already exists in the record at `R30RevLesson.md` pass 9.

### 2.4 `.ufo/waves/round-30/falsify/R30FxEntryCompleteSet.md`

- **(a)** ` M .ufo/waves/round-30/falsify/R30FxEntryCompleteSet.md`.
- **(b)** `59 1 .ufo/waves/round-30/falsify/R30FxEntryCompleteSet.md`.
- **(c)** §5c "Live-only findings at the newest blob (`f51951d3…`, HEAD `caf1e2b`)": H1 and H4 closed;
  **M7** (MEDIUM, `:74` denies the reading its own cells perform), **M8** (HIGH, provenance: three
  load-bearing CTC cells can only come from `templates/disclosure.yaml` @ `4dba1ed`, `sha256
  05131be9…`, an artefact with no registry row, while `:74` says the form "has not admitted"), **M9**
  (LOW, duplicated sentence `:125-126`), and **H3** regressed (`:41` "three" vs `:160` "two of its
  three"); a §6 later-blob delta table; and a re-based VERDICT that keeps `VERDICT: FAIL` anchored on
  the same candidate path. **Authorship: lane-authored evidence.** Verified: `SOURCES.md` has **0**
  rows matching `^\| *S12[234] *\|`; the entry has **0** hits for
  `disclosure.yaml|4dba1ed|Jangulo7|raw.githubusercontent`; the campaign table's key-name counts
  reproduce (H5); `:41`/`:160` both carry their counts at the pinned blob.
- **(d)** No contradiction of the committed verdict; the committed VERDICT named `a78eb18a` as the
  newest failing blob and asserted H4 live there — the worktree moves the failing basis to
  `f51951d3`/M8 and states H1/H4 closed, which is a supersession the §6 delta table records. The
  M8/H3 findings are new and are the substantive reason the FAIL stands at the settled pin.
- **(e)** **Commit.** Reverting would restore a verdict whose stated live basis (H4 at `:127`/`:184`)
  is no longer true of the entry and would drop the round's only HIGH provenance finding.

### 2.5 `.ufo/waves/round-30/falsify/R30FxEntryQ4Q6.md`

- **(a)** ` M .ufo/waves/round-30/falsify/R30FxEntryQ4Q6.md`.
- **(b)** `87 28 .ufo/waves/round-30/falsify/R30FxEntryQ4Q6.md`.
- **(c)** Q5 row re-scoped ("FAIL at `623c1fc`; closed in the entry at `9af639c`, open in the round's
  record"); Q6 row narrowed to S2 + R5; §0 adds a third object (tip `f51951d3`, 194 lines, "clean
  tree") and records `a78eb18a` as committed at `9af639c`; a new tier note (`S086 B`, `A 78 / B 8 /
  C 2`, lesson `:61` stale, `:134` not `:132`); R5 rewritten as *wrong property* rather than *missing
  field*, with the "R4 already covers it" rebuttal from the form's own bytes; the R1 self-contradiction
  re-dated as historical at `caf1e2b`; §4 rebuilt; §5 adds the two verified closures and the
  edit-residue class. **Authorship: lane-authored evidence**, corroborated by the lesson seat's
  independent fetch of the same form at the same commit (`sha256 05131be9…`).
  Verified anchors at the pinned blob: `:68` S2 row, `:72` "only new field", `:139` "the CC0 card",
  `:142` "bullet above.", `:186` "no contamination measurement"; `:132` is the wage-premium sentence
  and `:134` carries "two non-GEM source rows" — the report's line correction is right.
- **(d)** No contradiction of the committed *verdict* (still `VERDICT: FAIL`, same candidate). Three
  record defects: H2 (four states claimed, three tabulated; the committed `a78eb18a` H4 measurement
  replaced by `—`), H3 (the inherited "lesson itself is uncommitted" sentence, false at HEAD), and the
  §0 "clean tree" description, which is true of the entry blob but not of the worktree, where the
  entry is now `M` under C2.
- **(e)** **Commit.** Its Q4/Q6/R5 findings map onto the round-31 counter's calibration items R2 (Q6
  basis), R3 (Q2 tier cell), R5 (falsifier clause) and R7 (S2 "only new field"), and the file's own §4
  is the only finding-by-finding map of which repairs landed at which blob.

## 3. Recommendation — commit all five, revert none

**Commit, as authored, all five paths in one commit** (message naming R9), then land C2's remaining
counter items. Reasons, in order of weight:

1. **Revert cannot satisfy R9.** `check_r9` requires both a clean `git status` per path *and* the
   string `Pass 9` in `HEAD:.ufo/waves/round-30/build/R30DraftGate.md`. HEAD's blob contains `0`
   occurrences. Revert → clean status, but the second test fails with the counter's own message
   ("HEAD's R30DraftGate.md omits the pass-9 correction the worktree carried"), so R9 stays red and
   C2's frozen predicate (`defects=0`) is unreachable. Measured, not inferred.
2. **The worktree bytes are the only true-at-the-pin statements.** Reverting restores two claims that
   are now false of the committed entry: `R30RevLesson.md:674` "tier A 79, B 7, C 2" (registry is
   `A 78 / B 8 / C 2`) and `R30FxEntryCompleteSet.md`/`R30FxEntryQ4Q6.md` verdicts asserting H4 live
   at `a78eb18a` (the entry now reads "carries programme numbers and score tables … but no
   contamination measurement", `:150`). Committing replaces both with hash-pinned re-measurements.
3. **Committing cannot disturb the adoption gate.** The live admit row
   (`0883e72:corpus/lessons/round-30.md:17`) cites the six `R30FxSrcS08x.md` reports and **none** of
   the five modified files (`grep -o` over that line → no match); `gate_timing_check.py --lesson
   corpus/lessons/round-30.md --commit 0883e72` prints `admissions=1 passed=1 failed=0
   second-seat-reports=33`, exit 0. Each of the five keeps an anchored `VERDICT: FAIL —
   corpus/knowledge/contamination-transparency-card.md` line naming the candidate, so the identity and
   return checks they would be subject to still pass.
4. **The content is evidence, not scratch.** The claims I could re-derive all reproduce (entry blob
   `f51951d3…`/194 lines; `S086` tier `B`; lesson `:61` vs registry; `A 78/B 8/C 2`; the `:41`/`:160`
   dual count; `:132`/`:134`; zero `disclosure.yaml` hits; zero `S12[234]` rows; the M8 counts; the
   adoption counter line; the `623c1fc` Q13 counts and the 28/12 report numbers; the absent-report
   mechanism in `audit_admission`). What I could not re-derive is scratch-dependent (H4) or
   path-mislabelled (H5) — defects of reproducibility, not of substance.
5. **The four record defects are round-31 lesson/SCORECARD material, not edit-licence.** H1, H2, H3,
   H6 are corrections *about* seats' own records. This lane's calibration axis exists because a
   post-hoc edit to a seat's verdict record is exactly the class it penalises; the correction for H1
   already lives in the reviewing seat's report (RevLesson pass 9), which is where it belongs. My
   recommendation is therefore commit-as-authored and record, not commit-after-rewriting.

Residual decision for the integrator, stated plainly: if the integrator prefers a cleaner record, the
only defensible pre-commit change is an **appended** revision note (never a rewrite) on
`R30FxEntryQ4Q6.md` for the false "lesson itself is uncommitted" sentence and on `R30DraftGate.md` for
"moved twice". Both are within the counter's blob test (line count and `Pass 9` are unaffected), but
they are not required by R9 and I did not make them.

## 4. Residual risk and verification gaps

- **Unverifiable identity proofs (H4).** `/tmp/r30-DraftGate/gate.md` and probe commits `29d4b99`,
  `2606d27`, `069d545`, `2e0b35a`, `be475eb` are unreachable; the Q13 PASS rests on digests no future
  seat can re-derive. Committing freezes them. Mitigation available to the integrator: preserve
  `/tmp/r30-DraftGate/gate.md` under `corpus/evidence/round31/` — not done here (read-only).
- **Cross-report divergence (H1)** lands uncorrected in the coverage seat's report; the correction is
  in two sibling reports. A reader who opens only `R30FxCoverageAxis.md` gets the imprecise mechanism.
- **Entry drift.** The entry moved under C2 while I read (`f51951d3` → `eb8dacfd`); the `:41` cell the
  reports list as live is now repaired in the worktree (`:40-43` "two of its three source rows are not
  in this lane's registry (the GEM 2026 review it tabulates is the registered one)"). The five reports
  are correct about the pinned blob and will read stale on that one cell immediately after landing —
  expected under the lane's blob-pin convention, and the reports say so themselves.
- **Not re-run by me:** the round-30 `gate_timing_check` selftest and `--selftest` of
  `round31_defects.py` (out of scope for R9); the seats' Q13 probe runs on their scratch clones (the
  commits are gone); the `plans/round-30-claims.md:22-24` "*core*" item (frozen text, C2's R2/R3
  surface).
- **Tooling:** none installed or upgraded; no pacman transaction attempted (host-wide pause respected).

VERDICT: COMMIT — all five round-30 seat reports as authored; revert is ruled out by R9's committed-blob test (HEAD has 0 `Pass 9`) and would reinstate two figures false at the committed entry, while the added bytes are reproducible lane-authored evidence with four record defects (H1–H3, H6) that belong in the round-31 lesson, not in a rewrite of the seats' records.
