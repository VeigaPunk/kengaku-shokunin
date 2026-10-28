# R50C1ExecPopRepro — population pin reproduction (kengaku r50, w1)

Seat: `R50C1ExecPopRepro` (executor), serving **R50-C1** (novelty), item: reproduce the 126-fixture
honest-population pin three times at the freeze tree.

REV measured: `3b02d573d58cc6d2e0d27ef92ac0815354912252` (round-50 stage-1 freeze). Verified ancestor of the
lane tip before any measurement: `git merge-base --is-ancestor 3b02d57… HEAD` → yes (live lane HEAD at read
time `5c56819f7964f4af19c960de08a49cd8f95781ce`; the live checkout was **not** used for any build — all runs
were against a `git clone --shared` detached at `3b02d57`).

## Axes named

1. **A1 — run-to-run byte identity** of the rebuilt `population.txt` (three independent builds A/B/C).
2. **A2 — identity of the rebuilt population against the committed pin** (`b5197f94…`): file bytes, HONEST
   rows, `identity.jsonl`, `modules.sha256`, per-fixture receipts.
3. **A3 — fixture-set integrity**: 126 fixtures, unique canonical tree digests, per-population counts,
   determinism across `--repeats 2`, `CHECKS` clean.
4. **A4 — parallelism independence**: rebuild at a different `--jobs` value (supplementary run J, `--jobs 3`).
5. **A5 — pin regenerability**: is `b5197f94…` reachable from any *committed* tree, and do the header's
   self-describing fields (`lane=`, `builder_sha256=`) name committed objects?

## Instrument digest checks at the freeze tree (pre-measurement)

```
b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69  plans/honest50/population.txt
35e3de6059e4676133291c615fdac7b04342e7c43827ec1e70ac09f83267a70b  plans/honest50/build_honest_population.py
f9b9873e602dd09228d0164412d450b2cef95c3055ce9347fa05b9377637bd76  plans/round50_c1_verify.py
05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  plans/fixture_fence.py
6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad  plans/round44_c1_verify.py
```
All four frozen digests match `plans/round-50-claims.md` verbatim; the clone at `3b02d57` was clean
(`git status --porcelain` empty) before and after every run.

## Exact commands run

Scratch root `S=/fast/scratch/hyaku/kengaku-r50/R50C1ExecPopRepro`, `TMPDIR=$S`; clone:
```
git clone --shared --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" checkout --detach 3b02d573d58cc6d2e0d27ef92ac0815354912252
git -C "$S/lane" rev-parse --show-toplevel   # → /fast/scratch/.../R50C1ExecPopRepro/lane
```
Per run (A, B, C launched concurrently as three separate processes; J supplementary):
```
env TMPDIR="$S" python3 "$S/lane/plans/honest50/build_honest_population.py" \
  --lane "$S/lane" --modules "$S/lane/plans/honest50/modules" \
  --out "$S/run$r" --work "$S/w" --jobs 8 --repeats 2
```
(`runJ` identical except `--jobs 3`; each process makes its own `mkdtemp` under `$S/w`, so the three
concurrent A/B/C builds never share a fixture directory.)

## Observed output — the three POPULATION lines (verbatim)

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
POPULATION population.txt sha256=ca435f6817ee0e351bf63897726049f11d31bc3207ae5cc9ff4890837d9dbd11 fixtures=126
MODULE-MANIFEST modules.sha256 sha256=1599e56bed2c9f08f7323ad6ffc6431cc8332b4f7b7d2e29040a0c780b571fb9 modules=44
BUILDER build_honest_population.py sha256=35e3de6059e4676133291c615fdac7b04342e7c43827ec1e70ac09f83267a70b
COUNTS battery42=29 battery43=42 battery44=33 r46novel=9 novel48=7 novel49=4 novel50=2
CHECKS all-ok
PREDICATE POPULATION ok
```
Identical for **runA, runB and runC** (`DURATION seconds=21.2 / 21.1 / 21.4`, `EXIT_A=0`, `EXIT_B=0`,
`EXIT_C=0`; supplementary `runJ --jobs 3`: same POPULATION line, `DURATION seconds=21.4`, `EXIT_J=0`).

`GUARD` lines (A, verbatim):
```
GUARD base-fence-ok plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
GUARD builder-ok plans/round44_c1_verify.py sha256=6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad
GUARD lane-rev-ok 3b02d573d58cc6d2e0d27ef92ac0815354912252
HOST git=git version 2.56.0 python=3.14.8 platform=Linux-7.2.11-arch1-1-x86_64-with-glibc2.44
```
`--assert-base` was left ON (default). Note the round-50 amendment is in force: the guard checks the base
fence + pinned `round44_c1_verify.py`, **not** lane HEAD, so the builder runs at the r50 freeze tree.

## A1 — run-to-run byte identity: PASS

```
ca435f6817ee0e351bf63897726049f11d31bc3207ae5cc9ff4890837d9dbd11  runA/population.txt
ca435f6817ee0e351bf63897726049f11d31bc3207ae5cc9ff4890837d9dbd11  runB/population.txt
ca435f6817ee0e351bf63897726049f11d31bc3207ae5cc9ff4890837d9dbd11  runC/population.txt
runA==runB (cmp), runA==runC (cmp), runJ==runA (cmp) → JOBS-INDEPENDENT
```
`population.sha256` written by each run: `ca435f68…  population.txt` (A, B, C, J).

## A3 — fixture-set integrity: PASS

`fixtures=126`; per-population `battery42=29 battery43=42 battery44=33 r46novel=9 novel48=7 novel49=4
novel50=2` (= 104 battery + 22 novel, matching the frozen composition). 126 `IDENTITY … deterministic=1`
rows and 0 `deterministic=0`; 126 distinct `tree_sha256` values (no duplicate identity); 0 `BUILD-FAIL` /
`Traceback` / `SETUP` in any of the four logs; `CHECKS all-ok` and `PREDICATE POPULATION ok` in A, B, C and J.

## A2 — identity against the committed pin: content PASS, file bytes FAIL

```
=== HONEST rows A vs PIN ===
ROWS-IDENTICAL            (cmp runA HONEST rows  lane/plans/honest50/population.txt HONEST rows)
=== identity.jsonl A vs PIN ===
IDENTITY-IDENTICAL        (cmp, 126 lines each)
=== modules.sha256 A vs PIN ===
MODULES-IDENTICAL
=== receipts tree diff ===
(count: 0)                (diff -rq runA/receipts lane/plans/honest50/receipts → no differences)
```
But the **file** does not reproduce:
```
runA/population.txt lane/plans/honest50/population.txt differ: char 43, line 2
=== count of differing lines ===
2            (diff counts one < and one > for the single changed line)
diff:
< # lane=3b02d573d58cc6d2e0d27ef92ac0815354912252 builder_sha256=35e3de6059e4676133291c615fdac7b04342e7c43827ec1e70ac09f83267a70b base_fence_sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e builder_tree=plans/round44_c1_verify.py@6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad
> # lane=71f5f5f77591d8c3d19297ee9785436da45209e4 builder_sha256=b2560ebc9c9d1451c47c89039868f4f60d440cd1fa52b92f00baf6d0324a8002 base_fence_sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e builder_tree=plans/round44_c1_verify.py@6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad
```
Replacing line 2 in both files makes them byte-identical (`ALL-OTHER-LINES-IDENTICAL`); both files are 20702
bytes (the two changed fields are fixed-width hex, so the length is unchanged). Therefore:

- rebuilt `population.txt` = `ca435f68…`, **not** the frozen pin `b5197f94…`;
- the whole of the difference is line 2's two self-describing fields: `lane=` (measured rev) and
  `builder_sha256=` (the builder's hash of its own file).

## A5 — pin regenerability: FAIL (root cause, evidenced)

```
# builder_sha256 named by the pin header exists nowhere in the repository
git cat-file -t b2560ebc9c9d1451c47c89039868f4f60d440cd1fa52b92f00baf6d0324a8002
  → fatal: Not a valid object name …

# per-commit digest of plans/honest50/build_honest_population.py
71f5f5f  ABSENT (path does not exist at the rev the pin header names)
f7281bc  35e3de60…      ← stage-1 commit (first commit carrying the builder)
3b02d57  35e3de60…      ← freeze
5c56819f 35e3de60…

git log --oneline --all -- plans/honest50/build_honest_population.py
  → 007a4a5 (empty subject; jj prevent-loss snapshot, single parent 71f5f5f, NOT an ancestor of HEAD)
  → f7281bc round-50: stage-1 freeze …
git log --oneline --all -- plans/honest50/population.txt
  → 007a4a5, f7281bc   (both refs carry the same population blob content, sha256 b5197f94…)

# the untracked working-copy snapshot 007a4a5 already holds the FINAL builder, at the pinned population
git show 007a4a5:plans/honest50/build_honest_population.py | sha256sum → 35e3de60…
git show 007a4a5:plans/honest50/population.txt             | sha256sum → b5197f94…
```
So the pin was generated from a **builder draft (`b2560ebc…`) that was never committed**: by the time the
working copy was snapshotted (`007a4a5`, 2026-10-28 14:15:28, parent `71f5f5f`) the builder had already been
edited to `35e3de60…`, while `population.txt` was left as generated. The pin *constant* and the *committed
file* agree (`b5197f94…` in `f7281bc`, `3b02d57`, the working tree and the jj snapshot), but the file is a
receipt of one authoring session, not a function of any committed tree: no committed builder can emit it.

**Impact on the counter (read from source, not executed by this seat).** `plans/round50_c1_verify.py`
lines 183–204: `pop_sha = sha256_file(pop_path)` compares the **committed file's** bytes to the literal
`POPULATION_SHA` (line 66, `b5197f94…`) — at the freeze tree that passes by construction — and `mismatched`
compares each rebuilt `tree_identity` to the pinned **row** `tree`. Both rebuilt halves are proven identical
above (HONEST rows and identity.jsonl), so the header drift cannot fail the POPULATION leg. These are
[INFERENCE] from the counter source; this seat did not run the counter or the fence (other seats' items).

## Limits

- One host, one toolchain: git 2.56.0, Python 3.14.8, Linux-7.2.11-arch1-1; the claims already declare
  fixture identity host-sensitive where git output is.
- Only the population builder was executed. No fence, counter, refusal or mutant leg was run here; the
  C1 predicate is not measured by this seat, and no admission of R50-C1/C2 is claimed.
- The byte-level comparison is against the pin as committed at `3b02d57`; the live checkout's working tree
  was never read for builds (three other seats' uncommitted edits were present there).
- The exact header bytes cannot be reproduced at **any** committed revision: `builder_sha256` is fixed by
  the file's own content (`35e3de60…`) and `lane=` by the checked-out rev. `b5197f94…` is unreachable by
  construction, so a future mechanical "does the pin reproduce?" gate will always report drift.

## Defect report for the L1 (drift, not a re-pin)

1. **Header field `builder_sha256=b2560ebc…` in `plans/honest50/population.txt` cites a builder blob that is
   absent from the object database** (no ref, no commit, no reachable object carries it) and contradicts the
   frozen instrument digest in `plans/round-50-claims.md` (`35e3de60…`). The header's `lane=71f5f5f…` likewise
   names a tree in which the builder does not exist. Both are consequences of generating the pin from the
   pre-commit working copy before the builder's last edit (the jj prevent-loss snapshot `007a4a5` shows the
   final builder sitting beside the already-pinned, never-regenerated `population.txt`).
2. **The population *content* is frozen and fully reproduced**: 126 fixtures, 126 unique identities, 104+22
   composition, `CHECKS all-ok`, `deterministic=1` for all 126, byte-identical across three concurrent builds
   and a different `--jobs`. The drift is confined to `population.txt` line 2 and does not touch any `HONEST`
   row, `identity.jsonl`, `modules.sha256` or per-fixture receipt.
3. Because the counter checks the committed file's bytes against the literal (not a rebuild), the drift is
   cosmetic **for the predicate** but leaves the pin un-regenerable and mis-attributed. The open-window rule
   covers "an unreproducible fixture"; this is not a fixture failure, so whether to repair the header
   (which changes the pin and therefore the frozen predicate inputs) is an L1/claim decision, not this
   seat's. Recommended, if repaired inside the window: record old→new digest in the claims file and state
   that the pin line 2 is authoring metadata, not identity; do **not** silently re-pin.

## Scratch

`/fast/scratch/hyaku/kengaku-r50/R50C1ExecPopRepro` (lane clone, `runA|runB|runC|runJ`, `w/`) was removed
before this seat yielded; every citable value is transcribed above. The lane checkout was not modified
(`git -C clone status --porcelain` empty after all runs; no commits, no mutating git).

VERDICT: population content reproduced exactly (126/126 identities, three runs byte-identical, `CHECKS all-ok`,
exit 0); frozen file pin `b5197f94…` NOT reproduced — one header line differs (`ca435f68…`), root cause
evidenced (self-hashing builder generated from an uncommitted working copy at `71f5f5f`); reported as a defect,
not re-pinned.
