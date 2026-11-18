import marimo

app = marimo.App()


@app.cell
def _():
    from pathlib import Path

    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd

    return Path, mo, pd, plt


@app.cell
def _(Path, pd):
    root = Path(__file__).resolve().parent.parent
    df = pd.read_csv(root / "data" / "features" / "events.csv")
    df.head()
    return (df,)


@app.cell
def _(df, mo, plt):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.hist(df["duration_minutes"], bins=30, edgecolor="black")
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Number of events")
    ax.set_title("Distribution of event durations")
    mo.mpl.interactive(fig)
    return


if __name__ == "__main__":
    app.run()