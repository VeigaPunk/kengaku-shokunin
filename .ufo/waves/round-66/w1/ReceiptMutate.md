# ReceiptMutate — R66-C2 strict gate, mutation probe (round 66, w1)

Four proposal revisions probed (builder revised mid-wave): A `cd70ed61`, B `92eee57`,
C `06270270`, **D (landing) `b131e66eb74964c0dfc1001d6191115fd5e14587059e3ddc834a6fec0c3854af`**.
Receipts: `runs/` (A), `runs-rev92/` (B), `runs3/` (C), `runs4/` (D). Every run used a
scratch copy; no lane file was edited. Each strict run printed
`CHECK strict probe sha256=f44b7283… rel=plans/round65_c1_sqlite_probe.py`. Full matrices and
per-revision detail: `W/ReceiptMutate/report.md`; fixtures, scripts, `MANIFEST.sha256` there too.

## Baseline (all revisions)
fabricated → exit 1 (A 8 defects, B–D 9); committed R65 receipt → exit 0 `strict-pass`.

## Required mutants — rev D

| id | mutation | exit | first strict finding | verdict |
|---|---|---|---|---|
| a | fabricated + correct GRADER sha | 1 | `fabrication-declaration` / `toolchain-not-well-formed gcc` (9) | refused (identity-by-construction: fixture already carried it) |
| a′ | same as a second GRADER line | 1 | `grader-line-count 2 != 1` (10) | refused |
| b | fabricated + true `PROBE sha256=` | 1 | `fabrication-declaration` (8) | refused |
| c | fabricated + TOOLCHAIN/AMALG/NOBIND copied | 1 | `fabrication-declaration` (5) | refused |
| d | committed, `VECTOR G3` P/P/F → P/F/P | 1 | `vector-mismatch G3=P/F/P != P/P/F` | refused (default also fails) |
| e | committed, one `NOBIND G4` deleted | 1 | `nobind-missing G4` | refused (default also fails) |
| f | committed + `PROBE sha256=000…0` | 1 | `probe-sha 000… != committed f44b7283…` | refused, **strict-only** (default exit 0) |

(f) is literally impossible on the committed receipt (no `PROBE` line; `grep -c '^PROBE '`
→ 0) so the line is inserted; the mutation available on the existing binding
(`version=r65-c1/1` → `r65-c1/2`) is refused as `probe-version`.

## Fixes verified on rev D
- **d3 (rev C ordering bypass) closed**: c3 bytes with the declaration moved below `GRADER`
  now exits 1 `fabrication-declaration`; so does a declaration in a `RUN` driver field.
- **d2 (over-refusal) stays fixed**: committed receipt + `(sqlite3 binary fabricated by
  harness)` in a `LEG` fragment → exit 0.
- **q6**: true `PROBE` line + header `version=r65-c1/0` → exit 1 `probe-version`; both
  bindings validated independently (corrects my earlier rev-B remark).
- **Selftest 17/17, exit 0** in revs B–D.

## Residual survivors on rev D
- **d1 (semantic limit, builder-named)**: header + RUN driver reworded (`SYNTHETIC RECEPT …
  nothing executed`, `driver="transcribed values"`, `frag=synthetic`) → exit 0. Inside the
  builder's stated class; wider than the claims doc's "hand-copied full receipt" wording.
- **e1 (new, lexical scope)**: d1 with the literal declaration text appended to a
  `LEG … frag=` field → exit 0. The scan skips any line whose first token is `LEG` or `ENV`
  (rev D 854–859), so declaration text can ride in those families. Contrived placement, but
  the exemption is a token-based trust boundary, not a provenance check. Measured trade-off:
  any rule that catches e1 also refuses a live grader message containing the phrase (that is
  d2, refused on rev B), so the builder keeps the exemption by design; the remedy would be a
  provenance binding, not a wider phrase scan.
- Accepting lines: D 1006 `ok = not failures and not defects`, declaration loop 854–859,
  `strict_defects` (836–982) returning `[]`.

## Verdict
R66-C2 predicate not falsified on rev D: fabricated fixture refused (kill rule a clear),
committed receipt accepted (kill rule b clear), default output unchanged. Residuals d1/e1
are gate-scope findings (lexical tripwire, not provenance); a provenance proof needs a
live-run binding (`SHAPE` + per-case `BUILD`/`RUN`/`FILES`/`ENV` or nonce/per-case hashes),
which is next-round scope, not a re-judged predicate.

## Restoration
All fixture sha256 identical before/after (`unchanged=true` in `runs4/results.json`);
inputs, committed probe and all four revisions re-hashed unchanged (`17436b58…`, `25c7cab7…`,
`f44b7283…`, `b131e66e…`). `S/ReceiptMutate` removed after receipts were copied here;
`MANIFEST.sha256` verified with `sha256sum -c`.
