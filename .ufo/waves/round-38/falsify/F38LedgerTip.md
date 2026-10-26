# F38LedgerTip — falsify the D4 fix (`ledger_tip.py` in detached-HEAD clones)

Seat: executor (leaf), round 38 wave 2, item F38LedgerTip. Attacked: routed defect **D4** as landed by
wave-1 seat `R38LedgerTip` (`.ufo/waves/round-38/build/R38LedgerTip.md`), i.e. the claim that
`plans/ledger_tip.py` at `8c7422d7a646515d80af44844e8ecc8a1fc1d30a` no longer folds a detached-clone ref
into `observed=fail agree=NO`, that it refuses with exit 2 instead of reding a row, and that normal clones
see byte-identical output.

Lane read-only: nothing in `/home/vgpnk/Projects/shokunin/kengaku-shokunin` was written except
`.ufo/waves/round-38/falsify/F38LedgerTip.md` and the receipts in `.ufo/waves/round-38/falsify/F38LedgerTip/`.
No lane file, index, ref or jj state touched: `git -C <lane> status --porcelain -- plans/ corpus/ SKILL.md
SCORECARD.md LOG.md README.md PROVINCE.md` → **empty**. Scratch `S=/fast/scratch/hyaku/kengaku-r38/F38LedgerTip`
(`export TMPDIR=$S`), every git call with `-C`, every clone verified `--show-toplevel`; removed at the end.
No tool installed or upgraded (Python 3.14.8, git 2.56.0 already present), so there is no install line.

Script under test, identity checked four ways (all `f5baea4436a818b6ddecbd193b8df59be1f28b0d42c95258518e2138e95bc38c`):

```
$ git -C "$S/norm" show HEAD:plans/ledger_tip.py | sha256sum
f5baea4436a818b6ddecbd193b8df59be1f28b0d42c95258518e2138e95bc38c  -
$ sha256sum $L/plans/ledger_tip.py "$S/norm/plans/ledger_tip.py" $L/.ufo/waves/round-38/build/R38LedgerTip/ledger_tip.py
f5baea44…  <lane>/plans/ledger_tip.py
f5baea44…  <clone>/plans/ledger_tip.py
f5baea44…  <wave-1 draft>
```

## 1. Mandated run A — detached-HEAD source, driver's own `--shared` clone of `8c7422d`

Source `$S/det` = `git clone --no-local <lane> && git checkout 8c7422d && git branch -D master`
(`HEAD=8c7422d…`, `refs/heads/master` absent: `rev-parse --verify --quiet refs/heads/master` rc=1, clean).
Driver clone verified `--shared`: `$S/w1/lane/.git/objects/info/alternates` = `$S/det/.git/objects`,
`count-objects` → `count: 0`.

`receipts/01-detached-source.log`, `python3 plans/ledger_tip.py --source "$S/det" --work "$S/w1"`:

```
exit=0
TIP commit=8c7422d7a646515d80af44844e8ecc8a1fc1d30a clone=/fast/scratch/hyaku/kengaku-r38/F38LedgerTip/w1/lane
REF BIND ref=refs/heads/master rev=8c7422d7a646515d80af44844e8ecc8a1fc1d30a source_ref=absent why=clone-lacks-ref
R34-D1 status=closed observed=pass agree=yes ledger=corpus/defects.jsonl kind=live
R34-D2 status=closed observed=pass agree=yes ledger=corpus/defects.jsonl kind=pin
R34-D3 status=closed observed=pass agree=yes ledger=corpus/defects.jsonl kind=pin
R34-D4 status=closed observed=pass agree=yes ledger=corpus/defects.jsonl kind=pin
R34-D5 status=closed observed=pass agree=yes ledger=corpus/defects.jsonl kind=pin
LEDGER corpus/defects.jsonl rows=5 closed=5 observed_pass=5 mismatches=0
R35-D1 status=closed observed=pass agree=yes ledger=corpus/defects-round35.jsonl kind=live
R35-D2 status=closed observed=pass agree=yes ledger=corpus/defects-round35.jsonl kind=live
R35-D3 status=closed observed=pass agree=yes ledger=corpus/defects-round35.jsonl kind=pin
R35-D4 status=closed observed=pass agree=yes ledger=corpus/defects-round35.jsonl kind=pin
LEDGER corpus/defects-round35.jsonl rows=4 closed=4 observed_pass=4 mismatches=0
rows=9 closed=9 observed_pass=9 mismatches=0
```

**No `agree=NO`, exit 0.** The bound rev equals the `TIP commit=` sha, so the pins observe the audited
commit and not a sibling tree. Two more detached variants, same result: source detached with
`refs/heads/master` **present but diverged** at `10d2e97` (`receipts/03`, `source_ref=10d2e977…`,
rc=0) and at `1fa7af45` via the mandated clone itself (`receipts/19`, `source_ref=1fa7af4528a5…`, rc=0);
a third shape, source checked out on branch `audit@8c7422d` with `master@11d64530`, also binds and
passes (`receipts/15`, `why=clone-lacks-ref`, rc=0). `git clone --shared` of any of those sources creates
**no local branch** (`for-each-ref refs/heads | wc -l` = 0 in `w1`, `w13`), which is why the binding is the
path actually taken in the fixture shape the fleet mandates.

## 2. Mandated run B — normal clone

Source `$S/norm` = fresh clone, `checkout -B master 8c7422d` (`HEAD` = `master` = `8c7422d`).
`receipts/02-normal-clone.log`, `python3 plans/ledger_tip.py --source "$S/norm" --work "$S/w2"`:

```
exit=0
TIP commit=8c7422d7a646515d80af44844e8ecc8a1fc1d30a clone=/fast/scratch/hyaku/kengaku-r38/F38LedgerTip/w2/lane
R34-D1 status=closed observed=pass agree=yes ledger=corpus/defects.jsonl kind=live
R34-D2 status=closed observed=pass agree=yes ledger=corpus/defects.jsonl kind=pin
R34-D3 status=closed observed=pass agree=yes ledger=corpus/defects.jsonl kind=pin
R34-D4 status=closed observed=pass agree=yes ledger=corpus/defects.jsonl kind=pin
R34-D5 status=closed observed=pass agree=yes ledger=corpus/defects.jsonl kind=pin
LEDGER corpus/defects.jsonl rows=5 closed=5 observed_pass=5 mismatches=0
R35-D1 status=closed observed=pass agree=yes ledger=corpus/defects-round35.jsonl kind=live
R35-D2 status=closed observed=pass agree=yes ledger=corpus/defects-round35.jsonl kind=live
R35-D3 status=closed observed=pass agree=yes ledger=corpus/defects-round35.jsonl kind=pin
R35-D4 status=closed observed=pass agree=yes ledger=corpus/defects-round35.jsonl kind=pin
LEDGER corpus/defects-round35.jsonl rows=4 closed=4 observed_pass=4 mismatches=0
rows=9 closed=9 observed_pass=9 mismatches=0
```

No `REF BIND` line. `diff` of run A against run B with the clone path and the single `REF BIND` line
stripped → **empty** (`IDENTICAL_AFTER_REFBIND_STRIP`), so the binding adds exactly one line and changes
no row. Also green at the lane's live tip as `--source` (`receipts/11`, `TIP commit=1fa7af4528a5…`,
`rows=9 … mismatches=0`) — note the lane moved under me during this seat (`10d2e97` → `1fa7af45` between
my first and last clone; both green).

## 3. Before/after on the same commit, same shapes (does the fix attack a real red?)

Pre-fix body extracted from git, not retyped: `git show dc0cdb54:plans/ledger_tip.py` → sha256
`67cb3966c0dfc56f29997a7fc3e3200d07d7096f0f35bf70adb8fae5d051a271` (matches the wave-1 report's
`67cb3966…a271`).

| shape | body | receipt | result |
|---|---|---|---|
| detached `8c7422d` | pre-fix | `receipts/09-prefix-detached.log` | **rc=1**, `rows=9 closed=9 observed_pass=7 mismatches=2`, `R34-D2`/`R35-D3` `agree=NO error CalledProcessError: … 'ls-tree', '-r', '--name-only', 'refs/heads/master' … exit status 128` |
| detached `8c7422d` | fixed | `receipts/01` | rc=0, `mismatches=0`, one `REF BIND` |
| normal | pre-fix | `receipts/10-prefix-normal.log` | rc=0, `mismatches=0` |
| normal | fixed | `receipts/02` | rc=0, byte-identical to pre-fix |

So the D4 symptom is reproducible at the landed tip with the pre-fix body (a false red at exit 1, from a
healthy tree) and gone with the landed body; and the "normal clones unchanged" claim holds at `8c7422d`,
not only at the wave-1 seat's commit.

## 4. Exit-code contract (SKILL.md:581: `0` clean · `1` mismatch · `2` usage/clone refusal)

| path | receipt | observed |
|---|---|---|
| clean, detached / normal / branch source / live tip | 01, 02, 15, 19, 11, 12 | rc=0 |
| `--work` already holds a clone | `04-refuse-reuse.log` | rc=**2**, `REFUSE will not reuse …/w2/lane; remove it first`, no summary line |
| `--source` not a repo | `05-refuse-nonrepo.log` | rc=**2**, `REFUSE --source … is not a readable git repository` |
| no arguments | `13-usage.log` | rc=**2**, `ledger_tip.py: error: either --lane, or both --source and --work` |
| tree predates the check body (`plans/round36_c1_verify.py` absent) | `14-old-tree-missing-module.log` | rc=**2**, `REFUSE cannot import …/plans/round36_c1_verify.py: FileNotFoundError` |
| ledger file absent | `18-missing-ledger.log` | rc=**2**, `REFUSE cannot read corpus/defects-round35.jsonl: FileNotFoundError` |
| planted duplicate D4 correction line (control mode) | `07-control-planted-red.log` | rc=**1**, `R34-D4 … agree=NO correction_lines=2`, other 8 rows pass |

A genuine red still exits 1 and a clone/setup problem still exits 2, and the pin kind still bites after the
fix (row 7) — the fix is not masking.

## 5. Findings

### F1 — real, medium: control mode (`--lane`) still reads a *different commit* than `TIP commit=`, silently

`bind_pin_refs` keys on ref **existence**, not on ref **agreement with the audited tip**:
`plans/ledger_tip.py:145` `if git_out(lane, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"): continue`.
In `--lane` mode `source=None`, so nothing binds; the two pin bodies
(`plans/defect_ledger.py:51`, `plans/round36_c1_verify.py:293`) read `refs/heads/master` unmodified. The
mandated clone shape itself produces that divergence: `git clone --no-local <lane> && git checkout <sha>`
leaves `refs/heads/master` at the branch tip while `HEAD` is the audited sha.

Proof the read is real and can red — control mode, detached `HEAD=8c7422d`, `master` moved to `11d64530`
(pre-round-35 close), `receipts/06-control-stale-master.log`:

```
rc=1
TIP commit=8c7422d7a646515d80af44844e8ecc8a1fc1d30a control=…/ctl-stale dirty=0
R34-D2 status=closed observed=fail agree=NO committed_mirror_paths=109413 …
R35-D3 status=closed observed=fail agree=NO committed_nested_wave_paths=102164 …
rows=9 closed=9 observed_pass=7 mismatches=2
```

`109413` is the mirror-path count **at `11d64530`** and `0` at `8c7422d` in the same clone
(`git ls-tree -r --name-only 11d64530 -- <three roots> | wc -l` → `109413`; `… HEAD -- <same>` → `0`), so
the rows observed the stale ref, not the named tip. The output contains **zero** provenance for it: no
`REF BIND` line, and `grep -c '11d64530[0-9a-f]*'` over the receipt → nothing. Same class as the D4 harm
(`agree=NO` at exit 1 from a healthy tree), reached without touching the tree — only a ref.

Same shape, defaults, silent green — mandated clone (`HEAD=8c7422d`, `master=1fa7af45`), `receipts/16`:
rc=0, `rows=9 … mismatches=0`, `agree=NO` count 0, and no line naming `1fa7af45`. There the wrong-tree read
is unobservable because the pinned inputs are identical in both commits
(`git diff --stat 8c7422d 1fa7af45 -- SCORECARD.md corpus/defects*.jsonl .ufo/waves/round-34
corpus/evidence/round36 plans/defect_ledger.py plans/round36_c1_verify.py` → empty; correction lines 1 and 1;
nested-wave counts 0 and 0), so a receipt from this shape is green **and** unpinned to the commit it names.
[INFERENCE] in the green case the pins read `1fa7af45`: the ref resolves, so line 145 skips binding, and the
red case above shows an unbound ref is read as-is.

Why it matters: `SKILL.md:581` states `0` = "every closed ledger row's check passes **at the tip**", and
`--lane` is the documented control mode. The wave-1 report's §5 limit 1 names this as hypothetical
("if a clone *does* carry `refs/heads/master` pointing elsewhere"); it is not hypothetical — the fleet's own
clone rule manufactures the state on every seat. Bounded: clone mode (the mode that writes the receipts the
row is judged on) is safe, because `git clone` of a detached source creates no local branch — measured, not
assumed (`for-each-ref refs/heads | wc -l` = 0 in `w1`, `w13`).
Fix direction (not applied — leaf seat): bind when `git rev-parse <ref>` ≠ the audited tip, or print
`ref=<ref> rev=<resolved>` for every pin ref in both modes.

### F2 — real, low: a refusal raised mid-ledger prints ledger statements, including a false `agree=NO`

The docstring promises a refusal means "no ledger statement is made" and prints "exactly one `REFUSE` line
and no summary line". A `CalledProcessError` from the **second** ledger's check body fires after the first
ledger's table is already on stdout. `receipts/17-cpe-refusal.log` (control mode, detached clone, one
hostile-but-legal env var `GIT_INDEX_FILE=/nonexistent-dir/x`):

```
TIP commit=8c7422d… control=…/det dirty=10757
R34-D1 status=closed observed=fail agree=NO untracked=198 …
… LEDGER corpus/defects.jsonl rows=5 closed=5 observed_pass=4 mismatches=1
REFUSE check r35_d1 could not query …: Command '[…, 'add', '-A']' returned non-zero exit status 128.
rc=2
```

Six ledger statements and one `agree=NO` are printed before the refusal; the summary line is correctly
absent. Mechanism confirmed: with an unreadable index `git status --porcelain` and `git ls-files --others`
exit **0** with a wrong answer (`10757` and `10744` lines repo-wide, `198` under the round-34 paths), so no
`CalledProcessError` fires for them — the fix's reclassification only covers the raising case, and a
silently wrong git answer still reds a row (`agree=NO` for a tree that is green under a normal env:
`0` untracked for the same paths). Reachable only with a broken git env, so low.

### F3 — confirmed, not a defect: the wave-1 "no new output in normal clones" claim

Normal-clone output of the pre-fix and fixed bodies at `8c7422d` is byte-identical after path normalisation
(§3 table, `diff` empty, `NORMAL_CLONE_OUTPUT_BYTE_IDENTICAL_PREFIX_VS_FIXED`), and the detached output
differs from it by exactly the one `REF BIND` line (§2). Also confirmed: the binding reaches exactly the two
bodies that use `BRANCH` and no others (`grep -n BRANCH` → `defect_ledger.py:29,51`,
`round36_c1_verify.py:38,293`; the other seven checks never read the global), and the driver writes nothing
into the clone it evaluates (`git -C $S/{w1,w2,w3,w6}/lane status --porcelain` → 0 lines each).

## 6. Limits named now

- I verified the D4 mechanism and its exit contract; I did **not** re-adjudicate whether each ledger row's
  claim is true, nor re-run the round-38 C1/C2 counters (main's gate).
- F1 is demonstrated in control mode and shown **unreachable** through the driver's own clone mode; I did
  not test a source whose `HEAD` is a symref to a branch other than the audited commit with an additional
  local `master` — the `audit`-branch shape (receipt 15) covers the realistic variant.
- The binding is a module-global mutation (`setattr(mod, "BRANCH", …)`), so it depends on the frozen bodies
  continuing to read `BRANCH` at call time; a body switching to an env var or another constant would
  regress to D4 without any receipt changing. Nothing in the driver asserts that the rewrite took effect
  beyond the printed line.
- F2's trigger needs a broken git environment; I did not look for a non-env trigger.

## 7. Receipts

`.ufo/waves/round-38/falsify/F38LedgerTip/`: `01-detached-source.log`, `02-normal-clone.log`,
`03-detached-with-stale-master.log`, `04-refuse-reuse.log`, `05-refuse-nonrepo.log`,
`06-control-stale-master.log`, `07-control-planted-red.log`, `08-relative-source.log`,
`09-prefix-detached.log`, `10-prefix-normal.log`, `11-lane-tip-normal.log`, `12-control-detached.log`,
`13-usage.log`, `14-old-tree-missing-module.log`, `15-branch-source-diverged-master.log`,
`16-control-mandated-shape.log`, `17-cpe-refusal.log`, `18-missing-ledger.log`,
`19-mandated-clone-as-source.log`. Relative `--source .` from the detached clone also passes
(`08`: rc=0, `REF BIND … source_ref=absent`, `mismatches=0`). Scratch removed.

VERDICT: ledger-tip-detached-ok
