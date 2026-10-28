# C2RevCounterRule — frozen C2 counter attack

## Scope and result

Read the frozen claims file in full before examining the counter. Used the frozen counter at `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round52_c2_registry.py` without editing it. Fixture lanes and drivers were created only under `/fast/scratch/hyaku/kengaku-r52/C2RevCounterRule/`; scratch was removed after this report was written.

**Overall:** the counter detects the requested LOG-only advertisement and a missing registry heading when it can parse at least one advertised command. It has material vacuities in the advertised-universe extraction and self-test leg, and admits semantically empty rows. The clearest control failure is row deletion: a script advertised only by its own registry row can lose that row and the counter still passes.

## Findings by severity

### High — MISSING is blind to an advertised path class, and registry-row deletion can erase its own advertisement

**Evidence:** The counter's `CMD` pattern in `plans/round52_c2_registry.py` restricts `corpus/evidence/<dir>/<name>.py` segments to `[A-Za-z0-9_]+`; hyphens are excluded. Claims §C2 describes `<dir>` without that restriction. Fixture `E1b` advertised an existing `corpus/evidence/round52-foo/bar.py` in `SCORECARD.md`, supplied no registry row, and still returned `ADVERTISED total=0`, `MISSING 0`, all remaining legs 0, `PREDICATE R52-C2 pass`, exit 0. The same invisibility applies to the existing `corpus/evidence/round13-coverage/coverage_census.py` row: `collect()` found 46 parsed rows but only 44 registered scripts; its unresolved rows were the header and `coverage-census` entry. A broader scan of the specified files found existing advertised evidence scripts missed by `CMD`: `corpus/evidence/round11-power/recompute_r11.py`, `round12-ladder/recompute_r12.py`, `round13-coverage/coverage_census.py`, and `round9-fleet/test_harness.py`.

A separate counterexample uses the fact that `SKILL.md` is scanned for advertisements even though the registry is inside `SKILL.md`: an isolated lane with one instrument advertised only in its registry row passed (`ADVERTISED 1`, `MISSING 0`); deleting the row made both `ADVERTISED` and `REGISTERED` 0, and it still passed (`PREDICATE R52-C2 pass`, exit 0). The real lane has four scripts advertised only in that registry block by the counter's extraction: `plans/anchor_digest_check.py`, `plans/ledger_tip.py`, `plans/pkg_gate.py`, `plans/round39_c1_audit.py`. Deleting `package-gate` from a full copied lane reduced ADVERTISED 72→71 and REGISTERED 44→43, while MISSING stayed 28; that full-lane run still failed for unrelated existing defects, so the isolated passing fixture is the decisive row-deletion evidence.

**Leg verdict — MISSING: vacuous** for these paths/self-advertisements; it is sound for a literal supported `python3 plans/name.py` advertisement in the listed files when an independent advertisement remains after row deletion. Smallest tightening: implement the frozen path universe without the restrictive path regex, and exclude the registry block itself from advertisement discovery (or anchor the expected advertised population independently of the registry).

### High — SELFTEST-UNBACKED does not test whether a flag is accepted

`selftest_unbacked()` searches for flag-looking substrings in the self-test cell and then checks whether each substring occurs anywhere in a script's text. It does not inspect the script's accepted arguments. Fixture outcomes:

- B1: `plans/foo.py` accepts only `--lane`; cell claimed `--Selftest`. Uppercase first letter failed the case-sensitive `FLAG` regex, yielding `SELFTEST-UNBACKED 0` and predicate pass.
- B3: cell named the same script with valid `--lane` plus unsupported `--selftest`; `all(f not in body ...)` returned false because `--lane` occurs in the file, so the bogus flag was masked; predicate passed.
- B4: `--selftest` occurred only in a comment, while argparse did not accept it; the raw substring test treated it as backed; predicate passed.
- B5: cell named nonexistent `plans/nonexistent.py --selftest`; `if not path.exists(): return False` silently skipped it. ENTRY-MISSING remained 0 because that leg checks only the entry column; predicate passed.
- B6: cell named `foo.py --selftest` without a recognized path prefix; the script matcher found no script, so it skipped the check; predicate passed.

Fixture B2 named two scripts and the self-test leg skipped it as ambiguous; MISSING then failed because the second command also advertised `plans/bar.py` without a row. The frozen claims explicitly exclude ambiguous cells, so this is not by itself an implementation divergence; it illustrates that ambiguity can avoid this leg.

There is a live counterexample at the base tip: the counter reports `SELFTEST-UNBACKED 1` for `order-check`. Its cell says “no `--selftest` in the script” and describes external falsifiers, including `plans/round40_c1_verify.py`; the matcher selects that different script and finds the cell's `--claims`, `--receipt`, and `--selftest` strings absent from its body. The entry script is `plans/order_check.py`; its cell explicitly says the instrument has no self-test, a case the frozen rule says is accepted. This is a false attribution/negative-wording failure, not evidence that the entry script's command-line flags were checked.

**Leg verdict — SELFTEST-UNBACKED: vacuous/unsound.** It catches the narrow case where exactly one recognized script is named and every flag-like string is absent from its source bytes, but that is not equivalent to “the script does not accept the flag.” Smallest tightening: bind the check to the row's entry script, require exactly one flag as the frozen rule states, and inspect parsed/declared accepted arguments rather than source-text substring presence; explicitly accept a no-self-test declaration.

### Medium — INCOMPLETE accepts placeholder-only content

Fixture A used one row per advertised script with a real entry command and `x` in every other cell. It returned `MISSING 0`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 0`, `PREDICATE R52-C2 pass`, exit 0. Thus non-empty placeholders in verdict map, self-test, pinned values, scope, owner, and name are treated as complete. Literal `x` in all eight cells instead produced `MISSING 1` (entry cell could not resolve), so the passing result requires the necessary entry command; the other seven cells can still be vacuous. Fixture E8's `-` in the first cell was treated as a separator and the row was skipped, producing MISSING 1.

**Leg verdict — INCOMPLETE: vacuous** as a check of truthful/informative rows (sound only for detecting stripped-empty cells). Smallest tightening: reject placeholder-only values and validate the expected content of critical columns, at minimum a meaningful verdict map and an explicit self-test/no-self-test value.

### Medium — ENTRY-MISSING validates only the entry-cell script

Fixture B5 passed with an entry script that existed but a self-test cell naming a nonexistent script. The self-test check silently returns false for a missing path, and ENTRY-MISSING never examines that cell. The pinned-values and other path references are likewise not checked by this leg.

**Leg verdict — ENTRY-MISSING: vacuous** for script references outside the entry column; sound for a recognized entry-column path that is missing. Smallest tightening: treat an unresolved self-test script as unbacked and validate path references in the row's path-bearing fields (or constrain those fields to a declared syntax).

## Requested fixtures (aggregate outcome)

| Fixture | Observed result | Per-leg interpretation |
|---|---|---|
| (a) Eight-cell rows with entry command plus placeholder `x` values | All four counts 0; predicate pass. Literal all-`x` including entry fails MISSING because it registers no script. | INCOMPLETE is vacuous for placeholder content; MISSING works only when its command parser recognizes the entry. |
| (b) Unsupported self-test spelling | Uppercase flag, mixed valid+bogus flags, comment-only flag, missing script, and unrecognized bare script path all pass SELFTEST-UNBACKED; one two-script case skips as ambiguous. | SELFTEST-UNBACKED is vacuous/unsound as above. |
| (c) Script advertised only in `LOG.md`, with no row | `ADVERTISED total=2`, `MISSING 1` (`plans/logonly.py`), predicate fail, exit 1. | MISSING is sound for this exact spelling/source; `LOG.md` is included in `SELF_FILES`. |
| (d) Registry heading missing | With an independently advertised `plans/foo.py`, `MISSING 1`, predicate fail, exit 1; INCOMPLETE, ENTRY-MISSING, and SELFTEST-UNBACKED are 0 because there are no parsed rows. | MISSING is sound for a recognized advertisement; the other row-dependent legs are vacuous. With zero recognized advertisements and no heading/table, all four are 0 and the predicate passes. |

For (d), a renamed heading with a row and a 9-column table also failed via `MISSING 1`; this is fail-closed but reports no distinct “missing/malformed registry” diagnostic. Smallest tightening: require the heading/table and a recognized header as explicit setup conditions, and require a non-empty expected advertisement population.

## Per-leg summary

| Leg | Verdict | Smallest tightening |
|---|---|---|
| MISSING | **Vacuous** for excluded command/path spellings and self-advertisements; sound for recognized independent advertisements. | Match the frozen universe (including hyphenated evidence directories) and do not use registry rows as the sole advertisement source. |
| INCOMPLETE | **Vacuous** for non-empty placeholders. | Reject placeholder values and validate critical cell semantics. |
| ENTRY-MISSING | **Vacuous** outside the entry cell (e.g. missing self-test script). | Validate all path-bearing fields; missing referenced self-test scripts must not be silently accepted. |
| SELFTEST-UNBACKED | **Vacuous/unsound**: regex and raw substring checks are not acceptance checks; multiple flags dilute; negative claims can false-positive. | Bind to entry script; require exactly one flag; check declared/parsed CLI options and accept explicit no-self-test statements. |

## Verification and commands

No `lsp` device was available in the provided tool inventory, so semantic references/definition/diagnostics were unavailable; the counter source was read directly and fixture behavior was executed against that unchanged file. No tools were installed or updated.

Measured on the lane tree read at the time of this review (working-tree HEAD reported `1315234bdc8024499d943f0483dcb51fb5e4a618`; claims' frozen base tip is `30801b479e3418c11089b8586178b6960216f364`):

- Frozen counter lane run: `ADVERTISED total=72`, `REGISTERED total=44 rows=46`, `MISSING 28`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 1` (`order-check`), predicate fail, exit 1.
- Fixture A: 2 advertised / 2 registered, all four defects 0, predicate pass, exit 0.
- Fixture C: 2 advertised / 1 registered, MISSING 1, predicate fail, exit 1.
- Fixture D1/D2/D3: MISSING 1, row-dependent counts all 0, predicate fail, exit 1.
- E1b hyphenated evidence path without row: ADVERTISED 0, all counts 0, predicate pass, exit 0.
- Self-advertisement row deletion: row present → ADVERTISED 1 / REGISTERED 1 / pass; row deleted → ADVERTISED 0 / REGISTERED 0 / pass.
- Duplicate row names with two distinct scripts: ADVERTISED 2 / REGISTERED 2, all four counts 0, predicate pass.
- Zero recognized advertisements and missing registry heading: all four counts 0, predicate pass.
- Counter's embedded self-test, run with `--lane fixtures3/row_deletion_blind --selftest`: `SELFTEST cases=3 failures=0`, exit 0. Its source has only clean, missing-row, and incomplete-cell cases; it does not exercise ENTRY-MISSING or SELFTEST-UNBACKED.
- Broad-vs-frozen-regex scan over the named self-assessment files found four existing corpus/evidence scripts missed by the counter's regex (listed above); two hyphenated `.py` basenames were found under deeper evidence subdirectories, outside the frozen depth-2 path form.

Exact principal commands executed:

```sh
# Read frozen source and claims (via read tool)
read /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-52-claims.md
read /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round52_c2_registry.py

# Base counter
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/round52_c2_registry.py --lane .

# Create and run scratch fixtures
mkdir -p /fast/scratch/hyaku/kengaku-r52/C2RevCounterRule/tmp
cd /fast/scratch/hyaku/kengaku-r52/C2RevCounterRule && python3 mkfixtures.py
cd /fast/scratch/hyaku/kengaku-r52/C2RevCounterRule && python3 mkfixtures2.py
# An inline Python driver created fixtures3 and ran the frozen counter on each.

# Correct embedded-selftest invocation
cd /fast/scratch/hyaku/kengaku-r52/C2RevCounterRule && TMPDIR=/fast/scratch/hyaku/kengaku-r52/C2RevCounterRule/tmp python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round52_c2_registry.py --lane fixtures3/row_deletion_blind --selftest
```

An earlier attempted embedded-selftest invocation from the scratch root without `--lane` returned setup exit 2 (`SETUP no SKILL.md under ...`); rerunning with a fixture lane succeeded. An earlier full-copy row-deletion probe selected the wrong row name (`pkg-gate`) and removed zero lines; it was corrected to `package-gate`, after which the full-lane measured counts are reported above. No lane/counter files were edited.

## Produced files

- `/fast/scratch/hyaku/kengaku-r52/C2RevCounterRule/mkfixtures.py` — fixture builder; removed before yield.
- `/fast/scratch/hyaku/kengaku-r52/C2RevCounterRule/mkfixtures2.py` — second fixture builder; removed before yield.
- `/fast/scratch/hyaku/kengaku-r52/C2RevCounterRule/fixtures/` and `/fixtures2/` — fixture lanes; removed before yield.
- `/fast/scratch/hyaku/kengaku-r52/C2RevCounterRule/fixtures3/` — fixture lanes; removed before yield.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2RevCounterRule.md` — detailed findings.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2RevCounterRule/report.md` — this report copy.
