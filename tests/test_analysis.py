from pathlib import Path

import pandas as pd
import pytest

from analysis import (
    category_counts,
    decade_counts,
    gender_percentages,
    load_data,
    make_charts,
)


def test_load_adds_decade(tmp_path: Path):
    path = tmp_path / "data.csv"
    path.write_text("year,category,laureate,gender,country\n2018,Physics,A,Female,Canada\n", encoding="utf-8")
    frame = load_data(path)
    assert frame.loc[0, "decade"] == 2010


def test_missing_columns_are_rejected(tmp_path: Path):
    path = tmp_path / "data.csv"
    path.write_text("year,category\n2020,Chemistry\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Missing columns"):
        load_data(path)


def test_summary_functions():
    frame = pd.DataFrame(
        {
            "year": [2001, 2002, 2011],
            "decade": [2000, 2000, 2010],
            "category": ["Peace", "Peace", "Physics"],
            "gender": ["Female", "Male", "Female"],
        }
    )
    assert category_counts(frame)["Peace"] == 2
    assert decade_counts(frame).to_dict() == {2000: 2, 2010: 1}
    assert gender_percentages(frame)["Female"] == 66.7


def test_charts_are_created(tmp_path: Path):
    frame = pd.DataFrame(
        {"year": [2020], "decade": [2020], "category": ["Chemistry"], "gender": ["Female"]}
    )
    paths = make_charts(frame, tmp_path)
    assert all(path.exists() and path.stat().st_size > 0 for path in paths)
