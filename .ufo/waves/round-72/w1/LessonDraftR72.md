# LessonDraftR72 — round 72 w1: the lesson draft

Seat: `LessonDraftR72` (leaf scribe; no subagent dispatch as the item requires). Lane
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`, tip `b6336136e0e891522b113a94d8e0bd65e0eae8de`
(freeze commit, 2026-11-03T23:02:34-03:00). Read `plans/round-72-claims.md` in full before any
command. No port bound, no battery or gate run by this seat, no tool installed or upgraded (pacman
untouched), no git/jj mutation, no `agent://all`.

## Deliverable

`corpus/lessons/round-72.md` — 41,882 bytes, 345 lines, sha256
`dd264d9e666a7c71d6f24b99825e868c4b7c5c9d9115586ebdd79435673f80e8`, in the round-71 order:
`## Gate`, `## Mistakes` (11 rows), `## Census`, `## Verdicts`, `## Limits (named, not scored)`.

## What I ran (the only instrument)

| # | command | rc | outcome |
|---|---|---|---|
| 1 | `sh /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` | 0 | 26-line stdout (25 `W04` + `ok …/corpus/SOURCES.md`), sha256 `5bbde4ee…fcde`, `cmp`-identical to `.ufo/waves/round-72/census-before.txt`; row counter `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → **240** at the freeze tip |
| 2 | the same row counter over committed base bytes (`git show c6322972:corpus/SOURCES.md`) | 0 | **238** — the pre-freeze count; the two new rows land in the freeze (`git diff --numstat c6322972 b6336136 -- corpus/SOURCES.md` → `2 0`) |
| 3 | `sha256sum` / `wc -c` on `corpus/evidence/round72/sources/{bwrap.1.html,hf-model-card.md}` | 0 | `708f56ee…8de7` / 27,981 B and `75f17282…8851` / 10,512 B — equal to rows S247/S248 and to `KnowledgeIndexR72` §1 |
| 4 | read-only reads: the 15 wave reports, every round-72 receipt, `MERGE-REPORT.md`, the staged entry | 0 | sources for every non-census number in the lesson |

Every other number in the lesson is quoted from a committed receipt or a wave report, with the file
named. Nothing was re-run to decorate the report.

## Gate decisions

- **S247 admitted** (tier A, docs): URL, access date 2026-11-03, 27,981 bytes, sha256
  `708f56ee…8de7`, capture line 185, 15-word quote (`Unset all environment variables, except for
  PWD and any that are subsequently set by --setenv`). Fetch status is the row's record; this seat
  re-derived the capture only.
- **S248 admitted** (tier A, docs): 10,512 bytes, sha256 `75f17282…8851`, capture line 145, 3-token
  quote. The freeze row's "172 lines" was corrected to "197 lines" by the landing edit (`1 1` diff);
  the lesson records the correction and the audit that caught it (`KnowledgeIndexR72` §4.5).
- **S245/S246** re-derived from committed captures; no live re-fetch, stated as such.
- **`merge/kengaku` entry `card-provenance-and-preregistration.md` refused** (4,576 B): (i) triad
  offset (blank line 1, `source:` at `:2-7`); (ii) all six cited ids resolve in this lane to TB2
  `password-recovery` files (`corpus/SOURCES.md:174-179`), and the one URL the lane holds under
  another id (`2608.29463` = S081) is held for a different claim; (iii) `ground: N14 and N20` names
  two ground ids the lane holds nowhere and the headline kappa figures are not re-derivable from lane
  bytes. Flip: stage six fresh rows with the real URLs and the `PRE-REGISTRATION.md` pin at
  `4dba1ed9…`, then admit. **Assimilation: none.**
- **Census**: 238 → 240 data rows, 25 `W04`, stdout byte-identical (the two rows add no warning).
- **Admission status: HOLD.** `admission: hold` in the entry; `plans/gate_timing_check.py:241-243`
  accepts only a `falsify` or `wave 2` directory and `.ufo/waves/round-72/` holds `w1` only.

## Mistakes table (11 rows)

Required rows: (a) the pre-`--control` battery at `/fast/scratch/hyaku/kengaku-r72/l1/c1-control.txt`
(`mismatches=0`, `PREDICATE pass`, byte-identical to the receipt of record) against the corrected
control (nine `FFFF`, `mismatches=9`, `fail`); (b) the pre-freeze receipt
`/fast/scratch/hyaku/kengaku-r72/l1/receipt.txt` (`PROBE_BLOB sha256=unknown`, green vectors,
`PREDICATE fail`) and the `check_receipt` `PROBE_BLOB` clause. Nine further rows, each cited to the
seat that observed it: an unread kill-rule clause (`ReceiptReviewR72` F3), a superset test named
`allowlist_seen=9/9` (five independent observers), a round-72 entry written before its data
(`KnowledgeIndexR72`, `SurfaceScoutR72`, `C2ControlsR72`), a presence check read as attribution
(`C2RedBeforeR72`, `ClaimFalsifyR72`), registry rows that misstate their instruments' exit contract
(`RegistryAuditR72`: 9/32 cells), a registry gate bounded to a frozen list (`SiblingOverlapR72`),
a `null` that conflates a no-op with a fixture-invisible weakening (`GateMutateR72`), a non-load-bearing
checker conjunct (`CounterMutateR72`: M6/M8 survived), and the freeze doc's "five groups" count
(`SurfaceScoutR72` §4a).

## Calibration corrections made to seat claims (reported, never silent)

1. `ReceiptReviewR72` §F4 calls `corpus/evidence/round72/hf/check.txt` "a redirect slip". The wave
   spec's `HfBatteryR72` item step 3 assigns that exact path for the check's stdout, so the lesson
   names it the check receipt of record and says so in Limits.
2. My first draft's Gate bullet said the census *before* count was 240. The integrator's concurrent
   `## Census` rewrite said 238 → 240, and base bytes agree (238 at `c6322972`, rows landing with
   the freeze). Both places now say 238 → 240 with the base-bytes derivation.
3. `CounterMutateR72.md` and its receipt landed after the first draft; the lesson cites both and
   records its five `UNRUN` clauses rather than reading them as passes.

## Concurrent write (declared)

At 23:21:20 the integrator amended this lesson's `## Census` while the seat was drafting (238 → 240,
plus a citation to `corpus/evidence/round72/census-after.txt`). I kept the numbers and removed the
citation, because that file does not exist (`ls` rc 2) and the freeze-tip run is this seat's own
measurement. Everything else in the file is this seat's text, with the integrator's landing edits to
`LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md` and the entry recorded
in §Verdicts as landing edits, not seat writes.

## Limits

- No battery, gate, selftest, control or mutant was run by this seat; every such counter is quoted
  from the seat that ran it. The census is the only command executed.
- The census "after" is at the freeze tip; a re-run at the landing tip is owed by the L1.
- The `merge/kengaku` selection is this seat's (the package's closest match to the round's subject);
  no item pre-named an entry.
- The lesson's `## Census` validator-self-test line remains `not measured this round`; no seat ran it.

## Scratch / writes / tooling

- Scratch `/fast/scratch/hyaku/kengaku-r72/LessonDraftR72` (census stdout, one draft) was removed;
  `ls` of the path returns rc 2. Nothing of this seat's remains in `/tmp` (one `_src_freeze` temp was
  created and deleted in the same command; `find` returns empty).
- Lane writes: `corpus/lessons/round-72.md` and this report. No tracked product byte, no
  `.ufo/state/`, no `.scratch/`, no sibling lane, no git/jj mutation.
- No tool installed or upgraded; `python3`, `git`, `sha256sum`, `grep` sufficed.
