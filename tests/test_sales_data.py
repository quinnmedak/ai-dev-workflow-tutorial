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


from sales_data import monthly_sales


def test_monthly_sales_groups_by_month_and_sums():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2024-01-05", "2024-01-20", "2024-02-10"]),
        "total_amount": [100.0, 50.0, 25.0],
    })
    result = monthly_sales(df)
    assert list(result["month"]) == ["2024-01", "2024-02"]
    assert list(result["sales"]) == [150.0, 25.0]


def test_monthly_sales_sorted_chronologically():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2024-03-01", "2024-01-01", "2024-02-01"]),
        "total_amount": [1.0, 1.0, 1.0],
    })
    result = monthly_sales(df)
    assert list(result["month"]) == ["2024-01", "2024-02", "2024-03"]


def test_monthly_sales_has_twelve_months_for_real_data():
    df = load_sales_data("data/sales-data.csv")
    result = monthly_sales(df)
    assert len(result) == 12


from sales_data import sales_by_category, sales_by_region


def test_sales_by_category_groups_and_sorts_descending():
    df = pd.DataFrame({
        "category": ["Audio", "Electronics", "Audio"],
        "total_amount": [10.0, 100.0, 5.0],
    })
    result = sales_by_category(df)
    assert list(result["category"]) == ["Electronics", "Audio"]
    assert list(result["sales"]) == [100.0, 15.0]


def test_sales_by_region_groups_and_sorts_descending():
    df = pd.DataFrame({
        "region": ["South", "North", "South"],
        "total_amount": [10.0, 100.0, 5.0],
    })
    result = sales_by_region(df)
    assert list(result["region"]) == ["North", "South"]
    assert list(result["sales"]) == [100.0, 15.0]


def test_sales_by_category_matches_real_data_top_category():
    df = load_sales_data("data/sales-data.csv")
    result = sales_by_category(df)
    assert result.iloc[0]["category"] == "Electronics"
    assert len(result) == 5


def test_sales_by_region_matches_real_data_all_regions():
    df = load_sales_data("data/sales-data.csv")
    result = sales_by_region(df)
    assert set(result["region"]) == {"North", "South", "East", "West"}
    assert len(result) == 4


def test_full_dataset_matches_prd_expected_output():
    df = load_sales_data("data/sales-data.csv")
    assert total_orders(df) == 482
    assert total_sales(df) == pytest.approx(116500.21, abs=0.01)
    assert sales_by_category(df).iloc[0]["category"] == "Electronics"
    assert set(sales_by_region(df)["region"]) == {"North", "South", "East", "West"}
