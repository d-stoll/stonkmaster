import os

from discord.ext import commands


def alpha_vantage_command():
    async def predicate(ctx: commands.Context):
        if os.environ['ALPHA_VANTAGE_TOKEN'] is None:
            await ctx.send("**An Alpha Vantage API key must be provided in order to use this command.** :key:")
            return False
        return True

    return commands.check(predicate)
