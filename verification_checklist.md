# Verification checklist

Use this after the first successful refresh. The assignment requires at least one observation from each series to be checked against the original source.

## Manual data checks

Open the dashboard's **Verification table** and each official source page. Record one matching observation per raw series.

| Raw series | Series key | Period checked | Dashboard/API value | Official source value | Match? | Source |
|---|---|---|---:|---:|---|---|
| Real GDP growth | OECD QNA GDP growth | 2026-Q3 | 0.9681 |  |  | https://data-explorer.oecd.org/vis?df%5Bag%5D=OECD.SDD.NAD&df%5Bid%5D=DSD_NAMAIN1%40DF_QNA_EXPENDITURE_GROWTH_OECD&dq=Q.....B1GQ......G1.&vw=tb |
| USD/KRW exchange rate | M.KR.KRW.E | 2026-10 | 1335.2667 |  |  | https://data.bis.org/topics/XRU/BIS%2CWS_XRU%2C1.0/M.KR.KRW.E |
| Korea broad REER | M.R.B.KR | 2026-10 | 95.05 |  |  | https://data.bis.org/topics/EER/BIS%2CWS_EER%2C1.0/M.R.B.KR |
| Korea policy rate | M.KR | 2026-10 | 3.00 |  |  | https://data.bis.org/topics/CBPOL/BIS%2CWS_CBPOL%2C1.0/M.KR |
| U.S. policy rate | M.US | 2026-10 | 3.875 |  |  | https://data.bis.org/topics/CBPOL/BIS%2CWS_CBPOL%2C1.0/M.US |
| Korea credit-to-GDP gap | Q.KR.P.A.C | 2026-Q1 | -15.1257 |  |  | https://data.bis.org/topics/CREDIT_GAPS/BIS%2CWS_CREDIT_GAP%2C1.0/Q.KR.P.A.C |
| Korea private non-financial DSR | Q.KR.P | 2026-Q1 | 19.3 |  |  | https://data.bis.org/topics/DSR/BIS%2CWS_DSR%2C1.0/Q.KR.P |
| Korea real residential property price growth | Q.KR.R.771 | 2026-Q2 | -0.4738 |  |  | https://data.bis.org/topics/RPP/BIS%2CWS_SPP%2C1.0/Q.KR.R.771 |

### Derived indicator check

Korea–U.S. policy-rate spread = Korea policy rate − U.S. policy rate.

Period: 2026-10  
Korea policy rate: 3.00%  
U.S. policy rate: 3.875%  
Calculated spread: -0.875 percentage points  
Dashboard spread: -0.875 percentage points  
Match? Yes

## Successful refresh evidence

The dashboard refresh process was successfully tested using GitHub Actions.

Capture two screenshots:

1. **GitHub Actions:** a completed green `Refresh Korea dashboard data` workflow run.
2. **Streamlit dashboard:** the `Last successful refresh` timestamp and the expanded `Refresh evidence / audit trail`.

A successful refresh does not need to produce different values if the source has not released a new observation.

## Refresh test completed

GitHub Actions workflow: `Refresh Korea dashboard data`  
Status: Successful  
Refresh date: November 24, 2026  
Dashboard last successful refresh: 2026-11-24 16:20:31 UTC

The successful workflow created updated data snapshots and `refresh_log.json` in the GitHub repository.

## What to submit

- Screenshot or PDF of the dashboard.
- `prompt_used.md`.
- This completed verification checklist.
- Screenshot of the successful GitHub Actions refresh.
- Screenshot of the dashboard showing the last successful refresh timestamp and refresh audit trail.
