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
  <a href="#commands">Commands</a>
  •
  <a href="#configuration">Configuration</a>
  •
  <a href="#license">License</a>
</p>

## Overview

The Stonk Master is a Discord bot for fellow apes to monitor stonks without leaving their gaming habitat. It presents information about stonks in a very easy and simple way.

## Installation

The installation is only tested on Ubuntu 20.04 LTS, however other operating systems should also work without any problem. Just make sure that all dependencies are completly installed.

Make sure Python 3.8 or higher, pip and setuptools are installed on your system.

```{bash}
$ python --version # This should return 3.8.10 or higher
$ python -m pip install --upgrade pip
$ pip install --upgrade setuptools
```

Now clone the repository.

```{bash}
$ git clone git@github.com:d-stoll/stonkmaster.git
$ cd stonkmaster
```

And install all dependencies and the executable.

```{bash}
$ pip install .
```

(Optional) You can create your own configuration file to customize emotes and texts.

```{bash}
$ cp default.ini custom.ini
$ vim custom.ini
```

To run the bot, obtain you personal discord token and run the stonkmaster executable.

```{bash}
$ export DISCORD_TOKEN=<YOUR_PERSONAL_DISCORD_TOKEN>
$ stonkmaster
```

## Commands

### $price \<symbol\>

Shows the current price of the stonk, as well as its daily change.

<blockquote>
    <p>&gt;  <i>$price AMC</i></p>
    <img align="left" src=".github/assets/stonkmaster-avatar.png" alt="stonkmaster avatar">
        <b>Stonk Master</b><br />
        The market price of <b>AMC Entertainment Holdings, Inc. (AMC)</b> is <b>65.40$</b> (+104.12%)
</blockquote>

### $shorts \<symbol\>

Provides currently known information on how heavily the stonk is shorted.

<blockquote>
    <p>&gt;  <i>$shorts GME</i></p>
    <img align="left" src=".github/assets/stonkmaster-avatar.png" alt="stonkmaster avatar">
        <b>Stonk Master</b><br />
        Currently <b>11,972,632</b> shares of <b>GameStop Corp. (GME)</b> are shorted. This corresponds to <b>29.34%</b> of available shares.
</blockquote>


### $chart \<symbol\> \<range\>

Generates a chart showing the price development of the ticker over. The range can be specified 
in days (d), months (m) or years (y).

![Tesla Chart (2 years)](.github/assets/tsla_chart.png)


### $sec \<symbol\> \<filing-type\>

Fetches the latest SEC company filings from EDGAR.

![AMC sec filings (8-k)](.github/assets/amc_sec.png)

## Configuration

## License
