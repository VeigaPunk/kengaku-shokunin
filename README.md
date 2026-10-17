# kengaku-shokunin

LLM and model research and evaluation: which benchmark measures which
task, what a local probe actually showed, and how to replay that evidence
after the original files are gone.

Rank: **shonen**. [`SHONEN.md`](SHONEN.md) marks its boxes `[~]` — the
lane's own pointers, not a non-author promotion review.

Fleet: [shokunin](https://github.com/VeigaPunk/shokunin).

## The question

> What did this evaluation measure, on which bytes, and can those bytes
> be replayed without the endpoint?

The 2026-09-28 source of truth was `~/Projects/webzites/repos/llm-wiki`.
`SKILL.md` records that path absent as of the 2026-10-15 surface receipt.
What this repository retains is the digest set in `corpus/knowledge/` and
the probe trees under `corpus/evidence/`. Digests are derived evidence.
They are not the original wiki bytes.

## Boundary

**Owns:** eval craft as recorded here, the hermetic grader, and the
lane's own probe artifacts.

**Hands off:** the model-serving plane (llama-server flags, slots, batch
config) — reported to the integrator. Credential config (kagi). Route
resolution and operational failure taxonomy (kumitate). Bounty ledger
semantics (kasegi). Prompt and skill craft (kotoba) — this lane keeps the
measured effect of a prompt on a benchmark and hands the reusable craft
out. Web properties (kake).

Serving-plane numbers cited from `:34113` are historical interpretation
evidence. Flag changes stay unowned.

## Replay

Offline. No endpoint, no network.

```sh
python3 grader.py
python3 grader.py --selftest
```

Exit `0` when every recomputed value matches the stored one, `1` on a
mismatch (`MISMATCH <check-id>`), `2` when input is missing or
unparseable. The module docstring is the layer list: pins, meta, replay.

## Map

| Path | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | benchmark decision table, anti-patterns, checklist |
| [`PROVINCE.md`](PROVINCE.md) | surfaces, with absence notes |
| [`grader.py`](grader.py) | hermetic evidence replay |
| [`corpus/knowledge/`](corpus/knowledge/) | retained digests |
| [`corpus/evidence/`](corpus/evidence/) | durable probe bytes |
| [`corpus/README.md`](corpus/README.md) | index, including which originals are historical-unavailable |
| [`LOG.md`](LOG.md), [`SCORECARD.md`](SCORECARD.md) | rounds and axis verdicts |

Read `corpus/README.md` before citing a knowledge file outward. Several
rows name the original wiki path as historical-unavailable on purpose.
