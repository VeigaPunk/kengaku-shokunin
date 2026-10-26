# F38RevLesson receipts (kengaku round 38 wave 2, 2026-10-26)

All commands run read-only against the lane at /home/vgpnk/Projects/shokunin/kengaku-shokunin (no clone needed: no writes, no counter re-runs; counters were read from the landed receipts). Live fetches: 2 (Dockerfile, audit.txt).

## Commit graph
```
$ git -C <lane> log -1 --format='%H %ci %s' <sha>
fc1174f52b150999bef91f2e81da78732ca0eb9f 2026-10-26 02:25:17 -0300 round-37 verifier spot-check (integrator, hyaku): non-author admit/reject
21e6251bfebf87ecf09f7b0a6df98b5c6179d0e9 2026-10-26 02:38:25 -0300 round-37: wave-2 reports and results (37/37), outcome appended to lesson and SCORECARD
e0a378539a45cc9388c66cfba22f44275131de23 2026-10-26 02:38:28 -0300 round-38: freeze — claims C1 ... and C2 ...
e95cf5500b6c13305cc41b8532ae07fb2c9dcd7b 2026-10-26 02:38:41 -0300 round-38: first recorded build-pmars probe run on a clean clone of e0a37853 (cases=22 observed_pass=7 observed_fail=15 mismatches=0; second run byte-equal)
d93b7d68dacfd6a23ec2cf732a4615d6c732c73e 2026-10-26 02:56:10 -0300 round-38: frontier and routed items — Q28 ... Q29 ... D3 ... D4 ... tip_receipts.py ... D6 ...
8c7422d7a646515d80af44844e8ecc8a1fc1d30a 2026-10-26 03:06:14 -0300 round-38: wave-1 reports and results (40 seats, 40 reports, 0 dead) ...
$ git rev-parse e0a37853^  -> 21e6251bfebf87ecf09f7b0a6df98b5c6179d0e9
$ git diff --stat fc1174f5 21e6251 -- plans/ corpus/knowledge corpus/SOURCES.md corpus/README.md  -> (empty, rc=0)
$ git cat-file -e e0a37853:corpus/evidence/round38/build-pmars-probe.txt  -> rc=128 ("exists on disk, but not in e0a37853")
$ git ls-tree -r 21e6251 --name-only .ufo/waves/round-37/falsify | wc -l  -> 380
$ git ls-tree --name-only e0a37853 -- .ufo/waves/round-38/claims/  -> census-before.txt, control-c1-gate-edited.txt, control-c1-nothing.txt, control-c2-nothing.txt, control-c2-skip.txt, frozen-digests.txt
$ git diff --stat d93b7d68 8c7422d -- plans/ corpus/  -> only corpus/lessons/round-38.md added (77 lines)
$ git diff --stat 8c7422d 10d2e97 -- plans/ corpus/  -> (empty)
```
21e6251 stat includes `.ufo/waves/round-37/falsify-results.json`, `corpus/lessons/round-37.md` (+20), SCORECARD.md (grep -c = 1), 384 files.

## Controls (all read in full; match lesson lines 11-13)
- control-c1-nothing.txt: `PINS total=14 mismatched=0` / `BATTERY fixtures=64 wrong=0 renamed_disagree=0 sidechannel=0` / `MUTANTS total=22 killed=0 survived=22 invalid=0 null_detected=0` / `PREDICATE C1 fail` / exit=1.
- control-c1-gate-edited.txt: `PINS total=14 mismatched=1 first=plans/pkg_gate.py` ... `MUTANTS total=22 killed=0 survived=0 invalid=22` / exit=1.
- control-c2-nothing.txt: `checks=7 defects=4` (V2,V3,V4,V7 DEFECT; V6 ok) / exit=1.
- control-c2-skip.txt: `checks=7 defects=2` (V2 DEFECT, V6 DEFECT, V7 ok) with `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt` / exit=1.
- census-before.txt: 15 `W04` rows + `kengaku ok` / exit=0.

## Landing receipt .ufo/waves/round-38/integrate/measure-final.txt
`TIP d93b7d68dacfd6a23ec2cf732a4615d6c732c73e`, `untracked_in_clone=0`; C1 `MUTANTS total=22 killed=21 survived=1` (N21 SURVIVED) `PREDICATE C1 fail` exit=1; C2 `checks=7 defects=0` `PREDICATE C2 pass` exit=0 (P10 `probe_rerun=byte-equal bytes=5537`, P8 `index_rows=45 knowledge_files=45`); direction check `DIR N21 D5 declared=silence observed=mirror MISLABELLED`, `DIRECTIONS total=22 mislabelled=1`, exit=1; round37_c1 `MUTANTS total=55 killed=55`; anchor check `rows=109 tokens=17 defects=0`; ledger_tip `rows=9 closed=9 observed_pass=9 mismatches=0`; tip_receipts at tip d93b7d68 `receipts=24 byte_equal=4 differ=0 skipped=20` (19 `probe-r19-*` skip lines with `no-committed-re-run-command`; `regex-log-probe-first-run.txt` `declared-nonreproducible-absolute-scratch-paths`; 4 equal); census `--file` form `file ok` exit=0; `registry_rows=109 knowledge_files=45 index_rows=45`; `sha256sum -c frozen-digests.txt` all OK.

## Counts
```
$ git show e0a37853:corpus/SOURCES.md | grep -c '^| S'   -> 107
$ git show d93b7d68:corpus/SOURCES.md | grep -c '^| S'   -> 109
$ git ls-tree -r e0a37853 --name-only corpus/knowledge | wc -l -> 44
$ git ls-tree -r d93b7d68 --name-only corpus/knowledge | wc -l -> 45
$ wc -l .ufo/waves/round-38/assimilation/collisions -> 31 (ids S077..S114, all within the staged range)
$ cat .ufo/waves/round-38/assimilation/quarantine-slice -> S091, S105 (2 rows)
```

## Captures and quotes
```
$ sha256sum corpus/evidence/round38/tb2-build-pmars/test_outputs.py
d9d2796ddc19cf8159670567e174ea377e2bce675bf3451d5951c045b01f4e85  (lesson: d9d2796d…f4e85)
$ sha256sum corpus/evidence/round38/tb2-build-pmars/instruction.md
1606850579342a8b8f2189de0e499fae6be21198150d8dd1e4d18c2efbcf3b82  (lesson: 1606850…3b82)
$ sed -n '46p' .../test_outputs.py -> "    assert re.match(r"Results: \d+ \d+ \d+", battle_result), ("   (lesson line 22 quote exact)
$ sed -n '9p'  .../instruction.md -> "We'll verify the binary has no X11 dependencies, uses Debian sources, and that the debugger works properly."  (lesson line 23 quote exact)
$ grep -n "1.22.21" .ufo/waves/round-38/build/R38LessonDraft/tb2-issue-59-body.md -> line 14: E: Version '1.22.21' for 'dpkg-dev' was not found
```

## Live fetches (upstream, read-only)
```
$ curl -sfL .../terminal-bench-2/2fd12b88.../build-pmars/environment/Dockerfile | sed -n '7,11p'
WORKDIR /app
(blank)
COPY warriors/flashpaper.red warriors/rave.red /app/     <- line 9 exactly as lesson line 24 / entry :194
$ curl -sfL .../JonathanGabor/terminal-bench-2-audit/main/audit_results/20260120_125158/audit.txt | sed -n '249p;255p'
- There's no direct verification that the binary was compiled from the specific source in `/app` ...   (l.249)
- The X11 dependency check via `ldd` is reliable.                                                      (l.255)
```

## Key cross-references verified in place
- round-37.md:42 = the order-of-operations Mistakes row; its fix column ends: "Rule forward: a control that executes a frozen instrument keeps the run as a receipt." (basis of Defect 1). round-37.md:48 = Mistakes row 7 (C1 counter counts a kill without attributing it) — lesson line 40's "row 7's limit" resolves.
- plans/round-38-claims.md:8-15 = the disclosure block (lesson line 36 pointer resolves).
- plans/round38_c1_verify.py:140-141 = N21 row, replacement `sums.splitlines()` → `sums.splitlines()[:1]`, declared `silence`; docstring line 20 "the 13 non-equivalent survivors" (lesson line 38's second locus).
- plans/battery38: 12 modules; `d5m-n21-manifest-row-2` declared in d5m.py:17,77; p5m.py appends the N08 blank line at the END of the manifest (`path.write_text(text + line + "\n")`), so the spot-check item 3 "only accept fixture whose matching manifest row is not the first" holds.
- corpus/QUALITY.md:436-437 carries "the empty `frozen_instruments` branch of P1" inside the unclaimed list (lesson line 38's pointer 435-437 covers it); Q28 at :455, Q29 at :501.
- corpus/knowledge/tb2-git-webserver-grader.md:107 = `| instruction.md:9 | enforced | capitalised, leading-space |`; `## Errata (round 38)` at :293 correcting rows 7-9.
- .ufo/waves/round-38/build/R38MapErratum/controls.txt: Control B -> `(False, "rows=7 tags=7 bad=['results-format: labelled enforced, receipt derives partly']")`, Control C -> `(False, ... 'no-x11: cites no case or a case that does not violate it')`.
- .ufo/waves/round-38/build/R38MapRetro/run-entry.txt: `rows=4 disagree=2` (instruction.md:8 and :9 labelled≠derived), `MAP-RETRO disagree=2 ... fail`; run-corrected.txt: `disagree=0 ... pass`.
- .ufo/waves/round-38/build/R38BatD5.md §BLOCKER (:146): 8-shape manifest matrix, "No shape has `ref DEFECT` with a passing mutant", "`ref DEFECT ∧ mutant ok` — impossible for every input".
- .ufo/waves/round-38/build/R38CritClaims.md: D1 "unadvertised = 3, or 5" (N01, N08, N16 tier N; totals C 9, K 10, N 3); D4 "13 + 1 + 6 = 20 ... 17 + 6 − 1 = 22 ... The '13' should be 16"; §2 junk battery `BATTERY fixtures=66 wrong=0 renamed_disagree=0 sidechannel=0` / `MUTANTS total=22 killed=20 survived=2`.
- .ufo/waves/round-37/falsify/F37CritC2Map.md:15,171: `V7 ok rows=4 bad=0`.
- corpus/lessons/round-37-verifier-spotcheck.md §5 at :144 with D1 (:146) through D7 (:166).
- .ufo/waves/round-38/build/R38AnchorBind/receipts/mutant-M4b.txt: old checker `rows=107 tokens=16 defects=0 EXIT=0`, fixed copy `DEFECT S111 ... class=digest-wrong-capture ... defects=1 EXIT=1`; M5/M6/M7 receipts all contain `digest-wrong-capture`.
- .ufo/waves/round-38/build/R38LedgerTip: §4 "Before / after, same machine, same seconds"; receipts/01-before-detached.log shows `CalledProcessError ... exit status 128`; 02-after-detached.log shows `REF BIND ref=refs/heads/master rev=e95cf550... why=clone-lacks-ref`.
- .ufo/waves/round-38/build/R38TipReceipts/tip-receipts-tamper-control.txt: `flip=byte 1699 0x27->0x26 verdict=differ`.
- considereThese/2026-10-25.md:44: proposal 2 = "(b) blocks pre-registration when a class recurs twice, and (c) includes a tip-receipt validator (every `corpus/evidence/**` receipt re-run and byte-compared)".
- shokuknow (read-only): `merge/kengaku/knowledge/corpus/knowledge/benchmark-card-field-schema-2026-10-23.md` and `benchmark-card-adoption.md` exist; `git -C shokuknow log ba6779f0..HEAD -- merge/kengaku` -> empty; ba6779f0 = 2026-10-24 10:50:02.
- .ufo/waves/round-38/build/R38MergeRescreen.md:70: "admit 2 (rows 1–2), hold 5 (rows 3–7), refuse 5 (rows 8–12)"; rows 1-2 are the card family, rows 8-12 REFUSE.
- PROVINCE.md:311 "Reported out (round 38)" block: 16 instrument rows with file:line (tameshi 3, kumitate 4, mado 2, kake 3, mori 1, kotodama 1, kaidoku 2).
- plans/round38_c2_verify.py constants: SPEC_REL/GATE_REL+GATE_SHA256/PROBE_REL/DRY_REL/CAPTURES pinned (lesson line 56 D7 half); R36CritScope.md F3 (:123), F4 (:128), F5 (:134) exist and no round-38 commit touches that wording (8c7422d..10d2e97 plans/corpus diff empty).
- Entry tb2-build-pmars-grader.md: :26/:156/:233 "21-line" (no "14-line" left), :178 "### Contestable tags" ("the frozen tags ... are not edited"), :193-195 Dockerfile citation, :133-148 requirement map with `partly` rows (spot-check item 5 coherent).
- Counter runtime reads (grep open(/read_text): c1 reads gate/spec/battery only; c2 reads spec/dry/SHA256SUMS/SOURCES/receipt/entry — none of the paths 21e6251 touched (.ufo/waves/round-37/*, SCORECARD.md, corpus/lessons/round-37.md); supports lesson line 7.
