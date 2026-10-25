ATTACKS: plans/round25_census.sh (tip sha256 70f92470…) — tip 8ea41f9ed pristine, 6180e4f/3f371d2 archives, per-key independent re-derivation, mutations, YAML differential
Seat KengakuR25.RevCensusScript; scratch /tmp/k25w2-RevCensusScript/ (tip/ base/ base2/ prereg/ clone/ mut/ sib/; indep.py fuzz_triggers.py mutate.py).
## Survives (evidence)
- Base: `cd base2 && sh plans/round25_census.sh` (6180e4f archive, script copied in) → 14 keys + `exit=0` byte-identical to
  `corpus/evidence/round25-calibration/round25-census-before-6180e4f.txt:2-16` (diff rc 0). 3f371d2 archive → same output
  (header :5 names 3f371d2; `git diff --stat 6180e4f 3f371d2` touches only considerthese/ + plans/round-25-claims.md).
- Tip, every key re-derived without the script's awk/grep, all equal: python header-named table parse; fleet gawk CLI
  `scripts/sources-census.sh census --file tip/corpus/SOURCES.md` → rows 37, A34 B1 C2, mined26 queued8 rejected3 (base 26,
  A24 C2, 18/5/3), `validate` → `ok` both; `cut -d'|' -f10 | grep -c '^ *2026-10-20 *$'` → 11 = ids >S026 = S027–S037;
  `find corpus/knowledge -maxdepth 1 -type f -name '*.md'` → 33 (base 32; +attribution-interval-calibration.md);
  `sed -n '/^## Mistakes$/,/^## /p' | grep -cE '^\| M[0-9]+ \|'` → 8 (M23–M30); PyYAML 6.0.3 description → 6 triggers
  ('model evaluation' … 'novelty pricing'); SHONEN python parse 1,1,1,1. calib/state_check summary lines and exits equal
  `attrib-calibration-summary.txt:49-50` and `state-check-after.txt:1,15`; full calib stdout = receipt body.
- Read-only: `strace -f` on a full run → 0 successful write-mode opens (1 failed `/dev/tty` O_RDWR, shell startup); tree
  listing + `git status --ignored` unchanged. head: clone@8ea41f9 → `8ea41f9`; symlinked cwd → `8ea41f9`; archive nested in a
  foreign repo → `n/a`. Usage: arg → 2, non-lane cwd → 2. Output identical under C/C.UTF-8/en_US.UTF-8 and gawk --posix/--traditional.

## Breaks (by severity)
1. MEDIUM — `skill_frontmatter_triggers` claims a count "after YAML unquoting" (:22-23, :98-108) but prints a number for
   frontmatter that is not YAML. Base receipt `skill_frontmatter_triggers=0`; PyYAML on base SKILL.md → `ScannerError: mapping
   values are not allowed here` (line 2 col 264, `Rank: shonen.`); Bun 1.4.3 `Bun.YAML.parse` → `Unexpected token`. The before
   state was "unparseable" (D18; FrontmatterScribe.md:9-13), so the key cannot witness LOG.md:289 "now parses as YAML" — that
   claim is TRUE at tip (both parsers OK), but only an independent parse shows it. Differential on 18 fleet SKILL.md copies:
   8/8 YAML-valid agree (chousa 5, kengaku 6, kotoba 8, kotodama 9, lore 5, mori 5, souji 11, tameshi 0 — build predictions hold);
   10/10 YAML-invalid still get numbers (game-dev-3d 6, kaidoku 5, eight others 0). Fuzz (seeds 25, 7; 1200 cases): YAML-valid
   1084/1091 agree; YAML-invalid 109/109 printed numerically.
2. LOW-MED — doc/impl drift: :24-27 "last non-empty stdout line … the same for state_check"; :179 keeps the last
   `^(TOTAL |assertions=)` line (integrator edit after build sha fdc72b62…, CensusScriptExec.md:19 records the old rule). At tip
   the documented rule yields `VERDICT: PASS — all comparable frozen assertions match`; the census prints `assertions=236 …`.
3. LOW-MED — `shonen_evidence_lines_per_box` titled "(canonical form: exactly 1)" (:83) reads 1,1,1,1 at base, where the
   form was non-canonical: `state-check-before-6180e4f.txt:3-6` MISMATCH `P2c.box.1-4.pointer-only`; `diff base/SHONEN.md
   tip/SHONEN.md` = 4 prose lines → `SKILL.md:23`-style pointers. The key counts lines, is blind to the D17 repair.
4. LOW — `lesson_mistake_rows_r25` (:78) `^\| M` row pattern is looser than round 24's `^\| M[0-9]+ ` (round24_census.sh:50):
   mutation header `| Mistake |` → 9 (8 rows). Silent `0`, not `absent`, for `## Mistakes ` trailing blank, CRLF, 1-space-
   indented rows, or deleted heading. Tip unaffected (header `| id |`).
5. LOW — valid-YAML edges diverge (mut/F*): `"\u2018a\u2019, \x22b\x22"` → census 0 vs YAML 2; CRLF frontmatter → `absent`
   vs 6; `description :` → `absent` vs 6; `description: # 'x' 'y'` (YAML null) → 2; block-sequence value counted as text.
6. LOW — `knowledge_files` says "regular files" (:16) but `[ -f "$f" ]` (:71) follows symlinks: added symlink → 34 vs 33.
7. INFO — sources keys are frozen-v1 column-zero (contract-faithful): 2-space-indented S037 → rows 36 vs fleet CLI 37
   (CORPUS.md "Maintained parser note"); `\|` in a cell → malformed 1, new_rows 10. Tip: 0 indented, 0 escaped pipes.
8. GAP — SCORECARD.md:657-658 makes this script the round's counting command, but no after receipt landed (only
   `round25-census-before-6180e4f.txt`; round 24 landed after.txt, SCORECARD.md:590-594). No census after-value is cited, so
   none is contradicted. Tip values (this run): rows 37, malformed 0, A=34 B=1 C=2, mined=26 queued=8 rejected=3, new_rows 11,
   knowledge 33, mistakes 8, shonen 1,1,1,1, triggers 6, calib_exit 0, state_check_exit 0.

Residual risk: no dash/busybox on host (/bin/sh → bash), so POSIX conformance was tested only via gawk --posix/--traditional; the fleet
SKILL.md copies are live working-tree reads (2026-10-20), not pinned commits, so they test the instrument, not those lanes.

Installs: none (existing PyYAML 6.0.3, Bun 1.4.3, strace, gawk 5.4.1; `git clone` into scratch only).
VERDICT: PARTIAL — every key the census prints at the tip and base survives independent re-derivation, and the base receipt reproduces byte-for-byte; the instrument overclaims (a YAML count printed for unparseable YAML, including the base value, and a "canonical form" SHONEN key blind to D17), and its header misdocuments the summary-line rule.
