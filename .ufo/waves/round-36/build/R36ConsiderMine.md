# R36ConsiderMine — considerthese/2026-10-25.md mined against round-35 and round-36 implementations

Seat: scribe (leaf). Scope: proposals 1, 2(a)(b)(c), 3 of
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/considerthese/2026-10-25.md`, measured against lane
bytes at tip `f9efce3beb0705ec2e04ba3f8f449d10d64cc1dd` (wave-1 mid: 14 `R36*` build dirs, no
integrator landing yet). No lane file written; no commit, no index touch, no subagent.

## Behavior (what this seat did)

1. Read the proposal source in full and the frozen claims (`plans/round-36-claims.md`), then located
   each implementation the claims and lessons point at.
2. Ran two read-only counters at the tip and recorded their exact output (below), and searched for any
   code that reads the ledger's `class` field (the mechanical half of clause (b)).
3. Did **not** write, repair or re-freeze any instrument; did **not** run `plans/round35_c1_verify.py`,
   `plans/round35_hardening.py`, the C2 counter or the regex probe.

### Commands and their output (verbatim last lines)

```
$ python3 plans/defect_ledger.py --lane .
R34-D1 status=closed observed=pass agree=yes untracked=0
R34-D2 status=closed observed=pass agree=yes committed_mirror_paths=0
R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
R34-D4 status=closed observed=pass agree=yes correction_lines=1
R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
rows=5 closed=5 observed_pass=5 mismatches=0
PREDICATE C2 pass
# exit=0
```

```
$ python3 plans/round36_c1_verify.py --lane .
FIXTURES total=14 false_green=0 false_red=0 unevaluated=14
R35-D1 status=open observed=fail agree=yes fixtures=14 false_green=0 false_red=0 unevaluated=14 tip_package_rc=None
R35-D2 status=open observed=fail agree=yes untracked_anywhere=817 line_fixtures_wrong=6/6
R35-D3 status=open observed=fail agree=yes committed_nested_wave_paths=21
R35-D4 status=open observed=fail agree=yes round-36 lesson absent; recount 13 + 23 + 1 = 37 vs stated denominator 38
rows=4 closed=0 observed_pass=0 mismatches=0
PREDICATE C1 fail
# c1_exit=1
```

```
$ find . -name 'pkg_gate*' -not -path './.git/*'      # no output: plans/pkg_gate.py is absent at tip
$ git ls-files corpus/evidence | wc -l                # 459
$ git ls-files corpus/evidence | grep -c '\.txt$'     # 156
$ git ls-files corpus/evidence | cut -d/ -f3 | sort -u | wc -l   # 58
$ git ls-files --others --exclude-standard | wc -l    # 817 (wave-1 scratch; was 12 at freeze, see F4)
$ grep -rn '\["class"\]\|get("class")' plans/*.py     # only plans/attrib_probe.py trial classes, not a ledger
$ grep -n "routed-defect\|defect_ledger" SKILL.md     # no match: the ledger is not in the SKILL gate registry
```

## Clause-by-clause: implemented / partly / not

| clause (source line) | status | evidence | still missing |
|---|---|---|---|
| **(a)** re-run every closed defect's check at tip forever (`considerthese/2026-10-25.md:43`) | **implemented** (round 35) | `plans/defect_ledger.py:7-8` states the rule; `:119` reads `corpus/defects.jsonl`; `:122-137` re-runs each row's `check`, scores a mismatch for a `closed` row that fails and for an `open` row that passes, and prints the PREDICATE. Green at this tip: `rows=5 closed=5 observed_pass=5 mismatches=0`, exit 0 (command above). Contract text: `corpus/QUALITY.md:275-284`, `corpus/README.md:404`. | It reads **one** file and that file holds only round-34 rows (`corpus/defects.jsonl`, 5 rows). Round 36's four rows live in a *second* ledger, `corpus/defects-round35.jsonl` (4 rows, all `status=open`), re-run only by `plans/round36_c1_verify.py:41,322` — the per-round-counter pattern proposal 2 was written to end. The r35 checks are not in `plans/defect_ledger.py:111` and no code path will re-run them after round 36 unless someone promotes them. No SKILL.md gate-registry row (`grep` above), so "forever" rests on a seat remembering to call it (round-36's wave-1 sweep does: `.ufo/waves/round-36/build-spec.json`, seat `R36TipSweep`). |
| **(b)** block pre-registration when a class recurs twice (`:43-44`) | **not implemented** | `recurrence_of` is a recorded string only: `corpus/defects-round35.jsonl` row R35-D1 carries `recurrence_of: "R34-D4/R34-D5 …"`, R35-D2 carries `"R34-D1 … and R34-D4/R34-D5 …"`, R35-D3 carries `"R34-D2 …"`. No code reads the `class` field of either ledger (`grep` above: the only `["class"]` hits are `plans/attrib_probe.py` trial labels). The debt is stated, correctly, in `corpus/QUALITY.md:290-292` ("part (b) … is not implemented — `recurrence_of` is recorded, not enforced") and in `corpus/lessons/round-35.md:33`. | Everything mechanical: no pre-registration gate exists to block. The class `counter-accepts-junk` has now recurred twice (R34-D4/R34-D5 → R35-D1) and round 36 pre-registered C1 over it with no block; the freeze answered by construction instead — 14 fixtures and three skip-controls (`.ufo/waves/round-36/claims/control-c1-{accept-all,reject-all,legacy}.txt`) — which is a stronger control but not the proposed rule. A checker that counts distinct rounds per `class` and refuses a freeze where any class count ≥2 is unwritten. |
| **(c)** tip-receipt validator: every `corpus/evidence/**` receipt re-run and byte-compared (`:44-45`) | **not implemented at this tip; begun by C1** | `plans/pkg_gate.py` is absent (`find` above, no output) and the counter scores all 14 fixtures `unevaluated` with `tip_package_rc=None` (command above), matching the freeze control `.ufo/waves/round-36/claims/control-c1-nothing.txt`. The call site that will exercise it is `plans/round36_c1_verify.py:267-275` (`r35_d1`): `package --root <lane> --rerun --require-clean-tree`. C2 builds its own receipt equality for a second instrument: `plans/round36_c2_verify.py:171-191` re-runs the frozen probe and compares `corpus/evidence/round36/regex-log-probe.txt` byte-for-byte (W5). | A. The gate itself: until it lands, clause (c) is 0/1 commands. B. Scope: even landed, it validates **one** receipt of **156** committed `.txt` receipts under `corpus/evidence/` (459 files, 58 dirs); the spec names one `receipt`/`receipt_sha256`/`probe_cmd` triple (`plans/pkg-spec-r35.json:5-12`). C. Shape: `--rerun` re-runs a *pinned command*; a general validator needs a per-receipt command map (the round-36 set alone has receipts whose command is a probe, a suite run and a bye-nowhere file). D. The proposal's motivating case (r31 D3: a receipt rewritten with a wrong relative path at the tip) is only caught where a command is pinned. |

Count for the verdict: **1 of 3 implemented** (a only; b absent, c begun-and-absent).

## Proposal 1 — model-diverse verification: nothing round 36 may claim

`considerthese/2026-10-25.md:34-37` asks for a second model, a fixed seeded sample ≥5/round, an
agreement/disagreement log in SCORECARD, and treats sustained 100 % cross-model, cross-seed agreement
as the only admissible "discernment improved". Round-33 already classified it operator-side
(`corpus/lessons/round-33.md:67-68`: "proposal 1 (model-diverse verification) is operator-side and not
lane-actionable"). Nothing changed at this tip: the round-36 dispatch files carry no per-seat model
field (`grep -c '"model"' .ufo/waves/round-36/build-{spec,dispatch}.json` → 0, 0; `@m_` → 0, 0), and no
agreement or disagreement log exists in `SCORECARD.md` (`grep "model-diverse|seeded sample|agreement
log|second model"` over `plans/ corpus/ SCORECARD.md LOG.md` hits only the round-33 lesson line).
**Round 36 must leave it open**; the honest claim is zero, and the seat-routing observation belongs to
the operator (the round-30 observation that all roles route to `@m_flash` is quoted, not re-measured,
here).

## Proposal 3 — L0 coverage-cap decision packet: still open, quoted

The packet exists only as the L0 line, `.ufo/l0-questions.md:163` (verbatim, 22 words):

> decision packet: what committed evidence lifts the round-25 L0 coverage cap (SCORECARD coverage held at 7 across four rounds of real expansion)?

The line continues past the quote with four candidate classes (a) a `PROVINCE.md` coverage-surfaces
section, (b) further net-new admitted entries, (c) an operator-named rubric change, (d) the cap stays.
No answer line exists and no memo landed in the lane: `grep -n -i coverage PROVINCE.md` returns two
unrelated surface rows (`:109`, `:152`) and no coverage-surfaces section; `grep -rn "coverage-surfaces"`
over `plans/ corpus/` hits nothing. The round-36 freeze records the dependency honestly — claims
`plans/round-36-claims.md` (Axis selection paragraph) and C2's "judged on its counter, not on a score
move". **Round 36 cannot claim a coverage lift; C2 may claim only its counter.**

Friction worth recording (the L1 decides): proposal 3's second half says, until the cap is answered,
*stop* spending the lowest-axis slot on counts that cannot move a score and redirect to novelty or to
opening the S094/S097 rows. Round 36 spends the lowest slot (coverage, 7) on C2 and does not open
S094/S097 (`git ls-files corpus/evidence/round36` holds only the regex-log captures, the probe receipts
and the Toolathlon package). The freeze discloses the choice; it does not cite proposal 3 as its
authority, so the deviation should be named in the lesson rather than smoothed over.

## Draft lesson paragraph (for `corpus/lessons/round-36.md`, e.g. under `## Mines`)

> **Mined — `considerthese/2026-10-25.md` proposal 2 (one persistent routed-defect ledger).** Clause (a),
> re-run every closed defect's check at the tip, is round 35's `plans/defect_ledger.py` and still runs
> green here (`rows=5 closed=5 observed_pass=5 mismatches=0`, exit 0 at `f9efce3`); round 36 adds no row
> to `corpus/defects.jsonl`, and its four rows sit in a second ledger, `corpus/defects-round35.jsonl`,
> re-run only by `plans/round36_c1_verify.py:322` — so the per-round pattern the proposal named survives
> one more round. Clause (b), block pre-registration on a twice-recurred class, remains unbuilt: the
> `class` field of either ledger is read by nothing, and the class of R35-D1 (`counter-accepts-junk`,
> recurred from R34-D4/R34-D5) entered round 36 answered by construction (14 frozen fixtures, three
> skip-controls) rather than by a rule. Clause (c), a `corpus/evidence/**` tip-receipt validator, is begun
> and not built: `plans/pkg_gate.py` is absent at this tip, and when it lands its `--rerun` covers one
> package receipt of 156 committed `.txt` receipts under `corpus/evidence/`. Proposal 1 (model-diverse
> verification) stays operator-side and was not touched; proposal 3's packet is the open L0 line
> `.ufo/l0-questions.md:163`, and C2 claims no score move because of it.

## Draft SCORECARD sentence (round-36 section, in place of / beside the planned calibration row)

> considerthese mined: `considerthese/2026-10-25.md` proposal 2, **1/3 implemented** — (a) stands
> (`plans/defect_ledger.py:119-137`, green `rows=5 closed=5 mismatches=0` at `f9efce3`); (b) not
> implemented, `recurrence_of` recorded and the `class` field read by no code (`corpus/QUALITY.md:290-292`);
> (c) begun only, `plans/pkg_gate.py --rerun` over 1 receipt of 156. Proposals 1 (operator-side) and 3
> (open L0 `.ufo/l0-questions.md:163`) left open; no score move claimed.

## Draft LOG sentence (round-36 entry)

> Mined `considerthese/2026-10-25.md` proposal 2: clause (a) is the round-35 ledger and green at the
> round-36 tip; clause (b) is still unbuilt (`recurrence_of` recorded, never enforced); clause (c) is
> begun by C1's `pkg_gate.py --rerun` and covers one receipt of 156. Proposals 1 and 3 left open
> (proposal 1 operator-side; proposal 3 = L0 `kengaku | round-33`, `.ufo/l0-questions.md:163`).

## Findings for the L1 (no repair attempted; these are wave-1 observations)

- **F1 — two ledgers, two checkers.** `plans/defect_ledger.py:111` holds `r34_d1..r34_d5` only; the
  round-36 rows' checks `r35_d1..r35_d4` live in `plans/round36_c1_verify.py:267-322`. Unless they are
  promoted into the ledger's `CHECKS` next round, R35-D1..D4 are re-run exactly once — the failure mode
  Q23 was written against. This is the concrete debt clause (a) still carries.
- **F2 — the ledger has no SKILL gate-registry row** (`grep -n "routed-defect\|defect_ledger" SKILL.md`
  → no match), the same class as round-31 D4 (`sources_adopt.py` missing from the registry). A fresh
  reader of SKILL.md cannot find the ledger.
- **F3 — `--require-clean-tree` is currently unsatisfiable in the lane.** `r35_d1` calls the gate with
  `--require-clean-tree` over `--root <lane>` (`plans/round36_c1_verify.py:272`) and `r35_d2` counts
  untracked files anywhere (`untracked_anywhere=817` at my run). 817 untracked paths exist at this tip
  because wave-1 seats are writing under `.ufo/waves/round-36/build/`; the count moved 12 (freeze
  control) → 186 → 813 → 817 during this seat's reads. C1 cannot land unless every wave artifact is
  committed (or the tree is clean at the landing tip) — an integration ordering constraint, not a gate
  defect.
- **F4 — the R35-D1 class recurred into round 36 before the freeze.** `control-c1-nothing.txt` records
  `untracked_anywhere=12` at the freeze commit. That is the class R35-D2 opens (recurrence of R34-D1),
  i.e. proposal 2(b) would have blocked a pre-registration at exactly the moment it would have paid.
- **F5 — C2 adds a second one-receipt validator rather than a receipt layer.**
  `plans/round36_c2_verify.py:171-191` byte-compares one receipt to a fresh run; `pkg_gate --rerun`
  (when landed) does the same for another. Two instances of the pattern, still no population-wide check
  (156 `.txt` receipts, 58 evidence dirs, 459 tracked files).
- **F6 — quote discipline for the L0 line.** The `.ufo/l0-questions.md:163` line is longer than 25 words
  when its candidate classes are included; the quoted span above stops at the `?` (22 words). Any later
  citation must cut at the same point or it violates the 25-word CAP.

## Limits of this report

- I did not run `plans/regex_log_probe.py`, `plans/round36_c2_verify.py`, `plans/round35_c1_verify.py`
  or `plans/round35_hardening.py`; C2 statements here cite their code and the frozen claims, not a run.
- No C1/C2 verdict is offered: wave 1 is mid-flight (`plans/pkg_gate.py` absent; `corpus/lessons/round-36.md`
  absent; counter prints `PREDICATE C1 fail`, exit 1). Everything above is a mining report, not a scoring.
- Untracked counts are live and concurrent (817 at the last read); they are evidence of seat activity, not
  a violation by any one seat.
- No tool installed or upgraded by this seat.

## Artifact paths

- Report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-36/build/R36ConsiderMine.md`
- Seat scratch: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-36/build/R36ConsiderMine/` (empty; no fixture clone needed, every read was from the lane tip)

VERDICT: considerthese-mined-1/3
