# R44BatU6b receipts (seat R44BatU6b, kengaku round 44, build+attack v2 wave)

Module: `.ufo/waves/round-44/wave/R44BatU6b/battery/u6_long_b.py`
sha256 `52f50a2fecd053eb15346964702900859b4e474b06dfcf5fe5207f6b496d773a` (128 lines)

Clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r44/R44BatU6b/lane`
`git -C "$S/lane" rev-parse --show-toplevel` -> `/fast/scratch/hyaku/kengaku-r44/R44BatU6b/lane`
tip: `5e3d3aa round-44: v2 wave spec + validated dispatch (68 seats)`

## 1. U6 only, dev battery dir (three fixtures)

    $ envelope.sh "$S/env" python3 .../round44_c1_verify.py --lane "$S/lane" --battery-dir .../R44BatU6b/battery --only U6 --work "$S/w"

    ENVELOPE start 20:33:04 cwd=/home/vgpnk/Projects/shokunin
    PINS total=2 mismatched=0
    FIXTURE u6_long_b-registry-80hex tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
    FIXTURE u6_long_b-provenance-129hex tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
    FIXTURE u6_long_b-index-pair-96hex tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
    MUTANT U6 anchor silence killed by=u6_long_b-registry-80hex attributed=L522 value=differs hits=3 -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
    BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
    MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
    MUTANTS-BY-TOOL anchor=1/1 order=0/0
    ADVERTISED direct=1 indirect=0 none=0
    PINS-AFTER mismatched=0
    PREDICATE C1 n/a (non-default battery or mutant subset)
    ENVELOPE end 20:33:06 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged

## 2. Load-bearing, drop one (each variant keeps two fixtures)

    === VARIANT drop_registry ===
    FIXTURE u6_long_b-provenance-129hex ... ok
    FIXTURE u6_long_b-index-pair-96hex ... ok
    MUTANT U6 anchor silence killed by=u6_long_b-provenance-129hex attributed=L522 value=differs hits=2
    BATTERY fixtures=2 wrong=0 tampered=0 sidechannel=0
    MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
    ENVELOPE end 20:33:20 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged

    === VARIANT drop_provenance ===
    FIXTURE u6_long_b-registry-80hex ... ok
    FIXTURE u6_long_b-index-pair-96hex ... ok
    MUTANT U6 anchor silence killed by=u6_long_b-registry-80hex attributed=L522 value=differs hits=2
    BATTERY fixtures=2 wrong=0 tampered=0 sidechannel=0
    MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
    ENVELOPE end 20:33:23 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged

    === VARIANT drop_index ===
    FIXTURE u6_long_b-registry-80hex ... ok
    FIXTURE u6_long_b-provenance-129hex ... ok
    MUTANT U6 anchor silence killed by=u6_long_b-registry-80hex attributed=L522 value=differs hits=2
    BATTERY fixtures=2 wrong=0 tampered=0 sidechannel=0
    MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
    ENVELOPE end 20:33:26 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged

## 3. Load-bearing, keep one (each fixture alone)

    === VARIANT only_registry ===
    FIXTURE u6_long_b-registry-80hex tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
    MUTANT U6 anchor silence killed by=u6_long_b-registry-80hex attributed=L522 value=differs hits=1
    BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0
    MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
    ENVELOPE end 20:33:47 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged

    === VARIANT only_provenance ===
    FIXTURE u6_long_b-provenance-129hex tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
    MUTANT U6 anchor silence killed by=u6_long_b-provenance-129hex attributed=L522 value=differs hits=1
    BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0
    MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
    ENVELOPE end 20:33:50 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged

    === VARIANT only_index ===
    FIXTURE u6_long_b-index-pair-96hex tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
    MUTANT U6 anchor silence killed by=u6_long_b-index-pair-96hex attributed=L522 value=differs hits=1
    BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0
    MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
    ENVELOPE end 20:33:54 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged

## 4. Full default counter, module copied into the clone's plans/battery44/

    $ cp .../u6_long_b.py "$S/lane/plans/battery44/"   (sha256 equal to the wave-dir module)
    $ envelope.sh "$S/env" python3 .../round44_c1_verify.py --lane "$S/lane" --work "$S/w2"

    ENVELOPE start 20:33:59 cwd=/home/vgpnk/Projects/shokunin
    PINS total=2 mismatched=0
    FIXTURE u6_long_b-registry-80hex tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
    FIXTURE u6_long_b-provenance-129hex tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
    FIXTURE u6_long_b-index-pair-96hex tool=anchor expect=reject declared=digest-long observed_rc=1 observed=digest-long ok
    MUTANT U5 anchor silence SURVIVED exhibits=none -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
    MUTANT U6 anchor silence killed by=u6_long_b-registry-80hex attributed=L522 value=differs hits=3 -- plans/anchor_digest_check.py:88 'any other anchor token must be exactly 64 lowercase hex d
    MUTANT U7 anchor rc-mirror SURVIVED exhibits=none -- plans/anchor_digest_check.py:98-99 'A token that resolves to several of the row's captures
    MUTANT U9 anchor rc-mirror SURVIVED exhibits=none -- plans/anchor_digest_check.py:106-107 'lessons are read from the working tree for paths com
    MUTANT U14c order error SURVIVED exhibits=none -- plans/order_check.py:26-27 'Exit: 0 order holds · 1 order broken · 2 setup error (... unpa
    BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
    MUTANTS total=5 killed=1 survived=4 invalid=0 null_detected=0 unattributed=0
    MUTANTS-BY-TOOL anchor=1/4 order=0/1
    ADVERTISED direct=5 indirect=0 none=0
    PINS-AFTER mismatched=0
    PREDICATE C1 fail
    ENVELOPE end 20:34:01 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged

Mutant line (leg f site), `plans/anchor_digest_check.py:520-523`:

    520            if not HEX64.fullmatch(tok):
    521                if len(tok) != 64:
    522                    cls, why = ("digest-short" if len(tok) < 64 else "digest-long"), f"{len(tok)}-hex"
    523                else:
