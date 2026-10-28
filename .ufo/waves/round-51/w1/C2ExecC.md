# C2ExecC — round 51, lane `kengaku-shokunin`, seat executor (rows 19–27 attribution)

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7

Lane `kengaku-shokunin` at `4090c3db` (branch `master`; stage-1 freeze `e07f131cf7037e58a21db6e1f3986cf401ad257c`
is an ancestor — `git merge-base --is-ancestor` → exit 0; base tip `297e17927ba9342a87ba27a48cc5270a001de7cb`).
Working-tree content equals `HEAD` at measurement (`git diff --stat` empty — see F2 for the transient window
that forced a re-measure).

## Axes named

1. **adjacency (C2, judged axis for this seat)** — `corpus/routed-findings.jsonl` rows 19–27 (0-based 18..26):
   each row gets an `owner` from `../shokunin.conf`, a frozen `disposition`, a runnable `check`, and a
   measured exit code.
2. **freshness (secondary, instrument only)** — the frozen counter's own freshness hazards: `check`
   executability under its cwd contract (F1) and production files changing under concurrent measurement (F2).

No model, alias, endpoint or serving-plane path was touched.

## What I did (item 1–5)

For each of the nine rows: read the row and its `source` pointer; resolved `owner` with quoted evidence
(sibling/lane PROVINCE line, the lane's own registry, or the finding's own subject); chose a `disposition`
from the frozen vocabulary; made `check` runnable under the counter's execution contract
(`bash -lc`, cwd = counter scratch dir, `LANE` exported) by prefixing `cd "$LANE" &&` and adding a `test -f`
guard to the negated checks; ran every check in an empty scratch cwd and recorded exit code.

`check` was rewritten for all nine rows (the frozen text is preserved in this report's table and in the
evidence for each row). Reason and measurement: F1 — the pre-existing text cannot pass or fail honestly
under the counter's own cwd.

Fragment: `.ufo/waves/round-51/w1/C2ExecC.jsonl` (9 lines, one complete row each; all nine original fields
preserved verbatim, `check` excepted; `owner`, `disposition`, `evidence` appended; no `next` — none of the
rows is `routed`/`referral`).

## Attribution table

| # | id | class | owner | disposition | check exit | evidence used (quoted) |
|---|----|-------|-------|-------------|-----------|------------------------|
| 19 | R42-R6 | scratch-guard-exit-contract | `kengaku` | accepted-risk | 1 | kengaku-only instrument: `plans/scratch_guard.py` exists in `kengaku-shokunin` and **not** in the fleet root; no sibling `PROVINCE.md` names it. Docstring `plans/scratch_guard.py:16-17`: “exit 2 when the root is not a directory or the sentinel cannot be read (cannot evaluate)”. |
| 20 | R42-R3-01 | entry-false-arithmetic | `kengaku` | fixed-historical | 0 | kengaku's own knowledge entry; errata landed at `77ea425a` (resolves) — entry:459-460 “209²−1 = 43680”, “209² = 43681”. |
| 21 | R42-R3-02 | registry-row-line-citation | `kengaku` | accepted-risk | 1 | kengaku's registry: `SKILL.md:600` still cites “(`:178-184`)” for `round42-c2`; `grep -n 'receipt or entry absent' plans/round42_c2_verify.py` → `184` (def v4 :178) and `238` (def v7 :231). |
| 22 | R42-R3-03 | entry-internal-inconsistency | `kengaku` | fixed-historical | 0 | kengaku's own knowledge entry; errata quotes entry:96 at entry:500 (“… dropped if that fails” (`:96`)); `77ea425a` resolves. |
| 23 | R42-R3-04 | entry-wrong-citation | `kengaku` | fixed-historical | 0 | kengaku's own knowledge entry; errata cites `plans/fibsqrt_probe.py:201` at entry:467 and :473; `77ea425a` resolves. |
| 24 | R42-R3-05 | entry-line-ref-off-by-one | `kengaku` | accepted-risk | 1 | kengaku's own entry; capture `corpus/evidence/round42/tb2-circuit-fibsqrt/test_outputs.py` numbers `def fibonacci` :26, `def isqrt` :39, `return x` :52, `x = x_new` :53, `def test_sqrt_fib` :56 → helpers span :26-53; entry:350 still says “(`test_outputs.py:26-52`)”, `SKILL.md:1208` already cites “:26-53”. |
| 25 | R42-R3-06 | readme-provenance-label | `kengaku` | accepted-risk | 1 | kengaku's `corpus/README.md:75` sources cell: “S125, S126, S127, S128 (terminal-bench-2 @ 2fd12b88)” vs `PROVINCE.md:539` “S125, S126, S127; S128 prior art”. |
| 26 | R42-R3-07 | registry-row-overstatement | `kengaku` | accepted-risk | 1 | kengaku's registry: `SKILL.md:702` still says the `## Case table` is “equal to the receipt row”; `plans/round42_c2_verify.py:292-299` builds `want` as (case id, tests, observed) triples. |
| 27 | R42-R3-08 | gate-undeclared-dependency | `kengaku` | accepted-risk | 1 | `PROVINCE.md:262`: “`plans/pkg_gate.py` stays this lane's own gate (tameshi … never edits a sibling's gate)”; `plans/pkg_gate.py:276` still runs `uv run --no-project --with biopython==1.85`, while `plans/fibsqrt_probe.py` imports only stdlib (argparse, dataclasses, hashlib, os, pathlib, re, shutil, subprocess, sys, tempfile). |

Disposition rule applied (claims doc §C2): `routed`/`referral` require a **non-`kengaku`** owner plus `next`,
so they are unavailable to every row here — all nine findings are defects in this lane's own artifacts
(`SKILL.md`, `corpus/knowledge/`, `corpus/README.md`, `plans/`). A closed row whose `close` names a resolving
commit is `fixed-historical`; an open row whose check still fails at the tip is `accepted-risk`
(the lane carries it; no seat may edit production). `refused-out-of-scope` would contradict
`PROVINCE.md:262` for `plans/pkg_gate.py` and the lane's own registry/entry ownership for the rest.

## Commands and observed output (verbatim)

### Frozen counter over my fragment

```
$ python3 plans/round51_routing.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin \
    --ledger .ufo/waves/round-51/w1/C2ExecC.jsonl --run-checks --scratch <scratch>/counterA
LEDGER .ufo/waves/round-51/w1/C2ExecC.jsonl rows=9
FIELDS complete=9 incomplete=0
OWNERS attributed=9 unattributed=0
DISPOSITIONS set=9 bad=0
SOURCES resolved=9 missing=0
CHECKS present=9 absent=0
VERIFIED ran=0 passed=0 failed=0
CLOSE_REFS resolved=3 missing=0
NEXT violations=0
PREDICATE R51-C2 pass
exit=0
```

(`ran=0` is the expected consequence of `fixed-historical` + `accepted-risk`: the run-checks leg only
executes `fixed-verified` rows. The checks were therefore exercised directly — next block.)

### Every check, executed exactly as the counter does (`bash -lc`, empty cwd, `LANE` exported)

```
R42-R6     accepted-risk    exit=1 out=''
R42-R3-01  fixed-historical exit=0 out=''
R42-R3-02  accepted-risk    exit=1 out=''
R42-R3-03  fixed-historical exit=0 out=''
R42-R3-04  fixed-historical exit=0 out=''
R42-R3-05  accepted-risk    exit=1 out=''
R42-R3-06  accepted-risk    exit=1 out=''
R42-R3-07  accepted-risk    exit=1 out=''
R42-R3-08  accepted-risk    exit=1 out=''
```

### Fail-closed control (`LANE` pointed at an empty directory)

```
R42-R6     exit=1
R42-R3-01  exit=1
R42-R3-02  exit=1
R42-R3-03  exit=1
R42-R3-04  exit=1
R42-R3-05  exit=1
R42-R3-06  exit=1
R42-R3-07  exit=1
R42-R3-08  exit=1
```

All nine fail when the lane files are absent — the `test -f` guards removed the vacuous pass that the
original negated checks produced (F1).

### Row R42-R6 defect reproduction (scratch fixture, `$D/.ROUND-ROOT-SENTINEL` chmod 000)

```
$ python3 plans/scratch_guard.py check <scratch>/guardfix
ROOT <scratch>/guardfix
SENTINEL .ROUND-ROOT-SENTINEL present=no reason=sentinel-unreadable:Permission denied
SEAT seatA bytes=0 size=0B
ROOTFILES n=1 names=.ROUND-ROOT-SENTINEL
TOTAL seats=1 bytes=0 size=0B
CHECK red reason=sentinel-unreadable:Permission denied round=None want=* seats=1
exit=1
```

Docstring promises exit 2 for exactly this case; the selftest prints `SELFTEST ok=36/36` and its sentinel
cases are `check-sentinel-missing`, `check-sentinel-unparseable`, `refuse-sentinel`,
`refuse-symlink-to-sentinel` — no unreadable-sentinel case. Finding is live; `accepted-risk` is the honest
disposition (fix = one selftest case plus an exit-2 path, neither of which a seat may land).

### Instrument health

```
$ python3 plans/round51_routing.py --selftest
… [selftest] cases=11 failures=0
[selftest] ALL PASS
exit=0
```

## Findings for the L1 (routed defects, not mine to land)

**F1 — the frozen counter's `check` cwd contract makes every lane-relative check dishonest.**
`plans/round51_routing.py:121-124` runs each check as `bash -lc <check>` with `cwd=<scratch>` and
`LANE=<lane>` exported. The 61 pre-existing checks are written lane-relative, so under `--run-checks` they do not measure
the lane. Measured with the verbatim original text in an empty cwd:

```
[idx18] exit=2 out=''
[idx19] exit=2 out='grep: corpus/knowledge/tb2-circuit-fibsqrt-grader.md: No such file or directory'
[idx20] exit=2 out='grep: SKILL.md: No such file or directory'
[idx21] exit=0 out='grep: … No such file or directory'   <- VACUOUS PASS
[idx22] exit=2 out='grep: … No such file or directory'
[idx23] exit=2 out='grep: … No such file or directory'
[idx24] exit=2 out='grep: corpus/README.md: No such file or directory'
[idx25] exit=0 out='grep: SKILL.md: No such file or directory'   <- VACUOUS PASS
[idx26] exit=0 out='grep: plans/pkg_gate.py: No such file or directory'   <- VACUOUS PASS
```

Consequences: (a) no row can ever be `fixed-verified` with its original text, so the `CHECK_FAILED` leg is
inert for the whole ledger; (b) the three negated checks pass vacuously, i.e. the counter cannot tell
“claim holds” from “file missing”. Repair pattern (applied to my nine rows, and already used by sibling
fragment `C2ExecF.jsonl`): `cd "$LANE" && …`, plus `test -f <file> &&` in front of every negated check.
This is lane-wide, not row-local — it must be applied to all 71 rows at landing or the `CHECK_FAILED 0`
leg is decorative.

**F2 — production files were truncated in place while seats were measuring.**
At 15:20 on 2026-10-28 two tracked lane files read 0 bytes in the worktree
(`plans/scratch_guard.py` — earlier `wc -l` 622 — and `corpus/knowledge/tb2-circuit-fibsqrt-grader.md`),
and at 15:22:02 three tracked files carried mtime-only changes:

```
$ git -C <lane> status --porcelain=v1
 M plans/round42_c1_verify.py
 M plans/routed_open.py
 M plans/scratch_guard.py
$ git -C <lane> diff --stat
 plans/round42_c1_verify.py | 0
 plans/routed_open.py       | 0
 plans/scratch_guard.py     | 0
 3 files changed, 0 insertions(+), 0 deletions(-)
$ stat -c '%n %s %y' plans/round42_c1_verify.py plans/routed_open.py plans/scratch_guard.py
… 35983 2026-10-28 15:22:02.239911052 -0300
… 10877 2026-10-28 15:22:02.242982144 -0300
… 25643 2026-10-28 15:22:02.245919224 -0300
```

Content is intact again (`git diff --stat` now empty; sizes equal `git cat-file -s HEAD:<path>`), so this is
a truncate-and-restore cycle by some in-place mutation harness inside the lane worktree — not a landed
change. Every measurement in this report was re-taken after the restore. Two effects the L1 must decide on:
concurrent seats measure a moving target (my first pass over the same checks read the 0-byte window and is
discarded), and a mutation harness that writes production paths in place is exactly what the wave's
write-scope rule forbids — the seat that owns it should work in its clone, not in the lane.

**F3 — `--ledger` outside the lane crashes the frozen counter.**
`python3 plans/round51_routing.py --lane <lane> --ledger <scratch>/frag.jsonl --run-checks` →
`ValueError: '<scratch>/frag.jsonl' is not in the subpath of '<lane>'` at `plans/round51_routing.py:77`,
exit 1 with **no** `PREDICATE` line. A caller cannot distinguish an instrument crash from a predicate
failure. Low severity (the frozen command passes no `--ledger`), but it defeats the `--ledger` flag that the
argument parser advertises.

**F4 — the three `fixed-historical` rows are also green now.** `R42-R3-01`, `-03`, `-04` exit 0 at the tip,
so their disposition could have been `fixed-verified`; I kept `fixed-historical` because their `close`
names the landing commit `77ea425a` (resolves via `git cat-file -e 77ea425a^{commit}`) and that keeps the
`CLOSE_REF` leg of the predicate non-vacuous (`CLOSE_REFS resolved=3 missing=0`).

## Limits

- Nine rows of 71. No row added, none deleted; all nine original fields preserved verbatim except `check`
  (rewritten for F1; original text quoted above and per row in `evidence`).
- Owners are all `kengaku` because all nine findings are defects in this lane's own artifacts. I did not
  invent a non-kengaku owner to make a row `routed`; the counter's `NEXT` leg is satisfied by having no
  `routed`/`referral` row in this fragment.
- `accepted-risk` states “the lane carries this, unfixed”. I did not judge whether the L1 should fix any of
  the six at landing — that is the L1's call, and the checks are written so that a landed fix flips them to
  exit 0 without further edit.
- Endpoint/network claims were not probed: this seat measured only local files and local commands.
- No production file, `MANIFEST.json`, `.ufo/state`, `.scratch/` or sibling repo was written. Writes:
  this report and `.ufo/waves/round-51/w1/C2ExecC.jsonl`.
- No tool was installed or upgraded (nothing was needed); no pacman transaction was attempted.
- Scratch `/fast/scratch/hyaku/kengaku-r51/C2ExecC` held the fixtures, counter scratch dirs and the
  control fragment; it was removed before yield (see below). Free space seen: `/dev/nvme1n1p2 804G 264G
  used 540G avail 33% /fast` — no ENOSPC.

VERDICT: PASS — nine ledger rows (19–27) attributed: `owner=kengaku` on all nine with quoted evidence,
three `fixed-historical` (close `77ea425a` resolves; checks re-derived exit 0), six `accepted-risk`
(checks re-derived exit 1 at the tip), every check rewritten lane-rooted and fail-closed, and the frozen
counter prints `PREDICATE R51-C2 pass` (`rows=9 attributed=9 bad=0 SOURCES missing=0 CHECKS absent=0
CLOSE_REFS resolved=3 NEXT violations=0`) over the fragment at `4090c3db`. Three routed defects handed to
the L1: F1 (check cwd contract, lane-wide), F2 (in-place truncation of production files during the wave),
F3 (`--ledger` crash outside the lane).
