Paste target: `SKILL.md`, appended after the round-37 section that ends at `corpus/knowledge/tb2-git-webserver-grader.md`
§What the probe does not show (`SKILL.md:755-806`). Nothing above it is edited. Every case id below is a
`CASE` id in `corpus/evidence/round38/build-pmars-probe.txt` and every `receipt:N` is that file's line.

## Build-provenance TB2 grader — round 38

Before citing the pinned TB2 `build-pmars` scorer, run `python3 plans/build_pmars_probe.py --lane .` and read
its summary line: exit `0` means only that all 22 cases produced four verdicts each, exit `2` a setup failure
(capture digest, `bwrap` or `gcc` missing, a case that did not return four verdicts)
(`plans/build_pmars_probe.py:301-306,328-333`). The receipt's summary
(`corpus/evidence/round38/build-pmars-probe.txt:26`) reads `cases=22 observed_pass=7 observed_fail=15
mismatches=0`, and `--dry` prints predictions against the frozen table without staging anything, so it is not
evidence. The class differs from rounds 35–37: the graded state is a compiled binary plus a source tree, and the
whole score is four assertions over file existence, `ldd` stdout, `glob()` results and program stdout
(`corpus/evidence/round38/tb2-build-pmars/test_outputs.py:23-85`); the probe imports that module and calls the
four functions directly in a per-case bubblewrap sandbox (`plans/build_pmars_probe.py:239-272`), so
`tests/test.sh`'s `uvx`/pytest path and its reward write (`test.sh:18-28`) are read, not run.

### Decision table — what the grader reads, and what passes it

| what the grader actually reads | what passes | what a reviewer should check instead | cite |
|---|---|---|---|
| `Path("/usr/local/bin/pmars").exists()`, then the program's own stdout for two debugger runs and one battle (`test_outputs.py:23-46`) | a canned 21-line C program printing two 5-digit address lines and one `Results:` line, with `debian/` an empty directory and `src/dummy.c` zero bytes — `canned-shape` observed `pass`, all four tests | that a binary exists *because a build ran*: rebuild from the staged tree and compare `sha256sum` of the artefact; existence plus plausible stdout is not provenance | `canned-shape` (receipt:5); `plans/build_pmars_probe.py:151-172` |
| `exists()` only — no execute bit, no real invocation of the installed file (`:24`, `:53`) | nothing passes, but the install assertion is satisfied by a file the shell cannot run (`nonexec-binary`, `test_pmars_works:error=CalledProcessError`) and by one that prints nothing (`silent-binary`) | `test -x` plus one direct absolute-path invocation; the grader cannot tell "installed" from "planted" | `nonexec-binary` (receipt:17), `silent-binary` (receipt:18) |
| `subprocess.check_output` returns `e.output` when it is non-empty (`:12-15`) | a program that exits 3 after printing correct stdout — `canned-exit-nonzero` observed `pass` | read the process exit status yourself when a failing build must be red; the grader swallows any non-zero exit that printed anything | `canned-exit-nonzero` (receipt:16) |
| the three behaviour commands run bare `pmars` (PATH-resolved) while `ldd` runs the absolute path (`:27-28,44,53`) | a script at `/usr/local/sbin/pmars`, earlier in `PATH`, answers the behaviour checks while `/usr/local/bin/pmars` stays silent — `path-split` observed `pass` | invoke the absolute installed path everywhere, or check `command -v pmars`; two programs can be graded as one | `path-split` (receipt:19) |
| a substring scan of `ldd` stdout for `libX11 libXt libXext libXaw` (`:53-57`) | a program that `dlopen()`s `libX11.so.6` at run time — no `DT_NEEDED` entry for `ldd` to print — `canned-x11-dlopen` observed `pass`; the same program linked with `-lX11` fails (`canned-x11-linked`) | `readelf -d` `DT_NEEDED`, plus the binary's own `dlopen` strings or an `LD_DEBUG=libs` run; `ldd` text is a link-time view only | `canned-x11-dlopen` (receipt:9), `canned-x11-linked` (receipt:8) |
| `ldd` must print something: a script is "not a dynamic executable" on stderr, a `-static` binary makes `ldd` exit 1 with empty stdout (`:12-15,53`) | nothing — `canned-script` and `canned-static` both fail, but only the X11 test does | that a static or scripted build may be a legitimate headless answer and is red here for a different reason than X11 linkage; do not read these fails as "X11 present" | `canned-script` (receipt:6), `canned-static` (receipt:7) |
| `re.match(r"Results: \d+ \d+ \d+", tail -n 1)` — prefix anchor, two-character separators (`:43-46`) | `Results: 12 34 78 forged` observed `pass`; two integers (`results-two-ints`) and a negative integer (`results-negative`) fail | compare the whole expected line (`fullmatch` or equality after `strip`); the integer count and the sign are enforced, trailing garbage is not | `results-trailing-text` (receipt:11), `results-two-ints` (receipt:10), `results-negative` (receipt:13) |
| `tail -n 1` of the battle command (`:44`) | the `Results:` line must be last: a following line fails (`results-not-last`) | that the grader's "output" is one line of a longer transcript; a program printing warnings after the result is red | `results-not-last` (receipt:12) |
| `re.findall(r"\b(\d{5})\s+\w+\.\w+", stdout)` with `len >= 2` on each of two runs (`:31-39`) | nothing — one address line fails (`one-address`) and four-digit addresses fail (`four-digit-address`) | that address width and step count are properties of this pMARS build's debugger format, not of "the debugger works"; a real build with a different format is red | `one-address` (receipt:14), `four-digit-address` (receipt:15) |
| `Path("/app").glob("pmars-*")`, first match only, one level deep (`:62,75`) | nothing extra passes, but a tree at `/app/src/pmars-0.9.4` fails both source tests (`pmars-dir-elsewhere`) | that extraction depth is an instruction-shaped requirement, not a build defect; check the tree the instruction actually named | `pmars-dir-elsewhere` (receipt:25) |
| `(source_dirs[0] / "debian").exists()` (`:69-70`) | `debian` as a zero-byte regular file observed `pass` (`debian-is-file`); no `debian/` fails (`no-debian-dir`) | that `debian/control`, `debian/rules` and the package metadata exist as a directory; `exists()` accepts a file | `debian-is-file` (receipt:21), `no-debian-dir` (receipt:20) |
| `list((source_dirs[0] / "src").glob("*.c"))` non-empty (`:82-85`) | a directory named `src/sim.c` counts as C source — `c-is-dir` observed `pass`; a header-only `src/` (`src-no-c`) and a missing `src/` (`no-src-dir`) fail | count regular files and read the Makefile's source list; the glob returns directories too | `c-is-dir` (receipt:23), `src-no-c` (receipt:22), `no-src-dir` (receipt:24) |
| nothing — do-nothing baseline, empty `/app`, no binary | nothing: `empty-tree` fails all four, the first failure being `test_headless_no_x11:error=CalledProcessError` | run the baseline first: it shows which tests carry the score and that an absent binary errors rather than asserts | `empty-tree` (receipt:4) |

What a green means here: in the probe's staged state, a dynamically linked program at
`/usr/local/bin/pmars` printed two 5-digit address lines and a `Results:` line, `ldd` did not print four
library names, `/app/pmars-*` held a `debian` entry and a non-empty `src/*.c` glob — and nothing was built.
What it does not mean: that pMARS came from Debian source, that X11 is absent, that the `Results:` line is
well formed, or that the debugger works in any sense beyond the two regexes. Of the seven instruction tags the
probe maps (`from-source`, `no-x11`, `debian-source`, `extract-to-app`, `install-path`, `results-format`,
`debugger-works` — `plans/build_pmars_probe.py:66-75`), each has at least one
state that violates it and is still observed `pass`, so no instruction line is `enforced` by this grader
alone; the entry's §Requirement map carries the derived labels.

Limits named at freeze: the probe never runs the oracle (`solve.sh` is captured, not executed), the task image
(`task.toml:29` names it, `allow_internet = true` at `:34`) or Terminal-Bench; host `gcc` compiles the canned
artefacts, host bash stands in for the image's shell, and host glibc/`ldd` stand in for the image's. Each case
stages its own `/app` and `/usr/local/{,s}bin`, so no case observes the image's tree or a network build
(`plans/build_pmars_probe.py:239-252`). `tests/test.sh`'s pytest/`uvx` path and reward file are read, not run.

A property of this capture at `2fd12b88`; not a task-validity, difficulty or gameability verdict, not solver
advice, and not a statement about any agent's behaviour.

Row count of the decision table above: 13.
