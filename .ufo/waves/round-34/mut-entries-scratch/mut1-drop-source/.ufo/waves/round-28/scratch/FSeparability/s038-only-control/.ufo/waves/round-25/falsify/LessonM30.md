ATTACKS: lesson row M30 (`corpus/lessons/round-25.md:21`) — every cited pointer, the diagnosis, the class, and the named red run. Pristine tree: `git archive 8ea41f9ed | tar -x -C /tmp/k25w2-LessonM30`; mutations only there.

POINTERS — resolve.
- `PowerTableExec.md:38` (F2) and `CpReferenceExec.md:46` (F4) are committed at 8ea41f9ed (`git ls-tree`). Both state lo(16,16)=0.794092785792, that the pre-reg's 0.7940 is truncated, and that rounding gives 0.7941.
- The mistake is live at tip: `plans/round-25-claims.md:43` still reads "n=16 → 0.7940; n=17 → 0.8049"; identical at line 43 in `git show 3f371d2`, `710409f`, `8ea41f9ed`.

DIAGNOSIS — agree to 60 digits.
- Python 3.14.8 `Decimal` (prec 60): 0.025^(1/16)=0.79409278579217725756014; ROUND_DOWN 4dp = 0.7940, quantize 4dp = 0.7941. "Truncated" is exact; no other bound in evidence gives 0.7940 (one-sided 0.05^(1/16)=0.829250, Wilson 0.812500).
- 0.025^(1/17)=0.80493567703090676890403 → 6dp 0.804936. Exact tail test: 8^17=0.02251799813685248 ≤ 0.025 < 0.0281474976710656=8^16 ⇒ min n=17. `power_table.py --summary` → `power_ask_min_n=17`; `power_table.tsv:70` `power_ask_n17 PASS`; `cp_reference.tsv:154,172` agree.
- No declared truncation/precision convention in the claims doc (`grep -n 'truncat\|4 dp\|decimal\|precision'` hits only "round-24" prose), so this is an error, not a formatting mode.

CLASS — agree.
- `number-drift` is in the fleet vocabulary (`CORPUS.md:173-176`) and matches M25's use for a stale numeric cell; not `reference-drift` (a pointer) or `survivor` (no verdict rode on it).

CAPTURED-BY — agree with `none`.
- The definition is a QUALITY criterion/protocol rule. R12 covers SCORECARD/SHONEN/PROVINCE/README only (`plans/state_check.py:3-9`; `QUALITY.md:105`); Q10 is knowledge-entry admission. No rule re-reads numbers in `plans/*.md`. Wave-1 seats caught it (ConnKotoba:43; PowerTableExec F2) while SkillRuleScout:40 and TallyR09:39-40 called it a "match" — seats, not the named criterion.

FIX / RED RUN — disagree; no red run is named and none goes red on the drifted artifact.
- The cell names no command, exit code, or committed red-before transcript, against `corpus/lessons/round-25.md:9-10` ("A fix counts only once shown able to fail; the red run is named in each row") and `CORPUS.md:180-183`.
- The named fixtures are self-checks: `cp_reference.py --verify` green (`certified=1640 … failures=0`); replacing lo(16,16) with 0.794000000000 exits 1 (`failures=2`). `power_table.py --check` green; replacing line 8's 0.794093 with 0.794000 exits 1 ("differs … at line 8"). They can fail, but no command compares them to `plans/round-25-claims.md:43`: grep finds only comments; `power_table.py:49` hardcodes `POWER_ASK` and never parses the doc. A red run for the doc number does not exist.
- The wrong value is uncorrected at tip: no appended `## Amendment 2`, although `plans/round-25-claims.md:5` says amendments are appended, never edited in place, and M28 (same doc, same table) used Amendment 1. `plans/attrib_calibration.py:689-692,697` deliberately pins 0.7940 as the `cp_lo_trunc4` anchor — defensible as a truncation control, but it means "exact values" is not the whole landed state.
- Minor: the row calls 0.794093 "exact"; it is the 6-dp rounding of 0.794092785792 (`cp_reference.tsv:154`). No effect on anything.

VERDICT: PARTIAL — pointers, diagnosis, class, captured-by, and verdict-unchanged all reproduce; the fix column names no red run, the named fixtures never inspect the drifted document, and 0.7940 is still live at tip with no appended amendment.
Installs: none (python3.14 stdlib; read-only git; no pacman/uv/network).
