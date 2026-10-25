# Round 13 scout — which offline commands are current, and which commands only look current

Seat: `R13SurfaceScout` (leaf advisory L2, lane-dispatched; not an outside
non-author review). Baseline commit `3f31e54c6e7aeddef13db11985b3c7a9dad9e0cf`.
Read-only reconnaissance: this file is the only artifact I wrote. No script was
executed, no build/lint/test/formatter was run, and the receipt's eight paths
and `:34113/health` were not re-probed. One filesystem fact was measured
because seven script defaults spell the repo root with a lowercase `projects`:

- `test -e /home/vgpnk/projects` → **false**; `test -e
  /home/vgpnk/Projects/shokunin/kengaku-shokunin` → **true**.

Everything below is either read from a named line or that single measurement.

## 0. Method and evidence boundary

Files read (relevant sections only): `PROVINCE.md:8-20,83-93`;
`SKILL.md:1-30,228-245,478-512`; `SCORECARD.md:52-110,149-215,272-364`;
`LOG.md:16-25`; `SHONEN.md:9-12`; `corpus/README.md:1-48,72-138`;
`corpus/lessons/round-13-coverage.md`; `corpus/lessons/round-16-recensus.md:1-40`;
`corpus/evidence/round13-coverage/{surface-receipt.json,dispatch.json,r13-planner.md,baseline-initial.json}`.
Static enumeration of **all 35** `.py`/`.sh` files under `corpus/evidence`
(absolute string literals, `os.environ.get` defaults, endpoint hosts, `/tmp`,
`/proc`). Advertised-command sweep pattern
`(python3|bash) <path>\.(py|sh)` over `SKILL.md PROVINCE.md SCORECARD.md LOG.md
SHONEN.md AGENTS.md corpus/README.md corpus/knowledge corpus/lessons`.

Inherited and accepted without rerun: the eight absent paths, one
connection-refused endpoint, `knowledge 23/23`, `lessons 18/17` missing
`round-16-recensus.md`, `candidates=12`, `unmarked=12` (`surface-receipt.json`).
A retained digest is not original bytes; a committed response is not a live
model.

## 1. Current supported offline entrypoints — the safe bound

Resolution basis is the line that decides where the command looks for input.
All of these are stdlib-only, endpoint-free, and resolve from the script's own
location, so they work from any cwd and after any repo relocation.

| Command (as advertised) | Resolution basis | Advertised at |
|---|---|---|
| `python3 grader.py` (repo root) | `HERE = os.path.dirname(os.path.abspath(__file__))` + `DEFAULTS{...}` beside it — `grader.py:63-77`; no `--src`, no host path | `PROVINCE.md:19`; `corpus/README.md:17,95-101`; `SKILL.md:486-489`; `SHONEN.md:10`; `SCORECARD.md:194-195` |
| `python3 grader.py --selftest` | same, temp copies; exits 0 only when each corruption is caught with its expected check-id | as above |
| `python3 corpus/evidence/round12-ladder/recompute_r12.py [--selftest \| --out P]` | `HERE`/`_PARENT` then a candidate-dir search — `recompute_r12.py:115-118` | `corpus/knowledge/bench-arena-round12-ladder.md:186-187,253-255` |
| `python3 corpus/evidence/round11-power/recompute_r11.py [--selftest]` | `HERE` + `_CANDIDATE_DIRS` — `recompute_r11.py:61-62`; `--results` defaults to the committed jsonl (`:853`) | `corpus/knowledge/bench-arena-round11-power.md:100-102` |
| `python3 corpus/evidence/round13-ack-state/audit_ack_schedule.py [--selftest]` | `ROOT = Path(__file__).resolve().parents[3]` — `:15`; hermetic, no endpoint (`LOG.md:20`) | `LOG.md:20` |
| `python3 corpus/evidence/round13-ack-state/analyze_ack_state.py [--input P] [--selftest]` | `ROOT` — `:18`; `DEFAULT_INPUT = ROOT / "corpus/evidence/round11-power/results-r11.jsonl"` — `:19` | `LOG.md:20` |
| `python3 corpus/evidence/round12-ladder/power_r12.py` | `HERE`/`ROOT` from `__file__` — `:32-33`; reads committed bytes | `corpus/knowledge/bench-arena-round12-ladder.md` |
| `python3 corpus/evidence/round12-ladder/predict_r12.py` | `HERE`/`ROOT` — `:31-32`; **writes** prediction files into `HERE` (`:305-310,475-476`) — offline but not read-only | same |
| `python3 corpus/evidence/round10-fleet/probe_ref.py <r8j> <r8l> <r9j> <r9md>` | explicit `sys.argv[1:5]`, no default at all — `:47` (fewer than 4 args → `ValueError`); the historical run used the `/tmp/kengaku-r10/` copy (`r10-mutation-sh.md:8`) | `r10-mutation-sh.md:280,350`; `INTEGRATOR-NOTES.md:21` |
| `python3 corpus/evidence/round11-fleet/recompute_r11_draft.py`, `round12-fleet/recompute_r12_draft.py`, `round12-fleet/grader_r12_draft.py`, `round11-fleet/grader_r11_draft.py` | own-location resolve (`recompute_r12_draft.py:16`; `grader_r12_draft.py:114-130`) or fixture-only selftest — draft lineage artifacts later folded into `grader.py` | in-file usage only |
| `python3 corpus/evidence/round11-fleet/mock_server_r11.py` / `round12-fleet/mock_server_r12.py [port]` | binds `127.0.0.1` only (`mock_server_r11.py:4`) with `sys.argv[1]` port default 18113/18114 (`mock_server_r12.py:21`) — fixtures, never `:34113` | `SCORECARD.md:142`; `r11-mock-smoke.md` |

`corpus/README.md:17-23` states this bound correctly ("Historical experiment
scripts retain their capture-time host defaults and are not current entry
points"), and `corpus/README.md:104-108` correctly caveats the one cwd-bound
sidecar (`predictions-r9.sha256.repo`, round-10 critic F2).

## 2. Historical scripts carrying capture-time absolute host defaults

### 2a. Dead repo-root default (lowercase `projects`) — 7 functional defaults, 6 files

The audit line in `corpus/lessons/round-16-recensus.md:38` ("8 evidence-script
defaults opening `/home/vgpnk/projects/...`") refines to **8 token occurrences
in 6 files: 7 functional defaults + 1 usage comment**. Every one of the 7 is
dead on this host (§0), and each is either a bare `open()` or the root of a
joined path, so the affected scripts cannot run as committed.

| File:line | Default | Guarded? |
|---|---|---|
| `corpus/evidence/round9-fleet/test_harness.py:23-24` (`R8`, `SRC`) | `…/projects/…/round8-horizon/{results.jsonl,horizon.py}` | `SRC` use is inside `try/except` (`:261-279`); `R8` open at **`:299` is unguarded** → `FileNotFoundError` |
| `corpus/evidence/round9-fleet/analyze.py:5-6` | `REPO = …/round8-horizon`, `open(f"{REPO}/results.jsonl")` | unguarded |
| `corpus/evidence/round10-fleet/recompute_r8.py:5-6` | `P = …` then `open(P)` | unguarded |
| `corpus/evidence/round10-fleet/recompute_r9.py:5-6` | `P = …` then `open(P)` | unguarded |
| `corpus/evidence/round10-fleet/schema_probe.py:13-16` | `REPO = …` + `os.path.join(REPO, …)` | unguarded |
| `corpus/evidence/round10-fleet/mutate_test.sh:31` | `REPO="${1:-…/projects/…}"` | falls back to `SKIP … not found` exit 3 (`:33-34`) — degrades, does not crash |
| `corpus/evidence/round10-fleet/mutate_test.sh:9` | usage comment only | n/a |

### 2b. Live-endpoint default — needs the refused `:34113`

`horizon.py:11-12` and `replicate.py:11-12` hardcode
`BASE="http://127.0.0.1:34113/v1/chat/completions"`, `OUT="/tmp/bench-r8"`.
`probe_r11.py:20-21` and `probe_r12.py:24-25` make both env-overridable
(`KENGAKU_R1{1,2}_BASE`/`_OUT`); **`run_r11.py:32` and `run_r12.py:47` hardcode
`HOST` with no override** (`r11-mock-smoke.md:94-97` records exactly this, which
is why the mock smoke had to use an `http_proxy`). `grader_r11_draft.py:1069`
and `grader_r12_draft.py:3341` only *emit* a descriptors fixture carrying the
endpoint string — they never call it.

### 2c. Session-`/tmp` state — no committed input at those paths

`horizon.py:12`, `replicate.py:12`, `run_r9.py:2-4` (`sys.path.insert(0,
'/tmp/kengaku-r9')`, imports `replicate` from `/tmp`), `analyze_b.py:4`,
`analyze_b2.py:3`, `analyze_b3.py:3`, `probeA.py:2`, `probeC_grader_check.py:32`
(all `open('/tmp/bench-r8/results.jsonl')`), `mutate_r11.sh:4` (`/tmp/r11-mut`),
`precheck_r12.py:53`, `recompute_r12_draft.py:2953` (`/tmp/kengaku-r12*`).
Consistent with `PROVINCE.md:18` ("nothing headline-bearing cited from `/tmp`"):
their decisive numbers were re-landed or recomputed by the §1 entrypoints.

### 2d. Evidence *bytes* carrying a dead absolute path (not a default)

`corpus/evidence/round12-ladder/analysis_r12.md:66` — stored, md5-pinned
(`grader.py` r12 pins) — reads `Generator source:
/home/vgpnk/projects/shokunin/kengaku-shokunin/corpus/evidence/round12-ladder/probe_r12.py`,
i.e. the lowercase spelling. Regeneration on this host emits the uppercase
resolving path; the one-line difference is the filed F-R12-1
(`corpus/knowledge/bench-arena-round12-ladder.md:195-199`). This is archival
provenance, **not** a runnable default: it must not be repointed without a
recorded ruling. Recording it here so "missing absolute host default" is not
read as a script-only class.

## 3. Commands falsely advertised current

Each item names the advertised command, the fact that makes it non-current, and
the standing substitute. I did not execute any of them.

1. **`python3 corpus/evidence/round9-fleet/test_harness.py` → exit 0,
   50 cases, `38 PASS / 12 defect candidates` — `SCORECARD.md:70`** (round-9
   operability row). The advertised invocation resolves to a committed script,
   so it reads as current, but the script's own defaults are the dead lowercase
   paths (`:23-24`) and its docstring says `Run: python3
   /tmp/kengaku-r9/test_harness.py` (`:19`); the blast-radius block then opens
   `R8` unguarded (`:299`). Confidence **medium-high**: static (dead default
   measured, open unguarded), not executed. No erratum covers this default drift
   — the round-10 F1/F2/F3 errata cover the file count, the `.sha256.repo` cwd
   bug, and an over-claim about *where* r9 re-verification lived. Substitute:
   `python3 grader.py`, whose r8 layer replays the same records
   (`SCORECARD.md:160`).
2. **`BENCH_ROOT=<scratch> bash ~/archive/bench-arena/grade.sh <label>` —
   `SKILL.md:330`** (present-tense, inside the current production checklist:
   "Grade identically"), repeated as a cited-source line at **`SKILL.md:568`**
   and as a source row at **`PROVINCE.md:13`**. `~/archive/bench-arena` is
   absent per the inherited receipt, and `~/bench-arena` is absent too, so the
   advertised grader/runner cannot be invoked today. Confidence high for the
   path status (inherited receipt, not re-probed); the *historical* no-drift
   claim is not contradicted.
3. **`cd ~/bench-arena && BENCH_ROOT=/tmp/X bash grade.sh <label>` —
   `corpus/knowledge/bench-arena-round5-battery.md:107`** and the same recipe
   at **`corpus/knowledge/bench-arena-fresh-run.md:67`**;
   **`BENCH_ROOT=/tmp/bench-r6 bash ~/bench-arena/grade.sh …` —
   `bench-arena-round6-stability.md:99`**;
   **`BENCH_ROOT=/tmp/bench-r7 bash ~/bench-arena/grade.sh …` —
   `bench-arena-round7-scaffold-ablation.md:130`**;
   **`ln -s ~/bench-arena/tasks/$t …` — `bench-arena-fresh-run.md:65`**.
   Two of these files (`bench-arena-fresh-run.md`, which is a receipt
   candidate; `local-bench-arena.md:3`) are inside the twelve-candidate set, the
   other three are not (see §4). An annotation that marks the *source* row
   unavailable must not be read as making the *command recipe* runnable; the
   recipes still name a path that does not resolve.
4. **`python3 evidence/round13-coverage/coverage_census.py` (from
   `corpus/`) — `corpus/README.md:18`.** Named by the parent as a current
   offline entry point, but not present in
   `corpus/evidence/round13-coverage/` at my 2026-10-15T01:54 listing (dir held
   `baseline-initial.json`, `dispatch.json`, `r13-planner.md`,
   `surface-receipt.json`). Owned by `R13CoverageCensus`; this is **not** a
   claim of absence — it is a close-out check: if the file does not land, the
   README advertises a missing command, the exact failure mode of item 1.
5. **Adjacent stale-current text, not a command default:**
   `SCORECARD.md:302` ("All 149 checks recompute stored-vs-derived from
   committed bytes", present tense, undated) against the current gate's 733
   (`SCORECARD.md:160`; `LOG.md:21-22`; `corpus/lessons/round-16-recensus.md:8-10`).
   Same debt already named in the round-16 audit. Out of my lane to edit.

**Deliberately not flagged as false-current** (checked, they are correct as
written): `SKILL.md:486-489` (current prescription — "defaults resolve beside
the script", with the real flag list); `SKILL.md:499` and `LOG.md:17`
(`CHECKS n=149` are explicitly dated round-10 records, not present-tense
claims); `SCORECARD.md:194-195`; `PROVINCE.md:19`; `SHONEN.md:10`;
`corpus/README.md:95-108`; `SCORECARD.md:128,142` (round-10/round-11 historical
rows). `SKILL.md:229-241` (present-tense `~/archive/bench-arena/…` eval-battery
row) and `PROVINCE.md:12-16` are source-availability claims inside the
twelve-candidate annotation lane (`R13KnowledgeSources`), not script defaults.

## 4. Does the twelve-source selection omit other historical claims?

**Reproduced first, then measured.** Re-running the receipt's rule
(`first 12 lines match llm-wiki|wiki/|~/bench-arena|~/archive/bench-arena|~/.bailian|~/Projects/bounties`)
returns **exactly the 12 files** in `surface-receipt.json.source_candidates`, in
the same order. So the metric is a frozen candidate list — and it is narrower
than the citation class it stands for:

| Class | Measured | Selected by the rule? |
|---|---|---|
| Knowledge docs whose **first 12 lines** match the alternation | **12** | yes (the metric) |
| Knowledge docs matching the alternation **anywhere** | **16** | no — 4 missed: `bench-arena-round5-battery.md:104,107`; `bench-arena-round6-stability.md:99`; `bench-arena-round7-scaffold-ablation.md:130`; `bench-arena-task27-timeout-anatomy.md:84` |
| Knowledge docs citing an absent surface the alternation **never matches** — all 9 cite `127.0.0.1:34113`; `bench-arena-fresh-run.md:10,13,15-16` also `qwen-coder.service` + `opencode.json`, `bench-arena-round7-scaffold-ablation.md:10,133` also the opencode config | **9 of 23** | no — and here the gap is the rule, not the receipt: the receipt's `paths`/`endpoint` do record `:34113`, the unit, the jinja template and `/proc/1299/cmdline`. Only `~/.config/opencode/opencode.json` and `~/wikillm/llm-wiki` are outside the receipt entirely (the latter separately documented absent at `PROVINCE.md:12`, `SKILL.md:8-12`) |
| Same-class citations outside `corpus/knowledge` | ~7 script defaults (§2a) + living docs (`SKILL.md:229-241,330,565-571`; `PROVINCE.md:12-16`; `SCORECARD.md:70,302`; `LOG.md:16-22`; `SHONEN.md:12`; `corpus/README.md`) + lesson files + evidence `.md` files | no (unit is a knowledge document) |
| Unit definition | 1 document; the round-16 audit's unit is 1 citation occurrence / 1 token-hit | different unit, scope and revision |

**Therefore the honest limitation to state alongside any twelve-source claim:**

> Source-status coverage is bounded to the **12 named knowledge documents** in
> the receipt. At least 4 further knowledge documents cite the same
> unavailable-source tokens outside the rule's 12-line window, at least 9 more
> cite unavailable surfaces the rule's alternation does not match at all, and
> the 6 historical scripts with dead absolute defaults, the living
> documentation rows, lesson files and evidence documents are outside the unit
> entirely. None of these were re-classified here.

No `61 → 0`, no percentage of the wider audit, no "no stale citations remain"
and no absence-everywhere statement is supported by this measurement — the
round-16 audit's 61-live/369-token classification was not reproduced and its
revision is not the frozen comparison point.

## 5. Confidence and remaining unknowns

- **High** (read from source or measured): the §1 resolution basis per file;
  the 8 dead lowercase tokens = 7 functional + 1 comment in 6 files; the two
  repo path spellings; the 12-candidate rule reproducing exactly; the 4 and 9
  document counts in §4.
- **Medium-high**: item 1's non-runnability (static only); item 2/3 depend on
  the inherited receipt's path status, which I accepted rather than re-probed.
- **Unknown / not established:** whether an earlier host had a lowercase
  `projects` root (would explain how the §2a scripts ever ran — not
  reconstructible from in-repo records); whether an advertisement of a §2a
  script exists in a file my sweep pattern did not cover (pattern and file set
  are named in §0); whether any historical script outside `corpus/evidence`
  exists in this repo (the enumeration covered `corpus/evidence` only, plus the
  specific advertised-command sweep); and whether `coverage_census.py` lands.
- **No claim is made** about restored sources, original bytes, model identity,
  novelty, or any score. Coverage's declared-but-unresolvable-surface cap still
  applies to whatever the parent integrates.