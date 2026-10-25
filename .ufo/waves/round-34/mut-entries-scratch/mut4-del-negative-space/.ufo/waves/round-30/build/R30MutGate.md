# R30MutGate — mutation test of the adoption gate's quote validator

Seat: `L1Kengaku30.R30MutGate` (leaf). Claim under test: **C3** — `plans/sources_adopt.py`
refuses a 26-word quote (exit 6) and a quote absent from the artifact (exit 7), proven by
`--selftest` cases 11–14.

## 1. Target bytes

| role | path | sha256 | bytes |
|---|---|---|---|
| pre-change body (lane, read-only) | `plans/sources_adopt.py` | `6fe6e762ab0c61da4ddbf029a2aa1a38cb64732ebd1ccbee4773c5eadcf7ead2` | 20424 |
| patched validator, first copy seen 04:24 | `/tmp/r30-GateQuote/sources_adopt.py` | `93ee7f7c417d3b2fc1e2268e5bb3cc9cf98a30abe9c7e52e8eb15abfdde4368f` | 33030 |
| **patched validator, live at time of verdict** | `/tmp/r30-GateQuote/sources_adopt.py` | **`f26ed9bb94086e9e9a7c3d7812608870e3fd1de441d5fe10fcff380f7b14609d`** | 33956, 791 ln |
| same bytes, integrated into the lane at 04:29:03 | `plans/sources_adopt.py` | `f26ed9bb9…` (byte-identical to the line above, `diff -q`) | 33956 |

The sibling (`R30GateQuote`) revised the file mid-run: `93ee7f7c → f26ed9bb` adds a `found`
channel and receipt wording, and leaves **all four mutation sites and all four killer
assertions byte-identical** (`diff -u` in §7). Mutants were applied twice, to both revisions;
the verdicts below are on `f26ed9bb`, which was stable through the final run. Copies:
`/tmp/r30-R30MutGate/patched.py` (v1), `patched2.py` (v2, hash-equal to the live file).

Because the patched file did not exist when this seat started, I first built a **reference
stand-in** (`reference.py`, `3c253a38…`, baseline body + the spec's named interface: exit 6
over-long / exit 7 absent, four cases, `SELFTEST cases=14`). It is mine, not the sibling's; its
verdicts are reported separately as corroboration, never as the patch's.

## 2. Detector

`python3 <file> --selftest`, tally line `SELFTEST cases=N failed=M`, exit code. Baseline check
first: the pristine pre-change body scores `SELFTEST cases=10 failed=0`, exit 0 — the detector
is green on its own baseline, so a mutant's `failed=0` is a real survivor, not a broken harness.
Each mutant is additionally probed at the **CLI**, because a suite can pass while the tool lies:

```
art.txt   = 32-word sentence, CRLF-terminated, so the 26-word quote is present in the bytes
pq_long   = row whose anchor cell quotes words 1..26   (26 words, IS in the artifact)
pq_absent = row whose anchor cell quotes words 1..20 + " zzznotintheartifact"
            (21 words; its first 20 characters ARE in the artifact, the whole quote is not)
pq_one    = row whose anchor cell quotes "zzznotinartifact"  (1 word, nowhere in the artifact)
pq_ok     = row whose anchor cell quotes words 1..16        (16 words, located)
```

Pristine v2 gives `6 / 7 / 7 / 0` on those four — the intended behaviour.

## 3. Verdicts — the four named mutants, on the live patch (`f26ed9bb`)

| # | mutation (exact edit) | selftest tally | exit | CLI `long/absent/one/ok` | verdict |
|---|---|---|---|---|---|
| — | pristine | `cases=14 failed=0` | 0 | 6/7/7/0 | baseline green |
| **m1** | delete the length gate in `quote_check`: `if count > cap: overlong.append(…)` branch removed, `elif not where` → `if not where` | `cases=14 failed=1` (failed: `quote-overlong-refused`) | 1 | **0**/7/7/0 | **KILLED** |
| **m2** | `locates()` compares a prefix: `if needle in text` → `if needle[:20] in text` | `cases=14 failed=1` (failed: `quote-located-accepted`) | 1 | 6/**0**/7/0 | **KILLED** |
| **m3** | one refusal code for both classes: `if absent: return EXIT_QUOTE_ABSENT` → `return EXIT_QUOTE_TOO_LONG` | `cases=14 failed=2` (failed: `quote-absent-refused quote-located-accepted`) | 1 | 6/**6**/**6**/0 | **KILLED** |
| **m4** | as named — `normalize_text` collapses every whitespace run (`" ".join(text.split())`) **and** a single-token quote is treated as located (`elif not where and words(quote) > 1:`) | `cases=14 failed=1` (failed: `quote-located-accepted`) | 1 | 6/7/**0**/0 | **KILLED** |

Killers, attributed:

- m1 → `quote-overlong-refused` (case 11). Its fixture is the right shape: the 26-word span is
  *present* in `artifact-over.txt`, so only the cap can refuse it. CLI confirms: m1 returns 0
  for a 26-word located quote.
- m2 → `quote-located-accepted` (case 13), and **only** by the negative-location line
  `locates(f"intro\n{first} widened", wrapped) == ""`. Case 12's absent quote
  (`"the requested sentence is not in the captured bytes at all"`) shares no 20-character
  prefix with its artifacts, so it does not see the defect at all. CLI confirms: m2 returns 0
  for a 21-word quote that is absent but whose prefix locates.
- m3 → two independent assertions: `code == EXIT_QUOTE_ABSENT` in case 12 and
  `partial_code == EXIT_QUOTE_ABSENT` in case 13.
- m4 → `quote-located-accepted`, specifically the unit assertion
  `normalize_text("a\r\nb\rc") == "a\nb\nc"`. Attribution is in §4: the collapse half dies here,
  the one-word half does not die anywhere.

## 4. Survivors — named with the case that should have killed them

Two mutants survive the shipped suite (`cases=14 failed=0`, exit 0) while the CLI is provably
wrong. Each is a coverage finding, not a contract change.

| survivor | how built | selftest | CLI evidence | missing case |
|---|---|---|---|---|
| **m4b — one-word quote matches anything** | `elif not where and words(quote) > 1:` alone (whitespace normalisation untouched) | `cases=14 failed=0`, exit 0 | `pq_one` → **exit 0** (should be 7); `long/absent/ok` still 6/7/0 | **`quote-single-word-absent-refused`**: a row whose anchor cell carries a one-word quote (`"zzznotinartifact"`) that occurs nowhere in the artifact must exit 7. No shipped case uses a span shorter than 16 words, so the `words(quote) > 1` hole is invisible to the suite. |
| **m2b — 20-char prefix compare, with the guard removed** | m2 + delete `locates(f"intro\n{first} widened", wrapped) == ""` | `cases=14 failed=0`, exit 0 | `pq_absent` → **exit 0** (should be 7) | **`quote-absent-prefix-shared-refused`**: the absent fixture must share its opening characters with the artifact — e.g. quote words 1..20 of the capture plus one extra word, so the full span is absent while `quote[:20]` locates. Case 12's fixture shares nothing; the whole anti-prefix defence of the patch rests on one line of case 13. |
| **m3b — detector mutant, not a validator mutant** | m3 + both exact-code assertions weakened to `code != EXIT_OK` / `partial_code != EXIT_OK` | `cases=14 failed=0`, exit 0 | `pq_absent` → **exit 6**, i.e. the caller cannot tell "too long" from "not in the bytes" | none missing — this records that m3's kill is *assertion-strength*, not structural: the two refusal classes stay separable only while two separate assertions pin the exact numbers. `!= EXIT_OK` in either place reopens the C3 sub-predicate "distinct non-zero exit codes". |

Also attributed: **m4a** (whitespace collapse alone, no wildcard) is **killed** by the same
`normalize_text` assertion (`cases=14 failed=1`, `quote-located-accepted`), and its CLI stays
correct (7 for the one-word quote). So m4-as-named dies for the collapse, and its one-word half
is the part that escapes.

## 5. Fallback verdict on the pre-change body (as instructed)

`plans/sources_adopt.py` @ `6fe6e762` contains no quote surface at all:
`grep -c 'EXIT_QUOTE\|check_quotes\|quote_file' baseline.py` → `0`. Applied to that body, every
one of m1–m4 has **no behaviour-bearing site**, so each is a no-op and the suite cannot observe
it:

```
$ python3 baseline.py --selftest | tail -1
SELFTEST cases=10 failed=0
$ python3 baseline.py --quote-file q.txt --artifact art.txt ; echo exit=$?
baseline.py: error: unrecognized arguments: --quote-file q.txt --artifact art.txt
exit=2
```

Verdict on the baseline: **all four mutants survive vacuously** — `cases=10` contains no quote
case, and the tool exits 2 before any quote is examined. That is the C3 control, and it is the
reason the four new cases are not optional: on the pre-change body the detector is blind to the
entire defect class. Mutants injected into that body *together with* the four new cases are the
`m0` probe below, which is why the cases are failure-capable rather than decorative.

## 6. Corroboration on the independent reference stand-in (`reference.py`, `3c253a38`)

Different fixtures, same interface, 14 cases:

| mutant | tally | verdict |
|---|---|---|
| m0 — quote validation removed, cases kept | `cases=14 failed=2` (`quote-over-25-refused quote-absent-refused`) | killed (proves the new cases are failure-capable) |
| m1 (no cap) | `cases=14 failed=1` (`quote-over-25-refused`) | killed |
| m2 (20-char prefix) | `cases=14 failed=1` (`quote-absent-refused`) | killed |
| m3 (one code) | `cases=14 failed=1` (`quote-absent-refused`) | killed |
| m4 (collapse + one-word wildcard) | `cases=14 failed=0` | **survived** — same shape as the live patch |

The independent implementation reproduces the live patch's kill/survive profile for m1–m3 and
its m4 escape, so the escapes are properties of the *case set*, not of one author's code.

## 7. Reproduction

```bash
cd /tmp/r30-R30MutGate
cp -p /tmp/r30-GateQuote/sources_adopt.py patched2.py && sha256sum patched2.py   # f26ed9bb…
python3 patched2.py --selftest | tail -1                                         # cases=14 failed=0
for m in m1 m2 m2b m3 m3b m4 m4a m4b; do python3 q_$m.py --selftest | tail -1; done
for f in patched2 q_m1 q_m2 q_m3 q_m4b; do
  for q in pq_long pq_absent pq_one pq_ok; do
    python3 $f.py --quote-file $q.txt --artifact part.txt >/dev/null; echo "$f $q $?"; done; done
```

Mutant application method: `cp patched2.py q_mX.py`, then one surgical replacement per mutant
(the exact edits in §3/§4). For the v1→v2 port, `diff -u patched.py p_mX.py > p_mX.patch` and
`patch --fuzz=3 q_mX.py < p_mX.patch`; application is verified by
`diff p_mX.py q_mX.py`, whose output is exactly the v1→v2 additions (`found` channel, receipt
wording, four `found` assertions) and nothing else. m1 did not port mechanically (its hunk
context changed), so it was re-applied by hand to the v2 body and confirmed by
`grep -c 'count > cap' q_m1.py` → `0`.

Verbatim tallies of every run performed:

```
baseline   SELFTEST cases=10 failed=0     reference  SELFTEST cases=14 failed=0
patched    SELFTEST cases=14 failed=0     patched2   SELFTEST cases=14 failed=0
q_m1       SELFTEST cases=14 failed=1  (quote-overlong-refused)
q_m2       SELFTEST cases=14 failed=1  (quote-located-accepted)
q_m2b      SELFTEST cases=14 failed=0
q_m3       SELFTEST cases=14 failed=2  (quote-absent-refused quote-located-accepted)
q_m3b      SELFTEST cases=14 failed=0
q_m4       SELFTEST cases=14 failed=1  (quote-located-accepted)
q_m4a      SELFTEST cases=14 failed=1  (quote-located-accepted)
q_m4b      SELFTEST cases=14 failed=0
m0         SELFTEST cases=14 failed=2  (quote-over-25-refused quote-absent-refused)
m1         SELFTEST cases=14 failed=1  m2 SELFTEST cases=14 failed=1
m3         SELFTEST cases=14 failed=1  m3b SELFTEST cases=14 failed=0
m4         SELFTEST cases=14 failed=0  (reference stand-in)
p_m*       SELFTEST cases=14 failed={1,1,0,2,0,1,1,0}  (same shape on v1 93ee7f7c)
```

## 8. Restoration and integrity evidence

- This seat wrote **only** this report file under the lane. It never created, edited or deleted
  any other lane path, never wrote in `/tmp/r30-GateQuote/`, and never wrote under
  `/home/vgpnk/Projects/shokuknow` or `/home/vgpnk/Projects/shokunin`.
- The pre-change body I mutated is preserved untouched at `/tmp/r30-R30MutGate/baseline.py`:
  `6fe6e762ab0c61da4ddbf029a2aa1a38cb64732ebd1ccbee4773c5eadcf7ead2`, 20424 bytes. That hash
  equalled the lane file at 04:21 and at 04:27 (measured twice).
- **Lane file changed during this seat's run, by integration, not by me:** at 04:29:03
  `plans/sources_adopt.py` became `f26ed9bb94086e9e9a7c3d7812608870e3fd1de441d5fe10fcff380f7b14609d`,
  33956 bytes — `diff -q` says it is byte-identical to `/tmp/r30-GateQuote/sources_adopt.py`.
  Its selftest on the lane copy reads `SELFTEST cases=14 failed=0`, exit 0. So the bytes I
  mutation-tested are the bytes that landed; nothing needs re-running for the verdicts above.
- `/tmp/r30-GateQuote/` was read and copied only; its `sources_adopt.py` hash was `f26ed9bb…`
  before and after my final probe run. Its `mut/` directory and `__pycache__/` are the sibling's;
  I created nothing there.
- Every mutant lives in `/tmp/r30-R30MutGate/` under a distinct name (`m*` = reference-derived,
  `p_m*` = v1-derived, `q_m*` = live-v2-derived). No mutant name shadows a source file, and no
  mutant was ever executed from a path inside the lane or the sibling's scratch.

## 9. Reading of the result

The patch's quote validator kills three of the four named structural defects outright and kills
the fourth (m4) on its whitespace half. Both remaining escapes are narrow and case-shaped, not
contract-shaped:

1. a **one-word** span absent from the artifact is accepted (m4b — `words(quote) > 1` exempts it
   from the absence branch);
2. the prefix-only defence (m2/m2b) rests on a single negation line in case 13: case 12's absent
   fixture shares no 20-character prefix with its artifacts
   (`'the requested senten' in "a capture that says alpha elsewhere\nunrelated bytes\n"` → `False`,
   measured), so a prefix-comparing validator would pass case 12.

The two named cases in §4 would kill them. Whether the suite grows to 16 cases or C3's frozen
`cases=14` tally stands with these as recorded gaps is the claim owner's call; this seat only
reports that the two defects are currently invisible to `--selftest` while visible at the CLI.

Tooling: nothing installed or upgraded; `python3` (host) plus coreutils/`patch` were sufficient.
