# R31FxQuoteS093 — attack on S093 quotes and the DATA_DIRS claim in `benchmark-verifier-execution-model.md`

Leaf seat, round 31 wave 2 FALSIFY. Target: the S093 row of
`corpus/knowledge/benchmark-verifier-execution-model.md` (lines 68-79, 92-95): every line it cites from
`tests/test.sh` and `tests/parser.py` at the pinned commit, and whether the claim *"A fixture or snapshot an
agent edits — or adds — is neither restored from HEAD nor deleted, and reaches grading"* follows from those
bytes.

## 0. Fetch (contents API + raw, myself)

Target: `instance_internetarchive__openlibrary-00bec1e7c8f3272c469a58e1377df03f955ed478-v13642507b4fc1f8d234172bf8129942da2c2ca26`
at `scaleapi/SWE-bench_Pro-os@66f92766bba642462d4bbe5479e83f91f9211862` (pinned revision).

- Contents API: `gh api "repos/scaleapi/SWE-bench_Pro-os/contents/v2/tasks/<instance>/tests?ref=66f92766…"`
  (unauthenticated `api.github.com` was rate-limited from this IP; used the same endpoint authenticated).
  Lists 5 files: `config.json` 2447, `parser.py` 4229, `run_script.sh` 670, `test.sh` 7864,
  `test_patch.patch` 2355 — matches seat R31SrcS093a §captures.
- Raw: `curl` of `https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766…/v2/tasks/<instance>/tests/{test.sh,parser.py}`
  → HTTP 200, 7864 B / 4229 B.
- sha256 `test.sh` = `b6f26eecd87c1696a3702ee115d31f9d42f4704cf2116419cd879f66b60976d0`, `parser.py` =
  `303ceda2c97816c27383b767baa9e2f28f8e9b0cebed4dd5d6159c6760770b66` — byte-identical to the hashes
  recorded in R31SrcS093a/b. The files the entry cites are the files I read.
- Tool installs: none (used existing `gh` 2.102.0 + `curl`).

## 1. Every line the entry cites — actual bytes vs entry, and whether the cited text says what the entry says it says

Line numbers from `nl -ba` on the fetched files. All quoted bytes are verbatim from the files.

| Cited | Actual bytes (verbatim) | Entry's use | Match |
|---|---|---|---|
| test.sh:33 | `echo "Resetting test-space to base state (full test-code surface)..."` | "test.sh prints 'Resetting test-space to base state (full test-code surface)...' (test.sh:33)" | yes, verbatim |
| test.sh:38 | `DATA_DIRS = {'testdata', 'test_data', 'fixtures', 'fixture', 'mocks', 'mock', '__snapshots__'}` | "DATA_DIRS = {'testdata', 'test_data', 'fixtures', 'fixture', 'mocks', 'mock', '__snapshots__'} (test.sh:38)" | yes, verbatim |
| test.sh:43-44 | `    if any(s in DATA_DIRS for s in parents):` / `        return False` | "returns False from is_test_code (:43-44)" | yes, verbatim |
| test.sh:60 | `for p in git(['ls-files']):` | "absent from … the tracked list (:60)" — the list the reset walks | yes; the exclusion fires at :61-62, the `T` print at :62 |
| test.sh:63 | `for p in git(['ls-files', '--others', '--exclude-standard']):` | "absent from … the untracked list (:63)" | yes; `U` print at :65 |
| test.sh:71 | `        T) git checkout HEAD -- "$path" 2>/dev/null || true ;;` | "restores each tracked test-code path with T) git checkout HEAD -- "$path" (test.sh:71)" | yes, verbatim |
| test.sh:213-214 | `all_required = fail_to_pass \| pass_to_pass` / `success = all_required <= passed_tests` | "all_required = fail_to_pass | pass_to_pass then success = all_required <= passed_tests (test.sh:213-214)" | yes, verbatim |
| parser.py:68 | `    test_pattern = r'^([^\s]+\.py::[^\s]+)\s+(PASSED|FAILED|SKIPPED|ERROR)'` | "applies ^([^\s]+\.py::[^\s]+)\s+(PASSED|FAILED|SKIPPED|ERROR) with re.match on each line.strip() (parser.py:68,71)" | yes, verbatim |
| parser.py:71 | `        match = re.match(test_pattern, line.strip())` | same | yes, verbatim |
| parser.py:88-90 | `    # Also check stderr for any additional test results` / `    for line in stderr_content.split('\n'):` / `        match = re.match(test_pattern, line.strip())` | "to stdout and stderr (:88-90)" | yes, verbatim |
| parser.py:121 | `    unique_results = {result.name: result for result in results}.values()` | "dedupes by test name with unique_results = {result.name: result for result in results}.values() (:121) — i.e. last write wins" | yes, verbatim |

Every cited line exists at the cited number and carries exactly the bytes the entry quotes. Quote fidelity:
**PASS, 12/12**.

## 2. Does "fixture paths reaching grading" follow?

The entry's exact claim (lines 74-79 of the entry):

> "a path whose parent directory is in `DATA_DIRS = {…}` (test.sh:38) returns `False` from `is_test_code`
> (:43-44) and is therefore absent from both the tracked list (:60) and the untracked list (:63) the reset
> walks. A fixture or snapshot an agent **edits — or adds — is neither restored from HEAD nor deleted, and
> reaches grading**."

The input to the reset, per the bytes:
- Tracked list (`:60-62`): `git ls-files` filtered by `is_test_code` → `T` lines. A tracked fixture is excluded.
- Untracked list (`:63-65`): `git ls-files --others --exclude-standard` filtered by `is_test_code` → `U` lines.
  An added fixture is excluded. (The `--exclude-standard` flag also excludes *ignored* untracked files from the
  `U` list entirely — see §3.)
- But the reset does **not** walk only those two lists. A third, uncited pass exists at `test.sh:97-105`:
  - `:97` `git diff --name-only HEAD -- > /tmp/v6_modified.txt` — every **tracked** file modified vs `HEAD`;
  - `:100` case selector `*testdata/*|*test_data/*|*fixtures/*|*fixture/*|*mocks/*|*mock/*|*__snapshots__/*)`;
  - `:102` `git checkout HEAD -- "$p" 2>/dev/null || true ;;`.

### Verdict on the two halves of the claim

- **"adds … neither restored nor deleted, reaches grading" — HOLDS.** An agent-added fixture is untracked:
  excluded from `U` by `is_test_code` (:43-44), excluded from `T` (not tracked), and excluded from the v6 pass
  (`git diff --name-only HEAD` never lists untracked files). Nothing else in `test.sh` removes untracked files
  (the patch-stage deletions at `:77-79/:90-91` remove only paths the *gold patch* touches). It reaches grading.
- **"edits … neither restored nor deleted, reaches grading" — FALLS.** An agent-*edited* fixture is by
  definition tracked (it existed at `HEAD`). It is excluded from `T`/`U`, but `:97` lists it and `:102`
  restores it to `HEAD` **before** the patch application (:108) and the run. A tracked fixture edit does not
  reach grading. The entry's own cited evidence contradicts this half: the v6 block sits 26 lines below the
  `T`/`U` walk in the same file, and the entry never cites it.

## 3. Empirical demonstration (scratch, verbatim lines from the fetched test.sh)

`/tmp/r31fx-quotes093/repo/`: `git init` + base commit carrying `app/tests/test_x.py` and
`app/tests/fixtures/data.json`; then "agent" state: modified `test_x.py` (tracked test code), modified
`data.json` (tracked fixture), added `test_new.py` (untracked test code), added `new.json` (untracked
fixture), added `.gitignore-ignored/test_zzz.py` (untracked **ignored** test-code file).

1. `PYRESET` heredoc extracted verbatim from test.sh:34-66 (`sed -n '35,65p'`), run with cwd=repo:
   ```
   T app/tests/test_x.py
   U app/tests/test_new.py
   ```
   No line for `data.json`, `new.json`, or the ignored file — exactly as the entry describes for the two lists.
2. Driver loop, test.sh:68-74 verbatim: `test_x.py` restored to HEAD; `test_new.py` deleted.
3. v6 block, test.sh:97-105 verbatim: `git diff --name-only HEAD` → `data.json` matched `*fixtures/*` →
   `git checkout HEAD -- "app/tests/fixtures/data.json"` → restored to `{"base":1}` (agent's edit gone).
4. Final state: `data.json` = base bytes (restored); `new.json` = `{"added":true}` (survived);
   `.gitignore-ignored/test_zzz.py` survived; `test_new.py` deleted.

So, executed against the real bytes: **added fixtures survive; edited tracked fixtures are restored; and
additionally any untracked *ignored* file — including ignored test code — survives**, because `--exclude-standard`
(:63) never enumerates it. The entry's "the reset is scoped to test code" is also narrower than stated for
ignored files.

## 4. Findings

1. **[FALSIFIED] "A fixture or snapshot an agent edits … is neither restored from HEAD nor deleted, and
   reaches grading"** (entry lines 75-79). False for tracked fixtures: `test.sh:97-104` restores every
   modified-vs-`HEAD` tracked path matching `*testdata/*|*test_data/*|*fixtures/*|*fixture/*|*mocks/*|*mock/*|*__snapshots__/*`
   (`:100`, `:102`) before grading. Demonstrated in §3. The entry omits this third pass entirely.
2. **[SURVIVED] "A fixture or snapshot an agent … adds … is neither restored from HEAD nor deleted, and
   reaches grading"** — holds, incl. the empirical run in §3 (added `new.json` untouched after the full reset).
3. **[GAP, not a falsification] ignored-file hole** — `git ls-files --others --exclude-standard` (:63) never
   lists ignored untracked files, so even *test-code* files that are gitignored survive the reset (demo:
   `.gitignore-ignored/test_zzz.py`). Not claimed or refuted by the entry; reported for completeness.
4. **[SURVIVED] all 12 cited line quotes** are byte-exact at the pinned commit (table §1), including the
   reward lines `:213-214` and the parser lines `:68/:71/:88-90/:121`.

## VERDICT

S093 quote fidelity at 66f92766: **SURVIVED** (12/12 cited lines byte-exact). The DATA_DIRS hole as the entry
states it for **added** fixtures (untracked, reach grading): **SURVIVED**, executed. The same hole as the
entry states it for **edited** fixtures: **FELL** — `test.sh:97-104` restores modified tracked fixtures from
`HEAD` at `:102`, which the entry never cites; the sentence "A fixture or snapshot an agent edits — or adds —
is neither restored from HEAD nor deleted, and reaches grading" must be split, with the "edits" half corrected
(or deleted) and the v6 pass cited.

## Residual / verification gaps

- The empirical demo used a scratch repo with the same relative layout; the container's actual `/app` tree and
  `.git` state (whether `HEAD` == base commit, whether agent edits stay uncommitted) is `[INFERENCE]` from the
  image, as R31SrcS093a §bounds already notes. If an agent *committed* a fixture edit, `HEAD` would include it
  and v6 would restore to the *agent's* state — the entry's claim would then hold for that case, but that is
  an image property, not a property of the cited lines.
- Verified against the pinned files only; the entry's cross-instance claims (82 openlibrary tasks, 21 parser
  variants) were not re-run in this seat.
- No production files touched; scratch in `/tmp/r31fx-quotes093/` (≈100 KB).
