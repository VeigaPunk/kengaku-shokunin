# Python stdlib docs: C1 source opening

- Scope: Python `json`/`re` runtime semantics in the current extractor; this is not a general literature or tooling-registry search.
- Fetch: `curl -sS -L`; both requested URLs returned HTTP 200 on 2026-10-21 UTC. Hashes below are SHA-256 of fetched response-body bytes.
- JSON source: https://docs.python.org/3/library/json.html — Python 3.15.0 documentation; last updated Oct 21, 2026 (06:42 UTC); accessed 2026-10-21 06:51:32 UTC; HTTP 200; SHA-256 `54f7fa6bd094e5cc09b9e41f50d0dc44baa17d83c7d7146369dfe6e8ed641144`.
  - Exact location: §Basic Usage, `json.loads` (`#json.loads`); §Encoders and Decoders, `json.JSONDecoder` strict parameter (`#json.JSONDecoder`, rendered extract lines 403–405). `loads` is documented as identical to `load`; `load` defaults to `JSONDecoder`, whose `strict=True` is the default.
  - Verbatim excerpt (16 words): “If strict is false (True is the default), then control characters will be allowed inside strings.”
  - Relevance: F3 re-serializes the same JSON object with compact/indented formatting; the API docs describe `loads` deserialization and `dump`/`dumps` indentation controls. The strictness note is specifically about control characters inside strings, not CR before a line-feed outside a string.
- Regex source: https://docs.python.org/3/library/re.html — Python 3.15.0 documentation; last updated Oct 21, 2026 (06:42 UTC); accessed 2026-10-21 06:51:34 UTC; HTTP 200; SHA-256 `59d4a9c0e254047735e4756fe684dafa323c4d9b24ab055b4d1997534be268a0`.
  - Exact location: §Regular expression syntax, special sequence `\s` (rendered extract lines 528–530).
  - Verbatim excerpt (3 words): “This includes `[ \t\n\r\f\v]`”. The preceding sentence says Unicode `\s` matches whitespace as defined by `str.isspace()`.
  - Relevance: in `grader.py:121-128`, the fence regex has `\s*\n`; `\s` includes CR, so it can consume the CR in a CRLF fence line. F7's named operation is at `plans/round-26-claims.md:64`.
- Combined quotation: 19 words (under the 25-word limit). Both source pages are version 3.15.0; their footer reports the update date above.
- Recommended SOURCES tier: **A (primary)** for Python standard-library behavior only; these language docs are not prior-art evidence for an evaluation method.
- Teaches: Python's default JSON decoder strictness concerns control characters inside strings, while Unicode regex `\s` includes CR.
- C1 prior-art verdict: **No**—these docs document library behavior, not published verdict-invariance testing of an answer grader/extractor under response-format perturbation (method or tooling). This is a verdict about the two requested sources only, not a claim that no such prior art exists elsewhere.
- Installs: none.
- VERDICT: Official Python docs clarify the F3/F7 implementation semantics but do not themselves constitute C1 methodological/tooling prior art.
