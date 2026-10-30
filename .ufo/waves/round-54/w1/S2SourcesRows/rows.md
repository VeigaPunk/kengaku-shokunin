# R54-C1 SOURCES row proposal — S2SourcesRows

Axes: calibration and provenance fidelity; round axes are novelty and calibration. These are six draft rows, not integrated registry entries. TBD-S198 through TBD-S203 are placeholders; L1 assigns final ids. Proposed `mined` status and `used-by` apply only with simultaneous integration of `corpus/knowledge/external-anchor-freeze.md` citing each row. The knowledge draft is `.ufo/waves/round-54/w1/S1KnowledgeEntry/external-anchor-freeze.md`; no production-entry existence or admission is asserted here.

All canonical sources were opened by this seat on 2026-10-30, including the Zenodo file and the saved core source excerpt. Saved-byte paths below are lane-relative. SC2 receipts are raw fetched content; the SC1 Zenodo receipt is an attributed excerpt/translation receipt, not a complete raw-file capture. Live branch/site snapshots are identified by access date and saved-byte hashes rather than invented upstream commit revisions.

## Candidate registry rows

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| TBD-S198 | OpenTimestamps: a timestamping proof standard — https://opentimestamps.org/ | docs | A | the project's own description of existence-before-time proofs | How it Works, saved HTML lines 210-215, quote line 212; unversioned snapshot accessed 2026-10-30; sha256 6cf02d9234d0c400655026a1d991c1eecc3b2c93b34297af70a1a19a4d5fc66b | A timestamp establishes existence before a time, not truth or scientific validity of the stamped claims. | mined | 2026-10-30 | 180d | corpus/knowledge/external-anchor-freeze.md |
| TBD-S199 | OpenTimestamps Client README — https://github.com/opentimestamps/opentimestamps-client | docs | A | the official client's documented pending and upgrade lifecycle | README Usage lines 45-50 and 82-87; master snapshot accessed 2026-10-30; sha256 c1a65e8443d5bef6774274ae40ab4e3d16144be394c1508c47f29bf71538b116 | Stamping is not Bitcoin confirmation; upgrade adds the Bitcoin commitment path to an incomplete proof. | mined | 2026-10-30 | on-release | corpus/knowledge/external-anchor-freeze.md |
| TBD-S200 | python-opentimestamps attestation documentation — https://github.com/opentimestamps/python-opentimestamps | docs | A | BitcoinBlockHeaderAttestation's documented digest and header-binding semantics | opentimestamps/core/notary.py class docstring lines 237-266, quote line 240; master snapshot accessed 2026-10-30; sha256 62111f56d553b5c074be6ba26a5defd6466b21fc6d5eca245767239843cd43f6 | The attested digest must match the block header merkle root; finding an attestation object alone is insufficient. | mined | 2026-10-30 | on-release | corpus/knowledge/external-anchor-freeze.md |
| TBD-S201 | Block hashing algorithm — https://en.bitcoin.it/wiki/Block_hashing_algorithm | docs | B | the expert wiki's worked header-hashing explanation | Main text before Endianess, saved HTML line 113; oldid=68439 in footer line 199; accessed 2026-10-30; sha256 df1016fe6f2f5ecdaacccda18111e51b8037f3b000ed8df7eb8757b3be9af018 | Double-SHA256 header hashing requires explicit byte-order treatment when compared with displayed block hashes. | mined | 2026-10-30 | 180d | corpus/knowledge/external-anchor-freeze.md |
| TBD-S202 | Bitcoin Developer Reference: Block Chain — https://developer.bitcoin.org/reference/block_chain.html | docs | A | the reference's serialized block-header field layout | Block Headers heading line 208, sentence line 209, merkle-root table cells lines 235-237; unversioned snapshot accessed 2026-10-30; sha256 aacf6086578728ff50fe6c2030d0cbd5eaaf3d6b3ea0ad371f13ae7bf2fb2cb6 | The table independently grounds the derived merkle-root slice header[36:68] in an 80-byte header; offsets are arithmetic, not a verbatim source statement. | mined | 2026-10-30 | on-release | corpus/knowledge/external-anchor-freeze.md |
| TBD-S203 | Phase 22.E pre-declaration v1: Linear A / Knossos scope criterion — https://zenodo.org/records/22769923 | docs | A | this deposited protocol's stated Bitcoin-anchored preregistration sequence, not proof it was executed | 184_phase22E_prereg_v1.md dated 15 September 2026, section 9 Timestamping — lesson 19, ordered steps 1-4; accessed 2026-10-30; status line NOT LOCKED, thresholds pending | A published protocol already specifies stamping a preregistration and waiting for Bitcoin anchoring before acquisition; published procedure is not evidence of completed execution. | mined | 2026-10-30 | 180d | corpus/knowledge/external-anchor-freeze.md |

## Gate material

Each block supplies one located quote of at most 25 words. The quoted strings are contiguous source excerpts; line-wrap joins are normalized to spaces. No novelty score or C1 counter outcome is judged here.

### TBD-S198
- URL: https://opentimestamps.org/
- Access date: 2026-10-30.
- Quote: “A timestamp proves that some data existed prior to some point in time.”
- Location: How it Works, saved HTML line 212, heading line 210.
- Fetched bytes: `.ufo/waves/round-54/w1/SC2OtsDocs/fetched/opentimestamps.org.html`; checksum in row anchor and SC2 manifest.
- Verdict: **known** timestamping mechanism. This page alone does not establish novelty of a measurement-preregistration application.

### TBD-S199
- URL: https://github.com/opentimestamps/opentimestamps-client
- Raw URL: https://raw.githubusercontent.com/opentimestamps/opentimestamps-client/master/README.md
- Access date: 2026-10-30.
- Quote: “You can also upgrade an incomplete timestamp, which adds the path to the Bitcoin blockchain to the timestamp itself”
- Location: README Usage, saved lines 82-83.
- Fetched bytes: `.ufo/waves/round-54/w1/SC2OtsDocs/fetched/ots-client-README.md`.
- Verdict: **known** client lifecycle, including Git/file timestamping in the introduction. Requirements lines 13-14 describe local Bitcoin Core verification; this is not evidence C1 ran that full-node CLI verification.

### TBD-S200
- URL: https://github.com/opentimestamps/python-opentimestamps
- Source URL: https://raw.githubusercontent.com/opentimestamps/python-opentimestamps/master/opentimestamps/core/notary.py
- Access date: 2026-10-30.
- Quote: “The commitment digest will be the merkleroot of the blockheader.”
- Location: BitcoinBlockHeaderAttestation docstring, saved line 240; class line 237.
- Fetched bytes: `.ufo/waves/round-54/w1/SC2OtsDocs/fetched/pyots-core-notary.py`; repository README also opened at `.ufo/waves/round-54/w1/SC2OtsDocs/fetched/pyots-README.md`, Structure lines 13-18.
- Verdict: **known** attestation/header binding. Root matching alone does not demonstrate chain membership or proof-of-work; no library execution is claimed.

### TBD-S201
- URL: https://en.bitcoin.it/wiki/Block_hashing_algorithm
- Access date: 2026-10-30.
- Quote: “Bitcoin uses: SHA256(SHA256(Block_Header)) but you have to be careful about byte-order.”
- Location: main article immediately before Python example, saved HTML line 113; revision oldid=68439.
- Fetched bytes: `.ufo/waves/round-54/w1/SC2OtsDocs/fetched/bitcoinwiki-block-hashing-algorithm.html`.
- Verdict: **known** header hashing; tier B supplemental expert documentation, not sole support.

### TBD-S202
- URL: https://developer.bitcoin.org/reference/block_chain.html#block-headers
- Access date: 2026-10-30.
- Quote: “Block headers are serialized in the 80-byte format described below”
- Location: Block Headers, saved HTML line 209; table merkle-root cells lines 235-237.
- Fetched bytes: `.ufo/waves/round-54/w1/SC2OtsDocs/fetched/developer-bitcoin-block_chain.html`.
- Verdict: **known** header layout. Slice 36:68 derives from preceding 4-byte and 32-byte fields. Header time is miner-reported with consensus bounds, not an exact trusted creation timestamp. This documentation is not a block-explorer receipt.

### TBD-S203
- URL: https://zenodo.org/records/22769923
- Opened file URL: https://zenodo.org/records/22769923/files/184_phase22E_prereg_v1.md
- Access date: 2026-10-30.
- Quote: “Αναμονή αγκύρωσης σε block του Bitcoin · καταγραφή ύψους block”
- Location: section 9, “Χρονοσφράγιση — δίδαγμα #19”, ordered step 2; SC1 receipt lines 12-19. Translation, not an additional source quote: wait for Bitcoin-block anchoring and record block height. Step 1 specifies preregistration deposit plus ots stamp; step 3 places acquisition afterwards.
- Scout receipt: `.ufo/waves/round-54/w1/SC1PriorArt/fetched/zenodo-22769923-phase22E-prereg.md`; original file independently opened by S2SourcesRows.
- Verdict: **known** published preregistration/Bitcoin-anchor ordering, directly relevant to the frozen replication-pricing rule. Scope limit: the source itself says NOT LOCKED, thresholds pending; no completed anchor, execution, historical deposit date verification, or validated scientific result is asserted.

## Integration and provenance limits

The first five rows consolidate SC2OtsDocs material; the sixth uses SC1PriorArt's discovered protocol. Earlier directory scans found SC1's fetched directory empty; subsequent discovery found these receipts. An earlier empty listing is not evidence of whole-round absence. No global deduplication, source census, table parser, or counter was run by this seat. Reviewer R3KnowledgeSources-2 owns the requested 11-column check including TBD placeholders. L1 must assign ids and integrate every cited used-by reference together; do not present this draft's proposed mined rows as already admitted. Canonical Rust judgment, score assignment, and C1/C2 execution remain outside this scribe's scope.

Q26 admission prerequisite from reviewer R3KnowledgeSources-2: the row-anchor digests presently identify wave-directory captures only. Before admission, L1 must migrate the cited captures to committed corpus/evidence paths (or a committed SHA256SUMS inventory), preserve matching bytes and hashes in the same integration commit, and update Gate evidence paths accordingly. Otherwise remove digest tokens from proposed row anchors until that evidence is integrated. This scribe has not performed or verified that migration.
