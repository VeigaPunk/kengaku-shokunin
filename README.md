# kengaku-shokunin — LLM / model research & evaluation

**Measure what a benchmark actually measures. Replay the numbers offline.
Never confuse a serving pin with model quality.**

This is a [shokunin](https://github.com/VeigaPunk/shokunin) lane. Rank:
shonen. Kengaku owns eval craft. It does not own endpoint health (that
is [kama](https://github.com/VeigaPunk/kama-shokunin)), prompt-file
craft (that is [kotoba](https://github.com/VeigaPunk/kotoba-shokunin)),
or the serving-plane flags on `llama-server` (unowned — escalate to the
integrator).

Every claim cites a local file, a command, or a named source. Host-
absolute paths in the skill are dated historical since the 2026-10-15
surface receipt. No oral tradition.

## Province

**Owns:** benchmark selection and anti-patterns; hermetic replay of
committed probe trees; digest of eval notes into `corpus/knowledge/`;
novelty pricing of local findings against public literature; this
lane's own `grader.py`.

**Refuses:** the model-serving plane (llama-server flags, slot / batch
config); janitor consumer-side endpoint / credential config (kagi); OMP
route resolution (kumitate); bounty-ledger mission-state (kasegi);
prompt- and skill-craft rules (kotoba — this lane keeps the *measured*
effect of prompt format and hands the reusable implication out); web
properties (kake).

Source status (2026-10-15): `~/Projects/webzites/repos/llm-wiki` is
ABSENT. What this lane retains is the digest set in `corpus/knowledge/`
plus the rules in `SKILL.md`. Route telemetry
(`~/Projects/bounties/ledger/telemetry.jsonl`) is also absent —
historical inference only. Full boundary: [`PROVINCE.md`](PROVINCE.md).

## Start here

1. [`SKILL.md`](SKILL.md) — benchmark decision table, anti-patterns, serving-stack pin.
2. [`grader.py`](grader.py) — hermetic offline replay of committed evidence.
3. [`PROVINCE.md`](PROVINCE.md) — surfaces, refusals, report-outs.
4. [`corpus/README.md`](corpus/README.md) — coverage map.

## The hermetic grader

No endpoint. No network. Stdlib only. A stranger can run it.

```
python3 grader.py            # grade the committed evidence
python3 grader.py --selftest # corrupt temp copies; all must be caught
```

Exit `0` every recomputed value matches the stored one · `1` at least
one `MISMATCH` · `2` missing or unparseable input. The grader replays
committed probe trees (r8 / r9 / r11 / r12) layer by layer: pin, meta
regeneration from seed, raw-record replay, stored aggregates. `--selftest`
is S0–S7.

A green grader says the committed numbers recompute. It does not say
the served model is up, the wiki tree is present, or the model is good.

## What's in the repo

```
kengaku-shokunin/
├── SKILL.md          executable eval craft
├── PROVINCE.md       surfaces + report-outs to siblings
├── SHONEN.md         promotion checklist
├── LOG.md            append-only audit trail
├── SCORECARD.md      axis verdicts
├── AGENTS.md         operating rules
├── grader.py         hermetic evidence-replay gate
├── plans/            round plans
└── corpus/           knowledge/, lessons/, evidence/, QUALITY.md
```

Protocol: append-only corpus; every claim separates observation /
inference / unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme) for how a lane
learns.
