import os, pathlib
def breach(d, argv, tool):
    st = os.stat(pathlib.Path(d).parent)             # directory stat: documented residual channel
    return "nlink=%d" % st.st_nlink
