# R36RowsDraft — registry rows S108-S110 + C2 Gate source block

Seat: R36RowsDraft (scribe, wave 1). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Nothing under `corpus/`, `plans/`, `README.md`, `SCORECARD.md`, `LOG.md` was written: the lane's tracked
tree is clean at HEAD `f9efce3` (`git status --porcelain --untracked-files=no | wc -l` → `0`), and
`corpus/SOURCES.md` still digests `33549258a5ee4d9d68eec040b53f73c10c6e0179ba14c49b8dd5771fbe57e148`.
The three rows exist only as a draft for the L1 to append.

## Behavior delivered

1. Three registry rows in the exact 11-column `corpus/SOURCES.md` schema, ids `S108`/`S109`/`S110`,
   appended after `S107` — schema read from `corpus/SOURCES.md:19-21` and `../CORPUS.md:64-121`
   (SOURCES-CONTRACT-v1), row style copied from the last five rows (`S104`-`S107`).
2. A `## Gate` source block for the round-36 lesson: one row per new source with its pinned URL,
   access date `2026-10-25`, a located quote (`file:line`) and its sha256 prefix — every quote
   mechanically re-grepped with `grep -nF` against the committed captures.
3. Scratch validation of the appended registry with the fleet census validator and with the
   round-36 C2 counter's own `W2` row predicate, plus two red controls showing that predicate
   can fail on these rows.

## Draft rows (verbatim; paste target = `corpus/SOURCES.md`, after the `S107` line, before `## Paths`)

| S108 | Terminal-Bench 2.0 regex-log task grader (tests/test_outputs.py) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test_outputs.py | code | A | the executed scoring predicate of one Terminal-Bench 2.0 task at a pinned commit — which regex output test_regex_matches_dates asserts and how — for the code's own behaviour; the inline comments' labels about which fixture line should match are the authors' self-report | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, tests/test_outputs.py:8-90, :87 "matches = re.findall(pattern_text, log_text, re.MULTILINE)" (6 words); sha256 345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72 | the task score is one pytest function asserting re.findall output over a 25-line fixed log equals nine expected dates | mined | 2026-10-25 | 180d | corpus/knowledge/tb2-regex-log-grader.md |
| S109 | Terminal-Bench 2.0 regex-log verifier runner (tests/test.sh) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test.sh | code | A | how this one task's pytest outcome becomes its reward at a pinned commit, for the script's own behaviour; not Harbor's consumption or aggregation of the reward file | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, tests/test.sh:18-29, :26 "echo 1 > /logs/verifier/reward.txt" (4 words), :20 "-w pytest==8.4.1"; sha256 4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334 | the reward is binary, one iff pytest exits zero, and the pinned run installs pytest 8.4.1 plus a CTRF report at /logs/verifier/ctrf.json | mined | 2026-10-25 | 180d | corpus/knowledge/tb2-regex-log-grader.md |
| S110 | Terminal-Bench 2.0 regex-log task instruction (instruction.md) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/instruction.md | docs | A | the requirement bullets this one task states to the agent at a pinned commit, as the maintainer's own specification the grader is mapped against | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, instruction.md:1-19, :3 "Assume that February can have up to 29 days in all years, without distinguishing leap years from non-leap years." (19 words); sha256 4f7ac05e70cf922ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c | four operating rules beyond matching: last date per line, 29-day February, no leading-zero octets, no adjacent alphanumerics | mined | 2026-10-25 | 180d | corpus/knowledge/tb2-regex-log-grader.md |

Same three lines, machine-pasteable, at `build/R36RowsDraft/rows-S108-S110.md`.

## Gate source block (draft; L1 integrates into `corpus/lessons/round-36*.md`)

At `build/R36RowsDraft/gate-block-round36.md`. Its quotes and their locations, all verified with
`grep -nF` against `corpus/evidence/round36/tb2-regex-log/` (command and output in §Gates below):

| row | quote lines cited | words |
|---|---|---|
| S108 | `test_outputs.py:90` (assertion) | 9 |
| S109 | `test.sh:26` (reward write), `:20` (`-w pytest==8.4.1`), `:22` (pytest+ctrf invocation) | 4 / 2 / 5 |
| S110 | `instruction.md:7` (adjacency rule), `:2` (last date), `:3` (29-day February), `:4` (no leading zeros) | 20 / 19 / 19 / 12 |

Every quoted string is ASCII-verbatim from the capture; the surrounding delimiters are the lesson's
curly quotes, so each quote body greps exactly (the S108 body contains the file's own ASCII double
quotes around the f-string, which is why it is the one row whose body carries `"`).

## Gates run (exact commands, exact output)

All scratch work is under `.ufo/waves/round-36/build/R36RowsDraft/`. No `git clone` fixture was needed:
the rows are text appended to a copy of the committed registry, and the validator was pointed at that
copy with `--file` (its `dir` becomes the copy's parent, so `used-by` resolves inside the copy).

1. Scratch copy + stub entry (so `E11` has a real file to find; the stub is not the entry of record):

```sh
B=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-36/build/R36RowsDraft
cp -a .../kengaku-shokunin/corpus "$B/validate/corpus"
# stub at $B/validate/corpus/knowledge/tb2-regex-log-grader.md (5 provenance lines, marked stub)
# three rows inserted after the S107 line in $B/validate/corpus/SOURCES.md
```

Delta from the committed registry, whole-file diff:

```sh
diff -u corpus/SOURCES.md "$B/validate/corpus/SOURCES.md" | grep -cE '^\+[^+]'
# 3      (only the three added rows; no other line added or removed)
```

2. Census validator (the acceptance command):

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --file /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-36/build/R36RowsDraft/validate/corpus/SOURCES.md
```

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
file	ok	.../build/R36RowsDraft/validate/corpus/SOURCES.md
EXIT=0
```

No `E` finding and no `W01`/`W02`/`W03`. The fifteen `W04` rows are the pre-existing duplicates named in
the round-36 census-before control (`plans/round-36-claims.md` §Frontier step: "15 W04"); none is
`S108`-`S110`, and the validator still prints `file ok` with exit 0.

3. Frozen manual census checks from `../CORPUS.md:130-148`, run in the scratch lane root:

```sh
cd $B/validate
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md          # 103   (100 committed + 3)
awk -F'|' '... NF!=13 ...' corpus/SOURCES.md                                   # 0
awk -F'|' '... print i' corpus/SOURCES.md | sort | uniq -d                     # (empty)
awk -F'|' '... enum ...' corpus/SOURCES.md                                     # (empty)
awk -F'|' '... mined used-by ...' corpus/SOURCES.md | while read p; do [ -e "$p" ] || ...; done   # (empty)
awk -F'|' '{print NF-2}' on the three new rows                                 # 11 11 11
```

4. The C2 counter's own `W2` predicate, imported and called in isolation (the full counter needs the
   entry and probe receipt, which are other seats' surfaces):

```sh
python3 - "$T/lane" <<'PY'   # lane/corpus/SOURCES.md = the scratch registry
import importlib.util; spec = importlib.util.spec_from_file_location("c2", "plans/round36_c2_verify.py"); ...
print("w2:", m.w2(lane) or "ok")
PY
# w2: ok
```

Red controls on the same predicate (each attack applied to a fresh copy):

| attack | result |
|---|---|
| `S109` teaches replaced by `short teaches cell` (3 words) | `w2: S109 teaches has 3 words` |
| all three `used-by` cells repointed to `corpus/knowledge/tb2-protein-assembly-grader.md` | `w2: S108 used-by 'corpus/knowledge/tb2-protein-assembly-grader.md'` |

So `W2` is green for the drafted rows and demonstrably able to go red on exactly the two properties the
contract names (teaches length, used-by identity).

5. Capture integrity and quote locations:

```sh
cd corpus/evidence/round36/tb2-regex-log && sha256sum -c SHA256SUMS
# test_outputs.py: OK / test.sh: OK / instruction.md: OK / task.toml: OK / solve.sh: OK
sha256sum test_outputs.py test.sh instruction.md
# 345c3bd0…8f72 / 4770437e…6c334 / 4f7ac05e…96f9c  (equal to the counter's FILES pins)
grep -nF -- 'assert matches == expected_dates, f"Expected {expected_dates}, but got {matches}"' test_outputs.py   # 90:
grep -nF -- 'echo 1 > /logs/verifier/reward.txt' test.sh                                                          # 26:
grep -nF -- '-w pytest==8.4.1' test.sh                                                                            # 20:
grep -nF -- 'pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA' test.sh                           # 22:
grep -nF -- 'If multiple dates are present in a line, the regex should match only the last date in that line.' instruction.md   # 2:
grep -nF -- 'Assume that February can have up to 29 days in all years, without distinguishing leap years from non-leap years.' instruction.md   # 3:
grep -nF -- 'IPv4 addresses use normal decimal notation without leading zeros in each octet.' instruction.md       # 4:
grep -nF -- 'To avoid false matches, ensure that valid dates and IPv4 addresses are not immediately preceded or followed by alphanumeric characters.' instruction.md   # 7:
```

6. The two numeric claims inside `teaches` (not decorative — `S108` says "25-line" and "nine"), counted
   from the capture bytes:

```sh
python3 - # parse sample_logs = [...] and expected_dates = [...]
# sample_logs entries: 25        expected dates: 9
```

`S109`'s "binary, one iff pytest exits zero" is `test.sh:25-29` (`if [ $? -eq 0 ]; then echo 1 …
else echo 0`); "installs pytest 8.4.1" is `:20`; "CTRF report at /logs/verifier/ctrf.json" is `:22`.
`S110`'s four rules are `instruction.md:2`, `:3`, `:4`, `:7`; the row anchors on `:3` and the Gate block
carries the other three.

## Findings

- **F1 — C2 `W4` needs the entry before it can pass, and the counts are currently tied at 42.**
  `ls corpus/knowledge/*.md | wc -l` → `42`; `grep -c '^| \`knowledge/' corpus/README.md` → `42`.
  `W4` requires `knowledge files == index rows >= 43`, so the entry row (`corpus/knowledge/tb2-regex-log-grader.md`)
  plus its README index row and coverage bullet must land in the same integration step as these rows.
  My stub exists only inside `build/R36RowsDraft/validate/` and must never be copied back.
- **F2 — `W2`'s URL test is exact-string, so the three `source` cells must keep the bare pinned raw URL
  and no trailing punctuation.** I placed the URL last in the cell; `re.findall(r"https?://\S+", source)`
  returns exactly `[RAW + upstream_path]` for all three (verified by the `w2: ok` run, which is the only
  check that exercises that regex).
- **F3 — `S109` would duplicate `S106`'s teaching if worded the same way.** Both are a TB2 `test.sh` whose
  reward is `echo 1`/`echo 0` on pytest's exit status. I differentiated on what is actually distinct in
  this file — the CTRF report artefact and the `pytest==8.4.1` pin (this task pins Python 3.13 and does
  not install biopython) — and kept the three `teaches` cells pairwise distinct as `W2` requires
  (`teaches_words=19 / 22 / 17`, all different strings).
- **F4 — the registry is not dense.** The committed registry has 100 rows for ids `S001`-`S107`
  (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`), so `S107` being the last row does not mean the
  last id is `S107`. Appending after `S107` is still correct: the file is append-ordered and `S108` is the
  next unused id.
- **F5 — cross-item note for C1, not my surface.** The lane currently has 151 untracked files
  (`git ls-files --others --exclude-standard | wc -l`), the wave-36 `build/`, `integrate/` and
  `build.ready` paths. C1's predicate is measured with `--require-clean-tree` = no untracked file, so
  those paths have to be committed or removed before the C1 gate can be run on the landing tip.
- **F6 — Amendment 1 is in place and consistent.** `plans/round36_c2_verify.py:41` holds
  `PROBE_SHA256 = "d58194c8…519bc"`, `plans/regex_log_probe.py` digests `d58194c8…519bc`, and HEAD is
  `f9efce3`, sitting on top of `acbda2f` ("round-36: amendment 1 …"). The file's whole digest
  (`983ed65c…7120`) therefore differs from the freeze-block line `f70e6d3a…1500`, exactly the one-line
  move the amendment declares. That is a disclosed change, not drift; I did not touch the file.

## Known limits

- I did not fetch the three pinned URLs over the network. Every quote, line number and digest is checked
  against the committed captures (`corpus/evidence/round36/tb2-regex-log/`, `SHA256SUMS`-verified), whose
  digests equal the counter's frozen `FILES` pins; upstream byte-identity rests on the capture round, not
  on this seat.
- The full C2 counter (`checks=6 defects=0`) was not run: `W3`/`W4`/`W5` are the entry, README and probe
  seats' surfaces and the entry does not exist yet. Only `W2` was exercised, in isolation.
- The Gate block is a draft for the L1: a lesson may also want a candidate row for the entry itself, which
  is outside this ticket.
- No tool was installed or upgraded (nothing was needed); no `pacman`, `uv`, `npm` or binary install ran.

## Artifact paths (all inside `.ufo/waves/round-36/build/R36RowsDraft/`)

- `rows-S108-S110.md` — the three registry rows, nothing else.
- `gate-block-round36.md` — the `## Gate` source block.
- `validate/corpus/` — scratch copy with the rows appended and the stub entry.
- `validate/corpus/SOURCES.md` — the file the census validator was pointed at.

VERDICT: rows-drafted-census-0
