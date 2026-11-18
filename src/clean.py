"""Stage 1: clean raw events."""
import pandas as pd

RAW = "data/raw/events.csv"
OUT = "data/clean/events.csv"

# Adjust to the event types that actually appear in your data
# (inspect with: uv run python -c "import pandas as pd; print(pd.read_csv('data/raw/events.csv').event_type.value_counts())")
VALID_EVENT_TYPES = {"click", "view", "purchase", "login", "logout"}

COLUMNS = ["user_id", "timestamp", "event_type", "duration_seconds"]


def parse_timestamp(value: str):
    """Parse a timestamp in any of several formats; return NaT if unparseable."""
    s = str(value).strip()
    if s.replace(".", "", 1).isdigit():  # Unix epoch (seconds or milliseconds)
        num = float(s)
        unit = "ms" if num > 1e11 else "s"
        return pd.to_datetime(num, unit=unit, utc=True)
    try:
        return pd.to_datetime(s, utc=True)
    except (ValueError, TypeError):
        return pd.NaT


def main() -> None:
    df = pd.read_csv(RAW, dtype=str, keep_default_na=False)
    df = df[COLUMNS].apply(lambda c: c.str.strip())
    df = df.replace("", pd.NA).dropna()

    df["event_type"] = df["event_type"].str.lower()
    df = df[df["event_type"].isin(VALID_EVENT_TYPES)]

    df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")
    df = df[df["duration_seconds"] > 0]  # also drops NaN (non-numeric)
    df["duration_seconds"] = df["duration_seconds"].round().astype("int64")

    ts = df["timestamp"].map(parse_timestamp)
    df = df[ts.notna()].copy()
    df["timestamp"] = ts[ts.notna()].dt.strftime("%Y-%m-%dT%H:%M:%S")

    import os
    os.makedirs("data/clean", exist_ok=True)
    df.to_csv(OUT, index=False)


if __name__ == "__main__":
    main()