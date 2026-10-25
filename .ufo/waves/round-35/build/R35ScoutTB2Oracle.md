# R35ScoutTB2Oracle — the `protein-assembly` oracle (upstream `solution/solve.sh`) at pin `2fd12b88`

Seat: `R35ScoutTB2Oracle` (scout). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Date: 2026-10-25. Pin: `harbor-framework/terminal-bench-2@2fd12b88aafdd04a52c298e3940bcb189f9766d6`.

Scope note: the oracle was **not** run (it calls external APIs, per the assignment). It was read, and
its final design step was **replayed offline** against the grader's own literals. Live API calls were
made only for *reading* (PDB/FPBase), never to execute `solve.sh`.

---

## 1. Task tree at the pin (complete, 12 files)

The GitHub trees API was rate-limited for this host (`HTTP 403`, body: `"API rate limit exceeded for
179.218.13.209"`), so the tree was enumerated from the rendered HTML tree pages plus a blobless clone
`git clone --filter=blob:none --no-checkout https://github.com/harbor-framework/terminal-bench-2`,
`git checkout 2fd12b88aafdd04a52c298e3940bcb189f9766d6` (verified `git rev-parse HEAD` =
`2fd12b88aafdd04a52c298e3940bcb189f9766d6`). Total tree: **12 files, 24 746 bytes**.

| Bytes | Path (under `protein-assembly/`) | sha256 (first 16) |
|---|---|---|
| 5 316 | `solution/solve.sh` | `3502b801f1260857` |
| 3 847 | `tests/test_outputs.py` | `44a05a2482aa7a8e` |
| 631 | `tests/test.sh` | `9ede46648fc67c9c` |
| 2 655 | `instruction.md` | `1bb2af1d85e9a823` |
| 973 | `task.toml` | `d714960681ec921a` |
| 2 626 | `README.md` | `9e407b843058b4c6` |
| 273 | `environment/Dockerfile` | `fad40752bc9fd32d6` |
| 1 620 | `environment/pdb_ids.py` | `6563926f2aa31848` |
| 100 | `environment/pdb_ids.txt` | `ea338c4e1a776a33` |
| 475 | `environment/antibody.fasta` | `e0e13645b299470c` |
| 6 053 | `environment/plasmid.gb` | `c9e31ad0ebb4d14b` |
| 177 | `.gitignore` | `9a8dd8d9b6c3adb8` |

Raw URLs (all `HTTP 200`): `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/protein-assembly/<path>`.

**The three pinned captures the lane already holds are byte-identical to upstream.** Recomputed sha256
of upstream `tests/test_outputs.py`, `tests/test.sh`, `instruction.md` equals the lane's
`corpus/evidence/round35/tb2-eval/SHA256SUMS` entries exactly:
`44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582` (test_outputs.py),
`9ede46648fc67c9ce61975503de3e0fcff0b0fb110adc0f9e1d240a608c267b5` (test.sh),
`1bb2af1d85e9a823a8ae7273a87df8a3f67e2c93b06cddf34f0051a8b003f7c5` (instruction.md).
The lane's extra captures `task.toml` (`d714960681ec921a…`), `antibody.fasta` (`e0e13645b299470c…`)
and `pdb_ids.txt` (`ea338c4e1a776a33…`) also match upstream byte-for-byte.

---

## 2. Direct answers to the assigned questions

### 2a. Does the oracle's gBlock use GS linkers? — **Yes.**

`solution/solve.sh:165` sets `gs_linker = "GGGGS" * 3` and `:166-167` builds
`f"{flag}{gs_linker}{donor}{gs_linker}{dhfr}{gs_linker}{acceptor}{gs_linker}{snap}"`.

A `(GGGGS)₃` linker is 15 residues of G/S only, inside the grader's 5–20 window and matching its
`[GS]+` alphabet. Located quotes:

> “`gs_linker = "GGGGS" * 3`” — `solution/solve.sh:165`
> “`f"{flag}{gs_linker}{donor}{gs_linker}{dhfr}{gs_linker}{acceptor}{gs_linker}{snap}"`” — `solution/solve.sh:167`

### 2b. FLAG first, SNAP last? — **Yes, both.**

`flag = "DYKDDDDK"` (`solve.sh:164`) is the first element of `fusion` (`solve.sh:167`), and `snap` is
the last. That is exactly the grader's order assertion
`assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx` (`tests/test_outputs.py:42`) plus its
two terminal assertions `flag_idx == 0` (`:46`) and `snap_idx + len(snap_aa) == len(gblock_aa)` (`:60`).

The oracle also strips a leading Met from each of snap/acceptor/donor/dhfr (`solve.sh:155-162`,
`snap = snap[1:]` at `:156`), matching the instruction's "remove the N terminal methionine"
(`instruction.md:23`) and the grader's literals, which all begin after the Met.

### 2c. Codon choices meeting GC windows? — **Yes, and it is the mechanism, not a coincidence.**

`solve.sh:174` sets `EnforceGCContent(mini=0.3, maxi=0.7, window=50)` as a *hard* constraint alongside
`EnforceTranslation(translation=fusion)` (`:172`), with `CodonOptimize(species="e_coli")` (`:176`) as the
objective. `dnachisel`'s `gc_content(sequence, window_size=50)` returns the GC fraction of **every
sliding** 50-nt window (`dnachisel/biotools.py`, inspected at dnachisel 3.2.16), i.e. the same window
set the grader checks with its rolling counter at `tests/test_outputs.py:65-73`.

### 2d. Does anything in the task tree read `pdb_ids.txt`/`antibody.fasta` at grading time? — **No.**

This is the sharpest negative result, and it is a *whole-tree* result, not a file-level one:

- `tests/test_outputs.py` opens exactly one file: `gblock_path = Path("/app/gblock.txt")` (`:13`),
  read at `:15`. No other `open`/`Path`/`load`/`read` in either test file.
- `tests/test.sh` only installs pytest/biopython and runs pytest against `/tests/test_outputs.py`.
- The strings `pdb_ids` / `antibody.fasta` appear in the tree **only** in: `environment/Dockerfile:6-8`
  (`COPY antibody.fasta .` / `COPY plasmid.gb .` / `COPY pdb_ids.txt .`), `environment/pdb_ids.py:50`
  (the *agent-side* helper, and see §5 — it is **not** copied into the image), `instruction.md:14,16`
  (prose), `README.md:31-33,42` (prose), `solution/solve.sh:9,17,55,104` (the oracle, agent side), and
  one **comment** in the grader at `tests/test_outputs.py:26`:
  > “`# in pdb_ids.txt matches the requirement of task.yaml for each subprotein.`” — `tests/test_outputs.py:26`
- Repo-wide check: `git grep -ln 'antibody.fasta\|pdb_ids' HEAD -- . ':!protein-assembly'` → **empty**.
  No other task in the 89-task tree reads these files either.

So the grader's five subproteins are **amino-acid literals** compiled into `test_outputs.py:28-40`, and
the files the instruction names are inputs to the *agent*, never to the scorer. This independently
confirms the C1 entry's central claim (`corpus/knowledge/tb2-protein-assembly-grader.md`, §"The grader
checks"): the grader never opens `pdb_ids.txt`, `antibody.fasta`, the plasmid, or the FPBase/PDB APIs.

---

## 3. The oracle's design step, executed offline against the upstream grader

The oracle's final step (`gblock.py`, `solve.sh:127-183`) is pure computation once the protein
sequences are known. Replaying it with the grader's own literals, using the pinned dependency versions
the oracle installs (`solve.sh:5`: `biopython==1.85`, `dnachisel==3.2.16`) and the version the grader
pins (`test.sh:21`: `biopython==1.85`):

```
uv run --no-project --with dnachisel==3.2.16 --with biopython==1.85 python3 <replay>
```

Result: fusion = 902 aa, gBlock = **2 706 nt** (≤ the grader's 3 000 cap, `test_outputs.py:23`),
2 657 sliding 50-nt windows, GC count per window ∈ **[15, 35]** — the grader's inclusive band
(`tests/test_outputs.py:71`). **30/30 seeds passed the grader**; 30/30 produced identical length
2 706 nt; per-window GC minimum ranged 15–17 and maximum was always exactly 35 (the constraint binds at
the ceiling in ~60 of 2 657 windows per seed).

Then, the strongest form of the check — the **upstream grader file itself**, patched only for the
output path (`/app/gblock.txt` → a scratch path), executed under `pytest==8.4.1` (the pinned version,
`test.sh:19`):

```
k35_graderun/test_upstream_copy.py .                                    [100%]
PASSED k35_graderun/test_upstream_copy.py::test_gblock
============================== 1 passed in 0.08s ==============================
```

**The oracle's design is consistent with the grader.** Its gBlock passes the upstream grader verbatim.

### 3a. The oracle's component selection is reproducible from live APIs

The oracle picks components by FPBase spectral filters (`solve.sh:141-143`):

```
snap     = df[df["name"].str.lower().str.contains("snap")]["sequence"].iat[0]
acceptor = df[df["emission"] == 610]["sequence"].iat[0]
donor    = df[df["excitation"] == 505]["sequence"].iat[0]
```

Re-running the live FPBase API (`https://www.fpbase.org/api/proteins/?pdb__contains=<id>&format=json`)
over all 20 IDs in `environment/pdb_ids.txt` confirms the filters are still unique:

| Filter | Live match | PDB | fpbase ex/em |
|---|---|---|---|
| `excitation == 505` | **Clover** | 5WJ2 | ex 505 / em 515 |
| `emission == 610` | **mCherry** | 2H5Q | ex 587 / em 610 |
| name contains "snap" | **SNAP-tag** | 3KZY | — |

The three selected proteins are exactly the three the grader hard-codes (donor = Clover, acceptor =
mCherry, SNAP = SNAP-tag), and DHFR comes from `plasmid.gb`'s `folA` CDS translation
(`solve.sh:144-150`; `plasmid.gb:26-28`, `MISLIAALAVDRVIGMENAMP…`), which matches the grader's
`dhfr_aa` literal exactly after Met-stripping. The oracle's antibody reasoning also reproduces: the
heavy chain of `antibody.fasta` hits PDB **8RMO**, title "Crystal structure of anti-FLAG M2 Fab fragment
bound to FLAG-tag peptide epitope" (`rcsbapi` `SeqSimilarityQuery`, run locally) — i.e. the antibody
binder really is the FLAG tag, matching `flag_aa = "DYKDDDDK"` (`test_outputs.py:28`).

---

## 4. **A live-data drift that breaks the oracle as written (new, not in the lane's entry)**

This is the finding that changes how the oracle should be described. It is *not* a grader defect — the
grader is self-contained and its literals are stable. It is a defect in the **oracle's live inputs**.

**The RCSB FASTA endpoint changed its rendering for two of the three selected entries on 2026-03-18.**
The chromophore, previously a three-residue parent expansion, is now a single modified residue rendered
as `X`:

| PDB | grader's literal (as compiled into `test_outputs.py`) | live RCSB FASTA today |
|---|---|---|
| 5WJ2 (donor, Clover) | `…PTLVTTF`**`GYG`**`VACFSRYPDHMKQ…` | `…PTLVTTF`**`X`**`VACFSRYPDHMKQ…` |
| 2H5Q (acceptor, mCherry) | `…LPFAWDILSPQF`**`MYG`**`SKAYVKHPADIPDYL…` | `…LPFAWDILSPQF`**`X`**`SKAYVKHPADIPDYL…` |

Alignment (`difflib`, grader literal vs live, after Met-strip) — exactly one contiguous difference per
protein, no others:

```
== 5WJ2 grad_len=259 live_len=257
   replace  grader[85:88]='GYG'  live[85:86]='X'
== 2H5Q grad_len=235 live_len=233
   replace  grader[69:72]='MYG'  live[69:70]='X'
```

Snapshot evidence isolating the change to a single date (Wayback captures of the same URL):

| Snapshot | bytes | `X` count | seq len | equals grader literal after Met-strip? |
|---|---|---|---|---|
| `20260206054503` (before) | 332 | 0 | 260 | **True** |
| `20260409234812` (after) | 330 | 1 | 258 | **False** |
| live, 2026-10-25 | 330 | 1 | 258 | **False** |

The same drift is visible in the PDB archives' own revision records: `5WJ2` has
`REVDAT 8 18-MAR-26 5WJ2 1 SEQRES` and `2H5Q` has `REVDAT 6 18-MAR-26 2H5Q 1 SEQRES` — a SEQRES
revision on 2026-03-18, the same date as the Wayback flip and the same date as the entries'
`revision_date = 2026-03-18` / `major = 2`. The current SEQRES collapses the chromophore to one
residue: `5WJ2` chain A carries `CR2` at index 86 (1 MODRES row, parent `GLY`); `2H5Q` chain A carries
`CH6` at index 70 (3 MODRES rows, parents `MET`, `TYR`, `GLY` → the `MYG` the grader expects). The
`REMARK 465` header in `5WJ2.pdb` still reads `MISSING RESIDUES`.

**Consequence, executed.** Replaying the oracle's *own* selection against live PDB data — i.e. what
`solve.sh` would actually fetch today — the oracle does not merely produce a different gBlock, it
**crashes before writing one**:

```
donor_live  len=257 has_X=True matches_grader_literal=False
acceptor_live len=233 has_X=True matches_grader_literal=False
snap_live   len=182 has_X=False matches_grader_literal=True
fusion aa=898 (X count=2)
...
dnachisel.DnaOptimizationProblem.NoSolutionError.NoSolutionError: The solving of all constraints failed
===> FAILURE: 1 constraints evaluations failed
 FAIL ┍ EnforceTranslation[0-2694]
      │ Wrong translation at locations [324-327(+), 1611-1614(+)]
```

`/tmp/k35_live_gb.txt` was never created. The mechanism: `reverse_translate` cannot represent `X` in
DNA, and `X` is not a translatable residue (`Seq("ATGXGG").translate()` → `MX`), so
`EnforceTranslation(translation=fusion)` is unsatisfiable at the two chromophore positions. Note the
failure is *at the chromophore positions only* — `324-327` and `1611-1614` are the `X` codons.

So: **the oracle, run against the live API on 2026-10-25, aborts with `NoSolutionError` and writes no
`gblock.txt`; the grader would then score 0 (`gblock_path.exists()` fails at `test_outputs.py:14`).**
The upstream `main` branch is unchanged — `tests/test_outputs.py` on `main` is **byte-identical** to the
pinned version (`diff` → IDENTICAL, 3 847 bytes) — so upstream has not noticed or fixed it.

The task's own `task.toml` sets `allow_internet = true` (`:34`) and `docker_image =
"alexgshaw/protein-assembly:20251031"` (`:29`), so the oracle is expected to hit the live network at
run time; the pinned image contains only the three static inputs (verified: `docker run` on the pulled
image shows `/app` holding exactly `antibody.fasta` (475 B), `pdb_ids.txt` (100 B), `plasmid.gb`
(6 053 B)). Note `environment/pdb_ids.py` exists in the tree but is **not** copied by the Dockerfile and
is **not** present in the image (`ls: cannot access '/app/pdb_ids.py': No such file or directory`) — the
oracle re-creates it inline at `solve.sh:57-121` (with `time.sleep(2)` and `/app/pdb_ids.txt`, versus
the tree copy's `sleep(1)` and relative path).

### 4a. Is this a grader defect? No — and the distinction matters

The grader is **internally consistent and self-contained**: it never reads the PDB API (§2d), so the
PDB-side rendering change cannot affect the grader's verdict. The grader's literals are frozen at the
pre-2026-03-18 rendering (verified: the 2026-02-06 Wayback capture matches both literals exactly after
Met-strip). The defect is entirely in the **oracle's** live inputs, and it is a *reproducibility* break
of the shipped solution — it makes the reference solution unrunnable, and would make a legitimately
solved gBlock (built to the *current* RCSB rendering) **fail** the frozen grader, because the grader
searches for the literal `GYG`/`MYG` strings (`tests/test_outputs.py:38-40`) that today's PDB no longer
serves.

Both directions of the mismatch were executed:
- oracle's live inputs → oracle crashes, no gBlock, score 0 (above);
- grader's frozen literals → oracle's design step → upstream grader **passes** (§3).

---

## 5. Secondary observations (bounded, verified)

1. **`environment/pdb_ids.py` is dead weight in the tree.** The Dockerfile copies only the three static
   inputs; the helper is not in the image. It is a convenience copy for humans; the oracle duplicates it
   inline with different timings and an absolute path.
2. **The grader's own comment is stale.** `tests/test_outputs.py:26` says "the requirement of task.yaml",
   but the tree has `task.toml` and no `task.yaml` (`find . -name 'task.yaml'` → empty).
3. **`README.md` is the only place the intended reasoning is written down** (FLAG tag, donor ex 505,
   acceptor em 610, SNAP for benzylguanine, `(GGGGS)₃` linkers, dnachisel). It is consistent with
   `solve.sh` and with the grader.
4. **The 3000-nt cap is not the binding constraint for the oracle's own output** (2 706 nt), consistent
   with the C1 entry's `max_passing_nt=2766` observation; the oracle's 15-aa linkers sit below the
   20-aa ceiling that would produce that maximum.
5. **The oracle is the *only* solution artifact in the tree** — `find . -name '*.sh'` yields
   `solution/solve.sh` and `tests/test.sh` only.

---

## 6. Claim-by-claim summary

| Question | Answer | Confidence | Key evidence |
|---|---|---|---|
| GS linkers? | Yes — `(GGGGS)₃`, 15 aa, G/S only | certain | `solve.sh:165,167`; grader `[GS]+` + 5–20 (`test_outputs.py:54,57`) |
| FLAG first? | Yes — `flag` is element 0 of `fusion` | certain | `solve.sh:164,167`; `test_outputs.py:46` |
| SNAP last? | Yes — `snap` is the final element | certain | `solve.sh:167`; `test_outputs.py:60` |
| Codons meet GC windows? | Yes — hard `EnforceGCContent(mini=0.3,maxi=0.7,window=50)`; executed: 30/30 seeds in-band | certain | `solve.sh:174`; dnachisel 3.2.16 `gc_content` sliding-window source; replay + upstream grader `1 passed` |
| Oracle's design passes the upstream grader? | **Yes** | certain | upstream `test_outputs.py` (path-patched) → `PASSED` |
| Anything reads `pdb_ids.txt`/`antibody.fasta` at grading time? | **No** | certain | only file read is `/app/gblock.txt` (`test_outputs.py:13,15`); repo-wide `git grep` empty outside the task |
| Oracle still runnable against live APIs? | **No** — `NoSolutionError` on `X` chromophore | certain | executed traceback; Wayback before/after pair; `REVDAT … 18-MAR-26 … SEQRES` |

---

## 7. Tooling used (operator directive: record every install)

No system packages were installed and no `pacman` transaction was run (host-wide pacman pause).
Everything ran through the already-present `uv` tool (`/usr/bin/uv`) in **ephemeral, project-free**
environments (`uv run --no-project --with …`); packages are cached under
`~/.cache/uv/archive-v0/…` and nothing was added to the system Python or to `~/.local/bin`.

| Package | Version | Channel | Reason |
|---|---|---|---|
| `biopython` | 1.85 | PyPI via `uv` (ephemeral) | the version the oracle installs and the grader pins (`solve.sh:5`, `test.sh:21`) |
| `dnachisel` | 3.2.16 | PyPI via `uv` (ephemeral) | the oracle's codon-optimization dependency (`solve.sh:5`); needed to replay the design step and inspect `gc_content` semantics |
| `pandas` | 2.2.3 | PyPI via `uv` (ephemeral) | the oracle's dataframe dependency (`solve.sh:5`); needed to replay the `df[...]` selection filters |
| `rcsb-api` | 1.4.0 | PyPI via `uv` (ephemeral) | the oracle's PDB client (`solve.sh:5`); needed to reproduce the antibody→FLAG identification |
| `pytest` | 8.4.1 | PyPI via `uv` (ephemeral) | the version the grader's `test.sh` pins (`test.sh:19`); needed to run the upstream grader file |
| `docker` (client) | 29.9.1 | pre-installed system binary | inspect the pinned image `alexgshaw/protein-assembly:20251031` (pulled `sha256:94de701b…`) to confirm `/app` contents |

No `pacman -S/-Sy/-Syu/-U/-R` was executed. The scratch clone and all scratch files live under
`/tmp/k35-*`; nothing was written into the lane outside this report and this seat's scratch directory
`.ufo/waves/round-35/build/R35ScoutTB2Oracle/`. No `git`/`jj` mutating command was run in the lane.

---

## 8. Remaining unknowns / limits of this report

- The upstream oracle was **not executed** (assignment constraint). Its live-input failure was
  demonstrated by **replaying** its final design step with its own live-fetched sequences and its own
  pinned dependency versions — the same code path, not the script itself. `[INFERENCE]` that the
  unmodified `solve.sh` would hit the same `NoSolutionError` at `solve.sh:174-176`; the crash site and
  the failing constraint are identical in kind to the replayed one, but the script was not run.
- The exact wwPDB mechanism behind the 2026-03-18 SEQRES revision (whether it was a deliberate
  chromophore-representation standardization) is `[INFERENCE]`; what is *observed* is the SEQRES
  revision date, the `CR2`/`CH6` one-residue collapse, and the resulting `X` rendering.
- Whether upstream Harbor/Terminal-Bench 2.0 has since re-run or re-validated this task's reference
  solution was not checked; only that `main`'s `tests/test_outputs.py` is byte-identical to the pin's.
- Whether other tasks in the 89-task tree are affected by the same 2026-03-18 PDB rendering change was
  not surveyed — out of this seat's scope.

---

## 9. Bearing on the round's claims

- **C1** (pinned `protein-assembly` grader, executed probe): this seat adds an independent,
  executed confirmation of the entry's central negative — the grader reads nothing but
  `/app/gblock.txt` — and a positive one: the upstream **oracle** exists, its design is
  grader-consistent (upstream grader file: `1 passed`), and its component selection is reproducible
  from live FPBase/PDB (`5WJ2`/`2H5Q`/`3KZY` uniquely selected by the oracle's own filters).
- **New for the round (no lane entry covers it):** the shipped oracle is **not runnable against the
  live APIs as of 2026-10-25** — the 2026-03-18 RCSB SEQRES revision renders the Clover and mCherry
  chromophores as `X`, so the oracle's own hard `EnforceTranslation` constraint is unsatisfiable and
  `gblock.txt` is never written. The grader is *not* implicated (it never reads the PDB); the
  reference solution is. This is a task-validity observation about a benchmark's shipped oracle, and it
  is the kind of thing the corpus's `benchmark-task-validity-checklist.md` line of work cares about.

VERDICT: oracle-found-consistent-yes
