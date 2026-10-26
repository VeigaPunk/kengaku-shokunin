# F40RegistryRows — do the round-40 registry rows and the round-40 addendum run as written?

Seat: critic, kengaku round 40 wave 2 (FALSIFY). Attacks: the seven commands the round-40 `SKILL.md`
§Gate/probe registry rows and the "Round-40 registry addendum" (`SKILL.md:625-643`) state for
`order-check` (`SKILL.md:590`), `round39-c1-audit` (`:591`), `round40-c1-mutants` (`:592`),
`round40-c2` (`:593`), `db-wal-probe` (`:594`), `round_close` (addendum, `:633-636`) and
`tip-receipts` (`:586`, addendum `:636-638`).

Fixture: `S=/fast/scratch/hyaku/kengaku-r40/F40RegistryRows`; `git clone -q --no-local <lane> $S/lane`,
`git -C $S/lane checkout -q ec1005a2a28bc5cfdde7723374368ed4cc956eed`,
`rev-parse --show-toplevel` = `$S/lane`. Every command below ran from that clone root with `--lane .`.
The lane was never written; no lane git/jj command was run. C1 counters ran only inside the mandated
wrapper (`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin … --tmpfs /run/user/1000 --proc /proc
--unshare-pid --die-with-parent`); the wrapped `round40_c1_verify.py` still nested its own per-case
`--unshare-pid` sandboxes and returned the green predicate, so the wrapper is compatible with the tool.

Headline: **7 of 7 stated commands reproduce their row's exit code and verdict lines on a clean clone
of `ec1005a`.** Four documentation defects survive (F1–F4); none changes a measured exit code.

| # | row | command (clone root) | measured exit | row's map | match |
|---|---|---|---|---|---|
| 1 | `order-check` | `python3 plans/order_check.py --lane . --claims plans/round-40-claims.md --receipt corpus/evidence/round40/db-wal-probe.txt` | 0 | `0` + `ORDER ok …` + `ORDER RESULT PASS` | yes |
| 2 | `round39-c1-audit` | `python3 plans/round39_c1_audit.py --lane . --work <existing>` (bwrap) | 0 | `0` + 7 predicate lines | yes |
| 3 | `round40-c1-mutants` | `python3 plans/round40_c1_verify.py --lane . --work <scratch>` (bwrap) | 0 | `0` + 5 predicate lines | yes |
| 4 | `round40-c2` | `python3 plans/round40_c2_verify.py --lane . --work <existing>` | 0 | `checks=7 defects=0` + `PREDICATE C2 pass` | yes |
| 5 | `db-wal-probe` | `python3 plans/db_wal_probe.py --lane . --work <scratch>` | 0 | `0` + `regrade cases=28 differ=0` + `cases=28 … mismatches=0` | yes |
| 6 | `round_close` | `python3 plans/round_close.py --lane . --round 40 --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh` | 0 | `0` every leg passed (1 leg failed, 2 setup) | yes |
| 7 | `tip-receipts` | `python3 plans/tip_receipts.py --lane . --work <scratch>` | 0 | `0` every mapped receipt byte-equal + control `differ` | yes |

## 1. Predicate lines vs the rows

`order-check` — exit 0, `order-check.out`:

```
ORDER claims=plans/round-40-claims.md round=40 freeze=bbb109505670192035ef63d7c8b37733e99fa1a3
ORDER receipt=corpus/evidence/round40/db-wal-probe.txt receipt_commit=055748f78a3335434f2a4070bb3fb1cf8d0eba1f claims_dir=.ufo/waves/round-40/claims/
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS
```

Row `:590`'s `0` cell names exactly those two closing lines; the `1` control reproduced verbatim —
`--receipt corpus/evidence/round39/git-leak-probe.txt` printed `ORDER FAIL freeze-contains-receipt …`,
`ORDER FAIL receipt-before-claims …`, `ORDER FAIL freeze-contains-receipt receipt-before-claims hits=0`,
`ORDER RESULT FAIL`, exit 1 (`order-r39-receipt.out`); `--claims plans/round-99-claims.md` printed
`ORDER ERROR claims not committed in HEAD` + `ORDER RESULT ERROR`, exit 2 (`order-r99.out`) — the row
quotes that error string. Two further `2` cases: `--receipt /etc/passwd` → `ORDER ERROR path outside the
lane`, exit 2 (`order-outside.out`); a missing `--receipt` → argparse, exit 2 (`order-missing.out`).

`round39-c1-audit` — exit 0, 54.3 s wall (row: 55 s), `round39-c1-audit.log`:

```
PINS total=26 mismatched=0
BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0
MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0
PINS final total=26 mismatched=0
AUDIT nondeterministic_kills=0
AUDIT C1 clean
PREDICATE C1 pass
```

All seven lines the row's `0` cell names, in that order. The row's `PINS` composition claim ("gate,
round-36/37 counters, round-35 spec, round-37 attribution audit, 9 battery37, 12 battery38") parses to
26 entries from `plans/round39_c1_audit.py` (`PINS` counter: 12 battery38 + 9 battery37 + 5 singleton
files). Its `--work` limit reproduces: `--work <absent>` → `FileNotFoundError` at `:293`, traceback,
exit 1, no `SETUP` line (`absent.out`).

`round40-c1-mutants` — exit 0, 58.3 s wall, `round40-c1.log`:

```
PINS total=3 mismatched=0
BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0
MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 pass
```

Row `:592`'s five lines exactly. The three pin prefixes it quotes are the file digests at this tip
(`tool-digests.out`): `11bb2cad…` anchor, `853bcb2a…` ledger, `948d5e1d…` order. `--work` creation
reproduces (`--only A01` with an absent work dir: `work-created=yes`, exit 0, `c1-only-a01.out`).

`round40-c2` — exit 0, `round40-c2.log`:

```
V1 ok listed=8 bad=0 extra=0 … gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
…
V7 ok rows=6 tags=6 bad=0
checks=7 defects=0
PREDICATE C2 pass
```

Row `:593` matched, including its measured limit: absent `--work` → `FileNotFoundError` traceback,
exit 1 (`absent.out`); `--bogus` → argparse, exit 2 (`c2-bogus.out`); no `--work` at all → exit 0
(`c2-nowork.out`) — the "must already exist" clause applies only to a supplied path.

`db-wal-probe` — exit 0, 1.8 s, `db-wal-probe.log`:

```
regrade cases=28 differ=0
cases=28 observed_pass=8 observed_fail=20 mismatches=0
```

Both summary lines the row demands, with prediction mismatches kept off the exit code. `--dry` prints
28 `CASE ` lines and is byte-equal to the frozen table (`cmp` clean, `dbwal-dry2.out`);
`--stage-check` → `stagecheck cases=28 failed=0`, exit 0 (`dbwal-stage.out`); an absent `--work` is
created (`dbwal-newwork.out`).

`round_close` — exit 0, `round-close.log`:

```
ROUND-CLOSE claims=plans/round-40-claims.md sha256=8b9ed6e8…
ROUND-CLOSE order receipt=corpus/evidence/round40/db-wal-probe.txt exit=0 verdict=PASS
ROUND-CLOSE census exit=0 warnings=15 verdict=PASS
ROUND-CLOSE RESULT PASS exit=0
```

The addendum's red/green claim reproduces: `--round 39` → exit 0 (`rc39.out`), `--round 38` → exit 1
with `ORDER RESULT FAIL`/`ROUND-CLOSE RESULT FAIL exit=1` (`rc38.out`), `--round 40` → exit 0.
`--selftest` → `SELFTEST checks=5 ok=5 failed=0`, exit 0 (`rc-selftest.out`), the addendum's "five
fixture repos".

`tip-receipts` — exit 0, `tip-receipts.log`:

```
receipt corpus/evidence/round39/git-leak-probe.txt equal bytes=5867 exit=0 doc=SKILL.md:587+SKILL.md:590
receipt corpus/evidence/round40/db-wal-probe.txt equal bytes=8257 exit=0 doc=SKILL.md:593+SKILL.md:590
control receipt=corpus/evidence/round35/tb2-grader-probe.txt flip=byte 1699 0x27->0x26 verdict=differ
note compared=6 declared_bounded=1 no_command=19
receipts=26 byte_equal=6 differ=0 skipped=20
```

The addendum's derived-mapping claim ("`--list` prints `origin=derived`") holds for both new receipts
and only those (`tip-list.out`, `grep -c origin=derived` → 2). The other 19 live receipts all say
`skip reason=no-committed-re-run-command`, which the row's population clause ("with a committed re-run
command") already excludes.

## 2. Addendum's R2 claim, tested by edit (second clone, never the lane)

`git clone --no-local $S/lane $S/edit-lane`; one line changed in `plans/git_leak_probe.py`
(`grader is never imported` → `grader is not imported`, `git diff --stat` = 1 file, 1 insertion/1
deletion); then `python3 plans/round39_c2_verify.py --lane . --work <existing>` in the edited clone:

```
V2 DEFECT spec=frozen gate=frozen gate_exit=1
V5 DEFECT probe or dry table not at freeze digest
checks=7 defects=2
PREDICATE C2 fail          exit=1
```

Baseline in the same clone before the edit: `V1..V7 ok`, `checks=7 defects=0`, exit 0
(`c2r39-baseline.out`, `c2r39-edited-one-line.out`). So the addendum's "a one-line edit reds the
round-39 C2 counter's V2 and V5" is true as written, and the probe is not editable without re-freezing.
The shared `--work` precondition also reproduces for all four tools the addendum names
(`git_leak_probe`, `round39-c2`, `round40-c2`, `round39-c1-audit`): each exits 1 with the
`FileNotFoundError` traceback (`absent.out`).

## 3. Findings

**F1 — `round40-c1-mutants` row has no map entry for a mistyped `--battery-dir`; a setup error is
reported as a verdict failure.** Measured: `--battery-dir <absent>` → exit 1 with
`BATTERY fixtures=0 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=21 killed=0 survived=21`,
`PREDICATE C1 n/a`, and no `SETUP` line (`c1-mistyped.out`). The row's `2` cell lists only "`/usr/bin/
bwrap` not executable, lane clone failure, a battery build that raises, duplicate fixture id, argparse"
(`SKILL.md:592`), so the path-typo case is absent; the exit 1 is only incidentally covered by "any
survivor". Wave-1 measured this and said "the row declares it" (`.ufo/waves/round-40/build/
R40RegistryRows.md` §4 finding 2), but the landed row and the addendum's limits paragraph
(`SKILL.md:628-632`) do not declare it — a measured limit was dropped between draft and landing.
Smallest safe correction (text only): add to the `2` cell "an absent `--battery-dir` prints `BATTERY
fixtures=0` and exits 1, with no SETUP line". Impacted axes: verdict-map completeness, operability.

**F2 — the same row never states what a development selector exits.** Measured `--only A01` → exit 0,
`MUTANTS total=1 killed=1 survived=0`, `PINS-AFTER mismatched=0`, `PREDICATE C1 n/a` (`c1-only-a01.out`).
The row's `0` cell requires `PREDICATE C1 pass`, and its `1` cell has no dev-subset clause, so exit 0
with `n/a` is mapped by nothing — a seat wiring `$?` reads a selector run as pass while the predicate
never ran. The round-39 rows carry the missing clause (`SKILL.md:591`: "also a development subset whose
killed set is not clean (:423-425)"); the wave-1 warning ("the row must not read `n/a` as success") did
not reach the landed text. Smallest safe correction: append "selectors exit 0 on a clean subset, 1
otherwise; `PREDICATE C1 n/a` is never a pass". Same unmapped case exists on `round39-c1-audit`
(`--only M01` → exit 0, `PREDICATE C1 n/a`, `r39-only.out`), but its `1` cell already implies the clean
subset's 0.

**F3 — the addendum's `round_close` entry line omits `--census`.** Measured with the literal addendum
command on the clean clone (`$SHOKUNIN_ROOT` unset): `python3 plans/round_close.py --lane . --round 40`
→ exit 2, `ROUND-CLOSE ERROR no census script (scripts/sources-census.sh); pass --census PATH`,
`ROUND-CLOSE RESULT ERROR` (`rc-nocensus.out`). Exit 2 is the row's mapped setup code, so the map is not
violated — but the stated entry is not runnable as written outside the fleet, and the same addendum
tells seats to run on a disposable clone. Smallest safe correction: write the entry as
`python3 plans/round_close.py --lane . --round N [--census PATH]` and add "a clone outside the fleet
must pass `--census` (or set `$SHOKUNIN_ROOT`)". Impacted axes: operability.

**F4 — "the do-nothing control" does not do nothing.** Measured `round39_c1_audit.py --battery r38` →
exit 1, `BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=7 killed=3
survived=4`, `PREDICATE C1 n/a` (`r39-battr38.out`). The round-38 battery already kills 3 of the 7
round-39 mutants, so the label (`SKILL.md:588` and `:591`) invites reading exit 1 as a predicate
failure when the predicate never ran. The row's `1` cell does cover the mechanism ("a development
subset whose killed set is not clean"). Smallest safe correction: relabel "subset control (86 fixtures;
3 of 7 mutants already killed), `PREDICATE C1 n/a`".

## 4. Notes, not findings

- `tip-receipts` receives `--jobs`/`--timeout` (`plans/tip_receipts.py:236-237`) that its row entry does
  not list; no map mismatch, and the defaults reproduced the round-39/40 receipts byte-equal.
- `round40-c1-mutants`'s `2` cell also promises "lane clone failure (:471)" — measured with a non-git
  `--lane`: `SETUP cannot clone … repository … does not exist`, exit 2 (`c1-lanefail.out`).
- Unmeasured branches: `db-wal-probe`'s exit-2 setup cases (duplicate case id, unknown tag, malformed
  prediction) need edited frozen case data, which is out of bounds for this seat; they remain
  source-read only, as the row itself says every case is frozen.

## 5. Axes

Operability advanced: all seven stated invocations run from a bare clone root with `--lane .`, and every
predicate line in the rows is reproduced; the mandated bwrap wrapper does not disturb the C1 counter.
Verdict-map completeness advanced negatively — F1/F2 show two exit states the round-40 rows cannot
express; F3 shows one entry line that needs a flag the addendum never names; F4 mislabels a control.
Provenance verified: the addendum's R2 edit, red-38/green-39-40 and derived-mapping claims all hold.
No axis harmed; no lane byte written.

Artifacts in this directory: `order-check.out`, `order-r39-receipt.out`, `order-r99.out`,
`order-outside.out`, `order-missing.out`, `round39-c1-audit.log`, `r39-only.out`, `r39-battr38.out`,
`round40-c1.log`, `c1-only-a01.out`, `c1-mistyped.out`, `c1-lanefail.out`, `tool-digests.out`,
`round40-c2.log`, `c2-bogus.out`, `c2-nowork.out`, `absent.out`, `db-wal-probe.log`, `dbwal-dry.out`,
`dbwal-dry2.out`, `dbwal-stage.out`, `dbwal-newwork.out`, `round-close.log`, `rc38.out`, `rc39.out`,
`rc-selftest.out`, `rc-nocensus.out`, `tip-receipts.log`, `tip-list.out`, `c2r39-baseline.out`,
`c2r39-edited-one-line.out`.

VERDICT: registry-commands-match-7/7
