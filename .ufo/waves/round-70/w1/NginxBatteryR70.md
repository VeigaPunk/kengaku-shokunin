# NginxBatteryR70 — R70-C1 battery replay (seat report)

Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (master tip at run time
`384e9c76415e78093623b3eaff262423a89dbc3e`; base of the frozen claims `502893ad`).
Scratch: `/fast/scratch/hyaku/kengaku-r70/NginxBatteryR70`.
Item: run the frozen R70-C1 seven-case battery once and write the receipt of record.

## Verdict

**R70-C1 battery: PASS.** All seven cases produced exactly their frozen eight-leg vectors
(`mismatches=0`), every one of the eight grader legs is observed `P` in at least one case
and `F` in at least one case (`seen_p=8 seen_f=8`), all seven `case_sha256` values equal the
frozen `CASE_SHA` table, the receipt's PROBE, PROBE_BLOB and GRADER shas re-derive from
committed bytes, and `--check-receipt` exits 0 with an empty defect list. **No case's
observed vector differs from its frozen vector.** No frozen element was edited.

## What I ran

All commands from `L`; stdout/stderr captured under `W/NginxBatteryR70/` (W =
`.ufo/waves/round-70/w1`).

1. Preconditions.
   - `mkdir -p S` (S = `/fast/scratch/hyaku/kengaku-r70/NginxBatteryR70`) → rc 0.
   - `ss -ltnp '( sport = :8080 )'` → rc 0, no listener lines (header only):
     ```
     State Recv-Q Send-Q Local Address:Port Peer Address:PortProcess
     ss_rc=0
     ```
     Saved verbatim: `W/NginxBatteryR70/port-check.txt`. Port 8080 free before the run.
   - `which bwrap` → `/usr/bin/bwrap`; `bwrap --version` → `bubblewrap 0.13.1`.
   - Grader file sha256 `045cc716…4acda0` = `corpus/evidence/round52/graders/SHA256SUMS:111`.
   - Frozen table pre-check: `python3 plans/round70_c1_nginx_probe.py --render-table` → rc 0
     (full output `S/render-table.txt`); prints
     `FROZEN-VECTOR PPPPPPPP/PPFPPPPP/PPPPPPFF/PPPPPFPP/FPPPFPPP/PFFFPPFF/PPPFPPPP`,
     `LEG-COVERAGE-FROZEN legs=8 seen_p=8 seen_f=8`, per-leg counts
     `installed p=6 f=1`, `running p=6 f=1`, `index p=5 f=2`, `custom_404 p=5 f=2`,
     `config_syntax p=6 f=1`, `config_settings p=6 f=1`, `log_creation p=5 f=2`,
     `log_format p=5 f=2` — identical to `plans/round-70-claims.md` R70-C1.

2. Battery of record (one run):
   ```
   python3 plans/round70_c1_nginx_probe.py --lane . \
     --work /fast/scratch/hyaku/kengaku-r70/NginxBatteryR70/work \
     --receipt corpus/evidence/round70/nginx/receipt.txt \
     --evidence-dir corpus/evidence/round70/nginx/sandbox
   ```
   rc=0 (wall ~17 s). The instrument writes the receipt to the named path and prints nothing
   on success, so `W/NginxBatteryR70/stdout.txt` contains exactly `rc=0`.
   Note: the receipt parent directory did not exist; I created
   `corpus/evidence/round70/nginx/` (an assigned path) before the run. The work dir must
   pre-exist (`SETUP work-dir-required` otherwise — observed on a discarded first invocation
   with rc=2; that invocation wrote no receipt and staged nothing under the lane).

3. Checker of record:
   ```
   python3 plans/round70_c1_nginx_probe.py --check-receipt corpus/evidence/round70/nginx/receipt.txt
   ```
   rc=0; `W/NginxBatteryR70/check.txt`:
   ```
   CHECK ok cases=7 legs=8 seen_p=8 seen_f=8
   CHECK stored-predicate=pass derived=pass
   PREDICATE R70-C1 pass
   rc=0
   ```

4. Supplementary calibration arm (read-only w.r.t. lane; scratch only):
   ```
   python3 plans/round70_c1_nginx_probe.py --selftest \
     --work /fast/scratch/hyaku/kengaku-r70/NginxBatteryR70/selftest-work \
     --green-receipt corpus/evidence/round70/nginx/receipt.txt
   ```
   rc=0 (`W/NginxBatteryR70/selftest.txt`): `RED r1..r7 rc=1 refused=True` (7/7),
   `ACCEPT synthetic rc=0 accepted=True`, `PATH-INDEPENDENT sha_equal=True`,
   `STAGED-STATE changes_on_byte=True`, `GREEN receipt rc=0 accepted=True`,
   `SELFTEST red_refused=7/7 green_ok=1 accept_ok=1 ok=True`.

Tool installs/upgrades: none.

## Receipt lines (verbatim)

From `corpus/evidence/round70/nginx/receipt.txt` (3611 bytes, sha256
`237d28a154a64b06173a04c2ac3932dfd5e7a45441462269da2bdf838e2dc26a`):

```
PROBE plans/round70_c1_nginx_probe.py sha256 9aef6d33abc965f52a965b2f9197b78d257dc76003ddc124ca0e692a4fdbbe90
PROBE_BLOB plans/round70_c1_nginx_probe.py sha256 9aef6d33abc965f52a965b2f9197b78d257dc76003ddc124ca0e692a4fdbbe90
PROBE_VERSION 1
GRADER corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py sha256 045cc716c14efde3b0dcff5fc7c85ec5d18bfc6ce66f8b40a418fa2a3a4acda0 pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6
PORT 8080 free-at-start=True lock=/home/vgpnk/.local/share/kengaku-r70/port-8080.lock
CASE K1 case_sha256=0cf77ab849376a311f85b6cf47d1b2fd61fd21e0644720fb02e541e8ed074fb0 server_pid=2831758 sandbox_rc=0
CASE K2 case_sha256=c072ee5fa3f076d69a222ec173327a855f471029bf70bb78b13180b790012a0b server_pid=2834960 sandbox_rc=0
CASE K3 case_sha256=286db51eb5bab3aad7c3c3fb7ed6c4e2019940d6f3f1d6641269b33be946be34 server_pid=2838300 sandbox_rc=0
CASE K4 case_sha256=22ee1ff893a4acde45241c89fe55fc2c2f4bc23fd2ce452627605a436446c788 server_pid=2840297 sandbox_rc=0
CASE K5 case_sha256=5690e1e15975681496705203950f46436921a9e6e7911a7ab930a2e4199bb926 server_pid=2842033 sandbox_rc=0
CASE K6 case_sha256=d4035f6f30bb3f1a63b09ce268e57f7fb3eea788d8b28a4f393717d683452437 server_pid=None sandbox_rc=0
CASE K7 case_sha256=07eb2fd3f850a1b4b34b3518bca7985fec839bec6dba97dc12e0e593e0a91855 server_pid=2845742 sandbox_rc=0
VECTOR K1 PPPPPPPP expected PPPPPPPP agree=True
VECTOR K2 PPFPPPPP expected PPFPPPPP agree=True
VECTOR K3 PPPPPPFF expected PPPPPPFF agree=True
VECTOR K4 PPPPPFPP expected PPPPPFPP agree=True
VECTOR K5 FPPPFPPP expected FPPPFPPP agree=True
VECTOR K6 PFFFPPFF expected PFFFPPFF agree=True
VECTOR K7 PPPFPPPP expected PPPFPPPP agree=True
LEG-COVERAGE legs=8 seen_p=8 seen_f=8
SUMMARY cases=7 legs=56 mismatches=0 setup=0
PREDICATE R70-C1 pass
```

(Per-leg `TEST` lines are in the receipt, 8 per case = 56; each matches the frozen vector
character by character.)

**Cases whose observed vector differs from its frozen vector: none (0 of 7).**

## Independent re-derivation

- `git cat-file blob master:plans/round70_c1_nginx_probe.py | sha256sum` →
  `9aef6d33…fdbbe90`, equal to the receipt's `PROBE` **and** `PROBE_BLOB` lines and to
  `sha256sum plans/round70_c1_nginx_probe.py` (instrument unmodified between freeze and run).
- `sha256sum corpus/evidence/round52/graders/nginx-request-logging/tests/test_outputs.py` →
  `045cc716…4acda0`, equal to the receipt's `GRADER` line and `SHA256SUMS:111`.
- All seven `case_sha256` values match the frozen `CASE_SHA` prefixes in
  `plans/round70-claims.md` R70-C1 exactly (checked mechanically:
  `frozen_match=True` for K1–K7).
- Before → after target 1: `git cat-file -e 502893ad:corpus/evidence/round70/nginx/receipt.txt`
  → `fatal: path ... exists on disk, but not in '502893ad'`, rc=128; the receipt now exists
  with `PREDICATE R70-C1 pass`.
- Live witness (named limitation (i)): per-case `server_pid` lines are non-null for K1–K5,
  K7 and `None` for K6 (no service by construction). `sandbox/` holds seven captures
  (`K1..K7-sandbox.txt`), 8 new files total under
  `corpus/evidence/round70/nginx/` (receipt + 7 sandbox captures). K6's capture shows the
  grader's own text `Nginx is not running on port 8080` (leg 2) and
  `E:ConnectionError` on legs 3, 4, 7, 8; K7's capture shows leg 4 only:
  `Expected 'Page not found - Please check your URL', but got 'Page not found - Please check your URL!'`.

## Scope boundary

This seat ran the battery and wrote the receipt/evidence only. The C1 knowledge-side targets
(`SKILL.md` `executed 3 of 8`, the `S242` row) and all of R70-C2 are other seats' items and
were not touched or claimed here. No predicate, case table, vector, digest, kill rule or
target was edited; no git/jj mutation was run.

## Risks / limitations observed (from the freeze, confirmed by this run)

- `--check-receipt` re-derives text fields and cannot prove a live run; the `server_pid`
  lines and the seven sandbox captures are the live witness.
- The `nginx` binary is a lane-written shim answering `-t`; this prices the grader's config
  file, HTTP-body and log legs, not nginx's own syntax checker.
- K6 stages "no service" as a whole candidate state, so its five red legs are not
  independently isolated; K7 isolates leg 4 with the service up.
- `case_sha256` binds staged inputs, not the grader's behaviour.

## Blockers

None.
