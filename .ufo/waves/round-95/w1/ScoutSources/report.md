# ScoutSources — R95 SOURCES S303–S309 live re-open + C11/C15 source recon

Seat ScoutSources-35, kengaku round 95, ONE v1 wave. Measured tip T = `afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239`; all lane content was read from a detached `git clone --shared` of T in scratch (removed at seat exit, after receipts were copied). All fetches on 2026-11-05 (UTC). No instrument was touched (FROZEN RULE respected); every observation below routes to round 96 if wanted. No tools were installed or upgraded for this seat (none needed); no sysctl or namespace touched.

## 1. Live re-open of S303–S309 — 7/7 clean, zero drift

Method: each row's URL fetched with `curl -sS -o <live> -w '%{http_code} %{size_download} %{time_total}s'`; sha256 compared to (a) the row's recorded sha256 and (b) `git cat-file blob T:corpus/evidence/round95/graders/fix-code-vulnerability/<capture>`; quote located by exact substring match; word count = `len(quote.split())`.

| Row | URL (tail) | HTTP | bytes | sha256 = row | = capture | quote on cited line | unique | words |
|-----|------------|------|-------|--------------|-----------|---------------------|--------|-------|
| S303 | `fix-code-vulnerability/tests/test_outputs.py` @2fd12b88 | 200 | 4010 | yes `c006a5de…` | yes | :45 yes | yes | 7/7 |
| S304 | `fix-code-vulnerability/solution/solve.sh` @2fd12b88 | 200 | 913 | yes `7a0131b3…` | yes | :20 yes | yes | 4/4 |
| S305 | `fix-code-vulnerability/environment/Dockerfile` @2fd12b88 | 200 | 814 | yes `09174709…` | yes | :22 yes | yes | 6/6 |
| S306 | `bottlepy/bottle` `bottle.py` @0207a34f | 200 | 175847 | yes `abf64368…` | yes | :1562 yes | yes | 12/12 |
| S307 | `fix-code-vulnerability/instruction.md` @2fd12b88 | 200 | 3873 | yes `89b1abdf…` | yes | :18 yes | yes | 14/14 |
| S308 | `fix-code-vulnerability/tests/test.sh` @2fd12b88 | 200 | 653 | yes `f1611da6…` | yes | :9 yes | yes | 4/4 |
| S309 | `fix-code-vulnerability/task.toml` @2fd12b88 | 200 | 967 | yes `9aa2bd14…` | yes | :29 yes | yes | 3/3 |

Every quote occurs on exactly one line of its file — the cited line. Per-row machine receipt: `receipts/sources-refetch.json` (URL, t_start/t_end, curl timing, sha256, line hits, word count); raw bodies under `receipts/live/`.

S305's mechanism arithmetic also re-verified against the S306 capture: upstream `def _hkey` at bottle.py:1560 with raising check at 1562–1563; `def _hval` at 1567 with raising check at 1569–1570. The Dockerfile's two sequential `RUN sed` lines (Dockerfile:22 `'1562,1563d'`, :23 `'1567,1568d'`) therefore delete `_hkey`'s check at original numbering and `_hval`'s check at the post-deletion numbering (original 1569–1570 → 1567–1568). S305's wording "deletes lines 1562-1563, then 1567-1568 of the result" is exact.

## 2. C11/C15 recon — bottlepy/bottle @ 0207a34f0c5716cd292dd4480253ad35d3da49f3

Tree fetched two ways: codeload tar.gz (`https://codeload.github.com/bottlepy/bottle/tar.gz/0207a34f0c5716cd292dd4480253ad35d3da49f3`, HTTP 200, 829931 B) and raw `test/test_environ.py` (HTTP 200, 38675 B). Commit is "typing: Type hints for pyright", authored 2025-06-27T10:14:03Z (GitHub API).

**2a. No test names the helpers.** `grep -rni 'hval|injection|_hkey' test/` over all 30 test files → zero matches; `grep -rni injection` over the whole tree → zero matches. Receipt: `receipts/bottle-test-scan.txt`.

**2b. But a behavioral header-injection test exists at this exact commit.** `test/test_environ.py:735` `def test_prevent_control_characters_in_headers(self):` (735–755) drives `'\n', '\r', '\n\r', '\0'` through HeaderDict APIs (`append`, `replace`, `__setitem__`, `setdefault`; assertRaises at :745–746) and BaseResponse APIs (`add_header`, `set_header`, `__setitem__`; assertRaises at :754–755), both name-side and value-side. At 0207a34f the value side routes through `_hval` — call sites bottle.py:1712, 1722, 1726 (`BaseResponse.__setitem__`/`set_header`/`add_header`), 2190/2193/2196 (`HeaderDict.__setitem__`/`append`/`replace`), 1750 (`Set-Cookie`); the name side through `_hkey` (1703–1726, 2181–2205). [INFERENCE, not executed: deleting the `_hval` raising check — the task's oracle removal — makes :754 fail; deleting `_hkey`'s check makes :746/:755 fail. A 20-line harness could confirm if round 96 wants it.]

**2c. Grader side (C11).** Live `tests/test_outputs.py` contains zero `_hval` occurrences (grep receipt `receipts/c11-c15-grader-lines.json`). The only guard import is `from bottle import _hkey` at :61, :85, :105 inside `test_hkey_basic_cases` (:55), `test_hkey_error_cases` (:82), `test_hkey_real_world_examples` (:102); the ValueError leg is :87–99. Confirms the frozen C11 wording "no function of the grader calls `_hval`" against the live bytes.

**2d. C15 hook, quoted.** test_outputs.py:58–59:
```
    bottle_path = os.path.join(os.path.dirname(__file__), "bottle")
    sys.path.insert(0, bottle_path)
```
then `from bottle import _hkey` at :61; tests 2 and 3 import at :85/:105 with no sys.path setup of their own (they rely on the entry inserted by test 1 in the same pytest session, then the harness path). Full listing: `receipts/grader-imports-63-110.txt`. I did not re-run the shadowing experiment — that finding is owned elsewhere; this is the import-order evidence it hangs on.

**2e. Routed to round 96 [INFERENCE].** S308's recorded flip ("an offline copy of bottle's test tree at 0207a34f and pinned pytest wheels") would not be coverage-neutral: the upstream suite's `test_prevent_control_characters_in_headers` would detect BOTH oracle deletions behaviorally (2b). No frozen row or claim text asserts the absence of such a test, so nothing flips now — but any round-96 plan that stages the upstream test tree should expect it to fail on the vulnerable build and pass on the solved one.

## 3. Prebuilt image `alexgshaw/fix-code-vulnerability:20251031` — publicly readable without pulling

- Hub tag API `https://hub.docker.com/v2/repositories/alexgshaw/fix-code-vulnerability/tags/20251031`: HTTP 200, 825 B. Tag active, `tag_last_pushed` 2025-10-31T02:57:21.23906Z, single linux/amd64 image, `full_size` 190685882 B, digest `sha256:cac325252991f823713b2d0441502972901dd782bd67f66c03d9b1e410dac5c0`.
- Registry manifest (anonymous bearer token, no login): `https://registry-1.docker.io/v2/alexgshaw/fix-code-vulnerability/manifests/20251031` → HTTP 200, 2840 B, `Content-Type: application/vnd.docker.distribution.manifest.v2+json`, `Docker-Content-Digest: sha256:cac32525…` — identical to the Hub digest, and sha256 of the manifest body equals that digest (self-consistent). Config digest `sha256:fe9be33bb13823b31284102c8b366e3fc83f5e84cedbba42d2540081c2d9899a` (7731 B).
- Config blob also fetched anonymously (first attempt 307 → CDN `production.cloudfront.docker.com`; with `-L` → 200, 7731 B; body sha256 = config digest). Image `created` 2025-10-28T22:08:34Z, 18 history entries, including exactly:
  - `RUN /bin/sh -c git clone -o origin --single-branch https://github.com/bottlepy/bottle.git /app && cd /app && git …`
  - `RUN /bin/sh -c sed -i -e '1562,1563d' bottle.py`
  - `RUN /bin/sh -c sed -i -e '1567,1568d' bottle.py`
  Full list: `receipts/image-config-history.txt`.

So the prebuilt image's anonymous metadata shows it was built by precisely the captured Dockerfile's oracle-removal lines — S305's recipe is the image's actual /app provenance as far as readable-without-pull metadata goes. A full layer-diff comparison with `VULNERABLE_BOTTLE_SHA` (S309's flip) still needs a pull; the manifest + config do not.

## Findings

No defect found; nothing here would flip an R95 verdict. All rows and the mechanism notes re-verified; new evidence is routed for round 96.

## Receipts index (all under `ScoutSources/`)

- `receipts/sources-refetch.json` — per-row URL, access times, HTTP, size, sha256, cited-line hit, word count
- `receipts/live/S303…S309 (7 files)` — raw fetched bytes
- `receipts/SOURCES-S303-S309-at-T.md` — the seven rows verbatim at T (lane clone line numbers 319–325)
- `receipts/c11-c15-grader-lines.json`, `receipts/grader-imports-63-110.txt` — grader import/_hkey/_hval line evidence
- `receipts/recon-context.txt` — Dockerfile capture, upstream bottle.py 1560–1571, test_environ header-test defs
- `receipts/bottle-test-scan.txt` — test-tree greps (zero name-level hits) + test_environ.py:735–755 + bottle.py call sites
- `receipts/net/{log.tsv, hub-tag-20251031.json, registry-manifest.json, registry-manifest.headers, config.json, config.headers}` — network receipts

## Access log (UTC 2026-11-05; wall-clock spans in `receipts/net/log.tsv` and `sources-refetch.json`)

| When | URL | Status | Bytes |
|------|-----|--------|-------|
| 23:14:42 | hub.docker.com/v2/repositories/alexgshaw/fix-code-vulnerability/tags/20251031 | 200 | 825 |
| 23:14:42 | api.github.com/repos/bottlepy/bottle/commits/0207a34f… | 200 | 6070 |
| 23:14:42 | api.github.com/repos/bottlepy/bottle/contents/test?ref=0207a34f… | 200 | 32719 |
| 23:15:1x (×7, ~0.02–0.30 s each) | raw.githubusercontent.com … (S303–S309 rows) | 200 ×7 | 4010/913/814/175847/3873/653/967 |
| 23:16:31 | codeload.github.com/bottlepy/bottle/tar.gz/0207a34f… | 200 | 829931 |
| 23:16:31 | raw.githubusercontent.com/bottlepy/bottle/0207a34f…/test/test_environ.py | 200 | 38675 |
| 23:16:31 | registry-1.docker.io/v2/alexgshaw/fix-code-vulnerability/manifests/20251031 | 200 | 2840 |
| 23:26:02 | registry-1.docker.io/v2/…/blobs/sha256:fe9be33b… (no -L) | 307 | 0 |
| 23:27:54 | same blob with -L → production.cloudfront.docker.com/… | 200 | 7731 |
