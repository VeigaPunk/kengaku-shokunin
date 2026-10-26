# F42RevBatOclause — non-author honesty review of `plans/battery42/o_clause.py` (XO1, XO3)

Seat: reviewer, kengaku round 42 wave 2 (FALSIFY), lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Attack target: the battery module that carries the XO1 and XO3 kills in the landing measurement
(`.ufo/waves/round-42/integrate/measure-final.txt:46-47`). Method: read the module (116 lines, full), the two
mutant rows it kills (`plans/round42_c1_verify.py:191-200`), the gate clauses they skip
(`plans/order_check.py:17-19, 182-193`), the wave-1 substitute-shape report (`R42CritC1Counter.md §1`), and the
author's wave-1 report (`R42BatOrdClause.md`); then re-ran the counter and the gate by hand on fixtures I built
myself. No tool installed (pacman paused; nothing needed).

## 0. Identity and envelope

- Landed module = author sidecar: `sha256 plans/battery42/o_clause.py` =
  `badc9e3d3807e22c99161ae3c991db1e0ed840dd8c76542dbf9643c210af163b` =
  `sha256 .ufo/waves/round-42/build/R42BatOrdClause/battery/o_clause.py`; `diff -q` → identical. What I reviewed
  is what the landing measured.
- Clone: `git clone -q --no-local <lane> $S/lane && git -C $S/lane checkout -q 508434ad55c709337065611691c426f05875492d`;
  `git -C $S/lane rev-parse --show-toplevel` = `/fast/scratch/hyaku/kengaku-r42/F42RevBatOclause/lane`. PINS at
  the clone equal the counter's literals (`948d5e1d…` order, `11bb2cad…` anchor); `PINS total=2 mismatched=0`,
  `PINS-AFTER mismatched=0`.
- Envelope on every counter/build/tool run (Q32): `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin
  /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>`.
  `ls -A /home/vgpnk/.local/bin | sha256sum` = `8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52`
  before (18:03:17) and after (18:06:11) — unchanged. Full receipt:
  `.ufo/waves/round-42/falsify/F42RevBatOclause/counter-run.txt` (2.4 KiB).

## 1. Required counter run (single-module battery, `--only XO1,XO3`) — reproduces the landing

`python3 $S/lane/plans/round42_c1_verify.py --lane $S/lane --battery-dir $S/bat-o_clause --only XO1,XO3 --work $S/w`
inside the envelope, exit 0:

```
MUTANT XO1 order rc-silence killed by=o_clause-freeze-single attributed=L183 hits=2 -- plans/order_check.py:17,183 'FAIL when the freeze commit (the first commit adding <claims>
MUTANT XO3 order rc-silence killed by=o_clause-receipt-withdrawn attributed=L188 hits=2 -- plans/order_check.py:18,188 'FAIL when <receipt> was committed before <claims> (pre-regist
BATTERY fixtures=5 wrong=0 tampered=0 sidechannel=0
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/0 order=2/2
```

Byte-for-byte the landing's MUTANT lines (`measure-final.txt:46-47`), and all five FIXTURE lines `ok`.
`hits=2`: both fixtures of each pair exhibit the direction independently; the counter attributes the first.

## 2. Per-fixture honesty table

The advertised sentences (mutant `adv` cells, `round42_c1_verify.py:192,197`):
XO1 — "FAIL when the freeze commit (the first commit adding <claims>) already contains <receipt>" (clause
`order_check.py:183` skipped); XO3 — "FAIL when <receipt> was committed before <claims> (pre-registration
inverted …)" (clause `:188` skipped, which fires only when the receipt's first adding commit is a *strict*
ancestor of the freeze — the one-commit case is clause 1's).

| fixture (fid) | mutant(s) it silences | verdict | reason (verified, not read off the comment) |
|---|---|---|---|
| `o_clause-freeze-single` | XO1 (hits member) | **honest** | One commit adds claims+receipt together; unmutated gate prints `ORDER FAIL freeze-contains-receipt … already has corpus/evidence/round42/fibsqrt-probe.txt`, `hits=0` (clause 3 clean), rc=1; freeze==receipt_commit so clause 2 is vacuous — the only failure is the advertised clause 1, over a real receipt *file* with the real round-42 receipt body. Not the wave-1 `b-xo1-receipt-is-directory` substitute (there `--receipt` was a directory and no receipt artefact existed). |
| `o_clause-freeze-pair-edited-after` | XO1 (hits member) | **honest** | Three commits: scaffold → freeze (adds claims + receipt v1) → regrade (edits receipt, adds LOG.md). Gate: freeze=receipt_commit=ed34ca2, `ORDER FAIL freeze-contains-receipt`, clause 2 vacuous, clause 3 clean (1 blob scanned, 0 hits), rc=1. The freeze tree carries a real receipt file; the later edit is extra realism (the gate reads the freeze tree, not HEAD), not a substitute direction. |
| `o_clause-receipt-withdrawn` | XO3 (hits member) | **honest** | Round-9 paths: receipt committed (C1) → `git rm` + commit (C2) → claims frozen (C3, tree lacks the receipt) → receipt re-recorded (C4, satisfies the HEAD setup check). Gate: `ORDER FAIL receipt-before-claims 90a34e9… is an ancestor of 90ac9fe…`, `scanned commits=0` (clause 3 vacuous — claims_dir has no blob at/before C1), clause 1 does not fire, rc=1. Exactly "receipt committed before claims" over real receipt commits — the honest version of the wave-1 `b-xo3-emptied-directory` substitute (there the receipt path was a directory and *no receipt was ever committed*). |
| `o_clause-receipt-side-line` | XO3 (hits member) | **honest** | Branching history: receipt on master (C1) → withdrawn (C2) → freeze on side line (C3) → receipt re-recorded on master (C4) → `merge --no-ff` (C5). Gate resolves freeze=c58bf0e (side line), receipt_commit=cdc6449 (master C1, an ancestor of C3 through C2): `ORDER FAIL receipt-before-claims`, clause 1 does not fire (freeze tree branched after the withdraw), clause 3 vacuous (`scanned commits=0`), rc=1. Same advertised direction over a non-linear graph — shape diversity, not a substitute. |
| `o_clause-clean-order` | none (control) | **honest** | Pass path: claims frozen (C1) → receipt committed (C2). Gate: `ORDER RESULT PASS` rc=0; its claims blob is the one exempt gate line `P10 DEFECT receipt unreadable` (`EXECUTED_EXCUSE`, `order_check.py:58-60`) and still scores `hits=0` — it exercises the clause-3 exemption rather than hiding a defect. Carries no kill; not load-bearing (author's table agrees). |

**5/5 honest, 0 substitutes, 0 incidental.** The incidental-kill worry is closed two ways: (a) each reject
fixture's unmutated failure line names exactly the clause its mutant skips (`freeze-contains-receipt` for the
XO1 pair, `receipt-before-claims` for the XO3 pair) — the counter's `exhibits()` only compares exit codes, so
this had to be checked by hand; (b) the cross matrix below shows each mutant is silenced *only* by the pair
built for its clause.

## 3. Flip matrix (my own variant runs, same envelope)

Variants generated in scratch by the counter's own byte replacement (`old -> new` applied once to
`plans/order_check.py`); rc and verdict line from direct runs:

| fixture | reference | XO1 variant (clause 1 skipped) | XO3 variant (clause 2 skipped) |
|---|---|---|---|
| freeze-single | FAIL clause 1, rc=1 | **PASS rc=0** | FAIL clause 1, rc=1 |
| freeze-pair-edited-after | FAIL clause 1, rc=1 | **PASS rc=0** | FAIL clause 1, rc=1 |
| receipt-withdrawn | FAIL clause 2, rc=1 | FAIL clause 2, rc=1 | **PASS rc=0** |
| receipt-side-line | FAIL clause 2, rc=1 | FAIL clause 2, rc=1 | **PASS rc=0** |
| clean-order | PASS rc=0 | PASS rc=0 | PASS rc=0 |

XO1's exhibit set is exactly {the two XO1-shaped fixtures}, XO3's exactly {the two XO3-shaped fixtures} —
matching `hits=2` in both landing and my run. A fixture whose rc=1 came from some other clause could not
appear here; none does.

Load-bearing reproduced (counter, trimmed module copies in scratch, exit 1 both):
- both XO1 fixtures dropped → `MUTANT XO1 order rc-silence SURVIVED exhibits=none`;
- both XO3 fixtures dropped → `MUTANT XO3 order rc-silence SURVIVED exhibits=none`.
So within this module each kill is carried solely by the pair built for it; no fixture kills "by accident".

## 4. Witness read/import/copy check — clean

- The module has **no imports at all** and no file reads: `grep -n "witness\|w_order\|w_anchor\|import\|config\|symlink\|gpg\|showSignature\|worktree\|read_text\|open(" plans/battery42/o_clause.py` → no matches. It touches nothing outside the `ctx` API (`init`/`write`/`git`/`sh`), and the counter's own SIDECHANNEL scan (which includes the `witness` token) reports `sidechannel=0`.
- Structure vs `w_order.py` (the comparable witness; `w_anchor.py` is the anchor tool's, different contract): not a renamed copy. Witness helpers `c`/`args`, constants `CLAIMS/CDIR/RECEIPT`, fixtures `xo1, xo3, xo5, gate_repo`, fids `w-xo1-freeze-has-receipt` …, all round-42 paths, receipt body `probe receipt\n`, control blob `P10 DEFECT receipt unreadable`. o_clause: helpers `commit`/`gate_argv`, constants `M42/CLAIMS42/PROBE42/M9/CLAIMS9/PROBE9/CLEAN/RECEIPT_BODY`, fixture functions `xo1_single, xo1_edited_after, xo3_withdrawn, xo3_side_line, clean_order`, fids `o_clause-*`, clause-2 fixtures on **round-9** paths (exercising the round-number parse), receipt body = the real round-42 receipt body, control blobs `CLEAN`, plus two shapes the witness lacks entirely (receipt-edited-after-freeze; side-line freeze merged back) and an accept fixture. Overlap is confined to the counter's mandated battery contract and the clause shapes the adv cells require.

## 5. Repo-local config / symlink / core.worktree / gpg tricks — none

- Module text: no `git config`, no symlink creation, no gpg/signature tokens (grep above).
- Built fixtures inspected directly (I built them into scratch via the counter's `--build-module` child): all five repos' `.git/config` is the vanilla `git init` default (`repositoryformatversion/filemode/bare/logallrefupdates` only — no `core.worktree`, no `hooksPath`, no `gpg.program`, no `showSignature`); `find <fixture> -type l | wc -l` = 0 for every fixture; histories match the module comments exactly (`git log --graph --oneline --all` per fixture). The build/run env pins (`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `HOME=/nonexistent`, tool runs additionally `core.hooksPath=/dev/null`, `core.fsmonitor=false`) leave no room for the wave-1 V1/V1b vectors through this module.

## 6. Attribution strength (known limit, does not change the verdict)

The counter attributes XO1 at L183 and XO3 at L188 — lines that evaluate on every `main()` invocation, so the
span check alone is weak (wave-1 `R42CritAttribution`; the freeze names it). For these two mutants the gap is
closed by the clause-specific FAIL lines in §2/§3: the reference fails *on the skipped clause's own branch*
and the variant passes, so the result difference is that clause's behaviour, not an environmental accident.
The merge fixture (side-line) additionally shows the ancestry clause resolves correctly over a non-linear
graph, which a linear substitute could not demonstrate.

## 7. Residual risks / verification gaps

1. The counter's `exhibits()` for the order tool compares exit codes only; my clause-line check is the evidence
   that the failures are the advertised clauses. If a future battery fixture for order relied on rc alone, the
   same incidental-kill hole the wave-1 critic showed would reopen — the non-author review obligation stays.
2. `o_clause-clean-order`'s claims blob is the *exempt* gate line; it validates the exemption, but it is not a
   fully clean blob. A second accept fixture with a truly clean claims dir would be marginally stronger; not a
   defect (the exemption is exactly what the gate must not false-positive on).
3. My review covers this module only; the anchor modules and `o_scan.py` (XO5/XO6/XO7) are sibling seats' scope.
4. Host-side: `~/.local/bin` digest unchanged across all runs; no lane file edited; nothing written outside my
   report dir and `$S` (scratch removed at the end via `plans/scratch_guard.py safe-rm`, 547.2 MiB).

VERDICT: battery42-o_clause-honest-5/5-substitute-0
