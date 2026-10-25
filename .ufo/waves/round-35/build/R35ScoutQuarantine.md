# R35ScoutQuarantine — S091 staged-quote presence (C2 D5 observation side)

Seat: R35ScoutQuarantine (scout, read-only). Wave: kengaku round 35 / hyaku run 7, 2026-10-25.
Scope: one question only — is the staged S091 quote (spot-check `corpus/lessons/round-34-verifier-spotcheck.md:64`)
present in the round-34 reopen capture and in a fresh live fetch of the NEC article?

No lane file was edited. No corpus/plans/SCORECARD/LOG/README/SKILL/PROVINCE/SHONEN write.
No `git add/commit/stash/checkout/reset/push`, no mutating `jj` command in the lane.
All scratch written under `.ufo/waves/round-35/build/R35ScoutQuarantine/`.
No tools installed (none needed — `curl`, `python3`, `sha256sum`, `diff` are stock).

---

## 0. The staged quote

Extracted mechanically from the S091 table row (`spotcheck.md:64`), the `「…」` span:

> ただし、RAKUDAベンチマークは1ターンの対話かつ少数データでの評価のため、対話性能の一側面しか測れていないことには注意が必要となります。

70 characters. It is byte-identical to the frozen constant `S091_QUOTE` in `plans/defect_ledger.py:96`
(checked by importing the module and comparing — `True`).

Command:
```
python3 - <<'EOF'
import re,importlib.util,pathlib
spec=importlib.util.spec_from_file_location("dl","plans/defect_ledger.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
sc=pathlib.Path("corpus/lessons/round-34-verifier-spotcheck.md").read_text()
row=[l for l in sc.splitlines() if l.startswith("| S091")][0]
q=re.findall(r"「([^」]+)」",row)[0]
print("ledger_const == spotcheck_quote:", m.S091_QUOTE==q)
print("quote_len:",len(m.S091_QUOTE))
EOF
```
Output:
```
ledger_const == spotcheck_quote: True
quote_len: 70
```

---

## 1. Method (the prescribed strip)

For each HTML input: `html.unescape` → `re.sub(r"<[^>]+>", "", raw)` → `re.sub(r"\s+", "", …)`, then
substring test of the whitespace-stripped quote. Implemented in
`.ufo/waves/round-35/build/R35ScoutQuarantine/probe_s091.py` (written by this seat, inside the allowed
build tree) — same order as `plans/defect_ledger.py:105-108`.

Raw-line location: the same per-line strip is applied to every raw line; the line whose stripped form
contains the quote is reported. Checked under two line-splitting conventions (`str.splitlines()`, which
also breaks on the 21 CRLF pairs, and `str.split("\n")`) — both give the same line number.

---

## 2. Result A — committed round-34 capture: **PRESENT**

Input: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/assimilation/captures/nec-s091-reopen.html`

```
$ python3 probe_s091.py <capture> corpus/lessons/round-34-verifier-spotcheck.md --raw-line
html_path=.ufo/waves/round-34/assimilation/captures/nec-s091-reopen.html
html_bytes=60314 raw_chars=50460
spotcheck_row_line=64 staged_quotes=1
  quote_len=70 present_in_stripped=True :: ただし、RAKUDAベンチマークは1ターンの対話かつ少数データでの評価のため、対話性能の一側面しか測れていないことには注
    raw_lines_containing=[276] flat_offset=10745 approx_raw_line=275
    approx_raw_line_from_hit=276
```

**Approximate raw-HTML line of the quote: line 276** (the quote begins mid-line-276, after the
`図4` figure lead-in; the flat-text offset is 10745 and the line-276 stripped segment starts at 10470).
The line-276 hit is identical under both split conventions, and the raw line contains the quote
verbatim (no tag between characters):

```
$ awk 'NR==276' .ufo/waves/round-34/assimilation/captures/nec-s091-reopen.html \
    | grep -c "ただし、RAKUDAベンチマークは1ターンの対話かつ少数データでの評価のため、対話性能の一側面しか測れていないことには注意が必要となります。"
1
```

### Byte-count reconciliation (why my probe prints 60314, not 60,335)

The spot-check says the capture is 60,335 B. Both are right — they measure different things:

```
$ wc -c .ufo/waves/round-34/assimilation/captures/nec-s091-reopen.html
60335
$ python3 -c "raw=open(p,'rb').read(); t=raw.decode(); print(len(raw), len(t), t.count('\r'), t.count('\r\n'), len(open(p,encoding='utf-8').read()))"
60335 50481 21 21 50460
```
The file holds **21 CRLF pairs**. Python text mode applies universal-newline translation (each
`\r\n` → `\n`, dropping 21 characters), so a text-mode read yields 50,460 chars / 60,314 re-encoded
bytes. The on-disk size is **60,335 B**, matching the spot-check's figure. The quote test is unaffected
either way (`\s+` strips both `\r` and `\n`).

### Manifest verification (required by the task)

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin \
  && sha256sum -c .ufo/waves/round-34/assimilation/captures/quarantine-SHA256SUMS
.ufo/waves/round-34/assimilation/captures/nec-s091-reopen.html: OK
.ufo/waves/round-34/assimilation/captures/geniac-s105-reopen.html: OK
exit=0
```
Both digests match the committed bytes. The manifest is committed (`git ls-files --error-unmatch` lists
both `nec-s091-reopen.html` and `quarantine-SHA256SUMS`); the capture was committed in `0b3c627`
("round-34: evaluator coverage attempt and calibration honest stop").

---

## 3. Result B — live re-fetch: **PRESENT** (with a caveat that is itself a finding)

Fetch (browser UA, `curl -sSL`), written to `.ufo/waves/round-35/build/R35ScoutQuarantine/nec-s091-live.html`:

```
$ curl -sSL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36" \
    -w "http_code=%{http_code} size=%{size_download} url=%{url_effective}\n" \
    -o nec-s091-live.html "https://jpn.nec.com/techrep/journal/g23/n02/230212.html"
http_code=200 size=60335 url=https://jpn.nec.com/techrep/journal/g23/n02/230212.html
exit=0
$ sha256sum nec-s091-live.html
985bd701349adee17801ebf2508e13a9f076fb9521d47f248ea9f582e4096e86  nec-s091-live.html
```

Probe on the live bytes:
```
$ python3 probe_s091.py nec-s091-live.html corpus/lessons/round-34-verifier-spotcheck.md --raw-line
html_path=nec-s091-live.html
html_bytes=60314 raw_chars=50460
spotcheck_row_line=64 staged_quotes=1
  quote_len=70 present_in_stripped=True :: ただし、RAKUDAベンチマークは1ターンの…
    raw_lines_containing=[276] flat_offset=10745 approx_raw_line=275
    approx_raw_line_from_hit=276
```
Live raw line **276** — same line number as the capture.

### Live vs committed capture: one differing line, and it is not content

```
$ diff .ufo/waves/round-34/assimilation/captures/nec-s091-reopen.html \
       .ufo/waves/round-35/build/R35ScoutQuarantine/nec-s091-live.html | grep -cE '^[0-9]'
1
$ python3 - <<'EOF'   # per-line comparison
differing line numbers: [82]
line 82 len 4262 4262   first diff col 2763
  capture: ... a="wpna3ulincqkm2w6jxea-f-90bfcf263-clientnsv4-s.akamaihd.net" ...
  live   : ... a="wpna3ulincqkm2w6looqq-f-d205be072-clientnsv4-s.akamaihd.net" ...
EOF
```
Exactly one differing line (82), of identical length, differing only in the Akamai `clientnsv4`
session/edge token inside a `<script>` blob. **The article text is byte-identical**; the two files
differ only by an ephemeral CDN token. This independently corroborates that the round-34 capture was a
genuine live capture of the same page.

### CAVEAT / falsifier-grade finding: the live endpoint is intermittently 403

The NEC edge (Akamai) serves a 418-byte "Access Denied" body for a large fraction of requests:

```
$ for i in $(seq 1 12); do curl -sSL -A "<browser UA>" -o /dev/null -w "%{http_code}\n" <url>; done
plain-UA: 200=7 403=5 of 12
```
Per-variant success counts over 3 requests each:
```
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64...'   200_count=1/3
UA='Mozilla/5.0 (compatible; Googlebot/2.1; ...'  200_count=0/3
UA='curl/8.6.0'                                   200_count=0/3
```
(The original Linux-Chrome UA succeeded 1/3 in the same batch and 7/12 in the larger batch.)
So the browser UA matters, and even with it the URL is served intermittently.

The 403 body is the *same* Akamai denial the round-34 lane captured, modulo the edge reference id:
```
$ diff <(python3 -c "import html;print(html.unescape(open('…/nec-s091.html').read()))") \
       <(python3 -c "import html;print(html.unescape(open('nec-s091-live-1.html').read()))")
7,8c7,8
< Reference #18.9df11502.1792954045.9b2b010
< <P>https://errors.edgesuite.net/18.9df11502.1792954045.9b2b010</P>
---
> Reference #18.9df11502.1792957392.9b8b308
> <P>https://errors.edgesuite.net/18.9df11502.1792957392.9b8b308</P>
$ wc -c …/nec-s091.html nec-s091-live-1.html
418 …/nec-s091.html
418 nec-s091-live-1.html
```
Round-34's `nec-s091.html` (418 B, Akamai "Access Denied") is thus **not** evidence that the article
is unavailable — it is a transient edge denial. The same URL served the full 60,335 B article within
seconds, repeatedly. This is the concrete mechanism behind the D5 disagreement: the round-34 refusal
("quote absent; 418-byte Access Denied") rested on one unlucky fetch.

**Operational consequence for the lane (freshness/calibration):** any NEC capture must be retried on
403 rather than recorded as an access failure; a 418-byte Akamai body is a *retry* signal, not a
*source outcome*. `nec-s091-live.html` (the 200 response) is retained in this seat's build tree as the
re-fetch evidence; `nec-s091-live-1.html` / `nec-s091-live-2.html` retain the 403 bodies.

---

## 4. Bearing on C2 / D5

The D5 check in `plans/defect_ledger.py:99-114` has an **observation side** (quote present in the
capture) and a **self-assessment side** (a round-34 erratum line + a round-35 `## Mistakes` S091 row).
Observed just now, at the current working tree:

| D5 component | state | evidence |
|---|---|---|
| observation: quote in `nec-s091-reopen.html` | **true** | §2 — `present_in_stripped=True`, raw line 276 |
| `corpus/lessons/round-34.md` erratum line | **present** (`erratum_lines=1`) | `corpus/lessons/round-34.md:45` — "Erratum (round 35): the staged S091 quote is present in this round's own reopen capture … (60,335 B; after tag-strip and whitespace removal, raw HTML line 276)" — my line number **276** and byte figure **60,335 B** both match the erratum exactly |
| `corpus/lessons/round-35.md` `## Mistakes` section with an S091 row | **absent** (`r35_mistake_row=False`) | `grep -n "^## " corpus/lessons/round-35.md` → only `7:## Gate`; the ledger's regex `^## Mistakes\n` matches nothing |

Ledger run at the current working tree (read-only invocation of the frozen checker):
```
$ python3 plans/defect_ledger.py --lane .
R34-D1 status=open observed=fail agree=yes untracked=5
R34-D2 status=open observed=fail agree=yes committed_mirror_paths=109413
R34-D3 status=open observed=pass agree=NO listed=6 evaluator_listed=True bad=0
R34-D4 status=open observed=pass agree=NO correction_lines=1
R34-D5 status=open observed=fail agree=yes erratum_lines=1 r35_mistake_row=False
rows=5 closed=0 observed_pass=2 mismatches=2
PREDICATE C2 fail
```
**D5's only remaining red is the missing round-35 `## Mistakes` row** — the observation side it guards
is now confirmed true by two independent routes (committed capture + live re-fetch). The erratum in
`round-34.md:45` is already correct and needs no edit from me.

Note for the L1: adding a `## Mistakes` section to `corpus/lessons/round-35.md` with a row containing
`S091` flips `r35_mistake_row` to true and turns D5 observed=fail → observed=pass; flipping the
ledger row `R34-D5` to `closed` in `corpus/defects.jsonl` is then required too, or the row becomes a
self-assessment mismatch (`status=open` with a passing check → `agree=NO`, `mismatches>0`).
Both are the L1's writes, not this seat's.

---

## 5. Axis read (calibration, freshness)

- **calibration — improved, materially.** The lane's own committed capture already falsifies the
  round-34 "quote absent" refusal, and the live URL independently confirms it. D5's observation side
  is verified twice over (committed bytes with manifest-verified digest; live 200 response). The
  round-34 refusal was a single unlucky 403 fetch mistaken for a source outcome.
- **freshness — improved.** Live re-fetch on 2026-10-25 returns HTTP 200 / 60,335 B; the article text
  is byte-identical to the 2026-10-25 round-34 capture except for one Akamai CDN token line. The
  source has not changed, so the staged quote remains valid today.
- **new falsifier-grade observation (unrecorded anywhere else):** the NEC URL is served intermittently
  (≈ 5/12 → 403 with a 418-byte Akamai body, ≈ 7/12 → 200 with the full article) and a non-browser UA
  (incl. `Googlebot`, `curl/8.6.0`) never succeeded. A capture harness that records the first response
  as final will produce false "unavailable" refusals on this source class. This is a reusable rule, not
  an S091 fact.

## 6. Unknowns / not established here

- Whether the D5 erratum wording and the pending round-35 `## Mistakes` row will satisfy the L1's
  own final counter wording — my check is the frozen ledger's own regex, so a differently-worded
  Mistakes row could still miss `S091` (the check requires a `|`-prefixed line containing `S091` inside
  a `## Mistakes` section).
- The Akamai denial's cause (bot heuristics, rate limit, geo) is not established; only its
  reproducibility and its 418-byte shape are.
- Nothing here was tested for S105 / GENIAC; out of scope.

## 7. Files written by this seat (all inside the allowed build tree)

- `.ufo/waves/round-35/build/R35ScoutQuarantine.md` — this report.
- `.ufo/waves/round-35/build/R35ScoutQuarantine/probe_s091.py` — the strip/presence probe.
- `.ufo/waves/round-35/build/R35ScoutQuarantine/nec-s091-live.html` — the HTTP-200 live capture (60,335 B, sha256 `985bd701…96e86`).
- `.ufo/waves/round-35/build/R35ScoutQuarantine/nec-s091-live-1.html`, `nec-s091-live-2.html` — the 403 denial bodies.
- `.ufo/waves/round-35/build/R35ScoutQuarantine/f1.html … f8.html` — the 8-request flakiness sample.
- `.ufo/waves/round-35/build/R35ScoutQuarantine/receipt.txt` — captured command/output receipt.

No `mktemp` clone was needed: every artifact read was read-only and every write was confined to the
seat's own build directory.

VERDICT: s091-quote-capture-present-live-present
