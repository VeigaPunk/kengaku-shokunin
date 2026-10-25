# R33FN5Sentence — N5 correction semantics: check_n5 false-passes a non-correction (round 33 falsify wave)

Seat: `KengakuR33.R33FN5Sentence` (executor / leaf). Target: C2/N5 counter `check_n5` in
`plans/round33_defects.py` (sha256 `6ef17abc7ac11cc294efde5e23a3679e1335d5e42ef4a840069a70287064d5b6`,
unchanged before/after this run) against frozen claim `plans/round-33-claims.md:95-96`.

Frozen predicate (claims.md:95-96):

> N5 `corpus/lessons/round-31.md` still contains `:35-38` and carries a labelled
> correction note placing `verifier_mode.py`'s precedence docstring at `:39-40`;

`check_n5` (round33_defects.py:113-128) requires exactly:
1. `":35-38" in text` (token present anywhere);
2. `near(text, "verifier_mode.py", ":39-40", width=300)` — regex co-occurrence within 300 chars, either order;
3. `near(text, ":39-40", "correction", width=300)` **or** `near(text, ":39-40", "superseded", width=300)`.

No check verifies that the three tokens form a *correction note*, that the note is *labelled* as such,
that it is *appended* (append-only), or that it actually places the docstring at `:39-40`; condition 3
is satisfiable by a sentence that explicitly **denies** a correction.

## Method

Fresh `/tmp` sandbox `r33fn5-sentence.uLZ4qd/`; lanes `a`–`e` each carry
`corpus/lessons/round-31.md` (plus `SCORECARD.md` and a tracked `.ufo/waves/round-32/` for the full-CLI
end-to-end runs; `git init` scoped strictly inside the sandbox). Fixture bytes:

| fixture | lesson sha256 | content |
|---|---|---|
| `a` attack | `e06f8144…` | original stale Gate row `precedence docstring (:35-38)` **plus** unrelated decoy sentence (below) |
| `b` control | `ee6d5489…` | same original stale row, **no** decoy |
| `c` positive control | `16a9bb99…` | byte-for-byte copy of live `corpus/lessons/round-31.md` |
| `d` distance boundary | `f6f17cff…` | original + decoy tokens with `:39-40`↔`correction` gap > 300 chars |
| `e` polysemy variant | `08338ca0…` | original + "a spelling correction … verifier_mode.py … :39-40 window" (gap > 300 across sentences) |

Decoy sentence in fixture `a` (byte-exact, the entire ground of the attack):

> The auditor who greps for verifier_mode.py inside the :39-40 window files no correction against this
> lesson; the token here is a decoy only and no note here updates any locator.

Measured token distances in fixture `a`: `verifier_mode.py`↔`:39-40` = 253 chars;
`:39-40`↔`correction` = 82 chars; both within the 300-char window.

## Results (check_n5 exercised directly from the lane plan)

```
$ PYTHONDONTWRITEBYTECODE=1 python3 -B - <<'PY'   # imports plans/round33_defects.py verbatim
FIXTURE a: check_n5 -> ''   (green=True)
FIXTURE b: check_n5 -> "no appended correction updates verifier_mode.py's precedence locator to :39-40"   (green=False)
FIXTURE c: check_n5 -> ''   (green=True)
FIXTURE d: check_n5 -> 'the round-31 lesson correction note is not labelled'   (green=False)
FIXTURE e: check_n5 -> "no appended correction updates verifier_mode.py's precedence locator to :39-40"   (green=False)
```

- **Fixture `a` — FALSELY PASSES.** The lesson contains the stale `:35-38` and a sentence that
  *denies* any correction, yet `check_n5` returns `""` (green). The frozen claim's "labelled correction
  note placing verifier_mode.py's precedence docstring at :39-40" does not exist anywhere in the file.
- Fixture `b` proves the decoy sentence is the sole cause of the green: identical lesson minus the
  decoy goes red with the "no appended correction …" reason.
- Fixture `c` confirms the harness is wired correctly (real bytes still green — an honest positive).
- Fixture `d` shows the only structure the check enforces is ≤300-char token proximity: push
  `correction` beyond 300 chars and the same non-correction reddens with "not labelled".
- Fixture `e` (`correction` used for an unrelated spelling fix) also reddens only because its token
  gap exceeds 300 chars — token polysemy would pass if placed within the window.

## End-to-end CLI (official entrypoint)

```
$ python3 -B plans/round33_defects.py --lane /tmp/r33fn5-sentence.uLZ4qd/a
DEFECT N6 round30-lesson-errata: corpus/lessons/round-30.md is unreadable
checks=6 defects=1        # exit 1 — N5 NOT listed

$ python3 -B plans/round33_defects.py --lane /tmp/r33fn5-sentence.uLZ4qd/b
DEFECT N5 round31-lesson-locator: no appended correction updates verifier_mode.py's precedence locator to :39-40
DEFECT N6 round30-lesson-errata: corpus/lessons/round-30.md is unreadable
checks=6 defects=2        # exit 1 — N5 red only when the decoy is removed
```

Same lane layout, same original `:35-38` row, one unrelated sentence apart: N5 flips from red to
green. The counter therefore cannot distinguish a real labelled correction from a decoy/negation.

## Blocker check

The frozen claim's own acceptance ("carries a labelled correction note placing … at :39-40") fails on
fixture `a` semantically while the counter reports `defects=0` for N5. No lane/fleet file was edited,
committed, staged, or mutated: plan sha256 identical before/after; all fixtures and `git init`s live
under `/tmp/r33fn5-sentence.uLZ4qd/`; no tools installed (report per tooling directive).

## VERDICT: caught

N5 **falsely passes** a non-correction: `check_n5` greened a lesson whose only `:39-40`/`correction`
co-occurrence explicitly **denies** a correction and updates no locator. The counter enforces token
proximity (≤300 chars), not correction semantics, not a label, and not append-only — the frozen
"labelled correction note" predicate is not enforced. Confirmed limitation: the sole structural guard is
the 300-char `near` window (fixture `d` reddens only on distance); `correction`/`superseded` token
polysemy would green within the window (fixture `e`).
