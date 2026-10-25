# R32DraftMistakes — `## Mistakes` rows for `corpus/lessons/round-32.md`

Seat `L1Kengaku32.R32DraftMistakes`, round 32 build wave, 2026-10-25. Leaf: no subagent dispatch,
no production edits. Lane tip observed: `6084cd3` ("round-32: freeze-commit gate receipt (Q20
out-of-band)"); fleet HEAD observed: `6b0a9f0c`. Everything below is read-only: `git log/show/diff/
status/cat-file/ls-tree` and `python3` over files the lane already holds. No tool was installed or
upgraded this seat. Nothing in this file is a claim of a check I did not run; every quoted byte is
pasted with the command that produced it in §4.

Two things the drafter of the lesson must know before pasting:

1. The rows below are the paste-ready table. Row order follows the round-31 lesson's own table shape
   (`| class | evidence | captured-by | fix |`), with the class phrase carrying the one-line
   description, as round-31 does.
2. The C2 counter's R5 check needs a *single line* of the lesson to contain both `R31FxEntryBar` and
   `dead` within 160 characters (`plans/round32_defects.py:64-69` — `near()` uses `.` without
   `re.DOTALL`, so the two tokens must co-occur on one line). The paste-ready seat-ledger line is in
   §6.

---

## 1. Paste-ready `## Mistakes` table

| class | evidence | captured-by | fix |
|---|---|---|---|
| `landing` — a round-31 gate repair left the round's own CLI receipt unable to run its own command (routed D3) | `corpus/evidence/round31/gate-cli-exits.txt` at lane tip `87f0d32` and still at `6084cd3`: 5 lines read `can't open file '/…/round-31/c3-fixtures/../../../plans/sources_adopt.py'`; the run line it prints is `cd .ufo/waves/round-31/c3-fixtures && … python3 ../../../plans/sources_adopt.py`, which resolves to `.ufo/plans` (absent). The valid receipt is in history at `634ded8` | round-31 non-author verifier (`.ufo/reports/round-31/kengaku.md` §5 D3); this seat re-derived the count | regenerate from the committed fixtures with `../../../../plans/` and append a correction (the receipt is append-only); the repair is C2's R3. **criterion:** Q20 requires the receipt to be committed with the landing, not that its command resolves after a rewrite — so Q20 caught half of it; the missing half is "a receipt re-derives its own command", which no QUALITY row states |
| `reference-drift` — a report addendum cited a lane commit that never existed (routed D1) | `.ufo/reports/round-31/kengaku.md:226`: "fixed at lane tip \`a44b5a8\`-class commits"; `git cat-file -t a44b5a8` → `fatal: Not a valid object name a44b5a8`. The real locator fix is `ae95fe0` ("round-31: entry locator corrections (verifier_mode.py:18-21, :39-40) and final falsify evidence") | round-31 verifier §1 hash sweep and §5 D1 | appended erratum to the filed report naming `a44b5a8` as bogus and `ae95fe0` as the locator fix (C2's R1). **criterion:** `none` — Q10 makes a second seat re-read *source* locations; no lane criterion required every cited lane-commit hash to resolve. The check existed only inside the non-author's step-1 table |
| `landing` — the report-ordering defect recurred a second round: the filed report never cites the lane commits that ended the round (routed D2) | in `.ufo/reports/round-31/kengaku.md`: `grep -c ae95fe0` → `0`, `grep -c 87f0d32` → `0`; the erratum instead names `9591131e` as "the lane tip this round actually leaves" (`:199`, `:212`) | round-31 verifier §5 D2, which also names it as round-30 §5 item 7 still open | land the report's last append **after** the last lane commit and cite that tip; C2's R2 makes it a counter check (`round32_defects.py` R2) rather than a prose instruction. **criterion:** `none` as a QUALITY row — round-30 §5 item 7 is the only statement of the rule, and it was never landed as an R-criterion, so nothing re-derived it |
| `reference-drift` — an instrument shipped with no registry row, so nothing could find it (routed D4) | `git show 87f0d32:SKILL.md \| grep -c sources_adopt` → `0` (same at `6084cd3`), while `.ufo/waves/round-32/gate-receipt.txt` lists `sources_adopt: SELFTEST cases=17 failed=0` | round-31 verifier §5 D4 | add the `SKILL.md` §Gate/probe registry row (C2's R4). **criterion:** the `SKILL.md` §Gate standard states "no closure grades this gate conformant until that row exists" — the criterion existed and was simply not checked by any instrument; `state_check.py` does not read the SKILL registry |
| `landing` — a falsify seat never landed, and the round's own ledger said no seat was dead (routed D5) | round-31 falsify registry: `members: 36`; committed reports at `87f0d32`: `35`; set difference `['R31FxEntryBar']` | round-31 verifier §5 D5 (`comm` of registry keys vs `git ls-tree`); this seat re-derived it | land the report or record the seat dead in the round-32 lesson's seat ledger (C2's R5; paste-ready line in §6). **criterion:** Q19 ("a round records what its seats bought") states exactly this rule, but its own check is `test -e .ufo/waves/yield.tsv` → absent — the criterion was landed as prose in round 29 and never implemented |
| `reference-drift` — a correction sweep updated the entry and left the lesson table citing the same locator (routed D6) | `git show 87f0d32:corpus/lessons/round-31.md:57` still reads `precedence docstring (\`:35-38\`)` while the entry was corrected to `:39-40`; the round-30 lesson erratum points the Q6 retraction at entry `:78-81`, which at tip is `:72` and `:82-83` | round-31 verifier §5 D6 | appended correction notes in both lessons, never in-place edits (C2's R6; R6's check keeps `:35-38` present and requires `:39-40` within 300 chars of `verifier_mode.py` plus a `correction`/`superseded` label). **criterion:** Q10 — a second seat re-opening `verifier_mode.py` finds precedence at `:39-40`; Q10 existed and applies, it was not run on the lesson table |
| `reference-drift` — the round-30 lesson grouped S083/S086 as "peer-reviewed" (carried erratum debt, C2's R7) | `git show 6084cd3:corpus/lessons/round-30.md:66`: "S085 a self-report, S081/S082 preprints vs S083/S086 peer-reviewed); Q6 pass" | round-31 verifier §5 "Carried debt (lane-disclosed)" | appended erratum recording S086 as published **without** peer review (C2's R7). **criterion:** Q5 ("every source is labelled for what it is") — existed, applies, was not applied to this grouping |
| `misroot` — a test fixture was committed against the **fleet root**, deleting the whole tracked tree | fleet commit `35b91714` (author/committer `t <t@t>`, 2026-10-25 09:21:14 -03, message `t`) adds `corpus/README.md`, `corpus/knowledge/a b.md`, `"corpus/knowledge/caf\303\251.md"`; `git show --stat 35b91714` → `4606 files changed, 4 insertions(+), 823070 deletions(-)`; `git diff --diff-filter=D --name-only 35b91714^ 35b91714 \| wc -l` → `4603` (its parent `0619111d` held 4603 files) | `protocol-shokunin` repair commit `f47ad6ba` (09:29:03) "repair: restore fleet tree deleted by stray commit 35b91714"; this seat verified the numbers | repair landed (`f47ad6ba`: 4607 paths, fixtures dropped, no history rewritten). Structural fix: the fixture-writing selftest must run against a temp repo with isolated repository/index/worktree/object/config/template/hook selectors — Q16 already says this and the failure shows the instrument's isolation did not cover the fleet root. **criterion:** Q16, stated and unmet |
| `number-drift` — the repair commit's headline counts files-changed as paths-deleted | `f47ad6ba` body: "deleting 4,606 tracked paths"; the commit it describes gives `4606 files changed` = 4603 deletions + 3 additions (`git diff --diff-filter=D … \| wc -l` → `4603`; `git diff --name-status 35b91714^ 35b91714 \| grep '^A'` → 3 paths) | this seat (round-32 `R32DraftMistakes`) | state the unit: "4,606 files changed (4,603 deleted, 3 added)", or re-derive with `--diff-filter=D`. Not repaired here — fleet bytes are read-only to this lane, so it is routed. **criterion:** Q10, and round-30 §Mistakes 1's rule that "the count is re-derived in the lesson command's own unit" |
| `reference-drift` — a one-line divergent fork of a tracked instrument sat untracked at the fleet root, under a name its own docstring does not carry | `m-rev-vs-rev.py` (8796 B, sha256 `a2a3f790e83bd7d6552f7c35eacb8ab89f319b80aa7a39ab54a51eb734764e9a`); its docstring opens `"""souji-coverage-agreement.py — coverage-map agreement instrument (round 24 C2, round 25 C1)`; `diff` against the tracked `souji-shokunin/tools/souji-coverage-agreement.py` (sha256 `bb506469…`, tracked since `1efe406`) is 2 changed lines, one substantive: `base = entry_grounds(root, base_rev, knowledge_tree(root, base_rev))` → `base = grounds`; `grep -rl m-rev-vs-rev` over the fleet → 0 hits | this seat's misroot sweep (§3) | delete the fork (no reader) or land the change as a commit in the lane that owns the instrument; nothing in kengaku may cite it. **criterion:** R2 ("no round-owned path is left untracked") and Q7 ("no support rests on … an unlanded working copy") — both existed; neither has a sweep that reads the fleet root |
| `landing` — a lane's wave-2 falsify report never landed and now sits untracked in the **fleet** wave tree | `git status --porcelain` → `?? .ufo/waves/round-24/` → `.ufo/waves/round-24/w2/RevUnlandedResolution.md` (tabi lane, target tip `ad125e85`, baseline `573c99e4`); the report's own §0 F1 is "8 untracked paths, not 0" — the report is now one of them | this seat's misroot sweep (§3) | land it in the owning lane's wave tree or delete it; the fleet repo is read-only to this lane, so routed to tabi. **criterion:** R2 — existed, and the fleet-root wave tree is outside every lane's R2 check |
| `vacuous` — C3's model count is a page count, so the frozen figure cannot tell a catalog from a request | `plans/catalog_probe.py:29` `HF_URL = "https://huggingface.co/api/models?limit=50"`, `:54` `return len(data), [field for field in HF_FIELDS if field not in first]`, printed at `:112` as `hf_models={hf_n}`; the frozen control `.ufo/waves/round-32/claims/catalogs-before.txt:4` reads `probed=2026-10-25 hf=ok openrouter=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 entry=stale` — the HF figure equals the request's own `limit=50` | this seat, reading the counter the frozen predicate names | the claim is frozen, so the repair is an appended note in the entry/report, not a predicate change: state the figure as a page count (`limit=50`) and have the second receipt re-derive the unit; a true total needs pagination or a total-count header. **criterion:** Q10 (a second seat re-reads the number) and round-30 §Mistakes 1 (count re-derived in its own unit) — both existed; the frozen predicate was written after neither was applied |
| `scope` — the build wave ran as two concurrent seat sets for the same items | the dispatch roster for this seat carries both `L1Kengaku32.R32Frontier` and `L1Kengaku32.R32Frontier-3`, `L1Kengaku32.R32DraftScorecard` and `L1Kengaku32.R32DraftScorecard-3`, `L1Kengaku32.R32DraftErrata-3` beside this seat's unsuffixed batch; `.ufo/waves/round-32/build-assignments.json` held 34 `-3`-suffixed keys on my first read (e.g. `"L1Kengaku32.R32ReconPackage-3": "L1Kengaku32.R32ReconPackage-3"`) and 34 unsuffixed keys on a re-read, with mtime `09:44:36`; `build-run.log` (mtime `09:41:08`) holds `0` `-3` names; the L1's own status line reads "Killing duplicate agent batch -2" | the L1 (main agent), which killed the duplicate; this seat recorded the two reads | dispatch bookkeeping keyed by wave+item name (the registry already keys by name — `swarm-registry.json` `members` are unsuffixed — so the dispatch path bypassed it), and the killed batch's seats recorded as dead in the round-32 seat ledger so the seat count is honest. **criterion:** `none` — no QUALITY row bounds seat multiplicity; Q19 counts seat yield, not duplicate dispatch |

Notes on scope of the table:

- Rows 1–7 are the round-31 closure's routed items (D3, D1, D2, D4, D5, D6, and the carried
  peer-review erratum debt). They are **not** this round's mistakes; they are the debt C2 closes, and
  their class column is the mapping the task asks for.
- Rows 8–13 are mined this round. Rows 8–9 and 11 are fleet-level (repair author, untracked wave
  file) and are recorded here because the lane reports into that tree; they are not kengaku-authored
  and no kengaku seat may repair them.
- Row 12 is a hazard in this round's **frozen** claim C3, not in a landed artifact. It is recorded as
  a mistake of claim design; the predicate must not be rewritten after a seat has scored it.

---

## 2. Routed-defect mapping (class + criterion), compact

| item | class | criterion that should have caught it | why it did not |
|---|---|---|---|
| D1 phantom hash `a44b5a8` | `reference-drift` | `none` | Q10 covers source locators, not lane-commit hashes; the only check was the non-author's step-1 sweep, run after filing |
| D2 report ordering recurred | `landing` | `none` as a QUALITY row (round-30 §5 item 7 is its only statement) | never landed as an R-criterion; C2's R2 turns it into a counter check |
| D3 CLI receipt cannot run its own command | `landing` | Q20 (partial) | Q20 requires the receipt to exist and be committed; nothing requires it to re-run after a rewrite |
| D4 gate has no registry row | `reference-drift` | `SKILL.md` §Gate standard (Delivery) | the criterion exists in prose; no instrument reads the SKILL registry |
| D5 `R31FxEntryBar` unreported, ledger says "none" | `landing` | Q19 | Q19 was landed as prose in round 29; its own check (`test -e .ufo/waves/yield.tsv`) is absent |
| D6 locator drift in both lessons | `reference-drift` | Q10 | Q10 applies and was not run on the lesson tables |
| carried: round-30 `:66` S083/S086 "peer-reviewed" | `reference-drift` | Q5 | Q5 applies and was not applied to this grouping |

---

## 3. Misroot sweep (pasted; it did **not** find nothing)

Command, read-only, run from `/home/vgpnk/Projects/shokunin`:

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain; echo "EXIT=$?"; git status --porcelain | wc -l
 M .ufo/state/chousa.report-baseline
 M .ufo/state/kagi.report-baseline
 M .ufo/state/kaidoku.report-baseline
 M .ufo/state/kake.report-baseline
 M .ufo/state/kama.report-baseline
 M .ufo/state/kasegi.report-baseline
 M .ufo/state/kengaku.report-baseline
 M .ufo/state/kumitate.report-baseline
 M .ufo/state/mado.report-baseline
 M .ufo/state/mori.report-baseline
 M .ufo/state/souji.report-baseline
 M .ufo/state/tabi.report-baseline
 M .ufo/state/tameshi.report-baseline
 M .ufo/state/tsukuroi.report-baseline
 M .ufo/watchdog.log
 M scripts/hyaku/hyaku.env
 M scripts/hyaku/lane-addendum.md
?? .omp/mcp.json
?? .scratch/goal-20261025-hyaku-12h.md
?? .ufo/state/kotoba.report-baseline
?? .ufo/state/kotodama.report-baseline
?? .ufo/state/revenger.report-baseline
?? .ufo/waves/round-24/
?? m-rev-vs-rev.py
EXIT=0
--- count:
24
```

So the sweep found **24 entries** (17 modified, 7 untracked). Disposition of each, so the count is not
left as a bare number:

| entry | disposition |
|---|---|
| 14 × ` M .ufo/state/*.report-baseline` (incl. `kengaku`) | harness-owned run state; not round-owned, not a lane's write scope |
| 3 × `?? .ufo/state/{kotoba,kotodama,revenger}.report-baseline` | same, newly created baselines |
| ` M .ufo/watchdog.log` | mutable harness log (the round-31 spot-check itself labels it "mutable") |
| ` M scripts/hyaku/hyaku.env`, ` M scripts/hyaku/lane-addendum.md` | hyaku run-6 orchestrator config |
| `?? .omp/mcp.json` | operator tooling config (mtime 2026-10-24 18:07) |
| `?? .scratch/goal-20261025-hyaku-12h.md` | orchestrator-owned run state by its own header ("Not a misroot: lanes and seats never move, copy-then-delete, or edit this file") |
| `?? m-rev-vs-rev.py` | **misroot candidate** → row 10 |
| `?? .ufo/waves/round-24/` | **misroot candidate** → row 11 (`.ufo/waves/round-24/w2/RevUnlandedResolution.md`) |

Zero of the 24 are kengaku round-32 paths. The lane's own tree at the same moment:

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status --porcelain
?? .ufo/waves/round-32/assimilation/
?? .ufo/waves/round-32/build-assignments.json
?? .ufo/waves/round-32/build-run.log
?? .ufo/waves/round-32/build-spec.json
?? .ufo/waves/round-32/build/
count: 5
```

All five are the wave's own run artifacts under `.ufo/waves/round-32/`; the four claim controls and
`gate-receipt.txt` are already tracked (`git ls-files .ufo/waves/round-32` → 5). R2's "no round-owned
path is left untracked" is therefore **open** for this round until those five are committed with the
landing — named here as a live risk, not a mistake yet.

---

## 4. Receipts (verbatim command → output)

**D1**

```
$ sed -n '226p' .ufo/reports/round-31/kengaku.md
fixed at lane tip `a44b5a8`-class commits (`verifier_mode.py:22-23` → **`:18-21`** for the "Returns the
$ git cat-file -t a44b5a8
fatal: Not a valid object name a44b5a8
$ git -C kengaku-shokunin log --oneline -1 ae95fe0
ae95fe0 round-31: entry locator corrections (verifier_mode.py:18-21, :39-40) and final falsify evidence
```

**D2**

```
$ grep -c "ae95fe0" .ufo/reports/round-31/kengaku.md   → 0
$ grep -c "87f0d32" .ufo/reports/round-31/kengaku.md   → 0
$ grep -n "9591131e" .ufo/reports/round-31/kengaku.md | head -3
199:`9591131e893696fd051246cb7f8fcef74172b672`** (local = remote, `ahead=0`, clean tree), through
200:`f6422263` → `634ded8` → `a6ff2f0e` → `3e13607e` → `9591131e`.
212:   `corpus/README.md` (`9591131e`).
```

**D3** (lane, at `87f0d32`; unchanged at `6084cd3`)

```
$ git show 87f0d32:corpus/evidence/round31/gate-cli-exits.txt | head -12
# C3 CLI receipt (round 31, 2026-10-25). Self-contained: fixtures are committed at .ufo/waves/round-31/c3-fixtures/
# run: cd .ufo/waves/round-31/c3-fixtures && for m in map-ok map-bad map-unmapped; do python3 ../../../plans/sources_adopt.py --quote-file rows.txt --artifact cap.txt --url-map $m.json; echo exit=$?; done
#      plus: no-map run, and --url-map with --registry/--package (the exit-2 guard)
python3: can't open file '/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-31/c3-fixtures/../../../plans/sources_adopt.py': [Errno 2] No such file or directory
url-map map-ok -> exit=2
…
$ git show 87f0d32:corpus/evidence/round31/gate-cli-exits.txt | grep -c "can't open file"
5
$ git show 6084cd3:corpus/evidence/round31/gate-cli-exits.txt | grep -c "can't open file"
5
```

**D4**

```
$ git show 87f0d32:SKILL.md | grep -c sources_adopt
0
$ git show 6084cd3:SKILL.md | grep -c sources_adopt
0
```

**D5**

```
members: 36
reports: 35
registry-not-reported: ['R31FxEntryBar']
```

**D6**

```
$ git show 87f0d32:corpus/lessons/round-31.md | grep -n "35-38"
57:| S092 | …/src/harbor/models/task/verifier_mode.py | "or VerifierEnvironmentMode.SHARED" (2, `:31`); precedence docstring (`:35-38`) | 5 142 B, sha256 `e5893be9…8a6f2d` |
```

**Carried debt (round-30 `:66`)**

```
$ git show 6084cd3:corpus/lessons/round-30.md | sed -n '66p'
  S085 a self-report, S081/S082 preprints vs S083/S086 peer-reviewed); Q6 pass (§Extends names both
```

**Fleet stray commit (row 8) and its repair (rows 8–9)**

```
$ git show --stat --format='%H%nauthor=%an <%ae>%ncommitter=%cn <%ce>%ndate=%ad%n%s%n%b' 35b91714 | head -25
35b91714722fd2314c6b22839c446a116d1a5ffb
author=t <t@t>
committer=t <t@t>
date=Sun Oct 25 09:21:14 2026 -0300
t


 .devin/skills/flashseat/SKILL.md                   |     7 -
 …
$ git diff --name-status 35b91714^ 35b91714 | grep '^A'
A	corpus/README.md
A	corpus/knowledge/a b.md
A	"corpus/knowledge/caf\303\251.md"
$ git show --stat 35b91714 | tail -2
 templates/round-prompt.md                          |   140 -
 4606 files changed, 4 insertions(+), 823070 deletions(-)
$ git diff --diff-filter=D --name-only 35b91714^ 35b91714 | wc -l
4603
$ git log --format='%h %s' -1 35b91714^
0619111d round-53: kake report
$ git show --stat --format='…%s%n%b' f47ad6ba | head -8
f47ad6ba8d306f8125597401cb2ce45c1297a593
author=protocol-shokunin <protocol@shokunin.local>
date=Sun Oct 25 09:29:03 2026 -0300
repair: restore fleet tree deleted by stray commit 35b91714 (author t <t@t>, 09:21:14 -03)
A test fixture (corpus/README.md, 'a b.md', 'cafe.md') was committed against the fleet
root, deleting 4,606 tracked paths. This commit restores the tree of 35b91714^ (0619111d) …
$ git ls-tree -r --name-only f47ad6ba | wc -l
4607
$ git ls-tree -r --name-only f47ad6ba | grep -E '^(corpus/README\.md|a b\.md|cafe\.md)$' || echo "none (fixtures dropped)"
none (fixtures dropped)
```

**Forked instrument (row 10)**

```
$ sha256sum m-rev-vs-rev.py souji-shokunin/tools/souji-coverage-agreement.py
a2a3f790e83bd7d6552f7c35eacb8ab89f319b80aa7a39ab54a51eb734764e9a  m-rev-vs-rev.py
bb506469be860f994f74f4c7d6eb1c949a4931b676cdb60f9f79de041d12f27f  souji-shokunin/tools/souji-coverage-agreement.py
$ diff souji-shokunin/tools/souji-coverage-agreement.py m-rev-vs-rev.py
118c118
<     base = entry_grounds(root, base_rev, knowledge_tree(root, base_rev))
---
>     base = grounds
$ grep -rl "m-rev-vs-rev" --include='*.md' --include='*.json' --include='*.sh' --include='*.py' . | grep -v '^./.git'
(no output)
$ git -C souji-shokunin log --oneline -1 -- tools/souji-coverage-agreement.py
1efe406 round-24: instruments (size census, coverage agreement, three fixtures, C1 stub control) + preregistration amendment 1 + wave-1 spec/dispatch
```

**Untracked wave report (row 11)**

```
$ find .ufo/waves/round-24 -maxdepth 3
.ufo/waves/round-24
.ufo/waves/round-24/w2
.ufo/waves/round-24/w2/RevUnlandedResolution.md
$ sed -n '1,20p' .ufo/waves/round-24/w2/RevUnlandedResolution.md
# RevUnlandedResolution — routed defect 2 (89 unlanded paths): closure composition
Seat `L1Tabi24.RevUnlandedResolution`, round 24 wave 2, falsification pass.
Target: lane tip `ad125e85c235e1c4ec6a08e398bd64da01f68a08` …
- **F1 (HIGH) — the closure condition does not hold: 8 untracked paths, not 0.** …
```

**C3 page-capped count (row 12)**

```
$ grep -nE "limit|hf_models" plans/catalog_probe.py | head -5
29:HF_URL = "https://huggingface.co/api/models?limit=50"
41:    "per_request_limits", "hugging_face_id", "reasoning",
54:        raise ValueError("HF api/models did not return a nonempty list")
112:        f" hf_models={hf_n} or_models={or_n}"
$ sed -n '51,56p' plans/catalog_probe.py
def parse_hf(text: str) -> tuple[int, list[str]]:
    data = json.loads(text)
    if not isinstance(data, list) or not data:
        raise ValueError("HF api/models did not return a nonempty list")
    first = data[0]
$ cat .ufo/waves/round-32/claims/catalogs-before.txt
# C3 freeze control (round 32, 2026-10-25) — base entry stale
# command: python3 plans/catalog_probe.py --diff --lane .
probed=2026-10-25 hf=ok openrouter=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 entry=stale
HF missing fields: author, sha, lastModified, gated
exit=1
```

**Duplicate batch (row 13)**

```
$ ls -la --time-style=full-iso .ufo/waves/round-32/build-assignments.json .ufo/waves/round-32/build-run.log
-rw-r--r-- 1 vgpnk vgpnk  1578 2026-10-25 09:44:36.993837471 -0300 .ufo/waves/round-32/build-assignments.json
-rw-r--r-- 1 vgpnk vgpnk 55207 2026-10-25 09:41:08.450395767 -0300 .ufo/waves/round-32/build-run.log
$ grep -o 'R32[A-Za-z0-9]*-3' .ufo/waves/round-32/build-run.log | sort -u | wc -l
0
$ python3 -c '… json.load(build-assignments.json) …'   # first read, before 09:44:36
{"L1Kengaku32.R32ReconPackage-3": "L1Kengaku32.R32ReconPackage-3", "L1Kengaku32.R32SrcS094a-3": …, "L1Kengaku32.R32DraftMistakes-3": …}
$ python3 -c '… same file, re-read after 09:44:36 …'
assignments: 34 | with -3: 0
sample: ['R32ReconPackage', 'R32SrcS094a', 'R32SrcS094b']
```

---

## 5. Findings, hazards, out-of-scope

- **The sweep was not clean.** The task allowed a "found none" line; the fleet repo has 24 entries and
  two of them are genuine misroot candidates (rows 10, 11). I paste the sweep instead of claiming
  cleanliness. 21 of the 24 are harness/orchestrator-owned and outside every lane's write scope.
- **Two live seat sets exist for this wave right now** (row 13). Consequence for the lesson: the seat
  ledger must not count both sets, and any report path written by a duplicate scribe (this file's
  sibling `…-3` seat, if one exists) must be reconciled before the wave's reports are treated as one
  set. I wrote only my own path.
- **All three C2 repair targets I can read are still open at `6084cd3`** (R3: 5 `can't open file`
  lines; R4: `grep -c sources_adopt SKILL.md` → 0; R7: round-30 `:66` unchanged). That is the
  expected mid-wave state, not a defect of this draft; the closures land with the C2 seats.
- **`corpus/lessons/round-32.md` does not exist yet** — neither at tip `6084cd3` nor in the working
  tree. These rows are drafts for the `R32DraftLesson` seat; I did not create the lesson (production
  edit, outside my write scope).
- **Row 12 must not be repaired by changing the predicate.** C1/C3 are frozen at `0d32691d`; the fix
  belongs in the entry's provenance note and the report, per the claims file's own rule ("a predicate
  changed after a seat has scored is not this claim's predicate").
- **Out of scope, not done:** no repair of any defect (rows 1–13 are routed, not fixed); no edit to
  the round-31 report, the lessons, `SKILL.md`, the fleet tree, or the two misroot paths; no
  commit/push; no counter run beyond the read-only re-derivations in §4 (`plans/round32_defects.py`
  was read, not executed — the preflight belongs to its own seat).

---

## 6. Paste-ready seat-ledger line for R5

`plans/round32_defects.py:132-139` requires `R31FxEntryBar` and `dead` within 160 characters **on one
line** of `corpus/lessons/round-32.md`. Suggested row for that lesson's seat ledger (single line):

```
| falsify | 36 dispatched | `R31FxEntryBar` — dead: no report committed at round-31 tip `87f0d32` (35 of 36 landed); recorded per routed defect D5 | 0 |
```

VERDICT: mistakes-mined
