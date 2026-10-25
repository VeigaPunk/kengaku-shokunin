# FxPerSubstring — per-row anchor byte mutation

Task: probe the S094/S097 draft anchors against the captured artifacts through `plans/sources_adopt.py --quote-file ... --artifact ... --url-map ...`. Scratch copy and capture files: `/tmp/r32f-FxPerSubstring/`. No production bytes changed. Python 3.14.8; no tool installed or updated.

## Control

From each row's anchor I retained one quote (S094 `# Validate with 0.05% tolerance`; S097 the 20-word abstract sentence) and wrote exactly one quoted span per row. Pristine gate output:

```text
QUOTE rows=2 spans=2 located=2 found=2 overlong=0 absent=0 malformed=0 cap=25 artifacts=abs.html,main.py mismatch=0 unmapped=0 urlmap=map.json entries=2
  ok S094 words=5 at main.py quote="# Validate with 0.05% tolerance" bound=main.py->https://github.com/hkust-nlp/Toolathlon
  ok S097 words=20 at abs.html quote="This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations." bound=abs.html->https://arxiv.org/abs/2412.05579
```

Exit: **0** (observed as successful tool completion).

## Mutants

Each mutant changes one byte-level text feature in only the selected row's quote: S094 changes `Validate` to `validate` (case); S097 collapses the space between `This` and `paper` by adding one space. Gate outputs:

```text
QUOTE rows=2 spans=2 located=1 found=1 overlong=0 absent=1 malformed=0 cap=25 artifacts=abs.html,main.py mismatch=0 unmapped=0 urlmap=map.json entries=2
  REFUSED S094 absent words=5 quote="# validate with 0.05% tolerance"
  ok S097 words=20 at abs.html quote="This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations." bound=abs.html->https://arxiv.org/abs/2412.05579
S094_exit=7
```

```text
QUOTE rows=2 spans=2 located=1 found=1 overlong=0 absent=1 malformed=0 cap=25 artifacts=abs.html,main.py mismatch=0 unmapped=0 urlmap=map.json entries=2
  ok S094 words=5 at main.py quote="# Validate with 0.05% tolerance" bound=main.py->https://github.com/hkust-nlp/Toolathlon
  REFUSED S097 absent words=20 quote="This  paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations."
S097_exit=7
```

Both one-byte quote mutants were detected as absent, **exit 7**. Requested exit 8 is not the applicable result: gate source documents exit 8 specifically for a URL mismatch after a quote is located (`sources_adopt.py` lines 450–461); a non-substring is exit 7. Thus the mutation probe confirms byte-substring enforcement, not exit 8. No quote mutation is expected to yield exit 8 absent a separate URL-map defect.

## Hash / restoration evidence

Pristine isolated quote-file SHA-256 before mutation: `03b49a4806e8d670bec2d7ddefa90a3f687b481c29cd51f8e381e69d1b13adbb`. Mutants were separate scratch files; pristine file remained unchanged. After the probes, its SHA-256 was again `03b49a4806e8d670bec2d7ddefa90a3f687b481c29cd51f8e381e69d1b13adbb` (matches). Mutant file hash (combined initial scratch probe) `dc2f528d4e8d6e910fcdfd6ab65d7d0eb81feffea0db1d3cf619020d2e439249`.

VERDICT: <substring-enforced>
