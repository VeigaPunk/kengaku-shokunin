# R48C2MutOrder — C2 probe-order mutation

**Axes:** coverage (assigned); order-gate mutant sensitivity.  
**VERDICT: SURVIVED — coverage finding.** The order gate detects the pre-receipt P10 run on pristine and restored bytes, but the one-line mutant accepts the same committed evidence. Thus this detector does not reject the mutant. No C2 admission or claim verdict is made.

## Freeze and scope

Verified the committed lane tree at stage-1 freeze `a543d92083557dd9b33ee674e9b99b03411f80af`; `git log -1` reports commit time `2026-10-27T06:53:29-03:00`. The committed claims file contains the frozen rule that pre-receipt controls disable P10 and `plans/order_check.py` pins their ordering receipt. This freeze predates this measurement. The committed tree does not contain `plans/round48_c2_verify.py`; therefore no stage-2 counter/control execution was attempted. No full probe, scored probe, or scored counter ran. The bounded detector below is the order gate alone, using a disposable committed-history fixture in the isolated clone.

## Mutant and detector

Mutant: in `plans/order_check.py::blob_hits`, replace the condition that records every `P10` line except `DEFECT receipt unreadable` with `m.group(1) == "DEFECT" and not EXECUTED_EXCUSE.match(detail)`. This drops successful `P10 ok …` lines from the evidence of probe execution.

Detector command (pristine, mutant, restored):

```sh
python3 plans/order_check.py --lane . --claims plans/round-48-claims.md --receipt corpus/evidence/round48/pre-receipt-probe.txt
```

The scratch history included a committed claims artifact containing `gate: P10 ok probe_rerun=byte-equal bytes=6613`, committed before a committed receipt. Fixture git writes were made only after asserting `git -C "$D" rev-parse --show-toplevel` equaled `$D`.

## Commands and observed outputs

Setup/fixture commands run:

```sh
mkdir -p /fast/scratch/hyaku/kengaku-r48/R48C2MutOrder
cd /fast/scratch/hyaku/kengaku-r48/R48C2MutOrder
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
cd lane
git checkout a543d92083557dd9b33ee674e9b99b03411f80af
# asserted git -C "$D" rev-parse --show-toplevel = "$D"
git -C "$D" add .ufo/waves/round-48/claims/pre-receipt-control.txt
git -C "$D" commit -m 'scratch fixture: pre-receipt P10 success line'
git -C "$D" add corpus/evidence/round48/pre-receipt-probe.txt
git -C "$D" commit -m 'scratch fixture: receipt after P10 control'
```

The fixture commits were `60762de70a9d3170fc54e356bc7b9f0e27090dfc` (P10 line) and `160a8456e97dab3e50d049d75d8dfa4d0f089ab9` (receipt). **REV 160a8456e97dab3e50d049d75d8dfa4d0f089ab9** is the tree measured by all three detector runs.

Pristine gate hash: `948d5e1d2b3429d76a598fd11c4b22856d9f43ec093efd2c6aa0025aa0fc6ecc`.
Output (verbatim):

```text
ORDER claims=plans/round-48-claims.md round=48 freeze=a543d92083557dd9b33ee674e9b99b03411f80af
ORDER receipt=corpus/evidence/round48/pre-receipt-probe.txt receipt_commit=160a8456e97dab3e50d049d75d8dfa4d0f089ab9 claims_dir=.ufo/waves/round-48/claims/
ORDER scanned commits=1 file_entries=1 distinct_blobs=1
ORDER HIT .ufo/waves/round-48/claims/pre-receipt-control.txt@60762de70a9d:1 kind=gate-p10 `gate: P10 ok probe_rerun=byte-equal bytes=6613`
ORDER FAIL probe-executed-before-receipt hits=1
ORDER RESULT FAIL
exit=1
```

Mutant hash: `ba11f234348df7d2cfa6fc178da1a284fb9a4686c770959982790fdce88575c1`.
Output (verbatim):

```text
ORDER claims=plans/round-48-claims.md round=48 freeze=a543d92083557dd9b33ee674e9b99b03411f80af
ORDER receipt=corpus/evidence/round48/pre-receipt-probe.txt receipt_commit=160a8456e97dab3e50d049d75d8dfa4d0f089ab9 claims_dir=.ufo/waves/round-48/claims/
ORDER scanned commits=1 file_entries=1 distinct_blobs=1
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS
exit=0
```

Restoration: `git -C "$D" checkout -- plans/order_check.py` after verifying the clone top-level. Restored hash is exactly `948d5e1d2b3429d76a598fd11c4b22856d9f43ec093efd2c6aa0025aa0fc6ecc`. Restored detector output is byte-for-byte the same lines and exit `1` as the pristine output above, including the same `ORDER HIT` and `ORDER RESULT FAIL`.

## Limits and source trace

This demonstrates the gate's ordering behavior on a committed-history fixture, not the unavailable stage-2 C2 counter's full control suite. The claims freeze names `order_check.py` for ordering receipts but the round-46 counter shows no digest pin for that file; no separate frozen control was run that would catch this gate mutation. The surviving mutant is a coverage finding only; no frozen predicate or control was changed.

Sources opened 2026-10-27 (local source URLs; located quotations are ≤25 words):

- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md`, §C2 V8: “`plans/order_check.py` pins each control's ordering receipt”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md`, §Routed defects item 3: “make pre-receipt controls unable to run P10”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/order_check.py`, `blob_hits`: “a gate `P10` line whose detail is anything other than `receipt unreadable`”.
