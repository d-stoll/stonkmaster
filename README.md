# The Stonk Master 📈💎🙌

![Build status](https://github.com/d-stoll/stonkmaster/actions/workflows/build.yml/badge.svg)
![License](https://img.shields.io/github/license/d-stoll/stonkmaster)
![Top language](https://img.shields.io/github/languages/top/d-stoll/stonkmaster)
![Code quality](https://img.shields.io/badge/code%20quality-excellent-brightgreen)

The Stonk Master is a Discord bot for fellow apes to monitor stonks without leaving their gaming habitat. It presents information about stonks in a very easy and simple way.

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


