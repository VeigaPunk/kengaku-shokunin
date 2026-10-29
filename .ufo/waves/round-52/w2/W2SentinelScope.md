# W2SentinelScope — scoped findings (round 52, wave 2, read-only)

Full report with commands, numbers and receipts: `.ufo/waves/round-52/w2/W2SentinelScope/report.md`. Snapshot ~20:57 (-0300); wave 2 was still writing.

## Verdict

Scope discipline: **partially clean.** No round-52 seat wrote a tracked file outside the declared surfaces. No seat touched fleet tracked files, `scripts/`, `templates/`, `MANIFEST.json`, fleet `.ufo/state/`, or a sibling lane (by evidence; fleet and sibling attribution is by timing and is marked as inference in the full report).

## Findings

| id | sev | what | where | remediation |
|---|---|---|---|---|
| F1 | MEDIUM (latent) | GH013-excluded bytes on disk, untracked, in a wave-1 report dir. The directory is an untracked byte-identical duplicate of the 184-file capture set. Auto-track is `none()`, so this needs an explicit track or `git add` to publish. | `.ufo/waves/round-52/w1/C1ExecFetchGraders/artifacts/graders/sanitize-git-repo/tests/test_outputs.py` (sha256 `57e49041…b59e`, matches EXCLUDED.md) | L1 deletes the untracked `artifacts/graders/` duplicate; append-only correction of the w1 report pointer (lines 82–85) |
| F2 | MEDIUM | Same blob reachable from local refs: commits `de616d7` (7 `refs/jj/keep/*`) and `cdc0d68` (1 keep ref). Not ancestors of `master` `87301ba`. | `git log --all --find-object=3269e74e…` | Never `push --all`/`--mirror`; keep `refs/jj/keep/*` out of pushes |
| F3 | LOW | Non-report artefacts in wave-2 seat dirs not named in `w2-spec.json`: `W2ExecCapturesVerify/verify.py`; `W2ExecEntryDraft/{ast_cmp.py,why.py,build.py,counter.out}`; `W2ScribeIndexRows/receipts/{c1-now,c2-now,c1-selftest-now,c2-selftest-now}.txt`; `W2ConnectSiblings2/{c1,c2}-landed.txt` | `.ufo/waves/round-52/w2/<seat>/` | L1 copies only spec-named receipts; un-named ones stay out of commits |
| F4 | LOW (convention) | Host absolute paths in 89 committed round-52 files (610 occurrences); largest are orchestrator dispatch/run logs. Captures: 0. Pre-round history: 6133 files. | `w2-run.out`, `w2-dispatch.json`, `w1-run.out`, `w1-dispatch.json`, `w1-results.json`, `w2-spec.json`, `w2/swarm-registry.json`, `w1-spec.json` | Redact or exclude orchestrator logs from lane commits |

## Credentials (redacted)

- Committed round-52 surfaces: 0 token-shape hits. 2 generic hits, both false positives (identifier `authority` in `w1/C2ScribeRowsB/census-base.json:133`; upstream `tokenizer = …from_pretrained(…)` in `corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py:18`).
- Untracked round-52 (`w2/`, `claims/`): 0 token shapes. 4 generic hits in 3 files, all code identifiers (`password_match`, `secret`, `tokenizer`).
- Excluded copy (F1): 2 `hf_`-shaped tokens, total lengths 35 and 37 chars. Value not reproduced.
- Committed captures (183): 0 token shapes.
- Unanchored `sk-` pattern: 133 pre-round files, all substring false positives (word-bounded: 0).

## Capture set

183 committed captures = 93 `test_outputs.py` + 89 `test.sh` + 1 `verify.sh`. `sha256sum -c`: **183 OK, 1 missing** (the excluded file, as A5 expects). Names all match TB2 grader shapes. No host paths or non-benchmark content found. Spot-checked 3 captures against raw upstream at pin: MATCH.

## Fleet, sibling, state

- Fleet tracked `MANIFEST.json`, `SCORECARD.md`, `LOG.md`, `scripts/`, `templates/`: no uncommitted diff; in-window mtimes trace to protocol-shokunin ledger commits (orchestrator).
- Fleet `.ufo/state/`: appended by orchestrator daemons (20:57:49, 20:54:51). No kengaku seat signature.
- Sibling lanes: many in-window writes in their own trees; 2 text mentions of kengaku paths in kaidoku round-49 files; none attributable to a kengaku seat.
- `~/.local/bin`: untouched. No tool installs by this seat.
- Scratch `/fast/scratch/hyaku/kengaku-r52/` 3.1 GB; `gh013/` (L1) holds an exact copy of the excluded bytes outside the lane.

## Commands

Read-only only: `git status`, `git log`, `git ls-files`, `git grep --cached`, `git diff --name-only/--numstat` (base `30801b4`), `git for-each-ref --contains`, `git log --all --find-object`, `jj --version`, `jj --ignore-working-copy config list --repo`, `sha256sum -c`, `diff -rq`, `file`, `find -newer`, and `curl` GETs (3 files, scratch, removed). No counter run. No mutation, no pacman, no install.
