# R41QualityDraft — two QUALITY criteria drafted from round 41's mined mistake and round-40 closure R2

Seat R41QualityDraft (scribe, leaf, no subagents). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` read at
`fc79f2a49be0221e138b3885fa0d83bc43b31a42` (`master`, wave-1 spec/dispatch commit; freeze `8ef8b4fc`, first
recorded probe run `f774a87a` are its two ancestors). Read-only throughout the lane: nothing staged, committed,
edited or created outside this report dir and its `R41QualityDraft/` subdir. No scratch dir was needed (no clone,
no fixture, no work tree); nothing was written under `/fast/scratch`, `/tmp`, `$HOME` or any PATH directory.
Report-dir writes at 15:41–15:42 -03; no write outside it exists to timestamp.

**Axes named before work (Godspeed).** X1 *format fidelity* — does each draft read as a QUALITY row (bold rule,
evidence with file:line or receipt line, executable check, shown-able-to-fail, limits, lesson, supersession)?
X2 *evidence grounding* — is every location and every number in the drafts produced by a command whose output
this report shows? X3 *calibration* — does a draft claim only what the receipt shows (no green half asserted
from an unrun counter)? X4 *discernment* — does each draft name the limit that would make a future reviewer
distrust it? X3 and X4 drove the drafts' `Limits` paragraphs.

## 1. Behaviour

Two criteria drafted in `corpus/QUALITY.md`'s existing row format (read at `corpus/QUALITY.md:1-569`, latest rows
Q27-Q30), numbered Q31 and Q32 because `grep -n 'Round41\|Q31\|Q32' corpus/QUALITY.md` returns nothing — the
file's last section heading is `## Round39 criterion — a class that recurs twice is closed by a gate over
committed history` (`:520`, running to the end, 569 lines), so both land as new `## Round41 criterion — …`
sections appended after line 569.

- **Q31** closes this round's mined mistake (`F40CritPlanNext` D1/D2: a round-41 predicate satisfiable with zero
  round-41 work) with the fix that demonstrably fails the vacuous shape: `TOTAL`/`FLOORS` literals plus a control
  that empties the mutant list while the literal stands.
- **Q32** closes round-40 closure R2 (host safety): read-only-PATH sandbox for every attack seat, the envelope in
  the receipt, and a timestamp for any host write.

Paste-ready text is `.ufo/waves/round-41/build/R41QualityDraft/quality-q31-q32.md` (identical to §2 below).

## 2. The drafts (paste block, no lane edit made)

## Round41 criterion — a frozen predicate's denominator is a literal the counter cannot self-satisfy

- **Q31 — a frozen predicate of the shape `MUTANTS total=<n> killed=<n> survived=0` is non-vacuous only when
  the counter binds the total and a per-tool floor to module literals and its pass conjunct reads them; a
  predicate whose only guard is `len(MUTANTS) == TOTAL`, with `TOTAL` written by the same author who writes
  the list, is satisfied by an empty list.** The round-41 plan as landed in round 40 failed exactly here: a
  copy of the round-40 counter with four appended lines (`MUTANTS = []`, `TOTAL = 0`) printed the full green
  predicate — `MUTANTS total=0 killed=0 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass`, exit 0 —
  with the landed battery present (`.ufo/waves/round-40/falsify/F40CritPlanNext.md:30-33`; receipt
  `F40CritPlanNext/runA-vacuous.txt:24,26`), and the plan's drafted predicate left `<n>` unbound
  (`F40CritPlanNext.md:105-115`, D1). The round-41 freeze binds both: `plans/round41_c1_verify.py:123-124`
  `TOTAL = 23`, `FLOORS = {"receipts": 13, "sources": 10}`; `:640-641` requires every floor ≥1,
  `sum(FLOORS.values()) == TOTAL`, and each tool's `[counted, killed]` equal to `[floor, floor]`; `:642` puts
  `len(MUTANTS) == TOTAL and floors_ok` in the pass conjunct; and `:631` prints
  `MUTANTS-BY-TOOL receipts=<k>/<n> sources=<k>/<n>`, so one total cannot stand for two tools. The
  discriminating control D2 asked for is committed and red with the literal untouched: the frozen counter
  copied with one appended line `MUTANTS = []` (`claims/control-c1-no-mutants.patch`, hunk `233a234`) prints
  `BATTERY fixtures=22 wrong=0 tampered=0 sidechannel=0` (`claims/control-c1-no-mutants.txt:24`),
  `MUTANTS total=0 killed=0 survived=0 invalid=0 null_detected=0` (`:25`), `MUTANTS-BY-TOOL receipts=0/0
  sources=0/0` (`:26`), `PREDICATE C1 fail` (`:29`), `exit=1` (`:30`), with `TOTAL = 23` and `FLOORS`
  unchanged — so the red is the binding and not a second edit, and it is sharper than the round-40
  falsifier's own copy, which zeroed the total as well.
  Check (executable, round-41 instance): `python3 plans/round41_c1_verify.py --lane .` prints `PINS total=2
  mismatched=0`, then `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, then `MUTANTS total=23
  killed=23 survived=0 invalid=0 null_detected=0`, then `MUTANTS-BY-TOOL receipts=13/13 sources=10/10`, then
  `PINS-AFTER mismatched=0`, then `PREDICATE C1 pass`, exit 0; the one-line-emptied copy prints
  `MUTANTS total=0` … `PREDICATE C1 fail`, exit 1. Both controls are committed with the freeze
  (`8ef8b4fc`), before `plans/battery41` existed (`ls plans/battery41` → `No such file or directory`,
  2026-10-26), so neither is fitted to the battery; the counter's own digest is a freeze row
  (`claims/frozen-digests.txt`: `8835a94b…  plans/round41_c1_verify.py`), which is what makes an edit of the
  list *and* the literals together visible at closure.
  Shown able to fail: the falsifier's run A is green with the list empty — the defect this criterion names; at
  the round-41 freeze the two controls are red for different reasons: no battery prints `BATTERY fixtures=0`,
  `MUTANTS total=23 killed=0 survived=23`, `PREDICATE C1 fail` (`claims/control-c1-nothing.txt`), and one
  appended line in `plans/tip_receipts.py` prints `PINS mismatched=1`, the 13 receipts mutants `invalid`,
  `PREDICATE C1 fail` (`claims/control-c1-tool-edited.txt`); a development run cannot be filed as either,
  because `--battery-dir`/`--only` print `PREDICATE C1 n/a …` (`claims/control-c1-hostile.txt:32`).
  Limits: the floors are literals the same author writes as the list, so the binding proves the list was not
  emptied and never that 23 is the right denominator (Q27's "the mutant list is the denominator" stands — a
  round can clear a 13/10 floor with reachable mutants only); the control is a copy plus a patch, so it prices
  the predicate's shape, not the frozen file, and the green half is the round's own predicate, not this
  control; the total counts rows, not distinct replacement sites — a row is only checked for
  `src.count(old) == 1` (`:589`) and mutant ids are not uniqueness-checked (fixture ids are, `:547`), so two
  rows carrying the same replacement both count; the per-tool equality leg makes a mutant's declared `tool`
  cell load-bearing, so a misfile reports `invalid` instead of reddening a floor; and the digest pin sees an
  edit, not a round that freezes low and lands green.
  Lesson: `.ufo/waves/round-40/falsify/F40CritPlanNext.md` §0 and D1/D2 (2026-10-26); discharged in
  `plans/round-41-claims.md` §C1, which states that "the predicate binds `TOTAL = 23` and `FLOORS =
  {receipts: 13, sources: 10}`", and in `plans/round41_c1_verify.py:13-17`. `corpus/lessons/round-41.md` does
  not exist at this draft (2026-10-26: `ls corpus/lessons/round-41.md` → `No such file or directory`), so the
  lesson pointer moves there when the round writes it. Supersedes: none; extends Q27's fourth limit and Q24's
  ordering leg (a control lands with the freeze, not after the first score).

## Round41 criterion — an attack seat's sandbox is part of its evidence

- **Q32 — a seat that runs a counter, a battery or a fixture build runs it inside a sandbox that makes every
  shared PATH directory and the host home read-only, with only its fixture root and a private tmp writable; its
  receipt carries the envelope command, a post-run check that the forbidden target is absent, and `date +%T`
  for every write it makes outside its report and its scratch dir.** A host-safety breach is not a style
  defect: round 40's `R40CritC1Counter` wrote a `git` shim, from inside the counter's build child, to
  `/home/vgpnk/.local/bin`, "a shared host directory ahead of `/usr/bin` on every lane's PATH"
  (`corpus/lessons/round-40.md:67`), and "the seat's receipts do not timestamp the writes"
  (`corpus/lessons/round-40.md:69`), so the window had to be inferred from other lanes' failures at
  ~14:05–14:07 -03 (`:69-71`); the attack's scoped form measured the same result, so the ambient write
  "bought nothing" (`:73`). The round-40 closure routed it as R2 (`corpus/lessons/round-40-verifier-spotcheck.md:95-96`)
  and neutralized both attack modules, which now raise `SystemExit` at import and point `SHIM_DIR` at
  `/nonexistent` (`build/R40CritC1Counter/crit_git_shim.py:10-12,18`, `crit_ledger_selfread.py:9-11`); measured
  2026-10-26:
  `ls -l /home/vgpnk/.local/bin/git` → `No such file or directory`. The round-41 implementation is the
  counter's own envelope — builds and tool runs in `bwrap --ro-bind / /` with the lane hidden,
  `--unshare-pid --unshare-net`, a fixed system PATH and `HOME=/nonexistent`
  (`plans/round41_c1_verify.py:56-70`, `:116`, `:318-325`) — plus a freeze control written to try the round-40
  vectors: `claims/hostile/h_host_writes.py` ("Targets are marker files under the user's home, NOT a PATH
  directory, so a sandbox failure is harmless", `:1-2`), whose receipt prints `SIDECHANNEL
  hostile/h_host_writes.py tokens=/home/` (`claims/control-c1-hostile.txt:2`),
  `build_write=OSError.lane_read=FileNotFoundError` (`:3`), `sidechannel=1` (`:27`) and `markers after the run:
  ls: cannot access '/home/vgpnk/k41-hostile-*': No such file or directory` (`:34`). Measured absence at the
  criterion's creation: `grep -c 'host-safety\|Host-safety' corpus/QUALITY.md` → 0 and
  `grep -c 'bwrap\|read-only-PATH' corpus/QUALITY.md` → 0; Q20 and Q23 govern where a gate run and a mutation
  clone live, not what the sandbox may write or what the receipt must show.
  Check (executable, round-41 instance): the two red halves are one command each —
  `grep -n 'markers after the run' .ufo/waves/round-41/claims/control-c1-hostile.txt` prints line 34 with
  `No such file or directory`, and `ls -l /home/vgpnk/.local/bin/git` fails with the same message; the forward
  leg is a per-receipt sweep — every report a round's claim cites as having run a counter, battery or fixture
  build contains its `bwrap … --ro-bind` line and a timestamp line for each host write it made, and the round
  names the sweep's result in its report.
  Shown able to fail: the incident itself — the shim sat outside every fixture directory, so no fingerprint
  covered it (`corpus/lessons/round-40.md:67-71`); a re-run of either neutralized module is an import-time
  `SystemExit`, not an attack; and on the round-41 control the token scan catches a hostile module by name
  (`sidechannel=1`) while the sandbox denies the write (`build_write=OSError`) and the marker set is empty
  after the run (`:34`).
  Limits: the token scan is textual, so a module that names no forbidden token while writing there is invisible
  — the sandbox, not the scan, is the guard; the receipt quotes the envelope and does not prove the flags, so a
  forged receipt passes and only a non-author re-run (Q10) prices it; `--ro-bind / /` says nothing about the
  network or pids (`--unshare-net`/`--unshare-pid` do, unverified by the receipt); `date +%T` is seat-supplied
  text and proves order, not authorship; the criterion cannot reach a write made before the sandbox exists,
  which is exactly the round-40 case (a build child in a pid namespace over a shared filesystem), and a vector
  the envelope does not name — a socket to a host daemon, a shared device — stays open; and it protects
  neighbours, not the claim: a shim scoped under the seat's own scratch is compliant and measured the same
  attack result (`corpus/lessons/round-40.md:73`), so a green attack receipt says nothing about the counter's
  soundness.
  Lesson: `corpus/lessons/round-40.md:64-75` §Conformance incident; routed item R2,
  `corpus/lessons/round-40-verifier-spotcheck.md:95-96`; controls `plans/round-41-claims.md` §C1 "Other
  controls". Supersedes: none; extends Q23's scratch clause (where the scratch lives) with how it runs and
  what the receipt must show.

## 3. Evidence table (every cited number and location, with its command)

| cited in | command | output |
|---|---|---|
| Q31 before-state: green with zero mutants | `grep -n 'PREDICATE' .ufo/waves/round-40/falsify/F40CritPlanNext.md`; `sed -n '24,34p' …F40CritPlanNext.md` | `32:PREDICATE C1 pass`; block at :29-33 = `BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=0 killed=0 survived=0 invalid=0 null_detected=0`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass`, `exit=0 … (receipt runA-vacuous.txt, 49.5 s)` |
| Q31 vacuity copy's shape | `cat .ufo/waves/round-40/falsify/F40CritPlanNext/counter-vacuous.patch` | hunk `@@ -572,5 +572,10 @@`: two comment lines + `MUTANTS = []` + `TOTAL = 0` added (four lines), `TOTAL` rewritten to 0 |
| Q31 before-state receipt | `grep -n 'MUTANTS\|PREDICATE\|exit=' .ufo/waves/round-40/falsify/F40CritPlanNext/runA-vacuous.txt` | `24:MUTANTS total=0 …`, `26:PREDICATE C1 pass` |
| Q31 D1 | `grep -n '### D1\|### D2' .ufo/waves/round-40/falsify/F40CritPlanNext.md` | `105:### D1 — the round-41 predicate is satisfiable with zero round-41 work [M] — X1`, `117:### D2 …` |
| Q31 binding | `grep -n 'TOTAL\|FLOORS\|MUTANTS-BY-TOOL\|len(MUTANTS) == TOTAL' plans/round41_c1_verify.py` | `123:TOTAL = 23`, `124:FLOORS = {"receipts": 13, "sources": 10}`, `631` MUTANTS-BY-TOOL print, `640-641` `floors_ok`, `642` `len(MUTANTS) == TOTAL and floors_ok` |
| Q31 row-vs-site limit | `grep -n 'src.count(old)\|per_tool.setdefault\|duplicate fixture id' plans/round41_c1_verify.py` | `547` duplicate *fixture* id refusal only, `585` per-row floor count, `589` `src.count(old) != 1` — no mutant-id uniqueness check |
| Q31 discriminating control | `cat .ufo/waves/round-41/claims/control-c1-no-mutants.patch` | `233a234` / `> MUTANTS = []  # CONTROL: the empty mutant list (F40CritPlanNext D1/D2)` — one added line, `TOTAL`/`FLOORS` untouched |
| Q31 control receipt | `grep -n 'BATTERY\|MUTANTS\|PREDICATE\|exit=' …/control-c1-no-mutants.txt` | `24:BATTERY fixtures=22 wrong=0 tampered=0 sidechannel=0`, `25:MUTANTS total=0 …`, `26:MUTANTS-BY-TOOL receipts=0/0 sources=0/0`, `29:PREDICATE C1 fail`, `30:exit=1` |
| Q31 no-battery control | `cat …/control-c1-nothing.txt` (tail) | `BATTERY fixtures=0 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=23 killed=0 survived=23 …`, `PREDICATE C1 fail`, `exit=1` |
| Q31 tool-edited control | `cat …/control-c1-tool-edited.txt` (head/tail) | `PINS total=2 mismatched=1 first=plans/tip_receipts.py`, 13 `MUTANT T01..T13 … invalid`, `PREDICATE C1 fail`, `exit=1` |
| Q31 dev-mode leg | `grep -n 'PREDICATE' …/control-c1-hostile.txt` | `32:PREDICATE C1 n/a (non-default battery or mutant subset)` |
| Q31 freeze digests | `cat …/claims/frozen-digests.txt` | `8835a94b0ad62dc1f58c861e2025b7c4bc8c0b936c202c64e01bc8b43f53eaa8  plans/round41_c1_verify.py` |
| Q31 ordering (control before battery) | `ls plans/battery41` | `No such file or directory` (2026-10-26, tip `fc79f2a`) |
| Q31 lesson file absent | `ls corpus/lessons/round-41.md` | `No such file or directory` |
| Q32 incident | `grep -n 'Conformance incident\|SHIM_DIR\|do not timestamp' corpus/lessons/round-40.md` | `64:## Conformance incident (wave 1)`, `67:… SHIM_DIR = /home/vgpnk/.local/bin — a shared host directory ahead of /usr/bin on every`, `69:… the seat's receipts do not timestamp the writes …` |
| Q32 routed item | `grep -n 'R2\*\* Host-safety' corpus/lessons/round-40-verifier-spotcheck.md` | `95:- **R2** Host-safety (D1): no seat may write outside the lane scope or scratch; keep the read-only ~/.local/bin sandbox for` |
| Q32 neutralization | `grep -n 'raise SystemExit\|SHIM_DIR =' .ufo/waves/round-40/build/R40CritC1Counter/{crit_git_shim,crit_ledger_selfread}.py` | `crit_git_shim.py:10:raise SystemExit("NEUTRALIZED …`, `:18:SHIM_DIR = pathlib.Path("/nonexistent/neutralized-shim-dir")`; `crit_ledger_selfread.py:9:raise SystemExit("NEUTRALIZED …` |
| Q32 live PATH state | `ls -l /home/vgpnk/.local/bin/git` | `ls: cannot access '/home/vgpnk/.local/bin/git': No such file or directory` |
| Q32 envelope | `grep -n '^PATH = \|ro-bind\|bwrap' plans/round41_c1_verify.py` | `56`/`60` isolation docstring, `116:PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"`, `318:argv = [BWRAP, "--ro-bind", "/", "/", …` |
| Q32 control | `grep -n 'SIDECHANNEL\|sidechannel=\|OSError\|markers after the run' …/control-c1-hostile.txt` | `2:SIDECHANNEL hostile/h_host_writes.py tokens=/home/`, `3:… build_write=OSError.lane_read=FileNotFoundError …`, `27:BATTERY fixtures=1 … sidechannel=1`, `34:markers after the run: ls: cannot access '/home/vgpnk/k41-hostile-*': No such file or directory` |
| Q32 hostile module docstring | `grep -n 'Targets are marker' …/claims/hostile/h_host_writes.py` | `2:Targets are marker files under the user's home, NOT a PATH directory, so a sandbox failure is harmless."""` |
| Q32 measured absence | `grep -c 'host-safety\|Host-safety' corpus/QUALITY.md`; `grep -c 'bwrap\|read-only-PATH' corpus/QUALITY.md` | `0` and `0` |
| numbering free | `grep -n 'Q31\|Q32\|^## Round41' corpus/QUALITY.md` | no matches |

## 4. Gates and verification

- **No gate was executed by this seat.** `plans/round41_c1_verify.py` was not run: wave 1 is in flight and its
  battery does not exist yet (`ls plans/battery41` → `No such file or directory`), so the green half of Q31's
  check is the executors' deliverable and is *not* claimed here. The draft says so in its own Check paragraph.
- The red halves are the frozen receipts at `8ef8b4fc` and were re-read, not re-run (`cat`/`grep` above).
- No jj/git mutation, no pacman, no service, no background job, no `systemd-run`.

## 5. Touched surfaces

| path | action |
|---|---|
| `.ufo/waves/round-41/build/R41QualityDraft.md` | created (this report) |
| `.ufo/waves/round-41/build/R41QualityDraft/quality-q31-q32.md` | created (paste block) |

Nothing else. `corpus/QUALITY.md`, `plans/*`, `SCORECARD.md`, `LOG.md`, `SKILL.md`, `PROVINCE.md` and the Git
index are untouched; the insertion point for the L1 is `corpus/QUALITY.md:569` (end of the Q30 block).

## 6. Findings / discernment notes

1. **The round-41 control is stronger than the round-40 falsifier's, and the difference is the point.** The
   falsifier's vacuity copy appended `MUTANTS = []` *and* `TOTAL = 0`, so `len(MUTANTS) == TOTAL` was
   trivially true and the green came from the missing floors. The round-41 control appends only
   `MUTANTS = []` (`control-c1-no-mutants.patch`, one line), leaving `TOTAL = 23` and `FLOORS` as frozen, so it
   reddens both the length leg and the per-tool floor leg — i.e. it prices the binding rather than a second
   edit. Q31 records that contrast because a future round copying the falsifier's shape would not have shown
   the fix works.
2. **Binding ≠ right denominator.** The floors are author-written literals; Q31's limits keep Q27's standing
   warning and name the free shape: 13 reachable mutants clear a 13 floor. Nothing here substitutes for a
   reviewer (Q10).
3. **The total counts rows, not behaviours.** `plans/round41_c1_verify.py:589` only requires each `old` to
   occur once in its tool; mutant ids are not uniqueness-checked (`:547` refuses duplicate *fixture* ids only),
   so two rows with the same replacement both count toward 23. Named as a limit, not repaired — the frozen
   counter is not this seat's to edit, and no rule required id uniqueness at freeze.
4. **Q32 protects neighbours, not the claim.** The lesson's own measurement is that the scoped shim produced the
   same attack result (`corpus/lessons/round-40.md:73`); the read-only PATH exists so a seat's attack cannot
   reach another lane, and a green attack receipt is not evidence of a counter's soundness. Q32 says this in
   its limits so it is not read as a quality criterion for the attack's argument.
5. **`corpus/lessons/round-41.md` does not exist yet.** The claims file points the mined mistake at that lesson
   (`plans/round-41-claims.md` §Frontier step). Q31's `Lesson:` line points at the falsify report that actually
   carries the measurement today, and says the pointer moves when the round writes the lesson — so an L1
   pasting Q31 now does not create a dangling citation.
6. **Q32's forward leg is a sweep, not a tool.** No `plans/` tool checks envelopes or timestamps
   (`grep -c 'host-safety' corpus/QUALITY.md` → 0; the counter carries the envelope in its docstring only), so
   the executable half is the two live probes plus a per-receipt `bwrap`/timestamp sweep the round reports. If
   the L1 wants it mechanised, the cheapest shape is a grep over the round's cited attack receipts, not a new
   frozen instrument — named here, not built (out of this seat's scope).

## 7. Out of scope (not done, by instruction)

- No edit to `corpus/QUALITY.md` or any lane file; no integration, commit, push or jj operation.
- No C1 counter run, no battery, no fixture build, no mutation (wave-1 executors' and the main agent's work).
- No re-run of any frozen receipt, and no re-derivation of round-40 numbers beyond the greps above.
- No tool installed or upgraded (nothing was needed; no pacman, no `uv tool`).

VERDICT: quality-criteria-drafted-2
