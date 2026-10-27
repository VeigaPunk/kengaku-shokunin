# R45MergeRescreen — assimilation rescreen (kengaku round 45, wave 1, 2026-10-26)

Seat: reviewer, leaf. Read-only on both repos: no lane file other than this report and my receipt dir
was created, edited or deleted; `/home/vgpnk/Projects/shokuknow` was only read plus two outbound
HTTP GETs. Writes: this report and
`.ufo/waves/round-45/w1/R45MergeRescreen/` (receipt copies listed in §5). Scratch
`/fast/scratch/hyaku/kengaku-r45/R45MergeRescreen` held the fixtures and fetches; removed at the end.
Tooling installed: none (pacman untouched).

The round-45 claims file (`plans/round-45-claims.md`, read in full) and the round-40 predecessor
report (`.ufo/waves/round-40/build/R40MergeRescreen.md`) were used as the method baseline; the same
guard script is re-driven so numbers stay comparable.

## 1. (a) id-collision check — exactly per the round prompt

Command (the prompt's own pipeline; run at cwd=fleet root, 2026-10-26 ~23:33 -03):

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <lane>/corpus/SOURCES.md | sort | wc -l
141
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <shokuknow>/merge/kengaku/SOURCES.append.md | sort | wc -l
175
$ comm -12 reg.ids staged.ids | wc -l
65
```

**The registry moved under the check.** The same pipeline re-run minutes later (and the round-36
guard script, §2) prints:

```
$ A=<scratch>/guard-real sh <lane>/.ufo/waves/round-36/assimilation/id-collision-check.sh
reg-ids=149 staged-ids=175 collisions=73        (exit=3, as designed)
```

| instant (2026-10-26 -03) | reg-ids | staged-ids | collisions | pinned by |
|---|---|---|---|---|
| ~23:33 | 141 | 175 | 65 | first pipeline run; ids S001–S148 |
| 23:35–23:38 | **149** | **175** | **73** | guard run + re-run; raw id set `diff`-equal to guard `reg-ids` (`raw-pipeline ids == guard reg-ids`) |

- The +8 delta is exactly **S149, S150, S151, S152, S153, S154, S155, S156**
  (`comm -13 old new` output, verbatim). `git -C <lane> diff -U0 -- corpus/SOURCES.md` shows exactly
  8 added rows `+| S149 |` … `+| S156 |`, 0 removed — all eight are this round's frozen C2 rows
  (tb2-password-recovery captures; S149 = tests/test_outputs.py, S156 = task.toml). They are the
  L1's **uncommitted working-tree draft** (`git status --short` → ` M corpus/SOURCES.md`); the
  committed registry at HEAD `05b02e2` ends at S148.
- Range arithmetic (checked from the id files): reg S001–S156 minus gaps
  S087/S088/S089/S095/S096/S098/S099 → 149 ✓ (committed state: minus the same 7 gaps → 141 ✓).
  staged S077–S251 contiguous → 175 ✓. Collisions = S077–S086 (10) + S090–S094 (5) + S097 (1) +
  S100–S156 (57) = **73** ✓ (committed: S100–S148 = 49 → 65 ✓).
- **Package is unchanged since round 39/40:** `staged-ids` sha256
  `2df53989ae5ab5c4f698f7ed459310a9a376cd970240e7483aeed40c3cdf5e1c` — byte-identical to the
  `2df53989…5e1c` recorded in `R40MergeRescreen.md` §2. So collisions 37→73 since round 40 are
  entirely registry-side: S121–S148 landed in rounds 41–44 (+28) and S149–S156 are this round's
  draft (+8).
- The 8 new collisions are pure id clashes with unrelated staged rows: lane S149 = "Terminal-Bench
  2.0 password-recovery grader" (`corpus/SOURCES.md:164`) vs staged S149 = "SkillEvaluator
  CHANGELOG" (`SOURCES.append.md:79`). **Floor for any later staged-row adoption: renumber past
  S156** (r40 said S120).

Sources & frontier line inputs: **reg-ids=149, staged-ids=175, collisions=73** (working tree,
sha256 of `corpus/SOURCES.md` = `c716f43c00eb467e4494c09fc9df54b75340f0580e6b909daff8d32de4af3e35`;
committed-state numbers 141/175/65).

MEASUREMENT HAZARD (for the L1): the registry is a concurrently-drafted uncommitted file; these
numbers must be re-taken at integration time and will drift while the wave lands. One observed
oddity I could not resolve and do not paper over: the file mtime reads
`2026-10-26 23:30:02.744 -0300`, which *predates* my first (141) read, yet the id set changed
between reads. The 8-row diff and the two pinned counts are ground truth; the mtime is not a
reliable landing marker under this tree.

## 2. (b) guard proof on a scratch fixture — indented `  | S002 |` row

Guard: `.ufo/waves/round-36/assimilation/id-collision-check.sh` (anchor
`^ {0,3}\|[[:space:]]*S[0-9]{3,}`; exit 3 collisions, 2 input absent/anchor-silent). Its `--selftest`
hard-codes `/tmp`, so per round-40 precedent the identical fixture was built under scratch and run
through the real script. Fixtures (copied to my receipt dir, §5):

```
reg.md     : "  | S002 | indented collision bait | code |" + "| S900 | control | code |"
staged.md  : "| S002 | staged twin | code |" + "| S901 | no twin | code |"
indent.md  : "    | S003 | four-space code row | code |" + "   | S004 | three-space row | code |"
```

Runs (all under the round-45 envelope; ENVELOPE lines verbatim, local-bin digest
`c263b11afb1cccf6` unchanged on every run — no INVALID):

```
ENVELOPE start 23:35:21 cwd=/home/vgpnk/Projects/shokunin
reg-ids=2 staged-ids=2 collisions=1
ENVELOPE end 23:35:23 exit=3 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
$ cat $S/guard-fix1/collisions
S002
```
→ **the 2-space-indented `  | S002 |` row IS caught** (exit 3, collision = S002). Mechanism:
`ids_of` re-extracts bare `S[0-9]{3,}` after the anchor grep, normalizing indentation before
`comm`; the negative control shows the danger it guards — a bare `^[|]` anchor on the same reg.md
sees only `S900` and would silently miss the collision.

```
ENVELOPE start 23:35:24 … ENVELOPE end 23:35:26 exit=0 … unchanged   (indent edge)
reg-ids: S004
```
→ 4-space `    | S003 |` is not parsed (excluded deliberately), 3-space `   | S004 |` parses.

```
ENVELOPE start 23:33:52 … ENVELOPE end 23:33:54 exit=2 … unchanged
REFUSED: input absent: …/fixture/nope
```
→ a missing registry **refuses** (exit 2) where the bare prompt pipeline would false-green
`grep→empty, comm→0, exit 0`.

Operational note (F1): my first real-input guard run under the envelope failed because `A=` pointed
into the lane tree — inside bwrap `/home/vgpnk` is read-only (`reg-ids: Read-only file system`,
script REFUSED exit 2). Not a measurement; re-run with `A=` in scratch produced §1's counting run
(ENVELOPE start 23:35:21 / end 23:35:23, digest unchanged). **Under the envelope, the guard's
`A=` receipt dir must live outside `/home/vgpnk`.**

## 3. (c) quarantine slice — lane `kengaku`

Register `/home/vgpnk/.ufo/…` — exact path
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`, sha256
`5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833` = byte-identical to round 40's
`5afe1810…d833`; last commit `d4ab45f2` (unchanged). Data-row extraction (broad awk
`-F'|' '$2 ~ /kengaku/'` returns **3** lines: the 2 data rows + the by-lane summary
`| \`kengaku\` | 2 |`; precise data-row grep):

```
$ grep -nE '^\| `kengaku` \| round[0-9]+ \| S[0-9]{3,} \|' <register>
101:| `kengaku` | round2 | S091 | `payload-absent` | https://jpn.nec.com/techrep/journal/g23/n02/230212.html | `import re,html;s=open('/tmp/keng_s091.html',…;pri` | …
102:| `kengaku` | round3 | S105 | `payload-absent` | http://web.archive.org/web/20251118034714/https://www.meti.go.jp/policy/mono_info_service/geniac/selection_1/result_1/index.html | `指定されたページまたはファイルは存在しません` | …
```

**k = 2 quarantine rows** (by-lane table agrees: `| \`kengaku\` | 2 |`; the NEVER-CHECKED section
contains 0 kengaku lines: `sed -n 256,375p | grep -ci kengaku` → 0). Hand-check performed on
**S105** (formal fetch + quote locate); S091 verified to the extent possible without the live page.

### S105 (round3) — hand-checked, verdict: register's absence-claim holds for today's bytes; class payload-absent NOT confirmable as fabrication; error-shell/misbinding candidate. Adopt nothing.

```
$ curl -sS -L -o s105-snapshot.html -w 'http=%{http_code} bytes=%{size_download} url=%{url_effective}\n' --max-time 120 'http://web.archive.org/web/20251118034714/https://www.meti.go.jp/policy/mono_info_service/geniac/selection_1/result_1/index.html'
http=200 bytes=13027 url=http://web.archive.org/web/20251118034714/https://www.meti.go.jp/policy/mono_info_service/geniac/selection_1/result_1/index.html
$ sha256sum s105-snapshot.html
15a6622f07993a41550d448befdac6cfc9c3ba50561bd850d8647965e87b7003
$ grep -c -F '指定されたページまたはファイルは存在しません' s105-snapshot.html
0
$ grep -oE '<title>[^<]*' s105-snapshot.html
<title>​GENIAC事業 第1期 性能評価結果公開 （METI/経済産業省）
$ grep -c '性能評価結果' s105-snapshot.html   → 10      $ grep -ci geniac → 20
```

The cited snapshot today serves the genuine METI page (title = GENIAC 第1期 性能評価結果公開; the
性能評価結果 section the round-29 seat located is present), and the registered quote — the page's
error-shell text — occurs **0** times in it. So the row's quoted span is indeed absent from the
cited bytes (the register's own claim), but the source itself is reachable and real: a corrected
quote is available and the `payload-absent` "fabrication class" reading is **not** confirmable.
This matches the round-29 finding (`R29a2QuarS105.md`: census lifted a quoted span from an
explanatory sentence — quote-column misbinding). Verdict: stay quarantined; refuse the row; adopt
nothing.

### S091 (round2) — verdict: live source unreachable (403); registered quote proven to be a mechanical slice of the lane's own scraper command; not a verifiable fabrication. Adopt nothing.

```
$ curl -sS -L -o s091-nec.html -w 'http=%{http_code} bytes=%{size_download} url=%{url_effective}\n' --max-time 120 'https://jpn.nec.com/techrep/journal/g23/n02/230212.html'
http=403 bytes=416 url=https://jpn.nec.com/techrep/journal/g23/n02/230212.html
```
Live fetch refused today (WAF; same flapping round 29 saw: scout 200/60,335 B vs seat 403/418 B),
so the quote cannot be hand-checked against the article today. What IS provable locally: the
registered span (121 bytes with newline, i.e. the renderer's 120-char cut) is a **byte-exact
substring of `shokuknow/lanes/kengaku/round2/SOURCES-PROPOSED.md:43`** —

```
$ grep -boF -f s091-quote.txt s091-line43.txt
119:import re,html;s=open('/tmp/keng_s091.html',encoding='utf-8',errors='replace').read();s=re.sub(r'(?s)<[^>]+>',' ',s);pri
```

— i.e. Python code (offset 119 inside the 356-byte line). Code cannot appear verbatim in an HTML
article, so a literal-match failure is guaranteed by construction; `payload-absent`'s fabrication
reading is inapplicable; the honest class is quote-column misbinding (plus unreachable-today).
Same disposition as `R29a2QuarS091.md` (mechanical slice, corrected quote available). The entries
citing these rows (`cjk-eval-journal-access` S091, `cjk-benchmark-governance-2026-10-23` S105) are
already REFUSE verdicts in the carried `entry-verdicts.tsv`; nothing observed today moves any of
the 65 entry verdicts (package bytes identical to r40).

## 4. Verdicts per quarantine row (both rows, nothing adopted)

| row | cited source today | registered quote vs cited bytes | verdict |
|---|---|---|---|
| kengaku round2 S091 | 403 / 416 B (WAF) | uncheckable live; quote proven a 120-char slice of `SOURCES-PROPOSED.md:43` code | misbinding-by-construction, live-unreachable; not a confirmed fabrication; refuse, adopt nothing |
| kengaku round3 S105 | 200 / 13,027 B, sha `15a6622f…7003`, real GENIAC 性能評価結果 page | quote occurs 0× in fetched bytes | register's absence-claim holds for today's bytes; error-shell misbinding, corrected quote available; refuse, adopt nothing |

## 5. Receipts (this dir; none over 1 MiB)

`reg-ids` ba34916b…3f2da (149), `staged-ids` 2df53989…f5e1c (175), `collisions` 1b311809…4da11 (73)
— sha256 as printed by `sha256sum` in the run log; `quarantine-kengaku.rows`
e4f90ad4…0890; `s105-snapshot.html` 15a6622f…7003; `s091-nec.html` 9186ec21…a6bd;
`fixture/{reg.md 53e45936…, staged.md 328aa57f…, indent.md 650933fc…}`. All envelope runs:
`local_bin_content before=after=c263b11afb1cccf6 unchanged`; zero INVALID measurements. Scratch
removed with `plans/scratch_guard.py safe-rm`.

Unresolved / verification gaps: NEC page content unverifiable today (403 — no lane property
depends on it); the registry mtime vs observation mismatch (§1) unresolved and disclosed; entry
verdicts carried unchanged from round 40 on byte-identity, not re-derived.

VERDICT: merge-rescreen-collisions-73-quarantine-2-rows
