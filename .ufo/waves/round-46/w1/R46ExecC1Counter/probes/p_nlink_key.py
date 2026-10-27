import os, pathlib
def breach(d, argv, tool):
    st = os.stat(pathlib.Path(d).parent)
    return "nlink-key" if st.st_nlink < 20 else None
