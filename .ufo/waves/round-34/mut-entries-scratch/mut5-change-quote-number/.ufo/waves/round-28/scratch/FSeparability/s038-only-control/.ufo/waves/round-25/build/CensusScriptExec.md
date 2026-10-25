# CensusScriptExec — round 25 build (writer, private clone)

Seat `KengakuR25.CensusScriptExec`; clone `/tmp/kengaku-r25-CensusScriptExec`, branch `r25-CensusScriptExec`;
observed base `git rev-parse HEAD` → `3f371d2a2ce5ccf1b40b2161210f6591a8320a0a`. Not committed (KengakuR25 integrates).

## File changed
- `plans/round25_census.sh` — new, 187 lines, mode 755 (as `plans/round24_census.sh`), sha256
  `fdc72b621052d61b37004d29a21d7c22223bfeb6a0df6d26f1c987cc481ba2c8`. `git status --short` → `?? plans/round25_census.sh` only.

## Behavior
POSIX sh, lane root, no arguments → key=value lines, exit 0; exit 2 on any argument or a cwd lacking `SKILL.md`+`corpus/`.
Read-only: python runs with `PYTHONDONTWRITEBYTECODE=1`; after the run `git status --short` shows no new path.
- `sources_rows/_malformed/_tier_histogram/_status_histogram`: contract-v1 grep/awk verbatim (`CORPUS.md:135,137,139,141`); histogram tokens sorted (C locale) since awk `for (k in n)` order is unspecified.
- `sources_new_rows_r25`: NF==13 rows whose `opened` ($10) is 2026-10-20; a column-shifted row is not misread and is counted by `sources_malformed`.
- `knowledge_files`: regular `corpus/knowledge/*.md` (same population as `plans/round24_census.sh:13`).
- `lesson_mistake_rows_r25`: `^\| M` lines inside `^## Mistakes$` up to the next `^## `; `absent` without `corpus/lessons/round-25.md`.
- `shonen_evidence_lines_per_box`: one count per `- [?]` box, comma-joined (canonical = 1 each, `PROTOCOL.md:432`).
- `skill_frontmatter_triggers`: quoted strings in frontmatter `description` after undoing YAML scalar style (block/double/single/plain).
- `calib_summary`, `state_check_summary`: last non-empty stdout line of `python3 plans/<x>.py --summary`, else `absent`.
- `head`: short HEAD only when cwd is itself a git toplevel, else `n/a`.

## Base output — `cd /tmp/kengaku-r25-CensusScriptExec && sh plans/round25_census.sh; echo census_exit=$?`
```
head=3f371d2
sources_rows=26
sources_malformed=0
sources_tier_histogram=A=24 C=2
sources_status_histogram=mined=18 queued=5 rejected=3
sources_new_rows_r25=0
knowledge_files=32
lesson_mistake_rows_r25=absent
shonen_evidence_lines_per_box=1,1,1,1
skill_frontmatter_triggers=0
calib_summary=absent
calib_exit=absent
state_check_summary=absent
state_check_exit=absent
census_exit=0
```
Internal consistency: tier 24+2 = status 18+5+3 = rows 26.

## Decisions beyond the literal key list (no requested key changed)
1. `calib_exit`/`state_check_exit` added: per the shared interface, exit 0/1/2 is each instrument's verdict; a last line alone cannot tell exit 0 from exit 1.
2. YAML-aware trigger count: fleet descriptions use a `"…"` scalar holding `'…'` triggers (`chousa-shokunin/SKILL.md:3`, `mori-shokunin/SKILL.md:3`), a `>` block holding `"…"` triggers (kotoba, lore), or a plain scalar (kengaku). A naive `"` pair count gives 1 for chousa (true 5) and 1 for `tameshi-shokunin/SKILL.md:3`, a quoted scalar with 0 triggers.
3. `head` guard: a `git archive` export nested inside another repo would otherwise report that repo's HEAD.

## Risks / open
- Only the base paths ran (wave rule: no tests mid-flight); the quoted/block-scalar and python-present branches are unexercised. Predictions for L1's post-integration check, read-only — `(cd /home/vgpnk/Projects/shokunin/<lane> && sh /tmp/kengaku-r25-CensusScriptExec/plans/round25_census.sh) | grep triggers`: chousa 5, mori 5, kotoba 8, lore 5, tameshi 0 (all five have SKILL.md + corpus/).
- `^\| M` (as specified) also matches a header row starting `| M…`; round-24's header is `| id |` (`corpus/lessons/round-24.md:9`); round-24's census used the stricter `^\| M[0-9]+ ` (`plans/round24_census.sh:50`).
- `'` pairs only at ASCII word boundaries: `rock 'n' roll` counts 1; a UTF-8 letter before `'` reads as a boundary.
- Index parity: `corpus/README.md` has no row for `plans/round25_census.sh` or `plans/round-25-claims.md` (grep `round2[45]_census|round-25` → only `:171`, the round-24 census row). README row + LOG entry are L1's.
- `/bin/sh` → `/usr/bin/bash` (`readlink -f /bin/sh`); no dash/busybox on host, so POSIX conformance rests on constructs (no `local`/arrays/`[[`/`echo -e`; POSIX awk functions only), not a dash run.

Installs: none.

VERDICT: plans/round25_census.sh landed in the private clone (uncommitted); base run at 3f371d2 prints 14 keys, exit 0, and writes nothing.
