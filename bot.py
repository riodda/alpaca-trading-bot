# -*- coding: iso-8859-1 -*-
'''
WATB !!!!
Webhook Alpaca Trading Bot by Dario Armellin riodda@gmail.com
(C) 2021

Base trading bot, intially based on the idea from East Village Trading Robot
https://github.com/wallacewd/Alpaca-TradingView-Trading-Bot-for-AWS.git
Evolved on his own
Don't use for live trading
NOT A FINANCIAL ADVICE
'''
import ast
import requests
import json
from flask import Flask, request, abort
from flask_apscheduler import APScheduler
import functions as rff
import math
import os
from config import *

WATB_VERSION = '0.1-b.3'
__version__ = WATB_VERSION

def webhookParse(webhook_data):
    
    data = ast.literal_eval(webhook_data)
    return data

flaskServer = Flask(__name__)
scheduler = APScheduler()

def update_symbol_list():
    all_symbols = rff.alpaca_get_all_symbols()
    rff.writelog("SYSTEM,Updating Symbol List")
    return


@flaskServer.route('/')
def root():
    return 'online'

base_url = '/'+webhook_uuid
@flaskServer.route(base_url, methods=['POST'])
def webhookListen():
    if request.method == 'POST':
        data = request.get_data(as_text=True)
        #try to decode as json
        try:
            json_data  = json.loads(data)
            rff.writelog("SYSTEM,Payload Received,"+data.strip("\n")) 
                    #check if payload has right token
            if (json_data['token'] == webhook_token):
                rff.writelog("SYSTEM,Correct Token")
            else:
                rff.writelog("SYSTEM,ERROR,Incorrect Token")
            
        except:
            rff.writelog("SYSTEM,ERROR,Malformed or invalid json payload")
            abort(400, description="Malformed or invalid json payload")
        
        #check al fields are correct and present symbol side qty type time in force usdorder
        
        
        #check if symbol is valid
        if not(json_data['symbol'] in all_symbols):
            rff.writelog("TRADING,ERROR,Invalid symbol")
            abort(400, description="Invalid symbol")
        
        #save load and compare with last json message
        filename = 'payload_'+str(json_data['symbol'])+'.json'

        if os.path.isfile(payload_dir+filename):
            #old symbol, load json and compare with previous payload
            f = open(payload_dir+filename)
            old_message = json.load(f)
            
            if (old_message == json_data):
                rff.writelog("SYSTEM,ERROR,Duplicated payload,"+data.strip("\n"))
                abort(400, description="Duplicated payload")
            else:
                #different json payload replace file
                os.remove(payload_dir+filename)
                with open(payload_dir+filename, 'w') as f:
                    json.dump(json_data,f)

        else:
            #new symbol, save first message
            with open(payload_dir+filename, 'w') as f:
                    json.dump(json_data,f)


        #retrive asset details
        asset = rff.alpaca_get_asset(json_data['symbol'])
        #redundant code, check is already done with symbo list
        #if (asset == False):
        #    rff.writelog("TRADING,ERROR, Unrecognized Symbol,"+data.strip("\n"))
        #    abort(400, description="Invalid Symbol") 

        last_price = rff.alpaca_get_last_price(json_data['symbol'])
        #Check if market is open
        if (rff.alpaca_check_market_open() == False):
            rff.writelog("TRADING,ERROR,Market Closed,"+json_data['symbol'])
            abort(400, description="Market Closed")
        
        if json_data['action'] == "buy":
            #retrive account buying power and daytrade count
            
            account = rff.alpaca_get_account()
            max_buy_amount = float(account.buying_power)
            daytrade_count = int(account.daytrade_count)
                
            rff.writelog("TRADING,Current Buying power "+str(max_buy_amount))
            rff.writelog("TRADING,Current daytrade count "+str(daytrade_count))
            #Create a Special Alert for DAYTRADE count >= 4            
            
            
            #Buy Routine check for usd or base order and asset fractionability   
            if (json_data['usd_order'] == "false"):                                                         
                if (float(json_data['qty'])*last_price) < max_buy_amount:
                    if 'strategy' in json_data:
                        order = rff.alpaca_submit_market_buy_order(json_data['symbol'],json_data['qty'],'gtc',json_data['strategy'])
                    else:
                        order = rff.alpaca_submit_market_buy_order(json_data['symbol'],json_data['qty'],'gtc')
                    print(order)
                    rff.writelog("TRADING,"+"BUY,"+str(json_data['symbol'])+","+json_data['qty']+","+str(last_price)+","+str(order.id)) 
                else:
                    rff.writelog("TRADING,ERROR,Insufficent Buying power:"+str(max_buy_amount)+" needed:"+str(float(json_data['qty'])*last_price)) 
                    abort(400, description="Insufficent Buying power")
                    
            #asset  fractionable calculate asset amount to buy
            
            if ((json_data['usd_order'] == "true") and (asset.fractionable)):
                if  (float(json_data['qty']) < max_buy_amount):
                    if 'strategy' in json_data:
                        order = rff.alpaca_submit_market_notional_buy_order(json_data['symbol'],json_data['qty'],'day',json_data['strategy'])
                    else:
                        order = rff.alpaca_submit_market_notional_buy_order(json_data['symbol'],json_data['qty'],'day')
                    print(order)
                    rff.writelog("TRADING,"+"BUY,"+str(json_data['symbol'])+","+str(json_data['qty'])+","+str(last_price)+","+str(order.id))
                else:
                    rff.writelog("TRADING,ERROR,Insufficent Buying power:"+str(max_buy_amount)+" needed:"+str(float(json_data['qty'])))
                    abort(400, description="Insufficent Buying power")
                    
            #asset not fractionable calculate asset amount to buy and round up to integer.
            if ((json_data['usd_order'] == "true") and not(asset.fractionable)):                    
                buy_amount = math.ceil((float(json_data['qty'])/last_price))
                if (buy_amount*last_price < max_buy_amount):
                    if 'strategy' in json_data:
                        order = rff.alpaca_submit_market_buy_order(json_data['symbol'],buy_amount,'gtc',json_data['strategy'])
                    else:
                        order = rff.alpaca_submit_market_buy_order(json_data['symbol'],buy_amount,'gtc')
                    print(order)
                    rff.writelog("TRADING,"+"BUY,"+str(json_data['symbol'])+","+str(json_data['qty'])+","+str(last_price)+","+str(order.id))
                else:
                    rff.writelog("TRADING,ERROR,Insufficent Buying power:"+str(max_buy_amount)+" needed:"+str(buy_amount*last_price))
                    abort(400, description="Insufficent Buying power")
                 
                    
        if (json_data['action'] == "sell") and (int(json_data['qty']) > 0): 
            #Sell Routine
            #Retrive Position
            
            position = rff.alpaca_get_position(json_data['symbol'])     
            if (position == False):
                rff.writelog("TRADING,ERROR,"+str(json_data['symbol'])+",Missing Position")
             
            if not(position == False):
                if 'strategy' in json_data:
                    order = rff.alpaca_submit_sell_order(json_data['symbol'],json_data['qty'],'gtc',json_data['strategy'])
                else:
                    order = rff.alpaca_submit_sell_order(json_data['symbol'],json_data['qty'],'gtc')
                print(order)
                rff.writelog("TRADING,"+"SELL,"+str(json_data['symbol'])+","+str(json_data['qty'])+","+str(last_price)+","+str(order.id))
                 
        #CLose Routine, check if market open then market close (sell with 0 qty for TV strategy generated alerts sells DLR)
        if (json_data['action'] == "close") or ((json_data['action'] == "sell") and (int(json_data['qty']) == 0)):
            #close code, check if market open then retrive postions find position for symbol check qty then close sell position
            #Retrive Position
            position = rff.alpaca_get_position(json_data['symbol']) 
            if ((rff.alpaca_check_market_open() == True) and (not(position == False)) and (float(position.unrealized_plpc) > min_pct_for_sell)):
                order = rff.alpaca_close_position(json_data['symbol'])
                print(order)
                rff.writelog("TRADING,CLOSE,"+str(json_data['symbol'])+","+str(position.qty)+","+str(last_price)+","+str(order.id)+","+str(position.unrealized_pl))
            

        
        return '', 200

    else:
        print("Some kind of error has happen")
        rff.writelog("SYSTEM,Generic Error")
        abort(400)

#Start Bot

slpash = """
Starting

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
Webhook Alpaca Trading Bot Version:"""+WATB_VERSION
url = "Webhook url: http://"+ip_address+':'+str(webhook_port)+base_url

if __name__ == '__main__':
    print(slpash)
    print(url)
    rff.writelog("SYSTEM,WATB Bot Started version "+WATB_VERSION)
    all_symbols = rff.alpaca_get_all_symbols()
    rff.writelog("SYSTEM,Updating Symbol List")
    scheduler.add_job(id = 'Update Symbols', func=update_symbol_list, trigger="interval", minutes=120)
    scheduler.start()
    flaskServer.run(host=str(ip_address),port=webhook_port, debug=True)
   
    

   
