# R53SentinelFetch2 — wave-3 security screen of the evidence this round lands

Seat: sentinel (`R53SentinelFetch2`). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scope: (1) credential / injection / privacy screen of every file the wave-2 readers, the wave-3 pricing and touch
seats and the wave-1 source scouts produced; (2) screen of the prior-art archives destined for
`corpus/evidence/round53/fetched/`; (3) re-check of the captured grader bytes under `corpus/evidence/round52/graders/`.
Axes judged: calibration, adjacency. **No lane file was edited** (the only writes are this report and
`.ufo/waves/round-53/w3/R53SentinelFetch2/scan_extended.py`, both inside my own seat directory).

Lane state observed: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD` →
`9ead4476bf55b1ea6490d0204b668195db4a4d1d`; the task text's build-time tip was `b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe`
(one commit earlier — the lane advanced under me, as the task warned). I ran the scans against the working tree at
`9ead4476` (the lane's current HEAD at scan time) and against a clean clone
`git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r53/R53SentinelFetch2/lane`
whose `git rev-parse --show-toplevel` printed `/fast/scratch/hyaku/kengaku-r53/R53SentinelFetch2/lane` and whose HEAD was
also `9ead4476bf55b1ea6490d0204b668195db4a4d1d`.

## Tooling

No tool was installed or upgraded: the lane already ships `plans/stage_scan.py` (the round-53 credential-pattern
scanner, 33-case selftest, `SELFTEST cases=33 failures=0` at `9ead4476`) and the host has `python3`, `curl`, `sha256sum`.
Per the orchestrator ruling of 2026-10-20 no pacman transaction was run. No `pacman`, no `uv tool install`, no
`~/.local/bin` write.

I wrote one new file — `plans/stage_scan.py` does not cover session cookies, signed URLs, JWTs, `Bearer` headers,
`Set-Cookie`, URL-embedded credentials, absolute host paths or prompt-injection shapes, so I added a companion scanner
in my own seat directory:

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53SentinelFetch2/scan_extended.py` (6.1 KiB,
  25 rules in 3 classes: credential / injection / privacy). It never prints a matched secret in full (credential
  matches are masked to the first 8 characters) and it passes its own scan
  (`python3 plans/stage_scan.py .ufo/waves/round-53/w3/R53SentinelFetch2/scan_extended.py` → `SCAN files=1 skipped=0 hits=0`).
  The 1Password-reference rule is assembled from string fragments so the scanner never contains the literal scheme
  prefix — same discipline `stage_scan.py` itself uses.

## Commands run (the whole screen)

```
# clone (read-only), lane identity
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r53/R53SentinelFetch2/lane
git -C /fast/scratch/hyaku/kengaku-r53/R53SentinelFetch2/lane rev-parse --show-toplevel
git -C /fast/scratch/hyaku/kengaku-r53/R53SentinelFetch2/lane rev-parse HEAD
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD

# disk guard
bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
df -h /fast /home

# lane scanner over every screened tree
python3 plans/stage_scan.py .ufo/waves/round-53/w2
python3 plans/stage_scan.py .ufo/waves/round-53/w3
python3 plans/stage_scan.py .ufo/waves/round-53/w1/C1ScoutSrcAudit .ufo/waves/round-53/w1/C1ScoutSrcBench \
    .ufo/waves/round-53/w1/C1ScoutSrcTB2 .ufo/waves/round-53/w1/C1ScoutSrcTesting
python3 plans/stage_scan.py corpus/evidence/round52/graders
python3 plans/stage_scan.py corpus/evidence/round53
python3 plans/stage_scan.py corpus/                      # whole corpus, for the pre-existing baseline

# companion scanner
python3 .ufo/waves/round-53/w3/R53SentinelFetch2/scan_extended.py <tree>...

# archive inventory: SOURCE-URL header, size, inline <script> bytes, session-ish tokens
# archive digests vs the parts that cite them
# names_task() check of each candidate archive against its task (counter's own predicate)
# longest verbatim run of captured grader bytes inside every w2/w3 report
```

## Measured numbers

`stage_scan.py` (the lane's own scanner) over every tree I was asked to screen, at `9ead4476`:

| tree | files | skipped | hits |
|---|---|---|---|
| `.ufo/waves/round-53/w2/` | 19 | 0 | **0** |
| `.ufo/waves/round-53/w3/` | 173 | 4 | **4** (all analysed below) |
| `.ufo/waves/round-53/w1/C1ScoutSrcAudit/` | 9 | 0 | **0** |
| `.ufo/waves/round-53/w1/C1ScoutSrcBench/` | 17 | 0 | **0** |
| `.ufo/waves/round-53/w1/C1ScoutSrcTB2/` | 22 | 0 | **0** |
| `.ufo/waves/round-53/w1/C1ScoutSrcTesting/` | 11 | 4 | **0** |
| `corpus/evidence/round52/graders/` (all 185 files) | 185 | 0 | **0** |
| `corpus/evidence/round53/` (landed: 3 files) | 3 | 0 | **0** |

Companion scanner over `.ufo/waves/round-53/w3/`: 169 files, 419 hits → 24 credential, 4 injection, 391 privacy
(each privacy hit is a path string; the substantive ones are tabulated below).

Baseline for calibration: `python3 plans/stage_scan.py corpus/` reports **55 hits in files that already landed in
earlier rounds** — 54 are a JSON key named `token` whose value is a human sentence, inside
`corpus/evidence/round27-calibration/*` and `corpus/evidence/round28-calibration/*` (e.g.
`corpus/evidence/round27-calibration/state-base-final-json.json:4052`, whose value is a markdown decision-table
heading), and 1 is the literal one-password-reference scheme prefix inside
`corpus/lessons/round-9-aggregator-corpus-verdict.md:20`. Those are prose, not secrets; they are the lane's accepted
pre-existing state and are **not** this round's finding. (I quote the shape, never the matched bytes, throughout this
report — a report that reproduces a credential-shaped literal is itself a stage-scan hit.)

## Findings — file:line, class, and whether it must block landing

### F1 — `credential` (HIGH, must block landing of the archive as-is)
`.ufo/waves/round-53/w3/C1PriceScoutE/fetched/tb2audit-substack.html:557` and `:581`

- `:557` — a JS assignment `clientToken: '<35 hex chars>'` (a third-party Substack publish-side client token; the
  value is deliberately not reproduced here).
- `:581` — a Cloudflare beacon script attribute carrying a JSON key `token` whose value is 32 hex chars (also not
  reproduced).

Both are **public page bytes**, not the lane's secrets and not live credentials of this project (a client token embedded
in a public blog page for analytics). But they are credential-shaped strings inside a third-party archive, they are
exactly what `stage_scan.py`'s `generic` rule is built to catch, and the lane has a recorded history of being blocked
by GitHub push protection (GH013) on a credential-shaped string inside a captured upstream file — the reason
`plans/stage_scan.py` and the `sanitize-git-repo` exclusion exist (`corpus/evidence/round52/graders/EXCLUDED.md`).
`python3 plans/stage_scan.py .ufo/waves/round-53/w3/C1PriceScoutE/fetched/tb2audit-substack.html` → `HIT …:557 generic`
`HIT …:581 generic`, exit **1**.

**Must block landing** of that archive as a byte-for-byte capture, unless the L1 either (a) does not land this archive
(the seat's row does not need it — the substack page is a pointer to the audit repo, whose files are also archived), or
(b) lands it with the two token values redacted and records the redaction plus the pre-redaction sha256 in the row.
Option (a) is smaller and loses nothing: `tb2audit-readme.md`, `tb2audit-human-notes.txt`, `tb2audit-20260120-audit.txt`,
`tb2audit-ratings.json`, `tb2audit-stats.json` and `tb2audit-terminalbench.md` are all in the same seat directory, all
carry a `SOURCE-URL:` header, and all scan clean. Smallest remediation: exclude `tb2audit-substack.html` from the
landing set, or redact the two values; either way do not stage it silently.

### F2 — `credential` (LOW, must block the *file*, not the round)
`.ufo/waves/round-53/w3/C1ScoutLitSrc/fetched/harbor-verifier.md:98`

An environment-variable assignment whose *key* names a vendor API-key variable and whose *value* is the shell-style
placeholder `${…ANTHROPIC_API_KEY…}` — a **placeholder** in the upstream Harbor docs (a TOML snippet showing how a task's
verifier would pass the key through from the environment). No key value is present. `stage_scan.py` fires
(`HIT …:98 generic prefix=API_`, exit 1). This is a false positive of the `generic` rule on documentation prose.
**Must not block the round**, but the file must not be staged without either a documented waiver or a redaction, because
the lane's own pre-stage gate would exit 1 on it and the same GH013-shaped push protection applies. The sibling files in
that directory (`harbor-lint.md`, `harbor-separate-verifier.md`, `harbor-reward-hacking.md`) scan clean — the row can
cite one of them instead if the API-key placeholder snippet is not load-bearing.

### F3 — `credential` (NONE — false positives; must not block)
- `.ufo/waves/round-53/w3/swarm-registry.json:338` — the 1Password reference-scheme prefix appearing inside the *seat-spec text* of the dispatch file
  (the spec string that enumerates what to scan for). Same shape at `.ufo/waves/round-53/w3-spec.json:10` and `:285`,
  and in the already-committed `w1-spec.json`, `w2-spec.json`, `w1-dispatch.json`, `w2-dispatch.json`, `w3-dispatch.json`,
  `build_spec_w1.py:53`, `build_spec_w2.py:41`, `build_spec_w3.py:49`. **Precedent: this shape already landed** — the
  round-53 spec files are tracked at `1373b6ca` and trip the same rule. Class: none (it is the name of a scheme in
  prose, not a reference). Must not block; note that `stage_scan.py` over the *whole* `.ufo/waves/round-53/` tree will
  therefore always exit 1, so the gate must be run per-tree (as the registry row says) rather than over the wave dir.
- `.ufo/waves/round-53/w3/C2RevLedgerPlan/anchor-digest-check.txt:1-21` — 21 lines of the form `anchor token=<64 hex>`.
  These are the sha256 anchors of `corpus/SOURCES.md` rows S173–S193; I matched them against the source and they are
  byte-identical to the digests in `corpus/SOURCES.md` (e.g. `39ce8d13…09439` at `corpus/SOURCES.md:188`). Class: none.
  Worth one line in the L1's landing note: the word `token` in that file is a label for a content digest, not a secret.
- `.ufo/waves/round-53/w3/C1PriceScoutD/fetched/row-tune-mjcf__dao-code-verify-tunemjcf-introspect.ts:26` —
  `const apiKey = process.env.VOLCENGINE_API_KEY ?? "";`. Class: none — an env-var read with an empty default, no
  value in the file.
- `.ufo/waves/round-53/w3/C1PriceScoutD/fetched/row-pytorch-model-recovery__arxiv-2608.23616v3.html` — the only archive
  with an absolute-path-looking string, `/home/page.tsx`; it is a route in an upstream Next.js app, not a host path.

### F4 — `injection` (NONE — must not block; 3 quoted prompts, 1 real prompt template)
No fetched third-party byte in w1/w2/w3 carries an instruction addressed to an AI reading *this* corpus. The matches
my scanner produced are all quoted material in papers about agents, and all are inert as instructions:

| file:line | content | assessment |
|---|---|---|
| `C1ScribeSources2A/fetched/verification-horizon-arxiv-2606.26300v1.html:2121` | "You are a helpful assistant agent that can interact with a computer shell multiple times." | a **quoted prompt** printed in the paper's appendix "We present the full prompt used by our quality judge agent" — a specimen, not an instruction to the reader |
| same file `:2865`, `:2937` | judge prompts ("You are a senior frontend developer and strict code reviewer…") | appendix specimens (Appendix D) |
| same file `:3996` | "You are a professional expert in human–computer dialogue quality evaluation." | appendix specimen (I.1 System Prompt) |
| same file `:2215` | "The agent must output a single-line JSON object:" | descriptive paper prose |
| `C1ScribeSources2A/fetched/benchjack-2605.12673v1-first1MiB.html:2273`, `:2541`, `:2910` | "If the agent and evaluator must share an environment…", "The agent is required to write…", "the agent must report all the flaws…" | paper prose describing an audit design |
| `C1PriceScoutE/fetched/tb2audit-harden_tests.py:125` | `prompt = f"""You are a test case hardening expert…"""` | **a real LLM prompt template inside a third-party script**. It is inert as an injection (it is an f-string constant inside a Python file that is never executed by the lane), but it is the one archive in the landing set that contains a live prompt template aimed at a model. Worth naming to the L1. |
| `C1PriceScoutE/fetched/tb2audit-20260120-audit.txt:258`, `:1136`, `:1465`, `:2936` | "…would be difficult to bypass without actually solving the task", "…are essentially ignored, despite the task explicitly stating…", "The agent must actually find and extract the secret", "…an agent must properly solve the problem…" | audit prose about agent behaviour |

Class for all of these: **none** (contextual quotation, not injection). Two remarks that matter for the corpus
rather than for safety: the `verification-horizon` archive prints complete agent system prompts verbatim, and the
`tb2audit` archive prints per-task grader findings (`tb2audit-human-notes.txt` names `cobol-modernization`,
`merge-diff-arc-agi-task`, `modernize-scientific-stack`, `extract-moves-from-video` — four of the round's confirmed
tasks). Both are legitimate public sources and both are admissible prior-art material; they are only worth flagging
because a downstream reader may mistake quoted specimens for live instructions.

I also ran a targeted injection sweep over the wave-2 instruction captures and the wave-3 GitHub-API issue bodies
(`ghapi-issues-242.json`, `tb2-pr53.json`, `row-*.json`, the `sweep-*.json` search results) for
`ignore previous instructions`, `do not tell the user`, `you are now`, `act as`, `<<<SYS>>>`/`[INST]`/chat-template tags,
role-prefixed lines, `curl … | sh` and env-var exfiltration shapes: **0 hits**. The wave-2 instruction files
(`w2/C1ConfReadC/instruction-*.md`, `w2/C1ConfReadD/*.instruction.md`) are upstream Terminal-Bench task instructions
addressed to a *solver agent*, not to the reader of this corpus, and the reading seats quoted them rather than obeying
them — `w2/C1ConfReadC.md` describes them ("Instruction asks: find the CWE vulnerability in Bottle's `/app/bottle.py`…").

### F5 — `privacy` (MEDIUM for the corpus; LOW for the wave tree)
**(a) Absolute host paths that would dangle in a committed corpus.** The *landed* round-53 evidence is clean:
`corpus/evidence/round53/confirmations.json` contains **0** occurrences of `/home/vgpnk`; every `report` field is
lane-relative (`.ufo/waves/round-53/w2/C1ConfReadX.md`) and every one of the 20 rows' `report_sha256` matches the
file on disk (I re-hashed all 20: 20/20 match). `corpus/evidence/round53/pin-tree-2fd12b88.json` and
`tests-index.json` carry no host paths.

The wave tree itself is full of host paths, and that is expected of seat reports (they are told to print absolute
paths). Two cases would dangle **if copied into the corpus**:
- `.ufo/waves/round-53/w3/C1RevSources2/wave1-fetch-results.json` (46 `/fast/scratch/hyaku/kengaku-r53/…` pointers),
  `extra-fetch-results.json` (26), `lit-fetch-results.json` (15) — these point at scratch that is deleted at seat exit.
  Class: privacy/dangling-pointer. Must not block, but the L1 must not copy these `file`/`textfile` fields into
  `corpus/`; the durable pointers are the `sha256` and the archive names.
- `.ufo/waves/round-53/w3/C1RelabelRev2/read-manifest.json` (33 `/home/vgpnk/…` capture paths) — a reader manifest,
  fine in the wave tree.
- One landed-path defect worth the L1's attention, in the **ledger** rather than the wave tree:
  `plans/round53-tipstate.json`, row `round-close-check`, `argv[4]` = `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
  — a hard-coded fleet path in a file the C2 counter re-executes. Class: privacy (dangling). It is the `adoption-check`
  red cause already named in `facts.md`; I am not re-opening it, only recording that it is present at `9ead4476`.

**(b) Personal data in public archives.** Author e-mail addresses appear in the fetched papers and READMEs
(`barr-harman-…-survey.txt:7,10`; `schuler-zeller-…wayback.txt:5,20`; `blindspoteval-2610-32548v1.html:203,212,221,230`;
`petrovic-ivankovic-mutation-state-google.txt:7,10`; `holdout-findings-readme-2026-10-28.md:76`;
`rdi-trustworthy-benchmarks.html:307`). All are the published contact addresses of the paper authors, in papers already
cited by the lane. Class: privacy, no secret. Must not block.

### F6 — `privacy` — the graders corpus re-check (item 3): **clean**
`python3 plans/stage_scan.py corpus/evidence/round52/graders/` over **all 185 files** → `SCAN files=185 skipped=0 hits=0`,
so the round-52 "clean" verdict holds on the whole corpus, not only on the requested sample. The deterministic 10-file
sample I was asked to confirm (`find … -name '*.py' | sort | awk 'NR%9==1' | head -10`) is:

```
corpus/evidence/round52/graders/adaptive-rejection-sampler/tests/test_outputs.py
corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py
corpus/evidence/round52/graders/crack-7z-hash/tests/test_outputs.py
corpus/evidence/round52/graders/feal-linear-cryptanalysis/tests/test_outputs.py
corpus/evidence/round52/graders/gpt2-codegolf/tests/test_outputs.py
corpus/evidence/round52/graders/log-summary-date-ranges/tests/test_outputs.py
corpus/evidence/round52/graders/mteb-retrieve/tests/test_outputs.py
corpus/evidence/round52/graders/polyglot-c-py/tests/test_outputs.py
corpus/evidence/round52/graders/qemu-startup/tests/test_outputs.py
corpus/evidence/round52/graders/schemelike-metacircular-eval/tests/test_outputs.py
```

`stage_scan.py` on that sample → `SCAN files=10 skipped=0 hits=0`; my extended scanner → 2 hits, both
`privacy/tmp-path` for `/tmp/data.txt` inside `qemu-startup/tests/test_outputs.py:15,58` (a container path in a test
fixture, not a host path). Independent supplementary shapes I checked over all 185 files — JWT (`eyJ….….…`),
`Authorization:` header, `curl -u user:pass`, PEM private key, credentials embedded in a URL, `.netrc`,
`ssh-rsa AAAA`, dotenv-style `*_KEY=…` — **0 hits**.

The only credential-shaped text in the whole corpus is documented and deliberately absent:
`corpus/evidence/round52/graders/EXCLUDED.md` records that `sanitize-git-repo/tests/test_outputs.py` was excluded
because push protection flags a Hugging Face token pattern in that public upstream fixture. I confirmed the exclusion
still holds: `sha256sum -c SHA256SUMS` inside the graders directory → **183 OK**, 1 failure = the deliberately absent
`sanitize-git-repo` path (listed but unreadable, exactly as `EXCLUDED.md` says), and
`corpus/evidence/round52/graders/sanitize-git-repo/tests/` contains no `test_outputs.py`. Class: none. The password-like
strings that do appear are task fixtures (`password-recovery/tests/test_outputs.py:18` expects the literal
`8XDP5Q2RT9ZK7VB3BV4WW54`; `qemu-alpine-ssh/tests/test_outputs.py:27` uses `password123`; `git-leak-recovery` uses
`secret[lost_and_found_in_git]`) — these are benchmark challenge values, not credentials. Class: none.

## Item 2 — the prior-art archives that will land in `corpus/evidence/round53/fetched/`

`corpus/evidence/round53/fetched/` **does not exist yet** at `9ead4476`; the pricing seats keep their archives in their
own seat directories and the L1 integrates them. So I screened every archive that a pricing seat has produced, on the
criterion you gave: body embeds secrets, session URLs, or > 1 MiB of minimised JS.

- **89 archives** exist across `.ufo/waves/round-53/w3/*/fetched/` at 2026-10-30T05:14Z (the tree is live: seats are
  still writing, so this count moves) plus **52** in the wave-1 scout directories. 66 of the 89 wave-3 archives carry a
  `SOURCE-URL:` first line; the 23 that do not are the scribe's raw captures (`C1ScribeSources2A/fetched/`) and the
  `C1ScoutLitSrc/fetched/manifest.json` index. **None** of the 52 wave-1 scout archives carries the header.

  That matters for the C1 counter's PRIOR-ART leg, not for safety: the
  counter requires the archive's first line to be `SOURCE-URL: <url>` matching the row's URL (`HDR` in
  `plans/round53_c1_triage.py:375`, used at `:425`). The wave-3 pricing archives (C1PriceScoutC/D/E, C1ScoutLitSrc)
  are all correctly headed; the scribe archives are not, and they are not cited by any prior-art row, so this is
  consistent — but the L1 must not reuse a scribe archive as a PRIOR-ART archive without adding the header.
- **Secrets:** the two findings above are the only credential-shaped strings in any landing candidate. Nothing else in
  the 89 wave-3 archives matches any of my 25 rules. Specifically **0** live credentials, **0** `Bearer` headers, **0**
  `Set-Cookie`, **0** session-cookie assignments, **0** signed-URL parameters (`X-Amz-Signature`, `sig`, `access_token`),
  **0** JWTs, **0** private keys, **0** 1Password-style references.
- **Session URLs:** I scanned every URL in every archive for session-bearing parameters
  (`session`, `jsessionid`, `sid`, `PHPSESSID`, `token`, `access_token`, `auth`, `api_key`, `X-Amz-Signature`,
  `X-Amz-Credential`, `sig`, `refresh_token`): **0 hits** across w1, w2 and w3. The GitHub-API JSON archives
  (`ghapi-issues-242.json`, `ghapi-pulls-53.json`, `tb2-pr53.json`, `ekellbuch-tb21-issue4.json`, the `sweep-*.json`
  search results) contain `"private": false` (the repository-visibility field) and `git@github.com:…` SSH URLs — public
  metadata, no credentials, no e-mail addresses.
- **> 1 MiB of minimised JS:** **0 archives** exceed 1 MiB of inline `<script>` bytes. The largest are
  `tb2audit-substack.html` (207 427 bytes total, 82 040 script bytes) and `inspect-ai-scorers.html` (65 855 / 19 229).
  Two archives worth naming for a different reason: `preferencemodel-tb4-issues.html` (wave 1) is 1 000 000 bytes of
  which 519 694 are inline script (a client-rendered page, truncated at a 1 MB cap — the cap is disclosed in
  `w1/C1ScoutSrcBench/search-log.md:66`) and `benchjack-arxiv-2605.12673v1.html` is exactly 1 048 576 bytes (truncated
  at exactly 1 MiB, disclosed in `w1/C1ScoutSrcAudit/draft-registry-rows.md:12`). Both are truncated captures, which is
  a provenance note, not a security one — and the counter's quote check reads only the text as stored.
- **Integrity of the archives the rows cite:** I re-hashed every archive referenced by the two delivered
  `prior-art-part.json` files. All 8 cited archives and all 5 sweep archives of C1PriceScoutC, and all cited archives of
  C1PriceScoutD, **match** their recorded sha256; every quote is 8–21 words and is present verbatim in the archive it
  cites (8/8 and 8/8). Class: none.

## One adjacency finding the L1 should see (not a security finding, but it blocks the same landing)

The PRIOR-ART leg of the counter resolves an archive path with `inside(lane, rel, "corpus/evidence/round53/fetched")`
(`plans/round53_c1_triage.py:400-404`, helper at `:86-96`): the path must be **lane-relative** and must resolve
**inside `corpus/evidence/round53/fetched/`**. I ran that helper over the delivered parts:

- `C1PriceScoutC/prior-art-part.json` — cites `corpus/evidence/round53/fetched/ghapi-pulls-53.json` etc. Those paths
  are the right *shape* but the directory does not exist yet, so `inside()` returns `None` today; once the L1 copies the
  archives into `corpus/evidence/round53/fetched/` they become admissible. Correct as written.
- `C1PriceScoutD/prior-art-part.json` — cites `.ufo/waves/round-53/w3/C1PriceScoutD/fetched/row-…` (the seat's own
  directory). `inside()` **rejects** that shape: it is outside `corpus/evidence/round53/fetched/`. Every one of D's rows
  and sweeps is currently inadmissible and would be rejected as
  `fetch-missing-outside-fetched-dir-or-digest-mismatch` / `sweep-fetch-missing-duplicate-headerless-or-names-the-task`.
  D's own part file has been rewritten once already (the earlier `row-gcode-to-text__adeotek-pr11.json` is gone, replaced
  by `row-gcode-to-text__arxiv-2507.02825v1.html`), so this is a live file.

Smallest remediation for the L1: when integrating, rewrite D's `fetched`/`file` pointers to
`corpus/evidence/round53/fetched/<basename>` and copy the archives there. I am not editing it — the pricing seats own
their parts and the L1 integrates.

For completeness: I also checked D's `tune-mjcf` row, whose quote is 8 words (the lower bound of the frozen 8–25 rule)
and whose verdict is `phenomenon-known`, and `C1PriceScoutC`'s `modernize-scientific-stack` row, whose archive
(`ghapi-issues-242.json`, upstream issue #242) **does** name the task and its test — as `phenomenon-known` requires
(`names_task` returned `True` for it and `False` for all seven `phenomenon-new` archives, so the A1/A2 "the body must not
name the task" rule holds on the delivered set).

## Grader bytes copied into reports (the ≤ 25-word rule)

I measured the longest run of captured grader bytes appearing verbatim in each wave-2/wave-3 report, by matching
report substrings against the concatenated 185-file grader corpus. Longest run in any report: **109 characters / ~1 word**
(`w2/C1ConfRead{A,B,C,D,G}.md`), and the longest multi-word run is **8 words / 56 characters**
(`w3/C1ScoutLitSrc.md`, a phrase from a fetched page, not from the graders). Every `quote` in the landed
`corpus/evidence/round53/confirmations.json` is ≤ 9 words (max over 20 rows), and in the five wave-2
`confirmations-part.json` files the max is 9 words. No report copies grader bytes wholesale; the ≤ 25-word rule holds.

## Bottom line for the L1

1. **One archive must not be staged as-is**: `w3/C1PriceScoutE/fetched/tb2audit-substack.html` (F1) — two public
   credential-shaped strings; exclude it from the landing set (the sibling `tb2audit-*` files suffice) or redact the two
   values and record the redaction.
2. **One documentation file needs a waiver or a redaction**: `w3/C1ScoutLitSrc/fetched/harbor-verifier.md:98` (F2) — a
   `$ANTHROPIC_API_KEY` placeholder; false positive, but the lane's own `stage-scan` gate exits 1 on it.
3. **Everything else is clean**: 0 live credentials, 0 session URLs, 0 > 1 MiB minimised-JS archives, 0 prompt
   injections, 0 host paths in the corpus that will land, and the round-52 grader corpus is clean on all 185 files
   (not only the 10-file sample) with the one credential-shaped upstream fixture still deliberately excluded.
4. **Adjacency**: `C1PriceScoutD/prior-art-part.json` points its archives at its own seat directory, which the counter's
   `inside()` helper rejects — rewrite the pointers to `corpus/evidence/round53/fetched/…` at integration time.

## Files produced (absolute paths)

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53SentinelFetch2.md` — this report.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53SentinelFetch2/scan_extended.py` — companion
  scanner (25 rules, credential / injection / privacy; masks matched secrets; passes its own `stage_scan.py`).

Scratch: `/fast/scratch/hyaku/kengaku-r53/R53SentinelFetch2/` (a `--shared` clone of the lane plus one `mktemp -d`
fixture used to test `stage_scan.py` against a projected `corpus/evidence/round53/fetched/` layout) — removed before
yield. Disk guard read before the heavy passes: `/fast` 464 G free (43 % used), `/home` 534 G free (41 % used); no
ENOSPC.

Tool versions / channels: `python3` (system), `git`, `curl`, `sha256sum` (system) — no installs, no upgrades, no
pacman. No `tool:` inconsistencies observed.
