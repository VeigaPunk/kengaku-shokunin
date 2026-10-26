# F40RoundClose — falsifying `plans/round_close.py` (wave 2, roster F40RoundClose)

Seat: executor, round 40 wave 2 (FALSIFY). Target: the landed round-close caller
`plans/round_close.py`, measured on a clean clone of the lane tip
`ec1005a2a28bc5cfdde7723374368ed4cc956eed` (branch `master`). Scratch
`/fast/scratch/hyaku/kengaku-r40/F40RoundClose/` (NVMe, removed at exit). Every tool invocation
below ran inside
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent`.
No lane file was written, no commit, no jj command, no `systemd-run`; no tool installed (pacman paused
host-wide, nothing needed).

Tool bytes are the reviewed draft: `sha256sum plans/round_close.py` →
`112b52f0051357491b1654932948989d57b923c22bea817c15b710e5f9785c3b`, identical to wave-1's
`R40CloseCheck` digest, and `git diff ec172168 ec1005a2 -- plans/round_close.py plans/order_check.py`
is empty (the landed-measurement tip `ec172168` is an ancestor of my tip and carries the same bytes).
`plans/order_check.py` is `948d5e1d2b34…` (unchanged, as C1 pins it).

## 0. Receipt map (all in `.ufo/waves/round-40/falsify/F40RoundClose/`)

| receipt | what it proves |
|---|---|
| `baseline.txt` | shipped `--selftest` 5/5, rounds 36-40, census discovery (2 ways + 1 refusal), census `--file`≡`--root`, non-executable census |
| `mutants.txt` | 14 single-line mutants × (`--selftest` + rounds 36-40), baseline beside each |
| `attacks.txt` | attacks A-G: the cases the shipped controls cannot express |
| `provenance.txt` | per-round, per-rule receipt provenance; fixture D run under shipped and mutant bytes |
| `hermeticity.txt` | `--selftest` green→red from a registry row alone (no tool change) |
| `zero-receipt.txt` | both zero-receipt routes; live-lane census re-read |

Clone hygiene: `git -C "$S/lane" status --porcelain` empty before the matrix and after every attack
(`FINAL clone_status='<clean>'`, `attacks.txt`; `RESTORE … dirty_lines=0` after each temporary edit).

## 1. The two required demonstrations

### 1.1 `--selftest` — 5/5 green, and what each case is worth

```
$ python3 plans/round_close.py --lane <clone> --selftest --work <scratch>/st --census <fleet>/scripts/sources-census.sh
SELFTEST case=A-excused-p10 shape=receipt-last expect=0 got=0 verdict=ok
SELFTEST case=B-executed-p10 shape=receipt-last expect=1 got=1 verdict=ok
SELFTEST case=C-receipt-first shape=receipt-first expect=1 got=1 verdict=ok
SELFTEST case=D-receipt-uncommitted shape=receipt-uncommitted expect=2 got=2 verdict=ok
SELFTEST case=E-no-receipt-named shape=no-probe expect=2 got=2 verdict=ok
SELFTEST checks=5 ok=5 failed=0   exit=0
```
(`baseline.txt`.) Wave-1's number reproduces on a fresh clone of the tip.

### 1.2 Rounds 36-40 on a clean clone — 38 red, 39/40 green (and 37 red)

```
$ python3 plans/round_close.py --lane <clone> --round N --census <fleet>/scripts/sources-census.sh
round 36 exit=0  order receipt=corpus/evidence/round36/regex-log-probe.txt exit=0 census exit=0 warnings=15
round 37 exit=1  order receipt=corpus/evidence/round37/git-webserver-probe.txt exit=1 census exit=0 warnings=15
round 38 exit=1  order receipt=corpus/evidence/round38/build-pmars-probe.txt exit=1 census exit=0 warnings=15
round 39 exit=0  order receipt=corpus/evidence/round39/git-leak-probe.txt exit=0 census exit=0 warnings=15
round 40 exit=0  order receipt=corpus/evidence/round40/db-wal-probe.txt exit=0 census exit=0 warnings=15
```
(`baseline.txt`.) The card's expectation holds exactly: 38 red, 39 and 40 green; 36 green and 37 red
match wave-1's series table. The 38-vs-39 difference comes from `ORDER HIT … round-38/claims/control-c2-skip.txt`
(the gate's non-excused `P10` line) and nothing else.

**Operability caveat, measured, not a defect:** on a clone under `/fast/scratch` the census is *not*
discoverable from the lane's parents, so the bare documented form exits 2 —
`exit=2 stderr=ROUND-CLOSE ERROR no census script (scripts/sources-census.sh); pass --census PATH`
(`baseline.txt`). Supplying either `--census <path>` or
`SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin` gives exit 0 (`same five rounds…` block). The docstring
names this (`round_close.py:49-53`, "a clone that has neither is a setup error, never a skipped leg"),
so the only inaccuracy is that the frozen expectation is reproducible only with one of the two flags.

## 2. Does it ever pass with zero receipts? No.

Two routes, both shipped-bytes, both exit 2 (`zero-receipt.txt`):

1. claims naming no probe and no receipt:
`ROUND-CLOSE ERROR the claims name no readable receipt for round 41` → `exit=2`.
2. claims naming a probe whose receipt exists neither on disk nor in HEAD:
`ROUND-CLOSE note=skipped-unreadable-receipt corpus/evidence/round41/git-leak-probe.txt` then the same
`ERROR` → `exit=2`. The note path is what `round_close.py:33` documents; it fires exactly here and
nowhere in rounds 36-40.

The guard that makes this true is one line, `round_close.py:191` (`if not receipts:`), and it is
load-bearing: mutating it to `return 0` (M07) makes the tool **PASS with zero receipts** — measured,
`ATTACK-C M07-zero-receipt-pass --round 41 exit=0` vs `shipped --round 41 exit=2` (`attacks.txt`).

## 3. Mutation matrix — 14 single-line mutants, 6 killed

Each mutant is one whole line replaced (`assert` one whole-line match), compiled, then run through
five fixture repos and five real rounds. "Killed" = `--selftest` exit ≠ 0 **or** any round exit differs
from baseline `{36:0, 37:1, 38:1, 39:0, 40:0}`.

| # | mutant (one line) | category | `--selftest` | rounds changed | verdict |
|---|---|---|---|---|---|
| M01 | rule (a) regex can never match (`\breceipts?\b`→`\breceiptzz\b`) | receipt rule (a) | 0 (5/5 ok) | none | **SURVIVED** |
| M02 | rule (b) suffix loosened `-probe\.txt`→`\.txt` | receipt rule (b) | 0 (5/5 ok) | 39→1, 40→1 | KILLED (rounds only) |
| M03 | rule (c) derivation drops `_`→`-` | receipt rule (c) | 1 (3/5 fail) | 38→2, 39→2, 40→2 | KILLED (both) |
| M04 | rule (c) hardcodes `round{40}` | receipt rule (c) | 1 (3/5 fail) | 38→2, 39→2 | KILLED (both) |
| M05 | order verdict map swapped (`0`↔`1`) | exit mapping | 1 (3/5 fail) | all five flip | KILLED (both) |
| M06 | order leg: unknown rc maps to `PASS` | exit mapping | 1 (1 case) | none | KILLED (selftest only) |
| M07 | zero-receipt guard → `return 0` | exit mapping | 1 (case E) | none | KILLED (selftest only) |
| M08 | no-claims-file guard → `return 0` | exit mapping | 0 | none | **SURVIVED** |
| M09 | census leg's status contribution → `max(status, 0)` | census leg | 0 | none | **SURVIVED** |
| M10 | readability filter → `if True:` | receipt filter | 0 | none | **SURVIVED** (stricter, §5.4) |
| M11 | dedup removed (`if rel:`) | receipt dedup | 0 | none | **SURVIVED** |
| M12 | selftest exit → `return 0` | selftest exit | 0 | none | **SURVIVED** |
| M13 | `find_census` returns a non-file path | census setup | 0 | none | **SURVIVED** (guard doubled) |
| M14 | gate's census `is_file()` guard removed | census setup | 0 | none | **SURVIVED** (guard doubled) |

`SUMMARY total=14 killed=6 survived=8` (`mutants.txt`). The division of labour is precise and worth
stating because it is the calibration result:

- **rule (b)'s suffix condition is calibrated by the rounds alone** (M02: selftest stays 5/5 green —
  the fixtures resolve by rule (c) only). Round 40's own claims quote
  `corpus/evidence/round40/db-wal-dry-cases-freeze.txt` (`plans/round-40-claims.md:78`), which a
  loosened rule (b) would gate as a receipt and turn red: `receipts=2` for round 40.
- **rule (c) is calibrated by both** legs (fixture claims name `plans/git_leak_probe.py`,
  `round_close.py:231`).
- **the ERROR mapping and the zero-receipt guard are calibrated by the selftest only** (M06, M07): no
  landed round produces an order-tool rc > 1 or an empty receipt set.
- **the census leg and both setup guards are calibrated by neither** (M08, M09, M13, M14).

## 4. Attacks the shipped controls cannot express

`attacks.txt`, shipped bytes vs the surviving mutant, clone temporarily edited and restored clean.

| attack | shipped | mutant | shows |
|---|---|---|---|
| A: `plans/order_check.py` replaced by a stub exiting 3 | `exit=2`, `exit=3 verdict=ERROR` | M06 `exit=0`, `exit=3 verdict=PASS` | a leg that cannot be evaluated is a setup error today; nothing shipped would notice it becoming a pass (M06 is caught only by selftest case D) |
| B: census returns exit 1 with an `E12` finding | `exit=1`, `census exit=1 warnings=0 verdict=FAIL` | M09 `exit=0`, same census line | **the census leg has no shipped control at all** |
| C: claims naming nothing (round 41) | `exit=2` | M07 `exit=0` | §2, PASS with zero receipts |
| D: `--round 99`, no claims file | `exit=2`, `no claims file: plans/round-99-claims.md` | M08 `exit=0` | setup guard untested by the shipped set |
| E: claims whose only receipt source is rule (a) | `receipts=1`, order `exit=2 verdict=ERROR` | M01 `receipts=0` | rule (a) *works*, but see §5.2 — no landed round needs it |
| F: round-40 claims gain one line `Receipt: \`corpus/evidence/round38/build-pmars-probe.txt\`` | before `exit=0`, after `exit=1 receipts=2` | — | rule (a) is round-agnostic: a foreign receipt is gated as this round's |
| G: `--census /nonexistent/…` | `exit=2` | M13, M14 `exit=2` | the setup guard is double-implemented (`main` and `gate`), so M13/M14 are *equivalent* mutants — their survival is redundancy, not a hole |

## 5. Findings

Each names what it attacks and the receipt that carries the number.

### 5.1 The census leg — half the tool's contract — has no shipped control (F1)
M09 sets the census leg's status contribution to `max(status, 0)`: `--selftest` stays 5/5 green and
all five rounds return the baseline exits (`mutants.txt`). Every fixture's census exits 0, measured
directly (`census_exit=0` on fixture A and B registries) — the fixtures copy a clean
`corpus/SOURCES.md`, so the census leg is never *seen failing* by the selftest. Wave-1's control
(one injected `E12` row, `R40CloseCheck.md` §5.3) was a hand run, not a shipped case. Consequence: a
regression that discards the census verdict passes the entire shipped control set; only my attack B
separates `exit=1` (shipped) from `exit=0` (mutant). This is a proof gap, not a live defect — the
landed bytes are right (`ATTACK-B shipped exit=1`).

### 5.2 Rule (a) contributes zero distinct receipts across rounds 36-40, and its docstring is wrong about round 36 (F2, F3)
`provenance.txt`, per round: `a_hits=[]` for 36, 38, 39, 40 and `a_hits=[corpus/evidence/round37/git-webserver-probe.txt]`
for 37 — the same path rule (b) already yields, so `a_distinct_only=[]` for every round. M01 (rule (a)
dead) is therefore invisible to both legs. The docstring says at `round_close.py:26`
"(rounds 36 and 37 write it this way)" — for round 36 that is false: round 36's `Receipt:`-free text
resolves by rule (b) *and* rule (c) (four derived candidates, one path). The only landed round that
writes rule (a) is 37, where rule (b) is redundant. Attack E proves the rule is live code (synthetic
claims: `receipts=1` shipped, `receipts=0` under M01), so this is a coverage/doc defect, not dead code.

### 5.3 Rule (a) has no round filter — one quoted foreign receipt flips a green round red (F4)
`round_close.py:84` matches any `Receipt: `path.txt`` line; rule (b) filters `round(\d+) == round_no`
(`round_close.py:87,120-121`). Attack F: adding one line naming round 38's receipt to round 40's
claims takes round 40 from `exit=0` to `exit=1 receipts=2` with
`order receipt=corpus/evidence/round38/build-pmars-probe.txt exit=1 verdict=FAIL` (`attacks.txt`).
Bounded: the direction is false **red** (a claims file that merely *quotes* an older receipt to
discuss it now fails its own round), never false green. A future round that says "the receipt
`corpus/evidence/roundNN/…-probe.txt`" in prose while naming its own probe elsewhere would be gated
on the wrong round's receipt. Not triggered by 36-40.

### 5.4 The readability filter is unreachable in the direction it claims (F5)
`round_close.py:131` keeps a candidate if it is on disk *or* in HEAD. An uncommitted-on-disk receipt
therefore survives the filter and is rejected downstream by `order_check.py` itself:
`ORDER ERROR receipt not committed in HEAD`, composite 2 (`provenance.txt`, `FIXTURE-D shipped exit=2,
receipts=1`). Mutant M10 (`if True:`) produces the *identical* line and exit. So selftest case D
exercises `order_check`'s ERROR path, not the filter; the filter's drop path is exercised only when a
candidate is neither on disk nor in HEAD (my route-2 run, `note=` then exit 2). M10 survives because it
is strictly *stricter* (a missing candidate becomes an ERROR instead of being dropped), so it has no
false-green path. The docstring's `note=skipped-unreadable-receipt` is real (`zero-receipt.txt`) but
no landed round and no selftest case ever reaches it.

### 5.5 `--selftest` green is not a property of the tool alone (F6)
`build_fixture` copies `corpus/knowledge/` and `corpus/lessons/` from `--lane` because the census's
E11 needs the registry's used-by targets to exist (`round_close.py:254-257`). So the fixtures inherit
the lane's registry verdict. `hermeticity.txt`: with one `mined` row whose used-by path is missing
inserted into the clone's registry (exactly the in-flight shape wave-1 §6 reported for round 40),
and **no tool change**:

```
BEFORE selftest_exit=0 :: SELFTEST checks=5 ok=5 failed=0   (round40_exit=0)
AFTER  selftest_exit=1 :: SELFTEST case=A-excused-p10 expect=0 got=1 verdict=FAIL
AFTER  round40_exit=1  :: file	E11	S999 missing used-by corpus/knowledge/tb2-nonexistent-probe.md
```
Consequence for admission: a red `--selftest` does not localize to the verdict map — it can be the
registry's state — and the docstring's "five two-commit fixture repos" (`round_close.py:37-40`) each
carry a corpus copy, so "differing only in where the receipt and one `P10` line sit" holds for the
fixtures' *git history*, not for their census leg. Green today because the clone's census is clean
(15 W04, 0 E11; `baseline.txt`).

### 5.6 A census that exists but is not executable breaks the documented exit contract (F7)
Docstring: `2` = "a leg could not be evaluated" (`round_close.py:18-20`). With
`--census <copy of census, chmod 644>`:

```
exit=1
stdout_tail=ORDER RESULT PASS / ROUND-CLOSE order receipt=… exit=0 verdict=PASS
stderr_last=PermissionError: [Errno 13] Permission denied: '…/census-noexec.sh'
```
(`baseline.txt`.) An uncaught traceback, exit 1, and **no** `ROUND-CLOSE RESULT` line — so a receipt
reader keying on `RESULT` sees a truncated run, and a wrapper keying on `exit 2` for setup sees a
"failure" instead. Fail-safe in direction (1 ≠ 0, never a pass), but it is the one place where the
exit contract and the receipt grammar both break. Same class: `main()` checks `census is None` and
`gate()` re-checks `census.is_file()` — hence M13/M14's equivalence — but neither checks executability.

### 5.7 Two survivors that would hide a real regression (F8)
- M11 (dedup removed): invisible because duplicate candidates yield identical verdicts — round 39
  derives three identical paths (`provenance.txt`), and running `order_check` twice on a FAIL round
  still composites to 1. Dedup is defensive, untested, and cheap; not a defect, but a regression there
  is undetectable.
- M12 (`selftest` returns 0 regardless of `failed`): survives trivially while all cases pass, and is
  the one mutant that would make every other selftest-based kill vacuous. Combined with M03 (3/5 cases
  FAIL) the printed lines are the only remaining signal — measured: M03 alone gives `SELFTEST checks=5
  ok=2 failed=3` with `exit=1`, so the exit code is currently the sole machine-readable signal and
  nothing cross-checks it.

## 6. Limits of this measurement

- One tip (`ec1005a2`), one clone reused for every run, `--census` supplied explicitly (or `SHOKUNIN_ROOT`); the
  census leg is work-tree scoped by design, so its verdict moves with uncommitted edits — my clone was
  clean for every recorded run (`FINAL clone_status='<clean>'`).
- Mutants are single-line and hand-chosen along the card's three axes plus the two guards; 14 is not a
  complete mutant set (e.g. `norm_repo_path`'s outside-lane rejection, `gate`'s work-tree-top check and
  the `--round`/`--selftest` argument handling were not mutated — they have no candidate on any landed
  round and no selftest case, which is itself the pattern §5.1/§5.4 report).
- `SHOKUNIN_ROOT`/`--census` set from the outside; the tool's `sys.executable` is the host `python3`
  inside bwrap (`3.14`), matching the lane's shebang contract (`#!/usr/bin/env python3`).
- I did not re-run the lane's C1/C2 predicates, gates or linters (wave rule): this report judges
  `round_close.py` only.
- The docstring's "identical 15 W04 + 2 E11" (`round_close.py:51`) is a wave-1-time live-lane
  snapshot; on my clone and on the live lane now the E11 count is 0 (`baseline.txt`,
  `zero-receipt.txt` — the S119/S120 used-by entry landed). The *equivalence* claim re-measures true:
  `--file` vs `--root` differ only in the trailing `ok <path>` line, findings identical
  (`findings_lines=16 W04=15 E11=0`).

## 7. Tooling

None installed or upgraded. `bubblewrap 0.13.1` (`/usr/bin/bwrap`) and `python3` were already present;
`pacman` transactions are paused host-wide and nothing here needed one. No file was written to
`~/.local/bin`, `$HOME` outside scratch, `/usr`, `/etc`, `/run/user`, or any PATH directory.

VERDICT: round-close-mutants-caught-6/14
