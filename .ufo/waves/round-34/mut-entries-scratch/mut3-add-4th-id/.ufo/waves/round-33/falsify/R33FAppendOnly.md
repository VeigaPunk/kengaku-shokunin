# R33FAppendOnly — C2 N3–N6: do the checks prove append-only bytes, or mere token presence?

Seat: `KengakuR33.R33FAppendOnly` (leaf; no subagents). Round 33, hyaku run 7, 2026-10-25.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Target: `plans/round33_defects.py`
checks N3–N6 vs the frozen C2 predicate (`plans/round-33-claims.md` §C2).

Method: read-only inspection of the checker and the four target files; read-only git history
queries (fleet repo `/home/vgpnk/Projects/shokunin`, lane repo); a `/tmp/r33-appendonly/`
sandbox harness (fixtures + git scoped to `/tmp`) exercising the **real unmodified check
functions** via `importlib`. No tool installs. No lane/fleet file mutated — this report is the
only lane-tree write.

## Verdict

**The checks prove token presence/co-occurrence in the current file — they do not prove
append-only bytes.** `check_n3`–`check_n6` read only the live file text; none compares against
the pre-repair blob or git history, none verifies ordering or that new text follows the original
body, and `near()` is bidirectional and newline-blind. The frozen predicate's append-only
clauses ("the original token stays", "append-only addendum", "the stale text stays") are only
partially enforced — as stale-*token-substring* survival, not as byte preservation. A rewritten,
reordered, or prepended file passes all four checks. The actual round-33 repairs *are* genuine
appends (verified below), so this is a **limitation/false-negative-class** finding about the
instrument, not evidence that the current repairs are dishonest.

## 1. What the checks actually do (code-observed)

- `check_n3` (lines 100–111): requires `"a44b5a8" in text`, plus `near(text,"a44b5a8","superseded")`
  OR `near(text,"a44b5a8","erratum")` (width 300 default), plus `"ae95fe0" in text` (file-wide).
- `check_n4` (114–120): requires `"112091c" in text` — nothing else. The original tip
  `bcd2a6c` is not required to survive; no addendum framing is required.
- `check_n5` (123–136): requires `":35-38"` present, `near(verifier_mode.py, :39-40)`,
  `near(:39-40, correction|superseded)`.
- `check_n6` (139–163): requires `:78-81`/`78–81` present, `:72` and `82-83` present,
  `near(:72, 82-83)`, `near(:72, corrected|superseded)`, `"peer-reviewed"` present,
  `near(S086, without peer review|not peer-reviewed)`, `near(S086, erratum|correction)`.
- `near()` (60–65): `re.search(re.escape(a)+".{0,W}"+re.escape(b), text, re.I)` in both orders.
  Consequences: (a) **newline-blind** — `.{0,W}` never crosses `\n`; (b) **bidirectional** — a
  note placed *before* the original text binds as well as one appended after; (c) any occurrence
  pair within a window qualifies, regardless of section/meaning.
- None of N3–N6 calls `git` or any baseline blob; the freeze control (`defects-before.txt`) is
  not part of the counter.

## 2. Frozen predicate vs counter: concrete divergences

| item | predicate wording | code | effect |
|---|---|---|---|
| N3 | `a44b5a8` within **400 chars** of `superseded`/`erratum` | `near()` width **300** | compliant 301–400-char erratum reddens (false negative) |
| N3 | erratum "naming the real locator-fix commit `ae95fe0`" | `ae95fe0` anywhere in file (E3) | unrelated footer mention satisfies the check |
| N3–N6 | "append-only; the original token stays" / "append-only addendum" / "stale text stays" | token presence only; no ordering/byte preservation | full rewrite, in-place edit, or prepend passes |

## 3. Observed evidence

### 3a. Live counter and selftest

```
$ python3 plans/round33_defects.py --lane .          # lane, read-only
checks=6 defects=0        EXIT=0
$ python3 plans/round33_defects.py --selftest
SELFTEST checks=14 failed=0        EXIT=0
```
The selftest is weak on this axis: its N3–N6 red cases are all *file-absent* cases on an empty
dir; no case presents an existing file with wrong content (same shape as `R33CounterAttack`
M1/M1b).

### 3b. What makes the live checks bind (exact strings)

- N3 green binds via the word `Erratum` in the *title* of the appended addendum on the same line
  as `a44b5a8` (line 242 of `.ufo/reports/round-31/kengaku.md`: `The "Erratum addendum
  (trend-verdict seat)" above names lane tip a44b5a8 …`). The actual superseding sentence
  (`This citation is superseded, not rewritten.`, line 246) is 1 828 characters of linear text
  away from the first `a44b5a8` and on a different line — invisible to `near()`. The check never
  verifies that the token is actually declared superseded.
- N4 binds on the bare substring `112091c` at report line 68.
- N5 binds on lesson line 198 (`…verifier_mode.py … :39-40, this correction`), N6 on lesson
  lines 214/216 — each a single line containing all required tokens.

### 3c. Mutant run (real functions, `/tmp/r33-appendonly/` fixtures)

| fixture | semantics | result |
|---|---|---|
| `n3/base.md` (pre-repair bytes) | control | red: `no appended erratum supersedes the a44b5a8 citation` |
| `n3/g3a-rewrite.md` | **whole report rewritten**; only token sentence survives | **GAMED — green** |
| `n3/g3b-prepend.md` | erratum **prepended before** the body | **GAMED — green** |
| `n3/g3c-inplace.md` | original citing line **edited in place** | **GAMED — green** |
| `n3/g3e-footer.md` | erratum sentence present; `ae95fe0` in unrelated footer ~10 000 chars away | **GAMED — green** |
| `n3/f3a-width350.md` | same-line `a44b5a8`→`superseded` gap **350** (predicate: ≤400) | red — **false negative** (code width 300) |
| `n3/f3b-newline.md` | `a44b5a8` / `superseded` on adjacent lines | red — **false negative** (newline-blind) |
| `n4/base.md` | pre-repair bytes | red: `does not name … 112091c` |
| `n4/g4a-replace.md` | old tip `bcd2a6c` **replaced in place** by `112091c` | **GAMED — green** |
| `n4/g4b-bare.md` | file containing only `112091c` | **GAMED — green** |
| `n4/g4c-unrelated.md` | unrelated appendix mention (`worker nodes 112091c, 0fa3`) | **GAMED — green** |
| `n5/base.md` | pre-repair bytes | red: `no appended correction updates … to :39-40` |
| `n5/g5a-inplace-v2.md` | original Gate row **edited in place** (all tokens one line) | **GAMED — green** |
| `n5/g5b-append-sentence.md` | one appended style sentence, no docstring repair | **GAMED — green** |
| `n5/g5c-prepend.md` | note **prepended** | **GAMED — green** |
| `n6/base.md` | pre-repair bytes | red: `no appended correction updates … to :72 / :82-83` |
| `n6/g6a-inplace.md` | errata sentence **rewritten in place** (all tokens one line) | **GAMED — green** |
| `n6/g6b-append-sentence.md` | one appended sentence satisfies all six N6 bindings | **GAMED — green** |

### 3d. End-to-end fabricated lane (zero semantic repair)

Built in `/tmp/r33-appendonly/fakelane/`: committed wave file (N1), bare `## Round 32` heading
(N2), one-line token sentences in both lessons (N5/N6), no repair content. Result:

```
$ python3 plans/round33_defects.py --lane /tmp/r33-appendonly/fakelane
checks=6 defects=0        EXIT=0
```
Caveat (B6, matches `R33CounterAttack`): N3/N4 read absolute fleet paths
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-{31,32}/kengaku.md` regardless of `--lane`,
so in this run they were green against the **live repaired fleet reports**, not the fake lane.
The counter is therefore not hermetic for N3/N4: `--lane` does not scope them.

### 3e. Reality check — the actual repairs are true appends (git, read-only)

- Fleet commit `3d3ca566` ("round-33: kengaku erratum appends for routed defects N3 … and N4 …"):
  `git show --numstat` → `.ufo/reports/round-31/kengaku.md` **+7/−0**, `.ufo/reports/round-32/kengaku.md`
  **+7/−0**; both diffs are pure tail appends (Erratum addendum 3 / Addendum).
- Lane commit `7895588` ("round-33: C2 routed-defect repairs (N2 scorecard section, N5/N6 lesson
  errata) …"): `corpus/lessons/round-31.md` **+9/−0**, `corpus/lessons/round-30.md` **+9/−0**;
  both diffs append `## Corrections (round 33 …)` / `## Errata (round 33 …)` at file end.

So the observed after-state satisfies the append-only description; the counter simply cannot
detect a non-append-only state that keeps the tokens.

## 4. What IS guarded (honest partial credit)

- Deleting the disputed stale token outright reddens: N3 without `a44b5a8`, N5 without `:35-38`,
  N6 without `:78-81`/`78–81` **and** without `peer-reviewed` (the fake-lane first attempt reddened
  on `peer-reviewed` before the word was added).
- Every check is fail-closed on missing files and exceptions; all four redden correctly on the
  pre-repair bytes (also reproduced by `defects-before.txt` and `R33CounterAttack` §2).

## 5. Findings by severity

1. **[High] N3–N6 do not implement the predicate's append-only clauses.** `defects=0` certifies
   token placement in the current file, not that bytes were appended and originals preserved.
   Demonstrated: full rewrite (g3a), in-place edits (g3c/g5a/g6a), prepends (g3b/g5c), bare-token
   file (g4b), and a fully fabricated lane all green. (Corroborates `R33ClaimsReview` §"C2/N3–N6"
   and `R33CounterAttack` B4/E4–E6/F1.)
2. **[Medium] N3 predicate/code width mismatch: 400 vs 300.** A same-line gap of 350 chars satisfies
   the predicate wording and reddens the counter (f3a). `R33ClaimsReview` and `R33CounterAttack`
   B3/E3b concur.
3. **[Medium] `near()` is newline-blind and bidirectional.** Adjacent same-sentence tokens across a
   line break redden (f3b); notes placed before the original text bind as well as appends. This
   pushes honest repairs toward line-stuffing — the exact pattern the gameable exploits use.
4. **[Medium] N4 has no preservation requirement at all.** The old tip `bcd2a6c` may be deleted and
   the file reduced to the bare token; the check still passes (g4a/g4b).
5. **[Low] N3/N4 ignore `--lane`** (absolute fleet paths) — the counter's own `defects=0` on a
   lane mirror depends on live fleet state rather than the tree under test (B6).

## 6. Residual risk / verification gaps

- The conclusion that the *current repairs* are honest appends rests on git numstat/diff (3e) —
  read-only, at commits `3d3ca566` and `7895588`. It was not re-derived by the counter.
- Untested here: interaction with earlier round-31/32 appends in the same files (e.g. the
  round-31 report already carried three earlier erratum addenda; N3 binds to the newest one).
  Not needed for the verdict.
- The frozen predicate itself was read at `plans/round-33-claims.md`; `R33ClaimsReview` confirmed
  the same text at freeze commit `f0b20aea`. No post-score predicate change observed.

VERDICT: **limitation / false-negative class** — C2's N3–N6 checks verify token presence and
co-occurrence, not append-only bytes; the claim's append-only description is not enforced by the
counting command. The specific repairs landed this round are, on git evidence, genuine appends.
