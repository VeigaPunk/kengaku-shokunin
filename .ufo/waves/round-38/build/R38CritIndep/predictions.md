# R38CritIndep — blind predictions (written BEFORE any probe run, from test_outputs.py only)

Source of truth used: corpus/evidence/round38/tb2-build-pmars/test_outputs.py (sha256 d9d2796d…)
+ case `-- requirement` text in build-pmars-dry-cases-freeze.txt.

Derivation rules extracted from test_outputs.py:
- T1 test_pmars_works: `/usr/local/bin/pmars` must exist; `echo -e 's\ns\ns\nq' | pmars -e X`
  output must have >=2 matches of `\b(\d{5})\s+\w+\.\w+`; and
  `pmars -b -r 50 -f flashpaper.red rave.red | tail -n 1` must satisfy re.match
  `Results: \d+ \d+ \d+` (prefix-anchored). run_shell_command strips output; on
  CalledProcessError with non-empty stdout returns it, with empty stdout raises.
- T2 test_headless_no_x11: `ldd /usr/local/bin/pmars` stdout must not contain
  libX11/libXt/libXext/libXaw. ldd failure with empty stdout -> CalledProcessError raised.
- T3 test_debian_source_used: `/app/pmars-*` glob non-empty (one level), [0]/debian exists().
- T4 test_built_from_source: `/app/pmars-*` non-empty, [0]/src exists, src.glob("*.c") non-empty.
- Order T1,T2,T3,T4.

| # | case | predicted tests | reason |
|---|---|---|---|
|1|canned-shape|PPPP|works+ldd clean+debian dir+dummy.c|
|2|canned-script|PFPP|script answers T1; ldd: not a dynamic executable, empty stdout -> error F|
|3|canned-static|PFPP|T1 ok; static ldd exits 1 empty stdout -> F|
|4|canned-x11-linked|PFPP|libX11 listed|
|5|canned-x11-dlopen|PPPP|no DT_NEEDED -> ldd lists nothing|
|6|results-two-ints|FPPP|two ints < three|
|7|results-trailing-text|PPPP|re.match prefix only|
|8|results-not-last|FPPP|tail -n 1 sees extra line|
|9|results-negative|FPPP|`\d+` cannot match `-1` after "Results: "|
|10|one-address|FPPP|needs >=2|
|11|four-digit-address|FPPP|`\d{5}` unsatisfied|
|12|canned-exit-nonzero|PPPP|e.output non-empty returned|
|13|nonexec-binary|FPPP|exists() true, shell 126 empty stdout -> error|
|14|silent-binary|FPPP|no addresses|
|15|path-split|PPPP|PATH /usr/local/sbin first -> script; ldd reads silent /usr/local/bin|
|16|no-debian-dir|PPFP|T3 only|
|17|debian-is-file|PPPP|Path.exists() on file true|
|18|src-no-c|PPPF|glob *.c empty|
|19|c-is-dir|PPPP|glob matches dirs|
|20|no-src-dir|PPPF|src missing|
|21|pmars-dir-elsewhere|PPFF|glob /app/pmars-* empty -> T3,T4|
|22|empty-tree|FFFF|all four miss|

Predicted aggregate: pass 7 (canned-shape, x11-dlopen, trailing-text, exit-nonzero, path-split,
debian-is-file, c-is-dir), fail 15.

## Extra cases (mine, predicted before run)

| cid | staged state | predicted | reason |
|---|---|---|---|
| x-results-leading-space | battle output `   Results: 12 34 78` | PPPP | run_shell_command .strip() removes the leading spaces before re.match |
| x-debian-broken-symlink | /app/pmars-0.9.4/debian is a dangling symlink, src/dummy.c present | PPFP | Path.exists() follows the link -> False |
| x-app-pmars-binary | /app/pmars is a working canned ELF binary, no /app/pmars-* entry | PPFF | glob "pmars-*" does not match "pmars" -> T3,T4 |
