# SourcesHostR75 — round 75, w1 — source opening and host re-verification

seat: `SourcesHostR75`, role scout (leaf; no subagent dispatch).
Observed revision: lane `HEAD` = `43255758` (Amendment A1); worktree state in §4.
Scratch used and deleted: `/fast/scratch/hyaku/kengaku-r75/SourcesHostR75`.
Every number below names the command that produced it and its exit code; nothing is quoted from
the L1's prose without re-reading the committed bytes.

## 1. S251 — live re-fetch vs the committed capture

Fetch, run in my scratch dir (never the lane checkout):

```
cd /fast/scratch/hyaku/kengaku-r75/SourcesHostR75
curl -sS -m 60 -o git-rev-parse.html -w 'http_code=%{http_code}\n' https://git-scm.com/docs/git-rev-parse
echo "curl_rc=$?"
```

| field | fresh fetch | committed capture |
|---|---|---|
| HTTP code | `http_code=200` (curl rc 0) | n/a (file) |
| bytes (`wc -c`) | `122459` | `122459` |
| sha256 | `00e3b1aaf8ae9df59a7a6bb8224e19e825c628b7a0cd69a4f03aeda79c2be587` | `00e3b1aaf8ae9df59a7a6bb8224e19e825c628b7a0cd69a4f03aeda79c2be587` |
| `cmp` fresh vs `corpus/evidence/round75/sources/git-rev-parse.html` | `cmp_rc=0` | — |

**Verdict: byte-identical, no delta.** The capture names exactly the bytes the URL serves today, so
the row's `recheck: on-release` is satisfied by this fetch.

Quote location and length:

```
sed -n '2720p' corpus/evidence/round75/sources/git-rev-parse.html
→ <p>Verify that exactly one parameter is provided, and that it
sed -n '2720p' /fast/scratch/.../git-rev-parse.html   → same line
printf '%s' 'Verify that exactly one parameter is provided, and that it can be turned into a
  raw 20-byte SHA-1' | wc -w                            → 18
```

Line 2720 is the first line of the `--verify` option paragraph: line 2717 is `--verify` and the
sentence continues on 2721–2722 (`…raw 20-byte SHA-1 that can be used to access the object
database…`). The frozen quote is **18 words**, inside the ≤25 requirement. `grep -n` finds the
sentence once in the capture (`2720:`), so the anchor is not ambiguous.

Scope confirmation for the row's teaches cell: the paragraph describes *resolving* a rev and
emitting the object id; it does not certify that a tree produced printed numbers, which is why
R75-C2's ancestry leg (`git merge-base --is-ancestor`) is a separate check. S251 as written is
correct for the `--verify` acceptance claim only.

## 2. Host surfaces — seven facts, verbatim

| # | command | output | exit code |
|---|---|---|---|
| 1 | `curl -s -m 5 -o /dev/null -w '%{http_code}' http://127.0.0.1:34113/health` | `000` | 7 |
| 2 | `pgrep -a llama-server` | `1505 /home/vgpnk/src/llama.cpp/build/bin/llama-server --models-dir /home/vgpnk/models/lfm3 --models-preset /home/vgpnk/models/lfm3/presets.ini --models-max 2 --host 127.0.0.1 --port 1234 --jinja` | 0 |
| 3 | `test -d ~/archive/bench-arena` | (no output) | 1 |
| 4 | `test -d ~/Projects/bounties` | (no output) | 1 |
| 5 | `test -d ~/Projects/webzites/repos/llm-wiki` | (no output) | 1 |
| 6 | `test -d ~/Projects/ufo-fsd-alpha` | (no output) | 0 |
| 7 | `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log --oneline -3` | `43255758 round-75: A1 — stamp every receipt mode, claims Before corrected by counted values` / `e462a649 round-75: freeze — index-parity gate (R75-C1), attributed registry audit (R75-C2), S251, lesson Gate/Mistakes` / `4c4249a2 round-74 verifier spot-check (integrator, hyaku): non-author admit/reject` | 0 |

Readings (kept separate from the facts above):

- Fact 1 is a refused connection (`curl` rc 7), not an HTTP error: nothing is listening on
  `127.0.0.1:34113`. [INFERENCE] The model host itself is alive — fact 2 shows `llama-server`
  bound to `127.0.0.1:1234` — so a probe aimed at `:34113` measures a port-on-this-host, and any
  round-75 claim that depends on `:34113` would be measuring an absent service, not a slow one.
- Facts 3, 4, 5: three of the four trees earlier rounds treated as surfaces are absent on this
  host; only `~/Projects/ufo-fsd-alpha` (fact 6) resolves. `corpus/README.md:346` already records
  bench-arena as unavailable (moved to `~/archive/bench-arena`, then gone); this probe confirms
  both paths are still gone.
- Fact 7: the A1 commit is HEAD; the base and freeze commits are the next two entries, so the
  round's chain `4c4249a2 → e462a64 → 43255758` is linear and present locally.

## 3. Planning data-walk (bounded) — what is still open after R75-C1/C2

Sources read in full at the observed revision: `plans/round-75-claims.md` (frozen claims + A1);
`plans/round-74-claims.md` tail (Frontier step + A1); `corpus/lessons/round-74-verifier-spotcheck.md`
§6; `corpus/lessons/round-73-verifier-spotcheck.md` §6; `corpus/lessons/round-72-verifier-spotcheck.md`
§6–7; `corpus/lessons/round-75.md`; `SCORECARD.md`'s last §Planned block
(`### Planned (round 74; not new round work here)`, `SCORECARD.md:3320-3326`), quoted verbatim:

> Freeze against the projected registered tree; replace malformed-row skipping with a named defect;
> bind a declared instrument universe independently of rows that advertise themselves. Use the
> seats' preserved false-green fixtures to price exact entry argv and erratum semantics, without
> re-scoring either round73 claim. Outside-observed HF provenance remains unimplemented and held.
> Open L0 questions unchanged: kengaku rounds25/33/51,54,56,63,65,66,67.

That block is the last planner-authored §Planned in `SCORECARD.md`; there is no `Planned (round 75)`
and no `Planned (round 76)` block (`grep -n Planned SCORECARD.md | tail -1` → `3320`).

### 3a. Routed defects of rounds 72–74 — one line each, status measured

| id | status after R75-C1/C2 | evidence / command |
|---|---|---|
| R72-V1 dead landing-hash citation | **closed** — errata item 1 names the corrected object | `.ufo/reports/round-73/kengaku.md:177` |
| R72-V2 `census-after.txt` revision label | **closed** — errata item 2 withdraws attribution and orders it not be attributed to the tip rerun | `.ufo/reports/round-73/kengaku.md:178` |
| R72-V3 reject-ground `N14`/`N20` sweep | **closed** — errata item 3 withdraws the fabricated negative sweep | `.ufo/reports/round-73/kengaku.md:179` |
| R71-R2 carried receipt-revision attribution | **closed** — errata item 4 names the receipt's measured revision `c80fcdb3…` | `.ufo/reports/round-73/kengaku.md:180` |
| R72-D1 five missing registry rows | **closed** — five hyphen-form rows present, one each | `for r in round66-c1-tensor-probe round69-c1-nginx-probe round69-c2-routed-defects round70-c1-nginx-probe round70-c2-routed-defects; grep -c "^| \`$r\`" SKILL.md` → 1,1,1,1,1 |
| R72 §6 item 6 carried instrument limits (not defects of that claim) | **open, unchanged** — see 3b | `corpus/lessons/round-72-verifier-spotcheck.md:155-160` |
| R73 routed defects | **none existed** — "no routed defects to the lane this round"; the round's limits are filed, not routed | `corpus/lessons/round-73-verifier-spotcheck.md:71` |
| R74-D1 receipts carry no measured revision | **class closed prospectively; record defect open** — `--check-stamps` exists and fails the round-74 evidence (`STAMPS files=11 stamped=0 unstamped=11`, `PREDICATE R75-C2 fail`), but the round-74 receipts are still stamp-free (`grep -c LANE_TIP corpus/evidence/round74/*.txt` → 0 for all 11) and the A2 erratum the spotcheck prescribed is absent (`grep -c Amendment plans/round-74-claims.md` → 1, A1 only) | `corpus/evidence/round75/c2-stamp-red-before.txt`; `plans/round75_c2_registry_audit.py:133-160` |
| R74-D2 stale `MISSING 5` line | **closed as a correction this round** — dated line appended in place naming the receipt's actual `ADVERTISED total=115 … MISSING 0` | `corpus/lessons/round-74.md:53` |
| R74-D3 false "deletion column is 0" | **open at observation** — the sentence still stands, measured numstat is `3 1` on `SKILL.md`; no dated correction exists (`grep -c R74-D3 SCORECARD.md` → 0) | `sed -n '3373p' SCORECARD.md`; `git diff --numstat b7910802 cbb8b8d8 -- SKILL.md` → `3	1	SKILL.md` |
| R74-D4 any-defect kill counting / literal tallies / no null arm | **class closed prospectively; combined-run receipt not yet measured** — `--mutants` now prints `MUTANTS real=9 expected_matched=9 wrong_id=0 survived=0 null_arms=1 null_survived=1 total=10`, and the off-target control prices the old metric at 10/10 vs 9/10 `wrong_id=1`; but the frozen counting command's `STAMPS files=K stamped=K` line has no committed receipt (`ls corpus/evidence/round75/*.txt | wc -l` → 8, no `c2-after.txt`), so `K` is unmeasured at observation | `corpus/evidence/round75/c2-audit-mutants.txt`; `c2-control-attribute.txt` |
| R74-D5 no claim evidence cites `S###` | **addressed in prose, not in receipts** — S251 is cited in `plans/round-75-claims.md` (2 mentions), `corpus/SOURCES.md` (1), `corpus/lessons/round-75.md` (3), and `plans/round75_c2_registry_audit.py` (1); no round-75 *receipt* names it (`grep -rn S251 corpus/evidence/round75/` → `sources/git-rev-parse-anchor.md:1` only) | those four greps |
| R74 conformance note (prompt authored by the lane) | **not a defect**, unchanged; promotion-owned | `corpus/lessons/round-74-verifier-spotcheck.md:190` |

### 3b. Carried instrument limits still open (named by the lane, never routed as defects)

- Forged-but-consistent receipts still pass `--check-receipt`; R75-C2's stamp leg proves resolvability
  and ancestry, not that the bytes were produced at the named revision (it validates the `LANE_TIP`
  line, not the measurements) — `corpus/lessons/round-72-verifier-spotcheck.md:155-156`.
- `transformers_file` is still prefix-checked in `plans/round72_c1_hf_probe.py` (`grep -n transformers_file`
  → :197, :607-618).
- `E1a` is still a frozen four-entry tuple, first-row-wins; `E1b` is still presence-only
  (`plans/round72_c2_routed_defects.py:56-61`).
- The R72-C2 mutant matrix still prices 6 of ~13 refusal sites (spotcheck :157) — R75-C2 is a new
  instrument with 9 real mutants, it does not widen that matrix.
- Four knowledge entries still carry `admission: hold` and no second-seat falsify wave is on record:
  `grep -l 'admission: hold' corpus/knowledge/*.md` → `instrument-registry-derivation.md`,
  `registry-argv-and-flag-audit.md`, `tb2-hf-model-inference-offline.md`,
  `tb2-hf-model-inference-provenance.md`. Round 75's lesson names three; the fourth
  (`tb2-hf-model-inference-offline.md`) is the round-72 candidate and is still held.
- R73 limits that remain limits, not defects: structural-not-semantic audit (R75's audit still
  parses with `ast.parse`, one call), 13/16 adversarial battery accepted, pad-able A1.

### 3c. Planner-facing leftovers from the last §Planned

- "Outside-observed HF provenance remains unimplemented and held" — still true; no round-75 seat
  touches it.
- "price … erratum semantics" — R75-C2 prices entry argv (`:entry:flag-not-declared:`) but nothing
  prices erratum semantics; that half of the item survives.
- L0 carried: `kengaku | round-25/33/51`, `54`, `56`, `63`, `65`, `66`, `67` (round 75's frontier
  names only `round-54`; the rest are still carried).
- The five rows R72-D1 named are registered but advertised only through `plans/round-66/69/70/73`
  claims docs — the registry row is present, the "advertised universe" question is now round-74's
  `files=136 plans_seen=90`, not this list.

## 4. State notes measured at observation (not claim scores)

- `git status --porcelain` at `43255758`: `M PROVINCE.md`, `M corpus/README.md`,
  `M corpus/lessons/round-75.md`, `M plans/round-75-claims.md`, `M plans/round75_c1_index_parity.py`,
  `M plans/round75_c2_registry_audit.py`, `?? .ufo/waves/round-75/`, `?? corpus/evidence/round75/`
  (8 `.txt` receipts). The index repair therefore exists only as uncommitted working-tree edits at
  observation; committed `corpus/README.md` at A1 has 71 `knowledge/` and 87 `lessons/` index rows
  (`git show 43255758:corpus/README.md | grep -c '^| \`knowledge/'` → 71; `… '^| \`lessons/'` → 87),
  matching the before receipt's `indexed=` values; the working tree has 74 and 123.
- The before receipt is self-consistent with a clean clone at A1: `corpus/evidence/round75/` exists
  there because `sources/` is tracked (`git ls-files corpus/evidence/round75 | wc -l` → 2), which is
  why `MISSING-EVIDENCE round75` can print in a clone that has no receipts.
- `WORKTREE clean` is a *tracked-tree* claim: both instruments compute it with
  `git status --porcelain --untracked-files=no` (`plans/round75_c1_index_parity.py:66`,
  `plans/round75_c2_registry_audit.py:129`). Untracked receipts and the untracked wave dir do not
  dirty it; a receipt reader must not read the line as "nothing outside `LANE_TIP` exists".
- All 8 round-75 receipts carry `LANE_TIP 43255758ed7d74ea05c8e03686dd9ad37837f0cd` +
  `WORKTREE clean`; `census-before.txt` carries `LANE_TIP 4c4249a2…` (base) — correct for a
  before-state capture.

## 5. Remaining unknowns (stated, not filled)

- `STAMPS files=K stamped=K unstamped=0 unresolved=0 not_ancestor=0` with `K > 0` is unmeasured: the
  frozen counting command's green run has no receipt yet. Only the round-74 red (`files=11 stamped=0`)
  and the 4-arm selftest's synthetic stamp arm (`files=2 stamped=1 unstamped=1`) exist.
- R74-D3's correction text does not exist at observation; only the integration owner can land it.
- I did not run `plans/round75_c1_index_parity.py` (claim scoring belongs to the replay seats); the
  evidence-dir `indexed=46` figure uses the gate's own matcher and is not reproducible from a simple
  `^| \`evidence/` row count (24 rows, which counts the other index's rows too).
