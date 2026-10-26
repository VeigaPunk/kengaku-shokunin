# R40LessonDraft — mistake mining for `corpus/lessons/round-40.md` `## Mistakes`

Seat: R40LessonDraft (scribe). Axes served: **quality** (a wrong lesson row is a false statement in the lane's memory),
**calibration** (every row must rest on a measured observation, and a row's *fix* is priced only where a
falsifier exists). Lane read-only: no lane file edited, no git mutation in the lane, no tool installed.
Scratch `S=/fast/scratch/hyaku/kengaku-r40/R40LessonDraft` (shared clone at `3077adbc…`; removed at exit).

Measured against lane HEAD `3077adbc7145726519f60f01426a5d03381ad444` and the freeze commit
`bbb109505670192035ef63d7c8b37733e99fa1a3`.

Answer to the assigned questions first:

- **(1) O13.** Confirmed: `R39PlanNext.md:126` asserts "reachable with one new fixture"; it is **equivalent**, and the
  mutant was withdrawn pre-freeze. Measured by me, not just argued: reference `rc=0 ORDER RESULT PASS`, mutant
  (`CASE_LINE.match` → `.search`) `rc=0 ORDER RESULT PASS` on the `w-o13-quoted-case` end state.
- **(2) `--work` absent.** Confirmed in `plans/round40_c2_verify.py:266` (`FileNotFoundError` traceback, `exit=1`).
  **The committed control does not show it**: `control-c2-nothing.txt` reproduces line-for-line at `bbb1095` only when
  a real `--work` parent exists (my run, §2). The same freeze's C1 counter *does* handle it (`created if absent`),
  so the two counters disagree inside one freeze.
- **(3)** One further live recurrence found and measured: `plans/tip_receipts.py` again enumerates the newest receipt
  and skips it with a reason that its own parser disproves (round-39 `F39TipReceipts` F1, routed R4, unlanded).

## 1. Draft rows (schema of `corpus/lessons/round-39.md:41`; the L1 decides)

### M1 — reachability asserted, not witnessed (a survivor labelled "reachable" from code reading; it is equivalent)

| field | content |
|---|---|
| class | a frozen mutant list classified a survivor as "reachable with one new fixture" without building the fixture; the mutant turned out **equivalent**, so the label was wrong in the direction that inflates the claim |
| evidence pointer | `.ufo/waves/round-39/build/R39PlanNext.md:126` — "survive, reachable with one new fixture (4) … O13 `CASE` arm unanchored (`search` for `match`)"; withdrawn at the round-40 freeze, `plans/round-40-claims.md:35-37` "`O13` was withdrawn before freeze: its witness showed it EQUIVALENT"; recorded as a limit in the counter, `plans/round40_c1_verify.py:65-67` "`R39PlanNext`'s O13 (`CASE_LINE.match` -> `.search`) is EQUIVALENT, not reachable" |
| captured-by | the round-40 L1 at the freeze (withdrawal before any mutant was frozen); re-measured by this seat |
| fix | **not yet shown able to fail.** No lane instrument reds when a seat writes "reachable" beside a survivor it never ran. Proposed (cheap, reuses what already exists): the C1 `MUTANTS` rows already carry a `witness` column — require that column to name an *executed* witness line, and let a prose-only witness print `UNWITNESSED` (the verdict `plans/mutant_direction_check.py` already defines) so such a mutant cannot be counted killed. Flip for the row: a later claims file lists a survivor as "reachable" whose witness column is prose, and nothing goes red. |

Measured evidence (my run, `S/o13repo`; two-commit fixture: freeze commit adds
`.ufo/waves/round-50/claims/control.txt` = `note: CASE a predicted=pass observed=pass`, receipt commit adds the receipt):

```
$ python3 $S/lane/plans/order_check.py --lane $S/o13repo --claims plans/round-50-claims.md --receipt corpus/evidence/round50/probe.txt
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS
rc=0
$ python3 $S/order_mut.py …            # CASE_LINE.match(line) -> CASE_LINE.search(line), one-line edit
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS
rc=0
```

**Calibration note on the row's own sourcing.** `plans/round-40-claims.md:35-36` says "its witness showed it
EQUIVALENT". The committed witness cannot show that: `.ufo/waves/round-40/claims/witness/w_order.py:35-36` builds an
**accept** fixture (`expect="accept"`, `defects=[]`) and `witness-run.txt` prints `declared=- observed_rc=0
observed=-` for it — an accept fixture on the reference only. Equivalence rests on the `^`-anchored pattern matched
line-at-a-time (correct, and confirmed by the run above), i.e. on code reading; `witness-run.txt` never runs the
O13 mutant at all. If the lesson quotes the claims sentence it should quote the docstring argument, not the witness.

### M2 — `--work` absent → uncaught traceback, rc colliding with the predicate's own failure code (round-39 D3, recurring in a counter written in the same freeze that fixed it elsewhere)

| field | content |
|---|---|
| class | a tool's `--work` parent is handed straight to `tempfile` without `mkdir`; the traceback escapes the per-check `try`, and `exit=1` is indistinguishable from the tool's legitimate "predicate fail" |
| evidence pointer | `plans/round40_c2_verify.py:266`; the round-39 original at `corpus/lessons/round-39-verifier-spotcheck.md:30` — "Probe `--work` must pre-exist." — and its routed repair `…spotcheck.md:134` (R2) |
| captured-by | round-39 closure D3 (non-author spot-check); recurrence found by this seat against the round-40 counter |
| fix | **not landed; shown able to fail.** One line before the `TemporaryDirectory`: `if a.work: pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)` — exactly what the sibling counter already does. Demonstration that the current state is red is in §2 below; the fix's flip is that same command returning a counter verdict instead of a traceback. |

Measured:

```
$ python3 plans/round40_c2_verify.py --lane . --work "$S/absent-dir"
  File ".../plans/round40_c2_verify.py", line 266, in main
    with tempfile.TemporaryDirectory(prefix="k40-c2-", dir=a.work) as work:
FileNotFoundError: [Errno 2] No such file or directory: '…/absent-dir/k40-c2-56xzhhc9'
exit=1
```

Contrast inside the same freeze — `plans/round40_c1_verify.py:71` documents "`--work DIR` scratch parent, created if
absent" and `:462-463` does `pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)`; measured:
`--work "$S/absent-c1" --only A01` created the dir and printed `PINS total=3 mismatched=0` … `PREDICATE C1 n/a`.
The C2 counter's docstring never mentions `--work` at all (`--work` appears only in its `argparse`), so the defect is
outside its documented surface but inside the seat workflow that tells every seat to pass `--work` explicitly.

Same class, still unlanded from round 39: `plans/git_leak_probe.py:258` `tempfile.mkdtemp(prefix="k39-glr-", dir=a.work)`
with no `mkdir` → measured `FileNotFoundError … /absent-glp/k39-glr-3otvtme_`, `rc=1`.

### M3 — a gate's verdict map counts receipts it cannot price; the newest receipt is skipped with a reason the tool's own parser disproves (two rounds running)

| field | content |
|---|---|
| class | the registry sentence quantifies over "every committed `probe*` receipt with a committed re-run command", but enumeration is a five-entry literal table, so each new round's receipt falls out of scope and is reported with a false skip reason — the gate stays green |
| evidence pointer | `SKILL.md:586` — "`0` every committed `probe*` receipt with a committed re-run command is byte-equal at the tip"; `plans/tip_receipts.py:55-60` (five literal entries, round35–38 only); previous instance `.ufo/waves/round-39/falsify/F39TipReceipts.md:58` (F1, routed R4, unlanded) |
| captured-by | `F39TipReceipts` (round-39 wave-2 falsifier) on the round-39 receipt; recurrence on the round-40 receipt measured by this seat |
| fix | **shown able to fail — this is the best-priced row of the three.** Current state, measured at HEAD `3077adbc`: `--list` prints `receipt corpus/evidence/round40/db-wal-probe.txt skip reason=no-committed-re-run-command`, while the tool's own `usage_argv` parses that probe to `(['python3','plans/db_wal_probe.py','--lane','.'], 'docstring')` — the same skip reason is printed for `corpus/evidence/round39/git-leak-probe.txt` too. `--tamper` on it is refused: `SETUP: --tamper corpus/evidence/round40/db-wal-probe.txt is not a mapped receipt`, `rc=2` (`plans/tip_receipts.py:303`). Fix: enumerate by `usage_argv` over every candidate (skip only when it returns no argv), keeping the literal table for `kind=`. Flip: after the fix `--list` shows both receipts as mapped **and** `--tamper corpus/evidence/round40/db-wal-probe.txt` answers `differ`; before it, the `rc=2` above. |

```
$ python3 plans/tip_receipts.py --lane . --list | grep -E 'round39|round40'
receipt corpus/evidence/round39/git-leak-probe.txt skip reason=no-committed-re-run-command
receipt corpus/evidence/round40/db-wal-probe.txt skip reason=no-committed-re-run-command
$ python3 plans/tip_receipts.py --lane . --only round40 --tamper corpus/evidence/round40/db-wal-probe.txt
SETUP: --tamper corpus/evidence/round40/db-wal-probe.txt is not a mapped receipt
rc=2
```

## 2. The committed C2 control, reproduced — and what it does not cover

`control-c2-nothing.txt` is honest and reproducible: in the clone detached at the freeze `bbb1095`,
`python3 plans/round40_c2_verify.py --lane . --work "$S/w"` reproduces it line for line (`checks=7 defects=4`,
V2 V3 V4 V7, `PREDICATE C2 fail`), the only difference being the trailing shell `exit=1` echo that is not counter
output. It was run with a real work parent, so **the control neither exercises nor reveals the M2 crash**, and an
absent `--work` cannot be told from a red predicate by rc alone (both `1`).

## 3. Considered and declined (with the reason, so the L1 does not re-mine them)

| candidate | decision | reason |
|---|---|---|
| `mutant_direction_check.py` cannot price the round-40 list | no row | needs the round-38 surface (`battery38_fixtures`, `attributed`, `FAMILY`); round 40 keeps its `MUTANTS` inside the counter. Already known and routed (`F39MutDirection`, R4); the round-40 claim substitutes committed text witnesses plus `null_detected`. Not new evidence. |
| R1 — gates with no registry row | no row (yet) | `grep -n 'order_check\|round40_c1_verify\|round40_c2_verify' SKILL.md` → no hit at `3077adbc`; seat `R40RegistryRows` is live on it this wave. A carried routed item in flight, not a mistake; re-check at integration. |
| seat scratch hygiene (D5/R5) | not judgeable | 20+ seat dirs under `/fast/scratch/hyaku/kengaku-r40/` at read time, but the seats are running. Judge after the wave. |
| both committed controls end with a shell `exit=1` echo | note, not a row | `control-c1-nothing.txt` and `control-c2-nothing.txt` carry a harness line that is not tool output; harmless for the freeze rule, but a byte-comparison of a control against a re-run fails on it (mine did). |
| C1 claims arithmetic `anchor 11, ledger 7, order 3 = 21` | holds | table rows by prefix = 11/7/3; `control-c1-nothing.txt` lists the same 21. No row. |
| "R5 drafts are byte-identical to the landed tools" (`plans/round-40-claims.md:38-40`) | holds | `sha256sum .ufo/waves/round-39/build/R39LedgerProvenance/ledger_tip.py plans/ledger_tip.py` → both `853bcb2a…77ad4`; `R39AnchorUnion/anchor_digest_check.py` = `plans/anchor_digest_check.py` = `11bb2cad…fd4c2`; `diff -q` empty ×2. |

## 4. Sweep — commands run (all read-only against the lane; scratch only under `$S`)

1. `git clone -q --shared <lane> "$S/lane"`; `git -C "$S/lane" rev-parse --show-toplevel` = clone; HEAD `3077adbc…`.
2. `python3 plans/round40_c2_verify.py --lane . --work "$S/absent-dir"` → traceback, `exit=1`.
3. `python3 plans/round40_c2_verify.py --lane . --work "$S/w"` at `3077adbc` and at `bbb1095`; `diff` vs
   `claims/control-c2-nothing.txt` → identical at the freeze commit.
4. `python3 plans/round40_c1_verify.py --lane . --work "$S/absent-c1" --only A01` → dir created, counter ran.
5. `python3 plans/git_leak_probe.py --lane . --work "$S/absent-glp"` → `FileNotFoundError`, `rc=1`.
6. Two-commit fixture `$S/o13repo` + `sed`-free copy `$S/order_mut.py` (`match`→`search`); both tools run → `rc=0` each.
7. `python3 plans/tip_receipts.py --lane . --list | grep -E 'round39|round40'`; `--only round40 --tamper …` → `rc=2`;
   `import tip_receipts; usage_argv(…, 'plans/db_wal_probe.py')` → `(['python3','plans/db_wal_probe.py','--lane','.'],'docstring')`.
8. Digest and line checks: `sha256sum` of the three tripwire tools (match claims `11bb2cad`/`853bcb2a`/`948d5e1d`),
   `grep -cE '^    \("[ALO][0-9]{2}"' plans/round40_c1_verify.py` → 21, `grep -n 'O13'` over claims/counter,
   `sed -n 55,60p plans/tip_receipts.py`, `sed -n '/^def main/,$p' plans/round40_c2_verify.py`.

## 5. Limits of my evidence

- Every claim above is from the clone at `3077adbc` / the freeze `bbb1095`; wave-1 seats are still landing
  `plans/battery40/` and the C2 package, so M2/M3 statuses may change before integration. Re-check at the landing tip.
- M1's fix and M2's fix are *proposals*: neither is shown able to fail in the lane (no instrument reds on them today);
  only M3 carries a `rc=2` demonstration of the defect and a stated flip.
- I did not run the full C1 counter (a battery subset only) and did not re-run the C2 probe: the receipt's byte-equality
  is P10's business at the counter, not mine, and I did not need it for any row.
- Exit-code readings are rc from this host's `python3` 3.14; the lane's pins assume the same interpreter family.

VERDICT: mistakes-drafted-3
