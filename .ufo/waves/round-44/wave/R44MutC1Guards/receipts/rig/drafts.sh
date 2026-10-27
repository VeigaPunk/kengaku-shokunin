#!/usr/bin/env bash
# Draft red controls for round-44 C1-counter surviving guards (seat R44MutC1Guards).
# Each draft runs pristine (base counter) and the mutant counter copy; all runs in the round-44 envelope.
set -u
S=/fast/scratch/hyaku/kengaku-r44/R44MutC1Guards
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
C=$L/.ufo/waves/round-44/claims
ENV="$C/envelope.sh"
D=$S/drafts
mkdir -p "$D/out" "$D/modules/d05" "$D/modules/d06" "$D/modules/d08" "$D/modules/d09"
cp "$D/d05symlink.py" "$D/modules/d05/"
cp "$D/d06orderdir.py" "$D/modules/d06/"
cp "$D/d08barewt.py" "$D/modules/d08/"
cp "$D/d09underdecl.py" "$D/modules/d09/"

run() { # $1=label  rest=arguments (counter copy + args)
  local label=$1; shift
  "$ENV" "$S" python3 "$@" > "$D/out/$label.txt" 2>&1
  echo "== $label done =="
}

# ---------- d05 symlink breach ----------
run d05-pristine "$S/mut/base.py" --lane "$L" --battery-dir "$D/modules/d05" --only U5 --work "$D/w-d05-p"
run d05-M05     "$S/mut/M05.py" --lane "$L" --battery-dir "$D/modules/d05" --only U5 --work "$D/w-d05-m"

# ---------- d06 order receipt-is-directory ----------
run d06-pristine "$S/mut/base.py" --lane "$L" --battery-dir "$D/modules/d06" --only U14c --work "$D/w-d06-p"
run d06-M06     "$S/mut/M06.py" --lane "$L" --battery-dir "$D/modules/d06" --only U14c --work "$D/w-d06-m"

# ---------- d08 bare-worktree (worktree branch) ----------
run d08-pristine "$S/mut/base.py" --lane "$L" --battery-dir "$D/modules/d08" --only U5 --work "$D/w-d08-p"
run d08-M08     "$S/mut/M08.py" --lane "$L" --battery-dir "$D/modules/d08" --only U5 --work "$D/w-d08-m"

# ---------- d09 underdeclared defects conjunct ----------
run d09-pristine "$S/mut/base.py" --lane "$L" --battery-dir "$D/modules/d09" --only U5 --work "$D/w-d09-p"
run d09-M09     "$S/mut/M09.py" --lane "$L" --battery-dir "$D/modules/d09" --only U5 --work "$D/w-d09-m"

# ---------- d04 newline-count validity (table row XNL1 injected) ----------
add_xnl1() { # $1=counter copy
  python3 - "$1" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
row = ("    ('XNL1', 'anchor', 'digest-short', 'silence', 'direct',\n"
       "     \"draft XNL1: a split expression changes the newline count\",\n"
       "     \"draft (seat R44MutC1Guards)\",\n"
       "     'cls, why = (\"digest-short\" if len(tok) < 64 else \"digest-long\")',\n"
       "     'cls, why = (\"digest-long\"\\n                if len(tok) < 64 else \"digest-short\")'),\n")
assert s.count("MUTANTS = [") == 1
i = s.index("MUTANTS = ["); j = s.index("\n]\n", i)
open(p, "w").write(s[:j+1] + "\n" + row + s[j+1:])
PY
}
cp "$S/mut/base.py" "$S/mut/d04-base-copy.py"; add_xnl1 "$S/mut/d04-base-copy.py"
cp "$S/mut/M04.py" "$S/mut/d04-M04-copy.py"; add_xnl1 "$S/mut/d04-M04-copy.py"
run d04-pristine "$S/mut/d04-base-copy.py" --lane "$L" --battery-dir "$C/witness" --only XNL1 --work "$S/wd-d04-p"
run d04-M04     "$S/mut/d04-M04-copy.py" --lane "$L" --battery-dir "$C/witness" --only XNL1 --work "$S/wd-d04-m"

# ---------- d10 floors sum redundancy (FLOORS sum != TOTAL) ----------
mk_floors() { # $1=counter copy
  python3 - "$1" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = 'FLOORS = {"anchor": 4, "order": 1}'
assert s.count(old) == 1
open(p, "w").write(s.replace(old, 'FLOORS = {"anchor": 6, "order": 4}'))
PY
}
cp "$S/mut/base.py" "$D/d10-base-copy.py"; mk_floors "$D/d10-base-copy.py"
cp "$S/mut/M10.py" "$D/d10-M10-copy.py"; mk_floors "$D/d10-M10-copy.py"
for V in d10-base-copy d10-M10-copy; do
  B=$D/mm-$V; rm -rf "$B"; mkdir -p "$B/plans/battery44"
  cp "$L/plans/anchor_digest_check.py" "$L/plans/order_check.py" "$D/$V.py" "$B/plans/"
  mv "$B/plans/$V.py" "$B/plans/round44_c1_verify.py"
  cp "$C/witness/w_u.py" "$B/plans/battery44/"
done
run d10-pristine "$D/mm-d10-base-copy/plans/round44_c1_verify.py" --lane "$D/mm-d10-base-copy" --work "$D/w-d10-p"
run d10-M10     "$D/mm-d10-M10-copy/plans/round44_c1_verify.py" --lane "$D/mm-d10-M10-copy" --work "$D/w-d10-m"

# ---------- d12 fingerprint content term (content-only rewrite between fingerprints) ----------
mk_tamper() { # $1=counter copy
  python3 - "$1" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = "        prints = [fingerprint(fx[\"dir\"]) for fx in fixtures]"
new = ("        prints = [fingerprint(fx[\"dir\"]) for fx in fixtures]\n"
       "        for fx in fixtures:\n"
       "            _p = fx[\"dir\"] / \"lane\" / \"corpus/SOURCES.md\"\n"
       "            if not _p.exists():\n"
       "                for _top, _ds, _fs in os.walk(fx[\"dir\"]):\n"
       "                    if \"SOURCES.md\" in _fs:\n"
       "                        _p = pathlib.Path(_top) / \"SOURCES.md\"; break\n"
       "            if _p.exists():\n"
       "                _b = _p.read_bytes(); _p.write_bytes(_b[::-1])\n")
assert s.count(old) == 1, "tamper anchor"
open(p, "w").write(s.replace(old, new))
PY
}
cp "$S/mut/base.py" "$S/mut/d12-base-copy.py"; mk_tamper "$S/mut/d12-base-copy.py"
cp "$S/mut/M12.py" "$S/mut/d12-M12-copy.py"; mk_tamper "$S/mut/d12-M12-copy.py"
run d12-pristine "$S/mut/d12-base-copy.py" --lane "$L" --battery-dir "$C/witness" --work "$S/wd-d12-p"
run d12-M12     "$S/mut/d12-M12-copy.py" --lane "$L" --battery-dir "$C/witness" --work "$S/wd-d12-m"

# ---------- d15 null run (second "unmodified" copy is actually U5-mutated) ----------
mk_null() { # $1=counter copy
  python3 - "$1" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = "            nv.write_text(srcs[tool])"
new = ("            nv.write_text(srcs[tool].replace(\n"
       "                'cls, why = (\"digest-short\" if len(tok) < 64 else \"digest-long\")',\n"
       "                'cls, why = (\"digest-long\" if len(tok) < 64 else \"digest-long\")'))\n")
assert s.count(old) == 1, "null anchor"
open(p, "w").write(s.replace(old, new))
PY
}
cp "$S/mut/base.py" "$S/mut/d15-base-copy.py"; mk_null "$S/mut/d15-base-copy.py"
cp "$S/mut/M15.py" "$S/mut/d15-M15-copy.py"; mk_null "$S/mut/d15-M15-copy.py"
run d15-pristine "$S/mut/d15-base-copy.py" --lane "$L" --battery-dir "$C/witness" --work "$S/wd-d15-p"
run d15-M15     "$S/mut/d15-M15-copy.py" --lane "$L" --battery-dir "$C/witness" --work "$S/wd-d15-m"
run d03-base-seed0 "$S/mut/base.py" --lane "$L" --battery-dir "$C/witness" --work "$D/w-d03-p0"
run d03-M03-seed0 "$S/mut/M03.py" --lane "$L" --battery-dir "$C/witness" --work "$D/w-d03-m0"
run d03-base-seed7 "$S/mut/base.py" --lane "$L" --battery-dir "$C/witness" --work "$D/w-d03-p7"
run d03-M03-seed7 "$S/mut/M03.py" --lane "$L" --battery-dir "$C/witness" --work "$D/w-d03-m7"

# ---------- d03 reference-trace stability: negative measurement (outer seed varied) ----------
run d03-base-seed1 "$S/mut/base.py" --lane "$L" --battery-dir "$C/witness" --work "$D/w-d03-p1"
run d03-M03-seed1 "$S/mut/M03.py" --lane "$L" --battery-dir "$C/witness" --work "$D/w-d03-m1"
echo "drafts done"
