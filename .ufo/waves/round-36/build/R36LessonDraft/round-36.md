# Round 36 — a hardened package gate, and one more TB2 grader executed (2026-10-25, hyaku run 7)

Baseline `b662a5d6dd370491049e4206818373c61be44816`; frozen claims `plans/round-36-claims.md` (freeze
`3241b86cde0e9a3b9363a0d4c7fff12ec5d5f5e2`; Amendment 1 — pre-scoring probe repair, the `mkdtemp` path
normalised to `<tmp>` in the printed assertion text — `acbda2f3936838ba4849f14937fbecb8aed461e5`).
Controls scored red before any gate write, probe run or repair: `git log --oneline -3` at drafting time
reads `f9efce3` (wave-1 spec and dispatch), `acbda2f` (amendment 1), `3241b86` (freeze);
`.ufo/waves/round-36/claims/control-c1-nothing.txt` gives `unevaluated=14` with `plans/pkg_gate.py`
absent, `control-c1-legacy.txt` gives `LEGACY accepted=7/7`, `control-c2-nothing.txt` gives
`checks=6 defects=4`. Every number below that wave 1 has not yet measured is marked `<TBD at landing>`;
no landing-time result is asserted here.

## Gate

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| `knowledge/tb2-regex-log-grader.md` (C2) | **Admit-candidate** | Drafted in wave 1 (`build/R36EntryDraft/entry.md`); at freeze W3/W5 are red (`claims/control-c2-nothing.txt`: `checks=6 defects=4`). Admitted only when `python3 plans/round36_c2_verify.py --lane .` prints `checks=6 defects=0` on a clean clone of the landing tip — `<TBD at landing>`. Flip to refused: any W red at the landing tip, or a receipt/quote that does not re-run. |
| S108 `tests/test_outputs.py` @ `2fd12b88` | **Admit-candidate (mined)** | Opened 2026-10-25 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test_outputs.py`; quote, line 87: “matches = re.findall(pattern_text, log_text, re.MULTILINE)”; capture `corpus/evidence/round36/tb2-regex-log/test_outputs.py`, sha256 `345c3bd0…8f72`. The scored artefact is a regex file, and the expected nine dates are a literal list at lines 71-81 over a fixed 25-line log at lines 34-68. Flip: the capture's digest leaves the pin. |
| S109 `tests/test.sh` @ `2fd12b88` | **Admit-candidate (mined)** | Opened 2026-10-25 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test.sh`; quote, line 26: “echo 1 > /logs/verifier/reward.txt”; capture sha256 `4770437e…c334`. Binary reward from the pytest exit status at line 25. Flip: the capture's digest leaves the pin. |
| S110 `instruction.md` @ `2fd12b88` | **Admit-candidate (mined)** | Opened 2026-10-25 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/instruction.md`; quote, line 2: “If multiple dates are present in a line, the regex should match only the last date in that line.”; capture sha256 `4f7ac05e…f9c`. Line 4 forbids leading-zero octets; line 3 permits 29 February in every year. Flip: the capture's digest leaves the pin. |
| Assimilation: `considerthese/2026-10-25.md` proposal 2(c) (read 2026-10-25) | **Mined as a lesson / QUALITY criterion** | The proposal (§Self-improvement suggestions 2(c), `considerthese/2026-10-25.md:44-45`, line break and indentation normalised) asks for a tip-receipt validator: “includes a tip-receipt validator (every `corpus/evidence/**` receipt re-run and byte-compared), which would have caught D3 mechanically”. C1 realises the single-receipt half — `plans/pkg_gate.py --rerun` re-runs the spec's probe command and byte-compares the receipt — and C2's W5 realises it for the regex-log receipt. The every-receipt sweep over all of `corpus/evidence/**` is **not** built; the gap is stated in the QUALITY draft. |
| Package `grader-fixture-probe-stage3.md` (merge/kengaku, round 9) | `<scout verdict: R36ScoutMergePkg>` | Row-level screening only: its S170 is a lane own-work artefact (`lanes/kengaku/round9/toolathlon-grader-fixture-probe3.md`, not re-runnable here), but S171 is a real upstream module at a pin — `…/hkust-nlp/Toolathlon/9be8d8fe…/tasks/finalpool/academic-pdf-report/evaluation/main.py` — and the lane holds neither that path nor staged S143/S144 (`grep -c academic-pdf-report corpus/SOURCES.md` → 0; `grep -c 'S143' corpus/SOURCES.md` → 0 and `grep -c 'S144' corpus/SOURCES.md` → 0). Theme: measured verdicts per grader predicate, the same construct C2 executes. Flip to admitted: the scout reopens S171 at its pin, quotes it, and renames the entry's own-work half. |
| Package `grader-fixture-coverage.md` (merge/kengaku, round 8) | **Refused** | Its only source is S155, the lane's own stage-2 probe write-up (`lanes/kengaku/round8/toolathlon-grader-fixture-probe2.md`); no receipt for its counts exists in this lane, and a receipt is evidence only if something here re-runs it (`considerthese/2026-10-25.md` §Top lessons 3). Flip: an in-lane re-run of the stage-2 probe against `9be8d8fe` with the lane's own receipt cited. |
| Package `toolathlon-grader-behaviour-probe-2026-10-23.md` (merge/kengaku, round 6) | **Refused** | S130 is a campaign own-work locator (`lanes/kengaku/round6/toolathlon-grader-behaviour-probe.md` in shokuknow); §10 forbids the campaign tools, so the probe cannot be re-run from this lane, and the package's own denominator is one more than its rows support (see the erratum below). Flip: an equivalent probe re-run in-lane against `9be8d8fe` with the lane's own receipt, and the denominator corrected. |
| Package `terminal-bench-release-identity.md` (merge/kengaku, round 2) | **Refused** | Cites S100 and S092, both already in the registry with `used-by` = `corpus/knowledge/benchmark-verifier-execution-model.md`; it adds no coverage ground the lane does not hold (same reason as rounds 34 and 35). Flip: a release-identity fact no admitted entry states, with a located quote at the pin. |
| Package `grader-predicate-input-types.md` (merge/kengaku, round 7) | **Held (admit-candidate, not admitted)** | S143 is a real upstream module at its pin and the lane holds no row for it, but S144 is own-work and no round-36 claim opens S143; §10 forbids widening a frozen target. Flip: a claim that re-opens S143 at its pin and lands the amendment under renumbered ids. |

Erratum (round 36): S130's package (`corpus/evidence/round36/toolathlon-package.md`, byte copy of the merge/kengaku entry) states denominator 38, but its own outcome rows recount to 13 + 23 + 1 = 37 (callable 13, isolated-but-not-callable 23, exec failed 1), so the stated denominator 38 is one candidate larger than the rows it is divided into; either the missing candidate is named or every share is recomputed against 37.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| vacuous — frozen counters accepted junk | `corpus/lessons/round-35-verifier-spotcheck.md:86` ("`plans/round35_c1_verify.py` passes a stub probe plus one-word quotes; `plans/defect_ledger.py` D4/D5 accept labelled-but-false lines"); `plans/round35_hardening.py:10-15` (H1–H6, post-hoc and not a rule); red-before `.ufo/waves/round-36/claims/control-c1-legacy.txt` → `LEGACY accepted=7/7` | none — round 35 froze before any junk-package control existed; its pre-freeze skip-control re-dressed a round-34 draft instead of building the cheapest adversarial package | `plans/pkg_gate.py` (absent at freeze: `control-c1-nothing.txt` `unevaluated=14`) plus the frozen 14-fixture battery in `plans/round36_c1_verify.py`; H1–H6 promoted as pins, per-row quote parsing, teaches word floor, directional d4/d5 lines and a whole-tree clean check. Result `<TBD at landing>`. |
| reference-drift — the frozen probe was not byte-deterministic | `corpus/evidence/round36/regex-log-probe-first-run.txt:21-22` (the `invalid-regex` and `regex-file-absent` assertion texts carry `/tmp/tmp68j2v92s/` and `/tmp/tmp7c39pj0f/`); `plans/round-36-claims.md` §Amendment 1 | none — W5's "fresh run byte-equal to the receipt" was written before the first run, and the first run falsified it; two `mkdtemp` paths made every run unique | `plans/regex_log_probe.py:127` replaces the temp directory with `<tmp>`; W5 keeps the byte-compare, so a second drift fails the counter rather than being explained away. The `--dry` case table is byte-identical before and after (`corpus/evidence/round36/regex-log-dry-cases-freeze.txt`). |
| working-tree (round-34 D1; ledger `R35-D2`) / token-cooccurrence — a check that reads the working tree or mere co-occurrence | `corpus/lessons/round-35-verifier-spotcheck.md:87` ("D1 is a working-tree check, D4/D5 token co-occurrence"); `plans/defect_ledger.py` (`r34_d1` reads `git ls-files --others` over a subtree only; D4/D5 match patterns in text); ledger row `R35-D2` | none — round 34's D1 was narrowed to three paths and round 35's d4 pattern is a regex over one clause | the gate reads committed bytes (`git show <rev>:<path>`) and `--require-clean-tree` refuses any `git -C ROOT ls-files --others --exclude-standard` entry; `d4-line`/`d5-line` require each citation to be followed in the same clause by its own token, and d5's erratum must assert `is present` over a capture matching its manifest digest. Result `<TBD at landing>`. |
| scope — ledger rows split per opened round so the frozen older checker keeps passing | `corpus/defects.jsonl` (5 `R34-D*` rows, all `closed`, checks `r34_d1..d5`) beside `corpus/defects-round35.jsonl` (4 `R35-D*` rows, `opened_round: 35`, `status: open`); `plans/defect_ledger.py` requires `closed == len(rows)` over `defects.jsonl` and round 35 froze `rows=5 closed=5`; `plans/round-36-claims.md` "its check names and ids are frozen" | round-35 integrator: appending four open rows to the shared file would have broken the round-35 predicate, so the rows went to a file of their own | the split is kept but made explicit: ids and check names are frozen, a row changes in place only (`status`, `closed_round`, `recurrence_of`), and the round-36 counter reads the round-35 file and prints `rows=4 closed=4 observed_pass=4 mismatches=0` as its own label. A new open row in a file whose checker demands all-closed is the trap this row names. |

### Round-36 disposition of the six routed items (`corpus/lessons/round-35-verifier-spotcheck.md` §5)

| §5 item | round-36 disposition | measurement |
|---|---|---|
| 1. Frozen counters accept junk | **Closing (C1).** `plans/pkg_gate.py` + the 14-fixture battery; the junk-package control exists before freeze data this time (`claims/make-controls.sh`, `control-c1-accept-all.txt` `false_green=11`, `control-c1-reject-all.txt` `false_red=3`). | at freeze: `unevaluated=14` (gate absent) and `LEGACY accepted=7/7`; target `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0` — `<TBD at landing>`. |
| 2. D1 working-tree check; D4/D5 token co-occurrence | **Closing.** Committed-bytes reads, whole-tree untracked check, directional d4/d5 line fixtures (six of them, three must accept and three must reject). | ledger row `R35-D2`; counter label `r35_d2` prints `untracked_anywhere` and `line_fixtures_wrong` — `<TBD at landing>`. |
| 3. D2's roots are narrow (21 nested committed paths at `e7f0decd`) | **Closing.** The counter applies `^\.ufo/waves/round-3[0-9]/.*/\.ufo/waves/round-` to the branch tip rather than to three named roots. | at drafting time `git ls-tree -r --name-only master`, counted with `grep -cE '^\.ufo/waves/round-3[0-9]/.*/\.ufo/waves/round-'` → `21`; target `0` — `<TBD at landing>`. The 912 round-28 paths that match `/.ufo/waves/` but not the `round-3x` pattern are untouched, as the claims' limit states. |
| 4. Gate row omission (the Toolathlon package's 38 vs 37 denominator) | **Closed by this lesson's Gate section**, whose erratum line carries `S130`, the recount `13 + 23 + 1 = 37` from the committed copy and `denominator 38`; the package row also keeps the own-work locator reason. | `r35_d4` reads `corpus/lessons/round-36.md` and requires exactly one erratum line with all three parts — `<TBD at landing>`. |
| 5. S091 live leg (NEC returns a 418-byte denial from this host) | **Carried, not closed.** Any future claim resting on the page cites the committed capture and its digest, never live reachability; this draft makes no live claim. | round-35 spot-check §5 item 5; `corpus/lessons/round-34.md:45` erratum. |
| 6. SHONEN (for the operator) | **Carried, operator-owned.** No box is ticked by this round's scribes; the end-to-end-task box's non-author evidence is the C1/C2 re-run receipts, which are `<TBD at landing>`. | round-35 spot-check §5 item 6. |

## Census

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`.
Before (freeze): 15 W04, `kengaku ok`, exit 0 (`.ufo/waves/round-36/claims/census-before.txt`, 15 lines
plus the `ok` line; the 15 are duplicate-URL warnings on S040, S048, S057, S058, S059, S064, S065, S066,
S067, S068, S069, S071, S075, S076, S100).

At drafting time: registry rows
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `100`; knowledge files
`ls corpus/knowledge/*.md | wc -l` → `42`; README knowledge index rows
`grep -cE '^\| \`knowledge/[^\`]+\` \|' corpus/README.md` → `42`. S108–S110 add three rows and the entry
adds one knowledge file, so index parity becomes `43/43` only if both land together (`<TBD at landing>`).

After: `<TBD at landing>` — expected 15 W04 and exit 0 if the three new rows add no new duplicate URL;
the census reads the registry, not the lesson.

## Spot-check

`<TBD at landing>` — the non-author closure for this round is wave-2/next-round work. What it must check,
in the order that fails cheapest first:

1. `python3 plans/round36_c1_verify.py --lane .` on a **clean clone** of the landing tip (no untracked
   files) and record `FIXTURES …`, `rows=4 …`, `PREDICATE C1 …` verbatim.
2. `python3 plans/round36_c2_verify.py --lane .` and record `checks=6 …`, `PREDICATE C2 …`.
3. Re-run the gate against each of the six line fixtures by hand, to confirm the directional clauses hold
   outside the battery's own harness.
4. Confirm no gate check recognises a fixture by name, path or marker string — the wave-2 mutant seats
   attack this by renaming fixtures and rewriting comments.
5. Read the four ledger rows at the tip and confirm each `closed` row's check passes from committed bytes
   (`git show <rev>:<path>`), not from the working tree.
6. Re-read the Amendment 1 disclosure against `corpus/evidence/round36/regex-log-probe-first-run.txt` and
   confirm the amended probe still reproduces its receipt byte-for-byte.
