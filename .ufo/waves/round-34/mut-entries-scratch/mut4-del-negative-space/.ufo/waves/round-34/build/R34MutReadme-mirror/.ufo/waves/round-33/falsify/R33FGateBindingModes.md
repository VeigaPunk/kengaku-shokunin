# R33FGateBindingModes — no-map versus URL-map binding

**Verdict: limitation (no-map is byte-presence only; map mode checks caller-declared URL membership, not capture provenance).** All probes ran on a fresh `/tmp/r33f-binding-modes/` copy of the gate and captures; no lane files were changed by the probes. Gate copy SHA-256 was `38492bf175e0c619596c69911954e3b3c247166bdc240f8c1d44a02b7f4103e0`, identical to `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/sources_adopt.py`.

## Exact S103 URL and captured bytes

The S103 source cell in both `.ufo/waves/round-33/assimilation/append-rows.md` and `corpus/SOURCES.md:118` cites the repository root **and** this blob URL:

`https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py`

The committed `.ufo/waves/round-33/assimilation/url-map.json` maps `toolathlon-ab-testing-evaluation-main.py` to that same pinned commit and exact task-file path. Local capture evidence: `wc -lc` reported `297 14138`; its SHA-256 is `3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad`, matching the entry in `captures/SHA256SUMS.txt` and the digest recorded in `assimilation/quotes.json`. The five S103 spans appear in the local capture, including the quoted lines recorded at 58, 218, 234, 279 and 280. This establishes that the committed map *labels* the capture with the exact pinned blob URL and that the local capture matches the recorded digest; this probe did not independently fetch the remote URL.

## Reproduction and modes

The one-row fixture was extracted unchanged from `append-rows.md` (1 line, 1852 bytes). On the copied gate:

```sh
python3 /tmp/r33f-binding-modes/sources_adopt.py \
  --quote-file /tmp/r33f-binding-modes/rows-s103.md \
  --artifact /tmp/r33f-binding-modes/captures
```

Observed: exit 0, `QUOTE rows=1 spans=5 located=5 found=5 overlong=0 absent=0 malformed=0 cap=25 ...`; each `ok S103` says only `at toolathlon-ab-testing-evaluation-main.py`, with no `bound=` field. With the committed map:

```sh
python3 /tmp/r33f-binding-modes/sources_adopt.py \
  --quote-file /tmp/r33f-binding-modes/rows-s103.md \
  --artifact /tmp/r33f-binding-modes/captures \
  --url-map /tmp/r33f-binding-modes/maps/committed.json
```

Observed: exit 0, `mismatch=0 unmapped=0`, and each S103 `ok` line reports `bound=toolathlon-ab-testing-evaluation-main.py->https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py`.

No-map omits citation checks: a fixture with the S103 source URL removed also exited 0 (5/5 located); the same fixture with the committed map exited 8, five `cites-no-url` refusals. No-map also omits artifact identity/binding: a synthetic unrelated file containing the five quoted strings exited 0 (`artifacts=forged-toolathlon.py`, all five `ok`). The map is not provenance proof either: mapping that synthetic file's name to the exact pinned blob URL also exited 0, with all five `bound=...-><pinned blob>` lines. A copied `retry.py` with the S103 strings appended likewise exited 0 without a map; using its real committed retry-URL mapping exited 8 (`mismatch=5`), but falsely declaring that file to be the pinned task URL exited 0. Thus map mode detects an inconsistent declaration, not a false declaration or forged capture.

## What URL matching enforces—and does not

`bind_failure` in the cited source extracts all source-cell URLs and accepts when **any** mapped quote-containing artifact URL equals **any** cited URL after narrow normalization. The S103 cell includes the coarse repository root as well as the pinned blob, so a map of the actual task capture to `https://github.com/hkust-nlp/Toolathlon` also exited 0 and printed that root as `bound=`. Therefore the exact pin is present in the committed map, but exact-task-file pinning is **not required by the gate** while the root URL remains cited. As observed in the probe, mappings to a different SHA, a different file path, the raw fetch URL, branch `main`, or `http` exited 8; a trailing slash on the exact blob URL still exited 0. A wrong artifact-map key (`captures/toolathlon-ab-testing-evaluation-main.py` rather than the loaded basename) exited 9, `unmapped=5`.

The gate also does not validate anchor line numbers: changing the anchor's `main.py:58` to `main.py:9999` (and `:218` to `:1`) still exited 0, both with and without a map. It validates quote length and literal normalized-text occurrence; the map adds only citation-membership checking. These behaviors are explicit in `quote_check`'s docstring and `bind_failure` in the current absolute source file `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/sources_adopt.py` (notably `load_url_map`, `bind_failure`, and the no-map branch in `quote_check`).

## Conflicting build finding

`build/R33GateMutants.md` reports exit 8 with the committed map because its S103 row supposedly cites only the root. Current observed bytes contradict that premise: the staged row and `corpus/SOURCES.md:118` both contain the root URL **and** the exact pinned blob URL; running that same row with the copied committed map exited 0. This report records the tested current bytes and command, not the earlier report's premise. The existing committed `gate-receipts.txt` also records a green result, with S103 bound to the pinned blob URL.

**Risk / limitation:** neither a green no-map run nor a green URL-map run authenticates that a capture was fetched from the URL it claims. No-map additionally accepts URL-less rows and any artifact containing the quote; map mode can accept root-level declarations or arbitrary bytes when the map is caller-authored. No tools were installed; no blocker.