# F39LedgerTip — `plans/ledger_tip.py` re-run at tip a6832f5 (round 39, wave 2 / FALSIFY)

Seat: F39LedgerTip (executor, leaf). Lane repo: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Tip under test: `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c` (branch `master` at dispatch time;
the lane's `master` has since advanced to `acf4375`, see §2A). Freeze: `088f7c36e94ce2f15e6f9aa0c5a5c5b75a1646c8`.
No lane file was edited; every run below is on a clone in `/fast/scratch/hyaku/kengaku-r39/F39LedgerTip/`
(removed at the end). No build/lint/formatter was run (parent owns the gate).

## 1. Fixture

```
S=/fast/scratch/hyaku/kengaku-r39/F39LedgerTip; mkdir -p "$S"; export TMPDIR="$S"
git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane" \
  && git -C "$S/lane" checkout -q a6832f53c1a94bb092a6cfd79fb4e449f2d4054c
$ git -C "$S/lane" rev-parse --show-toplevel
/fast/scratch/hyaku/kengaku-r39/F39LedgerTip/lane
$ git -C "$S/lane" rev-parse HEAD
a6832f53c1a94bb092a6cfd79fb4e449f2d4054c
$ git -C "$S/lane" status --porcelain | wc -l
0
```

The fixture clone's branch layout is not what the tool assumes:

```
$ git -C "$S/lane" for-each-ref --format='%(refname) %(objectname)'
refs/heads/master                    acf437542b00ae1723eba9dcc79d46af2e40d96e
refs/remotes/origin/HEAD              acf437542b00ae1723eba9dcc79d46af2e40d96e
refs/remotes/origin/master            acf437542b00ae1723eba9dcc79d46af2e40d96e
refs/remotes/origin/hyaku/s3-kengaku-containment 6a2c2df788a4fdb216dd5790f9ae6dd326169f47
refs/remotes/origin/round29/R29ExecCore 31934e5660f1814326c6472eefdfa0c41e642a2f
```

A plain clone of the lane (the fleet fixture recipe: clone + `checkout <sha>`) leaves the clone's
local `refs/heads/master` at the *source's* master, `acf4375` — one commit ahead of the audited tip.
The lane's own worktree is not clean either (read-only check):

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status --porcelain | wc -l
4
   ?? .ufo/waves/round-39/build/R39SourcesRecheck/scipyjson.json
   ?? .ufo/waves/round-39/falsify.ready
   ?? .ufo/waves/round-39/falsify.ready.dispatched
   ?? .ufo/waves/round-39/falsify/
```

## 2. Runs requested by the card

All commands are `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/ledger_tip.py …`
(the landed tip file; nothing edited). Receipts are in
`.ufo/waves/round-39/falsify/F39LedgerTip/`.

| # | shape | command | exit | headline output |
|---|---|---|---|---|
| A | `--lane .` at the tip, plain fixture clone | `--lane "$S/lane"` | 2 | `TIP commit=a6832f5… dirty=0` then `REFUSE stale pin ref: refs/heads/master resolves to acf4375…` |
| B | `--lane` with local master moved to the tip | `git update-ref refs/heads/master $TIP; --lane "$S/lane"` | 0 | `REF AUDIT … state=match`, `rows=9 closed=9 observed_pass=9 mismatches=0` |
| C | `--source <tip clone> --work` | `--source "$S/lane" --work "$S/w-src"` | 0 | `TIP commit=a6832f5… clone=…/w-src/lane`, `REF AUDIT … state=match`, `rows=9 … mismatches=0` |
| D | detached clone, no local branch, `--lane` | `git clone --no-local … && checkout $TIP && branch -D master; --lane "$S/det"` | 0 | `REF BIND ref=refs/heads/master rev=a6832f5… tip=a6832f5… source_ref=absent why=clone-lacks-ref`, `rows=9 … mismatches=0` |
| D2 | detached clone as `--source` | `--source "$S/det" --work "$S/w-det"` | 0 | same `REF BIND … source_ref=absent`, `rows=9 … mismatches=0` |
| E | stale local master (freeze sha) | `git branch -f master $FREEZE; --lane "$S/stale"` | 2 | `TIP commit=a6832f5…` then `REFUSE stale pin ref: … resolves to 088f7c3…` |
| G | `--source` the live lane (HEAD = master = acf4375) | `--source <lane> --work "$S/w-lane"` | 0 | `TIP commit=acf4375…`, `REF AUDIT … state=match`, `rows=9 … mismatches=0` |
| K | `--work` already holds `lane` | `--source "$S/lane" --work "$S/w-src"` (second time) | 2 | `REFUSE will not reuse …/w-src/lane; remove it first` |
| L | `--lane` on a non-git directory | `--lane "$S/nogit"` | 2 | `REFUSE …/nogit is not a readable git work tree` |

Verbatim B (the canonical clean run at the tip):

```
TIP commit=a6832f53c1a94bb092a6cfd79fb4e449f2d4054c control=/fast/scratch/hyaku/kengaku-r39/F39LedgerTip/lane dirty=0
REF AUDIT ref=refs/heads/master rev=a6832f53c1a94bb092a6cfd79fb4e449f2d4054c tip=a6832f53c1a94bb092a6cfd79fb4e449f2d4054c state=match
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
exit=0
```

The published landing measurement ran the same script at the *parent* commit and got the same
summary (`measure-final.txt:600-616`: `TIP commit=34158b0…`, `rows=9 … mismatches=0`, `exit=0`).

### 2.1 Refusal buffering (the round-38 F2 / round-39 R5b fix) is real

```
$ printf 'not json\n' > "$S/buf/corpus/defects-round35.jsonl"        # second ledger, after 5 rows would print
$ python3 plans/ledger_tip.py --lane "$S/buf"
TIP commit=a6832f53… control=…/buf dirty=1
REF AUDIT ref=refs/heads/master rev=a6832f5… tip=a6832f5… state=match
REFUSE cannot read corpus/defects-round35.jsonl: JSONDecodeError: Expecting value: line 1 column 1 (char 0)
exit=2
```

Same tree, freeze-version script (`git show 088f7c3:plans/ledger_tip.py`), exits 2 but **prints the
already-evaluated ledger statements first** (`R34-D1 … LEDGER corpus/defects.jsonl rows=5 …`).
So the buffering change is measured, not asserted.

## 3. Diff vs freeze `088f7c3`

`git diff 088f7c3 a6832f5 -- plans/ledger_tip.py` → `1 file changed, 56 insertions(+), 31 deletions(-)`
(single commit `34158b0`). Four behaviour changes, one rename:

1. docstring: "Detached-clone refs" section replaced by a "Ref provenance" section that adds the
   `REF AUDIT` line, a `tip=` field on `REF BIND`, and the stale-ref refusal contract;
2. `bind_pin_refs` → `audit_pin_refs`, which now `REFUSE`s a ref resolving to anything but the
   commit under audit (exit 2, before any ledger statement) and prints `REF AUDIT … state=match`
   when it matches (`plans/ledger_tip.py:159-170`);
3. one `statements` list buffers every row and per-ledger line until all ledgers are evaluated, so a
   refusal leaves no ledger statement (`plans/ledger_tip.py:208`, `:247-248`);
4. the summary/exit contract is untouched (`return 0 if (rows and mism == 0) else 1`).

No change to row evaluation, to `KIND`, to `clone_lane`, or to which tree the non-ref checks read.
Differential between the two scripts on one detached source (clone mode) is one line:
`< REF BIND ref=… rev=… source_ref=absent why=clone-lacks-ref` vs
`> REF BIND ref=… rev=… tip=… source_ref=absent why=clone-lacks-ref`.

## 4. Does it print which revision it audits?

**Yes, in every mode that evaluates a tree — with one qualification that is defect D2 below.**

- clone mode: `TIP commit=<40-hex> clone=<path>` is the first line (`plans/ledger_tip.py:203`);
- control mode: `TIP commit=<40-hex> control=<path> dirty=<n>` (`plans/ledger_tip.py:194`);
- every ref a check body names is then resolved and printed once: `REF AUDIT ref=… rev=… tip=… state=match`
  or `REF BIND ref=… rev=… tip=… source_ref=<sha|absent> why=clone-lacks-ref`, and the module's
  `BRANCH` is set to that sha, so `ls-tree` in the check bodies reads the printed commit
  (`plans/defect_ledger.py:51`, `plans/round36_c1_verify.py:293`);
- refusals carry both revisions in their single line: `… resolves to 088f7c3… but the commit under
  audit is a6832f5…`;
- usage/clone refusals (K, L) print no revision, but no tree is evaluated either.

Refs really are bound: `grep -n 'refs/heads/master' plans/` finds only the two `BRANCH =` constants
plus two round-26/27 census scripts, so the `BRANCH` binding covers every ref a check body names.
Measured consequence: on a tree at the tip with `master` at the freeze sha, the tip script refuses
(exit 2) whereas the freeze script reads the stale ref silently and still prints
`rows=9 closed=9 observed_pass=9 mismatches=0` (receipt Q) — the pin paths happen not to differ
between those two commits, so the guard is conservative here, not observably load-bearing.

## 5. Defects

### D1 (moderate) — in the mandated clone mode two `kind=live` rows cannot fail, and the log does not say so

`clone_lane` refuses a clone that is not clean (`plans/ledger_tip.py:135-136`), and `git clone` only
copies committed bytes; a worktree-level "nothing untracked" query therefore always observes zero in
that mode. `R34-D1` is *entirely* that query (`git ls-files --others … .ufo/waves/round-34/` plus three
plan-tool paths, `plans/defect_ledger.py:37-45`); `R35-D2` is that query over the whole lane plus six
line fixtures (`plans/round36_c1_verify.py:277-290`). Both are labelled `live`, described as
"a repo-state query with a zero-tolerance observation" (`plans/ledger_tip.py:14`, `:79`, `:85`), and on
pass the note that carries the observed number is suppressed (`tail = note if (a.keep_notes or not ok) else ""`,
`:241`) — so the log shows `observed=pass agree=yes` with no evidence at all.

Receipt (one untracked file under a round-34 path, worktree only):

```
$ printf 'leftover\n' > "$S/dirty2/.ufo/waves/round-34/build/stray.txt"
$ python3 plans/ledger_tip.py --lane "$S/dirty2"          # control mode sees it
R34-D1 status=closed observed=fail agree=NO untracked=1 ledger=corpus/defects.jsonl kind=live
LEDGER corpus/defects-round35.jsonl rows=4 closed=4 observed_pass=2 mismatches=2
rows=9 closed=9 observed_pass=6 mismatches=3          exit=1
$ python3 plans/ledger_tip.py --source "$S/dirty2" --work "$S/w-dirty2"   # same tree as source
R34-D1 status=closed observed=pass agree=yes …
rows=9 closed=9 observed_pass=9 mismatches=0          exit=0
$ git -C "$S/w-dirty2/lane" ls-files --others --exclude-standard -- .ufo/waves/round-34/ | wc -l
0
```

This is not hypothetical for the lane today: `git status --porcelain` on the lane shows **4**
untracked entries (§1), so the row `R35-D2` ("whole-lane untracked set") is false in control mode
while the clone-mode log — the shape the registry row prescribes — prints it `observed=pass agree=yes`
and the summary `mismatches=0`. The SKILL.md row reads `0` "every closed ledger row's check passes at
the tip" (`SKILL.md:581`); in this mode one closed row's check cannot fail and a second cannot
observe the class it names. The wave-1 diff neither introduced nor addressed this.

Minimal honest fixes (not applied — lane is read-only for this seat): evaluate the worktree rows against
`--source` when it is supplied and print the two observation values, or mark those rows
`kind=pin`-like in the clone mode and print `untracked_anywhere=<n>` on pass too.

### D2 (low) — control mode names a commit that the row set and live inputs need not come from

The header prints `TIP commit=<sha>`, but in control mode the ledger row *set* is read from the
worktree (`p = lane / ledger_rel; ledger = [json.loads(l) …]`, `plans/ledger_tip.py:213`), the live
checks read worktree bytes, and only the pin checks read `<sha>`. Flipping one row's declared status
inside the worktree changes the printed row set while the header still names the commit:

```
$ # corpus/defects.jsonl: R34-D1 "status": "closed" -> "open"   (worktree only)
$ python3 plans/ledger_tip.py --lane "$S/dirty"
TIP commit=a6832f53c1a94bb092a6cfd79fb4e449f2d4054c control=…/dirty dirty=1
R34-D1 status=open observed=pass agree=NO ledger=corpus/defects.jsonl kind=live
rows=9 closed=8 observed_pass=9 mismatches=1          exit=1
```

`dirty=1` is the sole signal; no path list, no worktree digest, and the docstring's
"the printed provenance is the whole story" (`plans/ledger_tip.py:52`) is false for this mode.
The control mode itself is deliberate ("a deliberately broken clone can be used to show each check
still bites", `:62`), so this is a disclosure gap in the output, not a wrong verdict. The sentence at
`:52` should be scoped to clone mode, or `--lane` should print `dirty=<n> paths=…`/a worktree hash.

## 6. Residuals (measured, not counted)

- **R1 ordering.** `TIP commit=` is a stdout `print`, `REFUSE` goes to stderr. With the fleet habit
  `> log 2>&1` and default buffering the merged file shows `REFUSE …` *before* `TIP commit=…`
  (receipt S; with `PYTHONUNBUFFERED=1`, as in this shell, the order is TIP then REFUSE). No
  information is lost (the refusal names both shas), but "The `TIP commit=` line is printed first"
  (`plans/ledger_tip.py:49-50`) is only true of the unbuffered stream.
- **R2 shared clone is not self-contained.** The clone is created with `--shared`
  (`plans/ledger_tip.py:121`), so its object store is an alternate pointing at the source; the
  docstring says the clone is "left in place for inspection" (`:58-59`). Measured: after moving the
  source aside, `git -C <clone> log` fails with `fatal: bad object HEAD` (receipt P). Harmless when
  `--source` is the persistent lane and the clone lives in scratch, fatal for a kept-for-inspection
  clone of a scratch source.
- **R3 stale-ref guard is conservative.** On the measured pair (tip `a6832f5` with `master` at freeze
  `088f7c3`) the pin paths are identical, so the refused run would have produced the same
  `rows=9 … mismatches=0` (receipt Q). The guard costs a refusal where the answer was unaffected;
  it still names both revisions and the remedy.
- **R4 `--source` audits whatever the source's HEAD is**, not a revision argument: with the lane now
  at `acf4375`, `--source <lane>` prints `TIP commit=acf4375…` and passes (receipt G). Correct by
  contract, but a caller expecting "the tip this round measured" must check the printed sha.

## 7. Result

No lane change; the tool is operable in all four requested shapes and prints the revision it audits
(TIP line + one `REF AUDIT`/`REF BIND` per named ref, rev bound into the check body), the stale-ref
refusal and the statement buffering both bite on measured fixtures, and the clone-mode pass at
`a6832f5` reproduces the landing measurement (`rows=9 closed=9 observed_pass=9 mismatches=0`, exit 0).
Two defects remain: D1 (two live rows are unsatisfiable in the prescribed clone mode, one of them
false for the lane as it stands) and D2 (control-mode header names a commit the row set is not taken
from). Parent should run the integration gate; this seat ran no build, lint, test or formatter.

Exact receipts in `.ufo/waves/round-39/falsify/F39LedgerTip/`:
`A-lane-tip.log`, `B-lane-master-tip.log`, `C-source-work.log`, `D-lane-detached.log`,
`D2-source-detached.log`, `E-stale-freeze-master.log`, `F-buffer-refuse.log`,
`F-old-freeze-script-same-tree.log`, `G-source-live-lane.log`, `H0-dirty-clean.log`,
`H1-dirty-rowflip.log`, `I-dirty-body.log`, `K-work-reuse.log`, `L-not-a-repo.log`,
`O1-lane-untracked.log`, `O2-source-of-dirty.log`, `P-shared-inspection.log`,
`Q-old-stale-master.log`, `R-old-clone.log`, `R-new-clone.log`,
`S-merged-order-default-buffering.log`.

VERDICT: ledger-tip-2-defects
