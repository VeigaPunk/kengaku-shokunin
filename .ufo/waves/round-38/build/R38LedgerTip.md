# R38LedgerTip — routed D4: `ledger_tip` in detached-HEAD clones (round 38 wave 1, executor)

Seat: executor (leaf), round 38 wave 1, item R38LedgerTip. Lane read-only: **nothing** in
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` was written except this report dir
`.ufo/waves/round-38/build/R38LedgerTip/`. No lane git index, jj state, `plans/`, `corpus/`, SCORECARD,
LOG, SKILL or PROVINCE file touched: after the whole seat `git -C <lane> status --porcelain -- plans/
corpus/ SCORECARD.md LOG.md SKILL.md` prints exactly one line, `?? plans/mutant_direction_check.py` —
a concurrent wave-1 seat's in-flight file (`Round-38 mined-mistake fix: … kill DIRECTION`, written
02:50 while this seat ran), not mine and untouched — and `git -C <lane> rev-parse HEAD
refs/heads/master` → both `2c5f4e0ba8e2865af4b71e337f3cde86eaf0702e`. Measured lane tip: `2c5f4e0b` (round-38 wave-1 build spec). Nothing committed
anywhere. No tool was installed or upgraded (no pacman call; Python 3.14.8 and git were present), so
there is no tool-install line to record beyond that.

Scratch `S=/fast/scratch/hyaku/kengaku-r38/R38LedgerTip` (`export TMPDIR=$S`), every git call with
`-C "$S/lane"`, toplevel verified `= "$S/lane"` before any write, removed at the end.

Deliverables in this seat dir:

| file | role |
|---|---|
| `ledger_tip.py` | **fixed draft** (sha256 `f5baea4436a818b6ddecbd193b8df59be1f28b0d42c95258518e2138e95bc38c`) — land as `plans/ledger_tip.py` |
| `ledger_tip.committed.py` | byte copy of the landed file (sha256 `67cb3966…a271`) so the draft is reviewable as a diff without the lane |
| `ledger_tip.diff` | `diff -u committed draft` (179 lines, 126 +/- lines) |
| `controls.sh` | replays every control below; every rc quoted here appears on its `##` line |
| `receipts/01…14-*.log` | the raw run logs quoted below |

## 1. Root cause: two defects, both in the driver's exit contract

Reproduced on a scratch clone of the lane, source clone checked out **detached** at the tip's parent
`e95cf550` while its `refs/heads/master` stayed at `2c5f4e0b` — the shape the fleet's fixture rule
imposes on every seat — with the **landed** `plans/ledger_tip.py`:

```
python3 plans/ledger_tip.py --source "$S/src-det2" --work "$S/before2/det"   # rc=1
R34-D2 status=closed observed=fail agree=NO error CalledProcessError: … 'ls-tree', '-r', '--name-only', 'refs/heads/master' … exit status 128
R35-D3 status=closed observed=fail agree=NO error CalledProcessError: … 'ls-tree', '-r', '--name-only', 'refs/heads/master' … exit status 128
rows=9 closed=9 observed_pass=7 mismatches=2
```
(`receipts/01-before-detached.log`; identical to `F37NoHarmSweep.md` §3's observation.)

Clone state after that run: `for-each-ref refs/heads | wc -l` = **0**, `refs/remotes/origin/master` =
`2c5f4e0b`, `HEAD` = `e95cf550` — `git clone --shared` of a detached source creates no local branch, so
the two pin bodies (`plans/defect_ledger.py:29` and `plans/round36_c1_verify.py:38`, both
`BRANCH = "refs/heads/master"`) cannot resolve the rev they name.

Defect 2, same receipt family: the script's **declared** refusals did not use the declared code. The
registry row says "`2` usage/clone refusal" (`SKILL.md:581`), but
`raise SystemExit(f"refuse to reuse {dest}…")` exits **1**:

```
python3 plans/ledger_tip.py --source "$S/lane" --work "$S/before/normal"   # lane already exists
refuse to reuse …/before/normal/lane; remove it first                       # rc=1  (receipts/05)
```
and a non-git `--source` raised an uncaught `CalledProcessError` traceback at **1** (`receipts/07`).

## 2. Where the fix must live (why not the two check bodies)

`plans/defect_ledger.py` is a **frozen instrument of another round**:
`plans/pkg-spec-r35.json` `frozen_instruments["plans/defect_ledger.py"] = 4e386677…` (the file's current
sha256 is exactly that), and that spec is itself a pin of the frozen round-38 C1 counter
(`PINS["plans/pkg-spec-r35.json"] = e085b435…`). Measured consequence of editing it — one appended
comment line in a scratch clone, then the gate over that tree:

```
python3 plans/pkg_gate.py package --root $S/editdg --spec plans/pkg-spec-r35.json
P1 DEFECT pinned=3 mismatched=['plans/defect_ledger.py']        defects=1   rc=1
```
(`receipts/14-gate-p1-edited-defect_ledger.log`.) A red P1 makes the gate reject the genuine round-35
package, which reddens round-36 fixture P0 and therefore the frozen C1 battery. `plans/round36_c1_verify.py`
is pinned outright by the frozen counter (`PINS[…round36_c1_verify.py] = d7c3687c…`), so it is out of
scope by the round-38 freeze. **Both check bodies therefore stay byte-identical; the binding is done by
the driver, which is not pinned by anything** (`grep -rn ledger_tip plans/*.json plans/round38_c2_verify.py
plans/pkg-spec-r38.json` → no hits).

## 3. The draft's change (4 points, `ledger_tip.diff`)

1. `bind_pin_refs()` — after the clone, each imported module's `BRANCH` is read. A ref the clone carries
   is left alone (normal clones: **no** new output). A ref it lacks is bound to the commit under audit —
   the clone's `HEAD`, the same sha the `TIP commit=` line prints — and reported once per ref:
   `REF BIND ref=refs/heads/master rev=<tip> source_ref=<sha|absent> why=clone-lacks-ref`.
   `ls-tree` accepts a commit id, so the frozen pin bodies observe the audited tree unchanged.
2. `refuse(msg)` — prints one `REFUSE <reason>` line to stderr and raises `SystemExit(2)`, used by every
   clone/usage/setup path (source not a repo, clone rc≠0, toplevel mismatch, no HEAD, dirty clone, ref
   reuse, unloadable module, unreadable ledger). This makes `SKILL.md:581`'s "`2` usage/clone refusal"
   true, and keeps `1` meaning "a ledger row disagrees".
3. A `subprocess.CalledProcessError` escaping a check body is now a **setup refusal (exit 2)**, not
   `observed=fail agree=NO` — the exact fold F37 named as the harm. Other check-body exceptions stay
   observed failures ("a crash is an observed failure, never a pass" is preserved).
4. `git clone` runs with `-c advice.detachedHead=false`, so a receipt's first line is the `TIP` line
   instead of git's multi-line detached-HEAD advice block.

## 4. Before / after, same machine, same seconds

| # | shape | command | before (landed) | after (draft) | receipt |
|---|---|---|---|---|---|
| 1 | detached source (`HEAD`=`e95cf550`, master=`2c5f4e0b`) | `ledger_tip.py --source $S/src-det2 --work …` | **rc=1**, `observed_pass=7 mismatches=2`, 2× `CalledProcessError … 128` | **rc=0**, `rows=9 closed=9 observed_pass=9 mismatches=0`, `REF BIND ref=refs/heads/master rev=e95cf550… source_ref=2c5f4e0b…` | `01`, `02` |
| 2 | normal clone (source on master, `--shared` like the fixture rule's first step) | `--source $S/lane --work …` | rc=0, `mismatches=0` | rc=0, `mismatches=0`, **output byte-identical** after normalising the work path (`diff` empty) | `03`, `04` |
| 3 | real lane `kengaku-shokunin` at `2c5f4e0b` | `--source <lane> --work …` | rc=0 | rc=0, **identical** output | `12`, `13` |
| 4 | existing `<work>/lane` | `--work <already used>` | rc=**1**, `refuse to reuse …` | rc=**2**, `REFUSE will not reuse …` | `05`, `06` |
| 5 | `--source` not a git repo | `--source $S/notarepo` | rc=**1**, `CalledProcessError` traceback | rc=**2**, `REFUSE --source … is not a readable git repository` | `07`, `08` |
| 6 | control mode, detached clone **with `master` deleted**, one planted D4 defect | `--lane $S/ctl-nobranch` | rc=1, `observed_pass=6 mismatches=3` (2 ref crashes + the planted one) | rc=1, `observed_pass=8 mismatches=1` — `R34-D4 … agree=NO correction_lines=2` only; `R34-D2`/`R35-D3` now `observed=pass`, and the durable defect **still** exits 1 | `09`, `10`, `11` |
| 7 | `--work` several levels absent | `--source $S/lane --work $S/wtest/deep/absent` | rc=0 (mkdir already present) | rc=0, clone created | `controls.sh` run |

Row 6 is the sharp control: on one tree, before → 3 mismatches (2 of them the environment artifact),
after → 1 mismatch (the planted pin failure). The fix removes only the environment artifact; the pin
kind still bites, and a genuine failure still exits 1 rather than 2.

## 5. Limits named now

- The bound commit is the **audited tip** (clone `HEAD`), not the source's branch tip; when they differ
  the `REF BIND` line prints the source's value (`source_ref=…`), so the divergence is visible, never
  silent. If a clone *does* carry `refs/heads/master` pointing elsewhere than `HEAD`, that ref is still
  used unmodified — unchanged from the landed behaviour, and the `TIP commit=` line names the tree the
  behaviour rows read.
- The binding works by setting the imported module's `BRANCH` global (read at call time inside both
  bodies); no file, ref or index is written. It is a driver-level binding, not an edit of a frozen body —
  a reader who trusts only the bodies must accept the one printed `REF BIND` line as the provenance.
- `CalledProcessError → exit 2` intentionally reclassifies "git could not read this tree" as setup; a
  check body that raises anything else stays an observed failure.
- I did not re-run the two round-38 claim counters or the round-36/37 batteries: that is the main
  agent's post-integration gate, and the draft lands in `plans/ledger_tip.py`, which no pin covers.

## 6. Integration note for the L1

Land `ledger_tip.py` over `plans/ledger_tip.py` (no other file needs to change: `SKILL.md:581`'s
"`2` usage/clone refusal" and its `0/1` meanings become true as written). The controls cited by that row
(`.ufo/waves/round-37/build/R37LedgerTip/control-ctl*.txt`) remain valid: every one of them lands in the
`observed=fail agree=NO … rc=1` branch, which the draft leaves unchanged. If the L1 prefers a different
binding rule (source branch tip instead of the audited tip), the only edit needed is inside
`bind_pin_refs`; the exit-code contract is independent of it and is what the row declares.

VERDICT: ledger-tip-detached-fixed
