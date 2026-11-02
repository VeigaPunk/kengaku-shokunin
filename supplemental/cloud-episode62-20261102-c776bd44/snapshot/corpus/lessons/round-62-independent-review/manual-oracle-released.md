# Manual oracle — sealed until answer freeze
Derived by reviewer by hand, not running former generated oracle or authored implementation.
1. Six pairs: five contain ≥1 pass, one contains 2 passes. A=5/6; R=1/6 measured. Plug-in A=3/4 and R=1/4 are wrong finite-panel targets.
2. Four singleton slots, two pass: A=R=1/2 measured.
3. Sole triple all pass: A=R=1/1 measured.
4. Sole triple all fail: A=R=0/1 measured.
5. Sole quintuple mixed: A=1/1,R=0/1 measured.
6. PF sole pair A=1,R=0. PPPFF ten pairs, nine have pass, three both pass: A=9/10,R=3/10. Equal-task macro A=19/20,R=3/20 measured. Pooling four passes among seven gives A=6/7,R=2/7, a different target.
7. Six pairs, observed success count1 through3. A lower3/6=1/2 upper1; R lower0 upper3/6=1/2. bounded. All failures/all successes assignments of E,M attain endpoints.
8. Three pairs, at least one known pass in each: A=[1,1]; R=[1/3,1]; status bounded, not measured.
9. P is ineligible k2, metrics null; PPF three pairs A=1,R=1/3 measured; suite could-not-evaluate and macro null, not dropping P.
10. PEF three pairs c1→2 gives A=[2/3,1],R=[0,1/3]. MPPFF ten pairs c2→3 gives A=[7/10,9/10],R=[1/10,3/10]. Macro A=[41/60,19/20],R=[1/20,19/60], bounded.
Sharpness: coordinatewise monotonicity and free binary completion give simultaneous all-negative/all-positive attainable endpoints, not confidence coverage or independence assumptions. Complete panels support descriptive finite-uniform-subset proportions under dependence too. Future IID equal-success-probability sampling interpretation is extra design/semantic assumption.
