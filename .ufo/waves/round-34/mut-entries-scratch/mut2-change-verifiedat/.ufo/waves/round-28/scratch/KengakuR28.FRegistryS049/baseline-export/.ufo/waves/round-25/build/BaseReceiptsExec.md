# Kengaku round-25 base receipt

Axis: calibration (round-start baseline only; no implementation claim).
Files changed: this report only. No lane source or receipt bytes changed.
Archive: `mkdir -p /tmp/k25-base && git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive 6180e4f | tar -x -C /tmp/k25-base` (exit 0).
Observed base: `git rev-parse 6180e4f` → `6180e4fb92e90c0b172e9788e2c765d097f2e142`.

Commands and retained output (grader tails per request; SOURCES census commands are CORPUS.md:131-148):

```text
COMMAND: python3 grader.py
CHECKS n=733 mismatches=0 errata_pinned=1
VERDICT: PASS — stored evidence fully re-derives offline
EXIT: 0

COMMAND: python3 grader.py --selftest
[selftest] PASS S6 stats anchors (betai/t_crit known values): all known-value assertions hold
[selftest] PASS S7 r12 stats anchors (Page L / grade_seq / Brier-BSS / Newton): all known-value assertions hold
[selftest] ALL PASS
EXIT: 0

COMMAND: python3 plans/attrib_probe.py freeze-check --frozen plans/attrib-r23-frozen.md
FREEZE-CHECK: reads=1 block_sha=1b2d6a01bfa431ec pinned=1b2d6a01bfa431ec stable=True -> OK
EXIT: 0

COMMAND: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate /tmp/k25-base
k25-base	ok	/tmp/k25-base/corpus/SOURCES.md
EXIT: 0

COMMAND: TZ=UTC /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate /tmp/k25-base
k25-base	ok	/tmp/k25-base/corpus/SOURCES.md
EXIT: 0

COMMAND: grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
26
EXIT: 0

COMMAND: awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0
EXIT: 0

COMMAND: awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
A=24 C=2 
EXIT: 0

COMMAND: awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
mined=18 queued=5 rejected=3 
EXIT: 0

COMMAND: awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
EXIT: 0

COMMAND: awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md
EXIT: 0

COMMAND: awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
EXIT: 0
```

Behavior: round-start gates reproduced offline from the base archive. SOURCES contract manual census found 26 rows, 0 malformed, tiers A=24/C=2, statuses mined=18/queued=5/rejected=3, and no duplicate IDs, enum violations, tier inflation, or missing mined paths. This is not the round-25 calibration implementation or landed-tree verification.
Risks/blockers: none in the assigned receipt commands; no live model or endpoint was contacted.
Installs: none.
VERDICT: BASE RECEIPT CAPTURED; ALL ASSIGNED GATES EXITED 0.
