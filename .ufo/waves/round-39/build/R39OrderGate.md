# R39OrderGate — the order-of-operations gate (round-39 wave 1, executor)

Seat: `R39OrderGate`. Assignment: round-38 closure R3 (`corpus/lessons/round-38-verifier-spotcheck.md` §5 item 3) +
`considerthese/2026-10-25.md` proposal 2(b) — "blocks pre-registration when a class recurs twice"
(`considerthese/2026-10-25.md:42-44`). Mined mistake the claims file names: "the order-of-operations class recurred
twice (round 37 lesson row 3, round 38 lesson row 2)" (`plans/round-39-claims.md:99`).

**Headline.** `order_check.py` (draft for `plans/order_check.py`) is built, stdlib-only, read-only over git history,
and shows the required states on a clean clone of the lane:

| round | claims | receipt | freeze commit | receipt commit | gate |
|---|---|---|---|---|---|
| 38 | `plans/round-38-claims.md` | `corpus/evidence/round38/build-pmars-probe.txt` | `e0a37853…` | `e95cf550…` | **RED**, exit 1 |
| 37 | `plans/round-37-claims.md` | `corpus/evidence/round37/git-webserver-probe.txt` | `ca790460…` | `5c7b34e9…` | **RED**, exit 1 |
| 39 | `plans/round-39-claims.md` | `corpus/evidence/round39/git-leak-probe.txt` | `088f7c36…` | `6a1eb5e1…` | **GREEN**, exit 0 |

The round-37 receipt is `corpus/evidence/round37/git-webserver-probe.txt` — the only `*probe*` file under
`corpus/evidence/round37/` (`ls` of that dir: `git-webserver-probe.txt`, `git-webserver-dry-cases-freeze.txt`, plus
`anchor-captures/`, `prior-art/`, `tb2-git-webserver/`).

Nineteen controls: 13 repository fixtures and 6 source mutants, 13/13 and 6/6 attributable, rerun byte-equal.
Nothing frozen was edited; no lane file was written.

## 1. Files written (all inside my report dir)

| file | sha256 | role |
|---|---|---|
| `.ufo/waves/round-39/build/R39OrderGate/order_check.py` | `948d5e1d2b34…fc6ecc` | the gate; drop-in for `plans/order_check.py` |
| `…/R39OrderGate/calibrate.py` | `b549460f3988…b6b0939` | 13-fixture + 6-mutant harness |
| `…/R39OrderGate/calibration.txt` | `501b02c0d946…32accb` | primary run |
| `…/R39OrderGate/calibration-rerun.txt` | byte-equal to the above (`cmp` clean) | reproducibility |
| `…/R39OrderGate/real-repos.txt` | — | RED/GREEN receipts, live-lane run, setup refusal, read-only proof |
| `…/R39OrderGate/defects-round39.draft.jsonl` | — | the ledger row draft (§5) |
| `.ufo/waves/round-39/build/R39OrderGate.md` | — | this report |

Scratch was `/fast/scratch/hyaku/kengaku-r39/R39OrderGate` (NVMe, `TMPDIR` exported, removed before finishing).
No file under the lane's `corpus/`, `plans/`, `.ufo/waves/round-39/claims/`, root docs or git index was touched; no
git-mutating command ran anywhere in the lane (`git clone --shared` + read-only `-C` calls in scratch only).

## 2. What the gate decides

CLI: `python3 plans/order_check.py --lane DIR --claims plans/round-NN-claims.md --receipt <path>`. `NN` comes from
the claims file name; the claims directory is derived (`.ufo/waves/round-NN/claims/`), so no second argument can
lie about which round is being policed. Paths are repo-relative and resolve against the lane's toplevel.

It reads commits only (working tree and index are irrelevant), with `rev-parse`, `log --diff-filter=A`, `rev-list`,
`ls-tree`, `cat-file`, `merge-base --is-ancestor`. It never imports or runs the gate, a counter, or the probe.

Three FAIL classes, exit 1:

1. **`probe-executed-before-receipt`** — some blob ever committed under `.ufo/waves/round-NN/claims/` in the history
   reachable from the first commit that adds `<receipt>` carries either
   * a gate `P10` line whose detail is not the non-executing one — `P10 ok …`, `P10 DEFECT fresh probe output is not
     byte-equal …`, `P10 DEFECT fresh probe exit=…` all mean the probe ran; the only excused detail is
     `receipt unreadable` (optionally with `: <path>` appended), which is the branch
     `plans/pkg_gate.py:268-270` returns **before** it touches the probe: `return False, "receipt unreadable"`; or
   * a receipt-shaped `CASE <id> … observed=` line (the probe's own per-case record).
2. **`freeze-contains-receipt`** — the commit that adds the claims file already carries the receipt.
3. **`receipt-before-claims`** — the first commit adding the receipt is an ancestor of the freeze commit
   (pre-registration inverted). Not in the ticket's two clauses; added because it is the same defect class and costs
   four lines. It is the only clause that sees the inversion when the receipt was later deleted from the freeze tree
   (fixture `f5b`).

Exit 2 on setup errors, never a silent pass: not a git work tree, claims or receipt never committed in `HEAD`,
unparseable `round-NN-claims.md` name, path outside the lane. Consequence worth naming: **run at the freeze commit
the gate refuses (2)** — it cannot certify before the receipt exists, and that is the correct shape.

Output grammar (stable, greppable, one fact per line): `ORDER claims=… round=… freeze=…`, `ORDER receipt=…
receipt_commit=… claims_dir=…`, `ORDER scanned commits=… file_entries=… distinct_blobs=…`, one
`ORDER HIT <path>@<commit>:<line> kind=<gate-p10|case-observed> \`<line>\`` per hit, `ORDER FAIL <classes> hits=N`
or `ORDER ok …`, then `ORDER RESULT FAIL|PASS|ERROR`.

## 3. Real-repo evidence (`real-repos.txt`)

Clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"`,
`git -C "$S/lane" rev-parse --show-toplevel` = `$S/lane`, `HEAD 750473847af9c7a461487ba3a589b5519fac5ed8`,
`status --porcelain` empty before and after every run.

Round 38 (RED) — the committed control proves the probe ran at freeze time, which is exactly what
`plans/round-38-claims.md:8-10` discloses ("the gate's P10 executed the frozen probe once inside the scratch clone at
control time"):

```
ORDER claims=plans/round-38-claims.md round=38 freeze=e0a378539a45cc9388c66cfba22f44275131de23
ORDER receipt=corpus/evidence/round38/build-pmars-probe.txt receipt_commit=e95cf5500b6c13305cc41b8532ae07fb2c9dcd7b claims_dir=.ufo/waves/round-38/claims/
ORDER scanned commits=1 file_entries=6 distinct_blobs=6
ORDER HIT .ufo/waves/round-38/claims/control-c2-skip.txt@e0a378539a45:11 kind=gate-p10 `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt`
ORDER FAIL probe-executed-before-receipt hits=1
ORDER RESULT FAIL
exit=1
```

Round 37 (RED, same class one round earlier) — hit at `control-c2-skip.txt@ca790460e9b7:12`, `ORDER FAIL
probe-executed-before-receipt hits=1`, `exit=1`.

Round 39 (GREEN) — the only `P10` line committed under the claims dir is the excused one
(`control-c2-nothing.txt:11` `gate: P10 DEFECT receipt unreadable`, precisely the claims header's claim that with no
receipt on disk "the gate's P10 returns `receipt unreadable` before it executes anything",
`plans/round-39-claims.md:10-11`), and
`scanned commits=1 file_entries=7 distinct_blobs=7` yields no hit:

```
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS
exit=0
```

Also in that receipt: the same three verdicts against the **live lane** (not a clone; untracked wave files present,
`git status --porcelain` non-empty) — `r37 exit=1`, `r38 exit=1`, `r39 exit=0` — so the gate does not need a clean
tree; and at a clone checked out at `e0a3785` (the round-38 freeze) it refuses: `ORDER ERROR receipt not committed in
HEAD: …`, `exit=2`.

## 4. Calibration: 13 fixtures, 6 mutants (`calibration.txt`)

```
FIXTURES total=13 wrong=0
MUTANTS total=6 killed=6 survived=0
SELFTEST cases=13 wrong=0 mutants_wrong=0
```

Each fixture is its own repository under scratch (`git init -q`, every call named `-C "$D"`), with fixed author and
commit timestamps, so two runs are **byte-equal** (`cmp calibration.txt calibration-rerun.txt` clean) — the lane's
receipt practice.

| fixture | shape | expect | observed |
|---|---|---|---|
| `f1-executed-before-receipt` | control with an executing `P10 DEFECT …` at freeze | 1 | 1 |
| `f2-case-observed` | control with a receipt-shaped `CASE … observed=` line | 1 | 1 |
| `f3-clean-passes` | control carries only `P10 DEFECT receipt unreadable` | 0 | 0 |
| `f4-tolerated-detail` | excused detail with a path appended | 0 | 0 |
| `f5-receipt-before-claims` | receipt commit, then freeze commit | 1 | 1 |
| `f5b-receipt-ancestor-of-freeze` | receipt, deleted at the freeze commit, restored later (isolates clause 3) | 1 | 1 |
| `f6-freeze-contains-receipt` | one commit adds claims + receipt | 1 | 1 |
| `f7-control-between-freeze-and-receipt` | offending control committed **after** the freeze, before the receipt | 1 | 1 |
| `f8-control-after-receipt` | offending control committed after the receipt (outside the window) | 0 | 0 |
| `f9-receipt-uncommitted` | receipt never committed | 2 | 2 |
| `f10-not-a-repo` | plain directory | 2 | 2 |
| `f11-bad-claims-name` | `plans/foo.md` | 2 | 2 |
| `f12-other-round-ignored` | offending control under `round-98/claims/` while policing round 99 | 0 | 0 |

Mutants are single exact-string replacements; a mutant is **KILLED** only when the set of fixtures whose verdict
changes is *exactly* the set it must change — a degenerate mutant (syntax error, always exit 2) changes everything
and reads `UNATTRIBUTED`, not a kill:

| mutant | changed | status |
|---|---|---|
| `m1-excuse-removed` | `f3`, `f4`, `f8`, `f12` | KILLED |
| `m2-case-arm-removed` | `f2` | KILLED |
| `m3-freeze-clause-removed` | `f6` | KILLED |
| `m4-order-clause-removed` | `f5b` | KILLED |
| `m5-window-freeze-only` (scan the freeze tree only) | `f7` | KILLED |
| `m6-window-head` (scan to `HEAD`) | `f8` | KILLED |

Two findings came out of building the controls, both kept:
* clause 2 subsumes clause 3 in the plain inversion, so `f5b` was added to make clause 3 load-bearing on its own
  (`m4` survived until it existed) — a clause that no fixture can isolate is dead weight;
* `m1`'s changed set is four fixtures, not one: the excused detail is also what keeps every CLEAN-control window
  (including the after-receipt and other-round windows) green. I first asserted the one-fixture set and the
  attribution check read `UNATTRIBUTED`; the harness was right and the expectation wrong.

## 5. `corpus/defects.jsonl` row draft

Schema read first: `corpus/defects.jsonl` holds five `R34-D*` rows with keys
`id, class, opened_round, source, check, status, closed_round, recurrence_of` (`plans/defect_ledger.py:3-8`, `:111`,
`:119`), and `corpus/defects-round35.jsonl` holds the `R35-D*` rows — the split exists because the round-35 predicate
is frozen at `rows=5 closed=5` (`plans/defect_ledger.py:13`, `:138`). Appending to `corpus/defects.jsonl` would break
that frozen predicate, so the draft row is a one-line file of its own, on the round-35 precedent:

`…/R39OrderGate/defects-round39.draft.jsonl` → proposed `corpus/defects-round39.jsonl`:

```json
{"id": "R39-D1", "class": "order-of-operations", "opened_round": 39, "source": "corpus/lessons/round-38.md:36", "check": "order_check", "status": "open", "closed_round": null, "recurrence_of": "round-37 (corpus/lessons/round-37.md:42): the C2 skip-control's gate P10 executed the frozen probe before the first recorded run; recurred in round 38 (corpus/lessons/round-38.md:36)", "recurrence": 2}
```

Key set = the existing eight plus `recurrence` (checked: `extra=['recurrence']`, `missing=[]`), which is proposal 2's
field list ("id, class, opened_round, closing_commit, recurrence", `considerthese/2026-10-25.md:42`).

* **`recurrence=2` counting rule** (state it with the row so nobody re-derives it): two recorded occurrences in the
  lessons — `corpus/lessons/round-37.md:42` and `corpus/lessons/round-38.md:36`. Round 39 is *not* an occurrence; it
  is the first round the gate reads green. If the L1 reads `recurrence` as "occurrences after the first" the value
  would be 1 — the frozen claims file says `recurrence=2` (`plans/round-39-claims.md:102`), so the row follows the
  claims.
* **`check: "order_check"`** names the gate (the row carries no command; the exit contract is below). `status` stays
  `open` until integration, when the L1 sets `closed_round: 39` and the row is `closed` — with the landing-tip
  receipt `ORDER RESULT PASS exit=0` for round 39 in the same commit.
* **Integration warning (do not wire it as a tip-invariant row).** `plans/defect_ledger.py` and
  `plans/ledger_tip.py` (`LEDGERS`, `plans/ledger_tip.py:61-64`) expect a check that passes at the tip for every
  closed row. This class cannot be tip-invariant: rounds 37 and 38 are red **in history** and cannot be repaired
  without rewriting it, and the gate is per `(claims, receipt)` pair. A tip-safe wrapper would be a table
  `{37: red, 38: red, 39: green}` re-derived at the tip by running the gate over each round's pinned pair — that
  makes the observation historical but stable, and is the shape I recommend when the L1 wires it. Building the
  wrapper was outside this ticket; the row's `check` names the gate either way.

## 6. Operability — ready-to-paste registry row (`SKILL.md`, eight columns)

```
| `order-check` | gate | `python3 plans/order_check.py --lane . --claims plans/round-NN-claims.md --receipt <receipt>` (read-only over git history; no `--work`, no probe) | `0` no claims/ file committed at or before the first receipt commit shows the frozen probe executed, the freeze commit does not carry the receipt, and the receipt is not an ancestor of the freeze commit · `1` `ORDER FAIL <class>` (`probe-executed-before-receipt` / `freeze-contains-receipt` / `receipt-before-claims`) · `2` setup (not a repo, claims or receipt never committed, bad round name) | `calibrate.py`: 13 fixtures 13/13, 6 mutants 6/6 attributed, rerun byte-equal (`build/R39OrderGate/calibration.txt`); shown red on rounds 37 and 38, green on 39 (`build/R39OrderGate/real-repos.txt`) | the lane's git history, `plans/round-NN-claims.md`, the receipt under `corpus/evidence/` | nothing (stdout only) | kengaku |
```

Recheck command (copy-paste, lane root, no scratch):

```
python3 plans/order_check.py --lane . --claims plans/round-39-claims.md --receipt corpus/evidence/round39/git-leak-probe.txt
python3 plans/order_check.py --lane . --claims plans/round-38-claims.md --receipt corpus/evidence/round38/build-pmars-probe.txt
python3 plans/order_check.py --lane . --claims plans/round-37-claims.md --receipt corpus/evidence/round37/git-webserver-probe.txt
```

expected `PASS/0`, `FAIL/1`, `FAIL/1`. Recalibration: `python3 calibrate.py --gate plans/order_check.py --work <scratch>`
(expected `FIXTURES total=13 wrong=0` … `MUTANTS total=6 killed=6 survived=0`, byte-equal on rerun).

## 7. Limits and risks

* **Token heuristic.** A claims file that merely *quotes* a forbidden line trips it. That is the literal rule ("what a
  committed file shows"), and it is the safe direction for a pre-registration gate; the false-negative side is a
  `P10` line split across lines. Not tested: a `P10` line written with a prefix that defeats `^\s*(?:gate:\s*)?P10`
  (e.g. inside a diff hunk with `+`), which a future controls-file format could produce — the gate would miss it.
* **Commit order is not authorship order.** The gate polices what history proves; a probe run whose output was never
  committed (the round-37/38 shape) is caught only because the counter's skip-control echoed the gate's own line.
  A round that runs the probe and commits *nothing* that shows it stays invisible to this gate; that residue is
  `plans/tip_receipts.py`'s half, not this gate's.
* **The receipt must be committed.** At freeze time the gate exits 2; a wave that wants an at-freeze verdict gets
  refusal, by design.
* **Windows are path-derived.** A claims control committed under a *different* round's directory is not scanned
  (fixture `f12`) — correct for the class, and it means a mis-shelved control escapes.
* The gate does not verify the receipt's content or its probe's digest (that is C2 V1/V5); it answers one question.

## 8. Axes (godspeed)

* **Calibration — moves.** The class the claims file names "recurred twice" now has an executable check, with a
  red-before state on both occurrences computed from committed history rather than from a prose disclosure, and with
  a green state on the round that fixed it. 13 fixtures / 6 attributable mutants / byte-equal rerun is the same
  receipt shape the frozen counters use, so the L1 can admit it without a second instrument. No existing number is
  reinterpreted: round 37's and 38's verdicts were already recorded as mistakes in their lessons; this gate makes
  them machine-checkable.
* **Operability — moves.** One stdlib script, no scratch, no sandbox, no probe run, three positional facts, stable
  `ORDER …` line grammar, exit 2 for every unanswerable state, a registry row and a three-line recheck command.
  Running it at the landing tip is seconds and needs no clone.
* Harmed axes: none identified. Nothing frozen was edited, and the gate is additive (no lane caller changes).

## 9. For the L1 (integration, in order)

1. Place `order_check.py` at `plans/order_check.py` (digest `948d5e1d…fc6ecc`); add the `order-check` registry row.
2. Commit `calibration.txt`, `calibration-rerun.txt`, `real-repos.txt` and `calibrate.py` under the round-39 evidence
   path you choose, so the controls are lane bytes, not wave bytes.
3. Commit `corpus/defects-round39.jsonl` with the row above (`status: open`); flip to `closed`/`closed_round: 39` in
   the landing commit with the tip receipt attached, and decide the tip-wrapper question in §5.
4. Append the round-38 lesson correction (R3's second half: that lesson row misstates the round-37 fix) yourself —
   that file is a lane file, and drafting its wording was not assigned here.

VERDICT: order-gate-r38-red-r39-green
