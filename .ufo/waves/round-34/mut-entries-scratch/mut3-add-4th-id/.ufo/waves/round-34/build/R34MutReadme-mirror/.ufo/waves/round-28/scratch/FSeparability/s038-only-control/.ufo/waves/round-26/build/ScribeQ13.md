# ScribeQ13 — Q13 draft and evidence (round 26, build)

Seat: KengakuR26-2.ScribeQ13-4. Scope: draft QUALITY Q13 (style of Q9/Q10); read-only on the live tree.
This seat wrote nothing in `corpus/`, `plans/`, or the lane's git/jj state.

## Draft Q13 (integrator lands after Q12 at `corpus/QUALITY.md:90-95`, before `## Round-closure criteria` `:108`)

```
- **Q13 — a Gate row cites only reports its landing commit already contains (extends Q10).** An entry is
  admitted only in a commit whose tree already holds every second-seat (Q10) re-read report that its `## Gate`
  row cites; the cell names each report by repo-relative path (`.ufo/waves/round-<N>/<wave>/<Seat>.md`), and a
  generic seat reference ("wave-2 seats", "falsify seats", "by wave-N") supports nothing. Check:
  `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-<N>.md --commit <landing>` exits 0;
  red-before: `--lesson corpus/lessons/round-25.md --commit 8ea41f9` exits 1 on the Q10 cell
  (`round-25.md:29`, "by wave-2 seats", no path).
  Lesson: `corpus/lessons/round-26.md` M39; `corpus/lessons/round-25-verifier-spotcheck.md:36-39`.
```

## Findings

1. **A Q13 already sits uncommitted in the live tree.** `git status`: ` M corpus/QUALITY.md` (+11 lines);
   `git show HEAD:corpus/QUALITY.md | grep -c 'Q13 —'` → `0`. Live text: `corpus/QUALITY.md:97-106`. Substance
   matches the draft; it is ~2x Q9/Q10 length. Not touched; integrator chooses. Author of that edit: unknown.
2. **Red-before facts are tree facts, not mtimes.**
   - `git ls-tree -r --name-only 8ea41f9 .ufo/waves/round-25/ | grep -c 'falsify/'` → `0`.
   - First commit adding falsify reports: `8239a56` (2026-10-20 22:01:48 -0300); its tree holds `83`
     (`git ls-tree -r --name-only 8239a56 .ufo/waves/round-25/falsify | wc -l`). `8ea41f9` is its ancestor.
   - Landing `8ea41f9` is 21:44:48 -0300; gap to first committed falsify report = 17 min.
   - `git show 8ea41f9:corpus/lessons/round-25.md | sed -n 29p | grep -o 'by wave-2 seats'` → `by wave-2 seats`.
3. **"Five minutes" rests on a filesystem mtime.** `round-25-verifier-spotcheck.md:38` and
   `round-26-claims.md:3-4` cite "first wave-2 report mtime 21:49:53". On-disk top-level mtimes in
   `.ufo/waves/round-25/falsify/` start at 21:47:30 (`swarm-registry.json`) and 21:47:51
   (`ScribeMisrootSweep.md`); no 21:49:53 file was in that listing. Mtimes do not survive checkout reliably.
   Recommend citing the tree counts (item 2), not the mtime.
4. **Check command not yet runnable.** `plans/gate_timing_check.py` is absent in the live tree and at
   `e0037a8` (`git cat-file -e e0037a8:plans/gate_timing_check.py` → exit 128); `corpus/lessons/round-26.md`
   is absent in the live tree. Q13's Check and the M39 citation stay pending until those land.
5. **Citation verified.** `corpus/lessons/round-25-verifier-spotcheck.md:36-39` is the "Report defect
   (status-neutral)" bullet, matching pre-registration row R26-E4.
6. **Q10 cell.** `round-25.md:29` (at 8ea41f9) also cites `plans/fixtures/r25/attrib_oracle.sh` (a parser, not a
   seat report, present at 8ea41f9). Only the generic "by wave-2 seats" fails the Q13 rule; the red-before
   exit-1 expectation holds on that cell.

## Installs / updates

None.

## Files written

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-26/build/ScribeQ13.md` (this report only).

VERDICT: Q13 draft ready (short form above); the live tree holds an uncommitted 11-line Q13 at
`corpus/QUALITY.md:97-106` for the integrator to reconcile; red-before rests on 0 vs 83 committed falsify
reports, not the 21:49:53 mtime; the check is blocked until `plans/gate_timing_check.py` lands.
