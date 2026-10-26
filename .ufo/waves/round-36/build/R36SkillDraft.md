# R36SkillDraft — SKILL.md additions for round 36 (wave 1, scribe)

Seat: R36SkillDraft. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (tip `f9efce3`, on top of
freeze `3241b86`, amendment 1 `acbda2f`). Read first: `plans/round-36-claims.md` (full), `SKILL.md`
registry table + task-spec observability sections, `plans/round36_c1_verify.py`,
`plans/round36_c2_verify.py`, `plans/regex_log_probe.py`, `plans/pkg-spec-r35.json`, both control
receipts, the regex-log capture set and receipt.

## Behavior

Drafted, not applied: **3 registry rows**, **1 addendum paragraph**, **1 new section** for `SKILL.md`.
Nothing in the lane was edited. The draft of record is
`.ufo/waves/round-36/build/R36SkillDraft/skill-additions.md`; it is reproduced verbatim below so the L1
can paste without reading the scratch file.

Anchors (current line numbers; re-check after any earlier insertion):
- rows go after `SKILL.md:573` (the `sources-adopt` row, last row of the table that starts at `:562`);
- addendum paragraph after `SKILL.md:586` (end of the round-26 addendum; blank line 587, next heading
  `## Production checklist — running an eval` at 588);
- new section appended after `SKILL.md:704` (last line of the file: the round-29 section's final
  sentence, `need no filename check.`).

`[if landed]` marking: `plans/pkg_gate.py` does not exist at this tip
(`ls plans/pkg_gate.py` → `No such file or directory`), and `corpus/lessons/round-36.md` is absent, so
both C1 rows carry `[if landed]` and the addendum states that the rows record the frozen counter
contract, not a green run. `regex-log-probe` is landed and executed (evidence below), so it carries no
marker. One dependency inside its self-test cell is stated in prose rather than marked: C2's W5 is red
until `corpus/knowledge/tb2-regex-log-grader.md` lands.

## Draft (verbatim)

### Registry rows — after SKILL.md:573

```
| `package-gate` [if landed] | gate | `python3 plans/pkg_gate.py package --root DIR --spec plans/pkg-spec-r35.json [--rerun] [--require-clean-tree]` (subcommands `d4-line --file F --spec SPEC`, `d5-line --file F --capture-dir D --spec SPEC`) | `0` accept · `1` reject (a hardened check fails) · `2` usage/setup (unreadable spec/root, unevaluable) | `python3 plans/round36_c1_verify.py --lane .` (14-fixture battery: P0 genuine, P1–P7 junk packages, L1/L4 genuine and L2/L3/L5/L6 labelled-but-false lines; green means `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0`) | `plans/pkg-spec-r35.json` sha256 `e085b435…` pins rows S105–S107 with their capture digests, receipt `corpus/evidence/round35/tb2-grader-probe.txt` sha256 `2359d906…`, and three frozen instruments (`tb2_grader_probe.py`, `round35_c1_verify.py`, `defect_ledger.py`); `corpus/evidence/round35/tb2-eval/SHA256SUMS` | reads ROOT + spec; `--rerun` re-executes the package's own `probe_cmd` inside ROOT and byte-compares the receipt to its pinned sha256; `--require-clean-tree` reads `git -C ROOT ls-files --others --exclude-standard`; no network, no commit, no lane write | kengaku |
| `round36-c1-battery` [if landed] | gate | `python3 plans/round36_c1_verify.py --lane .` (`--legacy`: the seven junk fixtures against the round-35 counter of record) | `0` C1 predicate holds (`FIXTURES … false_green=0 false_red=0 unevaluated=0`, `rows=4 closed=4 observed_pass=4 mismatches=0`, `PREDICATE C1 pass`) · `1` any fixture wrong or unevaluated, any ledger row disagreeing with its check, predicate fail · `2` usage | none declared beyond itself (the battery is the self-test; `--legacy` is the pre-fix control) | `plans/round36_c1_verify.py` sha256 `d7c3687c…`; `plans/pkg-spec-r35.json` sha256 `e085b435…`; `corpus/defects-round35.jsonl` four rows R35-D1…D4, each closed only while its check passes | none — fixtures are index-only git repos under `mktemp`, built from committed round-35 bytes; reads `git ls-files --others` and `git ls-tree`; no network | kengaku |
| `regex-log-probe` | probe | `python3 plans/regex_log_probe.py --lane .` (`--dry` prints the 24 frozen cases, regexes and predictions without running the grader) | `0` all 24 predictions matched · `1` a mismatch (`match=NO` on the differing case) · `2` grader digest refused (`REFUSE grader digest …`) | `python3 plans/round36_c2_verify.py --lane .` W5 (probe digest, fresh run byte-equal to the receipt, summary line `cases=24`; red until the C2 entry lands) | grader `corpus/evidence/round36/tb2-regex-log/test_outputs.py` sha256 `345c3bd0…` pinned in the probe; probe digest `d58194c8…` pinned in `plans/round36_c2_verify.py` (amendment 1); receipt `corpus/evidence/round36/regex-log-probe.txt` | writes only its own `mktemp` dir and monkeypatches the grader's `Path` so `/app/regex.txt` resolves there; imports the captured grader with `importlib`; no network, no model, never the live `/app` | kengaku |
```

### Addendum — after SKILL.md:586

```
Round-36 registry addendum: `package-gate` and `round36-c1-battery` are `[if landed]` — at wave-1 draft
`plans/pkg_gate.py` is absent, so both rows record the frozen contract from `plans/round36_c1_verify.py`'s
docstring, not a green run: the current tree prints `FIXTURES total=14 false_green=0 false_red=0
unevaluated=14`, `rows=4 closed=0 observed_pass=0 mismatches=0`, exit 1
(`.ufo/waves/round-36/claims/control-c1-nothing.txt`). The gate may not recognise a fixture by name, path
or marker string — the battery's fixture roots are `mktemp` dirs named `k36-P0…k36-P7`, so a path check
would pass the battery while hardening nothing, which is what the wave-2 mutation seats attack. No row
here claims a live host probe or a network call: `regex-log-probe` imports only committed capture bytes
and its receipt is byte-reproducible (fresh run `cmp`-equal, 2026-10-25).
```

### Section — append after SKILL.md:704

```
## TB2 regex-log grader — round36

Before citing the pinned TB2 `regex-log` scorer, run `python3 plans/regex_log_probe.py --lane .`: exit `0`
means all 24 frozen predictions matched, `1` a mismatch, `2` the capture no longer hashes to `345c3bd0…`
(TB2 `2fd12b8`, rows S108–S110). The grader compiles `/app/regex.txt` and applies `re.findall(…,
re.MULTILINE)` to one fixed 25-line log, asserting exact equality with nine dates
(`corpus/evidence/round36/tb2-regex-log/test_outputs.py:34-90`); the receipt's summary line
(`corpus/evidence/round36/regex-log-probe.txt:26`) reads `cases=24 observed_pass=8 observed_fail=16
mismatches=0`, and `--dry` prints predictions without running anything, so it is not evidence.

Observed enforcement is narrower than the instruction. Enforced: last date per line (`:4`), a valid IPv4
anywhere in the line (`:17`), octets 0-255 (`:6`), months 01-12 (`:8-9`), days 01-31 (`:10-11`),
letter-adjacency on both date and IP (`:12-13,15-16`), and the file/compile/findall mechanics including an
extra capture group (`:20-23`) and a padded pattern file (`:24`). Not enforced: a literal alternation of
the nine expected dates passes with no pattern logic (`:18`); leading-zero octets pass though the
instruction forbids them (`:7`, `instruction.md:4`); digit-adjacent dates — the instruction's own
`1134-12-1234` example — are unobserved, so a letters-only boundary passes (`:14`, `instruction.md:6`);
year widths other than four are unobserved (`:19`); month-length validity is unobserved because the
Feb 30 and Apr 31 lines sit on invalid-IP lines (`:2`, `test_outputs.py:65,67`); and a regex that rejects
Feb 29 still passes, so the instruction's permission (`instruction.md:3`) is untested (`:25`).

What to do: read `tests/` before trusting a pass, and treat a green fixed log as evidence about that log
only — never as evidence of instruction compliance. `test.sh:26-28` writes reward 1/0 from pytest's exit
alone, so a passing submission can be a hardcoded alternation.
```

Receipt pointers in the section are bare `:N` because the file is named two sentences earlier; the
instruction.md and test_outputs.py pointers are capture-relative (they sit beside the receipt under
`corpus/evidence/round36/tb2-regex-log/`). If the L1 prefers absolute pointers, replace `instruction.md`
→ `corpus/evidence/round36/tb2-regex-log/instruction.md` and `test_outputs.py` → the same prefix.

## Evidence (every number, with its command)

Instruments and digests — `sha256sum`:

```
d7c3687c09ed4c8a09a9d7c63efa9232c2b1aff8ffb229fb8a0505578317df73  plans/round36_c1_verify.py
983ed65c885990f6d783abffbe21b70ab5414431b88a3b27d52fdbda65d67120  plans/round36_c2_verify.py
e085b43505c9848c8d19eb52c52fec1a3282dac3c5b436f59320e95e5c299fc4  plans/pkg-spec-r35.json
d58194c817685546a945e8b116588a52590fc944e6218ac40218381a376519bc  plans/regex_log_probe.py
acd7d38dca3a982d22900ca034c50aa3d22817395273bbc62b5665b1913040d0  plans/tb2_grader_probe.py
05a6137d22e2cae220a79b642ec3aeab49400c113ee9d1ebb202b5d443a286f7  plans/round35_c1_verify.py
4e386677b48fd66e1a19a7459ab5e5359139e282e0968afa2cfd2395768d763d  plans/defect_ledger.py
439101fa2eac0e79ebec088ab47d9fc4481df0ec12d0ebc6c3475319d426a2be  corpus/evidence/round36/regex-log-probe.txt
```

- `plans/pkg-spec-r35.json` pins exactly the three frozen instruments above plus the receipt digest
  `2359d9067906f59d2c55b5802603d1ef45c376f653ad9997de1ef7da412b25b8`, checksummed directly
  (`sha256sum corpus/evidence/round35/tb2-grader-probe.txt` → same value). The spec's `rows` block
  (S105–S107) and `entry_rules` supply the quote/teaches thresholds quoted in the task.
- Probe CLI and roll-up — `python3 plans/regex_log_probe.py --lane .` from `/tmp`:
  `rc=0`, last line `cases=24 observed_pass=8 observed_fail=16 mismatches=0`, and
  `cmp` against `corpus/evidence/round36/regex-log-probe.txt` → `BYTE-EQUAL`.
  Exit map confirmed in source: digest refusal `return 2` at `plans/regex_log_probe.py:141-142`,
  mismatch `return 0 if mism == 0 else 1` at `:160`; flags are `--lane`, `--dry` only (`:133-134`).
- C1 current state — `python3 plans/round36_c1_verify.py --lane .` → exit 1:
  `FIXTURES total=14 false_green=0 false_red=0 unevaluated=14`,
  `R35-D1 … tip_package_rc=None`, `R35-D3 … committed_nested_wave_paths=21`,
  `R35-D4 … round-36 lesson absent; recount 13 + 23 + 1 = 37 vs stated denominator 38`,
  `rows=4 closed=0 observed_pass=0 mismatches=0`, `PREDICATE C1 fail`. (Identical FIXTURES/ledger
  verdicts to `.ufo/waves/round-36/claims/control-c1-nothing.txt`; `untracked_anywhere` reads 768 now
  versus 12 at freeze because wave-1 build dirs are uncommitted — see Findings.)
- C2 current state — `python3 plans/round36_c2_verify.py --lane .` → exit 1: `W1 ok`, `W2 DEFECT S108
  present 0 times`, `W3 DEFECT entry absent`, `W4 DEFECT index row absent or missing S108/S109/S110`,
  `W5 DEFECT entry absent`, `W6 ok`, `checks=6 defects=4`, `PREDICATE C2 fail`. So the `regex-log-probe`
  row's self-test is currently red for a reason outside the probe (entry not landed), as worded in the row.
- Grader structure behind the section's line pointers: `sample_logs` at
  `corpus/evidence/round36/tb2-regex-log/test_outputs.py:34`, 25 entries in `:34-69` (`awk 'NR>=34 &&
  NR<=69 && /^        "/' … | wc -l` → `25`), Feb 30 at `:65`, Apr 31 at `:67`, `expected_dates` at
  `:71-81`, `re.findall(pattern_text, log_text, re.MULTILINE)` at `:87`, equality assert at `:90`,
  `/app/regex.txt` at `:21`. Instruction: Feb-29 permission `instruction.md:3`, no-leading-zeros `:4`,
  `1134-12-1234` example `:6`, alphanumeric-adjacency rule `:7`. Reward: `test.sh:26` echo 1, `:28`
  echo 0.
- Receipt pointers used in the section are the file's own line numbers
  (`grep -n "case=" corpus/evidence/round36/regex-log-probe.txt`): `:2` lenient-days pass, `:4`
  first-date-only fail, `:6` unbounded octets fail, `:7` leading-zeros pass, `:8-9` month 13/00 fail,
  `:10-11` day 32/00 fail, `:12-13` date boundaries fail, `:14` letters-only boundary pass, `:15-16` IP
  boundaries fail, `:17` IP-anywhere pass, `:18` hardcoded alternation pass, `:19` year-width pass,
  `:20-23` empty/invalid/absent/extra-group fail, `:24` padded pass, `:25` Feb-29-rejecting pass, `:26`
  summary. All 24 cases are `match=yes`, so every "enforced / not enforced" clause cites an observed
  verdict, not a reading.
- Traceability: `git ls-files` confirms the probe, both counters, the spec, the ledger, the round-36
  capture set and both receipts are tracked at `f9efce3`; `git status --porcelain SKILL.md plans corpus`
  is empty after the draft (only `.ufo/waves/round-36/{build,integrate}/` and `build.ready` are
  untracked).

## Gates

- Not run: nothing required a gate for this seat's deliverable. The C1 battery/C2 counter were run only
  to record the state the draft describes; their pass/fail is not my acceptance criterion.
- Not run and not claimed: exit `1` and exit `2` of `regex-log-probe` (no mismatch exists by design; exit
  2 would require tampering the capture, which the lane bounds forbid). Their maps are read from source,
  not observed — the row says nothing beyond the source contract.
- Not claimed on `package-gate`: its `0/1/2` behaviour, `--rerun` byte-comparison, clean-tree rule,
  d4/d5 checks. The script is absent; every clause in those two rows is the frozen requirement from
  `plans/round36_c1_verify.py`'s docstring and the claims file, and is marked `[if landed]`.

## Touched surfaces

- Wrote: `.ufo/waves/round-36/build/R36SkillDraft.md` (this report) and
  `.ufo/waves/round-36/build/R36SkillDraft/skill-additions.md` (draft). Created
  `.ufo/waves/round-36/build/R36SkillDraft/`.
- Lane files read, none modified: `SKILL.md`, `plans/*`, `corpus/SOURCES.md`, `corpus/knowledge/` (entry
  absent), `corpus/evidence/round36/**`, `corpus/evidence/round35/**`, `corpus/defects-round35.jsonl`,
  `.ufo/waves/round-36/claims/*`.
- No commit, no `git add`, no jj command, no fixture clone, no network fetch.

## Findings

1. **Draft-time registry rows cannot be verified past the contract.** `plans/pkg_gate.py` is absent, so
   the two C1 rows are requirements-only. If the L1 hands the rows to review before the gate lands, the
   `[if landed]` marker plus the addendum is the whole defence; do not drop the marker when the gate
   lands — replace it with the observed battery line from that seat's receipt.
2. **The C1 counter is now red for a working-tree reason unrelated to the gate.**
   `untracked_anywhere=768` (vs 12 at freeze) because `.ufo/waves/round-36/build/` is uncommitted. The
   claims' predicate is measured "on a clean clone of the landing tip", so any L1 run in the live tree
   will see R35-D2 fail for as long as wave scratch is uncommitted. This is a measurement-procedure
   constraint on the C1 claim, not a defect in the counter — but an unwary integrator could misread it.
3. **Stale digest hazard in the claims block.** `plans/round-36-claims.md`'s "Frozen digests" block still
   lists `plans/regex_log_probe.py` as `34ab5dfd…`; amendment 1 moved it to `d58194c8…` and the C2
   counter's `PROBE_SHA256` constant to the same value (`plans/round36_c2_verify.py:41`). The draft pins
   `d58194c8…`. Anyone copying the frozen-digest block into docs would reintroduce the pre-amendment pin.
4. **The section's strongest claim is the cheapest to attack, and it is observed.** "A literal
   alternation of the nine dates passes" is receipt `:18` (`hardcoded-expected-dates predicted=pass
   observed=pass`), and the same fixed log is visible in `test_outputs.py:34-69`, so the claim does not
   depend on any inference about hidden test data.
5. **Two registry rows would be the first in the table whose exit map is `0/1/2` with `2` = usage/setup
   for a *gate* of this shape** (`sources-adopt` uses `2..9` for semantic refusals). Consistent with the
   frozen docstring ("other = unevaluated"), and the battery treats any non-`0/1` as `unevaluated`, so
   the row and the counter agree on what exit 2 means.

## Limits

- The section cites `tests/` visibility as advice ("read `tests/` before trusting a pass"). Whether a TB2
  agent can see `/tests` at solve time is not established by any committed byte here; `test.sh` copies
  the grader into the image at grading time and the instruction does not mention it. I did not assert
  access either way.
- The claims' disclosed reading of `solve.sh` is not restated in the section: the probe docstring
  (`plans/regex_log_probe.py:3-9`) discloses it, and the section's numbers are all observed, so nothing
  in the draft depends on the oracle.
- The draft does not touch `corpus/README.md`, `corpus/SOURCES.md`, `LOG.md`, `PROVINCE.md`,
  `SCORECARD.md` or the knowledge entry — those are C2's surfaces and other seats' write scope.
- `plans/round36_c2_verify.py` digest `983ed65c…` differs from the claims' frozen `f70e6d3a…`; that is
  amendment 1's one-line pin move, not a wave-1 change (the file is unchanged since `acbda2f`).

VERDICT: skill-drafted-3-rows
