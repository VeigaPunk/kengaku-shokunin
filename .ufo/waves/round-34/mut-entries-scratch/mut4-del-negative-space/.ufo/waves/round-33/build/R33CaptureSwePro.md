# R33CaptureSwePro — S093 SWE-bench_Pro-os verifier capture (C1 identity check)

Round 33, hyaku run 7, 2026-10-25. Leaf seat. Assignment: re-open S093's source at the pinned
commit, capture `tests/test.sh`, and report path / bytes / sha256 / the four required located
lines / one anchor quote.

**VERDICT: captured**

## 1. Resolution (one tree API call, then one raw fetch)

Tree call (single, unauthenticated, not truncated):

```
curl -fsSL 'https://api.github.com/repos/scaleapi/SWE-bench_Pro-os/git/trees/66f92766bba642462d4bbe5479e83f91f9211862?recursive=1'
```

- response bytes: `6205275`; sha256 `3efaec248726ba86210654af2db5b25181a4799991cedfbf06c1cdf58da88001`
- `truncated: false`; `tree` entries: `16077`; response `sha` begins `66f92766bba6`
- No rate limit encountered (HTTP 200 on the first call).

**Ambiguity found and resolved by the registry, not guessed.** The pattern
`v2/tasks/instance_internetarchive__openlibrary-*/tests/test.sh` matches **82** distinct task
instances in this commit, not one. The instantiation used is the one `corpus/SOURCES.md:112`
(S093) already names verbatim, character for character:

```
v2/tasks/instance_internetarchive__openlibrary-00bec1e7c8f3272c469a58e1377df03f955ed478-v13642507b4fc1f8d234172bf8129942da2c2ca26/tests/test.sh
```

Tree entry for that path (from the same response):

```
{"path": "…/instance_internetarchive__openlibrary-00bec1e7…-v13642507…/tests/test.sh",
 "mode": "100755", "type": "blob",
 "sha": "70b0d1aa40351d358dab48e1b0a7f19b94250270", "size": 7864}
```

Raw fetch at the pinned commit:

```
curl -fsSL 'https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766bba642462d4bbe5479e83f91f9211862/<resolved path>'
```

## 2. Capture file

| field | value |
|---|---|
| committed path | `.ufo/waves/round-33/assimilation/captures/swebench-pro-tests-test.sh` |
| absolute | `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-33/assimilation/captures/swebench-pro-tests-test.sh` |
| bytes | `7864` |
| lines | `234` (final byte `0x0a`, so 234 newline-terminated lines) |
| sha256 | `b6f26eecd87c1696a3702ee115d31f9d42f4704cf2116419cd879f66b60976d0` |
| mode installed | `0644` |
| type | `Bourne-Again shell script, ASCII text executable` |
| provenance binding | `git hash-object` of the capture = `70b0d1aa40351d358dab48e1b0a7f19b94250270` = the tree blob sha at `66f92766` |

The last row is the identity proof: the captured bytes hash to the blob object the pinned
commit's tree names, so the file is byte-identical to that revision, not merely similar.

## 3. Required located lines (verbatim, `:` = line number)

1. `:33` — `echo "Resetting test-space to base state (full test-code surface)..."`
2. `:29` — `find . -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true`
   (the immediately following sibling line is `:30` `find . -name '*.pyc' -delete 2>/dev/null || true`;
   `:29` runs *after* `cd /app || cd /testbed`, `:28`)
3. `:213` — `all_required = fail_to_pass | pass_to_pass` and `:214` —
   `success = all_required <= passed_tests` (adjacent, same reward block, inside `EVAL_EOF`)

**Row anchor (≤25 words, located):**

> `find . -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true` — 15 words, `tests/test.sh:29`

## 4. Identity check against the existing S093 row

`corpus/SOURCES.md:112` cites `:33`, `:71` and `:214`. All three resolve in this capture:

| row citation | captured text | resolves |
|---|---|---|
| `:33 "Resetting test-space to base state (full test-code surface)..."` | identical | yes |
| `:71 \`T) git checkout HEAD -- "$path"\`` | `        T) git checkout HEAD -- "$path" 2>/dev/null || true ;;` (row quote is a leading-space-free prefix of the line) | yes |
| `:214 "success = all_required <= passed_tests"` | identical | yes |

The row's path abbreviation (`instance_internetarchive__openlibrary-…`) is a legitimate
`…`-elision of the resolved path above; it does not denote a different instance.

The uncommitted draft `corpus/knowledge/benchmark-grader-semantics.md` (read only, not edited by
this seat) already carries the three re-pointed `source:` lines for S093/S103/S104; this capture
supplies the S093 half of that gate. S103/S104 resolution is not this seat's assignment.

## 5. Risks / limits

- **One instance of 82.** S093's claim is scoped to the single `openlibrary-00bec1e7…` task; the
  capture cannot support any statement about the other 81 instances without a further fetch.
- `test.sh` is one of three files the S093 row names (`test.sh`, `parser.py`, `config.json`); only
  `test.sh` was captured here. The row's `parser.py` quotes were not re-verified by this seat.
- The capture is untracked at hand-off (this seat may not touch the lane Git index). The L1
  commits it; the path is inside the lane's wave-evidence tree and is committable as-is.
- No rate limit, no fallback path taken.

## 6. Compliance

- No production edits: the only bytes written under the lane repo are this report and the single
  assigned capture. Nothing written to `/home/vgpnk/Projects/shokunin`, `shokuknow`, sibling
  lanes, `.ufo/state`, `MANIFEST.json`, or any Git index.
- No tools installed or upgraded (all work with `curl`, `sha256sum`, `git hash-object`, `python3`).
- Scratch confined to `/tmp/r33-R33CaptureSwePro/` (`tree.json` 6.2 MB, `test.sh` 7.9 KB; well under 60 MB).
- Access date for the source opened this round: 2026-10-25.

**VERDICT: captured** — `.ufo/waves/round-33/assimilation/captures/swebench-pro-tests-test.sh`,
7864 bytes, sha256 `b6f26eecd87c1696a3702ee115d31f9d42f4704cf2116419cd879f66b60976d0`, blob
`70b0d1aa40351d358dab48e1b0a7f19b94250270` at `66f92766bba642462d4bbe5479e83f91f9211862`.
