# R33FN1 — Selftest Commit Falsification

**Seat:** KengakuR33.R33FN1SelftestCommit (falsify wave, round 33)
**Date:** 2026-10-25
**Target:** N1 green selftest fixture commit status — `plans/round33_defects.py` (lane: kengaku-shokunin)
**Tools installed:** none (no installs performed this run)

## Frozen claim under test

N1 (fixture docstring, `plans/round33_defects.py:12-14`):

> N1 ten round-32 wave paths sat untracked at a pushed tip. The repair commits the
> whole `.ufo/waves/round-32/` tree under this round's entry.

`check_n1` docstring (`:69`): "Every file under .ufo/waves/round-32/ is tracked; nothing untracked remains."
Registry label (`:167`): `N1 round32-wave-tree-committed`.

Prior ink: R33ClaimsReview.md:19 already flags the residual risk — "C2/N1 compares filesystem files with `git ls-files` … so it demonstrates index tracking, not necessarily committed-tree membership. … No check was run as part of this review." This seat runs the check.

## Verdict: **FALSIFIED — the green fixture creates NO commit; it stages only.** The check (and the fixture's green case) accepts a purely staged tree with no commit object, so the frozen claim's core predicate ("commits the whole tree") is unenforced.

---

## 1. The fixture's green path contains no commit

The entire green-path Git sequence in `selftest()` is (`:227-228`):

```python
subprocess.run(["git", "-C", str(empty), "init", "-q"], check=False)
subprocess.run(["git", "-C", str(empty), "add", "."], check=False)
cases.append(("N1-green-tracked", not check_n1(empty)))
```

`grep -nE "git|commit" plans/round33_defects.py` shows the only Git invocations in the whole file are `git init`, `git add .`, and the check's `git ls-files` (`:77`). **No `git commit` call exists anywhere in the fixture.** The only lines containing "commit" (`:12`, `:20`, `:110`) are prose/label text. Baseline selftest passes: `SELFTEST checks=14 failed=0` (rc 0).

## 2. Empirical proof on isolated /tmp repos (git 2.56.0, Python 3.14.8; `GIT_CONFIG_GLOBAL=/dev/null`, all `git -C` scoped to /tmp sandboxes)

Replicated the fixture's green tree byte-for-byte (`wave/seat.md`, scorecard, lessons; `git init -q`; `git add .`; **no commit**), using the **real** imported `check_n1`:

| Scenario | `check_n1` | HEAD | `git status --porcelain -- wave` | Committed-tree mutant |
|---|---|---|---|---|
| A. fixture green path verbatim (init+add, no commit) | **GREEN** (`""`) | `rev-parse --verify HEAD` → `fatal: Needed a single revision` (absent) | `A  .ufo/waves/round-32/seat.md` (staged) | RED (`"no commit at HEAD"`) |
| B. empty baseline commit exists, wave tree only staged | **GREEN** | `149ee08…` | `A  …/seat.md` (staged) | RED (`"1 wave files absent from HEAD tree: seat.md"`) |
| C. after real `git commit` | GREEN | `30ee005…` | `[]` | GREEN |
| D. `git add -N` on stray file (content never staged) | **GREEN** | `30ee005…` | ` A …/stray.md` | — |
| E. committed, working bytes rewritten | **GREEN** | `30ee005…` | ` M …/seat.md` | RED (`"seat.md differs from its committed blob"`) |
| F. committed, no remote, no upstream | **GREEN** | present | `[]` | — (`git remote -v` empty; `@{u}` → `fatal: no upstream configured`) |

Key facts:

- **A** is precisely the fixture's own `N1-green-tracked` case: `check_n1` returns `""` while `rev-parse --verify HEAD` fails — there is no commit object. The case passes on index state alone.
- **B** shows the check cannot tell "staged" from "committed": with a HEAD that does not contain the wave tree, `check_n1` is still green.
- **D**: the "nothing untracked remains" half is defeated by `git add -N` (intent-to-add): `git ls-files` lists `stray.md`, so the stray's content — never staged, untracked — is invisible.
- **E**: committed bytes vs working bytes are never compared; dirty/modified content passes.
- **F**: the claim's "at a pushed tip" is unenforced — no remote/upstream exists or is consulted.

## 3. Mutant test — a check that only consults `git ls-files`

A mutant restricted to `git ls-files` (no `find` disk comparison) was built (`lsfiles_only`):

```python
p = sh(lane, "ls-files", "--", WAVE32)
tracked = {l[len(W)+1:] if l.startswith(W+"/") else l for l in p.stdout.splitlines() if l}
```

On scenario A (stage-only) it returns `""` — **identical outcome to the real `check_n1`** (also `""`). The real check's observable behavior on the green path is exactly that of the ls-files-only mutant; the `find` disk comparison adds only the stray-file red case, not committedness.

## 4. Gate mutant — substituting committed-tree membership fails the fixture's own case

Rebinding the module-global `check_n1` to a committed-tree variant (`git ls-tree -r --name-only HEAD -- wave`; defect if HEAD absent or on-disk paths missing from HEAD tree) and running the fixture's *own* `selftest()`:

```
CASE N1-green-tracked FAIL
SELFTEST checks=14 failed=1
rc = 1
```

So the fixture's selftest is **insensitive to the committed-vs-staged distinction**: the green case passes only because the check reads the index (`git ls-files`), never `HEAD`. (Note: `selftest()` calls `check_n1` by direct global name in the green/red cases, not through `CHECKS`; patching `m.check_n1` is the correct injection point.)

## 5. Consequences for the claim

- The frozen wording "commits the whole … tree under this round's entry" is not enforced; staging alone satisfies N1. `git ls-files` proves index membership, not committed-tree membership, not "under this round's entry" (no ancestry/author/message check exists at all).
- `N1-red-untracked` (stray file) is the only N1 case the check actually exercises; it does not discriminate the claim's commit predicate.
- Falsification class: **uncaught false-accept** (a repair that only stages — or that pushes nothing — passes the green gate; the claim's stronger wording is untestable by this check). Secondary blind spots demonstrated: intent-to-add (`git add -N`), deleted-on-disk-but-indexed files, dirty working-tree content, and absent remote/upstream ("pushed tip" unenforced).

## Evidence retained

- `plans/round33_defects.py` lines 68-88 (`check_n1`), 227-235 (green/red cases), 167 (N1 label), grep confirming no `git commit` invocation.
- Live selftest output (above): `checks=14 failed=0`.
- Sandbox lab runs `A`-`F` (scenario table), ls-files-only mutant equality, and gate-mutant `N1-green-tracked FAIL` — all in /tmp (`/tmp/r33n1selftest/lab.py`, plus ad-hoc heredoc runs), fully isolated; no lane/fleet repo touched, no file edited, no git command run outside the /tmp sandboxes.
