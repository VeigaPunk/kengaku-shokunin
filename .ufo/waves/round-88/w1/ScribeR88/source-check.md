# ScribeR88 — S277 source re-open and gate-record check (round 88, wave 1, frontier step)

Seat: ScribeR88 (leaf; no subagents). Read-only against production files. Scratch under
`/fast/scratch/hyaku/kengaku-r88/ScribeR88/`, deleted before yield. Lane HEAD at check time:
`d9cb2b40b58358abbd54beb3250f53761ef03a8a`. Measured tip `7fcc680b86599eedd63e862a061848298428b3cc` and
frozen commit `0220c2f9f356bf032bd58b4ed39e32f6e26fa440` are both ancestors of HEAD (`git merge-base --is-ancestor`).
Tools installed or upgraded: none.

## Checks

| # | Check | Evidence (command / observed) | Result |
|---|---|---|---|
| 1 | Live re-open of the pinned grader | `curl -sSL -o "$S/fix-git-test_outputs.py" -w '%{http_code} %{size_download}' https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/fix-git/tests/test_outputs.py` → `200 1194`, curl rc 0. `sha256sum` → `a8a6f51eb0d7c4ebdf0813c8f0b645edf29c995f1f9faf2aca3886a6713043f3`. `wc -c` → 1194. | PASS |
| 1b | Byte comparison with round-52 capture | `cmp "$S/fix-git-test_outputs.py" corpus/evidence/round52/graders/fix-git/tests/test_outputs.py` → silent, rc 0. Capture hash matches `corpus/evidence/round52/graders/SHA256SUMS:62`. | PASS |
| 2a | Quote appears verbatim at cited line | `sed -n 19p` → `    assert hash_file(path_a) == hash_file(path_b), (`; `grep -qF` of `assert hash_file(path_a) == hash_file(path_b), (` on line 19 → match. S277 cites `test_outputs.py:19`. | PASS |
| 2b | Quote ≤ 25 whitespace-split words | `printf '%s' "$Q" \| wc -w` → 5 | PASS |
| 2c | Quote carries no `\|` | `grep -c '|'` on the quote → 0 | PASS |
| 3a | Registry row has 11 cells between outer pipes | `awk -F'|' '/^\| S277 /{print NF}'` → 13 (2 empty outer fields + 11 cells: id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by). Header at `corpus/SOURCES.md:21` has the same 11 columns. | PASS |
| 3b | Legal enum values | tier `A`; kind `code` (in `sources-census.sh` E05 list); status `mined` (in E07 list). | PASS |
| 3c | Recheck format | `180d` (NNd form); `validate` reports no E09 for S277. | PASS |
| 3d | used-by path exists | `corpus/lessons/round-88.md` present (`test -f`). | PASS |
| 3e | Lesson Gate table agrees with row | Gate table row (lesson line 27): id `S277`, decision "admit, A … (member replay only)" (row: tier A, scope "member replay only"); URL identical to row (`grep -cF` = 1 in each file); access date `2026-11-05` in both; quote `assert hash_file(path_a) == hash_file(path_b), (` at line 19, identical in both, "5 words, ≤25" consistent. | PASS |
| 3f | Registry changed from base only by the new row | `git diff --numstat 801b903a HEAD -- corpus/SOURCES.md` → `1 0`. Only added line is the S277 row; no removed lines. Consistent with lesson claim that no existing row's status, recheck or used-by changed. | PASS |
| 4a | Dated pointer to round-87 spot-check (V3) | Round-87 spot-check `corpus/lessons/round-87-verifier-spotcheck.md:127` (V3) asks for a dated pointer appended in the round-88 lesson. Lesson Gate (lines 21–23) carries it: `corpus/lessons/round-87-verifier-spotcheck.md` "committed 801b903a, 2026-11-05". File exists and is in base `801b903a` (`git cat-file -e`); `801b903a` commit date `2026-11-05T02:06:08-03:00`. | PASS |
| 4b | Census figures recount | Command: `awk -F'\|' '/^## Registry/{r=1;next} /^## /{r=0} r && /^\| *S[0-9]+ *\|/ { t=$5; s=$9; gsub(/ /,"",t); gsub(/ /,"",s); n++; if(t=="A")a++; if(s=="mined")m++ } END{printf "rows=%d A=%d mined=%d\n", n,a,m}'` on `git show 801b903a:corpus/SOURCES.md` → `rows=268 A=238 mined=243`; on `git show HEAD:corpus/SOURCES.md` (and working tree, clean vs HEAD) → `rows=269 A=239 mined=244`. Lesson figures 268→269, A 238→239, mined 243→244 match. Cross-check: `sources-census.sh census --root /home/vgpnk/Projects/shokunin kengaku` → rows 269, tier.A 239, status.mined 244, rejected 17, queued 8; base copy via `--file` → 268 / 238 / 243 / 17 / 8. Lesson's "rows added by tier: A 1" consistent with 3f. | PASS |
| 5 | Census validate exit code | `sh scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → **rc 0**. Output: 0 E-lines; 30 W-lines, all W04 (same URL across scopes) for other rows, none for S277; final `kengaku ok …/kengaku-shokunin/corpus/SOURCES.md`. Output copied to `sources-census-validate.tsv` in this directory. | PASS |

## Findings

1. **Cosmetic, outside the Gate section (defect, not a check failure).** `corpus/lessons/round-88.md` line 33
   begins `Considerthese: no unimplemented proposal …` with no space after the `Considerthese` label. Not in the
   Gate table, no check depends on it; reported only, not edited (production file).

## Observations (not defects)

- The S277 row, the Gate row and the grader bytes agree on every cited fact (id, URL, access date, quote,
  line, word count, byte hash, tier, scope, status, used-by).
- Lane HEAD `d9cb2b40` is two commits past the measured tip `7fcc680b` (`d9cb2b40` wave-1 spec, `0f6ea1de`
  L1 transcripts). I did not check whether those commits change anything other than the transcripts and
  wave spec; the registry diff against base is one added row at HEAD.
- Process note: my first census recount omitted `-F'|'` and returned nonsense; it was discarded. Every figure
  above comes from the `-F'|'` rerun.

## Receipts

- `sources-census-validate.tsv` (validate stdout, rc 0), `sources-census-validate.stderr` (empty).
- Fetch record: HTTP 200, 1194 bytes, sha256 `a8a6f51eb0d7c4ebdf0813c8f0b645edf29c995f1f9faf2aca3886a6713043f3`,
  `cmp` silent against `corpus/evidence/round52/graders/fix-git/tests/test_outputs.py`.

SEAT ScribeR88 VERDICT FINDINGS findings=1
