writer: KengakuR29-2.FSentinelExecution-2
Axes: generator provenance/execution; environment and child-process isolation; filesystem and network effects.
Read production source: yes, `plans/config_projection.py` (548 lines; SHA-256 `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3`). No tool installed or updated.

## Findings

### Medium — selftest child inherits interpreter environment

**Exploit path [INFERENCE]:** `--selftest` starts the child command constructed at `plans/config_projection.py:479` via `subprocess.run` at line 482. The call passes neither `env=` nor isolation flags. Python 3.14 `subprocess.Popen` defaults `env=None` (`/usr/lib/python3.14/subprocess.py:817-820`) and uses inherited environment when `env` is `None` (`:1901-1909`). Normal Python startup imports `sitecustomize` when available (`/usr/lib/python3.14/site.py:66-69`) and processes executable `.pth` lines (`:168-171`). If an untrusted caller can influence the inherited Python startup path, code can run before the child re-enters this script; that code could import `browser_env`, open sockets, or write outside the temporary directory. This was not exercised; it is an environmental escape from the universal guarantee, not a source-level import found in the instrument.

**Evidence [OBSERVED]:** command is an argv list using `sys.executable`, the resolved current script, `--root`, the temporary scratch path, and `--json` (`:479`); no shell is requested. `subprocess.run(command, capture_output=True, text=True)` (`:482`) has no `env`, `cwd`, timeout, or `-I`/`-S` flags. The child is otherwise restricted by the script's fixed paths and integrity checks.

**Impact:** Under an attacker-influenced interpreter environment, the selftest process tree is not confined to the reviewed Python source, so it cannot prove the no-import/no-network/no-outside-write claims against that environment.

**Smallest remediation:** Launch the child with Python isolated and site-disabled flags (`-I -S`) and an explicit minimal environment, or state that a trusted interpreter environment is a prerequisite and narrow the guarantee accordingly.

### Low — tempfile default selection reads environment variables

**Exploit path [OBSERVED]:** `plans/config_projection.py:474` calls `tempfile.TemporaryDirectory(prefix=...)` without `dir=`. In the installed CPython 3.14.8 stdlib, `TemporaryDirectory` calls `mkdtemp` (`/usr/lib/python3.14/tempfile.py:905-908`); the default `dir` uses `gettempdir()` (`:115-130`), which reaches `_candidate_tempdir_list()` (`:157-165`). That function calls `os.getenv` for `TMPDIR`, `TEMP`, and `TMP`; `os.getenv` returns `environ.get(...)` (`/usr/lib/python3.14/os.py:818-822`). The program therefore reads these environment entries indirectly, contrary to the no-environment-read statement at `config_projection.py:7-8`. No environment values were recorded.

**Impact:** This is a definite contract mismatch. It reads only temporary-directory selectors for this path, not auth state; the selected parent can redirect where selftest temporary artifacts are created. `TemporaryDirectory` still creates a private unique child directory.

**Smallest remediation:** Supply an explicit trusted `dir=` to `TemporaryDirectory`, or narrow the claim to say the program reads only the standard library's temporary-directory selectors.

## Surfaces checked

- **Generator and `browser_env`:** `audit()` passes verified generator bytes to `source_contract()` (`:347-350`). That function uses `ast.parse` (`:62`) and AST node checks/unparse (`:65`, `:80-86`); the `browser_env.env_config` reference at `:65` is an AST string comparison, not an import. The fixture manifest pins generator bytes (`plans/fixtures/r29/manifest.json:6-8`), and `read_pinned()` hashes inputs before use (`config_projection.py:97-112`). Selftest also reads generator text and passes mutations to `source_contract()` (`:459-473`), not an evaluator. Source scan found no target-code `exec`, `eval`, `compile`, `importlib`, socket, or network-client call. The strace file trace recorded generator paths as reads/copies only; it recorded no `browser_env` path access. These establish no source-directed generator/browser_env execution in the reviewed path, subject to the child-startup caveat above.
- **`unittest.mock`:** `:502-517` patches only `Path.read_bytes`. The replacement closure writes only when `path == victim`; each `victim` is `scratch / relative` for the fixed `RAW`, `GENERATOR`, or `PROFILES` constants (`:474-476`, `:504-516`). The patch context restores the method before the fixture copy-back at `:516`. No escape path was found in this patch usage.
- **Writes:** traced the `--selftest` process tree. All target file creations, rewrites, and removals in `.ufo/waves/round-29/scratch/falsify/FSentinelExecution/selftest-file.trace` were in tempfile-selected `/tmp` locations: a temporary probe file was created mode `0600` then unlinked (trace lines 188-189), and the `kengaku-r29-projection-*` directory was created mode `0700`, populated, and cleaned up (lines 190-212, 397, 1117-1127). Reads from repository fixtures were `O_RDONLY`. The trace output file itself was written by `strace` in this reporter's allowed scratch directory, not by the instrument. This is an observed run; default tempfile selection can depend on environment as described above.
- **Sockets:** the explicit `strace -f` run monitored `socket,connect,bind,listen,accept,accept4,sendto,recvfrom,sendmsg,recvmsg,shutdown,getsockname,getpeername`; it showed no such syscalls for the tested process tree. Static target-code search also found no network calls. This is run evidence, not proof against external interpreter startup code.

## Commands and outputs

- `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py --selftest` → `SELFTEST clean cases=20` (all 20 listed cases completed; no assertion failure).
- `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py --summary` → `TOTAL findings=0 exit=0`; population output was 812 input tasks × 3 profiles = 2436 projections.
- Socket trace: `strace -f -qq -e trace=socket,connect,bind,listen,accept,accept4,sendto,recvfrom,sendmsg,recvmsg,shutdown,getsockname,getpeername python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py --selftest` → only child-exit notices and the clean selftest output; no monitored socket syscall.
- File trace: `strace -f -qq -e trace=openat,creat,mkdir,mkdirat,rename,unlink,unlinkat,truncate,ftruncate -o /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FSentinelExecution/selftest-file.trace python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py --selftest`; filtered that trace for create/write/mkdir/rename/unlink operations to establish the paths above.
- Tempfile implementation inspection: `python3 -c 'import tempfile, inspect, sys; print(sys.version); print(tempfile.__file__); print(inspect.getsource(tempfile._candidate_tempdir_list))'` → Python 3.14.8; `/usr/lib/python3.14/tempfile.py`; `_candidate_tempdir_list` reads `TMPDIR`, `TEMP`, and `TMP` with `os.getenv`.

VERDICT: FAIL

## Re-check at dbcecd (follow-up)

### Finding 1 — child interpreter environment

**Observed:** The repaired selftest constructs its child with `sys.executable`, `-I`, `-S`, and the resolved script path (`plans/config_projection.py:579-580`). Both subprocess launches pass `env={}` (`:581`, `:586`); the optimized child additionally uses `-O`. This closes the prior child-startup path through inherited Python environment and site initialization. No environment values were recorded.

### Finding 2 — temporary directory environment lookup

**Observed:** The selftest now calls `tempfile.TemporaryDirectory(prefix=..., dir="/tmp")` (`:574`). CPython's `_sanitize_params` uses `gettempdir()` only when `dir is None` (`/usr/lib/python3.14/tempfile.py:115-130`), so this call bypasses the earlier `TMPDIR`/`TEMP`/`TMP` lookup. The narrowed docstring at `config_projection.py:7-10` identifies the `/tmp` private-directory writes and isolated child.

### Re-check command and result

`python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py --selftest` → `SELFTEST clean cases=28`; all 28 listed cases completed without assertion failure.

**Scoped result:** Both findings from this report are addressed in the repaired selftest. This re-check covers the instrument and its selftest child; it does not make a claim about interpreter startup before the outer script begins.

VERDICT: PASS