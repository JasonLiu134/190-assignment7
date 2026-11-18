"""Stage 3: add duration_minutes and weekday."""
import os
import pandas as pd


def main() -> None:
    df = pd.read_csv("data/transformed/events.csv", dtype={"user_id": str})
    df["duration_minutes"] = df["duration_seconds"] / 60
    df["weekday"] = pd.to_datetime(df["date"]).dt.day_name()
    os.makedirs("data/features", exist_ok=True)
    df.to_csv("data/features/events.csv", index=False)


if __name__ == "__main__":
    main()