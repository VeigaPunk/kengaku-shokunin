import os, runpy, sys
log = open(os.environ["AUDIT_LOG"], "w", buffering=1)
def hook(event, args):
    if event in ("open", "os.mkdir", "os.rename", "os.remove", "os.rmdir", "os.symlink", "os.listdir", "os.scandir", "subprocess.Popen", "os.putenv", "os.chdir"):
        log.write(event + " " + repr(args)[:300] + "\n")
sys.addaudithook(hook)
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0], run_name="__main__")
