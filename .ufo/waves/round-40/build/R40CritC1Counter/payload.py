import time, pathlib, sys
time.sleep(6)
pathlib.Path(sys.argv[1]).write_text("esc4")
