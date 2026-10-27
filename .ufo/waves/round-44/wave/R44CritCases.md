# R44CritCases — attack on the frozen C2 probe case set

Round 44 wave critic seat (leaf). Target: `corpus/evidence/round44/feal-linear-dry-cases-freeze.txt` +
`plans/feal_linear_probe.py` (both frozen; read in full, never modified). All fresh measurements ran inside the
round-44 envelope (`claims/envelope.sh`); envelop lines are in the receipt
`wave/R44CritCases/extra-cases-receipt.txt` (sha256 below). No frozen file was edited; the probe was imported
read-only to reuse its sandbox/harness machinery for extra end states.

## 1. Grader behaviours the frozen case set does NOT exercise (each verified empirically)

The 14 frozen cases exercise exactly three code paths of `test_outputs.py`: file absent → `FileNotFoundError`
(nop, :120); one constant missing → `AssertionError` (one-missing, :122); substring presence → pass (all P
cases, :121-122). Everything else is unexercised. I graded seven additional end states with the same captured
grader, same harness, same sandbox (receipt above):

| extra state | observed | grader path |
|---|---|---|
| directory at `/app/plaintexts.txt` | F `error=IsADirectoryError` | read-error family, not in frozen set |
| file mode 000 | F `error=PermissionError` | read-error family, not in frozen set |
| non-UTF-8 bytes (`\xff\xfe\x00\x01`) | F `error=UnicodeDecodeError` | encoding axis, not in frozen set |
| file exists, zero bytes | F (AssertionError) | distinct from absent; nop covers only absent |
| CRLF (`\r\n`) separators | P | encoding/format axis, not in frozen set |
| canary/comment lines around the oracle output | P | substring ignores non-numeric lines |
| one constant split across a newline (clean 100-line base) | F | split/delimiters axis, not in frozen set |

Claims an entry could later make that the probe cannot support: “a directory at the answer path fails with
IsADirectoryError”, “unreadable file fails”, “non-UTF-8 content fails”, “an empty file fails”, “CRLF output
passes”, “a constant split across lines fails”. All are true (measured) but none is exercised by the 14 frozen
rows or by V11's 48 states (`STATE_KINDS` in `round44_c2_verify.py:380-381` has no dir / permission /
non-UTF-8 / CRLF kind; the closest are absent/empty/split-one). If the entry asserts any of these, the counter's
V11 will not object and no receipt row backs it.

**Timing of the verifier / size:** `task.toml:22` sets `timeout_sec = 1800.0` for the verifier; no case
materialises a slow/huge plaintexts file, and the probe never measures wall time (deterministic receipt). A
claim like “the verifier times out on a pathological file” is unexercised and should be written as a limit.
**pytest collection:** the harness replaces pytest with a direct call of `test_attack` and maps exit-status 0 ↔ P
(`feal_linear_probe.py:244-256`); pytest's collection/exit-code semantics (pytest exit 2 = error, 5 = no tests
collected, plus `--ctrf`/`-v -rA` in `test.sh:18-22`) are never run. Equivalent for this single-test pinned
capture, but the equivalence itself is unmeasured — the entry should not claim “pytest” behaviour beyond what the
harness observed. **Canary line:** `test_outputs.py:1-2` holds the canary comment; it is inert in the grader and
no case touches its role (comment-wrapper shows comment lines in the answer file pass, which is the only
observable canary-adjacent behaviour).

## 2. Redundant cases

- **pairs-plaintexts ≈ ciphertexts-copied** (`dry table :17-18`). Both produce a file containing zero of the
  100 constants (pair plaintexts use counters 0-31, `gen.py:23-27`; the 100 targets use counters 32-131,
  `gen.py:57-62`, so neither file can contain any target). Both fail on the first `assert c in data`, and both
  are DECISIVE on the same line (`round44_c2_verify.py:336-337` → `test_outputs.py:122`). Only the narrative
  differs; one of the two adds no coverage.
- **oracle-concatenated ≈ oracle-reversed** (`dry table :10,12`): both transform the complete 100-answer set in
  presentation only (no separators vs reversed order) and exercise the same substring assertion. The more
  informative format axes are already carried by oracle-zero-padded (leading zeros) and oracle-plus-decoys
  (extra lines); concat and reversed overlap with each other and with those. Dropping one would not reduce the
  covered behaviour set.
- Non-redundant: nop (absence), oracle-solve-sh (honest attack), the three attackless /pub reads (each proves a
  different public artifact suffices), one-missing (any-missing ⇒ fail), hex-output (format reject), wrong-key
  (key correctness), each fail row's distinct DECISIVE line.

## 3. `violates=` audit against instruction.md exact words

The tags map to exact instruction lines (`probe:77-82`): `known-plaintext-attack`/`recover-key` →
`instruction.md:7` “Implement a known-plaintext attack that recovers the key of the cipher.”; `decrypt-all` →
`instruction.md:8` “Prove you have recovered the key by decrypting all the ciphertexts in”; `plaintexts-file` →
`instruction.md:10` “/app/plaintexts.txt”. Line-by-line check of every case: **no tag is wrong**. Highlights
where a tag could have been contested, and why it stands:
- `hex-output` violates=() is correct: the instruction names no format; hex digits simply fail the substring
  check. The row's own note states this.
- `oracle-plus-decoys` violates=() is correct: “your answer” is written in full; extra wrong-key decryptions
  are extra content, not a missing requirement.
- `decrypt-public-keys`/`replay-public-gen`/`copy-public-constants` carry `recover-key`+`known-plaintext-attack`
  (and `decrypt-all` for the two that do not run `./decrypt`): obtaining the key from public source is not the
  instructed attack, so “violates” is defensible.
- `nop` carries all four tags; it implements nothing, so all four prose requirements are unmet.
One nuance worth recording: the `recover-key` tag on the /pub cases depends on reading “recovers the key” as
“by cryptanalysis”; the dry table's phrasing (“no attack”) makes that reading explicit, so it is consistent.

## 4. Is the /pub modelling honest? Yes, with two caveats

- The three /pub files are byte-exact pin captures (`probe:60-68` digests; `PINS` checked before every run) and
  exactly the upstream paths `tests/test_outputs.py`, `environment/task-deps/gen.py`, `solution/solve.sh`. The
  image deletes `gen.py` (`Dockerfile:12-13`) and never ships the tests, but the benchmark repo publishes them,
  and `task.toml:34` sets `allow_internet = true` — so a real agent can fetch them. The modelling honestly
  discloses this (`probe:14-17`) and the freeze's “Limits” section repeats that cases are constructed end states.
- Caveat 1: /pub hands the agent the **verifier's own test file**, i.e. the exact oracle; the three attackless
  passes therefore read as “the public repo leaks the answer”. That is a property of the benchmark, not a probe
  artefact, but the entry must present copy-public-constants & co. as grader-gameability findings, not as proof
  of any robustness property.
- Caveat 2: the oracle (`oracle-solve-sh`) does not produce a clean 100-line answer. `solve.sh`'s `attack`
  writes its diagnostics (“Maybe …”, “… for mask …”) into `/app/plaintexts.txt` too (`solve.sh:289,304`;
  measured: 266 lines, constants embedded). All oracle-variant passes therefore hold on a polluted file — which
  strengthens the substring finding but means the case set never proves the oracle's own output is the clean
100-line file the entry may want to describe.

## 5. Defect list (summary)

1. **Read-error family beyond FileNotFoundError not exercised** — directory, mode-000, undecodable bytes all
   produce distinct F classes (measured); the entry must not claim them, and the counter cannot check them.
2. **Empty-file state absent** from the 14 (distinct from nop); measured F.
3. **Delimiter/encoding axes partially absent** — CRLF passes, a constant split across a newline fails
   (measured); neither is a frozen row.
4. **Verifier timing/size and pytest-collection equivalence unexercised** — write as limits, not claims.
5. **Redundant rows**: pairs-plaintexts ≈ ciphertexts-copied; oracle-concatenated ≈ oracle-reversed.
6. **No wrong `violates=` tag found** (audit §3).
7. **/pub modelling is honest**; note the grader-file disclosure and the polluted-oracle nuance (§4).

Evidence files: `corpus/evidence/round44/feal-linear-probe.txt` (frozen receipt, 14/14 match), the dry freeze
table, and `wave/R44CritCases/extra-cases-receipt.txt` (new measurements, sha256
`3ab2112a791b7caa1e10e3c49fff6f3b129289ffc3afd173b9d12659dd96dfae`). Envelope lines pasted in the receipt;
`local_bin` digest unchanged on every run.

VERDICT: case-set-defects-7
