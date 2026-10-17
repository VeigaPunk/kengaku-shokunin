# kengaku-shokunin

LLM and model research, and the evaluation craft around it: what a
benchmark is allowed to claim, how a local run is replayed, and how a
number stays tied to the bytes that produced it.

The 2026-09-28 source of truth was `~/Projects/webzites/repos/llm-wiki`.
`SKILL.md` records that path **absent** as of 2026-10-15
(`corpus/evidence/round13-coverage/surface-receipt.json`). Wiki citations
in the skill are dated historical observations. What the lane still holds
is the digest set in `corpus/knowledge/` and the rules in `SKILL.md`.

## The job

`PROVINCE.md` owns the research notes, the local benchmark battery (later
found under `~/archive/bench-arena/`), probe artifacts under
`corpus/evidence/`, the in-repo grader, and the public literature used to
price a local finding. Route telemetry at
`~/Projects/bounties/ledger/telemetry.jsonl` is recorded absent.

The lane does not own the model-serving plane (llama-server flags, slots,
batch config). That is escalated, not remediated here. It also refuses
kagi's credential config, kumitate's route resolution, kasegi's bounty
ledger, kotoba's prompt-craft rules (this lane keeps the *measured* effect
of a prompt on a benchmark), and kake's web properties. The shared word
"probe" carries no scope.

## The offline entry point

`grader.py` replays committed probe evidence with no endpoint and no
network. The module docstring is the contract:

```sh
python3 grader.py
python3 grader.py --selftest
```

Exit 0 means every recomputed value matches the stored one. Exit 1 prints
`MISMATCH <check-id>` lines. Exit 2 means missing, unreadable, or
unparseable evidence. `--selftest` corrupts temporary copies and requires
every corruption to be caught. A green grader re-verifies the committed
trees. It does not assert that a live model is still serving.

## Read this first

1. [`PROVINCE.md`](PROVINCE.md) — surfaces, which of them are absent, and the refusals.
2. [`SKILL.md`](SKILL.md) — the playbook, with the wiki path marked historical.
3. [`corpus/README.md`](corpus/README.md) — the knowledge index.
4. `grader.py` — the docstring at the top, then a run.

## On disk

| Path | Role |
|---|---|
| `SKILL.md` | Evaluation playbook. |
| `PROVINCE.md` | Surface table and report-outs. |
| `grader.py` | Hermetic replay of the committed probe trees. |
| `corpus/` | Knowledge digests and `corpus/evidence/` run bytes. |
| `plans/` | Round plans. |
| `SHONEN.md` | Promotion checklist. Rank is shonen. |
| `LOG.md`, `SCORECARD.md` | Audit trail and axis verdicts. |

## Fleet

Protocol and roster: [shokunin](https://github.com/VeigaPunk/shokunin).
Roster id `kengaku`, rank **shonen**.
