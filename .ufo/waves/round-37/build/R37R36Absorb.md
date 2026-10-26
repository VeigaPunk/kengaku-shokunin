# R37R36Absorb — round-36 leftovers absorbed as append-only errata (draft only)

Seat: R37R36Absorb (scribe). Round 37 (hyaku run 8), wave 1. Lane:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`, read-only for this seat.
Scratch: `/fast/scratch/hyaku/kengaku-r37/R37R36Absorb` (removed at the end; receipts copied to
`.ufo/waves/round-37/build/R37R36Absorb/` first). No lane file, index, or jj state was written.

## 1. Behavior

Absorbed three round-36 leftovers as **drafts** for the L1, verifying every claim against the pinned capture
and the frozen probe case table rather than against the round-36 reports' prose:

| item | source of the claim | what I did | result |
|---|---|---|---|
| (a) probe-predicate confound | `.ufo/waves/round-36/build/R36RevProbePred.md` §3 (D-RP2) | re-executed the frozen `plans/regex_log_probe.py` patterns over the log rebuilt from the capture; attributed every divergent match to its sample line → file line | confound **confirmed**, and the entry's `What decides it` row carries **wrong line numbers** on top of it (§4) |
| (b) anchor drift | `corpus/lessons/round-36-verifier-spotcheck.md:68,91` | `sed -n`, `grep -n`, AST element linenos | the S110 span drift is **real** (`1–11` vs `:1-19`; exact = `:1-10`); the lesson's `71-81` is **correct** — the spot-check's `72–82` is the drifted cell (§5) |
| (c) S110 anchor digest | `corpus/SOURCES.md:125` vs `SHA256SUMS` | length compare + `sha256sum -c` | row digest is **63 hex** (one `0` dropped at index 15); correct digest from `SHA256SUMS:3` (§5) |

Drafts (paste-ready, append-only style, nothing applied):
`.ufo/waves/round-37/build/R37R36Absorb/errata-entry.md` (the `## Errata (round 37)` section for
`corpus/knowledge/tb2-regex-log-grader.md`) and
`.ufo/waves/round-37/build/R37R36Absorb/errata-lessons.md` (the matching lines for
`corpus/lessons/round-36-verifier-spotcheck.md`, plus the explicit "no erratum" finding for
`corpus/lessons/round-36.md`).

## 2. Gates and capture integrity

- `sha256sum -c corpus/evidence/round36/tb2-regex-log/SHA256SUMS` → `test_outputs.py: OK`, `test.sh: OK`,
  `instruction.md: OK`, `task.toml: OK`, `solve.sh: OK` (5/5). Receipt:
  `.ufo/waves/round-37/build/R37R36Absorb/capture-digests.txt`.
- I ran **no** lane gate: `plans/pkg_gate.py`, `plans/round37_c1_verify.py` and `plans/round37_c2_verify.py`
  are other seats' instruments and frozen this round; a scribe running them would produce no artefact this
  task needs. My only executions were the two read-only scripts below, both `python3 -B` and in-memory
  `compile()`/`exec()` so that **no `__pycache__` was written into `corpus/evidence/`** (the D-RP6 hole a
  sibling seat measured last round).
- Lane-state claim is limited to what I did: every command I issued was a read (`sed`, `grep`, `wc`,
  `sha256sum -c`, `python3 -B` on in-memory copies of lane sources). I ran no git/jj command at all.

## 3. The method and its reproduction of the receipt

Script: `.ufo/waves/round-37/build/R37R36Absorb/attribution.py`; log rebuilt from the capture by AST
(`sample_logs`, 25 strings, `:35`–`:67`; `expected_dates`, 9 strings, `:72`–`:80`); patterns taken from the
frozen `build_cases()` (no hand transcription). Verdict reproduction:
`.ufo/waves/round-37/build/R37R36Absorb/receipt-verdicts.py` →

```
file-mode cases: 23
verdict mismatches vs receipt (with .strip() as the grader does): 0 []
```

(The 24th case, `regex-file-absent`, is `mode="absent"` and needs a filesystem probe; not reproduced. My first
run without `.strip()` mis-called `padded-file`, which is exactly the grader's `strip()` step —
`padded-file raw == expected: False`, `padded-file strip == expected: True`.)

## 4. Item (a): the `What decides it` table — which rows are not independent evidence

Measured flip sets (frozen pattern vs the reference `reference-month-aware` pattern, per sample line; sample
index → capture file line; full output in `line-attribution.txt`):

| case | flips (sample idx → file line) | note |
|---|---|---|
| `ip-octets-unbounded` | 44, 45, 64, 65, 67 | the out-of-range-octet lines are 44 (`256.100.50.25`), 45 (`123.456.78.90`), 64/65/67 (`172.16.0.256`) |
| `ip-no-left-boundary` | 44, 50, 63 | 50 and 63 are the labelled `abc`-prefix lines (L12/L22); **44 is an octet line** |
| `ip-no-right-boundary` | 62, 64, 65, 67 | 62 is the labelled `abc`-suffix line (L21); **64, 65, 67 are octet lines** |
| `no-ip-condition` | 38, 44, 45, 50, 62, 63, 64, 65, 67 | 9 flips = superset of the two rows above → coarse |
| `ip-before-date-only` | 35, 41, 59 (drops) | clean |
| `first-date-only` | 36, 42 (swaps) | clean |
| `date-no-left-boundary` / `date-no-right-boundary` | 57 / 56 | clean, one line each |
| `month-13/00`, `day-32/00` | 52, 53, 54, 55 | clean, one line each |

**Verdict on independence.** Two rows are not independent evidence, and they are not independent *of each
other*:

- `IPv4 not alnum-adjacent (7)` (`ip-no-left-boundary`, `ip-no-right-boundary`): 4 of the pair's 7 flips are
  lines the octet row owns. For `ip-no-right-boundary`, **only 1 of 4** flips is the boundary line it is named
  for — the missing trailing guard makes the regex read the invalid octet `256` as the valid address
  `172.16.0.25`. For `ip-no-left-boundary`, line 44 (`256.100.50.25` → `56.100.50.25`) is likewise an octet
  failure, not an adjacency failure. An auditor reading the pair as "evidence for line 7" is reading three
  quarter of an octet-range case.
- `octets 0–255 (4)` (`ip-octets-unbounded`): the same overlap seen from the other side; and three of its five
  *cited* lines are wrong (§ below).
- `only lines containing an IPv4 address (1)` (`no-ip-condition`) is coarse by construction (whole clause
  removed, 9 flips that include both rows above): it corroborates, it cannot attribute.

Four rows survive as independent, single-requirement evidence: `first-date-only`, the month pair, the day
pair, and the date-boundary pair. The date-boundary pair is the clean analogue the IP pair is not
(`date-no-left-boundary` flips exactly 57; `date-no-right-boundary` exactly 56).

**Row-by-row anchor corrections** (entry line numbers in parentheses; full table in the draft):

| entry row | cell as filed | measured |
|---|---|---|
| L83 `only lines containing an IPv4 address (1)` | "line 37 has a date and no IP" | line **38**; 37 is the comment `# Y: multiple dates, pick last` |
| L84 `last date on a line (2)` | "line 36 has two dates" | 36 ✓ **and 42** (`2018-05-05 8.8.8.8 info 2018-06-06`) |
| L85 `octets 0–255 (4)` | "lines 41–42, 62, 65, 67 carry 256 / 456" | **44, 45, 64, 65, 67**; 41, 42 and 62 carry no out-of-range octet; 45 and 64 are omitted |
| L86 `IPv4 not alnum-adjacent (7)` | "lines 60, 61 (`abc` before / after the IP)" | **63** (`abc10.0.0.5`, before) and **62** (`192.168.1.1abc`, after); 60 is a Y line, 61 a comment; the cited order is also swapped relative to the two cells |
| L87 `IP may sit after the date (1, implicitly)` | "line 38 puts the date first" | **35, 41, 59**; 38 has a date and **no IPv4 at all**, so it cannot decide a date-position case |
| L88 / L89 / L90 | "52, 53" / "54, 55" / "56, 57" | ✓ exact |
| L99 `month-length validity` | "(65, 67)" | ✓ exact |

**Why this matters more than the line numbers: the column invites a check the receipt cannot support.**
`corpus/evidence/round36/regex-log-probe.txt` has fields `case/predicted/observed/match/assertion/requirement`
— no per-line field — and **11 of the 16 failing cases carry a byte-identical `assertion=` string** (measured:
6 distinct assertion strings over the 16 fails, 7 over all 24 cases). Every case in the octet/boundary cluster
is one of those 11, so the receipt cannot distinguish which line decided them; the entry's `What decides it`
numbers are the only place that attribution exists, and four of the five cells there are mis-anchored. This
confirms D-RP1's count first-hand (11/16, 7 distinct) and raises its severity for *this* table.

## 5. Items (b) and (c): anchor drift and the S110 digest

**(b1) S110 span.** Both cells are imprecise, and the two files disagree. Measured on the pinned 19-line
`instruction.md` (`wc -l` → 19): requirement sentences at **1–4, 6–7, 9–10**; lines 5 and 8 blank; line 11 is
`Example Python usage:`; 12–19 the example code block. So the entry's `source:` line (`lines 1–11`) includes
one non-requirement line and `corpus/SOURCES.md:125`'s `instruction.md:1-19` includes eight. Drafted erratum:
exact bullet anchor `instruction.md:1-10`.

**(b2) `expected_dates` span — the round-36 spot-check is the drifted cell, not the lesson.**
`grep -n 'expected_dates = \[\|^    \]' test_outputs.py` → `71:    expected_dates = [`, `81:    ]`, and the AST
gives the nine element linenos `[72, 73, 74, 75, 76, 77, 78, 79, 80]`. The statement therefore spans **71–81**,
which is exactly what `corpus/lessons/round-36.md:18` says and what the entry's own `Oracle values | 71–81` row
says. The `72–82` recorded at `corpus/lessons/round-36-verifier-spotcheck.md:68` and `:91` as the correction is
wrong on both readings (72–80 are the literals, 81 the close, 82 blank). Likewise the lesson's
`lines 34-68` for `sample_logs` measures exact (`34:    sample_logs = [`, `68:    ]`). **No erratum to
`corpus/lessons/round-36.md` is warranted**; the erratum belongs in the spot-check file, and that is what I
drafted.

**(c) S110 digest.** `corpus/SOURCES.md:125` files
`4f7ac05e70cf922ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c` — 63 hex, first divergence at index 15
(`e` where the true digest has `0`, i.e. `…922ea0…` vs `…9220ea0…`). Correct 64-hex digest, copied from
`corpus/evidence/round36/tb2-regex-log/SHA256SUMS:3`:
`4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c`. Drafted as the one-line
`Erratum (round 37): S110 anchor sha256 …` form used elsewhere in `corpus/lessons/`, with both strings verbatim.

## 6. Findings and calibration

1. **The round-36 spot-check's own correction is off by one** (finding (b2)). It marked the entry's provenance
   and anchors "agree" while carrying a wrong span for the very row it was correcting — line-level anchors are
   evidently not being mechanically checked in assimilation. Cheap fix, worth a gate column: re-derive every
   `file:N-M` span in a knowledge entry from the capture and compare, instead of trusting the previous review.
2. **A `What decides it` column must be generated, not authored.** Four of its five line cells are wrong while
   every `Observed` verdict is right; the split is exactly "receipt-backed" vs "prose". Where a receipt has no
   per-line field, the honest cell is "the receipt cannot attribute this", or the attribution is produced by a
   committed script (as here).
3. **Independence is a property of the flip sets, not of the labels.** The entry's row for instruction line 7
   prints two cases and `fail, fail`; the pairs look like replication. Measured, the pair's flip set is 57%
   octet lines, and the right-boundary case is a 1-of-4 boundary case. The lane's convention should be: a row
   is independent evidence only if its flip set is disjoint from every other row's.
4. **The three structurally clean rows are the date-side ones** (`date-no-left/right`, month/day): the fixture
   authors built those as one-line traps and the IP side as overlapping traps. That asymmetry is the actual
   content behind R36RevProbePred's "confounded-2".
5. **Round-36's assertion truncation is confirmed first-hand** (11/16 identical) — no new defect, but it means
   the entry's unobserved rows (L96–L100) are the only claims in the table that do not depend on a line
   attribution the receipt cannot supply; they re-measure clean (`feb-29: []`, leading-zero-octet `[]`,
   `1134: []`, hardcoded alternation `== expected_dates`).

## 7. Touched surfaces

- Written (only here): `.ufo/waves/round-37/build/R37R36Absorb.md` (this report) and
  `.ufo/waves/round-37/build/R37R36Absorb/` — `errata-entry.md`, `errata-lessons.md`, `attribution.py`,
  `receipt-verdicts.py`, `line-attribution.txt`, `capture-digests.txt`, `anchors.txt`.
- Not written: the lane's `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`, `SKILL.md`,
  `PROVINCE.md`, `SHONEN.md`; the lane's git index and jj state; `/home/vgpnk/Projects/shokunin` root; sibling
  lanes; `/home/vgpnk/Projects/shokuknow` (not touched at all this seat).
- Tools installed/upgraded: none. Host `python3` is 3.14 (my runs); no pacman/uv/npx call.

## 8. Out of scope / known limits

- Drafts only: I did not edit the entry, the spot-check lesson, or `SOURCES.md`; the L1 integrates.
- No live re-fetch: digests were verified against the lane's own `SHA256SUMS` (5/5 OK), not by `curl` to
  `raw.githubusercontent.com`. If the L1 wants an upstream re-verify, that is a separate fetch.
- My attribution applies each frozen pattern to one line at a time. For these `^`-anchored, `MULTILINE`
  patterns this is equivalent to the grader's whole-text `findall` (the `(?=.*ip)` lookahead cannot cross a
  newline and the left boundary succeeds at a line start); the reproduction check (§3, 0 mismatches on 23
  file-mode cases) is the evidence for that equivalence, not an assumption.
- The `regex-file-absent` case (filesystem probe) was not reproduced; it is outside the items I was asked to
  absorb.
- I did not run the round-37 C1/C2 counters, the package gate, or any mutation campaign.
- The `R36RevProbePred` report's own per-line table (§7 there) agrees with my measured flip sets; I read it as
  data after measuring, not before.

VERDICT: absorb-drafted-4-errata
