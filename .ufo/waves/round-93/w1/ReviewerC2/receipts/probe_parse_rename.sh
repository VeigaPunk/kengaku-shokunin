#!/bin/bash
set -u
S=/fast/scratch/hyaku/kengaku-r93/ReviewerC2; L=$S/lane; B2=f0018773f507f363854123856990f8ff8a87eb8c; B9=1df7653633bd4c5a5f373d139f9f1ed02e0f9c07
echo "### W1 independent recomputation (sha256 of git cat-file blob, no gate code)"
for p in plans/round92_c1_replay.py plans/round92_c2_conformance.py plans/round92_burndown.py plans/round91_counter_pin.py; do
  a=$(git -C $L cat-file blob $B2:$p | sha256sum | cut -d' ' -f1); b=$(git -C $L cat-file blob $B9:$p | sha256sum | cut -d' ' -f1)
  [ "$a" = "$b" ] && s=same || s=differ; echo "$s $p"; done
echo "### parse probes (python, gate parse_table at T)"
python3 - <<'PY'
import importlib.util, pathlib
spec = importlib.util.spec_from_file_location("g", "/fast/scratch/hyaku/kengaku-r93/ReviewerC2/zgate_T.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
h = "96257f2573626799caf2d307bde36ca45ffb1c39037f5361a6eb4e55d0239edd"
cases = {
 "normal": f"```frozen-instruments\n{h}  c.py\n```\n",
 "crlf": f"```frozen-instruments\r\n{h}  c.py\r\n```\r\n",
 "trailing-spaces": f"```frozen-instruments\n{h}  c.py   \n```\n",
 "path-with-space": f"```frozen-instruments\n{h}  my dir/c.py\n```\n",
 "uppercase-sha": f"```frozen-instruments\n{h.upper()}  c.py\n```\n",
 "duplicate-path-wrong-sha": f"```frozen-instruments\n{h}  c.py\n{'0'*64}  c.py\n```\n",
 "second-block-malformed": f"```frozen-instruments\n{h}  c.py\n```\n```frozen-instruments\nnot-a-row\n```\n",
}
for k, v in cases.items():
    try: print(f"{k}: rows={[(w[:8],p) for w,p in m.parse_table(v)]}")
    except m.CouldNotEvaluate as e: print(f"{k}: CouldNotEvaluate {e}")
PY
echo "### rename probe: instrument renamed a.py->b.py after freeze (expect broken absent-at-rev)"
d=$S/fx/t8; rm -rf $d; mkdir -p $d; git -C $d init -q -b main
[ "$(git -C $d rev-parse --show-toplevel)" = "$d" ] || { echo MISMATCH; exit 9; }
ID="-c user.name=fixture -c user.email=fixture@invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null"
printf 'a\n' > $d/a.py; printf '```frozen-instruments\n%s  a.py\n```\n' "$(sha256sum $d/a.py | cut -d' ' -f1)" > $d/claims.md
git -C $d add -A && git -C $d $ID commit -q -m freeze; f=$(git -C $d rev-parse HEAD)
git -C $d mv a.py b.py && git -C $d $ID commit -q -m rename; t=$(git -C $d rev-parse HEAD)
python3 -I -B $S/zgate_T.py --lane $d --freeze $f --rev $t --claims claims.md --work $S/fx/work-t8 2>&1 | grep -E '^(INSTRUMENT|PREDICATE)'; echo "rc=${PIPESTATUS[0]}"
