# Round 12 scope / safety audit

Audit evidence was collected read-only from the `kengaku-shokunin` root. I did not read `/tmp/kengaku-r12-main/results-r12.jsonl`; the landed copy and run log were checked only after they appeared in the repo. No request was sent to `127.0.0.1:34113` by this audit.

## 1. Protected files and repository state

Commands:

```sh
git rev-parse HEAD
git status --porcelain=v1
git diff --stat f09ff1f..HEAD
git diff --name-status f09ff1f..HEAD
```

Observed:

```text
HEAD=e171cdfbdb350ee90bfc1c66dac54106a3a5e2ca
 M SKILL.md
 M grader.py
?? corpus/evidence/round12-fleet/
?? corpus/evidence/round12-ladder/
 e171cdf... only: A corpus/lessons/round-9-aggregator-corpus-verdict.md
```

The initial audit snapshot (before L1 landing) had only the two untracked round-12 directories. During this audit L1's in-progress landing made `SKILL.md` and `grader.py` dirty. `stat` gives `SKILL.md` mtime `2026-09-28 22:28:37 -0300` and `grader.py` mtime `2026-09-28 22:45:30 -0300`. The diffs are the round-12 knowledge additions (+59 lines to `SKILL.md`) and the round-12 offline gate splice (+3881/−2 lines to `grader.py`), matching the L1-owned integration described in `corpus/evidence/round12-fleet/INTEGRATOR-NOTES.md` (owner and ownership table, §0 and §4). ExecutorGrader separately stated that it wrote only `grader_r12_draft.py` and `r12-grader-notes.md`, and no protected file; those two artifacts have the expected fleet paths.

`e171cdf` is authored by `aggregator-shokunin <aggregator@shokunin.local>` at `22:19:06 -0300`, and `git show --stat e171cdf` shows exactly one added file: `corpus/lessons/round-9-aggregator-corpus-verdict.md`. It does not touch any protected path. This is the same cross-lane aggregator lesson pattern visible in the sibling HEADs, not an L2 edit.

The protected-path content check is direct: `git diff --name-only f09ff1f..HEAD -- SCORECARD.md LOG.md PROVINCE.md SHONEN.md SKILL.md corpus/README.md grader.py 'corpus/evidence/round8-*' 'corpus/evidence/round9-*' 'corpus/evidence/round10-*' 'corpus/evidence/round11-*'` has no output; `git diff --cached --stat` was empty at the snapshots. Thus no protected file was changed by an L2. The current dirty `SKILL.md`/`grader.py` state is an L1 integration-in-progress deviation from the brief's earlier clean-tree expectation, not evidence of an L2 edit.

## 2. Stray-write and push sweep

The three-hour sweep command was:

```sh
find /home/vgpnk/projects/shokunin -name .git -prune -o -type f -mmin -180 -print \
 | grep -v -E '(__pycache__|/\.git$)' \
 | grep -v -E 'corpus/evidence/round12-(ladder|fleet)/' | sort
```

It listed the shared `.ufo` driver/state/wave files, other lanes' own corpus/docs, and the main-repo coordination files. These are concurrent fleet churn (watchdog log records e.g. `launch kengaku round=12` at `2026-09-28T21:21:48-03:00`; state counters read `kengaku=12`, while sibling counters are kagi=15, kake=15, kasegi=16, kotoba=15, kumitate=15). No unexpected *kengaku round-12 artifact path* outside `corpus/evidence/round12-*` was found. The targeted in-repo sweep after the round-12 launch, excluding both round-12 directories, returned only git internals and `corpus/lessons/round-9-aggregator-corpus-verdict.md`; the round-8/9/10/11 sample mtimes are historical/pre-round (`round8 results 18:08:50`, `round9 results 18:26:50`, `round10 models 19:30:49`, `round11 results 20:33:43`).

Sibling commands:

```sh
git -C ~/projects/shokunin/<lane>-shokunin log --oneline -3
git -C ~/projects/shokunin/kengaku-shokunin status -sb
```

Outputs showed kengaku `## master...origin/master [ahead 1]`, with local `e171cdf` and remote tip exactly `f09ff1f` (`git log -1 origin/master`); therefore kengaku did not push the aggregator commit. The kengaku reflog has `f09ff1f` at 21:15:23 and `e171cdf` at 22:19:06. Siblings are ahead locally: kagi ahead 2, kake ahead 1, kasegi ahead 1, kotoba ahead 3; kumitate was in sync with its origin at its own round-14 close. Those are other lanes' own remotes/scopes, allowed by MISSION §Push scope; they are not kengaku-r12 pushes. Main repo status was `## master...origin/master`.

## 3. Domain trees

Commands and outputs:

```sh
git -C ~/Projects/webzites status --porcelain
# fatal: not a git repository

git -C ~/bench-arena status --porcelain
# fatal: not a git repository

ls -ld ~/Projects/bounties
# ls: cannot access .../Projects/bounties: No such file or directory
```

Verdicts: `~/Projects/webzites` = **DIRTY/UNVERIFIABLE AS GIT** (directory exists, but the requested git status cannot resolve); `~/bench-arena` = **DIRTY/UNVERIFIABLE AS GIT** (directory exists, but not a git worktree); `~/Projects/bounties` = **ABSENT**. The committed kasegi loss record `kasegi-shokunin/corpus/knowledge/source-tree-loss-2026-09-28.md:1-15` independently records bounties absent and actor UNDETERMINED; this audit does not attribute that loss to kengaku.

## 4. Endpoint discipline and mock binding

At the current socket snapshot, `ss -tnp | grep -E '34113|18114'` showed the only client as `python3 ... corpus/evidence/round12-ladder/run_r12.py` (pid 1372957) connected to llama-server pid 1299 on `127.0.0.1:34113`; `ss -tlnp` showed only llama-server listening on 34113. `pgrep -af mock_server_r12` returned no process. ExecutorGrader confirmed zero endpoint traffic from its offline gate work and no process touching the main-run tree.

The committed `mock_server_r12.py` source binds `ThreadingHTTPServer(("127.0.0.1", PORT), Handler)` with default `PORT=18114` (source lines 21 and 201); its `do_GET`/`do_POST` classify an absolute-form foreign target as `INTERCEPT`. `/tmp/r12-intercept.log` records `21:52:30 MOCK listening on 127.0.0.1:18114` and `21:52:30 INTERCEPT GET 127.0.0.1:34113/v1/models -> models`; the body is `{"data": [{"id": "mock-r12"}]}`. This proves the request was received by the 18114 proxy, not sent to 34113. The mock smoke tree has 142 records and both descriptor model IDs `mock-r12`; no mock process remains.

The known real-endpoint actors are: ScoutEndpointFresh's self-disclosed two GETs (`r12-endpoint-freshness.md:40-54`, 00:44:25Z, before the run), the permitted L1 real smoke (first request `01:18:37Z`, 72 records), and the L1 main run. The two scout GETs are a **contract violation** under the binding rule as stated for L2 (no L2 sends traffic to 34113), although they were explicitly authorized by the lane's draft roster, read-only, pre-burst, and self-disclosed. Cause: ScoutEndpointFresh executing the L1-dispatched freshness step; recoverable by recording the bounded deviation (no chat-completion traffic and no burst-state perturbation). This is the sole hard-rule violation found.

## 5. Preregistration integrity and ordering

From repo root:

```text
sha256sum -c corpus/evidence/round12-ladder/prereg-bundle.sha256
# all 9 listed files: OK; rc=0
```

The hash manifest's member mtimes are all no later than `prereg-bundle.sha256` mtime `22:16:08.039 -0300`; the latest member is `prereg-precheck.log` at `22:16:08.029`. No bundle member postdates the hash-manifest write. `ordering.log` records pre/post-hash and script hashes at `2026-09-29T01:16:08Z`; first smoke request timestamps are mock `01:18:02Z` and real `01:18:37Z`, both strictly later. The recorded `probe_r12.py` and `run_r12.py` digests reproduce (`1871697f...` and `3beb91ea...`).

The main run landed after the audit started: `corpus/evidence/round12-ladder/results-r12.jsonl` has 4114 lines and `run.log` has 427 lines; their md5s exactly equal `/tmp/kengaku-r12-main/results-r12.jsonl` (`9dd8aa2b6a7aa7890aa802c37d5af0f9`) and `/tmp/kengaku-r12-main/run.log` (`700d1ddd2ece50d7bdedd55859c59f3a`). I did not read the main results until the landed copy existed in-repo.

## 6. Fabrication sweep (eight numeric claims)

| # | Claim | Re-derivation | Status |
|---|---|---|---|
| F1 | bundle has 9 verified files | `sha256sum -c .../prereg-bundle.sha256` printed nine `OK` lines, rc 0 | REPRODUCES |
| F2 | per-problem pass events = 416 | `wc -l predictions-r12-perproblem.jsonl` = 416; arithmetic `5*64+2*48=416` | REPRODUCES |
| F3 | sign events = 304 | `wc -l predictions-r12-signevents.jsonl` = 304; arithmetic `4*64+48=304` | REPRODUCES |
| F4 | total scored events = 727 | `416+304+7=727`, matching INTEGRATOR-NOTES §1 | REPRODUCES |
| F5 | full-run census = 4114 records | independent JSON counter on landed bytes: descriptors 2, meta 64, meta2 48, graded 1328, ack 2256, fillers 416, errors 0; sum 4114 | REPRODUCES |
| F6 | smoke census = 72 records | independent JSON counter on `/tmp/kengaku-r12-smoke/results-r12.jsonl` = 72; cells include descriptors 1/end 1, meta/meta2 1 each, 22 graded | REPRODUCES |
| F7 | mock census = 142 records and zero errors | independent counter on `/tmp/kengaku-r12-mock/results-r12.jsonl` = 142, descriptors model IDs both `mock-r12`, error count 0 | REPRODUCES |
| F8 | served capture is 872 bytes | `wc -c /tmp/r12f-models.json` = 872; md5 `cd90917c...`, sha256 `9267e1ee...`, matching `r12-endpoint-freshness.md:120-122` | REPRODUCES |

An additional independent check recomputed E6 final-turn outcomes from 4114 landed records: 416 events, per-arm passes `A-INC 48/64`, `A-CKPT4710 28/64`, `A-CKPT710 21/64`, `A-CKPT10 10/64`, `A-MONO 2/64`, `T-DENSE 2/48`, `T-SPARSE 2/48`; Brier 0.128750 and BSS 0.044726. The promoted engine's default invocation currently exits 2 because RL3's prediction markdown contains unescaped `|` characters in the event text (`predictions-r12.md:147`), while its parser splits on unescaped pipes; this is an L1 integration defect to resolve, not a fabricated numeric result and not an L2 scope write.

## Verdict table

| id | rule | evidence | verdict |
|---|---|---|---|
| S1 | No L2 protected-file modification | `git diff f09ff1f..HEAD` has only aggregator lesson ADD; current `SKILL.md`/`grader.py` dirt is L1's integration, with L2 ownership records in `INTEGRATOR-NOTES.md` and ExecutorGrader response | CLEAN for L2; L1 landing is in progress |
| S2 | No stray kengaku-r12 writes outside allowed paths | post-launch targeted find found no kengaku-r12 path outside `corpus/evidence/round12-*`; other in-window paths are shared driver/other-lane churn | CLEAN |
| S3 | No unauthorized kengaku push/new remote commit | `status -sb` ahead 1; origin tip remains f09ff1f; reflog identifies local e171cdf only | CLEAN |
| S4 | Domain source trees untouched | webzites/bench-arena are directories but not git worktrees; bounties absent and loss independently documented | UNVERIFIABLE / ABSENT (not attributable to this round) |
| S5 | Endpoint only L1 smoke + main; no L2 traffic | current socket only main; mock bound 18114; but ScoutEndpointFresh self-documents two 34113 GETs | VIOLATION (1 bounded, recoverable) |
| S6 | Prereg hash and smoke ordering | all 9 hashes OK; all bundle-member mtimes ≤ manifest; 01:16:08Z hash lines precede 01:18:02Z/01:18:37Z smoke requests | CLEAN |
| S7 | Numeric claims reproducible | F1–F8 all REPRODUCES; main result/run bytes md5-match `/tmp` landing source | CLEAN |

The ScoutEndpointFresh traffic is precisely attributable and recoverable before the round-12 commit: disclose the two metadata GETs in the L1 report and keep the run evidence unchanged. The in-progress L1 `SKILL.md`/`grader.py` edits are also recoverable as normal landing work, but must not be attributed to an L2.

SCOPE VERDICT: VIOLATION (1)
