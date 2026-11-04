# U4RedBeforeR81 — R80-U4 red-before reproduction (round-81 w1, executor)

Seat `U4RedBeforeR81`, item U4: show M80-1's claimed failure actually failing (R81-C2 calibration
evidence). Measured lane tip `805a65c836f745703e5c1652d10ce8e55043265b` (clone HEAD); lane master at
re-check `60123c7f7bb8abd06c7d273a3f09c70889b81e25`. Axes: this seat serves calibration (R81-C2),
which the frozen claims hold at ceiling 10 and exercise via the six routed ids; nothing here touches
coverage (R81-C1).

## 1. What was run and what it returned

Setup: `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/clone`; clone top-level
verified equal to `$S/clone`, worktree clean. No fixture repo needed. Host: `/usr/bin/python3`,
`Python 3.14.8`; `python3 -c "import Bio"` → `ModuleNotFoundError`, rc 1; `openssl version` →
`OpenSSL 3.6.5 29 Sep 2026 (Library: OpenSSL 3.6.5 29 Sep 2026)`.

Claim source: `corpus/lessons/round-80.md` M80-1 ("remove the `prefix` from the table and the protein
leg dies with the same `ModuleNotFoundError`, which the gate reports as `REPRODUCTION-EXIT`");
neighbourhood `corpus/routed-findings.jsonl` R79-V1 row (round-79 claim context). Frozen entry
`plans/round80_probes.json` → `protein-assembly`: `tool=plans/tb2_grader_probe.py`,
`argv=["--lane","."]`, `prefix=["uv","run","--no-project","--with","biopython","python3"]`.

**Red run** (prefix removed; cwd = measured clone):

```
$ python3 plans/tb2_grader_probe.py --lane .
Traceback (most recent call last):
  File ".../clone/plans/tb2_grader_probe.py", line 168, in <module>
    sys.exit(main())
             ~~~~^^
  File ".../clone/plans/tb2_grader_probe.py", line 145, in main
    import Bio  # noqa: F401  (fail loudly if Biopython is absent)
    ^^^^^^^^^^
ModuleNotFoundError: No module named 'Bio'
```

exit code 1; stdout empty. The grader digest gate passed first (capture sha256
`44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582` equals the probe's pin), so the
failure is exactly the missing dependency at `tb2_grader_probe.py:145`.

**Green control** (same tree, prefix restored): `uv run --no-project --with biopython python3
plans/tb2_grader_probe.py --lane .` → exit code 0, 18 cases, `observed_pass=5 observed_fail=13
mismatches=0`, biopython=1.88, stderr empty.

**Gate mapping** — `plans/round80_c1_located_replay.py:191` builds
`cmd = (spec.get("prefix") or [python]) + [spec["tool"]] + render_argv(...)`; lines 322-323 do
`if rc != 0: add("REPRODUCTION-EXIT", f"rc={rc}")`. Direct call of the gate's `run_probe` with the
prefix removed returned `rc=1 stdout_len=0`. Full gate run in the clone with `prefix` deleted from
the table:

```
DEFECT REPRODUCTION-EXIT protein-assembly rc=1
DEFECTS n=2
TARGET members=6 located=6 reproduced=5 ledger_flipped=6 diverged=2 defects=2
PREDICATE R80-C1 fail
```

exit code 1. The second defect is `LEDGER-GATE-COUNTS executed=26 unlocated=0` — the clone is a
round-81 tree whose population ledger already holds 26 executed, while round-80's gate hardcodes 24;
it is unrelated to the prefix. The table was restored after the run (`git checkout --`; sha256 back to
`caa4333f...0f22`, clone clean).

**Verdict: the failure reproduces on this host.** Prefix removed → exit 1 + `ModuleNotFoundError: No
module named 'Bio'`; prefix restored → exit 0; the gate prints `DEFECT REPRODUCTION-EXIT
protein-assembly rc=1`. M80-1's claim is true as written.

## 2. Required report points

**(a) Does a committed selftest case cover `REPRODUCTION-EXIT`? No.** `plans/round80_c1_located_replay.py`
`CASES` (lines 535-555) has 19 cases; none induces a nonzero replay. `exit-nonzero` targets the
receipt's `EXIT` stamp (`EXIT-NONZERO`), not the replay's rc. The selftest fixture tool
(`FIXTURE_TOOL`, lines 386-391) only prints and always exits 0; no mutation alters it, and
`fixture_check` runs `check(..., reproduce=True, sys.executable, ...)`. The committed battery receipt
`corpus/evidence/round80/c1-selftest.txt` agrees: line 12 `CASE exit-nonzero expect=EXIT-NONZERO`,
line 20 `SELFTEST cases=19 red=15 failures=0`. `REPRODUCTION-EXIT` is therefore reachable only through
a real probe failure (as above), and the round-80 spot-check said so itself: "the C1 selftest has 19
cases, none for the interpreter prefix" (`corpus/lessons/round-80-verifier-spotcheck.md:182-183`).
The U4 repair took the red-before option, not the selftest-case option; the check family remains
unexercised by the committed battery.

**(b) Does a `QUALITY.md` criterion cite M80-1 today? Yes.** `master:corpus/QUALITY.md:1298-1302` Q58
names R80-U4, M80-1, the exact failure string, and the receipt path
`corpus/evidence/round81/r80-u4-red-before.txt`; QUALITY.md is clean in the worktree. The registered
check passes at tip: `python3 plans/round81_c2_checks.py u4` → `OK u4`, rc 0.

## 3. State of the C2 repair at measurement

`corpus/routed-findings.jsonl` already carries the R80-U4 row (`closed`, `close` naming
`corpus/evidence/round81/r80-u4-red-before.txt` + QUALITY Q58, `check` =
`python3 plans/round81_c2_checks.py u4`, `evidence_literal` = `ModuleNotFoundError: No module named 'Bio'`),
and the evidence file is committed at master (added in `4ac8471b`, sha256
`dc733e63ace0947ceeca643cca352b1ffe62f1d3bafab81ef04e68ac26952114`). My independently measured
witness (clone at `805a65c`, tool bytes identical to master `60123c7f`) agrees with it: same exit 1,
same traceback sites (lines 145/168), same module error. The committed receipt states the run was made
in the lane worktree with `/usr/bin/python3`; mine was made in a `git clone --shared` at the measured
tip — same interpreter (`/usr/bin/python3`, 3.14.8) and same bytes.

## 4. Deliverable

`.ufo/waves/round-81/w1/r80-u4-red-before.txt` — first line carries `R80-U4`; contains the command,
`exit code: 1`, the verbatim stderr, the green control and the gate's `DEFECT REPRODUCTION-EXIT`
line. It also carries every token `plans/round81_c2_checks.py u4` requires (`R80-U4`,
`ModuleNotFoundError: No module named 'Bio'`, `exit code: 1`, `uv run --no-project --with biopython`),
so the L1 can copy it to `corpus/evidence/round81/r80-u4-red-before.txt` unchanged if a re-mint is
wanted.

## 5. Files, tools, risks

- Files written: the deliverable above and this report only; scratch `$S` removed (trap).
- No tool installs, no pacman transactions, no subagent dispatch, no lane writes/mutations.
- Observation (not a defect in the claim): `plans/tb2_grader_probe.py`'s docstring prescribes
  `--with biopython==1.85`, while the frozen table prefix is unpinned `--with biopython`; the green
  run resolved biopython 1.88. The probe's hard pin is the grader digest, not biopython, so the
  red-before is unaffected, but the table and the docstring name different environments.
- Residual gap for the L1: `REPRODUCTION-EXIT` has no committed selftest case (see §2a); if the round
  wants that check family exercised, it needs a fixture whose probe exits nonzero — not produced here
  (out of this seat's write scope).
