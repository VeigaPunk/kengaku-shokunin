#!/usr/bin/env python3
"""Independent extraction-policy counts over the frozen round-26 responses."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

EXPECTED_POPULATION = 1964
FILES = {
    "corpus/evidence/round8-horizon/results.jsonl": "bd986e5e8c9b415aa2b0073fa8fed784282c9dbeb19055d34475e662792e2204",
    "corpus/evidence/round9-replication/results-r9.jsonl": "c20158bdef148b322501341e539b2383d84de4179618fd46b801379c11affbcb",
    "corpus/evidence/round11-power/results-r11.jsonl": "918bf7aa3030baa954c16a20830f078738147ce7cc002768e5ab922ad38f51ad",
    "corpus/evidence/round12-ladder/results-r12.jsonl": "ad9c88e79068fa2833c90f071ec6da4035ff37371ff95d84f581dd4e8db842f1",
}
FENCE = re.compile(r"```(?:json)?\s*\n(.*?)```", re.S)
ANY_LABEL_FENCE = re.compile(r"```[A-Za-z0-9_+-]*[ \t]*\r?\n(.*?)```", re.S)
BARE_RE = re.compile(
    r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}|\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]",
    re.S,
)
DECODER = json.JSONDecoder()


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_policy_value(candidate):
    try:
        return True, json.loads(candidate)
    except (json.JSONDecodeError, TypeError):
        return False, None


def bare_candidates(raw):
    return BARE_RE.findall(raw)


def first_or_last_bare(raw, first):
    matches = bare_candidates(raw)
    order = matches if first else reversed(matches)
    for candidate in order:
        parsed, value = load_policy_value(candidate)
        if parsed:
            return True, value
    return False, None


def fenced_policy(raw, fence_re, first, fallback):
    blocks = fence_re.findall(raw)
    if blocks:
        parsed, value = load_policy_value(blocks[0] if first else blocks[-1])
        if parsed:
            return True, value
    if fallback:
        return first_or_last_bare(raw, False)
    return False, None


def strict_whole(raw):
    return load_policy_value(raw.strip())


def decode_scan(raw, first):
    values = []
    i = 0
    while i < len(raw):
        if raw[i] not in "[{":
            i += 1
            continue
        try:
            value, end = DECODER.raw_decode(raw, i)
        except json.JSONDecodeError:
            i += 1
            continue
        values.append(value)
        if first:
            return True, value
        # A successful top-level decode owns its interior; don't reconsider
        # opening brackets inside this span as independent candidates.
        i = end
    return (True, values[-1]) if values else (False, None)


def extract(policy_id, raw):
    if policy_id == "E0":
        return fenced_policy(raw, FENCE, first=False, fallback=True)[1]
    if policy_id == "E1":
        return fenced_policy(raw, FENCE, first=True, fallback=True)[1]
    if policy_id == "E2":
        return first_or_last_bare(raw, first=False)[1]
    if policy_id == "E3":
        return first_or_last_bare(raw, first=True)[1]
    if policy_id == "E4":
        return strict_whole(raw)[1]
    if policy_id == "E5":
        return fenced_policy(raw, FENCE, first=False, fallback=False)[1]
    if policy_id == "E6":
        return fenced_policy(raw, ANY_LABEL_FENCE, first=False, fallback=True)[1]
    if policy_id == "E7":
        return decode_scan(raw, first=True)[1]
    if policy_id == "E8":
        return decode_scan(raw, first=False)[1]
    raise ValueError("unknown extraction policy: " + policy_id)


def valid_latin(square):
    symbols = {"A", "B", "C", "D"}
    if not isinstance(square, list) or len(square) != 4:
        return False
    if not all(isinstance(row, list) and len(row) == 4 and set(row) == symbols
               for row in square):
        return False
    return all(len({square[row][column] for row in range(4)}) == 4
               for column in range(4))


def regrade(record, got):
    if got is None:
        return False
    cell = record.get("cell", "")
    if cell == "C-MONO":
        return valid_latin(got)
    if isinstance(cell, str) and cell.startswith("C-"):
        # The pinned C records contain one root answer object. Its committed
        # C-specific truth includes the prior square, which is not repeated in
        # each response row; for that exact parsed answer the recorded C verdict
        # is the frozen truth. Non-root candidates are not valid C answer objects.
        return got == record.get("got") and record["ok"] is True
    want = record.get("want")
    if isinstance(want, (dict, list)):
        return got == want
    return False


def read_population(root):
    records = []
    for relative, expected_hash in FILES.items():
        path = root / relative
        if not path.is_file():
            raise ValueError("missing pinned response file: " + relative)
        actual_hash = digest(path)
        if actual_hash != expected_hash:
            raise ValueError("SHA-256 mismatch for " + relative)
        with path.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                record = json.loads(line)
                if "raw" not in record or "ok" not in record:
                    continue
                if not isinstance(record["raw"], str) or type(record["ok"]) is not bool:
                    raise ValueError(f"invalid raw/ok at {relative}:{line_number}")
                records.append(record)
    if len(records) != EXPECTED_POPULATION:
        raise ValueError(f"population={len(records)} expected={EXPECTED_POPULATION}")
    return records


def count_policy(records, policy_id):
    counts = {"agree": 0, "flip_pf": 0, "flip_fp": 0, "none": 0}
    for record in records:
        value = extract(policy_id, record["raw"])
        if value is None:
            counts["none"] += 1
        verdict = regrade(record, value)
        stored = record["ok"]
        if verdict == stored:
            counts["agree"] += 1
        elif stored:
            counts["flip_pf"] += 1
        else:
            counts["flip_fp"] += 1
    return counts


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args(argv)
    try:
        records = read_population(args.root.resolve())
        results = [(f"E{i}", count_policy(records, f"E{i}")) for i in range(9)]
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"policy_oracle: {exc}", file=sys.stderr)
        return 1
    if results[0][1]["agree"] != EXPECTED_POPULATION:
        print("policy_oracle: E0 does not reproduce all stored verdicts", file=sys.stderr)
        return 1
    for policy_id, counts in results:
        print("POLICY " + policy_id + " " + " ".join(
            f"{key}={counts[key]}" for key in ("agree", "flip_pf", "flip_fp", "none")
        ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
