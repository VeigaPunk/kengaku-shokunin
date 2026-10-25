VERDICT: frontier-read

# R32Frontier — coverage-map and frontier wording for round 32

Scout lane, kengaku round 32 (2026-10-25). Read-only. Baseline `f20a1097`. Access date for every
source opened here: 2026-10-25.
Axes named: (a) the frontier clause C1 discharges, (b) the coverage-map row, (c) the index row,
(d) the clauses C2/C3 touch. Every string below is quoted from the lane tree at
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`, with the line number it sits on and a byte pin.

Pins used below (all `corpus/README.md`, md5 of the single line):
`L276` 841 bytes, md5 `d76f2629a0c128b0b26bb728cb126230`; `L253` 555 bytes; `L66` 488 bytes,
md5 `7ab14efe9f002805f1a30ba9b4911040`.

---

## (a) Frontier bullet 1 — the clause C1 discharges, and its after-state

**Location.** `corpus/README.md:274` is the bullet head, `:275` the round-29 discharge, `:276` the
round-31 discharge (L276). The instruction line C1 narrows lives in `:274`:

> `Next source/instrument: the primary specs and scoring code for Terminal-Bench 2.0, Toolathlon, and SWE-bench Pro (unopened leads in the ART dossier), turned into a per-benchmark task-validity checklist.`

**Exact current text of L276 (841 bytes, verbatim):**

> `  - *Partly discharged round 31 (2026-10-25):* \`knowledge/benchmark-verifier-execution-model.md\` reads the harness's own verifier-mode resolver and \`Verifier.verify\` at Harbor commit \`6099b8cf\`, so the \`their scoring code was not read and stays open\` clause above is discharged for **verifier execution** (where grading runs, what is restored first, how SWE-bench Pro V2 derives its PASSED set). The clause stays open for the other benchmarks' scoring code (one SWE-bench Pro V2 task's grader *is* read here, in depth, and that is the only task-level code this round opens), for runtime task validity (which \`PROVINCE.md\` refuses to this lane) and for Toolathlon; the Terminal-Bench 2.0 axis-E cell is filled by this entry and the SWE-bench Pro axis-E cell was already credited to S078 in \`knowledge/benchmark-task-validity-checklist.md:96\`.`

**The sub-clause C1 discharges.** The exact substring `and for Toolathlon` (L276, inside
"The clause stays open … and for Toolathlon;") — nothing else. It is *not* the whole
"The clause stays open for the other benchmarks' scoring code (…)" parenthetical, and it is *not*
the round-29 phrase `their scoring code was not read and stays open` (`:275`), which round 31 already
narrowed.

**Before → after. L276 is not edited.** The lane's own precedent (round 30 appended `:278` and left
`:277`'s instruction byte-identical, saying so in the appended text) and round 31 (appended `:276`,
left `:275` untouched) both append a new 2-space-indented sub-bullet. Same here: append after L276,
before `:277` (`- **Contamination transparency cards**…`).

Anchor (unique) — old:

```
 SWE-bench Pro axis-E cell was already credited to S078 in `knowledge/benchmark-task-validity-checklist.md:96`.
- **Contamination transparency cards**: why —
```

new:

```
 SWE-bench Pro axis-E cell was already credited to S078 in `knowledge/benchmark-task-validity-checklist.md:96`.
  - *Partly discharged round 32 (2026-10-25):* `knowledge/benchmark-grader-semantics.md` reads Toolathlon's own task evaluation script at commit `9be8d8fe` (S094) — a state comparison of a produced `record.csv` against `groundtruth_workspace/expected_ratio.csv` at the 0.05-point tolerance its call site passes (the signature's `tolerance_pct: float = 0.1` default is not the executed path), a project-wide bucket-prefix existence check and a log-bucket cleanliness check that returns `True` when its own read fails, and no judge prompt or rubric anywhere in the file — so the `and for Toolathlon` clause above is discharged for the one task whose evaluation script is read, not for the benchmark's whole scoring surface. It also re-reads S093's grader as the same kind of artefact (binary set containment over the union of `fail_to_pass` and `pass_to_pass`), which restates `knowledge/benchmark-verifier-execution-model.md` rather than re-opening it, and uses S097's five-part survey to keep a deterministic grader and an LLM judge from being described in the same terms. The clause stays open for every other benchmark's scoring code, for Toolathlon tasks whose `evaluation/main.py` differs from this one, for how much of a pass the `grade_with_retry` defaults (3 attempts, 5 s apart) absorb, for runtime task validity (which `PROVINCE.md` refuses to this lane) and for hosted judges.
- **Contamination transparency cards**: why —
```

Three wording constraints the drafter must not relax:
1. **"one task whose evaluation script is read", never "Toolathlon's scoring code".** The evidence is a
   single file at `tasks/finalpool/ab-testing/evaluation/main.py`. Toolathlon has a per-task
   `evaluation/` directory per task; one task is not the benchmark's scoring surface.
2. **The S093 half must be described as restating round 31.** `corpus/knowledge/benchmark-verifier-execution-model.md`
   already holds the containment reward (`:99-101`, `all_required = fail_to_pass | pass_to_pass` /
   `success = all_required <= passed_tests`) and the fixture asymmetry the staged entry presents as its
   own finding (`:76-90`: `DATA_DIRS = {'testdata','test_data','fixtures','fixture','mocks','mock','__snapshots__'}`
   at `test.sh:38`, agent-added fixtures in neither list, `git diff --name-only HEAD` → `git checkout HEAD -- "$p"` at
   `test.sh:97-104`). Q6 forbids a duplicate; the new entry extends, and the frontier text must say so.
3. **Do not touch L274.** The instruction line stays byte-identical; the discharge is the appended
   sub-bullet (round-30's `:278` states this rule explicitly for its own case).
4. **The `0.05` in (a), (b) and (c) is conditional on fixing the entry first.** The staged entry states
   `0.1` (its `:69`) because it quotes the signature default; the executed call passes `0.05`
   (`main.py:280`, verified below). If the entry lands with `0.1`, every README string here must be
   rewritten to match the entry, not the code — but then the README would be asserting a tolerance the
   grader does not use, so the correction belongs in the entry. Land the entry's fix first.

---

## (b) Coverage-map row

**Insertion point:** immediately after `:253` (`- **Benchmark verifier execution model**…`), i.e. as a
new `:254`, directly before `## Open gaps` (there is no blank line there today). Q7 requires entry +
index row + coverage-map row to land in the same commit.

**Row name (bold lead):** `**Benchmark grader semantics**` — matches the entry title
(`# Benchmark grader semantics`, staged file line 8) and the existing noun-phrase style
(`**Benchmark verifier execution model**`, `**Benchmark task-validity instruments**`).

Anchor (unique) — old (tail of `:253` plus the next line):

```
SED set. Not runtime task validity (PROVINCE refuses it), not contamination measurement, not deployment config.
## Open gaps
```

new:

```
SED set. Not runtime task validity (PROVINCE refuses it), not contamination measurement, not deployment config.
- **Benchmark grader semantics**: covered at source-code depth (round 32, 2026-10-25) — knowledge/benchmark-grader-semantics.md; S093, S094, S097. Discharges the round-31 clause "and for Toolathlon" for that benchmark's scoring code only: one task's `evaluation/main.py` compares a produced `record.csv` against `groundtruth_workspace/expected_ratio.csv` at the 0.05-point tolerance its call site passes, adds a project-wide bucket-prefix existence check and a log-bucket cleanliness check that fails open on its own read errors, and carries no judge prompt or rubric in the scoring path. The S093 half restates the binary set-containment reward and test-space reset already held in the round-31 entry, and S097's five-part survey supplies the frame that keeps a deterministic grader and an LLM judge from being described in the same terms. Not runtime task validity (PROVINCE refuses it), not contamination measurement, not the SWE-bench Pro V2 grader (read round 31), not deployment config.
## Open gaps
```

Note the closing trio is the house form on `:253` (`Not runtime task validity (PROVINCE refuses it), not
contamination measurement, not deployment config.`) and on `:252` in a different order
(`Not deployment config, not runtime task validity, not contamination measurement.`); the row above
copies `:253`'s order and wording, since it discharges the same clause.

---

## (c) Index-table tail

**Insertion point:** `:66` is the last knowledge row (`| \`knowledge/benchmark-verifier-execution-model.md\` | … | S092 (Harbor @ 6099b8cf), S093 (SWE-bench Pro V2 @ 66f92766), S100 (terminal-bench-2 @ 2fd12b88) |`);
`:67` starts the lessons block (`| \`lessons/round-1.md\` | Path-correction, replace-don't-appe…`). The new
knowledge row goes between them — the table's knowledge tail.

Anchor (unique) — old:

```
PASSED set | S092 (Harbor @ 6099b8cf), S093 (SWE-bench Pro V2 @ 66f92766), S100 (terminal-bench-2 @ 2fd12b88) |
| `lessons/round-1.md` | Path-correction, replace-don't-appe
```

new:

```
PASSED set | S092 (Harbor @ 6099b8cf), S093 (SWE-bench Pro V2 @ 66f92766), S100 (terminal-bench-2 @ 2fd12b88) |
| `knowledge/benchmark-grader-semantics.md` | What two benchmarks' scoring code actually does, read as grader *kinds*: SWE-bench Pro V2's binary set containment over the union of `fail_to_pass` and `pass_to_pass`, Toolathlon's state comparison of a produced `record.csv` against a ground-truth ratio file at the 0.05-point tolerance its call site passes, plus two side-effect checks one of which fails open, and S097's five-part frame separating deterministic graders from LLM judges; extends `knowledge/benchmark-verifier-execution-model.md`, not runtime task validity, contamination measurement or model performance | S093 (SWE-bench Pro V2 @ 66f92766), S094 (Toolathlon @ 9be8d8fe), S097 (arXiv 2412.05579v2) |
| `lessons/round-1.md` | Path-correction, replace-don't-appe
```

**Shape constraints enforced by the frozen counters** (read from source, not inferred):
- `plans/adoption_check.py:76` matches `^\| \`knowledge/<name>\` \|` — the row must start at column 0
  with exactly that prefix (one space either side of the backticked name). A bullet or an indented row
  does not count.
- `plans/adoption_check.py:126-133` requires **exactly one** such row and **≥3 non-empty cells**
  (entry, Covers, Primary source). `plans/round32_c1_verify.py:104-111` (V4) additionally requires
  cell 2 ≥ 20 chars.
- Because cells are split on `|`, the Covers cell above avoids a literal `|` (it says "the union of
  `fail_to_pass` and `pass_to_pass`"). If the drafter prefers the code's own `fail_to_pass | pass_to_pass`,
  escape it as `\|` exactly as `corpus/SOURCES.md:112` does.
- The coverage-map bullet in (b) must stay a bullet: it must **not** match the index regex, or
  `indexed` becomes 2 and C1 fails.

---

## (d) Other frontier clauses touched by C3 and C2

### C3 (freshness) — touches the coverage map and one index row, no frontier bullet

**d1. Coverage-map `:233` is falsified by C3 as written.** Exact current text:

> `- **Model catalog access**: historical Bailian digest plus historical HF/OpenRouter API observations; Bailian originals are unavailable, and public catalogs were not re-fetched in this continuation (\`knowledge/local-model-index.md\`, \`knowledge/open-model-catalogs.md\`).`

Neither C3 counter reads `README.md` (`plans/catalog_probe.py` has no README/index/coverage reference;
its `entry_ok` at `:82-92` reads only the knowledge entry for `verified-at: 2026-10-25`, `S101`, `S102`).
So this is a Q7/consistency obligation the counters do not enforce — and a critic will route it, because
after C3 lands the clause is simply false.

Two legal after-states; **preferred is the append-only one** (Q6: numbers corrected by appended errata,
never in-place edits; round 30 set the precedent by amending `:243`'s row with a *new* row rather than
rewriting `:242`):

- Preferred — leave `:233` byte-identical, append after it:
  `- **Public model catalog freshness**: re-probed 2026-10-25 (round 32) — knowledge/open-model-catalogs.md now carries `verified-at: 2026-10-25`, cites S101/S102 and points at its receipt under `corpus/evidence/round32/catalogs/`; the "not re-fetched in this continuation" clause in the row above describes the state before that refresh.`
- Alternative — in-place state correction of `:233` (only if the drafter argues a state clause is not a
  number): replace `and public catalogs were not re-fetched in this continuation` with
  `and public catalogs were re-probed 2026-10-25 (S101, S102)`.

**d2. Index row `:40` carries the stale probe date C3's own claim quotes.** Exact current text:

> `| \`knowledge/open-model-catalogs.md\` | HF + OpenRouter live catalog schemas, filter/sort fields, open-weight twin links | \`huggingface.co/api/models\`, \`openrouter.ai/api/v1/models\`, probed 2026-09-28 |`

After (append-only, keeps the old date visible):

> `| \`knowledge/open-model-catalogs.md\` | HF + OpenRouter live catalog schemas, filter/sort fields, open-weight twin links | \`huggingface.co/api/models\`, \`openrouter.ai/api/v1/models\`, probed 2026-09-28, re-probed 2026-10-25 (S101/S102) |`

Same treatment inside the entry: `corpus/knowledge/open-model-catalogs.md:5` reads
`verified reachable and schema-probed 2026-09-28 (no auth needed for reads):` — leave it, and add the
`verified-at: 2026-10-25` frontmatter block C3's predicate names (the entry has **no** frontmatter today;
line 1 is `# Open model catalogs (non-Bailian)`).

**d3. C3 does not touch frontier bullet 4.** `:284` (`Identity-verified endpoint for novelty probes`,
`:34113` absent) is about a model-serving endpoint for capability/novelty probes. Public HF/OpenRouter
catalog reads need no identity-verified endpoint, and C3's own Non-claims forbid a novelty verdict. Do
not attach C3 to `:284`.

### C2 (calibration) — touches no README clause at all

The seven routed items are D1–D6 (`corpus/lessons/round-31-verifier-spotcheck.md:147-166`) plus the
carried peer-review erratum debt. Their surfaces, verbatim from that file: `.ufo/reports/round-31/kengaku.md:226`
(D1), the final lane commits `ae95fe0`/`87f0d32` vs the report (D2), `corpus/evidence/round31/gate-cli-exits.txt`
(D3), `SKILL.md` §Gate/probe registry (D4), the falsify registry vs `R31FxEntryBar`'s report (D5),
`corpus/lessons/round-31.md` `## Gate` (`verifier_mode.py:35-38` → `:39-40`) and the round-30 lesson
erratum (`:78-81` → `:72`/`:82-83`) (D6), and round-30 lesson `:66` "S083/S086 peer-reviewed" (R7).

None is `corpus/README.md`. **Do not invent a README edit for C2.** The one ordering constraint C2 does
impose on the README work: R2 requires the round-32 report to be appended *after* the last lane commit
and to cite that tip, so all of (a)/(b)/(c)/d1/d2 must land in a lane commit that precedes the report
append.

---

## Evidence opened this round (what changed the wording)

All fetches via `curl` of single named files at pinned revisions; scratch under `/tmp/r32-frontier`
(68 KB). Access date 2026-10-25.

1. **S094 resolves, and the staged entry's tolerance is wrong.**
   `https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py`
   → HTTP 200, 14 138 bytes, sha256 `3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad`.
   - `:58` `def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1) -> None:` — the **default**.
   - `:279-280` `# Validate with 0.05% tolerance` / `validate_record_data(actual_records, expected_records, tolerance_pct=0.05)` — the **executed** path.
   The staged `benchmark-grader-semantics.md` (`:69`, "outside the 0.1-percentage-point tolerance") and
   the staged `SOURCES.append.md:24` anchor quote the default, not the call. **Correct
   the entry to 0.05 before admission** (Q10: numbers re-read by a second seat; a default that is never
   used is not the code's behaviour). This is a kill-rule-adjacent defect, not a wording preference.
2. **No judge in Toolathlon's scoring path.** `grep -cEi "openai|anthropic|llm|judge|chat/completions|rubric"`
   over the same file → `0` (exit 1). The staged entry's "no judge prompt and no rubric in the scoring
   path" holds; the frontier/coverage wording may state it.
3. **The log-bucket check fails open.** `:217-218` `print(f"Warning: Could not check abtesting_logging bucket: {e}")`
   then `return True  # Don't fail evaluation if we can't check logs`. A side-effect check that cannot
   see its own error is a grader-semantics fact neither round-31 entry nor the staged entry records.
4. **The bucket check is prefix-only and project-wide.** `:125` `check_storage_bucket_exists(bucket_prefix: str, project_id: str = "mcp-bench0606")`
   lists every bucket in the project (`:134` `buckets = list(storage_client.list_buckets())`) and passes on
   `bucket.name.startswith(bucket_prefix)` (`:136`) with prefix `promo-assets-for-b` (`:225`); on
   credential failure it shells out (`:150` `['gcloud', 'storage', 'buckets', 'list', '--project', project_id, '--format', 'value(name)']`,
   same prefix test at `:156`).
   So a bucket created by an earlier trial satisfies it — the check does not establish the bucket was
   created *by this task*.
5. **Retry semantics live outside the task file.** `:12` `from utils.evaluation.retry import grade_with_retry`;
   `utils/evaluation/retry.py` at the same commit (HTTP 200, 4 519 bytes) defaults
   `max_attempts: int = DEFAULT_MAX_ATTEMPTS` documented at `:61-63` as "Default 3 — i.e. 1 initial try +
   up to 2 retries", `poll_s` default 5 s. This bounds how much of a pass is retry absorption — keep it
   in the frontier's open list.
6. **S097 resolves verbatim.** `https://arxiv.org/abs/2412.05579` → HTTP 200, page carries
   `arXiv:2412.05579v2` and the abstract sentence "This paper presents a comprehensive survey of the
   LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications,
   Meta-evaluation, and Limitations." The staged `source:` line and the five-part frame are sound.
7. **S093 is already held, not new.** `corpus/SOURCES.md:112` is `S093 … | mined | 2026-10-25 | 180d | corpus/knowledge/benchmark-verifier-execution-model.md`.
   C1 needs that `used-by` cell to become
   `corpus/knowledge/benchmark-verifier-execution-model.md, corpus/knowledge/benchmark-grader-semantics.md`
   — comma-separated, exact-path parts, because `plans/adoption_check.py:96-99` matches the cell by
   `rel in [part.strip() for part in registry[row_id][10].split(",")]`, not by substring.
   Precedent for the multi-path cell: `corpus/SOURCES.md:33` (`llm-judge-calibration.md, attribution-interval-calibration.md`).
8. **S094/S097 are absent from the lane registry** (rows present: S090 `:103`, S091 `:104`, S092/S093/S100
   `:111-113`), so they are genuinely new rows as C1 states. The staged `SOURCES.append.md` carries both
   (rows at `:24` and `:27`) with tier A/B and quote anchors that match the files I fetched.

## Remaining unknowns

- **Toolathlon's other tasks.** Only `ab-testing` was fetched. Whether other tasks' `evaluation/main.py`
  files are also model-free state comparisons is unverified — hence the frontier wording's "for Toolathlon
  tasks whose `evaluation/main.py` differs from this one".
- **`utils/evaluation/retry.py`'s `DEFAULT_MAX_ATTEMPTS` constant value.** The docstring says 3; the
  constant's literal was not read (grep showed the docstring, not the assignment).
- **Whether the round-32 lesson plans to record the tolerance correction** as a source-location correction
  in the round-31 pattern (`lessons/round-26.md` §Source-location correction before admission). If the
  staged entry lands with 0.1, the correction must appear as an erratum, not a silent edit.
- **Coverage-map row is counter-invisible.** No frozen counter reads the coverage-map row for C1 or C3
  (`adoption_check.py` and `round32_c1_verify.py` read only the `| \`knowledge/…\`` index rows). Q7's
  "land together" is therefore an honour obligation this round; a reviewer must check it by eye.

## Tooling

No installs or upgrades this round. Read-only git only (`git log -S`, `git cat-file` not needed). Scratch
`/tmp/r32-frontier` holds two fetched files and one arXiv page, 68 KB total.
