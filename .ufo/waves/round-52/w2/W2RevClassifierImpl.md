# W2RevClassifierImpl — wave 2 (falsify) — R52-C1 counter as a measurement

Seat: `W2RevClassifierImpl` (reviewer, read-only). Lane: `kengaku-shokunin`. Subject:
`plans/round52_c1_grader_audit.py` (429 lines), read against `plans/round-52-claims.md` §C1 and
Amendments A1, A2, A4, A5. Lane tree: **not modified** (counter run with `PYTHONDONTWRITEBYTECODE=1`;
every attack ran on a copy under scratch, since removed). No tools installed; stdlib `python3` and
`curl` only. Receipts (scripts, outputs, pinned upstream tree) are in `receipts/` beside this file.

## Bottom line

The counter reproduces the claims file's *live* state correctly, and its capture **bytes** are
genuinely correct (they match the pinned upstream tree). But its predicate is **not a measurement of
the frozen claim**. Every leg that is supposed to certify a *receipt* (confirmation, prior-art) can be
passed by a wrong input, the population's own count fields are self-declared, the digest leg trusts
`SHA256SUMS`, the per-test classifier misses hand-confirmed presence-only tests, and the A5 additive
predicate can be made to pass while a real primary grader is missing. The literal `PREDICATE R52-C1`
still exits 1 in every attack I could make on the *real* population (the operator exclusion keeps
`present=183`), so the kill rule as written is not defeated today; the defects are in what the
instrument would accept once receipts exist.

## Live reproduction (lane tree, read-only)

```
TASKS total=89 records=89 classified=88
CAPTURES expected=184 present=183 mismatched=0
CLASS V1=2 V4=0 V2=53 V3=31 V0=3
TESTCLASS presence_only_tests=33 tasks_with_presence_only=27
CANDIDATES total=29          (27 via P1 tests + 2 via file-level V1 only)
CONFIRMED new=0 []
PRIOR-ART ok=False urls=0
LABELS agree=0 of 0
PREDICATE R52-C1 fail        (exit 1)
A5 EXCLUDED listed=1 digest_pinned=1 tasks=['sanitize-git-repo']
A5 CAPTURES present+pinned_excluded=184 of 184
A5 TASKS classified+excluded=89 of 89
PREDICATE R52-C1-A5 fail
--selftest: failures=0 (exit 0)
```

Corroborating facts (all measured): `corpus/evidence/round52/` contains **only `graders/`** — there is
no `confirmations.json`, no `prior-art.md`, no `labels.json` at this tip, so legs 3–4 are unsatisfied
for a reason independent of any attack.

## Per-leg verdicts

Verdict key: **sound** = a wrong input cannot pass it; **vacuous** = a specific wrong input passes it
(exact input given); **drift** = the code departs from the frozen text.

| # | Leg | Verdict | Exact input that passes it (measured) |
|---|---|---|---|
| 1 | CAPTURES expected | **vacuous** | `expected` is `pop["capture_file_count"]`, a self-declared field. The code never asserts 184. Fixture F7: drop `sanitize-git-repo` from `tasks` and `capture_population`, set `task_count=88`, `capture_file_count=182`, add two valid receipts + 3 URLs → `CAPTURES expected=182 present=182`, `TASKS total=88`, **`PREDICATE R52-C1 pass`, exit 0.** |
| 1b | CAPTURES digest | **vacuous vs deliberate edit; sound vs drift** | `load_sums` reads `SHA256SUMS` (same tree, untrusted). F8: edit `mteb-leaderboard/tests/test_outputs.py` and rewrite its SHA line → `mismatched=0`. F8b: leave stale line, *append* `<newdigest>  ./<path>` → `load_sums` is last-wins (`out[path]=…`) → `mismatched=0`. Current bytes are sound: see "Anchor check" below. |
| 2 | TASKS classified | **vacuous** (count) | `tasks_total = pop["task_count"]` and `len(records)` come from the same JSON; F7 shows 88/88 passes. |
| 3a | CONFIRMED — new-task guard | **vacuous** | `lane_read_tasks` derives the read set from **filenames currently in the tree** (`tb2-*-grader.md`), not history. F4: delete `corpus/knowledge/tb2-password-recovery-grader.md` → `CONFIRMED new=2 [... 'password-recovery']`. Control with the entry present → `REJECTED password-recovery not-a-new-task`. |
| 3a' | CONFIRMED — new-task guard, false rejections | **drift / hazard** | F5: an L1 entry named by the convention, `tb2-mteb-leaderboard-grader.md`, makes a valid confirmation `REJECTED … not-a-new-task`. The guard's outcome depends on file naming. |
| 3b | CONFIRMED — `reader` independence | **vacuous** | Only `c.get("reader")` truthiness is checked (`:312`). No independence check of any kind. |
| 3c | CONFIRMED — `confirmed` | **vacuous** | `not c.get("confirmed")` is truthiness. F1: both receipts `"confirmed":"false"` (a string) → `CONFIRMED new=2 ['mteb-leaderboard','multi-source-data-merger']`. |
| 3d | CONFIRMED — hardening (i) candidate membership | **vacuous (broader than A1)** | Code: `candidate = bool(p1) or cls in ("V1","V4")` (`:193`). A1 defines a vacuity candidate as "≥1 of its tests is P1". F3: `pytorch-model-recovery` and `torch-tensor-parallelism` have **zero** P1 tests and enter the queue only via file-level V1, which A1 says misdescribes them; both receipts pass `CONFIRMED new=2`. |
| 3e | CONFIRMED — hardening (ii) quote verbatim | **vacuous** | `quote not in grader.read_text(...)` (`:316`) is a bare substring test: no minimum length, no line location, not tied to the accused test. F2: `"quote":"assert"` for two tasks → `CONFIRMED new=2`. (The reject path for an absent quote is by code reading only; not separately exercised.) |
| 4 | PRIOR-ART ≥3 distinct URLs | **vacuous** | `len(set(URL.findall(text))) >= 3` is exact-string distinctness. The regex keeps trailing `>`, `.` and fragments. F6: `https://github.com/harbor-framework/terminal-bench-2`, the same with `/`, and `<https://…>` → `urls=3`, `ok=True`. Nothing checks fetched/access date, host, per-finding `phenomenon-new` / `phenomenon-known` verdict (so the frozen **score rule is not checked by any leg**). F1/F2/F3 also show `PRIOR-ART ok=True urls=3` on a 3-URL synthetic file. |
| 5 | LABELS (evidence only) | **vacuous** | Rows whose `class` is outside `CLASS_ORDER` are skipped silently and the denominator shrinks. F10: 5 rows (2 with label `P1`, one duplicate) → `LABELS agree=3 of 3`. |
| A5 | CAPTURES (additive) | **launderable** | `excluded_captures` takes the first `Excluded path` in `EXCLUDED.md`, requires only that it be absent and its digest equal the `SHA256SUMS` line, and never checks population membership. F9: `EXCLUDED.md` names fake `made-up-task/tests/test_outputs.py` (SHA line appended) with sanitize still absent → `A5 CAPTURES present+pinned_excluded=184 of 184`. |
| A5 | full `PREDICATE R52-C1-A5` | **launderable** | A5 TASKS blocks F9 (`88 of 89`) because the excluded path is not a primary grader. F9b: delete the **real** primary `bn-fit-modify/tests/test_outputs.py`; replace sanitize's bytes with fabricated ones and rewrite its SHA line; re-point `EXCLUDED.md` at bn-fit → `A5 CAPTURES 184 of 184`, `A5 TASKS 89 of 89`, **`PREDICATE R52-C1-A5 pass`**. The literal predicate still fails (exit 1), so the kill rule stands; A5 as an additive report does not. |

## Classification leg — measurements

### Drift from the frozen vocabulary (undisclosed; A1 says "same marker vocabulary")

- `CONTENT` adds `|assert.*\bin\b` (line 36). Not in the frozen content list.
- `PRESENCE` adds `\b` anchors and `os\.path\.isfile`.
- `BEHAVIOUR` writes `curl ` with a trailing space (frozen: `curl`). No grader in the population has a bare `curl` token, so no effect today.
- Per-test `BEHAV_T` adds `multiprocessing|mp\.|threading|dist\.`. `mp\.` is unanchored and matches `tmp.`; `dist\.` matches `dist.` attributes. Removing the extras leaves the P1 count unchanged (27 / 33), but they change P-classes.
- Per-test `VALUE` (P3 "content/value") is a new vocabulary with `\bin\b` and `[<>]` — see the defect below.

Effect on file-level classes (`sens.py`): **3 tasks** differ from the frozen-text rule.

| task | impl | frozen text | cause |
|---|---|---|---|
| bn-fit-modify | V3 | V1 | impl `assert.*\bin\b` (line 39 `assert all(col in …)`) |
| portfolio-optimization | V3 | V1 | impl `assert.*\bin\b` (line 49 `assert any(… for ext in …)`) |
| distribution-search | V0 | V1 | frozen text matches the **def name** `def test_distribution_file_exists():`; impl's `\b` does not |

So the frozen literal text itself matches function *names* as presence checks, and the implementation
diverges from it in both directions without disclosure. Candidate-queue delta is 2 tasks (frozen-literal
V1 set = 5, impl V1 set = 2).

### Per-test defects (false negatives: presence-only tests escape the queue)

Measured on the 89 primary graders, 305 test blocks (`sens.py`, `variants.py`):

1. **English "in" in comments/docstrings is a value comparison.** `VALUE` matches `\bin\b` anywhere in the
   block, including comments. 14 tests are P3 *only* because of docstring/comment text. Removing
   docstrings and comments: **36 tasks / 46 P1 tests** versus impl **27 / 33**.
   Example: `pytorch-model-recovery::test_model_file_exists`, whose body is a single presence assert,
   is P3 because of the comment `# Reference the directory the agent operated in (the WORKDIR …)`.
2. **Helper defs are absorbed into the preceding test.** `split_tests` cuts only at `^def test_`, so a
   following non-test helper belongs to the previous test's block. 9 test blocks in 7 files absorb a helper.
   `torch-tensor-parallelism::test_parallel_linear_exists` is P2 because `dist.init_process_group` sits in
   the absorbed `_setup_process_group`. Splitting at any top-level `def` (and removing docs) makes it **P1**.
   `tune-mjcf::test_tuned_model_exists` moves P3 → P1 under the same fix.
3. **Presence vocabulary gap.** `isdir(`, `glob(`, `listdir(`, `os.access(`, `os.stat(`, `getsize(` are
   not presence calls. 11 assert-bearing non-P1 test blocks contain them (examples:
   `adaptive-rejection-sampler::test_has_test_function` P3, `compile-compcert::test_compcert_exists_and_executable` P3).
   An extended-presence variant gives 30 tasks instead of 27.

### The A1 hand-read does not reproduce under the amended rule

A1 names `test_model_file_exists` (pytorch-model-recovery) and `test_parallel_linear_exists`
(torch-tensor-parallelism) as presence-only per test. The counter classifies them:

| test | impl split | impl, docs/comments removed | any-def split, docs removed |
|---|---|---|---|
| pytorch-model-recovery::test_model_file_exists | P3 | P1 | P1 |
| torch-tensor-parallelism::test_parallel_linear_exists | P2 | P2 | P1 |

Neither test is a P1 under the implemented rule. Both tasks are in the queue **only** via file-level V1,
which A1 itself retracts for these two graders. The counter's own output therefore does not support A1's
observation; the amendment's "per-test" unit is not what the code measures.

### Anchor check (digest leg substance)

- Pinned upstream tree (`api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88…?recursive=1`,
  saved as `receipts/upstream-tree-2fd12b88.json`): **184 grader-like blobs** (94 `test_outputs.py`, 89
  `test.sh`, 1 `verify.sh`). The population's 184 paths are **exactly equal** to that set.
- Local captured bytes, git blob SHA-1 (`sha1("blob <n>\0"+bytes)`) versus upstream blob sha: **183 match,
  0 mismatch, 1 absent** (sanitize).
- Upstream blob for `sanitize-git-repo/tests/test_outputs.py` = `3269e74e727fda61c936ca34b8f3bfaacf199dda`,
  equal to the `git blob sha1` written in `EXCLUDED.md`.
- `SHA256SUMS`: 184 lines, no duplicate paths (today), agrees with the local bytes for 183/183.

So the bytes are right. The counter does not check them against the pin; it checks them against a file
in the same tree. Fixtures F8/F8b show that is enough to be fooled.

## Fixture battery (every fixture: scratch copy of `plans/` + `corpus/evidence/round52/` + `corpus/knowledge/`, counter run with `--lane <copy>`)

| fixture | edit | observed | passes? |
|---|---|---|---|
| F0 base | none | `CONFIRMED new=0`, `PRIOR-ART ok=False urls=0` | baseline reproduces live state |
| F1 | both receipts `"confirmed":"false"` (string) | `CONFIRMED new=2`, `PRIOR-ART ok=True urls=3` | A5 pass; literal fail only on 183/184 |
| F2 | quotes `"assert"` | `CONFIRMED new=2` | A5 pass |
| F3 | two V1-only tasks, quotes from their presence lines | `CONFIRMED new=2` | A5 pass |
| F4 | delete knowledge entry for `password-recovery` | `CONFIRMED new=2 [... 'password-recovery']` | A5 pass; control (entry present) rejects |
| F5 | new entry `tb2-mteb-leaderboard-grader.md` for a valid receipt | `REJECTED mteb-leaderboard not-a-new-task` | false rejection |
| F6 | three spellings of one repo URL, no verdicts | `PRIOR-ART ok=True urls=3` | yes |
| F7 | population shrunk to 88 tasks / 182 captures | **`PREDICATE R52-C1 pass` (exit 0)** | **yes — literal predicate** |
| F8 | graded bytes edited + SHA line rewritten | `mismatched=0` | digest leg vacuous |
| F8b | stale SHA line + appended duplicate | `mismatched=0` | digest leg vacuous |
| F9 | `EXCLUDED.md` → fake absent path, SHA line appended | `A5 CAPTURES 184 of 184`; `A5 TASKS 88 of 89` → A5 fail | partial (capture leg only) |
| F9b | real bn-fit primary deleted, sanitize fabricated, EXCLUDED re-pointed | `A5 CAPTURES 184 of 184`, `A5 TASKS 89 of 89`, **`PREDICATE R52-C1-A5 pass`** | **yes — A5** (literal still exit 1) |
| F10 | labels with out-of-vocabulary rows and a duplicate | `LABELS agree=3 of 3` (5 rows) | evidence leg vacuous |

Receipts for F0–F10: `receipts/fixtures.out.txt`, F9b: `receipts/f9b.out.txt`.

## Answers to the item's explicit questions

- **Capture-count leg (184 vs real set):** the real set is 184 (population = upstream = 183 on disk + 1
  excluded). The counter does not derive 184; it reads a declared number. Sound on today's data, vacuous
  against any self-consistent edit of the population JSON (F7).
- **Digest leg:** compared against captured bytes, yes (`sha256_bytes(cf.read_bytes())`). The reference is
  `SHA256SUMS` from the same tree and is trusted (F8, F8b).
- **Classification leg:** drift from frozen text in 3 tasks; per-test P1 under-triage (14 comment/docstring
  "in" false P3s, 9 absorbed-helper blocks, 11 presence-vocabulary misses); A1's two named tests are not
  P1 under the implemented rule.
- **CONFIRMED hardening (candidate membership):** checked, but over a broader set than A1 defines (V1/V4
  file-level admitted). Admits two tasks A1 says are not presence-only as whole graders (F3).
- **CONFIRMED hardening (quote verbatim):** a substring test with no length, location or task-binding
  (F2). Verbatim in the captured bytes, yes; a located, task-bound quote, no.
- **PRIOR-ART "distinct how?":** exact-string set after a regex that keeps `>`, `.`, fragments. Not
  distinct by host, path or source (F6).

## Residual risk and gaps

- No receipts exist at this tip, so I could not exercise the reader-independence rule in a real case;
  the attacks above use synthetic receipts in scratch copies only. Prior-art URLs in fixtures are
  `example.org` placeholders, not fetched primaries.
- The reject path of the verbatim-quote check was read, not exercised.
- I did not check C2 (registry) here; that is outside this item.
- The upstream check used a single unauthenticated GitHub API call (`curl`, exit 0, 184 grader-like blobs).

## Files (absolute)

- Report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2RevClassifierImpl/report.md`
- Item file: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2RevClassifierImpl.md`
- Receipts: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2RevClassifierImpl/receipts/`
  (`counter-live.out.txt`, `counter-selftest.out.txt`, `sens.out.txt`, `variants.out.txt`,
  `fixtures.out.txt`, `f9b.out.txt`, `upstream-tree-2fd12b88.json`, and scripts `analyse.py`, `probe.py`,
  `sens.py`, `variants.py`, `fixtures.py`, `f9b_run.py`)
- Scratch `/fast/scratch/hyaku/kengaku-r52/w2-W2RevClassifierImpl/`: removed after copying receipts.

## Commands run (all read-only against the lane)

```
python3 plans/round52_c1_grader_audit.py --lane .        # live verdict
python3 plans/round52_c1_grader_audit.py --selftest      # selftest
python3 <scratch>/analyse.py | probe.py | sens.py | variants.py   # import counter via importlib; no writes
python3 <scratch>/fixtures.py ; python3 <scratch>/f9b_run.py     # counter run with --lane <scratch copy>
curl -fsS "https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1"
```

Installs/updates: none.
