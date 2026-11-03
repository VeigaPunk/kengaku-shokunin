# ReceiptMutate — R66-C2 strict-mode mutation probe (round 66, w1)

Seat: mutation tester. The proposal was revised four times mid-wave; each revision was
probed on a scratch copy. No lane file was edited at any point.

| rev | sha256 | receipts |
|---|---|---|
| A | `cd70ed6120da66fc28f15dd14b0fd559af91825cdcb2f9ccaf3027896345f7bc` | `runs/` |
| B | `92eee5720a5c01b8d8918c385a87c684b3eaee38dc474702119f5a1c4a23a173` | `runs-rev92/` |
| C | `062702702d752058842fcddc90c4271e6d1e8ac0c31f8e8c8645683814ed47d4` | `runs3/` |
| **D (landing candidate)** | `b131e66eb74964c0dfc1001d6191115fd5e14587059e3ddc834a6fec0c3854af` | `runs4/` |

Inputs (read-only, hashed at run time): fabricated fixture `17436b58…`, committed R65
receipt `25c7cab7…`, committed probe (the strict `PROBE` binding target) `f44b7283…`.
Every strict run printed
`CHECK strict probe sha256=f44b72834d8662cb6986e192dfbdf236daf6c99a174768294e504f7b634db4eb rel=plans/round65_c1_sqlite_probe.py`.

## Pristine baseline (unmutated bytes, all revisions)

| fixture | exit | result |
|---|---|---|
| fabricated fixture | 1 | 8 defects (A) / 9 defects (B–D, declaration first) |
| committed R65 receipt | 0 | `CHECK ok cases=5 strict=yes`, `strict-pass` |

## Required mutants — rev D (landing bytes)

| id | mutation | exit | first strict finding (defects) | verdict |
|---|---|---|---|---|
| (a) | fabricated + GRADER line with the correct grader sha | 1 | `fabrication-declaration`, then `toolchain-not-well-formed gcc='fabricated'` (9) | refused |
| (a′) | same, added as a *second* GRADER line | 1 | `grader-line-count 2 != 1` (10) | refused |
| (b) | fabricated + true `PROBE sha256=f44b7283…` | 1 | `fabrication-declaration` (8) | refused |
| (c) | fabricated + TOOLCHAIN, AMALG, NOBIND copied | 1 | `fabrication-declaration` (5) | refused |
| (d) | committed, `VECTOR G3=P/P/F` → `P/F/P` | 1 | `vector-mismatch G3=P/F/P != P/P/F` | refused |
| (e) | committed, one `NOBIND G4` line deleted | 1 | `nobind-missing G4` | refused |
| (f) | committed + `PROBE sha256=000…0` (64 zeros) | 1 | `probe-sha 000… != committed f44b7283…` | refused |

Exit codes and value-level findings are identical in revs A–D; only the fabricated family's
first finding changes (the declaration check from rev B on). Facts behind the rows:

- **(a) is identity-by-construction.** The fabricated fixture already carries the correct
  `GRADER sha256=b165f850…`, so "add a GRADER line with the correct sha" reproduces it byte
  for byte (`17436b58…` before and after). Only (a′) adds a line; strict refuses it on count.
- **(f) is literally impossible on the committed receipt**, which has no `PROBE` line
  (`grep -c '^PROBE '` → 0). The mutant inserts one. The mutation available on the existing
  binding (`version=r65-c1/1` → `r65-c1/2`) is refused as
  `probe-version 'r65-c1/2' != 'r65-c1/1'` in every revision.
- **(d)/(e) are not strict-specific kills**: both also fail the default checker (2 `CHECK
  fail` lines each). **(f)** and **(a′)** are refused by strict only — default mode prints
  `CHECK ok cases=5`, exit 0, for both.

## Escalations and survivors, by revision

| id | mutation | A | B | C | D |
|---|---|---|---|---|---|
| (c3) | fabricated + copied values + true `PROBE` line | **0** | 1 decl. | 1 decl. | 1 decl. |
| (c4) | fabricated + copied values + static instrument header (no sha) | **0** | 1 decl. | 1 decl. | 1 decl. |
| (d1) | (c3) with header + RUN driver reworded (`SYNTHETIC`, `transcribed values`, `frag=synthetic`) | — | **0** | **0** | **0** |
| (d2) | committed + LEG fragment `(sqlite3 binary fabricated by harness)` | — | 1 (over-refusal) | **0** | **0** |
| (d3) | (c3) bytes unchanged except declaration lines moved below `GRADER` | — | — | **0** | 1 (fixed) |
| (e1) | (d1) + declaration text appended to a `LEG … frag=` field | — | — | — | **0** |
| (q6) | committed + true `PROBE` line + header `version=r65-c1/0` | — | — | 1 `probe-version` | 1 `probe-version` |
| (f2) | committed + true `PROBE` line (control) | 0 | 0 | 0 | 0 |
| (falt) | committed, instrument version changed | 1 `probe-version` | 1 | 1 | 1 |

Rev A boundary on the fabricated bytes: `8` pristine → `7` +PROBE → `4`
+TOOLCHAIN/AMALG/NOBIND → `1` +banners → `0` +header or +PROBE line. No single family
flipped acceptance; four value families plus one probe binding did.

## Findings on the landing revision (D = `b131e66e`)

1. **d3 is fixed, verified.** The scan now covers every line except `LEG`/`ENV` (D lines
   854–859; the skip is `line.split(" ", 1)[0] in ("LEG", "ENV")`). The d3 receipt — same
   bytes as (c3) with the declaration lines below the `GRADER` — now exits 1 on
   `fabrication-declaration`, and so does a declaration carried in a `RUN` driver field.
   Rev C's ordering bypass is closed.
2. **d2 remains fixed.** The committed receipt with
   `(sqlite3 binary fabricated by harness)` in a `LEG` fragment exits 0: grader-printed free
   text cannot refuse a value-valid receipt.
3. **e1 survives — the exemption is token-based, not provenance-based.** d1 with the
   declaration text moved into a `LEG … frag=` field (the only line family carrying it,
   zero non-exempt hits) exits 0 with the literal
   `FABRICATED RECEPT - contains NO live-run data, no driver run produced this file` present
   in the receipt. Any line whose first token is `LEG` or `ENV` is invisible to the
   tripwire. Placement in a fragment is contrived — a fabricator would not normally declare
   itself there — but it shows the check cannot distinguish grader-printed from
   fabricator-written text in those two families, so the exemption is a trust boundary, not
   a proof.
4. **d1 is the residual the builder now names.** Reworded provenance (`SYNTHETIC RECEPT —
   values transcribed from the frozen claim text, nothing executed`, `driver="transcribed
   values"`, `frag=synthetic`) exits 0. This is the semantic limit of a lexical tripwire and
   is inside the builder's stated survivor class; it remains wider than the claims doc's
   wording of the named limitation, "a hand-copied full receipt", because the measured
   survivor needs four value families, not a copy of the receipt.
5. **q6 confirmed again.** A true `PROBE` line plus a wrong header version exits 1 on
   `probe-version`; both bindings are validated independently, so a correct `PROBE` line
   does not excuse a wrong header. (My earlier rev-B remark that `probe_lines` wins was
   wrong; corrected.)
6. **Selftest 17/17, exit 0** in revs B, C and D (`runs-rev92/selftest.txt`,
   `runs3/selftest.txt`, `runs4/selftest.txt`), including `strict-declared-fabricated` and
   `strict-valid-receipt`.
7. **d2 and e1 are the two sides of one trade-off, and my own mutants measure both.** Rev B
   scanned every line: d2 (a harness-authored `LEG` fragment containing `fabricated`,
   standing in for a live grader message) exited 1. Rev D exempts `LEG`/`ENV`: e1 (the same
   declaration text placed in a `LEG` field) exits 0. Any rule that catches e1 also refuses a
   live receipt whose captured message contains one of the four phrases, because a receipt
   has no field recording who wrote a `frag=` value. The builder's disposition — keep the
   exemption, record it as a trust boundary, no code change after this run — is consistent
   with those bytes. A real fixation would be a provenance binding (per-case artifact hash
   or nonce), not a wider phrase scan.

Accepting lines in rev D: acceptance at D line 1006 `ok = not failures and not defects`,
with the declaration loop skipping `LEG`/`ENV` (854–859), `strict_defects` (836–982)
returning `[]` at 982, and the probe binding satisfied. `strict_defects` still never inspects `SHAPE`, `BUILD`, `RUN`,
`FILES`, `CASE`, `LEG`, `PREDICTION`, or any provenance binding beyond the phrase list and
the six value families.

## Verdict for R66-C2 (rev D `b131e66e`)

The claim's predicate is not falsified: strict exits 1 on the named fabricated fixture
(kill rule a clear), exits 0 on the committed receipt (kill rule b clear), and default mode
is unchanged. The declaration check has converged to a lexical tripwire that refuses the
named fixture and every accidental declaration shape (header, moved header, RUN driver),
while exempting grader text. Two residual survivors, both scope findings rather than
predicate failures: **d1** (reworded provenance — the semantic limit the builder now names)
and **e1** (declaration text riding in an exempt `LEG`/`ENV` line — a token-based trust
boundary). A provenance proof would need a live-run binding (`SHAPE` plus per-case
`BUILD`/`RUN`/`FILES`/`ENV`, or a nonce/per-case artifact hash as in the C1 probe), not a
phrase list; that is next-round scope, not a re-judged predicate.

Final state on `b131e66e`: no code change after these runs (the builder re-hashed the file
and confirmed it), so `runs4/` is valid evidence for the landing sha. The exemption stays,
by design, with the trust boundary stated; the residual class is exactly "four value
families + no literal phrase in a non-`LEG`/`ENV` line" (witnesses d1 and e1).

## Restoration evidence

- Every fixture sha256 identical before and after its run (`unchanged=true` for all rows in
  `runs4/results.json`; earlier revisions likewise). Read-only inputs, committed probe and
  all four proposal revisions re-hashed after the runs and unchanged (`17436b58…`,
  `25c7cab7…`, `f44b7283…`, `b131e66e…`).
- `S/ReceiptMutate` removed at exit; receipts copied here first under `runs/`,
  `runs-rev92/`, `runs3/`, `runs4/`, plus `fixtures/` and the five generator/runner scripts;
  `MANIFEST.sha256` verified with `sha256sum -c`.
