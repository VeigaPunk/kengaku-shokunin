# SiblingOverlap — round 65 w1, seat report (kengaku)

Seat: `SiblingOverlap` (connector, leaf, read-only). Round: kengaku r65 w1 (v1, 12 seats).
Scope: sibling-overlap scan for R65-C1 (`sqlite-with-gcov`, TB2 class `db-state`) and R65-C2.
Mode: read-only across the fleet; no file written outside this seat dir
(`.ufo/waves/round-65/w1/SiblingOverlap/`). No network open, no port bound, no package installed,
no git mutation. Receipt with every command + observed output: `.ufo/waves/round-65/w1/SiblingOverlap/scan-receipt.txt`.

## Method (what was searched)

The item's window is "SCORECARD.md tail, LOG.md tail, corpus/lessons/round-6[34]*.md". Sibling
lanes number their rounds independently, so the window was resolved per lane as *that lane's* last
two `corpus/lessons/round-N.md` files plus its whole `SCORECARD.md` and `LOG.md` (round numbers
observed: tabi 56–57, souji 52–53, kasegi 56–57, kaidoku 62–63, tsukuroi 64–65, tameshi 70–71,
mori 77–78, chousa 71–72, kama 68–69, kake 68–69, kumitate 72–73, kotoba 83–84, kotodama 80–81,
kagi 29–30, mado 63–64, revenger 87–88). All 16 named lanes exist. The window files were grepped
for `db-state`, `sqlite-with-gcov`, `query-optimize`, `gcov`, `sqlite3`; each hit was then opened
for context (no sibling corpus was opened beyond what a hit names).

## Per sibling

**tabi** — `tabi-shokunin/.ufo/waves/round-33/w1/ScribeSrcLauncher/receipts/Makefile.a7ed2cb89fe28c91199524c828866201c9d6b5e5:39`
`$(RM) $(CHROMIUM_NAME) runtests *.o *.{gcda,gcno,gcov}` — a vendored Chromium Makefile `clean`
rule inside an r33 wave receipt. Chromium's own build flags, no database, no grader. **Not an
overlap.** tabi's `SCORECARD.md`/`LOG.md` contain no `sqlite` string at all
(`grep -n -i sqlite tabi-shokunin/LOG.md tabi-shokunin/SCORECARD.md` → no output). No
`db-state`/`sqlite-with-gcov`/`query-optimize` anywhere in the lane.

**souji** — `souji-shokunin/LOG.md:405` "sqlite3 (3.53.4) checked per operator: live consumers =
1Password … and the /tmp seat DBs" — a host-consumer audit of a CLI tool, incidental. **Not an
overlap.** souji's one Terminal-Bench string is `souji-shokunin/census/round-31/waves/w2/SwarmConnector28.md:21`,
which *routes kengaku's* TB2 git-leak grader ground to kengaku ("kengaku holds measured plain-git
reflog/object-retention ground … Terminal-Bench 2 git-leak grader") — a sibling explicitly
deferring to kengaku's province, the opposite of a contest.

**kasegi** — `kasegi-shokunin/SCORECARD.md:1763,1803` use the word "grader" only for its own
pinned-artifact/mechanical corpus checks ("they are pinned-artifact graders … they do not certify
that the entry adds analysis"). `SCORECARD.md:1918` "79 class members in protected files" is
kasegi's own *class* of corpus rows, unrelated to TB2's `db-state` class. **Not an overlap.**

**kaidoku** — `kaidoku-shokunin/SCORECARD.md:3256-3271` (round 31) runs `rea
inspect-sqlite-database --schema-scope database` on 12 published SQLite files and compares against
an independent reader. This is a sibling **running SQLite tooling for its own domain** (a
third-party MCP reader's behaviour, oracle-checked) — under the item's own discriminator this is
explicitly *not* an overlap; it is not a Terminal-Bench grader and claims no benchmark-grader
capability. **Not an overlap.**

**tsukuroi** — r64/r65 lessons and LOG: systemd v262 NvPCR/UKI boot-chain plane and an
`initramfs-arm` census arm (`corpus/lessons/round-65.md:1-8`). No database, no grader, no TB2
string in SCORECARD/LOG. **Not an overlap.**

**tameshi** — r70/r71 lessons and LOG: no `db-state`, `sqlite-with-gcov`, `query-optimize`, `gcov`
or `sqlite3` hit; no Terminal-Bench string. **Not an overlap.**

**mori** — `mori-shokunin/LOG.md:1879,1913` matched only on the seat-name token
`CriticRoutingCoverage` (substring `gcov` inside "RoutingCoverage"); no gcov tooling. **Not an
overlap.**

**chousa** — `chousa-shokunin/SCORECARD.md:2859,2891` list `sqlite3.connect` as one of the
*hook-bypass classes* its own build-spans gate battery must defeat ("native `import` and
`sqlite3.connect` — round-56 routed item 3"). That is chousa's Python-subprocess-guard
operability surface, not a graded database surface. `SCORECARD.md:820-929` are about a
"LLM benchmarks" *scope-phrase* gap in a record classifier — no benchmark is run. **Not an overlap.**

**kama** — r68/r69 lessons and LOG: three portability repairs and a classifier-defect fixture
(`LOG.md:2588-2631`); "offline Ollama evidence replay" (`SCORECARD.md:457,504`) is a *local model
runtime* replay for kama's own domain, not a TB2 grader replay. **Not an overlap.**

**kake** — r68/r69 lessons and LOG: offline static canonical-link preflight over local HTML
(`SCORECARD.md:196`); no database, no grader. **Not an overlap.**

**kumitate** — the highest Terminal-Bench string count in the fleet (158 files), and it is worth
being precise about why it is not a contest: every occurrence is the **arXiv MAS-coordination
paper** `2512.08296v3`, whose benchmark list includes Terminal-Bench as a *research subject*.
Keyed hits: `kumitate-shokunin/corpus/knowledge/multi-agent-coordinator-topologies.md:29,53,83`
("Terminal-Bench (2 tools): Independent +1.7% …"; "S197 — 'Terminal-Bench shows mixed results:
Independent achieves marginal gains (+2%) while Centralized degrades (-19%)'") and
`kumitate-shokunin/corpus/lessons/round-63.md:13` (the Terminal-Bench caption rounding was *cut*
in the staged entry). These are coordinator-topology **data citations**, already ruled as such in
kengaku's round 37 (recorded in `kengaku-shokunin/PROVINCE.md:352-357`). kumitate's round-65 wave
touches `sqlite` only as oh-my-pi *source rows* (`K65ConnOmpSources/consistency.md:134-135`,
`K65ExecCollisionGuard/assimilation/doc-lane:54-56,88` — `packages/utils/src/sqlite.ts`,
`packages/ai/src/auth/sqlite-credential-store.ts`, sqlite.org WAL doc). **Not an overlap.**

**kotoba** — `kotoba-shokunin/LOG.md:143` "sqlite3 -readonly ~/.omp/agent/skill-descriptions.db"
— host drift measurement. `kotoba-shokunin/.ufo/waves/round-71/receipts/census-after.txt:28` names
the fleet census row `kengaku W04 S100 duplicate url github.com/laude-institute/terminal-bench-2`
— that row is kengaku's own registry row seen by the *fleet* census, not a kotoba claim. **Not an
overlap.**

**kotodama** — r80/r81 lessons and LOG: no database/grader/TB2 hit. **Not an overlap.**

**kagi** — `kagi-shokunin/LOG.md:124` (sqlite3 on an opencode DB), `:1610` (sqlite3-dependent
selftests), `corpus/lessons/round-30.md:10` (host sqlite3 present) — incidental host use.
`kagi-shokunin/SCORECARD.md:98,120` map sibling verifiers and name "kengaku `grader.py`" as a
*sibling verifier*, again a deferral. `kagi-shokunin/.ufo/waves/round-30/ConnOverlap-report.md:64,228`
clears "kengaku 'key management'" as "OpenSSL key management **as a benchmark grader surface**
(Terminal-Bench `openssl-selfsigned-cert` task)" — kagi explicitly classifies this as kengaku's
ground and does not claim it. **Not an overlap.**

**mado** — `mado-shokunin/.ufo/waves/round-47/w1/ConnSiblings/report.md:63` is a homonym note:
"kengaku 'Terminal-Bench 2.0' is a benchmark subject (kengaku SKILL.md:233-236) … Neither touches
the terminal-selection plane" — a deferral plus a homonym guard. `mado-shokunin/.ufo/waves/round-44/w2/RerunCensus/census-fleet.txt:32`
is the fleet census row naming kengaku's registry row. **Not an overlap.**

**revenger** — `revenger-shokunin/SCORECARD.md:958,976,983,988` (round 80) runs "a real SQLite
schema-inventory producer run (criterion F3, `sqlite`)" — `rea inspect-sqlite-database --schema-scope
database --format json` on one authored fixture, an oracle-checked record inside revenger's own
in-province F family. A sibling running SQLite tooling for its own domain; no grader, no TB2
string in SCORECARD/LOG. Its round-65 `R65LabAttribution.md:71` uses "grader" once for its own
`measure.py` exit-status gate. **Not an overlap.**

## Item 2 — does any sibling claim offline grader execution of ANY TB2 `db-state` class member?

No. Three independent measurements, all over committed bytes:

1. `grep -rl -i -- 'db-state' */ | grep -v '^kengaku-shokunin/' | wc -l` → **0**
   (`sqlite-with-gcov` → 0, `query-optimize` → 0). The three class-member names exist nowhere
   outside kengaku; inside kengaku `sqlite-with-gcov` appears in 101 files.
2. `grep -ci -E 'terminal[-_ ]bench'` on every sibling `SCORECARD.md` and `LOG.md` → **0 for all
   16 lanes**. No sibling SCORECARD planned/claims row (round 60+ window) even names the benchmark,
   let alone claims a class member execution.
3. Case-insensitive `grep -rli -E 'terminal[-_ ]bench' */` outside kengaku and outside `.ufo/`
   returns exactly three files, all analysed above and all deferring to kengaku: kumitate's two
   coordinator-topology files and souji's census connector note. Including `.ufo/` adds only
   historical wave receipts that quote kengaku paths or the fleet census row for kengaku's registry
   URL (kagi r30, kaidoku r41, kotoba r71, kumitate r61–62, mado r44, tabi r35, tsukuroi r43).

The lane's own standing check (`kengaku-shokunin/PROVINCE.md:352-357`, quoted in the receipt) says
the same thing: "Verified that no sibling reads, scores or claims TB2 grader execution". This seat
re-measured it rather than inheriting it, on the r65 tip.

## Reading against the item's discriminator

- "a sibling RUNNING sqlite tooling for its own domain is not an overlap" → kaidoku (r31,
  `inspect-sqlite-database` on 12 published files) and revenger (r80, `sqlite` schema-inventory
  producer) are exactly this case; both are their own domain's oracle-checked behaviour records,
  neither claims a grader capability.
- "a sibling claiming TB2 grader replay as a capability is" → no sibling does. Zero TB2 strings in
  any sibling SCORECARD/LOG; zero `db-state` class-member names anywhere outside kengaku.
- kumitate's 158-file Terminal-Bench count is the only thing that could look like a contest at
  grep scale; on reading it is a MAS-coordination paper's benchmark table, already ruled in kengaku
  round 37, and it states nothing about grader execution.

## Risks / limits of this scan

- The scan is grep-scoped to the item's named surfaces plus the class-member names; a sibling
  holding TB2 grader ground under different wording (not "Terminal-Bench", not "db-state") would
  not be caught by it. The strongest independent check here is the *absence* of the class-member
  names fleet-wide and of any TB2 string in sibling SCORECARD/LOG, which is what the item asks for.
- Sibling lanes' round numbering is independent of kengaku's; the "round-6[34]" window in the item
  has no literal counterpart in most siblings, so the per-lane last-two-lessons resolution was used
  and is stated above (read-only; nothing in the lane's round-64/65 claims or lessons was touched).
- No sibling file was modified; nothing in the frozen claims, counters, kill rules or leg vectors
  is affected by this seat.

## Verdict

OVERLAP: none
