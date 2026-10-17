# kengaku-shokunin

**LLM / model research and evaluation.**

Kengaku owns how a model is *measured*: which benchmark family fits a
task class, what a number actually measured, contamination and
construct-validity cautions, and hermetic replay of this lane's own
probe trees. It does not own serving (kama) and it does not own
prompt-craft rules (kotoba) — it keeps the *measured effect* of a
prompt format and hands the reusable craft implication out.

This is a **shokunin lane** of the [shokunin fleet](https://github.com/VeigaPunk/shokunin).
Rank: **shonen**.

## The craft

- Task-class → benchmark mapping, with contamination status
  (`corpus/knowledge/benchmark-selection.md`).
- Eval-design digests (reference-class, autonomy slider, Goodhart,
  ReAct failure classes) retained in `corpus/knowledge/`.
- Identity of a served local model is *re-probed* when the endpoint
  exists; serving-flag authority stays unowned (integrator).
- Hermetic offline grader over committed probe trees — the current
  offline entry point when live surfaces are gone.

**Source status (2026-10-15).** The research SSOT
`~/Projects/webzites/repos/llm-wiki` is **ABSENT**. Wiki citations in
`SKILL.md` / `PROVINCE.md` are dated historical observations. What
this lane retains is the digest set in `corpus/knowledge/` plus the
rules in `SKILL.md`. Route telemetry
(`~/Projects/bounties/ledger/telemetry.jsonl`) is also absent.
See `corpus/evidence/round13-coverage/surface-receipt.json` and
`corpus/README.md`.

## Province

Owns: LLM / model research & evaluation — eval craft, benchmark
selection, probe artifacts, the in-repo grader.

**Refuses:** the model-serving plane (flags, slot/batch config —
unowned; escalate), janitor consumer credentials (kagi), OMP route
resolution (kumitate), bounty-ledger mission-state (kasegi),
prompt/skill *craft rules* (kotoba), web properties (kake). Domain
source repos are read-only.

See [`PROVINCE.md`](PROVINCE.md).

## What's in this repository

```
kengaku-shokunin/
├── SKILL.md            benchmark tables, anti-patterns, production checklist
├── PROVINCE.md         surfaces + report-outs (append-only)
├── SHONEN.md           promotion checklist
├── LOG.md              append-only trail
├── SCORECARD.md        per-axis verdicts
├── AGENTS.md
├── grader.py           hermetic offline replay of committed probe trees
├── plans/
└── corpus/
    ├── README.md       coverage map + source-availability
    ├── knowledge/      retained digests
    ├── lessons/
    └── evidence/       per-round probe trees (r8–r14, …)
```

## Start here

From this repo root — no network, no live model required:

```sh
python3 grader.py
python3 grader.py --selftest
```

`grader.py` hermetically replays committed probe trees (r8 / r9 / r11 /
r12 as pinned in `PROVINCE.md`). Exit 0 / 1 / 2. It grades *this
lane's recorded bytes*, not a new model's quality.

Then read [`SKILL.md`](SKILL.md) against the digests, not against the
absent wiki originals.

## How a round works

One axis-move, typically novelty + calibration. Lane identity:
`kengaku-shokunin <kengaku@shokunin.local>`.

## Fleet

[VeigaPunk/shokunin](https://github.com/VeigaPunk/shokunin) ·
[kimi-shokunin](https://github.com/VeigaPunk/kimi-shokunin)
