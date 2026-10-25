# RevF10 — W3ReviewKengaku F10 re-check (round-25, read-only seat)

Axis: calibration. Subject: kaika-w3 F10 (dynamic-page receipt caveat) at lane tip `3f371d2` (base read: `plans/round-25-claims.md` — frozen P1/P2, CP rule, n=17 power ask, P1–P5).

## Verdict: OPEN — the caveat was never written
1. F10 (`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w3/kengaku-review.md:141`): "Add an access-time capture caveat to `corpus/evidence/round24-sources/gate.md`" — S005 `0568df0b…`≠`8bd40cbc…`, S006 `e3052697…`≠`fba4c005…`, S023 `bf62b2cd…`≠`ee510e84…`.
2. `git -C <lane> log -S 'dynamic' -- corpus/evidence/round24-sources/gate.md` → empty (also `-S 'caveat'`, `-S 'Access-time'` → empty). `gate.md` has exactly two commits: `94da19e` (created) and `e21f9ea` (+1 line = S026 receipt row, now `gate.md:34` — a superseding receipt, not the caveat).
3. Tip sweep `grep -in 'dynamic|caveat|access-time|byte-repro'` over `LOG.md SHONEN.md SCORECARD.md PROVINCE.md corpus/lessons corpus/README.md plans` → no receipt rule; the only "dynamic" note is `corpus/lessons/round-24-verifier-spotcheck.md:12` ("S005/S006/S023 dynamic") — it states the fact and adds no rule for re-verification.
4. `e21f9ea` fixed F1–F5 (Q9/Q10 in `corpus/QUALITY.md:69-81`, S026 supersedes S023 `corpus/SOURCES.md:48`, 21 recheck cells, §Corrections blocks); F10 was not among the fixes.

## Evidence the gap is real (re-fetched 2026-10-20 via curl, read-only)
- S005 `https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/` → 9,843 bytes (byte count = receipt) but sha `e6f58c18…` and `1da6fa12…` across two fetches 2 s apart; receipt `8bd40cbc…` not reproduced; the diff is a Cloudflare challenge block (`cH:`/`cRay:`/`cITimeS:` tokens differ per fetch).
- S006 `https://openai.com/index/separating-signal-from-noise-coding-evaluations/` → 9,852 bytes (= receipt), sha `faec654e…` ≠ receipt `fba4c005…`.
- S023/S026 `https://scale.com/blog/swe-bench-pro` → 128,773 bytes (= receipt), sha `c7e50638…` ≠ `ee510e84…` (S023) and ≠ `171087c5…` (S026's own receipt, `gate.md:34`).
- Pattern: byte count stable, bytes not. The recorded shas are access-time captures; nothing in-repo says so, so every future re-verifier re-derives the false mismatch (or wrongly fails these rows).

## Partial-fix credit
- Operational substance is partly covered: S026 supersedes S023 and admission rests on quote+location (Q10), not on sha; round-25 C1 rule 1 ("No receipt byte is edited") protects forward receipts from this class.
- The documentation gap remains: no receipt states that dynamic-page shas are non-reproducible and no rule tells a re-verifier what to do.

## Smallest append-only fix (writer: lane L1; this seat is read-only)
Append to `corpus/evidence/round24-sources/gate.md` after line 105 (EOF), dated section, no registry change (receipt file is outside the rule-2 old→new registry paths):

```
## Access-time capture caveat (added 2026-10-20, W3ReviewKengaku F10 re-check)
The sha256 receipts above are access-time captures, not byte-reproducible contracts, for
challenge-served pages: S005, S006, S023, S026 (OpenAI/Scale). Same-day re-fetches hash
differently at identical byte counts (S005 e6f58c18…, S006 faec654e…, S026 c7e50638…) while
quotes and locations verify in rendered text. For these rows re-verification is
quote-and-location based; the recorded sha binds the capture, not the page. From round 25, a
receipt row for such a page carries the note "dynamic page: sha is an access-time capture";
superseding a capture is a new row (SOURCES contract rule 2).
```

Optionally the same commit may add one QUALITY line making it enforceable for future rounds; the caveat alone closes F10 as filed (the review's requested fix, verbatim).

## Residual risk / verification gaps
- Quotes re-verified by hash/size only this round; rendered-quote verification is the 2026-10-19 review §4 result (17/20 hash-exact + quote checks).
- `grep -c 'gate.md'` in `.ufo/waves/round-25/build/{build-spec.json,swarm-registry.json}` → 0: no sibling seat owns `gate.md`; no sibling build report touches F10 (`grep -l 'F10\|dynamic'` → none).
- Installs: none. Writes: this report only.
