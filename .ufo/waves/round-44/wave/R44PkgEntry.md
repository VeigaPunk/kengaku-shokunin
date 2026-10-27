# R44PkgEntry — draft: `corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md`

Seat: R44PkgEntry (scribe). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Date: 2026-10-26.
Wave item: round-44 C2 (coverage), entry draft for the pinned TB2 `feal-linear-cryptanalysis` grader.

**Deliverable (draft for the L1, not integrated by me):**
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/wave/R44PkgEntry/tb2-feal-linear-cryptanalysis-grader.md`
— 37541 bytes, sha256 `bf0dee2a0d2b9025d707f367c0c198eaf9f89921db65ff09607b454b2eddf5e8`. The L1 places it at
`corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md`.

**Receipts in the same subdir:** `counter-entry-only.txt` (counter with the entry alone),
`counter-final-package.txt` (counter with the entry + the L1-owned integration staged in my clone),
`integration-patch.diff` (that staging, as a patch the L1 can lift).

## Axes (godspeed)

- **Coverage / depth** — the entry is the 10th TB2 grader and a class the lane has not executed: constant-compare of
  an agent-written text file. Moves kept: the three attack-free public-file passes, the format asymmetry
  (hex fails / zero-pad passes), the conjunction (one missing value fails), and an executable `## Predictor`.
- **Operability** — every counter leg that the entry owns is green without any integration (V1, V4–V8, V10, V11;
  gate P1–P5, P7, P10). The remaining legs are exactly the L1's files, staged once in a clone to show the whole
  package reaches `PREDICATE C2 pass`.
- **Honesty** — predictions frozen before the run are reported as such; the one pre-freeze grader execution (V11's 48
  generated states) is disclosed in the entry; no novelty claim is made; the prior-art search is left to the wave item
  the claims assign it to.

## What I read (frozen, unedited)

`plans/round-44-claims.md` (in full); `plans/round44_c2_verify.py` (all 554 lines, incl. `DECISIVE`, V11's
`states()`/`GRADE_PY`); `plans/pkg_gate.py` (all clauses `P1`–`P10`, `QUOTE_ROW`);
`plans/pkg-spec-r44.json`; `corpus/evidence/round44/feal-linear-probe.txt`;
`corpus/evidence/round44/feal-linear-dry-cases-freeze.txt`; all eleven captures in
`corpus/evidence/round44/tb2-feal-linear-cryptanalysis/` (`test_outputs.py`, `test.sh`, `instruction.md`, `gen.py`,
`Dockerfile`, `README.md`, `solve.sh`, `decrypt.c`, `task.toml`, `feal.c`, `gitignore`) plus `SHA256SUMS`;
`plans/feal_linear_probe.py` (docstring + `CASES` + `HARNESS_PY`); `plans/order_check.py` (docstring);
`corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md` (structure model, all 437 lines);
`corpus/SOURCES.md` (header + `S129`–`S137` row shapes); `corpus/README.md` (index/Frontier/coverage);
`PROVINCE.md` (round-43 paragraph). Nothing under `plans/` or `corpus/` was modified anywhere.

## The entry's shape

| Section | Content | Counter leg |
|---|---|---|
| `source:` × 9 | S138–S146, one pinned raw URL each (`pkg-spec-r44.json` `raw_base` + `upstream`) | gate P7 |
| `verified-at:` / `recheck:` | 2026-10-26 / 180d with the re-runnable triple (`sha256sum -c`, re-fetch, re-run probe) | gate P7 |
| `## Summary` | substring semantics, three attack-free passes, shape-free/presence-strict, format asymmetry, `cases=14 observed_pass=8 observed_fail=6 mismatches=0` | V4 |
| `## Class difference from the round-43 feal entry` | file-byte constant compare vs imported module; no in-process surface | — |
| `## Source labels` | S138/S142/S146 scoring; S140/S141/S145 environment; S144 oracle; S139 request; S143 authors' prose | gate P7 |
| `## What is graded` | 10-row mechanism table + five structural consequences | — |
| `## Located quotes` | 22 quotes at 22 distinct `capture:line` locations, 3–25 words, byte-exact | gate P3/P4 |
| `## Requirement map` | 4 frozen tags, labels derived from the receipt | V7 |
| `## Case table` | 14 rows in receipt order, `(cid, tests letter, observed)` | V4/V9 |
| `## Mechanism` | 14 rows, one per receipt case, `DECISIVE` line + ≥2-word verbatim quote | V10 |
| `## Findings` | 10 findings, each tied to its receipt cases | — |
| `## Regrade` | `regrade cases=14 differ=0`, read as determinism (the keys are literals, so not a second key draw) | V4 |
| `## What the probe does not show` | image/pytest/image-toolchain/`/pub`-as-model/agent-trajectory/validity limits | — |
| `## Prior art (not searched by this seat)` | explicitly no search, no novelty claim | — |
| `## Negative space` | non-claims + falsifier (a)–(f) | gate P7 |
| `## Predictor` | exactly one ```python block, `predict(text)` | V11 |

## Counter evidence (envelope-wrapped, as the round-44 host-safety rule requires)

### Run 1 — entry alone in a clean clone (defects are exactly the L1's files)

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44PkgEntry/env /fast/scratch/hyaku/kengaku-r44/R44PkgEntry/env --bind /fast/scratch/hyaku/kengaku-r44/R44PkgEntry/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c2_verify.py --lane /fast/scratch/hyaku/kengaku-r44/R44PkgEntry/lane --work /fast/scratch/hyaku/kengaku-r44/R44PkgEntry/w
ENVELOPE start 20:37:47 cwd=/fast/scratch/hyaku/kengaku-r44/R44PkgEntry
V1 ok listed=11 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=22 distinct_quotes=22 distinct_lines=22 out_of_word_range=0
    gate: P4 ok checked=22 bad=0 first=0
    gate: P5 ok manifest_entries=11 bad=0 first=0
    gate: P6 DEFECT rows=9 bad=9 first=S138: rows=0
    gate: P7 ok source_lines=9 bad=0 first=0
    gate: P8 DEFECT index_rows=50 knowledge_files=51 bad=3 first=index rows for knowledge/tb2-feal-linear-cryptanalysis-grader.md=0
    gate: P9 DEFECT untracked=1 first=corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md
    gate: P10 ok probe_rerun=byte-equal bytes=3630
    gate: defects=3
V2 DEFECT spec=frozen gate=frozen gate_exit=1
V3 DEFECT rows=9 bad=['S138:row', 'S139:row', 'S140:row', 'S141:row', 'S142:row', 'S143:row', 'S144:row', 'S145:row', 'S146:row']
V4 ok cases=14 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=4 tags=4 bad=0
V8 ok order_exit=0 result=PASS
V9 DEFECT case_rows=14/14 bad=['PROVINCE.md names the task and the entry on no line', 'README ## Frontier does not name the task']
V10 ok mechanism_rows=14/14 bad=0
V11 ok states=48 grader_pass=24 grader_fail=24 disagree=0
checks=11 defects=3
PREDICATE C2 fail
ENVELOPE end 20:37:53 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

`V9`'s two red sub-defects in this run are `PROVINCE.md` and `README ## Frontier` — lane files I may not edit; the
entry-owned legs of V9 (`case_rows=14/14`, every S138–S146 id in the body outside `source:` lines) are green here.

### Run 2 — final entry + the L1-owned integration staged in the same clone

Staging (clone only, never committed): the nine `SOURCES.md` rows, one `corpus/README.md` index row + coverage bullet
+ `## Frontier` sub-bullet, one `PROVINCE.md` paragraph, then `git -C "$S/lane" add -A` (index only, no commit) so
gate `P9` sees a clean tree. Patch: `R44PkgEntry/integration-patch.diff` (66217 bytes, sha256
`1bb9d1a236359b1b8b0c010afbb5cdab7c734bf18d8be0bce49314e8637a1e58`).

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44PkgEntry/env /fast/scratch/hyaku/kengaku-r44/R44PkgEntry/env --bind /fast/scratch/hyaku/kengaku-r44/R44PkgEntry/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c2_verify.py --lane /fast/scratch/hyaku/kengaku-r44/R44PkgEntry/lane --work /fast/scratch/hyaku/kengaku-r44/R44PkgEntry/w
ENVELOPE start 20:39:25 cwd=/fast/scratch/hyaku/kengaku-r44/R44PkgEntry
V1 ok listed=11 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=22 distinct_quotes=22 distinct_lines=22 out_of_word_range=0
    gate: P4 ok checked=22 bad=0 first=0
    gate: P5 ok manifest_entries=11 bad=0 first=0
    gate: P6 ok rows=9 bad=0 first=0
    gate: P7 ok source_lines=9 bad=0 first=0
    gate: P8 ok index_rows=51 knowledge_files=51 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=3630
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=9 bad=0
V4 ok cases=14 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=4 tags=4 bad=0
V8 ok order_exit=0 result=PASS
V9 ok case_rows=14/14 bad=0
V10 ok mechanism_rows=14/14 bad=0
V11 ok states=48 grader_pass=24 grader_fail=24 disagree=0
checks=11 defects=0
PREDICATE C2 pass
ENVELOPE end 20:39:31 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Requested legs, verbatim from this run:

```
V4 ok cases=14 mismatches_named=0/0 bad=0
V7 ok rows=4 tags=4 bad=0
V9 ok case_rows=14/14 bad=0
V10 ok mechanism_rows=14/14 bad=0
V11 ok states=48 grader_pass=24 grader_fail=24 disagree=0
```

### V11 pre-check (before staging, entry-only clone)

```
V11 (True, 'states=48 grader_pass=24 grader_fail=24 disagree=0')
ENVELOPE end 20:37:42 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

V11's split (24 pass / 24 fail) matches the generator's 16 kinds × 3: the eight kinds that keep every constant as a
contiguous substring pass (`exact`, `shuffled`, `concat`, `zero-pad`, `decoys`, `comma`, `duplicated`,
`prefixed-digit`), the eight that break one do not (`drop-one`, `drop-three`, `hex`, `bump-one`, `absent`, `empty`,
`split-one`, `half`).

## Findings the entry states (each with line evidence; quotes ≤25 words)

1. **Substring semantics over the whole file.** `test_outputs.py:120` `data = open("/app/plaintexts.txt").read()`;
   `:121` `for c in soln.split():`; `:122` `assert c in data`. Order, separators, duplicates, padding and any extra
   content are outside the predicate; presence of all 100 constants is the whole condition. Measured:
   `oracle-concatenated P`, `oracle-reversed P`, `oracle-zero-padded P`, `oracle-plus-decoys P`, `one-missing F`.
2. **Three attack-free passes from public pin files.** `decrypt-public-keys P` (keys at `gen.py:12`:
   `keys = ["0x68e63", "0x62571", "0x1f61c", "0xb74a5"]`), `replay-public-gen P` (`gen.py:61`
   `plaintext_hash = hashlib.sha256(seed_hash + counter_bytes).digest()`, counters 32-131), `copy-public-constants P`
   (`test_outputs.py:4-103`). The image deletes the generator (`Dockerfile:14` `RUN rm gen.py`) but the repository
   publishes it; the probe's `/pub` models an agent that read the repository.
3. **The request states no format; the grader accepts decimal only.** `instruction.md:9` "the file
   /app/ciphertexts.txt, and saving your answer in the file" (and `:10` `/app/plaintexts.txt`) say nothing about
   radix; `hex-output F` (correct plaintexts in hex) vs `oracle-zero-padded P`. The decimal shape of the oracle's
   answer is `decrypt.c:136` `printf("%lu\n", plaintext);`, reached through `solve.sh:289`'s `./decrypt` call and
   `:304` `./attack > /app/plaintexts.txt` — S144/S145 line evidence for every sentence that rests on them.
4. **Class difference from the round-43 feal entry.** That grader imports an agent module into its own interpreter and
   compares one value (`assert feal_in_c.get_keys()[5] == stolen`); this one executes no agent code and compares file
   bytes. Consequence stated in the entry: the round-43 namespace cheats have no analogue, and the trade is looser
   shape (concat/reverse/pad pass) for stricter presence (all 100, `one-missing F`).
5. **Reward shape.** `test.sh:22` runs the one captured test under pytest; `:25-29` map the exit status to
   `/logs/verifier/reward.txt` (one bit, no partial credit), so all four failing shapes land on the same 0.

## Integration the L1 owns (drafted, exercised in a clone only)

- **`corpus/SOURCES.md`**: nine rows after `S137`, 11 cells each, tier `A`, status `mined`, opened `2026-10-26`,
  recheck `180d`, used-by `corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md`; anchor cell carries
  `sha256 <pkg-spec-r44.json digest>`; teaches cell ≥8 words and pairwise distinct. S138 row as exercised:

  `| S138 | Terminal-Bench 2.0 feal-linear-cryptanalysis grader (tests/test_outputs.py) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-linear-cryptanalysis/tests/test_outputs.py | code | A | the executed scoring predicate of this one TB2 task at a pinned commit: one pytest function that reads an agent-written text file and tests 100 embedded decimal constants as substrings of the whole text | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, test_outputs.py:1-122, :122 "assert c in data" (4 words); sha256 f59ebc7218a648582483cee02556c3bc1235e186301376bc3be066ed106ed9f9 | one test function, not a suite: the whole check is a loop over soln.split() asserting each constant is a substring of the file's text, with no count, order, format or exactness test | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md |`

- **`corpus/README.md`**: (a) one index row `| \`knowledge/tb2-feal-linear-cryptanalysis-grader.md\` | … |` citing
  `S138, S139, S140, S141, S142, S143, S144, S145, S146` (the gate wants every row id literally, so no `S138–S146`
  range in that row); (b) one coverage bullet starting `- ` naming the entry and the receipt path
  `evidence/round44/feal-linear-probe.txt`; (c) one `## Frontier` sub-bullet naming `feal-linear-cryptanalysis`
  (V9 requires the literal task name in that section).
- **`PROVINCE.md`**: one line carrying both `feal-linear-cryptanalysis` and the entry filename (V9's one-line test),
  plus the round-44 narrowing sentence.
- All four texts are in `R44PkgEntry/integration-patch.diff`; they are drafts, not reviewed prose.

## Discrepancies found in the frozen material (reported verbatim, not edited)

1. **`plans/round-44-claims.md` §C2 says** "gen.py is deleted from the image (Dockerfile:12-13)". The capture has a
   blank line at `Dockerfile:12`, `RUN rm orig_plaintexts.txt` at `:13` and `RUN rm gen.py` at `:14`
   (`nl -ba Dockerfile`). The entry cites `:13`/`:14`. The frozen claims are untouched.
2. **`plans/round-44-claims.md` §C2 says** "test.sh:22-26 rewards pytest's exit status". The capture's `:22` is the
   pytest invocation; the reward mapping is `:25-29` (`if [ $? -eq 0 ]; then` / `echo 1 > /logs/verifier/reward.txt`).
   The entry cites `:22` and `:25-29`.
3. No other claim was contradicted by the captures. `instruction.md:10`, `test_outputs.py:4-103`/`:120`/`:121-122`,
   `gen.py:12`/`:57-62`, and the receipt summary `cases=14 observed_pass=8 observed_fail=6 mismatches=0` /
   `regrade cases=14 differ=0` all match byte-for-byte.

## Limits of what I ran

- The two counter runs are in a `git clone -q --shared` of the lane at `$S/lane` (`rev-parse --show-toplevel` =
  that path), under the round-44 envelope; both envelopes report the PATH-dir content digest unchanged. No lane file,
  Git index, jj state or fleet-root file was written; the clone's index was staged (`git add -A`) but never committed.
- Run 2 proves the whole package reaches `PREDICATE C2 pass` **with my staged drafts of the L1's files**; it does not
  prove the L1's final wording passes, and it is not a run on the landing tip.
- `V2`/gate `P10` re-ran the frozen probe inside the clone (`probe_rerun=byte-equal bytes=3630`); the image was never
  pulled, pytest was never run, and the probe's own limits are restated in the entry's `## What the probe does not
  show`.
- I did not re-fetch the nine URLs; the entry's `recheck:` line names the re-fetch that would supersede it.
- No tool was installed or upgraded (nothing was needed); no pacman/uv/npx transaction ran.
- Prior art for this task was not searched (the claims assign it to a wave item); the entry claims none.

## Out of scope / not done

- No edit to `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`, `PROVINCE.md`, `SKILL.md`, `SHONEN.md` — the
  entry and its integration drafts are handed to the L1.
- No commit, push, or jj mutation anywhere; no C1 (`plans/battery44`) work; no `feal.c`/`gitignore` registry rows
  (they are captures, not spec rows — `feal.c` is not cited by line in the entry for that reason).
- Scratch `/fast/scratch/hyaku/kengaku-r44/R44PkgEntry` is deleted with `plans/scratch_guard.py safe-rm` after the
  receipts were copied into this subdir.

VERDICT: entry-drafted-c2-legs-ok-5/5
