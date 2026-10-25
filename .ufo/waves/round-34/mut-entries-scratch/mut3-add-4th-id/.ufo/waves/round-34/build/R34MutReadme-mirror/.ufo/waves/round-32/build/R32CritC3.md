# Round 32 C3 critic — catalog freshness

Scope: attack `plans/catalog_probe.py --diff --lane .` against the frozen C3 predicate. Read-only review; no probe or production files changed, and no tools installed.

## Evidence

`plans/catalog_probe.py` lines 82–91 checks that the entry exists, has a line matching `^verified-at: 2026-10-25\b`, contains both substrings `S101` and `S102`, and contains the literal receipt-directory string. It does not open source-registry rows or receipt files. Lines 109–120 print counts/deltas and return success if probe returns `ok`, both missing-field lists are empty, and `entry_ok` says `ok`. `parse_hf` and `parse_openrouter` (51–71) test only the first item. `probe` (74–79) fetches HF and then OpenRouter sequentially, returning a single all-or-nothing tuple.

The frozen claim requires the entry to cite S101/S102, have a receipt pointer under the receipt directory, and record schema-delta per source (round-32-claims.md:85–111). Its kill rule says an unreachable API gives an honest partial result and the unreachable source does not pass (108–109). The baseline entry has neither C3 date nor S101/S102 (open-model-catalogs.md lines 1–5; registry search returned no S101/S102 matches); the freeze control captured a successful live probe but stale entry, including `hf_schema_delta=4 or_schema_delta=0` (catalogs-before.txt:1–5). No `corpus/evidence/round32/` directory existed at review time.

## Attack routes and verdicts

| Route | Strong counterexample / code path | Verdict |
|---|---|---|
| (a) Cite S101/S102 without probe | Put the two bare strings, dated line, and receipt-directory string in the entry. `entry_ok` accepts them; it never verifies registry provenance or that this run created/opened anything. However, ordinary `--diff` still performs both live fetches and requires both schemas to have no missing expected fields. | **Escape on entry provenance; kill for wholly fake/no-network probe.** The gate does not establish the citations identify this round's actual opened rows, but the required successful network sample still limits a fully offline fake. |
| (b) Print deltas, don't record them | A real successful probe prints the counts and missing fields to stdout, then tests only that both missing lists are empty. No comparison with or parsing of the entry's delta record occurs. | **Escape.** C3 can pass without any schema-delta being recorded, contrary to frozen predicate. |
| (c) `verified-at` with no receipts | Entry containing date, both ids, and `receipts: corpus/evidence/round32/catalogs/` passes `entry_ok`; neither directory nor pointed file is checked. The built-in selftest explicitly creates this pointer without a receipt file and expects green (146–156). | **Escape.** Receipt pointer is not a receipt; absent evidence is accepted. |
| (d) Network flakiness / partial probe | `probe()` fetches HF then OpenRouter; any exception bubbles to one `except`, which sets one `fail:<type>`, zeros both counts and clears both deltas (102–108). Thus an OpenRouter outage after HF succeeds discards HF success and reports both failed. It exits 1 (120), so no partial-success false pass. | **Kill (safe failure), but dishonest/incomplete partial accounting.** It fails closed, while violating the frozen partial-result reporting rule; a successful HF result is erased. |
| (e) Schema delta checks first item only | Both parsers validate a nonempty list and inspect `data[0]` only (HF 53–58; OpenRouter 65–71). A response whose first object contains every expected field but later objects omit required fields has zero schema delta and can pass. | **Escape.** A heterogeneous catalog is certified from one item. |

## Smallest safe correction

Keep the live two-API success condition, but make evidence part of the predicate: require actual receipt files and validate their source URLs, captured response identity/time, and recorded counts/delta against the run; validate S101/S102 as registry rows opened on the access date and used by the entry. Record each source's delta in the entry and compare it with the probe result. Probe each endpoint independently so one failure preserves the other result while overall exit remains nonzero unless both pass. For the stated delta definition, inspect all sampled records (or explicitly define a bounded sample and report its size); do not infer whole-catalog schema from index zero.

VERDICT: attack-finished