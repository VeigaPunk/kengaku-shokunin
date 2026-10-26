# F40RegradeRecheck — re-run of `R40RegradeSweep`'s table on configure-git-webserver and git-leak-recovery

Seat: executor (leaf), round 40 wave 2 (FALSIFY). Attacks
`.ufo/waves/round-40/build/R40RegradeSweep.md` §"Per-task results" (rows `:73-78`, `:79-81`) and §"Which graders
mutate the graded state" (`:95-116`), specifically the sentence at `:95` — "Two of five; cgw mutates on all three
selected cases, glr on the two failing cases (its oracle case already holds the lost-found files)" — and the summary
at `:158`. Lane tip `ec1005a2a28bc5cfdde7723374368ed4cc956eed` (branch `master`), cloned `--no-local` into
`/fast/scratch/hyaku/kengaku-r40/F40RegradeRecheck/lane`; `git -C "$S/lane" rev-parse --show-toplevel` =
`…/F40RegradeRecheck/lane`, `git status --porcelain` empty. Probes copied byte-identical from the clone
(`cmp` yes for both, `setup.txt`). Scratch removed after the evidence copy.

Question: does "two of five graders mutate the graded state, no verdict flip" hold, measured by rebuilding one listed
state per task with the lane's own probe builders and grading it twice **without rebuilding**, recording the verdicts
and the files the grader wrote (`find -newer`)?

**Answer: yes — for both tasks, on every listed row, with writes exactly as the report says (plus two omissions and
one wrong mechanism). 26 gradings, 0 flips.**

## Method (what is actually measured)

Harness `regrade2.py` (mine, evidence dir) loads the two lane probes unmodified and, per case, calls the probe's own
builder **once** — `prepare(work, tools, server, HARNESS_PY)` for cgw, `sandbox_argv` + `HARNESS_PY stage` for glr —
then invokes the pinned grader **twice in two fresh bwrap processes**, with no rebuild between them. After each
grading it prints the manifest delta over the graded root and the literal GNU `find <root> -newer <marker>` list
(marker mtime bumped before each grading, so each list is that grading's writes only). cgw follows the sweep's
protocol (delete the probe's `ready` handshake before each grading); the glr sandbox is bound over the same `/app`
and setup+recipe are never re-run.

Every invocation — the harness and each nested probe sandbox — ran inside the orchestrator's host-safety bwrap:

```bash
S=/fast/scratch/hyaku/kengaku-r40/F40RegradeRecheck
export TMPDIR="$S"
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
      --proc /proc --unshare-pid --die-with-parent /usr/bin/python3 "$S/regrade2.py" > "$S/regrade-run1.txt"
# rc=0, regrade-run1.err 0 bytes
```

Nested bwrap works (the probes' own `--unshare-net/pid/ipc` sandboxes ran inside it: `--smoke` printed
`SMOKE status=200`, first cgw case ran). Captures verified at their pins before grading (`PIN … ok=yes` ×6,
`regrade-run1.txt:1-6`), so I graded the same bytes the sweep did.

`TOTAL` graded: 8 built states × 2 gradings (16) + 5 repeats × 2 (10) = **26 gradings, 0 verdict differences**.

## Per-row reproduction (the two tasks)

`grade1`/`grade2` below are my runs; `files written` is the `find -newer` output, relative to the graded root
(cgw root = the probe work dir standing for the task's cwd/HOME; glr root = `/app`).

| task | case | report row | grade1 | grade2 | regrade | files written (find -newer) |
|---|---|---|---|---|---|---|
| cgw | `static-file-no-git` | `:73` pass/pass, MUT | pass | pass | same | g1 `cwd/git_test.exp`, `home/.ssh`, `home/.ssh/config`, `ready`; g2 `cwd/git_test.exp`, `home/.ssh/config`, `ready` |
| cgw | `no-server` | `:74` fail/fail, MUT | fail | fail | same | g1 `cwd/git_test.exp`, `home/.ssh`, `home/.ssh/config`; g2 `cwd/git_test.exp`, `home/.ssh/config` |
| cgw | `capitalised` | `:75` fail/fail, MUT | fail | fail | same | g1 `cwd/git_test.exp`, `home/.ssh`, `home/.ssh/config`, `ready`; g2 `cwd/git_test.exp`, `home/.ssh/config`, `ready` |
| glr | `oracle-solve-sh` | `:79` PPPPP, unchanged | PPPPP | PPPPP | same | g1 **none** (0 entries); g2 none |
| glr | `untouched` | `:80` FPPPP, MUT | FPPPP | FPPPP | same | g1 `repo/.git/lost-found`, `…/lost-found/commit`, `…/commit/<oid>`; g2 the same `…/commit/<oid>` (TOUCH) |
| glr | `dangling-secret-blob` | `:81` PPPFP, MUT | PPPFP | PPPFP | same | g1 `repo/.git/lost-found`, `…/lost-found/other`, `…/other/<oid>`; g2 `…/other/<oid>` (TOUCH) |

Manifest deltas agree: cgw grade1 `MUT:added=cwd/git_test.exp,home/.ssh,home/.ssh/config[,ready]`, grade2
`TOUCH:cwd/git_test.exp,home/.ssh/config[,ready]`; glr `untouched` grade1
`MUT:added=repo/.git/lost-found,repo/.git/lost-found/commit,repo/.git/lost-found/commit/eb8e568b…`, grade2
`TOUCH:repo/.git/lost-found/commit/eb8e568b…`; `dangling-secret-blob` grade1 adds
`repo/.git/lost-found/other/52d18a09…`, grade2 TOUCH (`regrade-run1.txt`, sections 1 and 5). Directory mtimes
(`"."`, `cwd`, `home`, `repo/.git`) appear in grade1's `find -newer` only, as expected for entry creation.

Verdicts match the report's columns on 6/6 rows, and glr's five per-test letters match the probe's frozen `predicted`
string on both gradings (`match=yes` ×3), so my build is the state the report grades.

## Findings

**F1 — the headline claim reproduces (agree).** Both graders mutate on the rows the report says they do, on the
first grading, and the second grading returns identical verdicts on all six listed rows. cgw's mutation is exactly the
two paths at `:73-75` (`git_test.exp` in the graded cwd; `~/.ssh/config` in HOME), plus `ready` (probe handshake,
excluded by `:27`), plus the `home/.ssh` directory the table omits (present in the sweep's own output,
`.ufo/waves/round-40/build/R40RegradeSweep/sweep-run1.txt:8`). glr's mutation is inside the graded repository
(`repo/.git/lost-found/…`) and, on the two failing rows, the **second** grading rewrites the same file (TOUCH,
content-identical), which the report states at `:174` and I confirm by `find -newer`.

**F2 — the parenthetical at `:101` is static-only in the report; measured here, it is real and still harmless.**
All three sweep-selected cgw cases use `tools="curl"` (`plans/git_webserver_probe.py:69-78`), so verify.sh's wget
branch (`corpus/evidence/round37/tb2-git-webserver/verify.sh:75`) never ran in the sweep — the report's "plus
`wget -q -O test_output.html` on the wget branch" is a reading of the script, not a measurement. I rebuilt the
unlisted case `wget-static-file` (tools=`wget`) twice from one state: verdict `pass`/`pass`, and `cwd/test_output.html`
appears in **both** gradings' `find -newer` lists (`regrade-run1.txt:67`, `:75`). So the wget branch adds a third
non-dot file to the graded cwd and still cannot flip the verdict, because cgw's grader reads only verify.sh's stdout
(`test_outputs.py:13`; the full capture has exactly one test function and one assertion). Coverage extension, no
contradiction.

**F3 — glr's "no flip" is contingent on the dot-path skip, and I can price it.** For each glr case I ran the grader's
own checksum command and the same command without the skip, inside the same `/app`:

```
skip = find /app/repo -type f -not -path '*/\.*' -exec sha256sum {} + | sort | sha256sum
full = find /app/repo -type f                  -exec sha256sum {} + | sort | sha256sum
```

| case | skip before g1 | skip after g1 | skip after g2 | full before g1 | full after g1 | full after g2 | files skip/all |
|---|---|---|---|---|---|---|---|
| oracle-solve-sh | `2c3d6389…` | `2c3d6389…` | `2c3d6389…` | `0bac9833…` | `0bac9833…` | `0bac9833…` | 1 / 32 |
| untouched | `2c3d6389…` | `2c3d6389…` | `2c3d6389…` | `4064f138…` | `5a6e2aa2…` | `5a6e2aa2…` | 1 / 34 |
| dangling-secret-blob | `2c3d6389…` | `2c3d6389…` | `2c3d6389…` | `db4f87e9…` | `8a39c011…` | `8a39c011…` | 1 / 33 |

(`regrade-run1.txt`, `CHECKSUM` lines.) `2c3d6389…` is the grader's hard-coded constant
(`corpus/evidence/round39/tb2-git-leak-recovery/test_outputs.py:110`), and 1 of 32 tracked-tree files survives the
skip. The mutation is therefore **visible in the graded tree** — the full-tree checksum changes at the first grading on
exactly the two rows that mutate — and invisible only because of `test_outputs.py:101`. This turns the report's prose
("a dot-path-skipping checksum can hide a VCS-side write", `:159-160`) into a receipt, and it means the no-flip result is
one token deep: drop `-not -path '*/\.*'` and the second grading of `untouched` would fail test 5.

**F4 — the stated reason for glr's oracle row being unchanged is wrong (the conclusion is still right).** `:95` says
"its oracle case already holds the lost-found files". Existence does not suppress the write: on `untouched` grade 2 a
*lost-found file that already existed* was rewritten (TOUCH, F1). The operative mechanism is that `solve.sh` runs
`git fsck --lost-found` (`solve.sh:11`) and then `git gc --prune=now` (`solve.sh:28`), so the object is pruned and the
next fsck finds nothing to write. Staged once, before any grading (`mechanism.py`, `mechanism.txt`):

```
### glr/oracle-solve-sh stage_rc=0 STAGE setup rc=0 STAGE recipe rc=0
  LF=[".git/lost-found/commit/2a6e19c8adea0fd9719b6362f5232d49e3cd111a"]
  OBJ-EXISTS 2a6e19c8adea rc=1          # the file's object is gone
  FSCK rc=0 dangling_lines=0            # nothing to write
  REFLOG entries=0
### glr/untouched stage_rc=0 STAGE setup rc=0 STAGE recipe rc=0
  LF=[]
  FSCK rc=0 dangling_lines=1
  FSCK-OUT=["dangling commit 2a6e19c8adea0fd9719b6362f5232d49e3cd111a"]
  REFLOG entries=4
```

So the oracle row mutates on neither grading because **no object is dangling**, not because files pre-exist. A reader
who took `:95` literally would predict the wrong behaviour for any case whose lost-found files survive grading (which
is the `untouched`/`dangling-secret-blob` shape).

**F5 — `:158` ("both do so on every run") is contradicted by `:79` and by measurement.** glr writes nothing on its
oracle row: `find -newer` returns 0 entries and the manifest is `unchanged` after each grading. The mutating rows for
glr are exactly the two the table names; the summary sentence should say so, or say "on every row where an object is
dangling".

**F6 — small evidence gaps, no effect on the verdict.** (a) For a server case the sweep's own output records
three non-directory writes — `cwd/git_test.exp`, `home/.ssh/config`, `ready`
(`.ufo/waves/round-40/build/R40RegradeSweep/sweep-run1.txt:8`) — and the table cell at `:73`/`:75` names two:
`ready` is at least declared in prose at `:27`, while the `home/.ssh` directory the write also creates is named by
neither. (b) cgw's capture set has no `Dockerfile` (`corpus/evidence/round37/tb2-git-webserver/SHA256SUMS`: six
files, no Dockerfile), so the task's WORKDIR — and hence where `cat > git_test.exp` lands in TB2 — is **not pinned**
by any capture; the sweep's `cwd` is an analogue, which the report hedges ("the closest analogue", `:104`) but its
column header ("graded state") does not. glr is pinned: `Dockerfile:4` is `WORKDIR /app` and `/app/repo` is graded.

**F7 — null result on a disclosed protocol deviation.** The sweep deletes the probe's `ready` handshake between the
two gradings (`:27`), which is a state reset the phrase "no rebuild, no state reset" (`:22`) has to be read around. I
measured whether it is load-bearing: `static-file-no-git` graded twice from one build **without** clearing `ready`,
five independent times, gave `pass`/`pass` 5/5 (`REPEAT noclear runs=5 regrade_same=5 diff=0`, `repeat-noclear.txt`).
The deletion is defensive (RUN_SH's wait loop at `plans/git_webserver_probe.py:188-194` would break immediately on a
stale handshake, and the fresh server still binds first), not a hidden reset that manufactures agreement. The
disclosure at `:27` is adequate; the claim at `:22` is not strictly literal for cgw.

## Incidental control: state construction really is wall-clock dependent

Building `oracle-solve-sh` and `untouched` back to back inside one second gave the **same** commit id in both rows
(`2a6e19c8…`, `mechanism.txt`), while the earlier harness run, whose rows were built seconds apart, produced
`17dbbe32…` (oracle) and `eb8e568b…` (untouched). This independently reproduces `:128-131` and shows the dependence is
sub-second, not merely "two builds 2 s apart". Consequence for my own receipts: object ids in them are not reproducible
across runs; verdicts are.

## Limits

- Two of five graders, six listed rows plus one unlisted row (F2); `protein`, `regex`, `bpm` and the rest of the
  15-row table were not re-run (out of scope for this seat).
- Host toolchain: `git 2.56.0`, python 3.14.8, `/usr/bin/expect` absent, `curl` and `wget` present (`setup.txt`); the
  probe sandbox is not the TB2 container, and cgw's oracle path (root/apt/nginx/sshd) is still not executed.
- cgw's manifest root is the probe work dir, so a write to the sandbox-private tmpfs (`--tmpfs /tmp`) would be
  invisible to `find -newer`. The captured `verify.sh` has no `/tmp` write; `apt-get` is absent from every case's PATH
  (`BASE_TOOLS`, `git_webserver_probe.py:48`), so its install step cannot write outside the root either.
- One grading pair per listed row; the flake question here is "does the second grading see the same verdict", not a
  rate estimate.

## Retained evidence (`.ufo/waves/round-40/falsify/F40RegradeRecheck/`, `SHA256SUMS`)

- `regrade2.py` — build-once/grade-twice harness (`find -newer`, manifests, fresh process per grading).
- `regrade-run1.txt` (sha256 `34b4389f…`, stderr empty) — 8 states, 16 gradings: pins, per-grading verdicts, write
  lists, checksum table.
- `repeat_noclear.py`, `repeat-noclear.txt` (`e7bdeb00…`) — five `ready`-not-cleared repeats, 10 gradings.
- `mechanism.py`, `mechanism.txt` (`f9da38ab…`) — pre-grading glr state: lost-found inventory, object existence,
  fsck dangling count, reflog depth.
- `setup.txt` (`2a3f203b…`) — clone HEAD/toplevel, probe-copy equality, toolchain, exact commands, outer bwrap form.

VERDICT: regrade-recheck-agree
