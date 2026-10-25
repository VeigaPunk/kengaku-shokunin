# RevF12 — W3ReviewKengaku F12 recheck at lane tip 3f371d2

Axes (godspeed): calibration (accuracy of the entry’s coverage lineage). Read-only; no lane changes.

## Finding — OPEN (low severity)

- W3 finding: `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w3/kengaku-review.md:143` says the paired-eval entry’s “Extends the README ‘Statistical reporting’ coverage row” target was created this round, not present on the base map.
- At tip, `corpus/knowledge/paired-eval-uncertainty-reporting.md:32-34` still has that claim; `corpus/README.md:212` is the Statistical reporting row.
- Base `99cf615` coverage-map output contains the pre-existing planning-horizon row but no Statistical reporting row; the latter appears at `94da19e`. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log --oneline -S 'Extends the README' --all` → `94da19e ... round-24: SOURCES registry + 5 sourced knowledge entries ...` (creation, not a fix). Per-file history for the paired-eval entry likewise returns only `94da19e`.
- Post-review `e21f9ea` did not touch the paired-eval entry or `corpus/README.md`; its appended correction record in `corpus/lessons/round-24.md:116-141` does not mention F12. No later fixing change is present at 3f371d2.

## Smallest append-only fix

Append a dated `## Corrections` note to `corpus/knowledge/paired-eval-uncertainty-reporting.md`, leaving the landed text untouched. State that the README row (`corpus/README.md:212`) was created in the same round/commit as this entry (`94da19e`), so this is new coverage rather than an extension of that row; retain the true extension claim only for pre-existing paired work (r8/r11/r12 and `bench-arena-round7-noise-n25.md`).

Installs: none.
VERDICT: F12 is OPEN at 3f371d2; the existing README-row “Extends” claim needs an append-only correction.