# ScoutSources — round 98 wave 1

Seat: `ScoutSources` (leaf, no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scratch: `/fast/scratch/hyaku/kengaku-r98/ScoutSources` (removed before yield).
Judged axes: **coverage** (R98-C1) and **freshness** (R98-C2).

**Verdict: both claims hold at T under independent re-execution — `PREDICATE R98-C1 pass` and
`PREDICATE R98-C2 pass` (both rc 0) — and no DEFECT was found in the SOURCES rows, the flat
capture, the provenance bindings, the ledger flip, the freeze, or the census. All 8 new rows and all
5 spot-checked population rows re-open live at their pinned URLs with bytes identical to the row
digest and to the committed capture. One non-blocking observation (collateral defect clearance) is
recorded in §6.**

---

## 0. Setup and provenance of the check

| item | value |
|---|---|
| clone | `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin clone`, detached at `8e37fc65d5649bb37166fdd6b1657445a8cb55b9` (= measured T) |
| `git rev-parse --show-toplevel` | `/fast/scratch/hyaku/kengaku-r98/ScoutSources/clone` (asserted before every fixture write) |
| fixture clones | `p0clone` (P0 `5584a6f7`), `l10tree` (T + BASE gate bytes), `fixt` (T, PROVENANCE.md removed and committed) — all under scratch, all `--shared` clones of the scratch clone |
| grader venv | `uv venv -p 3.13 G` (CPython 3.13.16) + `uv pip install --python G/bin/python pytest==8.4.1 chess==1.11.2`; verified `chess 1.11.2 / pytest 8.4.1` |
| tooling | `uv 0.13.0` (x86_64-unknown-linux-gnu) — already present at `/home/vgpnk/.local/bin/uv`, **no install performed, no pacman transaction** (host-wide pacman guard respected) |
| network | live re-open of 13 pinned `raw.githubusercontent.com` URLs, all HTTP 200 |
| scratch size | ≈ 180 MB (two `--shared` clones + venv + downloads); `TMPDIR` set explicitly to `<scratch>/tmp`; no `/tmp` use above 50 MB |

No production file in the lane, the fleet repo or any sibling repo was created, modified or deleted.
The only writes outside scratch are this report and the receipts under
`.ufo/waves/round-98/w1/ScoutSources/`.

---

## 1. R98-C1 — the eight new SOURCES rows S326–S333 re-opened live

Every row was re-opened at its pinned URL. For each: HTTP code, byte count, sha256 of the live
bytes, compared against (a) the sha256 and byte count written in the SOURCES row and (b) the
committed flat capture under `corpus/evidence/round98/tb2-regex-chess/`.

| row | URL path (repo `harbor-framework/terminal-bench-2`, pin `2fd12b88`) | live HTTP | live bytes | live sha256 | = row sha | = row bytes | = capture sha | = capture bytes | quote found at stated line |
|---|---|---|---|---|---|---|---|---|---|
| S326 | `regex-chess/tests/test_outputs.py` | 200 | 5356 | `4983c44d21c56dd8191381eff0304afc8b87bb714527ea9036b3319c015a30b4` | ✅ | ✅ | ✅ | ✅ | ✅ `tests/test_outputs.py:35` |
| S327 | `regex-chess/tests/test.sh` | 200 | 629 | `8f7f00a1c4dde7fcca6c918c768f2aba432b8c4007c15989716c68091950da87` | ✅ | ✅ | ✅ | ✅ | ✅ `tests/test.sh:21` |
| S328 | `regex-chess/solution/solve.sh` | 200 | 72716 | `b728bf0ea392a3d244afbd0818d36933c8d3e190e47743c1382cd518d518a2e9` | ✅ | ✅ | ✅ | ✅ | ✅ `solution/solve.sh:4` |
| S329 | `regex-chess/instruction.md` | 200 | 1632 | `a6ed3fcc54fc92d71a84af921942422d299ca89b410dcd92cd05a53d0d06436c` | ✅ | ✅ | ✅ | ✅ | ✅ `instruction.md:27` |
| S330 | `regex-chess/environment/Dockerfile` | 200 | 208 | `2616cd775252303839dfda0ee2f047eb862952b053b0103bd6b2460ef90c11b7` | ✅ | ✅ | ✅ | ✅ | ✅ `environment/Dockerfile:5` |
| S331 | `regex-chess/environment/check.py` | 200 | 4412 | `f9c416ae9ea01dcdd5f6a43170c8434b8c0a0b389a4a30876a2048e277d191c7` | ✅ | ✅ | ✅ | ✅ | ✅ `environment/check.py:98` |
| S332 | `regex-chess/task.toml` | 200 | 871 | `07fe52636fcc4bc9fff25d5630af145b97a5331219d719cc8decb4ca67ea21d4` | ✅ | ✅ | ✅ | ✅ | ✅ `task.toml:29` |
| S333 | `regex-chess/README.md` | 200 | 1830 | `9296cbee592fc996c58d228b51fee303647e5ecfae82d5666d42a40cb30ec355` | ✅ | ✅ | ✅ | ✅ | ✅ `README.md:33` |

**8/8 rows AGREE.** Every quoted fragment is present *at the stated line number* in the committed
capture (byte-identical to the live bytes), e.g. S326 line 35 is literally
`assert x in python_chess_moves or x.rpartition(" ")[0]+" -" in python_chess_moves, (`.

Row metadata as committed (SOURCES.md lines 342–349): S326–S330 `mined` / tier A (or docs for
S329) with `used-by plans/round98-cases.json`; S331, S332 `rejected` tier A; S333 `rejected` tier B
— matching the claim's "S326–S330 admitted (tier A), S331–S333 rejected with flips".

### Capture integrity
- `sha256sum -c corpus/evidence/round98/tb2-regex-chess/SHA256SUMS` → 8/8 **OK** (all eight files
  in the flat capture, including `README.md` and `SHA256SUMS` itself).
- The capture dir is **byte-identical P0 → T** (`git diff 5584a6f7..8e37fc65 -- corpus/evidence/round98/tb2-regex-chess/`
  shows only the P0-added files; the diff P0→T for that path is empty apart from the receipt added
  at C). No capture byte moved after F.
- The eight digests equal the frozen-instruments table in `plans/round-98-claims.md` for the seven
  files it names, and S333's digest equals the `README.md` entry in the capture's own `SHA256SUMS`.

### L10 — the new rows are flagged by no anchor-digest DEFECT
- Rows added after BASE = exactly `{S326…S333}` (BASE 317 rows, T 325 rows; nothing removed).
- The **BASE gate bytes** (`11bb2cad…`, byte-identical at BASE and at T) run against a
  `git clone --shared --no-checkout` fixture checked out at T: `rows=325 tokens=209 defects=45`,
  and **no `DEFECT S32x`/`S33x` line at all**. This reproduces the L10 leg exactly (same fixture
  construction the frozen script uses).
- The T gate bytes give the same `rows=325 tokens=209 defects=45` and the same absence.

---

## 2. R98-C2 — five spot rows of the 39-row population re-opened live

The population was taken from the frozen list `.ufo/waves/round-98/L1/c2-pop.txt` (39 rows) and
independently re-derived from the frozen script (`round98_c2_nested_bind.py --derive`) — the derived
set is **identical** to the committed list (39 rows, same digests, same capture paths, same
`# GATE_SHA 11bb2cad… n=39` footer).

| row | upstream subpath | live HTTP | live bytes | live sha256 | = row/pop token | = committed nested capture | capture == token | anchor quote at stated line |
|---|---|---|---|---|---|---|---|---|
| S181 | `bn-fit-modify/tests/test_outputs.py` | 200 | 5892 | `364069f893e336a021c907dd0ac11ff4c9e7ca7b4fa7ab506c360166960e455b` | ✅ | ✅ `corpus/evidence/round52/graders/bn-fit-modify/tests/test_outputs.py` | ✅ | ✅ line 14 = `"""Test that the sampled data from the fitted BN exists"""` (row states "line 14 docstring of test_bn_sample_exists (lines 13-17)") |
| S276 | `mteb-leaderboard/tests/test_outputs.py` | 200 | 537 | `b28f8fc8b7614801305813c402be52f4be1e75de6658ecdfdf9383aa793892cf` | ✅ | ✅ `…/round52/graders/mteb-leaderboard/tests/test_outputs.py` | ✅ | ✅ `test_outputs.py:15` |
| S290 | `schemelike-metacircular-eval/tests/test_outputs.py` | 200 | 6823 | `fbb84e3c0c2f72ed7de90f54380f860052c16155e7d0c9076cd57c966e9be7ed` | ✅ | ✅ `…/round93/graders/schemelike-metacircular-eval/tests/test_outputs.py` | ✅ | ✅ `tests/test_outputs.py:121` (`def test_interp():`) |
| S310 | `multi-source-data-merger/tests/test_outputs.py` | 200 | 1889 | `a070888930cf829aeca039771260b1386bda990ea805f313468d381ba3608ca5` | ✅ | ✅ `…/round96/graders/multi-source-data-merger/tests/test_outputs.py` | ✅ | ✅ `tests/test_outputs.py:53` (`if email_conflicts:`) |
| S322 | `sparql-university/environment/university_graph.ttl` | 200 | 10481 | `0b0b1f2c0ee7ea7ddc9382f94ff8181996ffa7be60a1651111c1f57b49e09a85` | ✅ | ✅ `…/round97/graders/sparql-university/environment/university_graph.ttl` | ✅ | ✅ `environment/university_graph.ttl:113` (`uni:hasName "Orfeas Menis" ;`) |

**5/5 spot rows AGREE** on every axis: live bytes still hash to the row's 64-hex token, and the
committed nested capture is byte-identical to the live fetch and hashes to the same token.

### Whole-population checks (39 rows, beyond the 5 spot checks)
- Every one of the 39 rows: token present in the SOURCES row text; named capture exists in the tree
  and hashes to the token. **0 issues.**
- Every one of the 39 rows: SOURCES row text **byte-identical BASE → T**; named capture
  **byte-identical BASE → T** and equal to the token. **0 issues.**
- `corpus/evidence/PROVENANCE.md`: 39 provenance rows, one per population row; each row's `file here`
  path is the tail of the population's capture path, each `sha256` equals the population token, and
  each `pinned URL` equals the URL in the corresponding SOURCES row. **0 mismatches.**

---

## 3. C2 predicate re-executed at T

```
$ python3 plans/round98_c2_nested_bind.py --lane . --rev 8e37fc65… --work <scratch>/w2
LEGS K1=pass K2=pass K3=pass K4=pass K5=pass K6=pass K7=pass
GATE defects base=86 rev=45
TARGET pop=39 cleared=39 still=0 unbound=0 rows_changed=0 captures_changed=0 new_old_row_defects=0
PREDICATE R98-C2 pass        rc=0
```

Matches the frozen predicate string in `plans/round-98-claims.md` exactly. The `GATE defects
base=86 rev=45` line is informational (the claim says so) and is consistent with the claim's own
statement that BASE had 86 defects.

### Falsification of the C2 mechanism (independent of the frozen counter)
The claim's causal story — "the gate cannot reach nested captures; one new file
`corpus/evidence/PROVENANCE.md` binds them through the gate's provenance-row rule" — was tested by
removing only that file in a fixture:

| fixture (clone at T, `--show-toplevel` asserted) | gate result | population rows still flagged |
|---|---|---|
| T as committed | `rows=325 tokens=209 defects=45` | **0 of 39** |
| T with `corpus/evidence/PROVENANCE.md` deleted from the worktree only | `defects=45` | 0 of 39 (worktree deletion does not bind — the gate reads committed/index state) |
| T with `corpus/evidence/PROVENANCE.md` deleted **and committed** (fixture commit `61470aa9`) | `rows=325 tokens=209 defects=86` | **39 of 39** |

So the provenance file is the *sole* cause of the 39-row clearance: removing it (as a commit)
restores every one of the 39 `anchor-unbound` defects and the defect count returns to the BASE
value 86. That is exactly the mechanism the claim asserts, independently reproduced.

---

## 4. Census at T

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
kengaku  W04  S040 duplicate url … (30 lines)
kengaku  ok    /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
rc = 0
```

**rc = 0.** 30 `W04` warnings, **0 `E*` errors** — identical to the pre-freeze expectation
("only the 30 pre-existing W04 warnings"). None of the 30 warnings names S326–S333, so the eight new
rows introduce no new warning. The census was also run against a `git archive` extract of T
(`--file …/Ttree/corpus/SOURCES.md`): **rc = 0**, and the finding set is line-for-line identical to
the lane run (only the file path in the `ok` line differs), so the clean verdict is a property of T's
bytes, not of the lane's later integration commit.

---

## 5. Ledger, freeze and candidate-byte checks (supporting C1)

| check | result |
|---|---|
| ledger at BASE vs T | BASE executed set = 41 members; T = 42; `added = {regex-chess}`, `removed = {}` → **set equality BASE ∪ {regex-chess} holds** (the round-97 MutC1 superset hole is closed) |
| class cells | BASE `file-artifact` 32 → T 33; `serialization-schema` 7 → T 8 (claims say 32→33 of 76 and 7→8 of 10) |
| `regex-chess` ledger entry | `status: executed`, `round: 98`, `receipt: corpus/evidence/round98/regexchess-probe.txt`, `verdict: cases`, `reason: replayed` |
| frozen instruments at T | all 13 digests in the `frozen-instruments` table of `plans/round-98-claims.md` reproduce byte-for-byte at T (`87163078…`, `02f30e6a…`, `e3613832…`, `77c6ba05…`, `31493146…`, `11bb2cad…`, `4983c44d…`, `8f7f00a1…`, `b728bf0e…`, `2616cd77…`, `f9c416ae…`, `07fe5263…`, `a6ed3fcc…`) |
| freeze F → T | `git diff e1a3afd9..8e37fc65` over every frozen path is **empty** — no frozen instrument changed after F. The only commit between F and T is C (`8e37fc65`) |
| candidate bytes at T | `SKILL.md` `6daa8e1d…`, `plans/grader-population-ledger.json` `915c3b44…`, `corpus/SOURCES.md` `793b0520…`, `corpus/evidence/PROVENANCE.md` `d3fc4b7c…` — all equal the `candidate-bytes` table |
| C commit file set | `8e37fc65` touches exactly `SKILL.md`, `plans/grader-population-ledger.json`, `corpus/SOURCES.md`, `corpus/evidence/PROVENANCE.md`, `corpus/evidence/round98/regexchess-probe.txt` — the four candidate files plus the one receipt, as the claim requires |
| candidate bytes unchanged after C | `corpus/SOURCES.md`, `corpus/evidence/PROVENANCE.md`, the ledger and `SKILL.md` are byte-identical between T and the lane HEAD (`4654ffc1`) |
| ledger flip | `executed_rows` 41 → 42 with member `regex-chess` and set equality — confirmed by direct ledger diff, independent of the counter |
| probe receipt | `corpus/evidence/round98/regexchess-probe.txt` lists 12 cases C01–C12, each with `predicted`/`observed` equal and `ok=True`, `mismatches 0`; the five graded cases' rebuilt artefacts in the replay work dir (`C01,C04,C07,C11,C12`) hash to the receipt's `DETAIL … sha=` values exactly (e.g. C01 `19dbeb84c93f34f5`, C12 `4dc7986c2c20d5de`) — the committed receipt is reproducible, not hand-written |
| registry rows | `SKILL.md` carries the four `round98-*` rows (`round98-regexchess-probe`, `round98-c1-replay`, `round98-c2-nested-bind`, `round98-provenance-build`) |

---

## 6. Observations (non-blocking)

1. **Collateral defect clearance beyond the population.** The gate's defect count drops 86 → 45, i.e.
   **41 defect lines** clear, while the population is 39 rows. The extra two are outside the
   population and are *not* counted by the frozen counter (which scopes to `POP`):
   - `S213` (a correction row for the same `chess-best-move/tests/test_outputs.py` upstream as
     `S201`): its `anchor-unbound` line clears because the gate's `provenance-url` rule now resolves
     that subpath. Its remaining `token-outside-anchor` line is unrelated and stays.
   - `S230` (`kv-store-grpc/tests/test_outputs.py`, same upstream as `S234`): its
     `digest-wrong-capture` line clears for the same reason.

   Both are **cleared, not introduced** — the gate reports 0 new defect rows at T. The claim's
   predicate is scoped to the population and its `new_old_row_defects=0` holds. Worth recording so the
   86→45 delta is not read as "39 rows cleared" plus "2 unexplained": the mechanism is one new file
   binding 38 distinct upstream subpaths, which incidentally reaches two rows the population rule
   (single-defect, `anchor-unbound`, nested-upstream) excludes — `S213` had two defects and `S230`
   had a `digest-wrong-capture` class.
2. **The BASE gate bytes and the T gate bytes are the same file** (`11bb2cad…` at BASE and at T).
   The claim's L10 wording ("the BASE gate bytes flag none of the SOURCES rows added after BASE") is
   therefore a statement about the same instrument, and it holds: 0 of the 8 new rows are flagged
   under either copy.
3. `c2-pop.txt` is byte-equal to what `round98_c2_nested_bind.py --derive` produces today, so the
   frozen population is reproducible from the frozen script, not hand-maintained.

No defect was found in the SOURCES rows, the flat capture, the provenance bindings, the ledger
flip, the freeze, or the census.

---

## 7. R98-C1 counter re-execution — PASS at T

The frozen counter was run in the scratch clone against the measured tip:

```
$ python3 plans/round98_c1_replay.py --lane . --rev 8e37fc65d5649bb37166fdd6b1657445a8cb55b9 \
      --work <scratch>/w --grader-venv <scratch>/G
LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass L10=pass
TARGET executed_rows=42 member=regex-chess cells=file-artifact:33,serialization-schema:8 set_equals_base_plus_member=1 located=1 executed=1 cases=12 legs=60 mismatches=0 new_rows=8 new_rows_flagged=0 defects=0
PREDICATE R98-C1 pass        rc=0
```

The `TARGET` line is character-for-character the frozen target string in `plans/round-98-claims.md`:
executed rows 41→42, set equality with BASE plus the single member `regex-chess`, the two class
cells 32→33 and 7→8, 12 cases × 5 legs = 60 observed legs, 0 mismatches, 8 new rows, **0 of them
flagged by the anchor-digest gate** (`new_rows_flagged=0`, the L10 leg), and 0 defects.

Both frozen predicates now re-executed independently at T:
- `PREDICATE R98-C1 pass` (rc 0) — receipt `c1_replay_T.txt`.
- `PREDICATE R98-C2 pass` (rc 0) — receipt `c2_replay_T.txt`.

Neither kill rule fires: no leg failed, both predicates print `pass`, no frozen file changed after F,
and C landed exactly the candidate-bytes table plus the one receipt path.

---

## 8. Receipts

Under `.ufo/waves/round-98/w1/ScoutSources/`:

| file | content |
|---|---|
| `source-reopen-results.json` | per-row machine record: live code/bytes/sha, row sha/bytes, capture sha/bytes, quote-at-line flags (8 new rows + 5 spot rows) |
| `live-fetch-digests.txt` | sha256 + byte size of every one of the 13 live downloads |
| `census.txt` | census `validate --root … kengaku` output (rc 0) |
| `census_T_file.txt` | census `validate --file` against the `git archive` extract of T (rc 0) |
| `gate_T_verbose.txt` | `anchor_digest_check.py --verbose` at T (45 defects; 0 from the population; 0 from S326–S333) |
| `gate_P0_verbose.txt` | same gate at P0 (86 defects; all 39 population rows flagged) |
| `gate_BASEbytes_on_T.txt` | BASE gate bytes on a T checkout (L10 reproduction: 45 defects, 0 new-row flags) |
| `gate_T_without_PROVENANCE.txt` | T with PROVENANCE.md removed from the worktree only (uncommitted → no effect) |
| `gate_T_no_prov_committed.txt` | T with PROVENANCE.md removed **and committed** → 86 defects, 39/39 population rows flagged (mechanism falsification) |
| `c2_replay_T.txt` | the C2 counter's output at T (K1–K7 pass, TARGET pop=39 cleared=39, PREDICATE pass) |
| `c1_replay_T.txt` | the C1 counter's output at T (L1–L10 pass, TARGET executed_rows=42 … new_rows_flagged=0, PREDICATE pass) |
