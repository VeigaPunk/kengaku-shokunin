# ExecStateCheckV3 — round 26

- Private clone base: `e0037a8da26850fcf4c4b6ba40f14a017b3ecf2d`; only `plans/state_check.py` was written in it.
- Final SHA-256: `32a684ffcb3fb222b0360333f83c2e4654c19ec1c3ad6ed47016052401428089`. No installs. LSP unavailable in the mounted inventory.
- P3b census freezes exactly S001–S042, verifies the full unique ID set, and ignores S043+; derived correction tokens retain `rows=42` plus `id_set=exact`.
- P3a now checks every occurrence of named fields, audits otherwise-unclassified semantic numbers, and verifies the R1–R6 range against selftest receipt IDs (R1b counts as R1). P3a/P3b/P3c/P3d/P3e selftests pin exact ID inventories (14/9/7/3/10).
- P3 corrections require strict full-line dated R26-E format, post-freeze line floors, unique correction IDs, and exact derived-token equality. Source document is primary; SCORECARD fallback applies only when no matching primary exists. P2 lookup remains unchanged.

## Green selftest (exit 0)
```text
selftest ok   P3a: duplicate metric, R1–R6, base mismatch and correction-parser reds
selftest ok   P3b: unique-samples, scored-trials and frozen-id-set reds
selftest ok   P3b: strict source-first/fallback corrections and exact id set
selftest ok   P3c: all Box-1 headings red on missing and duplicate
selftest ok   P3c: red mutation (P3c.box.3.pointer.1)
selftest ok   P3d: red mutation (P3d.axis.novelty.anchor.1.pin)
selftest ok   P3e: outside-spotcheck row, row/file mutations (P3e.row-to-file.lessons/round-25.md; P3e.file-to-row.lessons/round-25.md)
[selftest] ALL PASS (canonical seed, pointers, out-of-population box, pointer-only, sources supersession, ABSENT rule, ABSENT word boundary, R25–R29-E exact-token supersession, P3a–P3e red mutations, anchor content)
exit=0
```

## Final deletion-mutant checks (each `--selftest` exited 1 as expected)
```text
P3a base-mismatch comparison removed: missing=['P3a.capability.state-assertion-check.base-mismatch'], extra=[]
P3b unique-samples comparison removed: missing=['P3b.province.interval-reverdict.unique-samples'], extra=[]
P3e file loop changed to row set: missing=['P3e.file-to-row.lessons/round-25-verifier-spotcheck.md'], extra=['P3e.file-to-row.lessons/round-24-verifier-spotcheck.md']
P3c whole-file token-hit predicate removed: selftest: P3c Box-1 missing survived (P3c.box.1.pointer.1.needle.1)
```

## P2 projection on `git archive f11bffbf` extracted at `/tmp/kengaku-r26-base`
```text
v2_exit=0 v3_exit=1
P2_filtered_assertions=247 P2_summary={'assertions': 235, 'match': 231, 'mismatch': 0, 'superseded': 1, 'offline_unverifiable': 3, 'out_of_population': 12}
filtered_json_diff=none summary_equal=True diff_exit=0
```

## Final base-tree `--summary` (exit 1; preregistered mismatch>=3 met)
```text
assertions=278 match=269 mismatch=5 superseded=1 offline_unverifiable=3
OUT_OF_POPULATION: P2a.out-of-population.interval-reverdict:558 — "interval-reverdict"
OUT_OF_POPULATION: P2a.out-of-population.state-assertion-check:559 — "state-assertion-check"
SUPERSEDED: P2a.capability.sources-registry:557 — {"correction_exact": true, "correction_line": 646, "correction_tokens": ["rows 26", "malformed 0", "A=24 C=2", "mined=18 queued=5 rejected=3"], "observed": "rows 26; malformed 0; A=24 C=2; mined=18 queued=5 rejected=3", "stale_tokens": ["rows 25", "A=24 C=1", "mined=18 queued=5 rejected=2"]}
OUT_OF_POPULATION: P2e.out-of-population.row.knowledge/attribution-interval-calibration.md@61:61 — "knowledge/attribution-interval-calibration.md"
OUT_OF_POPULATION: P2e.out-of-population.row.lessons/round-24-verifier-spotcheck.md@92:92 — "lessons/round-24-verifier-spotcheck.md"
OUT_OF_POPULATION: P2e.out-of-population.row.lessons/round-25.md@93:93 — "lessons/round-25.md"
OUT_OF_POPULATION: P2e.out-of-population.row.evidence/round25-sources/@167:167 — "evidence/round25-sources/"
OUT_OF_POPULATION: P2e.out-of-population.row.evidence/round25-calibration/@168:168 — "evidence/round25-calibration/"
OUT_OF_POPULATION: P2e.out-of-population.file.evidence/round25-calibration/ — "evidence/round25-calibration/"
OUT_OF_POPULATION: P2e.out-of-population.file.evidence/round25-sources/ — "evidence/round25-sources/"
OUT_OF_POPULATION: P2e.out-of-population.file.knowledge/attribution-interval-calibration.md — "knowledge/attribution-interval-calibration.md"
OUT_OF_POPULATION: P2e.out-of-population.file.lessons/round-25-verifier-spotcheck.md — "lessons/round-25-verifier-spotcheck.md"
OUT_OF_POPULATION: P2e.out-of-population.file.lessons/round-25.md — "lessons/round-25.md"
MISMATCH: P3a.capability.interval-reverdict.selftest-checks:558 — {"assertion_document": "SCORECARD.md", "correction_line": null, "correction_tokens": null, "derived_tokens": ["18 checks", "0 failed"], "observed": {"claim": ["14", "0"], "claim_occurrences": [["14", "0"]], "receipt": ["18", "0"], "receipt_occurrences": [["18", "0"]]}}
MISMATCH: P3a.capability.state-assertion-check.base-mismatch:559 — {"assertion_document": "SCORECARD.md", "correction_line": null, "correction_tokens": null, "derived_tokens": ["mismatch=10"], "observed": {"claim": ["11"], "claim_occurrences": [["11"]], "receipt": ["10"], "receipt_occurrences": [["10"]]}}
MISMATCH: P3b.province.public-literature-registry.rows:112 — {"assertion_document": "PROVINCE.md", "correction_line": null, "correction_tokens": null, "derived_tokens": ["rows=42", "id_set=exact"], "observed": {"SOURCES_frozen_census": {"duplicate_ids": [], "exact_id_set": true, "ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42], "missing_ids": [], "rows": 42, "unexpected_ids": []}, "claim": ["25"]}}
MISMATCH: P3b.province.round25-correction.rows:119 — {"assertion_document": "PROVINCE.md", "correction_line": null, "correction_tokens": null, "derived_tokens": ["rows=42", "id_set=exact"], "observed": {"SOURCES_frozen_census": {"duplicate_ids": [], "exact_id_set": true, "ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42], "missing_ids": [], "rows": 42, "unexpected_ids": []}, "claim": ["37"]}}
MISMATCH: P3e.file-to-row.lessons/round-25-verifier-spotcheck.md:82 — {"assertion_document": "corpus/README.md", "correction_line": null, "correction_tokens": null, "derived_tokens": ["path=lessons/round-25-verifier-spotcheck.md", "exists=true", "row_count=0"], "observed": {"exists": true, "path": "lessons/round-25-verifier-spotcheck.md", "row_lines": []}}
VERDICT: FAIL — at least one frozen assertion mismatches
exit=1
```

No installs, build, lint, or formatter. P3b's two stale PROVINCE claims and the frozen outside-spotcheck README gap remain expected base findings; integration must land exact full-value corrections for a zero-mismatch result.