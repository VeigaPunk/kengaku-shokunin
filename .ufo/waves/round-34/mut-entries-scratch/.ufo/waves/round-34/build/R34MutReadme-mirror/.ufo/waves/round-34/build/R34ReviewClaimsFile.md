# R34 Review — frozen claims audit (round-34-claims.md)

Seat: R34ReviewClaimsFile (reviewer). Scope: audit `plans/round-34-claims.md` + the three
freeze receipts at `.ufo/waves/round-34/claims/` against the live lane and the round's draft
counter/mutation artifacts. All evidence commands are reproduced below with output.

## Verified-clean items (pass)

- Baseline/freeze history: claims name baseline tip `5022357cc69334e83b5a2f76c34daea440077a57`; git log shows
  `5022357` → freeze `adaf25dfd27dedfc1bf25f308576a6f2c8ad64ae` ("round-34: frozen prereg + controls…"), with the
  three receipts committed in the freeze. `git rev-parse HEAD` = `adaf25dfd27dedfc1bf25f308576a6f2c8ad64ae`.
- Registry rows: `grep -cE '^\| S' corpus/SOURCES.md` = **97**; `grep -cE '^\| S10[5-9] |^\| S11[0-9] ' corpus/SOURCES.md` = **0** (S105+ unused). Matches claim and control-c1 "registry rows count (expect 97)".
- Census-before: reran `./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` from the fleet root: **exit=0, 15 W04**, output byte-identical to `claims/census-before.txt` (`diff` clean; receipt ends `kengaku ok …/corpus/SOURCES.md`). Matches the claim's "census exit 0 with 15 W04". Note: the lane repo has no `scripts/` dir and no `shokunin.conf`; the written command only runs from the fleet root with the lane name as a positional arg — a documentation nuance, not a numbers mismatch.
- C1 control cat-file probes: `git cat-file -e adaf25d:corpus/knowledge/terminal-bench-task-grader.md` → exit 128; `…:plans/round34_c1_verify.py` → exit 128. Match control-c1 lines 3–6.
- C2 control probes: `git cat-file -e adaf25d:plans/round34_defects.py` and `…:plans/round34_mutate.py` → exit 128 each. Match control-c2 lines 3–6. The receipt's round-33 green claim is true today: `python3 plans/round33_defects.py --lane .` → `checks=6 defects=0` exit 0.
- C1 counter labels V1–V8 (`R34C1CounterDraft/round34_c1_verify.py`) line up with the predicate's eight V-checks (source ids, verified-at, row status/used-by, single index row, discharge sentence, frontier bullet, control receipt, SHA256SUMS), with the V7 mismatch described in F3.
- Frontier bullet is at README line 279 and its discharge text matches the claim's description.
- Knowledge index parity claim (41 files / 41 rows): `ls corpus/knowledge/*.md | wc -l` = 41; `grep -cE '^\|\s*`knowledge/' corpus/README.md` = 41.
- Collision guard output exists and is nonempty (`assimilation/collisions`, 21 staged/registry collisions), as the claim expects.
- Kill rules: C1's is unambiguous (quote-locateability, <3 survivors ⇒ honest stop). C2's is mostly unambiguous ("failing-before then green-after"; partial receipt or selftest alone not closure) but is not currently satisfiable (F1) and its mutant→check expectations conflict with the harness (F2).

## Numbered findings

### F1 (HIGH) — C2's own harness cannot run green on the clean tree; predicate unsatisfiable as built
The frozen C2 predicate requires `plans/round34_mutate.py` to print `MUTANTS total=8 detected=8`
exit 0 **and** "stays green on the clean tree". The current harness's recorded run
(`build/R34MutateDraft/harness-run.txt`) fails before any mutation:

```
CLEAN exit=1
DEFECT N3 round31-report-append-only-erratum: /tmp/…/clean/.ufo/reports/round-31/kengaku.md is unreadable
DEFECT N4 round32-report-closure-hash: /tmp/…/clean/.ufo/reports/round-32/kengaku.md is unreadable
DEFECT N7 round33-lesson-ledger-correction: round-33 lesson has no dated correction stating ledger sum 36+53=89
checks=8 defects=3
```

I reproduced this on the live tree: `python3 .ufo/waves/round-34/build/R34C2CounterDraft/round34_defects.py --lane .`
→ `checks=8 defects=3` exit 1 (N3/N4/N7). The clean baseline the hardened counter "must keep"
(control-c2: round-33 counter green, checks=6) is not kept by three of the new N-checks. The claim
gives no mechanism for these surfaces to heal — the round's listed work does not edit
`.ufo/reports/round-{31,32}/kengaku.md` or `corpus/lessons/round-33.md` (see F5/F6).

### F2 (HIGH) — harness mutant→check mapping targets files the mapped N-checks never read
`round34_mutate.py:141` assigns expected check labels: M4→N7, M6→N6, M7→N3, M8→N4. The mutants
touch different files than those checks read:

- M4 empties the SCORECARD `## Round 32` section (`round34_mutate.py:68-76`); N7 reads the round-33 **lesson**
  and `swarm-registry.json`, never SCORECARD. N2 (scorecard-round-sections) is what would fire, so the harness
  will print `UNDETECTED expected=N7` (it requires the expected label in the output).
- M6 rewrites `:78–81` → `:78– 81 ` in the **round-31** lesson (`:80-82`); N6 reads the **round-30** lesson
  (`check_n6`, LESSON30). N5 (round-31 lesson) only checks `:35-38`/`:39-40`, so neither N6 nor N5 catches M6.
- M7 prepends `a44b5a8`/`ae95fe0` junk to `.ufo/waves/round-31/falsify/*.md` (`:83-89`); N3 reads
  `.ufo/reports/round-31/kengaku.md`. Different path — N3 cannot fire.
- M8 appends `112091c` narrative to `.ufo/waves/round-32/falsify/*.md` (`:90-96`); N4 reads
  `.ufo/reports/round-32/kengaku.md`. Different path — N4 cannot fire.

So even after F1/F5's path fixes, four of eight mutants are configured to be undetectable by the
checks the harness demands. The four classes map to check pairs (N2/N7, N5/N6, N3/N4, N8) but the
mutants for the paired checks are aimed at the wrong surfaces, and the label list at `:141` hard-codes the wrong pairings.

### F3 (HIGH) — C1 V7 cannot pass against the committed control receipt
The counter's V7 (`round34_c1_verify.py:46`) requires the regexes `.*registry rows\s*=\s*97.*` and
`.*rows S105\+\s*=\s*0.*` inside `claims/control-c1.txt`. The committed receipt instead reads
`## registry rows count (expect 97)` / `97` and `## rows S105+ (expect 0, empty)` / `0` — no `=`
between label and number. Tested directly:

```
V7a registry rows = 97: False
V7b rows S105+ = 0: False
```

Running the draft counter on the lane prints `DEFECT V7: freeze control receipt values` among 7
defects (V1–V6 are expected pre-landing; V7 is not — it will still be red after C1 lands unless the
receipt text is amended or the regex loosened, both of which contradict the receipt being frozen
"committed at freeze").

### F4 (MED) — claims describe control-c1 contents that are not in the file
The claims text says control-c1 contains "git cat-file -e for the entry and **each new row** fails
(exit 128) … and the counter on the pre-tree prints `checks=8 defects=8` and exits 1". The actual
receipt has only the entry probe and the `round34_c1_verify.py` probe (no S105/S106/S107 probes), and
the counter pre-tree line is a prose comment — "counter on pre-tree (simulated via absence probe above;
real counter does not exist)" — with no `checks=8 defects=8`/exit output. The claim's description of
its own control does not match the committed artifact (the same class of control-prose-vs-receipt drift
the freeze claims it was addressing).

### F5 (MED) — N3/N4 point at lane-relative report paths that do not exist in the lane
`round34_defects.py:12-13` sets `R31_REPORT = Path(".ufo/reports/round-31/kengaku.md")` etc.
(relative). The lane tracks only `.ufo/reports/round-17/kengaku.md`; `ls .ufo/reports/round-31/`
fails (dir absent). The round-33 counter this replaces used fleet-root absolute paths
(`round33_defects.py:40-42`: `FLEET / ".ufo/reports/round-31/kengaku.md"`, which exists at
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-31/kengaku.md`). The re-derivation silently changed
the surface from fleet-root to lane-relative, making N3/N4 permanently red unless the round creates
lane-local report copies — which the claims never list (the claim's surface list is "SCORECARD,
lessons, wave trees", and `.ufo/reports/…` is absent from it).

### F6 (MED) — N7 cannot be satisfied without editing a historical lesson
`check_n7` requires a dated correction in `corpus/lessons/round-33.md` matching
`36\s*\+\s*53\s*=\s*89` or `36 build.*53 falsify.*89`. The lesson says "Wave-1 build: 36 seats;
wave-2 falsify: 53 seats; total **89**." (line 48) with no "+" or "build…falsify" phrasing on one
line; the dated-correction requirement also fails (`grep` + harness N7 defect confirm). The claims only
promise to address the "lesson header seat-count wording" in the **round-34** lesson, not to amend the
round-33 lesson, so N7 has no planned path to green.

### F7 (LOW) — separability statement overstates isolation from C1
The claim says C2's counter reads "no artifact C1 creates (SOURCES rows S105–S109, knowledge entries,
README rows)". But N8 (`check_n8`) scans `corpus/knowledge/*.md` and `corpus/README.md` index rows —
exactly the two artifact classes C1 produces (its entry file and its single index row). No dedicated
fixtures are shared, but the landed-tree surfaces overlap; the sentence as written is false, and the
practical guarantee holds only if C1's landed state is consistent before/while C2's checks run.

### F8 (LOW) — mutant-count prose ambiguity
Frozen prose says the harness "applies one mutant per class", but the predicate requires `MUTANTS
total=8` with four classes (2/class). The check-pair mapping (N2/N7, N5/N6, N3/N4) implies two mutants
per class; "one mutant per class" is at best imprecise. Combined with F2, the correspondence between
the 8 mutants and the classes/checks is not determinable from the claim alone.

### F9 (LOW) — red-before receipts are weaker than the claim's "failing-before then green-after"
Four receipts exist under `.ufo/waves/round-34/falsify/red-before/` (one per class) and each honestly
documents a naive-probe blind spot (e.g., width-newline: `grep -n ':35-38' corpus/lessons/round-31.md`
→ no match, exit 1, with an explicit note that "sandbox-export mutations … were not executed"; token-cooc
uses a synthetic string fixture, not the lane tree). They demonstrate the classes, but they do not show
the round-34 counter going red on a mutation, and no green-after run exists anywhere yet (F1's clean-red
prevents it). The kill rule's "shown failing-before then green-after" standard is therefore not yet met
by the committed evidence.

### F10 (LOW) — "committed SHA256SUMS"/"committed proof fixture" are not in the freeze commit
C1 V8 says captured evaluator bytes match "the committed SHA256SUMS", and the id-guard proof fixture is
claimed "committed under `.ufo/waves/round-34/assimilation/`". At review time the freeze commit
`adaf25d` contains only the three claims receipts; `assimilation/captures/tb2-eval/SHA256SUMS` and
`assimilation/id-guard-proof.txt` are untracked (`git status` shows `.ufo/waves/round-34/assimilation/`
as `??`). The wording anticipates a later landing commit; as frozen, the objects V8 depends on do not
exist in git. (V8's `_sums_valid` does pass against the on-disk capture.)

## Residual risk / verification gaps
- The final landed counter/harness are not yet in `plans/`; drafts were reviewed. If F1/F2/F3/F5/F6
  are fixed during the wave, the predicate may become satisfiable — but no fix path exists in the
  claims text, and the frozen receipts cannot be amended without breaking "committed at freeze".
- C1's V5/V6 discharge/frontier regexes are looser than "verbatim" (presence of clause fragments, not
  byte equality); low severity, noted as part of F3's family.
- I did not validate the captured TB2 evaluator bytes against the pinned upstream commit (read-only
  source access to GitHub not exercised); only the internal SHA256SUMS consistency was checked.

## VERDICT: review-claims findings 10
