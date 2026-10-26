#!/bin/bash
# Mechanism probe: what each SQLite-version-sensitive case does to the same seeded end state.
# APP must contain main.db + main.db-wal (the encrypted WAL). Prints one line per variant.
set -u
APP=${APP:-/app}
SEED=${SEED:-/seed}
CAP=${CAP:-/cap}
P3=${P3:-python3}
ver=$($P3 -c 'import sqlite3;print(sqlite3.sqlite_version)')
sqlite3 --version | cut -d' ' -f1-2 | sed "s/^/CLI /" | sed "s/^/py=$ver /"

seed() { rm -rf "$APP"; mkdir -p "$APP"; cp "$SEED/main.db" "$APP/main.db"; cp "$SEED/main.db-wal.encrypted" "$APP/main.db-wal"; }
wal() { if [ -e "$APP/main.db-wal" ]; then stat -c%s "$APP/main.db-wal"; else echo GONE; fi; }
xor() { $P3 -c 'import sys;p=sys.argv[1]+"/main.db-wal";d=open(p,"rb").read();open(p,"wb").write(bytes(b^int(sys.argv[2],16) for b in d))' "$APP" "$1"; }
count() { sqlite3 "$APP/main.db" 'SELECT count(*) FROM items ORDER BY id;' 2>&1; }
jsonlen() { if [ -e "$APP/recovered.json" ]; then $P3 -c 'import json,sys;print(len(json.load(open(sys.argv[1]))))' "$APP/recovered.json" 2>&1; else echo NOJSON; fi; }

seed
printf "A plain-rw-read out=%s wal=%s\n" "$(count)" "$(wal)"
seed
printf 'B read-ro count=%s wal=%s\n' "$(sqlite3 "file:$APP/main.db?mode=ro" 'SELECT count(*) FROM items;' 2>&1)" "$(wal)"
seed; xor 43
printf 'C xor-43 count=%s wal=%s msg=%s\n' "$(count)" "$(wal)" "$(sqlite3 "$APP/main.db" 'SELECT count(*) FROM items;' 2>&1 >/dev/null | tr '\n' ' ')"
seed; xor 42
printf 'D xor-42 count=%s wal=%s\n' "$(count)" "$(wal)"
seed; xor 42; sqlite3 "$APP/main.db" 'PRAGMA wal_checkpoint(TRUNCATE);' >/dev/null 2>&1
printf 'E xor-42-checkpoint count=%s wal=%s\n' "$(count)" "$(wal)"
seed; bash "$CAP/solve.sh" >/dev/null 2>&1; rc=$?
printf 'F oracle rc=%s json=%s wal=%s\n' "$rc" "$(jsonlen)" "$(wal)"
seed; sqlite3 "$APP/main.db" 'SELECT count(*) FROM items;' >/dev/null 2>&1; bash "$CAP/solve.sh" >/dev/null 2>&1; rc=$?
printf 'G plain-then-oracle rc=%s json=%s wal=%s\n' "$rc" "$(jsonlen)" "$(wal)"
