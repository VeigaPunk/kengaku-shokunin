# ScribeLesson — draft `corpus/QUALITY.md` criterion Q77 (round 95)

Seat ScribeLesson (leaf scribe). Draft only; the L1 integrates. Nothing in this file is
committed by me. The lane was read-only (`git rev-parse` / `log` / `show` / `cat-file` /
`ls-tree` / `diff` / `merge-base`, plus `git clone --shared` into scratch).

## Proposed text (append after Q76, under a new heading)

```markdown
## Round95 measurement-cwd lesson

- **Q77 — a measurement receipt states the revision it measured, and that revision must resolve as a commit of the lane the receipt claims to measure: a receipt whose stamped HEAD is not an object of that lane was taken in some other tree and is evidence about that tree, never about this lane.** Grounding: `corpus/lessons/round-95.md` Mistakes M1 (the R95-C2 census was launched from a backgrounded `( … ) &` group whose `cd` applied to a sibling only, so the counter ran from the fleet root `/home/vgpnk/Projects/shokunin`, where `plans/round95_false_gate_census.py` does not exist — `python3: can't open file '/home/vgpnk/Projects/shokunin/plans/round95_false_gate_census.py': [Errno 2] No such file or directory`, rc 2) and `corpus/lessons/round-94.md` Mistakes M4 (the same class one round earlier: a backgrounded group whose `cd` applied to a sibling only ran the R94 counter from the fleet root; the round-94 fix asserted the cwd in the receipt but never checked that the asserted revision was the lane's). Executable half: `git -C . cat-file -e <the HEAD the receipt stamps>^{commit}` — exit 0 for `.ufo/waves/round-95/L1/c2-tip.txt` (stamp `afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239`, the lane's T) and exit 128 (`fatal: Not a valid object name`) for `.ufo/waves/round-95/L1/mistake-M1-c2-tip-wrong-cwd.txt` (stamp `9b93fc8fbbdb53221694f1e24d6c1f6044d37d2c`, which is the *fleet root's* HEAD and is not an object of the lane at all).
```

## A dependency the L1 must satisfy

The criterion's `Grounding:` clause cites `corpus/lessons/round-95.md` Mistakes M1, and
**that file does not exist yet** (`ls corpus/lessons/round-95.md` → no such file; the
round's lesson is written at integration, as it was for round 94). The mistake it must
ground on is already recorded and committed — the receipt
`.ufo/waves/round-95/L1/mistake-M1-c2-tip-wrong-cwd.txt`, added at `ea19299d` — and its
error line is exactly what the criterion quotes:

```
python3: can't open file '/home/vgpnk/Projects/shokunin/plans/round95_false_gate_census.py': [Errno 2] No such file or directory
```

So the L1 can land the criterion and the lesson's M1 row together; the criterion is not
landable before the lesson exists, but nothing in it is speculative. **I did not write
`corpus/lessons/round-95.md`** — the lesson is the L1's, and writing it would be
editing a lane file this seat may not edit.

## Why this criterion, in the file's own terms

- It is the second half of the round-94 M4 lesson, which the round-95 M1 shows was
  **incomplete**. Round-94 M4's fix was *"one measurement per command, cwd asserted in the
  receipt"*. The round-95 M1 receipt **does** assert a cwd and a HEAD
  (`cwd /home/vgpnk/Projects/shokunin HEAD 9b93fc8f…`) — the assertion was made, it was
  simply never *checked*. So the criterion Q77 adds is the mechanical half the round-94
  lesson lacked: the asserted revision must be a commit of the lane. The two receipts
  differ in exactly that one property, so the check separates them with no other input.
- It names the evidence by file and by the two stamps, in the shape Q63–Q76 use: a
  `Grounding:` clause pointing at the lesson mistake, then an `Executable half:` clause
  giving the command and the two results it produces.
- It is falsifiable and it binds the next round. A receipt stamped with a revision the
  lane cannot resolve fails; a receipt stamped with a lane revision passes. Neither
  outcome depends on the reader's trust in the receipt's prose.

## Formatting check against the file's existing style

- Q75 and Q76 are one-line bullets under a `## RoundNN … lesson` heading; each starts
  `- **QNN — <statement>.** Grounding: <file> <section> (<why>). Executable half: <command>
  …`. The draft above has exactly that shape and the same three-part order.
- The file's last heading is `## Round94 freeze-integrity-counter lesson`
  (`corpus/QUALITY.md:1388`), whose last bullet is Q76 (`corpus/QUALITY.md:1390`, the file's
  last line). The draft adds `## Round95 measurement-cwd lesson` after Q76, so the
  numbering continues Q77 with no gap and no reuse.
- Q77 is free: `grep -rn "Q77" corpus/QUALITY.md` returns nothing (the `Q77` hits under
  `/home/vgpnk/Projects/shokunin` are other lanes' corpora — `kama-shokunin`,
  `kotoba-shokunin`, `kumitate-shokunin`, `souji-shokunin` — not this lane's file).

## The check, shown able to fail

The check is one `git cat-file -e` per receipt, and the two round-95 receipts differ in
exactly the property it reads. Measured by this seat (`receipts/receipt-revision-stamp-resolves-in-lane.txt`):

| receipt | stamped HEAD | resolves in the lane? |
|---|---|---|
| `.ufo/waves/round-95/L1/c1-tip.txt` | `afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239` | yes (rc 0) |
| `.ufo/waves/round-95/L1/c2-tip.txt` | `afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239` | yes (rc 0) |
| `.ufo/waves/round-95/L1/c2-tip-do-nothing-r94-counter.txt` | `afe9c229e37aecc0b52b78b0e5c7dd80cf0ef239` | yes (rc 0) |
| `.ufo/waves/round-95/L1/mistake-M1-c2-tip-wrong-cwd.txt` | `9b93fc8fbbdb53221694f1e24d6c1f6044d37d2c` | **no** (rc 128) |

The two stamps are heads of **two different repositories**:

```
lane  /home/vgpnk/Projects/shokunin/kengaku-shokunin : ea19299d8dacb6d024c429c53982fb5a73d50035
fleet /home/vgpnk/Projects/shokunin                  : 9b93fc8fbbdb53221694f1e24d6c1f6044d37d2c
git -C /home/vgpnk/Projects/shokunin cat-file -t 9b93fc8f…  -> commit      (the fleet root's own HEAD)
git -C /home/vgpnk/Projects/shokunin cat-file -t afe9c229…  -> fatal: git cat-file: could not get object info
```

That is the whole defect in one line: the M1 receipt's stamp is a real commit — of the
fleet root, one directory up — and the lane has never heard of it. A receipt can only
misattribute a measurement by stamping a revision the reader cannot resolve, and this
stamp is exactly that.

A runnable form of the check is shipped beside this draft as
`draft-receipt-rev-check.py` (this wave dir). Measured on the two receipts:

```
$ python3 draft-receipt-rev-check.py --lane . --receipt .ufo/waves/round-95/L1/c2-tip.txt
RECEIPT-REV .ufo/waves/round-95/L1/c2-tip.txt head=afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239 verdict=IN-LANE
RECEIPTS total=1 in-lane=1 not-in-lane=0 unstamped=0
PREDICATE RECEIPT-REV pass
rc=0

$ python3 draft-receipt-rev-check.py --lane . --receipt .ufo/waves/round-95/L1/mistake-M1-c2-tip-wrong-cwd.txt
RECEIPT-REV .ufo/waves/round-95/L1/mistake-M1-c2-tip-wrong-cwd.txt head=9b93fc8fbbdb53221694f1e24d6c1f6044d37d2c verdict=NOT-IN-LANE
RECEIPTS total=1 in-lane=0 not-in-lane=1 unstamped=0
PREDICATE RECEIPT-REV fail
rc=1
```

## What the criterion deliberately does NOT say

- It does not say a receipt must carry a stamp. `draft-receipt-rev-check.py` reports a
  receipt with no `HEAD`/`REV` stamp as `UNSTAMPED` and does **not** count it a defect:
  a receipt that asserts no revision misattributes nothing. Over all 9,033 committed
  `.txt`/`.log` files under `.ufo/waves/`, 8,870 carry no stamp at all — the check would
  be a red gate on the lane if it demanded one. The rule is "if you stamp a revision,
  it must be the lane's", not "every receipt must stamp a revision".
- It does not name a *directory* to run from. The round-94 M4 fix's "cwd asserted in the
  receipt" is about the receipt's prose; Q77 is about the receipt's *stamp*, because the
  stamp is the one thing a reader can resolve without trusting the prose.
- It does not repair the round-95 receipt. The M1 receipt is committed evidence of the
  mistake (`ea19299d`), and it stays. Q77 says how a receipt is *read*, not what a
  past receipt must become.

## Honest limits of this draft

- The check is measured on this host with this lane's git object store. It is a
  `git cat-file -e` against the lane the receipt claims to measure; it says nothing
  about whether the *contents* behind that stamp are the ones the receipt describes.
  A receipt can stamp a lane revision and still describe something else — that is what
  the frozen-instruments table and the freeze-integrity gate are for, and Q77 does not
  touch them.
- The 13 other `NOT-IN-LANE` hits in a full `.ufo/waves` scan are round-49 fixture-repo
  receipts (they stamp `REV <sha>` of a **fixture** repository under
  `/fast/scratch/hyaku/kengaku-r49/…/fixture`, not of any lane) and one round-76 receipt
  that stamps a `LANE_TIP` of a revision no longer in the lane's history. Those are
  receipts of *other* trees by construction; the criterion applies them only when they
  are offered as evidence about this lane, and the L1 should scope the gate's
  population accordingly (the round-95 L1 receipt set is the natural scope).
