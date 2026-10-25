writer: KengakuR29-2.FSourcesCensus-2

# FSourcesCensus — census delta and S070–S073 SOURCES-contract check

observed-at: 2026-10-21T16:50:47Z (13:50:47 -03)
lane HEAD: `56fd949a6478342531e61f4feecb4a685d831640`
independence: I did **not** read or import `plans/config_projection.py`; this item compares the
census instrument's output only. No REA MCP device used. No tool install or update (no pacman
transaction; stdlib `python3` and coreutils only).

## Attack

Two integrated-state claims are attacked:

1. adding S070–S073 leaves `scripts/sources-census.sh validate` clean except warnings that the
   SOURCES contract and the census design already expect;
2. the four new registry rows obey SOURCES contract v1 (`CORPUS.md` §“SOURCES.md — where a
   shokunin learns”, lines 64–155 at this commit).

The projection instrument, the 2436 projections, and the candidate knowledge file are outside
this item and were not re-run.

## 1. Exact command, output, and baseline delta

Command, run from the lane root:

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
```

Observed stdout, 13 lines, exit `0` (12 `W04` lines + one `ok` line; long lines shown whole):

```
kengaku	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
kengaku	W04	S048 duplicate url aclanthology.org/2020.acl-main.442 across scopes
kengaku	W04	S057 duplicate url arxiv.org/abs/2405.11874 across scopes
kengaku	W04	S058 duplicate url github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py across scopes
kengaku	W04	S059 duplicate url www.rfc-editor.org/rfc/rfc8259 across scopes
kengaku	W04	S064 duplicate url spec.commonmark.org/0.31.2 across scopes
kengaku	W04	S065 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S066 duplicate url doi.org/10.1017/S0950268810000385 across scopes
kengaku	W04	S067 duplicate url doi.org/10.1017/S0950268810000385 across scopes
kengaku	W04	S068 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json across scopes
kengaku	W04	S069 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py across scopes
kengaku	W04	S071 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
```

Baseline receipt `corpus/evidence/round29-calibration/sources-before.txt`: 1181 bytes, 14 lines,
mtime `2026-10-21 12:56:42.315980419 -0300`. Its 14 lines are the same 11 `W04` lines (S040,
S048, S057, S058, S059, S064, S065, S066, S067, S068, S069), the same `ok` line, then one empty
line, then `exit=0`. Last bytes confirmed with `od -c`:
`... / S O U R C E S . m d \n \n e x i t = 0 \n`.

Warning-only comparison (drop the `ok` line and the receipt's out-of-band blank/`exit=0` lines):

```
@@
 kengaku	W04	S069 duplicate url raw.githubusercontent.com/.../evaluation_harness/evaluators.py across scopes
+kengaku	W04	S071 duplicate url docs.python.org/3/library/json.html across scopes
```

Exactly **one new warning**, no warning removed, nothing reordered. Exit stays `0`.

Baseline provenance was reproduced independently: `git diff --numstat df33fc8 b98dcf3 --
corpus/SOURCES.md` prints `4  0` (four inserted lines, zero changes), and a copy of
`df33fc8:corpus/SOURCES.md` run through `validate` reproduced the receipt's 11 `W04` lines
(lane label differs, temp-dir `E11` lines dropped because `used-by` paths resolve against the
temp lane dir). Commit times: `df33fc8` 12:34:03 -03, `b98dcf3` 13:39:10 -03, `56fd949`
13:40:37 -03.

Census-count delta, `sources-census.sh census` on the current registry vs a copy of
`df33fc8:corpus/SOURCES.md`:

| metric | current (HEAD) | pre-round-29 (`df33fc8`) | delta |
|---|---:|---:|---:|
| rows | 73 | 69 | +4 |
| tier.A | 67 | 63 | +4 |
| tier.B | 4 | 4 | 0 |
| tier.C | 2 | 2 | 0 |
| status.queued | 12 | 8 | +4 |
| status.mined | 57 | 57 | 0 |
| status.rejected | 4 | 4 | 0 |

So the only registry delta is four new tier-A, queued rows.

## 2. Why only S071 warns, and why it is not an error

Observed mechanics in `scripts/sources-census.sh`:

- `url_of()` (lines 600–606) strips the fragment (`sub(/#[^ ]*$/,"",u)`, line 602), the scheme,
  a trailing slash, and lowercases the host. A fragment on S071 would therefore **not** remove
  the warning.
- W04 is printed at line 645 when the normalized URL was seen before and the `(URL, scope)` pair
  is new.
- E04 is printed at lines 647–650 only when the same `(URL, scope)` pair was already seen, the
  prior row is non-rejected, and `teaches` does not match `supersedes S[0-9]{3}`.
- Warnings do not set `findings`; only an `E` code does (line 740). Header lines 16–18 state
  W-codes “never change status”. Hence 12 W04 lines and exit `0`.

Three rows on the same docs page normalize to the same URL:

| row | line in `corpus/SOURCES.md` | normalized URL | scope (paraphrase) |
|---|---:|---|---|
| S052 | 74 | docs.python.org/3/library/json.html | `raw_decode` return/trailing-data tolerance |
| S065 | 87 | docs.python.org/3/library/json.html | documented Python NaN/Infinity acceptance |
| S071 | 93 | docs.python.org/3/library/json.html | default escaping and deserialization rejection |

S065 was already the second occurrence and already warned in the receipt. S071 is the third
occurrence, so its W04 is the expected consequence of adding a third, differently scoped row on
the same page. It is not E04 because S071's `scope` cell differs from S052's and S065's, and
S071 is not a correction of either; no `supersedes` clause is required by rule 2. The scoped
distinction is substantive: NaN acceptance is not escaping/BOM/duplicate-name behavior.

[INFERENCE] This warning needs no row change and no merge: merging S071 into S065 would conflate
two distinct source contracts, and the census itself classifies cross-scope duplication as a
warning rather than an error.

## 3. S070–S073 against the SOURCES contract

### 3.1 Mechanized shape checks

Frozen census commands from `CORPUS.md` lines 135–147, run from the lane root (rows begin at
column zero; `od -c` of line 93 starts `|   S   0 7 1 ...`):

| check | output |
|---|---|
| rows (`grep -cE`) | `73` |
| malformed rows, `NF!=13` | `0` |
| duplicate ids | `0` lines |
| enum violations / tier inflation | `0` lines |
| mined rows with missing `used-by` paths | `0` lines |

Maintained `validate` emits no `E01`–`E12`, no `W01`–`W03`; the only new line is S071 `W04`.
S070–S073 occupy `corpus/SOURCES.md` lines 92–95, are the four highest ids after S069, and are
all `queued` with `used-by` `—` (so `W03`, which is mined-only, does not apply).

### 3.2 Per-row anchor and content verification

Observed against the bytes on disk and the live docs page:

| row | kind/tier/status | anchor check |
|---|---|---|
| S070 | code / A / queued | `plans/fixtures/r29/generate_test_data.py` sha256 `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` equals the row's claimed hash; `wc -lc` = 27 lines, 838 bytes (row says 838); `cat -n` confirms `main` 8–23, six ordered `raw.replace` calls 11–16 in the listed order (`__GITLAB__`, `__REDDIT__`, `__SHOPPING__`, `__SHOPPING_ADMIN__`, `__WIKIPEDIA__`, `__MAP__`), `json.loads` 20, `enumerate` loop 21–23. The row's three behavioral sentences match those lines. |
| S071 | docs / A / queued | Live fetch `https://docs.python.org/3/library/json.html` returned HTTP 200, 115104 bytes. Stripped page text contains `3.15.1 documentation`, `Last updated on Oct 21, 2026 (13:02 UTC)`, the quoted sentence `thus escaping the output so that the resulting strings only contain printable ASCII characters.` (14 words, `len(str.split())`), `ignores all but the last name-value pair` (7 words), `raises a ValueError when an initial BOM is present` (9 words), and the heading `Character Encodings`. Version, section, and the taught facts are therefore independently grounded. |
| S072 | docs / A / queued | `README.md` sha256 `081c826497f9b7da4952771ee128c2215ec3532379db0fe9f7fcbd899d9c9287` equals the row's claim; matching copy `.ufo/waves/round-28/scratch/OpenTasks/pinned-README.md` is 162 lines, 9717 bytes. `awk` of the row's anchor lines confirms line 79 (812-example note), 84–92 (step 2 and exactly seven scheme-less `export` lines, `SHOPPING_ADMIN` with `/admin`, `WIKIPEDIA` with a long path, `HOMEPAGE` marked placeholder), 95 (workflow note), 97–101 (step 3, `python scripts/generate_test_data.py`, one config per example). Line 108 (API-key placeholder) is outside the row's anchor and is not reproduced. |
| S073 | code / A / queued | `prepare.sh` sha256 `97b8671fc66518fbfed54467f9a64965bafa54d01702d922bfbb8b32c1b0c7e2` equals the row's claim; scratch copy is 6 lines, 120 bytes; commands are lines 5–6 (`mkdir -p ./.auth`, `python browser_env/auto_login.py`). Counts on that file: `generate_test_data`=0, `scripts/`=0, `config_files`=0, `export `=0, matching the row's negative claim. |

Rule 2 (append-only) holds: the commit diff is four inserted rows, zero modified rows. Rule 3
(no second method) holds: the rows are source claims, not method restatements. Rule 6 holds: all
four `source` cells are public commit-pinned `raw.githubusercontent.com`/docs URLs at `dce04686`
(or the versioned docs page); no credentials, cookies, auth-state contents, private URLs, or
`op://` references appear in the rows.

### 3.3 Contract mismatch found

**M1 — rule 1’s round-lesson Gate is absent from the integrated commit.** Rule 1 requires the
round lesson's `## Gate` to record, for every new row, the URL, access date, and a ≤25-word
located quote. At `56fd949`:

- `git cat-file -e 56fd949:corpus/lessons/round-29.md` → exit `128`, `fatal: path
  'corpus/lessons/round-29.md' exists on disk, but not in '56fd949'`;
- `git ls-tree -r --name-only 56fd949 corpus/lessons | grep -i 29` → no output, exit `1`;
- the live but untracked `corpus/lessons/round-29.md` (3567 bytes, mtime
  `2026-10-21 13:47:54.035393767 -0300`) has `grep -c '^## Gate'` = `0` and
  `grep -c 'S070\|S071\|S072\|S073'` = `0`.

The opening material exists only in build reports: `build/R29SourceGenerator.md` states a
24-word quote and byte pin, `build/R29SourceJsonDocs.md` a 14-word quote at rendered lines
581–582 (independently reproduced here), `build/R29SourceWorkflow.md` a 19-word quote and
`README.meta.json` `quote_words: 19`, `build/R29SourceCaller.md` a 5-word quote. The contract
names the round lesson, not build reports, as the Gate record. This is the only row-contract
rule I could not find satisfied at the integrated state.

**M2 — baseline receipt contains two non-instrument lines.** `sources-before.txt` lines 13–14
are an empty line and `exit=0`; census stdout has neither (it ends with the `ok` line). This is
a capture-harness artifact, not an instrument or row mismatch; it does not affect the
warning-only diff once removed. Exact tail bytes shown in §1.

**M3 — S071 rendered line numbers were not independently reproduced.** The row's anchor cites
`Character Encodings §576-591`, `581-582`, `254`, `402`, `591`, `624-625`. A raw-HTML fetch
cannot reproduce a reader's rendered line numbering; the heading (`Character Encodings`),
version (`3.15.1`), last-updated stamp, and every quoted fact were reproduced. The anchor still
carries an exact heading plus revision, so I record this as a method caveat, not a violation.
[INFERENCE] The line numbers are reader-layout positions, consistent with the build report's
stated method.

**M4 — no round-29 Search-log entry (low confidence, rule 5).** `corpus/SOURCES.md` line 105
starts `## Search log`; `grep -n 'Round 29\|round-29\|round29' corpus/SOURCES.md` returns no
line. The four rows came from assigned single-URL fetches whose sweep blocks live in the build
reports. [INFERENCE] If the lane classifies those as bounded searches, rule 5's SOURCES note is
missing; if they are source openings rather than searches, rule 5 does not apply.

No other mismatch was found: no malformed row, duplicate id, enum violation, same-scope
duplicate, missing `used-by` path, credential material, or modified pre-existing row.

## 4. Scoped result

Observed: the census delta is exactly one new warning (S071, cross-scope duplicate of S052/S065,
W04 by design, exit 0); the four rows’ field shapes, enums, statuses, dates, hashes, line
anchors, and taught facts check out; the commit contains only four appended rows. The one
unsatisfied contract rule is rule 1’s Gate, absent from `56fd949` and from the live untracked
round lesson at observation time.

VERDICT: PARTIAL
