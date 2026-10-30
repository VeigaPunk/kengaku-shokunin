# C3VacuityAttack — independent 12-case derivation vs frozen R55-C3 oracle

Seat: C3VacuityAttack (kengaku round 55, wave 1). Date: 2026-10-30.
Basis: frozen case table in `plans/round55_c3_chess_probe.py` @ commit 80afa613
(round-55 claims freeze); captured grader
`corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py`
(sha256 verified == frozen pin `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286`).

The oracle's only instruction is the grader's one assertion:

```python
move = Path("/app/move.txt").read_text().strip().split()
assert sorted(move) == sorted(["g2g4", "e2e4"])
```

Constant target: `sorted(["g2g4","e2e4"]) == ["e2e4","g2g4"]` (codepoint order, stable
across CPython 3.x; no locale/hash involvement). Case bytes are what the probe
materializes: `content.encode("utf-8")`; sandbox ENV pins UTF-8
(`PYTHONUTF8=1`, `LC_ALL=C.UTF-8`), so `read_text()` decodes UTF-8 with
`newline=None` (universal newlines: `\r\n`→`\n`).

| # | case (frozen name) | move.txt bytes | tokens after `read_text().strip().split()` | `sorted(tokens)` | my verdict | frozen | delta |
|---|--------------------|----------------|--------------------------------------------|------------------|-----------|--------|-------|
| 1 | both-lowercase-two-lines | `b'g2g4\ne2e4\n'` | `['g2g4','e2e4']` | `['e2e4','g2g4']` == target | **P** | P | — |
| 2 | both-space-separated | `b'g2g4 e2e4'` | `['g2g4','e2e4']` | `['e2e4','g2g4']` == target | **P** | P | — |
| 3 | reversed-order | `b'e2e4 g2g4'` | `['e2e4','g2g4']` | `['e2e4','g2g4']` == target | **P** | P | — |
| 4 | single-move-only | `b'g2g4\n'` | `['g2g4']` | len 1 ≠ len 2 | **F** | F | — |
| 5 | uppercase-white | `b'G2G4\ne2e4\n'` | `['G2G4','e2e4']` | `['G2G4','e2e4']` ('G'=0x47 < 'e'=0x65) ≠ `['e2e4','g2g4']` | **F** | F | — |
| 6 | extra-decoy-move | `b'g2g4\ne2e4\na2a3\n'` | `['g2g4','e2e4','a2a3']` | len 3 ≠ len 2 | **F** | F | — |
| 7 | duplicate-move | `b'g2g4\ne2e4\ne2e4\n'` | `['g2g4','e2e4','e2e4']` | `['e2e4','e2e4','g2g4']` ≠ target (cardinality) | **F** | F | — |
| 8 | whitespace-padded | `b'  g2g4   e2e4  \n\n'` | `['g2g4','e2e4']` (`strip` eats end runs incl. blank lines; `split` collapses interior runs) | `['e2e4','g2g4']` == target | **P** | P | — |
| 9 | empty-file | `b''` | `[]` (`''.split() == []`) | `[]` ≠ target | **F** | F | — |
| 10 | crlf-line-endings | `b'g2g4\r\ne2e4\r\n'` | `['g2g4','e2e4']` | `['e2e4','g2g4']` == target | **P** | P | — |
| 11 | instruction-example-h1h8 | `b'h1h8\ne2e4\n'` | `['h1h8','e2e4']` | `['e2e4','h1h8']` ≠ `['e2e4','g2g4']` | **F** | F | — |
| 12 | fullwidth-unicode-digit | `b'g\xef\xbc\x92g4\ne2e4\n'` (U+FF12 FULLWIDTH DIGIT TWO) | `['g２g4','e2e4']` | `['e2e4','g２g4']` ≠ target (`'g２g4' != 'g2g4'`) | **F** | F | — |

**Deltas: 0 / 12.** Every frozen prediction is reproduced by derivation from the
assertion alone. No pre-run prediction error to surface.

## Called-out risk areas — cleared

- **CRLF (case 10):** `Path.read_text()` opens with `newline=None` → universal
  newlines translate `\r\n`→`\n` before `strip`/`split` (verified empirically:
  `read_text(b'g2g4\r\ne2e4\r\n')` → `'g2g4\ne2e4\n'`). Defense in depth:
  `'\r'.isspace()` is True, so `split()` would tokenize identically even with
  translation disabled. Verdict P is over-determined, not underdetermined.
  (Nit, not a risk: the frozen comment names only the `split` mechanism; the
  primary mechanism is `read_text`'s newline translation.)
- **Fullwidth digit (case 12):** the probe writes `content.encode("utf-8")`, so
  the bytes are exactly `67 EF BC 92 67 34 0A 65 32 65 34 0A`; under the pinned
  UTF-8 decode the token is `'g２g4'` (U+FF12), and `'\uff12'.isspace()` is
  False, so no token-splitting rescue — `sorted` equality fails on the first
  element comparison. Verdict F is exact-string, robust.
- **Whitespace-padded (case 8):** `.strip().split()` order — `strip` removes
  leading/trailing whitespace runs (both spaces and the trailing `\n\n` blank
  lines), `split()` with no argument then collapses any interior run and drops
  empty strings. Tokens exactly `['g2g4','e2e4']`. P robust. (`split` alone
  would give the same result; `strip` is redundant but harmless.)

## Vacuity / underdetermination sweep (why the oracle is total over these 12)

- **Verdict mapping totality:** probe maps rc 0 → P, `"AssertionError"` in
  output → F, else SETUP. For all 12 cases the grader can only exit 0 or raise
  `AssertionError`: the file always exists (probe writes it), the bytes are
  valid UTF-8 by construction (no `UnicodeDecodeError`), and the grader body
  contains no other raising statement than the `assert`.
- **Version independence:** `read_text`/`strip`/`split`/`sorted`/list-`==`
  semantics are unchanged across CPython 3.x; `sorted` is codepoint order
  (no locale, no hash randomization).
- **Encoding pinning:** `PYTHONUTF8=1` + `LC_ALL=C.UTF-8` fix `read_text`'s
  codec to UTF-8; even if both were dropped, the C.UTF-8 locale still yields
  UTF-8, and cases 1–11 are pure ASCII (codec-invariant). Case 12 is the only
  non-ASCII case and is pinned twice over.
- **Multiset semantics:** the assertion is full-multiset equality after sorting
  both sides with the identical procedure; there is no case where list
  equality could disagree with multiset comparison here.

## Bottom line

No case exists whose prediction the grader source underdetermines, and no
frozen prediction is wrong. The strongest counterexample available from local
evidence is the CRLF comment's mechanism description (translation vs. split),
which is a documentation imprecision, not a prediction defect, and cannot fire
the R55-C3 kill rule (which targets miscounted mismatches, foreign oracles, or
a failed upstream-identity check — all intact: sha256 verified against the
frozen pin above).
