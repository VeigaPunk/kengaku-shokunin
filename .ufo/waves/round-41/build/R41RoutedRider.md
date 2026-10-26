# R41RoutedRider — routed-findings burn-down (proposal 1 as a rider)

Seat: executor, round 41 wave 1. Lane tip measured: `fc79f2a49be0221e138b3885fa0d83bc43b31a42` (2026-10-26T18:42Z).
Lane repo untouched: no writes outside `.ufo/waves/round-41/build/R41RoutedRider/` and
`/fast/scratch/hyaku/kengaku-r41/R41RoutedRider/` (removed before this report). No git mutation anywhere.

## What landed

| file (under `.ufo/waves/round-41/build/R41RoutedRider/`) | sha256 (first 16) | what |
|---|---|---|
| `routed_open.py` (245 lines) | `3ce44d941b14a28c` | stdlib burn-down reader for one JSONL file; `--selftest`, `--list`, `--observe` |
| `routed-findings.jsonl` (10 rows) | `d6cf5803bf5676ad` | seed: one row per routed item R1–R5 of `corpus/lessons/round-39-verifier-spotcheck.md:132-140` and `corpus/lessons/round-40-verifier-spotcheck.md:92-101` |
| `run.txt`, `run-observe.txt`, `run-list.txt`, `selftest.txt`, `measure-tip.txt` | — | receipts quoted below |

Reading of D7 (`F40CritPlanNext.md:174-184`): keep **one printed line and one file**, and put the rows in a
sibling append-only file that `plans/ledger_tip.py` does not read, so the round-40 C1 pin is untouched.

* One file only: `--file` defaults to `<lane>/corpus/routed-findings.jsonl`; the tool refuses any basename
  starting `defects` with exit 2, so it can never read or move `corpus/defects.jsonl` /
  `corpus/defects-round35.jsonl` (the files `plans/ledger_tip.py:6-7,72-73` binds to `defect_ledger.py` checks).
* One line: `routed_open=<n> oldest_round=<r>`, exit 0; `n` = rows with status `open` or `blocked`
  (a `refused` row is a decision, not a burn-down item); `r` = smallest `opened_round` among them, `-` if none.
* Never a green on a broken file: a malformed row, a duplicate id, a closed row without `close` evidence, a
  blocked/refused row without `blocker`, a bad status/round, or a `source` path/line that is absent prints
  `DEFECT line=<n> …` + `ROWS total=<n> invalid=<n>` and exits 1 **without** the summary line, so a round close
  cannot quote a number off a broken file.
* Append-only is read strictly: an id appears once, ever; a second row for an id is a defect, not an update
  (the summary is the row's current status, so a burn-down closes a row by editing it, never by re-appending).
* `--observe` is the anti-rot leg D7 asks for in spirit: it runs each row's `check` from the lane root and prints
  `OBSERVE <id> rc=<n> observed=pass|fail self=<status>`; `closed`/`refused` must pass, `open`/`blocked` must
  fail, a mismatch exits 1. Without it the count would be a file that a do-nothing round reprints.

Row schema: `id, class, source (file:line), opened_round, status (open|closed|refused|blocked), close, blocker,
check, note`. `source` is validated against lane bytes (file exists, line in range and non-blank), so a lesson
reflow cannot silently orphan a row.

## Seed rows and their status at the tip

| id | source | status | measured evidence |
|---|---|---|---|
| R39-R1 | `round-39-…:132` | closed | registry rows exist: `SKILL.md:590` order-check, `SKILL.md:591` round39-c1-audit, added by `ec17216` |
| R39-R2 | `:134` | open | absent `--work` still tracebacks: `FileNotFoundError` from `tempfile.mkdtemp` (`plans/git_leak_probe.py:258`), rc=1 |
| R39-R3 | `:135` | blocked | `corpus/defects.jsonl` = 5 R34 rows only; pinned via `plans/ledger_tip.py:6-7,72-73` + `plans/round40_c1_verify.py:98`; block recorded `plans/round-41-claims.md:126-128` |
| R39-R4 | `:136` | open | 2 of 6 sub-items closed: Q30 wired (`plans/round_close.py:14`), tip_receipts derives the round-39 receipt. Open: order_check fail-open (`plans/order_check.py` unedited since `34158b0`), `F39LedgerTip` D1 (`corpus/lessons/round-40.md:106`), direction check refuses the r39 list, C1 repairs in flight |
| R39-R5 | `:140` | closed | `ls -d /fast/scratch/hyaku/kengaku-r39` → rc=2 (absent) |
| R40-R1 | `round-40-…:92` | closed | `plans/round41_c1_verify.py:116` fixed PATH; `:318` `--ro-bind / /`; tool runs wrapped at `:417`; frozen in `plans/round-41-claims.md:46-48` |
| R40-R2 | `:95` | closed | envelope in every seat prompt: `.ufo/waves/round-41/build-spec.json:5` (`1` match for `ro-bind /home/vgpnk/.local/bin`); both attack modules stay neutralized (`crit_git_shim.py:10`, `crit_ledger_selfread.py:9`) |
| R40-R3 | `:97` | open | no `round-close` gate row (`grep -c '^| \`round-close\`' SKILL.md` → 0); `SKILL.md:586` does not name the derived mapping |
| R40-R4 | `:99` | closed | `control-c1-nothing.txt:28`: `ADVERTISED direct=21 indirect=2 none=0` over the 23 frozen mutants; `none` handled at `plans/round41_c1_verify.py:586,590` |
| R40-R5 | `:101` | open | `round40_c2_verify --work` traceback fixed in the round-41 counter (`plans/round41_c2_verify.py:290`); order class still blocked, `F39LedgerTip` D1, `F39MutDirection`, `F39OrderGateMut` fail-open, W04 census line unverified (close report not filed) |

Counts: 5 closed, 4 open, 1 blocked, 0 refused → `routed_open=5`, `oldest_round=39`.

## Exact outputs

Tool, at the lane tip (`run.txt`, exit 0):

```
ROWS total=10 open=4 blocked=1 closed=5 refused=0
routed_open=5 oldest_round=39
```

Self-assessment vs observation (`run-observe.txt`, exit 0 — 0 mismatched):

```
OBSERVE R39-R1 rc=0 observed=pass self=closed
OBSERVE R39-R2 rc=1 observed=fail self=open
OBSERVE R39-R3 rc=1 observed=fail self=blocked
OBSERVE R39-R4 rc=2 observed=fail self=open
OBSERVE R39-R5 rc=0 observed=pass self=closed
OBSERVE R40-R1 rc=0 observed=pass self=closed
OBSERVE R40-R2 rc=0 observed=pass self=closed
OBSERVE R40-R3 rc=1 observed=fail self=open
OBSERVE R40-R4 rc=0 observed=pass self=closed
OBSERVE R40-R5 self=open observed=n/a
OBSERVE rows=10 mismatched=0
```

Selftest, `--selftest` (`selftest.txt`, exit 0): 12/12 cases, each a real row through the real validator on a
temp lane — `valid-closed` rc=0; `malformed-json`, `missing-key`, `duplicate-id`, `closed-without-evidence`,
`blocked-without-blocker`, `bad-status`, `source-past-eof`, `source-missing-file`, `bad-opened-round`,
`bad-id` all rc=1; `defect-ledger-guard` rc=2. Closing line: `SELFTEST 12/12`.

Guard and setup, measured in the lane root:

```
$ python3 …/routed_open.py --lane . --file corpus/defects.jsonl
SETUP refusing defects.jsonl: the defect ledgers are pinned by plans/ledger_tip.py
exit=2
$ python3 …/routed_open.py --lane .
SETUP routed-findings file missing: …/corpus/routed-findings.jsonl
exit=2
```

Per-row measurements (`measure-tip.txt`, command → first line of output, cut from the receipt):

```
$ grep -nE '^\| `(order-check|round39-c1-audit)`' SKILL.md
590:| `order-check` | gate | …
591:| `round39-c1-audit` | gate | …
$ git log -S'`order-check`' --oneline -- SKILL.md | tail -1
ec17216 round-40: battery40 …
$ python3 plans/git_leak_probe.py --lane . --work "$TMPDIR/absent"   → rc=1
FileNotFoundError: [Errno 2] No such file or directory: '…/absent/k39-glr-ejose9sm'
$ wc -l corpus/defects.jsonl            → 5 corpus/defects.jsonl
$ grep -c '"order' corpus/defects.jsonl → 0 (rc=1)
$ python3 plans/mutant_direction_check.py --lane . --counter plans/round39_c1_verify.py → rc=2
SETUP counter plans/round39_c1_verify.py is not a round-38-list counter: missing=battery38_fixtures,attributed
$ python3 plans/tip_receipts.py --lane . --list | grep round39
receipt corpus/evidence/round39/git-leak-probe.txt kind=byte script=plans/git_leak_probe.py origin=derived …
$ git log --oneline -1 -- plans/order_check.py  → 34158b0 round-39: …
$ ls -d /fast/scratch/hyaku/kengaku-r39  → rc=2
$ grep -n 'PATH = "|"--ro-bind", "/", "/"' plans/round41_c1_verify.py
116:PATH = "/usr/local/sbin:/usr/local/bin:…
318:    argv = [BWRAP, "--ro-bind", "/", "/", "--dev", "/dev", "--proc
$ grep -c 'ro-bind /home/vgpnk/.local/bin' .ufo/waves/round-41/build-spec.json → 1
$ grep -c NEUTRALIZED …/crit_git_shim.py …/crit_ledger_selfread.py → 1 and 1
$ grep -c '^| `round-close`' SKILL.md → 0 (rc=1)
$ grep -n ADVERTISED .ufo/waves/round-41/claims/control-c1-nothing.txt
28:ADVERTISED direct=21 indirect=2 none=0
$ grep -n 'mkdir(parents=True, exist_ok=True)' plans/round41_c2_verify.py
290:        pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
$ grep -rl W04 .ufo/waves/round-41/build/*.md | wc -l → 3 ; ls .ufo/waves/round-41/build/*.md | wc -l → 15
```

## Integration notes for the L1 (not done here)

1. The tool belongs at `plans/routed_open.py` with the seed at `corpus/routed-findings.jsonl`; both artefacts are
   lane-relative and already run from the lane root. Nothing references them yet — a round close that does not
   invoke `routed_open.py` prints no line, exactly the D7 failure mode.
2. Proposal 1's tripwire ("freeze refuses a new coverage claim while the oldest open finding is more than two
   rounds old") is **not** implemented: it needs a call inside the freeze path (`order_check.py`/`round_close.py`/
   the claims template) plus a decision on whether `blocked` ages. This rider delivers the readout the tripwire
   would read; wiring it is a separate, priced change.
3. Two rows are bundles (R39-R4, R40-R5) with one check or none; their `note` carries the per-sub-item state.
   Splitting them into one row per residual is a schema-compatible follow-up (new ids), but would retro-fit the
   round-39/40 texts, so it was left to the integrator.
4. Adding real rows to these ledgers later must go through a fresh id; the tool's duplicate-id defect enforces it.

## Risks / limits, stated

* Statuses are point-in-time at `fc79f2a4`; several sibling seats are editing `SKILL.md` for R40-R3 right now, so
  that row may flip to closed before the tip lands. Re-run `--observe` at the landing tip.
* `--observe` runs each row's shell `check` unsandboxed from the lane root (read-only commands only, one 180 s
  cap); R39-R2's check uses `mktemp -d -p "${TMPDIR:-/tmp}"` and removes it — run it with `TMPDIR` on scratch.
* A row's `check` is a convention, not a proof: a check can be written to pass while the finding is live. The
  seed's checks are the measurements above; they were each exercised and match the declared status 10/10.
* Host safety: no shared-PATH, `$HOME`, `/usr` or `/etc` write; the `mktemp` dir above is the only path outside
  the build dir and scratch, created and deleted by the check itself. Scratch
  `/fast/scratch/hyaku/kengaku-r41/R41RoutedRider/` removed after copying receipts here.
* Tooling: nothing installed or upgraded.

VERDICT: rider-rows-10-open-5-oldest-39
