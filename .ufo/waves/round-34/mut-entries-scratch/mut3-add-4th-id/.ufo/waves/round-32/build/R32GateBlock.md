# R32 Gate Block — adoption gate exercise (C1 preflight)

Seat: `L1Kengaku32.R32GateBlock` (leaf). Date: 2026-10-25.
Scope: exercise `plans/sources_adopt.py` for round-32 C1 in scratch only. **No production edits were made** — nothing under the lane repo was created or changed except this single report file; all gate outputs went to `/tmp/r32-R32GateBlock/` (scratch, well under 60 MB). No tools were installed (no new tool needed; `python3` already present).

Invocations run from the lane repo root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`:
- registry = `corpus/SOURCES.md` (91 rows)
- staged package = `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md` (read-only source)
- entries path passed to `--entries` = `corpus/knowledge/benchmark-grader-semantics.md` (the C1 entry's future lane path, used for the `used-by` cell)

---

## (a) Scoped adoption run (as specified)

Command:

```
python3 plans/sources_adopt.py \
  --registry corpus/SOURCES.md \
  --package /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md \
  --admit-ids S094,S097 \
  --entries corpus/knowledge/benchmark-grader-semantics.md \
  --access-date 2026-10-25 \
  --recheck 180d \
  --attest-opened \
  --scope-to-admit \
  --out /tmp/r32-R32GateBlock/block.md
```

Full output:

```
registry=91 staged=173 collisions=0 malformed=0 duplicates=0 defects=0 prose=2
  attested: the caller asserts every requested source was opened on 2026-10-25
  normalized recheck S094: 2026-10-23 — re-verify at the next upstream release (Gate S094 below)
  normalized recheck S097: 2026-10-23 — re-verify at the next revision (Gate S097 below)
wrote /tmp/r32-R32GateBlock/block.md rows=2
EXIT=0
```

Exit code: **0** (`EXIT_OK`). The block was built: `/tmp/r32-R32GateBlock/block.md` holds exactly two rows, `S094` and `S097`. Both rows in the built block carry the gate-applied mutations: `opened` re-dated to `2026-10-25` (attestation honored, `--attest-opened`), `recheck` normalized from prose (`2026-10-23 — re-verify at … (Gate S094/S097 below)`) to `180d` (`--recheck 180d`), and `used-by = corpus/knowledge/benchmark-grader-semantics.md`. Full built rows (11 cells each):

```
| S094 | Toolathlon task evaluation script (evaluation/main.py) — https://github.com/hkust-nlp/Toolathlon | code | A | the executed scoring code for one Toolathlon task at a pinned commit: what is compared, against what, and with what tolerance, for the code's own behaviour | commit 9be8d8fe07a497b18ee61e3f2ae694e9797f39eb, tasks/finalpool/ab-testing/evaluation/main.py: "def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1)" comparing a produced record.csv against groundtruth_workspace/expected_ratio.csv, plus check_abtesting_logging_bucket_clean() asserting no log bucket writes between launch and evaluation | the benchmark scores by comparing a *produced artefact* against a ground-truth artefact with a stated numeric tolerance, and checks the absence of side-effect writes — a state-based deterministic grader with no judge model in the loop | mined | 2026-10-25 | 180d | corpus/knowledge/benchmark-grader-semantics.md |
| S097 | LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods — https://arxiv.org/abs/2412.05579 | paper | B | the survey's own five-part structure for LLM-as-a-judge evaluation — functionality, methodology, applications, meta-evaluation, limitations — for the preprint's own text; tier B under row 10 because it was a preprint at the time of opening | arXiv 2412.05579v2 (submitted 7 Dec 2024, last revised 10 Dec 2024), Abstract: "This paper presents a comprehensive survey of the LMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations."; Comments: "60 pages, comprehensive and continuously updated" | the field's own survey separates *meta-evaluation* — how a judge is itself evaluated — from methodology and applications, which is the separation a calibration protocol needs; the limitations section is where a lane should look for the known failure modes of judge-based scoring | mined | 2026-10-25 | 180d | corpus/knowledge/benchmark-grader-semantics.md |
```

## (b) Refusal?

**(a) did not refuse** — it built the block and exited 0. So no defect category applies to the scoped run.

The refusal taxonomy exists, though, and is what `--scope-to-admit` bypasses (observed in the (c) run): the gate's refusal classes are `EXIT_COLLISION` (3, staged id already in registry), `EXIT_MALFORMED` (4, schema/status/escaped-pipe defects), `EXIT_REQUEST` (5, requested id absent from package, not mined, or not opened this round without attestation). In scoped mode these are narrowed to the admitted ids only.

## (c) Same run, `--scope-to-admit` omitted

Command: identical to (a) minus `--scope-to-admit` (and minus `--out`, same as (a)'s command line otherwise).

Output (summary and refusal lists; the 167 per-row defect lines are all identical in kind, so only the counts and the list of ids are reproduced):

```
registry=91 staged=173 collisions=14 malformed=2 duplicates=0 defects=167 prose=167
  collisions: S077 S078 S079 S080 S081 S082 S083 S084 S085 S086 S090 S091 S092 S100
  malformed: S093:escaped-pipe S101:escaped-pipe
  defect S077: recheck-prose
  … (defect S078 … S251: all 167 rows carry recheck-prose)
EXIT=3
```

Exit code: **3** (`EXIT_COLLISION`). Difference vs (a): without scoping, the gate refuses the whole staged package because of staged rows other than S094/S097 — 14 id collisions with the live registry (S077–S086, S090–S092, S100; e.g. the registry already holds its own S091/S093 rows), 2 malformed rows with escaped pipes (S093, S101), and 167 rows whose `recheck` cell is prose (S094 and S097 are among them). `--scope-to-admit` is exactly the opt-in that says "this round appends only S094/S097, so refuse only their defects"; with it, the unrelated staged rows' collisions/malformed/prose-recheck no longer block the two-row append.

## (d) Selftest

Command:

```
python3 plans/sources_adopt.py --selftest
```

Tail line (last line of output):

```
SELFTEST cases=17 failed=0
```

Exit code: **0**. All 17 cases PASS (collision-zero-indent, collision-one-space, collision-three-space, four-space-not-a-row, escaped-pipe-refused, prose-recheck-normalized, usedby-projected, duplicate-staged-id, clean-package-passes, missing-requested-id, quote-overlong-refused, quote-absent-refused, quote-located-accepted, quote-boundary-25-accepted, quote-url-bound-accepted, quote-url-mismatch-refused, quote-url-unmapped-refused).

---

## Verdict

VERDICT: block-built

The adoption gate is operable for C1: the specified scoped invocation produces the S094/S097 append block (2 rows, correct `opened=2026-10-25`, `recheck=180d`, `used-by=corpus/knowledge/benchmark-grader-semantics.md`) and exits 0; the selftest passes 17/17; the unscoped default correctly refuses on unrelated package defects (collisions/malformed/prose-recheck), which is the difference `--scope-to-admit` is documented to make.
