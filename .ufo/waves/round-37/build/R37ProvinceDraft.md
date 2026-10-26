# R37ProvinceDraft — PROVINCE.md round-37 paragraph + round-36 wording fixes (draft only)

Seat: `R37ProvinceDraft` (scribe, leaf). Lane `kengaku-shokunin`; report dir
`.ufo/waves/round-37/build/`. No lane file edited, no counter run, no git/jj command issued. Scratch not
needed (all work was path-scoped reads); nothing written outside this report and
`.ufo/waves/round-37/build/R37ProvinceDraft/`.

**Report:** `.ufo/waves/round-37/build/R37ProvinceDraft.md`
**Drop-in artifact:** `.ufo/waves/round-37/build/R37ProvinceDraft/province-round37-dropin.md`

**Answer in one line:** the round-37 paragraph is drafted at 139 body words for EOF insertion after
`PROVINCE.md:257`; four fixes are drafted as exact old→new pairs (F3, F4, F5 against the admitted
round-36 entry; F6 against `PROVINCE.md:244-255`), and two are declined with reasons (F8, F10 — both
target closed or already-resolved records), with two stale adjacency citations found in the landed
round-36 paragraph.

---

## 1. What was drafted (behavior)

| Fix | Target | Disposition |
|---|---|---|
| round-37 paragraph | `PROVINCE.md` EOF (after `:257`) | drafted, 139 words, artifact above |
| F3 oracle framing | `corpus/knowledge/tb2-regex-log-grader.md:148`, insert after `:152` | drafted (append/heading pair); does **not** land in PROVINCE.md |
| F4 report, don't adjudicate | `corpus/knowledge/tb2-regex-log-grader.md:178-179` | drafted; does **not** land in PROVINCE.md |
| F5 negative-space additions | `corpus/knowledge/tb2-regex-log-grader.md:217-218` | drafted; does **not** land in PROVINCE.md |
| F6 round-36 paragraph | `PROVINCE.md:244-255` | drafted two ways (recommended: 67-word appended correction) |
| F8 axis naming | `plans/round-36-claims.md:63`, `SCORECARD.md:1222` | **declined** — frozen claims of a closed round; SCORECARD already holds the score |
| F10 capability definition | `SCORECARD.md:562` | **declined** — a separate capability row already exists at `SCORECARD.md:565` |

Nothing frozen from `plans/round-37-claims.md` is touched: `plans/pkg_gate.py`, the counters, the probe,
the mutant list and the claims file are unmodified.

---

## 2. Drop-in: round-37 paragraph

Placement: append at EOF, **after `PROVINCE.md:257`** (the round-36 `**Reported out:**` line). Appending
keeps the file's own correction convention (`:119`, `:175` append dated notes rather than rewrite an
admitted paragraph) and keeps the round-36 paragraph adjacent to its own reported-out note.

```markdown
## Round37 partial frontier admission (2026-10-26)

**Core addition:** offline execution of a third pinned Terminal-Bench 2.0 grader of a class the lane had
not run — `configure-git-webserver/tests/test_outputs.py` and `tests/verify.sh` at terminal-bench-2
`2fd12b88`, a stdout-substring verdict over a helper script probing a live HTTP service — over 22 frozen
synthetic service states, each in a private-network bubblewrap sandbox, via
`corpus/knowledge/tb2-git-webserver-grader.md` (S111–S113), `plans/git_webserver_probe.py` and receipt
`corpus/evidence/round37/git-webserver-probe.txt` (`cases=22 observed_pass=9 observed_fail=13
mismatches=0`). It records what that verdict depends on for lane-built states only: it never runs
Terminal-Bench, the task image, the oracle path or a real git push; validate or certify a task; own
nginx, git or ssh administration; or measure agent performance. Adjacent: fixture craft (tameshi),
research method (chousa), prompt craft (kotoba) and seat arrangement (kumitate) stay theirs. The round36
paragraph above stays as written; this one narrows only its "any other TB2 task" clause for this task.
```

Word count: 139 body words, the same bulk as the landed round-36 paragraph (139 words over
`PROVINCE.md:244-255`); the ceiling named in the task is 140. Terms used are the frozen claims' own:
"stdout substring", "helper shell script", "private network namespace", "does not show that the intended
path passes" (`plans/round-37-claims.md:62-67`, `:96-97`).

Why each clause is worded this way:
- **"a class the lane had not run"** — a property of the lane's executed probes, not a construct claim:
  `plans/round-37-claims.md:64` says "the first service/state grader the lane reads". The paragraph does
  not say "new construct" (F8's vector, §5).
- **"the oracle path"** means `solution/solve.sh`, never executed: the claims' own limit is "it never
  runs the oracle or a real git push, so it does not show that the intended path passes"
  (`plans/round-37-claims.md:96-97`). It is not a solvability claim.
- **"own nginx, git or ssh administration"** is a refusal, not a capability gap: no fleet lane claims
  that ground (§4).

---

## 3. Fix F6 — round-36 paragraph (PROVINCE.md:244-255)

### 3.1 State of the fix: unabsorbed, three clauses

The landed paragraph is the 139-word draft (`awk 'NR>=244 && NR<=255' PROVINCE.md | wc -w` → `139`). Three
of F6's four deltas are still absent (`R36CritScope.md` §3 F6):

| F6 delta | Landed text | Status |
|---|---|---|
| "(lane-authored patterns, not agent outputs)" | `:245-248` "over 24 frozen `/app/regex.txt` candidates" and "the graded artefact is an agent-authored regex file" — the candidate/probe split is unstated | unabsorbed |
| "establish regex or log-parsing correctness" | `:251` "establish which pattern the instruction demands" only | unabsorbed |
| contamination as a refusal | absent from `:250-252` | unabsorbed |
| arithmetic (`87` remaining) | `:255` "only its \"other 88 TB2 tasks\" clause" | unabsorbed, and now stale: 89 TB2 task dirs (`corpus/knowledge/benchmark-verifier-execution-model.md:131`) minus three admitted graders (protein-assembly, regex-log, configure-git-webserver) = **86** |

### 3.2 Recommended landing: appended correction (67 words)

Anchor: insert immediately after `PROVINCE.md:255` (the line ending `...clause for this one task.`).

**Old:** no text removed.

**New (insert after `:255`):**

```markdown
*Round-37 correction R37-P1 (appended 2026-10-26; supersedes three clauses of the round36 paragraph at
`:244-255`): the 24 candidates were lane-authored patterns, not agent outputs; the paragraph establishes
no regex or log-parsing correctness and no contamination measurement (the in-test log and its literal
dates are the grader's own fixture); and with three TB2 graders now read, `:255`'s "other 88 TB2 tasks"
reads `86 of TB2's 89 task graders` (`corpus/knowledge/benchmark-verifier-execution-model.md:93`).*
```

Why append rather than rewrite: `PROVINCE.md:119` and `:175` both correct earlier paragraphs by appending
a dated note that names what it supersedes; `:244-255` belongs to a closed round (round 36 is closed and
wave 2 was never dispatched, `SCORECARD.md:1244`). A rewrite would erase the admitted record F6 reviewed.

### 3.3 Optional in-place variant (only if the L1 rules the paragraph open)

Use `R36CritScope/province-rewrite.txt` verbatim (134 words), with one substitution: `87 TB2` → `86 TB2`
(the round-36 rewrite assumed two admitted graders). Replace `PROVINCE.md:244-255` with that text. I did
not re-cut its wording; it is the critic's drop-in.

---

## 4. Fixes F3, F4, F5 — entry-scope pairs (do not land in PROVINCE.md)

All three target the admitted round-36 entry `corpus/knowledge/tb2-regex-log-grader.md`. They are drafted
here because the task routed them to this seat, but none is a PROVINCE.md edit: the PROVINCE-level
refusals they add are already carried by F6's correction (§3.2). If the L1 lands them, they are appended
amendments to an admitted artefact (the entry already uses that form at `:43`, "amended **before any seat
scored**"), so each pair below is written as an insertion or a self-contained replaced sentence.

### F3 — oracle framing (`:148` heading, insert after `:152`)

**Old (`:148`):**
```
## The oracle (`solution/solve.sh`, captured; tier C, own reading)
```
**New (`:148`):**
```
## The oracle (`solution/solve.sh`, captured; tier C — pattern text extracted, script not run)
```
**Insert after `:152` (`row**:`):**
```
One offline application of the captured function to the pattern text this lane extracted: it is not the
maintainers' oracle-passes check, not a solvability or instruction-consistency verdict, and no submission
was involved.
```
Grounding: the section body already says "own reading, not a graded result and not a registry row"
(`:151-152`) and that the oracle entered the same `mod.Path` path as every case (`:162`). F3 was "partly
absorbed" (heading says `tier C`) — this closes the remaining two refusals.

### F4 — report, don't adjudicate (`:178-179`)

**Old (`:178-179`):**
```
but it **admits a two-digit leading-zero octet** (`01.`) — the instruction's line-4 rule is not
enforced by the oracle either, and the fixture cannot see the difference.
```
**New (`:178-181`):**
```
but it **admits a two-digit leading-zero octet** (`01.`), while `instruction.md:4` asks for none; the
pattern is not a graded artefact here, and which of the two the maintainers intend is theirs to resolve.
This entry records the difference only (routed out, not absorbed).
```
Grounding: `instruction.md:4` is quoted at `:261` ("IPv4 addresses use normal decimal notation without
leading zeros in each octet."), and the same leading-zero finding is already recorded as a post-hoc
observation at `:194-195`.

### F5 — negative space (`:217-218`)

**Old (`:217-218`):**
```
anything about the other TB2 tasks. The probe runs the captured function under the host Python, not
inside `alexgshaw/regex-log:20251031`.
```
**New (`:217-223`):**
```
anything about the other TB2 tasks. The probe runs the captured function under the host Python, not
inside `alexgshaw/regex-log:20251031`. It also establishes no regex or log-parsing correctness (no case
shows a correct pattern for real logs, that a canonical pattern exists, or that the 25-line log
represents a real log), no contamination measurement (the log and its literal dates are the grader's own
fixture), nothing about task difficulty, quality or gameability (an accepted shortcut says nothing about
how any agent behaves), and no harness fidelity: the probe runs host CPython 3.14.8 while `test.sh:18-20`
runs `uvx -p 3.13` with `pytest==8.4.1`, so the `invalid-regex` `re.error` text is interpreter-dependent.
```
Grounding for the added facts: `python3 --version` → `Python 3.14.8`;
`corpus/evidence/round36/tb2-regex-log/test.sh:18-20` → `uvx \ -p 3.13 \ -w pytest==8.4.1`; the capture
dir carries `__pycache__` beside the six captured files (`ls corpus/evidence/round36/tb2-regex-log/`),
consistent with several interpreters having run it. No receipt byte is "repaired".

---

## 5. Fix F8 — declined (both targets)

F8 asked for (a) a sub-row/arithmetic form of the `coverage` label in the round-36 claims file and (b)
demotion of "a new edge class for the probe".

**Declined, with reasons:**
1. `plans/round-36-claims.md:63` still reads "and a new edge class for the probe: the". That file is a
   frozen claim record of a closed round; the current round's own rule is "A rule changed after a seat
   has scored is not the claim's rule" (`plans/round-37-claims.md:9`). Editing it now would rewrite the
   record a seat was judged against.
2. The score half of F8 is already landed: `SCORECARD.md:1222` records `**7 → 7 held** (L0 cap); frozen
   predicate met` for the round-36 row. The sub-row split (surfaces vs constructs) is a presentation
   change on a closed row; it changes no number. If the L1 wants it, the place is the round-37 row, not
   a retro-edit of `:1222`.

**Residual vector (reported, not mine to fix):** `plans/round-37-claims.md:64` repeats the construction —
"and a new grader class for the lane". That is the exact phrase F8 asked to demote; it is in the frozen
round-37 claims, so the wave-2 critic/L1 must rule on it. My paragraph says "a class the lane had not
run", which is an execution fact, not a construct claim.

---

## 6. Fix F10 — declined as written

F10 proposed amending the `pinned-grader-probe` cell (`SCORECARD.md:562`) from "a frozen table of
synthetic **outputs**" to inputs-plus-patterns. The landed disposition went the other way: round 36
registered a sibling row, `pattern-valued-grader-probe` (`SCORECARD.md:565`, "The pinned-grader-probe
instrument on a grader whose graded artefact is an agent-authored regex file"), first-working round 36.
Widening `:562` now would make two rows claim the same 24-case probe and leave `:565` redundant. F10's
intent (the second task sits inside a named capability) is met by `:565`; the round-37 equivalent is a
third sibling row for the service/state case, which is the L1's SCORECARD edit, not a PROVINCE edit.
I therefore propose no `:562` change.

---

## 7. Adjacency (lanes touched, citations)

Read at current tips (several lanes have advanced past kengaku-round-36 numbering; see the stale-citation
finding below).

| Lane | Cited | What it owns (≤25-word quote) |
|---|---|---|
| tameshi | `tameshi-shokunin/PROVINCE.md:3,14-17,44-45` | "**Domain:** verification-fixture craft — the reusable method of honest" (`:3`); "Never edits a sibling's gate code" (`:16-17`) |
| chousa | `chousa-shokunin/PROVINCE.md:5-7,10-11` | "question framing; source hierarchy … citation chaining and hop resolution" (`:5-6`); "model-quality or evaluation claims (→ kengaku)" (`:11`) |
| kotoba | `kotoba-shokunin/PROVINCE.md:3` | "**Domain:** prompt & skill craft — scopes SKILL.md/AGENTS.md quality, trigger fidelity" |
| kumitate | `kumitate-shokunin/PROVINCE.md:24` | "orchestration topology **decisions** (how a wave's seats are arranged …), not agent evaluation" |
| kama (adjacent, not absorbed) | `kama-shokunin/PROVINCE.md:3,10` | "local model serving & endpoint health" (`:3`); "read-only service inspection of local serving ports" (`:10`) — the probe's HTTP service is sandbox fixture state, not a served model |

The paragraph names only tameshi, chousa, kotoba and kumitate, matching the round-36 form; kama is cited
here because a reader of "live HTTP service" would look for a service owner. It does not apply: kama
governs endpoint identity/health for local model serving, and the probe's service exists only inside the
per-case namespace (`plans/git_webserver_probe.py:204`, `bwrap --unshare-net`).

**Unowned ground (finding):** no fleet lane claims nginx/git/ssh administration or git push/repo
semantics. `for f in *-shokunin/PROVINCE.md; do grep -l -i 'nginx' "$f"; done` → no output;
`… -i 'git administration\|git server\|git push'` → no output, exit 1 (run at the fleet root). So the
paragraph's "own nginx, git or ssh administration" is a correct refusal, and the fleet has no owner for
it — a report-out, not an absorption.

**Stale citations in the landed round-36 paragraph (finding for the L1):**
- `PROVINCE.md:253` cites `kotoba-shokunin/PROVINCE.md:61`; that line is now the `kaidoku` adjacency row
  (`sed -n '61p'` → `| kaidoku | none | …`). kotoba's prompt-craft domain line is `:3`.
- `PROVINCE.md:253-254` cites `kumitate-shokunin/PROVINCE.md:23,28`; `:23` is now durable-execution
  research and `:28` is MCP/OAuth routing. Seat arrangement is `:24`.
- tameshi (`:3,14-17,44-45`) and chousa (`:5-7,10-11`) citations still land on the quoted text.
These are only fixable if F6 lands in-place (§3.3); otherwise the appended correction can carry the two
corrected citations in one extra clause.

---

## 8. Dependencies and gate state (why this draft cannot land alone)

The paragraph points at three artefacts that do not exist in the lane tree at this seat's read:

| Artefact | Check | Output |
|---|---|---|
| `corpus/knowledge/tb2-git-webserver-grader.md` | `ls` | `No such file or directory` |
| S111–S113 registry rows | `grep -cE '^\| *S11[123] *\|' corpus/SOURCES.md` | `0`, exit 1 |
| receipt | `tail -2 corpus/evidence/round37/git-webserver-probe.txt` | `cases=22 observed_pass=9 observed_fail=13 mismatches=0` (present) |

So the C2 predicate (`checks=7 defects=0`, `PREDICATE C2 pass`, `plans/round37_c2_verify.py` docstring) is
not reachable yet: V2/V4/V7 need the entry, V3 needs the rows. Land order for the L1: captures → entry +
S111–S113 rows + index/coverage row → PROVINCE paragraph. If the paragraph lands first, a reader hits two
dangling references.

Second-run byte-equality (the brief's claim) is evidenced, not re-run by me:
`.ufo/waves/round-37/claims/measure-before-committed.txt:89` → `gate: P10 ok probe_rerun=byte-equal
bytes=8443`.

---

## 9. Evidence (every claim with its command)

| Fact | Command | Output |
|---|---|---|
| round-36 paragraph is 139 words | `awk 'NR>=244 && NR<=255' PROVINCE.md \| wc -w` | `139` |
| round-35 paragraph is 103 words | `awk 'NR>=232 && NR<=240' PROVINCE.md \| wc -w` | `103` |
| draft paragraph is 139 words | `len(body.split())` in the seat kernel | `139` |
| PROVINCE ends at :257 | `wc -l PROVINCE.md`; `awk 'NR>=250 && NR<=256'` | `257` lines; `:255` is the round-36 last line |
| F6 rewrite is 134 words | read `.ufo/waves/round-36/build/R36CritScope/province-rewrite.txt` | 134 (`len(split())`) |
| entry oracle heading/body | `awk 'NR>=149 && NR<=152' corpus/knowledge/tb2-regex-log-grader.md` | `:148` heading, `:150-152` body ending `row**:` |
| F4 sentence verbatim | `sed -n '176,180p' …tb2-regex-log-grader.md` | ends "…cannot see the difference." at `:179` |
| F5 anchor | `awk 'NR>=208 && NR<=218' …` | Negative space `:210-218` |
| entry amendment form | `grep -n 'amended' …tb2-regex-log-grader.md` | `:43` "amended **before any seat scored**" |
| host interpreter | `python3 --version` | `Python 3.14.8` |
| image interpreter | `grep -n 'uvx\|3\.13\|pytest' corpus/evidence/round36/tb2-regex-log/test.sh` | `18:uvx`, `19: -p 3.13`, `20: -w pytest==8.4.1` |
| capture dir contents | `ls corpus/evidence/round36/tb2-regex-log/` | six captures + `SHA256SUMS` + `__pycache__` |
| probe sandbox | `grep -n 'bwrap\|--unshare-net' plans/git_webserver_probe.py` | `:204` `--unshare-net --unshare-pid …`; `:9-10` "private network namespace" |
| receipt summary | `tail -2 corpus/evidence/round37/git-webserver-probe.txt` | `cases=22 observed_pass=9 observed_fail=13 mismatches=0` |
| graded-without-git observation | `sed -n '7p' corpus/evidence/round37/git-webserver-probe.txt` | `CASE static-file-no-git … verify.sh:49 never reads the expect step's status …` |
| second run byte-equal | `grep -n 'byte-equal' .ufo/waves/round-37/claims/measure-before-committed.txt` | `:89 gate: P10 ok probe_rerun=byte-equal bytes=8443` |
| SCORECARD capability basis | `read SCORECARD.md:562`; `:565` | `:562` "synthetic outputs"; `:565` `pattern-valued-grader-probe` … "agent-authored regex file" |
| round-36 score row | `grep -n '7 → 7' SCORECARD.md` | `:1222` `**7 → 7 held** (L0 cap); frozen predicate met` |
| round-36 closed | `sed -n '1244p' SCORECARD.md` | "**Wave 2 was not dispatched.** The operator ended the run" |
| F8 residual | `grep -n 'a new grader class' plans/round-37-claims.md` | `:64` |
| F8 frozen rule | `grep -n 'A rule changed after' plans/round-37-claims.md` | `:9` |
| round-36 claims frozen phrase | `grep -n 'new edge class' plans/round-36-claims.md` | `:63` |
| TB2 task count (86) | `read corpus/knowledge/benchmark-verifier-execution-model.md:93,131` | "of its 89 `tests/test.sh` files"; "89 directories and 3 files" |
| adjacency quotes | `sed -n '3p;14,17p;44,45p' tameshi-shokunin/PROVINCE.md`; `sed -n '5,7p;10,11p' chousa-shokunin/PROVINCE.md`; `sed -n '3p' kotoba-shokunin/PROVINCE.md`; `sed -n '24p' kumitate-shokunin/PROVINCE.md`; `sed -n '3p;10p' kama-shokunin/PROVINCE.md` | quoted in §7 |
| stale kotoba citation | `sed -n '61p' kotoba-shokunin/PROVINCE.md` | `\| kaidoku \| none \| …` (kotoba domain is `:3`) |
| stale kumitate citations | `sed -n '23p;28p' kumitate-shokunin/PROVINCE.md` | durable-execution research (`:23`), MCP/OAuth routing (`:28`); seat arrangement is `:24` |
| no nginx owner | `for f in *-shokunin/PROVINCE.md; do grep -l -i 'nginx' "$f"; done` | no output |
| no git-admin owner | `… grep -l -i 'git administration\|git server\|git push'` | no output, exit 1 |
| entry absent | `ls corpus/knowledge/tb2-git-webserver-grader.md` | `No such file or directory` |
| registry rows absent | `grep -cE '^\| *S11[123] *\|' corpus/SOURCES.md` | `0`, exit 1 |
| probe digest matches claims | `grep -n 'PROBE_SHA256 =' plans/round37_c2_verify.py` vs claims `63cb75cf…5eedf` | identical `63cb75cfcd1c224a…d3a5eedf` |

No tool was installed or upgraded (none needed). No counter was run: C1/C2 belong to the executor seats
and the L1 measures the predicates after all wave-1 work lands.

---

## 10. Touched surfaces and out-of-scope

- **Touched:** `.ufo/waves/round-37/build/R37ProvinceDraft.md` (this file) and
  `.ufo/waves/round-37/build/R37ProvinceDraft/province-round37-dropin.md` only.
- **Not touched:** no lane file (`PROVINCE.md`, `corpus/`, `plans/`, `SCORECARD.md`, `README.md`,
  `SKILL.md`, `SHONEN.md`), no git index, no jj state, no scratch tree, no sibling lane.
- **Out of scope by rule:** landing the paragraph; SCORECARD row/capability edits (F8/F10's real home);
  amending the admitted round-36 entry (needs an L1 ruling); running C1/C2.

---

## 11. Limits

- Word counts use Python `str.split()` on the paragraph body only (heading excluded). A different counter
  could differ by one or two tokens; the draft is at 139 of a 140 ceiling, and the artifact records a
  130-word cut if the L1 wants slack.
- F3/F4/F5 are pairs against an **admitted** entry; landing any of them changes a round-36 record after
  admission. I drafted them append-shaped where possible but did not adjudicate legality — that is the
  L1's call, and F6 already carries the same refusals at PROVINCE level.
- I read the round-37 receipt and probe source, not a fresh probe run; execution claims in the paragraph
  rest on the committed receipt and the frozen case table, and on
  `.ufo/waves/round-37/claims/measure-before-committed.txt:89` for byte-equality.
- Adjacent-lane heads were read at today's tips; two lanes (kotoba, kumitate) have advanced far past the
  line numbers the landed round-36 paragraph cites, which is why I cited current lines and flagged the
  drift rather than reusing `:61` / `:23,28`.
- I did not read any round-37 entry draft (absent) or SCORECARD round-37 row (not yet written); the
  paragraph's capability framing therefore stays descriptive and avoids naming an unlanded row.

VERDICT: province-drafted-4-fixes
