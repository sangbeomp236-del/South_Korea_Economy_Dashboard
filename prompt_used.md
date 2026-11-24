# Prompt used to build the dashboard

Build a Streamlit dashboard for my Kellogg International Finance assignment.

**Country:** South Korea

**Question:** Is Korea's macro-financial and FX environment becoming more favorable for a USD-based private equity investor?

I plan to work in private equity and may evaluate cross-border investments, so I want the dashboard to focus on the currency, financing, and financial-cycle risks that can affect entry valuation, leverage, and exit proceeds.

Use reliable primary/international-organization data and avoid social media or informal secondary sources. Use the OECD for real GDP growth and the Bank for International Settlements (BIS) for FX and financial conditions. Both provide official, regularly updated programmatic data access.

Use these indicators:

1. Quarterly Korea real GDP growth (quarter-on-quarter, seasonally and calendar adjusted) from the OECD.
2. Monthly USD/KRW exchange rate, end of period, quoted as KRW per USD.
3. Monthly Korea broad real effective exchange rate (REER), index 2020=100.
4. Monthly Korea minus U.S. policy-rate spread, calculated in percentage points.
5. Quarterly Korea private non-financial credit-to-GDP gap.
6. Quarterly Korea private non-financial debt service ratio.
7. Quarterly Korea real residential property price growth, year over year.

For every chart:
- show units;
- show frequency;
- show source;
- show the latest observation date;
- state the exchange-rate quotation convention or any transformation;
- use a sample beginning around 2010 by default, with enough history to interpret recent developments.

For the REER, clearly state that a higher index means real appreciation. A historical median may be shown as a simple benchmark, but do not label it as fair value.

Add a short “PE lens” under each chart explaining how I would use the indicator in a cross-border PE screen. Avoid creating a black-box investment score.

**Automation and auditability**
- Retrieve the data programmatically from the OECD SDMX API and BIS API.
- Create a separate Python refresh script.
- Add a GitHub Actions workflow that refreshes the data daily and commits the latest snapshots and a refresh log.
- Display the timestamp of the last successful refresh separately from each series’ latest observation date.
- Include a manual “Refresh data now” button in Streamlit.
- Show an audit/refresh log.

**Verification**
- Create a verification table listing every raw series, source/series key, latest API observation/value, unit, and direct official source URL.
- Make it downloadable as CSV.
- Provide instructions for manually checking at least one observation per raw series against the official OECD/BIS source page.
- For the derived Korea–U.S. policy-rate spread, verify both component policy-rate series.

Also create:
- `requirements.txt`;
- `README.md` with local run, Streamlit deployment, GitHub Actions scheduling, and submission-evidence steps;
- a verification checklist/template;
- a copy of this prompt.

Keep the design clean, professional, and easy to screenshot for the assignment.
