# R33FN5Newline — falsify report (round 33, hyaku run 7)

Seat: `KengakuR33.R33FN5Newline` (mutation-tester, leaf; no subagents; no tool installs).
Item: **N5 multiline correction robustness** — "express the genuine locator correction across a
natural line break, retaining original `:35-38`; test whether `check_n5` accepts the wrapped correction."

## Grounding

- Target artifact: `corpus/lessons/round-31.md` (sha256 `16a9bb99463912aad3d24b568a739c9f826be4ece173cfa803dbdc899326cee8`, 20771 bytes, unmutated — re-hashed after all probes).
- Frozen claim (C2/N5, `plans/round-33-claims.md`): *"`corpus/lessons/round-31.md` still contains `:35-38` and carries a labelled correction note placing `verifier_mode.py`'s precedence docstring at `:39-40`."*
- Code under test: `plans/round33_defects.py::check_n5` (reads `lane/corpus/lessons/round-31.md` only; `main --lane` dispatches identically).

```
def check_n5(lane):
    text = read(lane / LESSON31)
    if ":35-38" not in text: return "… stale :35-38 locator is gone …"
    if not near(text, "verifier_mode.py", ":39-40", width=300): return "no appended correction updates … to :39-40"
    if not near(text, ":39-40", "correction", width=300) and not near(text, ":39-40", "superseded", width=300):
        return "the round-31 lesson correction note is not labelled"
    return ""

def near(text, a, b, width=300, flags=re.I):
    return bool(re.search(re.escape(a) + r".{0," + str(width) + r"}" + re.escape(b), text, flags)
            or re.search(re.escape(b) + r".{0," + str(width) + r"}" + re.escape(a), text, flags))
```

## Method

All fixtures built under `/tmp/r33fn5-od2a5mig/` (fresh sandbox, git-free; no lane/fleet mutation —
lane report file sha256 verified unchanged after all runs). Each fixture = full copy of `round-31.md`
with only the appended correction block replaced; `:35-38` retained at the original line 57 in every
fixture. Probe driver: `importlib` load of `plans/round33_defects.py`, direct `check_n5(lane)` /
`near(...)` calls.

## Results

### Primary attack — correction wrapped across a natural line break

| Fixture | Mutation (only the correction block) | `:35-38` kept | `:39-40` literal present | `check_n5` result |
|---|---|---|---|---|
| F0-control | verbatim lane copy | yes | yes | `""` (PASS) |
| F1-wrap-plain | single occurrence `:39-` + newline + `40`, same words/evidence | yes | no | `"no appended correction updates verifier_mode.py's precedence locator to :39-40"` (REJECT) |
| F2-wrap-codespan | ` :39-` + newline + `40` inside a backtick span | yes | no | same REJECT message |
| F4-wrap-plus-copy | one wrapped occurrence + a second intact `:39-40` on the same line later | yes | yes | `""` (PASS — passes only via the surviving same-line copy) |

**Verdict for the named item: REJECTED.** `check_n5` refuses a genuine correction expressed across a
natural line break: with the locator token split by a hard wrap (`:39-` / `40`), the literal `:39-40`
substring is absent and the check fails — despite the note containing the same facts, same
`ae95fe0` evidence, and the label words. The original artifact passes only because line 198 of
`round-31.md` happens to hold `verifier_mode.py`, `:39-40` (twice) and `correction` on one physical line.

### Root cause probes — `near()` is line-bounded AND width-bounded

Direct `near()` calls (direction symmetric in both orders):

| Probe text | `near(width=300)` | `near(width=1e6)` |
|---|---|---|
| `verifier_mode.py :39-40 correction` (same line) | **True** | True |
| `verifier_mode.py\n:39-40 correction` (adjacent lines, intact tokens) | **False** | **False** |
| `verifier_mode.py\r\n:39-40 correction` | False | False |
| `verifier_mode.py\n\n:39-40 correction` | False | False |
| `verifier_mode.py :39-\n40 correction` (token split) | False | False |
| `:39-40` + 301 × `x` + `correction` (one line) | False | True (width=302 → True) |

Regex `.` does not match `\n` (no `re.S`), so ANY newline between the two strings breaks the
proximity test regardless of width — even with both tokens fully intact and directly adjacent across
the break. Width 300 adds a second, independent binding constraint (301 unused chars on one line also
fails).

### Label-clause isolation

| Fixture | first clause `near(verifier_mode.py, :39-40)` | label clause `near(:39-40, correction\|superseded)` | `check_n5` result |
|---|---|---|---|
| F7c-label-wrapped-only (tokens intact on one line; `correction`/`superseded` only on next line) | True | **False / False** | `"the round-31 lesson correction note is not labelled"` |

### Secondary observation (false positive direction)

| Fixture | content | `check_n5` result |
|---|---|---|
| F9-denial | "`:35-38` … there is **no correction** here. `:39-40` in verifier_mode.py is wrong and this note **supersedes nothing**; nothing was repaired." | `""` (**PASS**) |

The predicate is a bag-of-substrings: a note that *denies* the correction satisfies it because the
words `correction`/`supersedes` and the token `:39-40` co-occur (coincidentally on one line). The
check verifies string co-location, never that the correction states the claimed placement.

## Verdict

- **Primarily: limitation / false-negative.** `check_n5` is not robust to line wrapping in either of
  the two ways a genuine correction can wrap: the token split across a line (`F1`/`F2`) or the
  co-located label/tokens separated by a line break (`F3`/`F7c`). The frozen predicate's phrase
  "placing … at `:39-40`" is enforced as exact byte co-location on a single physical line. A
  faithful, evidence-identical correction expressed across a natural line break is rejected →
  the claimed closure would report an open defect for a genuinely repaired artifact.
- `near()`'s missing `re.S` is the root cause; the 300-char width is an independent secondary bound.
- Secondary: the bag-of-substrings predicate accepts a denial note (`F9`), so the check is also
  over-permissive in the opposite direction (not the named item, recorded as an observation).

## Evidence (exact outputs)

```
$ python3 - <<'EOF'   # probe driver (importlib load of plans/round33_defects.py)
F0-control           :35-38=True :39-40=True  ret=''
F1-wrap-plain        :35-38=True :39-40=False ret="no appended correction updates verifier_mode.py's precedence locator to :39-40"
F2-wrap-codespan     :35-38=True :39-40=False ret="no appended correction updates verifier_mode.py's precedence locator to :39-40"
F3-wrap-elsewhere    :35-38=True :39-40=True  ret="no appended correction updates verifier_mode.py's precedence locator to :39-40"
F4-wrap-plus-copy    :35-38=True :39-40=True  ret=''
F5-label-wrapped     :35-38=True :39-40=True  ret="no appended correction updates verifier_mode.py's precedence locator to :39-40"
F6-all-split         :35-38=True :39-40=True  ret="no appended correction updates verifier_mode.py's precedence locator to :39-40"
F7c-label-wrapped-only :35-38=True :39-40=True ret="the round-31 lesson correction note is not labelled"
F8-label-301-same-line:35-38=True :39-40=True ret="no appended correction updates verifier_mode.py's precedence locator to :39-40"
F9-denial            :35-38=True :39-40=True  ret=''
same-line-adjacent near(width=300)=True  near(width=1e6)=True
newline-adjacent   near(width=300)=False near(width=1e6)=False
width 300, 301 pad: False
width 302, 301 pad: True
lane lesson sha256: 16a9bb99463912aad3d24b568a739c9f826be4ece173cfa803dbdc899326cee8 unchanged: True
EOF
```

## Scope / hygiene

- Leaf seat; no subagents, no background jobs, no tool installs, no git commands anywhere (fixtures
  are plain files under `/tmp`).
- Only writes: the report file. Lane, fleet, index, and sibling repos untouched (verified by
  re-hash of the target lesson file).
