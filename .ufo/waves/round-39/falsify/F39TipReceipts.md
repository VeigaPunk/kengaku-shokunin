# F39TipReceipts — `plans/tip_receipts.py` at tip a6832f5 (round 39, wave 2)

Seat: F39TipReceipts (executor, axes: freshness, operability). Lane read-only; all runs in
`/fast/scratch/hyaku/kengaku-r39/F39TipReceipts` (removed at exit). No lane file edited, no git
mutation, no tool installed.

## What was attacked

The registered gate row `SKILL.md:586` claims, in its verdict map: `0` "every committed `probe*`
receipt **with a committed re-run command** is byte-equal at the tip and the tamper control answers
`differ`", population "`corpus/evidence/**/probe*.{txt,log}` at HEAD". The question: does the round-39
receipt `corpus/evidence/round39/git-leak-probe.txt` (probe `plans/git_leak_probe.py`, registry row
`SKILL.md:587`) enter that comparison?

## Setup

```
S=/fast/scratch/hyaku/kengaku-r39/F39TipReceipts; mkdir -p "$S"; export TMPDIR="$S"
git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" checkout -q a6832f53c1a94bb092a6cfd79fb4e449f2d4054c
git -C "$S/lane" rev-parse --show-toplevel   -> /fast/scratch/hyaku/kengaku-r39/F39TipReceipts/lane
git -C "$S/lane" rev-parse HEAD              -> a6832f53c1a94bb092a6cfd79fb4e449f2d4054c
sha256sum plans/tip_receipts.py (clone, tip) -> f2a35b47d9e4d2ce3ec981dbb07a5c968d61d41c207ee32ecef4b9ea1932bcdd
sha256sum plans/tip_receipts.py (lane)       -> f2a35b47…dd (same bytes)
python3 -V -> 3.14.8; /usr/bin/bwrap, /usr/bin/git both executable
```

At lane `HEAD` (`acf4375`, the wave-2 dispatch commit) the tool is byte-identical:
`git diff --stat a6832f5 acf4375 -- plans/tip_receipts.py` → empty. The findings below therefore hold
at the measured tip **and** at the lane head.

## Headline measurement at the tip

```
python3 <clone>/plans/tip_receipts.py --lane <clone> --work $S/tr      # receipt: tip-receipts-run.txt
tip a6832f53c1a94bb092a6cfd79fb4e449f2d4054c
receipt corpus/evidence/round35/tb2-grader-probe.txt  equal bytes=3399 exit=0 …
receipt corpus/evidence/round36/regex-log-probe-first-run.txt skip reason=declared-nonreproducible-absolute-scratch-paths (equal after masking) …
receipt corpus/evidence/round36/regex-log-probe.txt   equal bytes=5907 exit=0 …
receipt corpus/evidence/round37/git-webserver-probe.txt equal bytes=8529 exit=0 …
receipt corpus/evidence/round38/build-pmars-probe.txt equal bytes=5537 exit=0 …
receipt corpus/evidence/round39/git-leak-probe.txt    skip reason=no-committed-re-run-command
control receipt=corpus/evidence/round35/tb2-grader-probe.txt flip=byte 1699 0x27->0x26 verdict=differ
note compared=4 declared_bounded=1 no_command=20
receipts=25 byte_equal=4 differ=0 skipped=21
EXIT=0
```

**Answer to the assigned question: no. `git-leak-probe.txt` is enumerated and then skipped**, with a
reason that is false for it (`no-committed-re-run-command`). Receipts/byte_equal/differ/skipped at the
tip = **25 / 4 / 0 / 21**; exit 0, green.

`--list` (`tip-receipts-list.txt`) shows the mechanism: 5 receipts are mapped by the literal table
`RECEIPTS` (`plans/tip_receipts.py:55-60`), the other 20 — round-39's receipt included — are
`unmapped` (`plans/tip_receipts.py:214-215`) and printed by the `--list`/run branches
(`plans/tip_receipts.py:226`, `:327`).

## F1 — the round-39 receipt has a committed re-run command and reproduces byte-equal; the gate skips it

The tool's own definition of a skip candidate is satisfied, so the printed reason is wrong:

| requirement | evidence |
|---|---|
| committed probe script with a `Run as:` line | `plans/git_leak_probe.py:4` — "python3 plans/git_leak_probe.py --lane . run every frozen case, print the receipt" |
| registry row naming that command | `SKILL.md:587` — "`python3 plans/git_leak_probe.py --lane .`" |
| receipt documents both | `corpus/README.md:475`, `corpus/knowledge/tb2-git-leak-recovery-grader.md:24-25` |
| receipt declared reproducible | `corpus/README.md:475` — "cases=25 observed_pass=13 observed_fail=12 mismatches=0, a second run byte-equal" |

Direct re-run at the tip (`git-leak-rerun.txt`):

```
cd $S/lane && TMPDIR=$S python3 plans/git_leak_probe.py --lane .      -> exit 0 (2.74 s)
sha256(direct re-run)        d7f3a465ccc411572c96fc039235854093d1eb52ccd685b618a28a10de609b5f
sha256(HEAD blob)            d7f3a465ccc411572c96fc039235854093d1eb52ccd685b618a28a10de609b5f
cmp -> identical; 30 lines, 5867 bytes, cases=25, tail: cases=25 observed_pass=13 observed_fail=12 mismatches=0
```

So the gate does not merely defer an unverifiable receipt: it passes while leaving out a receipt that
is verifiably byte-equal at the tip in under three seconds.

## F2 — the one-line mapping that closes it (operability control)

Patched **copy** of the tool in scratch (lane untouched), one dict line added:
`"corpus/evidence/round39/git-leak-probe.txt": ("plans/git_leak_probe.py", "byte")`
(`$S/patched/tip_receipts_map39.py`, sha256 `73c44e09f3a4af2d601e5c327fac07b64d061cbeb494886831f21af87f3fa99f`):

```
python3 tip_receipts_map39.py --lane <clone> --work $S/tr7 --only git-leak \
        --tamper corpus/evidence/round39/git-leak-probe.txt
receipt corpus/evidence/round39/git-leak-probe.txt equal bytes=5867 exit=0 doc=SKILL.md:587+SKILL.md:876
control receipt=corpus/evidence/round39/git-leak-probe.txt flip=byte 2933 0x65->0x64 verdict=differ
note compared=1 declared_bounded=0 no_command=0
receipts=1 byte_equal=1 differ=0 skipped=0
EXIT=0   (3.18 s)
```

Population also names both halves: `provenance` resolves to `SKILL.md:587+SKILL.md:876` — the registry
command and the receipt line — for this receipt, versus `undocumented`-style joins nowhere needed.

**Cost of the omission: 1 table line, ~3 s of runtime.** The gap is not a design limit, it is an
unfilled table.

## F3 — the tamper control is structurally unavailable for the skipped receipt

```
python3 tip_receipts.py --lane <clone> --work $S/tr6 \
        --tamper corpus/evidence/round39/git-leak-probe.txt
SETUP: --tamper corpus/evidence/round39/git-leak-probe.txt is not a mapped receipt
EXIT=2
```

`--tamper` is refused (`plans/tip_receipts.py:303`, `die(... is not a mapped receipt)`), so the
registry row's "the tamper control answers `differ`" is established only for the four mapped receipts
(automatic control this run: byte 1699, `differ`). For the round-39 receipt there is no control at
all — the gate cannot be shown able to go red on it.

## F4 — a filtered run is green having checked nothing about the target

```
python3 tip_receipts.py --lane <clone> --work $S/tr3 --only git-leak        # unpatched
receipt corpus/evidence/round39/git-leak-probe.txt skip reason=no-committed-re-run-command
note compared=0 declared_bounded=0 no_command=1
receipts=1 byte_equal=0 differ=0 skipped=1
EXIT=0

python3 tip_receipts.py --lane <clone> --work $S/tr4 --only zzzz
note compared=0 declared_bounded=0 no_command=0
receipts=0 byte_equal=0 differ=0 skipped=0
EXIT=0
```

`skipped=21` in the headline conflates "no command" (20) with "declared bounded" (1), and `exit 0`
makes an all-skip run indistinguishable from an all-equal one. Round-38 reported the same class
(F38TipReceipts F4/F5, `.ufo/waves/round-39/build/R39R38Integrate/dispositions.md:209-210`); the
behaviour is unchanged at this tip.

## F5 — freshness: this is round-38's F1 recurring, not a new surprise

`.ufo/waves/round-39/build/R39R38Integrate/dispositions.md:206`:
"F38TipReceipts | F1 — a new runnable probe receipt is labelled `no-committed-re-run-command`, gate
green | `R40` | population/label rule". Round 39 then landed exactly that: a new runnable probe
receipt (`corpus/evidence/round39/git-leak-probe.txt`), a registry row for it, and a gate that still
prints the identical label and stays green. Deferring the population rule cost one round's coverage
of the round's newest receipt — and the round-39 population grew by exactly one file, which is the
one file not compared: `receipts=24 → 25`, `byte_equal=4 → 4` (round-38 baseline
`.ufo/waves/round-38/build/R38TipReceipts/tip-receipts-run.txt`:
`receipts=24 byte_equal=4 differ=0 skipped=20`).

Corollary: no round-39 frozen claim covers this gate (`grep -n 'tip.receipt\|tip_receipts'
plans/round-39-claims.md` → no match), so C1/C2 can be fully green with this gap open; the only
authority here is the `SKILL.md:586` verdict map, and the printed reason contradicts it.

## Risks

- Any future round's `probe*` receipt is skipped by default with a false cause name; the gate's
  `exit 0` is unchanged by it, so the failure mode is invisible in CI-style use and in an
  `integrate/measure-final.txt` line that reports only the exit code.
- The false label is actively misleading to an operator deciding whether a receipt is still
  reproducible: the assigned question is literally answered wrong by the tool.
- Not measured here (out of seat scope): whether the r19 log receipts (19 files, referenced from
  `corpus/README.md`, `plans/state_check.py:147-151`) have committed re-run commands under a form the
  tool does not parse; and F3-of-r38 ("absent dependency counted as `compared`") — this run had no
  absent dependency, so it was not exercised.

## Suggested next move (R40, single point of change)

Either add the round-39 line to `RECEIPTS` (proven above: `equal`, control `differ`, 3 s) *and* a red
state for `skipped>0` when a skipped receipt's basename appears in a `SKILL.md` registry row with a
`Run as:` command, or derive `mapped` from the registry-row command instead of the literal table. The
label must change: `unmapped-receipt: not in RECEIPTS — add it` is true where
`no-committed-re-run-command` is false.

## Receipts (this seat)

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-39/falsify/F39TipReceipts/` —
`tip-receipts-run.txt` (full tip run), `tip-receipts-list.txt` (`--list`), `unpatched-only-git-leak.txt`,
`tamper-unmapped.txt`, `mapped-control.txt`, `git-leak-rerun.txt` (direct re-run + shas + cmp).
Scratch `/fast/scratch/hyaku/kengaku-r39/F39TipReceipts` removed after the receipts were copied; no
process left running.

VERDICT: tip-receipts-4/25-git-leak-skipped
