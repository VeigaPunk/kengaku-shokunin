# W2CritC1Reach — round 52, wave 2 (falsify), seat critic C1-reach

Scope: falsify R52-C1's after-state end to end (read-only). Question: can `plans/round52_c1_grader_audit.py --lane .` print `PREDICATE R52-C1 pass` without the claimed work being done? Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Lane tree, fleet repo, sibling lanes, `.ufo/state/`, `templates/`, `scripts/` and `MANIFEST.json` were not written. The only git commands run against the lane were read-only (`git -C <lane> cat-file -t`, `git -C <lane> show <rev>:path`). All fixtures lived in `/fast/scratch/hyaku/kengaku-r52/w2-W2CritC1Reach/` (now removed; receipts kept below).

## Verdict

**The attack landed. The counter can print `PREDICATE R52-C1 pass` without any grader read, any upstream fetch, or any independent reader.** Five independent routes reach `pass` (fx02, fx03, fx03b, fx03c/fx03h, fx06). The live lane, measured today, honestly prints `fail` (183 of 184 captures, 88 of 89 classified, 0 confirmations, no prior-art file). The falsification is in the instrument's reach, not in the lane's current evidence: the lane's 183 captures are genuinely upstream (blob-verified below), but the counter does not prove that.

What the PASS path requires, in full: (a) 184 files that exist and match a `SHA256SUMS` the lane itself writes; (b) a population JSON that the counter trusts as its own authority; (c) two confirmation objects with a truthy `confirmed` value and any substring as `quote`; (d) three URL-shaped strings in a text file. No grader is read by the counter as evidence of a human reading it, no URL is fetched, and no reader identity is checked.

## Live state (read-only run of the frozen counter on the lane)

Command: `python3 plans/round52_c1_grader_audit.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` (exit 1). Output: `receipts/live_verdict.txt`.

```
TASKS total=89 records=89 classified=88
CAPTURES expected=184 present=183 mismatched=0
CLASS V1=2 V4=0 V2=53 V3=31 V0=3
TESTCLASS presence_only_tests=33 tasks_with_presence_only=27
CANDIDATES total=29
CONFIRMED new=0 []
PRIOR-ART ok=False urls=0
LABELS agree=0 of 0
PREDICATE R52-C1 fail
A5 EXCLUDED listed=1 digest_pinned=1 tasks=['sanitize-git-repo']
A5 CAPTURES present+pinned_excluded=184 of 184
A5 TASKS classified+excluded=89 of 89
PREDICATE R52-C1-A5 fail
```

- Selftest (`--selftest`): `cases=6 failures=0` (`receipts/live_selftest.txt`). The selftest covers the classifier rules only; it tests none of the pass routes below.
- Per-test count `33 P1 tests / 27 tasks` reproduces Amendment A4's corrected figure.
- Population authority: `plans/round52-tasks.json` is byte-identical to its freeze-commit version: `git -C <lane> show 1315234:plans/round52-tasks.json | sha256sum` = `0230b68c666c1e0649b42d61d7121a30eedf247411642bbf397e3390436b5cfc`, same as the working file. The counter never performs this comparison.
- Upstream blob check (captures): fetched the pin tree `curl -fsS "https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1"` (1038 blobs, not truncated). For the 184 population capture paths: **match 183, mismatch 0, not in tree 0, absent 1** (`sanitize-git-repo/tests/test_outputs.py`, the operator-excluded file). The lane's captures are genuine. The counter does not check this.
- Candidate population: 27 tasks with ≥1 P1 test, plus `pytorch-model-recovery` and `torch-tensor-parallelism`, which are candidates only through the file-level `V1` rule that Amendment A1 itself calls false (see finding 4).

## Constructions: counter answer and smallest fix

Fixture = copy of the read-only inputs (`plans/`, the 183 captures, the 12 `tb2-*-grader.md` entries) with one attack applied, then the frozen counter run unmodified. Outputs: `receipts/runs/<fixture>.txt`. Builder: `receipts/build_fx.py`.

| # | construction | counter answer (measured) | leg holds? | smallest fix that rejects it |
|---|---|---|---|---|
| fx00 | no capture directory at all | `present=0`, `classified=0`, `PREDICATE fail` | yes | — |
| fx01 | only the 29 candidates' graders captured, population untouched | `present=59 of 184`, `classified=29 of 89`, `fail` | yes | — |
| **fx02** | as fx01, **population JSON rewritten** to 29 tasks (`task_count`, `capture_file_count`, `tasks`, `capture_population`) | `CAPTURES expected=59 present=59`, `TASKS total=29 classified=29`, `PREDICATE R52-C1 pass` | **no** | hard-code 89 and 184 in the counter; require `plans/round52-tasks.json` sha256 = the freeze-commit blob (`0230b68c…`, reproduced above) |
| **fx03** | all 184 present; `sanitize-git-repo/tests/test_outputs.py` replaced by a one-line stub and its `SHA256SUMS` line re-pinned to the stub; population untouched | `present=184 mismatched=0 classified=89`, `pass` | **no** | verify each capture's git blob SHA1 against a committed pin-tree listing (`receipts/pin-tree-2fd12b88.json`, 1038 blobs; today 183/183 match) and verify the listing against the freeze; stop trusting self-written `SHA256SUMS` |
| **fx03b** | as fx03; two confirmations: `reader="KengakuR52a3"` (the L1), `confirmed="false"` (a non-empty string), `quote=" "` and `quote="assert"` | `CONFIRMED new=2 ['code-from-image','mteb-retrieve']`, `pass` | **no** | require `confirmed is True`; reader ≠ author id and reader's report digest present under `.ufo/waves/round-52/w1|w2`; quote length ≥ 20 and contained in a P1 test block of that task (not merely anywhere in bytes) |
| fx03c | as fx03b with prior-art = three `example.org` URLs labelled `phenomenon-known`, no fetch | `PRIOR-ART ok=True urls=3`, `pass` | **no** | per-finding table (task · verdict ∈ {phenomenon-new, phenomenon-known} · URL · sha256 of an archived fetch under `corpus/evidence/round52/fetched/`); counter requires one row per confirmed task and prints a separate `PRIOR-ART new>=1` line for the score rule |
| fx03h | prior-art = three query-string variants of one GitHub URL, text says "phenomenon-known for all" | `urls=3`, `pass` | **no** | same as fx03c |
| fx03g | prior-art with two URLs | `urls=2`, `fail` | yes | — |
| fx03d | confirmations wrapped as `{"confirmations":[...]}` | `CONFIRMED new=0`, no REJECTED line printed, `fail` | yes, but silently | print a reason for non-list input |
| fx03e | same task twice | `CONFIRMED new=1`, `fail` | yes | — |
| fx03f | `reader=""` | `REJECTED incomplete-receipt` ×2, `fail` | yes | — |
| fx03i | `confirmations.json` absent | `CONFIRMED new=0`, `fail` | yes | — |
| fx05 | `labels.json` = the classifier's own output | `LABELS agree=89 of 89`, `PREDICATE R52-C1 pass` | predicate: yes (labels non-gating); **evidence: no** | commit `labels.json` before classifier output and bind its digest to the labrat seat's report; without that, agreement is not a blind measurement |
| fx05b | `labels.json` = all `V0` | `LABELS agree=2 of 89`, `pass` | predicate yes; evidence visible only | same |
| fx04 | delete one P1 grader (`bn-fit-modify`) and name it in `EXCLUDED.md` with its digest; sanitize left absent | `present=182`, `A5 CAPTURES 183 of 184`, `PREDICATE R52-C1-A5 fail` | yes (A5 cannot launder a second absence) | — |
| **fx04b** | as fx04 but with the fx03 sanitize stub (count restored) | literal `fail` (present 183); **`PREDICATE R52-C1-A5 pass`** | **no** | hard-code the single excluded path as `sanitize-git-repo/tests/test_outputs.py` with blob `3269e74e727fda61c936ca34b8f3bfaacf199dda` (from `EXCLUDED.md`); stop parsing an arbitrary path from `EXCLUDED.md` |
| **fx06** | `code-from-image` grader replaced by a test whose presence assert is followed by `assert _matches_reference(...)` (a helper that compares via `json.loads(...) == {...}`) | candidate `class=V3 presence_only=test_output_file_exists`; confirmed; `pass` | **no** (presence-only label on a comparing test) | inline same-file helper bodies into the calling test block; a block that calls a helper containing a VALUE marker is P3 |
| **fx07** | confirmations on `openssl-selfsigned-cert` (quote `def test_directory_structure`, a real P1 candidate) | `CONFIRMED new=2 ['mteb-retrieve','openssl-selfsigned-cert']`, `pass` | **no** | see finding 5: the never-read guard checks hand-read filenames only; the lane has run this task's nop/oracle (SCORECARD.md:1604, `nop 0/6, oracle 5/6`) |
| ctl-name-only | population with 89 names and empty file lists | `classified=0`, `fail` | yes | — |
| ctl-drop-capture | `bn-fit-modify` grader removed from honest state | `present=182`, `fail` | yes | — |

Three PASS routes need no population edit at all (fx03 + fx03b/fx03c): the forgery is one file and one SHA line. Two need only a population edit (fx02). None requires a human to read a grader or a URL to be fetched.

## Other findings (each with a measured receipt)

1. **Population and capture counts are self-referential.** `expected`, `tasks_total` and `capture_population` come from one JSON file with no digest check against the freeze (fx02). `capture_file_count` (184) is never compared with `len(capture_population)` either. Fix: constants in the counter plus a freeze-commit digest check.

2. **Digests are self-authored.** `SHA256SUMS` is written by the lane and checked only against the lane's own bytes (fx03). The honest state is currently true (183/183 blob matches), but the counter cannot distinguish it from a forgery. Fix: compare each capture's git blob SHA1 against a committed listing of the pin tree.

3. **Confirmation receipt checks are type-blind and content-blind.** `not c.get("confirmed")` accepts `"false"` and `"no"` (fx03b). `quote in grader.read_text()` accepts `" "` and `"assert"` (fx03b). The reader is only checked for truthiness, so the L1's own id passes (fx03b). The "independent second reader" leg of the frozen claim is therefore not measured at all. Fix: as listed in the table.

4. **Amendment A1's per-test rule does not reproduce its own exemplars (re-measured).** Per-test classes for the two named tests (`receipts/receipts_check2.txt`):
   - `pytorch-model-recovery::test_model_file_exists`: as-is **P3** (the comment `# Reference the directory the agent operated in` and the word `in` match `\bin\b`); with comments and docstrings blanked: **P1**.
   - `torch-tensor-parallelism::test_parallel_linear_exists`: as-is **P2** (its block runs to the next `def test_` and absorbs `_setup_process_group` with `dist.`); truncated at the next top-level def only: **P3** (docstring word `in`); truncated **and** comment/docstring-blanked: **P1**.
   - Both tasks currently reach `CANDIDATES` only through the file-level `V1` rule, which A1 disowns. Under the per-test rule alone (file-level forced to V0), both have `P1=[]`.
   - Across the 33 live P1 tests, none calls a helper that compares values; one (`write-compressor::test_compressed_file_exists`) calls `setup()`, which runs `gcc` through `subprocess`. The behaviour exclusion cannot see it because it scans only the block. This is a presence-only test by definition but hides a subprocess.
   - Fix: blank comments and docstrings by source position, end each test block at the next top-level `def`/`class`, and inline same-file helper bodies. Verified for the two exemplars (`truncated_and_stripped=P1`). Inlining is untested [INFERENCE].

5. **The never-read guard is narrower than "never read".** `lane_read_tasks()` reads only `corpus/knowledge/tb2-*-grader.md` filenames. All 12 derive to population ids (verified: none is outside the population). But SCORECARD.md:1604 records `openssl-selfsigned-cert` as a pilot with `nop 0/6, oracle 5/6`, i.e. the lane ran that task's verifier outcomes before this round, and the guard cannot see it (fx07 accepted it). [INFERENCE: the pilot used the TB2 grader bytes; the SCORECARD line gives the numbers and not the file.] Fix: rename the leg to "no hand-read entry" in the claim, or add a scan of SCORECARD/LOG run records for the task's grader.

6. **Control `c1-control-blind-class` is not reproducible as written.** The frozen control says forcing every task to V0 gives `CANDIDATES total=0`. Forcing the file-level class to V0 in-process (`classify` monkeypatched) gives **`CANDIDATES total=27`**, because candidacy is driven by the per-test P1 rule that A1 added. The control must force both the file-level class and every per-test class to P0 to reach zero (by construction, not re-run).

7. **Labels are evidence without a blind measurement.** `labels.json` copied from the classifier gives `agree=89 of 89` (fx05); all-V0 gives `2 of 89` (fx05b). The predicate correctly ignores labels, but the claim reports the agreement number as evidence, and nothing distinguishes a blind label set from a copy. Fix: commit labels before classifier output and bind their digest to the labrat report.

8. **A5 cannot be laundered alone, but can be with the sanitize stub.** Deleting one P1 grader and naming it in `EXCLUDED.md` fails A5 (fx04: 182 + 1 ≠ 184), because one excluded path cannot cover two absences. Combined with the sanitize forgery, A5 passes for an arbitrary deleted grader (fx04b). Fix: hard-code the one excluded path and its blob.

9. **Score rule is not enforced by the predicate.** The frozen score rule requires at least one `phenomenon-new` finding. fx03h (text: "phenomenon-known for all") prints `pass`. Fix: a separate printed `PRIOR-ART new>=1` line that the predicate or the closure reads.

## What held (negatives reported)

- Empty captures, partial captures without a population edit, dropped capture, name-only manifest, absent confirmations, empty reader, duplicate-task confirmations, two-URL prior art, and A5 without a forgery all print `fail` as frozen.
- The 12 hand-read filenames map cleanly onto population ids (no orphan), so the guard's mapping is not broken.
- The lane's captures are upstream-true today (183/183 blob matches).

## Commands run

- `python3 plans/round52_c1_grader_audit.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` (live, read-only) and `--selftest`.
- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t 1315234`; `git -C … show 1315234:plans/round52-tasks.json | sha256sum`; `git -C … show 1315234:plans/round52_c1_grader_audit.py | sha256sum` (the counter has been amended since freeze, so this differs as expected).
- `curl -fsS -m 30 "https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1"` (GET into scratch only).
- `python3 build_fx.py` (fixture builder, run in scratch), then `python3 base/plans/round52_c1_grader_audit.py --lane fx/<name>` for each fixture.
- `receipts_check.py` (blob check) and `receipts_check2.py` (exemplar re-classification, positional stripping).
- Read-only greps for prior mentions of the candidate task names across `corpus/`, `SCORECARD.md`, `LOG.md`, `SKILL.md`.

## Files produced

- This report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2CritC1Reach/report.md` (identical copy at `.ufo/waves/round-52/w2/W2CritC1Reach.md`).
- Receipts (kept): `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2CritC1Reach/receipts/` — `live_verdict.txt`, `live_selftest.txt`, `live_tests.json` (per-test classes for all 89 tasks), `runs/*.txt` (21 counter outputs, one per fixture/control), `build_fx.py`, `dump_tests.py`, `pin-tree-2fd12b88.json` (upstream tree listing), `blob_check.txt`, `receipts_check.py` (blob part; its exemplar lines are superseded by `receipts_check2.py`), `receipts_check2.py`, `receipts_check2.txt`.
- Scratch `/fast/scratch/hyaku/kengaku-r52/w2-W2CritC1Reach/` removed after the receipts were copied.

## Tools

None installed or updated. `curl` and `python3` were already present.
