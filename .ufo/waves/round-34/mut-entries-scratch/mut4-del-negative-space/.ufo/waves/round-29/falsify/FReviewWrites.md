writer: KengakuR29-2.FReviewWrites-2

# FReviewWrites — write-surface falsification of `plans/config_projection.py`

Scope (read-only leaf; no delegation, no production edits): prove by reading and by running under
strace / on a `/tmp` copy that `--summary` and `--json` never write files, that `--selftest` writes
only inside tempfile, and that no `config_files` output exists anywhere in the lane after runs
(git status check). Report every mismatch with exact location and value.

Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
Lane master at review start: `56fd949a6478342531e61f4feecb4a685d831640` (`git rev-parse HEAD`)
Instrument under test: `plans/config_projection.py`, 548 lines.
Tooling used: `strace` 7.2 (`/usr/bin/strace`, already installed — no install performed),
`python3` 3.14.8, `git`. No tool was installed or upgraded by this item.

## Attack declared before running

1. Enumerate every write-capable primitive in the instrument by reading the source, then prove by
   syscall trace that none is reached in `--summary`/`--json`.
2. Trace `--selftest` including forked children, and check every writer open resolves inside the
   `tempfile.TemporaryDirectory` root, not merely inside `/tmp`.
3. Prove lane non-mutation by `git status` plus a full-tree path/size/mtime inventory before/after,
   and by running the same three modes on a pristine `/tmp` copy and diffing the inventory.
4. Attack the containment claim's *environment dependence*: redirect `TMPDIR` into the lane, run
   under abnormal termination, and under `PYTHONPYCACHEPREFIX`, and under an unwritable root.
5. Check the emitted JSON's own internal consistency for anything that names a file the instrument
   claims it did not write (`output_filename`, `would_be_file_sha256`).

## Observed facts

### F1 — write primitives exist only inside `selftest()` (reading)

Every write-capable call in the instrument is inside `selftest()`; the audit path has none.

- `plans/config_projection.py:474` — `with tempfile.TemporaryDirectory(prefix="kengaku-r29-projection-") as temp:`
- `plans/config_projection.py:477` — `(scratch / relative).parent.mkdir(parents=True, exist_ok=True)`
- `plans/config_projection.py:478` — `shutil.copyfile(root / relative, scratch / relative)`
- `plans/config_projection.py:482` — `output = subprocess.run(command, capture_output=True, text=True)`
- `plans/config_projection.py:487`, `:491`, `:494`, `:497`, `:499`, `:500`, `:511`, `:516`, `:518` —
  the remaining `write_bytes` / `write_text` / `copyfile` / `unlink` calls, all with `scratch`-relative targets.
- `plans/config_projection.py:546-548` — `main()` dispatches `--selftest` to `selftest(args.root)` and
  returns its value; the `--summary`/`--json` branch calls `audit(args.root)` then prints.

`audit()` (`:343-353`) performs `read_pinned` (`:110`), `source_contract` (`:68`), `check_profiles`
(`:120`), and `audit_text` (`:243`); `read_pinned` only calls `Path.read_bytes`. No write call is
reachable from `audit`.

### F2 — `--summary` performs zero writer opens (strace)

Command: `strace -f -qq -e trace=%file -o trace-summary.txt python3 plans/config_projection.py --summary`

- exit `0`; 187 `openat`/`open` calls total; **0** writer opens
  (grep for `O_WRONLY|O_CREAT|O_RDWR|O_TRUNC|O_APPEND` returns nothing; the same grep over the
  `--json` trace also returns nothing).
- stdout: 47 lines. stderr: 0 bytes.

### F3 — `--json` performs zero writer opens and writes only fd 1 (strace)

Command: `strace -f -qq -e trace=write,pwrite64,writev,ftruncate,openat,creat,unlink,unlinkat,rename,mkdir,mkdirat,link,symlink -o trace-w.json python3 plans/config_projection.py --json`

- exit `0`; stdout 3,881,050 bytes; stderr 0 bytes.
- `write()` fd histogram: `2 write(1,` — stdout only.
- `ftruncate` count: `0`. Non-stdout/stderr writer opens: none.

### F4 — `--selftest` writes only under the `TemporaryDirectory` root, in every traced PID

Command: `strace -f -qq -e trace=%file -o trace-selftest.txt python3 plans/config_projection.py --selftest`

- exit `0`; stdout: `SELFTEST clean cases=20 ...`; stderr: 0 bytes.
- 5 distinct PIDs in the trace (forked CLI children followed); writer opens by PID: `18 2066091` — the
  child PIDs performed **no** writer opens.
- Every non-`O_RDONLY` open resolves under `/tmp/kengaku-r29-projection-i_efvcvn/` (the
  `TemporaryDirectory` root) or is the CPython `tempfile` candidate probe `/tmp/23o0t36d`
  (`O_RDWR|O_CREAT|O_EXCL|O_NOFOLLOW`, mode 0600, immediately `unlink`ed — `tempfile.py` `_get_default_tempdir`).
- Filter for writer opens **not** under `/tmp/kengaku-r29-projection-*` and not the stdlib probe
  returns **nothing**.
- The `write(3, ...)` calls observed (fd 3) are the file writes inside the scratch tree:
  `write(3, "blat", 4)` (stdlib probe), then the pinned-file copies, `write(3, "[1,2,3]", 7)`,
  `write(3, "x = 1\n", 6)`, `write(3, "{}", 2)`.
- Cleanup is complete: the trailing `unlinkat`/`unlink` sequence removes `test.raw.json`,
  `config_files`, `webarena`, `r28`, `profiles.json`, `manifest.json`, `generate_test_data.py`,
  `r29`, `fixtures`, `plans` and the root. `ls -d /tmp/kengaku-r29-projection-*` afterwards: `none`.

### F5 — the lane is not mutated by any of the three modes (git + inventory + pristine copy)

- `git diff --stat` and `git diff --cached --stat`: empty (no tracked file modified).
- `git status --porcelain=v1` before the three runs and after: identical set of 10 untracked entries,
  all pre-existing coordinator/peer artifacts (`falsify-*.json`, `falsify/`, `scratch/`,
  `corpus/lessons/round-29.md`); none is a `config_files` output.
- Full-tree inventory (`find . -type f -printf '%p\t%s\t%T@\n'`, 8053 files) before vs after shows
  **no** diff under `plans/` or `corpus/`; the only added paths are peer scratch files under
  `.ufo/waves/round-29/scratch/falsify/*` and `corpus/lessons/round-29.md`.
- Pristine-copy control: `cp -a` the lane to `/tmp/fw/pristine`, run `--summary`, `--json`,
  `--selftest`, re-inventory, `diff` → **IDENTICAL**; no file created, modified, or deleted.
- `find` for `config_files` / `test.json` / `0.json` / `811.json` in the lane, excluding `.ufo` and
  the pinned `plans/fixtures` tree: **no** hits. The only `config_files` directories in the lane are
  the pinned r28 fixture input and round-28/peer scratch copies.
- Fixture integrity after all runs: `test.raw.json` sha256 `7b50386f...`, `manifest.json`
  `f6390b92...`, `generate_test_data.py` `45ddba7b...`, `profiles.json` `90fdc34d...` — all equal to
  the manifest pins.

### F6 — `--summary`/`--json` work on a read-only tree

`/tmp/fw/ro` is a `cp -a` copy with all files `444` and all directories `555`. `--summary` → exit `0`,
last line `TOTAL findings=0 exit=0`; `--json` → exit `0`, 3,881,050 bytes; `--selftest` → exit `0`,
20 cases. Nothing in the audit path requires write access.

### F7 — the failure path also writes nothing

`python3 plans/config_projection.py --json --root /tmp/fw/nonexistent-root` → exit `2`; strace shows
**0** writer opens and only `write(1,` — the could-not-evaluate path writes nothing.

### F8 — output is stdout-only in all three modes

`--summary`, `--json`, `--selftest` each: stderr 0 bytes; `2>&1 >/dev/null` produces empty output.
The instrument's docstring states "never read; no config_files/test.json or per-task file is ever
written. Output is stdout only." (`:8`), and the prereg states "Read-only and no network; output is
stdout, never writes real config_files/test.json or per-task benchmark files"
(`plans/round-29-claims.md:52`).

### F9 — receipts reproduce exactly

- `python3 plans/config_projection.py --json | sha256sum` → `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`,
  identical to `corpus/evidence/round29-calibration/build-json-sha256.txt` and identical across 3
  consecutive runs.
- `build-summary.txt` and `build-selftest.txt` differ from a fresh run only by the trailing
  `exit=0` line the recorder appended (`diff` reports `48d47 < exit=0` and `2d1 < exit=0`).

## MISMATCHES (defects)

### D1 — `would_be_file_sha256` is not reproducible from the instrument's own `--json` output (HIGH for the artifact's self-consistency; does not affect the write-surface claim)

**Location:** `plans/config_projection.py:333` (digest computed) versus `:541`
(`print(json.dumps(result, sort_keys=True, separators=(",", ":")))`).

`audit_text` computes, per task and profile:

    "would_be_file_sha256": hashlib.sha256(json.dumps(task, indent=2).encode("utf-8")).hexdigest()

where `task` is the projected object **in the source document's key order**. The `--json` emitter then
serializes the whole result with `sort_keys=True`, which re-sorts every nested object, so the
`projected_task` a consumer receives is key-sorted and the original order is **not recoverable** from
the output.

Measured, task index 0, profile `distinct_origins`:

- `would_be_file_sha256` as emitted: `9533088e31781047e4c4f3b9cafe02f734aaaa3fb9c47ebc29176bd8d6a6e5e6`
- recomputed from the emitted `projected_task` with `json.dumps(projected_task, indent=2)`:
  `823a9a7fd4ca2b16ae5d6e0c7966f22584691845bdb675832ad56983085aebcd`
- emitted key order is sorted (`list(projected_task) == sorted(projected_task)` → `True`)

Scale of the mismatch, measured over all three profiles: **2436 of 2436** task/profile records mismatch
when the digest is recomputed from the emitted `projected_task`. Cause confirmed independently:
`tasks where original-order digest == sorted-order digest: 0 of 812` — every task's original key order
differs from sorted order, so the two digests can never coincide.

**The digest value itself is correct.** Reproducing upstream's own write
(`json.dump(item, f, indent=2)`, `plans/fixtures/r29/generate_test_data.py:22-23`) for all 812 tasks
under each of the three profiles and hashing the resulting bytes gives **2436 of 2436** agreement with
the emitted `would_be_file_sha256`. So the field faithfully describes the file upstream *would* write;
it is the *published artifact* that is internally inconsistent — it ships a digest and a payload that
disagree, and no consumer can check one against the other. The prereg requires "per task/profile:
original task_id, output ordinal/filename, exact projected task object and changed leaf paths with
original/projected values" (`plans/round-29-claims.md:66-67`); the emitted `projected_task` is a
key-reordered rendering of that object, not the object upstream would serialize.

Scope note: this is a **publication/consistency** defect, not a write-surface defect. It does not
contradict the instrument's own write-surface claim (F2–F8 all hold). Fixes are outside this
read-only item.

### D2 — the selftest's containment is bounded by `TMPDIR`, and abnormal termination leaves a `config_files` tree behind (MEDIUM, environmental)

**Location:** `plans/config_projection.py:474` (the `TemporaryDirectory` root is `tempfile.gettempdir()`,
which honors `TMPDIR`/`TEMP`/`TMP`).

The claim "writes only inside tempfile" holds in the sense that every write lands inside a
`TemporaryDirectory` — but that directory's *location* is environment-controlled, and its contents
mirror the pinned fixture layout, including a directory literally named `config_files`.

Demonstrated with `TMPDIR` pointed inside the lane
(`.../scratch/falsify/FReviewWrites/killtest`), `timeout -s KILL 0.30 python3 plans/config_projection.py --selftest`:

    .../killtest/kengaku-r29-projection-ueq8zpr_/plans/fixtures/r28/webarena/config_files/test.raw.json

Under normal exit and under an injected exception the tree is removed (verified: residue empty after
both). Under `SIGKILL` it persists. Note the residue is **not** a projection output — it is a copy of
the pinned raw input — and it is git-ignored (`.gitignore:2` `__pycache__/` does not cover it, but the
whole `.ufo/` tree is untracked and `git status` shows it only as the pre-existing `?? .ufo/waves/round-29/scratch/falsify/`
entry; a per-file check confirmed no new top-level `git status` line appeared). The acceptance
criterion "no config_files output anywhere in the lane after runs" is therefore satisfied for the
instrument's *own* outputs, but a `TMPDIR`-scoped, killed selftest does deposit a `config_files/`
directory tree inside the lane tree.

With the default `TMPDIR` unset (`tempfile.gettempdir()` → `/tmp`), the killed run leaves residue in
`/tmp/kengaku-r29-projection-1vvm2yeu`, not in the lane; `git status` entries before and after: 10 and
10, unchanged.

### D3 — the lane `plans/__pycache__/config_projection.cpython-314.pyc` is NOT produced by the instrument (NOT a defect; attribution result)

`plans/__pycache__/config_projection.cpython-314.pyc` (mtime `2026-10-21 13:49:19`) appeared in the
lane during this review window but was **absent** from my pre-run inventory (`grep -c` → `0`).

Attribution test on a `/tmp` copy with `plans/__pycache__` deleted, then all three modes run: **no**
`plans/__pycache__` is created — running a script as `__main__` does not write its own bytecode cache,
and the mtime/size of the lane `.pyc` was unchanged across a further `--summary` + `--selftest` run.
Creating the `.pyc` requires *importing* the module: `python3 -c "import config_projection"` with
`sys.path` pointing at `plans/` does produce `plans/__pycache__/config_projection.cpython-314.pyc`.
So this file is attributable to a peer/agent that imported the module, not to the instrument's CLI. It
is git-ignored (`.gitignore:2` → `__pycache__/`). Recorded here because a reviewer diffing the lane
should not misattribute it.

## Verification gaps / residual risk

- **Attribution of `plans/__pycache__/config_projection.cpython-314.pyc` is inferred**, not proven to a
  specific process: the import-vs-run experiment proves the *mechanism* (import creates it, CLI does
  not) but not which agent imported at 13:49:19.
- **`strace` covers file-name syscalls and `write()`, not `mmap`/`memfd` writeback.** A write via
  `mmap` to an already-mapped file would not appear as a writer `open`. Mitigation: the full-tree
  inventory diff and the read-only-tree run (F5, F6) are syscall-independent and both show no mutation.
- **`PYTHONPYCACHEPREFIX` into the lane writes `.pyc` files there** — measured 5 `.pyc` files under the
  prefix directory. This is CPython's import machinery, not the instrument, and it is not a
  `config_files` output. It means "no writes in the lane" holds for the instrument but not for the
  interpreter under an adversarial `PYTHONPYCACHEPREFIX`.
- **`--selftest` inherits the ambient `TMPDIR`**, so D2 is reachable by configuration rather than by
  any defect in the instrument's logic.
- I did **not** execute the upstream generator itself (it imports `browser_env.env_config`, which is
  absent); the upstream-write reproduction in D1 was performed by re-implementing its exact two
  statements (`json.dump(item, f, indent=2)`) against the projected tasks, not by running it.
- The `write()` fd histogram in F3 (`2 write(1,`) reflects two buffered flushes for the 3.88 MB
  `--json` payload; no write reached any fd ≥ 2.
- Quote lengths in this report were counted programmatically; all quoted spans are ≤ 25 words.

## Verdict reasoning

The assigned write-surface claim is **upheld** on every probe attempted: `--summary` and `--json` make
zero writer opens (F2, F3), write only to fd 1 (F3, F8), work on a read-only tree (F6), and write
nothing on the failure path (F7); `--selftest` confines every write to the `TemporaryDirectory` root in
every traced PID including forked children (F4) and cleans up completely (F4, D2); the lane shows no
tracked modification, no new file under `plans/` or `corpus/`, and no `config_files` output anywhere
outside the pinned fixture input and peer scratch (F5); a pristine `/tmp` copy is byte-identical after
all three modes (F5); and the recorded build receipts reproduce exactly (F9).

Two mismatches remain: **D1**, a genuine self-consistency defect in the published `--json` artifact
(digest vs. payload disagree for 2436/2436 records; the digest is faithful to upstream but
unverifiable from what is shipped), and **D2**, an environmental bound on containment that can deposit
a `config_files`-named tree inside the lane when `TMPDIR` points there and the run is killed.

D1 is real, precisely located, and reproducible, and it is not the instrument's write surface. D2
weakens the containment boundary only under a non-default environment plus abnormal termination, and
the deposited tree is a copy of the pinned input rather than a projection output. Neither refutes the
write-surface claim as scoped; D1 is the one finding a maintainer should act on before admission.

VERDICT: PASS
