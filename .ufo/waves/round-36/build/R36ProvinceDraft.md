# R36ProvinceDraft — PROVINCE.md round-36 paragraph (draft only)

Seat: `R36ProvinceDraft` (scribe, leaf). Round 36, wave 1, 2026-10-25. Lane repo
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` (baseline tip `b662a5d6`).
No lane file was edited: this seat only read lane bytes and wrote this report plus
`.ufo/waves/round-36/build/R36ProvinceDraft/`. Nothing committed, no git index touched.

## 1. Draft — insert verbatim

Insertion point: append after `PROVINCE.md:240` (last line of the round-35 paragraph, which ends
`…this one task.`). The heading pattern matches the four existing partial-admission sections
(`PROVINCE.md:192, 204, 213, 230`); the file is append-only at this tail, so kotoba's citation of
`kengaku PROVINCE.md:30-32, 138` as the split statement (`kotoba-shokunin/PROVINCE.md:61`) is
untouched.

```markdown
## Round36 partial frontier admission (2026-10-25)

**Core addition:** offline execution of one more pinned Terminal-Bench 2.0 grader —
`regex-log/tests/test_outputs.py::test_regex_matches_dates` at terminal-bench-2 `2fd12b88` — over 24
frozen `/app/regex.txt` candidates, via `corpus/knowledge/tb2-regex-log-grader.md` (S108–S110),
`plans/regex_log_probe.py` and receipt `corpus/evidence/round36/regex-log-probe.txt` (`cases=24
observed_pass=8 observed_fail=16 mismatches=0`); the graded artefact is an agent-authored regex file,
run against the grader's fixed 25-line log. It records how that captured grader answers synthetic
patterns only: it does not run Terminal-Bench, the task image or a real submission, validate or
certify a task, establish which pattern the instruction demands, measure model or agent performance,
observe hidden or held-out tests, or speak for any other TB2 task. Adjacent: verification-fixture
craft (tameshi), research method (chousa), prompt craft (kotoba) and seat arrangement (kumitate) stay
theirs; pattern text is data. The round35 paragraph above stays as written; this paragraph narrows
only its "other 88 TB2 tasks" clause for this one task.

**Reported out:** nothing absorbed — `plans/pkg_gate.py` stays this lane's own gate (tameshi owns the reusable fixture/mutation method and never edits a sibling's gate, `tameshi-shokunin/PROVINCE.md:3,14-17,44-45`); capture and citation method stay chousa's (`chousa-shokunin/PROVINCE.md:5-7,10-11`); prompt/skill wording stays kotoba's (`kotoba-shokunin/PROVINCE.md:61`); seat arrangement, not evaluation, stays kumitate's (`kumitate-shokunin/PROVINCE.md:23,28`).
```

Word count of the paragraph (heading and `Reported out` line excluded), measured on the body copied
to `/tmp/r36-province-paragraph.txt`:

```
$ python3 -c "import pathlib; t=pathlib.Path('/tmp/r36-province-paragraph.txt').read_text(); print('draft_words', len(t.split()))"
draft_words 139
```

139 ≤ 140. (Earlier variants measured 141 and 140; the extra margin is deliberate, since a
whitespace tokenizer and `wc -w` agree at 139 but em-dash-separated tokens are the fence-post.)

## 2. What the draft asserts, and the bytes behind each assertion

| Assertion in the draft | Command run | Output |
|---|---|---|
| the graded artefact is an agent-authored regex file | `cat -n corpus/evidence/round36/tb2-regex-log/test_outputs.py` | `:21` `regex_file = Path("/app/regex.txt")`; `:25` `pattern_text = regex_file.read_text().strip()`; `:87` `matches = re.findall(pattern_text, log_text, re.MULTILINE)` |
| the log inside the grader is fixed and 25 lines | `python3 -c` parse of the `sample_logs = [` block (`test_outputs.py:34-68`) counting leading string literals | `sample_log_entries 25` (9 expected dates at `:71-81`) |
| 24 cases, 8 pass / 16 fail, no mismatch | `tail -1 corpus/evidence/round36/regex-log-probe.txt` | `cases=24 observed_pass=8 observed_fail=16 mismatches=0` |
| the grader is pinned by digest | `sha256sum corpus/evidence/round36/tb2-regex-log/test_outputs.py` | `345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72` — equals `GRADER_SHA256` (`plans/regex_log_probe.py:27`) and the capture's `SHA256SUMS:1`; `PIN` at `:25` is `2fd12b88…` |
| it is *execution*, not a re-implementation of the rule | `sed -n '113,128p' plans/regex_log_probe.py` | `run_grader` loads the captured module (`spec_from_file_location`), rebinds `mod.Path` (`:122`), calls `mod.test_regex_matches_dates()` (`:124`) and classifies `AssertionError` |
| the probe is the amended frozen instrument | `sha256sum plans/regex_log_probe.py` | `d58194c817685546a945e8b116588a52590fc944e6218ac40218381a376519bc` — the Amendment-1 digest (`plans/round-36-claims.md` §Amendment 1) |
| the receipt the draft quotes is the committed one | `sha256sum corpus/evidence/round36/regex-log-probe.txt` | `439101fa2eac0e79ebec088ab47d9fc4481df0ec12d0ebc6c3475319d426a2be` |
| `S108`–`S110` are the intended registry ids | `grep -n "S10[5-9]\|S110" corpus/SOURCES.md` | `:120-122` = S105–S107 (protein-assembly) only; no S108–S110 row exists yet |

## 3. Adjacency — read from each sibling's PROVINCE.md, quoted, not renegotiated

| Lane | Boundary clause (verbatim) | Cite | What round 36 does not take from it |
|---|---|---|---|
| **tameshi** | `**Domain:** verification-fixture craft — the reusable method of honest checks`; `**Refuses:** product domains — every lane's gate remains its own`; `Never edits a sibling's gate code (read-only probes; recommendations travel in round reports)`; adjacent row: `every sibling gate's code and product clauses (owner lane)` | `tameshi-shokunin/PROVINCE.md:3`; `:14-17`; `:44-45` | C1's `plans/pkg_gate.py` and C2's probe stay lane-local instruments; the reusable "fail-closed fixture battery" lesson may travel as a report recommendation, and this draft sends none |
| **kotoba** | `LLM and model research and evaluation … kengaku keeps measured capability effects of prompt format, kotoba owns the craft rules` | `kotoba-shokunin/PROVINCE.md:61` (its `kengaku`, `adjacent` row) | the 24 candidate regexes are grader inputs (data), not prompt or skill text; no craft rule is derived and no SKILL.md/AGENTS.md surface is read |
| **kumitate** | `Multi-agent coordinator topology — orchestration topology **decisions** … not agent evaluation`; `Local model serving and endpoints → kama. Prompt and skill craft → kotoba. Research method → chousa.` | `kumitate-shokunin/PROVINCE.md:23`; `:28` | no seat arrangement, route resolution or fallback policy is touched. Its shorthand `adjacent, not absorbed: kengaku evaluates agents, this lane arranges the seats around that judgment` (`:23`) is about remit, not a mandate to measure model performance — the draft keeps the round-35 line `measure model or agent performance` as a non-claim |
| **chousa** | `**Owns:** question framing; source hierarchy (primary / secondary / aggregator / unsourced); citation chaining and hop resolution; claim-vs-source verification`; `**Refuses:** … model-quality or evaluation claims (→ kengaku)` | `chousa-shokunin/PROVINCE.md:5-7`; `:10-11` | the probe adds offline execution of a captured artefact; the capture/hop method and claim-vs-source discipline stay chousa's, and eval claims route back to this lane rather than out |

`kama` is deliberately absent from the paragraph: the probe makes no endpoint or serving-plane call
(`plans/regex_log_probe.py` imports only `argparse, hashlib, importlib.util, pathlib, sys, tempfile`),
so the round-24 map's kama row (`PROVINCE.md:136`) needs no restatement.

## 4. Integration preconditions — the paragraph is a draft, not an earned admission

1. `corpus/knowledge/tb2-regex-log-grader.md` is **absent** at this seat's read time
   (`test -e corpus/knowledge/tb2-regex-log-grader.md` → absent). The draft names it; land the
   paragraph only after C2 admits the entry.
2. `S108`–`S110` are **not** in `corpus/SOURCES.md` yet (see §2). The parenthetical `(S108–S110)`
   binds the paragraph to C2's registry adoption; if the C2 seat lands different ids, the L1 must
   rewrite that span, not the claim.
3. C1's `plans/pkg_gate.py` is **absent** at draft time (`test -e plans/pkg_gate.py` → absent). This
   draft makes no C1 province claim, so it does not depend on C1 landing; adding one would need a
   further sentence (139 of 140 words are spent).
4. If a fresh `--rerun` in wave 2 changes any receipt byte, re-read the summary line with
   `tail -1` before landing — the draft quotes it literally.

## 5. Findings, precision notes and limits

- **Execution, not container execution.** The probe rebinds `mod.Path` so the grader's hard-coded
  `/app/regex.txt` resolves into a `tempfile.TemporaryDirectory` (`plans/regex_log_probe.py:122`); it
  does not mount `/app`, does not run `tests/test.sh`, and writes no `/logs/verifier/reward.txt`. The
  draft therefore says `offline execution … over 24 frozen /app/regex.txt candidates`, never "runs
  the task". This is the round-35 correction lesson applied in advance: `corpus/README.md:406`
  records that the round-35 sub-bullet's "reads and executes … `tests/test.sh`" overstated, because
  only the `test_*` function ran.
- **One of the 24 candidates is an absent path, not a pattern.** `add("regex-file-absent", None, "fail",
  …, mode="absent")` (`plans/regex_log_probe.py:103`) writes `absent-regex.txt` instead of
  `regex.txt` and exercises the existence branch (`test_outputs.py:22`); the other 23 write a pattern
  (one of them empty, `:101`). The draft's `24 frozen /app/regex.txt candidates` therefore covers a
  missing file as a candidate state — the probe's own docstring uses the same framing.
- **`tests/test.sh` (S109) is read, not executed.** The draft names only
  `tests/test_outputs.py::test_regex_matches_dates`; the runner's `uvx … pytest` body is registry-row
  evidence for the entry, not an executed surface.
- **The probe can be satisfied without pattern logic.** `build_cases` includes
  `add("hardcoded-expected-dates", "|".join(EXPECTED), "pass", …)` (`plans/regex_log_probe.py:97-98`),
  and the receipt records it `observed=pass`; the "does not … establish which pattern the instruction
  demands" clause is what keeps that observation from being read as task validity.
- **Capture hygiene.** `corpus/evidence/round36/tb2-regex-log/__pycache__/` holds six compiled
  variants of the captured grader from probe runs (`test_outputs.cpython-{311,312,313,313.opt-1,314,314.opt-1}.pyc`).
  It is ignored: `git check-ignore -v corpus/evidence/round36/tb2-regex-log/__pycache__` →
  `.gitignore:2:__pycache__/`, and `git status --porcelain --ignored=no corpus/evidence/round36/`
  prints nothing. So it does not breach C1's `--require-clean-tree`, and a clean clone carries none
  of it — but the L1 should not add those bytes to a capture directory whose `SHA256SUMS` is a
  positive manifest.
- **Working-tree state at draft time (environmental, not C1's result).**
  `git ls-files --others --exclude-standard | wc -l` → `813`, nearly all wave-36 seat scratch
  (e.g. `.ufo/waves/round-36/build/R36ProbeHarnessMut/…`). C1's predicate is measured on a clean
  clone of the landing tip, so build scratch must stay uncommitted; recorded because it is the
  environment the predicate will be measured in, not a defect this seat may fix.
- **No tool installed or upgraded** by this seat (no pacman, uv, npx or binary fetch); no fixtures
  created — every read was against lane bytes or a sibling lane's PROVINCE.md.

## 6. Not done, deliberately

- No edit to `PROVINCE.md`, `SKILL.md`, `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`
  or any sibling lane.
- No counter run (`round36_c1_verify.py`, `round36_c2_verify.py`) and no probe re-run: C1/C2 scoring
  is the frozen counters' job, and re-running to decorate this report would be decoration.
- No commit, no `git add`, no jj command.

VERDICT: province-drafted
