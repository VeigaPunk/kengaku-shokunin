#!/usr/bin/env python3
"""Independent ground truth: derive the expected rows from the two captures, not from the probe's TRUTH."""
import hashlib
import json
import pathlib
import shutil
import sqlite3
import sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r40/F40IndepProbe")
CAP = S / "lane/corpus/evidence/round40/tb2-db-wal-recovery"
gt = S / "gt"
shutil.rmtree(gt, ignore_errors=True)
gt.mkdir(parents=True)

base_only = gt / "base"
base_only.mkdir()
shutil.copyfile(CAP / "main.db", base_only / "main.db")


def rows_at(db):
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        return [{"id": a, "name": b, "value": v}
                for a, b, v in con.execute("SELECT id, name, value FROM items ORDER BY id")]
    finally:
        con.close()


print("base-only rows:", json.dumps(rows_at(base_only / "main.db")))
print("base-only digest:", hashlib.sha256(json.dumps(rows_at(base_only / "main.db")).encode()).hexdigest())

for key in (0x42, 0x43):
    d = gt / f"k{key:02x}"
    d.mkdir()
    shutil.copyfile(CAP / "main.db", d / "main.db")
    enc = (CAP / "main.db-wal.encrypted").read_bytes()
    wal = bytes(b ^ key for b in enc)
    (d / "main.db-wal").write_bytes(wal)
    print(f"key {key:#04x} wal size={len(wal)} sha256={hashlib.sha256(wal).hexdigest()} head={wal[:4].hex()}")
    try:
        rows = rows_at(d / "main.db")
        print(f"  ro rows={len(rows)} ids={[r['id'] for r in rows]} values={[r['value'] for r in rows]}")
        print(f"  11row-digest={hashlib.sha256(json.dumps(rows).encode()).hexdigest()}")
    except Exception as e:
        print(f"  ro read failed: {type(e).__name__}: {e}")
        rwwal = d / "main.db-wal"
        print(f"  wal still present={rwwal.is_file()} size={rwwal.stat().st_size if rwwal.is_file() else 0}")

print("capture digests:", {n: hashlib.sha256((CAP / n).read_bytes()).hexdigest()
                           for n in ("main.db", "main.db-wal.encrypted")})
sys.exit(0)
