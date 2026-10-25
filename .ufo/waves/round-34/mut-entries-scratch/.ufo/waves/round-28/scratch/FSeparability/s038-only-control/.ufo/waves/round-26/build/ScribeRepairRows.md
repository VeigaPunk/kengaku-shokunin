# ScribeRepairRows — R26-E1..E3 correction drafts (round 26, build wave)

Base: lane `e0037a8da268` (HEAD; `corpus/SOURCES.md` unchanged `f11bffb..e0037a8`). Drafts only; no lane file written.

## Re-derived values (observed this session)

- **E1** `python3 plans/attrib_calibration.py --selftest` → last line `selftest: 18 checks, 0 failed`, exit 0. Stored: `corpus/evidence/round25-calibration/attrib-calibration-selftest-v2.txt:19`. Superseded text: `SCORECARD.md:558` "`--selftest` 14 checks 0 failed". SKILL.md:557 already says 18.
- **E2** Reproduced: `state_check.py` (HEAD v2) run in a `6180e4f` checkout placed beside `PROTOCOL.md` (the script exits 2 `INPUT ERROR` without it; `plans/state_check.py` does not exist at `6180e4f`) → `assertions=241 match=228 mismatch=10 superseded=0 offline_unverifiable=3`, exit 1; the 10 MISMATCH lines are byte-identical to `corpus/evidence/round25-calibration/state-check-before-6180e4f-v2.txt`. The v1 receipt `state-check-before-6180e4f.txt:1` says `mismatch=11` over 242 — that is the superseded value. Superseded text: `SCORECARD.md:559` "base `6180e4f` `mismatch=11`".
- **E3** `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → `42` at `f11bffb` (`git show f11bffb:corpus/SOURCES.md` also 42); 42 unique ids, last `S042`. S038–S042 landed in `8239a56` (after `8ea41f9`, where the count was 37). Superseded text: `PROVINCE.md:119` "holds 37 after round 25".

## Draft 1 — SCORECARD.md, append at end of file (new block)

```
## Corrections recorded in round 26 — current-state assertions (appended; superseded lines stay as written)

Found by the round-26 repairs (`plans/round-26-claims.md` §0, R26-E1–E3) and re-derived 2026-10-21. Each line names what it supersedes.

- **R26-E1 (2026-10-21)** supersedes `P3a.capability.interval-reverdict` — the `interval-reverdict` cell (`SCORECARD.md:558`) says "`--selftest` 14 checks 0 failed"; now `python3 plans/attrib_calibration.py --selftest` → `selftest: 18 checks, 0 failed`, exit 0 (receipt `corpus/evidence/round25-calibration/attrib-calibration-selftest-v2.txt`, last line; SKILL.md registry row already says 18). Tokens: `selftest: 18 checks, 0 failed`.
- **R26-E2 (2026-10-21)** supersedes `P3a.capability.state-assertion-check` — the `state-assertion-check` cell (`SCORECARD.md:559`) says "base `6180e4f` `mismatch=11`"; now `python3 plans/state_check.py --summary` run in a `6180e4f` checkout beside `PROTOCOL.md` → `assertions=241 match=228 mismatch=10 superseded=0 offline_unverifiable=3`, exit 1 (receipt `corpus/evidence/round25-calibration/state-check-before-6180e4f-v2.txt`; the v1 receipt `state-check-before-6180e4f.txt` counted `mismatch=11` over 242 assertions and is superseded by v2 Amendment 2). Tokens: `mismatch=10`.
- **R26-E3 (2026-10-21)** supersedes `P3b.province.registry-count` — `PROVINCE.md:119` says the registry "holds 37 after round 25"; now `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → `42` at base `f11bffb` (ids S001–S042; S038–S042 landed in `8239a56`). Correction appended in PROVINCE.md. Tokens: `42`.
```

## Draft 2 — PROVINCE.md, insert as a new paragraph directly after `:119` (no existing line edited)

```
*Round-26 correction (appended 2026-10-21): the round-25 correction above says the registry "holds 37 after round 25". That is the count at the round-25 landing commit `8ea41f9`. The round-25 falsify-wave revision `8239a56` appended S038–S042 (Reiczigel et al. 2010; Lang & Reiczigel 2014; Angelopoulos et al. PPI; cigate 0.2.0 PyPI; Hanley & Lippman-Hand 1983), and the registry holds 42 at base `f11bffb` (`grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → 42; ids S001–S042). The 37 figure is superseded by this line, not rewritten.*
```

## Notes for the integrator

- Token format: the v2 `superseding_tokens` (`plans/state_check.py:192,406-416`) matches `^- \*\*R25-E\d+…` only; the v3 widening to `R2[5-9]-E` must also accept the `P3*` ids used above. The proposed ids (`P3a.capability.*`, `P3b.province.registry-count`) are not yet frozen in the instrument; confirm against the v3 enumeration before landing or the rows will be `MISMATCH`.
- P2a's rule (`state_check.py:430`) requires a correction's code spans to equal the observed census exactly; P3 correction tokens above are the full re-derived values, but the v3 matcher must be checked against them.
- E3 is in PROVINCE (not parsed by the SCORECARD-only regex); the SCORECARD E3 row is the parseable closure.
- Historical mentions of "14 checks" (`.ufo/waves/round-25/falsify/*.md`) and `37` in round-25 receipts are records, not current-state; left untouched (append-only).
- Lesson `corpus/lessons/round-25-verifier-spotcheck.md:101,156` already records E1; not edited here (R26-E4 owns `round-26.md` errata).

## Files and tools

- Written: this report only (`.ufo/waves/round-26/build/ScribeRepairRows.md`).
- Scratch (not lane): `/tmp/r26-scribe-base`, `/tmp/r26-scribe-fleet/`, `/tmp/r26-scribe-sel.txt`, `/tmp/r26-scribe-6180.txt` — removable.
- Installs: none (git read-only, python3 stdlib, coreutils).
- Lane git: read-only (`rev-parse`, `log`, `diff --stat`, `show`) only.

VERDICT: E1 (18 checks, 0 failed), E2 (mismatch=10 reproduced, identical lines to v2 receipt), E3 (42 at f11bffb) re-derived; drafts ready for integrator to append; P3 token-matching not yet verified against v3.
