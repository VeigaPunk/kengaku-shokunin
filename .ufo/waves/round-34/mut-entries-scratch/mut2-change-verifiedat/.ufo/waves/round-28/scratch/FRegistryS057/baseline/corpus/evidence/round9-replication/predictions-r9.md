# Round 9 preregistered predictions

Scope: 8 fresh problems, pids 101–108, seeds `2000 + pid*29`, endpoint/model/settings copied from round 8. Point predictions (not probabilities):

| Cell | Predicted final passes | Direction / falsifier |
|---|---:|---|
| A-INC | 6/8 | INC > CKPT4710 > CKPT710 > MONO; if A-INC is not higher than both checkpoint cells, the scaffold-assist claim is dead. |
| A-CKPT4710 | 2/8 | Intermediate ladder cell; if it is no better than A-MONO, the scaffold-assist claim is dead. |
| A-CKPT710 | 1/8 | Sparser checkpoint dose should be no better than CKPT4710; if it exceeds CKPT4710, the scaffold-dose claim is dead. |
| A-MONO | 0/8 | Baseline expected lowest; if A-MONO reaches or exceeds A-INC, the scaffold-assist claim is dead. |

Predicted INC mean onset turn: 5.0 (first incorrect graded state, conditional on an error; onset is undefined for perfect trajectories). These are point-count predictions, so scoring will use `|predicted-observed|/8`, explicitly not a probabilistic Brier score.
