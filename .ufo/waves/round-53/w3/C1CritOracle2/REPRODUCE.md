# C1CritOracle2 — reproduction (all commands run under /fast/scratch/hyaku/kengaku-r53/C1CritOracle2)

Lane clone base (read-only source of truth):
  git clone -q /home/vgpnk/Projects/shokunin/kengaku-shokunin base
  git -C base rev-parse HEAD      # 9ead4476bf55b1ea6490d0204b668195db4a4d1d

A. Baseline counter on the pristine lane (FREEZE/ORACLE green):
  cd base && python3 plans/round53_c1_triage.py --lane .

B. Angle 1 (spec ambiguity) — recompute the oracle and audit ambiguity shapes:
  python3 load.py        # oracle.json: decided/contested/Y/N/v2/disagree
  python3 amb2.py        # module-level reach, any()/all() over listings
  python3 amb3.py        # negated existence, uncaptured imports, fixtures
  python3 amb4.py        # env-gated tests, vacuity-shaped assertions
  python3 flip.py        # listing-count vs listing-membership assertions
  python3 showsrc.py '<test id>' ...   # dump one test body with its span

C. Angle 2 (shared-spec collusion) — 10 Y + 10 N sampled by me, re-read by hand:
  python3 -c "import json,random; o=json.load(open('oracle.json')); ..."
  # samples-20.json holds the ids; all-52-Y-bodies.txt holds every Y body I read

D. Angle 3 (control direction) — all 23 r52 disagreements enumerated:
  python3 -c "... o['dec'], o['r52'], o['v2'] ..."  # direction split 21 r52=P0/oracle=Y, 2 r52=P1/oracle=N

E. Angle 4 (freeze integrity) — the forgery that LANDS:
  git clone -q --shared base e14 && cd e14
  python3 ../forgery-rewrite5.py       # rebuilds freeze+label commits with a forged classifier and 10 flipped labels
  git checkout -q -B forge refs/heads/forge
  python3 plans/round53_c1_triage.py --lane .
  # => FREEZE clean=yes ... labels_after_freeze_and_untouched=yes
  #    ORACLE ... oracle_Y=42 ... disagree=0 per_label_agree=1.000
  #    CONFIRM new_confirmed=20 rejected=0     <-- four legs green on forged labels

F. Corrections (each verified to keep the pristine lane green AND kill the forgery):
  python3 ../correction-patch.py plans/round53_c1_triage.py   # adds CLASSIFIER_SHA + LABEL_SHA pins
  python3 ../correction-patch.py ... + FREEZE_COMMIT literal  # alternative anchor
