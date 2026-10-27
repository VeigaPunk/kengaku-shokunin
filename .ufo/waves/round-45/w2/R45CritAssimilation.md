# R45CritAssimilation — re-check of wave-1 R45MergeRescreen (kengaku round 45, wave 2, 2026-10-26)

Seat: critic, leaf. Read-only on lane and `/home/vgpnk/Projects/shokuknow`. Writes: this report +
`.ufo/waves/round-45/w2/R45CritAssimilation/` receipts. Scratch `/fast/scratch/hyaku/kengaku-r45/R45CritAssimilation`
held id files, guard output, fetches; removed via `plans/scratch_guard.py safe-rm`. Tooling installed: none.
Lane tip measured at `d4c0cdfbdc3886eadac4710ee49630ce00722ee1` (`git -C <lane> rev-parse HEAD`),
`corpus/SOURCES.md` clean in `git status` (no ` M` line) — the S149–S156 draft wave-1 saw uncommitted
has been integrated by the L1.

## 1. (a) id-collision command re-run — CONFIRMED, zero drift on pinned axes

Re-ran the same 0-3-space pipeline (`grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' | sort | wc -l`,
cwd=fleet root, 2026-10-26 ~23:52 -03):

```
$ grep -oE "$ANCH" <lane>/corpus/SOURCES.md        | sort | wc -l   → 149   (working tree)
$ git -C <lane> show HEAD:corpus/SOURCES.md | grep -oE "$ANCH" | sort | wc -l  → 149   (committed)
$ grep -oE "$ANCH" <shokuknow>/merge/kengaku/SOURCES.append.md | sort | wc -l  → 175   (staged)
$ comm -12 reg.ids staged.ids | wc -l                                    → 73
```

Guard re-run under the envelope (ENVELOPE lines verbatim):

```
ENVELOPE start 23:52:41 cwd=/home/vgpnk/Projects/shokunin
reg-ids=149 staged-ids=175 collisions=73
ENVELOPE end 23:52:43 exit=3 local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged
```

- Receipt sha256s **byte-identical to wave-1's**: `reg-ids` ba34916b…3f2da, `staged-ids`
  2df53989…f5e1c (same sha as round-40's pin — staged package unchanged since r40),
  `collisions` 1b311809…4da11; `corpus/SOURCES.md` sha `c716f43c…4af3e35` unchanged.
- Independent re-derivation of the range arithmetic on my own collision file:
  `S077-086=10 S090-094=5 S097=1 S100-156=57 other=[] sum=73`; registry = S001–S156 minus the
  same 7 gaps (S087,S088,S089,S095,S096,S098,S099) → 149. Wave-1's arithmetic correct.
- **The only drifted number is the committed registry**: wave-1 reported committed=141 @ HEAD
  `05b02e2` (pre-integration); now HEAD=`d4c0cdf`, committed=149 = working tree. This is exactly
  the integration wave-1's MEASUREMENT HAZARD warned about ("numbers must be re-taken at
  integration time"). Both numbers were right at their instants; current truth: **149/175/73
  both working tree and committed** — wave-1's working-tree pin was the durable one. No error.

## 2. (b) quarantine slice awk re-derived — CONFIRMED, k=2

Register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`:
sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833` (byte-identical to
wave-1/round-40's pin); last commit still `d4ab45f2`; clean in `git status`.

```
$ awk -F'|' '$2 ~ /kengaku/' <register>   → 3 lines: S091 + S105 data rows + `| `kengaku` | 2 |` summary
$ grep -nE '^\| `kengaku` \| round[0-9]+ \| S[0-9]{3,} \|' <register>
101:| `kengaku` | round2 | S091 | `payload-absent` | https://jpn.nec.com/techrep/journal/g23/n02/230212.html | `import re,html;s=open('/tmp/keng_s091.html',…;pri` | …
102:| `kengaku` | round3 | S105 | `payload-absent` | http://web.archive.org/web/20251118034714/…/result_1/index.html | `指定されたページまたはファイルは存在しません` | …
$ sed -n '256,375p' <register> | grep -ci kengaku   → 0   (NEVER-CHECKED section clean)
$ grep -nE '^\| *`?kengaku`? *\| [0-9]+ \|' <register>   → 252:| `kengaku` | 2 |
```

k=2 confirmed (S091 round2, S105 round3); by-lane table agrees. Minor cosmetic note, not a defect:
wave-1's receipt `quarantine-kengaku.rows` (sha e4f90ad4…0890) holds the **broad-awk 3-line output**
while their text described the precise grep beside it; my receipt (sha bdb89763…f77) holds the
precise-grep 2-line output. Both support k=2; flagging only so later readers are not surprised by
the sha mismatch.

## 3. (c) hand-check of ONE MORE row — S091 (wave-1 formally checked S105; S091 was 403 for them)

Wave-1's `curl -sS -L` (no UA) got `http=403 bytes=416` and could only prove the substring property.
I re-fetched with a browser UA under the envelope:

```
ENVELOPE start 23:53:03 cwd=/home/vgpnk/Projects/shokunin
http=200 bytes=60334 url=https://jpn.nec.com/techrep/journal/g23/n02/230212.html
ENVELOPE end 23:53:06 exit=0 local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged
$ sha256sum s091-nec.html  → dc392edfb982dc0fc91ea6073a49d71be84aece1e6bfaeb91d804a615bd3ec05
$ grep -oE '<title>[^<]*' s091-nec.html
<title>日本語性能に優れたNECの大規模言語モデル（LLM）: Vol.75 No.2: ビジネスの常識を変える生成AI特集 … | NEC
$ grep -c -F "import re,html;s=open('/tmp/keng_s091.html',…;pri" s091-nec.html   → 0
```

The fetched page is the genuine article (NEC LLM technical report, Vol.75 No.2; markers `230212`×11,
`NEC`×52, `技報`×10), matching the round-29 scout's 200/60,335 B vs the seat's 403/418 B — the WAF
flapping wave-1 documented is UA-sensitive, not dead. **The registered quote occurs 0 times in the
live article's real bytes**: the register's `payload-absent` absence-claim now holds on the cited
source itself, upgrading wave-1's "uncheckable live" to checked.

Re-derived the substring proof wave-1 reported (121-byte span incl. newline, offset 119 of a
356-byte line):

```
$ wc -c s091-line43.txt s091-quote.txt   → 356 / 121
$ grep -boF -f s091-quote.txt s091-line43.txt   → 119:import re,html;s=open('/tmp/keng_s091.html',…;pri
```

Byte-exact — the quote is a mechanical 120-char slice of the lane's own scraper code in
`shokuknow/lanes/kengaku/round2/SOURCES-PROPOSED.md:43`; it could never appear in the article
(now verified on real bytes). Honest class remains quote-column misbinding; `payload-absent`'s
fabrication reading still not confirmable. **Verdict for S091: refuse, adopt nothing — same
disposition as wave-1, now on stronger evidence** (live page fetched and quote located-absent
rather than unreachable).

## 4. Drift ledger vs wave-1's reported numbers

| axis | wave-1 reported | measured now | drift? |
|---|---|---|---|
| reg-ids (working tree) | 149 | 149 | none — sha-identical |
| staged-ids | 175 | 175 | none — sha-identical to r40 too |
| collisions | 73 | 73 | none — sha-identical |
| committed reg-ids | 141 @ 05b02e2 | 149 @ d4c0cdf | predicted integration landing; both right at their instants |
| quarantine k | 2 (S091, S105) | 2 | none |
| S091 live fetch | 403/416 B | 200/60,334 B | WAF flapped as wave-1 noted; new evidence supports their verdict |

## 5. Receipts (`.ufo/waves/round-45/w2/R45CritAssimilation/`, all < 1 MiB)

`reg-ids` ba34916b…3f2da · `staged-ids` 2df53989…f5e1c · `collisions` 1b311809…4da11 ·
`quarantine-kengaku.rows` bdb89763…f77 · `s091-nec.html` dc392edf…ec05 (60,334 B) ·
`s091-quote.txt` 4809e6a9…b24d (121 B) · `s091-line43.txt` 96948ffd…fb2 (356 B).
Every envelope run: `local_bin_content before=after=e396f23e40a69201 unchanged`; zero INVALID.

VERDICT: rescreen-confirmed-yes-row-verdict-S091-quote-absent-from-live-page-refuse-adopt-nothing
