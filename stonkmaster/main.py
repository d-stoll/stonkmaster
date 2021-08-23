import argparse
import configparser
import os

from discord.ext import commands

from stonkmaster.commands.ChartCommand import ChartCommand
from stonkmaster.commands.PriceCommand import PriceCommand
from stonkmaster.commands.SecCommand import SecCommand
from stonkmaster.commands.ShortsCommand import ShortsCommand


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path of configuration file.", default="/opt/stonkmaster/default.ini")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)

    help_command = commands.DefaultHelpCommand(no_category="Commands")
    bot = commands.Bot(command_prefix=config["discord.py"]["CommandPrefix"],
                       description=config["discord.py"]["description"],
                       help_command=help_command)

    bot.add_cog(ChartCommand(bot, config))
    bot.add_cog(PriceCommand(bot, config))
    bot.add_cog(SecCommand(bot, config))
    bot.add_cog(ShortsCommand(bot, config))

    bot.run(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    main()
