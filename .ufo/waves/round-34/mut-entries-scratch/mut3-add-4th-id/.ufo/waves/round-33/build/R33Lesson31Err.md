# R33Lesson31Err — N5: round-31 lesson locator erratum (draft)

Role: leaf scribe/executor seat, C2 item N5. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Access date for every byte quoted below: **2026-10-25**. Lane HEAD at read time:
`78955888542258ba369f5aa72c200c913b4c3c90` (`7895588`). No production edit was made by this seat.

## 1. What the committed bytes actually say

| location | committed bytes (verbatim) | how obtained |
|---|---|---|
| `corpus/knowledge/benchmark-verifier-execution-model.md:31` | `resolver, never about the field alone. For multi-step tasks the precedence is spelled out at` | `grep -n "spelled out at"` on the working file (clean vs HEAD) |
| `corpus/knowledge/benchmark-verifier-execution-model.md:32` | `` `verifier_mode.py:39-40`: explicit step mode, then step environment, then the task-level resolution, then `` | same |
| `corpus/lessons/round-31.md:57` (Gate row, S092) | `` | S092 | …/src/harbor/models/task/verifier_mode.py | "or VerifierEnvironmentMode.SHARED" (2, `:31`); precedence docstring (`:35-38`) | 5 142 B, sha256 `e5893be9…8a6f2d` | `` | `git show HEAD:corpus/lessons/round-31.md` |
| `corpus/lessons/round-31.md:194` | `## Corrections (round 33, appended — the filed bytes above stand as written)` | `git show HEAD:corpus/lessons/round-31.md` (file is 200 lines at HEAD) |
| `ae95fe0` diff, entry file | `-`verifier_mode.py:35-38`: explicit step mode, then step environment, then the task-level resolution, then` / `+`verifier_mode.py:39-40`: explicit step mode, then step environment, then the task-level resolution, then` | `git show ae95fe0 -- corpus/knowledge/benchmark-verifier-execution-model.md \| grep '^[-+].*\(35-38\|39-40\)'` |

So both halves of the assignment's premise are confirmed in committed bytes: the **entry** cites the
precedence docstring at `:39-40` (post-`ae95fe0`), and the **lesson Gate row at `:57`** still says `:35-38`
— the stale line survives, which is what append-only requires.

**Prior state, disclosed:** the repair is *already committed* at `7895588` ("round-33: C2 routed-defect
repairs (N2 scorecard section, N5/N6 lesson errata), Q22, defects-after receipt", 9 lines added to
`corpus/lessons/round-31.md`). This seat did not author it. The committed section is at `:194` and its
bullet at `:196-200`; its locator sentence reads:

```
- **verifier_mode.py precedence locator (routed defect N5).** The Gate row at `:57` cites the
  precedence docstring at `:35-38`; after the entry's locator repair (`ae95fe0`) the verifier_mode.py
  precedence docstring is at `:39-40` (verifier_mode.py ... :39-40, this correction) — this
  correction supersedes the `:35-38` citation while the
  stale line is kept verbatim per append-only. Evidence: `git show ae95fe0 --stat`.
```

That bullet satisfies N5 but its parenthetical `(verifier_mode.py ... :39-40, this correction)` is
window filler, not prose; the block below is the canonical wording the assignment names.

## 2. Verbatim append block (exact bytes, for the END of `corpus/lessons/round-31.md`)

Append after line 200, preceded by one blank line. The note is deliberately **one physical line**: the
counter's `near()` uses `.{0,300}` without `re.DOTALL`, so the three tokens must co-occur on a single line.

```markdown

## Corrections (round 33)

Correction (round 33, appended): the Gate row at :57 cites verifier_mode.py's precedence docstring at :35-38; the entry's repair (ae95fe0) placed it at :39-40 — the :35-38 citation is superseded, not rewritten.

Evidence: `git show ae95fe0 -- corpus/knowledge/benchmark-verifier-execution-model.md` moves the entry's locator from `verifier_mode.py:35-38` to `verifier_mode.py:39-40`; at lane tip `7895588` the entry reads at `corpus/knowledge/benchmark-verifier-execution-model.md:32` "`verifier_mode.py:39-40`: explicit step mode, then step environment, then the task-level resolution, then" (12 words, byte substring of that line, re-read 2026-10-25), while `corpus/lessons/round-31.md:57` keeps the stale Gate row verbatim.
```

## 3. Gates (what was actually run, and what it printed)

| command | output | exit |
|---|---|---|
| `python3 plans/round33_defects.py --lane .` (live lane, working tree at HEAD for both files) | `checks=6 defects=0` | 0 |
| `check_n5` on `/tmp/r33-R33Lesson31Err` = `git show HEAD:corpus/lessons/round-31.md` **+** the block above | `reason=''` | green |
| `check_n5` control on `git show HEAD~1:corpus/lessons/round-31.md` (pre-`7895588`, no correction) | `reason="no appended correction updates verifier_mode.py's precedence locator to :39-40"` | red |
| `check_n5` on `git show 112091c:corpus/lessons/round-31.md` **+** only the block above (no `7895588` section) | `reason=''` | green — the block is self-sufficient |

Window measurements of the note line, computed on the exact bytes (`len(line)=210`):
`index("correction")=0`, `index("verifier_mode.py")=59`, `index(":39-40")=152` →
`correction→:39-40 = 152` chars, `verifier_mode.py→:39-40 = 93` chars, both inside the 300-char window.
The block is a byte substring check that also passed: `"`verifier_mode.py:39-40`: explicit step mode, then
step environment, then the task-level resolution, then" in entry` → `True`; the quoted Gate row → `True`.

## 4. Calibration findings

1. **N5's repair predates this seat.** `7895588` already greens N5 and the full counter. The C2 predicate
   (`checks=6 defects=0`, exit 0) is therefore *already* satisfied at HEAD; this seat's draft is redundant
   unless the L1 wants the assignment's exact wording.
2. **The requested heading would be a second H2 for the same round.** HEAD contains
   `## Corrections (round 33, appended — the filed bytes above stand as written)` at `:194`; the exact
   string `\n## Corrections (round 33)\n` is **absent**. Appending the block verbatim yields two
   same-round corrections headings. Recommended landing (append-only, no duplicate H2, no rewrite of
   filed correction bytes): append the block's **note + evidence lines as a second bullet under the
   existing `:194` heading**, omitting the duplicate `## Corrections (round 33)` line. Verified equivalent
   for the counter: `near()` is file-wide, so heading placement does not affect N5.
3. **Order sensitivity of the label test.** `check_n5` accepts `near(":39-40","correction")` *or*
   `near(":39-40","superseded")`, both ordered `a→b`. A note whose only `correction` token precedes
   `:39-40` (as the required sentence's leading label does) does **not** satisfy the first branch; the
   note greens through `superseded` ("… citation is superseded, not rewritten."). This is why the
   required sentence carries both words — do not trim `superseded`.
4. **Single-line requirement is unwritten.** `near()` has no `re.DOTALL`; a prettily wrapped note
   (70–80 col) reddens N5 even though the words are all present. The block keeps the sentence at 210
   chars on one line on purpose; any reformatting must preserve that.
5. **Stale line intact.** `:35-38` remains at `:57` (Gate row) and the file grew only by append
   (200 lines at HEAD, section at `:194`), so append-only holds for the filed Gate bytes.

## 5. Out of scope / not done

- No edit to `corpus/lessons/round-31.md` or any other lane file (leaf bound; the repair already exists
  in `7895588`). Nothing written outside this report and `/tmp/r33-R33Lesson31Err/` (64 KB).
- N6, N1–N4 not re-verified here (other seats' items); only the aggregate counter line is reported.
- No fleet-repo write, no `.ufo/state`, no git mutation (read-only `show`/`log`/`diff` only). No pacman;
  no tool installed this seat.

## 6. Artifacts

- This report: `.ufo/waves/round-33/build/R33Lesson31Err.md`
- Scratch (not committable, /tmp): `/tmp/r33-R33Lesson31Err/{corpus/lessons/round-31.md, pre/, self/}`

VERDICT: lesson31-errata-drafted
