# FP4c — frozen wave-count assertions

Scope: calibration only. No novelty uplift evaluated. Frozen base is `b5719440e5eee46c1886fddbdf7bdc1624829454`; my private clone was created at candidate `b5f62e5e637b34a1549e3475fc58b4227ed87e5a`. Exported the base with `git -C /tmp/kengaku-r27-FP4c archive b5719440e5eee46c1886fddbdf7bdc1624829454 | tar -x -C /tmp/kengaku-r27-base` (exit 0). P4c's frozen scope is `plans/round-27-claims.md:114-124`; Amendment 1 is read at `:155-190`.

## v4 execution and complete P4c status

Commands (both exit 0):
- `python3 -B /tmp/kengaku-r27-FP4c/plans/state_check.py --json --root /tmp/kengaku-r27-base` → JSON summary `assertions=327 match=318 mismatch=0 superseded=6 offline_unverifiable=3 out_of_population=20`.
- `python3 -B /tmp/kengaku-r27-FP4c/plans/state_check.py --json --root /tmp/kengaku-r27-FP4c` → JSON summary `assertions=327 match=318 mismatch=0 superseded=6 offline_unverifiable=3 out_of_population=24`.

Every registered P4c ID returned `MATCH` on both roots (base / candidate):

| ID | base / candidate |
|---|---|
| `P4c.build.seats` | MATCH / MATCH |
| `P4c.build.role-mix` | MATCH / MATCH |
| `P4c.build.reports` | MATCH / MATCH |
| `P4c.falsify.seats` | MATCH / MATCH |
| `P4c.falsify.role-mix` | MATCH / MATCH |
| `P4c.falsify.dead-seats` | MATCH / MATCH |
| `P4c.falsify.reports` | MATCH / MATCH |
| `P4c.round.total-136` | MATCH / MATCH |
| `P4c.round.total-139` | MATCH / MATCH |
| `P4c.r25.raw-tree-entries` | MATCH / MATCH |
| `P4c.r25.markdown-reports` | MATCH / MATCH |

P4c has no MISMATCH or OFFLINE_UNVERIFIABLE result. The three global offline-unverifiable IDs (not P4c) are `P2d.surface.Served local model.availability`, `P2d.surface.Model catalogs.url`, and `P2d.surface.Public literature.url`; the global six SUPERSEDED IDs are P2a, P3a×2, P3b×2, and P4b (`P4b.readme.covers.round26-sources`). The base/candidate out-of-population counts differ (20/24); they do not alter any P4c verdict.

## Independent re-derivation from exported base and named history

The base files independently yield the promised build/falsify role mixes: `jq -r '[.items[].role] | sort | group_by(.)[] | "\\(.[0])=\\(length)"' .ufo/waves/round-26/build-spec.json` (exit 0) → connector=6, critic=6, executor=14, revenger=4, reviewer=12, scout=22, scribe=6, sentinel=1, simplifier=1; the corresponding command on `falsify-spec.json` → connector=2, critic=4, executor=2, mutation-tester=10, reviewer=39, scout=7. Assignment-map `jq` on base (exit 0) → build names/unique IDs 72/72; falsify 64/64; combined unique assignment IDs 136; cross-wave overlap `[]`. `falsify-dead-seats.json` (exit 0) → 11 dead, `replaced=false`, all 11 recorded `agentId`s match the assignment-map value for that name. `find .ufo/waves/round-26/{build,falsify} -maxdepth 1 -type f -name '*.md'` counts (exit 0) → 72 / 53 reports. These independently match lesson lines 87-91 and 118-123. The named recovery receipt says “Three bounded read-only recovery reviews dispatched separately” (`corpus/evidence/round26-calibration/recovery-start.txt:4`), supporting 136+3=139 as a fact.

I separately ran `git -C /tmp/kengaku-r27-FP4c ls-tree -r --name-only REV -- .ufo/waves/round-25/falsify/ | jq -R -s 'split("\\n") | .[:-1] as $n | {entries:($n|length),markdown_reports:([$n[]|select(endswith(".md"))]|length)}'` (exit 0) at each P4c-named revision: `8ea41f9` → 0/0; `8239a56` → 83/82; `9d8a00d` → 88/87. This independently confirms lesson lines 108-114; the raw-entry and Markdown-report units are distinct.

## Findings

**MEDIUM — P4c's total assertions do not verify distinct dispatch identities or independently observe the recovery increment.** In `plans/state_check.py:2637-2640`, `p4_assignment_names` returns assignment *keys*; `:2899-2913` computes “unique dispatched” as the sum of those set sizes and never checks assignment-map values for uniqueness or cross-wave collisions. Current base values are indeed unique/disjoint (independent result above), but duplicate IDs would still satisfy the 136 assertion. The 139 check then sets `total_139 = total_136 + 3` (`:2903`) and records `recovery_reviewers: 3` as a literal (`:2922-2925`); it never reads the independent `recovery-start.txt:4` receipt or recovery dispatch records. Therefore a missing/conflicting recovery receipt would not affect MATCH. This under-covers the registered “unique dispatched seats” and 139 claims; observed values themselves rederive correctly. Also, `P4c.falsify.dead-seats` checks dead names are assigned (`:2844-2866`) but does not compare each dead record's `agentId` to the corresponding assignment value; the current 11 happen to match.

**LOW — the 139 assertion loses its source-line anchor.** v4 JSON reports `source_line:null` for `P4c.round.total-139` on both roots, although it parses 139 from the lesson. Its anchor predicate in `plans/state_check.py:2916-2926` searches for the full phrase on one physical line; the claim wraps across `corpus/lessons/round-26.md:121-122` (“...three recovery” / “reviewers bring...”). This is a traceability defect, not a numeric mismatch.

## Residual risk / verification gaps

The registered P4c population has 11 IDs and covers the explicit categories in the frozen clause; all 11 pass. It does not claim every numeric token in the lesson: Amendment 1 says the separate frozen P4 inventory exposes unmapped numerics and “is not a claim to check every current number” (`plans/round-27-claims.md:184-186`). No P4c mismatch/unverifiable was observed. No installs/updates; no build, lint, formatter, or selftest run. The P4c run on the base used the candidate-clone checker and the clone's Git object database for historic `ls-tree` lookup (the exported archive itself has no `.git`).

VERDICT: All 11 P4c IDs MATCH on the exported base and frozen candidate, and independent base/history counts match the lesson. Recommend tightening the identity/recovery-source checks and restoring the 139 line anchor before treating these self-assertions as fully re-derived; this is a scoped calibration recommendation, not an admission.
### Command evidence correction

The prose in the independent-rederivation section used command shorthand; the exact commands actually run (all exit 0) and outputs are:

- `jq -r '[.items[].role] | sort | group_by(.)[] | "\(.[0])=\(length)"' /tmp/kengaku-r27-base/.ufo/waves/round-26/build-spec.json` → connector=6, critic=6, executor=14, revenger=4, reviewer=12, scout=22, scribe=6, sentinel=1, simplifier=1.
- `jq -r '[.items[].role] | sort | group_by(.)[] | "\(.[0])=\(length)"' /tmp/kengaku-r27-base/.ufo/waves/round-26/falsify-spec.json` → connector=2, critic=4, executor=2, mutation-tester=10, reviewer=39, scout=7.
- `jq -n --slurpfile b /tmp/kengaku-r27-base/.ufo/waves/round-26/build-assignments.json --slurpfile f /tmp/kengaku-r27-base/.ufo/waves/round-26/falsify-assignments.json '$b[0] as $build | $f[0] as $falsify | [$build[]] as $bi | [$falsify[]] as $fi | ($bi|unique) as $bu | ($fi|unique) as $fu | {build_names:($build|length),build_unique_ids:($bu|length),falsify_names:($falsify|length),falsify_unique_ids:($fu|length),combined_unique_ids:(($bi+$fi)|unique|length),overlap_ids:[$bu[] as $id | select($fu|index($id))]}'` → `{"build_names":72,"build_unique_ids":72,"falsify_names":64,"falsify_unique_ids":64,"combined_unique_ids":136,"overlap_ids":[]}`.
- `jq -n --slurpfile a /tmp/kengaku-r27-base/.ufo/waves/round-26/falsify-assignments.json --slurpfile d /tmp/kengaku-r27-base/.ufo/waves/round-26/falsify-dead-seats.json '$a[0] as $assigned | $d[0] as $dead | {dead_count:($dead.dead|length),replaced:$dead.replaced,dead_names:[$dead.dead[].name],dead_ids_match_assignment:([$dead.dead[] | select($assigned[.name] == .agentId)]|length)}'` → dead_count=11, replaced=false, dead_ids_match_assignment=11.
- `printf 'build_reports='; find /tmp/kengaku-r27-base/.ufo/waves/round-26/build -maxdepth 1 -type f -name '*.md' | wc -l; printf 'falsify_reports='; find /tmp/kengaku-r27-base/.ufo/waves/round-26/falsify -maxdepth 1 -type f -name '*.md' | wc -l` → build_reports=72; falsify_reports=53.
- `git -C /tmp/kengaku-r27-FP4c ls-tree -r --name-only 8ea41f9 -- .ufo/waves/round-25/falsify/ | jq -R -s 'split("\n") | .[:-1] as $n | {entries:($n|length),markdown_reports:([$n[]|select(endswith(".md"))]|length)}'` → 0/0; same command with `8239a56` → 83/82; with `9d8a00d` → 88/87.

The revision-specific tree commands above were run separately; `REV` in the earlier sentence was a placeholder, not a literal command argument.
The v4 command detail above omitted only its output redirection/wrapper: actual base command was `python3 -B /tmp/kengaku-r27-FP4c/plans/state_check.py --json --root /tmp/kengaku-r27-base > /tmp/kengaku-r27-FP4c-base-v4.json; rc=$?; printf 'command=python3 -B /tmp/kengaku-r27-FP4c/plans/state_check.py --json --root /tmp/kengaku-r27-base\nexit=%s\n' "$rc"; exit 0` (printed `exit=0`). Candidate command was identical with root `/tmp/kengaku-r27-FP4c` and output `/tmp/kengaku-r27-FP4c-candidate-v4.json` (printed `exit=0`); the summaries above are from those saved JSON files.