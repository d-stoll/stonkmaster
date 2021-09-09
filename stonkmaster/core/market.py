import datetime
import os
import requests
from io import StringIO

import pandas
import holidays
import pytz
import yfinance as yf

alpha_vantage_base_url = "https://www.alphavantage.co/query"


def get_price_and_change(symbol: str):
    yf_ticker = yf.Ticker(symbol)
    info = yf_ticker.info

    current = info['regularMarketPrice']
    previous = info['previousClose']
    change = ((current - previous) / previous) * 100

    return current, change


def is_market_closed(now=None):  # credits @Reddit u/numbuh-0

    tz = pytz.timezone('US/Eastern')
    us_holidays = holidays.US()
    if not now:
        now = datetime.datetime.now(tz)
    open_time = datetime.time(hour=9, minute=30, second=0)
    close_time = datetime.time(hour=16, minute=0, second=0)
    # If a holiday
    if now.strftime('%Y-%m-%d') in us_holidays:
        return True
    # If before 09:30 or after 16:00
    if (now.time() < open_time) or (now.time() > close_time):
        return True
    # If it's a weekend
    if now.date().weekday() > 4:
        return True

    return False


def intraday(symbol: str, interval: str, days: int):
    assert days < 60

    if days == 1:
        intraday_data = requests.get(alpha_vantage_base_url, params={
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol.upper(),
            "interval": interval,
            "apikey": os.environ['ALPHA_VANTAGE_TOKEN']
        }).json()

        df = pandas.DataFrame.from_dict(intraday_data[f"Time Series ({interval})"], orient='index')
        df.index = pandas.to_datetime(df.index)
        df["open"] = df["1. open"]
        df["high"] = df["2. high"]
        df["low"] = df["3. low"]
        df["close"] = df["4. close"]
        return df
    else:
        month = 1
        df = None

        while days > 0:
            monthly_intraday_data = requests.get(alpha_vantage_base_url, params={
                "function": "TIME_SERIES_INTRADAY_EXTENDED",
                "symbol": symbol.upper(),
                "interval": interval,
                "slice": f"year1month${month}",
                "apikey": os.environ['ALPHA_VANTAGE_TOKEN']
            }).content.decode("utf-8")

            batch = pandas.read_csv(StringIO(monthly_intraday_data), sep=',')
            batch.index = pandas.to_datetime(batch.index)

            if df is None:
                df = batch
            else:
                df.append(batch)

            days -= 30
            month += 1

        return df


def daily(symbol: str):
    daily_data = requests.get(alpha_vantage_base_url, params={
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol.upper(),
        "outputsize": "full",
        "apikey": os.environ['ALPHA_VANTAGE_TOKEN']
    }).json()

    df = pandas.DataFrame.from_dict(daily_data["Time Series (Daily)"], orient='index')
    df.index = pandas.to_datetime(df.index)
    df["open"] = df["1. open"]
    df["high"] = df["2. high"]
    df["low"] = df["3. low"]
    df["close"] = df["4. close"]
    return df
