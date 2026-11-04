# SourcesR79 — SourcesScribeR79

## Behavior and axes
Coverage: opened upstream primary sources at the frozen Terminal-Bench 2.0 tree. Calibration: distinguish an upstream container model from evidence that the lane's offline instrument cannot stage a particular dependency. Decision: **REJECT S256's full proposed scope**; do not change the frozen claim or taxonomy.

Read `plans/round-79-claims.md` in full before any shell command. No counters, grader, installation script, services, fixtures, or benchmark were executed. No tool installation or update.

## Live provenance
Access date: **2026-11-04**. Pin: `2fd12b88aafdd04a52c298e3940bcb189f9766d6`.

Base URL: `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/`.

| URL suffix | HTTP | bytes downloaded | SHA256 |
|---|---|---:|---|
| README.md | 200 | 4574 | 7dfa9992c45c7e30744cda7ce659ba77309f43120a0990fce033eb8afd972364 |
| nginx-request-logging/tests/test.sh | 200 | 634 | 27761195f53cbfe5941fe39b573631f6c926869e64b7c43220377e1e116528e7 |
| nginx-request-logging/environment/Dockerfile | 200 | 246 | 43003466d89ab83484a3fa618e35b58cdb74a002b1e8716ef30f12b3ac8302d8 |

Captures were saved in `/fast/scratch/hyaku/kengaku-r79/SourcesScribeR79/` as `README.md`, `test.sh`, `Dockerfile`, opened with the read tool, and hashed. These temporary captures are deleted before returning, per scratch discipline; no persistent capture in `corpus/evidence/round79/sources/` is claimed.

Located quote (README.md:43, **21 words**):
> You should now be able to run TB 2.0\! Test it by running the dataset oracle solutions in docker containers locally:

Supporting observations, not additional quotations: README.md:24 describes containerized environments; test.sh:4–5 installs curl, :8 downloads/runs a uv installer, :17–22 stages Python/pytest dependencies and invokes `/tests/test_outputs.py`, :25–28 writes verifier reward. Dockerfile:2–7 selects a Python container base, sets `/app`, and installs requests and curl. None of these three opened files starts a service. None describes the lane's offline probe or establishes that it cannot stage those operations in-process.

## Finding and admit/reject rationale
The existing S256 row inspected at `corpus/SOURCES.md:272` states, verbatim:

> the harness's execution model: a TB2 run is a containerized run, so a grader's `test.sh` installs and starts services inside a container and an in-process offline replay is a different execution surface — the premise of the R79 blocker taxonomy

Its README capture supports the containerized-run clause, **not** the inferred package/service-starting and offline-probe-capability clauses. The additional pinned grading script supports package staging specifically, but still not service startup or the offline probe's limitations. Thus tier A is justified only for upstream's own documented execution model and checked-in commands, not the whole claimed blocker taxonomy. This is an evidence-scope rejection, not a finding that the frozen detectors or target are wrong. No predicate, target, control, or kill rule was reopened.

## Draft contract-v1 row (11 columns; do not apply automatically)

| id | source | kind | tier | what it grounds | anchor | quote | status | verified | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S256 | Terminal-Bench 2.0 README — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md | docs | A | REJECT for the full blocker-taxonomy premise: upstream documents Docker execution, not test.sh service startup or the lane offline probe's inability to stage it; flip: add pinned service-startup evidence and separately located own-work evidence of the offline probe's staging boundary | README.md:43 at 2fd12b88aafdd04a52c298e3940bcb189f9766d6; HTTP 200; 4574 bytes; SHA256 7dfa9992c45c7e30744cda7ce659ba77309f43120a0990fce033eb8afd972364 | You should now be able to run TB 2.0\! Test it by running the dataset oracle solutions in docker containers locally: | rejected | 2026-11-04 | on-release | corpus/lessons/round-79.md, plans/round-79-claims.md |

`rejected` is the registry's existing rejection status; `REJECT` is explicit in the scope cell. Source kind `docs` and scope-limited primary-source tier A follow the registry's contract restatement (SOURCES.md:11–17). The draft uses the requested S256 identity but does not overwrite its existing row.

## Exact shell commands and outcomes
All completed with exit 0. Curl outputs respectively: `HTTP 200 bytes 4574`, `HTTP 200 bytes 634`, `HTTP 200 bytes 246`. Hash output is recorded above.

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r79/SourcesScribeR79
curl --fail --silent --show-error --location --output /fast/scratch/hyaku/kengaku-r79/SourcesScribeR79/README.md --write-out 'HTTP %{http_code} bytes %{size_download}\n' https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md
curl --fail --silent --show-error --location --output /fast/scratch/hyaku/kengaku-r79/SourcesScribeR79/test.sh --write-out 'HTTP %{http_code} bytes %{size_download}\n' https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/nginx-request-logging/tests/test.sh
curl --fail --silent --show-error --location --output /fast/scratch/hyaku/kengaku-r79/SourcesScribeR79/Dockerfile --write-out 'HTTP %{http_code} bytes %{size_download}\n' https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/nginx-request-logging/environment/Dockerfile
sha256sum /fast/scratch/hyaku/kengaku-r79/SourcesScribeR79/README.md /fast/scratch/hyaku/kengaku-r79/SourcesScribeR79/test.sh /fast/scratch/hyaku/kengaku-r79/SourcesScribeR79/Dockerfile
```

Discovery: read the upstream recursive tree at `https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1`, then searched its returned artifact for service-related task paths. Also read the reporting/operator rules and relevant skills. No git commands were needed.

## Gates, limits, touched surfaces
Observed gates: three live HTTP 200 fetches and capture hashes only. C1/C2 execution, census validation, runtime capability testing, and canonical judgment are out of scope and unperformed. No extrapolation from one task to all 88 members. No source-registry or product-code edits; only this report persists. Cleanup command: `rm -rf -- /fast/scratch/hyaku/kengaku-r79/SourcesScribeR79`.

Self-evaluation: accuracy 4/5 (runtime incapability deliberately unproven); completeness 4/5 (honest rejection instead of unsupported admission); clarity 4/5 (separates upstream facts and local boundary); actionability 4/5 (explicit flip evidence); conciseness 4/5 (commands retained for audit). Overall 4.0/5. Improvement: service-startup and local probe-boundary evidence would be necessary for a broader admission, not a stronger interpretation of this README. User-agreement check: report meets the explicit refusal branch without claiming execution evidence.

Artifact: `.ufo/waves/round-79/w1/SourcesScribeR79.md`.
