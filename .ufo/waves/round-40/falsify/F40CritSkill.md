# F40CritSkill — SKILL.md round-40 rows, verified at `ec1005a`

Critic seat, kengaku round 40 wave 2 (falsify). Fixture: clone of the lane at
`ec1005a2a28bc5cfdde7723374368ed4cc956eed` (`git -C ... rev-parse HEAD`), every counter/probe
invocation run inside the mandated `bwrap` wrapper with `--lane` on that clone. After all runs
`git -C <clone> status --porcelain` printed 0 lines and HEAD was unchanged — the tools wrote no lane
byte. Scratch `/fast/scratch/hyaku/kengaku-r40/F40CritSkill` removed before this report.

Scope and counting rule: the 14 body rows of the decision table (`SKILL.md:982-995`, under
`## Database-recovery TB2 grader — round 40`, `SKILL.md:958`) plus the five registry rows
`SKILL.md:590-594` (`order-check`, `round39-c1-audit`, `round40-c1-mutants`, `round40-c2`,
`db-wal-probe`). A row counts **verified** when its invocation, exit codes, printed outputs, pinned
artifacts and controls reproduce on the tip; a row with a false contractual statement counts
**wrong**. Plain citation slips and descriptive labels are filed as findings without flipping a row,
unless they misstate what the tool does or pins.

Receipts in `falsify/F40CritSkill/`: `ordercheck.txt`, `c2.txt`, `c1-mutants.txt`, `audit-full.txt`,
`audit-battery-r38.txt`, `dbw-probe-rerun.txt`, `dbw-dry.txt`, `dbw-stagecheck.txt`,
`dbw-stagefail-exit1.txt`, `c1-duplicate-exit2.txt`, `pins.txt`, `z_dup_module.py`.

## Baseline evidence used by many rows

```
$ python3 plans/db_wal_probe.py --lane . --work <scratch>          # exit 0, 2.7 s
$ cmp <fresh output> corpus/evidence/round40/db-wal-probe.txt && echo receipt_byte_equal=yes
receipt_byte_equal=yes                                             # 8257 bytes, == row's bytes=8257
cases=28 observed_pass=8 observed_fail=20 mismatches=0
regrade cases=28 differ=0
$ python3 plans/db_wal_probe.py --lane . --dry | cmp - corpus/evidence/round40/db-wal-dry-cases-freeze.txt
dry_byte_equal=yes
$ python3 plans/db_wal_probe.py --lane . --stage-check           # exit 0
stagecheck cases=28 failed=0
```

Grader line refs re-read from `corpus/evidence/round40/tb2-db-wal-recovery/test_outputs.py`:
`9` path assert; `15` `json.load`; `30` `required_fields.issubset`; `33-35` isinstance trio;
`43-44` sorted; `53,58` `len==11` + `ids==list(range(1,12))`; `64-66` id 1/2 values; `70-80` names
3-11; `89` duplicate-id; `98,104-107` `len(data)>5` and the two `if`-guarded re-reads.

Independent WAL facts (scratch copies of the captures, read-only):
`enc_first4 753d44c0` → XOR 0x42 → `dec_first4 377f0682`; decrypted read = 11 rows
`(1,apple,150) (2,banana,250) (3,cherry,300) … (11,mango,1100)`; a plain read-write open deletes
the encrypted WAL (`wal_exists_after=False`, 16512 → gone) while `file:…?mode=ro` preserves it
(`wal_after=16512`).

## A. Decision table — 14/14 verified

| # | `SKILL.md` line | claim exercised | receipt / command |
|---|---|---|---|
| 1 | 982 | path test only; `truth-trailing-garbage` `PFFFFFF` (test 1 passes) | receipt:26 `tests=PFFFFFF`; `test_outputs.py:9` |
| 2 | 983 | `json.load` + list + non-empty; object `TypeError` in tests 4,6 | receipt:23 error list `sorted/no_duplicate:error=TypeError`; `:12-18` |
| 3 | 984 | `issubset({"id","name","value"})`; extra keys free, 7/7 | receipt:22 `PPPPPPP`; `:30-32` |
| 4 | 985 | isinstance trio; bool passes, floats fail only test 3 | receipt:31 `PPPPPPP`; :18,:25 `PPFPPPP`; `:33-35` |
| 5 | 986 | `ids==sorted(ids)`; empty list and duplicate lists pass it | receipt:28 `PFPPFPF`, :20,:21 `PPPPFFP`; `:43-44` |
| 6 | 987 | `len==11` then `range(1,12)`; hand-typed 11 ids 7/7 | receipt:15 `PPPPPPP`, :29 `PPPPFPP`; `:53,58` |
| 7 | 988 | `len(set(ids))` cannot fail alone; both dup states already `PPPPFFP` | receipt:20,:21; `:83-89` |
| 8 | 989 | only id 1/2 values read; id 3 = 301 passes 7/7 | receipt:30 `PPPPPPP`; `:64-66` |
| 9 | 990 | names 3-11 only; ids 1-2 wrong 7/7, id 3 wrong `PPPPFPP` | receipt:16,:17; `:70-80` |
| 10 | 991 | `test_wal_was_decrypted` reads export only; string keys pass vacuously | receipt:15 7/7, :24 `PPFFFPP`; `:92-107` |
| 11 | 992 | repaired WAL, no export = `FFFFFFF` | receipt:14 `FFFFFFF` |
| 12 | 993 | wrong key 0x43 = `PPPPFPF`; WAL magic `37 7f 06 82` | receipt:11; magic measured `377f0682` |
| 13 | 994 | plain rw open first = `PPPPFPF`; rw open deletes the WAL | receipt:10; destructive-read test above |
| 14 | 995 | `empty-app`/`untouched` `FFFFFFF`, oracle and both decrypt routes 7/7 | receipt:6,7,8,12,13 |

Prose numbers re-derived from the receipt (script over `CASE … violates=` lines):
`fix-wal 23/5 pass`, `extract-all 15/4`, `json-at-path 5/0`, `record-format 8/2`,
`sorted-by-id 1/0`, `eleven-records 10/0` — identical to `SKILL.md:1005-1012`; V7 re-derives them
in the green c2 run (`V7 ok rows=6 tags=6 bad=0`). Frozen table `:1-6` carries the six `TAG` lines.
Host `sqlite3` is 3.54.0 and `task.toml:29,34`, `Dockerfile:3,14-15`, `test.sh:18-29`,
`solve.sh:8-10` all read as cited.

## B. Registry rows — 4 verified, 1 wrong

| row | `SKILL.md` | what reproduces | verdict |
|---|---|---|---|
| `order-check` | 590 | all three outputs: exit 0 `ORDER ok …` / `ORDER RESULT PASS`, `freeze=bbb1095`, `receipt_commit=055748f`, `scanned commits=1 file_entries=12`; `--receipt …round39…` → `ORDER FAIL freeze-contains-receipt receipt-before-claims hits=0`, exit 1; `--claims round-99` → `ORDER ERROR claims not committed in HEAD`, exit 2. No `selftest` symbol; imports only argparse/re/subprocess/sys/pathlib. | verified |
| `round39-c1-audit` | 591 | green: `PINS total=26 mismatched=0`, `BATTERY fixtures=90 wrong=0 …`, `MUTANTS 7 killed=7`, `PINS final … 0`, `AUDIT C1 clean`, `PREDICATE C1 pass`, exit 0 (76.7 s); `--only M01` → `n/a`; unpinned module → `AUDIT unpinned battery module present`, exit 2; absent `--work` → `FileNotFoundError`, exit 1; `--battery r38` → exit 1, `killed=3 survived=4`, `n/a` (finding F2). | verified (F2/F3/F4) |
| `round40-c1-mutants` | 592 | green: `PINS total=3 mismatched=0`, `BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass`, exit 0; `--only A01` → `n/a`, exit 0; duplicate fixture id → `SETUP duplicate fixture id`, exit 2; tool digests `11bb2cad/853bcb2a/948d5e1d` match `PINS`; three control files read as described (`nothing`: fixtures=0, killed=0 survived=21, exit 1; `tool-edited`: `PINS mismatched=1`, A01–A27 (11) `invalid`; `hostile-daemon`: fixture unchanged, killed=0, counterfactual `SOURCES.md changed after 6 s = True`). | verified |
| `round40-c2` | 593 | green: `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0; `gate: P10 ok probe_rerun=byte-equal bytes=8257`; all 12 pinned digests (spec, gate, probe, dry table, 8 captures) match `pins.txt`; control `control-c2-nothing.txt` = `defects=4` (V2 V3 V4 V7); absent `--work` → `FileNotFoundError` traceback, exit 1. | verified |
| `db-wal-probe` | 594 | invocation, exit map (`0` rerun byte-equal 8257; `1` only under a failing stage — patched-copy receipt `STAGECHECK empty-app rc=3 recipe rc=1`, `stagecheck … failed=1`, exit 1; `2` setup at `:314-315,327-328,331-332,337-338,362-364`), sandbox flags (`--unshare-net/-pid/-ipc`, `/usr`,`/etc` ro, fresh `/app`, cwd `/app`, `bash -euo pipefail`), `--dry`/`--stage-check` semantics all hold — **but its pinned-values cell is false**: the probe pins **four** captures, not eight (F1). | **wrong** |

## Findings

**F1 — `db-wal-probe` row overstates its pin set (contractual; flips the row to wrong).**
Cell: “`PINS` in the probe: the eight captures … and six more, each checked before any case”
(`SKILL.md:594`). Measured: the probe’s `PINS` dict has four keys —
`['test_outputs.py','solve.sh','main.db','main.db-wal.encrypted']` (`pins.txt`; `plans/db_wal_probe.py:61-66`)
— and the committed receipt prints exactly four `# capture …` lines (`db-wal-probe.txt:2-5`). The
other four captures are pinned in `plans/round40_c2_verify.py:49-58` `CAPTURES` (8 entries, V1
`listed=8`). The probe never reads `Dockerfile`, `instruction.md`, `task.toml` or `test.sh`
(`grep` finds no such file opened). Second half of the same cell also misfiles the receipt digest:
`round40_c2_verify.py` has no receipt-digest constant (`SPEC`’s `receipt_sha256` is `null`,
`pkg-spec-r40.json:6`); V2 fills it live into the effective spec and gate `P2`/`P10` use it, while
V4 checks case ids + summary and V5 pins probe + dry table (c2 receipt `V4 ok cases=28 …`,
`V5 ok probe=frozen dry_byte_equal=True`).

**F2 — `round39-c1-audit`: the “do-nothing” arm is not do-nothing (descriptive; row stays verified).**
`--battery r38` (the label comes from `plans/round39_c1_audit.py:63`) printed
`BATTERY fixtures=86 … MUTANTS total=7 killed=3 survived=4`, `PREDICATE C1 n/a`, exit 1. M01, M05,
M06 die on round-36/37/38 fixtures. The row’s exit-1 map already declares “a development subset
whose killed set is not clean (`:423-425`)”, so the contract is accurate; only the label needs the
qualifier.

**F3 — timing cell not reproduced (environment).** Full audit 76.7 s wall on this host under nested
bwrap with sibling jobs; the row’s `55 s` is wave-1’s idle-host measurement
(`.ufo/waves/round-40/build/R40RegistryRows.md:159-167`, `rc=0 # 55.18 s wall`). Not a contract
defect; the row should say “55 s measured on an idle host”.

**F4 — cite range off by one line.** The audit row lists `PINS final … mismatched=0` inside the
`:418-428` block, but it prints at `plans/round39_c1_audit.py:417` (418 is
`AUDIT nondeterministic_kills`). Correction: `:417-428`.

**F5 — decision-table wording vs code (content right).** “the ground-truth table … is computed from
the two captured files under XOR key 0x42 … (`plans/db_wal_probe.py:25-29`)” reads as runtime
derivation, but `TRUTH` is a literal comprehension at `plans/db_wal_probe.py:86`; the values do
equal an independent XOR-0x42 read of the captures (baseline above), so only the wording (“was
derived from”) needs the edit.

## Smallest safe correction (F1, one cell, no script or artifact change)

Replace in `SKILL.md:594`:

> `PINS` in the probe: the eight captures (`test_outputs.py` `88dc5c2a…`, `solve.sh` `ed8530c9…` and
> six more, each checked before any case); the frozen dry table and the receipt digest are pinned by
> `plans/round40_c2_verify.py` (V4, V5)

with:

> `PINS` in the probe: four captures — `test_outputs.py` `88dc5c2a…`, `solve.sh` `ed8530c9…`,
> `main.db` `68cb288e…`, `main.db-wal.encrypted` `68753bdc…` — each checked before any case; the
> other four captures are pinned in `plans/round40_c2_verify.py` `CAPTURES` and checked by V1. The
> dry-table digest is pinned by V5; the receipt has no frozen digest (spec `receipt_sha256` null) —
> its authenticity rests on V2’s effective spec and gate `P10`’s fresh-run byte compare.

Plus F2’s six-word qualifier and F4’s `:417-428`; F3/F5 are optional wording fixes.

## Limits of this seat

- Terminal-Bench, the task image and the TB harness were not run — the row says they are not (probe
  limits, `plans/db_wal_probe.py:14-20`); I did not contradict that.
- The probe’s `regrade=` is a same-process determinism read, not re-run stability; I re-ran the whole
  probe once and got a byte-equal receipt, which is re-run evidence for *this* host only.
- `z_dup_module.py` is a synthetic duplicate-fid module I wrote into a copy of `plans/battery40`
  under scratch to exercise the exit-2 arm; it is not a lane file.
- No pacman/uv installs were needed; nothing was installed or upgraded.

VERDICT: skill-rows-verified-18/19
