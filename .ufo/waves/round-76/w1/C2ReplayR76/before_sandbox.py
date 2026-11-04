import pathlib, runpy, sys
original = pathlib.Path.mkdir
def mkdir(self, *args, **kwargs):
    if str(self) == "/fast/scratch/hyaku/kengaku-r76/c2":
        self = pathlib.Path(sys.argv[1])
    return original(self, *args, **kwargs)
pathlib.Path.mkdir = mkdir
script, scratch = sys.argv[2], sys.argv[1]
sys.argv = [script, "--lane", ".", "--rev", "fda63968"]
runpy.run_path(script, run_name="__main__")
