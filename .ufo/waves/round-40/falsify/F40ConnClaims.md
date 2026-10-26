# F40ConnClaims — cross-document consistency, kengaku round 40 wave 2 (falsify)

Seat: F40ConnClaims (connector, leaf). Scope per dispatch: claims, both counters' docstrings, controls,
measure-final, lesson, SCORECARD/LOG round-40 text, README/PROVINCE/SKILL round-40 text, and the knowledge
entry/receipt/dry table those texts share numbers with — every shared number (21 mutants, 28 cases, 8/20,
111→114 rows, 46→47 files, killed counts, hashes).

Fixture: clean `--no-local` clone of the lane at `ec1005a2a28bc5cfdde7723374368ed4cc956eed` under
`/fast/scratch/hyaku/kengaku-r40/F40ConnClaims/lane` (toplevel verified), all reads from the clone, no lane
writes, no commits. All quoted line numbers are from that clone.

## Verdict in one line

3 drifts: the wave-2-context tip hash vs the recorded landing tip; the knowledge entry Requirement-map prose
"six tags on **four** instruction lines" (five are enumerated, frozen and corroborated); LOG's "17 (13 direct)"
parenthetical, corroborated nowhere. Every other shared number checks out.

---

## DRIFT 1 — the landing/measurement tip hash: wave-2 context says `ec1005a2…`, the lane's own records say `ec17216…`

**Both locations:**
- Wave-2 context (this dispatch; rendered from `.ufo/waves/round-40/make_falsify_spec.py:46` "measured at lane
  tip {TIP} (branch master)"): tip = `ec1005a2a28bc5cfdde7723374368ed4cc956eed`.
- `.ufo/waves/round-40/integrate/measure-final.txt:1` — `TIP ec17216844585d0fecde9f1d4c4be0b78a3bf76f`
  (again at :560–561 ledger-tip `REF AUDIT … rev=ec172168… state=match`, and :576 `tip ec172168…`).
- `SCORECARD.md:1453` — "landing `ec17216844585d0fecde9f1d4c4be0b78a3bf76f`".
- `LOG.md:1194` — "landing `ec172168`".

**Receipt:**
```
$ grep -rn "ec1005a2a28bc5cfdde7723374368ed4cc956eed" <clone>   # → no output
$ grep -rn "ec17216844585d0fecde9f1d4c4be0b78a3bf76f" <clone>   # → measure-final.txt ×4, SCORECARD.md:1453
$ git -C <clone> log --oneline -2
  ec1005a round-40: lesson, SCORECARD/LOG round-40 sections, landing measurement + census after, wave-1 reports/results (37/37), …
  ec17216 round-40: battery40 (7 modules, 21 tripwire mutants), C2 package (db-wal entry, S119-S121, README, PROVINCE, SKILL …)
$ git -C <clone> merge-base --is-ancestor ec17216844585d0fecde9f1d4c4be0b78a3bf76f HEAD   # → exit 0 (ancestor)
$ git -C <clone> diff --stat ec17216844585d0fecde9f1d4c4be0b78a3bf76f ec1005a2a28bc5cfdde7723374368ed4cc956eed | tail
  → 287 files changed: .ufo/waves/round-40/** (build reports, integrate/measure-final.txt, census-after.txt,
    make_falsify_spec.py), LOG.md, SCORECARD.md, corpus/lessons/round-40.md only
```

**Reading.** `ec1005a2` is the round-40 master tip and is the right checkout for this wave; it is also the commit
that *contains* measure-final.txt. But the measurement inside it was executed one commit earlier, at `ec17216`,
and the lane's own records (measure-final TIP line, SCORECARD "landing", LOG "landing") all say `ec17216`.
`ec1005a2` appears in zero lane documents. The delta `ec17216..ec1005a2` touches no measured artifact — no
`plans/`, no `corpus/knowledge/`, no `corpus/SOURCES.md`, no README/PROVINCE/SKILL — so every instrument the
counters read is byte-identical at both commits and every counter would re-run identically (the frozen digests
all verify at the tip, see Consistency receipts). This is the same class the round-39 connector recorded
(SCORECARD.md:1447–1448, "cross-document drift 1 (the wave-2 context's tip hash vs the measured tip,
`F39ConnClaims`)"). Drift is in the hash string, not in any measured result.

## DRIFT 2 — knowledge entry Requirement-map prose: "six tags on four instruction lines"; five lines are enumerated, frozen, and corroborated

**Both locations:**
- `corpus/knowledge/tb2-db-wal-recovery-grader.md` `## Requirement map` — "The frozen table carries six tags on
  **four** instruction lines (`:7`, `:8`, `:9`, `:12`, `:13`)" — the parenthetical names **five** distinct lines.
- Same paragraph's own table: rows at `:7`, `:8`, `:9`, `:12`, `:13`, `:13` — six tags, five distinct lines
  (`:13` hosts `sorted-by-id` and `eleven-records`).
- `corpus/evidence/round40/db-wal-dry-cases-freeze.txt:1-6` — six `TAG` lines on five distinct instruction
  lines (`sorted-by-id` and `eleven-records` both `instruction.md:13`).
- `SKILL.md` §"Database-recovery TB2 grader — round 40" — enumerates the same six tags with lines
  `:7, :8, :9, :12, :13, :13`.

**Receipt:**
```
$ sed -n '1,6p' corpus/evidence/round40/db-wal-dry-cases-freeze.txt
  TAG fix-wal instruction.md:7 / TAG extract-all instruction.md:8 / TAG json-at-path instruction.md:9
  TAG record-format instruction.md:12 / TAG sorted-by-id instruction.md:13 / TAG eleven-records instruction.md:13
$ sed -n '121,135p' corpus/knowledge/tb2-db-wal-recovery-grader.md   # table rows :7,:8,:9,:12,:13,:13
```

Same paragraph then says "Three lines are enforced and three are not." The table's labels are a **tag** count
(3 enforced tags `json-at-path`/`sorted-by-id`/`eleven-records`, 3 `partly` tags); read as instruction lines it
is 2 enforced lines (`:9`, `:13`) vs 3 partly lines (`:7`, `:8`, `:12`). The derived labels themselves are
correct — recomputed from the receipt (`fix-wal` 23 violating/5 pass → partly; `extract-all` 15/4 → partly;
`json-at-path` 5/0 → enforced; `record-format` 8/2 → partly; `sorted-by-id` 1/0 → enforced; `eleven-records`
10/0 → enforced), matching SKILL's V7 paragraph and the counter's V7 (`rows=6 tags=6`, measure-final.txt). The
defect is the prose count "four" (should be five) and the loose "Three lines" phrasing.

## DRIFT 3 — LOG round-40 C1 bullet: "Advertised count 17 (13 direct) → 0"; the "(13 direct)" split is corroborated nowhere

**Both locations:**
- `LOG.md:1203` — "Advertised count 17 (13 direct) → 0."
- `.ufo/waves/round-39/build/R39PlanNext.md:143-146` (the cited source, §2.7) — "all 17 unkilled by tip and
  standing detectors: anchor (10) …; `ledger_tip` (7) …" — no "direct" split; 17 = 10 + 7.
- `plans/round-40-claims.md` C1 — the 17 "minus `L08` … plus one mutant per round-39 R5 clause (`A27`, `L21`)
  plus the order-gate mutants whose witnesses exist (`O04`, `O12`, `O14`)" → 21; directions "14 by `R39PlanNext`'s
  harness runs … 7 by this freeze's witness run".
- `.ufo/waves/round-40/claims/witness-run.txt` tail — `MUTANTS total=21 killed=7 survived=14` (the 7 =
  A27, L01, L11, L21, O04, O12, O14).

The only "13" figures in R39PlanNext are "4 of 13" order mutants (:23, :117-129) and "13 ledger fixtures" (:61) —
neither decomposes the 17. The witness split the claims record is 14 + 7, not 13 + 4. The parenthetical
contradicts no arithmetic (the 17 and the →0 are right), but as written it is an unsupported number in a shared
count. Cosmetic-to-minor; flagged so the L1 can fix or source it.

---

## Consistency receipts (numbers checked, found consistent)

- **21 mutants (anchor 11, ledger 7, order 3).** C1 counter `MUTANTS` table = 21 entries (A01,A02,A03,A06,A08,
  A09,A15,A17,A21,A22,A27 / L01,L05,L06,L11,L14,L15,L21 / O04,O12,O14), `TOTAL = 21` (`plans/round40_c1_verify.py:225`);
  measure-final `MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0`; claims "Total **21** (anchor 11,
  ledger 7, order 3)"; SCORECARD.md:1460,1472; LOG.md:1197; SKILL.md:592,625-627. O13 recorded as equivalent in the
  counter docstring (`plans/round40_c1_verify.py:64-67`), claims, and LOG.md:1198 — all agree.
- **Battery 7 modules / 21 fixtures.** `ls plans/battery40/*.py` = 7 (a_tok, a_row, a_bind, a_man, l_rows,
  l_refuse, o_gate); measure-final `BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0`; the 21 fixture fids in
  measure-final match the dispatch list (a_tok A01-A03 … o_gate O04/O12/O14); LOG.md:1199 "seven wave-1 executors …
  (21 fixtures)".
- **Controls.** control-c1-nothing: `fixtures=0 … total=21 killed=0 survived=21 … PREDICATE C1 fail exit=1`
  (claims, lesson ✓). control-c1-tool-edited: `PINS total=3 mismatched=1`, 11 anchor mutants `invalid` (claims,
  lesson ✓). control-c1-hostile-daemon: `fixtures=1 tampered=0`, `killed=0`, `COUNTERFACTUAL no-pid-namespace
  build: SOURCES.md changed after 6 s = True` (claims "3 s later" = the daemon's delay; lesson's "changed after
  6 s = True" ✓). control-c2-nothing: `checks=7 defects=4` with V2/V3/V4/V7 DEFECT (claims, lesson, SKILL.md:593,
  SCORECARD.md:1461 ✓); its `P8 … index_rows=46 knowledge_files=46` is the correct before-state for 46→47.
- **C2 28 cases / 8-20 / regrade.** Receipt `corpus/evidence/round40/db-wal-probe.txt:34-35`
  `regrade cases=28 differ=0` / `cases=28 observed_pass=8 observed_fail=20 mismatches=0`; dry table
  `predicted=pass` 8 + `predicted=fail` 20 = 28 CASE lines; identical in claims, measure-final (V4 `cases=28`,
  probe summary, P10), lesson header, SCORECARD.md:1461,1473, LOG.md:1204, README.md:267,498, PROVINCE.md:422-424,
  SKILL.md:967, entry:25. `first-run.txt`: "run1 rc=0, run2 rc=0, cmp run1 run2: byte-equal". Receipt is 8257 bytes
  = measure-final `P10 … bytes=8257` = tip_receipts `equal bytes=8257` = `first-run/run2.txt` 8257 bytes.
- **7 checks V1-V7, no check added/relaxed.** C2 counter docstring; measure-final `checks=7 defects=0 /
  PREDICATE C2 pass` (round-40 counter); V7 `rows=6 tags=6`. Tag stats recomputed from the receipt equal SKILL's
  V7 paragraph and the entry table (23/5, 15/4, 5/0, 8/2, 1/0, 10/0 → partly, partly, enforced, partly, enforced,
  enforced).
- **8 captures.** Claims "8 files + SHA256SUMS"; C2 counter `CAPTURES` = 8 entries whose digests match
  `corpus/evidence/round40/tb2-db-wal-recovery/SHA256SUMS`, SOURCES S119 `88dc5c2a…` and S120 `5a203751…`;
  measure-final `V1 ok listed=8 bad=0 extra=0`; README.md:497 ("the eight pinned db-wal-recovery files"); LOG.md:1193.
- **111→114 rows, 46→47 files.** `grep -c "^| S[0-9]" corpus/SOURCES.md` = 114; `ls corpus/knowledge/*.md` = 47;
  README knowledge index rows = 47; lesson Census "111 → 114 … 46 → 47 … 46 → 47"; SCORECARD.md:1461 "SOURCES
  111→114; knowledge files/index rows 46→47"; measure-final last line `registry_rows=114 knowledge_files=47
  index_rows=47`; anchor check `rows=114 tokens=21 defects=0`.
- **Hashes.** Freeze `bbb109505670192035ef63d7c8b37733e99fa1a3` = freeze commit (`git rev-parse bbb1095`) — matches
  assignment, lesson, SCORECARD.md:1452, LOG.md:1192, measure-final ORDER line. First probe run
  `055748f78a3335434f2a4070bb3fb1cf8d0eba1f` = first-run commit — matches assignment, lesson, SCORECARD.md:1453,
  LOG.md:1194, measure-final `receipt_commit`. Tool pin prefixes 11bb2cad…/853bcb2a…/948d5e1d… (claims) =
  frozen-digests full digests; `sha256sum -c .ufo/waves/round-40/claims/frozen-digests.txt` → all 11 OK at the tip;
  C2 counter `SPEC_SHA256 4af78f4f…` = frozen-digests = actual `plans/pkg-spec-r40.json`.
- **Census.** `census-before.txt` and `census-after.txt` both carry exactly 15 W04 lines and `kengaku ok …
  SOURCES.md` / `exit=0`; measure-final census lists the same 15 W04 then `file ok`; lesson "15 W04".
- **No-harm.** SCORECARD.md:1463-1466 vs measure-final: round-37 C1 `total=55 killed=55`; round-38 C1
  `total=22 killed=21 survived=1` (SCORECARD's "killed=21 survived=1"); round-39 C1 `total=7 killed=7`; all C2s
  `checks=7 defects=0`; order_check round 38 `ORDER RESULT FAIL exit=1`, rounds 39/40 PASS; ledger_tip
  `rows=9 closed=9 observed_pass=9 mismatches=0`.
- **Witnesses / pilot.** claims "14 by R39PlanNext's harness runs … 7 by this freeze's witness run"; witness-run
  `killed=7 survived=14` with A27, L01, L11, L21, O04, O12, O14 killed; R39PlanNext §2.7 lists the 17
  (anchor 10 + ledger 7) and +4 order mutants (O04, O12, O13, O14) and the two R5 clauses — the O13 withdrawal
  reconciles 17−L08+A27+L21+3 = 21. Probe docstring names exactly 7 pilot cases (`untouched`, `oracle-solve-sh`,
  `base-only-ro`, `literals-never-open-db`, `literals-names-1-2-wrong`, `literals-id3-name-wrong`,
  `truth-value-float-id1`) matching claims "Seven of the 28".
- **Receipt line citations.** Every `receipt:N` cited in SKILL.md §"Database-recovery TB2 grader" and PROVINCE.md
  was verified against `corpus/evidence/round40/db-wal-probe.txt` (e.g. `:7 untouched`, `:8 oracle-solve-sh`,
  `:14 decrypt-in-place-no-json FFFFFFF`, `:35` summary, `:34` regrade) — all correct.
- **S119/S120/S121.** S119 quote at `test_outputs.py:98` verbatim in the capture, 12 words; S120 quote at
  `instruction.md:7` verbatim, 9 words; S121 21-word quote, "state open, merged false at 2026-10-26 14:04 -03"
  identical in lesson Gate table and SOURCES.md row. "6 of 89 TB2 graders" consistent (README, entry, SCORECARD);
  "22 of the 33 id/name/value cells pinned" consistent (README, PROVINCE, LOG, SKILL decision table).

VERDICT: drift-3
