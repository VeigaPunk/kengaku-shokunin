# RevF8 — re-check of W3ReviewKengaku F8 (capability rows are re-demonstrations) at lane tip 3f371d2

Axes: calibration (primary — the rows are SCORECARD-vs-repo state), novelty (same rows gate C1's separability). Read-only; base verified `3f371d2a` tip, `6180e4fb` base.

## Disposition of F8 (kaika-w3/kengaku-review.md:139)

**PARTIALLY FIXED.**
- Labeling prong — **fixed** at `94da19e` (no later commit touches it; `git log -S 're-demonstrated'` → `94da19e` only): `SCORECARD.md:555` "10 (re-demonstrated 24)", `:556` "21 (instrument `0d23c61`; re-demonstrated 24)"; Amendment 7 (`plans/round-24-claims.md:131-134`) declared rows enter only for capabilities run in round 24. The "C2.capability_rows 0→3 measures table filling" point was conceded by the lane itself (`LOG.md:258-262` verdict line records the critic dissent; score held 8→8), and r25 separates it: C2's P2a (`round-25-claims.md:76-77`) counts the table as *assertions*, not as an axis measure. No further action.
- Registry-accuracy prong — **OPEN, and worse than F8 stated**: row 3's evidence cell is stale at tip.

## F8' (new, same rows) — `sources-registry` evidence cell and receipt-of-record are stale at tip

Root cause chain: the row landed at `94da19e` (cell then true: 25 rows), then `e21f9ea` appended S026 (`corpus/SOURCES.md:48`; `gate.md:34`) per the F4 fix — no dependent count was refreshed. The integrator's own adjudication already states "capability `sources-registry` (26 rows, census ok)" (`corpus/lessons/round-24-verifier-spotcheck.md:17`), so the lane was told and did not correct.

Re-derived fresh (archive `git archive 6180e4f | tar -x -C /tmp/k25-f8`):
- `awk` census → **rows 26, tiers A=24 C=2, statuses mined=18 queued=5 rejected=3** (commands verbatim `gate.md:42-83`).
- `TZ=UTC bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate /tmp/k25-f8` → `k25-f8 ok`, exit 0 — registry itself is clean; the defect is cell-vs-registry drift, not registry validity.
- Rows 1–2 reproduce exactly: `python3 grader.py` → `CHECKS n=733 mismatches=0 errata_pinned=1` / `VERDICT: PASS` exit 0; `python3 plans/attrib_probe.py freeze-check --frozen plans/attrib-r23-frozen.md` → `block_sha=1b2d6a01bfa431ec pinned=1b2d6a01bfa431ec stable=True -> OK` exit 0; the Amendment-7 command `block-sha` → `1b2d6a01bfa431ec4e78bf89fd989f9ad500d10bb78634362a3c0e3bce794f87` (matches the pin).

Stale sites at tip (3 mismatches, independently confirmed by `.ufo/waves/round-25/build/CapRowsScout.md` 8/11 on row 3):
1. `SCORECARD.md:557` — "rows 25", "`A=24 C=1`", "rejected=2" vs true 26 / C=2 / 3.
2. `corpus/evidence/round24-sources/gate.md:93-101` — "Final census re-run at round-24 close … receipt of record" prints 25 / A=24 C=1 / rejected=2; the round-24 close/admitted tree is `e21f9ea`, which has 26 rows. The block is a true receipt for `94da19e` (cf. `06872d4`) but is mislabeled "of record".
3. `corpus/evidence/round24-census/after.txt:29-32` — same stale block (correct as a `94da19e` receipt; mislabeled only if cited as tip state).

C2 impact: P2a frozen at base will (correctly) fire 3 mismatches on row 3 — this is the undisclosed-defect firing CritC2Calibration F2 asks for; it must not be pre-neutralized by choosing lenient tokens.

## Smallest append-only fix (no history rewrite)

1. Append one errata row in SCORECARD's round-24 section, D14 pattern (`SCORECARD.md:618-620`): "D15 errata (round 25). `SCORECARD.md:557` census counts `rows 25`, `A=24 C=1`, `rejected=2` reflect `94da19e`; S026 (`e21f9ea`) makes the admitted-tree census rows 26, A=24 C=2, mined=18 queued=5 rejected=3. Old cell stays as written; this row supersedes it." (SCORECARD is not in the append-only list — W3 review §2 — but the D14 errata pattern is the lane's own precedent and keeps P2a's supersession rule uniform.)
2. Log the old→new in `corpus/lessons/round-25.md` (recheck-cell logging precedent of `e21f9ea`), and add a fresh census receipt (new file under `corpus/evidence/round25-sources/`) running the six commands on the landed tree. Do NOT edit `gate.md`/`after.txt`.
3. Re-freeze P2a's expected tokens after the fix so the landed tree verifies; base mismatch count (3 on row 3) stays the firing datum.
4. Systemic (r24 outside-decision lesson): F8/F9 received no disposition row while F1–F5 did (`corpus/lessons/round-24.md:113-141` covers F1-F5-class fixes only; `git log -S 'F8'` in-lane → no disposition). Append a `## W3 review disposition` table (F1–F14 → fixed commit / open + owner) to `corpus/lessons/round-25.md` so outside findings can no longer rot silently.

## Residual risk

- `C2.capability_rows` census key (`plans/round24_census.sh:64`) remains a bare count; harmless now that r25 scores it as assertion re-derivation, but the r24 report table (`.ufo/reports/round-24/kengaku.md:125`) still presents it without the table-filling caveat — historical, no action.
- If the fix lands as an in-place cell edit instead of the errata row, P2a's frozen base tokens still fire (correct); only the supersession bookkeeping changes.

## Verification gaps

- I did not re-run the six census commands inside `gate.md`'s first (superseded) block against `94da19e` itself (the `06872d4` receipt already pins it); only the final block's staleness was tested.
- Whether the integrator's "census ok" in `round-24-verifier-spotcheck.md:17` included a validator run at `e21f9ea` is unverifiable from committed bytes (my validator run is on `6180e4f`).
- `plans/state_check.py` and `plans/attrib_calibration.py` do not exist yet at tip (`ls plans/` → neither); P2a/P2b token re-freeze is a prerequisite on their landing.

Installs: none (stdlib awk/git/sha256 only; no pacman, no uv, no network).

VERDICT: F8 partially fixed — relabeling prong closed at `94da19e`; the same rows still carry a stale `sources-registry` evidence cell and mislabeled receipt-of-record (true census at tip: 26 rows, A=24 C=2, rejected=3) — fix by one D14-pattern errata row + logged old→new + fresh receipt, never by rewriting receipts.
