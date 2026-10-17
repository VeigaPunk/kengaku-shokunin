# kengaku-shokunin — 見学

**LLM / model research and evaluation.** Selecting what a benchmark
actually measures, running it so the trace is replayable, and pricing
local findings against prior art.

A **shokunin lane**: an expert agent for one domain, minted and trained
under the [shokunin skill](https://github.com/VeigaPunk/shokunin).
Rank: **shonen**. Promotion is a named non-author review of
[`SHONEN.md`](SHONEN.md), never self-attestation.

This lane answers: *what did this model do on this task, and can a
stranger re-derive that number from committed bytes — without the
endpoint, without the original wiki?*

## Domain

From [`PROVINCE.md`](PROVINCE.md): eval craft, benchmark selection,
route telemetry as *historical inference about model service*, and the
hermetic grader in this repo.

The 2026-09-28 source of truth
`~/Projects/webzites/repos/llm-wiki` is **absent** as of 2026-10-15
(`corpus/evidence/round13-coverage/surface-receipt.json`). Wiki
citations in `SKILL.md` are dated historical observations. What this
lane retains is the digest set in `corpus/knowledge/` plus the rules
and probe trees that `grader.py` still replays.

**Not owned:** the model-serving plane (llama-server flags, KV cache,
slot/batch config) — report to the integrator. Quality of a *served
identity right now* is [kama](https://github.com/VeigaPunk/kama-shokunin).
Prompt/skill craft implications go to
[kotoba](https://github.com/VeigaPunk/kotoba-shokunin).

## What's here

| Path | Role |
|---|---|
| [`SKILL.md`](SKILL.md) | benchmark decision table, probe conventions, cited-source status |
| [`PROVINCE.md`](PROVINCE.md) | surfaces, refusals, and report-outs |
| [`grader.py`](grader.py) | hermetic offline replay of committed probe trees |
| [`corpus/knowledge/`](corpus/knowledge/) | eval digests (the wiki is gone; these remain) |
| [`corpus/evidence/`](corpus/evidence/) | durable run bytes — nothing headline-bearing from `/tmp` |
| [`SCORECARD.md`](SCORECARD.md) · [`LOG.md`](LOG.md) · [`SHONEN.md`](SHONEN.md) | axes, trail, promotion |

## The gate

```sh
python3 grader.py            # replay committed evidence; exit 0/1/2
python3 grader.py --selftest # corrupt temp copies; all must be caught
```

No network. No live endpoint. A green run means stored values re-derive
from stored raw bytes and pins — not that a model is “good”.

## How a lane learns

Append-only corpus; every claim separates observation / inference /
unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme).
