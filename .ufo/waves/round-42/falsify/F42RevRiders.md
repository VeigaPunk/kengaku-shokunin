# F42RevRiders — the three riders (round-42 wave 2, falsify)

Seat: F42RevRiders (reviewer, leaf). Basis: a clean clone of the lane at the docs tip
`508434ad55c709337065611691c426f05875492d` (the state this wave attacks); freeze `bc856d80…`,
landing `ff14d76d…`, first probe run `523b2780…`. The lane's HEAD has since moved to `3e8a2e5e`
("tip re-measure at 508434ad (verdicts equal) … falsify ready marker") — not in my clone; where it
matters I measured the lane's worktree read-only and say so. Every check ran from the clone root.

Envelope for every run that can write files (host-safety rule), with `HOME`/`TMPDIR` in scratch and
`PATH` restricted to system dirs inside:

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>
```

Receipts (envelope line, START/END `date +%T`, `ls -A /home/vgpnk/.local/bin | sha256sum`
before/after): `receipt-A-roundclose-selftest.txt`, `receipt-B-gate-path.txt`,
`receipt-C-scratch-guard.txt`, `receipt-D-ledger-rows.txt`, `receipt-E-lane-worktree.txt` — all in
this directory. Nothing in the lane outside this report dir and these five files was written; no
git/jj mutation anywhere; no tools installed (nothing needed beyond stdlib + the fleet census).

---

## 1. `plans/round_close.py` R5 fix — no defect found

Diff vs freeze `bc856d80` (`git diff bc856d80 508434ad -- plans/round_close.py`): exactly 9
insertions — `import shutil` plus the 8-line reset block at the top of `build_fixture`, including
the provenance comment "Round-41 closure R5 carried item; draft and red/green check by wave-1 seat
R42R5Carried." Landed sha256 `cd581f8a263372b164f5a4fdf20e25eefaa22d2087097de75e463c19043a8144`
(wave-1 draft was `0148c8e7…`; the extra attribution comment line explains the difference). Nothing
else in the file changes; the gate path (`main` → `gate` → order_check/census) is untouched by the
diff.

- **--selftest twice on one --work** (the R5 acceptance): run1 rc=0, run2 rc=0, run2 stdout
  byte-equal to run1 (`cmp`), stderr empty both runs, no nested `corpus/knowledge/knowledge`
  (receipt-A). Matches the L1's own `integrate/r5-round-close-check.txt` (run1_rc=0 run2_rc=0,
  "CHECK PASS rc=0 twice, identical output, no nested copy").
- Third run with a symlink planted at `<work>/B-executed-p10` → victim dir intact (only `.keep`),
  the link consumed and rebuilt as a real dir, rc=0 — the symlink branch behaves as drafted.
- Default path (no `--work`): rc=0, `SELFTEST checks=5 ok=5 failed=0`.
- **Gate path unchanged for rounds 41/42**: landed clone vs a clone with the 9 lines
  reverse-applied (`plans/round_close.py` sha back to the freeze value `112b52f0…`): gate outputs
  for round 41 AND round 42 byte-identical except the 4 lines that embed the clone's own path
  (header + census cmd echo); both rounds `ROUND-CLOSE RESULT PASS exit=0`, census
  `exit=0 warnings=15`, stderr empty (receipt-B).
- Residual (restated, accepted by wave-1): the reset deletes any existing `<work>/<case-id>`
  unconditionally — no fixture-signature check — so a caller pointing `--work` at a non-scratch
  directory containing same-named subdirs loses them. `--work`'s help documents "scratch parent";
  note-level, by design.
- Observation: the L1's own receipt `integrate/r5-round-close-check.txt` carries times + localbin
  digests but no `ENVELOPE` line (Q32 asks receipts to carry the envelope line).

## 2. `plans/scratch_guard.py` — selftest green; one doc/behavior defect + one selftest gap

Landed bytes sha256 `f0360e3028c79ce32fcabf7f89f0103b88205200bce802a8b2520e1f9364aa5d` — identical
to the wave-1 build copy's sha in `R42ScratchGuard.md`; the landed tool is the drafted tool.

- **--selftest on the landed bytes**: `SELFTEST ok=36/36`, rc=0 (receipt-C).
- **Escape probes beyond the selftest** (private fixture root): every refusal holds — `..`
  (relative and absolute), symlink file/dir escapes, symlink-to-sentinel/root, another seat,
  invalid seat forms, untrusted root, fs-root; `--dry-run` does not bypass a refusal (rc 2); a
  trailing-slash file target deletes the file correctly (normpath strips the slash); an absolute
  target inside the seat, the seat dir itself, and a root spelled via a symlink all behave as
  documented; a **hardlink of the sentinel** unlinked from inside a seat leaves the sentinel
  byte-intact (no escape). On the real root: `check --round 42` rc=0 (35 seats, 13.9 GiB walked,
  read-only), dry-run `WOULD-DELETE` on my own scratch path, real sentinel sha `efc83fb9…`
  unchanged.
- **Mutant** (dotdot guard removed from a scratch copy): selftest goes red 33/36 —
  `refuse-root-dot, refuse-dotdot-relative, refuse-dotdot-absolute` — rc=1; the selftest is
  non-vacuous on the landed bytes. (Without the dotdot guard the three targets are still refused —
  `target-is-root` / `target-resolves-outside-seat` / `target-outside-seat` — the dotdot guard is
  defense-in-depth; the selftest pins the *reasons*, which is what catches its removal.)

**D3 (defect, doc/behavior): `check` on a root whose sentinel is unreadable exits 1; the docstring
documents exit 2.** Probe: sentinel `chmod 000` → `check` prints `SENTINEL .ROUND-ROOT-SENTINEL
present=no reason=sentinel-unreadable:Permission denied` … `CHECK red
reason=sentinel-unreadable:Permission denied …` and exits **1**. The docstring says it twice:
"exit 2 when the root is not a directory or the sentinel cannot be read (cannot evaluate)" and the
exit-code summary "2 usage, cannot evaluate, or a refused delete". `safe-rm` is consistent
(`root-untrusted` → 2); only `check`'s exit code contradicts its own contract. A consumer branching
on 1-vs-2 ("red" vs "cannot evaluate") misclassifies the failure. Location:
`plans/scratch_guard.py` docstring, check section + exit-code summary; wave-1's contract table
(`R42ScratchGuard.md`) carries the same wrong map.

**D4 (defect, selftest coverage): the 36-case selftest has no unreadable-sentinel `check` case.**
The check cases cover green, round-mismatch, sentinel-missing, sentinel-unparseable,
non-directory, wrote-nothing, json — not unreadable. That gap is exactly what let D3 land green.
One added case (chmod 000 sentinel → expect the documented code) closes both, whichever way D3 is
resolved.

Notes (not defects): (a) a sentinel replaced by a symlink is *followed* by `check` (rc 0) and is
then listed as a SEAT named `.ROUND-ROOT-SENTINEL` with `ROOTFILES n=0` — cosmetic, and check's
integrity story is weak if a seat can rewrite the root (same-uid host: it can anyway; cooperative
model, documented limit 1); (b) a seat name whose `<root>/<seat>` is a regular file reports
`seat-missing` (mislabel); (c) an unreadable seat dir lists as `bytes=0` (misleading size);
(d) a symlinked seat's size is the link's own length; (e) the `target-nul` refusal is unreachable
via execve (NUL cannot appear in argv) — in-process defense only; (f) the seat argument is
self-asserted — any seat can pass another seat's name and delete inside it (inherent; the guard
binds paths, not identities).

## 3. `corpus/routed-findings.jsonl` — the six appended rows: one status mismatch, one stale check

The six rows are byte-equal to the wave-1 draft
(`.ufo/waves/round-42/build/R42RoutedRider/appended-rows.jsonl`, untracked in the worktree; diff
empty, 7862 bytes). All 16 rows validate (no `DEFECT line=` output); `routed_open.py --selftest`
12/12. Observe at the 508434ad clone (the tool runs every check, shell=True, cwd=lane):

| row | status | check rc | agrees? |
|---|---|---|---|
| R42-R1 | open | 1 | yes — c1–c4 pass; c5 fails: no uv pin in `plans/battery42/` (committed, 5 files) |
| R42-R2 | open | 1 | yes in a clean clone — but see D2 |
| R42-R3 | open | 1 | yes — filler control + `"V9"` present (c1=0, c2=0); no live-state reader (c3=1) |
| R42-R4 | open | **0** | **NO — MISMATCH (D1)** |
| R42-R5 | open | 2 | yes — `SETUP … not a round-38-list counter: missing=R37_REL,battery38_fixtures,attributed,FAMILY` |
| R40-R1.1 | closed | 0 | yes |

Older rows all agree (R39-R1/R39-R5/R40-R2/R40-R3/R40-R4 closed+pass; R39-R2 open+fail; R39-R3
blocked+fail; R39-R4 open+fail rc=2; R40-R1/R40-R5 no check). `OBSERVE rows=16 mismatched=1`,
observe exit 1 (receipt-D).

**D1 (defect, ledger): R42-R4's check passes at the landing while the row says open — the ledger's
own observe leg is red.** Standalone at the docs tip: `test "$(git diff d69452cf..HEAD --
corpus/SOURCES.md | grep -c '^-[^-]')" -eq 0` → `removed_lines=0`, and `grep -rqs 'never in place'
corpus/QUALITY.md corpus/SOURCES.md` → `corpus/QUALITY.md:759:## Round42 criterion — a SOURCES row
is corrected by a new superseding row, never in place` (the Q34 section states the rule in full).
The L1 landed the rule the row was waiting for but appended no closing row — the ledger is 16 rows
at the docs tip AND at the lane's current worktree. `routed_open.py --observe` at the docs tip:
`OBSERVE R42-R4 rc=0 observed=pass self=open MISMATCH`, `mismatched=1`, exit 1 — and it still
mismatches at the lane's current tip (receipt-E). Fix: append an `R42-R4.1` closed row (close
evidence = `corpus/QUALITY.md:759` + the standing no-removal invariant), the same way R40-R1.1 was
appended for R40-R1.

**D2 (defect, stale check): R42-R2's clause 3 pins the uncommitted build copy, not the landed
tool.** Clause 3 is `test -f .ufo/waves/round-42/build/R42ScratchGuard/scratch_guard.py`; at the
docs tip the ONLY committed file under `.ufo/waves/round-42/build/` is `swarm-registry.json`
(`git ls-files`) — the clause is unpassable in any clean clone, so the check can never go green
from the committed state; and no clause references the landed `plans/scratch_guard.py`, so the
check cannot see the tool that actually landed (deleting `plans/scratch_guard.py` would not flip
it). In the lane's worktree the untracked build copy exists, so the clause passes there and
R42-R2 becomes a SECOND mismatch: observe at the lane worktree = `mismatched=2` (R42-R2 and
R42-R4), exit 1 (receipt-E). The clause was right at draft time (tool absent, seat in flight) and
is wrong at the landing. Fix: an appended row whose check tests `plans/scratch_guard.py`
(committed).

Note-claim spot-checks, all verified in the 508434ad clone: `plans/round42_c1_verify.py` :302
`--unshare-ipc/--tmpfs /run`, :311 `--ro-bind-data`, :343 `def path_ok`, :504 path_ok use, :526
PINS, :635 `unattributed`, :108 the PATH constant keeping `/usr/local/bin`;
`claims/frozen-digests.txt:2` = `559fca0c…` (round42_c1_verify.py), `:8` = `948d5e1d…` =
sha256(`plans/order_check.py`); `build-spec.json` 3× `ROUND-ROOT-SENTINEL`;
`integrate/measure.sh` 1× `SENTINEL` (committed at this tip — the note's "untracked" was true at
the wave-1 tip `fda71ae`); `control-c2-filler.txt:1-3` as quoted; `control-c1-hostile-escape.txt`
SETUP line + `exit=2` and `claims/hostile/h_esc42.py` present; 9 `claims/*.txt` receipts carry
`ENVELOPE`; the two round-41 pointer files named in R42-R5's note exist.

## 4. Integration and process findings

**D5 (defect, integration): the landed guard has no SKILL.md registry row.**
`grep -c 'scratch_guard\|scratch-root-guard' SKILL.md` → 0 (PROVINCE.md 0, README.md 0;
`LOG.md:1299` mentions the landing once: "R2 `plans/scratch_guard.py` (selftest 36/36)"). The
wave-1 draft row (`R42ScratchGuard.md` §Draft SKILL.md registry row) was not integrated; the
round-42 addendum names only `round42-c1-mutants`/`round42-c2`/`fibsqrt-probe`. The guard is
discoverable only through the wave context (`build-spec.json`) and the LOG line — the registry is
where the next round's seats will look.

**Q32 process note: the plain `ls -A ~/.local/bin | sha256sum` digest is not a stable quantity on
this host.** The harness `ls` is a shell builtin that does not sort: for the same 102-entry set
(builtin-sorted == GNU-sorted, diff empty, no subdirectories) I read three different plain digests
within ~2 minutes — `77408cab…` (18:10:38, runs A/B before), `b5f03609…` (18:10:41-42, runs A/B
after), `8cf5b151…` (18:11+) — while the order-independent digest stayed `77408cab…` in every
measurement that computed it. `stat` gives `/home/vgpnk/.local/bin` mtime `18:10:45` — the listing
was modified host-side while four seats' runs were live. My runs had no write path to that
directory (ro-bound inside bwrap; PATH inside excludes it; the outer scripts only read it and
write scratch), so the A/B pre≠post is concurrent authorized seat activity, not my runs.
Recommendation: Q32 receipts should hash the **sorted** listing (`ls -A … | sort | sha256sum`); a
pre≠post plain digest alone proves nothing.

Also: the wave-1 build tree is untracked at the docs tip (only `build/swarm-registry.json`
committed) — the wave-1 reports and build copies (incl. the R42ScratchGuard draft and the
R42RoutedRider rows draft) live only in the lane's worktree. Anyone re-running the R42-R2 check
from a clean clone sees clause 3 fail (D2).

## Defects (numbered)

- **D1 (high, ledger):** R42-R4 open with a passing check — `routed_open.py --observe` exits 1
  (`mismatched=1`) at the landing tip and still at the lane's current tip; closing row missing.
- **D2 (medium, ledger):** R42-R2's clause 3 pins the uncommitted build copy
  (`.ufo/waves/round-42/build/R42ScratchGuard/scratch_guard.py`); the landed
  `plans/scratch_guard.py` is invisible to the check; unpassable from a clean clone, and a
  worktree-only pass.
- **D3 (low, guard):** `check`'s documented exit 2 for an unreadable sentinel is actually 1
  (docstring vs code, confirmed by chmod-000 probe).
- **D4 (low, guard):** the 36-case selftest lacks the unreadable-sentinel `check` case that would
  have caught D3.
- **D5 (low-medium, integration):** no SKILL.md registry row for the landed guard (wave-1 draft
  row not integrated; LOG.md mention only).

Residuals/notes not counted as defects: round_close `--work` reset footgun (documented
scratch-parent contract); guard notes (a)–(f); the L1's r5 receipt missing the `ENVELOPE` line;
the Q32 plain-digest volatility.

Report: .ufo/waves/round-42/falsify/F42RevRiders.md

VERDICT: riders-defects-5
