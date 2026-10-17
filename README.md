# kengaku-shokunin

**LLM and model research & evaluation — numbers a stranger can replay
offline.**

A **shokunin lane** minted and trained under the
[shokunin](https://github.com/VeigaPunk/shokunin) skill.

**Wiki:** [lane overview](https://app.devin.ai/org/veigapunk/wiki/VeigaPunk/kengaku-shokunin?branch=master)

## Domain

From `PROVINCE.md` and `SKILL.md`: benchmark selection, eval-craft
digests, route-telemetry interpretation, and the hermetic grader that
replays committed probe bytes. The 2026-09-28 source of truth was
`~/Projects/webzites/repos/llm-wiki`. That path is **ABSENT** as of
2026-10-15 (`corpus/evidence/round13-coverage/surface-receipt.json`).
What the lane retains is the digest set in `corpus/knowledge/` plus the
rules in `SKILL.md` — derived evidence, not original wiki bytes.

Host-absolute paths in the skill are dated historical observations.
Current offline entry point: `python3 grader.py`.

## What this lane does *not* own

The model-serving plane (llama-server flags, slot/batch config, KV
quantization) is unowned — escalate to the integrator. A process-level
pin is capability-*interpretation* evidence this lane keeps; flag-change
authority stays elsewhere. Serving identity *right now* is
[kama](https://github.com/VeigaPunk/kama-shokunin). Prompt-craft rules
are [kotoba](https://github.com/VeigaPunk/kotoba-shokunin) — kengaku
keeps the *measured* effect of prompt format on a benchmark and hands
the reusable implication out.

## In this repository

```
PROVINCE.md     surface table + report-outs
SKILL.md        benchmark decision table + gate registry
grader.py       hermetic evidence-replay grader
SHONEN.md  SCORECARD.md  LOG.md
corpus/
  knowledge/    eval digests, bench-arena notes, prior-art
  evidence/     committed probe trees (r8–r14 and later)
  lessons/
```

## Grade the committed evidence

No endpoint. No network.

```bash
python3 grader.py            # every recomputed value matches the stored one
python3 grader.py --selftest # corrupt temp copies; all must be caught
```

Exit `0` = match · `1` = `MISMATCH` · `2` = missing / unreadable input.
Pins are checked only when the default in-repo paths are graded.

## How a lane learns

Append-only corpus; every claim separates observation / inference /
unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme).
