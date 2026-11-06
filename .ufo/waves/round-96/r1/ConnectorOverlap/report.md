# ConnectorOverlap — round 96 sibling-overlap scan

Seat: `ConnectorOverlapR` (leaf; no subagents). Date 2026-11-05.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (branch `master`).
Measured tip: `T = 09717e49ff46fad5b255619d671aaaae52dfc180`; BASE `45740a61`.
Read-only throughout: greps under `/home/vgpnk/Projects/shokunin/*-shokunin/`, `git show` at T,
one `git clone --shared` fixture at T under `/fast/scratch/hyaku/kengaku-r96/ConnectorOverlap/`
(asserted `rev-parse --show-toplevel` = the clone before any commit). No lane mutation, no
subagent dispatch, no tool installs.

Two surfaces: (a) TB2 grader replays / parquet-pandas graders in sibling lanes; (b) counters that
pin absolute totals vs member sets, standing-gate batteries, bite/grow forgery legs.

---

## (a) TB2 grader replays / parquet-pandas graders

### Scan result

| token / class | sibling files (kengaku excluded) | verdict |
|---|---|---|
| `multi-source-data-merger` | **0** | no sibling lane names the member |
| `merged_users`, `merged_users.parquet` | **0** | no sibling lane names the outputs |
| `conflicts.json` | 5, all unrelated generic names (`p1-conflicts.json`, `pairwise_conflicts.json`) | not this member's output |
| `tb2-*` knowledge entries | **31, all in kengaku** | no sibling owns a TB2 grader entry |
| `Terminal-Bench` / `terminal-bench` | 84 files: 81 under `.ufo/` (connector/report receipts), 2 in kumitate `corpus/` (a published study's benchmark use), 1 souji census note | citations only; **no sibling replay** |

Receipts: `receipts/a-sibling-tokens.txt`, `receipts/a-tb2-ownership.txt`.

Sibling PROVINCE lines that assign this ground to kengaku (read, not renegotiated):
`chousa-shokunin/PROVINCE.md:11` ("or evaluation claims (→ kengaku)"),
`kasegi-shokunin/PROVINCE.md:50` ("kengaku — LLM evaluation and benchmarks"),
`kama-shokunin/PROVINCE.md:42` ("Refuses: model quality/eval (kengaku)"),
`game-dev-3d-shokunin/PROVINCE.md:77` ("LLM/model research and evaluation belong to
`kengaku-shokunin`"), `kumitate-shokunin/PROVINCE.md:25` ("kengaku evaluates agents, this lane
arranges the seats").

### Overlap classifications (a)

1. **Complement — chousa connector seats cite kengaku's TB2 entries, never replay them.**
   `chousa-shokunin/.ufo/waves/round-63/w1/ConnSiblingOverlap.md:69-70` cites
   `kengaku-shokunin/corpus/knowledge/tb2-git-leak-recovery-grader.md:157,284` as a reachability
   case; `chousa-shokunin/.ufo/waves/round-55/w1/R55ConnSiblings.md:67` cites the round-44
   `feal.c` capture. Both are source citations, not executions.
2. **Complement — tameshi's round-58 connector receipt cites kengaku's round-36 receipt bytes.**
   `tameshi-shokunin/.ufo/waves/round-58/w2/T58W2ConnSib-receipts/narrow-60.json:14` quotes
   `evidence/round35/tb2-grader-probe.txt` and `defects.jsonl` from kengaku's tree. No tameshi
   instrument runs a TB2 grader.
3. **Complement — kaidoku's round-90 connector seat read kengaku's probe for isolation, not for a
   replay.** `kaidoku-shokunin/.ufo/waves/round-90/w1/ConnectorOverlap/receipts/kengaku.json`
   records a `read` of `kengaku-shokunin/plans/constraints_probe.py:1-45,235-280,300-315` (the
   round-41 sandbox recipe). It is an outside reading of an older probe; it neither duplicates nor
   conflicts with the round-96 probe.
4. **Complement — the round-96 capture is a superset of the round-52 capture, and the graded files
   are byte-identical.** At T:
   `tests/test_outputs.py` = `a070888930cf…` on both sides, `tests/test.sh` = `d5a00e64413c…` on
   both sides; the round-52 tree holds only those two files, the round-96 tree adds
   `solve.sh`, `Dockerfile`, the three `environment/data` sources, `instruction.md`, `task.toml`.
   So the r79 blocker detector (which reads
   `corpus/evidence/round52/graders/<member>/tests/test_outputs.py`,
   `plans/round79_c1_population_ledger.py:60-70`) reads the same grader bytes the round-96 replay
   executed. This is a consistency check, not a second independent observation of the grader.
   Receipt: `receipts/a-capture-parity.txt`.
5. **Duplicate — none. Conflict — none** on surface (a).

### PROVINCE verdict

**Holds.** The lane's declared domain is LLM/model research & evaluation (`PROVINCE.md:3`); the
TB2 grader replay, the population ledger and the standing battery are all inside it. No sibling
lane claims the surface (0 token hits, 31/31 `tb2-*` entries in kengaku, five sibling PROVINCE
lines assigning it here). The only sibling activity is citation/reading (items 1–3), which is the
declared "reported out, not absorbed" pattern. One presentational caveat: `PROVINCE.md`'s
`## Surfaces` table names external surfaces, not instruments, so the ledger/battery/probe are
correctly absent from it; `SKILL.md`'s gate registry is the right index for them.

---

## (b) Absolute totals vs member sets; standing batteries; bite/grow legs

### The 14-counter population and what each L7 pinned at BASE

| counter | L7 at BASE | BASE verdict (P0 `ff6765a6`) | round-96 repair |
|---|---|---|---|
| r79 population gate | derives `k` from the ledger; SKILL cell compared to derived `k` (`plans/round79_c1_population_ledger.py:337-360`) | **red**: `SUBJECT-MISMATCH mteb-retrieve ledger=tb2-result-file receipt=tb2-header` | ledger row subject re-pinned (r87) |
| r83, r84, r85, r86, r88, r89 | no absolute executed total; per-member legs | green | none |
| r87 | exact row tuple incl. `LEDGER_SUBJECT` (`plans/round87_c1_replay.py:48`) | green at BASE (r79 was the red one) | `LEDGER_SUBJECT` `tb2-result-file` → `tb2-header` |
| r90 | `exec_total == 34` + exact cells | **red** (`executed=39`) | set ⊇ + cells ≥ |
| r91 | `exec_total == 35` + exact cells | **red** | set ⊇ + cells ≥ |
| r92 | `exec_total == 36` + exact cells | **red** | set ⊇ + cells ≥ |
| r93 | `exec_total == 37` + exact cells | **red** | set ⊇ + cells ≥ |
| r94 | `exec_total == 38` + exact cells | **red** | set ⊇ + cells ≥ |
| r95 | `exec_total == 39` + exact cells | green at BASE; **red at a C1-landed tip** (`c2-c1-only.txt`, red 7) | set ⊇ + cells ≥ |
| r96 (C1) | set-keyed from the start (`plans/round96_c1_replay.py:252`) | n/a | none |

Exact repaired pointers: `plans/round90_c1_replay.py:61,281`; `round91:47,227`;
`round92:46,247`; `round93:55,229-230`; `round94:235`; `round95:243`; `round87:48`.
The old `EXECUTED_AFTER` constants remain in r90–r95 as message/print values only
(`round90:60`, `round91:46`, `round92:45,299`, `round93:54`, `round94:61`, `round95:61`); they no
longer gate a verdict. Receipt: `receipts/b-counter-l7.txt`.

### Battery design and controls

`plans/round96_standing_battery.py`: population 14 (`:41-56`), `BITE_SET` 6 (`:67-75`), forgery
selection (`:187-199`), verdict (`:207-208`), predicate (`:224`). P2 controls, read at
`.ufo/waves/round-96/L1/controls/`:

| control | STANDING | BITES | GROWS | predicate |
|---|---|---|---|---|
| `c2-c1-only` (C1 landed, no repair) | green 7 / red 7 | 0 | 0 | fail |
| `c2-delete-l7` (L7 removed) | green 14 | 0 | 6 | fail |
| `c2-repin-abs` (L7 re-pinned to 40) | green 14 | 12 | 0 | fail |
| `c2-full` (candidate bytes + C1 flip) | green 14 | 12 | 6 | pass |
| `c2-c2-only` (candidate bytes, no C1 flip) | green 14 | 12 | 6 | pass |

The two-sided control is sound: deleting L7 passes grows and fails bites; an absolute re-pin
passes bites and fails grows.

### Findings on the battery

**CO-2 (minor) — the 12 bites and 6 grows are not 12+6 independent forgery inputs.**
`others = sorted(executed with round < rnd)` and `unexecuted = sorted(...)` are recomputed per
counter, but the lexicographic first is the same for all six: `others[0] = build-pmars` (round 38)
for r90–r95, `unexecuted[0] = adaptive-rejection-sampler` for r90–r95. So the 12 bites are 6 own
demotions + 6 copies of the same `build-pmars` demotion, and the 6 grows are 6 copies of one
promotion: **8 distinct forgery inputs, not 18**. The counts are literally true but the
independence they suggest is not. A per-counter `other` (e.g. the lexicographically first member
in that counter's own BASE set, excluding its own member) and a per-counter grow member would make
the count mean what it says. Receipt: `receipts/b-battery-forgery.txt`.

**CO-3 (minor) — the repair removes the last absolute-total cross-check and the compensating
bound is not composed in the battery.** The set-keyed L7 accepts *any* executed superset; the
grow forgery is a ledger-only promotion with a fabricated receipt (`round96-grow-fixture`), and
the six repaired counters accept it by design. The compensating control is r79's per-row
`RECEIPT-UNTRACKED` / `SUBJECT-*` / `VERDICT-*` / `CLASS-K-MISMATCH` validation
(`plans/round79_c1_population_ledger.py:232-253,337-360`), which is in the STANDING population but
is never run against the grow commit. I verified the composition: r79 passes at T
(`DEFECTS n=0`, `replayed=40`, `PREDICATE R79-C1 pass`, rc 0) and **fails** on the same grow
forgery (`DEFECT RECEIPT-UNTRACKED adaptive-rejection-sampler round96-grow-fixture`, plus four
`CLASS-K-MISMATCH` lines, `DEFECTS n=5`, rc 1). Receipts: `receipts/c-r79-at-T.txt`,
`receipts/c-r79-grow-forgery.txt`. The battery's `GROWS` leg measures tolerance without measuring
its bound.

**CO-7 (minor) — the one r91 grow failure at T is a flake the instrument cannot attribute.**
The battery's `bite()` keeps only `rc` and the predicate match and discards the counter's stdout
(`plans/round96_standing_battery.py:204-208`), and `run_counter` deletes the work dir in
`finally` (`:107-117`), so a red grow leg leaves no counter output. I re-ran all six counters at
the same forged commit (ledger-only promotion of `adaptive-rejection-sampler`): **6/6 pass**
(`executed_rows=41`, `defects=0`, rc 0; receipts `c-grow-r90.txt` … `c-grow-r95.txt`), matching
the L1's isolated and 6× parallel diagnostics (`.ufo/waves/round-96/L1/diag-r91-grow/`). That is
13 passes against 1 unattributable failure. The failure is a flake, not a counter defect — but a
standing gate that cannot print why a leg went red is a calibration liability, and this flake is
the reason R96-C2 is reported not met at T.

**CO-6 (major) — the absolute-total-pin class is not fully repaired: r80 and r81 still pin the
r79 gate's executed count, and the battery's `--rev` invocation structurally cannot see them.**
`plans/round80_c1_located_replay.py:335-351` runs the r79 gate in **worktree mode only** and
requires `executed == 24`; `plans/round81_c1_new_members.py:390-414` skips the population leg for
any non-worktree tree and otherwise requires `executed == 26`. At T the r79 gate prints
`executed=40` (`receipts/c-r79-at-T.txt`), so in worktree mode the comparisons are `40 != 24` and
`40 != 26`. Both are SCORECARD-met C1 counters (`SCORECARD.md:3760,3832`, the R80-C1/R81-C1
rows). The round-96
claim's population is explicitly "round 79 + rounds 83–95", so the frozen predicate is unaffected;
but the claim's *class* statement ("the repair = L7 of r90–r95 keyed to …") is incomplete: two
more counters in the population-ledger family carry the same absolute pin, and their legs are
worktree-only, so a
battery that always passes `--rev <sha>` will report them green while the pin is never evaluated.
`[INFERENCE]` whether r80/r81 pass their other legs at T; the population leg's comparison is
arithmetic from the code and the r79 receipt.

### Sibling primitives nearest to this mechanism

| sibling primitive | what it does | classification vs the round-96 battery |
|---|---|---|
| `kumitate-shokunin/scripts/receipt-evidence.mjs:14-24` | REPRODUCTION: re-runs a receipt's recorded argv inside a `git archive` of the judged rev, compares exit + stdout/stderr sha256 | **complement** — proves a receipt reproduces; does not re-run an old counter at a new rev or judge a verdict line |
| `tabi-shokunin/scripts/check-measurement-binding.mjs:3-22` | binds a counted claim to counter bytes sha256, the measured revision and declared inputs; `--at` defaults to the lane tip | **complement, and conflict-by-design with the repair**: applied to r90–r95's original manifests it would flag the round-96 byte change exactly as the freeze gate does. Not run here (kengaku has no tabi-format manifest); `[INFERENCE]` from the gate's stated contract |
| `kama-shokunin/tools/round72-receipt-tip-binding.py:1-14` | every cited receipt must exist at the tip, carry a rev header, be an ancestor, and intervening commits touch only declared paths | **complement** — binds receipts to revisions; does not re-run counters |
| `mori-shokunin/tools/mori-retention-reconcile.py:1-3` | reconciles committed retention accounting against the tree; "agreement never grants clearance" | **complement/adjacent** — ledger-vs-tree reconciliation, not a counter re-run |
| `kotodama-shokunin/tools/check-evidence-coupling.py:1-10` | frozen-expectation evidence coupling for a bounded packet | **adjacent** — same "frozen expectation file" shape, different object |
| tabi round-60 v19 meter (`tabi-shokunin/.ufo/waves/round-60/c1/v19-meter-at-data-r60.json`) | no-regression meter reading **live** sibling heads; killed by sibling movement (`.ufo/l0-questions.md:283`) | **contrast/complement** — kengaku's clone-at-`--rev` design is immune to that failure mode; whether this answers tabi's open L0 question is not this seat's call |
| standing battery re-running other rounds' counters | **0 hits** outside kengaku for `STANDING total=` / `BITES checked=` / `GROWS checked=` / `set_contains_base` | the mechanism is lane-local; no duplicate, no conflict |

Receipt: `receipts/b-sibling-primitives.txt`.

---

## Cross-axis pattern between the two claims

**Coverage growth is the adversarial input to calibration, and the calibration repair removes the
counter that could see growth — while leaving two survivors the standing battery cannot reach.**

1. Every executed member added since round 90 broke every earlier absolute pin: at BASE
   (39 executed) r90–r94 were red against their own 34–38, and r95 was green only because 39 was
   still its own total. C1's +1 (39 → 40) is the next increment; at a C1-landed tip r95 goes red
   too (`c2-c1-only.txt`: red 7). The debt is monotone in coverage.
2. C2's repair converts `exec_total == N` to `rev_set >= base_set | {MEMBER}` and exact cells to
   `>=`. This is growth-tolerant by construction and removal-sensitive (superset), which is the
   right shape for the debt — but it accepts *any* superset, including a ledger-only promotion
   with a fabricated receipt (the grow forgery).
3. The compensating bound exists (r79's per-row receipt/subject/verdict validation) and I verified
   it rejects the same grow commit; the battery never composes the two, so `GROWS 6/6` measures
   tolerance without its bound.
4. Two counters of the same absolute-pin class (r80, r81) survive the repair, and their legs are
   worktree-only, so the battery's `--rev` invocation cannot see them. The "standing" mechanism
   therefore has a mode blind spot exactly where the unrepaired class lives.
5. Contract surface: the seven repaired counters are frozen instruments of rounds 87/90–95, and
   the repair is a post-freeze byte replace. Under those rounds' freeze-integrity gates the change
   is a breach: ExecHarm measured r93/r94/r95 `broken=1`, `PREDICATE freeze-integrity fail`, and
   `round95_c2_counter W4 fail` at T, green at BASE
   (`.ufo/waves/round-96/w1/ExecHarm.md:57-90`; gate contract
   `plans/round94_freeze_integrity.py:1-20`). This is a true positive under each gate's own
   definition, not a false alarm. Under the chosen byte-replace repair, **R96-C2 pass and the
   r93/r94/r95 freeze-integrity pass are mutually exclusive**; an additive supersession (new
   set-keyed counters, old bytes intact) would decouple them. That is a contract-surface
   contradiction to state, not to smooth into the calibration score. Receipt:
   `receipts/c-freeze.txt`.

---

## Proposed move (one, bounded; round 97 — never in-round under the frozen rule)

**Compose the grow forgery with r79: make the standing battery's tolerance two-sided and bounded.**

Add one leg to the round-97 successor of `plans/round96_standing_battery.py`:

- reuse the existing grow commit (ledger-only promotion of `adaptive-rejection-sampler`, receipt
  `round96-grow-fixture`);
- run `plans/round79_c1_population_ledger.py` against that commit;
- require `PREDICATE R79-C1 fail` rc 1 **with** `DEFECT RECEIPT-UNTRACKED <member>` present (an
  attributed failure, not any failure — a `CLASS-K-MISMATCH`-only failure would not count);
- require `PREDICATE R79-C1 pass` rc 0 at the unmodified measured tip (the control).

This is a synthesis of the round's two mechanisms: C1's receipt discipline supplies the bound,
C2's forgery harness supplies the input, and r79 supplies the judge. Neither claim has the
composition alone.

**Affected axes.** Calibration: improved — the set-keyed tolerance stops being an unbounded
promise and becomes a measured, attributed property. Coverage: unchanged — C1's growth is
receipt-backed and r79 is green at T. Contract: unchanged — this move does not address CO-4/CO-6;
those need their own round-97 decisions.

**Risks.**
- r79's receipt checks are shape-based: a copied receipt with a rewritten header and a matching
  observation line passes. The leg proves *unreceipted* growth is caught, not *fabricated* growth.
- The grow commit must stay ledger-only; adding a receipt to it changes the leg's meaning.
- Adding the leg changes `GROWS` from a one-sided tolerance count to a two-sided count — that is a
  predicate change for the round-97 claim, not an amendment of round 96's frozen text.
- The leg needs its own freeze, do-nothing control (must pass at T) and forgery control (must fail
  with the named defect), plus a stated limit for the shape-based receipt check.
- It does not repair r80/r81 (CO-6) or the freeze contradiction (CO-4); those are separate.

**Verification (already run at T; receipts in this seat's wave dir).**

```sh
# control: unmodified T
cd <clone at T> && python3 plans/round79_c1_population_ledger.py \
  --lane <clone> --rev 09717e49ff46fad5b255619d671aaaae52dfc180 --work <scratch> --quiet
# observed: DEFECTS n=0 / TARGET ... replayed=40 ... / PREDICATE R79-C1 pass / rc 0
#   receipts/c-r79-at-T.txt

# forgery: ledger-only promotion of adaptive-rejection-sampler (same shape as the battery's grow)
cd <clone at forged sha> && python3 plans/round79_c1_population_ledger.py \
  --lane <clone> --rev <forged> --work <scratch> --quiet
# observed: DEFECT RECEIPT-UNTRACKED adaptive-rejection-sampler round96-grow-fixture
#           DEFECT CLASS-K-MISMATCH x4
#           DEFECTS n=5 / PREDICATE R79-C1 fail / rc 1
#   receipts/c-r79-grow-forgery.txt
```

---

## Findings

- **CO-1 (info)** — No sibling lane replays TB2 graders or touches `multi-source-data-merger`;
  0 token hits, 31/31 `tb2-*` entries in kengaku, four sibling PROVINCE lines assign the ground
  here. PROVINCE holds. Sibling activity is citation/reading only (complement).
- **CO-2 (minor)** — the battery's 12 bites / 6 grows use 8 distinct forgery inputs
  (`build-pmars` ×6, `adaptive-rejection-sampler` ×6); the counts overstate independence.
  `plans/round96_standing_battery.py:187-199`.
- **CO-3 (minor)** — the set-keyed repair removes the last absolute-total cross-check; the
  compensating r79 bound is not composed in the battery. Verified: r79 pass at T, fail on the
  grow forgery.
- **CO-4 (major)** — the seven repaired counters are post-freeze edits to rounds 87/90–95
  instruments; r93/r94/r95 freeze-integrity gates flip PASS→FAIL at T (ExecHarm). Under the
  byte-replace repair, R96-C2 pass and those gates' pass are mutually exclusive; a true positive
  under each gate's definition, a contract-surface contradiction for the lane.
- **CO-5 (info)** — fleet-root `.pytest_cache/v/cache/nodeids` (mtime 2026-11-05T23:15:12) names
  the three round-96 grader test functions; a same-round pytest invocation used the fleet root as
  its rootdir (cwd not established). Untracked, no git state change; scratch-discipline
  observation only.
- **CO-6 (major)** — r80 (`plans/round80_c1_located_replay.py:335-351`, `executed == 24`) and r81
  (`plans/round81_c1_new_members.py:390-414`, `executed == 26`) still pin the r79 gate's absolute
  executed count, worktree-only; at T the gate prints 40. The round-96 population excludes them,
  so the frozen predicate is unaffected, but the absolute-pin class is not fully repaired and the
  battery's `--rev` invocation cannot see them.
- **CO-7 (minor)** — the battery discards a failed grow leg's counter output
  (`plans/round96_standing_battery.py:204-208`, `run_counter` `finally` at `:107-117`), so the one
  r91 grow failure at T is unattributable. I re-ran all six counters at the same forged commit:
  6/6 pass (receipts `c-grow-r90.txt` … `c-grow-r95.txt`), 13 passes against 1 failure including
  the L1 diagnostics. Flake, not a counter defect; the instrument's diagnostic gap is the finding.

## Receipts

`receipts/a-sibling-tokens.txt`, `a-tb2-ownership.txt`, `a-capture-parity.txt`,
`b-counter-l7.txt`, `b-battery-forgery.txt`, `b-sibling-primitives.txt`, `c-freeze.txt`,
`c-r79-at-T.txt`, `c-r79-grow-forgery.txt`, `c-grow-r{90..95}.txt`.

## Tool installs

None.
