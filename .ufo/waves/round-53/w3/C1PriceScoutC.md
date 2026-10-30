# C1PriceScoutC — wave-3 prior-art pricing for R53-C1 (four confirmed tasks)

Seat: `C1PriceScoutC` (scout), kengaku round 53 wave 3, L1 `KengakuR53`.
Scope: the PRIOR-ART leg of R53-C1 for the four confirmed never-read, presence-only tasks
`fix-code-vulnerability`, `modernize-scientific-stack`, `pytorch-model-cli`,
`torch-tensor-parallelism`. For each task: is a presence-only (artefact-existence) weakness of
**that task's** grader already documented anywhere public?

**Outcome: 4/4 tasks priced — 1 `phenomenon-known`, 3 `phenomenon-new`. No `unclear`.**

## State and tooling

* Lane clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r53/C1PriceScoutC/lane`
  → `git rev-parse --show-toplevel` printed `/fast/scratch/hyaku/kengaku-r53/C1PriceScoutC/lane`.
* **Lane HEAD I ran at: `9ead4476bf55b1ea6490d0204b668195db4a4d1d`** — the lane had advanced past the
  dispatched tip `b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe` while this seat worked; the L1 reconciles.
* Disk guard before the pass: `scripts/hyaku/disk-guard.sh status` → `/fast/scratch/hyaku` 42 % used,
  467.6 G free, 2.3 G under `/fast/scratch/hyaku/kengaku-r53`; no ENOSPC.
* Tools used, **no installs and no upgrades**: `gh` 2.102.0 (pre-existing at `~/.local/bin/gh`,
  authenticated), `curl`, `python3` (stdlib only). No pacman transaction (pacman is paused host-wide).
  The GitHub token was never printed or stored: every API call went through `gh api`.
* Read but never modified outside my seat dir: `plans/round53_c1_triage.py` (the frozen counter),
  `plans/round52-tasks.json`, `corpus/evidence/round53/tests-index.json`, `corpus/SOURCES.md`.
  Not read, as instructed: the label files, the classifier output, `.ufo/waves/round-53/w2/` reader parts.

## Method (exact commands)

```sh
# 1. complete enumeration of the three Terminal-Bench trackers (+ one fork), then a local grep
gh api "repos/harbor-framework/terminal-bench-2-1/issues?state=all&per_page=100&page=$p"   # 249 items
gh api "repos/harbor-framework/terminal-bench-2/issues?state=all&per_page=100&page=$p"     #  89 items
gh api "repos/harbor-framework/terminal-bench/issues?state=all&per_page=100&page=$p"        # 2084 items
gh api "repos/RyanMarten/terminal-bench-3/issues?state=all&per_page=100&page=$p"           #  94 items
#   → grep each title+body for the 4 task ids and all 17 of their test names (see tests-index.json)

# 2. GitHub search API (38 distinct queries; 39 responses saved)
gh api "search/issues?q=repo:harbor-framework/terminal-bench-2-1+%22<pkg>%22+%22only+checked+to+exist%22"
gh api "search/issues?q=repo:harbor-framework/terminal-bench-2+%22<pkg>%22+existence"
gh api "search/issues?q=repo:harbor-framework/terminal-bench-1+%22<pkg>%22+%22only+checked+to+exist%22"
gh api "search/issues?q=%22<test-name>%22"                    # global, per P1 test name
gh api "search/code?q=%22<test-name>%22"                      # 6 P1 test names
gh api "search/issues?q=%22<pkg>%22"                           # global, per package
gh api "search/issues?q=%22<pkg>%22+exists" / +verifier        # global weakness-word probes

# 3. archive the primaries (fetched bytes verbatim after a SOURCE-URL: header)
gh api "https://api.github.com/repos/harbor-framework/terminal-bench-2/pulls/53"   > <bytes>
curl -sSL --max-time 90 "https://arxiv.org/abs/2503.15223"                          > <bytes>

# 4. validate the rows with the frozen counter's own leg (the counter is imported, not re-implemented)
python3 -c "import importlib.util; ... m.leg_prior_art(fake_lane, m.CFG, confirmed, idx)"
```

Test names used for every name check (from the pinned `corpus/evidence/round53/tests-index.json`):
`fix-code-vulnerability` 6 names, `modernize-scientific-stack` 2, `pytorch-model-cli` 6,
`torch-tensor-parallelism` 3 — 17 in total.

## Verdicts (measured)

| task | verdict | the archive that decides it | why |
|---|---|---|---|
| `modernize-scientific-stack` | **phenomenon-known** | tb2-1 issue **#242** "modernize-scientific-stack: dependency file only checked to exist, output numbers can be hardcoded" | names the task **and** its test `test_dependency_file_exists`; documents the existence-only weakness: "`touch requirements.txt` plus a script with two hardcoded `print()` calls passes … the file is never opened". The report was moved to the legacy tracker as tb1 **#2173** and the fix is tb1 PR **#2464** ("the old test only checked the dependency file existed … so `touch requirements.txt` + two hardcoded prints scored 1") — the weakness is unambiguously public. |
| `fix-code-vulnerability` | **phenomenon-new** | TB2 PR #53 body (maintainers' own class: "Tests were updated when they over-specified or let any solution pass") | no public item documents an artefact-existence weakness of this task's grader. The only task-naming public items are tb2-1 #134 (oracle left in git HEAD — image packaging), tb2 PR #50 (a missing `_hval` assertion — coverage gap) and tb2-1 #7 (pytest traceback leaks test source). None describes a presence-only verifier. |
| `pytorch-model-cli` | **phenomenon-new** | arXiv:2503.15223 (SWE-bench: "because testing is rarely exhaustive, a patch may pass the tests") | the only public item naming the task and the word "existence" is tb2-1 **#156** (README demands C, instruction/verifier do not) — a **language-contract mismatch**, not an existence-only weakness: #156 itself states the verifier checks "existence, executability, prediction correctness only", i.e. the prediction **content** is checked. The zai-org TB2.0 Verified card names the task under *Instruction Fixes* (image preprocessing), again not existence-only. |
| `torch-tensor-parallelism` | **phenomenon-new** | arXiv:2511.21654 (EvilGenie: agents "can easily reward hack, such as by hardcoding test cases or editing the testing files") | the only public items naming the task are tb2 #80 (verifier pulls the CUDA torch build, 3.03 GB vs 176 MB), tb2 #81 (`mp.spawn(join=True)` behind `dist.barrier()` has no timeout), tb1 #631 row T24 (instruction clarification + memory), the zai-org card (instruction clarification) and fugue-labs/gollem #23 (agent-side checks green while the hidden verifier failed — the opposite of an existence-only weakness). None documents that merely creating the artefact passes this grader. |

Negative-claim evidence for the three `phenomenon-new` rows (all archived, all zero-hit, all bodies
naming neither the task nor any of its tests): 5 sweeps for `fix-code-vulnerability`, 4 each for
`pytorch-model-cli` and `torch-tensor-parallelism` — tracker-scoped queries pairing the task id with
`"only checked to exist"` / `existence`, plus global and tracker-scoped queries on the task's P1
test name. Every sweep archive is a distinct `SOURCE-URL:`-headed fetch with a distinct sha256.

One global query could not be used as a sweep and is documented as such:
`search/issues?q=%22test_report_file_exists_example%22` returns **1** item — benchflow-ai/skillsbench
PR #83, a task-addition PR for a *different* benchmark's task (`10-k-extraction`) that happens to
share the test name; it documents no weakness, but its body names the test name, so it is unusable
as a sweep (A2 rule). The `fix-code-vulnerability` sweep therefore uses the repo-scoped test-name
query plus the global query for `test_vul_file` (0 hits).

## Deliverable rows

`.ufo/waves/round-53/w3/C1PriceScoutC/prior-art-part.json` — 4 rows, one per task:

| task | verdict | url | quote (words) | sweep |
|---|---|---|---|---|
| `fix-code-vulnerability` | phenomenon-new | https://api.github.com/repos/harbor-framework/terminal-bench-2/pulls/53 | "Tests were updated when they over-specified or let any solution pass." (11) | 5 |
| `modernize-scientific-stack` | phenomenon-known | https://api.github.com/repos/harbor-framework/terminal-bench-2-1/issues/242 | "Lines 46–50 (`test_dependency_file_exists`) check that `/app/requirements.txt` or `/app/pyproject.toml` exists. The file is never opened." (14) | — (known rows carry no sweep) |
| `pytorch-model-cli` | phenomenon-new | https://arxiv.org/abs/2503.15223 | "These benchmarks leverage testing to validate generated patches. However, because testing is rarely exhaustive, a patch may pass the tests" (20) | 4 |
| `torch-tensor-parallelism` | phenomenon-new | https://arxiv.org/abs/2511.21654 | "create an environment in which agents can easily reward hack, such as by hardcoding test cases or editing the testing files" (21) | 4 |

Every quote was extracted programmatically from the archived bytes (never retyped), so it is verbatim.

## Verification (the frozen counter's own leg, on my part alone)

The counter module `plans/round53_c1_triage.py` was imported from the clone and `leg_prior_art` run
against a scratch tree holding my four rows and my archives under `corpus/evidence/round53/fetched/`:

```
PRIOR-ART rows=4 tasks_covered=4/4 known=1 new=3 urls=4 rejected=0 target: urls>=3 new>=1
leg_prior_art ok = True
```

Per-row local checks (all `True`): quote word count in 8..25, quote present in the normalised archive,
`SOURCE-URL:` header equals the row URL after `url_key`, the known row's quote names a test of its
task, each `phenomenon-new` archive body names neither the task nor any of its tests, and each sweep
archive is header-bearing, distinct and free of the task's names.

## Numbers measured

* Tracker items enumerated and grepped: 249 (tb2-1) + 89 (tb2) + 2084 (tb1) + 94 (fork) = **2516**;
  items naming any of the four task ids: 6 (tb2-1), 4 (tb2), 3 (tb1), 3 (fork) — all read, all rejected
  as known-candidates with the reason in `candidates.md`.
* Search API: **38 distinct queries** (39 saved responses) plus 4 re-run after a transient 404.
  Global package queries returned 3 473 863 / 79 / 1461 / 887 raw hits (GitHub tokenises hyphenated
  terms, so these are upper bounds; the tracker enumerations above are the reliable part).
* Code search over the six P1 test names: 868 / 388 / 1136 / 1084 / 1146 / 257 hits — all either the
  benchmark's own task files, third-party run artefacts (ctrf.json), or this lane's own texts.
* Archives written: 18 files ≤ 1 MiB, `SHA256SUMS` included.

## Limits (stated, not hidden)

1. The sweep is a **negative claim** and rests on (a) complete enumeration of the three TB trackers plus
   one fork and (b) zero-result GitHub searches. A weakness published outside GitHub (a blog, a forum,
   a private tracker) would not be visible to it.
2. `phenomenon-new` for `pytorch-model-cli` and `torch-tensor-parallelism` is a judgement that the
   public items naming those tasks document *other* defects (instruction contract, packaging, hang,
   agent-side verification fidelity) and not an artefact-existence weakness of the grader. The closest
   item for `pytorch-model-cli` is tb2-1 #156; if the L1 reads #156 as a presence-only report, that
   row flips to `phenomenon-known` and the archive must then be #156 itself (its quote would have to
   name the task id or a test name — #156's line `tests/test_outputs.py | No (existence, executability,
   prediction correctness only)` does name the task, so the flip is mechanically available).
3. `arxiv.org/abs/<id>` pages were used (not `export.arxiv.org/api/query?id_list=…`) because the
   counter's `url_key` strips the query string: all `export.arxiv.org/api/query` URLs would collapse to
   one key and the ≥3-distinct-URL threshold would be threatened.

## Files produced (absolute paths)

* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1PriceScoutC/prior-art-part.json` — the 4 priced rows (deliverable).
* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1PriceScoutC/fetched/` — 18 archives + `SHA256SUMS`.
* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1PriceScoutC/candidates.md` — every URL opened and every rejected candidate with its reason.
* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1PriceScoutC.md` — this report.
* Scratch (clone, raw fetches, builder script, fake lane) under `/fast/scratch/hyaku/kengaku-r53/C1PriceScoutC/` — **removed before this report was written**.

Integration note for the L1: the row paths point at the counter's own location
`corpus/evidence/round53/fetched/<file>`; copy `fetched/` there and the rows need no edit
(the L1 writes `corpus/evidence/round53/`, not this seat).

## Tool observation

`tool: gh api "search/issues?q=repo:harbor-framework/terminal-bench-2-1+<term>" returned HTTP 404 "Not Found" for four valid repo-scoped queries in one batch and then succeeded with the identical command on retry (and for the same queries later in the run) — the 404 is transient, not a query error.`

Report: .ufo/waves/round-53/w3/C1PriceScoutC.md
