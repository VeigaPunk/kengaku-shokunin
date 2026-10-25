# Round 30 — frozen claims (kengaku, hyaku run 6, 2026-10-25)

Baseline: lane branch tip at freeze. Three claims, three distinct axes. Frozen BEFORE any wave seat
ran; a predicate changed after a seat has scored is not this claim's predicate.

Lowest non-retired axis: **coverage 7**, tied with **novelty 7** (SCORECARD §Round 29 attempt 2).
No stagnation waiver is available: the saturation line is 8, novelty sits below it, and a capability
row entered at round 29. Tie-break per SCORECARD's recorded rule: the claim that is most falsifiable
with the sources an on-host tool can open wins — C1 opens six public sources and lands a registry
delta; a novelty claim needs a phenomenon probe, and no identity-verified endpoint exists
(`corpus/README.md` §Frontier bullet 4). C1 therefore carries the lowest-axis obligation.

Round shape: two v1 waves (`ufo-wave-policy.json`, band 32–64).

## C1 — coverage: shokuknow assimilation round 2, the contamination-transparency card as an amendment

**Surface this claim moves:** the admission bar's fallback ladder — round-29 attempt 2 refused the
staged `contamination-transparency-card.md` on scope ("a fourth card design where the campaign's own
round 6 tabulated three published designs"), with the recorded flip condition "re-open the cited
sources in a later round … land it as an amendment to the tabulated designs rather than a new
design". This round discharges that flip: the card's Q1–Q8 gate is admitted as an amendment that
names the lane entry it extends, not as a rival design. Frontier bullet 2
(`corpus/README.md` §Frontier, "Contamination transparency cards") moves from *unopened lead* to
*core*.

**Frozen predicate (one sentence, same condition in the counter's code, same label in the receipt):**

> `corpus/knowledge/contamination-transparency-card.md` exists with `source:` lines citing exactly
> the six ids S081 S082 S083 S084 S085 S086 (six distinct), a `verified-at: 2026-10-25` line, and
> every one of those six cited rows present in `corpus/SOURCES.md` with `status=mined`,
> `opened=2026-10-25` and `used-by` naming the entry; the entry has one index row in
> `corpus/README.md`; and `python3 plans/adoption_check.py --expect
> .ufo/waves/round-30/adoption-expect.json --census` prints
> `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok` and exits 0.

**Counting command:** the last clause above (`adoption_check.py`, unchanged from round 29).
**Control (committed at freeze):** the same command on the pre-append tree prints `entries=0 …`
and exits 1 — `.ufo/waves/round-30/claims/control-nothing.txt`.
**Kill rule:** a cited source whose located quote cannot be found in this round's own fetch is
refused for that row; if fewer than four of the six survive, the entry is not admitted and C1 is an
recorded honest stop (registry delta 0).
**Axis verdict shape:** the entry is new corpus bytes on ground the lane did not hold; the canonical
coverage score stays 7 while the round-25 L0 coverage cap is open (unchanged by this round), so the
row records the ledger delta and an `improved` trend, not a raised number.

## C2 — calibration: routed-defect closure D1–D5, mismatch count 5 → 0

**Surface this claim moves:** the eight mismatches between the lane's self-assessment and observed
repo state that round 29's non-author closure routed to the lane
(`corpus/lessons/round-29-verifier-spotcheck.md` §5). Five were routed as defects.

**Frozen predicate:**

> `python3 plans/round30_defects.py --lane .` prints `defects=5` and exits 1 on the pre-repair tree
> and prints `defects=0` and exits 0 on the repaired tree, where the five checks are exactly
> D1 receipt-at-cited-path, D2 kappa-sweep scope, D3 S078 line-75 word count, D4 uncommitted wave
> evidence, D5 S091 `used-by` asymmetry recorded in `adoption-expect.json`.

**Counting command:** `python3 plans/round30_defects.py --lane .`
**Control (committed at freeze):** the do-nothing run — `.ufo/waves/round-30/claims/defects-before.txt`
(D1, D2, D3, D5 fail; D4 is a git-state item whose fix is a commit, so its pre-repair state is the
wave-worktree status line in the same receipt).
**Kill rule:** a D-item that cannot be repaired inside the lane's write scope is reported as an open
defect and C2 misses; D5's repair must leave round 29's frozen counter fields unchanged
(`cited_rows=5`), proved by re-running round 29's expect file in the same round.
**Separability:** reads only round-29 bytes (`corpus/lessons/round-29.md`,
`corpus/evidence/round29-attempt2/`, `.ufo/waves/round-29/attempt2/`,
`.ufo/waves/round-29/attempt2/adoption-expect.json`) — no artifact C1 creates.

## C3 — operability: the adoption gate validates quotes, not just cells

**Surface this claim moves:** the standing gate `plans/sources_adopt.py` validates registry
*schema* (ids, 11 cells, escaped pipes, recheck normalization, `used-by` projection) but not the
thing that makes a row evidence: its quote. Round 29's closure named exactly this gap ("the gate
still has no quote/word validation", `corpus/lessons/round-29-verifier-spotcheck.md` §5 quality).

**Frozen predicate:**

> `python3 plans/sources_adopt.py --selftest` prints `SELFTEST cases=14 failed=0` and exits 0,
> including two new failure-capable cases — a 26-word quote is refused and a quote absent from the
> supplied artifact bytes is refused (distinct non-zero exit codes) — and the gate's pre-change
> bytes (`git show <freeze-baseline>:plans/sources_adopt.py`) reject the same invocation with
> argparse exit 2, i.e. the control cannot reach the target.

**Counting command:** `python3 plans/sources_adopt.py --selftest` (plus the control line above).
**Control (committed at freeze):** `.ufo/waves/round-30/claims/gate-before.txt` — the pre-change
tool run with `--quote-file/--artifact` exits 2 (unknown argument) and its selftest prints
`cases=10`.
**Kill rule:** if either new case cannot be made to fail on the unmodified validator body, the
sub-check is withdrawn and the claim reports the partial count honestly.

## Non-claims

- No novelty credit is taken: S091 (ABC) already prices the per-task validity checklist as prior
  art, and this round adds no phenomenon or instrument claim.
- No score on any axis is raised by assertion; the SCORECARD row records the ledger delta and the
  open cap.
