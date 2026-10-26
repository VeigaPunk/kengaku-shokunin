# F37RevLesson receipts (kengaku r37 wave 2, 2026-10-26)

Scratch: /fast/scratch/hyaku/kengaku-r37/F37RevLesson (clone of 357deceb, show-toplevel asserted,
0 untracked) — removed at seat end. All commands read-only on the lane; git calls read-only
(rev-parse / log / merge-base --is-ancestor / show / ls-files / check-ignore).

## 1. sweep on clean clone of 357deceb (lesson's "sweep receipt at landing defects=0")
$ python3 plans/anchor_digest_check.py --lane .
rows=107 tokens=15 defects=0
exit=0

## 2. spot-check item 3 (lesson says "expect empty")
$ grep -nE 'k36-|p23-|p4-|p5-|p6-|p7-|p8-|d4-|d5-|git-webserver' plans/pkg_gate.py
5:  d4-line --file F --spec SPEC
6:  d5-line --file F --capture-dir D --spec SPEC
366:    pd4 = sub.add_parser("d4-line")
369:    pd5 = sub.add_parser("d5-line")
388:        if args.cmd == "d4-line":
grep-rc=0   (5 lines — the gate's own d4-line/d5-line subcommand strings; NOT empty)

## 3. spot-check item 6 (lesson says "the S110 63-hex cell must be gone")
$ sed -n '125p' corpus/SOURCES.md | grep -o 'sha256 [0-9a-f]*' | awk '{print length($2)}'
63    (cell present at 357deceb and at HEAD dc90676; resolved only via the lesson erratum :32)
$ python3 plans/anchor_digest_check.py --lane .   # erratum path active
rows=107 tokens=15 defects=0

## 4. frozen digests 11/11 (freeze commit AND worktree)
$ while read -r line; do p=$(awk '{print $NF}' <<<"$line"); d=$(awk '{print $1}' <<<"$line"); \
  g=$(git show ca790460e9b74d4dc5870c878affd13cc9c4437a:"$p" | sha256sum | awk '{print $1}'); \
  w=$(sha256sum "$p" | awk '{print $1}'); ... done < .ufo/waves/round-37/claims/frozen-digests.txt
MATCH freeze MATCH worktree plans/round37_c1_verify.py
MATCH freeze MATCH worktree plans/round37_c2_verify.py
MATCH freeze MATCH worktree plans/git_webserver_probe.py
MATCH freeze MATCH worktree plans/pkg-spec-r37.json
MATCH freeze MATCH worktree plans/pkg_gate.py
MATCH freeze MATCH worktree plans/round36_c1_verify.py
MATCH freeze MATCH worktree plans/pkg-spec-r35.json
MATCH freeze MATCH worktree corpus/evidence/round37/git-webserver-dry-cases-freeze.txt
MATCH freeze MATCH worktree corpus/evidence/round37/tb2-git-webserver/SHA256SUMS
MATCH freeze MATCH worktree .ufo/waves/round-37/claims/make_c2_skip.py
MATCH freeze MATCH worktree .ufo/waves/round-37/claims/make-controls.sh

## 5. ancestry (lesson preamble)
$ git merge-base --is-ancestor 3ea9a1d9… ca790460… && OK      -> OK
$ git merge-base --is-ancestor ca790460… 5c7b34e9… && OK      -> OK
$ git merge-base --is-ancestor 5c7b34e9… 44b7298a… && OK      -> OK

## 6. probe join (spot-check item 5 numbers)
$ python3 (parse CASE lines of git-webserver-dry-cases-freeze.txt vs git-webserver-probe.txt)
ids_equal_order: True n= 22
predicted_pass: 9 observed_pass: 9
disagreements: 0 match_NO_ids: []
receipt summary line :49: cases=22 observed_pass=9 observed_fail=13 mismatches=0

## 7. live re-open S111 (spot-check item 7, one of three)
$ curl -fsSL https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88…/configure-git-webserver/tests/test_outputs.py | sha256sum
526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37  -   (= row anchor)

## 8. mistakes row 5 quote vs the cited file (D3)
$ grep -E 'CASE M1-|CASE M2-' .ufo/waves/round-37/build/R37AnchorSweep/fixture-receipt.txt
CASE M1-erratum-wrong-correction ref=index defects=3/3 ids=S110 … exit=1 ok
CASE M2-correction-not-in-manifest ref=index defects=2/2 ids=S110 … exit=1 ok
$ git show 9cf7ee0:<same path> | grep 'CASE M[12]-'   -> same ok lines
$ git show 67cbe7a:<same path> | grep 'CASE M[12]-'   -> same ok lines
$ grep -rn 'defects=3/1\|defects=2/1' <lane>  -> only corpus/lessons/round-37.md:45,
  .ufo/waves/round-37/build/R37LessonDraft/round-37.md:39, R37LessonDraft.md:52-53

## 9. census counts on lane (landing)
$ grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 107
$ ls corpus/knowledge/*.md | wc -l                                          -> 44
$ grep -cE '^\| `knowledge/[^`]+` \|' corpus/README.md                       -> 44
census-before.txt: 15 W04 lines (S040…S100), kengaku ok, exit=0; same 15 SIDs as
.ufo/waves/round-36/claims/census-before.txt (15 W04).

## 10. dispatch and wave-1 close
$ python3 -c "json.load(falsify-dispatch.json)['counts']" -> {"spawn": 37, "resume": 0, "total": 37}
$ grep -o '357deceb[a-f0-9]*' falsify-dispatch.json       -> 2 hits (tip named)
$ ls .ufo/waves/round-37/build/*.md | wc -l              -> 40

## 11. spot-check item 9
$ find .ufo/waves/round-37/build -maxdepth 2 -name corpus -o -name plans   -> (empty), rc 0

## 12. erratum arithmetic
$ printf '4f7ac05e70cf922ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c' | wc -c -> 63
$ printf '4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c' | wc -c -> 64
$ grep instruction corpus/evidence/round36/tb2-regex-log/SHA256SUMS
4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c  instruction.md
round-36 capture test_outputs.py: :71 `expected_dates = [`, :72-80 nine literals, :81 `]`
regex-log instruction.md: 19 lines; requirement bullets 1-4, 6-7, 9-10 -> exact span 1-10
