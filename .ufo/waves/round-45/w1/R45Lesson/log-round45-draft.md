# LOG.md draft — round-45 entry (paste at integration)

Shape copied from `LOG.md:1337-1372` (round 44): a `##` heading naming the measured claim, the L1/freeze/landing
line, then `- C1 (…)`, `- C2 (…)`, `- Closure …`, `- Mistakes mined: …`, `- Re-verification (freshness): …`,
`- Round shape: …`. `<<FILL: …>>` slots are the L1's; the C2 numbers below are the probe receipt's
(`corpus/evidence/round45/password-recovery-probe.txt`, sha256 `587c8b34…`), which this seat read, not ran.

```markdown
## Round 45 (hyaku run 9, 2026-10-26) — the advertised fixture fence calibrated to <<FILL: contradicted=0>>
contradictions; eleventh TB2 grader executed (exact line-membership of one constant)

L1 `KengakuR45` (planner seat). Freeze `b4fcd351` (claims; `plans/round45_c1_verify.py` with the ten hostile
modules of `plans/refusals45/` and the five freeze controls; `plans/round45_c2_verify.py`, the 16-case probe, the
spec, nine captures with `SHA256SUMS`, and the red controls nothing / r44-fence / admit-all / refuse-all /
static-only / c2-nothing / c2-predictor); post-freeze C2 spec re-pin `52d7486` (gitignore removed as a row; both
digests kept in `claims/frozen-digests.txt`); first recorded probe run `23:27:11-23:27:15 -03`; attempt-1 residue
discarded pre-freeze (`.ufo/waves/round-45/attempt1-unclaimed/`, `attempt1-unclaimed/README` absent). Lesson
`corpus/lessons/round-45.md`.

- C1 (calibration, `<<FILL: predicate met | not met>>`): freeze `contradicted=7` for the round-44 fence (f7/f8/f9
  LEAKED; f1/f4/f6/f10 READ outside `d`) and `contradicted=10` with no fence; landing `<<FILL: PINS total=33
  mismatched=0 / REFUSALS total=10 clean=10 … / HONEST fixtures=104 admitted=104 … / CALIBRATION advertised=10
  contradicted=0 / PREDICATE C1 pass>>`. The work is `plans/fixture_fence.py` (`breach(d, argv, tool)`), pure
  filesystem legs first (walk `d`, `.git` file-or-dir, symlinks, `commondir`, `config.worktree`,
  `[include]`/`[includeIf]`/`extensions.worktreeConfig` in any `.git/config*`, alternates, a `.git` above `d`),
  bounded git legs second; judged under `strace -f -y` in a read-only bwrap sandbox.
- C2 (coverage, `<<FILL: predicate met | not met>>`): TB2 `password-recovery` @ `2fd12b88`, S149–S156 (A); probe
  `cases=16 observed_pass=5 observed_fail=11 mismatches=0`, `regrade cases=16 differ=0`; V11 `states=48
  grader_pass=18 grader_fail=30 disagree=0` (`claims/control-c2-predictor.txt`). Observations: the whole score is
  two functions over `/app/recovered_passwords.txt` — `Path(...).exists()` (`test_outputs.py:8-10`) and whole-line
  membership of the embedded 23-character constant `8XDP5Q2RT9ZK7VB3BV4WW54` (`:18`) — with the
  `len(guesses) > 0` assert at `:16` unable to fire, line order/count/duplicates never read, CRLF accepted through
  `read_text()`'s universal-newline mode (`constant-crlf`, `crlf-line`), the `PASSWORD=` form refused
  (`password-eq`), decoys on the answer's line refused (`constant-joined`) and 1000 decoy lines accepted
  (`decoys-1000`). The constant is published by the task's own `README.md:31`, so the `constant` case passes
  without touching the disk image, and `allow_internet = true` (`task.toml:34`) keeps it fetchable; the fifth
  pass is the oracle (`oracle-solve-sh`, `solve.sh:51` relative output, landing at the graded path only because
  `Dockerfile:20` sets `WORKDIR /app`). Setup seeds a 4 MB image (`setup.sh:22`), splits at `offset+20`
  (`:29-30`), dd's the halves at 1 MB and 3 MB (`:36-37`). pytest is not run: the harness reproduces each test's
  verdict, the only thing `tests/test.sh:25-28` rewards.
- Closure `<<FILL: R1–Rn>>`.
- Mistakes mined: the round's C1 first drafted as a do-nothing battery45 copy (attempt 1; the standing-battery
  control already carries those five kills); a probe-docstring repair with the pre-repair text unrecoverable; a
  spec row admitted for `gitignore` (no graded predicate, caught by the Gate rule); a frozen instrument edited
  after the freeze with both digests kept; entry line citations off by one to twelve lines.
- Re-verification (freshness): nine captures re-fetched `cmp`-identical (`R45ScoutRefetch`; this seat 23:3x,
  `http=200` ×9), upstream drift 0 at the pin.
- Round shape: `<<FILL: seats, wave count>>`.
```

## Notes for the L1

- The C1 bullet's parenthetical is the claim; paste `predicate met` only when the counter's last printed line is
  `PREDICATE C1 pass`, exit 0, on a clean clone — the LOG's round-44 precedent records the before-state too, so
  keep `contradicted=7` visible.
- The C2 bullet uses `observed_pass=5 observed_fail=11` from the receipt on disk (this seat did not run the
  probe). If the L1's own run replaces the receipt, re-read those two numbers rather than reusing mine.
- `R45PkgProse` drafted a longer C2 block for the same slot (`w1/R45PkgProse/05-log-c2-block.md`); its numbers are
  placeholders and its line cites are correct (`README.md:31`, `task.toml:22`, `test.sh:25-28`, `Dockerfile:20`).
  Pick one form, not both.
