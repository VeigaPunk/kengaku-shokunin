# SC2OtsDocs — round 54 C1 source scout

Completed six source blocks in `.ufo/waves/round-54/w1/SC2OtsDocs/rows-material.md`, each with exact URLs, access date 2026-10-30, ≤25-word quote, saved-file location, C1 teaching, and prior-art boundaries. Eight fetched receipts and byte-size/SHA256 provenance are under `.ufo/waves/round-54/w1/SC2OtsDocs/fetched/`; inventory: `fetched/manifest.json`.

## Findings (high confidence, source-observed)
- OpenTimestamps homepage, How it Works: timestamping demonstrates prior existence, not correctness or authorship.
- `opentimestamps-client/README.md`, Usage: new stamps may remain pending; calendars supply missing Bitcoin-header paths. Requirements explicitly distinguishes creation without a node from CLI verification with Bitcoin Core.
- `python-opentimestamps/README.md`, Structure: core modules are consensus-critical validation dependencies.
- `opentimestamps/core/notary.py:237–300`, `BitcoinBlockHeaderAttestation`: commitment is the block-header merkle root; height enables external lookup. `verify_against_blockheader` compares a 32-byte digest to the root and returns nTime; that alone is not chain-membership or proof-of-work validation.
- Bitcoin developer reference, Block Headers table: 80-byte serialization; 4-byte version, 32-byte previous hash, then 32-byte merkle root. Derived arithmetic: root occupies zero-based bytes 36–67, i.e. `header[36:68]`. This is an explicitly labeled derivation, not a quoted numeric offset.
- Bitcoin Wiki: double-SHA256 header hashing and byte-order caution independently reinforce C1's header/hash comparison.

## Limits / remaining unknowns
These sources establish existing mechanisms, not novelty of the specific preregistration workflow. Neither upstream commit versions nor equivalence to installed opentimestamps-client 0.8.0 were established; saved byte hashes provide local provenance. Round-specific anchor correctness, explorer independence, chain trust, and score admission were outside this source-fetch assignment and were not tested. LSP was unavailable in this seat's inventory; source observations are literal inspection, not a semantic caller trace.

The initial unqualified `master/core/notary.py` raw URL returned HTTP 404 / curl exit 22. The correct `master/opentimestamps/core/notary.py` returned HTTP 200 and was opened. No login wall encountered. No tools installed/updated, no git/jj mutation, no live-lane production edits, no child dispatch, and no scratch directory or clone created; therefore no scratch remained to remove. Network requests were public GETs for source documents, not uploads. No counter/build/test run was performed.

## Self-evaluation
Accuracy 4/5: located source evidence; upstream live-master versions remain unpinned. Completeness 5/5: six blocks exceed four required, including README and attestation docstring plus independent header reference. Clarity 4/5: byte-offset arithmetic is separate from quotes, but table-cell quotation requires markup normalization. Actionability 4/5: directly usable row material, with integration/IDs intentionally left to L1. Conciseness 4/5: supplemental wiki block adds overlap but preserves independent byte-order guidance. Overall 4.2/5. Highest-impact improvement outside this brief: pin upstream commits before asserting version-specific library behavior. User-agreement self-check: evidence and unverified boundaries are explicit.

Report: .ufo/waves/round-54/w1/SC2OtsDocs.md
