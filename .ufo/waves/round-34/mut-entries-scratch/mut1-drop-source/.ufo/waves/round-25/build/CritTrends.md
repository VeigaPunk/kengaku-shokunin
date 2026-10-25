# CritTrends — round 25 adversarial review of the three trend verdicts (read-only)

Pre-attacks what each LEARNING.md trend verdict would say at close, using
`plans/round-25-claims.md` (base `6180e4fb92e9`, pre-reg landed `3f371d2`) and
the observable contracts at `kimi-shokunin/skills/shokunin/protocol/LEARNING.md:31-35`.

## expansion (`improved` = net new admitted entries on uncovered ground, each `source:` citing a `mined` SOURCES row)

- C1's knowledge entry is not a named acceptance test — claims.md:100-101 only
  commits SOURCES rows + a cite. If the entry never lands, `improved` is
  unreachable: unchanged at best.
- A `mined`-row failure is live: the round-24 pattern shows mined/queued are
  distinct statuses (SOURCES.md:9); an entry citing a `queued` row (S024/S025
  pattern) violates LEARNING.md:33 verbatim → the admission itself fails its bar
  → `harmed`, not merely "not improved".
- Boundary: the new entry *extends* `knowledge/attrib-r21.md` ground (same
  instrument, same receipts). Q6 (QUALITY.md:50-55) forces it to name
  `attrib-r21.md`; an entry that doesn't, or that claims the coverage map lacked
  "instrument self-measurement" without a coverage-map row, is an admit that
  fails its bar → harmed.
- Honestly supportable `improved`: entry admitted, cites new `mined` S02x rows
  (exact-interval / Rogan–Gladen primaries — a new source *kind* for this lane),
  README coverage row lands in the same commit (Q7, QUALITY.md:56-59), and the
  Frontier item "Judge calibration applied inward" (README.md:236) is moved or
  struck in the same commit, not left duplicated in both places.

## quality (`harmed` = an entry found false or stale and left unmarked)

- Strongest counterexample: P1 (claims.md:52) predicts the r22 `TARGET hyper
  10/10 -> PASS` re-verdicts INDETERMINATE (n=10 < 17, claims.md:43-45). The
  same PASS premise is written as current at `SCORECARD.md:533` ("hyper
  **COVERED** (run-2: 10/10 on-target = 1.000, bar 0.80)") and
  `knowledge/attrib-r21.md:463,590`. If the instrument prints INDETERMINATE and
  neither gets a dated erratum (R5, QUALITY.md:90), the round *itself* leaves a
  stale entry unmarked → `harmed`. Frozen rule is exit-clean (exit 0 tolerates
  disagreement between stored point verdict and interval verdict — contract
  §Shared interfaces), so nothing forces the erratum except this review.
- P2d freeze defect: claims.md:82-84 freezes `PROVINCE.md ## Surfaces` — the
  round-14 historical table (PROVINCE.md:8-20) whose local paths (`llm-wiki`,
  `bench-arena`) fail `test -e` today and carry no `ABSENT` (ABSENT count = 2,
  only rows 15's inline marker). Closing each mismatch honestly means a dated
  erratum on rows preserved verbatim as historical record (PROVINCE.md:97-100)
  — appending `ABSENT` in-row would be a silent rewrite of that record (R1).
  Unresolvable cleanly → a row is left stale and unmarked → harmed. Re-scoping
  P2d to §Core (PROVINCE.md:102-115) post-freeze is loosening and forbidden.
- P2e file→row: `corpus/lessons/round-24-verifier-spotcheck.md` exists (1d ago)
  with no README index row (README.md:61-90 omits it) — a guaranteed base
  mismatch; it is orchestrator-owned, so "closed by an appended correction"
  (claims.md:90) collides with round-24's own convention (README.md:72,77:
  aggregator-owned files get an index row only, never edits).
- Honestly supportable `improved`: base-run mismatches each closed by dated
  erratum + recompute command (R1), flipped stored verdicts get errata, after-
  run exits 0, and the three red mutation receipts land (claims.md:62-63).

## discernment (`improved` = outside spot-check agrees on ≥1 admit AND ≥1 reject, or disagreement → grounded QUALITY criterion)

- R6 (QUALITY.md:91) + LEARNING.md:46: a lane-dispatched seat is still the
  lane. Every critic in this wave is `.ufo/prompts/`-dispatched; none can fill
  the spot-check. If `round-25.md` records "Spot-check: none yet" (the
  round-24.md:77-79 pattern), verdict is `unchanged` — full stop.
- Structural trap: LEARNING.md:44 requires the check to sample ≥1 admit and ≥1
  reject *of this round's gate*. C1's prior-art sweep is narrow; a gate with
  zero rejects makes `improved` unprovable regardless of the outside verdict.
- Harmed paths: any new QUALITY.md row without a cited lesson (LEARNING.md:35;
  Q9/Q10 exist only because M21/M22 produced them); a spot-check disagreement
  absorbed as prose without a criterion.
- Honestly supportable: orchestrator/fresh-agent spot-check names an id absent
  from `.ufo/prompts/`, agrees on the C1 entry admit + one recorded reject
  (rejected inference or rejected source row — so the Gate must keep at least
  one), or each disagreement becomes a criterion citing a `## Mistakes` row.

## Smallest safe correction

Require the close-out lesson to (a) append a dated erratum on every corpus
line whose stored premise the instrument flips (SCORECARD.md:533,
attrib-r21.md:463,590 — only if P1 fires), (b) record at least one rejected
gate candidate so the outside spot-check has a reject to sample, (c) write the
P2d `## Surfaces` mismatch class explicitly (historical-table rows vs §Core)
so a passing exit-0 isn't read as "the stale table now matches state".

## Falsifiable condition

`quality: harmed` iff the instrument prints INDETERMINATE for r22-hyper and
`grep -n 'erratum\|superseded' corpus/knowledge/attrib-r21.md SCORECARD.md`
shows no new dated line citing `plans/attrib_calibration.py` output.
`discernment: improved` is falsified by `grep -c 'Spot-check: none yet'
corpus/lessons/round-25.md` = 1.

VERDICT: expansion/quality/discernment `improved` are each claimable but fragile — the named erratum + one recorded reject are the load-bearing cheap fixes.
No tools installed; stdlib reads only.
