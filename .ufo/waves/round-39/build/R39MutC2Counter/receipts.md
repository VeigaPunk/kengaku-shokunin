# Receipts — R39MutC2Counter (verbatim counter outputs)

All runs: `cd /fast/scratch/hyaku/kengaku-r39/R39MutC2Counter/lane && TMPDIR=/fast/scratch/hyaku/kengaku-r39/R39MutC2Counter python3 plans/round39_c2_verify.py --lane . --work /fast/scratch/hyaku/kengaku-r39/R39MutC2Counter/w`

## Baseline (pristine green package)

```
V1 ok listed=7 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=29 distinct_quotes=29 distinct_lines=29 out_of_word_range=0
    gate: P4 ok checked=29 bad=0 first=0
    gate: P5 ok manifest_entries=7 bad=0 first=0
    gate: P6 ok rows=2 bad=0 first=0
    gate: P7 ok source_lines=2 bad=0 first=0
    gate: P8 ok index_rows=46 knowledge_files=46 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=5867
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=2 bad=0
V4 ok cases=25 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=4 tags=4 bad=0
checks=7 defects=0
PREDICATE C2 pass
exit=0
```

## M01 — entry map: secret-gone label partly → enforced

```
V7 DEFECT rows=4 tags=4 bad=['secret-gone: labelled enforced, receipt derives partly']
checks=7 defects=1
PREDICATE C2 fail
exit=1
```

## M02 — entry map: files-untouched row cites message-rewritten (non-violating)

```
V7 DEFECT rows=4 tags=4 bad=['files-untouched: cites no case or a case that does not violate it']
checks=7 defects=1
PREDICATE C2 fail
counter_exit=1   (captured via ${PIPESTATUS[0]} on the re-run)
```

## M03 — entry map: files-untouched row duplicated

```
V7 DEFECT rows=5 tags=4 bad=["tags missing=0 duplicated=['files-untouched']"]
checks=7 defects=1
PREDICATE C2 fail
exit=1
```

## M04 — entry map: messages-untouched row deleted

```
V7 DEFECT rows=3 tags=4 bad=["tags missing=['messages-untouched'] duplicated=0"]
checks=7 defects=1
PREDICATE C2 fail
exit=1
```

## M05 — entry map: messages-untouched line instruction.md:5 → :4

```
V7 DEFECT rows=4 tags=4 bad=['messages-untouched: line 4 is not the frozen instruction.md:5']
checks=7 defects=1
PREDICATE C2 fail
exit=1
```

## M06 — SOURCES.md: S117 anchor digest replaced by S118's

```
V3 DEFECT rows=2 bad=['S117:anchor_digest']
checks=7 defects=1
PREDICATE C2 fail
exit=1
```

## M07 — receipt: CASE untouched line deleted

```
    gate: P10 DEFECT fresh probe output is not byte-equal to the receipt
    gate: defects=1
V2 DEFECT spec=frozen gate=frozen gate_exit=1
V4 DEFECT cases=24 mismatches_named=0/0 bad=['case ids differ from the frozen table', 'summary disagrees with the CASE lines']
V7 DEFECT rows=4 tags=4 bad=['recover-secret: cites no case or a case that does not violate it', 'secret-gone: cites no case or a case that does not violate it']
checks=7 defects=3
PREDICATE C2 fail
exit=1
```

## M08 — spec: one byte, "min_quotes": 8 → 9

```
V2 DEFECT error ValueError: spec template not at its freeze digest
V3 DEFECT error ValueError: spec template not at its freeze digest
V4 DEFECT error ValueError: spec template not at its freeze digest
V7 DEFECT error ValueError: spec template not at its freeze digest
checks=7 defects=4
PREDICATE C2 fail
exit=1
```

## M09 — dry table: one byte, predicted_pass=13 → 14

```
V4 DEFECT error ValueError: dry table not at its freeze digest
V5 DEFECT probe or dry table not at freeze digest
V7 DEFECT error ValueError: dry table not at its freeze digest
checks=7 defects=3
PREDICATE C2 fail
exit=1
```

## M10 — probe: one docstring byte, offline → ofline

```
    gate: P1 DEFECT pinned=2 mismatched=['plans/git_leak_probe.py']
    gate: defects=1
V2 DEFECT spec=frozen gate=frozen gate_exit=1
V5 DEFECT probe or dry table not at freeze digest
checks=7 defects=2
PREDICATE C2 fail
exit=1
```

## M11 — capture Dockerfile: one byte, FROM → FRM

```
V1 DEFECT listed=7 bad=['Dockerfile'] extra=0
    gate: P5 DEFECT manifest_entries=7 bad=1 first=Dockerfile: manifest digest does not match the bytes
    gate: defects=1
V2 DEFECT spec=frozen gate=frozen gate_exit=1
checks=7 defects=2
PREDICATE C2 fail
exit=1
```

## Post-restore verification (all seven targets cmp-equal to backups)

```
RESTORED-BYTE-EQUAL corpus/knowledge/tb2-git-leak-recovery-grader.md
RESTORED-BYTE-EQUAL corpus/SOURCES.md
RESTORED-BYTE-EQUAL corpus/evidence/round39/git-leak-probe.txt
RESTORED-BYTE-EQUAL plans/pkg-spec-r39.json
RESTORED-BYTE-EQUAL corpus/evidence/round39/git-leak-dry-cases-freeze.txt
RESTORED-BYTE-EQUAL plans/git_leak_probe.py
RESTORED-BYTE-EQUAL corpus/evidence/round39/tb2-git-leak-recovery/Dockerfile
FINAL-RESTORE-BYTE-EQUAL corpus/knowledge/tb2-git-leak-recovery-grader.md
```

Counter on restored bytes:

```
V1 ok listed=7 bad=0 extra=0
    gate: P1..P10 all ok … gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=2 bad=0
V4 ok cases=25 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=4 tags=4 bad=0
checks=7 defects=0
PREDICATE C2 pass
exit=0
```
