# F38EntryQuotes receipts (kengaku r38 w2 falsify, 2026-10-26)

Target: `corpus/knowledge/tb2-build-pmars-grader.md` — the 28 `## Located quotes` rows and every
sentence citing a `corpus/evidence/round38/build-pmars-probe.txt` case.

## R1 — capture integrity
`cd corpus/evidence/round38/tb2-build-pmars && sha256sum -c SHA256SUMS` → all five files `OK`.
Pinned raw re-fetch at `2fd12b88` (falsifier clause (a)):
- `curl -sS .../build-pmars/tests/test_outputs.py | sha256sum` →
  `d9d2796ddc19cf8159670567e174ea377e2bce675bf3451d5951c045b01f4e85` = capture digest ✓
- `curl -sS .../build-pmars/instruction.md | sha256sum` →
  `1606850579342a8b8f2189de0e499fae6be21198150d8dd1e4d18c2efbcf3b82` = capture digest ✓
- `curl -sS .../build-pmars/environment/Dockerfile | cat -n` → line 9 is exactly
  `COPY warriors/flashpaper.red warriors/rave.red /app/` (doc's "line 9 at `2fd12b88`" ✓).

## R2 — located-quote check (mechanical)
Parsed all 28 rows of `## Located quotes`; for each, read the cited `sed -n '<n>p'` line from the
capture and tested verbatim substring + word count.
Result: `TOTAL=28 OK=28 BAD=0` (verbatim=True, 3 ≤ words ≤ 25 for every row; word counts span 3
(`test_outputs.py:23`,`:31`,`:62`,`:84`) to 17 (`instruction.md:9`)). Per-row output retained in the
seat transcript.

## R3 — frozen-probe re-run (falsifier clause (b))
`S=/fast/scratch/hyaku/kengaku-r38/F38EntryQuotes; TMPDIR=$S python3 plans/build_pmars_probe.py
--lane . --work $S > $S/rerun-receipt.txt`; rc=0;
`diff corpus/evidence/round38/build-pmars-probe.txt $S/rerun-receipt.txt` → empty (byte-equal);
tail line `cases=22 observed_pass=7 observed_fail=15 mismatches=0`.
Copy: `rerun-receipt-byte-equal.txt`.

## R4 — receipt-derived label arithmetic (V7 over ALL violating cases)
Parsed 22 CASE lines. Carriers/pass/fail → label:
`debian-source 22 7 15 partly; debugger-works 22 7 15 partly; extract-to-app 22 7 15 partly;
from-source 22 7 15 partly; install-path 4 1 3 partly; no-x11 3 1 2 partly; results-format 5 1 4 partly`.
All 14 map-table (tag, case, direction) citations: OK (tag in violates-set, observed verdict matches).
Load-bearing: drop `canned-x11-dlopen` → `no-x11` becomes `enforced` (carriers left: empty-tree,
canned-x11-linked, both fail) — doc's claim reproduced.
Drop-checks ("no label moves"): results-negative→results-format, pmars-dir-elsewhere→extract-to-app,
four-digit-address→debugger-works, silent-binary→install-path: every label stays `partly`. ✓
Drop `canned-shape`: from-source/debian-source/extract-to-app/debugger-works each keep 6 pass
carriers → still `partly` (basis of finding F1).

## R5 — per-case letters vs doc citations
All 22 (case, observed, tests, predicted_tests, match=yes) checked against the doc's Summary,
per-line readings, group table and Findings §1–8: all OK (e.g. empty-tree FFFF; canned-script,
canned-static, canned-x11-linked PFPP + `test_headless_no_x11:error=CalledProcessError`;
no-debian-dir PPFP; no-src-dir, src-no-c PPPF; pmars-dir-elsewhere PPFF; seven pass cases PPPP).

## R6 — instrument cross-check (`plans/build_pmars_probe.py`, sha256
`32f0771cd5c4129a9a9795e3016a4f1c2cf660003f09cb4d719731fd5825c24a` = doc's `32f0771c…25c24a`)
- `PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"` (Debian default order) ✓
- bwrap: `--unshare-net --unshare-pid --unshare-ipc`, `--ro-bind /usr /usr`, `--tmpfs /tmp`,
  ro-binds of work dirs to `/usr/local/bin`, `/usr/local/sbin`, `/app`, `--dir /tests` + ro-bind of
  only `test_outputs.py`, `--chdir /app` ✓
- verdict mapping: `except AssertionError: F`; `except Exception as e: F error=<class>`; return P;
  `overall` = pass iff PPPP ✓
- `C_SRC` is 21 lines; its `main` scans argv: `for (int i = 1; i < argc; i++) if (strcmp(argv[i],
  "-b") == 0) battle = 1;` — basis of finding F2; script variant: `for a in "$@"; do if [ "$a" =
  "-b" ]` ✓; DLX11 branch only `dlopen("libX11.so.6", RTLD_LAZY); (void)h;` — no X11 symbol called ✓
- x11 variant `-DLINKX11 -Wl,--no-as-needed -lX11`; `canned-exit-nonzero` `Art(exit=3)` ✓
- no case stages `rave.red`/`flashpaper.red` (grep of CASES/staging code) ✓

## R7 — other cited artifacts
- `test.sh:18-29`: `uvx -p 3.13`, `-w pytest==8.4.1`, reward `1` iff pytest exits 0 ✓
- `solve.sh`: deb-src `:8`, pinned installs `:12-16`, `apt-get source pmars` `:20`,
  `-DXWINGRAPHX` strip `:25`, `LIB = -lncurses` `:26`, `install -m 0755` `:29` ✓
- `task.toml`: verifier/agent timeouts `:22`/`:25`, image `:29`, `allow_internet = true` `:34` ✓
- `plans/round-38-claims.md:8-15`: `**Disclosure…**` paragraph starts at line 8 ✓
- `.ufo/waves/round-38/build/R38CritProbe.md` §3 lists exactly five contestable tags,
  `canned-x11-dlopen` marked LOAD-BEARING with the strace `openat … /usr/lib/libX11.so.6` evidence ✓
- host shell: `ls -l /usr/bin/sh` → `sh -> bash` (doc's "the sandbox shell is the host's bash") ✓
