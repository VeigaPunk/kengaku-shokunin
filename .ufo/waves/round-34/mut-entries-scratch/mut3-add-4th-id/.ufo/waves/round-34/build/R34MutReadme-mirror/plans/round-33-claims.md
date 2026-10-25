# Round 33 — frozen claims (kengaku, hyaku run 7, 2026-10-25)

Baseline: lane branch tip `112091c2d9077e484b53512ca363d2fe6ba6fc5c` (local = remote, `ahead=0`).
Registry 95 rows (ids ≤ S102; S103+ unused), `corpus/knowledge/` 40 files, 40 index rows,
census exit 0 with 15 `W04` (before receipt: `.ufo/waves/round-33/claims/census-before.txt`).
Three claims, three distinct axes. Frozen BEFORE any wave seat ran; a predicate changed
after a seat has scored is not this claim's predicate.

Lowest non-retired axis: **coverage 7**, tied with **novelty 7** (SCORECARD §Round 31;
round 32 moved no score and landed no SCORECARD section — that omission is C2's N2).
No stagnation waiver: the saturation line is 8, novelty sits below it, and a capability
row entered at round 31. Tie-break per the lane's recorded rule: the claim most
falsifiable with the sources an on-host tool can open wins — C1 opens two pinned
documents plus one already-mined row and lands a registry delta; a novelty claim needs
a phenomenon probe and no identity-verified endpoint exists (`corpus/README.md`
§Frontier bullet 4). C1 carries the lowest-axis obligation.

Round shape: two v1 waves (`ufo-wave-policy.json`, band 32–64), 36 build + 36 falsify.
Routing per the operator's run-7 role map (host route table; no per-seat model).
The §3 planner seat is held by the L1 (validator-frozen topology); a bounded planning
data-walk rides the R33ReconPackage scout item.

## C1 — coverage: shokuknow assimilation round 5, the grader-semantics entry admitted under renumbered ids

**Surface this claim moves:** the round-31 Gate's flip condition for this exact candidate
("a later round that takes the theme and opens the rows", `corpus/lessons/round-31.md`
§Gate), as narrowed by the round-32 refusal: staged ids S094/S097 collide with live
registry identities and staged S101/S102 identify unrelated SWE-bench sources
(`corpus/lessons/round-32.md` §Assimilation). This claim takes the theme with
**unused lane ids**: staged S094 → **S103** (Toolathlon `tasks/finalpool/ab-testing/evaluation/main.py`
at `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`), staged S097 → **S104** (arXiv
2412.05579v2), re-grounded this round by opening both sources, with the entry's
`source:` lines re-pointed by document. The round-32 refusal committed a draft of
`corpus/knowledge/benchmark-grader-semantics.md` citing the refused ids S094/S097 —
this claim repairs that draft to cite S093/S103/S104 (the draft is unadmitted until
the citations resolve; it is not new corpus bytes, it is in-flight debt). S093
(SWE-bench Pro V2 verifier files, round-31 row) is already `mined` and gains the
entry in `used-by`. The four round-32 refusal rows at S094/S097/S101/S102 stand
unchanged (ids never reused; CORPUS.md rule 2). Staged catalog rows S101/S102 are
**not** cited by this entry and are not appended (expansion is knowledge, not rows —
CORPUS.md rule 4).

**Frozen predicate (one sentence, same condition in the counter's code, same label in the receipt):**

> `corpus/knowledge/benchmark-grader-semantics.md` exists with `source:` lines citing
> exactly the three ids S093, S103, S104 (three distinct), a `verified-at: 2026-10-25`
> line, and every one of those three cited rows present in `corpus/SOURCES.md` with
> `status=mined`, `opened=2026-10-25` and `used-by` naming the entry (S093's `used-by`
> gains the entry; S103 and S104 are new rows); the entry has exactly one index row in
> `corpus/README.md`; and
> `python3 plans/adoption_check.py --expect .ufo/waves/round-33/claims/adoption-expect.json --census`
> prints `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok` and exits 0.

**Counting command:** the last clause above (`plans/adoption_check.py`, unchanged from
rounds 29–32), plus the content-level second receipt
`python3 plans/round33_c1_verify.py --lane .` → `checks=8 defects=0`, exit 0.
**Control (committed at freeze):** `.ufo/waves/round-33/claims/control-nothing.txt` —
the same counter on the pre-append tree prints `entries=0 …` and exits 1, with the
expect file's sha256 pinned in the receipt.
**Kill rule:** a cited source whose located quote cannot be found in this round's
captured bytes at the pinned revision is refused for that row (quote >25 words is
refused; exit 6/7/8/9 paths of `plans/sources_adopt.py` bind); if fewer than two of
the three cited rows survive (S093's round-31 quotes already resolve; S103 and S104
must resolve this round), the entry is not admitted and C1 is a recorded honest stop
(registry delta 0). The scratch id-collision guard (0–3 leading spaces, both id lists)
runs before any append and its proof fixture is committed under
`.ufo/waves/round-33/assimilation/`.
**Axis verdict shape:** the entry is new corpus bytes on ground the coverage map did
not hold (Toolathlon scoring code); the canonical coverage score stays 7 while the
round-25 L0 coverage cap is open, so the row records the ledger delta and an
`improved` trend, not a raised number.

## C2 — calibration: round-32 routed-defect closure, mismatch count 6 → 0

**Surface this claim moves:** the mismatches between the lane's self-assessment and
observed repo state that round 32's non-author closure routed to the lane
(`corpus/lessons/round-32-verifier-spotcheck.md` §5), plus the structural debts round
32 left: no SCORECARD round-32 section and ten uncommitted round-32 wave paths at a
pushed tip. Six items, each a location the closure or the protocol named.

**Frozen predicate:**

> `python3 plans/round33_defects.py --lane .` prints `checks=6 defects=6` and exits 1 on
> the pre-repair tree (freeze control committed at
> `.ufo/waves/round-33/claims/defects-before.txt`) and prints `checks=6 defects=0` and
> exits 0 on the repaired tree, where the six checks are exactly
> N1 every file under `.ufo/waves/round-32/` is git-tracked and no untracked path
> remains beneath it (inherited-state resolution per §5 of the round contract);
> N2 `SCORECARD.md` contains a `## Round 32` section recording round 32's dispositions;
> N3 the fleet report `.ufo/reports/round-31/kengaku.md` carries an appended erratum
> with `a44b5a8` within 400 characters of `superseded` or `erratum` and naming the real
> locator-fix commit `ae95fe0` (append-only; the original token stays);
> N4 the fleet report `.ufo/reports/round-32/kengaku.md` contains the round-32 closure
> tip `112091c` (append-only addendum);
> N5 `corpus/lessons/round-31.md` still contains `:35-38` and carries a labelled
> correction note placing `verifier_mode.py`'s precedence docstring at `:39-40`;
> N6 `corpus/lessons/round-30.md` still contains `:78-81` (or `78–81`) and carries a
> labelled correction note pointing the Q6 retraction at entry lines `:72` and
> `82-83`, and carries a labelled erratum recording S086 as published without peer review.

**Counting command:** `python3 plans/round33_defects.py --lane .`
**Control (committed at freeze):** `.ufo/waves/round-33/claims/defects-before.txt` —
the same counter on the pre-repair tree (`checks=6 defects=6`, exit 1).
**Kill rule:** an item that cannot be repaired inside the lane's write scope plus its
own filed fleet reports (append-only errata per `PROTOCOL.md`'s correction rule) is
reported as an open defect and C2 misses; a partial receipt or a selftest is not closure
(round-32 closure language, adopted verbatim).
**Separability:** reads only round-30/31/32 bytes (fleet reports, lessons, wave trees),
`SCORECARD.md`, and this round's lesson/report — no artifact C1 or C3 creates.

## C3 — freshness: public model catalogs re-probed with committed raw bytes

**Surface this claim moves:** `corpus/knowledge/open-model-catalogs.md`, re-probed
2026-10-25 in round 32 with only a summary receipt — the round-32 closure routed:
"raw API payloads are not retained; preserve bounded response bytes plus digests next
probe". This claim preserves them: a fresh live probe of both public catalogs on
2026-10-25 whose **bounded raw response bytes and sha256 digests are committed in the
lane**, with a `--verify` mode that re-derives every number offline from those bytes.

**Frozen predicate (one sentence):**

> `python3 plans/catalog_probe.py --verify --lane .` exits 0 only when
> `corpus/evidence/round33/catalogs/` contains `hf.raw.json` and `or.raw.json` (each
> ≤ 64 KiB, digests verifying against the committed `SHA256SUMS`), the receipt
> `corpus/evidence/round33/catalogs/after.txt` records `hf_models=<n> or_models=<n>
> hf_schema_delta=<d> or_schema_delta=<e>` with `<d>` naming the HF default-projection
> gap fields, every one of those numbers re-derives exactly from the committed raw
> bytes, and `corpus/knowledge/open-model-catalogs.md` carries a
> `## Re-probe 2026-10-25 (round 33)` block citing the new receipts and recording the
> same numbers; the do-nothing control (pre-probe tree) exits 1 with
> `raw=absent`.

**Counting command:** `python3 plans/catalog_probe.py --verify --lane .`
**Control (committed at freeze):** `.ufo/waves/round-33/claims/control-verify.txt` —
`--verify` on the pre-probe tree prints `raw=absent` and exits 1.
**Kill rule:** if either endpoint is unreachable from this host during the probe
window, or the captured bytes fail to parse as the expected JSON shapes, the probe is
an honest stop (no fabricated bytes may ever satisfy `--verify`; the digest check
binds the receipt to the capture). The round-32 frozen predicate (zero missing
fields) stays **failed as declared** and is not re-run as a pass.
**Separability:** reads only `corpus/evidence/round33/catalogs/`, the catalog entry,
and `plans/catalog_probe.py` — no artifact C1 or C2 creates.

## Frontier step (§2b), considerthese (§10), and disclosures

- **Sourced claim:** C1 rests on rows opened this round — S103/S104's Gate records
  carry this round's access date and ≤25-word located quotes; the admitted entry
  cites them.
- **Mistake mining:** `corpus/lessons/round-33.md` §Mistakes (class · evidence ·
  captured-by · fix); at least the round-32 lesson's `landing`-class row (summary
  receipt without raw bytes) and this round's own freeze lessons ride in.
- **considerthese:** `considerthese/2026-10-25.md` proposal 3 is actioned as an L0
  decision-packet append (what evidence lifts the round-25 coverage cap) — one report
  line names it; proposal 2's hygiene rule (a receipt is only evidence if something
  re-runs it at the tip) lands as `QUALITY.md` Q22, satisfied mechanically by C2's
  tip-reading counter and C3's `--verify` mode.
- **Inherited state:** the untracked `.ufo/waves/round-32/` tree (named by the
  round-32 closure) is committed under this round's entry via N1.
- **Assimilation guard proof:** the 0–3-space id-collision fixture runs in scratch
  before the first registry append; its red/green receipts are committed under
  `.ufo/waves/round-33/assimilation/`.
