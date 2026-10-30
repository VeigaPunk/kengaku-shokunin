# SC4BtcHeader — independent external-pin check

## Status and scope

**Conclusion: latest-block sha256d derivation agrees across all three explorers at height 973815; the R54-C1 anchor-block check is PENDING because the supplied claims.ots has no BitcoinBlockHeaderAttestation.**

Axes: derivation correctness, independent-source agreement, complete fetch evidence, honest pending-state reporting. Frozen claims read in full. This is a bounded explorer/header check, not a C1 predicate pass or chain-consensus verification.

## Anchor proof observation

The venv Python library successfully deserialized the supplied `corpus/evidence/round54/anchor/claims.ots` with:

```python
from opentimestamps.core.timestamp import DetachedTimestampFile
from opentimestamps.core.serialize import BytesDeserializationContext
proof = DetachedTimestampFile.deserialize(BytesDeserializationContext(raw))
# Recursively walk proof.timestamp.ops and each timestamp.attestations.
```

Observed root/file digest: `d7aa05c8fcd4aff2ec6f1b606c4e5072d1082b51da8d1c091e2ed1df0d995eb8`, matching sha256 of the current frozen claims bytes and anchor.json. All four attestations were PendingAttestation, with calendar URIs:

- https://finney.calendar.eternitywall.com
- https://btc.calendar.catallaxy.com
- https://bob.btc.calendar.opentimestamps.org
- https://alice.btc.calendar.opentimestamps.org

No Bitcoin attestation height was available. A scratch-copy `ots upgrade claims-probe.ots` probe immediately before the 11:25:14Z tip fetch exited 1, reporting `Failed! Timestamp not complete`. Finney and Catallaxy reported pending; Bob reported transaction `497a0a4f68de3c45b28c9c3608be36b61d55ccae63efe2e30d6d667a9a2d2f7d`, Alice reported transaction `df9559326c633d43e71b56e268112d540c9d11970c66c54b257d057879485f08`, both waiting for 6 confirmations. Those are calendar responses, not independently checked transaction inclusion. The lane proof was never modified.

## Latest-block fallback: sources and fetch times

All successful requests returned HTTP 200. Times below are UTC request-start times, not claimed server receipt times. The initially attempted https://mempool.space/api/tips returned 404 at 2026-10-30T11:23:33Z; the working tip-height endpoint was used instead.

| Source / purpose | Exact URL | Fetched at UTC |
|---|---|---|
| Mempool latest height | https://mempool.space/api/blocks/tip/height | 2026-10-30T11:25:14Z |
| Mempool hash at 973815 | https://mempool.space/api/block-height/973815 | 2026-10-30T11:25:15Z |
| Blockstream hash at 973815 | https://blockstream.info/api/block-height/973815 | 2026-10-30T11:25:15Z |
| Blockstream 80-byte header | https://blockstream.info/api/block/00000000000000000000c4d9520d136813ac60c7ee8807435c19508eba9fa4a4/header | 2026-10-30T11:25:16Z |
| Blockchain.info raw-block hex | https://blockchain.info/rawblock/00000000000000000000c4d9520d136813ac60c7ee8807435c19508eba9fa4a4?format=hex | 2026-10-30T11:25:16Z |
| Blockchain.info independently reported hash/height/time | https://blockchain.info/rawblock/00000000000000000000c4d9520d136813ac60c7ee8807435c19508eba9fa4a4 | 2026-10-30T11:26:31Z |

The raw-block hex response contained 3,279,494 characters; its first 160 hex characters were byte-identical to Blockstream's header. Only header and compact fetch metadata are retained in `fetch-log.json`; no full block payload is retained. Latest means the tip returned at the stated fetch time, not a permanent tip assertion.

## Header and derivation

Header hex (160 characters = 80 bytes):

```text
00600220ae9344d4e5884c4aa10fb3063c14754eee9cc102c38f0100000000000000000018eb96cbf6e83d5606bfcbac7e5b7c45dfef0f39ff867aa1ddbc2fb8d6d92d0b477ee46aace501177774d25c
```

Derived directly with Python hashlib, not by comparing strings supplied by explorers:

```python
header = bytes.fromhex(header_hex)
assert len(header) == 80
first = hashlib.sha256(header).digest()
second = hashlib.sha256(first).digest()
display_hash = second[::-1].hex()
```

| Derivation stage | Result |
|---|---|
| sha256(header), raw digest hex | `44623b12127f9f17039ec89dc3071a50801c0aef568a339097aba6511e40977e` |
| sha256(sha256(header)), raw digest hex | `a4a49fba8e50195c430788eec760ac1368130d52d9c400000000000000000000` |
| Display hash: reverse second digest bytes | `00000000000000000000c4d9520d136813ac60c7ee8807435c19508eba9fa4a4` |

The nTime field, bytes 68:72 interpreted little-endian, is 1793359431 = 2026-10-30T11:23:51Z. Blockchain.info JSON independently reports the same time and height 973815. Nonce = 1557296247; nBits = `1701e5ac`.

## Agreement table

Let D = `00000000000000000000c4d9520d136813ac60c7ee8807435c19508eba9fa4a4`.

| Source/check | Reported / derived hash | Agreement with independently computed D |
|---|---|---|
| Mempool block-height response | D (full value retained in fetch-log.json) | MATCH |
| Blockstream block-height response | D (full value retained in fetch-log.json) | MATCH |
| Blockchain.info JSON `hash` | D (full value retained in fetch-log.json) | MATCH |
| Blockchain.info raw-block first 80 bytes, double-sha256/reversed | D | MATCH; header also byte-identical to Blockstream |

## Confidence and remaining unknowns

High confidence in this header/hash derivation and three-source agreement: two independent header byte fetches yield the same 80 bytes, and three sources report its computed hash. No chainwork, PoW, or explorer-operator-independence audit was performed. Source diversity is domain/service diversity, not proven infrastructure independence. No semantic source-code contract was investigated; LSP was not needed for this data/cryptographic check.

The actual C1 attestation height and its relation to a Bitcoin header remain unavailable in the supplied pending proof. This fallback header is NOT presented as the C1 anchor header, nor as evidence that the claims digest is included in block 973815. Confirmation availability can change after these observations.
