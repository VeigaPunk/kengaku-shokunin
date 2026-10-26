# F40MapControl raw run logs (C2 V7 map controls), 2026-10-26

Detector command for every run below (only `<STATE>` varies — pristine / mutated / restored):
`cd $S/lane && bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent python3 plans/round40_c2_verify.py --lane "$S/lane" --work "$S"` with `S=/fast/scratch/hyaku/kengaku-r40/F40MapControl`, `TMPDIR=$S`.
Clone: `git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane" && git -C "$S/lane" checkout -q ec1005a2a28bc5cfdde7723374368ed4cc956eed`; `git -C "$S/lane" rev-parse --show-toplevel` = `/fast/scratch/hyaku/kengaku-r40/F40MapControl/lane`.
Pristine entry `corpus/knowledge/tb2-db-wal-recovery-grader.md` sha256 `f51dd9e7766de9a96f7efe96582aadc3f39e24e9b2c2a4975b0b35c29649a9ba` (saved copy `$S/entry.pristine.md`).

## Baseline (pristine)

```
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
EXIT=0
```

## M1 fix-wal label partly→enforced (mutated sha256 c5fa6f9ad0007753dfd5ee173b147ff12c6d13bc2791a9081f4971af1ac35818)

```
V1 ok listed=8 bad=0 extra=0
    gate: P1..P10 ok, gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=2 bad=0
V4 ok cases=28 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 DEFECT rows=6 tags=6 bad=['fix-wal: labelled enforced, receipt derives partly']
checks=7 defects=1
PREDICATE C2 fail
EXIT=1
```
(Full gate block identical to baseline; elided here for width, seen in full on the run.)

## M2 extract-all label partly→unenforced (mutated sha256 1556d313e69e3eae5fb8ec9215069c7321298e95ee33164d0a29c28d08353d0b)

```
V1 ok listed=8 bad=0 extra=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=2 bad=0
V4 ok cases=28 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 DEFECT rows=6 tags=6 bad=['extract-all: labelled unenforced, receipt derives partly']
checks=7 defects=1
PREDICATE C2 fail
EXIT=1
```

## M3 json-at-path label enforced→partly (mutated sha256 af29d464facadd6f52422a86dd1584259e67f0302c6d6d58f83842af8ca1cb90)

```
V7 DEFECT rows=6 tags=6 bad=['json-at-path: labelled partly, receipt derives enforced']
checks=7 defects=1
PREDICATE C2 fail
EXIT=1
```
(V1-V6 ok as in M2; same filter.)

## M4 record-format label partly→enforced (mutated sha256 8693bf689c97a3c04525add1d0fc31a24aca029c8d6f445f38a24e174c2dd03e)

```
V7 DEFECT rows=6 tags=6 bad=['record-format: labelled enforced, receipt derives partly']
checks=7 defects=1
PREDICATE C2 fail
EXIT=1
```

## M5 sorted-by-id label enforced→unenforced (mutated sha256 b026fe29be0e30667e7d19492edb43f58aa2b2102352f408047cd87e97f6c19d)

```
V7 DEFECT rows=6 tags=6 bad=['sorted-by-id: labelled unenforced, receipt derives enforced']
checks=7 defects=1
PREDICATE C2 fail
EXIT=1
```

## M6 eleven-records label enforced→partly (mutated sha256 ce652153582c7ffb6641678a8e746c45ca3cc1348a8afa48e4336a5a648c8604)

```
V7 DEFECT rows=6 tags=6 bad=['eleven-records: labelled partly, receipt derives enforced']
checks=7 defects=1
PREDICATE C2 fail
EXIT=1
```

## M7 cite non-violating case `oracle-solve-sh` in sorted-by-id row (mutated sha256 23755cee238a251fbf1b9252a2b95adaabedf3cbca3e67b4acd9765ef7d25839)

```
V7 DEFECT rows=6 tags=6 bad=['sorted-by-id: cites no case or a case that does not violate it']
checks=7 defects=1
PREDICATE C2 fail
EXIT=1
```

## M8 drop the sorted-by-id row (mutated sha256 dd2dd578a9a54506369eea27aef656f90451080cc5b32a64a942bb73238e37a9)

```
V7 DEFECT rows=5 tags=6 bad=["tags missing=['sorted-by-id'] duplicated=0"]
checks=7 defects=1
PREDICATE C2 fail
EXIT=1
```

## M9 duplicate the sorted-by-id row (mutated sha256 26a4fea4df3ad35cf351f46a765647594fc82636ddd227d10a5988b78b67b7a4)

```
V7 DEFECT rows=7 tags=6 bad=["tags missing=0 duplicated=['sorted-by-id']"]
checks=7 defects=1
PREDICATE C2 fail
EXIT=1
```

## M10 fix-wal line number instruction.md:7→instruction.md:6 (mutated sha256 aebc1e41c73c48697de809345fb61d88a5d5ca17538dca0fe82c1c2cbe688fb4)

```
V7 DEFECT rows=6 tags=6 bad=['fix-wal: line 6 is not the frozen instruction.md:7']
checks=7 defects=1
PREDICATE C2 fail
EXIT=1
```

## Restoration evidence

After every mutation the pristine bytes were copied back (`cp "$S/entry.pristine.md" "$E"`) and the sha256 re-checked: `f51dd9e7766de9a96f7efe96582aadc3f39e24e9b2c2a4975b0b35c29649a9ba` — 10/10 identical to pristine. Final run on restored bytes:

```
V1 ok listed=8 bad=0 extra=0
    gate: P1..P10 ok, gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=2 bad=0
V4 ok cases=28 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=6 tags=6 bad=0
checks=7 defects=0
PREDICATE C2 pass
EXIT=0
```

`git -C "$S/lane" status --porcelain` → empty; `git -C "$S/lane" rev-parse HEAD` → `ec1005a2a28bc5cfdde7723374368ed4cc956eed`.
