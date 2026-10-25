# R33CaptureVerify — independent re-fetch verification of the three C1 captures

Date: 2026-10-25 · lane: kengaku-shokunin · scope: the three captures under
`.ufo/waves/round-33/assimilation/captures/` backing S093 (SWE-bench Pro test.sh),
S103 (Toolathlon ab-testing evaluation/main.py), S104 (arXiv 2412.05579v2 abs).
Re-fetch target dir: `/tmp/r33-capture-verify/` (scratch, bytes retained there).

## Method

- Toolathlon: `curl -fsSL https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py`
- arXiv: `curl -fsSL https://arxiv.org/abs/2412.05579v2` (v2-pinned URL; see note 2)
- SWE-bench Pro test.sh: resolved via the GitHub trees API —
  `GET /repos/scaleapi/SWE-bench_Pro-os/git/trees/66f92766bba642462d4bbe5479e83f91f9211862:v2/tasks/instance_internetarchive__openlibrary-00bec1e7c8f3272c469a58e1377df03f955ed478-v13642507b4fc1f8d234172bf8129942da2c2ca26/tests`
  returned `test.sh` blob `70b0d1aa40351d358dab48e1b0a7f19b94250270` size 7864 (tree `43ac9188…`, truncated:false);
  then `curl` of the same path under `raw.githubusercontent.com/…/66f92766…` and a git-blob-sha1 recomputation
  (`blob 7864\0<content>` → `70b0d1aa40351d358dab48e1b0a7f19b94250270`) confirmed byte-for-blob identity.

## Diff table

| capture file | capture sha256 | re-fetch sha256 | bytes (cap/fetch) | byte-diff |
|---|---|---|---|---|
| toolathlon-ab-testing-evaluation-main.py | `3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad` | `3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad` | 14138 / 14138 | IDENTICAL |
| arxiv-2412.05579v2-abs.html | `44195c5f4c8e0ff915f5894a78e88f22a121d87d908e9ad211d611799d17a660` | `44195c5f4c8e0ff915f5894a78e88f22a121d87d908e9ad211d611799d17a660` | 43661 / 43661 | IDENTICAL |
| swebench-pro-tests-test.sh | `b6f26eecd87c1696a3702ee115d31f9d42f4704cf2116419cd879f66b60976d0` | `b6f26eecd87c1696a3702ee115d31f9d42f4704cf2116419cd879f66b60976d0` | 7864 / 7864 | IDENTICAL |

`cmp -s` on all three pairs: zero divergent bytes. Additionally the test.sh re-fetch's
git blob hash equals the blob SHA the trees API reports at the pinned commit.

## Quote spot-check (kill-rule grounding, from my re-fetched bytes)

- S093 test.sh: `:33` "Resetting test-space to base state (full test-code surface)..." ✓;
  `:71` `T) git checkout HEAD -- "$path"` ✓; `:214` `success = all_required <= passed_tests` ✓.
- S103 main.py: `:58` `def validate_record_data(... tolerance_pct: float = 0.1) -> None:` ✓;
  `:280` `validate_record_data(actual_records, expected_records, tolerance_pct=0.05)` ✓ (executed
  tolerance 0.05, not the 0.1 default — the C1 repair's correction is confirmed by the bytes);
  `:168` `def check_abtesting_logging_bucket_clean` ✓.
- S104 abs page: abstract line at html `:123` block — "comprehensive survey of the LLMs-as-judges
  paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation,
  and Limitations." ✓; Comments "60 pages, comprehensive and continuously updated" ✓; title tag
  names `[2412.05579v2]` ✓.

## Manifest notes (not content divergence — flags for the integrator)

1. `captures/SHA256SUMS.txt` lists only 3 of the 4 capture files —
   `swebench-pro-tests-test.sh` (`b6f26e…`) is **absent from the committed sums** though its
   bytes verify. The L1 should add the line before committing manifests as evidence.
2. `assimilation/url-map.json` records `https://arxiv.org/abs/2412.05579` (unversioned) for the
   abs capture, but the captured bytes equal what `…/abs/2412.05579v2` serves: the unversioned
   URL today serves a 43647-byte page (sha `851b03db…`, title `[2412.05579]`) differing only in
   version-suffix chrome — both render v2, but only the v2-pinned URL reproduces the capture
   byte-exactly. Same for the map's `github.com/blob/…` forms vs the `raw.githubusercontent.com`
   bytes actually captured. Recommend tightening url-map to the byte-exact URLs.
3. `url-map.json` has no entry at all for `swebench-pro-tests-test.sh`.
4. `toolathlon-utils-evaluation-retry.py` (sha `db11e66e…`, in SHA256SUMS.txt) is outside this
   item's three-document scope and was not re-fetched here.

## Verdict

VERDICT: captures-verified
