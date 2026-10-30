# C3VacuityAttack — seat report (kengaku round 55, wave 1)

**Assignment:** falsify R55-C3's oracle — find cases whose prediction the
captured `chess-best-move` grader source underdetermines, deriving each verdict
independently from the assertion only, before the probe receipt lands.

## What I ran

1. Read the frozen claims (`plans/round-55-claims.md` @ 80afa613) — predicates,
   counters, kill rules fixed; no changes made or needed.
2. Read the captured grader
   `corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py` —
   one assertion: `Path('/app/move.txt').read_text().strip().split()` then
   `sorted(move) == sorted(["g2g4","e2e4"])`.
3. Read the frozen 12-case table in `plans/round55_c3_chess_probe.py` (CASES)
   plus its materialization path (`content.encode("utf-8")` → case-owned
   `/app`; sandbox ENV pins UTF-8; verdict rc0→P / "AssertionError"→F / else
   SETUP).
4. `sha256sum` of the captured grader → `a540714e…8f286` == frozen pin. **exit 0**
5. Independent derivation aid in my scratch dir (NOT the grader, NOT the probe,
   NOT bwrap): a small script applying only the two-line transformation named
   in the seat spec to the 12 frozen case byte strings, plus targeted
   language-semantics checks for the three called-out areas (CRLF translation,
   fullwidth-digit bytes, strip/split order). **exit 0, deltas=0**

Commands + exit codes are recorded inline above; no installs/upgrades were
needed (no pacman, no uv/npx). No subagents dispatched. No mutating git/jj
command run. Scratch: `/fast/scratch/hyaku/kengaku-r55/C3VacuityAttack/`
(deleted after this report; receipts copied here first).

## Findings

- **0 / 12 deltas.** Every frozen prediction is reproduced by deriving solely
  from `read_text().strip().split()` + sorted equality. Full 12-row table with
  exact bytes, token lists, sorted comparisons, and per-case reasoning:
  `.ufo/waves/round-55/w1/C3VacuityAttack/derivation.md`.
- **Called-out areas cleared:**
  - *crlf-line-endings*: `Path.read_text()` uses `newline=None` → universal
    newlines translate `\r\n`→`\n` (verified); redundantly, `split()` treats
    `\r` as whitespace. P is over-determined.
  - *fullwidth-unicode-digit*: bytes are exactly `b'g\xef\xbc\x92g4\ne2e4\n'`;
    U+FF12 is not whitespace and `'\uff12' != '2'` → token mismatch → F.
  - *whitespace-padded*: `strip` eats leading/trailing runs + trailing blank
    lines, `split` collapses interior runs → tokens exactly the two moves → P.
- **Vacuity sweep:** the oracle is total over the 12 cases — verdict mapping
  cannot fall into SETUP (file always written, bytes always valid UTF-8, only
  raising statement is the `assert`); semantics are version-independent
  (codepoint `sorted`, stable stdlib behavior); encoding is pinned twice over.
- **One nit (not a prediction risk, cannot fire the kill rule):** the frozen
  comment on the CRLF case names only the `split`-treats-`\r`-as-whitespace
  mechanism; the primary mechanism is `read_text`'s newline translation.
  Verdict identical either way; the R55-C3 kill rule targets miscounted
  mismatches, non-grader oracles, or upstream-identity failure — none present
  (sha256 identity verified).

## Files written

- `.ufo/waves/round-55/w1/C3VacuityAttack/derivation.md` (independent 12-row
  derivation table + delta analysis + vacuity sweep)
- `.ufo/waves/round-55/w1/C3VacuityAttack.md` (this report)

## Defects found

None. No sibling-owned file showed a defect from this seat's read-only scope;
nothing to report to the L1 for integration.

## Dead ends

None — the attack produced a clean negative result: the frozen oracle is fully
determined by the captured grader's own assertion for all 12 cases, so the
pre-landing prediction-risk surface is empty. This seat did not run the grader
or the probe, per bounds; the empirical check above re-implements only the
assertion's two-line transformation on the frozen case bytes in my own scratch.
