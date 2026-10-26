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
