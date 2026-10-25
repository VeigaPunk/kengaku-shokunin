# R33 Falsify — quote-gate source provenance (S103/S104)

**Verdict: UNCAUGHT as a provenance/pin/location gate; correctly limited in the implementation's own documentation.** The observed gate proves short quoted strings occur in a supplied UTF-8 artifact and that a caller-declared URL for at least one containing artifact normalizes to any URL in the row's source cell. It does not prove how the artifact was fetched, which revision/version it represents, or that a quote occurs at the row's stated line. No lane source was changed; adversarial fixtures were under `/tmp/r33fsourcesauth-mutants-20261025`.

## Observed facts

- `append-rows.md` has S103 and S104. `quotes.json` records five S103 and three S104 spans, with claimed line numbers, and lists SHA-256/byte counts for the captures. The gate receipt reports `rows=2 spans=8 located=8 found=8 overlong=0 absent=0 ... cap=25`, then `EXIT=0`.
- The exact gate command, run read-only, was:
  ```
  python3 plans/sources_adopt.py --quote-file .ufo/waves/round-33/assimilation/append-rows.md --artifact .ufo/waves/round-33/assimilation/captures --url-map .ufo/waves/round-33/assimilation/url-map.json
  ```
  It returned exit 0 and eight `ok` lines. The receipt bound the S103 artifact to the pinned GitHub **blob URL** string and S104 HTML capture to `https://arxiv.org/abs/2412.05579`.
- Capture probes confirmed S103 quote text at lines 58, 218, 234, 279, and 280; each tested quoted span occurs once in that capture. S104 capture has the title span at line 41, arXiv version marker `arXiv:2412.05579v2` at line 109, abstract span at line 124, and comments span at line 131. The title string occurs 11 times and the abstract string 3 times in the HTML. Thus these local line claims are consistent with the current capture, but their locations are not established by the gate.
- Independently fetched the pinned S103 raw URL (read-only):
  ```
  curl -fsS 'https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py' -o /tmp/r33fsourcesauth-provenance-20261025/main.py
  sha256sum /tmp/r33fsourcesauth-provenance-20261025/main.py .ufo/waves/round-33/assimilation/captures/toolathlon-ab-testing-evaluation-main.py
  cmp -s /tmp/r33fsourcesauth-provenance-20261025/main.py .ufo/waves/round-33/assimilation/captures/toolathlon-ab-testing-evaluation-main.py && echo 'BYTE_IDENTICAL=yes'
  ```
  Observed: both SHA-256 values were `3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad`; `BYTE_IDENTICAL=yes`. A separate read-only curl reported HTTP 200 and 14,138 bytes for that raw URL. This independently supports the S103 capture's identity at the pinned raw URL during this probe; it is not a validation performed by the quote gate or a historical fetch receipt.
- `curl` of the unversioned S104 abs URL returned HTTP 200, 43,647 bytes; the committed local capture is 43,661 bytes. No byte-identity comparison was performed. The local capture itself identifies as v2 at line 109, but the mapped/cited URL has no version suffix.

## Falsification / what the gate does not prove

1. **Fetch provenance — uncaught.** `sources_adopt.py` lines 340–347 describe `--url-map` as caller-authored and explicitly say it is a citation-membership check, not provenance proof; the gate cannot verify a fetch. `load_artifact` reads files and `locating_artifacts` checks substring presence. The map does not contain a fetch receipt or derive its URL from the bytes. S103's captured Python source is independently shown to match the raw URL, but the gate's receipt maps it to a GitHub `/blob/` URL, not that raw URL.
2. **Pin/version identity — uncaught.** In a fresh `/tmp` fixture, generated text artifacts containing only the eight quoted spans, changed every stated quote line to `:99999`, changed the S103 commit in both row and URL map to forty zeroes, and supplied no S104 version marker. Ran:
   ```
   python3 plans/sources_adopt.py --quote-file /tmp/r33fsourcesauth-mutants-20261025/rows.md --artifact /tmp/r33fsourcesauth-mutants-20261025/artifacts --url-map /tmp/r33fsourcesauth-mutants-20261025/url-map.json
   ```
   Observed `rows=2 spans=8 located=8 found=8 ... mismatch=0 unmapped=0` and `EXIT=0`; the S103 `bound=` lines named the all-zero commit URL. Repointing the fake S103 artifact's map to the row's unpinned repository-root URL also returned `EXIT=0` (`bound=fake-S103.txt->https://github.com/hkust-nlp/Toolathlon`). This demonstrates the gate accepts arbitrary capture bytes and a fabricated commit identity when the caller makes the citation/map strings agree. S104's unversioned abs URL likewise cannot distinguish v2 from another version; the fabricated S104 artifact had no version marker and passed.
3. **Exact quote location — uncaught.** `locating_artifacts` uses `needle in text` over the entire normalized artifact; it does not parse the `:line` annotations. The same `/tmp` attack changed all quote line references to `:99999` and still passed. Actual current line locations above are capture facts, not a location check performed by the gate.
4. **Digest manifest — not gate-enforced.** `SHA256SUMS.txt` is present in the artifact directory and appears in the gate's artifact listing, but `sources_adopt.py` does not hash artifacts or compare this manifest. Its quote test only loads text and searches for substrings. The local digest entries are useful recorded evidence, but the gate receipt does not validate them.

The decisive gate logic is `words()` (`split()` count), `load_artifact()` (UTF-8 read/newline normalization), `locating_artifacts()` (substring search), and `bind_failure()` (normalized URL-string membership against URLs extracted from the source cell). S103's source cell includes both repository root and pinned blob URLs; the binding rule accepts **any** cited URL, so the pin is not a required binding target.

## Calibration and impact

The gate correctly catches overlong/missing quotes and wrong/unmapped declared URLs within its documented scope. It does **not** catch false provenance, false pin identity, or false line anchors. Therefore `found=8` / `EXIT=0` must not be represented as proof of fetched-at-pin sources or exact quote locations. The build's `quotes.json` fetch-check statements are records/assertions; the S103 raw fetch was independently reproducible in this probe, while S104's version identity is only self-asserted by the capture contents and is not bound by the gate. The general provenance claim is unsupported by the receipt, not disproved for the real S103 capture.

**Severity:** low-to-medium evidence-integrity/calibration defect (not a defect against the gate's explicitly stated limited contract). A fabricated or stale artifact could satisfy the receipt and be mistaken downstream for pin-verified evidence.

**Smallest remediation:** describe the receipt narrowly as “quote present in caller-supplied artifact; caller-declared URL matches a cited URL.” Treat fetch, pin/version, digest, and line-location assertions as separately supported only where independent evidence exists. If those guarantees are required, validate a fetched-artifact digest against an immutable/versioned source URL and parse/check the stated line anchors; do not infer them from this gate's current exit 0.
