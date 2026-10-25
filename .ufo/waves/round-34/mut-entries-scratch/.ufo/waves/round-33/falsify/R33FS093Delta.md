# R33FS093Delta — C1's "S093 used-by gains the entry": no transition occurred

Seat: `KengakuR33.R33FS093Delta` (critic, leaf). Date: 2026-10-25. Round 33, hyaku run 7.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (HEAD `77ac8c1`, freeze `f0b20aea`).
Target: the frozen C1 clause that S093 "gains" `corpus/knowledge/benchmark-grader-semantics.md`
in `used-by`.
Mode: read-only. No lane/fleet file edited, staged, or committed; no tool installed. All git
invocations were reads (`git show`, `git archive`); every fixture write went to a fresh
`/tmp/r33-R33FS093Delta` sandbox.

## 1. The clause under attack (quoted, frozen, not edited)

`plans/round-33-claims.md:36-38`:

```
the citations resolve; it is not new corpus bytes, it is in-flight debt). S093
(SWE-bench Pro V2 verifier files, round-31 row) is already `mined` and gains the
entry in `used-by`. The four round-32 refusal rows at S094/S097/S101/S102 stand
```

`plans/round-33-claims.md:48-49` (frozen predicate):

```
> `status=mined`, `opened=2026-10-25` and `used-by` naming the entry (S093's `used-by`
> gains the entry; S103 and S104 are new rows); the entry has exactly one index row in
```

The clause asserts a registry delta. The measurement below shows there is none.

## 2. Measurement: S093's row is byte-identical at freeze and at tip

```
$ git -C . show f0b20aea:corpus/SOURCES.md | grep -E '^\| S093' | sha256sum
bc7809b4977d7178df95c934afbdf3b9af8d3a563aa8c59226da6976fdeb3475  -
$ grep -E '^\| S093' corpus/SOURCES.md | sha256sum
bc7809b4977d7178df95c934afbdf3b9af8d3a563aa8c59226da6976fdeb3475  -
$ diff <(git show f0b20aea:corpus/SOURCES.md | grep -E '^\| S093') <(grep -E '^\| S093' corpus/SOURCES.md)
ROW_IDENTICAL
$ git diff f0b20aea..HEAD -- corpus/SOURCES.md | grep -c S093
0
```

Line number is `112` at both commits. The `used-by` cell (cell 11) is identical byte for byte:

```
$ git show f0b20aea:corpus/SOURCES.md | awk -F'|' '$2 ~ /S093/{print $12}' | sha256sum
4799b852154977f7e5905d5989b85895853df9970e8d51def9b2fac2e36ebb61  -
$ awk -F'|' '$2 ~ /S093/{print $12}' corpus/SOURCES.md | sha256sum
4799b852154977f7e5905d5989b85895853df9970e8d51def9b2fac2e36ebb61  -
```

Cell text at both:

```
corpus/knowledge/benchmark-verifier-execution-model.md, corpus/knowledge/benchmark-grader-semantics.md
```

The other two predicate cells are equally untouched (`mined`, `2026-10-25` at `bcd2a6c^`,
`bcd2a6c`, `f0b20aea`, `HEAD`):

```
$ for c in bcd2a6c^ bcd2a6c f0b20aea HEAD; do printf "%s -> status=%s opened=%s\n" "$c" \
    "$(git show $c:corpus/SOURCES.md | awk -F'|' '$2 ~ /S093/{gsub(/^ +| +$/,"",$9);print $9}')" \
    "$(git show $c:corpus/SOURCES.md | awk -F'|' '$2 ~ /S093/{gsub(/^ +| +$/,"",$10);print $10}')"; done
bcd2a6c^ -> status=mined opened=2026-10-25
bcd2a6c -> status=mined opened=2026-10-25
f0b20aea -> status=mined opened=2026-10-25
HEAD -> status=mined opened=2026-10-25
```

No round-33 commit touches S093: `git log --oneline -S'corpus/knowledge/benchmark-grader-semantics.md' -- corpus/SOURCES.md`
returns only `bcd2a6c` (round 32) and `b54feca` (round 33, which adds the two new rows S103/S104
whose own `used-by` cells carry the same string — not an S093 edit).

## 3. Where the cell actually came from: round 32, commit `bcd2a6c`

```
$ git show bcd2a6c^:corpus/SOURCES.md | awk -F'|' '$2 ~ /S093/{print "OLD["$12"]"}'
OLD[ corpus/knowledge/benchmark-verifier-execution-model.md ]
$ git show bcd2a6c:corpus/SOURCES.md | awk -F'|' '$2 ~ /S093/{print "NEW["$12"]"}'
NEW[ corpus/knowledge/benchmark-verifier-execution-model.md, corpus/knowledge/benchmark-grader-semantics.md ]
```

`bcd2a6c` ("round-32: record rejected assimilation and C3 probe") is an ancestor of the freeze
(`git log --oneline --graph` → `bcd2a6c → 112091c → f0b20ae`). That same commit is the one that
committed the *refused* draft entry and recorded the refusal. The frozen round-32 claim carried the
same parenthetical (`plans/round-32-claims.md:35`), and round 32 delivered it — while refusing the
entry:

- `corpus/lessons/round-32.md:25`: "No registry append was accepted; the staged rows are recorded as rejected".
- `corpus/lessons/round-32.md:35`: "C1: entry draft exists but is not admitted; do not count it as a corpus expansion."

So the round-32 record says no registry change was accepted, while its own commit changed a
registry cell (`S093.used-by`) to point at an entry the same record forbids counting. Round-32's
frozen counter earned nothing from it — replaying round-32's own expect on the `bcd2a6c` tree:

```
$ git -C . archive bcd2a6c corpus | tar -x -C /tmp/r33-R33FS093Delta/r32tip
$ python3 plans/adoption_check.py --lane /tmp/r33-R33FS093Delta/r32tip \
    --expect .ufo/waves/round-32/claims/adoption-expect.json
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=1 usedby_ok=0 census=skipped
exit=1
```

The cell edit advanced no counter in its own round. Round 33 then inherited the string and
described it as a round-33 gain.

## 4. Predicate-level proof: S093's clause was already satisfied at the freeze

Sandbox built from the freeze tree; the only fixture change is that the entry's `source:` lines were
reduced to S093 alone (so the all-of `usedby_ok` check isolates S093), with `--expect` sources
`["S093"]`:

```
$ git -C . archive f0b20aea corpus | tar -x -C /tmp/r33-R33FS093Delta/freeze
$ python3 plans/adoption_check.py --lane /tmp/r33-R33FS093Delta/freeze \
    --expect /tmp/r33-R33FS093Delta/freeze/.expect-s093.json
entries=1 indexed=1 cited_rows=1 rows_present=1 rows_mined=1 usedby_ok=1 census=skipped
exit=1
$ # same probe on the tip tree
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=skipped
```

Every non-census field for the S093 clause reads exactly the target value **at the freeze commit**;
the exit code is 1 only because `--census` was not run (see §11). In other words, the frozen
predicate's S093 condition — `status=mined`, `opened=2026-10-25`, `used-by` naming the entry — was
true at `f0b20aea`, before any round-33 byte existed. Nothing was "gained".

Control reproduction on a clean freeze copy, canonical expect:

```
$ git -C . archive f0b20aea corpus | tar -x -C /tmp/r33-R33FS093Delta/freeze-clean
$ sha256sum /tmp/r33-R33FS093Delta/freeze-clean/corpus/knowledge/benchmark-grader-semantics.md
20e9cec8dd53e7260b053278e278eed818ab7baa273bfbcde3665bc64ca1c637  -
$ python3 plans/adoption_check.py --lane /tmp/r33-R33FS093Delta/freeze-clean \
    --expect .ufo/waves/round-33/claims/adoption-expect.json
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=1 usedby_ok=0 census=skipped
```

This matches the committed control receipt (`.ufo/waves/round-33/claims/control-nothing.txt`:
`entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=1 usedby_ok=0 census=ok`, `exit=1`)
field for field, apart from the unrun census.

## 5. The `usedby_ok` 0 → 1 flip is earned entirely by S103/S104

At the freeze, S103/S104 rows do not exist, and S093 alone is linked:

```
== f0b20aea == entry cited ids: ['S093', 'S094', 'S097']
  S093: status='mined' opened='2026-10-25' linked=True  usedby='...verifier-execution-model.md, ...grader-semantics.md'
  S094: status='rejected' opened='2026-10-25' linked=False usedby='—'
  S097: status='rejected' opened='2026-10-25' linked=False usedby='—'
  expect-id S093: present=True linked=True
  expect-id S103: present=False linked=None
  expect-id S104: present=False linked=None
== HEAD == entry cited ids: ['S093', 'S103', 'S104']
  S093: linked=True (same cell)
  S103: status='mined' opened='2026-10-25' linked=True usedby='...grader-semantics.md'
  S104: status='mined' opened='2026-10-25' linked=True usedby='...grader-semantics.md'
```

(Computed with the exact `adoption_check.py` row parser and `linked` predicate, lines 38-47 and
90-98.) So the round-33 delta that flips `usedby_ok` 0→1 is the *appearance of two rows*, and the
`rows_mined` 1→3 flip is their `mined` status. S093 contributes zero bytes to either flip.

## 6. Why no lane authority caught it (mechanism, not excuse)

1. **The frozen counter is a state predicate.** `plans/adoption_check.py:90-98` asks whether the
   entry path is a member of each cited row's `used-by` list. Membership cannot distinguish "was
   already there" from "was added this round"; §4 shows it reads the same value on both sides of the
   freeze.
2. **The fleet census validates existence, not admission.** `scripts/sources-census.sh:566-567`:

   ```
   if [ ! -e "$dir/$path" ]; then
     printf '%s\tE11\t%s missing used-by %s\n' "$lane" "$id" "$path"
   ```

   The draft `corpus/knowledge/benchmark-grader-semantics.md` existed on disk (and was indexed —
   the freeze control prints `indexed=1`) while being unadmitted, so E11 was clean at the freeze.
   A `used-by` naming an unadmitted entry is invisible to both counters.

Neither defect is in C1's predicate. They are the reason the false delta survived freeze review and
then hardened into committed records.

## 7. Blast radius: the false delta is committed, not just preregistered

| Artifact | Line | Text | State |
|---|---|---|---|
| `plans/round-33-claims.md` | 36-38, 48-49 | "is already `mined` and gains the entry in `used-by`" / "S093's `used-by` gains the entry" | frozen prereg — inaccurate |
| `corpus/lessons/round-33.md` | 20 | "S093 already `mined`; `used-by` gains the entry" | **committed** (`c1a520d`) |
| `LOG.md` | 922-923 | "S093 stays `mined` and gains the entry in `used-by`" | **committed** |
| `corpus/README.md` | 255 | freeze: "covered at source-code depth (round 32, 2026-10-25) … S093, S094, S097"; tip: "(round 33, 2026-10-25, admitted under renumbered ids) … S093, S103, S104" | re-dated in place, no erratum |

The `LOG.md` line is the sharpest form: "stays `mined` and gains the entry" asserts both
continuity and change for the same row. The freeze-time README already attributed the coverage to
round 32, so the lane's own bytes contradicted the claim before the build wave started.

## 8. Charitable readings tested, and why each fails

- **"The link becomes valid on admission, so it 'gains' the entry."** The clause is paired with
  "S103 and S104 are new rows" — registry-byte deltas on both sides of the semicolon. And the
  claim's own instrument (`adoption_check` `usedby_ok`) is textual path membership, which was
  already true at the freeze (§4), so the claim's own counter cannot distinguish admission-validity
  from pre-existing text. Under this reading the claim would still need to say the *link* becomes
  valid, not that the cell gains the entry.
- **"The gate wrote it this round."** The round-33 gate was invoked with `--admit-ids S103,S104`
  only (`R33SourcesAdoptDry.md` F2/F5), and `R33C1KillRule.md` row 4 records S093's merge as a
  hand edit. The gate never had S093 as a target.
- **"The entry, not the cell, gains."** The entry's own bytes did change (source re-pointing,
  `20e9cec8…` → `6eed24f6…`), but that is the entry, and the clause explicitly names S093's
  `used-by`.

## 9. Verdict

**VERDICT: caught** — the clause is a false delta. S093's `used-by` cell is byte-identical at
`f0b20aea` and `77ac8c1` (sha256 `4799b852…`), the whole row is identical (`bc7809b4…`), and the
cell has named the entry since round-32 commit `bcd2a6c`. The frozen predicate's S093 condition was
already satisfied at the freeze; only S103/S104 are new.

Severity: medium — calibration/provenance, **not predicate-breaking**. Still true and not attacked
here: the required end state for S093 holds; S103/S104 are genuinely new rows; the entry's two
source re-points are real; the printed pass line
(`entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok`, exit 0)
honestly describes the state, only not a transition.

Impacted axes: **calibration** (primary — false provenance in a frozen prereg and in two committed
records), **coverage ledger attribution** (secondary — the round-33 ledger records a registry cell
delta earned in round 32; no numeric change, the coverage score is held at 7 either way).
Not impacted: depth, control fidelity.

## 10. Smallest safe correction (no frozen-claim edit proposed)

1. **Append a dated erratum** (per `corpus/QUALITY.md:52-55`: "numbers are corrected by appended
   errata, never an in-place edit"; R5) to `corpus/lessons/round-33.md` and `LOG.md`, naming this
   report and `corpus/SOURCES.md:112`: "S093's `used-by` already named the entry at `f0b20aea`
   (added `bcd2a6c`, round 32, with the then-refused draft); no round-33 cell change. The round-33
   delta is the entry's two source re-points plus rows S103/S104." A second erratum for round 32
   should note that `bcd2a6c` changed `S093.used-by` although `corpus/lessons/round-32.md:25`
   records "No registry append was accepted" and `:35` says the draft must not be counted.
2. **Optional, non-blocking:** make census E11 admission-aware (require an index row / admit
   receipt, not only `-e`), so a `used-by` to an on-disk but unadmitted entry is flagged. Today it
   passes, which is what let a dangling link sit in a `mined` row across two freezes.
3. **No change to `plans/round-33-claims.md`.** The frozen text is recorded as inaccurate; that
   record is this wave's product.

## 11. Limitations

- The census leg of the canonical exit-0 form cannot be reproduced in `/tmp`: `adoption_check.py`
  runs `scripts/sources-census.sh validate --root <lane.parent> <lane.name>` (lines 132-141), which
  is fleet-root-bound. My sandbox runs print `census=skipped`; the `census=ok` in the committed
  control is taken from the committed receipt. I did not run the fleet census.
- Prior build findings agree and are not duplicated here: `R33ClaimsReview.md:8`,
  `R33ReconRegistry.md:405`, `R33ReconPackage.md:236`. This seat adds the isolated-counter proof
  (§4), the flip attribution (§5), the counter/census mechanism (§6), and the committed spillover
  plus round-32 origin (§3, §7).
- Lane state observed but not touched: worktree carried unrelated uncommitted changes
  (` M SCORECARD.md`, ` M .ufo/waves/round-33/build/R33L0Packet.md`, ` D
  .ufo/waves/round-33/assimilation/append-package.md`, ` D
  .ufo/waves/round-33/assimilation/quotes-rows.txt`). `corpus/SOURCES.md` was clean, so the tip
  reading equals `HEAD`.
- No tools installed or updated.
