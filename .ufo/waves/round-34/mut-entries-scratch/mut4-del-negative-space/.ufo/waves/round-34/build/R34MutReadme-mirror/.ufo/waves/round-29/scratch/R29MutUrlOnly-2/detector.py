"""Bounded own-work fixture detector; not production verification or an oracle."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
ORDER = ("GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP")


def string_leaves(value, path="$"):
    if isinstance(value, str):
        return {path: value}
    leaves = {}
    if isinstance(value, dict):
        for key, item in value.items():
            leaves.update(string_leaves(item, path + "." + key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            leaves.update(string_leaves(item, f"{path}[{index}]"))
    return leaves


def main():
    fixture_bytes = (ROOT / "fixture.json").read_bytes()
    expected_bytes = (ROOT / "expected.json").read_bytes()
    candidate_bytes = (ROOT / "candidate.py").read_bytes()
    fixture = json.loads(fixture_bytes)
    expected = json.loads(expected_bytes)
    raw = fixture["raw_text"]
    original = json.loads(raw)
    # This is authored local scratch code, not the pinned upstream generator.
    namespace = {"__name__": "r29_url_only_own_scratch"}
    exec(compile(candidate_bytes, str(ROOT / "candidate.py"), "exec"), namespace)
    actual = namespace["project"](raw, fixture["values"])
    before_leaves = string_leaves(original)
    after_leaves = string_leaves(actual)
    expected_leaves = string_leaves(expected["projection"])
    changed_paths = sorted(path for path in before_leaves if after_leaves.get(path) != before_leaves[path])
    mismatch_paths = sorted(path for path in set(after_leaves) | set(expected_leaves) if after_leaves.get(path) != expected_leaves.get(path))
    raw_counts = {"__" + name + "__": raw.count("__" + name + "__") for name in ORDER}
    remaining = sum(text.count("__" + name + "__") for text in after_leaves.values() for name in ORDER)
    checks = {
        "input_task_count": len(original) == expected["input_task_count"],
        "profile_count": expected["profile_count"] == 1,
        "task_profile_projection_count": len(actual) == expected["task_profile_projection_count"],
        "raw_occurrence_units": raw_counts == expected["raw_replacement_occurrences_by_token"],
        "whole_projected_object": actual == expected["projection"],
        "changed_leaf_paths": changed_paths == expected["changed_string_leaf_paths"],
        "changed_task_count": sum(a != b for a, b in zip(original, actual)) == expected["changed_task_count"],
        "no_known_environment_tokens": remaining == expected["remaining_known_environment_token_occurrences"],
        "url_control": actual[0]["start_url"] == expected["projection"][0]["start_url"],
        "non_url_intent": actual[0]["intent"] == expected["projection"][0]["intent"],
        "unread_annotation": actual[0]["eval"]["reference_answer_raw_annotation"] == expected["projection"][0]["eval"]["reference_answer_raw_annotation"],
        "published_references_unchanged": actual[0]["eval"]["reference_answers"] == original[0]["eval"]["reference_answers"],
        "runtime_markers_preserved": actual[0]["fixture_markers"] == "__last_url__ __page__",
    }
    output = {
        "scope": "own-work hand-case discrimination only; production mutation untested",
        "case_id": fixture["case_id"],
        "candidate_sha256": hashlib.sha256(candidate_bytes).hexdigest(),
        "fixture_sha256": hashlib.sha256(fixture_bytes).hexdigest(),
        "expected_sha256": hashlib.sha256(expected_bytes).hexdigest(),
        "input_tasks": len(original),
        "profiles": 1,
        "task_profile_projections": len(actual),
        "raw_replacement_occurrences_by_token": raw_counts,
        "actual_changed_string_leaf_paths": changed_paths,
        "actual_changed_string_leaf_count": len(changed_paths),
        "remaining_known_environment_token_occurrences": remaining,
        "mismatch_paths": mismatch_paths,
        "checks": checks,
        "result": "PASS" if all(checks.values()) else "FAIL",
    }
    print(json.dumps(output, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
