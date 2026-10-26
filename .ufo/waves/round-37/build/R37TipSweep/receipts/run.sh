#!/usr/bin/env bash
# Baseline runner: executes each TSV line (label, shell command) inside $LANE,
# records exit code and last non-empty output line to $LOG/summary.tsv.
set -u
LANE=$1; LOG=$2; CMDS=$3; PAR=${4:-4}
export TMPDIR=${TMPDIR:-/fast/scratch/hyaku/kengaku-r37/R37TipSweep}
while IFS=$'\t' read -r label cmd; do
  [ -z "${label:-}" ] && continue
  (
    cd "$LANE" || exit 200
    start=$(date +%s)
    bash -c "$cmd" >"$LOG/$label.log" 2>&1
    rc=$?
    end=$(date +%s)
    last=$(grep -v '^[[:space:]]*$' "$LOG/$label.log" | tail -1)
    printf '%s\t%s\t%ss\t%s\n' "$label" "$rc" "$((end-start))" "$last" >> "$LOG/summary.tsv"
  ) &
  while [ "$(jobs -r | wc -l)" -ge "$PAR" ]; do sleep 0.2; done
done < "$CMDS"
wait
