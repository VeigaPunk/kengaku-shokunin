## Round43 criterion — a conditional Gate refusal is resolved by a recorded flip check

- **Q35 — every Gate refusal whose reason states a flip condition is resolved, in the same lesson and
  on a line after the flip statement, by `Flip check (round N): <item> — fired|not fired — <evidence>`;
  a condition that fires at landing must not be representable as silence, because the lane's only
  record that a flip was examined at all is the sentence that says so.**
  The obligation is written 45 times across 18 lessons and was executed on none of them. Of the 55 files
  in `corpus/lessons/`, 20 carry a `## Gate` heading (`grep -l '^## Gate$' corpus/lessons/*.md` →
  `round-13-coverage.md`, `round-24.md` … `round-42.md`), 18 of those carry at least one refusal whose
  reason states a flip, and the checker below counts 45 such obligations with 45 unresolved
  (`FLIPS total=45 unresolved=45` summed over the 18; the per-lesson numbers are in
  `.ufo/waves/round-43/build/R43FlipCheck/sweep.txt`). No line in `corpus/` or `plans/` says
  `Flip check` (`grep -rn "Flip check" corpus plans` → no matches), so nothing in the lane has ever
  recorded that a flip fired or did not.
  The measured instance is round 42. Its Gate refuses `Dockerfile` conditionally —
  `corpus/lessons/round-42.md:44`, "if the entry keeps the `WORKDIR /app` sentence" (10 words) — and the
  landed entry kept the sentence and made it load-bearing
  (`corpus/lessons/round-42-verifier-spotcheck.md:92`), so "by the Gate's own flip the file should be a
  row"; no `S###` row was opened and no line records the flip at all
  (`corpus/lessons/round-42-verifier-spotcheck.md:37`, "D3 Gate flip condition fired and was not
  executed (Dockerfile)."). A second obligation on the same section, `README.md` (`:43`), is in the same
  state. The old instruments cannot see this class: `plans/gate_timing_check.py` checks that admits name
  returned second-seat reports, `plans/round_close.py` checks the round's order of operations, and
  `plans/state_check.py` re-derives frozen assertions — none reads a lesson's flip conditions, and the
  only `flip:` string anywhere in `plans/*.py` is a fixture literal a registry test writes
  (`plans/round33_c1_verify.py:215`, "REJECTED: duplicate id; flip: a future candidate uses a new id"),
  never a line read or checked.
  Check (executable, round-42 instance): `python3 plans/gate_flip_check.py --lesson
  corpus/lessons/round-42.md` prints one `FLIP line=<n> flip_line=<n> item=<item> … resolution=<detail>`
  line per conditional refusal, then `FLIPS total=<n> unresolved=<u>`; exit 1 iff `u>0`, exit 2 when the
  lesson is unreadable or carries no `## Gate` section. On the landed lesson it prints `FLIP line=43 … item=README.md
  … unresolved:no-line`, `FLIP line=44 … item=Dockerfile shapes=flip:,if-admit … unresolved:no-line`,
  `FLIPS total=2 unresolved=2`, exit 1. A scratch copy of the same file with the two resolution lines
  appended prints `FLIPS total=2 unresolved=0`, exit 0; the same copy carrying only the `Dockerfile`
  resolution prints `FLIPS total=2 unresolved=1`, exit 1. The tool is a draft at
  `.ufo/waves/round-43/build/R43FlipCheck/gate_flip_check.py`, sha256
  `d849250d…bf1d`, 504 lines, stdlib only, and must land as `plans/gate_flip_check.py` for this line to
  run as written.
  Shown able to fail: `--selftest` builds 19 fixtures in a temporary directory and runs the checker on
  each as a subprocess — `SELFTEST ok=19/19` (10 red, 8 green, 1 setup). The reds are the shapes the
  criterion has to separate: a refusal with no resolution line; a `flips when` refusal with none; a
  resolution placed *before* its flip statement; a resolution naming another candidate; evidence `none`
  and evidence of one word; `(round 4)` under a `round-42` file name; a malformed `<state>`; a
  `- **Rejected:**` bullet with no resolution; and a companion flip bullet with no resolution. The two
  halves of the round-42 demonstration differ by exactly the appended lines and by nothing else
  (`FLIPS total=2 unresolved=2` exit 1 against `total=2 unresolved=0` exit 0), and the partial copy
  differs by one of the two lines and moves `unresolved` 2→1, so the check is per-obligation, not
  all-or-nothing. On the corpus the same run is red on all 18 lessons that carry obligations, the
  landed round-42 lesson among them.
  Limits: the verdict is a recorded *sentence*, never the executed consequence — a `fired` line whose
  evidence names the wrong landing passes, and a `not fired` line whose condition had in fact fired
  passes just as well; the class is 45 obligations wide at creation, so as a gate it binds from round 43
  forward and this criterion does not re-adjudicate the older 43; the section is found by a level-2
  `## Gate` heading, so a lesson with no such section is exit 2 (`SETUP`) and not a pass — 35 of the 55
  lesson files are in that state and two more (round-13-coverage, round-31) have a Gate section and zero
  obligations, which reads green but demonstrates nothing; a flip phrased imperatively rather than
  conditionally is not counted (`round-30.md:34`, "flip one entry at a time under CORPUS rule 4"), so
  round 30's obligation count is 3 of its 4 rejects; the item name is derived from the refusal's first
  id-shaped token, else its first code span, so a candidate named only in prose needs the resolution to
  repeat that prose; a companion bullet attaches to every refused candidate it names and to none it does
  not; `fired`/`not fired` is a two-word vocabulary, so a round that resolves a flip with a third state
  (`moot`, `superseded`) gets an unresolved line until it says one of the two and explains the other in
  its evidence; and the checker reads the working tree only, so a resolution line committed and later
  deleted is invisible and a resolution line that lives in another file (a seat report, `PROVINCE.md`)
  does not count — the criterion deliberately keeps the record beside the condition.
  Lesson: `corpus/lessons/round-43.md` mined mistake (round-42 D3, routed as closure R2 in
  `corpus/lessons/round-42-verifier-spotcheck.md:125-128`: "a conditional reject's flip is re-checked at
  landing"); the class's first instance is `corpus/lessons/round-42.md:44` against
  `corpus/lessons/round-42-verifier-spotcheck.md:37-42` and `:92`. Supersedes: none; it is the first
  executable leg of the flip condition the Gate has been writing since round 25.
