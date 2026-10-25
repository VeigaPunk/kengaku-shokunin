# R31DraftRows — the three registry rows this lane would append on 2026-10-25

Seat: `L1Kengaku31.R31DraftRows` (leaf scribe). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Round 31 (hyaku run 6), claim C1 (coverage). Baseline tip `0883e72ef8474ca42ac1a54eb0273079f1507035`.
Everything below was executed on 2026-10-25 between 05:45 and 06:00 −03:00. Nothing in the lane tree was
written except this file; all captures live in `/tmp/r31-R31DraftRows/` (1.3 MB, well under the 60 MB bound).

## What I did

1. Read the frozen claims (`plans/round-31-claims.md`), the staged package
   (`/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`, rows S092/S093/S100 at lines 22, 23, 30),
   the staged entry (`…/knowledge/corpus/knowledge/benchmark-verifier-execution-model.md`) and the live registry's
   recent rows (S090 `corpus/SOURCES.md:103`, S091 `:104`) for style.
2. Re-opened all three sources at their pinned commits with `curl` against
   `raw.githubusercontent.com` and the GitHub REST API. No clone, no token, no campaign tool.
3. Rewrote the three rows as 11-cell rows with `opened=2026-10-25`, `recheck=180d`,
   `used-by=corpus/knowledge/benchmark-verifier-execution-model.md` only, `status=mined`, and every quoted span
   ≤25 words by the gate's own counter (`sources_adopt.words`), each with a file+line location.
4. Ran the required gate, then two extra probes: a URL-bound quote check per row, and a refusal probe on the
   staged S093 row.

## Provenance of every capture (opened 2026-10-25)

| id | URL the row cites | resolves today to | pin | captured | bytes |
|---|---|---|---|---|---|
| S092 | `https://github.com/laude-institute/harbor` | `harbor-framework/harbor` (repo id 1032170083) | `6099b8cf2bfbbb3e7ff1eb2163bfc4524dbd9ba5` | `src/harbor/models/task/config.py` (1060 L), `src/harbor/verifier/verifier.py` (310 L) | 39055 + 11910 |
| S093 | `https://github.com/scaleapi/SWE-bench_Pro-os` | unchanged (id 1051347649) | `66f92766bba642462d4bbe5479e83f91f9211862` | `v2/tasks/instance_internetarchive__openlibrary-00bec1e7…ca26/tests/test.sh` (234 L), `tests/parser.py` (157 L), `tests/config.json` (4 L); `v2/tasks` listing = 642 entries | 7864 + 4229 + 2447 |
| S100 | `https://github.com/laude-institute/terminal-bench-2` | `harbor-framework/terminal-bench-2` (id 1063848495; the API answers **301 → /repositories/1063848495/**) | `2fd12b88aafdd04a52c298e3940bcb189f9766d6` | `README.md` (100 L); tree API, untruncated | 4574; tree 26062 |

GitHub REST calls used (unauthenticated, all HTTP 200 after following the 301s): SWE-bench `contents/v2/tasks`
(642 entries), `terminal-bench-2` tree + `/tags` (`[]`), `/repositories/1063848495`, `harbor-framework/terminal-bench`
`/tags` (`v4.0.0`=452bf30, `v3.0.0`=2b0442c) and four subtree listings (`tasks/` 68 entries at v4.0.0, `archive/`
2 entries at v4.0.0, `tasks/` 76 entries at v3.0.0, no `archive/` at v3.0.0), plus identity probes on
`laude-institute/terminal-bench` (→ `harbor-framework/terminal-bench-1`, id 918420677) and
`harbor-framework/terminal-bench` (id 1141514919, created 2026-01-25).

## The three rows (exactly as the gate emits them)

Produced by `plans/sources_adopt.py … --out /tmp/r31-R31DraftRows/emitted-baseline.txt`; the only cells the gate
changed from my package are `recheck` (staged prose → `180d`), byte-identical otherwise. `awk -F'|'` gives 11 cells
per row, and `grep -c '\\|'` gives 0 — no literal and no escaped pipe in any cell.

| S092 | Harbor harness source (verifier execution model) — https://github.com/laude-institute/harbor | code | A | the framework code that decides *where* a task's verifier runs and *what* it overwrites before grading, for the harness's own behaviour at a pinned commit | commit 6099b8cf2bfbbb3e7ff1eb2163bfc4524dbd9ba5, src/harbor/models/task/config.py:590-593 (VerifierConfig.environment_mode description, split across two string literals): "Whether the verifier runs in the agent's environment ('shared')" (9 words) and "to 'separate' if a verifier 'environment' is set, otherwise" (9 words); src/harbor/verifier/verifier.py:168 docstring "Discard stale rewards without removing other verifier inputs or logs." (10 words); :207 "await self._remove_reward_files()" (2 words); :209 "if not self._skip_tests_upload:" (3 words); :220 "await self.environment.upload_dir(" (2 words) | the framework default is shared — the verifier runs in the container the agent worked in unless the task sets a verifier environment or environment_mode='separate' — so isolation is a per-task opt-in; what the default path guarantees is narrower than isolation: stale reward files are deleted first, and the tests directory is re-uploaded from the host, an upload the caller can skip (verifier.py:209) | mined | 2026-10-25 | 180d | corpus/knowledge/benchmark-verifier-execution-model.md |
| S093 | SWE-bench Pro V2 task verifier files (test.sh, parser.py, config.json) — https://github.com/scaleapi/SWE-bench_Pro-os | code | A | the executed grading code for one SWE-bench Pro V2 task at a pinned commit: what is reset before grading, which paths the reset skips, and how the reward is computed, for the code's own behaviour | commit 66f92766bba642462d4bbe5479e83f91f9211862, v2/tasks/instance_internetarchive__openlibrary-00bec1e7c8f3272c469a58e1377df03f955ed478-v13642507b4fc1f8d234172bf8129942da2c2ca26/tests/test.sh:29 "find . -name '__pycache__' -type d -prune -exec rm -rf {} +" (12 words); :33 "Resetting test-space to base state (full test-code surface)..." (8 words); the reset list is built by is_test_code() at :40-55, where :38 "DATA_DIRS = {'testdata', 'test_data', 'fixtures', 'fixture', 'mocks', 'mock', '__snapshots__'}" (9 words) and :43 "if any(s in DATA_DIRS for s in parents):" (8 words) reach :44 "return False" (2 words), so data-dir paths are absent from both the tracked list at :60 and the untracked list at :63; the embedded grader at :169-229 reads :183 "fail_to_pass_raw = config.get('fail_to_pass', [])" (4 words), builds :204 "pass_to_pass = set(parse_tests(pass_to_pass_raw))" (3 words) and :210 "passed_tests.add(test.get('name', ''))" (2 words) from the status at :209, then :214 "success = all_required <= passed_tests" (5 words) | the reward is a binary set-containment test over the union of fail_to_pass and pass_to_pass (test.sh:213,214): every required test name must appear in the PASSED set, so a task is graded on named tests rather than on an aggregate; the pre-grade reset restores test *code* only — a path whose parent is fixtures, fixture, testdata, test_data, mocks, mock or __snapshots__ is neither restored from HEAD nor deleted when untracked, so an agent-modified or agent-added file under a fixture directory reaches grading | mined | 2026-10-25 | 180d | corpus/knowledge/benchmark-verifier-execution-model.md |
| S100 | Terminal-Bench dataset releases and task-count audit — https://github.com/laude-institute/terminal-bench-2 | dataset | A | which repository holds which Terminal-Bench release, how many task directories each release carries, and whether a release tag identifies a dataset version, for the repositories' own trees and the dataset README at a pinned commit | laude-institute/terminal-bench-2 at commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, README.md:46 "uv run harbor run --dataset terminal-bench@2.0" (6 words) — the dataset is addressed by a name@version string, not a git ref; that repository's tree API for the same commit (untruncated response) 「92 top-level entries: 89 directories and three blobs (.gitignore, LICENSE, README.md)」; its /tags endpoint returns 「[] — no tag pins this tree」; the cited URL resolves today to harbor-framework/terminal-bench-2 (repository id 1063848495); a different repository, harbor-framework/terminal-bench (id 1141514919), carries v3.0.0 (2b0442c) with 「76 entries under tasks/ and no archive/ directory」 and v4.0.0 (452bf30) with 「68 entries under tasks/ and 2 under archive/」 | the 89-task Terminal-Bench 2.0 dataset lives in a repository that carries no git tags, while the tagged v3.0.0 and v4.0.0 releases are a different repository with a different task count — so a dataset version cannot be pinned by tag and must be pinned by commit; the round-1 figure of 92 task directories was a miscount of top-level entries, which include three non-task files, and the true task count at this commit is 89 | mined | 2026-10-25 | 180d | corpus/knowledge/benchmark-verifier-execution-model.md |

## The dropped span (S093), stated exactly

The staged S093 row (`SOURCES.append.md:23`) carries this quoted span in its anchor cell:

    all_required = fail_to_pass \| pass_to_pass

I dropped it. Two independent reasons, both measured:

1. **The bytes contain a literal `|`.** `test.sh:213` is, verbatim,
   `all_required = fail_to_pass | pass_to_pass`. A literal `|` is the table delimiter: it turns an 11-cell row into
   a 12-cell row, and `split_cells` refuses the escaped form too — the staged row's own `\|` is refused as
   `escaped-pipe` (probe below, exit 4).
2. **Nothing is lost.** The same fact is carried by a pipe-free span one line down, `test.sh:214`
   `success = all_required <= passed_tests` (5 words, located), and by the `teaches` cell, which states in prose that
   the required set is the union of `fail_to_pass` and `pass_to_pass` and that the reward is set containment over
   that union. The union line is named as a location (`test.sh:213,214`) without reproducing its bytes.

Refusal probe — the staged row through the same gate:

    $ python3 plans/sources_adopt.py --package /tmp/r31-R31DraftRows/staged-S093-row.txt \
        --registry /tmp/r31-R31DraftRows/SOURCES-baseline.md --admit-ids S093 --scope-to-admit \
        --access-date 2026-10-25 --entries corpus/knowledge/benchmark-verifier-execution-model.md
    registry=88 staged=0 collisions=0 malformed=1 duplicates=0 defects=0 prose=0
      malformed: S093:escaped-pipe
    EXIT=4

## Other anchor corrections against the staged package

These are corrections, not restylings; each is grounded in bytes fetched today.

- **S092, the staged span was over the cap and not byte-contiguous.** The staged anchor quotes
  `"Whether the verifier runs in the agent's environment ('shared') or in a dedicated container ('separate').
  When omitted: defaults to 'separate' if a verifier 'environment' is set, otherwise 'shared'."` — 28 words by
  `sources_adopt.words` (cap 25), and `in config.py` is **False**: in the source it is four concatenated string
  literals at `config.py:590-593`, so no contiguous run matches it. It would be refused twice (exit 6 overlong,
  exit 7 absent). I split it into two single-literal spans, 9 words each, both located.
- **S092, `teaches` narrowed.** The staged cell says the tests directory "is re-uploaded from the host before the
  verifier runs"; `verifier.py:209` makes that upload conditional (`if not self._skip_tests_upload:`), so the row now
  says the upload is skippable and names the line.
- **S093, `teaches` corrected.** The staged cell says "the fixture-restore step iterates tracked modifications only,
  so an agent-added untracked file under a fixture directory survives into grading". The first clause is false at
  this commit: `test.sh:63` enumerates `git ls-files --others --exclude-standard` and `:65` prints `U` for untracked
  test-code paths, which the reset loop deletes. The survival is real but for a different reason — `is_test_code()`
  returns `False` whenever a *parent* segment is in `DATA_DIRS` (`:38`, `:43-44`), so fixture/data paths appear in
  neither list and are neither restored from `HEAD` nor deleted when untracked. The row states the corrected rule.
- **S100, two staged claims dropped or corrected.** Dropped: "the first commit with exactly 89 task directories is
  f8f596a0fb06517d6731ff75093c92eb82ee3d80 (2025-10-30)" — an ordering claim about history I did not walk today, so
  it is not restated. Corrected: "harbor-framework/terminal-bench is tagged v3.0.0 (2b0442c) and v4.0.0 (452bf30),
  each with 68 entries under tasks/ and 2 under archive/" — v3.0.0 has **76** entries under `tasks/` and **no**
  `archive/` directory; only v4.0.0 has 68 and 2. Kept and re-verified: 92 top-level entries = 89 directories +
  `.gitignore`, `LICENSE`, `README.md` at `2fd12b8`; `/tags` on that repository returns `[]`.
- **S100, the rename is now in the row.** The cited URL `laude-institute/terminal-bench-2` answers 301 to
  `harbor-framework/terminal-bench-2` (id 1063848495). The row keeps the cited URL in `source` (so the URL-bound
  quote check binds to the URL the row cites) and records the resolution in the anchor.

## Stripped prose (recorded separately, as required)

Each staged `recheck` cell was prose; the gate normalized it to `180d` and printed the stripped text. Verbatim:

- S092 — `2026-10-23 — re-verify at the next upstream release (Gate S092 below)`
- S093 — `2026-10-23 — re-verify at the next upstream release (Gate S093 below)`
- S100 — `2026-10-23 — re-verify at the next upstream release (Gate S100 below)`

The `(Gate S092 below)` tail referred to a gate section inside the staged package; it does not survive into the
registry, where the cell is `180d`. Nothing else in those cells is lost: the "next upstream release" trigger is what
`180d` encodes, and the rows' `opened` is the access date.

## Gate run (required command)

The tree moved while I worked: a sibling seat appended S092/S093/S100 to `corpus/SOURCES.md` at lines 111–113
between my first and second run, so the same command gives two different results. Both are reported.

**Run 1 — 05:52, registry still at 88 rows (`sha256 41f09e6b…` before the sibling's append):**

    $ python3 plans/sources_adopt.py --package /tmp/r31-R31DraftRows/rows.txt \
        --registry corpus/SOURCES.md --admit-ids S092,S093,S100 --scope-to-admit \
        --access-date 2026-10-25 --entries corpus/knowledge/benchmark-verifier-execution-model.md
    registry=88 staged=3 collisions=0 malformed=0 duplicates=0 defects=0 prose=3
      normalized recheck S092: 2026-10-23 — re-verify at the next upstream release (Gate S092 below)
      normalized recheck S093: 2026-10-23 — re-verify at the next upstream release (Gate S093 below)
      normalized recheck S100: 2026-10-23 — re-verify at the next upstream release (Gate S100 below)
    | S092 | … | S093 | … | S100 | …      (three rows written to stdout)
    EXIT=0

**Run 2 — 05:58, same command, registry now at 91 rows (the three ids already appended):**

    registry=91 staged=3 collisions=3 malformed=0 duplicates=0 defects=0 prose=3
      collisions: S092 S093 S100
    EXIT=3

**Control — the same package against the baseline registry (`git show 0883e72:corpus/SOURCES.md`, 88 rows):**

    registry=88 staged=3 collisions=0 malformed=0 duplicates=0 defects=0 prose=3
      normalized recheck S092: 2026-10-23 — re-verify at the next upstream release (Gate S092 below)
      normalized recheck S093: 2026-10-23 — re-verify at the next upstream release (Gate S093 below)
      normalized recheck S100: 2026-10-23 — re-verify at the next upstream release (Gate S100 below)
    wrote /tmp/r31-R31DraftRows/emitted-baseline.txt rows=3
    EXIT=0

Read together: the package is valid (0 malformed, 0 duplicates, 0 defects, prose normalized, exit 0) and run 2's
exit 3 is the *collision* refusal — the registry already holds these ids — not a defect in the rows. The gate binary
I ran is the working-tree version (`sha256 4e49a3e2…`, +244 lines vs `0883e72`; the baseline has no `--url-map` at
all, `grep -c url_map` = 0), i.e. the C3 seat's in-progress URL-binding work, not the frozen baseline.

## Extra evidence: every span located in the document the row cites

Not required by the ticket, run because it is the only way to show the quotes are bytes and not paraphrase. One
invocation per row, each with its own artifact directory and URL map, so a span cannot be satisfied by a capture of
some other document:

    $ python3 plans/sources_adopt.py --quote-file …/row-S092.txt --artifact …/art-s092 \
        --url-map …/map-s092.json
    QUOTE rows=1 spans=6 located=6 found=6 overlong=0 absent=0 mismatch=0 unmapped=0 malformed=0 cap=25
      urlmap=entries=2 artifacts=harbor_src_harbor_models_task_config.py,harbor_src_harbor_verifier_verifier.py
      ok S092 words=9 at harbor_src_harbor_models_task_config.py quote="Whether the verifier runs in the agent's environment ('shared')"
      ok S092 words=9 … quote="to 'separate' if a verifier 'environment' is set, otherwise"
      ok S092 words=10 at harbor_src_harbor_verifier_verifier.py quote="Discard stale rewards without removing other verifier inputs or logs."
      ok S092 words=2 … quote="await self._remove_reward_files()"
      ok S092 words=3 … quote="if not self._skip_tests_upload:"
      ok S092 words=2 … quote="await self.environment.upload_dir("
    EXIT=0

    $ python3 plans/sources_adopt.py --quote-file …/row-S093.txt --artifact …/art-s093 \
        --url-map …/map-s093.json
    QUOTE rows=1 spans=9 located=9 found=9 overlong=0 absent=0 mismatch=0 unmapped=0 malformed=0 cap=25
      urlmap=entries=1 artifacts=swe_tests_test.sh
      ok S093 words=12 quote="find . -name '__pycache__' -type d -prune -exec rm -rf {} +"
      ok S093 words=8  quote="Resetting test-space to base state (full test-code surface)..."
      ok S093 words=9  quote="DATA_DIRS = {'testdata', 'test_data', 'fixtures', 'fixture', 'mocks', 'mock', '__snapshots__'}"
      ok S093 words=8  quote="if any(s in DATA_DIRS for s in parents):"
      ok S093 words=2  quote="return False"
      ok S093 words=4  quote="fail_to_pass_raw = config.get('fail_to_pass', [])"
      ok S093 words=3  quote="pass_to_pass = set(parse_tests(pass_to_pass_raw))"
      ok S093 words=2  quote="passed_tests.add(test.get('name', ''))"
      ok S093 words=5  quote="success = all_required <= passed_tests"
    EXIT=0

    $ python3 plans/sources_adopt.py --quote-file …/row-S100.txt --artifact …/art-s100 \
        --url-map …/map-s100.json
    QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 mismatch=0 unmapped=0 malformed=0 cap=25
      urlmap=entries=1 artifacts=tb2_README.md
      ok S100 words=6 at tb2_README.md quote="uv run harbor run --dataset terminal-bench@2.0"
    EXIT=0

16 spans, all located, all ≤12 words, all bound to their row's cited URL. S100's tree counts and tag facts are
`「」` spans over the API responses named in the anchor, not document quotes, so they are deliberately outside the
`"…"` span set the gate counts; they are re-derivable from the URLs and shas the anchor names.

Gate selftest at the same moment (recorded, not claimed as C3): `SELFTEST cases=17 failed=0`, exit 0.

## Findings for Main

1. **The append already landed.** `corpus/SOURCES.md:111-113` carries S092, S093 and S100 with `opened=2026-10-25`,
   `recheck=180d`, `used-by=corpus/knowledge/benchmark-verifier-execution-model.md` and no pipe. Any further append
   of these ids must be a *replacement*, not an addition; the gate's collision refusal (exit 3) is the correct
   signal.
2. **The landed S092 anchor would fail the quote gate.** It quotes
   `"When omitted: defaults to 'separate' if a verifier 'environment' is set, otherwise 'shared'."` (13 words) —
   that run crosses the literal boundary between `config.py:591` and `:592`/`:593`, so it is not a byte substring of
   the file. Against a real capture it is refused as absent (exit 7). My row splits it into two single-literal
   spans, which locate. This is a C1-side risk on a row that is already in the registry.
3. **The landed S100 anchor and mine agree on the rename** (301 → `harbor-framework/terminal-bench-2`) and on 92
   top-level entries; the landed row does not carry the tag census, so it does not repeat the staged v3.0.0 error
   (76 entries under `tasks/`, no `archive/`).
4. **Round-1's "92 task directories" is a top-level-entry count**, not a task count: 92 = 89 directories + 3 files.
   Re-verified today from the untruncated tree API at `2fd12b8`.

## Out of scope / not claimed

- C2 (R1–R10) untouched; I ran no defect counter and claim no closure there.
- C3 not claimed: I used `--url-map` and recorded the selftest, but the implementation is the sibling's and the
  frozen predicate is theirs to prove.
- The knowledge entry itself was not edited (staged copy read only; `verified-at` there still reads 2026-10-23).
- No tool installed or upgraded; nothing needed beyond `curl` and `python3`.
- No campaign tool, no clone, no write outside `/tmp/r31-R31DraftRows/` and this report.

## VERDICT

VERDICT: ROWS-READY — three 11-cell rows produced with `opened=2026-10-25`, `recheck=180d` (prose recorded above),
`status=mined`, `used-by` naming only `corpus/knowledge/benchmark-verifier-execution-model.md`, no literal or escaped
pipe, 16/16 quoted spans located in the row's cited document and ≤12 words each; gate exits 0 on the 88-row baseline
(`registry=88 staged=3 collisions=0 malformed=0 duplicates=0 defects=0 prose=3`) and exits 3 on the live 91-row tree
solely because the same three ids were appended by a sibling seat at `corpus/SOURCES.md:111-113` before my second run.
