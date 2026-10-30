# Prior art — R54-C1: is anchoring research/measurement preregistration digests in a public blockchain (OpenTimestamps or equivalent) published practice?

Seat: SC1PriorArt (scout, leaf) · kengaku round 54 wave 1 · 2026-10-30 · lane: kengaku-shokunin
Claim priced: R54-C1 (novelty 8→9), externally anchored measurement freeze (`plans/round-54-claims.md`, frozen; its bytes are the C1 anchor digest — not touched).
Fetch receipts: `fetched/` (this dir) — one file per URL: URL, access date, fetch method, verbatim located quotes.

## Bottom line

**Yes — published practice (verdict: known).** A publicly deposited, dated preregistration (Zenodo 22769923, 15 Sep 2026) explicitly hard-codes the procedure "deposit prereg → `ots stamp` → wait for Bitcoin-block anchoring, record block height → only then acquire data and `ots stamp` the produced data file → report the block-height **interval** as the evidence of blinding", and gates its tools on a deposited SHA-256 of the prereg. The OTS→Bitcoin mechanism and header-attestation verification are standard published practice (opentimestamps.org, Wikipedia, IETF draft). What no fetched source documents as a single practice is the R54-C1 instrument's exact trio: digest-before-measurement **plus** ≥2-independent-explorer block-header/explorer receipt verification **plus** forged-proof/pending-proof adversarial controls over an eval pipeline's freeze — the IETF draft is closest (VERIFY-ANCHOR procedure, single-explorer verifier called insufficient, negative test vectors, false-finality threat).

Per the frozen rubric in `plans/round-54-claims.md`: "If prior art shows Bitcoin-anchored preregistration freezes are published practice, the honest verdict is replication/instrument-new and the score holds at 8 — the rubric's replication clause is applied, not argued away." **This finding triggers exactly that clause: prior art exists; honest verdict = replication/instrument-new.**

## Sweep record (bounded search)

Search engine: agent web_search (AI-summarized listings; every load-bearing quote below comes from the fetched primary pages, never from the summaries).

| # | Query | Sources listed | Notable |
|---|---|---|---|
| Q1 | `site:arxiv.org opentimestamps` | 10 | engine note observed: "no results matched `site:arxiv.org`; the constraint was relaxed" — no arXiv-hosted OTS paper surfaced on this query; arXiv coverage came via Q6's snaproot (arxiv.org/html/2606.10625v1) |
| Q2 | `blockchain-anchored preregistration research timestamping` | 10 | surfaced tandfonline primer, MDPI anchoring paper, OSF pages, OriginStamp/BaseStamp |
| Q3 | `"OpenTimestamps" research data timestamping scientific integrity` | 10 | surfaced 34C3 OTS session, opentimestamps.org, atproto discussion |
| Q4 | `OSF preregistration timestamp integrity blockchain anchor` | 10 | surfaced CSIRO blockchain-anchor pattern, snaproot (arXiv), OSF registries |
| Q5 | `"OpenTimestamps" preregistration OR "pre-registration" study` | 10 | surfaced the two Zenodo preregistration records (22769923, 22764720) + Wiley research-synthesis prereg paper |
| Q6 | `bitcoin block header attestation anchoring research data digest timestamp proof` | 10 | surfaced IETF SCITT time-anchor draft, IEEE Merkle anchoring paper, OTS python docs |

Fetch attempts: 7 · succeeded: 6 primary pages (2 Zenodo primary files, IETF datatracker, arXiv HTML, opentimestamps.org, Wikipedia) · failed: 1 (tandfonline full text, HTTP 403 — receipt in `fetched/`).
Stop rationale: the item bound the sweep (3–6 fetches); after 6 fetches all three verdict dimensions (a)/(b)/(c) are covered by located primary quotes, and Q5 had already produced a direct answer to the seat question; further fetches add breadth, not verdict discrimination.

## Fetched sources and verdict lines

Verdict vocabulary per item: known / adjacent / not-found, with claims-file mapping (known → "published practice"; the rubric's replication/instrument-new clause).

### S-A. Zenodo record 22769923 — Phase 22.E pre-declaration (Linear A/Knossos study) — **known**
Receipt: `fetched/zenodo-22769923-phase22E-prereg.md` (bytes: `https://zenodo.org/records/22769923/files/184_phase22E_prereg_v1.md`, accessed 2026-10-30).
Documents: §9 "Χρονοσφράγιση — δίδαγμα #19" orders: Zenodo deposit + `ots stamp` → "Αναμονή αγκύρωσης σε block του Bitcoin · καταγραφή ύψους block" (wait for anchoring in a Bitcoin block · record block height) → "**Μετά**" (only after that) run the harvester on hold-out data, `ots stamp` the produced CSV, and "Καταγραφή του ύψους block των δεδομένων και του **διαστήματος** μεταξύ των δύο" (record the data block height and the interval between the two) — "Το διάστημα αναφέρεται ως μέγεθος της μελέτης. Είναι το τεκμήριο τυφλότητας." (the interval is the evidence of blinding). §8: harvester and runner refuse to run without a deposited proof file carrying the Zenodo DOI and "το SHA-256 του `184_phase22E_prereg_v1.md` όπως κατατέθηκε" (the SHA-256 of the prereg as deposited).
- (a) anchoring a digest before measurement: **yes** — prereg digest anchored via OTS/Bitcoin before data acquisition; tools enforce the ordering via the deposited SHA-256 gate.
- (b) verifying via block header + explorer receipts: **partial** — block heights recorded and ordered; no block-header bytes or explorer receipt verification procedure described.
- (c) adversarial integrity of an eval pipeline's freeze: **no** — blinding evidence for a linguistics study; no forged-proof/pending controls.
- Verdict: **known** (leg (a) published). Claims-file mapping: known → replication clause; the absent (b)-completeness and (c) legs leave R54-C1's instrument remainder **instrument-new** at most.

### S-B. Zenodo record 22764720 — Phase 22 pre-declaration (same study, earlier phase) — **adjacent**
Receipt: `fetched/zenodo-22764720-phase22-prereg.md` (bytes: `.../files/165_phase22_prereg_v1.md`, accessed 2026-10-30).
Documents: the lock discipline — "Το έγγραφο πρέπει να υπογραφεί και να χρονοσφραγιστεί **πριν** από την πρώτη εκτέλεση του `166`" (the document must be signed and timestamped **before** the first execution of 166); pre-declared verdict table with no positive rounding; signature "Κλειδώθηκε από: Χρήστος Παπανικολάου · 2026-09-14 07:20 EEST"; its own timestamping field is "Χρονοσφράγιδα OSF: ______ (εκκρεμεί)" (OSF timestamp: pending).
- (a) yes in intent (timestamp-before-first-execution), but the mechanism named here is OSF, not a public blockchain.
- (b) no. (c) no.
- Verdict: **adjacent** (prereg lock discipline without the blockchain anchor at this record).

### S-C. IETF Internet-Draft draft-fassbender-scitt-time-anchor-08 — **known**
Receipt: `fetched/ietf-draft-fassbender-scitt-time-anchor-08.md` (accessed 2026-10-30; draft dated 23 Oct 2026, Independent Submission, "In ISE Review" — an I-D, not an RFC).
Documents: profile committing "cryptographic hashes ... to the Bitcoin blockchain via the OpenTimestamps protocol", "independently verifiable by any party with access to independently validated Bitcoin chain data"; §4.1 VERIFY-ANCHOR procedure, §4.2 Verification Independence; motivating example is an AI research lab's model weights + safety evaluations with the regulator's question "How do we know the lab did not register these weights after the safety evaluation was already public -- backdating the claim?", yielding "these model weights existed no later than block height H"; threats §8.1 forged commitment, §8.5 temporal claim inflation, §8.11 "Premature Anchored Status (False Finality)"; Appendix D negative test vectors; and the independence bar: "the reference verifier Umarise publishes obtains block headers from a single block explorer, which under Section 4.1 yields unverifiable rather than valid."
- (a) yes (artifact hash anchored, temporal guarantee "existed no later than block height H"; the example is measurement-adjacent — safety evaluations, not a preregistered measurement run).
- (b) yes — full verification procedure over Bitcoin chain data; single-explorer sourcing explicitly insufficient → direct published support for R54-C1's ≥2-independent-explorer receipts leg.
- (c) adjacent-to-yes — adversarial framing (backdating, false finality, forged commitment) over AI-safety audit artifacts via SCITT receipts; not an eval-lane claims freeze.
- Verdict: **known** (mechanism + adversarial verification published; I-D status noted).

### S-D. arXiv 2606.10625 snaproot — **adjacent**
Receipt: `fetched/arxiv-2606.10625-snaproot.md` (accessed 2026-10-30; arXiv:2606.10625v1 [cs.CR], 09 Jun 2026).
Documents: Solana (not Bitcoin) hash anchoring, positioned against "established hash-anchoring systems (OpenTimestamps, OriginStamp, Chainpoint)"; threat-model assumption "Pre-registration integrity. The registrant performs registration before any adversarial modification of the file"; limitations: "it does not certify the authenticity of pre-registration content, it does not currently defend against frontrunning of unconfirmed registrations".
- (a) partial — anchoring before *adversarial modification* is assumed, not measurement-freeze ordering.
- (b) no (hash recompute + on-chain compare via RPC; no block-header attestation).
- (c) partial — formal threat model names pre-registration manipulation and frontrunning.
- Verdict: **adjacent** (general file integrity; preregistration appears only as a limitation discussion).

### S-E. opentimestamps.org — **known** (mechanism standard)
Receipt: `fetched/opentimestamps.org.md` (accessed 2026-10-30).
Documents: "A timestamp proves that some data existed prior to some point in time. OpenTimestamps defines a set of operations for creating provable timestamps and later independently verifying them." Bitcoin timestamping supported; free calendar servers; stamp/verify workflow.
- (a) general primitive, not research-specific. (b) yes — the verify standard (pending → Bitcoin attestation upgrade). (c) no.
- Verdict: **known** (mechanism).

### S-F. Wikipedia "OpenTimestamps" — **known** (mechanism) / **adjacent** (research use)
Receipt: `fetched/wikipedia-opentimestamps.md` (accessed 2026-10-30).
Documents: "A timestamp is a proof that some data d existed prior to a certain point in time."; upgrade "update[s] the OTS file with the Bitcoin block header attestation"; verification by checking "the transaction merkle root ... equal to the one observed in the blockchain"; use cases listed: "defensive publications and digital multimedia file integrity" — research preregistration not listed.
- (a) no research-specific practice documented. (b) yes (mechanism incl. block header attestation). (c) no.
- Verdict: **known** (mechanism), **adjacent** (research application).

### Failed fetch
- tandfonline "Quantum-resistant timestamping for open science: a non-technical primer" — HTTP 403, no bytes; excluded from verdicts (`fetched/tandfonline-403-failed.md`). Search-snippet-only evidence, not quoted as primary.

## Negative-space finding (what was NOT found)

No fetched source documents the full R54-C1 instrument as one practice: preregistration-digest-before-measurement anchoring **together with** ≥2-independent-explorer header/receipt verification **and** forged/pending-proof adversarial controls over an eval pipeline's freeze. The components are each published (S-A: (a) with block-height ordering; S-C: (b) and (c) adversarial framing; S-E/S-F: mechanism). The absence is bounded to this sweep's queries/fetches (6 fetches; counts above); it is not a proof of worldwide absence.

## Provenance caution (unresolved)

The two Zenodo records share strong stylistic markers with this fleet's practice culture (phase-numbered preregs, pre-declared verdict tables, numbered "lessons"/δίδαγματα, AI-assisted design, OTS→Bitcoin ordering as blinding evidence). Lane greps this round found no prior citation of them (`opentimestamps` absent from `corpus/SOURCES.md`; `22769923|22764720|Knossos|DĀMOS` no matches in the lane). Author name on 22764720 is Χρήστος Παπανικολάου; whether that overlaps this lane's operator identity is **unresolved** here. If same-origin, the records remain external published artifacts (different project, earlier dates) but the "independent prior art" strength drops — the L1 should weigh this before relying on S-A/B as the sole known-practice evidence. [INFERENCE beyond the flagged style observation.]

## Candidate SOURCES-row Gate material (for S2SourcesRows / L1; verified-at 2026-10-30)

| Candidate URL | ≤25-word located quote (verbatim) | Location |
|---|---|---|
| https://zenodo.org/records/22769923 (files/184_phase22E_prereg_v1.md) | "Αναμονή αγκύρωσης σε block του Bitcoin · καταγραφή ύψους block" (wait for anchoring in a Bitcoin block · record block height) | §9 Χρονοσφράγιση — δίδαγμα #19, item 2 |
| https://zenodo.org/records/22764720 (files/165_phase22_prereg_v1.md) | "Το έγγραφο πρέπει να υπογραφεί και να χρονοσφραγιστεί **πριν** από την πρώτη εκτέλεση" | blockquote ΚΑΝΟΝΑΣ ΚΛΕΙΔΩΜΑΤΟΣ |
| https://datatracker.ietf.org/doc/draft-fassbender-scitt-time-anchor/ | "cryptographic hashes are committed to the Bitcoin blockchain via the OpenTimestamps protocol" | Abstract |
| https://opentimestamps.org/ | "A timestamp proves that some data existed prior to some point in time" | §How it Works |
| https://en.wikipedia.org/wiki/OpenTimestamps | "update the OTS file with the Bitcoin block header attestation" | §Timestamp creation |
| https://arxiv.org/html/2606.10625v1 | "The registrant performs registration before any adversarial modification of the file" | §Threat model, Pre-registration integrity |

Verdict for the C1 knowledge entry, in the claims file's vocabulary: known (replication) for the anchor construct; instrument-new remainder for the ≥2-explorer receipts + forged-control pairing.

## Tooling

No tools installed or upgraded this seat (read-only web + file writes in my wave dir). No pacman, no uv, no network writes beyond search/fetch reads. No credentials or secrets used; only public URLs.
