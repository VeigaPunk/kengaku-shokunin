# R33FQuoteArtifactSet — SHA256SUMS.txt participates in quote search; manifest-only quotes locate

Seat: R33FQuoteArtifactSet (executor, leaf). Date: 2026-10-25.
Lane: `kengaku-shokunin` (quote-gate + round-33 assimilation artifacts, read-only).
Target: `plans/sources_adopt.py` artifact loading (`load_artifact`) and quote search
(`locates`/`locating_artifacts`/`bind_failure`), against the lane's committed captures
(`.ufo/waves/round-33/assimilation/captures/`).

Build-wave report under test: `R33C1KillRule.md` row 11 — "Helper artifact absorbed into
quote search — `load_artifact` treats *every* UTF-8 file under `captures/` as a quote
candidate, including `SHA256SUMS.txt`" (marked UNCAUGHT). Also `R33SourcesAdoptDry.md`
§4 (F3/F4 runs), `R33RowDrafts.md`.

## 1. Code ground truth (read-only; line numbers at HEAD `2b4cef2`)

- `sources_adopt.py:304-335` `load_artifact`: a directory artifact is
  `candidates = sorted(item for item in path.rglob("*") if item.is_file())` — **no name,
  extension, or role filter**. Every file is decoded UTF-8 and appended to the loaded list;
  a file that fails to decode is skipped and named only if *nothing* loads (`:328-333`).
  `rglob("*")` also admits dotfiles (`.hidden-notes` loads — verified).
- `sources_adopt.py:393-412` `locating_artifacts`/`locates`: byte-substring membership over
  **all** loaded texts; `locates` returns the **first containing artifact in sorted order**.
  `SHA256SUMS.txt` sorts before all lowercase-named captures (`S`=0x53 < `a`=0x61), so it
  is the first candidate for any quote it contains; dotfiles sort even earlier (`.`=0x2E).
- `sources_adopt.py:415-441` `bind_failure`: binding is existential — *any* containing
  artifact mapped to *any* cited URL satisfies the row. Nothing distinguishes a checksum
  manifest from a captured document.
- `sources_adopt.py:495-569` `quote_check`: exit 7 is **byte-presence only**; with
  `--url-map` the manifest-only quote is refused only if the map has no `SHA256SUMS.txt`
  key (exit 9 unmapped), never because the manifest is a helper artifact.

## 2. Materialized lane evidence (no edits; lane bytes unchanged)

The lane's own committed receipt `.ufo/waves/round-33/assimilation/gate-receipts.txt`:

```
QUOTE rows=2 spans=8 located=8 found=8 overlong=0 absent=0 malformed=0 cap=25 artifacts=SHA256SUMS.txt,arxiv-2412.05579v2-abs.html,swebench-pro-tests-test.sh,toolathlon-ab-testing-evaluation-main.py,toolathlon-utils-evaluation-retry.py mismatch=0 unmapped=0 urlmap=url-map.json entries=3
```

So the **actual round-33 gate run loaded `SHA256SUMS.txt` as a quote candidate** — the
manifest was part of the quote search corpus. Dir contents: 5 files; `SHA256SUMS.txt`
covers 3 (no row for `swebench-pro-tests-test.sh`).

`plans/sources_adopt.py --selftest` → `SELFTEST cases=17 failed=0`. Case 12
(`quote-absent-refused`) pins that an unrelated helper file is loaded into the search:
`qreport["artifacts"] == ["capture.txt", "notes.md"]` — the selftest itself asserts a
stray `notes.md` is a quote candidate.

## 3. Sandbox reproduction (`/tmp/r33f-quote-artifact-set/`, fresh; lane never mutated)

Fixture: copy of the committed captures dir + `url-map.json` (sha256
`76c75639110cd95cf56e6cc1a5f0aa16fb129f02d9e818e9580454d15f5c9082`) and
`append-rows.md` (`9d00d4a1…`). Quote rows are the lane's S103/S104 rows rebuilt by the
gate's own 11-cell format with the anchor cell swapped.

**T1 (baseline):** `--quote-file append-rows.md --artifact captures --url-map url-map.committed.json`
→ exit 0, 8/8 located, `artifacts=SHA256SUMS.txt,…` (reproduces the receipt).

**T2 — quote found only in the manifest locates (no map):** row cites Toolathlon main.py
blob URL; quote is `"3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad"`
(sha256 of main.py — verified **absent from the bytes of all four captures**; it exists
only in `SHA256SUMS.txt`):
```
QUOTE rows=1 spans=1 located=1 found=1 … cap=25 artifacts=.hidden-notes,SHA256SUMS.txt,…
  ok S103 words=1 at SHA256SUMS.txt quote="3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad"
EXIT=0
```
The byte-presence gate (the kill rule's exit-7 refusal) passes a quote that lives only in
the manifest.

**T3 — same quote + committed map:** → exit 9 `REFUSED S103 unmapped … at SHA256SUMS.txt`
(`found=1` — bytes found, binding refused only because the committed map has no manifest key).

**T4 — same quote + map with one added key `"SHA256SUMS.txt": <main.py blob URL>`:**
→ exit 0:
```
  ok S103 words=1 at SHA256SUMS.txt quote="3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad" bound=SHA256SUMS.txt->https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py
```
A quote that occurs **nowhere in main.py** is validated and bound to main.py's citation.
The map is caller-authored (same mechanism as the committed entries), so nothing structural
prevents it.

**T5 — sorted-first receipt misattribution (real committed bytes):** quote `"evaluation"`
occurs in the manifest paths AND in main.py/retry.py; committed map:
```
  ok S103 words=1 at SHA256SUMS.txt quote="evaluation" bound=toolathlon-ab-testing-evaluation-main.py->…main.py
```
The receipt prints `at SHA256SUMS.txt` — the locatedness statement names the manifest —
while binding passes through main.py. The manifest's sorted-first position launders the
"at" attribution.

**T6 — manifest as the *sole* artifact:** `--artifact captures/SHA256SUMS.txt` alone
satisfies the S103 row (exit 0, `artifacts=SHA256SUMS.txt`). The gate does not distinguish
a checksum file from the cited source document.

**T7 — generic helper absorption:** added `notes.md` (UTF-8) and `.hidden-notes`
(dotfile) to the sandbox captures copy; both appear in `artifacts=`; a quote present only
in `notes.md` locates and binds (exit 0). `binary.bin` (non-UTF-8) is silently dropped from
the list with no warning when other files load.

**T8/T8b — fabricated manifest content is quotable:** appended a fabricated line
`deadbeefcafebabe  …/fabricated-doc.txt` to the sandbox manifest copy; quote
`"deadbeefcafebabe"` → `ok S103 words=1 at SHA256SUMS.txt`, exit 0; with the manifest-keyed
map it also binds (exit 0). The manifest's *content* is trusted verbatim; the gate never
re-verifies the hashes, so any line a caller puts in `SHA256SUMS.txt` becomes quotable.

## 4. Verdict

**CAUGHT — confirmed uncaught limitation (row 11 of R33C1KillRule).**
`SHA256SUMS.txt` is included in quote search (proven by the lane's own receipt and by
reproduction); a quote found only in the manifest locates (exit 0 via T2), and binding is
green whenever the map declares a manifest key (T4, T8b). The kill rule's byte-presence
refusal is not a document-identity check. Generalizes beyond the manifest: any UTF-8
helper file in the artifact directory (notes, dotfiles, receipts) is a quote source, and
non-UTF-8 helpers vanish silently.

Severity: medium-low for the *committed* round-33 state (the committed map has no manifest
key, so T3 refuses the manifest-only path with exit 9; the green T1 pass uses only real
capture quotes), but the mechanism is open for any future admission: a caller-authored map
entry plus a manifest-only (or fabricated-manifest) quote yields a green gate with no quote
in the cited document. Receipts printed today already name the manifest as a locator (T5).

## 5. Risks / notes for L1

- The gate gives no way to *exclude* helper artifacts; any fix would need an allowlist or
  a digest-bind of loaded texts to `SHA256SUMS.txt` (which itself must not be quotable).
- The lane's committed `SHA256SUMS.txt` does not cover all capture files
  (`swebench-pro-tests-test.sh` has no row) and is never verified by the gate.
- No files in the lane were written, moved, or mutated; the git/jj state is untouched.
  Scratch lives in `/tmp/r33f-quote-artifact-set/` (≈200 KiB). No tool installed.
