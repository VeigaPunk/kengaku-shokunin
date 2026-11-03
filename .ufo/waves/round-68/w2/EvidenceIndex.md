# EvidenceIndex — round 68, attempt 2, w2

## Scope and result

Axes: coverage (complete artifact enumeration) and calibration (distinguish committed bindings, out-of-index bindings, and unresolved runtime artifacts).

Read the full working-tree frozen claims, including Amendment A2. No predicate, counter, table, target, or kill rule was changed. This is an evidence-index audit, not a C1/C2/A2 execution verdict.

- Revision: `0e52fb5d0bc931a8b7ceddb25d007b8667c8390d`.
- Index: `.ufo/waves/round-68/w2/EvidenceIndex/evidence-index.txt`.
- 81 committed files enumerated; 82 index entries including the explicitly labeled working-tree attempt-2 gate. Entries are sorted by repository-relative path.
- Committed hashes were computed from the exact stdout bytes of `git -C L show 0e52fb5d:<path>` using SHA-256, not from the lane working tree.
- Index SHA-256: `f36f36c2cca84473684dcc9789a00bb31e8c947bf7d6c1deb97a58e19ad50357`.
- Working-tree gate SHA-256: `18fbfc2111d747ae9f40220333f0bbd56062c89e93bcd7c2477358228a0723f4` (snapshot at indexing time, not a committed-byte claim).

## Receipt token-resolution table

Both receipts were read from the pinned commit. `pypi` means `corpus/evidence/round68/pypi/receipt.txt`; `r67` means `corpus/evidence/round68/r67-probe-selftest.txt`. The scan includes `wheel_sha256` and `stderr_sha256`, not just standalone `sha256` fields. `none` is not a 64-hex token. All indexed matches below are committed files; the working-tree gate supplies no receipt match.

| Receipt:line / field | SHA-256 token | Indexed committed match |
|---|---|---|
| pypi:1 / `sha256` | `4a6fae5328e1cacd3b667fb59f50622d1602574a5763f741bda7dc0293b3fdfc` | `plans/round68_c1_pypi_finish.py` |
| pypi:2 / `sha256` | `2ebaf54ea427475f2f897304b7d31f6bea26eb4e5074a759447f0f710919b929` | **No indexed match** |
| pypi:3 / `sha256` | `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c` | **No indexed match** |
| pypi:4 / `wheel_sha256` | `6fad8ea86492def2ce9bb48ba80c11e2b35ce88d8d2ea3757c276754c9d0ced6` | **No indexed match** |
| pypi:4 / `stderr_sha256` | `268c02efc4bcdefb1d142a0f3e218eccf6429eaefea2f767a6dd664a90ffecb3` | `corpus/evidence/round68/pypi/stderr/K1.txt` |
| pypi:5 / `stderr_sha256` | `dedbc20d70cc292e39eec807222312473313ee274e3a8db8476e3e0d8565375d` | `.ufo/waves/round-68/w1/PypiReplicate-evidence/stderr/K2.txt`<br>`corpus/evidence/round68/pypi/stderr/K2.txt` |
| pypi:6 / `wheel_sha256` | `df8d66ab40465261894ca5f17b354a3b079061303e12e97f9fc7d1d1393c07aa` | **No indexed match** |
| pypi:6 / `stderr_sha256` | `9c7014b3b55bad773f6b5ac8bf950338e191a40f1ea7e002a25f7a9e1f2b4a58` | `corpus/evidence/round68/pypi/stderr/K3.txt` |
| pypi:7 / `wheel_sha256` | `b97edcfcd8870426abed8d8100aab73ad26f022ed4a32d6756b7d6b1c4f9fe92` | **No indexed match** |
| pypi:7 / `stderr_sha256` | `6a0ccd86a8b5606aa190add39cd8095eb5346b71d2a39eb08200b77e58e777ef` | `.ufo/waves/round-68/w1/PypiReplicate-evidence/stderr/K4.txt`<br>`corpus/evidence/round68/pypi/stderr/K4.txt` |
| pypi:8 / `sha256` | `574c3a2f7594d05d45ab06526baa61fc36bcc3ee60ec04cc6716e88f1c47af28` | `corpus/evidence/round68/pypi/server-log.txt` |
| r67:3 / `sha256` | `03793f4f9e184e8f829916ef848e0f0d41d94b1bef8ed17eda0fe3c28b0a9f1e` | **No indexed match** |

Result: 12 token occurrences (12 distinct values); 6 resolve within the index and 6 do not. Of the 6 out-of-index values, 3 were independently resolved to committed files outside the requested enumeration; the remaining 3 are wheel hashes without indexed byte witnesses.

## Findings and unresolved pointers

1. **Expected missing committed path:** `plans/round68_report_contract.py` is the only explicitly requested path absent at `0e52fb5d`. Its working-tree bytes are indexed with `(working tree, attempt 2)`. The seven other requested file/directory roots each produced committed files.
2. **Attempt boundary:** the committed `plans/round-68-claims.md` contains no `## Amendment A2`; the full working-tree document read for this assignment does. The claims entry in the index intentionally binds the attempt-1 committed document, not the A2 working-tree version. Likewise, the committed wave enumeration is historical; it cannot bind later w2 reports or the index itself. Attempt-2 material must not be described as covered by the pinned commit.
3. **Three index-coverage gaps, resolved outside the index:** the exact hashes below were re-derived with `git show` at the same pinned commit. These are enumeration-boundary gaps, not observed binding mismatches. They are reported separately rather than silently widening the requested index domain.

| Receipt pointer | Committed path outside index | Re-derived SHA-256 |
|---|---|---|
| pypi:2 BASE-PROBE | `plans/round63_c1_pypi_probe.py` | `2ebaf54ea427475f2f897304b7d31f6bea26eb4e5074a759447f0f710919b929` |
| pypi:3 GRADER | `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py` | `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c` |
| r67:3 PROBE | `plans/round67_c1_pipeline_probe.py` | `03793f4f9e184e8f829916ef848e0f0d41d94b1bef8ed17eda0fe3c28b0a9f1e` |

4. **Three unresolved wheel-byte pointers:** pypi:4 K1 `6fad8ea86492def2ce9bb48ba80c11e2b35ce88d8d2ea3757c276754c9d0ced6`; pypi:6 K3 `df8d66ab40465261894ca5f17b354a3b079061303e12e97f9fc7d1d1393c07aa`; pypi:7 K4 `b97edcfcd8870426abed8d8100aab73ad26f022ed4a32d6756b7d6b1c4f9fe92`. No indexed file has these SHA-256 values, and the committed enumeration contains no `.whl` file. No repository-wide absence claim is made. These tokens therefore remain runtime-artifact identifiers rather than independently recoverable byte witnesses in this evidence set. This does not by itself falsify frozen C1: its stated check requires a 64-hex K1 wheel hash, while the explicitly byte-bound artifacts are the probe, base probe, grader, stderr captures, and server log. No rule was changed.
5. **No byte-binding mismatch observed among resolved tokens:** the C1 probe, four stderr captures, server log, supplemental base probe and grader, and supplemental R67 probe all match their receipt tokens. K2 and K4 each additionally match the corresponding independently retained replicate stderr file; the table preserves both matches.

## Re-derivation commands

Set `L=/home/vgpnk/Projects/shokunin/kengaku-shokunin`. The enumeration used exactly:

```sh
git -C "$L" ls-tree -r --name-only 0e52fb5d -- plans/round-68-claims.md plans/round68_c1_pypi_finish.py plans/round68_c2_correction_gate.py plans/round68_report_contract.py corpus/evidence/round68 .ufo/waves/round-68 corpus/knowledge/tb2-network-service-offline-grader.md corpus/lessons/round-68.md
```

For every emitted path `P`, the index value is the SHA-256 of the raw committed blob (equivalent command):

```sh
git -C "$L" show "0e52fb5d:$P" | sha256sum
```

The single exception is explicitly labeled and uses:

```sh
sha256sum "$L/plans/round68_report_contract.py"
```

Extract receipt tokens from committed bytes using `([A-Za-z_-]*sha256)=([0-9a-fA-F]{64})(?![0-9a-fA-F])`, retaining receipt path, line, field name, and each occurrence. Compare group 2 against the hash column of committed index entries. The supplemental table uses the same committed-blob hashing command for each listed path. No clone, checkout, fixture repository, or git mutation was needed.

## Handoff and limits

Only this report and the named index were written in the lane. Scratch was created under `/fast/scratch/hyaku/kengaku-r68/EvidenceIndex` and removed before yield. No tools installed or updated; no listener started. No builds, tests, linters, formatters, predicate execution, report-contract selftest, or live battery was run by this seat. The parent owns those gates. No source symbols were edited or refactored; LSP was not needed, and no LSP tool is mounted in this seat.

The index proves recoverable bytes at a revision, not execution provenance. The working-tree gate hash can drift after this snapshot; re-hash it when assembling the final attempt-2 record. Resolve the three wheel-byte pointers with retained wheel artifacts only if stronger provenance is required; do not infer their contents from a hash string.

Self-evaluation: accuracy 4/5 (wheel bytes remain unavailable in the index); completeness 5/5 (all 81 committed files, gate exception, and 12 tokens covered); clarity 4/5 (long hashes necessarily widen the table); actionability 5/5 (commands and supplemental paths supplied); conciseness 4/5 (full token values retained for reproducibility). Overall 4.4/5. Main improvement: retain the exact wheel artifacts if demanding recoverable runtime bytes. This assessment distinguishes measured coverage from unproven provenance.
