# R45ExecNoHarm — post-landing no-harm measure (kengaku round 45, wave 2, falsify)

Seat `R45ExecNoHarm` (executor, leaf). Scope: **measure the lane TIP**, no lane file edited, no counter/fixture/probe touched,
nothing committed or pushed anywhere, no tool installed. Every run went through
`.ufo/waves/round-45/claims/envelope.sh` (`bwrap`, `/home/vgpnk` read-only, `~/.cache` overlaid from scratch,
`~/.local/bin` content digest bracketed, `exit 4 + INVALID` on any PATH-dir change). No `exit 4` occurred, nothing was re-run.

## Axes (Godspeed)

1. **host-safety** — no write outside scratch: all 15 runs bracketed `before=after=e396f23e40a69201 unchanged` (envelope lines below).
2. **operability** — every older instrument the round-45 landing could have broken, re-run on the tip: round-44 C1/C2, anchor, order, gate-flip, routed, census, round-close 44 **and** 45, plus the frozen-state re-derivation.
3. **fidelity** — instrument digests at the measured tip compared to the frozen pins and to the wave-1 baseline; claim receipts reproduced from a clean clone, not quoted.
4. **reproducibility** — one command line per line of evidence; receipts retained; per-run envelope brackets pasted.

## Setup (exact)

```
S=/fast/scratch/hyaku/kengaku-r45/R45ExecNoHarm ; mkdir -p "$S" ; export TMPDIR="$S"
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" rev-parse --show-toplevel   -> /fast/scratch/hyaku/kengaku-r45/R45ExecNoHarm/lane
git -C "$S/lane" rev-parse HEAD             -> d4c0cdfbdc3886eadac4710ee49630ce00722ee1  ("round-45: lesson + README lesson row")
git -C "$S/lane" status --porcelain         -> (empty; clean clone)
lane HEAD after every run                   -> d4c0cdfbdc3886eadac4710ee49630ce00722ee1 (unchanged; `git status` in the lane shows no
                                               modified `plans/` or `corpus/` file from this seat)
```

The lane tip moved twice while this seat was reading it (`4290d64` → `d4c0cdf`, the L1 landing the lesson + README row), so the
measured object is named by sha and nothing below is attributed to a moving tree.

Instrument identity at the measured tip (`sha256sum plans/<tool>` in the clone):

| tool | tip digest | pin / baseline |
|---|---|---|
| `plans/round44_c1_verify.py` | `6cf05323bafa9cdb…` | = wave-1 baseline digest |
| `plans/round44_c2_verify.py` | `334ce2dac6828f8d…` | = wave-1 baseline digest |
| `plans/anchor_digest_check.py` | `11bb2cad87be1c29…` | = wave-1 baseline digest |
| `plans/order_check.py` | `948d5e1d2b3429d7…` | = wave-1 baseline digest |
| `plans/routed_open.py` | `3ce44d941b14a28c…` | = wave-1 baseline digest |
| `plans/round45_c1_verify.py` | `7745eb0a4bdf281a…` | = `claims/frozen-digests.txt:2` (frozen) |
| `plans/round45_c2_verify.py` | `ab6825e34596ba71…` | = `claims/frozen-digests.txt:3` (frozen) |
| `plans/fixture_fence.py` | `ac65c03293084d7b…` | = the digest the C1 claim receipt records |
| `plans/round_close.py`, `gate_flip_check.py`, `state_check.py` | `cd581f8a…`, `e29e54a0…`, `4aa47a63…` | not in the wave-1 table (recorded here for the next measure) |

## Envelope (verbatim; command line is identical per run except the `env-<name>` dir)

`ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind <S>/env-<name> <S>/env-<name> --bind <S>/env-<name>/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- <cmd…>`

| run | ENVELOPE start | ENVELOPE end |
|---|---|---|
| m1 | `start 23:51:14 cwd=/fast/scratch/hyaku/kengaku-r45/R45ExecNoHarm` | `end 23:51:20 exit=0 local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged` |
| m2 | `start 23:51:14 …` | `end 23:51:23 exit=0 … after=e396f23e40a69201 unchanged` |
| m3 | `start 23:51:14 …` | `end 23:51:16 exit=0 … unchanged` |
| m4 | `start 23:51:14 …` | `end 23:51:16 exit=0 … unchanged` |
| m5 | `start 23:51:25 …` | `end 23:51:27 exit=0 … unchanged` |
| m5b | `start 23:51:25 …` | `end 23:51:27 exit=0 … unchanged` |
| m6 | `start 23:51:25 …` | `end 23:51:26 exit=2 … unchanged` |
| m6b | `start 23:51:25 …` | `end 23:51:27 exit=0 … unchanged` |
| m6c | `start 23:51:28 …` | `end 23:51:31 exit=0 … unchanged` |
| m7 | `start 23:51:32 …` | `end 23:51:40 exit=0 … unchanged` |
| m8 | `start 23:51:32 …` | `end 23:51:38 exit=0 … unchanged` |
| m9 | `start 23:51:28 …` | `end 23:51:30 exit=0 … unchanged` |
| m10 | `start 23:51:28 …` | `end 23:51:30 exit=0 … unchanged` |
| m11 | `start 23:51:28 …` | `end 23:51:30 exit=0 … unchanged` |
| m12 | `start 23:52:54 …` | `end 23:52:58 exit=0 … unchanged` |

All 15: `local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged` (no `INVALID`, no re-run).
The receipt `measure-final.txt` carries every full line verbatim.

## Measure table (tip `d4c0cdf`)

| # | command (in the envelope, `--lane "$S/lane"` unless noted) | measured line(s) | exit | baseline (`b4fcd35`) | delta |
|---|---|---|---|---|---|
| M1 | `plans/round44_c1_verify.py --work "$S/w"` | `PINS total=2 mismatched=0` · `BATTERY fixtures=33 wrong=0 tampered=0 sidechannel=0` · `MUTANTS total=5 killed=5 survived=0 invalid=0 null_detected=0 unattributed=0` · `MUTANTS-BY-TOOL anchor=4/4 order=1/1` · `ADVERTISED direct=5 indirect=0 none=0` · `PINS-AFTER mismatched=0` · **`PREDICATE C1 pass`** | 0 | identical | none |
| M2 | `plans/round44_c2_verify.py` | `V1 ok listed=11` · gate `P1..P10 ok`, `P3 rows=22 distinct_quotes=22`, `P6 rows=9`, `P10 probe_rerun=byte-equal bytes=3630` · `V11 states=48 grader_pass=24 grader_fail=24 disagree=0` · `checks=11 defects=0` · **`PREDICATE C2 pass`** | 0 | same except `P8 index_rows=51 knowledge_files=51` | +1 knowledge file (round-45 entry) |
| M3 | `plans/anchor_digest_check.py` | **`rows=149 tokens=55 defects=0`** | 0 | `rows=141 tokens=47 defects=0` | +8 rows/+8 tokens (S149–S156), defects still 0 |
| M4 | `plans/routed_open.py --list` | **`ROWS total=60 open=23 blocked=1 closed=34 refused=2`** · `routed_open=24 oldest_round=39` | 0 | identical | none (see F1) |
| M5 | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` | 15 `W04` duplicate-url advisories, then `kengaku ok …/kengaku-shokunin/corpus/SOURCES.md` | 0 | identical (same 15 rows) | none |
| M5b | `sources-census.sh validate --file "$S/lane/corpus/SOURCES.md"` | `file ok …/lane/corpus/SOURCES.md` | 0 | not in baseline | new |
| M6 | `plans/round_close.py --round 44` | `ROUND-CLOSE ERROR no census script (scripts/sources-census.sh); pass --census PATH` · `ROUND-CLOSE RESULT ERROR` | 2 | identical | none (pre-existing shape, F5) |
| M6b | `plans/round_close.py --round 44 --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh` | `ORDER RESULT PASS` (`freeze 5f16ed04`, receipt `corpus/evidence/round44/feal-linear-probe.txt`) · `census exit=0 warnings=15 verdict=PASS` · **`ROUND-CLOSE RESULT PASS exit=0`** | 0 | identical | none |
| M6c | `plans/round_close.py --round 45 --census …/sources-census.sh` | `ROUND-CLOSE claims=plans/round-45-claims.md sha256=cb2fae38…` (`= claims/frozen-digests.txt:1`) · `receipts=2`; both round-45 receipts `ORDER RESULT PASS` (`probe-run-envelope.txt`, `password-recovery-probe.txt`) · `census exit=0 warnings=15 verdict=PASS` · **`ROUND-CLOSE RESULT PASS exit=0`** | 0 | not in baseline | new (round-45 close gate green) |
| M7 | `plans/round45_c1_verify.py --work "$S/w45"` | `PINS total=33 mismatched=0` · `FENCE plans/fixture_fence.py sha256=ac65c032…` · 10 `REFUSAL … clean` · **`REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0`** · **`HONEST fixtures=104 admitted=104 refused=0`** · **`CALIBRATION advertised=10 contradicted=0`** · **`PREDICATE C1 pass`** | 0 | `FENCE … absent`, `clean=0 leaked=10`, `admitted=0`, `contradicted=10`, `PREDICATE C1 fail` (exit 1) | **the claim holds at the tip** |
| M8 | `plans/round45_c2_verify.py` | `V1 ok listed=9` · gate `P1..P10 ok`, `P3 rows=19 distinct_quotes=19`, `P5 manifest_entries=9`, `P6 rows=8`, `P8 index_rows=52 knowledge_files=52`, `P9 untracked=0`, `P10 probe_rerun=byte-equal bytes=4659`, `defects=0` · `V2 spec=frozen gate=frozen` · `V4 cases=16 mismatches_named=0/0` · `V7 rows=9 tags=9` · `V8 order_exit=0 result=PASS` · `V11 states=48 grader_pass=18 grader_fail=30 disagree=0` · `checks=11 defects=0` · **`PREDICATE C2 pass`** | 0 | `checks=11 defects=8`, `PREDICATE C2 fail` (freeze-tree instrument mismatch) | **the claim holds at the tip** |
| M9 | `plans/order_check.py --claims plans/round-45-claims.md --receipt corpus/evidence/round45/password-recovery-probe.txt` | `freeze=b4fcd351…` · `receipt_commit=05b02e2b…` · `ORDER ok no claims file committed at or before the receipt shows the frozen probe executed` · **`ORDER RESULT PASS`** | 0 | not run in baseline | new |
| M10 | `plans/gate_flip_check.py --lesson corpus/lessons/round-45.md` | `lesson_round=45 refused_rows=2 malformed_resolutions=0` · `FLIPS total=0 unresolved=0` · `FLIP-CITE entries=- missing=instruction.md,README.md not_fired=0 red=0` | 0 | not in baseline | new (no unresolved flip) |
| M11 | `digcheck.py "$S/lane"` (re-hash every registry) | `FROZEN r39..r45 entries=9/11/11/12/12/12/18 diff=0 absent=0` · **`FROZEN TOTAL entries=85 ok=85 diff=0 absent=0`** | 0 | not in baseline | new (nothing frozen changed) |
| M12 | `plans/state_check.py --root "$S/lane" --summary` | `assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5` · **`VERDICT: PASS — all comparable frozen assertions match`** | 0 | not in baseline | new (the round-45 SCORECARD/README/PROVINCE additions do not break frozen P2/P3/P4) |

### Complete list of lines that differ from the baseline

Only three measurements differ, and each is explained; everything else is line-for-line identical (`measure-final.txt` opens with
a per-measure `diff -u` against `w1/R45NoHarmBaseline/`).

1. **M2** `- gate: P8 ok index_rows=51 knowledge_files=51` → `+ gate: P8 ok index_rows=52 knowledge_files=52` — the round-45
   knowledge entry `knowledge/tb2-password-recovery-grader.md` plus its README index row; still `bad=0`.
2. **M3** `- rows=141 tokens=47 defects=0` → `+ rows=149 tokens=55 defects=0` — the eight new SOURCES rows S149–S156; `defects` unchanged at 0.
3. **M7 / M8** — the two round-45 predicates flip from `fail` to `pass`; that is the landing, listed here so no reader mistakes it for drift:
   - `FENCE plans/fixture_fence.py absent` → `sha256=ac65c032…`; `REFUSALS total=10 clean=0 leaked=10` → `clean=10 leaked=0`;
     `HONEST … admitted=0 refused=104` → `admitted=104 refused=0`; `CALIBRATION contradicted=10` → `contradicted=0`; `PREDICATE C1 fail` → `pass`.
   - `checks=11 defects=8` → `checks=11 defects=0`; `PREDICATE C2 fail` → `pass`. (The eight baseline defects were the freeze-tree
     instrument mismatch `V2..V4,V7..V11 error ValueError: spec template not at its freeze digest`; at the tip every V row is `ok`.)

No measurement regressed: M1 `pass`, M3 `defects=0`, M4 counts and `routed_open=24` identical, M5/M6/M6b identical, M11 `diff=0`, M12 `mismatch=0`.

## Claim reproduction from a clean clone (not quoted — re-run)

- **C2**: my M8 body (non-`ENVELOPE` lines, 111 lines) is **byte-equal** to both frozen receipts —
  `sha256 596d98b59ed7bbc8` for `corpus/evidence/round45/counter-a-run.txt` and `counter-b-run.txt`, measured body identical (`cmp`).
- **C1**: my M7 body (133 lines) differs from `corpus/evidence/round45/c1-counter-run.txt` in **two lines only**, both echoing the
  absolute work dir (`/tmp/k45-c1-k77n5lri/…` in the receipt vs `$S/w45/k45-c1-89ei7lat/…` in mine, in the
  `f2-deep-worktree` and `f6-repo-above-d` detail text). Same fence digest, same 133 lines, same predicate.
- **C2 predictor / probe**: `V5 ok probe=frozen dry_byte_equal=True` and gate `P10 ok probe_rerun=byte-equal bytes=4659` on a fresh
  clone — the probe recipe still reproduces its receipt byte for byte. Older probe: M2 `P10 probe_rerun=byte-equal bytes=3630`,
  the same byte count as the baseline run.
- **C1 calibration controls** were re-read, not re-run: they are variant fences by construction
  (`control-c1-fence-admit_all` `leaked=10`; `refuse_all` `admitted=0 refused=104` → still `fail`; `static_only` `clean=9 leaked=1
  contradicted=1`; `r44-fence` `clean=3 leaked=3 read=4 contradicted=7`), matching `plans/round-45-claims.md:56-62`. The landed fence
  digest `ac65c032` appears in `c1-counter-run.txt` and in my M7 — the control receipts intentionally carry other digests.

## Findings for the L1 (no lane file touched)

- **F1 (operability, measured) — the routed ledger has no round-45 row.** `ROWS total=60` and `routed_open=24` are *identical* to the
  baseline, and `grep -c R45 corpus/routed-findings.jsonl` = `0` (latest ids are `R42-R3-41`). Yet `SCORECARD.md:1994` says
  "the residual call (frozen counters not edited; **routed**): `R45SentinelC2Sandbox`" and `:2006` lists it under "**Routed:**".
  `plans/round-45-claims.md`-grade bookkeeping for round 45 therefore does not reach `plans/routed_open.py`, so the round-close number
  under-counts the round's residuals. This is a bookkeeping gap, not a no-harm regression: no older row changed status.
- **F2 (fidelity, minor)** — `SCORECARD.md:1982-1983` and `LOG.md:1391` name the landing measurement as a clone of `8f9a898`, which is
  two commits behind the tip (`d4c0cdf`, lesson + README lesson row). My tip measure still yields `PREDICATE C1 pass` /
  `PREDICATE C2 pass` and byte-equal C2 receipts, so the statement is not stale in substance; only the named commit is behind. Say
  "`8f9a898` (re-verified at `d4c0cdf`)" if it is ever re-quoted.
- **F3 (reproducibility, minor)** — the C1 receipt is not byte-reproducible: two detail lines interpolate the absolute work dir. A
  reloader comparing bytes sees a false 2-line diff. Normalising those two carriers (or pinning the receipt's expected diff) would
  make the receipt byte-comparable like the C2 one.
- **F4 (host-safety observation)** — the `~/.local/bin` content digest moved between the wave-1 baseline (`c263b11afb1cccf6`,
  23:26–23:29) and this measure (`e396f23e40a69201`, 23:51+): `OpenBot-0.51.1-x86_64.AppImage` appeared at 23:36 and
  `agy.1793063119693176144.old` at 23:51, neither by this seat. Every one of my runs is bracketed `before=after` with that same
  digest, so the measurement is valid; the cross-run digest is not comparable to the baseline's and must not be read as drift by a seat.
- **F5 (pre-existing, unchanged)** — `round_close.py` without `--census` still exits 2 on any lane that keeps
  `scripts/sources-census.sh` in the fleet root: `ROUND-CLOSE ERROR no census script …; pass --census PATH`. Identical to the baseline;
  only the `--census PATH` form is a meaningful green (M6b, M6c).

## What this does and does not settle

Settled: at the tip `d4c0cdf`, on a clean `--shared` clone, the round-44 instruments, anchor, routed, census, round-close (44 and 45),
the frozen-digest registries r39–r45 and the frozen-state re-derivation are all green; the two round-45 predicates hold and reproduce
their receipts; nothing this seat ran wrote outside scratch.
Not settled (other seats' scope): whether the round-45 package's *content* claims (S149–S156 citations, predictor, lesson Gate rows)
are true — the counters say the package is internally consistent, not that the reading is right; and `routed_open --observe` (runs
each row's check) was not executed by this seat, same as the baseline.

## Retained evidence

- `.ufo/waves/round-45/w2/R45ExecNoHarm/measure-final.txt` — sha256 `c1ad07b0406bd9a904bc5b99631033f05b96dad44ef105e884bb0ae0baedb655`,
  750 lines / 69 650 bytes: header, per-measure `diff -u` against the baseline, then all 15 runs verbatim
  (`m1,m2,m3,m4,m5,m5b,m6,m6b,m6c,m7,m8,m9,m10,m11,m12` + exit table).
- `.ufo/waves/round-45/w2/R45ExecNoHarm/claim-reproduction.txt` — sha256 `ec3ef5baee062c0c843a146e4d69b45cedffd851822492590e7dc432519e663b`,
  the C1 two-line diff, the C2 byte-equality hashes, the routed-row grep and M12's verdict line.

## Scratch

`/fast/scratch/hyaku/kengaku-r45/R45ExecNoHarm` (clone + `w`, `w45`, 15 envelope `env-*` dirs, driver scripts) — removed with
`python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r45 R45ExecNoHarm "$S"`
after this report was written.

No tool was installed or upgraded (no `pacman`, no `uv`, no PATH-dir write); nothing to record under the tooling directive.

VERDICT: no-harm-regressions-0
