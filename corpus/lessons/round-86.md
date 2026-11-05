# Kengaku round 86 — one more executed Terminal-Bench 2.0 member, and the lane's last self-assessment mismatch

Round 86 (hyaku run 15, attempt 1), 2026-11-05. L1 `KengakuR86`. Lane `kengaku-shokunin`,
branch `master`. BASE `88651a72ef112ed9f5361e1c8c197babec691f96` (round-85 non-author closure tip);
claims freeze `61b0e074a44259c8c022aa2fda257182a0708346`; instrument bytes
`316811fa604eeef1d157bdbf62b5595891dc015a`. Two claims on two axes: `R86-C1` coverage (one more
executed population member by a located offline replay of a pinned grader over eight frozen
schema-drift cases) and `R86-C2` calibration (the lane's self-assessment mismatch count 1 → 0, with
`SHONEN.md` box 4's `PROVINCE.md:129` pointer re-derived to line 151 from bytes).

## Gate

The L1 opened the source below on 2026-11-04 (`curl`, HTTP 200, 2029 bytes) and byte-compared it
with the round-52 capture before admitting the row; the two files are identical
(`sha256 171fae772ccf262aec8ddac5bd2c6c731eed842421f5d8439a330b158c9f8c13`, `cmp` silent). One new
`corpus/SOURCES.md` row, **S274**, is admitted. Its scope is member replay only: this pinned
grader's acceptance bands and key set, not a solved-task, model, image or serving-plane claim. No
existing row's status, recheck or used-by cell changes.

| id and decision | URL or own-work location | access date | located quote (≤25 words) | reason / flip |
|---|---|---|---|---|
| S274 admit, A for pinned grader acceptance semantics (member replay only) | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/raman-fitting/tests/test_outputs.py | 2026-11-04 | `:36` `assert x0_correct and gamma_correct and A_correct and offset_correct,` (8 words by `len(quote.split())`; the trailing ` (` of line 36 is outside the quote) | The pinned grader supplies the acceptance rule for three tests over one JSON file: existence (`:11`), a G-peak band (`:31-36`: absolute `x0<5`, `gamma<1`; relative `amplitude<0.05`, `offset<0.1`) and a 2D-peak band (`:60-65`: relative `x0<0.05`). A missing key or a string value raises an uncaught `KeyError`/`TypeError` rather than a graded assertion, and extra keys are tolerated — that asymmetry is what the round's eight cases price. It does not prove an agent solved the task. Flip: a revision whose grader bytes differ from the pin is opened and anchored, or a solved-task claim is made from it as a separate claim (not made here). |

Rejected candidate, recorded with its flip: **no member is rejected this round**. The round screens
exactly one member and replays it; the screen is the ledger's `no-blocker: tests/test_outputs.py
sha256=171fae772ccf262a` note, checked against the bytes (stdlib-only imports at `:4-5`, no
subprocess, no service, no GPU). Flip for a future round: a member whose bytes need an interpreter
this host lacks is refused the way `adaptive-rejection-sampler` was refused in round 85.

### Admission-bar decisions

The round admits no new `corpus/knowledge/` entry, for the round-85 reason that is still open: the
only available entry form (a TB2 member replay note) is already carried by earlier members, and the
Q13 checker cannot confirm a one-wave round's second-seat re-read (`plans/gate_timing_check.py`
`is_second_wave` resolves only `falsify/` or `wave2/` paths; open L0 `kengaku | round-84`). The C1
ground lands as S274 + the executed population-ledger row + the receipt + this Gate.

| candidate | decision | reason |
|---|---|---|
| new `corpus/knowledge/` entry for `raman-fitting` | not created | Q13 cannot be confirmed in a one-wave round (L0 `kengaku | round-84`); writing an unconfirmable entry is what round 84 refused. Flip: the operator rules the Q13 checker shape, or a residual falsify wave is dispatched inside the round cap. |
| `corpus/SOURCES.md` S274 | admit | Re-opened and byte-identical to the capture; scope stated; quote located and under 25 words. |
| `corpus/QUALITY.md` Q63, Q64 | admit | The two instrument defects this round found at its own pre-data battery, turned into criteria (below). |
| `merge/kengaku/` package | none | Still blocked by L0 `kengaku | round-54` (mass id drift); nothing read into the lane this round. |
| `considerthese/2026-10-26.md` | none new | Its §2 proposal (a standing TB2 admission counter) is still the open half of Q61's limits section; this round adds no counter for it. |

## Corrections

- **Inherited attempt's receipt (2026-11-04).** The earlier attempt of this round left
  `corpus/evidence/round86/raman-fitting-probe.txt` with `LANE_TIP bfda0472` and `WORKTREE dirty`.
  It is superseded, not edited: the round re-minted the receipt at a clean committed tip after the
  ledger row landed, and the superseded stamp is retained in `.ufo/waves/round-86/L1/` history.
- **Inherited instruments.** `plans/round86_c1_replay.py`, `plans/round86_c2_repin.py`,
  `plans/round86_raman_probe.py` and `plans/round86-cases.json` were inherited from that attempt.
  They were re-verified from their own batteries, two legs were repaired (Mistakes 1–2), and the
  instrument bytes were frozen at `316811fa` *before* any tip run.

- **Box-4 pin provenance (measured 2026-11-05).** The pin was not laundering. `### Adjacent` was
  physically at `PROVINCE.md:129` in the commits that froze it (`8ea41f9e` round 25, `3a2aeb15`
  round 26: `grep -n '^### Adjacent' PROVINCE.md` → `129`), and PROVINCE.md later grew so the token
  slid to 151 by the round-85 tip (`88651a72`: line 129 is a table rule `|---|---|---|`; line 151 is
  the token). The repair moved the pointer **to the token**, not the pin to wherever the pointer
  already was, and `P1-derive` recomputes the line from bytes on every run. The repair itself landed
  in the inherited attempt's commit `0481a6d3`; this round's own work is the counter, the derive leg,
  the four controls and the mutant battery, all committed at `316811fa` before any tip run.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **A self-test can test a tree the counter never reads.** `selftest`'s `freeze-anchor-fails-closed` leg deleted `plans/round86-cases.json` from a local extraction of the freeze revision, but `frozen_table()` reads the table with `git show FREEZE:path` from the *repository*. The leg could not fail for the reason it claimed; it printed `FAIL` only because the freeze placeholder did not resolve yet. | `.ufo/waves/round-86/L1/freeze-battery.txt` first run: `SELFTEST freeze-anchor-fails-closed FAIL`, `cases=10 red=9`; the leg's body in `plans/round86_c1_replay.py` at `316811fa` | the pre-data battery, run before the tip data existed (the run-15 rule that controls precede data) | the leg now names a **resolvable revision that does not carry the table** (`BASE_REV`) and asserts exit 2 + `DEFECT SETUP` + `PREDICATE R86-C1 fail`; green at `316811fa` (`cases=10 red=10`) |
| **A fixture written through a hardlink mutates its source.** `hardlink_copy` + `write_text` truncates the *shared inode*, so the second `derive()` case inherited the first case's edit and the duplicate-token check reported pass on a tree that no longer had a first token. | `.ufo/waves/round-86/L1/freeze-battery.txt` first run: `SELFTEST duplicate-token-fails-closed FAIL`; `hardlink_copy`/`sel-double` in `plans/round86_c2_repin.py` | the same battery; and QUALITY Q20's "run the gate outside the working copy" principle, which should have been read as "a fixture is not the tree" | every fixture edit goes through `rewrite()`, which writes a fresh inode and `os.replace`s it; green at `316811fa` (`cases=4 red=4`) |
| **A mutant whose removed check is not the only guard on its fixture proves nothing.** C2's P2 and P3 legs are re-derived by `state_check.py` inside P4, so no single removal turns the `shonen-stale` or `pin-stale` fixture green. The battery reported `necessary=0`, which reads as "the instrument is weak" when the truth is "these legs are redundant by construction". | `.ufo/waves/round-86/L1/freeze-battery.txt` first run: `MUTANT no-shonen … unmutated_defect=False`; the repaired battery prints `caught_by=P3-pin,P4-state` | §9's "the counter's code and the claim's sentence are the same sentence" — a mutant set that cannot be isolated is evidence about the *legs*, not about the work | each mutant now declares `necessary` or `redundant`, names the leg that still catches it, and a `necessary` one is isolated on an unrelated content-pinned assertion (`SCORECARD.md:162`, `**novelty**`); `MUTANTS real=3 necessary=1 redundant=2`, rc 0 |
| **A known red gate was carried across a round under its own "not caused by this round" label.** Round 85 measured `P3c.box.4.pointer.1` red at BASE and at its own tip and deferred it; nobody re-derived the pointer. | `LOG.md` round-85 gate block (the carried-red bullet); `SCORECARD.md` round-85 *Planned* item 2; round-85 spotcheck's carried-state line | round-85's own outside closure, which named the state red and did not route it | round 86 derives the line and repairs the pointer (R86-V1); BASE `state_check --summary` prints `MISMATCH P3c.box.4.pointer.1`, `mismatch=1` (`.ufo/waves/round-86/L1/base-runs.txt`) |
| **A round's own draft can outrun its bytes.** The report draft's Corrections clause said the inherited receipt had been superseded by a re-mint; at `ab9da0d4` the committed receipt still read `LANE_TIP bfda0472` and `WORKTREE dirty`, because the re-mint must wait for a clean tip and the wave seats keep the tree dirty until they settle. | `corpus/evidence/round86/raman-fitting-probe.txt` stamp lines at `ab9da0d4`; seat `ScribeR86`'s read-only check | the seat's read-only re-read of the delivered bytes — the one check the L1 could not do on itself | the receipt is re-minted **after** the wave settles and the tree is clean, and the tip measurement is the commit that carries it |
| **A quote count can be right and its quote wrong.** S274 was first written with the line-36 text including the trailing ` (` while the cell said "8 words"; `len(quote.split())` on that text is 9. | `corpus/SOURCES.md` S274 (pre-`981d6f19`) against `awk 'NR==36'` of the capture | seat `SourceR86`'s independent count, and `ScribeR86`'s re-count | the committed row quotes the trimmed substring (`…offset_correct,`) and states the counting method; the same class as round 85's S272/S273 correction |
| **A receipt is not admitted on its numbers alone.** The inherited receipt's eight vectors were correct and its `TOOL_SHA` true, yet it named a dirty worktree and a tip that predated the ledger row. | the inherited `raman-fitting-probe.txt` (superseded) and `L3-tip` in `plans/round86_c1_replay.py` | the round-85 outside closure, which rejected a claim whose controls did not bind the frozen bytes | re-mint at a clean committed tip after the ledger row lands, and let `L3` refuse any tip that is not an ancestor of the measured revision |

## Definition horizon

What would make this lesson wrong, and what this round does **not** establish:

- A fourth `test_` function, or a different acceptance band, in a later upstream revision of
  `raman-fitting/tests/test_outputs.py` invalidates S274 and every vector derived from it. The row's
  `recheck: 2027-02-05` is the date, not a mechanism; the mechanism is the pinned sha256.
- The class histogram in `plans/grader-population-ledger.json` is the round-62 16-detector census
  re-priced per member. A seventh `serialization-schema` member executed in a later round changes
  the "3 of 10" cell; nothing in this round freezes that denominator.
- The `E` verdict is an observation of *this* probe harness (`P` returned, `F` graded refusal,
  `E` uncaught error). A grader that catches `KeyError` itself would move a case from `E` to `F`
  with no change to the task's semantics; the eight vectors are statements about the captured bytes
  plus this harness, not about Terminal-Bench's own harness.
- `R86-C2` repairs a self-assessment pointer. It does not establish that the frozen assertion was
  *right* when it was frozen at 129; it establishes that the lane's prose and its own instrument now
  agree with the bytes, and the historical value 129 is retained as `STALE_LINE`.
