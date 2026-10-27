# R44FlipVerdict — the flip checker sees a `not fired` verdict the entry contradicts

Seat: executor (leaf). Task: closure R1 second half — a `Flip check (round N): <item> — not fired — …`
line that names a file is RED when the entry the lesson's Gate concerns carries a `<file>:<line>`
citation of that file. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` was read only: the extended
tool lives at `.ufo/waves/round-44/wave/R44FlipVerdict/gate_flip_check.py`
(sha256 `e29e54a031bb86cfb6b2dc056c7744b15a5a9c256a228a376df7d1ab5bc8477f`, 747 lines; lane original
`plans/gate_flip_check.py` `d849250da6b3815dba421d5a5763c6cff20662a80f7fcf95c1e2912dfd44bf1d`, 504 lines;
`git diff --no-index --stat` → `263 insertions(+), 20 deletions(-)`). Scratch
`/fast/scratch/hyaku/kengaku-r44/R44FlipVerdict`. Every run below is inside
`.ufo/waves/round-44/claims/envelope.sh "$S/env" …`; every envelope ends
`local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged` (never `INVALID`).
Receipts: `.ufo/waves/round-44/wave/R44FlipVerdict/receipts/`.

## 1. What the extension is (four changes, old checks untouched)

The 19 pre-existing selftest cases and the four pre-existing checks (section, refusals, flips,
resolution shape) are unchanged in behaviour — the sweep below measures that on 62 lessons.

1. **Citation leg (new rule 5).** Entries = the `.md` names the `## Gate` section writes, resolved as
   `<nearest ancestor holding corpus/knowledge>/corpus/knowledge/<basename>`; `--entry FILE|DIR`
   (repeatable) adds entries explicitly. For every obligation whose accepted resolution says
   `not fired`, the files that resolution's item+evidence name are extracted (dotted extension, plus the
   bare set `Dockerfile Makefile SHA256SUMS LICEN[CS]E CHANGELOG`), and each entry is searched for
   `<file>` + optional backticks/space + `:` + a line number (or `a-b`). A hit prints
   `FLIP-CITE line=<n> item=<item> state=not fired file=<f> citation=<entry>:<line> quote="…" verdict=RED`
   and the tool exits 1. Output lines added: one `FLIP-CITE` per obligation, plus the summary
   `FLIP-CITE entries=<…> missing=<…> not_fired=<n> red=<r>`.
2. **Last matching resolution wins (rule 4).** Needed for R1's own prescription:
   `corpus/lessons/round-43-verifier-spotcheck.md:156` says "Append a corrected `Flip check (round 44):
   task.toml — fired — …` (append only)". Under the first-match-wins rule the false line stays the
   accepted record and the append changes nothing, so the closure could not go green by its own
   instructions. Now the last line naming the item decides (a later malformed/thin line leaves the
   obligation unresolved). Both correction forms are demonstrated in §4.
3. **Selftest fixture trees.** Each case now gets `<work>/<case>/corpus/lessons/round-42.md` plus an
   optional `{relative path: text}` map and argv (`{case}` = case dir), so the leg is exercised on real
   `corpus/knowledge` lookups; the `--entry` flag has its own case.
4. **CLI**: `--entry` added; `--lesson`, `--selftest`, exit codes 0/1/2 unchanged in meaning
   (1 now also when `red>0`).

## 2. RED on the committed round-43 lesson

```
$ /…/envelope.sh "$S/env" python3 …/R44FlipVerdict/gate_flip_check.py --lesson corpus/lessons/round-43.md
ENVELOPE start 20:45:27 cwd=/home/vgpnk/Projects/shokunin
FLIP line=41 flip_line=41 item=task.toml shapes=flip: resolution=line:46:not fired:round=43
FLIP-CITE line=46 item=task.toml state=not fired file=task.toml citation=tb2-circuit-fibsqrt-grader.md:332 quote="- **The task image is never pulled; the host's tools stand in.** `task.toml:29` names" verdict=RED
FLIP-CITE line=46 item=task.toml state=not fired file=task.toml citation=tb2-feal-differential-cryptanalysis-grader.md:41 quote="is the verifier timeout of 1800 s (`task.toml:22`). A reference attack followed by a 45 s sleep" verdict=RED
FLIP-CITE line=46 item=task.toml state=not fired file=setup.py citation=tb2-feal-differential-cryptanalysis-grader.md:96 quote="| Extension build | at grading time the test shells out: `(cd /tests && python setup.py build_ext --inplace)`, i.e. it c" verdict=RED
FLIP-CITE line=46 item=task.toml state=not fired file=solve.sh citation=tb2-feal-differential-cryptanalysis-grader.md:230 quote="| `oracle-solve-sh` | `solve.sh:90` | “if (c1l ^ c2l) == 0x02000000:” |" verdict=RED
FLIP line=42 flip_line=42 item=merge/kengaku/ shapes=flip: resolution=line:47:not fired:round=43
FLIP-CITE line=47 item=merge/kengaku/ state=not fired files=- verdict=clear
FLIP-DETAIL lesson=…/corpus/lessons/round-43.md lesson_round=43 refused_rows=2 malformed_resolutions=0
FLIPS total=2 unresolved=0
FLIP-CITE entries=tb2-circuit-fibsqrt-grader.md,tb2-feal-differential-cryptanalysis-grader.md missing=instruction.md,README.md,R43MergeRescreen.md,SOURCES.md not_fired=2 red=1
ENVELOPE end 20:45:28 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

`corpus/lessons/round-43.md:46` is the false line — "`Flip check (round 43): task.toml — not fired — no
entry sentence rests on task.toml, setup.py, solve.sh, feal.h or SHA256SUMS alone`" — and the feal entry
cites `task.toml:22` at `:41`, `:122`, `:240`, `:300`. `red=1`, `exit=1`; the `merge/kengaku/`
obligation (`:47`) stays clear because it names no file. The entry was found by the repo-root rule with
no `--entry`; the four `missing=` names are Gate-named `.md` files that are not knowledge entries
(captured task files, a seat report, `SOURCES.md`) and are reported, not judged.

Attribution note: the red is over-determined. `tb2-circuit-fibsqrt-grader.md:332` is the round-42 task's
`task.toml:29`, not the feal task's; the leg matches by basename across every entry the Gate names, so it
prints each hit with its entry — the feal entry alone carries three of the four hits, so the verdict does
not rest on the coarser one.

## 3. Faithful-copy control (same bytes, other tree)

`copied/` = committed `corpus/lessons/round-43.md` + the two entries the Gate names, copied under a
scratch `corpus/` tree: identical output and `exit=1` (`receipts/copied.txt`) — the verdict follows the
tree it is given, not the lane path.

## 4. GREEN on both corrected scratch copies

| copy | correction | result |
|---|---|---|
| `corrected-append` | R1's literal prescription: two lines appended, `Flip check (round 44): task.toml — fired — closure R1: entry cites task.toml:22 as the only time bound (…:122, :300)` and the same for `solve.sh` | `resolution=line:105:fired:round=44`, `not_fired=1 red=0`, `exit=0` |
| `corrected-inplace` | the false line rewritten to `Flip check (round 43): task.toml — fired — corrected at closure R1: …` | `resolution=line:46:fired:round=43`, `not_fired=1 red=0`, `exit=0` |

`FLIPS total=2 unresolved=0` in both; the `merge/kengaku/` line is still `not fired` and `clear`. The
only difference between the red and green runs is the correction text (`receipts/r43-committed-red.txt`,
`receipts/corrected-append.txt`, `receipts/corrected-inplace.txt`, all with their envelope lines).

## 5. Selftest — 27 cases, 13 red / 13 green / 1 setup

```
$ …/gate_flip_check.py --selftest
SELFTEST case=cite-not-fired-red expect=red got=red total=1 unresolved=0 not_fired=1 cite_red=1 rc=1 ok
SELFTEST case=cite-not-fired-clear expect=green got=green total=1 unresolved=0 not_fired=1 cite_red=0 rc=0 ok
SELFTEST case=cite-fired-not-tested expect=green got=green total=1 unresolved=0 not_fired=0 cite_red=0 rc=0 ok
SELFTEST case=cite-entry-missing expect=green got=green total=1 unresolved=0 not_fired=1 cite_red=0 rc=0 ok
SELFTEST case=cite-not-fired-names-no-file expect=green got=green total=1 unresolved=0 not_fired=1 cite_red=0 rc=0 ok
SELFTEST case=cite-later-fired-supersedes expect=green got=green total=1 unresolved=0 not_fired=0 cite_red=0 rc=0 ok
SELFTEST case=cite-later-not-fired-reopens expect=red got=red total=1 unresolved=0 not_fired=1 cite_red=1 rc=1 ok
SELFTEST case=cite-entry-flag expect=red got=red total=1 unresolved=0 not_fired=1 cite_red=1 rc=1 ok
SELFTEST ok=27/27
ENVELOPE end 20:45:13 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

The 19 original cases still pass (`SELFTEST ok=19/19` inside the same run). The eight new cases separate
exactly the shapes the leg must: a citation under `not fired` (red); the same line with an entry that
cites nothing (green); a `fired` line never tested (green); an entry the Gate names but that is absent
(inert, green); a `not fired` line naming no file (green); a later `fired` superseding (green); a later
`not fired` reopening it (red); `--entry` supplying the entry the Gate does not name (red).

## 6. No collateral red — 62 lessons, old tool vs extended tool

```
$ python3 sweep_all.py            (one envelope; receipts/sweep-all.txt)
round-43.md     old_exit=0 new_exit=1 DIFF not_fired=2 red=1
SWEEP lessons=62 differ=1 red=18
ENVELOPE end 20:45:48 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

`ls corpus/lessons/*.md | wc -l` → 62; `grep -l '^## Gate$' corpus/lessons/*.md | wc -l` → 21. Exit
codes agree on 61 of 62 files; the only change is the intended one (`round-43.md` 0→1). Old tool red = 17
lessons, new = 18 (`grep -c 'old_exit=1'` / `'new_exit=1'` over the receipt). Lessons the old tool already
reported red keep their exact verdicts; the last-line-wins change moved nothing else.

## 7. QUALITY criterion draft — next free number is Q36

Append under a new `## Round44 criterion` heading in `corpus/QUALITY.md` (Q35 is the last, at `:872`):

> - **Q36 — a `not fired` flip verdict that names a file is red when an entry the lesson's Gate concerns
>   cites that file at a line, because a recorded verdict that contradicts the corpus is worse than no
>   verdict: the first says the question was asked, and answers it wrongly.**
>   Q35 requires the sentence to exist; it explicitly cannot see whether the sentence is true
>   ("a `not fired` line whose condition had in fact fired passes just as well", Q35 Limits). Round 43 is
>   the measured instance: `corpus/lessons/round-43.md:46` records "task.toml — not fired — no entry
>   sentence rests on task.toml, setup.py, solve.sh, feal.h or SHA256SUMS alone" while the entry the same
>   Gate names cites `task.toml:22` at four lines and rests finding 11 on it
>   (`corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md:41`, "is the verifier timeout of 1800
>   s (`task.toml:22`). A reference attack followed by a 45 s sleep" (17 words); `:122`, `:240`, `:300`).
>   The round-43 closure found it by reading, not by instrument
>   (`corpus/lessons/round-43-verifier-spotcheck.md:124`, "**disagree** (on the flip verdict)"; routed as
>   `:156` R1). Old tool on the committed lesson: `FLIPS total=2 unresolved=0`, exit 0.
>   Check (executable): `python3 plans/gate_flip_check.py --lesson corpus/lessons/round-43.md` prints one
>   `FLIP-CITE line=<n> item=<item> state=not fired file=<f> citation=<entry>:<line> quote="…"
>   verdict=RED|…` line per `not fired` resolution and a `FLIP-CITE entries=… missing=… not_fired=<n>
>   red=<r>` summary; exit 1 when `red>0` as well as when `unresolved>0`. On the committed lesson it
>   prints four `verdict=RED` hits for `task.toml`/`setup.py`/`solve.sh` at
>   `tb2-feal-differential-cryptanalysis-grader.md:41/:96/:230` (and `task.toml:29` in the round-42 entry
>   the same Gate names), `not_fired=2 red=1`, exit 1; the `merge/kengaku/` line is `clear`. A scratch
>   copy with R1's two appended `Flip check (round 44): … — fired — …` lines prints `not_fired=1 red=0`,
>   exit 0; a scratch copy that instead rewrites line 46 to `fired` also prints `red=0`, exit 0; a scratch
>   copy of the committed bytes under another `corpus/` tree reproduces the same four hits. The tool
>   (drafted `.ufo/waves/round-44/wave/R44FlipVerdict/gate_flip_check.py`, sha256 `e29e54a0…bc8477f`,
>   747 lines, stdlib only) is the Q35 tool plus rule 5; `--selftest` builds 27 fixtures —
>   `SELFTEST ok=27/27` (13 red, 13 green, 1 setup), the eight new ones listed in
>   `receipts/selftest.txt`. On the corpus the extended run is red on 18 lessons against the old tool's
>   17, and the single differing exit code is `round-43.md` (`SWEEP lessons=62 differ=1 red=18`).
>   Limits: the leg sees `<file>:<line>` only where name and line stand together (an entry that puts the
>   file in one cell and `:22` in the next is not seen); it matches by basename across every entry the
>   Gate section names, so an unrelated entry's citation of the same file name also fires (attributed per
>   line, so the reviewer can see which entry); a cited directory or an extension-less name outside the
>   literal set is not seen; a Gate naming no entry that resolves under `corpus/knowledge/` leaves the leg
>   inert (`entries=-` or `missing=…`); and a later `fired` line supersedes an earlier `not fired` one, so
>   an appended correction clears the red without the false line being deleted — the criterion forces a
>   recorded correction, not its truth, which stays Q35's named limit.
>   Lesson: `corpus/lessons/round-43-verifier-spotcheck.md:156` (R1) and `:124` (the disagreement);
>   the class's first instance is the same round's `task.toml` verdict. Supersedes: none; it is the
>   second executable leg of the flip condition, and Q35's Check line keeps its counts.

## 8. What the L1 has to land (I did not touch the lane)

1. `cp .ufo/waves/round-44/wave/R44FlipVerdict/gate_flip_check.py plans/gate_flip_check.py`
   (sha256 `e29e54a031bb86cfb6b2dc056c7744b15a5a9c256a228a376df7d1ab5bc8477f`).
2. Append Q36 above to `corpus/QUALITY.md`.
3. Apply closure R1's lesson correction — append the two `Flip check (round 44): … — fired — …` lines to
   `corpus/lessons/round-43.md` (append only; §4 shows the appended form clears the red). Land 1 and 3 in
   the same commit: the tool alone turns the registered `gate-flip-check` row red on the round-43 lesson,
   which is the intended red-before state but must not survive the round's own close.
4. `python3 plans/gate_flip_check.py --selftest` → `SELFTEST ok=27/27`; then
   `python3 plans/gate_flip_check.py --lesson corpus/lessons/round-43.md` → `red=0`, exit 0.

## 9. Risks and blockers

- **R1's append-only instruction did not work with the tool as it stood** (first-match-wins); the fix is in
  this draft (rule 4). If the L1 prefers not to change resolution order, the alternative is to rewrite
  lesson line 46 rather than append — shown green in §4 — but that edits a landed lesson line, which the
  lane's append-only rule avoids.
- **Coarse attribution** (`task.toml:29` from the round-42 entry also fires) is named in Q36 Limits and
  visible in the output; it never changes a verdict the feal entry does not already carry here.
- **Missing entries are inert**, not red: a lesson whose Gate names a `.md` that does not resolve under
  `corpus/knowledge/` gains nothing from this leg (round-43 has four such names). A stricter rule would
  need the entry path written in the Gate row, which no lesson does.
- No blocker: every run is inside the envelope with the PATH-dir digest unchanged; nothing was written to
  the lane, `$HOME`, or any PATH directory; the scratch dir `/fast/scratch/hyaku/kengaku-r44/R44FlipVerdict`
  was removed with `plans/scratch_guard.py safe-rm` at the end of this seat (receipts were copied into
  `receipts/` first).

VERDICT: flip-verdict-check-red-on-r43-yes-selftest-27/27
