# Draft — round-93 lesson `## Gate` block (S290–S296)

Draft only; the L1 integrates. Format source: `corpus/lessons/round-92.md` `## Gate` (six
columns: candidate · decision · access · located quote and location · reason · flip; the same
preamble sentence; the same census footer).

**Every cell is taken from the SOURCES row itself** (`corpus/SOURCES.md` lines 306–312, ids
S290–S296, committed at C `22972a31`): `id` + `source` → candidate; `tier` + `status` →
decision; `anchor` → access and located quote; `teaches` → reason and flip; `opened` → the
access date; `kind` → the dataset/code tag. Nothing here is re-derived from the probe, and
nothing is taken from the round-93 claims file.

Two kinds of cell are **not** in the SOURCES rows and are marked inline:
`[not in the row: …]` for the flip cells of the four admitted rows (S290–S293 carry no `flip:`
clause in `teaches`, only the rejected rows do), and `[not confirmed: …]` for one size figure
(S295's "about 4.2 MB"). Everything else was re-measured against the pinned bytes and holds
(receipts in `receipts/source-verification.txt`).

---

## Text to land (verbatim)

```markdown
## Gate

Candidates opened this round (CORPUS rule 1: each row written only after its source was opened
here, with URL, access date and a located quote; every fetch HTTP 200 on 2026-11-05 from
raw.githubusercontent.com at `2fd12b88aafdd04a52c298e3940bcb189f9766d6`).

| candidate | decision | access | located quote and location | reason | flip |
|---|---|---|---|---|---|
| S290 `schemelike-metacircular-eval/tests/test_outputs.py` @ `2fd12b88` (member replay only) | **admit** (tier A) | 2026-11-05, raw.githubusercontent.com, HTTP 200, 6823 B, sha256 `fbb84e3c…9be7ed`, byte-identical to the lane capture | line 121: `def test_interp():` (2 words); `assert failed == 0` at :220 | one function runs every test program directly (10 s timeout) and through eval.scm (60 s timeout), strips one trailing True line from each side, and asserts failed == 0; with no test programs it returns 1 before any assert, so it passes with no evaluator (case C07) | [not in the row: no `flip:` clause — the row's own scope is the single test function this round's eleventh offline replay grades, as the captured bytes define it; a claim about the TB2 harness or a real submission would need its own receipt] |
| S291 `schemelike-metacircular-eval/tests/interp.py` @ `2fd12b88` (member replay only) | **admit** (tier A) | 2026-11-05, same base URL, HTTP 200, 17578 B, sha256 `efb8b5cd…bea2c1`, byte-identical to the lane capture and to `environment/tests/interp.py` | line 381: `env.define("newline", lambda: print())` (3 words) | the grader copies this file next to each test program and runs it as `python3 interp.py`; the probe stages it unmodified at /app and /tests | [not in the row: no `flip:` clause — an interpreter-version claim would need a new fetch at a new revision] |
| S292 `schemelike-metacircular-eval/solution/solve.sh` @ `2fd12b88` (member replay only) | **admit** (tier A) | 2026-11-05, same base URL, HTTP 200, 11910 B, sha256 `e2c5b0ac…712510`, byte-identical to the lane capture | line 4: `cat <<'EOF' > eval.scm` (4 words) | the heredoc body passes all 63 captured programs (C01); one changed primitive mapping drops it to 19 of 63 (C04); a bare trailing True drops it to 56 of 63 (C08) | [not in the row: no `flip:` clause — the row's own scope is the task author's reference eval.scm, the replay's positive control and the base of its derived variants] |
| S293 `schemelike-metacircular-eval/tests/test/` + `tests/shadow_test/` (63 `.scm` programs, dataset) @ `2fd12b88` (member replay only) | **admit** (tier A) | 2026-11-05, same base URL, HTTP 200 for all 63; `tests/test/01-factorial.scm` sha256 `2623000a…26a6ad`; sorted sha256 manifest of the 63 files hashes to `227d7bd1…e1be8f` | `tests/test/01-factorial.scm:1` quote `;; Test 1: Factorial - Classic recursive function` (8 words) | the 63 programs (32 in test/, 31 in shadow_test/) the grader enumerates by glob; shadow_test/ repeats test/ programs with changed constants, so an evaluator that memorizes outputs cannot pass both; calculator.scm exists only in test/ | [not in the row: no `flip:` clause — the row's own scope is the 63 programs the grader enumerates by glob] |
| S294 `schemelike-metacircular-eval/tests/test.sh` @ `2fd12b88` (verifier wrapper) | **reject** | 2026-11-05, same base URL, HTTP 200, sha256 `4770437e…e6c334`, byte-identical to the lane capture `corpus/evidence/round93/graders/schemelike-metacircular-eval/tests/test.sh` | line 3: `# Install curl` (3 words) | REJECTED: installs curl and uv over the network and runs pytest under uvx on Python 3.13, which the offline replay forbids; the grader semantics live in S290 | a claim about verifier-harness reward semantics opened as its own replay with the network legs pinned |
| S295 `financial-document-processor/tests/test_outputs.py` @ `2fd12b88` (member candidate) | **reject** | 2026-11-05, same base URL, HTTP 200, 10336 B, sha256 `978f506a…7f5a9a`; not captured in the round-93 capture tree, but byte-identical to the lane's round-52 capture `corpus/evidence/round52/graders/financial-document-processor/tests/test_outputs.py` | line 14: `digest = hashlib.file_digest(f, "sha512")` (4 words) | REJECTED as this round's member: a full-pass case needs the 17 environment documents (about 4.2 MB of jpg/pdf [not confirmed: the 17 documents at the pin total 4,002,650 B = 3.82 MiB]) whose sha512 digests the grader pins, and the grader imports pandas, absent on this host | a round that captures the documents and supplies pandas offline |
| S296 `large-scale-text-editing/tests/test_outputs.py` @ `2fd12b88` (member candidate) | **reject** | 2026-11-05, same base URL, HTTP 200, 8935 B, sha256 `f5e69f4f…e4cd43`; not captured in the round-93 capture tree, but byte-identical to the lane's round-52 capture `corpus/evidence/round52/graders/large-scale-text-editing/tests/test_outputs.py` | line 170: `cmd = ["vim", "-Nu", "NONE", "-n", "-Es", str(INPUT), "-S", str(APPLY_SCRIPT)]` (10 words) | REJECTED as this round's member: two of its five test functions run vim headlessly (test_apply_macros_runs, test_macros_nonempty_and_efficient) and vim is absent on this host (`which vim` → not found) while pacman is paused | vim installed through an official channel |

Round-start census (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
kengaku`): exit 0, `kengaku ok`, 281 registry rows (30 pre-existing W04 duplicate-url warnings)
(`.ufo/waves/round-93/L1/census-start.txt`). Round-end census: exit 0, `kengaku ok`, 288 registry
rows, 30 W04 duplicate-url warnings (`bash scripts/sources-census.sh census --root
/home/vgpnk/Projects/shokunin kengaku`).
```

---

## Values not confirmed (marked inline above)

1. **S295, "about 4.2 MB of jpg/pdf".** Not confirmed. The 17 documents at the pinned tree
   (`corpus/evidence/round53/pin-tree-2fd12b88.json`) total **4,002,650 B = 3.82 MiB = 4.00 MB**
   (11 `.jpg` + 6 `.pdf`); the whole task tree including `solution/solve.sh` is 4,031,474 B =
   3.84 MiB. "About 4.2 MB" matches neither. The file *count* (17) is exact and the mix
   (`jpg`/`pdf`) is right; only the size figure is off by about 5 %. All 17 documents were
   re-fetched (HTTP 200, sizes equal to the pin) and their sha512 digests match the grader's 17
   pinned digests exactly, one for one (`receipts/source-verification.txt` R7).
2. **S295 / S296, "not captured in the lane".** True only of the round-93 capture tree; both
   files *are* in the lane, byte-identical, under `corpus/evidence/round52/graders/`. The draft
   says so rather than repeating "not captured in the lane", because a reader checking the
   sha256 against the lane will find the bytes.
3. **Flip cells for S290–S293.** The four admitted rows carry no `flip:` clause in their `teaches`
   cell (only the three rejected rows do), so there is no flip value in the SOURCES rows to take.
   The draft marks those cells `[not in the row: …]` and quotes the row's own `scope` cell, so
   the reader can see the limit is the row's and not an invention.

## Values confirmed by re-measurement (not marked inline)

- Every sha256 and byte count in the `access` column (S290–S296) was re-fetched from
  `raw.githubusercontent.com` at `2fd12b88` on 2026-11-05: HTTP 200, byte counts equal to the row,
  sha256 equal to the row. The four files captured in the lane match their rows byte for byte.
- Every located quote sits at the cited line of the cited file, and every word count equals the
  row's count (2, 3, 4, 8, 3, 4, 10).
- S293's sorted-manifest digest reproduces (`227d7bd1…e1be8f`) — but only over the `sha256sum`
  *listing* (paths included, sorted); the bare-hash variant hashes to `c6f397ff…d746` and a
  path-prefixed variant to `a4a2892d…681e`. The row states the value but not the recipe; the
  recipe above is the one that reproduces it.
- S291's "byte-identical to … `environment/tests/interp.py`" holds: the pinned tree gives both
  paths the same git blob id `5bbc7664f6abdc16a39f4c10bea32679e0975186` (17578 B).
- The 63-program split (32 `test/` + 31 `shadow_test/`), `shadow_test/`'s changed constants and
  `calculator.scm` living only in `test/` all hold.
- S290's grader semantics hold in the captured bytes: 10 s direct timeout, 60 s through-eval
  timeout, one trailing `True` line stripped per side, `assert failed == 0` at :220, and the
  no-test-programs path returning 1 at :136 before any assert. Under pytest 8.4.1 (the version
  `tests/test.sh` pins) a non-`None` return is a warning, not a failure — measured on this host
  in a Python 3.13 venv (`receipts/source-verification.txt` R10), so the row's "it passes with
  no evaluator" is the verdict pytest would also report.
- S292's C01/C04/C08 numbers match the committed receipt `corpus/evidence/round93/scheme-probe.txt`
  (63/0, 19/44, 56/7).
- S295's pandas claim holds (`import pandas` → `ModuleNotFoundError` on this host) and S296's
  vim claim holds (`which vim` → not found; five test functions, the two named ones shell out to
  vim).
- The census footer is measured: validate exits 0 with `kengaku ok` (30 pre-existing W04), census
  reports 288 rows after this round's seven rows were added (281 at round start + 7).

## Notes for the L1 (not part of the landed text)

- The **already-committed** `corpus/lessons/round-93.md` Gate block (commit `fb79ef74`) differs
  from the SOURCES rows in ways the L1 should decide on before this block replaces it:
  (a) its S292 digest truncation `e2c5b0ac…10512` is not a suffix of the true digest
  `e2c5b0ac2bef…f712510` — the last five characters are `12510`, and `10512` does not occur in
  the digest at all; the draft uses `e2c5b0ac…712510`;
  (b) its S290/S292/S293 rows paraphrase the rows' `teaches` cell and drop the S290
  "passes with no evaluator (case C07)" and the S293 "32 in test/, 31 in shadow_test/" facts;
  (c) its S295 row repeats "about 4.2 MB" without the size correction;
  (d) its S295/S296 rows repeat "not captured in the lane", which the lane's own round-52
  capture contradicts.
  A filed lesson is never rewritten in place (QUALITY Q55): the correction is a new row or an
  erratum commit that names the superseded text.
- The truncations in the committed block use a 4–5 character tail; the round-92 file's house style
  is head-8 / tail-6 (`80b06b7c…d96ffa`). This draft uses head-8 / tail-6 throughout.
- The SOURCES `used-by` cells for these rows name `plans/round93-cases.json` (S290, S293) and
  `plans/round93_scheme_probe.py` (S291, S292); the census `E11` check (used-by path missing on
  disk) is clean, so both paths exist at the measured tip.
