# R31MutCounter — mutation test of the C2 counter (`plans/round31_defects.py`)

Seat: mutation tester (leaf). Claim under test: **C2** — `python3 plans/round31_defects.py --lane .`
prints `defects=0` and exits 0 on the repaired tree (`plans/round-31-claims.md` §C2).
Question asked: is that counter mutation-adequate, i.e. does it still report the ten defects when a
check is deleted, gutted, weakened, or when its own guards and exit contract are changed?

Everything below was run. Nothing is inferred unless the line says `[INFERENCE]`.

## 1. Target, and the drift I had to absorb

| label | bytes | sha256 | when |
|---|---|---|---|
| v0 | `plans/round31_defects.py` as copied at seat start | `f5da41869cb6fd794cdc7146e0f6e862c59177a00d92b959deb29659986695cd` | 05:49 |
| v1 | the same path, current at report time | `2c320d58dab609d7041318980354d0369cde437eef5ddf8a75012a0a7d4f3234` | 05:58 → unchanged since |

`git -C <lane> status --porcelain -- plans/round31_defects.py` → `?? plans/round31_defects.py`
(untracked). Between my copy and the first battery a sibling seat rewrote the file: `check_r6` gained
the `document_key` normalization, `check_r7` gained three assertions, `check_r2` gained `flat()`.
**Both versions were mutation-tested** — v0 as the bytes that existed when the seat started, v1 as the
bytes that will be graded. The v0 run is not padding: it is what caught the R6 hole in §5.1.

## 2. Detectors and trees

Detectors (both shipped by the counter itself):

- **D1** `python3 <subject> --selftest` — baseline `SELFTEST checks=10 failed=0`, exit 0.
- **D2** `python3 <subject> --lane <tree>` — baseline per tree below; a mutant is *killed* iff D2's
  stdout or exit status changes, and the change must move in the failing direction (a mutant that goes
  green on a defective tree is a false negative, not a kill).

Trees are pinned fixtures in `/tmp/r31-R31MutCounter`, built from read-only sources (no `git clone`;
`git -C <lane> show HEAD:<path>` plus `cp`), each a git repo so R9's `status`/`cat-file` calls run:

| tree | content | D2 baseline |
|---|---|---|
| `fixture-pre` | HEAD blobs of the six round-30 files + the five dirty seat reports | `checks=10 defects=10`, exit 1 |
| `fixture-post2` | snapshot of the lane's repaired bytes, seat reports committed | `checks=10 defects=0`, exit 0 |
| `fixture-post` | v0-only: my authored repairs, **registry byte-identical to the lane** | v0: `defects=1` (§5.1) |
| `fixture-post-B` | v0-only: as above + S001's URL normalized to the staged `.pdf` form | v0: `defects=0`, exit 0 |
| `probe6v1` | `fixture-post2` with the counted form replaced by the bare form | `defects=1`, exit 1 |
| `probe9stub2` | `fixture-post2` with `R30RevLesson.md` at HEAD replaced by a 3-line stub | `defects=1`, exit 1 |
| `probe9dirty2` | `fixture-post2` with `R30DraftGate.md` modified in the worktree only | `defects=1`, exit 1 |

`probe6v1`/`probe9stub2`/`probe9dirty2` are **not** shipped test cases. They exist to show whether a
weakened check can still separate a violating tree from a clean one.

## 3. Mutation table — v1 (current bytes, the graded version)

Acceptance tree for "killed / survived" is `fixture-post2` (`defects=0`), because that is the state
C2 claims. The pre-repair column is reported separately: a mutant caught there is caught only because
the tree still carries the defect the check exists to find.

| # | mutation (site) | D1 `--selftest` | D2 full run @ `fixture-post2` | D2 full run @ `fixture-pre` | verdict |
|---|---|---|---|---|---|
| m1 | delete `("R8", "entry-licence-adjective", check_r8),` from `CHECKS` (v1:274) | **KILLED** — `CASE registry-complete FAIL`, `SELFTEST checks=9 failed=1`, exit 1 | **KILLED** — `DEFECT registry: the check list no longer matches the frozen ten`, `checks=9 defects=10`, exit 1 | killed | killed by both |
| m2 | `check_r7` returns `""` always (injected before v1:203) | **KILLED** — `CASE R7-red-on-empty FAIL`, `SELFTEST checks=10 failed=1`, exit 1 | survived — byte-identical `checks=10 defects=0`, exit 0 | killed (`defects=9`) | killed by **selftest only** |
| m3 | `check_r9` weakened to "HEAD has the path" (`cat-file -e` only) | survived — identical, exit 0 | **survived** — identical `checks=10 defects=0`, exit 0 | killed (`defects=9`) | **SURVIVED** at acceptance; `probe9stub2`→`defects=0` and `probe9dirty2`→`defects=0` (false negative) |
| m4 | `check_r6` weakened to a substring test on `"source rows are not in this lane's registry"`; staged-file and registry re-derivation deleted | survived — identical, exit 0 | **survived** — identical `checks=10 defects=0`, exit 0 | killed (`defects=9`) | **SURVIVED** at acceptance; `probe6v1`→`defects=0` (false negative) |
| m5 | `FROZEN` derived from `CHECKS` (v1:282-292 → `FROZEN = tuple((i, l) for i, l, _ in CHECKS)`) | survived — identical, exit 0 | **survived** — identical, exit 0 | survived | **SURVIVED** (equivalent mutant: both guards now compare `CHECKS` to itself) |
| m6 | final exit inverted (v1:338 → `return 0 if defects != 0 else 1`) | survived — selftest's own exit untouched, `SELFTEST checks=10 failed=0`, exit 0 | **KILLED by exit status only** — stdout byte-identical `checks=10 defects=0`, exit **1** | killed (exit 0 with `defects=10`) | killed by exit status; a grep-only detector survives it |
| m7 | m5 + m1 (extra probe) | exit **0**, `SELFTEST checks=9 failed=0` | `checks=9 defects=0`, exit **0** | `checks=9 defects=9`, exit 1 | killed only by the printed `checks=9` token |

Kills: m1, m6. Kills by a single detector only: m2 (selftest), m6 (exit status). Survivors: m3, m4, m5.

### The exact lines that survive

- **m3** — `lane_now.py:231-244`: `git status --porcelain` on each report (231-236), the HEAD blob
  fetch and its `>= 100`-line stub test (237-241), and the `"Pass 9"` anti-revert test on
  `HEAD:R30DraftGate.md` (242-244). With
  those gone, `git cat-file -e HEAD:<path>` is the whole of R9, so a worktree that differs from HEAD
  and a HEAD blob that is a three-line stub both read as clean (`probe9stub2` → `checks=10 defects=0`).
- **m4** — `lane_now.py:165-199`: the staged-file read, the `document_key` registry comparison
  (178-183) and the counted/bare number parse (187-197). With those gone, R6 is satisfied by the
  presence of the phrase, so an entry that re-grows the retracted claim beside the corrected one reads
  clean (`probe6v1` → `checks=10 defects=0`).
- **m5** — `lane_now.py:282-292`: the ten-entry `FROZEN` literal. Nothing observes it while `CHECKS`
  is intact; the guard's value appears only in m7, and then only as the printed `checks=9`.
- **m2** — the whole of `check_r7` (`lane_now.py:202-216`): invisible to D2 on every tree where R7 is
  legitimately green. D1's `R7-red-on-empty` is the only detector.
- **m6** — the printed line at `lane_now.py:337` is identical in the mutant; only the return value at
  `lane_now.py:338` differs.

## 4. Mutation table — v0 (the bytes as copied, `f5da4186`)

| # | D1 `--selftest` | D2 @ `fixture-post-B` (`defects=0`) | D2 @ `fixture-pre` (`defects=10`) | verdict |
|---|---|---|---|---|
| m1 | KILLED (`registry-complete FAIL`, `checks=9 failed=1`) | KILLED (`DEFECT registry …`, exit 1) | killed | killed by both |
| m2 | KILLED (`R7-red-on-empty FAIL`) | survived (identical) | killed | killed by selftest only |
| m3 | survived | **survived** | killed | SURVIVED at acceptance |
| m4 | survived | **survived** | killed | SURVIVED at acceptance |
| m5 | survived | **survived** | survived | SURVIVED (equivalent) |
| m6 | survived | KILLED by exit status (stdout identical) | killed | killed by exit status |
| m7 | exit 0, `SELFTEST checks=9 failed=0` | `checks=9 defects=0` | `checks=9 defects=9` | killed only by `checks=9` |

Same shape as v1: the guard (m1/m7), the always-green check (m2) and the exit contract (m6) are
covered; check **strength** (m3, m4) is not, in either version.

## 5. Findings the fixture work surfaced

### 5.1 v0's R6 was unsatisfiable on the lane's own registry (fixed in v1)

The staged file names three sources; the lane's `corpus/SOURCES.md:23` carries the GEM review as
`https://aclanthology.org/2026.gem-main.50/` while the staged row cites
`https://aclanthology.org/2026.gem-main.50.pdf`. v0 tested
`registered = [url for url in urls if url.rstrip("/") in registry]` and demanded `unregistered == 2`,
so on **byte-identical registry bytes** it re-derived 3 and refused:

```
$ python3 pristine.py --lane fixture-post      # registry byte-identical to the lane's
DEFECT R6 entry-staged-source-count: re-derived 3 unregistered staged sources, the repair assumes 2
checks=10 defects=1
```

`fixture-post` is a fully repaired entry over the committed registry (HEAD blob), so v0 could not
reach `defects=0` at all: C2's exit-0 arm required either an undisclosed registry edit or a different
R6. v1 fixes this with `document_key` (`lane_now.py:178-183`), and the fix does the work by itself —
the registry was never rewritten for it:

```
$ grep -n "gem-main.50" <lane>/corpus/SOURCES.md        # HEAD blob and live worktree, same cell
23:| S001 | … — https://aclanthology.org/2026.gem-main.50/ | paper | A | …
$ python3 lane_now.py --lane fixture-post2                # repaired entry + that registry
checks=10 defects=0
```

(`corpus/SOURCES.md` did change during the session — C1 appended S092/S093/S100 at `:111-113` — but
S001's URL cell is byte-identical in HEAD and the worktree, so R6's verdict on it is unchanged.)

### 5.2 v1's bare-form branch is unreachable after a lowercase word

`lane_now.py:188` guards the bare form with `(?<![a-z] )`. That is right for `two of its three …`
(the `of ` prefix must be excluded) but it also rejects the bare form after any lowercase word:

```
$ python3 lane_now.py --lane probe6v1      # entry reads "and its three source rows are not in this lane's registry"
DEFECT R6 entry-staged-source-count: the entry states no staged-source count; the re-derived count is 2
```

The tree is still red, so C2's count is unaffected, but the branch that exists to name this exact
shape (`asserts all three staged source rows are unregistered`) never runs, and the message misnames
the defect.

### 5.3 The selftest's only assertion is red-on-empty

`lane_now.py:298-308` calls each check against an empty `TemporaryDirectory` and requires a non-empty
return. It never feeds a check a **non-empty violating** tree, which is exactly why m3, m4 and m5 pass
it, and why m2's kill depends on it alone. Two cheap cases would close most of the gap, e.g.
`probe9dirty2`-shaped (report dirty at HEAD) and `probe6v1`-shaped (counted form replaced by bare).

## 6. Bounds, restoration, tooling

- The lane copy was **never written**. `plans/round31_defects.py` hashed `2c320d58…` before and after
  every battery run; the only change observed all session is the sibling's own rewrite
  (`f5da4186…` → `2c320d58…`), detected at 05:58 and re-targeted. My only lane write is this report.
- Every mutation lives in `/tmp/r31-R31MutCounter/{mutant_*,v1_mutant_*}.py`; the pristine bytes are
  kept beside them (`pristine.py`, `lane_now.py`) and the fixtures are git repos with the pristine
  state committed, so each cell above is reproducible with one command.
- Scratch: 9.9 MB. No tool installed or upgraded (Python 3.14.8 only); no pacman transaction, no
  network fetch, no `git clone`, no write outside `/tmp/r31-R31MutCounter` and this file.
- Read-only git only: `show`, `status --porcelain`, `cat-file`, `rev-parse`, `log`.

VERDICT: NOT MUTATION-ADEQUATE — 3 of 6 mutants (m3 R9 weakened to "HEAD has the path", m4 R6 weakened to a substring test, m5 vacuous FROZEN guard) survive both shipped detectors on the repaired tree, and m2/m6 are each killed by only one detector (selftest / exit status), so `checks=10 defects=0` is not by itself evidence that R6 and R9 still test what they claim.
