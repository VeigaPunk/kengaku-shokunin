# R34RowsQuarantine — adopted-row drafting blocked by missing source evidence

**Axis:** coverage. **Frozen basis:** `plans/round-34-claims.md` (freeze commit `adaf25dfd27dedfc1bf25f308576a6f2c8ad64ae`), §10 requires payload-absent staged S091/S105 sources to be hand-checked and adopted only if their cited quotes are located in this round's captures.

## Evidence

- Read `assimilation/captures/nec-s091.html`: 418-byte Akamai Access Denied response; lines 6–8 show the denied NEC URL and edgesuite reference. The companion `build/R34CaptureNec.md` reports the retrieval command and output: `curl -sL --max-time 40 -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" https://jpn.nec.com/techrep/journal/g23/n02/230212.html -o .../nec-s091.html && wc -c ... && sha256sum ...`; output size 418 and SHA-256 `967e4c244fa28577dc3dc9e5ba282c495372607ca5e32bc7a82b06bc75fdeed3`. Its extraction reports no RAKUDA paragraph or section 6.2 context. The staged source quote therefore is not located in the permitted capture.
- Read `assimilation/captures/geniac-s105.html`: archived METI page contains the hold-out description at captured HTML line 112, under `性能評価結果（日本語）(※2024年８月時点)` (line 111). Located quote (20 Japanese whitespace-delimited tokens; under 25 words): 「ホールド・アウトデータ(最終的な性能評価を行うための非公開のデータセット)を生成・評価を行いました。」 This supports the limited claim that the page describes generating/evaluating a non-public hold-out dataset for final evaluation; it does not independently establish how it was used for each model.

## Gate inputs

No `append-rows.md`, `quotes.json`, or `url-map.json` was written: S108 cannot honestly be adopted with a located quote, and the requested pair of adopted rows is a joint deliverable. In particular, neither a fabricated S108 quote nor an S109-only gate payload would satisfy the frozen admission rule. The requested build subdirectory was absent when inspected; this report is at the specified report path.

## Exact observed evidence commands and outputs

- `read /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/assimilation/captures/nec-s091.html` → HTML Access Denied page, 10 displayed lines; no article text.
- `read /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/assimilation/captures/geniac-s105.html:70-170` → captured line 112 includes the hold-out passage.
- `read /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/build/R34CaptureNec.md` → records curl command, size/hash, and explicit absent-quote finding.
- `read /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/assimilation/quarantine-slice` → `S091 payload-absent`, `S105 payload-absent`.

**Touched surface:** this report only. No tool installed or updated. No product, registry, package, or gate files edited. No checks run.

**VERDICT: rows-quarantine-not-drafted (S108 quote absent from capture; S109 quote located)**
