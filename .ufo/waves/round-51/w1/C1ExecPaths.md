# C1ExecPaths — every declared HOST path, probed independently

Axes named: **(1) host-surface truth** — does each path `PROVINCE.md` declares exist today, and
what does it look like; **(2) relocation falsification** — is there a moved copy under `~` that a
reader would mistake for the declared one; **(3) counter coverage** — is each declared host path
actually probed by `plans/round51-surfaces.json`, since a declared path nobody probes cannot move
the C1 predicate. No production file was edited; this report is the only write.

## Revision measured

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
4090c3db79d11279ab5e5121ba25e74aa316e6e7
```

Freeze `e07f131cf7037e58a21db6e1f3986cf401ad257c` is an ancestor of HEAD
(`git merge-base --is-ancestor` → yes), and the three C1 files are byte-identical at both:

```
$ git diff --stat e07f131cf7037e58a21db6e1f3986cf401ad257c HEAD -- PROVINCE.md plans/round51-surfaces.json plans/round51_surfaces.py
(no output, exit 0)
$ git rev-parse HEAD:PROVINCE.md HEAD:plans/round51-surfaces.json HEAD:plans/round51_surfaces.py
a1492cdd46c238b8991c3b9aa79939dd78d358dc
154ba1cfa0871e7b8c26fbe5118e87565a7bf7f6
6107c605925310ed64433b1f27d3459e8836ed43
$ git rev-parse e07f131...:PROVINCE.md ...:plans/round51-surfaces.json ...:plans/round51_surfaces.py
a1492cdd46c238b8991c3b9aa79939dd78d358dc
154ba1cfa0871e7b8c26fbe5118e87565a7bf7f6
6107c605925310ed64433b1f27d3459e8836ed43
```

So every reading below applies to the frozen tree, not to a moved tip.

## Frozen counter, run as declared (context, not the assignment)

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/round51_surfaces.py --lane . ; echo "EXIT=$?"
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
MANIFEST plans/round51-surfaces.json entries=19 sections=2
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
  DETAIL DRIFT SF01 prose=present state=absent (the row's first path cell asserts the wiki tree resolves; round-15/25 rows alrea)
  DETAIL DRIFT SF02 prose=present state=absent (the row asserts the relocated battery resolves at the archive path)
  DETAIL DRIFT SF03 prose=present state=absent (the row declares a live served model endpoint)
STALE 0
UNVERDICTED 1
  DETAIL UNVERDICTED SF04 row has no ABSENT <ISO date> marker
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
EXIT=1
```

Identical to the before-receipt figures in `plans/round-51-claims.md` (`DRIFT 3`, `UNVERDICTED 1`,
`NUMBER-DRIFT 1`, `present=13`, exit 1). My probes below explain *why* each absent row is absent and
whether the recorded state is truthful.

## Probe commands (exact)

```sh
paths=( ~/Projects/webzites/repos/llm-wiki ~/archive/bench-arena ~/bench-arena \
        ~/Projects/bounties/ledger/telemetry.jsonl ~/Projects/bounties \
        ~/.bailian/telemetry.jsonl ~/.bailian/wiki-sync-state.json \
        ~/.bailian/skills/bailian-docs-llm-wiki/models/index.md \
        ~/.local/share/ds-flash-shim/shim.py )
for p in "${paths[@]}"; do
  if test -e "$p"; then echo "PATH $p PRESENT"; stat -c '  STAT %F %s %y' "$p"
  else echo "PATH $p ABSENT"
       if test -e "$(dirname "$p")"; then echo "  PARENT $(dirname "$p") present"
       else echo "  PARENT $(dirname "$p") absent"; fi; fi
done
find ~ -maxdepth 5 -name '<basename>' -not -path '*/.git/*'      # per basename, verbatim as assigned
sha256sum ~/.local/share/ds-flash-shim/shim.py
```

`$HOME` printed `/home/vgpnk`, `readlink -f ~` printed `/home/vgpnk`.

Verbatim output of the existence/stat loop:

```
PATH /home/vgpnk/Projects/webzites/repos/llm-wiki ABSENT
  PARENT /home/vgpnk/Projects/webzites/repos absent
PATH /home/vgpnk/archive/bench-arena ABSENT
  PARENT /home/vgpnk/archive absent
PATH /home/vgpnk/bench-arena ABSENT
  PARENT /home/vgpnk present
PATH /home/vgpnk/Projects/bounties/ledger/telemetry.jsonl ABSENT
  PARENT /home/vgpnk/Projects/bounties/ledger absent
PATH /home/vgpnk/Projects/bounties ABSENT
  PARENT /home/vgpnk/Projects present
PATH /home/vgpnk/.bailian/telemetry.jsonl ABSENT
  PARENT /home/vgpnk/.bailian absent
PATH /home/vgpnk/.bailian/wiki-sync-state.json ABSENT
  PARENT /home/vgpnk/.bailian absent
PATH /home/vgpnk/.bailian/skills/bailian-docs-llm-wiki/models/index.md ABSENT
  PARENT /home/vgpnk/.bailian/skills/bailian-docs-llm-wiki/models absent
PATH /home/vgpnk/.local/share/ds-flash-shim/shim.py PRESENT
  STAT regular file 16957 2026-10-15 14:15:50.923131309 -0300
```

Parent-chain probe:

```
PRESENT /home/vgpnk/Projects directory 2026-10-28 14:09:05.497912371 -0300
ABSENT /home/vgpnk/Projects/webzites
ABSENT /home/vgpnk/Projects/webzites/repos
ABSENT /home/vgpnk/archive
ABSENT /home/vgpnk/.bailian
ABSENT /home/vgpnk/.bailian/skills
PRESENT /home/vgpnk/.local/share directory 2026-10-27 21:21:47.161781809 -0300
```

Relocation search, depth 5 exactly as assigned (all six basenames, `2>/dev/null`):

```
=== find llm-wiki ===
=== find bench-arena ===
=== find bounties ===
=== find wiki-sync-state.json ===
=== find bailian-docs-llm-wiki ===
=== find telemetry.jsonl (maxdepth 5) ===
=== find shim.py ===
/home/vgpnk/.local/share/devin-shim/shim.py
/home/vgpnk/.local/share/cursor-shim/shim.py
/home/vgpnk/.local/share/oauth-shim/shim.py
/home/vgpnk/.local/share/ds-flash-shim/shim.py
/home/vgpnk/.local/share/glm-flash-shim/shim.py
/home/vgpnk/.local/share/antigravity-shim/shim.py
/home/vgpnk/.local/share/claude-shim/shim.py
/home/vgpnk/kimi-code-wiring-oauths/shims/cursor/shim.py
/home/vgpnk/kimi-code-wiring-oauths/shims/claude/shim.py
/home/vgpnk/kimi-code-wiring-oauths/shims/antigravity/shim.py
/home/vgpnk/kimi-code-wiring-oauths/shims/devin/shim.py
/home/vgpnk/kimi-code-wiring-oauths/shims/ds-flash/shim.py
/home/vgpnk/kimi-code-wiring-oauths/shims/glm-flash/shim.py
/home/vgpnk/kimi-code-wiring-oauths/shims/oauth/shim.py
```

Secondary, deeper, pruned search (my own extension, bounded, 1.86 s, no timeout):

```
$ timeout 180 find /home/vgpnk -maxdepth 8 \
    \( -name .git -o -name node_modules -o -name .cache -o -name .venv -o -name .jj \) -prune -o \
    \( -name 'llm-wiki' -o -name 'bench-arena' -o -name 'telemetry.jsonl' \
       -o -name 'wiki-sync-state.json' -o -name 'bailian-docs-llm-wiki' -o -name 'bounties' \) -print
(no output)
SECONDARY_EXIT=1
```

`exit 1` from `find` here is "no match", not an error (stderr was empty).

## Table

| # | path | present/absent | evidence command | relocation candidate |
|---|---|---|---|---|
| 1 | `~/Projects/webzites/repos/llm-wiki` | **absent** | `test -e` → absent; `test -e ~/Projects/webzites` → absent (whole chain gone) | none at depth 5 or pruned depth 8 |
| 2 | `~/archive/bench-arena` | **absent** | `test -e` → absent; `test -e ~/archive` → absent | none at depth 5 or 8 |
| 3 | `~/bench-arena` | **absent** | `test -e` → absent; parent `~` present | none at depth 5 or 8 |
| 4 | `~/Projects/bounties/ledger/telemetry.jsonl` | **absent** | `test -e` → absent; `ledger` parent absent | none at depth 5 or 8 |
| 5 | `~/Projects/bounties` | **absent** | `test -e` → absent; `~/Projects` present | none at depth 5 or 8 |
| 6 | `~/.bailian/telemetry.jsonl` | **absent** | `test -e` → absent; `~/.bailian` absent | none at depth 5 or 8 |
| 7 | `~/.bailian/wiki-sync-state.json` | **absent** | `test -e` → absent; `~/.bailian` absent | none at depth 5 or 8 |
| 8 | `~/.bailian/skills/bailian-docs-llm-wiki/models/index.md` | **absent** | `test -e` → absent; `models` parent absent | none at depth 5 or 8 |
| 9 | `~/.local/share/ds-flash-shim/shim.py` | **present** | `test -e` → present; `stat` → regular file, 16957 B, 2026-10-15 14:15:50.923131309 -0300; `sha256sum` → `42d86d99d42658214e362c2759ecab88a03de005e9ed93e9c1804cbf8c15a386` | the declared path itself; 13 other `shim.py` files exist (see F7) |

## Findings for the L1

**F1 — the eight absences are real, not a probe artifact.** Every absent path fails `test -e`, and in
four cases the *parent* is gone too (`~/Projects/webzites`, `~/archive`, `~/.bailian`,
`~/Projects/bounties`), so the failure is a removed tree, not a renamed leaf. This confirms
`state=absent` for SF01, SF02, SF04, SF05, SF06 — the counter's `STALE 0` is correct, and no row can
be repaired by re-pointing at a sibling inside those trees, because there is no sibling.

**F2 — no relocation anywhere under `~`.** `llm-wiki`, `bench-arena`, `bounties`, `telemetry.jsonl`,
`wiki-sync-state.json`, `bailian-docs-llm-wiki` have zero hits at depth 5 and zero at pruned depth 8.
That independently re-confirms the round-14 parenthetical in `PROVINCE.md:15` ("no relocation under
`~/Projects`, `~/archive`, or Trash") as still true on 2026-10-28 — including Trash, which sits under
`~/.local/share/Trash` and was not pruned.

**F3 — the one live host surface still matches its pin.** `~/.local/share/ds-flash-shim/shim.py` is
present, unchanged since 2026-10-15 14:15:50, and hashes to
`42d86d99d42658214e362c2759ecab88a03de005e9ed93e9c1804cbf8c15a386`, i.e. the Core row
(`PROVINCE.md:113`) pin `42d86d99…15a386` and the pin quoted in `corpus/evidence/attrib-r22-*.log`.
SF15's `present` and its `sha256` probe are truthful at this tip. Two `.bak` files sit beside it
(`shim.py.20261015-112418.bak`, `shim.py.20261015-112620.bak`, 16070 B each) — backups, not the
declared target, and not probed.

**F4 — three declared host paths are declared but never probed by the manifest.** The rows declare
more than the entries check:

| row | declares | manifest probe (`SF`) | unprobed declared path |
|---|---|---|---|
| `PROVINCE.md:16` (SF05) | `~/.bailian/telemetry.jsonl`, `~/.bailian/wiki-sync-state.json` | `SF05` → `targets: ["~/.bailian/telemetry.jsonl"]` | `~/.bailian/wiki-sync-state.json` |
| `PROVINCE.md:17` (SF06) | `…/models/{index.md,models.jsonl}` + 2 URLs | `SF06` → `targets: ["…/models/index.md"]` | `…/models/models.jsonl` |
| `PROVINCE.md:13` (SF02) + `:155` | `~/archive/bench-arena`, and `~/bench-arena` as the "relocated from" path | `SF02` → `targets: ["~/archive/bench-arena"]` | `~/bench-arena` (no entry at all; `### Historical` is not in `sections`) |

Consequence for the freshness axis: if `wiki-sync-state.json`, `models.jsonl` or `~/bench-arena`
reappeared, **no counter line would change**. All three are absent today (table rows 3, 7, and the
`models.jsonl` sibling of row 8), so this is a coverage gap, not a live drift. L1's call whether to
extend `SF05`/`SF06` `targets` (and mint an entry for `~/bench-arena`) or record it as a stated limit.

**F5 — the two `## Surfaces` DRIFT rows are already dated, so the correction is textual.** Lines 12
and 13 each end with `**ABSENT 2026-10-20** (round 25: first local path fails test -e; superseded by
§Province map)` while their path cells still assert resolution ("relocated intact … all resolve at the
archive path"). My probes agree with the marker and with `state=absent`; the row body is what still
reads as present. That is exactly `DRIFT SF01/SF02`. Nothing in my measurement suggests the date is
wrong — 2026-10-20 is a lower bound on the absence, and the trees are still gone on 2026-10-28.

**F6 — `UNVERDICTED 1` is a missing date, nothing else.** `PROVINCE.md:15` reads
`… — **ABSENT**, reconfirmed round 14 (last resolved round 11 at 7,226 lines; …)`; there is no
`ABSENT <ISO date>` token on the line, which is what `ABSENT_RE` requires. The absence itself is
confirmed (rows 4–5 of the table). One dated marker clears it.

**F7 — a second `ds-flash` shim copy exists and is a different program.** `find` surfaced
`~/kimi-code-wiring-oauths/shims/ds-flash/shim.py`; its digest is
`026546c34bbbbd47329f06cee53f9c99e835805152edba4a4095a85227fb8a6c`, which does **not** match the
pinned `42d86d99…`. It is not a relocation of the declared surface (the declared path resolves), but
any seat that reads the sibling copy instead of `~/.local/share/ds-flash-shim/shim.py` will fail the
pin. Naming it here so the L1 can decide whether it deserves a dated row or a refusal line; I did not
promote it.

## Limits

- Relocation search is bounded: depth 5 exactly as assigned, plus one pruned depth-8 pass. A copy
  deeper than 8, or inside a pruned dir (`.git`, `node_modules`, `.cache`, `.venv`, `.jj`), would not
  have been seen.
- Home only (`/home/vgpnk`). `/root`, `/fast`, `/mnt`, `/media`, and external mounts were not searched;
  the declared paths are all under `$HOME`, so a move off-home is outside the probe's reach.
- `test -e` follows symlinks; a dangling symlink at a declared path would read absent. None of the
  declared paths existed at all (no `lstat` entry), so this did not bite, but a future dangling
  symlink would be reported absent by both this probe and the counter.
- Endpoint surfaces (SF03 `:34113`, SF16 `:8791`, `:8793`) were **not** probed — they are not host
  paths and are outside this item; the counter's own `http`/`port` probes stand unexamined by me.
- In-repo rows SF07/SF11 declare 10 and 12 evidence dirs; the manifest probes 5 and 7. I verified all
  10 + 12 dirs exist (`present` each), so the partial coverage hides no absence today, but the
  asymmetry is the same class as F4. Reported as observation only — in-repo coverage is another
  seat's item.
- No tool was installed or upgraded. No network call was made. No git write, no commit, no checkout.
- Scratch `/fast/scratch/hyaku/kengaku-r51/C1ExecPaths` was created (`TMPDIR` exported to it, 555 G
  free on `/fast` at start) and removed before yielding; nothing of this seat remains on disk there.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7

VERDICT: all nine declared host paths independently probed at REV 4090c3db (C1 files identical to freeze e07f131); the eight recorded-absent paths are genuinely absent with their parent trees gone and **no** relocation candidate at depth 5 or pruned depth 8, while `~/.local/share/ds-flash-shim/shim.py` is present and still matches its `42d86d99…15a386` pin — so SF01/SF02/SF04/SF05/SF06 `state=absent` and SF15 `state=present` are truthful, the counter's `STALE 0` is correct, and the three DRIFT/UNVERDICTED defects are prose defects (undated `ABSENT` at line 15; dated markers contradicted by present-tense path cells at lines 12–13) plus a real coverage gap: `wiki-sync-state.json`, `models.jsonl` and `~/bench-arena` are declared but never probed, so their resurrection would move no counter line.
