from Data import getDataFM
from BackTest import ChartTrade,Performance
import mplfinance as mpf
import pandas as pd
prod="0050"
data=getDataFM(prod,"2007-01-01","2022-05-01")
data["ceil"]=data.rolling(3)["high"].max().shift()
position=0
trade=pd.DataFrame()
movestoploss=0.05
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
            stoploss=order_price*(1-movestoploss)
    elif(position==1):
        stoploss=max(stoploss,c_close*(1-movestoploss))
        if(c_close<stoploss):
            position=0
            cover_time=n_time
            cover_price=n_open
            trade=trade.append(pd.Series([prod,"Buy",order_time,order_price,cover_time,cover_price,order_unit]),ignore_index=True)
addp=[]
addp.append(mpf.make_addplot(data["ceil"]))
Performance(trade,"ETF")
ChartTrade(data,trade,addp=addp)
