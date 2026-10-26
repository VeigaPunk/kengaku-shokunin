# Round 42 — a calibration battery whose kills must be attributed; an eighth TB2 grader whose answer is a gate list run by a compiled simulator (2026-10-26, hyaku run 9)

L1 `KengakuR42` (planner seat). Frozen claims `plans/round-42-claims.md` (freeze `bc856d8`, first recorded probe run
`523b278`); baseline lane tip `d69452c` (the round-41 non-author spot-check). Drafted by wave-1 seat `R42LessonDraft`;
`<L1 fill>` marks the landing numbers this seat cannot observe (wave-1 batteries and the entry not yet integrated).

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **A declared direction copied from a table instead of re-derived from the run** — XO5 and XO6 are `rc-mirror` (the mutant is *stricter*: reference exits 0, mutant 1), but the round-40 near-variant table labels both `rc-silence`, and the same table's own §2 records the opposite result. | `.ufo/waves/round-40/falsify/F40XMutLedgerOrder/xmut_driver.py:113` (`("XO5", "order", "-", "rc-silence"`) and `:121` (XO6), beside the same rows' witness prose `:116-117` and `:125-126` — "reference ORDER ok rc=0, mutant ORDER HIT rc=1" (8 words); the summary table carries it verbatim (`F40XMutLedgerOrder.md:70-71`) while §2 measures `the reference scans commits=1 and PASSes; the mutant … FAIL rc=1` (`:120-125`). The round-41 wave-1 scout re-printed the label unchanged (`R41PlanNext/near40_survivors_only.txt:40-41`, ids at `R41PlanNext.md:59`). | None at the time: the round-40 table was never frozen, so QUALITY Q29 (a direction witnessed before the freeze) did not bind it; `plans/round-42-claims.md` §Frontier names this row as the round's mined mistake, captured by Q29 applied only in round 42. | Re-derive both from the run, not the table: `rc-mirror` (`plans/round42_c1_verify.py:201,206`; definition `:44` "fixture `expect=accept`, reference exits 0, mutant exits 1"), witnessed by `claims/witness-run.txt:29-30` — `XO5 … rc-mirror killed by=w-xo5-post-receipt-blob attributed=L117`, `XO6 … w-xo6-p10-pass-line attributed=L53`. **Shown able to fail:** `claims/control-c1-direction-mislabel.txt` restores the two round-40 labels (`control-c1-direction-mislabel.patch`) and the frozen counter prints `MUTANT XO5 order rc-silence SURVIVED exhibits=0>1,rc-mirror` (`:29-30`), `MUTANTS total=14 killed=12 survived=2` (`:33`), `PREDICATE C1 fail` (`:37`, `exit=1`) — the two corrected labels are the only difference between 14/14 and 12/14. |
| **A kill credited to a fixture that did not produce it** — X2 X4 X5 X11 are recorded as "killed by battery40", but the killing fixture is a clone of the whole lane, and every defect the mutants print lands on a lane row, never on the row the fixture adds. | `.ufo/waves/round-42/build/R42CritEquiv.md` §4: `plans/battery40/a_bind.py:83-105` builds `a17` as `ctx.clone(d / "lane")`; re-run `R42CritEquiv/probe_a17.txt` → `REF rc=0 defects=0`, `X2 rc=1 defects=3 [(S036…),(S114…),(S124…)]`, `X4/X5` one `S110` defect each, `X11` two lane rows; and `probe_none.txt` (two-row repo, no clone) → all four differ from nothing. | Round-41 closure R1 asked for the soundness residuals; this round's C1 leg f (attribution) is the mechanical answer, and `R42CritEquiv` §4 is the audit that found the provenance gap. | A kill counts only when a traced re-run reproduces the result **and** executes a line of the replaced span, and every fixture is built from nothing (`plans/round42_c1_verify.py` docstring leg f; battery contract "No lane clone is offered"). **Shown able to fail:** `claims/control-c1-attribution.txt` forces the attributed span to line 1 → `killed=0 unattributed=14`, `PREDICATE C1 fail`. The four round-40 rows stay excluded on substance (they are non-equivalent and killable from nothing), corrected in the record, not relabelled. |

Named limits carried with these two rows (measured this wave, no fix claimed):

- **Class-only kills.** X6 and X7 change only which class is printed; both directions keep rc=1 (measured
  `R42CritEquiv/probe_lbl.txt`: `REF rc=1 classes=[digest-wrong-capture, digest-unknown]`, `X6 rc=1 classes=[digest-unknown,
  digest-unknown]`, `X7 rc=1 classes=[digest-wrong-capture, digest-wrong-capture]`). The `silence` direction is defined on
  class sets (`exhibits()`), so the kills are legitimate, but an operator reading only rc sees no difference — and one
  repo carrying both a sibling-digest row and a made-up-token row kills both mutants at once (`R42CritEquiv` §2.1).
- **An `indirect` adv cell is a strictness kill, not a demonstration of the quoted sentence.** XO6's `adv` cell quotes
  `plans/order_check.py:52-53` (the `gate: ` echo prefix) while the mutation widens the verdict alternation with `PASS`;
  the live gate prints only `ok`/`DEFECT` (`plans/pkg_gate.py:301`), so the fixture must forge `P10 PASS`. The freeze
  discloses the one `indirect` cell; the kill should not be read as evidence about `:52-53` (`R42CritEquiv` §2.3, §3 row k).
- **The witness-as-battery loophole from round 41 persists**: a copy of the freeze modules into `plans/battery42`
  satisfies the predicate (`claims/control-c1-witness-as-battery.txt`, `PREDICATE C1 pass`), so a kill records a result
  difference in the declared direction, not authorship; the battery may not read the witness modules and non-author
  review stays part of admission.

Round-40's `--work` traceback class did not recur: both round-42 counters create `--work` before use, and the C2 counter
prints `receipt unreadable` rather than crashing on an absent receipt (`claims/control-c2-nothing.txt`).

## Gate

Opened or captured this round. Access date 2026-10-26 for every row; times are -03. Quotes are ≤25 words and located at
the cited line of the capture.

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| S125 `tests/test_outputs.py` @ `2fd12b88` | **Admitted (mined, tier A)** | Opened by the L1 2026-10-26 17:08 -03 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/circuit-fibsqrt/tests/test_outputs.py`; re-fetched cmp-identical 17:20:09 and 17:24:14 -03 (`.ufo/waves/round-42/build/R42PkgRows/refetch.txt`: three `200`, three `cmp=IDENTICAL`). Quote, `test_outputs.py:23`: "assert line_count < 32000" (4 words); sha256 `6117b8ed…0438`. This is the whole score: existence, a line count over *all* lines, and 28 fixed inputs each run as `/app/sim N` against `fib(isqrt(N)) % 2^32` after a `gcc -O3 /tests/sim.c -o sim` in the cwd (`:65-67`, `:119`). Flip: the capture's digest leaves the pin in `plans/pkg-spec-r42.json` (`rows.S125`). |
| S126 `instruction.md` @ `2fd12b88` | **Admitted (mined, tier A)** | Opened 2026-10-26 17:08 -03 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/circuit-fibsqrt/instruction.md`; cmp-identical re-fetch 17:20:09, 17:24:14 -03. Quote, `instruction.md:8`: "the first 32 lines are defined by the binary representation of stdin" (12 words); sha256 `a7f50026…b9ea`. The probe falsifies the interface in two places: `sim.c:324` takes the value from `argv[1]` (stdin is never read), and `instruction.md:9`'s "the last 32 lines" is not what is printed — `sim.c:340-347` prints the 32 highest-indexed signals (case `lookup-28-reversed-lines` passes). Flip: digest leaves the pin. |
| S127 `tests/sim.c` @ `2fd12b88` | **Admitted (mined, tier A)** | Opened 2026-10-26 17:08 -03 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/circuit-fibsqrt/tests/sim.c`; cmp-identical re-fetch 17:20:09, 17:24:14 -03. Quote, `sim.c:335`: "for (int step = 0; step < 32000; step++)" (9 words); sha256 `700645ac…6173`. The graded-state deciders live here: `parse_gates("gates.txt")` is cwd-relative (`:319`), lines that do not scan as `outN = op` are skipped (`:113-115`), and the printed integer is the high-index register window (`:340-347`). Flip: digest leaves the pin. |
| `README.md` @ `2fd12b88` | **REJECT — captured, not a row** | Capture `201f7c88…4cbd`. It is the task's own narrative restatement of the same three artefacts and carries no predicate of its own: every checkable sentence it makes is already anchored to S125/S126/S127, and it is not shipped into the image (`Dockerfile:9-10` copies only `tests/sim.c` and `gates.txt`; `test.sh:18-22` runs `/tests/test_outputs.py`). Quote, `README.md:10`: "The provided `sim.c` simulator reads this file and simulates the circuit for 32,000 time steps." (15 words). Reason for refusal: a tier-A anchor on documentation no check reads would age silently and add no statement the entry can cite that its three siblings do not already carry. Flip: an entry statement that **only** README supports (the skills framing or the declared resource envelope), or a README sentence that diverges from the tests — either makes it a documented-vs-executed row. |
| `Dockerfile` @ `2fd12b88` | **REJECT — captured, not a row; one claim flagged** | Capture `780c2398…d3d4`. Refused for the same reason as README, with one exception the entry must settle: the entry's cwd paragraph and the `fake-sim-script` case rest on `Dockerfile:3` — "WORKDIR /app" (2 words) — because `test_outputs.py:66` writes `./sim` while `:119` runs `/app/sim`, and `test.sh:13` guards only `PWD = /`. Flip: if the entry keeps the `WORKDIR /app` sentence (its draft cites `Dockerfile:3` in its own tables), admit `Dockerfile` as a **tier-B mechanism row**; the cheaper alternative is to drop the sentence and describe the case as conditional on the grading cwd. |
| `test.sh`, `task.toml`, `SHA256SUMS` @ `2fd12b88` | **Captured, not rows** | `test.sh` (`4770437e…c334`) is the pytest→reward mechanism (`uvx -p 3.13 -w pytest==8.4.1 …`, `:18-22`); `task.toml` (`9f5aa1f7…0972`) is author metadata and the declared envelope (`timeout_sec = 3600.0`, `:22`/`:25`), read only, never exercised — the image is never pulled; `SHA256SUMS` (`36b15d5b…2edf`) is the capture inventory that pins all nine files, not a source. Flip: an entry statement that needs the reward mapping, a declared timeout, or a file identity as its source. |
| `solve.sh`, `gates.txt` @ `2fd12b88` | **Captured, not rows** | `solve.sh` (`a4ffab41…5d0b`) is the oracle end state, run as the `oracle-solve-sh` case (`PPP`) — an input to the probe, not a source of an entry statement; the entry's draft marks it tier C and rests no finding on its logic. `gates.txt` (`032786f9…ad29`) is the shipped example circuit and the seeded state of the `nop` case (`PPF`, it prints `N/2` as `instruction.md:10` says). Flip: an entry sentence about the oracle's construction or the example's exact output. |

Gate prose: the three admitted rows are exactly the three the spec pins (`plans/pkg-spec-r42.json` `rows` = S125, S126,
S127; `raw_base` = the `circuit-fibsqrt/` tree at the pin). The registry coupling is measured: with the rows present and
the entry absent, `sources-census.sh validate` exits 1 with exactly three `E11` lines for this entry's `used-by`
(`R42PkgRows.md` §3.1); with the entry present, `CENSUS_EXIT=0`, `E=0 W=15`. `anchor_digest_check.py --evidence-ref
index|head` on a clone carrying the rows prints `rows=120 tokens=27 defects=0`, every new row binding by `url-task` to
its own capture. The admission of tier A is for these three files at this commit, nothing about TB2 as a whole.

The falsified sentences are the round's sharpest Gate result: the instruction's interface (stdin, "last 32 lines") is
wrong about the graded machine, and its two worked examples are not graded inputs — `lookup-28` prints 0 for both 208
and 20000 and still passes 3/3 (receipt `fibsqrt-probe.txt:6`; `cases=16 observed_pass=7 observed_fail=9 mismatches=0`,
`regrade cases=16 differ=0`).

## Routed

Items from `corpus/lessons/round-41-verifier-spotcheck.md` §5, each with this round's disposition.

- **R1 C1 counter soundness residuals** (`R41SentinelCounter` F1–F4, `R41CritC1Counter` A1′; T08's `uv`-absent
  assumption). *Partly closed; a–c remain limits without a red control in this tool pair.* The round-42 counter carries
  the five `F41C1Hardened` repairs frozen plus leg f attribution (`plans/round42_c1_verify.py:19-30`). Two of them have a
  red control this round: **f** → `claims/control-c1-attribution.txt` (`killed=0 unattributed=14`, `PREDICATE C1 fail`);
  **d** (relative-token `path_ok`) → `claims/control-c1-hostile-escape.txt` (`SETUP fixture … breaks the contract`,
  `exit=2`). **a–c** (variant bound by fd with the store hidden, `--unshare-ipc`, `--tmpfs /run`) have no hostile control
  that can reach them here, because both tools in this mutant list run no fixture code (git plumbing only) — the freeze
  states that as a limit, and wave-1 seats `R42SentinelCounter` / `R42MutC1Counter` attack it; `<L1 fill: their
  verdicts>`. T08's `uv` assumption is **not carried into this round**: the 14 mutants need `git` only and the counter
  pins a fixed system PATH (`plans/round42_c1_verify.py:108`); no pin was added, so the assumption stays open for any
  later receipts battery.
- **R2 Scratch hygiene.** *Landed as a guard the seats cannot silently remove, and Q32's forward leg is red on one
  receipt.* `/fast/scratch/hyaku/kengaku-r42/.ROUND-ROOT-SENTINEL` exists (71 B, mtime 16:56; measured this seat by
  `ls -la`); the context handed to all 39 wave-1 seats carries the rule once (`build-dispatch.json`
  `taskCall.context`: one "Scratch rule" paragraph naming `$S`, the sentinel, and deletion allowed only inside `$S/`);
  seat `R42ScratchGuard` is tasked with `scratch_guard.py` (`check <root>` / `safe-rm <root> <seat> <path>` / a
  `--selftest` that shows every refusal able to fail) — `<L1 fill: scratch-guard selftest k/n>`. Envelope coverage of
  this round's L1 receipts, measured as the `ENVELOPE` block count over `.ufo/waves/round-42/claims/*.txt`: 9 of 13
  files carry it (the seven C1 controls, `witness-run.txt`, `control-c2-nothing.txt`), and `control-c2-filler.txt` — a
  control that imports `plans/round42_c2_verify.py` and calls its `v9()` (`claims/c2_filler_control.py`) — carries **no**
  envelope or timestamp line. `c2-stage-check.txt`
  and `census-before.txt` are the by-design non-counter runs (dry stage check, census) and `frozen-digests.txt` is a
  digest list. So the forward leg Q32 asks for is met for the C1 counter runs and red for one C2 control.
- **R3 C2 filler admission (both halves).** *Filler half closed; the tier-B live-state half stays open.* V9 is the
  ninth check (`plans/round42_c2_verify.py:327`) and holds the entry's `## Case table` to the receipt row by row, the row
  ids outside their `source:` lines, the PROVINCE line and the README `## Frontier` name. The standing control is red as
  required: `claims/control-c2-filler.txt` → `V9 DEFECT case_rows=0/16 bad=["no '## Case table' section", …]`, and the
  same mirror with measured content → `V9 ok case_rows=16/16 bad=0`, `CONTROL-C2-FILLER red-as-required`. The second half
  — "a check that reads S124-style tier-B PR rows' live state word" — is **not** in this round's instruments:
  `grep -n "closed\|merged" plans/round42_c2_verify.py plans/pkg_gate.py` returns nothing, so a tier-B row's
  `open/closed/merged` state is still prose. Routed again.
- **R4 SOURCES rule 2 (correction by a new `supersedes` row).** *Wave rule applied; nothing edited in place this
  round.* `git diff bc856d8..HEAD -- corpus/SOURCES.md` → empty (measured); S125–S127 are new rows on fresh ids, drafted
  verbatim with an 11-cell self-check and a census that leaves `E=0 W=15` (`R42PkgRows.md` §2–§3). Flip: any round-42
  correction must open with `supersedes S0NN —`.
- **R5 Carried items.** One per item:
  - *`round_close.py --selftest` second-run traceback* — assigned this round to seat `R42R5Carried` (cause `file:line`,
    smallest patch, a check red before / green after, and whether any `frozen-digests.txt` pins `round_close.py`);
    `<L1 fill: its verdict>`. No report exists at this draft.
  - *14 `round_close.py`/`tip_receipts.py` residual mutants* and *`F39LedgerTip` D1, `F39MutDirection`,
    `F39OrderGateMut` fail-open* — named carried again in the freeze (`plans/round-42-claims.md` §Limits) with no owner;
    `R42CritEquiv` §3 prices the adjacent gap at **u = 18** advertised behaviours without a frozen mutant (9 anchor + 9
    order; narrowest defensible reading 11).
  - *`s_usage-03` incidental fixture* — carried, unchanged, no work item.
  - *34 unpriced advertised rows of `tip_receipts.py`/`sources_adopt.py`* — carried, named in the freeze §Limits.

New for round 43 (not in §5): the round's calibration surface is wider than its 14 rows — the biggest unpriced classes
are the whole setup/exit-2 path on both tools and the `--verbose`/read-only contracts, 14 of 18 being one exit-2 or
read-set fixture away (`R42CritEquiv` §3). And the tier-B state word from R3 now has a named defect class behind it
(S124's "published" wording), but still no schema check.

## Census

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`.
Before (freeze): exit 0, `kengaku ok`, 15 `W04` (`.ufo/waves/round-42/claims/census-before.txt`); registry rows 117
(`grep -c '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`). The wave-1 row draft measures the three
states — rows only → exit 1 with three `E11`; rows + entry stand-in → `CENSUS_EXIT=0`, `E=0 W=15`; baseline `E=0 W=15`
(`R42PkgRows.md` §3.1). After (landing): `<L1 fill>`; expected registry 117 → 120, tier A +3, all `mined`, all used by
`corpus/knowledge/tb2-circuit-fibsqrt-grader.md`.

## Falsifiers run in wave 1 (other seats' reports, not re-run here)

- `R42CritEquiv` — no equivalent among the 14 (`e = 0`), no incidental kill under the strict test (`i = 0`), three
  named limits (§2), the four round-40 provenance corrections (§4), and `u = 18` unlisted advertised behaviours (§3).
  Its probes are its own from-nothing repos (`probe_a17.txt`, `probe_none.txt`, `probe_xo3.txt`, `probe_lbl.txt`).
- `R42PkgRows` — three live re-fetches at the pin, all `cmp=IDENTICAL` with the captures and with the spec's digests, and
  `anchor_digest_check.py` green on a clone after staging (`rows=120 tokens=27 defects=0`).
- The frozen controls re-read here, not re-run: `control-c1-nothing.txt` (`MUTANTS total=14 killed=0 survived=14`,
  `PREDICATE C1 fail`), `control-c1-no-mutants.txt`, `control-c1-tool-edited.txt` (`PINS mismatched=1`),
  `control-c1-direction-mislabel.txt`, `control-c1-attribution.txt`, `control-c1-hostile-escape.txt`,
  `control-c2-nothing.txt` (`checks=9 defects=6`, `PREDICATE C2 fail`), `control-c2-filler.txt`.
- Landing measurement of both counters, the battery review and the pytest parity re-grade: `<L1 fill>`.
