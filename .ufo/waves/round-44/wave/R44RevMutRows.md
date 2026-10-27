# R44RevMutRows — MUTANTS row review (round-44 C1 counter)

Seat: R44RevMutRows (reviewer, leaf). Scope: the five MUTANTS rows of `plans/round44_c1_verify.py:230-256` against the pinned tools `plans/anchor_digest_check.py` and `plans/order_check.py`, and direction labels against `.ufo/waves/round-44/claims/witness-run.txt`.

## Method

- Each row's `old`/`new` were taken verbatim from the MUTANTS table (read at `plans/round44_c1_verify.py:228-256`).
- Occurrence/span checks reproduce exactly what the counter itself does (round44_c1_verify.py:851 `src.count(old) != 1` → invalid; :852 `old.count("\n") != new.count("\n")` → invalid; :858 `src.replace(old, new, 1)`; :866-867 span lines): source text = `(lane / TOOLS[tool]).read_text()`, count substrings, locate first occurrence, compute start line and span, and `compile()` the replaced text for syntax.
- Advertising ranges pasted with `sed -n` from the pinned tools.
- Direction labels cross-checked against witness-run.txt MUTANT lines.

## Row verdicts

### U5 — anchor, digest-short, silence, direct — **ok**
- `old` = `cls, why = ("digest-short" if len(tok) < 64 else "digest-long")` occurs **exactly once** (count=1), at line 522 of `plans/anchor_digest_check.py`; first line of the replaced span L522 (matches witness attribution `attributed=L522`).
- `new` flips the first branch: `("digest-long" if len(tok) < 64 else "digest-long")` — single minimal replacement (one string literal), newline count preserved (0/0), mutant compiles. Effect matches advertised "a short token labelled digest-long".
- Advertised quote `any other anchor token must be exactly 64 lowercase hex digits (`digest-short`, `digest-long`` — verbatim on cited line 88 (`sed -n '86,90p'`: `  * any other anchor token must be exactly 64 lowercase hex digits (`digest-short`, `digest-long`,`).
- Direction `silence` matches witness-run.txt line 10 `MUTANT U5 anchor silence`; class `digest-short` matches fixture `u5-sixty-three-hex declared=digest-short` (witness-run.txt line 5).

### U6 — anchor, digest-long, silence, direct — **ok**
- Same `old` as U5, occurs exactly once at line 522 (count=1); span L522 (matches witness `attributed=L522`).
- `new` flips the second branch: `("digest-short" if len(tok) < 64 else "digest-short")` — single minimal replacement, newline count preserved, compiles. Effect matches advertised "a long token labelled digest-short".
- Same quote verbatim on line 88.
- Direction `silence` matches witness-run.txt line 11 `MUTANT U6 anchor silence`; class `digest-long` matches fixture `u6-sixty-five-hex declared=digest-long` (witness-run.txt line 6).

### U7 — anchor, -, rc-mirror, direct — **ok**
- `old` multi-line block `hit = sorted(p for p, ent in per.items() if tok in ent["digests"])\n                claimed.update(hit)\n                if verbose:\n                    path, how` occurs **exactly once** (count=1), matching lines 539-542 of the pinned anchor tool (first line matched as the continuation suffix of L539, which carries 16 leading spaces): `sed -n '537,543p'` shows L539 `                hit = sorted(p for p, ent in per.items() if tok in ent["digests"])`, L540 `                claimed.update(hit)`, L541 `                if verbose:`, L542 `                    path, how, label = row_scope[tok]`. Span L539-L542 (matches witness `attributed=L539`).
- `new` adds `[:1]` to the `sorted(...)` call — single minimal insertion at one point; newline count preserved (3/3), compiles. Effect matches advertised "only the first resolving capture is claimed".
- Advertised quote `A token that resolves to several of the row's captures is not a defect` — verbatim across cited lines 98-99 (`sed -n '97,101p'`: L98 ends `A token that`, L99 begins `resolves to several of the row's captures is not a defect — that means …`).
- Direction `rc-mirror` matches witness-run.txt line 12 `MUTANT U7 anchor rc-mirror`; class `-` is valid for rc-mirror (counter validity rule :853 passes).

### U9 — anchor, -, rc-mirror, direct — **ok**
- `old` = `f.read_text(encoding="utf-8", errors="replace")` occurs **exactly once** (count=1), at line 384 of the pinned anchor tool (the only other `read_text(...)` at L398 uses receiver `(lane / "corpus/SOURCES.md")`, not `f`). Span L384 (matches witness `attributed=L384`).
- `new` = `git(lane, "show", "HEAD:" + p).decode("utf-8", "replace")` — one statement swapped at one site (reads HEAD blob instead of working tree); newline count preserved (0/0), compiles, and `p` is in scope (loop variable at `load_errata`, anchor tool L377). Effect matches advertised "lessons read from HEAD instead".
- Advertised quote `lessons are read from the working tree for paths committed at HEAD, so a seat's erratum counts before it is committed` — verbatim across cited lines 106-107 (`sed -n '105,109p'`: L106 ends `lessons are read from`, L107 begins `the working tree for paths committed at HEAD, so a seat's erratum counts before it is committed while the`).
- Direction `rc-mirror` matches witness-run.txt line 13 `MUTANT U9 anchor rc-mirror`; class `-` valid for rc-mirror.

### U14c — order, -, error, direct — **ok**
- `old` = `        if not m:\n            raise SetupError(f"claims file name` occurs **exactly once** (count=1), at lines 161-162 of `plans/order_check.py` (`sed -n '159,164p'`: L161 `        if not m:`, L162 `            raise SetupError(f"claims file name is not round-NN-claims.md: {claims}")`). Span L161-L162 (matches witness `attributed=L161`).
- `new` = `        if False:\n            raise SetupError(f"claims file name` — single minimal replacement (`not m` → `False`), newline count preserved (1/1), compiles. Effect matches advertised "the claims-name guard disabled" (odd claims name no longer raises; exit becomes 0/1 instead of 2 → error direction).
- Advertised quote `Exit: 0 order holds · 1 order broken · 2 setup error (... unparseable round number, bad arguments)` — the quoted words appear verbatim in cited range 26-27 (`sed -n '24,28p'`: L26 `Exit: 0 order holds · 1 order broken · 2 setup error (not a git work tree, claims or receipt never`, L27 `committed, unparseable round number, bad arguments).`). Note: `(...` is an elision marker standing in for `(not a git work tree, claims or receipt never committed,`; the remaining quoted words are verbatim and in order across the cited range.
- Direction `error` matches witness-run.txt line 14 `MUTANT U14c order error`; class `-` valid for error direction.

## Cross-checks

- `old` count = 1 for all five rows; `new` count = 0 in every pinned tool (no accidental double-hit); `old.count("\n") == new.count("\n")` for all five (counter validity gate :852 passes).
- All five mutants compile after substitution; all five reference tools compile.
- All five direction labels match witness-run.txt MUTANT lines verbatim; all five adv_kind = `direct` (witness ADVERTISED direct=5, line 18).
- Span start lines (L522, L522, L539, L384, L161) match the witness-run attribution legs (`attributed=L522 / L539 / L384 / L161`).
- Classes align with declared fixture defects: U5↔u5-sixty-three-hex (digest-short), U6↔u6-sixty-five-hex (digest-long), U7↔u7-twin-captures (accept), U9↔u9-dirty-erratum (accept), U14c↔u14c-odd-claims-name (error).

## Findings

No defects found. Five rows reviewed: U5 ok, U6 ok, U7 ok, U9 ok, U14c ok (the U14c advertised quote's `(...` elision is a cosmetic ellipsis; all quoted words are verbatim in the cited range).

VERDICT: mutant-rows-5/5
