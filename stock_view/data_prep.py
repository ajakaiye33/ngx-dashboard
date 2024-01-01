"""
Created on Tue Jun 17 00:59:25 2021
@author: Hedgar Ajakaiye
"""

import pandas as pd
import json
from gazpacho import get, Soup
from datetime import datetime

# import requests

# Data Ingestion and Transformation
def load_equities_data(
    url="https://doclib.ngxgroup.com/REST/api/statistics/equities/?market=&sector=&orderby=&pageSize=300&pageNo=0",
):
    """
    Ingest and transform equities data.
    """
    # Load data from url
    data = pd.read_json(url)
    # Remove rows with NaN values
    data = data.dropna()
    return data


# Insider Trading Data
def get_insider_symbols(
    url="https://raw.githubusercontent.com/ajakaiye33/ngrcoydisclosures/main/docs/insider-dealings.csv",
):
    """
    Get a list of company symbols with recent insider dealings.
    """
    # Load data from url
    data = pd.read_csv(url, parse_dates=["date_created"])
    # Keep only the relevant columns
    data = data[["date_created", "company_symbol"]]
    # Add a new column with the day of the month
    data["day"] = data["date_created"].dt.day
    # Keep only the rows with a day value less than or equal to 30
    data = data[data["day"] <= 30]
    # Get the unique company symbols
    symbols = data["company_symbol"].unique().tolist()
    return symbols


def filter_top_gainers(data):
    """
    Filter top gaining equities.
    """
    # Keep only the rows where the opening price is less than the closing price
    data = data[data["OpeningPrice"] < data["ClosePrice"]]
    # Sort by descending order of change
    data = data.sort_values(by="Change", ascending=False)
    # Remove irrelevant columns
    columns_to_remove = [
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
    data = data.drop(columns_to_remove, axis=1)
    return data


def filter_top_losers(data):
    """
    Filter top losing equities.
    """
    # Keep only the rows where the opening price is greater than the closing price
    data = data[data["OpeningPrice"] > data["ClosePrice"]]
    # Sort by ascending order of change
    data = data.sort_values(by="Change", ascending=True)
    # Remove irrelevant columns
    columns_to_remove = [
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
    data = data.drop(columns_to_remove, axis=1)
    return data


# Define a function that retrieves and processes data for the dividend tracker feature
def dividend_tracker_data():
    """
    Returns data for the dividend tracker feature on the Streamlit dashboard.
    """
    # Get data from the corporate actions URL and convert it to a Pandas dataframe
    try:
        # Define the URL endpoint for corporate actions in 2023
        current_year = datetime.now().year
        previous_year = current_year - 1
        # CORP_ACTIONS_URL = f"https://ngxgroup.com/wp-json/corporate-actions/v1/by-year/{current_year}"
        CORP_ACTIONS_URL = (
            f"https://ngxgroup.com/wp-json/corporate-actions/v1/by-year/{current_year}"
        )

        data = pd.read_json(CORP_ACTIONS_URL)

        # Convert the 'cct_modified' column to a datetime object and sort the dataframe by this column
        data["cct_modified"] = pd.to_datetime(data["cct_modified"])
        data = data.sort_values(by="cct_modified", ascending=False)

        # Drop unnecessary columns and rename some columns for clarity
        data = data.drop(
            [
                "_ID",
                "cct_status",
                "year",
                "cct_author_id",
                "cct_created",
                "type",
                "company",
                "bonus",
            ],
            axis=1,
        )
        data = data.rename(
            columns={
                "company_symbol": "symbol",
                "closure_of_register": "register_closure_date",
                "dividend_share": "dividend_amount",
                "cct_modified": "date",
            }
        )

        # Set the 'date' column as the index and select the relevant columns
        data = data.reset_index(drop=True)
        data = data.set_index("date")
        data = data[
            [
                "symbol",
                "payment_date",
                "register_closure_date",
                "agm_date",
                "dividend_amount",
            ]
        ]
        return data
    except Exception as e:
        print(f"Data not available yet {e}")

    try:
        # Define the URL endpoint for corporate actions in 2023
        current_year = datetime.now().year
        previous_year = current_year - 1
        # CORP_ACTIONS_URL = f"https://ngxgroup.com/wp-json/corporate-actions/v1/by-year/{current_year}"
        CORP_ACTIONS_URL = (
            f"https://ngxgroup.com/wp-json/corporate-actions/v1/by-year/{previous_year}"
        )

        data = pd.read_json(CORP_ACTIONS_URL)

        # Convert the 'cct_modified' column to a datetime object and sort the dataframe by this column
        data["cct_modified"] = pd.to_datetime(data["cct_modified"])
        data = data.sort_values(by="cct_modified", ascending=False)

        # Drop unnecessary columns and rename some columns for clarity
        data = data.drop(
            [
                "_ID",
                "cct_status",
                "year",
                "cct_author_id",
                "cct_created",
                "type",
                "company",
                "bonus",
            ],
            axis=1,
        )
        data = data.rename(
            columns={
                "company_symbol": "symbol",
                "closure_of_register": "register_closure_date",
                "dividend_share": "dividend_amount",
                "cct_modified": "date",
            }
        )

        # Set the 'date' column as the index and select the relevant columns
        data = data.reset_index(drop=True)
        data = data.set_index("date")
        data = data[
            [
                "symbol",
                "payment_date",
                "register_closure_date",
                "agm_date",
                "dividend_amount",
            ]
        ]
        return data
    except Exception as e:
        print(f"Data not available yet {e}")


# Define the base URL for retrieving index data
INDEX_DATA_URL = "https://doclib.ngxgroup.com/REST/api/chartdata/"

# Define functions for retrieving and processing NGX50, NGX30, and NGXPENSION index data
def _get_index_data(index_name):
    """
    Retrieves index data from the NGX API for a given index name.
    """
    # Construct the URL for the given index and retrieve the data
    url = f"{INDEX_DATA_URL}{index_name}"
    url_req = get(url)
    soup = json.dumps(url_req)

    # Convert the data to a Pandas dataframe and format the 'date' column as a datetime object
    df = pd.read_json(soup)
    index_data = pd.DataFrame(df["IndiciesData"].to_list(), columns=["date", "prices"])
    index_data["date"] = pd.to_datetime(index_data["date"], unit="ms")

    return index_data


def ngx_50_index():
    """
    Returns NGX50 index data from the NGX API.
    """
    return _get_index_data("NGX50")


def ngx_30_index():
    """
    Returns NGX30 index data from the NGX API.
    """
    return _get_index_data("NGX30")


def ngx_pension_index():
    """
    Returns NGXPENSION index data from the NGX API.
    """
    return _get_index_data("NGXPENSION")


def latest_news():
    """
    Scrape stock news and links
    """
    html = get("https://stocksng.com/category/business-economy/")
    soup = Soup(html)
    article_title = soup.find("h2", {"class": "entry-title"})
    news_links = {i.find("a").text: i.find("a").attrs["href"] for i in article_title}
    # for news, link in news_links.items():
    return news_links
