# R29a2LessonDraft — attempt-2 `## Mistakes` rows (draft only)

Seat: `L1Kengaku29.R29a2LessonDraft` (leaf scribe). Round 29 attempt 2, 2026-10-25.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

## Behaviour

Drafted five additive `## Mistakes` rows (proposed ids M99–M103) for round 29 attempt 2 at
`/tmp/r29a2-LessonDraft/mistakes.md`, in the lesson's existing four-column shape
(`corpus/lessons/round-29.md:159-160`: id · class · evidence pointer · captured-by · fix and
failure-capable evidence). No production file was created, edited or deleted. One probe run wrote
only inside `/tmp/r29a2-LessonDraft/probe/`.

Two facts shaped the draft and belong in the L1's integration decision:

1. An attempt-2 `### Mistakes` table **already exists** in the live tree —
   `corpus/lessons/round-29.md:157-168`, rows M92–M98, uncommitted, mtime `03:47:36` (the file is
   `M` against HEAD `8c14a5d`; `git diff --stat HEAD` = `57 insertions`). My rows are additive and
   none repeats M92–M98.
2. The object under test moved while I worked. `plans/sources_adopt.py` measured sha256
   `505478fd…` (401 ln, 03:46) → `ab594472…` (416→424 ln, 03:47:19) → `194f0511…` (432 ln,
   03:49:54), all `M` against HEAD. Every row therefore names the revision its receipt was taken
   on, and the two probes I own were re-run on the newest revision.

## Measured receipts (commands + observed output)

| # | command | observed |
|---|---|---|
| 1 | `sha256sum plans/sources_adopt.py plans/adoption_check.py` (03:47:19 / 03:49:54) | gate `ab594472…` then `194f0511…`; counter `704b6544…` then `ee34914c…`; both `M` in `git status` |
| 2 | `git show 8c14a5d:plans/adoption_check.py \| sed -n '104,107p'` | print spans 104–107 and emits `verified_at={verified_at_ok} census={census_state}` — the field C1's frozen line omits |
| 3 | `grep -n 'entries=1\|usedby_ok\|census=ok\|prints exactly' plans/round-29-attempt2-claims.md` | `:22`, `:24`, `:27` — frozen line has 7 fields, no `verified_at` |
| 4 | `sed -n '1,4p' .ufo/waves/round-29/attempt2/control.nothing.txt` | `:3` `… usedby_ok=0 verified_at=0 census=skipped`, i.e. the freeze commit's own control receipt already carried the field |
| 5 | `cat .ufo/waves/round-29/attempt2/adoption-measured.txt` | `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 verified_at=1 census=ok` (96 B, mtime 03:46:10) |
| 6 | `wc -l .ufo/waves/round-29/attempt2/package-gate.txt`; `tail -4` | 174 lines; `:1` `registry=76 staged=173 collisions=0 malformed=2 duplicates=0 defects=171`; `:174` `exit=4`; no `prose=` field, no `wrote` line |
| 7 | `ls -la --time-style=full-iso` on the receipt vs the tool | receipt 03:39:05; tool rewrites 03:44:59, 03:47:17, 03:49:5x → receipt predates every rewrite |
| 8 | `python3 /tmp/r29a2-LessonDraft/sources_adopt.live194f0511.py --registry reg.md --package pkg.md --admit-ids S900 --access-date 2026-10-25 --out block3.md` | `registry=0 staged=1 … defects=0 prose=0` / `wrote block3.md rows=1` / `exit=0`; block's last cell empty (`\|  \|`); identical result on `ab594472…` |
| 9 | re-run same tool on its own `block.md` | `defects=0`, `exit=0` — the gate accepts its own empty-`used-by` output |
| 10 | cell split of the package rows (`/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`) | S077–S090 each 11 cells; `recheck` = `2026-10-23 — re-verify at the next upstream release (Gate S0xx)` (prose) ×5; S078 `used-by` names `corpus/knowledge/judge-calibration-thresholds.md` |
| 11 | `ls corpus/knowledge/ \| grep -i judge` | `llm-judge-calibration.md` only — the S078 target entry does not exist; the landed row `corpus/SOURCES.md:101` names only the checklist (projection worked) |
| 12 | `sed -n '25,50p' plans/adoption_check.py` | `:33` `ROW_RE` matches 0–3 spaces; `:44` `cells = raw.rstrip()[1:-1].split("|")`; `:45-46` non-11-cell rows dropped silently |
| 13 | `sed -n '38,42p' plans/round28_census.py` | `:40` `re.match(r"^\|\s*S[0-9]{3,}\s*\|", …)` — column 0 only |
| 14 | `sed -n '305,316p;364,378p' plans/sources_adopt.py` (`194f0511…`) | case 5 asserts `columns=12` (`:309-316`); case 10 asserts an unscoped prose row is refused (`:369-378`) — both added after the mutation run |
| 15 | `python3 -c` on `PROSE_ROW`/`GOOD_ROW` of the frozen snapshot | `PROSE_ROW != GOOD_ROW` → `True`, so the fixture conflation named in my brief is **not** present in current bytes |

Peer receipts cited as such (not re-derived by me): `build/R29a2FixtureMutations.md:21-52` +
`/tmp/r29a2-FixtureMutations/results.json` (M1–M5 mutation table, survivors M2/M3, revision
`505478fd…`); `build/R29a2CritClaimC2.md:164-200` (status-cell mutant surviving 10/10) and
`:205-233` (empty-`used-by` path plus the fleet-census `ok`/W03 comparison);
`build/R29a2RevCensus.md:130-207` (F1–F4: E09 prose recheck ×5, E11 dangling used-by, counter's
indented-row drop, anchor provenance) and `:226` (F5, the same target/counter mismatch I derived
independently at receipts 2–5).

## Gates / checks I ran

No lane gate was executed by this seat (the report is a draft; running `grader.py`,
`plans/round28_census.py` or `sources-census.sh` would decorate it, not test it). The only
executions were the two gate probes at receipts 8–9, against fixtures under
`/tmp/r29a2-LessonDraft/probe/`, plus the constant comparison at receipt 15. Nothing was installed,
upgraded or removed; no pacman transaction attempted; no fetch or push.

## Touched surfaces

- Written (allowed): `/tmp/r29a2-LessonDraft/mistakes.md`, `sources_adopt.snapshot.py`,
  `sources_adopt.live194f0511.py`, `adoption_check.snapshot.py`, `probe/{reg.md,pkg.md,block.md,block2.md,block3.md}`.
- Written (report): this file.
- Read only: `plans/round-29-attempt2-claims.md`, `plans/sources_adopt.py`, `plans/adoption_check.py`,
  `plans/round28_census.py`, `corpus/lessons/round-29.md`, `corpus/SOURCES.md`,
  `.ufo/waves/round-29/attempt2/*`, `.ufo/waves/round-29/attempt2/build/*`,
  `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`, `/tmp/r29a2-*` peers' scratch,
  git history (`git show 8c14a5d:…`, `git status`, `git log`).
- Untouched: everything else; no commit.

## Findings

1. **C1's frozen target cannot be printed exactly.** The claim freezes a 7-field line
   (`plans/round-29-attempt2-claims.md:27`); the counter committed in the same commit prints 8
   (`adoption_check.py:104-107`), and both the control receipt (`control.nothing.txt:3`) and the
   live measurement (`adoption-measured.txt:1`) carry `verified_at`. As written, C1's own predicate
   is unsatisfiable — the honest reading is "the measured line minus nothing", which the round
   report must state explicitly. Drafted as **M99**.
2. **The gate's real-package evidence is red and stale.** `package-gate.txt` is `exit=4` with 171
   defects, produced at 03:39 by a format that no longer exists, before the scoped rewrite that
   makes five-row adoption passable; no green gate receipt exists anywhere in the wave dir (only
   counter runs are green). A later reader will take the committed receipt as the gate's verdict.
   Drafted as **M100**.
3. **The live gate emits a `mined` row with an empty `used-by` and certifies it clean.**
   `--admit-ids` without `--entries` → `exit=0`, `wrote … rows=1`, last cell empty; re-running the
   gate on that output is `defects=0`. W03 cannot see it (it keys on `—`, peer receipt), so nothing
   downstream corrects it, and it directly contradicts C1's `rows_mined=5`/`usedby_ok=1`. Drafted as
   **M101** — the highest-value row in this set because it is reproducible on the current bytes.
4. **Four row parsers, four anchors, one silently dropped indented row.** The claim's justification
   ("the census parser's own 0–3 anchor") has no single referent: `adoption_check.py` matches 0–3
   and splits at column 0 (a matched indented row becomes 12 cells and vanishes), `round28_census.py`
   is column 0 only, `sources_adopt.py` strips first, the census shell uses `NF==13`. Drafted as
   **M102**.
5. **Suite coverage arrived by luck, not by rule.** At `505478fd…` a widened column check and an
   any-nonempty-`recheck` both survived 10/10; both are now caught only because a mutation seat ran
   and fixtures were added afterwards. C2's kill rule is per-case, never per-capability. Drafted as
   **M103**.
6. **My brief's first candidate is ungrounded and must not be written.** No receipt exists for "the
   gate's first selftest failed on indented rows because the splitter sliced before stripping": the
   committed and live gate strip before slicing (`sources_adopt.py:71-74`), and searches of the tree,
   `.ufo/waves/round-29/**`, `/tmp/r29a2-*`, `/tmp` mtimes 03:30–03:41 and shell histories found no
   red first run. The *described* defect is real but in `adoption_check.py:44` (the counter), which
   is M102. The brief's second candidate is already recorded as **M92** and is no longer true of the
   code (`PROSE_ROW != GOOD_ROW` → `True`), so I added nothing for it.
7. **Live-tree churn is itself a hazard for this lesson.** `plans/sources_adopt.py` changed three
   times in ~4 minutes and `corpus/lessons/round-29.md` grew its attempt-2 table at 03:47:36. Any
   mistake row that names a line number without a sha256 is stale by the time the round closes; the
   draft names a revision per row, and the L1 should re-pin all of them against the final tree before
   landing.

## Out of scope / not done

- Did not integrate the rows into `corpus/lessons/round-29.md` (production edit; L1 owns it).
- Did not judge C1/C2, did not run `grader.py`, the fleet census, or the wave's regression set.
- Did not verify the five sources' quotes (separate reviewer seats own that).
- Did not audit `adoption_check.py`'s remaining counters (its census lane-name bug is already M93).
- Round-35 scratch-sweep messages from `L1Mado35.*` were read and ignored: no round-29 citation of
  round-35 scratch exists in this report.

## Artifact paths

- Draft rows: `/tmp/r29a2-LessonDraft/mistakes.md`
- Frozen revisions compared: `/tmp/r29a2-LessonDraft/sources_adopt.snapshot.py` (`ab594472…`),
  `/tmp/r29a2-LessonDraft/sources_adopt.live194f0511.py` (`194f0511…`),
  `/tmp/r29a2-LessonDraft/adoption_check.snapshot.py` (`704b6544…`)
- Probe fixtures and outputs: `/tmp/r29a2-LessonDraft/probe/{reg.md,pkg.md,block.md,block2.md,block3.md}`
- This report: `.ufo/waves/round-29/attempt2/build/R29a2LessonDraft.md`
