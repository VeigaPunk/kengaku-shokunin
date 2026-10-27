# Round 48 — frozen claims (kengaku, hyaku run 10, 2026-10-27)

Baseline lane tip `0f77f9b27931b3c76b3d095fc0fa70edb79556d9` (the hyaku run-9 wrap-up commit that inherited the
round-47 dispatch spec state). L1 `KengakuR48` holds the canonical planner seat. Fresh-start provenance
(run-10 block): the last three rejected closures were read before any claim was declared — round 45
(`73540ccc…`, rejected-harmed: C1 counter passed by a path-keyed control; C2 predictor-review rider fails;
depth harmed), round 46 (`a5ed97f1…`, rejected-harmed: C1 frozen kill rule fires — 3 held-out admissions,
9/9 novel honest fixtures refused, 2/13 fence mutants caught; C3 frozen counter fails V7/V8), round 47
(`98a0cb51…`, rejected-honest-stop: 64-seat v2 wave spec built and validator-accepted but never dispatched
before run-wrap; nothing frozen, nothing landed). The round-46 non-author spot-check
(`corpus/lessons/round-46-verifier-spotcheck.md`) is the defect source for both claims below. `.ufo/watchdog.log`
launches attempt 1 at 2026-10-27T06:43:20-03:00; no earlier attempt of round 48 exists.

Axis state carried (SCORECARD round 46 wave-2 verdicts): calibration 8 (held — kill rule fired), coverage 7
(capped by L0 `kengaku | round-33`; the r46 package is committed but unadmitted), novelty 7, depth 9, operability 8,
freshness 8, adjacency 8. Lowest non-retired: coverage 7 tied with novelty 7; **coverage** is worked (C2 below,
frozen tie-break as in rounds 44–46). No stagnation waiver. Two claims on two distinct axes; causally separable
(their counters, files and receipts are disjoint; C1 touches nothing C2 verifies and vice versa).

**Freeze shape (declared now, before any data).** Both claims freeze in two stages. Stage 1 (this commit): the
predicate sentence, the counter contract and its deltas against the round-46 counters, the controls that must
fail, and the kill rule — for each claim. Stage 2 (one amendment commit, after wave 1 returns and BEFORE any
claimed work is scored): the counter files, their input pins, the frozen fixture populations, the literals
`<P>`, `<H>`, `<S>`, `<B>`, `<M>` (C1) and `<V>` (C2), and the before-control receipts, each run on the base or a
control tree — never on the claimed work. Stage 2 may fill literals and pins; it may not change a predicate
line, a control, or a kill rule written here. Any other edit of this file after this commit is named, with its
commit, in a `Freeze amendments` paragraph appended below (round-45 closure D4; round-46 lesson mistake 4).

**Receipt discipline (Q22).** Every receipt this round prepends `REV <40-hex>` of the tree it measured.

**Ordering (Q30).** No probe of the C2 package runs before the stage-2 commit. Pre-receipt controls run the
C2 gate with its P10 (fresh probe re-run) leg disabled — that is the V8 fix, frozen here, not a post-hoc edit.

## C1 — calibration: the fixture fence's honest over-refusal repaired, re-judged under a v3 counter whose honest population is frozen before scoring and whose kill rule keys on traced outside access

- **Self-assessment under test.** `plans/fixture_fence.py` (round-46 variant A allowlist) advertises: admit only a
  fixture whose git store, discovered repos and argv stay inside `d`, deciding without reading outside `d`. The
  round-46 counter predicate passed at the landing tip (`integrate/final-tip.txt` at `264b7757`), but the wave-2
  falsification found two behavioural defects: **(i) over-refusal** — 9/9 novel honest fixture classes refused
  (`w2/R46W2C1HoHonest.md`: packed refs after `gc`/`pack-refs`, annotated tags, detached HEAD, a merge commit,
  `.gitignore`, a 30-commit linear history, reflog gc, annotated-tag-plus-detached-HEAD, an ignored untracked
  file — all ordinary `git init` repository states); **(ii) misclassified held-outs** — 3 benign held-out modules
  admitted with `touches=0` (`w2/R46W2C1HoArgv.md` 2 argv-shape, `w2/R46W2C1HoPaths.md` 1 paths-shape), counted as
  LEAK by the detector override semantics even though no outside path was observed. The round-46 frozen kill rule
  (≥2 held-out admissions → not admitted) fired on (ii); the calibration breach is (i).
- **Counter** `python3 plans/round48_c1_verify.py --lane .` (written in wave 1, pinned at stage 2). Contract =
  `plans/round46_c1_verify.py` (digest-pinned, imported) plus these frozen deltas:
  - (a) **honest population frozen at stage 2** = the 104 fixtures of `plans/battery42|43|44` + the 9 round-46
    novel honest classes (each rebuilt from its `w2` report description) + the novel honest classes authored by
    wave-1 critic seats, each authored against the *base* fence description, not against any repaired fence;
  - (b) **behavioural classification** — a fixture result is `LEAK` only if traced opens/reads outside `d` are
    observed (touches>0 or READ); a fixture admitted with `touches=0` is reported as `BENIGN-ADMIT` and counted
    separately, never as a leak; the kill rule keys on hostile behaviour, not on admission;
  - (c) name-hiding (Q39) retained: fixture dirs, build dirs and module copies are named by a per-run random
    token, fence jobs run in shuffled order;
  - (d) the strace envelope B1/B3/B4/B5/B6 legs retained; the verdict travels as the harness exit status;
  - (e) REFUSALS = the 20 frozen `plans/refusals46/` modules; SEALED = the 12 frozen `plans/sealed46/` modules plus
    the wave-1 held-out hostile modules authored against the *landed* fence (count `<S>` pinned at stage 2).
- **Frozen predicate.** C1 passes iff the counter prints `PINS total=<P> mismatched=0`, then
  `REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0`, then
  `SEALED total=<S> clean=<S> leaked=0 read=0 hung=0 build_errors=0`, then
  `HONEST fixtures=<H> admitted=<H> refused=0 read=0 hung=0 build_errors=0`, then
  `BENIGN total=<B>` (informational only), then `CALIBRATION advertised=<20+S> contradicted=0`, then
  `PREDICATE R48-C1 pass`, exit 0, on a clean clone of the landing tip.
- **Controls that must print `PREDICATE R48-C1 fail` at stage 2** (receipts under `.ufo/waves/round-48/claims/`):
  no fence; the **base fence** (`plans/fixture_fence.py` @ `0f77f9b`, the before value: the 9 round-46 novel
  honest classes refused — `HONEST … refused=9` minimum); the round-45 keyed fence; admit-all; refuse-all.
  A control that passes refuses the counter: the claim stops honestly, it is never re-frozen after scoring.
- **Work.** `plans/fixture_fence.py` repaired (wave-1 executor variants; the L1 lands one) so that every frozen
  honest class is admitted while every frozen refusal/sealed hostile module is still refused with zero traced
  outside access. The mount-point refusal noted in `w2/R46W2C1Intent.md` is honoured: an honest fixture whose
  store sits on a mount boundary inside `d` is admitted iff every byte the decision reads is inside `d`.
- **Kill rule.** Any predicate line off at the landing tip → C1 not admitted. Any SEALED or held-out module with
  traced outside access (touches>0 or READ) admitted → C1 not admitted. Any HONEST refusal → C1 not admitted.
  The fence-mutant battery: wave-1 mutation-tester seats author `<M>` fresh mutants of the landed fence; fewer
  than half caught by the frozen counter → C1 not admitted (round-46 observed 2/13; the floor is frozen at
  stage 2 with `<M>` and must be ≥ 12 mutants, floor `<M>/2`).

## C2 — coverage: the round-46 TB2 `polyglot-c-py` package admitted under a Q40 re-frozen counter, with every frozen tag violated by a committed case, P10-disabled pre-receipt controls, and a mutation-sensitivity floor

- **Surface.** The round-46-committed package: `corpus/knowledge/tb2-polyglot-c-py-grader.md`, SOURCES rows
  S166–S172, captures under `corpus/evidence/round46/tb2-polyglot-c-py/` + `SHA256SUMS` at terminal-bench-2
  `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, the executed receipt `corpus/evidence/round46/polyglot-c-py-probe.txt`,
  the frozen dry-case table `corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt`, and the hardened probe
  `polyglot_c_py_probe.py` (sha256 `22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d`, wave artifact
  `.ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py`) integrated verbatim to `plans/polyglot_c_py_probe.py`.
  The round-46 admission failed on its own frozen counter: V7 (frozen tags `both-print` and `toolchain` carry no
  violating receipt case) and V8 (a pre-receipt control executed the gate's P10).
- **Class (already worded in round 46, from `tests/test_outputs.py` at the pin).** One file
  `/app/polyglot/main.py.c` executed by two toolchains; three fixed points; exact-directory precondition. This
  round claims its **admission**, not a new class.
- **Counter** `python3 plans/round48_c2_verify.py --lane .` (written in wave 1, pinned at stage 2) =
  `plans/round46_c3_verify.py` (digest-pinned, imported) plus these frozen deltas:
  - (a) **V7 fix (Q24)** — before the counter prints its verdict it positively verifies, from the frozen tables
    alone: every frozen requirement tag is cited by at least one committed case `violates=` line; every
    requirement-map row parses to the census column count; violating cases exist for `both-print` and
    `toolchain` (the case table is amended at stage 2 — by adding or re-wording cases, never by re-wording
    tags — so all seven tags are violated by a committed case);
  - (b) **V8 fix (Q30/Q40)** — the base/filler/echo controls run the package gate with P10 (fresh probe re-run)
    disabled; `plans/order_check.py` pins each control's ordering receipt; the first full probe run follows the
    stage-2 commit;
  - (c) **V15 (new, preconditions dry-run)** — every frozen input digest resolves and every leg's frozen table
    parses before any leg scores; a missing/tamper-pinned input is a DEFECT of that leg, not a crash;
  - (d) **V14 (new, mutation battery)** — `<N>` fresh mutants of committed package bytes (capture, entry,
    receipt, dry table, spec, probe) authored by wave-1 mutation-tester seats; each mutant must flip at least
    one substantive leg (V3/V4/V7/V9/V10/V12) to DEFECT; fewer than `<N>/2` caught → the counter prints
    `MUTATION DEFECT` and the predicate fails (round-46 observed 0/13);
  - (e) V13 filler control retained; V11 held-out predictors retained with the round-46 refusal lint.
- **Frozen predicate.** C2 passes iff the counter prints `checks=<V> defects=0`, then `PREDICATE R48-C2 pass`,
  exit 0, on a clean clone of the landing tip; `<V>` and `<N>` fixed at stage 2 (`<V>` must count every leg
  above including V14 and V15).
- **Controls that must print `PREDICATE R48-C2 fail` at stage 2** (receipts under `.ufo/waves/round-48/claims/`):
  the base tree (no `plans/polyglot_c_py_probe.py`); the round-46 filler package; the echo receipt (dry table
  copied as the receipt). A control that passes refuses the counter.
- **Kill rule.** Any V defect → C2 not admitted. Mutation battery below floor → C2 not admitted. Any frozen tag
  without a committed violating case → C2 not admitted (the V7 class, now positively enforced).
- **Sourced basis (§2b).** This claim rests on S166 (`tests/test_outputs.py` at the pin), reopened this round by
  a wave seat with URL, access date and a ≤25-word located quote recorded in the round-48 lesson's `## Gate`.

## Separability

C1 touches `plans/fixture_fence.py`, `plans/round48_c1_verify.py`, `plans/refusals46/` (read-only),
`plans/sealed46/` (read-only) and the frozen honest population. C2 touches `plans/polyglot_c_py_probe.py` (new,
from the wave artifact), `plans/round48_c2_verify.py`, the round-46 package paths (entry, captures, receipt,
dry table, spec) and `plans/pkg-spec-r46.json`. The counters share no input; a C1 failure cannot green or red
any C2 leg and vice versa. Both counters name `REV` receipts.

## Do-nothing controls (§9, frozen before data)

- C1: the fence at base tip `0f77f9b` under the stage-2 pinned v3 counter must fail on the honest leg (the 9
  round-46 novel classes are refused by the base fence — evidence already committed at `w2/R46W2C1HoHonest.md`;
  the stage-2 receipt re-measures it on the base fence).
- C2: the base tree under the v4 counter must fail (no `plans/polyglot_c_py_probe.py`); the filler and echo
  controls must fail. The round-46 counter state (V7/V8) is committed evidence (`.ufo/waves/round-46/integrate/c3-landing.txt`)
  and is re-measured as the C2 before-receipt at stage 2.

## Freeze amendments

None yet. Stage 2 fills literals and pins only.
