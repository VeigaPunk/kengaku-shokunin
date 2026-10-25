# FxSentinel — security/safety scan of round-32's whole new byte surface

Seat: `L1Kengaku32.FxSentinel` (sentinel, falsify wave) · 2026-10-25 · lane
`kengaku-shokunin`, claims frozen at `0d32691d`.
Scope scanned: drafted entry `corpus/knowledge/benchmark-grader-semantics.md`,
new SOURCES rows S093/S094/S097/S101/S102 (`corpus/SOURCES.md`), the four
counters (`plans/round32_defects.py`, `plans/catalog_probe.py`,
`plans/round32_c1_verify.py`, `plans/adoption_check.py`), claims receipts
(`.ufo/waves/round-32/claims/*`), `gate-receipt.txt`, captures
(`.ufo/waves/round-32/assimilation/captures/*`), assimilation state files,
`build-run.log`/`falsify-run.log`, specs/registries, and all 34 build-seat
reports under `.ufo/waves/round-32/build/`.
Method: regex scans (credentials, URL shapes, shell/subprocess patterns,
resource patterns, IPs, emails), digest re-verification, URL inventory, and
targeted reads. No tools installed (read-only grep/read/curl; `pacman`
paused host-wide — no channel activity to record).

Findings are grouped (a)-(e); item count = number of distinct attack
items/observations (numbered). All file:line references are relative to the
lane root unless prefixed `FLEET:` (fleet repo).

---

## (a) Credential material — no live credentials; 7 observations

1. **Zero real `op://` references** in the new byte surface. The only
   occurrences of `op://` are echoes of the seat prompts inside
   `build-spec.json:191`, `falsify-spec.json:32`, and the run logs
   (`build-run.log:552`, `falsify-run.log:512`) — prompt text, not usage.
   Verified by targeted grep excluding prompt echoes. (clean check)
2. **Zero token patterns**: no JWT (`eyJ…`), no `sk-`/`hf_`/`AKIA`/
   `AIza`/`BEGIN … PRIVATE KEY`/`ssh-rsa`, no `access_token=`,
   `client_secret=`, `X-Amz-Signature`, `GoogleAccessId`, `Signature=`
   across `.ufo/waves/round-32/`, the entry, and the four plans. The only
   substring hits are prose (`round32_defects.py:15` "bogus token") and
   the hyphenated word "sk-parameterised" in the staged sibling package
   (reported by R32Sentinel.md:16). (clean check)
3. **Userinfo URLs**: none (`user:pass@host` count 0). (clean check)
4. **Capture contains a working service-account loader template** —
   `assimilation/captures/toolathlon-ab-testing-evaluation-main.py:104`
   `get_project_id_and_credentials(credentials_file="configs/gcp-service_account.keys.json")`,
   `:116` `service_account.Credentials.from_service_account_file(credentials_path)`.
   Bytes are upstream public code (pinned Toolathlon commit, digest
   `3bad26b6…` verified), so no secret is leaked; but this is a live
   credential-loading path inside the committed byte surface, and if the
   file were ever executed at a cwd containing a real
   `configs/gcp-service_account.keys.json`, it would read it. It must stay
   capture-only (never executed by any counter — confirmed: the counters
   never import or run the capture).
5. **Sibling credential guidance referenced, not reproduced** —
   `R32ConnSibling.md:102-103` names `corpus/knowledge/credential-isolation.md:18-21`
   (OpenRouter credential-prefix/env-var cut) — pointer only, no value in
   this surface.
6. **Path names of potential credential carriers appear in a build report**
   — `R32DraftMistakes.md:88` (fleet status paste: ` M scripts/hyaku/hyaku.env`,
   `?? .omp/mcp.json`) and `:110` (disposition table). No contents land in
   the lane; but these are exactly the files that may hold run credentials,
   and the report confirms they were modified this cycle. Hygiene note:
   no lane-committed byte should ever need to name them; recommend scrubbing
   the sweep output before landing the lesson if it is copied verbatim.
7. **No env-var reads, no credential env names** in the four plans: grep
   for `os.environ|getenv|API_KEY|AWS_|GOOGLE_|OPENROUTER_|HF_` returns no
   plan code hits (only prose mentions in reports). `catalog_probe.py:46`
   sets a fixed `User-Agent` header only; no Authorization header, no
   cookie, no token parameter. (clean check)

## (b) Unpinned / session URLs — 8 observations

8. **S097 registry row URL is unpinned and unversioned** —
   `corpus/SOURCES.md:115` cites `https://arxiv.org/abs/2412.05579`
   (no `v2` fragment). The pin lives only in the anchor cell text; the URL
   itself serves "current version" (today v2). If arXiv posts v3+, the row
   URL silently redirects while the row claims v2. Effective-URL behavior
   documented at `R32LearnC1.md:12`.
9. **Entry cites the same unversioned abs URL** —
   `corpus/knowledge/benchmark-grader-semantics.md:3`
   (`https://arxiv.org/abs/2412.05579` + "arXiv 2412.05579v2" in prose).
   `R32RevEntry.md:162-167` (F7) already flags the entry-vs-row citation
   mismatch; the on-disk entry still carries the unversioned URL. For
   byte-equal citations, use `/abs/2412.05579v2`.
10. **S093 and S094 registry rows cite bare repo roots** —
    `corpus/SOURCES.md:112` `https://github.com/scaleapi/SWE-bench_Pro-os`
    and `:114` `https://github.com/hkust-nlp/Toolathlon`. Pins
    (`66f92766…`, `9be8d8fe…`) are anchor-cell text only; the URL resolves
    to branch-tip. Acceptable as-is since the anchor pins, but the row URL
    is not itself pinning.
11. **Probe endpoints are live by design and unpinned** —
    `plans/catalog_probe.py:29-30` (`https://huggingface.co/api/models?limit=50`,
    `https://openrouter.ai/api/v1/models`). This is inherent to C3's
    freshness claim; the hazard is that the counter records no response
    digest (see item 25) — nothing proves which bytes satisfied it.
12. **Quarantine report cites a cleartext-http Wayback snapshot** —
    `R32Quarantine.md:25`: `http://web.archive.org/web/20251118034714/https://www.meti.go.jp/...`
    (http, not https). Snapshot is timestamp-pinned (fixed), but the
    transport is not.
13. **Captured arXiv page references an unversioned PDF link** —
    `assimilation/captures/arxiv-2412.05579v2-abs.html:41`
    (`https://arxiv.org/pdf/2412.05579`). Page content, not a lane
    citation; it is another unversioned reference carried inside the
    capture.
14. **Catalog entry cites the live endpoints twice** —
    `corpus/knowledge/open-model-catalogs.md:1-2` (source lines) and
    `:15`, `:35` (GET statements). Consistent with the claim; unpinned by
    design; documented in the entry.
15. **All other URLs in the surface are public and pinned by commit or
    snapshot**: raw.githubusercontent.com links carry full commit SHAs
    (e.g. `R32ReconPackage.md:20-24`, `captures/SHA256SUMS.txt:3-4`),
    GitHub rows pin via anchor cells, arXiv v2 via anchor. No session URLs,
    no private domains, no IP literals except `127.0.0.1:34113` in the
    pre-existing local-inventory section (`open-model-catalogs.md:52`,
    unchanged content). (clean check)

## (c) Command injection / shell=True — 6 observations

16. **`round32_defects.py:58-61`** — `subprocess.run(["git","-C",str(lane),*args], …)`
    argv-list, no `shell=True`, no `os.system`/`popen`/`eval`/`exec`.
    (clean check)
17. **`adoption_check.py:132-141`** — census `subprocess.run([str(CENSUS),"validate","--root",str(lane.parent),lane_name], …)`;
    argv-list; `lane_name` derived by suffix slice (`:133`), no shell
    interpolation. (clean check)
18. **`catalog_probe.py:45-48`** — `urllib.request.urlopen` only. (clean
    check)
19. **`round32_c1_verify.py`** — no subprocess at all (pure file reads and
    regex). (clean check)
20. **A committed report embeds a shell-command example** —
    `R32DraftMistakes.md:254` (`grep -rl "m-rev-vs-rev" --include='*.md' …`).
    Not executed by any process today; flagged as latent template-injection
    surface only if tooling ever starts executing report content (none
    does).
21. **Task specs present commands with placeholder filenames** —
    `build-spec.json:89` and `falsify-spec.json:16/20` instruct seats to
    run `python3 plans/sources_adopt.py --quote-file <rows.txt> --artifact <capture-dir> --url-map <map.json>`.
    If a seat resolves the placeholders by copy-paste under a hostile
    filename, argv/flag injection is possible (e.g. `--out …`), though no
    harness executes these strings programmatically. Process-level note,
    low severity.

## (d) Unbounded / destructive resource use — 9 observations

22. **Unbounded response read** — `plans/catalog_probe.py:47-48`:
    `response.read().decode(...)` with no size cap; `timeout=20` bounds
    time only. A misbehaving/compromised endpoint could balloon memory.
    Moderate; the two fixed endpoints are small today (HF limit=50;
    OpenRouter ~790 KB observed).
23. **JSON parse of the whole body** — `catalog_probe.py:51-58` /
    `:61-71` `json.loads(text)` on the full unbounded body (same root as
    22).
24. **Good guards**: `parse_hf` rejects empty list (`:54-56`); `parse_openrouter`
    rejects missing/empty `data` (`:63-69`); fetch failures are caught at
    `:111-117`. (clean check)
25. **The C3 counter writes NO receipts** — `catalog_probe.py` has no write
    path (verified by code read and by the empty
    `corpus/evidence/round32/` directory). The receipts the frozen C3
    predicate and the rows/entry cite
    (`corpus/evidence/round32/catalogs/after.txt` — `SOURCES.md:116-117`,
    `open-model-catalogs.md:1-4`) DO NOT EXIST at scan time. `entry_ok`
    (`catalog_probe.py:82-91`) checks only that the literal directory
    string appears in the entry. The claim can turn green with zero receipt
    bytes on disk. This is the strongest integrity/safety gap in the
    surface. (finding)
26. **All-or-nothing probe accounting** — `catalog_probe.py:74-79,111-120`:
    one API exception zeroes both counts and prints `hf=fail openrouter=fail`
    (also recorded by `R32CritC3.md:18`). Fails closed (safe) but erases
    the reachable source's result, contradicting the kill rule's per-source
    honesty wording.
27. **Local reads are bounded by repo/file size** — `round32_defects.py:54-55`,
    `adoption_check.py:40,60,64,73`, `round32_c1_verify.py:43-44` use
    `read_text` on committed files only; no unbounded iteration. (clean
    check)
28. **No destructive operations in any plan**: no `rm -rf`, `shutil.rmtree`,
    `unlink`, truncation, `chmod/chown`, or device writes; selftests use
    `tempfile.TemporaryDirectory` (`round32_defects.py:207-240`,
    `catalog_probe.py:123-171`). (clean check)
29. **Wave seats were non-destructive** — file inventory shows only the 34
    build reports under `build/`, claims receipts, assimilation state, and
    the two captures; report assertions confirm `--max-time`-bounded curl
    into `/tmp/r32-*` only (e.g. `R32CatProbe.md:4-7`,
    `R32Quarantine.md:6`). (clean check)
30. **`round32_c1_verify.py:130`** reads expect-file bytes for sha256 —
    bounded. (clean check)

## (e) PII — 8 observations

31. **Commit-author identities embedded in a committed build report** —
    `R32DraftMistakes.md:232`:
    `author=protocol-shokunin <protocol@shokunin.local>` and
    `t <t@t>` (with `date=Sun Oct 25 09:29:03 2026 -0300`). Synthetic
    and domain-local, but these are personal-looking name+email tokens in
    a lane-committed artifact; recommend redacting the author tokens (keep
    the commit hashes) if this incident evidence is carried into the
    lesson.
32. **Workstation username/absolute paths leak into committed receipts** —
    `claims/defects-before.txt:4` and `claims/control-nothing.txt:3-4`
    carry `/home/vgpnk/Projects/shokunin/...`; `gate-cli-exits.txt` (regenerated
    receipt) pastes the same absolute cwd; `R32PlanWalk.md:101-117` pastes
    fleet-root paths. This discloses the local account name and machine
    layout in bytes that are meant to be repro/receipt artifacts, and it
    breaks portability (same counters on another user/path will not match
    byte-for-byte). Recommend `$HOME`-relative renderings.
33. **arXiv author list appears in the capture** —
    `captures/arxiv-2412.05579v2-abs.html:41` (Li Haitao, Dong Qian, Chen
    Junjie, Su Huixue, Zhou Yujia, Ai Qingyao, Ye Ziyi, Liu Yiqun) and in
    `R32SrcS097.md:14` and `falsify/FxS097Frame.md:10`. Public
    bibliographic data, required for provenance — not PII in the GDPR
    sense, recorded for completeness.
34. **Writer pseudonym** — `benchmark-grader-semantics.md:6` and
    `open-model-catalogs.md:5` `writer: KengakuR32` — pseudonym, fine.
35. **No other emails/phones/private IPs** in the surface: IP scan finds
    only `127.0.0.1:34113` (pre-existing local-inventory line,
    `open-model-catalogs.md:52`) and DOI hosts; email scan finds only
    item 31's author tokens. (clean check)
36. **`falsify/FxS097Frame.md` names the authors again** (public data, same
    class as 33). (clean check)
37. **Agent identities** — swarm registries (build + falsify) carry only
    seat names/roles/status; no personal data. (clean check)
38. **The run logs embed full seat prompts** incl. lanes' absolute paths
    (`build-run.log:397`, `falsify-run.log:382`) — operational data, not
    PII; noted because the logs are uncommitted wave artifacts that would
    carry the same machine paths if ever committed.

## Additional integrity/operability observations surfaced by the scan (4)

39. **Cited receipts absent while counters can pass** — item 25's concrete
    evidence: `corpus/evidence/round32/` exists (created 09:53) but is
    empty; `corpus/evidence/round32/catalogs/after.txt` does not exist;
    yet `catalog_probe.py` would print `entry=ok` (it only substring-tests
    `RECEIPTS`). S101/S102 rows (`SOURCES.md:116-117`) would cite a
    nonexistent receipt. Landing must create these bytes *before* the
    counters run; an unrun/uncreated receipt is a refusal verdict.
40. **V6 control provenance is a git witness, not a counter** —
    `round32_c1_verify.py:125-136` pins the expect-file digest and
    `exit=1`, but nothing ties the control file to the freeze commit; an
    actor mutating both `adoption-expect.json` and `control-nothing.txt`
    in the landed tree passes V6 (also documented at `R32CritC1.md:75`).
41. **Hard-coded absolute FLEET paths couple counters to this host** —
    `round32_defects.py:44-46` and `adoption_check.py:35`; a moved home or
    another user fails closed (exit 1) — safe direction, portability cost.
42. **Quote-location methodology is capture-dir sensitive** —
    `R32QuoteMode.md:87-90`: putting the rows file inside the artifact dir
    made S097's abstract quote "locate" inside rows.txt itself (false
    `unmapped` vs `absent`). The gate's verdict depends on a clean capture
    dir; a reviewer re-running quote mode must preserve that invariant.

---

## VERDICT: findings
