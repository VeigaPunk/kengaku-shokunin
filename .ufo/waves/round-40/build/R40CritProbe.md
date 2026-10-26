# R40CritProbe — attack on `plans/db_wal_probe.py` + `corpus/evidence/round40/db-wal-probe.txt`

Seat: critic (round 40, wave 1, C2). Lane read-only; nothing edited. Scratch
`/fast/scratch/hyaku/kengaku-r40/R40CritProbe` (clone of lane HEAD `3077adbc`, removed on exit).
Host: sqlite3 3.54.0, python 3.14.8, bubblewrap 0.13.1 — the probe's own stated stand-ins.

Method: (a) read the frozen claims, probe, dry table, receipt, counter V7, all eight captures;
(b) re-ran the probe twice and diffed against the committed receipt; re-ran `--dry` and `--stage-check`;
(c) re-derived the ground truth from the two captured files by hand; (d) re-ran 15 recipes in the probe's
own bwrap sandbox with a harness that dumps the `/app` end state (file sizes, sha256, WAL magic) **before**
importing the grader, plus three cases the frozen table does not contain; (e) recomputed V7's labels from the
frozen table and the receipt, then recomputed them under nine counterfactual tag edits.

Receipts: `R40CritProbe/{run1.txt,dry.txt,stage.txt,endstates.txt,wal-fate.txt}` in this directory.

---

## 1. What holds (checked, not assumed)

| check | command | output |
|---|---|---|
| receipt reproducible, byte-equal to committed | `python3 plans/db_wal_probe.py --lane . --work "$S/w1" > run1.txt` | `diff` empty; sha256 `c74c6b91c8c49b17…` for run1, run2 **and** `corpus/evidence/round40/db-wal-probe.txt` |
| run time | as above, `time` | `real 0m1.872s` |
| dry table is the probe's own output | `python3 plans/db_wal_probe.py --lane "$L" --dry` | `DRY-BYTE-EQUAL` to `db-wal-dry-cases-freeze.txt` |
| stage-check claim in the claims file | `python3 plans/db_wal_probe.py --lane . --stage-check --work "$S/w3"` | `stagecheck cases=28 failed=0`, byte-equal to `.ufo/waves/round-40/claims/c2-stage-check.txt` |
| probe is the frozen instrument | `sha256sum plans/db_wal_probe.py` | `69af65dfe4e2ecab…` = `frozen_instruments` in `plans/pkg-spec-r40.json` |
| pins match the capture sums | read `PINS` vs `SHA256SUMS` | all four digests equal |
| ground truth in the docstring | XOR 0x42 the captured WAL, read `items` | base alone = 5 rows `100..500`; WAL applied = 11 rows `apple…mango`, values `150,250,300,…,1100`; decrypted header `377f0682` — exactly the docstring's table (`db_wal_probe.py:25-28`) |
| tag line numbers | `instruction.md` 1..14 vs `TAGS` (`db_wal_probe.py:77-82`) | `7,8,9,12,13,13` all correct (`7` "Fix the WAL file…", `13` "sorted by id. You should recover all 11 records total") |
| predictions | receipt | `cases=28 observed_pass=8 observed_fail=20 mismatches=0`; the 7 pilot rows match `.ufo/waves/round-39/build/R39PlanNext/dbwal/run1.txt` line for line |
| headline "22 of 33 cells" | `test_outputs.py:57-58` (ids), `:64-67` (values 1-2), `:70-80` (names 3-11) | 11+2+9 = 22 pinned; names of 1-2 and values of 3-11 unpinned — witnessed by `literals-never-open-db` (9 value cells wrong, passes) and `literals-names-1-2-wrong` (2 name cells wrong, passes) |

The tag sets are internally consistent **under one rule**: `extract-all` = the recovered data's coverage and
values differ from the database's data; `record-format` = JSON types/keys differ. The decision pair is
`truth-bool-value-id5` (`true` ≠ the value 500 → both tags) vs `truth-value-string-id4` (`"400"` is the value 400 in a
string → `record-format` only). Under that rule every one of the 28 tag sets checks out, including
`truth-id3-wrong` (301 ≠ 300) and `truth-ids-as-{strings,floats}` (right numbers, wrong JSON type). **That rule is
not written down anywhere** — see D7.

Case texts vs recipes: 12 of the 28 frozen cases were executed here and inspected in `/app` (`untouched`,
`base-only-ro`, `plain-read-then-solve`, `xor-wrong-key`, `decrypt-then-extract`, `decrypt-checkpoint-truncate`,
`decrypt-in-place-no-json`, `oracle-solve-sh`, `literals-never-open-db`, `truth-extra-field`, `truth-ids-as-strings`,
`truth-value-string-id4`); the other 16 were checked by reading each recipe against `MK_PY` and the byte-equal
receipt's per-test letters. No mismatch beyond D5/D6 was found: `base-only-ro` really leaves the encrypted WAL
intact (16512 B, sha `68753bdce26196a5`), `decrypt-in-place-no-json` really leaves a decrypted WAL
(`a00cfbf891cb3615`, head `377f0682`) with no JSON, and from `MK_PY` source `truth-dup-id10-no-id11` writes 11
records with a duplicated id 10 while `empty-app` seeds nothing.

---

## 2. Defects

Severity: **H** = changes what the entry may claim; **M** = wrong or misleading case text / missing witness;
**L** = bookkeeping that cannot move a label.

### D1 (H) `regrade=` is not a re-run; `differ=0` is near-tautological
The docstring says the harness "grades the SAME end state a second time, without rebuilding it"
(`db_wal_probe.py:21-23`), and the claims call it "graded twice on the same end state … proposal 3's stability
rider" (`plans/round-40-claims.md:79`, `:106`). The implementation is one `exec_module` followed by
`for tag in ("TEST", "REGRADE"):` (`db_wal_probe.py:245`) — two calls of the same seven functions in the same
interpreter, over the same file, with no second process and no second sandbox. Since all seven tests only
`open("/app/recovered.json")` (`test_outputs.py:94` etc.), `regrade cases=28 differ=0` cannot fail for any
deterministic end state. It can only catch an in-sandbox leftover writer. **Correction (entry text):** describe the
column as a second read in the same run, never as re-run stability; a real rider grades the same end state in a
second fresh sandbox. No number in the receipt is wrong.

### D2 (H) `fix-wal` = `partly` is confounded; no case's failure is attributable to it
V7 derives `fix-wal` `partly` from 23 tagged cases of which 5 pass. But nothing in the grader reads
`/app/main.db-wal`: `test_wal_was_decrypted` opens `/app/recovered.json` (`test_outputs.py:92-98`). Measured end
states show the tag is not observable at all:

| case | `/app/main.db-wal` after the recipe | verdict |
|---|---|---|
| `untouched`, `base-only-ro`, `literals-*`, `truth-*` (hand-typed) | 16512 B, sha `68753bdce26196a5`, head `753d44c0` (still encrypted) | 5 of these **pass** |
| `decrypt-then-extract`, `decrypt-checkpoint-truncate`, `oracle-solve-sh` | **0 B** (checkpointed into `main.db`, sha `682055f65aadf683`) | **pass** |
| `plain-read-then-solve` | 0 B (+ 0 B `main.db-wal.decrypted`) | fail |
| `xor-wrong-key` | absent | fail |
| `decrypt-in-place-no-json` (only genuinely repaired WAL) | 16512 B, sha `a00cfbf891cb3615`, head `377f0682` | fail |

So every failing fix-wal case fails on a different tag (`extract-all`, `record-format`, `json-at-path`), and the
oracle ends in the same WAL shape as the destructive-read case. **Correction:** the entry keeps the V7-mandated
label but must state that `partly` here is an artefact of co-tagging, that zero of the seven tests observe the WAL,
and cite `literals-never-open-db` as the proof. It must not read `partly` as "partially enforced". This is also
where the entry's headline ("Fix the WAL file is never checked") and the derived label visibly disagree — say so
rather than pick one.

### D3 (M) No passing case ends with a repaired WAL file
The only repaired-WAL end state in the frozen table is `decrypt-in-place-no-json`, and it fails (no JSON). A pure
"decrypt in place, read read-only" pipeline is missing; I ran it (not a frozen case):

`run("xor-correct-key-RO", DECRYPT(0x42) + EXTRACT(mode=ro))` → `main.db-wal` 16512 B, sha `a00cfbf891cb3615`,
head `377f0682`; `recovered.json` 11 rows; `TEST …` 7 × P. This is the only shape that distinguishes "the WAL file
was fixed" from "the WAL was checkpointed away", and the probe has no such witness in either direction.

### D4 (M) No correct hand-typed export in the table; the grader passes with no database at all
`mk("truth")` is reachable code and no case uses it at the default path (`truth-wrong-path` uses it at
`/app/out/recovered.json`; every other `truth-*` case perturbs it). I ran it:

- `truth` at `/app/recovered.json`: `RECIPE rc=0`; `main.db` 8192 B sha `68cb288eb29e76d8` and `main.db-wal`
  16512 B sha `68753bdce26196a5` — both **bit-identical to the seeded captures**; `recovered.json` sha
  `dd04f318daf77655`; `TEST` 7 × P.
- `rm -f /app/main.db /app/main.db-wal` then `mk truth`: `/app` holds only `recovered.json`; `TEST` 7 × P.

The second one is the strongest available statement of the edge class ("the graded artefact's source of truth is a
main database plus an encrypted WAL"): neither file is required to exist. The frozen table supports the weaker
"hand-typed JSON that never opens the database passes 7/7" only via `literals-never-open-db`, which passes **with
9 of 11 values wrong (0)** — that is a stronger, not weaker, witness, but the entry must describe it accurately
rather than as a correct export.

### D5 (M) `xor-wrong-key` text is wrong about the end state and the case is confounded
Case text (`db_wal_probe.py:183`): "XOR with the wrong single-byte key 0x43: the WAL magic stays invalid, SQLite
ignores it, 5 base rows". Measured: the wrong-key WAL is `367e0783`, and the case's `EXTRACT` uses the read-write
URI, so SQLite **discards** it — after the recipe there is no `/app/main.db-wal` at all. Under a read-only open the
wrong-key WAL survives intact (16512 B, sha `8a46e91ed1cca62f`, head `367e0783`) and still gives 5 rows (my
`xor-wrong-key-RO-isolation` run). So the 5-row result is caused by the key **and** by the destructive read, and
"ignores it" describes the read, not the end state. **Correction:** "discards it"; and the probe would need the
read-only variant to isolate the key (wave-2 or a named limit).

### D6 (L) `plain-read-then-solve` end state is not "WAL gone"
Case text (`db_wal_probe.py:179-180`) — "it deletes the encrypted WAL … nothing left to decrypt" — is true of the
encrypted file: a plain read-write `sqlite3 main.db` deletes the 16,512-byte WAL (host check: `enc/rw after:
main.db:8192` only). But the graded end state is `main.db-wal` **0 B** plus `main.db-wal.decrypted` 0 B, because
`solve.sh` line 10 opens `mode=ro` and recreates an empty WAL, and `decrypt_wal.py` then XORs 0 bytes. The entry
should say "the encrypted WAL is destroyed and a 0-byte WAL is left", not that no WAL remains.

### D7 (M) The `violates=` rule is stated as an end-state rule but `extract-all` is provenance
`db_wal_probe.py:74-75`: "A case violates a tag when its end state does not do what the instruction asks under that
tag, whatever the grader says." For `fix-wal` the end state decides it (the WAL file is observable, D2). For
`extract-all` nothing in an end state distinguishes "extracted" from "typed": my exact `truth` case ends with a
byte-identical encrypted WAL and a correct JSON and is indistinguishable from `decrypt-then-extract`, yet the tag
sets require it to violate `extract-all` (it did not extract) while `truth-extra-field` also did not extract and is
not tagged. So the operative rule is content-based ("data ≠ the database's data"), not end-state-based, and it is
never written down. The pair that flips meaning is `truth-bool-value-id5` vs `truth-value-string-id4` (§1).
**Correction (entry text):** state the rule explicitly; a hand-typed but correct export violates `fix-wal`
(observable: WAL unfixed) and `extract-all` (provenance, not observable), and the grader cannot see either.

### D8 (L) Uneven tag policy, no label effect
`empty-app` omits `fix-wal` while `untouched` carries it, though neither end state has a readable WAL (absent vs
encrypted). `truth-trailing-garbage` carries `json-at-path` but not `record-format`, while
`truth-wrapped-object` carries `record-format` but not `json-at-path` — root-cause-only in one place, "all violated
requirements" in another (`literals-*` carry `fix-wal` **and** `extract-all`). Additions here change no label
(verified below).

---

## 3. Requirement-map labels (V7 `derive`, recomputed)

Derived from every receipt case whose `violates=` carries the tag — `enforced` all fail, `unenforced` all pass,
`partly` mixed:

| tag | line | label | tagged cases | passing violators |
|---|---|---|---|---|
| `fix-wal` | `instruction.md:7` | **partly** | 23 | `literals-names-1-2-wrong`, `literals-never-open-db`, `truth-bool-value-id5`, `truth-extra-field`, `truth-value-id3-wrong` |
| `extract-all` | `instruction.md:8` | **partly** | 15 | `literals-names-1-2-wrong`, `literals-never-open-db`, `truth-bool-value-id5`, `truth-value-id3-wrong` |
| `json-at-path` | `instruction.md:9` | **enforced** | 5 | — |
| `record-format` | `instruction.md:12` | **partly** | 8 | `truth-bool-value-id5`, `truth-extra-field` |
| `sorted-by-id` | `instruction.md:13` | **enforced** | 1 | — |
| `eleven-records` | `instruction.md:13` | **enforced** | 10 | — |

Label changes under contestable tag edits (each edit recomputed against the frozen receipt):

| edit | label change |
|---|---|
| add `extract-all` to `truth-value-string-id4`, `truth-ids-as-strings`, `truth-ids-as-floats`, `truth-value-float-id1` | **none** |
| add `extract-all` to all 16 hand-typed cases (provenance reading) | **none** |
| add `fix-wal` to `empty-app` | **none** |
| add `json-at-path` to `truth-wrapped-object` | **none** |
| add `record-format` to `truth-trailing-garbage` | **none** |
| drop `extract-all` from `truth-bool-value-id5` | **none** |
| drop `fix-wal` from the passing violators | `fix-wal`: partly → **enforced** |
| drop `record-format` from `truth-extra-field` **and** `truth-bool-value-id5` | `record-format`: partly → **enforced** |

Exactly **two** labels are tag-fragile, and both flips are indefensible: they would assert enforcement where the
measured evidence is a passing case that violates the requirement. Everything else is robust. Note also that
`sorted-by-id`'s `enforced` rests on a single case (`truth-reversed-order`) whose only co-tag is `fix-wal` — legal
under V7, but the entry should name the single witness.

---

## 4. What the entry must not claim (given the freeze)

1. Do not call `regrade cases=28 differ=0` re-run stability (D1).
2. Do not present `fix-wal`'s `partly` as partial enforcement; no test reads the WAL (D2).
3. Do not present `oracle-solve-sh` or `decrypt-then-extract` as ending with a fixed WAL — both end with a 0-byte
   WAL and a checkpointed `main.db` (sha `682055f6…`); only `main.db-wal.decrypted` (oracle) holds the decrypted
   bytes (D3).
4. Do not describe the passing hand-typed cases as correct exports: `literals-never-open-db` passes with values
   `[150,250,0,0,0,0,0,0,0,0,0]` (D4).
5. Do not claim a case isolates the wrong key: its WAL is discarded by the read-write extraction (D5).
6. Do not state the 5 base rows of `plain-read-then-solve` as reaching an empty `/app` WAL state: a 0-byte
   `main.db-wal` remains (D6).

Feasible improvements, all outside the frozen table: name the proposed wave-2 cases (`truth` at the default path,
read-only decrypt+extract, `rm` both files + `truth`, wrong-key read-only) and the tag rule (D7) in the entry's
limits/`## Requirement map` prose.

## Limits of this review

Labels were recomputed with the counter's own `derive`; V7 was not executed because the entry does not exist yet
(`corpus/knowledge/tb2-db-wal-recovery-grader.md` absent at review time) — the numbers above are the values V7
will demand. Host sqlite3 3.54.0/python 3.14.8 stand in for the image; the destructive-delete behaviour was
measured only on 3.54.0. Nothing in the frozen set was edited or re-pinned.

VERDICT: probe-attack-8-defects-labels-change-2
