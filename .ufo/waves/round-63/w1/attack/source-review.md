# SourceReview — non-author verification of S228 and S229 (round 63, wave 1)

Seat: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-63/w1/attack/`
Scratch: `/fast/scratch/hyaku/kengaku-r63/SourceReview/` (empty; removed before yield)
Date: 2026-11-03. Frozen claims read first: `plans/round-63-claims.md`.
Scout recon used for quote cross-check: `.ufo/waves/round-63/w1/recon/recon.md` (present at poll check 8 of 20, `sleep 60` between checks; both scout captures `cmp`-identical to my independent re-opens before any quote work).

Every observed value below carries the command that produced it. I re-opened both sources myself; the scout's captures were only compared, never trusted as substitutes.

---

## 1. S228 — TB2 `pypi-server` grader at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`

### Re-open (live)

```
$ curl -fsSL --max-time 60 https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/pypi-server/tests/test_outputs.py -o <seat>/S228-reopen.py
CURL_S228_OK
$ sha256sum <seat>/S228-reopen.py
82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c  <seat>/S228-reopen.py
$ wc -c <seat>/S228-reopen.py
3177 <seat>/S228-reopen.py
$ cmp <seat>/S228-reopen.py corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py && echo CMP_IDENTICAL
CMP_IDENTICAL
$ sha256sum corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py
82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c  .../tests/test_outputs.py
$ sed -n '134p' corpus/evidence/round52/graders/SHA256SUMS
82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c  ./pypi-server/tests/test_outputs.py
$ cmp .ufo/waves/round-63/w1/recon/S228-pypi-test_outputs.py <seat>/S228-reopen.py && echo S228_SCOUT_BYTES_IDENTICAL
S228_SCOUT_BYTES_IDENTICAL
```

- sha equals the frozen pin sha `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c` — **MATCH**.
- Byte-identical (cmp) to the lane capture **and** to the scout's capture; 3177 bytes, 88 lines (`wc -l`).
- Content spot-read: `install()` = uninstall (`check=True`, tolerates "not installed") → `python -m pip install --index-url http://localhost:8080/simple vectorops==0.1.0` (`check=True`) → `pip show vectorops`; `test_api()` calls `install()`, imports `vectorops`, then four asserts (`assert v.dotproduct([1, 1], [0, 1]) == 1` at :85 etc.). Exactly the install/assertion contract the claims freeze describes.

### Scout quote verification (S228)

| scout quote | wc -w | verbatim in my re-opened bytes? | lines |
|---|---|---|---|
| `localhost:8080` | 1 | **YES** (`grep -F -n`) — 2 hits | :18, :30 |
| `pip install --index-url` | 3 | **NO contiguous string** (`grep -c -F` → 0) — the scout reported this absence itself; correct. argv is split one token per line (:24–32); `--index-url` alone at :29 | — |
| `vectorops==0.1.0` | 1 | **YES** — 2 hits | :31, :50 |

Scout's cited line numbers for these (:18, :29, :30, :31, :50) each confirmed by `sed -n '<n>p'`.

### Verdict S228: **verified**

No mismatch. The scout's non-quote observation ("pip install --index-url" is not a contiguous string in the file) is itself accurate and worth keeping in the row's anchor so nobody greps for it later.

---

## 2. S229 — PEP 503, Simple Repository API

### Re-open (live)

```
$ curl -fsSL --max-time 60 https://peps.python.org/pep-0503/ -o <seat>/S229-reopen.html
CURL_S229_OK
$ sha256sum <seat>/S229-reopen.html
5b97cb7e14fc1a384bdfaac70195763e0b3bfca5a4c5f70142c6e37d2c453c4f  <seat>/S229-reopen.html
$ wc -c <seat>/S229-reopen.html; wc -l <seat>/S229-reopen.html
20398 / 269 lines
$ cmp .ufo/waves/round-63/w1/recon/S229-pep-0503.html <seat>/S229-reopen.html && echo S229_SCOUT_BYTES_IDENTICAL
S229_SCOUT_BYTES_IDENTICAL
```

### Layout text location (the `/simple/<project>/` contract)

```
$ grep -n 'simple/' <seat>/S229-reopen.html | sed -n '1,2p'
144:  ... https://pypi.org/simple/ ...        (base URL sentence)
149:  ... https://pypi.org/simple/foo/ ...   (relative-URL note example)
$ grep -n 'Below the root URL' ... ; grep -n 'normalized name' ...
165:<p>Below the root URL is another URL for each individual project contained within
167:is replaced by the normalized name for that project, so a project named
$ sed -n '140p' <seat>/S229-reopen.html
<h2><a class="toc-backref" href="#specification" role="doc-backlink">Specification</a></h2>
```

- Line numbers: :144 (base URL `https://pypi.org/simple/`), :149 (note example `https://pypi.org/simple/foo/`), :165–:168 (project-URL paragraph: `/<project>/`, normalized name, "HolyGrail" → `/holygrail/`).
- Section heading: **`Specification`** (h2 at :140, `<section id="specification">` at :139).
- Page identity: title `<h1 class="page-title">PEP 503 – Simple Repository API</h1>` at :92; footer `Last modified: 2025-08-20 21:30:45 UTC` at :260 (`grep -n -i 'modified'`).

### Scout quote verification (S229)

| scout quote | wc -w | verbatim in my re-opened bytes? | lines |
|---|---|---|---|
| "The format of this URL is /<project>/ where the <project> is replaced by the normalized name for that project" | 19 | **YES, across :166–167** — docutils markup interleaves the fragments; each fragment contiguous ("The format of this URL is" :166, "is replaced by the normalized name for that project" :167). Not a single-line byte string; the scout noted the HTML wrapping itself | :166–:167 |
| "Below the root URL is another URL for each individual project contained within a repository." | 15 | **YES, across :165–166** ("… contained within" :165, "a repository." opens :166) | :165–:166 |
| section heading `Specification` | — | **YES** (h2) | :140 |
| title `PEP 503 – Simple Repository API` | — | **YES** (h1) | :92 |
| `Last modified: 2025-08-20 21:30:45 UTC` | — | **YES** at :260. Minor citation nit: the recon echoes `grep -n -i 'last-modified'` as the finding command, but the bytes carry `Last modified:` with a **space**, so that hyphenated pattern returns 0 (`grep -n -i 'last-modified'` → no output in my copy). The data (line, text, date) is correct; the echoed command is imprecise. Data verified by `grep -n -i 'modified'` → :260 | :260 |

### Verdict S229: **verified**

No content mismatch. One minor citation-echo imprecision in the recon (the hyphenated `last-modified` grep pattern vs the page's `Last modified:` text) — recorded, not blocking: the line, text, and date all verify.

---

## 3. Independent check of the scout's base-tip observation

```
$ git -C <L> rev-parse c78749a5
c78749a565dfd186f10a1d8ac98e19dac2429666
$ git -C <L> log -1 --format='%H %s' c78749a5
c78749a565dfd186f10a1d8ac98e19dac2429666 round-62 verifier spot-check (integrator, hyaku): non-author admit/reject
$ git -C <L> rev-parse c78749a5565dfd186f10a1d8ac98e19dac2429666
fatal: ambiguous argument ... unknown revision
```

The claims header prints `c78749a5565dfd…`; the repository's actual commit is `c78749a565dfd…`. Scout finding confirmed independently (read-only git only; no edit to the frozen file — a dated erratum is the L1's call).

---

## 4. Residual risk / verification gaps

- S229 is a live HTML page, not a content-addressed pin: its sha256 (`5b97cb7e…c453c4f`) is a point-in-time capture of 2026-11-03. The PEP's own `Last modified: 2025-08-20` footer is the stability anchor. Re-opened bytes match the scout's same-day capture exactly.
- S228 sits at an immutable commit pin; re-opening at `2fd12b88` must keep yielding these bytes (same-day double-open agrees).
- `pypi-server` collides on port 8080 with `nginx-request-logging` (same class) — relevant to C1's implementation, not to these two sources' verification.
- Quotes verified are the scout's recon quotes; all are ≤ 25 words (max 19).

## Verdicts

- **S228: verified** — sha matches the pin and the lane capture byte-for-byte; scout quotes verified (incl. the correctly-reported contiguous-string absence).
- **S229: verified** — layout text located (:144, :149, :165–:168) under h2 `Specification` (:140); scout quotes verified; one minor command-echo imprecision recorded (data correct).
