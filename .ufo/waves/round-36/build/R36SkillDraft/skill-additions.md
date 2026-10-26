# SKILL.md additions — round 36 (R36SkillDraft, wave 1)

Draft only. The L1 integrates; this seat wrote nothing outside `.ufo/waves/round-36/build/R36SkillDraft/`.
Insertion points: registry rows after SKILL.md:573 (the `sources-adopt` row, last table row); addendum
paragraph after SKILL.md:586 (after the round-26 addendum paragraph); new section appended after
SKILL.md:704 (end of file).

## 1. Registry rows — insert after SKILL.md:573, inside the `## Gate/probe registry` table

| `package-gate` [if landed] | gate | `python3 plans/pkg_gate.py package --root DIR --spec plans/pkg-spec-r35.json [--rerun] [--require-clean-tree]` (subcommands `d4-line --file F --spec SPEC`, `d5-line --file F --capture-dir D --spec SPEC`) | `0` accept · `1` reject (a hardened check fails) · `2` usage/setup (unreadable spec/root, unevaluable) | `python3 plans/round36_c1_verify.py --lane .` (14-fixture battery: P0 genuine, P1–P7 junk packages, L1/L4 genuine and L2/L3/L5/L6 labelled-but-false lines; green means `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0`) | `plans/pkg-spec-r35.json` sha256 `e085b435…` pins rows S105–S107 with their capture digests, receipt `corpus/evidence/round35/tb2-grader-probe.txt` sha256 `2359d906…`, and three frozen instruments (`tb2_grader_probe.py`, `round35_c1_verify.py`, `defect_ledger.py`); `corpus/evidence/round35/tb2-eval/SHA256SUMS` | reads ROOT + spec; `--rerun` re-executes the package's own `probe_cmd` inside ROOT and byte-compares the receipt to its pinned sha256; `--require-clean-tree` reads `git -C ROOT ls-files --others --exclude-standard`; no network, no commit, no lane write | kengaku |
| `round36-c1-battery` [if landed] | gate | `python3 plans/round36_c1_verify.py --lane .` (`--legacy`: the seven junk fixtures against the round-35 counter of record) | `0` C1 predicate holds (`FIXTURES … false_green=0 false_red=0 unevaluated=0`, `rows=4 closed=4 observed_pass=4 mismatches=0`, `PREDICATE C1 pass`) · `1` any fixture wrong or unevaluated, any ledger row disagreeing with its check, predicate fail · `2` usage | none declared beyond itself (the battery is the self-test; `--legacy` is the pre-fix control) | `plans/round36_c1_verify.py` sha256 `d7c3687c…`; `plans/pkg-spec-r35.json` sha256 `e085b435…`; `corpus/defects-round35.jsonl` four rows R35-D1…D4, each closed only while its check passes | none — fixtures are index-only git repos under `mktemp`, built from committed round-35 bytes; reads `git ls-files --others` and `git ls-tree`; no network | kengaku |
| `regex-log-probe` | probe | `python3 plans/regex_log_probe.py --lane .` (`--dry` prints the 24 frozen cases, regexes and predictions without running the grader) | `0` all 24 predictions matched · `1` a mismatch (`match=NO` on the differing case) · `2` grader digest refused (`REFUSE grader digest …`) | `python3 plans/round36_c2_verify.py --lane .` W5 (probe digest, fresh run byte-equal to the receipt, summary line `cases=24`; red until the C2 entry lands) | grader `corpus/evidence/round36/tb2-regex-log/test_outputs.py` sha256 `345c3bd0…` pinned in the probe; probe digest `d58194c8…` pinned in `plans/round36_c2_verify.py` (amendment 1); receipt `corpus/evidence/round36/regex-log-probe.txt` | writes only its own `mktemp` dir and monkeypatches the grader's `Path` so `/app/regex.txt` resolves there; imports the captured grader with `importlib`; no network, no model, never the live `/app` | kengaku |

## 2. Addendum paragraph — insert after SKILL.md:586 (after the round-26 addendum)

Round-36 registry addendum: `package-gate` and `round36-c1-battery` are `[if landed]` — at wave-1 draft
`plans/pkg_gate.py` is absent, so both rows record the frozen contract from `plans/round36_c1_verify.py`'s
docstring, not a green run: the current tree prints `FIXTURES total=14 false_green=0 false_red=0
unevaluated=14`, `rows=4 closed=0 observed_pass=0 mismatches=0`, exit 1
(`.ufo/waves/round-36/claims/control-c1-nothing.txt`). The gate may not recognise a fixture by name, path
or marker string — the battery's fixture roots are `mktemp` dirs named `k36-P0…k36-P7`, so a path check
would pass the battery while hardening nothing, which is what the wave-2 mutation seats attack. No row
here claims a live host probe or a network call: `regex-log-probe` imports only committed capture bytes
and its receipt is byte-reproducible (fresh run `cmp`-equal, 2026-10-25).

## 3. New section — append after SKILL.md:704 (end of file)

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
