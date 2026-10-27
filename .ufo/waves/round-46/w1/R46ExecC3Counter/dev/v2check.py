import importlib.util, pathlib
S = pathlib.Path("/fast/scratch/hyaku/kengaku-r46/R46ExecC3Counter"); L = S / "lane"
spec = importlib.util.spec_from_file_location("c3", str(L / "plans/dev_pinned_c3_verify.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
work = S / "work-v2b"; work.mkdir(parents=True, exist_ok=True)
print("V2:", m.v2(L, m.real_pkg(L), work))
