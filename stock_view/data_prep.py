import pandas as pd


def data_load(
    URL="https://doclib.ngxgroup.com/REST/api/statistics/equities/?market="
    "&sector=&orderby=&pageSize=300&pageNo=0",
):
    """
    Ingest and transform data
    """
    dataz = pd.read_json(URL)
    # drop all na in data
    data_api = dataz.dropna()
    return data_api


def insider_data(
    URL="https://raw.githubusercontent.com/ajakaiye33/ngrcoydisclosures/"
    "main/docs/insider-dealings.csv",
):
    df = pd.read_csv(URL, parse_dates=["date_created"])
    work_element = ["date_created", "company_symbol"]
    df = df[work_element]
    df["Last_hours"] = df["date_created"].dt.day
    df = df.drop("date_created", axis=1)
    df = df[df["Last_hours"] <= 30]
    df = df["company_symbol"].unique()
    df = df.tolist()
    return df


def top_gainers(df):
    """
    Filter Top Gainers
    """
    df = df[df["OpeningPrice"] < df["ClosePrice"]]
    df = df.sort_values(by="Change", ascending=False)
    remove = [
        "$id",
        "CalculateChangePercent",
        "Id",
        "PrevClosingPrice",
        "HighPrice",
        "LowPrice",
        "PercChange",
        "Trades",
        "Volume",
        "Value",
        "Market",
        "Sector",
        "Company2",
        "TradeDate",
    ]
    df = df.drop(remove, axis=1)
    return df


def top_losers(df):
    df = df[df["OpeningPrice"] > df["ClosePrice"]]
    df = df.sort_values(by="Change", ascending=True)
    remove = [
        "$id",
        "CalculateChangePercent",
        "Id",
        "PrevClosingPrice",
        "HighPrice",
        "LowPrice",
        "PercChange",
        "Trades",
        "Volume",
        "Value",
        "Market",
        "Sector",
        "Company2",
        "TradeDate",
    ]
    df = df.drop(remove, axis=1)
    return df
