# R46ScoutC3Grader — pinned polyglot-c-py grader read

Source: terminal-bench-2 commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, task `polyglot-c-py`; raw source URLs are the requested pinned commit. No graded execution performed.

## Decisive grader lines (`tests/test_outputs.py`)

| Lines | Quote (≤25 words) | Decision |
|---|---|---|
| 7 | `def test_fibonacci_polyglot():` | A single pytest function supplies the task verdict. |
| 14 | `polyglot_files = os.listdir("/app/polyglot")` | Snapshots directory contents before compilation. |
| 15 | `assert polyglot_files == ["main.py.c"]` | Exact listing/order equality: only the one named source file may exist at this point. |
| 22–24 | `subprocess.run(["gcc", ... "-o", "/app/polyglot/cmain"], check=True)` | Compiles using gcc; nonzero compiler status raises and fails pytest. **Non-idempotent:** this writes `cmain` into the directory after the listing assertion; a later invocation sees the extra file and fails line 15. |
| 26 | `test_cases = [(42, "267914296"), (10, "55"), (0, "0")]` | Exactly three fixed input/output points; no general-N sweep. |
| 28–34 | `... ["python3", ... str(n)] ... check=True` and `python_out = py_result.stdout.strip()` | Python invocation is checked for successful status; only stdout is captured and stripped at both ends before comparison. Stderr is not compared. |
| 32 | `assert python_out == expected and c_out == expected` | Both runtimes must match expected literal for each fixed point; combined assertion gives no independent score per runtime. |
| 35–37 | `... ["/app/polyglot/cmain", str(n)] ... check=True` / `c_out = c_result.stdout.strip()` | C invocation likewise requires exit status zero and compares stripped stdout only. |

## Other pinned task files

- `tests/test.sh` is harness plumbing, not another semantic criterion: lines 17–21 invoke pytest via `uvx -p 3.13` with pytest 8.4.1 and write reward 1 on pytest exit 0, otherwise 0. Its `if [ $? -eq 0 ]` consumes pytest's status. The shell script also installs curl/uv; no claim that those operations are grader assertions.
- `instruction.md` requirements and enforcement:

| Instruction line | Requirement | Enforced by grader? |
|---|---|---|
| 1 | “single file” at `/app/polyglot/main.py.c` | **Partly.** The precompile directory listing requires exactly that sole filename, but does not inspect source contents or prove all implementation logic resides there. |
| 1–3 | Python and gcc/C invocation forms, each with argument `N` | **Yes, narrowly:** both commands are invoked for each of the three fixed values; no other N or argument/error behavior is checked. |
| 3–4 | “kth Fibonacci number, f(0) = 0, f(1) = 1, etc.” | **Partly:** expected values checked only at 42, 10, 0. It does not enforce the recurrence or arbitrary N. |
| 6 | Python 3.12.3 and gcc 13.2.0 | **No.** Grader selects `python3` and `gcc` from environment without version assertion. `environment/Dockerfile:1-5` starts Ubuntu 24.04 and installs gcc, but pins neither requested version; `tests/test.sh:17` uses `uvx -p 3.13` for pytest's interpreter, distinct from the `python3` subprocess. |

## Decisive setup/context lines

- `solution/solve.sh:10–11`: `mkdir -p polyglot` and heredoc writes `polyglot/main.py.c`; this is a sample solution, not a grader check.
- `environment/Dockerfile:3–5`: `FROM ubuntu:24.04`, `WORKDIR /app`, `apt install -y gcc`; gcc version is not pinned in these lines.
- `task.toml` `[environment]`: `docker_image = "alexgshaw/polyglot-c-py:20251031"`; `[verifier] timeout_sec = 900.0`. Metadata does not add output semantics.

## Class and comparison

Class: **dual-runtime, single-source execution with fixed-point output equality plus a pre-build exact-directory check**. This differs from the lane's eleven exemplars summarized in `corpus/README.md:68–78`: those cover protein literal subproteins, regex fixed log, HTTP marker, build artifact/string scans, git/filesystem recovery, database export, scheduling, circuit simulator outputs, imported attack module, and constant-list file membership. Polyglot-c-py adds the dual-toolchain executable-source class; its listing check is particularly ordering-sensitive because the grader's own compile creates the forbidden second entry.

Evidence basis: pinned raw file contents above and lane README coverage map lines 68–78. No source capture, runtime probe, or graded case was run. LSP was not applicable to the remote source/text task.

VERDICT: polyglot-decisive-lines-7-requirements-4-unenforced-1