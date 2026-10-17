
## Results
<!-- RESULTS:START -->
### Summary

| Prompt | Model | Runs | Clean JSON | Field accuracy | Hallucinations | Cost / 1k invoices |
|---|---|---|---|---|---|---|
| v1_zero_shot | claude-haiku-5-5 | 3 | 0.0% ± 0.0% | 63.3% ± 1.9% | 2.3 ± 1.5 | $0.00 |
| v2_rules | claude-haiku-5-5 | 3 | 85.6% ± 6.7% | 98.7% ± 0.2% | 0.3 ± 0.5 | $0.00 |

### Accuracy per field

| Field | v1_zero_shot | v2_rules |
|---|---|---|
| `document_type` | 50% | 100% |
| `supplier` | 99% | 100% |
| `ico` | 92% | 99% |
| `amount_due` | 0% | 100% |
| `vat` | 6% | 96% |
| `currency` | 97% | 97% |
| `due_date` | 100% | 100% |

### Errors


**v1_zero_shot / claude-haiku-5-5** (latest run)

- `INV-01.pdf` · `document_type` · wrong: expected `invoice`, got `Faktura – daňový doklad`
- `INV-01.pdf` · `amount_due` · missed: expected `244807.0`, got `None`
- `INV-01.pdf` · `vat` · wrong: expected `42487.2`, got `CZ76234550`
- `INV-02.pdf` · `document_type` · wrong: expected `invoice`, got `Faktura – daňový doklad`
- `INV-02.pdf` · `amount_due` · missed: expected `56518.0`, got `None`
- `INV-02.pdf` · `vat` · wrong: expected `7864.38`, got `CZ39720616`
- `INV-03.png` · `document_type` · wrong: expected `invoice`, got `Faktura - daňový doklad`
- `INV-03.png` · `amount_due` · missed: expected `167397.0`, got `None`
- `INV-03.png` · `vat` · wrong: expected `29052.45`, got `CZ67965776`
- `INV-04.pdf` · `amount_due` · missed: expected `27957.0`, got `None`
- `INV-04.pdf` · `vat` · wrong: expected `4716.71`, got `CZ47378476`
- `INV-05.pdf` · `document_type` · wrong: expected `invoice`, got `Faktura – daňový doklad`
- `INV-05.pdf` · `amount_due` · missed: expected `19467.0`, got `None`
- `INV-05.pdf` · `vat` · wrong: expected `2367.0`, got `CZ64572951`
- `INV-06.jpg` · `document_type` · wrong: expected `invoice`, got `Faktura - daňový doklad`
- `INV-06.jpg` · `amount_due` · missed: expected `202172.0`, got `None`
- `INV-06.jpg` · `vat` · wrong: expected `34177.35`, got `CZ90555236`
- `INV-07.pdf` · `amount_due` · missed: expected `26789.4`, got `None`
- `INV-07.pdf` · `vat` · wrong: expected `4649.4`, got `CZ96542004`
- `INV-08.pdf` · `document_type` · wrong: expected `invoice`, got `Faktura – daňový doklad`
- `INV-08.pdf` · `amount_due` · missed: expected `509454.09`, got `None`
- `INV-08.pdf` · `vat` · wrong: expected `82411.13`, got `CZ80236057`
- `INV-09.jpg` · `document_type` · wrong: expected `invoice`, got `Faktura - daňový doklad`
- `INV-09.jpg` · `amount_due` · missed: expected `22197.3`, got `None`
- `INV-09.jpg` · `vat` · wrong: expected `3147.3`, got `CZ57033749`
- `INV-10.pdf` · `amount_due` · missed: expected `212420.0`, got `None`
- `INV-10.pdf` · `vat` · missed: expected `0.0`, got `None`
- `INV-11.pdf` · `document_type` · wrong: expected `invoice`, got `Faktura – daňový doklad`
- `INV-11.pdf` · `amount_due` · missed: expected `30795.0`, got `None`
- `INV-11.pdf` · `vat` · wrong: expected `5344.5`, got `CZ65421433`
- `INV-12.pdf` · `document_type` · wrong: expected `invoice`, got `Faktura - daňový doklad`
- `INV-12.pdf` · `amount_due` · missed: expected `74280.0`, got `None`
- `INV-12.pdf` · `vat` · wrong: expected `12985.35`, got `CZ46104089`
- `INV-13.pdf` · `amount_due` · missed: expected `1223.74`, got `None`
- `INV-13.pdf` · `vat` · wrong: expected `0.0`, got `SK6447308954`
- `INV-14.pdf` · `amount_due` · missed: expected `1684.95`, got `None`
- `INV-14.pdf` · `vat` · wrong: expected `299.46`, got `SK1080626253`
- `INV-15.png` · `amount_due` · missed: expected `1559.9`, got `None`
- `INV-15.png` · `vat` · wrong: expected `0.0`, got `SK5582759292`
- `INV-16.pdf` · `amount_due` · missed: expected `1992.28`, got `None`
- `INV-17.pdf` · `amount_due` · missed: expected `986.11`, got `None`
- `INV-17.pdf` · `vat` · wrong: expected `102.77`, got `DE596471012`
- `INV-18.pdf` · `amount_due` · missed: expected `22528.6`, got `None`
- `INV-18.pdf` · `vat` · wrong: expected `0.0`, got `DE914144116`
- `INV-19.jpg` · `amount_due` · missed: expected `7114.89`, got `None`
- `INV-19.jpg` · `vat` · wrong: expected `914.36`, got `DE922401556`
- `INV-20.pdf` · `amount_due` · missed: expected `907.85`, got `None`
- `INV-20.pdf` · `vat` · wrong: expected `0.0`, got `ATU78236606`
- `INV-21.jpg` · `amount_due` · missed: expected `2422.17`, got `None`
- `INV-21.jpg` · `vat` · wrong: expected `395.96`, got `ATU13458275`
- `INV-21.jpg` · `currency` · wrong: expected `EUR`, got `CZK`
- `INV-22.pdf` · `amount_due` · missed: expected `3105.46`, got `None`
- `INV-22.pdf` · `vat` · wrong: expected `0.0`, got `PL4016101527`
- `INV-23.pdf` · `document_type` · wrong: expected `invoice`, got `Faktura VAT`
- `INV-23.pdf` · `amount_due` · missed: expected `14481.39`, got `None`
- `INV-23.pdf` · `vat` · wrong: expected `2833.53`, got `PL2538647141`
- `INV-24.pdf` · `amount_due` · missed: expected `2070.76`, got `None`
- `INV-24.pdf` · `vat` · wrong: expected `0.0`, got `{'amount': 0.0, 'currency': 'GBP', 'supplier_vat_no': 'GB589893924', 'customer_vat_no': 'CZ52081559', 'note': 'Outside the scope of UK VAT; customer accounts for VAT (reverse charge)'}`
- `INV-25.pdf` · `ico` · hallucinated: expected `None`, got `20981173`
- `INV-25.pdf` · `amount_due` · missed: expected `28823.2`, got `None`
- `INV-25.pdf` · `vat` · wrong: expected `4803.87`, got `GB916830891`
- `INV-26.pdf` · `amount_due` · missed: expected `12043.53`, got `None`
- `INV-26.pdf` · `vat` · wrong: expected `0.0`, got `CZ92786898`
- `INV-27.jpg` · `amount_due` · missed: expected `6078.06`, got `None`
- `INV-27.jpg` · `vat` · missed: expected `495.46`, got `None`
- `INV-28.pdf` · `amount_due` · missed: expected `773.69`, got `None`
- `INV-28.pdf` · `vat` · wrong: expected `0.0`, got `HU12071855`
- `INV-29.png` · `amount_due` · missed: expected `988.05`, got `None`
- `INV-29.png` · `vat` · wrong: expected `0.0`, got `IT64747636427`
- `INV-30.pdf` · `document_type` · wrong: expected `invoice`, got `Faktura – daňový doklad`
- `INV-30.pdf` · `amount_due` · missed: expected `116473.0`, got `None`
- `INV-30.pdf` · `vat` · wrong: expected `20214.26`, got `CZ64572951`

**v2_rules / claude-haiku-5-5** (latest run)

- `INV-10.pdf` · `vat` · missed: expected `0.0`, got `None`
- `INV-21.jpg` · `currency` · wrong: expected `EUR`, got `CZK`
<!-- RESULTS:END -->
