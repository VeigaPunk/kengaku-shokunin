# F41C2Rerun — C2 re-measure at the landing tip (round 41, wave 2, falsify)

Seat: F41C2Rerun (executor). Target: C2, the pinned TB2 `constraints-scheduling` grader package.
Scratch: `/fast/scratch/hyaku/kengaku-r41/F41C2Rerun` (removed at end). Receipts: `F41C2Rerun/receipts/`.
Every run below used the mandated envelope:
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent`.

## 0. Environment, tip and freeze integrity

```
$ git -C /fast/scratch/hyaku/kengaku-r41/F41C2Rerun/lane rev-parse HEAD   # after clone of lane master
d7c77895752a2a5f317fa22f2362416ada50a04b
$ git merge-base --is-ancestor 3d0058fbde484c9d6c23fd997d9ee09a0663bcdb HEAD -> YES-ancestor
$ git diff --stat 3d0058fb..HEAD -- plans corpus SCORECARD.md LOG.md README.md SKILL.md PROVINCE.md
(empty)   # plans/ and corpus/ byte-identical between the assigned tip and d7c7789
```

**Tip note (not a defect).** The assignment names tip `3d0058f`; lane master is `d7c7789`, one commit later
(`round-41: wave-2 (falsify) spec and dispatch (34 seats)`). `3d0058f` is an ancestor and the diff over
`plans/`+`corpus/`+docs is **empty**, so C2 artifacts are identical. I measured at **both** commits
(§1 and §3) and the counter output is byte-identical.

Frozen digests all verify against `.ufo/waves/round-41/claims/frozen-digests.txt`:
`round41_c2_verify.py = cf1632b5…`, `constraints_probe.py = 8c471fbd…`, `constraints-dry-cases-freeze.txt = a656ce9b…`.

## 1. Counter, run 1 and run 2 (assigned tip 3d0058f, `--work` absent)

```
$ bwrap … python3 …/plans/round41_c2_verify.py --lane "$S/lane" --work "$S/absent/w"
V1 ok listed=10 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=29 distinct_quotes=29 distinct_lines=29 out_of_word_range=0
    gate: P4 ok checked=29 bad=0 first=0
    gate: P5 ok manifest_entries=10 bad=0 first=0
    gate: P6 ok rows=2 bad=0 first=0
    gate: P7 ok source_lines=2 bad=0 first=0
    gate: P8 ok index_rows=48 knowledge_files=48 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=5775
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=2 bad=0
V4 ok cases=25 mismatches_named=2/2 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=11 tags=11 bad=0
V8 ok order_exit=0 result=PASS
checks=8 defects=0
PREDICATE C2 pass
EXIT=0
```

Run 2 printed the same lines; `cmp` of the two captures:
```
counter run1==run2: BYTE-EQUAL   (sha256 878ab2c2ac3b1ac7b13340be60aba0437f1b98bdf7d971b645936e7b77f1fc4e)
```
**Holds.** The D10(b) absent-`--work` fix works (`--work "$S/absent/w"` did not raise), and the run is deterministic.

## 2. Probe, three runs incl. `env -i`; `--dry`

```
PROBE RUN 1 @ 16:13:59   EXIT=0 bytes=5775
PROBE RUN 2 @ 16:14:10   EXIT=0 bytes=5775
PROBE RUN 3 (env -i PATH=/usr/bin:/bin HOME=… TMPDIR=…) @ 16:14:23   EXIT=0 bytes=5775
probe-1: BYTE-EQUAL to receipt
probe-2: BYTE-EQUAL to receipt
probe-3-envi: BYTE-EQUAL to receipt
```
All three stderr files are empty. `probe-1.txt` sha256 = `c5aa674277f9b9473de4c0884629c577f2b6467d8b73c3a90eec33b24b7701da`
= the committed `corpus/evidence/round41/constraints-probe.txt`.

```
$ bwrap … python3 …/constraints_probe.py --lane "$S/lane" --dry
EXIT=0 bytes=3899
DRY: BYTE-EQUAL to freeze table          (sha256 a656ce9b… = DRY_SHA256 / frozen-digests.txt)
```
**Holds: probe-byte-equal 3/3**, and `--dry` reproduces the freeze table exactly.

Extra determinism (coverage), four more runs, all byte-equal to the receipt:
```
[TZ=Asia/Tokyo] exit=0 BYTE-EQUAL
[TZ=America/New_York] exit=0 BYTE-EQUAL
[LANG=C LC_ALL=C] exit=0 BYTE-EQUAL
[TZ=UTC LANG=ja_JP.UTF-8] exit=0 BYTE-EQUAL      # probe total 7/7 byte-equal
```
The probe is timezone- and locale-independent. (Note: an earlier TZ run that reported exit 2 was **my own error** —
it ran concurrently with my capture-tamper test below and correctly refused the tampered file. Re-run serially on the
clean tree: byte-equal. I record the invalid first attempt rather than quietly dropping it.)

## 3. Counter at actual master HEAD d7c7789

```
HEAD=d7c77895752a2a5f317fa22f2362416ada50a04b
V1..V8 all ok, checks=8 defects=0, PREDICATE C2 pass
master counter vs assigned-tip counter: BYTE-EQUAL
```
**Holds at both commits.**

## 4. Do the checks have teeth? (four tampers, my clone only, `git restore` after each)

| Tamper | Result | Meaning |
|---|---|---|
| T-A: append one byte to `alice_calendar.ics` | `V1 DEFECT listed=10 bad=['alice_calendar.ics']`; `V2 DEFECT gate_exit=1`; `checks=8 defects=2`; `PREDICATE C2 fail` | capture pin bites, twice |
| T-B: forge receipt **self-consistently** (`weekend-sat-20` observed fail→pass **and** summary `6/19`→`7/18`) | `gate: P2 ok receipt_sha256=pinned` then `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt`; `V4 ok`; `V2 DEFECT`; `PREDICATE C2 fail` | **P2 is presence-only** (V2 copies the on-disk digest into the spec before calling the gate, `round41_c2_verify.py:169`); authenticity rests entirely on **P10**, and P10 does bite |
| T-C: requirement-map `hard-constraints` `partly`→`enforced` | `V7 DEFECT bad=['hard-constraints: labelled enforced, receipt derives partly']`; `defects=1`; `PREDICATE C2 fail` | derived-label rule bites; V4's internal-consistency check alone would not have caught it |
| D: append one byte to `bob_calendar.ics`, then run the **probe** | `SETUP capture bob_calendar.ics missing or not at its pinned digest`, `probe exit=2` | the probe refuses a tampered capture instead of grading it |

Tree was clean after every restore: `tree-clean-after=[]`.

## 5. Receipt arithmetic, recounted from the receipt itself

```
CASE lines: 25      observed=pass: 6      observed=fail: 19      match=NO: 2
TAG lines in dry: 11      CASE lines in dry: 25
```
Agrees with the frozen label `cases=25 observed_pass=6 observed_fail=19 mismatches=2`. The two `match=NO` cases
(`later-valid-wed-1105`, `seconds-30`) are named in the entry (8 and 9 backticked occurrences respectively), so
V4's `mismatches_named=2/2` is earned, not incidental.

## 6. Residual risks (reported, not remediable by me — the counter is frozen)

1. **Content-blindness is structural, and I confirm it by code reading rather than by a filler package.**
   No check reads the entry's analytical prose: `plans/pkg_gate.py` clauses are `c_instruments, c_receipt,
   c_quote_shape, c_quote_verbatim, c_captures, c_sources, c_provenance, c_readme, c_clean_tree, c_rerun`
   (`pkg_gate.py:287-289`), and `min_teaches_words` gates the SOURCES row's teaches **cell**
   (`pkg_gate.py:204`), not the entry. `plans/round41_c2_verify.py` contains **0** occurrences of `teaches`.
   So `R41CritClaims.md §1` stands unmitigated at the tip: V1–V8 pin reproduction and internal consistency,
   never whether the prose teaches the grader. This is the prose item the L1 still needs non-author review on.
2. **The probe receipt has no freeze digest.** `corpus/evidence/round41/constraints-probe.txt` is absent from
   `.ufo/waves/round-41/claims/frozen-digests.txt` (`grep -c` → 0); it is pinned only transitively, by
   P10 rerun-equality from the frozen probe (`8c471fbd…`, itself V5/P1-pinned). Combined with T-B this is
   adequate at measure time — a forged receipt cannot survive P10 — but the freeze list is 1 file short of the
   counter's own inputs, so freeze-diff auditing must remember the receipt is covered indirectly.
3. **V4 cannot detect a self-consistent-but-wrong receipt on its own** (T-B: `V4 ok` on a forged receipt).
   Sole barrier is P10. Any future change that drops `--rerun` from V2's gate invocation
   (`round41_c2_verify.py:171`) silently converts C2 into a rubber stamp; worth a wave-2 note for the L1.
4. Inherited wave-1 limits I did **not** re-test and that do not touch my measurement: AF_UNIX/SysV isolation,
   relative-argv escape, dead-site crediting — all **C1** vectors, out of this seat's scope.

## 7. Compliance

- Wrote only `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-41/falsify/F41C2Rerun{,.md}/receipts/`
  and `/fast/scratch/hyaku/kengaku-r41/F41C2Rerun` (now deleted). No lane file, no `~/.local/bin`, no fleet root touched.
- No `git add/commit/checkout` on the lane; in my own clone only `checkout --detach`/`checkout master`/`restore`.
- No tools installed, so nothing to record under the tooling directive.

VERDICT: c2-pass-yes-probe-byte-equal-3/3
