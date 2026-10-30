# R53ScoutSurfaces — per-surface reconnaissance at the lane's current HEAD

Seat: `R53ScoutSurfaces` (scout, wave 3 of 3). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Role: recon only — the lane tree was **not** modified (no `git add/commit/checkout/reset/pull`; only read commands
plus scratch clones under `/fast/scratch/hyaku/kengaku-r53/R53ScoutSurfaces/`).

## 1. What I did

1. Read `/home/vgpnk/.omp/agent/RULES.md` and `.ufo/waves/round-53/facts.md` (read in full) before writing a number.
2. Cloned the lane twice into scratch (`lane`, then `lane2` when the lane advanced mid-seat) and ran the
   round-51 surface counter from the **lane root**, exactly as the SKILL.md registry row documents.
3. Dumped all 20 manifest entries with their individual probe result and detail.
4. Probed the three historical-absent surfaces and the two live endpoints named in the seat spec.
5. Established the *cause* of every non-clean line: for SF14 the row-count history (`git show` at three tips),
   for SF20 the systemd unit's own journal (`systemctl --user status`, `journalctl --user -u lfm3-server.service`).
6. Ran repair experiments on **copies** of the manifest/PROVINCE under scratch to establish the minimum
   repair set and the counter's floor sensitivity.

No tool was installed or upgraded (nothing was missing); nothing to record for the tooling directive.

## 2. Lane HEAD I ran at

| what | hash |
|---|---|
| build-time tip named in the assignment | `b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe` (17:12:59 -0300) |
| lane HEAD when my second clone was made | `9ead4476bf55b1ea6490d0204b668195db4a4d1d` (17:13:00 -0300, "round-53: confirmations integrated … wave-3 spec+dispatch evidence") |

I ran the counter in **both** clones; the output is byte-identical apart from the `REV` line, and
`git diff --stat b1f79a54 9ead4476 -- PROVINCE.md plans/round51-surfaces.json corpus/SOURCES.md` is empty
(HEAD moved only wave-3 evidence), so every verdict below holds at the lane's current HEAD.

## 3. The command and its full output

```
$ cd /fast/scratch/hyaku/kengaku-r53/R53ScoutSurfaces/lane2
$ python3 plans/round51_surfaces.py --lane .
REV 9ead4476bf55b1ea6490d0204b668195db4a4d1d
MANIFEST plans/round51-surfaces.json entries=20 sections=2
ANCHORS total=20 dup=0 missing=0
ROWS section="## Surfaces" rows=10 entries=10 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=20 present=13 absent=7 errors=0
DRIFT 0
STALE 1
  DETAIL STALE SF20 probe=absent state=present (http://127.0.0.1:1234/health -> <urlopen error [Errno 111] Connection refused>)
UNVERDICTED 0
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 171, probe says SOURCES rows=186
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
EXIT=1
```

Saved verbatim: `.ufo/waves/round-53/w3/R53ScoutSurfaces/surfaces-counter-at-HEAD.txt`.

**Two non-clean lines only: `STALE SF20` and `NUMBER-DRIFT SF14`.** `DRIFT`, `UNVERDICTED`, `ANCHOR-DUP`,
`ANCHOR-MISSING`, `UNCOVERED`, `SECTION-MISSING` are all 0, and `RESOLVE` is met (13 present, floor 13).

## 4. The two non-clean lines, with the observed truth

### 4.1 NUMBER-DRIFT SF14 — **manifest-stale-growth**

* Manifest row: `plans/round51-surfaces.json` → entry `SF14`, section `### Core`, anchor
  `| Public-literature registry | \`test -e corpus/SOURCES.md\` |`, `state=present`, `prose=present`,
  `count_claim=171`, probe `{"kind":"count","target":"corpus/SOURCES.md","pattern":"^\\|\\s*S[0-9]{3,}\\s*\\|","label":"SOURCES rows"}`.
* Observed truth (commands):
  * `grep -cE '^\|\s*S[0-9]{3,}\s*\|' corpus/SOURCES.md` → **186**
  * `git show 11e79380:corpus/SOURCES.md | grep -cE …` (the round-51 landing of this very manifest) → **171**
  * `git show 536925b:corpus/SOURCES.md | grep -cE …` (round-52 base tip) → **186**
  * `git diff 11e79380..43438294 -- corpus/SOURCES.md | grep -cE '^\+\| *S[0-9]{3,}'` → **15**
    (round-52 commit `43438294` "… S179-S193 …" appended 15 rows: 171 + 15 = 186).
* Verdict: **manifest-stale-growth**. The lane legitimately grew; the manifest's `count_claim` was frozen at
  round 51 and never re-stated. The PROVINCE row itself (`PROVINCE.md:113`) also still reads
  "present; 171 rows (round 51: … → 171; 170 at the round-51 base tip plus S178)" — the row's *number* is stale
  too, although the counter does not check prose numbers (it only compares `prose` ∈ {present,absent} to `state`),
  which is why `DRIFT` stays 0. **Nothing broke.**
* Repair: set `count_claim` to 186 in the manifest **and** restate "186 rows" in `PROVINCE.md:113`.

### 4.2 STALE SF20 — **manifest-stale-broken** (the host surface was retired; it did **not** move)

* Manifest row: entry `SF20`, section `## Surfaces`, anchor `| Served local model (round 51 successor) |`,
  `state=present`, `prose=present`,
  probe `{"kind":"http","urls":["http://127.0.0.1:45669/health","http://127.0.0.1:1234/health"]}`.
* Observed truth (commands):
  * `curl -s -m 5 http://127.0.0.1:45669/health` → empty, `curl_exit=7` (connection refused).
  * `curl -s -m 5 http://127.0.0.1:1234/health` → empty, `curl_exit=7` (connection refused).
  * `ss -ltn` (full listing) → **no listener on 45669 and none on 1234**; 8791 is the only one of the
    lane's three live ports that is up.
  * `systemctl --user status lfm3-server.service` →
    `Active: inactive (dead) since Thu 2026-10-29 07:58:02 -03; 17h ago`,
    `Process: 272392 ExecStart=…/llama-server --models-dir /home/vgpnk/models/lfm3 … --port 1234 --jinja
    (code=exited, status=0/SUCCESS)`.
  * `journalctl --user -u lfm3-server.service --since 2026-10-28` → the router's last lines are
    `operator(): exit command received, exiting...` (07:57:02) then
    `systemd[1494]: Stopping … Stopped llama.cpp router serving LFM3 models …` (07:58:02) and **no restart**.
  * Capture-time truth in the lane: `corpus/evidence/round51/surfaces/endpoints.txt` (2026-10-28) records
    `HTTP http://127.0.0.1:45669/health -> 200`, `HTTP http://127.0.0.1:1234/health -> 200`,
    `LISTEN 127.0.0.1:45669`, `LISTEN 127.0.0.1:1234`, plus the served model ids and argv.
  * Not moved: the only llama.cpp server still on the host listens on **37323** and serves a different
    model blob from another seat's scratch (`ps -eo pid,etime,cmd | grep llama-server` →
    `/home/vgpnk/.local/opt/ollama-v0.40.11/lib/ollama/llama-server --model …/blobs/sha256-270cba1b… --port 37323`,
    a fixture of `kama-r61-closure`, not the lane's LFM3 surface). The LFM3 weights are still on disk
    (`/home/vgpnk/models/lfm3/LFM3-1.7B/LFM3-1.7B-Q8_0.gguf`), only the servers are stopped.
* Verdict: **manifest-stale-broken** — a clean, operator-initiated stop (exit status 0/SUCCESS, "exit command
  received"), not a crash of the lane's own making and not a relocation. The manifest froze a *live host
  endpoint* as `state=present` with no re-verification date; the endpoint died on 2026-10-29 07:58:02 -03,
  **after** round-53's wave-1/wave-2 measurements (the last wave-2 commit `e1e07d51` is 2026-10-28 23:39:59 -03).
  Nothing in the lane broke; the host retired the surface.
* Repair: set `SF20.state=absent` and `SF20.prose=absent`, and add a dated `**ABSENT 2026-10-30**` marker to
  the `PROVINCE.md:15` row (the counter's `UNVERDICTED` check requires an `ABSENT <ISO date>` marker on any row
  whose entry is `absent`).

## 5. Verdict per surface (all 20 entries)

Commands for the endpoint/absence rows are quoted in §4 and §6; the in-repo rows were probed by the counter
itself (per-entry detail in `per-surface-probes.txt`).

| id | section | manifest state | observed | verdict | command that shows it |
|---|---|---|---|---|---|
| SF01 | Surfaces | absent | absent | **manifest-right** | `test -e ~/Projects/webzites/repos/llm-wiki` → ABSENT |
| SF02 | Surfaces | absent | absent | **manifest-right** | `test -e ~/archive/bench-arena` → ABSENT (also `~/bench-arena` ABSENT: the round-14 relocation target itself is gone, as recorded) |
| SF03 | Surfaces | absent | absent | **manifest-right** | `http://127.0.0.1:34113/health` → connection refused; no listener on 34113 in `ss -ltn` |
| SF04 | Surfaces | absent | absent | **manifest-right** | `test -e ~/Projects/bounties/ledger/telemetry.jsonl` → missing (parent `~/Projects/bounties` absent too) |
| SF05 | Surfaces | absent | absent | **manifest-right** | `test -e ~/.bailian/telemetry.jsonl` → missing |
| SF06 | Surfaces | absent | absent | **manifest-right** | `test -e ~/.bailian/skills/bailian-docs-llm-wiki/models/index.md` → missing |
| SF07 | Surfaces | present | present | **manifest-right** | probe `paths`: all 5 evidence targets resolve |
| SF08 | Surfaces | present | present | **manifest-right** | probe `paths`: `grader.py` resolves |
| SF09 | Surfaces | present | present | **manifest-right** | probe `paths`: `corpus/knowledge/eval-prior-art-calibration.md` resolves |
| SF10 | Core | present | present | **manifest-right** | probe `sha256`: `grader.py` digest `90c87c88…` matches pin |
| SF11 | Core | present | present | **manifest-right** | probe `paths`: all 7 evidence dirs resolve |
| SF12 | Core | present | present | **manifest-right** | probe `sha256`: `plans/attrib_probe.py` digest `489f938a…` matches pin |
| SF13 | Core | present | present | **manifest-right** | probe `paths`: `corpus/QUALITY.md` resolves |
| SF14 | Core | present | present | **manifest-stale-growth** | probe `count`: `SOURCES rows=186` vs `count_claim 171` (§4.1) |
| SF15 | Core | present | present | **manifest-right** | probe `sha256`: `~/.local/share/ds-flash-shim/shim.py` digest `42d86d99…` matches pin |
| SF16 | Core | present | present | **manifest-right** | `ss -ltn 'sport = :8791'` → LISTEN 127.0.0.1:8791 |
| SF17 | Core | present | present | **manifest-right** | probe `paths`: both knowledge files resolve |
| SF18 | Core | present | present | **manifest-right** | probe `paths`: `plans/attrib_calibration.py` resolves |
| SF19 | Core | present | present | **manifest-right** | probe `paths`: `plans/state_check.py` resolves |
| SF20 | Surfaces | present | **absent** | **manifest-stale-broken** | both endpoints refused; unit inactive since 2026-10-29 07:58:02 -03 (§4.2) |

**No `surface-moved` case exists.** 17 surfaces manifest-right, 1 manifest-stale-growth (SF14), 1
manifest-stale-broken (SF20). Coverage is complete and current: `UNCOVERED 0` for both declared sections
(`## Surfaces` 10 rows/10 entries, `### Core` 10 rows/10 entries), and `PROVINCE.md` is **unchanged** since the
round-51 landing (`git log 11e79380..HEAD -- PROVINCE.md` → empty), so no new surface row slipped in uncovered.

## 6. The seat-spec spot checks (historical-absent + live endpoints)

```
$ ss -ltn 'sport = :8791'
LISTEN 0 512 127.0.0.1:8791 0.0.0.0:*
$ curl -s -m 5 http://127.0.0.1:45669/health   → (empty) curl_exit=7
$ curl -s -m 5 http://127.0.0.1:1234/health    → (empty) curl_exit=7
$ test -e ~/Projects/webzites/repos/llm-wiki  → ABSENT
$ test -e ~/archive/bench-arena                → ABSENT
$ test -e ~/Projects/bounties                   → ABSENT
```
All three historical-absent surfaces are **still absent**; of the two live endpoints, **8791 is up** and
**45669/1234 are down**. Read-only probes only; no model traffic was generated. Saved:
`endpoints-and-absent.txt`.

## 7. Minimum repair set (measured, on copies — the lane was not touched)

`repair-experiment.txt` (manifest/PROVINCE copies under scratch; `--manifest/--province` overrides):

| experiment | change | result |
|---|---|---|
| E0 baseline | none | exit 1 — STALE 1, NUMBER-DRIFT 1, `PREDICATE R51-C1 fail` |
| E1 | `SF14.count_claim`→186, `SF20.state/prose`→absent, dated `ABSENT 2026-10-30` on `PROVINCE.md:15` | **exit 0, `PREDICATE R51-C1 pass`**, all problem counters 0, `RESOLVE observed_present=13 floor=13 verdict=met` |
| E2 | E1 + `resolve_floor` 13→12 | exit 0 (floor change is **not** needed) |
| E3 | only `SF14.count_claim`→186 | exit 1 — STALE 1 remains: **fixing the count alone does not turn the row green** |
| E4 | E1 minus the PROVINCE dated marker | exit 1 — UNVERDICTED 1: the dated `ABSENT` marker is mandatory |

Consequences the L1 should carry:
* **Three edits** turn the `round51-surfaces` registry row green; the `resolve_floor` of 13 needs no change —
  SF20 is already counted in the 7 absent, so `observed_present` stays 13 and the floor stays met (measured, E1).
* Fixing only SF14 leaves the row red (E3) — the ledger's current reason names SF14 alone, so the ledger
  **under-describes the cause** at HEAD.

## 8. Implication for R53-C2 (tip-state ledger)

`plans/round53-tipstate.json` (78 rows) records for `round51-surfaces`:
`{"argv": ["python3","plans/round51_surfaces.py","--lane","."], "exit": 1, "kind": "entry", "state": "red",
"evidence": "NUMBER-DRIFT SF14 row claims 171, probe says SOURCES rows=186", "reason": "… after round 52 appended
S179-S193 … PROVINCE.md line 113 and manifest count_claim 171 were never updated"}`.

At HEAD `9ead4476` the same argv yields **exit 1** and the same `NUMBER-DRIFT` line, but the counter's **first**
`DETAIL` line is now `STALE SF20 …` (the counter prints STALE before NUMBER-DRIFT). So the row's `exit`/`state`
still hold, while its `evidence` field is one defect out of date: at HEAD the row is red for **two independent
reasons**, and the second (SF20) only appeared after the endpoint was stopped at 2026-10-29 07:58 -03 — i.e.
after the wave-1/wave-2 measurements that produced the ledger entry. The L1's re-declaration should say so
explicitly (and record that the row stays red until the three-part E1 repair lands).

## 9. Calibration observation for whoever re-measures the row (counter hygiene)

`plans/round51_surfaces.py`'s `paths` probe resolves **relative** targets against the **process CWD**
(`expand()` → `Path(p)`), *not* against `--lane`. Measured:

```
$ cd <scratch>; python3 lane2/plans/round51_surfaces.py --lane lane2
PROBES run=20 present=3 absent=17 errors=0
STALE 11 … RESOLVE observed_present=3 floor=13 verdict=violated  → PREDICATE R51-C1 fail
$ cd lane2; python3 plans/round51_surfaces.py --lane .
PROBES run=20 present=13 absent=7 … STALE 1, NUMBER-DRIFT 1 → PREDICATE R51-C1 fail
```

So the registry row must be executed **from the lane root** (SKILL.md:634 documents exactly that: "lane root").
Any C2 re-measurement that runs the row from a scratch parent directory produces 11 spurious `STALE` rows plus a
`RESOLVE … violated`. The counter's own selftest is green: `python3 plans/round51_surfaces.py --selftest` →
`[selftest] cases=9 failures=0`, `[selftest] ALL PASS`, exit 0 (the per-fixture `PREDICATE` lines it prints are the
fixtures' own output). Saved: `counter-hygiene-selftest-and-cwd.txt`.

## 10. Files produced (absolute paths)

* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScoutSurfaces.md` — this report.
* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScoutSurfaces/surfaces-counter-at-HEAD.txt`
  — full counter output at `9ead4476` (verbatim, 18 lines).
* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScoutSurfaces/per-surface-probes.txt`
  — all 20 entries: anchor, probe spec, observed state and detail (82 lines).
* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScoutSurfaces/endpoints-and-absent.txt`
  — `ss`, `curl`, `systemctl --user status` and the three `test -e` results + the full listener list.
* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScoutSurfaces/growth-evidence-SF14.txt`
  — SOURCES row counts at three tips, the +15 diff, and the two PROVINCE rows (113, 15) at HEAD.
* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScoutSurfaces/repair-experiment.txt`
  — E0–E4 results (the repair set and the floor sensitivity).
* `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScoutSurfaces/counter-hygiene-selftest-and-cwd.txt`
  — selftest output and the cwd-sensitivity measurement.

Scratch (`/fast/scratch/hyaku/kengaku-r53/R53ScoutSurfaces/`, two shared clones + fixture copies) was removed
at exit of this seat (`rm -rf`, verified gone). `scripts/hyaku/disk-guard.sh status` was checked before the heavy pass:
`/fast` had 464G free, `/fast/scratch/hyaku` 463.2G free, no ENOSPC.

## 11. Exact commands run (for replay)

```
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r53/R53ScoutSurfaces/lane
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r53/R53ScoutSurfaces/lane2
git -C …/lane2 rev-parse --show-toplevel ; git -C …/lane2 rev-parse HEAD
cd …/lane2 && python3 plans/round51_surfaces.py --lane .
cd …/lane2 && python3 plans/round51_surfaces.py --selftest
ss -ltn 'sport = :8791' ; ss -ltn
curl -s -m 5 http://127.0.0.1:45669/health ; curl -s -m 5 http://127.0.0.1:1234/health
test -e ~/Projects/webzites/repos/llm-wiki ; test -e ~/archive/bench-arena ; test -e ~/Projects/bounties
systemctl --user status lfm3-server.service --no-pager
journalctl --user -u lfm3-server.service --since 2026-10-28 --no-pager
git show 11e79380:corpus/SOURCES.md | grep -cE '^\|\s*S[0-9]{3,}\s*\|'      # 171
git show 536925b:corpus/SOURCES.md | grep -cE '^\|\s*S[0-9]{3,}\s*\|'       # 186
grep -cE '^\|\s*S[0-9]{3,}\s*\|' corpus/SOURCES.md                           # 186
git diff 11e79380..43438294 -- corpus/SOURCES.md | grep -cE '^\+\| *S[0-9]{3,}'  # 15
git log --oneline 11e79380..HEAD -- PROVINCE.md plans/round51-surfaces.json   # (empty)
git diff --stat b1f79a54 9ead4476 -- PROVINCE.md plans/round51-surfaces.json corpus/SOURCES.md  # (empty)
```

Report: .ufo/waves/round-53/w3/R53ScoutSurfaces.md
