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

## Measured kill table

| id | mutation of the entry bytes | rule(s) that should fire | rules.py reports | exit | verdict |
|---|---|---|---|---|---|
| `repaired` | green baseline: ISO date + command + the commit pin named | none | `q1=pass q21=pass` | 0 | **GREEN AS REQUIRED** |
| `m1` | date removed from recheck (pin and command kept) | `q1` | `q1=fail[timing] q21=pass` | 1 | **KILLED** |
| `m2` | pin removed from recheck (date and command kept) | `q21` | `q1=pass q21=fail` | 1 | **KILLED** |
| `m3` | recheck replaced by `monthly re-verify`: cadence, no object, no pin | `q1`, `q21` | `q1=fail[action] q21=fail` | 1 | **KILLED** |
| `m4` | recheck moved to line 4 (blank line inserted at line 3) | `q1` | `q1=fail[order] q21=pass` | 1 | **KILLED** |
| `m5` | recheck pin differs from the source pin by one hex digit | `q21` | `q1=pass q21=fail` | 1 | **KILLED** |
| `m6` | date with no action and no pin | `q1`, `q21` | `q1=fail[action] q21=fail` | 1 | **KILLED** |
| `m7` | recheck names only the 7-char pin prefix | `q21` | `q1=pass q21=fail` | 1 | **KILLED** |
| `N1` | `re-pin when needed`: re-pin token, no cadence term (date and command kept) | `q21` | `q1=pass q21=fail` | 1 | **KILLED** |
| `N2` | source carries a 64-hex sha256 and no 40-hex commit pin | `q21` | `q1=pass q21=fail` | 1 | **KILLED** |
| `N3` | source pin embedded in a 41-hex run (no standalone 40-hex) | `q21` | `q1=pass q21=fail` | 1 | **KILLED** |
| `N4` | calendar-invalid ISO shape (Feb 31) with command and pin | `q1` | `q1=fail[timing] q21=pass` | 1 | **KILLED** |
| `N5` | source carries two 40-hex pins; recheck names the second | `q21` | `q1=pass q21=fail` | 1 | **KILLED** |
| `P1` | Q21 re-pin-cadence branch, no pin named: must pass | none | `q1=pass q21=pass` | 0 | **GREEN AS REQUIRED** |
| `m8` | instrument mutant: every Q1/Q21 predicate replaced by always-true (`rules_m8_always_true.py`) | BASE must stay red | BASE reported `q1=pass q21=pass`, pristine `q1=fail[timing] q21=fail` | 0 | **KILLED (base-sensitivity gate)** |

`killed=8 of 8` (entry mutants 7/7, instrument mutant included).

Body invariant: every fixture's lines after its header are byte-identical to BASE (ok), so each row prices one header edit and nothing else.

## Full rule reasons per fixture

| id | Q1 (`why`) | Q1 spans | Q21 (`why`) |
|---|---|---|---|
| `repaired` | ok | order=ok timing=ok action=ok | recheck names pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 |
| `m1` | recheck value names neither an ISO date nor a cadence | order=ok timing=bad action=ok | recheck names pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 |
| `m2` | ok | order=ok timing=ok action=ok | recheck names neither pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 nor a re-pin cadence |
| `m3` | action verb 're-verify' carries no object: nothing observable is re-checked | order=ok timing=ok action=bad | recheck names neither pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 nor a re-pin cadence |
| `m4` | line 3 is not 'recheck:' (got '') | order=bad timing=ok action=ok | recheck names pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 |
| `m5` | ok | order=ok timing=ok action=ok | recheck names neither pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 nor a re-pin cadence |
| `m6` | no re-check action: no argv-shaped command and no action verb | order=ok timing=ok action=bad | recheck names neither pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 nor a re-pin cadence |
| `m7` | ok | order=ok timing=ok action=ok | recheck names neither pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 nor a re-pin cadence |
| `N1` | ok | order=ok timing=ok action=ok | recheck names neither pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 nor a re-pin cadence |
| `N2` | ok | order=ok timing=ok action=ok | source: line carries no standalone 40-hex commit pin |
| `N3` | ok | order=ok timing=ok action=ok | source: line carries no standalone 40-hex commit pin |
| `N4` | recheck value names neither an ISO date nor a cadence | order=ok timing=bad action=ok | recheck names pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 |
| `N5` | ok | order=ok timing=ok action=ok | recheck names neither pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 nor a re-pin cadence |
| `P1` | ok | order=ok timing=ok action=ok | recheck names a re-pin cadence |

BASE under the instrument:

```
Q1=fail order=ok timing=bad action=ok
Q1.timing: recheck value names neither an ISO date nor a cadence
Q21=fail pin=2fd12b88aafdd04a52c298e3940bcb189f9766d6 named=no repin_cadence=no
Q21.why: recheck names neither pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6 nor a re-pin cadence
Q1.why: recheck value names neither an ISO date nor a cadence
SHA256=fc42c76cb5a05c131a5fec4d2aa3e441d9627841d130a54d1b616f2042675271 BYTES=2854
DEFECTS=2
RESULT=fail
```

## Exact mutant header bytes

Lines 1-4 of each fixture as generated (body lines 5+ are byte-identical to BASE).

`repaired` — sha256 `3f4a38dc4dd0d7f8c1048dcee0301242e5c80938402f9bf08d7b806d886e5694`

```
1| source: S267 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/code-from-image/tests/test_outputs.py :10-31; capture corpus/evidence/round52/graders/code-from-image/tests/test_outputs.py
2| verified-at: 2026-11-04 (round 83; frozen subject b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a)
3| recheck: 2027-05-01 — python3 plans/round83_c1_replay.py --lane . --work DIR; pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6
4|
```

`m1` — sha256 `b51a21b9bb59d62a27b5af7aa7f93dcdb28c5b75b9ca48b1736fc6907969a720`

```
1| source: S267 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/code-from-image/tests/test_outputs.py :10-31; capture corpus/evidence/round52/graders/code-from-image/tests/test_outputs.py
2| verified-at: 2026-11-04 (round 83; frozen subject b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a)
3| recheck: python3 plans/round83_c1_replay.py --lane . --work DIR; pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6
4|
```

`m2` — sha256 `2635ddc77057e7e94210251b984cc91de47a687e0b09c938fdf5f3cff12b76a4`

```
1| source: S267 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/code-from-image/tests/test_outputs.py :10-31; capture corpus/evidence/round52/graders/code-from-image/tests/test_outputs.py
2| verified-at: 2026-11-04 (round 83; frozen subject b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a)
3| recheck: 2027-05-01 — python3 plans/round83_c1_replay.py --lane . --work DIR
4|
```

`m3` — sha256 `38caf6365833a5cad0ea5a60311c9df6905d73c34b17e89c7ee14c5114a521f5`

```
1| source: S267 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/code-from-image/tests/test_outputs.py :10-31; capture corpus/evidence/round52/graders/code-from-image/tests/test_outputs.py
2| verified-at: 2026-11-04 (round 83; frozen subject b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a)
3| recheck: monthly re-verify
4|
```

`m4` — sha256 `28ba1b3c4ba3f83130562d32f2a41a4ed354e41355e2a679f4663dd60d1a1613`

```
1| source: S267 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/code-from-image/tests/test_outputs.py :10-31; capture corpus/evidence/round52/graders/code-from-image/tests/test_outputs.py
2| verified-at: 2026-11-04 (round 83; frozen subject b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a)
3|
4| recheck: 2027-05-01 — python3 plans/round83_c1_replay.py --lane . --work DIR; pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6
```

`m5` — sha256 `51d10c99cb351509cd1317651843143fa029fbfbd0767c60d465b4908b7801a7`

```
1| source: S267 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/code-from-image/tests/test_outputs.py :10-31; capture corpus/evidence/round52/graders/code-from-image/tests/test_outputs.py
2| verified-at: 2026-11-04 (round 83; frozen subject b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a)
3| recheck: 2027-05-01 — python3 plans/round83_c1_replay.py --lane . --work DIR; pin 2fd12b88aafdd04a52c298e3940bcb189f9766d7
4|
```

`m6` — sha256 `98a1e484c9b643f85a0debd95118ae32337d309e0f870c9ec34792a9030af288`

```
1| source: S267 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/code-from-image/tests/test_outputs.py :10-31; capture corpus/evidence/round52/graders/code-from-image/tests/test_outputs.py
2| verified-at: 2026-11-04 (round 83; frozen subject b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a)
3| recheck: 2027-05-01
4|
```

`m7` — sha256 `2aabda19ac689230ff94f6bf4b82947c17973182a2ad8fb9c244a012e7ae6de2`

```
1| source: S267 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/code-from-image/tests/test_outputs.py :10-31; capture corpus/evidence/round52/graders/code-from-image/tests/test_outputs.py
2| verified-at: 2026-11-04 (round 83; frozen subject b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a)
3| recheck: 2027-05-01 — python3 plans/round83_c1_replay.py --lane . --work DIR; pin 2fd12b8
4|
```

`N1` — sha256 `852c3ac5f0e07ff0d3c8ef89b613dbe0e329b006b8e149eeccedb731a6882b84`

```
1| source: S267 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/code-from-image/tests/test_outputs.py :10-31; capture corpus/evidence/round52/graders/code-from-image/tests/test_outputs.py
2| verified-at: 2026-11-04 (round 83; frozen subject b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a)
3| recheck: 2027-05-01 — re-pin when needed; python3 plans/round83_c1_replay.py --lane . --work DIR
4|
```

`N2` — sha256 `8ee40c34f4cef4d54024bca5c22d78d08618b79db0784f38a1904b6b8de6a3ad`

```
1| source: S267 — corpus/evidence/round52/graders/code-from-image/tests/test_outputs.py; sha256 b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a
2| verified-at: 2026-11-04 (round 83; frozen subject b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a)
3| recheck: 2027-05-01 — python3 plans/round83_c1_replay.py --lane . --work DIR; pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6
4|
```

`N3` — sha256 `3b4e75d39eeca18da19df33b8b486804e0aaa4ffa785aa3f9a39666cdca1d9a9`

```
1| source: S267 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d60/code-from-image/tests/test_outputs.py :10-31
2| verified-at: 2026-11-04 (round 83; frozen subject b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a)
3| recheck: 2027-05-01 — python3 plans/round83_c1_replay.py --lane . --work DIR; pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6
4|
```

`N4` — sha256 `cf0c2154e65c3cccc57f24e493199e2fdfb8e4901d5227f773536ed58a54e5bc`

```
1| source: S267 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/code-from-image/tests/test_outputs.py :10-31; capture corpus/evidence/round52/graders/code-from-image/tests/test_outputs.py
2| verified-at: 2026-11-04 (round 83; frozen subject b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a)
3| recheck: 2027-02-31 — python3 plans/round83_c1_replay.py --lane . --work DIR; pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6
4|
```

`N5` — sha256 `033329e40c6d35db09ca650e3dcc30973b7370133834defbf18ddf0ddd3347aa`

```
1| source: S267 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/code-from-image/tests/test_outputs.py :10-31; superseded pin aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
2| verified-at: 2026-11-04 (round 83; frozen subject b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a)
3| recheck: 2027-05-01 — python3 plans/round83_c1_replay.py --lane . --work DIR; pin aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
4|
```

`P1` — sha256 `11c26e3bee6d43d2e6f02c1af35b50aae890397d49e1273fa3a0e625d400b30a`

```
1| source: S267 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/code-from-image/tests/test_outputs.py :10-31; capture corpus/evidence/round52/graders/code-from-image/tests/test_outputs.py
2| verified-at: 2026-11-04 (round 83; frozen subject b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a)
3| recheck: quarterly — python3 plans/round83_c1_replay.py --lane . --work DIR; re-pin to the then-current upstream commit
4|
```

## Survivors and rule gaps

No entry mutant survived: 7/7 killed, and the instrument mutant m8 is killed by the BASE-sensitivity gate.

The always-true instrument (m8) flags none of the 7 mutant fixtures green, i.e. it lets every entry mutant through: `m1`, `m2`, `m3`, `m4`, `m5`, `m6`, `m7`.

That is why the kill rule is anchored to BASE being red: without the sensitivity gate, m8 would be an unkillable detector that reports a clean admission bar for every entry.

## Transcripts

`runs.txt` holds every command, its full output and its exit code (50 invocations), plus the mechanically derived kill summary. Fixture construction is scripted in `mkfixtures.py`; `fixtures/fixtures.json` pins every fixture sha256 and its expected failing rules.
