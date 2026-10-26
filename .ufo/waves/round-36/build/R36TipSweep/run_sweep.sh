#!/usr/bin/env bash
# R36TipSweep baseline driver: run each gate command in the fixture clone,
# record exit code + last non-empty output line.
set -u
L="${1:?lane}"
OUT="${2:?outfile}"
: > "$OUT"

run_one() {
  local label="$1"; shift
  local log rc last
  log="$(mktemp /tmp/k36-tipsweep-log-XXXX)"
  ( cd "$L" && "$@" ) >"$log" 2>&1
  rc=$?
  last="$(awk 'NF{ln=$0} END{print ln}' "$log")"
  printf '%s\t%s\t%s\t%s\n' "$label" "$rc" "${#log}" "$last" >> "$OUT"
  printf '=== %s rc=%s\n' "$label" "$rc"
  printf '%s\n' "$last"
  cp "$log" "/tmp/k36-tipsweep-full-${label//[^A-Za-z0-9_.-]/_}.log"
  rm -f "$log"
}

run_one grader.py                 python3 grader.py
run_one grader-selftest           python3 grader.py --selftest
run_one defect_ledger             python3 plans/defect_ledger.py --lane .
run_one r35_c1_verify             python3 plans/round35_c1_verify.py --lane .
run_one r35_hardening             python3 plans/round35_hardening.py --lane . --skip H6
run_one state_check               python3 plans/state_check.py --summary
run_one registry_check            python3 plans/registry_check.py --summary
run_one benchmark_spec_audit      python3 plans/benchmark_spec_audit.py --summary
run_one config_projection         python3 plans/config_projection.py --summary
run_one sources_census            /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku

echo "--- table ---"
cat "$OUT"
