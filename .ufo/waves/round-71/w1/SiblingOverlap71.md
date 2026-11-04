# SiblingOverlap71 — sibling-lane overlap scan for the round-71 w1 surface

Seat: SiblingOverlap71 (connector; leaf — no subagent dispatch, no network, no VCS mutation,
no tool installs). Read the frozen claims in full first:
`plans/round-71-claims.md` (both claims, frozen case table, kill rules).

Snapshot: 2026-11-03T22:22–22:30 -03:00. Lane tip observed
`d8a77d3f2b4c8747dbc3a5bcf458b23160a459e0` (`git -C kengaku-shokunin rev-parse master`, rc 0);
claims' freeze base `1cb49cac52999475de35f8955d5c01f2ddb66ccf`.

Surface scanned: the R71-C1 `hf-model-inference` Terminal-Bench 2.0 grader offline-replay surface,
under the nine assigned terms — `hf-model-inference`, `transformers`,
`AutoModelForSequenceClassification`, `torch`, `flask`, `model_cache`, `sentiment`,
`0.0.0.0:5000`, `distilbert` — plus the ownership question ("model serving" / "HF model load",
kama and kagi named).

`sweep coverage: 21 lane repos (20 siblings + kengaku for framing); assigned-scope corpus
1,531 files / 29,687,120 bytes; full-tree confirmation over every sibling repo, .git excluded;
no sibling file was written; kengaku itself excluded from every "sibling" count.`

---

## 1. What I ran

| # | command (read-only) | rc | result |
|---|---|---|---|
| 1 | `read L/plans/round-71-claims.md` | 0 | both claims, eight-case table, four legs, predicates, kill rules read before any scan |
| 2 | `git -C kengaku-shokunin rev-parse master` | 0 | `d8a77d3f…` (working tree carries L1 round-71 evidence untracked) |
| 3 | Python `os.walk` census (no ignore rules) over `*-shokunin/{SKILL.md,PROVINCE.md,corpus/knowledge/**}` — case-insensitive literal counts of all nine terms, occurrence-level and line-level | 0 | 21 lanes, 1,531 files, 29.7 MB; `S/scan.json` (`S=/fast/scratch/hyaku/kengaku-r71/SiblingOverlap71`) |
| 4 | per-lane `rg -i -l -F --no-ignore --glob '!.git/**'` for the four exact tokens `hf-model-inference`, `distilbert`, `AutoModelForSequenceClassification`, `0.0.0.0:5000` over every sibling repo | 0 | **0 sibling files** (`SWEEP-DONE`, no matching path printed) |
| 5 | same full-tree sweep for HF-load tokens `from_pretrained`, `AutoModel`, `from transformers import`, `import torch` | 0 | **0 sibling files** |
| 6 | same full-tree sweep for `transformers`, `torch`, `flask`, `sentiment`, `model_cache`, and `huggingface`, file counts per lane | 0 | counts in §3.3; `model_cache` = 0 in every sibling; huggingface mentions only chousa 8 / kama 24 / revenger 1 / souji 2 |
| 7 | `rg -n -e ':5000\b' *-shokunin/{PROVINCE.md,SKILL.md} *-shokunin/corpus/knowledge` | **1** | **0 lines** — no sibling declares or records port 5000 |
| 8 | phrase sweep over every sibling `PROVINCE.md`/`SKILL.md` for `model serv|hugging|hf model|model load|model infer|inference serv|ml model|machine learning|pytorch|llm|vllm|triton|diffusion|comfyui|embedding` | 0 | matches only in kama (domain + GGUF artifact URLs), kumitate/tsukuroi/mori (route serving→kama), game-dev-3d/kasegi/chousa (route eval→kengaku), plus incidental `LLM`/`embedding` uses in kaidoku/kotoba/revenger/tameshi/mado (§4) |
| 9 | full read of `kama-shokunin/PROVINCE.md`, `kagi-shokunin/PROVINCE.md`; targeted reads of kumitate/tsukuroi/mori/chousa/game-dev-3d/kasegi/kengaku boundary lines | 0 | quotes in §4 |
| 10 | `rg -n -i 'kengaku' kama-shokunin/.ufo/waves/round-31/w1/out/ConnSibling/overlap.md` | **1** | the artifact kama cites for "kengaku excludes the model-serving plane" contains no kengaku line (§6) |

No battery, no port bind, no install, no `git`/`jj` mutation. Scratch is `S`; the report is the
only file written under `L`.

---

## 2. Hit table — assigned scope (knowledge + SKILL.md + PROVINCE.md; occurrence counts)

Term order: T1 `hf-model-inference`, T2 `transformers`, T3 `AutoModelForSequenceClassification`,
T4 `torch`, T5 `flask`, T6 `model_cache`, T7 `sentiment`, T8 `0.0.0.0:5000`, T9 `distilbert`.

| lane | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 | T9 | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **kengaku-shokunin** (incumbent; not a sibling) | 3 | 7 | 0 | 52 | 1 | 0 | 0 | 0 | 0 | **63** |
| kotodama-shokunin | 0 | 1 | 0 | 3 | 3 | 0 | 6 | 0 | 0 | **13** |
| audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kasegi, kotoba, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi (19 lanes) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| **sibling total (20 lanes)** | **0** | **1** | **0** | **3** | **3** | **0** | **6** | **0** | **0** | **13** |

File-level detail for the two non-zero lanes:

- kengaku 63 occurrences / 8 files: `SKILL.md` (torch ×5); `corpus/knowledge/tb2-torch-pipeline-parallel-offline.md`
  (transformers ×6, torch ×22); `tb2-torch-tensor-parallel-offline.md` (transformers ×1, torch ×17);
  `tb2-grader-vacuity-triage.md` (hf-model-inference ×1, torch ×6); `tb2-grader-class-census.md`
  (torch ×2); `tb2-kv-store-grpc-offline.md` (hf-model-inference ×1);
  `tb2-network-service-offline-grader.md` (hf-model-inference ×1); `llm-judge-calibration.md` (flask ×1).
- kotodama 13 occurrences / 12 files: `civilizations/{aegean-minoan-mycenaean,etruria,japan-edo,pacific-northwest,scythian-saka}.md`,
  `culture-material/{scent-perfume-aromatics-codes,vessel-container-lexicon}.md`,
  `linguistics/kinship-terminology.md`, `myth-symbol/{creation-myths-taxonomy,death-afterlife-eschatology,hero-journey-variants,plant-symbolism}.md`.

**Surface anchor (why this is kengaku's object).** The class row is kengaku-only:
`SKILL.md:78` `| network-service | 8 | executed 3 of 8 (…` at the freeze base `1cb49cac` and at
committed `master` `d8a77d3f`; the working tree (L1 in flight, not verified by this seat) carries
`executed 4 of 8`. `network-service` matches only kengaku files
(`PROVINCE.md`, `SKILL.md`, four `tb2-*` knowledge entries); zero sibling files.

---

## 3. Classification — term-level vs surface-level

### 3.1 Sibling hits: 13/13 term-level, 0 surface-level

| lane | term | path:line | quoted fragment | class |
|---|---|---|---|---|
| kotodama | torch | `corpus/knowledge/myth-symbol/hero-journey-variants.md:51` | "mother Hecabe dreams of a burning torch" | term-level — myth/art object |
| kotodama | torch | `corpus/knowledge/civilizations/aegean-minoan-mycenaean.md:163` | "not generic torchlight" | term-level — lighting |
| kotodama | torch | `corpus/knowledge/civilizations/etruria.md:65` | "Vanth's winged/torch-bearing imagery" | term-level — funerary iconography |
| kotodama | flask | `corpus/knowledge/culture-material/scent-perfume-aromatics-codes.md:15` | "used as \"a flask for perfume or perfumed oils\"" | term-level — vessel |
| kotodama | flask | `corpus/knowledge/civilizations/scythian-saka.md:90` | "some implements \"sword\" and \"flask\"" | term-level — Herodotus translation |
| kotodama | flask | `corpus/knowledge/culture-material/vessel-container-lexicon.md:4` | "cosmetic containers — kohl pots, oil flasks" | term-level — pottery lexicon |
| kotodama | sentiment | `corpus/knowledge/linguistics/kinship-terminology.md:10` | "Structure and Sentiment, U Chicago Press" | term-level — book title |
| kotodama | sentiment | `corpus/knowledge/linguistics/kinship-terminology.md:115` | "binding obligations between families, not just sentiment" | term-level — humanistic sense |
| kotodama | sentiment | `corpus/knowledge/myth-symbol/creation-myths-taxonomy.md:65` | "ancestors as structural powers, not sentiment" | term-level |
| kotodama | sentiment | `corpus/knowledge/myth-symbol/death-afterlife-eschatology.md:42` | "mummification as doctrine, not sentiment" | term-level |
| kotodama | sentiment | `corpus/knowledge/myth-symbol/plant-symbolism.md:97` | "their meaning rides on offices, not feelings — steal the institution, not the sentiment" | term-level |
| kotodama | sentiment | `corpus/knowledge/civilizations/japan-edo.md:114` | "sentimental fiction" | term-level — literary register |
| kotodama | transformers | `corpus/knowledge/civilizations/pacific-northwest.md:22` | "*Since the Time of the Transformers: The Ancient Herit…*" (McMillan title) | term-level — ethnography title |

**0/13 sibling hits is surface-level.** No sibling hit names the TB2 task, a grader, a Hugging Face
model load, `model_cache`, `0.0.0.0:5000`, or `distilbert`. The nearest-looking collision (kasegi's
Flask advisory, §3.3) is a different object.

### 3.2 Kengaku hits: 63/63 surface-level (incumbent)

All 63 are the lane's own eval/TB2 record: three `hf-model-inference` census mentions
(`tb2-grader-vacuity-triage.md:97` names `hf-model-inference::test_model_downloaded`;
`tb2-kv-store-grpc-offline.md:34` and `tb2-network-service-offline-grader.md:31` list it in the
frozen `network-service` membership), the two `torch-*-parallelism` replay entries (which own the
`process-environment` class row, `SKILL.md:81`), and the class census. Caveat for calibration:
the one `flask` hit in scope is **not** the web framework — `llm-judge-calibration.md:91` reads
"**FLASK 40.53–48.58%**", the FLASK NLP benchmark. The TB2 task's Flask app appears only in
`corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py` (`requests.get("http://0.0.0.0:5000")`,
`:29-31`) and `corpus/evidence/round71/hf/instruction.md` (`/app/model_cache/sentiment_model`,
distilbert download), i.e. in evidence, outside the knowledge layer.

### 3.3 Full-tree confirmation (all sibling repos, `.git` excluded) — still no surface-level hit

| term | sibling lanes / files | what the hits are | class |
|---|---|---|---|
| `hf-model-inference`, `AutoModelForSequenceClassification`, `model_cache`, `0.0.0.0:5000`, `distilbert` | **0 / 0** | — | — |
| `from_pretrained`, `AutoModel`, `from transformers import`, `import torch` | **0 / 0** | — | no lane claims HF model loading |
| `transformers` | chousa 6, kotodama 3 | chousa: research-paper captures ("relying on the huggingface implementation", "Huggingface's transformers: …"); kotodama: titles/word collisions | term-level citation |
| `torch` | audio 1, chousa 3, kaidoku 19, kasegi 2, kotodama 8, souji 1, tabi 12, tsukuroi 2 | kaidoku: JSON evidence envelopes (substring in base64/hex payloads); tabi: minified Playwright/Chromium sources (`toSelectorChannel` → substring `torch`); kasegi: "Cisco Torch" attack tool + a `pytorch-model-recovery` rule-label citation; others: package/path/word noise | term-level / substring noise |
| `flask` | chousa 1, kasegi 1, kotodama 12 | chousa: web capture markup; kasegi `corpus/source-snapshots/round-40/S025.txt:1410`: "hardcoded 'SECRET_KEY' in the flask configuration, allowing attackers to forge a session" — the Python framework, inside a security advisory the lane captured as source material; kotodama: pottery/perfume | term-level (kasegi is the only framework-sense hit; object is a CVE advisory, not grader replay) |
| `sentiment` | kotodama 11 | humanities prose/book titles | term-level |
| `huggingface` | chousa 8, kama 24, revenger 1, souji 2 | chousa: paper/HTML captures with `huggingface.co` dataset/model links; kama: pinned GGUF artifact download URLs and replay-tool source; revenger: a source snapshot ("published on HuggingFace"); souji: log/listing receipts | term-level citation / artifact URL |

For scale, the same full-tree pass puts the surface squarely in kengaku: files per term
T1–T9 = **20 / 22 / 2 / 107 / 48 / 23 / 56 / 13 / 4**, against sibling totals
**0 / 9 / 0 / 48 / 14 / 0 / 11 / 0 / 0** — and the inspected files in the `torch`/`flask`
columns are the substring/citation noise classified above.

---

## 4. Ownership question — who claims "model serving" / "HF model load"?

**"Model serving": kama claims it, scoped to the local LLM serving plane.** Quoted:

- `kama-shokunin/PROVINCE.md:3` — "**Domain:** local model serving & endpoint health — local LLM
  endpoints, baseURL drift, served-model reconciliation, probe conventions."
- `kama-shokunin/SKILL.md:3` — "description: Domain specialist — local model serving & endpoint
  health — scopes local LLM endpoints, baseURL drift, model-id reconciliation."
- `kama-shokunin/PROVINCE.md:10` — owns "producer discovery & read-only service inspection of local
  serving ports | `tools/kama-probe.sh listeners` (`ss -ltn` loopback enumeration + per-listener
  classification)".
- Boundary and refusal, `kama-shokunin/PROVINCE.md:42-45` — "**Refuses:** model quality/eval
  (kengaku), credential material & auth flows (kagi), dispatch/route mechanism (kumitate), remote
  web surfaces (kake). Boundary rule: kama answers *'is the thing at this baseURL the model this
  config believes it is, right now'* — never *'is the model good'* or *'is the request safe'*."
- same file `:142-144` — "Sibling lanes hold no competing claim on this surface: … and kengaku
  excludes the model-serving plane (`.ufo/waves/round-31/w1/out/ConnSibling/overlap.md`)."

**"HF model load": no lane claims it.** Full-tree zero for `from_pretrained`,
`AutoModelForSequenceClassification`, `from transformers import`, `import torch` in all 20 sibling
repos. kama's 24 huggingface files are GGUF artifact URLs, the `huggingface_hub` download guide, or
the fixture cache path (`corpus/SOURCES.md:243-246`, `SKILL.md:1513`), feeding
`kama-llamacpp-live.py` a pinned **GGUF** (llama.cpp load), not a `transformers` `from_pretrained`
load. `distilbert` appears in no sibling file.

**kagi: no serving claim.** `kagi-shokunin/PROVINCE.md:3` — "**Domain:** secrets & vault ops — the-janitor
flows, credential hygiene evidence"; "**Refuses:** anything outside this domain". Its only
model-adjacent line is a historical substrate row, `:63` — "configured model endpoint
`127.0.0.1:8080` (dead: Jitsi) vs live llama-server on `34113`" — presence inventory, not serving
ownership; kama routes auth handling to kagi (`kama-shokunin/SKILL.md:133` "Escalate auth handling
to kagi").

**The fleet routes the two planes consistently:**

| lane | quote | direction |
|---|---|---|
| kumitate | `PROVINCE.md:31` "Local model serving and endpoints → kama. Prompt and skill craft → kotoba. Research method → chousa." | serving → kama |
| tsukuroi | `PROVINCE.md:25` "**Refuses:** endpoint/model serving health (→ kama), secrets (→ kagi)" | serving → kama |
| mori | `PROVINCE.md:67` "kama \| Owns local model-serving and endpoint health; mori does not infer serving health from host/resource signals." | serving → kama |
| game-dev-3d | `PROVINCE.md:77` "LLM/model research and evaluation belong to `kengaku-shokunin`" | eval → kengaku |
| kasegi | `PROVINCE.md:50` "kengaku — LLM evaluation and benchmarks" | eval → kengaku |
| chousa | `PROVINCE.md:10-12` "**Refuses:** … model-quality or evaluation claims (→ kengaku)" | eval → kengaku |

**kengaku's own boundary is declared on both sides of the line:**

- `kengaku-shokunin/PROVINCE.md:25-26` — "**Not owned:** the model-serving plane (llama-server
  flags, slot/batch config) — no lane owns it; escalate to the integrator instead of remediating."
  (flag/config authority stays unowned; see the next line)
- `kengaku-shokunin/PROVINCE.md:137` — "**kama** \| serving plane + endpoint identity … kama is
  rostered and owns serving-plane health/detection and endpoint identity; kengaku keeps
  *interpretation* evidence and never remediates flags … flag-change authority is unowned/integrator".
- `kengaku-shokunin/PROVINCE.md:15` — the served-model surface row is "capability interpretation
  only; flag authority is kama's (serving plane)".
- `kengaku-shokunin/PROVINCE.md:972-973` — "The gRPC-inside-sandbox pattern does not overlap kama's
  serving plane (`.ufo/waves/round-64/w1/SiblingOverlap/sibling-overlap.md`)."

There is no in-lane contradiction here: :25-26 withholds **flag/config** authority (still
unowned/integrator), while :137 assigns **health/detection and endpoint identity** to kama. Neither
assigns the TB2 grader replay to anyone else.

**Answer to the ownership question.** kama claims the *term* "local model serving" as a domain, but
over local LLM endpoints (llama.cpp/vLLM/SGLang/Ollama), their baseURLs, served-model identity, and
health probes — and it explicitly refuses model quality/eval. No lane claims "HF model load"
(`transformers`/`from_pretrained`). kengaku owns LLM/model research & evaluation, and R71-C1's object
— the `hf-model-inference` TB2 grader replay — is evaluation ground. kama's domain is therefore
adjacent, not contested.

---

## 5. Contested? (one line, as asked)

**No: kengaku's claim to the `hf-model-inference` TB2 grader-replay surface is uncontested** — zero
sibling files carry the task, grader, HF-load, cache, or endpoint tokens; the adjacent
"model serving" term is kama's by declared domain and kengaku's exclusion is declared on both
sides, so the boundary is settled rather than competing.

---

## 6. Routing

**None.** No sibling lane holds or contests this surface; no sibling province needs an edit; no
cross-lane finding is routed from this seat.

Two record-only observations (not routed, no action requested from any sibling; both trace to the
round-64 connector's C-2/C-3, which the L1 already has):

1. **Port plane, carry-over of round-64 C-2.** The round-71 fixture binds `0.0.0.0:5000` (wildcard,
   task-mandated) for the replay's duration; the round-64 fixture bound `127.0.0.1:5328`. kama's
   listener census classifies a wildcard as `scope=wildcard` (`tools/kama-probe.sh:280`) and a
   non-model HTTP answer as `FOREIGN_SERVICE` (`:552,:558`), so a concurrent kama probe could observe
   an unattributed wildcard listener. Not a claim conflict (a benchmark fixture is not a registered
   model endpoint; kama's registry rows are `127.0.0.1:8080` and `:34113` only,
   `registry/endpoint-consumers.tsv:35-37`). The `--port-lock` serialises kengaku seats only, so the
   L1 may want to re-confirm C-2 with the wildcard variant in mind; this seat binds nothing.
2. **kama's citation, correction to round-64 C-3.** `kama-shokunin/PROVINCE.md:143-144` cites
   `.ufo/waves/round-31/w1/out/ConnSibling/overlap.md` for "kengaku excludes the model-serving
   plane". Resolved **kama-relative**, that path exists
   (`kama-shokunin/.ufo/waves/round-31/w1/out/ConnSibling/overlap.md`), so round-64 C-3's "path does
   not exist" is a false positive caused by resolving a kama-relative path in kengaku's tree.
   However, that artifact's scope is nine named lanes and contains no kengaku line
   (`rg -i 'kengaku'` → rc 1), so the citation does not carry the proposition it is attached to;
   the proposition itself is true from `kengaku-shokunin/PROVINCE.md:25-26`. Report-only — the file
   is kama's.

---

## 7. Second-order effects and risks (traced across runtime / contract / substrate / verification)

- **Runtime:** the replay's wildcard listener is the only host-visible artefact of this surface. It
  exists only while a battery holds `--port-lock`; no sibling declares port 5000 as a surface
  (rc 1, 0 lines in PROVINCE/SKILL/knowledge) and the exact `0.0.0.0:5000` string appears in no
  sibling file, so no sibling's gate or consumer is bound by it. Residual risk: kama's read-only listener census
  could record it as an unowned `FOREIGN_SERVICE`/wildcard if a probe runs concurrently — observation
  only, no claim conflict (§6.1).
- **Contract:** the frozen claim already words the candidate as a lane-written stdlib shim standing in
  for the Flask app (limitation i) and prices the grader's logic, not serving capability. That wording
  is what keeps kengaku off kama's domain; a future round must not reword the result as "kengaku
  serves a model", which would be an overclaim against `kama-shokunin/PROVINCE.md:3` and against
  `kengaku-shokunin/PROVINCE.md:25-26`.
- **Substrate:** the surface's literals (`0.0.0.0:5000`, `/app/model_cache/sentiment_model`,
  `distilbert-base-uncased-finetuned-sst-2-english`) live in `corpus/evidence/` (round52 grader
  capture, round71 instruction/sandbox), not in `corpus/knowledge/`: a knowledge-only census sees
  `hf-model-inference` three times and none of the endpoint/cache tokens. That is a knowledge-layer
  limit of any sibling scan, not a gap in this one (full-tree pass closes it) — and it is the
  reason this report does not infer "nobody mentions it" from a knowledge-only grep.
- **Verification:** no sibling instrument re-derives or cites the round-71 receipt path
  (`corpus/evidence/round71/…` is kengaku-only; zero sibling files under the exact tokens). The
  surface's verification chain (predicate, digests, `--check-receipt`) remains lane-local, consistent
  with "no fleet standard" (round-70 §4).

---

## 8. Verification transcript (exercised)

```sh
# scope census (case-insensitive literal, occurrence + line counts, no ignore rules)
# python os.walk over 21 lanes {SKILL.md,PROVINCE.md,corpus/knowledge/**}
# → 1,531 files / 29,687,120 bytes; kengaku 63 (T1 3,T2 7,T4 52,T5 1), kotodama 13
#   (T2 1,T4 3,T5 3,T7 6); all other 19 sibling lanes 0 across nine terms.
#   receipt: /fast/scratch/hyaku/kengaku-r71/SiblingOverlap71/scan.json   [rc 0]

# exact surface tokens over every sibling repo, no ignore, .git excluded
# → hf-model-inference | distilbert | AutoModelForSequenceClassification | 0.0.0.0:5000
#   zero matching files; loop ended SWEEP-DONE.                            [rc 0, 0 hits]

# HF-load tokens over every sibling repo
# → from_pretrained | AutoModel | "from transformers import" | "import torch"
#   zero matching files.                                                    [rc 0, 0 hits]

# port sweep
rg -n -e ':5000\b' *-shokunin/PROVINCE.md *-shokunin/SKILL.md *-shokunin/corpus/knowledge
# → no output; rg rc 1 (zero lines).

# ownership reads (quoted in §4): kama/kagi full PROVINCE; kumitate:31, tsukuroi:25,
# mori:67, game-dev-3d:77, kasegi:50, chousa:10-12, kengaku:15,25-26,137,972-973.
# kama round-31 artifact: rg -i 'kengaku' kama-shokunin/.ufo/waves/round-31/w1/out/ConnSibling/overlap.md
# → rc 1, no match (§6.2).

# surface-anchor state (observed, not verified as a claim)
git -C kengaku-shokunin show 1cb49cac:SKILL.md | rg -n 'executed [0-9] of 8'  # → :78 3 of 8
git -C kengaku-shokunin show d8a77d3f:SKILL.md  | rg -n 'executed [0-9] of 8' # → :78 3 of 8
git -C kengaku-shokunin diff --stat master -- SKILL.md                         # → 1 file, 1+/1- (working tree: 4 of 8)
```

Tooling: none installed or upgraded (no channel used; nothing recorded). No network. No git/jj
mutation. No sibling file edited; all sibling reads were `read`/`rg` on absolute paths.

---

## 9. Verdict

For the item this seat attacks — sibling-lane overlap with round-71's `hf-model-inference` replay
surface — **no sibling lane owns, contests, or even names the surface** (0 files across all four
exact tokens and all four HF-load tokens in 20 sibling repos; 13 assigned-scope sibling hits are
13/13 word collisions in kotodama's humanities corpus; full-tree noise is substring/citation noise),
and the only real adjacency is kama's declared **serving plane**, which kama itself refuses to extend
to model quality/eval and which kengaku explicitly excludes — so the claim is uncontested, nothing
is routed, and no boundary text needs to change on either side.
