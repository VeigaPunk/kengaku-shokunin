# R50C1CritBlind4 — two blind hostile modules for the round-50 C1 fence

Seat `R50C1CritBlind4` (critic, blind-hostile author). Item served: **R50-C1 (novelty)** — author TWO blind
hostile modules for the fixture fence: (i) a `.git` FILE whose `gitdir:` line carries a NUL / newline delimiter
trick, (ii) a store whose `config` gains an `[include]` only AFTER the gitfile is followed.

```
REV  lane tip at measurement   c3372a9b24d3a200946a6b37dc0a31ed5c982cc1  (live checkout, not written to)
REV  measurement clone         kengaku-shokunin @ 3b02d573d58cc6d2e0d27ef92ac0815354912252 (git clone --shared)
REV  freeze ancestry           git merge-base --is-ancestor 3b02d57… c3372a9… -> FREEZE_ANCESTOR_OK
REV  fence under test          plans/fixture_fence.py sha256 05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e (still the BASE fence at the live tip)
REV  population pin            b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 (126 rows, verified by the counter leg below)
REV  toolchain                 git 2.56.0, python 3.14
REV  live working tree         at report time `git status` shows `M plans/fixture_fence.py`, `M plans/mutants50/c1-mutants.json`, `M plans/round50_c1_verify.py` — other seats' in-progress S2 work, NOT this seat's and NOT what was measured. Every measurement above is against the frozen clone at 3b02d57 (fence `05d5fe03…`).
```

Axes named: **novelty** (this seat only authors C1's SEALED-leg content). No coverage claim, no C2 pointer
surface touched, no SCORECARD/LOG/corpus write, no commit. The seat does not judge or claim R50-C1 admission.

## Deliverables (2 module files, 3 fixtures)

| file (delivered at `.ufo/waves/round-50/w1/C1CritBlind4/sealed/`) | sha256 | fixtures |
|---|---|---|
| `c4_gitfile_delimiter.py` | `95429f872677b32c06a6d53c8edd09668b9798854fdfa5470075c7100a6142fa` | 2 |
| `c4_gitfile_store_include.py` | `3c99e89ba2426b7022521417649e46b077c403800fb20496ed1704df1467b04a` | 1 |

Byte payloads of the `.git` FILEs (the whole point of the modules; everything else is the honest `n21` shape
`gitdir: ../store\n` over a plain-init store inside `d` plus two commits):

```
b4a-gitfile-nul-two-stores         b"gitdir: ../../side/store2\x00../store\n"
b4a-gitfile-newline-two-pointers   b"gitdir: ../store\ngitdir: ../../side/store2\n"
b4b-gitfile-store-include          b"gitdir: ../store\n"  + tail of <store>/config:
                                   b"[include]\n\tpath = ../../side/foreign.cfg\n"   (appended after the last git child)
                                   + <gen>/side/foreign.cfg : b"[core]\n\tfsmonitor = ../../side/spy.sh\n"
```

Both modules are **blind**: authored in w1 against git's documented gitfile/config format and the honest class
`n21-separate-gitdir` only; the repaired `plans/fixture_fence.py` does not exist at any measured revision (the
live fence is still `05d5fe03…`). Neither module's docstring asserts anything about how the repair is spelled.

## 1. What git 2.56.0 actually does (the ground the modules stand on)

Probe `probe_gitfile.py` (scratch), full output in `receipts/probe_gitfile2.out`. Layout per case: `<case>/d` =
fixture dir, `<case>/d/wt/.git` = the FILE under test, `<case>/d/store` = in-`d` plain store
(`INSIDE-STORE-COMMIT`), `<case>/side/store2` = **bare** store outside the fixture dir
(`OUTSIDE-STORE-COMMIT`). Decisive rows:

```
CASE w1-two-gitdir-lines bytes= 'gitdir: ../store\ngitdir: ../../side/store2\n'
  git rc=128 resolved=- inside_d=None
  git stderr=[fatal: gitfile does not point to a valid repository: <W>/cases/w1-two-gitdir-lines/d/wt/.git]
CASE w3-nul-outside-first bytes= 'gitdir: ../../side/store2\\0../store\n'
  git rc=0 resolved=<W>/cases/w3-nul-outside-first/side/store2 inside_d=False
  log rc=0 subject=OUTSIDE-STORE-COMMIT
CASE w4-nul-inside-first bytes= 'gitdir: ../store\\0../../side/store2\n'
  git rc=0 resolved=<W>/cases/w4-nul-inside-first/d/store inside_d=True
CASE w5-crlf-outside bytes= 'gitdir: ../../side/store2\r\n'
  git rc=0 resolved=<W>/cases/w5-crlf-outside/side/store2 inside_d=False
CASE w6-trailing-space-inside bytes= 'gitdir: ../store \n'
  git rc=128 resolved=-
CASE w8-nul-only-outside bytes= 'gitdir: ../../side/store2\\0\n'
  git rc=0 resolved=<W>/cases/w8-nul-only-outside/side/store2 inside_d=False
CASE w9-blank-then-outside bytes= 'gitdir: ../../side/store2\n\n'
  git rc=0 resolved=<W>/cases/w9-blank-then-outside/side/store2 inside_d=False
CASE w10-no-space bytes= 'gitdir:../store\n'   -> fatal: invalid gitfile format
```

Rules pinned by measurement (all 15 cases in the receipt):

1. **NUL truncates the value (C-string semantics).** `…store2\0../store` resolves `store2` — the store git uses
   is a *prefix* of the declared bytes. w3 is therefore a **live escape**: git's git dir is outside `d` while
   the same bytes name an in-`d` store.
2. **An embedded newline is not a second declaration — git refuses the whole file** (`fatal: gitfile does not
   point to a valid repository`, rc 128): it stats the buffer including the newline. A line-oriented reader
   takes line 1 (`../store`), which is a *complete plain-init store inside `d`*.
3. CRLF and a trailing blank line are accepted and stripped; `gitdir:` without the space is `invalid gitfile
   format`; a trailing space/tab before the newline is **rejected**.

Why refusal is the only sound verdict on both payloads: in each, the store git uses (or refuses to pick) is not
the store the bytes declare, and one of the two candidate stores lies outside `d`. The fence's own predicate is
"admit only a fixture whose git store is provably the shape a plain init writes inside `d`"; a pointer with two
readings is not provable.

## 2. Measured verdicts on the built fixtures (lane builder, lane Ctx)

`driver.py` builds each module with the lane's **own** `plans/honest50/build_honest_population.py::build_once`
and the round-44 `Ctx`, then runs the frozen fence (`receipts/driver.out`):

```
FIXTURE b4a-gitfile-nul-two-stores tool anchor argv ['--lane', 'wt']
  base-fence verdict=BREACH reason='wt/.git is a file (gitdir redirect), not a directory'
  git gitdir rc=0 resolved=<S>/driver/c4_gitfile_delimiter/side/store2 inside_d=False
  git log -1 rc=0 subject=OUTSIDE-STORE-COMMIT
  lane gitfile_index_paths -> RAISES ValueError: lstat: embedded null character in path

FIXTURE b4a-gitfile-newline-two-pointers tool anchor argv ['--lane', 'wt']
  base-fence verdict=BREACH reason='wt/.git is a file (gitdir redirect), not a directory'
  git gitdir rc=128 resolved=- inside_d=None
  git stderr='fatal: gitfile does not point to a valid repository: <S>/driver/…/f001/wt/.git'

FIXTURE b4b-gitfile-store-include tool anchor argv ['--lane', 'wt']
  base-fence verdict=BREACH reason='wt/.git is a file (gitdir redirect), not a directory'
  git gitdir rc=0 resolved=<S>/driver/c4_gitfile_store_include/f000/store inside_d=True
  git log -1 rc=0 subject=two
  git config --includes --get core.fsmonitor rc=0 out='../../side/spy.sh' err=''
  strace outside-include opens=1
    openat(AT_FDCWD<<S>/driver/c4_gitfile_store_include/f000/wt>, "<S>/driver/c4_gitfile_store_include/f000/store/../../side/foreign.cfg", O_RDONLY) = 4<<S>/…/side/foreign.cfg>
```

The store in module (ii) is provably **inside** `d` (`rev-parse --absolute-git-dir` = `<d>/store`), its entry
list is exactly a plain init, and the only path outside `d` is opened *because* a git child followed the gitfile
and parsed the resolved store's config. That is the property the module pins.

## 3. Kill directions, witnessed (QUALITY Q38) — and the fairness control

Four candidate resolvers, all reusing the lane's own tree walk and `_store` (scratch candidate code, not a lane
deliverable), scored against every fixture plus the honest class `n21` (`receipts/matrix.out`, verbatim):

```
fixture                            base       strict/full line-first/full line-first/names last-NUL/full
n21-separate-gitdir                BREACH     ADMIT      ADMIT          ADMIT          ADMIT
b4a-gitfile-nul-two-stores         BREACH     refuse     refuse         refuse         ADMIT
b4a-gitfile-newline-two-pointers   BREACH     refuse     ADMIT          ADMIT          ADMIT
b4b-gitfile-store-include          BREACH     refuse     refuse         ADMIT          refuse
```

- `strict` = git's documented format (one `gitdir: ` line, no NUL, no CR, no trailing whitespace) + the lane's
  `_store`. It **ADMITs the honest class and refuses all three hostile fixtures** → the modules are passable by
  a sound repair, not bait, and they demand exactly one thing: the pointer must be classified byte-exactly and
  the *resolved* store's config must still be parsed.
- Witnessed kill directions: `line-first` (any repair that resolves the first `gitdir:` line and classifies that
  store — a full classification, not just names) admits the **newline** fixture, whose second declaration names
  a store outside `d`; `line-first/names` (classifies the resolved store by entry names only, config unparsed)
  admits the **store-include** fixture; `last-NUL` admits the **NUL** fixture while git resolves the outside
  store.
- The honest control (`receipts/honest_control.out`): `n21-separate-gitdir` → `base-fence verdict=BREACH` (the
  claims' over-refusal) and `probe[*] -> ADMIT` for all three lenient resolvers, i.e. the resolvers are
  candidate repairs that already satisfy the honest leg for that class.

## 4. Wiring receipt — the counter's SEALED leg on the two modules

Scratch clone at the freeze commit, the two files copied into its `plans/sealed50/`, frozen counter run with
`--skip-mutants` (mutant leg is not this seat's business) and `--allow-dirty` (the clone carries the copies):

```
$ git -C $S/lane rev-parse HEAD
3b02d573d58cc6d2e0d27ef92ac0815354912252
$ python3 plans/round50_c1_verify.py --lane . --skip-mutants --allow-dirty --work "$S/countwork"
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
FENCE …/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=2 clean=2 leaked=0 build_errors=0
SEALED50-TOTAL 2 expected_min=6
PREDICATE R50-C1 fail
EXIT=1
```

Both modules build with **0 build errors** and every fixture is `BREACH` (clean=2/2, leaked=0) on the base
fence; the honest leg and the population are untouched by them (126 / mismatched=0 — the base fence's 13
refusals are the claims' control, reproduced exactly). The `PREDICATE fail` is the base fence's, not the
modules': the do-nothing control must fail before S2.

`SEALED50-TOTAL 2 expected_min=6` is the arithmetic the L1 needs: `SEALED50_MIN` counts **module files**, so
this seat contributes **2 of the 6 required files (3 fixtures)**; the wave needs ≥4 more module files from
other blind seats.

## 5. Findings handed to the L1 (defects of the surrounding instrument, not of the modules)

- **F1 (real, blocks a naive repair).** The lane's own n21 identity helper **raises** on the NUL payload:
  `plans/honest50/build_honest_population.py::gitfile_index_paths` does `(p.parent / m.group(1)).resolve()` on
  the `GITFILE` group, and `os.path.realpath` raises `ValueError: lstat: embedded null character in path`. A
  repaired fence that resolves a gitfile with `.resolve()`/`realpath` therefore does not *refuse* this fixture,
  it **raises**; `verdicts()` scores a raising fence `ERROR`, which is not `BREACH`, so the SEALED leg goes
  unclean and C1's kill rule ("any sealed module not refused") fires. The repair must return a one-line refusal
  reason for any NUL in the pointer, never raise. (The helper is not on the counter's sealed path today — the
  only `tree_identity` call in `round50_c1_verify.py` is the honest-row population check — so the predicate
  itself does not crash; `receipts/driver.out` shows the exception, `receipts/counter.out` shows the leg clean.)
- **F2 (wiring).** `plans/sealed50/` exists in the live checkout, **untracked**, and as of this measurement
  holds byte-identical copies of both files (`sha256` equal to the table above, verified with `cmp`). This seat
  wrote only `.ufo/waves/round-50/w1/C1CritBlind4/`; it did not write, and must not be credited with, the
  `plans/sealed50/` copies. The directory holds 18 module files, so the ≥6 floor is met from the wave, but
  nothing there is committed yet (`git status --porcelain plans/sealed50` -> `?? plans/sealed50/`).
- **F3 (novelty, no duplicate authority).** No other module in `plans/sealed50/`, `plans/sealed46/`,
  `plans/refusals46/` or the batteries carries a NUL in a `.git` FILE (the only NUL literal in `sealed50` is
  mine) or a second `gitdir:` declaration; the gitfile neighbours there are different classes (symlink chain,
  relative objects link, second store mount). No existing module puts an `[include]` into the config of the
  store a gitfile names — the four include modules (`f10`, `f11`, `f13`, `f14`) append it to a plain repo's
  `.git/config`. Both classes are new, and they are the hostile counterparts of the honest class the repair must
  keep admitting (`n21`).
- **F4 (rules to encode).** From §1: NUL truncates (so a NUL must be refused, not truncated and judged);
  embedded newline ⇒ git refuses the file (so "first line wins" is unsound); CRLF and a trailing blank line are
  git-accepted (refusing them is over-refusal on a state git itself writes, not a breach); `gitdir:` with no
  space is invalid; a trailing space before the newline is git-rejected while the lane's own `GITFILE` regex
  accepts it (`group '../store'` in the receipt) — a repair reusing that regex without a trailing-whitespace
  check admits a file git will not use.

## Exact commands run (scratch root `S=/fast/scratch/hyaku/kengaku-r50/R50C1CritBlind4`, `TMPDIR=$S`)

```
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
git -C lane checkout -q --detach 3b02d573d58cc6d2e0d27ef92ac0815354912252
sha256sum lane/plans/fixture_fence.py lane/plans/honest50/population.txt
python3 probe_gitfile.py  "$S/probe1"      # first pass (outside store built as a work tree; superseded)
python3 probe_gitfile2.py "$S/probe3"      # bare outside store -> receipts/probe_gitfile2.out
python3 driver.py         "$S"             # build both modules with the lane builder; fence + git + probes
python3 probe_honest.py   "$S"             # honest n21 control -> receipts/honest_control.out
python3 probe_matrix.py   "$S"             # killed/fairness matrix -> receipts/matrix.out
mkdir -p lane/plans/sealed50 && cp <two modules> lane/plans/sealed50/
cd lane && python3 plans/round50_c1_verify.py --lane . --skip-mutants --allow-dirty --work "$S/countwork"
```

Every git call in the fixtures ran through the lane's `Ctx` (env pinned per child: `GIT_CONFIG_GLOBAL=/dev/null`,
`GIT_CONFIG_NOSYSTEM=1`, fixed author/committer identity and dates) or through `env`-scoped calls in the
probes; nothing exported a git variable into the shell. Fixture writes went only into scratch directories whose
`rev-parse --show-toplevel` was themselves.

## Limits

- The verdict measured is the **base** fence's (`05d5fe03…`), which refuses every `.git` FILE by blanket rule;
  these modules therefore have no measured kill against a *repair* — only against the candidate resolvers in §3,
  which are this seat's own scratch code, not the S2 fence. Their S2 behaviour is unmeasured by construction
  (that is what "blind" means here).
- `gitfile_index_paths` (F1) was exercised directly; the counter's sealed path does not call it, which is why
  the leg is clean. If S2 or S3 adds an identity digest over sealed fixtures, that call site would raise.
- Build determinism: both modules rebuilt into a second tree produce the same per-fixture digest with the
  stat-cache `index` masked (`receipts/driver.out`, `IDENTITY … same=True`); the NUL fixture's digest is a
  local digest because the lane's `tree_identity` raises on it (F1).
- Host sensitivity: the modules pin git 2.56.0 semantics. On a git whose gitfile reader strips a trailing space
  or accepts a second line, the payloads would be a different state — the payloads are literals, so the fixtures
  do not change, but the witness in §1 would.
- Nothing here touches the outside-`d` read property of `plans/round46_c1_verify.py`, the mutant battery, or the
  honest population; io_uring and non-fixture paths are not observed.

## Scratch

`/fast/scratch/hyaku/kengaku-r50/R50C1CritBlind4` (clone, probes, driver, counter work) was removed before this
report was yielded; every output cited above is copied to
`.ufo/waves/round-50/w1/C1CritBlind4/receipts/` (`driver.out`, `matrix.out`, `honest_control.out`,
`probe_gitfile2.out`, `counter.out`).

## Post-yield boundary check: the current lane working-tree fence (`57adce4a…`)

`R50C1ExecRepair` reported (IRC) that `plans/fixture_fence.py` in the live working tree is now
`57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1` (uncommitted, not this seat's write) and asked
for a gitfile-side check. Read-only measurement: the live file copied into scratch, imported, and run on the three
fixtures above, built by the lane builder from a `git clone --shared` at the freeze (`receipts/boundary-vs-live-lane-fence.out`):

```
base_fence_sha 05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
lane_repair_sha 57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
b4a-gitfile-nul-two-stores         base         BREACH  'wt/.git is a file (gitdir redirect), not a directory'
b4a-gitfile-nul-two-stores         lane_repair  BREACH  'wt/.git is a .git file that is not a gitdir line'
b4a-gitfile-newline-two-pointers   base         BREACH  'wt/.git is a file (gitdir redirect), not a directory'
b4a-gitfile-newline-two-pointers   lane_repair  BREACH  'wt/.git is a .git file that is not a gitdir line'
b4b-gitfile-store-include          base         BREACH  'wt/.git is a file (gitdir redirect), not a directory'
b4b-gitfile-store-include          lane_repair  BREACH  'store/config section [include] is not allowlisted'
n21-separate-gitdir                lane_repair  ADMIT   ''
```

So on this class the lane file refuses all three hostile fixtures with a one-line reason and keeps the honest
`n21` admitted — no `ERROR`, no over-refusal, and F1 does not bite it: its `GITFILE` class is
`[^\r\n\x00]+?`, so a NUL/newline payload fails the match and is refused by the parser instead of being resolved.
The store-include fixture is caught by the resolved store's config parser, i.e. the property that module pins is
satisfied by that implementation. **This is a three-fixture boundary check, not a judgement or an endorsement of
`57adce4a…`**: it says nothing about its mount/device leg, its detached-HEAD acceptance, the rest of
`plans/sealed50/`, the mutant floor, or the honest classes it still refuses (`HONEST` was not run here). The
`refs/notes` / non-hex `refs/replace` probes `R50C1ExecRepair` asked for are a different class, not authored or
measured by this seat.

VERDICT: delivered — two blind hostile modules (`c4_gitfile_delimiter.py`: NUL-truncated and two-`gitdir:`-line
pointers; `c4_gitfile_store_include.py`: `[include]` in the gitfile-resolved store's config), 3 fixtures, all
`BREACH` on the base fence with 0 build errors and a clean SEALED wiring, git's divergent resolution witnessed
per fixture, one kill direction witnessed per module against a lenient resolver, and a `strict` resolver that
admits honest `n21` and refuses all three (the modules are passable). The three fixtures also score `BREACH`
(never `ERROR`) on the current lane working-tree fence `57adce4a…`, which keeps honest `n21` admitted. No
production file, no commit, no claim of R50-C1 admission. Instrument defect F1 (`gitfile_index_paths` raises on a
NUL pointer) is handed to the L1.
