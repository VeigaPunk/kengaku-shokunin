# R33FMultipleCaptures — multiple containing capture selection in `sources_adopt.py`

Seat: `KengakuR33.R33FMultipleCaptures` (leaf). Date: 2026-10-25. Lane:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` @ `77ac8c1307ba60e9572a7e2789b71ae31b133440`.

Target: `plans/sources_adopt.py` `locates` / `locating_artifacts` / `bind_failure` /
`quote_check` (HEAD `77ac8c1`; module sha256 `38492bf175e0c619596c69911954e3b3c247166bdc240f8c1d44a02b7f4103e0`), imported read-only via `importlib.util.spec_from_file_location`; every run uses the unmodified real functions. All fixtures in `/tmp/r33-multicap/`; no lane file mutated except this report.

## Method

`--artifact` is a directory ⇒ `load_artifact` builds the loaded list in **sorted path order** (`sorted(item for item in path.rglob("*") if item.is_file())`, `sources_adopt.py:330`). `locates` = first containing artifact in that order (`:404-413`); `bind_failure` receives the *whole* containing set and returns the first mapped containing artifact whose normalized URL is in the row's cited set (`:415-453`). The two real Toolathlon captures (committed bytes, sha256 `3bad26b6…` main.py / `db11e66e…` retry.py) share the real substring `except Exception as e` (main.py:121/141/216/259/293, retry.py:86 as `except Exception as exc:`). Fixture rows cite `…/blob/9be8d8fe…/tasks/finalpool/ab-testing/evaluation/main.py` (MAIN) or `…/blob/9be8d8fe…/utils/evaluation/retry.py` (RETRY).

## Observations (all verbatim from the harness runs)

`loaded order: ['a-decoy-main.py', 'b-real-retry.py']` · `locating_artifacts(quote): ['a-decoy-main.py', 'b-real-retry.py']` · `locates(quote): 'a-decoy-main.py'`.

| case | artifacts | map | row cites | exit | receipt line (verbatim) |
|---|---|---|---|---|---|
| A | decoy+real, both contain quote | decoy→MAIN, real→RETRY | RETRY | 0 | `ok S510 words=4 at a-decoy-main.py … bound=b-real-retry.py->…retry.py` |
| B | same | same | MAIN | 0 | `ok S511 … at a-decoy-main.py … bound=a-decoy-main.py->…main.py` |
| C | same | decoy→MAIN only (real capture unmapped) | RETRY | **8** | `REFUSED S512 url-mismatch words=4 at a-decoy-main.py …` |
| D | same | decoy→RETRY (misdeclared), real→MAIN | RETRY | 0 | `ok S513 … at a-decoy-main.py … bound=a-decoy-main.py->…retry.py` |
| E | same | real→RETRY only (decoy unmapped) | RETRY | 0 | `ok S514 … at a-decoy-main.py … bound=b-real-retry.py->…retry.py` |
| F | renamed: `z-decoy-main.py` sorts after real | real→RETRY, z-decoy→MAIN | RETRY | 0 | `ok S516 … at b-real-retry.py … bound=b-real-retry.py->…retry.py` |
| G | same | decoy→X, real→Y (both unrelated) | MAIN | 8 | `REFUSED S515 url-mismatch words=4 at a-decoy-main.py …` |
| H/H2 | synthetic `a-paper.html`+`b-blog.html` share `"the verifier never runs in the agent's sandbox"` | paper→arXiv, blog→example.invalid | arXiv then blog | 0 / 0 | `at a-paper.html … bound=a-paper.html->…` / `at a-paper.html … bound=b-blog.html->…` |

CLI end-to-end (E): `python3 plans/sources_adopt.py --quote-file quotes-E.txt --artifact art --url-map map-E.json` → `QUOTE rows=1 spans=1 located=1 found=1 … artifacts=a-decoy-main.py,b-real-retry.py mismatch=0 unmapped=0 … entries=1`, `ok S514 words=4 at a-decoy-main.py … bound=b-real-retry.py->…retry.py`, `EXIT=0`.

## Findings

1. **`locates` picks the first containing artifact in sorted path order, regardless of which artifact the row cites.** In E/H2 the receipt's `at` field names a document the row does *not* cite (`a-decoy-main.py` / `a-paper.html`), while the pass is carried by a different containing artifact (`b-real-retry.py` / `b-blog.html`). The `at` field is a citation-independent sweep-first match — pure name-order evidence, not attribution.
2. **`bind_failure` does consider every containing artifact (existential).** A correctly mapped capture that sorts later is not refused (A, E, H2) — the documented round-31 design intent holds.
3. **Multiplicity is unobservable in the receipt and has no exit code.** One quote in N>1 captures prints one `at` and one `bound`; there is no count, no `ambiguous`/`multi` verdict, no distinct exit. Identical bytes renamed (F) flip the receipt's `at` with no content change: `at a-decoy-main.py` → `at b-real-retry.py`.
4. **`unmapped` (exit 9) cannot be attributed to the row's own capture.** The docstring's stated distinction — "an unmapped artifact is a gap in the caller's map" — is evaluated over the *aggregate* containing set, so it is unreachable whenever at least one containing artifact has a map entry. A row whose own capture is missing from the map is reported as `url-mismatch` (exit 8, case C) if any *other* containing artifact is mapped elsewhere, or green (exit 0, case E/D) if some other containing artifact is mapped to a cited URL. The gate never learns which artifact is *the row's* document; only the caller-authored map can express that, and nothing checks the map key against the row's `source` cell.
5. **No gate-level pass/fail defect found.** Refusal still fires whenever *no* containing artifact maps to a cited URL (G → exit 8; all-unmapped → exit 9). The multi-capture behavior is a reporting/attribution limitation, not a wrong exit code.

## Verdict

**LIMITATION (multi-capture selection and receipt attribution), UNCAUGHT as a binding defect.** `locates` deterministically chooses the first containing artifact (sorted), `bind_failure` genuinely considers all containing artifacts — the claim's mechanism holds. What fails is auditability: the receipt's `at` field is citation-independent and order-dependent, quote multiplicity is invisible, and `unmapped`/`mismatch` verdicts cannot be tied to the row's own capture.

## Risks / flag for L1

- A receipt consumer treating `at <name>` as "the quote was verified in this document" will be misled whenever the quote is shared across captures (the committed `gate-receipts.txt` is not affected — I verified all eight committed S103/S104 quotes occur in exactly one capture: `in-main=True in-retry=False` ×5, `in-main=False in-retry=False` ×3).
- If the C1 kill rule is interpreted as "the row's own capture must contain the quote", the gate cannot enforce it: the map is the only row↔artifact link and is caller-authored (root-level citations accept any capture declared against that root — see R33C1KillRule rows 2/12 for the materialized variant).

## Receipts

- Harness: `/tmp/r33-multicap/harness.py`, `harness2.py`, `quotes-E.txt`, `map-E.json` (outputs quoted verbatim above).
- Fixture real captures: byte copies of committed `toolathlon-ab-testing-evaluation-main.py` (`3bad26b6…`) and `toolathlon-utils-evaluation-retry.py` (`db11e66e…`); synthetic `a-paper.html`/`b-blog.html`.
- No tools installed; tools used: python3, cp, shutil, grep/sed (read-only). Lane bytes untouched (HEAD `77ac8c1` unchanged; module sha above matches the lane).
