import sys, re
sys.dont_write_bytecode = True
sys.path.insert(0, '.')
import c1_counter_copy as C
for f in ["bn-fit-modify","pytorch-model-recovery","torch-tensor-parallelism"]:
    body = open(f"fetch/{f}.test_outputs.py", encoding="utf-8").read()
    print("==", f, "file-level", C.classify(body))
    for name, block in C.split_tests(body):
        cls = C.classify_test(block)
        hits = {k: bool(v.search(C.PRESENCE.sub(" ", block))) for k, v in [("BEHAV_T", C.BEHAV_T), ("VALUE", C.VALUE)]}
        vm = C.VALUE.findall(C.PRESENCE.sub(" ", block))
        bm = C.BEHAV_T.findall(C.PRESENCE.sub(" ", block))
        print(f"  {name:42s} class={cls} presence={bool(C.PRESENCE.search(block))} value_hits={sorted(set(vm))[:6]} behav_hits={sorted(set(bm))[:4]} lines={block.count(chr(10))}")
