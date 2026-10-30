# R54-C2 independent row re-execution

Scratch clone: `/fast/scratch/hyaku/kengaku-r54/E6RowAudit14/lane`, shared clone source `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, tip `62e9bba5e4a0bed376890299aa6a09039db7e68e`. Each command ran with cwd at that clone, timeout 600 seconds, `TMPDIR` rooted in `/fast/scratch/hyaku/kengaku-r54/E6RowAudit14`, and environment returned by the counter's imported `hermetic_env`.

All three argv declarations are legal entry mode (none includes `--selftest`, `--help`, `--dry`, or `--version`); each named script exists in the clone. All are green rows, so no evidence fragment is declared; fragment-match is null/not applicable.

| name | declared | observed | fragment-match | verdict |
|---|---:|---:|---|---|
| round36-c1-battery | 0 | 0 | n/a (no evidence fragment) | CONFIRMED |
| round36-c2 | 0 | 0 | n/a (no evidence fragment) | CONFIRMED |
| round37-c1-mutants | 0 | 0 | n/a (no evidence fragment) | CONFIRMED |

## Commands and output tails

### round36-c1-battery (5.82s)
Command: `python3 plans/round36_c1_verify.py --lane .`

```text
FIXTURE P0 expect=accept observed=accept ok -- genuine round-35 package
FIXTURE P1 expect=reject observed=reject ok -- 8 one-word quotes
FIXTURE P2 expect=reject observed=reject ok -- 8 copies of one quote
FIXTURE P3 expect=reject observed=reject ok -- an unparsed quote row beside the genuine rows
FIXTURE P4 expect=reject observed=reject ok -- junk teaches cells
FIXTURE P5 expect=reject observed=reject ok -- stub probe printing the receipt
FIXTURE P6 expect=reject observed=reject ok -- untracked leftover file
FIXTURE P7 expect=reject observed=reject ok -- cheapest package: one-word quotes + junk teaches + stub probe + stray file
FIXTURE L1 expect=accept observed=accept ok -- D4 genuine correction line
FIXTURE L2 expect=reject observed=reject ok -- D4 line with the two file:line citations swapped
FIXTURE L3 expect=reject observed=reject ok -- D4 line without the harness token
FIXTURE L4 expect=accept observed=accept ok -- D5 genuine erratum line
FIXTURE L5 expect=reject observed=reject ok -- D5 erratum saying the quote is not present
FIXTURE L6 expect=reject observed=reject ok -- D5 genuine line over an altered (quote-injected) capture
FIXTURES total=14 false_green=0 false_red=0 unevaluated=0
R35-D1 status=closed observed=pass agree=yes fixtures=14 false_green=0 false_red=0 unevaluated=0 tip_package_rc=0
R35-D2 status=closed observed=pass agree=yes untracked_anywhere=0 line_fixtures_wrong=0/6
R35-D3 status=closed observed=pass agree=yes committed_nested_wave_paths=0
R35-D4 status=closed observed=pass agree=yes erratum_lines=1 recount=13 + 23 + 1 = 37 stated_denominator=38
rows=4 closed=4 observed_pass=4 mismatches=0
PREDICATE C1 pass
```

### round36-c2 (0.51s)
Command: `python3 plans/round36_c2_verify.py --lane .`

```text
W1 ok
W2 ok
W3 ok
W4 ok
W5 ok
W6 ok
checks=6 defects=0
PREDICATE C2 pass
```

### round37-c1-mutants (134.4s)
Command: `python3 plans/round37_c1_verify.py --lane .`

```text
-file expect=reject declared=P8 observed_rc=1 observed_defects=P8 ok
FIXTURE p910-not-a-git-repo expect=reject declared=P9 observed_rc=1 observed_defects=P9 ok
FIXTURE p910-receipt-deleted expect=reject declared=P10,P2 observed_rc=1 observed_defects=P10,P2 ok
FIXTURE p910-probe-exits-1 expect=reject declared=P1,P10 observed_rc=1 observed_defects=P1,P10 ok
FIXTURE p910-receipt-one-byte expect=reject declared=P10,P2 observed_rc=1 observed_defects=P10,P2 ok
BATTERY fixtures=64 wrong=0 renamed_disagree=0
MUTANT M01 P1 killed by=r36-P5 -- frozen instrument digest mismatch
MUTANT M02 P2 killed by=p23-p2-receipt-deleted -- receipt unreadable
MUTANT M03 P2 killed by=p23-p2-receipt-byte -- receipt digest differs from the pin
MUTANT M04 P3 killed by=p23-p3-heading-renamed -- no Located quotes section
MUTANT M05 P3 killed by=r36-P3 -- an unparsed quote row
MUTANT M06 P3 killed by=p23-p3-seven-texts -- fewer distinct quotes than min_quotes
MUTANT M07 P3 killed by=p23-p3-seven-locations -- fewer distinct located lines than min_distinct_locations
MUTANT M08 P3 killed by=p23-p3-two-word-quote -- a quote outside the word range
MUTANT M09 P4 killed by=p23-p3-heading-renamed -- no parsed quote
MUTANT M10 P4 killed by=p4-capture-unreadable -- quote cites an unreadable capture
MUTANT M11 P4 killed by=p4-line-outside -- quote line range outside the capture
MUTANT M12 P4 killed by=p4-one-char-off -- quote not verbatim on its cited line
MUTANT M13 P5 killed by=p5-manifest-absent -- capture manifest absent
MUTANT M14 P5 killed by=p5-manifest-unparsed-line -- unparsed manifest line
MUTANT M15 P5 killed by=p5-capture-bytes-stale-digest -- manifest digest does not match the capture bytes
MUTANT M16 P5 killed by=p5-row-capture-unpinned -- row capture not pinned in the manifest
MUTANT M17 P5 killed by=p5-manifest-digest-off-pin -- manifest digest differs from the spec pin
MUTANT M18 P5 killed by=p4-capture-unreadable -- quoted capture not pinned in the manifest
MUTANT M19 P5 killed by=p5-extra-capture-file -- capture file not covered by the manifest
MUTANT M20 P6 killed by=p6-m20-registry-row-duplicated -- registry row missing or duplicated
MUTANT M21 P6 killed by=p6-m21-row-with-twelve-cells -- registry row without 11 cells
MUTANT M22 P6 killed by=p6-m22-url-off-the-pinned-raw-path -- row url not the pinned raw path
MUTANT M23 P6 killed by=p6-m23-row-tier-b -- row tier wrong
MUTANT M24 P6 killed by=p6-m24-row-status-queued -- row status wrong
MUTANT M25 P6 killed by=p6-m25-used-by-another-path -- row used-by is not the entry
MUTANT M26 P6 killed by=p6-m26-five-word-teaches-cell -- teaches cell under min_teaches_words
MUTANT M27 P6 killed by=p6-m27-two-identical-teaches-cells -- teaches cells not pairwise distinct
MUTANT M28 P7 killed by=p7-m28-entry-deleted -- entry unreadable
MUTANT M29 P7 killed by=p7-m29-source-url -- source line absent or not the pinned url
MUTANT M30 P7 killed by=p7-m30-verified-at -- verified-at absent or not the frozen date
MUTANT M31 P7 killed by=p7-m31-recheck-line -- recheck line absent
MUTANT M32 P7 killed by=p7-m32-negative-heading -- no Negative space section
MUTANT M33 P7 killed by=p7-m33-falsifier-word -- Negative space carries no falsifier
MUTANT M34 P8 killed by=p8-readme-deleted -- README unreadable
MUTANT M35 P8 killed by=p8-index-row-duplicated -- index rows for the entry not exactly one
MUTANT M36 P8 killed by=p8-index-row-missing-sid -- index row does not cite every registry row
MUTANT M37 P8 killed by=p8-coverage-bullet-removed -- no coverage bullet naming entry and receipt
MUTANT M38 P8 killed by=p7-m28-entry-deleted -- knowledge files differ from index rows
MUTANT M39 P9 killed by=p910-not-a-git-repo -- root is not a git worktree
MUTANT M40 P9 killed by=r36-P6 -- untracked file present
MUTANT M41 P10 killed by=p910-receipt-deleted -- receipt unreadable at re-run
MUTANT M42 P10 killed by=p910-probe-exits-1 -- fresh probe exits nonzero
MUTANT M43 P10 killed by=p910-receipt-one-byte -- fresh probe output not byte-equal to the receipt
MUTANT M44 D4 killed by=d4-m44-file-unreadable -- d4 file unreadable
MUTANT M45 D4 killed by=d4-m45-not-one-line -- d4 file is not exactly one line
MUTANT M46 D4 killed by=d4-m46-label-not-carried -- d4 line does not carry the label
MUTANT M47 D4 killed by=r36-L2 -- d4 directional pattern absent
MUTANT M48 D5 killed by=d5-m48-file-unreadable -- d5 file unreadable
MUTANT M49 D5 killed by=d5-m49-two-lines -- d5 file is not exactly one line
MUTANT M50 D5 killed by=d5-m50-label-altered -- d5 line does not carry the label
MUTANT M51 D5 killed by=d5-m51-require-missing -- d5 required token missing
MUTANT M52 D5 killed by=d5-m52-forbid-present -- d5 forbidden token present
MUTANT M53 D5 killed by=d5-m53-capture-missing -- d5 capture unreadable
MUTANT M54 D5 killed by=r36-L6 -- d5 capture digest not in the manifest
MUTANT M55 D5 killed by=d5-m55-quote-absent -- d5 quote absent from the capture
MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass
```
