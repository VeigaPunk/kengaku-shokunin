# ClaimFalsify — R68 wave 1 falsification seat (C1 counter + kill rules + C2 gate)

Scratch: `/fast/scratch/hyaku/kengaku-r68/ClaimFalsify` (forgeries under `forge/`, deleted on exit).
Method: `python3 plans/round68_c1_pypi_finish.py --check-receipt <forged>` run from the lane root;
the checker resolves all sha bindings against committed lane bytes via `__file__`, so scratch-resident
receipts are still scored against the real evidence. Baseline: the receipt of record scores
`PREDICATE R68-C1 pass`, rc=0.

## 1. Receipt forgeries (spec'd f1–f5, adversarial f6–f8)

```
FALSIFY f1 refused=True  defect=CHECK defect probe-sha (none) != 4a6fae5328e1cacd3b667fb59f50622d1602574a5763f741bda7dc0293b3fdfc   (+12 more: base-probe-sha, all four stderr-sha binds, server-log-sha/flags, k2-clause-line, class-line, exit-agreement, stored-predicate (missing) != derived)
FALSIFY f2 refused=True  defect=CHECK defect K2-observed P != F
FALSIFY f3 refused=True  defect=CHECK defect k2-stderr-sha receipt 268c02efc4bcdefb1d142a0f3e218eccf6429eaefea2f767a6dd664a90ffecb3 != committed dedbc20d70cc292e39eec807222312473313ee274e3a8db8476e3e0d8565375d
FALSIFY f4 refused=True  defect=CHECK defect server-log-sha receipt 268c02efc4bcdefb1d142a0f3e218eccf6429eaefea2f767a6dd664a90ffecb3 != committed 574c3a2f7594d05d45ab06526baa61fc36bcc3ee60ec04cc6716e88f1c47af28
FALSIFY f5 refused=True  defect=CHECK defect class-line CLASS network-service executed=2 absent
FALSIFY f6 refused=False defect=(none printed) — K2 `exception=CalledProcessError`→`exception=none` PASSES: exception= is an unbound field
FALSIFY f7 refused=False defect=(none printed) — index_pid=999999 + wheel_sha256=64×'f' PASSES: pid/wheel are format-only checks
FALSIFY f8 refused=False defect=(none printed) — `PREDICTION-VECTOR P/P/P/P derived=P/F/F/F` PASSES: only the derived= half is enforced
```

Every refused forgery also correctly trips `exit-agreement` and `stored-predicate` (the stored
`pass`/`CLASS-PROBE-EXIT=0` disagree with the derived `fail`) — the receipt cannot lie about its own
verdict. f1 (the real round-63 receipt of record) is refused on 13 defects; it lacks every new
binding, exactly as the frozen control predicted.

**Surviving-forgery analysis.** No forged receipt can fabricate a pass without the committed
evidence bytes: every sha named is re-hashed from committed files, the K2 clause is re-checked inside
the committed capture, and the derived vector is recomputed from the byte-verified base probe.
BUT three fields in the frozen receipt *format* are unbound, so a receipt that differs from the
receipt of record only in them still prints `PREDICATE R68-C1 pass`:

- `exception=` on every CASE line — unchecked. The frozen format records real exceptions
  (CalledProcessError, AssertionError); a receipt claiming K2 failed with `exception=none` passes.
- `index_pid`/`wheel_sha256` on K2–K4 fully unbound; K1's are format-checked only (non-none pid,
  64-hex wheel). Neither is cross-referenced to `battery-run.txt` or any committed wheel — this is
  inside disclosed limitation (i) (provenance), but it means the checker proves
  "a receipt consistent with committed bytes", not "this byte-exact receipt of record".
- The declared half of `PREDICTION-VECTOR <declared> derived=<derived>` — only `derived=` is
  enforced.

Smallest safe correction (report only): bound `exception=` and the declared vector in a future
re-freeze, or mark the unbound fields explicitly informational in the format comment. Not a kill of
R68-C1 — the frozen predicate names none of these fields — but the frozen receipt format implies a
stricter binding than the checker implements.

## 2. Kill rules (a)–(e): room to narrow the predicate after data?

Class checked: the round-63 A1 lesson (detector widened after the miss). The meta-rule does the
work — "a rule changed after any seat has scored is not this claim's rule; any later amendment is a
new dated section, never an edit" — so a seat or the L1 cannot repair a miss inside this claim;

- **(a) frozen vector vs receipt** → closed. Vector is byte-compared; a post-data change is an
  amendment = new claim. No narrowing room.
- **(b) checker exit ≠ 0 for non-(a) reason** → closed. Declares the counter wrong, claim not
  admitted; fixing the checker produces a different instrument under a new claim.
- **(c) hang > 900 s → exit 2, could-not-evaluate** → **MISSTATED, unimplementable as written.**
  `LEG_TIMEOUT = 900` in the finish probe is dead code (grep: defined line 37, referenced nowhere);
  every leg and the K2 pip run use the base probe's `LEG_TIMEOUT = 180`. And a timeout returns
  `(observed="F", exception="TimeoutExpired")` — i.e. a normal F leg, rc 1 on vector mismatch at
  best, never exit 2. Sharper: `exception=` is unbound (f6), so a timeout on an *expected-F* case
  (K2/K3/K4) is indistinguishable from a clean failure and would have PASSED silently — a hung leg
  on the quiet window would be scored a success. Rule (c)'s promised semantics do not exist.
  Smallest safe correction: reword the rule to the instrument's real behavior (leg timeout =
  `exception=TimeoutExpired`, scored F; expected-F hangs are undetectable → limitation) and/or bind
  `exception=` so a TimeoutExpired on an expected-F leg is at least visible in the scored receipt.
- **(d) K2 returns P** → closed. observed=P on the quiet window mismatches F by (a); the battery's
  own pip-succeeds SetupError also refuses to emit a pass receipt. No narrowing room.
- **(e) foreign service on 8080** → closed. `require_port_free` guards every case window and a K2
  pip success raises SetupError; the predicate fails, not the claim gets reinterpreted.

Rule-gap verdict: (a),(b),(d),(e) leave no room for post-data narrowing; the A1 class is excluded by
the claims doc's own amendment rule. (c) is the defect — it describes mechanics the instrument never
implements, and its undetectable-hang corner is a real (if unexercised this round) gap.

## 3. R68-C2: is the red-before genuine?

**Yes, with one concurrency caveat.** The peer-captured red-before
(`.ufo/waves/round-68/w1/gate/red-before.txt`) shows `DEFECTS n=5, PREDICATE R68-C2 fail, rc=1`,
and all five defect reasons are ABSENCE reasons, not crashes:
`E1 "## Erratum (round 68) section absent"`, `E2/E5 "no erratum section"`,
`E3 "r67-probe-selftest.txt missing (probe re-hash ok)"`, `E4 "pipeline-row=False, sqlite-row-strict=False"`.
The gate cannot pass the pre-landing tree: it only sees a landed erratum, a committed tally, and the
registry rows — none were present. My independent re-run now shows `DEFECTS n=4`: peer
SelftestTally's `corpus/evidence/round68/r67-probe-selftest.txt` (dated 2026-11-03T23:00:47Z)
landed mid-wave and E3 flipped green (also captured by GateRedRun's `red-after-concurrent-tally.txt`).
This is the gate truthfully tracking live state, not a false green — but it proves the green receipt
`corpus/evidence/round68/c2-green.txt` MUST be captured only after the L1 finishes all landings;
a mid-landing run yields partial counts.

`--selftest` (own run, scratch): 5/5 defects on the by-construction fake lane,
`SELFTEST defects-in-fake=5 want=5 all-fail=True`, rc=0 — no check is vacuous; it stays valid
post-landing because it strips corrections from a copied tree.

Under-bindings in the gate (corroborated by GateRedRun's `clause-fixtures.txt`, not re-run here):
E1's frozen text requires "exactly one `## Erratum (round 68)` heading" but `erratum_section` reads
the FIRST only — a second stray heading is invisible (dup-heading fixture passes); E3's checks are
substring-in-file, not line-anchored — `XPROBE sha256=…`, `NOTSELFTEST`, any `rc=` satisfy them
(loose-tally fixture passes); E4 accepts the probe name anywhere in the registry section and reads
only the first sqlite row line. Same class as C1's f6–f8: format implies more than the gate binds.
Smallest safe correction: heading-count == 1 and line-anchored (regex `^PROBE sha256=`, `^SELFTEST`)
checks in a future gate revision — report only, no edit.

## 4. Verdict

- **R68-C1 counter: stands.** f1–f5 refused for the exact predicted reasons; no forged receipt can
  fabricate a pass without the committed evidence bytes. Non-fatal under-bindings survive in
  unbound format fields (`exception=`, pids/wheels, declared-vector half) — inside disclosed
  limitation (i) but worth a dated note.
- **Kill rules:** (a),(b),(d),(e) airtight against post-data narrowing. **(c) is misstated** — the
  900 s bound is dead code, the real bound is 180 s, and a leg timeout scores as F (exit-2
  could-not-evaluate does not exist; an expected-F hang would pass silently). Reported, not edited.
- **R68-C2 gate: red-before genuine** (n=5, all absence reasons, captured pre-landing); gate
  non-vacuous (selftest 5/5); cannot pass pre-landing; green receipt must wait for the L1's full
  landing; heading-uniqueness and line-anchoring under-bindings noted (GateRedRun fixtures agree).
