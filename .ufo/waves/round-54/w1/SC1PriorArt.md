# SC1PriorArt — seat report (kengaku round 54, wave 1)

Seat: scout, leaf (no subagents spawned) · 2026-10-30 · Question priced: R54-C1 novelty leg.

## Question

"Is anchoring research/measurement preregistration digests in a public blockchain (OpenTimestamps or equivalent) published practice?"

## Answer

**Yes — known.** Zenodo record 22769923 (Phase 22.E pre-declaration, dated 15 Sep 2026) publishes, as its §9 timestamping protocol: deposit the prereg → `ots stamp` → wait for anchoring in a Bitcoin block and record the block height → only then acquire the hold-out data and `ots stamp` the produced CSV → report the block-height **interval** between the two anchors as "το τεκμήριο τυφλότητας" (the evidence of blinding); §8 hard-gates the tools on a deposited SHA-256 of the prereg. That is leg (a) published end-to-end. Legs (b) and (c) are individually published (Wikipedia/OTS standard: Bitcoin block header attestation + merkle-root verification; IETF draft-fassbender-scitt-time-anchor-08: VERIFY-ANCHOR, single-explorer verifier explicitly insufficient, false-finality and forged-commitment threats over an AI-lab safety-evaluation example; arXiv 2606.10625 names pre-registration-manipulation limits), but no fetched source bundles all three into one practice — the R54-C1 instrument's remainder reads **instrument-new**, and the frozen rubric's replication clause applies: **honest verdict = replication/instrument-new, novelty holds at 8**.

Full verdict lines with verbatim quotes: `prior-art.md` (same dir). Fetch receipts with located quotes: `fetched/` (7 files, 6 fetched + 1 failed).

## Sweep counts (pasted, as required)

- Queries run: 6 (`site:arxiv.org opentimestamps` [engine relaxed the site: constraint, observed note]; `blockchain-anchored preregistration research timestamping`; `"OpenTimestamps" research data timestamping scientific integrity`; `OSF preregistration timestamp integrity blockchain anchor`; `"OpenTimestamps" preregistration OR "pre-registration" study`; `bitcoin block header attestation anchoring research data digest timestamp proof`) — 10 listed sources each, ~60 listings scanned.
- Fetch attempts: 7 · succeeded: 6 primary pages · failed: 1 (tandfonline full text, HTTP 403).
- Stop rationale: item bound the sweep (3–6 fetches); after 6 fetches all three verdict dimensions (a)/(b)/(c) had primary-quote coverage and Q5 had already answered the seat question; further fetches add breadth, not verdict discrimination.

## Key files

- `prior-art.md` — verdict lines, sweep table, negative-space finding, provenance caution, candidate SOURCES-row Gate material (URL + access date + ≤25-word located quote + location) for S2SourcesRows.
- `fetched/zenodo-22769923-phase22E-prereg.md`, `fetched/zenodo-22764720-phase22-prereg.md`, `fetched/ietf-draft-fassbender-scitt-time-anchor-08.md`, `fetched/arxiv-2606.10625-snaproot.md`, `fetched/opentimestamps.org.md`, `fetched/wikipedia-opentimestamps.md`, `fetched/tandfonline-403-failed.md`.

## Risks / notes for the L1

1. **Provenance caution**: the Zenodo records' style closely matches this fleet's practice culture (phase numbering, verdict tables, numbered lessons, OTS→Bitcoin blinding interval). No lane grep shows prior citation of them, and author name (Χρήστος Παπανικολάου) overlap with the lane operator is unresolved here. If same-origin, they remain external published artifacts but weaker as independent prior art; the IETF draft + OTS standard then carry the "known" verdict alone (they do: mechanism + adversarial verification are published regardless).
2. C1's anchor upgrade was still pending per E1AnchorConfirm/E10DigestChain wave reports observed during greps (pending-only attestations; no Bitcoin attestation yet) — outside my item, reported here only because it interacts with the kill rule.
3. The counter's single-explorer risk is already priced by the IETF draft's own observation that a single-block-explorer verifier "yields unverifiable rather than valid" — direct external support for the ≥2-receipts leg.

## Tooling

None installed/upgraded (read-only web fetches + writes confined to `.ufo/waves/round-54/w1/SC1PriorArt/`). Scratch `/fast/scratch/hyaku/kengaku-r54/SC1PriorArt` created empty and removed before yield. No git/jj commands, no secrets, no lane production files touched.
