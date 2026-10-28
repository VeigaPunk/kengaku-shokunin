# Seat C2ScribeRowsD — wave 1, build — R52-C2 registry rows (5 instruments)

**Lane:** `kengaku-shokunin` · **Round:** 52 (hyaku run 11) · **Wave:** 1 (build) · **Seat:** C2ScribeRowsD (scribe)
**Base tip:** `30801b479e3418c11089b8586178b6960216f364` · **Lane HEAD at run:** `1315234bdc8024499d943f0483dcb51fb5e4a618` (round-52 freeze commit)
**Deliverable:** `/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsD/rows.md` (kept: `.ufo/waves/round-52/w1/C2ScribeRowsD/artifacts/rows.md`)

---

## 1. What I did

Drafted the five missing `SKILL.md` *## Gate/probe registry* rows assigned to this seat, each from
the script's own bytes (docstring, argparse block, every `return`/`sys.exit` site, every write
call) and then re-measured by running the instrument:

| instrument | kind | script sha256 | lines |
|---|---|---|---|
| `plans/round35_hardening.py` | **gate** | `1f1502e10b61…` | 131 |
| `plans/round36_c2_verify.py` | **gate** | `983ed65c8859…` | 234 |
| `plans/round45_c1_verify.py` | **gate** | `7745eb0a4bdf…` | 331 |
| `plans/round45_c2_verify.py` | **gate** | `ab6825e34596…` | 591 |
| `plans/round46_c1_verify.py` | **gate** | `ef19380e862e…` | 635 |

`kind = gate` for all five: each prints a frozen predicate and returns 1 when it does not hold
(not a probe that always exits 0 with mismatches on a summary line).

**No row was blocked.** Every cell is filled and every claim is checkable in the script; two rows
additionally carry a *measured* red state at the tip (§4), disclosed rather than suppressed.

## 2. Exact commands run

Scratch root `/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsD/`; every command below ran with
`TMPDIR=/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsD/tmp` where it spawns temp files.

```sh
# 1. read the five scripts in full (docstring + argparse + exit sites + writes)
read plans/round35_hardening.py ; plans/round36_c2_verify.py ; plans/round45_c1_verify.py
read plans/round45_c2_verify.py ; plans/round46_c1_verify.py
read plans/round52_c2_registry.py                      # the frozen counter that parses my rows

# 2. confirm the accepted spellings (read-only)
for f in the five scripts; do python3 "$f" --help; done

# 3. baseline of the frozen counter at the lane
python3 plans/round52_c2_registry.py --lane .          # ADVERTISED 72 / REGISTERED 44 rows=46 / MISSING 28 / SELFTEST-UNBACKED 1 (`order-check`)

# 4. clean clone of the lane at HEAD (scripts byte-identical to the base tip)
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r52/C2ScribeRowsD/lane
git -C lane diff --stat 30801b47..HEAD                 # 13 files, all round-52 freeze additions
git -C lane diff --name-only 30801b47..HEAD -- plans/round35_hardening.py plans/round36_c2_verify.py \
    plans/round45_c1_verify.py plans/round45_c2_verify.py plans/round46_c1_verify.py corpus/knowledge/ corpus/README.md
                                                       # empty -> the five scripts are the base-tip bytes

# 5. live measurement of each instrument
python3 plans/round35_hardening.py --lane .            # live lane, and in the clone
python3 plans/round36_c2_verify.py --lane .            # live lane, and in the clone
python3 plans/round45_c1_verify.py --lane . --work <scratch>/w/r45c1            # clone
python3 plans/round45_c2_verify.py --lane . --work <scratch>/w/r45c2            # clone
python3 plans/round46_c1_verify.py --lane . --work <scratch>/w/r46c1 --jobs 6   # clone
git -C lane status --porcelain                         # empty after every run (write-scope claim)

# 6. row conformance: insert my 5 rows into the CLONE's SKILL.md and re-run the frozen counter
python3 tmp/insert_rows.py                             # asserts 5 rows x 8 non-empty cells
python3 plans/round52_c2_registry.py --lane .          # in the clone, with my rows inserted
```

No tool was installed or upgraded (nothing needed; `pacman` untouched).

## 3. Measured numbers

| measurement | result |
|---|---|
| counter at the lane, before my rows | `ADVERTISED total=72`, `REGISTERED total=44 rows=46`, `MISSING 28`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 1` (`order-check`), exit 1 |
| counter in the clone **with my 5 rows inserted** | `ADVERTISED total=72`, `REGISTERED total=49 rows=51`, **`MISSING 23`** (−5), `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 1` (still only `order-check`), exit 1 (23 other seats' rows still absent) |
| `round35_hardening.py --lane .` in the **clean clone** | `H1..H6 ok`, `hardening run=6 failed=0`, **exit 0** |
| `round35_hardening.py --lane .` on the **live lane** | `H6 FAIL untracked_anywhere=2`, `hardening run=6 failed=1`, **exit 1** (the two untracked files are `.ufo/waves/round-52/w1.ready` and `w1.ready.dispatched` — wave markers, not lane defects) |
| `round36_c2_verify.py --lane .` clean clone **and** live lane | `W1 W2 W3 W5 W6 ok`, **`W4 DEFECT knowledge files=55 index rows=54 (want equal and >=43)`**, `checks=6 defects=1`, **exit 1** |
| `round45_c1_verify.py --lane . --work …` clean clone | `PINS total=33 mismatched=0`, `REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0`, `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`, `CALIBRATION advertised=10 contradicted=0`, `PREDICATE C1 pass`, **exit 0**, 3.9 s |
| `round45_c2_verify.py --lane . --work …` clean clone | `V1 ok`, **`V2 DEFECT spec=frozen gate=frozen gate_exit=1`** (the embedded gate prints `P8 DEFECT index_rows=54 knowledge_files=55`), `V3–V11 ok` (V11 `states=48 grader_pass=18 grader_fail=30 disagree=0`), `checks=11 defects=1`, **exit 1**, 2.1 s |
| `round46_c1_verify.py --lane . --work … --jobs 6` clean clone | `PINS total=65 mismatched=0`, `REFUSALS total=20 clean=20 …`, `SEALED total=12 clean=12 …`, `HONEST fixtures=104 admitted=104 …`, `CALIBRATION advertised=32 contradicted=0`, `REASON -`, `PREDICATE C1 pass`, **exit 0**, 5.9 s |
| write scope, all five | `git -C lane status --porcelain` empty after every run; the only writes are each script's own `tempfile` scratch under `--work`/`$TMPDIR` |

## 4. Findings (for the L1 — not fixed, outside my write scope)

**F1 — a committed knowledge/README drift makes two of the five instruments red at the tip.**
`corpus/knowledge/fixture-honest-geometry.md` (added by round-50 commit `822f3b7`) has a
`corpus/README.md` coverage-map bullet (line 658) but **no row in the README index table** (the
`| knowledge/<file> | … |` rows): `ls corpus/knowledge/*.md | wc -l` = **55**,
``grep -c '^| `knowledge/' corpus/README.md`` = **54**.
Two instruments assert that equality structurally and now fail on it:
`plans/round36_c2_verify.py` W4 (`knowledge files=55 index rows=54`) and `plans/round45_c2_verify.py`
V2 via the embedded `plans/pkg_gate.py` P8 (`index_rows=54 knowledge_files=55`). Both are green in
their committed receipts (`.ufo/waves/round-36/integrate/measure-final.txt`,
`corpus/evidence/round45/counter-a-run.txt`), so the rot is post-round-45, not a counter regression.
The two rows I wrote disclose the current red in their verdict-map cell instead of implying green.
Fixing it is a one-row `corpus/README.md` edit — the L1's call, since my scope forbids lane edits.

**F2 — `round35_hardening.py` H6 is wave-sensitive.** H6 counts *every* untracked file in the lane
(`git ls-files --others --exclude-standard`), so any wave in flight makes the full run exit 1
(`untracked_anywhere=2`, measured live above). The committed receipt
(`corpus/evidence/round35/hardening-counterexamples.txt`) and the SCORECARD line both run with
`--skip H6`. My row states this in the write-scope cell so a stranger does not read the red as a
lane defect.

**F3 — `round45_c1_verify.py`'s own keyed-name control passes.** `.ufo/waves/round-45/claims/control-c1-fence-keyed_name.txt`
prints `CALIBRATION advertised=10 contradicted=0`, `PREDICATE C1 pass`, `exit=0`: the round-45
counter is satisfied by a fence that keys on the counter's fixture names (the Q39 weakness the
round-46 counter exists to catch). My `round45-c1` row names this limit rather than citing that
control as a falsifier; the failing round-45 controls I cite are `control-c1-nothing`
(`clean=0 leaked=10`), `-fence-admit_all` (`contradicted=10`), `-fence-refuse_all`
(`admitted=0 refused=104`), `-fence-static_only` (`contradicted=1`) and `-fence-r44` (`contradicted=7`).

**F4 — peer artefact quality (used, with corrections).** `C2ExecRowFacts/facts_ast.json` existed and
its `argparse_flag_names` for all five scripts agree with my `--help` runs; its `network` and
`writes` fields are unreliable for these files (`round36_c2_verify.py` is reported `network: true`
from two `dict.get()` calls and a URL string that is only ever string-compared — the script imports
no HTTP client; `round35_hardening.py` lists `subprocess:run` under `writes` while it writes no
file). I took no field from it as truth without reading the source. `C2ExecRowFacts/probe_runtime.py`
declares it writes `runtime_default.json`; that file was **absent** when I finished, so I derived
every runtime fact myself (step 5 above) and say so here rather than borrowing unmeasured claims.

## 5. Files produced (absolute paths)

- `/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsD/rows.md` — the five rows (deliverable)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2ScribeRowsD/artifacts/rows.md` (kept copy)
- `…/artifacts/insert_rows.py` — row-shape assertion + clone insertion (5 rows × 8 non-empty cells)
- `…/artifacts/registry-after-insert.txt` — frozen counter with my rows in the clone (`MISSING 23`, exit 1)
- `…/artifacts/r35clone.out`, `r36clone.out`, `r45c1.out`, `r45c2.out`, `r46c1.out` — clean-clone runs
- `…/artifacts/r35.out`, `r36.out` — live-lane runs (`H6` and `W4` reds above)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2ScribeRowsD/report.md` — this report

## 6. Limits

- The five rows are drafted only; I did not edit `SKILL.md` (L1 is the single integration owner).
- `round35_hardening.py` and `round45_c1_verify.py` name no self-test in the script; their
  self-test cells say so plainly and cite external falsifiers, which the frozen counter accepts.
- The three heavy counters were measured on a clone at `1315234` whose five scripts are byte-identical
  to the base tip (`git diff --name-only 30801b47..HEAD` empty for those paths); the base tip itself
  was not checked out (mutating git is forbidden to this seat).
- Scratch dir `/fast/scratch/hyaku/kengaku-r52/C2ScribeRowsD/` was removed after the receipts above
  were copied out (no tree left on disk).
