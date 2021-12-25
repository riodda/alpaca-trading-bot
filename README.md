# alpaca-trading-bot
Simple Python Alpaca Trading Bot, DON'T USE FOR LIVE TRADING

This Bot will lissen for a webhook from Trading View on port 80 and executed the trade received by the webhook.
Example Payload

{ 
"symbol": "{{ticker}}", 
"qty": "1", 
"usd_order": "false", 
"action": "buy", 
"type": "market",
"time_in_force": "gtc" 
}


Currently supports fractional orders or base orders (if a symbo il not fractionable but usd_order is set as true will calculate the psize accoding to the qty received and will round up the amount.

Due to the wellknown Tradingview misfire problem on alerts DO NOT USE IT FOR LIVE TRADIN.

Any Contribution is wellcome.

-WORKING:
1. Basic buy and Sells

-TO DO:

1. Filter for misfire 
2. Enable more order types
3. Check and track positions 
4. Improve logging
5. Add don't sell at loss
