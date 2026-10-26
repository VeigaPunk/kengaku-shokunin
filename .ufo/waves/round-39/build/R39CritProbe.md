# R39CritProbe — attack on the frozen `git-leak-recovery` probe (round 39, wave 1)

Target: `plans/git_leak_probe.py` (frozen), its receipt `corpus/evidence/round39/git-leak-probe.txt`, the frozen dry
table `corpus/evidence/round39/git-leak-dry-cases-freeze.txt`, the seven captures in
`corpus/evidence/round39/tb2-git-leak-recovery/`, judged against `instruction.md` and the requirement map rule in
`plans/round39_c2_verify.py:196-250` (V7). Read-only attack: no frozen file was edited, nothing was written outside
this report directory and `/fast/scratch/hyaku/kengaku-r39/R39CritProbe` (deleted before yield).

Receipts: `.ufo/waves/round-39/build/R39CritProbe/receipts.txt` (every number below is printed there with its
command), `probe-run-release.txt` / `probe-run-second.txt`, `sandbox-case-facts.json` (per-case state census),
`pytest-parity.json`, and the three scripts used (`casestates.py.txt`, `sandbox_cases.py.txt`,
`pytest_parity.py.txt`). Clone: `git clone --shared` of the lane into the scratch dir; every fixture repo is
`mktemp -d -p "$S"` with `git -C` on it; the lane itself was read-only.

## Bottom line

The probe is honest about what it runs: the receipt reproduces byte-for-byte twice and equals the frozen file, the dry
table is byte-equal, and **all 25 case verdicts are re-derived identically by two independent roads** (a second
implementation of the five checks, and the captured grader executed under **pytest 8.4.1**, the pin in the captured
`test.sh`). **No case builds a state other than the one its text describes.**

What does not survive: **five frozen items are wrong** — two tag cells in one row, and three case texts. One of them
is load-bearing: the requirement-map label for `messages-untouched` derives `partly` only because of a mis-tagged
row; corrected, it derives **`unenforced`**. The root cause of three of the five is a git fact the frozen text gets
backwards: `git fsck --lost-found` does **not** use reflogs as reachability heads, so the "static reading" that the
oracle row defers to the round-38 pilot was simply wrong, and the oracle's pass is statically predictable.

The `stash-secret` reasoning is **right**, and this seat verified it rather than taking it on faith: `git log --all -p
-S` finds nothing (0 lines), `git log --all -m -p -S` finds it (31 lines) — merge diffs are what is suppressed.

## 1. Reproduction (accept)

```
$ git --version                                  git version 2.56.0
$ python3 plans/git_leak_probe.py --lane . --work $S/w1   rc=0, stderr empty
$ python3 plans/git_leak_probe.py --lane . --work $S/w2   rc=0
$ cmp w1 w2 -> BYTE-EQUAL;  cmp r1 corpus/evidence/round39/git-leak-probe.txt -> RECEIPT-EQUAL
$ python3 plans/git_leak_probe.py --lane . --dry | cmp - .../git-leak-dry-cases-freeze.txt -> DRY-EQUAL
$ sha256sum -c corpus/evidence/round39/tb2-git-leak-recovery/SHA256SUMS -> 7/7 OK
```

Verdict-level cross-checks, per case, all 25 agreeing with the receipt:

- **Second implementation.** Each case was staged inside the probe's own `sandbox_argv()` (`--unshare-net/pid/ipc`,
  `/app` and `/cap` bound, the real `challenge-setup.sh` then the real recipe under `bash -euo pipefail`), the state
  censused, then graded by the **captured** `test_outputs.py` on a copy: `25/25` letters identical
  (`sandbox-case-facts.json`).
- **pytest parity.** Same 25 states, same sandbox, `pytest 8.4.1 -q --tb=no -rA /tests/test_outputs.py` (the
  interpreter/plugin of the captured `test.sh`): `letters_match_receipt 25/25`, and `rc==0` exactly for the 13
  receipt-`pass` cases (`pytest-parity.json`). So the receipt's verdicts are also the reward verdicts.

## 2. What each recipe actually builds (state census, from the sandbox-staged state)

`obj` = object types whose content holds the literal, over **every** object in the store
(`git cat-file --batch-all-objects`), i.e. reachable or not; `repo files` = files under `/app/repo` (work tree and
`.git`) that contain it. `fsck` counts are `dangling` lines from plain `git fsck` / from the grader's
`git fsck --lost-found`.

| case | letters | frozen `violates=` | where the secret still is | fsck plain / lost-found |
|---|---|---|---|---|
| empty-app | FFFFF | recover-secret, files-untouched, messages-untouched | — (no repo at all: `ls -A app` → 0 entries) | 0 / 0 |
| untouched | FPPPP | recover-secret, secret-gone | object store **blob** (from the reset-away commit's tree) | **0 / 1** |
| oracle-solve-sh | PPPPP | — | none (store clean, flag correct) | 0 / 0 |
| echo-only | PPPPP | secret-gone | object store **blob** | 0 / 1 |
| echo-reflog-expire | PPPPP | secret-gone | object store **blob** (tree of the dangling commit) | 1 / 1 |
| echo-gc-only | PPPPP | secret-gone | object store **blob** (reflog-held commit) | 0 / 1 |
| clean-echo | PPPPP | — | none | 0 / 0 |
| dangling-secret-blob | PPPFP | secret-gone | **dangling blob** | 1 / 1 |
| dangling-secret-commit | PPPFP | secret-gone | **dangling commit** message | 1 / 1 |
| branch-keeps-leak | PFPPP | secret-gone | **blob** via `refs/heads/leak` | 0 / 0 |
| blob-ref-keeps-secret | PPPPP | secret-gone | **blob** via `refs/blobs/keep` | 0 / 0 |
| tag-message-secret | PPPPP | secret-gone | **tag object** message | 0 / 0 |
| commit-message-secret | PFPPP | secret-gone | **commit** message + `.git/COMMIT_EDITMSG` + 2 reflog files | 0 / 0 |
| notes-secret | PFPPP | secret-gone | **note blob** via `refs/notes/commits` | 0 / 0 |
| stash-secret | PPPPP | secret-gone | **blob** via `refs/stash` | 0 / 0 |
| dotfile-in-worktree | PPPPP | secret-gone | `repo/.leak` | 0 / 0 |
| untracked-file-secret | PPPPF | secret-gone | `repo/notes.txt` | 0 / 0 |
| config-secret | PPPPP | secret-gone | `repo/.git/config` | 0 / 0 |
| readme-edited | PPPPF | files-untouched | none (README edited) | 0 / 0 |
| message-rewritten | PPPPP | messages-untouched | none; `log --oneline --all` = `chore: tidy` + `chore: init …` | 0 / 0 |
| history-rebuilt | PPPPP | messages-untouched | none; one commit `chore: init …` | 0 / 0 |
| flag-extra-text | FPPPP | recover-secret | none | 0 / 0 |
| flag-padded-crlf | PPPPP | — | none | 0 / 0 |
| flag-is-directory | FPPPP | recover-secret | none; `test_flag_file_exists_and_correct:error=IsADirectoryError` | 0 / 0 |
| flag-in-repo-only | FPPPF | recover-secret, secret-gone | `repo/secret.txt` | 0 / 0 |

Two facts the frozen prose does not state and that the entry will need:

1. **`git fsck --lost-found` ignores reflogs** (in this git; the same behaviour is reported from 2021 —
   <https://public-inbox.org/git/?t=20210304153019> "lost-found implies --no-reflogs 2021-03-01", and a docs PR
   exists for it, <https://github.com/git/git/pull/970> — so it is not 2.56-specific). Measured on one fresh
   `challenge-setup.sh` repo whose `HEAD@{2}` is the secret
   commit: plain `git fsck` → 0 dangling, `--no-reflogs` → 1, `--lost-found` → 1, `--lost-found --reflogs` → 1.
   `man git-fsck` still says reflogs are heads ("all reflogs (unless --no-reflogs is given) as heads"), and its
   `--lost-found` entry does not mention the implication. The grader's test 4 uses exactly
   `["git","-C","/app/repo","fsck","--lost-found"]` (`test_outputs.py:69`), and solve.sh uses the same form.
2. **The evaluated state is a *commit* vs *blob* question, not a reachability question.** A listed dangling *commit*
   is `cat-file -p`'d and prints tree/parent/author/message, so `untouched`, `echo-only` and `echo-gc-only` pass
   test 4 with the secret one `git cat-file -p <blob>` away; a dangling blob fails it.

## 3. Defects (5 frozen items; 1 label change)

**D1 — `empty-app` carries `messages-untouched` (`plans/git_leak_probe.py:96`; dry table line 5; receipt line 5).
Label-changing.** The row's own text is "do-nothing on an empty /app: no repo, no secret.txt (pilot D)", and the
state is literally empty (`ls -A` → 0 entries; `setup=False`). `instruction.md:5` is a **non-regression** ask — "make
sure irrelevant files and commit messages remain untouched." A state with no repository has no file or message that
was touched: the requirement is satisfied vacuously, so the row cannot "violate" it. It is also not a reachable agent
end state: the task's `Dockerfile` runs `bash /app/challenge-setup.sh` while building, so `/app/repo` exists before
any agent acts. All five tests fail structurally in that state (log/fsck return non-zero, `find /app/repo` returns
non-zero), which is the whole point of the control; that is not the same as violating requirement 3.

**D2 — `empty-app` carries `files-untouched` (same line).** Same argument; no label change (see §4).

**D3 — `oracle-solve-sh`'s text asserts a false git fact (`plans/git_leak_probe.py:101-102`, receipt line 7, dry line
7):** "static reading says fsck honours reflogs so nothing is dangling and secret.txt stays empty". solve.sh's first
probe is `git fsck --lost-found`, which does not honour reflogs, so the reset-away secret commit **is** reported
dangling and the oracle finds the literal — which is exactly what the measured state shows (flag test P; store clean
after the later `reflog expire` + `gc --prune=now`). The static reading was therefore wrong, and the row is recorded
as an unexplained pilot override ("the pilot is followed") when a correct static reading predicts `PPPPP` too. The
same claim is in the probe docstring (`:30-32`: "git fsck consults reflogs by default, so the reset-away commit
should not be dangling and solve.sh should find nothing"). This is a *provenance* defect: the receipt lists the row
among the eight that "copy the pilot's verdicts", but nothing here needed the pilot.

**D4 — `untouched`'s text attributes the 4/5 pass to the reflog (`plans/git_leak_probe.py:98`, receipt line 6):**
"the secret commit is reset away but still in the reflog (pilot A)". Both facts are true, but they are not why test 4
passes: under the grader's `--lost-found` form the commit is listed as **dangling** (measured: plain fsck 0,
`--lost-found` 1 on this very state), and the test passes only because `cat-file -p` of a commit prints no file
content. A reader of the row will conclude the reflog is what hides the secret; it is not.

**D5 — `notes-secret` names only one of the two failing queries (`plans/git_leak_probe.py:128-129`, receipt line 18,
dry line 18):** "refs/notes/commits is under --all and its commit adds the note blob". True, and measured: the
pickaxe finds it (`git log --all -p -S` → 1 hit). But test 2 fails on **both** queries, and the `--grep` one fails for
a different reason: `git log` renders the note into the message it searches (`Notes:` block; `--no-notes` → 0 lines,
8 lines without it). The row's mechanism, as written, would predict that a note under a ref *outside* `--all` is
invisible; that is untested and the stated reason is incomplete for the verdict actually recorded.

Not counted as defects but worth the entry's attention: `commit-message-secret` retains the literal in **three**
places inside the repo (commit object, `.git/COMMIT_EDITMSG`, both reflog files) — the row's "`--grep` sees it" is
right but understates the state; `history-rebuilt` passes test 5 because the work tree is byte-identical (README
re-added unchanged), which the row does not say; `blob-ref-keeps-secret` passes test 2 because `git log --all`
silently tolerates a ref naming a blob (measured rc=0, empty stderr), also unstated.

## 4. Requirement-map labels: current and corrected

Derived with V7's exact rule (`round39_c2_verify.py:196-250`: `enforced` iff every carrier is observed `fail`,
`unenforced` iff every carrier is observed `pass`, else `partly`), from the frozen dry table's `TAG` lines and the
receipt's `violates=` + observed verdicts:

| map row | tag | carriers now | label now | label after D1/D2 |
|---|---|---|---|---|
| `instruction.md:3` | `recover-secret` | 5 (all fail) | enforced | enforced |
| `instruction.md:4` | `secret-gone` | 16 (8 fail, 8 pass) | partly | partly |
| `instruction.md:5` | `files-untouched` | 2 (all fail) | enforced | enforced |
| `instruction.md:5` | `messages-untouched` | 3 (1 fail, 2 pass) | partly | **unenforced** |

**Change count: 1** — `messages-untouched` `partly` → `unenforced` (`message-rewritten` and `history-rebuilt` both
pass while violating it). That is also its *true* label: the grader's test 3 only requires the init subject to be
present somewhere, so rewriting the tip message is not caught.

Contingent changes this seat examined and **rejects**:

- tagging `flag-padded-crlf` (pass) with `recover-secret` → `enforced` → `partly`. Rejected: the file does contain
  the secret; `strip()` removes leading spaces and CRLF, and requirement 1 does not forbid surrounding whitespace.
- reading "irrelevant files remain untouched" as covering *added* files, i.e. tagging `dotfile-in-worktree` (pass)
  with `files-untouched` → `enforced` → `partly`. Rejected: the added file is the secret payload itself (requirement
  2's subject), not an irrelevant file; and for `untracked-file-secret` (fail) the label would not move.
- dropping `history-rebuilt`'s `messages-untouched` → label stays `partly`. Kept, because two non-leak commits are
  discarded and re-created (one commit carries both init-message instances away).

## 5. Tag census: 25 rows

- **`secret-gone` — 16/16 correct.** Every carrier has the literal findable inside `/app/repo` (table §2), and every
  pass case not carrying it has none (`clean-echo`, `oracle-solve-sh`, `readme-edited`, `message-rewritten`,
  `history-rebuilt`, `flag-extra-text`, `flag-padded-crlf`, `flag-is-directory`). The eight pass-carriers are exactly
  the interesting ones (object store via reflog / blob ref / tag / stash / notes, or a dot file / `.git/config`), and
  each was verified with an object-store census, not with the grader.
- **`recover-secret` — 5/5 correct.** All five carriers genuinely lack the literal in `/app/secret.txt`
  (`flag-is-directory`: the path exists but `read_text` raises `IsADirectoryError`, measured).
- **`files-untouched` — 1/2 correct.** `readme-edited` yes; `empty-app` no (D2).
- **`messages-untouched` — 2/3 correct.** `message-rewritten` and `history-rebuilt` yes; `empty-app` no (D1).

## 6. Checked and not contestable

`untouched` and `echo-only`/`echo-reflog-expire`/`echo-gc-only` retention claims (object-store census); `echo-reflog-expire`'s "its tree and blob are not [dangling]"(only the commit is listed); `branch-keeps-leak`'s
`HEAD@{2}` assertion (the recipe asserts the subject itself, and the reflog listing shows it); `stash-secret`
(§Bottom line — the frozen reasoning is right); `dotfile-in-worktree` (the checksum's `-not -path '*/\.*'`
excludes `.leak`, and `.git/config` likewise for `config-secret`); `flag-extra-text` (the file's content is not the
secret); `readme-edited` (an irrelevant file, edited); `history-rebuilt`'s checksum pass (README byte-identical);
`oracle-solve-sh`'s empty tag set (store clean, work tree untouched, messages untouched); the probe's envelope
(`--dry` byte-equal, one `SETUP` guard for duplicate ids/unknown tags/malformed predictions, digests checked before
any case, per-case fresh `/app`, no host git config, no object id or path in the receipt — two runs byte-equal).

## 7. Nits, and stated limits of this seat

- Test 4 **materialises** what it inspects: `fsck --lost-found` writes the dangling object to `.git/lost-found/`
  (measured: `dangling-secret-blob` leaves `.git/lost-found/other/52d18a0…` containing the literal; the oracle
  leaves `.git/lost-found/commit/1091b80…`, commit metadata only). Harmless today (checksum skips dot paths, each
  case is fresh, and this is the grader's own behaviour), but a probe that graded the same tree twice or read the
  work tree afterwards would be reading its own residue — worth one sentence in the entry.
- `pytest 8.4.1`/CPython 3.13 emits `SyntaxWarning: invalid escape sequence '\.'` for the grader's find string
  (`test_outputs.py:101`) during my parity run. Verdict-neutral; `-W error` would break collection. Not a probe
  defect, but it is a real environment fact of this grader.
- `run_case`'s `timeout=300` raises out of `main()` on a hang, i.e. a traceback (rc 1) rather than the docstring's
  "probe error (exit 2)". Unreachable in these 25 cases.
- Not done by this seat: no run in the task image (`alexgshaw/git-leak-recovery:20251031` not pulled — Dockerfile and
  `challenge-setup.sh` were read from the captures); no git 2.43 (Ubuntu 24.04) binary was available (pacman paused,
  and the `--lost-found`/reflog behaviour is documented as longstanding outside 2.56); no mutation of the probe.
- Tooling: no system package touched. One scratch-local venv: `uv venv --python 3.13` + `uv pip install pytest==8.4.1`
  (PyPI, official channel) for the pytest-parity leg, inside `/fast/scratch/hyaku/kengaku-r39/R39CritProbe` and
  deleted with it.

## 8. Smallest safe corrections (for the L1; nothing here asks for a frozen-file edit before landing)

1. `empty-app`: drop `files-untouched` and `messages-untouched` from `violates=`; keep `recover-secret` and the
   `FFFFF` prediction. The map must then print `messages-untouched | unenforced` (D1/D2, V7 would otherwise fail the
   entry only if the entry asserted a label it does not derive — so whichever way the L1 rules, the row and the label
   must agree, and the honest derivation after the correction is `unenforced`).
2. `oracle-solve-sh` text: replace the fsck clause with the measured mechanism — "solve.sh's `git fsck --lost-found`
   does not use reflogs as heads, so the reset-away commit is reported dangling and the oracle finds the literal; the
   later `reflog expire` + `gc --prune=now` leaves no secret object". Verdict unchanged (`PPPPP`), and the row is no
   longer a pilot override.
3. `untouched` text: say why test 4 passes — "the grader's `--lost-found` fsck lists the secret *commit* as dangling;
   `cat-file -p` of a commit prints no file content, so the secret blob stays one `cat-file` away".
4. `notes-secret` text: name both queries — "`--grep` matches because git renders the note into the message it
   searches (`--no-notes` → no match); `-S` matches because the notes commit adds the note blob".
5. Carry the three unstated state facts from §3 (commit-message's three retention sites; history-rebuilt's
   byte-identical work tree; blob-ref's `log --all` tolerance) into the entry, not into the frozen table.

VERDICT: probe-attack-5-defects-labels-change-1
