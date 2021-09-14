import configparser

from discord.ext import commands, tasks

from stonkmaster.cogs.base import BaseCog
from stonkmaster.commands.chart import ChartCommand
from stonkmaster.commands.price import PriceCommand
from stonkmaster.tasks.update_status import UpdateStatusTask


class TechnicalsCog(BaseCog, name="Technicals"):

    def __init__(self, bot: commands.Bot, config: configparser.ConfigParser):
        super().__init__(bot, config)
        self.price_command = PriceCommand(self.config)
        self.chart_command = ChartCommand(self.config)
        self.update_status_task = UpdateStatusTask(self.bot, self.config)

    @commands.command(name="price",
                      description="Shows the current price of the stonk, as well as its daily change.")
    async def _price(self, ctx: commands.Context, ticker: str):
        await self.price_command.execute(ctx, ticker)

    @commands.command(name="watch",
                      description="Displays the price and change of a ticker in the status.")
    async def _watch(self, ctx: commands.Context, ticker: str):
        pass

    @commands.command(name="chart",
                      description="Generates a chart showing the price development of the share in the last months.")
    async def _chart(self, ctx: commands.Context, ticker: str, range: str):
        await self.chart_command.execute(ctx, ticker, range)

    @tasks.loop(seconds=20.0)
    async def update_status(self):
        await self.update_status_task.loop()

    @update_status.before_loop
    async def before_update_status(self):
        await self.update_status_task.before_loop()
