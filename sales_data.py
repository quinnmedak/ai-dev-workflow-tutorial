import os
import pandas as pd

REQUIRED_COLUMNS = [
    "date", "order_id", "product", "category",
    "region", "quantity", "unit_price", "total_amount",
]


def load_sales_data(csv_path: str) -> pd.DataFrame:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Sales data file not found: {csv_path}")

    df = pd.read_csv(csv_path, parse_dates=["date"])

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Sales data is missing required columns: {missing}")

    return df


def total_sales(df: pd.DataFrame) -> float:
    return float(df["total_amount"].sum())


def total_orders(df: pd.DataFrame) -> int:
    return len(df)


def monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    monthly = df.copy()
    monthly["month"] = monthly["date"].dt.strftime("%Y-%m")
    result = monthly.groupby("month")["total_amount"].sum().reset_index()
    result = result.rename(columns={"total_amount": "sales"})
    return result.sort_values("month").reset_index(drop=True)
