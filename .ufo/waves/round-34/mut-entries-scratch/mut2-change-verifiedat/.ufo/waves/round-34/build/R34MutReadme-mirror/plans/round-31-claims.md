# Round 31 — frozen claims (kengaku, hyaku run 6, 2026-10-25)

Baseline: lane branch tip `0883e72ef8474ca42ac1a54eb0273079f1507035` (local = remote, `ahead=0`).
Registry 88 rows, `corpus/knowledge/` 39 files, 39 index rows, census exit 0 with 14 `W04`.
Three claims, three distinct axes. Frozen BEFORE any wave seat ran; a predicate changed after a seat
has scored is not this claim's predicate.

Lowest non-retired axis: **coverage 7**, tied with **novelty 7** (SCORECARD §Round 30). No stagnation
waiver is available: the saturation line is 8, novelty sits below it, and a capability row entered at
round 30. Tie-break per the lane's recorded rule: the claim that is most falsifiable with the sources
an on-host tool can open wins — C1 opens three pinned-commit source trees and lands a registry delta;
a novelty claim needs a phenomenon probe and no identity-verified endpoint exists
(`corpus/README.md` §Frontier bullet 4). C1 therefore carries the lowest-axis obligation.

Round shape: two v1 waves (`ufo-wave-policy.json`, band 32–64).

## C1 — coverage: shokuknow assimilation round 3, the benchmark verifier execution model

**Surface this claim moves:** *runtime task validity*, named open twice and never held —
`corpus/README.md` §Frontier bullet 1 ("contamination-transparency cards, runtime task validity and
hosted judges remain open") and the round-29 coverage row's own bound ("Not deployment config, not
runtime task validity, not contamination measurement",
`corpus/README.md:250`). Round 29's `knowledge/benchmark-task-validity-checklist.md` left axis E
("grader integrity") open for Terminal-Bench 2.0 and called it *partly observable*; the staged entry
`benchmark-verifier-execution-model.md` closes that axis by reading the harness's own resolution
rule, and it corrects the round-1 framing instead of restating it.

**Frozen predicate (one sentence, same condition in the counter's code, same label in the receipt):**

> `corpus/knowledge/benchmark-verifier-execution-model.md` exists with `source:` lines citing exactly
> the three ids adopted this round (three distinct), a `verified-at: 2026-10-25` line, and every one
> of those three cited rows present in `corpus/SOURCES.md` with `status=mined`, `opened=2026-10-25`
> and `used-by` naming the entry; the entry has one index row in `corpus/README.md`; and
> `python3 plans/adoption_check.py --expect .ufo/waves/round-31/adoption-expect.json --census` prints
> `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok` and exits 0.

**Counting command:** the last clause above (`plans/adoption_check.py`, unchanged from rounds 29–30).
**Control (committed at freeze):** the same command on the pre-append tree prints `entries=0 …` and
exits 1 — `.ufo/waves/round-31/claims/control-nothing.txt`.
**Kill rule:** a cited source whose located quote cannot be found at the pinned revision is refused
for that row; if fewer than two of the three survive, the entry is not admitted and C1 is a recorded
honest stop (registry delta 0).
**Axis verdict shape:** the entry is new corpus bytes on ground the coverage map did not hold; the
canonical coverage score stays 7 while the round-25 L0 coverage cap is open, so the row records the
ledger delta and an `improved` trend, not a raised number.

## C2 — calibration: round-30 routed-defect closure, mismatch count 10 → 0

**Surface this claim moves:** the mismatches between the lane's self-assessment and observed repo
state that round 30's non-author closure routed to the lane
(`corpus/lessons/round-30-verifier-spotcheck.md` §5 items 1–8), plus the two copyedit residues the
same pass located inside the admitted entry. Ten items, each a location the closure named.

**Frozen predicate:**

> `python3 plans/round31_defects.py --lane .` prints `defects=10` and exits 1 on the pre-repair tree
> and prints `defects=0` and exits 0 on the repaired tree, where the ten checks are exactly
> R1 `LOG.md:792` named correction appended, R2 lesson Q6 basis erratum, R3 lesson Q2 tier cell
> erratum, R4 entry duplicated "reconciled truth" sentence removed, R5 entry falsifier duplicated
> clause removed, R6 entry source-row count consistent (`two of its three`), R7 entry S2 "only new
> field" narrowed to the card-level field, R8 entry licence adjective grounded or dropped,
> R9 the five round-30 seat reports committed at HEAD, R10 lesson round-shape `34` corrected to `33`.

**Counting command:** `python3 plans/round31_defects.py --lane .`
**Control (committed at freeze):** `.ufo/waves/round-31/claims/defects-before.txt` — the same counter
run on the pre-repair tree (`defects=10`, exit 1).
**Kill rule:** an item that cannot be repaired inside the lane's write scope is reported as an open
defect and C2 misses. R9's repair must leave the five reports' bytes intact (no revert to the older
committed revision), proved by the committed-blob test in the counter.
**Separability:** reads only round-30 bytes (`LOG.md`, `corpus/lessons/round-30.md`,
`corpus/knowledge/contamination-transparency-card.md`, `.ufo/waves/round-30/`) — no artifact C1 or C3
creates.

## C3 — operability: the adoption gate binds the capture to the row's cited URL

**Surface this claim moves:** the standing gate `plans/sources_adopt.py` validates a row's quoted
span against *bytes it was handed*, and round 30 disclosed the gap in its own words: "it does not
bind the artifact to the cited URL"
(`SCORECARD.md` §Round 30 C3 row). A capture of any document that contains the same string satisfies
the gate, so a row can be green while its quote was never read in the document it cites.

**Frozen predicate:**

> `python3 plans/sources_adopt.py --selftest` prints `SELFTEST cases=17 failed=0` and exits 0, with
> three new failure-capable cases: a row whose located quote comes from an artifact mapped to its own
> cited URL is accepted; the same row with the artifact mapped to a different URL is refused with
> exit 8; and the same row whose artifact has no map entry is refused with exit 9. The gate's
> pre-change bytes (`git show 0883e72:plans/sources_adopt.py`) reject the same invocation with
> argparse exit 2, i.e. the control cannot reach the target.

**Counting command:** `python3 plans/sources_adopt.py --selftest` (plus the control line above).
**Control (committed at freeze):** `.ufo/waves/round-31/claims/gate-before.txt` — the baseline tool
run with `--url-map` exits 2 (unrecognized argument) and its selftest prints `cases=14`.
**Kill rule:** if either new refusal cannot be made to fail on the unmodified validator body, that
sub-check is withdrawn and the claim reports the partial count honestly.

## Non-claims

- No novelty credit is taken: the entry's finding is a reading of a published harness default, not a
  phenomenon this lane measured; S091-style prior art is not claimed either way.
- No score on any axis is raised by assertion; every SCORECARD row records the ledger delta.
