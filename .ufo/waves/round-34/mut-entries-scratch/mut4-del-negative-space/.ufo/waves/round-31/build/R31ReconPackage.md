# R31 recon — staged-package citations of S092 / S093 / S100, and what dangles on a one-entry adoption

Seat: `L1Kengaku31.R31ReconPackage` (leaf, read-only). Access date 2026-10-25.
Staged package read at `/home/vgpnk/Projects/shokuknow/merge/kengaku/` (read-only; nothing written there).
Lane read at `/home/vgpnk/Projects/shokunin/kengaku-shokunin/` (tip `0883e72` + round-31 working tree).
No campaign tool run, no `pacman` transaction, no tool installed. Scratch: `/tmp/r31-reconpackage/`
(`measure.py`, `quotes.py`, `quotes2.py` — my own re-implementations of the gate's cell/quote rules).

Labels: **[M]** measured by me on the bytes named; **[I]** inference from measured bytes; **[P]** prior-round receipt quoted, not re-run.

---

## (a) Every staged entry whose `source:` lines cite S092, S093 or S100

Three of the 65 staged knowledge entries. No other staged file mentions the three ids — `grep -rn
'S09[23]\|S100'` over the whole package returns only these files plus the three registry rows
(`SOURCES.append.md:22,23,30`). [M]

| # | staged entry | `source:` line(s) | ids | `verified-at:` | `recheck:` |
|---|---|---|---|---|---|
| 1 | `knowledge/corpus/knowledge/benchmark-verifier-execution-model.md` | `:2` S092, `:3` S093, `:4` S100 | **all three** | `:5` `2026-10-23` | `:6` `180d — re-run the Gate commands for S092, S093 and S100 … (ran 2026-10-23)` |
| 2 | `knowledge/corpus/knowledge/terminal-bench-release-identity.md` | `:2` S100, `:3` S092 | S100, S092 | `:4` `2026-10-23` | `:5` `180d — … S100 and S092 …` |
| 3 | `knowledge/corpus/knowledge/benchmark-grader-semantics.md` | `:2` S093, `:3` S094, `:4` S097 | S093 (+S094, S097) | `:5` `2026-10-23` | `:6` `180d — … S093, S094 and S097 …` |

Exact `source:` bytes for the three ids [M]:

- `benchmark-verifier-execution-model.md:2` — `source: S092 — https://github.com/laude-institute/harbor — `# VerifierConfig.environment_mode` and `# Verifier.verify` — commit `6099b8cf2bfbbb3e7ff1eb2163bfc4524dbd9ba5``
- `benchmark-verifier-execution-model.md:3` — `source: S093 — https://github.com/scaleapi/SWE-bench_Pro-os — `# v2/tasks/…/tests/test.sh` — commit `66f92766bba642462d4bbe5479e83f91f9211862``
- `benchmark-verifier-execution-model.md:4` — `source: S100 — https://github.com/laude-institute/terminal-bench-2 — `# task tree at 2fd12b8` — commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6``

The frozen round-31 expectation names exactly one entry with exactly these three ids
(`.ufo/waves/round-31/adoption-expect.json:6-7`, `"sources": ["S092", "S093", "S100"]`), matching
`plans/round-31-claims.md:31-33` ("`source:` lines citing exactly the three ids adopted this round
(three distinct)"). [M]

### Adjacency of those ids against the live registry

- Lane registry holds **88** rows: ids `S001–S086` plus `S090`, `S091` (`corpus/SOURCES.md`, 88 row
  anchors, no duplicates). **S092, S093, S100 and the secondary ids S094/S097 are all free.** [M]
- The staged block as a whole collides on **12** ids — `S077 S078 S079 S080 S081 S082 S083 S084 S085
  S086 S090 S091` — because the package was staged when the lane held 76 rows
  (`MERGE-REPORT.md:9`). `MERGE-REPORT.md:5-6` still says `accepted: 175 / refused: 0`, and 175 is
  also the wrong count: 175 row-anchored lines parse to **173** 11-cell rows, with 2 refused as
  malformed (`S093` `:23`, `S101` `:31`). [M]
- So the three ids this claim adopts are the collision-free ones; a whole-file append would not be. [M]

---

## (b) Do the staged `used-by` cells point at entries this lane would not adopt? Yes — 3 pointers, 2 distinct paths

Measured `used-by` cells of the three staged rows [M]:

| row | staged `used-by` | entry 1 (adopted) | entry 2 | entry 3 |
|---|---|---|---|---|
| `S092` (`SOURCES.append.md:22`, col 11) | `corpus/knowledge/benchmark-verifier-execution-model.md, corpus/knowledge/terminal-bench-release-identity.md` | exists after adoption | **dangles** | — |
| `S093` (`:23`) | `corpus/knowledge/benchmark-verifier-execution-model.md, corpus/knowledge/benchmark-grader-semantics.md` | exists after adoption | — | **dangles** |
| `S100` (`:30`) | `corpus/knowledge/benchmark-verifier-execution-model.md, corpus/knowledge/terminal-bench-release-identity.md` | exists after adoption | **dangles** | — |

- None of the three entry paths exists in the lane today (`ls corpus/knowledge` → 39 files; no
  `benchmark-verifier-execution-model.md`, no `terminal-bench-release-identity.md`, no
  `benchmark-grader-semantics.md`). [M]
- The lane currently has **zero** dangling `used-by` targets: over all 88 rows, every `corpus/…`
  target of a `used-by` cell exists on disk. Adopting the staged cells verbatim would create the
  lane's first three. [M]
- The lane's own checker would catch it: `plans/registry_check.py:77-81` emits
  `used_by_missing` for any `used-by` path that is not a file, and `:82-86` emits `missing_used_by`
  for a citing entry the row omits. [M]
- **The C1 counter would not catch it.** `plans/adoption_check.py:93-98` computes
  `linked = all(rel in [part.strip() for part in registry[row_id][10].split(",")] …)` — membership,
  not equality. A `used-by` naming the adopted entry *and* two paths that do not exist still prints
  `usedby_ok=1`. So the frozen predicate (`plans/round-31-claims.md:35-37`, "`used-by` naming the
  entry") greens on a row that `registry_check.py` calls broken. [M] + [I]
- The gate's own rewrite is the mitigation: `plans/sources_adopt.py:177` sets
  `cells[10] = used_by` where `used_by = ", ".join(admitted_entries)` (`:158`) — i.e. the staged
  cell is replaced, never appended to. [M]

### Second dangling class: the adopted entry's own cross-references

Even with the rows clean, one-entry adoption leaves three entry-side references pointing at text the
lane does not hold. [M]

1. `benchmark-verifier-execution-model.md:10-11` — "Round 1 left axis E … open for Terminal-Bench 2.0
   and flagged it as *partly observable*. This entry closes it, and the answer **corrects the round-1
   framing**", restated at `:78` ("The round-1 checklist entry recorded axis E for TB2.0 as 'partly
   observable'"). That premise is true only of the **staged** checklist
   (`merge/kengaku/knowledge/…/benchmark-task-validity-checklist.md:49`: "E is partly observable (the
   Harbor harness separates the verifier from the agent) but the lane has not read the harness
   source"). The lane holds a **revised** checklist whose `:71-74` already reads: "Axis E is scoped to
   the harness that publishes the claim. S078 states isolation for its locked release protocol; a
   harness that runs the verifier in a shared environment by default does not inherit that property".
   `partly observable` occurs **0** times anywhere under `corpus/` — only in `plans/round-31-claims.md:24`
   and two seat reports. So C1's own surface sentence (`plans/round-31-claims.md:23-25`) and the
   entry's opening paragraph both describe a text the lane does not hold; the entry's "correction"
   corrects a document that was superseded in round 29/30. [M]
2. The entry qualifies lane row **S078**'s quote — `:54-56` "SWE-bench Pro V2's own README states
   'The verifier never runs in the agent's sandbox.'", which is S078's anchor verbatim
   (`corpus/SOURCES.md` S078 anchor: `§The locked protocol line 75: "The verifier never runs in the
   agent's sandbox." (8 words)`). S078 is not in the entry's `source:` lines, so S078's `used-by`
   will never name the entry and no counter fires: `registry_check.py` derives `citing` from
   `source:` lines only, not prose. [M]
3. The entry's per-benchmark table reads documents no cited row anchors [M]:
   - `:31` TB2.0 `protein-assembly/task.toml`: `[verifier] timeout_sec = 1800.0 only`,
     `[environment] allow_internet = true`. Lane S079's anchor covers **only** `timeout_sec = 1800.0`
     (line 22) plus schema/difficulty/time baselines — not `[environment]`, not the absence of a
     `[verifier.environment]` section.
   - `:32` SWE-bench `…/task.toml`: `network_mode = "public"`, `timeout_sec = 3000.0`, `collect = []`.
     **No row in the lane or in the staged package anchors a SWE-bench `task.toml`** (S093's scope is
     "task verifier files (test.sh, parser.py, config.json)"; only S079's anchor mentions `task.toml`
     at all across `SOURCES.append.md`).
   - `:34-35` "No task in either repository sets `environment_mode` … verified by grepping every
     `*.toml` in both trees" — a negative-grep claim with no row and no committed capture.

---

## (c) Schema defects, the three rows specifically

Gate rules read from `plans/sources_adopt.py` (`:82-89` escaped-pipe and 11-cell split, `:110-118`
status/recheck/source, `:165-170` opened/`--attest-opened`, `:271` `QUOTE_WORDS = 25`, `:275`
`QUOTE_SPAN_RE`, `:287-303` `quoted_spans`). Measurements are mine, replicating those rules. [M]

| row | `SOURCES.append.md` line | cells (literal `\|` split) | cells (escape-aware) | escaped pipe | `status` | `opened` | `recheck` | gate verdict class |
|---|---|---|---|---|---|---|---|---|
| S092 | `:22` | 11 | 11 | none | `mined` | `2026-10-23` | prose: `2026-10-23 — re-verify at the next upstream release (Gate S092 below)` | accepted by the row check; `opened` needs `--attest-opened`, `recheck` normalized |
| S093 | `:23` | **12** | 11 | **1** (`\|` inside the reward-block quote) | `mined` | `2026-10-23` | prose: same shape, `(Gate S093 below)` | **refused: `S093:escaped-pipe`, exit 4** |
| S100 | `:30` | 11 | 11 | none | `mined` | `2026-10-23` | prose: same shape, `(Gate S100 below)` | accepted by the row check; `opened`/`recheck` as above |

Row-level details:

1. **Cell counts.** All three are 11-cell rows once `\|` is honoured; S093 is 12 on a literal split
   because of the escaped pipe. Package-wide the same defect hits `S101` (`:31`) — 2 malformed rows,
   matching `MERGE-REPORT.md:6`'s `refused: 0` only if the report never ran a cell split. [M]
2. **S093's escaped pipe is not cosmetic — the quote is unrepresentable in the row format.** The
   escape sits inside a quoted span: anchor `:23` carries `"all_required = fail_to_pass \| pass_to_pass"`.
   The gate rejects any cell containing `\|` (`:82-83`) *before* counting cells, and a literal `|`
   inside the cell would split it into 12. So the upstream line cannot be carried verbatim: the repair
   is to quote a pipe-free span (the anchor already quotes three others) or to describe the reward
   block without quoting it. Prior rounds recorded the same refusal (`round-29` receipt quoted at
   `.ufo/waves/round-29/attempt2/build/R29a2ConnCapability.md:119`: "`--admit-ids S092,S100` → exit 0;
   adding `S093` → exit 4"). [M] + [P]
3. **Prose `recheck` on all three** (and on 167 of the 173 parseable staged rows). The gate normalizes
   it to the frozen access date and reports the stripped prose (`:171-176`, `--recheck` default
   `180d`). A prose cell is a defect at the registry bar, not a blocker in scoped mode. [M]
4. **`opened` is stale for all three** (`2026-10-23`). `build_block` refuses with
   `not-opened-this-round` unless `--attest-opened` is passed (`:167-170`), and C1 requires
   `opened=2026-10-25` (`plans/round-31-claims.md:34-35`, enforced in
   `plans/adoption_check.py:114-116`). Passing the flag without re-opening the three pinned sources
   would launder a stale row. [M]
5. **S092's anchor quote is over the cap.** Its single double-quoted span is the `environment_mode`
   docstring, **28 words** by the gate's counter (`len(text.split())`, `:278-279`) against
   `QUOTE_WORDS = 25` (`:271`) → `quote_check` refuses `overlong` with exit 6 when the row is fed
   through `--quote-file`/`--artifact`. [M]
6. **S100's anchor carries no double-quoted span at all.** Its only quote is in corner brackets —
   `「89 task directories, plus .gitignore, LICENSE and README.md, i.e. 92 top-level tree entries」`
   (13 words). `quoted_spans` matches `"…"` only (`:275`, `:287-303`), so S100 returns `no-quote` → malformed,
   exit 4, in quote mode. S093 by contrast carries 4 double-quoted spans of 8, 12, 5 and 5 words —
   all inside the cap. [M]
7. **The `recheck` prose points at a block that is not in the package.** All three say "(Gate S09x
   below)"; `grep -c '^## Gate' SOURCES.append.md` → **0**. `MERGE-REPORT.md:106` sends the reader to
   the lane's `SOURCES-PROPOSED.md`, which is not staged either (package = `MERGE-REPORT.md`,
   `MERGE-REPORT.json`, `SOURCES.append.md`, 65 knowledge files). The gate evidence for these three
   rows is therefore not reachable from the package, which matters for C3's capture binding. [M]
8. Not defects, for the record: `status=mined` on all three (`:112-114`); `source` cells non-empty;
   ids distinct and collision-free; no duplicate staged id in the package. [M]

---

## (d) Recommended `used-by` projection for the adopted rows

The projection that satisfies both the frozen predicate and the lane's own link checker is
**per-row, exactly the admitted entries whose `source:` lines name that id**:

| row | recommended `used-by` (single-entry adoption, the frozen shape) | if the other two entries are ever admitted |
|---|---|---|
| S092 | `corpus/knowledge/benchmark-verifier-execution-model.md` | `…benchmark-verifier-execution-model.md, …terminal-bench-release-identity.md` |
| S093 | `corpus/knowledge/benchmark-verifier-execution-model.md` | `…benchmark-verifier-execution-model.md, …benchmark-grader-semantics.md` |
| S100 | `corpus/knowledge/benchmark-verifier-execution-model.md` | `…benchmark-verifier-execution-model.md, …terminal-bench-release-identity.md` |

Why this is the right shape, and where the tooling cannot express it:

- The frozen adoption is one entry over three rows (`.ufo/waves/round-31/adoption-expect.json:6-7`).
  For this shape the gate's single global list is *already exact*: `--entries
  corpus/knowledge/benchmark-verifier-execution-model.md` writes that one path to all three rows
  (`plans/sources_adopt.py:158,177`), and all three rows are cited by that one entry, so no
  over-attribution and no dangling pointer results. `adoption_check.py` then prints `usedby_ok=1`
  honestly. [M]
- **The gate cannot express the multi-entry column.** `--entries` is one global list applied to every
  appended row (`:158`, `:177`). With all three entries admitted, the global list would name
  `benchmark-grader-semantics.md` on S092 and S100 (which it does not cite) and
  `terminal-bench-release-identity.md` on S093 (which it does not cite) — the mirror defect,
  over-attribution, which `registry_check.py` does **not** flag (`used_by_missing` only checks
  existence). The multi-entry column therefore has to be written per row by hand, or `--entries` needs
  a per-row form. [M] + [I]
- `--entries` is not validated at all: no existence check, no "does this entry cite this row" check
  (`plans/sources_adopt.py:1021-1024`, `entries = [item for item in args.entries.split(",") if item]`
  → `build_block`). A typo'd path would be written into the registry and only `registry_check.py`
  would ever notice. Worth one line in the round's report. [M]
- Do **not** keep the staged second pointers as a "will be filled later" note: they are the only
  construct that turns C1's green into a broken registry, and the counter that decides C1 cannot see
  them.

Row repairs the projection presupposes (each measured in (c)): repair S093's anchor to a pipe-free
quote before admitting it; re-date `opened` to `2026-10-25` by actually reopening the three pinned
commits (not by `--attest-opened` alone); let the gate normalize the prose `recheck` to `180d`; shorten
S092's 28-word span or move the long docstring to `scope`/`teaches`; give S100 a double-quoted span if
its anchor is to pass `--quote-file` (its `「」` quote is invisible to `quoted_spans`).

Entry-side repairs the projection does **not** fix, and that one-entry adoption leaves dangling:
re-point `benchmark-verifier-execution-model.md:10-11,78` from "the round-1 checklist" to the staged
round-1 text (the lane's held checklist `:71-74` already says the stronger thing, so the entry's
"correction" must not claim to correct bytes the lane does not hold); and decide the
`task.toml` seam — `:31`/`:32`/`:34-35` rest on documents outside the three cited rows (S079 covers
`protein-assembly/task.toml` line 22 only; no row anywhere anchors a SWE-bench `task.toml`). Since C1
forbids a fourth `source:` line, the clean fix is to widen S093's anchor to the SWE-bench `task.toml`
at the same pinned commit (a row edit inside the re-open this round already owes) rather than to add a
row.

---

## What I did not verify

- I did not re-fetch Harbor / SWE-bench_Pro-os / terminal-bench-2 at the pinned commits, so I do not
  assert that any of the three anchors' quotes still locate upstream. The kill rule in
  `plans/round-31-claims.md:40-42` is that check's owner, not mine.
- I did not run `plans/sources_adopt.py`, `plans/adoption_check.py`, `plans/registry_check.py` or the
  fleet census (the gate is being edited in this same wave; a mid-edit reading would be a transient
  number). Every gate statement above is a reading of the gate's code plus my own replication of its
  rules, and the one exit-code pair I quote is labelled [P] as a round-29 receipt.
- `MERGE-REPORT.json`'s `accepted/refused` counters were read as keys only, not audited row by row.

VERDICT: three staged entries cite the three ids — `benchmark-verifier-execution-model.md:2-4` (all three), `terminal-bench-release-identity.md:2-3` (S100, S092), `benchmark-grader-semantics.md:2` (S093) — and a one-entry adoption of the verifier model is sound for the registry only if `used-by` is written as the single admitted entry path (the staged cells would dangle on `terminal-bench-release-identity.md` ×2 and `benchmark-grader-semantics.md` ×1, invisible to `adoption_check.py:93-98` but caught by `registry_check.py:77-81`), with S093's anchor repaired of its escaped pipe, all three `opened` cells re-dated to 2026-10-25 by a real re-open, S092's 28-word span shortened, S100's `「」` quote made visible or accepted as unquoted, and the entry's "corrects the round-1 framing" premise re-pointed because the lane's held checklist `:71-74` already holds the stronger reading.
