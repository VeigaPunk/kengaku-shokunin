# ReviewerC185 — independent derivation and replay attack on R85-C1

2026-11-04. Seat ReviewerC185, round 85 wave 1. Read-only attack seat.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Frozen contract read in full first: `plans/round-85-claims.md` at freeze `1a45aeb5e8706b1518ba58fd0fe882df1631e2a0`.

**Revision note.** The lane tip moved while this review ran:
`d4253aa0` (the tip when I started) → `dc02d818` → `f8884277` → `b1e57097` (the tip at the end).
All committed-state findings are measured at a pinned revision and labelled with it. The worktree is
still being written by sibling seats, so every command below names the revision or copies the blob.

Frozen files untouched by the round: `git diff --stat 1a45aeb5 master -- plans/round-85-claims.md
plans/round85-cases.json plans/round85-defects.json` is empty. No frozen element was edited by me.

---

## 1. Independent derivation (written before the table and the probe were read)

File: `derived.txt` in this directory. Written from
`corpus/evidence/round52/graders/sqlite-db-truncate/tests/test_outputs.py` only (sha256
`8f5bc11018687d8c5894ebf1b4ec6fad004828e5ce442d3cc04d925ef53ef881`, matching the freeze pin).

The grader: `soln` is an eight-element list; `soln_tuples = {(word, value)}`; `data_tuples` the same
from `/app/recover.json`; `score = len(soln_tuples & data_tuples)`; `assert score > 6`.

Semantics relied on:

- **S1** the intersection counts distinct `soln` tuples and cannot exceed 8;
- **S2** `json.load` maps fractional literals to `float` and bare integers to `int`;
- **S3** `10 == 10.0` and `hash(10) == hash(10.0)`, so integral JSON ints match float solution values;
  non-integral `99.99` and `0.5` accept only the exact float;
- **S4** `"10.0" == 10.0` is `False`, so string values never match;
- **S5** set construction deduplicates 16 duplicated rows to 8;
- **S6** extra non-solution rows cannot change the intersection;
- **S7** `> 6` is strict: 7 passes, 6 raises `AssertionError`.

Derived vector, before seeing the frozen table:

| id | derived | frozen table | probe observed |
|---|---|---|---|
| exact8 | 8/P | 8/P | 8/P |
| seven | 7/P | 7/P | 7/P |
| six | 6/F | 6/F | 6/F |
| empty | 0/F | 0/F | 0/F |
| extras | 8/P | 8/P | 8/P |
| duplicates | 8/P | 8/P | 8/P |
| string-values | 0/F | 0/F | 0/F |
| int-values | 6/F | 6/F | 6/F |

**8/8 cases and 16/16 legs agree; no derivation disagreement.**

The frozen table's data confirms the discriminating shapes: `duplicates` is 16 rows (8 distinct),
`int-values` carries bare JSON ints `10,25,42,50,75,99` against the six integral solution values,
`string-values` carries `"10.0"`… strings. `plans/round85-cases.json` sha256
`bd98794b9d35168ccb296ad9176cf45b0b421cf961515935a814eadc40d49114`, identical at the freeze
commit and at master, and equal to the probe's own `FROZEN_TABLE_SHA`.

---

## 2. Probe replay

```
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
python3 plans/round85_sqlite_truncate_probe.py --lane . \
  --work /fast/scratch/hyaku/kengaku-r85/ReviewerC185/probe
```

```
MEMBER sqlite-db-truncate
SUBJECT_CAPTURE corpus/evidence/round52/graders/sqlite-db-truncate/tests/test_outputs.py
SUBJECT_SHA 8f5bc11018687d8c5894ebf1b4ec6fad004828e5ce442d3cc04d925ef53ef881
CASE_TABLE_SHA bd98794b9d35168ccb296ad9176cf45b0b421cf961515935a814eadc40d49114
TOOL plans/round85_sqlite_truncate_probe.py
TOOL_SHA d00868acbfe8c398a4703860b39c101734799aeb8cc5de8f2f3d3e05ccb0582f
HOST_PYTHON Python 3.14.8
HOST_OPENSSL OpenSSL 3.6.5 29 Sep 2026 (Library: OpenSSL 3.6.5 29 Sep 2026)
LANE_TIP d4253aa0ebb8c3f17e3bd0711c2c588dcec9fd57
WORKTREE dirty
...
CASE exact8 predicted=8/P observed=8/P
...
CASE int-values predicted=6/F observed=6/F
cases=8 legs=16 mismatches=0
PREDICATE R85-PROBE pass
```

(`WORKTREE dirty` is the sibling wave in flight, not the probe's input.) The probe was run from its
own `--lane .` copy on the then-tip; at the final tip the same table and vectors hold (see §3).

---

## 3. Counter runs

### 3.1 After-state, measured revision = master

Working-tree counter, tip `d4253aa0`:

```
TARGET members=1 cases=8 legs=16 mismatches=0 located=1 executed=1 defects=0
PREDICATE R85-C1 pass
EXIT=0
```

Committed counter blob, extracted from git and run against the same lane (provenance check; the
worktree instrument differs from committed blobs while siblings edit it):

- `plans/round85_c1_replay.py` at `d4253aa0`, sha256 `9f1e5944…` → same PASS, exit 0;
- `plans/round85_c1_replay.py` at `b1e57097`, sha256 `095d5ed7…` → same PASS, exit 0.

So the pass at the frozen target line is reproduced by the **committed** instrument, not only by an
uncommitted working-tree copy.

### 3.2 Before-state, BASE `0de45354d7aff18e4a23a348ec13de3a1f707a44`

`--rev BASE` from the git lane (both the `d4253aa0` and the `b1e57097` committed counter blobs):

```
DEFECT TABLE-MISSING plans/round85-cases.json@rev 0de45354d7af
DEFECT TOOL-MISSING plans/round85_sqlite_truncate_probe.py
DEFECT LEDGER-UNEXECUTED status=unexecuted
DEFECT LEDGER-ROUND None
DEFECT LEDGER-RECEIPT None
DEFECT LEDGER-SUBJECT None
DEFECT LEDGER-VERDICT None
DEFECT RECEIPT-MISSING corpus/evidence/round85/sqlite-db-truncate-probe.txt
TARGET members=1 cases=0 legs=0 mismatches=0 located=0 executed=0 defects=8
PREDICATE R85-C1 fail
EXIT=1
```

This is exactly the frozen before-state (`defects>=1`, exit 1).

Bare extraction, as this seat's item prescribes:

```
git -C …/kengaku-shokunin archive 0de45354… | tar -x -C <scratch>/baseextract
python3 plans/round85_c1_replay.py --lane <scratch>/baseextract --work <scratch>
DEFECT SETUP frozen-input-missing plans/round85-cases.json (no git at …/baseextract)
PREDICATE R85-C1 fail
EXIT=2
```

This is R84-V2's fail-closed path, not a scoring run. See F3 for the wording consequence.

### 3.3 Controls (frozen set), all four

```
CONTROL do-nothing target_reached=False defects=8 codes=LEDGER-RECEIPT,LEDGER-ROUND,LEDGER-SUBJECT,LEDGER-UNEXECUTED,LEDGER-VERDICT,RECEIPT-MISSING,TABLE-MISSING,TOOL-MISSING
CONTROL ledger-only target_reached=False defects=1 codes=RECEIPT-MISSING
CONTROL fabricated-observations target_reached=False defects=2 codes=REPRODUCE-MISMATCH,VECTOR-MISMATCH
CONTROL forged-receipt target_reached=False defects=1 codes=REPRODUCE-MISMATCH
```

All four reject, each with the defect the frozen control set names. The forged-correct-vector
receipt is killed by the unconditional REPRODUCE leg (R84-V3's repair holds).

### 3.4 Counting figures

Population ledger (`plans/grader-population-ledger.json`), BASE → master:

- executed 28 → 29, unexecuted 60 → 59 — **matches the freeze**.
- `sqlite-db-truncate`: `unexecuted` (BASE) → `executed`, round 85, receipt path exact (master) —
  matches the C1 predicate.

Class figure does **not** match: see F1.

---

## 4. Receipt audit

### 4.1 Blob equality with the commit (item step 4)

```
sha256sum corpus/evidence/round85/sqlite-db-truncate-probe.txt              = d3cc4cd180f618…
git cat-file -p ce5b9ef8:corpus/evidence/round85/sqlite-db-truncate-probe.txt | sha256sum = d3cc4cd180f618…
diff <(git cat-file -p ce5b9ef8:…) corpus/evidence/round85/sqlite-db-truncate-probe.txt      → IDENTICAL
```

At the later tip the receipt was re-minted (`f8884277`); its blob at master is also byte-identical
to the worktree copy (`diff` empty), tracked (`git ls-files --error-unmatch` resolves).

### 4.2 Stamp completeness and TOOL_SHA binding

At master `b1e57097` the receipt carries all twelve required fields (MEMBER, SUBJECT_CAPTURE,
SUBJECT_SHA, CASE_TABLE_SHA, TOOL, TOOL_SHA, HOST_PYTHON, HOST_OPENSSL, LANE_TIP, WORKTREE, COMMAND,
EXIT) plus the `# tb2 sqlite-db-truncate grader probe` header line and an OBSERVATIONS block.

- `TOOL_SHA 04d5fc1a78e6bab178005c44bd722bcce1bb5d234b8178aad3b7aed9933d3538` equals
  `git show dc02d818:plans/round85_sqlite_truncate_probe.py | sha256sum` (the receipt's own
  `LANE_TIP`) and equals the probe at master and the counter's `TRUSTED_TOOL_SHA`. **Binding holds.**
- `SUBJECT_SHA 8f5bc110…` equals the capture file and the freeze pin.
- `CASE_TABLE_SHA bd98794b…` equals the frozen table and the probe's `FROZEN_TABLE_SHA`.
- `LANE_TIP dc02d818` is an ancestor of master; `EXIT 0`; `COMMAND` names the probe with
  `--lane .` and a `--work` directory (reconstructed argv, never executed from the receipt).
- The earlier receipt (at `ce5b9ef8`) bound `TOOL_SHA d00868ac…`, which was the probe at its own
  `LANE_TIP 99a7cb3b`; that binding also held when checked.

The 16 observation legs in both receipts are the eight derived pairs above.

---

## 5. Predicate sentence identity (item step 3)

Frozen claim, `plans/round-85-claims.md:15-19`:

> Predicate R85-C1: the base-unexecuted `sqlite-db-truncate` member has exactly one located,
> host-pinned receipt `corpus/evidence/round85/sqlite-db-truncate-probe.txt` whose frozen eight-case
> table (`plans/round85-cases.json`) reproduces the captured grader's single test function with zero
> mismatches on a two-leg vector (leg `score`: the set-intersection cardinality; leg `verdict`: the
> grader's `score > 6` pass/fail), and the population ledger marks that receipt executed in round 85.

Counter label (both committed blobs and the worktree):

> `PREDICATE R85-C1 pass`

Probe/receipt label (`plans/round-85-claims.md:53`, and the receipt's last observation line):

> `PREDICATE R85-PROBE pass`

The claim id and the counter's label are the same claim. The receipt's own label is `R85-PROBE` by
the claim's design — and that divergence from the lane's older gate vocabulary is finding F2.

---

## Findings

### F1 — MEDIUM — the frozen class figure is wrong under the lane's own class accounting

`plans/round-85-claims.md:60`:

> `serialization-schema` class executed 0 of 9 → 1 of 9.

`corpus/lessons/round-85.md:100` repeats it:

> the `serialization-schema` class executes 0 of its 9 members → 1 of 9.

The lane's canonical class accounting — the ledger's `classes` field, the round-79 population gate,
and `SKILL.md`'s derived class table — says the class has **10** members and **1** already-executed
member at BASE:

```
$ python3 plans/round79_c1_population_ledger.py --lane . --rev 0de45354… | grep 'CLASS serialization-schema'
CLASS serialization-schema k=1 n=10 cell=executed 1 of 10

$ … --rev master
CLASS serialization-schema k=2 n=10 cell=executed 2 of 10 (round 85 adds `sqlite-db-truncate` …)

$ git show master:SKILL.md | sed -n '84p'
| serialization-schema | 10 | executed 2 of 10 (round 85 adds `sqlite-db-truncate` to round 40's `db-wal-recovery`) | …
```

BASE ledger row proving the existing executed member: `db-wal-recovery` — `executed`,
`classes: [file-artifact, serialization-schema]` (`git show 0de45354:plans/grader-population-ledger.json`).

So the true movement is **1 of 10 → 2 of 10**; the claim states 0 of 9 → 1 of 9, wrong on both the
numerator and the denominator. If the author meant "of the nine *remaining* members", that reading
collides with the gate's `executed k of n` vocabulary and with the `SKILL.md` cell the same round
updated. The R85-C1 pass predicate does not reference this figure, so the claim still passes; the
coverage delta as stated overstates the delta by one member and one executed member. The claim is
frozen and must not be edited — the correction belongs in the round report.

### F2 — HIGH (lane integrity) — the ledger's own gate fails at the committed tip because of the C1 ledger row's `verdict`

At BASE the population gate is green; at the committed tip `b1e57097` it is red:

```
$ python3 plans/round79_c1_population_ledger.py --lane . --rev 0de45354… 
DEFECTS n=0
PREDICATE R79-C1 pass

$ python3 plans/round79_c1_population_ledger.py --lane . --rev master
DEFECT VERDICT-MISMATCH sqlite-db-truncate ledger=predicate receipt=cases
DEFECTS n=1
PREDICATE R79-C1 fail
```

Cause. The gate's frozen verdict vocabulary (`plans/round79_c1_population_ledger.py:37-40`) is:

> `^PREDICATE R<n>-C<m> pass` (verdict `predicate`), else any `^VECTOR ` line (verdict `vectors`),
> else any `^CASE ` or `^case=` line (verdict `cases`).

The receipt's line is `PREDICATE R85-PROBE pass`, which does not match `R<n>-C<m>`; the gate falls
through to the `CASE` lines and classifies the receipt `cases`. The ledger row
(`git show master:plans/grader-population-ledger.json`, key `members.sqlite-db-truncate`) says
`"verdict": "predicate"`. `check()` then raises `VERDICT-MISMATCH` at
`plans/round79_c1_population_ledger.py:248`.

The collision is structural in the committed instruments: the R85 counter hard-requires
`row.get("verdict") == "predicate"` (`plans/round85_c1_replay.py:216` at master), while the R79 gate
derives `cases` from the same receipt, so **no single ledger value satisfies both committed
counters**. Demonstrated: a scratch fixture carrying `verdict: "cases"` passed the worktree counter
but would be the only gate-consistent value; carrying `verdict: "predicate"` passes the committed
R85 counter and fails the gate.

State at hand-off. The worktree carries an uncommitted repair: the counter now tests
`row.get("verdict") != "cases"`, and the worktree ledger row is already `"verdict": "cases"`. In
worktree mode both gates are green:

```
$ python3 plans/round85_c1_replay.py --lane . --work …          → PREDICATE R85-C1 pass, EXIT=0
$ python3 plans/round79_c1_population_ledger.py --lane . --rev worktree → DEFECTS n=0, PREDICATE R79-C1 pass
```

That repair must be **committed** before the round closes; as measured at committed master the lane
ships a base-green gate turned red by this round's C1 row. It is not covered by any frozen R85
sentence (the C1 predicate only requires the row to mark the receipt executed, which it does), so it
is a lane-integrity regression, not a C1 predicate failure.

### F3 — LOW — the frozen before-state's `exit 1` is invocation-dependent

`plans/round-85-claims.md:58-59` states BASE as `… defects>=1`, `PREDICATE R85-C1 fail`, exit 1. That
holds for the `--rev BASE` invocation (verified with both committed counter blobs, §3.2, exit 1). It
does not hold when the counter is pointed at a bare BASE extraction — the form this seat's item
prescribes — which returns:

```
DEFECT SETUP frozen-input-missing plans/round85-cases.json (no git at …/baseextract)
PREDICATE R85-C1 fail
EXIT=2
```

This is the deliberate R84-V2 fail-closed branch (`ensure_freeze` in `plans/round85_c1_replay.py`),
not a defect in behaviour; the defect is that the frozen before-state sentence does not name the
invocation it depends on, so two honest readings produce different exit codes. Low severity: the
scored vector is unaffected.

---

## Residual risk and verification gaps

- R79-C1 is the ledger's stated gate (`plans/grader-population-ledger.json` `why`, "Gated by
  plans/round79_c1_population_ledger.py (R79-C1)") but is not one of the frozen R85 checks; F2 is
  reported as changed behaviour of the landed diff, not as a frozen-predicate failure.
- The lane tip moved four times during this review; commits after `b1e57097` may close F2. Re-run the
  two commands in F2 at the close tip before accepting the round.
- The probe's `reference_score` (host-side `ast.literal_eval` + set intersection) is a table
  validator, not the observed score leg; it shares Python set semantics with the sandbox harness, so
  it is not an independent oracle for the semantics themselves. It cannot turn a wrong table green.
- No network fetch, no tool install or upgrade was performed for this seat (nothing installed; no
  `pacman`, `uv`, `npx` or binary channel touched). Scratch was used only under
  `/fast/scratch/hyaku/kengaku-r85/ReviewerC185/`.
- Frosted-element complaint is confined to F1 (wrong class arithmetic); the case table, defect list,
  control set, kill rule and target are correct as frozen.
