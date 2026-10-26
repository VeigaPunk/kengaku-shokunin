# R39CritFsckReflog — why `oracle-solve-sh` passes and `untouched` is FPPPP, not FFFFF

Seat: critic (round 39 wave 1, kengaku). Scope: the two receipt rows `untouched` and
`oracle-solve-sh` of `corpus/evidence/round39/git-leak-probe.txt`, against the probe docstring's
static reading ("git fsck consults reflogs by default, so the reset-away commit should not be
`dangling` and solve.sh should find nothing"). Everything below is measured on a fixture built
from the frozen capture `corpus/evidence/round39/tb2-git-leak-recovery/challenge-setup.sh` in my
own scratch, plus the git sources/docs at the two relevant tags, plus a real Ubuntu 24.04 /
git 2.43.0 container (docker was already usable without root: server 29.9.1, user in `docker`).

## 0. Answer

The static reading is correct about **bare** `git fsck` and wrong about the command the grader and
the oracle actually run. `--lost-found` is not a display option: it silently sets
`include_reflogs = 0` (`builtin/fsck.c`, v2.56.0:905-908 / v2.43.0:950-953). With reflogs as heads
the reset-away secret commit is reachable and `git fsck` prints nothing; with `--lost-found` the
same commit is `dangling` and the secret is findable. `tests/test_outputs.py` test 4 and
`solution/solve.sh` both use `--lost-found`, which is why `untouched` fails only the flag test
(FPPPP) and the oracle passes 5/5 (PPPPP). Nothing in the receipt changes.

## 1. Fixture

```
S=/fast/scratch/hyaku/kengaku-r39/R39CritFsckReflog ; export TMPDIR="$S"
D=$(mktemp -d -p "$S") ; cp <capture>/challenge-setup.sh "$D/app/"
cd "$D/app" && GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null bash ./challenge-setup.sh
```

`challenge-setup.sh` (19 lines) does: `chore: init` commit -> `secret[lost_and_found_in_git]` into
`secret.txt` -> `feat: add scratch notes` commit -> `git reset --hard HEAD~1` -> README edit ->
second `chore: init` commit. Resulting objects (identical ids on host 2.56 and in the 2.43
container, because the commit/reflog timestamps are baked in by the setup):

| object | id | role |
|---|---|---|
| commit 1 | `3b1a11f71d8ed00e7e4bb36d297cc0d120c5a728` | `chore: init …` (still on `master`) |
| commit 2 | `ca8f07040d38fd6b0cf814f1f31d04cc01010a3a` | `feat: add scratch notes` — **the secret commit**, reset away |
| commit 3 | `871437429cf2b4690b6183d2a59b8645fcab3223` | second `chore: init …` (tip) |
| tree of commit 2 | `aa7dfd0c18e6582cdc8959609bc02653870cd96a` | holds `secret.txt` |
| blob `secret.txt` | `52d18a091cd9755bacb8eaccab2882a24b080dc7` | content `secret[lost_and_found_in_git]` |

`.git/logs/HEAD` (4 lines, all ts 1792997493; `date +%s` = 1792997536, so nothing is "in the
future"):

```
0000… 3b1a11f7 …  commit (initial): chore: init e665d1a2-04a7-4e61-b523-e897e231d9cc
3b1a11f7 ca8f0704 …  commit: feat: add scratch notes          <- reflog keeps the secret commit
ca8f0704 3b1a11f7 …  reset: moving to HEAD~1
3b1a11f7 87143742 …  commit: chore: init e665d1a2-04a7-4e61-b523-e897e231d9cc
```

`.git/logs/refs/heads/master` carries the same four lines. `git fsck --verbose 2>&1 | grep -c
"Checking reflog"` -> `8`.

## 2. The six fsck invocations (host git 2.56.0, same fixture)

```
$ git fsck                        -> (no output)  rc=0
$ git fsck --unreachable          -> (no output)  rc=0
$ git fsck --lost-found           -> dangling commit ca8f07040d38fd6b0cf814f1f31d04cc01010a3a
$ git fsck --no-reflogs           -> dangling commit ca8f07040d38fd6b0cf814f1f31d04cc01010a3a
$ git fsck --unreachable --lost-found
    unreachable tree aa7dfd0c18e6582cdc8959609bc02653870cd96a
    unreachable commit ca8f07040d38fd6b0cf814f1f31d04cc01010a3a
    unreachable blob 52d18a091cd9755bacb8eaccab2882a24b080dc7
$ find .git/lost-found -type f -> .git/lost-found/commit/ca8f07040d38fd6b0cf814f1f31d04cc01010a3a
```

`--lost-found` and `--no-reflogs` produce the same verdict on this repo, and `--lost-found` also
implies `--full`. So the probe's static reading describes rows 1-2 of the table and the grader's
command is row 3.

## 3. Which object is dangling, and why only the commit

`git show ca8f0704` prints `+secret[lost_and_found_in_git]` (the tree `aa7dfd0c` lists `README.md`
+ `secret.txt`; blob `52d18a09` is the literal). `fsck` calls the commit dangling and the tree/blob
merely unreachable because of the `USED` rule: with `show_unreachable` off, only unreachable
objects that *nothing points at, including other unreachable objects*, are printed as
`dangling` (v2.56.0 `check_unreachable_object`, builtin/fsck.c:269-330: `show_unreachable` branch
first, then `if (!(obj->flags & USED))`). The dangling commit's own walk marks its tree and blob
`USED`, so they are suppressed unless `--unreachable` is given. Practical consequence for the
corpus entry: `--lost-found` alone never hands the grader a blob, so `cat-file -p` of the dangling
commit shows header + `feat: add scratch notes` and *no* secret — the leak test on the initial
state passes even though the secret blob is still on disk.

## 4. Provenance (git source + docs)

| claim | source |
|---|---|
| reflogs are heads by default | https://github.com/git/git/blob/v2.56.0/Documentation/git-fsck.adoc#L26-L28 ("…and all reflogs (unless --no-reflogs is given) as heads"); same at v2.43.0 `Documentation/git-fsck.txt#L26-L28` |
| `--no-reflogs` = ignore commits referenced only by a reflog entry | v2.56.0 adoc#L49-L53; v2.43.0 txt#L48-L52 |
| `--lost-found` description says nothing about reflogs | v2.56.0 adoc#L89-L92; v2.43.0 txt#L88-L92 — the implication is **undocumented**, and no test in `t/t1450-fsck.sh` at either tag mentions `--lost-found` (grep) |
| default `include_reflogs = 1` | v2.56.0 builtin/fsck.c:35; v2.43.0 builtin/fsck.c:43 |
| `--lost-found` clears it | v2.56.0 builtin/fsck.c:905-908 (`if (write_lost_and_found) { odb_fsck_opts.flags |= ODB_FSCK_FULL; include_reflogs = 0; }`); v2.43.0 builtin/fsck.c:950-953 (`check_full = 1; include_reflogs = 0;`) |
| reflog entries mark objects reachable | v2.56.0 builtin/fsck.c:483-496 (`fsck_handle_reflog_ent` -> `fsck_handle_reflog_oid(ooid,0)` / `(noid,ts)`); v2.43.0 builtin/fsck.c:477-513 (same, without the future-timestamp gate) |
| v2.56-only: reflog entries with `timestamp > now` are skipped | v2.56.0 builtin/fsck.c:485-486 — not triggered here (reflog ts 1792997493 < now 1792997536), but it is a portability footnote for clock-skewed fixtures |

## 5. Row reconciliation (measured, not argued)

bwrap sandbox as the probe builds it, `/app` = a scratch copy of the setup, grader
`test_outputs.py` imported and its five functions called in file order:

```
--- untouched (fresh copy)      TESTS FPPPP     (test 1 only: no /app/secret.txt)
--- oracle-solve-sh (solve.sh)  TESTS PPPPP
--- post-oracle: git fsck       rc=0, no output ; .git/logs/HEAD 0 bytes
```

`solve.sh` output: `Found in: ca8f0704…` / `Secret: secret[lost_and_found_in_git]`, then
`reflog expire --expire=now --all` + `gc --prune=now --aggressive`, which prunes the dangling
commit — hence test 4 is clean afterwards and the reflog file is empty. Both letters match the
frozen receipt rows exactly (`untouched FPPPP`, `oracle-solve-sh PPPPP`).

## 6. Ubuntu 24.04 / git 2.43

The task image is `FROM ubuntu:24.04` + `apt-get install -y git` (capture `Dockerfile:3,7`), and
noble ships git **2.43.0** (`1:2.43.0-1ubuntu7.x`, https://launchpad.net/ubuntu/noble/+source/git).
The load-bearing line is byte-for-byte the same at that tag (builtin/fsck.c:950-953), and the docs
at 2.43.0 say the same thing (txt:26-28, 88-92). Empirically, `docker run ubuntu:24.04` (image
digest `sha256:68ee2204…aff33ac`, apt git 2.43.0, no task image pulled):

```
git version 2.43.0
--- plain fsck               (no output, rc=0)
--- lost-found               dangling commit ca8f07040d38fd6b0cf814f1f31d04cc01010a3a
--- no-reflogs               dangling commit ca8f07040d38fd6b0cf814f1f31d04cc01010a3a
--- unreachable+lost-found   unreachable tree aa7dfd0c… / commit ca8f0704… / blob 52d18a09…
--- solve.sh                 Found in: ca8f0704… / Secret: secret[lost_and_found_in_git] / SUCCESS
--- /app/secret.txt          secret[lost_and_found_in_git]\n
--- post fsck --lost-found   (no output) ; .git/logs/HEAD 0 bytes
--- grader                   untouched FPPPP ; oracle PPPPP
```

A second run let **2.43 create the repo itself** inside the container (`bash challenge-setup.sh`,
then `git fsck`): plain `fsck` silent, `git fsck --lost-found` -> `dangling commit
ac400e2e7bebc8a11f563cfd6566a5e8bbc9b67d`, solve.sh recovers the secret, post-solve `fsck` silent.
So the split is old and version-independent: the same construct exists at v2.0.0 (builtin/fsck.c:
642-645, `include_reflogs = 0`). No Ubuntu patch touches this path (Ubuntu carries 2.43.0 upstream
code; the container is the check).

## 7. Impact on frozen round-39 artifacts

- **No receipt row changes.** All 25 rows keep their observed verdicts; only the *narrative* of two
  rows was wrong about *why*. `predicted_tests` strings, `violates=` tags, requirement map and
  C2 counter V7 labels are untouched.
- The probe (`plans/git_leak_probe.py`, frozen) keeps its docstring sentence; the correction belongs
  in the corpus entry (and the round-39 lesson), not in a frozen file. Also note the docstring's
  sentence is true of bare `fsck` — the miss is that it inferred from `fsck`, not from
  `fsck --lost-found`.
- No new authority is introduced: nothing here re-decides the gate, the spec, or the mutants.

## 8. Draft entry paragraph for the L1 (3 sentences, paste as-is)

> `git fsck` treats every reflog entry as a head by default, so the reset-away `feat: add scratch
> notes` commit is reachable and a bare `git fsck` prints nothing on the task's initial state; but
> `--lost-found` also clears `include_reflogs` (builtin/fsck.c:905-908), which is exactly the flag
> both `tests/test_outputs.py::test_no_secrets_in_unreachable_objects` and `solution/solve.sh` pass,
> so the same commit prints as `dangling commit ca8f0704…`. That flag split explains both rows:
> `untouched` scores FPPPP because only the missing `/app/secret.txt` fails (the dangling commit's
> `cat-file -p` output holds no secret — its tree and blob are `USED`, hence not "dangling"), while
> the oracle scores PPPPP because solve.sh reads that commit, `git show` prints the secret from its
> tree, and `reflog expire --expire=now --all` + `gc --prune=now` then prunes it. Ubuntu 24.04's git
> 2.43.0 carries the identical line (builtin/fsck.c:950-953) and reproduced every step, so this is
> not a host-git artefact.

## 9. Critic return

- **Counterexample to the static reading:** the same repo, same git, no mutation — `git fsck` is
  silent while `git fsck --lost-found` reports `dangling commit ca8f0704…` (§2). The variable is
  the flag, not the repository state.
- **Second counterexample to any "fsck sees the blob" reading:** `--lost-found` alone never emits
  the secret blob; only `--unreachable` does (§3). So a detection rule built on `--lost-found`
  output cannot see a reachable-only-through-an-unreachable-commit blob.
- **Impacted axes:** (1) row explanation / entry correctness for C2; (2) provenance of the corpus
  entry's claim about the grader; (3) portability to the task image's git; (4) frozen-artifact
  integrity. (1)-(3) improve; (4) unchanged — no frozen file was or needs to be touched, and no
  receipt number moves.
- **Smallest safe correction:** keep every frozen artifact as is; in the corpus entry
  `corpus/knowledge/tb2-git-leak-recovery-grader.md` state the `--lost-found` ⇒ `--no-reflogs`
  implication (undocumented in `git-fsck.adoc:89-92`) as the reason the initial repo passes the
  leak test and the oracle passes all five, and drop the probe docstring's inference as an
  explanation of the rows. If a future round re-freezes the probe, replace "static reading says
  fsck honours reflogs so nothing is dangling" with "a bare `fsck` sees nothing; `--lost-found`
  turns reflog heads off and the commit is dangling".

## 10. Hygiene / tooling

- Scratch: `/fast/scratch/hyaku/kengaku-r39/R39CritFsckReflog` (fixtures, fetched sources, t1450);
  removed before finishing. No clone of the lane was written by this seat and no lane file was
  touched (write scope: this report only).
- Tooling: no host install. `docker` already usable without root (29.9.1); pulled
  `ubuntu:24.04` (`sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac`),
  `apt-get install -y git python3` inside ephemeral containers only (git 2.43.0, Python 3.12.3).
  Fetched read-only `builtin/fsck.c`, `Documentation/git-fsck.txt|.adoc`, `t/t1450-fsck.sh` at
  v2.0.0/v2.43.0/v2.56.0 from raw.githubusercontent.com.
- `corpus/knowledge/…` was not created; integration is the L1's.

VERDICT: fsck-reflog-explained
