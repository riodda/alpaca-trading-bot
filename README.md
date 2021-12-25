# alpaca-trading-bot
Simple Python Alpaca Trading Bot, DON'T USE FOR LIVE TRADING

This Bot will lissen for a webhook from Trading View on port 80 and execute the trade received by webhook.
Example Payload (json format)

{ 
"symbol": "{{ticker}}", 
"qty": "1", 
"usd_order": "false", 
"action": "buy", 
"type": "market",
"time_in_force": "gtc" 
}

qty is base if usd_order set to false, usd is usd_order set to true.

Currently supports fractional orders or base orders (if a symbol isnot fractionable but usd_order is set as true will calculate the psize accoding to the qty received and will round up the amount.

Due to the wellknown Tradingview misfire problem on alerts DO NOT USE IT FOR LIVE TRADING.

To start the bot is suggested to use screen

start at boot on crontab with:

@reboot /usr/bin/screen -S alpaca_bot -d -m   /usr/bin/python3 -u /foder_of_bot/bot.py

If you have other flask instances is likely not to work.


Any Contribution is wellcome.

-WORKING:
1. Basic buy and Sells
2. Filter for misfire, basic check of received paylod if is equal to stored one is considered a misfire, be sure to add to the payload something that guarantee that is a geniuine strategy generated signal (trade counter for example). Still no guarnatee about the coeherence between trading view strategy and alerts generated.

-TO DO:


1. Enable more order types
2. Check and track positions 
3. Improve logging
4. Add don't sell at loss (to prevent unwanted sells).
5. Some security/token/password on webhook
6. Formal check of payload
7. Check of symbol existence/treadability
8. Support for pre and after hour markets (can't be tested on paper)
