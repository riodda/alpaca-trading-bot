# -*- coding: utf-8 -*-
import ast
import requests
import json
from flask import Flask, request, abort
import functions as rff
import math


def webhookParse(webhook_data):
    
    data = ast.literal_eval(webhook_data)
    return data

flaskServer = Flask(__name__)

@flaskServer.route('/')
def root():
    return 'online'

@flaskServer.route('/webhook', methods=['POST'])
def webhookListen():
    if request.method == 'POST':
        data = request.get_data(as_text=True)
        json_data  = json.loads(data)
        rff.writelog("SYSTEM,Payload Received,"+data.strip("\n"))
        #retrive asset details
        asset = rff.alpaca_get_asset(json_data['symbol'])
        last_price = rff.alpaca_get_last_price(json_data['symbol'])
        
        if json_data['action'] == "buy":
             #Buy Routine, check if market open then market buy, if market closed limit buy (TBD)           
             if (rff.alpaca_check_market_open() == True):
                 if (json_data['usd_order'] == "false"):                                                         
                    order = rff.alpaca_submit_market_buy_order(json_data['symbol'],json_data['qty'],'gtc')
                    rff.writelog("TRADING,"+"BUY,"+str(json_data['symbol'])+","+json_data['qty']+","+str(last_price)+","+str(order.id))                  
                 if ((json_data['usd_order'] == "true") and (asset.fractionable)):                    
                    #rff.alpaca_submit_market_buy_order(json_data['symbol'],json_data['qty'],'gtc')
                    order = rff.alpaca_submit_market_notional_buy_order(json_data['symbol'],json_data['qty'],'day')
                    rff.writelog("TRADING,"+"BUY,"+str(json_data['symbol'])+","+str(json_data['qty'])+","+str(last_price)+","+str(order.id))
                 if ((json_data['usd_order'] == "true") and not(asset.fractionable)):                    
                    buy_amount = math.ceil((float(json_data['qty'])/last_price))
                    order = rff.alpaca_submit_market_buy_order(json_data['symbol'],buy_amount,'gtc')
                    rff.writelog("TRADING,"+"BUY,"+str(json_data['symbol'])+","+str(json_data['qty'])+","+str(last_price)+","+str(order.id))
                    #calculate asset amount to buy and truncate to integer.
             if (rff.alpaca_check_market_open() == False):
                 rff.writelog("TRADING,ERROR,Market Closed,"+json_data['symbol'])
                    
        if (json_data['action'] == "sell") and (int(json_data['qty']) > 0):
             #Sell Routine, check if market open then market buy, if market closed limit buy 
             #Retrive Position
             position = rff.alpaca_get_position(json_data['symbol'])     
             if (position == False):
                 rff.writelog("TRADING,ERROR,"+str(json_data['symbol'])+",Missing Position")
             
             if ((rff.alpaca_check_market_open() == True) and (not(position == False))):
                 order = rff.alpaca_submit_sell_order(json_data['symbol'],json_data['qty'],'gtc')
                 rff.writelog("TRADING,"+"SELL,"+str(json_data['symbol'])+","+str(json_data['qty'])+","+str(last_price)+","+str(order.id))
                 
             if (rff.alpaca_check_market_open() == False):
                 rff.writelog("TRADING,ERROR,Market Closed,"+str(json_data['symbol']))
                 
        if (json_data['action'] == "close") or ((json_data['action'] == "sell") and (int(json_data['qty']) == 0)):
             #close code, check if market open then retrive postions find position for symbo check qty then close sell position
             #Retrive Position
             position = rff.alpaca_get_position(json_data['symbol']) 
             if ((rff.alpaca_check_market_open() == True) and (not(position == False))):
                 order = rff.alpaca_close_position(json_data['symbol'])
                 rff.writelog("TRADING,CLOSE,"+str(json_data['symbol'])+","+str(position.qty)+","+str(last_price)+","+str(order.id)+","+str(position.unrealized_pl))
                 
             if (rff.alpaca_check_market_open() == False):
                 rff.writelog("TRADING,ERROR,Market Closed,"+str(json_data['symbol']))
        print(order)
        return '', 200
    else:
        print("Some kind of error has happen")
        rff.writelog("SYSTEM,Generic Error")
        abort(400)

#Start Bot
    
if __name__ == '__main__':
    rff.writelog("SYSTEM,Bot Started")
    flaskServer.run(host='212.227.30.186',port=80, debug=True)
    