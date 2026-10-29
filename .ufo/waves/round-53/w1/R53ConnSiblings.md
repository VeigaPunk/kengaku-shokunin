# R53ConnSiblings — sibling-overlap scan (kengaku round 53, wave 1, connector, read-only)

Seat: `R53ConnSiblings` (leaf; no subagent dispatch). Judged on: adjacency. Lane: kengaku (`/home/vgpnk/Projects/shokunin/kengaku-shokunin`, HEAD `1373b6c`, detached; read-only use). Frozen claims read in full: `plans/round-53-claims.md`.

Scope read: `PROVINCE.md` and `SKILL.md` headings of the 20 `*-shokunin` lanes, plus `grep` over their `corpus/`, `tools/`, `.ufo/` and `lessons` for the requested terms. Counts below are **file counts** from `grep -rl` / `uniq -c` unless a line number is given. Overlap is reported, not absorbed. Nothing was edited, committed, installed or run in any lane.

## 0. Blindness and hygiene

- I did not open any `C1Label*` file, any `w1/C1ExecClassifier*` file, or any label output of any seat. I did not open `plans/round53_c1_classify.py`.
- A fleet-wide `grep -l` ran in the background; kengaku hits were filtered out before display. No kengaku file body was printed from it.
- Scratch `/fast/scratch/hyaku/kengaku-r53/R53ConnSiblings/` (only an exact-grep file list) was removed before yield; `ls` afterwards shows no `R53ConnSiblings` entry.
- No install, no upgrade.

## 1. Commands used (representative; run in-session, read-only)

```sh
ls -d /home/vgpnk/Projects/shokunin/*-shokunin
# per-term file counts, excluding kengaku
grep -rIl -i -E 'terminal-bench|terminal_bench|Terminal-Bench' --include='*.md' --include='*.py' --include='*.json' --exclude-dir=.git . | grep -v '^./kengaku-shokunin/' | awk -F/ '{print $2}' | sort | uniq -c
#   same shape for: test smell | mutation|mutant | oracle | gate registry|Gate/probe registry | tip-state|tip state | ledger | executed row|row existence | presence-only | blind label|labeler
grep -rIn -i -E 'terminal-bench|terminal_bench' kumitate-shokunin mado-shokunin souji-shokunin tabi-shokunin kaidoku-shokunin .ufo MANIFEST.json
grep -n -i -E 'smell|mutation|mutant|oracle|registry|ledger|presence|grader' tameshi-shokunin/PROVINCE.md
grep -n '^#' tameshi-shokunin/SKILL.md
grep -n -E 'entry-registry walk|^### Gate/probe registry|^## The leg ledger|^## The mutation bar|^## The mutation service|replays every row|A registry row stops' tameshi-shokunin/SKILL.md
grep -n -E 'expect|needles|stdout_contains' tameshi-shokunin/tools/registry-check.py      # grep-extracted lines 21-49, 231, 652
python3 -c "import json;d=json.load(open('tameshi-shokunin/tools/registry.json'));print(len(d['rows']))"   # -> 60
grep -n -E '^\| `(ledger-tip|tip-receipts|defect-ledger|round52-c1|round52-c2)`' kengaku-shokunin/SKILL.md
awk -F'|' '/^\| `?[a-z0-9-]+`? *\| (gate|probe)/{n++} END{print n}' kengaku-shokunin/SKILL.md   # -> 75
grep -rl 'terminal-bench\|terminal_bench' */ | grep -v '^kengaku-shokunin/' | wc -l          # the exact PROVINCE.md:353 command -> 1299 files (1293 under lane3/)
grep -c 'terminal-bench\|terminal_bench' kumitate-shokunin/corpus/knowledge/multi-agent-coordinator-topologies.md kumitate-shokunin/corpus/lessons/round-63.md   # -> 0, 0
grep -c -i 'freeze-integrity' kengaku-shokunin/PROVINCE.md   # -> 0
git -C lane3 rev-parse --abbrev-ref HEAD; git -C lane3 log -1 --format='%h %ci %s'; git -C lane3 status --porcelain | wc -l   # master, 297e179, 0
diff -q lane3/PROVINCE.md kengaku-shokunin/PROVINCE.md   # differ
git -C kengaku-shokunin log -1 --format='%h %ci %s'      # 1373b6c
grep -n 'lane3' MANIFEST.json                             # line 31979 routed note
```

## 2. Sibling overlap table

Relation key: **DUP** = duplicates an existing sibling or same-lane instrument; **DEP** = claim depends on it; **REUSE** = claim could reuse it (adjacency: reported, not absorbed); **HOMONYM** = same word, different meaning; **NONE** = no overlap found.

| # | Sibling (owner of what) | path:line | Relation to kengaku's claim | Detail |
|---|---|---|---|---|
| 1 | **tameshi** — executed registry replay. `tools/registry-check.py` re-runs every row of `tools/registry.json` (60 rows) in a scratch clone and compares observed exit with `expect.exit`; verdicts `held` / `differs` / `superseded` | `tameshi-shokunin/SKILL.md:1882` ("replays every row of"); `:1872` (`differs`, exit 1); `:2197` (entry-registry walk row); `tools/registry-check.py:35` (row holds when exit equals `expect.exit`); `:231`, `:652` (`stdout_contains` needles) | **DUP** of C2's executed-row leg (declared exit, scratch clone, mismatch count). **DUP-adjacent** for the evidence fragment: tameshi rows carry `stdout_contains` for positive outcomes only. | C2 would build a second executed-row walk in a second lane with the same mechanism. The frozen claim does not name tameshi's walk. Reuse candidate: mirror tameshi's contract rather than reimplement. C2's distinct content is the per-row declared *tip-state* plus red-row evidence. |
| 2 | **tameshi** — lifecycle rule: a row leaves `active` only as `superseded` with `superseded_by`, and still runs | `tameshi-shokunin/SKILL.md:1872` | **REUSE** for C2's kill rule. C2 has no superseded state; a red row with reason is its only non-green path. | Fleet answer to "registry row stops holding". |
| 3 | **tameshi** — mutation bar (nominal vs load-bearing), mutation service, leg ledger, service limits | `tameshi-shokunin/SKILL.md:122`, `:822`, `:949`, `:1282` | **REUSE / DEP** for C1's 16-mutant leg (`W2MutC1`) and its control legs. The "load-bearing" bar and "arm coverage is the floor" rule apply directly. | `kengaku-shokunin/PROVINCE.md:316-330` already routes sandboxed mutated-child execution to tameshi, kumitate, mado and kake as fleet prior art. |
| 4 | **tameshi** — third case: cross-author confirmation; no-permissiveness audit; fail-closed arm taxonomy | `tameshi-shokunin/SKILL.md:696`, `:494`, `:525` | **REUSE** for C1's "two labels from two seats, not the author" leg and "every control must fail its named leg". | Not blind-label work. Same discipline, different measurement. |
| 5 | **tameshi** — gate/probe registry cell shape (Name / Kind / Entry command / Verdict map / Self-test / Pinned values / Write scope / Owner) | `tameshi-shokunin/SKILL.md:1541`, `:1719`, `:1849`, `:2181` | **DUP** of the registry *format*. Kengaku's registry at `SKILL.md:560` uses the same shape. | Fleet convention. C2 inherits the format; the 75 rows are kengaku-specific. |
| 6 | **kengaku (same lane)** — `ledger-tip` gate: every closed ledger row's check re-runs on a clean clone of the tip | `kengaku-shokunin/SKILL.md:581` (also `:677`) | **NAME COLLISION / DUP-adjacent** with C2's "tip-state ledger" (`plans/round53-tipstate.json`). | Not a sibling. Two lane instruments already answer "ledger at tip". The L1 should pick a distinct file name and say how C2 relates. |
| 7 | **kengaku (same lane)** — `tip-receipts` (byte-equal re-run at tip); `defect-ledger` | `kengaku-shokunin/SKILL.md:586`, `:612` | Same-lane overlap with C2's declared state at tip. | Noted so the L1 knows the existing tip-facing instruments. |
| 8 | **kengaku (same lane)** — `round52-c2`: every advertised verdict instrument has a registry row (`MISSING`, `ENTRY-MISSING`, `DUPLICATE`) | `kengaku-shokunin/SKILL.md:636` | **DUP** of C2's row-existence leg (`missing=0 extra=0 duplicate_names=0`). C2 adds only the executed leg. | The claim already calls the row-existence counter existence-only; `round52-c2` is that counter. |
| 9 | **kengaku (same lane)** — `round52-c1`: whole-benchmark grader-vacuity triage of 89 TB2 tasks | `kengaku-shokunin/SKILL.md:635` | **Superseded by C1** if admitted. | `PROVINCE.md` has no round-52 paragraph (`grep -n -i -E 'round.?52' PROVINCE.md` → none). The non-admission is not recorded in PROVINCE. |
| 10 | **souji** — `## Gate registry`; `souji-registry-agreement` (`mismatches=0`); `LG-MISSING-REG` in landing gate | `souji-shokunin/SKILL.md:189`, `:255`; `souji-shokunin/tools/souji-registry-agreement.py`; `souji-shokunin/tools/souji-landing-gate.py:66`, `:179` | **DUP** of registry-vs-list agreement (C2 `missing/extra/duplicate`). **REUSE**. | Souji checks agreement with a list, not execution. |
| 11 | **kama** — `gate-registry-check.py`: "occurrence check only, it does not inspect row columns"; round-32 repair grades `thin-row`, `empty-exit-map`, `missing-path` | `kama-shokunin/SKILL.md:1263`, `:1359` | **DUP-adjacent** for row existence; **NONE** for execution. | Kama explicitly disclaims execution. |
| 12 | **kagi** — executed-row accounting: `rows_run` against deferred, POLICY and HOST-SKIP rows | `kagi-shokunin/corpus/claim-ledger.sh:1071`, `:1256`, `:1260`; `kagi-shokunin/corpus/lessons/round-24.md:129`; `round-22.md:259` | **REUSE** for C2's "executed = registry" count. `:1071` records a counting bug: rows were counted as run before they ran. C2 must avoid the same. | Counting hazard already diagnosed in a sibling. |
| 13 | **kumitate** — `gate-mutants.mjs` 43-mutant battery, no bwrap (cited by kengaku `PROVINCE.md:322-323` as `SKILL.md:616`) | `kumitate-shokunin/SKILL.md:616` (per PROVINCE); `kumitate-shokunin/corpus/knowledge/runtime-remainder-census.md:218` (executed-rows-only mutation battery) | **REUSE** for C1's mutant leg. **NONE** for TB2 grading. | Kumitate's `registry-check.mjs` is a `@role` checker, not an executed-row walk. |
| 14 | **kaidoku** — freeze-integrity table (`touched`, `restored`, `blob_changed`, FREEZE an ancestor of REV) and "freeze-integrity evidence is only evidence when its own forgeries fail" | `kaidoku-shokunin/SKILL.md:584-596`, `:613`; `tools/round-32/freeze-integrity.py` (named `SKILL.md:1407`); `:362` (held-out set seeded by freeze) | **DEP / REUSE** for C1's FREEZE leg (classifier sha committed before labels; freeze commit a strict ancestor of the labels commit). Kaidoku already built this check and its forgery arms. | Kengaku `PROVINCE.md` does not cite kaidoku's freeze tool (`grep -c -i freeze-integrity` → 0). Adjacency gap. |
| 15 | **kasegi** — round-44/45 lessons: "presence-only predicates accepted denials"; "frozen v1 counters were presence-only: a 37-byte stub printing `selftest cases=8 failures=0`" | `kasegi-shokunin/corpus/lessons/round-44.md:189` (M44-10); `round-45.md:13` (M45-3) | **DEP / REUSE**. This is the forgery class C1's frozen control list encodes (population shrunk, capture bytes replaced by stub, forged selftest). The round-52 failure that C1 cites is the same class kasegi recorded. | Prior art for C1's control set; cite it. Also a HOMONYM (§3). |
| 16 | **chousa** — research method (question → source hierarchy → citation chain; SOURCES contract) | per kengaku `PROVINCE.md:138` (chousa's own `SKILL.md` not opened) | **DEP** for C1's prior-art leg (`SOURCES.md` S194+, archived fetches, sweep of ≥2 non-naming fetches). **Tension** with `PROVINCE.md:138`: "holds neither method nor duplicates it". | See §4 item 5. |
| 17 | **chousa** — its own round-53 wave-1 connector, same seat name | `chousa-shokunin/.ufo/waves/round-53/w1/R53ConnSiblings.md:40` (cites kengaku `SKILL.md:586`); `:93-114` (cites kengaku `PROVINCE.md:224-228`, `plans/sources_adopt.py`) | Same-round parallel scan; no duplicated claim. Name collision in fleet indexes (two `R53ConnSiblings` reports in different lanes). | The L1 should keep both paths distinct in any index. |
| 18 | **mado** — round-47 connector names kengaku's "Terminal-Bench 2.0" as a homonym (benchmark subject, not a terminal) | `mado-shokunin/.ufo/waves/round-47/w1/ConnSiblings.md:63` | **HOMONYM** only. | No mado surface touches TB2 grading. |
| 19 | **souji** — round-31 connector: kengaku holds the TB2 git-leak grader; plain-git reflog overlap | `souji-shokunin/.ufo/waves/round-31/w2/SwarmConnector28.md:21` | **NONE** in the claims; confirms TB2 grader ground is attributed to kengaku. | No sibling holds TB2 grader classification. |
| 20 | **mori** — "presence-only file test" for the watchdog driver; silence grading | `mori-shokunin/corpus/knowledge/silence-grading-r2.md:196`; `lane-silence-r2.md:172`; `verdict-machine-r4.md:332` | **HOMONYM** (§3). | Grader asserts file presence. |
| 21 | **kagi** — `presence-only` as a census *mode* / claim value | `kagi-shokunin/corpus/knowledge/adjacency-scope.md:64`, `:74`, `:91`, `:126`, `:167`, `:280` | **HOMONYM** (§3). | Census modes, not a grader class. |
| 22 | **kaidoku** — blind labels and freeze-before-run in a wave artefact | `kaidoku-shokunin/.ufo/waves/round-18/w2/FreezeBeforeRun.md:145` | **REUSE** (method only). | Wave file, not a corpus instrument. |
| 23 | **tabi, mori, kaidoku, kagi, kasegi, kumitate** — `presence-only` | file counts: tabi 128, mori 87, kaidoku 81, kagi 80, kasegi 78, kumitate 75 | **HOMONYM** (breadth only). | Not opened file by file. |
| 24 | **kotoba** — `## Gate registry` heading | `kotoba-shokunin/SKILL.md:448` | **NONE found** on the requested terms (heading only). | The combined pattern gave 460 files; most are not registries of executed rows. Not inspected further. |
| 25 | **tameshi, kumitate, kotodama, kasegi, kama, kake …** — `ledger` | file counts (tameshi 3307, kotodama 2406, kumitate 2361, kasegi 2064, kama 2062 …) | **HOMONYM** for the word. | Not inspected. C2's file name must be specific. |
| 26 | **souji, kama, tameshi, kotoba, mado** — `tip-state` / `tip state` | file counts (souji 21, kama 15, tameshi 14, kotoba 12, mado 10) | **HOMONYM** ("branch tip state" in ordinary sense). | No sibling holds a declared per-row tip-state instrument that I found. |
| 27 | **`lane3/`** (fleet root) — a second git clone of kengaku: `origin` = `kengaku-shokunin`, `master` @ `297e179` (round-50 notes), clean, own PROVINCE and SKILL that differ from the current lane | `lane3/` ; `MANIFEST.json:31979` routed note: "fleet-root .scratch/ and lane3/ strays not attributable to lane" | **Hazard, not a sibling.** It accounts for 1,293 of the 1,299 files that the exact PROVINCE.md:353 command returns outside kengaku, and it is outside every `*-shokunin` glob. | Any wave-2 "clean clone" or `*/` scan that does not exclude it double-counts kengaku. |

Checked, empty for the lane-specific meaning: no sibling holds a TB2 grader classifier; no sibling holds a blind-label oracle for graders. `test smell` appears in one file only (`tameshi-shokunin`, 1 file), with no smell-taxonomy row.

## 3. Homonyms the claim text must pin

- **presence-only**: C1 means "the grader's pass depends only on presence of an artefact", as defined in the round-53 P1 spec (`.ufo/waves/round-53/p1-spec.md`, cited by the claims; not opened by this seat). Siblings use the same words for a *counter* failure class (kasegi `round-44.md:189`, `round-45.md:13`), a *watchdog file test* (mori `silence-grading-r2.md:196`), and a *census mode* (kagi `adjacency-scope.md:64`). The claim text should cite the P1 spec definition, not the bare term.
- **tip-state**: C2's declared state versus the ordinary branch-tip wording (souji, kama, tameshi).
- **ledger**: kengaku's own `ledger-tip` (`SKILL.md:581`) already means a clean-clone re-run of ledger rows at the tip. C2's `round53-tipstate.json` should not be called a ledger in the claim text without saying so.
- **Terminal-Bench**: mado (`round-47/w1/ConnSiblings.md:63`) already reads it as a benchmark subject, not a terminal.

## 4. Statements in kengaku `PROVINCE.md` that the two claims would make false or stale

| # | PROVINCE.md:line | Statement | Effect of C1 / C2 | Status |
|---|---|---|---|---|
| 1 | `:126-127` (Frontier) | "agentic benchmark task-spec audits (Terminal-Bench 2.0 … — unopened leads)" | Already superseded at `:222-223` ("now opened", round 29). C1 widens the opened ground to the whole benchmark. The Frontier paragraph is still stale. | **Stale in place**; C1 widens the gap. |
| 2 | `:277`, `:304`, `:398`, `:446`, `:509`, `:611` (plus the round-43 family near `:557`, "8 of 89 read") | "… speak for the remaining N TB2 task graders (89 carry `tests/test.sh`; N are read)" | C1's label seats and classifier open the grader source of all 89 tasks (305 tests). If "are read" keeps its present meaning (opened and reasoned about), the parenthetical becomes false after wave 2. Recorded values across rounds: 3, 4, 5, 6, 7, 9. | **Would be made false** unless the claim defines "read". |
| 3 | `:353-355` ("Verified that no sibling reads, scores or claims TB2 grader execution: `grep -rl 'terminal-bench\|terminal_bench' */` outside `kengaku-shokunin/` returns only `kumitate-shokunin/corpus/knowledge/multi-agent-coordinator-topologies.md` and `kumitate-shokunin/corpus/lessons/round-63.md`") | Exact command, run today: **1,299 files** outside kengaku (1,293 under `lane3/`; 6 others: `kaidoku-shokunin/.ufo/waves/round-41/w2/artifacts/R41W2Reservation/tx-scan.json`, `kotoba-shokunin/.ufo/waves/round-71/receipts/census-after.txt`, `kumitate-shokunin/.ufo/waves/round-63/build/K63RevengerDispatcher/forgery-borrowed/.ufo/waves/round-35/build-dispatch.json`, `mado-shokunin/.ufo/waves/round-44/w2/RerunCensus/census-fleet.txt`, `tabi-shokunin/.ufo/waves/round-35/w1/CritC1Counter/bg-blindspots-full.json`, `tsukuroi-shokunin/.ufo/waves/round-43/w2/AdjFinal/sibling-skillmd-pin-lines.txt`). Both named kumitate files return **0** lowercase matches. | **False as written today.** Dated round 37, not caused by C1/C2. C1 adds TB2 citations, and this sentence is a routing rule. | Stale/false; amend or restate with the exact command and its scope. |
| 4 | ABSENT-surface rows, `:16`, `:113`, `:159` | Not touched by either claim. | None. | — |
| 5 | `:138` (Adjacent, chousa row): "research method … this lane holds neither method nor duplicates it" | C1's prior-art leg needs a sweep discipline (≥2 archived fetches that do not name the task, per `plans/round-53-claims.md` PRIOR-ART) plus new `SOURCES.md` rows (S194+). In practice that is a source-search method. | **Tension**: the claim does not say the sweep is chousa's method or reused from it. | Claim text should cite chousa as method owner. |
| 6 | `:223-229` ("fleet census remains the registry's authority") and `:319-330` (sandbox table) | C2 executes every registry argv; C1 runs mutants. The table says sandboxed graded or mutated child execution is fleet prior art, "not kengaku ground". | C2 and C1 put execution of kengaku's own gates and graders inside kengaku. PROVINCE does not say that is kengaku ground. | Ambiguous; amend the table to say which execution kengaku now owns. |
| 7 | (absent) round-52 paragraph | `PROVINCE.md` has no round-52 entry. The round-52 `round52-c1` row (`SKILL.md:635`) is the only record of the triage, and it does not say "not admitted". | Not made false. Non-admission of round-52 C1 is unrecorded in PROVINCE. | Gap. |
| 8 | (no statement found) | Registry claims about exit codes at the landing tree | C2 says 22 rows are red at base. I found no PROVINCE statement that contradicts this (checked by grep for registry, tip and ledger terms). | None found. |

## 5. Verdict for the adjacency axis

- **C1 (presence-only TB2 triage, blind labels):** no sibling holds TB2 grader classification or a blind-label oracle. TB2 adjacency is clean. The overlaps are *method* (tameshi mutation bar and cross-author confirmation; kaidoku freeze-integrity; kasegi forgery-class lessons) and a *homonym* (presence-only). Reuse, do not duplicate.
- **C2 (75-row tip-state ledger):** **real duplication with tameshi's `registry-check.py`** (executed rows, declared exit, scratch clone, `differs` verdict, 60 rows today). C2's row-existence leg duplicates kengaku's own `round52-c2` and souji's `registry-agreement`. C2's distinct content is the declared tip-state of each row and the red-row evidence fragment. The claim should state that as its delta against tameshi.
- **Lane-local naming:** `ledger-tip` (`SKILL.md:581`) and `tip-receipts` (`:586`) already occupy "ledger at tip" and "tip receipts". The new file name must be distinct, and the claim text must say how it relates to them.

Nothing here is absorbed into kengaku. Items 1, 3, 4, 8, 10, 12, 14, 15 and 16 of §2 are reported for the L1 to route.

## 6. Tool notes

- `tool: PROVINCE.md:353 exact grep returns 1,299 files outside kengaku; its two cited kumitate files return 0 lowercase matches` (one line, for the QA record).
- No tool install or upgrade in this seat.

## 7. Files

- Report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/R53ConnSiblings.md` (this file).
- Scratch: `/fast/scratch/hyaku/kengaku-r53/R53ConnSiblings/` — created for the exact-grep list, removed before yield.
