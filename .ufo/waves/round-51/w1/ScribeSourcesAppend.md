# Round 51 · ScribeSourcesAppend — the SOURCES.md append block for the rows this round opens

Seat: `ScribeSourcesAppend` (scribe, leaf — no subagent dispatch). Lane:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`, read-only. Judged axis: **adjacency**.
Scope: draft the exact append block for the two rows round 51 opens (`SrcLlamaServer`,
`SrcHFRevision`), validate it against the fleet census in scratch, and report the exit code and
any E03/E04 finding. The lane registry was not edited.

## Axes named (Godspeed)

1. **adjacency** — each row must name the entry that uses it and must be *true* about that use; a
   `used-by` cell is a citation, not a routing note.
2. **cell integrity** — 11 columns, no `|` inside any cell, `status` and `recheck` in the contract's
   vocabularies, ids that do not collide with the 170 committed rows.
3. **landability** — the block must pass the lane's own pre-append gate *and* the fleet census,
   measured, not asserted.
4. **non-absorption** — no production file touched; the L1 lands the block.

## Binding inputs read before any draft

| path | what was read |
|---|---|
| `plans/round-51-claims.md` | full file |
| `corpus/SOURCES.md` | header, contract-v1 tiers/kinds/statuses, registry table (rows S001–S177), `## Paths` / `## Search log` / `## Leads` |
| `corpus/QUALITY.md` | admission rules referenced by the registry header |
| `.ufo/waves/round-51/w1/SrcLlamaServer.md` | the seat's proposed row, anchors, quotes, digest |
| `.ufo/waves/round-51/w1/C1ScribeKnowledge.served-endpoint-identity-pin.md` | the knowledge entry fragment, which cites `S178` |
| `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` | `validate` mode: E01–E12, W01–W04, `--file` target resolution, used-by resolution against the lane dir |
| `plans/sources_adopt.py` | the lane's pre-append gate (11 cells, collisions, used-by rewrite) |

## Revision measured

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
```

HEAD is one commit past the stage-1 freeze `e07f131cf7037e58a21db6e1f3986cf401ad257c`
(`git rev-parse HEAD`; the frozen claims file is unchanged between the two, `git log --oneline -3`).
The row ids below are assigned against that tip: the registry's last committed row is **S177**
(`grep -o '^| S[0-9]\+' corpus/SOURCES.md | sort -V | tail -1`).

## The append block

Insert immediately **before the `## Paths` heading** (`corpus/SOURCES.md:193` at `4090c3d`), i.e. as
the last two rows of the `## Registry` table.

```markdown
| S178 | ... |
| S179 | ... |
```

(Two full rows — see "Row S178" and "Row S179" below; the block is reproduced byte-exactly in
`.ufo/waves/round-51/w1/ScribeSourcesAppend.append.md`.)

### Row S178 — llama.cpp server documentation (`SrcLlamaServer`)

Status **`mined`**: the knowledge entry `corpus/knowledge/served-endpoint-identity-pin.md` cites
this row by id — its first line is `source: corpus/SOURCES.md S178 — llama.cpp HTTP server
documentation, tools/server/README.md at commit 8642541b…`. That entry is drafted by seat
`C1ScribeKnowledge` (fragment
`.ufo/waves/round-51/w1/C1ScribeKnowledge.served-endpoint-identity-pin.md`, 12536 bytes). This is
the only row of the two that a knowledge entry cites, so it is the only `mined` row.

### Row S179 — Hugging Face revision pinning (`SrcHFRevision`)

Status **`queued`**: no knowledge entry cites it. `corpus/knowledge/served-endpoint-identity-pin.md`
names S178 only; nothing in `corpus/knowledge/` names the HF row.

`used-by` is therefore **`—`**, not the knowledge path. The item's instruction to name
`corpus/knowledge/served-endpoint-identity-pin.md` in `used-by` is satisfied by S178, and applying it
to S179 would assert a citation that does not exist — the exact adjacency defect the axis measures.
The census agrees: `usedby_findings()` only resolves `used-by` for `status == mined` rows
(`sources-census.sh:552-568`), and `plans/sources_adopt.py:160` computes one `used-by` string for
the whole package, which is why an adoption run through that tool would silently stamp the knowledge
path onto an uncited row.

## Commands run (verbatim)

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r51/ScribeSourcesAppend
export TMPDIR=/fast/scratch/hyaku/kengaku-r51/ScribeSourcesAppend
cp -a /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus $TMPDIR/lane/corpus
cp /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-51/w1/C1ScribeKnowledge.served-endpoint-identity-pin.md \
   $TMPDIR/lane/corpus/knowledge/served-endpoint-identity-pin.md
python3 apply_block.py $TMPDIR/lane block.md          # inserts before '## Paths', refuses NF!=13
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $TMPDIR/lane/corpus/SOURCES.md
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $TMPDIR/ctrl-noentry/corpus/SOURCES.md
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/sources_adopt.py \
  --registry $TMPDIR/adopt-test/corpus/SOURCES.md --package $TMPDIR/block.md \
  --admit-ids S178 --entries corpus/knowledge/served-endpoint-identity-pin.md \
  --access-date 2026-10-28 --out $TMPDIR/adopt-test/append.md
curl -sSL https://raw.githubusercontent.com/ggml-org/llama.cpp/8642541b255bfb5dc39cd351a178be09013a55d6/tools/server/README.md -o pinned-server-README.md
sha256sum pinned-server-README.md
sed -n '480,495p;1000,1020p;1345,1350p;1376p' pinned-server-README.md
```

`apply_block.py` (scratch-only) parses the block, refuses any row whose `|`-split count is not 13
(i.e. any `|` inside a cell), refuses an id already in the registry, and inserts before `## Paths`.

## Observed outputs (verbatim where they are evidence)

### Baseline — the committed registry, unmodified, in scratch

```
file	W04	S040 duplicate url arxiv.org/abs/2301.09633 across scopes
...
file	W04	S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
file	ok	/fast/scratch/hyaku/kengaku-r51/ScribeSourcesAppend/lane/corpus/SOURCES.md
EXIT=0
```

16 W04 warnings, zero E-codes, exit 0. This is the control: the append is measured against a
registry that is already clean, so any E-code after the append is attributable to the block.

### The append block, validated

See "Validation results" below.

## Validation results

(pending — filled from the measured run)
