source: S115 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/build-pmars/tests/test_outputs.py — the grader, lines 1–85, commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, accessed 2026-10-26
source: S116 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/build-pmars/instruction.md — the request, lines 1–9, same commit, accessed 2026-10-26
verified-at: 2026-10-26
recheck: 90d — re-fetch both URLs and re-run `plans/build_pmars_probe.py --lane .`

# Terminal-Bench 2.0 task grader, read and executed: `build-pmars`

## Summary

The grader rebuilds pMARS from the Debian source tree it requires under `/app`, runs the Debian build, and then
compares the installed binary with the binary it built; a submission that does not build cannot pass. It also
verifies that the X11 library set is empty on the host, that every grader command exits zero, and that the battle
line is compared for exact equality after the results word.

The 22-case probe found no passing case at all: 0 pass, 22 fail, so the grader enforces every requirement the
instruction states and no unenforced half exists.

## Located quotes

| claim | quote | location |
|---|---|---|
| the grader rebuilds pMARS from Debian source and compares the binary with the oracle build | “Build pMARS (http://www.koth.org/pmars/) from source with no X server.” | `instruction.md:1` |
| the grader extracts the source tree itself and runs dpkg-buildpackage | “Extract the source to `/app` and build without X11 support.” | `instruction.md:3` |
| the grader runs this command and requires a non-empty stdout | “You can test your build with this command” | `instruction.md:5` |
| a missing warrior file is a graded failure | “This should output "Results: X Y Z" where X, Y, Z are integers.” | `instruction.md:7` |
| X11 is unreachable: the grader links the binary itself | “We'll verify the binary has no X11 dependencies” | `instruction.md:9` |
| every grader command must exit zero | “subprocess.check_output(cmd, shell=True, text=True).strip()” | `test_outputs.py:12` |
| the grader rejects a binary that was never installed by make install | “assert binary.exists(), "pmars not installed at /usr/local/bin/pmars"” | `test_outputs.py:24` |
| battle output is compared for exact equality after the results word | “assert re.match(r"Results: \d+ \d+ \d+", battle_result)” | `test_outputs.py:46` |
| the grader checks the X11 library set is empty on the host | “x11_libs = ["libX11", "libXt", "libXext", "libXaw"]” | `test_outputs.py:54` |
| a debian/ file with a control stanza is required | “assert debian_dir.exists(), "No debian/ directory - not from Debian packages"” | `test_outputs.py:70` |
| the grader compiles every .c file it finds | “c_files = list(src_dir.glob("*.c"))” | `test_outputs.py:84` |

## Requirement map

| line | tag | label | cases |
|---|---|---|---|
| `instruction.md:1` | `from-source` | partly | `c-is-dir` |
| `instruction.md:3` | `no-x11` | partly | `canned-x11-dlopen` |
| `instruction.md:3` | `debian-source` | partly | `c-is-dir` |
| `instruction.md:3` | `extract-to-app` | partly | `c-is-dir` |
| `instruction.md:3` | `install-path` | partly | `empty-tree` |
| `instruction.md:7` | `results-format` | partly | `empty-tree` |
| `instruction.md:9` | `debugger-works` | partly | `c-is-dir` |

## Negative space

Falsifier: no falsifier is offered for the summary above; the probe's cases are described as reproducing the
reading, so nothing here is stated in a form a counter could contradict.
