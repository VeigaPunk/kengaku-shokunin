# R31 C3 — citation-bound gate falsification

Scope: four counterexamples named in `.ufo/waves/round-31/build/R31GateDesign.md` §5, run against the landed `dbb07364` body copied read-only to `/tmp/r31fx-c3gate/sources_adopt_landed.py`. Fixture row is S092-shaped and the quote sentence is synthetic; all fixture files are in `/tmp/r31fx-c3gate/`. Commands below were run from that scratch directory, so the repository was not edited by these checks.

## Four counterexamples

| Case | Command / fixture | Measured verdict | Design report limit accurate? |
|---|---|---|---|
| Map = raw fetch URL | `python3 sources_adopt_landed.py --quote-file rows.md --artifact capture.txt --url-map map-pin.json` (map value `https://raw.githubusercontent.com/laude-institute/harbor/6099b8cf2bfbbb3e7ff1eb2163bfc4524dbd9ba5/src/harbor/models/task/config.py`) | **Refused**, exit 8, `url-mismatch`; output `found=1`, `located=0`. | **Yes.** This reproduces §5 case 2 and §6 R1/R2: the row cites only repo root, and raw-file URL is rejected despite being the fetch URL. Fixture quote is synthetic, not fetched from Harbor. |
| Map = cited repo root | `python3 sources_adopt_landed.py --quote-file rows.md --artifact capture.txt --url-map map-root.json` | **Accepted**, exit 0, `located=1`, `mismatch=0`. | **Yes.** The root is accepted under exact normalized set-membership; it does not prove the bytes were fetched from Harbor. |
| Map = repo root + different file of same repo | `python3 sources_adopt_landed.py --quote-file rows.md --artifact readme.txt --url-map map-diff-file.json` | **Accepted**, exit 0, `located=1`, `mismatch=0`. `readme.txt` contains the sentence despite the row anchor pointing to `src/harbor/models/task/config.py`. | **Yes.** Reproduces §5 case 3 / §6 R1: URL mapping is at the granularity of the cited root; another same-repo file passes. |
| Map = repo root + whole-repo dump | `python3 sources_adopt_landed.py --quote-file rows.md --artifact repo-dump.txt --url-map map-dump.json` | **Accepted**, exit 0, `located=1`, `mismatch=0`. | **Yes.** Reproduces §5 case 4 / §6 R1: the gate checks byte substring in supplied text and citation membership, not source-file boundaries or actual fetch provenance. |

The fixture contents and JSON maps are `/tmp/r31fx-c3gate/{rows.md,capture.txt,readme.txt,repo-dump.txt,map-pin.json,map-root.json,map-diff-file.json,map-dump.json}`. The pinned raw URL and repo-root citation are fixture values; no assertion is made that these files are actual pinned Harbor captures.

Control: `python3 sources_adopt_landed.py --quote-file rows.md --artifact capture.txt` exits 0 with no `urlmap=` field, as expected for opt-in binding (the receipt is unbound, not evidence of binding).

## Comment/help consistency

On the landed commit, the section comment at `plans/sources_adopt.py:338-342` says `--url-map` names “the document each artifact was fetched from” (provenance); the help text at `:969-972` says the value is a URL the row cites and explicitly “not the raw fetch URL” for a pinned file (citation membership). **They disagree.** This confirms the defect reported in R31GateDesign §1/§9 C1. In the current working tree (which differs from HEAD due to concurrent edits), the comment at `:338-345` has been rewritten to call this citation-membership rather than provenance, and agrees with help; I report this as observed working-tree state, not as content of landed commit `dbb07364`.

## Limits / instrumentation

`python3 sources_adopt_landed.py --selftest` produced `SELFTEST cases=17 failed=0`, exit 0, stderr 0 bytes. That selftest does not contain these repository-root/raw/different-file/dump cases: its binding fixtures are `example.invalid` and exercise normalization, a wrong document, unmapped, and directory existential behavior (`plans/sources_adopt.py:880-963` in the current working tree; landed source copied to scratch). Thus a green tally does not falsify the four residual limits above.

The design report accurately disclosed the four measured limits: case 2 inversion/refusal, cases 3-4 coarse repo-root acceptance, and the fact it is citation membership rather than provenance. The report’s broader R1/R2 descriptions match the measured behavior. It should be read as risk disclosure, not evidence that the instrument binds the pinned file or verifies capture provenance.

**VERDICT: The raw-fetch URL counterexample survives as a refusal (exit 8); the cited-root, different-file, and whole-repo-dump counterexamples survive as false-granularity acceptances (exit 0). The design report disclosed these limits accurately. On landed HEAD the section comment’s provenance wording conflicts with the citation-membership help; current uncommitted comment text fixes that wording.**