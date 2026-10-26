# R42LessonDraft — draft `corpus/lessons/round-42.md` (kengaku round 42, wave 1, scribe)

Seat: leaf scribe, no subagents, no background jobs, no labrat. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
read-only; nothing written outside this report's two files. No tool installed or upgraded (no pacman, `uv`, `npm`;
`~/.local/bin` untouched — digest below unchanged). No scratch work beyond `mkdir -p` of my own `$S`; no `rm -rf` was
run at all, so no scratch rule could be violated.

Paste-ready draft: `.ufo/waves/round-42/build/R42LessonDraft/round-42.md` (18 956 B, 135 lines, sha256
`0a3dbca65fa01187fb327ada04a53c2a9eb1c9ddaebf4e4a19d94eae822111d4`). Its six `<L1 fill>` markers are the numbers this
seat cannot observe: the wave-1 battery and entry not yet integrated, the landing measurement, the scratch-guard and
R5 seat verdicts, and the census-after row count.

## 1. Inputs read (whole or at the cited range)

| input | what was taken |
|---|---|
| `plans/round-42-claims.md` (whole) | freeze `bc856d8`, first run `523b278`, baseline `d69452c`; C1 14 mutants / 9+5 floors; the XO5/XO6 `rc-mirror` correction and its control; C2 S125–S127 + 16 cases; §Frontier mined mistake; §Separability; §Limits; the R1–R5 routing line |
| `corpus/lessons/round-41.md` (whole) | section order (`## Mistakes`, `## Gate`, `## Routed`, `## Census`, `## Falsifiers`), table shape, errata style, `<L1 fill>` convention |
| `corpus/lessons/round-41-verifier-spotcheck.md` (whole) | §5 R1–R5, verbatim item text used as the `## Routed` skeleton |
| `.ufo/waves/round-42/claims/` — `witness-run.txt`, `control-c1-direction-mislabel.txt` + `.patch`, `control-c1-nothing.txt`, `control-c1-no-mutants.txt`, `control-c1-tool-edited.txt`, `control-c1-attribution.txt`, `control-c1-hostile-escape.txt`, `control-c2-nothing.txt`, `control-c2-filler.txt`, `c2-stage-check.txt`, `census-before.txt`, `frozen-digests.txt`, `envelope.sh` | every control line quoted in the draft; envelope coverage count; 15 `W04` |
| `.ufo/waves/round-40/falsify/F40XMutLedgerOrder/xmut_driver.py:105-133`, `F40XMutLedgerOrder.md:60-135` | the mislabel: `rc-silence` at `:113`/`:121` beside witness prose `:116-117`/`:125-126`, table rows `:70-71`, measured §2 `:120-127` |
| `.ufo/waves/round-41/build/R41PlanNext/near40_survivors_only.txt:40-41`, `R41PlanNext.md:59` | the label carried into round-41 wave-1 unchanged |
| `plans/round42_c1_verify.py:1-140` (docstring, PINS, directions, BATTERY_REL), MUTANTS rows `:201,:206` | direction definitions, leg a–f, floors 9/5, fixed PATH `:108` |
| `plans/round42_c2_verify.py` (grep `V9`, `closed`, `merged`, `def v9`), `plans/pkg_gate.py:299-303` | V9 is the ninth check; no live-state word is read by any check; the gate prints only `ok`/`DEFECT` |
| `plans/pkg-spec-r42.json` (`rows`, `raw_base`) | the spec pins exactly S125/S126/S127 |
| captures `corpus/evidence/round42/tb2-circuit-fibsqrt/` — `test_outputs.py` (whole), `sim.c:95-130,303-353`, `instruction.md` (whole), `README.md` (whole), `Dockerfile`, `test.sh`, `task.toml`, `gates.txt:1-5`, `SHA256SUMS` | located quotes, digests, the cwd/compile/print mechanics |
| `corpus/evidence/round42/fibsqrt-probe.txt` (whole) | 16 case lines, `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, `regrade cases=16 differ=0` |
| wave-1 reports `R42PkgRows.md` (whole), `R42CritEquiv.md` (whole), entry draft `R42PkgEntry/tb2-circuit-fibsqrt-grader.md` (grep `source:`, `Dockerfile`, `208`, `stdin`) | live re-fetch receipt, census three states, anchor rows=120; equivalents/limits/u=18; the entry's three `source:` lines and its `Dockerfile:3` citations |
| `.ufo/waves/round-42/build-dispatch.json` (`taskCall.context`, member tasks) | the scratch-rule paragraph is in the shared context; R42ScratchGuard / R42R5Carried / R42ScoutMisroot task text; 39 members |

## 2. Behaviour — what the draft contains

- **`## Mistakes`** — two rows, each `class · evidence pointer · captured-by · fix`, each fix **shown able to fail**:
  1. **XO5/XO6 direction mislabel (the required row).** The round-40 near-variant table labels both `rc-silence`; the
     same rows' witness prose and §2 record `reference ORDER ok rc=0, mutant ORDER HIT rc=1` (8 words) and
     `the reference scans commits=1 and PASSes; the mutant … FAIL rc=1` (`F40XMutLedgerOrder.md:120-125`). Round-41
     wave 1 re-printed the label (`R41PlanNext/near40_survivors_only.txt:40-41`). Fix = re-derive both as `rc-mirror`
     (`plans/round42_c1_verify.py:201,206`; definition `:44`), witnessed `claims/witness-run.txt:29-30`
     (`rc-mirror killed by=w-xo5-post-receipt-blob attributed=L117`). Shown able to fail:
     `claims/control-c1-direction-mislabel.txt:29-30` prints `SURVIVED exhibits=0>1,rc-mirror`, `:33`
     `MUTANTS total=14 killed=12 survived=2`, `:37` `PREDICATE C1 fail`, `exit=1`.
  2. **A kill credited to a fixture that did not produce it** (X2 X4 X5 X11 on a lane clone). Evidence
     `R42CritEquiv.md` §4 + `probe_a17.txt` / `probe_none.txt`. Fix = leg f attribution + from-nothing builds; shown
     able to fail by `control-c1-attribution.txt` (`killed=0 unattributed=14`, `PREDICATE C1 fail`).
  Three named limits follow the table: class-only kills (X6/X7 keep rc=1, one repo kills both), XO6's `indirect` cell
  is a strictness kill rather than a demonstration of `order:52-53`, and the round-41 witness-as-battery loophole
  persists (no automated check). One negative note: round-40's `--work` traceback class did not recur.
- **`## Gate`** — seven rows, 2026-10-26 access date throughout. S125/S126/S127 **admitted** (mined, tier A) with the
  L1's 17:08 -03 open time, the 17:20:09 / 17:24:14 cmp-identical re-fetch, a ≤25-word quote at a located line and the
  capture digest. `README.md` **rejected** (narrative restatement, not shipped into the image, `Dockerfile:9-10`);
  `Dockerfile` **rejected with one flagged claim** (`WORKDIR /app`, `:3`, is load-bearing for the `fake-sim-script` case
  and the entry's cwd paragraph); `test.sh`/`task.toml`/`SHA256SUMS` and `solve.sh`/`gates.txt` **captured, not rows**.
  Every row carries a flip condition. Gate prose states the spec pin, the measured census coupling (rows-only → exit 1,
  three `E11`; rows+entry → `CENSUS_EXIT=0`, `E=0 W=15`; anchor `rows=120 tokens=27 defects=0`) and the falsified
  instruction sentences (stdin, "last 32 lines", the two ungraded examples).
- **`## Routed`** — round-41 spotcheck §5 R1–R5, each with this round's disposition: R1 partly closed (f and d red,
  a–c no reachable hostile control in this tool pair, T08 `uv` assumption not carried); R2 landed as sentinel + context
  sentence + a drafted guard seat, and Q32's forward leg **red on one receipt** (`control-c2-filler.txt`); R3 filler half
  closed (V9 + red filler control), tier-B live-state half open (no check reads `closed`/`merged`); R4 wave rule applied
  (`git diff bc856d8..HEAD -- corpus/SOURCES.md` empty); R5 split per item (R42R5Carried assigned, 14 residuals + three
  F39 items + `s_usage-03` + 34 unpriced rows carried, u=18 priced). One new round-43 item proposed (the wider surface).
- **`## Census`** — command, before-state (exit 0, `kengaku ok`, 15 `W04`, 117 rows), the three measured census states,
  `<L1 fill>` for after.
- **`## Falsifiers run in wave 1`** — R42CritEquiv (e=0, i=0, u=18), R42PkgRows (three `cmp=IDENTICAL`), the frozen
  controls re-read verbatim, landing measurement as `<L1 fill>`.

## 3. Gates (the draft's own Gate table, row by row)

| candidate | decision in the draft | basis (measured, located) |
|---|---|---|
| S125 `tests/test_outputs.py` @ `2fd12b88` | admit, mined, tier A | open 2026-10-26 17:08 -03 (L1); re-fetch `cmp=IDENTICAL` 17:20:09 + 17:24:14 (`R42PkgRows/refetch.txt`); quote `:23` "assert line_count < 32000" (4 words); sha256 `6117b8ed…` |
| S126 `instruction.md` @ `2fd12b88` | admit, mined, tier A | same opens; quote `:8` "…binary representation of stdin" (12 words); sha256 `a7f50026…`; falsified at `sim.c:324` (argv) and `:340-347` (highest-indexed, not "last 32 lines") |
| S127 `tests/sim.c` @ `2fd12b88` | admit, mined, tier A | same opens; quote `:335` "for (int step = 0; step < 32000; step++)" (9 words); sha256 `700645ac…` |
| `README.md` @ `2fd12b88` | **REJECT — captured, not a row** | restates S125–S127, no own predicate, not in the image (`Dockerfile:9-10` copies only `tests/sim.c`, `gates.txt`); quote `:10` (15 words); flip = an entry statement only README supports, or README diverging from the tests |
| `Dockerfile` @ `2fd12b88` | **REJECT — captured, not a row; one claim flagged** | `:3` "WORKDIR /app" (2 words) is load-bearing (`test_outputs.py:66` writes `./sim`; `:119` runs `/app/sim`; `test.sh:13` guards only `PWD = /`); flip = if the entry keeps the cwd sentence, admit as tier-B mechanism row |
| `test.sh`, `task.toml`, `SHA256SUMS` | captured, not rows | mechanism (`test.sh:18-22`), declared envelope (`task.toml:22,25`), inventory; flip = an entry statement needing one as its source |
| `solve.sh`, `gates.txt` | captured, not rows | oracle end state (`oracle-solve-sh`, `PPP`) and the shipped example (`nop`, `PPF`); flip = an entry sentence about the oracle's construction or the example's exact output |

## 4. Touched surfaces

| path | change |
|---|---|
| `.ufo/waves/round-42/build/R42LessonDraft.md` | this report (new) |
| `.ufo/waves/round-42/build/R42LessonDraft/round-42.md` | the paste-ready lesson draft (new, 18 956 B, sha256 above) |
| `/fast/scratch/hyaku/kengaku-r42/R42LessonDraft/` | `mkdir -p` only; nothing else created; nothing deleted |

Nothing else was written. `git -C <lane> diff --stat` → 0 lines (no tracked file changed);
`git -C <lane> status --porcelain` lists only other seats' untracked wave dirs plus the L1's
`.ufo/waves/round-42/integrate/`, `build.ready*`. No `git add`/commit/stash/checkout/reset anywhere; no jj command; no
`corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`, `SKILL.md`, `PROVINCE.md`, `SHONEN.md` or frozen artefact
touched. `plans/battery42` does not exist yet (checked: `ls plans/battery42` → `No such file or directory`).

## 5. Out of scope (and correctly left undone)

- **No counter, battery, probe or gate was run.** The draft's C1/C2 verdict sentences stay `<L1 fill>`. Every control
  number in the draft is quoted from a committed receipt, and each quote carries its file and line.
- **No lane file written.** The task says "Draft `corpus/lessons/round-42.md`"; the seat's write bound is
  `.ufo/waves/round-42/build/`, so the draft sits in `R42LessonDraft/round-42.md` for the L1 to paste. `## Census`
  after-state, the falsifier verdicts of seats still running (`R42ScratchGuard`, `R42R5Carried`, `R42CritPytest`, the
  entry and prose seats, `R42SentinelCounter`, `R42MutC1Counter`) and the landing measurement are L1 fills, not guesses.
- **Not re-verified by me:** the live raw URLs (R42PkgRows re-fetched them twice at 17:20:09/17:24:14 — its receipt is
  the evidence, not my run); the entry draft's content (§ outside the Gate claim it triggers); prior-art (no
  `R42ScoutPriorArt` report exists at this writing).
- **No edit to any frozen input.** Digests of `plans/round-42-claims.md`, both counters, the probe, spec, gate, dry
  table, captures and `claims/` are unchanged by this seat (read-only access).

## 6. Findings for the L1

1. **The XO5/XO6 mislabel is fully closed as a lesson row and already fail-tested.** The chain is
   `xmut_driver.py:113,121` (label) → `:116-117,125-126` (same rows' measured prose) → `F40XMutLedgerOrder.md:70-71`
   (table) → `R41PlanNext/near40_survivors_only.txt:40-41` (carried) → `round42_c1_verify.py:201,206` (re-derived
   `rc-mirror`) → `control-c1-direction-mislabel.txt` (round-40 labels → `killed=12`, `PREDICATE C1 fail`). One
   sentence of the freeze is slightly generous: it says "the round-41 **plan** carried the list without re-deriving";
   the carrier I could locate is the round-41 **wave-1 scout report/dump** (`R41PlanNext.md:59`,
   `near40_survivors_only.txt:40-41`), not `plans/round-41-claims.md` (`grep XO5` there → no match). The draft says
   "the round-41 wave-1 scout".
2. **The Dockerfile is the one Gate decision that needs the L1, not me.** The entry draft cites `Dockerfile:3`
   (`WORKDIR /app`) in its own tables (`R42PkgEntry/tb2-circuit-fibsqrt-grader.md:64-66`, `:89`) while declaring it "a
   capture of the harness". Either the entry drops the cwd sentence (then the case is conditional on cwd) or
   `Dockerfile` becomes a fourth tier-B row. The draft's flip condition states both; picking one is a Gate call.
3. **Q32's forward leg is red on exactly one round-42 receipt.** `ENVELOPE` block counts over
   `.ufo/waves/round-42/claims/*.txt`: 3 lines each in the seven C1 controls, `witness-run.txt`, `control-c2-nothing.txt`
   (9 files); **0** in `control-c2-filler.txt`, which is a counter-function run (`claims/c2_filler_control.py` imports
   `round42_c2_verify.py` and calls `v9()`). Also 0 in `c2-stage-check.txt` (pre-freeze, no sandbox by design),
   `census-before.txt` (census script) and `frozen-digests.txt` (a digest list) — those three are not counter runs.
   The draft records the gap as an R2 finding rather than smoothing it.
4. **R3's second half has no instrument.** `grep -n "closed\|merged" plans/round42_c2_verify.py plans/pkg_gate.py` →
   no output, so S124-style tier-B live states remain prose; the filler half is closed and red-tested
   (`control-c2-filler.txt`: `V9 DEFECT case_rows=0/16`, `CONTROL-C2-FILLER red-as-required`).
5. **The F39/F40 denominator question got a number this round**: `u = 18` advertised behaviours with no frozen mutant
   (`R42CritEquiv` §3; narrowest defensible reading 11). Recorded as a round-43 routed line, not as a defect of C1.

## 7. Evidence (commands and their output; every number above traces here)

```
$ sha256sum corpus/evidence/round42/tb2-circuit-fibsqrt/{test_outputs.py,instruction.md,sim.c}
6117b8edb7d567b30e32b16a9244bec4c131ec01e9065d52f6f53f87e36f0438  …/test_outputs.py
a7f500266a878d04ac9de39fba76220cfad216d8f6b8063bba93bebb3d4ab9ea  …/instruction.md
700645ac6156cdc88ec1e210f7c7d8d9969bb42aec969c410597e8efca796173  …/sim.c
  (the three values `SHA256SUMS`, `plans/pkg-spec-r42.json` rows and `R42PkgRows/refetch.txt` carry)

$ grep -n "rc-silence" .ufo/waves/round-40/falsify/F40XMutLedgerOrder/xmut_driver.py
113:    ("XO5", "order", "-", "rc-silence",
121:    ("XO6", "order", "-", "rc-silence",
$ sed -n '116,117p;125,126p' …/xmut_driver.py
     "witness wit-xo5: repo with a P10-ok claims blob committed after the receipt (reference ORDER "
     "ok rc=0, mutant ORDER HIT rc=1); battery40 never commits claims after the receipt",
     "witness wit-xo6: claims blob 'P10 PASS receipt unreadable' (reference ORDER ok rc=0, mutant "
     "ORDER HIT rc=1); no battery40 fixture carries a PASS verdict line",

$ grep -E "MUTANTS total|PREDICATE" .ufo/waves/round-42/claims/control-c1-direction-mislabel.txt
MUTANT XO5 order rc-silence SURVIVED exhibits=0>1,rc-mirror …
MUTANT XO6 order rc-silence SURVIVED exhibits=0>1,rc-mirror …
MUTANTS total=14 killed=12 survived=2 invalid=0 null_detected=0 unattributed=0
PREDICATE C1 fail

$ grep -n "XO5\|XO6" .ufo/waves/round-42/claims/witness-run.txt
29:MUTANT XO5 order rc-mirror killed by=w-xo5-post-receipt-blob attributed=L117 hits=1 -- plans/order_check.py:116-117 …
30:MUTANT XO6 order rc-mirror killed by=w-xo6-p10-pass-line attributed=L53 hits=1 -- plans/order_check.py:52-53 …

$ grep -n "('XO5'\|('XO6'" plans/round42_c1_verify.py
201:    ('XO5', 'order', '-', 'rc-mirror', 'direct',
206:    ('XO6', 'order', '-', 'rc-mirror', 'indirect',

$ for f in control-c1-nothing control-c1-no-mutants control-c1-tool-edited control-c1-attribution control-c2-nothing; do grep -E "MUTANTS total|checks=|PREDICATE" …/$f.txt; done
MUTANTS total=14 killed=0 survived=14 …          PREDICATE C1 fail
MUTANTS total=0 killed=0 survived=0 …            PREDICATE C1 fail
MUTANTS total=14 killed=5 survived=0 invalid=9 …  PREDICATE C1 fail   (PINS total=2 mismatched=1)
MUTANTS total=14 killed=0 survived=0 … unattributed=14  PREDICATE C1 fail
checks=9 defects=6                                PREDICATE C2 fail

$ grep -c ENVELOPE .ufo/waves/round-42/claims/*.txt
9 files at 3; control-c2-filler.txt=0, c2-stage-check.txt=0, census-before.txt=0, frozen-digests.txt=0

$ grep -n "closed\|merged" plans/round42_c2_verify.py plans/pkg_gate.py      # → no output
$ ls plans/battery42                                                          # → No such file or directory
$ grep -c "W04" .ufo/waves/round-42/claims/census-before.txt                  # → 15 (tail: kengaku ok … census_rc=0)
$ grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md  # → 117
$ git diff --stat bc856d8..HEAD -- corpus/SOURCES.md                          # → empty
$ ls -la /fast/scratch/hyaku/kengaku-r42/.ROUND-ROOT-SENTINEL                  # → 71 B, 2026-10-26 16:56
```

Quotes used in the draft are ≤25 words and located at the cited file:line of the cited capture; the two that stand
outside the lane (`R42PkgRows`, `R42CritEquiv`) are quoted as those seats' measured output, never as mine.

## 8. Limits

- The draft is a **draft**: six `<L1 fill>` markers hold the landing truth, and the seven-row Gate's Dockerfile
  decision is a judgement the L1 must make against the entry as it lands.
- My reading of "13 `claims/*.txt` files" is a file count at this writing; a later control added by another seat would
  change the 9/13 ratio, not the finding (the filler control carries no envelope).
- I did not re-grade any C2 case, re-run any counter, or open any URL; where the draft states a digest or a
  `cmp=IDENTICAL`, the receipt named beside it is the source.
- The draft's title and axis framing are mine; the round's score moves stay the L1's (the freeze says C2 is judged on
  its counter, not a score move).

## 9. Host-safety receipt (QUALITY Q32)

- Envelope line for this seat: **no bwrap-wrapped command was needed** — every action was a read of committed bytes,
  `mkdir`, and two file writes under `.ufo/waves/round-42/build/`. No counter/battery/fixture process was started
  (the counter requires one; none was run). Had one run, the required form is
  `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc
  --unshare-pid --die-with-parent <command>`.
- `date +%T` before/after: **17:30:11 / 17:31:26**.
- `ls -A /home/vgpnk/.local/bin | sha256sum` before/after:
  `436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18` / same (unchanged).
- Nothing written to `/usr`, `/etc`, `$HOME` outside scratch, or any PATH directory; `/tmp` unused; scratch confined to
  `/fast/scratch/hyaku/kengaku-r42/R42LessonDraft/`.

VERDICT: lesson-drafted
