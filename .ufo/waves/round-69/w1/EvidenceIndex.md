# Round 69 w1 — evidence index (one row per artifact a closure must resolve)

**Seat:** EvidenceIndex (scribe, leaf). **Wave:** kengaku-r69-w1 (14 dispatch entries, 13
build+attack seats + this index). **Written:** 2026-11-03, live snapshot at
`2026-11-03T21:10:32-03:00` (re-snapshot commands in §S; live state moves under a running wave).
A **post-snapshot drift** block (§G, `2026-11-03T21:14:58-03:00`) records landings that occurred
while this file was being written; §A–§F describe the 21:10:32 snapshot only.

**All paths below are lane-root-relative.** Lane root
`L = /home/vgpnk/Projects/shokunin/kengaku-shokunin`. Wave root
`W = L/.ufo/waves/round-69/w1`. Scratch roots are `/fast/scratch/hyaku/kengaku-r69/<seat>/`
and must be deleted by their seat before it yields.

**Two revisions matter and are not the same.**

- `a518980e` — the claims' freeze base ("the lane tree is clean at freeze base a518980e",
  `plans/round-69-claims.md` preamble). The do-nothing controls are anchored here.
- `b288e8e0` — the freeze commit (HEAD at index time): adds `plans/round69_c1_nginx_probe.py`,
  `plans/round69_c2_routed_defects.py`, this round's claims doc and the wave spec/dispatch, plus
  `.ufo/waves/round-69/{c2-red-before,nginx-control,census-before}.txt`.

**Status legend (every cell is a command result, never an impression).**

- `0` / `1` / `n` — `grep -c` (or listed count) over the committed bytes of that revision
  (`git show <rev>:<file> | grep -c …`, §S2).
- `absent` / `present` — `git cat-file -e <rev>:<path>` exit status (§S1).
- **live** — working-tree observation at the snapshot timestamp above; re-run §S1/§S2 to refresh.
  A live `present` is not a verdict: the artifact's own verdict line still has to be read.
- **`[INFERENCE]`** — a consequence derived from two observed facts but not itself executed by
  this seat. Everything not marked `[INFERENCE]` was observed by a command quoted in this file or
  in the cited seat report.

---

## A. Frozen inputs and controls (present at the freeze commit; use them, do not edit them)

| # | Path | What it is | Verdict-bearing content / digest | Re-derive | a518980e | b288e8e0 | live |
|---|---|---|---|---|---|---|---|
| A1 | `plans/round-69-claims.md` | the two frozen claims, case table, kill rules | sha256 `0088cfb0034897ccf3e57e4dd86a532d5ca0882249d40bc033a1fe7786a53a41`; `FROZEN-VECTOR PPPPPPPP/PPFPPPPP/PPPPPPFF/PPPPPFPP/FPPPFPPP` (line 35); close-out list at lines 129–131 | `sha256sum plans/round-69-claims.md`; `git log --oneline -1 -- plans/round-69-claims.md` → `b288e8e0 round-69 freeze: …` | absent | present | present (unmodified: `git status --porcelain` shows no entry) |
| A2 | `plans/round69_c1_nginx_probe.py` | C1 instrument (battery, checker, selftest, renderer) | sha256 `66b5128dffbb1637b710f9a5d6fb8cacbe7639d89218dfa4b5010539070100ea` — equal to the receipt's `PROBE` line and the control's `FROZEN-SHA` line | `sha256sum plans/round69_c1_nginx_probe.py` | absent | present | present, digest equal |
| A3 | `plans/round69_c2_routed_defects.py` | C2 gate E1–E7 + selftest | sha256 `ea28b006d528a99befdc193c5463ef552b0a15d0b71b03a091ec011fae115485` | `sha256sum plans/round69_c2_routed_defects.py` | absent | present | present, digest equal |
| A4 | `.ufo/waves/round-69/c2-red-before.txt` | C2 do-nothing measurement | seven `E<n> defect …` lines (`E1 defect rows=0/4 missing=[…four names…] thin=[]`, `E2 defect headings=0 q50=False round68-lesson=False spotcheck=False`, `E3 defect … missing`, `E4 defect verified-at-lines=1 last-names-landing=False`, `E5 defect strict-lines=0`, `E6 defect rerecord-lines=0`, `E7 defect problems=['corpus/evidence/round69/gates/depth-gate.txt:missing', 'corpus/evidence/round69/gates/trio.txt:missing']`), then `DEFECTS n=7`, `PREDICATE R69-C2 fail`, `rc=1` | §S9 (extract `b288e8e0` to scratch, run the gate there, `diff -u` against this file) | absent | present | present; read in full — the seven defect lines, `DEFECTS n=7`, fail, `rc=1` |
| A5 | `.ufo/waves/round-69/nginx-control.txt` | C1 do-nothing control | contains `$ git cat-file -e a518980e:corpus/evidence/round69/nginx/receipt.txt` → `rc=128`; `grep -c 'executed 3 of 8' SKILL.md` → `0`; `--check-receipt …` → `SETUP receipt-missing`, `rc=2`; the five-line render block, `FROZEN-VECTOR …`, `LEGS 8`, three `FROZEN-SHA` lines | `git show b288e8e0:.ufo/waves/round-69/nginx-control.txt` | absent | present | present |
| A6 | `.ufo/waves/round-69/census-before.txt` | census baseline | 24 `kengaku W04 …` lines + `kengaku ok …/corpus/SOURCES.md` + `rc=0` (25 lines) | §S13; count `grep -c $'\tW04\t'` → 24 | absent | present | present; closing run must reproduce it (§F9) |
| A7 | `corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py` | the replayed TB2 grader | sha256 `045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0`; eight `def test_…` in this file order: installed (:11), running (:17), index_page_content (:33), custom_404_page (:46), config_syntax (:59), config_settings (:67), log_file_creation (:123), log_file_format (:144) | `sha256sum …test_outputs.py` | present | present | present |
| A8 | `corpus/evidence/round52/graders/SHA256SUMS` | digest registry | line 111 is `045cc716…  ./nginx-request-logging/tests/test_outputs.py` | `sed -n '111p' corpus/evidence/round52/graders/SHA256SUMS` | present | present | present |

---

## B. R69-C1 artifacts (coverage: the grader replayed offline)

Predicate sentence (`plans/round-69-claims.md:10–13`): five cases × eight frozen legs, **every
leg `P` in ≥1 case and `F` in ≥1 case**, PROBE and GRADER sha256 equal the committed bytes,
checker prints `PREDICATE R69-C1 pass` and exits 0. Kill rule: any vector mismatch, any leg with
no `P`/no `F`, any `SETUP` path, any nonempty `--check-receipt` defect list.

| # | Path | Owner seat | Must contain (verdict line / required bytes) | Re-derive | a518980e | b288e8e0 | live |
|---|---|---|---|---|---|---|---|
| B1 | `corpus/evidence/round69/nginx/receipt.txt` | NginxBattery per claims' *Measuring command* | the receipt of record as the claims name it: `PROBE … sha256 66b5128d…`, `GRADER … sha256 045cc716… pin 2fd12b88aafd…`, 5 `CASE K<n> case_sha256=… server_pid=… sandbox_rc=0`, 40 `TEST`, 5 `VECTOR … agree=True`, `LEG-COVERAGE legs=8 seen_p=8 seen_f=8`, `SUMMARY cases=5 legs=40 mismatches=0 setup=0`, `PREDICATE R69-C1 pass`; checker then prints `CHECK ok cases=5 legs=8 seen_p=8 seen_f=8` + `PREDICATE R69-C1 pass`, rc 0 | §S15 checker; §S3 leg tally; §S6/§S7 digests | **absent** (`cat-file` rc 128 — the control's own line) | absent | **absent** |
| B2 | `.ufo/waves/round-69/w1/nginx/receipt.txt` | NginxBattery (dispatch argv names this path) | same line set as B1; observed instead: `LEG-COVERAGE legs=8 seen_p=8 seen_f=6`, `SUMMARY cases=5 legs=40 mismatches=0 setup=0`, `PREDICATE R69-C1 fail` (file sha256 `44dd4eb185872e8acee13b48d80fc5e2fa476f91dccb38e9d8321eac749a2263`, 2647 B) | same as B1 with this path | absent | absent | **present**; verdict is a failure, see §F1 |
| B3 | `corpus/evidence/round69/nginx/sandbox/K{1..5}-sandbox.txt` | NginxBattery per claims' command (`--evidence-dir`) | five captures; each begins `rc=0 server_pid=<pid>` then `--- stdout` with eight `TEST <leg> P\|F <ms>` lines and `--- stderr` (limitation (i): these are the live witness the checker cannot read) | `ls corpus/evidence/round69/nginx/sandbox` → 5; `head -1` each | absent | absent | **absent** (directory does not exist) |
| B4 | `.ufo/waves/round-69/w1/nginx/sandbox/K{1..5}-sandbox.txt` | NginxBattery (dispatch argv) | as B3; observed 5 files, each `rc=0 server_pid=<pid>` with 8 `TEST` lines: K1 1256831, K2 1262306, K3 1266496, K4 1270481, K5 1277524 — every pid equal to the same case's `server_pid=` in B2 (live cross-check, not a verdict) | `ls .ufo/waves/round-69/w1/nginx/sandbox \| wc -l`; `head -1` each; `grep '^CASE '` B2 | absent | absent | **present (5)** |
| B5 | `SKILL.md` class row (`:78`, `network-service`, `executed 2 of 8`) | landing (L1) | one occurrence of `executed 3 of 8` | `grep -c 'executed 3 of 8' SKILL.md` → 1; `grep -c 'executed 2 of 8' SKILL.md` → 0 | 3of8=**0**, 2of8=1 | 3of8=**0**, 2of8=1 | 3of8=**0**, 2of8=1 (row still reads `executed 2 of 8` — the pending edit) |
| B6 | `corpus/SOURCES.md` row `S241` | landing (L1), row text from SourceOpen | one 11-column data row (`id \| source \| kind \| tier \| scope \| anchor \| teaches \| status \| opened \| recheck \| used-by`): id `S241`, grader URL at pin `2fd12b88`, kind `code`, tier `A`, scope `network-service grader offline execution (R69-C1)`, opened `2026-11-03`, recheck `180d`, status `mined`, `used-by` resolvable (landed row cites the new `corpus/knowledge/tb2-nginx-request-logging-offline.md`; the SourceOpen item proposed the older `tb2-network-service-offline-grader.md` — §G), anchor = sha256 + ≤25-word located quote with line number, **no literal `\|` inside a cell**; census must stay exit 0 with 24 W04 | `grep -cE '^\|[[:space:]]*S241[[:space:]]*\|' corpus/SOURCES.md` → 1; §S13 | **0** | **0** | **1** at `corpus/SOURCES.md:256` (§G) |
| B7 | `corpus/knowledge/tb2-network-service-offline-grader.md` — nginx section citing S241 | **unassigned at freeze** (no seat item names it; §F6) | a knowledge entry citing `S241` (claims line 52 calls S241 "cited by the knowledge entry's nginx section"); post-snapshot the landing put it in a **new** file, `corpus/knowledge/tb2-nginx-request-logging-offline.md` (§G) | `grep -n 'S241' corpus/knowledge/tb2-nginx-request-logging-offline.md` → ≥1 (§G); `grep -c '^## .*nginx' corpus/knowledge/tb2-network-service-offline-grader.md` | **0** mentions | **0** | **0** at snapshot; **new entry cites S241 twice post-snapshot (§G)** |
| B8 | C1 selftest tally (required at close, `claims:129–130`; **no frozen path**) | ReceiptReverify / landing | with a green receipt: `SELFTEST red_refused=5/5 green_ok=1 ok=True`, rc 0. Live attempt printed `SETUP work-dir-required (not a directory)`, rc 2 (`.ufo/waves/round-69/w1/ReceiptReverify/selftest-nginxbattery.txt`) | §S15 | n/a | n/a | **absent as a passing tally**; [INFERENCE] cannot reach `green_ok=1` while §F2 holds |

---

## C. R69-C2 artifacts (calibration: the seven routed defects, gate `E1`–`E7`)

Predicate (`plans/round-69-claims.md:74–77`): each of the seven defects in
`corpus/lessons/round-68-verifier-spotcheck.md` §5 (items 1–7) closed by a dated correction that
the gate re-derives as E1–E7; gate prints `DEFECTS n=0`, `PREDICATE R69-C2 pass`, rc 0. Kill
rule: any `E<n> defect` line fails; prose without a re-deriving check is not a closed defect.

| # | Path | Owner seat | Must contain (verdict line / required bytes) | Re-derive | a518980e | b288e8e0 | live |
|---|---|---|---|---|---|---|---|
| C1 | `corpus/evidence/round69/c2-receipts/provenance-erratum.txt` | ProvenanceRederive → landing copy (gate reads **this** path) | `TREE 27f649f8`, `LANDING 1ec2e60a`, six `INPUT <path> at-tree=<sha> at-landing=<sha>` lines, `DIFFERS SKILL.md` exactly (the only differing input) | §S8 (re-hash every input at both revisions); `git cat-file -e 27f649f8^{commit}`, `git cat-file -e 1ec2e60a^{commit}` | absent | absent | **present**, 1174 B, sha256 `fad393d0709067d0e5a95fd4e080db6e362a8fe75ec369de0796cfa868b25652` (6 INPUT, 1 DIFFERS) |
| C2 | `.ufo/waves/round-69/w1/provenance-erratum.txt` | ProvenanceRederive (dispatch path, draft) | same field set; observed identical to C1 except the `DIFFERS SKILL.md` line is last instead of before the sixth `INPUT` (sha256 `9261c8d73e939b7859746d8aae6a84b1611e21587cd2330202d14ba36341831c`) | `diff -u` against C1 | absent | absent | **present**; parser-equivalent (E3 compares sets), but the gate never reads this path |
| C3 | `corpus/evidence/round69/gates/depth-gate.txt` | GateReceipts → landing copy (E7 reads **this** path) | exactly the stdout of `python3 plans/round63_gate_checks.py depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt --root .`: `ROWS n=16 class_match=True count_mismatch=0 paths total=33 resolved=33 share=1.00`, `PREDICATE R63-C2 pass` | §S10 (fresh run + `diff -u`) | absent | absent | **present**, 104 B, sha256 `f683297c35998f66187475daf2f68333f62294fab9356d436cba459c02efc9d9` |
| C4 | `corpus/evidence/round69/gates/trio.txt` | GateReceipts → landing copy | exactly the stdout of `python3 plans/round63_gate_checks.py trio corpus/knowledge/tb2-network-service-offline-grader.md`: `TRIO pass corpus/knowledge/tb2-network-service-offline-grader.md` | §S10 | absent | absent | **present**, 65 B, sha256 `d877fe2fa696bf0cb45255fd159ef5fe92946f7d088237e282d92cd974922cb7` |
| C5 | `.ufo/waves/round-69/w1/gates/{depth-gate,trio}.txt` | GateReceipts (dispatch paths) | byte-identical to C3/C4 | `sha256sum` both pairs (`C3`/`C5`, `C4`/`C5`) | absent | absent | **present**; both pairs observed byte-identical (same shas as C3/C4) |
| C6 | `SKILL.md` `## Gate/probe registry` rows for `round68_c1_pypi_finish`, `round68_c2_correction_gate`, `round68_report_contract`, `round68_capability_table` | landing (L1), text from CorrectionDraft `drafts/registry-rows.md` | one row each, **8 cells**, cell 2 (index 2) containing `plans/round68_*.py` (file must exist), cell 3 containing both `` `0` `` and `` `1` ``, cell 4 non-empty (self-test spelling); plus semantics: pinned values and write scope | `grep -n 'round68_c1_pypi_finish' SKILL.md` (repeat per name: each must show one registry row); the gate's own E1 | **0,0,0,0** | **0,0,0,0** | **1,1,1,1** at `SKILL.md:690–693` |
| C7 | `corpus/QUALITY.md` `## Round69 criterion` (Q50) | landing (L1), text from `drafts/quality-q50.md` | exactly one heading `## Round69 criterion`; section contains `Q50`, `corpus/lessons/round-68.md`, `corpus/lessons/round-68-verifier-spotcheck.md`; criterion is "re-hash a report citation from committed bytes before writing it" | `grep -c '^## Round69 criterion' corpus/QUALITY.md` → 1; `sed -n` the section; gate E2 | **0** | **0** | **1** (`QUALITY.md:1207`) |
| C8 | `corpus/knowledge/tb2-network-service-offline-grader.md` second `verified-at:` line | landing (L1) | a second appended `verified-at:` line whose text names `1ec2e60a`; the first (`base c78749a5…`) stays unedited | `grep -n '^verified-at:' …` → exactly 2, last contains `1ec2e60a`; gate E4 | **1** | **1** | **2**, last = `verified-at: 2026-11-03 (round 69: the round-68 amendment tip is 1ec2e60a; …)` |
| C9 | `corpus/lessons/round-68.md` strict-attack-share correction | landing (L1), text from `drafts/lesson-corrections.md` | exactly one line carrying `strict attack share`, `3/12`, and all of `reviewer`, `critic`, `mutation-tester`, `labrat` | `grep -n 'strict attack share' corpus/lessons/round-68.md`; gate E5 | **0** | **0** | **1** (`## Corrections (round 69, dated; …)` section) |
| C10 | `corpus/lessons/round-68.md` `w1-results.json` re-record | landing (L1) | ≥1 line carrying `w1-results.json`, `output: ""`, and `per-seat` (points at the twelve per-seat reports) | `grep -n 'w1-results.json' corpus/lessons/round-68.md`; gate E6 | **0** | **0** | **1** |
| C11 | C2 green run (required at close, `claims:129–131`; **no frozen path**) | landing (L1) | `E1 ok …` … `E7 ok …` then `DEFECTS n=0`, `PREDICATE R69-C2 pass`, rc 0 | §S11 | n/a | n/a | **absent** (no green receipt under `corpus/evidence/round69/` or `W/` at snapshot) |
| C12 | C2 selftest tally (required at close; **no frozen path**) | GateMutate (tally) / landing | `SELFTEST defects-in-fake=7 want=7 all-fail=True` **and** `SELFTEST e7-stale-red=True rc=1`, rc 0 | §S12 | n/a | n/a | **absent** at snapshot |

---

## D. Close-out records the claims require (`plans/round-69-claims.md:129–131`)

| # | Path | What it must say | Re-derive | live |
|---|---|---|---|---|
| D1 | `LOG.md` — new `## Round 69 …` section | both predicates' before→after, the close-out list (C1 receipt, C1 selftest tally, C2 green, C2 selftest tally, census exit, depth/trio receipts, class-row count), wave seat count/roles, verdicts and L0 carried | `grep -n '^## Round 69' LOG.md` → 1 | **0** |
| D2 | `SCORECARD.md` — new `## Round 69 …` section (+ `### …` addendum if attempts split) | same claims table shape as `## Round 68` (`SCORECARD.md:2940`), plus the capability/class-row consequence of C1 | `grep -n '^## Round 69' SCORECARD.md` | **0** |
| D3 | `.ufo/waves/round-69/w1-results.json` | driver-written seat index; **its `output` fields are not the seat-output record** (round-68 lesson `## Corrections`; E6) — the output record is the 14 reports below | `ls .ufo/waves/round-69/w1-results.json`; `python3 -c "import json;print(len(json.load(open('….json')).get('members',{})))"` (schema check by eye) | **absent** |
| D4 | fleet report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-69/kengaku.md` | **outside this lane's write scope**; written by the driver/L1. Listed so a closure does not mistake it for a lane artifact. Round-68 attempt 1 was killed for missing `## SHONEN` / `## Trend verdicts` (`plans/round68_report_contract.py` gates the shape) | `python3 plans/round68_report_contract.py <report> --shonen SHONEN.md` (lane gate; run by whoever owns the report) | not checked (fleet repo, not mine to read for this index) |
| D5 | closing census exit (**no frozen path**; `claims:130`) | `exit-code: 0`, `W04-count: 24`, verdict line `kengaku ok …/corpus/SOURCES.md`, and no new W04 from S241 (F9) | §S13; compare the 25 lines with `census-before.txt` | **no closing run yet**; `W/CensusAudit/census.txt` is the start-of-wave run (`exit-code: 0`, `W04-count: 24`) |

---

## E. Wave evidence — one report per dispatched seat (`W/<Name>.md`)

Every seat report must carry, per its item: exact argv, the raw output lines that carry a
verdict, its conclusion, findings an attacker should use, and **every command it did not run**.
Scratch-only artifacts (forged receipts, mutants, base clones) are deleted before yield, so the
report must quote their path + bytes/digest + output; a closure cannot re-run them from the
report. Live at 21:10:32: 3 of 14 present (`CensusAudit.md`, `GateReceipts.md`, `NginxBattery.md`).

| Seat (role) | Report | Scratch-bound evidence the report must quote | Verdict line the report must carry |
|---|---|---|---|
| NginxBattery (executor) | `W/NginxBattery.md` | `W/NginxBattery/stdout.txt`, `check.txt`, the receipt B2, sandbox B4 | `VECTOR` ×5, `LEG-COVERAGE`, `SUMMARY`, `PREDICATE R69-C1`, rc, five server PIDs |
| ReceiptReverify (executor) | `W/ReceiptReverify.md` | `W/ReceiptReverify/battery.txt`; the item's `check.txt`/`selftest.txt` live as `check-nginxbattery.txt`/`selftest-nginxbattery.txt`; own `receipt2.txt` only if a run succeeded (live: the battery printed `SETUP port-8080-occupied`, rc 2) | `AGREE`/`DIFF` per case vs B2 and the frozen table; selftest tally; SETUP line if refused |
| ProvenanceRederive (executor) | `W/ProvenanceRederive.md` | C2 erratum draft + per-input commands | `TREE`/`LANDING`, 6 `INPUT` lines with both shas, the identical set and the one differing input |
| GateReceipts (executor) | `W/GateReceipts.md` | `W/gates/*.txt`, run1/run2 diffs | `ROWS n=16 class_match=True count_mismatch=0 paths total=33 resolved=33 share=1.00`, `PREDICATE R63-C2 pass`, `TRIO pass …`, both rcs, byte-equality table |
| LegPricing (reviewer) | `W/LegPricing.md` | grader source lines quoted | one line per leg: `LEG <n> <name> priced_by=<case> attributes=<PASS\|FINDING …>`; false-green windows named |
| ReceiptReview (reviewer) | `W/ReceiptReview.md` | five forged receipts (scratch, deleted) — quote sha256 + defect line each | clause table (implemented/partly/not) + `M-<letter>` findings with ACCEPTED/REFUSED |
| CensusAudit (reviewer) | `W/CensusAudit.md` | `W/CensusAudit/census.txt` | census exit 0, W04 count 24, data-row count, highest id, S241 free, last-row cell shapes/used-by resolution, class-row/lesson counts |
| ClaimFalsify (critic) | `W/ClaimFalsify.md` | freeze-order git outputs; forged receipt | `F1..Fn` with file:line/command output; per-case per-leg agreement derived independently; red-before honesty |
| GateMutate (mutation-tester) | `W/GateMutate.md` | `S/mutants/m<n>.py` (deleted) — quote each run's `DEFECTS n=` | `MUTANTS total=7 killed=<k> survived=<s>` + unmutated fixture `DEFECTS n=7` + `--selftest` tally |
| CorrectionDraft (scribe) | `W/CorrectionDraft.md` | `W/drafts/registry-rows.md`, `quality-q50.md`, `lesson-corrections.md` | exact correction text + ungroundable facts (draft-only; the checkable bytes are C6–C10) |
| SourceOpen (scout) | `W/SourceOpen.md` | curl status/bytes/sha; capture cmp; instruction.md (or 404) | live-fetch result vs `SHA256SUMS:111`; proposed 11-cell S241 row verbatim; column/cell parse check |
| SiblingOverlap (connector) | `W/SiblingOverlap.md` | grep -l/-n hits only | `TERM-LEVEL n`, `SURFACE-LEVEL n` + lane:file:line list; routed vs contested |
| HostsProbe (revenger) | `W/HostsProbe.md` | patched probe copy (scratch, deleted) — quote patch + outputs | arm A leg vector (leg 2 `P`, no NameResolutionError) vs arm B (`E:ConnectionError`/`NameResolutionError`), hypothesis holds/refuted |
| EvidenceIndex (scribe) | `W/EvidenceIndex.md` | this file | the checklist itself |

Drafts live at snapshot: 2 of 3 (`quality-q50.md`, `registry-rows.md`); `lesson-corrections.md`
absent. Draft absence is not a claim failure — C7/C9/C10 are the checkable bytes.

---

## F. Findings a claim's attacker or the closure must use

**F1 — R69-C1's frozen predicate is unreachable from the frozen case table (observed; blocks the
claim).** The table's vectors leave legs 2 (`test_nginx_running`) and 4 (`test_custom_404_page`)
with **zero** `F` witnesses (`P=5 F=0` each); `plans/round-69-claims.md:36–37` says "Each of the
eight legs has one red witness and four green witnesses by construction". The live receipt prints
`LEG-COVERAGE legs=8 seen_p=8 seen_f=6`, and the instrument's `ok` requires `full_f == 8`, so it
prints `PREDICATE R69-C1 fail`, rc 1. Per the kill rule this is an honest miss, not a re-scorable
run; the case table, vectors and kill rule are frozen and this seat did not edit them. Re-derive:
§S3 (from the receipt) and §S4 (from `CASES`). NginxBattery.md reports the same two legs at
lines 12–13 and 135–137.

**F2 — C1's checker and its own receipt writer disagree on `VECTOR` arity (observed; blocks the
checker clause).** The writer emits six whitespace tokens (`…probe.py:460`:
`VECTOR K1 PPPPPPPP expected PPPPPPPP agree=True`); `check_receipt` requires exactly five
(`…probe.py:513`). The authentic receipt is therefore refused with one `DEFECT vector-line` per
case, `case-set got=[]`, eight `leg-coverage` defects and `stored-predicate PREDICATE R69-C1 fail`
(`W/NginxBattery/check.txt`, `W/ReceiptReverify/check-nginxbattery.txt`). Consequence
[INFERENCE]: the selftest's five red fixtures write the same six-token form
(`…probe.py:602`), so all five are "refused" through `vector-line` regardless of the mutation they
encode, and a green receipt is refused too — the tally cannot reach `red_refused=5/5 green_ok=1
ok=True` while these bytes stand. A checker whose red arms fire for an unintended reason is a
vacuous selftest (this is what Q49 priced for round 66, one layer down).

**F3 — the C1 receipt-of-record path diverges between the claims and the dispatch (observed;
pointer risk).** Claims *Measuring command* writes
`corpus/evidence/round69/nginx/receipt.txt` and its `--evidence-dir corpus/evidence/round69/nginx/sandbox`;
the NginxBattery item's argv writes `W/nginx/receipt.txt` and `W/nginx/sandbox`. At snapshot the
corpus paths are **absent** and the wave paths present. `--check-receipt` is content-only, so either
file can be checked, but the claims' after-target (`claims:50`) names the corpus receipt. A closure
must cite which path it scored; it must not count the wave receipt as the claims' target.

**F4 — the provenance erratum exists twice with different bytes (observed; not an E3 defect).**
The wave draft (`9261c8d7…`) and the gate-read corpus copy (`fad393d0…`) differ only in the
position of `DIFFERS SKILL.md` (line 8 vs line 9); E3 builds a set, so both parse identically.
The gate reads `corpus/evidence/round69/c2-receipts/provenance-erratum.txt`. Re-derive the shas
with `sha256sum` and the content with `diff -u`.

**F5 — E7's receipts are already byte-identical across the two roots (observed).** `depth-gate.txt`
(`f683297c…`, 104 B) and `trio.txt` (`d877fe2f…`, 65 B) match between `W/gates/` and
`corpus/evidence/round69/gates/`; E7 reads the corpus copies and compares to a fresh run, so
byte-equality must be re-proved after any later edit to `SKILL.md` (GateReceipts run 3 arms in
`W/GateReceipts.md:54–57`, including an `executed 3 of 8` copy).

**F6 — "the knowledge entry's nginx section" has no owner and no check (observed; pointer risk).**
`claims:52` calls S241 "the live-reopened grader row, cited by the knowledge entry's nginx
section", but none of the 14 seat items writes that section and no C1 target or gate check reads
it. At snapshot `corpus/knowledge/tb2-network-service-offline-grader.md` has no nginx section
(`grep -c '^## .*nginx'` → 0; the only `nginx` hit is `:31`, class membership). Either the landing
adds it or the parenthetical stays unproven; C1's predicate sentence is unaffected. **Post-snapshot
(§G):** the landing added a separate entry, `corpus/knowledge/tb2-nginx-request-logging-offline.md`
(cites `S241` twice) and a `corpus/README.md` index row; the old file still has no nginx section,
so the citation `claims:52` asserts exists, but as a new entry, not a section of the old one.

**F7 — the C2 green run and C2 selftest tally have no frozen receipt path (observed; pointer
risk).** Only E7's two receipts have paths; everything else in the close-out list is a *record*.
A closure must not look for a green receipt that was never specified, and must not treat the
wave's `census-before.txt`/`c2-red-before.txt` as the closing values. Expected lines are in C11/C12.

**F8 — the checker does not bind `CASE`, `PORT`, or the sandbox captures (observed).**
`check_receipt` parses only `PROBE`, `GRADER`, `VECTOR`, `TEST`, `SUMMARY`, `PREDICATE`; `CASE`
lines (which carry `case_sha256`, `server_pid`, `sandbox_rc`) and `PORT` are written
(`…probe.py:446–447`) and never read. This is claims limitation (i) ("cannot prove a live run")
made concrete: the per-case pids and B3/B4 captures are the live witness, and a forged receipt can
omit or invent `CASE` lines without a defect. Confirmed by `awk` over the checker body (§S16).

**F9 — the closing census must reproduce `exit 0` with 24 W04 (observed baseline).** Live
`W/CensusAudit/census.txt` records `exit-code: 0`, `W04-count: 24`, verdict line
`kengaku ok …/corpus/SOURCES.md`, and freshness against `census-before.txt`'s first 25 lines.
The S241 URL is not currently in `corpus/SOURCES.md` (`grep -c 'nginx-request-logging'
corpus/SOURCES.md` → 0), so a properly shaped new row should not add a W04; that is an expectation,
not an observation of the closing registry.

**F10 — claims' `--render-table` byte-equality clause cannot hold as literally written
(observed).** `claims:25` says the frozen case table "(`--render-table` must byte-equal it)". The
control's renderer output is a plain-text block (`case  setup … vector`), the claims artifact is a
markdown table; byte-equality between them is impossible. The practical re-derivation is
byte-equality between a fresh `--render-table` and the committed render block in
`.ufo/waves/round-69/nginx-control.txt` (§S14). NginxBattery.md reports this at line 230. The C1
predicate sentence does not mention the renderer, so this bites the doc's parenthetical, not the
predicate.

**Status (not findings, for calibration):** at snapshot `SKILL.md` still reads `executed 2 of 8`
(B5 pending), `S241` absent (B6), the knowledge nginx section absent (B7), C2 green/selftest absent
(C11/C12), `LOG.md`/`SCORECARD.md` round-69 sections absent (D1/D2), `w1-results.json` absent (D3),
and 3/14 seat reports present. The C2 corrections E2/E4/E5/E6 (C7–C10) and E1/C6 are already in
the working tree and are uncommitted (`git status --porcelain`: `M SKILL.md`, `M
corpus/QUALITY.md`, `M corpus/knowledge/tb2-network-service-offline-grader.md`, `M
corpus/lessons/round-68.md`, `?? corpus/evidence/round69/`).

---

## G. Post-snapshot drift (`2026-11-03T21:15:29-03:00`; §A–§F stay the 21:10:32 snapshot)

While this file was being written the landing produced three artifacts; no claim check reads them.
Recorded here so a closure does not treat §B's live cells as the tip.

```sh
$ grep -cE '^\|[[:space:]]*S241[[:space:]]*\|' corpus/SOURCES.md
1                                        # row 256
$ grep -c 'executed 3 of 8' SKILL.md
0
$ sha256sum corpus/knowledge/tb2-nginx-request-logging-offline.md
ae70a6307e42599be4946bed7b751459773670264b7a47f3077b948e726380f9  corpus/knowledge/tb2-nginx-request-logging-offline.md
$ grep -c 'S241' corpus/knowledge/tb2-nginx-request-logging-offline.md
2
$ grep -c 'tb2-nginx-request-logging-offline.md' corpus/README.md
1
$ ls corpus/evidence/round69/nginx/receipt.txt corpus/evidence/round69/nginx/sandbox .ufo/waves/round-69/w1-results.json
# absent ×3 (all three still absent at 21:15:29)
```

- **S241 landed** at `corpus/SOURCES.md:256`: `| S241 | Terminal-Bench 2.0 nginx-request-logging
  grader … | code | A | network-service grader offline execution (R69-C1): … | tests/test_outputs.py:13
  verbatim … sha256 045cc716…4acda0 (5947 bytes) = SHA256SUMS line 111, byte-identical by cmp | legs
  2-4 are HTTP-observable and need no nginx; … | mined | 2026-11-03 | 180d |
  corpus/knowledge/tb2-nginx-request-logging-offline.md |`. Its `used-by` cites the **new** entry,
  not the `tb2-network-service-offline-grader.md` the SourceOpen item proposed (B6). The row
  resolves (the named file exists); the claims' before→after target is only `grep -c … → 1`, so
  the cell divergence is a citation choice a closure should name, not a missing row.
- **New knowledge entry** `corpus/knowledge/tb2-nginx-request-logging-offline.md` (sha256
  `ae70a630…`, one `verified-at:`, two `S241` citations) plus a `corpus/README.md` index row. Its
  title records the verdict: "…the legs the frozen table could not price (R69-C1, MISS)" —
  independent corroboration of §F1. It is **not** the
  `corpus/knowledge/tb2-network-service-offline-grader.md` file E4 reads, so it neither helps nor
  harms E4.
- **Still absent:** `corpus/evidence/round69/nginx/receipt.txt`, `corpus/evidence/round69/nginx/sandbox`,
  `.ufo/waves/round-69/w1-results.json`; the class row still reads `executed 2 of 8` (correct for a
  C1 miss: the class row is not moved).
- `git status --porcelain` at 21:14:52 additionally listed `M corpus/README.md`, `M corpus/SOURCES.md`,
  `?? corpus/knowledge/tb2-nginx-request-logging-offline.md` — the three landings above.

---

## S. Re-derivation snippets (verbatim; `S` = the walker's scratch root)

```sh
# S1 presence at a revision
for p in corpus/evidence/round69/nginx/receipt.txt corpus/evidence/round69/c2-receipts/provenance-erratum.txt \
         corpus/evidence/round69/gates/depth-gate.txt corpus/evidence/round69/gates/trio.txt; do
  for rev in a518980e b288e8e0; do
    git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -e "$rev:$p" 2>/dev/null \
      && echo "present $rev $p" || echo "absent $rev $p"
  done
done

# S2 textual targets on committed bytes (substitute the real file/pattern)
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show b288e8e0:SKILL.md | grep -c 'executed 3 of 8'

# S3 per-leg P/F tally from a receipt
awk '$1=="TEST"{c[$3]++; if($4=="P") p[$3]++; else if($4=="F") f[$3]++}
     END{for(k in c) printf "%s P=%d F=%d\n", k, p[k], f[k]}' RECEIPT

# S4 per-leg tally from the frozen CASES (loads module constants only; no port, no sandbox)
python3 - <<'EOF'
import importlib.util
s = importlib.util.spec_from_file_location('p', 'plans/round69_c1_nginx_probe.py')
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
for i, n in enumerate(m.LEGS, 1):
    print(i, n, "P=%d" % sum(c['expected'][i-1] == 'P' for c in m.CASES),
          "F=%d" % sum(c['expected'][i-1] == 'F' for c in m.CASES))
EOF

# S5 VECTOR arity of a receipt (writer emits 6, checker requires 5)
awk '$1=="VECTOR"{print NR": "NF" tokens"}' RECEIPT

# S6 grader digest vs registry line
sha256sum corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py
sed -n '111p' corpus/evidence/round52/graders/SHA256SUMS

# S7 instrument digest vs receipt line 1
sha256sum plans/round69_c1_nginx_probe.py

# S8 E3 re-hash of every INPUT at both revisions (from the lane root)
grep '^INPUT ' corpus/evidence/round69/c2-receipts/provenance-erratum.txt | while read -r _ p a b; do
  ta=$(git show 27f649f8:"$p" | sha256sum | cut -d' ' -f1)
  tb=$(git show 1ec2e60a:"$p" | sha256sum | cut -d' ' -f1)
  printf '%s tree=%s(%s) landing=%s(%s) %s\n' "$p" "$ta" "$([ "$ta" = "${a#at-tree=}" ] && echo ok || echo MISMATCH)" \
         "$tb" "$([ "$tb" = "${b#at-landing=}" ] && echo ok || echo MISMATCH)" "$([ "$ta" = "$tb" ] && echo same || echo DIFFERS)"
done
git cat-file -e 27f649f8^{commit} && git cat-file -e 1ec2e60a^{commit}

# S9 reproduce the C2 red-before receipt at the freeze commit
mkdir -p "$S/base" && git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive b288e8e0 | tar -x -C "$S/base"
(cd "$S/base" && python3 plans/round69_c2_routed_defects.py) > "$S/red.txt"; echo rc=$?
diff -u /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-69/c2-red-before.txt "$S/red.txt"

# S10 E7: fresh stdout must equal the committed receipt byte for byte (run from the lane root)
python3 plans/round63_gate_checks.py depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt --root . > "$S/depth.fresh"
diff -u corpus/evidence/round69/gates/depth-gate.txt "$S/depth.fresh"
python3 plans/round63_gate_checks.py trio corpus/knowledge/tb2-network-service-offline-grader.md > "$S/trio.fresh"
diff -u corpus/evidence/round69/gates/trio.txt "$S/trio.fresh"

# S11 C2 green
python3 plans/round69_c2_routed_defects.py; echo rc=$?   # want: DEFECTS n=0 / PREDICATE R69-C2 pass / rc=0

# S12 C2 selftest
mkdir -p "$S/st" && python3 plans/round69_c2_routed_defects.py --selftest --work "$S/st"

# S13 closing census
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku; echo rc=$?

# S14 renderer vs the control's committed block (not vs the markdown table — see F10)
python3 plans/round69_c1_nginx_probe.py --render-table

# S15 C1 checker and selftest
python3 plans/round69_c1_nginx_probe.py --check-receipt RECEIPT
mkdir -p "$S/st" && python3 plans/round69_c1_nginx_probe.py --selftest --work "$S/st" --green-receipt RECEIPT

# S16 confirm the checker never reads CASE/PORT lines (empty output = not read)
awk 'NR>=483 && NR<=575 && (/CASE/ || /PORT/ || /sandbox/)' plans/round69_c1_nginx_probe.py
```

**Closure order.** S1/S2 for the before-column → read each verdict artifact (B*/C*/D*) with its
S-snippet → S9 (red-before honesty) → S11/S12 (C2) → S15 (C1) → S10 (E7) → S13 (census) → D1/D2
write-up. Score C1 only from the receipt the claims name (B1) plus §S15; score C2 only from
`DEFECTS n=0` at the landing tip. Do not re-score a miss (kill rule), and do not edit a predicate,
case table, vector, kill rule or target.

---

## Commands NOT run by this seat (scribe boundary)

- The C1 battery (`python3 plans/round69_c1_nginx_probe.py --lane . --work … --receipt …`) — port
  8080 was not opened by this seat.
- `--check-receipt`, `--selftest`, `--render-table` on the C1 instrument (their live outputs are
  quoted from `W/NginxBattery/check.txt` and `W/ReceiptReverify/*`; §S15/S14 are for the closure).
- The C2 gate in any mode (`--root`, `--selftest`) — green/red values are quoted from the frozen
  receipts and held for the seats that own them.
- `plans/round63_gate_checks.py depth|trio` — E7 byte-equality is quoted from GateReceipts' report;
  this seat compared the two committed copies with `sha256sum` only.
- `scripts/sources-census.sh` — the census result is read from `W/CensusAudit/census.txt`.
- Any `curl` fetch (S241 quote/status) — SourceOpen's item.
- Any git/jj **write** command in the lane or fleet; any edit to a tracked lane file. This seat
  wrote only this report; its scratch `/fast/scratch/hyaku/kengaku-r69/EvidenceIndex/` is deleted
  before yield.
- The importlib snippet (§S4) **was** executed: it loads module constants and runs nothing.
  `sha256sum`, `git show`, `git cat-file`, `git status`, `diff`, `awk`, `grep`, `find`, `ls`,
  `stat`, and the `python3 - <<EOF` derivation above are the only commands this seat ran against
  the lane.
