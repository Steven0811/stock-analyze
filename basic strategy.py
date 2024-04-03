from Data import getDataFM
from Chart import chartCandle
from BackTest import ChartTrade,Performance,line_print
import pandas as pd
import datetime
'''
while(True):
    current=str(datetime.datetime.now().time())
    if(current.startswith("10:01:00")):
        en=datetime.datetime.now().strftime("%Y-%m-%d")
        data=getDataFM("0050","2007-01-01","2022-05-01")
'''
trade=pd.DataFrame()
position=0 #交易部位(持股)
data=getDataFM("0050","2007-01-01","2023-06-09")
for i in range(data.shape[0]-1):
    c_time=data.index[i]
    c_low=data.loc[c_time,"low"]
    c_open=data.loc[c_time,"open"]
    c_close=data.loc[c_time,"close"]
    c_high=data.loc[c_time,"high"]
    n_time=data.index[i+1]
    n_open=data.loc[n_time,"open"]
    #進場
    if(position==0): #空手
        if((c_close>c_open) and (c_close-c_open<0.5*(c_open-c_low))):#紅K線(收盤>開盤)長度(收盤-開盤)小於下引線(開盤-最低)的一半
            position=1 #進場
            order_i=i
            order_time=n_time
            order_price=n_open
            order_unit=1
            signal=3
            #print(c_time,"觸發進場訊號 隔日進場",order_time,"進場價",order_price,"進場",order_unit,"單位")
        else:
            signal=1
    #出場
    elif(position==1): #持股
        if(i>order_i+3 and c_close>c_open): #三天後為紅K則出場
            position=0 #出場
            cover_time=n_time
            cover_price=n_open
                    #print(c_time,"觸發出場訊號 隔日出場",order_time,"出場價",order_price)
                    #交易紀錄
            trade=trade._append(pd.Series(["00878","Buy",order_time,order_price,cover_time,cover_price,order_unit]),ignore_index=True)
            signal=4
        else:
            signal=2
        #print(trade)
Performance(trade,"ETF")
ChartTrade(data,trade)
        
