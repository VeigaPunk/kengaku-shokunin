# C1PriceScoutD — prior-art pricing for R53-C1 (PRIOR-ART leg), wave 3, round 53

Seat: `C1PriceScoutD` (scout / prior-art pricing).
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Clone I ran at: `git clone -q --shared … /fast/scratch/hyaku/kengaku-r53/C1PriceScoutD/lane` →
`git -C …/lane rev-parse --show-toplevel` printed `/fast/scratch/hyaku/kengaku-r53/C1PriceScoutD/lane`;
`CLONE_HEAD=9ead4476bf55b1ea6490d0204b668195db4a4d1d` (the lane had already advanced past the build-time tip
`b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe`; the lane HEAD at the end of my seat was the same
`9ead4476bf55b1ea6490d0204b668195db4a4d1d`). The only lane file I read was
`corpus/evidence/round53/tests-index.json` (to get each task's exact test names) and
`plans/round53_c1_triage.py` (the frozen counter). I did **not** read the label files, the classifier output, or
`.ufo/waves/round-53/w2/`.

## 1. Verdicts

| task | tests of that task (from `tests-index.json`) | verdict | row archive | sweep |
|---|---|---|---|---|
| `gcode-to-text` | `test_hello_file_exists`, `test_hello_file_content` | **phenomenon-new** | `https://arxiv.org/html/2507.02825v1` | 4 archived zero-result tracker fetches |
| `mteb-leaderboard` | `test_result_exists`, `test_data_matches` | **phenomenon-new** | `https://api.github.com/repos/harbor-framework/terminal-bench-2/issues/74` | 4 archived zero-result tracker fetches |
| `pytorch-model-recovery` | `test_weights_file_unchanged`, `test_model_file_exists`, `test_model_loads_weights`, `test_state_dicts_match`, `test_model_loss` | **phenomenon-new** | `https://arxiv.org/html/2608.23616v3` | 4 archived zero-result tracker fetches |
| `tune-mjcf` | `test_model_ref_unchanged`, `test_tuned_model_exists`, `test_correctness`, `test_model_speed` | **phenomenon-known** | `https://raw.githubusercontent.com/tigicion/dao-code/master/scripts/verify-tunemjcf-introspect.ts` | not required for a known row (see §3.4) |

No task is `unclear`. Every verdict is backed by an archived, byte-verbatim fetch.

**The one reading the L1 must ratify (important).** `phenomenon-known` requires an archive that names the task id
*or one of its test names* **and** describes an existence-only / let-anything-pass verifier **for it**. The task's
own grader source (which is public, because TB2 is a public benchmark) names the test and *is* the presence-only
check — but it does not *describe* the weakness; it is the object under audit. I therefore read "describes" as
"characterises/discusses the verifier as passable-without-the-work", and did **not** count grader sources as prior
art. The alternative reading (grader source = prior art) would make every one of the 20 confirmed tasks
`phenomenon-known` and would make the leg's own `new >= 1` threshold unsatisfiable — the leg could then never pass,
which is evidence for my reading. `tune-mjcf` is nevertheless `phenomenon-known` under *both* readings, because a
public artefact discusses it as a weakness (below).

## 2. Exact commands run (abridged; the full transcript is in the seat's scratch log)

```sh
# clone the lane (mandatory first step)
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin \
    /fast/scratch/hyaku/kengaku-r53/C1PriceScoutD/lane && \
    git -C /fast/scratch/hyaku/kengaku-r53/C1PriceScoutD/lane rev-parse --show-toplevel
# -> /fast/scratch/hyaku/kengaku-r53/C1PriceScoutD/lane        (CLONE_HEAD 9ead4476bf55b1ea6490d0204b668195db4a4d1d)

# read the counter's prior-art leg
grep -n "def names_task\|def leg_prior_art\|def url_key\|^HDR" plans/round53_c1_triage.py   # lines 370-455
read plans/round53_c1_triage.py:370-470

# whole-tracker sweep (core API, does not burn the search quota)
gh api --paginate "repos/harbor-framework/terminal-bench-2/issues?state=all&per_page=100"  # 89 issues+PRs
gh api --paginate "repos/harbor-framework/terminal-bench-1/issues?state=all&per_page=100"  # 1473
gh api --paginate "repos/harbor-framework/terminal-bench/issues?state=all&per_page=100"    # 2084
# then scanned every title+body with the counter's own regex
#   (?<![A-Za-z0-9_-])<task-or-test>(?![A-Za-z0-9_-])

# per-task tracker sweeps (search API, ~30 req/min; paced 3-4 s)
gh api -X GET "search/issues" -f q="repo:<owner>/<repo> \"<task-id>\"" -f per_page=10

# global (all-GitHub) sweeps
gh api -X GET "search/issues" -f q="\"<task-id>\"" -f per_page=10
gh api -X GET "search/issues" -f q="test_hello_file_exists"   # and the other three test names
gh api -X GET "search/code"  -f q="<task-id> verifier"        # and other code searches
gh api -X GET "search/code"  -f q="\"均PASS\" \"<task-id>\""   # narrow hunt for per-task verifier write-ups

# archived fetches (byte-verbatim, each written with a SOURCE-URL: first line)
curl -sSL -A "kengaku-r53-scout/1.0 (research)" "https://arxiv.org/html/2507.02825v1" -o …
curl -sSL -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
     "https://api.github.com/repos/harbor-framework/terminal-bench-2/issues/74" -o …
curl -sSL -A "kengaku-r53-scout/1.0 (research)" \
     "https://raw.githubusercontent.com/tigicion/dao-code/master/scripts/verify-tunemjcf-introspect.ts" -o …

# re-ran the FROZEN counter's own leg on my rows (synthetic lane, §5)
python3 - <<'PY'   # importlib load of plans/round53_c1_triage.py, then:
                    m.leg_prior_art(Path('fakelane'), {"URL_MIN":3}, confirmed, idx)
PY
```

Disk guard before the heavy pass: `scripts/hyaku/disk-guard.sh status` → `/fast/scratch/hyaku 43 % used,
463.2 G free`; `/tmp 24 % / 97.8 G free`; `/var/tmp 41 % / 533.9 G free`. No ENOSPC.

## 3. Reasoning per task (and the negative evidence behind each `phenomenon-new`)

### 3.1 `gcode-to-text` — phenomenon-new
* The whole-tracker scan (89 + 1473 + 2084 issues/PRs of `harbor-framework/terminal-bench-2`,
  `harbor-framework/terminal-bench-1`, `harbor-framework/terminal-bench`) found **no** item naming
  `gcode-to-text` or `test_hello_file_exists` / `test_hello_file_content` at all.
* Global issue search `"gcode-to-text"`: the only Terminal-Bench-adjacent hits were
  `ekellbuch/terminal-bench-2#3` (“Test oracles”, an oracle/docker pass table) and `#4` (“Terminal bench 2.1
  oracle tests”, same kind of table) — no weakness claim.
* Global code search `"gcode-to-text" verifier` surfaced
  `egonSchiele/agency-lang :: packages/agency-lang/evals/terminal-bench-mini/gcode-to-text/graders.ts`, a public
  **port** of the TB2 verifier. **Rejected as a known-row archive**: it names the task but describes the task's
  verifier as *comparing the trimmed file content against the exact expected string* (plus a hash of it) — i.e. the
  task is **not** passable by mere existence; the port's first grader is existence-only but the second is a content
  check. It documents the grader's structure, not a weakness.
* `prime-radiant-inc/evener#306` (“No provisional-artifact discipline…”) names `gcode-to-text__ffXVje9` and
  reports “both tests failed on file-not-found”. **Rejected**: it is about agents withholding an artefact, and it
  says nothing about an existence-only verifier for this task.
* `maxingaussian/pi-plans` and `xln3/tbench-test` public run artefacts name the task; grep for
  weak / vacuous / only-check / reward-hack language returned **nothing**.
* **Row archive** (general primary, names neither the task nor its tests):
  `https://arxiv.org/html/2507.02825v1` — *Establishing Best Practices for Building Rigorous Agentic Benchmarks*
  (ABC). Quote (12 words, verbatim in the fetched bytes):
  `an agent that does nothing can also have a positive evaluation result`.
* **Sweep** (4 archived zero-result fetches, bodies name neither the task nor its tests):
  `repo:harbor-framework/terminal-bench-2`, `repo:harbor-framework/terminal-bench`,
  `repo:harbor-framework/terminal-bench-challenges`, `repo:harbor-framework/terminal-bench-science`, all
  `"gcode-to-text"` → `total_count 0`.

### 3.2 `mteb-leaderboard` — phenomenon-new
* Tracker items that **do** name the task (so they cannot serve as sweeps), each inspected:
  `harbor-framework/terminal-bench-2#41` (“Reduce mteb-leaderboard difficulty to easy” — difficulty),
  `#27` (“oracle updates for 3 tasks” — container swap/memory), `#53` (“Terminal-Bench 2.1”),
  `harbor-framework/terminal-bench-1#851` (CI base image),
  `harbor-framework/terminal-bench#2061` (“remove outdated leaderboard task” — the grader accepts only
  `GritLM/GritLM-7B`, i.e. over-strict, not existence-only), `#763`/`#779` (static lints),
  `#631` (“tb3 hardening: per-task audit of tb2.1 (PR #53) fixes” — its row T15 for `mteb-leaderboard` is a
  Pillow-dependency / memory finding, *not* an existence-only finding).
  **None** of them describes an existence-only / let-anything-pass verifier for this task.
* Global issue search `"mteb-leaderboard"` → 1381 hits, all irrelevant MTEB-the-embedding-benchmark chatter except
  the tracker items above. Global code search `"mteb-leaderboard" "test_result_exists"` surfaced
  `llm-as-a-verifier/llm-as-a-verifier :: …/mteb-leaderboard__D8kmscc_trajectory.json`, which contains the **public
  grader source** (`def test_result_exists(): assert os.path.exists("/app/result.txt")` next to
  `def test_data_matches()`). **Rejected as a known-row archive**: it is the grader source, not a description of
  its weakness — and it also shows the task's grader is existence **plus** a content check.
* **Row archive** (general primary on the phenomenon, names neither the task nor its tests):
  `https://api.github.com/repos/harbor-framework/terminal-bench-2/issues/74` — the TB2 report of a verifier whose
  tests “pass vacuously” when the artefact is missing because they are guarded by `if os.path.exists(...)`.
  Quote (13 words, verbatim): `the 2 posterior tests pass vacuously — they are guarded by \`if os.path.exists(...)\`` .
* **Sweep** (4 archived zero-result fetches): `repo:harbor-framework/terminal-bench-challenges`,
  `repo:harbor-framework/terminal-bench-science`, `repo:laude-institute/terminal-bench-datasets`,
  `repo:bitfun-datasets/terminal-bench-2-1`, all `"mteb-leaderboard"` → `total_count 0`.
  The four trackers that *do* return hits for this id are unusable as sweeps by rule; they were read instead
  (listed above).

### 3.3 `pytorch-model-recovery` — phenomenon-new
* Tracker hits: `harbor-framework/terminal-bench-2#80` (“verifier installs the CUDA torch build on `gpus = 0`
  (3.03 GB vs 176 MB)”) — a verifier *environment* cost issue, not a weakness. Nothing else in the three trackers
  names the task.
* Public artefacts naming the task's test names: `minixalpha/nanoPyCodeAgent ::
  benchmarks/harbor/reports/en/pytorch-model-recovery-{verifier-20261021,prepared-20261024}.md` — both read; they
  report verifier timeouts and a successful 5/5 pass (`test_weights_file_unchanged`, `test_model_file_exists`,
  `test_model_loads_weights`, `test_state_dicts_match`, `test_model_loss` all Passed). **Rejected as known-row
  archives**: they report outcomes, they do not describe an existence-only verifier.
* **Row archive** (general primary on the phenomenon, names neither the task nor its tests):
  `https://arxiv.org/html/2608.23616v3` — *Mechanically-Enforced Specs for Agentic App Rebuilds*. Quote (12 words,
  verbatim): `Verification signals can encode a measurement artifact rather than a real requirement`.
* **Sweep** (4 archived zero-result fetches): `repo:harbor-framework/terminal-bench`,
  `repo:harbor-framework/terminal-bench-challenges`, `repo:harbor-framework/terminal-bench-science`,
  `repo:laude-institute/terminal-bench-datasets`, all `"pytorch-model-recovery"` → `total_count 0`.
  (`repo:harbor-framework/terminal-bench-2` returns 1 hit that **does** name the task — issue #80 — so it is
  unusable as a sweep and was read instead.)

### 3.4 `tune-mjcf` — phenomenon-known
* `harbor-framework/terminal-bench-1#1013` (“tune-mjcf is a question”) names the task but is about prompt style —
  **rejected**.
* `adeotek/coding-agent-bench#11` (“Task audit over all 89: 78 healthy, 8 broken, 3 host-limited”) names
  `tune-mjcf` in its defect table as “no artifacts produced” and `mteb-leaderboard` as host-limited, and states
  that **no verifier in the whole 89-task set is satisfiable by inaction** (`oracle` must pass, `nop` must fail).
  **Rejected as this row's archive** (it names the task but does not describe an existence-only weakness of it —
  it says the opposite). Archived anyway as `extra-adeotek-pr11.json` because it is the best general primary on
  the *instrument* (the nop gate).
* **ACCEPTED archive** (this is the known row):
  `https://raw.githubusercontent.com/tigicion/dao-code/master/scripts/verify-tunemjcf-introspect.ts` — a public
  per-task verifier introspection script. It names **four of the task's test names** and documents that submitting
  an *unmodified copy* of `model_ref.xml` as `model.xml` makes `test_model_ref_unchanged`,
  `test_tuned_model_exists` (the file merely exists) and `test_correctness` **PASS**, with only `test_model_speed`
  failing. That is a public, task-specific description of a let-anything-pass verifier for `tune-mjcf`.
  Quote (8 words by the counter's whitespace tokenisation; verbatim; this is exactly the string carried in the JSON
  row): `test_model_ref_unchanged: PASS test_tuned_model_exists: PASS(文件存在,但内容=未调参的原始拷贝) test_correctness: PASS(diff=0.0000,因为就是原样拷贝,物理状态自然一致) test_model_speed: FAIL`
  (the Chinese parentheticals are the upstream file's own glosses: “the file exists, but the content is the
  untuned original copy” / “because it is an exact copy of model_ref.xml”). The quote is ≤ 25 words and names four
  of the task's test names, as the counter's `names_task` requires.
  *Caveat for the L1:* this artefact shows 3 of 4 tests passing on an untuned copy, not the whole task passing;
  `test_model_speed` still fails. It is prior art for the **existence-only** weakness of `tune-mjcf`, which is what
  leg 4 prices.
* **Sweep** (not required for a known row, but run and archived anyway): `repo:harbor-framework/terminal-bench-2`,
  `repo:harbor-framework/terminal-bench`, `repo:harbor-framework/terminal-bench-2-1`,
  `repo:harbor-framework/terminal-bench-challenges`, all `"tune-mjcf"` → `total_count 0`.
  One tracker item does name the task's *test name* `test_correctness` —
  `harbor-framework/terminal-bench#19` (“Add latency-collapse task…”) — but it concerns a different task and does
  not describe an existence-only weakness of `tune-mjcf`; it is therefore not a known-row archive (and it is not
  among my sweeps, whose bodies are zero-result).

## 4. Rejected candidates (all URLs I opened, with the reason)

**Search-API queries (GitHub search, ~30 req/min):**
`repo:harbor-framework/terminal-bench-2 "gcode-to-text"` (0) · `… "mteb-leaderboard"` (3, names the task → unusable
as a sweep, read instead) · `… "pytorch-model-recovery"` (1, names the task → unusable, read instead) ·
`… "tune-mjcf"` (0) · the same four ids against `harbor-framework/terminal-bench` (0 / 9 / 0 / 0),
`harbor-framework/terminal-bench-1` (1 / 2 / 2 / 1), `harbor-framework/terminal-bench-2-1` (1 / 13 / 2 / 0),
`harbor-framework/terminal-bench-challenges` (0 / 0 / 0 / 0), `harbor-framework/terminal-bench-science`
(0 / 0 / 0 / 0), `laude-institute/terminal-bench-datasets` (0 for mteb / 0 for pytorch),
`bitfun-datasets/terminal-bench-2-1` (0 for mteb), `ekellbuch/terminal-bench-2` (3 / 2),
`RyanMarten/terminal-bench-3` (1), `adeotek/coding-agent-bench` (1), `harbor-framework/harbor` (1);
global `"gcode-to-text"` (543), `"mteb-leaderboard"` (1381), `"pytorch-model-recovery"` (150), `"tune-mjcf"` (88),
`test_hello_file_exists` (42), `test_result_exists` (1), `test_model_file_exists` (21),
`test_tuned_model_exists` (0), `"mteb-leaderboard" grader weak` (0), `"tune-mjcf" weak test` (4, none about this
task), `"pytorch-model-recovery" verifier exists` (12, none about this task), `"gcode-to-text" grader` (4, none
about this task).
Code searches: `test_tuned_model_exists` (342), `test_hello_file_exists` (1384), `test_model_file_exists` (1010),
`test_result_exists` (928), `"gcode-to-text" verifier` (2032), `"mteb-leaderboard" verifier` (1642),
`"pytorch-model-recovery" verifier` (1836), `"tune-mjcf" verifier` (2100), `"gcode-to-text" introspect` (12),
`"mteb-leaderboard" introspect` (21), `"pytorch-model-recovery" introspect` (13),
`"mteb-leaderboard" "test_result_exists"` (229), `"test_hello_file_exists" "gcode-to-text"` (194),
`"test_result_exists" "mteb-leaderboard"` (229), `"test_model_file_exists" "pytorch-model-recovery"` (108),
`"均PASS" "<task>"` ×3 (0 for gcode/mteb/pytorch, 1 for tune-mjcf → the accepted artefact),
`"复测结果印证" tune-mjcf` (1 → the same artefact).

**Fetched but rejected as row archives (reason in brackets):**
`https://arxiv.org/html/2601.11868` [Terminal-Bench paper — names **all four** task ids, so unusable as a
general primary for any of them]; `https://arxiv.org/abs/2507.02825` [abstract only; the v1 HTML is the archived
copy]; `https://arxiv.org/abs/2604.16529` [test-time scaling paper, no verifier-validity content];
`https://api.github.com/repos/harbor-framework/terminal-bench-2/issues/80` [verifier CUDA install size];
`…/terminal-bench-2/pulls/{41,27,53,72,73}` [difficulty / dependency / tb2.1 roll-up];
`…/terminal-bench-2/issues/74` [ACCEPTED as the mteb row archive];
`…/terminal-bench-1/issues/1013` [prompt style]; `…/terminal-bench-1/pulls/455` [the NOP agent — archived as
`extra-tb1-pr455.json`, a general primary, but 103 chars of body; not used as a row archive];
`…/terminal-bench-1/issues/{1459,1429,1171,1134,1116,1086,1020,813}` [weak-test reports for **other** tasks —
`sudo-llvm-ir weak test`, `word2vec-from-scratch`, `deterministic-tarball weak test`, `parallelize graph`,
`chem-rf`, `make-mips-interpreter` reward hacking — the closest public relatives of the phenomenon, and the
clearest evidence that the phenomenon class is public while these four tasks are not named];
`…/terminal-bench-1/pulls/{1436,1363,1272,968,480,464}` [other tasks]; `…/terminal-bench/issues/631` [names
`mteb-leaderboard` — a dependency finding];
`…/terminal-bench/pulls/{2061,779,763,19,2470}` [see §3.2, §3.4];
`…/terminal-bench/issues/{2450,2448,2447,2443,2442,2439,2434,2430,2426,2424,2418,2417,2416,2412,2410,2409,2408,2407,2406,2405,2402,2399,2398,2394}`
[TB3 reward-hack series for other tasks];
`https://api.github.com/repos/ekellbuch/terminal-bench-2/pulls/{3,4}` [oracle pass tables];
`https://api.github.com/repos/RyanMarten/terminal-bench-3/pulls/{62,42}` [task imports];
`https://api.github.com/repos/2389-research/hex/issues/16` [TB2.0 eval results];
`https://api.github.com/repos/Ark0N/Qwen5090/issues/1` [harness findings];
`https://api.github.com/repos/prime-radiant-inc/evener/issues/306` [artefact withholding; names `gcode-to-text`
but not as an existence-only weakness];
`https://api.github.com/repos/egonSchiele/agency-lang/pulls/743` [eval framework];
`…/agency-lang/contents/packages/agency-lang/evals/terminal-bench-mini/gcode-to-text/graders.ts` [a faithful port
of the TB2 verifier; names the task but shows a content check, so not a known-row archive];
`https://api.github.com/repos/HansBug/OpenClaw-RL/issues/21` [TB2.0 run statistics];
`https://api.github.com/repos/macanderson/stella/issues/950` [preregistration];
`…/nanoPyCodeAgent/contents/…/pytorch-model-recovery-{verifier-20261021,prepared-20261024}.md` [verifier
timeouts / a 5/5 pass; no weakness claim];
`…/llm-as-a-verifier/llm-as-a-verifier/contents/…/mteb-leaderboard__D8kmscc_trajectory.json` [contains the public
grader source, not a weakness description];
`…/MaxInGaussian/pi-plans/contents/…/gcode-to-text__p6Mmm8b/result.json` [run result];
`…/xln3/tbench-test/contents/runs/…/gcode-to-text/…/results.json` [run result];
`…/Terranimus/TerranSoul/contents/benchmark/terminal-bench-2.1/terminal-bench-curriculum.md` [general agent-failure
methodology; names `gcode-to-text` only in a task-similarity list];
`…/evalstate/fast-agent/contents/docs/benchmark_data/runs/luna-max-6h.json` [run data; no weakness language];
`https://api.github.com/repos/tigicion/dao-code/contents/scripts/verify-tunemjcf-introspect.ts` [the contents API
returns base64, so the archived copy is the raw URL instead];
`https://api.github.com/repos/laude-institute/terminal-bench-2` [redirects to `harbor-framework/terminal-bench-2`];
`https://api.github.com/repos/terminal-bench/terminal-bench` [404 — that repo name does not exist];
`https://api.github.com/repos/laude-institute/terminal-bench` [redirects to `harbor-framework/terminal-bench-1`].

## 5. The frozen counter accepts these rows (executed)

I rebuilt the counter's own view of the evidence in a scratch lane (`corpus/evidence/round53/fetched/`,
`prior-art.json`, `tests-index.json`), imported the **frozen** `plans/round53_c1_triage.py` unchanged and called
its own `leg_prior_art`:

```
leg_prior_art ok = True
  PRIOR-ART rows=4 tasks_covered=4/4 known=1 new=3 urls=4 rejected=0 target: urls>=3 new>=1
```

Every archive's first line is `SOURCE-URL: <the public url I actually fetched>` and equals the row's `url`; every
quote is 8–25 words (counter whitespace tokenisation) and is present verbatim in its archive; every phenomenon-new
archive and every sweep body was tested with the counter's own `names_task()` (task id **and** all of that task's
test names) and none names them; the four sweep files of each phenomenon-new row have four distinct sha256.

## 6. Files produced (absolute paths)

* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1PriceScoutD.md` — this report.
* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1PriceScoutD/prior-art-part.json` —
  the deliverable: a JSON list of 4 rows
  (`task`, `verdict`, `url`, `fetched`, `fetched_sha256`, `quote`, and `sweep` on the three phenomenon-new rows).
  `fetched` / `sweep[].file` are paths **relative to the lane root**:
  `.ufo/waves/round-53/w3/C1PriceScoutD/fetched/<file>`.
* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1PriceScoutD/fetched/` — 23 archives
  (4 row archives, 3 supporting `extra-*` archives, 16 sweep archives) + `SHA256SUMS` (sha256 of every archive).
* Scratch (deleted at exit): `/fast/scratch/hyaku/kengaku-r53/C1PriceScoutD/` — the lane clone, the raw search
  dumps, the candidate fetches and the synthetic lane used for the counter re-run.

### Integration instructions for the L1 (I did not write `corpus/evidence/round53/` myself, by instruction)
1. `cp .ufo/waves/round-53/w3/C1PriceScoutD/fetched/<file> corpus/evidence/round53/fetched/` for the 4 row archives
   and the 12 sweep archives that the 3 phenomenon-new rows reference (the `extra-*` archives are supporting
   evidence and may be copied too if the L1 wants them in the fetched pool).
2. Rewrite the `fetched` and `sweep[].file` paths of my 4 rows to
   `corpus/evidence/round53/fetched/<file>`; the sha256 values stay valid because the file bytes do not change.
3. Merge the 4 rows into `corpus/evidence/round53/prior-art.json` (one row per confirmed task, A3 rule 3).
4. `corpus/evidence/round53/fetched/` must contain the archives — the counter's `inside()` rejects any path outside
   that directory, so the row paths cannot stay under `.ufo/`.

## 7. Tooling

No installs, no upgrades, no `pacman` transactions (the host-wide pacman guard was respected). Tools used, all
already present: `gh` 2.102.0 (official GitHub CLI binary in `~/.local/bin`, authenticated as `VeigaPunk`, scopes
`gist, read:org, repo, workflow`), `curl` 8.23.0, `python3` 3.14.8, `jq` 3.1.1 (jaq), `git` (system). The GitHub
token was read into a shell variable from the keyring and used only as an HTTP header; it was never printed and
never written to disk. `gh api --paginate` and `gh api` with `-f` were used for reads only.

`tool: gh api -X GET "search/issues" -f q=… — a quoted phrase with hyphens is tokenised by GitHub, so `"pytorch-model-recovery"` also matches items containing only "pytorch"/"model"/"recovery"; the hit counts (150 / 543 / 1381 / 88) are therefore loose. Every sweep I archived is a zero-result query, and every hit was re-checked with the counter's own token-boundary regex before being treated as "naming" the task.`
`tool: gh api "repos/laude-institute/terminal-bench-2" — the repository has been renamed; the API transparently
redirects to harbor-framework/terminal-bench-2 (and laude-institute/terminal-bench → harbor-framework/terminal-bench-1).
Repo-name redirects do not affect the archived SOURCE-URL headers, which use the current canonical names.`

## 8. Notes for the L1 / other pricing seats

* The tracker namespaces moved: `laude-institute/terminal-bench-2` → `harbor-framework/terminal-bench-2`,
  `laude-institute/terminal-bench` → `harbor-framework/terminal-bench-1`, and the current 1.0-lineage tracker is
  `harbor-framework/terminal-bench`. A sweep written against the old owner names still resolves, but the archived
  `SOURCE-URL` should use the canonical name.
* The lane repo itself is public on GitHub (`VeigaPunk/kengaku-shokunin`): GitHub code search for
  `test_tuned_model_exists` already returns `.ufo/waves/round-53/claims/c1-candidates.txt` from the lane. Noted as
  an observation only; it does not change any verdict above, but it is worth the L1 knowing that round-53's own
  artefacts are publicly indexed (a contamination risk for any later "is this documented publicly?" question).
* The richest public relatives of this phenomenon — useful if another seat needs a *general* primary that names no
  task at all — are: `harbor-framework/terminal-bench-1#455` (“Adds an agent that does nothing. Useful for
  verifying that the tests don't pass on their own”), `harbor-framework/terminal-bench-1#1020` (“sudo-llvm-ir weak
  test”), `harbor-framework/terminal-bench-1#1086` (“Test that the output file exists and is correct…”),
  `harbor-framework/terminal-bench-2#74` (vacuous `os.path.exists`-guarded tests),
  `harbor-framework/terminal-bench-2#67` (“make-doom-for-mips passes without a DOOM binary built”), and
  `adeotek/coding-agent-bench#11` (the oracle/nop gate over all 89 TB2 cells).
