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
OR_URL = "https://openrouter.ai/api/v1/models?limit=10"
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

# Round 33 (2026-10-25), claim C3: raw-byte retention. The round-32 closure routed
# "raw API payloads are not retained; preserve bounded response bytes plus digests
# next probe". `--capture` fetches live and writes the bounded bytes; `--verify`
# re-derives every recorded number offline from the committed bytes (no network).
CAP_DIR = "corpus/evidence/round33/catalogs/"
RAW_HF = "hf.raw.json"
RAW_OR = "or.raw.json"
DIGESTS = "SHA256SUMS"
AFTER = "after.txt"
RAW_CAP = 64 * 1024
REPROBE_HEADING = "## Re-probe 2026-10-25 (round 33)"


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "kengaku-catalog-probe/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read()


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
    total = data.get("total_count", len(models))
    if not isinstance(total, int) or total < len(models):
        raise ValueError("OpenRouter total_count is missing or inconsistent with returned page")
    return total, [field for field in OR_FIELDS if field not in first]


def capture(lane: Path) -> int:
    """Fetch both catalogs live and write bounded raw bytes + digests + receipt."""
    out = lane / CAP_DIR
    out.mkdir(parents=True, exist_ok=True)
    hf_raw = fetch(HF_URL)
    or_raw = fetch(OR_URL)
    hf_n, hf_missing = parse_hf(hf_raw.decode("utf-8"))
    or_n, or_missing = parse_openrouter(or_raw.decode("utf-8"))
    if len(hf_raw) > RAW_CAP or len(or_raw) > RAW_CAP:
        print(f"capture=oversize hf={len(hf_raw)} openrouter={len(or_raw)} cap={RAW_CAP}")
        return 1
    (out / RAW_HF).write_bytes(hf_raw)
    (out / RAW_OR).write_bytes(or_raw)
    import hashlib

    hf_sha = hashlib.sha256(hf_raw).hexdigest()
    or_sha = hashlib.sha256(or_raw).hexdigest()
    (out / DIGESTS).write_text(
        f"{hf_sha}  {RAW_HF}\n{or_sha}  {RAW_OR}\n", encoding="utf-8"
    )
    summary = (
        f"probed={ACCESS_DATE} hf=ok openrouter=ok hf_models={hf_n} or_models={or_n}"
        f" hf_schema_delta={len(hf_missing)} or_schema_delta={len(or_missing)} entry=pending\n"
        f"raw_sha256 hf={hf_sha} or={or_sha} cap={RAW_CAP}\n"
    )
    if hf_missing:
        summary += "HF missing fields: " + ", ".join(hf_missing) + "\n"
    if or_missing:
        summary += "OpenRouter missing fields: " + ", ".join(or_missing) + "\n"
    (out / AFTER).write_text(summary, encoding="utf-8")
    print(summary, end="")
    return 0


def _load_raw(lane: Path) -> tuple[str, str] | None:
    out = lane / CAP_DIR
    digest_path = out / DIGESTS
    hf_path = out / RAW_HF
    or_path = out / RAW_OR
    if not (digest_path.is_file() and hf_path.is_file() and or_path.is_file()):
        return None
    import hashlib

    for line in digest_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        sha, name = line.split(None, 1)
        name = name.strip()
        data = (out / name).read_bytes() if (out / name).is_file() else b""
        if hashlib.sha256(data).hexdigest() != sha:
            raise ValueError(f"digest mismatch for {name}: the capture was altered or fabricated")
    hf_raw = hf_path.read_bytes()
    or_raw = or_path.read_bytes()
    if len(hf_raw) > RAW_CAP or len(or_raw) > RAW_CAP:
        raise ValueError(f"a raw file exceeds the {RAW_CAP}-byte bound")
    return hf_raw.decode("utf-8", errors="replace"), or_raw.decode("utf-8", errors="replace")


def verify(lane: Path) -> int:
    """Re-derive every recorded number from the committed raw bytes (no network)."""
    try:
        raw = _load_raw(lane)
    except ValueError as error:
        print(f"raw=invalid {error}")
        return 1
    if raw is None:
        print("raw=absent")
        return 1
    hf_text, or_text = raw
    try:
        hf_n, hf_missing = parse_hf(hf_text)
        or_n, or_missing = parse_openrouter(or_text)
    except ValueError as error:
        print(f"raw=unparsable {error}")
        return 1
    receipt_path = lane / CAP_DIR / AFTER
    if not receipt_path.is_file():
        print("raw=ok receipt=absent")
        return 1
    receipt = receipt_path.read_text(encoding="utf-8", errors="replace")
    expected = (
        f"hf_models={hf_n}",
        f"or_models={or_n}",
        f"hf_schema_delta={len(hf_missing)}",
        f"or_schema_delta={len(or_missing)}",
    )
    for token in expected:
        if token not in receipt:
            print(f"raw=ok receipt-mismatch missing:{token}")
            return 1
    if hf_missing and "HF missing fields:" not in receipt:
        print("raw=ok receipt-mismatch missing:HF-missing-fields-line")
        return 1
    entry = (lane / ENTRY).read_text(encoding="utf-8", errors="replace")
    if REPROBE_HEADING not in entry:
        print(f"raw=ok entry-mismatch missing:{REPROBE_HEADING}")
        return 1
    block = entry.split(REPROBE_HEADING, 1)[1]
    block = block.split("\n## ", 1)[0]
    if CAP_DIR not in block:
        print(f"raw=ok entry-mismatch missing:{CAP_DIR}")
        return 1
    for token in expected:
        if token not in block:
            print(f"raw=ok entry-mismatch missing:{token}")
            return 1
    print(
        f"raw=ok hf_models={hf_n} or_models={or_n}"
        f" hf_schema_delta={len(hf_missing)} or_schema_delta={len(or_missing)} verify=ok"
    )
    if hf_missing:
        print("HF missing fields: " + ", ".join(hf_missing))
    if or_missing:
        print("OpenRouter missing fields: " + ", ".join(or_missing))
    return 0


def probe() -> tuple[str, int, int, list[str], list[str]]:
    hf_raw = fetch(HF_URL)
    or_raw = fetch(OR_URL)
    hf_n, hf_missing = parse_hf(hf_raw.decode("utf-8"))
    or_n, or_missing = parse_openrouter(or_raw.decode("utf-8"))
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
    parser.add_argument("--capture", action="store_true", help="round 33: fetch live and write bounded raw bytes")
    parser.add_argument("--verify", action="store_true", help="round 33: re-derive recorded numbers from committed bytes")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    lane = args.lane.resolve()
    if args.capture:
        try:
            return capture(lane)
        except Exception as error:
            print(f"probed={ACCESS_DATE} hf=fail openrouter=fail capture-error={type(error).__name__}: {error}")
            return 1
    if args.verify:
        return verify(lane)
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
                                   "reasoning": {"effort": None}}], "total_count": 467})
    or_missing = json.dumps({"data": [{"id": "m"}]})

    n, missing = parse_hf(hf_ok)
    cases.append(("hf-parses", n == 1 and missing == []))
    n, missing = parse_hf(hf_missing)
    cases.append(("hf-missing-detected", n == 1 and len(missing) > 0))
    n, missing = parse_openrouter(or_ok)
    cases.append(("or-total-count-rederived", n == 467 and missing == []))
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

        # Round 33 --verify: absent raw is red; a fixture capture verifies green;
        # a tampered digest and a missing entry block are red again.
        import hashlib

        lane33 = Path(tmp) / "lane33"
        cap = lane33 / CAP_DIR
        cap.mkdir(parents=True, exist_ok=True)
        cases.append(("verify-absent-red", verify(lane33) == 1))
        hf_raw = hf_ok.encode("utf-8")
        or_raw = or_ok.encode("utf-8")
        (cap / RAW_HF).write_bytes(hf_raw)
        (cap / RAW_OR).write_bytes(or_raw)
        (cap / DIGESTS).write_text(
            f"{hashlib.sha256(hf_raw).hexdigest()}  {RAW_HF}\n"
            f"{hashlib.sha256(or_raw).hexdigest()}  {RAW_OR}\n",
            encoding="utf-8",
        )
        (cap / AFTER).write_text(
            f"probed={ACCESS_DATE} hf=ok openrouter=ok hf_models=1 or_models=467"
            f" hf_schema_delta=0 or_schema_delta=0 entry=pending\n",
            encoding="utf-8",
        )
        (lane33 / "corpus/knowledge").mkdir(parents=True, exist_ok=True)
        (lane33 / ENTRY).write_text(
            f"{REPROBE_HEADING}\n\nverified-at: {ACCESS_DATE}\nreceipts: {CAP_DIR}\n"
            "hf_models=1 or_models=467 hf_schema_delta=0 or_schema_delta=0\n",
            encoding="utf-8",
        )
        cases.append(("verify-fixture-green", verify(lane33) == 0))
        (cap / RAW_HF).write_bytes(hf_missing.encode("utf-8"))
        cases.append(("verify-digest-tamper-red", verify(lane33) == 1))
        (cap / RAW_HF).write_bytes(hf_raw)
        text = (lane33 / ENTRY).read_text(encoding="utf-8").replace(REPROBE_HEADING, "## Something else")
        (lane33 / ENTRY).write_text(text, encoding="utf-8")
        cases.append(("verify-entry-block-red", verify(lane33) == 1))
    failed = [name for name, passed in cases if not passed]
    for name, passed in cases:
        print(f"CASE {name} {'PASS' if passed else 'FAIL'}")
    print(f"SELFTEST checks={len(cases)} failed={len(failed)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
