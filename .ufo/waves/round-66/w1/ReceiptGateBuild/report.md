# ReceiptGateBuild — R66-C2 strict mode, proposed copy (round 66, w1)

Scope: build `--strict` for the round-65 sqlite receipt checker in a PROPOSED copy only.
The lane file `plans/round65_c1_sqlite_probe.py` was not edited (receipt `10-j`: empty
`git status --porcelain -- plans/round65_c1_sqlite_probe.py` and `git diff --stat` for that
path). One observation for the record: `plans/round66_c1_tensor_probe.py` is modified by
another wave seat during this run; it is not this seat's file and was not touched. No
battery run, no port bound, no network, no install.

Revision history (each step forced by a measured defect, no frozen value changed):

| rev | sha256 | what changed / why |
|---|---|---|
| 1 | `cd70ed61…` | first cut: frozen strict list, no selftest. Mutation tester: a receipt copying four value families was accepted while still carrying `# FABRICATED RECEPT … contains NO live-run data`; strict had no selftest. |
| 2 | `92eee572…` | added a whole-file `fabrication-declaration` word scan and seven strict selftest rows. Mutation tester: a live receipt whose LEG fragment contained `fabricated by harness` was refused (over-refusal); a reworded header evaded the scan. |
| 3 | `06270270…` | scan scoped to the header (lines before `GRADER`). Mutation tester: d3 — the same bytes with the declaration comments moved below `GRADER` passed, so the tripwire refused line order. |
| 4 | `b131e66e…` (this) | scan scoped to **probe-authored lines**: every line except `LEG` and `ENV`, the two families that carry grader-printed text. Moved comments and `RUN … driver="fabricated …"` fields are now caught; grader free text is still never read. |

## Files

| file | sha256 / size |
|---|---|
| `proposed/round65_c1_sqlite_probe.py` (proposal) | `b131e66eb74964c0dfc1001d6191115fd5e14587059e3ddc834a6fec0c3854af`, 1289 lines |
| `plans/round65_c1_sqlite_probe.py` (committed, untouched) | `f44b72834d8662cb6986e192dfbdf236daf6c99a174768294e504f7b634db4eb`, 1020 lines |
| `round65-strict.diff` | `diff -u` lane → proposed, 343 lines, 6 hunks: `@@ -77,11 +77,24 @@`, `@@ -112,6 +125,20 @@`, `@@ -781,18 +808,208 @@`, `@@ -869,6 +1086,22 @@`, `@@ -964,6 +1197,38 @@`, `@@ -983,12 +1248,16 @@` |
| `receipts/00`–`13` | one file per command, each ending `exit=<code>` |

Hunks are exactly: docstring (strict paragraph + usage line), constants, the new
`lane_root`/`_fields`/`strict_defects` block with the rewritten `check_receipt`, the
`strict_receipt()` helper, the strict selftest rows, and `main()` (`--strict` flag +
`SETUP strict-requires-check-receipt` guard).

## Frozen requirement → implementation

Frozen text: `plans/round-66-claims.md` R66-C2 "Strict-mode requirements".

| frozen item | code | defect names |
|---|---|---|
| GRADER sha = `b165f850…` **and** the committed grader bytes | `GRADER` line unique; `sha256`/`pin`/`rel` vs `GRADER_SHA256`/`TB2_PIN`/`GRADER_REL`; `sha256_file(<lane>/GRADER_REL)` vs the receipt's sha | `grader-line-count`, `grader-sha`, `grader-pin`, `grader-rel`, `grader-bytes` |
| AMALG sha = `0a9c8e34…` | `AMALG` line unique; `sha256` and `url` vs the frozen constants | `amalg-line-count`, `amalg-sha`, `amalg-url` |
| TOOLCHAIN well-formed, values equal the values the receipt itself carries | `gcc/gcov/bwrap/python` match `^\d+\.\d+(\.\d+)?$`; `gcc/gcov/bwrap` equal `version_token()` of the receipt's own `CC `/`GCOV `/`BWRAP ` banner lines (each banner unique) | `toolchain-line-count`, `toolchain-not-well-formed`, `toolchain-banner-count`, `toolchain-mismatch` |
| PROBE sha equals the committed probe bytes at this revision | probe binding = exactly one `PROBE sha256=<64 hex>` line equal to `sha256_file(<lane>/PROBE_REL)`, **or** the `# instrument plans/round65_c1_sqlite_probe.py version=` header whose version equals `PROBE_VERSION`; when both are present both are validated | `probe-line-count`, `probe-sha-not-well-formed`, `probe-sha`, `probe-instrument-count`, `probe-version`, `probe-binding-missing` |
| each VECTOR line equals the frozen table | every `VECTOR name=value` names a frozen case exactly once with the frozen value; unknown names refused | `vector-line-malformed`, `vector-duplicate`, `vector-missing`, `vector-mismatch`, `vector-unknown` |
| NOBIND G1–G5 present with `delta=0` | per case at least one `NOBIND <case> ` line, every `delta` `=0`; when `listeners_before`/`after` are present they must be integers with `after-before == 0` | `nobind-missing`, `nobind-delta`, `nobind-listeners-not-integer`, `nobind-listeners` |

One check beyond the frozen list: a receipt whose **probe-authored lines** (every line
except `LEG` and `ENV`, which carry grader-printed text) declare fabrication or
non-execution — `FABRICATED`, `nothing ran`, `no driver run`, `no live-run data` — is
refused as `fabrication-declaration`. The committed receipt has no hit in any
probe-authored line; the fabricated fixture has two in its comments and five in its `RUN`
driver fields.

Output shape in strict mode: `CHECK strict probe sha256=<lane probe sha> rel=…`, then the
default predicate's `CHECK fail …` lines (strict is a superset — a receipt the default
refuses is never accepted), then `CHECK defect: <name> …` per strict miss, then
`PREDICATE R65-C1 strict-pass|strict-fail`; exit 0 only when both lists are empty.
Default mode prints exactly what it printed before (receipt `07-g`: empty `diff -u`
between the lane probe's and the proposal's default-mode output on both fixtures).

## Commands (all from the proposal unless stated)

| # | command | exit | first finding / terminal line |
|---|---|---|---|
| a | `--check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt` | 0 | `CHECK ok cases=5` → `PREDICATE R65-C1 pass` |
| b | `--check-receipt corpus/evidence/round66/red/fabricated-r65.txt --strict` | 1 | `CHECK defect: fabrication-declaration '# FABRICATED RECEPT … contains NO live-run data'` (9 defects: 1 declaration, 4 well-formedness, 3 banner-count, 1 probe-binding-missing) → `PREDICATE R65-C1 strict-fail` |
| c | `--check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt --strict` | 0 | `CHECK ok cases=5 strict=yes` → `PREDICATE R65-C1 strict-pass` |
| d | `--check-receipt corpus/evidence/round66/red/fabricated-r65.txt` | 0 | `CHECK ok cases=5` → `PREDICATE R65-C1 pass` (M-1 default-mode behaviour, unchanged) |
| e | `--selftest --work <scratch>` | 0 | `SELFTEST pass`, 17/17 rows (8 default + 7 strict + render-table + predict-legs) |
| f | `--strict` (no `--check-receipt`) | 2 | `SETUP strict-requires-check-receipt` |
| g | `diff -u` lane vs proposal, default mode, both fixtures | 0 | `default-mode-identical=yes` (no diff lines) |
| h | proposal copied to scratch, `--strict` from there | 0/1 | committed → `strict-pass` exit 0; fabricated → 9 defects exit 1 (proves `lane_root()` fallback resolves the committed bytes from a scratch copy) |
| i | probe-binding fixtures (`09-i`) | 0/1/1/1 | committed + correct `PROBE` sha → 0; committed + 64 zeros → `CHECK defect: probe-sha …` exit 1; fabricated + correct sha → exit 1 (8 defects); committed + correct `PROBE` sha + `version=r65-c1/0` header → `CHECK defect: probe-version 'r65-c1/0' != 'r65-c1/1'` exit 1 (both bindings cross-checked) |
| j | `sha256sum` proposal/lane/zip/grader; `git status`/`git diff` of the lane probe | 0 | `0a9c8e…` (zip, 2990966 B), `b165f8…` (grader) measured; lane probe unchanged |
| k | `diff -u … > round65-strict.diff` | 1 | 6 hunks (diff exit 1 = files differ, as intended) |
| l | boundary fixtures (`12-l`) | 1/1/0/0/0/1/1/0 | q1 four value families + declarations kept → 1 defect; q2 `FABRICATED` word removed, `no driver run` comment kept → 1; q3 declarations removed, `frag=fabricated` LEG values kept → **passes**; q4 every named value copied → **passes**; q5 committed receipt with a LEG fragment `… (sqlite3 binary fabricated by harness)` → **passes** (grader text exempt); q7 header reworded but `RUN … driver="fabricated - nothing ran"` kept → 1 defect; q8 q1 with the declaration comments moved below `GRADER` → 1 defect (d3 closed); q9 every probe-authored line reworded and values copied → **passes** (the named limitation) |
| m | exemption placement (`13-m`) | 0/0 | q9 → 0; e1 = q9 plus the declaration appended inside a `LEG … frag=` value → 0 (trust boundary, Finding 1) |

Expectations a–d: **all four met**. Nothing in the frozen expectation was changed.

## Findings (calibration; no frozen rule edited)

1. **The declaration check refuses the sentinel's own words anywhere in the probe's
   voice, and nothing else.** Scope: every line except `LEG` and `ENV` (the two families
   that carry grader-printed text). Measured: the literal declaration is refused in the
   header (q1), in a comment moved below `GRADER` (q8, the mutation tester's d3) and in a
   `RUN … driver=` field (q7); a grader fragment containing `fabricated` is accepted (q5);
   a receipt whose probe-authored lines are all reworded and whose values are copied
   passes (q9, the mutation tester's d1). The exemption is a trust boundary, not a
   guarantee: a declaration placed inside a `LEG … frag=` value is invisible (receipt
   `13-m` e1, exit 0), and scanning those values would resurrect the d2 over-refusal — the
   two measurements are the same trade-off from opposite sides. q9/e1 are the claims'
   named limitation ("a receipt that copies every value from the committed bytes still
   passes strict"), now measured to be exactly a semantic/placement limit: lexical
   tripwire vs. reworded provenance. The frozen list also does not require the
   `SHAPE`/`FILES`/`ENV`/`PREDICTION` live-evidence lines; adding such a requirement would
   be a new receipt-format rule, so this proposal does not.
2. **The committed receipt carries no `PROBE` line** (line 2 is `# instrument
   plans/round65_c1_sqlite_probe.py version=r65-c1/1`; no `^PROBE ` line anywhere in the
   file). The frozen "PROBE sha equals the committed probe bytes" clause is therefore
   implemented as a binding, not a sha comparison: a `PROBE sha256=` line when present
   (must equal the committed bytes; a wrong sha is always refused), otherwise that
   instrument header (path must be the committed probe, version must equal
   `PROBE_VERSION`). When both are present both are validated (receipt `09-i` q6). The
   committed receipt passes through the header branch; the sha strict resolved is printed
   in every strict run (`CHECK strict probe sha256=f44b7283…`, the lane file's bytes, not
   the proposal's `b131e66e…` — the frozen text names the committed probe). Limitation:
   for the committed receipt the binding is path+version; a sha binding needs a receipt
   regenerated by a battery run, which this seat is forbidden to do.
3. **Strict's terminal line is `PREDICATE R65-C1 strict-pass|strict-fail`**, distinct from
   the default `pass|fail`, so a strict refusal is not misread as the default predicate
   failing (the default predicate passes on the fabricated fixture — that is M-1).
4. **TOOLCHAIN also requires the `CC`/`GCOV`/`BWRAP` banner lines.** The frozen clause
   "values equal the values the receipt itself carries" has no referent without them, so a
   receipt missing a banner is refused (`toolchain-banner-count`). The committed receipt
   carries all three; the fabricated fixture carries none.
5. **A missing reference file is `SETUP` exit 2, not exit 1.** If `<lane>/GRADER_REL` or
   `<lane>/PROBE_REL` cannot be read, strict cannot evaluate (exit 2), matching the
   counter's existing `SETUP receipt-missing` convention. Unreachable on this host: both
   files are present and hash to the frozen values (receipt `10-j`). A missing *receipt
   item* is always exit 1 with a named `CHECK defect:` line, as frozen.
6. **NOBIND is checked to the frozen minimum.** The fabricated fixture's bare
   `NOBIND Gx delta=0` lines satisfy that clause; the fixture is refused by the
   declaration, toolchain and probe-binding defects instead. Tightening NOBIND would
   exceed the frozen text.
7. **`--strict` without `--check-receipt` is a usage error** (`SETUP`, exit 2), so the flag
   can never silently change battery/selftest behaviour.
8. **No receipt-format change.** The emitter is untouched and `PROBE_VERSION` stays
   `r65-c1/1`: strict adds only a checker mode and selftest rows, so no emitted byte
   changes and the committed receipt stays valid. Bumping the version would have refused
   the committed receipt.
9. **Strict has a selftest.** Seven rows: `strict-valid-receipt` accepted; wrong `PROBE`
   sha, missing binding, mismatched `TOOLCHAIN`, drifted `VECTOR`, missing `NOBIND`, and a
   declared-fabricated comment each refused. Revision 1 shipped without them.
10. **Named limitation (from the claims, unchanged):** a declaration-free hand-copied
    receipt passes strict. This proposal refuses value-free, value-mismatched and
    literally-declared fabrication, not a hand-copied receipt.

## Not run

No R65 battery, no `--lane` run, no port 12355 listener, no network, no install. The only
processes started were the proposal's `--check-receipt`/`--selftest` invocations above.
