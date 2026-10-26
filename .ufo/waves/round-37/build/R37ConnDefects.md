# R37ConnDefects — cross-round defect-class map (rounds 30–36), read-only connector report

Seat: R37ConnDefects (connector, leaf). Wave 1 of 2, kengaku round 37 (hyaku run 8, 2026-10-26).
Axes named (godspeed): **calibration** — every class count and recurrence is tied to a spot-check
file:line; **adjacency** — every class is mapped to what this round's frozen C1/C2 counters and the
wave-1 anchor sweep do and do not mechanically check, and to `considerthese/2026-10-25.md` proposal 2(b).

Method: read all seven `corpus/lessons/round-3N-verifier-spotcheck.md` (N=0..6) in full, plus
`plans/round-37-claims.md`, `plans/round37_c2_verify.py` (docstring V1–V7), `corpus/QUALITY.md`
Q24/Q25, `considerthese/2026-10-25.md` (proposal 2), and the round-37 claims controls. Counting
rule: a class "recurs" in a round if that round's spot-check routes or conformance-names at least one
item of the class (line citations below; line numbers from `grep -n` over the committed files, run
2026-10-26). No lane file was edited; no fixtures, no scratch needed (read-only seat); no tools
installed.

---

## 1. The class map

13 classes, ordered by recurrence. "Rounds" = distinct rounds 30–36 with at least one routed or
conformance-named item of that class.

### Recurring classes (≥2 rounds)

**C1. counter-accepts-junk / weak counter** (shape-not-support checks, gameable batteries, counter
blind spots, partial receipts presented as closure). **Rounds: 3 (r32, r35, r36); 4 routed items.**
- r32:87 — "Correct counter blind spots identified by round-32 mutation evidence; do not present a
  partial receipt or selftest as closure" (C2 left at `checks=7 defects=5`, selftest offered as evidence).
- r35:86 item 1 — "Frozen counters accept junk … passes a stub probe plus one-word quotes;
  `plans/defect_ledger.py` D4/D5 accept labelled-but-false lines."
- r36:89 item 2 — "Frozen battery gameable and clause-incomplete … must cover the eight fixture-less
  clauses and include a renamed-fixture run."
- r36:90 item 3 — "C2 counter admits a junk package … W2/W3 check shape, not support."
- (Disclosed, not routed: r31 C2 — every repair has a fakeability route, `R31FxC2Survivors.md`.)

**C2. digest/anchor transcription & manifest gaps** (a digest or manifest that does not match the
bytes it pins, with nothing checking the equality). **Rounds: 3 (r34, r35, r36); 3 items.**
- r34:77 D3 — "`tb2-eval/SHA256SUMS` omits `test_outputs.py`/`test.sh`, contradicting
  `R34CaptureTB2Eval.md`."
- r35:90 item 5 — S091 live leg: NEC returns a 418-byte denial; "cite the committed capture + digest,
  not live reachability" (grounding rule for the class).
- r36:88 item 1 — "S110 anchor digest truncated" (63 hex; one `0` dropped); "Nothing checks the row's
  digest against the manifest … Add a counter check that each row's anchor digest equals the capture
  manifest."

**C3. receipt drift / evidence not re-runnable at tip** (a committed receipt that no longer reproduces
or mislabels its own measurement; records quoting it go stale). **Rounds: 2 (r30, r31); 2 items.**
- r30 §2 C2 — `defects-after.txt` header names measured commits `623c1fc9 -> d0253c52`; the report
  table says "measured at `706ed3f2`" (stale revision label; superseded by erratum 1).
- r31:154 D3 — "`ae14f46` rewrote `corpus/evidence/round31/gate-cli-exits.txt` with a run whose path
  … resolves to `.ufo/plans` (absent); every line reads `can't open file` and `exit=2`", while the
  report calls the receipt "self-contained" and SCORECARD quotes its old 0/8/9/2 exits.

**C4. scratch leaks** (uncommitted round work at closure; committed scratch bloat; nested mirrors).
**Rounds: 4 (r30, r32, r34, r35); 5 items.**
- r30:184 item 6 — five wave seat reports modified in the working tree, "a writer was still appending
  to them during this pass … after the driver's `complete` line".
- r32:90 — "ten wave paths remain at lane tip despite `ahead=0`".
- r34:75 D1 — 1423 untracked paths incl. three `plans/round34_*.py` instruments.
- r34:76 D2 — `.ufo/waves/round-34/mut-entries-scratch/` "106,323 blobs, 1650.6 MiB logical" of
  recursive repo mirrors committed.
- r35:88 item 3 — residual: 21 committed nested `.ufo/waves/` mirror paths (r35 counted 21 by its
  method vs 28 cited; roots "narrow"). Closed in r36 (21→0, `round-36-verifier-spotcheck.md` §2 table).

**C5. stale/erroneous record vs evidence** (append-only correction debt: wrong cells, misattribution,
copyedit residue, findings not absorbed; the record says X, the bytes say Y). **Rounds: 7 (r30–r36,
every round); ~14 items — the most recurrent class.**
- r30: items 1–3 (`LOG.md:792` retracted delta; Q6 basis; Q2 tier cell `S086 A` vs registry B),
  item 4 (duplicated sentence, entry :125-126), item 5 (S2 "only new field" contradiction + CC0 vs
  CC BY), item 8 (lesson :3 "34 falsify" vs registries 33).
- r31:165 D6 — correction sweep cites stale locators (`:35-38` corrected to `:39-40`; `:78-81` vs
  `:72`/`:82-83`).
- r33 §5 — lesson header "36 + 36 seats" vs registries 36+53; frozen control prose `entries=0` vs
  printed `entries=1`.
- r34:78 D4 — SCORECARD C2 row "misattributes the red selftest to the counter draft" (it was the
  harness, `R34MutC2Harness.md:12`).
- r34:79 D5 — S091 refusal reason false: "quote absent" while the quote is present verbatim in the
  round's own reopen capture; lesson line "opened NEC response was unavailable" contradicted.
- r35:89 item 4 — Toolathlon refusal row cites only one of two reasons (omits the 38 vs 13+23+1=37
  denominator).
- r36:91 item 4 — "Wave-1 findings not absorbed" (F3–F6, F8, F10; `R36RevProbePred` non-independent
  cases) + anchor drift (S110 `lines 1–11` vs row `:1-19`; "lines 71-81" vs list lines 72–82).

**C6. report-before-commit / stale tip / phantom hash.** **Rounds: 3 (r30, r31, r32); 4 items;
closed since r33.**
- r30:190 item 7 — report's last commit precedes the lane's final three commits; erratum's "lane tip"
  stale (`caf1e2b4` vs `2dcf06c5`).
- r31:149 D1 — phantom hash "`a44b5a8`-class commits"; `git cat-file -t a44b5a8` → missing.
- r31:151 D2 — item 7 recurred: final commits `ae95fe0`/`87f0d32` never cited; erratum names `9591131e`.
- r32:87 — both still red in C2 receipts. Closed r33 (N3/N4 re-derived green, `round-33-verifier-spotcheck.md` §2).

**C7. locator/line drift** (citations pointing at lines the content no longer occupies, distinct from
C5 only in mechanism: edits moved content, the pointer stayed). **Rounds: 2 (r31, r36); 2 items.**
- r31:165 D6 (above). r36:91 item 4 (above) + r36 §2/§3 one-line drift ("lines 71–81" vs 72–82).

**C8. evidence retention / live-reachability dependence** (raw bytes not retained; claims resting on
live fetches a host can deny). **Rounds: 2 (r32, r35); 2 items.**
- r32:89 — "raw API payloads are not retained; preserve bounded response bytes plus digests next
  probe" (C3 failed as declared; raw JSON existed only in a seat's `/tmp`).
- r35:90 item 5 — S091 418-byte denial; future claims must cite committed capture + digest.

**C9. seat-ledger / round-shape / attribution conformance.** **Rounds: 5 (r30, r31, r32, r33, r36);
6 items.**
- r30 item 8 (34 vs 33 — also C5); r31:162 D5 — falsify registry 36 members, 35 reports committed,
  `R31FxEntryBar` missing while the report says "0 dead"; r32:87 — seat ledger red; r33 §5(a) —
  header seat count wrong; r36:22 — "Round size below the run-7 floor: wave 1 only, 40 seats … wave 2
  (34 seats, `falsify-spec.json`) committed and not dispatched", plus attribution `6e1bc4a` (lane
  identity, not in the landed-changes table) and measured revision `612458f3` vs cited tip.

### Singleton classes (1 round each)

**C10. counter method** (counter reads the working tree instead of committed bytes; check roots too
narrow; token co-occurrence instead of content). r35:87 item 2, r35:88 item 3. 1 round, 2 items.
**C11. source-id collision** (staged package proposes live ids S094/S097). r32:88. 1 round, 1 item.
**C12. wave-2 not run** (r36:22; also r36:83 "the planned wave-2 re-verification did not run"). 1
round, open — this round's wave 2 is pending. **C13. closure/spot-check debt** (r36:93 item 6 —
`round-36.md` `## Spot-check` reads "Pending"; items 3–4 not executed: hand-running the gate on the
six line fixtures; fixture-name keying). 1 round, 1 item. Also singleton-adjacent: r31:159 D4 (gate
registry row missing for `sources_adopt.py`) — folded into C9's conformance family, r31 only.

Totals: **13 classes; 9 recurring** (C1–C9); 34 routed/named items across 7 spot-checks (counting
r32's grouped bullet R1/R2/R5/R6/R7 as the four items it names, and r30 items once each).

---

## 2. Which classes this round's C1 / C2 / anchor sweep check mechanically

Sources: `plans/round-37-claims.md` (frozen predicate + kill rules + controls);
`plans/round37_c2_verify.py:1-32` (V1–V7 docstring); `.ufo/waves/round-37/claims/control-*.txt`
(all red at freeze, verified listed); `.ufo/waves/round-37/claims/census-before.txt` (`exit=0`, 15 W04).

| class | mechanical check this round | coverage |
|---|---|---|
| C1 counter-accepts-junk | **C1 counter**: 55 frozen mutants must all be killed; mislabel battery → `wrong=1`; gate-edited → `invalid=55`; example-fixture-only kills 1; `renamed_disagree=0` kills name-keyed fixtures (r36 item 2 + the §6 item-4 fixture-name keying). **C2 V2**: package gate over `pkg-spec-r37.json` brings quote-support clauses (verbatim on cited line) — r36 item 3's exact fix. | **full** |
| C2 digest/anchor | **C2 V1** (SHA256SUMS lists exactly the six captures at frozen digests, bytes match); **V3** (each S111–S113 anchor carries `sha256 <64 hex>` equal to its pin, "no other sha256 token" — the 63-hex class caught by construction). **Wave-1 anchor sweep** (seat R37AnchorSweep): lane-wide "each row's anchor digest equals the capture manifest" — r36 item 1's routed fix. | **full** |
| C3 receipt drift | **C2 V4** (receipt internally consistent, ids equal frozen case table); **V7** (requirement-map labels must agree with executed verdicts — a hand-typed receipt cannot pass). Skip-control `control-c2-skip.txt` shows hand-typed receipt → V2 red (fresh re-run not byte-equal). | **partial** — covers only C2's own receipt; no lane-wide tip-receipt validator (that is considerthese proposal 2(c), unimplemented) |
| C4 scratch leaks | none — no counter inspects the lane's working tree or committed-tree mirror paths; C1's genuine fixture exercises the gate's P9-untracked clause *inside the fixture package*, not the lane. Seat scratch rules (`/fast/scratch`) are process directives, not a check. | **none** |
| C5 stale record | **V7** binds the new entry's map labels to executed verdicts (a record-vs-evidence agreement check for one file). QUALITY Q20/Q23/Q24/Q25 are judgment criteria, not executors. | **partial** (one file) — no lane-wide record-vs-evidence check; still 7/7 rounds |
| C6 report-before-commit | none (closure-conformance domain, integrator-enforced). | **none** (closed since r33, but nothing prevents recurrence) |
| C7 locator drift | C2 V2's quote-support mechanically verifies each quote on its cited line — a locator check for the **new** package; legacy entries unaffected. | **partial** (new material only) |
| C8 retention / live reachability | C2 freezes captures with SHA256SUMS and runs the probe fully offline (bubblewrap, private netns) — byte-retention demonstrated for the new evidence. | **partial** (new evidence only) |
| C9 seat ledger / shape / attribution | none. | **none** |
| C10 counter method | both frozen predicates require measurement "on a clean clone of the landing tip" — removes the working-tree hazard for the new counters. | **partial** |
| C11 id collision | none (census W04 flags duplicate URLs across scopes, not staged-vs-live id collisions). | **none** |
| C12 wave-2 not run | none — nothing blocks a round from closing wave-1-only; r37's own wave 2 is pending. | **none** |
| C13 closure debt | none. | **none** |

**Recurring classes with no mechanical check this round: C4 (scratch leaks, 4 rounds), C6
(report-before-commit, 3 rounds), C9 (seat ledger/shape, 5 rounds).** C11–C13 are unchecked
singletons. Second-order note (adjacency): C1 and C2 counters each run on a clean clone and read
disjoint trees (claims file "Separability"), so neither counter's green can mask the other's red —
the map above inherits that independence class-by-class.

---

## 3. Proposal 2(b) — the smallest honest implementation

Source: `considerthese/2026-10-25.md:42-47` — one persistent `corpus/defects.jsonl` (id, class,
opened_round, closing_commit, recurrence) with a checker that "(a) re-runs every closed defect's
check at tip forever, (b) blocks pre-registration when a class recurs twice, and (c) includes a
tip-receipt validator".

**Reading chosen.** "Blocks pre-registration when a class recurs twice" has two readings:
(i) ≥2 occurrences ever → permanent block — dishonest, since it punishes a class that recurred and
was fully closed, and would push the lane toward misclassification to escape; (ii) ≥2 occurrences
with ≥1 currently open → block until closed with evidence — operable and matches intent (a class
that already bit once and shows up again unaddressed). The smallest honest implementation uses (ii)
and records the reading in the claims freeze.

**The implementation (three parts, all in existing lane idiom):**

1. **Ledger** `corpus/defects.jsonl` — one row per routed *occurrence*, not per defect:
   `{id, class, opened_round, source: "<spotcheck file>:<line>", quote: "≤25 words from the item",
   closing_commit: null, closed_round: null}`. Rows are appended by the **non-author integrator at
   closure**, keyed off the spot-check's routed list — the class count is then not lane
   self-assessment (the honesty core: the r30–r36 record shows lanes under-route their own escapes;
   every recurrence above was found by the non-author). `class` is a closed enum (C1–C13 above or a
   coarser cut); enum edits are themselves reviewed changes, so "misc" cannot absorb recurrences.
   The `quote` field makes every classification auditable against the cited spot-check line.

2. **Checker** `plans/defect_class_gate.py --lane .` (~120 lines, same shape as the existing
   `plans/defect_ledger.py` it supersedes): validate schema + enum + quote presence; per class
   compute `occurrences` (distinct `opened_round`) and `open` (rows with `closing_commit: null`);
   if any class has `occurrences >= 2 && open >= 1` print
   `CLASS-BLOCK class=<c> occurrences=<n> open=<m>` and exit 1, else print
   `CLASSES total=<n> recurring=<n> blocked=0` exit 0. Closure honesty, minimally: a closing row
   must name a `closing_commit` that exists in the lane and a check-artifact path that exists at tip
   (existence only — re-proving the check passes is proposal 2(a), a separate small checker; 2(b)
   alone must not pretend "closed" means "verified"). State that dependency in the ledger header.

3. **Where the block bites** — receipt-based, no hooks: the round's claims freeze (the
   `plans/round-NN-claims.md` commit set) must include
   `.ufo/waves/round-NN/claims/defect-classes-before.txt`, the checker's green output at freeze
   time — exactly the pattern `census-before.txt` already follows (`exit=0`, 15 W04, committed with
   the claims). The validator that freezes claims runs the gate first; the closure integrator
   re-runs it and treats a missing or red receipt as a conformance defect. No git/jj hooks: the
   lane's enforcement has always been committed receipts plus integrator refusal, and a hook on a
   jj-managed lane is operationally heavier than the freeze receipt. Honest limitation, stated: the
   block is exactly as strong as the integrator's refusal of a red receipt — the same strength as
   the census and gate-registry rules already in force.

**Retroactive would-have-blocked test** (applying the map in §1 to r30–r36): at r37 freeze the gate
would be red on **counter-accepts-junk** (r32, r35, r36 open), **digest/anchor** (r34, r36 open),
**stale-record** (every round, r36 item 4 open) and **seat-ledger/shape** (r30–r33, r36 open); green
on report-before-commit (all closed since r33) and receipt drift (r30, r31 both closed). So 4
classes would have blocked r37 pre-registration — and the round's build budget is in fact spent on
exactly two of them (C1/C2 mutant-and-support checks for junk counters; V3 + the anchor sweep for
digests). The mechanism targets real recurrences; its cost is one jsonl append at closure plus one
receipt per freeze.

**Risks.** (a) Misclassification — bounded by the non-author append rule + quote field, not
eliminated; a determined integrator can mislabel, but every label carries its own audit quote.
(b) Taxonomy drift — the closed enum forces explicit, reviewable class births (C11–C13 this map
shows births happen). (c) 2(b) without 2(a) weakens "closed" to "asserted with a cited artifact" —
stated above; the two checkers compose and 2(a) is the natural next slice. (d) Permanent-block
reading (i) would be theater; the freeze text must pin reading (ii).

---

## Limits of this report

Round-37 in-flight build items (battery37, the lane-wide anchor sweep) were assessed from the frozen
claims file and the goal-statement seat list, not from executed output — the anchor sweep's
mechanical reach is as specified in r36 routed item 1 ("each row's anchor digest equals the capture
manifest"). Class boundaries are a connector taxonomy: C5/C7 and C9/C12 are split by mechanism, and
a coarser cut would merge them (counts would drop to ~10 classes; recurrences to 7). No spot-check
was re-executed; all citations are to committed files at the lane tip.

VERDICT: classes-13-recurring-9-unchecked-3
