# R29a2 — independent verification of the S077 located quote

Seat: `L1Kengaku29.R29a2RevQuoteS077` (leaf reviewer, no dispatch, no production edits).
Scope: verify the claimed S077 quote against the pinned source, fetched by this seat, not read
from any sibling's artifact. Access date **2026-10-25**. Read-only everywhere outside this file.

## Artifact under test

- URL: `https://raw.githubusercontent.com/harbor-framework/terminal-bench/e67a2cb7db4d9795c212909b3395d8c22ad60aec/docs/TASK_REVIEW_AUTOMATION.md`
- Fetch: `curl -sSL` → exit 0, `/tmp/r29a2-revquotes077/TASK_REVIEW_AUTOMATION.md` (this seat's own
  scratch; ephemeral by nature, and **not** part of any lane `.ufo/.../scratch/` tree. The durable
  anchor is the pinned URL plus the sha256 below — the file can be re-fetched byte-identically
  without me. No `.ufo/waves/round-29/scratch` artifact is cited by this report.)
- `sha256sum` = `b0a7cb1495a08a4429d957904dd724db08293627dfba040c2df7c09929278b61`
- Size: 41842 bytes, `wc -l` = 461 (462 split-lines; file ends with `\n`, last bytes per `od -c` are
  ``his rubric.\n``)
- Independent second fetch → same sha256 and `cmp` **IDENTICAL_REFETCH** (not a one-shot read)
- `git hash-object` = `68d84d6c6c2bd699f446cbcb7ebe7a9287962b17`
- Pin integrity: the pinned commit's bytes are **byte-identical to `main` head at fetch time**
  (`cmp` → `PIN_EQUALS_MAIN`, both `b0a7cb14…78b61`). The quote is current; no pin-vs-head drift
  exists to weaken the citation.

Claimed strings are taken from the authoritative L1-authored claim, not from paraphrase:
`plans/round-29-attempt2-claims.md` (frozen) names S077 as "Harbor task-review automation", and
`.ufo/waves/round-29/attempt2/build-spec.json` → `items[10].prompt` supplies the exact strings handed
to the draft seat: the full sentence
`'Prevents training data contamination by ensuring a unique canary string is present in task files.'`
plus rows `'Nop Validation' / 'Doing nothing fails tests'` and `'Cheat Trials' / 'Adversarial reward-hack detection'`.

Word counts are whitespace tokens (`wc -w` convention). For table rows both the raw row count and the
content-cell count excluding bare `|` tokens are given.

## Verdicts

| # | Claimed quote | Present | Line | Word count | Verdict |
|---|---|---|---|---|---|
| Q1 | `Prevents training data contamination by ensuring a unique canary string is present in task files.` | yes, literal, `str.count == 1`, `line.startswith(quote) == True` | **95** | **15** | **PASS** |
| Q2 | `\| [Nop Validation](#docker-build-oracle-nop) \| Doing nothing fails tests \| Auto on PR + every push / \`/validate\` \|` | yes, exact full-row equality (`L29 == row` → True), `count == 1` | **29** | **18** raw / **14** content tokens | **PASS** |
| Q3 | `\| [Cheat Trials](#cheat-trials) \| Adversarial reward-hack detection \| \`/cheat\` \|` | yes, exact full-row equality (`L31 == row` → True), `count == 1` | **31** | **10** raw / **6** content tokens | **PASS** |

All three are inside the lane's ≤25-word budget (`corpus/QUALITY.md:31-33`, Q3: "an anchored quote
(≤25 words, with location) … a paraphrase may narrow the quote, never widen it").

### Q1 — location and sentence boundary

Line 95 sits under `#### check-canary` (heading line 93) inside `### Static Checks` (heading line 89;
scope sentence at line 91: "Static checks that catch common mistakes with no API keys required.").
Line 95 is one sentence ending at `files.`; the bytes immediately after the quote are
`' Checks `instruction.md`, '` — a new sentence. The claimed text therefore cannot be a window that
spills past its source sentence. Q1's subject is the `check-canary` static check only (it names
instruction/task.toml/Dockerfile/solution/tests canary scanning), not task validity in general.

### Elision form in this ticket is not the claim, and is not literal

The ticket-level rendering `'Prevents training data contamination ... present in task files.'` occurs
**0 times** in the file (`str.count == 0`) — necessarily, since `...` is not in the source. Word-index
proof that the ellipsis is a pure intra-sentence elision:

```
sentence words:  [0 Prevents][1 training][2 data][3 contamination][4 by][5 ensuring][6 a]
                 [7 unique][8 canary][9 string][10 is][11 present][12 in][13 task][14 files.]
prefix match: True   suffix match: True
elided words: ['by','ensuring','a','unique','canary','string','is']  count 7
```

8 kept words + 7 elided = 15, exactly the source sentence, in the same sentence, with **zero words
beyond it**. No widening; the ellipsis form narrows.

## Landed entry — end use of S077 (entry appeared during this run)

`corpus/knowledge/benchmark-task-validity-checklist.md` is now present (there were 0 bytes of it at
first check; it landed while this seat was verifying). Its S077 use, checked after it landed:

- L1 anchor: `# Static Checks` → `#### check-canary` (line 95) and §Pipeline Overview rows
  `Nop Validation` (line 29) / `Cheat Trials` (line 31), commit `e67a2cb7…0aec`. The three line
  numbers **match this seat's independent line map exactly**, and the commit string is present.
- L32 (axis G evidence): the 15-word sentence is quoted **verbatim** (exact `"…"` substring match,
  `'...' not in` the line). No ellipsis, no widening. **PASS.**
- L28 (axis C) quotes `"Doing nothing fails tests"` verbatim; L31 (axis F) quotes
  `"Adversarial reward-hack detection"` verbatim. Both cells are literal. **PASS.**
- L43: "S077's pipeline runs the static checks (including the canary) automatically on every PR,
  while cheat trials are maintainer-triggered (`/cheat`)" — supported by source rows 25/31 and
  line 35. **PASS.**

## Findings (advisory, for the L1)

1. **Anchor heading level is wrong in the entry.** Entry L1 writes `` `# Static Checks` ``; the source
   heading is `### Static Checks` (line 89, `repr(src[88]) == '### Static Checks'`). An anchor is
   supposed to be reproducible by search; `# Static Checks` does not match the heading text. Fix to
   `### Static Checks`. Evidence: source line 89 vs entry line 1.
2. **"Axis F is periodic" (entry L43) converts on demand into a cadence.** The source says trials
   "are run on demand by maintainers with `/run` or `/cheat`" (line 35), "Cheat trials likewise
   require `/cheat` or a manual dispatch" (line 252), "Maintainers trigger adversarial cheat trials by
   commenting `/cheat`" (line 297). Nothing states a period. "on demand, not per-PR" would be exact.
3. **Axis F's "adjudicated" is supported by line 301, not by the cited row.** Entry L31 says
   "adversarial cheat trials are run and adjudicated" and cites `S077 "Adversarial reward-hack
   detection"`. Adjudication is established only at line 301: "The LLM-based analysis determines
   whether actual hacking occurred." Add line 301 to the evidence cell; the row alone does not carry
   the second half of the claim.
4. **Axis B's "the maintainer's own reference solution" (entry L27) is gloss beyond row 28.** Row 28
   reads `Solution passes all tests`; the oracle is named `solve.sh` at line 244. "maintainer's own"
   and "reference" are not in the cited cell — a narrowing gloss on the same property, so low risk,
   but it is the entry's own wording rather than the quote's.
5. **Do not ship the ellipsis form as a located quote** in any S077 artifact (SOURCES anchor, lesson
   Gate block). The full 15-word sentence fits the budget and is a literal substring; the ellipsis
   form is not (`count == 0`) and a literal-substring linter will report it absent.
6. **Cite the row, not the label.** Label-only anchors are not unique: `Nop Validation` occurs on
   lines 29 and 244; `Cheat Trials` on lines 31, 41, 295. The full-row forms are unique (`count == 1`),
   which is what the entry and this verification use — keep it that way.

## Residual risk / coverage gaps

- Q1/Q2/Q3 verified for presence, line, count, and non-widening only. No claim is made here about the
  other four sources (S078/S079/S080/S090); those belong to their own seats.
- Word counts are whitespace-token counts; a grader that splits `reward-hack` or counts `+`/`/`
  silently will differ by a few tokens on row counts, never across the 25-word ceiling.
- Entry L1 states the pin but links `blob/main`; today pin == main (proved above), so the URL is
  currently honest. If main moves, the link will silently point at different bytes while the commit
  string stays pinned — prefer the pinned `blob/e67a2cb…` URL.
- No tool installs or updates were performed in this seat; PACMAN guard untouched; nothing written
  under the lane except this report.

## Evidence commands

```
curl -sSL -o TASK_REVIEW_AUTOMATION.md <pinned raw URL>      # EXIT=0
sha256sum TASK_REVIEW_AUTOMATION.md                          # b0a7cb14…78b61
wc -l -c TASK_REVIEW_AUTOMATION.md                           # 461 41842
curl -sSL <pinned raw URL> -o refetch.md && cmp -s refetch.md TASK_REVIEW_AUTOMATION.md
                                                             # IDENTICAL_REFETCH
curl -sSL -o main.md <main raw URL> && cmp -s main.md TASK_REVIEW_AUTOMATION.md
                                                             # PIN_EQUALS_MAIN
git hash-object TASK_REVIEW_AUTOMATION.md                    # 68d84d6c…2b17
python3: str.count / line.startswith / full-row equality / word-index prefix+suffix proofs
```
