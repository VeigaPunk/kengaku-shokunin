# ReviewC1 — R98-C1 correctness review (regex-chess replay, round 98)

Reviewer: ReviewC1 (leaf). Scope: `plans/round98_regexchess_probe.py`, `plans/round98_c1_replay.py`,
`plans/round98-cases.json`, committed receipt `corpus/evidence/round98/regexchess-probe.txt`,
captured grader `corpus/evidence/round98/tb2-regex-chess/test_outputs.py` + `test.sh`, all read at
T `8e37fc65d5649bb37166fdd6b1657445a8cb55b9` from a fresh `git clone --shared` detached at T.
Frozen predicates taken from `plans/round-98-claims.md` (frozen-instruments table). No production
edits; no frozen instrument touched.

**Verdict: R98-C1 correct as frozen. No DEFECT found. Predicate independently reproduced at T.**
One INFO nit and three observations, none actionable in round.

## Independent exercise (freshness)

- Clone at T verified (`git rev-parse HEAD` = T); lane tip read-only. All 10 files of the
  `frozen-instruments` + `candidate-bytes` tables in `plans/round-98-claims.md` hash byte-identical
  at T (verified by `sha256sum` in the clone): 10/10 match.
- Commit chain BASE `49a1c4f1` → P0 `5584a6f7` → P1 `350d0e59` → febd88b9 (operator) → P2 `c71f04e6`
  → F `e1a3afd9` → T `8e37fc65`; F verified ancestor of T.
- Grader venv staged fresh: python 3.13.16, chess 1.11.2, pytest 8.4.1 (exact `test.sh` uvx pins).
- My own counter run from the clone root, `--rev T`, work/venv outside the lane
  (receipt `w1/ReviewC1/replay-c1-run1.txt`, 842.9 s):
  `LEGS L1=pass … L10=pass`, `TARGET executed_rows=42 member=regex-chess
  cells=file-artifact:33,serialization-schema:8 set_equals_base_plus_member=1 located=1 executed=1
  cases=12 legs=60 mismatches=0 new_rows=8 new_rows_flagged=0 defects=0`, `PREDICATE R98-C1 pass`,
  rc 0 — the frozen TARGET string reproduced field-for-field.
- Spot checks agreeing with L7/L10 from raw bytes: executed ledger members 41 (BASE) → 42 (T);
  SOURCES markdown rows 317 (BASE) → 325 (T); `| S326 |` absent at BASE; S326–S333 present at T
  (S331–S333 marked rejected).

## Findings

### 1. Observe-only pytest hook is faithful; no masking path found — PASS

- Hook: `round98_regexchess_probe.py:146-161` (RUNNER). Call phase: `rep.when == "call"` → `P` only
  on `rep.passed` (:150-151); failure verdict from `call.excinfo.typename`, `AssertionError` → `F`,
  else `E:<typename>` (:152-154); no-excinfo odd outcome → `E:<rep.outcome>` (:155-156).
- Setup/teardown: non-call phases are recorded only when `rep.failed` (:149). A failed setup aborts
  the call phase (pytest `runtestprotocol` semantics), so a setup error cannot leave a stale `P`;
  the recorded verdict comes from the setup `CallInfo`'s excinfo — the true failing phase and type.
  A teardown failure after a passing call OVERWRITES `P` with `E:<type>` — fails closed.
- Uncollected/absent verdicts print `MISSING` (:159) and the probe's expected vector is built from
  `verdict.get(name, "MISSING")` (:286), which never equals a predicted `P`/`F`/`E:` — fails closed.
- xfail/skip masking is impossible for the captured file: `test_outputs.py` contains no
  `pytest.mark.*`, `xfail` or `skip` (pinned bytes `4983c44d…`; grep negative). Even hypothetically:
  non-strict xfail-fail still exposes call excinfo → `F`/`E:Skipped`; xpass reports `P` with pytest
  rc 0, exactly the real verifier's reward; strict xpass fails the run → rc ≠ 0 → reward 0.
- Corroborated by the committed dry-run history
  `.ufo/waves/round-98/L1/dryrun/README.md`: dry runs 1–2 parsed pytest's short summary (printed
  rewritten bare-assert text, `E:assert`), dry run 3 switched to the observe hook — the summary line
  is documented as not a type channel.
- L6 (`round98_c1_replay.py:259-278`) re-runs the probe from a `git archive` of T and requires the
  full CASE+DETAIL observation block byte-equal plus TOOL_SHA/CASE_TABLE_SHA/GRADER_SIDE stamps
  (:70, :273-275) — my run reproduced the committed block exactly.

### 2. Reward leg is pytest's own exit code — PASS

- Runner: `pytest.main(["-q","-p","no:cacheprovider","/tests/test_outputs.py"])` → `rc`
  (`probe:157`), `print("RC", rc)`, `sys.exit(rc)` (:160-161). Reward bit: `"1" if rc == 0 and
  proc.returncode == 0 else "0" if rc is not None else "NORC(%d)"` (:287) — i.e. pytest's exit code,
  with a crash guard: if the sandboxed runner dies before printing RC, the vector becomes
  `NORC(...)` ≠ predicted → probe rc 1. Cannot fake a pass.
- Captured verifier `test.sh:21-27`: `uvx … pytest --ctrf … /tests/test_outputs.py -rA`, then
  reward 1 iff `$? == 0` — same semantics. The replay pre-stages the venv (pins checked inside the
  sandbox, `probe:196-207`; mismatch → exit 2) matching the claims' "network before the probe".
- INFO (no action): the replay venv omits `pytest-json-ctrf==0.3.5` (present in test.sh uvx pins);
  it is a report-writer, verdict-neutral, and `-q`/`no:cacheprovider` differ from `-rA --ctrf` in
  output only. GRADER_UNPINNED (CPython micro 3.13.16) is stamped but deliberately excluded from
  re-run stamp equality (`probe:373`, `replay:70`) — honest, per round-96 W-2.

### 3. C09 lookup-table builder: fair adversarial artefact, not a voiding leak — PASS

- Builder (`probe:100-125`): monkeypatches `verify_legal_moves` to record exactly the FENs the
  grader would ask, then answers each with python-chess, mirroring the grader's own answer
  construction including the queen-promotion filter (`probe:107-108` ≡ `test_outputs.py:25-26`).
  Runs inside the same bwrap sandbox, same venv.
- The submitted artefact does no move generation at grade time — that is the located gap, not a
  flaw in the case: the grader tests only the three public games (`test_outputs.py:96-149`),
  membership-per-line + equal count (:34-41) cannot detect memorization, and the task statement
  itself promises "tested on other positions" (S329, instruction.md:27). C09 passing demonstrates
  the gap; C10 (one entry dropped → only Naroditsky–Ivanchuk fails) shows its granularity; C08
  bounds the `rpartition` ep-fallback (:35). The leak is the finding. Informativeness preserved.

### 4. Receipt LANE_TIP is the freeze F — PASS (nit)

- Committed receipt `corpus/evidence/round98/regexchess-probe.txt:7`:
  `LANE_TIP e1a3afd9069a19e38fd0bc3b015970231f303fc7` = F, the freeze commit; F verified ancestor
  of T. The probe stamps LANE_TIP as `git -C lane rev-parse HEAD` at run time (`probe:371`).
- NIT-1 (INFO): L3 (`replay:219`) checks LANE_TIP is an *ancestor* of --rev, not equal to F.
  Ancestry suffices for "receipt not fabricated after measurement" and the frozen C1 predicate does
  not constrain L3's strength; the receipt byte itself pins F. No action; note for round 99 if
  stronger pinning is ever wanted.

### 5. L7 set equality and L10 scope match the frozen predicate text exactly — PASS

- Frozen text: executed member set at T EQUALS BASE's set plus `regex-chess`; L10: BASE gate bytes
  flag none of the SOURCES rows added after BASE.
- L7 (`replay:283-293`): `set_ok = bool(base_set) and MEMBER not in base_set and rev_set ==
  base_set | {MEMBER}` — exact set equality (superset fails: round-97 MutC1), plus member
  status=executed, round=98, classes == ["file-artifact","serialization-schema"], legacy fields
  receipt/subject/verdict. Matches the frozen text clause-for-clause and strengthens it (member
  absent from BASE guarded).
- L10 (`replay:146-175`, :309-310): rows added after BASE = row-id set difference (BASE → rev) over
  `corpus/SOURCES.md`; runs the BASE *bytes* of `plans/anchor_digest_check.py` on a shared-clone
  checkout of rev; `l10 = bool(added) and not flagged` — the non-vacuity guard (added must be
  non-empty) goes beyond the frozen text in the safe direction. My run: new_rows=8
  new_rows_flagged=0, agreeing with the prefreeze control (`controls/README.md`: none of S326–S333
  flagged).
- TARGET format (`replay:317-321`) reproduces the frozen TARGET field-for-field in order; `legs=60`
  is 12 cases × 5 legs (`leg_order` length), `executed=1` is the leg conjunction. OBS-2 (INFO): no
  leg hard-asserts the literal `executed_rows=42`; the count is produced from the ledger and judged
  against the frozen string externally — consistent with the claims' "neither names a global row
  count" design; L7 pins the set, the printout pins the count for the reader.

### 6. Sandbox and lane hygiene — PASS

- Sandbox fixed at `/usr/bin/bwrap` (`probe:61,207-209`; round-97 MutC1), `--unshare-all
  --clearenv`, host /usr read-only, /etc unbound, captures pinned by sha before any run
  (`probe:335-338`), captured `solve.sh` executed unmodified for the positive control (`probe:269-277`,
  C01 transform `none`). Probe and counter both refuse work paths inside the lane (`probe:328-331`,
  `replay:183-185`); L10's gate fixture is its own shared clone under `--work`. My run mutated
  nothing in the lane; receipts only in `w1/ReviewC1/`.

## Observations (no action)

- OBS-1: verdicts keyed by `item.name` — duplicate test names would collide; the captured file has
  four unique names and is pinned by sha, so theoretical only (`probe:146-161`, :286).
- OBS-2: see NIT/OBS-2 above (executed_rows printed, not asserted).
- OBS-3: L9 compares HOST_BASH to the live host (`replay:299-303`) — a cross-host re-run fails the
  leg honestly rather than silently passing; matches the claims' "match the measured tree and host".

## Residual risk and verification gaps

- Reward-leg equivalence is argued from source + pins + the 12/12 match in two independent runs
  (official at F, my rerun within L6, my full counter run); it is not a bit-level reproduction of
  the uvx/ctrf environment. Judgment: immaterial to the frozen claim's wording ("pytest's own exit
  code").
- bwrap/userns prerequisites were verified present on this host (bwrap executable; max_user_namespaces
  122865); the counter refuses honestly when absent.
- C2 provenance binding is out of my scope (separate seat).

## Tooling record

Installed (scratch only, uv channel, no pacman): grader venv `uv venv -p 3.13` +
`uv pip install pytest==8.4.1 chess==1.11.2` (grader replay pins). No host tools added or changed.
Scratch removed after receipt copy.
