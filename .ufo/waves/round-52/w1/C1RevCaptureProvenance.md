# C1RevCaptureProvenance — R52 wave 1

See the detailed scoped report at `C1RevCaptureProvenance/report.md`.

## Result

Read `plans/round-52-claims.md` in full first. Re-fetched deterministic sorted population positions 30, 60, 90, 120, 150 from pinned raw URLs; compared raw fetches (with and without redirect-following), Contents API bytes, and pinned codeload tarball. All five matched byte-for-byte. Across the full frozen 184-path population, every path exists at the complete tree (truncated=false), every raw body matched its Git blob SHA-1 at the pin, and the tarball's basename-selected path set exactly equaled the frozen population (184/184).

| Position | Path | SHA-256 to record | Git blob SHA-1 | Bytes |
|---:|---|---|---|---:|
| 30 | `configure-git-webserver/tests/test_outputs.py` | `526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37` | `8036593f765683db7b05911aa13e0730b8192e85` | 547 |
| 60 | `fix-code-vulnerability/tests/test.sh` | `f1611da693cb4cfc5e8482698c6a1858a5c67220ae9db89b50aed66584e9b17f` | `2d2aefa518b26a0038f03409cbbb5f5e7324eb23` | 653 |
| 90 | `log-summary-date-ranges/tests/test_outputs.py` | `2fc06a6ce1944ad82f84fb437395fa75ed8c0eadd385b92e375c27e5bc9cb2b4` | `c245058c3fe2b2fa3687f2b14e72c256ad8558da` | 1,655 |
| 120 | `path-tracing-reverse/tests/test.sh` | `a719dbb1ba7ae76df095e9d815941dfa4c55edaf11f173b9c3c3097afa838548` | `05ee2e4ec690486f3e5a40baddbdae4487908acb` | 650 |
| 150 | `regex-log/tests/test.sh` | `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` | `cb4a41a45e4b23f4d1f1392fd68f6e47c5dbbf57` | 608 |

## Provenance risks and counter status

- Real raw 404 response: HTTP 404, `text/plain`, body `404: Not Found` (14 bytes). With a non-failing curl invocation this can be stored; the frozen classifier assigns V4 and queues it as a candidate. Empty files and a no-`-L` HTTP→HTTPS redirect body (observed 301, zero-byte body) also classify as V4. A real GitHub API rate-limit response was HTTP 403 / 280-byte JSON after the shared unauthenticated Core quota reached 0/60; per-file Contents API downloads (184 requests) exceed that quota. Latest details and exact body are in the detailed report.
- Frozen counter version capped `present` at 89 although expected=184, skipped all 95 non-primary paths, and missed sibling `./` checksum keys: corrupting a primary capture still gave mismatched=0. This was independently reproduced. During review the lane’s live, uncommitted counter changed; its current version iterates all 184 paths, strips `./`, and reports missing checksum rows. With the sibling artifacts the current version returned `present=184 mismatched=0`. These defects are reported as fixed in the working copy, not as defects in the latest snapshot.
- Current collector still does not validate HTTP status, non-empty/text format, or reject error bodies before manifest generation. SHA-256 created from the same failed response is self-certifying; compare each file’s Git blob SHA-1 against the pinned complete tree before trusting/recording it.
- I could not verify a same-repository alternate-pin-only path: `main` currently resolves to the frozen SHA. A related-repository path probe returned 200 but its bytes matched the pinned build-pmars grader, so it is not reported as a wrong-byte case.

## Minimal L1 checks

Require exact equality among the 184 frozen paths, captured files, and path-keyed manifest rows; normalize `./`; reject missing and extra paths. Before writing digests, require HTTP 200, expected pinned final URL/ref, non-empty text response, and reject 404/HTML/API-error signatures. Compare every file’s computed Git blob SHA-1 with the complete pinned tree’s blob SHA. Record SHA-256 and bytes per path; run `sha256sum -c` from the graders root.

## Commands, tooling, artifacts

Created scratch with `mkdir -p /fast/scratch/hyaku/kengaku-r52/C1RevCaptureProvenance/tmp`; used Python to sort/populate/fetch/hash and compare, `curl` for raw/API/codeload/status probes, and `sha256sum`/`tar` for independent checks. Also ran frozen and current counter copies against scratch fixture trees. No tools installed or updated. `/fast` had 537 GB free; no ENOSPC. No lane files were edited by this seat.

Reports produced:
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1RevCaptureProvenance.md`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1RevCaptureProvenance/report.md`

All fetched content, fixtures, tarball, and receipts were kept under `/fast/scratch/hyaku/kengaku-r52/C1RevCaptureProvenance/` and removed before yielding.