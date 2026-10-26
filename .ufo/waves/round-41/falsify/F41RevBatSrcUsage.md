# F41RevBatSrcUsage — non-author review of `plans/battery41/s_usage.py` (S02, S03, S05, S06)

Seat: critic, round 41 wave 2 (falsify), hyaku run 9, 2026-10-26. Target:
`kengaku-shokunin/plans/battery41/s_usage.py`, sha256 `c9ca3abe3d4b5dff02d9196e026ab31f7b37347d0866769ac509116fc07afeff`,
claimed kills S02/S03/S05/S06 of `plans/round41_c1_verify.py`. Nothing in the lane was edited.

## 0. What holds / what breaks

- **Holds.** All four mutants die by this module alone (`killed=4/4`, `wrong=0 tampered=0 sidechannel=0
  null_detected=0`), every kill names a `s_usage-*` fid, and on each of the four `killed by=` fixtures the mutated
  line provably executes (`TRACE-MUT` printed from the mutated line itself). None of the wave-1 counterexample
  vectors is present: the module contains **no file read at all** (only two `ctx.write` calls, both inside `d`), no
  import beyond `from __future__ import annotations`, no `ctx.sh`/`ctx.git`, no stub script, no socket, no IPC, no
  `..` token; hiding the whole lane changes no verdict (8/8 ref rc unchanged, 8/8 mutant rc unchanged).
- **Breaks (one fixture).** `s_usage-03-single-digit-month-duplicate-request` is an **incidental** kill: its
  mutant exit 5 is `duplicate-request`, produced identically with the date trigger removed
  (`ref_rc=5 mut_rc=5` on the same fixture with `--access-date 2026-10-26`), so the fixture adds no evidence about
  the `--access-date` guard. Its twin `s_usage-03-dotted-access-date` carries S03 honestly. The author already
  disclosed the mechanism (wave-1 `R41BatSrcUsage.md` §1: "the mutant's 5 comes from `duplicate-request`, not from
  the opened cell"), so this is a calibration weakness, **not** a false claim and **not** a C1 admission failure
  (the frozen kill rule counts kills, and the mutant is still killed by a fixture of this module).
- **Caveat, not a defect.** S02's `2>1` is satisfied by an uncaught `AttributeError` (`None.read_text`), and
  `SKILL.md:573` advertises no exit `1` for this tool at all, so the pair is unambiguous evidence that the guard is
  load-bearing; but the counter records only rc, so no future reader may read `2>1` here as "the mutant took the
  tool's exit-1 path".

## 1. Provenance and frozen state

```
$ git -C "$S/lane" rev-parse 3d0058f:plans/battery41/s_usage.py   -> a2d2dd910aaf90197a58b4fb19110e7195ffbddd
$ git -C "$S/lane" rev-parse HEAD:plans/battery41/s_usage.py      -> a2d2dd910aaf90197a58b4fb19110e7195ffbddd
$ git -C "$S/lane" diff --stat 3d0058f HEAD -- plans/battery41 plans/sources_adopt.py plans/round41_c1_verify.py
  (empty)
$ sha256sum plans/round41_c1_verify.py plans/sources_adopt.py plans/battery41/s_usage.py
  8835a94b0ad62dc1f58c861e2025b7c4bc8c0b936c202c64e01bc8b43f53eaa8  plans/round41_c1_verify.py
  38492bf175e0c619596c69911954e3b3c247166bdc240f8c1d44a02b7f4103e0  plans/sources_adopt.py
  c9ca3abe3d4b5dff02d9196e026ab31f7b37347d0866769ac509116fc07afeff  plans/battery41/s_usage.py
$ sha256sum .ufo/waves/round-41/build/R41BatSrcUsage/battery/s_usage.py
  c9ca3abe...c07afeff   (byte-identical to the landed module)
```

The counter digest equals `claims/frozen-digests.txt` (`8835a94b…`) and the tool digest equals the counter's `PINS`
(`38492bf1…`); every counter run below prints `PINS total=2 mismatched=0` and `PINS-AFTER mismatched=0`. The module itself is not
in `frozen-digests.txt` — it is reviewable, which is exactly this seat's mandate ("non-author code review of
battery41 stays part of admission", `plans/round-41-claims.md` C1 *Limits*). Clone tip is `d7c7789` (wave-2 dispatch
commit); the battery, tool and counter blobs are identical at the stated landing tip `3d0058f`.

Envelope used for every counter/battery/fixture run (nested sandboxes inside it):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
      --proc /proc --unshare-pid --die-with-parent <cmd>
```

Scratch `S=/fast/scratch/hyaku/kengaku-r41/F41RevBatSrcUsage`, clone at `$S/lane`
(`git -C "$S/lane" rev-parse --show-toplevel` -> `$S/lane`), battery dir `$S/bat` holding **only** `s_usage.py`.

## 2. Attribution — each mutant dies by THIS module (receipt `scoped-module-only.txt`)

```
$ bwrap … python3 $S/lane/plans/round41_c1_verify.py --lane "$S/lane" --battery-dir "$S/bat" \
      --only S02,S03,S05,S06 --work "$S/w3"
PINS total=2 mismatched=0
FIXTURE s_usage-02-registry-without-package … observed_rc=2 … ok
FIXTURE s_usage-02-package-without-registry … observed_rc=2 … ok
FIXTURE s_usage-03-dotted-access-date … observed_rc=2 … ok
FIXTURE s_usage-03-single-digit-month-duplicate-request … observed_rc=2 … ok
FIXTURE s_usage-05-two-ids-without-entries … observed_rc=2 … ok
FIXTURE s_usage-05-empty-entries-value … observed_rc=2 … ok
FIXTURE s_usage-06-recheck-cadence-word … observed_rc=2 … ok
FIXTURE s_usage-06-recheck-prose-scoped-row … observed_rc=2 … ok
MUTANT S02 sources 2>1 killed by=s_usage-02-registry-without-package -- …
MUTANT S03 sources 2>5 killed by=s_usage-03-dotted-access-date -- …
MUTANT S05 sources 2>0 killed by=s_usage-05-two-ids-without-entries -- …
MUTANT S06 sources 2>0 killed by=s_usage-06-recheck-cadence-word -- …
BATTERY fixtures=8 wrong=0 tampered=0 sidechannel=0
MUTANTS total=4 killed=4 survived=0 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=0/0 sources=4/4
ADVERTISED direct=4 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)      rc=0
```

`killed by=` names only the *first* exhibiting fixture; my per-fixture matrix (§3) shows the second fixture of each
pair exhibits too. The landing measurement's attributions are reproduced unchanged by this module alone
(`measure-final.txt`: S02→`s_usage-02-registry-without-package`, S03→`-03-dotted-access-date`,
S05→`-05-two-ids-without-entries`, S06→`-06-recheck-cadence-word`).

**No accidental credit.** The same module run against all ten sources mutants (receipt `sweep-sources.txt`):

```
$ … --only S01,S02,S03,S04,S05,S06,S07,S08,S09,S11 --work "$S/w4"
MUTANT S01 … SURVIVED exhibits=none      MUTANT S04 … SURVIVED exhibits=none
MUTANT S02 … killed by=s_usage-02-registry-without-package
MUTANT S03 … killed by=s_usage-03-dotted-access-date
MUTANT S05 … killed by=s_usage-05-two-ids-without-entries
MUTANT S06 … killed by=s_usage-06-recheck-cadence-word
MUTANT S07/S08/S09/S11 … SURVIVED exhibits=none
BATTERY fixtures=8 wrong=0 tampered=0 sidechannel=0
MUTANTS total=10 killed=4 survived=6 invalid=0 null_detected=0
```

This module neither claims nor supplies evidence for any mutant outside its four.

## 3. Mutated-line execution — 4/4 (receipt `driver2.out`)

Non-author driver (`driver2.py`): rebuild all 8 fixtures through the frozen counter's own `build_battery`, then run
(a) the reference, (b) the frozen mutation, (c) a **traced mutant** whose mutated line carries its own proof —
`if False:` → `if (print("TRACE-MUT <id>", file=sys.stderr) or False):` (S06: `if False and (` →
`if (print(...) or False) and (`), semantics unchanged — and (d) a traced reference with a print before the guard
showing the operands. All runs inside `bwrap --ro-bind / /`, cwd = the fixture dir.

| mutant | `killed by=` fixture | mutated line executed | reference guard reached with (operands) | reference message |
|---|---|---|---|---|
| S02 | `s_usage-02-registry-without-package` | `TRACE-MUT S02` | `TRACE-REF S02 registry=…/corpus/SOURCES.md package=None` | `--registry and --package are required unless --selftest` |
| S02 | `s_usage-02-package-without-registry` | `TRACE-MUT S02` | `TRACE-REF S02 registry=None package=…/corpus/SOURCES.append.md` | same |
| S03 | `s_usage-03-dotted-access-date` | `TRACE-MUT S03` | `TRACE-REF S03 access_date='26.10.2026'` | `--access-date must be an ISO date (YYYY-MM-DD)` |
| S03 | `s_usage-03-single-digit-month-duplicate-request` | `TRACE-MUT S03` | `TRACE-REF S03 access_date='2026-1-5'` | same |
| S05 | `s_usage-05-two-ids-without-entries` | `TRACE-MUT S05` | `TRACE-REF S05 entries=''` | `--entries is required when --admit-ids is given (used-by has no fallback)` |
| S05 | `s_usage-05-empty-entries-value` | `TRACE-MUT S05` | `TRACE-REF S05 entries=''` | same |
| S06 | `s_usage-06-recheck-cadence-word` | `TRACE-MUT S06` | `TRACE-REF S06 recheck='monthly'` | `--recheck must be an ISO date, <N>d, or a known symbolic cadence` |
| S06 | `s_usage-06-recheck-prose-scoped-row` | `TRACE-MUT S06` | `TRACE-REF S06 recheck='every 30 days'` | same |

No dead-site credit: the traced mutant line prints on every fixture that kills, and prints on *no* fixture whose
reference stops at an earlier guard (e.g. `S06`'s trace is absent on all six non-killing fixtures — the guard chain
short-circuits before it, exactly as the frozen `main()` order dictates). **e = 4/4.**

## 4. Per-fixture verdicts

| # | fixture | verdict | evidence |
|---|---|---|---|
| 1 | `s_usage-02-registry-without-package` | **honest** | ref rc 2 at the frozen line with `package=None`; mutant rc 1 from `collect()` line 185 `AttributeError: 'NoneType' object has no attribute 'read_text'`; the mutant line executes. The fixture's advertised subject ("`--package` forgotten, every other flag of a real adoption present") is exactly what the argv shows; the kill is caused solely by the removed guard. |
| 2 | `s_usage-02-package-without-registry` | **honest** | second operand: `registry=None`, mutant rc 1 at line 186 `registry.read_text`; same reasoning. |
| 3 | `s_usage-03-dotted-access-date` | **honest** | ref rc 2 with `access_date='26.10.2026'`; mutant rc 5 and stdout `missing: S131:not-opened-this-round` — a direct consequence of the non-ISO string reaching `build_block` (control: the same mutant with `--access-date 2026-10-26` exits **0**, so the 5 is date-caused). |
| 4 | `s_usage-03-single-digit-month-duplicate-request` | **incidental** | ref rc 2 with `access_date='2026-1-5'` (honest reference side, line executes) but mutant rc 5 with stdout `missing: duplicate-request`, and the control **`ref_rc=5 mut_rc=5`** with the date replaced by `2026-10-26`: the mutant's exit is date-insensitive, so the fixture isolates nothing about the date guard. Comment names both triggers; author disclosed the mechanism in wave 1. |
| 5 | `s_usage-05-two-ids-without-entries` | **honest** | ref rc 2 at the entries guard (`entries=''`); mutant rc 0 and writes two rows with used-by `—` (meaning "no fallback"), i.e. it exhibits exactly the degradation the guard prevents. |
| 6 | `s_usage-05-empty-entries-value` | **honest** | `--entries ""` is accepted by argparse (observed rc 2, not a parser complaint), so the refusal really is `not args.entries`; mutant rc 0 with one row ending `180d | — |`. |
| 7 | `s_usage-06-recheck-cadence-word` | **honest** | ref rc 2 at the recheck guard (`recheck='monthly'`); mutant rc 0 writes the block with the packaged `180d` cell — the invalid flag value is silently ignored, exactly the behaviour the guard exists to prevent. |
| 8 | `s_usage-06-recheck-prose-scoped-row` | **honest** | ref rc 2 (`recheck='every 30 days'`); mutant rc 0 writes `| S133 | … | mined | 2026-10-26 | every 30 days | … |` after `normalized recheck S133: …` — the strongest demonstration in the module: the CLI default rewrites a prose recheck cell with a non-cadence. |

`h = 7/8`. Verdicts 1/2 carry the crash caveat of §0 (mutant exits via an uncaught exception, which is legitimate
under the frozen kill rule `2>1` and is unambiguous because `SKILL.md:573` advertises no exit `1` for this tool).

## 5. Wave-1 counterexample-vector audit — none present

| vector (wave 1) | present? | evidence |
|---|---|---|
| reads the counter's scratch root / `variants/` / slot file | **no** | module has **no** read call of any kind: `grep -n "open(\|read_text\|read_bytes\|/proc\|socket\|__file__\|inspect\|variants\|slots" plans/battery41/s_usage.py` → only line 7, the docstring word `witness's`. The only file operations are `ctx.write(reg, …)` and `ctx.write(pkg, …)` (lines 52/54), both under `d`; `Ctx.write`/`Ctx._inside` refuse anything outside `d`; `tampered=0` in every run. |
| `/proc`, ppid, cmdline, environ | **no** | no token in the module text (counter: `sidechannel=0`); the module's argv carries no such path. |
| relative `../` argv token | **no** | the only relative token is `--entries corpus/knowledge/tb2-constraints-scheduling-grader.md`, no `..`, and it is **never opened**: `sources_adopt.py:1061` only splits it (`entries = [item for item in args.entries.split(",") if item]`), `build_block` uses it as the used-by cell. Proof: the S05/S06 mutants exit 0 while that path does not exist in the fixture dir. |
| AF_UNIX sockets / SysV IPC / `fork`-style side channel | **no** | the module builds no executable content: `driver2.out` lists exactly two files per fixture and nothing else (`8 × corpus/SOURCES.md`, `8 × corpus/SOURCES.append.md`, 16 `FILE` lines for 8 fixtures — pure markdown tables); there is no script, stub, `sh`/`git` call, or subprocess in the module at all (`grep -n "ctx\.sh\|ctx\.git\|ctx\.init"` → no hits). |
| reads the tool's or counter's program text | **no** | `grep -n "^import\|^from"` → `11:from __future__ import annotations` only. Empirically: rebuilding and rerunning all 8 fixtures with the **whole lane `tmpfs`-hidden** gives identical results — `ref=2 refhide=2` on 8/8 and mutant rc identical on 8/8 (`driver2.out`). |
| probe stub that branches on anything but its committed bytes | **n/a** | no probe stub exists in this module; the tool under test is the lane's `sources_adopt.py` (via the counter's `PINS`-checked source), so every verdict is produced by tool code. |

## 6. Independence from the witness modules

- Frozen rule: "The battery may not import, copy or read the witness modules" (`round-41-claims.md` C1 *Work*).
  `s_usage.py` imports nothing, opens nothing; no path under `.ufo/…/claims/` appears in its text.
- Shapes differ from `claims/witness/w_sources.py`: witness uses flat `reg.md`/`pkg.md`, one id `S900`, date
  `2026/10/25`, `--recheck soon`, and `b02` is a zero-argument invocation; `s_usage` uses a lane-shaped
  `corpus/SOURCES.md` (two rows S118/S124) + `corpus/SOURCES.append.md` (S131/S132/S133), and its triggers are
  `26.10.2026`, `2026-1-5` (+ duplicate id), `--entries ""`, `monthly`, and a scoped prose recheck.
- Independence is demonstrated, not asserted: with **only this module** in the battery dir, all four mutants die
  (§2) — the witness modules are not loaded, imported or consulted by the counter.

## 7. Findings for the L1 (no lane file edited by this seat)

- **F1 (incidental kill, smallest safe correction).** `s_usage-03-single-digit-month-duplicate-request` should be
  made date-caused or dropped. Smallest edit: `--admit-ids "S131,S131"` → `--admit-ids "S131"` (keep
  `--access-date 2026-1-5`); the mutant then exits 5 via `missing: S131:not-opened-this-round`, which is caused by
  the non-ISO spelling. Dropping the fixture is equally safe: `s_usage-03-dotted-access-date` already carries S03,
  and the frozen predicate (`killed=23`, `sources=10/10`) is unchanged either way because `killed by=` stays on
  `-03-dotted-access-date`. Leaving it is *not* an admission failure; it is a redundancy that reads as stronger
  evidence than it is (the wave-1 load-bearing table implies either `-03-*` fixture can carry the mutant; only one
  can honestly).
- **F2 (calibration vocabulary, no edit possible this round).** For `sources`, every `2>1` pair in the frozen table
  (S02, S08) is satisfied by an uncaught-exception rc, not by an advertised exit-1 behaviour — `SKILL.md:573`
  advertises `0,2,3,4,5,6,7,8,9` and no `1`. That is fine for the kill rule but should be recorded on the direction
  class so a later round does not read `2>1` as "defect found".
- **F3 (admission).** Nothing in this module fails C1 admission: the four kills are attributable, the mutated lines
  execute, no wave-1 vector is used, the witness modules are untouched, and `PINS`/`PINS-AFTER` are clean. The one
  incidental fixture does not change any frozen number.

## 8. Host safety and bounds

- Every counter run, fixture build and traced tool run went through the mandated envelope; the counter nested its
  own `--ro-bind / /` sandboxes inside it. Nothing was written to `~/.local/bin`, `/usr`, `/etc`, `$HOME`, the fleet
  root, the lane, or any sibling lane; `git` was called read-only (`rev-parse`, `log`, `diff`, `cat-file`) on the
  clone, whose toplevel was asserted; no `pacman`, no installs, no services touched.
- Writes: this report and its receipts only —
  `.ufo/waves/round-41/falsify/F41RevBatSrcUsage/{F41RevBatSrcUsage.md, scoped-module-only.txt,
  sweep-sources.txt, driver.out, driver2.out, driver2.py}` (created 16:18).
- Scratch `/fast/scratch/hyaku/kengaku-r41/F41RevBatSrcUsage` removed before this seat ends; no clone, mirror or
  corpus tree was copied into the report dir.

VERDICT: battery41-s_usage-honest-7/8-mutated-line-executed-4/4
