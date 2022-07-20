import pandas as pd
import json
from gazpacho import get


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
#Index & its metric

AP = "https://doclib.ngxgroup.com/REST/api/chartdata/"

#NGX50
def ngx_50_index():
    ng50 = 'NGX50'
    URL = f'{AP}{ng50}'
    url_req = get(URL)
    soup = json.dumps(url_req)
    df = pd.read_json(soup)
    ngx50 = pd.DataFrame(df["IndiciesData"].to_list(), columns=["date", "prices"])
    ngx50["date"] = pd.to_datetime(ngx50["date"], unit="ms")
    return ngx50

#NGX30
def ngx_30_index():
    ng30 = 'NGX30'
    URL = f"{AP}{ng30}"
    url_req = get(URL)
    soup = json.dumps(url_req)
    df = pd.read_json(soup)
    ngx30 = pd.DataFrame(df["IndiciesData"].to_list(), columns=["date", "prices"])
    ngx30["date"] = pd.to_datetime(ngx30["date"], unit="ms")
    return ngx30

#NGXPENSION
def ngx_pension_index():
    ngpens = 'NGXPENSION'
    URL = f"{AP}{ngpens}"
    url_req = get(URL)
    soup = json.dumps(url_req)
    df = pd.read_json(soup)
    ngxpen = pd.DataFrame(df["IndiciesData"].to_list(), columns=["date", "prices"])
    ngxpen["date"] = pd.to_datetime(ngxpen["date"], unit="ms")
    return ngxpen
    
# current NGX50    
def current_p50():
    curr50 = 'NGX50'
    html = f"{AP}{curr50}"

    url = get(html)
    soup = json.dumps(url)
    df = pd.read_json(soup)
    df = df.iloc[0,1]
    return df
    
#current NGX30   
def current_p30():
    curr30 = 'NGX30'
    html = f"{AP}{curr30}"

    url = get(html)
    soup = json.dumps(url)
    df = pd.read_json(soup)
    df = df.iloc[0,1]
    return df

#current NGXPENSION    
def current_pens():
    currp = 'NGXPENSION'
    html = f"{AP}{currp}"

    url = get(html)
    soup = json.dumps(url)
    df = pd.read_json(soup)
    df = df.iloc[0,1]
    return df
    
#previous NGX50   
def yesterday_p50():
    yes50 = 'NGX50'
    html = f"{AP}{yes50}"
    url = get(html)
    soup = json.dumps(url)
    df = pd.read_json(soup)
    ngx30 = pd.DataFrame(df['IndiciesData'].to_list(),columns=['date','prices'])
    ngx30['date'] = pd.to_datetime(ngx30['date'],unit='ms')
    pricey = ngx30.iloc[-2,1]
    return pricey

#previous NGX30
def yesterday_p30():
    yes30 = 'NGX30'
    html = f"{AP}{yes30}"
    url = get(html)
    soup = json.dumps(url)
    df = pd.read_json(soup)
    ngx30 = pd.DataFrame(df['IndiciesData'].to_list(),columns=['date','prices'])
    ngx30['date'] = pd.to_datetime(ngx30['date'],unit='ms')
    pricey = ngx30.iloc[-2,1]
    return pricey
    
    
#previous NGXPENSION
def yesterday_pens():
    yesp = 'NGXPENSION'
    html = f"{AP}{yesp}"
    url = get(html)
    soup = json.dumps(url)
    df = pd.read_json(soup)
    ngx30 = pd.DataFrame(df['IndiciesData'].to_list(),columns=['date','prices'])
    ngx30['date'] = pd.to_datetime(ngx30['date'],unit='ms')
    pricey = ngx30.iloc[-2,1]
    return pricey