# Round 51 · ScribeSourcesAppend — the SOURCES.md append block for the rows this round opens

Seat: `ScribeSourcesAppend` (scribe, leaf — no subagent dispatch). Lane:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`, read-only. Judged axis: **adjacency**.
Scope: draft the exact append block for the two rows round 51 opens (`SrcLlamaServer`,
`SrcHFRevision`), validate it against the fleet census in scratch, and report the exit code and any
E03/E04 finding. **The lane registry was not edited by this seat.**

## Axes named (Godspeed)

1. **adjacency** — a row's `used-by` cell is a citation, not a routing note: it may name an entry
   only when that entry cites the row, and a `mined` row is `mined` because something cites it.
2. **cell integrity** — 11 columns, no `|` inside any cell, `status`/`recheck` inside the contract's
   vocabularies, ids that do not collide with the committed registry.
3. **landability** — measured against the fleet census *and* the lane's own pre-append gate, on
   scratch copies, in every registry state that existed during the run (`4090c3d`, the L1's working
   tree, the landing tip `11e7938`).
4. **non-absorption** — no production file touched; the block is handed to the L1.

## Revision measured

```
REV 11e79380d33d6e811f0010f2a2a0c22a3cdc359e
```

Chain read at 18:40Z: `11e7938 round-51: C1 surface truth landed … and C2 routed-finding
attribution` ← `2cec536 round-51: inherit round-50 wave outputs` ← `4090c3d round-51: v2 wave spec
(64 seats) + validated dispatch payload` ← `e07f131 round-51: stage-1 freeze …`. The stage-1 freeze
is an ancestor of the tip.

**The registry moved under this seat twice while it worked**, so three states are measured:

| state | observed | registry | what it means for the block |
|---|---|---|---|
| `4090c3d` (wave-spec tip) | 18:23Z | 170 rows, last `S177` | Block A (both rows) is valid here |
| working tree, same HEAD | 18:36Z | 171 rows — ` M corpus/SOURCES.md`, S178 appended but uncommitted | Block B (HF row as `S179`) is valid here |
| `11e7938` (landing tip) | 18:40Z | 171 rows, S178 **committed**; `corpus/knowledge/served-endpoint-identity-pin.md` **committed** (4417 bytes) | **Block B is the block to land** |

The landed S178 is a llama.cpp row pinned at tag **`b7200`**, not at the `v0.8.0` pin
`SrcLlamaServer` proposed. Both pins are truthful (verified below); they are the same document, so
only one may be registered.

## Binding inputs read before any draft

| path | what was read |
|---|---|
| `plans/round-51-claims.md` | full file (C1 freshness, C2 adjacency, predicates, controls, limits) |
| `corpus/SOURCES.md` | header, contract-v1 tiers/kinds/statuses, the whole registry (S001–S177 at HEAD; S178 as landed), `## Paths` / `## Search log` / `## Leads` |
| `.ufo/waves/round-51/w1/SrcLlamaServer.md` | proposed row, anchors, five located quotes, byte digest, findings |
| `.ufo/waves/round-51/w1/SrcHFRevision.md` | proposed row (refusal), the 404 matrix, the mechanism-page alternative |
| `.ufo/waves/round-51/w1/C1ScribeKnowledge.served-endpoint-identity-pin.md` | the knowledge entry fragment; its line 1 is `source: corpus/SOURCES.md S178 — …` |
| `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` | `validate` mode: E01–E12, W01–W04, `--file` target resolution, `usedby_findings()` |
| `plans/sources_adopt.py` | the lane's pre-append gate: 11 cells, collisions, `used-by` rewrite, `not-mined` refusal |

## The append block

### Block A — against HEAD `4090c3d` (170 rows): both rows this round opens

Insert as the last two rows of the `## Registry` table, immediately **before** the `## Paths` heading
(`corpus/SOURCES.md:193` at `4090c3d`):

```markdown
| S178 | llama.cpp HTTP server (`llama-server`) API documentation — https://github.com/ggml-org/llama.cpp/blob/8642541b255bfb5dc39cd351a178be09013a55d6/tools/server/README.md | docs | A | the llama.cpp server's own `/v1/models`, `/props` and `/health` contracts, and the `--model`/`--alias` flags that name the served model | `tools/server/README.md` L100, L190, L480-494, L930-1024, L1345-1404 at tag v0.8.0 (commit `8642541b255bfb5dc39cd351a178be09013a55d6`, sha256 `8fd5abde`) | `/v1/models` returns exactly one entry, whose `id` is the `-m` file path unless `--alias` renames it; `/props` reports `model_path`, `total_slots` (`--parallel`), `build_info`; `/health` is public and answers 503 while loading, else 200 ok | mined | 2026-10-28 | 90d | corpus/knowledge/served-endpoint-identity-pin.md |
| S179 | Hugging Face Hub docs — the model-revisions page named for the model-identity pin claim, canonical https://huggingface.co/docs/hub/model-revisions | docs | B | refused correction record: the named page does not resolve on 2026-10-28 at any tested URL, so no anchored quote exists to admit; not an admitted citation and not support for any claim | no anchor — the page is absent, not unread: HTTP 404 at the canonical URL and at its `.md` twin (body 52007 bytes, sha256 `10000fed…`), 0 of 274 entries in `huggingface/hub-docs` `docs/hub` carry `model-revisions`, and the Hub docs index `llms.txt` (277 pages) has 0 lines matching `revis` | REJECTED: the page cannot be fetched, so nothing grounds the pin sentence; the live Hub docs instead permit a tag as a `revision` (`hub/transformers.md:89`), so the prescription is lane policy over the ref-to-commit mechanism, not vendor text; flip: a page at a resolving canonical URL that states the ref-to-commit distinction must be opened as a NEW row id with its own located quote — candidate `https://huggingface.co/docs/hub/local-cache` section `refs/`, fetched 2026-10-28, sha256 `2f13a05e…` | rejected | 2026-10-28 | 90d | — |
```

### Block B — against the landing tip `11e7938` (171 rows, S178 and its knowledge entry committed)

Only the second row is still to append; it takes id **`S179`**, unchanged:

```markdown
| S179 | Hugging Face Hub docs — the model-revisions page named for the model-identity pin claim, canonical https://huggingface.co/docs/hub/model-revisions | docs | B | refused correction record: the named page does not resolve on 2026-10-28 at any tested URL, so no anchored quote exists to admit; not an admitted citation and not support for any claim | no anchor — the page is absent, not unread: HTTP 404 at the canonical URL and at its `.md` twin (body 52007 bytes, sha256 `10000fed…`), 0 of 274 entries in `huggingface/hub-docs` `docs/hub` carry `model-revisions`, and the Hub docs index `llms.txt` (277 pages) has 0 lines matching `revis` | REJECTED: the page cannot be fetched, so nothing grounds the pin sentence; the live Hub docs instead permit a tag as a `revision` (`hub/transformers.md:89`), so the prescription is lane policy over the ref-to-commit mechanism, not vendor text; flip: a page at a resolving canonical URL that states the ref-to-commit distinction must be opened as a NEW row id with its own located quote — candidate `https://huggingface.co/docs/hub/local-cache` section `refs/`, fetched 2026-10-28, sha256 `2f13a05e…` | rejected | 2026-10-28 | 90d | — |
```

**This is the block I recommend landing**, because S178 is committed at the tip as a verified
llama.cpp row at tag `b7200` (see finding 3). Landing Block A on top of that tree would put two rows
for one document in the registry, and the census would not stop it (finding 4).

### Why the statuses are `mined` / `rejected`, not `queued`

- **S178 `mined`** — `corpus/knowledge/served-endpoint-identity-pin.md` cites it by id on line 1
  (`source: S178 — llama.cpp server API reference, tools/server/README.md @ tag b7200 …`). At the
  landing tip that entry is committed (4417 bytes) and its only `S1xx` reference is `S178`: grep for
  `S179`/`S180` in it returns nothing. It was drafted by seat `C1ScribeKnowledge` (wave fragment
  `.ufo/waves/round-51/w1/C1ScribeKnowledge.served-endpoint-identity-pin.md`, 12536 bytes) and
  shortened by the L1 on landing; the citation survives the shortening.
- **S179 `rejected`** — the item's parenthetical (`queued`, or `mined` when cited) has no third case,
  but `SrcHFRevision`'s item binds the failure branch: *"If the page cannot be fetched, record the
  failure and propose the row as a rejection with its flip condition instead — do not invent a
  quote."* The page 404s at the canonical URL, at its `.md` twin, at its `/en/` twin, and does not
  exist among the 274 files of `huggingface/hub-docs` `docs/hub`; there is no quote to anchor a
  `queued` row, and `corpus/SOURCES.md`'s own header says *"A row is a claim made only after opening
  the source in this round."* A `queued` row for an unfetchable page would assert an opening that did
  not happen. The in-repo precedent for a refusal record is S094 (`docs`, `B`, `rejected`,
  `used-by = —`, `180d`); S179 follows it with `90d`.
- **`used-by`** — S178 names `corpus/knowledge/served-endpoint-identity-pin.md`; S179 is `—`. The
  item asks for the knowledge path in `used-by`, and S178 satisfies that. Writing it into S179 would
  claim a citation the entry does not make — and the census agrees that `used-by` is a `mined`-only
  field: `usedby_findings()` skips every row whose `status != mined`
  (`sources-census.sh:552-568`). Every rejected row in the registry (S003, S023, S026, S094) carries
  `—`.

## Commands run (verbatim)

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r51/ScribeSourcesAppend
export TMPDIR=/fast/scratch/hyaku/kengaku-r51/ScribeSourcesAppend

# baseline + variants (each a fresh copy of the lane's corpus/)
cp -a /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus <copy>/corpus
cp /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-51/w1/C1ScribeKnowledge.served-endpoint-identity-pin.md \
   <copy>/corpus/knowledge/served-endpoint-identity-pin.md
python3 apply_block.py <copy> <block-file>      # refuses NF!=13 and duplicate ids, inserts before '## Paths'
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <copy>/corpus/SOURCES.md

# the lane's own pre-append gate, on scratch copies only
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/sources_adopt.py \
  --registry <copy>/corpus/SOURCES.md --package <block> --admit-ids S178 \
  --entries corpus/knowledge/served-endpoint-identity-pin.md --access-date 2026-10-28 --out <out>

# independent verification of both pins
curl -sSL https://raw.githubusercontent.com/ggml-org/llama.cpp/8642541b255bfb5dc39cd351a178be09013a55d6/tools/server/README.md -o pinned-server-README.md
curl -sSL https://raw.githubusercontent.com/ggml-org/llama.cpp/b7200/tools/server/README.md -o b7200-server-README.md
sha256sum pinned-server-README.md b7200-server-README.md
grep -n 'By default, model `id` field\|The returned list always has one single element' b7200-server-README.md
sed -n '480,495p;1000,1020p;1345,1350p;1376p' pinned-server-README.md
curl -sS -o /dev/null -w 'blob=%{http_code}\n' https://github.com/ggml-org/llama.cpp/blob/8642541b255bfb5dc39cd351a178be09013a55d6/tools/server/README.md
```

`apply_block.py` is scratch-only: it parses the block, refuses any row whose `|`-split count is not
13 (i.e. any `|` inside a cell), refuses an id already in the registry, and inserts before
`## Paths`. It is not a lane file and is not proposed for one.

## Observed outputs (verbatim where they are evidence)

### Baseline — the HEAD registry, unmodified, in scratch

```
file	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
…  (16 W04 lines in total)
file	ok	/fast/scratch/hyaku/kengaku-r51/ScribeSourcesAppend/lane/corpus/SOURCES.md
EXIT=0
```

Zero E-codes, 16 W04 warnings, exit 0. The append is therefore measured against a registry that is
already clean: any E-code after the append is attributable to the block.

### Variant A — HEAD registry (170 rows) + both rows

```
INSERTED 2 rows before '## Paths' at line 193
file	ok	/fast/scratch/hyaku/kengaku-r51/ScribeSourcesAppend/finalA/corpus/SOURCES.md
EXIT=0
```

**No E03, no E04.** Only the pre-existing W04 warnings (filtered out of the line above).

### Variant B — 171-row registry + the HF row (measured twice)

Against the working tree at 18:36Z (knowledge entry staged as the wave fragment):

```
landed S178 present: 1
INSERTED 1 rows before '## Paths' at line 194
file	ok	/fast/scratch/hyaku/kengaku-r51/ScribeSourcesAppend/finalB/corpus/SOURCES.md
EXIT=0
```

Against the landing tip `11e7938` (S178 and the knowledge entry committed, `corpus/SOURCES.md`
clean):

```
rows=171
INSERTED 1 rows before '## Paths' at line 194
file	ok	/fast/scratch/hyaku/kengaku-r51/ScribeSourcesAppend/tipB/corpus/SOURCES.md
EXIT=0
```

**No E03, no E04 in either run.** This is the recommended landing: exit **0**.

### Controls — the validation is not vacuous

| control (scratch) | observed | exit |
|---|---|---|
| the same row inserted twice | `file	E03	S178 duplicate id` and `file	E04	S178 duplicate url github.com/ggml-org/llama.cpp/blob/8642541b… within scope the llama.cpp server's own …` | **1** |
| a `\|` inserted inside the `teaches` cell | `file	E01	S178 fields=12` | **1** |
| S178 `mined` with the knowledge entry **not** staged | `file	E11	S178 missing used-by corpus/knowledge/served-endpoint-identity-pin.md` | **1** |
| the landed `b7200` row plus the seat's `v0.8.0` row as S179 | `file	ok	…` — two llama.cpp rows, no finding | **0** |

### The lane's pre-append gate (`plans/sources_adopt.py`), measured

```
# S178 alone against the HEAD registry
registry=170 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
wrote …/append.md rows=1
EXIT=0

# the HF rejection row against the 171-row working-tree registry
registry=171 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=0
  missing: S179:not-mined
EXIT=5

# the two-row block against the 171-row working-tree registry
registry=171 staged=2 collisions=1 malformed=0 duplicates=0 defects=0 prose=0
  collisions: S178
EXIT=3
```

## Verification of the row that is already in the tree

The L1's landed S178 was checked, not trusted:

```
http=200 bytes=72181
fb4ab6f2e4db180bf9c89533ef63556559c60a66f9c39a92f0c23cd88f6c6a53  b7200-server-README.md
1530 b7200-server-README.md
758:### **GET** `/props`: Get server global properties.
1157:### GET `/v1/models`: OpenAI-compatible Model Info API
1161:The returned list always has one single element. The `meta` field can be `null` (for example, while the model is still loading).
1163:By default, model `id` field is the path to model file, specified via `-m`. You can set a custom value for model `id` field via `--alias` argument. For example, `--alias gpt-4o-mini`.
```

The landed row's URL resolves (200), its `sha256` prefix `fb4ab6f2e4db180bf9c8…` matches the fetched
bytes, and its two anchors (`:758-770` = `/props`, `:1157-1163` = `/v1/models` + the `--alias`
sentence, quoted at `:1163`) are where it says they are. **The landed row is truthful.** Its pin
differs from `SrcLlamaServer`'s proposal (tag `b7200` / `ab49f094…`, 1530 lines, 72181 bytes vs tag
`v0.8.0` / `8642541b…`, 2616 lines, 135608 bytes).

This seat's own S178 draft was verified against the pinned bytes independently:

```
http=200 bytes=135608
8fd5abde2fb52de3b30f30a170631d4c0d92febecc8da44d0541e48b132b35c6  pinned-server-README.md
8fd5abde2fb52de3b30f30a170631d4c0d92febecc8da44d0541e48b132b35c6  …/w1/SrcLlamaServer/llamacpp-tools-server-README-v0.8.0.md
blob=200
```

Every clause of its `teaches` cell is on the pinned page: one-element list (`:1349`), `id` = `-m`
path unless `--alias` (`:1376`), `/props` `model_path`/`total_slots` (`--parallel`)/`build_info`
(`:1006`, `:1019`, `:1013`), `/health` public with 503-while-loading and 200-ok (`:482`, `:486-492`).

## Findings for the L1

1. **The block and the knowledge entry must land in the same commit — and now they can.** A `mined`
   row whose `used-by` path is not on disk is `E11` and **exit 1** (control above).
   `corpus/knowledge/served-endpoint-identity-pin.md` did not exist at `4090c3d` (it existed only as
   the wave fragment); the L1 landed it in `11e7938`, so the coupling that this seat measured is
   already satisfied at the tip. Appending the block is now safe on its own; appending it *before*
   that entry landed would have turned a clean registry into an `E11` failure.
2. **`plans/sources_adopt.py` cannot land this block.** It admits `mined` rows only
   (`build_block()`: `if cells[7] != "mined": return …, [f"{row_id}:not-mined"]`), so the HF
   `rejected` row is refused with exit **5**; and it computes **one** `used-by` string for the whole
   package (`used_by = ", ".join(admitted_entries) or "—"`, line 160), so it would stamp the
   knowledge path onto an uncited row. Both are measured above. The append must be made by hand (or
   the gate taught per-row `used-by` and a `rejected` path) — the census is the only gate that can
   validate the result as it stands.
3. **Two pins of one document were in play; the L1 resolved it by landing `b7200`.** The tip carries
   S178 at tag `b7200`; `SrcLlamaServer` proposed the same document at tag `v0.8.0`. Both are
   truthful (both verified above). Registering both would double-cite one source, so Block A is now
   **documentation only** — it collides on `S178` at the tip (`sources_adopt.py` exits 3) and must not
   be landed. Block B (recommended) keeps the landed row and appends only the HF row.
4. **E04 cannot see a re-pin.** `E04` keys on normalized **URL + scope**, so a second row for the same
   document at a different tag is invisible: the control with both llama.cpp pins printed
   `file	ok` and exit **0** while the registry held two rows for `tools/server/README.md`. Any
   round that re-pins a document by changing the tag/commit in the URL needs a human check, not the
   census. (Same class as the `docs/server.md` premise defect `SrcLlamaServer` routed: the path, not
   just the tag, is a moving part.)
5. **`recheck: 90d` is the item's cadence, not the source seat's.** `SrcLlamaServer` proposed
   `on-release` (the doc floats with the repo; S005/S006 use it). The item fixes `90d`, and `90d` is
   what both rows carry; it is also the registry's shortest in-use cadence (12 rows) and matches the
   knowledge entry's `recheck: 90d`. A doc pinned to a tag does not change under the pin, so `90d` is
   a re-open check, not an expiry: state it that way if the L1 revisits the cell.
6. **No `## Search log` line is drafted.** The round opened two sources and refused a third; the
   registry's search log records sweeps, and this seat's item named the row block only. If the L1
   wants the round recorded there, the two rows' anchors (`plans/round-51-claims.md`,
   `.ufo/waves/round-51/w1/SrcLlamaServer.md` §2.1, `SrcHFRevision.md` §2.1) are the material — this
   is flagged, not written.
7. **The HF refusal leaves the mechanism page unregistered.** `hub/local-cache` (`refs/` → commit
   hash) was opened with two located quotes and is the groundable alternative; it is *not* in this
   block because the round's rows are the two named sources and that page is a third row needing its
   own id and quote. `SrcHFRevision` §3 offers it; the decision is the L1's.

## Limits

- **Three registry states, one measurement each.** Variant A used a copy of the working tree with the
  landed `S178` line removed (170 rows, byte-identical to `4090c3d:corpus/SOURCES.md` apart from that
  line); variant B used the working tree at 18:36Z and again the committed corpus at `11e7938`
  (171 rows). If the L1 appends more rows before landing, the ids shift and the block must be
  re-based.
- **`used-by` was resolved by staging the knowledge entry** as
  `<copy>/corpus/knowledge/served-endpoint-identity-pin.md` — first the wave fragment, then the
  committed 4417-byte entry. The entry's *content* was not audited (that is `C1ScribeKnowledge`'s
  deliverable and the critic seats' target); only its `S178` citation was read, because that citation
  is what makes the row `mined`.
- **The census validates the registry's mechanics, not the sources.** It cannot tell that the HF page
  is absent (finding 4 is the same limitation seen from the other side); that evidence is
  `SrcHFRevision`'s, and this seat re-checked only that the row's `source` URL is the one that 404s.
- **`sources_adopt.py` was run only against scratch copies**, never against the lane registry; its
  refusals are observed exits, not code readings.
- **Point-in-time:** the 404s, the 200s, the `b7200` bytes, and the registry at 170 / 171 / 171 rows
  are 2026-10-28 18:2x–18:40Z readings. The lane landed two commits while this seat ran
  (`2cec536`, `11e7938`), so the revision line below is the tip at 18:40Z, not the tip at which the
  first draft was written.
- **No tool was installed**, no package manager was run (pacman paused host-wide per the operator
  guard). `curl`, `sha256sum`, `grep`, `sed`, `python3` stdlib only.

## Files touched

- Written: `.ufo/waves/round-51/w1/ScribeSourcesAppend.md` (this report) — the only lane-path write.
- Scratch only: `/fast/scratch/hyaku/kengaku-r51/ScribeSourcesAppend/` (`apply_block.py`, the block
  files, the corpus copies, the two fetched READMEs) — **removed before yield**; every citable
  number above is inline in this report, not a scratch path.
- Not written: any `plans/*`, `corpus/*`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `SKILL.md`,
  `MANIFEST.json`, `.ufo/state`, `.scratch/`. No commit, push, or mutating git/jj command (only
  `rev-parse`, `status`, `log`).

VERDICT: The append block for round 51's two rows is drafted, cell-checked (11 columns, no `|` inside
a cell) and validated in scratch against the fleet census: **exit 0, `file ok`, no E03, no E04** in
every registry state measured — 2 rows against `4090c3d` (170 rows), and the HF row alone against the
L1's working tree and against the landing tip `11e7938` (171 rows, S178 and its knowledge entry
committed). S178 (`mined`, `used-by corpus/knowledge/served-endpoint-identity-pin.md`, because that
entry cites S178 and nothing else) and S179 (`rejected` — the Hugging Face model-revisions page 404s
at every tested URL, so no quote exists and a `queued` row would assert an unopened source;
`used-by —`). Four measured controls show the validation bites: duplicate row → E03+E04 exit 1, pipe
in a cell → E01 exit 1, `mined` row without its entry → E11 exit 1, and two pins of one document →
`ok` exit 0 (E04 is URL+scope keyed, so a re-pin is invisible — reported, not fixed).
`plans/sources_adopt.py` cannot land this block (refuses `not-mined`, exit 5; one `used-by` for the
whole package), and Block A collides on the now-committed S178 (exit 3), so Block B — the HF row as
`S179` — is the block to land. Lane registry not edited; scratch removed.

REV 11e79380d33d6e811f0010f2a2a0c22a3cdc359e
