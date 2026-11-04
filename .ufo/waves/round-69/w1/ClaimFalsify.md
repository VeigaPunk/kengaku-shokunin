# ClaimFalsify-2 — round 69, wave w1 (freeze attack)

Scope: the two frozen claims in `plans/round-69-claims.md` at freeze `b288e8e0`. I did not
edit the lane, did not run the C1 battery, and did not judge the C2 landing commit.

## Verdict in one paragraph

**Freeze order holds.** The claims doc and both instruments are committed at `b288e8e0`, and no
C1 receipt exists at that commit or at base (`git cat-file -e` → rc 128 both). **R69-C1 is
unsatisfiable as frozen, by two independent locks**: (i) the frozen table leaves legs 2 and 4
with no `F` witness, which the frozen kill rule and the instrument's own coverage gate both
reject — the table violates the rule it was frozen under; (ii) the battery emits 6-token
`VECTOR` lines while `--check-receipt` requires exactly 5, so every receipt the instrument can
produce is rejected before its vectors are read. **R69-C2 reaches `DEFECTS n=0` on the current
worktree, but the predicate's "the gate re-derives as E1–E7" is false for five of the seven
checks**: E1/E2/E4/E5/E6 flip from defect to ok on prose-only edits (demonstrated), E3's
completeness is self-declared (a one-input erratum passes while 145 files differ), and E7's
only negative arm is rc-driven, never the byte comparison. Under the claim's own kill rule
("a correction that exists only as prose with no re-deriving check is not a closed defect"),
`n=0` does not entail the predicate.

## Freeze order — verified

```
$ git -C L cat-file -e b288e8e0:corpus/evidence/round69/nginx/receipt.txt   → fatal: ... does not exist in 'b288e8e0'; rc=128
$ git -C L cat-file -e a518980e:corpus/evidence/round69/nginx/receipt.txt   → fatal: ... does not exist in 'a518980e'; rc=128
$ git -C L log --oneline -5 -- plans/round-69-claims.md
b288e8e0 round-69 freeze: ...          (no later commit touches the file)
$ git -C L show b288e8e0:plans/round69_c1_nginx_probe.py | sha256sum  → 66b5128d...0100ea
$ git -C L show b288e8e0:plans/round69_c2_routed_defects.py | sha256sum → ea28b006...15485
$ git -C L show b288e8e0:plans/round-69-claims.md | sha256sum          → 0088cfb0...53a41
```

All three equal the `FROZEN-SHA` lines in `.ufo/waves/round-69/nginx-control.txt`, and the
worktree copies are byte-identical (`sha256sum` same; `git status --porcelain plans/` empty).
No after-the-fact vector: the vectors were committed before any receipt existed. **PASS.**

Base-state before→after anchors, re-derived:

```
$ git show a518980e:SKILL.md | grep -c 'executed 2 of 8'      → 1
$ git show a518980e:SKILL.md | grep -c 'executed 3 of 8'      → 0
$ git show a518980e:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S241[[:space:]]*\|' → 0
```

## R69-C1 — independent derivation from the grader source

Read `corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py:1-178`
(sha `045cc716…`, = `SHA256SUMS:111`). Leg semantics as implemented, not as described:

| leg | what actually decides it |
|---|---|
| 1 | `subprocess.run(["which","nginx"])` rc == 0 |
| 2 | `requests.get("http://localhost:8080")` status == 200 (3 tries, 2 s apart) |
| 3 | `GET /` status 200 **and** `response.text.strip() == "Welcome to the benchmark webserver"` |
| 4 | `GET /nonexistent-page` status 404 **and** body strip-equals `"Page not found - Please check your URL"` |
| 5 | `subprocess.run(["nginx","-t"])` rc == 0 |
| 6 | `/etc/nginx/conf.d/benchmark-site.conf` exists, `listen\s+8080`, `root\s+/var/www/html`; `/etc/nginx/nginx.conf` has `log_format` + 4 fields + `limit_req_zone.*?rate=10r/s` |
| 7 | after `GET /`, `/var/log/nginx/benchmark-access.log` exists |
| 8 | after `GET /test-<ts>`, that log matches timestamp, method, `\s\d{3}\s`, trailing quoted UA |

Derivation, case by case (staged knobs: `index`, `log`, `shim`, `rate_limit`):

| case | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | derived | frozen | agree |
|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | P | P | P | P | P | P | P | P | `PPPPPPPP` | `PPPPPPPP` | yes |
| K2 | P | P | F | P | P | P | P | P | `PPFPPPPP` | `PPFPPPPP` | yes |
| K3 | P | P | P | P | P | P | F | F | `PPPPPPFF` | `PPPPPPFF` | yes |
| K4 | P | P | P | P | P | F | P | P | `PPPPPFPP` | `PPPPPFPP` | yes |
| K5 | F | P | P | P | F | P | P | P | `FPPPFPPP` | `FPPPFPPP` | yes |

40/40 legs agree with the frozen table. Non-obvious legs:
- **leg 2 is P in all five cases**: K2's defect is the body, not the status; K5 removes the
  `nginx` shim but the service is the probe's own Python server (`stage_case`/`SERVER`), so
  `/` still answers 200.
- **leg 4 is P in all five cases**: the 404 body is identical in every case dict.
- **K4 leg 5 P**: the shim exits 0 for `-t` unconditionally, so a config missing the rate
  clause still passes (the claims doc's named limitation (ii), confirmed here).
- **K5 leg 5 F**: `["nginx","-t"]` raises `FileNotFoundError`; the runner prints `E:...` and
  maps it to F — not an AssertionError.

### F1 (fatal, freeze-blocking) — the frozen table violates the frozen kill rule

Claims doc line 36: *"Each of the eight legs has one red witness and four green witnesses by
construction."* Column counts from the frozen vector:

```
leg 1 PPPPF F=1   leg 5 PPPPF F=1
leg 2 PPPPP F=0   leg 6 PPPFP F=1
leg 3 PFPPP F=1   leg 7 PPFPP F=1
leg 4 PPPPP F=0   leg 8 PPFPP F=1
total F=6 total P=34          (not 8 and 32)
```

Legs 2 and 4 have **no** `F` witness. The claims doc's own kill rule (line 43): *"any leg with
no `P` or no `F` witness"* fails. The probe implements that rule at
`plans/round69_c1_nginx_probe.py:463-465` (`full_f == len(LEGS)`) and
`:554` (`defect("leg-coverage", ...)`). Consequence: `run_battery` prints
`PREDICATE R69-C1 fail` even if every staged vector matches, and `--check-receipt` rejects any
receipt whose vectors match the frozen table. The live battery receipt produced by a sibling
seat corroborates on real data (labels: sibling artifact, not my run —
`.ufo/waves/round-69/w1/nginx/receipt.txt`):

```
LEG-COVERAGE legs=8 seen_p=8 seen_f=6
SUMMARY cases=5 legs=40 mismatches=0 setup=0
PREDICATE R69-C1 fail
```

No case in the frozen table can redden leg 2 or leg 4: the four knobs do not touch the
service's status code or the 404 body. This is structural, not a staging miss.

### F2 (fatal) — the emitter and parser disagree on the `VECTOR` line

Emitter, `plans/round69_c1_nginx_probe.py:460-461`:
`VECTOR {id} {vector} expected {expected} agree={agree}` → **6** whitespace tokens.
Parser, `:513-518`: `if len(parts) != 5: defect("vector-line", ln); continue` then reads
`parts[4].split("=")[-1]` as the agree flag.

Raw output of the checker on the actual 6-token receipt:

```
$ python3 plans/round69_c1_nginx_probe.py --check-receipt .ufo/waves/round-69/w1/nginx/receipt.txt
CHECK ok cases=5 legs=8 seen_p=0 seen_f=0
DEFECT vector-line VECTOR K1 PPPPPPPP expected PPPPPPPP agree=True
... (K2..K5 identical)
DEFECT case-set got=[] want=['K1', 'K2', 'K3', 'K4', 'K5']
DEFECT leg-coverage test_nginx_installed p=0 f=0
... (all 8 legs p=0 f=0)
DEFECT stored-predicate PREDICATE R69-C1 fail
PREDICATE R69-C1 fail
rc=1
```

`vectors` is never populated, so `case-set` and all eight `leg-coverage` defects follow
mechanically. The parser's `parts[4]` only works for a 5-token form
`VECTOR <id> <obs> <ignored> agree=True`, which the battery never writes and the selftest never
writes either (`body()` at `:389` emits the same 6 tokens).

### F3 — the acceptance set is empty (proof, independent of F1/F2' staging)

A receipt passes only if, for every case, `derived == VECTOR` (`leg-vector`) and
`VECTOR == frozen expected` (`vector-mismatch`), and every leg has `seen_f >= 1`
(`leg-coverage`). The first two force the TEST values to equal the frozen table; the frozen
table has no `F` for legs 2 and 4. Contradiction. Therefore **no receipt can ever make
`--check-receipt` return 0**, and `run_battery`'s `ok` (`full_f == 8`) can never be true. The
claim's before→after target ("receipt present with `PREDICATE R69-C1 pass`") is unreachable
without a post-freeze amendment.

Closest possible receipt (hand-built, 5-token form, correct shas, frozen vectors):

```
$ python3 plans/round69_c1_nginx_probe.py --check-receipt $S/five-token.txt
CHECK ok cases=5 legs=8 seen_p=8 seen_f=6
DEFECT leg-coverage test_nginx_running p=5 f=0
DEFECT leg-coverage test_custom_404_page p=5 f=0
CHECK stored-predicate=pass derived=fail
PREDICATE R69-C1 fail
rc=1
```

### F4 — the C1 selftest is vacuous for 3 of 5 red fixtures

```
$ python3 plans/round69_c1_nginx_probe.py --selftest --work $S/stwork
RED r1-all-p rc=1 refused=True
RED r2-probe-sha rc=1 refused=True
RED r3-leg-vector rc=1 refused=True
RED r4-missing-leg rc=1 refused=True
RED r5-grader-sha rc=1 refused=True
SELFTEST red_refused=5/5 green_ok=0 ok=True
rc=0
```

Defect kinds actually printed per fixture (checker run on the fixture files):

- `r1-all-p`: 5×`vector-line`, `case-set`, 8×`leg-coverage` — no `vector-mismatch`.
- `r2-probe-sha`: `probe-sha` fires (has teeth) **plus** the format defects.
- `r3-leg-vector` (K2=`PPPPPPPP`): 5×`vector-line`, `case-set` — **no `vector-mismatch`**; the
  property the fixture is named for is never exercised.
- `r4-missing-leg`: 5×`vector-line`, `case-set` — **no `leg-set` / `leg-missing`**.
- `r5-grader-sha`: `grader-sha` fires (has teeth) plus the format defects.

So 3/5 red arms pass only because the format bug rejects everything; the probe-sha and
grader-sha checks are the only ones demonstrated able to fail. I verified the hidden checks do
fire when given a parseable receipt: a 5-token receipt with K2=`PPPPPPPP` yields
`DEFECT vector-mismatch K2 PPPPPPPP != PPFPPPPP`; dropping a leg yields `leg-set` +
`leg-vector` + `leg-missing`. They have teeth — the selftest just never reaches them. The
`dup_leg` parameter of `body()` (`:378`) is never used by any fixture, so duplicate TEST lines
are untested (a duplicate is silently collapsed by the `legs[...]` dict; observed no defect).

`green_ok=0` and `ok=True`: the selftest's pass criterion does not require a green receipt, and
none can exist (F3).

### F5 — the do-nothing forgery is invisible to the checker

I forged a receipt that claims the frozen vectors with **zero evidence**: `case_sha256=0…0`,
fabricated `server_pid=4242`, `sandbox_rc=0`, no evidence directory, and then deleted every
`CASE` line. The checker's verdict is unchanged (only the same two coverage defects). The
checker never reads `CASE`, `case_sha256`, `server_pid`, or `sandbox_rc` — its only line
handlers are `PROBE`, `GRADER`, `VECTOR`, `TEST`, `SUMMARY`, `PREDICATE`
(`plans/round69_c1_nginx_probe.py:495-565`). Named limitation (i) says the pid and captures are
"the live witness"; that is true, but the checker does not consult the witness at all — a
zero-evidence receipt differing from a live one only in fields the checker never reads. If the
coverage clause were satisfiable, this forgery would pass.

### F6 — `--render-table` does not byte-equal the claims table

Claims doc line 25: *"`--render-table` must byte-equal it"*. It does not: the render header is
`case  setup ... vector`, the K1 note reads `all-green end state: ...` (doc: `all-green: ...`),
K4 loses its backticks, and the doc rows are pipe-delimited. The five **vectors** match row for
row; the byte-equality assertion is false. Minor documentation over-claim, not a vector defect.

Also note the C1 predicate sentence (line 10) does not mention the class-row or `SOURCES.md`
targets at line 48; a round could print `PREDICATE R69-C1 pass` (if the table were fixable)
without touching `executed 3 of 8` or S241.

## R69-C2 — red-before verified, checks audited

### Red-before is honest

Extracted base bytes (`git archive a518980e | tar -x -C $S/base-lane`), copied the frozen gate
in, ran it, diffed:

```
$ python3 plans/round69_c2_routed_defects.py --root $S/base-lane
E1 defect rows=0/4 missing=[...]
E2 defect headings=0 q50=False round68-lesson=False spotcheck=False
E3 defect corpus/evidence/round69/c2-receipts/provenance-erratum.txt missing
E4 defect verified-at-lines=1 last-names-landing=False
E5 defect strict-lines=0
E6 defect rerecord-lines=0
E7 defect problems=['...depth-gate.txt:missing', '...trio.txt:missing']
DEFECTS n=7
PREDICATE R69-C2 fail
rc=1
$ diff -u .ufo/waves/round-69/c2-red-before.txt $S/c2-base-rerun.txt
-rc=1        # only the trailer line, which the committed receipt writes as part of its capture
```

**PASS**: the committed red-before is the base bytes' honest run (10 lines identical, rc 1).
The gate's selftest also matches the doc: `defects-in-fake=7 want=7 all-fail=True`,
`e7-stale-red=True`, rc=0.

### F7 — five of seven checks flip on prose-only edits

Built a lane from **base bytes** and added only prose: four thin registry rows to `SKILL.md`,
a `## Round69 criterion` heading whose body is `Q50 see <lesson> and <spotcheck>`, an appended
`verified-at: 1ec2e60a`, a `strict attack share 3/12 reviewer critic mutation-tester labrat`
line, and a `w1-results.json ... output: "" ... per-seat` line. No defect was actually fixed.

```
E1 ok rows=4/4 missing=[] thin=[]
E2 ok headings=1 q50=True round68-lesson=True spotcheck=True
E3 defect ... provenance-erratum.txt missing
E4 ok verified-at-lines=2 last-names-landing=True
E5 ok strict-lines=1
E6 ok rerecord-lines=1
E7 defect problems=['...depth-gate.txt:missing', '...trio.txt:missing']
DEFECTS n=2
PREDICATE R69-C2 fail
```

Per-check findings (file:line):
- **E1** (`plans/round69_c2_routed_defects.py:150-165`): only `len(cells)>=8`, the entry path in
  `cells[2]` existing, `` `0` ``/`` `1` `` in `cells[3]`, and `cells[4]` non-empty are checked.
  My rows left pinned values, write scope and owner empty (cells 5–7) and passed. The claims
  doc's "complete ... pinned values and write scope" is not enforced; kind (`gate|probe`) is
  not checked either.
- **E2** (`:169-181`): one heading, the token `Q50`, and both path strings. No normative
  content is required — `Q50 see <paths>` passes. The "owed criterion" could be a citation-only
  paragraph.
- **E4** (`:225-234`): count ≥ 2 and the *last* line contains the landing. Rewriting the
  original line — which the routed defect explicitly forbids ("append a new line; do not
  rewrite the old one") — still passes:
  `E4 ok verified-at-lines=2 last-names-landing=True` with line 1 rewritten to
  `verified-at: 2026-01-01 (rewritten original, not an append)`.
- **E5** (`:240-246`): a string match on `strict attack share`, `3/12` and the four role names.
  The count is asserted, never recounted from the wave roster.
- **E6** (`:247-250`): a string match on `w1-results.json`, `output: ""`, `per-seat`. It does
  not check that twelve reports exist/non-empty or that the JSON has twelve empty outputs.

The actual landing artifacts are substantive (I read them: the E1 rows carry kind, command,
verdict map, selftest, pinned values, scope, owner; Q50 has a normative rule; the strict line
and re-record are complete). The finding is about the **check**, not the landing: `n=0` is
reachable with citation-only text, so it is not evidence of closure. The claim's own kill rule
(line 105) says a prose-only correction is not a closed defect; five checks are prose-only.

### F8 — E3 completeness is self-declared; one input suffices

`E3` iterates only over `INPUT` lines the erratum itself declares (`:197-221`); `inputs` needs
to be non-empty, nothing more. A one-input erratum naming an unchanged file passes:

```
TREE 27f649f8
LANDING 1ec2e60a
INPUT plans/round63_gate_checks.py at-tree=a98d9c0f... at-landing=a98d9c0f...
$ python3 plans/round69_c2_routed_defects.py --root $S/e3-lane
E3 ok inputs=1 differs=[] problems=[]
DEFECTS n=6
```

`git diff --name-only 27f649f8 1ec2e60a` reports 145 changed paths; this erratum names zero of
them and omits the `SKILL.md` sha-mismatch nit entirely. The check's real guarantee is "the
listed inputs hash correctly", not "every bound input is listed". Encoding hazard: an empty
`DIFFERS` set must be expressed by *omitting* the line; `DIFFERS none` / `DIFFERS -` would
become a set element and fail.

The committed erratum itself is honest: all six `INPUT` shas verify at both revisions, and
`DIFFERS {SKILL.md}` equals the observed difference (`SKILL.md` `3fe9a6d0…` at tree →
`544ad892…` at landing). So F8 is a check-strength defect, not a landing defect.

### F9 — E7's stale-receipt arm is rc-driven, not byte-driven

`E7` (`:252-264`) appends `f"{rel}:rc={rc}"` and `continue`s on non-zero rc before the
`fresh != path.read_text()` comparison. In the fixture lane the depth command fails:

```
$ cd $S/c2selftest/fake-lane && python3 plans/round63_gate_checks.py depth --skill SKILL.md \
    --receipt corpus/evidence/round62/class-survey.txt --root .
ROWS n=16 class_match=True count_mismatch=0 paths total=33 resolved=2 share=0.06
PREDICATE R63-C2 fail
depth-rc=1
```

So `_selftest_e7`'s "stale receipt" is red because rc=1, never because the bytes differ. The
byte-comparison branch has no negative witness. The docstring concedes the fixture lane cannot
reproduce the real lane's 33 resolved paths. The green arm is outside the selftest. On the real
lane both commands pass now (`depth` rc=0 share=1.00; `trio` → `TRIO pass`), so E7 can go green,
but its failure detection is unproven.

Related calibration: the C2 selftest copies from the live worktree (`lane_root()`), not from a
frozen revision, so two runs of the same commit can disagree while a sibling lands corrections.
It fails safe here (strip-by-construction still yielded 7), but it is not reproducible.

### Landing state at time of review (not judged)

`python3 plans/round69_c2_routed_defects.py` on the uncommitted worktree printed
`E1..E7 ok`, `DEFECTS n=0`, `PREDICATE R69-C2 pass`, rc=0. I did not verify this against a
landing commit; the C2 predicate is defined at the landing tip.

## Smallest safe corrections (reported, not applied)

- **R69-C1**: (a) the table must redden legs 2 and 4 — e.g. a sixth case with the service down
  (reddens 2 and cascades) or a 404-body-differs case (reddens 4) — with a re-frozen vector; or
  drop "every leg `F` at least once" from the predicate. (b) Make emitter and parser agree on
  the `VECTOR` token count (change `:460` to 5 tokens or `:513` to 6 and read `agree=`).
  (c) Add a green-arm fixture and a byte-diff negative arm; make the checker read `CASE` if it
  is meant to witness a live run.
- **R69-C2**: either narrow the predicate to what the gate measures ("the seven checks pass"),
  or make E1/E2/E4/E5/E6 re-derive: E1 parse the instrument's real flags/selftest output; E2
  require a testable rule bound to the round-68 mistake rows; E4 diff the first line against
  base; E5 recount from the wave dispatch; E6 count the twelve reports and the JSON entries.
  E3 must read the bound-input list from the round-68 receipt rather than the erratum; E7 needs
  a byte-diff negative arm on a lane where the command passes.

## Commands NOT run (state every one)

- **The C1 battery** (`--lane . --work ... --receipt ... --evidence-dir ...`): my item does not
  authorize it and the wave spec says only seats whose item names it run it. I bound no port;
  I did not write `corpus/evidence/round69/nginx/`. The observed vectors I cite are a sibling
  seat's committed-in-W receipt, labeled as such; my vectors are derived from grader source.
- Any git/jj write: no init in the lane, no commit/push/stage/stash/checkout/switch, no
  worktree add. The only git fixture I initialized was none — `$S/e3-lane/.git` is a plain
  `gitdir:` pointer read by `git show`; no write command ran against it.
- `--selftest --green-receipt` for C1: no green receipt exists, and F3 proves none can.
- TB2 pin `2fd12b88`: not verified (no local TB2 checkout); the probe only records it.
- Real `nginx -t` syntax behavior: not verified (lane shim only; named limitation (ii)).
- No pacman/uv/npm installs; nothing to record.
- No edits to any tracked lane file, `MANIFEST.json`, the fleet root, or sibling lanes.

## Exact argv used (scratch root `S=/fast/scratch/hyaku/kengaku-r69/ClaimFalsify-2`)

```
git -C L log --oneline -- plans/round-69-claims.md
git -C L cat-file -e b288e8e0:corpus/evidence/round69/nginx/receipt.txt
git -C L cat-file -e a518980e:corpus/evidence/round69/nginx/receipt.txt
git -C L show --stat --oneline b288e8e0
git -C L show b288e8e0:{plans/round69_c1_nginx_probe.py,plans/round69_c2_routed_defects.py,plans/round-69-claims.md} | sha256sum
sha256sum plans/round69_c1_nginx_probe.py plans/round69_c2_routed_defects.py plans/round-69-claims.md
git -C L archive a518980e | tar -x -C $S/base-lane
python3 $S/base-lane/plans/round69_c2_routed_defects.py --root $S/base-lane
python3 plans/round69_c2_routed_defects.py --root $S/prose-lane
python3 plans/round69_c2_routed_defects.py --root $S/e3-lane
python3 plans/round69_c2_routed_defects.py --root $S/e4-lane
python3 plans/round69_c2_routed_defects.py --selftest --work $S/c2selftest
python3 plans/round69_c2_routed_defects.py            # live worktree
python3 plans/round69_c1_nginx_probe.py --check-receipt <receipt>
python3 plans/round69_c1_nginx_probe.py --selftest --work $S/stwork
python3 plans/round69_c1_nginx_probe.py --render-table
python3 plans/round63_gate_checks.py depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt --root .
python3 plans/round63_gate_checks.py trio corpus/knowledge/tb2-network-service-offline-grader.md
git -C L show 27f649f8:SKILL.md | sha256sum ; git -C L show 1ec2e60a:SKILL.md | sha256sum
git -C L diff --name-only 27f649f8 1ec2e60a
```

Scratch `$S` deleted before yield; no receipts were copied out because the report quotes the
raw lines verbatim.
