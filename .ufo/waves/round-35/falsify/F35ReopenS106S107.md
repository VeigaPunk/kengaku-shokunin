# F35ReopenS106S107 — re-open of S106 (`tests/test.sh`) and S107 (`instruction.md`)

Round 35 (hyaku run 7, 2026-10-25), wave 2 (falsify). Seat axes: **coverage**, **freshness**.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, landing tip `dfee6fff631ebc5f623ba4506e5c7992a215401c`.
Repro script (read-only, re-runnable): `.ufo/waves/round-35/falsify/F35ReopenS106S107/repro.sh`
— `bash .ufo/waves/round-35/falsify/F35ReopenS106S107/repro.sh` (exit 1 = defect found).

---

## Verdict in one line

The **coverage** and **freshness** claims of S106 and S107 hold completely — every digest, anchor
line, quoted span and the "fifteen requirement bullets" teaches cell verify byte-for-byte against a
fresh fetch. But the two rows carry a **metadata defect**: their `(N words)` parentheticals
disagree with the lane's own canonical word counter, and both were **introduced by this round**
(the registry had zero such mismatches before it). Neither defect changes any quote, digest,
location or claim, and neither breaks the frozen predicate.

---

## What I attacked, and the evidence that would have shown disagreement

| # | Attack | Command | Result |
|---|---|---|---|
| 1 | Do the pinned digests still equal the live upstream bytes? | `curl -sSL` of the three pinned raw URLs + `sha256sum` | **agree** — all three equal the manifest |
| 2 | Do the capture files still match their manifest digests? | `sha256sum -c SHA256SUMS` in `corpus/evidence/round35/tb2-eval/` | **agree** — 6/6 `OK` |
| 3 | Are the rows' anchor quotes verbatim on the *cited line* of the fresh fetch? | repro step 3 | **agree** — 3/3 verbatim |
| 4 | Is the `(N words)` parenthetical equal to the lane's canonical counter? | repro step 4 vs `len(text.split())` | **DISAGREE** — S105 9≠11, S107 16≠15 |
| 5 | Does S107's teaches cell ("fifteen requirement bullets") match the file? | repro step 5 | **agree** — exactly 15 |
| 6 | Are the entry's 22 `## Located quotes` rows verbatim on fresh bytes? | repro step 6 | **agree** — 22/22, 0 not-verbatim |
| 7 | Has upstream drifted from the pin (freshness)? | pinned vs `main` byte-compare | **agree** — no drift |
| 8 | Do the frozen counters still hold? | `round35_c1_verify.py`, `defect_ledger.py` | **agree** — C1 pass, C2 pass |

---

## 1. Coverage: digests, anchors, quotes — all hold

### 1.1 Fresh fetch vs manifest (`repro.sh` steps 1–2)

```
tests/test.sh          http=200 bytes=631  sha256=9ede46648fc67c9ce61975503de3e0fcff0b0fb110adc0f9e1d240a608c267b5
instruction.md         http=200 bytes=2655 sha256=1bb2af1d85e9a823a8ae7273a87df8a3f67e2c93b06cddf34f0051a8b003f7c5
tests/test_outputs.py  http=200 bytes=3847 sha256=44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582

=== MANIFEST sha256sum -c ===
test_outputs.py: OK
test.sh: OK
instruction.md: OK
task.toml: OK
antibody.fasta: OK
pdb_ids.txt: OK
```

S106's pinned digest `9ede4664…` and S107's `1bb2af1d…` are exactly the strings carried in the
`corpus/SOURCES.md` anchor cells and in `corpus/evidence/round35/tb2-eval/SHA256SUMS`. The pinned
commit is real and dated: GitHub API for `2fd12b88aafdd04a52c298e3940bcb189f9766d6` returns
`sha: 2fd12b88aafdd04a52c298e3940bcb189f9766d6`, `date: 2026-04-30T05:53:30Z`,
`msg: Add task metadata to task manifests`.

### 1.2 The rows' anchor quotes sit on the cited lines of the *fresh* bytes

`repro.sh` step 3 checks the quoted span against the freshly-downloaded file (not the capture):

```
S106 tests/test.sh:27 verbatim=True  'echo 1 > /logs/verifier/reward.txt'
S106 test.sh:21 (continuation form) verbatim=True  '-w biopython==1.85'
S107 instruction.md:29 verbatim=True  'The GS linkers between different subproteins should be between 5 and 20 amino acids long.'
```

The raw lines:

```
$ sed -n '27p' test.sh     → '  echo 1 > /logs/verifier/reward.txt'
$ sed -n '21p' test.sh     → '  -w biopython==1.85 \'
$ sed -n '29p' instruction.md → ' * The GS linkers between different subproteins should be between 5 and 20 amino acids long.'
```

### 1.3 The entry's quotes citing them — all 22 verbatim on fresh bytes

`repro.sh` step 6 verifies every row of `corpus/knowledge/tb2-protein-assembly-grader.md`
`## Located quotes` against the fresh fetch (the landed V3 check uses the *captures*, so this is
strictly stronger):

```
quoted rows checked against fresh bytes: 22, not-verbatim: 0
```

Including the three that bear on my seat: `test.sh:21` (`-w biopython==1.85 \`),
`test.sh:27` (`echo 1 > /logs/verifier/reward.txt`), `test.sh:29`
(`echo 0 > /logs/verifier/reward.txt`), and `instruction.md:29`.

### 1.4 S107's teaches cell — "fifteen requirement bullets" is exact

`repro.sh` step 5 counts the bullets in the fetched `instruction.md`:

```
bullets in instruction.md = 15  (row claims fifteen)
  10, 12, 14, 16, 20, 21, 22, 24, 25, 27, 28, 29, 30, 32, 33
```

15 bullet markers, and the row's parenthetical enumeration maps onto them one-for-one:
file shape (10), allowed parts (12), PDB/`pdb_ids.txt` (14), antibody binder (16),
plasmid/`plasmid.gb` (20), no start/stop codons (21), N-terminal Met (22), linker separation (24),
FPbase/filter cube (25), no termini linkers (27), linker between subproteins (28), linker 5–20 aa (29),
GC windows (30), 3000-nt cap (32), part order (33). **The "fifteen" claim is correct.**

### 1.5 S106's teaches cell — also exact

"the reward is binary (1 iff pytest exits 0) and the grader runs under uvx with Python 3.13,
pytest 8.4.1 and biopython 1.85" — matches `test.sh:18-23` (`uvx -p 3.13 -w pytest==8.4.1
-w biopython==1.85`) and `test.sh:26-30` (`if [ $? -eq 0 ]; then echo 1 … else echo 0`).

---

## 2. Freshness: no upstream drift

`repro.sh` step 7 byte-compares the pinned commit against upstream `main`:

```
tests/test.sh      main == pinned (no upstream drift)
instruction.md     main == pinned (no upstream drift)
```

All three pinned files are byte-identical at `main` today; the pin is current, not stale. The
`recheck: 180d` cadence in the entry head and the `recheck` cell of all three rows are consistent
with a commit that has not moved since 2026-04-30. The probe receipt also reproduces byte-for-byte:

```
$ uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane . > probe.out
$ diff probe.out corpus/evidence/round35/tb2-grader-probe.txt   → no output (identical)
cases=18 observed_pass=5 observed_fail=13 mismatches=0
```

---

## 3. DEFECT: the `(N words)` parentheticals are wrong in S105 and S107

### 3.1 The observation

`corpus/SOURCES.md` rows 120 and 122 carry parenthetical word counts. Compared against the
lane's own canonical counter — `plans/sources_adopt.py:280-281` and `plans/round30_defects.py:39-40`,
both `def words(text): return len(text.split())`, with the source comment *"a word count printed by
this gate cannot disagree with one in a round's defect receipt"* — two rows disagree:

```
MISMATCH S105: claimed=9 canonical(len split)=11  'assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx, ('
MISMATCH S107: claimed=16 canonical(len split)=15  'The GS linkers between different subproteins should be between 5 and 20 amino acids long.'
mismatching parentheticals in the whole registry: 2
```

All 22 other counted rows in the registry agree exactly with `len(text.split())`, including the
three also opened this round (`S077` 15/15, `S091` 18/18, `S090` 18/18 and 11/11, `S081` 22/22
6/6 18/18, `S082` 11/11 17/17, `S092` 9/9 9/9 10/10, `S093` 8/8 5/5, `S100` 6/6, `S103` 11/11,
`S104` 8/8 20/20 6/6). The convention is therefore unambiguous and the two outliers are the
round's own new rows.

### 3.2 Provenance — each miscount has a mechanical cause

**S107 (16 vs 15).** The cited line is a markdown bullet, so the *whole line* is 16 whitespace
tokens while the *quoted span* is 15. The drafter counted the source line, not the quote:

```
line29 repr: ' * The GS linkers between different subproteins should be between 5 and 20 amino acids long.'
quote words (len split) = 15
line29 words (len split) = 16   <- includes the bullet marker "*"
```

The wave-1 draft shows the same slip: `.ufo/waves/round-35/build/R35RowsDraft.md:29` records
`→ 29: * The GS linkers … long.` **(16 words)** — the grep line, not the quote. The quote text
itself is verbatim on line 29 (confirmed in §1.2), so the number is a counting artefact.

**S105 (9 vs 11).** The quote ends `…, snap_idx, (` — an open call-bracket. Counting the quote
without the trailing `, (` gives 10; the draft's own note (`R35RowsDraft.md:25`) records the grep
line `42:    assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx, ( (9 words)`.
Neither 9 nor 11 is the canonical count of the quoted span — the canonical count is **11**
(`assert`, `flag_idx`, `<`, `donor_idx`, `<`, `dhfr_idx`, `<`, `acceptor_idx`, `<`, `snap_idx,`, `(`).

Both miscounts are **off in the safe direction for the ≤25-word cap** (both quotes are ≤25 words
under any counting), so neither can breach SOURCES contract v1 rule 1 (QUALITY Q3).

### 3.3 This round introduced the defect

```
$ git show 4fe72a9^:corpus/SOURCES.md | <count check>
pre-round (4fe72a9^) rows_with_count=21 mismatches=0
$ git show 4fe72a9:corpus/SOURCES.md | grep -o 'tests/test_outputs.py:[0-9]* "[^"]*" ([0-9]* words)'
tests/test_outputs.py:42 "assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx, (" (9 words)
```

The pre-round registry had **0/21** mismatches; the round-35 admit commit `4fe72a9` introduced
both. The miscount persisted through every subsequent commit (`7d89c23`, `ddb997f`, `0cbfabd`,
`346850e`, `5665913`, `4fe72a9`, `368d908`) and is present at the landing tip.

### 3.4 Why no gate caught it

- `scripts/sources-census.sh` has **0** occurrences of `words` — it never inspects the parenthetical.
- `plans/round35_c1_verify.py` V2 checks cell count, URL, tier/status/opened and used-by only; it
  never reads the anchor cell's quotes or their counts (lines 82-99).
- V3 checks the *entry's* `## Located quotes` table for ≤25 words, but the row anchor cells in
  `corpus/SOURCES.md` are not covered by any check.

So the landed predicate is blind to this class. That is the falsification-relevant point: the
counter proves the quotes are ≤25 words, not that the *stated* counts are right.

### 3.5 Severity — cosmetic, not claim-breaking

Neither count is load-bearing:

- The **quote text** is verbatim on the cited line (both).
- The **sha256** is correct (both).
- The **location** (`tests/test.sh:27`, `:21`, `instruction.md:29`) is correct (both).
- The **≤25-word cap** holds under every counting (11 and 15, and even the claimed 9 and 16).
- The **teaches** cells are correct (both, §1.4/§1.5).
- No entry sentence, probe prediction or scored claim depends on the parenthetical.

This is a registry-metadata defect, not a sourcing defect. It should be corrected by rewriting the
two parentheticals to the canonical count (S105 → 11, S107 → 15) — a one-cell edit — but it does
**not** invalidate C1, and it does not touch S106, whose `(4 words)` is correct.

**Note on scope:** S105 is row 120 and outside my seat's named rows (S106/S107), but it is the
same defect in the same round's row set and the same one-line edit; I report it here because the
two are a single root cause. A sibling seat (`F35ReopenS105`) may cover S105's quotes
specifically.

---

## 4. Frozen predicates — unaffected

Run read-only in the lane at the working tree, and separately in a clean fixture clone at the
landing tip (per the fixture rule: `mktemp -d`, `git clone --no-checkout --shared`,
`sparse-checkout set --no-cone`, `checkout dfee6fff…`, `rev-parse --show-toplevel` verified
before use; the clone was removed afterwards).

At the landing tip `dfee6fff631ebc5f623ba4506e5c7992a215401c` in the fixture clone:

```
V1 ok
V2 ok
V3 ok
V4 ok
V5 ok
V6 ok
checks=6 defects=0
PREDICATE C1 pass
```

In the live lane:

```
checks=6 defects=0
PREDICATE C1 pass
rows=5 closed=5 observed_pass=5 mismatches=0
PREDICATE C2 pass
```

(The live working tree carries an uncommitted `## Errata` section appended to
`corpus/knowledge/tb2-protein-assembly-grader.md` and a `corpus/README.md` line by a falsify-wave
sibling seat; the C1 counter still passes with that text present, so the errata does not break
the predicate. I did not touch either file.)

---

## 5. Coverage/freshness score for this seat

| Axis | Score | Basis |
|---|---|---|
| Coverage | **full** | 3/3 pinned digests equal manifest and live bytes; 3/3 anchor quotes verbatim on the cited line of the fresh fetch; 22/22 entry located-quotes verbatim on fresh bytes; "fifteen requirement bullets" exact; S106 and S107 teaches cells exact |
| Freshness | **full** | pinned bytes identical at upstream `main` for all three files (no drift); pinned commit dated 2026-04-30 and still current; probe receipt reproduces byte-for-byte; `recheck: 180d` consistent |

## 6. Remaining unknowns / not run

- `git ls-remote` against the upstream repo was not used; the commit's existence was confirmed via
  the GitHub REST API for the commit SHA instead (HTTP 200, sha/date/message echoed above).
- The `## Located quotes` check in step 6 re-fetches only the three files this seat covers;
  `test_outputs.py` was included, so all 22 rows were in fact checked against fresh bytes.
- No lane file was written by this seat. The only artifact is this report and its `repro.sh`
  helper, both inside `.ufo/waves/round-35/falsify/F35ReopenS106S107/`.

VERDICT: s106s107-defect
