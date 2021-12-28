# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import alpaca_trade_api as tradeapi
from config import *
from datetime import datetime
import time
import os

LogDirectory = log_dir

api = tradeapi.REST(key, secretKey, base_url=api_url, api_version='v2') # or use ENV Vars shown below

def writelog(msg):
    time=(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

    s=f'{time} {msg}\n'

    fh=open(LogDirectory+'/alpaca_bot.log','a')
    fh.write(s)
    fh.close()
    
def alpaca_get_15Min_bars(_symbol,_number):
    _df=pd.DataFrame()
    _temp=pd.DataFrame()
    if _number<1000:
        _df = api.get_barset(_symbol, '15Min', limit=_number, start=None, end=None, after=None, until=None).df
    else:
        _num_cycles, _residual = divmod(_number, 1000)
        if _residual == 0:
            _df = api.get_barset(_symbol, '15Min', limit=1000, start=None, end=None, after=None, until=None).df
            _num_cycles -=1
        else:
            _df = api.get_barset(_symbol, '15Min', limit=_residual, start=None, end=None, after=None, until=None).df    
        for i in range(1,_num_cycles+1):
            _temp = api.get_barset(_symbol, '15Min', limit=1000, start=None, end=None, after=None, until=_df.first_valid_index().isoformat()).df
            _df= pd.concat([_temp,_df,])
    return _df

def alpaca_get_buying_power():
    account = api.get_account()
    return float(account.buying_power)

def alpaca_get_account():
    _account = api.get_account()
    return _account
    
def alpaca_get_positions():
    _positions = api.list_positions()
    return _positions

def alpaca_get_position(_symbol):
    try:
        _position = api.get_position(_symbol)
        return _position
    except:
        return False

def alpaca_check_market_open():
    if (api.get_clock().is_open):
        return True
    else:
        return False

def alpaca_get_positions():       
    return api.list_positions()

def alpaca_submit_market_buy_order(_symbol,_qty,_time_in_force):    
    _order = api.submit_order(symbol=_symbol,qty=_qty,side='buy',type='market',time_in_force=_time_in_force)
    return _order

def alpaca_submit_market_notional_buy_order(_symbol,_qty,_time_in_force):    
    _order = api.submit_order(symbol=_symbol,notional=_qty,side='buy',type='market',time_in_force=_time_in_force)
    return _order

def alpaca_submit_limit_buy_order(_symbol,_qty,_limit_price,_time_in_force):    
    _order = api.submit_order(symbol=_symbol,qty=_qty,side='buy',type='limit',limit_price=_limit_price,time_in_force=_time_in_force)
    return _order
    
def alpaca_close_position(_symbol):
    _position = api.close_position(symbol=_symbol)
    return _position

def alpaca_get_last_price(_symbol):
    _last_trade = api.get_last_quote(symbol=_symbol)
    _last_price = (float(_last_trade.askprice)+float(_last_trade.bidprice))/2
    return _last_price

def alpaca_submit_buy_order(_symbol,_qty):
    _order = api.submit_order(symbol=_symbol,qty=_qty,side='buy',type='market',time_in_force='gtc')
    return _order

def alpaca_submit_sell_order(_symbol,_qty,_time_in_force):
    _order = api.submit_order(symbol=_symbol,qty=_qty,side='sell',type='market',time_in_force=_time_in_force)
    return _order

def alpaca_trailing_sell_order(_symbol,_qty,_trailing_pct):
    _order = api.submit_order(symbol=_symbol,qty=_qty,side='sell',type='trailing_stop',trail_percent=_trailing_pct,time_in_force='gtc')
    return _order

def alpaca_trailing_buy_order(_symbol,_qty,_trailing_pct):
    _order = api.submit_order(symbol=_symbol,qty=_qty,side='buy',type='trailing_stop',trail_percent=_trailing_pct,time_in_force='gtc')
    return _order

def alpaca_get_asset(_symbol):
    _asset = api.get_asset(_symbol)
    return _asset
    
    
def alpaca_get_all_symbols():
    try:
        _active_assets = api.list_assets(status='active')
        _symbols = []
        for _asset in _active_assets:
            _symbols.append(_asset.symbol)
        return _symbols
    except:
        return False
