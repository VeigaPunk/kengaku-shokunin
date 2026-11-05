import importlib.util, os, sys, pathlib
mod_path = pathlib.Path(os.environ["GATE"])
spec = importlib.util.spec_from_file_location("gate", mod_path)
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
lane_dir, rev, work = pathlib.Path(sys.argv[1]), sys.argv[2], pathlib.Path(sys.argv[3])
work.mkdir(parents=True, exist_ok=True)
try:
    lines, code = G.evaluate(G.Lane(lane_dir), rev, 92, work)
    for l in lines: print(l)
    print("EVAL-RC", code)
except G.CouldNotEvaluate as e:
    print("DEFECT SETUP", e); print("EVAL-RC 2")
