# Exact executed command forms

Shell calls (cwd fleet root unless absolute paths control destination):
```sh
bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
mkdir -p /fast/scratch/hyaku/kengaku-r53/C1RevSources2 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C1RevSources2 && TMPDIR=/fast/scratch/hyaku/kengaku-r53/C1RevSources2 git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r53/C1RevSources2/lane && git -C /fast/scratch/hyaku/kengaku-r53/C1RevSources2/lane rev-parse --show-toplevel && git -C /fast/scratch/hyaku/kengaku-r53/C1RevSources2/lane rev-parse HEAD
```

Live opens ran in the persistent Python Eval kernel, not a shell. Exact fetch API:
```python
req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 C1RevSources2 source review'})
with urllib.request.urlopen(req,timeout=50) as f:
    data=f.read(1048577)
```
`u`, HTTP result, final URL, bytes and digest for each request are in `wave1-fetch-results.json`, `extra-fetch-results.json`, and `lit-fetch-results.json`. Schuler full PDF needed one additional `urllib.request.urlopen(u,timeout=60)` with `f.read()` (1,492,763 bytes, scratch only). Wayback gzip bodies were decoded with `gzip.decompress(b)`. Downloads used `concurrent.futures.ThreadPoolExecutor(max_workers=16)`, then 12, 8 and 15 for independent batches.

PDF extraction used exact argv templates via `subprocess.run`:
```python
['pdftotext','-layout',str(dest),str(out)]
['pdftotext',f['file'],f['textfile']]
['pdftotext',str(scratch/'schuler-full.pdf'),str(scratch/'schuler-full.txt')]
```
The later plain extraction replaced layout extraction because columns interleave in layout mode. HTML text was `unescape(re.sub('<[^>]+>',' ',s))`; PDF whitespace was normalized using `' '.join(s.split())`. GitHub API `body` fields were decoded using `json.loads`; raw README and PR241 `.diff` were additionally opened for U13/U27. Quotes were checked as substrings, not inferred from page titles or snippets.

Required census, executed via `subprocess.run` with `env={**os.environ,'TMPDIR':str(scratch)}`:
```sh
TMPDIR=/fast/scratch/hyaku/kengaku-r53/C1RevSources2 bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /fast/scratch/hyaku/kengaku-r53/C1RevSources2/lane/corpus/SOURCES-review.md
```
The retained assembly and id map reproduce the input after scratch cleanup. Initial wave-1 fallback assembly was also run with that argv; the final receipt supersedes it. Final corrected B wording was included in the last run.

Final scratch cleanup (exit 0):
```sh
rm -rf -- /fast/scratch/hyaku/kengaku-r53/C1RevSources2
```
