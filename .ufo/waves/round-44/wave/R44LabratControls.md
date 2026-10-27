# R44LabratControls — C1 freeze control re-derivation on a clean `--no-local` clone (round 44, wave item)

Seat: R44LabratControls (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scratch: `/fast/scratch/hyaku/kengaku-r44/R44LabratControls` (deleted at the end of this seat).
No lane file was written; no counter, tool, spec, gate, receipt, capture or `claims/` file was modified.

## Axes (godspeed)

1. **Reproducibility** — do the 14 committed `claims/control-c1-*.txt` receipts re-derive, byte for byte on their
   verdict lines, from a clone of the freeze commit? (the seat's falsifiable hypothesis)
2. **Independence of the clone** — the clone must not share objects, alternates or hardlinks with the lane, so a
   re-derivation cannot succeed because it read the lane's live state.
3. **Comparator discrimination** — a pass is only meaningful if the diff harness fails on a perturbed receipt.
4. **Envelope validity** — the Q32 digest must be `unchanged` on every run, and must equal the freeze's digest
   (no PATH-dir drift since the freeze).

## 0. Freeze provenance (verified, not assumed)

```
$ git -C <lane> log --oneline -3
5e3d3aa round-44: v2 wave spec + validated dispatch (68 seats)
45dc0bc round-44: first recorded feal-linear probe run (14 cases, mismatches=0)
5f16ed0 round-44: freeze C1 (5 u-row mutants, fences F1-F6) and C2 (TB2 feal-linear-cryptanalysis, V11 predictor) with controls; round-43 wave control residue (closure R3)
```

`claims/frozen-digests.txt` re-checked against the clone's own files at 5f16ed0 (`sha256sum … | diff -`):

```
<12 digest lines>  -> FROZEN-DIGESTS-MATCH
```

and the four tools the controls execute are identical lane↔clone:

```
anchor_digest_check.py lane=11bb2cad…4c2 clone=11bb2cad…4c2 SAME
order_check.py         lane=948d5e1d…6cc clone=948d5e1d…6cc SAME
round44_c1_verify.py   lane=6cf05323…8ad clone=6cf05323…8ad SAME
round43_c1_verify.py   lane=1a1cd1f8…cca clone=1a1cd1f8…cca SAME
```

`diff -rq <lane>/.ufo/waves/round-44/claims <clone>/.ufo/waves/round-44/claims` → no differences (`claims-diff-rc=0`),
so the committed receipts I diff against are the freeze's own, and no receipt has drifted since.

## 1. Clone

```
$ git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin \
      /fast/scratch/hyaku/kengaku-r44/R44LabratControls/lane
$ git -C "$S/lane" checkout -q 5f16ed04b04a80a17a5a1a060c12093d9a152a64
$ git -C "$S/lane" rev-parse --show-toplevel
/fast/scratch/hyaku/kengaku-r44/R44LabratControls/lane
$ git -C "$S/lane" rev-parse HEAD
5f16ed04b04a80a17a5a1a060c12093d9a152a64
alternates: ABSENT
clone pack=…/.git/objects/pack/pack-85dfa60c….pack inode=1619838694 links=1
clone size=50M
```

`--no-local` (a real object copy, not a hardlink farm), no `objects/info/alternates`, `links=1`. The driver asserts
toplevel and HEAD before running anything; the lane was only read.

## 2. Method

`replay.sh` (receipt, sha256 `84319736…`) is `.ufo/waves/round-44/claims/c1_controls.sh` with exactly three changes:
`L` is my clone instead of the lane, `C` is the clone's own `claims/` tree (identical to the lane's), and every
output goes to my scratch (`out2/`, `ctl2/`) instead of `claims/`. Blocks 1–10 and their commands are otherwise the
frozen script's: same `mirror`/`patched` helpers, same `--only` selections, same `head -12` truncation of the
no-mutants diff, same `timeout 60` on the round-43 leg of the hostile block. The primary run used
`cwd=$S/lane` (matching the frozen run's `cwd` semantics: the lane/clone root); an earlier full run from the fleet
root gave the same 14/14 (`compare-out1.txt`, identical sha256 to `compare-out2.txt`).

Every run went through the frozen envelope:
`<clone>/.ufo/waves/round-44/claims/envelope.sh /fast/scratch/hyaku/kengaku-r44/R44LabratControls/ctl2 <cmd…>`
(home read-only, scratch the only writable tree, `~/.cache` overlaid, content digest of `~/.local/bin` before/after).
**20 envelope-wrapped runs, all `unchanged`, none `INVALID`, digest `328be01808ba022f` on both sides of every run —
the same digest the freeze recorded.** (Freeze + this run agree, so the PATH dir has not changed since the freeze.)

Comparison (`compare.py`, sha256 `dbc0eec4…`) normalizes only what cannot reproduce: the envelope command echo
(paths), the `ENVELOPE start/end` timestamps, `cwd=`, the scratch work dir (`<W>`), the clone/lane root (`<L>`),
the random per-fixture-run `k44-c1-<8 chars>` suffix (`k44-c1-RAND`), and the `diff -u` `---`/`+++` header lines.
Everything else — every `PINS`, `FIXTURE`, `MUTANT`, `BATTERY`, `MUTANTS`, `MUTANTS-BY-TOOL`, `ADVERTISED`,
`PINS-AFTER`, `PREDICATE`, `SETUP`, `SIDECHANNEL`, `MODULE`, `DIFF` hunk line, and the envelope exit code and
digest state — is compared byte for byte. Raw (unnormalized) diffs show only those excluded fields differ, e.g.:

```
$ diff <ref> control-c1-nothing.txt     # 3 lines differ, all envelope
1,2c1,2   ENVELOPE /usr/bin/bwrap … ; ENVELOPE start 20:19:34 cwd=<lane>
15c15     ENVELOPE end 20:19:35 exit=1 … 328be01808ba022f … unchanged
          (mine: ENVELOPE end 20:39:… exit=1 … 328be01808ba022f … unchanged)
```

Comparator discrimination (so a 14/14 is not vacuous): perturbing a receipt copy in three different fields —
`ENVELOPE end exit=1`→`exit=0`, `MUTANTS … killed=5 survived=0`→`killed=4 survived=1`, `PREDICATE C1 fail`→`pass`
— was detected in all three (`PERTURBED-DETECTED` ×3), while an untouched receipt stayed `UNTOUCHED-CONFIRMED`.

## 3. Per-control result (14/14 confirmed)

Envelope exit codes and digests are from `out2/` (`ENVELOPE end … exit=N … unchanged`). Key lines are quoted
verbatim from my run and are identical to the committed receipt after the documented normalization.

| # | receipt | exit | key verdict lines (my run = committed) | verdict |
|---|---|---|---|---|
| 1 | `control-c1-nothing.txt` | 1 | `BATTERY fixtures=0 wrong=0 tampered=0 sidechannel=0` · `MUTANTS total=5 killed=0 survived=5 invalid=0 null_detected=0 unattributed=0` · `MUTANTS-BY-TOOL anchor=0/4 order=0/1` · `PREDICATE C1 fail` | **CONFIRMED** |
| 2 | `control-c1-standing-batteries.txt` | 1 | 12 `MODULE` lines · `BATTERY fixtures=71 wrong=0 tampered=0 sidechannel=0` · `MUTANTS total=5 killed=0 survived=5 …` · `PREDICATE C1 fail` | **CONFIRMED** |
| 3 | `control-c1-witness-as-battery.txt` | 0 | `BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0` · `MUTANTS total=5 killed=5 survived=0 invalid=0 null_detected=0 unattributed=0` · `MUTANTS-BY-TOOL anchor=4/4 order=1/1` · `PREDICATE C1 pass` | **CONFIRMED** |
| 4 | `control-c1-no-mutants.txt` | 1 | 12 `DIFF` hunk lines (MUTANTS emptied) · `MUTANTS total=0 killed=0 survived=0 …` · `MUTANTS-BY-TOOL anchor=0/0 order=0/0` · `PREDICATE C1 fail` | **CONFIRMED** |
| 5 | `control-c1-attribution.txt` | 1 | 11 `DIFF` lines (`span = {1}`) · `MUTANT U5 … UNATTRIBUTED … last=span-not-run … span=L1-L1` (×5) · `MUTANTS total=5 killed=0 survived=0 … unattributed=5` · `PREDICATE C1 fail` | **CONFIRMED** |
| 6 | `control-c1-value.txt` | 1 | 10 `DIFF` lines (`SITE_EQUAL … return True`) · `MUTANT U5 … UNATTRIBUTED … last=site-record-equal …` (×5) · `unattributed=5` · `PREDICATE C1 fail` | **CONFIRMED** |
| 7 | `control-c1-tool-edited.txt` | 1 | `PINS total=2 mismatched=1 first=plans/anchor_digest_check.py` · `MUTANT U5/U6/U7/U9 anchor … invalid` · `MUTANT U14c … killed by=u14c-odd-claims-name attributed=L161 value=differs hits=1` · `killed=1 … invalid=4` · `PINS-AFTER mismatched=1` · `PREDICATE C1 fail` | **CONFIRMED** |
| 8 | `control-c1-direction-mislabel.txt` | 1 | 9 `DIFF` lines (U7 `rc-mirror`→`rc-silence`) · `MUTANT U7 anchor rc-silence SURVIVED exhibits=0>1,rc-mirror` · `MUTANTS total=1 killed=0 survived=1 …` · `PREDICATE C1 n/a (non-default battery or mutant subset)` | **CONFIRMED** |
| 9 | `control-c1-hostile-f1.txt` | 1;2 | r43: `FIXTURE f1-gitdir-outside tool=order expect=accept declared=- observed_rc=0 observed=- ok` · r44: `SETUP fixture 'f1-gitdir-outside' … --lane rev-parse --absolute-git-dir=…/side/gitdir is outside the fixture` | **CONFIRMED** (F1) |
| 10 | `control-c1-hostile-f2.txt` | 1;2 | r43: `FIXTURE f2-deep-worktree … observed_rc=2 … ok` · r44: `SETUP … --lane rev-parse --show-toplevel=…/wt is outside the fixture` | **CONFIRMED** (F2) |
| 11 | `control-c1-hostile-f3.txt` | 1;2 | r43: `FIXTURE f3-abbrev-tree-claims … observed_rc=0 observed=- WRONG` · `BATTERY fixtures=1 wrong=1 …` · r44: `SETUP … order argv is not the contract shape ['--lane', '--claims', '--receipt']: ['--lane', …, '--claim', …, '--receip', …]` | **CONFIRMED** (F3) |
| 12 | `control-c1-hostile-f4.txt` | 124;2 | r43: `ENVELOPE end … exit=124 …` (killed by `timeout 60`, no fixture line) · r44: `SETUP fixture 'f4-fifo-include' … --lane git hung` at the 30 s fence | **CONFIRMED** (F4) |
| 13 | `control-c1-hostile-f5.txt` | 1;2 | r43: `FIXTURE f5-alternates-outside … observed_rc=2 … ok` · r44: `SETUP … lane/.git/objects/info/alternates present` | **CONFIRMED** (F5) |
| 14 | `control-c1-hostile-f6.txt` | 1;2 | both: `SIDECHANNEL hb-f6_above/f6_above.py tokens=inspect` · r43: `FIXTURE f6-repo-above-d … observed_rc=2 … ok`, `sidechannel=1` · r44: `SETUP … --lane rev-parse --show-toplevel=…/f6_above is outside the fixture` | **CONFIRMED** (F6) |

Secondary (not a `control-c1-*.txt`, reported because it is the freeze's direction re-derivation):
`witness-run.txt` → `MUTANTS total=5 killed=5 survived=0 invalid=0 null_detected=0 unattributed=0`,
`MUTANTS-BY-TOOL anchor=4/4 order=1/1`, every kill `value=differs`, `PREDICATE C1 n/a (non-default battery or
mutant subset)`, exit 0 — **CONFIRMED** (byte-identical after normalization, same `L522/L539/L384/L161`
attribution lines).

Harness totals, both full runs:

```
$ python3 compare.py out2   ->  14 CONFIRMED, 0 FALSIFIED, REPLAY-CTL 14/14
$ python3 compare.py out    ->  14 CONFIRMED, 0 FALSIFIED, REPLAY-CTL 14/14   (same receipt sha256)
```

## 4. Receipts (this report's subdir; each < 1 MiB)

`out2/`'s 15 receipts copied flat, plus `compare-out1.txt`/`compare-out2.txt`, `replay.sh`, `compare.py`,
`replay.log`, with
`SHA256SUMS`. Notable: `control-c1-nothing.txt 9a8bee93…`, `control-c1-standing-batteries.txt 58178f87…`,
`control-c1-witness-as-battery.txt a3485b80…`, `witness-run.txt 44030bb4…`, `compare-out2.txt c130be9d…`,
`replay.sh 84319736…`, `compare.py dbc0eec4…`. All 20 envelope brackets: `local_bin_content_before=
328be01808ba022f after=328be01808ba022f unchanged`.

## 5. Limits and risks (named, not hidden)

- **This is a re-execution, not a second implementation.** It shows the committed receipts follow from the frozen
  script plus the freeze commit; it cannot detect a control whose *intent* is wrong (e.g. a control that passes for
  the wrong reason). The direction/orientation evidence is exactly the receipts compared here.
- **`control-c1-standing-batteries-six-mutant-draft.txt` was not replayed and is excluded from n=14.** It is a
  pre-freeze draft (header says so) produced by no command in `c1_controls.sh` (six mutants incl. U3); its superseded
  frozen counterpart `control-c1-standing-batteries.txt` reproduces exactly.
- **Excluded from comparison by construction:** envelope timestamps, `cwd`, command echo paths, the random
  `k44-c1-*` run id (it appears inside `SETUP`/`argv` evidence lines), and `diff -u` header lines. Line counts still
  matched exactly for all 14 (e.g. 14/14, 97/97, 20/20, 25/25, 29/29, 9/9, 7/7, 11/11), so no line was dropped or
  added by the replay.
- **Environment identity:** host `python3`/`git`/`gcc` and the same bwrap envelope as the freeze; the freeze's
  digest of `~/.local/bin` is unchanged, so tool drift is not a confound. This says nothing about other hosts.
- **Time behaviour:** the f4 round-43 leg depends on a 60 s wall-clock timeout; it reproduced `exit=124` here but a
  slower/faster host could shift the margin (the round-44 leg's 30 s fence reproduced its refusal in ~32 s wall
  time, which is within a few seconds of the bound).
- No lane, fleet-root, PATH-dir or `$HOME` write occurred; the clone lives only in scratch and was deleted.

## Files changed

None in the lane (read-only throughout). Scratch-only: `replay.sh`, `compare.py`, `out/`, `out2/`, `ctl/`, `ctl2/`,
`out-norm*/`, `sens/`. This report + `.ufo/waves/round-44/wave/R44LabratControls/` receipts are the only lane-tree
writes, both inside the seat's own wave dir.

VERDICT: c1-controls-reproduce-14/14
