# R33FExtraURL — multiple cited URL binding

**Target:** `plans/sources_adopt.py::bind_failure`  
**Scratch:** `/tmp/r33-R33FExtraURL/`; all fixture and mutant work stayed there.  
**Frozen/build basis:** round-33 frozen claim and `build/R33C1KillRule.md` item 13 (“Extra cited URLs silently widen binding”); source copied from the lane at SHA-256 `38492bf175e0c619596c69911954e3b3c247166bdc240f8c1d44a02b7f4103e0`.

## Source rule observed

`sources_adopt.py:415-443` extracts all URLs from source cell 1, normalizes them into a set, then checks each mapped containing artifact URL for exact membership in that set. The first membership match returns `artifact->URL`; if mapped artifacts exist but none match, it returns `url-mismatch`. The normalizer strips fragments and trailing slashes and lowercases scheme/host; it preserves path case and distinguishes `http` from `https`. `quote_check` passes every containing artifact to `bind_failure` (`:526-529`); mismatch exits 8, unmapped exits 9 (`:559-568`).

## Fixture and exact detector

Created a single UTF-8 capture `captures/main.py` containing the 12-word quote `The scoring gate accepts only exact label matches under the pinned tolerance.` The markdown quote rows have 11 cells, source in cell 1, and that quote in anchor cell 5. `rowA-root-blob.txt` cites both the Toolathlon repository root and the pinned `9be8d8fe…/evaluation/main.py` blob URL. Other rows swap URL order, cite only root, or cite the blob plus `https://example.org/eval-notes/unrelated-doc`.

The detector invocation was the same CLI for each case:

```sh
python3 /tmp/r33-R33FExtraURL/sources_adopt.work.py \
  --quote-file /tmp/r33-R33FExtraURL/rows/<row>.txt \
  --artifact /tmp/r33-R33FExtraURL/captures \
  --url-map /tmp/r33-R33FExtraURL/maps/<map>.json
```

The no-map case omitted the final two arguments. Every output below is the observed CLI summary and row detail; exit is the process exit code.

| Case | Row / map | Exit and observed output |
|---|---|---|
| P1 | root+blob / root | `0`; `mismatch=0 unmapped=0`; `ok S103 … bound=main.py->https://github.com/hkust-nlp/Toolathlon` |
| P2 | root+blob / pinned blob | `0`; `mismatch=0 unmapped=0`; `ok S103 … bound=main.py->https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py` |
| P3 | root+blob / unrelated URL (not cited) | `8`; `mismatch=1 unmapped=0`; `REFUSED S103 url-mismatch …` |
| P4 | root+blob / `http://github.com/hkust-nlp/Toolathlon` | `8`; `mismatch=1`; `REFUSED S103 url-mismatch …` |
| P5 | root+blob / root with trailing `/` | `0`; `mismatch=0`; `ok … bound=main.py->https://github.com/hkust-nlp/Toolathlon/` |
| P6 | root+blob / root with `#readme` | `0`; `mismatch=0`; `ok … bound=main.py->https://github.com/hkust-nlp/Toolathlon#readme` |
| P7 | blob + unrelated URL / map to that unrelated URL | `0`; `mismatch=0`; `ok … bound=main.py->https://example.org/eval-notes/unrelated-doc` |
| P8 | root only / pinned blob map | `8`; `mismatch=1`; `REFUSED S103 url-mismatch …` |
| P9 | root+blob / no URL map | `0`; `QUOTE rows=1 spans=1 located=1 found=1 …`; `ok S103 …` (byte-presence-only mode) |
| P10 | root+blob / map key `other.py` only | `9`; `mismatch=0 unmapped=1`; `REFUSED S103 unmapped …` |

The selftest on the pristine scratch copy exited 0 and printed `SELFTEST cases=17 failed=0` (all 17 cases PASS). Direct `normalize_url` probes observed: trailing slash and fragment normalize to the root; `http://` remains `http://`; uppercase scheme/host normalize lowercase; path case remains unchanged.

## Mutation probe (same CLI detector)

1. **M1, first-citation-only defect:** changed `cited_keys = {normalize_url(url) for url in cited}` to `cited_keys = {normalize_url(cited[0])}` in the scratch working copy. With the swapped-order row (blob first, root second) and root map, the detector exited `8`, printed `mismatch=1` and `REFUSED S103 url-mismatch`. With root first and the same root map, it exited `0` and bound the root. **Killed by this order-swapped case**; it demonstrates why the all-citations existential check differs from first-only behavior.
2. **M2, prefix-match defect:** changed the membership predicate to accept `normalized.startswith(key)` in addition to exact membership. Root-only row + pinned-blob map changed from pristine exit `8` to mutant exit `0`, with `ok … bound=main.py-><pinned blob URL>`. The fixture detects this prefix relaxation. Root+blob row + unrelated uncited map remained exit `8` under M2.

M1 working-copy SHA-256: `5363431d8f4a45cdb1a1c1fa75e9569ad8d94fe0166d0e1382fb01254791815b`. M2 working-copy SHA-256: `704c175f746162f2dfa3552547973611dc8ad9b2f451f86bd8d9f4f219032fe1`.

## Restoration and verdict

After each mutation, the working copy was restored by copying `sources_adopt.pristine.py` bytes back. Final SHA-256: `38492bf175e0c619596c69911954e3b3c247166bdc240f8c1d44a02b7f4103e0`, equal to the pristine copy. Re-running P1 after restoration exited `0` with `mismatch=0 unmapped=0` and `bound=main.py->https://github.com/hkust-nlp/Toolathlon`.

**Verdict: UNCAUGHT coverage finding, reproduced.** Any single exact-normalized matching citation suffices even when the same row also cites a different document. In particular, the row citing the pinned Toolathlon blob plus the unrelated example URL passes when the map binds only the unrelated URL (P7, exit 0). By contrast, a map URL absent from the row's citation set fails (P3, exit 8), and a repository-root citation does not bind a pinned blob URL by prefix (P8, exit 8). This is membership, not proof that the selected citation is the row's intended or authoritative source. The first-only and prefix mutants were both caught by the fixture.
