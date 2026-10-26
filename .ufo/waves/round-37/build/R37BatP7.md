# R37BatP7 — C1 battery module `p7` (gate clause P7 provenance, mutants M28–M33)

Seat: executor, kengaku round 37 wave 1. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Read-only on the lane: no lane file, index or digest was touched. Frozen inputs read first:
`plans/round-37-claims.md`, `plans/round37_c1_verify.py`, `plans/pkg_gate.py` (digest verified
`ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`), `plans/pkg-spec-r35.json`,
`corpus/knowledge/tb2-protein-assembly-grader.md`, `.ufo/waves/round-37/claims/example_battery/ex_p3_words.py`.

## Product

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-37/build/R37BatP7/battery/p7.py`
— six single-defect fixtures, one per frozen mutant, stdlib only (AST scan: zero `Import`/`ImportFrom`
nodes). Every builder starts from `ctx.genuine_package(d)`, edits only the entry
`corpus/knowledge/tb2-protein-assembly-grader.md`, stages with `ctx.git_add(d)` (no commit), and returns
`["package", "--root", str(d), "--require-clean-tree"]` (no `--rerun`, so P10 is out of scope).

| Fixture (`fid`) | Gate branch silenced by the mutant | Entry edit | Declared `defects` |
|---|---|---|---|
| `p7-m28-entry-deleted` | `pkg_gate.py:212-213` `entry is None → "entry unreadable"` (M28) | entry file unlinked | `P3,P4,P7,P8` |
| `p7-m29-source-url` | `pkg_gate.py:221` source line not the pinned url (M29) | S106 `source:` URL path changed `tests/test.sh` → `tests/test_other.sh` | `P7` |
| `p7-m30-verified-at` | `pkg_gate.py:222-223` verified-at absent/wrong (M30) | `verified-at: 2026-10-25` → `2026-10-24` | `P7` |
| `p7-m31-recheck-line` | `pkg_gate.py:224-225` recheck line absent (M31) | `recheck:` line removed | `P7` |
| `p7-m32-negative-heading` | `pkg_gate.py:226-228` no `## Negative space` section (M32) | heading line removed | `P7` |
| `p7-m33-falsifier-word` | `pkg_gate.py:229-230` section carries no falsifier (M33) | `**Falsifier:** … is falsified if` → `**Check:** … is contradicted if` | `P7` |

Why `p7-m28` declares four clauses: deleting the entry is the only way to reach `entry is None`, and the
entry is the unique input of three other clauses, which therefore also fire on the same tree — P3
`no '## Located quotes' section` (`quote_section is None`), P4 `no parsed quote`, P8
`knowledge files=N index rows=M` (one knowledge file gone vs the README index). The other five fixtures
leave every non-P7 clause green, so each declares exactly `P7`. Each mutant still flips the gate's
result on its fixture: reference prints P7 DEFECT, the mutant returns `ok` for that branch while every
other clause is unchanged — for M28 the mutant's set drops P7 and keeps `{P3,P4,P8}`.

Mutant-proof edits are guarded: each builder asserts the edited literal occurs exactly once (or the
dropped line count is exactly one) and raises `RuntimeError` on a no-op, so a future drift of the entry
fails the run loudly instead of silently mislabelling a fixture.

## Evidence — dev-mode counter (exit 0)

```
$ export TMPDIR=/fast/scratch/hyaku/kengaku-r37/R37BatP7
$ python3 plans/round37_c1_verify.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin \
    --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-37/build/R37BatP7/battery \
    --only M28,M29,M30,M31,M32,M33 --work "$S"
GATE plans/pkg_gate.py sha256=frozen
FIXTURE r36-P0 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-P1 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P2 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P3 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P4 expect=reject declared=- observed_rc=1 observed_defects=P6 ok
FIXTURE r36-P5 expect=reject declared=- observed_rc=1 observed_defects=P1 ok
FIXTURE r36-P6 expect=reject declared=- observed_rc=1 observed_defects=P9 ok
FIXTURE r36-P7 expect=reject declared=- observed_rc=1 observed_defects=P1,P3,P6,P9 ok
FIXTURE r36-L1 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L2 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L3 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L4 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L5 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE r36-L6 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE p7-m28-entry-deleted expect=reject declared=P3,P4,P7,P8 observed_rc=1 observed_defects=P3,P4,P7,P8 ok
FIXTURE p7-m29-source-url expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
FIXTURE p7-m30-verified-at expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
FIXTURE p7-m31-recheck-line expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
FIXTURE p7-m32-negative-heading expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
FIXTURE p7-m33-falsifier-word expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
BATTERY fixtures=20 wrong=0 renamed_disagree=0
MUTANT M28 P7 killed by=p7-m28-entry-deleted -- entry unreadable
MUTANT M29 P7 killed by=p7-m29-source-url -- source line absent or not the pinned url
MUTANT M30 P7 killed by=p7-m30-verified-at -- verified-at absent or not the frozen date
MUTANT M31 P7 killed by=p7-m31-recheck-line -- recheck line absent
MUTANT M32 P7 killed by=p7-m32-negative-heading -- no Negative space section
MUTANT M33 P7 killed by=p7-m33-falsifier-word -- Negative space carries no falsifier
MUTANTS total=6 killed=6 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

Full stdout saved at `.ufo/waves/round-37/build/R37BatP7/receipt-p7.txt` (sha256 `fa269af6…78b9`).
The run was executed twice with identical output (byte-equal to the block above). Every module FIXTURE
line ends `ok`, `wrong=0`, `renamed_disagree=0`, `null_detected=0`, `invalid=0`, and each mutant is
`killed by=<its p7 fid>`.

## Evidence — load-bearing ablation (delete one fixture at a time)

Method: for each mutant M, copy `p7.py` to a scratch battery dir and append
`FIXTURES = [f for f in FIXTURES if f["fid"] != "<its fid>"]`, then run
`--only M --battery-dir <variant>`. Receipt: `.ufo/waves/round-37/build/R37BatP7/load-bearing.txt`
(sha256 `30fab954…320d`).

| Fixture removed | Mutant under test | Result | `wrong` |
|---|---|---|---|
| `p7-m28-entry-deleted` | M28 | `MUTANT M28 P7 SURVIVED -- entry unreadable` | 0 |
| `p7-m29-source-url` | M29 | `MUTANT M29 P7 SURVIVED -- source line absent or not the pinned url` | 0 |
| `p7-m30-verified-at` | M30 | `MUTANT M30 P7 SURVIVED -- verified-at absent or not the frozen date` | 0 |
| `p7-m31-recheck-line` | M31 | `MUTANT M31 P7 SURVIVED -- recheck line absent` | 0 |
| `p7-m32-negative-heading` | M32 | `MUTANT M32 P7 SURVIVED -- no Negative space section` | 0 |
| `p7-m33-falsifier-word` | M33 | `MUTANT M33 P7 SURVIVED -- Negative space carries no falsifier` | 0 |

Each of the six fixtures is the sole killer of its mutant inside this module (and the remaining
round-36 fixtures do not kill P7 mutants — the freeze receipt shows P7 in the survivor set).

## Digests

| Artifact | sha256 |
|---|---|
| `battery/p7.py` | `5245533a336761f7a161395c77b0b9b2ed23609c6426edcfa762135515ae0f39` |
| `receipt-p7.txt` | `fa269af649e9391ba6117067e8b7040062145bf5cd09d69e7c4acc25b61578b9` |
| `load-bearing.txt` | `30fab95474f30b031d78dc044e60e9d7ddb4fe0859e01631e74bfd62b77f320d` |
| `plans/pkg_gate.py` (read) | `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41` (freeze) |
| entry (read) | `a4e668cc97d86cfc9e4f572e3d8ae7c96d37e248b0c3ddd0508072c89b592036` |

## Limits and risks

1. **Demonstration is observational**, per the freeze's named limit: each fixture shows the P7 branch
   is reached and its verdict visible; it does not prove the branch is the *right* check.
2. **Landing-order dependency (P8).** The genuine fixture copies every `corpus/knowledge/*.md` and the
   README from the lane. Five of the six fixtures declare exactly `P7`, which holds only while P8 is
   green on the baseline tree. The frozen claims require C1 to be measured where C2's new entry and its
   index row are both present or both absent; a half-landed C2 (knowledge file without index row, or
   vice versa) would add P8 to those five declarations and show as `wrong` — a landing-order error, not
   a broken mutation. M28's declaration is insensitive to this (P8 already fires on it).
3. **Literal coupling.** `p7-m29/m30/m33` rely on the exact entry strings listed above and
   `p7-m31/m32` on the unique `recheck:`/`## Negative space` lines; the builders' exact-once guards
   convert any future entry drift into a loud failure. The entry is not edited by this wave, so the
   coupling is to frozen bytes.
4. **No `--rerun`**, so P10 and the probe are untouched (out of scope for P7 mutants, and it keeps the
   counter run at ~7 s).
5. Scratch `/fast/scratch/hyaku/kengaku-r37/R37BatP7` removed after the receipts were copied here; no
   lane, fleet-root, corpus or plans file written; no git/jj mutation in the lane.

VERDICT: battery-p7-killed-6/6-wrong-0
