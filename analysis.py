from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REQUIRED_COLUMNS = {"year", "category", "laureate", "gender", "country"}


def load_data(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
    frame = frame.copy()
    frame["year"] = pd.to_numeric(frame["year"], errors="raise").astype(int)
    frame["decade"] = frame["year"] // 10 * 10
    return frame


def category_counts(frame: pd.DataFrame) -> pd.Series:
    return frame.groupby("category").size().sort_values(ascending=False)


def gender_percentages(frame: pd.DataFrame) -> pd.Series:
    # percentage is easier to compare
    return (frame["gender"].fillna("Unknown").value_counts(normalize=True) * 100).round(1)


def decade_counts(frame: pd.DataFrame) -> pd.Series:
    return frame.groupby("decade").size().sort_index()


def make_charts(frame: pd.DataFrame, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = [output_dir / "prizes_by_category.png", output_dir / "awards_by_decade.png"]

    category_counts(frame).sort_values().plot(kind="barh", color="#287271", title="Sample awards by category")
    plt.xlabel("Awards in dataset")
    plt.tight_layout()
    plt.savefig(paths[0], dpi=150)
    plt.close()

    decade_counts(frame).plot(kind="line", marker="o", color="#b45309", title="Sample awards by decade")
    plt.ylabel("Awards in dataset")
    plt.tight_layout()
    plt.savefig(paths[1], dpi=150)
    plt.close()
    return paths


def main() -> None:
    frame = load_data(Path("data/nobel_sample.csv"))
    print("Awards by category")
    print(category_counts(frame).to_string())
    print("\nGender percentage in sample")
    print(gender_percentages(frame).to_string())
    for path in make_charts(frame, Path("figures")):
        print(f"Saved {path}")


if __name__ == "__main__":
    main()
