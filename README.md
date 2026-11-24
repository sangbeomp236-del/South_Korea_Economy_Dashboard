# Korea PE Macro-FX Monitor

## Research question
**Is Korea's macro-financial and FX environment becoming more favorable for a USD-based private equity investor?**

The dashboard is designed as a country-level PE screening tool. It does not replace company underwriting.

## Indicators
1. Korea real GDP growth, quarterly q/q, seasonally and calendar adjusted (OECD).
2. USD/KRW, monthly end-of-period, KRW per USD.
3. Korea broad REER, monthly, 2020=100.
4. Korea minus U.S. policy-rate spread, monthly, percentage points.
5. Private non-financial credit-to-GDP gap, quarterly.
6. Private non-financial debt service ratio, quarterly.
7. Real residential property price growth, quarterly YoY.

Real GDP growth comes from the OECD. The FX and financial-condition series come from the Bank for International Settlements (BIS).

## Why these indicators?
- **Real GDP growth:** simple macro backdrop for domestic revenue growth and deal underwriting.
- **USD/KRW:** direct translation risk for USD entry and exit proceeds.
- **REER:** medium/long-run currency valuation and competitiveness context.
- **Policy spread:** relative USD/KRW monetary conditions and local funding environment.
- **Credit gap:** whether credit is running above or below its long-run trend.
- **Debt service ratio:** how much income is absorbed by debt payments.
- **Real house prices:** asset-cycle and collateral-value context.

## Local run
```bash
pip install -r requirements.txt
python refresh_data.py
streamlit run app.py
```

## First refresh
Run:
```bash
python refresh_data.py
```
This creates CSV snapshots under `data/` and `refresh_log.json`.

## Deploy on Streamlit Community Cloud
1. Create a GitHub repository and upload this project.
2. In Streamlit Community Cloud, choose the repository.
3. Set the main file to `app.py`.
4. Deploy.
5. The app requires no secret API key.

## Automatic refresh
`.github/workflows/refresh.yml` runs every day at 12:17 UTC.

It:
1. downloads the newest OECD and BIS observations;
2. rewrites the CSV snapshots;
3. writes `refresh_log.json`;
4. commits changed snapshots back to the repository.

The schedule is intentionally more frequent than the release frequency. The assignment explicitly allows a successful refresh that produces no changed values.

You can also run the workflow manually from:
**GitHub → Actions → Refresh Korea dashboard data → Run workflow**.

## Verification
After the first successful refresh:
1. open the dashboard's Verification table;
2. open each linked official OECD/BIS series page;
3. compare at least one period/value for every raw series;
4. fill in `verification_checklist.md`;
5. verify the policy spread calculation separately from its two component rates.

## Suggested submission evidence
- Dashboard screenshot showing all seven charts.
- Screenshot of “Last successful refresh.”
- Screenshot of a green GitHub Actions refresh run.
- Completed verification table/checklist.
- `prompt_used.md`.

## Exchange-rate convention
USD/KRW is **KRW per USD**.  
An increase means KRW depreciation; a decrease means KRW appreciation.

## Important limitations
- REER is not a stand-alone fair-value estimate. The dashboard's 10-year median is only a historical benchmark.
- Policy-rate spreads do not determine exchange rates by themselves.
- Credit gaps and debt service ratios are financial-cycle indicators, not timing signals.
- Residential property prices do not represent all corporate asset valuations.
- Country-level conditions should be combined with target-company cash flows, leverage, industry structure, and deal-specific FX exposure.

Data attribution: OECD and Bank for International Settlements (BIS).
