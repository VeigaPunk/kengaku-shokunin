# R33FOpenRouter — OpenRouter bounded raw query and count semantics

**Seat:** KengakuR33.R33FOpenRouter (leaf executor; single labrat, no subagents)
**Date:** 2026-10-25 · **Scope:** `plans/catalog_probe.py` + committed `corpus/evidence/round33/catalogs/or.raw.json`
**Verdict:** **caught (count semantics flawed)** — artifact is genuine and fresh today, but `or_models` is an envelope-trusted passthrough, not a re-derivation; `or_schema_delta` samples a single object; receipt date/sha lines are unchecked.

---

## 1. Independent parse of committed `or.raw.json`

| check | observed |
|---|---|
| bytes | 16,010 (under 64 KiB cap; `hf.raw.json` = 27,698) |
| sha256 | `9755544573fb4fa343afb216f9133371b0b226e94e87dd97d8696a3b68fc6bc5` — matches `SHA256SUMS` **and** the receipt's `raw_sha256 or=` line |
| JSON shape | top-level dict, keys `data`, `total_count`, `links` |
| `len(data)` | **10** model objects |
| `total_count` | **467** (int) |
| `links.next` | `/api/v1/models?offset=10&limit=10` → committed bytes are **page 1 of ≈47** |
| first entry | `moonshotai/kimi-k3.1-pro`, 20 keys incl. all 12 `OR_FIELDS` |

## 2. Freshness: committed bytes == live bounded query today

```
$ curl -sS -A "kengaku-catalog-probe/1.0" -o /tmp/or.limit10.json \
    "https://openrouter.ai/api/v1/models?limit=10"
$ sha256sum /tmp/or.limit10.json
9755544573fb4fa343afb216f9133371b0b226e94e87dd97d8696a3b68fc6bc5  /tmp/or.limit10.json
```
Byte-identical (16,010 B) to the committed file — the committed `or.raw.json` is genuinely the `?limit=10` response for `OR_URL = "https://openrouter.ai/api/v1/models?limit=10"`.

Live unfiltered `?` (no query) today: 791,075 B, `len(data)=467`, `total_count=467`, `links.next=None`; page data exactly equals full `[0:10]` (ids and first-object bytes equal). So **467 is the true live count**, and the committed page is literally the catalog's first 10 models — but the committed 16,010 B cannot establish that: they only show a `total_count` envelope integer plus 10 objects.

```
$ python3 plans/catalog_probe.py --verify --lane .      # read-only, committed tree
raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok
EXIT=0
```

## 3. Falsification experiments (fresh `/tmp` sandbox per case; lane untouched)

Each case copies the exact lane artifacts into `/tmp/r33-or-cases/<case>`, mutates only the copy, recomputes `SHA256SUMS`, syncs receipt/entry tokens, runs `catalog_probe.py --verify --lane .`.

| case | mutation (copy only) | result |
|---|---|---|
| **E1** | `total_count` 467 → **999999** (10 models unchanged) | **EXIT 0**, prints `or_models=999999` |
| **E2** | delete `total_count` entirely | **EXIT 0**, prints `or_models=10` (page-length fallback) |
| **E3** | strip `reasoning` from data[5], `pricing` from data[7] | **EXIT 0**, still `or_schema_delta=0` |
| **E4** | `total_count=9` (< len(data)) | EXIT 1, `raw=unparsable ... inconsistent with returned page` (sole cross-check) |
| **E5** | receipt `raw_sha256 or=` → `deadbeef` **and** `probed=1999-01-01` | **EXIT 0** |

`parse_openrouter` (`catalog_probe.py:44-58`) does:

```python
total = data.get("total_count", len(models))
if not isinstance(total, int) or total < len(models):
    raise ValueError(...)
```
and computes missing fields from `models[0]` only.

## 4. Do all receipt numbers derive from raw bytes?

- **Strictly yes for the four tokens** — `hf_models=50` (re-parsed list length), `or_models=467` (passthrough of `total_count`), `hf_schema_delta=4`, `or_schema_delta=0` (single-object scan) — plus byte count and digest are internally consistent.
- **But the OR count is not re-derived from observed models.** `or_models=467` is trusted from a server-asserted envelope integer; the only enforced invariant is `total_count >= len(data)` (E4). The entry's phrase "`or_models=467` re-derives from that retained response" is vacuously true — the number happens to be true today (live full catalog = 467), but the committed bytes cannot prove it (E1: any integer ≥ 10 passes).
- **`or_schema_delta=0` overclaims coverage** — computed from `models[0]` only, so it says nothing about the other 9 captured objects, let alone the 467-model catalog (E3).
- **Not all receipt fields derive from bytes**: `probed=2026-10-25`, `hf=ok openrouter=ok`, `entry=pending`, `cap=65536` are code constants, and the receipt's `raw_sha256` line is never checked (E5 — sha lies and date lies still verify green; the *binding* check is `SHA256SUMS`, which is enforced).

## 5. Retained evidence

- `artifact://10569` — round-33 build dir listing.
- Commands/outputs above, all run 2026-10-25 from `/home/vgpnk/Projects/shokunin/kengaku-shokunin` and `/tmp/r33-or-cases/*`.
- Characteristic outputs:
  - E1: `raw=ok hf_models=50 or_models=999999 hf_schema_delta=4 or_schema_delta=0 verify=ok` EXIT=0
  - E2: `raw=ok hf_models=50 or_models=10 hf_schema_delta=4 or_schema_delta=0 verify=ok` EXIT=0
  - E5: `raw=ok ... verify=ok` EXIT=0 after receipt sha+date lies

## 6. Risks / blockers

- None blocking. Network was available; live probes are read-only. No tools installed (no `sudo`/pacman/uv/cargo usage — none required). No lane files were edited, staged, or committed; all mutations confined to `/tmp/r33-or-cases` and `/tmp/r33-or-sandbox{,2}`.

Report: .ufo/waves/round-33/falsify/R33FOpenRouter.md
