# SourceOpen — kengaku round 69, wave w1 (R69-C1 source opening)

Seat: `SourceOpen` (leaf; no subagents dispatched). Date 2026-11-03.
Item: open the R69-C1 source live and produce the S241 row evidence.
Lane base at start: `b288e8e03bdfed715bbb6de0ea166e2c465c0453` (`round-69 freeze: …`), lane tree
carried siblings' uncommitted work (`SKILL.md`, `corpus/QUALITY.md`,
`corpus/knowledge/tb2-network-service-offline-grader.md`, `corpus/lessons/round-68.md` modified;
`corpus/evidence/round69/` and `.ufo/waves/round-69/w1/` untracked). `corpus/SOURCES.md` was
**clean and unmodified** throughout; I did not edit it.

Scratch: `/fast/scratch/hyaku/kengaku-r69/SourceOpen` (created with `mkdir -p`, passed explicitly,
deleted before yield). No tool installed or upgraded; no pacman transaction attempted.

## 1. Grader fetched live at the frozen pin

```
curl -sS -o test_outputs.py -w 'HTTP=%{http_code} BYTES=%{size_download} URL=%{url_effective}\n' \
  https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/nginx-request-logging/tests/test_outputs.py
HTTP=200 BYTES=5947 URL=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/nginx-request-logging/tests/test_outputs.py

sha256sum test_outputs.py
045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0  test_outputs.py
```

Comparison with the committed capture and the manifest:

```
C=/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py
cmp test_outputs.py "$C"  →  CMP identical rc=0
sha256sum "$C"            →  045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0  "$C"
wc -c "$C"                →  5947 "$C"
sed -n '111p' corpus/evidence/round52/graders/SHA256SUMS
045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0  ./nginx-request-logging/tests/test_outputs.py
git -C L cat-file -p HEAD:corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py | sha256sum
045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0  -
```

Access witness (same URL, headers only): `HTTP/2 200`, `content-type: text/plain; charset=utf-8`,
`etag: "c9658a998676f510aa25d1c57fafc83e692739db9c69d00c89d8e769513c5287"`.

**Conclusion.** The live fetch at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` is byte-identical
to the committed capture, to `SHA256SUMS:111`, and to the blob at lane HEAD; 5947 bytes, sha256
`045cc716…acda0`. The frozen claim's grader sha256 is reproduced from the network and from the
lane's own bytes. (Observed.)

## 2. `instruction.md` at the same pin

```
curl -sS -o instruction.md -w 'HTTP=%{http_code} BYTES=%{size_download}\n' \
  …/2fd12b88aafdd04a52c298e3940bcb189f9766d6/nginx-request-logging/instruction.md
HTTP=200 BYTES=1882
sha256sum instruction.md → 26a7ac98aced6107f147206790ada77bbf8ed3c25fb360cf323d5fc6889edf99
wc -l -c instruction.md  → 24 1882
```

Not a 404: the task ships `instruction.md` (24 lines) and `task.toml` (`HTTP=200 BYTES=885`,
`name = "terminal-bench/nginx-request-logging"`) at the pin.

Coverage of the three clauses the item names (instruction line numbers):

| grader clause | stated in instruction? | lines |
|---|---|---|
| expected index body `Welcome to the benchmark webserver` (grader :39) | **yes, verbatim** | :15 "Create a simple index.html file … with the content:"; :16 `"Welcome to the benchmark webserver"` |
| custom 404 body `Page not found - Please check your URL` (grader :52) | **yes, verbatim** | :17 "Create a custom 404.html page with the content:"; :18 `"Page not found - Please check your URL"` |
| rate-limit clause `limit_req_zone.*?rate=10r/s` (grader :119) | **semantics yes, literal token no** | :9 "rate limiting … only 10 requests per second per IP address with a burst capacity of 10 requests using a 10MB memory zone"; :10 "Add the rate limiting zone definition (`limit_req_zone`) to `/etc/nginx/nginx.conf` and apply the rate limiting (`limit_req`) in the server block" |

Related instruction facts the grader does **not** check: error log `/var/log/nginx/benchmark-error.log`
(:8), disabling `/etc/nginx/sites-enabled/default` (:13), `limit_req` application in the server block
(:10), burst capacity 10 and 10MB zone (:9). The 404 clause is stated as "serves /404.html" (:11),
but the grader requests `/nonexistent-page` and compares the body (:48-52) — it never requires a
`404.html` file to exist.

## 3. Proposed S241 row (exact text; not landed by this seat)

```
| S241 | `nginx-request-logging` TB2 grader `tests/test_outputs.py` at pin `2fd12b88` — eight pytest legs over `localhost:8080`, two config files and one access log — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/nginx-request-logging/tests/test_outputs.py | code | A | network-service grader offline execution (R69-C1) | pin `2fd12b88`, fetched 2026-11-03 HTTP 200, 5947 bytes; :22 verbatim: response = requests.get("http://localhost:8080", timeout=2) — legs in file order :11 :17 :33 :46 :59 :67 :123 :144; sha256 045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0 = SHA256SUMS:111, cmp rc 0 against corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py | eight legs: PATH `which nginx` :13 and `nginx -t` :61; status 200 :22-25; index body :38-40 and 404 body :51-53 compared after strip; conf.d/benchmark-site.conf `listen 8080` :86 and `root /var/www/html` :89; nginx.conf `log_format` fields :107-113 and `limit_req_zone.*?rate=10r/s` :119; access-log existence :132 and line format :165-177 — five staged cases make every leg both P and F | mined | 2026-11-03 | 180d | corpus/knowledge/tb2-network-service-offline-grader.md |
```

Row-shape verification (the lane's own parsers, run on a scratch copy):

```
cells: 11
census-regex (^ {0,3}\|\s*(S\d{3,})\s*\|): True
inner pipes in body: 10  (= cells-1; no literal `|` inside any cell)
quote `response = requests.get("http://localhost:8080", timeout=2)` — 4 words, at grader :22
sha256 tokens: ['045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0'] (count 1, in anchor, 64 lowercase hex)
corpus/evidence/ paths named: ['corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py'] (exactly one capture)
```

Design notes for the landing seat:
- The anchor cell carries the only `sha256` token, per Q26.
- `SHA256SUMS:111` is deliberately written **without** the `corpus/evidence/` prefix. Naming
  `corpus/evidence/round52/graders/SHA256SUMS` would declare a second capture; the row carries one
  token, so `plans/anchor_digest_check.py` would raise `capture-unanchored` for that second file.
- `corpus/evidence/round52/graders/` has no `task.toml`, so the URL cannot bind by task slug
  (`terminal-bench/nginx-request-logging` is not among the 15 committed evidence `task.toml` slugs);
  binding is by the explicit lane path (`by=row-path`), which the check confirms.

## 4. Anchor binding re-derived (Q26)

Method: `git clone -q --shared --no-checkout L $D` (scratch, `git -C $D rev-parse --show-toplevel`
= `$D`, HEAD `b288e8e0`), copy the lane's working-tree `corpus/SOURCES.md` and `corpus/lessons/`
into `$D/corpus/`, append the row, then run the lane's own checker read-only:

```
python3 plans/anchor_digest_check.py --lane "$D" --verbose
BIND S241 capture=corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py by=row-path
RESOLVED S241 digest=045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0 via=corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py bind=row-path listed=corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py
rows=233 tokens=125 defects=41
```

Lane baseline (same checker, no row): `rows=232 tokens=124 defects=41` (33 `anchor-unbound`,
6 `digest-wrong-capture`, 1 `digest-unknown`, 1 `token-outside-anchor`; the 41 are pre-existing and
are not this seat's to fix). The row adds one row and one token and **zero** defects; there is no
`DEFECT S241` line. Exit code 1 in both runs is the checker's "defects found" (the pre-existing 41),
not a row failure.

Calibration note: a first run of the clone without `corpus/lessons/` read `defects=42` — the extra
`S110 digest-short` line is the erratum exemption in `corpus/lessons/` that the checker loads from the
**working tree** (`load_errata`: `if not f.is_file(): continue`). Copying `corpus/lessons/` reproduced
the lane's 41 exactly; the difference was the clone's missing worktree, not the row.

Target-shape check: `grep -cE '^\|[[:space:]]*S241[[:space:]]*\|' corpus/SOURCES.md` → **0** on the
lane now, **1** on the proposed file. `corpus/SOURCES.md` was not modified by this seat.

## 5. Findings a C1 attacker should use

F1 — **K5 needs a serving process that is not the PATH shim.** Legs 2-4 and 7-8 speak HTTP and read
the access log; only legs 1 (`which nginx`, :13) and 5 (`nginx -t`, :61) use PATH. The probe already
satisfies this: `plans/round69_c1_nginx_probe.py:155-207` runs a lane-built
`http.server`/`ThreadingTCPServer` on 127.0.0.1:8080 independently of the `/shim` bind
(`:303-306`, `:339-340`), so K5's `shim=False` (`:104`) still yields `FPPPFPPP`. Verified from the
probe source; a seat that "removes the shim" without keeping the server would instead observe
`FFFFF???` and misreport the frozen vector as broken.

F2 — **Leg 6 reads two files, and a missing `nginx.conf` fails with a misleading message.**
`test_nginx_config_settings` reads `/etc/nginx/conf.d/benchmark-site.conf` (:70-83) and
`/etc/nginx/nginx.conf` (:93-104); if the second is absent `config_content` stays `""`, so the first
failing assert is `has_log_format` at :113 ("No log_format directive found") — not a missing-file
message. K1/K4 staging must create both files.

F3 — **The grader is narrower than the instruction and stricter in one token.** Unchecked:
`burst=10`, `zone=…:10m`, `limit_req` in the server block, `error_log` path, default-site removal.
Stricter: `re.search(r"limit_req_zone.*?rate=10r/s", …)` (:119) runs without `DOTALL`, so the zone
definition and `rate=10r/s` must be on **one line**; the literal `rate=10r/s` is not in the
instruction (:9-10 state the semantics only).

F4 — **Leg 8 never asserts the unique path appears.** `:161` breaks out of the loop only if
`unique_path in log_content`; a stale log line from an earlier request still satisfies the four
format regexes (:165-177). A replay that reuses a log file between cases can therefore green leg 8
for the wrong reason.

F5 — **Legs 3, 4, 7, 8 issue `requests.get` with no timeout** (:35, :48, :126, :148). A staged server
that accepts and never answers hangs the replay instead of failing the leg; the battery needs an
outer per-case timeout (leg 2 is the only HTTP leg with `timeout=2`).

F6 — **The 404 leg checks a body, not the file.** `test_custom_404_page` requests
`/nonexistent-page` (:48) and compares the stripped body (:51-53); the instruction's "serves
/404.html" (:11) is satisfied by any mechanism producing that body (e.g. `return 404 "…"`), and no
leg checks that `/404.html` exists.

F7 — **Line-number caution for the knowledge entry.** The nginx grader's `localhost:8080` literals are
at :22, :35, :48, :126, :148; **:30 is `time.sleep(2)`**. The sentence in
`corpus/knowledge/tb2-network-service-offline-grader.md:31` ("the grader's own line 30 carries the
literal `localhost:8080`") is about the **pypi-server** grader (S228), where :30 is
`"http://localhost:8080/simple"` — confirmed at
`corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py:30`. The nginx section the C1
landing adds must cite :22 (as this row's anchor does), not :30.

F8 — **The probe's frozen table matches the claims doc.** `plans/round69_c1_nginx_probe.py:57-107`
carries K1 `PPPPPPPP`, K2 `PPFPPPPP`, K3 `PPPPPPFF`, K4 `PPPPPFPP`, K5 `FPPPFPPP` — identical to
`plans/round-69-claims.md`. The lane-built server writes a log line matching all four leg-8 regexes
(`"%d/%b/%Y:%H:%M:%S %z"`, `GET`, 3-digit status, trailing quoted UA) and only when `--log` is set,
which is how K3 (`log=False`) reds legs 7-8.

## 6. Commands NOT run (stated explicitly)

- The C1 battery (`plans/round69_c1_nginx_probe.py --lane . --work … --receipt …`) and
  `--check-receipt` — not this seat's item; I did not observe any live P/F vector.
- The C2 gate, its `--selftest`, and any C2 receipt run.
- `scripts/sources-census.sh validate` and the anchor check against the lane file (the check was run
  only against the scratch clone carrying the proposed row; the lane run was the baseline).
- Any `git`/`jj` write: no commit, push, stage, stash, checkout, switch; no edit to `corpus/SOURCES.md`,
  `corpus/knowledge/*`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/lessons/*`, `plans/*`, `MANIFEST.json`
  or the fleet root. Only the scratch clone's `corpus/SOURCES.md` (in `/fast/scratch`) received the row.

## 7. Confidence and remaining unknowns

- **Observed:** fetch status/bytes/sha256, byte equality with the committed capture and
  `SHA256SUMS:111`, the HEAD blob digest, instruction content and line numbers, `task.toml` name,
  the 11-cell parse, and the anchor binding (`BIND`/`RESOLVED`, defects unchanged at 41).
- **[INFERENCE]:** which legs a live replay will print P/F — derived leg by leg from the grader
  source; this seat did not execute the battery. F1-F6 are source readings, not observations of a run.
- **Unresolved:** none blocking the row. The only open decision is the landing seat's: keep
  `SHA256SUMS:111` unprefixed (a prefixed `corpus/evidence/…/SHA256SUMS` would create a second named
  capture and a `capture-unanchored` defect), and cite grader :22 in the knowledge entry's new nginx
  section rather than the pypi grader's :30.
