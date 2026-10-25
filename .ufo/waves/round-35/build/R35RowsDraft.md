# R35RowsDraft — scribe report (kengaku round 35 wave 1)

Seat: R35RowsDraft (scribe, leaf — no subagents, no background jobs).
Task: draft registry rows S105–S107 for `corpus/SOURCES.md` (11-column schema) + lesson
`## Gate` source block + census validation in scratch.

## Behavior

- Read the frozen claims (`plans/round-35-claims.md`, freeze commit 11d6453) — C1 lists the
  three sources at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, kind code/docs, tier A,
  scope = maintainer's task-grader code for this one task, opened 2026-10-25, recheck 180d,
  used-by `corpus/knowledge/tb2-protein-assembly-grader.md`.
- Read the SOURCES contract (fleet `CORPUS.md` §SOURCES, frozen v1) and the current registry
  (header line 21, last 5 rows = S103–S107; `corpus/SOURCES.md:118-122`).
- **State note:** the lane's `corpus/SOURCES.md` already carries S105–S107 at lines 120–122
  (end of the Registry table, immediately before `## Paths` at line 123), opened 2026-10-25,
  status mined, recheck 180d. My draft below is byte-identical to those integrated rows; the
  scratch validation exercises exactly that state.
- Verified the pinned captures (byte-identical, `corpus/evidence/round35/tb2-eval/`):
  `sha256sum -c SHA256SUMS` → all 6 files OK, including the three source files
  (test_outputs.py 44a05a…, test.sh 9ede466…, instruction.md 1bb2af… — all three sha256
  values match the frozen claim and the row anchors).
- Verified each row's located quote with `grep -nF` against the tb2-eval captures:
  - S105: `grep -nF 'assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx, ('`
    → `42:    assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx, (` (9 words)
  - S106: `grep -nF 'echo 1 > /logs/verifier/reward.txt'` → `27:  echo 1 > /logs/verifier/reward.txt`
    (4 words); `grep -nF -- '-w biopython==1.85'` → `21:  -w biopython==1.85 \`
  - S107: `grep -nF 'The GS linkers between different subproteins should be between 5 and 20 amino acids long.'`
    → `29: * The GS linkers between different subproteins should be between 5 and 20 amino acids long.`
    (16 words)
  All quotes ≤25 words; all locations confirmed by grep output.
- Read the probe receipt `corpus/evidence/round35/tb2-grader-probe.txt` (`cases=18 observed_pass=5
  observed_fail=13 mismatches=0`, grader sha256 44a05a… matches the S105 anchor) — the "teaches"
  cells do not cite unobserved counts beyond it.
- No tools installed (existing bash/coreutils/grep/cp/gawk only); no pacman transactions; no
  writes outside my scratch dir and report; no edits to `corpus/`, `plans/`, or any lane file.

## Drafted rows (S105–S107, 11 columns, `|`-free cells)

```
| S105 | Terminal-Bench 2.0 protein-assembly task grader (tests/test_outputs.py) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/tests/test_outputs.py | code | A | the executed scoring predicate of one Terminal-Bench 2.0 task at a pinned commit — which output properties test_gblock asserts and how — for the code's own behaviour; the comments' claims about which PDB entries match are the authors' self-report | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, tests/test_outputs.py:42 "assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx, (" (9 words); sha256 44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582 | the task score is one pytest function over literal expected subproteins, order, FLAG/SNAP boundaries, 5-20 residue [GS]+ linkers and 15-35 GC per 50-nt window; reference input files are never read | mined | 2026-10-25 | 180d | corpus/knowledge/tb2-protein-assembly-grader.md |
| S106 | Terminal-Bench 2.0 protein-assembly verifier runner (tests/test.sh) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/tests/test.sh | code | A | how this one task's pytest outcome becomes its reward at a pinned commit, for the script's own behaviour; not Harbor's consumption or aggregation of the reward file | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, tests/test.sh:27 "echo 1 > /logs/verifier/reward.txt" (4 words) and :21 "-w biopython==1.85" ; sha256 9ede46648fc67c9ce61975503de3e0fcff0b0fb110adc0f9e1d240a608c267b5 | the reward is binary (1 iff pytest exits 0) and the grader runs under uvx with Python 3.13, pytest 8.4.1 and biopython 1.85 | mined | 2026-10-25 | 180d | corpus/knowledge/tb2-protein-assembly-grader.md |
| S107 | Terminal-Bench 2.0 protein-assembly task instruction (instruction.md) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/instruction.md | docs | A | the requirement bullets this one task states to the agent at a pinned commit, as the maintainer's own specification the grader is mapped against | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, instruction.md:29 "The GS linkers between different subproteins should be between 5 and 20 amino acids long." (16 words); sha256 1bb2af1d85e9a823a8ae7273a87df8a3f67e2c93b06cddf34f0051a8b003f7c5 | fifteen requirement bullets (file shape, allowed parts, PDB/FPbase/plasmid sources, no start/stop codons or N-terminal Met, linker rules, GC windows, 3000-nt cap, part order) | mined | 2026-10-25 | 180d | corpus/knowledge/tb2-protein-assembly-grader.md |
```

## Lesson `## Gate` source block (round-35 lesson draft)

```
## Gate

New rows S105–S107, access date 2026-10-25 (quotes verified with grep -nF against
corpus/evidence/round35/tb2-eval/, byte-identical to the pinned raw files):
- S105 https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/tests/test_outputs.py
  test_outputs.py:42 "assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx, (" (9 words)
- S106 https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/tests/test.sh
  test.sh:27 "echo 1 > /logs/verifier/reward.txt" (4 words); test.sh:21 "-w biopython==1.85"
- S107 https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/instruction.md
  instruction.md:29 "The GS linkers between different subproteins should be between 5 and 20 amino acids long." (16 words)
```

## Census validation (scratch)

Commands:

```
mkdir -p <build>/R35RowsDraft/validate
cp -r <lane>/corpus <build>/R35RowsDraft/validate/corpus
<fleet>/scripts/sources-census.sh validate --file <build>/R35RowsDraft/validate/corpus/SOURCES.md; echo "EXIT=$?"
```

The copy carries the full corpus (used-by paths resolve), with S105–S107 at the end of the
Registry table (lines 120–122, before `## Paths` at 123). Output (verbatim):

```
file	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
file	W04	S048 duplicate url aclanthology.org/2020.acl-main.442 across scopes
file	W04	S057 duplicate url arxiv.org/abs/2405.11874 across scopes
file	W04	S058 duplicate url github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py across scopes
file	W04	S059 duplicate url www.rfc-editor.org/rfc/rfc8259 across scopes
file	W04	S064 duplicate url spec.commonmark.org/0.31.2 across scopes
file	W04	S065 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S066 duplicate url doi.org/10.1017/S0950268810000385 across scopes
file	W04	S067 duplicate url doi.org/10.1017/S0950268810000385 across scopes
file	W04	S068 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json across scopes
file	W04	S069 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py across scopes
file	W04	S071 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S075 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S076 duplicate url docs.python.org/3/library/json.html across scopes
file	W04	S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
file	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-35/build/R35RowsDraft/validate/corpus/SOURCES.md
EXIT=0
```

Exit 0. The 15 W04 warnings are pre-existing (the frozen census-before also had 15 W04);
none involve S105–S107 (their URLs are unique). `file ok` means zero E-findings.

## Gates

- No edits to `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, README/SKILL/PROVINCE/SHONEN, or
  any lane file — draft only, for the L1.
- No git/jj mutation; no writes outside `<build>/R35RowsDraft/` and this report.
- No subagents / background jobs / `task` (leaf seat).
- All numbers carry their producing command and output (above).

## Out-of-scope items

- S105–S107 are already integrated in the lane SOURCES.md at lines 120–122 (state at start of
  work); this report re-drafts them verbatim and validates that state — no further action to the
  file is performed by this seat.
- Not assessed: C1 counter (`plans/round35_c1_verify.py`), C2 ledger, knowledge-entry content
  (that is the C1 seat's surface).

## Findings

- All three quote locations verified by grep -nF match the anchors exactly (42 / 27+21 / 29).
- sha256 values in the rows match SHA256SUMS and the frozen claim.
- Census validate on the integrated state exits 0.

VERDICT: rows-drafted-census-0
