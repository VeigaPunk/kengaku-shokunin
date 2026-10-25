# RevF6 — W3 F6 re-check at lane tip 3f371d2 (calibration)

Axis: calibration (stale-pointer class = "entries match observed repo state"). Read-only; no writes outside this report. No tool installs (git/grep sufficed; pacman paused).

## Verdict: OPEN — born stale in 94da19e, never fixed

- `SCORECARD.md:567` is blank at tip; `SCORECARD.md:569` = `## Round 23 — stream-path leg forcing (executed 2026-10-16; NOT-ADMITTED; recorded round 24)`.
- Provenance: `git show 94da19e:SCORECARD.md | grep -n '^## Round 23'` → `569:` — the round-23 header sat at 569 **at the same commit that introduced the `:567` cites**. F6 never pointed at a true line; it is born stale, not line drift.
- No fix landed since the W3 review: `git -C <lane> log -S'SCORECARD.md:567' --oneline --all` → only `94da19e` (the introducing commit); `-S'SCORECARD.md:569'` → empty (the correct string never appears anywhere). `git diff 6180e4f..3f371d2 --stat` → only `considerthese/2026-10-20.md` + `plans/round-25-claims.md` (150 insertions).
- The round-24 post-review commit `e21f9ea` (ancestor of tip; author 2026-10-19 19:39:16 -03) fixed sibling W3 findings (S026 supersedes S023, gate caveat, two knowledge §Corrections, Q9/Q10) and added 32 lines to `corpus/lessons/round-24.md` — but both `:567` cites survived: `grep -c 'SCORECARD.md:567'` on `e21f9ea`'s version → 2. F6 was in the review's Low tier and was simply not actioned.
- Cites still live at tip: `corpus/lessons/round-24.md:24` (M14 fix cell) and `:54` (Round 23 disposition).
- Not a W3-style born-stale case: `git log -S` distinguishes introduced (`94da19e`) from fixed (absent) — a lane reviewer can reuse this two-grep pattern.

## Smallest append-only fix (never rewrite history)

Append at end of `corpus/lessons/round-24.md` (currently 141 lines):

```markdown
## Errata

- [2026-10-20] W3 F6 recheck: M14's fix cell and "Round 23 disposition" cite
  `SCORECARD.md:567`; that line is blank. The round-23 header was already at
  `SCORECARD.md:569` when 94da19e wrote these cites (born stale, no drift).
  Read both as `SCORECARD.md:569`. The `LOG.md:208` and `corpus/README.md`
  (`:89`, `:150-151`, `:166`) pointers re-verified 2026-10-20 and hold.
```

Append-only; no committed line is rewritten; the "no row is dropped" lesson preamble is respected. Every sibling pointer in those two lines re-verified at tip: `SCORECARD.md:163` (calibration 8, breach), `:165` (coverage 7), `:262` (r16 61-citation debt), `LOG.md:208` (round-23 heading, exact).

## Axis relevance

- C2 (state_check.py) P2b pins `SCORECARD.md:610-616` and P2c covers SHONEN pointers only — F6 sits outside the frozen population, so the mechanical state check will not fire on it. If the round wants pointer drift of `corpus/lessons/*.md` caught mechanically, that is an Amendment-registered assertion (L1's call; changes only status/recheck/used-by are registry-legal, and this is outside `corpus/SOURCES.md` anyway).
- The W3 lesson for the r25 instrument: `git log -S` on both the stale and corrected string is the cheap discriminator for "born stale" vs "fixed elsewhere"; worth a line in round-25 lessons only if mined with a red-before demonstration.

## Verification gaps

- `.ufo/waves/` exists untracked in the lane tree (`git status --porcelain` → `?? .ufo/waves/`); tip-identity checks (HEAD = 3f371d2, e21f9ea ancestor) are unaffected by it.
- Did not sweep the full repo for other cites of `SCORECARD.md:56[0-8]` outside `corpus/lessons/round-24.md` — grep found the pattern only in `.ufo` wave specs (dispatch copies of this assignment) and the lesson file.

VERDICT: F6 OPEN (born stale in 94da19e, missed by e21f9ea); smallest fix = append-only Errata section in corpus/lessons/round-24.md pointing both cites to SCORECARD.md:569.
