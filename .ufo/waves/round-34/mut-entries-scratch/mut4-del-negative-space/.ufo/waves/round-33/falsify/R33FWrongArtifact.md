# R33FWrongArtifact — citation binding to the wrong file within the same repository

Seat: `R33FWrongArtifact` (leaf). Lane: `kengaku-shokunin`, round 33 (hyaku run 7), 2026-10-25.
Target: C1/S103 kill rule — the claim that a row's located quote must be found in the captured bytes
at the pinned revision of the cited source. Attack: bind a quote unique to `retry.py` to an S103
row scoped to `main.py` (same Toolathlon repo) and observe whether the adoption gate accepts it.

## Sandbox (fresh /tmp; no git, no lane mutation except this report)

- `/tmp/r33-R33FWrongArtifact/` rebuilt from scratch: `sources_adopt.py` copied from `plans/`
  (sha256 `38492bf175e0c619596c69911954e3b3c247166bdc240f8c1d44a02b7f4103e0`, identical to the
  lane file), and `captures/` copied verbatim from
  `.ufo/waves/round-33/assimilation/captures/` (main.py, retry.py, arxiv html, swebench sh,
  SHA256SUMS.txt).
- No tool installed/upgraded. `python3` host 3.14.
- All fixtures, maps, runs and mutations lived under `/tmp/r33-R33FWrongArtifact`; no git/jj/index
  operation anywhere, lane files untouched except this report.

## The quote is unique to retry.py

`DEFAULT_MAX_ATTEMPTS = 3` (3 words, ≤ 25-word cap):

```
COUNT SHA256SUMS.txt: 0
COUNT arxiv-2412.05579v2-abs.html: 0
COUNT swebench-pro-tests-test.sh: 0
COUNT toolathlon-ab-testing-evaluation-main.py: 0
COUNT toolathlon-utils-evaluation-retry.py: 1
HOLDERS: ['toolathlon-utils-evaluation-retry.py']
```

It exists only in `toolathlon-utils-evaluation-retry.py` (`:44`), never in the `main.py` capture.

## Grounding in sources_adopt.py

- `locating_artifacts` (`plans/sources_adopt.py:393-402`) returns **every** artifact whose bytes
  contain the quote — global across the whole captures directory; there is no per-file scope filter.
- `locates` (`:404-413`) is the first match thereof.
- `bind_failure` (`:415-440`) accepts when **any containing artifact** is mapped (`--url-map`) to
  **any URL the row's cell 1 cites** (`cited_urls`, `:350-353`; equality via `normalize_url`,
  `:355-369`). The code comment at `:419-425` codifies the rule: "The rule is *any* containing
  artifact against *any* cited URL."
- Consequently the row's named file (`tasks/finalpool/ab-testing/evaluation/main.py`) never
  participates in the binding test except through the URLs its `source` cell happens to carry.

## Runs (all `python3 sources_adopt.py --quote-file <q> --artifact captures --url-map <m>` in the sandbox)

### Variant A — the attack: retry.py mapped to repo root, S103 row scoped to main.py
Row `S103`: `source` cell identical to the staged/landed S103 cell 1
(`Toolathlon task evaluation script (tasks/finalpool/ab-testing/evaluation/main.py) — https://github.com/hkust-nlp/Toolathlon — pinned blob https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py`);
anchor cell carries `"DEFAULT_MAX_ATTEMPTS = 3"`. Map `mapA.json`:
`{"toolathlon-utils-evaluation-retry.py": "https://github.com/hkust-nlp/Toolathlon",
  "toolathlon-ab-testing-evaluation-main.py": "<pinned main.py blob URL>"}`.

```
QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 cap=25 artifacts=SHA256SUMS.txt,arxiv-2412.05579v2-abs.html,swebench-pro-tests-test.sh,toolathlon-ab-testing-evaluation-main.py,toolathlon-utils-evaluation-retry.py mismatch=0 unmapped=0 urlmap=mapA.json entries=2
  ok S103 words=3 at toolathlon-utils-evaluation-retry.py quote="DEFAULT_MAX_ATTEMPTS = 3" bound=toolathlon-utils-evaluation-retry.py->https://github.com/hkust-nlp/Toolathlon
EXIT=0
```

**The wrong-file quote passes.** The kill rule's refusal (`exit 7` absent) never triggers because
containment is satisfied by `retry.py`; the binding is satisfied because the row cites the repo
root and the `retry.py` capture is declared against that root.

### Variant B — tight citation (pinned blob only) refuses
Same row, but the `source` cell cites **only** the pinned `main.py` blob URL (root URL removed);
same map. 

```
  REFUSED S103 url-mismatch words=3 at toolathlon-utils-evaluation-retry.py quote="DEFAULT_MAX_ATTEMPTS = 3"
EXIT=8
```

Shows the pass in A depends on the root-level citation being among the row's cited URLs.

### Variant C — forged map: retry.py capture declared to answer the main.py blob URL
Tight row (blob-only) + `{"toolathlon-utils-evaluation-retry.py": "<pinned main.py blob URL>", ...}`:

```
  ok S103 words=3 at toolathlon-utils-evaluation-retry.py quote="DEFAULT_MAX_ATTEMPTS = 3" bound=toolathlon-utils-evaluation-retry.py->https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py
EXIT=0
```

The map is caller-authored attestation; the gate never verifies the capture's real identity.

### Variant D — control: real S103 row + committed map
The actual `append-rows.md` S103 row (5 genuine `main.py` quotes) with the committed `url-map.json`:

```
QUOTE rows=1 spans=5 located=5 found=5 overlong=0 absent=0 malformed=0 ... mismatch=0 unmapped=0 urlmap=mapD.json entries=2
  ok S103 ... bound=toolathlon-ab-testing-evaluation-main.py->.../main.py   (x5)
EXIT=0
```

Harness is sound; today's committed form passes honestly.

### Variant E — control: absent quote
`"THIS_QUOTE_EXISTS_NOWHERE_0123456789"` → `REFUSED S103 absent ... EXIT=7`. The gate does
enforce byte-presence; it just cannot scope it to the named file.

### Selftest on the identical sandbox copy
`SELFTEST cases=17 failed=0`, exit 0. (The selftest exercises a bound happy-path,
`quote-url-bound-accepted`, and mismatch paths — never a wrong-file-within-repo case.)

## Verdict

**UNCAUGHT** — the kill-rule claim is falsified at file granularity. An S103 row scoped to
`main.py` passes `EXIT=0` when its located quote exists *only* in `retry.py` of the same repository,
because (1) `locating_artifacts` searches every capture in the directory and (2) `bind_failure`
accepts any containing artifact mapped to any cited URL — and the landed/staged S103 row
(`corpus/SOURCES.md:118`, `.ufo/waves/round-33/assimilation/append-rows.md`) still carries the
repo-root URL alongside the blob, so declaring `retry.py`'s capture against that root suffices.

Severity: **high** for the gate mechanism. Note the mitigation already in place: the committed
`url-map.json` maps each capture to its own pinned blob URL, so the retry.py-unique quote plus the
real row is refused (variant B shape) — no current admission is invalidated by this attack. But the
vulnerability is live for any root-citing row or cross-mapped capture, and the landed S103 row's
root citation persists in the registry.

## Residual risk / verification gaps

- No automated check ties a located quote to the artifact named by the row's `source` cell (path
  token vs artifact name). Closing the gap would require file-scoped containment (restrict
  `locating_artifacts` to the capture mapped to the precise file URL, or bind the artifact name to
  the cited path) — not just URL membership.
- The `--url-map` is self-attestation (variant C) and the gate cannot verify capture identity.
- Not run here (parent-gate checks, out of seat scope): `plans/adoption_check.py`,
  `plans/round33_c1_verify.py`. Neither invokes `sources_adopt.py` (see R33C1KillRule), so the
  wrong-file bind would not surface there either.
- Tools installed/upgraded: none.

## L1 integration correction

The final S103 row no longer cites the repository root; it cites only the pinned `main.py` blob, and the final `url-map.json` maps that capture to the same blob. The report's specific root-citation variant is therefore closed for current S103 bytes. The general limitation remains: the caller-authored map can still associate an incorrect artifact with a cited blob, and the gate does not authenticate that mapping's provenance.
