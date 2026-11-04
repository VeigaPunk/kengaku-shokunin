# Q1 / Q21 admission-rule mutants — round-84 mutation battery

`seat: MutationR84` · `role: mutation-tester` · wave `round-84/w1` · base `4087b2f8369fb0c317a8460725a607681ff2fd7f` ·
frozen claims `b12a9d46806cb8d69fe48fac0f4efff0b266e4c2` (`plans/round-84-claims.md`).

Target: the two admission-bar rules R84-C2 states for `corpus/knowledge/tb2-code-from-image-offline.md`, exercised on the
frozen BASE bytes. Q13 is deliberately absent — it needs the round-84 Gate and belongs to the L1's C2 counter, not to
these entry bytes.

Frozen sentences, quoted and not edited:

> **Q1** — its first three lines are `source:`, `verified-at:` and `recheck:`, and `recheck:` names an ISO date or cadence and a re-check action;
> **Q21** — its `source:` line carries a 40-hex commit pin and its `recheck:` line names that pin or the re-pin cadence;

## Method

- Input bytes: `entry-base.md` = `git show 4087b2f8:corpus/knowledge/tb2-code-from-image-offline.md`,
  sha256 `fc42c76cb5a05c131a5fec4d2aa3e441d9627841d130a54d1b616f2042675271`, 2854 bytes. That is the revision the frozen
  claim measures its before-state at, so it is the only revision this battery scores.
- Instruments: `rules.py` (the two rules; operationalisation decisions D1–D7 are written out in its module docstring),
  `mkfixtures.py` (scripted fixture construction from the BASE bytes), `battery.py` (driver; writes `runs.txt` and this
  file). No third-party tool was installed for this seat.
- Fixtures: each is BASE with an edit to the three header lines only, body byte-identical to BASE. `fixtures/fixtures.json`
  pins every fixture sha256 and its expected failing rules. `repaired` is the green baseline: BASE's own recheck command,
  plus an ISO date, plus the commit pin its `source:` line already cites.
- Kill criterion, fixed before running:
  - an **entry mutant is KILLED** iff the observed failing-rule set equals the expected set, the exit code is 1
    (0 for the green fixtures), and its bytes differ from `repaired` (a mutation that changed nothing is a no-op, not a kill);
  - **SURVIVED** iff an expected rule did not fire;
  - **OVERFIRED** iff it was killed *and* an unexpected rule also fired (detection bought with a false positive);
  - the **instrument mutant m8 is KILLED** iff it reports BASE green — C2's kill rule is "a base-insensitive check […]
    fails the claim", and an always-true detector is exactly that.
- Interpretive judgement calls, stated because the frozen text under-determines them:
  - **D3** a bare action verb with no object is not a re-check action, so m3's `monthly re-verify` fires Q1. m3 also fires
    Q21 independently, so the kill does not rest on this reading; the robustness row below records both readings.
  - **D6** `re-pin when needed` carries a re-pin token but no cadence, so N1 fires Q21. That is stricter than "any re-pin
    mention" and is recorded as a judgement, not as claim text.
  - **D7** the frozen Q1 does not relate the recheck date to `verified-at:`, so a past date would pass; the instrument
    adds no such requirement.

## Calibration check available to this seat

The frozen claim states the BASE before-state as `q1=1 q21=1` (both red) out of `defects=3`, with Q13 red as well. This
instrument must reproduce `q1=1 q21=1` on the same BASE bytes and nothing better; the `BASE bytes` block below is that
check. If the two disagree, the instrument is wrong, not the claim.

## Residual risk (nothing here is silently dropped)

- The frozen text does not say which pin is authoritative when `source:` carries two 40-hex pins; D4 takes the first
  one. N5 records the behaviour. Two-pin entries are unaddressed by the claim.
- The frozen Q21 says "the re-pin cadence" without defining its vocabulary; D6's list is mine (daily … yearly,
  per round/wave/release, on upstream/pin change). A cadence phrased outside it would fire Q21 on a correct entry. The
  error is biased toward strictness on purpose: a missed defect is worse than a strict reading, and the production
  reading belongs to the L1's counter, not to this instrument.
- No fixture carries a pin with uppercase hex or inside a URL query fragment; `PIN_RE` is case-insensitive on hex, and
  the frozen entry's pins are lowercase, so the fixtures use the shape the entry actually has.
- These rules were probed against one entry (BASE) and its fixtures. They are not a general admission checker and this
  battery makes no claim about any other knowledge entry.

Re-run from this directory with `python3 battery.py`; it rebuilds the fixtures, reruns every probe and rewrites
`runs.txt` and this file. Scratch (`$HYAKU_SCRATCH/kengaku-r84/MutationR84`) is transient here: the fixtures and the
receipts live in this seat directory.

<!-- generated sections follow; the tables are emitted by battery.py from the observed runs, never hand-copied -->
