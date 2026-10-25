# Lessons — round 14 (the landing debt: a round ends at commit + index + log)

Source: measured at repo root `kengaku-shokunin`, HEAD `e171cdf`, 2026-09-29.
Evidence: `git status --porcelain`, `LOG.md`, `SCORECARD.md`, `corpus/README.md`
(as read this round); the debts themselves live in `corpus/evidence/round12-ladder/`,
`corpus/evidence/round12-fleet/`, `corpus/evidence/round13-ack-state/`.

The narrative: rounds 12 and 13 both finished their *work* — a full powered
preregistered run with its fleet and prior-art pricing (r12), two hermetic
ack-state audit scripts (r13) — and neither round *landed*. The evidence sat in
the working tree across a full round while `LOG.md`, `SCORECARD.md` and
`corpus/README.md` continued to describe the corpus as it stood at round 11.

Measured state at the start of round 14:

| check | command | observed |
|---|---|---|
| uncommitted rounds | `git status --porcelain` | `M SKILL.md`, `M grader.py`, `?? corpus/evidence/round12-fleet/`, `?? corpus/evidence/round12-ladder/`, `?? corpus/evidence/round13-ack-state/` |
| newest LOG entry | `grep -n "^- 2026" LOG.md \| tail -1` | `LOG.md:18` — round 11 (16 dated entries total) |
| SCORECARD move | `grep -c "^## Round 12" SCORECARD.md` | `0` — the newest post-move table is `SCORECARD.md:136` "Round 11 — post-move (novelty axis-move landed)" |
| corpus index | `grep -c "round12\|round13" corpus/README.md` | `0` — no index row, no coverage-map line, no open-gap line |
| corpus entries | `ls corpus/knowledge \| wc -l`, `ls corpus/lessons \| wc -l` | `23` / `14` (knowledge includes this round's new entry; the r12 knowledge entry and the r12/r13 lessons entries did not exist) |
| gate layer | `wc -l < grader.py` vs `git show HEAD:grader.py \| wc -l` | `5734` vs `1711` → the 4 023-line r12 replay layer (`CHECKS n=732`) is in the working tree only; a fresh clone still gets the round-11 gate |
| last commits | `git log --oneline \| head -2` | `e171cdf` (a corpus lesson append) on top of `f09ff1f` ("round-11") — the newest *round* commit is round 11; `git ls-files corpus/evidence` lists round8/round9/round10-fleet/round11-power/round11-fleet, and **not** round12-ladder/round12-fleet/round13-ack-state |

Consequences, all of which were live until round 14 landed:

1. **Novelty is not durable until it is indexed.** The r12 claim set
   (`LADDER ESTABLISHED`, `DISSOCIATION ESTABLISHED`, `TRANSPORT DIRECTIONAL`,
   `FORECAST SKILLED`) existed only as bytes in an untracked directory. The
   `SCORECARD.md` novelty axis still read **6** with a round-11 anchor, so the
   round-12 axis-move could not be scored, cited, or audited by any later round.
2. **A cold agent cannot find the work.** `corpus/README.md` is the entry point
   for a reader with no oral context (the standing `SHONEN.md` box-3 gap): with
   no index row and no `knowledge/`/`lessons/` entries, rounds 12 and 13 are
   invisible to exactly the consumer the corpus exists for. Evidence on disk is
   not evidence in the corpus.
3. **Unlanded artifacts rot, and then the drafts become wrong.** While the r12
   tree sat unlanded, `analysis_r12.md` was regenerated after
   `r12-report-final.md` / `r12-log-final.md` pinned its hash: the drafts pin md5
   `ddfe60d2…` / sha256 `ef1e69db…`, the working tree satisfies md5 `029c3bcd…`
   / sha256 `1ceebd75…` (F-R12-2 in `corpus/knowledge/bench-arena-round12-ladder.md`).
   The same generated file carries a generator path (`/home/vgpnk/projects/…`)
   that does not resolve on this host (F-R12-1). Both defects are *landing-time*
   defects: the fix is to pin hashes from the bytes actually being committed and
   to keep generated output path-insensitive. A draft's hash is evidence of what
   the drafter saw, never of what will be committed.
4. **The debt compounds silently.** Each unlanded round raises the cost of the
   next: the r12 tree had to carry its own `INTEGRATOR-NOTES.md`, doc-deltas,
   log draft and report draft *as artifacts* because there was no LOG entry and
   no SCORECARD row to write into — a whole second document set that exists only
   to be consumed at landing. Round 13 then added a second unlanded directory on
   top of it.

The rule (and the round-14 closure checklist — a round is not over until every
line below is true):

1. `git add` the round's evidence dir and **commit** it (no `??` for the round's
   own directory when the round closes).
2. One physical line appended to `LOG.md`, evidence-first, every count
   re-measured or named as a command.
3. The `SCORECARD.md` post-move table (and the axis-move score, which is the
   round's own judgement).
4. `corpus/README.md`: evidence-table row, main-table row, coverage-map line,
   open-gaps lines — **both directions** equal at close (rows = files).
5. The `corpus/knowledge/` entry (first line = source pointer) and the
   `corpus/lessons/` entry for the round.
6. Hashes re-pinned **at landing** from the committed bytes; any hash copied
   from a draft is a claim to verify, not a value to paste.
7. `python3 grader.py` exits 0 on the landed tree, with the round's own replay
   layer committed in the same round (r11 §Planned clause (d), honoured by r12
   and only *durable* once committed).

Standing consequence for this corpus: the "unanalyzed run ≠ result" lesson
(`lessons/round-8.md`) has a sibling — **an unlanded round ≠ a round**. Round 13
is the second instance, and its own audit is what surfaced it: a repo whose
newest index row is two rounds stale cannot be trusted to describe its own
evidence.