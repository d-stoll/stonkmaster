import configparser
import logging

from stonkmaster.commands.base import BaseCommand
from stonkmaster.core.market import get_info
from stonkmaster.tasks.update_status import UpdateStatusTask


class WatchCommand(BaseCommand):
    def __init__(self, config: configparser.ConfigParser, update_status_task: UpdateStatusTask):
        super().__init__(config)
        self.update_status_task = update_status_task

    async def execute(self, ctx, ticker):
        try:
            info = get_info(ticker)

            if len(info) <= 1:
                logging.info(f"{ctx.author.display_name} tried to watch invalid ticker {ticker}")
                await ctx.send(f"{ticker.upper()} gibt's ned oida! {self.config['emojis']['NotFound']}")
                return

            if 'longName' in info:
                msg = f"Alright, i'm watching **{info['longName']} ({info['symbol']})** now. " + \
                      self.config['emojis']['Eyes']
            else:
                msg = f"Alright, i'm watching **{info['symbol']}** now. {self.config['emojis']['Eyes']}"

            logging.info(f"{ctx.author.display_name} set watched ticker to {info['symbol']}")
            self.update_status_task.current_ticker = info['symbol']
            await self.update_status_task.loop()
            await ctx.send(msg)

        except Exception as ex:
            logging.exception(f"Exception in WatchCommand: {ex}")
            await ctx.send(f"Do hod wos ned bassd, I bin raus. {self.config['emojis']['Error']}")
