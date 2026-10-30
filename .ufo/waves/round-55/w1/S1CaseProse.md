# S1CaseProse — scoped findings (kengaku round 55, wave 1)

Seat: S1CaseProse (scribe). Deliverable:
`.ufo/waves/round-55/w1/S1CaseProse/case-requirements.md` (114 lines, 12 sections).
Full report with commands, exit codes, defects and dead ends:
`.ufo/waves/round-55/w1/S1CaseProse/report.md`. Receipt: `…/S1CaseProse/derivation.txt`.

## Result

Each of the 12 frozen R55-C3 chess probe cases is mapped to the instruction requirement it
exercises, quoting the S202 words; each section names the grader line
(`tests/test_outputs.py:25`, `assert sorted(move) == sorted(["g2g4","e2e4"])` over
`move = Path("/app/move.txt").read_text().strip().split()` at :23), why the predicted verdict
follows from that one assertion, and what a contrary verdict would mean (a grader finding vs an
instrument/oracle defect). A Q28-shaped requirement map and a gaps list close the file.

## Checks run

- `sha256sum` of the in-repo grader capture → `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286`
  = the frozen S201 pin; `grep -n assert` → the assertion is at line 25 (the only one).
- `curl` (read-only GET) of the upstream `instruction.md` at commit `2fd12b88…` → 260 bytes,
  sha256 `6ba25be4e291a4ad04ae42b2dddefcdaef67ca45ca9d5dce661a2e517b19ce7a` = the S202 row's pin.
- `python3 derive_cases.py` → exit 0, `cases=12 derived_agree=12 disagreements=[]` — all twelve
  verdicts re-derived from the assertion alone (not a grader run; the bwrap battery is E5/E6's).
- Cross-check: `plans/round55_c3_chess_probe.py:56-78` (E5, landed 12:28) reproduces all 12
  frozen names, byte strings and predictions verbatim.
- No mutating git/jj command anywhere; scratch `/fast/scratch/hyaku/kengaku-r55/S1CaseProse/`
  deleted before yielding; no tool installed.

## Defects reported (sibling-owned files not edited)

1. `plans/round55_c3_chess_probe.py:67` — the `duplicate-move` comment says the multiset is "short
   of 'g2g4'"; it is long by one extra `e2e4` (cardinality 3 vs 2). Comment only, prediction `F`
   is right, but it is the sentence a later reader would cite as the mechanism.
2. `plans/round55_c3_chess_probe.py:73` — the `crlf-line-endings` comment omits that `read_text()`
   in text mode already does universal-newline translation, so `\r` never reaches `split()`.
3. Coverage gaps in the frozen table (grader-side, not file defects): a missing `/app/move.txt`
   and non-UTF-8 bytes would be SETUP rather than FAIL under the instrument's classification, and a
   non-breaking space separator **PASSES** (verified locally) — no case covers it.
4. For E7: the instruction's board-image requirement is exercised by no case (the grader never
   opens `chess_board.png`), so under Q28 it must be recorded as untested, not mapped to a case.

## Dead ends

Deliverable first drafted at 183 lines (over the 120-line cap) → rewritten 127 → trimmed to 113;
a bulk blank-line removal also stripped the space after `###`, breaking heading syntax, repaired on
read-back. No prior-round precedent for this artefact shape exists to copy. No grader/bwrap run
was performed here, so no `observed=` value is claimed from execution.
