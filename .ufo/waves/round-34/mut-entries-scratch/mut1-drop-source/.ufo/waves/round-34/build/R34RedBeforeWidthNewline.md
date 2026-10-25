# R34 width/newline red-before

Scoped item: calibration red-before evidence only. Frozen claims were read first: `plans/round-34-claims.md` lines 71-101 assigns width/newline to N5/N6 and requires one red-before receipt per class under `.ufo/waves/round-34/falsify/red-before/`.

Receipt: `.ufo/waves/round-34/falsify/red-before/width-newline.txt`.

Evidence command (cwd `/home/vgpnk/Projects/shokunin/kengaku-shokunin`):

```
grep -n ':35-38' corpus/lessons/round-31.md
```
Actual output: no match; actual exit code 1.

```
grep -n '78–81' corpus/lessons/round-30.md
```
Actual output: no match; actual exit code 1.

Located context: `corpus/lessons/round-31.md` lines 196-200 (read result) discusses the `:35-38` locator and corrected `:39-40`; `corpus/lessons/round-30.md` lines 72-81 (read result) includes the section whose citation is referenced as `:78-81` in the round-31 verifier spotcheck. Important limitation: the requested sandbox-export mutations and grep against those mutated copies were not executed. Consequently these actual exit-1 probes show literal misses in the source tree, not measured post-mutation red-before behavior. Receipt records that limitation rather than claiming otherwise.

VERDICT: red-before-width-newline miss-proven
