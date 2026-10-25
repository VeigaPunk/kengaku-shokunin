# ScribeEntrySkeleton — round 26 (C1 knowledge entry skeleton)

Seat: KengakuR26-2.ScribeEntrySkeleton-4 (writer, leaf, no delegation). Base: e0037a8da268.
Private clone: /tmp/kengaku-r26-ScribeEntrySkeleton, branch r26-ScribeEntrySkeleton, commit fff9bd2.

## Behavior
Drafted the skeleton of the C1 knowledge entry in the order requested: provenance triad first
(`source:` / `verified-at:` / `recheck:`), Claim, Method, Population, Families, Results, What this does not
establish, Extends, How kengaku applies it, Rejected, Corrections. Every numeric slot, quote, and
observed result is `TO-FILL`; no number, verdict, or quote was typed. Predicted p(PASS) values are copied
from `plans/round-26-claims.md` §C1 (pre-registered, code-derived).

## Placement (Q13 / pre-registration)
Draft written to `drafts/round-26/grader-perturbation-audit.md` in the clone, NOT `corpus/knowledge/`.
Reason: `round-26-claims.md` §Q13 says the C1 entry is drafted outside `corpus/` and admitted only in a commit
that also lands the wave-2 re-read reports it cites. The admit target remains
`corpus/knowledge/grader-perturbation-audit.md`. Integrator (KengakuR26-2) moves it at admit time.

## Sources and facts used (verified by read in the clone at e0037a8)
- `grader.py:121` `extract_json_block`, `:221` `grade_state`, `:247` `grade_c`, `:2115` `grade_seq` — `grep -nE '^def …'` output matches the claims file.
- `extract_json_block` takes the last fenced block first (`blocks[-1]`), then falls back to brace scanning — read at `grader.py:121-134`.
- Population files exist; `wc -l`: round8 268, round9 284, round11 1473, round12 4114.
- `plans/attrib_calibration.py:144` `clopper_pearson` exists.
- `corpus/README.md` Frontier names "Judge calibration applied inward" (line 253); it is partly discharged for the attribution receipts only (line 254–255), so this entry is the named remaining gap.
- SOURCES rows S009, S010, S011, S012, S027, S028 exist in `corpus/SOURCES.md` (existing rows, not re-opened here). SOURCES currently has 93 lines; S040–S042 present.

## Not done (by design, not omitted)
- No instrument run (`plans/grader_perturb.py` is a wave-1 build item; absent at base). No numbers filled.
- No new SOURCES rows; no prior-art search performed by this seat (the skeleton lists search slots, marked TO-FILL). Candidate leads (CheckList INV/DIR, arXiv 2005.04118) are unopened and not cited as sourced.
- No edits to the live lane tree, its jj/git state, MANIFEST, or `corpus/`.

## Findings
- F-1 corpus/knowledge is the admit path only; drafting there now would violate Q13 ordering (claims §Q13, last paragraph).
- F-2 D1 prediction (p=0.03) rests on `blocks[-1]` at `grader.py:122-124`; this is the single code path the D1 family should stress. Recorded as code-derived in the skeleton.
- F-3 Frontier item "Judge calibration applied inward" wording at `corpus/README.md:253` says "S010-style perturbation audit … remains frontier"; this entry discharges that only if the instrument lands and the Results table is filled from its output.

## Installs / updates
None. No tool installed or upgraded. (pacman paused host-wide; no install was needed for a Markdown skeleton.)

## Files written
- `/tmp/kengaku-r26-ScribeEntrySkeleton/drafts/round-26/grader-perturbation-audit.md` — 153 lines, sha256 `150a1c7815c0a3ed799570a5f02e4a9e2ac11b19dc5c6261f91978ba422bc23f` (committed fff9bd2 in the clone).
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-26/build/ScribeEntrySkeleton.md` — this report (own report file only; directory created by `mkdir -p`).

## Checks for the main agent (not run by this seat)
- `python3 plans/grader_perturb.py --summary` once the instrument lands (exit 0 required) → fill the Results table from its output only.
- `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-26.md --commit <landing>` at admit.
- Census `scripts/sources-census.sh validate` after SOURCES rows are added.

VERDICT: skeleton drafted with every numeric and quoted slot marked TO-FILL; draft placed outside corpus/ per Q13 ordering; no numbers, quotes, or installs invented or performed.
