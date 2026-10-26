# Round 43 wave 1 — R43ExecNoHarm: no-harm baseline at the receipt commit

Seat `R43ExecNoHarm` (executor, leaf). Lane read-only; measurements in a clean `--no-local` clone detached at the round-43
receipt commit `6b49694d2ff533135fc238a8400f3e0dc1c82026` (ancestor of `master`, verified with
`git merge-base --is-ancestor 6b49694 master` → exit 0). Nothing was written inside the lane, no tool was installed, no
subagent or labrat was used. Axes moved: **operability** (the round-42 measured set still runs end-to-end at this tree and
every prior-round instrument reproduces its recorded bytes) and **calibration** (the two round-43 counters are red exactly
where the freeze control says they must be, and green nowhere they shouldn't be yet).

Script: `.ufo/waves/round-43/build/R43ExecNoHarm/measure.sh` (sha256 `4dda1b4f13c01715e17c3b29308fec33994ee7d0b227bf168081a3ea5d65f55b`),
adapted from `.ufo/waves/round-42/integrate/measure.sh` with the round-43 counters moved to the front and the round-43
frozen digests / `round_close --round 43` added. Receipt:
`.ufo/waves/round-43/build/R43ExecNoHarm/measure-v1.txt` (sha256 `a923af8bd4af54b0e361035719cdef981856a51c479aad073018968b194fe12c`,
92 612 bytes, 1032 lines). Second, narrower receipt: `r43-c2-single-rerun.txt`
(sha256 `6875160ee02e4ba0a1dbcb03c408f5034e58fd221fc28f78cfb2b873d102e8fb`).

## Envelope (QUALITY Q32, both lines verbatim)

Command (scratch `S=/fast/scratch/hyaku/kengaku-r43/R43ExecNoHarm`):

```
S=/fast/scratch/hyaku/kengaku-r43/R43ExecNoHarm
.ufo/waves/round-43/claims/envelope.sh "$S/env" \
  .ufo/waves/round-43/build/R43ExecNoHarm/measure.sh v1 > .../measure-v1.txt 2>&1
```

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r43/R43ExecNoHarm/env /fast/scratch/hyaku/kengaku-r43/R43ExecNoHarm/env --bind /fast/scratch/hyaku/kengaku-r43/R43ExecNoHarm/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/build/R43ExecNoHarm/measure.sh v1
ENVELOPE start 19:12:29 cwd=/home/vgpnk/Projects/shokunin
...
ENVELOPE end 19:23:29 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

`local_bin_content_before = after` (content digest, not names): no PATH directory changed, so the measurement counts; no
re-run needed. Envelope process exit 0, wall 11 min.

Clone facts (`measure-v1.txt:3-6`): `SENTINEL present` · `REC 6b49694…` · `HEAD 6b49694…` · `untracked_in_clone=0`.
The lane worktree itself carries 10 modified / 7 untracked entries (`git status --porcelain`, mostly wave-1 drafts); the
clone is committed bytes only, so none of that enters this baseline.

## Result: 32 green of 36 baseline checks

The baseline is the round-42 measured set (34 command checks + 2 byte-equality comparisons) plus the three round-43 checks
prepended. `exit=` is the command's status; the last column quotes the decisive line, with its line in `measure-v1.txt`.

| # | check | exit | decisive line |
|---|---|---|---|
| 1 | `round43_c1_verify.py --lane .` | **1** | `:19 MUTANTS total=9 killed=0 survived=9 invalid=0 null_detected=0 unattributed=0` |
| 2 | `round43_c2_verify.py --lane .` | **1** | `:47 checks=10 defects=6` · `:48 PREDICATE C2 fail` |
| 3 | `order_check.py` round 43 | 0 | `:55 ORDER RESULT PASS` |
| 4 | `round42_c1_verify.py` | 0 | `:103 MUTANTS total=14 killed=14 survived=0 …` · `:107 PREDICATE C1 pass` |
| 5 | `round42_c2_verify.py` | 0 | `:130 checks=9 defects=0` · `:131 PREDICATE C2 pass` |
| 6 | `order_check.py` round 42 | 0 | `:138 ORDER RESULT PASS` |
| 7 | `round41_c1_verify.py` | 0 | `:214 MUTANTS total=23 killed=23 survived=0 …` |
| 8 | `round41_c2_verify.py` | 0 | `:240 checks=8 defects=0` |
| 9 | `order_check.py` round 41 | 0 | `:248 ORDER RESULT PASS` |
| 10 | `round40_c1_verify.py` | 0 | `:295 MUTANTS total=21 killed=21 survived=0 …` |
| 11 | `round40_c2_verify.py` | 0 | `:318 checks=7 defects=0` |
| 12 | `order_check.py` round 40 | 0 | `:326 ORDER RESULT PASS` |
| 13 | `order_check.py` round 39 | 0 | `:333 ORDER RESULT PASS` |
| 14 | `order_check.py` round 38 | **1** (carried) | `:339 ORDER HIT …control-c2-skip.txt@e0a378539a45:11 kind=gate-p10` · `:341 ORDER RESULT FAIL` |
| 15 | `round39_c1_verify.py` | 0 | `:443 MUTANTS total=7 killed=7 survived=0 …` |
| 16 | `round39_c2_verify.py` | 0 | `:465 checks=7 defects=0` |
| 17 | `round38_c1_verify.py` | **1** (carried) | `:577 MUTANT N21 D5 silence SURVIVED` · `:579 MUTANTS total=22 killed=21 survived=1 …` |
| 18 | `round38_c2_verify.py` | 0 | `:601 checks=7 defects=0` |
| 19 | `round37_c1_verify.py` | 0 | `:726 MUTANTS total=55 killed=55 survived=0 …` |
| 20 | `round37_c2_verify.py` | 0 | `:748 checks=7 defects=0` |
| 21 | `round36_c2_verify.py --lane .` | 0 | `:758 checks=6 defects=0` |
| 22 | `anchor_digest_check.py --lane .` | 0 | `:762 rows=121 tokens=27 defects=0` |
| 23 | `sources-census.sh validate --file corpus/SOURCES.md` | 0 | `:780 file ok …/corpus/SOURCES.md` |
| 24 | `sha256sum -c …/round-43/claims/frozen-digests.txt` | 0 | 12/12 `OK` (`:782-795`) |
| 25 | `sha256sum -c …/round-42/claims/frozen-digests.txt` | 0 | 12/12 `OK` (`:796-809`) |
| 26 | `sha256sum -c …/round-41/claims/frozen-digests.txt` | 0 | 11/11 `OK` (`:810-822`) |
| 27 | `sha256sum -c …/round-40/claims/frozen-digests.txt` | 0 | 11/11 `OK` (`:823-835`) |
| 28 | `sha256sum -c …/round-39/claims/frozen-digests.txt` | 0 | 9/9 `OK` (`:836-846`) |
| 29 | `ledger_tip.py --source <clone> --work` | 0 | `:848 TIP commit=6b49694…` · `:861 rows=9 closed=9 observed_pass=9 mismatches=0` |
| 30 | `tip_receipts.py --lane . --work` | 0 | `:910 receipt corpus/evidence/round43/feal-probe.txt equal bytes=3292 exit=0` · `:913 receipts=29 byte_equal=9 differ=0 skipped=20` |
| 31 | `routed_open.py` | 0 | `:916 ROWS total=16 open=9 blocked=1 closed=6 refused=0` · `:917 routed_open=10 oldest_round=39` |
| 32 | `db_wal_probe.py --lane . --work` | 0 | `:954 cases=28 observed_pass=8 observed_fail=20 mismatches=0` |
| 33 | `constraints_probe.py` byte-equality | 0 | `:956 constraints_probe exit=0 byte_equal=yes` |
| 34 | `fibsqrt_probe.py` byte-equality | 0 | `:957 fibsqrt_probe exit=0 byte_equal=yes` |
| 35 | `round_close.py --round 42` | 0 | `:987 ROUND-CLOSE RESULT PASS exit=0` |
| 36 | `round_close.py --round 43` | 0 | `:1018 ROUND-CLOSE RESULT PASS exit=0` |

Green = exit 0 (for #33/#34, `exit=0` **and** `byte_equal=yes`). **32 of 36 green.** The 55 digest lines across #24-#28
are all `: OK`, zero `FAILED`; every counter's `PINS … mismatched=0` / `PINS-AFTER mismatched=0` holds.

## The four reds, and why none is harm

1–2. **Round-43 counters are red exactly as the freeze says they must be.** No `plans/battery43` exists at this commit
(`git ls-tree 6b49694 plans/battery43` → empty) so C1 builds an empty battery:
`BATTERY fixtures=0 wrong=0 tampered=0 sidechannel=0` (`:18`), `MUTANTS total=9 killed=0 survived=9` (`:19`),
`MUTANTS-BY-TOOL anchor=0/6 order=0/3` (`:20`), `ADVERTISED direct=8 indirect=1 none=0` (`:21`), `PREDICATE C1 fail`
(`:23`) — matching `.ufo/waves/round-43/claims/control-c1-nothing.txt` `killed=0 survived=9`. No corpus entry exists
(`git ls-tree 6b49694 corpus/knowledge/ | grep feal` → 0), so C2 reports `checks=10 defects=6` (`:47`) with V1 V5 V6 V8
green and V2 V3 V4 V7 V9 V10 red — one defect *fewer* than the freeze control `control-c2-nothing.txt` (`checks=10
defects=7`), and the difference is exactly **V8**, which now passes (`:44 V8 ok order_exit=0 result=PASS`), because the
receipt is committed and the claims were frozen before it. That is the expected wave-1 state, not a regression.

14, 17. **Two round-38 reds carried in from the round-42 baseline, byte-identical in kind.** They are red in
`.ufo/waves/round-42/integrate/measure-tip3.txt` at tip `3e8a2e5` (`:284-291` order FAIL on the same
`control-c2-skip.txt@e0a378539a45:11 kind=gate-p10` hit; `:520-529` `MUTANT N21 D5 silence SURVIVED`, `MUTANTS total=22
killed=21 survived=1`). My run reproduces both with the same ids, hit line and counts. They are not caused by anything in
round 43 and are outside this seat's remit (round-38 routed work).

## Notes worth carrying

- **The round-43 receipt already re-runs byte-equal.** `tip_receipts.py` classified
  `corpus/evidence/round43/feal-probe.txt` as `equal bytes=3292 exit=0 doc=plans/feal_probe.py:4+plans/round-43-claims.md:100`
  (`:910`) and `differ=0` overall (`:913`), up from round 42's `receipts=28 byte_equal=8` — the count moved by exactly the
  new receipt. So the committed receipt is reproducible at this tree, and every earlier receipt still is.
- **`round_close --round 43` passes at the receipt commit** (`:1018`), because `round_close` checks the claims file digest,
  receipt presence, order and the census — not the C1/C2 predicates. A green close here must not be read as wave-1
  admission: items 1–2 above are the admission facts. Reported as a scope note, not a defect.
- **Round-43 `order_check` is green on its own merits**: `:52 ORDER scanned commits=1 file_entries=30 distinct_blobs=30` ·
  `:54 ORDER ok no claims file committed at or before the receipt shows the frozen probe executed` (`freeze=02753f26`,
  `receipt_commit=6b49694d`). The 30 claims files (controls, hostile vectors, witness run) trip no P10/`CASE` token.
- **Extra, deliberately outside the 36** (not in the round-42 baseline): `python3 plans/pkg_gate.py package --root .
  --spec plans/pkg-spec-r43.json` → exit 1, `defects=6` (`:1021-1029`), all entry/rows-shaped (P2 included: the raw frozen
  spec carries `"receipt_sha256": null` by design, the counter injects the digest — see row #2's gate block, where P2 is
  `ok receipt_sha256=pinned`). Informational only; excluded from k/n.
- **Determinism spot-check**: the round-43 C2 counter alone, re-run in a second clone under the envelope
  (`r43-c2-single-rerun.txt`, `ENVELOPE start 19:26:45 … end 19:28:24 exit=0 … unchanged`), printed the same
  `V1 … V10` statuses with `P2 ok receipt_sha256=pinned` and `checks=10 defects=6` — the wave-1 red is stable, not flaky.

## Risks / blockers

- This measurement is pinned to the *receipt* commit. `plans/battery43/` is already present and untracked in the lane
  worktree; wave-2 must re-run this script at the landing tip (its printed reds 1–2 are expected to flip only then).
- `round38` items 14/17 stay red until round-38 routed work lands; they should not be attributed to round 43.
- No blocker. Scratch `/fast/scratch/hyaku/kengaku-r43/R43ExecNoHarm` held the clone, the work dirs and the second
  envelope run; it was removed with `plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r43 R43ExecNoHarm <S>`.

VERDICT: no-harm-baseline-32-green-of-36
