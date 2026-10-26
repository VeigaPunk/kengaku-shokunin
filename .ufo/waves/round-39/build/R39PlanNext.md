# R39PlanNext — `### Planned (round 40)` data walk (kengaku r39, wave 1, scout)

Seat: R39PlanNext (scout, leaf). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` at
`750473847af9c7a461487ba3a589b5519fac5ed8`, read-only; nothing in the lane was edited, staged or committed. Scratch
`/fast/scratch/hyaku/kengaku-r39/R39PlanNext/` (removed at the end, §9). Receipts copied first to
`.ufo/waves/round-39/build/R39PlanNext/` (harnesses, outputs, case tables; harness scripts name the scratch paths they ran
under).

Axes named before work (Godspeed): **A1** class distance from the five graders read (data string, agent regex, live
service, build provenance, repo-history state); **A2** offline executability with a task-oracle control; **A3** quote
supply; **A4** prior-art clearance; **A5** reach of a calibration gap by a frozen counter; **A6** a do-nothing control run
now. A2/A5/A6 ran first (cheap, executable); A4 only on survivors.

## 0. Headline

Three candidates priced, each with a control executed this seat.

1. **Calibration (8): the tripwire tools' mutants, re-priced.** The standing detectors kill **0 of the 17 mutants** the
   plan below would freeze (anchor 10 + `ledger_tip` 7), and 2 of 26 anchor mutants / 1 of 20 `ledger_tip` mutants
   overall. Round 38's "1 of 5" has moved: D3/D4 landed and the anchor tool now has fixtures — but they sit in a wave
   directory, not in `plans/`, and kill 7 of 26. A fixture set written this seat kills 23 of 26 and 15 of 20, so the gap is
   fixtures, not tool design. The newest tripwire (`order_check.py`, R39OrderGate) killed 6/6 of its author's mutants and
   **4 of 13** of mine.
2. **Coverage (7, capped): TB2 `db-wal-recovery`** is the cleanest next grader (task oracle passes 7/7 offline, nop fails
   7/7, byte-equal reruns); **`openssl-selfsigned-cert`** is the richer one (26 cases, 25/26 predictions right, one grader
   defect no one has filed) but its oracle **fails its own grader on this host's OpenSSL 3.6.5** (5/6). Recommendation:
   db-wal-recovery first, openssl as fallback with the version limit declared.
3. **Novelty (not filed): grader re-run stability.** `polyglot-c-py`: a valid answer passes the grader and the same state
   fails the second grading (`['main.py.c', 'cmain']`); db-wal and openssl graders are idempotent. Priced as a rider on the
   coverage probe (one extra grading per case), not a claim: TB guidance on repeat verification exists (§4).

## 1. Inputs read

`.ufo/waves/round-38/build/R38PlanNext.md` (full); `plans/round-39-claims.md` (full);
`corpus/lessons/round-38-verifier-spotcheck.md` (full); `plans/anchor_digest_check.py` (full), `plans/ledger_tip.py`
(full), `plans/round37_c1_attribution.py` (full), `plans/mutant_direction_check.py` (head), `plans/tip_receipts.py` (head);
`.ufo/waves/round-38/build/R38AnchorBind/run_fixtures.py` (full), `falsify/F38AnchorFix.md` (full), `falsify/F38MutDirection.md`
and `falsify/F38TipReceipts.md` (verdict lines); round-39 wave-1 drafts `R39AnchorUnion/anchor_digest_check.py`,
`R39LedgerProvenance/ledger_tip.py`, `R39OrderGate/order_check.py` + `calibrate.py` (read, run, not edited). TB2 at the pin:
blobless clone, `git rev-parse origin/HEAD` = `2fd12b88aafdd04a52c298e3940bcb189f9766d6` = the lane's pin; all 89
`tests/test_outputs.py` + `instruction.md` + `environment/` read by script (`tb2_census.json`, `tb2_callable.json`).

## 2. Candidate A — calibration (8): mutants of the lane's tripwire tools

### 2.1 What changed since round 38

`R38PlanNext` §3 priced five anchor mutants at `kills=1` and listed `ledger_tip` D4 and the attribution audit. Since then:
D3 (`anchor_digest_check.py` row-bound rewrite, sha256 `98847e89…`) and D4 (`ledger_tip.py` detached-ref binding, `f5baea44…`)
landed at `d93b7d68`; this round's R5 drafts exist unlanded (`R39AnchorUnion/anchor_digest_check.py` `11bb2cad…`,
`R39LedgerProvenance/ledger_tip.py` `853bcb2a…`); `order_check.py` (`948d5e1d…`) is new this round. The attribution audit is
**dropped**: it audits only the round-37 counter, and the round-39 counter's own docstring carries the attributed kill rule
(`plans/round39_c1_verify.py:4`), so its four old mutants no longer price a live gap.

### 2.2 Method (executed)

Per tool, a mutant table `old → new` (single replacement, `old` occurs once) and a fixture set; a mutant is **killed** by a
fixture when `(exit code, sorted DEFECT classes, last summary line, first stderr line)` differs from the unmodified tool on
that fixture. That is a result difference, not an attributed kill; attribution is counter work (§2.7). Three detector
tiers: **tip** = the run the lane does today (`defects=0` / `mismatches=0` on the tip tree); **standing** = tip + the
fixtures already written (anchor: the 12 `R38AnchorBind/run_fixtures.py` fixtures; ledger: the four `--source` shapes T00–T03);
**mine** = a fixture set written this seat (35 anchor fixtures incl. tip + the 12; 13 ledger fixtures). Harnesses:
`h_anchor.py`, `h_ledger.py` (re-run with `TOOL=<draft> TAG=_r5` for the R5 drafts).

### 2.3 Anchor tool, 26 mutants (tip `7504738`, tool `98847e89…`)

```
$ python3 h_anchor.py                       # out_anchor2.txt
MUTANTS n=26 killed_by_tip=2 killed_by_tip+r38_fixtures=7 killed_by_all_fixtures=23
```

| group | mutants | killed by |
|---|---|---|
| tip only | A12 erratum exemption off, A23 `task.toml` slug binding off | 2/26 (both turn the tip red) |
| + 12 round-38 fixtures | A11 wrong-capture relabelled, A13 erratum laundering via global A, A14 erratum unresolved-hex off, A19 exit always 0, A26 unbound rows pass through | 7/26 |
| + 22 new fixtures of mine (16 more mutants) | A01 uppercase accepted (`X01`), A02 abbrev floor 8→1 (`X03`), A03 ceiling 63→64 (`X05`), A05 prefix unchecked (`X02`,`X22`), A06/A07 row-indent 3→4 / 3→2 (`X09`,`X08`), A08 outside-anchor rule off (`X06`), A09 12-cell rows (`X07`), A15 ambiguous slug binds (`X17`), A17 head/index swapped (`X15`,`X17`), A18 token count (`X06`, summary text only), A20 usage exit 2→1 (`X18`), A21 manifest case not folded (`X21`), A22 manifest view ignored (`X20`,`X21`), A24 prefix→substring (`X22`), A25 erratum indent unbounded (`X13`) | 23/26 |
| survive | **A04** abbrev lowercase rule dropped (class-identical; only `detail=` text differs), **A10** (`not row_scope` → `is None`; equivalent for any bound row), **A16** (task component may be the file basename; equivalent while no slug equals a basename) | 3/26 |

Pristine verdicts on the fixtures are in `out_anchor2.txt` (`== pristine verdicts ==`). Fixture `X19` (no-evidence usage)
turned out not to reach its path (rc 0 in head mode) and is not counted as a witness. Pre-freeze witnesses for a frozen
list are the killer lists above (fixture ids in `h_anchor.py`).

**R5 draft** (`R39AnchorUnion`, `11bb2cad…`): same harness, `TOOL=… TAG=_r5` (`out_anchor_r5.txt`): tip stays
`rows=109 tokens=17 defects=0`; the second-URL shape (`X10`, F38AnchorFix F1) goes from rc 0 `defects=0` to rc 1
`class=capture-unanchored`; two needles move (A05, A24: `SETUP needle count 0`), so `n=24`, `killed_by_all=21`, survivors the
same A04/A10/A16. The new `capture-unanchored` class has no mutant yet (one more row for the table).

### 2.4 `ledger_tip.py`, 20 mutants (tool `f5baea44…`)

```
$ python3 h_ledger.py                       # out_ledger.txt
MUTANTS n=20 killed_by_tip=1 killed_by_tip+d4=5 killed_by_all=15
```

Killed by tip alone: L17 (a `kind=` label). Killed by the D4 fixtures (T02/T03 detached / stale `--source`): L02 never bind,
L03 bind not applied, L04 `REF BIND` line dropped, L16 double bind print. Killed only by fixtures of mine: L01 refuse
exit 2→1 (T08/T09), L05 open-row staleness ignored (T05), L06 zero rows accepted (T06), L07/L08/L09/L18 counters (T04,T05,
T07,T10–T12), L11 existing clone dir reused (T09), L14 crash counted as pass (T10), L15 unknown check counted as pass (T07).
Survivors (5): **L10** (D4 revert: `CalledProcessError` folded back into a mismatch — reachable with a fixture whose tree
has a deleted object; not built), **L12, L13** (clean-tree and clone-top refusals: a fresh `git clone --shared` is always
clean/top-level, so unreachable through `--source`), **L19** (no-tip refusal, unreachable), **L20** (equivalent rebinding).

The reason most of these survive the tip run is arithmetic: every ledger row is `closed` and passing, so `passed += 1`,
`closed += 1`, `mism += 0` and `agree = ok` all print the same line.

**R5 draft** (`R39LedgerProvenance`, `853bcb2a…`; `out_ledger_r5.txt`): `n=18` (L02, L04 needles moved),
`killed_by_tip=2 killed_by_tip+d4=3 killed_by_all=13`. Control-mode stale `master` (F38LedgerTip F1), measured both ways in
a clone with `master` at `HEAD~6` and `HEAD` detached at the tip:

```
$ python3 plans/ledger_tip.py --lane .                         -> rows=9 closed=9 observed_pass=9 mismatches=0   rc=0   (silent)
$ python3 <R39LedgerProvenance/ledger_tip.py> --lane .         -> REFUSE stale pin ref: refs/heads/master resolves to 10d2e977… but the commit under audit is 75047384…   rc=2
```

The `--source` stale shape (T03) is identical in both tools (`refbind=1`), so the draft's new refusal needs the control-mode
fixture above in the table; no mutant of that clause exists yet.

### 2.5 `order_check.py` (new this round), 13 non-author mutants

`R39OrderGate/calibrate.py` ships 13 fixtures and 6 author mutants (6/6 killed, attributed). I added 14 single-line mutants
`O01–O14` (`order-mutants/`) and ran the author's fixtures against each (`calibrate.py --gate <mutant>`; O08 needle absent,
13 valid):

| result | mutants |
|---|---|
| killed (4) | O01 oldest add→newest add (f5b), O03 `gate:` echo prefix not read (f1, f7), O06 wrong round dir (f1, f2, f7), O09 setup error exits 1 (f9, f10, f11) |
| survive, reachable with one new fixture (4) | O04 excuse applies to `P10 ok` lines, O12 non-blob tree entries scanned, O13 `CASE` arm unanchored (`search` for `match`), O14 claims-name regex unanchored |
| survive, equivalent or redundant (5) | O02 `--diff-filter=A`→`AM`, O05 blob attributed to last commit (text only), O07 HEAD-commit guard (the next guard refuses anyway, exit 2), O10 distinct-commit guard (same exit), O11 `rev-list` pathspec (count only) |

Author mutants 6/6, non-author 4/13: the same asymmetry rounds 37 and 38 recorded for batteries, now on a tool.

### 2.6 What is not priced

`mutant_direction_check.py`: `F38MutDirection` measured 1 of 3 mutants caught (m1, m2 survive); `R39DirCheckLeg` is drafting the
redundant leg, so not re-run. `tip_receipts.py`: tamper control 4/4 (`F38TipReceipts`), no source mutants ever priced and its
verdict depends on `--only` (F5); not re-run.

### 2.7 Counter sketch

`plans/round40_c1_verify.py`, structure of `round39_c1_verify.py`: pins the three tools (post-landing bytes) and the
round-37/38/39 counters; a frozen `MUTANTS` table `Tnn | tool | old -> new | direction | advertised behaviour | witness`;
fixtures built by the counter in a child process from a fresh clone (anchor lane-trees, a `--source` / control-mode ledger
set, a git-history set for the order gate). Kill = attributed: the mutant's own class line / exit code changes in the
declared direction. Starting list, all pre-witnessed above and **all 17 unkilled by tip and standing detectors**:

- anchor (10): A01, A02, A03, A06, A08, A09, A15, A17, A21, A22;
- `ledger_tip` (7): L01, L05, L06, L08, L11, L14, L15;
- order gate (+4, witnesses to be written in wave 1 before freeze, Q29): O04, O12, O13, O14;
- the R5 clauses (`capture-unanchored`, stale-ref REFUSE): one mutant each once the drafts land.

Equivalents (A10, A16, L12, L13, L19, L20, O02, O05, O07, O10, O11) are listed in the claims file as limits, never removed
(round-38/39 rule). Sequence: the counter freezes **after** the R5 drafts are integrated in `plans/` — A05, A24, L02, L04
already moved needles in the drafts, so a freeze against the unlanded bytes would invalidate mutants.

## 3. Candidate B — coverage (7, capped): the next TB2 grader

### 3.1 Census of the 89 graders at the pin (`tb2_census.json`, `tb2_callable.json`)

| measure | result | command |
|---|---|---|
| graders whose test module parses and has no fixtures/marks and no missing host import (callable without pytest) | 58 of 89 (30 import something absent: `pandas`, `torch`, `Bio`, `selenium`, …; 7 use fixtures or marks) | `ast` scan + `importlib.util.find_spec` |
| graders with a compile / build / write call (static, heuristic) | 27 of 89 (`state-mutating-graders-static.txt`) | regex scan |
| quote supply (3–25-word lines) `test_outputs.py` / `instruction.md` | `db-wal-recovery` 69 / 12; `openssl-selfsigned-cert` 90 / 22; `polyglot-c-py` 21 / 5; `fix-git` 16 / **0**; `cancel-async-tasks` 48 / **0** | line scan |

Already read by the lane: `protein-assembly`, `regex-log`, `configure-git-webserver`, `build-pmars`, `git-leak-recovery`
(round 39 C2). Next free SOURCES ids: S119, S120 (S117/S118 are round 39's).

### 3.2 `db-wal-recovery` (`environment/` = `main.db` 8192 B + `main.db-wal.encrypted` 16512 B; offline, exact)

Pin digests (`git show 2fd12b88:<f> | sha256sum`): `tests/test_outputs.py` blob `faf2f70e5744`, sha256 `88dc5c2a3abba75b…`, 107 lines, 7 tests;
`instruction.md` blob `474ffff6e05d`, `5a20375162921b89…`, 14 lines; `solution/solve.sh` blob `c76aef172efc`, 105 lines;
`environment/main.db` `68cb288eb29e76d8…`, `main.db-wal.encrypted` `68753bdce26196a5…`.

Executed offline (`bwrap --unshare-net`, `/app` seeded from the two committed files, `/solution` and `/tests` bound, test
functions called after import; sqlite3 3.54.0, host `sqlite3` + `xxd`; `dbwal/run.py`, `run1.txt`, second run `cmp` byte-equal):

```
nop                              tests=7 fail=7
oracle-solve.sh                  tests=7 fail=0
base-only-5-rows                 tests=7 fail=2 recovered_data_completeness,wal_was_decrypted
typed-literals-never-open-db     tests=7 fail=0
typed-literals-names1-2-wrong    tests=7 fail=0
typed-literals-id3-name-wrong    tests=7 fail=1 recovered_data_completeness
value-float                      tests=7 fail=1 recovered_data_structure
```

Read, with locations (`tests/test_outputs.py`): the expected answer is a literal in the grader; `test_recovered_data_completeness`
pins `value` only for ids 1 and 2 (150, 250) and `name` for ids 3–11 — 22 of the 33 id/name/value cells; names of ids 1–2 and
values of ids 3–11 are unpinned (11 cells), and a hand-typed JSON that never opens the database passes 7/7. `test_wal_was_decrypted`
repeats the completeness test, and "Fix the WAL file" (`instruction.md`, step 1) is never checked.

**Destructive-read trap (measured):** `sqlite3 /app/main.db "select count(*) from items;"` returns 5 and afterwards `main.db-wal`
(16512 B) is **gone**; with `file:/app/main.db?mode=ro` it is untouched (`sha256 68753bdc…` before and after, plus a 32768 B
`main.db-shm`). The oracle's own comment says "read-only to avoid WAL interaction" (`solve.sh`), and a `web_search` snippet
(not opened) cites a third-party write-up reporting the same failure, so this is published — **prior art exists for the trap;
no novelty is claimed**. Image sqlite is Ubuntu 24.04's, not 3.54.0: limit.

A2 holds fully (nop 7/7 fail, oracle 7/7 pass, reruns equal, grader idempotent: two gradings of the oracle state both `fail=0`).
A1: data-literal grader again (class distance to `protein-assembly` small), but the graded state is a binary file pair with an
irreversible first command — new to the lane.

### 3.3 `openssl-selfsigned-cert` (no environment files; host `openssl`; 26-case probe built and run)

Pin digests: `tests/test_outputs.py` blob `e81aaade1618`, `90970bb3c372e8e7…`, 160 lines, 6 tests; `instruction.md` blob
`8ed50b24d2b0`, `38054a3371f7c2c8…`, 29 lines; `solution/solve.sh` blob `8058f1efb55c`, 98 lines.

`ossl/cases.py` (predictions written first; `ossl/dry-table.txt` sha256 `010ae622bef0f831…`: `cases=26 predicted_pass=15 predicted_fail=11`),
`ossl/run.py` (bwrap `--unshare-net`, host OpenSSL 3.6.5):

```
cases=26 observed_pass=14 observed_fail=12 mismatches=1      (run1.txt == run2.txt, cmp byte-equal)
```

The one `match=NO`: `names-only-in-issuer` fails `verification.txt` (its subject line is the cert's real subject), a prediction error of mine.
Headline observations (each is a case, with the grader location):

- **`key-mode-577` passes 6/6** — `assert key_permissions <= 0o600` (`test_outputs.py:22`) compares numerically, so `r-xrwxrwx` passes;
  644 fails. With bwrap `--cap-add ALL --uid 0` (root-like, as the task agent runs) **`key-mode-000` also passes** (`run_root.txt`:
  2 mismatches against the unprivileged table, the second being that case), i.e. the verdict is privilege-dependent.
- `not-self-signed` (issuer ≠ subject), `validity-in-the-past` (notBefore/After in 2000), `days-365-plus-23h59` (`timedelta.days` floors),
  `key-cert-mismatch` (unrelated 2048-bit key), `pem-unrelated-key`, `pem-fake-key-comment` (`# PRIVATE KEY` string), `org-suffix`,
  `cn-suffix` all pass 6/6; `verif-fabricated` (invented fingerprint and date) and `script-prints-literals-only` pass 6/6;
  `script-only-no-cert` passes the script test alone.
- **Oracle caveat:** the task's `solve.sh` run in the sandbox passes 5 of 6 — `test_python_verification_script` fails
  "does not display Common Name" because the oracle's `check_cert.py` splits on `"CN = "` and OpenSSL 3.6.5 prints
  `subject=O=DevOps Team, CN=dev-internal.company.local`. The image is `python:3.13-slim-bookworm`, whose OpenSSL 3.0.x prints
  the spaced form [INFERENCE, not pulled]. A probe on this host cannot show "oracle 6/6"; it needs either that limit named or an
  OpenSSL 3.0 binary (none available offline here; no pacman, no `uv` OpenSSL CLI). Grader idempotent (two gradings of one
  good state both `fail=0`).

Prior art: `gh api search/issues` on `repo:harbor-framework/terminal-bench-2` for `openssl-selfsigned-cert`, `openssl`,
`db-wal-recovery`, `wal` returned `total_count=0` each (search-index result, not proof of absence).

### 3.4 Alternates and refusals

`polyglot-c-py` (1 test, 21/5 quotes; graded state one file; **non-idempotent**, §4) — good novelty rider, thin as a package;
`constraints-scheduling` (the grader embeds its own `_hard_ok` solver and pins input sha256s; read lines 1–60 only, **not
executed**) — a "grader carries a reference implementation" class, a differential-test candidate for round 41, unpriced;
`fix-git` and `cancel-async-tasks` refused (0 quote-eligible instruction lines); `sanitize-git-repo` refused again (pins an
upstream commit); `prove-plus-comm` needs `coqc` (absent here).

## 4. Candidate C — novelty (not filed): grader re-run stability

Question: does a grader give the same verdict when run twice on one state? The lane's probes always grade a freshly built
state, so the property was never observed.

Control (executed; `poly/h.py`, `poly/run1.txt`; a valid polyglot, 15-line file, python/C via `#if 0` / `'''`, graded inside
bwrap with the task's grader called twice):

```
GRADE 1 PASS
GRADE 2 FAIL AssertionError Expected only main.py.c, found: ['main.py.c', 'cmain']
fresh-state grade PASS   (twice, each on a rebuilt state)
```

The grader compiles `cmain` into the graded directory (`polyglot-c-py/tests/test_outputs.py`) and then requires
`os.listdir == ['main.py.c']`. db-wal and openssl: both gradings `fail=0`. Static screen (heuristic, not a measurement of
non-idempotence): 27 of 89 graders contain compile or write calls. Prior art: one `web_search` (LLM-synthesised prose,
snippets only, not opened) says TB authoring guidance expects deterministic verifier results on repeat runs; a prior-art seat
would have to open `docs/` and the `SEPARATE_VERIFIER_CONVERSION` page. **Not filed as novelty**: standalone it needs ~10
offline-buildable oracle states (not measured), and the published guidance probably covers the finding. As a rider on plan B
it costs one extra grading per probe case.

## 5. DRAFT — `### Planned (round 40)` (paste-ready for `SCORECARD.md`)

```markdown
### Planned (round 40)

- **Calibration (8, lowest-tied candidate; L1 to confirm against the round-39 axis table):** mutation-test the lane's
  tripwire tools, which no round has frozen a mutant list for: `plans/anchor_digest_check.py`, `plans/ledger_tip.py`,
  `plans/order_check.py` (the R5 fixes and the order gate integrated and committed first, so mutant `old` strings target
  landed bytes — the R5 drafts already move four needles). Measured at `7504738` with a controlled harness
  (`.ufo/waves/round-39/build/R39PlanNext.md` §2): 26 anchor mutants, of which the tip run kills 2 and the round-38
  fixtures 7 (a 35-fixture set kills 23); 20 `ledger_tip` mutants, tip run kills 1, the four detached-source fixtures 5 (a
  13-fixture set kills 15); the new order gate kills 6/6 of its author's mutants and 4/13 of a non-author's. The frozen
  list is the 17 pre-witnessed mutants no standing detector kills (anchor 10, `ledger_tip` 7) plus the four order-gate
  mutants once their witnesses are committed and one mutant per R5 clause; equivalents are listed as limits, never
  removed. Counter `plans/round40_c1_verify.py` = the round-39 structure over these tools: pins, child-process fixtures,
  attributed kill (the mutant's own class / exit changes in its declared direction, Q29). Predicate (to freeze):
  `MUTANTS total=<n> killed=<n> survived=0 invalid=0 null_detected=0`, then `PREDICATE C1 pass`. Before / do-nothing
  (measured now): the standing detectors kill 0 of the 17; skip-control: an exit-code-only detector must print
  `survived>0` [INFERENCE, not run], an empty fixture dir `killed=0`. Kill rule as rounds 38–39: any survivor, invalid mutant or null
  detection means not admitted.
- **Coverage / novelty (7, capped by the open L0 question `kengaku | round-33`; judged on its counter, no score move
  claimed):** a sixth Terminal-Bench 2.0 grader, `db-wal-recovery` @ `2fd12b88` — a binary-format-recovery grader whose graded
  state is a SQLite file plus an XOR-encrypted WAL (rows S119 `tests/test_outputs.py`, S120 `instruction.md`, ids re-derived
  at freeze; `solve.sh`, `test.sh`, `Dockerfile`, `main.db`, `main.db-wal.encrypted` captured). Measured offline in a
  `--unshare-net` sandbox: the task oracle passes 7/7, the untouched state fails 7/7, base-only data fails 2, a hand-typed
  JSON that never opens the database passes 7/7 (values of ids 3–11 and names of ids 1–2 are unpinned: 11 of 33 cells), and
  a plain `sqlite3 /app/main.db "select …"` deletes the encrypted WAL while `mode=ro` leaves it (published: the oracle's own
  comment; novelty not claimed). Package, probe (cases and `violates=` tags frozen before the first recorded run, first run
  recorded before any `--rerun` control and checked by `plans/order_check.py`), counter and predicate as round 39 C2
  (`checks=7 defects=0`, `PREDICATE C2 pass`, receipt `mismatches=0`, byte-equal second run). Every probe case is graded
  twice on the same state and the verdicts compared (re-run stability; `polyglot-c-py` shows the failure mode, §4).
  Fallback, already executed (26 cases, 25/26 predicted, byte-equal): `openssl-selfsigned-cert` — grader defects measured
  (numeric `<= 0o600` lets mode 0577 pass; not-self-signed, expired, unrelated key and fabricated self-report files pass;
  its oracle passes 5/6 on host OpenSSL 3.6.5 because of the `CN = ` format, so an "oracle passes" control needs the
  version limit stated). Refused: `fix-git`, `cancel-async-tasks` (0 quote-eligible instruction lines), `sanitize-git-repo`
  (pinned upstream commit).
```

## 6. Limits

- Kills in §2 are result differences on my fixtures, not attributed kills; A18, L08, L17 differ only in summary text; the
  counter must classify each (§2.7). The fixture sets are mine (an author's set again): non-author mutants are the point of
  §2.5, and the same asymmetry will apply to §2.3/§2.4.
- The R5 drafts and `order_check.py` are unlanded round-39 drafts at the digests above; mutant counts for them can move.
- `A10/A16/L12/L13/L19/L20/O02/O05/O07/O10/O11` are classified equivalent or unreachable by reasoning plus one fixture run each
  where noted; none was proven.
- TB2 probes ran on host git/bash/python 3.14, sqlite 3.54.0, OpenSSL 3.6.5 — not the task images (not pulled). The root-like openssl
  run used bwrap capabilities, not a container root.
- Prior art for the destructive-read trap and for re-run stability rests on `web_search` snippets (LLM-synthesised, unopened);
  `gh` issue search returned 0 for `openssl` and `wal`.
- `constraints-scheduling` was read (lines 1–60) and not executed; the `fix-git`/`cancel-async-tasks` quote counts are line-scan
  measurements, not entry drafts. `tip_receipts` and the direction check were not re-run.

## 7. Evidence ledger

| claim | command | output |
|---|---|---|
| tip, clean baseline | `git -C $S/lane rev-parse HEAD` | `750473847af9c7a461487ba3a589b5519fac5ed8` |
| anchor mutants | `python3 h_anchor.py` | `MUTANTS n=26 killed_by_tip=2 killed_by_tip+r38_fixtures=7 killed_by_all_fixtures=23` (`out_anchor2.txt`) |
| anchor R5 draft | `TOOL=…/R39AnchorUnion/anchor_digest_check.py TAG=_r5 python3 h_anchor.py` | `n=24 … killed_by_all_fixtures=21`; `X10 rc=1 classes=['capture-unanchored']` (`out_anchor_r5.txt`) |
| ledger mutants | `python3 h_ledger.py` | `MUTANTS n=20 killed_by_tip=1 killed_by_tip+d4=5 killed_by_all=15` (`out_ledger.txt`) |
| ledger R5 draft | `TOOL=…/R39LedgerProvenance/ledger_tip.py TAG=_r5 python3 h_ledger.py` | `n=18 killed_by_tip=2 killed_by_tip+d4=3 killed_by_all=13` (`out_ledger_r5.txt`) |
| stale `master`, control mode | tool `--lane` vs draft `--lane` in a clone with `master` = `HEAD~6` | tool rc 0 `mismatches=0`, draft rc 2 `REFUSE stale pin ref …` |
| order-gate mutants | `calibrate.py --gate order-mutants/Onn.py --work …` ×14 | 4 killed, 9 survive, O08 needle absent (`order-mutants/`) |
| TB2 pin | `git rev-parse origin/HEAD`; `git checkout 2fd12b88` | `2fd12b88aafdd04a52c298e3940bcb189f9766d6` |
| census | `ast` + `find_spec` scan of 89 graders | 58 callable, 30 missing import, 7 fixture/mark (`tb2_callable.json`) |
| db-wal controls | `python3 dbwal/run.py` (×2, `cmp`) | table in §3.2, byte-equal |
| db-wal trap | `sqlite3 /app/main.db "select count(*) from items;"` rw vs `file:…?mode=ro` in bwrap | rw: 5, WAL removed; ro: WAL intact, sha256 `68753bdc…` unchanged |
| openssl probe | `python3 ossl/run.py dry`; `python3 ossl/run.py run` ×2 | `cases=26 predicted_pass=15 predicted_fail=11`; `observed_pass=14 observed_fail=12 mismatches=1`, `cmp` equal |
| openssl root-like | `ossl/run_root.py` (`--uid 0 --cap-add ALL`) | `key-mode-000 observed_fail=-`; `mismatches=2` |
| openssl oracle | `bash /solution/solve.sh` then grader in bwrap | `test_python_verification_script FAIL … does not display Common Name`; 5/6 pass |
| polyglot idempotence | `bwrap … python poly/h.py` | `GRADE 1 PASS`, `GRADE 2 FAIL … ['main.py.c', 'cmain']` |
| issue search | `gh api -X GET search/issues -f q='repo:harbor-framework/terminal-bench-2 <term>'` | `total_count` 0 for `openssl-selfsigned-cert`, `db-wal-recovery`, `openssl`, `wal` |

Tools: none installed; `bwrap`, `gh`, `git`, `sqlite3`, `openssl`, `python3` were present. No pacman use; no `uv` installs
(pytest not needed: graders called directly).

## 8. Out of scope

No lane file, claim, counter, probe, spec, capture or corpus path written; no `git add/commit` in the lane; no subagent; no
scratch outside `/fast/scratch/hyaku/kengaku-r39/R39PlanNext/`; the source repo `shokuknow` untouched; wave-1 seats' drafts read
and run from scratch copies only.

## 9. Scratch

`rm -rf /fast/scratch/hyaku/kengaku-r39/R39PlanNext` run after the last receipt copy (verified below).

VERDICT: plan40-drafted
