import datetime

import holidays
import pytz
import yfinance as yf


def get_price_and_change(symbol: str):
    yf_ticker = yf.Ticker(symbol)
    info = yf_ticker.info

    current = info['regularMarketPrice']
    previous = info['previousClose']
    change = round(((current - previous) / previous) * 100, 2)

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