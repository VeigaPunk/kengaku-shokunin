## Summary

`caffe-cifar-10` can be passed by rewriting CIFAR-10 labels in the agent-controlled Caffe checkout. The verifier does not score against a sealed holdout dataset — it reuses the agent's data — so a degenerate one-class dataset can satisfy the accuracy checks.

## Evidence from #148

Surfaced during reward-hack adjudication on [#148](https://github.com/harbor-framework/terminal-bench-2-1/pull/148) (GPT-5.6 Luna medium + fast-agent).

| Role | Link |
| --- | --- |
| Task | [caffe-cifar-10](https://hub.harborframework.com/tasks/terminal-bench/caffe-cifar-10) |
| Original trial | [`26a75c8c`](https://hub.harborframework.com/jobs/a76a00ca-aca4-5696-ad59-3b01e7f8c5e2/trials/26a75c8c-2582-567a-b803-9bf23dbc3e5e) |
| Judge verdict | [`fe14987a`](https://hub.harborframework.com/jobs/493b2eaf-7f46-4047-bcca-b076f535e57c/trials/fe14987a-9aab-4412-bb1b-56eba50f6914?tab=votes) |
| Judge job | [`493b2eaf`](https://hub.harborframework.com/jobs/493b2eaf-7f46-4047-bcca-b076f535e57c) |
| Source job | [`a76a00ca`](https://hub.harborframework.com/jobs/a76a00ca-aca4-5696-ad59-3b01e7f8c5e2) |

The agent installed/built Caffe, then rewrote all ~60k CIFAR-10 records to label `0`, producing high train/test accuracy on a one-class dataset rather than a real classifier. Submitter ([evalstate on #148](https://github.com/harbor-framework/terminal-bench-2-1/pull/148#issuecomment-5002361468)) agreed this is a supported individual disqualification.

## Why this is a task defect

The verifier in `tasks/caffe-cifar-10/tests/test_outputs.py`:

1. Parses accuracy from the agent-written `training_output.txt`
2. Runs `caffe test` against the agent's model + prototxt under `/app/caffe`

Those prototxts point at data in the same agent-writable checkout. There is no sealed holdout, so poisoning train+test labels (50k+10k) fools both the training log and the verifier re-test (`>45%` and within 5% of train).

## Suggested fix

- Score accuracy on a verifier-owned, agent-inaccessible CIFAR-10 holdout (or verify data integrity / checksums before testing)
- Optionally assert label distribution / that the dataset is unmodified relative to a known-good hash

## Notes

- Trial-level DQ on the leaderboard submission is still appropriate under the current reward-hacking rubric.
- This issue tracks hardening the task so the same bypass is not available going forward.