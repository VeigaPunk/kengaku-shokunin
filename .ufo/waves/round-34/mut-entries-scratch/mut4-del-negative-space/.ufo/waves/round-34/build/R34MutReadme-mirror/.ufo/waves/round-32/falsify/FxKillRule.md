# FxKillRule — C1 kill-rule reachability and honest-stop branch (round 32)

Seat: `L1Kengaku32.FxKillRule` (UFO-FSD critic, leaf). Date: 2026-10-25.
Target: C1's frozen kill rule (`plans/round-32-claims.md:45-48`), freeze commit `0d32691d`.
Method: synthetic lane mirrors under `/tmp/r32f-FxKillRule/` (≤440 KB, well under the 60 MB cap);
the two frozen C1 counters run against them. No repo bytes modified; read-only git only.

---

## 1. The kill rule under test (frozen text, claims lines 45-48)

> **Kill rule:** a cited source whose located quote cannot be found at the pinned revision is refused
> for that row; if fewer than two of the three survive (S093's round-31 quotes already resolve; S094
> and S097 must resolve this round), the entry is not admitted and C1 is a recorded honest stop
> (registry delta 0).

Frozen predicate (lines 30-38) requires the counter to print
`entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok` and exit 0, and
`plans/round32_c1_verify.py --lane .` to print `checks=6 defects=0`, exit 0. Committed control
`.ufo/waves/round-32/claims/control-nothing.txt` pins the do-nothing line (`entries=0 … census=ok`,
exit 1) and the expect-file digest.

## 2. Simulation — kill state (S094/S097 rows absent, entry present)

Mirror `Kill`: current on-disk `corpus/SOURCES.md` minus the S094/S097 rows (id-based removal), entry
`corpus/knowledge/benchmark-grader-semantics.md` present, README with the index row, expect + control
receipts copied. S093 row present with `status=mined`, `opened=2026-10-25`, used-by naming the entry
(the planned on-disk state).

```
$ python3 plans/adoption_check.py --expect .ufo/waves/round-32/claims/adoption-expect.json
entries=1 indexed=1 cited_rows=3 rows_present=1 rows_mined=1 usedby_ok=0 census=skipped
rc=1
```

Confirmed: **exit nonzero with rows_present=1 < 3** (rows_mined=1, usedby_ok=0). Second receipt:

```
$ python3 plans/round32_c1_verify.py --lane .
DEFECT V2 cited-row-identity: S094 has no registry row
checks=6 defects=1
rc=1
```

Variant `Kill2` (same, but S093 at baseline used-by, i.e. the clean refusal without the S093 edit)
prints the byte-identical adoption line and rc=1. Both the clean refusal and a partial-admission botch
(S093 used-by updated, rows refused) are indistinguishable to the counter.

## 3. Simulation — honest-stop branch (registry delta 0, entry not admitted)

Mirror `StopExact`: exact baseline tree (`git show f20a1097` for `corpus/SOURCES.md` and
`corpus/README.md` — baseline README has no entry index row, confirmed), entry absent, expect/control
copied. This is the committed state of the recorded stop (registry delta 0):

```
$ python3 plans/adoption_check.py --expect .ufo/waves/round-32/claims/adoption-expect.json
entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=skipped
rc=1
```

With `--census` this reproduces `control-nothing.txt` exactly (`census=ok`, exit 1; the live
with-census re-run is recorded in `R32RevClaims.md` §(d)). A stop mirror that includes the uncommitted
draft bundle only in the README (index row present, entry file absent) prints `entries=0 indexed=1`,
still rc=1.

**Answer to the assignment's branch question: yes — the lane can record a stop at registry delta 0
while the counter still fails; the counter is forced to fail there**, because the frozen predicate
requires `rows_present=3` and exit 0, which is unsatisfiable without landing the rows. There is no
state in which the counter passes while delta 0 holds (passing implies S094/S097 rows exist and S093's
used-by changed), so the stop is one-way coherent.

## 4. What a reviewer would observe

1. `adoption_check.py --expect … --census` → `entries=0 indexed=0 cited_rows=0 rows_present=0
   rows_mined=0 usedby_ok=0 census=ok`, exit 1 — byte-identical to the committed control receipt.
2. `round32_c1_verify.py` → `DEFECT V2 cited-row-identity: S094 has no registry row`, `checks=6
   defects=1`, exit 1 (V6 still passes: control receipt intact).
3. The round report/lesson (prose) is the only place the stop is recorded; C2's R2 only checks that
   the report exists after the last lane commit and cites the final tip — it does not check the stop
   narrative, the refused rows, or the delta-0 claim.
4. **No counter verifies the stop's defining properties**: "registry delta 0" and "entry not
   admitted" are never measured. A half-landed botch (entry + index row committed, rows refused)
   prints the same failing line as the clean stop (§2), and a silent do-nothing round prints the same
   failing line as the recorded stop. The adjective "honest" is unenforced by any machine.

## 5. Kill-rule reachability — verdict and caveats

- **The failing state is reachable and machine-detectable**: verified above (rows present → `rows_present=1 < 3`, rc=1; V2 defects). The honest stop is therefore expressible and observable as a *failure*.
- **The trigger is only semi-mechanical.** Neither frozen counter performs any quote check (both read only lane files; no network, no pin fetch). The refusal is enforced by the adoption gate `plans/sources_adopt.py --quote-file/--artifact` (`EXIT_QUOTE_TOO_LONG=6`, `EXIT_QUOTE_ABSENT=7`, `EXIT_URL_MISMATCH=8`, `EXIT_URL_UNMAPPED=9`), which lives outside both receipts — consistent with `R32CritC1.md` route (c) (a row whose quote cannot be found still counts as present/mined/opened/used-by; 0/3 resolved quotes admit). So a counter-only reviewer cannot tell a refused row from a landed one.
- **Empirically, the trigger would not fire this round**: the three pinned quotes resolve today (S093 @ `66f92766`; S094 @ `9be8d8fe` `main.py:58/:280`; S097 arXiv `2412.05579v2` abstract — fetched and verified in `R32LearnC1.md`/`R32CritC1.md` §Ground truth). A stop would require a fetch failure, a mis-location, or a deliberate refusal.
- **The kill rule's admissible branch is dead as written.** The rule would admit the entry when exactly two of three survive, but the counter demands all three rows present *and* cited (`cited_rows==required==3`); an admitted 2-source entry fails both receipts forever with no defined recording (neither pass nor stop). `R31RevClaims.md` already flagged this ("the kill rule's admissible branch cannot verify … the branch is dead as written"), `R32DraftReport.md:146-147` carries it as known ("unreachable under the frozen predicate because `cited_rows` must equal 3"), yet the frozen round-32 claims repeat the same sentence, and `R32RevClaims.md` §(c) re-states the threshold as "fewer than three cited rows survive" — conflating quote survival (prose) with row presence (counter) and contradicting the claims' own ≥2-admit letter.

## 6. Impacted axes

C1 coverage 7 (this seat's calibration item): the kill-rule honesty contract is not machine-enforced;
the stop is observable only as a generic counter failure. No frozen counter is broken; the gap is a
missing enforcement/recording mechanism, not a false pass.

## 7. Smallest safe correction

1. In the claims text, collapse the kill rule to the single fallback actually supported: any refused
   row ⇒ entry not admitted ⇒ recorded stop (delete the dead "≥2 survive ⇒ admit" clause).
2. Make the stop observable: commit a one-line stop receipt (e.g. `sources_adopt.py`'s `REFUSED`
   lines plus the decision) in `corpus/evidence/round32/`, and require the round report to name the
   refused rows — then extend `round32_c1_verify.py` with a V7 that asserts, when rows are absent,
   that this receipt exists and cites the refused ids. Leave the frozen counters untouched.
3. Optionally have `R32RevClaims`-style reviews quote the claims' threshold verbatim instead of
   paraphrasing "fewer than three" for "fewer than two".

---

VERDICT: kill-rule-reachable
