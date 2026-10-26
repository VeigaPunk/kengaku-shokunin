# R39PkgProse — C2 lane prose drafts (kengaku round 39, wave 1)

Seat: scribe. Assignment: draft paste-ready lane prose for C2 — PROVINCE paragraph, README §Frontier sub-bullet,
a SKILL.md decision-table section, and gate-registry rows for the round-39 tools. Observations only.

**Report path:** `.ufo/waves/round-39/build/R39PkgProse.md`
**Draft dir:** `.ufo/waves/round-39/build/R39PkgProse/`
**Lane writes:** the four draft files below plus this report. Nothing in `corpus/`, `plans/`, `SKILL.md`,
`PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `SHONEN.md`, the lane's git index or jj state was touched.
**Scratch:** none created — drafting needs no clone, fixture or work tree. `/fast/scratch/hyaku/kengaku-r39/`
exists (sibling seats), but no `R39PkgProse` subdir was made there and nothing was written to `/tmp`
(`test -e /fast/scratch/hyaku/kengaku-r39/R39PkgProse` → absent).
**Tools installed/upgraded:** none (no `pacman`, no `uv tool`, no binary download; nothing was needed).

---

## 1. Behavior — what the four drafts say, and where each lands

| # | Draft file | Paste target | What it carries | Row count |
|---|---|---|---|---|
| a | `R39PkgProse/province-round39.md` | `PROVINCE.md`, new `## Round39 partial frontier admission (2026-10-26)` after the round-38 section | Core admission (probe + entry + S117/S118 + receipt line), the graded-state class (git object store + refs + one flag file), sandbox shape, the headline observations, and the admission limits the assignment names: grader probe only, image never pulled, repository-history state as a new graded-state class; narrows only "remaining TB2 tasks" for this task | one section paragraph + one reported-out line |
| b | `R39PkgProse/readme-frontier-round39.md` | `corpus/README.md` §Frontier, bullet *Agentic benchmark task-spec audits*, as a child sub-bullet after the round-38 one | `*Partly discharged round 39 …*` sub-bullet carrying `5 of 89 read` (was 4), the class sentence, the observed pass/fail headline, and the unchanged open clauses | one sub-bullet (11 wrapped lines) + a count audit + an out-of-scope note |
| c | `R39PkgProse/skill-repo-history-tb2-grader.md` | `SKILL.md`, new `## Repository-history TB2 grader — round 39` after the round-38 section | Run-first paragraph (probe CLI, exit map, receipt summary, class difference), decision table (what the grader reads → what passes → what a reviewer should check instead), green/not-green paragraph, the derived requirement-map labels, limits, closing property line | **12 decision-table rows**, every row citing ≥1 receipt case id |
| d | `R39PkgProse/registry-rows-round39.md` | `SKILL.md` §Gate/probe registry — three rows after `tip-receipts`, plus a `Round-39 registry addendum:` paragraph | `git-leak-probe` (probe), `round39-c1-mutants` (gate), `round39-c2` (gate), in the table's 8-column shape, with controls and pinned values | **3 registry rows** + addendum + 4 paste-notes |

Every path above is relative to `/home/vgpnk/Projects/shokunin/kengaku-shokunin/`.

**Decision-table content (the 12 rows, by grader read):** flag literal equality (`test_outputs.py:11-17`);
`.strip()` tolerance (`:15`); whole-line equality (`:16`); directory → `IsADirectoryError` (`:14-15`); literal
in the wrong location (`:14`); `log --all --grep` over messages (`:19-38`) — passes for non-commit holders and
reds for `branch-keeps-leak`/`commit-message-secret`/`notes-secret` (two rows); `log --all -p -S` (`:39-49`);
`fsck --lost-found` + `cat-file -p` over `dangling` (`:66-92`); `log --oneline --all` substring (`:51-64`);
work-tree checksum with dot-path exclusion (`:95-113`); do-nothing baselines + the oracle. Each row's `cite`
cell names receipt case ids with their line numbers.

---

## 2. Gates — what the L1 must run, and what would turn this draft red

1. `python3 plans/round39_c2_verify.py --lane .` from the lane root. This draft is **not** green-by-itself: V3
   (anchor cells on S117/S118), V4 (receipt case ids + entry names every `match=NO` case — none here), V6
   (census) and V7 (the entry's `## Requirement map`) read bytes other seats land. V7 is the check that
   adjudicates the labels I state below.
2. Red-on-this-draft: any label in the entry's `## Requirement map` disagreeing with §3's table, or any
   `instruction.md:<L>` mismatching the frozen dry table's TAG lines
   (`corpus/evidence/round39/git-leak-dry-cases-freeze.txt:1-4` → `:3`, `:4`, `:5`, `:5`).
3. Red-on-the-count: a §Frontier cell other than `5 of 89` — the four prior sub-bullets say 1,2,3,4 of 89 and
   the round-38 one says `4 of 89 read`; this task is the fifth (denominator `89` restated from
   `plans/round-39-claims.md` §C2 and the round-37 PROVINCE paragraph; not re-derived here).
4. No gate was run by this seat (wave-1 rule: verification is the main agent's). Nothing in this draft asserts a
   measured counter state of its own.

---

## 3. Findings — the numbers behind the prose, with their commands

All commands below run from `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

**F1 — receipt shape.** `cat -n corpus/evidence/round39/git-leak-probe.txt` → 30 lines: 1 header, 3 capture
lines, 25 `CASE` lines (lines 5–29), summary at line 30:
`cases=25 observed_pass=13 observed_fail=12 mismatches=0`. `match=yes` on all 25 (no `match=NO` case, so the
entry owes no mismatch disclosure under V4).

**F2 — derived requirement-map labels (the entry must agree).** Independent derivation from the receipt, using
V7's rule (all violating cases fail → `enforced`; all pass → `unenforced`; mixed → `partly`):

```
awk '/^CASE /{id=$2; obs=""; viol=""; for(i=1;i<=NF;i++){if($i ~ /^observed=/){split($i,a,"=");obs=a[2]} if($i ~ /^violates=/){split($i,b,"=");viol=b[2]}} if(viol!=""){n=split(viol,t,","); for(j=1;j<=n;j++){printf "%s %s %s\n", t[j], obs, id}}}' corpus/evidence/round39/git-leak-probe.txt | sort | awk '{c[$1]++; if($2=="fail") f[$1]++; else p[$1]++} END{for(t in c){lab = (f[t]==c[t])?"enforced":((p[t]==c[t])?"unenforced":"partly"); printf "%s cases=%d fail=%d pass=%d -> %s\n", t, c[t], f[t]+0, p[t]+0, lab}}' | sort
```

Output:

```
files-untouched cases=2 fail=2 pass=0 -> enforced
messages-untouched cases=3 fail=1 pass=2 -> partly
recover-secret cases=5 fail=5 pass=0 -> enforced
secret-gone cases=16 fail=8 pass=8 -> partly
```

Label sources: `recover-secret` — `empty-app`, `untouched`, `flag-extra-text`, `flag-is-directory`,
`flag-in-repo-only` (all observed fail). `files-untouched` — `empty-app`, `readme-edited`. `messages-untouched`
— `empty-app` (fail), `message-rewritten`, `history-rebuilt` (pass). `secret-gone` — 16 cases, 8/8 split.
**Caveat carried into the SKILL draft:** one of the two `files-untouched` witnesses is the empty-`/app`
baseline (`receipt:5`), so `enforced` is a property of the frozen case set, not of the clause.

**F3 — dry-table tag lines.** `grep -n '^TAG' corpus/evidence/round39/git-leak-dry-cases-freeze.txt` →
`recover-secret instruction.md:3`, `secret-gone instruction.md:4`, `files-untouched instruction.md:5`,
`messages-untouched instruction.md:5`. `instruction.md` is 9 lines; line 3 is "recover the secret and write it to
a /app/secret.txt file", line 4 "clean up the secret … cannot be found anywhere", line 5 "irrelevant files and
commit messages remain untouched" (both tags share it).

**F4 — grader assertion line map.** `grep -n 'def test_\|exists()\|-S\|oneline\|fsck\|find /app' …` on
`corpus/evidence/round39/tb2-git-leak-recovery/test_outputs.py` (113 lines): five test functions at `:11`, `:19`,
`:51`, `:66`, `:95`; `exists()` `:14`, `strip()` `:15`, equality `:16`; `log --all --grep` `:25-38`, `-p -S`
`:41`; oneline substring `:54,61`; `fsck --lost-found` `:69`, dangling loop `:77`, `cat-file -p` `:84`;
checksum `find … -not -path '*/\.*'` `:101-102`, expected digest `:110`, `expected in output` `:111`.

**F5 — the setup state explains three passing rows.** `cat -n challenge-setup.sh` → 22 lines; the init message
`chore: init e665d1a2-…` is committed twice (`:12` and `:22`), the secret commit is `git reset --hard HEAD~1`'d
(`:18`). That is why `message-rewritten` (receipt:24) and `history-rebuilt` (receipt:25) still satisfy the
oneline substring, and why the untouched state is `FPPPP` (receipt:6).

**F6 — the oracle is executed, unlike round 38.** `plans/git_leak_probe.py` runs each case's recipe; the
`oracle-solve-sh` case runs the captured `solve.sh` and observed `PPPPP` (receipt:7). `solve.sh` writes the
literal only inside its dangling-commit branch (`solve.sh:17-24`), so "the oracle found a dangling commit" is
derived from the receipt + that code, not printed by the probe. My drafts say so explicitly and do **not** copy
the round-38 wording "the oracle is not executed".

**F7 — registry controls.** `grep -n 'BATTERY\|^exit=' .ufo/waves/round-39/claims/control-c1-*.txt` →
`control-c1-nothing.txt:88 BATTERY fixtures=86 … :98 exit=1`; `control-c1-gate-edited.txt:88` same battery line,
`invalid=7` in the tail; `control-c1-hostile-inproc.txt:90 BATTERY fixtures=88`, `killed=3 survived=4`,
`exit=1`. `control-c2-nothing.txt` → `checks=7 defects=4` (V2, V3, V4, V7), `PREDICATE C2 fail`, `exit=1`, plus
eight embedded `gate: P#` defects (P2, P3, P4, P6, P7, P8, P9, P10).
Probe exit map read from source: `plans/git_leak_probe.py:226-301` — `return 2` on capture/bwrap/git/malformed-
case setup, stage arm `return 0 if bad == 0 else 1`, graded run `return 0` with mismatches only on the summary
line; the per-case child's `sys.exit(3)` (`:168,170`) surfaces as the parent's exit 2.

**F8 — C1/C2 counter interfaces (for the registry rows).** `plans/round39_c1_verify.py:256-395` — `PINS` printed
before anything else, dev selectors set `dev` and print `PREDICATE C1 n/a (non-default battery or mutant
subset)` (`:383`), predicate line at `:388`, `return 0 if good else 1`; setup refusals are the `return 2` sites
at `:278,290,300,305` (forbidden argv from an in-process or an out-of-process fixture, a module import/build
failure, duplicate fixture id). `plans/round39_c2_verify.py:258-282` —
`--lane`, `--work`; a check that raises prints `error <Class>: …` and counts as a defect; `return 0 if defects
== 0 else 1`.

**F9 — adjacency preserved.** The PROVINCE draft cites the round-38 prior-art block rather than re-making the
sandbox claim (runner → kumitate, method → tameshi) and routes capture/citation (chousa), prompt wording
(kotoba), deployment configuration and runtime task validity (refused). No sibling lane's instrument is claimed;
no git-internals ownership is asserted — the drafts grade "the grader's assertions", never git's storage
semantics.

---

## 4. Touched surfaces (all inside the wave-1 build dir)

- `.ufo/waves/round-39/build/R39PkgProse.md` (this report)
- `.ufo/waves/round-39/build/R39PkgProse/province-round39.md`
- `.ufo/waves/round-39/build/R39PkgProse/readme-frontier-round39.md`
- `.ufo/waves/round-39/build/R39PkgProse/skill-repo-history-tb2-grader.md`
- `.ufo/waves/round-39/build/R39PkgProse/registry-rows-round39.md`

Read-only reads this seat performed: `plans/round-39-claims.md`, `PROVINCE.md`, `corpus/README.md`,
`SKILL.md` (registry + round-37/38 sections), `plans/git_leak_probe.py`, `plans/round39_c1_verify.py`,
`plans/round39_c2_verify.py`, `corpus/evidence/round39/git-leak-probe.txt`,
`corpus/evidence/round39/git-leak-dry-cases-freeze.txt`, the seven files in
`corpus/evidence/round39/tb2-git-leak-recovery/`, `.ufo/waves/round-39/claims/`.

---

## 5. Out of scope for this seat (and who owes it)

- `corpus/knowledge/tb2-git-leak-recovery-grader.md` itself (entry, `## Requirement map`, `match=NO` disclosure
  line) — the entry seat. At the time of drafting the file does **not** exist (`ls corpus/knowledge | grep
  git-leak` → empty), so the C2 counter's V4/V7 are red until it lands.
- `corpus/SOURCES.md` rows S117/S118 with their 11-cell shape and one `sha256 <64 hex>` anchor token (V3).
- `corpus/README.md` §What's here index row and §Coverage map bullet for the new entry (V6 census / index
  parity; `control-c2-nothing.txt`'s embedded gate reports `P8 index_rows=45 … bad=2`).
- `SCORECARD.md`, `LOG.md`, `SHONEN.md`, `PROVINCE.md` itself, `SKILL.md` itself — L1 integrates from these
  drafts.
- Any C1 work (`plans/battery39/`) and any counter run.
- The claims' own frozen text — I copied its wording where a claim is stated (order-of-operations record,
  `stagecheck cases=25 failed=0`), and marked the two places where I state something the probe does not print
  (the oracle's mechanism) as derived.

---

## 6. Limits of this report

- I ran no lane gate, counter or probe: every counter line quoted here is copied from the frozen claims file or
  from a committed control receipt, and says so.
- The `89` denominator is not re-derived here (round-35 census restatement); the draft says that explicitly.
- The requirement labels in §3 are my independent awk derivation of V7's rule; they are a prediction the counter
  will adjudicate, not a pass.
- Wording choices that a reviewer may want to change before pasting: the registry row names
  (`round39-c1-mutants`, `round39-c2`) follow the table's round-37/38 convention rather than the claims file's
  "C1 counter"/"C2 counter"; and the PROVINCE paragraph's "reflog/object store" phrase follows the claims file
  verbatim rather than the probe's mechanism wording.

Drafted rows: 12 decision-table rows + 3 registry rows = 15.

VERDICT: c2-prose-drafted-15-rows
