# F40RevLesson — review of `corpus/lessons/round-40.md` (kengaku round 40, wave 2 falsify, 2026-10-26)

Seat: F40RevLesson (reviewer, leaf). Target: every Gate row's evidence (access dates, quotes, digests), all four Mistakes
rows (class, pointer, captured-by, fix able to fail or honestly not), census numbers, routed R1–R5 vs
`corpus/lessons/round-39-verifier-spotcheck.md` §5. Measured at lane tip `ec1005a2a28bc5cfdde7723374368ed4cc956eed`.

Method: read-only. No clone, no scratch (repo state via `git -C <lane> show/log/diff/ls-tree` at `d3a6277f`/`ec1005a2`;
live re-opens via `curl` to the pinned URLs and `api.github.com`). No C1 counter, battery module or attack module was
executed, so the bwrap host-safety rule was not triggered. No lane file written except this report and
`.ufo/waves/round-40/falsify/F40RevLesson/receipts.md`. Verbatim evidence for every claim below: receipts.md R1–R9.

## Findings (by severity)

### Medium

**M-a. Routed R4 silently drops three of the six residuals the round-39 closure named.**
`round-39-verifier-spotcheck.md:136` lists six carried residuals: F39OrderGateMut ("`order_check.py` 2/6 mutants and the
fail-open mid-scan git error"), F39CritQ30, F39TipReceipts, F39LedgerTip D1 ("ledger-tip clone-mode rows that cannot
fail"), F39MutDirection ("direction check unable to load the round-39 list"), and the C1 soundness repairs A1/A3/A4/A5.
The round-40 lesson's R4 bullet (`corpus/lessons/round-40.md:59`) dispositions only three (C1 soundness → this C1;
Q30 → `round_close.py`; tip_receipts → landed). The other three have no disposition anywhere in the lesson
(`grep -n 'F39OrderGateMut|F39LedgerTip|F39MutDirection' corpus/lessons/round-40.md` → no match) nor in the frozen
claims' carried list (`plans/round-40-claims.md`, "Routed items carried" names only R1, R2, R3, "R4 (C1 counter
soundness …; the tripwire mutation tests …)", R5). The fail-open mid-scan git error in particular is a behavioural
residual no round-40 instrument prices (the 21 frozen mutants do not include it). Receipts.md R2.
Smallest correction: append to the R4 bullet one disposition per item, e.g. "F39OrderGateMut — the 2/6 author-mutant gap
is subsumed by this C1's order mutants / the fail-open mid-scan git error: not priced, carried; F39LedgerTip D1 —
carried; F39MutDirection — carried" (or each routed to round 41 with a reason).

**M-b. Mistakes row 1's fix miscounts its own receipt: "six" vs killed=7.**
`corpus/lessons/round-40.md:38` (M1 fix): "the same witness step killed the six new mutants it targeted
(`claims/witness-run.txt`)". The cited receipt's summary line is `MUTANTS total=21 killed=7 survived=14 invalid=0
null_detected=0` and the seven killed-by lines are A27, L01, L11, L21, O04, O12, O14 — exactly the seven the lesson's own
Controls paragraph and the frozen claims ("7 by this freeze's witness run") name. `R40LessonDraft` contains neither
"six" nor "seven", so the error entered at integration. Receipts.md R1.
Smallest correction: "six" → "seven".

### Minor

**m-c. M2's fix over-attributes the `--work` precondition to the `round39-c2` row.**
`corpus/lessons/round-40.md:39` fix: "the SKILL registry rows for `round39-c2`, `round40-c2`, `round39-c1-audit` and the
`git-leak-probe` addendum now declare "`--work` must already exist"". In SKILL.md only the `round39-c1-audit` (:591) and
`round40-c2` (:593) rows declare it (`grep -n 'must already exist' SKILL.md` → 591, 593); the `round39-c2` row's entry
cell reads just "(`--work DIR`)". The Round-40 registry addendum (:625–631) does declare it for git-leak-probe and "The
same precondition holds for `round39-c2`, `round40-c2` and `round39-c1-audit`" — so the substance is recorded, the
attribution is off for one row. Receipts.md R3.
Smallest correction: reword to "the `round40-c2` and `round39-c1-audit` rows declare it inline and the round-40 registry
addendum declares the same for `git-leak-probe`, `round39-c2`, `round40-c2` and `round39-c1-audit`".

**m-d. Header baseline parenthetical mislabels `d3a6277f`.**
`corpus/lessons/round-40.md:3`: "Baseline as read at round start: `d3a6277f…` (the round-39 non-author spot-check)".
`git show --name-only d3a6277f` → the round-36 salvage commit ("round-36: hyaku run-8 orchestrator salvage…"), one file
`.ufo/waves/round-36/falsify.ready.dispatched`. The spot-check report itself landed at `d8fad16`
(2026-10-26T05:27:44-03:00) and measured tip `9d3aff94`. If the intended reading is "the tip whose newest closure
artifact is the spot-check", it should say so; as written it identifies the commit. Receipts.md R4.
Smallest correction: "(the tip whose newest closure artifact is the round-39 non-author spot-check, `d8fad16`)".

**m-e. Routed R5's pointer dangles as committed.**
`corpus/lessons/round-40.md:62`: "this round's leftovers are listed in the report". At the tip there is no
`.ufo/reports/round-40/` (`ls` → No such file or directory) and `.ufo/waves/round-40/integrate/` carries no leftovers
receipt (c1-determinism, census-after, fleet-untracked-before, measure-baseline, measure-final, measure.sh,
witness-prefreeze-with-o13 only). Receipts.md R5.
Smallest correction: name the intended path (the L1 round report, to be filed) or inline the leftover list.

## Checked clean

**Gate rows.** S119: live digest `88dc5c2a…` = capture = SHA256SUMS (8/8 OK), line 98 quote verbatim (12 words), and the
"(= the round-39 planning seat's pin read)" resolves at `.ufo/waves/round-39/build/R39PlanNext.md:169`. S120: live digest
`5a203751…`, line 7 quote verbatim (9 words). Captured-files row: the captures dir is exactly the 8 named files.
S121: live API `state=open merged=false created=2026-05-21T21:43:34Z` matches the meta capture (4/4 SHA256SUMS OK); body
§Reasoning carries the 21-word quote verbatim; the SOURCES row self-stamps the 14:04 re-open; the entry cites it from
§Prior art only (:294, :325). SQLite row: the cleanup sentence is verbatim in the live wal.html (split across source
lines 479–480). #2218/#3607: quotes verbatim/consistent in the scout captures. JonathanGabor `audit.txt:782` @
`35f11039`: live line contains "Not all values are verified". Merge re-screen: 113/175/37, scratch-collisions nonempty,
verdicts 2 ADMIT-candidate / 42 HOLD / 21 REFUSE, quarantine slice S091+S105, word-bounded grep receipt present,
`git -C shokuknow log -1 -- merge/kengaku` → ba6779f0 2026-10-24 (pre-round-38). considerthese proposal 3 quote verbatim
(lane `considerthese/2026-10-26.md:54-56`); the stability measurement receipt matches (15/15 `regrade=same`; two of five
graders mutate). SOURCES curation: exactly 2 `rechecked 2026-10-26` notes landed (S046, S052, the seat's drafted text);
S005/S027 re-opened unchanged; overdue zero per the seat receipt. Access dates 13:05/14:04 are consistent with commit
windows (see gaps).

**Mistakes rows.** M1 pointers resolve: `R39PlanNext.md:126` lists O13 as reachable; `witness-prefreeze-with-o13.txt`
shows `O13 … SURVIVED exhibits=none`; the draft reproduced both runs `ORDER RESULT PASS`; the counter docstring records
O13 "EQUIVALENT, not reachable … listed as a limit and not frozen"; the D10 calibration ("argued by code reading") is
carried into the fix (count error = M-b). M2: pointer `plans/round40_c2_verify.py:266` is the `TemporaryDirectory(dir=
a.work)` line; the draft measured the crash (FileNotFoundError, rc=1); the fix honestly says "not fixed (the counter is
frozen)" and the registry rows for the tools that do create `--work` say "created if absent". M3: captured-by resolves
(`.ufo/waves/round-39/falsify/F39TipReceipts.md`); red-before `skip … compared=0` and green-after `equal` +
`--tamper → differ` receipts exist (out-red-only-round39/40, out-green-only-round39/40, out-green-tamper-round39/40) —
shown able to fail. M4: the committed `control-c1-tool-edited.txt` carries the observed `exit=1` and no "appended by"
line survives — consistent with the re-run story.

**Census.** Registry rows 111 → 114 (`grep -cE '^ {0,3}\|\s*S[0-9]{3,}\s*\|'` on `git show` at the two commits);
knowledge files 46 → 47 (ls-tree count); README index rows 46 → 47 (`grep -cE '^\| `knowledge/'` on corpus/README.md);
the SOURCES diff touches only S046/S052 (note appends) and adds S119/S120/S121, each `mined` / opened `2026-10-26` /
`180d`; census-before.txt and census-after.txt both show 15 `W04` + `kengaku ok` + `exit=0`.

**Routed R1–R5.** R1 landed (order-check and round39-c1-audit rows at SKILL.md:590-591). R2 honestly "declared, not
fixed": `git_leak_probe.py` diff empty baseline→tip; the addendum declares the precondition and its pin rationale.
R3 honestly blocked: `corpus/defects.jsonl` unchanged; `ledger_tip.py` imports clone tip bytes as-is; battery40 ledger
fixtures declare the `NO:` sets (l_rows.py:52-58). R4: C1 = this counter (21 mutants); `round_close.py` red-38 /
green-39 / green-40 receipts (R40CloseCheck.md:89,103,117; measure-final.txt) — coverage gap = M-a. R5 — pointer gap =
m-e.

**Header controls / order / first run.** All six controls match the quoted values exactly (21/0 survived; mismatched=1
with 11 anchor `invalid`; hostile-daemon `tampered=0` + `COUNTERFACTUAL … changed after 6 s = True`; witness-run 7/14
split; C2 do-nothing defects=4 V2 V3 V4 V7 with `P10 … receipt unreadable`; stage-check `cases=28 failed=0`).
`measure-baseline.txt` carries the round-40 `ORDER RESULT PASS` / `exit=0`. Freeze `bbb1095` (13:21:59) is the parent of
first-run `055748f` (13:22:18; file-stamped run 13:22:17, `run2` byte-equal, `regrade cases=28 differ=0`, `cases=28
observed_pass=8 observed_fail=20 mismatches=0`); `sha256sum` of `corpus/evidence/round40/db-wal-probe.txt` =
`c74c6b91…` as recorded. Dry table `cases=28 predicted_pass=8 predicted_fail=20`.

## Residual risks / verification gaps

- Wall-clock access times (13:05, 13:20, 14:04 -03) are L1-asserted; no independent clock receipts exist in the repo.
  Commit windows bracket them (captures/controls committed 13:21:59; receipt commit 13:22:18; the S121 row self-stamps
  14:04), so they are consistent, not independently proven.
- The frozen predicates were measured at `ec172168` (measure-final.txt `TIP ec172168…`), one commit before the lesson
  tip; `git diff --stat ec172168 ec1005a2` touches only SCORECARD.md (+50) and this lesson (+89), neither read by
  C1/C2/census, so the measurement transfers nominally — the spot-check's item 1 (re-run at the tip) remains the
  authoritative check.
- I verified at receipt level plus live re-opens; I did not re-execute the counters (host-safety rule; not required for
  a lesson review), and R2's "a one-line edit reds V2 and V5" is taken from the R40RegistryRows receipts, not re-derived.
- m-e may self-resolve when the L1 files `.ufo/reports/round-40/`; as committed at `ec1005a2` the pointer is unresolvable.

Report: .ufo/waves/round-40/falsify/F40RevLesson.md
VERDICT: lesson-review-5-defects
