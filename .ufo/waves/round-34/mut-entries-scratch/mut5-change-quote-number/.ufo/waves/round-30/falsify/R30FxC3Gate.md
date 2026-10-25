# R30FxC3Gate — attack on the quote validator after strengthening

Seat: `L1Kengaku30.R30FxC3Gate-3` (leaf). Round 30, falsify wave, claim **C3**
(`plans/round-30-claims.md` §C3). Subject: `plans/sources_adopt.py` quote mode.
No lane bytes were edited; every mutation ran on a `/tmp/r30fx-C3Gate/` copy. No tool installed,
no pacman transaction, no host change.

## 0. Subject bytes (measured, not asserted)

| body | source | sha256 | lines |
|---|---|---|---|
| strengthened (live lane) | `git` worktree, **dirty** (`M plans/sources_adopt.py`, HEAD `363a4eb`) | `e9b6bc044…191a195` | 811 |
| seat deliverable | `/tmp/r30-GateQuote/sources_adopt.py` | `f26ed9bb9…7b14609d` | 791 |
| freeze baseline | `git show HEAD:plans/sources_adopt.py` | `6fe6e762a…7ead2` | 478 |

Python 3.14.8. Line citations below are into the strengthened byte.

```
$ python3 plans/sources_adopt.py --selftest | tail -1        # strengthened
SELFTEST cases=14 failed=0            exit 0
$ python3 /tmp/r30fx-C3Gate/baseline.py --selftest | tail -1  # HEAD byte
SELFTEST cases=10 failed=0            exit 0
$ python3 /tmp/r30fx-C3Gate/baseline.py --quote-file fx/pq_ok.txt --artifact fx/part.txt
sources_adopt.py: error: unrecognized arguments: --quote-file … --artifact …   exit 2
```

Cases 1–10 are byte-identical between baseline and strengthened (`diff` of `^CASE` lines: empty).
C3's control line in `.ufo/waves/round-30/claims/gate-before.txt` reproduces exactly.
`words()` in `plans/round30_defects.py:38-39` is `len(text.split())`, identical to
`sources_adopt.words` (`:272-273`) — the "same counter" comment holds.

## 1. The two named survivors, reproduced

Fixtures (`/tmp/r30fx-C3Gate/fx/`): `part.txt` = 26-word run; `pq_one` quotes the single word
`zzznotinartifact` (absent); `pq_absent` quotes `w1 w2 w3 w4 w5 w6 w7 zzznotinartifact` — its
**first 20 characters** (`w1 w2 w3 w4 w5 w6 w7`) are in `part.txt`, the 8-word span is not;
`pq_ok` = 16 words present; `pq_long` = 26 words present.

Mutants (sed on copies, exactly the two the mutation-tester named in `build/R30MutGate.md:78-79`):

- **m4b** `current.py:399` `elif not where:` → `elif not where and words(quote) > 1:`
- **m2b** `current.py:336` `needle = normalize_text(quote)` → `…[:20]`, **and** delete the single
  negation line `locates(f"intro\n{first} widened", wrapped) == ""` (the seat's own copy of it)

```
$ for f in seat seat_m4b current cur_m4b seat_m2 seat_m2b current cur_m2 current cur_m2b; do
    python3 $f.py --selftest | tail -1; done
seat       SELFTEST cases=14 failed=0   ← m4b survives on the seat byte
seat_m4b   SELFTEST cases=14 failed=0        exit 0
current    SELFTEST cases=14 failed=0
cur_m4b    SELFTEST cases=14 failed=1   failed: quote-absent-refused
seat_m2    SELFTEST cases=14 failed=1   failed: quote-located-accepted
seat_m2b   SELFTEST cases=14 failed=0   ← m2b survives on the seat byte
current    SELFTEST cases=14 failed=1   failed: quote-absent-refused
cur_m2b    SELFTEST cases=14 failed=1   failed: quote-absent-refused
```

Behavioural difference (exit codes, same fixtures):

```
seat_m4b  pq_one    exit 0   QUOTE … located=1 absent=0 … ok S931 words=1 at  quote="zzznotinartifact"
seat_m2b  pq_absent exit 0   QUOTE … located=1 absent=0 … ok S932 words=8 at part.txt
current   pq_one    exit 7 ; current pq_absent exit 7 ; current pq_ok exit 0 ; current pq_long exit 6
```

Verdict on the two named mutants: **both are dead on the strengthened body** (`:652`
`word_report["absent"] == ["S022"]` kills m4b; `:656` `prefix_report["absent"] == ["S023"]` kills
m2b-with-the-negation-deleted). Both kills live inside the single case `quote-absent-refused`, so
both reopen if that one case is relaxed — the tally stays `cases=14` either way (§4, F9).
The one-word kill is not cosmetic: on the mutant the `ok` line prints `at ` with an empty artifact
name, i.e. a matched-where-nothing-was-found receipt.

## 2. Required probes

### 2a. Artifact = directory holding a non-UTF-8 file

`fx2/dir-mixed/`: `capture.txt` (UTF-8, irrelevant text) + `latin1.dat` whose bytes carry
`Die Verfügungssicherheit ist nicht belegt hier` as latin-1 (`caf\xe9`, undecodable as UTF-8).
The row quotes exactly that sentence.

```
$ python3 current.py --quote-file fx2/a-row.txt --artifact fx2/dir-mixed
QUOTE rows=1 spans=1 located=0 found=0 overlong=0 absent=1 malformed=0 cap=25 artifacts=capture.txt
  REFUSED S941 absent words=6 quote="Die Verfügungssicherheit ist nicht belegt hier"
exit=7
```

The span *is* in the directory's bytes but is reported against `capture.txt` only: the skipped file
is not named, and the refusal is labelled `absent` — the label a reader must repair by *re-opening
the source*, though the real repair is *re-capture in UTF-8*. `load_artifact` records the skip in
`skipped`, but `:320-321` only surfaces it when **nothing** decoded, so `artifacts=` silently omits
it. (Decoding was not silently rescued — the conservative direction — but the receipt hides that a
file was dropped.)

Directory whose only file is undecodable: `exit 2`,
`problem=--artifact holds no UTF-8 text (unreadable: only.dat)`.

### 2b. A row with three spans where one is absent

```
$ python3 current.py --quote-file fx2/b-row.txt --artifact fx2/three.txt
QUOTE rows=1 spans=3 located=2 found=2 overlong=0 absent=1 malformed=0 cap=25 artifacts=three.txt
  ok S942 words=5 at three.txt quote="t1 t2 t3 t4 t5"
  ok S942 words=6 at three.txt quote="t6 t7 t8 t9 t10 t11"
  REFUSED S942 absent words=3 quote="totally absent span"
exit=7
```

Correct and honest at span granularity: `spans=3` is the true count, the refused span is named, and
the row is refused. Note `located=2 absent=1` for **one** row — `located/absent/overlong/found` are
span lists, not row sets (`rows=1`), so a caller aggregating "rows located" from them double-counts;
`build/R30GateProp.md` §7 warned of this, and the summary line still invites the misread.

### 2c. 25-word vs 26-word quotes (both fully present)

```
$ python3 current.py --quote-file fx2/c25-row.txt --artifact fx2/c-art.txt   → ok S944 words=25   exit 0
$ python3 current.py --quote-file fx2/c26-row.txt --artifact fx2/c-art.txt   → REFUSED S945 overlong
                                              words=26 cap=25 at c-art.txt    exit 6
```

Cap inclusive at 25, exclusive at 26, refusal is length not absence (`found=1 located=0`).
Failure-capability re-proved independently of the build report: `count > cap` → `count > cap + 2`
gives `SELFTEST cases=14 failed=1 failed: quote-overlong-refused` and greens the 26-word CLI at exit 0.

### 2d. Artifact that is not the cited source

```
$ python3 current.py --quote-file fx2/self.txt --artifact fx2/self.txt
QUOTE … located=1 … artifacts=self.txt
  ok S946 words=8 at self.txt quote="the quote file is its own artifact witness"
exit=0
$ python3 current.py --quote-file fx2/self.txt --artifact fx2/unrelated.txt   # row's source cell says https://example.invalid/x
  ok S946 words=8 at unrelated.txt                                            exit 0
```

**Yes, trivially.** `--artifact` is caller-chosen; `quote_check` never reads the row's `source` cell
(`:340-421` touches only `cell(5)` and the artifact bytes). The gate accepts **its own input file as
the witness**. The only trace is the artifact name in the `ok` line, which the caller supplied.

Degenerate spans pass the same door — measured, not inferred:

```
fx2/d-word.txt  p.9: "the"   → ok S947 words=1 at unrelated.txt   exit 0
fx2/d-space.txt p.9: " "     → ok S948 words=0 at unrelated.txt   exit 0
```

`QUOTE_SPAN_RE = [^"]+` admits a single space; `words(" ")==0`; `locates(" ")` matches any text
containing a space. So the strengthened body still greens a **zero-word** quote and a one-word quote
that merely occurs somewhere. m4b's repair covers only *absent* one-token spans.

## 3. Mutants that still survive the strengthened suite (calibration)

Each is one semantic edit on a `/tmp` copy; `--selftest` prints `cases=14 failed=0`, exit 0.

| mutant | edit | suite | behavioural delta measured |
|---|---|---|---|
| **m5b** refusal precedence swapped | absence branch before cap branch (`:390-399`) | `failed=0` | `fx2/b2-row.txt` (25w present + 26w + absent): swapped `exit 7 overlong=0 absent=2` vs correct `exit 6 overlong=1 absent=1`. The docstring's "first refusal in the order 2, 4, 6, 7 wins" is unpinned for one span that is *both* overlong and absent — no case has that span shape. |
| **m13** decode-with-replacement | `decode("utf-8","replace")`, `except OSError` (`:315-320`) | `failed=0` | `dir-mixed` → `artifacts=capture.txt,latin1.dat`: the documented "skipped and named" contract is dropped and the suite cannot tell. Low blast radius (U+FFFD rarely equals a quote), but the docstring claim is untested. |
| **m15** case-insensitive locate | `needle.lower() in text.lower()` (`:336-337`) | `failed=0` | quote `the verifier never runs in the agent's sandbox` against `The Verifier Never Runs in the Agent's Sandbox.` → `exit 0` (correct body: `exit 7`). Contradicts "never a fuzzy … match"; every fixture differs in more than case, so nothing pins case sensitivity. |

Not survivors, for the record: `count > cap → count >= cap` and `count > cap + 2` die on
`quote-boundary-25-accepted` / `quote-overlong-refused` respectively.

## 4. Findings, by severity

**F1 — high (calibration). The C3 predicate cannot distinguish the two byte states.**
`f26ed9bb` (seat, 791 lines) and `e9b6bc04` (strengthened, 811 lines) **both** satisfy C3's frozen
predicate as written: both print `SELFTEST cases=14 failed=0` exit 0, and both refuse an absent
multi-word quote (7) and a 26-word quote (6) at distinct codes. The predicate's clause "a quote
absent from the supplied artifact bytes is refused" is satisfied by *a* multi-word absent quote; the
seat byte greens a *one-token* absent quote (measured, §1). So the predicate certifies the tally plus
two reachable refusal classes — not that the validator has no wildcard. It is a necessary, not
sufficient, proof of C3's surface sentence ("the adoption gate validates quotes").
Second-order: the strengthened byte is **uncommitted** (` M plans/sources_adopt.py` while HEAD is
`363a4eb`). The predicate's green exists only in a dirty worktree; `git stash`/`checkout` reverts it
to `cases=10`. `plans/gate_timing_check.py` reads reports from a commit, so a Gate return that quotes
this green must rest on a commit that actually carries `e9b6bc04`.

**F2 — high (operability). No binding between the row's `source` and `--artifact`.**
Measured §2d. The gate proves "this span is a byte substring of bytes the caller handed me". It
cannot detect the laundering loop `corpus/QUALITY.md` Q5 forbids, and it accepts its own quote file
as witness. `R30GateQuote.md` §7 states this risk, but the frozen predicate does not encode it, so a
green cannot be read as "the cited source says this".

**F3 — medium. Degenerate spans green.** A one-word present quote (`"the"`) and a zero-word span
(`" "`) both exit 0 (§2d). The m4b repair refuses *absent* one-token spans only; nothing requires a
span to be evidence-shaped (word floor, or a minimum length).

**F4 — medium. A non-UTF-8 file in a directory artifact is dropped silently and mislabelled.**
§2a: a quote present in the skipped file is refused as `absent`, and `artifacts=` omits the file. The
refusal label points the reader at the wrong repair. `:320-321` names the skip only when nothing
loads.

**F5 — medium. Documented refusal precedence (2,4,6,7) is unpinned.** m5b survives and changes a
real exit code (§3). No fixture carries a span that is both overlong and absent.

**F6 — low/medium. Case-insensitive compare survives** (m15), greening a case-only paraphrase. The
docstring's exactness claim is asserted in prose, not in a case.

**F7 — low. The quote file is read unguarded.** `:367` `quote_file.read_text(encoding="utf-8")` is
outside any try. Measured: missing file, non-UTF-8 file, and a directory all raise an uncaught
traceback with **exit 1** — an undocumented code that collides with the selftest-failure code, so a
caller cannot tell "python crashed" from "case failed". The artifact side has `EXIT_QUOTE_UNREADABLE`;
the quote-file side has nothing.

**F8 — low. The cap is per span, and the cell's `(N words)` annotation is never checked.**
Measured: three located 25-word spans in one anchor cell → `exit 0 spans=3` (75 quoted words green);
a 24-word quote annotated `(3 words)` → `exit 0`. `build/R30GateQuote.md` §7 declares the per-span
cap as intended; the annotation gap is undeclared, and the live rows S084–S086 carry
`(3 whitespace tokens)` cells whose counts the gate never verifies.

**F9 — low. Both new mutant kills are single-point.** `:652` and `:656` are the only assertions that
kill m4b and m2b respectively; deleting those four lines reproduces `f26ed9bb` and the tally still
reads `cases=14 failed=0`. The suite's shape (assertions folded into case 12 to keep the count at 14)
means the count is not a measure of coverage.

**F10 — informational. `absent` conflates a paraphrase with a line-wrap mismatch.** `locates` is a
byte test after `\r\n`/`\r` normalisation only; a source line that wraps and is transcribed with a
space is refused as `absent`, indistinguishable from a fabricated quote. Measured on `fx2/b2-row.txt`:
`at nowhere` although the first 25 words are in the artifact. Strict-by-design and honest in the
report, but the refusal label does not separate "re-transcribe" from "re-check the claim".

Non-findings (tested, held): NBSP does not split-and-hide — `"\u00a0".join(...)` of 30 tokens counts
30; a 3-quote cell refuses if any span is absent; escaped/greedily-paired quotes stay structural;
the 25/26 boundary is exact; `locates` is newline-symmetric; the live S078 row still parses as two
8-word spans (`exit 0`).

## 5. What C3 proves, and what it does not

- **Proves:** the gate now has a quote mode; per-span word cap 25 enforced inclusively; a span absent
  from the supplied bytes is refused with a code (7) distinct from over-length (6), from structural
  defects (4) and from an unreadable artifact (2); the pre-change byte cannot reach the mode at all
  (argparse 2); the suite grew 10 → 14 with cases 1–10 untouched; both named survivors from the build
  wave are now killed.
- **Does not prove:** that a green row's quote came from the row's cited source (F2); that a span is
  evidence-shaped (F3, F8); that the artifact set was complete and decodable (F4); that the
  documented refusal precedence holds (F5); that matching is exact in case (F6); that the tally
  counts coverage rather than assertions (F9); that the tested bytes are the committed bytes (F1).
- **Does not satisfy:** C3's frozen predicate as a *guard* — the same predicate passes on the
  pre-strengthening byte (F1), so a future body that reintroduces the one-token hole would still
  print `cases=14 failed=0` unless the S022/S023 assertions survive.

## 6. Verdict

C3's frozen predicate **holds on the strengthened body, measured**: `SELFTEST cases=14 failed=0`,
exit 0; `EXIT_QUOTE_TOO_LONG`=6 and `EXIT_QUOTE_ABSENT`=7 both reachable and separable; both new
cases failure-capable (cap mutant, m4b); baseline at `git show 363a4eb:` rejects the invocation with
argparse exit 2 and its selftest prints `cases=10`. The two mutants the build wave left alive are
dead on the strengthened byte and were alive on the byte it replaced.

```
VERDICT: PASS — C3's frozen predicate holds on the strengthened byte (cases=14 failed=0, exit 0; 6 vs 7 separable; baseline argparse exit 2), but the same predicate also passes the pre-strengthening byte, and the artifact is caller-trusted, so the surface sentence is broader than the evidence.
```

## 7. Residual risk and verification gaps

- The lane body is uncommitted; my green (and C3's) dies with a checkout. Re-run
  `python3 plans/sources_adopt.py --selftest` **after** the round's commit lands and confirm the file
  in the commit is `e9b6bc04…`.
- F2 cannot be closed by this tool in its current shape: any fix needs the artifact to be derived
  from, or pinned to, the row's `source` cell (a fetch receipt), not from a second CLI argument.
- F3/F8 need a span-shape floor (minimum words, or minimum non-space characters) and an annotation
  cross-check; neither exists, and neither is required by C3's predicate.
- Seeds/survivors left for a later wave: m5b (precedence), m13 (replace-vs-skip), m15 (case). A suite
  that adds one case per class would kill them; adding assertions inside case 12 would keep the tally
  at 14 while raising coverage, which is exactly the F9 confusion.
- Scratch is `/tmp/r30fx-C3Gate/` (`current.py`, `seat.py`, `baseline.py`, `cur_m*.py`, `seat_m*.py`,
  `fx/`, `fx2/`); nothing there is evidence, it is a reproduction recipe.
