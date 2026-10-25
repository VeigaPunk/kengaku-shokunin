#!/usr/bin/env python3
"""Re-probe the two live public model catalogs and check the catalog entry's freshness.

Round 32 (2026-10-25), claim C3. `corpus/knowledge/open-model-catalogs.md` was
probed on 2026-09-28; this tool probes Hugging Face `api/models` and OpenRouter
`api/v1/models` on the access date, records the per-source schema delta (only
fields the 09-28 description names and that are absent from the sampled
response), and exits 0 only when both probes succeed AND the entry carries the
dated `verified-at:` line, the two row citations S101/S102, and a receipt
pointer. The receipt line is the claim's counter line.

Frozen schema expectations (open-model-catalogs.md, probed 2026-09-28):
  HF        id, author, sha, lastModified, downloads, likes, trendingScore,
            pipeline_tag, library_name, tags, gated
  OpenRouter id, canonical_slug, context_length, knowledge_cutoff, created,
            pricing, architecture, supported_parameters, top_provider,
            per_request_limits, hugging_face_id, reasoning
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
import urllib.request
from pathlib import Path

ACCESS_DATE = "2026-10-25"
HF_URL = "https://huggingface.co/api/models?limit=50"
OR_URL = "https://openrouter.ai/api/v1/models"
ENTRY = "corpus/knowledge/open-model-catalogs.md"
RECEIPTS = "corpus/evidence/round32/catalogs/"

HF_FIELDS = (
    "id", "author", "sha", "lastModified", "downloads", "likes",
    "trendingScore", "pipeline_tag", "library_name", "tags", "gated",
)
OR_FIELDS = (
    "id", "canonical_slug", "context_length", "knowledge_cutoff", "created",
    "pricing", "architecture", "supported_parameters", "top_provider",
    "per_request_limits", "hugging_face_id", "reasoning",
)


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "kengaku-catalog-probe/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_hf(text: str) -> tuple[int, list[str]]:
    data = json.loads(text)
    if not isinstance(data, list) or not data:
        raise ValueError("HF api/models did not return a nonempty list")
    first = data[0]
    if not isinstance(first, dict):
        raise ValueError("HF model entry is not a JSON object")
    return len(data), [field for field in HF_FIELDS if field not in first]


def parse_openrouter(text: str) -> tuple[int, list[str]]:
    data = json.loads(text)
    if not isinstance(data, dict) or "data" not in data or not isinstance(data["data"], list):
        raise ValueError("OpenRouter api/v1/models did not return a data list")
    models = data["data"]
    if not models:
        raise ValueError("OpenRouter model list is empty")
    first = models[0]
    if not isinstance(first, dict):
        raise ValueError("OpenRouter model entry is not a JSON object")
    return len(models), [field for field in OR_FIELDS if field not in first]


def probe() -> tuple[str, int, int, list[str], list[str]]:
    hf_text = fetch(HF_URL)
    or_text = fetch(OR_URL)
    hf_n, hf_missing = parse_hf(hf_text)
    or_n, or_missing = parse_openrouter(or_text)
    return "ok", hf_n, or_n, hf_missing, or_missing


def entry_ok(lane: Path) -> str:
    path = lane / ENTRY
    if not path.is_file():
        return "missing"
    text = path.read_text(encoding="utf-8", errors="replace")
    if not __import__("re").search(
        r"^verified-at: 2026-10-25\b", text, __import__("re").MULTILINE
    ):
        return "stale"
    if "S101" not in text or "S102" not in text or RECEIPTS not in text:
        return "stale"
    # The claim requires an actual receipt, not an unvalidated directory substring.
    if not (lane / RECEIPTS / "after.txt").is_file():
        return "missing-receipt"
    receipt = (lane / RECEIPTS / "after.txt").read_text(
        encoding="utf-8", errors="replace"
    )
    required = ("hf_schema_delta=", "or_schema_delta=", "HF missing fields:")
    if any(token not in receipt for token in required):
        return "invalid-receipt"
    return "ok"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lane", type=Path, default=Path("."))
    parser.add_argument("--diff", action="store_true", help="accepted for the claim's counting command")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    try:
        status, hf_n, or_n, hf_missing, or_missing = probe()
    except Exception as error:
        status = f"fail:{type(error).__name__}"
        hf_n = or_n = 0
        hf_missing = or_missing = []
    entry = entry_ok(args.lane.resolve())
    print(
        f"probed={ACCESS_DATE} hf={status if status == 'ok' else 'fail'}"
        f" openrouter={status if status == 'ok' else 'fail'}"
        f" hf_models={hf_n} or_models={or_n}"
        f" hf_schema_delta={len(hf_missing)} or_schema_delta={len(or_missing)}"
        f" entry={entry}"
    )
    if hf_missing:
        print("HF missing fields: " + ", ".join(hf_missing))
    if or_missing:
        print("OpenRouter missing fields: " + ", ".join(or_missing))
    # Probe reachability and receipt validity define the outcome; nonempty
    # schema deltas are recorded findings rather than failures.
    return 0 if status == "ok" and entry == "ok" else 1


def selftest() -> int:
    cases: list[tuple[str, bool]] = []
    hf_ok = json.dumps([{"id": "a", "author": "x", "sha": "s", "lastModified": "d",
                          "downloads": 1, "likes": 2, "trendingScore": 3,
                          "pipeline_tag": "t", "library_name": "l", "tags": [],
                          "gated": False}])
    hf_missing = json.dumps([{"id": "a"}])
    or_ok = json.dumps({"data": [{"id": "m", "canonical_slug": "s", "context_length": 10,
                                   "knowledge_cutoff": "c", "created": 1, "pricing": {},
                                   "architecture": {}, "supported_parameters": [],
                                   "top_provider": {"context_length": 10},
                                   "per_request_limits": {}, "hugging_face_id": "h",
                                   "reasoning": {"effort": None}}]})
    or_missing = json.dumps({"data": [{"id": "m"}]})

    n, missing = parse_hf(hf_ok)
    cases.append(("hf-parses", n == 1 and missing == []))
    n, missing = parse_hf(hf_missing)
    cases.append(("hf-missing-detected", n == 1 and len(missing) > 0))
    n, missing = parse_openrouter(or_ok)
    cases.append(("or-parses", n == 1 and missing == []))
    n, missing = parse_openrouter(or_missing)
    cases.append(("or-missing-detected", n == 1 and len(missing) > 0))
    try:
        parse_hf("[]")
        cases.append(("hf-empty-list-guard", False))
    except ValueError:
        cases.append(("hf-empty-list-guard", True))
    try:
        parse_openrouter('{"data": []}')
        cases.append(("or-empty-data-guard", False))
    except ValueError:
        cases.append(("or-empty-data-guard", True))
    with tempfile.TemporaryDirectory() as tmp:
        lane = Path(tmp)
        cases.append(("entry-missing-red", entry_ok(lane) != "ok"))
        (lane / "corpus" / "knowledge").mkdir(parents=True, exist_ok=True)
        (lane / "corpus" / "evidence" / "round32" / "catalogs").mkdir(parents=True, exist_ok=True)
        entry = lane / ENTRY
        entry.write_text(
            "source: S101 — https://huggingface.co/api/models\n"
            "source: S102 — https://openrouter.ai/api/v1/models\n"
            "verified-at: 2026-10-25\n"
            f"receipts: {RECEIPTS}\n",
            encoding="utf-8",
        )
        cases.append(("entry-receipt-missing-red", entry_ok(lane) == "missing-receipt"))
        receipt = lane / RECEIPTS / "after.txt"
        receipt.write_text(
            "probed=2026-10-25 hf=ok openrouter=ok hf_models=50 or_models=467 "
            "hf_schema_delta=4 or_schema_delta=0 entry=ok\n"
            "HF missing fields: author, sha, lastModified, gated\n",
            encoding="utf-8",
        )
        cases.append(("entry-current-with-receipt-green", entry_ok(lane) == "ok"))
    failed = [name for name, passed in cases if not passed]
    for name, passed in cases:
        print(f"CASE {name} {'PASS' if passed else 'FAIL'}")
    print(f"SELFTEST checks={len(cases)} failed={len(failed)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
