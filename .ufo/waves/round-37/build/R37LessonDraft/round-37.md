# Round 37 — advertised gate classes made demonstrable, and a third TB2 grader executed (2026-10-26, hyaku run 8)

Baseline `3ea9a1d9005cc07d0a5ce69f4ebf53a81fbcecdd` (the round-36 verifier spot-check); frozen claims
`plans/round-37-claims.md` (freeze `ca790460e9b74d4dc5870c878affd13cc9c4437a`; first recorded probe run
`5c7b34e9223f460a440596e3a76bdae8bfdd37d8`). Ancestry checked at drafting with
`git merge-base --is-ancestor`: baseline → freeze → probe run → wave-1 dispatch `44b7298a`, all exit 0.
Controls are red before any battery fixture beyond the API example and before any recorded probe run:
`control-c1-nothing.txt` (`BATTERY fixtures=14 wrong=0 renamed_disagree=0`, `MUTANTS total=55 killed=5
survived=50`, `PREDICATE C1 fail`, exit 1), `control-c2-nothing.txt` (`checks=7 defects=4`, V2/V3/V4/V7 red),
`control-c1-gate-edited.txt` (`invalid=55`), `control-c1-mislabel.txt` (`wrong=1`) and the one-fixture
example `control-c1-example.txt` (M08 alone). The eleven frozen digests in
`.ufo/waves/round-37/claims/frozen-digests.txt` all equal the bytes at the freeze commit — `git show
ca790460:<path> | sha256sum`, 11/11 `MATCH` — so the round-36 number-drift class does not recur in this
freeze. Landing-time predicate numbers below are `<pending: integrate>`; every other open number names the
seat that owes it.

## Gate

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| `knowledge/tb2-git-webserver-grader.md` (C2) | **Admit-candidate (held, not landed at drafting)** | The entry is not in `corpus/knowledge/` at drafting — `ls corpus/knowledge/*.md \| wc -l` → `43`, the round-36 count — and the draft is `build/R37PkgDraft/entry.md` (rows at `build/R37PkgDraft/sources-rows.md`). What it will rest on is already frozen and executed: a 22-case offline probe with `cases=22 observed_pass=9 observed_fail=13 mismatches=0` (`corpus/evidence/round37/git-webserver-probe.txt`), predictions written before the first run (`git-webserver-dry-cases-freeze.txt`), and I recomputed the join at drafting: same 22 ids in the same order, 9 `predicted=pass`, 0 disagreements. At freeze the counter is `checks=7 defects=4`. The headline the entry buys: a file served on :8080 with no repository, hook or push passes, because `verify.sh:49` never reads the expect step's status; and a body containing `TEST PASSED` passes while `verify.sh:66` prints `TEST FAILED`, because `test_outputs.py:13` is a substring test over stdout that echoes the body. Flip to admitted only on `checks=7 defects=0` then `PREDICATE C2 pass`, exit 0, on a clean clone of the landing tip; flip to refused on any V red there. |
| S111 `tests/test_outputs.py` @ `2fd12b88…` | **Held (mined; row absent at drafting)** | Opened 2026-10-26 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/tests/test_outputs.py`; `sed -n 13p` of the capture reads `assert "TEST PASSED" in result.stdout, "Did not pass test"` (9 words). Capture `corpus/evidence/round37/tb2-git-webserver/test_outputs.py`, sha256 `526aee3d…46b37` (matches `SHA256SUMS`). Re-opened live at the pin 2026-10-26 by `R37ReopenPins`: `IDENTICAL test_outputs.py` and `test_outputs.py: OK` under `sha256sum -c` (`build/R37ReopenPins/reopen-verify.txt`). `grep -n "S111" corpus/SOURCES.md` → 0 at drafting; the row is drafted at `build/R37PkgDraft/sources-rows.md` and lands with the entry. Flip: the capture's digest leaves the pin. |
| S112 `tests/verify.sh` @ `2fd12b88…` | **Held (mined; row absent at drafting)** | Opened 2026-10-26 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/tests/verify.sh`; `sed -n 57p` reads `HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/hello.html)` (7 words). Capture sha256 `1dc44c92…3d05`. The stdout this script prints is the whole input to the assert; the body it echoes is what makes `TEST PASSED` reachable. Re-opened live 2026-10-26 by `R37ReopenPins` (`IDENTICAL verify.sh`, `verify.sh: OK`). Flip: the capture's digest leaves the pin. |
| S113 `instruction.md` @ `2fd12b88…` | **Held (mined; row absent at drafting)** | Opened 2026-10-26 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/instruction.md`; `sed -n 9p` reads `then I see the output "hello world".` (8 words). Capture sha256 `62151b73…1d97`. Lines 1-6 ask for a clone, a commit and a push; lines 7-9 ask for the file on :8080 — the two halves the probe separates (`static-file-no-git` passes, `no-server` fails). Re-opened live 2026-10-26 by `R37ReopenPins` (`IDENTICAL instruction.md`, `instruction.md: OK`). Flip: the capture's digest leaves the pin. |
| `tests/test.sh` @ `2fd12b88…` (captured) | **Captured, not a row** | It is harness plumbing, not this task's scoring predicate: `uvx -p 3.13 … pytest … /tests/test_outputs.py` at :14-18 and the pytest exit status turned into `/logs/verifier/reward.txt` at :21-22 — the same `exit → reward file` mechanism already admitted for this pin as S109 (regex-log `tests/test.sh:26`). A row would duplicate coverage ground the registry holds, and would not state how this task is scored. Captured at `corpus/evidence/round37/tb2-git-webserver/test.sh`, sha256 `afafc3ff…5895`; cited in the entry's provenance, not the registry. Flip: a task whose reward mapping differs from the pytest-exit pattern. |
| `task.toml` @ `2fd12b88…` (captured) | **Captured, not a row** | Manifest metadata, not a scoring predicate: `timeout_sec = 900.0` for verifier and agent, `docker_image = "alexgshaw/configure-git-webserver:20251031"`, `allow_internet = true`. The one fact that matters to a claim — internet and `apt-get` are available in the real environment, which the probe's sandbox lacks — is used as a named limit in the entry, not as evidence of behaviour. sha256 `ebb40d72…4751b`. Flip: a claim about environment isolation that needs the manifest as its source. |
| `solution/solve.sh` @ `2fd12b88…` (captured) | **Captured, not a row** | The oracle is an agent solution, not the grader, and the frozen probe never runs it (claims §C2, named limit: "it never runs the oracle or a real git push, so it does not show that the intended path passes"). A row would dress the oracle as evidence for an execution that did not happen. sha256 `c31cd92e…3a62`; the pre-run reading did include it, which is why predictions are predictions. Flip: a claim that executes the oracle end to end. |
| Assimilation: `considerthese/2026-10-25.md` proposal 2(a) (read 2026-10-26) | **Mined as a lesson; one third built** | Proposal 2 (`considerthese/2026-10-25.md:39-45`) asks for one persistent routed-defect ledger whose checker "(a) re-runs every closed defect's check at tip forever". 2(a) is realised this round by `R37LedgerTip`: at tip `44b7298ae1e03791173097cef0e898285f238870` it re-runs all nine closed rows and prints `rows=9 closed=9 observed_pass=9 mismatches=0` (`build/R37LedgerTip/ledger-tip-run1.txt`). 2(b) — blocking pre-registration when a class recurs twice — and 2(c) — every receipt re-run and byte-compared — are **not** built: the lane still splits `corpus/defects.jsonl` (5 rows) from `corpus/defects-round35.jsonl` (4 rows), and round 36's own eight lesson mistakes never became ledger rows (`grep -rl "R36-D" corpus/ plans/` → empty), so 2(a) re-runs nine of the lane's defects, not all of them. |

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| reference-drift / transcription — anchor digests that do not resolve: one hex digit dropped (S110) and four rows whose digest matches no committed capture or manifest (S070, S072, S073, S074) | `corpus/lessons/round-36-verifier-spotcheck.md:71`: "the row's anchor sha256 is 63 hex digits (`4f7ac05e70cf922ea0f…`) … so the counter cannot catch it"; §5 item 1 at `:88` | the round-36 non-author spot-check (a seat the lane dispatched) — no counter of that round read S110's anchor | two moves this round, one demonstrated. General sweep: `R37AnchorSweep` (`build/R37AnchorSweep/anchor_digest_check.py`) over the lane as it stands prints `rows=103 tokens=11 defects=5` — S110 `digest-short detail=63-hex` plus S070/S072/S073/S074 `digest-unknown` (`build/R37AnchorSweep/fixture-receipt.txt`, `CASE F0-lane-as-is`) — and `defects=0 exit=0` once the erratum and the four captures are staged (`CASE F2-erratum-plus-captures`). The sweep's own matrix is not green yet: `M1`/`M2` print `WRONG` although their id and class sets match, because `fixture_matrix.py:138` sets `want = len(expect_ids)` while the checker prints one line per defect — three lines for one id cannot equal one. So the sweep's receipt is `<pending: R37AnchorSweep>`, and the four `digest-unknown` rows are new routing. C2-local: `plans/round37_c2_verify.py:108-119` (V3) requires each of S111-S113 to carry exactly one `sha256 <64 hex>` equal to its spec pin, and I showed it able to fail at drafting: on a scratch clone with the three rows and exact digests, `v3 ok=True rows=3 bad=0`; with S111's digest short by one hex character, `v3 ok=False rows=3 bad=['S111:anchor_digest']` (`build/R37LessonDraft/v3-falsifier.txt`). **Not yet closed:** the round-37 baseline still carries the bad cell — `corpus/SOURCES.md:125` reads `sha256 4f7ac05e…2e96f9c` (63 hex), and `grep -o "sha256 [0-9a-f]*" corpus/SOURCES.md \| awk '{print length($2)}' \| sort \| uniq -c` shows `1 63` beside `8 64`. A routed item and its fix in the same round is progress, not closure: the sweep must land before this row can say closed. |
| vacuous — the frozen round-36 battery demonstrated 5 of the 55 advertised gate classes | `.ufo/waves/round-37/claims/control-c1-nothing.txt` (`MUTANTS total=55 killed=5 survived=50 invalid=0 null_detected=0`; M01 M05 M40 M47 M54 killed, the other 50 `SURVIVED`); the round-36 counter printed `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0` at `7d1fa691` | none — the round-36 battery was built from a junk list, not from the gate's clause list; the round-36 spot-check routed "gameable" (§5 item 2) without counting survivors | `plans/battery37/*.py`: one single-branch fixture per survivor, each declaring its exact `DEFECT` set, plus the counter's renamed run (a gate must not key on a fixture's name). At drafting the wave's receipts carry a `killed by=` line for all 55 ids: P2/P3 6/6 (M02-M08, `build/R37BatP23/receipts/`), P4 4/4 (M09-M12), P5 7/7 (M13-M19), P6 8/8 (M20-M27), P7 6/6 (M28-M33), P8 5/5 (M34-M38), P9/P10 4/4 (M39, M41-M43, `build/R37BatP910/receipts/dev-run.txt`), D4 3/3 (M44-M46), D5 7/7 (M48-M53, M55) — 50 new plus the frozen 5. That is per-seat evidence, not the predicate: the single admissible total is one `MUTANTS total=55 killed=55 survived=0` line from a clean clone, `<pending: integrate>`. |
| order-of-operations — the C2 skip-control executed the frozen probe before the first recorded run | `plans/round-37-claims.md:3-10` (disclosure): the skip-control's P10 clause "executed the frozen probe once inside a scratch clone at control time"; `control-c2-skip.txt` keeps only `P10 DEFECT fresh probe output is not byte-equal to the receipt` | the claims header itself — self-disclosed at freeze; no seat's receipt records the discarded execution | the discarded run cannot become evidence and the disclosure is the right shape, but the write-up must not be the only artefact. The probe was at its frozen digest `63cb75cf…5eedf` before that run and is re-pinned every run by C2 V5 (digest + `--dry` byte-equality) and by V2's `P10` fresh-run compare, so a hand-typed receipt is caught; the first recorded run is `5c7b34e9` and the second run's byte-equality is `<pending: R37ProbeRerun>`. Rule forward: a control that executes a frozen instrument keeps the run as a receipt. |
| derived-number — two different totals are readable from the wave's own receipts for the same mutant id | `build/R37BatP5/receipt-primary-counter.txt` (`MUTANT M13 P5 killed by=p5-manifest-absent …`, `MUTANTS total=7 killed=7`) beside `build/R37BatP5/receipt-removal-table.txt` (`MUTANT M13 P5 SURVIVED …`, `MUTANTS total=7 killed=6 survived=1`) and `build/R37BatP8/receipts/p8-ablation.txt` (`killed=0 survived=1`); a grep for `killed by=` over `build/` counted 51 ids at 01:44 and 55 at 01:46 as the last seat's receipts landed, while the per-seat primary blocks sum to 50 new + 5 frozen | none — the wave has no canonical receipt index; each seat writes its own runs, and ablation runs are the falsifier that the fixture is load-bearing | the agreement above is a property of a complete wave, not of the format, and it moved while I measured it. Rule the lesson records: the only admissible C1 number is the frozen predicate line measured on a clean clone; a per-seat number is quoted from that seat's primary block and labelled as such, never by grepping `killed by=`. |

| count — a fixture matrix measured its expectation in ids while the checker answered in lines | `build/R37AnchorSweep/fixture-receipt.txt` `CASE M1-erratum-wrong-correction … defects=3/1 … WRONG` and `CASE M2-correction-not-in-manifest … defects=2/1 … WRONG`, whose `expect ids=S110` and observed classes match; `build/R37AnchorSweep/fixture_matrix.py:138` `want = len(expect_ids)` | none — the mismatch is invisible in the printed receipt (both `n` and `want` are small integers) and only the code shows why | the sweep must declare defects per line, or count distinct ids in its output, before its `ok`/`WRONG` column can be read; until then the receipt is `<pending: R37AnchorSweep>`. Same class as the gate's distinct-quote vs distinct-line counters: a count is only meaningful with its unit named. |

Note on a gate property the battery had to absorb (not a mistake): silencing one branch changes the
observable *set*, not always one id — `build/R37BatP23.md:50` records M04 moving `(1, {P3,P4})` to
`(1, {P4})`. A single-defect fixture therefore declares every clause id its branch prints, which is why
the counter's kill criterion is the pair (exit code, clause set).

### Round-37 disposition of the seven routed items (`corpus/lessons/round-36-verifier-spotcheck.md` §5)

| §5 item | round-37 disposition | measurement |
|---|---|---|
| 1. S110 anchor digest truncated (63 hex) | **Carried, fix built but not landed.** `R37AnchorSweep` (the census's 15 warnings are all duplicate-URL lines, none about a digest); C2 V3 covers S111-S113 and was shown able to fail. | at drafting `corpus/SOURCES.md:125` still 63 hex; the sweep finds **five** unresolvable anchors (`F0` `defects=5`) and clears to 0 only with the erratum and four staged captures (`F2` `defects=0 exit=0`); V3 pair in `build/R37LessonDraft/v3-falsifier.txt`; sweep receipt `<pending: R37AnchorSweep>` |
| 2. Frozen battery gameable and clause-incomplete | **Closing (C1).** Frozen 55-mutant list, one single-branch fixture per survivor, renamed run required by the counter. | freeze `killed=5 survived=50`; drafting `killed by=` for 55 of 55 ids across nine seats; aggregate predicate `<pending: integrate>` |
| 3. The C2 counter admitted a junk package | **Closing (C2).** V2 runs the package gate with its quote-support clauses (verbatim on the cited line, distinct, 3-25 words, ≥8 lines); V3 pins anchors; V7 ties every requirement-map label to an executed verdict. The skip-control is built at freeze and is red. | `control-c2-skip.txt`: `V2 DEFECT gate_exit=1`, `V3 ok rows=3 bad=0` with the *right* digests, `checks=7 defects=1`, exit 1 — junk quotes now fail V2; `<pending: integrate>` for the landing run |
| 4. Wave-1 round-36 findings not absorbed (R36CritScope F3–F6, F8, F10; two non-independent probe cases; anchor drift) | **Carried to a seat.** `R37R36Absorb`. | `<pending: R37R36Absorb>` |
| 5. Amendment 1 ruling on the L0 queue | **Carried, operator-owned.** No claim this round depends on the ruling. | `.ufo/l0-questions.md` |
| 6. Spot-check debt (round-36 `## Spot-check` "Pending"; items 3-4 unexecuted) | **Partly answered.** Item 4 (fixture-name keying) is now mechanical: the counter re-runs every fixture under another directory name and prints `renamed_disagree`. Item 3 (hand-run the line fixtures) is this round's `## Spot-check` item 4. | `BATTERY … renamed_disagree=0` in every receipt quoted here |
| 7. SHONEN (for the operator) | **Carried, operator-owned.** No box ticked by this round's scribes. | `SHONEN.md` |

## Census

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`.
Before (freeze): exit 0, `kengaku ok`, 15 W04 — duplicate-URL warnings on S040, S048, S057, S058, S059,
S064, S065, S066, S067, S068, S069, S071, S075, S076, S100 (`.ufo/waves/round-37/claims/census-before.txt`:
15 W04 lines, then `kengaku ok /…/corpus/SOURCES.md`, then `exit=0`). The set is the same as round 36's: no new duplicate.

At drafting time: registry rows `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`
→ `103`; knowledge files `ls corpus/knowledge/*.md | wc -l` → `43`; README index rows
`grep -cE '^\| `knowledge/[^`]+` \|' corpus/README.md` → `43`. S111-S113 add three rows and the entry adds
one knowledge file, so index parity must hold at `106/44/44` when both land together — the state C1's
genuine fixture is sensitive to (claims §Separability): at drafting both are absent, which is one of the
two consistent states.

After: `<pending: integrate>` (`.ufo/waves/round-37/integrate/census-after.txt`).

## Spot-check

Pending — the non-author closure for this round follows the report (LEARNING.md: a seat the lane dispatched
is still the lane). Cheapest failing check first:

1. `python3 plans/round37_c1_verify.py --lane .` on a **clean clone** of the landing tip (no untracked
   files) and record `BATTERY …`, `MUTANTS …`, `PREDICATE C1 …` verbatim. One command; fails loudest.
2. `python3 plans/round37_c2_verify.py --lane .` and record `checks=7 …`, `PREDICATE C2 …`.
3. `grep -nE 'k36-|p23-|p4-|p5-|p6-|p7-|p8-|d4-|d5-|git-webserver' plans/pkg_gate.py` → expect empty:
   no gate path may name a fixture, a battery module or this round's evidence.
4. Hand-run one mutant outside the counter: apply one frozen `old → new` replacement to a scratch copy of
   `plans/pkg_gate.py`, run it on that mutant's fixture by hand, and confirm the clause set moves. This is
   the check round 36's spot-check left unexecuted (§5 item 6) — it proves the counter is not the only thing
   that can see the branch.
5. Recompute the probe's prediction/observation join from committed bytes: parse `CASE` ids from
   `corpus/evidence/round37/git-webserver-dry-cases-freeze.txt` and `…-probe.txt`, require the same 22 ids in
   the same order, 9 `predicted=pass` vs 9 `observed=pass`, and 0 disagreements (my drafting run: exactly
   that). Then read every `match=NO` id and confirm the entry names it.
6. Anchor sweep by hand: `grep -o "sha256 [0-9a-f]*" corpus/SOURCES.md`, keep only 64-hex tokens, and compare
   each with the capture it cites; the S110 63-hex cell must be gone.
7. Re-open S111-S113 live at the pin: `curl -s <url> | sha256sum` equals the row anchor, and `sed -n <line>p`
   equals the row quote. Three rows, three digests.
8. Re-read the claims' disclosure (`plans/round-37-claims.md:3-10`) beside `control-c2-skip.txt` and confirm
   the probe digest was frozen before the discarded run (`frozen-digests.txt`).
9. Confirm no `corpus/` or `plans/` copy, and no lane mirror, sits under `.ufo/waves/round-37/build/`
   (`find .ufo/waves/round-37/build -maxdepth 2 -name corpus -o -name plans`).

## Close (appended at closure)

Wave 2 (falsifiers: re-run both counters, re-open S111-S113 live, mutate the battery and the C2 counter,
re-read the entry and this lesson) has no committed spec at drafting (`.ufo/waves/round-37/` holds `build*`, `claims/`, an `integrate/`
whose receipts have begun to appear, `make_build_spec.py` and `make_falsify_spec.py`; no falsify spec). Consequences stated rather than softened: (1) the `## Gate` verdicts above are
`Admit-candidate` and `Held` precisely because nothing had landed when this draft was written — the C1
predicate and the C2 counter are unrun at the landing tip (`<pending: integrate>`); (2) the C1 fix is 55 of
55 mutants demonstrated in per-seat receipts, not yet one aggregate run, so the predicate line itself is
`<pending: integrate>` and a full-battery run can still surface a `wrong>` or `renamed_disagree>`
declaration error that no per-seat run showed;
(3) the S110 anchor defect the round-36 spot-check routed is still in the registry at this baseline, so its
row above says carried, not closed; (4) the six captures were re-opened live at the pin by `R37ReopenPins` (six `IDENTICAL`, `sha256sum -c`
exit 0, commit `2fd12b88…` recomputed), so the *bytes* are independently confirmed — but the three
`## Gate` rows are still `Held` because no row text exists in `corpus/SOURCES.md` at drafting, and no
non-author seat has checked the row quotes I sed-verified.
