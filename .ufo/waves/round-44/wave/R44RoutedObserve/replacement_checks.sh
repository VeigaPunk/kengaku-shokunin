#!/bin/sh
# run from lane root; each line: id | replacement check (exit 0 = closing evidence is present)
t() { id=$1; shift; if sh -c "$*" >/dev/null 2>&1; then echo "REPL $id pass"; else echo "REPL $id FAIL"; fi; }
t R42-R3-11 "grep -qF 'are **not** \"named carried again in the freeze\"' corpus/lessons/round-42.md"
t R42-R3-12 "grep -qF 'E3 — the route-mix ratios are quoted stdout, not persisted data' corpus/lessons/round-42.md"
t R42-R3-13 "grep -qF 'lookup-28\` CASE row is **line 11**' corpus/lessons/round-42.md && grep -qF 'pointer corrected' corpus/lessons/round-42.md"
t R42-R3-15 "grep -qF \"grep -cE '^ {0,3}\\\\|\" corpus/lessons/round-42.md"
t R42-R3-17 "grep -qF 'E6 — row 3' corpus/lessons/round-42.md"
t R42-R3-20 "grep -qF 'C3 (D3) — Q33 (b) cites a predicate line its own instruction cannot print' corpus/QUALITY.md"
t R42-R3-23 "grep -qF 'C6 (D6) — the last sentence' corpus/QUALITY.md"
t R42-R3-31 "grep -qF 'S1 — the envelope note is one counter too wide' SCORECARD.md"
t R42-R3-38 "grep -qE '^## Errata \\(round 43' corpus/knowledge/tb2-circuit-fibsqrt-grader.md && grep -qF '**E1 \`:296-298\`' corpus/knowledge/tb2-circuit-fibsqrt-grader.md"
t R42-R3-39 "grep -qE '^## Errata \\(round 43' corpus/knowledge/tb2-circuit-fibsqrt-grader.md && grep -qF '**E2 \`:309-312\`' corpus/knowledge/tb2-circuit-fibsqrt-grader.md"
t R42-R3-40 "grep -qE '^## Errata \\(round 43' corpus/knowledge/tb2-circuit-fibsqrt-grader.md && grep -qF '**E3 \`:430-432\`' corpus/knowledge/tb2-circuit-fibsqrt-grader.md"
t R42-R3-14 "sed -n 327p plans/round42_c2_verify.py | grep -qF '(\"V9\"'"
t R42-R3-16 "sed -n 9,10p corpus/evidence/round42/tb2-circuit-fibsqrt/Dockerfile | grep -c '^COPY' | grep -qx 2"
t R42-R2 "python3 plans/routed_open.py --lane . --list | grep -qE '^ROW R42-R2\\.[12] status=closed' && test -f plans/scratch_guard.py"
t R40-R1 "grep -q 'unshare-ipc' plans/round42_c1_verify.py && grep -q 'unattributed' plans/round42_c1_verify.py && grep -qs 'R42-R1' corpus/routed-findings.jsonl"
