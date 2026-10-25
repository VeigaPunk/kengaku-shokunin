# R33FVerifyTamper — C3 offline verifier tamper behavior

Round 33 hyaku run 7 falsify wave · seat: `KengakuR33.R33FVerifyTamper` (leaf) ·
date: 2026-10-25 · target: frozen claim C3 (freshness, `plans/catalog_probe.py --verify`)
from `plans/round-33-claims.md` §C3.

## Assignments (exactly as run)

> In a /tmp clone of the catalog receipt, mutate a raw byte without changing SHA256SUMS
> and run `plans/catalog_probe.py --verify --lane <tmp>`. Confirm expected red, record
> exit/output, and ensure no lane files are touched.

## Method

Fresh `/tmp` sandboxes only (`/tmp/r33f-verify-tamper`, `-or`, `-resign`), each cloned
read-only from the lane's committed receipt `corpus/evidence/round33/catalogs/`
(hf.raw.json, or.raw.json, SHA256SUMS, after.txt), the entry
`corpus/knowledge/open-model-catalogs.md`, and the counter script `plans/catalog_probe.py`
(all byte-identical to lane at clone time, `sha256sum` verified). `git init` used only
inside each sandbox (baseline commit before tampering) — no git command touched the lane.
No tools installed; no lane file written or mutated.

## 1. Baseline (clean clone)

```
$ cd /tmp/r33f-verify-tamper && python3 plans/catalog_probe.py --verify --lane .
raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok
HF missing fields: author, sha, lastModified, gated
EXIT=0
```

## 2. Tamper A — single raw byte in hf.raw.json, SHA256SUMS unchanged (the assigned step)

Byte-level mutation (no length change, JSON kept valid): `"likes":2935` → `"likes":6935`
at byte offset 87 (0-based) / 88 (1-based), the `2` replaced by `6` via `dd conv=notrunc`:

```
$ grep -b -o '"likes":2935' hf.raw.json   # offset 79
$ printf '6' | dd of=hf.raw.json bs=1 seek=87 count=1 conv=notrunc status=none
$ cmp -l <lane hf.raw.json> <clone hf.raw.json>
88  62  66                # octal 062='2' vs 066='6' — exactly one differing byte, size 27698 both
$ grep -o '"likes":6935' hf.raw.json        # mutation present
$ python3 -c "import json;d=json.load(open('hf.raw.json'));print(len(d))"  # 50 — still parses, numbers unchanged
$ sha256sum SHA256SUMS   # identical to lane (fa32b73c…) — digest file untouched
```

Tampered run:

```
$ python3 plans/catalog_probe.py --verify --lane .
raw=invalid digest mismatch for hf.raw.json: the capture was altered or fabricated
EXIT=1
```

**Verdict: CAUGHT.** Expected red confirmed; exit 1. The red is emitted before any
parsing or number derivation (the digest check runs first), so the verdict is the digest
binding, not a coincidental parse failure. Sandbox `git diff --stat` after the run shows
exactly `1 file changed, 1 insertion(+), 1 deletion(-)` (hf.raw.json) and
`SHA256SUMS diff lines: 0`.

## 3. Tamper B — single raw byte in or.raw.json, SHA256SUMS unchanged

`"total_count":467` → `"total_count":468` at byte offset 15955 (0-based), same `dd`
technique. SHA256SUMS byte-identical to lane (`fa32b73c…`).

```
$ python3 plans/catalog_probe.py --verify --lane .
raw=invalid digest mismatch for or.raw.json: the capture was altered or fabricated
EXIT=1
```

**Verdict: CAUGHT.** Both committed raw files are digest-covered; neither survives a
single-byte mutation while SHA256SUMS stays put.

## 4. Lane integrity (no lane files touched)

Every lane file hash-matches the pristine sandbox baseline commit (created from the lane
before any tampering): hf.raw.json `96aba4d1…`, or.raw.json `9755544573…`, SHA256SUMS
`fa32b73c…`, after.txt `e63cfa42…`, entry `d4fc27f4…`, script `1f202c3e…` — all MATCH.
Lane mtimes (14:34:25 / 14:34:34 / 14:43:43 on 2026-10-25) predate this seat's runs; the
read-only control on the real lane still exits 0:

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/catalog_probe.py --verify --lane .
raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok
EXIT=0
```

## 5. Boundary limitation (outside the assigned step, recorded for the integrator)

The digest check is self-referential: it verifies each raw file against the *committed*
`SHA256SUMS` file, which is itself unpinned and mutable. Boundary probe (sandbox
`/tmp/r33f-verify-tamper-resign`): mutate one raw byte that does not change any derived
number (`"downloads":85275` → `"downloads":85274`) **and** re-sign SHA256SUMS
(`sha256sum hf.raw.json or.raw.json > SHA256SUMS`), leaving receipt and entry untouched:

```
$ python3 plans/catalog_probe.py --verify --lane .
raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok
EXIT=0
```

So a *coordinated* rewrite (raw bytes + SHA256SUMS, receipts unchanged in the four
numbers) passes; this matches the build-wave `R33C3Design` rows a/f/f2 (fully fabricated
self-consistent tree passes; empty or misnamed SHA256SUMS makes every hash check a no-op;
`raw_sha256` receipt line lies unchecked). The assigned step — a single raw-byte mutation
with SHA256SUMS left at the committed value — is caught, but the verifier establishes
internal consistency of three committed artifacts, not an anchor to the network event.

## Verdict / evidence retained

- Assigned falsify: **CAUGHT** (red, `raw=invalid digest mismatch for hf.raw.json`,
  exit 1; same for or.raw.json). No lane files touched; lane still verifies green.
- Boundary limitation (not the assigned step): **limitation** — re-signed digest file
  narrows the tamper to "one byte, not two files".
- Sandboxes retained: `/tmp/r33f-verify-tamper` (Tamper A + git baseline), `/tmp/r33f-verify-tamper-or` (Tamper B), `/tmp/r33f-verify-tamper-resign` (boundary).
- Exact commands/outputs as above; no installs; tools: python3, dd, cmp, grep, git
  (sandbox-scoped), sha256sum, stat.

Report trailer: `.ufo/waves/round-33/falsify/R33FVerifyTamper.md`
