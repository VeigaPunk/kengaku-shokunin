# R45LabratRefetch — round 45 wave 2 falsification: refetch the pinned TB2 `password-recovery` capture

Seat: R45LabratRefetch (executor, leaf). Date: 2026-10-26. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scratch: `/fast/scratch/hyaku/kengaku-r45/R45LabratRefetch`. Nothing in the lane was written; all commands are reads or writes into scratch/this subdir.

## Bottom line

- **9/9 pinned files refetched byte-identical** to `corpus/evidence/round45/tb2-password-recovery/` (sha256 *and* git blob sha, both equal to the GitHub tree shas at the pinned commit).
- **No drift at upstream HEAD**: `HEAD` = `refs/heads/main` = `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, the pinned commit (committer date `2026-04-30T05:53:30Z`). HEAD-ref refetch of the same nine paths is identical to the pinned files 9/9; the task tree at HEAD has the same nine blobs and no extra file.
- The pack's 9 entries + `SHA256SUMS` are self-consistent (`sha256sum -c` 9/9 OK) and the pin table `plans/pkg-spec-r45.json` triple-matches (pin vs refetch vs capture) 8/8 rows; the receipt digest declared in the spec matches the on-disk receipt.
- Non-blocking packaging notes for the L1/C2 (see Risks): the capture pack **flattens** the upstream layout and stores `.gitignore` as `gitignore`; the entry's SOURCES rows cite the correct nested upstream paths. Four SOURCES line ranges are loose upper bounds beyond the file's actual line count (no content misquote).

## Network access

Network was live; `raw.githubusercontent.com` reached from the host shell and again from inside the bwrap envelope (no `--unshare-net`).

```
$ curl -sS -o /dev/null -w 'http=%{http_code}\n' https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/task.yaml
http=404
```

That 404 is expected (`task.yaml` does not exist; the manifest is `task.toml`) and was only a reachability probe — `git ls-remote` and every raw GET below returned 200.

## Upstream layout at the pin (GitHub tree API)

```
$ curl -sS -o tree.json 'https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1'
http=200 bytes=453523            # truncated=False entries=1446
$ python3 -c "... filter 'password-recovery' in path ..."
040000 tree - password-recovery 1c9b07ed999d3839
100644 blob 177 password-recovery/.gitignore ecd089e8ac7767b9
100644 blob 2007 password-recovery/README.md ff438f70a6f03b77
040000 tree - password-recovery/environment 87b1d2363c9bac9b
100644 blob 497 password-recovery/environment/Dockerfile a98ed55c7493e751
100644 blob 1582 password-recovery/environment/setup.sh 8bae61be72cb3dc5
100644 blob 644 password-recovery/instruction.md 80573f8662de4a39
040000 tree - password-recovery/solution 318d8327daeab54d
100644 blob 3071 password-recovery/solution/solve.sh 276086517e521f11
100644 blob 949 password-recovery/task.toml 9216e2e906b5e808
040000 tree - password-recovery/tests 0853919ea9ae074c
100644 blob 608 password-recovery/tests/test.sh cb4a41a45e4b23f4
100644 blob 594 password-recovery/tests/test_outputs.py 358a5273aec0a5de
```

Exactly nine blobs, no `task.yaml`, and the task appears once in the repo tree. The capture pack's flat names map to these nested paths (see Risks note 1).

## HEAD drift check

```
$ git ls-remote https://github.com/harbor-framework/terminal-bench-2 HEAD 'refs/heads/*'
2fd12b88aafdd04a52c298e3940bcb189f9766d6	HEAD
...
2fd12b88aafdd04a52c298e3940bcb189f9766d6	refs/heads/main

$ curl -sS 'https://api.github.com/repos/harbor-framework/terminal-bench-2/commits/main'
http=200
HEAD sha= 2fd12b88aafdd04a52c298e3940bcb189f9766d6
commit date= 2026-04-30T05:53:30Z
message= Add task metadata to task manifests
```

`HEAD` is the pinned commit itself, so "did HEAD move the task" answers no at the ref level. As a second, content-level leg (independent of the sha identity), all nine files were also fetched at `ref=HEAD` and compared to the pin refetch.

## Envelope run 1 — pinned vs HEAD refetch and pinned vs capture pack

Command (receipt `/…/w2/R45LabratRefetch/refetch-compare.txt`):

```
$ …/claims/envelope.sh "$S/env" bash "$S/compare.sh" > "$R/refetch-compare.txt"
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind …/R45LabratRefetch/env …/env --bind …/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- bash …/compare.sh
ENVELOPE start 23:50:03 cwd=/home/vgpnk/Projects/shokunin
```

```
HEAD .gitignore http=200 vs_pin=IDENTICAL sha256=9a8dd8d9b6c3adb8e9e56328df27deef859a3e98fffc9b8133c8b22207c25953
HEAD README.md http=200 vs_pin=IDENTICAL sha256=122bf15ef4a6ede562f21453f9f1c452fc10a3048bac7d46a013adbac6a13add
HEAD instruction.md http=200 vs_pin=IDENTICAL sha256=bc4f501148805bbccdb94a5c5b745f1ce9564f04ef0fe36bc37c3ca20b7810a5
HEAD task.toml http=200 vs_pin=IDENTICAL sha256=cfd0362d201b957796f9bf1c02cc75646250cb2bd107ec88c768bfcfd091b24b
HEAD environment/Dockerfile http=200 vs_pin=IDENTICAL sha256=6fabcb9e1fcb7155bf8cfe106c17f2dfa3344103e97960dab580c2444b6c9fe0
HEAD environment/setup.sh http=200 vs_pin=IDENTICAL sha256=9fdde5d9cd74ae0d633bdd59e7249cc6d7385d27a98b1e2dbbeb11b05a6f2af8
HEAD solution/solve.sh http=200 vs_pin=IDENTICAL sha256=c5f9fc70b6bae40befdd0088dde1a3bc6e909852c9fbb36a617c627b7b8d804f
HEAD tests/test.sh http=200 vs_pin=IDENTICAL sha256=4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334
HEAD tests/test_outputs.py http=200 vs_pin=IDENTICAL sha256=2dc14fc180734b6fbb0ee00f27c4f866071247b57a2217f579465ff8ed3bfc9e
HEAD_vs_PIN identical=9 differs=0

upstream=.gitignore local=gitignore bytes=177 refsha256=9a8dd8d9…25953 localsha256=9a8dd8d9…25953 refblob=ecd089e8ac77 localblob=ecd089e8ac77 BYTE-IDENTICAL
upstream=README.md local=README.md bytes=2007 refsha256=122bf15e…3add localsha256=122bf15e…3add refblob=ff438f70a6f0 localblob=ff438f70a6f0 BYTE-IDENTICAL
upstream=instruction.md local=instruction.md bytes=644 … refblob=80573f8662de localblob=80573f8662de BYTE-IDENTICAL
upstream=task.toml local=task.toml bytes=949 … refblob=9216e2e906b5 localblob=9216e2e906b5 BYTE-IDENTICAL
upstream=environment/Dockerfile local=Dockerfile bytes=497 … refblob=a98ed55c7493 localblob=a98ed55c7493 BYTE-IDENTICAL
upstream=environment/setup.sh local=setup.sh bytes=1582 … refblob=8bae61be72cb localblob=8bae61be72cb BYTE-IDENTICAL
upstream=solution/solve.sh local=solve.sh bytes=3071 … refblob=276086517e52 localblob=276086517e52 BYTE-IDENTICAL
upstream=tests/test.sh local=test.sh bytes=608 … refblob=cb4a41a45e4b localblob=cb4a41a45e4b BYTE-IDENTICAL
upstream=tests/test_outputs.py local=test_outputs.py bytes=594 … refblob=358a5273aec0 localblob=358a5273aec0 BYTE-IDENTICAL
PINNED_VS_LOCAL identical=9 differs=0

== local evidence pack integrity ==
pack entries (excluding SHA256SUMS): 9
Dockerfile: OK   README.md: OK   gitignore: OK   instruction.md: OK   setup.sh: OK
solve.sh: OK     task.toml: OK   test.sh: OK      test_outputs.py: OK

ENVELOPE end 23:50:08 exit=1 local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged
```

`exit=1` is **my own script's** trailing block (it fed the full-repo `tree.json`, 1038 blobs, into the task-level comparison and raised `KeyError: 'LICENSE'`); every comparison line above it had already completed and printed, and the PATH-dir digest is `unchanged`, so no measurement is invalidated. That broken block was rewritten as the standalone `tree_compare.py` and re-run in envelope run 2.

## Envelope run 2 — GitHub tree blob shas (pin vs HEAD) vs capture-pack blob shas

Command (receipt `/…/w2/R45LabratRefetch/tree-compare.txt`):

```
$ …/claims/envelope.sh "$S/env" python3 "$S/tree_compare.py" > "$R/tree-compare.txt"
ENVELOPE start 23:50:20 cwd=/home/vgpnk/Projects/shokunin
```

```
pinned-commit task files: 9
HEAD task-dir files: 9
task tree pinned == HEAD: True
.gitignore: tree=ecd089e8ac77 local_blob=ecd089e8ac77 MATCH
README.md: tree=ff438f70a6f0 local_blob=ff438f70a6f0 MATCH
environment/Dockerfile: tree=a98ed55c7493 local_blob=a98ed55c7493 MATCH
environment/setup.sh: tree=8bae61be72cb local_blob=8bae61be72cb MATCH
instruction.md: tree=80573f8662de local_blob=80573f8662de MATCH
solution/solve.sh: tree=276086517e52 local_blob=276086517e52 MATCH
task.toml: tree=9216e2e906b5 local_blob=9216e2e906b5 MATCH
tests/test.sh: tree=cb4a41a45e4b local_blob=cb4a41a45e4b MATCH
tests/test_outputs.py: tree=358a5273aec0 local_blob=358a5273aec0 MATCH
local_blob_vs_tree_shas match=9/9
upstream files with no local counterpart: none
local pack entries: 10 ['Dockerfile', 'README.md', 'SHA256SUMS', 'gitignore', 'instruction.md', 'setup.sh', 'solve.sh', 'task.toml', 'test.sh', 'test_outputs.py']
ENVELOPE end 23:50:22 exit=0 local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged
```

This is a third, path-independent identity: the capture files hash to the *same git blob ids* GitHub's tree API publishes for the pinned commit, and the pinned tree equals the HEAD task tree blob-for-blob.

## Envelope run 3 — pin table and receipt digest

Command (receipt `/…/w2/R45LabratRefetch/pin-verify.txt`):

```
$ …/claims/envelope.sh "$S/env" python3 "$S/pin_verify.py" > "$R/pin-verify.txt"
ENVELOPE start 23:50:49 cwd=/home/vgpnk/Projects/shokunin
```

```
raw_base       : https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/password-recovery/
pin table rows : 8 ['S149', 'S150', 'S151', 'S152', 'S153', 'S154', 'S155', 'S156']
S149 tests/test_outputs.py        pin=2dc14fc18073 refetch=2dc14fc18073 capture=2dc14fc18073 TRIPLE-MATCH
S150 instruction.md               pin=bc4f50114880 refetch=bc4f50114880 capture=bc4f50114880 TRIPLE-MATCH
S151 environment/setup.sh         pin=9fdde5d9cd74 refetch=9fdde5d9cd74 capture=9fdde5d9cd74 TRIPLE-MATCH
S152 environment/Dockerfile       pin=6fabcb9e1fcb refetch=6fabcb9e1fcb capture=6fabcb9e1fcb TRIPLE-MATCH
S153 tests/test.sh                pin=4770437ea96c refetch=4770437ea96c capture=4770437ea96c TRIPLE-MATCH
S154 README.md                    pin=122bf15ef4a6 refetch=122bf15ef4a6 capture=122bf15ef4a6 TRIPLE-MATCH
S155 solution/solve.sh            pin=c5f9fc70b6ba refetch=c5f9fc70b6ba capture=c5f9fc70b6ba TRIPLE-MATCH
S156 task.toml                    pin=cfd0362d201b refetch=cfd0362d201b capture=cfd0362d201b TRIPLE-MATCH
receipt        : corpus/evidence/round45/password-recovery-probe.txt declared= cf74f451df90aa4a actual= cf74f451df90aa4a MATCH
gitignore capture sha256= 9a8dd8d9b6c3adb8e9e56328df27deef859a3e98fffc9b8133c8b22207c25953 refetch sha256= 9a8dd8d9b6c3adb8e9e56328df27deef859a3e98fffc9b8133c8b22207c25953 MATCH
gitignore has a SOURCES row: False
pin rows triple-match: 8/8
ENVELOPE end 23:50:51 exit=0 local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged
```

The ninth captured file (`.gitignore` / capture `gitignore`) is the "rejected row candidate": byte-identical to upstream at the pin, present in the capture pack and in `SHA256SUMS`, and correctly absent from the SOURCES row set (8 rows S149–S156). The entry's own source header agrees (`corpus/knowledge/tb2-password-recovery-grader.md:72`: "the package's SOURCES rows are S149, S150, S151, S152, S153, S154, S155 and S156"), while the entry's recheck names "nine files" for `SHA256SUMS` (`:10`), which is the 9-file capture pack — consistent, since the pack's nine *are* the eight rows plus the gitignore.

## Probe-receipt spot check

`corpus/evidence/round45/password-recovery-probe.txt:1-5` records four capture digests; each equals the refetch digest in this report:

```
# capture instruction.md sha256=bc4f501148805bbccdb94a5c5b745f1ce9564f04ef0fe36bc37c3ca20b7810a5
# capture setup.sh sha256=9fdde5d9cd74ae0d633bdd59e7249cc6d7385d27a98b1e2dbbeb11b05a6f2af8
# capture solve.sh sha256=c5f9fc70b6bae40befdd0088dde1a3bc6e909852c9fbb36a617c627b7b8d804f
# capture test_outputs.py sha256=2dc14fc180734b6fbb0ee00f27c4f866071247b57a2217f579465ff8ed3bfc9e
```

## Risks / notes for the L1 (none blocks the refetch verdict)

1. **Capture pack layout is flattened, not upstream-shaped.** `corpus/evidence/round45/tb2-password-recovery/` stores `environment/setup.sh` as `setup.sh`, `environment/Dockerfile` as `Dockerfile`, `solution/solve.sh` as `solve.sh`, `tests/test.sh` as `test.sh`, `tests/test_outputs.py` as `test_outputs.py`, and `.gitignore` as `gitignore`. Content is byte-exact; the mapping is documented per-row in `plans/pkg-spec-r45.json` (`rows.S151.upstream` etc.), so a reader is not misled — but a naive re-fetch of the flat names returns 404 (measured: `Dockerfile/setup.sh/solve.sh/test.sh/test_outputs.py` all `http=404`, body 14 bytes, at the pin). Evidence: `plans/pkg-spec-r45.json` rows carry both keys, and the entry cites nested URLs (`corpus/knowledge/tb2-password-recovery-grader.md:3-8`).
2. **Four SOURCES line ranges overrun their file (loose upper bound, no misquote):** S151 says `setup.sh` "lines 1-45" (file: 1582 bytes, 42 newlines, last byte `t` → 43 lines with an unterminated last line); S153 says `test.sh` "lines 1-31" (29 lines); S154 says `README.md` "lines 1-46" (32 newlines, last byte `.` → 33 lines); S155 says `solve.sh` "lines 1-70" (68 lines). Every cited range is an enclosing superset, and none of the quoted text is affected; it is a citation-hygiene nit for C2/frontier, not a content defect. Files that match exactly: `instruction.md` 1-9 (9 lines), `task.toml` 1-41 (41), `Dockerfile` 1-16 (⊂20), `test_outputs.py` :9-10 and :14-18 (⊂18).
3. **Freshness is bounded by the pin, not by HEAD:** HEAD is the pin today (2026-10-26), so "no drift" is a true statement about now; it is not a guarantee about tomorrow. The entry's `recheck: 180d` (`…grader.md:10`) remains the right instrument, and its `sha256sum -c SHA256SUMS` leg still passes 9/9.
4. **Network was available for this run**; nothing here was measured offline. If a future seat lacks egress, the identity claims must fall back to the local pack + `SHA256SUMS` only.

## Method / hygiene

- Scratch `$S=/fast/scratch/hyaku/kengaku-r45/R45LabratRefetch`, `TMPDIR=$S`, all fetches and comparison scripts under it; nothing was written into the lane, the fleet root, or any PATH directory. `/home/vgpnk` was bound read-only inside every envelope run; `~/.cache` was an overlay from scratch; the `~/.local/bin` content digest was `e396f23e40a69201` before and after all three runs (`unchanged`).
- Receipts kept in `…/w2/R45LabratRefetch/`: `refetch-compare.txt`, `tree-compare.txt`, `pin-verify.txt` (all small; the refetch corpus itself stayed in scratch and was deleted).
- Tools installed: none (curl, python3, git, bwrap already present).
- The two probe scripts remain in scratch only; they are not proposed as lane instruments.

VERDICT: refetch-identical-9/9-drift-none
