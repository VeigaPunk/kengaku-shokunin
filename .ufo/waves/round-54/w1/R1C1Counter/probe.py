import importlib.util, io, hashlib, tempfile
from pathlib import Path
from opentimestamps.core.timestamp import Timestamp, DetachedTimestampFile
from opentimestamps.core.op import OpSHA256, OpAppend
from opentimestamps.core.notary import BitcoinBlockHeaderAttestation
from opentimestamps.core.serialize import StreamSerializationContext, StreamDeserializationContext
spec = importlib.util.spec_from_file_location('counter', '/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round54_c1_anchor.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
root = Timestamp(hashlib.sha256(b'root').digest())
child = root.ops.add(OpAppend(b'x'))
child.attestations.add(BitcoinBlockHeaderAttestation(900000))
f = io.BytesIO(); DetachedTimestampFile(OpSHA256(), root).serialize(StreamSerializationContext(f))
raw = f.getvalue()
for label, ctx in [('counter-reader', io.BytesIO(raw)), ('context-reader', StreamDeserializationContext(io.BytesIO(raw)))]:
    try:
        dtf = DetachedTimestampFile.deserialize(ctx); print(label, 'OK')
    except Exception as e: print(label, type(e).__name__, str(e))
try: m._collect_digests(root)
except Exception as e: print('valid-tree', type(e).__name__, str(e))
from types import SimpleNamespace
bad = SimpleNamespace(msg=b'z' * 32, ops={}, attestations={BitcoinBlockHeaderAttestation(900000)})
fake = SimpleNamespace(msg=root.msg, ops={OpAppend(b'x'): bad}, attestations=set())
m._UNARY_ALGOS[OpSHA256] = 'sha256'  # diagnostic isolation of the earlier name error
try: print('isolated-unreachable-child', m._collect_digests(fake))
except Exception as e: print('isolated-unreachable-child', type(e).__name__, str(e))
print('isolated-root keys', [type(k).__name__ for k in m._collect_digests(Timestamp(root.msg))])
work = Path(tempfile.mkdtemp(dir='/fast/scratch/hyaku/kengaku-r54/R1C1Counter'))
try:
    count, lines = m._verify_control_cases(work, raw, root.msg.hex(), work)
    print('controls count', count); print('\n'.join(lines))
except Exception as e: print('controls', type(e).__name__, str(e))
print('proof prefix byte5', raw[5], 'header prefix', raw[:12].hex())
