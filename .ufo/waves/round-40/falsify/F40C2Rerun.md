# F40C2Rerun — C2 re-measurement at lane tip `ec1005a2` (round 40, wave 2 falsify)

Seat: executor (leaf). Attacks: the round-40 C2 frozen predicate *as measured on a clean clone of the tip*, plus the
non-vacuity of each of its seven checks. No lane file was edited; every write went to
`/fast/scratch/hyaku/kengaku-r40/F40C2Rerun` (deleted before finishing) or this report dir.

Fixture (verbatim from the seat card):

```
$ S=/fast/scratch/hyaku/kengaku-r40/F40C2Rerun
$ git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane" \
    && git -C "$S/lane" checkout -q ec1005a2a28bc5cfdde7723374368ed4cc956eed
$ git -C "$S/lane" rev-parse --show-toplevel ; git -C "$S/lane" rev-parse HEAD ; git -C "$S/lane" status --porcelain | wc -l
/fast/scratch/hyaku/kengaku-r40/F40C2Rerun/lane
ec1005a2a28bc5cfdde7723374368ed4cc956eed
0
```

Every command below ran inside the host-safety sandbox, with `--lane .` and cwd `$S/lane`:

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
      --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <cmd>
```

Nested `bwrap` (the probe's own `/usr/bin/bwrap --unshare-net …`) was verified working under that outer sandbox with
the probe's exact mount shape before any measurement: `--ro-bind /usr /usr` + `--symlink`es + `--proc /proc --dev /dev`
→ exit 0. Nothing on `PATH`, `/usr`, `/etc`, `/run/user`, `$HOME` was written; no service or background job was started.

## 1. Counter at the tip — PASS

```
$ cd $S/lane && TMPDIR=$S bwrap <sandbox> python3 plans/round40_c2_verify.py --lane . --work "$S/w"   # rc=0
V1 ok listed=8 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=16 distinct_quotes=16 distinct_lines=16 out_of_word_range=0
    gate: P4 ok checked=16 bad=0 first=0
    gate: P5 ok manifest_entries=8 bad=0 first=0
    gate: P6 ok rows=2 bad=0 first=0
    gate: P7 ok source_lines=2 bad=0 first=0
    gate: P8 ok index_rows=47 knowledge_files=47 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=8257
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=2 bad=0
V4 ok cases=28 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=6 tags=6 bad=0
checks=7 defects=0
PREDICATE C2 pass
exit=0
```

Receipt: `F40C2Rerun/c2-verify.out` sha256 `776e515af84140123b485be4b1c9d238e48f769edf33402ac1cd17fb68ce0dfe`.
This reproduces `integrate/measure-final.txt:52-73` (`checks=7 defects=0` / `PREDICATE C2 pass`) byte-for-byte in the
check lines, including `gate: P10 ok probe_rerun=byte-equal bytes=8257`. The frozen sentence the measurement is
compared against is `plans/round-40-claims.md:83-84`: "C2 passes iff `python3 plans/round40_c2_verify.py --lane .` prints
`checks=7 defects=0`, then `PREDICATE C2 pass`, exit 0" (measured there as a clean clone of the landing tip).

## 1b. Tip identity — the landing measurement transfers to the assigned tip

`integrate/measure-final.txt:1` records `TIP ec17216844585d0fecde9f1d4c4be0b78a3bf76f`, which is **not** the tip
this seat was told to measure (`ec1005a2a28bc5cfdde7723374368ed4cc956eed`). Measured relation, in the clone:

```
$ git -C "$S/lane" merge-base --is-ancestor ec17216844585d0fecde9f1d4c4be0b78a3bf76f HEAD ; echo $?
0
$ git rev-list --count ec17216844585d0fecde9f1d4c4be0b78a3bf76f..HEAD
1                      # ec1005a "… shim modules neutralized, wave-2 maker"
$ git diff --name-only ec1721684 HEAD -- plans/db_wal_probe.py plans/pkg_gate.py plans/pkg-spec-r40.json \
    plans/round40_c2_verify.py corpus/evidence/round40 corpus/knowledge/tb2-db-wal-recovery-grader.md \
    corpus/SOURCES.md corpus/README.md plans/round-40-claims.md | wc -l
0
$ git diff --name-only ec1721684 HEAD | cut -d/ -f1-2 | sort | uniq -c
    284 .ufo/waves | 1 corpus/lessons | 1 SCORECARD.md | 1 LOG.md
```

So every input the C2 counter reads is byte-identical between the landing tip and the wave-2 tip; the single
intervening commit changes only `.ufo/waves/*`, `corpus/lessons/round-40.md`, `SCORECARD.md` and `LOG.md`. The
landing measurement and this one are measurements of the same C2 package. (`.ufo/waves` is not read: `grep -c '\.ufo'` over
`plans/round40_c2_verify.py` and `plans/pkg_gate.py` = 0/0, and the probe's single hit is a docstring citation of a
round-39 run log, `plans/db_wal_probe.py:36`.)

## 2. Probe three times — byte-equal 3/3

Each run compared with `cmp` against `corpus/evidence/round40/db-wal-probe.txt` (8257 bytes, sha256
`c74c6b91c8c49b1788f2dd7aa0d66edce0db0b52b549baf89ce69cfa8e2a730e`):

| variant | command suffix | rc | output sha256 | `cmp` |
|---|---|---|---|---|
| plain | `python3 plans/db_wal_probe.py --lane . --work "$S/wp"` | 0 | `c74c6b91…730e` | `PLAIN-IDENTICAL` |
| clean env | `env -i PATH=/usr/bin:/bin HOME=$S python3 …` | 0 | `c74c6b91…730e` | `ENVI-IDENTICAL` |
| hash seed | `env PYTHONHASHSEED=1 python3 …` | 0 | `c74c6b91…730e` | `SEED1-IDENTICAL` |

Receipts `probe-plain.out`, `probe-envi.out`, `probe-seed1.out` — all three hash identically to the receipt itself, so
the `env -i` variant adds nothing observable (no hidden env dependence) and hash-order variance does not reach any
printed line. `wc -c probe-envi.out` = `8257` = the receipt's byte count, matching the gate's
`probe_rerun=byte-equal bytes=8257` (`plans/pkg_gate.py:285`).

## 3. `--dry` against the frozen table — byte-equal

```
$ python3 plans/db_wal_probe.py --lane . --dry > $S/dry.out        # rc=0
$ cmp $S/dry.out corpus/evidence/round40/db-wal-dry-cases-freeze.txt && echo DRY-IDENTICAL
DRY-IDENTICAL
$ sha256sum $S/dry.out corpus/evidence/round40/db-wal-dry-cases-freeze.txt
688f34750eeb0977026dc8d10e036d5a661297297f5d81ef81f79604347044f2  $S/dry.out
688f34750eeb0977026dc8d10e036d5a661297297f5d81ef81f79604347044f2  corpus/evidence/round40/db-wal-dry-cases-freeze.txt
```
`688f34…44f2` is the counter's own `DRY_SHA256` (`plans/round40_c2_verify.py:66`). Dry table shape:
`grep -c '^TAG '` = 6, `grep -c '^CASE '` = 28; receipt `grep -c '^CASE '` = 28 — the two tables agree in count.

## 4. Capture manifest — 8/8 OK

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round40/tb2-db-wal-recovery && sha256sum -c SHA256SUMS
Dockerfile: OK      instruction.md: OK          main.db: OK       main.db-wal.encrypted: OK
solve.sh: OK        task.toml: OK               test.sh: OK       test_outputs.py: OK
rc=0
```
Repeated inside the clone (`(cd $S/lane/corpus/evidence/round40/tb2-db-wal-recovery && sha256sum -c SHA256SUMS)`):
8/8 OK, so the committed capture bytes are the manifest bytes at the tip.

**Three-way digest agreement (measured, not assumed).** For the four names the probe pins, the counter's `CAPTURES`
(`plans/round40_c2_verify.py:49-57`), the probe's `PINS` (`plans/db_wal_probe.py:61-66`) and `SHA256SUMS` carry the
*same* digests: `test_outputs.py 88dc5c2a…ba49`, `solve.sh ed8530c9…f5e8`, `main.db 68cb288e…d119`,
`main.db-wal.encrypted 68753bdc…6e26`. So the probe's own SETUP gate cannot rest on bytes the manifest rejects.

Pinned instruments at the tip, as measured:

```
$ sha256sum corpus/evidence/round40/db-wal-probe.txt plans/db_wal_probe.py corpus/evidence/round40/db-wal-dry-cases-freeze.txt plans/pkg-spec-r40.json plans/pkg_gate.py
c74c6b91…730e  corpus/evidence/round40/db-wal-probe.txt      (= the receipt's own bytes)
69af65df…9ff3  plans/db_wal_probe.py                         (= PROBE_SHA256)
688f3475…44f2  corpus/evidence/round40/db-wal-dry-cases-freeze.txt (= DRY_SHA256)
4af78f4f…8e78  plans/pkg-spec-r40.json                       (= SPEC_SHA256)
ea638822…dd41  plans/pkg_gate.py                             (= GATE_SHA256)
```

## 5. Non-vacuity: five single-file mutations, each detected, each restored

Each mutation was applied to the scratch clone, the full counter re-run, the file restored from a `cp` backup, and the
tree re-checked (`git -C $S/lane status --porcelain | wc -l` → `0` after every one; final run in §6 confirms PASS).

| # | mutation (one file) | counter result | receipt |
|---|---|---|---|
| 1 | append `X` to `…/tb2-db-wal-recovery/main.db` | `V1 DEFECT listed=8 bad=['main.db'] extra=0`; `V2 DEFECT gate_exit=1`; `checks=7 defects=2`; `PREDICATE C2 fail` | `mut1.out` |
| 2 | receipt summary `observed_pass=8 … fail=20` → `9 / 19` | `V4 DEFECT bad=['summary disagrees with the CASE lines']`; `V2 DEFECT` (P10 byte mismatch); `defects=2` | `mut2.out` |
| 3a | requirement map `sorted-by-id` label `enforced` → `partly` | `V7 DEFECT rows=6 tags=6 bad=['sorted-by-id: labelled partly, receipt derives enforced']`; `defects=1` | `mut3a.out` |
| 3b | same row cites `oracle-solve-sh` (a non-violating case) instead of `truth-reversed-order` | `V7 DEFECT bad=['sorted-by-id: cites no case or a case that does not violate it']`; `defects=1` | `mut3b.out` |
| 4 | one hex char flipped in the S119 anchor token in `corpus/SOURCES.md` (`88dc5c2a`→`f8dc5c2a`) | `V3 DEFECT rows=2 bad=['S119:anchor_digest']`; `defects=1`; `V6 ok census_exit=0` | `mut4.out` |
| 5 | append a `CASE phantom-case …` line to the frozen dry table | `V4 DEFECT error ValueError: dry table not at its freeze digest`; `V5 DEFECT probe or dry table not at freeze digest`; `V7 DEFECT error ValueError`; `defects=3` | `mut5.out` |

Reading of the mutation set: V3 (anchor token), V4 (receipt arithmetic), V5 (instrument digests), V7 (derived label and
citation) and V1 (capture bytes) each fail *independently* on a one-file change, and the whole-predicate line follows
(`defects != 0` → `PREDICATE C2 fail`). Mutation 4 also shows V6 does **not** carry the anchor binding — census accepts a
row whose anchor token is wrong (`V6 ok census_exit=0` beside `V3 DEFECT`), so V3 is the only check holding that cell,
which is what its docstring claims (`plans/round40_c2_verify.py:20-22`). Mutation 5 shows a digest-pinned input that
breaks is a defect, never a silent pass (`plans/round40_c2_verify.py:274`: "a check that cannot run is a defect, never a
pass").

Mutations 3a/3b are the round-37 routings re-attacked: the `enforced`-beside-a-passing-violator defect and the
"cite one convenient witness" defect both still fire at this tip.

## 6. Restored state re-measured (the number the verdict rests on)

```
$ git -C "$S/lane" rev-parse HEAD            ec1005a2a28bc5cfdde7723374368ed4cc956eed
$ git -C "$S/lane" status --porcelain | wc -l  0
$ sha256sum … main.db db-wal-probe.txt tb2-db-wal-recovery-grader.md SOURCES.md db-wal-dry-cases-freeze.txt
68cb288e…d119  main.db                     (= pin)
c74c6b91…730e  db-wal-probe.txt            (= receipt)
f51dd9e7…a9ba  tb2-db-wal-recovery-grader.md
6a3ec701…3f06  SOURCES.md
688f3475…44f2  db-wal-dry-cases-freeze.txt (= DRY_SHA256)
$ python3 plans/round40_c2_verify.py --lane . --work "$S/w"   → checks=7 defects=0 / PREDICATE C2 pass   (final.out)
```

## Findings

**F1 (attack on claims:96-97 — "separability"; observation, not a predicate failure at this tip).** The counter is not
lane-self-contained, contrary to the separability sentence "C2 reads only its captures, spec, gate, probe, receipt,
entry, SOURCES and README". V6 shells out to a fleet-root absolute path,
`plans/round40_c2_verify.py:67`: `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`. Receipt: hiding
only that directory under the sandbox (`--tmpfs /home/vgpnk/Projects/shokunin/scripts`, no other change) turns the
predicate over:

```
V6 DEFECT error FileNotFoundError: [Errno 2] No such file or directory: '/home/vgpnk/Projects/shokunin/scripts/sources-census.sh'
checks=7 defects=1
PREDICATE C2 fail
```
(`portability.out`.) Consequence to record: the frozen C2 predicate is reproducible only on a host that has the fleet
scripts tree; a clone measured anywhere else reports a V6 defect that is *not* a package defect. It does not weaken
this tip's PASS, but the sentence at `plans/round-40-claims.md:96` overstates what the counter reads.

**F2 (attack on the counter's own independence).** No check in the counter reads its own program text, and all three
subprocess sites use absolute paths or `sys.executable` (`plans/round40_c2_verify.py:125,197,204`:
`[sys.executable, gate…]`, `[sys.executable, probe… --dry]`, `[CENSUS, …]`) — no `PATH`
lookup, so the wave-1 C1 gaming tactic A2 (a `git`/tool shim earlier on `PATH`) has no hook in this counter. The only
`PATH`-sensitive code is inside the gate/probe sandboxes, whose `env` is a fixed dict
(`plans/db_wal_probe.py:288-289`) and whose `PATH` is the literal `/usr/local/sbin:…:/bin`
(`plans/db_wal_probe.py:72`), not the caller's. Measured consistent with that: the `env -i PATH=/usr/bin:/bin` run
produced the same 8257 bytes (§2).

**F3 (determinism ceiling).** Three runs, including one with an empty environment and one with a pinned hash seed,
agree byte-for-byte with the receipt. The probe's sandbox drops the network (`--unshare-net`) and pins its whole env
dict, so this is the strongest form of the run-to-run claim available without changing the instrument.

## Risks / limits of this receipt

- The measurement is host-scoped by F1: V6 needs `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`.
- The probe needs `/usr/bin/bwrap`, `/usr/bin/sqlite3`, `/usr/bin/xxd`, `/usr/bin/python3` (probe SETUP, exit 2 if
  absent); the counter's V2/V5 need them transitively. Present here.
- V2's P2 is a presence check by design (the counter fills `receipt_sha256` from the receipt it finds); authenticity
  rests on P10's fresh-probe byte compare, which mutation 2 demonstrated bites.
- Mutation detection was checked for V1/V3/V4/V5/V7 and against `PREDICATE C2`; V2 and V6 were exercised only through
  mutation 1 (V2) and the portability probe (V6), not with a dedicated single-file mutation of their own.
- No pacman transaction, no tool install, no service; nothing installed, so no tooling record to file.

Scratch removed: `rm -rf /fast/scratch/hyaku/kengaku-r40/F40C2Rerun` (after copying the `.out` receipts above into
this report's `F40C2Rerun/` directory).

VERDICT: c2-rerun-pass-probe-byte-equal-3/3
