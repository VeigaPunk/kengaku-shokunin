# ConnectorOverlap — kengaku round 67, wave 1 (connector seat)

Read-only sibling-overlap scan for the torch-pipeline and torch-tensor grader work.
Lane L = `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Seat dir W/ConnectorOverlap.
Nothing outside this seat dir and the report trailer was written. No git mutation, no
sibling lane edit, no network, no install. Scratch `/fast/scratch/hyaku/kengaku-r67/ConnectorOverlap`
held only the 40-path list below and is removed before yield.

## 0. Scope

Sibling lanes: the 20 `*-shokunin` directories other than kengaku that carry a PROVINCE.md or
SKILL.md. Files scanned (40, the explicit list; command `ls`-free loop, exit 0):

```
audio-shokunin/PROVINCE.md  chousa-shokunin/{PROVINCE,SKILL}.md  game-dev-2d-shokunin/PROVINCE.md
game-dev-3d-shokunin/{PROVINCE,SKILL}.md  kagi-shokunin/{PROVINCE,SKILL}.md
kaidoku-shokunin/{PROVINCE,SKILL}.md  kake-shokunin/{PROVINCE,SKILL}.md
kama-shokunin/{PROVINCE,SKILL}.md  kasegi-shokunin/{PROVINCE,SKILL}.md
kotoba-shokunin/{PROVINCE,SKILL}.md  kotodama-shokunin/{PROVINCE,SKILL}.md
kumitate-shokunin/{PROVINCE,SKILL}.md  lore-shokunin/{PROVINCE,SKILL}.md
mado-shokunin/{PROVINCE,SKILL}.md  mori-shokunin/{PROVINCE,SKILL}.md
revenger-shokunin/{PROVINCE,SKILL}.md  souji-shokunin/{PROVINCE,SKILL}.md
tabi-shokunin/{PROVINCE,SKILL}.md  tameshi-shokunin/{PROVINCE,SKILL}.md
tsukuroi-shokunin/{PROVINCE,SKILL}.md
```

Not present in the list: `audio-shokunin/SKILL.md`, `game-dev-2d-shokunin/SKILL.md` (absent on disk).
Plus wide scans of sibling `corpus/` and `plans/` trees for the grader names (section 3).

## 1. Term hits in sibling PROVINCE.md and SKILL.md (count, command output)

Command: `for t in torch pipeline tensor 'Terminal-Bench' 'process-environment' gloo; do grep -c -i -e "$t" <each sibling PROVINCE/SKILL>; sum; done`

| term | sibling hits | kengaku own hits (same method) | reading |
|---|---|---|---|
| torch | 0 | 0 | no sibling names torch |
| gloo | 0 | 0 | no sibling names the gloo rendezvous |
| Terminal-Bench | 0 | 51 | no sibling names TB2 in a lane doc |
| process-environment | 0 | 4 | no sibling names the class |
| tensor | 1 | 0 | `kama-shokunin/SKILL.md:688` ("never loads tensors"), term-only, see O4 |
| pipeline | 30 | 5 | generic uses (typed pipelines, speedrun pipeline, CI, pipefail); none names the torch grader |

Ownership statements that name kengaku as owner (not overlaps; listed so the routing is visible):
`game-dev-3d-shokunin/PROVINCE.md:69,77` (LLM/model research and evaluation belong to kengaku);
`chousa-shokunin/SKILL.md:61`, `chousa-shokunin/PROVINCE.md:11` (model-quality claims → kengaku);
`kama-shokunin/PROVINCE.md:42`, `kama-shokunin/SKILL.md:27` (model quality/eval → kengaku);
`kasegi-shokunin/PROVINCE.md:50` (`kengaku — LLM evaluation and benchmarks`);
`mado-shokunin/PROVINCE.md:15` (model quality → kengaku);
`kotoba-shokunin/PROVINCE.md:68`, `kotoba-shokunin/SKILL.md:13` (kengaku owns measured capability effects of prompt format).

## 2. Class-survey row (question 2)

`corpus/evidence/round62/class-survey.txt:14`:
`CLASS process-environment count=3 members=install-windows-3.11,torch-pipeline-parallelism,torch-tensor-parallelism`

Answer: no sibling lane claims the torch-pipeline grader or the torch-tensor grader. Both are kengaku-owned:
- torch-tensor-parallelism: kengaku R66-C1 (receipt `corpus/evidence/round66/tensor/receipt.txt`; commit `e02c2d90`; source row `corpus/SOURCES.md:198`, S183).
- torch-pipeline-parallelism: kengaku R67-C1 (this round; frozen in `plans/round-67-claims.md`; source rows `corpus/SOURCES.md:253-254`, S238/S239).
- install-windows-3.11 (third member): no sibling PROVINCE/SKILL names it (`grep -i -e 'install-windows|Windows 3\.11'` over sibling PROVINCE/SKILL/corpus/plans → no matches). Kengaku's own row is `SKILL.md:81`.

## 3. Wide scan for grader names in sibling corpus and plans

Command: `grep -rIl -E 'torch-pipeline-parallelism|torch-tensor-parallelism|offline-torch|pipeline-parallel|tensor-parallel' <sibling-dir>` over every sibling directory (whole tree, exit 0):

- `kama-shokunin/` — at least 20 files (the listing was cut by `head -20`, so the exact count is not measured), all under `.ufo/waves/round-20 … round-43` (html fetches, vLLM preload and release JSON, source captures, seat logs). The matches are vLLM `--tensor-parallel-size` CLI flags and vLLM serving text. See O3.
- `souji-shokunin/.ufo/waves/round-43/w1/R43connectorA.md` and `souji-shokunin/census/round-43/waves/w1/R43connectorA.md` — quote kengaku's own `corpus/lessons/round-52.md:56`. See O5.
- `kasegi-shokunin/`, `kumitate-shokunin/`, others: no matches for the grader names.

Word-boundary `torch` over sibling `corpus/` and `plans/` (first five per lane): hits are incidental
(`kaidoku` ELF envelope base64 JSON, `kasegi` source snapshot prose, `kotodama` mythology "torch",
`tabi` Blink source paths). None concerns the grader.

Terminal-Bench in sibling `corpus/` and `plans/`: `kumitate-shokunin/corpus/knowledge/multi-agent-coordinator-topologies.md:29,53-56,82-86` and `kumitate-shokunin/corpus/lessons/round-63.md:12-13`. See O1.

## 4. Overlap table and routing

Each row: owner of the surface, does kengaku's frozen claim touch it, routed or absorbed.
"Frozen claim" means R67-C1 (torch-pipeline grader offline) and R67-C2 (round-65 sqlite strict gate).

| id | path:line | term | owner of surface | frozen claim touches? | routing |
|---|---|---|---|---|---|
| O1 | `kumitate-shokunin/corpus/knowledge/multi-agent-coordinator-topologies.md:29,53-56,82-86`; `kumitate-shokunin/corpus/lessons/round-63.md:12-13` | Terminal-Bench (aggregate results of a third-party topology study, arXiv 2512.08296, S196/S197) | kumitate (coordinator topology decisions); the TB2 numbers are a cited study's, not a grader | No. R67-C1 executes one grader offline; it scores no TB2 task, no topology | Not routed. Not absorbed: kengaku takes no topology decision and does not re-score the study. kengaku `PROVINCE.md` already names these two files as "coordinator-topology data citations" |
| O2 | `kumitate-shokunin/PROVINCE.md:24` | "adjacent, not absorbed: kengaku evaluates agents, this lane arranges the seats" | kumitate (topology decisions); kengaku (agent evaluation) | No | Not routed. Boundary already stated on both sides; no edit |
| O3 | `kama-shokunin/.ufo/waves/round-43/c3/vllm-v0.31.0-preload.py:10,14` (and `round-43/w1/out/W1C01/preload.py`, `release.json`) | `--tensor-parallel-size` (vLLM serving CLI, not torch.distributed) | kama (serving-plane identity; `kama-shokunin/SKILL.md:1121-1127` records the serving plane as kama's claim) | No. The R67-C1 grader is torch.distributed gloo on a host port, not vLLM serving | Not routed. Term-only collision with the word "tensor-parallel" |
| O4 | `kama-shokunin/SKILL.md:688` | `tensor` ("never loads tensors") | kama | No | Not routed. Term-only |
| O5 | `souji-shokunin/.ufo/waves/round-43/w1/R43connectorA.md:459` (and `souji-shokunin/census/round-43/waves/w1/R43connectorA.md`) | quotes kengaku's `corpus/lessons/round-52.md:56` (torch-tensor-parallelism V1 row) | kengaku (the quoted lesson and grader are kengaku's; R66-C1 owns the torch-tensor grader) | Touches kengaku's own ground only by quotation. The quote is a citation; R67-C1 changes no sibling file | Not routed. The quote stays in souji's wave record; no edit in L |

Count: **5 overlap rows** (O1–O5), at term or quotation level. **0** claim the torch-pipeline grader or the torch-tensor grader. **0** rows require routing to a sibling lane. O1 and O2 are boundary citations already stated by both lanes; O3 and O4 are term-only collisions; O5 quotes kengaku's own lesson. **No overlap changes the frozen R67-C1 or R67-C2 claim text.**

## 5. Sibling ownership statements (for the record; not overlaps)

Section 1 lists them. Every one names kengaku as the owner of LLM or model evaluation, which is the ground R67-C1 and R67-C2 sit on. None claims a grader or an offline replay.

## 6. Reproduction notes

- The grep tool, given a glob path form (`*-shokunin/PROVINCE.md`, `*/PROVINCE.md`), returned `No matches found` for patterns that do occur in those files (e.g. `kama` `tensor`, `kengaku`). The 40-file explicit list gave the expected hits. The counts in section 1 come from shell `grep -c` over the explicit list, not from the glob form. Reported to xd://report_issue.
- Scratch 40-path list: `/fast/scratch/hyaku/kengaku-r67/ConnectorOverlap/p.list` (removed before yield; the list is reproduced in section 0).
- No install (tooling-only rule: install nothing unless the item names it).
