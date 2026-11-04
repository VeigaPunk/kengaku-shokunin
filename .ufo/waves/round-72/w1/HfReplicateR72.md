# HfReplicateR72 — independent replication of the R72-C1 nine-case battery

Seat: `HfReplicateR72` (leaf executor). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`,
branch `master`, tip at both runs `b6336136e0e891522b113a94d8e0bd65e0eae8de`. Scratch:
`/fast/scratch/hyaku/kengaku-r72/HfReplicateR72` (deleted at end; see §Scratch).

Item: replicate the R72-C1 battery in a **separate work tree**, `diff` against the receipt of record,
and re-derive all nine `case_sha256` values with the probe's own `stage_case`/`tree_digest`.

## Verdict

1. The replicate battery passes on its own: nine `VECTOR` lines `agree=True`, `LEG-COVERAGE
   legs=4 seen_p=4 seen_f=4`, `SUMMARY cases=9 legs=36 mismatches=0 setup=0 exc=2`,
   `PREDICATE R72-C1 pass`, rc 0.
2. `diff receipt.txt receipt-replicate.txt` is **empty**, `DIFF_RC=0`. Both files are 40 lines /
   3494 bytes, sha256 `fa060b7fa2e4adbf8f0d4de180bea2d66bc7598ed5f13dbcfcf6093b7c224087`
   (distinct inodes: 251692339 vs 251692421; `cmp` rc 0).
3. All nine `case_sha256` values re-derive from the committed model fixture and byte-pinned grader
   with the probe's `stage_case`/`tree_digest`, and equal the receipt's values. An **independent**
   tree-hash implementation (not the probe's function) reproduces all nine as well.
4. Non-determinism observed in the run: **only** the tqdm throughput digits in
   `sandbox-stderr.txt` for the seven captures that load a model (K1–K6, K9). Nothing that feeds
   the receipt varies: 29 of 36 capture files are byte-identical, including all nine
   `manifest.json`, all `sandbox-stdout.txt` and all `app-tree.txt`.

No predicate, case table, vector, digest, kill rule or target was edited. No git mutation, no
commit; this seat wrote only its assigned evidence paths, its scratch and this report.

## Commands actually run (exit codes verbatim)

1. `mkdir -p /fast/scratch/hyaku/kengaku-r72/HfReplicateR72` → ok.

2. Battery (cwd = lane):

   ```
   python3 plans/round72_c1_hf_probe.py --lane . \
     --work /fast/scratch/hyaku/kengaku-r72/HfReplicateR72/battery \
     --receipt corpus/evidence/round72/hf/receipt-replicate.txt \
     --evidence-dir corpus/evidence/round72/hf/sandbox-replicate \
     --port-lock /fast/scratch/hyaku/kengaku-r72/port5000.lock
   BATTERY_RC=0        (wall 87.09 s)
   ```

   stdout (verbatim):

   ```
   CASE K1 derived=PPPP rc=0 exc=[]
   CASE K2 derived=PPFP rc=0 exc=[]
   CASE K3 derived=PPFP rc=0 exc=[]
   CASE K4 derived=PPPF rc=0 exc=[]
   CASE K5 derived=PFPP rc=0 exc=[]
   CASE K6 derived=PFFF rc=0 exc=['test_api_error_handling', 'test_sentiment_endpoint']
   CASE K7 derived=FPPP rc=0 exc=[]
   CASE K8 derived=FPPP rc=0 exc=[]
   CASE K9 derived=PPPF rc=0 exc=[]
   LEG-COVERAGE legs=4 seen_p=4 seen_f=4
   SUMMARY cases=9 legs=36 mismatches=0 setup=0 exc=2
   PREDICATE R72-C1 pass
   ```

3. `diff corpus/evidence/round72/hf/receipt.txt corpus/evidence/round72/hf/receipt-replicate.txt;
   echo DIFF_RC=$?` → no output, `DIFF_RC=0`.

4. Digest re-derivation, scratch driver importing the probe module (rc 0) plus a second,
   independent code path through the probe's own CLI
   (`--render-table --stage-sha --work <scratch>/render-work`, rc 0). Both produced the same nine
   values; a second staging of every case into a different parent directory (`<work>/cases` vs
   `<work>/cases-b`) returned the identical digest per case — path independence re-confirmed, not
   taken from the probe's selftest line.

5. Extra, read-only checks (not required by the item, run because they are cheap and falsifiable):

   - `--check-receipt receipt-replicate.txt --work <scratch>/check-work` → `DEFECTS n=0`,
     `PREDICATE R72-C1 pass`, rc 0.
   - `--check-receipt receipt.txt --work <scratch>/check-record` → `DEFECTS n=0`,
     `PREDICATE R72-C1 pass`, rc 0 (independent re-run of the record's own check at this tip).
   - Independent tree-hash implementation over the staged `app/` trees → all nine match
     (see §Nine digest comparisons).
   - Sandbox provenance driver: the probe's `bwrap_argv` with its harness replaced by
     `python3 -c` (same binds, same nine `--setenv`) → rc 0,
     `{"tf_version":"5.21.0","tf_file":"/venv/lib/python3.13/site-packages/transformers/__init__.py",
     "executable":"/venv/bin/python3","cwd":"/app","canary":"ABSENT",
     "env_keys":"HF_HUB_OFFLINE,HOME,LANG,PATH,PWD,PYTHONNOUSERSITE,PYTHONPATH,PYTHONWARNINGS,TMPDIR,TRANSFORMERS_OFFLINE"}`.

## Step 3 — the receipt diff, line by line

The `diff` is empty, so there are **no differing lines to name**. The classes that *could* differ,
and why they did not:

| line class | expected source of variance | observed |
|---|---|---|
| `REV b6336136…` | lane tip at run time | identical: both batteries ran at tip `b6336136`, no commit landed between them (record 23:10, replicate 23:11 local) |
| `PROBE_BLOB … rev=b6336136…` | committed blob read at tip | identical for the same reason; `PROBE sha256` = `PROBE_BLOB sha256` = `99867c7f…` re-derived from the working tree and from `git show HEAD:plans/round72_c1_hf_probe.py` |
| `CASE K… server_pid=…` | OS process id | identical **because the pid is namespace-local**: `bwrap --unshare-all` unshares PID, so a served case always prints `3` and K6 prints `-`. Verified by two extra rounds of K6 and K9, each `pid` `null` / `3` |
| `LIBRARIES python=… torch=… transformers=… requests=…` | host venv versions | identical: same read-only `/fast/ComfyUI/.venv` on the same host |
| `CASE K… case_sha256=…` | staging path | identical by construction; independently re-derived (§Nine) |
| `PROVENANCE …` | inherited env, library file | identical: `env_cleared=True allowlist_seen=9/9 distinct=1 canary_seen=0`, file under `/venv/` |
| `LEGS` / `EXC` / `VECTOR` / `LEG-COVERAGE` / `SUMMARY` | grader outcomes | identical, including the deterministic `EXC K6` pair |

So the only classes that can legitimately move between two runs at one tip are `REV` (if a commit
landed) and `server_pid`; neither moved. Honest caveat: because staged-input digests are
path-independent **by design**, byte identity across two sequential runs at one tip is
corroboration of determinism, not fresh information about the staging function — the independent
value of this seat is item 4 (an independently implemented digest check), the separate work tree
and the extra reruns.

## Step 4 — nine digest comparisons

`case_sha256` = `tree_digest(app/)` after `stage_case`. Columns: receipt value (record and
replicate are byte-identical); re-derived by importing the probe (`stage_case` + `tree_digest`);
re-derived again into a different parent directory (path independence); independent implementation
(walk → `sha256(file)` → `"<hash>  <relpath>"`, sort by relpath, sha256 of the joined text) over the
replicate's staged trees.

| case | `case_sha256` (all sources equal) | probe re-derive | restage | independent impl |
|---|---|---|---|---|
| K1 | `4512bfa2140124948903dc7b0f80941656f2b8bf18da8a6ef60d442f89e533f1` | ✓ | ✓ | ✓ |
| K2 | `e0c2dc8e799f31a6e8a41413801c53930b10f6249041d368ce7a2f5105d2c3c8` | ✓ | ✓ | ✓ |
| K3 | `36ce18bf679d0c12d5214386dad24178c545125be9f3575450a6f49c2c75acac` | ✓ | ✓ | ✓ |
| K4 | `eaff30ccaff69ff34e3e8c4ec0bdfb20984c83f5ed8245bbf0ff99ae24d61cbe` | ✓ | ✓ | ✓ |
| K5 | `d0e8574ca9dafacf7c2e51b6434aa3585b53b03237048057d14a2871d901572a` | ✓ | ✓ | ✓ |
| K6 | `6317bec0d99e7c94bc0fd169655e32ee5c43900af5c8d3c6b4e2ebd132eaf7bd` | ✓ | ✓ | ✓ |
| K7 | `494f5d59138b69abdd11a2ea72d6b6f2aaf35d721a7b16e20f66f618c3ecbc1a` | ✓ | ✓ | ✓ |
| K8 | `b229944fa7b9665ccb02854edce0127a7ee1b36deb8b5dc280eecd163add329a` | ✓ | ✓ | ✓ |
| K9 | `3ecda97029e6108b91b8eae3cd31fa07fbed05c7f87c4daa5e7484e0850bf33f` | ✓ | ✓ | ✓ |

Nine distinct digests (`case-digest-unique` clause holds). Shape checks: the staged model in K1 is
byte-identical to the committed fixture on all five files; K8's staged model differs from the
fixture in exactly one file (`config.json` = `{"model_type": "bert", `, truncated invalid JSON) and
the other four files are byte-identical; the remaining difference between case digests is
`server.py`, whose bytes are generated from the mode. This is consistent with the nine distinct
values and with the vectors.

## Non-determinism observed

- **Receipt entry: none.** Two independent executions (record and replicate) produced byte-identical
  receipts; two extra K6 and two extra K9 reruns reproduced `case_sha256`, `derived`, `legs`,
  `exc`, `sandbox_rc` and the provenance fields exactly.
- **Evidence captures: stderr only.** `diff -rq sandbox sandbox-replicate` reports 7 of 36 files
  differing — `K1,K2,K3,K4,K5,K6,K9/sandbox-stderr.txt`, each on a single line
  `Loading weights: 100%|…| 25/25 [00:00<00:00, <throughput> it/s]`. K7/K8 stderr are empty
  (model absent / corrupt, nothing to load). Throughput is wall-clock noise; it does not enter the
  receipt, which is derived from `LEGS-JSON`, not from stderr.
- **K6 exception shape is deterministic**: `EXC K6 test_api_error_handling=E
  test_sentiment_endpoint=E` (ConnectionError scored `F`, pytest-equivalent), reproduced in both
  rounds of the extra rerun; `exc=2` in the `SUMMARY` is not flaky.

## Kill-rule accounting (frozen clauses, replicate run)

| clause | observed | verdict |
|---|---|---|
| any case `agree=False` | 0/9 | clear |
| one `setup` failure / `SETUP` / `ERROR` case | `setup=0`, no `SETUP`/`ERROR` line | clear |
| `PROVENANCE` absent or duplicated | exactly one line | clear |
| `distinct != 1` / file outside `/venv/` | `distinct=1`, `/venv/lib/python3.13/site-packages/transformers/__init__.py` | clear |
| `canary_seen > 0` | `0` | clear |
| `allowlist_seen != 9/9` | `9/9` | clear |
| stub control exposes the stub | not run by this seat (other seat's item); lane now carries `stub-control.txt` with `exposed=False` (see F5) | not evidenced here |

No retry was taken; no case was reselected after data.

## Findings (report-only; nothing edited)

**F1 — byte identity is corroboration, not independent variation.** The replicate ran in its own
work tree, its own processes and at a different wall time, but with the same committed instrument
and the same host libraries, and the probe's staging is path-independent by design. The genuinely
independent checks here are the second digest implementation (all nine matched) and the extra
reruns. A future replicate harness could perturb something the predicate is blind to (e.g., a
different `--work` filesystem, an injected parent env var other than `PYTHONPATH`) to widen the
test.

**F2 — the observed sandbox key set is 11 in model-loading cases, and `allowlist_seen` is a
superset check.** Measured with an independent driver: `bwrap --clearenv` + nine `--setenv` yields
exactly the nine allowlist keys plus `PWD`; importing `torch`/`transformers` adds nothing; but
`AutoModelForSequenceClassification.from_pretrained` **inside the sandbox** adds
`TORCHINDUCTOR_CACHE_DIR=/tmp/torchinductor_vgpnk`. The value names the host account (read from the
read-only `/etc` bind) and points at the sandbox tmpfs; it is created after the environment was
cleared, so it is not inherited. The receipt's clause is `allowlist_seen=9/9` (⊇), so this does not
break it, but the receipt does not witness an exact-set environment, and it records key *names*
only, not values. Corroborates `HfBatteryR72` F1 with the measured value and an independent
reproduction.

**F3 — `SUMMARY` carries `exc=2`, which the frozen claim sentence does not quote.** The claim text
quotes `SUMMARY cases=9 legs=36 mismatches=0 setup=0`; the line is that prefix plus ` exc=2`. The
frozen checker recomputes the `exc` term from the `EXC` line, so both readings pass. Documentation
precision, not an instrument defect.

**F4 — receipt `REV`/`PROBE_BLOB rev` bind the run tip `b6336136`, not the freeze base `c6322972`.**
Consistent with the predicate's "at the round tip" and with the checker's ancestry clause
(`receipt-rev` passed on both receipts); noted so the receipt is not read as a base-tip binding.

**F5 — the R72-C1 predicate's stub-control clause was absent at this seat's first check and is now
present from another seat.** `corpus/evidence/round72/hf/stub-control.txt` did not exist when I
looked during my battery window (it appeared with mtime 23:14, after that check); it is
`StubBeforeAfterR72`'s item and was not run here. The lane now carries it: 9 `VECTOR` lines, last
line `STUB-CONTROL exposed=False vectors_unchanged=True
stub_path=/fast/scratch/hyaku/kengaku-r72/StubBeforeAfterR72/sc/stub`. Noted so the receipt is not
attributed to this seat; I did not rerun or audit it.

**F6 — shared-port timing.** My battery took 87.09 s versus the record's 49.27 s; the `flock` is
taken **per case** with a 20 s `wait_port_free` cap, so a foreign listener that holds 5000 longer
than 20 s turns a case into `SETUP`. No `SETUP` occurred in either run, but the margin is one case
long, not one battery long.

## Write scope / scratch / tooling

- Lane footprint of this seat: `corpus/evidence/round72/hf/receipt-replicate.txt` and
  `corpus/evidence/round72/hf/sandbox-replicate/K1..K9/{manifest.json,sandbox-stdout.txt,
  sandbox-stderr.txt,app-tree.txt}` (36 files, 136 KB) — both assigned by the item — plus this
  report. No tracked file was modified; no `.ufo/state/`, `.scratch/`, `corpus/` outside the
  assigned paths, and no sibling lane was written.
- Scratch `/fast/scratch/hyaku/kengaku-r72/HfReplicateR72` (2.2 MB: battery work tree,
  `check-work`, `check-record`, `digest-work`, `render-work`, `rerun-work`, `envprobe`, drivers)
  deleted after the receipts, captures and values above were written into the lane; absence
  verified afterwards by `ls`. Nothing left in `/tmp` (`find /tmp -maxdepth 1 -user vgpnk
  -newermt '-40 minutes'` empty). The shared `port5000.lock` was not mine to remove and was left.
- No git command that mutates was run (`git rev-parse`, `git show`, `git log`, `git ls-tree`,
  `git status` only).
- No tool install or upgrade was needed or performed (bwrap 0.13.1, python 3.13.16, torch 2.14.1,
  transformers 5.21.0 as bound into the sandbox).
