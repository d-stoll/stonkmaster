import configparser

from discord.ext import commands, tasks

from stonkmaster.cogs.base import BaseCog
from stonkmaster.commands.chart import ChartCommand
from stonkmaster.commands.price import PriceCommand
from stonkmaster.commands.watch import WatchCommand
from stonkmaster.tasks.update_status import UpdateStatusTask


class PriceChartCog(BaseCog, name="Price & Chart Commands"):

    def __init__(self, bot: commands.Bot, config: configparser.ConfigParser):
        super().__init__(bot, config)
        self.update_status_task = UpdateStatusTask(self.bot, self.config)
        self.price_command = PriceCommand(self.config)
        self.chart_command = ChartCommand(self.config)
        self.watch_command = WatchCommand(self.config, self.update_status_task)
        self.update_status.start()

    @commands.command(name="price")
    async def _price(self, ctx: commands.Context, ticker: str):
        """Shows the current price of the stonk, as well as its daily change."""
        await self.price_command.execute(ctx, ticker)

    @commands.command(name="watch")
    async def _watch(self, ctx: commands.Context, ticker: str):
        """Displays the price and change of a ticker in the status."""
        await self.watch_command.execute(ctx, ticker)

    @commands.command(name="chart")
    async def _chart(self, ctx: commands.Context, ticker: str, range: str = "1d"):
        """Generates a chart showing the price development of the share in the last months."""
        await self.chart_command.execute(ctx, ticker, range)

    @tasks.loop(seconds=20.0)
    async def update_status(self):
        await self.update_status_task.loop()

    @update_status.before_loop
    async def before_update_status(self):
        await self.update_status_task.before_loop()
