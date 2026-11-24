from __future__ import annotations

import io
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

from series_config import SERIES

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
LOG_PATH = ROOT / "refresh_log.json"
DATA_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": "Kellogg-International-Finance-Country-Dashboard/1.0",
    "Accept": "text/csv,*/*",
}


def _candidate_urls(flow: str, key: str):
    # BIS currently supports both endpoints. Trying both makes the dashboard
    # more robust to API format changes.
    return [
        (
            f"https://stats.bis.org/api/v1/data/{flow}/{key}/all",
            {"format": "csvfile"},
        ),
        (
            f"https://stats.bis.org/api/v2/data/dataflow/BIS/{flow}/1.0/{key}",
            {"format": "csv"},
        ),
    ]


def _parse_period(period: str) -> pd.Timestamp:
    period = str(period)
    if "-Q" in period:
        return pd.Period(period, freq="Q").end_time.normalize()
    if len(period) == 4:
        return pd.Timestamp(f"{period}-12-31")
    return pd.to_datetime(period, errors="coerce")


def fetch_bis_series(flow: str, key: str, start_period: str) -> pd.DataFrame:
    errors = []
    for url, base_params in _candidate_urls(flow, key):
        params = dict(base_params)
        params["startPeriod"] = start_period
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=60)
            r.raise_for_status()
            df = pd.read_csv(io.StringIO(r.text))
            if "TIME_PERIOD" not in df.columns or "OBS_VALUE" not in df.columns:
                raise ValueError(f"Unexpected BIS response columns: {list(df.columns)}")
            out = df[["TIME_PERIOD", "OBS_VALUE"]].copy()
            out["OBS_VALUE"] = pd.to_numeric(out["OBS_VALUE"], errors="coerce")
            out["date"] = out["TIME_PERIOD"].map(_parse_period)
            out = out.dropna(subset=["date", "OBS_VALUE"]).drop_duplicates(
                subset=["TIME_PERIOD"], keep="last"
            )
            out = out.sort_values("date").reset_index(drop=True)
            if out.empty:
                raise ValueError("BIS returned no usable observations.")
            return out
        except Exception as exc:
            errors.append(f"{url}: {exc}")
    raise RuntimeError(" | ".join(errors))



def fetch_oecd_gdp(start_period: str) -> pd.DataFrame:
    """
    OECD Quarterly real GDP growth - OECD countries.
    We request only GDP / period-on-period real growth from the specialized dataflow,
    then filter to Korea (KOR).
    """
    url = (
        "https://sdmx.oecd.org/public/rest/data/"
        "OECD.SDD.NAD,DSD_NAMAIN1@DF_QNA_EXPENDITURE_GROWTH_OECD,1.1/"
        "Q.....B1GQ......G1."
    )
    params = {
        "startPeriod": start_period,
        "dimensionAtObservation": "AllDimensions",
        "format": "csvfile",
    }
    r = requests.get(url, params=params, headers=HEADERS, timeout=60)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    required = {"TIME_PERIOD", "OBS_VALUE", "REF_AREA"}
    if not required.issubset(df.columns):
        raise ValueError(f"Unexpected OECD response columns: {list(df.columns)}")
    df = df[df["REF_AREA"].astype(str).eq("KOR")].copy()
    out = df[["TIME_PERIOD", "OBS_VALUE"]].copy()
    out["OBS_VALUE"] = pd.to_numeric(out["OBS_VALUE"], errors="coerce")
    out["date"] = out["TIME_PERIOD"].map(_parse_period)
    out = out.dropna(subset=["date", "OBS_VALUE"]).drop_duplicates(
        subset=["TIME_PERIOD"], keep="last"
    )
    out = out.sort_values("date").reset_index(drop=True)
    if out.empty:
        raise ValueError("OECD returned no usable Korea GDP observations.")
    return out


def refresh_all(write_files: bool = True):
    fetched = {}
    status = {}
    started = datetime.now(timezone.utc)

    for slug, cfg in SERIES.items():
        try:
            if cfg.get("provider", "BIS") == "OECD":
                df = fetch_oecd_gdp(cfg["start_period"])
            else:
                df = fetch_bis_series(cfg["flow"], cfg["key"], cfg["start_period"])
            fetched[slug] = df
            status[slug] = {
                "ok": True,
                "rows": int(len(df)),
                "latest_period": str(df.iloc[-1]["TIME_PERIOD"]),
                "latest_value": float(df.iloc[-1]["OBS_VALUE"]),
            }
            if write_files:
                df.to_csv(DATA_DIR / f"{slug}.csv", index=False)
        except Exception as exc:
            status[slug] = {"ok": False, "error": str(exc)}

    success = all(v.get("ok") for v in status.values())
    finished = datetime.now(timezone.utc)
    log = {
        "success": success,
        "started_utc": started.isoformat(),
        "finished_utc": finished.isoformat(),
        "series": status,
    }

    if write_files:
        LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")

    if not success:
        failed = [k for k, v in status.items() if not v.get("ok")]
        raise RuntimeError(f"Refresh failed for: {', '.join(failed)}")

    return fetched, log


if __name__ == "__main__":
    _, log = refresh_all(write_files=True)
    print(json.dumps(log, indent=2))
