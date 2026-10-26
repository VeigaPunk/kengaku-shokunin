# R43PlanNext — round-44 data walk: calibration list pricing + next coverage task (scout, wave 1)

Seat `R43PlanNext` (leaf, read-only on the lane). Lane clone at `d33350fdb01ce27cbff47b04642fd2c1471e5c26`
(`git -C $S/lane rev-parse HEAD`; `$S=/fast/scratch/hyaku/kengaku-r43/R43PlanNext`, toplevel asserted = `$S/lane`).
Frozen files untouched (nothing in the lane was written; every run in `$S`). Scripts, outputs and sha256 in
`.ufo/waves/round-43/build/R43PlanNext/` (`COMMANDS_sha256.txt`; all files < 12 KiB).

Envelope (Q32), every run through `claims/envelope.sh "$S/env" <cmd>`; `local_bin_content_before=after=328be01808ba022f unchanged` at every boundary below:

| run | start→end | exit |
|---|---|---|
| `rcmeasure2.py` (first attempt: all 73 "killed" — my artefact, see §A.1) | 19:15:29→19:16:09 | 0 |
| `rcmeasure2.py` (fixed) | 19:17:13→19:17:49 | 0 |
| `rcextra.py` / `rcextra2.py` (extra witnesses) | 19:18:43→19:19:05 / 19:19:22→19:19:53 | 0 |
| `uprice.py` (u=18 mutants, direct ref-vs-mutant) | 19:22:05→19:22:09 | 0 |
| `qo_flake.py oracle 40` (query-optimize runtime test) | start 19:23:48, **no end line**: job killed at 900 s (`error: interrupted`) after printing the oracle result | – |
| query-optimize golden vs original timing | 19:38:53→19:40:59 | 0 |
| `feal_linear_run_oracle.sh` | 19:40:06→19:40:10 | 0 |
| `rcall.py` (combined round_close detectors) | 19:41:42→19:42:45 | 0 |
| `c1_u.py` vs battery42 (u-mutants) | 19:44:09→19:44:14 | 1 (dev mode, survivors) |
| `c1_u.py` vs scratch battery | 19:44:55→19:44:58 | 1 (dev mode, survivors) |

---

## Headline

1. **round_close.py survivors have a witnessed direction today — and the F42CritPlanNext "9 of 20" is stale in two ways.**
   (a) `plans/round_close.py` changed at the round-42 landing (`ff14d76`, +9 lines, sha `112b52f0…` → `cd581f8a…`), so every
   survivor line in `res_round_close.json` moved (+1 for L69-236, +9 from L237). (b) Re-measured at the tip: population **73**
   (not 70), the lane's standing detector `--selftest` kills 40, **33 survive**; 21 of the 33 have an exit-code direction
   witnessed today, 7 differ only in text, 5 are unwitnessed (one is equivalent by reading). R42's "20 survivors" were
   survivors of selftest **plus 8 live-lane commands**; against a from-nothing battery the base is the 33.
2. **u = 18 has no declared direction today (no mutant exists), but 8 of the 18 rows get a measured direction from one
   single-replacement mutant each**; six of those mutants are killed, attributed, `value=differs` by 7 scratch fixtures through
   the unmodified round-43 counter machinery (`MUTANTS-BY-TOOL anchor=5/5 order=1/4`, §B.3). Two rows are advertised behaviours
   the unmodified tool does **not** exhibit (u8, u10): a doc/code contradiction, not a mutant.
3. **Next coverage: TB2 `feal-linear-cryptanalysis` (class F1, 0 of 14 read)**, oracle measured offline in ~4 s with every file
   from the pin (§C). Query-optimize (class D1) is the second pick (flake-rider vehicle), blocked for a clean-clone counter by a
   50.6 MB external download.

---

## A. `round_close.py` survivors

### A.1 Method (commands)

```
S=/fast/scratch/hyaku/kengaku-r43/R43PlanNext; git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane
sha256sum $S/lane/plans/round_close.py        # cd581f8a263372b164f5a4fdf20e25eefaa22d2087097de75e463c19043a8144 (336 lines)
git diff ec17216 ff14d76 -- plans/round_close.py   # +9 insertions: `import shutil` (L68) and the R5 reused --work clear (L240-247)
envelope.sh $S/env python3 $S/rcmeasure2.py   # 73 AST mutants (R42PlanNext/mut_harness.py operators) x detector sets
envelope.sh $S/env python3 $S/rcall.py        # selftest-survivors x (9 witness + 9 live + 6 extra detectors), rc pair per killer
```

Detector sets: **standing** = `--selftest`; **live8(+r43)** = R42's eight live-lane commands (rounds 40/41/39/99, no `--round`,
missing census, `--lane` = `plans/`, `--lane` = a non-git dir) plus round 43; **witness9** = R41's nine
`wit_rc.py` commands (fixtures from the tool's own `build_fixture`); **extra** = five commands I added (§A.3). Kill =
`(rc, normalised stdout+stderr)` differs from the unmodified tool on that command (a result difference, not an attributed kill).
Reference run stable twice (`REF-STABLE True`). Artefact I hit and fixed: the mutant file must be named `round_close.py`,
otherwise argparse's `prog` differs and the `--round`-less command "kills" every mutant (all 73 killed on the first attempt).

### A.2 Numbers

| | R42 (`res_round_close.json`, old tool) | tip (this seat) |
|---|---|---|
| population | 70 | **73** (+3 from the R5 fix: L243 `if`, L243 `or→and`, L245 `if`) |
| killed by `--selftest` alone | – (R41: 40) | **40** |
| survive selftest | 30 (R41) | **33** |
| killed by selftest + live8 | 50 | 50 |
| survive selftest + live8 | 20 | **23** = R42's 20 shifted + 3 new |
| of those, witnessed by witness9 | 11 (9 directional + 2 message-only 2→2) | 11 (same lines shifted, same 9+2) |
| unwitnessed by witness9 | 9 | **12** (the 9 + 3 new) |

Line map (R42 → tip): L97→98, L121→122, L131→132, L144→145, L148→149, L164→165, L177→178, L179→180, L181→182, L199→200, L200→201,
L209→210, L291→300, L310/312/313/315→319/321/322/324. The R42 `res_round_close.json` mutant offsets (`a`,`b`) are for the old
bytes and **must not be reused**; `mut_harness.mutants()` regenerates them from the current file.

### A.3 Per-mutant table of the 33 selftest-survivors (`rc_all.json`, `rcall.out`)

Direction = rc pair (reference > mutant) of the killing command. "R" = reachable by a from-nothing fixture under the round-43
counter contract (cwd = fixture dir, env pinned, argv only, fixture dir read-only at run time, `{WORK}` fresh and empty) —
**[INFERENCE]** except where stated, because the detectors above use `build_fixture`/the live lane, not counter fixtures.

| line (tip) | mutation | killer (rc pair) | class | reach |
|---|---|---|---|---|
| 98 | `== 0 → != 0` (`git_ok`) | gate, receipt committed but deleted from work tree (0>2) | rc | R |
| 98 | `0 → 1` | same (0>2) | rc | R |
| 132 | `or → and` | same (0>2) | rc | R |
| 122 | `== → !=` (round filter) | claims naming only `corpus/evidence/round39/x-probe.txt` (0>2) | rc | R (**new**, `only-evidence-path-claims`) |
| 122 | `if → False` | same (0>2) | rc | R (**new**) |
| 145 | `and → or` | census only at cwd-relative path (2>0) | rc | R only with two stub censuses (lane's own first, cwd's second) (**new**) |
| 145 | `if → False` | `SHOKUNIN_ROOT` set (0>2) | rc | **env-gated: unreachable** (env pinned) |
| 149 | `if → False` | census in a parent of the lane (0>2) | rc | R (**new**) |
| 175 | `if → False` (no claims) | `--round 99` (2>1, traceback) | rc | R |
| 178 | `if → False` (no order tool) | (2>1) | rc | R |
| 319, 322 | selftest `if → False` | (2>1) | rc | R |
| 321, 324 | selftest `return 2 → 0` | (2>0) | rc | R |
| 326 | `is → is not` (census None) | any gate run (0>2) | rc | R |
| 328 | `if → False` / `is → is not` | `--census` missing (2>1) / any gate (0>2) | rc | R |
| 331 | `return 2 → 0` | `--census` missing (2>0) | rc | R |
| 243 ×2, 245 | R5 clear-reused-`--work`: `if → False`, `or → and`, `elif → False` | `--selftest` over a `--work` pre-seeded with a file / symlink / dir (0>1) | rc | **counter-gated: unreachable** (`{WORK}` is created fresh, empty; `d` is read-only) (**new**) |
| 116 | `and → or` | stdout only (0>0) | text | – |
| 165, 168, 170, 182 | setup guards `if → False` | message only (2>2) | text | – |
| 200 | `or → and` | stdout only (0>0) | text | – |
| 326 | `if → False` (no `--round`) | message only (2>2) | text | – |
| 180 | `if not census.is_file()` → False | **none** | equivalent: `find_census` only returns existing files | limit |
| 200 `not x→x`, 201, 210, 300 | stdout newline / stderr echo / selftest failure echo | none by rc; constructible only with a stub tool that writes stderr / lacks a trailing newline / fails a case | text-only | – |

Tally of 33: **21 exit-code direction witnessed** (98×2, 122×2, 132, 145×2, 149, 175, 178, 243×2, 245, 319, 321, 322, 324,
326-is, 328×2, 331); 7 text-only-witnessed; 5 unwitnessed (180 equivalent by reading + 4 stream-only). Under the counter contract
**17 are R**, 1 env-gated, 3 counter-gated. The counter's `PAIR` direction (`"2>0"`, `"0>2"`, `"2>1"`) already models all 17.
Text-only 12 would need a new direction (stdout/stderr digest) the counter does not have.

Counter cost for the 17 (priced, not built): a third tool key in `TOOLS`/`PINS` (round_close `cd581f8a…`, unchanged since
`ff14d76`), new `TOTAL`/`FLOORS`, `classes()` returning `-`; fixtures need a **stub `plans/order_check.py`** (exit 0/1/2 by
receipt state) and an **executable stub census** (`ctx.sh("install", …)`; the module source may not contain `chmod`), because
the tool shells out to both. `--selftest` mutants (319-324) need no stub. Mutants 98/132 need `rm` of a committed receipt.

---

## B. The `u = 18` unmutated advertised behaviours (R43CritEquiv §3)

### B.1 Today's declared directions: zero (no mutant exists for any of the 18). A from-nothing single-replacement probe

`uprice.py` builds each fixture repo from `git init`, runs the reference and a one-edit copy of the tool, and prints
`rc` + `class=` set (receipt `uprice.out`, all lines below are its output):

| # | row (R43CritEquiv numbering) | mutant (old → new) | ref → mutant | verdict |
|---|---|---|---|---|
| 3 | anchor:62-64 explicit lane path | row-path branch `if p in … → if False and …` | rc 0 [] → rc 1 [anchor-unbound] | **rc-mirror** |
| 5 | anchor:88 `digest-short` | label `short`→`long` for `<64` | rc 1 [digest-short] → rc 1 [digest-long] | **silence** |
| 6 | anchor:88 `digest-long` | label `long`→`short` | rc 1 [digest-long] → rc 1 [digest-short] | **silence** |
| 7 | anchor:99-100 twin captures not a defect | `hit = sorted(…)[:1]` | rc 0 [] → rc 1 [capture-unanchored] | **rc-mirror** |
| 9 | anchor:106-108 lessons from work tree | `f.read_text(…)` → `git show HEAD:<p>` | rc 0 [] → rc 1 [digest-unknown] | **rc-mirror** |
| 14 | order:26 bad arguments / unparseable round | `required=True→False` on `--claims`; `--lane`; name-pattern guard off | rc 2 → rc 1 (traceback), 3 of 3 | **error** |
| 16 | order:37-38 every blob read | `parts[1] != "blob"` + `.md`-only | rc 1 → rc 0 | **rc-silence** |
| 18 | order:14 dir from round number | `round_no` → `round_no + 1` | rc 1 → rc 0 | **rc-silence** |
| 2 | anchor:26-27 exit 2 | each of 3 guards off (`is_dir`, `SOURCES.md`, `.git`) | rc 2 → rc 2, text differs | rc-equivalent (redundant downstream fallbacks) |
| 12 | order:26 not a git tree / not a dir | guard off | rc 2 → rc 2 | rc-equivalent |
| 13 | order:26 never committed | `if not freeze`, `if not receipt_commit` off | rc 0 → rc 0, text **identical** | equivalent (dead guard behind the HEAD check) |
| 17 | order:41 uncommitted receipt is 2 | HEAD `cat-file` check off (staged and on-disk receipt) | rc 2 → rc 2, text differs | rc-equivalent (`add_commit` empty still → 2) |
| 4 | anchor:76 `--verbose` | `if verbose:` → `if False:` | rc 0 → rc 0, stdout lines only | text-only (no direction in the counter) |
| 1, 11, 15 | read-only invariants; commits only | – | – | no single-replacement mutant exists |
| 8 | anchor:102-103 "a row with no anchor token raises nothing … a multi-locator row with no claim stays green" | – | reference **rc 1**, two `class=capture-unanchored` (`uw/u8`: two row paths, `anchor none`, `tokens=0 defects=2`) | **doc/code contradiction in the unmutated tool** (`anchor:547-556`: `per and not ex and len(per) > 1` runs without any token) |
| 10 | anchor:114-115 "an erratum whose row was since repaired stays valid" | – | repaired row + erratum citing an uncommitted 64-hex wrong token: **rc 1 `erratum-digest-unresolved`**; citing a committed sibling digest: rc 0 | **doc true only when the wrong token is a committed digest** |

So **8 directional rows, 5 rc-equivalent/text-only, 3 invariants, 2 doc/code contradictions** (8+5+3+2 = 18). Row 18's mutant is
F42XMutNear's **NO26**, killed by `battery42`'s `o_scan-xo7-timeout-rows`: "unmutated" ≠ "undemonstrated"; run the candidate through the
standing battery before freezing it (B.2).

### B.2 Which are real survivors of `battery42` (the standing battery) — measured

Counter copy with the nine mutants as `MUTANTS` (`u_mutants_table.txt`), kept outside the lane in `$S/ctr/` (a copy beside work/battery
dirs breaks the counter's own hide of `COUNTER_DIR`, which cost me one failed run):

```
envelope.sh $S/env python3 $S/ctr/c1_u.py --lane $S/lane --battery-dir $S/lane/plans/battery42 --work $S/w42
PINS total=2 mismatched=0 | BATTERY fixtures=29 wrong=0 tampered=0 sidechannel=0
MUTANTS total=9 killed=2 survived=7 invalid=0 null_detected=0 unattributed=0 | MUTANTS-BY-TOOL anchor=0/5 order=2/4
MUTANT U16 killed by=o_scan-xo7-timeout-rows attributed=L126 value=differs   MUTANT U18 killed by=o_scan-xo7-timeout-rows attributed=L164 value=differs
```

### B.3 A scratch battery (7 fixtures, `u_rows.py` + `u_ord.py`) through the same counter

```
envelope.sh $S/env python3 $S/ctr/c1_u.py --lane $S/lane --battery-dir $S/bat --work $S/w43     (19:44:55→19:44:58)
BATTERY fixtures=7 wrong=0 tampered=0 sidechannel=0
MUTANT U3  killed by=u3-row-path-binds     attributed=L354 value=differs     MUTANT U5  killed by=u5-sixty-three-hex   attributed=L522 value=differs
MUTANT U6  killed by=u6-sixty-five-hex     attributed=L522 value=differs     MUTANT U7  killed by=u7-twin-captures     attributed=L539 value=differs
MUTANT U9  killed by=u9-dirty-erratum      attributed=L384 value=differs     MUTANT U14c killed by=u14c-odd-claims-name attributed=L161 value=differs
MUTANT U14 order error UNATTRIBUTED hits=1 last=site-record-equal first=u14-no-claims-flag span=L144-L144
MUTANTS total=9 killed=6 survived=2 invalid=0 null_detected=0 unattributed=1   (U16/U18 survive by construction: not in this battery)
```

`U14` (`required=False` on an `add_argument`) is a **leg-g false negative**: the replaced line's next event is identical because the
changed state hides inside the parser object — the limit the counter docstring already names. Use `U14c`, not `U14`/`U14b`.
Those fixtures are mine (scratch, not lane material, not offered as battery43 modules); they price the work at ~2 s per fixture and one
helper (`lane()`), and a non-author would still compare any adopted module for shape against `w_near.py`.

### B.4 Recommended round-44 C1 list (priced)

| block | mutants | counter change | state today |
|---|---|---|---|
| **u-rows on the two existing tools** | **6**: U3, U5, U6, U7, U9, U14c (rows 3, 5, 6, 7, 9, 14) | none beyond a new `MUTANTS` table, `TOTAL=6`, `FLOORS={anchor:5, order:1}`; legs f/g/h/i reused | **6/6 killed attributed** by scratch fixtures (B.3); 0 killed by battery42 (B.2) |
| `round_close.py` reachable-directional | **17** (A.3 "R") | third tool, PIN, stub order tool + stub census | direction witnessed by result difference today; reachability from-nothing **[INFERENCE]**, fixtures not built |
| carried as limits, never mutants | 4 doc/code or equivalence limits: rows 8, 10 (doc contradictions), 13 (dead guard), L180 (dead guard); 12 text-only | – | report, do not freeze |

Total recommended `n = 23` (6 counter-verified + 17 detector-witnessed). If the round must stay on the frozen tools only, `n = 6`.
Directions (Q29/Q33) are the pairs above, re-derived through the counter in development mode before any freeze; the round-43
`control-c1-direction-mislabel` shape (NA7 relabelled → `SURVIVED exhibits=0>1,rc-mirror`) applies per mutant.

---

## C. Next coverage task

R43ConsiderThese (`.ufo/waves/round-43/build/R43ConsiderThese.md`, 89 tasks, 11 classes): the lane's nine read graders touch 6
classes; uncovered by task count: **F1 14, V1 3, W1 2, O1 2, D1 1**. Its ranking: F1, then D1 + wall-clock gating, then O1.
I checked offline feasibility from the pinned files only (pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, tree via
`gh api repos/harbor-framework/terminal-bench-2/git/trees/<pin>?recursive=1`, 1446 entries).

### C.1 Survey of the 14 F1 tasks plus D1/O1 candidates (Dockerfile + `solve.sh` network use, static)

Self-contained (Dockerfile `COPY` only, `solve.sh` installs nothing): **feal-linear-cryptanalysis (26 KB), fix-git, password-recovery,
sqlite-db-truncate, vulnerable-secret, code-from-image**. Network in the image or oracle: chess-best-move, count-dataset-tokens,
crack-7z-hash, fix-ocaml-gc (`git clone`), gcode-to-text, log-summary-date-ranges, mteb-leaderboard, mteb-retrieve; query-optimize
(Dockerfile downloads a 50.6 MB DB); break-filter-js-from-html (`wget`).

### C.2 Pick: `feal-linear-cryptanalysis` (F1) — oracle executed offline

Files: `instruction.md`, `tests/test_outputs.py` (122 lines), `tests/test.sh`, `solution/solve.sh` (7.7 KB, builds `attack.c` with
OpenMP), `environment/Dockerfile` + `task-deps/{decrypt.c,feal.c,gen.py}`, `task.toml`, `README.md` (sha256 in `tb2_sha256.txt`).
Grader: 100 constants in `test_outputs.py:4-103`; `test_attack` reads `/app/plaintexts.txt` and asserts **substring**
`c in data` for each (`:120-122`). `gen.py:12` fixes the four keys (`0x68e63 0x62571 0x1f61c 0xb74a5`) and hashes them into the PRNG
(`:18-28`), so the image state is deterministic.

```
envelope.sh $S/env bash feal_linear_run_oracle.sh $S/tb2/fl/img   # gcc -O3 feal.c decrypt.c; python3 gen.py; rm orig_plaintexts.txt gen.py; solve.sh (paths remapped)
Generated 32 plaintext/ciphertext pairs ... Generated 100 ciphertexts ...
CONSTANTS 100 ALL_IN_DATA True LINES 928        ENVELOPE start 19:40:06 / end 19:40:10 exit=0
```

Everything (build, oracle, grader check) ran in about 4 s with gcc + python3; no network. The oracle's `plaintexts.txt` holds 928
whitespace tokens for 100 plaintexts (the C attack prints diagnostics too), and the check is satisfied: substring, not set equality,
not count. Limits: pytest is not run (`test.sh` uses `uvx` — same harness-mapping step as feal-differential); host gcc/python3 for the
image's `python:3.13-slim-bookworm`; **prior art for this task was not searched** (a dated receipt is a wave-1 item before any
novelty sentence); the class sibling `feal-differential-cryptanalysis` shares files with it, so the entry should state the class
difference (F1 constant compare of a file vs M1 imported module) rather than re-narrate the cipher.
Candidate probe cases (not run): nop (no file → FAIL), oracle (PASS), plaintexts-with-junk (PASS, the substring semantics),
plaintexts shuffled (PASS, no order check), one constant missing (FAIL), digits split across lines (FAIL), file of the 32 known pair
plaintexts only (FAIL), ciphertexts copied unchanged (FAIL).

### C.3 Runner-up: `query-optimize` (D1 + wall-clock), measured

`tests/test_outputs.py` has five tests; the decisive timing test is `:82-145`: `median(sol) <= 1.05 * median(golden)` over `ITERATIONS=5`
alternating runs; DB hash pin `:77` = `89eab7555b6b86a74b8e0ee5a7db7beec0b2575a45cd2b22fe132eae79f5ad5a`, equal to the HF
`x-linked-etag`, 50,606,080 bytes, downloaded in the Dockerfile (`huggingface.co/…/resolve/84e42d43…/oewn.sqlite`). **`solve.sh`'s query is
byte-identical to `tests/golden.sql`** (`cmp <(cat golden.sql; echo) solve_sol.sql` equal), so the oracle passes the runtime test only by
being the same query: measured with the test function mapped to scratch paths (stdlib sqlite 3.54.0, no pytest installed), **40/40
PASS, speedup 0.978–1.019** against a fail boundary of 1/1.05 = 0.952; golden 0.269 s, the original `my-sql-query.sql` 122.98 s (so a
slow-but-correct `sol.sql` costs ~25 min per grading). The 8-parallel load run was killed at the 900 s deadline and is **unmeasured**.
Blocker for a clean-clone counter: the 50.6 MB DB cannot be a committed capture (receipt cap 1 MiB); it needs a pinned-download
policy the lane has not used. Value: the only wall-clock-gated grader in D1 and the natural vehicle for considerthese proposal 3's flake
rider. Refused for now: V1 (3 qemu tasks), W1, O1 (headless Chrome, feasibility not tried).

---

## Limits

- A.3 reachability is inferred; the 17 round_close mutants were witnessed with `build_fixture` and live-lane commands, not counter fixtures.
- B.1's mutants are mine, one per row, chosen for observability; they are not a claim that no better mutant exists for rows 2, 4, 11, 12, 13, 15, 17.
- `u8`/`u10` are observations on the frozen tools (`uw/u8`, `uw/u10a/b` fixtures in `uprice.py`); nothing was edited.
- The scratch battery (B.3) is not offered as lane material; R43Bat* seats own battery43.
- The query-optimize flake rate under load and under `uvx pytest` was not measured.

Scratch `$S` is deleted with `plans/scratch_guard.py safe-rm` after this report is written.

VERDICT: plan44-calibration-23-mutants-coverage-feal-linear-cryptanalysis
