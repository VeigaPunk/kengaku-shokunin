# r13-knowledge-sources — source-availability annotations on the twelve fixed candidates

Seat `R13KnowledgeSources` (executor), round-13 re-dispatch, 2026-10-15.
Baseline commit `3f31e54c6e7aeddef13db11985b3c7a9dad9e0cf`. Advisory lane
evidence; lane-dispatched, not an outside learning/promotion check.

## What changed

One additive fenced annotation block was inserted in each of the twelve
`source_candidates` fixed in `surface-receipt.json` (lines 46–59), placed
after the existing title/source paragraph so the cited source lines stay at
their baseline positions. Every block carries the five fields, in this order:

```
source-status: historical-unavailable
original-source: <actual missing original root/path(s) + historical read/profiling date>
availability-evidence: corpus/evidence/round13-coverage/surface-receipt.json observed 2026-10-15T04:49:50Z — <receipt-scoped absences>
retained-evidence: baseline 3f31e54 digest sha256=<H> of this entry; <true retained raw if any> — digest/transcription explicitly NOT recovered original bytes
recheck: test -e <exact original path> && echo present || echo absent
```

Nothing else was touched: titles, `Source:` paragraphs, counts, historical
claims and body content are byte-identical. The other eleven knowledge
entries received no edits (verified: only 12 files contain the marker).

## Parent spot-check response (message received mid-wave)

Each block names: the actual source path; the historical read/capture date
carried into `original-source` (the date is recorded, not re-verified —
this is source-availability date only); the receipt pointer with its
observed timestamp in `availability-evidence`; and the retained-digest vs
original-bytes distinction in `retained-evidence`. Multi-source scoping:
`historical-unavailable` labels only the named host-local original path(s).
Where an entry's evidence lives elsewhere, the block says so —
`local-model-index.md` scopes out the public HF/OpenRouter sources (owned by
`open-model-catalogs.md`, untouched); `gemini-benchmark-suite.md` scopes out
its in-repo SKILL.md citation; `bench-arena-fresh-run.md` names the one
genuinely retained raw file (`corpus/evidence/round10-fleet/models-34113.json`,
a historical endpoint capture, "not a live model").

## Per-file table (original source → baseline digest)

| candidate | missing original (receipt rows) | historical read/profiling | baseline-3f31e54 sha256 (of the pre-annotation entry) |
|---|---|---|---|
| bailian-cli-telemetry.md | `~/.bailian/telemetry.jsonl` | 2026-09-28 | `3a95b8e49ffc3253c65275803530631138ee27afddbd2b008cb3a0804d9b08c6` |
| bench-arena-fresh-run.md | `~/bench-arena/` + `~/archive/bench-arena/`, service unit, jinja template, `:34113/health` refused | run 2026-09-28 | `b17665c24447549fceb37c5e6cdd998ea6ef73f73c5ee1cdbdb0996c67459f0e` |
| benchmark-selection.md | `.../llm-wiki/wiki/ai/agents-and-engineering/benchmark-shortlist-for-godspeed-research.md` | read 2026-09-28; note dated 2026-04-09 | `df1f059bf60ba869cab6b407cb9816ce3761f25556587eb8df814dc5a33154e9` |
| eval-design-digest-2.md | `.../llm-wiki/wiki/` (karpathy, gwern-essays, philosophy, ai/foundations, ai/books) | 2026-09-28 | `6549758ee5d10bac6b41d5fbc30761fb93753420b6d2c16652da8291813cb268` |
| eval-design-digest-3.md | `.../wiki/ai/scaling-and-forecasting/scaling-hypothesis-revisited.md` + `.../papers/react-reasoning-acting.md` | read in full 2026-09-28 | `7b6feb1afbe287bd65666550421a6e84576572a4360ccb146ce7e97026d58fed` |
| eval-theory-notes.md | `.../llm-wiki/wiki/` — yao-second-half, creative-benchmark, llm-trueskill-sorting, rlhf, bitter-lesson | 2026-09-28 | `5d2dd69b6aa8435810e3d3a3a8769548796463b635f2a02478ca8ec8ad568165` |
| gemini-benchmark-suite.md | `.../wiki/ai/agents-and-engineering/gemini-3.1-pro-godspeed-benchmarks.md` + `gemini-3.1-pro-godspeed-test-battery.md` | 2026-09-28 | `ea81dece718ec452866c281e4a71bb56932c39073b513940e327325e1930a5f2` |
| godspeed-eval-findings.md | `.../wiki/ai/agents-and-engineering/godspeed-umwelt-iteration-2.md` | read 2026-09-28; note dated 2026-04-09 | `f381fbe4fcea9d0a7087ad223ccb37f9430ba71604c8f97c2a113c8146193bd9` |
| ledger-route-telemetry.md | `~/Projects/bounties/ledger/telemetry.jsonl` | profiled 2026-09-28 | `76f6d2855c035521266dbc2c3969772a6f47fd52d4d437d58824995dc6856ae3` |
| local-bench-arena.md | `~/bench-arena/` (both roots) | verified by ls/DictReader 2026-09-28 | `c6a47b4e82fd12beefd85b7ea218a2bb4f6dde03b14498f80d5dbd4e71e4cd1a` |
| local-model-index.md | `~/.bailian/skills/bailian-docs-llm-wiki/models/` + `~/.bailian/wiki-sync-state.json` | generated 2026-09-11, head-verified 2026-09-28 | `342d15ed12e57651ede44ef89c0d42d5a47dc5489afe00c73782ccb89a153319` |
| telemetry-run-design.md | `.../wiki/ai/agents-and-engineering/godspeed-umwelt-iteration-3-alpha-shittycodex.md` (+ `godspeed-umwelt-iteration-3.md` same root) | read 2026-09-28; note dated 2026-04-09, status: plan | `f5f49ae1403ab922b2235f84f5667ca1094275d74068bee8df122a0d74284394` |

Digest honesty: the sha256 values were computed from the working tree at
baseline 3f31e54 (`git status --porcelain -- corpus/knowledge` empty) BEFORE
this seat's annotation, and every block labels them "baseline 3f31e54 digest".
Post-annotation each entry's own digest differs; no block claims otherwise.
No entry's cited digest is an original-source digest — no original bytes were
ever retained for any of the twelve (searched: no raw `.bailian`/ledger/
bench-arena/wiki bytes committed anywhere under `corpus/`; the only true
retained raw in-scope is the r10 endpoint JSON named above).

## Independent countability (author's prediction for the parent census)

- `grep -rc '^source-status: historical-unavailable$' corpus/knowledge/` → 1
  in each of the twelve candidates, 0 in the other eleven entries (12 files
  total contain the marker).
- Each field `^original-source:`, `^availability-evidence:`,
  `^retained-evidence:`, `^recheck:` occurs exactly once per annotated file.
- Marker line positions: 8–16 → all inside the first 24 lines.
- Twelve measured files now sum to 2236 lines (2116 baseline + 12×10).

## Line-shift map for historical citations

Each insertion adds exactly 10 lines after the baseline insertion point;
later lines in that file shift +10 (earlier lines unchanged). Known affected
citations: `eval-design-digest-2.md:47,82-83,109` → `57,92-93,119`;
`ledger-route-telemetry.md:8` → `18`. Preserved at baseline positions:
`bailian-cli-telemetry.md:3`, `benchmark-selection.md:3`,
`eval-theory-notes.md:3-6`, `eval-design-digest-3.md:1-10`,
`ledger-route-telemetry.md:3`. Index parity unaffected (no renames, titles
unchanged; knowledge remains 23 files / 23 README rows for this seat's scope).

## Limits and risks (not repaired by this seat)

- Inherited receipts accepted without rerun: the eight absent paths and the
  ECONNREFUSED endpoint come from `surface-receipt.json`; the authored
  `recheck:` commands were NOT executed by this seat — their validity is
  syntactic (POSIX `test -e`), for future operators only.
- Status is exact-path scope only; no absence-everywhere claim, no restored
  source, no live model, no public-URL refetch, no scientific re-verification.
  Coverage anchor stays 7 under the declared-but-unresolvable-surface cap.
- Parent owns README/SHONEN/SCORECARD/LOG/lesson updates, the after-census,
  gates and commits; the pre-edit baseline digests above should be recorded
  as of 3f31e54 before commit changes the tip.
- Present-tense surface claims outside the twelve lane files (PROVINCE.md,
  README rows, and knowledge entries whose first 12 lines do not match the
  receipt's source pattern — the candidate set was fixed at twelve) were not
  annotated here; the wider census belongs to the parent.
