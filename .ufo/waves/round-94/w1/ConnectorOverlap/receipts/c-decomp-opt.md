# Receipt (c) — decomp -O3 vs grader plain-gcc divergence ownership, 2026-11-05

## The object (kengaku at T; byte-read from the detached clone)

`corpus/evidence/round94/decomp-opt-divergence.txt:1-4`:
```
# host observation (not a claim leg), 2026-11-05T19:00:32-03:00: the task image builds /app/decomp with gcc -O3
# (environment/Dockerfile:8); the grader rebuilds decomp2 with plain gcc (tests/test_outputs.py:15); decomp.c:60/:75
# printf("%s") an uninitialised stack buffer, so trailing bytes depend on codegen
# reference data.comp sha256 3a905a56e8f2937983412e6d3077cf2cec3eeb945c05b62502bb138d195b9131 (2264 B), from captured main.rs
d_o3 output_bytes=4870 sha256=8169d274e58df62f vs data.txt(4868 B): differs
d_o0 output_bytes=4868 sha256=0fc483d0fb31128d vs data.txt(4868 B): identical
```
Disambiguation: "decomp" = the write-compressor task's *decompressor source* (`environment/decomp.c`,
`tests/original-decomp.c`, sha `7f8d9ef6…` in the frozen table, plans/round-94-claims.md:23,26) — NOT decompilation.

## Queries and results (tracked `;!**/.ufo/**` unless said otherwise)

1. `(?i)(ghidra|dewolf|decompil)` over all 21 sibling lanes (full, incl. .ufo): 1146+ files, overwhelmingly
   audio-shokunin (their `rea` Ghidra/rizin/Frida MCP availability notes in reports/round-72…87). Scoped re-runs:
   - revenger-shokunin tracked: LOG.md:23,28 (round-1 REA provider notes); :1032-1037 (r73 registry 305 rows, 10 themes
     incl. "disassembly/decompilation ground truth", tool installs ghidra/yara/capa/…); :1055-1061 (r75: ghidra
     12.1.4 headless recon capability, `return 0x2a;` fixture); PROVINCE.md:22-29 (host engines census);
     SCORECARD.md:168 (`ghidra-headless-recon` row), :743-746 (decompiler correctness paths, SAILR S113);
     corpus/SOURCES.md:68-128 (S054 REA, S055 Ghidra, S056 GhidraMCP, S058 JADX, S080 Decomperson, S081 variable-name
     recovery, S082-S084 decompile-LLM papers, S113 SAILR "spurious gotos come from compiler optimizations");
     considerthese/2026-11-05.md:19-22 (rounds 89-92 honesty ledger). → owns decompiler ground truth; zero connection
     to the write-compressor rebuild-flag divergence.
   - tameshi-shokunin tracked: **zero hits**.
   - tsukuroi-shokunin tracked: single hit `tools/check-adjacency-anchors.py:120` — "- Demand context:
     ~/Projects/gamez/research/ (incl. decomp/recomp interest)" — demand-context line, no ownership.
2. `-O3` over kumitate/tameshi/tsukuroi/kaidoku tracked: single hit kaidoku
   `corpus/evidence/round-42/local-sources/S083/binary-BVOr2mgE.js:5132,8548-8552` — vendored JS (Ghidra MIPS target
   profile strings), incidental. No sibling documents an -O3/-O0 rebuild divergence.
3. `(?i)(gcc .*(O0|O3)|-(O0|O3) |uninitiali[sz]ed (stack|buffer)|codegen divergence|optimi[sz]ation level)` tracked,
   all lanes: audio (uninitialized-stack mechanism class in its own driver domain: `corpus/fixtures/measure_audio.py:33332`,
   `reports/round-68/r68-boundary.md:209-212` "stack reads zero on this build … formally nondeterministic",
   `reports/round-95/r95-scout.md:62,306-307`), game-dev-2d `reports/round-72/r72-critic.md:218` (`gcc -O0 -o c_reorder`
   pty probe), kaidoku `corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md:16-27` (corpus binaries compiled at
   -O0/-O1/-O2 as extraction inputs, per-key table k02–k12). None treats grader-vs-image rebuild flags.

## Ownership call

kengaku owns the divergence: it arises from kengaku's own R94-C1 replay design (the probe rebuilds the reference
`data.comp` from the captured `solve.sh`; the grader's own rebuild uses plain gcc), and the observation is committed at
T inside kengaku's evidence tree, self-labelled "not a claim leg". No sibling province (tameshi, tsukuroi, kumitate,
revenger, audio, kaidoku) owns any part; nothing to route out. Adjacent prior art worth citing if the class recurs:
kaidoku -O-level corpora (flag-dependent byte corpora), audio uninitialized-stack reports (mechanism class),
revenger S113 SAILR (compiler optimizations as decompiler noise — literature only).
