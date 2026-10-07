from pathlib import Path
import json
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"


def load_sales_data() -> pd.DataFrame:
    file_path = DATA_DIR / "sales_data.csv"

    df = pd.read_csv(file_path, keep_default_na=False)

    df["order_date"] = pd.to_datetime(df["order_date"])

    df["revenue"] = (
        df["quantity"]
        * df["unit_price"]
        * (1 - df["discount"])
    )

    df["month"] = df["order_date"].dt.strftime("%Y-%m")

    return df


def load_targets() -> pd.DataFrame:
    file_path = DATA_DIR / "targets.csv"

    return pd.read_csv(file_path, keep_default_na=False)


def load_data_dictionary() -> dict:
    file_path = DATA_DIR / "data_dictionary.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)