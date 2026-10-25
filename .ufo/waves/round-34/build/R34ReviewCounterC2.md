# R34ReviewCounterC2 — review of the C2 counter and mutation harness (2026-10-25)

Scope: `.ufo/waves/round-34/build/R34C2CounterDraft/round34_defects.py` (sha256 `d8af348c…7bab550`) and
`.ufo/waves/round-34/build/R34MutateDraft/round34_mutate.py` (sha256 `44156300…3bd1f2`), against the frozen
C2 predicate in `plans/round-34-claims.md` (freeze commit `adaf25df`). Method: actual execution of both tools
and of the naive baseline `plans/round33_defects.py`; no `lsp` device exists in this session (tool inventory
checked — only `ast_edit`/`debug` are mounted), so semantic checks are execution + byte inspection, with grep
as the recorded fallback. The mutate draft changed under me mid-review (first read contained
`def replace_once`; the hashed current bytes do not — see B6); findings are stated against the hashed bytes.

## Verified baseline (command → output)

```
$ python3 .ufo/waves/round-34/build/R34C2CounterDraft/round34_defects.py --lane <lane>
DEFECT N3 round31-report-append-only-erratum: <lane>/.ufo/reports/round-31/kengaku.md is unreadable
DEFECT N4 round32-report-closure-hash: <lane>/.ufo/reports/round-32/kengaku.md is unreadable
DEFECT N7 round33-lesson-ledger-correction: round-33 lesson has no dated correction stating ledger sum 36+53=89
checks=8 defects=3        EXIT=1

$ python3 .ufo/waves/round-34/build/R34MutateDraft/round34_mutate.py
CLEAN exit=1 … (same 3 DEFECT lines) … checks=8 defects=3        EXIT=1   (dies at the clean gate)

$ python3 .ufo/waves/round-34/build/R34MutateDraft/round34_mutate.py --selftest
SELFTEST green failed (1) … checks=8 defects=3                    EXIT=1

$ python3 .ufo/waves/round-34/build/R34C2CounterDraft/round34_defects.py --selftest
SELFTEST cases=10 failed=0                                        EXIT=0   (fixture-only green)

$ python3 plans/round33_defects.py --lane <lane>                  (naive baseline)
checks=6 defects=0                                                EXIT=0
```

Tracking: `git -C <lane> ls-files .ufo/waves/round-34/falsify/red-before .ufo/reports` → only
`.ufo/reports/round-17/kengaku.md`; the four red-before receipts are **untracked**. The round-31/32 kengaku
reports exist only at **fleet root** (`git -C /home/vgpnk/Projects/shokunin ls-files` → both listed), which is
where `plans/round33_defects.py:11-12` reads them and where the round-33 spotcheck §2 (N3/N4 rows) re-derived them.

## Blockers — the frozen predicate is unreachable as drafted

- **B1. Counter is red on the landed tree (`checks=8 defects=3`, exit 1 vs frozen `defects=0` exit 0).**
  Three independent root causes: (i) `R31_REPORT`/`R32_REPORT` are lane-relative (defects draft :12-13) but the
  reports live at fleet root — the naive counter's `FLEET` anchoring is correct and this draft dropped it;
  (ii) N7's regex (:121) demands `36\s*\+\s*53\s*=\s*89` or `36 build.*53 falsify.*89`, while the landed
  round-33 lesson says "Wave-1 build: 36 seats; wave-2 falsify: 53 seats; total **89**." (word order `build: 36`
  never matches `36 build`); (iii) N7's dated-correction regex (:124) — no line in `corpus/lessons/round-33.md`
  pairs `correction|erratum` with an ISO date. The counter must key on the landed phrasing, not an imagined one.
- **B2. The harness can never go green in its own sandbox.** `archive_tree` (mutate draft :35-47) builds the
  sandbox from `git archive` of the **lane** repo, which structurally cannot contain the fleet-root reports
  N3/N4 read — so the CLEAN gate (:131-133) fails in every run regardless of B1(i)'s fix direction, and
  `MUTANTS total=8 detected=8` is unreachable. Fix shape: either the harness seeds the sandbox with the two
  report bytes, or the counter gains a report-root override (the naive counter already parameterizes
  `check_n3`/`check_n4` with report paths and injects fixtures in its selftest — reuse that precedent).
- **B3. M4's expected check id is wrong.** Mutate :68-76 empties the SCORECARD Round-32 body — only N2 can see
  that; `check_n7` (defects :111-128) reads `corpus/lessons/round-33.md` and the round-33 swarm ledger and never
  touches SCORECARD. The harness expects `N7` (:141, `7 if number == 4`) → guaranteed `UNDETECTED M4 expected=N7`
  even after B1/B2 are fixed. Consequence: the heading-only class has no working N7-side mutant; N7 has no
  heading-only surface at all despite the claims mapping "heading-only → N2/N7".
- **B4. M7/M8 mutate files no check reads.** M7 (:83-89) prepends a padded token line to
  `.ufo/waves/round-31/falsify/*.md`; M8 (:90-96) appends a narrative `112091c` line to
  `.ufo/waves/round-32/falsify/*.md`. N1 tracks only `.ufo/waves/round-{32,33}` (defects :14, :40-52) and no
  check reads falsify content; a content edit to a tracked file stays N1-green. Both mutants are undetectable by
  construction, so the expected labels N3/N4 (:141) can never appear. Additionally M7 **prepends**, but new N3
  keys on `lines[max(positions)+1:]` (defects :74-76) — the last pre-existing `a44b5a8` occurrence still precedes
  the real erratum, so even retargeting at the report leaves N3 green; the padded line must be **appended**.
  The `x*350` constant is clearly tuned against the naive `near(..., width=300)` (`plans/round33_defects.py`) —
  right idea, wrong file, wrong end, wrong arity of change.
- **B5. M5/M6's target literals do not exist.** M5 (:79) needs the exact span
  `` `verifier_mode.py ... :35-38` `` in `corpus/lessons/round-31.md`; the only `verifier_mode.py ...` span is
  `:39-40` (:198), and `:35-38` occurs only inside separate spans (:57 `(`:35-38`)`, :197, :199). M6 (:82) needs
  `:78–81` (en-dash) in **round-31.md**; no `:78-81` in either dash form exists there — the token lives in
  `corpus/lessons/round-30.md`:197,:214 as ASCII hyphens. Dead mutant either way (crash or silent no-op).
- **B6. Current bytes call an undefined function.** The hashed mutate draft has `replace_once(...)` call sites
  (:79, :82) but no `def replace_once` anywhere (grep over the whole file: zero hits; `:44-52` shows
  `archive_tree`'s commit tail directly followed by `def mutate`). M5 raises `NameError` before any literal
  check could even matter. (The first read minutes earlier still had the definition — the owner seat's edit is
  incomplete or regressing; either way the current bytes cannot run past M5.)

## Majors

- **J1. N4 is not hardened — the token-co-occurrence class is half-unimplemented.** New `check_n4`
  (defects :81-85) is byte-for-byte the naive presence test (`"112091c" not in text`); the draft contains no
  `near()` at all, while the frozen claim's class text says "the `near()` co-occurrence check must not pass when
  the tokens exist in the file but not in the required relation". N3 implements the class only as append-ordering.
  As drafted, no mutant can be naive-undetected yet N4-red; M8's stated intent ("outside the required section")
  is untestable against these bytes. The claims/code divergence must be resolved before landing.
- **J2. Two of the four red-before receipts are defective as evidence.** `width-newline.txt` self-admits "The
  requested sandbox export and post-mutation probes were not run in this seat" and records
  `grep -n ':35-38' corpus/lessons/round-31.md → exit=1 (no match)` — contradicted by the landed bytes (token
  present at :57/:197/:199; my grep output on file). `token-cooc.txt` records output `found` / `distance 638`;
  re-running its own embedded command verbatim prints `not found` / `distance 703` — a 300-char window cannot
  bridge 638+, so the recorded output cannot be produced by the recorded command. `index-head.txt` is honest but
  scopes itself to "independent-success checks, not equal-count detection", i.e. it does not exercise the new
  N8's comparison either; only `heading-only.txt` demonstrates what it claims. Per the frozen kill rule ("a
  partial receipt … is not closure"), C2's red-before evidence is currently incomplete for two classes.
- **J3. The red-before receipts are uncommitted.** `git ls-files` lists nothing under
  `.ufo/waves/round-34/falsify/red-before/`; the frozen predicate requires them "committed under" that path.
  This is the exact untracked-wave-tree failure round-33 routed as N1 (89 files at a pushed tip).

## Minors

- **m1. Counter selftest is fixture-tailored and under-red.** 10 cases = 8 green + only 2 red (N2, N8); N1 and
  N3–N7 have no red controls. It prints 10/10 PASS while the real lane is defects=3 — the "vacuous green" /
  "survivor" class round-30/31 already recorded (N7's fixture literally writes the regex's imagined phrasing
  `"Correction (2026-10-25): 36 + 53 = 89"`, which is why the fixture passes and the lane fails).
- **m2. "Undetected by naive" is unattainable for M5-style stale-token wraps.** Naive N5 requires verbatim
  `:35-38` retention, so any wrap reds naive too — those mutants are regression tests, not hardening demos. The
  one genuinely naive-green width variant exists in round-30.md: naive N6 accepts `78–81` as an alternative
  spelling (`":78-81" not in text and "78–81" not in text`), while new `anchored()` is ASCII-contiguous only.
- **m3. Harness assertion is a whole-stream substring test.** `check in result.stdout` (:142) cross-accepts if
  the expected id appears in any unrelated DEFECT line; anchor per line (e.g. `^DEFECT N7\b`, MULTILINE). The
  nested-conditional id map (:141) is where B3 was born — replace with an explicit `{mutant: (class, check)}` table.
- **m4. Dead/duplicated logic in the counter.** `check_n7` :126 re-runs the identical regex as :121 (unreachable
  second failure mode); `anchored()`'s docstring (:33) claims "permitting whitespace around punctuation" that
  the implementation does not do (nums are contiguous) — the strictness is desirable, the doc is wrong.
- **m5. `archive_tree` pins LANE `HEAD`** (mutate :36-37): the harness measures the committed tree, which matches
  the frozen "landed tree" wording but means any not-yet-committed state (today's receipts) is invisible; the
  run receipt should note the tip it archived.
- **m6. `COUNTER_CANDIDATES` prefers the sibling draft** (:17-20): correct for development, and it resolves to
  `plans/round34_defects.py` post-landing because `DRAFT.parent` changes — no action, recorded so nobody
  "fixes" it into a loop.

## Per-mutant audit (the eight)

| mutant | change | class | naive (round33_defects) | new detector | harness expects | verdict |
|---|---|---|---|---|---|---|
| M1 | delete a knowledge file | index-vs-HEAD | green (no such check) | N8 `missing_files` | N8 | **valid** |
| M2 | add unindexed fixture file | index-vs-HEAD | green | N8 `missing_rows` | N8 | **valid** |
| M3 | insert empty `## Round 33` before Round 32 | heading-only | green (heading-presence-only) | N2 (<2 content lines) | N2 | **valid** |
| M4 | empty SCORECARD Round-32 body | heading-only | green | N2 (not N7) | N7 | **broken mapping (B3)** |
| M5 | wrap `` `verifier_mode.py ... :35-38` `` | width/newline | would also be red (verbatim retention) | N5 | N5 | **broken: literal absent (B5), NameError (B6), not naive-undetected (m2)** |
| M6 | `:78– 81` spacing in round-31.md | width/newline | n/a | N6 | N6 | **broken: token not in that file (B5), NameError (B6)** |
| M7 | prepend padded `a44b5a8…ae95fe0` to round-31/falsify md | token-co-occurrence | n/a | none reads it | N3 | **broken: unread target + prepend inert under `max(positions)` (B4)** |
| M8 | append narrative `112091c` to round-32/falsify md | token-co-occurrence | n/a | none reads it | N4 | **broken: unread target; N4 presence-only could not redden anyway (B4+J1)** |

Net: 3 of 8 mutants are sound. Clean-mirror gate, red-gate shape (exit 1 + `DEFECT` + check id, :131-133,
:142), and the counter's CLI contract (`checks=8 defects=N`, `DEFECT <id> <label>: reason`, exception→DEFECT
wrapping in `main`) all match the frozen predicate's wording — keep those.

## Proposed additional mutants (one per class — reported, not implemented)

1. **index-vs-HEAD (duplicate row):** append a second `` | `knowledge/<existing>.md` | … `` row to
   `corpus/README.md` → exercises N8's `duplicate` branch, untouched by M1/M2 (defects `check_n8`).
2. **heading-only (N7-real):** replace the round-33 swarm ledger's `members` array with `[]` (or truncate the
   `## Seat ledger` table) → `seat ledger has 0 falsify members, expected 53`; naive has no N7, so this is
   genuinely naive-green/new-red — the mutant M4 pretends to be.
3. **width/newline (dash-width swap):** in `corpus/lessons/round-30.md`:197 change
   `contamination-transparency-card.md:78-81` → `…:78–81` (hyphen→en-dash): naive N6 green (accepts `78–81`),
   new N6 red (`anchored()` is ASCII-contiguous). The discriminating variant the class needs.
4. **token-co-occurrence (ordering violation):** append `a44b5a8 + 'x'*350 + ae95fe0` as the **last line** of
   the round-31 report: naive N3 green (original erratum still satisfies presence + `near` + `ae95fe0`), new N3
   red (no erratum word after the *last* `a44b5a8` line). An N4-side analog (unrelated `112091c` in a narrative
   line) becomes possible only after J1 hardens N4 beyond presence.

## Residual risk and verification gaps

- M1–M8 were not executed individually (the harness dies at the CLEAN gate); per-mutant conclusions for M4–M8
  are static (byte inspection + the checks' read sets). B5's failure mode is "ValueError-or-silent-no-op" in the
  first snapshot and "NameError" in the hashed snapshot — either way the mutants are dead; I did not run M5 in
  isolation to pick the exact exception.
- M3's first-match behavior against the real SCORECARD ordering is inferred from the heading-only receipt
  (Round 33 at :1123, appended empty heading at :1156 → ascending rounds) and not independently re-read.
- The ledger's 53 members is taken from the round-33 lesson/claims; N7's count branch never executed on the real
  lane (the :121 regex returns first), so `count != 53` is unverified against the live JSON.
- Drafts are owned by live sibling seats and changed once mid-review; findings are pinned to the hashed bytes
  above and the counter-draft anchors were re-verified against the current snapshot.
- Not in my scope (other seats): C1 files, quarantine rows, census, scorecard axes.

VERDICT: review-c2-counter (15 gaps found)
