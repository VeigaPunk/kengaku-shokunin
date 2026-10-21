# ExecStateCheckV3 — round 26

- **Files changed in private clone:** `plans/state_check.py` — SHA-256 `98c987ede159b032e05bd04699dc6b095059f89d2bccab9e3fa2ab035b9e595a`.
- **Clone base observed:** `e0037a8da26850fcf4c4b6ba40f14a017b3ecf2d` (`r26-ExecStateCheckV3-4`). No other clone files written; no installs.
- **Behavior:** adds fixed P3a–P3e assertions; P3b freezes and verifies the exact `S001–S042` id set, ignoring later `S043+` rows. Also checks v2 capability receipts, instrument rows, all seven SHONEN content pins, axis-table `:162`, and frozen base OOP README populations in both directions.
- Widens `SUPERSEDE_RE` to `R2[5-9]-E`. P3 supersession requires exact derived-token equality; source-document corrections are checked first (P3b→PROVINCE, P3e→README), with SCORECARD fallback. SHONEN corrections use SCORECARD to avoid P2c extra-prose findings. Pointer changes cannot be superseded by restating the old target pin.
- **LSP unavailable:** no LSP tool/endpoint is mounted in the available tool inventory; no cold empty response was treated as evidence.
- **Blockers:** none. Landing must add a proper R26-E3 correction in PROVINCE or SCORECARD using the derived `rows=42`; base P3e also identifies the existing unindexed `lessons/round-25-verifier-spotcheck.md` file.

## P2 equivalence on `git archive f11bffbf` at `/tmp/kengaku-r26-base`

Commands: v2 `/tmp/kengaku-r26-base/plans/state_check.py --root /tmp/kengaku-r26-base --json`; v3 `/tmp/kengaku-r26-ExecStateCheckV3-4/plans/state_check.py --root /tmp/kengaku-r26-base --json`. Filtered assertions by IDs starting `P2`.

```text
v2_exit=0 v3_exit=1
P2_filtered_assertions=247 P2_summary={'assertions': 235, 'match': 231, 'mismatch': 0, 'superseded': 1, 'offline_unverifiable': 3, 'out_of_population': 12}
filtered_json_diff=none summary_equal=True diff_exit=0
```

## `--selftest` (exit 0)

```text
selftest ok   P3a: red mutation and full-token R26-E (P3a.capability.interval-reverdict.selftest-checks)
selftest ok   P3b: instrument and exact-id-set red mutations (P3b.province.interval-reverdict.scored-trials)
selftest ok   P3c: red mutation (P3c.box.3.pointer.1)
selftest ok   P3d: red mutation (P3d.axis.novelty.anchor.1.pin)
selftest ok   P3e: row and file mutations (P3e.row-to-file.lessons/round-25.md; P3e.file-to-row.lessons/round-25.md)
[selftest] ALL PASS (canonical seed, pointers, out-of-population box, pointer-only, sources supersession, ABSENT rule, ABSENT word boundary, R25–R29-E exact-token supersession, P3a–P3e red mutations, anchor content)
exit=0
```

## Base-tree `--summary` (`/tmp/kengaku-r26-base`; exit 1)

```text
assertions=275 match=266 mismatch=5 superseded=1 offline_unverifiable=3
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
MISMATCH: P3a.capability.interval-reverdict.selftest-checks:558 — {"assertion_document": "SCORECARD.md", "correction_line": null, "correction_tokens": null, "derived_tokens": ["18 checks", "0 failed"], "observed": {"claim": ["14", "0"], "receipt": ["18", "0"]}}
MISMATCH: P3a.capability.state-assertion-check.base-mismatch:559 — {"assertion_document": "SCORECARD.md", "correction_line": null, "correction_tokens": null, "derived_tokens": ["mismatch=10"], "observed": {"claim": ["11"], "receipt": ["10"]}}
MISMATCH: P3b.province.public-literature-registry.rows:112 — {"assertion_document": "PROVINCE.md", "correction_line": null, "correction_tokens": null, "derived_tokens": ["rows=42", "id_set=exact"], "observed": {"SOURCES_frozen_census": {"duplicate_ids": [], "exact_id_set": true, "ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42], "missing_ids": [], "rows": 42, "unexpected_ids": []}, "claim": ["25"]}}
MISMATCH: P3b.province.round25-correction.rows:119 — {"assertion_document": "PROVINCE.md", "correction_line": null, "correction_tokens": null, "derived_tokens": ["rows=42", "id_set=exact"], "observed": {"SOURCES_frozen_census": {"duplicate_ids": [], "exact_id_set": true, "ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42], "missing_ids": [], "rows": 42, "unexpected_ids": []}, "claim": ["37"]}}
MISMATCH: P3e.file-to-row.lessons/round-25-verifier-spotcheck.md:82 — {"assertion_document": "corpus/README.md", "correction_line": null, "correction_tokens": null, "derived_tokens": ["path=lessons/round-25-verifier-spotcheck.md", "exists=true", "row_count=0"], "observed": {"exists": true, "path": "lessons/round-25-verifier-spotcheck.md", "row_lines": []}}
VERDICT: FAIL — at least one frozen assertion mismatches
exit=1
```

Prediction `mismatch>=3` is met: base mismatch is 5 (P3a two, P3b two, P3e one). No build/lint/formatter or other tests were run.