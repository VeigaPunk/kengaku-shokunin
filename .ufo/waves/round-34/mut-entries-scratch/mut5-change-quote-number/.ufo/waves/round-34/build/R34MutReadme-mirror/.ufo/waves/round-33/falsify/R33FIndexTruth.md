# R33FIndexTruth — falsify: README index row + coverage/frontier bullets for `benchmark-grader-semantics.md`

Seat: `KengakuR33.R33FIndexTruth` (leaf; no subagent dispatch, no background jobs).
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Access date: **2026-10-25**.
Report path: `.ufo/waves/round-33/falsify/R33FIndexTruth.md` (the only lane path written by this seat).
No tools installed. No lane/fleet file mutated; git usage read-only (`log`, `show`, `cat-file`, `merge-base --is-ancestor`, `status`, `diff`, `ls-tree`, `rev-parse`), all scoped to the lane. Scratch: `/tmp/r33fit_rows*.txt`, `/tmp/r33fit_files.txt` (< 10 KiB).

## 0. Tree state observed (re-derived, not assumed)

- Current tip: `77ac8c1307ba60e9572a7e2789b71ae31b133440` (`git rev-parse HEAD`).
- `git status --porcelain -- corpus/README.md` → empty; `git diff HEAD --stat -- corpus/README.md` → empty. All README verdicts below are committed-tree verdicts.
- The only commit reachable from HEAD that touches `corpus/README.md` after the build seats' observed tip is `b54feca` ("round-33: admitted grader semantics and re-probed catalogs", 3 hunks = lines 67/255/279). **`2b4cef2` — the tip the build seats (R33IndexTruth §0, R33FrontierText §0) recorded as "HEAD" — is NOT an ancestor of HEAD** (`git merge-base --is-ancestor 2b4cef2 HEAD` → exit 1). The build seats' byte-level verdicts transfer (see F5), but their commit attribution is a lineage erratum.
- `b54feca^:corpus/README.md:67` ids: `S094, S097, S093`; `:279`: `round 32 … S097` — the pre-patch state; `b54feca` landed the S103/S104/round-33 text now at the tip.

## 1. Acceptance checks (frozen C1 surface: plans/round-33-claims.md:49 "the entry has exactly one index row in `corpus/README.md`")

### V1 — exactly one index row: HOLDS

```
$ grep -c '^| `knowledge/benchmark-grader-semantics.md`' corpus/README.md
1
$ grep -n 'benchmark-grader-semantics' corpus/README.md | cut -c1-60
67:| `knowledge/benchmark-grader-semantics.md` | Toolathlon's ab-testing grader
255:- **Benchmark grader semantics**: covered at source-code depth (round 33, 20
279:  - *Partly discharged round 33 (2026-10-25):* `knowledge/benchmark-grader-s
```

The entry string occurs exactly 3× in the whole README (row :67, coverage bullet :255, frontier sub-bullet :279) — unanchored, so no duplicate row under any indentation exists anywhere in the file. Row↔file parity: `grep -o '^| `knowledge/[^`]*`' corpus/README.md | sort` vs `ls corpus/knowledge` → **41 rows == 41 files, name-sets identical** (`diff` clean after stripping the leading `| `). The +1 over the frozen 40/40 is exactly C1's new entry (see F2).

### V2 — entry title/ids in the row: HOLDS

Row `:67` (verbatim): title cell = "Toolathlon's ab-testing grader is a deterministic state comparison (record.csv vs expected_ratio.csv at the executed 0.05% tolerance; its log-bucket check mixes fail-open exceptions with fail-closed credential absence) and the LLM-as-judge survey frame: meta-evaluation is its own part"; citation cell = "S103 (Toolathlon @ 9be8d8fe), S104 (arXiv 2412.05579v2); S093 restated from the verifier-execution entry".

- Ids match the entry's own `source:` lines exactly (S093/S103/S104, three distinct, `verified-at: 2026-10-25` — read from `corpus/knowledge/benchmark-grader-semantics.md`).
- Ids match the registry anchors: S103 = commit `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`, `tasks/finalpool/ab-testing/evaluation/main.py` (SOURCES.md:118); S104 = arXiv 2412.05579v2 (SOURCES.md:119); S093 = commit `66f92766…` (SOURCES.md:112).
- The row's "S093 restated" wording matches the entry's own `## S093 — restated, not repeated` section; the description cell's fail-open/fail-closed clause matches the entry's credential-path reading (`main.py:176`, `:216-218`, `:234-235`).
- Registry cells (python extraction over SOURCES.md): S093/S103/S104 all `status=mined` (cell 7), `opened 2026-10-25` (cell 8), `recheck 180d` (cell 9), `used-by` (cell 10) naming `corpus/knowledge/benchmark-grader-semantics.md`; S093's used-by lists **both** entries (verifier-execution + grader-semantics).

### V3 — coverage bullet :255: HOLDS

Full line read (`:255:raw`, 802 chars): names the entry, `S093, S103, S104`, "Discharges the round-31 frontier clause \"and for Toolathlon\" for the one task whose evaluation script is read (Toolathlon `ab-testing/evaluation/main.py` @ `9be8d8fe`)", and closes with the same scope negatives the entry's §What this does not establish states ("Not runtime task validity (PROVINCE refuses it), not contamination measurement, not deployment config."). No second coverage bullet mentions the entry (grep: only :255).

### V4 — Frontier says only one Toolathlon task is discharged: HOLDS

Frontier `:279` (verbatim, full line): "*Partly discharged round 33 (2026-10-25):* `knowledge/benchmark-grader-semantics.md` reads **the one Toolathlon task** whose evaluation script this lane opens (`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`) and the LLM-as-judge survey frame (S104). The \"and for Toolathlon\" clause is discharged **for that one task's scoring code only**; the clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's; any SWE-bench Pro V2 grader beyond the round-31 task-level one) and for runtime task validity…".

- Cross-check against captures: the round-33 capture set holds exactly one Toolathlon *task* evaluation script (`toolathlon-ab-testing-evaluation-main.py`); the second Toolathlon capture is `utils/evaluation/retry.py` — a repo-level utility, not a task's evaluation script, so "one task" is accurate, not undercounted.
- Every other Toolathlon mention in README is an open-clause or spec-only mention, not a discharge: :276 (instruction, unopened leads), :277 (round-29: Toolathlon-Verified as checklist-artefact source only), :278 (round-31: clause "stays open … and for Toolathlon"), :359 (round-28 block: "Toolathlon … primary specifications … remain open"). No bullet claims a second discharged Toolathlon task.
- The entry's own §What this does not establish bounds the claim to the ab-testing family — consistent.

### V5 — canonical counting commands reproduce the frozen line: HOLDS

```
$ python3 plans/adoption_check.py --expect .ufo/waves/round-33/claims/adoption-expect.json --census
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok
adoption_exit=0
$ python3 plans/round33_c1_verify.py --lane .
checks=8 defects=0
c1_exit=0
```

Both byte-identical to the frozen predicate's expected outputs (claims.md:50-52). `adoption-expect.json` pins exactly `{"path": "corpus/knowledge/benchmark-grader-semantics.md", "sources": ["S093", "S103", "S104"]}`.

### V6 — the entry's README line citations hold: HOLDS

Entry cites the instruction phrase at `corpus/README.md:276` and the clause "and for Toolathlon" at `:278`. Verified in bytes: :276 contains "the primary specs and scoring code for Terminal-Bench 2.0, Toolathlon, and SWE-bench Pro"; :278 contains "and for Toolathlon". (This **corrects build seat R33IndexTruth F3**, which claimed the entry cites :276 for the "and for Toolathlon" clause — it cites :276 for the instruction phrase and :278 for the clause; both anchors are exact.)

## 2. Findings by severity

- **F1 (minor, residual, UNCAUGHT by both counting commands): frontier bullet `:279` never names `S103`.** R33ReadmePatch §4 required the discharge recorded "under S103"; its recommended AFTER text inserts `, S103` after `` `9be8d8fe`) ``. The committed line (current tip `77ac8c1`) names the path+commit and S104 but the id token `S103` is absent: `sed -n '279p' corpus/README.md | grep -c 'S103'` → `0`. The discharge remains traceable to S103 by document identity (the commit pin `9be8d8fe` in the same line is S103's), so this is a text-level omission, not a registry divergence — but it is exactly the deviation build seat R33IndexTruth F1 flagged, and it is still unfixed. Why uncaught: `plans/round33_c1_verify.py` `check_v4` reads **only** index rows (`raw.startswith(f"| \`knowledge/{name}\`")`, count != 1 → defect) and no v1–v8 check reads :255 or :279; `plans/adoption_check.py`'s `indexed` counter is per-entry boolean (docstring: "entries with a `| \`knowledge/<name>.md\` |` row"), so `indexed=1` cannot see duplicates or any bullet text. **No counting command enforces any coverage/frontier bullet byte.** Verdict: uncaught (by counters) / caught by this falsify seat; limitation of the C1 receipt.
- **F2 (claims-file erratum, confirmed): the frozen preamble's "40 files, 40 index rows" is stale.** Measured at the named baseline `112091c`: `git show 112091c:corpus/README.md | grep -c '^| `knowledge/'` → 41; `git ls-tree -r --name-only 112091c corpus/knowledge | wc -l` → 41; `git cat-file -e 112091c:corpus/knowledge/benchmark-grader-semantics.md` → exists. The round-32 draft and its index row predate the freeze, so the baseline was already 41/41. The frozen predicate itself is unaffected (it requires exactly one row *for the entry*, which holds); the narrative figure is wrong. Matches build seat R33IndexTruth §2.
- **F3 (claims-file erratum, confirmed): the freeze control does not print `entries=0`.** plans/round-33-claims.md:58 says the control "prints `entries=0 …` and exits 1"; the committed `.ufo/waves/round-33/claims/control-nothing.txt` records `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=1 usedby_ok=0 census=ok` / `exit=1`. The control still fails as required (exit 1, `usedby_ok=0`), but the frozen record misstates its observed line. Matches R33ClaimsReview's C1 finding; independently confirmed here.
- **F4 (claims-file erratum, confirmed): "S093's `used-by` gains the entry" is a false transition.** plans/round-33-claims.md:49; at the freeze commit `f0b20aea`, S093's used-by cell already read `corpus/knowledge/benchmark-verifier-execution-model.md, corpus/knowledge/benchmark-grader-semantics.md` (`git show f0b20aea:corpus/SOURCES.md`). The required final state holds (V2/V5); only S103/S104 are new rows. Matches R33ClaimsReview.
- **F5 (build-seat lineage erratum): the README patch landed in `b54feca`, not `2b4cef2`.** `git merge-base --is-ancestor 2b4cef2 HEAD` → exit 1 (not an ancestor); `b54feca` is an ancestor and its diff is the 3-hunk :67/:255/:279 patch from the S094/S097/round-32 state. `diff <(git show 2b4cef2:corpus/README.md | sed -n '255p;279p') <(sed -n '255p;279p' corpus/README.md)` → identical, so the build seats' byte-level verdicts transfer to the current tip despite the wrong commit label.
- **F6 (counter-strength note): `adoption_check`'s `indexed=1` alone is not uniqueness evidence.** It counts *entries having a row*, not rows per entry; the uniqueness proof is `c1_verify` v4 (`len(rows) != 1`) plus this seat's direct grep (V1). A duplicated row would still fail v4, so the conjunction is sound; recorded so no one cites `indexed=1` alone as the exactly-one-row proof.

## 3. Verdict

The three acceptance checks all **hold** at the current tip `77ac8c1`: entry title/ids exact (V2), exactly one index row with 41=41 parity (V1), and the Frontier discharges exactly one Toolathlon task (V4). The falsification attacks on the frozen C1 README surface **did not land** — no duplicate row, no stale id, no over-broad discharge claim survives scrutiny. Real residuals are F1 (the `S103` token omission in :279, uncaught by both counting commands — the only committed README defect found) and the frozen-claims narrative errata F2–F4, all previously build-flagged and here independently confirmed with commands and outputs.

Residual risk / verification gaps: neither counting command reads any coverage/frontier bullet byte, so future drift in :255/:279 is invisible to the frozen receipts (F1 is the live instance); this seat did not re-verify the S103/S104 quote bindings or capture digests (other seats' scope: R33FReceiptMismatch, R33C1KillRule findings stand); the `2b4cef2` lineage anomaly (a non-ancestor commit that build seats recorded as HEAD) is reported, not explained — the integrating L1 should confirm which commit it intended.

## L1 integration correction

README frontier line `:279` was updated after this seat's snapshot to name S103 and S104 explicitly; the current line cites the one Toolathlon task at `9be8d8fe` and the pinned survey frame. The 41/41 baseline correction and frozen control/S093-delta errata remain as reported.
