# R42RegistryRows — SKILL.md gate/probe registry rows for round 42 (draft for the L1)

Seat `R42RegistryRows`, round 42 wave 1 (scribe). Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Everything below was measured on a **clean clone** of tip `fda71ae` (round-42 wave-1 dispatch; the freeze is
`bc856d8`, the first recorded probe run `523b278`) at
`/fast/scratch/hyaku/kengaku-r42/R42RegistryRows/lane` — `git -C … rev-parse --show-toplevel` printed that path.
Nothing frozen was edited; no lane file was touched (draft only). Rows are drafted for the L1 to integrate.

Axes: **operability** (each row's command, selectors, exit codes and write scope must be usable by the next
seat) and **calibration** (each row's verdict map and control numbers must be the numbers the tool actually
prints today, not the freeze's numbers). Moves kept: a row only for facts I reproduced; where a freeze control
string has gone stale I keep the row and record the delta verbatim instead of quoting the freeze.

## Q32 envelope (every counter/battery/probe run below)

```
ENVELOPE /usr/bin/bwrap --dev-bind / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
  --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>
start 17:22:57   (clone: 17:22:57)
end   17:28:55
ls -A /home/vgpnk/.local/bin | sha256sum  before 436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18
                                          after  436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18  (unchanged)
```
Additional runs for the two later receipts: C1 at 17:27:43–17:27:44, C2 at 17:27:43–17:28:49 (66.7 s, exit 1).
Every run used `TMPDIR`/`--work` under `/fast/scratch/hyaku/kengaku-r42/R42RegistryRows`; no PATH directory was
written.

## 1. The rows (exact 8-column shape of the round-41 rows, `SKILL.md:559` header)

```markdown
| `round42-c1-mutants` | gate | `python3 plans/round42_c1_verify.py --lane .` (lane root; `--battery-dir DIR` and `--only X1,XO5` are development selectors printing `PREDICATE C1 n/a` — they still exit 1 on any survivor in the subset (measured: `--battery-dir <empty> --only X1` → `survived=1`, `PREDICATE C1 n/a`, exit 1); `--work DIR` created if absent and **refused inside the lane** (measured: exit 2); `--jobs N` parallel tool runs, default 8) | `0` frozen predicate holds: `PINS total=2 mismatched=0`, `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=14 killed=14 survived=0 invalid=0 null_detected=0 unattributed=0`, `MUTANTS-BY-TOOL anchor=9/9 order=5/5`, `PINS-AFTER mismatched=0`, then `PREDICATE C1 pass` (`:665`) · `1` any `SURVIVED` (printed `exhibits=<directions>`), any `UNATTRIBUTED` hit (a direction hit whose traced re-run neither reproduces (exit, class set) nor executes a line of the replaced span), an `invalid`, `invalid(compile)` or `invalid(variant changed during the run)` mutant, a `NULL … differs on a second unmodified run`, `wrong>0`, `tampered>0`, `sidechannel>0`, a pin mismatch before or after the run, `len(MUTANTS)!=14`, or a per-tool count other than `anchor=9/9 order=5/5` (`:660-665`) · `2` setup: `/usr/bin/bwrap` or `/usr/bin/python3` not executable, `--work` (or the scratch root) inside the lane, a battery module that breaks the contract, or a duplicate fixture id (`:530-554`) | controls `.ufo/waves/round-42/claims/control-c1-nothing.txt` (`BATTERY fixtures=0`, `survived=14`, `anchor=0/9 order=0/5`, `PREDICATE C1 fail`, `exit=1`) re-measured unchanged on the clean clone; `control-c1-attribution.txt` (`attributed span forced to line 1` → `unattributed=14`, fail — leg f can fail); `control-c1-tool-edited.txt` (`PINS mismatched=1`, 9 invalid); `control-c1-no-mutants.txt` (`MUTANTS total=0`, fail — non-vacuity); `control-c1-hostile-escape.txt` (`SETUP … breaks the contract`, exit 2); pre-freeze witness `claims/witness-run.txt` (`14/14 killed, attributed`, development mode) | `PINS` = `plans/anchor_digest_check.py` `11bb2cad…`, `plans/order_check.py` `948d5e1d…`; `TOTAL=14`, `FLOORS={anchor:9, order:5}`; the 14 frozen ids X1 X3 X6 X7 X9 X12 X13 X14 X15 (anchor) and XO1 XO3 XO5 XO6 XO7 (order), `ADVERTISED direct=13 indirect=1 none=0` (measured); counter digest `559fca0c…` in `.ufo/waves/round-42/claims/frozen-digests.txt` | scratch under `--work`/`$TMPDIR` only — every fixture build and every tool run in its own read-only `bwrap` sandbox, the lane hidden from builds; verified with the lane bound read-only (`--ro-bind`): identical predicate, lane `git status --porcelain` empty | kengaku |
| `round42-c2` | gate | `python3 plans/round42_c2_verify.py --lane .` (lane root; `--work DIR` scratch parent, **created if absent**) | `0` `checks=9 defects=0` then `PREDICATE C2 pass` (`:336-337`) · `1` any `Vn DEFECT <note>`, including a check that raises — `error <Class>: …` is a defect, never a pass (`:328-335`); V4 and V7 both report the one string `receipt or entry absent` when *either* file is missing (`:178-184`), so a landed receipt with an unlanded entry reads as absent · `2` argparse usage only — the script has no setup exit (`:318-338`; measured `--bogus` → exit 2) | itself; freeze control `.ufo/waves/round-42/claims/control-c2-nothing.txt` (`checks=9 defects=6`: V2 V3 V4 V7 V8 V9; `PREDICATE C2 fail`, `exit=1`; its gate reads `P2 DEFECT receipt unreadable`, `P9 DEFECT untracked=31`, `P10 DEFECT receipt unreadable`) — at tip `fda71ae` on a clean clone the same shape measures `checks=9 defects=5` (V2 V3 V4 V7 V9) because the receipt has since landed: `P2 ok receipt_sha256=pinned`, `P9 ok untracked=0`, `P10 ok probe_rerun=byte-equal bytes=4212`, `V8 ok order_exit=0 result=PASS`; filler control `control-c2-filler.txt` → `V9 DEFECT`, the measured content → `V9 ok` | spec `plans/pkg-spec-r42.json` `e836c425…`, gate `plans/pkg_gate.py` `ea638822…`, probe `plans/fibsqrt_probe.py` `fc58bf3f…`, dry table `corpus/evidence/round42/fibsqrt-dry-cases-freeze.txt` `9ee60af6…`, nine captures under `corpus/evidence/round42/tb2-circuit-fibsqrt/` (`SHA256SUMS` `36b15d5b…`), receipt `corpus/evidence/round42/fibsqrt-probe.txt` `2a54ca8a…` (not digest-pinned: P10 re-runs the probe and byte-compares) | scratch under `--work` only — verified with the lane bound read-only (`defects=5`, `exit=1`, `--work` empty afterwards); reads lane bytes and git history, writes nothing in it; its gate leg re-runs the probe, so a full run costs ≈62 s (measured 61.65 s) | kengaku |
| `fibsqrt-probe` | probe | `python3 plans/fibsqrt_probe.py --lane .` (`--dry` prints the seven `TAG` lines and the 16 frozen `CASE` lines, no sandbox; `--stage-check` builds every case's end state and prints only stage exit codes, the grader module is never imported; `--dry` and `--stage-check` are mutually exclusive; `--work DIR` scratch parent, created if absent) | `0` every case yielded three test verdicts twice and both summary lines printed — **prediction mismatches are on the summary line, never in the exit code** (measured `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, exit 0; `:358-360`) · `1` `--stage-check` only: a case's setup or recipe stage exited non-zero (`stagecheck cases=16 failed=<k>`, `:328-329`) · `2` setup: duplicate or malformed case id, unknown tag, malformed prediction or `len(GRADED)!=28` (`:290-293`); a capture missing or off its pinned digest (`:305-308`); `/usr/bin/bwrap`, `/usr/bin/python3`, `/usr/bin/bash` or `/usr/bin/gcc` not executable (`:309-312`); `--work` cannot be created (`:313-318`); a case that does not yield three test verdicts twice (`SETUP case <cid> did not yield three test verdicts twice`, `:341-344`) — a recipe that exits non-zero is a probe error, never a verdict | itself; receipt `corpus/evidence/round42/fibsqrt-probe.txt` reproduced **byte-equal** by a fresh run on the clean clone (`sha256=2a54ca8a…`, `bytes=4212`, 61 s, `diff` empty, `regrade cases=16 differ=0`); `--stage-check` `stagecheck cases=16 failed=0`, exit 0; `--dry` byte-equal to the frozen dry table (`9ee60af6…`, `diff` empty) | five capture digests in `PINS` (`test_outputs.py` `6117b8ed…`, `sim.c` `700645ac…`, `gates.txt` `032786f9…`, `solve.sh` `a4ffab41…`, `instruction.md` `a7f50026…`); 16 cases, 7 tags; the 28-value `GRADED` table (1, 4, 8, 12, 41, 42, 107, 220, 209, 366 and `x²−1`, `x²`, `x²+1` for x in 12, 41, 42, 107, 220, 209; max 48401); three grader tests in file order | scratch under `--work`/`$TMPDIR`, removed on exit (`:362`); reads the lane's captures only — verified with the lane bound read-only (`stagecheck cases=16 failed=0`, exit 0) and `git status --porcelain` empty after a full run | kengaku |
```

## 2. Addendum paragraph (draft, round-42 registry addendum)

> Round-42 registry addendum: `round42-c1-mutants` is the round-41 counter's shape re-pointed at the two tools
> round 42 leaves unedited (`anchor_digest_check.py`, `order_check.py`) with 14 frozen round-40 near-variants and a
> new **attribution** leg: a direction hit counts only when a traced re-run on the killing fixture reproduces the
> result *and* executes a line of the replaced span, so `unattributed=14` is a failure mode the tool list can now
> reach (`control-c1-attribution.txt`). Its predicate binds the total (14) and both per-tool floors, so an empty
> mutant list fails. At wave-1 build it reads the do-nothing control (`fixtures=0`, `survived=14`,
> `anchor=0/9 order=0/5`); it turns green only with `plans/battery42/`, whose fixtures are built from nothing under
> the counter's sandbox contract — run it with `--lane` on a disposable clone and inside the host-guard bwrap
> envelope. `round42-c2` is the round-41 counter's V1–V8 re-pointed at the `circuit-fibsqrt` package plus **V9
> content** (the entry's `## Case table` equal to the receipt row by row, every row id outside its `source:` line,
> PROVINCE naming the task and the entry, README `## Frontier` naming the task); it needs the entry, the S125–S127
> `corpus/SOURCES.md` rows and the README/PROVINCE surfaces as well as the receipt, and its gate leg re-runs the
> probe, so a full run costs ≈62 s. `fibsqrt-probe` is a `probe` row of the round-41 `constraints-probe` shape:
> `mismatches=` is a data line and the exit code never carries prediction disagreement. The round-42 freeze control
> for `round42-c2` (`defects=6`, V8 among them) is a **freeze-time** number: at the tip the receipt is committed
> after the claims file and the tree is clean, so the same do-nothing shape measures `defects=5` with `V8 ok` —
> quote the control with its commit, not as a standing expectation.

## 3. Measured evidence

### 3.1 `round42-c1-mutants` — do-nothing control at tip

```
$ bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
    --proc /proc --unshare-pid --die-with-parent python3 plans/round42_c1_verify.py --lane . --work "$S/w"
17:23:04 … 17:23:04
PINS total=2 mismatched=0
MUTANT X1 anchor rc-mirror SURVIVED exhibits=none -- plans/anchor_digest_check.py:50-52 …
… (14 SURVIVED lines, identical to claims/control-c1-nothing.txt) …
BATTERY fixtures=0 wrong=0 tampered=0 sidechannel=0
MUTANTS total=14 killed=0 survived=14 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/9 order=0/5
ADVERTISED direct=13 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
exit=1
```
Receipt: `.ufo/waves/round-42/build/R42RegistryRows/c1-run.txt` (`sha256 6b3e1e48…`, 2297 bytes), stamps
`17:27:43 / exit=1 / 17:27:44`. `plans/battery42/` does not exist at the tip (`ls plans/battery42` → no such
directory), so the row's controls are exactly the freeze's.

Refusal and selector behaviour (measured):
```
$ … round42_c1_verify.py --lane . --work .        → SETUP --work must not lie inside the lane … / exit=2
$ … --battery-dir <empty dir> --only X1 --work …   → MUTANTS total=1 killed=0 survived=1 … PREDICATE C1 n/a / exit=1
```
The read-only-lane run (`--ro-bind "$S/lane" "$S/lane"`, `--lane "$S/lane"`) printed the same predicate and
`exit=1`: the counter writes only its `--work` scratch.

### 3.2 `round42-c2` — do-nothing control at tip (clean clone)

```
$ … round42_c2_verify.py --lane . --work "$S/w2"          (17:23:04 → 17:24:05, 61.65 s)
V1 ok listed=9 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 DEFECT no '## Located quotes' section
    gate: P4 DEFECT no parsed quote
    gate: P5 ok manifest_entries=9 bad=0 first=0
    gate: P6 DEFECT rows=3 bad=3 first=S125: rows=0
    gate: P7 DEFECT entry unreadable
    gate: P8 DEFECT index_rows=48 knowledge_files=48 bad=2 first=index rows for knowledge/tb2-circuit-fibsqrt-grader.md=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=4212
    gate: defects=5
V2 DEFECT spec=frozen gate=frozen gate_exit=1
V3 DEFECT rows=3 bad=['S125:row', 'S126:row', 'S127:row']
V4 DEFECT receipt or entry absent
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 DEFECT receipt or entry absent
V8 ok order_exit=0 result=PASS
V9 DEFECT receipt, entry, PROVINCE.md or README absent
checks=9 defects=5
PREDICATE C2 fail
exit=1
```
V4/V7 read as "absent" only because `corpus/knowledge/tb2-circuit-fibsqrt-grader.md` has not landed yet
(`ls corpus/knowledge | grep fibsqrt` → empty); the receipt `corpus/evidence/round42/fibsqrt-probe.txt` **is**
committed (`523b278`). The same output shape reproduced under the read-only lane binding at 17:27:08
(`checks=9 defects=5`, `exit=1`, `--work` empty), and the receipt run saved to disk (17:27:43 → 17:28:49, 66.7 s,
`exit=1`) printed the same 21 lines byte-for-byte. Full log:
`.ufo/waves/round-42/build/R42RegistryRows/c2-run.txt` (`sha256 c92462a6…`, 913 bytes) with `.stamps`
(`17:27:43 / exit=1 / 17:28:49`).

Freeze control, verbatim from `.ufo/waves/round-42/claims/control-c2-nothing.txt`, for the delta:
`gate: P2 DEFECT receipt unreadable`, `gate: P9 DEFECT untracked=31 first=.ufo/waves/round-42/claims/c2_filler_control.py`,
`gate: defects=8`, `V8 DEFECT order_exit=2 result=not-PASS`, `checks=9 defects=6`, `exit=1`.

### 3.3 `fibsqrt-probe` — receipt reproduced, dry table byte-equal, stage-check green

```
$ … fibsqrt_probe.py --lane . --work "$S/wp"             (17:24:18 → 17:25:19, exit=0)
… 16 CASE lines, every one match=yes regrade=same …
regrade cases=16 differ=0
cases=16 observed_pass=7 observed_fail=9 mismatches=0
$ diff -u corpus/evidence/round42/fibsqrt-probe.txt "$S/probe-run.txt" → (empty)
   2a54ca8a76619a173280727938441fcf129ddcd482cc0a4d55f65b38d41ad92a  probe-run.txt   (4212 bytes)
   2a54ca8a76619a173280727938441fcf129ddcd482cc0a4d55f65b38d41ad92a  corpus/evidence/round42/fibsqrt-probe.txt
$ … fibsqrt_probe.py --lane . --dry > probe-dry.txt ; diff -q …fibsqrt-dry-cases-freeze.txt → identical
   9ee60af69ba3dc9fb1585dbaeb33faef2e96c92977d555837565ce416f6898b5  (both)
$ … fibsqrt_probe.py --lane . --stage-check --work "$S/wps"  (17:25:36 → 17:25:37, exit=0)
stagecheck cases=16 failed=0
$ … fibsqrt_probe.py --bogus → fibsqrt_probe.py: error: unrecognized arguments: --bogus   exit=2
```
Case verdicts (verbatim, from `probe-run.txt`): `nop` `PPF`, `oracle-solve-sh` `PPP`, `no-gates-file` `FFF`,
`empty-gates-file` `PPF`, `lookup-28` `PPP`, `lookup-27-drop-48401` `PPF`, `lookup-28-plus-examples` `PPP`,
`lookup-28-bitflip-41` `PPF`, `lookup-28-padded-31999` `PPP`, `lookup-28-padded-32000` `PFP`,
`lookup-28-comment-lines` `PPP`, `lookup-28-reversed-lines` `PPP`, `lookup-28-crlf` `PPP`,
`lookup-28-trailing-space` `PPF`, `fake-sim-script` `PPF`, `gates-is-directory` `PFF`
(`test_gates_file_size:error=IsADirectoryError`). Read-only-lane `--stage-check` also printed
`stagecheck cases=16 failed=0`, exit 0.

### 3.4 Digests I computed in the clone (pinned values cross-checked)

```
11bb2cad…  plans/anchor_digest_check.py            948d5e1d…  plans/order_check.py
559fca0c…  plans/round42_c1_verify.py              270097fd…  plans/round42_c2_verify.py
fc58bf3f…  plans/fibsqrt_probe.py                  e836c425…  plans/pkg-spec-r42.json
ea638822…  plans/pkg_gate.py                       36b15d5b…  corpus/evidence/round42/tb2-circuit-fibsqrt/SHA256SUMS
2a54ca8a…  corpus/evidence/round42/fibsqrt-probe.txt
```
Every value equals its entry in `.ufo/waves/round-42/claims/frozen-digests.txt` or the counter's own `PINS`
(`round42_c1_verify.py:97-100`, `round42_c2_verify.py:59-71`, `fibsqrt_probe.py:62-68`). Constants read by `ast`
from the clone: probe `PINS=5`, `TAGS=7`, `GRADED` literal 10 (+18 appended, run asserted 28); C2 `CAPTURES=9`;
C1 `PINS=2`, `TOTAL=14`, `FLOORS` 2 entries.

## 4. Findings for the L1

1. **C2's freeze control is stale by one check.** `control-c2-nothing.txt` prints `defects=6` with `V8 DEFECT
   order_exit=2`; at tip the same do-nothing shape prints `defects=5`, `V8 ok order_exit=0 result=PASS`
   (`P2`, `P9`, `P10` also flipped to ok). Cause: the control was taken before `523b278` committed the receipt
   and inside the L1 working tree (`P9 untracked=31`). Quote it as a freeze-time number.
2. **`V4`/`V7` conflate a missing receipt with a missing entry** (`plans/round42_c2_verify.py:178-184` returns
   `"receipt or entry absent"` for either). An operator reading `defects=5` cannot tell which file is missing
   from the note; the row says so, and `corpus/knowledge/tb2-circuit-fibsqrt-grader.md` is the missing one today.
3. **`round42-c2` needs a clean tree for `P9`** (gate `P9 untracked=0`); run it on a clone, not in the lane
   working tree, or the gate reports every wave-1 draft as untracked.
4. **`round42-c1-mutants`'s development selectors still exit 1 on a survivor** even though the predicate is `n/a`
   (measured `--only X1` → exit 1). Round 41's row only promised `PREDICATE C1 n/a`; the row above states both.
5. **The probe's receipt is deterministic and reproduces byte-for-byte in 61 s**, including `regrade=same` on
   all 16 cases; `--dry` is byte-equal to the frozen table. This is the only one of the three rows that is green
   at wave-1 build.

## 5. Scope

Drafted and verified: three registry rows (§1) and one addendum paragraph (§2). Not done, by instruction: no
edit to `SKILL.md` or any other lane file (L1 integrates), no counter/probe/battery/spec change, no commit, no
C1 battery work (wave-1 executors own `plans/battery42/`), no C2 entry/SOURCES/README/PROVINCE drafting (the
package seat owns it). Not claimed: that `round42-c1-mutants` can pass — at this tip it cannot, by construction
(no `plans/battery42/`); that `round42-c2` can pass — the entry, the three `SOURCES.md` rows and the README/
PROVINCE surfaces are absent, so `V2 V3 V4 V7 V9` are red (measured). No tool was installed.

Receipts under `.ufo/waves/round-42/build/R42RegistryRows/`: `c1-run.txt` + `c1-run.stamps`,
`c2-run.txt` + `c2-run.stamps`, `probe-run.txt`, `probe-dry.txt`.

VERDICT: registry-rows-drafted-3-verified-3
