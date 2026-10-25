# R31MutCounter — mutation test of the C2 counter (`plans/round31_defects.py`)

Seat: mutation tester (leaf). Claim under test: **C2** — `python3 plans/round31_defects.py --lane .`
prints `defects=0` and exits 0 on the repaired tree (`plans/round-31-claims.md` §C2).
Question: is that counter mutation-adequate — does it still report the ten defects when a check is
deleted, gutted, weakened, or when its own guards and exit contract are changed?

Everything below was run. Nothing is inferred unless the line says `[INFERENCE]`.

## 1. Target, and the two rewrites I had to absorb

| label | sha256 | when | state |
|---|---|---|---|
| v0 | `f5da41869cb6fd794cdc7146e0f6e862c59177a00d92b959deb29659986695cd` | 05:49, copied at seat start | superseded |
| v1 | `2c320d58dab609d7041318980354d0369cde437eef5ddf8a75012a0a7d4f3234` | 05:58 | superseded |
| **v2** | `c06ddc1e01eb6c6bb8edfdd58cf0ee6c7239dac57314a4a4353db580a81afd04` | 06:01 → current at report time | **graded version** |

`git -C <lane> status --porcelain -- plans/round31_defects.py` → `?? plans/round31_defects.py`
(untracked). A sibling seat rewrote the file twice while this seat ran: v1 added R6's `document_key`
normalization, three R7 assertions and `flat()` in R2; v2 added `append_only()` gates on R1/R2/R3/R10,
zero-width stripping in `plain()`, a single-regex R6 number parse, a row-cell-only CC0 test in R8, and
a revert test in R9. **All three versions were mutation-tested**; §3 is v2, §4 keeps v0/v1 because the
same gap recurs in all three and the rewrite history is what shows it is not a one-off slip.

## 2. Detectors and trees

Both detectors are the counter's own:

- **D1** `python3 <subject> --selftest` — baseline `SELFTEST checks=10 failed=0`, exit 0.
- **D2** `python3 <subject> --lane <tree>` — baseline per tree below. A mutant is *killed* iff D2's
  stdout or exit status moves in the failing direction; a mutant that reads green on a defective tree
  is a false negative, not a kill.

Fixtures live in `/tmp/r31-R31MutCounter`, built from read-only sources (`git -C <lane> show
HEAD:<path>`, `cp`, and one `git fetch <lane> <baseline-sha>` so v2's `append_only()` can diff against
the round's baseline commit — never `git clone`). The fetched objects are held once, in
`fixture-post3`; the other fixtures reach them through `objects/info/alternates`, so the whole scratch
tree is 41 MB (`rebuild_fixtures.py` recreates it). The v0/v1 fixtures used in §4 were pruned to stay
inside the scratch bound and are rebuilt on demand by `build_post.py` / `build_probes.py` /
`build_probes_v1.py`.

| tree | content | D2 baseline |
|---|---|---|
| `fixture-pre3` | baseline blobs + the five dirty seat reports | `checks=10 defects=10`, exit 1 |
| `fixture-post3` | snapshot of the lane's repaired bytes, seat reports committed | `checks=10 defects=0`, exit 0 |
| `probe6v2` | `fixture-post3` with the counted form replaced by the bare form | `defects=1`, exit 1 |
| `probe9stub3` | `fixture-post3` with `R30RevLesson.md` at HEAD replaced by a 3-line stub | `defects=1`, exit 1 |
| `probe9dirty3` | `fixture-post3` with `R30DraftGate.md` modified in the worktree only | `defects=1`, exit 1 |
| `probe9revert` | `fixture-post3` with `R30RevLesson.md` shortened to 120 lines (< 1023 at baseline) | `defects=1`, exit 1 |
| `LANE` | the live lane worktree, read-only | `checks=10 defects=0`, exit 0 |

The four probes are **not** shipped test cases; they exist to test whether a weakened check can still
separate a violating tree from a clean one. The `LANE` column is the strongest evidence in §3: at
report time the lane itself prints `defects=0` and exits 0, so "identical to baseline on LANE" means
the mutant is indistinguishable from the graded counter on the tree C2 will be judged on.

## 3. Mutation table — v2 (graded bytes)

| # | mutation (site) | D1 `--selftest` | D2 @ `fixture-post3` | D2 @ `LANE` (live) | verdict |
|---|---|---|---|---|---|
| m1 | delete `("R8", "entry-licence-adjective", check_r8),` from `CHECKS` (v2:318) | **KILLED** — `CASE registry-complete FAIL`, `SELFTEST checks=9 failed=1`, exit 1 | **KILLED** — `DEFECT registry: the check list no longer matches the frozen ten`, `checks=9 defects=10`, exit 1 | KILLED | killed by both |
| m2 | `check_r7` returns `""` always (injected before v2:236) | **KILLED** — `CASE R7-red-on-empty FAIL`, `SELFTEST checks=10 failed=1`, exit 1 | survived — byte-identical `checks=10 defects=0`, exit 0 | survived — identical | killed by **selftest only** |
| m3 | `check_r9` weakened to "HEAD has the path" (`cat-file -e` only; status, stub, revert and Pass-9 tests deleted) | survived — identical, exit 0 | **survived** — identical `checks=10 defects=0`, exit 0 | **survived** — identical | **SURVIVED** at acceptance; `probe9stub3`, `probe9dirty3`, `probe9revert` each → `checks=10 defects=0` (false negative) |
| m4 | `check_r6` weakened to a substring test on `"source rows are not in this lane's registry"`; staged-file, `document_key` and number parse deleted | survived — identical, exit 0 | **survived** — identical `checks=10 defects=0`, exit 0 | **survived** — identical | **SURVIVED** at acceptance; `probe6v2` → `checks=10 defects=0` (false negative) |
| m5 | `FROZEN` derived from `CHECKS` (v2:326-337 → `FROZEN = tuple((i, l) for i, l, _ in CHECKS)`) | survived — identical, exit 0 | **survived** — identical | **survived** — identical | **SURVIVED** (equivalent mutant: both guards compare `CHECKS` to itself) |
| m6 | final exit inverted (v2:382 → `return 0 if defects != 0 else 1`) | survived — selftest's own exit untouched, `SELFTEST checks=10 failed=0`, exit 0 | **KILLED by exit status only** — stdout byte-identical `checks=10 defects=0`, exit **1** | KILLED — exit 1 | killed by exit status; a grep-only detector survives it |
| m7 | m5 + m1 (extra probe) | exit **0**, `SELFTEST checks=9 failed=0` | `checks=9 defects=0`, exit **0** | `checks=9 defects=0`, exit 0 | killed only by the printed `checks=9` token |

Kills: m1 (both detectors), m6 (exit status). Single-detector kills: m2 (selftest only), m6.
Survivors: **m3, m4, m5** — identical stdout *and* exit status to the real counter on the live lane.

### The exact lines that survive

- **m3** — `v2:266-290`, the body of `check_r9` minus its `def` line: the `git status --porcelain`
  test (267-271), the `>= 100`-line stub test (275-276), the "shorter than at baseline" revert test
  (277-285), and the `"Pass 9"` anti-revert test on `HEAD:R30DraftGate.md` (286-288). What remains is
  `git cat-file -e HEAD:<path>`, so a dirty worktree, a stub HEAD blob and a reverted HEAD blob all
  read as clean — demonstrated on `probe9dirty3`, `probe9stub3` and `probe9revert`.
- **m4** — `v2:191-233`: the staged-file read (195-201), the `document_key` registry comparison
  (207-210) and the counted/bare number parse (219-231). With those gone, R6 is satisfied by the
  presence of the phrase, so an entry that re-grows the retracted "all three unregistered" claim
  beside the corrected one reads clean (`probe6v2` → `checks=10 defects=0`, where the shipped counter
  says `the entry asserts all three staged source rows are unregistered; 2 are`).
- **m5** — `v2:326-337`, the ten-entry `FROZEN` literal. Nothing observes it while `CHECKS` is intact;
  its value shows only in m7, and then only as the printed `checks=9`.
- **m2** — the whole of `check_r7` (`v2:235-250`): invisible to D2 on every tree where R7 is
  legitimately green. D1's `R7-red-on-empty` is the only detector.
- **m6** — the printed line at `v2:381` is byte-identical in the mutant; only the return value at
  `v2:382` differs.

## 4. The same six against v0 and v1

| # | v0 D1 | v0 D2 @ repaired tree | v1 D1 | v1 D2 @ repaired tree / live lane | shape |
|---|---|---|---|---|---|
| m1 | KILLED (`registry-complete FAIL`) | KILLED (`DEFECT registry …`) | KILLED | KILLED | guard holds |
| m2 | KILLED (`R7-red-on-empty FAIL`) | survived | KILLED | survived | selftest only |
| m3 | survived | **survived** | survived | **survived** | no strength test |
| m4 | survived | **survived** | survived | **survived** | no strength test |
| m5 | survived | **survived** | survived | **survived** | equivalent |
| m6 | survived | KILLED by exit status (stdout identical) | survived | KILLED by exit status | exit only |
| m7 | exit 0, `SELFTEST checks=9 failed=0` | `checks=9 defects=0` | same | same | `checks=9` only |

The v0 tree was `fixture-post-B` and the v1 tree `fixture-post2`/`LANE` (both `defects=0`). The
pattern is unchanged across two rewrites: the registry guard (m1/m7), the always-green check (m2) and
the exit contract (m6) are covered; **check strength** (m3, m4) is not, in any version.

## 5. What the fixture work surfaced

### 5.1 v0's R6 was unsatisfiable on the lane's own registry (fixed in v1, kept in v2)

The staged file names three sources; `corpus/SOURCES.md:23` carries the GEM review as
`https://aclanthology.org/2026.gem-main.50/` while the staged row cites
`https://aclanthology.org/2026.gem-main.50.pdf`. v0 tested
`registered = [url for url in urls if url.rstrip("/") in registry]` and demanded `unregistered == 2`,
so on byte-identical registry bytes it re-derived 3 and refused:

```
$ python3 pristine.py --lane fixture-post      # fully repaired entry, registry = committed bytes
DEFECT R6 entry-staged-source-count: re-derived 3 unregistered staged sources, the repair assumes 2
checks=10 defects=1
```

v0 therefore could not reach `defects=0` at all: C2's exit-0 arm required an undisclosed registry edit
or a different R6. v1's `document_key` fixed it and v2 keeps it; the registry was never rewritten for
it — S001's URL cell is byte-identical in the baseline blob and the live worktree (`…/2026.gem-main.50/`),
and `python3 lane_v2.py --lane fixture-post3` prints `checks=10 defects=0`. (`corpus/SOURCES.md` did
change this session — C1 appended S092/S093/S100 at `:111-113` — but not S001.)

### 5.2 v1's bare-form branch never fired; v2 fixes it

v1 guarded the bare assertion with `(?<![a-z] )`, which also rejects it after any lowercase word, so
`probe6v1` ("and its three source rows are not in this lane's registry") produced
`the entry states no staged-source count` instead of naming the retraction. v2 replaced it with
`(?:([a-z]+) of )?its three …` and now prints
`the entry asserts all three staged source rows are unregistered; 2 are` on `probe6v2`. Recorded
because it is the one case where a probe tree changed a verdict-relevant message rather than a count.

### 5.3 The selftest's only assertion is red-on-empty

`v2:340-352` runs each check against an empty `TemporaryDirectory` and requires a non-empty return. It
never feeds a check a **non-empty violating** tree — which is exactly why m3, m4 and m5 pass it, and
why m2's kill rests on it alone. Three cheap cases would close most of the gap, all already built
here: `probe9dirty3`-shaped (report dirty at HEAD), `probe6v2`-shaped (counted form replaced by bare)
and `probe9revert`-shaped (HEAD blob shorter than baseline).

### 5.4 Surface v2 added that these six mutants do not exercise

v2's `append_only()` gates on R1/R2/R3/R10 (`v2:100-116`), the zero-width strip in `plain()`
(`v2:77-87`), the row-cell-only CC0 test in R8 (`v2:253-263`) and the R9 revert test are **untested by
the six assigned mutants**. Only the revert test was exercised, by `probe9revert`, which it catches.
No claim is made here about whether a weakened `append_only` or a weakened `plain()` would be caught;
that would need its own mutants (e.g. `append_only` returning `""` unconditionally, or `INVISIBLES`
emptied).

## 6. Bounds, restoration, tooling

- The lane copy was **never written** by this seat. `plans/round31_defects.py` was read three times
  (`f5da4186…` → `2c320d58…` → `c06ddc1e…`, all sibling rewrites) and copied; every run against the
  lane used read-only git (`show`, `status --porcelain`, `cat-file`, `diff --numstat`, `rev-parse`,
  `log`). My only lane write is this report.
- Mutation substrate: `/tmp/r31-R31MutCounter/{mutant_*,v1_mutant_*,v2_mutant_*}.py`, with the three
  pristine copies beside them (`pristine.py`, `lane_now.py`, `lane_v2.py`). Fixtures are git repos
  holding the pristine state as a commit, so every cell above is one command away:
  `python3 v2_mutant_m3.py --lane probe9revert`.
- Scratch: 41 MB (`du -sh /tmp/r31-R31MutCounter`). No tool installed or upgraded (Python 3.14.8
  only); no pacman transaction, no network fetch, no `git clone`, no write outside
  `/tmp/r31-R31MutCounter` and this file.
- At report time the lane's own counter prints `checks=10 defects=0` and exits 0, and its bytes are
  still `c06ddc1e…` — the same bytes every cell of §3 was measured against.

VERDICT: NOT MUTATION-ADEQUATE — 3 of 6 mutants survive both shipped detectors byte-identically on the live lane (m3 R9 reduced to "HEAD has the path", m4 R6 reduced to a substring test, m5 vacuous FROZEN guard), and m2/m6 are each killed by only one detector (selftest / exit status), so `checks=10 defects=0` is not by itself evidence that R6 and R9 still test what they claim.
