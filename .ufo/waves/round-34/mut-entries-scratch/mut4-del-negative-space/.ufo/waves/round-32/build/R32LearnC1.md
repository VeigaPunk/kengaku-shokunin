# R32LearnC1 — C1 byte-exact source captures (S094, S097)

Date: 2026-10-25. Seat: leaf executor R32LearnC1. Scope: assemble byte-exact captures for C1's two new rows and record digests + manifest. No tools installed (curl only; no channel change to record).

## Captures

| File (scratch /tmp/r32-R32LearnC1/) | Source URL | Pin | HTTP | Bytes |
|---|---|---|---|---|
| S094-toolathlon-ab-testing-evaluation-main.py | https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py | commit 9be8d8fe07a497b18ee61e3f2ae694e9797f39eb | 200 | 14138 |
| S097-arxiv-2412.05579v2-abs.html | https://arxiv.org/abs/2412.05579 | arXiv 2412.05579v2 | 200 | 43647 |

Effective URLs (curl `%{url_effective}`): S094 — same raw.githubusercontent URL; S097 — `https://arxiv.org/abs/2412.05579` (serves the current version, v2; canonical/og:url point at `/abs/2412.05579v2`).

## Content verification (pinned quotes found at the pinned revision)

- S094, line 58 of the capture: `def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1) -> None:` — matches the S094 row's located quote.
- S097: `<title>[2412.05579] LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods</title>`; dateline `[Submitted on 7 Dec 2024 (v1), last revised 10 Dec 2024 (this version, v2)]`; submission history shows `[v1] Sat, 7 Dec 2024 08:07:24 UTC` and `[v2] Tue, 10 Dec 2024 05:49:12 UTC` — matches the S097 row's pin (arXiv 2412.05579v2) and abstract quote.

## Digests

- sha256(S094-toolathlon-ab-testing-evaluation-main.py) = `3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad`, 14138 bytes
- sha256(S097-arxiv-2412.05579v2-abs.html) = `851b03db6bf5ae74ac7abe0512a0d12be97c8d7b6f99916e7e09356ae67b043d`, 43647 bytes

## Material (SHA256SUMS.txt, written at /tmp/r32-R32LearnC1/SHA256SUMS.txt)

```
3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad  S094-toolathlon-ab-testing-evaluation-main.py  https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py  commit 9be8d8fe07a497b18ee61e3f2ae694e9797f39eb
851b03db6bf5ae74ac7abe0512a0d12be97c8d7b6f99916e7e09356ae67b043d  S097-arxiv-2412.05579v2-abs.html  https://arxiv.org/abs/2412.05579  arXiv 2412.05579v2
```

## Risks / notes

- Scratch holds ~58 KB total (well under 60 MB); captures remain at /tmp/r32-R32LearnC1/ for the round; they are not committed (leaf bounds).
- No source opened other than the two captures; no reads from the lane repo beyond the frozen-claims and staged-SOURCESES reads needed to resolve the pins.
- S097 capture is the v2 abs page (the current version served at /abs/2412.05579); the S097 row's pin and quote both resolve.

VERDICT: captures-ready
