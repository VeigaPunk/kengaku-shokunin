# Round 54 C1 — opened primary-source material

Access date for every block: **2026-10-30**. Axes: source fidelity, C1 applicability, provenance completeness; no production changes. Tier labels below are candidates, not admission decisions. Quotes are each ≤25 words. Locations refer to saved bytes, not inferred GitHub line numbers. Receipt paths are relative to this directory; exact byte sizes and SHA256 hashes are in `fetched/manifest.json`.

## 1. OpenTimestamps project homepage — tier A candidate
- URL: https://opentimestamps.org/
- Access date: 2026-10-30
- Quote: “A timestamp proves that some data existed prior to some point in time.”
- Location: How it Works, HTML lines 210–215; quote at line 212.
- Fetched receipt: `fetched/opentimestamps.org.html` (25,055 bytes).
- Observed: the following sentences describe operations for independently verifying timestamps and Bitcoin blockchain support.
- Teaches for C1: anchors existence-before-time of the claims bytes, not their truth, authorship, or scientific validity. The mechanism is documented public practice; this source alone does not establish novelty of a preregistration application.
- Prior-art material: known timestamping mechanism; a lane-specific instrument may apply it, but no novelty score is adjudicated here.

## 2. OpenTimestamps CLI README — tier A candidate
- URL: https://github.com/opentimestamps/opentimestamps-client
- README URL: https://github.com/opentimestamps/opentimestamps-client/blob/master/README.md
- Fetched raw URL: https://raw.githubusercontent.com/opentimestamps/opentimestamps-client/master/README.md
- Access date: 2026-10-30
- Quote: “Command-line tool to create and validate timestamp proofs with the OpenTimestamps protocol, using the Bitcoin blockchain as a timestamp notary.”
- Location: README opening paragraph, lines 3–4 (line wrap normalized to a space).
- Fetched receipts: `fetched/ots-client-README.md` (8,111 bytes); repository landing page `fetched/github-opentimestamps-client.html` (275,993 bytes).
- Observed: Usage lines 40–50 distinguish newly stamped, pending proofs from Bitcoin-confirmed ones; lines 66–67 explain that remote calendars supply the missing path to a Bitcoin header. Requirements lines 13–14 say the CLI requires a local Bitcoin Core node for verification.
- Teaches for C1: stamping is not confirmation. A pending-only `.ots` cannot satisfy the frozen Bitcoin-attestation requirement. C1's bespoke header/explorer check should not be described as having run the CLI's full-node verification unless separately exercised.
- Prior-art material: known Bitcoin timestamp proofs and Git-commit/file timestamping (opening lines 5–7); this is not evidence that the lane invented timestamped Git artifacts.

## 3. Python OpenTimestamps README — tier A candidate
- URL: https://github.com/opentimestamps/python-opentimestamps
- README URL: https://github.com/opentimestamps/python-opentimestamps/blob/master/README.md
- Fetched raw URL: https://raw.githubusercontent.com/opentimestamps/python-opentimestamps/master/README.md
- Access date: 2026-10-30
- Quote: “Python3 library for creating and verifying OpenTimestamps proofs.”
- Location: README introduction, line 3.
- Fetched receipts: `fetched/pyots-README.md` (953 bytes); repository landing page `fetched/github-python-opentimestamps.html` (228,336 bytes).
- Observed: Structure, lines 13–18, distinguishes consensus-critical core modules and warns that incompatible changes can cause inconsistent validation results.
- Teaches for C1: the proof parser and attestation types come from an existing verification library; preserve version provenance and distinguish this dependency from the counter's independent op-tree recomputation.
- Prior-art material: known library and core-validation boundary, not novel proof machinery.

## 4. BitcoinBlockHeaderAttestation source docstring — tier A candidate
- URL: https://github.com/opentimestamps/python-opentimestamps/blob/master/opentimestamps/core/notary.py
- Fetched raw URL: https://raw.githubusercontent.com/opentimestamps/python-opentimestamps/master/opentimestamps/core/notary.py
- Access date: 2026-10-30
- Quote: “The commitment digest will be the merkleroot of the blockheader.”
- Location: `opentimestamps/core/notary.py`, `BitcoinBlockHeaderAttestation` docstring, line 240; class begins line 237.
- Fetched receipt: `fetched/pyots-core-notary.py` (12,947 bytes).
- Observed: docstring lines 242–253 records height for external header lookup and calls for root matching and header-time extraction. `verify_against_blockheader`, lines 289–300, rejects non-32-byte digests and root mismatches, then returns `block_header.nTime`.
- Teaches for C1: bind the op-tree output to the header's merkle root at the attested height. Merely finding an attestation object is insufficient. This method itself does not demonstrate proof-of-work, chain membership, or an independently trusted header source; those are separate trust/verification requirements.
- Prior-art material: known attestation/header-binding design. This scout did not execute the library or verify the round's anchor.

## 5. Bitcoin developer reference — independent of OpenTimestamps
- URL: https://developer.bitcoin.org/reference/block_chain.html
- Section URL: https://developer.bitcoin.org/reference/block_chain.html#block-headers
- Access date: 2026-10-30
- Quote (contiguous table cells, markup removed): “32 merkle root hash char[32]”
- Location: Block Headers table, third data row, HTML lines 235–237. The 80-byte format is stated at line 209; preceding rows list 4-byte version (225–229) and 32-byte previous header hash (230–234).
- Fetched receipt: `fetched/developer-bitcoin-block_chain.html` (31,319 bytes).
- Observed: the merkle root is a 32-byte header field after 4 + 32 bytes. Merkle Trees, lines 284–295, explains ordered TXIDs, repeated double-SHA256 pairing, odd-leaf duplication, and internal byte order.
- Derived location (arithmetic, not a verbatim offset quote): zero-based bytes **36–67 inclusive**, Python slice **`header[36:68]`**, in the **80-byte** serialized header. The table does not explicitly print the offset 36.
- Teaches for C1: independently grounds the frozen counter's root slice and raw/internal byte-order handling. The table's time description (line 243) also cautions that nTime is miner-reported with consensus bounds, not an exact trusted wall-clock creation time.
- Prior-art material: known Bitcoin header/merkle construction; independent documentation, not an independent explorer receipt for this round's block.

## 6. Bitcoin Wiki — supplemental independent explanation
- URL: https://en.bitcoin.it/wiki/Block_hashing_algorithm
- Access date: 2026-10-30
- Quote: “Bitcoin uses: SHA256(SHA256(Block_Header)) but you have to be careful about byte-order.”
- Location: main article text immediately before the Python example, saved HTML line 113.
- Fetched receipt: `fetched/bitcoinwiki-block-hashing-algorithm.html` (29,285 bytes).
- Observed: header field table lines 55–108 places `hashMerkleRoot` after Version and hashPrevBlock; lines 109–114 explain indirect transaction commitment through the root and header double hashing.
- Teaches for C1: header digest and explorer-rendered block hash require explicit byte-order treatment. A plausible hex string is not evidence of correct comparison.
- Prior-art material: known block hashing algorithm. The developer reference above supplies the clearer 80-byte layout evidence.

## Boundaries and provenance

All eight successful receipts are public, unauthenticated GET responses; no login wall encountered. The first attempted notary URL, `https://raw.githubusercontent.com/opentimestamps/python-opentimestamps/master/core/notary.py`, returned HTTP 404 (curl exit 22); corrected package-qualified URL above returned HTTP 200 / 12,947 bytes. No failed response is presented as source evidence. No package/tool installation, repository mutation, anchor verification, source-row integration, or scratch clone occurred. These are live `master` URLs, not commit-pinned upstream versions; hashes preserve the fetched bytes.

LSP was not exposed in this seat's tool inventory. Class/method observations above are literal source inspection, not semantic references/implementation proof; no exported contract was changed and no caller-completeness claim is made.

Report: .ufo/waves/round-54/w1/SC2OtsDocs.md
