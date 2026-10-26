# F40NoHarmC1 — no-harm at the tip (round 40, wave 2)

Seat: `F40NoHarmC1` (critic). Assigned tip: `ec1005a2a28bc5cfdde7723374368ed4cc956eed` (branch `master`).
Fixture: `S=/fast/scratch/hyaku/kengaku-r40/F40NoHarmC1`, `git clone -q --no-local <lane> "$S/lane"` + `checkout ec1005a2`,
`git -C "$S/lane" rev-parse --show-toplevel` = `$S/lane` before any write. Base-of-round-40 control: second clone at
`d3a6277f188434458e1d2ce04aff59392c6f0dc6` (`$S/base38`, `$S/base37`); live-head control: third clone (`$S/head`,
`refs/heads/master`). Every counter, battery module and gate invocation ran inside
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent`
(from the lane clone, `TMPDIR=$S`), per the round-40 host-safety ruling; nothing was written outside `$S` and
`.ufo/waves/round-40/falsify/F40NoHarmC1/`. Scratch deleted at exit (`trap 'rm -rf -- "$S"' EXIT`); receipts below are the
copies. No pacman/uv/npx install was needed; no tool was installed or upgraded (recorded per the 2026-10-19 tooling directive).

## Axes

1. **Reproducibility** — do the counters print the recorded values at the assigned tip?
2. **Identity** — did round 40 touch any frozen instrument, battery, or gate?
3. **Attribution** — are the red lines pre-existing (recorded at round-39 closure / present at the base commit) rather than
   round-40 regressions?
4. **Non-vacuity** — can the assigned checks fail, or are they green because they compare nothing?

## 1. Verdict table (all measured at `ec1005a2`, clean clone)

| Instrument (default selectors — no `--only`/`--battery`/`--battery-dir`, so the predicate is a verdict, not `n/a`) | Recorded (measure-final @`ec172168`; round-39 closure) | Measured @`ec1005a2` | Base @`d3a6277f` |
|---|---|---|---|
| `plans/round39_c1_verify.py --lane . --work $S/work/r39c1` | `PINS total=26 mismatched=0`, `BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass`, exit 0 | **identical, 101/101 lines byte-equal**, exit 0 | identical 101 lines |
| `plans/round39_c2_verify.py --lane . --work $S/work/r39c2` | `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0 | **identical, 20/20 lines**, exit 0 | differs only `P8 46/46 → 47/47` (§4) |
| `plans/round38_c1_verify.py` | `PINS total=14`, `BATTERY fixtures=86 …`, `MUTANTS total=22 killed=21 survived=1`, `PREDICATE C1 fail`, exit 1; survivor `N21 D5 silence` | **identical, 112/112 lines** incl. `MUTANT N21 D5 silence SURVIVED`, exit 1 | identical 112 lines |
| `plans/round38_c2_verify.py` | `checks=7 defects=0`, `V7 ok rows=7 tags=7 bad=0`, pass | **identical**, exit 0 | differs only `P8 46/46 → 47/47` |
| `plans/round37_c1_verify.py` | `GATE plans/pkg_gate.py sha256=frozen`, `BATTERY fixtures=64 wrong=0 renamed_disagree=0`, `MUTANTS total=55 killed=55 survived=0`, `PREDICATE C1 pass`, exit 0 | **identical, 123/123 lines**, exit 0 | identical 123 lines |
| `plans/round37_c2_verify.py` | `checks=7 defects=0`, pass | **identical**, exit 0 | differs only `P8 46/46 → 47/47` |
| `plans/round36_c2_verify.py --lane .` | `W1..W6 ok`, `checks=6 defects=0`, pass | **identical**, exit 0 | identical |
| `plans/anchor_digest_check.py --lane .` | `rows=114 tokens=21 defects=0`, exit 0 | **identical line**, exit 0 | (protected file, unchanged) |
| `plans/ledger_tip.py --source <clone> --work …` | `rows=9 closed=9 observed_pass=9 mismatches=0`, exit 0 | **same rows**, exit 0; first two lines `REF BIND … why=clone-lacks-ref` vs `REF AUDIT … state=match` (§3) | — |
| `plans/order_check.py` r40 / r39 / r38 | PASS / PASS / **FAIL** (`HIT .ufo/waves/round-38/claims/control-c2-skip.txt@e0a378539a45:11 kind=gate-p10`) | **identical, 5/5/6 lines**, exit 0/0/1 | same exit 0/1, same HIT line |
| protected diff (item 3 of the target) | — | **0 files, 0 lines** | — |

Round-39 closure text this reproduces — `corpus/lessons/round-39.md:60` "`MUTANTS total=7 killed=7 survived=0 …`
`PREDICATE C1 pass`"; `:63` "`checks=7 defects=0`, `PREDICATE C2 pass`"; `:66` "round-38 … → exit 1; round 39 → exit 0";
`:67` "`round37_c1_verify.py` → `killed=55` (no harm); `round38_c1_verify.py` → `killed=21 survived=1` as landed"; and
`corpus/lessons/round-40.md:89` (same two values as the round-40 spot-check step). All five hold at the tip.

How the comparisons were made: each tip log was diffed against the corresponding block of
`.ufo/waves/round-40/integrate/measure-final.txt`, with the block extracted by the invoking `$ python3 …` line and the
trailing `exit=` line stripped (`diff` output empty ⇒ identical):
`r37c1.log` 123 lines, `r38c1.log` 112, `r39c1.log` 101, `r37c2.log` 20, `r38c2.log` 20, `r39c2.log` 20, `anchor.log` 1,
`order40/39/38.log` 5/5/6. Receipts: `r37c1.log r38c1.log r39c1.log r37c2.log r38c2.log r39c2.log r36c2.log anchor.log
ledger.log order40.log order39.log order38.log` in this seat's directory.

## 2. Identity — no instrument changed since the round-40 base

`bbb1095^` = `d3a6277f`, i.e. the base is exactly the round-40 pre-round commit, so `d3a6277f..ec1005a2` is round 40's whole
footprint (5 commits: `bbb1095 055748f 3077adb ec17216 ec1005a`). The assigned command
`git diff d3a6277f ec1005a2 -- plans/battery37 plans/battery38 plans/battery39 plans/round3*_verify.py
plans/anchor_digest_check.py plans/ledger_tip.py plans/order_check.py plans/pkg_gate.py` prints nothing:
`diff_lines=0`. Per-file blobs are equal, not merely equal-looking
(`git rev-parse <commit>:<path>`), e.g. `anchor_digest_check.py base=80e7292c… tip=80e7292c…`,
`order_check.py base=d298b6c0… tip=d298b6c0…`, `pkg_gate.py base=544135df… tip=544135df…`;
all ten individual files listed in `identity-evidence.txt`. Battery **tree** objects match at base, tip and live head:
`battery37 14254918…`, `battery38 5d69ebd4…`, `battery39 971b3e10…` (all three equal across the three commits).
Round 40's `plans/` footprint is additions only plus `M plans/tip_receipts.py` (`git diff --name-status d3a6277f ec1005a2
-- plans/`): `A plans/battery40/{a_bind,a_man,a_row,a_tok,l_refuse,l_rows,o_gate}.py`, `A plans/{db_wal_probe.py,
pkg-spec-r40.json,round-40-claims.md,round40_c1_verify.py,round40_c2_verify.py,round_close.py}`, `M plans/tip_receipts.py`.
Both frozen-digest manifests verify at the tip: `sha256sum -c .ufo/waves/round-39/claims/frozen-digests.txt` → 9× OK,
exit 0; `.ufo/waves/round-40/claims/frozen-digests.txt` → 11× OK, exit 0.

## 3. Attribution — the red lines are pre-existing, and one receipt line is a fixture artifact

**(a) `round38_c1_verify.py` is red at the tip (`exit 1`) and at the base commit, identically.** `b38c1.log` vs `r38c1.log`
are byte-identical (112 lines), including `MUTANT N21 D5 silence SURVIVED -- the capture digest is looked up in every
manifest row, not only the first [F37XMutD5 X3]`. So the survivor is not a round-40 regression: round 40 changed neither the
counter, the battery tree, nor the gate blob that counter pins (`GATE … sha256=frozen`), and the base commit exhibits it.
A no-harm gate worded "every historical counter exits 0" is therefore unsatisfiable and would misreport round 40 as harmful;
the correct predicate is *equality with the recorded baseline*, which holds. `round38_c1`'s `PREDICATE C1 fail` is the
project's own open defect (F37XMutD5 X3), carried forward unchanged.

**(b) `ledger_tip.py` prints `REF BIND … why=clone-lacks-ref` instead of measure-final's `REF AUDIT … state=match` when the
clone under test is detached at a commit that is not the branch head.** My first run used `--source $S/lane` (detached at
`ec1005a2`) with the clone's `refs/heads/master` = `c9c793ca33fab1cdaf1127c06ba31685c7db1325`
(`git -C $S/lane rev-parse refs/heads/master`), so the tool correctly reported the detached-clone case
(`plans/ledger_tip.py:174`) and bound `rev=ec1005a2 tip=ec1005a2 source_ref=c9c793ca…`. Re-run on a clone whose `HEAD` is
symbolic on `refs/heads/master` (`$S/head`): `REF AUDIT ref=refs/heads/master rev=c9c793c tip=c9c793c state=match`, then
`LEDGER corpus/defects-round35.jsonl rows=4 closed=4 observed_pass=4 mismatches=0` /
`rows=9 closed=9 observed_pass=9 mismatches=0`, exit 0. Ledger verdict is green in both shapes; only the ref line differs.
Anyone diffing `ledger_tip` output against measure-final will see exactly this two-line difference and should not read it as
drift — measured, not inferred: `ledger.log` (detached) vs `head_ledger.log` (branch).

**(c) The assigned tip is one commit behind the live branch head.** `git -C $S/lane rev-parse refs/heads/master` =
`c9c793c`; `git log --oneline -1 c9c793c` = "round-40: wave-2 spec and dispatch (35 seats, policy v1)", with
`git merge-base --is-ancestor ec1005a2 c9c793c` → YES and `git log --oneline c9c793c..ec1005a2` empty. The no-harm set is
still untouched at the head: `git diff --name-only d3a6277f c9c793c -- <the 8 protected paths>` → 0 files,
and `anchor_digest_check.py` at the head clone → `rows=114 tokens=21 defects=0`, exit 0 (`head_anchor.log`). So the
no-harm result covers the branch as it stands, not only the commit named in the item.

## 4. Non-vacuity — the checks can fail, and the C2 base→tip delta is corpus growth

**(a) The pathspec is live.** `plans/round3*_verify.py` expands in the shell to 12 files
(`round31/32/33/35/36_c1/36_c2/37_c1/37_c2/38_c1/38_c2/39_c1/39_c2 _verify.py`), and `git diff` globs pathspecs: the same
command shape reports `plans/tip_receipts*` → 1 file and `plans/round40*` → 2 files. Caution for the next reviewer:
`git ls-tree -r --name-only <commit> -- 'plans/round3*_verify.py'` returns **0** for *any* glob (also for
`plans/battery40*`), so validating the pathspec with `ls-tree` would wrongly suggest the glob is dead. `git ls-files` and
`git diff` do glob (12 and 1 respectively).

**(b) The C2 counters track the corpus instead of pinning it.** `r37_c2`, `r38_c2` and `r39_c2` differ between base and tip
in exactly one line each: `gate: P8 ok index_rows=46 knowledge_files=46` at `d3a6277f` → `index_rows=47 knowledge_files=47`
at `ec1005a2`. That is round 40's `S121` registry row plus `corpus/knowledge/tb2-db-wal-recovery-grader.md`, and the gate's
invariant (`index_rows == knowledge_files`, `bad=0`) still holds. Every other line is byte-equal, including each
`P10 ok probe_rerun=byte-equal bytes=<n>` line — `bytes=5867` (r39), `5537` (r38), `8443` (r37) identical at base and tip. Consequence: a no-harm check written as "same output as last round" would fail on this legitimate growth; the
predicate that holds is "same verdict", which is what was measured.

**(c) measure-final was recorded one commit before the assigned tip, and the gap is inert.** `measure-final.txt:1` says
`TIP ec172168…`; the tip I measured is `ec1005a`. `git diff --name-status ec172168 ec1005a` outside the round-40 report
report directory is exactly `M LOG.md`, `M SCORECARD.md`, `A corpus/lessons/round-40.md`, `A .ufo/waves/round-40/integrate/
{measure-final.txt,census-after.txt}`, `A make_falsify_spec.py`, plus `build*`/report files — no file any counter reads. That
is why every §1 comparison is byte-identical rather than merely value-equal, with the single exception of `ledger_tip`'s two
`REF` lines (§3b), whose difference is the clone's branch state, not a byte of the tool or of the ledgers it read.

## 5. Boundary note (no verdict attached)

`plans/tip_receipts.py` is modified by round 40 (`M` in §2) and is covered by neither frozen-digest list (`sha256sum -c` on
both manifests lists 20 files, none of them `tip_receipts.py`). That is the intended routed item of this round
(`R40TipReceipts`, `corpus/lessons/round-40.md:40`) and lies outside this item's protected set; recorded as
fact only, because it means the no-harm argument for that file rests on its own report and the landing measurement
(`receipts=26 byte_equal=6 differ=0 skipped=20`), not on file identity.

## 6. What could not be measured

Nothing in the item was skipped. One method limit: the round-38 survivor's *cause* is inferred from identical bytes at the
base commit plus the unchanged counter/battery/gate blobs, not from a diff of the defect itself — the counter is frozen and
may not be edited, so the pre/post byte-equality is the strongest available attribution.

## Findings summary

- **No harm found.** Twelve invocations at `ec1005a2` (six round-37/38/39 C1/C2 counters, `round36_c2`, `anchor_digest_check`,
  `ledger_tip`, three `order_check` runs) reproduce the landing measurement byte-for-byte and restate every
  round-39 closure value; the 8 protected paths and 3 battery trees are blob-identical to the round-40 base; both
  frozen-digest manifests verify; the same holds at the live head `c9c793c`.
- **Smallest safe correction, for the record (no file was edited):** if a later round turns this into a gate, assert
  *verdict equality against the recorded baseline* (and pin `ledger_tip`'s `REF` line out of the comparison, or run it from a
  clone whose `HEAD` is `refs/heads/master`); asserting "all counters exit 0" fails today on the pre-existing
  `round38_c1` survivor, and asserting "same bytes" fails on legitimate corpus growth in `P8`.

VERDICT: no-harm-c1-ok
