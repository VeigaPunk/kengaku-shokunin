# R36ReopenPins — independent re-open of the C2 Terminal-Bench pin (wave 1)

Seat: R36ReopenPins (executor, leaf). Lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin.
Frozen pin under test: `harbor-framework/terminal-bench-2` @ `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, path `regex-log/`.
All fetches performed 2026-10-26T01:11Z with `curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0 OpenSSL/3.6.5`.
Scratch: `.ufo/waves/round-36/build/R36ReopenPins/` (fetched bytes retained there). No lane file written; no git mutating command run.

## Axes

- **A1 freshness** — are the pinned bytes still what upstream serves at the pinned commit, and has `main` moved?
- **A2 identity** — do the bytes equal the lane's evidence captures, and does the receipt manifest actually verify?
- **A3 independent proof** — do the bytes match the commit-timestamped Git object graph (not just the same HTTP path)?
- **A4 scope** — does the pin cover the files the claim names (S108/S109/S110 + task.toml + oracle solve.sh), no more, no less?

## A1 — commit exists, with date and message

```
$ curl -fsSL https://api.github.com/repos/harbor-framework/terminal-bench-2/commits/2fd12b88aafdd04a52c298e3940bcb189f9766d6
sha            2fd12b88aafdd04a52c298e3940bcb189f9766d6
committer date 2026-04-30T05:53:30Z   (author date 2026-04-30T05:53:30Z)
message        'Add task metadata to task manifests'
```
(The commit object's top-level `tree` key is `null` in this API response payload; the tree sha was not needed because the recursive tree listing below is addressed by commit sha directly and returned `truncated=false`.)

Commit **exists**, dated **2026-04-30T05:53:30Z**, message **"Add task metadata to task manifests"**. Recorded.

## A1 — regex-log tree at the pinned commit

```
$ curl -fsSL "https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88...?recursive=1"
truncated False  entries 1446
type  size  path
blob   177  regex-log/.gitignore
blob  2075  regex-log/README.md
tree     -  regex-log/environment
blob   201  regex-log/environment/Dockerfile
blob  1021  regex-log/instruction.md
tree     -  regex-log/solution
blob   485  regex-log/solution/solve.sh
blob   989  regex-log/task.toml
tree     -  regex-log/tests
blob   608  regex-log/tests/test.sh
blob  3730  regex-log/tests/test_outputs.py
count 11 (8 blobs, 3 trees)
```
Sizes of the five pinned files agree exactly with the fetched bytes (see A3). The tree contains no `tests/` subdirectory beyond `test.sh`/`test_outputs.py`, so the claim's capture set is the full graded surface of the task.

## A2 — byte identity against the lane's evidence captures (5/5)

```
$ cd .../.ufo/waves/round-36/build/R36ReopenPins
  (fetched with curl -fsSL .../regex-log/{tests/test_outputs.py,tests/test.sh,instruction.md,task.toml,solution/solve.sh})
IDENTICAL tests_test_outputs.py == corpus/evidence/round36/tb2-regex-log/test_outputs.py
IDENTICAL tests_test.sh        == corpus/evidence/round36/tb2-regex-log/test.sh
IDENTICAL instruction.md       == corpus/evidence/round36/tb2-regex-log/instruction.md
IDENTICAL task.toml            == corpus/evidence/round36/tb2-regex-log/task.toml
IDENTICAL solution_solve.sh    == corpus/evidence/round36/tb2-regex-log/solve.sh
```

Fetched digests equal the receipt manifest line for line:

| file | sha256 (fetched == manifest) |
|---|---|
| test_outputs.py | `345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72` |
| test.sh | `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` |
| instruction.md | `4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c` |
| task.toml | `6bc98525852755caf1fe34c174c2f10f4328adb4ce6c1968dcafe1c877e4e160` |
| solve.sh | `7e670d4f2b4bccb1e4db38f2a173e085ceda028c38167912b466b0a84fcc0999` |

```
$ cd corpus/evidence/round36/tb2-regex-log && sha256sum -c SHA256SUMS
test_outputs.py: OK
test.sh: OK
instruction.md: OK
task.toml: OK
solve.sh: OK
exit=0
```
Receipt manifest verifies **5/5**, exit 0. The manifest names exactly the five captured files (no phantom rows).

## A3 — content-address cross-check against the commit's object graph

Independent of the raw HTTP path: recomputed `sha1("blob <len>\0" + bytes)` for each fetched file and compared to the tree API's blob sha at the pinned commit.

```
MATCH regex-log/tests/test_outputs.py  38c51719f480d2e852262ed2453842d5ea1ca79f (size 3730 = 3730)
MATCH regex-log/tests/test.sh          cb4a41a45e4b23f4d1f1392fd68f6e47c5dbbf57 (size  608 =  608)
MATCH regex-log/instruction.md         ab7f39b6e55776d9597657a435f902705c69450e (size 1021 = 1021)
MATCH regex-log/task.toml              1687e8f7a3fff35acc7b7ffea6aecd6bdfb7051e (size  989 =  989)
MATCH regex-log/solution/solve.sh      036acdf6b2ea66b34149a9a0336e7b9aed970a0d (size  485 =  485)
```
5/5 blob-sha matches ⇒ the captures are the actual objects committed at the pin, not merely what one URL served.

## A1 — drift: `main` since the pin

```
$ curl -fsSL https://api.github.com/repos/harbor-framework/terminal-bench-2/commits/main
main_head 2fd12b88aafdd04a52c298e3940bcb189f9766d6 2026-04-30T05:53:30Z 'Add task metadata to task manifests'
```
**`main` HEAD *is* the pinned commit.** `main` raw fetches therefore cannot differ from the pin:
- `regex-log/tests/test_outputs.py` @ main → sha256 `345c3bd0…8f72`, `cmp` vs capture: **identical**.
- `regex-log/tests/test.sh` @ main → **identical**.
- `regex-log/instruction.md` @ main → **identical**.

**DRIFT = no.** (Drift note, not a defect — and moot at this moment: no commits have landed upstream since the pin, so the pin is also current upstream `HEAD`. Any future upstream commit touching `regex-log/` would make this pin *older* but never wrong; the capture manifest stays the authority.)

## A4 — scope observations

1. **Capture set is exactly right.** The five captured files cover the grader (`tests/test_outputs.py` = S108), its runner (`tests/test.sh` = S109), the instruction (`instruction.md` = S110), the task manifest (`task.toml`), and the oracle (`solution/solve.sh`). `environment/Dockerfile`, `README.md`, `.gitignore` are deliberately uncaptured — none bears on the grader semantics the claim asserts.
2. **Probe receipt consistency (read-only check).** `corpus/evidence/round36/regex-log-probe.txt` terminates with `cases=24 observed_pass=8 observed_fail=16 mismatches=0`, matching the claim's headline exactly; its final case row `case=feb-29-rejected predicted=pass observed=pass match=yes … 'February can have up to 29 days (the permitting side is unobserved)'` is consistent with the claim's "permitting side of Feb 29 not enforced" finding.
3. **Admitted entry file absent at check time.** `corpus/knowledge/tb2-regex-log-grader.md` did not exist when I checked (2026-10-26T01:11Z; `ls corpus/knowledge/ | grep -i regex` empty). That is the C2 builder's wave-1 deliverable, not a pin defect — flagging so the L1 does not read my pin verification as covering an S108–S110 row set. My verdict covers captures + probe receipt only.
4. **`__pycache__` under the capture dir is harmless to `--require-clean-tree`.** `corpus/evidence/round36/tb2-regex-log/__pycache__/test_outputs.cpython-314.pyc` exists (2910 B) but is covered by `.gitignore:2:__pycache__/`, so `git ls-files --others --exclude-standard -- corpus/evidence/round36` returned **untracked_count=0**. The six tracked files in the capture dir are `SHA256SUMS` + the five captures. No clean-tree risk from the capture dir.
5. **No tool install performed.** `curl`/`python3`/`sha256sum`/`cmp` were already present; nothing installed or upgraded, so there is no version record to report beyond `curl 8.23.0` above.

## Limits

- Verification is HTTP + content-address only. I did not execute the task container or the grader; grader-behaviour claims belong to the probe receipt and its own counter.
- GitHub API responses were not cached across time; a later re-run could legitimately see `main` advanced past the pin. Timestamp of record: **2026-10-26T01:11Z**.

VERDICT: reopen-5/5-drift-no
