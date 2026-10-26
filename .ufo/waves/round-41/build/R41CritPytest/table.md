| case | receipt tests S,C,E | pytest tests S,C,E | receipt obs | pytest obs | match | regrade | pytest rc |
|---|---|---|---|---|---|---|---|
| `nop` | `FFF` | `FFF` | fail | fail | yes | same | 1 |
| `oracle-solve-sh` | `PPP` | `PPP` | pass | pass | yes | same | 0 |
| `literal-correct-slot` | `PPP` | `PPP` | pass | pass | yes | same | 0 |
| `later-valid-wed-1105` | `PFF` | `PFF` | fail | fail | yes | same | 1 |
| `later-valid-thu-1100` | `PPF` | `PPF` | fail | fail | yes | same | 1 |
| `conflict-mon-1230` | `PFF` | `PFF` | fail | fail | yes | same | 1 |
| `bob-start-0900-wed` | `PFP` | `PFP` | fail | fail | yes | same | 1 |
| `decoy-first-vevent` | `PPP` | `PPP` | pass | pass | yes | same | 0 |
| `duration-90min` | `FPP` | `FPP` | fail | fail | yes | same | 1 |
| `missing-carol` | `FPP` | `FPP` | fail | fail | yes | same | 1 |
| `title-wrong` | `FPP` | `FPP` | fail | fail | yes | same | 1 |
| `seconds-30` | `PFF` | `PFF` | fail | fail | yes | same | 1 |
| `tzid-form` | `FFF` | `FFF` | fail | fail | yes | same | 1 |
| `weekend-sat-20` | `FFF` | `FFF` | fail | fail | yes | same | 1 |
| `input-appended` | `FPP` | `FPP` | fail | fail | yes | same | 1 |
| `input-event-deleted-wed-1000` | `FPP` | `FPP` | fail | fail | yes | same | 1 |
| `wed-1059-overlaps-alice` | `PFP` | `PFP` | fail | fail | yes | same | 1 |
| `crlf-line-endings` | `PPP` | `PPP` | pass | pass | yes | same | 0 |
| `folded-attendee-line` | `FPP` | `FPP` | fail | fail | yes | same | 1 |
| `dtstart-value-datetime` | `FFF` | `FFF` | fail | fail | yes | same | 1 |
| `no-prodid-header` | `FPP` | `FPP` | fail | fail | yes | same | 1 |
| `decoy-second-vevent` | `PFF` | `PFF` | fail | fail | yes | same | 1 |
| `extra-attendee-dave` | `PPP` | `PPP` | pass | pass | yes | same | 0 |
| `lowercase-property-names` | `FPP` | `FPP` | fail | fail | yes | same | 1 |
| `input-crlf-rewrite` | `PPP` | `PPP` | pass | pass | yes | same | 0 |

cases=25 per-test-agreements=75/75
