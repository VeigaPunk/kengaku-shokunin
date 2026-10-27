# R45ExecStageCheck — round-45 wave 1 (build), lane `kengaku-shokunin`

Item: independently reproduce the C2 probe's `--dry` (byte-equal to the frozen dry table) and `--stage-check`
(`stagecheck cases=16 failed=0`) in a clone, inside the host-safety envelope; then read every case recipe in
`plans/password_recovery_probe.py` and say whether any case recipe could have run pre-freeze **on this host**.

Frozen inputs read first: `plans/round-45-claims.md` (both claims, kill rules, order of operations). Nothing
under `plans/`, `corpus/`, the lane's `.gitignore`d tree or the lane's index was modified; I wrote only this
report plus `.ufo/waves/round-45/w1/R45ExecStageCheck/` and my scratch.

Scratch `S=/fast/scratch/hyaku/kengaku-r45/R45ExecStageCheck`; clone:

```
$ git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
$ git -C "$S/lane" rev-parse --show-toplevel
/fast/scratch/hyaku/kengaku-r45/R45ExecStageCheck/lane
$ git -C "$S/lane" rev-parse HEAD
52d7486a8caf930855cd1f748032ac21648303f5
$ sha256sum "$S/lane/plans/password_recovery_probe.py" "$S/lane/corpus/evidence/round45/password-recovery-dry-cases-freeze.txt"
f87a9eebe464b29d95259cae24c00b56ea58de5bf93fef10884daa673e1488b5  …/plans/password_recovery_probe.py
46036abe542aa8e50a59080bda82c154ae4735de25ac64416906de263f71aabb  …/password-recovery-dry-cases-freeze.txt
```

Both digests equal the frozen-digest ledger rows (`.ufo/waves/round-45/claims/frozen-digests.txt:3,5`).

Tools used (all pre-installed; **nothing installed or upgraded this seat**): `strace 7.2`, `bubblewrap 0.13.1`,
`Python 3.14.8`, kern `7.2.11-arch1-1`.

## 1. `--dry` reproduced byte-equal

```
$ S=/fast/scratch/hyaku/kengaku-r45/R45ExecStageCheck
$ TMPDIR="$S" …/.ufo/waves/round-45/claims/envelope.sh "$S/env" /usr/bin/python3 \
    "$S/lane/plans/password_recovery_probe.py" --lane "$S/lane" --dry > "$S/dry.out" 2>&1
$ grep -v '^ENVELOPE ' "$S/dry.out" > "$S/dry.payload"
$ cmp "$S/dry.payload" "$S/lane/corpus/evidence/round45/password-recovery-dry-cases-freeze.txt" && echo CMP dry-identical
CMP dry-identical
$ sha256sum "$S/dry.payload"
46036abe542aa8e50a59080bda82c154ae4735de25ac64416906de263f71aabb  "$S/dry.payload"
```

26 lines, 9 `TAG`, 16 `CASE`, closing `cases=16 predicted_pass=5 predicted_fail=11`. Envelope:

```
ENVELOPE start 23:26:22 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 23:26:24 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```

`--dry` takes the `if a.dry:` branch at `plans/password_recovery_probe.py:299`, which returns before the
capture-digest loop, the tool check and the `mkdtemp` root: it cannot build or run a case. My run left no file
behind (`ls -la "$S"` before the stage run showed no `work/`).

## 2. `--stage-check` reproduced, byte-equal to the pre-freeze claim

```
$ TMPDIR="$S" …/claims/envelope.sh "$S/env" /usr/bin/python3 \
    "$S/lane/plans/password_recovery_probe.py" --lane "$S/lane" --stage-check --work "$S/work" > "$S/stage.out" 2>&1
$ grep -v '^ENVELOPE ' "$S/stage.out" > "$S/stage.payload"
$ cmp "$S/stage.payload" /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/c2-stage-check.txt \
  && echo CMP stage-identical-to-claim
CMP stage-identical-to-claim
$ sha256sum "$S/stage.payload"
2b4e159499c0a17bf9ad02f11ad1f74c489336e1b39dae0fa33ebe0bcf026a3a  "$S/stage.payload"
```

Last line `stagecheck cases=16 failed=0`; every case `seed rc=0 recipe rc=0`; per-case `recovered` = absent /
bytes=0,15,21,21,24×5,25,33,37,67,13917 exactly as the pre-freeze claim. Envelope:

```
ENVELOPE start 23:26:37 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 23:26:40 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```

`--work "$S/work"` was removed by the probe's `finally` (`shutil.rmtree(root)`): `ls -la "$S/work"` → empty.

Cross-check against the wave's full-run receipt `corpus/evidence/round45/password-recovery-probe.txt`
(mtime `2026-10-26 23:27:18`, i.e. **after** the 23:06:54 freeze commit): its 16 `CASE … observed=` verdicts are
consistent with my stage-check's end states (`nop` and `under-varsea` report `recovered absent`, `dir-state`
reports `bytes=15` yet fails on `IsADirectoryError`, `decoys-1000` `bytes=13917` passes), and its own envelope
shows the L1 scratch (`…/hyaku/kengaku-r45/L1/run`). That receipt is the first recorded graded run; see §4.

## 3. Every case recipe, read (all 16)

Rendered verbatim to `…/w1/R45ExecStageCheck/recipes.txt` (module loaded with `PYTHONDONTWRITEBYTECODE=1`;
`SEED None`; `nop` has `recipe=""`, so the probe writes `":"` into `/recipe.sh`, `plans/password_recovery_probe.py:249`).

| case | recipe writes | recipe reads |
|---|---|---|
| `nop` | — (no recipe) | — |
| `oracle-solve-sh` | relative files of `solve.sh` in cwd `/app` | `/pub/solve.sh`, seed `/app/varsea` |
| `constant` | `/app/recovered_passwords.txt` | `grep -ao '8XD[A-Z0-9]*' /pub/test_outputs.py` |
| `constant-crlf` | same, `\r\n` | same |
| `constant-joined` | same, answer + embedded decoy on one line | same |
| `dir-state` | `mkdir -p /app/recovered_passwords.txt`, `/app/recovered_passwords.txt/x` | same |
| `empty-file` | `: > /app/recovered_passwords.txt` | — |
| `wrong-23` | `printf 'ZZZ…Z'` (23) | — |
| `prefix-decoy` | `printf '8XD…W54'` | — |
| `sub-first` | `${PW:0:20}` → `/app/…` | `/pub/test_outputs.py` |
| `sub-last` | `${PW:3}` → `/app/…` | `/pub/test_outputs.py` |
| `lower23` | `tr 'A-Z' 'a-z'` → `/app/…` | `/pub/test_outputs.py` |
| `decoys-1000` | answer + `seq 1 1000 \| sed 's/^/WRONGGUESS/'` → `/app/…` | `/pub/test_outputs.py` |
| `password-eq` | `printf 'PASSWORD=%s\n'` → `/app/…` | `/pub/test_outputs.py` |
| `crlf-line` | answer + `WRONGDECOY0` | `/pub/test_outputs.py` |
| `under-varsea` | `solve.sh` run with cwd `/app/varsea` → `/app/varsea/recovered_passwords.txt` | `/pub/solve.sh` |

Complete absolute-path vocabulary of all 16 recipes (extracted mechanically; the `sed 's/^/WRONGGUESS/'`
operand is not a path):

```
/app/recovered_passwords.txt      /app/recovered_passwords.txt/x    /app/varsea
/dev/null                         /pub/solve.sh                     /pub/test_outputs.py
```

No recipe names `/home`, `$HOME`, `~`, `/tmp`, `/usr`, `/etc`, `/proc`, a PATH directory or any relative path
whose cwd is not fixed by the harness to `/app`. The only relative-path writer is the captured `solve.sh`
itself (`window.txt`, `possible_sequences*.txt`, `recovered_passwords.txt`); the harness pins its cwd
(`cwd="/app"`, `plans/password_recovery_probe.py:180`), so those land in the sandbox.

## 4. Could a recipe have run pre-freeze **on this host**? — No

"On this host" is the operative clause, and the answer is no on three independent legs. It is worth stating the
distinction precisely: the pre-freeze `--stage-check` **did** execute all 16 recipes, but inside the probe's own
throwaway sandbox, and the frozen claim's ordering sentence is about *grading*: "No case of this task was graded
on this host before the freeze" (`plans/round-45-claims.md`, order-of-operations ¶).

**(a) No host-level execution path exists in the probe.** The only two `subprocess` sites are the sandbox
(`plans/password_recovery_probe.py:234`, `subprocess.run(sandbox_argv(cap, work) + [… "/harness.py", mode])`) and
the harness shell-out (`:180`) that runs *inside* it. Every recipe is written to `work/recipe.sh` and executed by
`/harness.py` with `cwd="/app"` inside the bwrap per case; nothing calls a recipe on the host.

**(b) The sandbox cannot reach a host path even if a recipe named one.** I rebuilt the probe's exact
`sandbox_argv`/`ENV` (`…/w1/R45ExecStageCheck/sandbox_iso.py`) with a reporting harness; inside it:

```
ROOT_ENTRIES ['app','bin','dev','etc','harness.py','lib','lib64','proc','pub','recipe.sh','sbin','seed.sh','tests','tmp','usr']
EXISTS /home False        EXISTS /fast False        EXISTS /fast/scratch False        EXISTS /app True
MOUNT tmpfs / tmpfs rw,…   MOUNT … /usr btrfs ro   MOUNT … /etc btrfs ro   MOUNT … /app xfs rw
MOUNT … /tests ro   MOUNT … /pub/*.py ro   MOUNT … /dev/urandom xfs ro   (20 mounts, no host home)
WRITE /home/vgpnk/R45-CANARY-PROBE WROTE      ← inside the sandbox
```

and on the host, immediately after: `ls: cannot access '/home/vgpnk/R45-CANARY-PROBE': No such file or directory`.
The sandbox root is a private tmpfs: a write outside the explicit binds "succeeds" against that tmpfs and vanishes.
Envelope for that control:

```
ENVELOPE start 23:27:55 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 23:27:57 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```

**(c) A syscall audit of the whole stage-check sees no host write.** I re-ran `--stage-check` under
`strace -f -y -e trace=%file` inside the envelope; `stagecheck cases=16 failed=0` again, envelope:

```
ENVELOPE start 23:28:17 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 23:28:30 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```

60,402 traced lines; 292 distinct absolute write/mutate targets in 923 events, families: `/app/*` (seed +
recipes, incl. 130 generated `varsea` noise files), `/dev/null`, `/dev/tty` (bwrap `--new-session`), `/proc` fd
setup and `/proc/<pid>/{uid,gid}_map` (namespace setup), and my own `$S/work3/**` scratch. Absolute write targets
under `/home`, `/usr`, `/etc`, or `/fast` outside `$S`: **NONE** (`…/w1/R45ExecStageCheck/audit-writes.txt`).
Relative write targets resolve through the `strace -y` dirfd annotation into the sandbox — 516 write/mutate calls
at `AT_FDCWD</app>`, 8 at `AT_FDCWD</app/varsea>`, 472 inside per-case `kprp-*` dirs, 432 into bwrap's
`<newroot>` bind setup — e.g. `openat(AT_FDCWD</app>, "window.txt", O_WRONLY|O_CREAT|O_TRUNC) = 3</app/window.txt>`
and `openat(AT_FDCWD</app>, "recovered_passwords.txt", O_WRONLY|O_CREAT|O_APPEND) = 3</app/recovered_passwords.txt>`.
The probe process itself starts with cwd `/home/vgpnk/Projects/shokunin` (the envelope's cwd) and issues 80
write-intent opens from there; every one names an absolute `$S/work3/…` path — its own scratch. Raw log is
6,648,909 B — not copied (limit); sha256
`db04c1877683a94e043426d2b18850eb66e7a6d8a1df3a2c4b44745689b066a9`.

**(d) No grading happened pre-freeze.** The grader is imported only after the stage branch returns:

```
178  if mode in ("stage", "recipe"):
189      sys.exit(0)
190  spec = importlib.util.spec_from_file_location("tb2_password_recovery_grader", "/tests/test_outputs.py")
```

so `--stage-check` runs `seed`/`recipe` and reports only `os.path.getsize` existence. The pre-freeze claim
`claims/c2-stage-check.txt` (mtime 23:05:22) contains 16 `STAGECHECK … seed rc=0 recipe rc=0 recovered …` lines
and **zero** `TEST`/`CASE` lines; my reproduction likewise has none (`grep -c '^TEST '` → 0, `grep -c '^CASE '` → 0).
The recipe-run evidence in that file (`decoys-1000 … bytes=13917`) confirms the recipes themselves did execute —
sandboxed and ungraded — before the freeze, which is exactly what the frozen ordering sentence discloses.

**(e) Receipt chronology.** `plans/password_recovery_probe.py` first appears in commit
`b4fcd35141acda5fa0980a34dd29ab880b702ee6` (2026-10-26T23:06:54-03:00, the freeze commit) —
`git -C "$S/lane" log --format='%H %cI %s' -- plans/password_recovery_probe.py` returns that commit only. The
full-run receipt `corpus/evidence/round45/password-recovery-probe.txt` has mtime `23:27:18` (post-freeze, this
wave; its `ENVELOPE` line shows the L1 seat's scratch and `--work …/L1/w-probe`). No other probe receipt exists
anywhere in the lane (`grep -rl password_recovery_probe` → probe, claims, spec, C2 counter, package entry,
wave specs, the receipt). Attempt 1 (~22:27–22:48) left no probe receipt: `.ufo/waves/round-45/attempt1-unclaimed/`
holds only the discarded C1/C3 drafts and `witness/w_u.py`, a C1 direction module.

Host residue after my runs: `ls -d /app` → `No such file or directory`; no `recovered_passwords.txt` under
`/home/vgpnk`; the clone's `git status --porcelain` was empty at 23:26 (before my own module imports created an
ignored `plans/__pycache__/password_recovery_probe.cpython-314.pyc` **in the scratch clone**).

Residual, stated not hidden: this rules out every path the probe itself offers (`--dry`, `--stage-check`, full
run) and shows the sandbox is host-inert; it cannot prove the negative for a hand-written driver that bypasses
`plans/password_recovery_probe.py` and runs `solve.sh` from a host cwd (that script writes fixed *relative*
names, so a manual run would litter whatever cwd it was given). No receipt, no residue and no probe code path
support such a run, and the first graded execution is timestamped 23:27, after the freeze.

## 5. Risks / limits

- The strace audit covers file-namespace syscalls (`%file`): open/openat/creat/mkdir/unlink/rename/chmod/link
  families. It does not cover `ioctl`, memory, or network effects — moot here because the sandbox also has
  `--unshare-net` and the probe's ENV is fixed, and the host guard is `/home` read-only under the envelope.
- `--stage-check` is not a grading run: it proves case end states are constructible (16/16) and that the grader
  is never imported, not that verdicts hold. Verdict reproduction is the C2 counter's job, not this item's.
- `grep -ao '8XD[A-Z0-9]*' /pub/test_outputs.py` is the probe's declared leak channel, by design; the answer is
  read from the *public* grader copy at the pin, inside the sandbox, never from a host file.
- Informational for L1: a sibling's counter run left `plans/__pycache__/round45_c2_verify.cpython-314.pyc`
  (mtime 23:29:48) in the real lane; it is `.gitignore`d (`.gitignore:2 __pycache__/`), so it does not dirty the
  working tree. Not mine, not touched.

## 6. Receipts (`…/w1/R45ExecStageCheck/`)

| file | bytes | sha256 |
|---|---|---|
| `dry.out` (envelope + dry) | 4370 | `f10769901cdc2aa2adaa7e6564053cb583b153374d18f85de9e4d489d8851544` |
| `dry.payload` (dry body = freeze table) | 3685 | `46036abe542aa8e50a59080bda82c154ae4735de25ac64416906de263f71aabb` |
| `stage.out` (envelope + stage-check) | 1870 | `ffd12f97b72de36de54d004126245a971a3b5f45e33259a230a54ecb8f42f1ee` |
| `stage.payload` (= pre-freeze claim) | 1115 | `2b4e159499c0a17bf9ad02f11ad1f74c489336e1b39dae0fa33ebe0bcf026a3a` |
| `stage-strace.out` | 1978 | `53e1e014f658ac4969b5e9a4136c976a59d89118709d3605702eb48046ea1ec4` |
| `iso.out` (sandbox reach + canary) | 3352 | `abf5cc753bd3581bef1b64be5964dbcda8ad8db71ee4545c2e41549eb99f3bc7` |
| `sandbox_iso.py` | 2534 | `189b11aefde74ba986158b4d3f1c89ac89b46d46831984729a3b02f2160fddbf` |
| `recipes.txt` (all 16 recipes) | 2658 | `3b1bcf8225f3a9cb616c013d5e434c05d8fcd1c9f1f18d95c8de1d0bb5daf7d6` |
| `audit-writes.txt` (strace summary) | 38988 | `4e10a3503a44980844d7631e7c1bd6a8c24f832a9226c3c2257106da4ad0bd75` |

Strace log (6,648,909 B, sha256 `db04c1877683a94e043426d2b18850eb66e7a6d8a1df3a2c4b44745689b066a9`) is quoted above
and **not** copied (size limit). Scratch `/fast/scratch/hyaku/kengaku-r45/R45ExecStageCheck` removed with
`plans/scratch_guard.py safe-rm` before yield.

Changed files: this report and its subdirectory only. No frozen counter, probe, spec, gate, capture, dry table,
refusal module, battery, claim or lane file was modified; no git/jj mutation anywhere; no tool installed.

VERDICT: stage-check-reproduced-yes
