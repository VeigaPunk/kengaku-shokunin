#!/usr/bin/env python3
"""Round-27 preservation check for two plans/state_check.py builds (P2/P3 records).

Runs `state_check.py --json --root ROOT` for --old and for --new (each child with
PYTHONDONTWRITEBYTECODE=1 and cwd=ROOT), keeps every assertion whose id starts with P2 or
P3, and compares each record in full (id, source_line, check, observed, verdict, as canonical
JSON with sorted keys). Records are keyed by id; a repeated id is matched by occurrence. The
order of the P2/P3 subsequence is compared too, so a reorder is a difference. Ids with any
other prefix (P4a..P4e in v4) are outside this comparison by design.

Exit map:
  0  identical: same ids, every field equal, same P2/P3 order
  1  different: DIFF / ADDED / REMOVED / COUNT / ORDER lines printed
  2  not comparable: usage error, child exit other than 0 or 1, no JSON, timeout, or zero
     P2/P3 records on either side (never a vacuous PASS)

state_check exits 1 on mismatches but still prints its full JSON, so child exits 0 and 1 are
both comparable. Both runs take the same --root; records may embed absolute paths under it.

Reuse with v4 (round 27):
  python3 plans/fixtures/r27/p23_preservation.py --old OLD_STATE_CHECK.py --new NEW_STATE_CHECK.py --root BASE_TREE
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

COMPARED_PREFIXES = ("P2", "P3")
CHILD_TIMEOUT_SECONDS = 900
EXIT_IDENTICAL = 0
EXIT_DIFFERENT = 1
EXIT_NOT_COMPARABLE = 2


class NotComparable(Exception):
    """A child run or input that leaves no comparable P2/P3 population."""


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_state_check(script: Path, root: Path) -> tuple[int, dict[str, Any], list[dict[str, Any]]]:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    try:
        proc = subprocess.run(
            [sys.executable, str(script), "--json", "--root", str(root)],
            cwd=root, env=env, capture_output=True, timeout=CHILD_TIMEOUT_SECONDS, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise NotComparable(f"{script} timed out after {CHILD_TIMEOUT_SECONDS}s") from exc
    except OSError as exc:
        raise NotComparable(f"{script} could not start: {exc}") from exc
    if proc.returncode not in (0, 1):
        stderr = proc.stderr.decode("utf-8", "replace").strip()
        raise NotComparable(f"{script} exited {proc.returncode}: {stderr}")
    try:
        data = json.loads(proc.stdout.decode("utf-8"))
        summary, assertions = data["summary"], data["assertions"]
    except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise NotComparable(
            f"{script} printed no --json document ({type(exc).__name__}: {exc})") from exc
    if not isinstance(assertions, list) or not all(
            isinstance(item, dict) and "id" in item for item in assertions):
        raise NotComparable(f"{script} --json assertions are not keyed records")
    records = [item for item in assertions if str(item["id"]).startswith(COMPARED_PREFIXES)]
    return proc.returncode, summary, records


def canonical(record: dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2)


def grouped(records: list[dict[str, Any]]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for record in records:
        groups.setdefault(str(record["id"]), []).append(canonical(record))
    return groups


def compare(old: list[dict[str, Any]], new: list[dict[str, Any]], report: list[str]) -> tuple[int, int]:
    """Append diff lines to report; return (record pairs compared, differences)."""
    old_groups, new_groups = grouped(old), grouped(new)
    pairs = differences = 0
    for key in sorted(set(old_groups) | set(new_groups)):
        before_all = old_groups.get(key, [])
        after_all = new_groups.get(key, [])
        if not before_all:
            report.append(f"ADDED    {key}: {len(after_all)} record(s) present only in new")
            differences += len(after_all)
            continue
        if not after_all:
            report.append(f"REMOVED  {key}: {len(before_all)} record(s) present only in old")
            differences += len(before_all)
            continue
        if len(before_all) != len(after_all):
            report.append(f"COUNT    {key}: old={len(before_all)} new={len(after_all)}")
            differences += abs(len(before_all) - len(after_all))
        for occurrence, (before, after) in enumerate(zip(before_all, after_all), 1):
            pairs += 1
            if before == after:
                continue
            differences += 1
            label = f"{key}#{occurrence}" if len(before_all) > 1 else key
            report.append(f"DIFF     {label}")
            report.extend(difflib.unified_diff(
                before.splitlines(), after.splitlines(),
                fromfile=f"old {label}", tofile=f"new {label}", lineterm=""))
    old_order = [str(item["id"]) for item in old]
    new_order = [str(item["id"]) for item in new]
    if old_order != new_order:
        diverge = next((index for index, (a, b) in enumerate(zip(old_order, new_order)) if a != b),
                       min(len(old_order), len(new_order)))
        before_id = old_order[diverge] if diverge < len(old_order) else "<end>"
        after_id = new_order[diverge] if diverge < len(new_order) else "<end>"
        report.append(f"ORDER    P2/P3 sequence differs; first at position {diverge + 1}: "
                      f"old={before_id} new={after_id}")
        differences += 1
    return pairs, differences


def population(records: list[dict[str, Any]]) -> str:
    return " ".join(
        f"{prefix}={sum(1 for item in records if str(item['id']).startswith(prefix))}"
        for prefix in COMPARED_PREFIXES)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--old", type=Path, required=True, help="reference state_check.py, e.g. v3")
    parser.add_argument("--new", type=Path, required=True, help="candidate state_check.py, e.g. v4")
    parser.add_argument("--root", type=Path, required=True,
                        help="tree both runs inspect; the same tree is used for both")
    args = parser.parse_args(argv)
    try:
        root = args.root.expanduser().resolve(strict=True)
        if not root.is_dir():
            raise NotComparable(f"--root is not a directory: {root}")
        scripts: dict[str, Path] = {}
        for label, value in (("old", args.old), ("new", args.new)):
            script = value.expanduser().resolve(strict=True)
            if not script.is_file():
                raise NotComparable(f"--{label} is not a file: {script}")
            scripts[label] = script
        old_code, old_summary, old_records = run_state_check(scripts["old"], root)
        new_code, new_summary, new_records = run_state_check(scripts["new"], root)
    except OSError as exc:
        print(f"p23_preservation: USAGE: {exc}", file=sys.stderr)
        return EXIT_NOT_COMPARABLE
    except NotComparable as exc:
        print(f"p23_preservation: NOT COMPARABLE: {exc}", file=sys.stderr)
        return EXIT_NOT_COMPARABLE
    if not old_records or not new_records:
        print(f"p23_preservation: NOT COMPARABLE: zero P2/P3 records (old={len(old_records)} "
              f"new={len(new_records)}); refusing a vacuous PASS", file=sys.stderr)
        return EXIT_NOT_COMPARABLE
    report = [
        f"root: {root}",
        f"old: {scripts['old']} sha256={sha256_of(scripts['old'])} exit={old_code} "
        f"P2/P3 {population(old_records)} summary={json.dumps(old_summary, sort_keys=True)}",
        f"new: {scripts['new']} sha256={sha256_of(scripts['new'])} exit={new_code} "
        f"P2/P3 {population(new_records)} summary={json.dumps(new_summary, sort_keys=True)}",
    ]
    pairs, differences = compare(old_records, new_records, report)
    ids = {str(item["id"]) for item in old_records} | {str(item["id"]) for item in new_records}
    order_same = [item["id"] for item in old_records] == [item["id"] for item in new_records]
    report.append(f"compared: ids={len(ids)} record_pairs={pairs} differences={differences} "
                  f"order={'same' if order_same else 'differs'}")
    if differences:
        report.append(f"VERDICT: DIFFERENT - {differences} difference(s) in P2/P3 records; "
                      "see lines above")
    else:
        report.append(f"VERDICT: IDENTICAL - {len(old_records)} old and {len(new_records)} new "
                      "P2/P3 records match on every field, in the same order")
    print("\n".join(report))
    return EXIT_DIFFERENT if differences else EXIT_IDENTICAL


if __name__ == "__main__":
    sys.exit(main())
