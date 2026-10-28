# C1RevCaptureProvenance — R52 wave 1

## Scope and result

Read-only capture-provenance review. I read `plans/round-52-claims.md` in full before investigating. The frozen population is 89 tasks / 184 capture paths at `harbor-framework/terminal-bench-2@2fd12b88aafdd04a52c298e3940bcb189f9766d6`. Its JSON contains path lists, not SHA-256 values. I therefore compared my fetches to independent upstream representations, then calculated the SHA-256 values the capture manifest should record.

**The five deterministic samples all match byte-for-byte across raw.githubusercontent (following and not following redirects), the GitHub Contents API, and the pinned codeload tarball.** Separately, all 184 raw-fetched paths exist in the complete recursive tree at the pin, and their computed Git blob SHA-1s match the tree's blob SHA-1s (184/184). The tarball’s set of all `test_outputs.py`, `test.sh`, and `verify.sh` files equals the frozen capture set exactly (184/184).

**Two counter defects existed in the frozen 1315234 version:** `present` was capped at 89 while `expected=184`, and a `./`-prefixed `SHA256SUMS` made all digest lookups miss. I reproduced both. The lane’s live, uncommitted working copy changed during review (mtime 17:07:22); its current collector now iterates all `capture_population` paths, strips `./`, and counts an absent checksum row as a mismatch. Running that current counter against the sibling executor’s 184-file artifacts produced `present=184 mismatched=0`. I report the earlier defects as observed-and-fixed in the live working copy, not as defects in that latest snapshot. The latest collector still does not reject empty/non-text error bodies itself; see minimal checks below.

## Five deterministic paths and pins

Selection: flatten `capture_population`, sort paths lexicographically, take 1-based positions 30, 60, 90, 120, 150. For each path, I fetched twice from the pinned raw URL and once via the GitHub Contents API; all three bodies matched. The pinned codeload tarball copy also had the same SHA-256 for all five.

| Sorted position | Path | SHA-256 (record in `SHA256SUMS`) | Git blob SHA-1 at pin | Bytes |
|---:|---|---|---|---:|
| 30 | `configure-git-webserver/tests/test_outputs.py` | `526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37` | `8036593f765683db7b05911aa13e0730b8192e85` | 547 |
| 60 | `fix-code-vulnerability/tests/test.sh` | `f1611da693cb4cfc5e8482698c6a1858a5c67220ae9db89b50aed66584e9b17f` | `2d2aefa518b26a0038f03409cbbb5f5e7324eb23` | 653 |
| 90 | `log-summary-date-ranges/tests/test_outputs.py` | `2fc06a6ce1944ad82f84fb437395fa75ed8c0eadd385b92e375c27e5bc9cb2b4` | `c245058c3fe2b2fa3687f2b14e72c256ad8558da` | 1,655 |
| 120 | `path-tracing-reverse/tests/test.sh` | `a719dbb1ba7ae76df095e9d815941dfa4c55edaf11f173b9c3c3097afa838548` | `05ee2e4ec690486f3e5a40baddbdae4487908acb` | 650 |
| 150 | `regex-log/tests/test.sh` | `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` | `cb4a41a45e4b23f4d1f1392fd68f6e47c5dbbf57` | 608 |

Independent manifest cross-check: a manifest generated from my raw-fetch bytes with the sibling’s sorted `sha256sum` format and `./` path prefixes hashes to `b9ada6472642fa547935c6a1d4fb9474db4d84b412fb9ab3c1730fd65bc974c8`, exactly the sibling report’s `SHA256SUMS` digest. My plain-path version (the key form expected by the original frozen counter) hashes to `204a071d59ee906fa9e01d294b60d8793fe24df35afbd0e87202e26d44568a47`.

## Concrete failure modes and detection

- **404 / path absent at requested pin:** raw.githubusercontent returned HTTP 404, `text/plain`, body `404: Not Found` (14 bytes). A request without `-f` can save this body; `curl -sS -o file` returns success for the HTTP response. The frozen classifier calls this V4 and places it in `CANDIDATES`. I inserted that body as a primary grader in a scratch fixture; it produced a V4 candidate. The amended A1 quote-in-capture condition helps prevent confirming such a candidate, but does not prevent it polluting the candidate queue.
- **Empty file:** constructed a zero-byte capture. The classifier reports V4 / candidate; the counter has no content-format guard. The latest collector’s checksum check detects the empty bytes only if the pinned manifest contains the expected non-empty digest. A manifest regenerated from the bad body would self-certify it.
- **Redirect body:** an `http://raw.githubusercontent.com/...` request returned HTTP 301, `Location: https://raw.githubusercontent.com/...`, with a zero-byte body when not following redirects. A no-`-L` fetch can therefore save an empty capture if its caller ignores response status/headers. That empty body also classifies as V4.
- **Rate-limit body:** after the unauthenticated GitHub Core API budget reached 0/60, a real tree API request returned HTTP 403 and this 280-byte JSON body: `{"message":"API rate limit exceeded for 179.218.13.209. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)","documentation_url":"https://docs.github.com/rest/overview/resources/in-the-rest-api#rate-limiting"}`. This particular body classifies V2 because its documentation URL includes `rest`; it is still not grader source. Fetching 184 files with one Contents API request per file would exceed the observed unauthenticated 60/hour limit. Raw content and codeload worked without those Core API headers.
- **Wrong repository/ref:** the pinned raw URL is commit-addressed; using a branch or a different repository/ref can return plausible source bytes rather than an HTTP error. My attempted related-repository `terminal-bench-2-1` path returned 200, but on inspection its SHA-256 was identical to the pinned `build-pmars/tests/test_outputs.py`; it is therefore **not** evidence of a wrong-byte cross-pin case. The same-repo `main` ref resolves to the frozen SHA itself (`git ls-remote`), so I could not establish a verified same-repository alternate-pin path that exists elsewhere but not at this pin. The absent-at-pin 404 case is verified; the alternate-pin-specific case remains unverified.
- **Self-consistent corruption:** `SHA256SUMS` produced from the same failed response only pins the failed bytes. The independent tree’s blob SHA-1 (or a second independent retrieval such as codeload) detects this. The tree response was complete (`truncated=false`), 1,446 entries; all 184 captured paths were present and every computed Git blob SHA-1 matched the tree’s blob SHA-1.

The pinned tarball was 40,357,259 bytes and contained exactly 184 blobs with the three capture basenames. On my raw sweep, all 184 responses were HTTP 200 / `text/plain`, no empty/HTML/rate-limit signature was seen, minimum file size was 295 bytes, and the capture-set tree comparison had zero missing paths. The raw sweep yielded 147 distinct SHA-256 values across 184 paths, demonstrating why the manifest must be path-keyed (not a set of unique digests).

## Counter/manifest defects observed and current status

1. **Frozen collector count unreachable (fixed in current working copy).** The frozen counter’s `collect()` iterated 89 tasks and incremented `present` once per existing primary grader, so `present<=89`, while population `capture_file_count=184`; all 184 files present still printed `CAPTURES expected=184 present=89 mismatched=0`. The frozen `present==expected` leg was impossible. I reproduced this in a scratch fixture and against the sibling’s actual 184 files. The latest working-copy collector instead walks all unique `capture_population` paths; with sibling artifacts it prints `present=184 mismatched=0`.
2. **Frozen digest-key mismatch (fixed in current working copy).** The sibling’s `sha256sum` manifest uses keys like `./adaptive-rejection-sampler/tests/test_outputs.py`. The frozen loader removed leading `*` but not `./`; 0/89 primary grader keys matched. I corrupted a primary grader: with the sibling manifest the frozen counter reported `mismatched=0`; converting keys to plain paths made the same corruption report `mismatched=1`. The latest working-copy loader strips `./`.
3. **Frozen collector missed 95 paths (fixed in current working copy).** The frozen collector hashed only the 89 primary graders, leaving 89 `test.sh`, five extra environment `test_outputs.py` variants, and one `verify.sh` outside its count/digest loop. The latest collector walks all unique paths in `capture_population`.
4. **Missing checksum rows were not counted (fixed in current working copy).** Frozen code only incremented mismatch when `pg in sums and digest differs`; absent rows were skipped. The current collector increments mismatch if a capture path has no sums row.
5. **No source-format sanity gate remains.** The current capture loop counts a present file and compares SHA-256, but does not itself require non-empty bytes, reject HTML/JSON error bodies or validate the response status/content type. These checks are required at capture time (before generating SHA256SUMS); SHA-256 alone cannot authenticate an error body if the manifest is generated from it.

I also verified the frozen `c1-control-drop-capture` expected text `present=183 mismatched=1` was incompatible with the original frozen collector: deleting a primary capture yielded `present=88 mismatched=0`, and deleting its sums row while leaving the file yielded `present=89 mismatched=0`. The current collector fixes the count/missing-row behavior; the actual control should be rerun against the latest counter.

## Minimal checks for L1’s capture manifest

1. Derive the expected path set from frozen `capture_population`; require exact set equality between those 184 paths, captured files, and manifest rows (including no extras, no omissions). Store SHA-256 lines with paths relative to the `graders/` root; normalize `./` before comparison. Keep paths as keys because duplicate contents exist.
2. Require each fetch’s successful HTTP status (200), final URL/ref equal to the immutable pinned raw URL, zero redirects or an explicitly validated final URL, nonzero body, and an expected text content type. Reject common bodies/signatures such as `404: Not Found`, HTML, and GitHub API error JSON **before writing a digest**.
3. Compare each path’s Git blob SHA-1 (`sha1(b"blob " + str(n) + b"\\0" + body)`) with that path’s blob SHA in the complete recursive tree at the frozen commit. This is the independent pin; then record SHA-256 and byte count in the lane manifest. Optionally independently re-fetch a deterministic sample / codeload archive and require byte equality.
4. Run `sha256sum -c` from the `graders/` root and require exactly 184 successful rows. The frozen counter should also verify path-set equality, digest membership, and digest equality over all 184 (latest working copy now covers those count/key/missing-row cases).

## Exact commands / evidence

Tool installs/updates: none. Available `curl`, `python3`, `git`, `sha256sum`, and `tar` were used. `/fast` had 537 GB free when checked; no ENOSPC occurred.

Representative exact commands (all writes/fixtures stayed under this seat’s scratch directory; no lane files were edited by this seat):

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r52/C1RevCaptureProvenance/tmp
# deterministic selection from the frozen manifest
python3 - <<'PY'
import json
d=json.load(open('/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round52-tasks.json'))
paths=sorted(p for group in d['capture_population'].values() for p in group)
for i in (30,60,90,120,150): print(i, paths[i-1])
PY
# sample fetches used raw URLs at the frozen SHA; each path was fetched with curl -fsSL,
# curl -sS without -L (headers captured), and GitHub Contents API base64; SHA-256 compared.
# Whole-population raw sweep and Git blob SHA-1 comparison were run from Python under scratch.
curl -sS -D failmodes/ratelimit_real.hdr -o failmodes/ratelimit_real.body \
  'https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1' \
  -w 'code=%{http_code} size=%{size_download}\\n'
curl -sS -D failmodes/redirect_301.hdr -o failmodes/redirect_301.body \
  'http://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test.sh' \
  -w 'code=%{http_code} size=%{size_download}\\n'
curl -sSL --max-time 120 -o tb.tar.gz -w 'code=%{http_code} size=%{size_download} ctype=%{content_type}\\n' \
  'https://codeload.github.com/harbor-framework/terminal-bench-2/tar.gz/2fd12b88aafdd04a52c298e3940bcb189f9766d6'
```

I also ran the frozen and latest C1 counters only against scratch fixture trees, never against a modified lane tree. The latest live counter was read-only-run on a scratch copy with the sibling artifacts to confirm `present=184 mismatched=0`.

## Files produced

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1RevCaptureProvenance/report.md`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1RevCaptureProvenance.md` (seat-requested flat report)

Temporary fetches, API responses, manifest calculations, tree listing, fixtures, tarball and comparison data were under `/fast/scratch/hyaku/kengaku-r52/C1RevCaptureProvenance/` and were removed before yielding.
