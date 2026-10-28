# C1ScribeProvince — the round-51 `PROVINCE.md` correction block (drafted, not landed)

Seat: `C1ScribeProvince` (scribe). Lane: `kengaku-shokunin`. Claim: **R51-C1** (freshness 8 → 9).
Read first: `plans/round-51-claims.md` (full), `plans/round51_surfaces.py` (all 364 lines),
`plans/round51-surfaces.json` (19 entries), `.ufo/waves/round-51/claims/c1-before.txt`.

**This seat did not edit `PROVINCE.md`.** The block below is the exact markdown the L1 lands; every
claim in it was validated against the frozen counter in a scratch clone, and against
`plans/state_check.py` (a second frozen instrument the C1 repair can silently break — §6).

`REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7` (lane `master`). Instrument bytes are the freeze
bytes:

```sh
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff --stat \
  e07f131cf7037e58a21db6e1f3986cf401ad257c HEAD -- \
  PROVINCE.md plans/round51-surfaces.json plans/round51_surfaces.py   # empty, rc 0
sha256sum PROVINCE.md plans/round51-surfaces.json plans/round51_surfaces.py
# 5e00336ff4ce2edb79346c4021e5bec24e5a6490ef5ccc53bd81fe5b6f7a5298  PROVINCE.md
# 60d05a0a3f5b099061a902fac7612cd178c8dda01680ac04b84611a77fcf2dd8  plans/round51-surfaces.json
# edf09db7be767a29bac4a645185f2f87452ec1451322d9e723ca65111f53e01e  plans/round51_surfaces.py
```

## Axes named

1. **freshness / R51-C1** (judged axis) — does the landed text stop asserting that four dead
   surfaces resolve, and does the registry row stop asserting a stale count?
2. **instrument coherence** — a `PROVINCE.md` correction is a text edit to a document two frozen
   instruments read. A correction that clears C1 while reddening `plans/state_check.py` is not a
   move; this axis found and bounded that collision (§6).
3. **append-only reachability** — can the repair reach `PREDICATE R51-C1 pass` without deleting a
   row, rewriting a historical figure, or moving a pinned line?

## 1. What the frozen counter actually binds (measured, and it changes the deliverable)

`python3 plans/round51_surfaces.py --lane .` at `4090c3db` is **byte-identical to
`.ufo/waves/round-51/claims/c1-before.txt` apart from the `REV` line**:

```sh
diff <(sed 's/^REV .*/REV X/' .ufo/waves/round-51/claims/c1-before.txt) \
     <(sed 's/^REV .*/REV X/' /fast/scratch/hyaku/kengaku-r51/C1ScribeProvince/tip-counter.txt)
# no output
```

Verbatim at the tip (exit 1):

```
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
  DETAIL DRIFT SF01 prose=present state=absent (...)
  DETAIL DRIFT SF02 prose=present state=absent (...)
  DETAIL DRIFT SF03 prose=present state=absent (...)
STALE 0
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
```

**Binding fact.** `DRIFT` is computed as `e["prose"] != e["state"]` and `NUMBER-DRIFT` as
`count_claim != probed count` — both read **manifest fields only** (`check()`, lines 190–200 of the
frozen counter). The counter never parses a numeral or a truth claim out of a `PROVINCE.md` row. The
`UNVERDICTED` leg is the only one that reads row text, and only for `ABSENT <ISO date>`.

Consequence, proven in §7 run A: **the `PROVINCE.md` block alone cannot clear `DRIFT` or
`NUMBER-DRIFT`.** The landing must also edit `plans/round51-surfaces.json` (`SF01`–`SF03`
`prose: present → absent`; `SF14` `count_claim: 25 → 170`). Both obligations are independent and
only the manifest half is machine-checked — the row edit is the truth half.

## 2. (a) Inline dated markers — exact edits, anchored to current row text

Each edit is an append **inside the row's existing final cell**, before the closing ` |`. No row is
added or deleted; the line count of `PROVINCE.md` is unchanged by (a) and (c). Anchors are unique at
`5e00336f…`; each replacement count was asserted `== 1` by the applier before writing.

### SF01 — `PROVINCE.md:12`, Research notes (row already carries a `2026-10-20` marker that dates the *fallback* path, not the primary one)

OLD (row tail):

```
the `~/wikillm/llm-wiki` path does **not** exist here (`test -e` → absent) **ABSENT 2026-10-20** (round 25: first local path fails `test -e`; superseded by §Province map) |
```

NEW (row tail):

```
the `~/wikillm/llm-wiki` path does **not** exist here (`test -e` → absent) **ABSENT 2026-10-20** (round 25: first local path fails `test -e`; superseded by §Province map) **ABSENT 2026-10-28** (round 51: the row's own primary path `~/Projects/webzites/repos/llm-wiki` fails `test -e`; the 2026-10-20 marker above dates the `~/wikillm/llm-wiki` fallback, not this cell — receipt `.ufo/waves/round-51/claims/c1-before.txt` DRIFT SF01) |
```

### SF02 — `PROVINCE.md:13`, Local benchmark battery

OLD:

```
but historical commands using the old path are frozen evidence **ABSENT 2026-10-20** (round 25: first local path fails `test -e`; superseded by §Province map) |
```

NEW:

```
but historical commands using the old path are frozen evidence **ABSENT 2026-10-20** (round 25: first local path fails `test -e`; superseded by §Province map) **ABSENT 2026-10-28** (round 51: `~/archive/bench-arena` itself fails `test -e`, so the "all resolve at the archive path" assertion above is superseded — receipt `.ufo/waves/round-51/claims/c1-before.txt` DRIFT SF02) |
```

### SF03 — `PROVINCE.md:14`, Served local model

OLD:

```
hermetic gates pin committed bytes, never `/proc` **ABSENT 2026-10-20** (round 25: first local path fails `test -e`; superseded by §Province map) |
```

NEW:

```
hermetic gates pin committed bytes, never `/proc` **ABSENT 2026-10-20** (round 25: first local path fails `test -e`; superseded by §Province map) **ABSENT 2026-10-28** (round 51: `http://127.0.0.1:34113/health` refuses the connection, so no served model answers; the round-25 "first local path" clause does not apply to an endpoint row — receipt `.ufo/waves/round-51/claims/c1-before.txt` DRIFT SF03) |
```

### SF04 — `PROVINCE.md:15`, Route telemetry (the `UNVERDICTED` leg: `**ABSENT**` with no ISO date)

OLD:

```
model×lane and reroute-chain **historical inference about model service** only; never treat the path as live |
```

NEW:

```
model×lane and reroute-chain **historical inference about model service** only; never treat the path as live **ABSENT 2026-10-28** (round 51: `test -e ~/Projects/bounties/ledger/telemetry.jsonl` fails; this dates the round-14 ABSENT that carried only a round number — receipt `.ufo/waves/round-51/claims/c1-before.txt` UNVERDICTED SF04) |
```

Marker-form note: the frozen counter's `ABSENT_RE` is `ABSENT\s+(\d{4}-\d{2}-\d{2})` (unbolded, any
position in the row) while `plans/state_check.py`'s `ABSENT_MARK_RE` is
`\*\*ABSENT(?: \d{4}-\d{2}-\d{2})?\*\*` (bolded). The bold form above satisfies **both**; an
unbolded `ABSENT 2026-10-28` would satisfy C1 and leave state_check's P2d rule untouched only
because the rows already carry bolded markers — do not rely on that, use the bold form.

## 3. (b) New section — exact markdown, appended at EOF

Append after `PROVINCE.md`'s last line (round-46 paragraph, line 648 at `5e00336f…`), separated by
one blank line. Nothing above it moves.

```markdown
## Round-51 surface re-verification (2026-10-28)

*Appended by round 51 (seat `C1ScribeProvince`, L1 `KengakuR51`). Every row of `## Surfaces` and
`### Core` above was re-probed; this section is the current reading and leaves the round-14 table
and the round-24/25 map in place as the historical record. One manifest entry per table row
(`plans/round51-surfaces.json`), no row deleted, and no row added without an entry.*

Counting command, as frozen in `plans/round-51-claims.md` §C1:

    python3 plans/round51_surfaces.py --lane .

Reading at `4090c3db79d11279ab5e5121ba25e74aa316e6e7` (and identical to
`.ufo/waves/round-51/claims/c1-before.txt` at `297e17927ba9342a87ba27a48cc5270a001de7cb`):

    ANCHORS total=19 dup=0 missing=0
    ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
    ROWS section="### Core" rows=10 entries=10 uncovered=0
    PROBES run=19 present=13 absent=6 errors=0
    RESOLVE observed_present=13 floor=13 verdict=met

Registry count, re-derived independently: `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → `170`.

Registry number chain, kept append-only: `PROVINCE.md:112` still carries its round-24 `25 rows`
reading, now with a dated supersession marker in the same cell; the round-25 note at `:119`
("holds 37 after round 25") and the round-26 corrections R26-E3/E3a/E3b/E7/E8/E9/E10 at `:174`–`:190`
(`rows=42`, `id_set=exact`) stay true as **dated frozen populations** — `42` counts the ids
`S001`–`S042`, not the live file. The live count is **170** S-rows at 2026-10-28. No earlier figure
is deleted or rewritten, and the correction lines stay below the append-only floor that
`plans/state_check.py` enforces for `PROVINCE.md` (`P3_CORRECTION_FLOORS` → 173).

The landing measurement of the same command writes `.ufo/waves/round-51/claims/c1-after.txt`; its
`PREDICATE R51-C1 pass` line supersedes the `PREDICATE R51-C1 fail` line of the before receipt,
and every row below cites the before receipt that carries its observed state.

| Surface | Probe run | Observed 2026-10-28 | Receipt |
|---|---|---|---|
| SF01 Research notes | `test -e ~/Projects/webzites/repos/llm-wiki` | absent — path missing | `.ufo/waves/round-51/claims/c1-before.txt` |
| SF02 Local benchmark battery | `test -e ~/archive/bench-arena` | absent — path missing | `.ufo/waves/round-51/claims/c1-before.txt` |
| SF03 Served local model | `curl -s http://127.0.0.1:34113/health` | absent — connection refused | `.ufo/waves/round-51/claims/c1-before.txt` |
| SF04 Route telemetry | `test -e ~/Projects/bounties/ledger/telemetry.jsonl` | absent — path missing | `.ufo/waves/round-51/claims/c1-before.txt` |
| SF05 Client CLI telemetry | `test -e ~/.bailian/telemetry.jsonl` | absent — path missing | `.ufo/waves/round-51/claims/c1-before.txt` |
| SF06 Model catalogs (local) | `test -e ~/.bailian/skills/bailian-docs-llm-wiki/models/index.md` | absent — path missing | `.ufo/waves/round-51/claims/c1-before.txt` |
| SF07 Own probe artifacts | `test -d` over 5 evidence dirs | present — 5/5 resolve | `.ufo/waves/round-51/claims/c1-before.txt` |
| SF08 In-repo gate | `test -e grader.py` | present | `.ufo/waves/round-51/claims/c1-before.txt` |
| SF09 Public literature (anchor file) | `test -e corpus/knowledge/eval-prior-art-calibration.md` | present | `.ufo/waves/round-51/claims/c1-before.txt` |
| SF10 In-repo verdict gate | `sha256sum grader.py` | present — `90c87c88…` matches pin | `.ufo/waves/round-51/claims/c1-before.txt` |
| SF11 Own probe artifacts (Core loop) | `test -d` over 7 evidence dirs | present — 7/7 resolve | `.ufo/waves/round-51/claims/c1-before.txt` |
| SF12 Attribution instrument | `sha256sum plans/attrib_probe.py` | present — `489f938a…` matches pin | `.ufo/waves/round-51/claims/c1-before.txt` |
| SF13 Corpus gate docs | `test -e corpus/QUALITY.md` | present | `.ufo/waves/round-51/claims/c1-before.txt` |
| SF14 Public-literature registry | count probe over `corpus/SOURCES.md` | present — rows=170 | `.ufo/waves/round-51/claims/c1-before.txt` |
| SF15 ds-flash-shim source | `sha256sum ~/.local/share/ds-flash-shim/shim.py` | present — `42d86d99…` matches pin | `.ufo/waves/round-51/claims/c1-before.txt` |
| SF16 Live probe endpoint | `ss -ltn 'sport = :8791'` | present — LISTEN on `127.0.0.1:8791` | `.ufo/waves/round-51/claims/c1-before.txt` |
| SF17 Public literature (citation files) | `test -e` over 2 knowledge files | present — 2/2 resolve | `.ufo/waves/round-51/claims/c1-before.txt` |
| SF18 Interval re-verdict instrument | `test -e plans/attrib_calibration.py` | present | `.ufo/waves/round-51/claims/c1-before.txt` |
| SF19 State-assertion check | `test -e plans/state_check.py` | present | `.ufo/waves/round-51/claims/c1-before.txt` |
```

Per-surface observed states in that table are the frozen probe's own readings, extracted by
importing the frozen module and calling its `probe()` (read-only):

```
SF01 ## Surfaces absent   missing: ~/Projects/webzites/repos/llm-wiki
SF02 ## Surfaces absent   missing: ~/archive/bench-arena
SF03 ## Surfaces absent   http://127.0.0.1:34113/health -> <urlopen error [Errno 111] Connection refused>
SF04 ## Surfaces absent   missing: ~/Projects/bounties/ledger/telemetry.jsonl
SF05 ## Surfaces absent   missing: ~/.bailian/telemetry.jsonl
SF06 ## Surfaces absent   missing: ~/.bailian/skills/bailian-docs-llm-wiki/models/index.md
SF07 ## Surfaces present  all 5 targets resolve
SF08 ## Surfaces present  all 1 targets resolve
SF09 ## Surfaces present  all 1 targets resolve
SF10 ### Core   present  digest 90c87c88… matches pin
SF11 ### Core   present  all 7 targets resolve
SF12 ### Core   present  digest 489f938a… matches pin
SF13 ### Core   present  all 1 targets resolve
SF14 ### Core   present  SOURCES rows=170
SF15 ### Core   present  digest 42d86d99… matches pin
SF16 ### Core   present  LISTEN on 127.0.0.1:8791
SF17 ### Core   present  all 2 targets resolve
SF18 ### Core   present  all 1 targets resolve
SF19 ### Core   present  all 1 targets resolve
```

Independent host probes, same run:

```sh
test -e "$HOME/Projects/webzites/repos/llm-wiki"   # ABSENT
test -e "$HOME/archive/bench-arena"                # ABSENT
test -e "$HOME/Projects/bounties/ledger/telemetry.jsonl"  # ABSENT
curl -sS http://127.0.0.1:34113/health             # curl: (7) Failed to connect ... Could not connect to server
ss -ltn 'sport = :8791'                            # LISTEN 0 512 127.0.0.1:8791 0.0.0.0:*
```

**Receipt obligation.** `.ufo/waves/round-51/claims/` today holds only `c1-before.txt` and
`c2-before.txt`; `c1-after.txt` does not exist. The sentence naming it is a landing instruction, not
a citation. If the L1 lands without writing that file, delete that sentence (or repoint it at the
evidence file the landing actually writes) — do not leave the document citing a path that is absent.

## 4. (c) Registry numeric correction — `PROVINCE.md:112`

The count `C1ExecCounts` measures is **170**, and this seat re-derived it independently, three ways:

```sh
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md      # 170
grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md                           # 170
python3 -c "import re,pathlib;print(len(re.findall(r'^\|\s*S[0-9]{3,}\s*\|',pathlib.Path('corpus/SOURCES.md').read_text(),flags=re.M)))"   # 170
```

`C1ExecCounts` reports the same (`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-51/w1/C1ExecCounts.md` §1:
`Verdict: DISAGREES — 25 vs 170`, 170 unique ids, `S001`–`S177`, 0 duplicates).

**Form: dated supersession inside the cell, not a rewrite of the numeral.** Rationale measured, not
preferred: `plans/state_check.py` derives `P3b.province.public-literature-registry.rows` from the
row's **first** `\b(\d+)\s+rows?\b` match. Rewriting `25 rows` → `170 rows` changes that recorded
claim from `["25"]` to `["170"]` (verified, §7 run D); the verdict stays `SUPERSEDED` either way, but
the append-only form keeps the historical figure and the assertion's claim token exactly as the
round-25/26 record left them.

OLD:

```
present; 25 rows, contract-v1 census clean
```

NEW:

```
present; 25 rows (**superseded 2026-10-28: 170 rows** — the live registry count at round 51; see §Round-51 surface re-verification), contract-v1 census clean
```

No new line is inserted before the round-26 correction block; the `25`/`37`/`42` figures stay as the
dated frozen populations that R26-E3/E3a/E3b/E7/E8/E9/E10 record (`rows=42` counts `S001`–`S042`).

## 5. Landing prerequisites outside my scope (each proven necessary or sufficient)

| # | File | Edit | Why |
|---|---|---|---|
| P1 | `plans/round51-surfaces.json` | `SF01`, `SF02`, `SF03`: `"prose": "present"` → `"absent"` | `DRIFT` compares manifest `prose` to manifest `state`; the row text cannot move it (§1, §7 run A) |
| P2 | `plans/round51-surfaces.json` | `SF14`: `"count_claim": 25` → `170` | `NUMBER-DRIFT` compares `count_claim` to the live probe |
| P3 | `.ufo/waves/round-51/claims/c1-after.txt` | write the landing measurement | §3's citation |
| P4 | `plans/round51-surfaces.json` + `PROVINCE.md` | 20th surface, only if the L1 keeps that target | §6 |

## 6. Placement constraint found: `PROVINCE.md:129` is pinned by a second instrument

`plans/state_check.py` pins `P3C_PINS = (4, "PROVINCE.md:129", 129, "### Adjacent", None)`: it reads
`SHONEN.md`'s box-4 evidence pointer, requires it to be **exactly** `PROVINCE.md:129`, and requires
line 129 of `PROVINCE.md` to contain exactly one `### Adjacent`. Therefore:

- any inserted line **above** line 129 breaks `P3c.box.4.pointer.1` → `state_check --summary` FAIL;
- repointing `SHONEN.md` at the moved line also fails (`pointer_count=0`), because the pin demands
  the literal `PROVINCE.md:129`.

Measured, in the scratch clone at `4090c3db`:

```
# candidate block + C1ExecNewSurface's SF20 row appended as the last `## Surfaces` row (line 21):
ANCHORS total=20 dup=0 missing=0
ROWS section="## Surfaces" rows=10 entries=10 uncovered=0
PROBES run=20 present=14 absent=6 errors=0
PREDICATE R51-C1 pass                       <- C1 is happy
MISMATCH: P3c.box.4.pointer.1:12 — {..., "target_line": 129, "token_hits": 0, "line_text": "<blank>"}
VERDICT: FAIL — at least one frozen assertion mismatches     <- state_check is not
```

So the block in §2–§4 is deliberately line-count-neutral above 129 (all four markers and the
registry correction are in-place; the new section is at EOF). **A 20th surface row cannot go into
either declared table.** The compatible placement, measured to pass both instruments:

```
ANCHORS total=20 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
ROWS section="### Round-51 admitted surface (2026-10-28)" rows=1 entries=1 uncovered=0
PROBES run=20 present=14 absent=6 errors=0
RESOLVE observed_present=14 floor=13 verdict=met
PREDICATE R51-C1 pass
VERDICT: PASS — all comparable frozen assertions match
```

i.e. put SF20's row in a new `### Round-51 admitted surface (2026-10-28)` subsection **after** line
129, add that heading to the manifest's `sections`, and set the SF20 entry's `section` to it. That
keeps `## Surfaces` at 9 rows (kill rule: ≥9) and leaves line 129 alone. The predicate does not
require a 20th surface (`RESOLVE` is a floor of 13); the claims' *after target* prose does.

## 7. Verification of this draft (scratch only, no lane write)

Scratch: `/fast/scratch/hyaku/kengaku-r51/C1ScribeProvince` (`TMPDIR` exported there; clone
`git clone --shared`, `git -C "$D" rev-parse --show-toplevel` asserted equal to `$D`,
`HEAD=4090c3db79d11279ab5e5121ba25e74aa316e6e7`).

| Run | Tree | Command | Result |
|---|---|---|---|
| A | block only, original manifest | `python3 plans/round51_surfaces.py --lane . --province PROVINCE.candidate2.md` | `DRIFT 3`, `UNVERDICTED 0`, `NUMBER-DRIFT 1`, `PREDICATE R51-C1 fail`, exit 1 |
| B | block + P1 + P2 | same, `--manifest manifest.candidate.json` | `DRIFT 0 STALE 0 UNVERDICTED 0 NUMBER-DRIFT 0 ANCHOR-DUP 0 ANCHOR-MISSING 0 UNCOVERED 0 SECTION-MISSING 0`, `ROWS 9/10`, `RESOLVE observed_present=13 floor=13 verdict=met`, `PREDICATE R51-C1 pass`, exit 0 |
| C | B + SF20 inline (line 21) | `python3 plans/state_check.py --root . --summary` | `MISMATCH: P3c.box.4.pointer.1:12`, `VERDICT: FAIL` |
| D | B + SF20 in a tail subsection | both commands | C1 `PREDICATE R51-C1 pass` (present=14); state_check `VERDICT: PASS — all comparable frozen assertions match`; `sed -n '129p' PROVINCE.md` → `### Adjacent` |
| E | baseline, pristine `4090c3d` clone | `python3 plans/state_check.py --root . --summary` | `VERDICT: PASS — all comparable frozen assertions match` |

Run A is the load-bearing negative: the `PROVINCE.md` block alone leaves `DRIFT 3` and
`NUMBER-DRIFT 1`. Run D is the load-bearing positive: with P1+P2 the block reaches
`PREDICATE R51-C1 pass` **and** leaves the other frozen instrument green. Row counts never fall
below 9/10, no anchor goes missing, and `ANCHOR-DUP 0` throughout.

## 8. Observations the landing must not skip

1. **Transient count reading (unexplained, reproducible-warning).** At 15:22 local the same frozen
   command printed `DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=0` and
   `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` printed `0`, while
   `ls -la corpus/SOURCES.md` showed mtime `Oct 28 15:22`. One minute later the same two commands
   printed `170`, and `md5sum corpus/SOURCES.md` equalled
   `git show master:corpus/SOURCES.md | md5sum` (`46a60900e7794f8f22ce7ad8c6ebd07a`). Something
   rewrote the lane file mid-wave. Nothing in this seat wrote to the lane. **Before pinning
   `count_claim: 170`, the landing must re-measure with `git status --porcelain corpus/SOURCES.md`
   empty**; a `rows=0` reading is a truncated/absent file, not a count.
2. **`c1-after.txt` does not exist** — see §3's receipt obligation.
3. **The four markers cite the before receipt**, whose `DRIFT`/`UNVERDICTED` detail lines name
   exactly `SF01`, `SF02`, `SF03`, `SF04`. That is the receipt each line cites; the after receipt
   should show those four names absent from every problem list.
4. **`733 checks`, `28` root receipt logs, `12` evidence dirs and `S0–S7`** are true but
   un-machine-checked (the counter has no subprocess probe). They are `C1ExecCounts`'s item, not
   this block's; this block deliberately touches none of them.
5. **No tool was installed or upgraded** this seat (no `pacman`, no `uv tool`, no binary fetch).

## 9. Addendum (15:37 local) — the registry count is a moving target during this wave

`corpus/SOURCES.md` is being written by another seat while this report is being drafted. Measured,
read-only, minutes after the §1–§8 runs:

```sh
git status --porcelain corpus/SOURCES.md   #  M corpus/SOURCES.md
git diff --stat corpus/SOURCES.md          #  corpus/SOURCES.md | 1 +
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md   #  171
git diff corpus/SOURCES.md | grep '^+|'    #  +| S178 | llama.cpp server API reference … served-endpoint-identity-pin.md
```

So the count is `170` on the committed tree at `4090c3db` and `171` in the working tree with the
in-flight `S178` row (`corpus/knowledge/served-endpoint-identity-pin.md`). This is the same lane
state that produced the `rows=0` transient in §8.1.

**Rule for the landing, therefore:** the numeral in §3's `SF14` row and §4's marker is not `170`
by right; it is **whatever the frozen probe reads at the landing tip, after every wave edit to
`corpus/SOURCES.md` has landed, with `git status --porcelain corpus/SOURCES.md` empty**. Measure it
twice (the counter's `SOURCES rows=N` detail and `grep -cE`), and put the same `N` in
`plans/round51-surfaces.json` `SF14.count_claim`. The draft's `170` is the value at `4090c3db`; if
`S178` lands, both places read `171`.

## Limits

- One surface family (the two declared tables) is corrected here. Surfaces `PROVINCE.md` declares
  outside those tables (`## Refusals`, `## Frontier`, `## Province map` prose) are invisible to the
  counter and untouched by this block — `C1ScoutSurfaces` owns that enumeration.
- The block was validated against the frozen instruments at `4090c3db`; it was **not** landed, so
  the "after" numbers in §7 are candidate-tree numbers, not a landing measurement.
- `prose` values and `count_claim` are manifest fields the L1 must change; this seat only proved
  which values make the counter pass.
- Point-in-time host state: `:34113` and `~/archive/bench-arena` are absent *now*; if either returns,
  the manifest `state` goes `STALE` — the counter's intended behaviour.

`REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7`

VERDICT: PASS — the correction block is drafted exactly, anchored to the current row text, proven
necessary-and-sufficient in a scratch clone (block alone still fails: `DRIFT 3`, `NUMBER-DRIFT 1`;
block + the two manifest edits reaches `PREDICATE R51-C1 pass` at exit 0 with `ROWS 9/10` intact),
and proven not to redden the lane's other frozen instrument (`plans/state_check.py` PASS) provided
nothing is inserted above `PROVINCE.md:129` — the constraint that rules out the inline 20th-surface
row and gives the tail-subsection placement instead; the registry numeral is the landing-tip
measurement (§9), not this draft's `170`.
