SERIES = {

    "gdp": {
        "label": "Real GDP growth",
        "provider": "OECD",
        "start_period": "2000-Q1",
        "unit": "Quarter-on-quarter %",
        "frequency": "Quarterly, seasonally and calendar adjusted",
        "source": "OECD",
        "source_url": "https://data-explorer.oecd.org/vis?df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_NAMAIN1%40DF_QNA_EXPENDITURE_GROWTH_OECD&df[ag]=OECD.SDD.NAD&df[vs]=1.1&dq=Q..AUS%2BAUT%2BBEL%2BCAN%2BCHE%2BCHL%2BCOL%2BCRI%2BCZE%2BDEU%2BDNK%2BESP%2BFIN%2BEST%2BFRA%2BGBR%2BGRC%2BHUN%2BISL%2BLTU%2BIRL%2BISR%2BITA%2BJPN%2BKOR%2BLUX%2BLVA%2BMEX%2BNLD%2BNOR%2BNZL%2BPOL%2BPRT%2BSVK%2BSVN%2BSWE%2BTUR%2BUSA%2BOECD%2BG20%2BG7%2BUSMCA%2BOECDE%2BEA%2BEU..........&lom=LASTNPERIODS&lo=5&to[TIME_PERIOD]=false",
        "transformation": "OECD real GDP, chain-linked volume; growth rate versus previous quarter; seasonally and calendar adjusted.",
        "pe_use": "Underlying domestic growth backdrop for revenue and exit-multiple underwriting."
    },
    "fx": {
        "label": "USD/KRW exchange rate",
        "flow": "WS_XRU",
        "key": "M.KR.KRW.E",
        "start_period": "2000-01",
        "unit": "KRW per USD",
        "frequency": "Monthly, end of period",
        "source": "Bank for International Settlements (BIS)",
        "source_url": "https://data.bis.org/topics/XRU/BIS%2CWS_XRU%2C1.0/M.KR.KRW.E",
        "transformation": "No transformation. Quotation is KRW per USD; an increase means KRW depreciation against USD.",
        "pe_use": "Entry/exit translation risk for a USD-based investor."
    },
    "reer": {
        "label": "Korea real effective exchange rate (REER)",
        "flow": "WS_EER",
        "key": "M.R.B.KR",
        "start_period": "2000-01",
        "unit": "Index, 2020 = 100",
        "frequency": "Monthly",
        "source": "Bank for International Settlements (BIS)",
        "source_url": "https://data.bis.org/topics/EER/BIS%2CWS_EER%2C1.0/M.R.B.KR",
        "transformation": "BIS broad real effective exchange rate. Higher = real appreciation. Dashboard adds a trailing 10-year median as a valuation benchmark, not as fair value.",
        "pe_use": "Medium/long-run currency valuation and competitiveness context."
    },
    "kr_policy": {
        "label": "Korea policy rate",
        "flow": "WS_CBPOL",
        "key": "M.KR",
        "start_period": "2000-01",
        "unit": "% per year",
        "frequency": "Monthly",
        "source": "Bank for International Settlements (BIS)",
        "source_url": "https://data.bis.org/topics/CBPOL/BIS%2CWS_CBPOL%2C1.0/M.KR",
        "transformation": "No transformation.",
        "pe_use": "Local financing and discount-rate environment."
    },
    "us_policy": {
        "label": "U.S. policy rate",
        "flow": "WS_CBPOL",
        "key": "M.US",
        "start_period": "2000-01",
        "unit": "% per year",
        "frequency": "Monthly",
        "source": "Bank for International Settlements (BIS)",
        "source_url": "https://data.bis.org/topics/CBPOL/BIS%2CWS_CBPOL%2C1.0/M.US",
        "transformation": "No transformation.",
        "pe_use": "USD funding benchmark."
    },
    "credit_gap": {
        "label": "Private non-financial credit-to-GDP gap",
        "flow": "WS_CREDIT_GAP",
        "key": "Q.KR.P.A.C",
        "start_period": "2000-Q1",
        "unit": "Percentage points of GDP",
        "frequency": "Quarterly",
        "source": "Bank for International Settlements (BIS)",
        "source_url": "https://data.bis.org/topics/CREDIT_GAPS/BIS%2CWS_CREDIT_GAP%2C1.0/Q.KR.P.A.C",
        "transformation": "BIS actual credit-to-GDP ratio minus its long-run trend. Positive = credit above trend.",
        "pe_use": "Financial-cycle leverage and downside-risk indicator."
    },
    "dsr": {
        "label": "Private non-financial debt service ratio",
        "flow": "WS_DSR",
        "key": "Q.KR.P",
        "start_period": "2000-Q1",
        "unit": "% of income",
        "frequency": "Quarterly",
        "source": "Bank for International Settlements (BIS)",
        "source_url": "https://data.bis.org/topics/DSR/BIS%2CWS_DSR%2C1.0/Q.KR.P",
        "transformation": "No dashboard transformation. BIS estimate of interest plus amortization relative to income.",
        "pe_use": "Debt burden and sensitivity to financing conditions."
    },
    "house_price": {
        "label": "Real residential property price growth",
        "flow": "WS_SPP",
        "key": "Q.KR.R.771",
        "start_period": "2000-Q1",
        "unit": "Year-on-year %",
        "frequency": "Quarterly",
        "source": "Bank for International Settlements (BIS)",
        "source_url": "https://data.bis.org/topics/RPP/BIS%2CWS_SPP%2C1.0/Q.KR.R.771",
        "transformation": "BIS CPI-deflated residential property price series, reported as year-on-year change.",
        "pe_use": "Domestic asset-cycle and collateral-value context."
    },
}
