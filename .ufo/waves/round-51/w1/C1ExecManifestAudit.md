# C1ExecManifestAudit — `plans/round51-surfaces.json` vs `PROVINCE.md`, row by row

Seat: `C1ExecManifestAudit` (executor), kengaku round 51 / hyaku run 11.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scope: the single named item — audit the 19 manifest entries against the PROVINCE rows they anchor,
on two axes (is `prose` the correct reading of the row; is the anchor the right anchor for that row),
and flag rows whose prose is ambiguous.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7

`PROVINCE.md`, `plans/round51-surfaces.json` and `plans/round51_surfaces.py` are byte-identical between
the stage-1 freeze commit `e07f131cf7037e58a21db6e1f3986cf401ad257c` and this REV
(`git diff --stat e07f131..HEAD -- PROVINCE.md plans/round51-surfaces.json plans/round51_surfaces.py`
prints nothing), so the audit reads the frozen artefacts.

## Axes named

1. **Prose truth (freshness)** — for each entry, does `prose` (present|absent) record what the anchored
   PROVINCE row actually asserts about the entry's probed target, read whole (all three cells, including
   any dated `ABSENT` marker)?
2. **Anchor truth (freshness)** — does each entry's `anchor` identify the row the entry claims, uniquely
   inside its declared section, and is that the right row for the entry's surface?
3. **Probe adequacy (secondary, recorded not scored)** — does the entry's probe test the target the row
   declares, and enough of it that `state` can falsify the row?

## Method and exact commands

All commands run with cwd `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; `TMPDIR` exported to
`/fast/scratch/hyaku/kengaku-r51/C1ExecManifestAudit`; nothing written outside scratch and this report.

```sh
git rev-parse HEAD
git log --oneline -6
git diff --stat e07f131cf7037e58a21db6e1f3986cf401ad257c..HEAD -- PROVINCE.md plans/round51-surfaces.json plans/round51_surfaces.py
python3 plans/round51_surfaces.py --lane .            # frozen C1 command, run twice (see Observation O1)
sha256sum grader.py plans/attrib_probe.py ~/.local/share/ds-flash-shim/shim.py
ss -ltnH 'sport = :8791' ; ss -ltnH 'sport = :34113'
python3 -c "<socket connect to 127.0.0.1:{8791,34113}>"
for p in <host paths of SF01..SF06>; do test -e "$p" && echo PRESENT || echo ABSENT; done
for p in <in-repo paths of SF07..SF19>; do test -e "$p" && echo PRESENT || echo ABSENT; done
for d in round8-horizon round9-replication round9-fleet round10-fleet round11-power round11-fleet \
         round12-ladder round12-fleet round13-ack-state round13-coverage round14-fleet round18-kimi-routing; \
  do test -d corpus/evidence/$d && echo PRESENT || echo ABSENT; done
grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md
grep -oE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md | grep -oE 'S[0-9]{3,}' | sort -u | wc -l
grep -oE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md | grep -oE 'S[0-9]{3,}' | sort -u | awk -F'S' '$2+0<=42' | wc -l
python3 plans/attrib_calibration.py --summary ; echo "EXIT=$?"      # row SF18's declared check
python3 plans/state_check.py --summary        ; echo "EXIT=$?"      # row SF19's declared check
python3 <scratch>/anchor_audit.py                                   # imports section_rows() from the frozen counter
```

`anchor_audit.py` (scratch, 20 lines) reuses the frozen counter's own `section_rows()` so anchor→row
mapping is computed exactly as the counter computes it, then reports per entry: in-section hit count,
file-wide hit lines, the hit row's first cell, and whether the row carries a dated `ABSENT` marker.

No tools were installed or upgraded; nothing to record under the operator tooling authorization.
No git/jj mutation was run anywhere; `git status --porcelain` before and after my measurements shows
only pre-existing untracked wave files (no tracked-file change).

## The 19-row table

`Lnn` = PROVINCE.md line. Quotes are verbatim; `…` marks an elision inside a long cell, never at the
decisive clause. `P` = prose verdict, `A` = anchor verdict.

| ID | PROVINCE row (line; verbatim, trimmed) | prose | P | anchor → line | A | one-line reason |
|---|---|---|---|---|---|---|
| SF01 | L12 `\| Research notes (SSOT for eval craft) \| ~/Projects/webzites/repos/llm-wiki — … \| digest into corpus/knowledge/eval-* entries; the ~/wikillm/llm-wiki path does **not** exist here (test -e → absent) **ABSENT 2026-10-20** (round 25: first local path fails test -e; superseded by §Province map) \|` | present | **DISAGREE** | `\| Research notes (SSOT for eval craft) \|` → L12 | AGREE | The row's own dated verdict on its first path is `ABSENT 2026-10-20`; `present` reads only the Path cell and ignores the row's operative marker (target measured absent). |
| SF02 | L13 `\| Local benchmark battery \| ~/archive/bench-arena/ — relocated intact …; tasks/, grade.sh, loop.sh, … all resolve at the archive path \| … historical commands using the old path are frozen evidence **ABSENT 2026-10-20** … \|` | present | **DISAGREE** | `` `~/archive/bench-arena/` — relocated intact `` → L13 | AGREE | Row contradicts itself ("all resolve at the archive path" vs dated `ABSENT`); the dated marker is the operative verdict, so `present` is a reading of the superseded half. |
| SF03 | L14 `\| Served local model \| http://127.0.0.1:34113 — /v1/models, /health, /v1/chat/completions (…) … identity re-probed via /v1/models + /health 200 each round \| … hermetic gates pin committed bytes, never /proc **ABSENT 2026-10-20** (round 25: first local path fails test -e; …) \|` | present | **DISAGREE** | `` `http://127.0.0.1:34113` — `/v1/models` `` → L14 | AGREE | Row asserts both "re-probed 200 each round" and a dated `ABSENT`; `present` cannot be the unique reading (see ambiguity flag A3). |
| SF04 | L15 `\| Route telemetry \| ~/Projects/bounties/ledger/telemetry.jsonl — **ABSENT**, reconfirmed round 14 … \| … **historical inference about model service** only; never treat the path as live \|` | absent | AGREE | `` `~/Projects/bounties/ledger/telemetry.jsonl` — **ABSENT** `` → L15 | AGREE | Row's assertion is unambiguously absent; the undated marker is a real row defect (correctly counted as `UNVERDICTED 1`), not a prose error. |
| SF05 | L16 `\| Client CLI telemetry \| ~/.bailian/telemetry.jsonl, ~/.bailian/wiki-sync-state.json \| quota-vs-auth failure split, poll-verb rule **ABSENT 2026-10-20** (round 25: first local path fails test -e; …) \|` | absent | AGREE | `` `~/.bailian/telemetry.jsonl`, `~/.bailian/wiki-sync-state.json` `` → L16 | AGREE | Dated `ABSENT` on the row's first path, both files measured absent; marker scope is the first path only (flag A4). |
| SF06 | L17 `\| Model catalogs \| ~/.bailian/skills/bailian-docs-llm-wiki/models/{index.md,models.jsonl}, https://huggingface.co/api/models, https://openrouter.ai/api/v1/models \| selection fields, open-weight twins **ABSENT 2026-10-20** (round 25: first local path fails test -e; …) \|` | absent | AGREE | `` `~/.bailian/skills/bailian-docs-llm-wiki/models/{index.md,models.jsonl}` `` → L17 | AGREE | Correct for the local catalog (both files absent); the row also declares two remote endpoints with a different status (flag A1), and the probe tests `index.md` only. |
| SF07 | L18 `\| Own probe artifacts \| corpus/evidence/round8-horizon/, round9-replication/, round9-fleet/, round10-fleet/, round11-power/, round11-fleet/, round12-ladder/, round12-fleet/, round13-ack-state/, round14-fleet/ \| durable run bytes + analyses + L2 fleet artifacts; nothing headline-bearing cited from /tmp … \|` | present | AGREE | `` `corpus/evidence/round8-horizon/`, `round9-replication/` `` → L18 | AGREE | No absence claim; I verified all 10 named dirs present. Anchor is a second-cell fragment but is unique in-section and in the whole file. |
| SF08 | L19 `\| In-repo gate \| grader.py (repo root; python3 grader.py → exit 0/1/2; --selftest S0–S7) \| hermetic offline replay of **four** probe trees (r8/r9/r11/r12); 733 checks … \|` | present | AGREE | `\| In-repo gate \| `grader.py` (repo root;` → L19 | AGREE | `grader.py` present at repo root; row makes no absence claim. |
| SF09 | L20 `\| Public literature \| arXiv / ACL Anthology / ICLR proceedings / vLLM docs / GitHub issues (URLs in corpus/knowledge/eval-prior-art-calibration.md) \| novelty pricing of local findings \|` | present | AGREE | `\| Public literature \| arXiv / ACL Anthology` → L20 | AGREE | Row asserts external literature and presupposes the in-repo URL record; that record resolves, so `present` is correct for the only target the probe can see (the external sites are never probed — probe-adequacy note P2). |
| SF10 | L108 `\| In-repo verdict gate \| test -e grader.py && sha256sum grader.py \| present; 90c87c88…ae941f (replay tree r8/r9/r11/r12; …) \|` | present | AGREE | `\| In-repo verdict gate \| `test -e grader.py && sha256sum grader.py`` → L108 | AGREE | Row asserts present with a digest; measured `90c87c8865022681…e5ae941f`, matches the pin. |
| SF11 | L109 `\| Own probe artifacts \| for d in round8-horizon … round18-kimi-routing; do test -d corpus/evidence/$d \|\| echo missing $d; done (prints nothing) \| all present; plus 28 root receipt logs … \|` | present | AGREE | `\| Own probe artifacts \| `for d in round8-horizon ` → L109 | AGREE | Row asserts all 12 dirs present; I verified all 12 present. Anchor's `for d in` fragment is what separates it from the `## Surfaces` twin. |
| SF12 | L110 `\| Attribution instrument + frozen tables \| test -e plans/attrib_probe.py && sha256sum plans/attrib_probe.py; test -e plans/attrib-r21-frozen.md / -r22- / -r23- \| all present; probe sha256 today 489f938a…16e06b (floats between trials …) \|` | present | AGREE | `\| Attribution instrument + frozen tables \| `test -e plans/attrib_probe.py `` → L110 | AGREE | All four named files present; digest measured `489f938a198e08cf…c90616e06b`, matches the pin (risk R2: the row itself declares the digest floats). |
| SF13 | L111 `\| Corpus gate docs \| test -e corpus/QUALITY.md \| present (admission bar Q1–Q8 + round-closure criteria, created round 24) \|` | present | AGREE | `\| Corpus gate docs \| `test -e corpus/QUALITY.md`` → L111 | AGREE | File present; row asserts present. |
| SF14 | L112 `\| Public-literature registry \| test -e corpus/SOURCES.md \| present; 25 rows, contract-v1 census clean (corpus/evidence/round24-census/after.txt); receipts corpus/evidence/round24-sources/gate.md \|` | present | AGREE | `\| Public-literature registry \| `test -e corpus/SOURCES.md`` → L112 | AGREE | `present` is right for the file; the recorded `count_claim: 25` is not — the row is superseded in-section to 42 by its own corrections, and the live registry holds 170 (finding F3). |
| SF15 | L113 `\| ds-flash-shim source (read-only) \| sha256sum ~/.local/share/ds-flash-shim/shim.py \| present; 42d86d99…15a386 — identical to the disclosed pin in evidence/attrib-r22-*.log / attrib-r23-stream.log \|` | present | AGREE | `\| ds-flash-shim source (read-only) \| `sha256sum ~/.local/share/ds-flash-shim/shim.py`` → L113 | AGREE | File present; measured `42d86d99d4265821…c8f8c15a386`, matches the pin. |
| SF16 | L114 `\| Live probe endpoint \| ss -ltn 'sport = :8791' \| LISTEN on 127.0.0.1:8791 (ds-flash-shim, read-only shim; :8793 not probed this round) \|` | present | AGREE | `\| Live probe endpoint \| `ss -ltn 'sport = :8791'`` → L114 | AGREE | Measured `LISTEN 0 512 127.0.0.1:8791` and TCP connect ok; row asserts LISTEN (probe is a connect, not `ss` — note P3). |
| SF17 | L115 `\| Public literature \| URLs cited in knowledge/eval-prior-art-calibration.md, attrib-prior-art-r21.md, and the ART dossier \| reachable-by-citation only — documentation reads only this round, no live model/endpoint traffic \|` | present | **DISAGREE** | `\| Public literature \| URLs cited in `knowledge/eval-prior-art-calibration.md`` → L115 | AGREE | The row's paths are written without `corpus/` and both fail `test -e` at lane root; the manifest probes repaired paths (`corpus/knowledge/…`), so `present` is a reading of a row the manifest silently rewrote (finding F4). |
| SF18 | L116 `\| Interval re-verdict instrument (round 25) \| python3 plans/attrib_calibration.py --summary and --selftest \| exit 0 / exit 0; P1 receipts sha256-pinned; 4 unique samples, 92/92 correct, transitions FAIL>UNTESTED 2, PASS>INDETERMINATE 1 \|` | present | AGREE | `\| Interval re-verdict instrument (round 25) \| `python3 plans/attrib_calibration.py --summary`` → L116 | AGREE | Instrument present and its declared check still exits 0 at this REV (`TOTAL … scored_trials=92 correct=92 … mismatches=0`, `EXIT=0`); the manifest probe tests existence only (note P4). |
| SF19 | L117 `\| State-assertion check (round 25) \| python3 plans/state_check.py --summary and --selftest \| exit 0 / exit 0 on the landed tree (base 6180e4f: exit 1, 10 mismatches) \|` | present | AGREE | `\| State-assertion check (round 25) \| `python3 plans/state_check.py --summary`` → L117 | AGREE | Instrument present and its declared check still exits 0 at this REV (`VERDICT: PASS — all comparable frozen assertions match`, `EXIT=0`); probe tests existence only (note P4). |

**Tally — prose: 15 AGREE / 4 DISAGREE (SF01, SF02, SF03, SF17). Anchors: 19/19 AGREE.**

Every anchor resolves to exactly one row inside its declared section (in-section hits = 1 for all 19),
and to the row whose first cell is the surface the entry names — with one shape note: SF02, SF03, SF05,
SF06, SF07 anchor on a fragment of the second cell rather than the first cell. All five are still unique
inside their section. SF05's and SF06's anchor text also occurs in the `### Historical` table
(L160, L161) — invisible to the counter because it searches only the entry's own section, so not an
`ANCHOR-DUP`, but a reader grepping PROVINCE.md gets two hits.

## Ambiguity flags (rows that assert two different things)

| Flag | Row | Two assertions |
|---|---|---|
| A1 | SF06 (L17) | The local catalog is **absent, dated 2026-10-20**, while the two remote catalogs (`https://huggingface.co/api/models`, `https://openrouter.ai/api/v1/models`) are a different status — `### Historical` L171 records them as "not probed this round (docs-reads-only policy) | unverified". Two targets, two different claims, one `prose`. |
| A2 | SF02 (L13) | One target, two different assertions in one row: "… all resolve at the archive path" (Path cell) vs `**ABSENT 2026-10-20**` (Use cell). |
| A3 | SF03 (L14) | One target, two different assertions: "identity re-probed via /v1/models + /health 200 each round" vs `**ABSENT 2026-10-20**`, and the marker's stated reason ("first local path fails `test -e`") is inapplicable to an HTTP endpoint — it is boilerplate copied from the path rows. |
| A4 | SF05 (L16) | Two targets (`telemetry.jsonl`, `wiki-sync-state.json`); the dated marker and the probe cover only "first local path". `wiki-sync-state.json` is asserted by nobody and measured by nobody (I measured it absent). |
| A5 | SF14 (L112) | One target, three counts: row cell **25**; in-section round-25 correction L119 → **37**; R26-E3a/E10 L180/L190 → **42** `id_set=exact` with the instruction "count `SOURCES.md` ids ≤42, not future additions"; live registry at this REV **170**. |
| A6 | SF17 (L115) | Three referents (`knowledge/eval-prior-art-calibration.md`, `attrib-prior-art-r21.md`, "the ART dossier") under one assertion; two are probed only after a path repair, and "the ART dossier" is not a file in the lane (its only lane referents are `corpus/SOURCES.md` L3 and `corpus/README.md` L160/L327 — i.e. a document, not a path). |

SF01 is not a two-target ambiguity in the A1 sense: its two targets (`…/llm-wiki`, `~/wikillm/llm-wiki`)
are both asserted absent. It is a *declares-then-dates-absent* contradiction (surface-table declaration
vs dated marker), which is why its prose reading is contested rather than ambiguous between two live
claims.

## Cross-cutting findings

**F1 — The three DRIFT entries are manifest-prose errors, not PROVINCE text that "still asserts they
resolve".** `plans/round-51-claims.md` §C1 says the before measurement shows `DRIFT 3` because
"rows still assert they resolve". At this REV each of the three rows already carries
`**ABSENT 2026-10-20**` in its Use cell (L12, L13, L14), and the counter's own `UNVERDICTED` check
passes on all three for exactly that reason (only SF04 is `UNVERDICTED`). The recorded `prose: present`
reads the Path cell and discards the row's dated verdict. Consequence for the landing: appending a new
dated marker to those rows would leave `DRIFT 3` untouched; the truthful repair is to set
`prose: absent` for SF01/SF02/SF03 (and, for SF02/SF03, fix the contradictory half of the row — the
"all resolve at the archive path" clause and the inapplicable "first local path fails test -e"
parenthetical). Any repair that re-asserts presence instead would also drive `UNVERDICTED` to 4.

**F2 — SF17's row paths do not resolve as written.** `test -e knowledge/eval-prior-art-calibration.md`
and `test -e knowledge/attrib-prior-art-r21.md` are both absent at lane root (`ls -d knowledge` →
"No such file or directory"); the files exist at `corpus/knowledge/…`, which is how the sibling row
SF09 (L20) writes them. The manifest's probe silently prepends `corpus/`, so `state`/`prose` are
measured against a path the row does not contain. A reader following the row gets absent while the
counter prints present. Landing options: correct the row's two paths (append-only correction), or
record the row as absent-with-date; either way the manifest probe must name the path the row names.

**F3 — SF14's `count_claim: 25` is stale by the row's own append-only corrections.** Measured at this
REV: `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → **170**; unique ids → **170** (S001–S177);
ids ≤42 → **42**. The lane's own `plans/state_check.py --summary` prints, at this REV:
`SUPERSEDED: P3b.province.public-literature-registry.rows:112 — {… "correction_line": 190,
"correction_tokens": ["rows=42", "id_set=exact"], … "observed": {… "rows": 42, …}, "claim": ["25"]}`.
So the row-as-corrected value is 42 (frozen population S001–S042), the row cell says 25, and the live
registry says 170 — the probe's 170 is a count of the current file, not of the population the
corrections freeze. `NUMBER-DRIFT 1` is therefore a true finding, but the manifest cannot reach
`NUMBER-DRIFT 0` by changing `count_claim` alone without also stating which population the row now
claims (170 live rows vs 42 frozen) — the landing must pick one and word the row to match.

**F4 — Probe adequacy gaps (secondary axis, not part of the C1 predicate).** P1: SF07's probe tests
5 targets, of which `corpus/evidence/round13-coverage` is *not* named by the L18 row, and it omits 6
dirs the row does name (`round9-fleet`, `round10-fleet`, `round11-power`, `round11-fleet`,
`round12-fleet`, `round13-ack-state`); SF11's probe covers those 7 of its 12. Union across the two
entries covers all 12 Core dirs and all 10 Surfaces dirs, but no single entry probes its own row
completely, so a row-level regression is only caught by the sibling entry. P2: SF09/SF17 assert
external literature that no probe touches (by design — "reachable-by-citation only"). P3: SF16's probe
is a TCP connect, so it cannot distinguish ds-flash-shim from any other listener on 8791, while the row
names the process. P4: SF18/SF19 rows assert *exit 0* of two commands; the manifest probes only file
existence, so a broken instrument would keep `state=present`. I ran both commands read-only at this
REV: `attrib_calibration.py --summary` → `EXIT=0` (`scored_trials=92 correct=92 … mismatches=0`);
`state_check.py --summary` → `EXIT=0` (`VERDICT: PASS — all comparable frozen assertions match`), so
both rows are true today but the counter cannot see them break.

**F5 — SF12's sha256 pin is a declared-floating digest.** The row itself says the probe digest "floats
between trials and landing per the r21 lesson — frozen anchors live in the `-frozen.md` files", yet the
manifest makes that digest the entry's `state`. It matches today (`489f938a…16e06b`); the first
legitimate edit to `plans/attrib_probe.py` flips the counter to `STALE 1` for a reason the row declares
benign. Recorded risk for the landing, not a prose error.

**O1 — One transient counter reading, recorded because it changes a printed detail line.** At
`18:22:5xZ` the frozen command printed `DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=0`
and, in the same batch, `sed`/`wc -l`/`grep -cE` on `corpus/SOURCES.md` returned 0 lines. At
`18:23:0xZ` the same command printed `probe says SOURCES rows=170`, matching the before receipt, and the
file measured 142293 bytes / 224 lines / 170 pattern rows with `stat` mtime `2026-10-28 15:22:02 -0300`
(unchanged) and an empty `git status --porcelain corpus/SOURCES.md`. I could not reproduce the zero
reading; `NUMBER-DRIFT` stays 1 either way, so no claim depends on it, but an after-measurement that
lands in such a window would print a misleading detail line.

## Observed outputs (verbatim where they are evidence)

Frozen counter, first run (the transient window):

```
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
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=0
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
EXIT=1
```

Frozen counter, second run (reproducible state):

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
PROBES run=19 present=13 absent=6 errors=0
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
EXIT=1
```

Target probes:

```
90c87c8865022681b1249a42ea580726932d2e97ec0de43e0c89efe0e5ae941f  grader.py
489f938a198e08cf8c30efc3ca24ea5fac90ef3909d80aec0b1f62c90616e06b  plans/attrib_probe.py
42d86d99d42658214e362c2759ecab88a03de005e9ed93e9c1804cbf8c15a386  /home/vgpnk/.local/share/ds-flash-shim/shim.py
LISTEN 0      512    127.0.0.1:8791 0.0.0.0:*
(no listener on 34113)
8791 connect ok
34113 connect fail [Errno 111] Connection refused
```

```
ABSENT  /home/vgpnk/Projects/webzites/repos/llm-wiki
ABSENT  /home/vgpnk/wikillm/llm-wiki
ABSENT  /home/vgpnk/archive/bench-arena
ABSENT  /home/vgpnk/bench-arena
ABSENT  /home/vgpnk/Projects/bounties/ledger/telemetry.jsonl
ABSENT  /home/vgpnk/.bailian/telemetry.jsonl
ABSENT  /home/vgpnk/.bailian/wiki-sync-state.json
ABSENT  /home/vgpnk/.bailian/skills/bailian-docs-llm-wiki/models/index.md
ABSENT  /home/vgpnk/.bailian/skills/bailian-docs-llm-wiki/models/models.jsonl
PRESENT /home/vgpnk/.local/share/ds-flash-shim/shim.py
ABSENT  /home/vgpnk/.config/systemd/user/qwen-coder.service
ABSENT  /home/vgpnk/.config/llama/qwen-coder-godspeed.jinja
ABSENT  /proc/1299/cmdline
PRESENT grader.py / corpus/QUALITY.md / corpus/SOURCES.md / plans/attrib_probe.py
PRESENT plans/attrib-r21-frozen.md / plans/attrib-r22-frozen.md / plans/attrib-r23-frozen.md
PRESENT plans/attrib_calibration.py / plans/state_check.py
PRESENT corpus/knowledge/eval-prior-art-calibration.md / corpus/knowledge/attrib-prior-art-r21.md
ABSENT  knowledge/eval-prior-art-calibration.md
ABSENT  knowledge/attrib-prior-art-r21.md
PRESENT corpus/evidence/{round8-horizon,round9-replication,round9-fleet,round10-fleet,round11-power,
        round11-fleet,round12-ladder,round12-fleet,round13-ack-state,round13-coverage,round14-fleet,
        round18-kimi-routing}   (all 12)
```

Row-declared checks for SF18/SF19 (read-only; both instruments write only inside their own selftest
fixtures):

```
attrib_calibration.py --summary -> EXIT=0
TOTAL files=9 scored_files=5 trial_only=4 blocks=10 superseded=5 unique_samples=4 duplicates=1
      scored_trials=92 correct=92 incorrect=0 … stored_checks=119 mismatches=0
state_check.py --summary -> EXIT=0
VERDICT: PASS — all comparable frozen assertions match
```

Anchor audit (per entry: in-section hits, file-wide hit lines, row first cell):

```
SF01 sec='## Surfaces' line=12 insection_hits=1 file_hits=[12]  row_first_cell='Research notes (SSOT for eval craft)'
SF02 sec='## Surfaces' line=13 insection_hits=1 file_hits=[13]  row_first_cell='Local benchmark battery'
SF03 sec='## Surfaces' line=14 insection_hits=1 file_hits=[14]  row_first_cell='Served local model'
SF04 sec='## Surfaces' line=15 insection_hits=1 file_hits=[15]  row_first_cell='Route telemetry'
SF05 sec='## Surfaces' line=16 insection_hits=1 file_hits=[16, 160] row_first_cell='Client CLI telemetry'
SF06 sec='## Surfaces' line=17 insection_hits=1 file_hits=[17, 161] row_first_cell='Model catalogs'
SF07 sec='## Surfaces' line=18 insection_hits=1 file_hits=[18]  row_first_cell='Own probe artifacts'
SF08 sec='## Surfaces' line=19 insection_hits=1 file_hits=[19]  row_first_cell='In-repo gate'
SF09 sec='## Surfaces' line=20 insection_hits=1 file_hits=[20]  row_first_cell='Public literature'
SF10 sec='### Core' line=108 insection_hits=1 file_hits=[108] row_first_cell='In-repo verdict gate'
SF11 sec='### Core' line=109 insection_hits=1 file_hits=[109] row_first_cell='Own probe artifacts'
SF12 sec='### Core' line=110 insection_hits=1 file_hits=[110] row_first_cell='Attribution instrument + frozen tables'
SF13 sec='### Core' line=111 insection_hits=1 file_hits=[111] row_first_cell='Corpus gate docs'
SF14 sec='### Core' line=112 insection_hits=1 file_hits=[112] row_first_cell='Public-literature registry'
SF15 sec='### Core' line=113 insection_hits=1 file_hits=[113] row_first_cell='ds-flash-shim source (read-only)'
SF16 sec='### Core' line=114 insection_hits=1 file_hits=[114] row_first_cell='Live probe endpoint'
SF17 sec='### Core' line=115 insection_hits=1 file_hits=[115] row_first_cell='Public literature'
SF18 sec='### Core' line=116 insection_hits=1 file_hits=[116] row_first_cell='Interval re-verdict instrument (round 25)'
SF19 sec='### Core' line=117 insection_hits=1 file_hits=[117] row_first_cell='State-assertion check (round 25)'
```

SOURCES census:

```
SOURCES pattern rows: 170
unique ids: 170
ids<=42: 42
max id: S177
```

## Limits

- I audited the 19 declared entries only; a surface PROVINCE declares in prose but not in either table
  is invisible to both the counter and this audit (the manifest's own declared limit).
- `prose` is a reading, so the four DISAGREE verdicts are readings of the row's *operative* assertion
  (the row's dated marker / literal paths). For SF02 and SF03 the row genuinely asserts both ways; I
  state which half I take and why, and the landing owns the choice.
- The external surfaces (arXiv/ACL/ICLR/vLLM/GitHub, HF/OpenRouter catalogs) were not probed; the
  lane's documented policy is citation-only, and this seat made no network requests.
- I did not run `--selftest` on either instrument (only the `--summary` mode the rows name), and I did
  not re-run the C1 controls; those are other seats' items.
- `corpus/SOURCES.md` counts are point-in-time at this REV; the row's frozen population (42) and the
  live registry (170) are different questions (F3).

## VERDICT

The manifest's **anchor axis is sound (19/19)**: every anchor lands in exactly one row of its declared
section and in the row the entry names, with five second-cell fragments (SF02/SF03/SF05/SF06/SF07)
that are still unique in-section. The **prose axis is wrong on 4 of 19** — SF01, SF02, SF03 (each row
already carries `**ABSENT 2026-10-20**`, so `present` reads the superseded half; the C1 before-note's
"rows still assert they resolve" is inaccurate) and SF17 (the row's paths lack `corpus/` and do not
resolve as written; the probe silently repairs them). Six rows carry ambiguous prose (A1–A6), SF14's
`count_claim: 25` is superseded to 42 by the row's own corrections against a live registry of 170, and
four probe-adequacy gaps (P1–P4) leave rows the counter cannot falsify. No manifest change was made by
this seat; the repairs above are recommendations for the L1.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
