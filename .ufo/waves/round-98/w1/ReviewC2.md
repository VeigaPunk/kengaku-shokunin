# ReviewC2 — R98-C2 correctness review (round 98), measured T `8e37fc65d5649bb37166fdd6b1657445a8cb55b9`

Reviewer: ReviewC2 (leaf). Method: isolated `git clone --shared` detached at T under scratch, TMPDIR
pinned; no lane/repo mutations. Ran the frozen counter (`plans/round98_c2_nested_bind.py`), the gate
(`plans/anchor_digest_check.py`) in BASE and T worktrees with `--verbose`, and the builder
(`plans/round98_provenance_build.py`); diffed every gate line (DEFECT/BIND/RESOLVED/UNBOUND) BASE↔T;
validated PROVENANCE.md against the frozen POP and the SOURCES rows; checked prov_url collisions with
`round37/anchor-captures/PROVENANCE.md`; row-level SOURCES diff and BASE..T `diff --name-status`.
Receipts: `.ufo/waves/round-98/w1/ReviewC2/` (c2-predicate-run.txt, gate-base.txt, gate-rev.txt,
built-prov.md, side-effect-census.txt).

## Predicate

**PASS at T, independently reproduced:** `LEGS K1..K7 pass`, `TARGET pop=39 cleared=39 still=0
unbound=0 rows_changed=0 captures_changed=0 new_old_row_defects=0`, `PREDICATE R98-C2 pass`, rc 0.
Gate bytes identical at BASE and T (`11bb2cad…`, sha256sum verified in both worktrees).

## Population rule: applied exactly as the claims file states — no exception found

- All 39 POP rows satisfy the stated rule. Verified against BASE gate output: each has exactly one
  defect, class `anchor-unbound`, detail `no-capture-for-upstream-<task>/<sub>/<file>-task=<sub>`,
  64-hex token equal to the sha256 of a committed nested capture; expected capture = highest-round
  match (script docstring). K2 re-derivation at BASE == frozen POP == P1 receipt
  `.ufo/waves/round-98/L1/c2-pop.txt` (byte-compared; `# GATE_SHA 11bb2cad… n=39`).
- Named exclusions verified eligible-excluded:
  - **S213** (corpus/SOURCES.md:228): 2 defects at BASE — `anchor-unbound` (token `a540714e…`, same
    capture as S201) plus `token-outside-anchor` (prose "sha256 below" in the scope cell parses as
    token `be`). Excluded by the "only `anchor-unbound`" clause. Still defective at T (the
    outside-cell token remains).
  - **S220** (SOURCES.md:235): single `anchor-unbound` nested defect, but token `58cf3c84…` is the
    sha256 of **no committed nested capture** — fails the sha clause. Still `anchor-unbound` at T.
  - **S300** (SOURCES.md:316): 3 defects (two anchor tokens → two `anchor-unbound`; one
    `token-outside-anchor`). Excluded by the "only" clause; untouched at T.
- S324/S325 exist at BASE as rejected rows without anchor claims — outside the rule, correctly absent.
- **No ineligible row is in POP.**

## F1 — MATERIAL: PROVENANCE.md's URL column eliminates a standing defect on a row outside the population (S230)

Mechanism: the builder writes each table line's URL column from the row's own pinned URL
(`plans/round98_provenance_build.py:46`). The gate turns every PROVENANCE.md line URL into a
`prov_url[(repo, subpath)]` entry (`plans/anchor_digest_check.py:233-236`, `setdefault` first-wins;
`corpus/evidence/PROVENANCE.md` sorts before `round37/anchor-captures/PROVENANCE.md`), and `bind_row`
consults `prov_url` at the rule-2 fallback (`anchor_digest_check.py:327-329`) — **before** the row's
own explicit lane path (rule 3, `:336-347`).

- **S230** (corpus/SOURCES.md:246) shares S234's pinned URL. At BASE it bound by its own row-path to
  `corpus/evidence/round52/graders/SHA256SUMS`, so its anchor token `115de2e9…` (the sha256 of
  `kv-store-grpc/tests/test_outputs.py`) was flagged **`digest-wrong-capture`** — exactly the
  cross-capture substitution defect class this gate was created to catch (gate docstring, F37A-1 /
  mutants M4b/M5). At T the new `prov_url` entry shadows the row-path: S230 rebinds
  `by=provenance-url` to the round52 capture and goes **1 → 0 defects, fully green**.
- S230 is not in POP (its only defect was `digest-wrong-capture`, not `anchor-unbound` — the frozen
  rule excludes it), and PROVENANCE.md contains no S230 line: the effect is a pure side channel of
  the URL column. `grep -rn 'S213|S230|S237|S272|side'` over plans/round-98-claims.md,
  controls/README.md and PROVENANCE.md finds **no disclosure**.
- The frozen counter cannot see it: K7 (`plans/round98_c2_nested_bind.py:172-180`) detects only
  **added** defect classes on BASE rows; class removals pass silently. TARGET is POP-scoped. The only
  trace is the informational line `GATE defects base=86 rev=45` = **−41, not the population's 39** —
  numerically visible pre-freeze (`controls/c2-positive-run{1,2}.txt` print the same line) and waved
  off by the claims file as "informational … (it counts rows outside the population)"
  (plans/round-98-claims.md, R98-C2 section), without naming the changed rows.
- Substance: S230's token **is** the true digest of the capture (S234's provenance-row binding
  resolves the same (sid, token, capture) triple green), so the lane's final state is factually
  correct — but under the round's own governance ("a defect found after F … is never repaired in
  round"), the new file **repairs a standing non-population defect in round, undeclared**, and the
  claims sentence "The change binds each row … through the gate's provenance-row rule" does not cover
  it (S230 is bound by provenance-**URL**, a different rule, and is not "each row" of any claim).
- Avoidable: gate rule 1 needs only the sid + backticked filename; the URL column is documentation. A
  3-column table (row | file | sha256) produces byte-identical K3/K4 outcomes with **zero** side
  effects.

## F2 — MEDIUM: same mechanism clears S213's `anchor-unbound` (second undeclared verdict change, benign direction)

S213 ("correction row superseding S201, same source and capture", SOURCES.md:228) shares S201's URL;
its `anchor-unbound` token `a540714e…` equals the round52 chess-best-move capture sha and is cleared
at T `by=provenance-url`. The row keeps its `token-outside-anchor` defect, so nothing is fully hidden
— but this is a second verdict flip on a row the frozen rule declared ineligible, via a route
(provenance-url) the claim does not describe.

## F3 — LOW: binding redirection on green/claim-less rows (S237, S272)

- **S237** (SOURCES.md, "supersedes S234 teaches form"): BASE row-path binding to
  `round66/sources/kv-store-grpc-test_outputs.py` → T provenance-url binding to the round52 capture;
  green both ways only because the two captures are byte-identical. An external file now outranks the
  row's own locator for an untouched row.
- **S272**: unbound → bound via provenance-url; carries no anchor token, so no claim is raised either
  way (the gate's stated presence limit).
- No defect delta; binding provenance changed on rows the claim implies are untouched.

## F4 — INFO: counter blindness

K7 is addition-only by design; no leg censuses defect removals or binding redirects outside POP. The
17 committed C2 control pairs (`controls/c2-*-run{1,2}.txt`, all present) do not include a
side-effect census. The claims file pre-declares the GATE line informational, which converts the −41
anomaly into a non-predicate datum rather than a finding.

## What passed (freshness honesty, population scope)

- The 39 digest claims are genuinely re-verified against committed capture bytes through the gate's
  own designed extension point (rule 1, the same mechanism round37 used for S070–S074); K4 pins the
  exact expected capture paths, K6 pins their bytes. **For the population this is freshness, not
  relabelling.**
- PROVENANCE.md is deterministic: byte-identical to `round98_provenance_build.py` output at T; 39
  data lines; every sid ∈ POP; file+sha256 columns match POP exactly; the URL column equals the
  row's own first pinned URL; no stray S-ids; no collision with round37's `prov_url` keys (38 unique
  ours vs 4 theirs, intersection ∅).
- "No SOURCES row or capture changes": row-level diff BASE→T shows 0 changed, 0 removed, exactly
  +S326–S333 (C1's); `diff --name-status` shows additions only under `corpus/evidence` (no capture
  byte modified anywhere in the tree, not just POP paths).
- All still-red rows outside the change (31 UNBOUND at T, incl. S220/S300) remain honestly red.

## Verdict

R98-C2's frozen predicate is **met at T**, and the population rule is applied exactly as frozen
(eligible: none excluded; ineligible: none included; S213/S220/S300 exclusions all correct). The
claim **as written is materially incomplete**: the single new file also flips gate verdicts on two
non-population rows (S230: standing `digest-wrong-capture` eliminated; S213: `anchor-unbound`
cleared) and redirects bindings on two more (S237, S272), none disclosed, none falsifiable by the
counter. Recommendation: report the claim met-with-finding (or route per round governance to round
99), and either drop the URL column from the provenance table (removes all four side effects with no
predicate change) or amend the claims text to declare the four-row side effect and make the counter's
census symmetric (detect defect removals and binding redirects outside POP).

Residual risk / gaps: `prov_url` keys ignore the pinned commit (key is `(repo, subpath)`); all rows
involved cite the same commit `2fd12b88`, so no commit mismatch materialized, but a future row citing
a different commit of the same path would silently bind to this file's captures. C1 and the census
were not re-run (scoped per assignment); controls receipts were not independently re-executed.
