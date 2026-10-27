# R45PkgRows — SOURCES rows S149–S156 for the TB2 `password-recovery` package

Seat: `R45PkgRows` (scribe, round 45 wave 1). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scratch `S=/fast/scratch/hyaku/kengaku-r45/R45PkgRows` (`TMPDIR=$S`). Subdir
`.ufo/waves/round-45/w1/R45PkgRows/`.

## 1. What was drafted

**Eight registry rows, S149–S156**, in `.ufo/waves/round-45/w1/R45PkgRows/rows-S149-S156.md` — the exact set
`plans/pkg-spec-r45.json` `rows` names (S149 test_outputs.py, S150 instruction.md, S151 setup.sh, S152
Dockerfile, S153 test.sh, S154 README.md, S155 solve.sh, S156 task.toml), all `mined`, tier `A`, opened
`2026-10-26`, recheck `180d`, one used-by cell `corpus/knowledge/tb2-password-recovery-grader.md`, 11 cells each.
Five `code` (S149, S151, S152, S153, S155), three `docs` (S150, S154, S156).

**The ninth capture is not a row.** `gitignore` is rejected (repo hygiene, not graded content; zero mentions in
`tests/test_outputs.py`, `tests/test.sh`, `environment/setup.sh`); `SHA256SUMS` is rejected as inventory. No id is
minted for either because the frozen spec's `rows` map holds exactly S149–S156. Rejections, reasons and flip
conditions are in `gate-block.md`. The seat ticket's "nine SOURCES rows S149-S156" is an off-by-one: eight ids,
eight rows, one reject — matching the spec and the ticket's own "8 rows + the 9th is NOT a row".

`gate-block.md` holds the `## Gate` block: access date `2026-10-26` for every row, the pinned URL per row, a
≤25-word quote located at `capture:line` with that capture's sha256, the flip condition per row, the two reject
rows, the flip-check command and its run against the entry draft
(`.ufo/waves/round-45/w1/R45PkgEntry/tb2-password-recovery-grader.md`: `gitignore — not fired`,
`(.gitignore|SHA256SUMS) — not fired`).

Quotes as anchored (all verbatim, all 3–25 words):

| row | capture:line | words | sha256 (first 8 … last 8) |
|---|---|---|---|
| S149 | `test_outputs.py:18` | 7 | `2dc14fc1…ed3bfc9e` |
| S150 | `instruction.md:9` | 20 | `bc4f5011…20b7810a5` |
| S151 | `setup.sh:25` | 4 | `9fdde5d9…5a6f2af8` |
| S152 | `Dockerfile:17` | 3 | `6fabcb9e…4b6c9fe0` |
| S153 | `test.sh:26` | 4 | `4770437e…716e6c334` |
| S154 | `README.md:31` | 11 | `122bf15e…ac6a13add` |
| S155 | `solve.sh:63` | 4 | `c5f9fc70…7b8d804f` |
| S156 | `task.toml:22` | 3 | `cfd0362d…cfd091b24b` |

Integration point for the L1: append the eight lines **after the last `| S…` line of `## Registry`** — line 163
(`S146`) at lane tip `05b02e2b`; not at EOF, see finding F2.

## 2. Validation

Lane tip moved during the seat (`52d7486` → `05b02e2b`). `corpus/SOURCES.md` bytes are identical at
`b4fcd35`, `52d7486` and `05b02e2b` (`sha256 3911d00708c071966008d3f2f6a07bf7e163a63a20a6c80c98688516391836b0`),
so the rows target one file. All runs are on a `--shared` clone at `S/lane`
(`git -C "$S/lane" rev-parse --show-toplevel` = `$S/lane`; no commit made) inside the round-45 envelope.

### 2.1 Row self-check — `python3 rowcheck.py rows-S149-S156.md`

```
ROWS parsed=8
OK S149 capture=test_outputs.py upstream=tests/test_outputs.py line=18 verbatim=True words=7/7 range=3-25 sha256_pin=True cap=True meta=True teaches=64 cells=11
OK S150 capture=instruction.md upstream=instruction.md line=9 verbatim=True words=20/20 range=3-25 sha256_pin=True cap=True meta=True teaches=58 cells=11
OK S151 capture=setup.sh upstream=environment/setup.sh line=25 verbatim=True words=4/4 range=3-25 sha256_pin=True cap=True meta=True teaches=76 cells=11
OK S152 capture=Dockerfile upstream=environment/Dockerfile line=17 verbatim=True words=3/3 range=3-25 sha256_pin=True cap=True meta=True teaches=71 cells=11
OK S153 capture=test.sh upstream=tests/test.sh line=26 verbatim=True words=4/4 range=3-25 sha256_pin=True cap=True meta=True teaches=59 cells=11
OK S154 capture=README.md upstream=README.md line=31 verbatim=True words=11/11 range=3-25 sha256_pin=True cap=True meta=True teaches=63 cells=11
OK S155 capture=solve.sh upstream=solution/solve.sh line=63 verbatim=True words=4/4 range=3-25 sha256_pin=True cap=True meta=True teaches=79 cells=11
OK S156 capture=task.toml upstream=task.toml line=22 verbatim=True words=3/3 range=3-25 sha256_pin=True cap=True meta=True teaches=59 cells=11
DEFECTS 0
ROWCHECK_exit=0
```

Each line asserts: 11 cells; the URL's task-relative path equals the spec's `upstream`; the quoted string occurs
on that physical line of the capture; the stated word count equals the split and lies in `entry_rules.quote_words`;
the digest equals the capture bytes **and** the spec pin; tier/status/opened match `entry_rules`; `teaches` ≥ 8
words; recheck is an accepted cadence.

### 2.2 V3 — the frozen C2 counter's own function, read-only import, `lane=$S/lane`

```
V3 ok=True rows=8 bad=0
```

(`plans/round45_c2_verify.py` loaded by path and called as `v3(clone)`: one 11-cell registry row per spec id whose
anchor cell carries exactly `[spec sha256]`.)

### 2.3 Census green — rows inserted after `S146`, E11 placeholder present

`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/lane/corpus/SOURCES.md`

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
file	ok	/fast/scratch/hyaku/kengaku-r45/R45PkgRows/lane/corpus/SOURCES.md
CENSUS_exit_code=0
CENSUS_counts W04=15 E-codes=0
file	rows	149
file	tier.A	125
SOURCE_ROW_regex_hits 149
```

15 W04, all pre-existing (S040…S100, none of them mine), **0 E-codes**, exit 0; registry 141 → 149; tier A
117 → 125.

### 2.4 Red controls

E11 (used-by target removed → must fire on all eight):

```
CENSUS_red_exit_code=1
E11_rows_fired=8 E11_ids=S149 … S156 each "missing used-by corpus/knowledge/tb2-password-recovery-grader.md"
```

E12 (the same eight rows appended at EOF instead of inside `## Registry`; `$S/e12/` copy, `git show
HEAD:corpus/SOURCES.md` + rows):

```
E12_control_exit=1
E12_rows=8 E12_ids=S149 … S156 each "row outside Registry section"
CENSUS_rows_mode=141          # the eight rows are parsed for E12 and not counted as registry rows
```

Anchor digest (`plans/anchor_digest_check.py --lane $S/lane`): green leg **fails on 5 of my 8 rows** for an
evidence-layout reason, not a digest reason — finding F1:

```
DEFECT S149 … class=anchor-unbound detail=no-capture-for-upstream-password-recovery/tests/test_outputs.py-task=tests
DEFECT S151 … environment/setup.sh   DEFECT S152 … environment/Dockerfile
DEFECT S153 … tests/test.sh          DEFECT S155 … solution/solve.sh
rows=149 tokens=55 defects=5         (S150, S154, S156 bind by=url-task; S149–S156 all satisfy V3)
```

Anchor red control (S154 digest last nibble flipped, that row being bound):

```
DEFECT S154 anchor token=122bf15ef4a6ede562f21453f9f1c452fc10a3048bac7d46a013adbac6a13adf class=digest-unknown detail=not-committed-evidence-and-not-in-a-SHA256SUMS loc=corpus/SOURCES.md:169
rows=149 tokens=55 defects=6
ANCHOR_mutant_exit=1
```

Capture manifest, read-only, the entry's own recheck command:

```
( cd corpus/evidence/round45/tb2-password-recovery && sha256sum -c SHA256SUMS )   # nine OK, SHA256SUMS_exit=0
```

### 2.5 Envelope lines (every measurement above)

`validate.txt` (run 23:30:48–23:30:53, rowcheck + V3 + census green + E12/E11 controls + anchor):

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45PkgRows/env /fast/scratch/hyaku/kengaku-r45/R45PkgRows/env --bind /fast/scratch/hyaku/kengaku-r45/R45PkgRows/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- bash /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/w1/R45PkgRows/validate.sh
ENVELOPE start 23:30:48 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 23:30:53 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```

`controls.txt` (run 23:31:59–23:32:02, E12 control + capture manifest + gitignore evidence):

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45PkgRows/env /fast/scratch/hyaku/kengaku-r45/R45PkgRows/env --bind /fast/scratch/hyaku/kengaku-r45/R45PkgRows/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- bash /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/w1/R45PkgRows/controls.sh
ENVELOPE start 23:31:59 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 23:32:02 exit=0 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```

One earlier envelope run (23:29:22–23:29:26) measured the same rows appended at EOF; it produced the E12 evidence
now reproduced deliberately in `controls.txt`. No digest change in any run; no re-run of an INVALID measurement
was needed.

## 3. Findings

**F1 — `plans/anchor_digest_check.py` cannot bind a capture kept in an upstream subdirectory (5 of 8 rows
`anchor-unbound`).** Cause, read from the tool: `bind_row` resolves the URL's task slug to the evidence directory
`d` and then probes only `p = f"{d}/{base}"` (basename), plus `dir_entries[(d, base)]`
(`plans/anchor_digest_check.py:336-338`). Rounds 35–44 stored captures flat (`corpus/evidence/round44/
tb2-feal-linear-cryptanalysis/test_outputs.py`), so `tests/test_outputs.py` bound. The round-45 capture directory
keeps upstream subdirectories (`.../round45/tb2-password-recovery/{tests,environment,solution}/`, plus a
`SHA256SUMS` whose names are `tests/test_outputs.py`, `environment/setup.sh`, …), so the five rows whose upstream
path has a subdirectory cannot bind, while S150/S154/S156 (root-level upstream files) do. The digests themselves
are right: each equals both the committed bytes and its `SHA256SUMS` entry (`rowcheck.py`, `sha256sum -c`).
Not a C2 blocker: the frozen counter's V3 only requires the anchor cell's token to equal the spec pin
(`V3 ok=True rows=8 bad=0`), and `round45_c2_verify.py` does not invoke this tool. Two remedies, both for the L1:
(a) flatten the round-45 capture directory to `d/<basename>` with a flat `SHA256SUMS` (rounds 35–44 layout) —
but the captures are frozen, so this is a freeze revision; (b) teach the tool the subpath. I proved (b) on a
scratch copy: patch in `anchor-patch.diff` (14 added lines, one hunk) resolves `rel` below the task component,
tries `d/rel` first and falls back to `d/base`, and then prints all eight binds with the registry still green:

```
BIND S149 capture=corpus/evidence/round45/tb2-password-recovery/tests/test_outputs.py by=url-task
BIND S151 capture=corpus/evidence/round45/tb2-password-recovery/environment/setup.sh by=url-task
BIND S152 capture=corpus/evidence/round45/tb2-password-recovery/environment/Dockerfile by=url-task
BIND S153 capture=corpus/evidence/round45/tb2-password-recovery/tests/test.sh by=url-task
BIND S155 capture=corpus/evidence/round45/tb2-password-recovery/solution/solve.sh by=url-task
rows=149 tokens=55 defects=0      (patched; and with S149's digest flipped: defects=1, DEFECT S149 class=digest-unknown)
```

The patched run is evidence for the remedy, not a lane change: `plans/anchor_digest_check.py` is untouched.

**F2 — appending rows at EOF is an E12 defect in this registry as it now stands.** The round-44 seat appended at
EOF and stayed green because rows were last; `corpus/SOURCES.md` at tip ends in review/follow-up bullets, so EOF
append yields `E12 … row outside Registry section` on every row and `rows` stays 141 (§2.4). The integration
instruction is therefore positional: insert after line 163 (`S146`), inside `## Registry`.

**F3 — escaped quotes in an anchor cell break verbatim reproduction.** Three rows written with `\"` inside the
anchor quote failed `verbatim=False` on first check (S149, S151, S155); markdown table cells need no escaping, and
an escaping backslash makes the quote differ from the capture. Fixed by using the capture's own straight double
quotes; round 44's curly-delimiter workaround is only needed when the row's outer delimiters would be ambiguous.
The `rowcheck.py` verbatim test is what caught it.

**F4 — the ticket's row count and the frozen spec agree with each other, not with the ticket's first sentence.**
Ticket: "Draft the nine SOURCES rows S149-S156" and later "8 rows + the 9th is NOT a row". Spec `rows` holds eight
ids; C2's V3 iterates `s["rows"]`. Eight rows + one reject; registry 141 → 149, not 150.

**F5 — S151 makes the graded constant a repository artefact.** `setup.sh:25` writes
`PASSWORD=8XDP5Q2RT9ZK7VB3BV4WW54` in the clear, and S154 `README.md:31` prints the same constant. The grader
test (S149 `:18`) accepts that single line as a whole-line member, so the mining claim is stronger than "the
environment can be solved": the answer is in the public task files three times (S149, S151, S154) and absent only
from the oracle (S155 contains no literal constant — checked). Stated for the entry's §Frontier narrowing; not a
contradiction of any frozen claim.

## 4. Touched surfaces and bounds

Written: `.ufo/waves/round-45/w1/R45PkgRows.md` (this report) and, under
`.ufo/waves/round-45/w1/R45PkgRows/`: `rows-S149-S156.md`, `gate-block.md`, `rowcheck.py`, `validate.sh`,
`validate.txt`, `controls.sh`, `controls.txt`, `anchor-patch.diff`. Nothing else. Lane `corpus/`, `plans/`,
`SCORECARD.md`, `LOG.md`, `README.md`, `SKILL.md`, `PROVINCE.md` untouched; no git/jj mutation in the lane; no
commit/push anywhere; no `task`/subagent; no tool installed (nothing needed). Scratch `$S` (clone, `env/`, `e12/`,
patched copy) removed after the report; the `e12/` copy and `$S/lane` were never evidence, only instruments.

Read-only outside my subdir: the frozen claims and spec, the eight captures + `SHA256SUMS`, the dry table,
`plans/round45_c2_verify.py` (imported for V3), `plans/anchor_digest_check.py`,
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, and the entry draft
`.ufo/waves/round-45/w1/R45PkgEntry/tb2-password-recovery-grader.md` for the flip checks.

Out of scope and untouched: the entry, README index/bullets, PROVINCE paragraph, the probe receipt, the routed
ledger, and the frontier step's mined-mistake row (other seats). Facts the integrator may want: the entry draft's
`source:` lines already carry S149–S156 at the same lines and digests this seat rows, and its `recheck: 180d`
matches the rows' cadence; the flip checks above were run against that draft, so a landed entry that adds a
`gitignore:<line>` or `SHA256SUMS:<line>` body citation fires the reject conditions.

## 5. Artifact paths

- `.ufo/waves/round-45/w1/R45PkgRows/rows-S149-S156.md` — sha256 `1b2093d40eb65a8e5d7f0c549d894f4b8a78af11f9337a1d9f5467a08c04f384`
- `.ufo/waves/round-45/w1/R45PkgRows/gate-block.md` — sha256 `4d4adc81003657518c570a2a3cbb4dc1ed1416ea8583be96e249a3ea936523f1`
- `.ufo/waves/round-45/w1/R45PkgRows/validate.txt` (receipt, envelope lines 2.5) — sha256 `37162e58decf293060fa19a527dfc4e1d6d67e1882b6d97cb8b608f719be8375`
- `.ufo/waves/round-45/w1/R45PkgRows/controls.txt` — sha256 `dce8c0c34e48b6e104b7444ffda303a3bcd591392848c22c350f13aea7dadc82`
- `.ufo/waves/round-45/w1/R45PkgRows/rowcheck.py` — sha256 `a3c972f1758aca9f7ce71bbfa99b723a87d61645094391b6dfda9b5534660cf8`
- `.ufo/waves/round-45/w1/R45PkgRows/validate.sh` — sha256 `1b47c3ad27254db19493f57033ea5f7bd69cbf3bce2c721768a95ff94475014f`
- `.ufo/waves/round-45/w1/R45PkgRows/controls.sh` — sha256 `2c2be7f61438572b3d30f446c461c69994cb6776e0e0f66ea6965095d1816b44`
- `.ufo/waves/round-45/w1/R45PkgRows/anchor-patch.diff` (F1 remedy, not applied) — sha256 `101745fcbed0b547904f49bd02d15371a39b4d294a0c6e2652c38c9e20221217`

VERDICT: rows-drafted-8-valid-yes-reject-1
