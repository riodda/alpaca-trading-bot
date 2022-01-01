```
█     █░ ▄▄▄     ▄▄▄█████▓ ▄▄▄▄   
▓█░ █ ░█░▒████▄   ▓  ██▒ ▓▒▓█████▄ 
▒█░ █ ░█ ▒██  ▀█▄ ▒ ▓██░ ▒░▒██▒ ▄██
░█░ █ ░█ ░██▄▄▄▄██░ ▓██▓ ░ ▒██░█▀  
░░██▒██▓  ▓█   ▓██▒ ▒██▒ ░ ░▓█  ▀█▓
░ ▓░▒ ▒   ▒▒   ▓▒█░ ▒ ░░   ░▒▓███▀▒
  ▒ ░ ░    ▒   ▒▒ ░   ░    ▒░▒   ░ 
  ░   ░    ░   ▒    ░       ░    ░ 
    ░          ░  ░         ░      
                                 ░
```

# WATB Webhook Alpaca Trading Bot
Simple Python Alpaca Trading Bot, **DON'T USE FOR LIVE TRADING**

This Bot will lissen for a webhook from Trading View or other platforms on given port and execute the trade received by webhook.

Edit config.py with api keys, ip address, port, log and payload folders, ip addres and port, daytrade flag minimum pct for sell and (optional telegram credentials).

`key = "MYKEY"`

`secretKey = "MYSECRET"`

`api_url = "https://paper-api.alpaca.markets"`

`log_dir = "Z:\Trading\Alpaca TV Bot"`

`payload_dir = "Z:\Trading\Alpaca TV Bot"`

`ip_address = "127.0.0.1"`

`webhook_port = 80`

Replace my-token with a random generated token (with linux you can generate a random token with `tr -dc A-Za-z0-9 </dev/urandom | head -c 13 ; echo ''`)

`webhook_token = "my-token"`

Replace my-uuid with machine uuid (with linux you can generate a rando uuid wiht `uuidgen`)

`webhook_uuid = "my-uuid"`

`day_trade = False`

`min_pct_for_sell = 0`

`telegram_bot_token = 'telegram_token'`

`telegram_bot_chatID = 'telegram_chat_id'`

On console the bot will output the webhook address

![image](https://user-images.githubusercontent.com/13453063/147855033-8e0914f6-9530-485a-b388-45efcdd58c08.png)



Bot accepts orders only in json format

Example of base order payload

```
{ 
"token" : "my-token",
"Time":"{{time}}",
"symbol": "{{ticker}}", 
"qty": "1", 
"usd_order": "false", 
"action": "buy", 
"type": "market",
"time_in_force": "gtc" 
}
```

Example of fractional order payload (must be time in force = day).

```
{ 
"token" : "my-token",
"Time":"{{time}}",
"symbol": "{{ticker}}", 
"qty": "50", 
"usd_order": "true", 
"action": "buy", 
"type": "market",
"time_in_force": "day" 
}
```

if `"usd_order"` set to `"false"` `"qty"` is base (contracts), usd if `"usd_order"` set to `"true`".

Currently supports fractional orders or integer contract orders (if a symbol is not fractionable but usd_order is set as true will calculate the psize accoding to the qty received and will round up the amount.

Mandatory json fields: 

`"token","symbol","qty","usd_order","action","type","time_in_force"`

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
4. Formal check of payload
5. Support for pre and after hour markets (can't be tested on paper)
6. Check Daytrade Status and set alarm
7. Check Buying Power for short trades
8. Check all json fields are present
9. Limit Orders
10. Control trough to Discord/Telegram
11. Base pinescript strategy to test bot
12. Add strategy Name in Payload with ACTIVE/NON ACTIVE flag for forward testing

