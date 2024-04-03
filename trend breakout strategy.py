from Data import getDataFM
from BackTest import ChartTrade,Performance,line_print
import mplfinance as mpf
import pandas as pd
import datetime
prod="0050"
data=getDataFM(prod,"2007-01-01","2023-3-20")
data["ceil"]=data.rolling(3)["high"].max().shift()
position=0
trade=pd.DataFrame()
takeprofit=0.12
stoploss=0.05
strategy_name="趨勢突破交易策略"
en=datetime.datetime.now().strftime("%Y-%m-%d")
for i in range(data.shape[0]-1):
    c_time=data.index[i]
    c_high=data.loc[c_time,"high"]
    c_close=data.loc[c_time,"close"]
    c_ceil=data.loc[c_time,"ceil"]
    n_time=data.index[i+1]
    n_open=data.loc[n_time,"open"]
    if(position==0):
        if(c_close>c_ceil):
            position=1
            order_i=i
            order_time=n_time
            order_price=n_open
            order_unit=1
            signal=3
        else:
            signal=1
    elif(position==1):
        if(c_close>order_price*(1+takeprofit) or c_close<order_price*(1-stoploss)):
            position=0
            cover_time=n_time
            cover_price=n_open
            trade=trade._append(pd.Series([prod,"Buy",order_time,order_price,cover_time,cover_price,order_unit]),ignore_index=True)
            signal=4
        else:
            signal=2
addp=[]
addp.append(mpf.make_addplot(data["ceil"]))
Performance(trade,"ETF")
ChartTrade(data,trade,addp=addp)
'''
if(signal==1):
    line_print(f"{strategy_name}\n{prod}\n{en}\n維持空手")
elif(signal==2):
    line_print(f"{strategy_name}\n{prod}\n{en}\n維持進場")
elif(signal==3):
    line_print(f"{strategy_name}\n{prod}\n{en}\n進場訊號")
elif(signal==4):
    line_print(f"{strategy_name}\n{prod}\n{en}\n出場訊號")
'''
