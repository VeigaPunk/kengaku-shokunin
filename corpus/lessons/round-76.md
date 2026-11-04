# Round 76 — kengaku (2026-11-04 UTC)

Base `fda63968f29f8f58dc2b28831acac879405b8326` (round-75 verifier spot-check). Freeze
`42fad4827797e540c60a00821d3f2f5c18539632`; correction wave A `6977019bdf56a88921e14f728167da8f5726c1fc`.
R76-C1 targets coverage (lowest non-retired axis, L0-capped at 7): every `PROVINCE.md` `## Surfaces`
row resolved live and its dated declaration agreeing with the host. R76-C2 targets calibration (held
at 10, exercised): the round-75 closure's seven routed defects become a burn-down whose discharges
re-derive their values at check time.

## Gate

- **S252 admitted for `git merge-base --is-ancestor` and its three exit states.** URL opened live by
  L1 `KengakuR76` this round: `https://git-scm.com/docs/git-merge-base`. Access date 2026-11-04 UTC.
  Document title `Git - git-merge-base Documentation`. Capture
  `corpus/evidence/round76/sources/git-merge-base.html`, HTTP 200, 41397 bytes, sha256
  `46d106b777754f7ec3072813ace57d2c5385d110181b8db1c56b7136cfb49644`. Located anchor quote, capture
  line 1703, 25 words: **“Check if the first <commit> is an ancestor of the second <commit>, and exit
  with status 0 if true, or with status 1 if not.”** Kind docs, tier A for ancestry tests and their
  exit states. Registry change: absent → S252 `mined`, recheck `on-release`, used-by
  `corpus/lessons/round-76.md, plans/round-76-claims.md`.
- **Reject candidate:** "a commit id in a row's `close` text proves the discharge is on the branch".
  The same page establishes resolution of an object id, and the sentence following the quote —
  "Errors are signaled by a non-zero status that is not 1" — shows exit 1 is a *negative answer*, not
  an error. Flip: a dedicated `close_commit` field, the three-state test, and `CLOSE-NOT-ANCESTOR`
  kept distinct from `CLOSE-UNRESOLVED` (`plans/round76_c2_defect_discharge.py`, leg D6 + ledger leg).
- **Reject candidate:** "a declaration is evidence of resolution" (the round-75 `SourcesHostR75`
  finding, now mechanical). A row that asserts a surface resolves proves nothing about the host; the
  consequence measured this round is `c1-control-declared.txt` — trusting the rows prints
  `disagreements=1` while the live probe answers 000 for `:45669`. Flip: resolve, then compare the
  row's dated marker against the resolved verdict (R76-C1's `AGREE` leg).
- Assimilation: **none**. `/home/vgpnk/Projects/shokuknow/merge/kengaku/` was not adopted this round;
  open L0 `kengaku | round-54` carried.
- `considerthese/2026-10-26.md` proposal 1 ("a routed-findings burn-down, not just a defect ledger")
  is implemented by R76-C2: the ledger gains the seven R75 rows, `close_commit` + `verified_at` are
  required fields, and `plans/round76_c2_defect_discharge.py` re-derives each discharge. It lands as
  QUALITY Q55's sibling rule under `corpus/QUALITY.md` §Round76 and as this lesson's Gate entry. The
  reflection is a pointer, not evidence: the proposal's own claims about `corpus/defects.jsonl` (5
  rows) and `corpus/routed-findings.jsonl` (9 rows, 5 open before this round) were re-read first.
- Knowledge entries: none admitted this round. The four held candidates stay held
  (`instrument-registry-derivation.md`, `registry-argv-and-flag-audit.md`,
  `tb2-hf-model-inference-offline.md`, `tb2-hf-model-inference-provenance.md`).

## Mistakes

| id / class | evidence pointer | captured-by | fix / disposition |
|---|---|---|---|
| M76-1 counter-false-green — the C1 skip-control iterated `enumerate(rows)` over `(line_no, cells)` tuples, so `len(cells) < 3` held for every row, every row was skipped, and the control printed `rows=11 disagreements=0` — a control that asserted nothing while looking green | first `--control-declared` run: `CONTROL rows=11 disagreements=0` / `PREDICATE R76-C1-control pass` on bytes whose row 4 the gate itself flagged | the control's own condition (`disagreements > 0`), which its output contradicted | unpack `(lineno, cells)`; the control now prints `declared=present live=absent 4 http://127.0.0.1:45669`, `disagreements=1`, `target_reached=False` (`corpus/evidence/round76/c1-control-declared.txt`) |
| M76-2 arm-masking — the C1 `stale-text` selftest arm removed the row's `ABSENT` marker while adding the present-tense prose, so the fixture died as `UNDECLARED-ABSENT` and the `STALE-TEXT` branch never executed | first `--selftest`: `SELFTEST FAIL stale-text rc=1 want=1` with `failures=1` | the arm's own expected-line assertion | keep the marker in the fixture (`**ABSENT 2026-10-01**, relocated intact`); arm green, `cases=7 red=6` |
| M76-3 rev-mode ancestry — in worktree mode the C2 reader resolved `worktree^{commit}`, left `tip=unknown`, and every `close_commit` and receipt stamp printed `unresolved`; the clean fixture arm failed with 9 defects | first `--selftest`: `SELFTEST FAIL clean rc=1 want=0 defects=9`, all `CLOSE-UNRESOLVED` | the clean arm of the battery | worktree mode resolves the branch tip and `merge-base --is-ancestor` runs against it; clean arm green, `cases=10 red=9` |
| M76-4 receipt plumbing — `--receipt` was ignored in every battery mode (the early `return` skipped the writer), so selftest/mutant/control receipts were never written although each command printed its lines | `ls corpus/evidence/round76` after the first generation run: only the three before receipts and `sources/`, no battery receipts | the file listing, not the commands' exit codes (all printed rc 0) | a tee that stamps and writes in every mode; all nine receipts exist (`c1-selftest`, `c1-mutants`, `c1-control-declared`, `c2-selftest`, `c2-selftest-git`, `c2-mutants`, `c2-control-status`, both before receipts) |
| M76-5 frozen-count collision — R76-C1's target fixed `SURFACES total=11`, so declaring the new resolver inside the same `## Surfaces` table would have made the frozen target unreachable by the round's own work | `plans/round-76-claims.md` §R76-C1 target line vs the gate's `SURFACES total=`; the declaration went to `PROVINCE.md` §Round 76 instead | the frozen target itself, read before integrating | declare instruments outside a counted table, or count a set the work does not grow; recorded so a future claim either fixes a *set* that excludes its own addition or names the row it adds |

## Census and instrument readings

- `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → rc 0 at round start
  (243 rows, `corpus/evidence/round76/census-before.txt`) and rc 0 at round end (244 rows,
  `census-after.txt`); 25 `W04` duplicate-URL warnings both times (S252 adds a new URL).
- R76-C1 before `SURFACES total=11 present=4 absent=7 prose=0`, `AGREE agree=9 disagree=2`,
  `fail` rc 1 → after `AGREE agree=11 disagree=0`, `pass` rc 0.
- R76-C2 before `SCOPE ids=7 registered=0 closed=0 open=7`, `wrong=14`, `fail` rc 1 → after
  `registered=7 closed=7 discharged=7 legs_passed=7`, `pass` rc 0.
- Inherited drift repaired: the round-75 index gate was red at base with one missing lesson row
  (`corpus/lessons/round-75-verifier-spotcheck.md`); the README row was added and the gate prints
  `PREDICATE R75-C1 pass` (74/74, 124/124, 67/67). The round-74 C1 registry gate was red at base
  (`MISSING 2` — the two round-76 instruments unregistered); registering them turned it green, which
  is what makes the D6 receipt a measurement rather than an assertion.

## Correction (appended, round 76)

**The burn-down was not new.** This lesson's Gate entry says
`considerthese/2026-10-26.md` proposal 1 "is implemented by R76-C2"; seat `ScoutFrontierR76` showed the
proposal was implemented ~35 rounds ago (`plans/routed_open.py`, the `routed-findings-burndown` row at
`SCORECARD.md:1571`, `corpus/QUALITY.md:1129`), and the round-65 lesson already recorded that no
still-unimplemented proposal remained. R76-C2 **extends** it (seven rows with `close_commit`,
`verified_at`, `evidence_path`/`evidence_literal`, and legs that re-read the evidence at the commit
that carries it). No proposal was mined this round. The same scout found the seven rows initially broke
`plans/routed_open.py`'s `source`-line check; the pointers were corrected to the lesson's `## 6` lines
and that gate prints `ROWS total=86 open=31 blocked=1 closed=52 refused=2`, `--selftest 12/12`.
