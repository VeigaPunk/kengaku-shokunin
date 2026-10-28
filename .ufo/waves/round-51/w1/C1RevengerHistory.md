# C1RevengerHistory — timeline recovery for the three drifted surfaces (round 51, wave 1)

Seat: `C1RevengerHistory` (revenger, leaf). Item: recover, from the lane's own read-only git
history, the last committed round in which each of `~/Projects/webzites/repos/llm-wiki`,
`~/archive/bench-arena` and the `:34113` served model was **measured as resolving**, and the
**first** round that recorded its **absence** — a dated table that grounds the PROVINCE
correction's dates.

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7 (lane tip at measurement; stage-1 freeze `e07f131cf7037e58a21db6e1f3986cf401ad257c`; C1 before-receipt `297e17927ba9342a87ba27a48cc5270a001de7cb`).
All git calls below were read-only (`log`, `show`, `blame`, `rev-parse`). Nothing was written to
the lane outside this report file.

## Axes named

- **A1 freshness** — the axis C1 moves: do the PROVINCE surface rows carry true, dated
  availability facts? This seat supplies the *date truth* half (when each surface last resolved,
  when its absence was first recorded), not the probe half.
- **A2 evidence-chain completeness** — every date must resolve to a commit hash, a round number,
  a file:line and, where the lane recorded one, a capture timestamp.
- **A3 record non-regression** — the recovery must not require deleting or renumbering a row
  (C1 kill rule: `ROWS` must not fall below 9 and 10).

## Dated table (the deliverable)

Lane-local dates are `-0300`; UTC is given where the lane recorded a `Z` timestamp.

| Surface (PROVINCE row) | Last round **measured resolving** (commit + round + capture) | **First** committed round recording absence | Current state (frozen C1 probe at tip) |
|---|---|---|---|
| `~/Projects/webzites/repos/llm-wiki` (row at `PROVINCE.md:12`, SF01) | **round 14** — `0c16a79` (2026-09-29 01:21:34 -0300); measurement `2026-09-29T03:29:20Z`, `r14-scout-surfaces.md` S12 `git -C ~/Projects/webzites/repos/llm-wiki log -1` → `e66e614 …` **MATCH** | **round 16** — `7153e67` (2026-10-14 21:15:36 -0300), `corpus/lessons/round-16-recensus.md:23-24`: "`~/Projects/webzites/repos/llm-wiki` (SSOT) absent" | absent (probe `paths`, c1-before `PROBES present=13 absent=6`, `DRIFT SF01`) |
| `~/archive/bench-arena` (row at `PROVINCE.md:13`, SF02) | **round 14** — `0c16a79`; measurement `2026-09-29T03:29:20Z`, `r14-scout-surfaces.md` S11: archive tree resolves, content `0` files newer than 2026-09-28, **MATCH-content / DRIFT-path** (the *declared archive path* is the resolving one) | **round 16** — `7153e67`, `round-16-recensus.md:24-25`: "`~/archive/bench-arena` and `~/bench-arena` absent" | absent (`DRIFT SF02`) |
| `http://127.0.0.1:34113` (row at `PROVINCE.md:14`, SF03) | **round 14** — `0c16a79`; measurement `2026-09-29T03:29:19Z`, `r14-scout-surfaces.md` S2 `/health` → `200`, S1 `/v1/models` id **MATCH**, S4 sole listener pid 1299 **MATCH** | **round 15** — `d84e48d` (2026-10-14 09:41:08 -0300), `SCORECARD.md:212-219`: "`curl -s -m5 /health` → connection failure (000); `pgrep -a llama-server` → no rows; `systemctl --user status qwen-coder.service` → \"could not be found\"" | absent (probe `http` `/health`, `DRIFT SF03`) |

Two secondary rows of the same family, for completeness (not in the C1 drift list):

| Surface | Last measured resolving | First committed absence | Note |
|---|---|---|---|
| `~/bench-arena` (`PROVINCE.md:155`) | **round 12** — `r12-endpoint-freshness.md` §5.1: `ls -la ~/bench-arena` present, **NO-DRIFT** (evidence committed in `0c16a79`) | **round 14** — `r14-scout-surfaces.md` §5 **DRIFT: relocated to `~/archive/bench-arena`**; "Cited path no longer resolves" | round 13 did **not** probe it (see D4) |
| `/proc/1299/cmdline`, `qwen-coder.service`, jinja template (`PROVINCE.md:157`) | **round 14** — `r14-scout-surfaces.md` S1–S5 (pid 1299 EXACT_MATCH) | **round 15** — same `SCORECARD.md:212-219` block (`systemctl … could not be found`) | follows `:34113` exactly |

## Evidence chain, verbatim

Last-resolving round (`0c16a79`, round-14, committed 2026-09-29 01:21:34 -0300), from
`corpus/evidence/round14-fleet/r14-scout-surfaces.md`:

```
| S2 | `/health` | `curl -s -m5 -o /dev/null -w '%{http_code}' http://127.0.0.1:34113/health` | `200` (body `{"status":"ok"}`) | **MATCH** | 2026-09-29T03:29:19Z |
| S11 | Bench tree, relocated | `find ~/archive/bench-arena -newermt '2026-09-28 18:00' -type f | wc -l`; `stat -c %y` | `0` files; dir mtime `2026-08-29 03:58:10.451962237 -0300` | **MATCH-content / DRIFT-path** | 2026-09-29T03:29:20Z |
| S12 | llm-wiki resolves | `git -C ~/Projects/webzites/repos/llm-wiki log -1 --format='%h %cI %s'` | `e66e614 2026-08-08T21:40:55-03:00 Add product ship evidence…` | **MATCH** | 2026-09-29T03:29:20Z |
```

First-absence for `:34113` — round 15, `d84e48d`, `SCORECARD.md:212-217` (blame: line 212–219 all
`d84e48d 2026-10-14`):

```
- Served model `http://127.0.0.1:34113` — **ABSENT**: `curl -s -m5 /health` →
  connection failure (000); `pgrep -a llama-server` → no rows; `systemctl
  --user status qwen-coder.service` → "could not be found". The r10/r11/r14
  process-level pins (pid 1299, 41-token argv, q4_0 KV) remain high-confidence
  historical facts, per the scorecard's own rule that they are capture-time
  host state.
```

The **same commit** still asserted the other two as resolving (`SCORECARD.md:217-219`):

```
- `~/Projects/ufo-fsd-alpha` — **resolves** (present at new location);
  `~/archive/bench-arena` — resolves; `~/Projects/webzites/repos/llm-wiki` —
  resolves; `~/Projects/bounties/ledger/telemetry.jsonl` — still ABSENT.
```

First-absence for both paths — round 16, `7153e67` (2026-10-14 21:15:36 -0300),
`corpus/lessons/round-16-recensus.md:23-25`:

```
- `~/Projects/webzites/repos/llm-wiki` (SSOT) absent; `~/archive/bench-arena`
  and `~/bench-arena` absent; `~/.bailian` absent; `:34113` connection refused,
  pid 1299 / `qwen-coder.service` / jinja path absent — all still written as
  current in `SKILL.md`/`PROVINCE.md`.
```

Independent later confirmations (all read, none contradicting):

- **round-13 re-dispatch receipt** — `corpus/evidence/round13-coverage/surface-receipt.json`,
  `observed_at: 2026-10-15T04:49:50.049812+00:00`, `"dispatch": "2026-10-15 re-dispatch;
  historical round-13 material preserved"`; both paths `"exists": false`, endpoint
  `"<urlopen error [Errno 111] Connection refused>"`. Committed in `05cb955` (2026-10-16).
- **round-19/20 battery P9** — `corpus/evidence/probe-r19-P9-absent-port.log`, first request
  `2026-10-16T09:15:04Z`: `curl: (7) Failed to connect to 127.0.0.1:34113`; `derived:
  curl_exit=7 http_code=000 outcome_class=connection-refused`. Committed `af0e3e6`.
- **round-25 pre-repair state check** — `corpus/evidence/round25-calibration/state-check-before-6180e4f.txt:7-9`:
  `{"ABSENT_marked": false, "exists": false, "path": "~/Projects/webzites/repos/llm-wiki"}`, same for
  `~/archive/bench-arena/`; the markers were added by `8ea41f9` (round 25, 2026-10-20 21:44:48 -0300).
- **round-27 state-v4** — `corpus/evidence/round27-calibration/state-v4-base.json:365-388`:
  both paths `"exists": false, "ABSENT_marked": true`, verdict `MATCH`.
- **No post-round-16 record in `corpus/evidence/` shows either path `"exists": true`** (swept
  `corpus/evidence` for the two path literals with an `"exists": true` neighbour: 0 hits for the
  wiki path, 0 real hits for the archive path — the single context-window match was a different
  path, `lessons/round-24-verifier-spotcheck.md`).

## Divergences this recovery exposes (the dates PROVINCE carries are wrong in four places)

**D1 — `PROVINCE.md:152` ("absent since round-13 coverage receipt") is chronologically false.**
Round 13 (2026-09-28, `LOG.md:20`) was "ack-label prompt-intent audit; hermetic, **no endpoint
traffic**" and probed no surface. The `round13-coverage` receipt is a **2026-10-15 re-dispatch**
product, i.e. *later* than round 14's resolving measurement (2026-09-29T03:29:20Z). The first
absence record is round 16 (2026-10-14).

**D2 — `PROVINCE.md:154` ("round 14 … absent per round-13 receipt") conflates the last-resolving
round with an absence receipt.** Round 14 is the last round the archive path was *measured
resolving*; the round-13 receipt cannot be earlier evidence of its absence. First absence:
round 16.

**D3 — `PROVINCE.md:156` dates the `:34113` refusal to "the round-13 re-dispatch (2026-10-15)";
the first committed refusal is round 15, 2026-10-14** (`d84e48d`). The re-dispatch is a later
confirmation, one day and one round late.

**D4 — `PROVINCE.md:155` says `~/bench-arena` last resolved "round 13"; round 13 did not probe.**
Last measured resolving is round 12 (`r12-endpoint-freshness.md` §5.1, present, NO-DRIFT); first
absence round 14 (DRIFT-path).

**D5 — the marker date already in the three drifted rows is the *repair* date, not the absence
date.** `PROVINCE.md:12-14` each end with `**ABSENT 2026-10-20** (round 25: first local path fails
`test -e`; superseded by §Province map)` — added by `8ea41f9` on 2026-10-20, six days after the
measured absence. If the correction dates the absence, the truthful date is **2026-10-14**
(round 15 for the endpoint, round 16 for the two paths); 2026-10-20 is when the marker was
appended.

**D6 — two different "does this row tell the truth" rules are in play.** Round 27 read the same
rows as `MATCH` because its check is "first backticked local path agrees with `test -e` **and**
`ABSENT_marked`" (`state-v4-base.json:361-388`), while R51's manifest reads the row's primary
assertion as `prose=present` → `DRIFT`. The correction must satisfy **R51's** rule (the row's
asserted prose must itself state absence), not round 27's. Consequence for the L1: appending
another dated marker does not clear `DRIFT`; the present-tense assertion inside the first cell
(`— `wiki/ai/…`, `Home.md`, `raw/``, `… all resolve at the archive path`, `— `/v1/models`,
`/health`, `/v1/chat/completions``) is what the counter reads.

**D7 (inference, wording) — SF03's marker copies the local-path text verbatim.** `PROVINCE.md:14`
carries "(round 25: first local path fails `test -e`)" although the row's check is an HTTP endpoint
(`ss -ltn`/curl, per `PROVINCE.md:156`). The copied wording is observed; that it was a
copy-paste rather than a deliberate reading is inference.

## What this grounds for the PROVINCE correction (dates only — the L1 lands the edit)

- `llm-wiki`: last resolve **2026-09-29** (round 14, `0c16a79`); absent from **2026-10-14**
  (round 16, `7153e67`).
- `~/archive/bench-arena`: last resolve **2026-09-29** (round 14); absent from **2026-10-14**
  (round 16).
- `:34113`: last resolve **2026-09-29** (round 14); absent from **2026-10-14** (round 15,
  `d84e48d`), independently re-measured refused 2026-10-16T09:15:04Z (`P9`) and 2026-10-15T04:49:50Z
  (`surface-receipt.json`).
- `~/bench-arena` (map row only): last resolve **2026-09-29** (round 12 measurement, committed in
  round 14); absent from **2026-09-29** round 14 (relocation).

## Limits

- Round 15's "resolves" sentence for the two paths has **no saved transcript**; round 16 already
  ruled it transcript-less ("historical accuracy unresolved, current truth negative. Do not
  re-pin", `round-16-recensus.md:29-30`). So the transition between round 14 (measured present)
  and round 16 (measured absent) is **not dated more finely than 2026-09-29 → 2026-10-14**; the
  round-15 sentence is a contradictory record, not a measurement.
- "No post-round-16 record shows the paths present" is absence-of-record plus negative probes at
  rounds 25/27/28; it is not a continuous liveness monitor.
- I did not probe the host myself (sibling seats own probing). The "current state" column is the
  frozen C1 counter's own probe, run at tip: `PROBES run=19 present=13 absent=6`, `DRIFT 3`.
- Round numbers here are the lane's own; the round-13 evidence directory is a re-dispatch product
  and its `round: 13` label does **not** mean its measurements precede round 14.
- `git log -S` over `PROVINCE.md corpus/evidence corpus/knowledge` (17 / 11 / 20 commits for the
  three literals) was used only to bound the search; every date in the table comes from a named
  file:line read at the tip, not from the pickaxe alone.

## Commands run (verbatim, read-only)

```sh
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
git rev-parse HEAD                      # 4090c3db79d11279ab5e5121ba25e74aa316e6e7
git log --format='%h %ad %s' --date=short -S'webzites/repos/llm-wiki' -- PROVINCE.md corpus/evidence corpus/knowledge
git log --format='%h %ad %s' --date=short -S'archive/bench-arena'  -- PROVINCE.md corpus/evidence corpus/knowledge
git log --format='%h %ad %s' --date=short -S'34113'                -- PROVINCE.md corpus/evidence corpus/knowledge
for d in corpus/evidence/round*; do grep -rl "webzites/repos/llm-wiki" "$d" | wc -l; ...; done
git blame -L 12,14  --date=short PROVINCE.md
git blame -L 152,156 --date=short PROVINCE.md
git blame -L 212,219 --date=short SCORECARD.md
git log --format='%h %ad %s' --date=iso --follow -- corpus/evidence/round14-fleet/r14-scout-surfaces.md
git log --format='%h %ad %s' --date=iso --follow -- corpus/evidence/round13-coverage/surface-receipt.json
git log --format='%h %ad %s' --date=iso --follow -- corpus/lessons/round-16-recensus.md
git log --format='%h %ad %s' --date=iso --follow -- corpus/evidence/probe-r19-P9-absent-port.log
git show 8ea41f9 -- PROVINCE.md
git show d84e48d --stat
python3 plans/round51_surfaces.py --lane .     # frozen C1 command, read-only; output below
```

Frozen counter output at tip (abridged to the lines this seat cites):

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
MANIFEST plans/round51-surfaces.json entries=19 sections=2
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
  DETAIL DRIFT SF01 prose=present state=absent (the row's first path cell asserts the wiki tree resolves; round-15/25 rows alrea)
  DETAIL DRIFT SF02 prose=present state=absent (the row asserts the relocated battery resolves at the archive path)
  DETAIL DRIFT SF03 prose=present state=absent (the row declares a live served model endpoint)
STALE 0
UNVERDICTED 1
NUMBER-DRIFT 1
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
```

The three drift lines reproduce the before-receipt (`.ufo/waves/round-51/claims/c1-before.txt`,
`REV 297e179…`) exactly at the tip: no round between the freeze and the tip changed the drift set.

## Scratch

Scratch root `/fast/scratch/hyaku/kengaku-r51/C1RevengerHistory` was created, used only as
`TMPDIR` for the counter run, and **removed before this report was finalised** — no fixture clone
was needed (all reads ran against the lane, read-only). `df -h /fast` at start: `804G … 554G
available (32% used)`.

VERDICT: PASS — all three drifted surfaces' timelines are recovered from committed evidence with
commit + round + capture timestamp: last resolving **round 14 / 2026-09-29** for all three, first
absence **round 15 / 2026-10-14** for `:34113` (`d84e48d`) and **round 16 / 2026-10-14** for both
paths (`7153e67`); current state absent at tip per the frozen counter. The PROVINCE map's existing
dates are wrong in four places (D1–D4) and the rows' `ABSENT 2026-10-20` markers are repair dates,
not absence dates (D5); appending markers alone will not clear `DRIFT` under R51's reading (D6).
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
