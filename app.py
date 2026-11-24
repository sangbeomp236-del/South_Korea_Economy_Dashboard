from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from refresh_data import refresh_all
from series_config import SERIES

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
LOG_PATH = ROOT / "refresh_log.json"

st.set_page_config(
    page_title="Korea PE Macro-FX Monitor",
    page_icon="🇰🇷",
    layout="wide",
)

st.markdown(
    """
<style>
.block-container {max-width: 1320px; padding-top: 2rem; padding-bottom: 3rem;}
.small-note {font-size: 0.82rem; color: #666;}
.chart-meta {font-size: 0.78rem; color: #626262; line-height: 1.35;}
.pe-note {font-size: 0.86rem; background: #f6f7f9; border-left: 3px solid #555;
          padding: 0.55rem 0.7rem; margin-top: 0.25rem; margin-bottom: 1rem;}
</style>
""",
    unsafe_allow_html=True,
)

st.title("Korea PE Macro-FX Monitor")
st.caption(
    "Question: Is Korea's macro-financial and FX environment becoming more favorable "
    "for a USD-based private equity investor?"
)

st.info(
    "This dashboard is a country-level screening tool, not an investment recommendation. "
    "It focuses on currency valuation, funding conditions and the domestic financial cycle. "
    "Target-company fundamentals still need separate underwriting."
)


def parse_date_col(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    x["date"] = pd.to_datetime(x["date"], errors="coerce")
    return x.dropna(subset=["date", "OBS_VALUE"]).sort_values("date")


@st.cache_data(ttl=900)
def read_snapshots():
    data = {}
    for slug in SERIES:
        p = DATA_DIR / f"{slug}.csv"
        if not p.exists():
            return None
        data[slug] = parse_date_col(pd.read_csv(p))
    return data


def read_log():
    if LOG_PATH.exists():
        try:
            return json.loads(LOG_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return None


if "live_data" not in st.session_state:
    st.session_state["live_data"] = None
if "live_log" not in st.session_state:
    st.session_state["live_log"] = None

c1, c2, c3 = st.columns([1, 1, 2])
with c1:
    if st.button("Refresh data now", use_container_width=True):
        try:
            with st.spinner("Fetching current OECD/BIS data..."):
                d, log = refresh_all(write_files=False)
            st.session_state["live_data"] = d
            st.session_state["live_log"] = log
            st.success("Live refresh succeeded.")
        except Exception as exc:
            st.error(f"Live refresh failed: {exc}")

with c2:
    if st.button("Use scheduled snapshot", use_container_width=True):
        st.session_state["live_data"] = None
        st.session_state["live_log"] = None
        st.cache_data.clear()
        st.rerun()

snapshot_data = read_snapshots()
scheduled_log = read_log()

if st.session_state["live_data"] is not None:
    data = st.session_state["live_data"]
    active_log = st.session_state["live_log"]
    refresh_type = "Live session refresh"
elif snapshot_data is not None:
    data = snapshot_data
    active_log = scheduled_log
    refresh_type = "Scheduled GitHub Actions snapshot"
else:
    try:
        with st.spinner("No snapshot found. Fetching BIS data..."):
            data, active_log = refresh_all(write_files=False)
        refresh_type = "Live fallback refresh"
    except Exception as exc:
        st.error(
            "No local snapshot is available and live OECD/BIS retrieval failed. "
            f"Error: {exc}"
        )
        st.stop()

with c3:
    refresh_ts = None
    if active_log:
        refresh_ts = active_log.get("finished_utc")
    if refresh_ts:
        st.metric("Last successful refresh", refresh_ts.replace("T", " ")[:19] + " UTC")
        st.caption(refresh_type)
    else:
        st.metric("Last successful refresh", "Not recorded")
        st.caption(refresh_type)

st.divider()

start_year = st.sidebar.slider("Chart start year", 2000, datetime.now().year, 2010)
st.sidebar.markdown(
    "**FX convention**  \nUSD/KRW is reported as **KRW per USD**. "
    "A higher number means the Korean won has depreciated against the U.S. dollar."
)
st.sidebar.markdown(
    "**Sources**  \nBIS for FX/financial conditions; OECD for quarterly real GDP growth."
)

def trim(df):
    return df[df["date"].dt.year >= start_year].copy()


def latest_text(df):
    if df.empty:
        return "N/A", "N/A"
    row = df.iloc[-1]
    return str(row["TIME_PERIOD"]), f'{row["OBS_VALUE"]:,.2f}'


def line_chart(df, title, y_title, zero=False, benchmark=None, benchmark_label=None):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["OBS_VALUE"],
            mode="lines",
            name=title,
            line=dict(width=2.2),
        )
    )
    if zero:
        fig.add_hline(y=0, line_dash="dash", opacity=0.45)
    if benchmark is not None:
        fig.add_hline(
            y=benchmark,
            line_dash="dash",
            opacity=0.55,
            annotation_text=benchmark_label or "Benchmark",
            annotation_position="top left",
        )
    fig.update_layout(
        title=dict(text=title, font=dict(size=17)),
        height=330,
        margin=dict(l=20, r=20, t=55, b=15),
        xaxis_title="",
        yaxis_title=y_title,
        hovermode="x unified",
        showlegend=False,
    )
    return fig


def meta_html(cfg, latest_period, transform_override=None, extra_source=None):
    source_text = cfg["source"]
    if extra_source:
        source_text += f" + {extra_source}"
    transform = transform_override or cfg["transformation"]
    return (
        f"<div class='chart-meta'><b>Unit:</b> {cfg['unit']} &nbsp;|&nbsp; "
        f"<b>Frequency:</b> {cfg['frequency']} &nbsp;|&nbsp; "
        f"<b>Source:</b> {source_text} &nbsp;|&nbsp; "
        f"<b>Latest observation:</b> {latest_period}<br>"
        f"<b>Transformation / convention:</b> {transform}</div>"
    )


def pe_note(text):
    st.markdown(f"<div class='pe-note'><b>PE lens:</b> {text}</div>", unsafe_allow_html=True)


# Derived policy-rate spread
krp = data["kr_policy"][["TIME_PERIOD", "date", "OBS_VALUE"]].rename(
    columns={"OBS_VALUE": "KR"}
)
usp = data["us_policy"][["TIME_PERIOD", "date", "OBS_VALUE"]].rename(
    columns={"OBS_VALUE": "US"}
)
spread = pd.merge(krp[["date", "KR"]], usp[["date", "US"]], on="date", how="inner")
spread["OBS_VALUE"] = spread["KR"] - spread["US"]
spread["TIME_PERIOD"] = spread["date"].dt.strftime("%Y-%m")
spread = spread[["TIME_PERIOD", "date", "OBS_VALUE", "KR", "US"]]

# REER 10-year median as a simple historical benchmark
reer_full = data["reer"].copy()
latest_reer_date = reer_full["date"].max()
ten_year_cut = latest_reer_date - pd.DateOffset(years=10)
reer_median_10y = reer_full.loc[reer_full["date"] >= ten_year_cut, "OBS_VALUE"].median()

rows = [
    ("gdp", "Real GDP growth", True, None),
    ("fx", "USD/KRW exchange rate", False, None),
    ("reer", "Korea broad REER", False, reer_median_10y),
    ("spread", "Korea − U.S. policy-rate spread", True, None),
    ("credit_gap", "Private non-financial credit-to-GDP gap", True, None),
    ("dsr", "Private non-financial debt service ratio", False, None),
    ("house_price", "Real residential property price growth", True, None),
]

col_a, col_b = st.columns(2)

for i, (slug, title, zero, benchmark) in enumerate(rows):
    col = col_a if i % 2 == 0 else col_b
    with col:
        if slug == "spread":
            df = trim(spread)
            lp, lv = latest_text(df)
            fig = line_chart(df, title, "Percentage points", zero=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(
                (
                    "<div class='chart-meta'><b>Unit:</b> Percentage points &nbsp;|&nbsp; "
                    "<b>Frequency:</b> Monthly &nbsp;|&nbsp; "
                    "<b>Source:</b> BIS Korea and U.S. policy-rate series &nbsp;|&nbsp; "
                    f"<b>Latest observation:</b> {lp}<br>"
                    "<b>Transformation:</b> Korea policy rate minus U.S. policy rate.</div>"
                ),
                unsafe_allow_html=True,
            )
            pe_note(
                "A wider positive spread can support KRW carry, but it also means a higher local "
                "rate environment. I would use it together with DSR, not in isolation."
            )
        else:
            cfg = SERIES[slug]
            df = trim(data[slug])
            lp, lv = latest_text(df)
            fig = line_chart(
                df,
                title,
                cfg["unit"],
                zero=zero,
                benchmark=benchmark,
                benchmark_label=("10-year median" if slug == "reer" else None),
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(meta_html(cfg, lp), unsafe_allow_html=True)
            pe_note(cfg["pe_use"])

st.divider()
st.subheader("How I would use the dashboard in a PE screen")
st.markdown(
    """
1. **Growth backdrop:** Real GDP momentum provides a simple macro check on domestic revenue conditions.
2. **Entry valuation:** A weak KRW and a relatively low REER can make Korean assets cheaper in USD,
   but I would distinguish valuation opportunity from macro stress.
3. **Funding:** The Korea–U.S. policy spread and the debt service ratio show whether local leverage
   is becoming more or less burdensome.
4. **Financial cycle:** A large positive credit gap and strong real house-price growth can signal
   late-cycle leverage and collateral risk.
5. **Exit:** I would run exit-value sensitivities under several USD/KRW scenarios rather than assume
   today's exchange rate persists.
"""
)

st.subheader("Verification table")
verification_rows = []
for slug, cfg in SERIES.items():
    df = data[slug]
    latest = df.iloc[-1]
    verification_rows.append(
        {
            "Raw series": cfg["label"],
            "Series key": cfg.get("key", "OECD QNA: GDP / period-on-period real growth"),
            "Latest observation": str(latest["TIME_PERIOD"]),
            "Latest value from API": float(latest["OBS_VALUE"]),
            "Unit": cfg["unit"],
            "Official source page": cfg["source_url"],
        }
    )
ver_df = pd.DataFrame(verification_rows)
st.dataframe(
    ver_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Official source page": st.column_config.LinkColumn("Official source page")
    },
)
st.download_button(
    "Download verification snapshot (CSV)",
    data=ver_df.to_csv(index=False).encode("utf-8"),
    file_name="korea_dashboard_verification_snapshot.csv",
    mime="text/csv",
)

with st.expander("Refresh evidence / audit trail"):
    if active_log:
        st.json(active_log)
    else:
        st.write("No refresh log available.")
    st.caption(
        "For submission evidence, capture (1) this refresh panel after a successful refresh and "
        "(2) the GitHub Actions run showing the scheduled job completed successfully."
    )

with st.expander("Sources and definitions"):
    for slug, cfg in SERIES.items():
        st.markdown(
            f"**{cfg['label']}**  \n"
            f"- Series key: `{cfg.get('key', 'OECD QNA: GDP / period-on-period real growth')}`  \n"
            f"- Unit: {cfg['unit']}  \n"
            f"- Frequency: {cfg['frequency']}  \n"
            f"- Definition / transformation: {cfg['transformation']}  \n"
            f"- [Official BIS series page]({cfg['source_url']})"
        )

st.caption(
    "Data attribution: Bank for International Settlements (BIS) and OECD. "
    "Dashboard prepared for Kellogg International Finance."
)
