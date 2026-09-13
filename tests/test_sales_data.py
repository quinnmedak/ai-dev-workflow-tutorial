import pandas as pd
import pytest
from sales_data import load_sales_data

REQUIRED_COLUMNS = [
    "date", "order_id", "product", "category",
    "region", "quantity", "unit_price", "total_amount",
]


def test_load_sales_data_returns_dataframe_with_required_columns():
    df = load_sales_data("data/sales-data.csv")
    assert isinstance(df, pd.DataFrame)
    for column in REQUIRED_COLUMNS:
        assert column in df.columns


def test_load_sales_data_reads_all_rows():
    df = load_sales_data("data/sales-data.csv")
    assert len(df) == 482


def test_load_sales_data_missing_file_raises_file_not_found_error():
    with pytest.raises(FileNotFoundError):
        load_sales_data("data/does-not-exist.csv")


def test_load_sales_data_missing_required_column_raises_value_error(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("date,order_id,product\n2024-01-01,ORD-1,Widget\n")
    with pytest.raises(ValueError):
        load_sales_data(str(bad_csv))


from sales_data import total_sales, total_orders


def _fixture_df():
    return pd.DataFrame({
        "total_amount": [100.0, 50.0, 25.0],
    })


def test_total_sales_sums_total_amount():
    assert total_sales(_fixture_df()) == 175.0


def test_total_orders_counts_rows():
    assert total_orders(_fixture_df()) == 3


def test_total_sales_matches_expected_value_for_real_data():
    df = load_sales_data("data/sales-data.csv")
    assert total_sales(df) == pytest.approx(116500.21, abs=0.01)


def test_total_orders_matches_expected_value_for_real_data():
    df = load_sales_data("data/sales-data.csv")
    assert total_orders(df) == 482
