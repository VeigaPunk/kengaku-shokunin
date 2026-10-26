# R37ProbeRerun — determinism and environment sensitivity of the frozen C2 probe

Seat: executor, round 37 wave 1. Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (read-only for this seat).
Scratch `S=/fast/scratch/hyaku/kengaku-r37/R37ProbeRerun` (NVMe), `TMPDIR` under it, deleted at the end.
Nothing in `corpus/`, `plans/`, the lane git index or jj state was written; no tool was installed (pacman paused; `uv` and
`bwrap` already present).

## 1. Frozen inputs

```
$ sha256sum plans/git_webserver_probe.py
63cb75cfcd1c224a38eef34b99b66c9ec837261ca8c369577b23601ed3a5eedf  plans/git_webserver_probe.py
$ sha256sum corpus/evidence/round37/git-webserver-probe.txt
835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8  corpus/evidence/round37/git-webserver-probe.txt
$ wc -l corpus/evidence/round37/git-webserver-probe.txt
49
```

Probe digest matches `PROBE_SHA256` in `plans/round37_c2_verify.py:44` and the C2 claim's `63cb75cf…5eedf`
(`plans/round-37-claims.md`, C2). Host: Python 3.14.8, `bubblewrap 0.13.1`, `curl 8.23.0`, `GNU Wget 1.25.0`,
32 cores; host `python3` has **no** `Bio` module (`ModuleNotFoundError: No module named 'Bio'`), so the gate's P10 takes its
`uv` fallback (`plans/pkg_gate.py:272-276`).

## 2. Determinism matrix — 8 full runs, all 22 cases each

Every run: `python3 plans/git_webserver_probe.py …`, 22 cases, exit 0, printed 8529 bytes.
Receipt digest is the reference: `835507129cb536ff…`.

| # | variation | command (abridged) | rc | bytes | sha256(16) | == receipt | wall |
|---|---|---|---|---|---|---|---|
| A | lane cwd, `--work $S/w1` | `python3 plans/git_webserver_probe.py --lane <lane> --work "$S/w1"` | 0 | 8529 | `835507129cb536ff` | yes | 52.72 s |
| B | repeat of A, same `--work` dir reused | same as A | 0 | 8529 | `835507129cb536ff` | yes | 52.70 s |
| C | `TMPDIR=$S/t1`, no `--work` | `--lane <lane>` | 0 | 8529 | `835507129cb536ff` | yes | 52.69 s |
| D | `TMPDIR=$S/t2` (different dir), no `--work` | `--lane <lane>` | 0 | 8529 | `835507129cb536ff` | yes | 52.70 s |
| E | `LANG=C`, `LC_ALL`/`LC_CTYPE`/`LC_MESSAGES` unset, `LANGUAGE=C` | `--lane <lane>` | 0 | 8529 | `835507129cb536ff` | yes | 52.69 s |
| F | different cwd (`$S/elsewhere`), absolute script + lane | `python3 <lane>/plans/git_webserver_probe.py --lane <lane>` | 0 | 8529 | `835507129cb536ff` | yes | 52.70 s |
| G | the gate's P10 shape: `uv run` + Biopython, cwd = lane | `uv run --no-project --with biopython==1.85 python3 plans/git_webserver_probe.py --lane .` | 0 | 8529 | `835507129cb536ff` | yes | 52.70 s |
| H | minimal env: `env -i PATH=/nonexistent TMPDIR=$S/tmp` | `env -i … /usr/bin/python3 plans/git_webserver_probe.py --lane <lane>` | 0 | 8529 | `835507129cb536ff` | yes | 52.71 s |

Receipts: `runA.txt` (A), `runG.txt` (H, minimal env), `matrix.json` (B–G with rc/bytes/digest/stderr per run) — all
three copied beside this report, byte-identical to `corpus/evidence/round37/git-webserver-probe.txt`:

```
$ sha256sum runA.txt runG.txt
835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8  runA.txt
835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8  runG.txt
```

**Byte differences recorded: none.** All 8 runs, under every variation, produced zero differing bytes and empty stderr.
That is the whole point of the probe's own design (`plans/git_webserver_probe.py:26-27`: "Deterministic receipt: no temp
path, timing or host version is printed"), and it holds under the variations the gate actually exercises and several it
does not.

Cause of each non-difference, read from the code whose output is invariant:

- **`--work` / `TMPDIR`**: scratch path is never printed; `root = tempfile.mkdtemp(prefix="k37-cgw-", dir=a.work)`
  (`git_webserver_probe.py:271`) is only a parent for per-case dirs, removed in the `finally`
  (`:306`). After all runs, `ls -A $S/w1 $S/t1 $S/t2 $S/tmp` printed four empty dirs — no residue, no path leak.
- **cwd**: `lane = pathlib.Path(a.lane).resolve()`, captures resolved from the lane (`:251-253`); the probe never reads
  the cwd.
- **parent locale**: `run_case` builds the child env itself —
  `{"PATH": "/work/bin", "HOME": "/work/home", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONUTF8": "1", …}`
  (`:235-236`), so the sandboxed grader never sees `LANG=C` or a missing `LC_ALL`; host-side output is ASCII plus fixed
  literals copied from the case table.
- **interpreter**: the case bodies run `/usr/bin/python3` inside the sandbox (`RUN_SH`, `:195`), i.e. host 3.14.8 in both
  the plain and `uv` runs; `uv`'s 3.13.16/Bio-1.85 environment only executes the probe's own driver, which enforces the
  same pins before any case.
- **outer `PATH`**: the probe invokes `BWRAP = "/usr/bin/bwrap"` (`:49`) and, inside the sandbox, `/usr/bin/sleep` (`:191`) and
  `exec /usr/bin/python3 /work/HARNESS` (`:195`), with `/work/bin/*` symlinks built from `BASE_TOOLS` (`:219-225`); run H with `PATH=/nonexistent` still passed,
  so no host command lookup depends on the parent PATH.

### 2.1 The `uv` path is same-output but a different Python

```
$ uv run --no-project --with biopython==1.85 python3 -c 'import sys,Bio;print("python",sys.version.split()[0],"Bio",Bio.__version__)'
python 3.13.16 Bio 1.85
```

vs. host `python3` 3.14.8 with no `Bio`. Output equal (run G/H, digest `835507129cb536ff`). The gate's P10 chooses
between these two interpreters by `import Bio` success (`plans/pkg_gate.py:272-276`), so which interpreter runs the driver
is host-dependent while the receipt is not. Useful, but see risk R3 below for what the comparison actually checks.

## 3. Runtime

Full probe run: **52.7 s** (8 runs: 52.69–52.72 s), i.e. ≈2.4 s per case, dominated by bwrap setup, `curl`/`wget`
invocations and the one `slow-server-3s` case (`git_webserver_probe.py:112`). Headroom against the gate's
`timeout=600` in `c_rerun` (`plans/pkg_gate.py:278`) is ≈11×; the per-case `timeout=180` (`:238`) is never approached
(the slowest case has a 3 s server delay).

The C2 counter run (§4) takes 52 s total — V2's gate P10 subprocess is the whole cost; V1/V3–V7 are file reads plus the
census script.

## 4. C2 counter, read-only against the lane (expected red)

```
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round37_c2_verify.py \
    --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin --work "$S"
V1 ok listed=6 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 DEFECT no '## Located quotes' section
    gate: P4 DEFECT no parsed quote
    gate: P5 ok manifest_entries=6 bad=0 first=0
    gate: P6 DEFECT rows=3 bad=3 first=S111: rows=0
    gate: P7 DEFECT entry unreadable
    gate: P8 DEFECT index_rows=43 knowledge_files=43 bad=2 first=index rows for knowledge/tb2-git-webserver-grader.md=0
    gate: P9 DEFECT untracked=165 first=.ufo/waves/round-37/assimilation/c2-collisions
    gate: P10 ok probe_rerun=byte-equal bytes=8443
    gate: defects=6
V2 DEFECT gate_exit=1
V3 DEFECT rows=3 bad=['S111:row', 'S112:row', 'S113:row']
V4 DEFECT receipt or entry absent
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 DEFECT receipt or entry absent
checks=7 defects=4
PREDICATE C2 fail
exit=1
```

Raw output: `c2.out` beside this report (`sha256 c596301f5473a2d3…`); stderr empty (`c2.err`, 0 bytes).

Red causes, each traceable to a wave-1 (not yet landed) artifact:

- **V4/V7 and P7** — `corpus/knowledge/tb2-git-webserver-grader.md` is absent (`spec["entry"]` in
  `plans/pkg-spec-r37.json`), so the receipt/entry pairing and the requirement map cannot be read
  (`round37_c2_verify.py:122-128`, `:167-173`).
- **V3/P6** — no `S111`/`S112`/`S113` rows in `corpus/SOURCES.md` yet (`rows=0` each; `bad=3`).
- **P8** — no README index row for `knowledge/tb2-git-webserver-grader.md` (`index rows …=0`; the "bad=2" is the missing
  index row plus the missing coverage bullet for the entry — `pkg_gate.py:237-251`).
- **P3/P4** — the entry is where `## Located quotes` lives, so quote shape and verbatim support are unreadable.
- **P9** — the lane tree is dirty at round-37 wave-1 build time: `untracked=165`. (`git status --porcelain` shows 9
  lines because it collapses directories; `git ls-files --others` lists per file, which is what the gate counts.)
  Expected for an in-flight wave; V2 cannot pass on an uncommitted tree by design.
- **Green already**: V1 (6 captures at their pins), V5 (probe at freeze digest, `--dry` byte-equal to
  `git-webserver-dry-cases-freeze.txt`), V6 (census exit 0), and **P10** — the gate's own fresh probe re-run compared
  equal to the receipt inside the counter (`probe_rerun=byte-equal`), from a cwd of the lane with `--lane .`, i.e. the
  same shape I re-ran by hand as run G.

## 5. Risks and limits (reported, nothing edited)

- **R1 — P10's "byte-equal" is a decoded-text compare.** `c_rerun` uses `subprocess.run(..., text=True)` and
  `read()` = `path.read_text()` (`plans/pkg_gate.py:37-39`, `:278`, `:283-285`), so it compares Python strings, not bytes:
  the note's `bytes=8443` is 8443 characters — the receipt is 8529 bytes / 8443 chars, a delta of 43 non-ASCII
  characters × 2 extra UTF-8 bytes (`len(read_text())`; probe output is one line per case). Consequences: a receipt
  re-encoded to another normal form, or one with CRLF, would still compare equal to an LF fresh run (universal-newline
  translation), and an emoji-carrying line differs from a byte compare by up to 3×. My own byte compare
  (`cmp`, digest `835507129cb536ff…`) is the strict one; the gate's is laxer than its label. Frozen — calibration
  observation only.
- **R2 — hard host prerequisites.** The probe aborts with exit 2 if `/usr/bin/bwrap` is missing or unexecutable
  (`git_webserver_probe.py:268-270`), and the sandbox binds host `/usr`, `/etc`, `/dev`, `/proc`; `/usr/bin/python3`
  inside the sandbox is the host interpreter. A host with a different `http.server`/`urllib` behaviour or without
  bwrap changes the result class (SETUP abort, or different bodies), not the receipt.
- **R3 — `expect` masking is host-conditional by construction.** `if os.path.exists("/usr/bin/expect"): --ro-bind
  /dev/null /usr/bin/expect` (`:214-215`) makes `expect` absent everywhere; here it is absent anyway. Not exercised on a
  host that has `expect`, so the branch is code-read, not observed.
- **R4 — timing headroom is comfortable but P10 is the gate's slowest clause.** 52.7 s against 600 s; a cold `uv` cache
  would add download time to run G. On this host the `uv` env resolved instantly (cached 3.13.16/Bio-1.85).
- **R5 — determinism is observational across 8 runs on one host.** It shows the receipt is reproducible under the
  variations P10 and a reviewer plausibly apply (cwd, TMPDIR, locale, PATH, interpreter, uv); it cannot show a different
  kernel/bwrap/curl build agrees. Same limit class the C2 claim names ("demonstration is observational").
- **R6 — no lane writes observed.** The probe's only writes are under its `--work`/`TMPDIR` root (`:271`) and per-case
  `work` dirs (`:231-241`); scratch parents were empty after every run, and the durable copies I made are all under this report dir.

## 6. Files written

- `.ufo/waves/round-37/build/R37ProbeRerun.md` (this report)
- `.ufo/waves/round-37/build/R37ProbeRerun/runA.txt` — run A output (8529 B, `sha256 835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8`)
- `.ufo/waves/round-37/build/R37ProbeRerun/runG.txt` — run H (minimal env) output, same digest
- `.ufo/waves/round-37/build/R37ProbeRerun/matrix.json` — per-run rc/bytes/digest/stderr for B–G
- `.ufo/waves/round-37/build/R37ProbeRerun/c2.out`, `c2.err` — counter stdout (852 B) and empty stderr

Scratch `/fast/scratch/hyaku/kengaku-r37/R37ProbeRerun` removed after the copies. No dependency or tool changes.

For the L1: the probe is deterministic in every variation asked for; V2's remaining redness is wave-1 absence of the
entry, rows, index row and clean tree, not probe behaviour; the one calibration nit worth a routed item is R1 (P10
compares decoded text under a "byte-equal" label).

VERDICT: probe-deterministic-yes-uv-same-runtime-52.7s
