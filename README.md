# kengaku-shokunin — model research and evaluation

The question this lane answers is how a model-evaluation claim is replayed from committed evidence, not how a serving flag is changed (`PROVINCE.md`, `grader.py`).

**Rank:** `SHONEN.md` boxes are `[~]`. The notes distinguish historical verifier passes from a current outside non-author review, and they say that review was not performed. That is not a promotion.

## Owns / refuses

Owns the domain knowledge, playbooks, error patterns, and checklists for LLM and model research and evaluation, including route-telemetry history and the in-repo replay gate (`PROVINCE.md`).

Refuses the model-serving plane (llama-server flags, slot and batch config): escalate, do not remediate. Also refuses kagi's consumer-side endpoint and credential config, kumitate's route resolution and operational failure taxonomy, kasegi's bounty-ledger mission state, kotoba's prompt and skill craft, and kake's web properties. The shared word "probe" carries no scope (`PROVINCE.md`).

`PROVINCE.md` records several original surfaces as absent or relocated (the llm-wiki path, the benchmark battery's old path, route telemetry). Hermetic gates pin committed bytes. They do not read `/proc`.

## Start here

`grader.py` documents the offline replay:

```sh
python3 grader.py
python3 grader.py --selftest
```

Exit `0` means every recomputed value matches the stored one. Exit `1` means at least one mismatch. Exit `2` means missing, unreadable, or unparseable evidence. `--selftest` corrupts temporary copies and requires those faults to be caught. It does not call an endpoint and does not use the network (`grader.py` docstring). `PROVINCE.md` describes the gate as a hermetic replay of four probe trees.

## How to read the corpus

`corpus/README.md` is the evidence index. Reports and lessons cite it by line (`corpus/README.md:57-59`, `corpus/README.md:73-91` in the round-10 and round-23 drafts), so it was not reflowed. `corpus/evidence/` holds the durable run bytes. `corpus/knowledge/` holds the eval notes. `corpus/lessons/` holds the round lessons. `PROVINCE.md` §Source availability, as cited from `SHONEN.md`, separates historical-unavailable originals from retained digests.

## Map

| Path | What it is |
|---|---|
| `PROVINCE.md` | Surfaces, refusals, report-outs |
| `SKILL.md` | Decision tables and checklist |
| `SHONEN.md` | Checklist, `[~]` with the review gap named |
| `LOG.md` | Append-only record |
| `SCORECARD.md` | Axis verdicts |
| `AGENTS.md` | Operating rules |
| `grader.py` | Offline evidence replay |
| `corpus/` | Evidence, knowledge, lessons, index |
| `plans/` | Round plans |
| `.ufo/` | Round machinery |

## Neighbors

kama (is the endpoint the model the config names), kagi (credential-bearing consumers), kumitate (route mechanism), kotoba (prompt craft), kasegi (ledger mission state). Report-outs are listed in `PROVINCE.md`. They are not absorbed.

Fleet protocol: [VeigaPunk/shokunin](https://github.com/VeigaPunk/shokunin).
