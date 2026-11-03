| id | check removed (frozen lines) | mutant sha256 | true-receipt rc harness / literal | accepted forgery (survived on) | kept-out (killed by) | verdict |
|---|---|---|---|---|---|---|
| m1 | PROBE binding deleted (L250–254) | `3d1353d32c14` | 0 / 0 | F-probe | — | SURVIVED |
| m2 | BASE-PROBE binding deleted (L256–264) | `f0ffe73707b3` | 0 / 1 | F-base | — | SURVIVED |
| m3 | grader-bytes re-hash deleted (L274–276) | `ed23687a51d2` | 0 / 1 | F-grader-bytes | — | SURVIVED |
| m4 | duplicate-CASE detection deleted (L293–294) | `2749b9a009cd` | 0 / 1 | F-dup | — | SURVIVED |
| m5 | unknown-case detection deleted (L295–297) | `0323f83e7727` | 0 / 1 | F-unknown | — | SURVIVED |
| m6 | K2 clause-bytes check deleted (L353–354) | `dfde9865bfe9` | 0 / 1 | F-k2-clause | — | SURVIVED |
| m7 | per-case stderr binding deleted (L358–368) | `a1770bd47ec2` | 0 / 1 | F-k1-stderr, F-k3-stderr, F-k4-capture | — | SURVIVED |
| m8 | server-log fetch-proof checks deleted (L332–335) | `d7916f1d05f8` | 0 / 1 | F-log-no-simple, F-log-no-wheel | — | SURVIVED |
| m9 | exit-agreement check deleted (L390–391) | `f1c5c9490eb7` | 0 / 1 | F-exit | — | SURVIVED |
| m10 | stored-predicate agreement deleted (L392–393) | `be5348f47ab2` | 0 / 1 | F-stored | — | SURVIVED |
| m11 | per-case observed/expected checks deleted (L306–309) | `373d1f1666b3` | 0 / 1 | F-k1-observed, F-k1-expected, F-vector | — | SURVIVED |
| m12 | GRADER receipt sha+pin checks deleted (L270–273) | `b6f998b8170f` | 0 / 1 | F-grader-sha, F-grader-pin | — | SURVIVED |
| m13 | K1 index_pid check deleted (L315–316) | `86cf9bfb4340` | 0 / 1 | F-k1-pid | — | SURVIVED |
| m14 | K1 wheel-sha check deleted (L318–319) | `4ec91c4460ae` | 0 / 1 | F-k1-wheel | — | SURVIVED |
| m15 | server-log sha binding deleted (L329–330) | `3247156c1c07` | 0 / 1 | F-log-sha | — | SURVIVED |
| m16 | K2 clause line check deleted (L341–342) | `4ef1b80ea600` | 0 / 1 | F-k2-line | — | SURVIVED |
| m17 | K2 connection-refused check deleted (L355–356) | `337aea892ecc` | 0 / 1 | F-k2-refused | — | SURVIVED |
| m18 | CLASS line check deleted (L371–372) | `98659cdb81ed` | 0 / 1 | F-class | — | SURVIVED |
| m19 | PREDICTION-VECTOR line checks deleted (L378–381) | `e4160f314d88` | 0 / 1 | F-pred | — | SURVIVED |
| m20 | per-case leg check deleted (L310–311) | `153642a12bbd` | 0 / 1 | F-k1-leg | — | SURVIVED |
| m21 | case-missing defect deleted (L302–302) | `f4979490b5ef` | 0 / 1 | — | F-missing (still refused: K4-stderr-sha) | KILLED |
| m22 | server-log flags check deleted (L336–337) | `bbb32e269402` | 0 / 1 | F-log-flags | — | SURVIVED |
