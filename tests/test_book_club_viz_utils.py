import pandas as pd
import pytest

from book_club_viz_utils import get_num_meetings_from_df


@pytest.mark.parametrize(
    "date_columns_subset",
    [
        # empty subset
        [],
        # subset does not match any columns
        ["y", "m", "d"],
    ],
)
def test_get_num_meetings_from_df_raises_value_error(date_columns_subset):
    df = pd.DataFrame()
    with pytest.raises(ValueError):
        get_num_meetings_from_df(df=df, date_columns_subset=date_columns_subset)


@pytest.mark.parametrize(
    "input_df, date_columns_subset, expected_output",
    [
        # single row
        (pd.DataFrame({"y": [2001], "m": [1], "d": [1]}), ["y", "m", "d"], 1),
        # duplicate rows
        (
            pd.DataFrame({"y": [2001, 2001, 2002], "m": [1, 1, 1], "d": [1, 1, 1]}),
            ["y", "m", "d"],
            2,
        ),
        (
            pd.DataFrame({"y": [2001, 2001, 2001], "m": [1, 2, 1], "d": [1, 1, 1]}),
            ["y", "m", "d"],
            2,
        ),
        (
            pd.DataFrame({"y": [2001, 2001, 2001], "m": [1, 1, 1], "d": [1, 1, 2]}),
            ["y", "m", "d"],
            2,
        ),
        # no duplicates
        (
            pd.DataFrame({"y": [2001, 2002, 2003], "m": [1, 1, 1], "d": [1, 1, 1]}),
            ["y", "m", "d"],
            3,
        ),
        (
            pd.DataFrame({"y": [2001, 2001, 2001], "m": [1, 2, 3], "d": [1, 1, 1]}),
            ["y", "m", "d"],
            3,
        ),
        (
            pd.DataFrame({"y": [2001, 2001, 2001], "m": [1, 1, 1], "d": [1, 2, 3]}),
            ["y", "m", "d"],
            3,
        ),
        # non-unique subset
        (
            pd.DataFrame({"y": [2001, 2002, 2003], "m": [2, 2, 2], "d": [7, 8, 9]}),
            ["y", "m", "d"],
            3,
        ),
    ],
)
def test_get_num_meetings_from_df(
    input_df: pd.DataFrame,
    date_columns_subset: list[str],
    expected_output: int,
):
    output = get_num_meetings_from_df(
        df=input_df, date_columns_subset=date_columns_subset
    )
    assert output == expected_output
