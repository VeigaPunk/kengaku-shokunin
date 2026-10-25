#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")/../../.." && pwd)
W=/tmp/r11-mut
rm -rf "$W"; mkdir -p "$W"
cd "$ROOT"
BASE_STATUS="$W/status.before"
git status --porcelain > "$BASE_STATUS"
FILES="grader.py corpus/evidence/round8-horizon/results.jsonl corpus/evidence/round8-horizon/run.log corpus/evidence/round9-replication/results-r9.jsonl corpus/evidence/round9-replication/replication.md corpus/evidence/round11-power/results-r11.jsonl corpus/evidence/round11-power/run.log corpus/evidence/round11-power/analysis_r11.md corpus/evidence/round11-power/ordering.log corpus/evidence/round11-power/prereg-bundle.sha256 corpus/evidence/round11-power/power_analysis_r11.md corpus/evidence/round11-power/predictions-r11.md corpus/evidence/round11-power/probe_plan_r11.md"
md5sum $FILES > "$W/md5.before"
cp corpus/evidence/round8-horizon/results.jsonl "$W/r8.jsonl"
cp corpus/evidence/round8-horizon/run.log "$W/r8.log"
cp corpus/evidence/round9-replication/results-r9.jsonl "$W/r9.jsonl"
cp corpus/evidence/round9-replication/replication.md "$W/r9.md"
cp corpus/evidence/round11-power/results-r11.jsonl "$W/r11.jsonl"
cp corpus/evidence/round11-power/analysis_r11.md "$W/r11.md"
cp corpus/evidence/round11-power/run.log "$W/r11.log"
run() { label=$1; shift; set +e; "$@" >"$W/$label.out" 2>&1; rc=$?; set -e; echo "$rc" > "$W/$label.rc"; }
# M0 clean copies of all seven inputs.
run M0 python3 grader.py --r8-jsonl "$W/r8.jsonl" --r8-runlog "$W/r8.log" --r9-jsonl "$W/r9.jsonl" --r9-md "$W/r9.md" --r11-jsonl "$W/r11.jsonl" --r11-md "$W/r11.md" --r11-runlog "$W/r11.log"
# Dynamic mutations are confined to /tmp copies.
python3 - "$W/r11.jsonl" "$W/m1.jsonl" <<'PY'
import json,sys
src,dst=sys.argv[1:]; done=False
with open(src) as f,open(dst,'w') as o:
 for line in f:
  r=json.loads(line)
  if not done and r.get('cell')=='A-CKPT710' and r.get('ok') is True:
   r['ok']=False; done=True; line=json.dumps(r,separators=(',',':'))+'\n'
  o.write(line)
assert done
PY
run M1 python3 grader.py --r8-jsonl "$W/r8.jsonl" --r8-runlog "$W/r8.log" --r9-jsonl "$W/r9.jsonl" --r9-md "$W/r9.md" --r11-jsonl "$W/m1.jsonl" --r11-md "$W/r11.md" --r11-runlog "$W/r11.log"
python3 - "$W/r11.jsonl" "$W/m2.jsonl" <<'PY'
import json,sys
src,dst=sys.argv[1:]; done=False
with open(src) as f,open(dst,'w') as o:
 for line in f:
  r=json.loads(line)
  if not done and r.get('cell')=='A-CKPT710' and 'nwrong' in r:
   r['nwrong']+=1; done=True; line=json.dumps(r,separators=(',',':'))+'\n'
  o.write(line)
assert done
PY
run M2 python3 grader.py --r8-jsonl "$W/r8.jsonl" --r8-runlog "$W/r8.log" --r9-jsonl "$W/r9.jsonl" --r9-md "$W/r9.md" --r11-jsonl "$W/m2.jsonl" --r11-md "$W/r11.md" --r11-runlog "$W/r11.log"
python3 - "$W/r11.md" "$W/m3.md" <<'PY'
import sys
s=open(sys.argv[1]).read(); old='PREREGISTERED VERDICT: ESTABLISHED'; assert s.count(old)==1
open(sys.argv[2],'w').write(s.replace(old,'PREREGISTERED VERDICT: DIRECTIONAL',1))
PY
run M3 python3 grader.py --r8-jsonl "$W/r8.jsonl" --r8-runlog "$W/r8.log" --r9-jsonl "$W/r9.jsonl" --r9-md "$W/r9.md" --r11-jsonl "$W/r11.jsonl" --r11-md "$W/m3.md" --r11-runlog "$W/r11.log"
python3 - "$W/r11.md" "$W/m4.md" <<'PY'
import sys
s=open(sys.argv[1]).read(); old='): +0.352 sd'; assert s.count(old)==1
open(sys.argv[2],'w').write(s.replace(old,'): +0.452 sd',1))
PY
run M4 python3 grader.py --r8-jsonl "$W/r8.jsonl" --r8-runlog "$W/r8.log" --r9-jsonl "$W/r9.jsonl" --r9-md "$W/r9.md" --r11-jsonl "$W/r11.jsonl" --r11-md "$W/m4.md" --r11-runlog "$W/r11.log"
python3 - "$W/r11.md" "$W/m5.md" <<'PY'
import sys
s=open(sys.argv[1]).read(); old='Brier score (3 probabilistic predictions): 0.153'; assert s.count(old)==1
open(sys.argv[2],'w').write(s.replace(old,'Brier score (3 probabilistic predictions): 0.154',1))
PY
run M5 python3 grader.py --r8-jsonl "$W/r8.jsonl" --r8-runlog "$W/r8.log" --r9-jsonl "$W/r9.jsonl" --r9-md "$W/r9.md" --r11-jsonl "$W/r11.jsonl" --r11-md "$W/m5.md" --r11-runlog "$W/r11.log"
python3 - "$W/r11.log" "$W/m6.log" <<'PY'
import sys
s=open(sys.argv[1]).read(); old='A-CKPT710: 21/64'; assert s.count(old)==1
open(sys.argv[2],'w').write(s.replace(old,'A-CKPT710: 22/64',1))
PY
run M6 python3 grader.py --r8-jsonl "$W/r8.jsonl" --r8-runlog "$W/r8.log" --r9-jsonl "$W/r9.jsonl" --r9-md "$W/r9.md" --r11-jsonl "$W/r11.jsonl" --r11-md "$W/r11.md" --r11-runlog "$W/m6.log"
python3 - "$W/r11.jsonl" "$W/m7.jsonl" <<'PY'
import json,sys
src,dst=sys.argv[1:]; done=False
with open(src) as f,open(dst,'w') as o:
 for line in f:
  r=json.loads(line)
  if not done and r.get('cell')=='filler': done=True; continue
  o.write(line)
assert done
PY
run M7 python3 grader.py --r8-jsonl "$W/r8.jsonl" --r8-runlog "$W/r8.log" --r9-jsonl "$W/r9.jsonl" --r9-md "$W/r9.md" --r11-jsonl "$W/m7.jsonl" --r11-md "$W/r11.md" --r11-runlog "$W/r11.log"
python3 - "$W/r11.jsonl" "$W/m8.jsonl" <<'PY'
import json,sys
src,dst=sys.argv[1:]; done=False
with open(src) as f,open(dst,'w') as o:
 for line in f:
  r=json.loads(line)
  if not done and r.get('cell')=='meta' and r.get('pid')==201:
   r['init']['nails']+=1; done=True; line=json.dumps(r,separators=(',',':'))+'\n'
  o.write(line)
assert done
PY
run M8 python3 grader.py --r8-jsonl "$W/r8.jsonl" --r8-runlog "$W/r8.log" --r9-jsonl "$W/r9.jsonl" --r9-md "$W/r9.md" --r11-jsonl "$W/m8.jsonl" --r11-md "$W/r11.md" --r11-runlog "$W/r11.log"
# M9 fixed-path ordering swap, always restored and md5-checked.
cp corpus/evidence/round11-power/ordering.log "$W/ordering.backup"
before=$(md5sum corpus/evidence/round11-power/ordering.log | cut -d' ' -f1)
python3 - <<'PY'
p='corpus/evidence/round11-power/ordering.log'; s=open(p).read(); old='post-hash 2026-09-28T23:10:20Z'; assert s.count(old)==1
open(p,'w').write(s.replace(old,'post-hash 2026-09-29T23:00:00Z',1))
PY
run M9 python3 grader.py
cp "$W/ordering.backup" corpus/evidence/round11-power/ordering.log
after=$(md5sum corpus/evidence/round11-power/ordering.log | cut -d' ' -f1); test "$before" = "$after"
echo "$before $after" > "$W/M9.restore-md5"
# M10 fixed-path bundle swap, always restored and md5-checked.
cp corpus/evidence/round11-power/power_analysis_r11.md "$W/power.backup"
before=$(md5sum corpus/evidence/round11-power/power_analysis_r11.md | cut -d' ' -f1)
printf ' ' >> corpus/evidence/round11-power/power_analysis_r11.md
run M10 python3 grader.py
cp "$W/power.backup" corpus/evidence/round11-power/power_analysis_r11.md
after=$(md5sum corpus/evidence/round11-power/power_analysis_r11.md | cut -d' ' -f1); test "$before" = "$after"
echo "$before $after" > "$W/M10.restore-md5"
# M11 r9-only S3-style raw digit bump; r11 remains clean/default.
python3 - "$W/r9.jsonl" "$W/m11.jsonl" <<'PY'
import json,re,sys
src,dst=sys.argv[1:]; done=False
with open(src) as f,open(dst,'w') as o:
 for line in f:
  r=json.loads(line)
  if not done and r.get('cell')=='A-MONO':
   raw=r['raw']; bs=list(re.finditer(r'```(?:json)?\s*\n(.*?)```',raw,re.S))
   if bs:
    b=bs[-1]; inner=b.group(1); dm=re.search(r'\d',inner)
    if dm:
     d=str((int(dm.group(0))+1)%10); r['raw']=raw[:b.start(1)]+inner[:dm.start()]+d+inner[dm.end():]+raw[b.end(1):]; done=True; line=json.dumps(r,separators=(',',':'))+'\n'
  o.write(line)
assert done
PY
run M11 python3 grader.py --r9-jsonl "$W/m11.jsonl"
run ST python3 grader.py --selftest
set +e
python3 grader.py > "$W/DET-unset.out" 2>&1; rcu=$?
PYTHONHASHSEED=42 python3 grader.py > "$W/DET-42.out" 2>&1; rcs=$?
set -e
printf '%s\n' "$rcu" > "$W/DET-unset.rc"; printf '%s\n' "$rcs" > "$W/DET-42.rc"
md5sum "$W/DET-unset.out" "$W/DET-42.out" > "$W/determinism.md5"
md5sum $FILES > "$W/md5.after"
git status --porcelain > "$W/status.after"
# concise machine-readable summary; full outputs remain in /tmp/r11-mut.
for x in M0 M1 M2 M3 M4 M5 M6 M7 M8 M9 M10 M11 ST; do printf '%s rc=%s ' "$x" "$(cat "$W/$x.rc")"; grep '^MISMATCH ' "$W/$x.out" | cut -d' ' -f2 | paste -sd, - || true; done
printf 'DET rc_unset=%s rc_42=%s ' "$(cat "$W/DET-unset.rc")" "$(cat "$W/DET-42.rc")"; cat "$W/determinism.md5"
printf 'M9_restore '; cat "$W/M9.restore-md5"; printf 'M10_restore '; cat "$W/M10.restore-md5"
printf 'WORK=%s\n' "$W"
