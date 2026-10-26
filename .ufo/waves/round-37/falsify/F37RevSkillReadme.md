# F37RevSkillReadme — round-37 wave 2 (falsify), 2026-10-26

Seat: reviewer of the round-37 additions to `SKILL.md` (registry rows) and `corpus/README.md`
(index row, coverage bullet, evidence listing, knowledge==index).
Lane tip under review: `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5` (branch master contains it; `refs/heads/master` = `dc90676b`, one commit ahead).
Method: clean clone `git clone -q --no-local <lane> $S/fx/lane && git checkout -q 357dece…`
(`rev-parse --show-toplevel` = `$S/fx/lane` verified); every registry command run once on that
clone, cwd = clone root, `TMPDIR=$S` (scratch `/fast/scratch/hyaku/kengaku-r37/F37RevSkillReadme`,
removed at the end). Receipts: `.ufo/waves/round-37/falsify/F37RevSkillReadme/`.

## Registry rows — commands exist and run as written

All five round-37 rows' entry scripts exist in the tip tree and ran as written:

| row | command (as written) | exit | key output |
|---|---|---|---|
| `git-webserver-probe` | `python3 plans/git_webserver_probe.py --lane .` | 0 (53 s) | `cases=22 observed_pass=9 observed_fail=13 mismatches=0` |
| `round37-c1-mutants` | `python3 plans/round37_c1_verify.py --lane .` | 0 (82 s) | `BATTERY fixtures=64 wrong=0 renamed_disagree=0` · `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0` · `PREDICATE C1 pass` |
| `round37-c2` | `python3 plans/round37_c2_verify.py --lane .` | 0 (53 s) | `checks=7 defects=0` · `PREDICATE C2 pass` (gate P1–P10 all ok, `P10 ok probe_rerun=byte-equal bytes=8443`) |
| `anchor-digest-check` | `python3 plans/anchor_digest_check.py --lane .` | 0 | `rows=107 tokens=15 defects=0` |
| `ledger-tip` | `python3 plans/ledger_tip.py --source <clone> --work <scratch>` | **1** | `rows=9 closed=9 observed_pass=7 mismatches=2` — see D1 |

Full stdout of each run: receipts `git-webserver-probe-run.txt`, `round37-c1-mutants-run.txt`,
`round37-c2-run.txt`, `anchor-digest-check-run.txt`, `ledger-tip-tip-357dece-fail.txt`.

## Findings

### D1 (HIGH) — `ledger-tip` row: the declared green state is unreachable as documented on a clean clone of the tip; the landing's 9/0 receipt is not reproducible by its own committed script

Row text (SKILL.md:581): `0` = "every closed ledger row's check passes at the tip"; addendum
(SKILL.md:610): "every closed routed-defect row's check re-runs on a clean clone of the tip."

Measured on the tip clone (receipt `ledger-tip-tip-357dece-fail.txt`):

```
$ python3 plans/ledger_tip.py --source $D/lane --work $S/lt-work   # exit=1
R34-D2 status=closed observed=fail agree=NO error CalledProcessError: Command '['git', '-C',
  .../lt-work/lane', 'ls-tree', '-r', '--name-only', 'refs/heads/master', '--',
  '.ufo/waves/round-34/mut-entries-scratch', ...]' returned non-zero exit status 128.
R35-D3 status=closed observed=fail agree=NO error ... ls-tree -r --name-only refs/heads/master ... exit status 128.
rows=9 closed=9 observed_pass=7 mismatches=2
```

Exit 1 maps per the verdict map (`1` = a mismatch), so the mapping itself is true — but both
mismatches are artifacts, not ledger disagreement:

1. Both pin checks hardcode the ref: `BRANCH = "refs/heads/master"`
   (`plans/defect_ledger.py:29`, `plans/round36_c1_verify.py:38`); `ledger_tip.py` builds its
   inner clone with `git clone -q --shared` (`plans/ledger_tip.py:69`).
2. The lane's git HEAD is detached (`git symbolic-ref HEAD` → fatal) and `refs/heads/master`
   = `dc90676b` ≠ tip `357dece`; `dc90676b` ("round-37: close lesson … falsify ready marker")
   contains the tip (`git merge-base --is-ancestor 357dece dc90676b` → yes). So every clean
   clone of the tip made by the round's own fixture rule (`clone` + `checkout -q <tip sha>`,
   which detaches) has HEAD ≠ master.
3. Empirically (git 2.56.0, same host): `git clone --shared` from a source whose HEAD is
   detached at X creates a local `refs/heads/master` **iff the source's master tip == X**:
   - source detached at 357dece, master=dc90676b → inner clone has no `refs/heads/master`
     (`git show-ref` lists only `refs/remotes/origin/master`) → the two checks exit 128 →
     `mismatches=2`, exit 1;
   - source with HEAD symbolic→master at 357dece (`checkout -q -B master 357dece`) → inner
     clone gets `refs/heads/master=357dece` → `rows=9 closed=9 observed_pass=9 mismatches=0`,
     exit 0, TIP=357dece;
   - source detached at 357dece with master=357dece → inner clone gets master → 9/0, exit 0.
   So the row's green state silently requires `refs/heads/master == HEAD` in the `--source`
   tree — a precondition the row never states.
4. The landing receipt (`.ufo/waves/round-37/integrate/measure-final.txt`) shows 9/0 at
   `TIP commit=5c7d5d75…`. Its committed generator `measure.sh` derives
   `TIP=$(git -C "$L" rev-parse refs/heads/master)` and then does `git checkout -q "$TIP"`
   (which detaches — verified: `checkout -q <sha>` detaches even when the sha equals the
   current branch tip). Reproducing that exact sequence at the receipt's own TIP today
   (receipt `ledger-tip-repro-5c7d5d7-detached-source.txt`): `mismatches=2`, exit 1.
   The 9/0 was therefore measured while `refs/heads/master` still pointed at the measured
   commit (master has since moved ahead to `dc90676b`); it is not reproducible today by the
   committed script. [INFERENCE for the historical shape: reconstructed from the three
   controlled runs above; the landing's scratch clones were already removed.]
5. Same mechanism makes the committed `measure.sh` a moving target: re-run today it would
   measure `dc90676b`, not the landing tip `357dece`.

Net: the row records a pass its documented invocation can no longer produce, and even in a
passing configuration the pin rows verify `refs/heads/master`, not "the tip" — the row's
`0` wording ("passes at the tip") is only true when master == HEAD.

### Verified-accurate (no defect)

- **`git-webserver-probe` exit semantics**: flip experiment — `Case("no-server", …, "fail"→"pass")`
  in my clone, rerun: `cases=22 observed_pass=9 observed_fail=13 mismatches=1`, **exit 0**
  (receipt `git-webserver-probe-flip-prediction.txt`); probe restored to freeze digest
  `63cb75cf` after. Matches the row's "mismatches are on the summary line, never in the exit
  code" and README's "exit 0 means only that every case produced one verdict
  (`plans/git_webserver_probe.py:303-304`)" — line 303 prints the summary, line 304 `return 0`. ✓
- **`git-webserver-probe` line cites**: bwrap `--unshare-net --unshare-pid --unshare-ipc` at
  `:204` ✓; `/tests` ro-bind at `:209-213` ✓; `HOME=/work/home` at `:235` ✓. `/usr/bin/bwrap`
  executable ✓. Runtime ~53 s vs row's "~58 s, measured" — same order, not a defect.
- **`round37-c1-mutants` control pin**: `.ufo/waves/round-37/claims/control-c1-nothing.txt`
  ends `MUTANTS total=55 killed=5 survived=50 invalid=0 null_detected=0` / `PREDICATE C1 fail`
  — matches the row's "killed=5 survived=50". ✓
- **`round37-c2` control pin**: `control-c2-nothing.txt` = `V2 DEFECT gate_exit=1`,
  `V3 DEFECT rows=3 bad=['S111:row','S112:row','S113:row']`, `V4 DEFECT receipt or entry
  absent`, `V7 DEFECT receipt or entry absent`, `checks=7 defects=4`, exit 1 — matches the row
  verbatim. ✓
- **`anchor-digest-check` pins**: green on the tip (`rows=107 tokens=15 defects=0`, exit 0)
  after the S110 erratum + `anchor-captures/` landed; captures `sha256sum -c SHA256SUMS` →
  5/5 OK; wave-1 receipt `.ufo/waves/round-37/build/R37AnchorSweep/lane-run.txt` ends
  `rows=103 tokens=11 defects=5` with exactly S070/S072/S073/S074 `digest-unknown` + S110
  `digest-short` — matches the row's red-state description (the row says "its draft", and the
  draft is committed in that build dir, so the number traces). ✓
- **Pinned digests in the rows** (sha256sum on the tip clone, first 8 hex shown):
  test_outputs.py `526aee3d…`, verify.sh `1dc44c92…`, instruction.md `62151b73…`, probe
  `63cb75cf…`, receipt `83550712…`, dry table `0095e591…`, `pkg-spec-r37.json` `4c61d103…`,
  `pkg_gate.py` `ea638822…`, counter `dbc9f719…`, `pkg-spec-r35.json` `e085b435…`, capture
  `SHA256SUMS` `e70bb662…` — all match the rows' pins. ✓
- **corpus/README.md index row / coverage bullet** (line 261): names
  `knowledge/tb2-git-webserver-grader.md` (exists), S111/S112/S113 (all present in
  `corpus/SOURCES.md:126-128`; S114 at :129 for prior-art), probe + receipt paths (exist).
  Content claims verified against the captures: one pytest function asserting
  `"TEST PASSED" in result.stdout` (`test_outputs.py:13`); helper's clone/commit/push spawned
  at `verify.sh:21/34/38` with no status read; content check `[ "$CONTENT" = "hello world" ]`
  after `CONTENT=$(cat test_output.html)` (wget branch `:74-80`, curl branch `:55-63`). ✓
- **README evidence listing**: all six capture files + `SHA256SUMS` (`sha256sum -c` clean);
  receipt summary line at `git-webserver-probe.txt:49` exactly `cases=22 observed_pass=9
  observed_fail=13 mismatches=0`; `git-webserver-dry-cases-freeze.txt` present and `--dry`
  byte-equal (via my C2 run's `V5 ok probe=frozen dry_byte_equal=True`); `prior-art/` (body +
  meta + `SHA256SUMS`); `anchor-captures/` (4 pinned files + `PROVENANCE.md` + `SHA256SUMS`,
  clean); `../plans/battery37/` (9 modules, the single-defect battery). ✓
- **knowledge files == index rows**: independent count `index_rows=44 knowledge_files=44`
  (`grep -cE '^\| `knowledge/[^`]+` \|' corpus/README.md` vs `ls corpus/knowledge/*.md | wc -l`),
  and my C2 run's gate `P8 ok index_rows=44 knowledge_files=44 bad=0`. ✓

## Verification gaps

- Probe exit `2` (setup-refusal) and exit `1` (`--smoke` sandbox failure) paths not exercised.
- `ledger-tip` control mode (`--lane <clone>`) and its seven `control-ctl*.txt` receipts not
  re-run; the wave-1 receipts' source-clone shapes are inferred (D1 item 4), not observed.
- `round37-c1-mutants --battery r36` development selector not run (row marks it `PREDICATE C1 n/a`).
- The flipped-prediction run used my clone's edited probe; the freeze-digest probe itself was
  restored and re-verified by digest (`63cb75cf`).

VERDICT: skill-readme-1-defects
