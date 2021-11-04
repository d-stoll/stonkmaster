import datetime
import os
from io import StringIO

import holidays
import pandas
import pytz
import requests
import yfinance as yf

alpha_vantage_base_url = "https://www.alphavantage.co/query"


def get_info(symbol: str):
    return yf.Ticker(symbol).info


def get_price_and_change(symbol: str):
    yf_ticker = yf.Ticker(symbol)
    info = yf_ticker.info

    current = info.get('regularMarketPrice')
    previous = info.get('previousClose', current)
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
    assert days < 31

    diff = datetime.timedelta(days=days)
    tz = pytz.timezone("America/New_York")
    end = datetime.datetime.now(tz)
    start = end - diff

    # We should use alpha vantage since it's more stable, however av does not contain the current day.
    if days == 1:
        df = yf.Ticker(symbol).history(period="1d", interval=interval.replace("min", "m"))
        df = df.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close"
        })
    else:
        monthly_intraday_data = requests.get(alpha_vantage_base_url, params={
            "function": "TIME_SERIES_INTRADAY_EXTENDED",
            "symbol": symbol.upper(),
            "interval": interval,
            "slice": "year1month1",
            "apikey": os.environ['ALPHA_VANTAGE_TOKEN']
        }).content.decode("utf-8")

        df = pandas.read_csv(StringIO(monthly_intraday_data), sep=',')
        df = df.set_index("time")
        df.index = pandas.to_datetime(df.index).tz_localize("America/New_York")

        # Alpha vantage only updates over night, so it does not contain the data from today (if today is an trading day)
        if not is_market_closed():
            df = df.append(intraday(symbol, interval, 1))

    df = df.loc[df.index >= start]
    return df


def daily(symbol: str, days: int):
    diff = datetime.timedelta(days=days)
    end = datetime.date.today()
    start = end - diff

    daily_data = requests.get(alpha_vantage_base_url, params={
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol.upper(),
        "outputsize": "full",
        "apikey": os.environ['ALPHA_VANTAGE_TOKEN']
    }).json()

    df = pandas.DataFrame.from_dict(daily_data["Time Series (Daily)"], orient='index')
    df.index = pandas.to_datetime(df.index)
    df = df.rename(columns={
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close"
    })

    # Alpha vantage only updates over night, so it does not contain the data from today (if today is an trading day)
    if not is_market_closed():
        current_info = yf.Ticker(symbol).info
        df.loc[pandas.to_datetime(datetime.date.today().strftime("%Y-%m-%d"))] = {
            "open": current_info['regularMarketOpen'],
            "high": current_info['regularMarketDayHigh'],
            "low": current_info['regularMarketDayLow'],
            "close": current_info['currentPrice'],
        }

    df = df.loc[df.index >= pandas.to_datetime(start.strftime("%Y-%m-%d"))]
    return df
