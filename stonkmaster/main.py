import os
import sys

from stonkmaster.core.bot import create_bot
from stonkmaster.core.config import get_config
from stonkmaster.core.setup import create_data_dir


def main():
    config = get_config(sys.argv[1:])
    create_data_dir(config)
    bot = create_bot(config)
    bot.run(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    main()
