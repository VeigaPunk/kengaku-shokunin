# Round-93 pre-freeze controls (L1 KengakuR93)

Every receipt here was produced against instruments commit P1
`17cb9337b99344814bc449d62eed771e29e33981` (BASE `28e9f8bf4e8a68b1a34babfa71be9de595b78c4e` for the
two do-nothing runs) BEFORE the claims freeze F, by the commands each file's first line shows. The
C1 forgery ran on a `git clone --shared` of the lane detached at P1 plus one fixture-identity
commit (`fixture <fixture@invalid>`, toplevel verified) that flips the ledger member without any
probe receipt; the clone lived under /fast/scratch/hyaku/kengaku-r93/L1/forge-c1 and is not
evidence itself — the receipt is.

| receipt | revision | expected | observed |
|---|---|---|---|
| c1-base.txt | BASE | rc 1, all legs fail | rc 1, L1-L9 fail, executed_rows=36 |
| c1-forgery-ledger-only.txt | P1 + forged ledger flip | rc 1 | rc 1, L7 pass, L1-L6/L8/L9 fail |
| c1-sandbox-red.txt | P1, --bwrap /nonexistent/bwrap | rc 2 | rc 2, DEFECT SETUP sandbox-unavailable |
| c2-base.txt | BASE | rc 1, tool absent | rc 1, W1-W4 fail |
| c2-forgery-always_intact.txt | P1, --tool-file | rc 1 | rc 1, W1+W2 fail |
| c2-forgery-always_broken.txt | P1, --tool-file | rc 1 | rc 1, W1+W2 fail |
| c2-forgery-bytes_only.txt | P1, --tool-file | rc 1 | rc 1, W2 fail (edit-revert RED) |
| c2-forgery-log_only.txt | P1, --tool-file | rc 1 | rc 1, W2 fail (lying-table RED) |
| c2-real-at-P1.txt | P1 | W1-W3 pass, W4 fail (no claims yet) | as expected, rc 1 |

The dry runs `../dryrun-1.txt` (first case-table draft, all TBD) and `../dryrun-2.txt` (eight
cases; C08 hypothesis 60/3 refuted, observed 56/7) are the pre-freeze prediction runs.
