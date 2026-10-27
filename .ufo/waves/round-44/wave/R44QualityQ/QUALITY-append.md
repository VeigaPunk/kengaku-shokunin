## Round44 criterion — a flip verdict is checked against the entry it concerns

- **Q36 — a `Flip check (round N): <item> — not fired — <evidence>` resolution counts only when the entry the refusal is
  about carries no unbacked `<item>:<line>` citation; Q35 reads that the sentence exists, never that it is true, and a
  present false sentence is the round-43 defect Q35 was written to close.** Q35 landed as `plans/gate_flip_check.py`
  (sha256 `d849250da6b3815dba421d5a…`) and reads one lesson file: it takes `## Gate`, keeps the refusals whose text states
  a flip, and accepts a later line whose state is `fired` or `not fired`, whose evidence is ≥2 non-placeholder words and
  whose round is not older than the file name (`:37-46`). It never opens an entry. On the round-43 lesson, whose
  `task.toml` resolution is false, it prints `FLIPS total=2 unresolved=0`, exit 0
  (`.ufo/waves/round-44/wave/R44QualityQ/q35-round43.txt`). The verdict is false by the entry's own citations:
  `awk '/^## Located quotes/{s=1;next} /^## /&&s{s=0} !s' corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md`
  keeps 7 lines citing `task.toml:<line>`, none carrying an `S1xx` co-citation, among them the Mechanism row
  `| slow-oracle-45s | task.toml:22 |` and `:122` "the only ceiling is `task.toml:22`'s 1800 s verifier timeout"; the same
  scan gives `solve.sh` 3 unbacked, `setup.py` 1, `feal.h` 0, `SHA256SUMS` 0. The disagreement is recorded at
  `corpus/lessons/round-43-verifier-spotcheck.md:124` — "**disagree** (on the flip verdict; I agree with refusing them as
  rows)" — and routed as closure R1 at `:156`.
  Check (executable, round-44 instance): take each `not fired` resolution, the items it names and the entry the lesson's
  Gate concerns; strip the entry's `## Located quotes` section; red the line when any `<item>:<line>` hit carries no `S1xx`.
  The round-44 demonstration driver is `.ufo/waves/round-44/wave/R44QualityQ/flip_verdict_demo.py` (receipt beside it);
  `python3 …/flip_verdict_demo.py <clone>` prints `INSTANCE lesson=corpus/lessons/round-43.md:46 item=task\.toml
  recorded=not fired body_hits=7 unbacked=7 verdict_truth=fired RED` and `INSTANCE lesson=corpus/lessons/round-42.md:215
  item=README\.md recorded=not fired body_hits=0 unbacked=0 verdict_truth=not fired ok`. The same leg, drafted at
  `.ufo/waves/round-44/wave/R44FlipVerdict/gate_flip_check.py` (digest `31db1154…`, unlanded at this draft), prints
  `FLIP-CITE … verdict=RED` with `not_fired=2 red=1` and exit 1 on round 43, exit 0 on round 42. The leg lands in
  `plans/gate_flip_check.py` — a file that exists at this draft — as a `FLIP-CITE` line; a Check line that names only an
  unlanded wave path repeats the round-42 closure C1 defect.
  Shown able to fail: the red and the green above differ by the entry's bytes alone. The round-42 `README.md` verdict is
  true (0 body citations) and stays green, so the leg is per item, not a blanket `not fired` → red; the round-43
  `task.toml` line is red on 7 hits, and per named item the same rule reddens `setup.py` (1) and `solve.sh` (3) while
  `feal.h` and `SHA256SUMS` stay clear.
  Limits: the rule reads citations, not meaning — an entry that rests on a refused file without writing `<file>:<line>`
  passes, and a `fired` line's evidence is still never read (Q35's limit survives this leg); item names are bare file
  names, so a sibling task's entry is counted — the wave draft reports `item=task.toml … citation=
  tb2-circuit-fibsqrt-grader.md:332`, a different task's `task.toml`, so one line reddens for two right reasons and one
  wrong one; an inactive leg reads green — the same draft prints `FLIP-CITE entries=- missing=instruction.md,README.md,
  R42PkgRows.md not_fired=1 red=0` on the round-42 lesson because that lesson's Gate names no resolvable entry, and an
  entry never examined must be exit 2, not exit 0; a resolution naming a package rather than a file (`round-43.md:47`
  `merge/kengaku/`) has no citation to read and prints `files=- verdict=clear`, which is not a pass either; the
  `## Located quotes` exclusion is the current entry shape's convention, so a `<file>:<line>` quoted in another section
  counts as prose; and no leg says whether the refused item deserved a row — the S135–S137 admit path stays a judgement.
  Lesson: `corpus/lessons/round-43-verifier-spotcheck.md:124` (the disagreement) and `:156` (closure R1, the fix this
  criterion states); the first instance is `corpus/lessons/round-43.md:46`. Supersedes: none; it adds a truth leg to Q35
  and leaves Q35's existence rule, its exit 2 and its malformed-line handling unchanged.

## Round44 criterion — a do-nothing control runs the lane's standing batteries too

- **Q37 — the do-nothing control of a calibration claim is two runs over the same frozen mutant list — no battery, and the
  lane's standing batteries copied in as the battery — and every mutant the second run kills leaves the frozen list before
  the freeze, because "no battery kills it" is new work only when the batteries already in the lane do not.** Q31's
  control proves a predicate is not vacuous with respect to its own list (`claims/control-c1-nothing.txt`:9-14 `BATTERY
  fixtures=0`, `MUTANTS total=5 killed=0 survived=5`, `PREDICATE C1 fail`); it cannot see that a mutant was already
  demonstrated by a battery that landed after the table was written. Round 44's pre-freeze draft is the measured instance:
  `R43PlanNext` priced six mutants with the cell "**6/6 killed attributed** by scratch fixtures (B.3); 0 killed by
  battery42 (B.2)" (`.ufo/waves/round-43/build/R43PlanNext.md:184`), true while battery42 was the whole lane; battery43
  landed in round 43 (`77ea425`, 19:24:42) and its `a_alt-slug-deepest` (`plans/battery43/a_alt.py:411`) kills U3. The
  standing-battery run over all six prints `MUTANT U3 anchor rc-mirror killed by=a_alt-slug-deepest attributed=L354
  value=differs hits=16` (`claims/control-c1-standing-batteries-six-mutant-draft.txt:88`), `BATTERY fixtures=71 …` (`:94`),
  `MUTANTS total=6 killed=1 survived=5 …` (`:95`), `PREDICATE C1 fail`; the frozen five print `total=5 killed=0
  survived=5` (`claims/control-c1-standing-batteries.txt:92-93`). U3 was dropped before the freeze
  (`plans/round-44-claims.md:33`, "U3 was priced too and **dropped before freeze**") and the counter records why
  (`plans/round44_c1_verify.py:6`: "U3 is killed there by battery43 `a_alt-slug-deepest`, so it is already demonstrated and
  left out").
  Check (executable, round-44 instance): copy `plans/battery42/*.py` and `plans/battery43/*.py` into one directory under
  distinct file names and run the frozen counter twice on a clean clone — `python3 plans/round44_c1_verify.py --lane
  <clone> --battery-dir <dir> --work <w>` must print `BATTERY fixtures=71 wrong=0 tampered=0 sidechannel=0`, `MUTANTS
  total=5 killed=0 survived=5 invalid=0 null_detected=0 unattributed=0`, `PREDICATE C1 n/a (non-default battery or mutant
  subset)`; without `--battery-dir` the same counter must print `BATTERY fixtures=0`, the same `MUTANTS total=5 killed=0
  survived=5 …`, `PREDICATE C1 fail`. Receipts for both: `.ufo/waves/round-44/wave/R44QualityQ/standing-battery.txt` and
  `…/no-battery.txt`. Both are freeze controls run before the freeze; a claims file that does not name each removed mutant
  with its standing killer has not run the second.
  Shown able to fail: the six-mutant list over the same 71 fixtures prints `killed=1`, so the control reddens exactly the
  row a round would otherwise book as new work, and the red half is reconstructible from committed material — U3's tuple is
  `.ufo/waves/round-43/build/R43PlanNext/u_mutants_table.txt:2-6`, the frozen literals `TOTAL = 5` / `FLOORS = {"anchor":
  4, "order": 1}` are `plans/round44_c1_verify.py:147-148`.
  Limits: the standing-battery run is development mode and prints `PREDICATE C1 n/a`, so it is never landing evidence; the
  copied modules keep their fixture ids, so a standing id reused by a `battery44` module is refused as `SETUP duplicate
  fixture id` (`plans/round44_c1_verify.py:809`, exit 2) and one side must rename; the control sees only batteries present
  in the tree at the freeze; it forbids counting one kill twice, not a second kill of the same mutant for a different
  reason; a battery module the counter's contract cannot express is outside the run; and the six-mutant half is the L1's
  own pre-freeze receipt — a non-author reconstructs it from `u_mutants_table.txt` plus the frozen counter, not by
  re-running a counter draft that was never committed.
  Lesson: the U3 mis-price (`R43PlanNext.md:184` against `claims/control-c1-standing-batteries-six-mutant-draft.txt:88`) and
  the lane's pre-freeze correction (`plans/round-44-claims.md:33`; `plans/round44_c1_verify.py:6-7`). Supersedes: none; it
  extends Q31 — which asks whether the predicate can be satisfied without the work — by the question Q31 cannot ask:
  whether the work was already done by the lane.

## Round44 criterion — a content leg's key comes from executing the pinned source

- **Q38 — a content leg's verdict key is produced by executing the pinned source over generated end states and is stored
  nowhere in the counter; a key read off the instrument's own map, or off the source's prose, is a copyable answer and it
  disagrees with the source on exactly the states that separate the readings.** V10 (round 43) keeps a readable DECISIVE
  map in the counter, so a filler satisfies it (`R43CritClaims` §1; closure R5 at
  `corpus/lessons/round-43-verifier-spotcheck.md:169`). V11 is the first executed leg: `plans/round44_c2_verify.py:34-43`
  builds 48 end states from the 100 pinned constants, runs the captured grader's `test_attack` on each inside a sandbox and
  the entry's `predict` on each in a second, requires 0 disagreements and ≥8 passes and ≥8 fails, and states at `:40-42`
  "The verdicts are never stored here: they exist only by executing the grader, so a filler cannot copy them from the
  counter" and at `:379` "STATES is a generator, not an answer key: no verdict is stored in this file".
  Measured (`claims/control-c2-predictor.txt:3-7`, re-run by this seat into
  `.ufo/waves/round-44/wave/R44QualityQ/c2-predictor.txt` at 20:39:40): always-true `disagree=24`; whitespace-token-set
  `disagree=12` at `concat#4,zero-pad#5,comma#11,prefixed-digit#15,…`; exact-lines `disagree=18`; substring `disagree=0`;
  `CONTROL-C2-PREDICTOR red-as-required`, every line `states=48 grader_pass=24 grader_fail=24`. The reds are the readings a
  careful reader writes from the test file's text — one constant per line, the file's tokens are the constants — and they
  are wrong only where the executed `assert c in data` over the whole file accepts concatenated, zero-padded or
  decoy-bearing content.
  Check (executable, round-44 instance): `python3 plans/round44_c2_verify.py --lane .` prints `checks=11 defects=0`, then
  `PREDICATE C2 pass`, exit 0, V11 among the 11; `python3 .ufo/waves/round-44/claims/c2_predictor_control.py <work>`
  prints the four `CONTROL` lines and `CONTROL-C2-PREDICTOR red-as-required`, exit 0.
  Shown able to fail: three of the four control keys are red with named states and counts, and the non-vacuity leg (24
  passes and 24 fails of the 48) removes the always-pass escape, so the green substring key is not the empty key.
  Limits: the states come from `random.Random(44)` cycling 16 state kinds, so a predictor can be tuned to the generator —
  the docstring's answer is that tuning requires running the grader, which is the reading asked for; only
  `/app/plaintexts.txt` varies between states, so a decision that also read another input is under-modelled; the captured
  grader runs under the host `python3`, not the image's 3.13 (the claims' own limit); a correct predictor is a predictor of
  the graded decision, never of whether that decision is worth grading; and "no key stored" is a property of the frozen
  bytes at the pinned digest — nothing prevents a counter that executes the source once at freeze and embeds booleans
  behind a generator, so the pin makes that a reviewable edit, not an invisible one.
  Lesson: `.ufo/waves/round-43/build/R43CritClaims.md` §1 (V10's readable key) and closure R5
  (`corpus/lessons/round-43-verifier-spotcheck.md:169`); the lane's own statement of the residual is `plans/round-44-claims.md`
  §C2 V11. Supersedes: none; it closes V10's readable-key limit without relaxing V10.
