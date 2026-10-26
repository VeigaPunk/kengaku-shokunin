# R39LedgerProvenance — `ledger_tip.py` ref provenance + stale-ref refusal (round 39 wave 1, executor)

Seat: executor (leaf). Item: round-38 closure **R5b** (`corpus/lessons/round-38-verifier-spotcheck.md:169-171`),
defects **F1/F2** of `.ufo/waves/round-38/falsify/F38LedgerTip.md` §5. Lane
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` was **read-only** for this seat: no lane file, index, ref or jj
state was written; `git -C <lane> status --porcelain -- plans/ corpus/ SCORECARD.md LOG.md SKILL.md README.md
PROVINCE.md` after the whole seat prints exactly one line, `?? corpus/lessons/round-39.md` — a concurrent seat's
in-flight file, not mine. Every write went to this seat dir. No tool installed or upgraded (Python 3.14.8 and git
2.56.0 were already present; pacman transactions are paused host-wide anyway), so there is no install line to
record. Scratch `S=/fast/scratch/hyaku/kengaku-r39/R39LedgerProvenance` (`export TMPDIR=$S`), every git call with
`-C "$S/…"`, each clone verified `--show-toplevel` before use, removed at the end (`SCRATCH_REMOVED`).

## 0. Deliverables (all under `.ufo/waves/round-39/build/R39LedgerProvenance/`)

| file | role |
|---|---|
| `ledger_tip.py` | **fixed draft** (sha256 `853bcb2a5052b3c2319d3006459bb5012ba72dfc1e5f22874f7334b62eb77ad4`) — land as `plans/ledger_tip.py` |
| `ledger_tip.diff` | `diff -u plans/ledger_tip.py draft` (136 lines) so the change is reviewable without the lane |
| `receipts/01…14-*.log` | raw runs quoted below, each ending with its `exit=<n>` line |

Lane body replaced: `plans/ledger_tip.py` sha256 `f5baea4436a818b6ddecbd193b8df59be1f28b0d42c95258518e2138e95bc38c`
(`sha256sum plans/ledger_tip.py`, and `git show HEAD:plans/ledger_tip.py | sha256sum` → same, so the lane copy is
the committed body, unedited in place).

## 1. What the fix is (three points, `ledger_tip.diff`)

1. **Provenance before any row.** `bind_pin_refs` becomes `audit_pin_refs`: every ref a check body names
   (`plans/defect_ledger.py:29`, `plans/round36_c1_verify.py:38` — both `BRANCH = "refs/heads/master"`) is resolved
   once in the tree under audit, printed once, and **bound into the module as the sha that was printed**, so the row
   observes exactly the commit the output names and cannot be re-pointed under it mid-run. Two lines:
   `REF AUDIT ref=<ref> rev=<sha> tip=<sha> state=match` · `REF BIND ref=<ref> rev=<sha> tip=<sha>
   source_ref=<sha|absent> why=clone-lacks-ref` (the round-38 D4 detached-clone case, unchanged in effect, plus a
   `tip=` field).
2. **Stale ref = refusal (exit 2), before any ledger statement.** A ref that resolves to a commit other than the one
   under audit is `REFUSE stale pin ref: <ref> resolves to <rev> … but the commit under audit is <tip>; <body> would
   observe a different tree …`. This is the F1 harm turned into a visible stop: the round-38 shape reded a clean
   tree (`mismatches=2`, exit 1) while naming neither ref nor revision.
3. **F2: ledger statements are buffered** and flushed only after both ledgers have been evaluated, so a refusal
   raised mid-ledger leaves no row, no `LEDGER` line and no summary behind — matching the docstring's "no ledger
   statement is made". Normal output order is unchanged (flush happens in append order, then the summary line).

Exit-code contract is untouched: `0` clean · `1` a row disagrees · `2` usage/clone/setup refusal (`SKILL.md:581`).

## 2. Red-before (current lane body, fixture clone with stale master) — `receipts/01`

Fixture: `git clone --shared $S/lane $S/ctl-stale`; `git -C … checkout --detach 7504738…` (the audited tip);
`git -C … update-ref refs/heads/master 11d6453…` (round-35 close, so the pin inputs really differ —
`committed_mirror_paths=109413` there, `0` at the tip). Verified `HEAD`=`7504738…`, `refs/heads/master`=`11d6453…`,
`status --porcelain` empty.

```
$ python3 plans/ledger_tip.py --lane "$S/ctl-stale"          # lane body f5baea44
R34-D2 status=closed observed=fail agree=NO committed_mirror_paths=109413 …
R35-D3 status=closed observed=fail agree=NO committed_nested_wave_paths=102164 …
rows=9 closed=9 observed_pass=7 mismatches=2
exit=1
```
`grep -c 11d64530 receipts/01-…` → **0**: a clean tree is reded at exit 1 and the output names neither the ref nor
the revision it read — F1 reproduced at the round-39 tip, in the mode `SKILL.md:581` documents as control mode.

## 3. Green at the lane tip (fixed draft) — `receipts/03`, `04`

```
$ python3 <draft> --lane "$S/lane"                     # receipts/03, exit=0
TIP commit=750473847af9c7a461487ba3a589b5519fac5ed8 control=…/lane dirty=0
REF AUDIT ref=refs/heads/master rev=750473847af9c7a461487ba3a589b5519fac5ed8 tip=750473847af9c7a461487ba3a589b5519fac5ed8 state=match
…
rows=9 closed=9 observed_pass=9 mismatches=0

$ python3 <draft> --source "$S/lane" --work "$S/w-clone"   # receipts/04, exit=0
TIP commit=750473847af9c7a461487ba3a589b5519fac5ed8 clone=…/w-clone/lane
REF AUDIT … state=match
…
rows=9 closed=9 observed_pass=9 mismatches=0
```
(`REFUSE` count in receipt 03/04 = 0; `REF AUDIT` lines = 1 each, `grep -c '^REF AUDIT'`.)

## 4. Same fixture, fixed body — the stale ref is refused, not reded (`receipts/02`, `12`)

```
$ python3 <draft> --lane "$S/ctl-stale"                # receipts/02, exit=2
TIP commit=750473847af9c7a461487ba3a589b5519fac5ed8 control=…/ctl-stale dirty=0
REFUSE stale pin ref: refs/heads/master resolves to 11d64530179b78e33ba6074fc77d63d36ee7ac31 in …/ctl-stale but the commit under audit is 750473847af9c7a461487ba3a589b5519fac5ed8; plans/defect_ledger.py would observe a different tree (check out that ref or delete it, or audit 11d64530179b78e33ba6074fc77d63d36ee7ac31 instead)
```
`grep -c '^REFUSE'` = **1**, `grep -cE '^(R34|R35|LEDGER)'` = **0** — one line, no ledger statement, exit 2.
Direction of the divergence does not matter: with the audited tree at the **freeze** commit `088f7c3…` and master at
the tip (`receipts/12`) the same refusal fires (`rev=7504738…`, `tip=088f7c3…`, exit 2).

## 5. Every other path still behaves (`receipts/05…14`)

| path | receipt | observed |
|---|---|---|
| detached source, no local branch | `05-green-detached-source-bind` | `REF BIND … rev=7504738… tip=7504738… source_ref=absent why=clone-lacks-ref`, `rows=9 … mismatches=0`, exit 0 (round-38 D4 fix retained) |
| detached source whose own master is old | `06-bind-detached-source-with-stale-master` | clone has **no** local branch (`git clone` of a detached source creates none), so `REF BIND … source_ref=11d6453…`, rows read the audited tip, exit 0 — the divergence is printed, and the tree read is the audited commit by construction |
| control mode, no ref at all | `14-green-control-no-ref-bind` | `REF BIND … source_ref=absent`, `rows=9 … mismatches=0`, exit 0 |
| planted duplicate D4 correction line (genuine row failure) | `09-red-genuine-row-still-exits-1` | `R34-D4 … agree=NO correction_lines=2`, `rows=9 closed=9 observed_pass=8 mismatches=1`, exit **1** — the fix does not mask a row |
| no arguments | `10-usage` | argparse usage, exit **2** |
| `--work` already holds `<work>/lane` | `11-refuse-work-reuse` | `REFUSE will not reuse …; remove it first`, exit **2** |
| pre-fix body, clone mode at the tip | `13-prefix-clone-mode` | exit 0, `rows=9 closed=9 observed_pass=9 mismatches=0` |

**Output delta vs the round-38 body is exactly the provenance line**: receipt `04` with the one `^REF AUDIT` line
(and the work path) removed is `diff`-identical to receipt `13` (`IDENTICAL_AFTER_REF_AUDIT_STRIP`, 13 lines each).

## 6. F2, before/after on the same tree (`receipts/07`, `08`)

One broken-but-legal environment (`GIT_INDEX_FILE=/nonexistent-dir/x`) in control mode: `git status --porcelain` and
`git ls-files --others` then exit 0 with wrong answers, so `r34_d1` is folded into a false `agree=NO` and `r35_d1`
raises `CalledProcessError` afterwards.

| body | receipt | rows printed | verdict |
|---|---|---|---|
| lane body `f5baea44` | `07-f2-red-before-midledger` | **6** (`R34-D1 … agree=NO untracked=198`, the rest of ledger 1, `LEDGER corpus/defects.jsonl … mismatches=1`) then `REFUSE check r35_d1 could not query …` | exit 2 with a false `agree=NO` already on stdout |
| draft | `08-f2-green-no-statements-before-refuse` | **0** (`grep -cE '^(R34|R35|LEDGER)'` = 0) | `TIP` + `REF AUDIT` + one `REFUSE`, exit 2 |

## 7. Pinned check bodies stay byte-identical

Nothing in `plans/defect_ledger.py` or `plans/round36_c1_verify.py` was written, and their digests still equal the
pins that freeze them:

```
$ sha256sum plans/defect_ledger.py plans/round36_c1_verify.py
4e386677b48fd66e1a19a7459ab5e5359139e282e0968afa2cfd2395768d763d  plans/defect_ledger.py
d7c3687c09ed4c8a09a9d7c63efa9232c2b1aff8ffb229fb8a0505578317df73  plans/round36_c1_verify.py
```
— equal to `plans/pkg-spec-r35.json:36` `frozen_instruments["plans/defect_ledger.py"]` (gate clause P1) and to
`plans/round38_c1_verify.py:75` `PINS["plans/round36_c1_verify.py"]`. The change lives entirely in the driver
(`plans/ledger_tip.py`, which no pin names: `grep -rn ledger_tip plans/*.json` → no hits). The binding mechanism is
unchanged in kind — the imported module's `BRANCH` global is replaced — but now it is always replaced by the sha that
was printed, so the row's tree is pinned to the printed provenance rather than to a ref name.

## 8. Integration note for the L1 (draft, not applied)

- Land `ledger_tip.py` over `plans/ledger_tip.py`. No other file must change for the behaviour.
- `SKILL.md:581`'s `2` cell reads "usage/clone refusal". The draft adds one refusal class — a pin ref naming another
  commit. A minimal wording edit (L1's call, not made here): "`2` usage/clone/setup refusal, including a pin ref
  (`refs/heads/master`) that resolves to a commit other than the one under audit".
- The round-37 controls cited by that row (`.ufo/waves/round-37/build/R37LedgerTip/control-ctl*.txt`) are historical
  receipts of the round-37 body; re-running them under the draft would add one `REF AUDIT` line each. I did **not**
  re-run them (their fixture clones no longer exist); every one of them shows `TIP commit=44b7298a…` with a clone
  made from that tip, the shape in which `refs/heads/master` = `HEAD` = match, so the rows are expected unchanged —
  see the limit below.
- No pinned byte comparison of `ledger_tip.py` output exists: `plans/tip_receipts.py`'s population is
  `corpus/evidence/**/probe*.{txt,log}` and no counter or gate invokes `ledger_tip.py` (`grep -rn ledger_tip` over
  `plans/*.py`, `plans/*.json` → only the file itself).

## 9. Limits named now

- Red-before and green are measured on this host (git 2.56.0, Python 3.14.8) on scratch clones of lane tip
  `750473847af9c7a461487ba3a589b5519fac5ed8`; the refusal is by **commit identity**, so a stale ref whose pinned
  inputs happen to be identical in both commits is refused too. That is deliberate (the round-38 F1 silent-green
  shape, `F38LedgerTip` receipt 16) and it is why the message names the ref, its commit and the audited commit.
- The stale-ref refusal is reachable in control mode, which is where a prepared tree with a moved ref exists; a
  `git clone --shared` of a normal lane gives a clone whose local `master` **is** `HEAD` (match), and a clone of a
  detached source gets no local branch at all (bind), so clone mode in practice only ever prints BIND or MATCH.
  Measured, not assumed: `git -C $S/w-det/lane for-each-ref refs/heads | wc -l` = 0.
- I did not re-adjudicate whether each ledger row's claim is true, did not re-run the round-36/37/38 batteries or the
  round-39 C1/C2 counters, and did not run the gate — that is the parent's post-integration gate.
- A check body that reads a ref under another name, or stops reading `BRANCH` at call time, would bypass the
  provenance entirely; nothing in the driver asserts a body still has `BRANCH` beyond printing one line per ref it
  finds.

## 10. Receipts

`.ufo/waves/round-39/build/R39LedgerProvenance/receipts/`: `01-red-before-stale-master.log`,
`02-green-refuse-stale-master.log`, `03-green-lane-tip-control.log`, `04-green-lane-tip-clone.log`,
`05-green-detached-source-bind.log`, `06-bind-detached-source-with-stale-master.log`,
`07-f2-red-before-midledger.log`, `08-f2-green-no-statements-before-refuse.log`,
`09-red-genuine-row-still-exits-1.log`, `10-usage.log`, `11-refuse-work-reuse.log`, `12-refuse-master-ahead.log`,
`13-prefix-clone-mode.log`, `14-green-control-no-ref-bind.log`. Scratch removed before this report.

VERDICT: ledger-provenance-red-before-yes
