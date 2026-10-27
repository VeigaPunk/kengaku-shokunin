import importlib.util, pathlib, shutil
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
CLONE = pathlib.Path("/fast/scratch/hyaku/kengaku-r45/R45PkgEntry/lane")
WORK = pathlib.Path("/fast/scratch/hyaku/kengaku-r45/R45PkgEntry/v11b")
ENTRY = LANE / ".ufo/waves/round-45/w1/R45PkgEntry/tb2-password-recovery-grader.md"
shutil.copy(ENTRY, CLONE / "corpus/knowledge" / ENTRY.name)
spec = importlib.util.spec_from_file_location("c2", LANE / "plans/round45_c2_verify.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print("V11", m.v11(CLONE, WORK))
