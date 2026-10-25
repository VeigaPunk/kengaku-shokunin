# R34 TB2 evaluator capture

## Scope and evidence
Captured the pinned `protein-assembly` evaluator at commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6` into `.ufo/waves/round-34/assimilation/captures/tb2-eval/`.

Command: `wc -c -l test_outputs.py test.sh` (run in capture directory)
Output:
```
  73 3847 test_outputs.py
  30  631 test.sh
 103 4478 total
```
Command: `sha256sum test_outputs.py test.sh`
Output:
```
44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582  test_outputs.py
9ede46648fc67c9ce61975503de3e0fcff0b0fb110adc0f9e1d240a608c267b5  test.sh
```
The same hashes are in `assimilation/captures/tb2-eval/SHA256SUMS`.

## Located evaluator rules
All locations below are in captured `test_outputs.py`; quotes are verbatim.

- Path and basic single-line/content/maximum-length assertions: lines 13–23:
  - 14: `    assert gblock_path.exists(), f"File {gblock_path} does not exist."` (path literal initialized at 13: `    gblock_path = Path("/app/gblock.txt")`)
  - 19: `    assert len(lines) == 1, "Invalid number of lines in gblock.txt."`
  - 22: `    assert re.fullmatch(r"[atcg]+", gblock), "gBlock must contain only A, T, C, G."`
  - 23: `    assert len(gblock) <= 3000, "gBlock must be at most 3000 nucleotides."`
- Fusion-order assertion line 42: `    assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx, (`. Protein sequence literals occur at lines 28, 31, 32, 35, 36 respectively: flag `flag_aa = "DYKDDDDK"`; donor starts `donor_aa = "GSSHHHHHHSSGENLYFQGHMVSKGEELFTGVVPILVELDGDVNGHKFSVRGEGEGDATNGKLTLKFICTTGKLPVPWPTLVTTFGYGVACFSRYPDHMKQHDFFKSAMPEGYVQERTISFKDDGTYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNFNSHNVYITADKQKNGIKANFKIRHNVEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSHQSALSKDPNEKRDHMVLLEFVTAAGITHGMDELYK"`; DHFR literal begins `dhfr_aa = "ISLIAALAVDRVIGMENAMPWNLPADLAWFKRNTLNKPVIMGRHTWESIGRPLPGRKNIILSSQPGTDDRVTWVKSVDEAIAACGDVPEIMVIGGGRVYEQFLPKAQKLYLTHIDAEVEGDTHFPDYEPDDWESVFSEFHDADAQNSHSYCFEILERR"`; acceptor begins `acceptor_aa = "VSKGEEDNMAIIKEFMRFKVHMEGSVNGHEFEIEGEGEGRPYEGTQTAKLKVTKGGPLPFAWDILSPQFMYGSKAYVKHPADIPDYLKLSFPEGFKWERVMNFEDGGVVTVTQDSSLQDGEFIYKVKLRGTNFPSDGPVMQKKTMGWEASSERMYPEDGALKGEIKQRLKLKDGGHYDAEVKTTYKAKKPVQLPGAYNVNIKLDITSHNEDYTIVEQYERAEGRHSTGGMDELYK"`; SNAP begins `snap_aa = "GPGSDKDCEMKRTTLDSPLGKLELSGCEQGLHEIIFLGKGTSAADAVEVPAPAAVLGGPEPLMQATAWLNAYFHQPEAIEEFPVPALHHPVFQQESFTRQVLWKLLKVVKFGEVISYSHLAALAGNPAATAAVKTALSGNPVPILIPCHRVVQGDLDVGGYEGGLAVKEWLLAHEGHRLGKR"`.
- Linker requirements: line 54 `        assert re.fullmatch(r"[GS]+", linker), (`; length bound line 57: `        assert 5 <= len(linker) <= 20, (`.
- GC-content window: initialization lines 65–67 computes first 50-base window and requires `15 <= gc <= 35`; rolling window loop lines 69–73 applies same bound to each subsequent 50-nucleotide window. Exact assertion at 71: `        assert 15 <= gc <= 35, (`; diagnostic at 72: `            "GC content must be between 30 and 70% in all 50 nucleotide windows."`.
- Runner/reward writes in captured `test.sh`: pytest invocation line 23 `  pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA`; reward success line 27 `  echo 1 > /logs/verifier/reward.txt`; failure line 29 `  echo 0 > /logs/verifier/reward.txt`.

## Verification boundary
No tests, builds, lint, or formatters were run. No tools installed. Captured evidence is limited to the two requested evaluator files and their SHA256 manifest.

VERDICT: tb2-eval-captured (4478 bytes, 103 lines)
