# Round 42 — a calibration battery whose kills must be attributed; an eighth TB2 grader whose answer is a gate list run by a compiled simulator (2026-10-26, hyaku run 9)

L1 `KengakuR42` (planner seat). Frozen claims `plans/round-42-claims.md` (freeze `bc856d8`, first recorded probe run
`523b278`); baseline lane tip `d69452c` (the round-41 non-author spot-check). Drafted by wave-1 seat `R42LessonDraft`;
the landing numbers were filled by the L1 at integration (landing `ff14d76d`).

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
| S128 OpenAgents issue #9645 “Audit circuit grader coverage beyond its 48,401 input ceiling” (row appended by round-43 closure R2; the round-42 Gate table omitted it) | **Admitted (mined, tier B)** | Opened by wave-1 `R42ScoutPriorArt` 2026-10-26 17:35 -03; re-opened by the round-43 seat 2026-10-26 19:10:24 -03 at `https://github.com/OpenAgentsInc/openagents/issues/9645` (`gh api repos/OpenAgentsInc/openagents/issues/9645`: `state=closed`, `created_at=2026-09-25T09:01:50Z`, `closed_at=2026-09-25T09:11:26Z`, title equal). Quote, issue body line 3: "The official grader exercises 28 values, none above 48,401." (9 words). Tier B is right for a third party's published report cited as prior art for the coverage gap only: it builds no circuit and names none of the parse, ordering or cwd mechanics. Flip: the issue body is edited so the quoted sentence no longer holds, or the entry rests a mechanism claim on it rather than prior art. |

Gate prose: the three admitted rows are exactly the three the spec pins (`plans/pkg-spec-r42.json` `rows` = S125, S126,
S127; `raw_base` = the `circuit-fibsqrt/` tree at the pin). The registry coupling is measured: with the rows present and
the entry absent, `sources-census.sh validate` exits 1 with exactly three `E11` lines for this entry's `used-by`
(`R42PkgRows.md` §3.1); with the entry present, `CENSUS_EXIT=0`, `E=0 W=15`. `anchor_digest_check.py --evidence-ref
index|head` on a clone carrying the rows prints `rows=120 tokens=27 defects=0`, every new row binding by `url-task` to
its own capture. The admission of tier A is for these three files at this commit, nothing about TB2 as a whole.

Round-43 addendum to the prose above: the spec still pins three rows (`plans/pkg-spec-r42.json` `rows` = S125, S126,
S127), and two more rows are admitted by this Gate's own decisions — S128 (OpenAgents issue #9645, tier B, prior art
for the coverage gap) and S135 (`environment/Dockerfile` @ `2fd12b88`, tier B, the mechanism row the entry's cwd
statements rest on). "The three admitted rows" above therefore means the three *spec-pinned* rows; the Gate's
admitted set is five candidates, of which S125-S127 are tier A and S128/S135 tier B.

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
  states that as a limit, and wave-1 seats `R42SentinelCounter` / `R42MutC1Counter` attack it. `R42SentinelCounter`
  V1 (HIGH) falsifies that limit for `order_check.py`: `log.showSignature` + `gpg.program` in a fixture's own
  `.git/config` runs a program during `git log` inside the tool run (no fabricated kill shown; battery42 carries no such
  key) — routed to the round-43 counter. T08's `uv` assumption is **not carried into this round**: the 14 mutants need `git` only and the counter
  pins a fixed system PATH (`plans/round42_c1_verify.py:108`); no pin was added, so the assumption stays open for any
  later receipts battery.
- **R2 Scratch hygiene.** *Landed as a guard the seats cannot silently remove, and Q32's forward leg is red on one
  receipt.* `/fast/scratch/hyaku/kengaku-r42/.ROUND-ROOT-SENTINEL` exists (71 B, mtime 16:56; measured this seat by
  `ls -la`); the context handed to all 39 wave-1 seats carries the rule once (`build-dispatch.json`
  `taskCall.context`: one "Scratch rule" paragraph naming `$S`, the sentinel, and deletion allowed only inside `$S/`);
  seat `R42ScratchGuard` is tasked with `scratch_guard.py` (`check <root>` / `safe-rm <root> <seat> <path>` / a
  `--selftest` that shows every refusal able to fail) — `SELFTEST ok=36/36`, landed as `plans/scratch_guard.py`. Envelope coverage of
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
    verdict `r5-round-close-rerun-fixed-draft`: no frozen digest list pins `round_close.py`; the patch landed in
    `ff14d76d` and `integrate/r5-round-close-check.txt` shows run 1 and run 2 both `rc=0`, identical output (red before).
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
(`R42PkgRows.md` §3.1). After (landing): exit 0, `kengaku ok`, 15 `W04` (`.ufo/waves/round-42/integrate/census-final.txt`);
registry 117 → 121: tier A +3 (S125–S127), tier B +1 (S128, OpenAgents #9645, opened by the L1 17:35 -03), all `mined`, all used by
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
- Landing measurement (`.ufo/waves/round-42/integrate/measure-final.txt`, clean clone of `ff14d76d`): C1 `BATTERY
  fixtures=29 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=14 killed=14 … unattributed=0`, `PREDICATE C1 pass`;
  C2 `checks=9 defects=0`, `PREDICATE C2 pass`; fibsqrt probe re-run byte-equal; pytest parity 16/16 (`R42CritPytest`).
  The battery review is wave 2's.

## Mistakes added by the L1 at integration

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **An envelope that changes the instrument's result** — the Q32 envelope with the host home read-only made `uv run --with biopython` (the gate's P10 leg) fail its cache lock, so every C2-class counter and ledger row R35-D1 went red for an envelope reason | `.ufo/waves/round-42/integrate/measure-baseline-v1.txt` (`P10 DEFECT fresh probe exit=2 … Could not acquire lock`) vs `measure-baseline.txt` (v2: all green as at round 41) | none — Q32 names what must be read-only, not that the instrument must still answer the same | `integrate/envelope.sh` v2 overlays `~/.cache` from scratch (host cache untouched); shown able to fail by the v1 receipt itself |
| **A frozen sentence about a tool's attack surface written from the command list, not from git's config surface** — "both tools execute no fixture code (git plumbing only)" | `plans/round42_c1_verify.py:30`; falsified by `R42SentinelCounter` V1 (`log.showSignature` + `gpg.program`) | none — no criterion asks a counter to enumerate config keys that execute | routed: the round-43 counter pins `gpg.program`/`log.showSignature` with a red hostile control (`R42SentinelCounter` V1 remediation) |
| **A seat-tooling slip by the L1** — two `edit` calls on the freshly written probe used guessed line numbers and broke it (syntax error) before the freeze | the edit tool's syntax warning; corrected in the same minute; the frozen probe is the corrected file (`frozen-digests.txt` `fc58bf3f…`, dry table and stage-check after it) | the editor's parse check | re-read before every anchored edit; no frozen byte was affected |
| **A wave dispatched under the m_flash floor** — wave 2 carries 14/33 m_flash-routed seats (executor/scribe/critic/sentinel), below the run-8/9 rule "m_flash roles still carry ≥50 % of every wave"; the generator printed `flash=14/33` and the L1 wrote the ready file without reading it | `.ufo/waves/round-42/make_falsify_spec.py` output (`33 {'executor': 5, 'reviewer': 10, 'critic': 9, …} attack=22/33 flash=14/33`); `falsify.ready.dispatched` taken before the check | none — the validator checks the band, not the route mix | round-43 generators assert `flash*2 >= len(items)` before writing the spec (an assert shown able to fail by this spec: 28 < 33) |

## Errata (appended in round 43 from the wave-2 review; nothing above is edited)

`F42RevLesson` (`.ufo/waves/round-42/falsify/F42RevLesson.md`) routed eight defects; six are corrected here, two were
re-checked against this file at `d33350f` and are not defects (last paragraph). Line numbers are this file's.

- **E1 — R4's measurement (`:98`).** `git diff bc856d8..HEAD -- corpus/SOURCES.md` is not empty:
  `git diff --numstat bc856d8..HEAD -- corpus/SOURCES.md` → `4	0	corpus/SOURCES.md` — the four added rows `S125`–`S128`,
  zero removals. The substance holds (no in-place edit), but the honest wording is "the diff shows only additions, no
  in-place edits"; as written the sentence is true only against the freeze commit itself (`bc856d8..bc856d8`).
- **E2 — R5's freeze pointer (`:106-108`).** The 14 `round_close.py`/`tip_receipts.py` residual mutants and
  `F39LedgerTip` D1 / `F39MutDirection` / `F39OrderGateMut` fail-open are **not** "named carried again in the freeze":
  `plans/round-42-claims.md` has no `§Limits` section (headers at `:1,23,65,96,102`) and
  `grep -nE 'LedgerTip|MutDirection|OrderGateMut|fail-open|s_usage' plans/round-42-claims.md` → no output (rc=1). The
  freeze's "Limits named now" bullet (`:60-63`) names XL1–XL6, `state_check.py`/`round_close.py` survivors and the 34
  unpriced advertised rows — so `:111` is right and `:106-108` is not: the F39 trio and the residual mutants were
  carried by this lesson alone.
- **E3 — the route-mix ratios are quoted stdout, not persisted data (`:151`).** `flash=14/33` and `attack=22/33` appear
  nowhere under `.ufo/waves/round-42/` except the review that quotes them; `falsify-spec.json`'s 33 items carry only
  `axes, milestone, name, prompt, role` (reviewer 10, critic 9, executor 5, mutation-tester 3, scout 3, connector 3), and
  `falsify-dispatch.json` carries `counts {spawn 33, resume 0, total 33}` with no model or route field. The row's role
  list "(executor/scribe/critic/sentinel)" also names two roles wave 2 did not have. The class and the fix stand; the two
  ratios are one generator run's stdout, and the persisted facts are the role mix above and `counts.spawn=33`.
- **E4 — receipt pointer (`:57`).** `grep -n 'fibsqrt-probe.txt:6'` finds one citation, not the review's two. `:6` is
  the `# capture test_outputs.py sha256=` header. The summary
  is `:23` (`regrade cases=16 differ=0`) and `:24` (`cases=16 observed_pass=7 observed_fail=9 mismatches=0`); the
  `lookup-28` case is `:11`.
- **E5 — the census command (`:122`).** Run as printed (BRE) the `\|` is alternation and the `^ {0,3}` branch matches
  every line, so it yields 171/175 — `wc -l` at `bc856d8`/`508434a` — not 117/121. The quoted numbers come from the `-E`
  form: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`.
- **E6 — row 3's fix has no failing receipt (`:150`).** The syntax warning was ephemeral and nothing under
  `.ufo/waves/round-42/` stores it; `frozen-digests.txt:4` (`fc58bf3f…`) only proves the frozen probe is the corrected
  file (`sha256sum plans/fibsqrt_probe.py` matches). Every other Mistakes row names a persisted failing receipt; this
  one's falsifier exists only in its own sentence.
- **E7 — two C1 `adv` cites (from `F42CritAdv`).** The frozen `MUTANTS` rows X3 and X7 quote `plans/anchor_digest_check.py`
  verbatim but cite the wrong lines: X3 `:57-58` for a sentence at `:59-61`, X7 `:92-93` for a sentence at `:91-92`; both
  carried from `F40XMutAnchor.md` §5. Display-only — the counter echoes `label[:90]` and never parses it — so no
  admission claim moves; correct the cites when the counter is next editable.

Re-checked and **not** defects (at `d33350f`): `plans/round42_c2_verify.py:327` is the `("V7" …), ("V8" …), ("V9",
lambda: v9(lane))]` line and `:328` is `defects = 0`, so the R3 citation `:327` is exact (the review's D5 moved it one
line early); and `corpus/evidence/round42/tb2-circuit-fibsqrt/Dockerfile` carries `COPY tests/sim.c /app` at `:9` and
`COPY gates.txt /app` at `:10` with the comment at `:8`, so `Dockerfile:9-10` is right (the review's D7 moved both pins
one line late).

### Errata (round 43, closure R1 — receipt pointer)

- **`:57` pointer corrected — `fibsqrt-probe.txt:6` → `:11`.** `:57` cites "receipt `fibsqrt-probe.txt:6`" for the
  `lookup-28` row; line 6 of that receipt is the `# capture test_outputs.py sha256=6117b8ed…` header, and the
  `lookup-28` CASE row is **line 11** (`CASE lookup-28 predicted=pass observed=pass tests=PPP … violates=example-208,
  example-20000`). The sentence's content stands: `lookup-28` prints 0 for 208 and 20000 and still passes 3/3. Found by
  `F42CritOverclaim` §4 ("Wrong (1, minor)"); re-read at the receipt by this seat. Nothing deleted.

### Flip checks (round 43, closure R2 / Q35; appended)

Flip check (round 43): Dockerfile — fired — the entry kept the WORKDIR /app sentence (tb2-circuit-fibsqrt-grader.md:65, :89, :94, :435-438); executed in round 43 as tier-B row S135 and the appended entry block citing it
Flip check (round 43): README.md — not fired — no entry sentence rests on README.md alone; every checkable README sentence is carried by S125-S127

