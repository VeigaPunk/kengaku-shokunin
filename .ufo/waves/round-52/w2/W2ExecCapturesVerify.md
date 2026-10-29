# W2ExecCapturesVerify — capture-set verification (R52-C1)

**Attacked:** the 183 landed grader captures under `corpus/evidence/round52/graders/` and its `SHA256SUMS`. **Attack failed to land: no defective capture found.**

Commands: `python3 verify.py` (kept beside this report; reads `plans/round52-tasks.json` `capture_population` = 184 paths, sorted; selection = 0-based index `i % 19 == 0` -> 10 paths; fetches `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/<path>` with urllib; sha256 vs committed bytes and vs SHA256SUMS). Full JSON receipt: `capture-verification.json` (same dir; original at /fast/scratch/hyaku/kengaku-r52/w2-W2ExecCapturesVerify/, removed after copy).

## Ten re-fetch digests (all: fetched == committed == SHA256SUMS line)
| idx | path | bytes | sha256 |
|---|---|---|---|
| 0 | adaptive-rejection-sampler/tests/test.sh | 649 | 38b43560d173cc2b952c3a3e17b8a480216d84e33450515e047bcb0d806b1e0a |
| 19 | circuit-fibsqrt/environment/tests/test_outputs.py | 3710 | 6117b8edb7d567b30e32b16a9244bec4c131ec01e9065d52f6f53f87e36f0438 |
| 38 | custom-memory-heap-crash/tests/test_outputs.py | 6062 | 4e1cb33f777fa7fb5e1536f9bea9eace6deccd515c67d4f87570adbe692914ba |
| 57 | financial-document-processor/tests/test.sh | 629 | 48abbda713ace5cee00dd28c7398959f28280062350eb88206a6697a28c72790 |
| 76 | hf-model-inference/tests/test_outputs.py | 4239 | 61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857 |
| 95 | make-mips-interpreter/tests/test_outputs.py | 3646 | f1748ff20bfd670af1e1cb935647503eb176a4a14dd15f20935264ad7e4a98f6 |
| 114 | overfull-hbox/environment/tests/test_outputs.py | 3752 | 09756f87d1a29df533e86c5c7d5fd14f64acb17b03cabb55921bb2890d368e5d |
| 133 | pypi-server/tests/test.sh | 625 | d2b1220e42bcfdcce87907ac5bbd69ac210a3c94926545ca2439636786e7784e |
| 152 | reshard-c4-data/tests/test_outputs.py | 6615 | 7c3e934692e274d798d90e213a0f733a1d1ef08464245e17b9531335ea78ae0a |
| 171 | torch-tensor-parallelism/tests/test_outputs.py | 7171 | 4ae4285e15fba1fcf13d7b7c0638ac8c2e2b0797c937abab1fb6b136fd508290 |

10/10 match. (No selected index hit the excluded path.)

## Two-way count
- Expected (frozen population): 184. On disk (excluding SHA256SUMS, EXCLUDED.md): 183. SHA256SUMS: 184 lines / 184 distinct paths.
- expected-not-on-disk: exactly 1 = `sanitize-git-repo/tests/test_outputs.py` (the A5 operator exclusion). on-disk-not-expected: 0. expected-not-in-SUMS: 0. SUMS-not-expected: 0. on-disk-not-in-SUMS: 0. SUMS-not-on-disk: 1 (same path).
- All 183 on-disk files hash to their SHA256SUMS line (0 mismatches).
- Side probe (read-only, nothing written to lane): upstream bytes of the excluded path fetch to sha256 57e4904177ac…b59e, 2687 B, equal to both the SHA256SUMS line and EXCLUDED.md's claim — the exclusion record is truthful.

## Defect scan
- Byte lengths (183 files): min 295, p10 608, p25 616, median 822, p75 3710, p90 6164, max 18746, total 474687. Buckets: <1K 97, <10K 80, <100K 6; **files <100 B: 0**; empty: 0.
- Smallest: hf-model-inference/tests/test.sh 295, kv-store-grpc/tests/test.sh 295, build-cython-ext/tests/test.sh 435, count-dataset-tokens/tests/test_outputs.py 467.
- HTML-start / GitHub JSON-error body / raw "404: Not Found" text / non-UTF-8 text: 0 suspects. Truncation: the 10 spot-refetches are byte-exact; the 173 others are only digest-consistent with SHA256SUMS (not independently re-fetched), so truncation of them at capture time would be undetected only if SUMS were generated from the same truncated bytes — [INFERENCE] unlikely given 10/10 exact and no sub-100 B files.

Tools installed: none.
