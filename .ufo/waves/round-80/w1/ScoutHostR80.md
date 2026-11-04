# ScoutHostR80 — per-surface host reconnaissance for the six R80-C1 replay instruments

Seat `ScoutHostR80`, role scout, round 80 wave w1. Read-only: no file in the lane, fleet repo, sibling
lane or domain tree was written except this report; no git/jj mutation was run. Scratch used
`/fast/scratch/hyaku/kengaku-r80/ScoutHostR80/` (220 K, deleted before yielding).

Lane tips observed while measuring (the lane integrated under me, so each result names its tip):
freeze `af51132d`, integration `6669fe72`, A2 `5b11bc5f`, A3 gate `bb3d6555`, A3 receipts `446b157f`,
then `14cfe3d0`, `84a89e4e`, `e985e56a`. Replay wall times were measured against the worktree at
`6669fe72`; the full gate was replayed at `446b157f` (result in §5).

## 0. Host baseline (commands and output, run 2026-11-04 04:24–04:46 -03)

```
$ openssl version
OpenSSL 3.6.5 29 Sep 2026 (Library: OpenSSL 3.6.5 29 Sep 2026)
built on: Tue Sep 29 15:51:51 2026 UTC   platform: linux-x86_64
$ uv --version
uv 0.13.0 (x86_64-unknown-linux-gnu)
$ python3 -V
Python 3.14.8
$ nproc
32
$ bwrap --version
bubblewrap 0.13.1
$ uname -a
Linux plazir27 7.2.11-arch1-1 #1 SMP PREEMPT_DYNAMIC Fri, 16 Oct 2026 00:28:58 +0000 x86_64 GNU/Linux
$ cat /proc/sys/kernel/unprivileged_userns_clone
1
$ bwrap --unshare-all --die-with-parent --ro-bind /usr /usr --symlink usr/lib /lib \
    --symlink usr/lib64 /lib64 --symlink usr/bin /bin --proc /proc --dev /dev \
    /usr/bin/python3 -c "print('bwrap-ok')"      # (plus /etc bind, tmpfs /tmp,/home in the probes)
bwrap-ok        rc=0
$ bwrap ... /usr/bin/python3 -c "import sys,numpy;print(sys.version.split()[0], numpy.__version__, numpy.__file__)"
3.14.8 2.5.4 /usr/lib/python3.14/site-packages/numpy/__init__.py
$ bwrap ... /usr/bin/python3 -c "import os;print(os.cpu_count())"
cpu_count 32
$ uv run --no-project --with biopython python3 -c "import Bio,sys;print(Bio.__version__, sys.version.split()[0])"
Bio 1.88 py 3.15.0                         (wall 0.03 s)
$ uv python list | head -1
cpython-3.15.0-linux-x86_64-gnu  /home/vgpnk/.local/share/uv/python/cpython-3.15-linux-x86_64-gnu/bin/python3.15
$ curl -s https://pypi.org/pypi/biopython/json | jq -r .info.version
1.88
$ uv cache dir; du -sh ~/.cache/uv
/home/vgpnk/.cache/uv ; 5.6G
$ find ~/.cache/uv -name 'biopython-*.dist-info'
…/archive-v0/KBqMtmdSKTwsoXnX/biopython-1.88.dist-info
…/archive-v0/ef9CXPmyx2GRXUPy/lib/python3.15/site-packages/biopython-1.88.dist-info   # only 1.88 exists
```

## 1. Per-probe host surface

All five TB2 probes build a `bwrap --unshare-all` sandbox (`/usr` ro, `/etc` ro, `/proc`, `/dev`,
tmpfs `/tmp` and `/home`, probe-owned `/tests` and `/stub`, writable `/app`) and execute the graded
code with **`/usr/bin/python3`** inside it. The probe process itself runs under the gate's
`sys.executable` (default `/usr/bin/python3`); `protein-assembly` is the exception — no sandbox, run
through `uv`. Network is unshared in all five sandboxes; only `uv` can reach the network.

| member | sandbox | graded interpreter | third-party in sandbox | external binaries / host state | dynamic inputs | `--selftest` | replay wall |
|---|---|---|---|---|---|---|---|
| cancel-async-tasks | bwrap | `/usr/bin/python3` 3.14.8 | none (stdlib `asyncio`, `signal`, `subprocess`) | bwrap; unprivileged userns; SIGINT delivery through the PID ns; wall clock | 3 s task sleeps, SIGINT at 0.5 s, `communicate(timeout=5)`, `elapsed >= 6` | pass (2.46 s) | **161.60 s** |
| chess-best-move | bwrap | 3.14.8 | none (`pathlib` only) | bwrap; userns | none | pass (0.08 s) | 0.26 s |
| distribution-search | bwrap | 3.14.8 | **numpy 2.5.4 from `/usr`** (`float64`, KL sums; grader asserts `abs(sum-1)<1e-5`, `kf/kb <= TOL`) | bwrap; userns; system numpy | none | pass (0.13 s) | 0.58 s |
| largest-eigenval | bwrap | 3.14.8 | **numpy 2.5.4 from `/usr`**; grader uses `ProcessPoolExecutor(max_workers=1)` | bwrap; userns; system numpy; **wall-clock race** | `test_speedup` compares two medians of identical code (`assert dt < ref_dt`) | pass (0.23 s) | 2.15 s |
| openssl-selfsigned-cert | bwrap | 3.14.8 | none | **`openssl` 3.6.5 CLI** (`genrsa`, `req -x509`, `x509 -subject/-dates/-fingerprint`), `/etc/ssl` ro bind, key/serial randomness, filesystem mode bits | `-days 365`; grader computes `notAfter-notBefore == 365` from the cert itself (no host-clock dependence) | pass (0.09 s) | 1.07 s |
| protein-assembly | **none** | **uv-managed CPython 3.15.0** | **biopython 1.88** from the uv cache | uv 0.13.0; uv python 3.15.0; biopython resolution (cache or PyPI) | Biopython version string is printed into the block (`biopython=1.88`) | **none** (`--selftest` is an argparse error: `unrecognized arguments: --selftest`) | 0.13 s |

Notes measured, not inferred:

- `plans/tb2_grader_probe.py`'s own docstring says `--with biopython==1.85`, but the frozen table
  (`plans/round80_probes.json`) runs `uv run --no-project --with biopython` (unpinned). Today the
  unpinned form resolves **1.88**, and `uv run --offline --with biopython==1.85 …` **fails**:
  `because biopython==1.85 needs to be downloaded from a registry and you require biopython==1.85,
  we can conclude that your requirements are unsatisfiable` (only 1.88 is cached).
- The historical round-35 receipt was produced with `biopython=1.85`; every round-80 replay prints
  `biopython=1.88`. That single field is the whole protein historical divergence (see §5).
- Interpreter substitution is safe for the five sandboxed probes: `uv run --no-project python3
  plans/round58_c2_kl_probe.py …` and `plans/round55_c3_chess_probe.py …` produce the same verdicts
  (the graded legs always execute under the sandbox's `/usr/bin/python3`). What is *not* safe is a
  change to `/usr/bin/python3` itself or to `/usr/lib/python3.14/site-packages/numpy`.
- CPU count does **not** leak into any prediction: cancel uses n=2 tasks, and the eigen grader pins
  `ProcessPoolExecutor(max_workers=1)`. The sandbox does expose 32 CPUs, but nothing consumes it.

## 2. Dependencies NOT covered by the receipt stamp

The stamp the gate requires is exactly
`MEMBER, SOURCE_RECEIPT, SOURCE_SHA, TOOL, TOOL_SHA, LANE_TIP, WORKTREE, COMMAND, EXIT, MINTED_BY`
(`REQUIRED` at `plans/round80_c1_located_replay.py:71`, plus `MINTED_BY_SHA` after amendment A3).
**No stamp field records a host fact.** What a replay can silently change tomorrow, ranked by
measured risk:

1. **Biopython resolution (protein-assembly) — can change with no lane byte changing.**
   `--with biopython` is unpinned; the cache holds only 1.88 and PyPI's latest is 1.88 today. The
   resolved version is copied verbatim into the compared block (`grader=… biopython=1.88`). The day
   a 1.89 is published, an online replay re-resolves to it and the block no longer matches the
   committed bytes → `REPRODUCTION-MISMATCH` (a `DEFECT`, not a noted divergence). Pruning
   `~/.cache/uv` (5.6 G) also makes replay depend on network access.
2. **The eigen speed leg is a wall-clock coin flip — measured, not theoretical.**
   `test_speedup` asserts `dt < ref_dt` on two medians of the *same* algorithm
   (`corpus/evidence/round57/tb2-eigenval/tests/test_outputs.py:92-111`). Nine runs of the frozen
   probe on this unchanged host gave `OBSERVED-U eig-bare-speed-s10` = `P P F P F P P F F`
   (5 P / 4 F). Against the committed block (`s10=F`) the **full-block bytes matched 4/9 runs**;
   the A2 projection matched 9/9. Before A2 the full-block comparison failed 5 of 9 runs (56 %) on
   an untouched lane.
3. **System Python + numpy inside `/usr` (five probes).** The sandbox binds `/usr` read-only, so
   `python3` 3.14.8 and numpy 2.5.4 (for distribution-search and largest-eigenval) are the graded
   runtime. A host upgrade of either is invisible to every stamp; failures arrive as `SETUP`/rc!=0
   (`REPRODUCTION-EXIT`) or as numerically different legs (`REPRODUCTION-MISMATCH`).
4. **`openssl` 3.6.5 CLI text (openssl-selfsigned-cert).** The captured grader parses
   `openssl rsa -text` (2048-bit leg) and `x509 -subject/-dates/-fingerprint`; a CLI/format or
   default-provider change in the host openssl flips legs. The version is in no stamp; only the
   `openssl` path is inside the sandbox.
5. **bwrap + unprivileged user namespaces (five probes).** `/usr/bin/bwrap` 0.13.1 and
   `kernel.unprivileged_userns_clone=1` are prerequisites; without them every sandboxed probe
   prints `SETUP` and exits 2 (the probes explicitly test `pathlib.Path(BWRAP).exists()` only, not
   userns). Not recorded anywhere in the receipt.
6. **Kernel signal semantics and the timing constants (cancel-async-tasks).** The decisive teeth are
   `subprocess.run(..., timeout=5)` with 3 s tasks, SIGINT at 0.5 s, `communicate(timeout=5)` and
   `elapsed >= 6` (`corpus/evidence/round61/.../test_outputs.py:28,92-96,161-165`). The `elapsed>=6`
   band sits 1 s above the 5 s timeout. The slow-host direction is safe (sleeps only lengthen), but
   the compliant/cleanup legs require a 5 s post-SIGINT completion under a loaded kernel.
7. **Network.** Only `uv` may touch it; the five sandboxes are `--unshare-all`. PyPI was reachable
   today (`HTTP/2 200`), so a cold uv cache would silently need it.

Not a dependency (checked and excluded): host clock (openssl validity is measured cert-internally),
CPU count (§1), probe-process interpreter for the five sandboxed probes (§1), lane worktree
cleanliness (asserted at mint time only, `WORKTREE clean`, not re-verifiable later), and the literal
`COMMAND` lines: they name scratch paths from the mint
(`/fast/scratch/hyaku/kengaku-r80/remint4-work/…`), which are ephemeral — a replay must re-render
argv from the frozen probe table, as the gate does.

## 3. Slowest probe and the gate's timeout bound

```
$ python3 - <<'EOF'   # the gate's own argv/prefix/timeout, cwd=lane, sequential
… subprocess.run(cmd, cwd='.', timeout=spec['timeout']) … EOF
cancel-async-tasks         rc=0 wall= 161.60s timeout=420 stdout_lines=15
chess-best-move            rc=0 wall=   0.26s timeout=240 stdout_lines=14
distribution-search        rc=0 wall=   0.58s timeout=240 stdout_lines=15
largest-eigenval           rc=0 wall=   2.15s timeout=240 stdout_lines=27
openssl-selfsigned-cert    rc=0 wall=   1.07s timeout=300 stdout_lines=15
protein-assembly           rc=0 wall=   0.13s timeout=300 stdout_lines=21
```

**Slowest: `cancel-async-tasks`, 161.60 s** (12 cases; sleep-bound — two further runs took 323.35 s
for two, i.e. ~161.7 s each, and all three produced byte-identical blocks). The gate's per-probe
timeout is `timeout=int(spec.get("timeout", 300))` = **420 s**, so it bounds the probe with 2.60×
headroom; the probe's own wall time did not grow under load because it is dominated by its fixed
sleeps (measured while ~100 seats were live on 32 cores). Full-gate wall, including all six replays
plus the 900 s population-ledger subprocess (measured 0.18 s), was **166.31 s** and **166.25 s** on
two runs. There is no global gate timeout — only the per-probe values from
`plans/round80_probes.json`, which are sufficient for this host.

## 4. Scratch space

```
$ df -B1 /fast/scratch | tail -1          # 04:45 -03
/dev/nvme1n1p2 862342868992 469967093760 392375775232  55% /fast     # 392,375,775,232 B ≈ 365 GiB free
$ du -sh /fast/scratch/hyaku/kengaku-r80
9.3G
$ du -sh /fast/scratch/hyaku/kengaku-r80/* | sort -h | tail -4
671M …remint3   671M …remint4   813M …ReviewerC1R80
$ find /fast/scratch/hyaku/kengaku-r80 -type f -printf '%s %p\n' | sort -n | tail -1
24325657 …/ReviewerC1R80/uv-cache/…/numpy.libs/libscipy_openblas64_-f48b354e.so
$ du -sh /fast/scratch/hyaku/kengaku-r80/ScoutHostR80
220K
```

**Free: 392,375,775,232 bytes (≈365 GiB), 55 % of the 804 GB filesystem used** (it moved from
396.8 G free at 04:26 to 392.4 G at 04:46 as the wave minted). The round's scratch measured
**9.3 G total** and was still growing with active seats. Above 50 MB: yes, per directory — thirteen
seats hold a ~667–671 MB lane checkout each (`--shared` clones still materialise the full working
tree), and one seat's private uv cache is 142 MB. No single **file** exceeds 50 MB: the largest is
24,325,657 B (a numpy OpenBLAS `.so` inside a uv cache). My own scratch measured 220 K at the end
because every probe deletes its `--work` temp tree.

## 5. What I attacked, what broke, what held

**Attacked (all with commands re-run against committed bytes):**

1. *Reproduction stability of each replay.* Ran the exact frozen argv once per member, then extra
   runs against the committed `OBSERVATIONS_BEGIN…END` block (REV stripped, as the gate does):
   1 + 3 for chess/kl/openssl/protein, 1 + 2 for cancel, 1 + 8 for eigen.
   - Held byte-identical: cancel 3/3, chess 3/3, distribution-search 3/3, openssl 3/3,
     protein-assembly 3/3 (every run equals the committed block line-by-line).
   - **Broke: `largest-eigenval`.** Full block matched the committed receipt in only **4/9** runs;
     `OBSERVED-U eig-bare-speed-s10` alternated `P P F P F P P F F`. Under the A2 projection the
     same nine runs match **9/9**. This is the same finding A2's commit message records; my runs are
     an independent reproduction of it (different process, same host, minutes apart).
2. *Biopython/toolchain substitution.* `protein-assembly` under the probe's own documented pin
   (`--with biopython==1.85`) **cannot run offline** (not cached); the frozen table's unpinned
   `--with biopython` resolves 1.88 and reproduces the committed block exactly. `--offline` works
   today with 1.88.
3. *Interpreter substitution.* Running the probes under uv's CPython 3.15.0 instead of
   `/usr/bin/python3` leaves the five sandboxed verdicts unchanged (the graded code runs under the
   sandbox interpreter).
4. *Divergence-note basis.* The driver (`plans/round80_c1_remint.py:122-140`) computes the note from
   `proj(obs_lines(historical))`, while the gate compares
   `projection(whole historical file)`. The protein note therefore reads
   `HISTORICAL-DIVERGENCE 2 … produces 20 comparable lines where the historical receipt has 18`,
   but the gate's basis is **20 vs 20 with exactly one differing line** —
   `… biopython=1.85` (historical) vs `… biopython=1.88` (round 80). The note's `2` is the header
   lines the historical's observation slice lacks, not a count of changed observation content. The
   gate only requires `^HISTORICAL-DIVERGENCE \d+`, so this passes, but a member whose *only*
   divergence sat in a non-observation line would get no note from the driver and be flagged
   `DIVERGENCE-UNNOTED` by the gate — the two sides do not share a comparison basis.
5. *Gate state across the integration.* Six runs, each pinned to the bytes it could read:
   - 04:35, gate file being rewritten (mtime 04:36:58), receipts from `6669fe72`:
     `TARGET members=6 located=5 reproduced=6 ledger_flipped=6 diverged=2 defects=1`,
     `DEFECT DIVERGENCE-UNNOTED protein-assembly`, `PREDICATE R80-C1 fail` (rc 1). [INFERENCE: since
     the committed `6669fe72` gate bytes now yield `defects=0` on the same receipts, the process must
     have loaded an in-progress projection-based revision, which sees the `biopython=1.85/1.88`
     header line as divergence.]
   - `6669fe72` gate bytes against the current worktree (obs-lines comparison):
     `located=6 reproduced=0 ledger_flipped=6 diverged=2 defects=0`, pass (no replay).
   - `bb3d6555` gate bytes before A3 receipts landed:
     `DEFECTS n=13` = 6 `STAMP-MISSING … MINTED_BY_SHA` + 6 `MINTED-BY-SHA-MISMATCH` +
     1 `DIVERGENCE-UNNOTED protein-assembly`; fail.
   - `446b157f` gate with full replay (the state that matters):
     `TARGET members=6 located=6 reproduced=6 ledger_flipped=6 diverged=2 defects=0`,
     `LEDGER-GATE rc=0 executed=24 unlocated=0 defects=0`, `PREDICATE R80-C1 pass`, rc 0, wall 166.25 s.
   - `14cfe3d0` static re-check (`--no-reproduce`): same TARGET with `reproduced=0` by construction,
     `defects=0`, pass.
   - `e985e56a` static re-check: unchanged, `defects=0`, pass. Across `446b157f → 84a89e4e → e985e56a`
     `git diff --name-only` touches **no** C1 file (gate, driver, probe table, six receipts), so the
     `446b157f` replay verdict stands for the later tips.
6. *Scratch/space attack.* Ran probe replays and the full gate concurrently; no probe wrote outside
   its `--work` temp tree (its own `TemporaryDirectory(dir=a.work)`), no `/tmp` path was needed, and
   every probe-end deletes the tree (my scratch ended at 220 K).

**Could not break:** the five non-eigen replays' committed blocks (3/3 each), bwrap/userns sandboxing,
openssl determinism (12 cases, 3/3 identical), the unshared network in the sandboxes, the
`elapsed >= 6` / `timeout=5` bands under 3-way concurrent cancel runs, and the C1 gate at `446b157f`.

**Residual unknowns (stated, not hidden):** (a) cold-uv-cache behaviour was not tested — clearing the
shared 5.6 G cache would damage sibling seats; the 1.85 offline failure is the proxy evidence.
(b) The eigen speed leg was sampled 9 times, enough to show ~50/50 at s10 but not to bound it.
(c) Host-dependence of the cancel timing legs was tested only on this 32-core host.

## 6. Tooling

No installs or upgrades. `pacman` untouched; nothing written under `~/.local/bin` or any PATH
directory. All commands above use the host's existing `openssl 3.6.5`, `uv 0.13.0`, `python3 3.14.8`,
`bwrap 0.13.1`, numpy 2.5.4.
