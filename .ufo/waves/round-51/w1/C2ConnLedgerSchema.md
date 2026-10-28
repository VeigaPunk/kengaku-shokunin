# C2ConnLedgerSchema — cross-lane ledger schema scan (round 51, w1)

Seat: `C2ConnLedgerSchema` (connector). Lane: `kengaku-shokunin`.
Item: do sibling lanes' defect/routed-finding ledgers carry an owner or disposition field —
is round 51's C2 schema a lane-local repair or a fleet-wide gap worth routing?

**Axes named.** Primary: **adjacency** (C2's axis; `AXES.md:16` — "Cross-domain awareness —
evidence belonging to another domain reported, not absorbed"). Secondary kept unharmed:
**freshness** (C1) — nothing here reads or writes C1's surfaces (`PROVINCE.md`,
`round51_surfaces.py`, `round51-surfaces.json`); no file I touch is C1's. No third axis is moved.

**Revision measured.** `REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7` (kengaku HEAD,
branch `master`, at `2026-10-28T15:22–15:24-03:00`). The stage-1 freeze commit
`e07f131cf7037e58a21db6e1f3986cf401ad257c` is an ancestor of HEAD
(`git merge-base --is-ancestor e07f131 HEAD` → true); HEAD is one commit later
(`4090c3d round-51: v2 wave spec (64 seats) + validated dispatch payload`). Sibling lanes were
read at their working trees; every ledger I quote is **clean** at its lane tip
(`git -C <lane> status --porcelain -- <file>` → empty), at these tips:

```
kagi-shokunin          69b61db4   tabi-shokunin     2844de30   tsukuroi-shokunin  ff916972
souji-shokunin         2605bf20   tameshi-shokunin  981c5e8b   kama-shokunin      7ee8cbdf
kaidoku-shokunin       61b87d74   lore-shokunin     380ef3ab   mori-shokunin      325f7e63
kotoba-shokunin        47dbe878
```

Read-only throughout. No production file, sibling repo, fleet-root file, `MANIFEST.json`,
`.ufo/state`, or `.scratch/` was written. No commit, no mutating git. Scratch
`/fast/scratch/hyaku/kengaku-r51/C2ConnLedgerSchema` was created and **removed** before yield
(no clone was needed; no fixture git call was made). No tool was installed — nothing was needed,
so no pacman/uv/npx transaction occurred.

## 1. The literal sweep: `*-shokunin/corpus/*.jsonl`

```sh
for d in *-shokunin; do n=$(ls "$d"/corpus/*.jsonl 2>/dev/null | wc -l); printf '%-26s %s\n' "$d" "$n"; done
```

Observed (21 lanes scanned; only non-zero shown):

```
kengaku-shokunin           3
```

**Result: 20 of 21 lanes have zero `corpus/*.jsonl`.** The only JSONL ledgers in the fleet are
kengaku's own: `corpus/routed-findings.jsonl`, `corpus/defects.jsonl`,
`corpus/defects-round35.jsonl`. Fleet-wide, `find . -maxdepth 3 -name 'routed-findings*'` returns
exactly two paths — `./kengaku-shokunin/corpus/routed-findings.jsonl` and
`./lane3/corpus/routed-findings.jsonl`; `lane3/` is a stale mirror of this lane (same file set,
same lesson names), **not** a sibling lane, and is not counted.

A `.jsonl`-only answer would therefore be misleading: siblings keep defect and adjacency records
in `.json`/`.tsv` registers. The widened scan below is the substantive evidence.

## 2. Per-lane ledger table (production paths; wave receipts, `.ufo/`, `reports/`, `tests/`,
`corpus/evidence/`, `corpus/live/`, `__pycache__` excluded)

Field sets are the first row's keys (JSONL/JSON) or the documented column list (TSV).
"owner?" = a field naming **which lane owns the item**; "disposition?" = a field naming **what
was decided about it**.

| Lane | Defect / routed-finding ledger | Field set | owner? | disposition? |
|---|---|---|---|---|
| kengaku | `corpus/routed-findings.jsonl` (71 rows) | id, class, source, opened_round, status, close, blocker, check, note | **no** | **no** |
| kengaku | `corpus/defects.jsonl` (5) / `defects-round35.jsonl` (4) | id, class, opened_round, source, check, status, closed_round, recurrence_of | **no** | no (`status` only) |
| tameshi | `corpus/routed-defects.json` (49) | id, status, evidence, commit, seat, note, reason | **no** (`seat` = working seat, not lane) | no (`status` = fixed/declined/open) |
| kagi | `corpus/closure-dispositions.json` | id, class, disposition, note, pointer | **no** | **yes** (`no-action`, …) |
| kagi | `corpus/adjacency.tsv` (4 data rows) | path, **owner**, status, claim, basis, token, note | **yes** | yes (`status`: writer/shared-read/contested/unresolved) |
| kagi | `corpus/claim-ledger.tsv` | id, command, expect, exit, timeout, note | no | no |
| tabi | `corpus/adjacency.tsv` (16 data rows) | surface, sibling, sibling_ref, sibling_quote, tabi_ref, tabi_quote, **disposition**, ruling_ref, ruling_quote | **no** (`sibling` names the *other* lane) | **yes** (ruled 1, contested-open 4, split-declared 8, refused-route 3) |
| tabi | `corpus/adjacency-screen*.tsv` | sibling_ref, reason, surface, quote, note (drift variant: sibling_ref, status, note) | no | `status` only |
| tsukuroi | `corpus/knowledge/adjacency-mori-oom-r27.json` (6 rows) | id, sibling, sibling_commit, sibling_path, sibling_blob_sha256, snapshot, heading, quote, quote_line, lane_path, lane_quote, class, **owner**, action | **yes** (`owner`: tsukuroi / mori) | yes (`action` states the routed act) |
| tsukuroi | `corpus/knowledge/adjacency-handoffs-fleet-r1.json` | id, trigger, retains, **recipient**, sources, minimum_evidence, counterexample, negative_recipient, state, state_evidence, forbidden_inference | **yes** (`recipient`) | yes (`state`) |
| tsukuroi | `corpus/knowledge/adjacency-anchors-r19.json` | id, province_pointer, sibling, sibling_path, sibling_commit, sibling_blob_sha256, snapshot, heading, quote, quote_line, proposition | no | no |
| souji | `census/round-29/waves/w1/deliver-defect-disposition.tsv` (6 data rows) | defect, routed_statement, **addressed_by**, addressed, observable_command, base_observation, residual_and_handling, location | partial (`addressed_by` = claim + seat ids, e.g. "claim C2; items C2ToolV2 …", not a lane id) | **yes** (in the name; `addressed` = "yes (planned, claim C2)") |
| souji | `corpus/pointer-exemptions.tsv` | path, note (no header) | no | no |
| kama | `registry/verdict-ledger.tsv` / `claim-outcome-ledger.tsv` | round, trend\|claim, side, verdict\|outcome, repo, rev, path, line, note | **no** (`repo` = fleet\|lane; `side` = self\|outside) | verdict/outcome only |
| kaidoku | `corpus/claim-freezes.tsv` / `-v2.tsv` | round, verdict, findings, pointer | no | `verdict` only |
| kasegi | `corpus/instruments/limb-ledger.json` | id, instrument, find, replace, kill, live_exit, signal, note | no | no |
| lore | `corpus/knowledge/r102-debt-ledger.json` | round, file, seat, items_in_source, own_items, carry_records | no | no |
| mado | `quality/tool-ledger.md` (markdown, not data) | — | no | no |
| mori | `tools/mori-routed-check.py` (instrument; no data ledger) | greps md prose for `routed defects?\|items?`; **no** owner/disposition/next handling (`grep -E 'owner\|disposition\|assignee\|routed_to\|target_lane\|next'` → no match) | no | no |
| kotoba | `verifiers/check_routed_repairs*.py` (instrument) | same grep → no match; verifies repair claims, not ownership | no | no |
| kumitate | `scripts/routed-ledger.mjs` (instrument; parses md routed-item blocks) | no owner/disposition handling | no | no |
| audio, chousa, game-dev-2d, game-dev-3d, kake, kotodama, revenger | **no production defect/routed-finding ledger** | — | — | — |

Verbatim supporting rows:

```
# kagi-shokunin/corpus/adjacency.tsv:9
# Columns (row lines): path <TAB> owner <TAB> status <TAB> claim <TAB> basis <TAB> token <TAB> note

$HOME/.config/opencode                                              | integrator | unresolved
$HOME/.local/share/the-musketeer/chrome-profile                     | kake       | contested
$HOME/.local/share/the-musketeer/chrome-profile/NativeMessagingHosts| kagi       | writer
$HOME/.agents/AGENTS.md                                             | kotoba     | shared-read
```

```
# tsukuroi-shokunin/corpus/knowledge/adjacency-mori-oom-r27.json
{'id': 'OV2', 'sibling': 'mori', 'class': 'INBOUND-DRIFTED', 'owner': 'mori',
 'action': "Report to mori: its PROVINCE.md line 66 names lane PROVINCE.md lines 21-24 and
            35-44, which are now lines 30-33 and 44-53 … Mori re-pins its own pointer;
            tsukuroi edits nothing of mori's."}
{'id': 'OV5', 'sibling': 'mori', 'class': 'CONFLICTS', 'owner': 'mori', …}
{'id': 'OV1', 'sibling': 'mori', 'class': 'INBOUND-RESOLVES', 'owner': 'tsukuroi', …}
```

```
# souji-shokunin/census/round-29/waves/w1/deliver-defect-disposition.tsv:1
defect|routed_statement|addressed_by|addressed|observable_command|base_observation|residual_and_handling|location
```

## 3. What the fleet actually has

- **Owner attribution exists in the fleet — but only on adjacency/ownership registers, never on a
  defect or routed-finding ledger.** Three independent private schemas:
  kagi `owner`+`status` (surface partition, 4 rows, values `kagi|kake|kotoba|integrator`);
  tsukuroi `owner`+`action` (6 routed rows, values `tsukuroi|mori`);
  tsukuroi `recipient`+`state` (fleet handoffs).
- **Disposition exists in the fleet — on defect ledgers too, but without an owner:**
  tameshi `routed-defects.json` (`status`: fixed 31 / declined 11 / open 7, 49 rows, plus a
  free-text `reason`), kagi `closure-dispositions.json` (`disposition: no-action`), tabi
  `adjacency.tsv` (4-value controlled vocabulary `ruled | contested-open | split-declared |
  refused-route`, validated by `scripts/check-adjacency.mjs:77`), souji
  `deliver-defect-disposition.tsv` (`addressed`).
- **No lane carries both on a defect/routed-finding ledger.** kengaku's `routed-findings.jsonl`
  is the only routed-findings ledger in the fleet and carries neither field
  (`git show HEAD:corpus/routed-findings.jsonl` → 71 rows, keys
  `blocker, check, class, close, id, note, opened_round, source, status`).
- **The fleet axis does not specify a schema.** `AXES.md:16` says only "Lane reports name
  contested scope; integrator arbitrates" — it requires naming, not a field set, and assigns
  arbitration to the integrator.

**Judgment.** Round 51's C2 is a **lane-local repair of a lane-local instrument** — no fleet
schema exists to conform to, and `AXES.md` does not demand one. But the *gap* is fleet-wide in a
narrower, real sense: the two concepts the axis needs (owner, disposition) are each solved
privately in 2–3 lanes with mutually incompatible vocabularies, and the one artifact class that
matters for "reported, not absorbed" — a routed-findings ledger — has exactly one instance
fleet-wide and it has neither field. Round 51's schema is the first to require both, on the class
where they matter. That is worth **routing** as an integrator question, not absorbing: whether a
fleet-level routed-findings schema should exist, and if so whose vocabulary wins
(kagi's `owner`+`status`, tabi's 4-value `disposition`, tsukuroi's `owner`+`action`).

## 4. Instrument finding (C2 counter, read-only probe — routed, not fixed here)

The claims text says every `owner` names "a fleet lane from `../shokunin.conf`". Measured by
importing the frozen counter's own function at HEAD:

```sh
cd kengaku-shokunin && python3 -c "
import importlib.util; from pathlib import Path
spec=importlib.util.spec_from_file_location('r51','plans/round51_routing.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
o=m.load_owners(Path('..').resolve()); print(len(o))"
```

Observed:

```
owner set size 17
lanes on disk 21
lanes NOT accepted as owner: ['audio', 'game-dev-2d', 'game-dev-3d', 'lore', 'mado', 'revenger', 'tsukuroi']
non-lane entries accepted: ['aggregator', 'protocol', 'unowned:integrator']
```

Cause: `load_owners` matches `^\s{0,6}([a-z][a-z0-9-]{2,15}):\s*\{`, but `shokunin.conf`'s lane
block is pipe-delimited (`LANES="` … `lane-id|repo|axes`), so **zero** lines match and the owner
vocabulary is 100% the hardcoded `FALLBACK_OWNERS`. Consequences for C2 at landing:

1. A row owned by `tsukuroi`, `mori`'s neighbours in that list, `audio`, `lore`, `mado`,
   `revenger`, `game-dev-2d/3d` is rejected as "not a fleet lane" even though the lane exists —
   and `tsukuroi` is the most likely non-kengaku owner for an adjacency finding (it is the lane
   that already keeps `owner`-attributed routed rows). The predicate can therefore fail for a
   *correct* attribution.
2. The claims' stated provenance ("from `../shokunin.conf`") is false at this tip; the real
   vocabulary is a frozen constant in the counter. That is a C1-style truth defect living inside
   C2's instrument.

I did not edit the counter (read-only seat). Proposed routed row for the L1 to consider:
`owner: kengaku`, `disposition: fixed-verified` after repair, `check:` a command asserting every
lane under `../*-shokunin` is accepted by `load_owners` (the probe above, inverted).

## 5. Live-write observation (do not treat the ledger as quiescent)

At `15:22:02-03:00` (`stat` mtime of `corpus/routed-findings.jsonl`) one read of the ledger
returned `rows 0`; `wc -l` in the same minute returned `71`, and three consecutive re-reads
returned `run rows= 71 keys= 9` each. The 0-row read is **not reproducible** and I do not claim a
defect: the file is 48957 bytes, 71 lines, clean against HEAD, and the L1 is landing concurrently.
Recorded so the landing receipt pins `REV` — a 0-row ledger parses as `rows=0`, which C2's
predicate would report as a pass on an empty ledger (`LEDGER rows=0`, no failing counters). That
is a predicate-shape risk for the L1 to note: the kill rule says row count must not fall below 71,
so the guard is the kill rule, not the counter.

## 6. Limits

- I surveyed **production** ledgers only. `.ufo/` wave receipts, `reports/`, `tests/`,
  `corpus/evidence/` and `corpus/live/` were excluded; a sibling may hold an owner-attributed
  register there that never reached its corpus.
- `audio`, `chousa`, `game-dev-2d`, `game-dev-3d`, `kake`, `kotodama`, `revenger` have no
  defect/routed ledger I could find by name pattern (`defect|routed|finding|open-item|adjacency|
  *ledger*`); absence of a *matching name* is not proof of absence of records — several keep
  findings in per-round markdown (`kotodama/reports/round-*/adjacency.md`).
- Field sets are read from the first data row; a later row with extra keys would not show
  (tameshi's `reason` was found this way — its union is `commit, evidence, id, note, reason, seat,
  status`, first row lacks `reason`).
- Sibling tips are working-tree states; the cited ledgers are clean, so they equal their tips.
- I did not run `plans/round51_routing.py --run-checks`; that is not my item and it executes 61
  shell commands. The owner-vocabulary result above comes from calling its `load_owners` directly.

VERDICT: **Owner/disposition attribution on defect/routed-finding ledgers is a fleet-wide gap, not
a lane-local quirk.** Zero of 21 lanes carry both fields on such a ledger; kengaku's
`routed-findings.jsonl` (71 rows, 9 fields, no `owner`, no `disposition`) is the only
routed-findings ledger in the fleet. Adjacency registers in kagi (`owner`+`status`), tsukuroi
(`owner`+`action`, `recipient`+`state`) and tabi (`disposition`, 4-value vocabulary) prove the
pattern is implementable but each invented a private schema; `AXES.md:16` specifies no field set.
Round 51's C2 is a correct lane-local repair of a lane-local instrument and should land as such;
the fleet-level question (unify, or rule the divergence acceptable) is an integrator call and is
worth one routed row with a non-kengaku owner. Second finding, for the L1: `load_owners` accepts
17 names, rejects 7 real lanes (`tsukuroi` among them) because `shokunin.conf` is pipe-delimited,
so C2's owner vocabulary is hardcoded, not conf-derived as the claims state.
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
