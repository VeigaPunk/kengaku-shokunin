# C1GateReplayR74 — R74-C1 frozen gate replay (independent verification)

Seat role: executor, leaf. Independently re-ran the frozen decoupled registry gate for R74-C1
without trusting the L1 receipt. Lane tip at verification: `74e2e15a` (post Amendment A1);
working tree also carries the in-flight uncommitted SKILL.md amendment adding the
`round74-c1`/`round74-c2` registry rows and the `coverage_census.py` advertising sentence
(+3/-1, characterized via `git diff` — not authored by this seat).

## (a) Frozen counting command at the lane tip

Command: `python3 plans/round74_c1_registry.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin`

Raw output (byte-identical to committed receipt `corpus/evidence/round74/c1-after.txt`):

```
UNIVERSE mode=decoupled files=136 plans_seen=90 self_advertising_prevented=True
ADVERTISED total=116
REGISTERED total=116 rows=116
MISSING 0
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 0
DUPLICATE 0
PREDICATE R52-C2 pass
PREDICATE R74-C1 pass
rc=0
```

Every frozen target line for R74-C1 is present and exact: `UNIVERSE mode=decoupled`,
`ADVERTISED total=116`, `REGISTERED total=116 rows=116`, `MISSING 0`, `INCOMPLETE 0`,
`ENTRY-MISSING 0`, `SELFTEST-UNBACKED 0`, `DUPLICATE 0`, `PREDICATE R74-C1 pass`, rc 0.
(The extra `PREDICATE R52-C2 pass` line also appears in the committed receipt; not a divergence.)

## (b) Selftest

Command: `python3 plans/round74_c1_registry.py --selftest`

```
SELFTEST ok clean-decoupled
SELFTEST ok decoupled-missing
SELFTEST ok anti-circular
SELFTEST ok legacy-control
SELFTEST cases=4 failures=0
rc=0
```

Matches frozen sentence `SELFTEST cases=4 failures=0`; byte-identical to committed receipt
`corpus/evidence/round74/c1-selftest.txt`.

## (c) Legacy control

Command: `python3 plans/round74_c1_registry.py --universe legacy --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin`

```
UNIVERSE mode=legacy files=78 plans_seen=0 plans_only=0
ADVERTISED total=115
REGISTERED total=115 rows=116
MISSING 0
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 0
DUPLICATE 0
PREDICATE R52-C2 pass
PREDICATE R74-C1 fail
rc=1
```

Exit code 1 as required by the frozen control (legacy can never satisfy `PREDICATE R74-C1`:
it never sees `plans/*.md` instruments and its self-advertising masks dropped unreferenced
rows). Output is byte-identical to the committed receipt `corpus/evidence/round74/c1-before.txt`.

### Discrepancy note (resolved by Amendment A1)

The seat item text and the original claims-doc "Before"/"Control" prose quoted
`ADVERTISED total=110`, `MISSING 5`. Measured live — and against every committed tree state
tested in a scratch clone (`b7910802` freeze base: files=77, ADVERTISED 113, MISSING 0, rc 1;
`f4d651c5` freeze commit: files=78, ADVERTISED 113, MISSING 0, rc 1) — no state reproduces
110/5. The committed receipt itself records 115/0. Amendment A1 (landed at `74e2e15a` before
any seat returned, explicitly superseding the 110/5 prose with the receipt-backed 115/0)
resolves this; predicate, counting command, after-target, control and kill rule are unchanged.
This seat's legacy measurement confirms A1's stated numbers exactly.

## Cross-checks performed

- `git diff f4d651c5 cea7ebf3` (pre-A1): only `.ufo/waves/round-74/w1.ready`; the ADVERTISED
  113→115 delta between the clean freeze commit and the live tree is fully explained by the
  uncommitted SKILL.md registry-row amendment in the working tree.
- Decoupled control semantics (decoupled raises `MISSING 1` on a dropped row where legacy
  stays green) are covered by the passing `decoupled-missing` and `legacy-control` selftest
  arms; not independently re-fixtured (leaf seat, no labrat needed — selftest arms exercise
  both fixtures in isolated temp trees).
- Receipts `c1-after.txt`, `c1-before.txt`, `c1-selftest.txt` in
  `corpus/evidence/round74/` each match the corresponding live output byte-for-byte.

## Verdict

R74-C1 frozen predicate holds independently at the lane tip: all nine required decoupled
lines exact, selftest 4/4, legacy control exits 1 consistent with the committed receipt and
Amendment A1. No kill-rule trigger. Scratch cleaned (`/fast/scratch/hyaku/kengaku-r74/C1GateReplayR74`
removed). Lane repo untouched (read-only; clone used for historical state checks, then deleted).
