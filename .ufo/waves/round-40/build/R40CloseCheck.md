# R40CloseCheck — round close: the order gate gets a caller

Seat: executor, round 40 wave 1 (`R40CloseCheck`). Lane `kengaku-shokunin`; scratch
`/fast/scratch/hyaku/kengaku-r40/R40CloseCheck/` (removed at exit). Nothing in the lane was edited.

Residual addressed (draft only — it is in the lane once the L1 lands it): `F39CritQ30` — "Q30's 'closed by a gate' while nothing invokes it"
(`corpus/lessons/round-39-verifier-spotcheck.md` §5, R4). Q30 records the order class as *closed*
by `plans/order_check.py` (`corpus/QUALITY.md:533`, "it reads commits only"), and the lane's
Q30 "Check" is a hand-typed pair of commands in prose (`corpus/QUALITY.md:542-558`) that no round,
counter or registry row runs. `plans/order_check.py` is pinned by C1 and was not touched
(`sha256 948d5e1d2b34…` measured here, identical to the digest the round-40 claims cite).

## 1. Deliverable

| item | value |
|---|---|
| draft (proposed lane path `plans/round_close.py`) | `.ufo/waves/round-40/build/R40CloseCheck/round_close.py` |
| digest | `112b52f0051357491b1654932948989d57b923c22bea817c15b710e5f9785c3b` |
| size | 327 lines, stdlib only (`argparse hashlib os re shlex subprocess sys tempfile contextlib io pathlib`) |

```
python3 plans/round_close.py --lane . --round N [--census PATH]
python3 plans/round_close.py --lane . --selftest [--work DIR]
```

`--lane` must be the git work-tree top (order_check resolves its paths against the work-tree root).
`--census` defaults to `$SHOKUNIN_ROOT/scripts/sources-census.sh` (the census's own root contract),
then to the lane's parents; a clone with neither is a setup error, never a skipped leg.

Exit contract: `0` every leg passed · `1` a leg FAILED (order broken, or a census E-code) ·
`2` setup (no claims file, no order tool, no census script, no registry, a receipt on disk but not
in HEAD, claims naming no readable receipt, `--lane` not the work-tree top, bad arguments).

Legs, per round:

1. `plans/round-N-claims.md` read; its receipt(s) resolved (three rules, §2);
2. `plans/order_check.py --lane <lane> --claims <claims> --receipt <receipt>` once per receipt,
   its stdout echoed verbatim into the receipt;
3. `<census> validate --file <lane>/corpus/SOURCES.md` (TSV echoed; W-codes counted, not failing);
4. composite exit = worst leg (`PASS < FAIL < ERROR`), so a leg that cannot be evaluated is never
   a pass.

Every line starts `ROUND-CLOSE`; the child gate's lines start `ORDER` and the census's are TSV, so a
receipt is greppable for either.

## 2. How the receipt is found (the one non-obvious rule)

The claims name the probe, not always the receipt. The lane has written it three ways; all three
are read, deduplicated in this order:

- (a) one line `Receipt: `corpus/evidence/round37/…-probe.txt`` — rounds 36/37's spelling
  (`plans/round-37-claims.md:78`);
- (b) a backticked `corpus/evidence/roundN/…-probe.txt` for this round (`-probe-first-run.txt` and
  `-dry-cases-freeze.txt` deliberately do not match);
- (c) derived from a `plans/<stem>_probe.py` the claims name →
  `corpus/evidence/roundN/<stem with _→->.txt`; this is the rule rounds 38-40 need, because their
  claims name only the script (`plans/round-40-claims.md:77` names `plans/db_wal_probe.py`, the
  receipt is `corpus/evidence/round40/db-wal-probe.txt`).

A candidate that is neither a file in the lane nor in HEAD is printed as
`ROUND-CLOSE note=skipped-unreadable-receipt <path>` and dropped; if none survives, exit 2.
All five rounds 36-40 resolve to exactly one receipt through these rules (measured, §3-§4).

## 3. The required demonstration — RED on 38, GREEN on 39 and 40

Clean clone of lane HEAD `3077adb` (`git clone -q --shared <lane> "$S/lane"`, `rev-parse
--show-toplevel` = `$S/lane`; `git status --porcelain` = only the injected `?? plans/round_close.py`).
Command, unchanged for all three:

```
SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin python3 plans/round_close.py --lane . --round <N>
```

Receipt: `.ufo/waves/round-40/build/R40CloseCheck/run-clone-38-39-40.txt` (94 lines; census W04
lines elided below, none elided in the file).

```
######## round 38 ########
ROUND-CLOSE lane=/fast/scratch/hyaku/kengaku-r40/R40CloseCheck/lane round=38
ROUND-CLOSE claims=plans/round-38-claims.md sha256=5a74378357914dbd13aa1baa2beee5574a9bb4fe84256d917be02a4ed43c3916
ROUND-CLOSE order-tool=plans/order_check.py sha256=948d5e1d2b3429d76a598fd11c4b22856d9f43ec093efd2c6aa0025aa0fc6ecc
ROUND-CLOSE receipts=1
ORDER claims=plans/round-38-claims.md round=38 freeze=e0a378539a45cc9388c66cfba22f44275131de23
ORDER receipt=corpus/evidence/round38/build-pmars-probe.txt receipt_commit=e95cf5500b6c13305cc41b8532ae07fb2c9dcd7b claims_dir=.ufo/waves/round-38/claims/
ORDER scanned commits=1 file_entries=6 distinct_blobs=6
ORDER HIT .ufo/waves/round-38/claims/control-c2-skip.txt@e0a378539a45:11 kind=gate-p10 `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt`
ORDER FAIL probe-executed-before-receipt hits=1
ORDER RESULT FAIL
ROUND-CLOSE order receipt=corpus/evidence/round38/build-pmars-probe.txt exit=1 verdict=FAIL
ROUND-CLOSE census tool=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh sha256=3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30 cmd=…/sources-census.sh validate --file …/lane/corpus/SOURCES.md
ROUND-CLOSE census exit=0 warnings=15 verdict=PASS
ROUND-CLOSE RESULT FAIL exit=1
exit=1
```

```
######## round 39 ########
ROUND-CLOSE claims=plans/round-39-claims.md sha256=ec8760ea53bdec8814ae1953e5935687ec50332abacfbc188aaab60496ee014a
ORDER receipt=corpus/evidence/round39/git-leak-probe.txt receipt_commit=6a1eb5e1da4a435940b821e28530c31f3411549c claims_dir=.ufo/waves/round-39/claims/
ORDER scanned commits=1 file_entries=7 distinct_blobs=7
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS
ROUND-CLOSE order receipt=corpus/evidence/round39/git-leak-probe.txt exit=0 verdict=PASS
ROUND-CLOSE census exit=0 warnings=15 verdict=PASS
ROUND-CLOSE RESULT PASS exit=0
exit=0
```

```
######## round 40 ########
ROUND-CLOSE claims=plans/round-40-claims.md sha256=8b9ed6e833077c800eb6242fda3263c4adc02b63cceaea7e80e4eb8c9d58d1cf
ORDER claims=plans/round-40-claims.md round=40 freeze=bbb109505670192035ef63d7c8b37733e99fa1a3
ORDER receipt=corpus/evidence/round40/db-wal-probe.txt receipt_commit=055748f78a3335434f2a4070bb3fb1cf8d0eba1f claims_dir=.ufo/waves/round-40/claims/
ORDER scanned commits=1 file_entries=12 distinct_blobs=12
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS
ROUND-CLOSE order receipt=corpus/evidence/round40/db-wal-probe.txt exit=0 verdict=PASS
ROUND-CLOSE census exit=0 warnings=15 verdict=PASS
ROUND-CLOSE RESULT PASS exit=0
exit=0
```

The red and the greens come from the same tool bytes in the same clone in one run, and the 38-vs-39
difference is one line of one claims blob: round 38's control kept a non-excused `P10` detail,
round 39's keeps only `P10 DEFECT receipt unreadable` (the gate's exemption,
`plans/order_check.py:56-60`). That is Q30's own cited pair (`corpus/QUALITY.md:542-550`),
now produced by a command instead of by hand.

## 4. Series calibration, rounds 36-40 (bonus, same clone, same command)

Receipt: `.ufo/waves/round-40/build/R40CloseCheck/run-clone-36-37.txt`.

| round | receipt resolved by | order leg | census leg | composite | the lesson's own verdict on that round |
|---|---|---|---|---|---|
| 36 | rule (b) `corpus/evidence/round36/regex-log-probe.txt` | PASS | PASS | **0 GREEN** | no ordering mistake recorded |
| 37 | rules (a)+(b) `corpus/evidence/round37/git-webserver-probe.txt` | FAIL `HIT …round-37/claims/control-c2-skip.txt@ca790460e9b7:12` | PASS | **1 RED** | "repeats round 37's order-of-operations mistake" (`plans/round-38-claims.md:12`) |
| 38 | rule (c) | FAIL `HIT …round-38/claims/control-c2-skip.txt@e0a378539a45:11` | PASS | **1 RED** | "This repeats round 37's order-of-operations mistake" (same line) |
| 39 | rule (c) | PASS | PASS | **0 GREEN** | `R39` closed the class with the gate |
| 40 | rule (c) | PASS | PASS | **0 GREEN** | this round |

The gate is not always-red and not always-green: it separates exactly the two rounds whose lessons
record the mistake (37, 38) from the three that held. Round 37's red reproduces Q30's "shown able
to fail" clause (`corpus/QUALITY.md:552-558`) through the new command.

## 5. Controls (each leg shown able to fail alone)

### 5.1 Shipped self-test — `--selftest`

```
$ SHOKUNIN_ROOT=… python3 plans/round_close.py --lane . --selftest --work "$S/st"
SELFTEST case=A-excused-p10 shape=receipt-last expect=0 got=0 verdict=ok
SELFTEST case=B-executed-p10 shape=receipt-last expect=1 got=1 verdict=ok
SELFTEST case=C-receipt-first shape=receipt-first expect=1 got=1 verdict=ok
SELFTEST case=D-receipt-uncommitted shape=receipt-uncommitted expect=2 got=2 verdict=ok
SELFTEST case=E-no-receipt-named shape=no-probe expect=2 got=2 verdict=ok
SELFTEST checks=5 ok=5 failed=0
exit=0
```

Receipt: `…/R40CloseCheck/selftest.txt`. Q30 already names "three synthetic two-commit repos" as the proof that each leg bites
(`corpus/QUALITY.md:554-558`); this is that proof as a runnable command, plus two setup cases (D, E).
Five two-commit fixture repos under `--work`; each seeds
`plans/order_check.py`, `corpus/SOURCES.md`, `corpus/knowledge/`, `corpus/lessons/` and differs only
in commit order and the body of one claims/ control line. Case B differs from case A by exactly one
line (`fresh probe output is not byte-equal` vs `receipt unreadable`) and the verdict flips 0 → 1.
Case C exercises clauses (1) and (2) (`freeze-contains-receipt`, `receipt-before-claims`), not the
blob scan. D and E are the two ways a round can have no gated receipt.

### 5.2 The same five fixtures as standalone receipts

Receipt: `…/R40CloseCheck/order-controls.txt` (full `ROUND-CLOSE` lines, which `--selftest`
suppresses). Verdicts identical: A `PASS exit=0`, B `FAIL exit=1`, C `FAIL exit=1`,
D `ERROR exit=2`, E `ERROR exit=2`. B's hit line:
`ORDER HIT .ufo/waves/round-39/claims/control-c2-nothing.txt@3cf2bab9c77d:1 kind=gate-p10`.

### 5.3 Census leg and setup guards

Receipt: `…/R40CloseCheck/controls.txt`.

```
######## census control C1: one malformed registry row (uncommitted) on round 39 ########
ORDER RESULT PASS
ROUND-CLOSE order receipt=corpus/evidence/round39/git-leak-probe.txt exit=0 verdict=PASS
file	E12	S999 row outside Registry section
ROUND-CLOSE census exit=1 warnings=15 verdict=FAIL
ROUND-CLOSE RESULT FAIL exit=1
exit=1
restored, dirty-lines=0
```

The order leg stays PASS while the census leg fails: the composite is a conjunction, not an
either. Setup guards, all exit 2: `--round 99` → `no claims file: plans/round-99-claims.md`;
`--lane plans` → `--lane must be the work-tree top: …/lane/plans (top is …/lane)`;
`--census /nope/…` → `no census script (scripts/sources-census.sh); pass --census PATH`; a clone
with no `--census` and no `SHOKUNIN_ROOT` → the same message (never a silently skipped leg).

### 5.4 Census `--file` vs `--root` equivalence (why the leg needs no fleet roster)

```
$ scripts/sources-census.sh validate --file <lane>/corpus/SOURCES.md | cut -f2-   # exit 1
$ scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku | cut -f2-  # exit 1
diff … → (no output) findings IDENTICAL (17 lines: 15 W04 + 2 E11)
```

Both modes resolve E11 against the lane root and print the same 17 findings; only the TSV's lane
label differs (`file` vs `kengaku`). `--file` therefore works unchanged on a clone, which is what
round35's V6 already does for clone lanes (`plans/round35_c1_verify.py:182-189`).

## 6. Live-lane measurement — and one integration constraint the L1 must sequence

Receipt: `…/R40CloseCheck/live-lane.txt`. On the live work tree (`--lane
/home/vgpnk/Projects/shokunin/kengaku-shokunin --round 40`, census auto-discovered):

```
ORDER RESULT PASS
ROUND-CLOSE order receipt=corpus/evidence/round40/db-wal-probe.txt exit=0 verdict=PASS
file	E11	S119 missing used-by corpus/knowledge/tb2-db-wal-recovery-grader.md
file	E11	S120 missing used-by corpus/knowledge/tb2-db-wal-recovery-grader.md
ROUND-CLOSE census exit=1 warnings=15 verdict=FAIL
ROUND-CLOSE RESULT FAIL exit=1
```

Cause, measured at the same moment:

```
$ git -C <lane> status --porcelain
 M corpus/SOURCES.md
?? .ufo/waves/round-40/build.ready
?? .ufo/waves/round-40/build.ready.dispatched
?? .ufo/waves/round-40/build/
?? .ufo/waves/round-40/integrate/
?? corpus/lessons/round-40.md
```

The S119/S120 rows exist only in the work tree, not in HEAD (`git show HEAD:corpus/SOURCES.md`
differs from the work-tree file by exactly those two rows), and the entry they name does not exist
yet. Consequences for integration, stated as facts, not as requests:

- **`--round 40` goes GREEN on a clean clone of `3077adb` (no S119/S120 rows at HEAD) but is RED on
  the live work tree until `corpus/knowledge/tb2-db-wal-recovery-grader.md` lands and the rows are
  committed.** The clone measurement in §3 is the landing-tip measurement only if the C2 entry and
  its rows are committed by then; run it again at the landing tip.
- Any C2 check that needs a clean tree (`pkg_gate.py --require-clean-tree`, the counter's V2) sees
  `M corpus/SOURCES.md` right now. That is C2's seat to sequence, not mine; flagged because the
  order of the two landings decides whether the round-40 close command is green.
- The census leg is work-tree-scoped by design, so it is the one leg whose verdict a sibling's
  in-flight edit can move. That is a property of the census, not of this tool.

## 7. Drafts for the L1 (not applied — lane files are yours)

**SKILL.md §Gate/probe registry row** (8 columns, matching the existing header):

```
| `round-close` | gate | `python3 plans/round_close.py --lane . --round N` (`--census PATH`; default `$SHOKUNIN_ROOT/scripts/sources-census.sh`, then the lane's parents) | `0` every leg passed · `1` a leg failed (`ORDER RESULT FAIL`, or a census E-code) · `2` could-not-evaluate (no claims file / order tool / census script / registry, receipt on disk but not in HEAD, claims naming no readable receipt, `--lane` not the work-tree top) | `python3 plans/round_close.py --lane . --selftest` (A–E, five temp two-commit repos) | the round's `plans/round-N-claims.md`, the receipt(s) it names, `plans/order_check.py` (digest echoed), the fleet census script (digest echoed) | none — reads commits and `corpus/SOURCES.md`; writes nothing | kengaku |
```

**Q30 wiring** — the criterion's Check (`corpus/QUALITY.md:542-558`) is two hand-typed commands;
the invocable form is `python3 plans/round_close.py --lane . --round 38` → exit 1 and
`--round 39` → exit 0 (receipts §3). If you want one sentence in Q30, it is: *"Invoked per round as
`plans/round_close.py --lane . --round N` (exit 0 only when the order gate and the registry census
both pass); measured 2026-10-26 on a clean clone of `3077adb`: round 38 exit 1, rounds 39 and 40
exit 0."*

**Does this close R3?** No. R3 (`corpus/lessons/round-39-verifier-spotcheck.md` §5) asks for the
order class as a `corpus/defects.jsonl` row with `recurrence=2` through `defect_ledger`; that stays
blocked by C1's pin on `plans/ledger_tip.py` and is untouched here. This closes the *invocation*
half of R4 only.

## 8. Limits named

- One round per run; it does not sweep the series. The 36-40 table in §4 was produced by five runs.
- The order leg inherits `order_check.py`'s own limits verbatim (commits only; a committed *quote*
  of a forbidden line trips it; `receipt unreadable` is exempt). Round 38 is red only because its
  skip control kept one non-excused `P10` line — that is the gate's design, and this tool neither
  widens nor narrows it.
- Rule (c) is a naming convention, not a proof: a round whose receipt is named nothing like its
  probe and is not backticked in the claims would need a claims edit. All of 36-40 resolve.
- The census leg accepts W-codes by the census's own contract ("0 clean or warnings"); `warnings=15`
  is printed every run so a storm stays visible, but it does not fail the leg. That is the census's
  rule, adopted rather than tightened.
- `--selftest` copies `corpus/knowledge/` and `corpus/lessons/` per fixture (~700 KB × 5) because
  the census's E11 needs the registry's used-by targets to exist; it writes only inside `--work`
  (or a fresh temp dir when `--work` is omitted).
- Not run here (per the wave rule): the lane's own gates, counters, linters or the C1/C2 predicates.

## 9. Files

Written, all inside the seat's own dir:

- `.ufo/waves/round-40/build/R40CloseCheck.md` (this report)
- `.ufo/waves/round-40/build/R40CloseCheck/round_close.py` — the draft, `112b52f0…`
- `.ufo/waves/round-40/build/R40CloseCheck/run-clone-38-39-40.txt` — the required RED/GREEN receipt
- `.ufo/waves/round-40/build/R40CloseCheck/run-clone-36-37.txt` — series calibration
- `.ufo/waves/round-40/build/R40CloseCheck/selftest.txt` — shipped `--selftest`, 5/5
- `.ufo/waves/round-40/build/R40CloseCheck/order-controls.txt` — five fixture repos, full output
- `.ufo/waves/round-40/build/R40CloseCheck/controls.txt` — census red control + four setup guards
- `.ufo/waves/round-40/build/R40CloseCheck/live-lane.txt` — live work-tree measurement + dirty state

Not written: any lane file, `plans/`, `corpus/`, `SKILL.md`, `SCORECARD.md`, `LOG.md`; no commit,
no `git add`, no jj command in the lane. `plans/order_check.py` digest measured unchanged
(`948d5e1d…`). Tooling installed: none.

VERDICT: round-close-r38-red-r40-green
