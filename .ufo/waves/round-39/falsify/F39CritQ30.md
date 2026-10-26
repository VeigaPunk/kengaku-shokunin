# F39CritQ30 — QUALITY Q30 attacked (round 39 wave 2, falsify)

Seat: `F39CritQ30`, critic. Target: `corpus/QUALITY.md:520-569` (Q30), measured at lane tip
`a6832f53c1a94bb092a6cfd79fb4e449f2d4054c` on a clean `git clone --no-local` under
`/fast/scratch/hyaku/kengaku-r39/F39CritQ30/lane` (`git rev-parse --show-toplevel` = that path,
`git status --porcelain` = 0 lines). Every command below ran inside that clone; receipts are in
`.ufo/waves/round-39/falsify/F39CritQ30/`.

**Headline.** Every command Q30's Check writes reproduces byte-for-byte, and every factual limit
clause it states is true; what the Limits omit is the invocation gap below. Two defects remain: (1) the criterion's title claims the class is *closed by a
gate*, but nothing invokes the gate and its registry row is missing, so the artifact is a rule with
an executable check, not a gate; (2) Q30's "no `recurrence=2` row" note contradicts the frozen
claims' frontier-step sentence, and no erratum resolves it.

## 1. What reproduces (Q30 `Check`, `corpus/QUALITY.md:542-558`)

Receipt `.ufo/waves/round-39/falsify/F39CritQ30/check-runs.txt`.

| Q30 states | measured | agree |
|---|---|---|
| round 38 → `ORDER HIT .ufo/waves/round-38/claims/control-c2-skip.txt@e0a378539a45:11 kind=gate-p10`, `ORDER RESULT FAIL`, exit 1 | identical, `ORDER FAIL probe-executed-before-receipt hits=1`, `rc=1` | yes |
| round 39 → `ORDER scanned commits=1 file_entries=7 distinct_blobs=7`, `ORDER RESULT PASS`, exit 0 | identical, `rc=0` | yes |
| round 37 → `ORDER HIT .ufo/waves/round-37/claims/control-c2-skip.txt@ca790460e9b7:12`, `ORDER RESULT FAIL`, exit 1 | identical, `rc=1` | yes |
| synthetic: claims+receipt one commit → `ORDER FAIL freeze-contains-receipt`, exit 1 | `ORDER FAIL freeze-contains-receipt e80bd489… already has …`, `ORDER RESULT FAIL`, `rc=1` | yes |
| synthetic: receipt first → `ORDER FAIL freeze-contains-receipt receipt-before-claims`, exit 1 | identical pair of clauses, `rc=1` | yes |
| synthetic: clean freeze-then-receipt → `ORDER RESULT PASS`, exit 0 | `ORDER RESULT PASS`, `rc=0` | yes |

Receipt `.ufo/waves/round-39/falsify/F39CritQ30/synthetic-legs.txt` (three `git init` repos under
`$TMPDIR`, every git call `-C "$D"`, never committed anywhere else).

Other Check sentences, tested rather than read:

- **"reads commits only (working tree and index ignored)"** — appended
  `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt` to the *committed*
  `control-c2-nothing.txt` without committing (`git status --porcelain` → ` M …control-c2-nothing.txt`):
  round-39 still `ORDER RESULT PASS`, `rc=0`. Receipt `invariants.txt`.
- **"exit 2 on setup errors, never a silent pass"** — four legs, all `rc=2`: not-a-git-work-tree,
  `plans/nope.md`, `plans/round-XX-claims.md`, uncommitted `nope.txt`. Receipt `invariants.txt`.
- **Pre-state at creation** — `git cat-file -e 088f7c36:plans/order_check.py` →
  `fatal: path … exists on disk, but not in '088f7c36…'`, `rc=128`; the file has exactly one commit
  (`34158b0`). `grep -c 'order-of-operations' corpus/lessons/round-37.md corpus/lessons/round-38.md`
  → `1` and `2`, exactly as Q30 states.
- **Landed script is the audited draft** — `sha256sum plans/order_check.py` →
  `948d5e1d2b3429d76a598fd11c4b22856d9f43ec093efd2c6aa0025aa0fc6ecc`, matching
  `R39OrderGate.md:28` (`948d5e1d…fc6ecc`).
- **Read-only** — the only git subcommands in the file are `rev-parse`, `log`, `rev-list`, `ls-tree`,
  `cat-file`, `merge-base`; imports are `argparse re subprocess sys pathlib`; no `open(`/write. Holds.
- **"round 39's only `P10` line is the exempt …"** — `git grep -n -E 'P10 (DEFECT|ok)' 088f7c36 --
  .ufo/waves/round-39/claims/ | grep -v FIXTURE` returns exactly
  `control-c2-nothing.txt:11:    gate: P10 DEFECT receipt unreadable`. True; `pkg_gate.py:268-270`
  returns `"receipt unreadable"` before building the probe argv, so the round-39 green is not merely
  excused.

## 2. Defect 1 — "closed by a gate" is unearned: nothing invokes it, and its registry row is missing

**Counterexample.** Round 40 repeats the order-of-operations mistake: a skip control runs
`pkg_gate.py --rerun` at freeze and commits a `P10` line before the receipt. No artifact goes red,
because no artifact runs `plans/order_check.py`. The class is not closed; it is checkable on request.

**Evidence** (receipt `wiring.txt`, `ledger-and-registry.txt`):

- `ls -d .github/workflows` → `No such file or directory`; `ls .git/hooks | grep -v sample | wc -l` → `0`.
- `grep -c order_check grader.py` → `0`; `grep -l order_check plans/*.sh` → none.
- `plans/ledger_tip.py:71-74` `LEDGERS = (("corpus/defects.jsonl", "plans/defect_ledger.py"), ("corpus/defects-round35.jsonl", "plans/round36_c1_verify.py"))`
  — the forever-rerun path re-runs only those two ledgers, and the order class is in neither
  (`grep -c order corpus/defects.jsonl` → `0`).
- The lane's gate registry `SKILL.md:560` `## Gate/probe registry (PROTOCOL §Gate standard)` has
  26 rows (`awk 'NR>560 && NR<610 && /^\| \`/' SKILL.md | wc -l` → `26`) and none is the order gate
  (`… | grep -c order` → `0`, `grep -c order_check SKILL.md` → `0`).
- The wave-1 executor's own integration checklist required the row:
  `R39OrderGate.md:242` "add the `order-check` registry row" and, for the ledger,
  `R39OrderGate.md:246` "Commit `corpus/defects-round39.jsonl` with the row above". Neither landed.
- Q30 has no `Rule:` sentence; the sibling criterion Q29 does — `sed -n '522,569p' | grep -c 'Rule:'`
  → `0` for Q30 versus `QUALITY.md:513` "Rule: a round that freezes a mutant list … runs the check at
  its first battery integration" for Q29. Nothing obliges a future round to run Q30's check.
- Q30's own remedy clause is a non-sequitur: "a gate that only ever runs on the round that introduces
  it proves nothing" (`QUALITY.md:565-566`) — the red pair proves the check *discriminates*, not that
  any later round will run it.
- What the Limits do say is narrower: "the gate detects and does not block" (`QUALITY.md:562-563`).
  That covers non-blocking; it does not disclose unregistered, uninvoked.

**Impacted axes.** calibration (a "closure" claim whose closure artefact is never exercised);
operability (no registry row ⇒ the gate's CLI and 0/1/2 exit contract are not advertised anywhere the
lane reads).

**Smallest safe correction.** Two additive moves, neither touching a scored predicate or a frozen
file:
1. Land the already-drafted row in `SKILL.md` §Gate/probe registry (`R39OrderGate.md:197` carries its
   name, command, 0/1/2 verdict map and scope).
2. Because QUALITY forbids editing criteria in place (`corpus/QUALITY.md:6-7`), append — as a dated
   errata line under Q30 or a superseding Q31 — one `Rule:` sentence: every round runs
   `order_check.py` against its own claims/receipt pair at its first receipt commit, and a third
   recurrence is an honest stop. Drop the "proves nothing → red pair" remedy clause, which asserts a
   consequence the red pair does not have.

## 3. Defect 2 — the `recurrence=2` note is right and the frozen claims' sentence is wrong, unresolved

Q30 (`QUALITY.md:564-565`): "no `recurrence=2` row is written to `corpus/defects.jsonl` (its checker is
the round-35 frozen `plans/defect_ledger.py`, which has no check for this class; routed)".
The frozen claims (`plans/round-39-claims.md:99-102`, freeze `088f7c36`, sha256 `ec8760ea…`): "and the
class recorded with `recurrence=2` in `corpus/defects.jsonl`".

They contradict each other, and the bytes side with Q30 (receipt `q30-text.txt`):

- `wc -l corpus/defects.jsonl` → `5 corpus/defects.jsonl`; `grep -c order corpus/defects.jsonl` → `0`;
  `python3 plans/defect_ledger.py --lane .` → `rows=5 closed=5 observed_pass=5 mismatches=0`,
  `PREDICATE C2 pass` (rows are R34-D1…D5 only).
- `plans/defect_ledger.py:111` pins `CHECKS = {f.__name__: f for f in (r34_d1, r34_d2, r34_d3, r34_d4, r34_d5)}`
  — Q30's "no check for this class" is exact, and `plans/pkg-spec-r35.json` `frozen_instruments` pins
  `plans/defect_ledger.py` at `4e386677…`, so the "round-35 frozen" qualifier is exact too.
- `ls corpus/defects*.jsonl` → only `defects-round35.jsonl`, `defects.jsonl`; `defects-round39.jsonl`
  was not committed despite `R39OrderGate.md:246`.
- The landed SCORECARD agrees with Q30, not with the claims: `SCORECARD.md:1420` "Carried: a separately
  frozen `defect_ledger` check so the order class can enter `corpus/defects.jsonl` with
  `recurrence=2`."
- No erratum exists for the claims sentence: `grep -rn 'recurrence=2'` over the lesson, SCORECARD,
  QUALITY and the claims returns only the four lines above; the round-39 lesson §Errata carries the
  round-35 fixture-bytes correction and the `adv`-cell correction, not this one. R5
  (`corpus/QUALITY.md:167`) requires a dated erratum when later receipts overtake a landed note's
  premise; the premise here is not overtaken by a receipt, it was false from the freeze.

**Impacted axes.** calibration (the round's own self-assessment asserts an unlnded component);
operability (the one mechanism that would re-run this check forever — a ledger row — is the thing
missing).

**Smallest safe correction.** Do not touch the frozen claims (its digest is the round's contract).
Append one dated errata line to `corpus/lessons/round-39.md` §Errata naming
`plans/round-39-claims.md:99-102` and `SCORECARD.md:1420`, and state that the ledger row is the
round-40 carry already recorded there. If instead the row is landed now, R5 still needs the erratum,
because the claims sentence is frozen with the ledger absent.

## 4. Limits audit (which Q30 clauses are honest)

True: commits-only invisibility (worktree edit ignored, §1); "round 38 is red only because its skip
control kept one `P10` line" (`hits=1`); the `receipt unreadable` exemption is textual
(`EXECUTED_EXCUSE = ^receipt unreadable(?:: \S+)?$`) and round 39 itself rides it, which Q30 discloses;
`CASE … observed=` is a line-shape binding; non-blocking (`exit 1`, `pkg_gate.py` untouched);
Q23's limit line is `corpus/QUALITY.md:291` and is quoted, not amended; the ledger row is absent.
Incomplete: the set never says *nothing invokes the gate* and never says it is unregistered (Defect 1);
the "proves nothing → red pair" clause asserts a non-consequence.

## 5. Not tested

- No round-40+ history exists, so "a third recurrence is invisible" is a structural argument from the
  missing invocation paths, not an executed counterexample.
- I did not attempt to make the gate green on a genuinely ordered round with a `CASE … observed=` line
  in a *different* claims round directory (the tool only reads round-N's own dir); that is outside
  Q30's written rule.

## 6. Scratch and tools

Scratch `/fast/scratch/hyaku/kengaku-r39/F39CritQ30` removed after copying the five receipts above;
no tool installed or upgraded in this seat; the lane and its git/jj state were never written.

VERDICT: q30-2-defects
