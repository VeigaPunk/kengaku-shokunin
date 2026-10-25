# FxSourcesCensus
Scope: maintained SOURCES census, frozen contract-v1 manual checks, independent S043–S047 field parse, and source-row diff. Commands ran in `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; only this report was written. No tools installed.

## Maintained commands
```text
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kengaku
kengaku rows 48; tier.A 43; tier.B 3; tier.C 2; status.mined 36; status.queued 9; status.rejected 3
FLEET rows 48; tier.A 43; tier.B 3; tier.C 2; tier.invalid 0; status.queued 9; status.mined 36; status.rejected 3; status.invalid 0; missing 0
EXIT=0
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
kengaku W04 S040 duplicate url arxiv.org/abs/2301.09633 across scopes
kengaku W04 S048 duplicate url aclanthology.org/2020.acl-main.442 across scopes
kengaku ok /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
EXIT=0
```

## Frozen contract-v1 commands
Commands from `/home/vgpnk/Projects/shokunin/CORPUS.md:134-147`; cwd is the lane above. Each command exited 0:
```text
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md => 48
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md => 0
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md => A=43 B=3 C=2
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md => mined=36 queued=9 rejected=3
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d => (empty)
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md => (empty)
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done => (empty)
```

## Independent parse
`awk -F'|' '/^\| S04[3-8] \|/ {for(i=1;i<=NF;i++) gsub(/^[[:space:]]+|[[:space:]]+$/, "", $i); printf "%s\ttier=%s\tstatus=%s\tused-by=%s\tteaches=%s\n", $2, $5, $9, $12, $8}' corpus/SOURCES.md` exited 0. S043=A/mined; S044=A/mined; S045=B/mined; S046=A/mined; S047=A/mined; all five used-by `corpus/lessons/round-26.md`. S048 (current worktree only) =A/mined, same used-by.

## Diff findings
- `git rev-parse HEAD` → `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`, equal to `.ufo/waves/round-26/integration-revision.txt`.
- `git show f11bffbf9caa9c9e286fb32c568b81b97719656a:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 42, exit 0; same command at stamped integration `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8` → 47, exit 0. Thus stamped integration added exactly S043–S047 (5 rows).
- `git diff --unified=0 f11bffbf9caa9c9e286fb32c568b81b97719656a -- corpus/SOURCES.md`: +S043–S048 and one search-log line, 0 deletions. Current lane count is 48 (+6); `git diff --unified=0 3a2aeb15e6494a695d1a950ceea69b0cc9a154f8 -- corpus/SOURCES.md` is +S048 only, so S048 is post-stamp working-tree content.
- S047's `teaches` starts `supersedes S037 —` and corrects the old 14-check teaching with 18 checks, 0 failed. S037 remains untouched; `corpus/lessons/round-26.md:51,54` records that supersession. No pre-existing source-row field edits appear in the base-to-working-tree diff; no old→new field-change entry is needed. All new-row used-by paths resolve.
- W04 on S048 is same-URL-across-scopes warning for its S043 correction; validation remains `ok`. Existing S040 W04 also remains.
- `read xd://lsp` returned “No such tool” (LSP unavailable); findings are from direct file contents and read-only diffs, not semantic-index proof.

Remaining unknown: whether L1 intends to include the post-stamp S048 correction in a subsequent integration revision.

VERDICT: PARTIAL — maintained census and frozen v1 checks are clean on the live lane; S047 properly supersedes S037 without editing it. Count is 5 new rows at stamped integration versus 6 in the current working tree because S048 is post-stamp.