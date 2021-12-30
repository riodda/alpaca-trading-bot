# WATB Webhook Alpaca Trading Bot
Simple Python Alpaca Trading Bot, **DON'T USE FOR LIVE TRADING**

This Bot will lissen for a webhook from Trading View or other platforms on given port and execute the trade received by webhook.

Edit config.py with api keys, ip address, port, log and payload folders.

`key = "MYKEY"`

`secretKey = "MYSECRET"`

`api_url = "https://paper-api.alpaca.markets"`

`log_dir = "Z:\Trading\Alpaca TV Bot"`

`payload_dir = "Z:\Trading\Alpaca TV Bot"`

`ip_address = "127.0.0.1"`

`webhook_port = 80`

Bot accepts orders only in json format

Example of base order payload

`{ 
"Time":"{{time}}",
"symbol": "{{ticker}}", 
"qty": "1", 
"usd_order": "false", 
"action": "buy", 
"type": "market",
"time_in_force": "gtc" 
}`

Example of fractional order payload (must be time in force = day).

`{ 
"Time":"{{time}}",
"symbol": "{{ticker}}", 
"qty": "50", 
"usd_order": "true", 
"action": "buy", 
"type": "market",
"time_in_force": "day" 
}
`

if `"usd_order"` set to `"false"` `"qty"` is base (contracts), usd if `"usd_order"` set to `"true`".

Currently supports fractional orders or integer contract orders (if a symbol is not fractionable but usd_order is set as true will calculate the psize accoding to the qty received and will round up the amount.

Mandatory json fields: 

`"symbol","qty","usd_order","action","type","time_in_force"`

Due to the wellknown Tradingview misfire problem on alerts DO NOT USE IT FOR LIVE TRADING.

To start the bot is suggested to use screen

start at boot on crontab with:

`@reboot /usr/bin/screen -S alpaca_bot -d -m   /usr/bin/python3 -u /foder_of_bot/bot.py`

If you have other flask instances is likely not to work.


Any Contribution is wellcome.

**-KIND OF WORKING:**

1. Basic buy and Sells
2. Filter for misfire, basic check of received paylod if is equal to stored one is considered a misfire, be sure to add to the payload something that guarantee that is a geniuine strategy generated signal (trade counter for example). Still no guarnatee about the coeherence between trading view strategy and alerts generated.

**-TO DO:**

1. Enable more order types
2. Check and track positions 
3. Improve logging
4. Some security/token/password on webhook
5. Formal check of payload
6. Support for pre and after hour markets (can't be tested on paper)
7. Check Daytrade Status
8. Check Buying Power for short trades
9. Check all json fields are present
10. Limit Orders

