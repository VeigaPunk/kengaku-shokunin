# R33FC3Provenance — C3 kill-rule falsification: fabricated bytes satisfy `--verify`

Role: UFO-FSD sentinel (leaf). Scope: C3 kill-rule claim — "no fabricated bytes may
ever satisfy `--verify`; the digest check binds the receipt to the capture"
(`plans/round-33-claims.md` §C3), target artifact `plans/catalog_probe.py --verify`
(378 lines, tip snapshot `1f202c3e3d727f1254b7e0ebe6994b972e3a7fa26e825567a569486d8006cb82`,
mtime 2026-10-25 14:43:43, Python 3.14.8). No lane files touched; all fixtures in
`/tmp/r33fc3-*`; zero git commands; no tools installed.

## Verdict

**UNCAUGHT — the kill rule is false.** A fully fabricated, internally consistent
tree (raw JSON + SHA256SUMS + after.txt + entry block) that is *not* the output of any
live probe exits 0. The offline verifier authenticates **nothing** about the origin of
the bytes: no network I/O, no TLS/signature, no timestamp authority, no server
attestation — only self-consistency of files the fabricator wrote in the same commit,
and even that is partial (digest lines may be empty/misnamed; count tokens are
substring-checked; the OR count is a self-asserted `total_count` field inside the
committed payload). The parenthetical "digest check binds the receipt to the capture"
holds only in the narrow sense *digest file ↔ bytes* (tampering either half after the
fact is caught); it does not bind receipt *numbers* to bytes, and it does not bind
anything to the endpoint.

## Severity

High for the claim as worded. C3's `--verify` is the only freshness gate introduced
this round; a green `verify=ok` is indistinguishable between (a) an honest live probe
and (b) a single-commit fabrication by any producer with write access to
`corpus/evidence/round33/catalogs/` + the catalog entry (a future round, a sibling, a
reviewer). The predicate line "every one of those numbers re-derives exactly from the
committed raw bytes" is false for the receipt/entry tokens (V5) and for `or_models`
(V7).

## Exploit path (one-commit fabrication)

1. Write `corpus/evidence/round33/catalogs/hf.raw.json` — any valid JSON list of dicts
   (invented ids, no need for real HF data; omit `author, sha, lastModified, gated`
   to yield `hf_schema_delta=4` like the live capture).
2. Write `or.raw.json` — `{"data":[...], "total_count": N}`; `or_models=N` is read
   *from the bytes' own `total_count` field*, not counted (V7: `total_count=999999`
   over 3 records passes).
3. Compute `sha256sum` of both files → write `SHA256SUMS` (self-auth). Empty file
   (V2) or unrelated/missing names (V3, V8) also pass because `_load_raw`
   (lines 123–146) skips absent lines and treats a missing named file as `b""`.
4. Write `after.txt` containing the four tokens and the literal line `HF missing
   fields:` (names unchecked, V8-test; `raw_sha256` line unchecked, `deadbeef` passes).
5. Append `## Re-probe 2026-10-25 (round 33)` block to
   `corpus/knowledge/open-model-catalogs.md` containing the same four tokens (V9
   confirms the block scoping *is* enforced — tokens outside the block are not
   accepted).
6. `python3 plans/catalog_probe.py --verify --lane .` → exit 0.

## Evidence (exact commands and outputs)

### E1 — Fully fabricated tree passes (primary)

Sandbox `/tmp/r33fc3-provenance` (invented ids `invented/org-0…6` for HF,
`invented/model-0…2` for OR; receipt and entry written from the same fabricated bytes):

```
$ python3 plans/catalog_probe.py --verify --lane /tmp/r33fc3-provenance
raw=ok hf_models=7 or_models=3 hf_schema_delta=4 or_schema_delta=0 verify=ok
HF missing fields: author, sha, lastModified, gated
$ echo $?
0
```

Fabricated artifact digests in the tree: `hf.raw.json`
`01f36be91a0a92bfca997f4eaf52f163fd88379944df340c176704f416ab4c51`, `or.raw.json`
`45b1e377e5260226a6f2b8f2c57b95f741dcc3acb800b740fddd1fa58aaff25b`.

### E2 — Verifier is offline; no endpoint authentication

Ran under `unshare -rn` (new network namespace, no interfaces):

```
$ unshare -rn python3 plans/catalog_probe.py --verify --lane /tmp/r33fc3-net
raw=ok hf_models=7 or_models=3 hf_schema_delta=4 or_schema_delta=0 verify=ok
$ echo $?
0
```

Static check: `verify()`/`_load_raw()` (lines 123–192) contain no `fetch`/`urlopen`/
`urllib`/`http` references (grep found none). `--verify` is read-only (sandbox mtimes
unchanged across runs).

### E3 — Receipt/entry numbers need not re-derive (substring superset lie)

Receipt+entry edited to `hf_models=777 or_models=3000 hf_schema_delta=42`
(over-approximations of tokens `hf_models=7` / `or_models=3` / `hf_schema_delta=4`):

```
probed=2026-10-25 hf=ok openrouter=ok hf_models=777 or_models=3000 hf_schema_delta=42 or_schema_delta=0 entry=pending
$ python3 plans/catalog_probe.py --verify --lane /tmp/r33fc3-num
raw=ok hf_models=7 or_models=3 hf_schema_delta=4 or_schema_delta=0 verify=ok
$ echo $?
0
```

`verify()` uses `if token not in receipt` / `if token not in block` (lines 176, 192)
— substring containment, not value equality. The printed (re-derived) numbers differ
from the receipt/entry numbers yet the check passes.

### E4 — OR count is asserted by the fabricated payload itself

`total_count=999999` over a 3-record `data` list (digests recomputed, receipt/entry
updated):

```
$ python3 plans/catalog_probe.py --verify --lane /tmp/r33fc3-num
raw=ok hf_models=7 or_models=999999 hf_schema_delta=4 or_schema_delta=0 verify=ok
$ echo $?
0
```

`parse_openrouter` returns `data.get("total_count", len(models))` — the count is a
field the fabricator writes inside the committed bytes, not a re-derived count.

### E5 — Digest file is not structurally bound to the two raws

| Variant | Tree state | Result |
|---------|-----------|--------|
| V2 | `SHA256SUMS` exists, zero entries | `verify=ok`, exit 0 |
| V3 | `SHA256SUMS` names only `ghost.bin` with sha256 of `b""` (file absent) | `verify=ok`, exit 0 |
| V8 | `SHA256SUMS` covers only `hf.raw.json`; `or.raw.json` unbound | `verify=ok`, exit 0 |
| V4 | raw bytes swapped, digests NOT updated | `raw=invalid digest mismatch for hf.raw.json: the capture was altered or fabricated`, exit 1 |

Line 137: `data = (out / name).read_bytes() if (out / name).is_file() else b""` — a
missing named file is hashed as empty, and digest lines are never required to name
`hf.raw.json`/`or.raw.json`. V4 shows the one binding that *does* hold: digest line ↔
same-named bytes.

### E6 — No date/freshness token is checked

Receipt `probed=1999-01-01` with entry `verified-at:` line removed → exit 0. Receipt
with `probed=` token removed entirely → exit 0. (V1, V6.)

### E7 — Field-name line and `raw_sha256` line are cosmetics

`raw_sha256 hf=deadbeef or=deadbeef` and `HF missing fields: bogus, names, here, only`
→ exit 0.

### Calibration — what the counter does catch (behavior is not vacuous)

- V4: post-hoc tampering of one raw file without recomputing digests → red.
- V9: the four tokens moved outside the `## Re-probe …` block → red
  (`entry-mismatch missing:hf_models=7`).
- Selftest (in script): absent raw (`raw=absent`) red; entry-block heading removed red.
- The committed lane tree passes at tip: `raw=ok hf_models=50 or_models=467
  hf_schema_delta=4 or_schema_delta=0 verify=ok`, exit 0, so the sandbox shape matches
  the accepted shape. (Committed OR raw holds only 10 records + `total_count=467`;
  `or_models=467` is payload-asserted, corroborating E4.)

### Freshness/overlap notes

Tip code has **no envelope mode** (`meta.observed_models`, `sha256_full`) — the
round-33 build report `R33C3Design.md` rows E1/E4/E6 reference an earlier capture
variant; rows E8/E9 remain true at tip (confirmed E7). The build report already
documented rows a/f/f2 (fabricated/empty/misnamed digests pass); E3/E4/E5(V8) are
independently reproduced here, and E3 (substring-superset number lie) is a new
finding not in R33C3Design.

## Impact

- The freshness claim cannot distinguish a real 2026-10-25 probe from a fabricated
  one; the round's only offline freshness gate is a self-consistency check.
- The kill-rule sentence itself is false: "no fabricated bytes may ever satisfy
  `--verify`" — a single-commit full rewrite satisfies it, so the claim's "honest
  stop" semantics doesn't exist as specified. Any later dispute over whether
  round-33 catalog numbers were observed (vs. written) has no machine-checkable
  answer in the lane.

## Smallest remediation

1. Token equality: replace substring checks (lines 176, 192) with parsing
   `(?:^|\s)hf_models=(\d+)(?:\s|$)` (and the other three) plus `int` equality
   against re-derived values; require `HF missing fields:` list to equal the
   re-derived missing list exactly.
2. Digest structural binding: require `SHA256SUMS` to contain exactly one line per
   `hf.raw.json`/`or.raw.json` (reject empty files, extra names, missing names); treat
   a named-but-absent file as an error, not `b""`.
3. Provenance (the fundamental gap): an offline verifier *cannot* authenticate
   origin. Either (a) explicitly reword the kill rule to state what the check proves
   ("digest binds bytes↔digest file; numbers must re-derive; origin is not
   authenticated"), or (b) add a `--verify-online` mode that refetches both endpoints
   and compares digests/ETag with the committed capture, and run it from C2's
   tip-reading counter at the tip. (a) is required regardless; the committed
   `probed` date itself is a constant in the capture code and carries no authority.
