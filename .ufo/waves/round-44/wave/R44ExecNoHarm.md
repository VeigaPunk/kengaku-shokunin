# Round 44 wave — R44ExecNoHarm: no-harm baseline at the receipt commit

Seat `R44ExecNoHarm` (executor, leaf). Lane untouched; every measurement ran in a clean `git clone --no-local` of
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` detached at the round-44 receipt commit
`45dc0bc81e42e02ecd272712086c372c8844b108`, inside the round-44 envelope (`claims/envelope.sh`): home read-only,
`~/.local/bin` content digest bracketed, `date +%T` at both ends. Nothing was installed (python3 `3.14.8`,
`/usr/bin/bwrap` already present), no subagent or labrat was used, no lane file was written.

Axes moved: **operability** (the whole round-36→44 instrument set runs end-to-end at this tree from committed bytes,
arguments taken as `<clone> --work <dir>`) and **calibration** (the two round-44 counters are red in exactly the shape
their freeze controls prescribe, and the only other reds are the two round-38 reds carried byte-identically from the
round-42/43 baselines).

Script: `.ufo/waves/round-44/wave/R44ExecNoHarm/measure.sh` (sha256
`fa3843a87155f1ce8fdd682f68ef5e4b59c1775484906704ce2366dc76e4f977`), adapted from
`.ufo/waves/round-43/integrate/measure.sh` — round-44 counters first, then the full round-43 measured set, plus the
round-44 frozen digests, `round_close --round 44`, the two `gate_flip_check` lessons and `feal_probe` byte-equality.
Usage, enforced by the script itself:

```
measure.sh <clone> --work <dir>     # clone must be a git work-tree top; <dir> must lie outside it
```

Receipt: `.ufo/waves/round-44/wave/R44ExecNoHarm/no-harm-baseline.txt`
(sha256 `301cc8d31593f5be28f26299c2034456410899c196080e909fbc440bb3afef1d`, 98 180 bytes, 1 153 lines).

## Envelope (QUALITY Q32, all three lines verbatim, receipt `:1`, `:2`, `:1153`)

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44ExecNoHarm/env /fast/scratch/hyaku/kengaku-r44/R44ExecNoHarm/env --bind /fast/scratch/hyaku/kengaku-r44/R44ExecNoHarm/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44ExecNoHarm/measure.sh /fast/scratch/hyaku/kengaku-r44/R44ExecNoHarm/lane --work /fast/scratch/hyaku/kengaku-r44/R44ExecNoHarm/w
ENVELOPE start 20:58:43 cwd=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44ExecNoHarm
ENVELOPE end 21:10:57 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

`local_bin_content_before = after` (content digest, not names) ⇒ the measurement counts; envelope exit 0, wall 12 m 14 s.
Clone facts (`:3-7`): `HEAD 45dc0bc… · untracked_in_clone=0 · python3=/usr/bin/python3 Python 3.14.8 · bwrap=/usr/bin/bwrap`.

## Result: 40 green of 44 checks (`:1147`)

`SUMMARY total=44 green=40 red=4` · `:1148-1151` `RED r44-c1 expected-red`, `RED r44-c2 expected-red`,
`RED r38-order carried-red`, `RED r38-c1 carried-red` · `:1152 NO-HARM-BASELINE 40-green-of-44 expected_red=2
carried_red=2 unexpected_red=0`. Green = exit 0; the four probe checks also require byte-equality.

### Round-44 counters first (expected red at this commit)

| # | check | exit | decisive line (receipt) |
|---|---|---|---|
| 1 | `round44_c1_verify.py --lane .` | **1** | `:10 PINS total=2 mismatched=0` · `:16 BATTERY fixtures=0 wrong=0 tampered=0 sidechannel=0` · `:17 MUTANTS total=5 killed=0 survived=5 invalid=0 null_detected=0 unattributed=0` · `:18 MUTANTS-BY-TOOL anchor=0/4 order=0/1` · `:19 ADVERTISED direct=5 indirect=0 none=0` · `:20 PINS-AFTER mismatched=0` · `:21 PREDICATE C1 fail` |
| 2 | `round44_c2_verify.py --lane .` | **1** | `:42 V8 ok order_exit=0 result=PASS` · `:46 checks=11 defects=7` · `:47 PREDICATE C2 fail` |
| 3 | `order_check.py` round 44 | 0 | `:51 freeze=5f16ed04…` · `:52 receipt_commit=45dc0bc8…` · `:53 scanned commits=1 file_entries=32` · `:54 ORDER RESULT PASS` |

### Counters rounds 36-43 (the round-43 set)

| # | check | exit | decisive line |
|---|---|---|---|
| 4 | `round43_c1_verify.py` | 0 | `:110 BATTERY fixtures=42 wrong=0 tampered=0 sidechannel=0` · `:111 MUTANTS total=9 killed=9 survived=0` · `:112 anchor=6/6 order=3/3` · `:115 PREDICATE C1 pass` |
| 5 | `round43_c2_verify.py` | 0 | `:139 checks=10 defects=0` · `:140 PREDICATE C2 pass` |
| 6 | `order_check.py` round 43 | 0 | `:147 ORDER RESULT PASS` |
| 7 | `round42_c1_verify.py` | 0 | `:194 fixtures=29` · `:195 MUTANTS total=14 killed=14` · `:199 PREDICATE C1 pass` |
| 8 | `round42_c2_verify.py` | 0 | `:222 checks=9 defects=0` · `:223 PREDICATE C2 pass` |
| 9 | `order_check.py` round 42 | 0 | `:230 ORDER RESULT PASS` |
| 10 | `round41_c1_verify.py` | 0 | `:305 fixtures=48` · `:306 MUTANTS total=23 killed=23` · `:310 PREDICATE C1 pass` |
| 11 | `round41_c2_verify.py` | 0 | `:332 checks=8 defects=0` · `:333 PREDICATE C2 pass` |
| 12 | `order_check.py` round 41 | 0 | `:340 ORDER RESULT PASS` |
| 13 | `round40_c1_verify.py` | 0 | `:386 fixtures=21` · `:387 MUTANTS total=21 killed=21` · `:389 PREDICATE C1 pass` |
| 14 | `round40_c2_verify.py` | 0 | `:410 checks=7 defects=0` · `:411 PREDICATE C2 pass` |
| 15 | `order_check.py` round 40 | 0 | `:418 ORDER RESULT PASS` |
| 16 | `order_check.py` round 39 | 0 | `:425 ORDER RESULT PASS` |
| 17 | `order_check.py` round 38 | **1** (carried) | `:431 ORDER HIT …control-c2-skip.txt@e0a378539a45:11 kind=gate-p10` · `:433 ORDER RESULT FAIL` |
| 18 | `round39_c1_verify.py` | 0 | `:527 fixtures=90` · `:535 MUTANTS total=7 killed=7` · `:536 PREDICATE C1 pass` |
| 19 | `round39_c2_verify.py` | 0 | `:557 checks=7 defects=0` · `:558 PREDICATE C2 pass` |
| 20 | `round38_c1_verify.py` | **1** (carried) | `:648 fixtures=86` · `:669 MUTANT N21 D5 silence SURVIVED` · `:671 MUTANTS total=22 killed=21 survived=1` · `:672 PREDICATE C1 fail` |
| 21 | `round38_c2_verify.py` | 0 | `:693 checks=7 defects=0` · `:694 PREDICATE C2 pass` |
| 22 | `round37_c1_verify.py` | 0 | `:762 fixtures=64` · `:818 MUTANTS total=55 killed=55` · `:819 PREDICATE C1 pass` |
| 23 | `round37_c2_verify.py` | 0 | `:840 checks=7 defects=0` · `:841 PREDICATE C2 pass` |
| 24 | `round36_c2_verify.py --lane .` | 0 | `:850 checks=6 defects=0` · `:851 PREDICATE C2 pass` |

### Tools, census, frozen digests r39-r44

| # | check | exit | decisive line |
|---|---|---|---|
| 25 | `anchor_digest_check.py --lane .` | 0 | `:855 rows=130 tokens=36 defects=0` |
| 26 | `sources-census.sh validate --file corpus/SOURCES.md` | 0 | `:873 file ok …/lane/corpus/SOURCES.md` (15 `W04` duplicate-url warnings, ×4 runs incl. the three `round_close` runs; warnings do not fail) |
| 27 | `sha256sum -c …/round-44/claims/frozen-digests.txt` | 0 | 12/12 `OK` (`:876-887`) |
| 28 | `sha256sum -c …/round-43/claims/frozen-digests.txt` | 0 | 12/12 `OK` (`:890-901`) |
| 29 | `sha256sum -c …/round-42/claims/frozen-digests.txt` | 0 | 12/12 `OK` (`:904-915`) |
| 30 | `sha256sum -c …/round-41/claims/frozen-digests.txt` | 0 | 11/11 `OK` (`:918-928`) |
| 31 | `sha256sum -c …/round-40/claims/frozen-digests.txt` | 0 | 11/11 `OK` (`:931-941`) |
| 32 | `sha256sum -c …/round-39/claims/frozen-digests.txt` | 0 | 9/9 `OK` (`:944-952`) |

67 `: OK` lines total across the six files, zero `FAILED` (`grep -c ': OK$'` = 67; `grep -c FAILED` = 0). That includes
the round-44 freeze surfaces themselves: `plans/round-44-claims.md`, `round44_c1_verify.py`, `round44_c2_verify.py`,
`feal_linear_probe.py`, `pkg-spec-r44.json`, `pkg_gate.py`, `anchor_digest_check.py`, `order_check.py`, the dry table,
the TB2 `SHA256SUMS`, `claims/witness/w_u.py`, `claims/envelope.sh`.

### Ledgers and probes

| # | check | exit | decisive line |
|---|---|---|---|
| 33 | `ledger_tip.py --source <clone> --work` | 0 | `:956 TIP commit=45dc0bc8…` · `:969 rows=9 closed=9 observed_pass=9 mismatches=0` |
| 34 | `tip_receipts.py --lane . --work` | 0 | `:1019 receipt corpus/evidence/round44/feal-linear-probe.txt equal bytes=3630 exit=0` · `:1022 receipts=30 byte_equal=10 differ=0 skipped=20` |
| 35 | `routed_open.py` | 0 | `:1025 ROWS total=60 open=38 blocked=1 closed=21 refused=0` · `:1026 routed_open=39 oldest_round=39` |
| 36 | `db_wal_probe.py` byte-equality | 0 | `:1029 exit=0 byte_equal=yes` vs `corpus/evidence/round40/db-wal-probe.txt` |
| 37 | `constraints_probe.py` byte-equality | 0 | `:1032 exit=0 byte_equal=yes` vs `corpus/evidence/round41/constraints-probe.txt` |
| 38 | `fibsqrt_probe.py` byte-equality | 0 | `:1035 exit=0 byte_equal=yes` vs `corpus/evidence/round42/fibsqrt-probe.txt` |
| 39 | `feal_probe.py` byte-equality | 0 | `:1038 exit=0 byte_equal=yes` vs `corpus/evidence/round43/feal-probe.txt` |

### Round close and flip checks

| # | check | exit | decisive line |
|---|---|---|---|
| 40 | `round_close.py --round 42` | 0 | `:1070 ROUND-CLOSE RESULT PASS exit=0` |
| 41 | `round_close.py --round 43` | 0 | `:1101 ROUND-CLOSE RESULT PASS exit=0` |
| 42 | `round_close.py --round 44` | 0 | `:1112 ORDER RESULT PASS` · `:1132 ROUND-CLOSE RESULT PASS exit=0` |
| 43 | `gate_flip_check.py --lesson corpus/lessons/round-42.md` | 0 | `:1138 FLIPS total=2 unresolved=0` |
| 44 | `gate_flip_check.py --lesson corpus/lessons/round-43.md` | 0 | `:1144 FLIPS total=2 unresolved=0` |

`round_close --round 44` green is a scope note, not an admission: it checks claims digest, receipt presence, order and the
census, not the C1/C2 predicates. Items 1–2 are the admission facts.

## The four reds, and why none is harm

1–2. **The round-44 counters are red exactly as the freeze controls say.** `r44-c1` reproduces
`claims/control-c1-nothing.txt` line for line — `PINS total=2 mismatched=0`, `BATTERY fixtures=0`,
`MUTANTS total=5 killed=0 survived=5 … unattributed=0`, `MUTANTS-BY-TOOL anchor=0/4 order=0/1`,
`ADVERTISED direct=5`, `PINS-AFTER mismatched=0`, `PREDICATE C1 fail` — with the same five survivor ids
(U5 U6 U7 U9 U14c) and the same advertised quotes. There is no `plans/battery44` at this commit
(`git ls-tree 45dc0bc plans/battery44` → empty). `r44-c2` reports `checks=11 defects=7`; the freeze control ran in the
lane worktree *before* the receipt was committed and reported `checks=11 defects=8` with `V8 DEFECT order_exit=2
result=not-PASS`. The single-defect difference is exactly **V8**, which now passes (`:42 V8 ok order_exit=0
result=PASS`) because the receipt is committed after the freeze (`:51-54`, `freeze=5f16ed04 → receipt_commit=45dc0bc8`).
That is the expected wave-1 state and it is one defect *fewer* than the control, not a regression.

3. **`r38-order` is carried, byte-identical in kind**: same `ORDER HIT …control-c2-skip.txt@e0a378539a45:11
kind=gate-p10` line, same `hits=1`, as the round-43 baseline
(`.ufo/waves/round-43/build/R43ExecNoHarm/measure-v1.txt:339`) and the round-42 baseline
(`.ufo/waves/round-42/integrate/measure-tip3.txt`). Round-38 routed work.

4. **`r38-c1` is carried, same id and counts**: `MUTANT N21 D5 silence SURVIVED`, `MUTANTS total=22 killed=21
survived=1`, matching round-43 `measure-v1.txt:577` and round-42 `measure-tip3.txt:520-529`. Round-38 routed work.

## Deltas against the round-43 baseline (explained, not hidden)

| surface | round 43 | round 44 | cause |
|---|---|---|---|
| `anchor_digest_check` | `rows=121 tokens=27` | `rows=130 tokens=36` | S138–S146 (9 rows, 9 anchor tokens) landed this round |
| `tip_receipts` | `receipts=29 byte_equal=9 differ=0` | `receipts=30 byte_equal=10 differ=0` | the round-44 receipt re-runs byte-equal: `equal bytes=3630 exit=0` (`:1019`) |
| `routed_open` | `ROWS total=16 open=9` | `ROWS total=60 open=38` | the round-43 landing commits added 46 ledger rows: `git diff --stat 6b49694 45dc0bc -- corpus/routed-findings.jsonl` → `1 file changed, 46 insertions(+), 2 deletions(-)` (`8adf76c`, `77ea425`) |
| registry | `rows=121` | `rows=130` | same nine S-rows |

## Instrument iteration (the script was wrong first; the tree was not)

- **v1** (`measure-v1-workdir-bug.txt`, sha256 `b9c25532…`): I passed one fresh `--work` subdirectory per counter, but
  round-36→42 counters read `--work` without creating it, so seven checks died in `tempfile.mkdtemp(..., dir=…)` with
  `FileNotFoundError` (r40-c2, r39-c1, r39-c2, r38-c1, r38-c2, r37-c1, r37-c2) and reported as red. Fix: the script
  pre-creates every work dir (`measure.sh:34-39`), as round-43's one shared `$S/w` did implicitly. No number from v1 is
  used anywhere in this report.
- **v2** (`measure-v2-unlabeled-reds.txt`, sha256 `8ec2a554…`): all 44 checks ran; summary labelled the two carried
  round-38 reds `UNEXPECTED-RED` (`unexpected_red=2`, envelope exit 1).
- **v3** (the receipt, `no-harm-baseline.txt`): the same 44 checks plus an explicit three-way red classification
  (`expected-red` from the freeze controls, `carried-red` with their round-42/43 evidence in a comment, `UNEXPECTED`
  otherwise) and an inverse guard — an expected red that comes back **green** is flagged `MISSING-RED` and also fails
  the run. Result: `unexpected_red=0`, envelope exit 0. v2 and v3 agree on every check exit and every decisive count.

## Host safety

Every battery, counter, fixture build and probe in this report ran inside
`.ufo/waves/round-44/claims/envelope.sh`: `/home/vgpnk` read-only, `~/.cache` overlay scratch-backed, `~/.local/bin`
content-hashed before and after (unchanged, `328be01808ba022f`, all three runs). No file was written to `/usr`, `/etc`,
`~/.local/bin` or any PATH directory; nothing was installed or upgraded (no pacman, no `uv tool`, no `npx`). Writes
went only to `/fast/scratch/hyaku/kengaku-r44/R44ExecNoHarm/` (clone, work dirs, envelope dir) and to this wave
directory. The lane was never written; the clone's top level was asserted (`:3`) and every counter ran with
`--lane .` / `--source <clone>` from inside it.

## Risks / blockers

- Pinned to the **receipt** commit. Wave 2 must re-run this script at the landing tip; only then may `r44-c1`/`r44-c2`
  flip green (the script then prints `MISSING-RED`, which is the intended alarm).
- The two carried round-38 reds stay red until round-38 routed work lands; they must not be attributed to round 44.
- `db_wal_probe` byte-equality is now checked explicitly (round 43 only checked its exit); it reproduces its receipt
  exactly at this tree, so the class is safe to keep.
- No blocker. Scratch `/fast/scratch/hyaku/kengaku-r44/R44ExecNoHarm` held the clone, the three work trees and the
  envelope dirs; it was removed with `plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r44 R44ExecNoHarm <S>`.

VERDICT: no-harm-baseline-40-green-of-44
