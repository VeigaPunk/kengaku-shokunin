DRAFT — append-only erratum lines for the round-36 lesson files (seat R37R36Absorb, round 37 wave 1).
Nothing in the lane was edited. The L1 chooses the target file(s).

## Target: `corpus/lessons/round-36-verifier-spotcheck.md` (append a §Errata block)

```
## Errata (round 37)

Erratum (round 37): the "one-line drift" this file records at :68 and :91 is itself off by one, so
`corpus/lessons/round-36.md:18` needs no correction. Measured on the pinned capture:
`expected_dates = [` is test_outputs.py:71, the nine string literals are :72–:80 (AST element linenos
[72, 73, 74, 75, 76, 77, 78, 79, 80]) and the closing `]` is :81 — i.e. the statement spans 71–81, exactly as
the lesson says, and the entry's own `Oracle values | 71–81` row is right. The "72–82" in this file is the
drifted cell (82 is blank). The paired `sample_logs` span the lesson gives (`34-68`) is also exact
(`sample_logs = [` at 34, `]` at 68).

Erratum (round 37): the S110 span drift this file records at :91 is real, but the exact requirement-bullet
anchor is `instruction.md:1-10`, not `1–11` and not `:1-19`. Measured on the pinned 19-line file: requirement
sentences at 1–4, 6–7, 9–10; lines 5 and 8 blank; line 11 is `Example Python usage:`; 12–19 the example code
block.

Erratum (round 37): the S110 anchor digest in `corpus/SOURCES.md:125` is 63 hex
(`4f7ac05e70cf922ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c`); the 64-hex digest of the pinned file is
`4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c`
(`corpus/evidence/round36/tb2-regex-log/SHA256SUMS:3`; `sha256sum -c SHA256SUMS` → 5/5 OK on 2026-10-26).
```

## Target: `corpus/knowledge/tb2-regex-log-grader.md`

The same three items are drafted as the `## Errata (round 37)` section in
`.ufo/waves/round-37/build/R37R36Absorb/errata-entry.md` (item (a) of this seat's task: the
`What decides it` line corrections and the non-independence of the `ip-no-left-boundary` /
`ip-no-right-boundary` / `ip-octets-unbounded` rows).

## Target: `corpus/lessons/round-36.md`

No erratum drafted: its two spans (`lines 71-81`, `34-68`) measure exact. Its S110 row digest
(`4f7ac05e…f9c`) is a truncated *display* form, not a claimed digest, so it is not corrected here; the
63-hex defect lives in `corpus/SOURCES.md:125` only.

## Measurement receipts

```
$ wc -l corpus/evidence/round36/tb2-regex-log/instruction.md        → 19
$ sed -n '11p' corpus/evidence/round36/tb2-regex-log/instruction.md → Example Python usage:
$ grep -n 'expected_dates = \[\|^    \]' corpus/evidence/round36/tb2-regex-log/test_outputs.py
68:    ]           (sample_logs close)
71:    expected_dates = [
81:    ]           (expected_dates close)
$ sha256sum -c corpus/evidence/round36/tb2-regex-log/SHA256SUMS     → 5/5 OK
$ python3 -c "len('4f7ac05e70cf922ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c'), len('4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c')" → (63, 64); first diff at index 15 ('e' vs '0')
```
