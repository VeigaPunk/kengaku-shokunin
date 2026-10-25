# R32RevClaims — claim freeze discipline review (round 32)

Reviewer seat, 2026-10-25. Scope: `plans/round-32-claims.md` at freeze commit
`0d32691d` (claims, counters, controls). No seat edits; only read-only git and
counter runs.

## (a) Freeze commit exists and precedes any wave seat

- `git cat-file -t 0d32691d` → `commit`; subject "round-32: frozen claims,
  counters, freeze controls", authored 2026-10-25 09:40:16 -0300, on `master`
  (HEAD chain: `6084cd3` → `0d32691d` → `85a9695` → ... → `f20a109`).
- Freeze commit tree contains the claims file, the three counters, the expect
  file and the three control receipts (8 files, +758 lines).
- `git diff 0d32691d HEAD` touches only `.ufo/waves/round-32/gate-receipt.txt`
  (the Q20 freeze-gate receipt, 09:40:27); no claims/counter/control bytes
  changed since freeze.
- No round-32 wave report is committed: `git log --all -- .ufo/waves/round-32/build/`
  is empty; `git status` shows the whole wave build dir untracked. The only
  post-freeze commits touching `.ufo/waves/round-32/` add the gate receipt, not
  a wave report.
- Wave launch: `build-run.log` / `swarm-registry.json` mtime 09:41:08;
  earliest seat reports in `build/` 09:43–09:44 — all after the 09:40:16 freeze.
- Note (non-violating): four abandoned duplicate freeze commits
  (`75cd250`, `e7bdd2f`, `91754d9`, `0e03393`) sit off `f20a109` with an
  identical freeze tree but are not ancestors of `master`; the canonical freeze
  is `0d32691d`. Two empty commits (`2d6f5f5`, `b20c11e`) are harness artifacts.

## (b) Predicates: one sentence each, label- and behavior-matched to counters

| Claim | Predicate | Counter output lines | Match |
|---|---|---|---|
| C1 | one sentence | `adoption_check.py --expect …/adoption-expect.json --census` prints `entries=N indexed=N cited_rows=N rows_present=N rows_mined=N usedby_ok=N census=ok`, exit 0 iff all gates pass (incl. `opened=<access_date>`, no dup ids, exactly one non-trivial index row, census exit 0) | printed order/labels identical; semantics identical |
| C1 (2nd receipt) | — | `round32_c1_verify.py --lane .` prints `checks=6 defects=N`, exit 0 iff N=0 (V1–V6: entry at frozen path + `verified-at`, row identity URL host+path, three pinned revisions, index title, ≥40 lines/≥3000 bytes, control receipt pins `expect_sha256` + `exit=1`) | matches |
| C2 | one sentence | `round32_defects.py --lane .` prints `checks=7 defects=N`; FROZEN == R1–R7; exit 1 iff N>0 | matches |
| C3 | one sentence | `catalog_probe.py --diff --lane .` prints `probed=2026-10-25 hf=ok openrouter=ok hf_models=N or_models=M hf_schema_delta=X or_schema_delta=Y entry=…`, exit 0 iff both probes ok, no missing fields, entry has `verified-at: 2026-10-25`, S101/S102, receipt pointer | matches |

All three predicates in the claims file are single sentences. Live re-runs on
the current (pre-repair) tree reproduced the committed control outputs exactly
(see (d)), confirming counter↔predicate↔receipt agreement.

## (c) Kill rules reachable

- C1: a cited source whose quote cannot be located at the pinned revision is
  refused at the gate (`plans/sources_adopt.py --quote-file/--artifact`;
  `EXIT_QUOTE_TOO_LONG=6`, `EXIT_QUOTE_ABSENT=7`). If fewer than three cited
  rows survive, `adoption_check.py` prints `rows_present<3` and exits 1, and
  `round32_c1_verify.py` V2 defects on any missing identity — the honest stop
  (registry delta 0) is machine-expressible.
- C2: any unrepaired item prints as a `DEFECT Rn` line and forces exit 1 —
  the "open defect / C2 misses" outcome is reachable per check.
- C3: on fetch failure `catalog_probe.py` prints `hf=fail openrouter=fail`,
  zeroes counts and exits 1 — the claim cannot pass when either API is
  unreachable. Minor observation (not a violation): because one shared status
  variable drives both flags, a single unreachable API labels both sources
  `fail` and prints no counts from the reachable one, which is coarser than
  the kill rule's "reachable source still counts" wording; the pass/fail
  outcome is identical and honest.

## (d) Controls exist, committed at freeze, and show the before-states

All four control files are inside the freeze commit `0d32691d`:

| Control | Captured before-state | Live re-run (2026-10-25) |
|---|---|---|
| `control-nothing.txt` | `entries=0 … census=ok`, `exit=1`; pins `expect_sha256=…73be9f` | `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok`, exit 1 — identical |
| `defects-before.txt` | R1–R7 all DEFECT, `checks=7 defects=7`, `exit=1` | identical output, exit 1 |
| `catalogs-before.txt` | `probed=2026-10-25 hf=ok openrouter=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 entry=stale`, `exit=1` | identical output (incl. "HF missing fields: author, sha, lastModified, gated"), exit 1 |

Before-states confirmed: defects=7 (exit 1), entries=0 (exit 1), stale entry
(exit 1). `round32_c1_verify.py` V6 verifies the control receipt pins the
expect-file digest and records `exit=1`, so the controls cannot be swapped for
passing receipts post-hoc.

## Freeze violations

None found.

## Residual risk / verification gaps

- The (b) match was verified by reading the counter sources and re-running the
  counters on the pre-repair tree; the post-repair pass states cannot be
  exercised before the round lands.
- C3's kill-rule wording is finer than the implementation's single-status
  print (noted above; does not affect the frozen pass/fail contract).

VERDICT: freeze-clean
