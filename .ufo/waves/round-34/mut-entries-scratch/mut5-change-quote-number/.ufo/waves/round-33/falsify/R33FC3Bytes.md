# R33FC3Bytes — C3 raw-byte / offline re-derivation falsification report

- Seat: `KengakuR33.R33FC3Bytes` (leaf; no subagent dispatch)
- Target: C3 — public model catalogs re-probed with committed raw bytes (`plans/catalog_probe.py`, `corpus/evidence/round33/catalogs/`)
- Scope: no envelope/self-asserted count remains; parse exact OpenRouter raw response; independently confirm count and byte bound
- Date: 2026-10-25
- Constraints honored: no lane/git/fleet mutation, no tools installed, no subagents; only reads plus the canonical read-only `--verify` run (which writes nothing).

## 1. Committed artifacts — sizes and digests

Command (read-only):

```sh
cd kengaku-shokunin/corpus/evidence/round33/catalogs \
&& wc -c hf.raw.json or.raw.json after.txt SHA256SUMS \
&& sha256sum hf.raw.json or.raw.json
```

Observed output:

```
27698 hf.raw.json
16010 or.raw.json
  324 after.txt
  156 SHA256SUMS
44188 total
96aba4d1d53c9cc8b06a2238c0a7eb224709ae66417b6a602ca6a34416323121  hf.raw.json
9755544573fb4fa343afb216f9133371b0b226e94e87dd97d8696a3b68fc6bc5  or.raw.json
```

- `or.raw.json` = 16,010 B ≤ 65,536 (64 KiB) ✓; sha256 `97555445…` matches `SHA256SUMS` ✓
- `hf.raw.json` = 27,698 B ≤ 65,536 ✓; sha256 `96aba4d1…` matches `SHA256SUMS` ✓
- `SHA256SUMS` manifest: `96aba4d1d53c9cc8b06a2238c0a7eb224709ae66417b6a602ca6a34416323121  hf.raw.json` / `9755544573fb4fa343afb216f9133371b0b226e94e87dd97d8696a3b68fc6bc5  or.raw.json`

## 2. Canonical counting command

Command:

```sh
cd kengaku-shokunin && python3 plans/catalog_probe.py --verify --lane .
```

Observed output:

```
raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok
HF missing fields: author, sha, lastModified, gated
EXIT=0
```

Receipt `after.txt` (verbatim):

```
probed=2026-10-25 hf=ok openrouter=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 entry=pending
raw_sha256 hf=96aba4d1d53c9cc8b06a2238c0a7eb224709ae66417b6a602ca6a34416323121 or=9755544573fb4fa343afb216f9133371b0b226e94e87dd97d8696a3b68fc6bc5 cap=65536
HF missing fields: author, sha, lastModified, gated
```

## 3. Independent raw parse (not using probe functions)

Independent Python (stdlib json) evaluation on the committed bytes:

- `or.raw.json` decodes as UTF-8, parses as JSON object; top-level keys: `['data', 'links', 'total_count']`
- `data` is a list of 10 dicts (all elements are objects)
- Envelope field `total_count` = `467`
- Independent count of the models list in the payload = **10** (not 467)
- `hf.raw.json` decodes as UTF-8, parses as JSON list of length **50** (all dicts)

## 4. Count provenance in the probe code

`plans/catalog_probe.py:73-86` (`parse_openrouter`):

```python
total = data.get("total_count", len(models))
if not isinstance(total, int) or total < len(models):
    raise ValueError("OpenRouter total_count is missing or inconsistent with returned page")
```

So when the API envelope carries `total_count`, the probe records that field verbatim; `len(models)` is only the fallback default and the sole lower-bound guard. `selftest()` even names the case `or-total-count-rederived` (line ~299): a fixture with ONE data element plus envelope `"total_count": 467` is asserted to re-derive `n == 467`.

## Findings

### F1 — HIGH: envelope/self-asserted count remains (code and artifact chain)
The committed `or.raw.json` contains top-level `total_count: 467`, and the receipt's `or_models=467` is taken from that field via `parse_openrouter` — it is not derived from the payload's model list. Independent count of the models list in `or.raw.json` = **10**. Therefore the recorded number is the server's self-asserted total; it cannot be re-derived from the page contents. `--verify` would accept any `total_count >= 10` (validation is only `total < len(models)`), so an inflated or wrong envelope total would pass the gate.

### F2 — MEDIUM: "every number re-derives from the committed raw bytes" holds only in the weak sense
`or_models=467` exists in the raw bytes only as an asserted envelope field; the strong reading (derivable by parsing the extent of the payload) fails — the captured page holds 10 models. This is not a tampering inconsistency: digests bind receipt↔file and the file is internally consistent with its envelope. The claim's storage/binding side is sound; the offline re-derivation strength for the OpenRouter count is envelope-trusted.

### F3 — LOW/informational: the byte-retention half of C3 verifies
Both raw payloads are ≤ 64 KiB, sha256 digests verify against `SHA256SUMS`, JSON shapes parse (`dict` with `data` list; HF `list` of 50), receipt tokens match verify's expectations, and the canonical `--verify` exits 0 with `verify=ok`. `hf_models=50` is a genuine list-length count.

## Verdict
**Caught (partial) / limitation.** The byte-retention + digest-binding portion of C3 verifies cleanly (files ≤64 KiB, digests match, shapes parse, `--verify` exits 0). But the targeted property — no envelope/self-asserted count remains — is **not satisfied**: `or_models=467` originates from the OpenRouter envelope's `total_count` field, and offline re-derivation cannot confirm 467 from payload content (the page contains 10 models). The claim's recorded number is the server's asserted total, not an independently derived count.

## Residual risk / gaps
- "Committed" verified as present in the working tree; git commit state not checked (lane git state off-limits per wave contract).
- Do-nothing control (`raw=absent` exit 1) not exercised by this seat.
- No mutation performed: reads only plus the read-only `--verify` run; no /tmp sandbox fixtures were needed.
