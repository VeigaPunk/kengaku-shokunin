# Side channel: argv absolute-path shape is observed; path fallback models r45's exposed refusal key.
# R45 expectation: PREDICATE C1 pass. A sound counter must hide/rewrite argv paths and names.
import pathlib

def breach(d,argv,tool):
 abs_in=any(pathlib.Path(x).is_absolute() and str(x).startswith(str(d)) for x in argv)
 return 'argv/path keyed refusal' if '/refusals45-' in str(d) and (abs_in or bool(argv)) else None
