from Data import getDataFM
from BackTest import ChartTrade,Performance,line_print
import pandas as pd
from talib.abstract import EMA
import mplfinance as mpf
import datetime
prod="0050"
data=getDataFM(prod,"2007-01-01","2023-06-09")
data["ema"]=EMA(data,timeperiod=120)
position=0
trade=pd.DataFrame()  
for i in range(1,data.shape[0]-1):
    c_time=data.index[i]
    c_high=data.loc[c_time,"high"]
    c_close=data.loc[c_time,"close"]
    c_ema=data.loc[c_time,"ema"]
    n_time=data.index[i+1]
    n_open=data.loc[n_time,"open"]
    if(position==0):
        if(c_close>c_ema*1.01):
            position=1
            order_i=i
            order_time=n_time
            order_price=n_open
            order_unit=1
    elif(position==1):
        if(c_close<c_ema*0.995):
            position=0
            cover_time=n_time
            cover_price=n_open
            trade=trade._append(pd.Series([prod,"Buy",order_time,order_price,cover_time,cover_price,order_unit]),ignore_index=True)
addp=[]
addp.append(mpf.make_addplot(data["ema"]))
Performance(trade,"ETF")
ChartTrade(data,trade,addp=addp)
