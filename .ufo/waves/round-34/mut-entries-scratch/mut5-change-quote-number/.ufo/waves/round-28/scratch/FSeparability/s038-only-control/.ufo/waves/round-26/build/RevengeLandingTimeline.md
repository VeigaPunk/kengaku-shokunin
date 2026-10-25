# Round-25 landing timeline — M39 evidence

Axis: calibration (timing and provenance of the Q10 admission evidence).

- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show -s --format='%H %cI' 3f371d2 710409f 8ea41f9 8239a56 9d8a00d` returned:
  - `3f371d2a2ce5ccf1b40b2161210f6591a8320a0a` — `2026-10-20T21:11:53-03:00`
  - `710409fb219f93dbb5beee281a986ec8499bd2ce` — `2026-10-20T21:25:18-03:00`
  - `8ea41f9ed8ba0ee8dd1bcf31cb83d9b5c589092b` — `2026-10-20T21:44:48-03:00`
  - `8239a56691969b1bc34e7ccdc432c100ff7620ef` — `2026-10-20T22:01:48-03:00`
  - `9d8a00d2a69b83a1e83eb41e1d2ee840910949e4` — `2026-10-20T22:15:58-03:00`
- First-parent search `git log --first-parent --reverse -S 'wave-2 seats' --format='%H %cI %s' -- corpus/lessons/round-25.md` returned only `8ea41f9ed8ba0ee8dd1bcf31cb83d9b5c589092b 2026-10-20T21:44:48-03:00 round-25: interval-calibrated attribution verdicts (C1), state assertions re-derived (C2), sources S027-S037, lesson, wave-1 evidence`. Thus Q10 wording first appeared in the admission commit at 21:44:48 -03.
- `corpus/lessons/round-25.md:29` at that landing says Q10 was re-derived by a second parser “and by wave-2 seats”; it names no wave-2 report path. `git diff 710409f 8ea41f9 -- corpus/lessons/round-25.md` shows the lesson (including this row) added there.
- Landing-tree check `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin ls-tree -r --name-only 8ea41f9 -- .ufo/waves/round-25/falsify` returned no paths. The admission commit's tree therefore had no falsify reports to support its generic wave-2 citation.
- Current filesystem `stat` mtime census, sorted over `.ufo/waves/round-25/{build,falsify}/*.md` (timezone -0300): build first `2026-10-20 21:16:39.879179437` `.ufo/waves/round-25/build/SrcScipyBinomtest.md`; build last `2026-10-20 21:57:54.555796619` `.../build/StateCheckExec.md`. Falsify first `2026-10-20 21:47:51.766155398` `.../falsify/ScribeMisrootSweep.md`; falsify last `2026-10-20 22:15:37.433364374` `.../falsify/RevScorecardR25.md`. These are filesystem mtimes, not commit timestamps.
- The earliest falsify file is a fleet-root misroot sweep, not a Q10 source reread (`.ufo/waves/round-25/falsify/ScribeMisrootSweep.md:1-4`). Q10-related source reopens are later: `ReopenS027.md` mtime 21:50:29.932918699; `ReopenS034.md` 21:51:07.529229152; `ReopenS032.md` 21:51:28.926053277; `ReopenS030.md` 21:54:59.877093826 (-03). `corpus/lessons/round-25.md:73` identifies these rereads as the Q10 second-seat review.
- Timing gap: the Q10 admission landed at 21:44:48; even the earliest `.md` mtime in falsify is 21:47:51, and the cited source rereads above are later still. This confirms evidence cited before it existed in the landing tree (M39 / R26-E4; see `plans/round-26-claims.md:18-24`).
- Scope note: `plans/round-26-claims.md:18` calls 21:49:53 the “first wave-2 report.” The observed first mtime among *all* falsify Markdown files is earlier, 21:47:51; the file then is not a second-seat source reread. Keep those scopes distinct rather than treating 21:49:53 as the directory's earliest report mtime.

VERDICT: M39 confirmed — Q10's generic wave-2 support was absent from the 8ea41f9 landing tree and the relevant second-seat rereads followed admission; installs: none.