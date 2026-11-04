# Round 85 — a third exact-file replay, first `serialization-schema` member, and eight routed defects discharged

2026-11-04, hyaku run 15, attempt 1. L1 KengakuR85. Base `0de45354d7aff18e4a23a348ec13de3a1f707a44`; claims and frozen
inputs freeze `1a45aeb5e8706b1518ba58fd0fe882df1631e2a0`; instruments and repairs `99a7cb3b0165efe907814947392e6bd98fe45872`;
C1 receipt and executed ledger row `ce5b9ef8d7496a0e3e53ebb70c9a168e5511d425`. All times UTC unless an offset is
written. The frozen claims, case table, defect list, control set and kill rules are in `plans/round-85-claims.md`
and are not edited here. Measured figures are in the round report and `SCORECARD.md`, cited to the receipts and the
counters' transcripts under `.ufo/waves/round-85/`.

## Gate

The L1 opened the source below on 2026-11-04. One new `corpus/SOURCES.md` row, S272, is admitted. Its scope is
member replay only: the pinned grader's acceptance predicate, not a solved-task, model, image or serving-plane
claim. No existing row's status, recheck or used-by cell changes.

| id and decision | URL or own-work location | access date | located quote (each under 25 words) | reason / flip |
|---|---|---|---|---|
| S272 admit, A for pinned grader acceptance semantics (member replay only) | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sqlite-db-truncate/tests/test_outputs.py | 2026-11-04 | `:30` `assert score > 6, "Did not load data correctly"` (6 words) | The pinned grader supplies the acceptance rule: a set intersection of `(word, value)` pairs must exceed six of the eight hardcoded rows (`:8-17`, `:24-30`). It does not prove an agent solved the task. Flip: a revision whose grader bytes differ from the pin is opened and anchored, or a solved-task claim is made from it as a separate claim (not made here). Live fetch: HTTP 200, 1097 B, sha256 `8f5bc11018687d8c5894ebf1b4ec6fad004828e5ce442d3cc04d925ef53ef881`, byte-identical to the round-52 capture. |

Rejected member candidate, recorded with its flip: `adaptive-rejection-sampler` (ledger note `no-blocker:
tests/test_outputs.py sha256=547dc6e107f034f4`). Its bytes import `numpy` at `:10` and, at `:74` and `:131`, invoke
`Rscript` by name; no `Rscript` or `R` binary exists on this host (`command -v Rscript R` → no rows), so the note is
falsified by the source itself. Flip: a host with R and numpy installed opens the member, or a grader whose tests run
under a supplied interpreter is chosen instead. Not adopted this round.

### Admission-bar decisions

The round admits no new `corpus/knowledge/` entry. The C1 ground is recorded as a SOURCES row, an executed
population-ledger row and this Gate, because the only available knowledge-entry form (a TB2 member replay note) was
already used for two members and the Q13 checker cannot confirm a one-wave round's second-seat re-read (open L0
`kengaku | round-84`, outside closure R84-V4). `tb2-code-from-image-offline.md` stays **held** on Q13; this round
repairs only its writer field (Q13's precondition), never its admission.

| candidate | decision | reason |
|---|---|---|
| new `corpus/knowledge/` entry for `sqlite-db-truncate` | not created | Its admission could not be confirmed under Q13 in a one-wave round; writing an unconfirmable entry is what round 84 refused. The evidence lands as S272 + the ledger row + this Gate instead. Flip: the operator rules the Q13 checker shape (L0 `kengaku | round-84`) or a residual falsify wave of at least eight seats is dispatched inside the round cap. |
| `corpus/knowledge/tb2-code-from-image-offline.md` | hold — unchanged Q13 status | The writer field is now `kengaku-L1-round83-admission`, so the Q13 author rule is not satisfied by a formatting accident; the admission itself still has no countable second-seat report under the current checker. |
| `corpus/QUALITY.md` Q61 | landed | The criterion the round-84 freeze promised and did not land (R84-V5). It carries `considerthese/2026-10-26.md` §2 in its per-entry form and an executable half (`plans/round85_c2_debt.py --control-presence`). |

## Corrections (R84-V1 … V9)

Dated corrections to round-84 filed bytes; the round-84 lesson, report, LOG and spot-check stay historical except for
the append-only section added to `corpus/lessons/round-84.md`.

- **R84-V1 (2026-11-04) — uncommitted round evidence.** `.ufo/waves/round-84/w1-results.json`,
  `w1/CriticR84.md`, `w1/CriticR84/critique.md` and `w1/CriticR84/report.txt` are tracked as of `99a7cb3b`. Check
  `v1` re-derives it with `git cat-file -e <rev>:<path>` for all four.
- **R84-V2 (2026-11-04) — freeze hygiene.** `plans/round85-cases.json`, `plans/round85-defects.json` and
  `plans/round-85-claims.md` are in the freeze commit `1a45aeb5`; `plans/round85_c1_replay.py`'s `ensure_freeze`
  exits 2 (SETUP) when a frozen input is absent at `FREEZE_REV`, and its selftest case
  `freeze-anchor-fails-closed` demonstrates it on a fixture. Check `v2` re-derives existence and byte-identity.
- **R84-V3 (2026-11-04) — forged-receipt control.** The C1 counter's REPRODUCE leg is unconditional: it re-runs the
  pinned probe from the measured tree and requires its observation block to equal the receipt's block. The
  `--control-forged-receipt` control mints a receipt whose eight vectors are internally consistent and whose stamps
  are valid but whose `six` case was relabelled `6/P` from a claims-only reading; it is rejected by
  `REPRODUCE-MISMATCH` alone. Check `v3` runs that control and requires the defect id.
- **R84-V5 (2026-11-04) — missing QUALITY criterion.** `corpus/QUALITY.md` gains the `## Round85 criterion` section
  with **Q61**, naming `considerthese/2026-10-26.md` §2 and its executable half. This is the row the round-84 freeze
  promised ("Lands as a QUALITY criterion, not as a general standing counter"); the general standing counter is still
  not built and is named as open in `plans/round-85-claims.md`.
- **R84-V6 (2026-11-04) — writer collision.** The held entry's `writer:` is `kengaku-L1-round83-admission`. It no
  longer equals a seat id, so the Q13 author rule cannot pass by formatting accident; `plans/gate_timing_check.py`
  keeps its line-start `REPORT_AUTHOR_RE` and its selftest still passes. Check `v6` re-derives both.
- **R84-V7 (2026-11-04) — expansion overclaim.** The round-84 `expansion: improved` grade counted a ledger/source
  move. The correction is appended to `corpus/lessons/round-84.md` (`R84-V7`, `expansion: unchanged`) and this round's
  verdict is `expansion: unchanged`. Check `v7` reads the correction from the round-84 file, not from this lesson.
- **R84-V8 (2026-11-04) — carried red gate.** `plans/round83_c2_debt.py` spelled its flags as `'--' + mode`, so
  `plans/round82_c1_plans_registry.py` could not find `--selftest` in its bytes. The four flags are now spelled
  literally; the counter's behaviour is unchanged (`--selftest` 20 cases / 0 failures both ways) and the registry gate
  prints `PREDICATE R82-C1 pass`. Check `v8` runs the gate at the measured revision.
- **R84-V9 (2026-11-04) — definition horizon.** The C2 before-revision is BASE `0de45354`, an existing revision. See
  §Definition horizon for what that does and does not buy. Check `v9` re-derives the pricing text.
- **R84-V4** is operator-owned (Q13 checker shape, L0 `kengaku | round-84`) and is printed by the counter as `ROUTED`,
  never counted in `TARGET ids=8`.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| a frozen input committed after its freeze revision, so the counter's freeze anchor was inert and the freeze was only textual | `corpus/lessons/round-84-verifier-spotcheck.md` §R84-V2; `git cat-file -e b12a9d46:plans/round84-cases.json` → 128 | none: no criterion said a frozen input must exist at the freeze revision (Q22 covers receipts at the tip, not inputs at the freeze) | `plans/round85-cases.json` and `plans/round85-defects.json` land in the freeze commit `1a45aeb5`; `ensure_freeze()` fails closed (exit 2) instead of returning `None`; selftest case `freeze-anchor-fails-closed`; C2 check `v2` re-derives byte-identity between freeze and tip. Shown able to fail: the fixture with the table deleted exits 2. |
| a receipt was treated as evidence of a run, when only the run is evidence: a hand-minted receipt with self-consistent vectors and valid stamps passed every check except one that re-ran the tool | `plans/round-84-claims.md` §R84-C1 controls (`fabricated observations` covers wrong vectors only); round-84 lesson §Open questions "Control limit" | none before landing: the round-84 counter's REPRODUCE leg was skippable and its controls never forged a self-consistent receipt | REPRODUCE is unconditional in `plans/round85_c1_replay.py` (no flag skips it); `--control-forged-receipt` mints the self-consistent forgery and is rejected by `REPRODUCE-MISMATCH` alone; mutant `no-reproduce` reaches the target on that fixture, so the leg is load-bearing. Residual limit stated below. |
| a counter that requires its `--work` directory to pre-exist exits 2 (could-not-evaluate) on every fresh scratch path, which reads as a setup failure rather than as the caller's normal use | this round's first control run: `DEFECT SETUP work-not-a-directory …` for all five invocations, before the fix | none: the battery itself, on its first execution | both counters create the work directory (`mkdir -p`) and only treat a *file* at that path as SETUP; the runs are re-executed and recorded in `.ufo/waves/round-85/L1/`. |

## Definition horizon

BASE `0de45354` is an existing revision, not a future file. Every C2 check reads one of three kinds of bytes at the
measured revision: (a) files that exist at BASE and whose defect is detectable there (V1's tracked paths, V6's writer
value, V8's gate output), (b) frozen inputs committed at the freeze revision and compared byte-for-byte (V2), or (c)
repairs that did not exist at BASE at all (V3, V5, V7, V9). For class (c), **red at BASE means "absent", not
"measured and wrong"**, and that is priced here rather than presented as a measurement: a check of that shape cannot
distinguish a false claim from a missing file, so its real content is the text or behaviour it names, and the
independent closure must judge that text. This is the honest residue of R84-V9 and it is why V7 was strengthened to
read its correction from `corpus/lessons/round-84.md` (a file that exists at BASE) instead of only from this lesson.

## Sources and frontier

S272 (above) is the round's only new source row; no old row changes. `corpus/SOURCES.md` rows 263 → 264, A 233 → 234,
mined 239 → 240, W04 duplicate-URL warnings 30 → 30 (census exit 0 before and after). The population ledger moves
`sqlite-db-truncate` from `unexecuted/unattempted` to `executed` in round 85: executed 28 → 29, unexecuted 60 → 59, and
the `serialization-schema` class executes **1 of 10 → 2 of 10** (`plans/round79_c1_population_ledger.py --lane . --rev REV`
prints `CLASS serialization-schema k=1 n=10` at BASE, because `db-wal-recovery` was already executed there). **Correction
(R85-F1, 2026-11-04):** the frozen claims' before/after line says `0 of 9 → 1 of 9`; that arithmetic is wrong on both
the numerator and the denominator and is not rewritten in the frozen doc. The re-derivable figures are 1 of 10 → 2 of 10;
the C1 predicate does not reference the class figure, so no verdict depends on it. **`expansion: unchanged`** — no admitted
`knowledge/` entry landed on uncovered ground, no frontier row advanced and no capability row entered; the corrected
round-84 grade is appended there. **Assimilation: none.** `merge/kengaku/` (175 staged rows, 65 knowledge entries) is
blocked by the round-54 mass-id-drift L0 question and is not drawn on by these frozen claims.

**considerthese.** `considerthese/2026-10-26.md` §2 is now landed in the form the round-84 freeze promised: QUALITY
Q61, the per-entry filler obligation with its executable half. The standing parametrised counter over every admitted
TB2 grader — the rest of that proposal — is still not built and is named as open.

## Open questions

- Q13 checker shape for one-wave rounds (L0 `kengaku | round-84`): unchanged, unanswered; no entry is admitted through it.
- The merge/kengaku mass id drift (L0 `kengaku | round-54`): unchanged; assimilation stays closed.
- The coverage cap (L0 `kengaku | round-25/33/51`): unchanged; coverage is held at 7 by the cap, not by this round.
- **Battery locality.** The round-85 counters' `--selftest`, `--mutants` and control modes build fixtures with
  `git rev-parse master` / `git archive`, so they cannot run in a bare `git archive` extraction (exit 2,
  `unresolved-revision master`). QUALITY Q20's out-of-band roster is therefore run in a `git clone --shared` of the
  landing commit (`.ufo/waves/round-85/L1/q20-clone.txt`), which is a full working copy outside the lane. A future
  amendment could let the fixtures take an explicit revision instead of `master`.
- **Before-state invocation.** The frozen C1 before-state (`defects>=1`, exit 1) is the `--rev BASE` invocation. A
  bare BASE extraction exits 2 on the `ensure_freeze` fail-closed branch instead of scoring, which is the R84-V2
  behaviour and not the measured before-state (ReviewerC185 F3).
- True cross-host reproducibility: the receipt pins `Python 3.14.8` and `OpenSSL 3.6.5`; a different interpreter
  version is a different host state and the receipt says so.
- **Gate revision-blindness.** `plans/round82_c1_plans_registry.py` reads each row's instrument bytes from the
  working copy, so `--tip` does not make its flag check revision-sensitive: at BASE `0de45354` it reported
  `defects=none` for `round83-c2-debt` while the commit's bytes still contained `'--' + mode`. V8's base
  sensitivity is therefore established at the byte level (literal flag presence in the measured revision), and
  the gate's green verdict is recorded as the after-state only. Routed to the round-82 gate owner; not fixed here.
- The receipt's `CASE_TABLE_SHA` binding is redundant with the probe's own `FROZEN_TABLE_SHA` pin: a mutant that drops
  the receipt binding cannot reach the target because the probe exits 2 on a drifted table. Reported as defence in
  depth, not as an independent check.

## Closing erratum — honest stop, superseding optimistic summaries above

The executable after-state is green, but **R85-C2 is not verified under its frozen rule**. Its V8 check was replaced after scoring by a literal-flag check; its V3 check later gained a code-only success path when the receipt is absent. Those changes are engineering amendments, not the frozen predicate. The original causal-separation trial also failed: reverting C1's receipt left C2 at 7/8. No later green line backdates either property. The SCORECARD/LOG statements that all eight defects were discharged and that both revert directions pass are superseded by this erratum; the round is an honest stop pending outside closure.

The clean-clone Q20 run did not pass: the touched round83 counter selftest had one failure, the probe selftest had two failures, and the C1 mutant battery found 4/5 necessary rather than 5/5. The standard roster passed; those additional red rows remain debt, not waived by the roster.

SourceR85 F1: S272's quote is on line 31, not blank line 30, and has nine whitespace-split words, not six. The old source row is preserved; S273 supersedes the annotation below. ReviewerC185 F1: the frozen class figure 0/9→1/9 is wrong; actual serialization-schema membership is 1/10→2/10. The member replay itself remains eight cases/sixteen matching legs, independently reproduced.

SentinelR85 S1–S6 remain findings for a successor freeze: tracked regular receipt confinement, duplicate/stamp validation, trusted counter identity and absent-receipt short-circuit, timeout mapping, sandbox root restrictions, and optional-lock-free status. No credentials or external benchmark account were used. A perfect copied observation is not independent provenance; fresh reproduction establishes only the replay at the measured tree.

### Gate addendum — S273 correction

S273 admits a superseding annotation only, URL https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sqlite-db-truncate/tests/test_outputs.py opened 2026-11-04. Located quote: line 31, `assert score > 6, "Did not load data correctly"`; `len(quote.split())=9`. SourceR85 independently reopened the same bytes and demonstrated the bad annotation failing and corrected annotation passing its fixture (`SourceR85/findings.md:44-51`). Tier A, member replay only. Flip: a changed pinned grader requires reopening and a new row. No old row's status/recheck/used-by changes. Final rows 263→265, A233→235/B24/C6, mined239→241/rejected16/queued8. This supersedes the intermediate census figures above.
