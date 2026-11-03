# SweepBuild — R64-C3 trio-sweep instrument (round 64, w1)

Seat: `SweepBuild` (leaf). Lane under test is a **clean clone** of L at freeze commit
`859ac24f41061bffde588b9ed5d5adfea5ca8e27` (base tip `5f517fe7…`), built with
`git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin <scratch>/clone`;
`git -C <clone> rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r64/SweepBuild/clone`
(asserted before any write). No `git add`/`commit`/`checkout`/`reset` was ever run.

## Artifact to land

| source (seat dir) | target (lane) | sha256 |
|---|---|---|
| `.ufo/waves/round-64/w1/SweepBuild/round64_trio_sweep.py` | `plans/round64_trio_sweep.py` | `56638ea1dfc0ca47ee91dfc0afec9c9fcbbefa9b15d3e163ad423b7f8dbf8bb0` |

The seat copy is byte-identical to the clone file the receipts below were produced from
(`shutil.copy2` then sha-reasserted in `make_receipts.py`). Landing is a plain copy; the sha must
not change. **No corpus file was touched** — the addenda belong to the repair seats, and the
red-before receipt below was produced on the clone's untouched tree (0 addendum headings).

## Rule source (imported, not replicated)

`plans/round64_trio_sweep.py` does
`from round63_gate_checks import trio_missing` after inserting its own directory on `sys.path`.
A control printed `trio_missing.__module__=round63_gate_checks same_object=True`, i.e. the sweep
prices exactly the round-63 gate's rule (same keys, same 12-line window, same stop at the first
`## ` heading, same in-order requirement, same duplicate handling). If that import ever fails the
tool exits 2 with `SETUP gate-import-failed` on stderr instead of falling back to a look-alike
rule. Consequence: `plans/round63_gate_checks.py` must stay importable (it is; C2's `_resolves`
patch does not touch `trio_missing`).

## Red-before (receipt `sweep-red-before.txt`)

Command (cwd = clone root):

```
python3 -B plans/round64_trio_sweep.py --sweep --lane /fast/scratch/hyaku/kengaku-r64/SweepBuild/clone
```

Observed stdout:

```
SWEEP files=65 trio_open=36 addendum=0 red=29
RED corpus/knowledge/attrib-prior-art-r21.md        (… 29 RED lines, sorted …)
PREDICATE R64-C3 fail
# exit=1
```

The 29 `RED <path>` lines were diffed against
`corpus/evidence/round64/trio-red-at-base.txt` (sha256
`fe0498fb20b5102b50d80a3eca1258784cdf9d66edf4d9654b10fa99653a080a`, 29 entries, byte-identical
in the clone and in the committed lane copy) → **identical, entry-for-entry** (`diff` empty). The
stderr line records the frozen list actually used:
`INFO frozen-list=… sha256=fe0498fb… entries=29`.

Independently, running the round-63 gate over every entry at base
(`python3 plans/round63_gate_checks.py trio <file>` per file) produced the same 29 paths
(`diff` empty), which is the frozen list's stated provenance.

`--lane .` (the frozen counting-command shape) was also exercised from the clone root; same
`SWEEP files=65 trio_open=36 addendum=0 red=29`, `PREDICATE R64-C3 fail`, exit 1
(receipt `relative-lane.txt`).

## Selftest (receipt `selftest.txt`)

```
python3 -B plans/round64_trio_sweep.py --selftest --work /fast/scratch/hyaku/kengaku-r64/SweepBuild
SELFTEST classify case=RED      got=TRIO-RED      expect=TRIO-RED      ok
SELFTEST classify case=ADDENDUM got=TRIO-ADDENDUM expect=TRIO-ADDENDUM ok
SELFTEST classify case=OPEN     got=TRIO-OPEN     expect=TRIO-OPEN     ok
SELFTEST sweep-base     rc=1 expect=1 red=1 trio_open=1 addendum=1 ok
SELFTEST sweep-repaired rc=0 expect=0 red=0 addendum=2             ok
SELFTEST pass        # exit=0
```

Fixtures are written under `mkdtemp(dir=<work>)` and removed in a `finally`; nothing is written
into the lane. The two sweep legs use a three-file fixture lane and a `--frozen-list` naming only
its red file, so they prove both the graded-fail path and the pass path (including the
`red=0` conditional cross-check) without touching the real frozen list.

## Controls (receipt `controls.txt`, all fixture lanes under scratch)

| control | observed stdout | rc |
|---|---|---|
| frozen list short by one entry | `SETUP frozen-list-mismatch` (+ stderr `DETAIL … extra=<the unlisted red>`) | 2 |
| frozen list with one phantom entry | `SETUP frozen-list-mismatch` (+ `DETAIL … missing=<phantom>`) | 2 |
| simulated after-repair lane (all 29 frozen entries get a round-64 addendum) | `SWEEP files=65 trio_open=36 addendum=29 red=0` … `PREDICATE R64-C3 pass` | 0 |
| partial repair (1 of 29) | `SETUP frozen-list-mismatch` (+ `DETAIL … missing=<repaired entry>`) | 2 |
| knowledge dir emptied | `SETUP frozen-entry-missing` (+ `DETAIL frozen-entries-absent=<29> …`) | 2 |
| after-repair lane minus one frozen entry | `SETUP frozen-entry-missing` (+ `DETAIL frozen-entries-absent=<1> …`) | 2 |

Parity checks against the imported rule: out-of-order trio (`verified-at` before `source`) →
gate fails, sweep `TRIO-RED`; addendum carrying `verified-at: 2026-10-03` → `TRIO-RED` with
`NOTE addendum-incomplete missing=verified-at: 2026-11-03`; duplicate `source:` in canonical
order → gate passes, sweep `TRIO-OPEN` (same semantics).

These controls are the vacuity evidence: the tool cannot pass an empty tree, cannot pass after a
deletion, and cannot be pushed off the frozen population silently.

## Resolutions declared (frozen rule unchanged; these are the reading it is implemented under)

1. **Cross-check is conditional on `red>0`.** The frozen sentences require (a) the after-run to
   print `red=0`/pass and (b) the base red set to equal the frozen 29. Since the frozen list is
   the *base* population, comparing it at a repaired tip would force exit 2 forever. So: while
   red entries exist, red set == frozen list or `SETUP frozen-list-mismatch` exit 2; when
   `red=0` the comparison is vacuous, and instead every frozen entry must still exist as a file
   (`SETUP frozen-entry-missing` otherwise). Both frozen commands therefore run unmodified.
2. **`TRIO-OPEN` wins** over an addendum; an already-open entry is never counted ADDENDUM.
3. **Addendum block:** heading line equal to `## Freshness addendum (round 64)` after `rstrip()`
   (the gate's own heading comparison); block = following lines up to the next `## ` heading or
   EOF; any occurrence of the heading whose block holds a `verified-at:` line whose value starts
   with the date token `2026-11-03` (whitespace/end-bounded, so trailing prose is fine but a
   different date is not) and a `recheck:` line with a non-empty command classifies ADDENDUM.
   Repair seats must **append at EOF or ensure no further `## ` heading intervenes** inside the
   block, or the block ends early and the entry stays RED.
4. **Paths** in the output are lane-relative POSIX (`corpus/knowledge/x.md`), matching the frozen
   list, so `diff` against the receipt is direct.
5. Unreadable lane / knowledge dir / frozen list ⇒ `SETUP …` exit 2, never a vacuous pass.

## Named limitations (reported, not patched)

- ADDENDUM classification prices the *presence and shape* of the `recheck:` command, not its
  outcome; the frozen kill rule has the closure re-run each named command. A command that does
  not re-derive is a fail by that rule, not by this instrument.
- The frozen list is compared **by content**; its bytes are recorded in the red-before receipt
  (and stderr `INFO`) but not pinned as a constant, so a rewritten-but-equal list is tolerated
  and a rewritten-different list is caught by the entry-for-entry comparison. `--frozen-list`
  exists for fixture lanes only.
- The sweep tallies `corpus/knowledge/*.md` only; it does not price `corpus/README.md` index
  parity (predicate part (c), a separate frozen counting command) and does not repair anything.

## Scope attestation

Wrote only `.ufo/waves/round-64/w1/SweepBuild/` (4 receipts + the tool copy) and
`/fast/scratch/hyaku/kengaku-r64/SweepBuild/` (clone, fixture lanes, drivers — removed before
yield). No lane file outside the seat dir, no corpus edit, no fleet-repo write, no
`.ufo/state/`, no `MANIFEST.json`. No pacman, no installs, no network, no port bind, no model
change, no `ask`, no polling, no git mutation.
