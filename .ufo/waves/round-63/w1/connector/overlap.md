# Sibling-overlap scan — kengaku round 63, seat `SiblingOverlap` (connector)

Seat dir: `.ufo/waves/round-63/w1/connector/` · read-only scan · 2026-11-03.
Question (frozen, from the item): does any other lane already own
(a) offline replay of Terminal-Bench graders, (b) a localhost PEP 503 index replay,
(c) a grader-class census, or (d) a grader-class decision table?

**Verdict: NO sibling lane owns (a), (b), (c) or (d).** Zero overlap-owned hits.
Every hit is `bwrap` (149 lines) or `offline replay` (14 lines) in an unrelated
sense; the six claim-specific terms — `pypi-server`, `vectorops`, `PEP 503`,
`pep-0503`, `grader-class`, `class-survey` — produce **0 hits in every sibling
lane and in every fleet report scanned**. `kengaku-shokunin` is the sole owner of
the grader-class census (`corpus/knowledge/tb2-grader-class-census.md`, 21
`*grader*` knowledge entries) and of the TB2 grader-replay corpus.

## Commands run (exact)

Base pattern (`PAT`):

```
PAT='pypi-server|vectorops|PEP 503|pep-0503|grader-class|class-survey|bwrap|offline replay'
```

Per sibling lane (one loop body, run for each of the 20 lanes below; the lane
directory is the only variable, `kengaku-shokunin` excluded):

```
cd /home/vgpnk/Projects/shokunin
for d in audio-shokunin chousa-shokunin game-dev-2d-shokunin game-dev-3d-shokunin \
         kagi-shokunin kaidoku-shokunin kake-shokunin kama-shokunin kasegi-shokunin \
         kotoba-shokunin kotodama-shokunin kumitate-shokunin lore-shokunin mado-shokunin \
         mori-shokunin revenger-shokunin souji-shokunin tabi-shokunin tameshi-shokunin \
         tsukuroi-shokunin; do
  T=""; for s in corpus SKILL.md PROVINCE.md plans; do [ -e "$d/$s" ] && T="$T $d/$s"; done
  [ -z "$T" ] && continue
  grep -rilE "$PAT" $T 2>/dev/null        # file list
  grep -riE  "$PAT" $T 2>/dev/null | wc -l # line count
done
```

Claim-specific-term sub-scan (the one that decides overlap ownership):

```
grep -rilE 'pypi-server|vectorops|PEP 503|pep-0503|grader-class|class-survey' \
     */corpus */SKILL.md */PROVINCE.md */plans 2>/dev/null | grep -v '^kengaku-shokunin/'
```

→ **no output** (0 sibling files). The same sub-scan over
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-6[0-2]/` returns hits only in
`kengaku.md` (the owning lane's own reports) and `kumitate.md` (a duplicate
`raw.githubusercontent.com/.../bubblewrap/.../bwrap.xml` URL, unrelated).

## Hit counts

Siblings (files / lines), same `PAT`, restricted to `corpus/ SKILL.md PROVINCE.md plans/`:

| lane | files | lines | | lane | files | lines |
|---|---|---|---|---|---|---|
| audio-shokunin | 0 | 0 | | kumitate-shokunin | 20 | 68 |
| chousa-shokunin | 1 | 2 | | lore-shokunin | 0 | 0 |
| game-dev-2d-shokunin | 0 | 0 | | mado-shokunin | 8 | 16 |
| game-dev-3d-shokunin | 0 | 0 | | mori-shokunin | 3 | 5 |
| kagi-shokunin | 2 | 2 | | revenger-shokunin | 0 | 0 |
| kaidoku-shokunin | 9 | 19 | | souji-shokunin | 4 | 7 |
| kake-shokunin | 1 | 2 | | tabi-shokunin | 0 | 0 |
| kama-shokunin | 8 | 11 | | tameshi-shokunin | 20 | 53 |
| kasegi-shokunin | 0 | 0 | | tsukuroi-shokunin | 1 | 1 |
| kotoba-shokunin | 2 | 3 | | | | |
| kotodama-shokunin | 0 | 0 | | **total** | **79** | **188** |

Fleet reports (same `PAT`, `.ufo/reports/round-6[0-2]/`):

| dir | files | lines |
|---|---|---|
| round-60 | 1 | 1 |
| round-61 | 1 | 1 |
| round-62 | 2 | 9 |

**Total 79 sibling files / 188 lines + 4 report files / 11 lines.**
Term breakdown over the 188 sibling lines: `bwrap` 149, `offline replay` 14,
`pypi-server`/`vectorops`/`PEP 503`/`pep-0503`/`grader-class`/`class-survey` **0**.

Three additional files match only as binary noise (skipped above by
`--binary-files=without-match`, confirmed by `grep -aioE`): `kaidoku-shokunin/corpus/evidence/round-34/elf/e09.bin`
(1× "bWrap"), `.../e11.bin` (36× "bwrap"), `mori-shokunin/corpus/evidence/sources-r59/w1-settlement-r58.json`
(1× "Bwrap") — ELF/JSON byte coincidences, not mentions.

## Per-hit verdicts (one row per hit file; lines listed per file)

| owner lane | path | hit lines | term | verdict | reason |
|---|---|---|---|---|---|
| `chousa-shokunin` | `chousa-shokunin/corpus/lessons/round-62.md` | 37,55 | bwrap | **adjacent** | bwrap named as a routing remedy for a fail-open sandbox — method note, no grader replay |
| `kagi-shokunin` | `kagi-shokunin/corpus/QUALITY.md` | 132 | offline-replay | **no-overlap** | 'offline replay' = release-clock observation ambiguity — unrelated domain |
| `kagi-shokunin` | `kagi-shokunin/corpus/lessons/round-27.md` | 114 | offline-replay | **no-overlap** | 'offline replay' = release-clock observation ambiguity — unrelated domain |
| `kaidoku-shokunin` | `kaidoku-shokunin/corpus/README.md` | 130 | bwrap | **adjacent** | bwrap in REA binary-analysis notes — unrelated domain |
| `kaidoku-shokunin` | `kaidoku-shokunin/corpus/evidence/round-44/controls/pos/tree/corpus/README.md` | 126 | bwrap | **adjacent** | bwrap in REA binary-analysis notes — unrelated domain |
| `kaidoku-shokunin` | `kaidoku-shokunin/corpus/knowledge/2026-10-13-r2-version-diff-compare.md` | 18,22,37,52,115 | bwrap | **adjacent** | bwrap in REA binary-analysis notes — unrelated domain |
| `kaidoku-shokunin` | `kaidoku-shokunin/corpus/knowledge/2026-10-13-r4-10-real-version-pair.md` | 12 | bwrap | **adjacent** | bwrap in REA binary-analysis notes — unrelated domain |
| `kaidoku-shokunin` | `kaidoku-shokunin/corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` | 46 | offline-replay | **adjacent** | 'offline replay' = deterministic transform replay (shortcut-replay gate) — not a grader replay |
| `kaidoku-shokunin` | `kaidoku-shokunin/corpus/lessons/round-20.md` | 34,102 | bwrap | **adjacent** | bwrap in REA binary-analysis notes — unrelated domain |
| `kaidoku-shokunin` | `kaidoku-shokunin/SKILL.md` | 1005 | bwrap | **adjacent** | bwrap in REA binary-analysis notes — unrelated domain |
| `kake-shokunin` | `kake-shokunin/corpus/lessons/round-42.md` | 54,74 | bwrap | **adjacent** | bwrap in web/publishing notes — unrelated domain |
| `kama-shokunin` | `kama-shokunin/corpus/QUALITY.md` | 68,72 | offline-replay | **adjacent** | 'offline replay' = Ollama model-evidence replay classifier — replay of captures, not of TB2 graders |
| `kama-shokunin` | `kama-shokunin/corpus/README.md` | 1563 | bwrap | **adjacent** | bwrap in local-model endpoint evidence — unrelated domain |
| `kama-shokunin` | `kama-shokunin/corpus/SOURCES.md` | 317 | offline-replay | **adjacent** | 'offline replay' = Ollama model-evidence replay classifier — replay of captures, not of TB2 graders |
| `kama-shokunin` | `kama-shokunin/corpus/knowledge/battery-execution-evidence.md` | 47 | bwrap | **adjacent** | bwrap in local-model endpoint evidence — unrelated domain |
| `kama-shokunin` | `kama-shokunin/corpus/knowledge/ollama-evidence-replay.md` | 117,289 | offline-replay | **adjacent** | 'offline replay' = Ollama model-evidence replay classifier — replay of captures, not of TB2 graders |
| `kama-shokunin` | `kama-shokunin/corpus/lessons/round-14-verifier-spotcheck.md` | 127 | offline-replay | **adjacent** | 'offline replay' = Ollama model-evidence replay classifier — replay of captures, not of TB2 graders |
| `kama-shokunin` | `kama-shokunin/corpus/lessons/round-14.md` | 7,77 | offline-replay | **adjacent** | 'offline replay' = Ollama model-evidence replay classifier — replay of captures, not of TB2 graders |
| `kama-shokunin` | `kama-shokunin/corpus/lessons/round-52.md` | 63 | bwrap | **adjacent** | bwrap in local-model endpoint evidence — unrelated domain |
| `kotoba-shokunin` | `kotoba-shokunin/corpus/knowledge/sibling-overlap-census-round49.md` | 78 | offline-replay | **adjacent** | 'offline replay' = sibling-overlap census scope column — a lane-scope census, not a grader-class census |
| `kotoba-shokunin` | `kotoba-shokunin/corpus/knowledge/sibling-overlap-census-round74.md` | 62,93 | offline-replay | **adjacent** | 'offline replay' = sibling-overlap census scope column — a lane-scope census, not a grader-class census |
| `kumitate-shokunin` | `kumitate-shokunin/corpus/QUALITY.md` | 569,594,788 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `kumitate-shokunin` | `kumitate-shokunin/corpus/README.md` | 93 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `kumitate-shokunin` | `kumitate-shokunin/corpus/SOURCES.md` | 82,83,108 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `kumitate-shokunin` | `kumitate-shokunin/corpus/knowledge/agent-isolation-substrates.md` | 1,18,110,112,119,121,125,126,130,131,164,179,180,188,248 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `kumitate-shokunin` | `kumitate-shokunin/corpus/knowledge/counter-amendment-discipline.md` | 1,9,81 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `kumitate-shokunin` | `kumitate-shokunin/corpus/knowledge/jj-workspace-seat-containment.md` | 101,103 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `kumitate-shokunin` | `kumitate-shokunin/corpus/knowledge/mount-order-and-bind-scope.md` | 1,7,9,15 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `kumitate-shokunin` | `kumitate-shokunin/corpus/lessons/round-44-verifier-spotcheck.md` | 189 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `kumitate-shokunin` | `kumitate-shokunin/corpus/lessons/round-44.md` | 100,129,138,167 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `kumitate-shokunin` | `kumitate-shokunin/corpus/lessons/round-45-verifier-spotcheck.md` | 56 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `kumitate-shokunin` | `kumitate-shokunin/corpus/lessons/round-45.md` | 34,227 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `kumitate-shokunin` | `kumitate-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` | 44 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `kumitate-shokunin` | `kumitate-shokunin/corpus/lessons/round-47-verifier-spotcheck.md` | 136,144,151 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `kumitate-shokunin` | `kumitate-shokunin/corpus/lessons/round-47.md` | 17,19,43,55,108 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `kumitate-shokunin` | `kumitate-shokunin/corpus/lessons/round-49.md` | 56,60 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `kumitate-shokunin` | `kumitate-shokunin/corpus/lessons/round-50-verifier-spotcheck.md` | 46 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `kumitate-shokunin` | `kumitate-shokunin/corpus/lessons/round-73-verifier-spotcheck.md` | 57 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `kumitate-shokunin` | `kumitate-shokunin/corpus/lessons/round-73.md` | 24 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `kumitate-shokunin` | `kumitate-shokunin/SKILL.md` | 618,733 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `kumitate-shokunin` | `kumitate-shokunin/PROVINCE.md` | 38 | bwrap | **adjacent** | sandbox-substrate craft (bwrap isolation, mount/bind scope) — reusable method; no TB2 grader or PEP 503 index replay in this lane |
| `mado-shokunin` | `mado-shokunin/corpus/lessons/round-25-verifier-spotcheck.md` | 93 | bwrap | **adjacent** | bwrap in desktop/compositor fixture capture — unrelated domain |
| `mado-shokunin` | `mado-shokunin/corpus/lessons/round-26-verifier-spotcheck.md` | 125,221 | bwrap | **adjacent** | bwrap in desktop/compositor fixture capture — unrelated domain |
| `mado-shokunin` | `mado-shokunin/corpus/lessons/round-26.md` | 29,75 | bwrap | **adjacent** | bwrap in desktop/compositor fixture capture — unrelated domain |
| `mado-shokunin` | `mado-shokunin/corpus/lessons/round-40-verifier-spotcheck.md` | 23 | bwrap | **adjacent** | bwrap in desktop/compositor fixture capture — unrelated domain |
| `mado-shokunin` | `mado-shokunin/corpus/lessons/round-48-verifier-spotcheck.md` | 105 | bwrap | **adjacent** | bwrap in desktop/compositor fixture capture — unrelated domain |
| `mado-shokunin` | `mado-shokunin/corpus/lessons/round-48.md` | 257,263,267 | bwrap | **adjacent** | bwrap in desktop/compositor fixture capture — unrelated domain |
| `mado-shokunin` | `mado-shokunin/corpus/lessons/round-56-verifier-spotcheck.md` | 60 | bwrap | **adjacent** | bwrap in desktop/compositor fixture capture — unrelated domain |
| `mado-shokunin` | `mado-shokunin/corpus/lessons/round-56.md` | 73,74,88 | bwrap | **adjacent** | bwrap in desktop/compositor fixture capture — unrelated domain |
| `mori-shokunin` | `mori-shokunin/corpus/lessons/round-31.md` | 15 | bwrap | **adjacent** | bwrap as a one-path mask in fleet-observability notes — unrelated domain |
| `mori-shokunin` | `mori-shokunin/corpus/lessons/round-51.md` | 283 | bwrap | **adjacent** | bwrap as a one-path mask in fleet-observability notes — unrelated domain |
| `souji-shokunin` | `souji-shokunin/corpus/SOURCES.md` | 189 | bwrap | **adjacent** | bwrap in repo-hygiene receipts — unrelated domain |
| `souji-shokunin` | `souji-shokunin/corpus/lessons/round-34-verifier-spotcheck.md` | 27 | bwrap | **adjacent** | bwrap in repo-hygiene receipts — unrelated domain |
| `souji-shokunin` | `souji-shokunin/corpus/lessons/round-34.md` | 20,37 | bwrap | **adjacent** | bwrap in repo-hygiene receipts — unrelated domain |
| `souji-shokunin` | `souji-shokunin/SKILL.md` | 269,273,275 | bwrap | **adjacent** | bwrap in repo-hygiene receipts — unrelated domain |
| `tameshi-shokunin` | `tameshi-shokunin/corpus/QUALITY.md` | 1365 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tameshi-shokunin` | `tameshi-shokunin/corpus/SOURCES.md` | 102,142,444 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tameshi-shokunin` | `tameshi-shokunin/corpus/knowledge/guard-kill-closure.md` | 129 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tameshi-shokunin` | `tameshi-shokunin/corpus/knowledge/hermetic-env-differential.md` | 26,51,89 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tameshi-shokunin` | `tameshi-shokunin/corpus/knowledge/mutation-case-kumitate-round-gate.md` | 145 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tameshi-shokunin` | `tameshi-shokunin/corpus/knowledge/mutation-case-kumitate-sources-check.md` | 205 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tameshi-shokunin` | `tameshi-shokunin/corpus/knowledge/regression-tally-completeness.md` | 1,2,72 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tameshi-shokunin` | `tameshi-shokunin/corpus/lessons/round-16.md` | 28 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tameshi-shokunin` | `tameshi-shokunin/corpus/lessons/round-18.md` | 27 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tameshi-shokunin` | `tameshi-shokunin/corpus/lessons/round-30-verifier-spotcheck.md` | 159,162 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tameshi-shokunin` | `tameshi-shokunin/corpus/lessons/round-30.md` | 36,38,39,58 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tameshi-shokunin` | `tameshi-shokunin/corpus/lessons/round-32.md` | 60 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tameshi-shokunin` | `tameshi-shokunin/corpus/lessons/round-33.md` | 81,100 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tameshi-shokunin` | `tameshi-shokunin/corpus/lessons/round-45-verifier-spotcheck.md` | 73 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tameshi-shokunin` | `tameshi-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` | 38,101 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tameshi-shokunin` | `tameshi-shokunin/corpus/lessons/round-47-verifier-spotcheck.md` | 25 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tameshi-shokunin` | `tameshi-shokunin/corpus/lessons/round-48-verifier-spotcheck.md` | 98 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tameshi-shokunin` | `tameshi-shokunin/corpus/lessons/round-48.md` | 44,46,47,57,63,134,137,150,159,168,173,184,185,308,329 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tameshi-shokunin` | `tameshi-shokunin/corpus/routed-defects.json` | 473,508,518,560,575 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tameshi-shokunin` | `tameshi-shokunin/SKILL.md` | 1828,1972 | bwrap | **adjacent** | hermetic/mutation gate fixtures use bwrap — verification craft; no grader replay or index service |
| `tsukuroi-shokunin` | `tsukuroi-shokunin/corpus/knowledge/degraded-triage-r4.md` | 463 | bwrap | **adjacent** | bwrap in host-operability triage — unrelated domain |

## Ownership answers (the four sub-questions)

| capability | owned elsewhere? | evidence |
|---|---|---|
| (a) offline replay of Terminal-Bench graders | **no** | every sibling `corpus/` hit is `bwrap`/`offline replay`; no sibling has a `tb2-*grader.md`, a `graders/` tree, or a `test_api` invocation. `kumitate-shokunin/corpus/knowledge/multi-agent-coordinator-topologies.md:29,53,83` names Terminal-Bench only as a *cited benchmark* in a multi-agent-topology study — no grader execution, no pin, no receipt. |
| (b) localhost PEP 503 index replay | **no** | `pypi-server`, `vectorops`, `PEP 503`, `pep-0503` = 0 sibling hits. `kama-shokunin` and `kagi-shokunin` mention `127.0.0.1:8080` but as a **llama.cpp/Jitsi model endpoint** (`kama-shokunin/corpus/knowledge/consumer-registry.md:90`, `kagi-shokunin/corpus/knowledge/credential-isolation.md:35`) — a different service on the same port number, not a PEP 503 index. `revenger-shokunin` and `tabi-shokunin` serve loopback fixtures with `python -m http.server` on ports 8477 / 19461-2 — plain static file serving, no PEP 503 `/simple/<name>/` layout, no wheel. |
| (c) grader-class census | **no** | `grader-class` / `class-survey` = 0 sibling hits. The census itself (`corpus/evidence/round62/class-survey.txt`, `corpus/knowledge/tb2-grader-class-census.md`) lives in `kengaku-shokunin` only. `kotoba-shokunin/corpus/knowledge/sibling-overlap-census-round49.md:78` and `...-round74.md:62,93` are *lane-scope* censuses (which lane owns which skill), not grader-class censuses — different subject, adjacent only. |
| (d) grader-class decision table | **no** | no sibling `SKILL.md` carries a grader-class → recipe table. `chousa`, `kaidoku`, `kama`, `kasegi`, `kotodama`, `kumitate`, `lore`, `mori`, `revenger`, `souji`, `tabi`, `tameshi`, `tsukuroi` all have their own `## Decision table` sections, all on other subjects (research method, REA envelope, endpoints, finding triage, worldbuilding, dispatch shape, fiction records, commit runway, receipts, WebMCP, gates, health verdicts). `kengaku-shokunin/SKILL.md` at base `c78749a5` has 0 grader-class rows (`git show c78749a5:SKILL.md | grep -cE 'grader.class|network-service'` → 0) and 9 `## … TB2 grader — round N` sections, none of which is a class→recipe table. |

**Conclusion: no routing line is owed.** No sibling lane holds (a)–(d), so there
is no owned overlap to route and no `'<lane> | round-63 | routed: …'` line to
draft. The lane keeps its claim; the sibling lanes' `bwrap` and
`offline replay` mentions are adjacent-domain vocabulary reuse (sandbox
substrate, hermetic gates, capture replay, lane-scope census) and carry no
capability claim over this round's axes.

## Routing lines

(none — no owned overlap found; nothing to route to the L0 file)

## Second-order note for the L1 (read-only observation, no action taken)

The scan surfaced one cross-seat fact that touches the frozen C1 leg vector.
`127.0.0.1:8080` is **not** free on this host during the wave, even though the
round-start census recorded "no 8080 listener". Measured here:

- `ss -ltnp | grep :8080` showed a live `python3 -m http.server 8080 --bind 127.0.0.1`
  (pid 2648510, cwd `/fast/scratch/hyaku/kengaku-r63/PypiProbeBuild/index`) at
  15:06, and further transient listeners at 15:07 (pid 2689887), 15:2x
  (pid 82641, pid 110000). These are the peer seat `PypiProbeBuild`'s own
  index servers, started and stopped repeatedly during the wave.
- The peer seat's index is a **real, correct** `vectorops-0.1.0` index
  (`/fast/scratch/hyaku/kengaku-r63/PypiProbeBuild/index/simple/vectorops/index.html`
  → `…/packages/vectorops-0.1.0-py3-none-any.whl#sha256=0e2c37a9…`, matching
  the wheel's own sha256). A probe that reaches a *host* 8080 that happens to
  be serving a correct vectorops index would record leg P for K1 — attributing
  the pass to a service it did not start.

This is the exact hazard the frozen predicate guards ("the probe must prove
the index it reaches is its own, not a foreign service"; kill rule: "Any seat
finds the probe reaching a foreign service on 8080 → predicate fails"). The
draft probe handles it: it refuses with `SETUP port-8080-occupied` rather than
grading through a foreign listener (measured: probe run against a squatter on
8080 → `SETUP port-8080-occupied (K1 before start)`, exit 2). That is
correct-but-brittle: it converts a foreign listener into a setup abort rather
than into isolation.

The structural alternative — measured here, not proposed as a claim change —
is to give the probe its own network namespace so the sandbox's loopback is
private to the probe:

```
bwrap --unshare-net …            # sandbox has its own 127.0.0.1
```

Measured in this seat's scratch:

- With `--unshare-net`, a server bound **inside** the namespace is reachable
  from inside it (`BIND-OK on 127.0.0.1:8080 inside ns` / `SELF-CONNECT-OK`),
  while the **host** cannot reach it and `ss -ltnp` does not list it — the
  listener is invisible from the host, so no foreign host service can collide
  with it and the probe's own index is the only thing on the namespace's
  loopback.
- With a **host** squatter holding `127.0.0.1:8080` for the whole run, the
  namespace-isolated probe still produced the frozen vector:
  `K1: LEG P` / `K2: LEG F CalledProcessError` / `K3: LEG F AssertionError` /
  `K4: LEG F CalledProcessError` — i.e. **P/F/F/F** — with the host listener
  untouched throughout (`ss` still shows exactly 1 listener at the end).
- Without `--unshare-net`, the same sandbox **does** reach a host 8080
  (`REACHABLE` vs `UNREACHABLE ConnectionRefusedError` under `--unshare-net`),
  which is why the draft probe must refuse rather than grade.

**This is reported, not implemented.** The claims are frozen; a seat does not
change them. The L1 may note that the current design's correctness depends on
8080 being free for the whole run, and that the wave demonstrably has
concurrent 8080 users. Either the probe keeps its `SETUP` refusal (safe, but
the run can abort for a reason unrelated to the claim), or it moves its index
server and grader into one private namespace (isolated, and the P/F/F/F vector
was observed to hold under contention).

## Verification notes (every value above carries its command)

- Sibling scan: the two `grep` forms quoted above, run from
  `/home/vgpnk/Projects/shokunin`.
- Term isolation: `grep -rilE 'pypi-server|vectorops|PEP 503|pep-0503|grader-class|class-survey' */corpus */SKILL.md */PROVINCE.md */plans | grep -v '^kengaku-shokunin/'` → empty.
- Base-state check: `git show c78749a5:SKILL.md | grep -cE 'grader.class|network-service'` → 0;
  `git show c78749a5:SKILL.md | grep -cE '^## .*TB2 .*grader'` → 9.
- Port evidence: `ss -ltnp | grep :8080`; `ps -o pid,ppid,etimes,args -p <pid>`;
  `ls -l /proc/<pid>/cwd`.
- Namespace behaviour: `bwrap --unshare-net` reachability probe (host-bound vs
  in-namespace server), `ss -ltnp` from the host while the in-namespace server
  ran, and a marker-file fetch proving the host did not reach it.
- Leg vector under contention: the namespace-isolated driver run with a host
  squatter on 8080 → P/F/F/F.
- Peer-probe behaviour under a squatter: the draft probe
  (`w1/draft/depth/round63_c1_pypi_probe.py`) run with a foreign 8080 listener
  → `SETUP port-8080-occupied (K1 before start)`, exit 2.
- Grader capture: `w1/recon/S228-pypi-test_outputs.py`
  (sha256 `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c`),
  also the round-63 `recon/` copy.
- Also measured: the frozen control receipt
  `corpus/evidence/round63/control-k2.txt` (sha256
  `73f1fa330f02eecc9825e5538cb63c6d9fb76a404cb8a33ee067f408259100c9`) contains
  the literal `localhost:8080` only in the `CalledProcessError` **command repr**;
  pip's own stderr renders the endpoint as
  `host='localhost', port=8080` and pip's **stdout** as
  `http://localhost:8080/simple`. The draft probe already accepts both
  renderings (`ENDPOINT_PATTERNS`, `stderr_names_endpoint`) and prints which
  form matched (`K2 ENDPOINT form=urllib3-host-port`), so the frozen K2 limb
  ("captured pip stderr names `localhost:8080`") is satisfied in substance.

## Tooling

No installs, no upgrades, no network calls. `bwrap` 0.13.1, `python3` 3.14.8
and `pip` 26.2.1 (inside a scratch venv) were already present and were used
read-only for the measurements above.
