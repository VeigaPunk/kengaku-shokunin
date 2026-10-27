# R46ExecC2States — state tables

grader sha256 `2dc14fc180734b6fbb0ee00f27c4f866071247b57a2217f579465ff8ed3bfc9e`; answer len 23; states_json sha256 `4ff7e19d6939a6cade7be2e2f4dc7ce50c618d047fd827c7cbec3ad9c805be54`

## A. 16 frozen STATE_SHAPES (round46_c2_verify.py, C/D substituted as leg B does; newline='' write)

| state | grader | exists | match | P1 CRLF-only | P2 universal | P3 splitlines | P4 strip-per-line |
|---|---|---|---|---|---|---|---|
| `F00_'C\rD'` | True | True | True | False | True | True | True |
| `F01_'D\rC'` | True | True | True | False | True | True | True |
| `F02_'D\n\rC'` | True | True | True | False | True | True | True |
| `F03_'C\r'` | True | True | True | True | True | True | True |
| `F04_'\rC'` | True | True | True | True | True | True | True |
| `F05_'C\r\r\nD'` | True | True | True | False | True | True | True |
| `F06_'D\r\rC'` | True | True | True | False | True | True | True |
| `F07_'D\r\nC\rD'` | True | True | True | False | True | True | True |
| `F08_'C\r\n'` | True | True | True | True | True | True | True |
| `F09_'D\r\nC\r\n'` | True | True | True | True | True | True | True |
| `F10_'D\rD'` | False | True | False | False | False | False | False |
| `F11_'Cx\rD'` | False | True | False | False | False | False | False |
| `F12_'C\x0bD'` | False | True | False | False | False | True | True |
| `F13_'C\x0cD'` | False | True | False | False | False | True | True |
| `F14_'C\x85D'` | False | True | False | False | False | True | True |
| `F15_'C\u2028D'` | False | True | False | False | False | True | True |

## B. 30 states chosen by this seat

| state | grader | exists | match | P1 CRLF-only | P2 universal | P3 splitlines | P4 strip-per-line |
|---|---|---|---|---|---|---|---|
| `X01_CRLF_blank` | True | True | True | True | True | True | True |
| `X02_CRCR_after` | True | True | True | True | True | True | True |
| `X03_CRLF_then_CR` | True | True | True | True | True | True | True |
| `X04_CR_before` | True | True | True | True | True | True | True |
| `X05_LF_then_CR` | True | True | True | True | True | True | True |
| `X06_CRCRCR_decoy` | True | True | True | False | True | True | True |
| `X07_mixed_inside` | True | True | True | False | True | True | True |
| `X08_LF_CRLF_before` | True | True | True | True | True | True | True |
| `X09_ANS_CR_decoy` | True | True | True | False | True | True | True |
| `X10_CR_no_answer` | False | True | False | False | False | False | False |
| `X11_FS_interior` | False | True | False | False | False | True | True |
| `X12_GS_interior` | False | True | False | False | False | True | True |
| `X13_RS_interior` | False | True | False | False | False | True | True |
| `X14_US_interior` | False | True | False | False | False | False | False |
| `X15_FS_leading` | True | True | True | True | True | True | True |
| `X16_US_trailing` | True | True | True | True | True | True | True |
| `X17_PS_interior` | False | True | False | False | False | True | True |
| `X18_LS_trailing` | True | True | True | True | True | True | True |
| `X19_LS_end_second` | True | True | True | True | True | True | True |
| `X20_LS_leading` | True | True | True | True | True | True | True |
| `X21_NEL_leading` | True | True | True | True | True | True | True |
| `X22_NEL_trailing` | True | True | True | True | True | True | True |
| `X23_VT_trailing` | True | True | True | True | True | True | True |
| `X24_FF_trailing` | True | True | True | True | True | True | True |
| `X25_BOM_before_ANS` | False | True | False | False | False | False | False |
| `X26_BOM_own_line` | True | True | True | True | True | True | True |
| `X27_BOM_on_ANS_line` | False | True | False | False | False | False | False |
| `X28_NUL_after_ANS` | False | True | False | False | False | False | False |
| `X29_NUL_before_ANS` | False | True | False | False | False | False | False |
| `X30_NUL_other_line` | True | True | True | True | True | True | True |

## C. byte payloads (not valid UTF-8)

| payload | sha256[:16] | exists | match | P6 decode-guard |
|---|---|---|---|---|
| `Y01_utf16le_bom` | aa90ae645e79a3bd | True | False | False |
| `Y02_invalid_ff_after` | 4fbf950a8e8ed8cd | True | False | False |
| `Y03_bom_utf8_answer` | 2d4ffa779de30310 | True | False | False |
| `Y04_utf16le_no_bom` | a6d7b3a9674857ba | True | False | False |

## D. supplementary 8 Z states (padded/joined/empty)

| state | grader | P1 | P2 | P3 | P4 |
|---|---|---|---|---|---|
| `Z01_padded_answer` | True | True | True | True | True |
| `Z02_tab_answer` | True | True | True | True | True |
| `Z03_trailing_space` | True | True | True | True | True |
| `Z04_padded_decoy` | True | True | True | True | True |
| `Z05_password_eq` | False | False | False | False | False |
| `Z06_joined` | False | False | False | False | False |
| `Z07_empty` | False | False | False | False | False |
| `Z08_crlf_only` | False | False | False | False | False |

## E. interior-padding 6 Z states

| state | text | grader | P1 | P2 | P3 | P4 |
|---|---|---|---|---|---|---|
| `Z09_ANS_pad_then_D` | `'8XDP5Q2RT9ZK7VB3BV4WW54  \n\tQQQQ1111RRRR2222SSSS333\t\n'` | False | False | False | False | True |
| `Z10_D_then_padded_ANS` | `'QQQQ1111RRRR2222SSSS333\n  8XDP5Q2RT9ZK7VB3BV4WW54  '` | False | False | False | False | True |
| `Z11_ANS_space_mid` | `'QQQQ1111RRRR2222SSSS333\n8XDP5Q2RT9ZK7VB3BV4WW54 \nE'` | False | False | False | False | True |
| `Z12_padded_second` | `'8XDP5Q2RT9ZK7VB3BV4WW54\r\n  QQQQ1111RRRR2222SSSS333  \r\n'` | True | True | True | True | True |
| `Z13_pad_first_crlf` | `'  8XDP5Q2RT9ZK7VB3BV4WW54\r\nQQQQ1111RRRR2222SSSS333'` | True | True | True | True | True |
| `Z14_blank_then_space` | `'\n 8XDP5Q2RT9ZK7VB3BV4WW54\nQQQQ1111RRRR2222SSSS333'` | True | True | True | True | True |

Randomised text for the diverging ids (seed 46):

```
R157 = '\x0c\x1f\x00\t\r8XDP5Q2RT9ZK7VB3BV4WW54'
R049 = '8XDP5Q2RT9ZK7VB3BV4WW54\u2029\x0b8XDP'
R073 = '\u2028QQQQ1111RRRR2222SSSS333\x0c\x1d8XDP5Q2RT9ZK7VB3BV4WW54\u2028'
R129 = '8XDP5Q2RT9ZK7VB3BV4WW54\u20298XDP5Q2RT9ZK7VB3BV4WW54x\x0c\n'
R265 = '\n8XDP5Q2RT9ZK7VB3BV4WW54\x1d\x1c8XDP'
```

300-state sweep: pass=15 fail=285 disagree={'P1': 1, 'P2': 0, 'P3': 10, 'P4': 10}
ids P1=['R157']
ids P3=['R049', 'R073', 'R084', 'R089', 'R129', 'R138', 'R150', 'R265', 'R269', 'R289']
ids P4=['R049', 'R073', 'R084', 'R089', 'R129', 'R138', 'R150', 'R265', 'R269', 'R289']
