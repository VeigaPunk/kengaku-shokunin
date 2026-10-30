# Round 54 C2 entry-row re-execution audit

Clone HEAD: `62e9bba5e4a0bed376890299aa6a09039db7e68e`. Executions used counter `hermetic_env`, per-row scratch `TMPDIR`, 600-second timeout.

## state-assertion-check

- argv: `python3 plans/state_check.py --summary`
- entry mode and script exists: `True` (`plans/state_check.py`)
- declared/observed exit: 1 / 1
- evidence fragment match: True
- verdict: **CONFIRMED**
- observed output tail:

```text
ifier-spotcheck.md"
OUT_OF_POPULATION: P2e.out-of-population.file.lessons/round-46.md — "lessons/round-46.md"
OUT_OF_POPULATION: P2e.out-of-population.file.lessons/round-47-verifier-spotcheck.md — "lessons/round-47-verifier-spotcheck.md"
OUT_OF_POPULATION: P2e.out-of-population.file.lessons/round-48-verifier-spotcheck.md — "lessons/round-48-verifier-spotcheck.md"
OUT_OF_POPULATION: P2e.out-of-population.file.lessons/round-48.md — "lessons/round-48.md"
OUT_OF_POPULATION: P2e.out-of-population.file.lessons/round-49.md — "lessons/round-49.md"
OUT_OF_POPULATION: P2e.out-of-population.file.lessons/round-50-verifier-spotcheck.md — "lessons/round-50-verifier-spotcheck.md"
OUT_OF_POPULATION: P2e.out-of-population.file.lessons/round-50.md — "lessons/round-50.md"
OUT_OF_POPULATION: P2e.out-of-population.file.lessons/round-51-verifier-spotcheck.md — "lessons/round-51-verifier-spotcheck.md"
OUT_OF_POPULATION: P2e.out-of-population.file.lessons/round-51.md — "lessons/round-51.md"
OUT_OF_POPULATION: P2e.out-of-population.file.lessons/round-52-verifier-spotcheck.md — "lessons/round-52-verifier-spotcheck.md"
OUT_OF_POPULATION: P2e.out-of-population.file.lessons/round-52.md — "lessons/round-52.md"
OUT_OF_POPULATION: P2e.out-of-population.file.lessons/round-53-verifier-spotcheck.md — "lessons/round-53-verifier-spotcheck.md"
OUT_OF_POPULATION: P2e.out-of-population.file.lessons/round-53.md — "lessons/round-53.md"
SUPERSEDED: P3a.capability.interval-reverdict.selftest-checks:558 — {"assertion_document": "SCORECARD.md", "correction_line": 757, "correction_tokens": ["18 checks", "0 failed"], "derived_tokens": ["18 checks", "0 failed"], "observed": {"claim": ["14", "0"], "claim_occurrences": [["14", "0"]], "receipt": ["18", "0"], "receipt_occurrences": [["18", "0"]]}}
SUPERSEDED: P3a.capability.state-assertion-check.base-mismatch:559 — {"assertion_document": "SCORECARD.md", "correction_line": 758, "correction_tokens": ["mismatch=10"], "derived_tokens": ["mismatch=10"], "observed": {"claim": ["11"], "claim_occurrences": [["11"]], "receipt": ["10"], "receipt_occurrences": [["10"]]}}
SUPERSEDED: P3b.province.public-literature-registry.rows:113 — {"assertion_document": "PROVINCE.md", "correction_line": 191, "correction_tokens": ["rows=42", "id_set=exact"], "derived_tokens": ["rows=42", "id_set=exact"], "observed": {"SOURCES_frozen_census": {"duplicate_ids": [], "exact_id_set": true, "ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42], "missing_ids": [], "rows": 42, "unexpected_ids": []}, "claim": ["171"]}}
SUPERSEDED: P3b.province.round25-correction.rows:120 — {"assertion_document": "PROVINCE.md", "correction_line": 190, "correction_tokens": ["rows=42", "id_set=exact"], "derived_tokens": ["rows=42", "id_set=exact"], "observed": {"SOURCES_frozen_census": {"duplicate_ids": [], "exact_id_set": true, "ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42], "missing_ids": [], "rows": 42, "unexpected_ids": []}, "claim": ["37"]}}
MISMATCH: P3c.box.4.pointer.1:12 — {"assertion_document": "SHONEN.md", "correction_line": null, "correction_tokens": null, "derived_tokens": ["pointer=PROVINCE.md:129", "pointer_count=1", "target=PROVINCE.md:129", "token=### Adjacent", "token_hits=0", "line_text=<blank>"], "observed": {"pointer": "PROVINCE.md:129", "pointer_count": 1, "target_line": 129, "target_text": "", "token": "### Adjacent", "token_hits": 0}}
SUPERSEDED: P4b.readme.covers.round26-sources:457 — {"SOURCES_ids": [43, 44, 45, 46, 47, 48], "base_erratum_exact": true, "base_erratum_line": 472, "claimed_range": ["043", "047"], "derived_range": "S043–S048", "derived_tokens": ["sources=S043–S048", "source_count=6", "source_ids=S043,S044,S045,S046,S047,S048"], "expanded": [43, 44, 45, 46, 47]}
VERDICT: FAIL — at least one frozen assertion mismatches

```

## tb2-grader-probe

- argv: `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .`
- entry mode and script exists: `True` (`plans/tb2_grader_probe.py`)
- declared/observed exit: 0 / 0
- evidence fragment match: None
- verdict: **CONFIRMED**
- observed output tail:

```text
grader=corpus/evidence/round35/tb2-eval/test_outputs.py sha256=44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582 pin=2fd12b88aafdd04a52c298e3940bcb189f9766d6 biopython=1.85
components_aa=8,259,158,235,182 max_passing_nt=2766 cap_nt=3000
case=valid-balanced predicted=pass observed=pass match=yes nt=2586 gcwin=ok assertion='-' requirement='all bullets: GS linkers 5..20, order, no Met/stop, GC windows, <=3000 nt'
case=uppercase predicted=pass observed=pass match=yes nt=2586 gcwin=ok assertion='-' requirement='file holds only the sequence (case is not specified)'
case=no-trailing-newline predicted=pass observed=pass match=yes nt=2586 gcwin=ok assertion='-' requirement='file holds only the sequence'
case=trailing-empty-line predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='Invalid number of lines in gblock.txt.' requirement='No empty lines'
case=start-codon-prefixed predicted=fail observed=fail match=yes nt=2589 gcwin=ok assertion='Start of gBlock must match flag protein.' requirement='no start codon / remove N-terminal Met'
case=stop-codon-appended predicted=fail observed=fail match=yes nt=2589 gcwin=ok assertion='End of gBlock must match snap protein.' requirement='no stop codon'
case=linker-4aa predicted=fail observed=fail match=yes nt=2583 gcwin=ok assertion='Linker must be between 5 and 20 amino acids long.' requirement='linkers 5..20 aa'
case=linker-21aa predicted=fail observed=fail match=yes nt=2634 gcwin=ok assertion='Linker must be between 5 and 20 amino acids long.' requirement='linkers 5..20 aa'
case=linker-20aa predicted=pass observed=pass match=yes nt=2631 gcwin=ok assertion='-' requirement='linkers 5..20 aa (upper bound inclusive)'
case=linker-non-gs predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='Linker must only contain G and S amino acids.' requirement='only GS linkers between subproteins'
case=linker-g-only predicted=pass observed=pass match=yes nt=2586 gcwin=ok assertion='-' requirement='GS linkers (a G-only linker is not distinguished)'
case=n-terminal-linker predicted=fail observed=fail match=yes nt=2601 gcwin=ok assertion='Start of gBlock must match flag protein.' requirement='no GS linker on the N terminus'
case=c-terminal-linker predicted=fail observed=fail match=yes nt=2601 gcwin=ok assertion='End of gBlock must match snap protein.' requirement='no GS linker on the C terminus'
case=donor-acceptor-swapped predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' requirement='subprotein order'
case=donor-one-substitution predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='Fusion protein must be in the order flag - donor - dhfr - acceptor - snap' requirement='donor matches its PDB sequence'
case=donor-repeated predicted=fail observed=fail match=yes nt=3378 gcwin=ok assertion='gBlock must be at most 3000 nucleotides.' requirement='do not repeat a protein'
case=non-acgt-base predicted=fail observed=fail match=yes nt=2586 gcwin=ok assertion='gBlock must contain only A, T, C, G.' requirement='gBlock is a DNA sequence'
case=gc-window-high predicted=fail observed=fail match=yes nt=2586 gcwin=violated assertion='GC content must be between 30 and 70% in all 50 nucleotide windows.' requirement='GC 30..70% in every 50-nt window'
cases=18 observed_pass=5 observed_fail=13 mismatches=0

```

## tip-receipts

- argv: `python3 plans/tip_receipts.py --lane .`
- entry mode and script exists: `True` (`plans/tip_receipts.py`)
- declared/observed exit: 0 / 0
- evidence fragment match: None
- verdict: **CONFIRMED**
- observed output tail:

```text
tip 62e9bba5e4a0bed376890299aa6a09039db7e68e
receipt corpus/evidence/probe-r19-P1-key1-quota.log skip reason=no-committed-re-run-command
receipt corpus/evidence/probe-r19-P2-servicetier.log skip reason=no-committed-re-run-command
receipt corpus/evidence/probe-r19-P3.log skip reason=no-committed-re-run-command
receipt corpus/evidence/probe-r19-P4-devinleg.log skip reason=no-committed-re-run-command
receipt corpus/evidence/probe-r19-P4-glm.log skip reason=no-committed-re-run-command
receipt corpus/evidence/probe-r19-P5-glm.log skip reason=no-committed-re-run-command
receipt corpus/evidence/probe-r19-P6-zai.log skip reason=no-committed-re-run-command
receipt corpus/evidence/probe-r19-P8-kimi-code-auth.log skip reason=no-committed-re-run-command
receipt corpus/evidence/probe-r19-P9-absent-port.log skip reason=no-committed-re-run-command
receipt corpus/evidence/probe-r19-devin-shim-seat.log skip reason=no-committed-re-run-command
receipt corpus/evidence/probe-r19-hyper-predictions.log skip reason=no-committed-re-run-command
receipt corpus/evidence/probe-r19-hyper.log skip reason=no-committed-re-run-command
receipt corpus/evidence/probe-r19-opencode-health.log skip reason=no-committed-re-run-command
receipt corpus/evidence/probe-r19-p1-listing-mismatch.log skip reason=no-committed-re-run-command
receipt corpus/evidence/probe-r19-quota23.log skip reason=no-committed-re-run-command
receipt corpus/evidence/probe-r19-shim-ds-predictions.log skip reason=no-committed-re-run-command
receipt corpus/evidence/probe-r19-shim-ds-run.log skip reason=no-committed-re-run-command
receipt corpus/evidence/probe-r19-shim-glm-predictions.log skip reason=no-committed-re-run-command
receipt corpus/evidence/probe-r19-shim-glm-run.log skip reason=no-committed-re-run-command
receipt corpus/evidence/round45/probe-run-envelope.txt skip reason=no-committed-re-run-command
receipt corpus/evidence/round35/tb2-grader-probe.txt equal bytes=3399 exit=0 doc=SKILL.md:623+SKILL.md:574
receipt corpus/evidence/round36/regex-log-probe-first-run.txt skip reason=declared-nonreproducible-absolute-scratch-paths (equal after masking) doc=SKILL.md:576+corpus/README.md:589
receipt corpus/evidence/round36/regex-log-probe.txt equal bytes=5907 exit=0 doc=SKILL.md:576+SKILL.md:576
receipt corpus/evidence/round37/git-webserver-probe.txt equal bytes=8529 exit=0 doc=SKILL.md:577+SKILL.md:577
receipt corpus/evidence/round38/build-pmars-probe.txt equal bytes=5537 exit=0 doc=SKILL.md:582+SKILL.md:582
receipt corpus/evidence/round39/git-leak-probe.txt equal bytes=5867 exit=0 doc=SKILL.md:587+SKILL.md:590
receipt corpus/evidence/round40/db-wal-probe.txt equal bytes=8257 exit=0 doc=SKILL.md:593+SKILL.md:590
receipt corpus/evidence/round41/constraints-probe.txt equal bytes=5775 exit=0 doc=SKILL.md:596+SKILL.md:720
receipt corpus/evidence/round42/fibsqrt-probe.txt equal bytes=4212 exit=0 doc=SKILL.md:600+SKILL.md:600
receipt corpus/evidence/round43/feal-probe.txt equal bytes=3292 exit=0 doc=SKILL.md:604+SKILL.md:604
receipt corpus/evidence/round44/feal-linear-probe.txt equal bytes=3630 exit=0 doc=SKILL.md:607+SKILL.md:607
receipt corpus/evidence/round45/password-recovery-probe.txt equal bytes=4659 exit=0 doc=SKILL.md:615+SKILL.md:615
receipt corpus/evidence/round46/polyglot-c-py-probe.txt equal bytes=6613 exit=0 doc=SKILL.md:616+SKILL.md:616
control receipt=corpus/evidence/round43/feal-probe.txt flip=byte 1646 0x61->0x60 verdict=differ
note compared=12 declared_bounded=1 no_command=20
receipts=33 byte_equal=12 differ=0 skipped=21

```

