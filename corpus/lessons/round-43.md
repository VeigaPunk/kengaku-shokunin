# Round 43 — nine near-variants killed with value-attributed kills; a ninth TB2 grader that imports the agent's module into its own interpreter (2026-10-26, hyaku run 9)

L1 `KengakuR43` (planner seat). Frozen claims `plans/round-43-claims.md` (freeze `02753f26`, first recorded probe run
`6b49694d`); baseline lane tip `317148c4` (the round-42 non-author spot-check). Wave 1 dispatched at `d33350fd` (38 seats).
Written by the L1 at integration from the wave-1 reports named in each row.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **A conditional Gate refusal whose flip fired at landing and was never executed** (mined from round 42, closure D3) — the round-42 Gate refused `Dockerfile` "if the entry keeps the `WORKDIR /app` sentence … admit" and the landed entry kept the sentence and made it load-bearing; no row was opened and no line recorded the flip. A sweep finds the shape everywhere: 45 flip obligations in 18 lessons, none ever resolved. | `corpus/lessons/round-42.md:44`; `corpus/lessons/round-42-verifier-spotcheck.md:37-42`, `:92`; sweep `.ufo/waves/round-43/build/R43FlipCheck/sweep.txt` (`FLIPS total=45 unresolved=45` over 18 lessons) | none — no instrument read a lesson's flip conditions (`grep -rn "Flip check" corpus plans` → nothing before this round) | `plans/gate_flip_check.py` (seat `R43FlipCheck`): red on the landed round-42 lesson (`FLIPS total=2 unresolved=2`, exit 1, `R43FlipCheck/runs.txt`), green after the two `Flip check (round 43): …` lines were appended (`unresolved=0`), `--selftest` `ok=19/19`; criterion **Q35**; the Dockerfile flip executed as tier-B row S135. This round's own two fired flips (feal `Dockerfile`, `feal.py`) were executed at landing as S136/S137 (§Gate). |
| **An anchored edit applied with line numbers from a stale view** — while adding a stage-check leg to the C2 probe before the freeze, the L1's edit replaced lines 127–137 of `plans/feal_probe.py` (the `EXIT_ZERO`/`CLOCK_SEED` attack texts) instead of the harness block those numbers had named in an earlier read. | L1 session, 18:44 -03; the damaged block was visible in the edit response and restored before any run; the frozen probe (`17d694ba…`) is the repaired file | `--stage-check` would have: the replaced attack text no longer byte-compiles (`STAGE attack compiles=NO`, exit 4) | re-read the region before every anchored edit of an instrument that is about to be frozen; stage-check and `--dry` are re-run after the last edit and their outputs committed with the freeze (`claims/c2-stage-check.txt`) |
| **A freeze control whose own content was wrong** — the first `control-c2-informed-filler` run printed `BROKEN`: its `content` mirror quoted `srand(time(NULL));` for `cheat-clock-seed`, one word, so V10 (≥2 words) refused it. The counter was right; the control was not. | `claims/c2_filler_control.py` first run (L1, 18:52 -03): `CONTROL content V10 DEFECT … cheat-clock-seed:feal.c:60 quote not on the line`, `CONTROL-C2-INFORMED-FILLER BROKEN` | the control's own `red-as-required`/`BROKEN` verdict | the content mirror now quotes `feal.c:65`; committed control prints `red-as-required` |
| **A counter's answer key shipped inside the counter** — V10's frozen `DECISIVE` map is plain text in `plans/round43_c2_verify.py`, so a filler that copies the first decisive line per case from the counter source passes V10 without reading a capture. | `.ufo/waves/round-43/build/R43CritClaims.md` §1 (copycat filler: `V9 ok`, `V10 ok`, exit 0) | none — the freeze control tested only fillers built from the receipt | not fixed (the counter is frozen); named as a limit of C2's admission basis and routed: a content leg whose key is not readable from the instrument (e.g. a non-author seat's blind mechanism table compared after the fact) |
| **Counter fences narrower than their stated purpose** — R4's "a fixture repo must stay rooted at its own directory" passes a `.git` FILE pointing at an outside git dir and skips repos deeper than three levels; leg i is bypassed by an absolute `--receipt` spelling or argparse abbreviation. | `R43SentinelCounter.md` F1 (separate git dir: `FIXTURE esc-gitdir-outside … ok`), F2 (depth cap `:475`), F3; `R43CritC1Counter.md` V2′ (absolute argv) | the hostile controls test the named vectors only | not fixed (frozen counter); no landed battery43 fixture uses these shapes (`grep -iE 'separate-git-dir|gitdir|include\.path|alternates|symlink'` over `plans/battery43/*.py` → nothing); routed to the round-44 counter with red controls |

The round-42 wave-2 route-mix mistake did not recur: `.ufo/waves/round-43/make_build_spec.py` asserts the m_flash
share (≥½) and the attack share (≥¼) before writing a spec; the attack assert fired once while the spec was drafted
(`attack share 9/37 below a quarter`) and the wave was re-shaped before validation (closure R6, shown able to fail).

## Gate

Opened or captured this round. Access date 2026-10-26 for every row; times are -03. The L1 fetched all twelve files of
the task directory at 18:40 -03 (`corpus/evidence/round43/tb2-feal-differential-cryptanalysis/` + `SHA256SUMS`); seat
`R43PkgRows` re-fetched the six row candidates at 19:07:25–26 -03, six `200`, six `cmp` identical
(`.ufo/waves/round-43/build/R43PkgRows/refetch.txt`); the L1 re-fetched `Dockerfile` and `feal.py` at 19:18 -03 (`200`,
`cmp` identical). Quotes are ≤25 words and located at the cited line of the capture. Base URL
`https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-differential-cryptanalysis/`.

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| S129 `tests/test_outputs.py` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>tests/test_outputs.py`, opened 18:40, re-fetched 19:07:25. Quote, `test_outputs.py:30`: "assert feal_in_c.get_keys()[5] == stolen" (4 words); sha256 `585780e7…9631a3d`. The whole score: build the extension (`:20`), append `/app` then `/tests` to `sys.path` (`:22-23`), import the agent's module (`:24`) and the reference (`:25`), call, compare. Flip: digest leaves the pin. |
| S130 `instruction.md` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>instruction.md`, opened 18:40, re-fetched 19:07:25. Quote, `instruction.md:3`: "Your attack should run in less than 30 seconds" (9 words); sha256 `b4093780…fd722572`. Two of its clauses are ungraded (time, technique). Flip: digest leaves the pin. |
| S131 `tests/feal_module.c` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>tests/feal_module.c`, opened 18:40, re-fetched 19:07:26. Quote, `feal_module.c:52`: "Get the current keys as a list of 6 32-bit values" (11 words); sha256 `1ae1c8a3…a3379363`. The exported `get_keys` is the answer any module imported beside it can read. Flip: digest leaves the pin. |
| S132 `tests/feal.c` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>tests/feal.c`, opened 18:40, re-fetched 19:07:26. Quote, `feal.c:66`: "key[i] = (x * 1234567) & 0xFFFFFFFF" (7 words); sha256 `bd4e9fb3…7073e885`. Clock-seeded schedule (`:56-67`), Feistel core (`:71-95`). Flip: digest leaves the pin. |
| S133 `tests/test.sh` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>tests/test.sh`, opened 18:40, re-fetched 19:07:26. Quote, `test.sh:26`: "echo 1 > /logs/verifier/reward.txt" (4 words); sha256 `106c2739…77f72daf`. Reward = pytest exit status (`:25-28`). Flip: digest leaves the pin. |
| S134 `README.md` @ `2fd12b88` | **Admitted (mined, tier A)** | `<base>README.md`, opened 18:40, re-fetched 19:07:26. Quote, `README.md:35`: "Confirms the attack completes within the time limit" (8 words); sha256 `887407c7…5cb24e7f`. Admitted for that falsifiable sentence (`slow-oracle-45s` passes; nothing times the call). Flip: digest leaves the pin. |
| S136 `environment/Dockerfile` @ `2fd12b88` | **Admitted (mined, tier B) — a refusal whose flip fired** | Drafted as a refusal by `R43PkgRows` with the flip "if the landed entry cites the image at all, admit it as a tier-B mechanism row"; the landed entry cites it (`:69-71`, `:95`, `:149`). `<base>environment/Dockerfile`, re-opened by the L1 19:18:18 (`200`, 220 bytes, `cmp` identical). Quote, `Dockerfile:6`: "RUN pip install setuptools==80.9.0" (4 words); sha256 `c40553e4…f356a30`. No graded predicate; the environment the predicate assumes. |
| S137 `environment/feal.py` @ `2fd12b88` | **Admitted (mined, tier B) — a refusal whose flip fired** | Same flip shape ("if the landed entry cites this file"); the entry cites it (`:70-71`, `:209`, `:245`, `:248`). `<base>environment/feal.py`, re-opened 19:18:19 (`200`, 1951 bytes, `cmp` identical). Quote, `feal.py:27`: "x = random.randint(0, 0xFFFF)" (4 words); sha256 `23cc077b…d2885dfe`. The agent's copy keyed from Python `random`, never the graded cipher. |
| S135 `circuit-fibsqrt/environment/Dockerfile` @ `2fd12b88` | **Admitted (mined, tier B) — round-42 flip executed** | Round-42 closure R2/D3. Re-opened by seat `R43GateRowsR2` 19:10:24 (`200`, 321 bytes, `cmp` identical to `corpus/evidence/round42/tb2-circuit-fibsqrt/Dockerfile`). Quote, `Dockerfile:3`: "WORKDIR /app" (2 words); sha256 `780c2398…0483d3d4`. Cited by the appended block of `tb2-circuit-fibsqrt-grader.md`. |
| `task.toml`, `setup.py`, `solve.sh`, `feal.h`, `SHA256SUMS` @ `2fd12b88` | **REJECT — captured, not rows** | `task.toml` is metadata read once (`:22` "timeout_sec = 1800.0", 3 words); `setup.py` is the build recipe `:20` shells; `solve.sh` is the oracle end state (an input to the probe); `feal.h` declares the C API; `SHA256SUMS` is the capture inventory. Flip: an entry sentence that rests on one of them alone. |
| Assimilation set (`merge/kengaku/`, 65 staged entries, 175 staged rows) | **REJECT — none adopted** | Package bytes unchanged since 2026-10-24 (`R43MergeRescreen.md` §1: three sha256 equal round 42); id collisions 45 (0–3-space guard proven on an indented `  | S002 |` fixture, §2); quarantine slice S091/S105 refused (payload-absent, §3); no staged entry touches this round's surfaces (feal/cryptanalysis greps empty, §4). Flip: the package changes, or a staged entry lands on uncovered PROVINCE ground with a collision-free renumber. |

Flip check (round 43): Dockerfile — fired — the landed entry cites `Dockerfile:4` and `:6` (tb2-feal-differential-cryptanalysis-grader.md:69-71, :149); admitted as S136
Flip check (round 43): feal.py — fired — the landed entry cites the shipped feal.py (:70-71, :209, :245, :248); admitted as S137
Flip check (round 43): task.toml — not fired — no entry sentence rests on task.toml, setup.py, solve.sh, feal.h or SHA256SUMS alone
Flip check (round 43): merge/kengaku/ — not fired — merge/kengaku unchanged (R43MergeRescreen §1) and no staged entry on this round's surfaces
Flip check (round 44): task.toml — fired — the landed entry rests on `task.toml:22` alone (finding 11, `:299-302`, "it is the only time bound the grader's environment actually carries"; also `:41`, `:122`, Mechanism row `:240`); admitted as S147 (tier B), entry errata E3/E4
Flip check (round 44): solve.sh — fired — the landed entry rests on `solve.sh:90` alone (Mechanism row `:230` quotes "if (c1l ^ c2l) == 0x02000000:", finding 2 `:251-252`, finding 12 `:306`); admitted as S148 (tier B), entry errata E5/E6

Gate prose: the six spec-pinned rows (`plans/pkg-spec-r43.json` `rows` = S129–S134) are tier A; S135–S137 are tier B
mechanism rows added by executed flips, not by the spec. Registry 121 → 130. The census and the anchor check are green
with all nine rows present (`sources-census.sh validate --file corpus/SOURCES.md` exit 0, 15 `W04`; `anchor_digest_check.py
--lane . --evidence-ref index` → `rows=130 tokens=36 defects=0`).

## Routed

From `corpus/lessons/round-42-verifier-spotcheck.md` §5:

- **R1** entry errata — landed: `## Errata (round 43, closure R1; …)` appended to `corpus/knowledge/tb2-circuit-fibsqrt-grader.md`
  (seven items, E1–E4 the four `F42EntryQuotes` sentences, re-derived by `R43ErrataFibsqrt`), and the receipt-pointer
  correction appended to `corpus/lessons/round-42.md`. Nothing above either append edited.
- **R2** Gate record — landed: S128's Gate row inside the round-42 Gate table (one added line), the Dockerfile flip
  executed as S135 + the appended entry block, two `Flip check` lines; mistake → Q35 + `plans/gate_flip_check.py`.
- **R3** durable queue — landed: 41 wave-2 rows (`R42-R3-01…41`, `R43RoutedQueue`) + 3 rows and two field changes
  (`R43R42Defects` §2 D) in `corpus/routed-findings.jsonl`; rows this round closes are closed only after the clean-clone
  observe (SCORECARD round 43).
- **R4** C1 counter soundness — the round-43 counter (claims C1): R1–R4 from `F42C1Hardened`, value attribution g,
  symlink h, order-argv i, each with a red control; the round-42 "these two tools run no fixture code" sentence is
  corrected by name in `plans/round-43-claims.md` §C1.
- **R5** C2 content leg — V10 (claims C2), with the limit in §Mistakes row 4.
- **R6** hygiene — generator asserts (above); the envelope's PATH-dir digest now covers content
  (`claims/envelope.sh`); `R43ReviewEnvelope` measured 3/4 change kinds caught — a mode-only change and a rewrite of a
  mode-000 file are missed (routed).

Round-42 wave-2 doc defects: corrections appended to `corpus/lessons/round-42.md`, `corpus/QUALITY.md` (Q33/Q34) and
`SCORECARD.md` (`R43R42Defects`: 20 of 22 corrected, 3 refuted as the reviewer's own off-by-ones, each with evidence).

considerthese: `considerthese/2026-10-26.md` proposal 3 ("Batch the TB2 grader sweep … class histogram") — the
screening half run statically by `R43ConsiderThese`: 89/89 pinned task graders classified into 11 classes by what the
decisive assertion reads; the lane's nine reads cover 6 classes; largest uncovered class F1 constant-compare (14 tasks,
0 read). The histogram is the round-44 coverage selector (`.ufo/waves/round-43/build/R43ConsiderThese/hist.md`).

## Census

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`: before
exit 0, `kengaku ok`, 15 `W04` (`.ufo/waves/round-43/claims/census-before.txt`); after: see
`.ufo/waves/round-43/integrate/census-final.txt`. Registry rows 121 → 130 (tier A +6, tier B +3); knowledge files 49 → 50.

## Falsifiers run in wave 1 (other seats' reports, not re-run here)

- C1: battery43 42 fixtures over 7 modules, every module from its own seat, each mutant killed by ≥4 fixtures
  (L1 trial run, `MUTANTS total=9 killed=9 … unattributed=0`, hits 4–11); no module resembles the freeze direction
  module (difflib ratio ≤0.19); `R43CritC1Counter` 9 dishonest vectors blocked; `R43CritValueLeg` spurious 0, vacuous
  0/9, trace divergence 0; `R43RevSiteStable` verdict stable over 18 runs (jobs, seeds, roots); `R43RevMutRows` 9/9 rows,
  0 adv misquoted; `R43CritEquiv` equivalents 0, incidental 0, `u = 18` unmutated advertised behaviours.
- C2: `R43PytestParity` real pytest 8.4.1 under `uvx -p 3.13`: 12/12 verdicts equal the receipt; `R43CritIndep`
  re-derived 12/12 from the captures + 3 own cases as predicted; `R43CritProbe` 1 defect (clock-seed's 10 s window);
  `R43CritClaims` 3 defects (the V10 copycat above among them).

## Mistakes added by the L1 at close

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **A round closed under the operator's seat floor** — the round ran one 38-seat wave; the 33-seat falsify wave was specified and validated (`.ufo/waves/round-43/falsify-spec.json`, `falsify-dispatch.json`, validator `spawn=33`) but never dispatched, because the run's request budget ran out while wave 1's last two seats were still open. Round total 38 < 64 (run-9 directive "64–128 seats in total, every round"). | `.ufo/waves/round-43/build-results.json` (38 results); no `falsify.ready` in `.ufo/waves/round-43/` | none — nothing gates the round total before filing | the next round dispatches wave 1 sized ≥64 as one v2 wave, or writes the wave-2 `.ready` before integrating wave 1 so the falsify wave never depends on the integration finishing; the wave-2 attack list stays committed as round-44 input |
| **Two wrong sentences landed in the new entry and one in PROVINCE** — the `## Regrade` paragraph describes the round-42 harness (`TEST`/`REGRADE` tags, one process calling twice) and the PROVINCE paragraph counts "a ninth pass". | entry `## Errata (round 43, L1 self-review …)` E1–E2; `PROVINCE.md` tail erratum | the L1's own re-read after landing (no wave-2 review ran) | appended errata, nothing edited in place; a seat-drafted prose block is diffed against the frozen probe's harness before landing |
