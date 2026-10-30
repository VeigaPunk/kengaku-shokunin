import hashlib, sys
from opentimestamps.core.serialize import BytesDeserializationContext
from opentimestamps.core.timestamp import DetachedTimestampFile
from opentimestamps.core.notary import BitcoinBlockHeaderAttestation
p=sys.argv[1]
d=DetachedTimestampFile.deserialize(BytesDeserializationContext(open(p,'rb').read()))
print('file_digest',d.file_digest.hex())
seen=set(); reachable=set(); bitcoins=[]
def walk(t):
    if id(t) in seen:return
    seen.add(id(t)); reachable.add(t.msg)
    for a in t.attestations:
        print('attestation',type(a).__name__,repr(a))
        if isinstance(a,BitcoinBlockHeaderAttestation): bitcoins.append(a)
    for op,nxt in t.ops.items(): walk(nxt)
walk(d.timestamp)
print('attestation_types',sorted({type(a).__name__ for t in [] for a in t.attestations}) if False else 'listed above')
print('bitcoin_height', [a.height for a in bitcoins])
print('file_digest_reachable',d.file_digest in reachable)
print('reachable_nodes',len(reachable))
