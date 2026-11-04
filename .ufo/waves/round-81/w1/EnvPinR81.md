# EnvPinR81 — host-state measurement + round-80 A2 re-measurement

Seat: EnvPinR81 (executor, leaf). Date: 2026-11-04. Lane: `kengaku-shokunin`.
Deliverable written outside scratch: `.ufo/waves/round-81/w1/host-state.txt` (item 1).
Scratch: `/fast/scratch/hyaku/kengaku-r81/EnvPinR81` — deleted after this report was written;
every byte of evidence is reproduced below. No tools installed or upgraded (nothing needed;
pacman paused per orchestrator ruling 2026-10-20).

Lane tips observed while measuring (sibling seats were landing commits throughout):
`ca9bfe791422597e4d5ce0ab032c9eed7eac40c8` (session start) → `6781dd001236f2947fbedf87282b569c2818571d`
→ `7a24356474e64c63a3f6ceb663bf6d6bc1703c34` → `604be35096e41be92e1013a38daff08d5a114959` (tip when
host-state.txt was finalized). Freeze commit `4d896e0daf8831ef7a0016bf3c944d11ba465f70` present
(`git cat-file -t` → `commit`); base `4e833e9fee8022d24559535178c6fe32b2cd62f1` verified as commit.
The A2 measurement reads only `corpus/evidence/round57/tb2-eigenval/tests/test_outputs.py`, which the
probe sha256-checks against its frozen pin before executing, so tip drift cannot alter measured bytes.

## 1. Host state (item 1)

Commands (each line of host-state.txt is labelled with its command; outputs are exact stdout):

```
$ python3 -V            # rc 0; stdout only, stderr empty
Python 3.14.8
$ openssl version       # rc 0
OpenSSL 3.6.5 29 Sep 2026 (Library: OpenSSL 3.6.5 29 Sep 2026)
$ bwrap --version       # rc 0; /usr/bin/bwrap exists (mode -rwxr-xr-x, 84464 bytes)
bubblewrap 0.13.1
$ uname -r
7.2.11-arch1-1
$ python3 -c 'import sys;print(sys.executable)'      # rc 0
/usr/bin/python3
$ sha256sum /usr/bin/bwrap
33516b9cd1fa6432307ad71f23765fa30604b0a8d769dac0d2ba054e85aeec83  /usr/bin/bwrap
```

host-state.txt final bytes (header names the tip at write, `604be35096e41be92e1013a38daff08d5a114959`,
and the observed drift chain):

```
# host-state.txt — seat EnvPinR81, kengaku round 81 w1
# measured 2026-11-04; lane tip at write: 604be35096e41be92e1013a38daff08d5a114959
# lane tip moved repeatedly during the wave: ca9bfe79... -> 6781dd00... -> 7a243564... -> 604be350... (tip at write); see EnvPinR81.md
[python3 -V]
Python 3.14.8
[openssl version]
OpenSSL 3.6.5 29 Sep 2026 (Library: OpenSSL 3.6.5 29 Sep 2026)
[bwrap --version]
bubblewrap 0.13.1
[uname -r]
7.2.11-arch1-1
[python3 -c 'import sys;print(sys.executable)']
/usr/bin/python3
[sha256sum /usr/bin/bwrap]
33516b9cd1fa6432307ad71f23765fa30604b0a8d769dac0d2ba054e85aeec83  /usr/bin/bwrap
```

## 2. Round-80 A2 re-measurement (item 2)

Instrument unchanged since round 80:

```
$ sha256sum plans/round57_c2_eigen_probe.py
4f2b8bebb451c5f67d26dc06c76dbd99f3a459f41d9e8a8d555af12d15e0f105  /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round57_c2_eigen_probe.py
```

Six runs, all with cwd = lane root, in parallel (n = 1..6):

```
python3 plans/round57_c2_eigen_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r81/EnvPinR81/eigen-<n>
```

All six exited 0; all six stderr captures were 0 bytes.

Frozen A2 projection rule (`plans/round-80-claims.md`, "Freeze amendment A2"; same sentence in
`plans/round-81-claims.md` §R81-C1): the compared projection drops `REV <commit>` lines, `cases=`
summaries and `OBSERVED-U` lines, and any `CASE`/`case=` line whose predicted field contains `U`.
Applied mechanically as:

```
grep -vE '^(REV |cases=|OBSERVED-U )' eigen-<n>.stdout | grep -vE '^(CASE|case=).*predicted=U' | sha256sum
```

Per-run results (full-stdout sha256; projection sha256; the two U-case outcomes):

| run | full stdout sha256 | projection sha256 | eig-bare-speed-s2 | eig-bare-speed-s10 |
|---|---|---|---|---|
| 1 | 463877700639fcf7a522b207cbf88a3a6eebd2aa40d6afd5e1c258087ce8c784 | c5006e8e6d1e1ce86d9895fc07b12db3ebaa60aa9227477a7c9972016b41bd47 | F | P |
| 2 | d44ecaed4ca81ca14344fe04aeb95f485e5c1ebe10e0a0a218d899138b839bb6 | c5006e8e6d1e1ce86d9895fc07b12db3ebaa60aa9227477a7c9972016b41bd47 | F | F |
| 3 | d44ecaed4ca81ca14344fe04aeb95f485e5c1ebe10e0a0a218d899138b839bb6 | c5006e8e6d1e1ce86d9895fc07b12db3ebaa60aa9227477a7c9972016b41bd47 | F | F |
| 4 | 9498d376c2d6c063535c22aafe774e4bf6d58a2b00505bad37bcc6195746554e | c5006e8e6d1e1ce86d9895fc07b12db3ebaa60aa9227477a7c9972016b41bd47 | P | F |
| 5 | 463877700639fcf7a522b207cbf88a3a6eebd2aa40d6afd5e1c258087ce8c784 | c5006e8e6d1e1ce86d9895fc07b12db3ebaa60aa9227477a7c9972016b41bd47 | F | P |
| 6 | 463877700639fcf7a522b207cbf88a3a6eebd2aa40d6afd5e1c258087ce8c784 | c5006e8e6d1e1ce86d9895fc07b12db3ebaa60aa9227477a7c9972016b41bd47 | F | P |

Three distinct full-block hashes appeared (round 80 recorded two alternating). `463877700639fcf7…`
is byte-identical to the committed round-57 receipt `corpus/evidence/round57/eigen-probe.txt`;
`d44ecaed4ca81ca1…` is byte-identical to the round-80 remint observations block in
`corpus/evidence/round80/largest-eigenval-probe.txt`. The projection hash is identical in all six
runs and equals the projection hash recorded in round 80 (`c5006e8e6d1e1ce8…`).

Varying-lines diffs (each run is 27 lines: 24 CASE + cases= + OBSERVED-U + PREDICATE):

```
$ diff eigen-1.stdout eigen-2.stdout        # rc 1
23c23
< CASE eig-bare-speed-s10 predicted=U observed=P rc=0 (observed-only)
---
> CASE eig-bare-speed-s10 predicted=U observed=F rc=1 (observed-only)
25,26c25,26
< cases=24 observed_pass=15 observed_fail=9 mismatches=0 setup=0
< OBSERVED-U eig-bare-speed-s2=F eig-bare-speed-s10=P
---
> cases=24 observed_pass=14 observed_fail=10 mismatches=0 setup=0
> OBSERVED-U eig-bare-speed-s2=F eig-bare-speed-s10=F

$ diff eigen-1.stdout eigen-4.stdout        # rc 1
20c20
< CASE eig-bare-speed-s2 predicted=U observed=F rc=1 (observed-only)
---
> CASE eig-bare-speed-s2 predicted=U observed=P rc=0 (observed-only)
23c23
< CASE eig-bare-speed-s10 predicted=U observed=P rc=0 (observed-only)
---
> CASE eig-bare-speed-s10 predicted=U observed=F rc=1 (observed-only)
26c26
< OBSERVED-U eig-bare-speed-s2=F eig-bare-speed-s10=P
---
> OBSERVED-U eig-bare-speed-s2=P eig-bare-speed-s10=F

$ diff eigen-2.stdout eigen-4.stdout        # rc 1
20c20
< CASE eig-bare-speed-s2 predicted=U observed=F rc=1 (observed-only)
---
> CASE eig-bare-speed-s2 predicted=U observed=P rc=0 (observed-only)
25,26c25,26
< cases=24 observed_pass=14 observed_fail=10 mismatches=0 setup=0
< OBSERVED-U eig-bare-speed-s2=F eig-bare-speed-s10=F
---
> cases=24 observed_pass=15 observed_fail=9 mismatches=0 setup=0
> OBSERVED-U eig-bare-speed-s2=P eig-bare-speed-s10=F
```

Answers to the two required questions:

1. **Are the two `predicted=U` speed cases still the only varying case lines?** Yes. The only lines
   that differ between any pair of the six runs are the two `predicted=U` CASE lines
   (`eig-bare-speed-s2`, line 20; `eig-bare-speed-s10`, line 23) plus the two summary lines derived
   from them (`cases=`, line 25; `OBSERVED-U`, line 26) — all four are exactly the line classes the
   frozen A2 rule excludes. Run 4 exhibited a U-outcome combination round 80 never recorded (both U
   cases flipped relative to runs 1/5/6), producing a third distinct full-block hash
   (`9498d376…`) while the projection hash stayed identical — the projection is invariant even for
   U combinations outside round 80's sample.
2. **Does any predicted case vary?** No. Every predicted (P/F) CASE line — all 22 of them, including
   each `rc=` value — and the `PREDICATE R57-C2 pass` line are byte-identical across all six runs;
   `mismatches=0 setup=0` in every run. U-outcome tally: s2 flipped in 1/6 runs (run 4 → P),
   s10 flipped in 3/6 (runs 2, 3, 4 → F). The historical round-57 receipt (s2=F s10=P, the
   `463877700639fcf7…` block) was reproduced byte-for-byte today by runs 1, 5 and 6.

Cross-checks of the two committed receipts under the same mechanical rule:

```
$ grep -vE '^(REV |cases=|OBSERVED-U )' corpus/evidence/round57/eigen-probe.txt | grep -vE '^(CASE|case=).*predicted=U' | sha256sum
c5006e8e6d1e1ce86d9895fc07b12db3ebaa60aa9227477a7c9972016b41bd47
$ awk '/^OBSERVATIONS_BEGIN/{f=1;next}/^OBSERVATIONS_END/{f=0}f' corpus/evidence/round80/largest-eigenval-probe.txt | grep -vE '^(REV |cases=|OBSERVED-U )' | grep -vE '^(CASE|case=).*predicted=U' | sha256sum
c5006e8e6d1e1ce86d9895fc07b12db3ebaa60aa9227477a7c9972016b41bd47
```

Both committed historical blocks and all six fresh runs project to
`c5006e8e6d1e1ce86d9895fc07b12db3ebaa60aa9227477a7c9972016b41bd47` — the round-80 recorded A2
projection hash is reproduced exactly at the round-81 host state.

## 3. Environment-pin paragraph (item 3)

`plans/round-81-claims.md` §R81-C1, "Environment pin (this round's addition, and why it is in the
predicate)": "A replay's numbers are a function of the interpreter and the crypto/userland it
calls; the round-80 receipts recorded the stack only inside observations. A receipt minted under a
*different* `python3 -V` or `openssl version` is therefore not the measurement it claims
(`HOST-PYTHON-MISMATCH` / `HOST-OPENSSL-MISMATCH`), and a reader can re-run the pin."

One sentence: of the host, a round-81 receipt pins exactly two environment facts — the probe
interpreter's `python3 -V` first line (`HOST_PYTHON`) and `openssl version` or `absent`
(`HOST_OPENSSL`), i.e. the interpreter and the crypto/userland it calls, both re-derivable by
re-running the pin command — together with the measured-tree facts (`LANE_TIP` reachable,
`WORKTREE clean`), the pinned subject/tool/driver bytes (`SUBJECT_CAPTURE`/`SUBJECT_SHA`,
`TOOL`/`TOOL_SHA`, `MINTED_BY`/`MINTED_BY_SHA`) and the `COMMAND`/`EXIT` line; it pins no other
host fact — not the kernel, bwrap, `sys.executable` path, CPU, or locale — which is why those
unpinned facts are recorded here in `host-state.txt` as context rather than as predicate.

## 4. Risks, blockers, what I could not break

- **Tip drift**: four tips observed during the session (integration in flight). The measurement is
  tip-independent: the probe refuses to run unless the captured grader's sha256 equals its frozen
  pin `cdc58e3aa0960dac2e12a12b1cfa4131237d697762a6a78ebf33f80d2eb168ce`, and the instrument's own
  sha256 is unchanged (`4f2b8beb…`). host-state.txt records the drift chain.
- **Attack surface probed**: six parallel runs under load deliberately stress the timing legs; the
  projection invariance held, including a novel both-U-flipped combination (run 4). I could not
  produce any variation in a predicted line, in `mismatches`/`setup`, or in the projection hash;
  nor any nonzero exit. The A2 projection rule and the environment pin both survived re-measurement.
- **No blockers.** No files were written outside `.ufo/waves/round-81/w1/` (host-state.txt, this
  report) and the scratch dir, which was removed (`rm -rf /fast/scratch/hyaku/kengaku-r81/EnvPinR81`)
  after this report was written.
