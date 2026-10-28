# Wave-1 seat report — C1ExecBlindLabels (kengaku round 52, hyaku run 11)

- Seat: `C1ExecBlindLabels`, role executor, axis **novelty** (R52-C1 blind labels).
- Date: 2026-10-28. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (base tip `30801b47`).
- Blinding: I did **not** open `plans/round52_c1_grader_audit.py`'s output, the classifier seat's
  `records.json`/`notes.json`, or any other seat's labels. Labels below were fixed from my own
  reading of the fetched grader bytes before any counter/classifier output was consulted. I did
  read the counter *source* (regex definitions only) to disambiguate marker vocabulary; the
  class of every sampled task is **identical** under the claims-file vocabulary and the
  counter's regexes (verified, see "Vocabulary robustness").

## What I did

1. Read `plans/round-52-claims.md` §C1 in full (frozen marker vocabulary + class rules).
2. Loaded the frozen population `plans/round52-tasks.json` (89 tasks, pin
   `2fd12b88aafdd04a52c298e3940bcb189f9766d6`).
3. Sampled by the seat rule "every task whose index in sorted order is a multiple of 3"
   (0-based, alphabetical task-id sort). **Note:** that rule over 89 tasks yields **30** tasks,
   not the 24 stated in the seat item (1-based indexing yields 29; no indexing yields 24). I
   labeled **all 30 rule-selected tasks** and additionally shipped `labels-prefix24.json`
   (the first 24 of the rule sequence, sorted indices 0–69) so the L1 can take the exact
   24-row count without re-running anything.
4. Fetched each task's **primary grader** bytes from
   `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/<task>/tests/test_outputs.py`
   (all 89 tasks have a top-level `tests/test_outputs.py`, so that is the primary grader per
   claims §C1 for every sampled task; no `environment/tests/test_outputs.py` fallback needed).
5. Read all 30 graders end-to-end myself and assigned a class per the frozen rules
   (first match wins: V1 presence-only → V2 behavioural → V3 content-check → V4
   assertion-sparse ≤2 tests → V0 other).
6. Cross-checked every label with an independent mechanical application of the claims-file
   marker vocabulary (`tmp/mech.json`, scratch); hand labels and mechanical labels agreed 30/30.

## Exact commands

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r52/C1ExecBlindLabels/{tmp,graders}
# sample selection (python3): sorted(tasks); indices i%3==0; primary grader path per claims §C1
# fetch (30 parallel curl calls, python3 ThreadPoolExecutor):
curl -fsS -o graders/<task>/tests/test_outputs.py \
  "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/<task>/tests/test_outputs.py"
# classification: python3 regex passes over fetched bytes (claims §C1 vocabulary), then full manual read
sha256sum of each fetched file -> SHA256SUMS (receipt)
rm -rf -- /fast/scratch/hyaku/kengaku-r52/C1ExecBlindLabels/   # done after copying receipts
```

No tools were installed or upgraded (nothing needed; RULES.md channel order unused).

## Measured numbers

- Fetched: **30/30** graders, all HTTP 200, **132,304 bytes** total, zero empty responses,
  zero 404s. Digests in `SHA256SUMS` (30 lines, `<sha256>  <path>  task=<t> idx=<i>`).
- Label histogram (30 labels): **V1=1, V2=18, V3=11, V4=0, V0=0**.
- Prefix-24 subset (indices 0–69) histogram: **V1=1, V2=16, V3=7, V4=0, V0=0**.
- Feature counts per task (P=presence, C=content, B=behaviour, n=`def test_` lines):

| idx | task | class | P | C | B | n |
|---|---|---|---|---|---|---|
| 0 | adaptive-rejection-sampler | V2 | 1 | 1 | 1 | 9 |
| 3 | build-cython-ext | V2 | 1 | 0 | 1 | 11 |
| 6 | caffe-cifar-10 | V2 | 1 | 1 | 1 | 6 |
| 9 | circuit-fibsqrt | V2 | 1 | 1 | 1 | 3 |
| 12 | compile-compcert | V2 | 1 | 1 | 1 | 3 |
| 15 | count-dataset-tokens | V3 | 0 | 1 | 0 | 1 |
| 18 | db-wal-recovery | V3 | 1 | 1 | 0 | 7 |
| 21 | dna-insert | V2 | 1 | 1 | 1 | 1 |
| 24 | feal-differential-cryptanalysis | V2 | 0 | 1 | 1 | 1 |
| 27 | financial-document-processor | V3 | 1 | 1 | 0 | 7 |
| 30 | fix-ocaml-gc | V3 | 1 | 1 | 0 | 1 |
| 33 | git-multibranch | V2 | 0 | 1 | 1 | 1 |
| 36 | hf-model-inference | V2 | 1 | 0 | 1 | 4 |
| 39 | large-scale-text-editing | V2 | 1 | 1 | 1 | 5 |
| 42 | log-summary-date-ranges | V3 | 1 | 1 | 0 | 2 |
| 45 | make-mips-interpreter | V2 | 1 | 1 | 1 | 3 |
| 48 | model-extraction-relu-logits | V2 | 1 | 1 | 1 | 1 |
| 51 | mteb-retrieve | V3 | 1 | 1 | 0 | 2 |
| 54 | openssl-selfsigned-cert | V2 | 1 | 1 | 1 | 6 |
| 57 | path-tracing | V2 | 1 | 1 | 1 | 5 |
| 60 | polyglot-rust-c | V2 | 0 | 1 | 1 | 1 |
| 63 | prove-plus-comm | V2 | 1 | 1 | 1 | 4 |
| 66 | pytorch-model-recovery | V1 | 1 | 0 | 0 | 5 |
| 69 | query-optimize | V3 | 1 | 1 | 0 | 6 |
| 72 | regex-log | V3 | 1 | 1 | 0 | 1 |
| 75 | sam-cell-seg | V2 | 1 | 1 | 1 | 9 |
| 78 | sparql-university | V3 | 1 | 1 | 0 | 3 |
| 81 | torch-pipeline-parallelism | V3 | 1 | 1 | 0 | 3 |
| 84 | tune-mjcf | V3 | 1 | 1 | 0 | 4 |
| 87 | winning-avg-corewars | V2 | 1 | 1 | 1 | 3 |

(The rule-selected tasks at indices 72, 75, 78, 81, 84, 87 are exactly the six beyond the
24-task prefix.)

## Vocabulary robustness

The claims-file marker vocabulary and the frozen counter's regexes differ slightly (counter
adds `os.path.isfile` to PRESENCE, `assert … in …` to CONTENT, and requires `curl ` with a
trailing space in BEHAVIOUR). Re-running my classification with the counter's regexes changes
**no** label of the 30 (divergences: none). The only marker-level difference found:
`hf-model-inference` gains a content hit from `assert "positive" in result[...]` under the
counter's extra CONTENT alternative; its class stays V2 because the behaviour marker
(`requests`) precedes content in the frozen rule order.

## Hard-to-decide labels (with reasons)

1. **pytorch-model-recovery → V1.** The only markers the frozen vocabulary sees are
   `Path(...).exists()` presence checks; the grader's real work (`torch.load`, `torch.allclose`
   comparisons against `/tests/weights_gtruth.pt`) is content comparison but *not* in the
   content-marker list, so the rule yields V1 (a triage candidate) even though the grader is
   substantively strict. Vocabulary gap, honestly labelled per the frozen rules.
2. **count-dataset-tokens → V3 (looks sparse).** One test, 467 bytes, reads `answer.txt` and
   asserts one substring. Reads as assertion-sparse by eye, but it has a content marker
   (`read_text`) and no presence marker, so V3 wins over V4 in the frozen rule order.
3. **feal-differential-cryptanalysis → V2 (spurious content hit).** Its content-marker hit
   comes only from the substring `open(` inside `os.popen(`. Class is V2 anyway
   (`os.popen` behaviour), but the C flag is a vocabulary artifact worth knowing when reading
   the counter's feature columns.
4. **polyglot-rust-c → V2.** No presence marker although the grader lists `/app/polyglot`
   (`os.listdir` is not in the vocabulary); content hit again from `open(` inside `os.popen(`.
5. **git-multibranch → V2.** Most markers (`curl`, `apt-get`) sit inside the embedded
   `verify.sh` shell string the test writes; the Python-level behaviour marker is
   `os.popen("bash verify.sh")`. Rule says V2 either way.
6. **torch-pipeline-parallelism → V3.** It spawns multiprocessing workers
   (`torch.multiprocessing.spawn`), but the frozen file-level behaviour vocabulary
   (`subprocess|os.system|os.popen|Popen|socket|requests|urllib|http.client|docker|bwrap|curl`)
   does not include `multiprocessing`/`dist.`, so V3 is the rule-correct class.

## Files produced (absolute paths)

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecBlindLabels/labels.json` — primary deliverable (30 labels, `{"labels":[{task,class,why≤20w}]}`)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecBlindLabels/labels-prefix24.json` — same labels, first 24 of the stride-3 sequence (indices 0–69)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecBlindLabels/SHA256SUMS` — digest receipt for the 30 fetched graders
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecBlindLabels/sample.json` — the sampled (index, task, path) triples
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ExecBlindLabels.md` — scoped findings copy (same content as this report, per the seat Target line)

## Risks / notes for the L1

- The seat item's "sample of 24 tasks" is arithmetically inconsistent with its own rule
  (stride 3 over 89 sorted tasks = 30). `labels.json` carries all 30 rule-selected tasks;
  `labels-prefix24.json` is the deterministic 24-row subset. Merge either; both are blind.
- No repo tree, state file, or fleet-root file was written; no git/jj mutation anywhere; no
  counter was run; scratch dir removed after receipt copy.
