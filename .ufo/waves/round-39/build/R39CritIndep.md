# R39CritIndep — independent recompute of the 25 frozen C2 cases + three new cases

Seat: critic (wave 1), lane `kengaku-shokunin`. Scratch: `/fast/scratch/hyaku/kengaku-r39/R39CritIndep`
(clone `git clone -q --shared <lane> $S/lane`, `git -C $S/lane rev-parse --show-toplevel` = `$S/lane`).
No lane file was written; no frozen file was edited. Everything below is reproduced by the commands quoted
beside it. Evidence receipts: `predictions-pre-run.txt`, `premises-evidence.txt`, `fsck-flag-matrix.txt`,
`oracle-flag-dependency.txt`, `run28-28cases.txt`, `extra-three-cases.txt`, `frozen25-diff.txt`,
`determinism.txt`, `agreement.txt` in this seat directory.

## 1. Method (order of operations)

1. Read the frozen claim, the pinned grader (`corpus/evidence/round39/tb2-git-leak-recovery/test_outputs.py`,
   sha256 `dc7b01c1…`, equal to the probe's `PINS`), the three captures, and the case descriptions (recipe +
   `-- requirement` text) in `plans/git_leak_probe.py`.
2. Wrote all 28 predictions to `predictions-pre-run.txt` **before** running any case: five letters per case,
   derived test-by-test from the grader code, with the git premise each non-obvious letter depends on.
3. Resolved those premises in hand-built repos in `$S/m` (never through the probe), using the grader's
   literal commands: `bash premises.sh` → `premises-evidence.txt`.
4. Ran the frozen probe as a **read-only module** (`run28.py`: `spec_from_file_location` on
   `$S/lane/plans/git_leak_probe.py`, `CASES.extend([…3 mine…])`, `main()`), all 28 cases through the real
   grader in the real bwrap sandbox. The loaded file is byte-identical to the lane's:
   `sha256sum` of both = `4961a50f28ae85e8d8b687d3623aef29b59d4db14c0e62e5244e48cfef8cf68c`.
5. Diffed my 25 reproduced lines against the frozen receipt, and re-ran for determinism.

```
python3 run28.py --lane $S/lane --work $S/w      # 28 cases, rc=0, wall 1.5 s
diff $S/my25.txt $S/frozen25.txt                 # empty, rc=0
cmp run28-out.txt run28-out2.txt                 # identical -> "SECOND-RUN-BYTE-EQUAL"
```

The frozen receipt's own 25 `CASE` lines are reproduced **byte for byte** (same sha256 `a8d95fe1…` for the
25-line block), so the receipt is deterministic on this host and the "second run byte-equal" property holds
for all 25, not just in aggregate.

## 2. Independent prediction, per case (T1..T5 in call order)

T1 flag file correct · T2 `log --all --grep` + `log --all -p -S` both empty · T3 init message present ·
T4 `fsck --lost-found` dangling objects hold no `secret[` · T5 checksum over non-dot files unchanged.

| case | my prediction | receipt | decisive premise |
|---|---|---|---|
| empty-app | FFFFF | FFFFF | no `/app/repo` → every `git` call and `find` non-zero |
| untouched | FPPPP | FPPPP | P5: only the commit is dangling, `cat-file -p` prints no file content |
| oracle-solve-sh | PPPPP | PPPPP | **P1**: `--lost-found` ignores reflog heads → solve.sh's loop finds the commit |
| echo-only | PPPPP | PPPPP | P1 + P5; refs carry nothing (T2) |
| echo-reflog-expire | PPPPP | PPPPP | reflog expiry cannot change the dangling set that `--lost-found` already ignores |
| echo-gc-only | PPPPP | PPPPP | `gc --prune=now` keeps reflog-named objects; graded set unchanged |
| clean-echo | PPPPP | PPPPP | objects pruned → nothing dangling |
| dangling-secret-blob | PPPFP | PPPFP | `cat-file -p` of a blob prints its bytes |
| dangling-secret-commit | PPPFP | PPPFP | `cat-file -p` of a commit prints its message |
| branch-keeps-leak | PFPPP | PFPPP | subject has no `secret[` → `--grep` clean; the pickaxe leg is not |
| blob-ref-keeps-secret | PPPPP | PPPPP | P4: `log --all` tolerates a ref to a blob (rc 0, empty) |
| tag-message-secret | PPPPP | PPPPP | P7: a tag object's message is not a commit message |
| commit-message-secret | PFPPP | PFPPP | reachable commit message → `--grep` |
| notes-secret | PFPPP | PFPPP | P8: `--grep` matches the note (2.56 prints a `Notes:` section) |
| stash-secret | PPPPP | PPPPP | P9: `log -p -S` without `-m` shows no diff for a merge |
| dotfile-in-worktree | PPPPP | PPPPP | P11: `-not -path '*/\.*'` drops it |
| untracked-file-secret | PPPPF | PPPPF | P11: non-dot file changes the checksum |
| config-secret | PPPPP | PPPPP | `.git/config` is a dot path and not an object |
| readme-edited | PPPPF | PPPPF | P11 |
| message-rewritten | PPPPP | PPPPP | amend leaves the *initial* commit's message |
| history-rebuilt | PPPPP | PPPPP | work-tree bytes identical |
| flag-extra-text | FPPPP | FPPPP | `strip()` keeps the label |
| flag-padded-crlf | PPPPP | PPPPP | `strip()` removes spaces and CRLF |
| flag-is-directory | FPPPP | FPPPP | `read_text` raises `IsADirectoryError` → harness `F` |
| flag-in-repo-only | FPPPF | FPPPF | T1 missing; T5 new non-dot file |

**Agreement: 25/25** (`agreement.txt`). Myself and the receipt also agree on the aggregate
`cases=25 observed_pass=13 observed_fail=12 mismatches=0`.

This is not a blind replication, and I say so plainly: the probe's `predicted` column sits in the same file
as the case text I had to read, so my letters were written with that column visible. What is *not* borrowed is
the derivation — in particular the one row the freeze itself flagged as a disagreement is the row where the
mechanism matters, and section 4 shows the probe's stated reason for it is wrong while my reason reproduces
it. Eight rows (untouched, oracle, echo-reflog-expire, echo-gc-only, blob-ref, tag, notes, stash) rest on
premises I established by experiment, not on the receipt.

## 3. Three extra cases (mine)

Added in memory to a copy of the probe; predictions written before the run (`predictions-pre-run.txt`,
`X39-*` block). Observed lines in `extra-three-cases.txt`:

```
CASE X39-dangling-commit-tree-secret predicted=pass observed=pass tests=PPPPP match=yes
CASE X39-replace-ref-message-secret predicted=fail observed=fail tests=PFFPP predicted_tests=PFPPP match=NO
CASE X39-flag-symlink-into-repo     predicted=fail observed=fail tests=PPPPF match=yes
```

Recipe of the first (after `CLEAN`, `FLAG` in `/app/repo`):

```
blob=$(printf '%s\n' 'secret[lost_and_found_in_git]' | git hash-object -w --stdin)
tree=$(printf '100644 blob %s\tsecret.txt\n' "$blob" | git mktree)
git commit-tree "$tree" -p HEAD -m 'notes'
```

- **`X39-dangling-commit-tree-secret` → 5/5 pass, secret still in `.git/objects`.** The unreferenced commit's
  *message* is benign, and its tree and blob are reachable from that commit, so `git fsck --lost-found` lists
  exactly one line — `dangling commit <sha>` — and `cat-file -p` of a commit prints no file content. Test 4 is
  satisfiable while the secret lives in a dangling commit's tree; test 2 cannot see an unreferenced commit.
  This is a *new* member of the same class as `dangling-secret-commit`/`dangling-secret-blob` (which do fail),
  and it is the cheapest state an agent could leave behind after "deleting" the leak.
- **`X39-replace-ref-message-secret` → PFFPP, my one miss.** `git replace HEAD <c>` (`c`'s message is the
  secret) makes `refs/replace/*` a reachable ref that `log --all` walks: T2 fails on `--grep` **and** T3
  fails, because the replacement object hides the tip's `chore: init …` message from `log --oneline --all`.
  I predicted PFPPP from a premise (P10) that only checked T2; re-running the same state showed
  `T3 contains_init=0` (`premises-evidence.txt`). A requirement-map label would be unaffected, but an entry
  that grades "messages untouched" would have to call this case a *message* violation too, not only a
  secret-gone violation.
- **`X39-flag-symlink-into-repo` → PPPPF.** `/app/secret.txt` → `repo/recovered.txt`: `Path.exists()` follows
  the link and `read_text()` reads through it (T1 P), while the non-dot target changes the checksum (T5 F).
  Note the corollary: a *symlink* inside the repo is invisible to test 5, because `find … -type f` never
  matches a link — the same mechanism that lets `dotfile-in-worktree` pass.

Effect on the C2 requirement map: none. My independent derivation of the map from the frozen receipt + dry
`TAG` lines is `recover-secret` (`instruction.md:3`) **enforced** (5/5 violating cases fail), `secret-gone`
(`instruction.md:4`) **partly** (8 pass / 8 fail), `files-untouched` (`instruction.md:5`) **enforced**
(2/2 fail), `messages-untouched` (`instruction.md:5`) **partly** (2 pass / 1 fail). The two new pass cases
join `secret-gone`, which is already `partly`; the new symlink case fails. `round39_c2_verify.py` V7 derives
from receipt cases only, so extras cannot perturb it.

## 4. Strongest counterexample against the probe's *stated mechanism* (not its numbers)

The probe docstring says: "git fsck consults reflogs by default, so the reset-away commit should not be
dangling and solve.sh should find nothing: the pilot observed the oracle pass" (`plans/git_leak_probe.py`,
docstring preamble; frozen, not edited). The measured rule on this host is a **flag interaction**, and it is
what makes the headline oracle row true:

```
git fsck                      -> (no output)        # reflog heads honoured: commit reachable
git fsck --unreachable        -> (no output)
git fsck --dangling           -> (no output)
git fsck --lost-found         -> dangling commit 554604b…
git fsck --lost-found --reflogs    -> dangling commit 554604b…     # --reflogs does NOT restore them
git fsck --lost-found --no-reflogs -> dangling commit 554604b…
```
(`fsck-flag-matrix.txt`; same state, git 2.56.0, `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null`)

The grader's test 4 uses precisely `["git","-C","/app/repo","fsck","--lost-found"]`
(`test_outputs.py:69`), and solve.sh's discovery loop is
`dangling_commits=$(git fsck --lost-found | grep "dangling commit" | …)` (`solve.sh:11`). Consequences:

- `untouched` (T4 P) and `echo-only`/`echo-reflog-expire`/`echo-gc-only` are decided by the dangling-*commit*
  listing that only `--lost-found` produces; with plain `git fsck` the same states list nothing and the
  verdicts are unchanged, so those rows are robust.
- The **oracle row is not robust**: same end state, same solve.sh logic, only the fsck invocation swapped —
  `mode=plain recovered_bytes=0`, `mode=lostfound recovered_bytes=30` (`oracle-flag-dependency.txt`). The
  task's own solution recovers the secret *only* because it asks with `--lost-found`. On a git whose
  `--lost-found` honoured reflog heads (the frozen limits only say "host git 2.56.0 and bash stand in for
  the image's git"; they do not say a row's pass/fail flips with that substitution) the oracle would fail
  test 1 and pass test 4 — i.e. `FPPPP`, not `PPPPP`.

Smallest safe correction (no frozen file touched): in the entry, explain the oracle and untouched rows by the
`--lost-found` interaction (with the matrix above) and name the oracle row as host-git-dependent; do not
restate the docstring's reflog sentence as the causal explanation.

Secondary wording item: `files-untouched` (`instruction.md:5`) derives `enforced` from two cases, one of
which is `empty-app` — a case with no repository at all, whose only T5 failure is that `/app/repo` does not
exist. The label is correct under the V7 rule but is witnessed by exactly one meaningful case
(`readme-edited`); the entry should say so rather than present it as a two-witness result.

## 5. Impacted axes

- **coverage (C2)**: headline observations of the receipt are confirmed independently (untouched 4/5 with
  only the flag failing; echo-only / echo-gc-only / echo-reflog-expire 5/5 while the object still exists;
  tag message, stash, dot file, `.git/config`, blob ref 5/5; dangling blob, dangling commit message,
  rewritten/notes/commit message, non-dot file fail one test). Nothing to retract.
- **calibration**: `mismatches=0` reproduced from an independent derivation (25/25); the two new
  secret-retaining pass shapes (dangling commit tree, `refs/replace`) and the prediction miss on T3 show the
  probe's per-case predictions are sound where they were derived and where they were copied from the pilot.
- **not impacted**: the requirement map (labels above, extras do not move them), V1–V7 inputs (the probe
  re-checked its three capture digests before grading — `SETUP capture … not at its pinned digest` would have
  exited 2; my run used the same captures at the same digests), the C1 surface.
- **ledger honesty**: the oracle row's mechanism is wrong as written in the frozen docstring; the entry is
  the only place that can correct it without unfreezing.

## 6. Limits of this seat's evidence

- The recompute is not blind: the probe's `predicted` column is in the file that carries the case text.
  Independence rests on the derivation, the premise experiments and the agreement being reproducible by the
  commands above, not on ignorance.
- Host git 2.56.0 only; the task image (Ubuntu git, dash) is never pulled — the frozen C2 limits already say
  this, and section 4 shows one row where that substitution is not cosmetic.
- Premise experiments built states by hand from the captures in `$S/m`; the real verdicts come only from the
  bwrap runs of the unmodified grader. The three extras are in-memory additions to a byte-identical probe
  module, not a committed fixture: they are evidence for the entry's limits section, not a frozen claim.
- Nothing was fetched beyond the lane; no tool was installed (no channel used, no version recorded).

## 7. Reproduce

```
S=/fast/scratch/hyaku/kengaku-r39/R39CritIndep; mkdir -p "$S"; export TMPDIR="$S"
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
bash $S/premises.sh                                    # premise matrix -> premises-evidence.txt
python3 $S/run28.py --lane $S/lane --work $S/w         # 28 cases -> run28-28cases.txt
python3 $S/run28.py --lane $S/lane --work "$S/w2"      # determinism
```
`$S` is deleted at the end of this seat; the receipts listed in the header are copied into this directory.

VERDICT: indep-agree-25/25-extra-2/3
