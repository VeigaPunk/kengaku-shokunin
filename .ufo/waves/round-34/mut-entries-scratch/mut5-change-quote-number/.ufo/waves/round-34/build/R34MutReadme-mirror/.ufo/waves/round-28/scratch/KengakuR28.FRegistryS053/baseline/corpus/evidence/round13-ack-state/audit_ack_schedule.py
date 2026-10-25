#!/usr/bin/env python3
"""Recompute prompt-intent denominators behind the r9/r11 ack-label metrics.

The run logs use `-ack` for turns that sometimes request a full state. This
stdlib-only audit derives true ack-only turns from each runner's checkpoint
schedule, then compares the label-wide and prompt-verified prefix counts.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROUNDS = (
    ("r9", ROOT / "corpus/evidence/round9-replication/results-r9.jsonl", range(101, 109)),
    ("r11", ROOT / "corpus/evidence/round11-power/results-r11.jsonl", range(201, 265)),
)
CELLS = {
    "A-CKPT4710": {4, 7, 10},
    "A-CKPT710": {7, 10},
}


def true_ack_turns(checkpoints: set[int], total_turns: int = 10) -> tuple[int, ...]:
    return tuple(
        turn for turn in range(2, total_turns + 1)
        if turn not in checkpoints and turn - 1 not in checkpoints
    )


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{line_no}: expected JSON object")
        rows.append(row)
    return rows


def audit(round_name: str, path: Path, pids: range) -> list[tuple]:
    data = path.read_bytes()
    rows = load_jsonl(path)
    metas = [row for row in rows if row.get("cell") == "meta"]
    meta = {row.get("pid"): row for row in metas}
    if len(metas) != len(pids) or set(meta) != set(pids):
        raise ValueError(f"{round_name}: meta pid census does not match {pids.start}..{pids.stop - 1}")
    for pid, row in meta.items():
        if len(row.get("ops", [])) != 10 or len(row.get("truth", [])) != 10:
            raise ValueError(f"{round_name} pid {pid}: expected 10 ops and 10 truth states")

    output = []
    for cell, checkpoints in CELLS.items():
        name = cell + "-ack"
        ack_rows = [row for row in rows if row.get("cell") == name]
        true_turns = true_ack_turns(checkpoints)
        logged_turns = tuple(turn for turn in range(1, 11) if turn not in checkpoints)
        controls = tuple(turn for turn in logged_turns if turn not in true_turns)
        expected_keys = {(pid, turn) for pid in pids for turn in logged_turns}
        observed = {}
        for row in ack_rows:
            key = (row.get("pid"), row.get("turn"))
            raw = row.get("raw")
            if key not in expected_keys or key in observed:
                raise ValueError(f"{round_name} {name}: unexpected or duplicate key {key}")
            if not isinstance(raw, str) or len(raw) > 80:
                raise ValueError(f"{round_name} {name} {key}: raw must be at most 80 characters")
            observed[key] = raw
        if set(observed) != expected_keys:
            raise ValueError(
                f"{round_name} {name}: missing={len(expected_keys - set(observed))}, "
                f"extra={len(set(observed) - expected_keys)}"
            )

        prompt_rows = [observed[(pid, turn)] for pid in pids for turn in true_turns]
        prefix_count = sum(raw.strip().lower().startswith("ok") for raw in prompt_rows)
        bare_count = sum(raw.strip().lower() == "ok" for raw in prompt_rows)
        label_prefix_count = sum(raw.strip().lower().startswith("ok") for raw in observed.values())
        nonbare_pids = Counter(
            pid for pid in pids
            if any(observed[(pid, turn)].strip().lower() != "ok" for turn in true_turns)
        )
        output.append((
            round_name,
            name,
            len(ack_rows),
            len(prompt_rows),
            ",".join(map(str, true_turns)),
            ",".join(map(str, controls)),
            prefix_count,
            bare_count,
            label_prefix_count,
            len(nonbare_pids),
            hashlib.sha256(data).hexdigest(),
        ))
    return output


def selftest() -> int:
    checks = (
        true_ack_turns({7, 10}) == (2, 3, 4, 5, 6, 9),
        tuple(turn for turn in range(1, 11) if turn not in {7, 10} and turn not in true_ack_turns({7, 10})) == (1, 8),
        true_ack_turns({4, 7, 10}) == (2, 3, 6, 9),
        tuple(turn for turn in range(1, 11) if turn not in {4, 7, 10} and turn not in true_ack_turns({4, 7, 10})) == (1, 5, 8),
    )
    assert all(checks), checks
    print(f"SELFTEST: {len(checks)}/{len(checks)} PASS")
    return 0


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()

    result_rows = [row for round_name, path, pids in ROUNDS for row in audit(round_name, path, pids)]
    print("| Round | Logged cell | Label rows | True ack rows | True ack turns | Full-state controls | Prefix `ok` / true ack | Bare `ok` / true ack | Prefix `ok` / label rows | Pids with non-bare reply | Input SHA-256 |")
    print("|---|---|---:|---:|---|---|---:|---:|---:|---:|---|")
    for (round_name, cell, label_n, ack_n, ack_turns, control_turns, prefix_n, bare_n,
         label_prefix_n, nonbare_pids, digest) in result_rows:
        print(
            f"| {round_name} | `{cell}` | {label_n} | {ack_n} | {ack_turns} | {control_turns} | "
            f"{prefix_n}/{ack_n} ({100 * prefix_n / ack_n:.1f}%) | "
            f"{bare_n}/{ack_n} ({100 * bare_n / ack_n:.1f}%) | "
            f"{label_prefix_n}/{label_n} ({100 * label_prefix_n / label_n:.1f}%) | "
            f"{nonbare_pids}/{len(ROUNDS[0][2]) if round_name == 'r9' else len(ROUNDS[1][2])} | `{digest}` |"
        )
    print("\nPrompt schedule: `run_r9.py:16,26-28`; `run_r11.py:61,76-80`. `-ack` is a storage label, not prompt intent.")
    print("`Prefix ok` reproduces the historical proxy. `Bare ok` requires the entire stripped raw to equal `ok`; prefix-only rows with extra content are not silently counted as bare acknowledgements.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
