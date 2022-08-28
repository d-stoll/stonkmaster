import logging

from stonkmaster.commands.base import BaseCommand
from stonkmaster.core.language import get_text
from stonkmaster.core.market import is_market_closed, get_info


class PriceCommand(BaseCommand):

    async def execute(self, ctx, ticker):
        try:
            info = get_info(ticker)

            if len(info) <= 1:
                logging.info(f"{ctx.author.display_name} tried to fetch price for invalid ticker {ticker}")
                await ctx.send(get_text("TickerNotFound", self.config).format(ticker.upper(),
                                                                              self.config['emojis']['NotFound']))
                return

            current = info['regularMarketPrice']
            previous = info['previousClose']
            symbol = info['symbol']
            change = ((current - previous) / previous) * 100
            emoji = self.config['emojis']['StockUp'] if change >= 0 else self.config['emojis']['StockDown']

            if 'longName' in info:
                msg = (f"The market price of **{info['longName']} ({symbol})** is **{round(current, 2)}$** "
                       f"({'{0:+.2f}'.format(change)}%)  {emoji}")
            else:
                msg = (f"The market price of **{symbol}** is **{round(current, 2)}$** "
                       f"({'{0:+.2f}'.format(change)}%)  {emoji}")

            logging.info(f"{ctx.author.display_name} fetched price for ticker {symbol} (current={current}, " +
                         f"previous={previous}, change={change}%)")
            await ctx.send(msg)

            if is_market_closed():
                await ctx.send(f"Market is currently **closed** {self.config['emojis']['Closed']}")
            elif symbol == 'GME':
                await ctx.send("Wennst ned woasd, wannst GME vakaffa wuisd, kosd de do orientiern: " +
                               f"<https://gmefloor.com/> {self.config['emojis']['Money']}")
                await ctx.send("Weitere Infos findst do: <https://gme.crazyawesomecompany.com/> " +
                               f"{self.config['emojis']['Bulb']}")

        except Exception as ex:
            logging.exception(f"Exception in PriceCommand: {ex}")
            await ctx.send(get_text("ErrorMsg", self.config).format(self.config['emojis']['Error']))
