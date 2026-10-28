# SrcCensus — round 51 (hyaku run 11), seat report

Seat: `SrcCensus` (scribe). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (`kengaku`).
Wave: `.ufo/waves/round-51/w1/`. Read-only against the lane; the only file this seat wrote in the
lane is this report. Nothing was appended to `corpus/SOURCES.md` (verified below).

## Axes named before measuring

1. **Receipt fidelity** — every number in this report is copied from a captured command's stdout,
   with the exit code recorded beside it.
2. **Two-level collision truth** — the id-collision answer is given both at the pattern level
   (what the 0–3-leading-space anchor sees) and at the census level (what `validate` would say if
   the package were appended), because the two differ and the difference is itself evidence.
3. **Zero write-surface violation** — lane untouched; the one mutation performed is inside this
   seat's scratch clone and was reverted and re-measured.

## Revisions

- Stage-1 freeze commit measured: `e07f131cf7037e58a21db6e1f3986cf401ad257c`
  (`round-51: stage-1 freeze — C1 surface-truth counter+manifest, C2 routing counter, claims, before receipts`).
- Current tip measured: `4090c3db79d11279ab5e5121ba25e74aa316e6e7`
  (`round-51: v2 wave spec (64 seats) + validated dispatch payload`).
- Freeze measurement was taken in a scratch `git clone --shared` of the lane checked out at
  `e07f131`; the clone's `git rev-parse --show-toplevel` printed
  `/fast/scratch/hyaku/kengaku-r51/SrcCensus/kengaku-shokunin` before any write.
- Current measurement was taken against the live lane working tree at `4090c3d`.

## §1 Commands run

Census, at the freeze (scratch clone; the census labels an explicit lane dir by its basename, hence
`kengaku-shokunin` as the lane column rather than `kengaku` — same tree content, see §4):

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin \
  /fast/scratch/hyaku/kengaku-r51/SrcCensus/kengaku-shokunin
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin \
  /fast/scratch/hyaku/kengaku-r51/SrcCensus/kengaku-shokunin
```

Census, now (the item's frozen command, verbatim):

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kengaku
```

Collision guard (scratch script, `/fast/scratch/hyaku/kengaku-r51/SrcCensus/id-collision.py`,
removed at yield; the logic is quoted in §5 so the result is reproducible):

```sh
python3 id-collision.py --registry <lane>/corpus/SOURCES.md \
  --staged /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md
python3 id-collision.py --registry <lane>/corpus/SOURCES.md \
  --staged /home/vgpnk/Projects/shokuknow/lanes/kengaku/SOURCES-PROPOSED.md
```

Census-level append probe (scratch clone only, reverted in §6):

```sh
# staged rows inserted at the end of the `## Registry` section (before `## Paths`)
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin \
  /fast/scratch/hyaku/kengaku-r51/SrcCensus/kengaku-shokunin
```

No package manager ran. No tool was installed or upgraded this seat (nothing was needed).

## §2 Freeze measurement — `e07f131`

`validate` exit code: **0**. Verbatim stdout (16 lines):

```
kengaku-shokunin	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
kengaku-shokunin	W04	S048 duplicate url aclanthology.org/2020.acl-main.442 across scopes
kengaku-shokunin	W04	S057 duplicate url arxiv.org/abs/2405.11874 across scopes
kengaku-shokunin	W04	S058 duplicate url github.com/UKGovernmentBEIS/inspect_ai/blob/63e45cc52d39b873b944124613da21fdad6f6dcc/src/inspect_ai/scorer/_pattern.py across scopes
kengaku-shokunin	W04	S059 duplicate url www.rfc-editor.org/rfc/rfc8259 across scopes
kengaku-shokunin	W04	S064 duplicate url spec.commonmark.org/0.31.2 across scopes
kengaku-shokunin	W04	S065 duplicate url docs.python.org/3/library/json.html across scopes
kengaku-shokunin	W04	S066 duplicate url doi.org/10.1017/S0950268810000385 across scopes
kengaku-shokunin	W04	S067 duplicate url doi.org/10.1017/S0950268810000385 across scopes
kengaku-shokunin	W04	S068 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json across scopes
kengaku-shokunin	W04	S069 duplicate url raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py across scopes
kengaku-shokunin	W04	S071 duplicate url docs.python.org/3/library/json.html across scopes
kengaku-shokunin	W04	S075 duplicate url docs.python.org/3/library/json.html across scopes
kengaku-shokunin	W04	S076 duplicate url docs.python.org/3/library/json.html across scopes
kengaku-shokunin	W04	S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
kengaku-shokunin	ok	/fast/scratch/hyaku/kengaku-r51/SrcCensus/kengaku-shokunin/corpus/SOURCES.md
```

15 × `W04`, no `E`-code, terminating `ok` line. `W`-codes never change status
(`sources-census.sh` header, lines 17–18).

`census` exit code: **0**. Histograms verbatim:

```
kengaku-shokunin	rows	170
kengaku-shokunin	tier.A	146
kengaku-shokunin	tier.B	22
kengaku-shokunin	tier.C	2
kengaku-shokunin	status.mined	154
kengaku-shokunin	status.queued	8
kengaku-shokunin	status.rejected	8
FLEET	rows	170
FLEET	tier.A	146
FLEET	tier.B	22
FLEET	tier.C	2
FLEET	tier.invalid	0
FLEET	status.queued	8
FLEET	status.mined	154
FLEET	status.rejected	8
FLEET	status.invalid	0
FLEET	missing	0
```

Row/tier/status totals balance: `146 + 22 + 2 = 170` rows; `154 + 8 + 8 = 170` statuses;
`tier.invalid 0`, `status.invalid 0`, `missing 0`.

## §3 Current measurement — `4090c3d`

`validate` exit code: **0**. Verbatim stdout (identical W04 set, live lane label):

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
kengaku	W04	S075 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S076 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
```

`census` exit code: **0**. Histograms verbatim — every value identical to §2:

```
kengaku	rows	170
kengaku	tier.A	146
kengaku	tier.B	22
kengaku	tier.C	2
kengaku	status.mined	154
kengaku	status.queued	8
kengaku	status.rejected	8
FLEET	rows	170
FLEET	tier.A	146
FLEET	tier.B	22
FLEET	tier.C	2
FLEET	tier.invalid	0
FLEET	status.queued	8
FLEET	status.mined	154
FLEET	status.rejected	8
FLEET	status.invalid	0
FLEET	missing	0
```

**Both runs: exit 0, zero `E`-codes, 15 `W04` warnings, 170 rows, tiers 146/22/2, statuses
154/8/8.**

## §4 Why the two measurements agree — blob identity

The registry did not change between the freeze and the tip. `git diff --stat e07f131 4090c3d --
corpus/SOURCES.md` printed nothing, and the blob hashes are equal:

```
$ git -C <lane> rev-parse e07f131:corpus/SOURCES.md 4090c3d:corpus/SOURCES.md
6a6f4954b1a90e55bb67d624b5bc9e0bf2af7350
6a6f4954b1a90e55bb67d624b5bc9e0bf2af7350

$ sha256sum corpus/SOURCES.md ; git show e07f131:corpus/SOURCES.md | sha256sum
8a1ba15597360ea21b2c9b184c26be7827a49d9e0f50d7abae23d9957da2f4eb  corpus/SOURCES.md
8a1ba15597360ea21b2c9b184c26be7827a49d9e0f50d7abae23d9957da2f4eb  -
```

`git status --porcelain corpus/SOURCES.md` printed nothing: the working-tree registry is the
committed one. The freeze→tip commits (`4090c3d`) touched only
`.ufo/waves/round-51/build_spec.py`, `.ufo/waves/round-51/w1-dispatch.json`,
`.ufo/waves/round-51/w1-spec.json`.

## §5 Id-collision check against the staged shokuknow package

**Staged package found for this lane:** `/home/vgpnk/Projects/shokuknow/merge/kengaku/`
(`SOURCES.append.md` 177 759 bytes, `MERGE-REPORT.md`, `MERGE-REPORT.json`,
`knowledge/corpus/knowledge/` with 65 entry files). The package's own report states the registry
it was built against: `MERGE-REPORT.json` → `lane "kengaku"`, `accepted 175`, `refused []`,
`existing_rows 76`, `renumbered []`, `first_id "S077"`, `entries` 65. The lane now holds **170**
rows and ids up to **S177**; the staged rows span **S077–S251**.

**Pattern used (the census parser's own 0–3-leading-space anchor).** `sources-census.sh` states the
tolerance in its header ("Maintained parser accepts 0–3 leading ASCII spaces before Markdown
rows/headings; 4 or more spaces are indented code and ignored") and implements it at lines
609–616, quoted verbatim:

```awk
      if (line ~ /^ {0,3}##[ \t]/) {
        sub(/^ {0,3}/,"",line)
        in_registry=(trim(substr(line,3))=="Registry")
        next
      }
      if (line ~ /^ {0,3}#[ \t]/) { in_registry=0; next }
      if (line !~ /^ {0,3}\|/) next
      sub(/^ {0,3}/,"",line)
```

The id anchor applied to each row is therefore `^ {0,3}\|\s*(S\d{3,})\s*\|` — the same shape as
`plans/pkg_gate.py`'s `SOURCE_ROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")`. The lane list is
taken from the `## Registry` section only (the section the census scopes `E01`–`E12` to); the
staged list is every row-shaped id anywhere in `SOURCES.append.md` (the file carries no headings).

**Tolerance is not load-bearing here (measured, both files):**

```
registry: tolerant(0-3) 170 · column-zero 170 · indented 1-3  0
staged  : tolerant(0-3) 175 · column-zero 175 · indented 1-3  0
```

Both files are column-zero today, so a column-zero-only pattern gives the same counts *on this
data*; the tolerant pattern is still the one used, because it is the parser's own and a future
indented row would be missed otherwise.

**Registry id list (170, `corpus/SOURCES.md` `## Registry`, in file order):**

```
S001 S002 S003 S004 S005 S006 S007 S008 S009 S010 S011 S012 S013 S014 S015 S016 S017 S018 S019 S020
S021 S022 S023 S024 S025 S026 S027 S028 S029 S030 S031 S032 S033 S034 S035 S036 S037 S038 S039 S040
S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051 S052 S053 S054 S055 S056 S057 S058 S059 S060
S061 S062 S063 S064 S065 S066 S067 S068 S069 S070 S071 S072 S073 S074 S075 S076 S077 S078 S079 S080
S090 S091 S081 S082 S083 S084 S085 S086 S092 S093 S100 S094 S097 S101 S102 S103 S104 S105 S106 S107
S108 S109 S110 S111 S112 S113 S114 S115 S116 S117 S118 S119 S120 S121 S122 S123 S124 S125 S126 S127
S128 S129 S130 S131 S132 S133 S134 S135 S136 S137 S147 S148 S138 S139 S140 S141 S142 S143 S144 S145
S146 S149 S150 S151 S152 S153 S154 S155 S156 S157 S158 S159 S160 S161 S162 S163 S164 S165 S166 S167
S168 S169 S170 S171 S172 S173 S174 S175 S176 S177
```

(File order is not numeric order — ids were appended across rounds in a non-monotonic sequence;
`S090 S091` precede `S081`, and `S147 S148` precede `S138`. That is a reading of the file, not a
finding about validity: `E02`/`E03` are about id syntax and duplication, not ordering.)

**Staged id list (175, `merge/kengaku/SOURCES.append.md`, in file order):**

```
S077 S078 S079 S080 S081 S082 S083 S084 S085 S086 S087 S088 S089 S090 S091 S092 S093 S094 S095 S096
S097 S098 S099 S100 S101 S102 S103 S104 S105 S106 S107 S108 S109 S110 S111 S112 S113 S114 S115 S116
S117 S118 S119 S120 S121 S122 S123 S124 S125 S126 S127 S128 S129 S130 S131 S132 S133 S134 S135 S136
S137 S138 S139 S140 S141 S142 S143 S144 S145 S146 S147 S148 S149 S150 S151 S152 S153 S154 S155 S156
S157 S158 S159 S160 S161 S162 S163 S164 S165 S166 S167 S168 S169 S170 S171 S172 S173 S174 S175 S176
S177 S178 S179 S180 S181 S182 S183 S184 S185 S186 S187 S188 S189 S190 S191 S192 S193 S194 S195 S196
S197 S198 S199 S200 S201 S202 S203 S204 S205 S206 S207 S208 S209 S210 S211 S212 S213 S214 S215 S216
S217 S218 S219 S220 S221 S222 S223 S224 S225 S226 S227 S228 S229 S230 S231 S232 S233 S234 S235 S236
S237 S238 S239 S240 S241 S242 S243 S244 S245 S246 S247 S248 S249 S250 S251
```

**Collision count: `COUNT=94`** (94 of 175 staged ids already exist in the registry). Verbatim
tail of the guard:

```
COLLISIONS=S077 S078 S079 S080 S081 S082 S083 S084 S085 S086 S090 S091 S092 S093 S094 S097 S100 S101 S102 S103 …
COUNT=94
REG_COUNT=170 STAGED_COUNT=175 REG_UNIQUE=170 STAGED_UNIQUE=175
```

Collision set, full:

```
S077 S078 S079 S080 S081 S082 S083 S084 S085 S086 S090 S091 S092 S093 S094 S097 S100 S101 S102 S103
S104 S105 S106 S107 S108 S109 S110 S111 S112 S113 S114 S115 S116 S117 S118 S119 S120 S121 S122 S123
S124 S125 S126 S127 S128 S129 S130 S131 S132 S133 S134 S135 S136 S137 S138 S139 S140 S141 S142 S143
S144 S145 S146 S147 S148 S149 S150 S151 S152 S153 S154 S155 S156 S157 S158 S159 S160 S161 S162 S163
S164 S165 S166 S167 S168 S169 S170 S171 S172 S173 S174 S175 S176 S177
```

Decomposition: `S077–S086` (10) + `S090–S094` (5) + `S097` (1) + `S100–S177` (78) = **94**.

Staged ids **not** in the registry: **81** — `S087 S088 S089 S095 S096 S098 S099` (7, ids the lane
never took) and the contiguous `S178–S251` (74, ids beyond the registry's highest). Registry ids
not in the staged package: **76** (`S001–S076`), which matches the package's own
`existing_rows 76`.

**Id reuse, not just id overlap.** For each of the 94 colliding ids the registry row's URL and the
staged row's URL were compared (scheme/`www.` stripped, trailing slash stripped, lowercased):

```
collisions 94  same-url 10  different-url 84
```

So 84 of the 94 collisions are the *same id naming a different document*. Examples (registry →
staged):

```
S091  arxiv.org/abs/2507.02825                                     → jpn.nec.com/techrep/journal/g23/n02/230212.html
S103  github.com/hkust-nlp/toolathlon/.../ab-testing/evaluation/main.py → arxiv.org/pdf/2412.05579
S104  arxiv.org/abs/2412.05579v2                                   → meti.go.jp/.../geniac_kentojyokyo.pdf
S105  raw.githubusercontent.com/harbor-framework/terminal-bench-2/…/test_outputs.py → web.archive.org/web/20251118034714/…/index.html
```

The 10 `same-url` cases are the same document cited at a different URL form (e.g. `S077`
`raw.githubusercontent.com/harbor-framework/terminal-bench/e67a2cb…/docs/task_review_automation.md`
→ `github.com/harbor-framework/terminal-bench/blob/main/docs/task_review_automation.md`), which the
census would also flag as `E04` (duplicate URL+scope) if scopes match.

**Reading:** the staged package is stale. It was built when the lane held 76 rows; the lane has
since absorbed 94 of its ids (84 onto different documents), so appending it verbatim would be an
id collision on almost every row, not an addition.

## §6 Census-level verdict if the package were appended (scratch clone only)

Pattern-level `COUNT=94` is not what `validate` would print: two colliding rows are malformed
before their id is judged. Probe performed in the scratch clone at `e07f131` (toplevel asserted
`/fast/scratch/hyaku/kengaku-r51/SrcCensus/kengaku-shokunin`), by inserting all 175 staged rows at
the end of the `## Registry` section (before `## Paths`, line 193) so that `E12` cannot mask `E03`:

```
EXIT=1
E01 x2    E03 x92    E09 x167    E11 x168    W01 x2    W04 x48
```

- `E01` — the two escaped-pipe rows the round-29/30 lessons name:
  `kengaku-shokunin	E01	S093 fields=12` and `kengaku-shokunin	E01	S101 fields=15`.
- `E03` — **92** duplicate ids = the 94 pattern collisions minus `S093` and `S101`, which fail
  `NF=13` first. First lines verbatim:
  ```
  kengaku-shokunin	E03	S077 duplicate id
  kengaku-shokunin	E03	S078 duplicate id
  kengaku-shokunin	E03	S079 duplicate id
  ```
- `E09 x167` (prose `recheck` cells) and `E11 x168` (used-by paths absent from the tree) reproduce
  the same counts recorded in `corpus/lessons/round-29.md`/`round-30.md` for this package.

The clone was then restored (`git -C "$D" checkout -- corpus/SOURCES.md`, `git status --porcelain`
empty) and re-measured to confirm the scratch tree is back at the freeze state:
`kengaku-shokunin	ok	/fast/scratch/hyaku/kengaku-r51/SrcCensus/kengaku-shokunin/corpus/SOURCES.md`,
exit **0**. Nothing was written to the live lane; `corpus/SOURCES.md` there was never modified.

## §7 Second staged surface for the same lane (measured, secondary)

`/home/vgpnk/Projects/shokuknow/lanes/kengaku/SOURCES-PROPOSED.md` also carries row-shaped ids
(14 of them, `S077–S090`), i.e. a narrower earlier staging of the same id range:

```
STAGED_IDS=S077 S078 S079 S080 S081 S082 S083 S084 S085 S086 S087 S088 S089 S090
COLLISIONS=S077 S078 S079 S080 S081 S082 S083 S084 S085 S086 S090
COUNT=11
```

11 of its 14 ids collide with the registry (the 3 non-colliding are `S087 S088 S089`).

## §8 Out-of-scope observation (recorded, not claimed)

The package's `knowledge/corpus/knowledge/` holds 65 entry files; 4 of those filenames already
exist in the lane's `corpus/knowledge/` (`benchmark-grader-semantics.md`,
`benchmark-task-validity-checklist.md`, `benchmark-verifier-execution-model.md`,
`contamination-transparency-card.md`; the lane holds 54 files). A filename collision is not an id
collision and this seat did not evaluate entry content — flagged only so the L1 can route it.

## §9 Limits

- The census measures only what the lane's own registry declares; it says nothing about whether a
  row's `teaches`/`anchor` text is true. `W04` is a warning class and does not affect exit status.
- The id-collision count is a set intersection of pattern matches. It does not judge whether an
  overlapping row is semantically the same source; the URL comparison in §5 is a normalisation
  heuristic (scheme/`www.`/trailing slash only), so `same-url 10` is a lower bound on "same
  document" and `different-url 84` is an upper bound on "different document".
- The §6 probe is a hypothetical append in scratch, not a statement about what the operator should
  append. It is a single-point measurement with the default `--today` (`date -u +%F` = 2026-10-28).
- The staged package is dated 2026-10-24 (files `mtime`); the lane may have absorbed further rows
  since. Nothing here was appended to the registry, as instructed.

## §10 Scratch

Scratch root `/fast/scratch/hyaku/kengaku-r51/SrcCensus` (NVMe; `df -h /fast` showed
`804G total, 249G used, 555G avail, 31%` at start) held the `--shared` clone, the guard script and
the captured outputs. It was removed before yield; every number above is transcribed into this
report, which is the citable artifact.

VERDICT: both census runs agree — `validate` exit **0** at `e07f131` and at `4090c3d`, no `E`-code, 15 `W04` warnings, rows 170 (tier A/B/C = 146/22/2; status mined/queued/rejected = 154/8/8), registry blob identical (`6a6f4954…`). Staged shokuknow package `merge/kengaku/SOURCES.append.md` collides on **94 of 175** ids (census-level: `E03` 92 plus `E01` 2), 84 of them onto a different document; the package is stale against a 170-row registry and must not be appended verbatim. Nothing appended to the registry; lane untouched; scratch removed.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
REV e07f131cf7037e58a21db6e1f3986cf401ad257c
