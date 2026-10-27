# R45ExecCensusPost — post-landing census + row-count delta (round 45, wave 2, FALSIFY)

Seat: executor, leaf. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (read only; nothing written in the lane).
Lane tip measured: git `d4c0cdfbdc3886eadac4710ee49630ce00722ee1`, jj `ywrsrquz` (2026-10-26 23:51).
Baseline for the delta: the frozen-claims starting tip `9d5f9715ebb0343984171be312d44e681f96b9a8` (`plans/round-45-claims.md:3`),
read read-only through `git show`. All receipts: `.ufo/waves/round-45/w2/R45ExecCensusPost/`.

## 1. Census validate on the lane tip (under the mandatory envelope)

Command (cwd `/home/vgpnk/Projects/shokunin`, `TMPDIR=$S`):

```
$ /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh \
    "$S/env" /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --root /home/vgpnk/Projects/shokunin kengaku
```

ENVELOPE lines (QUALITY Q32), verbatim:

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45ExecCensusPost/env /fast/scratch/hyaku/kengaku-r45/R45ExecCensusPost/env --bind /fast/scratch/hyaku/kengaku-r45/R45ExecCensusPost/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
ENVELOPE start 23:51:30 cwd=/home/vgpnk/Projects/shokunin
... 15 W04 lines + final ok line, see tail ...
ENVELOPE end 23:51:32 exit=0 local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged
```

Tail (the last 3 registry lines of the receipt):

```
kengaku	W04	S076 duplicate url docs.python.org/3/library/json.html across scopes
kengaku	W04	S100 duplicate url github.com/laude-institute/terminal-bench-2 across scopes
kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
```

**exit = 0** (`envelope-rc=0`; envelope did not fire exit 4: `local_bin_content_before` = `...after` = `e396f23e40a69201`, `unchanged`).
15 `W04` warnings, all pre-existing (see §5 — the finding-code set is byte-identical to `claims/census-before.txt`).
No `E01`–`E12` code appears, so: no malformed row, no bad id, **no duplicate id (E03)**, no duplicate URL+scope (**E04**),
no enum violation, no `used-by` path missing on disk (E11), no row-shaped source outside `## Registry` (E12).
Full receipt: `R45ExecCensusPost/validate-receipt.txt` (sha256 `8efdf646…ff3623`).

## 2. Row count — 149

```
$ grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md
149
```

Independent agreement from the counter itself (`census` mode, same envelope, `exit=0`,
`local_bin_content_before=e396f23e40a69201 after=e396f23e40a69201 unchanged`, start 23:52:11 end 23:52:13):

```
kengaku	rows	149
FLEET	rows	149
FLEET	tier.A	125   FLEET.tier.B 22   FLEET.tier.C 2   FLEET.tier.invalid 0
FLEET	status.queued	8   FLEET.status.mined 133   FLEET.status.rejected 8   FLEET.status.invalid 0
FLEET	missing	0
```

Receipt: `R45ExecCensusPost/census-mode-receipt.txt`.

## 3. Knowledge-file count — 52

```
$ find /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge -name '*.md' | wc -l
52
```

`tb2-password-recovery-grader.md` is tracked at the tip: `100644 blob 6efbf8d78ee73679ced4a1b45b734e2881d61fc9 corpus/knowledge/tb2-password-recovery-grader.md`.

## 4. Duplicate-id check (round-prompt pattern) — none

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]{3,}' | sort | uniq -d
(no output)
$ ... | sort -u | wc -l
149
```

149 rows, 149 distinct ids. Id gaps `S087 S088 S089 S095 S096 S098 S099` are **pre-existing**: `comm` of
`seq S001..S148` against the baseline blob returns exactly the same seven ids, so round 45 introduced no gap and closed none.

## 5. Row-count / content delta vs the frozen baseline tip

```
$ git -C <lane> show 9d5f9715…:corpus/SOURCES.md | grep -cE '<row pattern>'
141
$ git -C <lane> ls-tree -r --name-only 9d5f9715… -- corpus/knowledge | grep -c '\.md$'
51
```

| metric | baseline `9d5f9715` | tip `d4c0cdf` | delta |
|---|---|---|---|
| registry rows | 141 | 149 | **+8** (S149–S156, contiguous, all present) |
| knowledge `.md` | 51 | 52 | **+1** |
| kind `code` | 41 | 49 | +8 |
| kind paper/docs/dataset/own-work/tool/spec | 42/40/4/6/3/5 | 42/40/4/6/3/5 | 0 |
| status mined / rejected / queued | 125/8/8 | 133/8/8 | +8 mined, 0 new rejected/queued |
| validate finding codes | 15×W04 | 15×W04 | **0 new** (`diff` rc=0) |

Pre/post warning diff (ENVELOPE lines stripped):

```
$ diff <(grep -v '^ENVELOPE' claims/census-before.txt) <(grep -v '^ENVELOPE' validate-receipt.txt)
diff-rc=0 (identical); W04 lines: 15
```

So the eight new rows added exactly one new knowledge file, no tier-C, no rejected row, and no new duplicate-URL or
enum finding — the delta is clean against the contract, not merely non-fatal.

## 6. New rows S149–S156 integrity (independent parse, read-only)

`R45ExecCensusPost/rows-fields.txt` (sha256 `4fce9022…d70737`):

```
rows parsed: 149
S149 nf=13 tier=code status=mined opened=2026-10-26 recheck=180d used-by=corpus/knowledge/tb2-password-recovery-grader.md exists=True url-shared-with=none
S150 … (same, all eight)
S156 nf=13 tier=code status=mined opened=2026-10-26 recheck=180d used-by=corpus/knowledge/tb2-password-recovery-grader.md exists=True url-shared-with=none
S149..S156 all present: True
distinct ids: 149
```

All eight: NF=13, `kind=code`, `tier=A`, `status=mined`, `opened=2026-10-26`, `recheck=180d`, `used-by` resolves on disk,
no URL shared with any other row (consistent with the absence of new `W04`). S147/S148 (round-44 admissions) also resolve
their `used-by` to `corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md`.

## 7. Findings, risks, limits

- **No defect found in the census surface.** The claim "rows 149 / knowledge 52 / no duplicate ids / validate ok" holds on
  the lane tip, measured under the envelope with an unchanged `~/.local/bin` content digest.
- W04 (`S040, S048, S057–S059, S064–S069, S071, S075, S076, S100`) is a warning class the contract says never affects
  status; the set is unchanged by round 45, so it cannot be attributed to this wave.
- Limits: `validate` was run for the `kengaku` lane only (the fleet's other lanes were out of scope and remain unmeasured
  here); the baseline comparison reads `git show`, i.e. committed blobs, not the baseline working tree — correct here
  because the frozen claims name that commit as the starting tip.
- The lane working tree carries other seats' untracked/modified files under `.ufo/waves/round-45/`; they do not touch
  `corpus/` or `plans/`, and my only writes were under `.ufo/waves/round-45/w2/R45ExecCensusPost/`.

Consolidated output of every command above: `R45ExecCensusPost/census-final.txt` (sha256 `2d1655f4…c66964`, 7.2 KB).

VERDICT: census-final-ok-yes-rows-149
