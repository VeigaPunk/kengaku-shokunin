# R31 recon — registry state and the id space the three adopted rows enter

Scout: `L1Kengaku31.R31ReconRegistry` (leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Baseline tip: `0883e72ef8474ca42ac1a54eb0273079f1507035`. Every source/registry byte read 2026-10-25.
Read-only: nothing under the lane repo was written except this file; all simulation scratch is in
`/tmp/r31-registry/` (well under 60 MB, no clone).

Adopted rows under study (per `plans/round-31-claims.md` C1 + lane facts): **S092** (Harbor),
**S093** (SWE-bench Pro V2 verifier files), **S100** (terminal-bench-2), staged read-only at
`/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`.

---

## (a) Row count by the census anchor

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
$ grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md
88
```

Cross-check with the frozen v1 anchor (column-zero only) and the malformed-row check:

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
88
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0
$ wc -l corpus/SOURCES.md
142 corpus/SOURCES.md
```

Registry table spans lines 19–110 (`## Registry` at line 19, `## Paths` at line 111); the append point
for new rows is after line 110, before `## Paths`.

```
$ grep -nE '^ {0,3}#{1,3} ' corpus/SOURCES.md
1:# SOURCES — where kengaku learns
19:## Registry
111:## Paths
119:## Search log
136:## Leads (unopened)
```

## (b) Highest ids in use; are S092, S093, S100 free?

```
$ awk -F'|' '/^ {0,3}\|[[:space:]]*S[0-9]{3,}/{i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | tr '\n' ' '
S001 S002 … S086 S090 S091 S081 S082 S083 S084 S085 S086   (88 ids)
```

Full file-order id list (verbatim, wrapped):

```
S001 S002 S003 S004 S005 S006 S007 S008 S009 S010 S011 S012 S013 S014 S015 S016 S017 S018 S019 S020
S021 S022 S023 S024 S025 S026 S027 S028 S029 S030 S031 S032 S033 S034 S035 S036 S037 S038 S039 S040
S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051 S052 S053 S054 S055 S056 S057 S058 S059 S060
S061 S062 S063 S064 S065 S066 S067 S068 S069 S070 S071 S072 S073 S074 S075 S076 S077 S078 S079 S080
S090 S091 S081 S082 S083 S084 S085 S086
```

```
$ awk -F'|' '/^ {0,3}\|[[:space:]]*S[0-9]{3,}/{i=$2; gsub(/[[:space:]]/,"",i); sub(/^S/,"",i); print i}' corpus/SOURCES.md | sort -n | tail -12
077
078
079
080
081
082
083
084
085
086
090
091
```

**Findings.**

- **Highest id in use: `S091`.** The registry holds `S001`–`S086` plus `S090` and `S091`; `S087`,
  `S088`, `S089` are **unused** (the registry already carries a gap below its max, and `S090`/`S091`
  were appended out of numeric order — they sit between `S080` and `S081` in file order).
- **`S092`, `S093`, `S100` are free.** No `S09[2-9]` / `S1[0-9]{2}` id token exists anywhere in
  `corpus/SOURCES.md`:
  ```
  $ grep -nE 'S0(9[2-9])|S1[0-9]{2}' corpus/SOURCES.md
  60:| S038 | … https://doi.org/10.1017/S0950268810000385 | …     <- DOI substring, not an id
  88:| S066 | … https://doi.org/10.1017/S0950268810000385 | …
  89:| S067 | … https://doi.org/10.1017/S0950268810000385 | …
  ```
  (all three hits are the `S0950268810000385` DOI; zero id collisions.)
- **Id-space hazard on the staged package, not on these three rows:** the staged `S091` is *not* the
  registry's `S091` —
  ```
  registry:  Agentic Benchmark Checklist (ABC) — https://arxiv.org/abs/2507.02825
  staged  :  日本語性能に優れたNECの大規模言語モデル（LLM）, NEC技報 Vol.75 No.2 — https://jpn.nec.com/techrep/journal/g23/n02/230212.html
  ```
  so appending the staged package wholesale would raise `E03 duplicate id` on `S091`. Adopting only
  `S092`/`S093`/`S100` avoids it; `S087`–`S089` and `S094`–`S099` stay unused after landing.
- After a clean three-row append the id set is `S001`–`S086, S090`–`S093, S100` — 91 rows, still no
  duplicate id (`E03` silent in every simulation below).

## (c) Every existing W04-class duplicate-URL warning, GitHub hosts marked

Authoritative run (frozen census tool, lane target, unchanged tree):

```
$ cd /home/vgpnk/Projects/shokunin
$ sh scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
kengaku	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
kengaku	W04	S048 duplicate url aclanthology.org/2020.acl-main.442 across scopes
kengaku	W04	S057 duplicate url arxiv.org/abs/2405.11874 across scopes
kengaku	W04	S058 duplicate url github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py across scopes
kengaku	W04	S059 duplicate url www.rfc-editor.org/rfc/rfc8259 across scopes
kengaku	W04	S064 duplicate url spec.commonmark.org/0.31.2 across scopes
kengaku	W04	S065 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S066 duplicate url doi.org/10.1017/S0950268810000385 across scopes
kengaku	W04	S067 duplicate url doi.org/10.1017/S0950268810000385 across scopes
kengaku	W04	S068 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json across scopes
kengaku	W04	S069 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py across scopes
kengaku	W04	S071 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S075 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S076 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
$ echo $?
0
$ grep -c W04 /tmp/r31-registry/census.txt
14
```

The normalization the tool applies (`scripts/sources-census.sh:620-626`): strip `#fragment`, strip
trailing `/`, strip scheme, lowercase **host only**, keep path case.

**Warnings that touch GitHub hosts — 3 of the 14:**

| warning | host | url | colliding pair |
|---|---|---|---|
| `W04 S058` | `github.com` | `github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc…/src/inspect_ai/scorer/_pattern.py` | S050 ↔ S058 |
| `W04 S068` | `raw.githubusercontent.com` | `raw.githubusercontent.com/web-arena-x/webarena/dce046…/config_files/test.raw.json` | S061 ↔ S068 |
| `W04 S069` | `raw.githubusercontent.com` | `raw.githubusercontent.com/web-arena-x/webarena/dce046…/evaluation_harness/evaluators.py` | S062 ↔ S069 |

The other 11 are arXiv (2), ACL Anthology (1), RFC Editor (1), CommonMark (1), docs.python.org (4),
doi.org (2). **None of the 14 involves `harbor`, `SWE-bench_Pro-os` or `terminal-bench-2`.** Independent
re-derivation of every normalized-URL collision in the registry (same rule) reproduces exactly those
14 pairs:

```
$ awk -F'|' '<url_of() as in the census> … print every url with >1 row' corpus/SOURCES.md | sort
aclanthology.org/2020.acl-main.442                  2 -> S043 S048
arxiv.org/abs/2301.09633                            2 -> S035 S040
arxiv.org/abs/2405.11874                            2 -> S044 S057
docs.python.org/3/library/json.html                 5 -> S052 S065 S071 S075 S076
doi.org/10.1001/jama.1983.03330370053031            2 -> S030 S042
doi.org/10.1016/j.prevetmed.2013.09.015             2 -> S034 S039
doi.org/10.1017/S0950268810000385                   3 -> S038 S066 S067
github.com/UKGovernmentBEIS/inspect_ai/blob/63e45…  2 -> S050 S058
raw.githubusercontent.com/web-arena-x/webarena/…/config_files/test.raw.json   2 -> S061 S068
raw.githubusercontent.com/web-arena-x/webarena/…/evaluation_harness/evaluators.py 2 -> S062 S069
scale.com/blog/swe-bench-pro                        2 -> S023 S026
spec.commonmark.org/0.31.2                          2 -> S054 S064
www.rfc-editor.org/rfc/rfc8259                      2 -> S053 S059
```

## (d) Tier and status histograms (frozen awk commands from `CORPUS.md`)

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
A=78 B=8 C=2

$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
mined=76 queued=8 rejected=4
```

Both sum to 88. Cross-checked with the maintained parser (0–3-space tolerant, same semantics):

```
$ sh scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kengaku
kengaku	rows	88
kengaku	tier.A	78
kengaku	tier.B	8
kengaku	tier.C	2
kengaku	status.mined	76
kengaku	status.queued	8
kengaku	status.rejected	4
FLEET	rows	88
FLEET	tier.A	78
FLEET	tier.B	8
FLEET	tier.C	2
FLEET	tier.invalid	0
FLEET	status.queued	8
FLEET	status.mined	76
FLEET	status.rejected	4
FLEET	status.invalid	0
FLEET	missing	0
$ echo $?
0
```

Also clean (frozen commands, must print nothing — all three printed nothing):
`duplicate ids`, `enum violations and tier inflation`, `mined rows whose used-by paths do not exist`.

## (e) Do existing rows already cite harbor / SWE-bench_Pro-os / terminal-bench-2?

**Yes — all three source trees are already in the registry**, each at the same pinned revision the
round-31 rows use. Full GitHub-host URL inventory of the registry:

```
$ awk -F'|' '/^ {0,3}\|[[:space:]]*S[0-9]{3,}/{… if url ~ /github/ print NR": "id" "url}' corpus/SOURCES.md
71: S049  https://github.com/EleutherAI/lm-evaluation-harness/blob/d6de8164…/lm_eval/filters/extraction.py
72: S050  https://github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc5…/src/inspect_ai/scorer/_pattern.py
73: S051  https://github.com/openai/evals/blob/main/evals/elsuite/basic/json_match.py
77: S055  https://github.com/openai/simple-evals/tree/652c89d0ca9df547706735883097e9537d40dc47
80: S058  https://github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc5…/src/inspect_ai/scorer/_pattern.py
83: S061  https://raw.githubusercontent.com/web-arena-x/webarena/dce04686…/config_files/test.raw.json
84: S062  https://raw.githubusercontent.com/web-arena-x/webarena/dce04686…/evaluation_harness/evaluators.py
85: S063  https://raw.githubusercontent.com/web-arena-x/webarena/dce04686…/evaluation_harness/helper_functions.py
90: S068  https://raw.githubusercontent.com/web-arena-x/webarena/dce04686…/config_files/test.raw.json
91: S069  https://raw.githubusercontent.com/web-arena-x/webarena/dce04686…/evaluation_harness/evaluators.py
92: S070  https://raw.githubusercontent.com/web-arena-x/webarena/dce04686…/scripts/generate_test_data.py
94: S072  https://raw.githubusercontent.com/web-arena-x/webarena/dce04686…/README.md
95: S073  https://raw.githubusercontent.com/web-arena-x/webarena/dce04686…/prepare.sh
96: S074  https://raw.githubusercontent.com/ServiceNow/BrowserGym/4ccc7233…/browsergym/webarena/src/browsergym/webarena/task.py
99: S077  https://raw.githubusercontent.com/harbor-framework/terminal-bench/e67a2cb7…/docs/TASK_REVIEW_AUTOMATION.md
100: S078  https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766…/v2/README.md
101: S079  https://github.com/laude-institute/terminal-bench-2
102: S080  https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe…/README.md
```

Relevant existing rows (`id | kind | tier | status | opened | recheck | used-by`):

```
S077 | docs | A | mined | 2026-10-25 | 180d | corpus/knowledge/benchmark-task-validity-checklist.md
S078 | docs | A | mined | 2026-10-25 | 180d | corpus/knowledge/benchmark-task-validity-checklist.md
S079 | spec | A | mined | 2026-10-25 | 180d | corpus/knowledge/benchmark-task-validity-checklist.md
S080 | docs | A | mined | 2026-10-25 | 180d | corpus/knowledge/benchmark-task-validity-checklist.md
S090 | docs | A | mined | 2026-10-25 | 180d | corpus/knowledge/benchmark-task-validity-checklist.md
```

Normalized-URL comparison (census rule) of the three staged rows against the registry:

```
registry S077: raw.githubusercontent.com/harbor-framework/terminal-bench/e67a2cb7…/docs/TASK_REVIEW_AUTOMATION.md
registry S078: raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766…/v2/README.md
registry S079: github.com/laude-institute/terminal-bench-2

staged   S092: github.com/laude-institute/harbor
staged   S093: github.com/scaleapi/SWE-bench_Pro-os
staged   S100: github.com/laude-institute/terminal-bench-2

S092 normalized=github.com/laude-institute/harbor        exact-url registry matches=none
S093 normalized=github.com/scaleapi/SWE-bench_Pro-os     exact-url registry matches=none
S100 normalized=github.com/laude-institute/terminal-bench-2  exact-url registry matches=['S079']
```

**Hazard verdict per row.**

- **S100 — hard collision.** Its cited URL is byte-identical (after normalization) to `S079`'s, because
  round 29 adopted the staged `S079` URL form unchanged. Landing S100 raises a **15th `W04`**:
  `W04 S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes`. Warning only —
  exit stays 0 — but any lesson text that repeats "the same 14 W04" is wrong after this round
  (number-drift). Mitigation options: accept the 15th warning and record it as intended (different
  scope: dataset releases/task-count audit vs task packages/schema), or cite a path-bearing URL
  (e.g. the pinned tree/`task.toml` blob URL) so the normalized URL differs.
- **S092 — no normalized-URL collision, real same-tree overlap.** `S077` cites
  `harbor-framework/terminal-bench` at `e67a2cb7…`; S092 cites `laude-institute/harbor` at
  `6099b8cf…`. Different repos, so the census stays silent. The overlap is at the *project* level
  (Harbor the harness vs Terminal-Bench the task set) and must be argued in the row's `scope`, not
  hidden.
- **S093 — no normalized-URL collision, same repo+commit as S078.** `S078` cites
  `raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766…/v2/README.md`; S093 cites
  `github.com/scaleapi/SWE-bench_Pro-os` at the same commit. Different hosts → no `W04`, no `E04`.
  Same tree, different artefact (release notes vs executed verifier code) — again a `scope` question.

## Landing simulation — the staged rows do not land as written

Scratch lane at `/tmp/r31-registry/simroot/kengaku-shokunin/` (real registry copy, three staged rows
inserted after line 110, `corpus/knowledge` and `corpus/lessons` symlinked to the lane's own dirs,
plus a stub `benchmark-verifier-execution-model.md`). Command form:

```
$ sh scripts/sources-census.sh validate --file /tmp/r31-registry/simroot/kengaku-shokunin/corpus/SOURCES.md
```

**Sim A — the three rows verbatim** (`grep -m1 "^| S092 |" SOURCES.append.md` etc.):

```
file	E09	S092 recheck=2026-10-23 — re-verify at the next upstream release (Gate S092 below)
file	E01	S093 fields=12
file	W04	S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
file	E09	S100 recheck=2026-10-23 — re-verify at the next upstream release (Gate S100 below)
file	E11	S092 missing used-by corpus/knowledge/benchmark-verifier-execution-model.md
file	E11	S092 missing used-by corpus/knowledge/terminal-bench-release-identity.md
file	E11	S100 missing used-by corpus/knowledge/benchmark-verifier-execution-model.md
file	E11	S100 missing used-by corpus/knowledge/terminal-bench-release-identity.md
EXIT=1
```

Cell-level evidence from the staged file:

```
$ for id in S092 S093 S100; do line=$(grep -m1 "^| $id |" SOURCES.append.md); echo "$id escaped_pipe=$(printf '%s' "$line" | grep -o '\\|' | wc -l) NF=$(printf '%s' "$line" | awk -F'|' '{print NF}')"; done
S092 escaped_pipe=0 NF=13
S093 escaped_pipe=1 NF=14
S100 escaped_pipe=0 NF=13

S092  status=[ mined ]  opened=[ 2026-10-23 ]  recheck=[ 2026-10-23 — re-verify at the next upstream release (Gate S092 below) ]
S093  (NF=14: the anchor cell's `all_required = fail_to_pass \| pass_to_pass` splits the row; every later cell shifts one column)
S100  status=[ mined ]  opened=[ 2026-10-23 ]  recheck=[ 2026-10-23 — re-verify at the next upstream release (Gate S100 below) ]
```

Four independent blockers, all confirmed by the run above:

1. **`E01` on S093** — one escaped pipe (`fail_to_pass \| pass_to_pass`) makes `NF=14`
   (`fields=12`), so the row must be rewritten pipe-free (round 29 already logged
   `S093:escaped-pipe`, `corpus/lessons/round-29.md:239-240`).
2. **`E09` on S092 and S100** — the `recheck` cell is prose with an em dash and a date; the tool accepts
   only an ISO date, `NNd`, or a bare symbolic cadence (`symbolic(s) = s ~ /^[A-Za-z][A-Za-z0-9 _-]*$/`,
   `scripts/sources-census.sh:582`). The prose cell fails.
3. **`opened=2026-10-23` on all three** — C1's frozen predicate requires `opened=2026-10-25`; the
   census itself passes 2026-10-23 (`E08` silent), so this is a claim-level, not tool-level, mismatch.
4. **`E11` on `corpus/knowledge/terminal-bench-release-identity.md`** — the staged `used-by` for S092 and
   S100 names that entry, which does not exist in the lane (39 knowledge files, none matching
   `terminal-bench`):
   ```
   $ ls corpus/knowledge/ | grep -i terminal
   (none)
   $ find corpus/knowledge -type f -name '*.md' | wc -l
   39
   ```
   S093's `used-by` also names `corpus/knowledge/benchmark-grader-semantics.md`, likewise absent.

**Sim B — corrected rows** (pipe-free, `opened=2026-10-25`, `recheck=180d`, `used-by` trimmed to the
one admitted entry, entry stub present):

```
file	W04	S040 …   (14 baseline warnings, unchanged)
…
file	W04	S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
file	ok	/tmp/r31-registry/simroot/kengaku-shokunin/corpus/SOURCES.md
EXIT=0
$ … | grep -c W04
15
```

Post-landing census of that corrected tree:

```
file	rows	91
file	tier.A	81
file	tier.B	8
file	tier.C	2
file	status.mined	79
file	status.queued	8
file	status.rejected	4
FLEET	rows	91
FLEET	tier.invalid	0
FLEET	status.invalid	0
FLEET	missing	0
```

So the achievable target state is: **91 rows, `A=81 B=8 C=2`, `mined=79 queued=8 rejected=4`,
census exit 0 with 15 `W04` (14 carried + the new S100/S079 pair)**. The `W04` count moving 14 → 15 is
the one registry fact that any "same 14 W04" sentence in the round-31 lesson would falsify.

## Observed / inference / open

**Observed** (commands above): 88 rows; ids `S001`–`S086, S090, S091`; S092/S093/S100 unused; 14 `W04`
of which 3 touch GitHub hosts (S058 on `github.com`, S068/S069 on `raw.githubusercontent.com`);
`A=78 B=8 C=2`, `mined=76 queued=8 rejected=4`; S077/S078/S079/S090 already cite the three source
trees at the same pinned revisions; staged S093 has `NF=14`; staged S092/S100 carry a prose `recheck`
and `opened=2026-10-23`; `corpus/knowledge/terminal-bench-release-identity.md` absent; simulated
corrected landing = exit 0, 91 rows, 15 `W04`.

**Inference** (`[INFERENCE]`): the census's `W04`/`E04` split means the S100/S079 pair will stay a
warning, not an error, because their `scope` cells differ and S100's `teaches` carries no
`supersedes S###` — `E04` fires only on same-URL *and* same-scope *and* both non-rejected.

**Open**: whether the row author will keep `github.com/laude-institute/terminal-bench-2` for S100 (15th
`W04`, intended-duplicate narrative needed) or switch to a path-bearing pinned URL (14 `W04` preserved);
and whether S093's `used-by` drops `benchmark-grader-semantics.md` or that entry is admitted too.

VERDICT: PASS — registry state is clean and the id space is free for S092/S093/S100, but the three staged rows cannot be appended verbatim: S093 raises `E01` (NF=14 escaped pipe), S092 and S100 raise `E09` (prose `recheck`), all three carry `opened=2026-10-23` against C1's `2026-10-25`, `used-by` names two absent knowledge entries, and S100 collides exactly with S079's URL so a clean landing moves the lane from 88 rows / 14 `W04` to 91 rows / 15 `W04`.
