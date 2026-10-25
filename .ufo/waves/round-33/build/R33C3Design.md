# R33C3Design — C3 `--verify` predicate attack

Role: UFO-FSD critic (leaf). Scope: C3 freshness, frozen at
`plans/round-33-claims.md` §C3, counter `plans/catalog_probe.py --verify --lane .`.
All results from the live lane worktree (commit `2b4cef2`; `catalog_probe.py`
lines 86–239 captured verbatim; the lane's committed `corpus/evidence/round33/catalogs/`
capture inspected). Scratch only: `/tmp/r33-c3design{,2,-final}/`. No production edits.

## 1. Exploit table (fabricated/stale bytes vs `--verify`)

| # | Attack | Result | Counter-output |
|---|--------|--------|----------------|
| a | Fully fabricated `hf.raw.json`+`or.raw.json` (valid JSON shapes, counts 3/5), **self-computed** `SHA256SUMS`, self-authored receipt + entry block | **PASSES (exit 0)** | `raw=ok hf_models=3 or_models=5 hf_schema_delta=0 or_schema_delta=0 verify=ok` |
| f | **Empty** `SHA256SUMS` (digest file exists, zero entries) | **PASSES (exit 0)** | same `verify=ok` |
| f2 | `SHA256SUMS` lists only an unrelated `unrelated.bin` (never `hf.raw.json`/`or.raw.json`) | **PASSES (exit 0)** | same `verify=ok` |
| | Live-claim receipt (hf=50, or=467, delta=4) over tiny fabricated raws (counts 1/1) | RED | `raw=ok receipt-mismatch missing:hf_models=1` |
| c | Receipt counts edited to differ from raw bytes | **CROSS-CHECK CATCHES IT** | `raw=ok receipt-mismatch missing:hf_models=3` |
| b | Raw file >64 KiBB | **RED** | `raw=invalid a raw file exceeds the 65536-byte bound` |
| b2 | Raw truncated *exactly at* 64 KiBB (mid-string) | RED (unparsable) | `raw=unparsable Expecting property name … line 1 column 65537 (char 65536)` |
| d | Entry block lacking the numbers | **RED** | `raw=ok entry-mismatch missing:hf_models=3` |
| e | Verify on live tree at session start | RED | `raw=unparsable Unterminated string starting at: line 1 column 65533 (char 65532)` + `argv=1` |
| E1 | Envelope asserts `meta.observed_models=9999` while bytes contain 1 model | **PASSES (exit 0)** | `raw=ok hf_models=3 or_models=9999 … verify=ok` |
| E8 | Receipt `HF missing fields:` line present but names **bogus** fields | **PASSES (exit 0)** | `verify=ok` (only the literal line is searched) |
| E9 | Receipt `raw_sha256` line **lies** vs `SHA256SUMS` | **PASSES (exit 0)** | `verify=ok` (line never checked) |
| E10 | `probed=1999-01-01` in receipt, no `verified-at`/date anywhere | **PASSES (exit 0)** | `verify=ok` |
| E4 | Envelope `meta` non-dict | Crash (rc 1, traceback `AttributeError`) | `Traceback …` — not a clean verdict |
| E5 | `observed_models="abc"` | RED | `raw=unparsable invalid literal for int() with base 10: 'abc'` |
| E6 | `observed_models="467"` (string) | **PASSES (exit 0)** | `verify=ok` (int() coerces) |

## 2. What `--verify` actually proves vs does not prove

**Proves (offline, no network):** the four tokens `hf_models`, `or_models`,
`hf_schema_delta`, `or_schema_delta` appear **literally** in the receipt and in
the entry's `## Re-probe 2026-10-25 (round 33)` block; the digest file has every
**named** path hash-matching the on-disk bytes (if it names `hf.raw.json` and
`or.raw.json` — see row f/f2); HF count and HF schema-delta re-derive from the
committed HF bytes by parsing; the OR count re-derives only in the non-envelope
path. In short: **internal consistency of three committed artifacts**, per the
ran hook. It **does not prove** the bytes came from `https://huggingface.co/api/models?limit=50`
or `https://openrouter.ai/api/v1/models`, nor that any number was observed on
2026-10-25, nor that the receipt matches the network event — a self-consistent
fabrication is indistinguishable.

## 3. Design weaknesses (ordered)

1. **The 64 KiBB cap cannot hold honest raw bytes for the OR endpoint.** The
   live response is 791,075 bytes (`meta.bytes_total` in the committed envelope);
   `capture()` truncates blind, `json.loads` then fails. The frozen kill rule
   ("no fabricated bytes may ever satisfy `--verify`") is unsatisfiable under
   `capture()` as *any* honest pass must be hand-fabricated or hand-shaped (rows
   b/b2, live-tree `raw=unparsable`). The sibling's envelope patch reached the
   same conclusion and made the artifact non-raw (next point).
2. **Envelope mode makes the OR count circular.** `verify()` takes
   `or_models` from `meta.observed_models` — a number *asserted inside the
   committed bytes* — instead of re-deriving it (E1: 9999 vs 1 present model
   passes). The frozen predicate's "every one of those numbers re-derives exactly
   from the committed raw bytes" is therefore false for the OR count; the
   committed envelope even records `sha256_full` without those bytes being
   committed (nothing can check it). A fabrication exploit for the original
   attack also passes: original fabricated raws + self-computed digests +
   matching receipt (row a).
3. **Digest binding is only as strong as the `SHA256SUMS` file.** Empty or
   misnamed digest files make every hash check a no-op (rows f/f2) — the "digest
   check binds the receipt to the capture" claim is not enforced structurally.
4. **No date check.** `probed=1999-01-01` and no `verified-at:` anywhere still
   verify (E10); the predicate's "fresh" semantics rest entirely on the static
   filename `round33` and the entry heading text.
5. **Token-substring checks, not value/field checks.** `"HF missing fields:"`
   literal existence passes with bogus names (E8); receipt `raw_sha256` line is
   not cross-checked (E9); `or_schema_delta`/`hf_schema_delta` are not verified
   to name the real fields in the entry block (the block only needs the four
   tokens).
6. **Crash rather than verdict** for missing entry file (unhandled
   `FileNotFoundError` traceback, rc 1) and non-dict envelope `meta` (E4).

## 4. Ordering/phase answer

`capture()` writes `after.txt` *after* raw bytes + digests, so a crash between
the writes leaves the receipt absent (red, good). There is no way for a *live*
capture to record probe numbers whose raw bytes show something else — the
receipt numbers are derived from the same full response text that was truncated.
But there is no mechanism stopping *any* producer (a future round, a sibling, a
reviewer) from rewriting raw + digests + receipt + entry **together**; the
committed artifact is self-consistent and `--verify` cannot detect the swap.
The digest check binds the receipt to the committed bytes — not the bytes to
the network.

## 5. Verdict

`VERDICT: c3-design-weak`

- The counter's offline re-derivation discipline is a genuine advance over round
  32's summary-only receipt; rows c/d red are correct and honest.
- The predicate as worded is **not honestly satisfied** by the code: the OR
  count is asserted, not re-derived, and the only `--verify`-passing trees are
  fabricated or hand-shaped (kill rule paraphrased as "no fabricated bytes may
  ever satisfy `--verify`" is false).
- Smallest safe correction: (1) commit the full OR response (≈791 KiB raw JSON)
  instead of the envelope and verify the digest against it — `or_models` then
  re-derives from the bytes; or (2) if the cap must stay, make `OR()` take the
  count from a committed, re-derivable artifact (e.g. a separate newline-delimited
  ID list from the full response) and drop the `meta.observed_models` trust. In
  either case: require `probed=2026-10-25` in the receipt, require every digest
  line to name exactly `hf.raw.json`/`or.raw.json`, and replace the substring
  checks with parsed-value equality (incl. `HF missing fields:` names).
