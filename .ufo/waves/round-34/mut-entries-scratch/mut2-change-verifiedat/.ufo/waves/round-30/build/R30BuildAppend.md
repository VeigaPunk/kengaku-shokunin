# Round 30 build — adoption gate on a scratch mirror, census proof

Seat: L1Kengaku30.R30BuildAppend (leaf). Scope: prove the S081–S086 append block is census-valid
*before* any registry append. No production file was touched; only this report is new.

**Verdict.** Gate exits **0** on the derived six-row set and writes the block; the mirror registry
built from a copy of `corpus/` plus that block passes `sources-census.sh validate` with exit **0**,
the 14 pre-existing W04 warnings and **zero E-codes**. Every E-class the acceptance names is shown
to be failure-capable by mutants that name the implicated row.

---

## 1. Acceptance commands, outputs, exit codes

### 1a. Gate (block construction)

```
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/sources_adopt.py \
    --registry /tmp/r30-BuildAppend/validate/corpus/SOURCES.md \
    --package /tmp/r30-BuildAppend/SOURCES.append.r30.md \
    --admit-ids S081,S082,S083,S084,S085,S086 \
    --entries corpus/knowledge/contamination-transparency-card.md \
    --access-date 2026-10-25 --scope-to-admit \
    --out /tmp/r30-BuildAppend/block.txt
registry=82 staged=6 collisions=0 malformed=0 duplicates=0 defects=0 prose=6
  normalized recheck S081: 2026-10-23 — re-verify at the next upstream release (Gate S081)
  normalized recheck S082: 2026-10-23 — re-verify at the next upstream release (Gate S082)
  normalized recheck S083: 2026-10-23 — re-verify at the next upstream release (Gate S083)
  normalized recheck S084: 2026-10-23 — re-verify at the next upstream release (Gate S084)
  normalized recheck S085: 2026-10-23 — re-verify at the next upstream release (Gate S085)
  normalized recheck S086: 2026-10-23 — re-verify at the next upstream release (Gate S086)
wrote /tmp/r30-BuildAppend/block.txt rows=6
GATE_EXIT=0
```

`--package` is the one token that differs from the assignment's command: the assignment points at
the read-only staged package, whose rows carry `opened=2026-10-23`, and the gate **refuses** those
bytes under a 2026-10-25 access date (§4a). The row set that is being validated here is the round's
own row set, derived per §2. `block.txt` is deterministic: two independent runs produced
`sha256 2ec3a83b06c7ef2a59ea7dac55e6b2c6187ff3312b7b965e539ca74f177d1529`.

Block cell audit (`awk -F'|'` over `block.txt`, all six rows):

```
NF=13 id= S081  status= mined  opened= 2026-10-25  recheck= 180d  usedby= corpus/knowledge/contamination-transparency-card.md
NF=13 id= S082  status= mined  opened= 2026-10-25  recheck= 180d  usedby= corpus/knowledge/contamination-transparency-card.md
NF=13 id= S083  status= mined  opened= 2026-10-25  recheck= 180d  usedby= corpus/knowledge/contamination-transparency-card.md
NF=13 id= S084  status= mined  opened= 2026-10-25  recheck= 180d  usedby= corpus/knowledge/contamination-transparency-card.md
NF=13 id= S085  status= mined  opened= 2026-10-25  recheck= 180d  usedby= corpus/knowledge/contamination-transparency-card.md
NF=13 id= S086  status= mined  opened= 2026-10-25  recheck= 180d  usedby= corpus/knowledge/contamination-transparency-card.md
```

NF=13 ⇒ 11 cells under the census contract; `recheck` prose normalized to `180d`; `used-by`
projected to exactly the admitted entry.

### 1b. Census validate (mirror, after the block was inserted)

```
$ sh /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --file /tmp/r30-BuildAppend/validate/corpus/SOURCES.md
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
file	ok	/tmp/r30-BuildAppend/validate/corpus/SOURCES.md
CENSUS_EXIT=0
```

Warnings only, and they are **not new**: the pre-append mirror (`/tmp/r30-BuildAppend/validate-pre/`)
produces the byte-identical finding set —
`cmp base-findings.txt mirror-findings.txt` → identical, 14 lines each, `grep -c 'E[0-9][0-9]'` → 0.
So S081–S086 add no finding of any class, E03/E04 included.

---

## 2. How the six rows were derived

- `/tmp/r30-DraftEntry/entry.md` **absent** on this host.
- `.ufo/waves/round-30/build/R30RowSchema.md` **absent** at run time (the directory held only
  `swarm-registry.json`), so the rows were derived by this seat, as the assignment permits.
- Source of cells: `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md` lines 11–16
  (rows S081–S086), extracted byte-for-byte into `/tmp/r30-BuildAppend/SOURCES.append.r30.md`.
- Exactly one cell per row was changed: `opened` `2026-10-23` → `2026-10-25`, the round's access
  date and the date C1's frozen predicate requires. `recheck` was left as the staged prose so the
  gate exercises its normalization branch; `used-by` was left as staged so the gate exercises its
  projection branch.
- Identity proof (python cell compare of package lines 11–16 against `block.txt`):
  `cells=1..7 identical: True` for all six, `ALL_IDENTITY: True`, `distinct ids: 6`,
  `distinct urls: 6`. Only `opened`, `recheck`, `used-by` differ, and only in the ways §1a records.
- Entry citations cross-checked against the block: 6 `source:` lines in the mirror entry, and each
  cited URL matches its row's URL (`S081..S086 url_match: True` — arxiv 2608.29463, arxiv
  2607.01254, aclanthology 2026.findings-eacl.353.pdf, doc.opencompass.org.cn …, caict.ac.cn …,
  anlp.jp …/Q2-11.pdf).

---

## 3. Mirror construction and the insertion

```
/tmp/r30-BuildAppend/
  SOURCES.append.r30.md          derived row set (six rows, header + separator)
  block.txt                      gate output, sha256 2ec3a83b…d1529
  pre-SOURCES.md                 copy of the lane registry before insertion
  validate/corpus/               cp -a of kengaku-shokunin/corpus (20 MB, 138-line registry)
  validate-pre/corpus/           same corpus, registry restored to pre-append (baseline receipt)
  mutants/{dup-id,dangling-usedby,staged-usedby}/corpus/   failure-capability fixtures
```

- Entry file: `/tmp/r30-DraftEntry/entry.md` does not exist, so the admitted entry was taken from
  the staged package — `merge/kengaku/knowledge/corpus/knowledge/contamination-transparency-card.md`,
  whose six `source:` lines are byte-real rather than a placeholder. **One delta** was applied in the
  mirror: `verified-at: 2026-10-23` → `verified-at: 2026-10-25` (C1's predicate requires the latter).
  Nothing else in the entry was edited; its `recheck:` line still reads
  `180d — re-run the Gate commands for S081–S086 (ran 2026-10-23)`.
- Insertion point: immediately after `S091` and before the `## Paths` heading — i.e. inside the
  `## Registry` table, contiguous with it. Lines 107–112 of the mirror registry.
- Byte fidelity: `awk 'NR>=107 && NR<=112' registry | cmp - block.txt` → `BLOCK_INSERTED_BYTE_IDENTICAL`.
- Registry hashes: before `e18b32d9b2e3b19053a3d431eb4586713fe057d04477651e6d02be51e8908236`,
  after `5dbc2e131b1293dd630b474f927c73b979810c7a04ce2db013f6b810b74fd505`, 138 → 144 lines.
- Census counts (`sources-census.sh census --file …`), pre → post:

```
rows 82 → 88   tier.A 76 → 79   tier.B 4 → 7   tier.C 2 → 2
status.mined 70 → 76   status.queued 8 → 8   status.rejected 4 → 4   invalid 0 → 0   missing 0 → 0
```

Both `census` runs exit 0. `overdue --file <mirror>` exits 0 and prints only informational
`cadence` lines, e.g. `file	cadence	S081 recheck=180d opened=2026-10-25` — nothing due.

---

## 4. Refusals (named, not softened)

### 4a. The distributed package cannot be adopted under a 2026-10-25 access date

The assignment's command verbatim, mirror in the pre-append state:

```
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/sources_adopt.py \
    --registry /tmp/r30-BuildAppend/validate/corpus/SOURCES.md \
    --package /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md \
    --admit-ids S081,S082,S083,S084,S085,S086 \
    --entries corpus/knowledge/contamination-transparency-card.md \
    --access-date 2026-10-25 --scope-to-admit \
    --out /tmp/r30-BuildAppend/block.txt
registry=82 staged=173 collisions=0 malformed=0 duplicates=0 defects=0 prose=6
  missing: S081:not-opened-this-round
GATE_EXIT=5
```

Exit 5 = `EXIT_REQUEST`; no block is written. The staged rows carry `opened=2026-10-23`, so the
gate refuses to stamp them with this round's access date. Two legal exits exist, and only these:
re-open on 2026-10-25 and re-date the cell (the derived row set of §2), or pass `--attest-opened`
so the gate prints `attested: the caller asserts every requested source was opened on 2026-10-25`.
This seat did not attest a fetch it did not perform, hence the re-dated row set.

### 4b. Re-running the gate against the post-append mirror is refused (collision guard)

```
registry=88 staged=6 collisions=6 malformed=0 duplicates=0 defects=0 prose=6
  collisions: S081 S082 S083 S084 S085 S086
GATE_EXIT=3
```

That is the gate doing its job on an already-appended registry (exit 3 = `EXIT_COLLISION`); it also
fixes the ordering: the gate must run **before** insertion, the census **after**.

### 4c. The census is failure-capable on exactly these conditions

| mutant | what was changed | finding | exit |
|---|---|---|---|
| `dup-id` | S081 row duplicated in place | `file	E03	S081 duplicate id` + `file	E04	S081 duplicate url arxiv.org/abs/2608.29463 within scope the four-field contamination disclosure protocol …` | 1 |
| `dangling-usedby` | S083 `used-by` → `corpus/knowledge/nonexistent-entry.md` | `file	E11	S083 missing used-by corpus/knowledge/nonexistent-entry.md` | 1 |
| `staged-usedby` | block keeps the package's `used-by` cells | `E11	S081 missing used-by corpus/knowledge/judge-calibration-thresholds.md`, `E11	S084 … cjk-eval-venue-access.md`, `E11	S085 … cjk-eval-venue-access.md`, `E11	S086 … cjk-eval-venue-access.md` | 1 |

Each mutant's `corpus/` is a hardlinked copy of the mirrored corpus, so the only difference from the
passing mirror is the mutated bytes. **No E03/E04 (and no other E-code) occurs in the appended
mirror.**

---

## 5. Gate state at the bytes this run used (C3 context, not C3's work)

`plans/sources_adopt.py` at `sha256 6fe6e762ab0c61da4ddbf029a2aa1a38cb64732ebd1ccbee4773c5eadcf7ead2`:

```
$ python3 plans/sources_adopt.py --selftest
SELFTEST cases=10 failed=0
EXIT_SELFTEST=0
```

`grep -c 'quote-file\|--artifact'` over those bytes → **0**: this revision validates registry
*schema* only. The block's quotes and word counts were therefore **not** checked by the gate — that
is C3's deliverable, and this lane's result is scoped to registry mechanics plus the census. It must
not be read as a quote check.

Two operability observations, reported rather than fixed (production file, another seat's scope):

1. `build_block` returns on the first stale row, so `missing:` names only `S081` although all six
   rows are stale. The refusal is correct, the message is under-informative.
2. The `--entries` projection is load-bearing, measured: `corpus/knowledge/judge-calibration-thresholds.md`
   and `corpus/knowledge/cjk-eval-venue-access.md` — the sibling `used-by` entries in the staged
   package — do **not** exist in the lane corpus (`ls corpus/knowledge/` → `ABSENT_IN_LANE_CORPUS`).
   Appending the staged `used-by` cells verbatim would have produced the four E11 findings of §4c.

---

## 6. Files changed

- Created: `.ufo/waves/round-30/build/R30BuildAppend.md` (this report). Nothing else.
- No production edit, no registry append: `corpus/SOURCES.md` and `corpus/README.md` in the lane are
  untouched; `shokuknow` was read only; `plans/` untouched; `.ufo/state`, `MANIFEST.json` and
  `watchdog.log` untouched.
- Scratch: `/tmp/r30-BuildAppend/`.
- Tool installs/upgrades: none (python3, gawk, coreutils, bash already present; pacman not used).

---

## 7. Risks and blockers

1. **The append must use the derived row set, not the distributed bytes.** Adopting
   `SOURCES.append.md` lines 11–16 unchanged under `--access-date 2026-10-25` is refused with exit 5.
   Whoever appends must either land the re-dated cells (after the 2026-10-25 re-open) or take the
   explicit `--attest-opened` path, and must cite the same `--entries` value, otherwise the census
   gains E11 findings (§4c).
2. **Entry-file dependency.** The mirror entry is the staged entry with one line changed
   (`verified-at: 2026-10-23` → `2026-10-25`). C1 also needs the entry's own `recheck:` line to stop
   saying "ran 2026-10-23" if the round wants no stale self-description; that edit belongs to whoever
   lands the entry, not to this seat.
3. **Mirror proven only for registry mechanics.** The census checks that a `used-by` path *exists*,
   not that the entry supports the row. Quote/word validation is absent from the gate at the hash in
   §5 — C1's kill rule (a quote that cannot be found in this round's fetch refuses that row) is not
   discharged by anything in this report.
4. **Mirror must stay lane-shaped.** `resolve_targets` resolves `used-by` against the registry's
   parent directory. Copying `SOURCES.md` straight into `/tmp/r30-BuildAppend/` produced 129
   spurious E11 lines (observed, discarded); the receipt comes only from `…/<lane>/corpus/SOURCES.md`.

## 8. Reproduce

```
mkdir -p /tmp/r30-BuildAppend/validate
cp -a <lane>/corpus /tmp/r30-BuildAppend/validate/corpus
cp -a <staged>/knowledge/corpus/knowledge/contamination-transparency-card.md \
      /tmp/r30-BuildAppend/validate/corpus/knowledge/
# then change that entry's single `verified-at:` line to `2026-10-25` (editor, not a script)
# derived package = header + staged rows S081-S086 with `| mined | 2026-10-23 |` -> `| mined | 2026-10-25 |`
python3 plans/sources_adopt.py --registry /tmp/r30-BuildAppend/validate/corpus/SOURCES.md \
  --package /tmp/r30-BuildAppend/SOURCES.append.r30.md --admit-ids S081,S082,S083,S084,S085,S086 \
  --entries corpus/knowledge/contamination-transparency-card.md --access-date 2026-10-25 \
  --scope-to-admit --out /tmp/r30-BuildAppend/block.txt      # exit 0
# insert block.txt after the S091 row (line 106), before `## Paths`
sh scripts/sources-census.sh validate --file /tmp/r30-BuildAppend/validate/corpus/SOURCES.md  # exit 0
```

---

## 9. Cross-reference: the row-content audit that landed after this run

`build/R30RevRows.md` appeared at 04:26 and audited **the same artifact** — `/tmp/r30-BuildAppend/block.txt`.
Its registry findings agree with §1b and §4c: census exit 0 on the proposal, zero E03/E04, all six
ids unused, all six URLs unique under the census URL normalization, `used-by` exactly the admitted
entry. It additionally flags three **content** defects this seat's evidence cannot see and this seat
does not repair: S081's quoted span is 30 words and its `§ Abstract` location is ambiguous between
the PDF and HTML versions; S082's anchor names a `§ Benchmark Governance` section the paper does not
have (the quotes live in §7.3); S085 flattened the source's fullwidth inner quotes to ASCII, which
breaks any `"…"`-pairing reader. A fourth note: S083's `contamination-resistant` is dehyphenated to
`contaminationresistant` by PDF text extraction.

Those are quote/word/location defects in the `anchor` cell — exactly the class that
`plans/sources_adopt.py` at `6fe6e762…` does **not** validate (§5). So: the block is census-valid and
schema-valid, and it is **not** quote-valid; the row bytes need the anchor repairs named there before
the append, and the gate needs C3's quote check before such repairs can be proved by machine.
