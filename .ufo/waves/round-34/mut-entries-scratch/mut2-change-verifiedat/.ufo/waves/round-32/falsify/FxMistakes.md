# FxMistakes — final `## Mistakes` table rows for `corpus/lessons/round-32.md`

Seat `L1Kengaku32.FxMistakes` (falsify wave, round 32), 2026-10-25. Leaf: no subagent dispatch, no
production edits. Read-only verification of the build draft `R32DraftMistakes.md` and the misroot
sweep facts; every quoted byte below was re-derived in this seat (§4 receipts). Lane tip observed
`6084cd3` (`git rev-parse master` → `6084cd3492c6aef10fd66afc36ffc00e79ace94a`); the C2 repair
targets are still open at tip, with the D3/D4 repairs already prepared in the working tree.

The table below is the paste-ready `## Mistakes` section. Row shape matches the round-31 lesson
(`| class | evidence | captured-by | fix |`), class phrase carrying the one-line description.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| `reference-drift` — a report addendum cited a lane commit that never existed (routed D1) | `.ufo/reports/round-31/kengaku.md:226`: "fixed at lane tip \`a44b5a8\`-class commits"; `git cat-file -t a44b5a8` → `fatal: Not a valid object name a44b5a8`. The real locator fix is `ae95fe0` ("round-31: entry locator corrections (verifier_mode.py:18-21, :39-40) and final falsify evidence") | round-31 non-author verifier §1 hash sweep and §5 D1 | appended erratum to the filed report naming `a44b5a8` as bogus and `ae95fe0` as the locator fix (C2's R1). **criterion:** `none` — Q10 makes a second seat re-read *source* locations; no lane criterion required every cited lane-commit hash to resolve. The check existed only inside the non-author's step-1 table |
| `landing` — the report-ordering defect recurred a second round: the filed report never cites the lane commits that ended the round (routed D2) | in `.ufo/reports/round-31/kengaku.md`: `grep -c ae95fe0` → `0`, `grep -c 87f0d32` → `0`; the erratum instead names `9591131e` as "the lane tip this round actually leaves" (`:199`, `:212`) | round-31 verifier §5 D2, which also names it as round-30 §5 item 7 still open | land the report's last append **after** the last lane commit and cite that tip; C2's R2 makes it a counter check (`round32_defects.py` R2) rather than a prose instruction. **criterion:** `none` as a QUALITY row — round-30 §5 item 7 is the only statement of the rule, and it was never landed as an R-criterion, so nothing re-derived it |
| `landing` — a round-31 gate repair left the round's own CLI receipt unable to run its own command (routed D3) | `corpus/evidence/round31/gate-cli-exits.txt` at lane tip `87f0d32` and still at `6084cd3`: 5 lines read `can't open file '/…/round-31/c3-fixtures/../../../plans/sources_adopt.py'`; the run line it prints resolves to `.ufo/plans` (absent). The valid receipt is in history at `634ded8`; the working tree already carries a regenerated copy that satisfies R3's tokens (`exit=0/8/9/2`, corrected `../../../../plans/`, no `can't open file`) | round-31 non-author verifier (`.ufo/reports/round-31/kengaku.md` §5 D3); this seat re-derived the count | regenerate from the committed fixtures with `../../../../plans/` and append a correction (the receipt is append-only); the repair is C2's R3. **criterion:** Q20 requires the receipt to exist and be committed; nothing required it to re-run after a rewrite |
| `reference-drift` — an instrument shipped with no registry row, so nothing could find it (routed D4) | `git show 87f0d32:SKILL.md \| grep -c sources_adopt` → `0` (same at `6084cd3`), while `.ufo/waves/round-32/gate-receipt.txt` lists `sources_adopt: SELFTEST cases=17 failed=0`; the working tree now carries a `sources_adopt.py` row (grep count 1) | round-31 verifier §5 D4 | add the `SKILL.md` §Gate/probe registry row (C2's R4). **criterion:** the `SKILL.md` §Gate standard states "no closure grades this gate conformant until that row exists" — the criterion existed and was simply not checked by any instrument; `state_check.py` does not read the SKILL registry |
| `landing` — a falsify seat never landed, and the round's own ledger said no seat was dead (routed D5) | round-31 falsify registry: `members: 36`; committed reports at `87f0d32`: `35`; set difference `['R31FxEntryBar']` | round-31 verifier §5 D5 (`comm` of registry keys vs `git ls-tree`); this seat re-derived it | land the report or record the seat dead in the round-32 lesson's seat ledger (C2's R5; paste-ready single line in §5). **criterion:** Q19 ("a round records what its seats bought") states exactly this rule, but its own check is `test -e .ufo/waves/yield.tsv` → absent — the criterion was landed as prose in round 29 and never implemented |
| `reference-drift` — a correction sweep updated the entry and left the lesson table citing the same locator (routed D6) | `git show 87f0d32:corpus/lessons/round-31.md:57` still reads `precedence docstring (\`:35-38\`)` while the entry was corrected to `:39-40`; the round-30 lesson erratum points the Q6 retraction at entry `:78-81`, which at tip is `:72` and `:82-83` (both carry the corrected text) | round-31 verifier §5 D6 | appended correction notes in both lessons, never in-place edits (C2's R6; R6's check keeps `:35-38` present and requires `:39-40` within 300 chars of `verifier_mode.py` plus a `correction`/`superseded` label). **criterion:** Q10 — a second seat re-opening `verifier_mode.py` finds precedence at `:39-40`; Q10 existed and applies, it was not run on the lesson table |
| `reference-drift` — the round-30 lesson grouped S083/S086 as "peer-reviewed" (carried erratum debt, C2's R7) | `git show 6084cd3:corpus/lessons/round-30.md:66`: "S085 a self-report, S081/S082 preprints vs S083/S086 peer-reviewed); Q6 pass"; the S086 registry row (`corpus/SOURCES.md:110`) records the society publishes "**without peer review**" | round-31 verifier §5 "Carried debt (lane-disclosed)" | appended erratum recording S086 as published **without** peer review (C2's R7). **criterion:** Q5 ("every source is labelled for what it is") — existed, applies, was not applied to this grouping |
| `misroot` — a test fixture was committed against the **fleet root**, deleting the whole tracked tree | fleet commit `35b91714` (author/committer `t <t@t>`, 2026-10-25 09:21:14 -03, message `t`) adds `corpus/README.md`, `corpus/knowledge/a b.md`, `"corpus/knowledge/caf\303\251.md"`; `git show --stat 35b91714` → `4606 files changed, 4 insertions(+), 823070 deletions(-)`; `git diff --diff-filter=D --name-only 35b91714^ 35b91714 \| wc -l` → `4603` (its parent `0619111d` held 4603 files) | `protocol-shokunin` repair commit `f47ad6ba` (09:29:03) "repair: restore fleet tree deleted by stray commit 35b91714"; this seat verified the numbers | repair landed (`f47ad6ba`: 4607 paths, fixtures dropped, no history rewritten). Structural fix routed: the fixture-writing selftest must write under a confined path (`/tmp` or `.ufo/waves/*/scratch/`), never the repo root, and a pre-commit guard should refuse root-level writes; the fleet repo is read-only to this lane, so the structural fix is operator-side |
| `number-drift` — the repair commit's headline counts files-changed as paths-deleted | `f47ad6ba` body: "deleting 4,606 tracked paths"; the commit it describes gives `4606 files changed` = 4603 deletions + 3 additions (`git diff --diff-filter=D … \| wc -l` → `4603`; `git diff --name-status 35b91714^ 35b91714 \| grep '^A'` → 3 paths) | this seat (round-32 falsify, `FxMistakes`) | state the unit: "4,606 files changed (4,603 deleted, 3 added)", or re-derive with `--diff-filter=D`. Not repaired here — fleet bytes are read-only to this lane, so it is routed. **criterion:** Q10, and round-30 §Mistakes 1's rule that "the count is re-derived in the lesson command's own unit" |
| `reference-drift` — a one-line divergent fork of a tracked instrument sat untracked at the fleet root, under a name its own docstring does not carry | `m-rev-vs-rev.py` (8796 B, sha256 `a2a3f790e83bd7d6552f7c35eacb8ab89f319b80aa7a39ab54a51eb734764e9a`); its docstring opens `"""souji-coverage-agreement.py — coverage-map agreement instrument (round 24 C2, round 25 C1)`; `diff` against the tracked `souji-shokunin/tools/souji-coverage-agreement.py` (sha256 `bb506469…`, tracked since `1efe406`) is 2 changed lines, one substantive: `base = entry_grounds(root, base_rev, knowledge_tree(root, base_rev))` → `base = grounds`; no tracked file invokes it (sibling sweeps list it only as an untracked path — e.g. `kasegi-shokunin/.ufo/waves/round-26/wave2/AttackF1.md:60`) | this seat's misroot sweep (§3) | delete the fork (no reader) or land the change as its own commit in the owning lane; the fleet repo is read-only to this lane, so routed. **criterion:** Q3/Q5 (an instrument's identity is its tracked name and docstring) — no instrument reads the fleet root for stray forks |
| `landing` — a lane's wave-2 falsify report never landed and now sits untracked in the **fleet** wave tree | `git status --porcelain` → `?? .ufo/waves/round-24/` → `.ufo/waves/round-24/w2/RevUnlandedResolution.md` (tabi lane, target tip `ad125e85`, baseline `573c99e4`); the report's own §0 F1 is "8 untracked paths, not 0" — the report is now one of them | this seat's misroot sweep (§3); corroborated by `kasegi-shokunin/.ufo/waves/round-26/wave2/AttackF1.md:60` | land it in the owning lane's wave tree or delete it; the fleet repo is read-only to this lane, so routed to tabi. **criterion:** R2 — existed, and the fleet-root wave tree is outside every lane's R2 check |
| `vacuous` — C3's model count is a page count, so the frozen figure cannot tell a catalog from a request | `plans/catalog_probe.py:29` `HF_URL = "https://huggingface.co/api/models?limit=50"`, `:112` prints `hf_models={hf_n}`; the frozen control `.ufo/waves/round-32/claims/catalogs-before.txt:4` reads `probed=2026-10-25 hf=ok openrouter=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 entry=stale` — the HF figure equals the request's own `limit=50` | this seat, reading the counter the frozen predicate names | the claim is frozen, so the repair is an appended note in the entry/report, not a predicate change: state the figure as a page count (`limit=50`) and keep the schema-delta as the discriminating signal; a predicate change after a seat has scored is not this claim's predicate |
| `scope` — the build wave ran as two concurrent seat sets for the same items (this round's own mistake) | `.ufo/waves/round-32/build-assignments.json` held 34 `-3`-suffixed keys on this draft's first read (e.g. `"L1Kengaku32.R32ReconPackage-3"`) and 34 unsuffixed keys on a re-read, mtime `09:44:36`; `build-run.log` (mtime `09:41:08`) holds `0` `-3` names; the L1's own status line reads "Killing duplicate agent batch -2"; the surviving build registry now holds 34 members, `0` with `-3` | the L1 (main agent), which killed the duplicate; the build draft seat recorded the two reads | dispatch bo (each wave dispatched once, registry keyed by unique seat id); the seat ledger must count one set, and any duplicate scribe output (a `-3` report path) must be reconciled before the wave's reports are treated as one set. **criterion:** wave-spec dispatch is a harness contract; the duplicate set was killed before landing, so the mistake is recorded as the round's own, not as a defect |

## 5. Paste-ready seat-ledger line for R5 (single line, `R31FxEntryBar` + `dead` within 160 chars)

`plans/round32_defects.py:139` uses `near(..., width=160)`, so both tokens must co-occur on one line:

```
| falsify | 36 dispatched | `R31FxEntryBar` — dead: no report committed at round-31 tip `87f0d32` (35 of 36 landed); recorded per routed defect D5 | 0 |
```

## 4. Receipts (this seat's independent re-derivation)

**Fleet incident (row: misroot + number-drift):**

```
$ git show --stat --format='%H%nauthor=%an <%ae>%ncommitter=%cn <%ce>%ndate=%ad%n%s%n%b' 35b91714 | head -16
35b91714722fd2314c6b22839c446a116d1a5ffb
author=t <t@t>
committer=t <t@t>
date=Sun Oct 25 09:21:14 2026 -0300
t
...
 4606 files changed, 4 insertions(+), 823070 deletions(-)
$ git diff --diff-filter=D --name-only 35b91714^ 35b91714 | wc -l
4603
$ git diff --name-status 35b91714^ 35b91714 | grep '^A'
A	corpus/README.md
A	corpus/knowledge/a b.md
A	"corpus/knowledge/caf\303\251.md"
$ git show --stat --format='…%s%n%b' f47ad6ba | head -6
repair: restore fleet tree deleted by stray commit 35b91714 (author t <t@t>, 09:21:14 -03)
A test fixture (corpus/README.md, 'a b.md', 'cafe.md') was committed against the fleet
root, deleting 4,606 tracked paths. This commit restores the tree of 35b91714^ (0619111d) …
$ git ls-tree -r --name-only f47ad6ba | wc -l
4607
```

**Misroot candidate 1 (fork):**

```
$ sha256sum m-rev-vs-rev.py souji-shokunin/tools/souji-coverage-agreement.py
a2a3f790e83bd7d6552f7c35eacb8ab89f319b80aa7a39ab54a51eb734764e9a  m-rev-vs-rev.py
bb506469be860f994f74f4c7d6eb1c949a4931b676cdb60f9f79de041d12f27f  souji-shokunin/tools/souji-coverage-agreement.py
$ diff souji-shokunin/tools/souji-coverage-agreement.py m-rev-vs-rev.py
118c118
<     base = entry_grounds(root, base_rev, knowledge_tree(root, base_rev))
---
>     base = grounds
$ git ls-files | grep -c m-rev-vs-rev
0
```

**Misroot candidate 2 (tabi wave report):**

```
$ git status --porcelain | grep 'round-24\|m-rev'
?? .ufo/waves/round-24/
?? m-rev-vs-rev.py
$ ls -la --time-style=full-iso .ufo/waves/round-24/w2/RevUnlandedResolution.md
-rw-r--r-- 1 vgpnk vgpnk 15891 2026-10-25 05:55:04.010735389 -0300 .ufo/waves/round-24/w2/RevUnlandedResolution.md
$ sed -n '1,20p' .ufo/waves/round-24/w2/RevUnlandedResolution.md
# RevUnlandedResolution — routed defect 2 (89 unlanded paths): closure composition
Seat `L1Tabi24.RevUnlandedResolution`, round 24 wave 2, falsification pass.
Target: lane tip `ad125e85c235e1c4ec6a08e398bd64da01f68a08` …
- **F1 (HIGH) — the closure condition does not hold: 8 untracked paths, not 0.** …
```

**Routed defects (open at tip):**

```
$ git cat-file -t a44b5a8
fatal: Not a valid object name a44b5a8
$ git log --oneline -1 ae95fe0
ae95fe0 round-31: entry locator corrections (verifier_mode.py:18-21, :39-40) and final falsify evidence
$ grep -c "ae95fe0" .ufo/reports/round-31/kengaku.md   → 0
$ grep -c "87f0d32" .ufo/reports/round-31/kengaku.md   → 0
$ sed -n '226p' .ufo/reports/round-31/kengaku.md
fixed at lane tip `a44b5a8`-class commits (`verifier_mode.py:22-23` → **`:18-21`** for the "Returns the
$ git show 6084cd3:corpus/evidence/round31/gate-cli-exits.txt | grep -c "can't open file"
5
$ git show 6084cd3:SKILL.md | grep -c sources_adopt
0
$ sed -n '66p' <(git show 6084cd3:corpus/lessons/round-30.md)
  S085 a self-report, S081/S082 preprints vs S083/S086 peer-reviewed); Q6 pass (§Extends names both
$ grep -n "S086" corpus/SOURCES.md | head -1
110:| S086 | … the society publishes these proceedings **without peer review** …
$ sed -n '57p' <(git show 6084cd3:corpus/lessons/round-31.md)
57:| S092 | …/src/harbor/models/task/verifier_mode.py | "or VerifierEnvironmentMode.SHARED" (2, `:31`); precedence docstring (`:35-38`) | …
$ sed -n '72p;82,83p' corpus/knowledge/contamination-transparency-card.md
72:So the delta is one field, and the rest is not a delta at all. …
82:is the authoritative status. Two earlier readings of this paragraph ("two new fields", then "one field, one
83:placement, one value set") overclaimed; this is the corrected one, …
```

**Duplicate dispatch (current state):**

```
$ python3 -c "import json; d=json.load(open('.ufo/waves/round-32/build-assignments.json')); ks=list(d); print(len(ks), sum(1 for k in ks if k.endswith('-3')))"
34 0
$ grep -o 'R32[A-Za-z0-9]*-3' .ufo/waves/round-32/build-run.log | sort -u | wc -l
0
$ ls -la --time-style=full-iso .ufo/waves/round-32/build-assignments.json .ufo/waves/round-32/build-run.log
-rw-r--r-- 1 vgpnk vgpnk  1578 2026-10-25 09:44:36.993837471 -0300 .ufo/waves/round-32/build-assignments.json
-rw-r--r-- 1 vgpnk vgpnk 55207 2026-10-25 09:41:08.450395767 -0300 .ufo/waves/round-32/build-run.log
```

**C3 vacuous:**

```
$ grep -nE "limit|hf_models" plans/catalog_probe.py | head -4
29:HF_URL = "https://huggingface.co/api/models?limit=50"
112:        f" hf_models={hf_n} or_models={or_n}"
$ grep -n "hf_models" .ufo/waves/round-32/claims/catalogs-before.txt
4:probed=2026-10-25 hf=ok openrouter=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 entry=stale
```

## 6. Notes for the lesson drafter

- Rows D1–D6 + R7 are the round-31 closure's routed debt, not this round's mistakes; their class column
  is the mapping the lesson asks for. The C2 counter closes them (R1–R7) when the repairs land.
- The fleet-level rows (35b91714 incident, number-drift headline, the two today-misroot candidates) are
  recorded because this lane reports into that tree; none is kengaku-authored and none may be repaired by
  a kengaku seat (fleet repo read-only).
- The `vacuous` C3 row is a hazard in this round's **frozen** claim, not in a landed artifact; the
  predicate must not be rewritten after a seat has scored it — the repair is an appended note.
- The duplicated-dispatch row is this round's own mistake; the kill already happened, so it is recorded
  as evidence, not as an open defect.
- The working tree already carries the D3 regenerated receipt and the D4 SKILL registry row; they are
  uncommitted repairs belonging to the C2 closure seats, not to this table.

VERDICT: mistakes-final
