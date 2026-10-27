# Round 49 — frozen claims (kengaku, hyaku run 10, 2026-10-28)

Baseline lane tip `3a548330c4899c6c5df34168a44a59f66828ce74` (the run-9 wrap-up chain plus the round-48
landings; `jj-lane.sh state` at round start: local=remote=`3a548330`, ahead=0, tracked=0). L1 `KengakuR49`
holds the canonical planner seat and is the single integration owner. Provenance: the round-48 closure
(`corpus/lessons/round-48-verifier-spotcheck.md`, verdict `rejected-honest-stop`) routed four defects into this
round — (1) a receipt path per seat item, (2) no role→alias map in the wave context, (3) the V7
unsatisfiable-tag precondition enforced before scoring, (4) the C1 mutation floor committed *with receipts*.
The round-48 lesson (`corpus/lessons/round-48.md`) is the defect source for both claims below.
`.ufo/watchdog.log` launches attempt 1 at 2026-10-28T08:59:38-03:00; no earlier attempt of round 49 exists.

Axis state carried (SCORECARD round-48 table): calibration 8, coverage 7 (capped by L0 `kengaku | round-33`),
novelty 7, depth 9, operability 8, freshness 8, adjacency 8. Lowest non-retired: coverage 7 tied with
novelty 7; **coverage** is worked (C2, frozen tie-break as in rounds 44–48) and **calibration** is worked (C1 —
the routed repair now carries the measured 8/120 base refusal, never the unreproducible r46 placeholder-argv
9/9 figure). No stagnation waiver. Two claims on two distinct axes; causally separable (their counters, files
and receipts are disjoint; C1 touches nothing C2 verifies and vice versa).

**Freeze shape (declared now, before any data).** Stage 1 (this commit): the predicate sentence, the counter
contract and its deltas, the controls that must fail, and the kill rule — for each claim. Stage 2 (one
amendment commit, after the wave returns and BEFORE any claimed work is scored): the counter files, their
input pins, the frozen fixture/module/mutant populations, the amended probe revision with its new dry table,
the literals `<P>`, `<H>`, `<S>`, `<B>`, `<M>` (C1) and `<V>`, `<N>` (C2), and the before-control receipts,
each run on the base or a control tree — never on the claimed work. Stage 2 may fill literals and pins; it may
not change a predicate line, a control, or a kill rule written here. Stage 3 (C2 only, one landing commit): the
first full probe run's receipt and its pin — see the C2 ordering rule; no predicate line changes. Any other
edit of this file after this commit is named, with its commit, in a `Freeze amendments` paragraph appended
below (round-45 closure D4; round-46 lesson mistake 4).

**Receipt discipline (Q22).** Every receipt this round prepends `REV <40-hex>` of the tree it measured; a
content-measured receipt says `REV <40-hex>` of the clone it ran in plus `TREE-BYTES` when the clone is
uncommitted.

**Ordering (Q30).** No full probe of the C2 package runs before the stage-3 commit lands the receipt; only
`--dry` and `--stage-check` are run pre-receipt. Pre-receipt controls run the C2 gate with its P10 (fresh
probe re-run) leg disabled — that is the V8 fix, frozen here, not a post-hoc edit. The stage-2 amendment is
committed only after the amended probe revision passes `--stage-check` on this host — the fresh falsifiable
control the planned row requires (the failed `22b7779e` revision failed 18/18 stage-checks under
`RLIMIT_NPROC=48`); its fail-receipt on the `22b7779e` revision is a committed stage-2 control.

## C1 — calibration: the fixture fence's honest over-refusal repaired, re-judged under a v3 counter whose honest population and mutation floor are frozen before scoring

- **Self-assessment under test.** `plans/fixture_fence.py` (round-46 variant-A allowlist) advertises: admit
  only a fixture whose git store, discovered repos and argv stay inside `d`, deciding without reading outside
  `d`. Round-48 measured the breach on the frozen 120-fixture population (`w1/R48C1ExecCounter.md`, scratch
  `REV a543d920…`): `HONEST fixtures=120 admitted=112 refused=8` — the base fence over-refuses 8 honest
  fixtures, and the r46 "9/9" figure does not reproduce (all nine r46 override modules used `{WORK}`
  placeholder argv; `w1/R48C1ExecControls.md:16-18`). Round-48's repair candidate measured 120/120 honest
  admissions with refusals 20/20 and sealed 12/12 in its development harness (`w1/R48C1ExecFenceA.md`), but no
  counter, fence or population landed in a stage-2 commit, and no fence-mutant battery was reported — the two
  defects this claim answers.
- **Counter** `python3 plans/round49_c1_verify.py --lane .` (written in wave 1, pinned at stage 2). Contract =
  `plans/round46_c1_verify.py` (digest-pinned, imported) plus these frozen deltas:
  - (a) **honest population frozen at stage 2** = the 104 fixtures of `plans/battery42|43|44` + the 16 novel
    honest classes of `w1/R48C1ExecHonest/` (the 9 r46 classes rebuilt + 7 r48 classes), each committed at
    stage 2 under `plans/honest49/` with per-module digests pinned, **plus** the novel honest classes authored
    by wave-1 seats this round against the *base* fence description (count folded into `<H>` at stage 2);
  - (b) **behavioural classification** — `LEAK` only on traced opens/reads outside `d`; an admission with
    `touches=0` is `BENIGN-ADMIT`, counted separately, never a leak; the kill rule keys on hostile behaviour;
  - (c) name-hiding (Q39) retained: per-run random tokens, padded parents, shuffled jobs;
  - (d) the strace envelope B1/B3/B4/B5/B6 legs retained; the verdict travels as the harness exit status;
  - (e) REFUSALS = the 20 frozen `plans/refusals46/` modules; SEALED = the 12 frozen `plans/sealed46/` modules
    plus the wave-1 held-out hostile modules authored against the *landed* fence candidate, committed at
    stage 2 under `plans/sealed49/` (count `<S>` pinned at stage 2);
  - (f) **MUTANTS leg (new, the round-48 routed gap)** — `<M>` fence mutants declared in
    `plans/mutants49/c1-mutants.json` (payload path + digest + description per mutant, authored by wave-1
    mutation-tester seats against the *landed* fence); the counter applies each mutant to a copy of the
    landed fence and re-measures the three legs on that copy; a mutant is *caught* iff the mutated fence no
    longer prints the clean signature (any new LEAK/READ/refusal or HONEST refusal). Fewer than `<M>/2`
    caught → the counter prints `MUTANTS … caught=<k> floor=<M>/2` then `PREDICATE R49-C1 fail`. The battery
    runs **with committed receipts**: its per-mutant output is part of the landing receipt, closing the
    round-48 gap "the ≥12-mutant kill battery was never reported".
- **Frozen predicate.** C1 passes iff the counter prints `PINS total=<P> mismatched=0`, then
  `REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0`, then
  `SEALED total=<S> clean=<S> leaked=0 read=0 hung=0 build_errors=0`, then
  `HONEST fixtures=<H> admitted=<H> refused=0 read=0 hung=0 build_errors=0`, then `BENIGN total=<B>`
  (informational), then `MUTANTS total=<M> caught=<k> floor=<M>/2 verdict=met`, then
  `CALIBRATION advertised=<20+S> contradicted=0`, then `PREDICATE R49-C1 pass`, exit 0, on a clean clone of
  the landing tip. `<M>` ≥ 12, frozen at stage 2.
- **Controls that must print `PREDICATE R49-C1 fail` at stage 2** (receipts under
  `.ufo/waves/round-49/claims/`): no fence; the **base fence** (`plans/fixture_fence.py` @ `3a548330`, the
  before value — the frozen population includes classes it refuses); the round-45 keyed fence; admit-all;
  refuse-all; a name-keyed fence. A control that passes refuses the counter: the claim stops honestly, never
  re-frozen after scoring.
- **Work.** `plans/fixture_fence.py` repaired (wave-1 executor variants; the L1 lands one) so every frozen
  honest class is admitted while every frozen refusal/sealed hostile module stays refused with zero traced
  outside access. The `w2/R46W2C1Intent.md` mount-point boundary is honoured: an honest fixture whose store
  sits on a mount boundary inside `d` is admitted iff every byte the decision reads is inside `d`.
- **Kill rule.** Any predicate line off at the landing tip → C1 not admitted. Any SEALED or held-out module
  with traced outside access admitted → C1 not admitted. Any HONEST refusal → C1 not admitted. Mutation floor
  unmet (`<M>` mutants, caught < `<M>/2`) → C1 not admitted (round-46 observed 2/13; the floor and receipts are
  committed, never asserted).

## C2 — coverage: the round-46 TB2 `polyglot-c-py` package admitted under a Q40 re-frozen counter, with every frozen tag violated by a committed case, P10-disabled pre-receipt controls, a mutation-sensitivity floor, and ordering that makes the fresh receipt possible

- **Surface.** The round-46-committed package: `corpus/knowledge/tb2-polyglot-c-py-grader.md`, SOURCES rows
  S166–S172, captures under `corpus/evidence/round46/tb2-polyglot-c-py/` + `SHA256SUMS` at terminal-bench-2
  `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, the executed receipt
  `corpus/evidence/round46/polyglot-c-py-probe.txt`, the frozen dry-case table
  `corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt`, and `plans/polyglot_c_py_probe.py`. The
  round-46 admission failed on its own frozen counter (V7: `both-print`/`toolchain` carry no violating case;
  V8: a pre-receipt control ran the gate's P10). Round-48 then measured two probe defects in the hardened
  `22b7779e…` revision (`w1/R48C2ExecProbe.md`): its `prlimit --nproc=48` cannot create a sandbox under this
  host's uid thread load (~1100 threads), and its `mode="all"` grade path never runs seed/recipe, so every
  predicted pass flips to fail.
- **Class (as worded in round 46).** One file `/app/polyglot/main.py.c` executed by two toolchains; three
  fixed points; exact-directory precondition. This round claims its **admission**, not a new class.
- **Counter** `python3 plans/round49_c2_verify.py --lane .` (written in wave 1, pinned at stage 2) =
  `plans/round46_c3_verify.py` (digest-pinned, imported) plus these frozen deltas:
  - (a) **V7 fix (Q24)** — before the verdict, positively verify from the frozen tables: every frozen tag is
    cited by at least one committed receipt case `violates=` token; every requirement-map row parses to the
    header's column count; violating cases exist for `both-print` and `toolchain`. The case table is amended
    **in the probe** at stage 2 — new cases added or re-worded, never tag names re-worded — so all seven tags
    are violated by a committed case; the new dry table lands at
    `corpus/evidence/round49/polyglot-c-py-dry-cases.txt` and the new receipt at stage 3 at
    `corpus/evidence/round49/polyglot-c-py-probe.txt`.
  - (b) **V8 fix (Q30/Q40)** — the base/filler/echo controls run the package gate with P10 disabled;
    `plans/order_check.py` pins each control's ordering receipt; the **fresh receipt** lands at stage 3 as
    this claim's first full probe run, and V8 verifies ordering from `git log`: the receipt's first-commit is
    the stage-3 commit, a descendant of the stage-2 commit, and carries `CASE … observed=` lines — replacing
    the round-48 inherited-receipt rule, which could never satisfy V7 on an amended table (a stage-2 receipt
    could not name cases a post-stage-2 probe run produces).
  - (c) **V15 (preconditions dry-run)** — every frozen input digest resolves and every leg's frozen table
    parses before any leg scores; a missing/tamper-pinned input is a DEFECT of that leg, not a crash.
  - (d) **V14 (mutation battery)** — `<N>` fresh mutants of committed package bytes (capture, entry, receipt,
    dry table, spec, probe) declared in `plans/mutants49/plan.json`; each must flip at least one substantive
    leg (V3/V4/V7/V9/V10/V12) to DEFECT; fewer than `<N>/2` caught → `MUTATION DEFECT` and the predicate
    fails.
  - (e) **probe repair (the `22b7779e` control)** — the stage-2 probe revision must (i) pass `--stage-check`
    on this host before stage 2 commits, and (ii) run seed+recipe on its grade path; both are falsifiable
    controls the wave authors, and the `22b7779e` revision's failure receipts are committed stage-2 controls.
  - (f) V13 filler control retained; V11 held-out predictors retained with the round-46 refusal lint.
- **Frozen predicate.** C2 passes iff the counter prints `checks=<V> defects=0`, then
  `PREDICATE R49-C2 pass`, exit 0, on a clean clone of the landing tip; `<V>` and `<N>` fixed at stage 2
  (`<V>` counts every leg including V14 and V15).
- **Controls that must print `PREDICATE R49-C2 fail` at stage 2** (receipts under
  `.ufo/waves/round-49/claims/`): the base tree (no `plans/polyglot_c_py_probe.py`); the round-46 filler
  package; the echo receipt (dry table copied as the receipt). A control that passes refuses the counter.
- **Kill rule.** Any V defect → C2 not admitted. Mutation battery below floor → C2 not admitted. Any frozen
  tag without a committed violating case → C2 not admitted (V7, positively enforced). A receipt whose
  first-commit is not the stage-3 commit → C2 not admitted (V8 ordering).
- **Sourced basis (§2b).** This claim rests on S166 (`tests/test_outputs.py` at the pin), reopened this round
  by the L1 at the pinned URL on 2026-10-28 (sha256 `b94a7a98…`, byte-equal to the committed capture);
  URL, access date and located quote are recorded in the round-49 lesson's `## Gate`.

## Separability

C1 touches `plans/fixture_fence.py`, `plans/round49_c1_verify.py`, `plans/refusals46/` + `plans/sealed46/`
(read-only), `plans/honest49/`, `plans/sealed49/` and `plans/mutants49/c1-mutants.json`. C2 touches
`plans/polyglot_c_py_probe.py` (amended), `plans/round49_c2_verify.py`, `plans/pkg-spec-r49.json`,
`plans/mutants49/plan.json`, the round-46 package paths (entry requirement map repair, new dry table and
receipt under `corpus/evidence/round49/`), and `plans/order_check.py` (read-only). The counters share no
input; a C1 failure cannot green or red any C2 leg and vice versa. Both counters name `REV` receipts.

## Do-nothing controls (§9, frozen before data)

- C1: the fence at base tip `3a548330` under the stage-2 pinned v3 counter must fail on the honest leg
  (measured 8/120 refusals on the frozen population by round-48; the stage-2 receipt re-measures on the
  extended population).
- C2: the base tree under the v4 counter must fail (no `plans/polyglot_c_py_probe.py`); the filler and echo
  controls must fail; the `22b7779e` revision's stage-check and mode-all receipts must fail. The round-46
  counter state (V7/V8) is committed evidence (`.ufo/waves/round-46/integrate/c3-landing.txt`) re-measured as
  the C2 before-receipt at stage 2.

## Freeze amendments

None yet. Stage 2 fills literals and pins only; stage 3 (C2) lands the fresh receipt and its pin only.
