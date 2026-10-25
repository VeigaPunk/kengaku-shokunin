# RevF9 — re-check of W3ReviewKengaku finding F9 (presence-based state census)

Reviewed at lane tip `3f371d2` (repo clean; only `?? .ufo/waves/`). F9 (kaika-w3
kengaku-review.md §9 Low): "plans/round24_census.sh:65–73 checks that headings or
strings exist (e.g. `grep -qE '^- \*\*D14 errata'`); `0/6` does not show SCORECARD
matches repo state." Axes: calibration.

## Verdict: **open (unfixed)** — pre-registration promises the fix, nothing fixed yet

- Fixing commit search: `git -C …/kengaku-shokunin log -S state_check --oneline --all`
  → only pre-registration commits (`2e56df3`, `5dd8c0f`, `2e0b320`, `3f371d2`),
  all adding `plans/round-25-claims.md` text. **No `plans/state_check.py` exists.**
  (`git log -S 'state_check.py' --all` → same 4 commits.)
- No post-review correction touches the census: `git show --stat e21f9ea` → 7 files
  (QUALITY, SOURCES, gate.md, 3 knowledge, round-24 lesson) — none is
  `plans/round24_census.sh`. No append-only correction (lane doc, LOG, report)
  addresses the presence-based defect. F9 is not superseded anywhere.
- The reviewer's own finding is now the lane's premise:
  `plans/round-25-claims.md:69-71` — "The round-24 census was presence-based
  (W3ReviewKengaku F9). C2 builds `plans/state_check.py` … exits 0 (all match) /
  1 (mismatch) / 2 (usage)". So: **acknowledged, scheduled, not yet built.**
- `grep -rn 'state_check' kengaku-shokunin` (working tree) → only
  round-25-claims.md. `plans/` at tip: no `state_check.py`, no `attrib_calibration.py`,
  no `fixtures/` dir.

## What the census actually checks (tip `3f371d2`, plans/round24_census.sh:63-73)

Re-run on a fresh `git archive` of `3f371d2` → `sh plans/round24_census.sh`:
`C2.scorecard_state_defects_open 0/6` (reproduces the stored value). Each of the 6
sub-checks is pure presence:

| d | check | script line |
|---|---|---|
| D10 | `awk` finds ≥7 re-derived axis rows in the `## Round 24` block | 65 |
| D11 | capabilities table has ≥1 row | 66 |
| D12 | saturation regex `saturation line: [0-9]+.*stagnation window N: [0-9]+` matches | 67 |
| D13 | `## Planned (round 25)` exists AND old plan marked `Superseded (round 24)` | 68 |
| D14 | literal grep `^- \*\*D14 errata` | 71 |
| D16 | any `^## Round 23 ` heading exists | 73 |

Presence-only counter-examples that a re-deriving checker would still flag (none
blocks the 0/6; they quantify how much the presence census misses):

1. D14's own errata cites a **stale line anchor**: SCORECARD.md:618 says
   `SCORECARD.md:305` "All 149 checks" is stale; the text sits at **:307**
   (`grep -n 'All 149' SCORECARD.md` → only :307). Two-line drift, exactly the
   class of defect a re-deriving state check exists to catch.
2. Round-24 table rows (SCORECARD.md:610-616) name **`PROVINCE.md` §Historical**
   as the coverage-cap basis, but PROVINCE.md contains no `## Historical` heading
   (`grep -n '## Historical' PROVINCE.md` → no match). An assertion row resolves to
   nothing its checker would re-derive.
3. The round-24 block has 8 axis rows; the census's `c>=7` floor plus `0/6` could
   not catch a wrong value — e.g. the novelty row "r21 'improved' verdict was never
   converted" is free text with no countable anchor at `:162`.

## Smallest append-only fix (lane-writer's move; I wrote nothing)

The pre-registered fix **is** the smallest one and is already correctly scoped
(claim + shared interface in `plans/round-25-claims.md:67-92`): build
`plans/state_check.py` under the round-25 C2 contract — re-derive P2a–P2e from the
repo, exit 0/1/2, frozen population P2 extracted from base bytes so later rows stay
out of scope. No census rewrite, no SCORECARD edit: the new script is additive and
`round24_census.sh` stays byte-frozen as historical evidence. Residual gap worth
recording for the writer seat (all outside my write rights):
- P2b as frozen does not require the table's `PROVINCE.md` §Historical basis rows
  to resolve (only backticked path/anchor + numeric claims) — §Historical is an
  unanchored heading; if P2b anchors are `:610-616` only, defect 2 stays invisible.
  Recommend the state-check seat also re-derive the D14-style stale-anchor class
  (assertion row cites a line anchor whose content moved), or F9 is only half-closed
  (re-derivation without stale-anchor detection).
- C2 selftest (claims `:90-92`) and P2a–P2e coverage should include one red case for
  the presence-check failure mode itself (mutate a re-derived value, keep headings),
  otherwise the new checker is only presence-with-more-steps.
- SCORECARD.md:618 anchor drift (:305 → :307) is a free appendix-only correction for
  the writer lane: appending "anchor is now :307" to the D14 errata row or the
  round-25 lesson is enough; no registry change needed.

No installs were needed (stdlib sh/git only).

VERDICT: F9 open at 3f371d2 — pre-registered fix (plans/state_check.py, C2) not yet built; smallest fix is exactly the pre-registered C2 build, plus P2b stale-anchor coverage for SCORECARD.md:618/:610-616 (PROVINCE §Historical unresolvable).
