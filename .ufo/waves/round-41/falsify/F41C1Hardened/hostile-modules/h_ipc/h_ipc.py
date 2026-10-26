"""Hostile battery module (repair b): SysV IPC crosses the build sandbox into every tool run.

The build child seeds a SysV shared-memory segment under a fixed key; the fixture's committed probe, run by
`plans/tip_receipts.py` inside the tool sandbox, looks that key up. The DEPLOYED counter neither unshares the
IPC namespace for the build child nor for the tool runs, so both live in the host IPC namespace and the
segment is shared: any fixture can hand state to, or read state from, any other sandbox (and the host).
The repaired counter passes `--unshare-ipc` to every sandbox, so the segment dies with the build namespace.

The receipt holds the "visible" output, so the fixture is green on the deployed counter and WRONG on the
repaired one. The segment is created 0666 so the child gets no privilege hint; nothing is written to disk.
"""

EV = "corpus/evidence/r/ipc-probe.txt"
KEY = "0x46343133"  # 'F413' — private to this demo module

SEED = '''import ctypes

libc = ctypes.CDLL("libc.so.6", use_errno=True)
libc.shmget.argtypes = [ctypes.c_int, ctypes.c_size_t, ctypes.c_int]
libc.shmget.restype = ctypes.c_int
libc.shmat.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
libc.shmat.restype = ctypes.c_void_p
sid = libc.shmget(KEYV, 64, 0o1666)
if sid >= 0:
    ctypes.memmove(libc.shmat(sid, None, 0), b"MARK", 4)
'''

PROBE = '''"""Fixture probe: is the build sandbox's SysV segment reachable from this run?

  python3 plans/ipc_probe.py --lane .
"""
import ctypes
import sys

libc = ctypes.CDLL("libc.so.6", use_errno=True)
libc.shmget.argtypes = [ctypes.c_int, ctypes.c_size_t, ctypes.c_int]
libc.shmget.restype = ctypes.c_int
libc.shmat.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
libc.shmat.restype = ctypes.c_void_p
sid = libc.shmget(KEYV, 64, 0)
seen = sid >= 0 and ctypes.string_at(libc.shmat(sid, None, 0), 4) == b"MARK"
sys.stdout.write("IPC " + ("visible" if seen else "hidden") + "\\n")
'''


def lane(ctx, d, files):
    root = ctx.init(d / "lane")
    base = {
        "README.md": "# hostile fixture lane\n",
        "SKILL.md": "# fixture skill\n",
        "corpus/README.md": "# fixture lane receipts\n",
        "corpus/knowledge/fixture.md": "# fixture knowledge note\n",
    }
    base.update(files)
    for rel in sorted(base):
        ctx.write(root / rel, base[rel])
    ctx.git(root, "add", "-A")
    ctx.git(root, "commit", "-q", "-m", "fixture lane")
    return root


def b_ipc(ctx, d):
    ctx.sh("/usr/bin/python3", "-c", SEED.replace("KEYV", KEY))
    root = lane(ctx, d, {EV: "IPC visible\n",
                         "plans/ipc_probe.py": PROBE.replace("KEYV", KEY)})
    return ["--lane", str(root), "--work", "{WORK}"]


FIXTURES = [
    {"fid": "h_ipc-build-segment-visible", "tool": "receipts", "expect": "accept",
     "defects": [f"equal:{EV}", "control:differ"], "build": b_ipc},
]
