# ScoutSourcesUsedBy — S043–S048 used-by cells vs actual citations (base b5719440)

Method: `git -C kengaku-shokunin grep -n 'S04[3-8]' b5719440 -- corpus plans` → 79 hits, 15 files, exit 0.
Cells parsed from `git show b5719440:corpus/SOURCES.md` (SOURCES.md:65-70); identical at HEAD 11a7fc8c64dc (cells unchanged).
Axes: novelty/calibration; this serves C2 P4e (plans/round-27-claims.md:119).

## Convention (what a used-by cell may legally contain)
Across all 48 rows at base, used-by cells contain ONLY: corpus/knowledge/* ×35, corpus/lessons/* ×6, `—` ×12.
Zero cells ever list README, plans/, or evidence receipts. So "files that actually cite" must be scoped to
knowledge+lessons, or every id false-mismatches. QUALITY.md has no used-by rule (grep 'used-by' → 0 hits);
round-27-claims.md:119 is the only written definition.

## Per-id table (cell vs citing files at b5719440)
| id | used-by cell | in-class cites (knowledge+lessons) | out-of-class cites (never cell targets) | verdict |
|---|---|---|---|---|
| S043 | lessons | lessons/round-26.md:47,54,59,66,81-83,99; knowledge/grader-perturbation-audit.md:1 (supersession pointer ONLY: "(supersedes S043 location)") | README:268,283-284 (ranges/history); round26-sources/gate.md:5,34; p3-oracle-*.txt "S043+ excluded" markers; p3_oracle.sh:11,128,142,216,273,411-412; state_check.py:212; round-26-claims.md:203; census.json:146; SOURCES.md:65,92 | MATCH iff pointer≠use (see F2) |
| S044 | lessons+knowledge | lessons:48,79,126; knowledge:1,3,20 | README:62,230 (Covers "S044–S046, S048"); gate.md:6; census.json:147; SOURCES.md:66,92 | MATCH |
| S045 | lessons+knowledge | lessons:36,49,79,126,128; knowledge:1,19 | gate.md:7,25-26; census.json:148; round-26-claims.md:199 (substantive prior-art use, plans class); SOURCES.md:67,92 | MATCH |
| S046 | lessons+knowledge | lessons:50,54,79,145; knowledge:1,3,48 | README:62,230; gate.md:8; census.json:149; SOURCES.md:68,92 | MATCH |
| S047 | lessons | lessons:51,54,81-82,126 (knowledge: zero mentions) | README:268,278,283; gate.md:9; census.json:150; SOURCES.md:69,92 | MATCH |
| S048 | lessons+knowledge | lessons:59,66,79,81,83,99,186; knowledge:1,3,18 | README:62,230,284; gate.md:32-40 (errata); p3b-new-source-control.txt:1-2; recovery-start.txt:8 + sources-census-final.txt:4 (W04 duplicate-URL warning = deliberate S043/S048 same-URL supersession); census.json:151; SOURCES.md:70 | MATCH |

No phantom entries: every cell-listed file literally cites its id. All raw surface mismatches are under-listings
outside the cell class — convention-consistent, not cell errors.

## P4e findings (for ExecStateCheckV4 / C2)
- F1 (spec pin): the citing-file universe for P4e MUST be {corpus/knowledge/*, corpus/lessons/*} — the only
  classes any of 48 cells ever names. A whole-corpus token scan flags ~13 file-id pairs that are receipts,
  census markers, or README history. Hard-exclude: SOURCES.md self, evidence receipts (gate.md = per-row
  provenance), plans/ (incl. round-26-claims.md:199), README, population markers ("S043+ excluded").
- F2 (only genuine content ambiguity — S043): knowledge/grader-perturbation-audit.md:1 contains literal S043
  inside the supersession pointer; S043's cell is lessons-only. Intended truth per lessons/round-26.md:66
  ("The draft now cites S048; the historical S043 row … superseded") and :81 ("S043/S047 remain lesson-only").
  Pin: a mention inside a "(supersedes X …)" parenthetical is NOT a use. Literal-token P4e without this rule
  reports 1 mismatch (S043) and is wrong; with it, 6/6 cells exact.
- F3 (range mechanics): en-dash ranges carry only endpoints as tokens — README:62/:230 and knowledge:3
  "S044–S046" do not contain literal S045 (S045 is cited at knowledge:1,19 anyway). No verdict changes, but
  the --selftest fixture should include a range case so the red-state is exercised honestly.
- F4 (expected outcome at base): with F1+F2 pins, P4e = 6 assertions, 0 mismatches on S043–S048. Any v4 run
  showing a P4e mismatch on these ids means the pin, not the corpus, is wrong.
- F5: cells identical at base and HEAD (11a7fc8c64dc) for all six ids — findings hold at both revisions.

Commands+exits: grep above (exit 0, 79 lines); `git show b5719440:corpus/SOURCES.md` parse (exit 0);
`git rev-parse HEAD` → 11a7fc8c64dc; `git status --porcelain` → only untracked .ufo/waves/round-27/.
Note: contract RULES path /home/vgpnk/Projects/shokunin/.omp/agent/RULES.md absent; read /home/vgpnk/.omp/agent/RULES.md (matches tooling directive). No installs (git+python3 sufficed).

VERDICT: all six S043–S048 used-by cells are exact under the registry's own knowledge+lessons convention; the single P4e trap is S043's supersession pointer at grader-perturbation-audit.md:1, which a literal-token checker would wrongly flag.
