# SC4BtcHeader — R54-C1 external-pin scout

**Conclusion: latest-block sha256d derivation agrees across all three explorers at height 973815; the R54-C1 anchor-block check is PENDING because the supplied claims.ots has no BitcoinBlockHeaderAttestation.**

Deliverables:
- `.ufo/waves/round-54/w1/SC4BtcHeader/header-check.md`: full header hex, intermediate SHA256 digests, exact source URLs, UTC fetch times, agreement table, pending-state evidence and limitations.
- `.ufo/waves/round-54/w1/SC4BtcHeader/fetch-log.json`: compact retained explorer receipts and header bytes.

Observed: frozen claims read in full. Correctly deserialized proof contains 4 PendingAttestations, zero BitcoinBlockHeaderAttestations; claims digest matches anchor.json and live claims bytes. Scratch-only upgrade exited 1 (`Failed! Timestamp not complete`); Bob/Alice calendar responses said waiting for 6 confirmations. No C1 block height can yet be read from the supplied proof.

Latest-block fallback: mempool tip height 973815 fetched 2026-10-30T11:25:14Z. Computed reversed double-SHA256 of Blockstream's 80-byte header = `00000000000000000000c4d9520d136813ac60c7ee8807435c19508eba9fa4a4`, matching Mempool, Blockstream and Blockchain.info's independently reported hashes. Blockchain.info's raw-block header is byte-identical. Its JSON reports matching height and header nTime 1793359431.

Scope: data/crypto derivation only; no exported source contract investigated, no LSP needed. No code edits, git mutations, source or claims changes, counter runs, or C1 pass claim. Three public services agree; infrastructure independence and Bitcoin chainwork are not established. The fallback block is not alleged to include the claims digest.

Tooling: reused `/fast/scratch/hyaku/kengaku-r54/l1/venv/otsenv`, opentimestamps-client 0.8.0 / Python opentimestamps library 0.5.0. No installation or update. Initial API/import attempts failed and were corrected; initial `/api/tips` URL returned 404, working `/api/blocks/tip/height` used. Disk guard printed 367.5G free on /fast/scratch/hyaku, then timed out while enumerating top consumers; no heavy pass performed. Scratch was limited to this seat and removed before handoff.

Self-evaluation (1–5): accuracy 4 (pending status time-bound; chainwork outside scope), completeness 4 (requested fallback delivered; actual C1 height unavailable), clarity 4 (full derivation lives in linked detailed report), actionability 4 (L1 must obtain confirmed proof before C1 block check), conciseness 4 (detail intentionally retained for reproducibility). Average 4.0. Main improvement opportunity: apply the same derivation to the actual attestation block once confirmation is available; no pending-proof acceptance is implied. User should agree that fallback math is complete while the C1 block remains pending.
