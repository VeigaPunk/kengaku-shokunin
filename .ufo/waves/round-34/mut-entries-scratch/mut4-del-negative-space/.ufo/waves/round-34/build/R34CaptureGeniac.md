# R34CaptureGeniac — staged S105 source hand-check

- Target: S105, METI GENIAC phase-1 performance-evaluation results, Internet Archive snapshot `20251118034714`.
- Retrieval: `curl -sL --max-time 60 -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" "http://web.archive.org/web/20251118034714/https://www.meti.go.jp/policy/mono_info_service/geniac/selection_1/result_1/index.html" -o /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/assimilation/captures/geniac-s105.html`
- Capture evidence: `wc -c /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/assimilation/captures/geniac-s105.html` → `13030 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/assimilation/captures/geniac-s105.html`; `sha256sum` on that same path → `2f46a13e672db0ed6f2f5deeec302de03224f5270a65d5ec57b78cea5129b341`.
- Text check: `python3 -c 'from html.parser import HTMLParser; from pathlib import Path; import re,sys; p=Path(sys.argv[1]); class_dummy=0; text=re.sub(r"\\s+"," ",re.sub(r"<[^>]+>"," ",p.read_text(errors="replace"))); target="GENIACでは、公平性担保のため完全に未知なテストデータを用いて性能評価を行うことが重要であるという観点から、Weights and Biases社と協業し、ホールド・アウトデータ(最終的な性能評価を行うための非公開のデータセット)を生成・評価を行いました。"; print("target_found="+str(target in text)); print(text)' /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/assimilation/captures/geniac-s105.html` → `target_found=True`. The normalized text is available in the capture inspection output (captured HTML text; not a live-source assertion).
- Located quote (capture, normalized text, section “性能評価結果（日本語）(※2024年８月時点)”): 「以下の2つのベンチマークを用いて、日本語の性能評価を行いました。」 (16 Japanese whitespace-delimited words/tokens by ordinary segmentation; within 25 words).
- Benchmark names immediately following: `Jaster-GENIAC-v0.1` and `JMT-Bench-GENIAC-v0.1`. The page also names English benchmarks later: `MMLU-GENIAC-v0.1` and `MT-Bench-GENIAC-v0.1`.
- S105 hand-check: **found**. The exact frozen hold-out-data sentence occurs in the normalized captured text, and the Japanese benchmark names follow it.
- Scope: wrote only the capture under `assimilation/captures/` and this assigned report; no source-repo writes, lane corpus/plan changes, installs, or verification suite runs.

VERDICT: geniac-s105 found
