# F41RevRider — rider review: `plans/routed_open.py` + `corpus/routed-findings.jsonl`

Seat F41RevRider, kengaku round 41 wave 2 (falsify), 2026-10-26.
Measured at lane HEAD `d7c77895752a2a5f317fa22f2362416ada50a04b` (wave-2 dispatch commit); the goal's frozen tip
`3d0058fbde484c9d6c23fd997d9ee09a0663bcdb` is an ancestor (`git merge-base --is-ancestor` → ok) and the only dirty
entries are this wave's own `.ufo/waves/round-41/falsify*`. No lane file was written by this seat; every command below
is read-only against the lane or runs in scratch `/fast/scratch/hyaku/kengaku-r41/F41RevRider` (removed at the end;
receipts first copied to `falsify/F41RevRider/`).

## 1. What I ran

| run | command (cwd = lane root unless noted) | observed |
|---|---|---|
| selftest | `TMPDIR=$S python3 plans/routed_open.py --selftest` | `SELFTEST 12/12`, rc=0 |
| list | `python3 plans/routed_open.py --list` | 10 ROW lines; `ROWS total=10 open=4 blocked=1 closed=5 refused=0`; `routed_open=5 oldest_round=39` |
| observe (plain) | `TMPDIR=$S python3 plans/routed_open.py --observe --timeout 120` | `OBSERVE rows=10 mismatched=0`, rc=0; **byte-equal** to the wave-1 receipt `.ufo/waves/round-41/integrate/routed-observe.txt` (`diff` → empty) |
| observe (bwrap) | `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent env TMPDIR=$S python3 plans/routed_open.py --observe --timeout 120` | rc=0, **byte-equal** to the same receipt again (`bwrap-observe-byte-equal`) |

The rider's printed line is actually consumed by the round docs: SCORECARD.md:1565 quotes
`ROWS total=10 open=4 blocked=1 closed=5 refused=0` + `SELFTEST 12/12`; LOG.md:1256 quotes `routed_open=5 oldest_round=39`.
No tool installs were needed (stdlib python3 only).

## 2. Row-by-row honesty at the tip — 10/10 statuses honest

Every `source` citation was opened; every `close` claim re-measured; every `check` either re-run (via `--observe`) or
inspected. Per-row detail:

- **R39-R1 closed — honest.** `git show ec17216:SKILL.md` shows both rows at :590 (`order-check`, verdict map 0/1/2) and
  :591 (`round39-c1-audit`); commit `ec1721684458…` (round-40 landing, "kengaku-shokunin", +99 SKILL.md) is an ancestor.
  The check greps both row names off SKILL.md — it tests exactly what round-39 §5 R1 routed (registration with verdict map).
- **R39-R2 open — honest.** Re-measured: `python3 plans/git_leak_probe.py --lane . --work <absent dir>` → traceback
  `FileNotFoundError … '/fast/scratch/…/absent-dir/k39-glr-yyteuj4_'` from `tempfile.mkdtemp` (plans/git_leak_probe.py:258),
  `probe_exit=1`; `--observe` prints `rc=1 observed=fail self=open` — consistent. The note's measurement ("at tip fc79f2a4")
  still holds at `d7c7789`.
- **R39-R3 blocked — honest.** `wc -l corpus/defects.jsonl` → 5; `grep -c '"order'` → 0; `plans/ledger_tip.py:72-73` binds
  `corpus/defects.jsonl` to `plans/defect_ledger.py` CHECKS; `plans/round40_c1_verify.py:98` PINS `ledger_tip.py` by sha256;
  `plans/round-41-claims.md:126-128` records the block ("recorded `open, blocked` in the rider's file"). Check currently
  fails (0 matches) → consistent with `blocked`.
- **R39-R4 open — honest, with an inert check.** All six note sub-items verified: (b) `plans/round_close.py:79`
  `ORDER_TOOL = "plans/order_check.py"` wired at :176-186/:313-314; (c) `plans/tip_receipts.py --list` prints
  `origin=derived` rows (git-leak-probe, db-wal-probe, constraints-probe); (a) `git log -- plans/order_check.py` → only
  `34158b0` (round-39), unedited since; (d) `corpus/lessons/round-40.md:106` carries the F39LedgerTip D1 disposition;
  (e) `plans/mutant_direction_check.py:91-101` refuses any non-round-38-list counter (observe `rc=2`); (f) repairs landed in
  `round41_c1_verify.py` but F1–F4 remain open (see R40-R1). Caveat: the row's own check can never pass for this list
  (always SETUP exit 2) — the note admits it — so `--observe` gives this row zero closure signal; the status is still right.
- **R39-R5 closed — honest.** `ls -d /fast/scratch/hyaku/kengaku-r39*` → `No such file or directory` (both the exact dir and
  the wildcard). Nuance: the check tests only `test ! -e …/kengaku-r39` (exact name), strictly weaker than the close's
  wildcard claim; the claim itself is true, so the status stands.
- **R40-R1 open — honest (the key question).** F1–F4 are real and still open at the tip: `path_ok`
  (plans/round41_c1_verify.py:349-356) validates only tokens that `startswith("/")`, so relative argv escapes the fixture
  dir (F4); the tool-run bwrap argv (:318) carries `--unshare-pid --unshare-net` but no IPC isolation (F2 AF_UNIX, F3 SysV
  IPC — confirmed by `.ufo/waves/round-41/build/R41SentinelCounter.md:57,85,115,135`); the mutant variant is bound into
  every tool run (:61), so a probe stub can read it (F1). The "partly addressed" half is also true: fixed system PATH
  (:116, :246, :485), lane hidden via `--tmpfs` (:57), scratch inside the lane refused (:532). Routed onward at
  SCORECARD.md:1650, which cites this row.
- **R40-R2 closed — honest.** `.ufo/waves/round-41/build-spec.json` (line 5, the seat-facing `context`) carries
  `--ro-bind /home/vgpnk/.local/bin`; both round-40 attack modules open with `raise SystemExit("NEUTRALIZED …")`
  (`crit_git_shim.py:10`, `crit_ledger_selfread.py:9`); 24/38 wave-1 build reports carry the envelope string
  (`grep -rln 'ro-bind /home/vgpnk/.local/bin' .ufo/waves/round-41/build/*.md | wc -l` → 24). Nuance: the check tests the
  spec *text*, not seat enforcement; enforcement is evidenced by the wave-1 reports, not by this check.
- **R40-R3 closed — honest.** SKILL.md:598 `round-close-check` gate row with a 0/1/2 verdict map and self-test spelling;
  SKILL.md:649+ "Round-41 registry addendum" carries the derived-mapping paragraph ("The `tip-receipts` derived mapping
  (round 40) is strict…"). The routed item's pricing half was done by `R41RoundCloseMut` (14 residuals re-measured,
  `corpus/lessons/round-41.md` §Routed R3: "Rows landed; pricing done, fixes not") and routed forward — the close text
  claims only the registration, which is real.
- **R40-R4 closed — honest.** `.ufo/waves/round-41/claims/control-c1-nothing.txt:28` reads
  `ADVERTISED direct=21 indirect=2 none=0`; `plans/round41_c1_verify.py:586-590` tallies `adv_kind` into
  `{direct, indirect, none}` and marks any other value `invalid` — the none category is handled as the close says.
- **R40-R5 open — honest.** `plans/round41_c2_verify.py:286-290` creates `--work` (`mkdir(parents=True, exist_ok=True)` +
  `TemporaryDirectory(dir=a.work)`) — the round-40 traceback fixed in the round-41 counter; `plans/round40_c2_verify.py`
  untouched since `bbb1095` (the round-40 freeze; `git log` → single commit); `corpus/lessons/round-40.md:106` carries the
  three carried residuals; `.ufo/reports/round-41/` does not exist, so the W04 census-line item (D3) is genuinely
  unverifiable yet (6/38 build reports mention W04 today; the note's "3 of 15 at 2026-10-26T18:42Z" was true when written).

## 3. Missing routed items

- **round-39 §5 (R1–R5) → rows R39-R1…R39-R5: nothing missing.** Sources `:132/:134/:135/:136/:140` all land on the
  corresponding routing sentences (checked line-by-line).
- **round-40 §5 (R1–R5) → rows R40-R1…R40-R5: nothing missing.** Sources `:92/:95/:97/:99/:101` all match.
- **Gap to append (not a landed defect):** `corpus/lessons/round-41.md` §Routed (landed `0d57419`, after the rider file at
  `74513c06`) routes R3's 14 open `round_close.py`/`tip_receipts.py` residuals to round 42 — the rider file has no R41-*
  rows. Before the round-41 close quotes `routed_open=<n>`, those must be appended, or the burn-down undercounts the
  round's own routings. (R40-R1's F1–F4 are already covered by that row's note.)

## 4. Can the file be gamed? Yes — demonstrated in scratch fixtures (receipts `G1`–`G7`)

Fixtures: `mktemp -d -p $S` + `git init`, one findings file each, real `routed_open.py`. Outputs in
`falsify/F41RevRider/G*.txt`.

| probe | row under test | observed | meaning |
|---|---|---|---|
| G1 | closed, `check:"true"`, close `"fabricated deadbeef absent.md:1"` | `observed=pass … mismatched=0`, rc=0 | A closed row with a vacuous check and **fabricated close evidence** sails through: `validate()` never inspects `close` content (the selftest's own good row uses `"abc123 lesson.md:2"` — also unverified). |
| G2 | closed, `check:null`, fabricated close | `observed=n/a … mismatched=0`, rc=0 | A closed row needs **no check at all**; `--observe` cannot catch it. |
| G3 | closed, check = `grep -q '"status": "closed"' corpus/routed-findings.jsonl`, work never done | `observed=pass … mismatched=0`, rc=0 | The **self-certifying row**: the check body is arbitrary shell and may test the file's own claim instead of reality. Fully self-consistent lie, undetectable by the tool. |
| G4 | closed, check = `touch pwned.txt` | file created in the fixture lane (`ls` + `git status` show `pwned.txt`) | `--observe` runs checks with `shell=True, cwd=lane` **unsandboxed** — a hostile findings file is arbitrary code execution at observe time, with write access to the lane. (I ran my observe passes with `TMPDIR` pinned to scratch and under the bwrap envelope; the landed checks only grep/test/mktemp-under-TMPDIR.) |
| G5 | refused, blocker `"decided not to"` | `routed_open=0 oldest_round=-`, rc=0 | A **refusal dodges the burn-down**: the tally counts only open+blocked, and blocker text is unverified prose. |
| G6 | closed, check = `false` | `MISMATCH … mismatched=1`, rc=1 | The one real protection — a closed row whose check fails is caught. It works. |
| G7 | `--file ledger-copy.jsonl` (renamed copy of a ledger-shaped file) | accepted, `routed_open=1`, rc=0 | The pinned-ledger guard (`is_ledger`) is **name-based only**; a renamed copy bypasses it. Minor — the guard's purpose is to keep the rider off the pinned ledgers, and the default path is safe. |

Also noted: R39-R2's check writes `${TMPDIR:-/tmp}` — anyone running `--observe` without `TMPDIR` pinned writes `/tmp`
against the scratch rule; pin `TMPDIR` (as both my passes did).

## 5. Residual risk and verification gaps

- The rider's honesty rests on author discipline, not the tool: `close`, `blocker` and `check` are unvalidated prose/shell.
  The **landed file is clean** — every closed row's evidence is real and every present check is meaningful (two strength
  nuances: R39-R5's check is narrower than its close claim; R40-R2's check tests spec text, not enforcement) — but the
  design permits a self-certifying closed row (G3) that no run of the tool can catch.
- `--observe` is an unsandboxed arbitrary-shell executor keyed off a lane file (G4); future observe runs should keep the
  bwrap envelope and a pinned `TMPDIR`, as the wave-1 receipt and my re-runs did.
- I did not execute the C1/C2 counters or the battery (out of my seat's scope); F1–F4 openness is verified from
  `R41SentinelCounter.md` plus the counter source at the tip, not by re-deriving the attacks.

## 6. Receipts

`falsify/F41RevRider/`: `observe-mine.txt`, `observe-bwrap.txt` (both byte-equal to
`.ufo/waves/round-41/integrate/routed-observe.txt`), `G1.txt`–`G7.txt`, `gaming.sh`. Scratch
`/fast/scratch/hyaku/kengaku-r41/F41RevRider` removed after copying (target checked against `$S` before `rm -rf`).

VERDICT: rider-rows-honest-10/10
