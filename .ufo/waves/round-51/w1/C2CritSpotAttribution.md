# C2CritSpotAttribution — spot-falsification of the routed-finding attribution

Seat: critic, round 51 (hyaku run 11), lane `kengaku-shokunin`.
Item: pick 12 rows spread across the ledger, read each `source` pointer and the finding itself,
decide independently whether the assigned owner is right, AGREE/DISAGREE per row.

## Axes named

- **adjacency** (primary, the axis this seat attacks): whether every routed finding names the
  lane that must act on it, and whether anything is routed rather than absorbed.
- **freshness** (read-only, not moved by me): the sibling declarations I quote are read at their
  current committed text; I date them where they are stale.

## Revision measured

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7   # lane HEAD, and the scratch clone's HEAD
base ledger: corpus/routed-findings.jsonl  rows=71  sha256 39fdef1e3fe06c6b75e63d363bd4420c87a830546e0fb1f4571e56b2a3d1cd7d
git status --porcelain corpus/routed-findings.jsonl -> 0 lines (working tree == HEAD)
```

Fragments read (8 of 8 present when I sampled), sha256:

```
6eaa0c91dadd95590380ba567badff707f9beda184fd5bfaa7f45c7bee743294  C2ExecA.jsonl
4989c38ecbd8eb9965b4de515501b269db4a14cba4f6c2bc7dec2645354fbe50  C2ExecB.jsonl
70c04d1b53180797386b399f1ff11b9feedb2e282815f2c7c942e8b64036b46a  C2ExecC.jsonl
85c9942141c843dc72083e60e0fa29db89a1f0f3e01ffed9bd7da89ae1ff29fc  C2ExecD.jsonl
182d3a8e87b7cc5b9f03b9611ae50bc765ac8b00083faeda303ab8ecbdbc1743  C2ExecE.jsonl
6d6122c44a99b950c05ef211ff38745313dcf6479958f4b3babeacba8a9342d8  C2ExecF.jsonl
ddb100305b123c93dc6edcd6b2a17aab9d0745606d5144c7864742db839715d8  C2ExecG.jsonl
64e5c91d50be9108656da82d4caeb07900b166b826731a40eeaad59074507a5e  C2ExecH.jsonl
```

## Commands run (verbatim)

```sh
# 12 rows + their source pointers with +-2 lines of context
python3 /fast/scratch/hyaku/kengaku-r51/C2CritSpotAttribution/dump.py
#   rows dumped: 1,6,12,19,24,30,37,43,49,55,62,70 (12) and 7,8,14 (boundary reads);
#   final sample below is 1,7,12,14,19,30,37,43,49,55,62,70

# assigned owner per row, from the executor fragments
python3 - <<'PY'   # glob .ufo/waves/round-51/w1/C2Exec?.jsonl, index by id
PY

# in-lane artifact presence for each sampled row
grep -n '^| `order-check`' SKILL.md ; grep -n '^| `round39-c1-audit`' SKILL.md
grep -c 'ro-bind /home/vgpnk/.local/bin' .ufo/waves/round-41/build-spec.json
ls -l plans/scratch_guard.py
grep -n 'never in place' corpus/QUALITY.md
sed -n '17,18p' plans/scratch_guard.py
grep -n 'not\*\* "named carried again in the freeze"' corpus/lessons/round-42.md
for f in plans/carried_direction_diff.py plans/sources_appendonly.py; do test -e "$f" && echo "PRESENT $f" || echo "ABSENT $f"; done
test -e plans/fixture_fence.py && echo "PRESENT plans/fixture_fence.py"
grep -n '^## Errata (round 46)' corpus/knowledge/tb2-password-recovery-grader.md

# instrument sanity + owner-set derivation
python3 plans/round51_routing.py --selftest
python3 -c "import round51_routing as R; print(sorted(R.load_owners(Path('/home/vgpnk/Projects/shokunin'))))"

# owner-leg matrix, on a scratch clone with the real fleet conf copied beside it
git clone --shared -q <lane> $S/lane ; test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
cp /home/vgpnk/Projects/shokunin/shokunin.conf $S/shokunin.conf
python3 <clone>/plans/round51_routing.py --lane <clone> --scratch $S/work    # once per owner value
```

Disk seen: `/dev/nvme1n1p2 804G 249G 555G 31% /fast`.

## The 12 rows: assigned vs independent verdict

Sample rule: one row from each executor band (rows 1–9, 10–18, 19–27, 28–36, 37–45, 46–54,
55–63, 64–71), plus every row in the ledger whose finding carries a fleet-wide clause
(host-safety envelope, scratch guard, SOURCES correction rule) — the three places where
"absorbed by kengaku" could be the wrong call. Bands: A(1,7) B(12,14) C(19) D(30) E(37,43)
F(49) G(55,62) H(70).

| # | idx | id | class | assigned (fragment) | verdict |
|---|---|---|---|---|---|
| 1 | 1 | R39-R1 | registry-missing-gate-rows | kengaku / fixed-verified (A) | **AGREE** |
| 2 | 7 | R40-R2 | host-safety-envelope | kengaku / fixed-verified (A) | **AGREE** (fleet clause unnamed, O3) |
| 3 | 12 | R42-R2 | scratch-root-guard | kengaku / fixed-verified (B) | **AGREE** (fleet clause unnamed, O3) |
| 4 | 14 | R42-R4 | sources-correction-rule | kengaku / fixed-verified (B) | **AGREE** (note/close contradiction, O2b) |
| 5 | 19 | R42-R6 | scratch-guard-exit-contract | kengaku / accepted-risk (C) | **AGREE** |
| 6 | 30 | R42-R3-11 | lesson-unsupported-carry-claim | kengaku / fixed-verified (D) | **AGREE** |
| 7 | 37 | R42-R3-18 | criterion-nonlanded-tool | kengaku / accepted-risk (E) | **AGREE** |
| 8 | 43 | R42-R3-24 | ledger-status-mismatch | kengaku / fixed-verified (E) | **AGREE** |
| 9 | 49 | R42-R3-30 | frozen-cell-wrong-citation | kengaku / fixed-verified (F) | **AGREE** |
| 10 | 55 | R42-R3-36 | plan-class-from-unfrozen-probe | kengaku / accepted-risk (G) | **AGREE** |
| 11 | 62 | R45-S5-2 | predictor-lone-cr | kengaku / fixed-verified (G) | **AGREE** |
| 12 | 70 | R45-S5-7d | intent-brace-prefix | kengaku / fixed-verified (H) | **AGREE** (attribution only; see O2) |

**12 AGREE, 0 DISAGREE** on the base 71. One DISAGREE-class finding exists in the *candidate*
ledger's new rows; it is reported out of sample in O1 below with its evidence, because those rows
are not part of the 71-row ledger this item names.

## Per-row reasoning (the evidence I used)

1. **R39-R1** — source `corpus/lessons/round-39-verifier-spotcheck.md:132`: "R1 Register
   `plans/order_check.py` (gate) and `plans/round39_c1_audit.py` in `SKILL.md` §Gate/probe
   registry". The artifact is this lane's own registry: `grep -n '^| \`order-check\`' SKILL.md`
   → `590:`, `round39-c1-audit` → `591:` (both present). The competing sibling is kotoba
   (`kotoba-shokunin/PROVINCE.md:12` "`SKILL.md` — trigger/frontmatter craft, anatomy and
   compression, decision tables"), but that is *craft over SKILL.md*, not the bookkeeping of one
   lane's gate rows; `kengaku-shokunin/PROVINCE.md:30` refuses to kotoba only "prompt- and
   skill-craft rules". Owner kengaku.
2. **R40-R2** — source `round-40-verifier-spotcheck.md:95`: "no seat may write outside the lane
   scope or scratch; keep the read-only `~/.local/bin` sandbox for every attack seat". Fleet-wide
   in wording, but the repair named by the close is this lane's own envelope:
   `grep -c 'ro-bind /home/vgpnk/.local/bin' .ufo/waves/round-41/build-spec.json` → `1`, and both
   shims carry `NEUTRALIZED` (1 each). kumitate's ground (`kumitate-shokunin/PROVINCE.md:22`
   "seat-containment rules derived from their mechanisms", `:24` "how a wave's seats are
   arranged") is the *fleet* owner of the general rule, and kumitate refuses to absorb
   (`PROVINCE.md:6` "report cross-domain evidence back to the orchestrator rather than absorbing
   it"), but it cannot edit this lane's build-spec. Owner kengaku for the recorded finding; the
   fleet clause stays unnamed — O3.
3. **R42-R2** — source `round-41-verifier-spotcheck.md:110-111`: "give the round root a guard the
   seats cannot remove … carry the guard sentence into every wave context". Repair: `plans/scratch_guard.py`
   (25,643 B, present) plus the SKILL.md registry row closed by child row R42-R2.2. Same boundary
   as #2. Owner kengaku.
4. **R42-R4** — source `round-41-verifier-spotcheck.md:116`: "correct a non-mutable cell by a new
   row opening `supersedes S0NN —`, never in place". The rule's authority is fleet-level and
   read-only for this lane (`/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`), which is the only
   real argument for a sibling owner. It loses to two measured facts: the defect is that this
   lane's docs did not state the rule, and the repair is in-lane
   (`grep -n 'never in place' corpus/QUALITY.md` → `759:` heading "…never in place"), and the
   aggregator is forbidden to make that edit — `CORPUS.md:53-56`: "the aggregator writes only
   `lessons/round-<N>-aggregator-*.md` and does not edit lane-authored corpus files in place".
   Owner kengaku.
5. **R42-R6** — source is the instrument itself, `plans/scratch_guard.py:17` (docstring: "exit 2
   when the root is not a directory or the sentinel cannot be read"). In-lane file, in-lane
   contract. Owner kengaku.
6. **R42-R3-11** — source `F42RevLesson.md:109` (R5's "named carried again in the freeze
   (§Limits)" is false). The subject is this lane's own lesson; the close names the round-43
   errata and `grep -n 'not\*\* "named carried again in the freeze"' corpus/lessons/round-42.md`
   → `170:`. Owner kengaku.
7. **R42-R3-18** — source `F42RevQuality.md:13` (Q33/Q34 executable checks name tools never
   landed). Both names are this lane's `plans/`:
   `plans/carried_direction_diff.py` ABSENT, `plans/sources_appendonly.py` ABSENT (measured).
   Owner kengaku.
8. **R42-R3-24** — the finding is *about this ledger* ("R42-R4 is open while its check passes").
   Only this lane can edit it; the claims doc makes every other seat read-only. Owner kengaku.
9. **R42-R3-30** — source `F42CritAdv.md:53` (frozen C1 cell X7 cites `:92-93` where `:93` is
   blank); the repair is a lesson erratum and the check reads `corpus/lessons/`. Owner kengaku.
10. **R42-R3-36** — source `F42CritPlanNext.md:91` (coverage class asserted from a non-frozen host
    probe; prior-art hits exist). Prior-art pricing is this lane's declared surface:
    `PROVINCE.md:20` "Public literature … | novelty pricing of local findings". chousa owns
    research *method*, not this lane's novelty claim. Owner kengaku.
11. **R45-S5-2** — source `round-45-verifier-spotcheck.md:147` (mark or supersede the entry's
    `## Predictor`); repair is an erratum in this lane's entry, measured present at
    `corpus/knowledge/tb2-password-recovery-grader.md:214` (`## Errata (round 46)`). Owner kengaku.
12. **R45-S5-7d** — source `round-45-verifier-spotcheck.md:155` ("brace-prefix bypass"); the
    artifact is this lane's fence `plans/fixture_fence.py` (present). tameshi owns
    verification-fixture *craft* as a domain, not this lane's tool. Owner kengaku. (The row's
    `status: open` + `fixed-verified` pairing is a disposition question, not attribution — O2.)

## Out-of-sample findings (labelled; not part of the 12)

### O1 — the one attribution I would change: `R51-R1`'s "flag authority stays kama's"

`.ufo/waves/round-51/w1/C2ExecLedgerMerge.jsonl` (75 rows = base 71 + `R51-R1..R4`) routes:

```
R51-R1 owner=kama  disposition=routed  next="kama: serving-plane health/flag authority for the LFM3 pair"
R51-R4 owner=kama  disposition=routed  next="kama: whether the qwen-coder unit is retired in favour of the LFM3 pair"
```

R51-R4 I agree with. R51-R1 I agree with **as to health**, and the owner `kama` is defensible on
the fleet map — `kumitate-shokunin/PROVINCE.md:29` "Local model serving and endpoints → kama";
`kama-shokunin/PROVINCE.md:3` "Domain: local model serving & endpoint health". What does not
hold is the *sentence* "flag authority stays kama's" against kama's own text:
`kama-shokunin/PROVINCE.md:10` "kama governs discovering whatever serves these ports and **never
claims an installed server**", and "restoring a unit is operator-owned work". Smallest safe
correction: keep `owner=kama`, change `next` to "kama: serving-plane health/identity for the LFM3
pair; flag/unit authority is operator-owned", and (separately, C1's business) date
`kengaku-shokunin/PROVINCE.md:24-25` "**Not owned:** the model-serving plane (llama-server flags,
slot/batch config) — no lane owns it; escalate to the integrator" — that line now contradicts both
kumitate:29 and the new routed row, and it is the one committed declaration the attribution
directly contradicts.

### O2 — owner/disposition pairings that do not read true (disposition seat's item, flagged here)

- `R42-R3-14` and `R42-R3-16`: `owner=kengaku` with `disposition=refused-out-of-scope` and
  `blocker` "REFUTED at the tip … no change owed". The owner is right (the artifacts are
  `plans/round42_c2_verify.py:327` and `corpus/evidence/round42/tb2-circuit-fibsqrt/Dockerfile:9-10`,
  both in-lane). The disposition is not: a *refuted* finding is not a *scope refusal*, and
  "out of scope" paired with owner `kengaku` is a self-contradiction the frozen vocabulary cannot
  express (there is no `refuted` member). Under the current vocabulary the honest value is
  `accepted-risk` (nothing owed) — the counter accepts all six, so this is a semantics call, not
  a predicate failure.
- `R45-S5-7d` (and any other `status: open` + `fixed-verified`): the counter checks
  `status ∈ {open,closed,refused,blocked}` and `disposition ∈ DISPOSITIONS` independently, so an
  open row may claim `fixed-verified`. Not an attribution defect; recorded so the L1 does not
  read my AGREE as endorsing the pairing.
- `R42-R4`: the close says "corpus/QUALITY.md:759 (Q34 states rule 2 in-lane)" while the row's own
  `note` still says "no lane doc states it (`grep -r 'never in place|mutable cell' …` -> 0 hits)".
  Both cannot be current; `:759` exists (measured). The note is stale, not the owner.

### O3 — the base ledger routes nothing, so the routing leg is vacuous

Fragment histogram over all 71 ids (8 fragments, 71 unique):

```
Counter({('kengaku','fixed-verified'):38, ('kengaku','accepted-risk'):24,
         ('kengaku','fixed-historical'):7,  ('kengaku','refused-out-of-scope'):2})
non-kengaku owners: []
```

`routed=0`, `referral=0` among the base rows, so `NEXT violations=0` cannot fire from them and the
axis signal ("named with its owner **and routed, not absorbed**") rests entirely on the four new
`R51-*` rows. This is not a defect in the predicate, but it is the counterexample to the claim's
strength: three of the twelve rows I sampled (7, 12, 14) carry fleet-wide clauses whose only
owner under the fleet map is a sibling (kumitate for seat containment/scratch discipline,
aggregator for the fleet corpus contract), and none of them is visible as routed. Smallest safe
correction: do **not** add rows to the base 71 (the after-target pins `rows=71`; the kill rule
fails only on a drop, but the target text would then be wrong without an amendment) — carry the
three clauses as report-outs (C2ScribeReportOuts' item), or add exactly one routed row and amend
the after-target count with a dated line.

## Instrument counterexamples (measured, attribution mechanism)

### E1 — the owner leg does not read `shokunin.conf`, and rejects four real lanes

`load_owners` uses `re.match(r"\s{0,6}([a-z][a-z0-9-]{2,15}):\s*\{", line)`; the fleet conf's lanes
are written `lane|repo|axes`, so the regex matches **0** lines:

```
REGEX_MATCHES=0
owners n= 17
conf lanes n= 23
fallback-only (not in conf LANES): ['unowned:integrator']
conf lanes rejected by counter: ['audio', 'game-dev-2d', 'game-dev-3d', 'lore', 'mado', 'revenger', 'tsukuroi']
```

Owner matrix, scratch clone + the real conf copied beside it, row 7's owner swapped each run:

```
owner=kengaku              rc=1 OWNERS attributed=71 unattributed=0 | - | PREDICATE R51-C2 fail
owner=tsukuroi             rc=1 OWNERS attributed=70 unattributed=1 | DETAIL OWNER R40-R2 owner 'tsukuroi' not a fleet lane | PREDICATE R51-C2 fail
owner=mado                 rc=1 OWNERS attributed=70 unattributed=1 | DETAIL OWNER R40-R2 owner 'mado' not a fleet lane | PREDICATE R51-C2 fail
owner=lore                 rc=1 OWNERS attributed=70 unattributed=1 | DETAIL OWNER R40-R2 owner 'lore' not a fleet lane | PREDICATE R51-C2 fail
owner=revenger             rc=1 OWNERS attributed=70 unattributed=1 | DETAIL OWNER R40-R2 owner 'revenger' not a fleet lane | PREDICATE R51-C2 fail
owner=kumitate             rc=1 OWNERS attributed=71 unattributed=0 | - | PREDICATE R51-C2 fail
owner=kotoba               rc=1 OWNERS attributed=71 unattributed=0 | - | PREDICATE R51-C2 fail
owner=unowned:integrator   rc=1 OWNERS attributed=71 unattributed=0 | - | PREDICATE R51-C2 fail
owner=nope-lane            rc=1 OWNERS attributed=70 unattributed=1 | DETAIL OWNER R40-R2 owner 'nope-lane' not a fleet lane | PREDICATE R51-C2 fail
```

(the `PREDICATE fail` on the accepted runs is the base ledger's 10 empty `check` fields, not the
owner leg). The frozen predicate says "every `owner` names a fleet lane from `../shokunin.conf`";
the implementation is a 17-string allowlist. Latent today (all 75 candidate rows use
kengaku/kama/protocol/unowned:integrator), fatal the moment a correct routed owner is `tsukuroi`,
`mado`, `lore` or `revenger`. Smallest fix: parse the conf's `LANES` block (`^([a-z][a-z0-9-]*)\|`)
instead of the `key: {` shape, keeping `unowned:integrator` as the one explicit non-lane.

### E2 — `--ledger` outside the lane crashes

```
File ".../plans/round51_routing.py", line 77, in check
    print("LEDGER %s rows=%d" % (ledger.relative_to(lane), len(rows)))
ValueError: 'led-tsukuroi.jsonl' is not in the subpath of '/home/vgpnk/Projects/shokunin/kengaku-shokunin'
```

Independent verification of a candidate ledger therefore requires a clone (what I did). Smallest
fix: fall back to `ledger` when `relative_to` raises.

### E3 — the selftest does not model a real-conf lane

```
[selftest] cases=11 failures=0
[selftest] ALL PASS
```

Its conf fixture is `"lanes:\n  kengaku: { cwd: x, axes: y }\n  kama: { cwd: z, axes: w }\n"` —
the `key: {` shape the real conf does not use, which is exactly why E1 is invisible to it.

## Limits

- I did not run the 71 ledger checks; `C2CritChecks` owns that comparison and `C2ExecOpenChecks`/
  `C2ExecClosedChecks` own the check classification. My verdicts are about **ownership**, not about
  whether a `fixed-verified` check passes.
- Disposition truth (vacuous checks, `accepted-risk` hiding an unowned defect) is
  `C2CritDisposition`'s item; I flag only pairings that contradict the owner I verified (O2).
- Sample: 12 of the 71 base rows, chosen by band + the three fleet-clause rows; plus the 4 new
  candidate rows out of sample. The remaining 59 base rows were not read line by line by me.
- Fragments were still landing when I began (A,B,D,F,G at 15:26–15:27; C,E,H by ~15:30). The
  merged candidate I inspected is 75 rows, not the 71 the after-target text pins — that count
  question is the L1's/`C2RevRecount`'s, not mine.
- My owner matrix ran on a `git clone --shared` with the real `shokunin.conf` copied beside it
  (the real lane is read-only), toplevel asserted:
  `git -C $D rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r51/C2CritSpotAttribution/lane`.
- Scratch `/fast/scratch/hyaku/kengaku-r51/C2CritSpotAttribution` removed before yield (see
  below); no receipt in this report depends on a `/tmp` or scratch path for its evidence.
- No tool installed or upgraded; no pacman transaction attempted.

## Scratch

`/fast/scratch/hyaku/kengaku-r51/C2CritSpotAttribution` (clone + variant ledgers + `work/`) is
deleted in the same turn as this report; nothing citable lives there — every number above is
reproducible from the lane tree at `REV 4090c3d` plus the fragment hashes.

VERDICT: AGREE 12/12 on the base-71 attribution I sampled (all `kengaku`, and kengaku is the lane that must act on every one of them); no DISAGREE on the sampled rows. One attribution defect found out of sample — `R51-R1`'s "flag authority stays kama's" contradicts kama's own PROVINCE ("never claims an installed server") and kengaku's stale `PROVINCE.md:24-25`; the smallest correction is to narrow that row's `next` and date the stale PROVINCE line. Two mechanism defects are measured and latent: the owner leg is a hardcoded 17-lane allowlist that rejects four real fleet lanes (`tsukuroi`, `mado`, `lore`, `revenger`) instead of reading `shokunin.conf`, and `--ledger` outside the lane crashes at `round51_routing.py:77`. The routing leg of adjacency is satisfied vacuously: 71/71 base rows are kengaku-owned with 0 `routed`, so the axis signal rests entirely on the four new `R51-*` rows.
