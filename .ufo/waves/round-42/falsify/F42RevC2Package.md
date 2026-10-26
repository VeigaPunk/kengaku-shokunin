# F42RevC2Package — C2 package review (kengaku round 42, wave 2 FALSIFY)

Seat: reviewer, leaf. Target: the C2 package as landed at docs-tip `508434ad55c709337065611691c426f05875492d`.
Landing `ff14d76d…` verified its ancestor (`git merge-base --is-ancestor ff14d76d… 508434a…` → ancestor). Live tip
moved to `3e8a2e5e…` during this review (2026-10-26 18:14); every defect below was re-grepped present at the live
tip — none already fixed. All line numbers are at `508434a`.

Scratch: `/fast/scratch/hyaku/kengaku-r42/F42RevC2Package` (pinned clone + work dirs; removed after this report).
Receipts: `F42RevC2Package/` beside this file.

## 1. What I ran (command → output)

1. **Clone/pin**: `git clone -q --no-local <lane> $S/lane && git -C $S/lane checkout -q 508434a…` →
   `toplevel=$S/lane`, `head=508434a…`, `git status --porcelain` = 0 entries.
2. **`--dry`**: `python3 plans/fibsqrt_probe.py --lane . --dry` → exit 0; `diff` vs
   `corpus/evidence/round42/fibsqrt-dry-cases-freeze.txt` empty; both sides sha256
   `9ee60af69ba3dc9fb1585dbaeb33faef2e96c92977d555837565ce416f6898b5` (= the spec's `DRY_SHA256`).
3. **`--stage-check`** (Q32 envelope): `stagecheck cases=16 failed=0`, exit 0; output file has 17 lines, all 16
   `STAGECHECK … rc=0`.
4. **Counter** (Q32 envelope): `python3 plans/round42_c2_verify.py --lane . --work $S/work` → V1–V9 all `ok`,
   `checks=9 defects=0`, `PREDICATE C2 pass`, exit 0, wall 56.56 s; gate P1–P10 all ok, `P10 ok
   probe_rerun=byte-equal bytes=4212`; lane `git status --porcelain` after = 0 entries.
5. **Census**: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin kengaku` → `kengaku ok …/corpus/SOURCES.md`, exit 0 (15 `W04 duplicate url`
   warnings, all on pre-existing rows S040–S100; none on S125–S128). Pinned registry: same script
   `validate --file $S/lane/corpus/SOURCES.md` → `file ok`, exit 0.
6. **Negative exits**: `round42_c2_verify.py --bogus` → exit 2 (row's claim ✓); `fibsqrt_probe.py --lane . --dry
   --stage-check` → exit 2 ("mutually exclusive" ✓).
7. **Negative package run** (Q32 envelope): entry removed from a scratch `cp -a` of the clone → exit 1,
   `PREDICATE C2 fail`; `V4 DEFECT receipt or entry absent` **and** `V7 DEFECT receipt or entry absent` (the
   SKILL row's behavioral claim measured true); `V6 DEFECT census_exit=1` (the census's dangling-used-by leg
   catches the removed entry through SOURCES' used-by cells); `V9 DEFECT receipt, entry, PROVINCE.md or README
   absent`.
8. **External**: the three pinned raw URLs fetched and hashed — all three sha256 equal the spec pins (entry
   falsifier (a) holds). S128's issue fetched: quote "The official grader exercises 28 values, none above
   48,401." present in the body's Problem paragraph; created 2026-09-25T09:01:50Z, state CLOSED, closing comment
   2026-09-25T09:11:26Z — matches the S128 anchor cell; the issue also states all six candidate simulator sources
   match sha256 `700645ac…` = our sim.c pin.
9. **Denominator**: `curl -sSL …/terminal-bench-2/tar.gz/2fd12b88…` → `tar -tzf | grep -c
   "^[^/]*/[^/]*/task.toml$"` = **89** — the "8 of 89" denominator is exact. All nine captures re-hashed from the
   tarball: byte-identical to the pinned captures, and the repo's second copy
   (`circuit-fibsqrt/environment/tests/{test_outputs.py,sim.c}`, `environment/{Dockerfile,gates.txt}`) is
   byte-identical to the top-level `tests/` copies the pins name — no two-copies divergence in the provenance.
10. **"Re-pointed, none relaxed"**: AST-level diff of `plans/round41_c2_verify.py` vs `plans/round42_c2_verify.py`:
    `v1 v3 v4 v5 v6 v7 v8 derive receipt_cases rows dry spec sha256` IDENTICAL; `v2` differs only in the
    effective-spec filename. V9 is the only new check.

## 2. The task's checklist — results

| Item | Result |
|---|---|
| README index row cites S125–S128 and the receipt | PASS (`corpus/README.md:75` — all four ids + `evidence/round42/fibsqrt-probe.txt`), but see D6 |
| Coverage bullet | PASS (`corpus/README.md:271` — accurate; S128 correctly labelled "tier B prior art") |
| §Frontier "8 of 89" | PASS (`corpus/README.md:374`; PROVINCE.md:556 "remaining 81" consistent; 89 verified from the tarball) |
| PROVINCE line with task + entry name | PASS (`PROVINCE.md:539` — both on one line; counter V9(c) measured ok) |
| SKILL rows match the commands | PASS on every exit-code/interface claim measured, EXCEPT D2, D7, D8 below |
| census `validate --root` exit 0 | PASS (live and pinned forms) |

Also verified by reading (not machine-checked anywhere): the entry's line references into the captures —
`test_outputs.py` is exactly 147 lines and `sim.c` exactly 353 (`wc -l`), and every span the entry and
`SKILL.md:1170-1204` cite (`:7-11`, `:14-23`, `:56-147`, `:65-67`, `:73-102`, `:115-117`, `:119`, `:134`, sim.c
`:5`, `:9`, `:101`, `:113`, `:118`, `:122`, `:126`, `:127`, `:156`, `:319`, `:324`, `:328`, `:329`, `:330`,
`:335`, `:340`, `:343`, task.toml `:15/:18/:19/:22/:25/:29/:34`, Dockerfile `:2/:3/:6/:9-10`, test.sh
`:7-13/:18-22/:25-29`) resolves correctly — except D5. The 24 quotes are gate-checked verbatim (P4 ok) and I
re-read every quoted line in the captures myself. The lookup-circuit arithmetic checks out: 32 copies + 32 NOTs +
868 AND + 231 OR + 32 final copies = 1195 lines, 0 constants (all 32 bits covered; popcount sum 263), and the
bitflip case's 1196 lines follow from answer(41)=8 (bit 0 = 0).

## 3. Defects

**D1 (content — false arithmetic clause) — `corpus/knowledge/tb2-circuit-fibsqrt-grader.md:297`.**
Quote: "maximum, 48401 = 220²+1, is the only reach above 2^15" (finding 7). False under every reading: six of the
28 graded inputs lie above 2^15 = 32768 (43680, 43681, 43682, 48399, 48400, 48401 — the whole 209² and 220²
clusters), and nine distinct printed answers exceed 2^15 (recomputed from the probe's own `GRADED` table,
`plans/fibsqrt_probe.py:86-91`; 48400 and 48401 even share one answer, 3361931507). "reach" is defined nowhere in
the entry or `plans/round-42-claims.md` (grep: the clause occurs only at :297). The sentence's second half
("nothing grades an input outside the list") is true; the numeric clause is not derivable. Not flagged by any
wave-1 seat (grep over `.ufo/waves/round-42/build/` matches only the entry draft itself, `R42PkgEntry/…:294`).

**D2 (SKILL row line reference wrong for V7) — `SKILL.md:600`.**
Quote: "V4 and V7 both report the one string `receipt or entry absent` when *either* file is missing (`:178-184`)".
The string is at `plans/round42_c2_verify.py:184` (V4) and `:238` (V7); the cited range covers only V4's
occurrence. The behavioral claim itself is true (measured, §1.7) and wave-1 `R42RegistryRows.md:171` already
disclosed the conflation — only the citation is incomplete.

**D3 (internal inconsistency) — entry:96.**
The What-is-graded "Gate forms" row says a binary line whose `sscanf` fails is "dropped if that fails" — the
entry's own finding 5 (:275) says the line "is not skipped … the gate keeps its zero-initialised type,
`OP_CONST_0`", and S127's teaches cell (`corpus/SOURCES.md:142`) and `SKILL.md:1177` say "keeps … as a constant-0
gate". The table row repeats the exact "half the story" wording the entry's wave-1 integration section corrects in
the probe docstring.

**D4 (citation location) — entry:311.**
Finding 10 cites "(probe docstring" for "the probe runs every case with stdin on `/dev/null`" — the docstring
never states this (its only stdin mention, `plans/fibsqrt_probe.py:28`, is about sim.c); the fact lives in harness
code (`plans/fibsqrt_probe.py:201`, `stdin=subprocess.DEVNULL`).

**D5 (line-ref off-by-one) — entry:350.**
"the captured grader's own helpers (`test_outputs.py:26-52`)" — `isqrt` ends at :53 (`grep -n`: :52 `return x`,
:53 `x = x_new`). `SKILL.md:1190`'s own decision table cites "(`:26-53`, `:115-117`)" correctly.

**D6 (provenance label) — `corpus/README.md:75`.**
The index row's sources cell reads "S125, S126, S127, S128 (terminal-bench-2 @ 2fd12b88)" — S128 is an OpenAgents
issue (`github.com/OpenAgentsInc/openagents/issues/9645`), not a TB2-pin artefact. The lane's own convention
separates prior-art sources (`corpus/README.md:70`, round-37 row: "S111, S112, S113 (terminal-bench-2 @
2fd12b88); S114 (TB2.1 issue #133, prior report)"); the coverage bullet (:271) and PROVINCE (:539) label S128
correctly.

**D7 (overstated check description) — `SKILL.md:684-685`.**
Quote: "the entry's `## Case table` equal to the receipt row by row". V9(a) compares only (case id, test letters,
observed verdict) triples (`plans/round42_c2_verify.py:298`, `:301` `got != want`); the description cells are
paraphrases and differ (e.g. entry "padded to 32000 lines: the size test counts blanks" vs receipt "(sim ignores
blanks; the size test counts them)"). The counter docstring (:31-33) and the claims file state the check
precisely; the addendum's compression overstates it.

**D8 (undeclared dependency in the frozen gate) — `plans/pkg_gate.py:273-276` + `SKILL.md:686-687`.**
P10's fallback runs the probe under `uv run --no-project --with biopython==1.85 python3` although the fbsqrt probe
imports only stdlib (no `Bio` anywhere in `plans/fibsqrt_probe.py`); the in-code comment "(the pinned grader's
dependency)" is false for this package. On this host (python 3.14.8, `import Bio` fails — measured) the counter's
V2 therefore needs the biopython==1.85 wheel from uv's cache or the network; the SKILL addendum discloses only
"needs a writable `~/.cache` for `uv`". Measured working here (P10 ok, warm cache); an offline host with a cold
cache fails V2 on a sound package.

**D9 (nit) — entry:328.**
"this grader writes nothing outside its own `./sim` and pytest's cache" — the probe never runs pytest (the
harness calls the three functions directly; no pytest import in the probe's harness), so no pytest cache exists in
the sandbox the Regrade section describes; the clause is vacuous there.

## 4. Residual risk / not checked

- The `fda71ae` control narrative in `SKILL.md:600`'s controls cell is historical; not re-measured (needs that
  commit's shape).
- Probe exit-1 (stage-check failure) and the counter's per-V failure notes other than V4/V7/V9 were code-read,
  not exercised; `--work`-refusal and `--jobs` belong to the C1 row (out of scope).
- QUALITY Q33/Q34, SCORECARD/LOG/lessons/routed-findings are other seats' surfaces; not reviewed here.
- The counter was run on this host only; D8's cold-cache failure mode is inferred from the code path, not
  reproduced (no offline host available).

## 5. Receipts (this dir)

`c2run.txt` (pass run), `c2-negative-run.txt`, `stagecheck.txt`, `dry-out.txt`, `raw-fetch-sha256.txt`.
Q32 envelopes (three bwrap runs, envelope `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin
/home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <cmd>`):
`date +%T` 18:08:51→18:08:52 (stage-check), 18:08:59→18:09:55 (counter), 18:13:11→18:14:11 (negative run);
`ls -A /home/vgpnk/.local/bin | sha256sum` = `8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52`
before and after every run (unchanged). Installs: none.

VERDICT: c2-package-defects-9
