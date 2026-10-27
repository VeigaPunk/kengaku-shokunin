# R44BatU9b — C1 battery44 module for frozen mutant U9

Seat: R44BatU9b (executor, leaf). Wave: kengaku round 44 (build + attack, v2).
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (read-only for this seat).
Clone: `git clone -q --shared <lane> /fast/scratch/hyaku/kengaku-r44/R44BatU9b/lane`, verified
`git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r44/R44BatU9b/lane`, tip
`5e3d3aa06c6b7000929ac3e62563a39159c4501f`. Every `git` call named `-C "$S/lane"` or `-C <fixture>`; nothing
committed anywhere; nothing written in the lane.
Host: Python 3.14.8, git 2.56.0, `bwrap` envelope for every counter run (all runs show
`local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`, so every measurement below is valid
under the round-44 envelope).
No tool installed, upgraded or removed (nothing was needed; `pacman` untouched).

## The mutant this module prices

Frozen definition, `plans/round44_c1_verify.py` MUTANTS row U9 (`tool=anchor`, class `-`, direction
`rc-mirror`, `adv_kind=direct`), advertised sentence
`plans/anchor_digest_check.py:106-107` — “lessons are read from the working tree for paths committed at HEAD, so a
seat's erratum counts before it is committed”:

```
old: f.read_text(encoding="utf-8", errors="replace")
new: git(lane, "show", "HEAD:" + p).decode("utf-8", "replace")
```

The replaced line is `plans/anchor_digest_check.py:384`, inside `load_errata()`; verified `src.count(old) == 1`
(so the counter admits the mutant, and the traced span is exactly `L384`). Direction `rc-mirror` therefore means:
the unmodified tool **accepts** the fixture (exit 0) and the mutant **rejects** it (exit 1).

## Module

`.ufo/waves/round-44/wave/R44BatU9b/battery/u9_worktree_b.py` — 6495 bytes,
sha256 `f1a14b5f0a8e24c512f645cfc3e6d5bd325e75efc9adf19a9c40db95e78aed6c`. stdlib only (`hashlib`), no lane
clone, no path outside its own build dir, `FIXTURES` = 3 entries, every fid prefixed `u9_worktree_b-`, one
comment line per fixture. Sidechannel scan over the module text (the counter's own `SIDECHANNEL` tuple,
case-insensitive, comments and strings included): **0 hits** — confirmed independently with the same tuple, and by
the counter's own `BATTERY ... sidechannel=0`.

Each fixture is an ordinary repository built from nothing (one or two commits, evidence captures committed at
HEAD, a census-shaped `corpus/SOURCES.md` whose row carries a stale 64-hex anchor token, and a committed
`corpus/lessons/*.md` whose **HEAD text is not the text that exempts that row**). The unmodified tool reads the
working tree, finds the erratum, exempts the row and prints no defect; a tool that reads HEAD finds no usable
erratum and rejects the same tree.

| fid | shape | reference | mutant |
|---|---|---|---|
| `u9_worktree_b-registry-erratum-appended` | four-row registry, two captures, one capture also named by a row with no claim; the erratum is **appended** to a committed lessons file and never committed (row-path binding, no manifest) | rc 0, `defects=0`, `EXEMPT S104` | rc 1, `class=digest-unknown` |
| `u9_worktree_b-erratum-retargeted-history` | **two commits** (S211 registered after the row it names), one capture bound through `SHA256SUMS`; a second, unchanged lessons file next to the one that changes; HEAD's erratum names S211, the working tree **retargets the same line** at S210 with S210's exact stale token | rc 0, `defects=0`, `EXEMPT S210` | rc 1, `class=digest-unknown` (HEAD erratum still names S211, `cited_wrong=[]`) |
| `u9_worktree_b-erratum-completed-in-place` | second trigger of the same branch: HEAD's erratum carries **only** the stale token; the working tree **completes it in place** with the correction token | rc 0, `defects=0`, `EXEMPT S310` | rc 1, `class=erratum-incomplete` **and** `class=digest-unknown` |

`defects: []` and `expect: "accept"` in every entry — the exact class set and exit code the UNMODIFIED tool
prints, which the counter re-measured (`FIXTURE ... ok`, below). Full per-fixture ref-vs-mutant text (including the
`DEFECT` lines): `ref-vs-mutant-per-fixture.txt`.

## Measured kill (task command, exactly)

```
envelope.sh "$S/env" python3 plans/round44_c1_verify.py --lane "$S/lane" \
  --battery-dir .ufo/waves/round-44/wave/R44BatU9b/battery --only U9 --work "$S/w"
ENVELOPE start 20:33:50 cwd=/fast/scratch/hyaku/kengaku-r44/R44BatU9b
PINS total=2 mismatched=0
FIXTURE u9_worktree_b-registry-erratum-appended tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u9_worktree_b-erratum-retargeted-history tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE u9_worktree_b-erratum-completed-in-place tool=anchor expect=accept declared=- observed_rc=0 observed=- ok
MUTANT U9 anchor rc-mirror killed by=u9_worktree_b-registry-erratum-appended attributed=L384 value=differs hits=3
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=1/1 order=0/0
ADVERTISED direct=1 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 20:33:52 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Receipt: `dev-u9-only.txt`. All three fixtures pass the reference measurement (`wrong=0`), the null re-run is
identical (`null_detected=0`), no fixture tree changed during the run (`tampered=0`), and `hits=3`: every fixture
exhibits the declared direction on its own.

## Load-bearing table (remove each fixture in turn)

Variants are copies of the module with one entry removed, each in its own envelope, `--only U9`; receipts in
`load-bearing.txt`.

| variant | U9 killed? | by= | attributed | value |
|---|---|---|---|---|
| drop `registry-erratum-appended` (2 left) | yes | `u9_worktree_b-erratum-retargeted-history` | L384 | differs |
| drop `erratum-retargeted-history` (2 left) | yes | `u9_worktree_b-registry-erratum-appended` | L384 | differs |
| drop `erratum-completed-in-place` (2 left) | yes | `u9_worktree_b-registry-erratum-appended` | L384 | differs |

No single fixture is load-bearing **to the exclusion of the others** — the kill is redundantly triple-covered.
Each fixture was also shown **sufficient alone** (three solo batteries of one fixture each):

| solo battery | U9 killed? | by= | attributed | value |
|---|---|---|---|---|
| `registry-erratum-appended` only | yes | `u9_worktree_b-registry-erratum-appended` | L384 | differs |
| `erratum-retargeted-history` only | yes | `u9_worktree_b-erratum-retargeted-history` | L384 | differs |
| `erratum-completed-in-place` only | yes | `u9_worktree_b-erratum-completed-in-place` | L384 | differs |

## Full default counter, module installed in `plans/battery44/` of the clone

`cp <module> "$S/lane/plans/battery44/"` then, with no `--only` / `--battery-dir`:
`python3 plans/round44_c1_verify.py --lane "$S/lane" --work "$S/w2"` (receipt `full-default.txt`)

```
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANT U9 anchor rc-mirror killed by=u9_worktree_b-registry-erratum-appended attributed=L384 value=differs hits=3
MUTANT U5 anchor silence SURVIVED exhibits=none
MUTANT U6 anchor silence SURVIVED exhibits=none
MUTANT U7 anchor rc-mirror SURVIVED exhibits=none
MUTANT U14c order error SURVIVED exhibits=none
MUTANTS total=5 killed=1 survived=4 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=1/4 order=0/1
PREDICATE C1 fail            (exit 1)
ENVELOPE end 20:34:46 exit=1 ... unchanged
```

U5, U6, U7 and U14c surviving is expected: this module prices U9 only; their fixtures are other seats' wave
items. `PREDICATE C1 fail` here is the honest reading of a one-module battery at integration time, not a defect
of this module.

## Independence

This module never imports, copies, reads or names `.ufo/waves/round-44/claims/witness/` (or any other battery
module); it has no file access at build time except `ctx` writes under its own fixture dir, and every repository,
capture and lessons file is written from bytes defined in the module. The three shapes above (appended-uncommitted,
retargeted-over-two-commits, completed-in-place) were designed from the frozen tool source
(`load_errata`, `anchor_digest_check.py:374-392`; `LESSONS` is read only there, at :377) — not from any witness fixture, which this seat did not read.
A second, independent U9 module is expected from another seat; nothing here coordinates with it.

## Limits

1. **One branch, three triggers.** All three fixtures reach U9 through `load_errata` → the erratum exemption. A
   working-tree lessons edit that changes the verdict by some other route is not exercised, because none exists in
   this tool: `load_errata` is the only reader of `corpus/lessons/`.
2. **Only the accept→reject half.** Every fixture is `expect: accept` (reference rc 0, mutant 1) — the declared
   direction. A working-tree erratum that *introduces* a defect (ref rc 1, mutant 0, i.e. `rc-silence`) is
   reachable for the same span but deliberately not built: it would not price the declared direction.
3. **Site record relies on the `text` local.** Leg g passes because `text` differs between the working tree and
   HEAD; a mutant that reached the same `text` by another route (e.g. reading the working tree through git) would
   produce an equal site record and stay unattributed. The frozen replacement does not, and `value=differs`.
4. **Small registries.** Fixtures carry 1–4 rows and 1–2 captures, not the lane's 109 rows; they were chosen so the
   *only* defect source is the erratum, which keeps `defects: []` exact and the verdict unambiguous. Voting between
   several errata, two errata for one row, or an erratum whose row is unbound are not covered.
5. **Two commits maximum.** The "history" shape is a two-commit repo; deeper history adds nothing to
   `git show HEAD:<path>`.
6. **Host stand-ins.** Measurements are on this host's Python 3.14.8 / git 2.56.0 under the round-44 envelope; the
   counter's own sandbox (not the lane's CI) is what these numbers mean.
7. **Deleting the clones.** The load-bearing variants and the built fixtures lived only in scratch and were removed
   with `plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r44 R44BatU9b <dir>`
   (`DELETE ... bytes=537716659 size=512.8MiB`); the receipts in this directory are the residue.

## Files

- `.ufo/waves/round-44/wave/R44BatU9b/battery/u9_worktree_b.py` (the module; to be moved to `plans/battery44/` by the L1)
- `.ufo/waves/round-44/wave/R44BatU9b/dev-u9-only.txt`
- `.ufo/waves/round-44/wave/R44BatU9b/load-bearing.txt`
- `.ufo/waves/round-44/wave/R44BatU9b/full-default.txt`
- `.ufo/waves/round-44/wave/R44BatU9b/ref-vs-mutant-per-fixture.txt`
- this report

No lane file was edited; no clone, corpus or plans tree was copied into the wave dir; no receipt exceeds 1 MiB.

VERDICT: battery44-u9_worktree_b-U9-killed-yes-fixtures-3
