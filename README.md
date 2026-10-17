# kengaku-shokunin

LLM and model research, scored by instruments you can re-run.

Kengaku keeps the measurement: how a model behaved on a committed probe,
whether a number still matches the bytes that produced it, and what prior
art already claimed. It does not own the server that served the model, the
route that selected it, or the prompt craft that shaped the ask.

Rank: **shonen**. `SHONEN.md` is still here. Registered in the fleet
`MANIFEST.json` roster since 2026-09-28.

## Province

**Owns.** Eval craft distilled from the research notes, the local benchmark
battery, route-telemetry *inferences about model service*, client CLI
telemetry, model-catalog fields, and this lane's own probe artifacts.
`grader.py` replays committed evidence offline.

**Hands off.** The model-serving plane — flags, slots, batch config — which
the province says no lane owns; escalate it. Janitor credentials (kagi).
OMP route resolution (kumitate). Bounty ledger semantics (kasegi). Prompt
and skill rules (kotoba); this lane keeps the measured effect and hands the
craft implication out. Web properties (kake).

`PROVINCE.md` is the surface table, including which paths were already
absent or relocated when they were last re-verified. The scorecard banner
says the historical wiki, telemetry, and benchmark originals are
unavailable at the exact paths in
`corpus/evidence/round13-coverage/surface-receipt.json`. Retained digests
and response bytes are a different thing from those originals.

## Start here

1. `PROVINCE.md` — surfaces, then the refusal list.
2. `corpus/README.md` — the knowledge index. It names historical wiki
   paths as historical-unavailable. Leave those paths as written.
3. `grader.py` — the operability gate.
4. `SKILL.md` — the distilled eval rules.
5. `SCORECARD.md` — read the sub-axis note. `MISSION.md` assigns this lane
   `novelty`, and `AXES.md` has no such axis; the scorecard states the
   mapping it uses until the protocol lane rules.

## Grade the committed evidence

From the repository root:

```sh
python3 grader.py --selftest
python3 grader.py
```

The module docstring is the contract. Exit 0 means every recomputed value
matches the stored one. Exit 1 prints `MISMATCH` lines. Exit 2 means
missing or unreadable input. The grader does not call an endpoint and does
not use the network. A green grade is replay fidelity of the committed
trees, not a claim that a live model still behaves that way.

## The tree

| Path | What it is |
|---|---|
| `grader.py` | Hermetic replay of the committed probe trees |
| `corpus/evidence/` | Durable run bytes, per round |
| `corpus/knowledge/` | Digests and findings, each with its source line |
| `corpus/lessons/` | What the round established and what it refused to conclude |
| `plans/` | Round plans |

## Fleet

Minted under [shokunin](https://github.com/VeigaPunk/shokunin).
