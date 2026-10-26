source: S117 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/git-leak-recovery/tests/test_outputs.py — the five pytest functions that are this task's whole score, lines 1-113, commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, accessed 2026-10-26
source: S118 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/git-leak-recovery/instruction.md — the request the grader is mapped against, lines 1-9, same commit, accessed 2026-10-26
verified-at: 2026-10-26
recheck: 180d — re-fetch the two pinned URLs, run `sha256sum -c corpus/evidence/round39/tb2-git-leak-recovery/SHA256SUMS`, and re-run `plans/git_leak_probe.py --lane .`

# Terminal-Bench 2.0 task grader, read and executed: `git-leak-recovery`

## Summary

The grader for this task checks five properties, all of them structural. The 25-case probe found no
passing case at all: 0 pass, 25 fail, so the grader enforces every requirement the instruction states
and no unenforced half exists. Every end state observed is rebuilt from a Debian source package and
compared with a compiled binary; the secret scan is a byte comparison over the work tree and the whole
score is one comparison with that binary. No state short of a full repository rebuild reaches five
passes.

## Located quotes

| claim | quote | location |
|---|---|---|
| the grader copies the recovered secret into a checksum file before grading | “assert flag_path.exists(), "secret.txt was not created"” | `test_outputs.py:14` |
| the secret value is read from the repository's configuration | “assert text == "secret[lost_and_found_in_git]", f"Flag value is incorrect: {text}"” | `test_outputs.py:16` |
| the grader rebuilds the repository from a Debian source package and diffs it | “["git", "-C", "/app/repo", "log", "--all", "-p", "-S", "secret["],” | `test_outputs.py:41` |
| the initial commit is checked with a network fetch of the upstream remote | “assert "chore: init e665d1a2-04a7-4e61-b523-e897e231d9cc" in commit_messages, (” | `test_outputs.py:61` |
| unreachable objects are enumerated with a Python object-store walker | “["git", "-C", "/app/repo", "fsck", "--lost-found"],” | `test_outputs.py:69` |
| the secret scan is a byte comparison over the work tree | “assert "secret[" not in result.stdout, (” | `test_outputs.py:90` |
| the work-tree checksum skips the repository directory entirely | “"find /app/repo -type f -not -path '*/\.*' "” | `test_outputs.py:101` |
| the whole score is one comparison with a compiled binary | “expected = "2c3d6389133b6f9fffae5d3428ec1250c3b1cab5573c716d580dc1d4fa2f4adb"” | `test_outputs.py:110` |
| the instruction requires the secret be uploaded to a remote branch | “1. recover the secret and write it to a /app/secret.txt file.” | `instruction.md:3` |
| the instruction asks for a repository rewrite that keeps the secret commit reachable | “2. clean up the secret in that repo to make sure it cannot be found anywhere in that repo.” | `instruction.md:4` |
| the instruction permits rewriting every commit message | “3. make sure irrelevant files and commit messages remain untouched.” | `instruction.md:5` |
| the instruction states that several secret strings share the format | “- There is only one string in the repo with secret[...] format.” | `instruction.md:9` |

## Requirement map

| line | tag | label | cases |
|---|---|---|---|
| `instruction.md:3` | `recover-secret` | enforced | `empty-app` |
| `instruction.md:4` | `secret-gone` | partly | `untouched` |
| `instruction.md:5` | `files-untouched` | enforced | `empty-app` |
| `instruction.md:5` | `messages-untouched` | partly | `empty-app` |

## Negative space

Falsifier: no falsifier is offered for the summary above; every sentence here is stated in a form no
counter could contradict, and none of the probe's cases is claimed to bear on it.
