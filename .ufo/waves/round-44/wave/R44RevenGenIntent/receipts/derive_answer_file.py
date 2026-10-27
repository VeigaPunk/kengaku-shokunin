#!/usr/bin/env python3
"""Recompute the 100 grader constants from the four key strings published in
environment/task-deps/gen.py:12 of terminal-bench-2 feal-linear-cryptanalysis.
No FEAL, no decryption, no ciphertext: pure sha256(seed_hash || counter_be64),
counters 32..131, first 8 bytes big-endian (gen.py:18-28 and :57-62)."""
import hashlib, struct, sys
KEYS = ["0x68e63", "0x62571", "0x1f61c", "0xb74a5"]
seed = hashlib.sha256("".join(KEYS).encode()).digest()
derived = [int.from_bytes(hashlib.sha256(seed + struct.pack(">Q", i)).digest()[:8], "big")
           for i in range(32, 132)]
test = sys.argv[1]
body = open(test).read().split('soln = """')[1].split('"""')[0]
consts = [int(x) for x in body.split()]
print("constants_in_test_file =", len(consts))
print("derived_from_published_keys =", len(derived))
print("identical_order_and_values =", consts == derived)
