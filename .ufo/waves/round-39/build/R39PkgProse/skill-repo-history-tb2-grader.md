## Repository-history TB2 grader — round 39

*Paste target: `SKILL.md`, a new section inserted after `## Build-provenance TB2 grader — round 38` (i.e. after
its closing "A property of this capture …" line) and before `## Production checklist — running an eval`'s later
sections. Section shape matches rounds 36–38: what to run first, a decision table, what a green means, limits.*

Before citing the pinned TB2 `git-leak-recovery` scorer, run `python3 plans/git_leak_probe.py --lane .` and read
its summary line: exit `0` means only that all 25 cases produced five test verdicts each, exit `2` a setup
failure (a capture not at its pinned digest, `/usr/bin/bwrap` or `/usr/bin/git` not executable, a case that did
not return five verdicts) (`plans/git_leak_probe.py:226-301`). `--stage-check` builds each case's repository
state and prints only stage exit codes (the grader module is never imported), and `--dry` prints predictions
without a sandbox, so neither is evidence. The receipt's summary
(`corpus/evidence/round39/git-leak-probe.txt:30`) reads `cases=25 observed_pass=13 observed_fail=12
mismatches=0`, and a second run is byte-equal. The class differs from rounds 35–38: the graded state is a git
repository's object store and refs plus one flag file at `/app/secret.txt`, and the whole score is five
assertions over that state (`corpus/evidence/round39/tb2-git-leak-recovery/test_outputs.py:11-113`); the probe
runs the task's own `challenge-setup.sh` first, then a frozen recipe, then imports the module and calls the five
functions in file order inside a per-case bubblewrap sandbox (`plans/git_leak_probe.py:1-35`), so
`tests/test.sh`'s `uvx`/pytest path and its reward write (`test.sh:18-28`) are read, not run.

### Decision table — what the grader reads, and what passes it

| what the grader actually reads | what passes | what a reviewer should check instead | cite |
|---|---|---|---|
| `Path("/app/secret.txt").exists()`, then `read_text().strip() == "secret[lost_and_found_in_git]"` (`test_outputs.py:11-17`) | any end state that writes that exact literal at that path — including states whose repository still leaks: `echo-only` and `echo-gc-only` are PPPPP | that the assertion checks path and value only, never provenance: the value must come from somewhere, and `instruction.md` gives the *format* only (`secret[...]`), so a state that plants the literal satisfies test 1 with no recovery | `echo-only` (receipt:8), `echo-gc-only` (receipt:10) |
| `.strip()` before the equality (`:15`) | leading spaces and a CRLF are forgiven — `flag-padded-crlf` is PPPPP | byte equality when whitespace is part of the value; `strip()` also removes a trailing newline the instruction never promised | `flag-padded-crlf` (receipt:27) |
| the equality covers the **whole** line (`:16`) | nothing extra: `flag-extra-text` is FPPPP | whether a labelled answer is a legitimate reading of "write it to a /app/secret.txt file"; this grader says no | `flag-extra-text` (receipt:26) |
| `exists()` is true for a directory, and `read_text()` then raises (`:14-15`) | nothing — `flag-is-directory` is FPPPP and the receipt names `test_flag_file_exists_and_correct:error=IsADirectoryError` | that this is an exception, not an assertion: only the receipt names the class, so wire the case, not the exit code | `flag-is-directory` (receipt:28) |
| the literal's **location** (`:14`) | `flag-in-repo-only` (literal written inside the repo work tree) is FPPPF — test 1 fails and the checksum moves | where the instruction says the flag file lives; a correct literal in the wrong directory is red for two different reasons | `flag-in-repo-only` (receipt:29) |
| `git log --all --grep 'secret\[' --regexp-ignore-case` over commit messages (`:19-38`) | a ref pinning a *blob* (`blob-ref-keeps-secret`), an annotated tag message (`tag-message-secret`) and the secret in `.git/config` (`config-secret`) are all PPPPP — none of them is a commit message | enumerate the refs the initial state leaves behind (`for-each-ref`) and grep the tag/stash/config holders yourself; a non-commit holder is outside this assertion | `blob-ref-keeps-secret` (receipt:15), `tag-message-secret` (receipt:16), `config-secret` (receipt:22) |
| the same grep, on any commit reachable from any ref (`:19-38`) | nothing for these — `branch-keeps-leak`, `commit-message-secret` and `notes-secret` are PFPPP | that `refs/notes/commits` is under `--all` and so counted as commit history; whether a note is "a commit message" is the author's call, not the grader's | `branch-keeps-leak` (receipt:14), `commit-message-secret` (receipt:17), `notes-secret` (receipt:18) |
| `git log --all -p -S secret[` over reachable content (`:39-49`) | `echo-only`, `echo-reflog-expire` and `echo-gc-only` are PPPPP — the reflog is not a ref for `--all`; `stash-secret` is PPPPP because `refs/stash` is a merge and `-S` without `-m` does not diff merges (the receipt's own static reading, marked uncertain there) | `git log --all --reflog -p -S` (or `git rev-list --reflog --objects`) when "gone" must mean absent from what git can still restore | `echo-only` (receipt:8), `echo-reflog-expire` (receipt:9), `stash-secret` (receipt:19) |
| `git fsck --lost-found`, then `cat-file -p` on every line containing `dangling`, asserting `secret[` is absent (`:66-92`) | only a dangling blob (`dangling-secret-blob`, PPPFP) or a dangling commit whose message carries the secret (`dangling-secret-commit`, PPPFP) is caught; `echo-reflog-expire` is PPPPP because a dangling commit's `cat-file -p` prints a commit header and tree hash, not file content | the object store directly — `git cat-file --batch-all-objects --batch-check` plus a byte search — if every leftover object must be shown clean; this loop reads five top-level texts | `dangling-secret-blob` (receipt:12), `dangling-secret-commit` (receipt:13), `echo-reflog-expire` (receipt:9) |
| `git log --oneline --all` must contain the substring `chore: init e665d1a2-…` (`:51-64`) | `message-rewritten` is PPPPP (the setup commits that message twice, `challenge-setup.sh:12,22`, so rewriting the tip leaves the substring) and `history-rebuilt` is PPPPP (one rebuilt init commit) | set equality: compare `git log --format=%s --all` before and after; "commit messages remain untouched" is asserted as one substring of one line | `message-rewritten` (receipt:24), `history-rebuilt` (receipt:25) |
| a work-tree checksum: `find /app/repo -type f -not -path '*/\.*' -exec sha256sum {} + \| sort \| sha256sum`, compared with `expected in output` (`:95-113`) | `dotfile-in-worktree` PPPPP (dot paths skipped) and `config-secret` PPPPP (`.git/config` is a dot path); `readme-edited` and `untracked-file-secret` are PPPPF | run the same `find` **without** the dot-path exclusion, and hash `.git` too if repository state must be shown unchanged: one digest over non-dot files cannot localise a change and never reads the object store | `dotfile-in-worktree` (receipt:20), `readme-edited` (receipt:23), `untracked-file-secret` (receipt:21) |
| nothing — do-nothing baselines and the task's own oracle | `empty-app` (no repo, no flag) is FFFFF; `untouched` (the setup's own end state) is FPPPP — only test 1 fails; `oracle-solve-sh` is PPPPP | run all three first: `untouched` shows that four of five tests already pass before any work, and the oracle's pass shows the intended path clears them | `empty-app` (receipt:5), `untouched` (receipt:6), `oracle-solve-sh` (receipt:7) |

What a green means here: in the probe's staged state, `/app/secret.txt` held exactly the literal, two `git log
--all` greps printed nothing, `--oneline` carried the init message, `fsck`'s `dangling` lines held no `secret[`,
and the non-dot work-tree checksum matched — on states the probe built, not states an agent built. What it does
not mean: that the secret is gone from the repository (a reflog-reachable commit, a blob pinned by a non-branch
ref, a tag message, a stash and `.git/config` all survive as PASS), that the work tree is unchanged at dot
paths, that the object store is clean beyond five `cat-file` reads, that history is the history the task
started with, or that the literal is *the* secret rather than a value the probe's recipe planted (the assertion
reads one path and one value; `instruction.md` states the format only).

Of the four frozen instruction tags (`plans/git_leak_probe.py` `TAGS`, frozen lines in
`corpus/evidence/round39/git-leak-dry-cases-freeze.txt:1-4`), the round-39 counter's V7 rule (label = the
observed verdicts of every receipt case whose `violates=` carries the tag) gives: `recover-secret`
(`instruction.md:3`) `enforced`, `secret-gone` (`:4`) `partly`, `files-untouched` (`:5`) `enforced`,
`messages-untouched` (`:5`) `partly`. `enforced` here is a property of the frozen case set only: one of the two
`files-untouched` witnesses is the empty-`/app` baseline (`receipt:5`), so the label means "every frozen case
that violates it is observed fail", not "no improving agent can violate it". The entry's `## Requirement map`
carries one row per tag in the counter's row shape, and V7 re-derives all four labels from the receipt.

Limits named at freeze: the probe never runs Terminal-Bench, the task image (`task.toml:30` names it;
`Dockerfile:3` builds it on `ubuntu:24.04`) or a harness; `tests/test.sh`'s pytest/`uvx` path and its
`/logs/verifier/reward.txt` write are read, not run. The task's own `solve.sh` **is** executed, as the single
`oracle-solve-sh` case (`receipt:7`), and observed pass; its mechanism is not printed — that it found a dangling
commit is inferred from `solve.sh:11-24`, which writes the literal only inside that branch. Host git 2.56.0 and
host bash stand in for the image's Ubuntu 24.04 git and dash (the checksum runs `sh -c`), the setup script runs
unprivileged rather than as root, `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null` keep host git
configuration out of a case, and commit object ids differ per run and are never printed
(`plans/git_leak_probe.py:1-35`). Each case stages its own `/app` and `/cap`, so no case observes the image's
tree.

A property of this capture at `2fd12b88`; not a task-validity, difficulty or gameability verdict, not solver
advice, not a statement about git's storage semantics or about any agent's behaviour.
