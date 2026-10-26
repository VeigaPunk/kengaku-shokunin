# R43ErrataFibsqrt — appended errata block for `tb2-circuit-fibsqrt-grader.md` (round-43 closure R1)

Seat: `R43ErrataFibsqrt` (scribe, leaf). kengaku round 43, wave 1, 2026-10-26. Task: closure R1 of
`corpus/lessons/round-42-verifier-spotcheck.md:121-124` (D4) — draft an append-only `## Errata (round 43)` section
for `corpus/knowledge/tb2-circuit-fibsqrt-grader.md` correcting every wrong or overclaiming sentence named by
`.ufo/waves/round-42/falsify/F42EntryQuotes.md` §4 (4) and `F42CritOverclaim.md` §4 (the lesson pointer), re-derive
each correction from the captures and the receipt, list any further wrong sentence found, and draft the matching
correction line for `corpus/lessons/round-42.md`. **Nothing was edited in place; the block below is for the L1.**

## 0. Provenance and instruments

| Surface | Digest / state | Check |
|---|---|---|
| `corpus/knowledge/tb2-circuit-fibsqrt-grader.md` (449 lines) | sha256 `b692435aa5aa8c1659a7e14884fe809d73ae738b15f85f77e081a5c8919da0f8` | `sha256sum` this seat; equals the digest `F42EntryQuotes` audited, so no sentence moved since round 42 |
| `corpus/evidence/round42/fibsqrt-probe.txt` (24 lines) | sha256 `2a54ca8a76619a173280727938441fcf129ddcd482cc0a4d55f65b38d41ad92a` | `sha256sum`; equals `F42EntryQuotes`' digest |
| `corpus/evidence/round42/tb2-circuit-fibsqrt/` (9 captures) | — | `sha256sum -c SHA256SUMS` → 9× `OK` this seat |
| `plans/fibsqrt_probe.py` (366 lines) | read-only | imported in-kernel (`len(L28)=1195`, `len(GRADED)=28`, `max(GRADED)=48401`) |
| host instruments | `gcc (GCC) 16.2.1 20260810`, `Python 3.14.8` | `gcc --version`, `python3 --version` |

Envelope: this seat ran **no battery, counter, probe or fixture build** — no bwrap-sandboxed run whose writes could
reach a PATH directory. The one measurement that compiled and ran code (E6) was bracketed by the round-43 envelope
anyway:

```
ENVELOPE start 19:13:24 cwd=/home/vgpnk/Projects/shokunin/kengaku-shokunin
gcc_rc=0
case=x gates=out0 = 1|out40 = out1 + out2| stdout=[0] rc=0
case=w gates=out0 = 1|out40 = out1 &| stdout=[0] rc=0
case=y gates=out0 = 1|out40 = 1| stdout=[2147483648] rc=0
case=z gates=out0 = 1| stdout=[] rc=0
700645ac6156cdc88ec1e210f7c7d8d9969bb42aec969c410597e8efca796173  sim.c
ENVELOPE end 19:13:26 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Full receipt: `.ufo/waves/round-43/build/R43ErrataFibsqrt/sim_unmatched_op.txt`. The compiled `sim.c` is the capture
(`700645ac…`, equal to `SHA256SUMS` and receipt line 4), compiled `-O3` as `test_outputs.py:66` does.

The entry's 24-row quote table was re-checked by this seat against the captures (regex parse of `:125-148`, substring
test of each quote on its cited `capture:line`, word count in [3,25]):

```
rows_ok 24 rows_bad 0
```

## 1. The block to append (verbatim, entry end after `:449`)

```markdown
## Errata (round 43, closure R1; appended 2026-10-26, nothing above edited)

Seven items. E1–E4 correct the four sentences `F42EntryQuotes` §4 found wrong or overclaiming; E5–E6 were found
re-deriving them; E7 is a locator `F42EntryQuotes` recorded as a nit outside its count. Each quotes the sentence with
its line, then the correction and the evidence line.

- **E1 `:296-298` (finding 7) — the `2^15` sentence.** Quote: "The table's maximum, 48401 = 220²+1, is the only reach
  above 2^15". **Wrong: six of the 28 graded inputs are above 2^15 = 32768**, all from the two largest roots —
  220²−1 = 48399 (`test_outputs.py:94`), 220² = 48400 (`:88`), 220²+1 = 48401 (`:100`), 209²−1 = 43680 (`:95`),
  209² = 43681 (`:89`), 209²+1 = 43682 (`:101`); the next-largest input is 107²+1 = 11450 (`:99`). Correction: "The
  table's largest input is 48401 = 220²+1, and six of its 28 inputs lie above 2^15 (220²−1, 220², 220²+1 and 209²−1,
  209², 209²+1); nothing grades an input outside the list." The summary sentence at `:17` and the rest of finding 7 (dropping 48401 or
  flipping one bit of one answer is `PPF` — only the value test fails, receipt lines 12 and 14) stand.

- **E2 `:309-312` (finding 10) — stdin scope and locator.** Quote: "the probe runs every case with stdin on
  `/dev/null` (probe docstring — the oracle case's own `solve.sh` recipe included)". **Wrong twice.** The probe pins
  `stdin=subprocess.DEVNULL` for the case *recipe only* (`plans/fibsqrt_probe.py:201`); each case's harness is launched
  with no `stdin=` (`fibsqrt_probe.py:266-267`), so the graded `/app/sim` calls — `subprocess.run(["/app/sim", …])` with
  no `stdin=` (`test_outputs.py:119`) — inherit the harness's stdin, i.e. the probe caller's. The probe docstring makes
  no `/dev/null` statement at all; its only stdin sentence is that `sim.c` "sets signals 0-31 from argv[1] (not stdin)"
  (`fibsqrt_probe.py:27-28`). Correction: "`sim.c:324` takes the value from `argv[1]` and no line of `sim.c` reads stdin
  (its only stream read is `fgets` over the gate file, `:108`); the probe pins the case recipe's stdin to `/dev/null`
  (`fibsqrt_probe.py:201`) and leaves the graded `/app/sim` calls on the caller's stdin (`:266-267`,
  `test_outputs.py:119`)." The finding's conclusion — the graded channel is argv, shown by `oracle-solve-sh` `PPP` —
  stands, on `sim.c`'s code, not on this sentence.

- **E3 `:430-432` (integration, D2 bullet) — the padded rows' verdicts.** Quote: "end in 32 blank lines, so they too
  pass only because the print window is the 32 highest-indexed signals". **Overclaim.** Only the *value* test passes
  for that reason: `lookup-28-padded-31999` is `PPP` (receipt line 15) but `lookup-28-padded-32000` is observed `fail`,
  `PFP` (receipt line 16), because `test_outputs.py:21-23` counts the blank lines and the file is exactly 32000.
  Correction: "…so their value test passes only because the print window is the 32 highest-indexed signals
  (`sim.c:340-347`); `lookup-28-padded-32000` is observed `fail` (`PFP`) on the size test, `lookup-28-padded-31999`
  `PPP`." The tag argument (both would carry `last-32-lines` and `line-form`) is unaffected.

- **E4 `:433-434` — the labels under that counterfactual.** Quote: "Neither changes a requirement-map label
  (`last-32-lines` and `line-form` stay `unenforced`)". **Wrong under the bullet's own counterfactual.** Tag both
  padded rows and `padded-32000` (observed `fail`) joins `lookup-28-comment-lines` (`P`, receipt line 17) in the
  `line-form` set and `lookup-28-reversed-lines` (`P`, line 18) in the `last-32-lines` set; by the V7 rule at
  `:152-154` each label then becomes `partly`, not `unenforced`. Correction: "the two labels are `unenforced` only
  because the frozen receipt does not tag the padded rows; under this bullet's counterfactual both become `partly`."
  The frozen tags and the V7 labels as computed stay as they are.

- **E5 `:430-431` — the count of blank lines.** Quote: "end in 32 blank lines". **Wrong count.** The builder appends
  `[""] * (31999 - len(L28))` and `[""] * (32000 - len(L28))` (`plans/fibsqrt_probe.py:177-181`) with `len(L28) = 1195`
  (measured by importing the frozen builder), so the files end in **30804** and **30805** blank lines — as finding 3
  itself says at `:261` ("31999 lines of which 30804 are empty"). Correction: "end in 30804 / 30805 blank lines, so the
  file's last 32 lines are blank". The `last-32-lines` argument needs only the last 32; its conclusion stands.

- **E6 `:96`, `:144` (and the wording at `:40`) — "dropped" for an operator outside `&|^`.** Quotes: "parsed by
  `sscanf(op, "out%d %c out%d", …)` and dropped if that fails" (`:96`); "binary gates are parsed by sscanf and
  silently dropped when it fails" (`:144`). **Wrong.** Nothing is dropped: `Gate gates[MAX_SIGNALS]` is zero-initialised
  at file scope (`sim.c:24`; `OP_CONST_0` is 0, `:9`), `num_signals` was already raised at `:117-118`, and the missing
  final `else` leaves the type at `OP_CONST_0`, so the line stays a constant-0 gate and drives its signal to 0.
  Measured on the captured `sim.c` (`gcc -O3`, digest `700645ac…`, round-43 envelope): `out0 = 1` + `out40 = out1 + out2`
  → `0`; `out40 = out1 &` (binary `sscanf` returns 2) → `0`; `out40 = 1` → `2147483648` (index 40 is bit 31);
  `out0 = 1` alone → no output (so `num_signals` really moved to 41). The entry already says this at `:275-276` and in
  the wave-1 note at `:428`; only these three places keep the old wording. Correction: "binary gates are parsed by
  `sscanf(op, "out%d %c out%d", …) == 3`; the `&`/`|`/`^` switch has no default, so an unhandled operator leaves the
  gate a zero-initialised `OP_CONST_0` that drives 0 — not skipped, not an error."

- **E7 `:305-306` (finding 9) — the existence locators.** Quote: "assert existence on the absolute path
  `/app/gates.txt` (`:9`, `:16`, `:18`)". **Locator wrong, claim right.** `:9` and `:16` are the
  `gate_path = Path("/app/gates.txt")` assignments; the asserts are `:11` (test 1) and `:18` (test 2). Correction:
  "`test_outputs.py:11` and `:18`". (Recorded as a nit by `F42EntryQuotes` §4, outside its count of four.)
```

## 2. Lesson-correction line for `corpus/lessons/round-42.md` (append; do not edit `:57`)

```markdown
## Errata (round 43, closure R1)

- **`:57` pointer corrected — `fibsqrt-probe.txt:6` → `:11`.** `:57` cites "receipt `fibsqrt-probe.txt:6`" for the
  `lookup-28` row; line 6 of that receipt is the `# capture test_outputs.py sha256=6117b8ed…` header, and the
  `lookup-28` CASE row is **line 11** (`CASE lookup-28 predicted=pass observed=pass tests=PPP … violates=example-208,
  example-20000`). The sentence's content stands: `lookup-28` prints 0 for 208 and 20000 and still passes 3/3. Found by
  `F42CritOverclaim` §4 ("Wrong (1, minor)"); re-read at the receipt by this seat. Nothing deleted.
```

## 3. Findings ledger

| # | Entry anchor | Class | Named by | Verdict this seat |
|---|---|---|---|---|
| E1 | `:296-298` | wrong fact | `F42EntryQuotes` §4 #1 | confirmed; six inputs above 2^15, derivation in §1 |
| E2 | `:309-312` | wrong fact + wrong locator | `F42EntryQuotes` §4 #2 | confirmed at `fibsqrt_probe.py:201`, `:266-267`, `test_outputs.py:119` |
| E3 | `:430-432` | overclaim | `F42EntryQuotes` §4 #3 | confirmed at receipt line 16 (`PFP`) |
| E4 | `:433-434` | wrong under its own counterfactual | `F42EntryQuotes` §4 #4 | confirmed against receipt lines 15-18 and the V7 rule `:152-154` |
| E5 | `:430-431` | wrong count (new) | this seat | confirmed: 30804 / 30805 blank lines (`fibsqrt_probe.py:177-181`, `len(L28)=1195`) |
| E6 | `:96`, `:144`, `:40` | wrong mechanism (new) | this seat | confirmed by measurement (envelope receipt above); contradicted by `:275-276` and `:428` |
| E7 | `:305-306` | wrong locator (relisted) | `F42EntryQuotes` §4 nit | confirmed at `test_outputs.py:9,11,16,18` |
| — | `round-42.md:57` | wrong pointer | `F42CritOverclaim` §4 | confirmed: receipt line 11, not 6 |

Checked and **not** defective (so no errata item): the summary's "largest graded input is 48401" (`:17`), the 28-value
list and its maximum (`:93`, `:244`), the 1195-line decomposition (`:245`), the two-padded-rows verdict letters in the
case table (`:230-231`), the `IsADirectoryError` locators (`:300-302`, `:20`), the `int("")` locator (`:254`, `:127`,
`:128-131`), the requirement-map label counts (`:156-158`, 15/14/14), the quote table (`:125-148`, re-read against the
captures line by line), and finding 5's zero-init mechanism (`:273-277`).

## 4. Why these are errata and not edits

- Each item quotes the offending sentence with its line and states the replacement; no line above `:449` changes.
  E1–E4 were already routed by `round-42-verifier-spotcheck.md` §5 R1; E5–E7 are additive and cite their own evidence.
- E4 is deliberately bounded: the frozen `violates=` tags are not edited (they are part of the freeze), and the entry's
  present labels are correct *for the frozen table*; only the counterfactual sentence is wrong.
- E6 does not change any verdict: the receipt's 7 pass / 9 fail were produced by the grader, and the corrected
  mechanism is the one finding 5 was written with. It is a prose defect in three places, as `R42CritProbe` D1 called it.
- E5 likewise changes no verdict; it repairs a number the entry itself contradicts at `:261`.

## 5. What this seat did not do (limits)

- Did not edit the entry, the lesson, or any lane file; no `git`/`jj` command ran in the lane; no clone was made.
- Did not re-run `plans/fibsqrt_probe.py` or re-grade the 16 cases: the receipt is taken as frozen (digest verified
  above; `F42EntryQuotes` §5 also did not re-run it). The landing re-run's byte-equality is read, not re-run, at
  `.ufo/waves/round-42/integrate/measure-final.txt:874` (`fibsqrt_probe exit=0 byte_equal=yes`); the round-42 claims
  file does not itself state it.
- Did not fetch the pin URLs: the captures are verified by `SHA256SUMS`; remote identity rests on `F42CritOverclaim`
  §1's live re-read, not this seat.
- E6's measurement uses host `gcc 16.2.1` on the captured `sim.c`; the mechanism is C static-storage initialisation,
  not compiler behaviour, but the *printed* values are host-gcc values (the image's `-O3` remains untested, as the
  entry already says at `:348-351`).
- `len(L28) = 1195` was measured by importing the frozen builder read-only; the builder's own construction was not
  re-derived line by line here (that is `F42EntryQuotes` §4's independent recompute).
- No tool was installed, no package manager ran, nothing was written outside `.ufo/waves/round-43/build/R43ErrataFibsqrt/`
  and the scratch dir; scratch deleted with `plans/scratch_guard.py safe-rm`.

VERDICT: errata-drafted-7-new-found-2
