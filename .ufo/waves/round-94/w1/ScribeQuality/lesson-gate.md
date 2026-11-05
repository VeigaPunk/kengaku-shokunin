# ScribeQuality — draft round-94 lesson `## Gate` block (S297–S302)

Seat ScribeQuality (leaf scribe). Draft only; the L1 integrates into
`corpus/lessons/round-94.md` (that file does not exist yet at the tip). Every value below is
taken from the SOURCES row it cites and checked against the lane capture; the check receipts
are `receipt-sources-s297-s302.txt` (sha256 / byte count / quote line / word count / quote
substring) and `receipt-s299-wordcount.txt`.

## Proposed text

```markdown
## Gate

Candidates opened this round (CORPUS rule 1: each row written only after its source was opened
here; every fetch HTTP 200 on 2026-11-05 from raw.githubusercontent.com at
`2fd12b88aafdd04a52c298e3940bcb189f9766d6`).

| candidate | decision | access | located quote and location | reason | flip |
|---|---|---|---|---|---|
| S297 `write-compressor/tests/test_outputs.py` (member replay only) | **admit** (tier A) | 2026-11-05, HTTP 200, 2427 B, sha256 `809f4860…384e2`, byte-identical to the lane's round-52 capture | line 15: `subprocess.run(["gcc", "-o", "decomp2", "decomp.c"], check=True)` (5 words); `max_size_bytes = 2500` at :63 | the three functions this round's twelfth offline replay grades: every one calls `setup()`, which overwrites `/app/decomp.c` and `/app/data.txt` from `/tests` and rebuilds `decomp2` without `-O`; the round-trip uses `text=True`, so a corrupted stream raises `UnicodeDecodeError` (C08) instead of failing its assertion | a claim about the TB2 harness or a real agent submission needs its own receipt |
| S298 `write-compressor/tests/original-decomp.c` (member replay only; byte-identical to `environment/decomp.c`) | **admit** (tier A) | 2026-11-05, HTTP 200, 1262 B, sha256 `7f8d9ef6…f62a`, equal to `write-compressor/environment/decomp.c` (HTTP 200, same sha256) | line 75: `printf("%s", buf);` (2 words) | the decoder both the task image and the grader build, and so the format a `data.comp` must satisfy; it prints an uninitialised 10000-byte stack buffer with `%s`, so on this host the `-O3` build emits 4870 B for the reference stream and the grader's plain build 4868 B (`corpus/evidence/round94/decomp-opt-divergence.txt`) | a claim about the task image's own `-O3` build output needs its own receipt |
| S299 `write-compressor/tests/original-data.txt` (member replay only; byte-identical to `environment/data.txt`) | **admit** (tier A) | 2026-11-05, HTTP 200, 4868 B, sha256 `0fc483d0…4fa4e`, equal to `write-compressor/environment/data.txt` (HTTP 200, same sha256) | line 1: `In information theory, data compression, source coding,[1] or bit-rate reduction` (10 words — the SOURCES row states 9; see SQ-1) | the 4868-byte text the round-trip must reproduce and the reference compressor reads; raw text as `data.comp` is 4868 B: it exists, does not round-trip, and breaks the 2500-byte wall (C03) | a claim about the corpus of texts the compressor could be pointed at needs its own fetch |
| S300 `write-compressor/solution/solve.sh` (member replay only) | **admit** (tier A) | 2026-11-05, HTTP 200, 24841 B, sha256 `01550b7d…b409`; heredoc body byte-equal to `write-compressor/environment/main.rs` (sha256 `fa53d657…ab389`) | line 4: `cat <<'EOF' > main.rs` (4 words); `rustc main.rs -o main` at :732 | the task author's compressor: the replay's positive control and the base of its derived variants; rebuilt offline with host rustc 1.99.1 it yields a 2264-byte `data.comp` (sha256 `3a905a56…9131`) that passes all three functions (C01), and +300 zero bytes still round-trips but fails the size wall (C06) | a claim about the shipped `main.rs` binary or the host rustc version needs its own receipt |
| S301 `write-compressor/tests/test.sh` (verifier wrapper) | **reject** | 2026-11-05, HTTP 200, 608 B, sha256 `4770437e…c334`, byte-identical to S294's `schemelike-metacircular-eval` wrapper | line 3: `# Install curl` (3 words) | REJECTED: installs curl and uv over the network and runs pytest under uvx on Python 3.13; the offline replay calls the three functions directly; same bytes as S294, so the wrapper is shared across members | a verifier-harness claim with the network legs pinned |
| S302 `write-compressor/environment/Dockerfile` (task image recipe) | **reject** | 2026-11-05, HTTP 200, 283 B, sha256 `9a583d29…93b` | line 8: `RUN gcc -O3 decomp.c -o /app/decomp` (6 words) | REJECTED as an input: apt-get over the network and a docker build; the probe stages the captured files instead. Kept as the pointer for the `-O3` vs grader-build divergence | a task-image build claim with the network legs pinned |
```

## Where each value comes from, and what the check found

Every cell above is copied from the SOURCES row it cites, then re-checked against the lane
capture at `corpus/evidence/round94/graders/write-compressor/`. The check is mechanical:
sha256 of the capture file vs the row's `sha256` token; byte count vs the row's `B`; the
row's cited line vs the line holding the quote; the row's `(N words)` vs
`len(quote.split())`; and the quote as a substring of the cited line.

| row | sha256 | bytes | quote line | word count | quote on that line |
|---|---|---|---|---|---|
| S297 | MATCH | MATCH | 15 ✓ | 5 = 5 ✓ | ✓ |
| S298 | MATCH | MATCH | 75 ✓ | 2 = 2 ✓ | ✓ |
| S299 | MATCH | MATCH | 1 ✓ | **9 ≠ 10 ✗** | ✓ |
| S300 | MATCH | MATCH | 4 ✓ | 4 = 4 ✓ | ✓ |
| S301 | MATCH | MATCH | 3 ✓ | 3 = 3 ✓ | ✓ |
| S302 | MATCH | MATCH | 8 ✓ | 6 = 6 ✓ | ✓ |

Secondary locators also checked: S297's `max_size_bytes = 2500` is at `:63` of the grader
(`max_size_bytes = 2500  # As specified in task.yaml`); S300's `rustc main.rs -o main` is at
`:732` of `solve.sh`. S300's heredoc body is byte-equal to `environment/main.rs`
(sha256 `fa53d6572fca95903e30d2d953f1e428bb8b63513ff218ebee9bc60a425ab389`, 24564 B, both
sides) — recomputed here, not taken on trust. S298's `environment/decomp.c` and S299's
`environment/data.txt` carry the same sha256 as their `tests/` twins.

The `reason` column for S297–S302 is the SOURCES `teaches` cell, quoted with the row's own
scope wording. The corroborating measurements are the round's own committed receipts:
`corpus/evidence/round94/compressor-probe.txt` (C01 `P,P,P,2264`, C03 `P,F,F,4868`,
C06 `P,P,F,2564`, C08 `P,E:UnicodeDecodeError,P,2264`, `mismatches 0`) and
`corpus/evidence/round94/decomp-opt-divergence.txt` (`d_o3 output_bytes=4870`,
`d_o0 output_bytes=4868`).

## SQ-1 — the one mismatch, stated plainly

**S299's `(9 words)` cell is wrong; the quote has 10 whitespace tokens.**
`In information theory, data compression, source coding,[1] or bit-rate reduction` splits
as `In` `information` `theory,` `data` `compression,` `source` `coding,[1]` `or` `bit-rate`
`reduction` = 10. The lane's convention is the whitespace-token count
(`plans/anchor_line_check.py`: `declared != len(q.split())` → a `words` defect; the same
convention `plans/sources_adopt.py:words()` uses).

Consequence, measured at the tip:

```
$ python3 plans/anchor_line_check.py --lane .          # in the lane
ROW S299 state=live defects=words:1
ANCHORLINE rows=294 cited=104 captured=91 uncaptured=13 defective=11 repaired=10 live=1 cells=1
rc=1
```

At BASE (`0cbb9279`) the same command printed `live=0 cells=0`, rc 0
(`receipt-s299-wordcount.txt`). The defect therefore entered with this round's C commit
`90c7677f`, which added S297–S302.

Two consequences the L1 must weigh, both exact:

1. `plans/round91_f1_counter.py --lane . --work DIR` — an admitted lane counter that
   requires `live=0` — now prints `DEFECT FULL-CHECK rc=1 … live=1 cells=1` and
   `PREDICATE R91-F1 fail`, rc 1, where at BASE it printed `PREDICATE R91-F1 pass`, rc 0
   (`receipt-s299-wordcount.txt`). That counter is not one of round 94's two claims and
   nothing in `plans/round-94-claims.md` reads it, so **neither R94-C1 nor R94-C2 is
   flipped** by this defect (both counters were re-run at T and pass: `receipt-c2-at-T.txt`,
   and the C1 receipt is the L1's committed `c1-tip.txt`). It is a lane-hygiene regression
   at the tip, not a claim verdict.
2. The defect is *not* in the freeze-integrity table and does not touch any of the 11
   tabled instruments (`plans/round-94-claims.md`'s table lists only `plans/` instruments and
   the six `corpus/evidence/round94/graders/write-compressor/` captures), so the round's
   frozen rule is untouched by the fix.

The repair the lane's own rules require is a **new superseding row**, not an in-place edit:
CORPUS rule 2 ("Only `status`, `recheck` and `used-by` change in place … A correction is a
new row whose `teaches` opens `supersedes S0NN —`") and QUALITY Q34 (same rule, "an in-place
change is a rule-2 defect even when the round wrote the row itself and the cell it corrects
is its own anchor"). I verified that path end-to-end in a scratch clone
(`receipt-s299-supersede-repair.txt`): appending one row `S303` whose `teaches` cell opens
`supersedes S299 —`, carrying the identical located quote with the count corrected to 10,
takes the gate to `ROW S299 state=repaired by=S303` and
`ANCHORLINE … defective=11 repaired=11 live=0 cells=0`, rc 0.

Note the lane's own precedent for this exact shape: round 92's M1 (`corpus/lessons/round-92.md`)
found three miscounted word cells in the first C-commit registry rows (S283 said 5 for 4,
S285 9 for 6, S287 9 for 7) and corrected them **in place** at `d1ccf56d`; round 93's W-7
found the same class again in its own rows and was "corrected in round (lesson and same-round
SOURCES rows; neither is an instrument)". Both are recorded, so the L1 has both precedents
available — but both are in-place edits of the round's own rows, which Q34 calls a rule-2
defect; the supersede row is the form Q34 and CORPUS rule 2 name. **The L1 decides; this
seat does not repair.** The lesson draft above carries the corrected count (10) with the
discrepancy marked, so that the lesson and any superseding row agree.

## Bound on this draft

The Gate block is the round-94 lesson's record of *candidates and their admission*, not a
claim about the instruments. Nothing here claims a C1/C2 verdict; the C1/C2 verdicts are the
L1's frozen claims, and this block's rows are the sources those claims cite.
