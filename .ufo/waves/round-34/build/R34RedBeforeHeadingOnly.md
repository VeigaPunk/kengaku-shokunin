# Round 34 heading-only red-before receipt

Scope: calibration axis — heading-only mutant class. Used a temporary sandbox export; the lane SCORECARD.md was not edited.

Evidence captured in `.ufo/waves/round-34/falsify/red-before/heading-only.txt`: append an empty `## Round 33` section, then run the naive grep. Output includes the appended heading at line 1156 and `exit=0`, despite no section content. The existing Round 33 heading in the source export was at line 1123, so the appended heading is explicitly distinguished.

No tools installed or tests/builds run. No blockers.

VERDICT: red-before-heading-only green-on-empty (proven)
