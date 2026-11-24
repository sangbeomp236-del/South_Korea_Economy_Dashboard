# Verification checklist

Use this after the first successful refresh. The assignment requires at least one observation from each series to be checked against the original source.

## Manual data checks

Open the dashboard's **Verification table** and each official source page. Record one matching observation per raw series.

| Raw series | BIS key | Period checked | Dashboard/API value | Official BIS value | Match? | Source |
|---|---|---|---:|---:|---|---|
| Real GDP growth | OECD QNA GDP growth |  |  |  |  | https://data-explorer.oecd.org/vis?df%5Bag%5D=OECD.SDD.NAD&df%5Bid%5D=DSD_NAMAIN1%40DF_QNA_EXPENDITURE_GROWTH_OECD&dq=Q.....B1GQ......G1.&vw=tb |
| USD/KRW exchange rate | M.KR.KRW.E |  |  |  |  | https://data.bis.org/topics/XRU/BIS%2CWS_XRU%2C1.0/M.KR.KRW.E |
| Korea broad REER | M.R.B.KR |  |  |  |  | https://data.bis.org/topics/EER/BIS%2CWS_EER%2C1.0/M.R.B.KR |
| Korea policy rate | M.KR |  |  |  |  | https://data.bis.org/topics/CBPOL/BIS%2CWS_CBPOL%2C1.0/M.KR |
| U.S. policy rate | M.US |  |  |  |  | https://data.bis.org/topics/CBPOL/BIS%2CWS_CBPOL%2C1.0/M.US |
| Korea credit-to-GDP gap | Q.KR.P.A.C |  |  |  |  | https://data.bis.org/topics/CREDIT_GAPS/BIS%2CWS_CREDIT_GAP%2C1.0/Q.KR.P.A.C |
| Korea private non-financial DSR | Q.KR.P |  |  |  |  | https://data.bis.org/topics/DSR/BIS%2CWS_DSR%2C1.0/Q.KR.P |
| Korea real residential property price growth | Q.KR.R.771 |  |  |  |  | https://data.bis.org/topics/RPP/BIS%2CWS_SPP%2C1.0/Q.KR.R.771 |

### Derived indicator check
Korea–U.S. policy-rate spread = Korea policy rate − U.S. policy rate.

Period: __________  
Korea policy rate: __________  
U.S. policy rate: __________  
Calculated spread: __________  
Dashboard spread: __________  
Match? __________

## Successful refresh evidence

Capture two screenshots:

1. **GitHub Actions:** a completed green `Refresh BIS dashboard data` workflow run.
2. **Streamlit dashboard:** the “Last successful refresh” timestamp and the expanded “Refresh evidence / audit trail.”

A successful refresh does not need to change the values if BIS has not released a new observation.

## What to submit

- Screenshot/PDF of the dashboard.
- `prompt_used.md`.
- This completed verification checklist or a short PDF containing the same table.
- Refresh screenshots/log evidence.
