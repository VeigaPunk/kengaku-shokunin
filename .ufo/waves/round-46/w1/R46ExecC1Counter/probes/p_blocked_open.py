import os, pathlib, sys, time
def breach(d, argv, tool):
    fifo = pathlib.Path(d).parent / "blocked.fifo"
    if fifo.exists() and not os.fork():
        try:
            open(fifo, "rb").read()                  # blocks forever: the open never returns
        finally:
            os._exit(0)
    time.sleep(0.3)
    return None
