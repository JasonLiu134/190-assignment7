"""Stage 2: add a date column."""
import os
import pandas as pd


def main() -> None:
    df = pd.read_csv("data/clean/events.csv", dtype={"user_id": str})
    df["date"] = df["timestamp"].str[:10]  # YYYY-MM-DD
    os.makedirs("data/transformed", exist_ok=True)
    df.to_csv("data/transformed/events.csv", index=False)


if __name__ == "__main__":
    main()