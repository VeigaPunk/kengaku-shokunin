author: kengaku (L1 KengakuR94, hyaku run 15 attempt 1)

# Kengaku round 94 — lesson

Lane `kengaku-shokunin`, branch `master`. Base `0cbb9279` (round 93 admitted, MANIFEST 1388);
P0 mechanism predictions + capture `bdcb1ec0`; instruments P1 `997a6fe5`; pre-freeze controls P2
`74b3d2a1`; frozen claims F `844c504e` (`plans/round-94-claims.md`, 11-row
`frozen-instruments` table); official receipt, ledger flip and SOURCES C `90c7677f` = measured tip
T; L1 receipts at T `242b3669`. Wave evidence: `.ufo/waves/round-94/w1/`.

## Round-93 spot-check routed defects — disposition

| # | routed defect (round-93 spot-check §6) | round-94 disposition |
|---|---|---|
| 1 | freeze-integrity registry row in `SKILL.md` | done: `SKILL.md` `## Gate/probe registry` row `freeze-integrity` (v2 current, v1 superseded) |
| 2 | capability row into `SCORECARD.md` `## Capabilities` | done: `freeze-integrity gate` row (first-working 93; v2: 94) |
| 3 | W-1/W-4/M4: seat forgeries and m06/m13 as committed controls under a new frozen predicate | **claimed (R94-C2)**: `.ufo/waves/round-94/L1/controls/c2-false-*.txt`, each red at its designated fixture |
| 4 | W-2 `--full-history`; W-3 second block; W-6 duplicate rows / freeze selector / W3 comment | **claimed (R94-C2)**: gate v2 `plans/round94_freeze_integrity.py`; W4 selector = the single add commit (more than one fails the leg) |
| 5 | W-5: C1 L7 member set, not aggregates | done in the R94-C1 counter L7 (set vs BASE); control `controls/c1-forgery-member-swap.txt` |
| 6 | counter echoes the `SELFTEST` line | done: R94-C2 W3 `W3 echo SELFTEST cases=15 ok=15` |
| 7 | carried round-92 #2/#3/#4/#6 | not claimed; still open, carried to round 95 with the same pointers |

The round-93 spot-check §4 recorded no disagreement (4/4 agree), so no discernment criterion is
owed from it.

## Gate

Candidates opened this round (CORPUS rule 1: each row written only after its source was opened
here; every fetch HTTP 200 on 2026-11-05 from raw.githubusercontent.com at
`2fd12b88aafdd04a52c298e3940bcb189f9766d6`).

| candidate | decision | access | located quote and location | reason | flip |
|---|---|---|---|---|---|
| S297 `write-compressor/tests/test_outputs.py` (member replay only) | **admit** (tier A) | 2026-11-05, HTTP 200, 2427 B, sha256 `809f4860…384e2`, byte-identical to the lane's round-52 capture | line 15: `subprocess.run(["gcc", "-o", "decomp2", "decomp.c"], check=True)` (5 words); `max_size_bytes = 2500` at :63 | the three functions this round's twelfth offline replay grades: every one calls `setup()`, which overwrites `/app/decomp.c` and `/app/data.txt` from `/tests` and rebuilds `decomp2` without `-O`; the round-trip uses `text=True`, so a corrupted stream raises `UnicodeDecodeError` (C08) instead of failing its assertion | a claim about the TB2 harness or a real agent submission needs its own receipt |
| S298 `write-compressor/tests/original-decomp.c` (member replay only; byte-identical to `environment/decomp.c`) | **admit** (tier A) | 2026-11-05, HTTP 200, 1262 B, sha256 `7f8d9ef6…f62a`, equal to `write-compressor/environment/decomp.c` (HTTP 200, same sha256) | line 75: `printf("%s", buf);` (2 words) | the decoder both the task image and the grader build, and so the format a `data.comp` must satisfy; it prints an uninitialised 10000-byte stack buffer with `%s`, so on this host the `-O3` build emits 4870 B for the reference stream and the grader's plain build 4868 B (`corpus/evidence/round94/decomp-opt-divergence.txt`) | a claim about the task image's own `-O3` build output needs its own receipt |
| S299 `write-compressor/tests/original-data.txt` (member replay only; byte-identical to `environment/data.txt`) | **admit** (tier A) | 2026-11-05, HTTP 200, 4868 B, sha256 `0fc483d0…4fa4e`, equal to `write-compressor/environment/data.txt` (HTTP 200, same sha256) | line 1: `In information theory, data compression, source coding,[1] or bit-rate reduction` (10 words; the row first stated 9 — corrected after T, lesson M1) | the 4868-byte text the round-trip must reproduce and the reference compressor reads; raw text as `data.comp` is 4868 B: it exists, does not round-trip, and breaks the 2500-byte wall (C03) | a claim about the corpus of texts the compressor could be pointed at needs its own fetch |
| S300 `write-compressor/solution/solve.sh` (member replay only) | **admit** (tier A) | 2026-11-05, HTTP 200, 24841 B, sha256 `01550b7d…b409`; heredoc body byte-equal to `write-compressor/environment/main.rs` (sha256 `fa53d657…ab389`) | line 4: `cat <<'EOF' > main.rs` (4 words); `rustc main.rs -o main` at :732 | the task author's compressor: the replay's positive control and the base of its derived variants; rebuilt offline with host rustc 1.99.1 it yields a 2264-byte `data.comp` (sha256 `3a905a56…9131`) that passes all three functions (C01), and +300 zero bytes still round-trips but fails the size wall (C06) | a claim about the shipped `main.rs` binary or the host rustc version needs its own receipt |
| S301 `write-compressor/tests/test.sh` (verifier wrapper) | **reject** | 2026-11-05, HTTP 200, 608 B, sha256 `4770437e…c334`, byte-identical to S294's `schemelike-metacircular-eval` wrapper | line 3: `# Install curl` (3 words) | REJECTED: installs curl and uv over the network and runs pytest under uvx on Python 3.13; the offline replay calls the three functions directly; same bytes as S294, so the wrapper is shared across members | a verifier-harness claim with the network legs pinned |
| S302 `write-compressor/environment/Dockerfile` (task image recipe) | **reject** | 2026-11-05, HTTP 200, 283 B, sha256 `9a583d29…93b` | line 8: `RUN gcc -O3 decomp.c -o /app/decomp` (6 words) | REJECTED as an input: apt-get over the network and a docker build; the probe stages the captured files instead. Kept as the pointer for the `-O3` vs grader-build divergence | a task-image build claim with the network legs pinned |

Round-start census: exit 0, `kengaku ok`, 288 registry rows (`.ufo/waves/round-94/L1/census-start.txt`).
Round-end census: exit 0, `kengaku ok`, 294 rows (`.ufo/waves/round-94/L1/census-end.txt`). Anchor gate
(Q76) on the landing tree: `ANCHORLINE rows=294 cited=104 captured=91 uncaptured=13 defective=10 repaired=10 live=0 cells=0`,
rc 0 (`.ufo/waves/round-94/L1/anchorline-end.txt`); at T it was `live=1` (S299, Mistake M1). Assimilation: none (`merge/kengaku/` held by L0 `kengaku | round-54`).
considerthese: none taken — the 2026-11-05 file's proposal 2 (root of trust outside the lane's
commits) is the gate's residual named again below; not implemented.

## Mistakes

Class · evidence pointer · captured-by · fix.

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | **hand-counted word count in a SOURCES quote cell** (the round-93 W-7 class, recurring) | S299 written at C `90c7677f` with "(9 words)"; the quote has 10 whitespace tokens. At T `python3 plans/anchor_line_check.py --lane .` → `ROW S299 state=live defects=words:1`, `live=1`, rc 1 (BASE: `live=0`, rc 0); `plans/round91_f1_counter.py` flips to fail (wave ScribeQuality SQ-1, `.ufo/waves/round-94/w1/ScribeQuality/receipts/receipt-s299-wordcount.txt`) | `plans/anchor_line_check.py` — an existing lane gate the L1 did not run before committing the rows | cell corrected to "(10 words)" after T (a SOURCES curation cell, not a tabled instrument); `anchor_line_check` back to `live=0 cells=0` rc 0 and `R91-F1 pass` rc 0 at the landing tip. QUALITY Q76 makes the gate run a precondition of any SOURCES commit. Shown able to fail: it went red at T |
| M2 | **author-chosen fixture set bounds the counter's discrimination** (round-93 M4, one level up) | before P1, the draft counter's own W5 showed K2 and K6 `SURVIVED` (designated fixtures that did not discriminate; `.ufo/waves/round-94/L1/c2-dryrun1-reproduced.txt`, draft bytes `c2-counter-dryrun1-prefix.py`) — fixed before P1. After T, non-author seats built ≥ 9 new false gates that pass the frozen counter 5/5 (ExecC2Rerun F1–F7: paths-mode absent/duplicate entries, rename, spaced row, octopus merge, delete-and-re-add, rc remap; CriticClaims C2-F1 stubbed battery; MutTesterGate M20 battery red but concealed) | pre-P1: W5's designated-fixture rule; post-T: none in the lane (non-author wave only) | routed to round 95 under a new frozen predicate: W2 gains paths-mode, rename, octopus, delete/re-add and spaced-row fixtures, W3 must run the battery's fixtures itself rather than read the gate's echo, and every wave-built false gate becomes a committed control. Not yet shown able to fail |
| M3 | **mechanism-derived prediction refuted** (Q74 working as intended) | P0 `predictions-mechanism.txt` C08 `P,F,P,2264`; dry runs observed `P,E:UnicodeDecodeError,P,2264` (`dryrun-1.txt`, `dryrun-2.txt`): the grader's `subprocess.run(..., text=True)` raises on the corrupted output | Q74 (only observed vectors are frozen; the refuted hypothesis is written beside them) | frozen as observed with the refutation in the case `why`; 7 of 8 mechanism predictions held. Shown able to fail: the C08 prediction itself |
| M4 | **shell job scoping sent a measurement to the wrong cwd** | the first `c2-tip.txt` run was a backgrounded group whose `cd` applied to its sibling only: `python3: can't open file '/home/vgpnk/Projects/shokunin/plans/round94_c2_counter.py'`, rc 2 | the counter's own rc 2 (could-not-evaluate is never a pass) | re-run from inside the clone (`git rev-parse HEAD` printed first, = T); the committed `c2-tip.txt` is that run. Lesson: one measurement per command, cwd asserted in the receipt |

## Honest limits of this round's evidence

- The C1 replay grades lane-built inputs against the captured grader bytes on this host
  (Python 3.14.8, gcc 16.2.1, rustc 1.99.1); the TB2 image uses Ubuntu 24.04's toolchain. The
  captured decoder prints an unterminated stack buffer (`decomp.c:75`), so outputs depend on
  codegen: ExecC1Rerun measured gcc `-O3` flipping 3 of 8 vectors (C01 fails round-trip) and clang
  flipping C07's tail bytes; at the grader's pinned `gcc -o decomp2 decomp.c` the vectors held in
  four full runs. The claim is "at the pinned compile on this host".
- C08's `UnicodeDecodeError` depends on a UTF-8 locale (bwrap inherits the environment; L9 does
  not pin LANG; SentinelProbe SP-2). Minimal and padded environments gave identical blocks.
- The freeze-integrity gate trusts the lane's git object view: a `refs/replace` object hides an
  edit-then-revert (CriticClaims C2-F2), and only the exact three-backtick fence is a table block
  (C2-F3). The lane holds zero replace refs and one fence per claims file at F and T.
- R94-C2's 5 → 0 is the frozen measure over the five false gates recorded by round 93; the critic
  rules the count confounded (each of the five is also red on v2-only fixtures and on W3) and the
  wave shows the counter's discrimination still narrower than its fixtures (M2).

## Wave w1 findings (non-author seats; routed to round 95, never repaired in round)

12 seats dispatched (`.ufo/waves/round-94/w1-results.json`); 9 reported, **3 dead**: ScoutSources
(scout), ReviewerC1 and ReviewerC2 (reviewer) returned empty final output and wrote no file; they
stay dead in the evidence and are not replaced. No tabled file changed after F (CriticClaims,
SentinelProbe: 11/11 sha256 at T equal the F table; ExecFreezeCensus: v2 on the round-94 window
11/11 intact).

| id | seat | severity | finding | effect on a verdict at T |
|---|---|---|---|---|
| W-1 | CriticClaims verdicts | — | R94-C1 "verifies, narrowed" (golden-file reproduction; P0 predictions not part of the predicate); R94-C2 "does not verify as calibration" (5 → 0 confounded and in-sample) | predicates pass at T (critic reproduced both, rc 0) |
| W-2 | ExecC2Rerun F1–F7 | major | seven new false gates built on v2 pass the counter 5/5 (paths-absent dropped, rename intact, spaced row dropped, octopus `-s ours`, delete-and-re-add, `--paths c.py c.py` rc 0, CNE remapped to rc 1) | none at T (W1/W4 windows: 0 merges, 0 renames, 0 deletes) |
| W-3 | CriticClaims C2-F1; MutTesterGate M20 | major | W3 reads the gate's printed `SELFTEST` line: a stubbed battery passes 5/5; a red battery with a forged ok line passes 5/5 | none at T (the real battery is 15/15; the real gate is the one measured) |
| W-4 | CriticClaims C2-F2, C2-F3; ConnectorOverlap R-N1 | major (latent) | replace refs hide history; four-backtick/tilde fences are not table blocks | none at T (0 replace refs; one fence) |
| W-5 | MutTesterGate | minor | 20 gate mutants: 11 killed, 9 survive (paths-dup guard, unterminated block, predicate line unpoliced, battery non-fatal/concealed; 3 with equivalence arguments) | none at T |
| W-6 | MutTesterC1 | major | 14 counter mutants: 6 killed, all by committed controls; m03+m04 jointly false-pass a forged receipt hiding five failing cases; m11 false-passes a probe swap with a regenerated receipt; m10 a foreign LANE_TIP; the T run kills nothing (every C1 control is P1-based, so receipt-side legs never run in their positive direction) | none at T |
| W-7 | ExecC1Rerun-1/-2; CriticClaims C1-F4 | major (scope) | C01 is compile-dependent (`-O3` fails it); clang flips C07's tail bytes | none at the pinned compile (four runs identical) |
| W-8 | CriticClaims C1-F2 | minor | dry-run-1 probe bytes `6c820857…` exist in no commit; "dry runs 1–3" names an uncommitted third run | none; P0 precedes both committed dry-run receipts (LANE_TIP stamps) |
| W-9 | ScribeQuality SQ-1 | major (conformance) | S299 word count (lesson M1) | none on C1/C2 (no round-94 counter reads SOURCES); fixed after T |
| W-10 | ScribeQuality SQ-3 | minor | gate v2 accepts a `--work` inside the lane | none |
| W-11 | SentinelProbe | info / minor | sandbox proven: no host writes, no AF_INET sockets in 43,069 traced events; SP-2 the probe inherits the operator env (273 vars) | none |
| W-12 | ExecFreezeCensus | info | v2 reproduces the v1 census for rounds 85–93 exactly; no historical verdict changes (every window linear, 0 merges) | report-only |
| W-13 | ConnectorOverlap | info | no sibling replays TB2 graders; kaidoku owns a mechanism-duplicate freeze/full-history family (complement, cross-cite); mado's freeze-order gate reads a reverted edit as OK where v2 counts it (explicit semantic fork) | adjacency note |
