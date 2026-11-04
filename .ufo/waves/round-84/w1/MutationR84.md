# MutationR84 — Q1 / Q21 admission-rule mutants on the BASE entry bytes

`role: mutation-tester` · `seat: MutationR84` · round 84, w1 · leaf (no subagents)
Base `4087b2f8369fb0c317a8460725a607681ff2fd7f`; claims frozen at `b12a9d46806cb8d69fe48fac0f4efff0b266e4c2`.

I mutated the two admission-bar rules R84-C2 states for `corpus/knowledge/tb2-code-from-image-offline.md` and measured
them with a standalone instrument, on the frozen BASE bytes and on scripted single-edit fixtures. Q13 is not here: it
needs the round-84 Gate and belongs to the L1's C2 counter.

**Result: `killed=8 of 8` — entry mutants `m1`–`m7` all killed, instrument mutant `m8` killed by the BASE-sensitivity
gate. Survivors: none.** Six controls behaved as required (P1 green; N1–N5 red for the reason each was built for).

## The three measurements that matter

| measurement | command | observed |
|---|---|---|
| BASE must be red | `python3 rules.py entry-base.md` | `q1=fail[timing] q21=fail`, `DEFECTS=2`, exit 1 — the frozen before-state `q1=1 q21=1` reproduced exactly on the frozen bytes |
| a satisfying fixture must be green | `python3 rules.py fixtures/repaired.md` | `q1=pass q21=pass`, `DEFECTS=0`, exit 0 — date, command and the pin its `source:` line cites |
| an always-true detector must die | `python3 rules_m8_always_true.py entry-base.md` | BASE reported green, and it flags none of the 7 entry mutants — i.e. it is base-insensitive, which is C2's kill condition |

## Kill table (observed, not hand-copied)

| mutant | edit | should fire | reported | exit | verdict |
|---|---|---|---|---|---|
| m1 | date removed from recheck | q1 | `q1=fail[timing] q21=pass` | 1 | KILLED |
| m2 | pin removed from recheck | q21 | `q1=pass q21=fail` | 1 | KILLED |
| m3 | recheck = `monthly re-verify` | q1, q21 | `q1=fail[action] q21=fail` | 1 | KILLED |
| m4 | recheck moved to line 4 | q1 (order) | `q1=fail[order] q21=pass` | 1 | KILLED |
| m5 | recheck pin one hex digit off | q21 | `q1=pass q21=fail` | 1 | KILLED |
| m6 | `recheck: 2027-05-01` (date only) | q1, q21 | `q1=fail[action] q21=fail` | 1 | KILLED |
| m7 | recheck names the 7-char pin prefix | q21 | `q1=pass q21=fail` | 1 | KILLED |
| m8 | instrument: every predicate always-true | BASE stays red | BASE `q1=pass q21=pass`, pristine `q1=fail[timing] q21=fail` | 0 | KILLED (base-sensitivity gate) |

Each frozen clause has an isolating mutant: Q1 order (m4), timing (m1), action (m3); Q21 pin presence and hex boundary
(N2: source reduced to a 64-hex sha256; N3: pin inside a 41-hex run), pin naming (m2, m5, m7, N5), re-pin cadence branch
(P1 positive, N1 negative). No clause is exercised only as collateral of another clause's failure.

## Findings for the L1's counter (the frozen text is not edited)

- **F3 — two pins is under-specified.** Q21 says "a 40-hex commit pin" (singular) and does not say which pin the recheck
  must name when `source:` cites two. My reading takes the first; N5 (recheck names the second) consequently fires Q21.
  The counter should state its own reading, otherwise N5's colour is a property of the counter, not of the entry.
- **F4 — "the re-pin cadence" has no frozen vocabulary.** `re-pin when needed` (N1) fires under my cadence list and would
  pass under "any re-pin mention". Minimal example: `recheck: 2027-05-01 — re-pin when needed; python3
  plans/round83_c1_replay.py --lane . --work DIR`. The counter should name the vocabulary it accepts.
- **F7 — locate `recheck:` by label, not by line index.** With the line moved to position 4 (m4), Q1 fires on order and
  Q21 still passes because it looks the label up. A counter that reads line 3 for Q21 would count two defects for one
  edit, and its tallies would stop being comparable with the frozen `q1=1 q21=1 q13=1` before-state.
- **F5 — a limit, not a defect.** The frozen Q1 does not require the recheck date to post-date `verified-at:`; a past date
  passes. Do not read the green repaired fixture as freshness enforcement.
- **F6 — the digest trap is handled.** The entry's `verified-at:` line carries a 64-hex subject sha256. N2 (source with
  only that digest) and N3 (pin inside a 41-hex run) both fire Q21, so a 40-hex match cannot be satisfied by a digest or a
  longer hex run.
- **F8 — no claim.** The fixtures are probes, not a proposed repair. The entry's repair is the L1's dated paragraph.
- **F9 — provenance note.** The round-83 Gate row S267 (`corpus/lessons/round-83.md`) cites the same pin
  `2fd12b88aafdd04a52c298e3940bcb189f9766d6` that the entry's `source:` line carries, so the entry's pin is traceable to an
  admitted Gate row at BASE. Q21 as frozen checks only that `recheck:` names that pin; Gate provenance is the Gate/Q13
  side and stays with the L1.

## Method and receipts

`entry-base.md` is `git show 4087b2f8:corpus/knowledge/tb2-code-from-image-offline.md`, sha256
`fc42c76cb5a05c131a5fec4d2aa3e441d9627841d130a54d1b616f2042675271`, 2854 bytes. Every fixture differs from BASE only in
its header lines (body invariant verified: ok). The kill criterion was fixed before running and is stated in
`mutants.md`; `fixtures/fixtures.json` pins all 14 fixture sha256 values and their expected failing rules.

All paths under `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-84/w1/MutationR84/`:

- `rules.py` (`44df925a…aadf297`) — Q1/Q21 instrument; operationalisation decisions D1–D7 in the docstring
- `rules_m8_always_true.py` (`1d3df511…542e82`) — the instrument mutant
- `mkfixtures.py` (`ff007cbf…84ac24`) — scripted fixture construction, refuses non-BASE input
- `battery.py` (`b0558baf…ed881d`) — driver, writes `runs.txt` and `mutants.md`
- `mutants.md` — kill table, per-fixture rule reasons, exact mutant header bytes, survivors/gaps
- `runs.txt` — 50 invocations, each with command, full output and exit code
- `report.txt` — the structured report (`role`, `seat`, `killed=8 of 8`, survivors)

No production file, manifest, state directory, template, script or domain tree was written; no git/jj mutation; no pacman
(host-wide pause); no tool installed (host `python3` 3.14.8 used as installed).

Report: .ufo/waves/round-84/w1/MutationR84/report.txt
