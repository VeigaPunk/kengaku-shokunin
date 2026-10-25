# R33CounterAttack — mutation probe of `plans/round33_defects.py` (C2 counter)

Round 33, hyaku run 7, 2026-10-25. Target: the six-check routed-defect counter
`plans/round33_defects.py` @ freeze commit `f0b20aea` (unchanged through tip `7895588`;
`git diff f0b20aea..7895588 -- plans/round33_defects.py` is empty — verified live).
Scratch: `/tmp/r33-counterattack/` (1 MB; harness `exploits.py` + fixtures). The module
was imported read-only (`importlib.util.spec_from_file_location`); every exploit runs the
real check functions unmodified.

## 1. Selftest receipt

```
$ python3 plans/round33_defects.py --selftest
CASE registry-complete PASS … CASE N1-red-untracked PASS
SELFTEST checks=14 failed=0        EXIT=0
```

All 14 cases pass. **But the selftest is itself weak evidence**, for two structural
reasons (proven as exploits M1/M1b below):

- Its red cases for N1/N2/N5/N6 are all *file-absent* cases on an empty dir. A mutant
  that degenerates each check to "file exists" or "stale token present" still passes
  every red case and every green fixture. No selftest case ever presents a file that
  exists with wrong content.
- Its N1 green fixture does `git init -q && git add .` — **no commit** — blessing the
  index-vs-committed blind spot (E1, the smallest genuine defect found).

## 2. Frozen baseline reproduction

`defects-before.txt` (committed at freeze) records `checks=6 defects=6`, exit 1.
Reproduction attempt: `git archive f0b20aea | tar -x` into `/tmp`, copied the live
`.ufo/waves/round-32/` tree back in to recreate the pre-commit disk state, `git init -q`
(empty index ⇒ all 89 wave files "untracked"):

```
$ python3 plans/round33_defects.py --lane .
DEFECT N1 … 89 untracked files remain under .ufo/waves/round-32: assimilation/captures/SHA256SUMS.txt, …
DEFECT N2 … no '## Round 32' section …
DEFECT N5 … no appended correction updates verifier_mode.py's precedence locator to :39-40
DEFECT N6 … no appended correction updates … to :72 / :82-83
checks=6 defects=4   exit=1
```

**Delta: 4 defects, not 6.** N1's file count is 89 vs the frozen 84 (the live wave tree
grew by 5 files between the freeze receipt and the N1 commit — the defect's shape and
reason string reproduce exactly). N3 and N4 are *absent* from the archive run — because
`check_n3`/`check_n4` default to the absolute fleet paths
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-{31,32}/kengaku.md`, which have since
been repaired (fleet commit `3d3ca566`, "kengaku erratum appends for routed defects N3
and N4"). Re-running `check_n3`/`check_n4` directly against the pre-erratum bytes
(`git show ffe89acd:…`, saved as `/tmp/r33-counterattack/r31-pre.md` / `r32-pre.md`)
reproduces the frozen reason strings exactly:

- `N3: 'no appended erratum supersedes the a44b5a8 citation'`
- `N4: 'the round-32 report does not name the round-32 closure tip 112091c'`

So the frozen 6/6 reproduces faithfully **only** when the fleet-side bytes are pinned;
the counter itself cannot reproduce its own frozen receipt on an archived lane — see
blind spot B6.

For reference, the live repaired lane tip `7895588` prints `checks=6 defects=0`, exit 0.

## 3. Exploit table

"GAMED" = the check greens without the repair the frozen predicate describes.
"CAUGHT" = the exploit fails (check still reddens). "FALSE-NEG" = a genuine repair
form the check reddens — fragility, not gameability, but still a defect of the counter.

| # | Check | Exploit | Result |
|---|-------|---------|--------|
| E1 | N1 | `git add .ufo/waves/round-32` **without committing** (index-only) | **GAMED** — `git ls-files` sees the index, not HEAD; "tracked" ≠ committed, and nothing binds the files to a commit |
| E1b | N1 | control: wave file left untracked | CAUGHT — `1 untracked files remain` |
| E1c | N1 | untracked **fifo** + symlink under wave dir | **GAMED** — `find -type f` never sees non-regular files; `ls-files` set-difference stays clean |
| E1d | N1 | `.ufo/waves/round-32` itself a symlink to an untracked dir | **GAMED** — `find` does not descend a symlinked root; `on_disk` = ∅ |
| E2 | N2 | `SCORECARD.md` with bare `## Round 32` heading, fenced code + "round 32 happened maybe" — zero dispositions | **GAMED** — `re.search(r"^## Round 32\b", re.M)` tests heading presence only |
| E2b | N2 | `## Round 32` heading *inside* a fenced code block | **GAMED** — regex is not fence-aware |
| E3 | N3 | erratum sentence (`a44b5a8` near "superseded") + `ae95fe0` in an *unrelated* footer | **GAMED** — `ae95fe0` check is file-wide `"ae95fe0" in text`, not near-bound |
| E3b | N3 | genuine erratum with `a44b5a8`…"superseded" 351 chars apart | FALSE-NEG — frozen predicate says "within 400 characters"; the code uses `width=300`. Predicate/code mismatch |
| E3c | N3 | `a44b5a8` on one line, `Erratum: superseded by ae95fe0` on the next | FALSE-NEG — `near()` uses `.{0,300}` without `re.DOTALL`: no `near()` window can ever cross a newline. Same tokens on one line → green |
| E4 | N4 | `112091c` in unrelated appendix text ("worker nodes 112091c, 0fa3") | **GAMED** — bare substring test, no commit/tip context bound |
| E5 | N5 | appended `Style correction: the table for verifier_mode.py test fixtures moved to :39-40.` — no docstring repair | **GAMED** — one unrelated sentence supplies all three bindings |
| E5b | N5 | genuine correction split across a line break | FALSE-NEG — same newline blind spot as E3c |
| E6 | N6 | one appended line: `Correction: S086 erratum — published without peer review; table row :72, columns 82-83 corrected.` | **GAMED** — a single unrelated sentence satisfies all six N6 predicates at once |
| E6b | N6 | does the *original* lesson-30 pre-satisfy the S086 label? | partially — `near(orig,"S086","erratum")` and `near(orig,"S086","without peer review")` are both False, so the appended S086 tokens were load-bearing; the label check is still satisfiable by the same appended sentence as E6 |
| M1 | selftest | mutant N2 = "file exists" | **GAMED** — passes selftest red (empty dir) and green (selftest's own fixture) |
| M1b | selftest | mutant N5 = "`:35-38` in text" | **GAMED** — same hole |
| F1 | whole counter | fully fabricated lane in /tmp: committed wave file, `## Round 32` heading, one-line token sentences in both lessons | **GAMED** — `python3 plans/round33_defects.py --lane /tmp/r33-counterattack/lanes/fullfake` → `checks=6 defects=0`, exit 0. (N3/N4 green only because the live fleet reports are already repaired — see B6) |

## 4. Blind spots, ranked

- **B1 (smallest genuine blind spot): N1 measures the index, not the commit.**
  `git ls-files` enumerates the index; the frozen predicate and the N1 narrative both say
  the repair *commits* the tree. `git add` with no commit, an intent-to-add entry, or a
  staged-then-reset tree all green the check while the pushed tip stays exactly as
  dirty as before. The selftest's own green fixture models this exploit. One-line hardening:
  compare `find` output against `git ls-tree -r --name-only HEAD -- .ufo/waves/round-32`
  (HEAD exists) rather than `git ls-files`.
- **B2: `near()` can never cross a newline** (`re` lacks `DOTALL`). All co-occurrence
  bindings (N3 label, N5 correction, N6 correction + erratum + label) are silently
  same-line-only. Honest wrapped prose reddens; crammed single lines green. This pushes
  repaires toward line-stuffing — the exact pattern that makes the gameable exploits work.
- **B3: predicate/code width mismatch on N3.** Claims file says "within 400 characters";
  `near()` defaults to 300. A compliant 350-char-gap erratum reddens.
- **B4: bare substring/token presence everywhere.** `ae95fe0` (N3), `112091c` (N4),
  `:72`, `82-83`, `:39-40` are matched without word boundaries or context; `## Round 32`
  is matched even inside a code fence. Every check is a presence test; none re-derives
  semantics (e.g., N4 never confirms `112091c` is a commit naming the closure tip;
  N2 never tests that dispositions exist under the heading).
- **B5: `find -type f` ignores non-regular files.** Untracked symlinks, fifos, sockets —
  and a symlinked `.ufo/waves/round-32` root — are invisible to the on-disk set while
  `git ls-files` (and git add, which follows symlinks-as-blobs) says nothing. Minor for
  this wave tree, real for the general contract "nothing untracked remains".
- **B6: N3/N4 are not hermetic under `--lane`.** They read absolute fleet paths
  regardless of `--lane`, so the counter cannot reproduce its own frozen
  `defects=6` receipt on an archived tree (it now prints 4), and the lane argument is
  misleading — "defects=0" on a mirror depends on live fleet state, not on the tree
  under test. The selftest knows this (it injects fixtures via the optional parameter)
  but `main()` has no such override.
- **B7: `git ls-files` asymmetries.** Files tracked but deleted on disk are invisible to
  the check (it only diffs disk−index); filenames containing newlines split differently
  in `find` vs `ls-files` output (false RED at worst — conservative direction).

## 5. What survived

- Untracked regular files under the wave tree still redden (E1b) — the primary defect
  case cannot be bypassed by file tricks alone.
- Deleting/rewriting the stale tokens reddens (append-only guards on N3 `:a44b5a8`,
  N5 `:35-38`, N6 `:78-81`/`peer-reviewed` are real).
- Every check is fail-closed on missing files and on raised exceptions.
- The six checks genuinely were all defects at freeze (verified: `:39-40` absent from
  lesson-31, `:72`/`82-83` absent from lesson-30, no `## Round 32` in SCORECARD,
  `ae95fe0`/`112091c` absent from the pre-erratum fleet bytes).

## 6. Verdict

**VERDICT: counter-gameable.** `defects=0` exit 0 is reachable end-to-end on a fabricated
lane with zero semantic repair (F1), and every per-check predicate is greenable by token
presence alone (E1–E6). The exploitable core is that all six checks verify *text/byte
presence* rather than re-deriving the repair, and N1 — the structural one — checks the
index rather than a commit. The counter is still useful as a smoke alarm (it did
reproduce the six real defects, and the append-only guards hold), but as a C2 counting
command it certifies token placement, not repair. Minimum hardening set: HEAD-based
`ls-tree` for N1, `re.DOTALL` (or sentence-level segmentation) plus the frozen 400-char
width for `near()`, word-boundary/commit-context anchoring for the hash and locator
tokens, a `has_dispositions` probe under the `## Round 32` heading for N2, a
`--r31-report/--r32-report` flag (or lane-relative default) for N3/N4, and selftest red
cases with file-present-wrong-content plus an N1 fixture that commits.

## Receipts index

- Harness: `/tmp/r33-counterattack/exploits.py` (output quoted verbatim above).
- Pre-erratum fleet bytes: `/tmp/r33-counterattack/r31-pre.md` (20998 B,
  `git show ffe89acd:.ufo/reports/round-31/kengaku.md`), `r32-pre.md` (6231 B).
- Freeze baseline run: archive of `f0b20aea` + live wave tree + `git init` →
  `checks=6 defects=4` exit 1 (delta explained in §2); N3/N4 frozen reason strings
  reproduced on pinned pre-erratum bytes.
- No installs; tools used: python3, git, find, grep, coreutils. No production files
  written — this report is the only lane-tree write.
