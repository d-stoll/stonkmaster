<h1 align="center">
  <br>
  The Stonk Master 📈💎🙌
  <br>
</h1>

<h4 align="center">Simple bot to monitor stocks, options and cryptos.</h4>

<p align="center">
  <a href="https://github.com/d-stoll/stonkmaster/actions/workflows/build.yml/badge.svg">
    <img src="https://github.com/d-stoll/stonkmaster/actions/workflows/build.yml/badge.svg" alt="Build status">
  </a>
  <a href="https://img.shields.io/github/license/d-stoll/stonkmaster">
    <img src="https://img.shields.io/github/license/d-stoll/stonkmaster" alt="License">
  </a>
  <a href="https://img.shields.io/github/languages/top/d-stoll/stonkmaster">
    <img src="https://img.shields.io/github/languages/top/d-stoll/stonkmaster" alt="Top language">
  </a>
  <a href="https://github.com/Rapptz/discord.py/">
    <img src="https://img.shields.io/badge/discord-py-blue.svg" alt="discord.py">
  </a>
  <a href="https://img.shields.io/badge/code%20quality-excellent-brightgreen">
    <img src="https://img.shields.io/badge/code%20quality-excellent-brightgreen" alt="Code quality">
  </a>
</p>

<p align="center">
  <a href="#overview">Overview</a>
  •
  <a href="#installation">Installation</a>
  •
  <a href="#features">Features</a>
  •
  <a href="#configuration">Configuration</a>
  •
  <a href="#license">License</a>
</p>

## Overview

The Stonk Master is a Discord bot for fellow apes to monitor stonks without leaving their gaming habitat. It presents information about stonks in a very easy and simple way.

## Installation

The installation is only tested on Ubuntu 20.04 LTS, however other operating systems should also work without any
problem.

Make sure Python 3.8 (or higher) and pip are installed on your system. Then simply run:

```{bash}
pip install stonkmaster
```

(Optional) Some commands access the alpha vantage API, so they are only usable if an API key is defined. You can claim your free personal api key [here](https://www.alphavantage.co/support/#api-key). It takes only a minute and there are no payment methods required.

```{bash}
export ALPHA_VANTAGE_TOKEN=<YOUR_PERSONAL_ALPHA_VANTAGE_KEY>
```

It is necessary to obtain your personal discord token and define it as an environment variable before starting the bot.

```{bash}
export DISCORD_TOKEN=<YOUR_PERSONAL_DISCORD_TOKEN>
```

To start the bot, simply run the stonkmaster executable:

```{bash}
stonkmaster
```

## Features

The main functionality of the bot is to query data from financial APIs and make it quickly accessible to users via a
simple interface. For this purpose, we have developed a collection of commands that you can use.

### Commands

- `$price [ticker]` -> Shows the current price of the stonk, as well as its daily change.
- `$shorts [ticker]` -> Provides currently known information on how heavily the stonk is shorted.
- `$sec [ticker] [filing-type]` -> Fetches the latest SEC company filings from EDGAR.
- `$watch [ticker]` -> Displays the price and change of a ticker in the bot status.
- `$wiki [keywords...]` -> Searches investopedia for a definition of the keyword.

Following commands access the alpha vantage API, so a valid API key must be set up:

- `$chart [ticker] [range]` -> Generates a chart showing the price development of the ticker over. The range can be specified in days (d), months (m) or years (y).

In future releases we also plan to implement the following commands:

- `$options [ticker]` -> Displays options and their greeks of a specified ticker.
- `$config [key] [value]` -> Changes the configuration of the bot (for example the emotes).
- `$watchlist [ticker]` -> Adds a ticker to your personal watchlist. The bot will inform you about movements in your
  stocks.
- `$ipos` -> Shows all IPOs that are likely to take place in the next 2 weeks.
- `$earnings` -> Shows all company earnings expected in the next 2 weeks.
- `$fundamentals [ticker]` -> Displays the fundamental data points of a company.

The list of commands is continuously being expanded. If you find bugs or want to suggest improvements, do not hesitate
to make a pull request.

## Configuration

You can create your own configuration file to customize emotes and texts. First copy the default configuration
from `config/default.ini` into a custom configuration file:

```{bash}
wget -O custom.ini https://raw.githubusercontent.com/d-stoll/stonkmaster/master/stonkmaster/config/default.ini
```

Now change all configurations to git your own setup:

```{bash}
vim custom.ini
```

Finally, run the bot with your personal configuration:

```{bash}
stonkmaster --config custom.ini
```

## License

Licensed under the Apache License, Version 2.0 (the "License"); You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "
AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
