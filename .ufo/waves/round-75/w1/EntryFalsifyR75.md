# EntryFalsifyR75 — held-entry / index boundary

Axes: coverage and calibration. Read-only review; recommendation only, not admission. Frozen claims read in full before shell execution. No production edits, commits, clones, tool installations, or subagents. Review covers the live integration working tree: both executed audits stamped `LANE_TIP 43255758ed7d74ea05c8e03686dd9ad37837f0cd` and `WORKTREE dirty`; this is not a clean landing-tree attestation.

## Findings by severity

### Medium — existing held candidate fails Q1; indexing cannot repair it

`corpus/knowledge/registry-argv-and-flag-audit.md:1–3` opens with YAML, not the mandatory provenance trio. Its `source:` is at line 16, `verified-at:` at line 8, and `recheck: on-release` at line 9 names no re-check action. This fails `corpus/QUALITY.md` Q1 (lines 15–19), independently of Q10/Q13/Q14 review timing. The `admission: hold` at line 11 is honest; neither the new README row nor a green C2 audit clears this defect. Current `corpus/lessons/round-75.md` M75-8 already records this held-entry defect. No frozen-predicate change is proposed.

### Low — round-75 lesson overstates held-row labelling and omits one held candidate

`corpus/lessons/round-75.md:30–32` says “The three held candidates stay held” and says their README rows are marked `admission: hold`. However, `corpus/README.md:96` indexes `tb2-hf-model-inference-provenance.md` without that label; line 95 likewise indexes `tb2-hf-model-inference-offline.md` without it, despite its own line 6 explicitly holding admission. Thus all four inspected entries are held, and only the two new registry-entry rows at README lines 920–921 visibly carry the literal hold label. The lesson's assertion is not reproduced. This does not make any entry admitted; it makes the discovery surface less honest than the entries themselves. Recommend correcting the lesson's inventory/label assertion and visibly preserving both HF entries' hold status in index prose, under the repo's correction discipline.

Evidence: `functions.grep` pattern `^(source:|verified-at:|recheck:|admission:)` over all four files returned four hold markers; `functions.grep` pattern `instrument-registry-derivation|registry-argv-and-flag-audit|tb2-hf-model-inference-offline|tb2-hf-model-inference-provenance|admission|held` over README located rows 95–96 and 920–921. Exact ranged reads of README and lesson confirmed the quoted bytes. Tool searches do not expose shell exit codes; their returned lines are the evidence, not invented rc values.

## Entry inventory and actual first three lines

### `corpus/knowledge/instrument-registry-derivation.md`

Marker, line 6: `admission: hold — requires a qualifying second-seat reread satisfying corpus/QUALITY.md Q10/Q13/Q14; no admission is inferred from structural audit output.`

Actual first three lines:

```text
source: S249 (corpus/SOURCES.md) — Python ast documentation — https://docs.python.org/3/library/ast.html#ast.parse; supporting anchors #ast.PyCF_ONLY_AST and #ast.walk; captured passages and live-fetch provenance: corpus/evidence/round73/sources/ast-anchor.md, sections “Grounding” and “ast.walk anchor”.
verified-at: 2026-11-04 UTC, round-73 freeze/base d96c3e62fd01771718368688c2685dceeef5b83e; freeze declaration: plans/round-73-claims.md opening. This identifies the declared base, not an independently verified landing tip.
recheck: on-release — From the lane root: python3 plans/round52_c2_registry.py --lane . ; python3 plans/round73_c2_registry_audit.py --lane . ; compare complete output and exit codes with plans/round-73-claims.md, not merely the final predicate token; source recheck: corpus/evidence/round73/sources/ast-anchor.md §Reproduction.
```

Q1 structural opening present, including cadence/action. Not a source-truth or admission certification. Round-75 claim citation: no literal entry/S249 citation in claims; lesson line 31 mentions only its held status. No load-bearing technical claim from this entry is explicitly attributed in these two documents.

### `corpus/knowledge/registry-argv-and-flag-audit.md`

Marker, line 11: `admission: hold`.

Actual first three lines:

```text
---
title: "Registry argv and flag audit — grounding command syntax against executable contracts"
branch: eval
```

Triad exists elsewhere, not at the opening: `verified-at: 2026-11-04 (L1 live fetch, HTTP 200; capture sha256 ad9095cdaa99c953046f510d6cd86cd6f7a1086c5aa35743c26e3fa41e4b5b8d)` (line 8); `recheck: on-release` (line 9); source at line 16 is S250, Python 3.15.2 argparse docs, `https://docs.python.org/3/library/argparse.html#name-or-flags`, capture `corpus/evidence/round74/sources/argparse-docs.html`, sha256 `ad9095cdaa99c953046f510d6cd86cd6f7a1086c5aa35743c26e3fa41e4b5b8d`, line 908. Q1 fails as above.

Round-75 claim citation: **shared source/teaching yes, entry-as-authority no**. `plans/round-75-claims.md:17–18,70–71` explicitly invokes S250's reject-flip; lesson lines 25–29 rejects flag-string presence as proof of argparse acceptance. This overlaps the entry's lines 30–33, but both round documents ground the rule in S250 / round-74 rejection, not an admission of the held note. Lesson line 31 names the entry only as held. Held status must not be used to negate the independent source citation, nor source citation to imply entry admission.

### `corpus/knowledge/tb2-hf-model-inference-offline.md`

Marker, line 6: `admission: hold — the QUALITY Q13/Q14 second-seat re-read is not yet on record; see corpus/lessons/round-71.md ## Gate (Admission status).` (The original puts backticks around the lesson path and heading.)

Actual first three lines:

```text
source: S245 (corpus/SOURCES.md) — Terminal-Bench 2.0 task `hf-model-inference`, task instruction at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/hf-model-inference/instruction.md — anchor: `instruction.md:3-7,11-28` — sha256 `29151c5b2306f522f38fa905de3d34566865829355e5ca0895f4fca04d51dcc1`; and S246 (the grader) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/hf-model-inference/tests/test_outputs.py — anchor: `tests/test_outputs.py:8-107` — sha256 `61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857`
verified-at: 2026-11-03 (live re-fetch at the pin: instruction HTTP 200, 1264 bytes, sha256 `29151c5b…d1cc1`; grader HTTP 200, 4239 bytes, sha256 `61a686d6…87857`; both `cmp` byte-identical to the committed captures `corpus/evidence/round71/hf/instruction.md` and `corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py`; model tree `c5c25767…8944` re-derived from the five committed files)
recheck: pinned at `2fd12b88aafdd04a52c298e3940bcb189f9766d6` (an immutable commit): `python3 plans/round71_c1_hf_probe.py --lane . --work <scratch> --port-lock <port-5000.lock> --receipt <path> --evidence-dir <path>` must reproduce the eight frozen vectors of `plans/round-71-claims.md`; `sha256sum corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py` must print `61a686d6…87857`; `--check-receipt` prints `DEFECTS n=0` / `PREDICATE R71-C1 pass`.
```

Q1 opening present; the immutable pin/action is explicit, but no separate ISO recheck date/cadence is named. Literal Q1 permits only ISO date or cadence, so immutable-pin-as-cadence is an unresolved interpretation, not an unconditional Q1 pass. Round-75 claims/lesson: no entry-name or S245/S246 load-bearing citation returned by the bounded sweep.

### `corpus/knowledge/tb2-hf-model-inference-provenance.md`

Marker, line 6: `admission: hold` with the explicit reason that Q13/Q14 second-seat re-read is not yet recorded from a `w2`/`falsify` registry, pointing to round-72 Gate.

Actual first three lines:

```text
source: S245 (corpus/SOURCES.md) — Terminal-Bench 2.0 task `hf-model-inference`, instruction at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/hf-model-inference/instruction.md — anchor: `instruction.md:3` — sha256 `29151c5b2306f522f38fa905de3d34566865829355e5ca0895f4fca04d51dcc1`; S246 (the grader) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/hf-model-inference/tests/test_outputs.py — anchor: `tests/test_outputs.py:103-107` — sha256 `61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857`; S247 (the sandbox manual) — https://man.archlinux.org/man/bwrap.1.en — anchor: the `--clearenv` entry — sha256 `708f56eed930f9a0b524fd79b8d9db92c4c35eb246646c4b0fab0812d7e68de7`; S248 (the checkpoint the task names) — https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english/raw/main/README.md — anchor: `README.md:145` — sha256 `75f17282923fea5b541df92640e2d8646c4ff5e8e3e16ed0a7e4e50ee7588851`
verified-at: 2026-11-03 (S247 and S248 fetched live this round: HTTP 200, 27981 and 10512 bytes, sha256 as above, captures at `corpus/evidence/round72/sources/`; S245/S246 re-derived from the committed captures `corpus/evidence/round71/hf/instruction.md` and `corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py`)
recheck: `python3 plans/round72_c1_hf_probe.py --lane . --work <scratch> --port-lock <port-5000.lock> --receipt <path> --evidence-dir <path>` must reproduce the nine frozen vectors of `plans/round-72-claims.md`; `python3 plans/round72_c1_hf_probe.py --lane . --check-receipt <path> --work <scratch>/check` prints `DEFECTS n=0` / `PREDICATE R72-C1 pass`; `python3 plans/round72_c2_routed_defects.py --lane .` prints `E1a ok … E2 ok`, `DEFECTS n=0` / `PREDICATE R72-C2 pass`.
```

Q1 ordering present, but recheck has action only, no ISO date/cadence: a further held-entry Q1 defect under the literal rule. Round-75 claims: no entry/S245–S248 citation; lesson line 32 names only held status, not technical support for either predicate.

Bounded citation sweep actually run through `functions.grep`: `instrument-registry-derivation|registry-argv-and-flag-audit|tb2-hf-model-inference-offline|tb2-hf-model-inference-provenance|S24[5-9]|S250|admi|hold|Q1` over `plans/round-75-claims.md` and `corpus/lessons/round-75.md`; later sweep `S250|S249|S245|S246|S247|S248|instrument-registry|registry-argv|tb2-hf|admission|knowledge` reproduced the distinction. These are lexical findings, not semantic proof of all possible paraphrases.

## Independent C2 execution

Commands run from the lane root, with bytecode writes disabled and explicit seat-owned scratch (the default `--work` would create shared scratch even for verdict-only execution):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 plans/round75_c2_registry_audit.py --lane . --work /fast/scratch/hyaku/kengaku-r75/EntryFalsifyR75/verdict
```

Exit **0**, output:

```text
LANE_TIP 43255758ed7d74ea05c8e03686dd9ad37837f0cd
WORKTREE dirty
D1 ok n=0
D2 ok n=0
D3 ok n=0
D4 ok n=0
MALFORMED ok n=0
FLAGS ok n=0
TEXT-FALLBACK n=0
INSTRUMENTS total=118 rows=118
PARSED scripts=118 failed=0
MISMATCH 0
DEFECTS n=0
PREDICATE R75-C2 pass
```

Also ran the full frozen mode independently:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 plans/round75_c2_registry_audit.py --lane . --mutants --check-stamps corpus/evidence/round75 --work /fast/scratch/hyaku/kengaku-r75/EntryFalsifyR75/full
```

Exit **0**, same baseline lines, plus:

```text
MUTANTS real=9 expected_matched=9 wrong_id=0 survived=0 null_arms=1 null_survived=1 total=10
STAMPS files=8 stamped=8 unstamped=0 unresolved=0 not_ancestor=0
PREDICATE R75-C2 pass
```

Do the four files change a C2 leg? **No knowledge-entry admission/content leg exists.** Canonical logic: `plans/round75_c2_registry_audit.py:229–247` delegates D1/D2/D3/D4/MALFORMED to R74 and adds FLAGS; `round74_c2_registry_audit.py:231–240` derives rows from SKILL, parses entry scripts, prices row declarations, detects duplicates, and checks round-71 errata. R75 FLAGS reads registry-named scripts (`:82–104`), mutant fixtures are created independently (`:167–227`), and stamps enumerate evidence `*.txt` (`:133–165`). These paths do not read the four knowledge entries or their admission markers. This is a source-read dependency conclusion, not a deletion experiment (none was authorized/performed). Their presence affects C1's disk/index universe, not C2's admitted knowledge count. Existing file presence may contribute to the generic WORKTREE dirty stamp if modified, but that stamp is not an admission verdict or a failing baseline leg.

## Rule interpretation: index ≠ admission

**No numbered admission rule makes a README row sufficient for admission.** `corpus/QUALITY.md:12–13` requires every admission row to pass and Gate to record entry decisions. Q1 is provenance structure; Q2 scoped A/B support; Q3 anchored bounded quotation; Q4 negative space; Q5 honest source labelling; Q6 named extension/supersession. Index-row existence establishes none of those. Q7 (`:56–58`) requires entry/index/coverage row to land together: necessary discoverability, not an alternative sufficient admission mechanism. Q10/Q13/Q14 add independent reread and admission-time support.

Fleet `../CORPUS.md` SOURCES contract **rule 3** (`:119–122`): “No second method. Claim admission stays in corpus/QUALITY.md”. **Rule 4** (`:123–125`) counts admitted knowledge, not rows, for expansion. README's own `:873` explicitly says: “A row here indexes a file; it does not admit it — the held entries stay held.” The held candidates must be indexed by C1's unfiltered universe while remaining unadmitted.

Two phrases are ambiguous if read alone:

- `../CORPUS.md:70`: “corpus/knowledge/ holds admitted facts”. A cold reader could infer that directory membership itself certifies admission, conflicting with four explicit holds stored there. This is a layout-description ambiguity, not permission to bypass numbered rule 3 or QUALITY's conjunction. It matters because unlabelled index rows 95–96 look like ordinary admitted inventory.
- `../CORPUS.md:46`: “An index row is a claim. Write the row when the file exists, not before.” The heading does not say what kind of claim; the next sentence binds it to existence. It must not be widened into admission or source-truth certification (Q3/Q4/Q5). Its scope matters when reporting C1 as coverage: parity certifies inventory links, not epistemic acceptance.

Q7's same-commit rule can also be misread as banning discovery repairs for old held files. Read under its admission-bar heading, it constrains an admitting landing; it does not authorize calling today's repair an admission. No admission claim was observed in the frozen C1 sentence.

## Residual risk, verification gaps, cleanup

- Semantic tooling unavailable: `read xd://lsp` returned `No such tool: xd://lsp`; no LSP status/references/definition/diagnostics device could be invoked. Used literal grep and targeted source reads, not semantic proof.
- No external sources were re-opened and no Q2–Q6 or Q10 source-truth reread was certified. Dates, hashes and historical counts in quoted metadata are transcription evidence, not newly reproduced historical runs.
- No C1 verdict or Q13 timing test run by this seat; no clean landing clone checked. C2 executions above are actual dirty-worktree results, not a claim of clean-tip acceptance. Live sibling changes were observed in the lesson/README while reviewing; cited findings name the actual ranged-read snapshot.
- `rm -rf /fast/scratch/hyaku/kengaku-r75/EntryFalsifyR75` executed, exit **0**. No owned scratch retained.

Self-evaluation: accuracy 4/5 (dirty live tree limits revision attribution); completeness 4/5 (all assigned entries and C2 modes covered, no independent source reread); clarity 4/5 (literal-rule versus source-citation distinction explicit, long metadata unavoidable); actionability 4/5 (label/lesson and Q1 defects concretely located); conciseness 4/5 (full first-three-line quotations required). Mean 4.0. Improvement priority: bind the final integration report to the clean landing revision; preserve visible hold labels in every inventory row. Would the user agree? The report distinguishes exercised commands from unrun admission certification.
