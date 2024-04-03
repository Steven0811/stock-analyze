from Data import getDataFM
from BackTest import ChartTrade,Performance,line_print
import pandas as pd
from talib.abstract import EMA
import mplfinance as mpf
import datetime
while(True):
    current=str(datetime.datetime.now().time())
    if(current.startswith("08:43:00")):
        prod="0050"
        st="2010-01-01"
        en=datetime.datetime.now().strftime("%Y-%m-%d")
        data=getDataFM(prod,st,en)
        data["ema"]=EMA(data,timeperiod=120)
        position=0
        signal=0
        for i in range(1,data.shape[0]):
            c_time=data.index[i]
            c_close=data.loc[c_time,"close"]
            c_ema=data.loc[c_time,"ema"]
            if(position==0):
                if(c_close>c_ema*1.01):
                    position=1
                    signal=3
                else:
                    signal=1
            elif(position==1):
                if(c_close<c_ema*0.995):
                    position=0
                    signal=4
                else:
                    signal=2
        strategy_name="均線策略"
        if(signal==1):
            line_print(f"{strategy_name}\n{prod}\n{en}\n維持空手")
        elif(signal==2):
            line_print(f"{strategy_name}\n{prod}\n{en}\n維持進場")
        elif(signal==3):
            line_print(f"{strategy_name}\n{prod}\n{en}\n進場訊號")
        elif(signal==4):
            line_print(f"{strategy_name}\n{prod}\n{en}\n出場訊號")


