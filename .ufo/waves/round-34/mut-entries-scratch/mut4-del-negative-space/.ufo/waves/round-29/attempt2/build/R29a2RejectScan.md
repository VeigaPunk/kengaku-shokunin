# R29a2 RejectScan — three staged entries scored for rejection

Seat: `L1Kengaku29.R29a2RejectScan` (scout, leaf — no dispatch, no production edits).
Date: 2026-10-25. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (read-only).
Staged tree: `/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/` (read-only).
Advisory only: this seat does not integrate, does not judge the round, and does not write
`corpus/lessons/round-29.md`. Every claim below carries a `file:line` or a command+output.

## Verdicts

| # | staged entry | verdict | landable this round? |
|---|---|---|---|
| 1 | `contamination-transparency-card.md` | **REJECT** | no — 6/6 sources last opened 2026-10-23, 0 re-open seats |
| 2 | `judge-calibration-thresholds.md` | **REJECT** | no — S081/S087 last opened 2026-10-23, 0 re-open seats |
| 3 | `benchmark-grader-semantics.md` | **REJECT** | no — S093 row is schema-malformed; S093/S094/S097 last opened 2026-10-23 |

All three are inside kengaku's province. No rejection here is a province rejection, and none
is a quality-of-thinking rejection: each is rejected on the specific property named under
"Reason (property)" (QUALITY Q9).

---

## 1. `contamination-transparency-card.md` — REJECT

**Ground it maps to.** The lane does *not* hold a card format; the card lead is open frontier,
named in `corpus/README.md:260` ("the lane has no standard card format recording detector
access, tier tested, and what a negative cannot rule out … draft a card template"). What is
already held, and what the entry would duplicate:

- Duplicated (lane): `corpus/knowledge/contamination-detection-and-transparency.md:7-13`
  (Claim — detector family, access, tier scope, transparency record) and `:70` (apply row
  "Name detector family, model access … contamination tier tested (T1–T4), and what a negative
  cannot rule out"). The entry's Q1/Q2/Q3/Q4 answers restate that row; the entry adds no new
  vocabulary over it.
- Duplicated (same merge package, later round): `benchmark-card-field-schema-2026-10-23.md:71`
  tabulates three *published* card designs ("Lane's proposed field | AI Alliance template |
  CTC v1.1 form | GEM § 7 Table 3"). The campaign's own recorded rule is
  `lanes/kengaku/round6/DOMAIN.md:43-46`: the lane's `contamination-transparency-card.md`
  "should be rewritten as an **amendment to published designs** rather than as a rival
  invention. The round-6 entry `benchmark-card-field-schema-2026-10-23.md` does that and
  tabulates the union of the three field sets" (same finding at
  `lanes/kengaku/round6/KNOWLEDGE-PROPOSED.md:82-101`).
- Registry seam: `S077` is cited inside the body at `:54` ("S077 (canary, per task)") but is
  absent from the entry's own `source:` triad at `:2-7`, which lists S081–S086 only — so
  `plans/adoption_check.py`'s `SOURCE_LINE_RE` (source-line-only) would under-count, and
  S077's `used-by` (SOURCES.append.md: bench entry only) would omit this citer.
- Label collision: the entry's gate is named "Q1–Q8" (`:45`, `:47`). In this lane that range
  is already the admission bar — `corpus/QUALITY.md:15` (Q1) through `:61` (Q8), now extended
  to Q18 at `:179`. Two different Q1–Q8 in one corpus is an operability defect, and
  `corpus/README.md:260`'s "gate a knowledge entry on Q1–Q8" predates Q9–Q18.

**Province verdict:** inside. Contamination measurement/disclosure for LLM benchmarks is core
`PROVINCE.md` scope ("LLM/model research & evaluation"); it is not a web property, not a
serving-plane question, not chousa's method.

**Source status:** six sources S081–S086, every one `status=mined opened=2026-10-23` in
`merge/kengaku/SOURCES.append.md` (parsed: S081,S082,S083,S084,S085,S086 all `opened=2026-10-23`).
None is in this round's frozen re-open set (`plans/round-29-attempt2-claims.md:33-36`:
S077/S078/S079/S080/S090), and no seat is re-opening them
(`grep -ln 'S081\|S082\|S083\|S084\|S085\|S086\|S087\|S093\|S094\|S097' *.md` in
`.ufo/waves/round-29/attempt2/build/` → no output, exit 1).

**Reason (property): the entry's scope claim over the card's published ground.** It asserts a
card *design* is needed and offers its own, while its own campaign records that three published
designs already exist and that this file must be an amendment to them, not a rival. Rejected on
Q6 (extends, never duplicates or overwrites) — the entry has no `Extends`/`## Extends` section
at all (headings: `:20`, `:62`, `:79`) and its `ground:` line at `:90` explicitly declines the
extension ("the *admission* of the card … is the lane's call, not this entry's"). Predicate
sources, not efficacy or province, are the secondary ground (Q1).

**Flip condition:** admit only when (a) the file is rewritten as an amendment section naming
`benchmark-card-field-schema-2026-10-23.md` and `contamination-detection-and-transparency.md` as
what it extends, keeping the union-of-three-designs table rather than a fourth design; (b) all
of S081–S086 **and** S077 are re-opened on 2026-10-25 with a ≤25-word located quote each and the
`source:` header lists every id the body cites; (c) the gate labels move off `Q1–Q8`; and (d) a
second seat (Q10) re-reads each quote/location. If the L1 wants the card ground this round, the
cheaper route is that the C1 checklist entry not be stretched to cover it — the merge package's
later field-schema entry is the correct carrier.

---

## 2. `judge-calibration-thresholds.md` — REJECT (narrow)

**Ground it maps to.** The lane holds the entry's load-bearing transferable point already:

- "a judge score is an estimate whose error must be measured against a human reference"
  (`judge-calibration-thresholds.md:29-30`) ≡ `corpus/knowledge/llm-judge-calibration.md:7-13`
  (Claim: "a defensible report calibrates on human labels and carries uncertainty from both the
  test cases and the calibration cases") and the apply row at `:70` ("Estimate sensitivity and
  specificity on a human-labeled calibration set; report corrected fraction with CIs carrying
  both uncertainty sources").
- The entry's third rule and its stated gap are wrong against lane bytes. It says
  (`:56-57`) "The lane's existing entries record intervals; adding the pre-registered threshold
  and the ceiling to the attribution receipt is the natural next step." The pre-registered
  threshold is already held and enforced: `corpus/QUALITY.md:82` (Q11, "a pass bar is
  interval-gated … exact two-sided 95% Clopper–Pearson lower bound at or above the bar";
  Q12 at `:90`) and `corpus/knowledge/attribution-interval-calibration.md:12` ("the
  pre-registered rule (PASS iff lower ≥ bar, FAIL iff upper < bar, INDETERMINATE otherwise,
  UNTESTED iff n = 0; `plans/round-25-claims.md`)"). The entry therefore widens an open gap the
  lane closed in round 25.
- Genuinely unheld residual: per-variable rather than pooled reporting, and a published
  test–retest **ceiling** (`grep -rn 'kappa' corpus/knowledge/*.md` → 0 hits; no ceiling concept
  in the lane). That residual is real but is one sentence of the entry, not its frame.

**Province verdict:** inside. Judge calibration is an existing lane cover row
(`corpus/README.md` coverage-map, "Judge calibration: covered at source-digest depth (round 24) —
knowledge/llm-judge-calibration.md; sources S009–S012") and `PROVINCE.md` §Round29 keeps
"hosted judges" open.

**Source status:** S078 is in this round's re-open set; **S081 and S087 are not** — both
`opened=2026-10-23` in `merge/kengaku/SOURCES.append.md`, and no round-29 seat touches them
(the same build-directory grep above returns no output, exit 1). The entry's
heaviest numbers all come from S081 (per-variable kappa 0.00–0.35, median 0.21, 29 main-pass
documents, ceiling 0.84, pooled 0.46, observed agreement 0.759, pre-registered 0.6 on AC2) —
seven quantities, none re-read this round by any seat.

**Reason (property): the entry's premise about the lane's current state.** The claim it is built
to justify — that the pre-registered threshold is missing inward — is false against the lane's
own admission bar and round-25 instrument; a claim may narrow its sources, never widen the gap
(Q3), and an entry that re-supplies held ground without naming the entry it extends fails Q6
(no `Extends` section; headings `:18`, `:72` only). Secondary: S081/S087 un-re-grounded (Q1) with
seven Q10-relevant numbers and no second seat.

**Flip condition:** admit only a rewritten, narrower entry that (a) keeps the two genuinely new
clauses — per-variable reporting and the published test–retest ceiling — and deletes the
"threshold is next" premise, citing `QUALITY.md:82` and
`attribution-interval-calibration.md:12` as where the threshold already lives; (b) names
`llm-judge-calibration.md` as the entry it extends; (c) re-opens S081 and S087 on 2026-10-25 with
≤25-word located quotes in `source:` and in the Gate, S078's quote being the one this round's
S078 seats locate; (d) a reviewer seat re-reads each of the seven numbers (Q10) — a
`PASS`-shaped claim about kappa against a ceiling additionally needs Q11/Q12 interval form.
Dropping the ceiling clause leaves nothing this round can carry.

---

## 3. `benchmark-grader-semantics.md` — REJECT

**Ground it maps to.** Unheld but contested frontier, and the entry's second half overruns its
source:

- Frontier: `corpus/README.md:259` ("the lane has no instrument that audits a benchmark's task
  specs, graders, and contamination separately. Next source/instrument: the primary specs and
  scoring code for Terminal-Bench 2.0, Toolathlon, and SWE-bench Pro"). This is the same bullet
  the frozen C1 entry `corpus/knowledge/benchmark-task-validity-checklist.md` fills this round —
  the frozen expectation lists exactly one entry
  (`.ufo/waves/round-29/attempt2/adoption-expect.json`, `entries[0].path =
  "corpus/knowledge/benchmark-task-validity-checklist.md"`).
- Lane-adjacent held ground: `corpus/knowledge/agent-time-horizon-and-task-validity.md:19`
  already carries the S006 self-report on SWE-bench Pro task breakage; the grader *mechanics*
  for these two benchmarks are the unheld part.
- In-package duplication: `benchmark-verifier-execution-model.md:8-31` already covers the
  verifier execution model (shared vs `environment_mode = "separate"`) for the same benchmarks,
  and S093's `used-by` names both entries — the two entries straddle one ground. Round 3 records
  the same overlap as an amendment: `lanes/kengaku/round3/KNOWLEDGE-PROPOSED.md:145`
  ("Amends the lane's staged `benchmark-verifier-execution-model.md` and
  `benchmark-grader-semantics.md`").

**Province verdict:** inside. Benchmark grader/scoring-code interpretation is core; the
`webarena-task-spec-audit` precedent (`PROVINCE.md` §Round28) holds the same class of ground,
and §Round29 explicitly keeps "named Terminal-Bench/Toolathlon/SWE-bench Pro specs … runtime
task validity" open.

**Source status:** S093, S094, S097 — all `status=mined opened=2026-10-23`; **none** in the
frozen re-open set and **no** round-29 seat on them. S093 additionally fails the round's own
staged-row schema: `.ufo/waves/round-29/attempt2/package-gate.txt:2` reports
`malformed: S093:escaped-pipe` (the anchor cell contains `all_required = fail_to_pass \| pass_to_pass`;
row parses to 12 cells under an escape-aware split, 11 columns required —
`plans/sources_adopt.py:14`, `:70` return `"escaped-pipe"` and refuse). So the entry's
SWE-bench Pro half has **no appendable registry row** this round, independent of its prose.

**Reason (property): the scope of the generalization it asserts from one task.** The entry
generalizes "Toolathlon — state-based, deterministic, with a tolerance" (`:62-72`) from a single
grader, `tasks/finalpool/ab-testing/evaluation/main.py` (S094). The package's own later
tabulation of the same repository contradicts that as a benchmark-level property:
`toolathlon-grader-contract-2026-10-23.md:6` ("tabulated across all 108 graders") and `:31`
("graders referencing a tolerance parameter | **16** | 108"). Sixteen of 108 is a minority
shape, not the benchmark's grader semantics. That is a Q3 violation (a paraphrase may narrow its
source, never widen it) and a Q5 failure (one task's script labelled as the benchmark's
contract); the SWE-bench Pro half is separately unlandable on the Q1/Q2 property (no valid row).
It is not rejected for being wrong about SWE-bench Pro — the set-containment claim is plausible
and worth keeping.

**Flip condition:** admit only when (a) the Toolathlon paragraph is narrowed to the `ab-testing`
grader it actually read, or replaced by the 108-grader tabulation (then citing that entry, not
performing a fourth tabulation); (b) S093's row is rewritten to a pipe-free 11-cell form and
S093/S094/S097 are re-opened on 2026-10-25 with ≤25-word located quotes plus a reviewer re-read
of every number (tolerance 0.1, the containment expression, the 642/642 figure it inherits);
(c) it is landed as the grader section of the C1 checklist entry (one entry, one frontier claim)
or explicitly names `benchmark-verifier-execution-model.md` as the entry it extends — not as a
second claim over the same frontier bullet. Note the asymmetry paragraph at `:51-59` (untracked
fixture files escape the revert) is the entry's best content; it survives a rewrite and is the
part to preserve.

---

## Cross-cutting notes the L1 needs (mechanics, not verdicts)

1. **`used-by` is the live hazard — currently avoided, so keep it that way.** Observed at
   2026-10-25 after the C1 landing: `corpus/SOURCES.md` now holds **81** rows
   (`grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → 81) = S001–S076 plus exactly
   S077/S078/S079/S080/S090, each `status=mined opened=2026-10-25 used-by=corpus/knowledge/benchmark-task-validity-checklist.md`,
   11 cells. **None** of the nine rows my three entries cite (S081–S087, S093, S094, S097) was
   appended — correct, since those entries are rejected. The failure mode to avoid is the
   reverse: the fleet census raises `E11 used-by path missing on disk` as an E-finding
   (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:29`; E10/E11 both exit 1), and
   `adoption_check.py`'s `census=ok` is a subprocess exit. The staged `used-by` cells name
   S082/S083 → `contamination-transparency-card.md`; S084/S085/S086/S087 → that file or
   `judge-calibration-thresholds.md` **plus** `cjk-eval-venue-access.md`; S093/S094/S097 →
   `benchmark-grader-semantics.md`. Appending any of them unchanged would leave a dangling
   `used-by` and can flip `census=ok` → not-ok, including for the C1 entry that is already
   landed. `plans/sources_adopt.py:16-18` rule 3 is the intended fix ("`used-by` is rewritten to
   exactly the admitted entries citing the row; a row naming an unadmitted entry never reaches
   the block") — the reject record must be written before any later append block is built.
   Also live: S078's landed scope is "the benchmark maintainer's own post-publication
   task-validity audit of SWE-bench Pro … and its dated per-tree release gate" with `used-by`
   naming only the checklist entry — so admitting `judge-calibration-thresholds.md` later means
   extending that `used-by`, and its §3 rests on a row scoped to a task-validity audit, not to
   judge meta-evaluation (Q2's scope condition).
2. **`recheck-prose` is not a per-entry reject reason.** `package-gate.txt` lists
   `recheck-prose` for all of S077–S087/S094/S097 (and 150 more). C2 rule 3 normalizes a prose
   `recheck` cell to the frozen access date and reports the stripped prose; it is gate work, not
   an entry defect. Do not inflate the reject count with it.
3. **`S093:escaped-pipe` is a per-entry blocker, not cosmetics.** It is the only schema-malformed
   row among the eleven my three entries cite (`package-gate.txt:2`), and it happens to be the
   row that carries the entry's strongest half.
4. **Frozen scope is one entry.**
   `.ufo/waves/round-29/attempt2/adoption-expect.json` pins
   `entries = [benchmark-task-validity-checklist.md]`. Admitting any of these three would leave
   the round claiming two or more entries under a target that names one; the round's own
   precedents resolve this with later dated amendments, not with extra base entries
   (`lanes/kengaku/round2/REJECTIONS.md:17-21`, `round3/REJECTIONS.md:61-66` — both already record
   these five round-1/round-2 files as *not* to be admitted beside later rounds).
   Confirmed against the landed tree: `corpus/README.md:64` is the checklist's index row, `:240`
   its coverage-map row, and the frontier sub-bullet at `:262` states the checklist "supersedes
   only the `unopened leads` phrase for those three sources; contamination-transparency cards,
   runtime task validity and hosted judges remain open". That landed sentence independently
   corroborates these verdicts: the ground of entries 1 and 2, and the runtime half of entry 3,
   is still open — so none of the three is rejected for falling outside coverage, only for the
   property named above.
5. **Adoption-order dependency (counter-argument, stated so the L1 can rule).** Later staged
   entries say they amend these files rather than replace them — e.g.
   `judge-meta-evaluation-2026-10-23.md` ("This amends the lane's existing
   `llm-judge-calibration.md` and the staged round-2 `judge-calibration-thresholds.md`. It does
   not replace either."). If the package is adopted wholesale, the base file must exist for the
   amendment to attach to. This does not clear Q1/Q3/Q6 today; it does mean the reject record
   should say "deferred to the amendment set", not "never".

## Limits of this scan (what I did and did not run)

- Ran: directory/registry censuses (`grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → **76**
  before the C1 append landed, **81** after it — S077/S078/S079/S080/S090, all
  `opened=2026-10-25`; `ls corpus/knowledge/*.md` → **38**, the checklist entry being the newest),
  the escape-aware column parse of
  `merge/kengaku/SOURCES.append.md` for the eleven cited ids, `package-gate.txt` read, seat-report
  grep for S081–S087/S093/S094/S097 (no hits, exit 1), `git cat-file -e
  1f3b0f1…:plans/sources_adopt.py` → exit 128 (absent at baseline; present at HEAD `8c14a5d`).
- **Not run:** no source URL was re-opened by this seat — that is the Src/RevQuote seats' work and
  is exactly the gap recorded above. No `git` write, no append, no lane edit. No production file
  touched; this report is the only file written.
- Not verified by me: whether any of S081–S087/S093/S094/S097 would *survive* a 2026-10-25
  re-open. Their quotes and numbers are therefore treated as unverified, not as false.
- Tooling: none installed or upgraded (nothing needed; no pacman transaction attempted).

## Recommendation to the L1 (advisory)

Admit exactly the frozen C1 entry, and record these three as **REJECT with the flip conditions
above** in `corpus/lessons/round-29.md` §Attempt 2 Gate — each rejection on the property named,
none on province. When the append block is built, drop or rewrite the `used-by` cells for
S078/S081–S087/S093/S094/S097 so no row points at an unadmitted entry (note 1), and keep
`S093:escaped-pipe` refused rather than silently repaired (note 3).
