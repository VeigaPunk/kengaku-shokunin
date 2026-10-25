# R33FCapability — round-33 capability row `offline-catalog-receipt-verification` (SCORECARD.md:561)

Seat: `KengakuR33.R33FCapability` (leaf; no subagent dispatch). Date: 2026-10-25.
Target: the new capability row in `SCORECARD.md` line 561 — verify the command really runs
without network, tests tamper detection, parses `total_count` from bytes, and its
first-working round is properly stated. No lane file was written or mutated; all fixture
work happened in a fresh /tmp sandbox (`/tmp/r33cap.u23na9`, retained). No tools installed.

## Row under test (verbatim, SCORECARD.md:561)

> `offline-catalog-receipt-verification` | Re-derive catalog totals and schema deltas from
> committed, bounded raw API responses without network access; OpenRouter uses the response's
> `total_count` plus returned sample and the digest binds the exact JSON bytes |
> `python3 plans/catalog_probe.py --verify --lane .` → `raw=ok hf_models=50 or_models=467
> hf_schema_delta=4 or_schema_delta=0 verify=ok`; raw responses + SHA256 in
> `corpus/evidence/round33/catalogs/` | 33

## 1. The command really runs without network — UNCAUGHT

Canonical run (lane root), output byte-matches the row's evidence string first line:

```
$ python3 plans/catalog_probe.py --verify --lane .
raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok
HF missing fields: author, sha, lastModified, gated
EXIT=0
```

Offline proof 1 — run inside a network-less namespace (`sudo -n unshare -n`, no network
namespace): identical output, exit 0.

Offline proof 2 — syscall trace `strace -f -e trace=network` during `--verify`: zero
network syscalls recorded (only `+++ exited with 0 +++`). `verify()` (catalog_probe.py:147-203)
calls only `_load_raw`, `parse_hf`, `parse_openrouter`, and entry/receipt reads; `fetch()`
(line 57) is never reached in `--verify` mode. No DNS/socket/connect during the run.

## 2. Tamper detection — CAUGHT (partial)

The script tests tamper detection and the basic single-file case is red:

- `--selftest`: 13/13 PASS, including `verify-digest-tamper-red` (mutate raw, digest
  untouched → `raw=invalid digest mismatch for hf.raw.json: the capture was altered or fabricated`,
  exit 1).
- Sandbox (fresh /tmp clone of the committed receipt): single-byte mutation of
  `hf.raw.json` with `SHA256SUMS` untouched → red, exit 1 (same result for `or.raw.json`).

**Bypasses observed in the sandbox (all green, exit 0):**

| # | Mutation | Outcome |
|---|---|---|
| T2 | Tamper `hf.raw.json` *and delete its line from `SHA256SUMS`* | `raw=ok ... verify=ok`, exit 0 — the missing digest line is simply not checked |
| T4 | Empty `SHA256SUMS` file | exit 0 — manifest is optional in effect; a capture with no digest lines passes |
| T3 | Inflate receipt numbers: `after.txt` `hf_models=50`→`hf_models=501`, `or_models=467`→`or_models=4670` | exit 0 — receipt tokens are matched as *substrings* (`"hf_models=50" in receipt`), so `501`/`4670` satisfy them |
| T9 | Same inflation inside the entry's re-probe block | exit 0 — same substring match in `open-model-catalogs.md` |

The per-file digest check is self-referential: `SHA256SUMS` is committed but unpinned
externally, so a coordinated rewrite (raw bytes + re-signed manifest) passes — corroborated
by sibling `R33FVerifyTamper.md` §5 and build-wave `R33C3Design` (rows a/f/f2). The row's
"the digest binds the exact JSON bytes" therefore holds for *within-manifest* consistency
only; it is not tamper-proof against an attacker who can rewrite the manifest, and the
receipt/entry numbers are not exact-value bound.

## 3. Parses `total_count` from bytes — UNCAUGHT (with wording caveat)

- `parse_openrouter` (catalog_probe.py:73-86) reads `total_count` from the parsed JSON
  bytes: `total = data.get("total_count", len(models))`, with only `total < len(models)`
  as a guard; `selftest` asserts the `or-total-count-rederived` case (1 data item + envelope
  `total_count=467` → 467).
- The committed `or.raw.json` bytes actually contain `total_count: 467` (top-level keys
  `data`, `links`, `total_count`; `data` length 10). The printed `or_models=467` comes from
  that byte field, exactly as the row says ("uses the response's `total_count` plus returned
  sample").
- Caveat (matches sibling `R33FC3Bytes.md` F1/F2): 467 is the server's asserted envelope
  total, not derivable from the retained page contents (10 models); the HF number
  `hf_models=50` is a genuine list-length but is limit-bound (`?limit=50`), so "catalog
  totals" is generous — HF's figure is a capped sample size, not a total. The row's own
  wording already distinguishes the OpenRouter case correctly; the general "totals" phrase
  overstates what offline re-derivation can prove.

## 4. First-working round = 33 — UNCAUGHT (properly stated)

- Round 32 (`plans/round-32-claims.md` §C3) used `catalog_probe.py --diff` — a *live*
  probe; its receipt (`corpus/evidence/round32/catalogs/after.txt`) explicitly says raw JSON
  existed only in a seat's /tmp capture and was cleaned; no offline verify mode existed.
- `--capture`/`--verify` and the committed `round33/catalogs/` bytes are new in round 33
  (catalog_probe.py:44-54; `plans/round-33-claims.md` §C3). Freeze control committed at
  `.ufo/waves/round-33/claims/control-verify.txt` shows the do-nothing pre-probe tree
  `raw=absent`, exit 1.
- SCORECARD row 561 states first-working round 33 and is consistent with the round-32
  section (`failed as declared`, no capability row) and the round-33 section (line 1134
  before `raw=absent` → after verify ok). The post-table sentence "entered in round 33 by
  passing its offline counter" is supported.

## Verdict

Four acceptance points: offline run **UNCAUGHT**; total_count-from-bytes parse
**UNCAUGHT** (byte-verified, with envelope-trust caveat); first-working round **UNCAUGHT**
(33 correct); tamper detection **CAUGHT (partial)** — the basic single-file digest tamper is
red and selftested, but three green bypasses (dropped/empty digest manifest, receipt and
entry number inflation via substring match, coordinated re-signing) mean the row's
tamper/digest-binding strength is overstated as a robustness guarantee.

Overall: the row is operational and its evidence pointer reproduces exactly; the claim's
*strength* is limited to internal consistency of four committed artifacts, not
authentication of the network event nor exact-value receipt binding.

## Limits / notes

- Git commit state not checked (lane git state off-limits per wave contract); "committed"
  verified as present in the working tree.
- `after.txt` still records `entry=pending` while the entry now carries the re-probe block —
  minor receipt stale-ness; does not affect `--verify` (entry tokens checked separately).
- Sandbox retained: `/tmp/r33cap.u23na9` (baseline + T1–T7 + receipt/entry inflation cases).
- No lane files touched; no installs (strace/sudo pre-existing).

Report trailer: `.ufo/waves/round-33/falsify/R33FCapability.md`
