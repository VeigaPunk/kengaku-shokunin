#!/usr/bin/env python3
"""Score state snapshots on true acknowledgement-only r11 turns.

The r11 `A-CKPT710-ack` cell is a storage label, not a prompt-intent label:
turns 1 and 8 request a full state, while turns 2-6 and 9 request only `ok`.
Raw ack captures are clipped to 80 characters, so ambiguous capped records are
reported unresolved rather than treated as model errors.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = ROOT / "corpus/evidence/round11-power/results-r11.jsonl"
EXPECTED_SHA256 = "918bf7aa3030baa954c16a20830f078738147ce7cc002768e5ab922ad38f51ad"
ACK_CELL = "A-CKPT710-ack"
PIDS = range(201, 265)
ACK_ONLY_TURNS = (2, 3, 4, 5, 6, 9)
LOGGED_ACK_TURNS = (1, 2, 3, 4, 5, 6, 8, 9)
CATEGORIES = (
    "exact-state",
    "nonexact-state",
    "ok/no-state",
    "unresolved-80-char-cap",
    "unresolved-other-raw",
)


def extract_json_block(text: str):
    """Use the r11 fenced-JSON-then-last-object parser on captured text."""
    blocks = re.findall(r"```(?:json)?\s*\n(.*?)```", text, re.S)
    for candidate in reversed(blocks):
        try:
            return json.loads(candidate)
        except (json.JSONDecodeError, TypeError):
            pass
    spans = re.findall(
        r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}|\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]",
        text,
        re.S,
    )
    for candidate in reversed(spans):
        try:
            return json.loads(candidate)
        except (json.JSONDecodeError, TypeError):
            pass
    return None


def intent_for_turn(turn: int) -> str:
    if turn == 1:
        return "initial-full-state"
    if turn in (7, 10):
        return "checkpoint-full-state"
    if turn - 1 in (7, 10):
        return "post-checkpoint-full-state"
    if turn in ACK_ONLY_TURNS:
        return "ack-only"
    raise ValueError(f"unexpected A-CKPT710 turn: {turn}")


def classify_raw(raw: str, truth: dict) -> str:
    parsed = extract_json_block(raw)
    if isinstance(parsed, dict):
        if parsed == truth:
            return "exact-state"
        if len(raw) >= 80:
            return "unresolved-80-char-cap"
        return "nonexact-state"
    if len(raw) >= 80:
        return "unresolved-80-char-cap"
    if raw.strip().lower() == "ok":
        return "ok/no-state"
    return "unresolved-other-raw"


def load_records(data: bytes) -> list[dict]:
    records = []
    for line_no, line in enumerate(data.splitlines(), 1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL at line {line_no}: {exc}") from exc
        if not isinstance(record, dict):
            raise ValueError(f"non-object JSONL record at line {line_no}")
        records.append(record)
    return records


def analyze(data: bytes) -> str:
    records = load_records(data)
    meta_rows = [record for record in records if record.get("cell") == "meta"]
    meta = {record.get("pid"): record for record in meta_rows}
    if len(meta_rows) != 64 or set(meta) != set(PIDS):
        raise ValueError("expected exactly one r11 meta row for each pid 201-264")
    for pid, record in meta.items():
        if len(record.get("ops", [])) != 10 or len(record.get("truth", [])) != 10:
            raise ValueError(f"pid {pid}: expected ten ops and ten truth states")

    rows = [record for record in records if record.get("cell") == ACK_CELL]
    if len(rows) != 512:
        raise ValueError(f"expected 512 {ACK_CELL} rows, found {len(rows)}")
    seen = set()
    by_pid_turn = {}
    for record in rows:
        pid, turn = record.get("pid"), record.get("turn")
        key = (pid, turn)
        if pid not in meta or key in seen:
            raise ValueError(f"invalid or duplicate acknowledgement key: {key}")
        if turn not in LOGGED_ACK_TURNS:
            raise ValueError(f"unexpected acknowledgement cell turn: {key}")
        raw = record.get("raw")
        if not isinstance(raw, str) or len(raw) > 80:
            raise ValueError(f"pid {pid} turn {turn}: raw must be a string of at most 80 chars")
        seen.add(key)
        by_pid_turn[key] = record
    expected = {(pid, turn) for pid in PIDS for turn in LOGGED_ACK_TURNS}
    if seen != expected:
        raise ValueError(f"acknowledgement key-set mismatch: missing={len(expected-seen)} extra={len(seen-expected)}")

    counts = Counter()
    by_turn = Counter()
    pid_exact_counts = Counter()
    pid_brace_counts = Counter()
    ack_prefix = Counter()
    for pid, turn in sorted(seen):
        record = by_pid_turn[(pid, turn)]
        raw = record["raw"]
        category = classify_raw(raw, meta[pid]["truth"][turn - 1])
        intent = intent_for_turn(turn)
        counts[(intent, category)] += 1
        by_turn[(turn, category)] += 1
        if intent == "ack-only" and category == "exact-state":
            pid_exact_counts[pid] += 1
        if intent == "ack-only" and "{" in raw:
            pid_brace_counts[pid] += 1
        if raw.strip().lower().startswith("ok"):
            ack_prefix[intent] += 1

    ack_total = sum(counts[("ack-only", category)] for category in CATEGORIES)

    lines = [
        "# Round-13 acknowledgement-state audit",
        "",
        "Input: `corpus/evidence/round11-power/results-r11.jsonl`",
        f"Input SHA-256: `{hashlib.sha256(data).hexdigest()}`",
        "Prompt-intent source: `corpus/evidence/round11-power/run_r11.py:76-80`; raw is clipped to 80 characters at `run_r11.py:74`.",
        "Scope: one served Qwen3-Coder-30B-A3B-Instruct UD-IQ2_XXS run; repeated turns are clustered within 64 pids.",
        "",
        f"Census: {len(meta_rows)} meta; {len(rows)} rows logged as `{ACK_CELL}`; {len(ACK_ONLY_TURNS)} true ack-only turns × 64 pids = {ack_total}.",
        "True ack-only turns: 2-6, 9. Turns 1 (initial state) and 8 (post-checkpoint full state) are full-state asks logged under the `-ack` label; they are controls, not ack-only observations.",
        "",
        "| Prompt intent | Turn | Exact state | Nonexact state | Bare `ok` / no state | Unresolved at 80-char cap | Unresolved uncapped raw |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for intent, turns in (
        ("ack-only", ACK_ONLY_TURNS),
        ("initial-full-state", (1,)),
        ("post-checkpoint-full-state", (8,)),
    ):
        for turn in turns:
            vals = [by_turn[(turn, category)] for category in CATEGORIES]
            lines.append(f"| {intent} | {turn} | " + " | ".join(str(value) for value in vals) + " |")
    for intent in ("ack-only", "initial-full-state", "post-checkpoint-full-state"):
        totals = [sum(counts[(intent, category)] for category in CATEGORIES)]
        if intent == "ack-only" and totals[0] != 384:
            raise ValueError(f"ack-only denominator mismatch: {totals[0]}")

    ack_n = 384
    exact = counts[("ack-only", "exact-state")]
    unresolved = counts[("ack-only", "unresolved-80-char-cap")]
    nonexact = counts[("ack-only", "nonexact-state")]
    ok_count = counts[("ack-only", "ok/no-state")]
    unresolved_other = counts[("ack-only", "unresolved-other-raw")]
    state_openers = sum(pid_brace_counts.values())
    state_pids = [pid for pid in PIDS if pid_brace_counts[pid] > 0]
    all_six_state_pids = sum(pid_brace_counts[pid] == len(ACK_ONLY_TURNS) for pid in PIDS)
    if not state_openers:
        raise ValueError("no state-shaped ack-only responses to bound")
    state_lower = exact / state_openers
    state_upper = (exact + unresolved) / state_openers
    incidence_lower = exact / ack_n
    incidence_upper = (exact + unresolved) / ack_n
    lines.extend([
        "",
        "## Reading the result",
        "",
        f"Among true ack-only turns, {ack_prefix['ack-only']}/384 raw replies start with `ok`; {ok_count}/384 are exactly bare `ok`; {exact}/384 contain a parseable state equal to that turn's simulator truth.",
        f"Stored ack-only raws containing `{{`: {state_openers}/384 across {len(state_pids)}/64 pids; {all_six_state_pids} pids have a brace on all six turns.",
        f"Of {exact + nonexact} parseable state objects, {exact} are exact. Among all {state_openers} brace-bearing raws, the exact-state share is bounded by [{state_lower:.3f}, {state_upper:.3f}] because {unresolved} hit the 80-char cap.",
        f"Verified exact-state emissions per ack-only prompt are bounded by [{incidence_lower:.3f}, {incidence_upper:.3f}] across all 384 prompts; {unresolved_other} uncapped non-bare raw replies have no parseable state and remain unresolved output-contract cases.",
        f"Pids with ≥1 exact ack-only state snapshot: {sum(1 for pid in PIDS if pid_exact_counts[pid] > 0)}/64.",
        f"Across all 512 `-ack`-labelled rows, `startswith('ok')` = {sum(1 for record in rows if record['raw'].strip().lower().startswith('ok'))}/512; this reproduces the old denominator, which mixes true ack-only and full-state-ask turns.",
        "",
        "An exact state on an ack-only turn is state-faithful but does not satisfy the literal `Reply 'ok'` response contract. A capped/unparseable response is unresolved, not a model failure. Counts are descriptive; no causal, cross-model, or population claim follows.",
    ])
    return "\n".join(lines) + "\n"


def selftest() -> int:
    truth = {"nails": 6, "bolts": 2}
    cases = (
        ("ok\n", "ok/no-state"),
        ("```json\n{\"nails\": 6, \"bolts\": 2}\n```", "exact-state"),
        ("{\"nails\": 6}", "nonexact-state"),
        ("I have updated the state.", "unresolved-other-raw"),
        ("ok\\n```", "unresolved-other-raw"),
    )
    checks = 0
    for raw, expected in cases:
        actual = classify_raw(raw, truth)
        assert actual == expected, (raw, expected, actual)
        checks += 1
    capped = "{" + "x" * 79
    assert len(capped) == 80 and classify_raw(capped, truth) == "unresolved-80-char-cap"
    checks += 1
    assert intent_for_turn(2) == "ack-only"
    assert intent_for_turn(8) == "post-checkpoint-full-state"
    checks += 1
    assert intent_for_turn(1) == "initial-full-state"
    checks += 1
    print(f"SELFTEST: {checks}/{checks} PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    data = args.input.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if args.input.resolve() == DEFAULT_INPUT.resolve() and digest != EXPECTED_SHA256:
        raise SystemExit(f"r11 input hash changed: expected {EXPECTED_SHA256}, got {digest}")
    print(analyze(data), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
