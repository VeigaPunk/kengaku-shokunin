#!/usr/bin/env python3
"""Is the 'decrypt in place + read-only extract' shape unique? Test alternate non-destructive URIs."""
import hashlib
import pathlib
import shutil
import sqlite3

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r40/F40IndepProbe")
src = S / "gt/k42"
if not (src / "main.db-wal").is_file():
    raise SystemExit("run gt.py first")

URIS = ["file:{d}/main.db?immutable=1", "file:{d}/main.db?mode=ro&immutable=1", "file:{d}/main.db?mode=ro"]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "ABSENT"


for i, uri in enumerate(URIS):
    d = S / f"gt/imm{i}"
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(src, d)
    (d / "main.db-shm").unlink(missing_ok=True)  # residue of the gt.py read, not of this test
    pre = sorted(p.name for p in d.iterdir())
    before = (sha(d / "main.db"), sha(d / "main.db-wal"))
    try:
        con = sqlite3.connect(uri.format(d=d), uri=True)
        rows = list(con.execute("SELECT id, name, value FROM items ORDER BY id"))
        con.close()
        verdict = f"rows={len(rows)} ids={[r[0] for r in rows]}"
    except Exception as e:
        verdict = f"ERROR {type(e).__name__}: {e}"
    after = (sha(d / "main.db"), sha(d / "main.db-wal"))
    extra = sorted(p.name for p in d.iterdir() if p.name not in pre)
    print(f"{uri.format(d='<d>')}: {verdict}")
    print(f"  pre={pre} created={extra}")
    print(f"  wal_before={before[1][:16]} wal_after={after[1][:16]} db_unchanged={before[0] == after[0]}"
          f" wal_unchanged={before[1] == after[1]} extra={extra}")
