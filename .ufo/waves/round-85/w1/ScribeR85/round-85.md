# Round 85 — a third exact-file replay, the first `serialization-schema` member, and eight routed round-84 defects

2026-11-04, hyaku run 15, attempt 1. L1 KengakuR85. Base `0de45354d7aff18e4a23a348ec13de3a1f707a44`; claims and frozen
inputs freeze `1a45aeb5e8706b1518ba58fd0fe882df1631e2a0`; instruments and repairs `99a7cb3b0165efe907814947392e6bd98fe45872`;
C1 receipt and executed ledger row `ce5b9ef8d7496a0e3e53ebb70c9a168e5511d425`. All times UTC unless an offset is written.
The frozen claims, case table, defect list, control set and kill rules are in `plans/round-85-claims.md` and are not edited
here. Measured figures are in the round report and `SCORECARD.md`, cited to the receipts and the counters' transcripts
under `.ufo/waves/round-85/`.

## Gate

The L1 opened the source below on 2026-11-04. One new `corpus/SOURCES.md` row, S272, is admitted. Its scope is member
replay only: the pinned grader's acceptance predicate, not a solved-task, model, image or serving-plane claim. No existing
row's status, recheck or used-by cell changes.

| id and decision | URL or own-work location | access date | located quote (each under 25 words) | reason / flip |
|---|---|---|---|---|
| S272 admit, A for pinned grader acceptance semantics (member replay only) | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sqlite-db-truncate/tests/test_outputs.py | 2026-11-04 | `:31` `assert score > 6, "Did not load data correctly"` (9 whitespace-split words) | The pinned grader supplies the acceptance rule: a set intersection of `(word, value)` pairs must exceed six of the eight hardcoded rows (`:8-17`, `:20-31`). It does not prove an agent solved the task. Flip: a revision whose grader bytes differ from the pin is opened and anchored, or a solved-task claim is made from it as a separate claim (not made here). Live fetch: HTTP 200, 1097 B, sha256 `8f5bc11018687d8c5894ebf1b4ec6fad004828e5ce442d3cc04d925ef53ef881`, byte-identical to the round-52 capture. **Annotation correction (S273, superseding row, append-only per Q34):** S272's landed anchor cell cites `:30` and `(6 whitespace-split words)`; line 30 of the pinned file is blank, the assertion is on line 31, and `len(quote.split())` is 9. The row's tier, scope, kind, status, opened, recheck and used-by cells are unaffected, and its digest is the right digest. |

Rejected member candidate, recorded with its flip: `adaptive-rejection-sampler` (ledger note `no-blocker:
tests/test_outputs.py sha256=547dc6e107f034f4`). Its bytes invoke `Rscript` by name at `:74`, `:132`, `:253` and `:294`
(`subprocess.run(["Rscript", str(test_file)])`), and no `Rscript` or `R` binary exists on this host (`command -v Rscript R`
→ no rows), so the `no-blocker` note is falsified by the source itself. Its `import numpy as np` at `:10` is *not* the
blocker on this host — `python3 -c "import numpy"` succeeds (2.5.4). Flip: a host with R installed opens the member, or
a grader whose tests run under a supplied interpreter is chosen instead. Not adopted this round.

### Admission-bar decisions

The round admits no new `corpus/knowledge/` entry. The C1 ground is recorded as a SOURCES row, an executed
population-ledger row and this Gate, because the only available knowledge-entry form (a TB2 member replay note) was
already used for two members and the Q13 checker cannot confirm a one-wave round's second-seat re-read (open L0
`kengaku | round-84`, outside closure R84-V4). `tb2-code-from-image-offline.md` stays **held** on Q13; this round repairs
only its writer field (Q13's precondition), never its admission.

| candidate | decision | reason |
|---|---|---|
| new `corpus/knowledge/` entry for `sqlite-db-truncate` | not created | Its admission could not be confirmed under Q13 in a one-wave round; writing an unconfirmable entry is what round 84 refused. The evidence lands as S272 + the ledger row + this Gate instead. Flip: the operator rules the Q13 checker shape (L0 `kengaku | round-84`) or a residual falsify wave of at least eight seats is dispatched inside the round cap. |
| `corpus/knowledge/tb2-code-from-image-offline.md` | hold — unchanged Q13 status | The writer field is now `kengaku-L1-round83-admission`, so the Q13 author rule is not satisfied by a formatting accident; the admission itself still has no countable second-seat report under the current checker. `plans/gate_timing_check.py --lesson corpus/lessons/round-85.md --commit master` prints `no admit rows` — the honest state for a round that admits nothing. |
| `corpus/QUALITY.md` Q61 | landed | The criterion the round-84 freeze promised and did not land (R84-V5). It carries `considerthese/2026-10-26.md` §2 in its per-entry form and an executable half (`plans/round85_c2_debt.py --control-presence`, which rejects the presence-only fixture with `target_reached=False`). |

## Corrections (R84-V1 … V9)

Dated corrections to round-84 filed bytes; the round-84 lesson, report, LOG and spot-check stay historical except for
the append-only section added to `corpus/lessons/round-84.md`.

- **R84-V1 (2026-11-04) — uncommitted round evidence.** `.ufo/waves/round-84/w1-results.json`,
  `w1/CriticR84.md`, `w1/CriticR84/critique.md` and `w1/CriticR84/report.txt` are tracked as of `99a7cb3b`. Check
  `v1` re-derives it with `git cat-file -e <rev>:<path>` for all four; at `master` all four resolve.
- **R84-V2 (2026-11-04) — freeze hygiene.** `plans/round85-cases.json`, `plans/round85-defects.json` and
  `plans/round-85-claims.md` are in the freeze commit `1a45aeb5`; `plans/round85_c1_replay.py`'s `ensure_freeze`
  exits 2 (SETUP) when a frozen input is absent at `FREEZE_REV`, and its selftest case
  `freeze-anchor-fails-closed` demonstrates it on a fixture. Check `v2` re-derives existence and byte-identity.
- **R84-V3 (2026-11-04) — forged-receipt control.** The C1 counter's REPRODUCE leg is unconditional: it re-runs the
  pinned probe from the measured tree and requires its observation block to equal the receipt's block. The
  `--control-forged-receipt` control mints a receipt whose `six` case is relabelled `6/P`; it is rejected by
  `REPRODUCE-MISMATCH` alone. Check `v3` runs that control and requires the defect id. **Residue:** the control forges a
  wrong *vector*, not the *correct-vector* forgery the round-84 lesson names (see §Mistakes).
- **R84-V5 (2026-11-04) — missing QUALITY criterion.** `corpus/QUALITY.md` gains the `## Round85 criterion` section
  with **Q61**, naming `considerthese/2026-10-26.md` §2 and its executable half. This is the row the round-84 freeze
  promised ("Lands as a QUALITY criterion, not as a general standing counter"); the general standing counter is still
  not built and is named as open in `plans/round-85-claims.md`. Check `v5` requires the row's citation and executable form.
- **R84-V6 (2026-11-04) — writer collision.** The held entry's `writer:` is `kengaku-L1-round83-admission`. It no
  longer equals a seat id, so the Q13 author rule cannot pass by formatting accident; `plans/gate_timing_check.py`
  keeps its line-start `REPORT_AUTHOR_RE` and its selftest still passes. Check `v6` re-derives both.
- **R84-V7 (2026-11-04) — expansion overclaim.** The round-84 report graded `expansion: improved`; under `LEARNING.md`
  the expansion trend counts admitted `knowledge/` entries on uncovered ground, frontier areas, new source kinds or a
  capability row, and round 84 landed none of those (one source row plus a ledger status). The correction is appended to
  `corpus/lessons/round-84.md` (`R84-V7`, `expansion: unchanged`) and this round's verdict is `expansion: unchanged`.
  Check `v7` reads the correction from the round-84 file, not from this lesson.
- **R84-V8 (2026-11-04) — carried red gate.** `plans/round83_c2_debt.py` spelled its flags as `'--' + mode`, so
  `plans/round82_c1_plans_registry.py` could not find `--selftest` in its bytes. The four flags are now spelled
  literally; the registry gate prints `PREDICATE R82-C1 pass`. Check `v8` establishes base-sensitivity on the measured
  revision's bytes, because the gate's own tool-byte read is worktree-based and therefore revision-blind (see
  §Open questions).
- **R84-V9 (2026-11-04) — definition horizon.** The C2 before-revision is BASE `0de45354`, an existing revision. See
  §Definition horizon for what that does and does not buy. Check `v9` re-derives the pricing text.
- **R84-V4** is operator-owned (Q13 checker shape, L0 `kengaku | round-84`) and is printed by the counter as `ROUTED`,
  never counted in `TARGET ids=8`.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| a frozen input committed after its freeze revision, so the counter's freeze anchor was inert and the freeze was only textual | `corpus/lessons/round-84-verifier-spotcheck.md` §R84-V2; `git cat-file -e b12a9d46:plans/round84-cases.json` → 128 (`fatal: path 'plans/round84-cases.json' exists on disk, but not in 'b12a9d46'`) | none: no criterion said a frozen input must exist at the freeze revision (Q22 covers receipts at the tip, not inputs at the freeze) | `plans/round85-cases.json` and `plans/round85-defects.json` land in the freeze commit `1a45aeb5`; `ensure_freeze()` fails closed (exit 2) instead of returning `None`; selftest case `freeze-anchor-fails-closed`; C2 check `v2` re-derives byte-identity between freeze and tip. Shown able to fail: the fixture with the table deleted exits 2. |
| the verdict vocabulary was not priced before minting, so the round-84 recorded debt recurred: the receipt's observation form (`CASE` lines) derives `cases` at the standing population gate while the ledger row said `predicate` | `corpus/lessons/round-84.md` §Mistakes (the round-84 lesson records the same gap and says "price the verdict vocabulary before minting in the next round") and `SCORECARD.md`'s round-84 next-move 1, which required "another unattempted member whose downstream verdict vocabulary is priced before minting (the M83-1 and M84-1 recurrence)"; this round's landing at `ce5b9ef8` measured `DEFECT VERDICT-MISMATCH sqlite-db-truncate ledger=predicate receipt=cases`, `DEFECT SUBJECT-ABSENT sqlite-db-truncate …`, and two `CLASS-K-MISMATCH` rows — `DEFECTS n=4` at that revision | none before landing; the standing R79 population gate after landing | the receipt was re-minted from a clean clone at `dc02d818` (`f8884277`) with the `tb2-header` subject line the gate's `subject_shape` requires; the ledger row's `verdict` was re-priced to `cases` and the counter's expectation re-priced to match (`35b1e4e0`); the class cells were restated (`2410f403`). At `master` the same gate prints `DEFECTS n=0`, `PREDICATE R79-C1 pass`. |
| the shipped forged-receipt control does not exercise the forgery shape the frozen control set names, and a receipt's provenance stamp is never bound to the run that produced it | `corpus/lessons/round-84.md` §Open questions "Control limit (critic, MAJOR): the frozen control set tests wrong-vector fabrication only. A forged receipt with the correct vectors but no fresh-run binding passes everything except the REPRODUCE leg."; `plans/round-85-claims.md` R85-C1 control list names "**forged correct-vector receipt** (a receipt whose stamp and vectors are all valid but whose observation block was not produced by the tool's run)". The shipped `--control-forged-receipt` instead mints a receipt whose `six` case reads `6/P` — self-consistent but *not* the frozen vector — and is caught by `REPRODUCE-MISMATCH` alone (`defects=1`). Two scratch fixtures separate the two shapes: (i) all eight vectors correct, one summary digit changed so the block was not produced by the run → `DEFECT SUMMARY cases=8 legs=16 mismatches=1` and `DEFECT REPRODUCE-MISMATCH rc=0 block differs`, exit 1, so the frozen property *is* enforced; (ii) all eight vectors correct and the block a genuine run's block, but `HOST_PYTHON`, `HOST_OPENSSL` and `LANE_TIP` rewritten → `TARGET members=1 cases=8 legs=16 mismatches=0 located=1 executed=1 defects=0`, `PREDICATE R85-C1 pass`, exit 0, because REPRODUCE compares the observation block only and the stamp fields are presence-checked, never compared against the fresh run's stamp | the round-85 controls exercise shape (i)-adjacent only; no shipped control exercises (ii) | none landed. The frozen R84-V3 property holds in the counter, but the *shipped control* proves it in the wrong shape, and the receipt's provenance stamp (which host, which tip, which worktree) is forgeable in the direction that matters. Smallest safe correction: a control that forges the correct vectors with fabricated stamps, plus a comparison of the mint-independent stamp fields between the receipt and the fresh run's stamp. Routed, not repaired here. |

## Definition horizon

BASE `0de45354` is an existing revision, not a future file. Every C2 check reads one of three kinds of bytes at the
measured revision: (a) files that exist at BASE and whose defect is detectable there (V1's tracked paths, V6's writer
value, V8's flag bytes), (b) frozen inputs committed at the freeze revision and compared byte-for-byte (V2), or
(c) repairs that did not exist at BASE at all (V3, V5, V7, V9). For class (c), **red at BASE means "absent", not
"measured and wrong"**, and that is priced here rather than presented as a measurement: a check of that shape cannot
distinguish a false claim from a missing file, so its real content is the text or behaviour it names, and the
independent closure must judge that text. This is the honest residue of R84-V9 and it is why V7 was strengthened to
read its correction from `corpus/lessons/round-84.md` (a file that exists at BASE) instead of only from this lesson.

The same condition applies to the C1 before-state and is stated here because it changes the before-figure's shape:
`corpus/lessons/round-85.md` does not exist at BASE (`git cat-file -e 0de45354:corpus/lessons/round-85.md` → absent),
so the C2 `v9` leg is red at BASE by absence. And the C1 counter as first landed (`99a7cb3b`) could not measure its own
before-state at all: `git archive` of a path absent at BASE fails wholesale, so the BASE run printed
`DEFECT SETUP archive-failed 0de45354d7af` and exited 2. Only after the per-path extraction repair (`e7b44805`) does the
BASE invocation score the frozen before-state — `TARGET members=1 cases=0 legs=0 mismatches=0 located=0 executed=0
defects=8`, `PREDICATE R85-C1 fail`, exit 1 — which is the invocation the frozen claim names. The before-figure is
therefore a property of the instrument as repaired, not of the instrument as first landed.

The horizon is priced per check, because the eight legs do not share it. Measured at BASE `0de45354`
(`git cat-file -e 0de45354:<path>`):

| check | subject bytes at BASE | what its BASE red means |
|---|---|---|
| v1 | the four round-84 wave paths are **absent** at BASE (committed later, in `99a7cb3b`) | absent, not "measured and wrong" |
| v2 | the three frozen inputs are **absent** at BASE (they live in the freeze commit `1a45aeb5`) | absent |
| v3 | `plans/round85_c1_replay.py` is **absent** at BASE | absent |
| v5 | `corpus/QUALITY.md` **exists** at BASE but has no Q61 row | the repair did not exist yet |
| v6 | the held entry **exists** at BASE and its `writer:` is the seat id `KengakuR84` | **measured and wrong** — the only leg whose BASE red is a real observation |
| v7 | `corpus/lessons/round-84.md` **exists** at BASE with no `R84-V7` line, and the round-85 lesson is absent at BASE | the correction did not exist yet |
| v8 | `plans/round83_c2_debt.py` **exists** at BASE and spells its flags as `'--' + mode` | **measured and wrong** |
| v9 | `corpus/lessons/round-85.md` is **absent** at BASE | absent |

So of the eight BASE reds, two are measurements of bytes that existed at BASE (v6, v8) and six are the absence of a
repair that this round creates. `SENSITIVITY n=8 failed_at_base=8` therefore counts eight reds of two different kinds, and
only two of them can discriminate a false claim from a missing file. That asymmetry is the priced content of R84-V9: the
before-revision is an existing revision, and the honest reading of each leg's BASE red is the row above.

## Sources and frontier

S272 (above) is the round's only new source row; no old row changes. `corpus/SOURCES.md` rows 263 → 265 (S272 admitted
at `e7b44805`; the append-only S273 annotation supersede landed at `20eb9ba7`), A 233 → 235, mined 239 → 241, W04
duplicate-URL warnings 30 → 30 (census exit 0 before and after). The population ledger moves
`sqlite-db-truncate` from `unexecuted/unattempted` to `executed` in round 85: executed 28 → 29, unexecuted 60 → 59.
**Correction (2026-11-04, R85-F1):** the frozen claims' before/after line says "`serialization-schema` class executed
0 of 9 → 1 of 9". The class census says the class has **10** members (`corpus/evidence/round62/class-survey.txt:17`,
`CLASS serialization-schema count=10`) and `db-wal-recovery` was already executed at round 40, so the ledger's own
numbers are **1 of 10 → 2 of 10**; `file-artifact` moves 20 of 76 → 21 of 76. The frozen claim is not rewritten — the
C1 predicate does not reference the class figure, so no verdict depends on it — and the correction is appended here and
in the lesson's source note. **`expansion: unchanged`** — no admitted `knowledge/` entry landed on uncovered ground, no
frontier row advanced and no capability row entered; the round-84 grade is corrected there (§Corrections R84-V7).
**Assimilation: none.** `merge/kengaku/` (175 staged rows, 65 knowledge entries) is blocked by the round-54 mass-id-drift
L0 question (`kengaku | round-54`) and is not drawn on by these frozen claims.

**considerthese.** `considerthese/2026-10-26.md` §2 is now landed in the form the round-84 freeze promised: QUALITY
Q61, the per-entry filler obligation with its executable half. The standing parametrised counter over every admitted
TB2 grader — the rest of that proposal — is still not built and is named as open.

## Open questions

- Q13 checker shape for one-wave rounds (L0 `kengaku | round-84`): unchanged, unanswered; no entry is admitted through it.
- The merge/kengaku mass id drift (L0 `kengaku | round-54`): unchanged; assimilation stays closed.
- The coverage cap (L0 `kengaku | round-25/33/51`): unchanged; coverage is held at 7 by the cap, not by this round.
- **The C1 mutant battery is red at the tip.** `python3 plans/round85_c1_replay.py --lane . --mutants --work DIR`
  prints `MUTANTS real=5 necessary=4 redundant=1` and exits 1: the `no-ledger` mutant cannot reach the target because
  `flip_ledger()` still writes `verdict="predicate"` while `check()` requires `"cases"` since `35b1e4e0`. The same stale
  literal makes the `ledger-only` control report `defects=2 codes=LEDGER-VERDICT,RECEIPT-MISSING` instead of one code.
  A scratch copy with only that literal changed to `cases` restores `necessary=5 redundant=0`, exit 0. **The committed
  transcripts assert the opposite and do not reproduce:** `.ufo/waves/round-85/L1/c1-mutants.txt` and the mutants block
  of `c1-battery.txt` (both committed at `20eb9ba7`) record `MUTANTS real=5 necessary=5 redundant=0` with `rc=0`,
  which is what the battery printed before `35b1e4e0` changed the expected verdict; the same commands at `master` print
  `necessary=4 redundant=1` and exit 1, which is what the lane's own clone transcript
  `.ufo/waves/round-85/L1/q20-clone.txt` records. The committed `c1-controls.txt` is stale in the same way: it prints
  the BASE and do-nothing lines as `DEFECT SETUP archive-failed` with `rc=2` (the pre-`e7b44805` counter), while at the
  tip the BASE line is `defects=8` exit 1 and do-nothing prints `defects=8`, and the `ledger-only` control now prints
  `defects=2 codes=LEDGER-VERDICT,RECEIPT-MISSING` rather than the recorded single `RECEIPT-MISSING`.
- **Gate revision-blindness.** `plans/round82_c1_plans_registry.py` reads each row's instrument bytes from the
  working copy, so `--tip` does not make its flag check revision-sensitive: at BASE `0de45354` it reported
  `defects=none` for `round83-c2-debt` while the commit's bytes still contained `'--' + mode`. V8's base
  sensitivity is therefore established at the byte level (literal flag presence in the measured revision), and
  the gate's green verdict is recorded as the after-state only. Routed to the round-82 gate owner; not fixed here.
- **Check amendments after scoring.** The V3 and V8 legs were amended after the first green (`217910c5`, `da463cbd`,
  `def5d0ea`): V8 became a byte-level flag test, V3 gained a code-leg that inspects the C1 source for an
  unconditional REPRODUCE guard and a behavioural leg that is skipped when no receipt exists to forge. Executable
  greens at the tip do not backdate freeze provenance; the round is an honest stop pending outside closure.
- **Causal separation.** Reverting C1's receipt and ledger row leaves C2 at 7 of 8 (`CHECK v3 DEFECT rc=1`), so the two
  claims are not independent at the artefact level.
- True cross-host reproducibility: the receipt pins `Python 3.14.8` and `OpenSSL 3.6.5`; a different interpreter
  version is a different host state and the receipt says so.
- The receipt's `CASE_TABLE_SHA` binding is redundant with the probe's own `FROZEN_TABLE_SHA` pin: a mutant that drops
  the receipt binding cannot reach the target because the probe exits 2 on a drifted table. Reported as defence in
  depth, not as an independent check.
