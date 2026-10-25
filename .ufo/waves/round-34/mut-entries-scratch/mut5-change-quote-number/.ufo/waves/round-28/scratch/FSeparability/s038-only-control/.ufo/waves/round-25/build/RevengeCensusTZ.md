# sources-census.sh date handling — E08 future-opened at the SP 21:00 UTC rollover

Lane: KengakuR25 (round 25, C1 novelty / C2 calibration axes). Scope: reverse-engineer
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` epoch()/E08 handling, decide
whether rows with `opened=2026-10-20` false-positive (E08) at round end in
TZ=America/Sao_Paulo after 21:00 local, and give a safe `opened` rule. Fleet script read
only; reproduction on a /tmp copy with synthetic rows.

## Answer (measured, not inferred)

**No false positive — and never can be, at either side of the rollover.**
`opened=2026-10-20` is accepted at every real clock state reachable from SP local time:
before 21:00 (UTC date `2026-10-20`), after 21:00 (UTC date `2026-10-21`), and any later
day. The premise direction is inverted: the 21:00 flip can only make the gate **more**
permissive as the UTC date advances, never less.

## Reconstructed mechanism (evidence chain, all script:NNN = sources-census.sh)

1. `TODAY=${TODAY:-$(date -u +%F)}` (script:90) — the comparison date is the **UTC
   calendar date**, TZ-blind by construction. `date -u +%F` is TZ-invariant (measured:
   identical under TZ=UTC / America/Sao_Paulo / Asia/Tokyo / Pacific/Kiritimati). The
   TZ=America/Sao_Paulo in the ticket changes **which UTC date the wall clock maps to**
   (SP −03:00, no DST since 2019 — verified: Jan and Jul 2026 both report `-0300`),
   it does not leak into `date -u`.
2. `TODAY_S=$(iso_epoch "$TODAY")` (script:91) → bash-side `iso_epoch()` (script:49-58):
   regex `^[0-9]{4}-[0-9]{2}-[0-9]{2}$`, `y==0` rejection, `mktime(sprintf("%04d %02d %02d
   00 00 00",y,m,d),1)` — the `1` flag forces **UTC**, then round-trip
   `strftime("%Y-%m-%d",t,1)==s` validates. Malformed/impossible dates return −1e15 →
   usage die.
3. gawk `epoch()` (script:584-590) is byte-identical logic, `INVALID_EPOCH=-1e15`.
4. E08 test (script:660-662):
   `opened_epoch==INVALID_EPOCH || opened_epoch>today_s` — **strict `>`**. Equal
   timestamps never fire: `epoch("2026-10-20")==today_s(2026-10-20)` ⇒ accepted. A row
   is "future" only if its UTC midnight epoch is strictly greater than today's UTC-midnight
   epoch, i.e. the opened date is at least one full day ahead of the UTC today.
5. Calendar sanity is the round-trip, not range checks: `2026-02-30`, `2026-00-15`,
   `2026-13-01`, `0000-01-01` all → −1e15 → E08 (measured matrix F2). `mktime(...,1)`
   also fixes the epoch independent of host TZ (SP has no DST wobble; Δ always 86400:
   epoch(2026-10-19)=1792368000, -20=1792454400, -21=1792540800, -22=1792627200).

## Measured behaviour (all runs against /tmp/r25tz copies)

Repro fixture: synthetic rows S900 (`opened=2026-10-20`, recheck 90d), S901
(`opened=2026-10-21`), S902 (`opened=2026-10-20`, recheck 1d) inserted **inside the
`## Registry` section** (lines 23-25) of a copy of
`kengaku-shokunin/corpus/SOURCES.md`; plus a dedicated `m-shokunin` one-row lane under a
/tmp fleet root. Commands: `sources-census.sh validate|overdue --file/--root … [--today D]`.

| opened | today (UTC date) | verdict |
|---|---|---|
| 2026-10-19 | 2026-10-20 or 2026-10-21 | accepted (validate rc 0) |
| **2026-10-20** | **2026-10-20 (before SP 21:00)** | **accepted — no E08** |
| **2026-10-20** | **2026-10-21 (after SP 21:00)** | **accepted — no E08** |
| 2026-10-21 | 2026-10-20 | E08 fires |
| 2026-10-21 | 2026-10-21 | accepted |
| 2026-10-22 | 2026-10-20 / 21 | E08 fires both |
| 2026-02-30 / 2026-00-15 / 2026-13-01 | either | E08 fires (round-trip) |

Boundary arithmetic: SP 20:59:59 local = 2026-10-20 20:59:59 UTC; SP 21:00:00 local =
2026-10-21 00:00:00 UTC (exact second; measured with `TZ=America/Sao_Paulo date`). So
"before 21:00" ≡ `date -u +%F` = 2026-10-20, "after" ≡ 2026-10-21. In both states
`epoch(opened=2026-10-20) <= today_s`, so no E08. Live-clock confirmation: run C
(`TZ=America/Sao_Paulo` at SP 21:17, no `--today`) resolved today=2026-10-21 and accepted
S900/S901.

Real-clock caveat (measured, run "stale-replay"): E08 can only fire for `opened=2026-10-20`
if `--today` is explicitly set **backwards** (`--today 2026-10-19`) — that is a caller
error, not the live clock. The watchdog gate never passes `--today`:
`sources_gate()` (shokunin-watchdog.sh:320-337) runs `census validate --root
$SHOKUNIN_ROOT $lane`, so it always uses the live `date -u +%F`.

## The real flip-time effect: overdue mode, not E08

`overdue` uses inclusive `due<=today_s` (script:684), `due=opened_epoch+NNd` (script:681).
Crossing SP 21:00 advances `today_s` by 86400 and **can newly flag rows**:

- Measured: `recheck=1d, opened=2026-10-20` → `not due` at today=2026-10-20
  (due=1792540800 > 1792454400), `overdue 0d` at today=2026-10-21 (inclusive ≤).
  Same for `recheck=0d` (due == opened midnight): reported `overdue 0d` on the opened
  date itself (run H: "tz overdue S105 0d recheck=0d opened=2026-10-20").
- Live-lane effect this round: none of the 26 kengaku rows (all `opened=2026-10-19`,
  recheck `2027-01-17`/`on-release`/`90d`) goes overdue at either boundary; the earliest
  NNd due is S024/S025 90d → 2027-01-17. `on-release` is symbolic → reported as cadence,
  never judged overdue (selftest lines 154-155 confirm).
- General: after the 21:00 flip, `opened=D, recheck=1d` rows newly read `overdue 0d`.

## Ground truth on the live lane (read-only)

`sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` →
`kengaku ok …`, rc=0. All 26 rows `opened=2026-10-19` ≤ today at both boundary dates;
no E08 possible. The 2026-10-19 header text ("re-opened today", SOURCES.md:4) matches
the registry dates. `selftest` → `selftest ok`, rc=0 (75 checks incl. E08-future-opened
at :133 and the TZ-invariance check `UTC-date-in-Sao-Paulo` at :160-161).

## Safe `opened` rule

1. Never write `opened` greater than **today's UTC date** (`date -u +%F` at write time).
   Same-UTC-day is explicitly safe (strict `>`); no SP-local adjustment is needed because
   the script is UTC-only end to end.
2. SP-local pitfall is the opposite direction: 21:00–23:59 SP local is already the next
   UTC day. A row written for "local today" during that window (e.g. `opened=2026-10-21`
   written at SP 22:00 on Oct 20) passes validate then, but would E08 on a stale replay
   against `--today 2026-10-20`. Rule: if the UTC date has already flipped, stamp the new
   UTC date, never the SP-local one.
3. Recheck cadence is what actually crosses at 21:00: a row is judged overdue on/after
   `opened+NNd` (inclusive). If a lane must survive a same-day verify, use `recheck≥2d`;
   `0d`/`1d` go overdue at or just after the flip. (Live lane minimum is 90d — safe.)

## Repro commands

```
rm -rf /tmp/r25tz && mkdir -p /tmp/r25tz/fleet/tz-shokunin/corpus /tmp/r25tz/fleet/m-shokunin/corpus
printf 'LANES="\ntz|tz-shokunin|tz fixture\n"\n' > /tmp/r25tz/fleet/shokunin.conf
# (SOURCES.md fixtures as described above; synthetic rows also inserted at lines 23-25
#  of a copy of kengaku-shokunin/corpus/SOURCES.md)
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /tmp/r25tz/fleet \
  --today 2026-10-20 m   # accepted
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /tmp/r25tz/fleet \
  --today 2026-10-21 m   # accepted
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh overdue --root /tmp/r25tz/fleet \
  --today 2026-10-21 tz  # S105/S106 overdue 0d — the genuine 21:00-crossing effect
```

## Installs

None (bash + gawk 5.4.1 + coreutils sufficed; no pacman/uv/npm transactions).

VERDICT: opened=2026-10-20 cannot E08 at the SP 21:00 rollover (strict >, UTC-only script); real flip effect is overdue-mode newly flagging recheck≤1d rows; rule — stamp `date -u +%F`, never SP-local "today".
