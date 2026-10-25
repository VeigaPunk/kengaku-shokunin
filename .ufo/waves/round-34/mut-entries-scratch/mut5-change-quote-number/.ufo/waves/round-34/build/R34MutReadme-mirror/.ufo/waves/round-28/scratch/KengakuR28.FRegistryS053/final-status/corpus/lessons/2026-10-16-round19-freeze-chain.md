# Round 19 — the freeze is the contract: what a 32-seat preregistration battery stressed

2026-10-16. First run of the standing battery (`plans/probe-battery-r19.md`,
9 probes, 23 binary + 7 numeric components, 19-request budget) plus four
seat-level prediction files. Receipts: `corpus/evidence/probe-r19-*.log`
(15 files, 07:43–08:04Z), plan §7/§7.1, `plans/probe-battery-TEMPLATE.md`.
The scorer's close-out (`corpus/knowledge/probe-battery-r19.md`) had not
landed at lesson write time (~08:07Z); everything below cites landed
artifacts only, and the aggregate calibration read is that file's to land.
The round took the parent's example — *predictions must be frozen before the
first request; timestamps are the contract* — and showed where that contract
actually breaks: not at the requests, but at the freeze.

1. **The ordering gate held everywhere it was enforced in code; the one
   breach proved the rule.** Verified chains: shim-ds seat predictions
   hashed before any request (block sha256 `78de64d9…`, filed 07:43:30Z) <
   freeze 07:52:04Z < first request 07:52:48Z; glm seat prereg 07:55:05Z <
   first request 07:56:26.388Z; every battery-governed log filed in the v1
   window carries `first_request_utc` 07:52:25–07:53:40Z > frozen
   07:52:04Z. The single breach — runner-leg-opencode's two live requests
   07:45:00–04Z, before the battery file existed — came from a "dry" mode
   that was a label, not a gate: the probe loop never checked `--live`
   (`probe-r19-opencode-health.log` §DEFECT 0). The reusable part is the
   containment: verbatim self-report with receipts, gate fixed to exit
   before the loop, re-tested at 0 sockets, outcomes excluded from scoring.
   A dry-run flag must default to no-network; enforcement lives in code,
   not in the seat's attention.

2. **The freeze itself is a race-prone protocol, not a line (BR-1).** The
   registrar posted `FROZEN: 2026-10-16T07:52:04Z sha256:e3f08a09…` from a
   hash computed ~07:50:47Z over pre-rebase bytes while the battery-author
   was still editing — the posted hash never covered the bytes runners
   read. Compute-then-write across concurrent editors. The repair (re-freeze
   07:55:58Z `e1a86777…` after a double-read stability check) verifies
   byte-exact now:
   `sed -n '1,/FROZEN-PREDICTIONS-ANCHO[R]/p' plans/probe-battery-r19.md | sha256sum`
   → `e1a867773ef14ce457a0d560180587324dd07b4deea1ec76d0c2adf65aaa00a1`,
   equal to the FROZEN line. The v1 hash does not reproduce from any slice
   of the current file — correctly so: it identifies superseded bytes, and
   plan §7.1 records it as exactly that. Fix that must migrate forward:
   re-verify immediately before writing (plan §7 step 4).

3. **A hash procedure that embeds its own search pattern hashes the wrong
   range.** The original §7 step-2 command
   `sed -n '1,/FROZEN-PREDICTIONS-ANCHOR/p'` self-matches: the pattern
   occurs inside the §7 procedure's own command text, so the range
   truncated at that line instead of running to the anchor. The `[R]`
   bracket (`ANCHO[R]`) breaks the self-match. Adjacent trap: hash
   conventions must state the exact byte range — the shim-ds seat hash
   `78de64d9…` reproduces only once "through the line 'computed at file
   time):' inclusive" is read as including that line's trailing newline
   (verified both ways: without the newline → `976516e7…`, with → exact
   match). An auditor who cannot reproduce a hash should exhaust the
   convention's literal readings before filing a breach.

4. **Amending predictions mid-flight is the cardinal breach; re-hashing
   caught it.** Runners executed 07:52:25–07:53:40Z under the v1 freeze;
   the battery was amended ~07:54:27Z (387→429 lines: §6 P4/P5 rows
   re-based on the operator's M7/M9 leg reorders, totals 18→20 requests,
   the §7 bracket fix) without a re-freeze until 07:55:58Z.
   runner-quota-23 re-hashed at 07:55Z, found
   `d2f08f12…` ≠ FROZEN `e3f08a09…`, and scoped the exposure from the diff:
   P1's §6 rows are byte-identical in both versions → no exposure; the
   amended components (4a–4f, 5a–5b) never executed under the stale freeze.
   The amendment was epistemically right (v1-P4's devin-first premise had
   been superseded by the operator the day before) — the defect was
   procedural: when the world changes mid-round, re-freeze; do not edit
   under the runners. A runner's job also does not end at "my start hash
   matched": re-hash before filing scoring inputs. Counter-examples in the
   same wave: `probe-r19-P4-devinleg.log` records
   `battery_sha256_at_start: e3f08a09…` with first request 07:56:39Z — a
   minute *after* the v2 re-freeze — and no verify receipt; the glm run
   log's header likewise cites the v1 line while its first request
   (07:56:26.388Z) postdates v2. Post-re-freeze, every in-flight runner
   must re-verify against the new FROZEN line and record it.

5. **Breach records are artifacts too, and this one misstated the
   exposure.** plan §7.1 (`plans/probe-battery-r19.md:438-441`): "no runner
   executions between the stale freeze and the re-freeze …
   probe-r19-shim-ds-run.log contains header lines only" — contradicted by
   the landed logs: six files carry `first_request_utc` 07:52:25–07:53:40Z
   (inside the 07:52:04→07:55:58Z window), and shim-ds-run.log's
   executions (07:52:48–07:53:29Z) were on disk (mtime 07:54:31Z) before
   the §7.1 text's own "as of 07:56:30Z" check. The two accounts of when
   the re-base bytes landed also disagree (BR-1: "through 07:52:08Z";
   quota23's matching v1 hash at 07:52:5xZ implies pre-rebase bytes still,
   with the 387→429 write observable at ~07:54:27Z). Lesson: the ordering
   audit's verdict must be derived from the logs' own timestamps and file
   mtimes at close — the scorer's §7.1 job — never asserted from a spot
   check; a wrong exposure claim would have laundered out-of-freeze runs
   into the aggregate.

6. **A shared lane meters its own probe: the wave's routing bucket 429'd
   the battery.** P6 (zai glm-5.3-flash, this wave's own bucket) drew 429
   `{"code":"1302","message":"Rate limit reached for requests"}` at
   07:52:25Z with **no retry-after header**; the glm seat's read-only
   journal recon the same morning showed leg-1 zai at a 35.6% serve rate
   under 429 pressure (302 OK / 547 FAIL). [INFERENCE] the wave's own
   control-plane traffic competes with its probes on the shared bucket.
   Two subordinate points: (a) meter-state priors should be grounded in
   the journal, not in one prior draw — the glm seat filed p=0.45
   leg-identity from the 35.6% base rate, and measurement-grounded priors
   are exactly what a calibration battery exists to reward; (b) 429
   classes differ — token-plan meter-death carries `retry-after` +
   `insufficient_quota` (P1's implied resets landed −1 s from the r18
   anchors: 2026-10-23T15:59:59Z / 2026-10-28T15:59:59Z), zai's rate limit
   carries neither. A "429 prediction" that hits may still miss the
   mechanism; class the response before scoring the mechanism.

7. **Seat-level batteries extended the contract cleanly where the battery
   had no coverage.** Three seats with targets outside the battery budget
   (shim-ds :8791 S1–S8; devin :8787 D1–D5; glm conditional G1–G8) filed
   hashed predictions before any request, spent ≤3 live requests each,
   self-scored with Brier terms, and produced corroborated findings: devin
   non-stream `temperature:0` → 400 `devin_shim_error invalid_argument`
   (M10's opus isolation now seen on swe-2 and independently corroborated
   on glm-5-3-flash-max by a second seat's single request), and the
   cascade failover performing as the code read predicted (leg-1 zai 429 →
   leg-2 devin serve with the model rewrite). "GET /models 200" now has
   both directions evidenced: not sufficient (token-plan keys 2/3: listing
   200, chat 429) and not necessary (devin shim's static list omits a
   serving id). The two-clock pattern is priced in TEMPLATE §10; it worked.

Named defects left for the scorer/critic (recorded, not patched here):
- plan §7.1 exposure claim — `plans/probe-battery-r19.md:438-441`.
- P4-devinleg's stale-hash header with no verify receipt (lesson 4).
- TEMPLATE §5 still carries the unbracketed sed and cites the stale
  `e3f08a09…` as its "verified working" example (lesson 2) — owner:
  template-author, next revision.
- P1 appears executed by two seats (`probe-r19-p1-listing-mismatch.log`,
  `probe-r19-quota23.log`) — budget reconciliation is the scorer's.
- Scorer's close-out pending at write time; aggregate read belongs to
  `corpus/knowledge/probe-battery-r19.md`.
