#!/usr/bin/env python3
"""Run one probe-under-test's check_receipt against one lane + one receipt.

The probe copy's own bytes differ from the frozen instrument, so the PROBE binding
(which binds the receipt to the instrument's bytes) is re-anchored to the frozen
probe's sha256; every other byte of the checker is the mutant's.  Control runs
(C1: record receipt -> rc 0, C2: forged PROBE sha -> rc 1) show the re-anchored
check still refuses a receipt naming a different sha.
"""
import importlib.util
import pathlib
import sys

FROZEN_PROBE_SHA = "4a6fae5328e1cacd3b667fb59f50622d1602574a5763f741bda7dc0293b3fdfc"


def main(argv):
    mod_path, lane, receipt = argv[1], argv[2], argv[3]
    spec = importlib.util.spec_from_file_location("probe_under_test", mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.own_sha256 = lambda: FROZEN_PROBE_SHA
    mod.lane_root = lambda: pathlib.Path(lane)
    mod._BASE = mod.load_base_probe()
    return mod.check_receipt(receipt)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
