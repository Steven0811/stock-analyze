import yfinance as yf
import pandas as pd
from FinMind.data import DataLoader
import requests
def getDataYF(prod,st,en):
    tmpdata=yf.download(prod,start=st,end=en)
    tmpdata_columns=[i.lower() for i in tmpdata.columns]
    return tmpdata
FM=DataLoader()
def getDataFM(prod,st,en):
    tmpdata=FM.taiwan_stock_daily_adj(stock_id=prod,start_date=st,end_date=en)
    tmpdata=tmpdata.rename(columns={"max":"high","min":"low","Trading_Volume":"volume"})
    tmpdata["date"]=pd.to_datetime(tmpdata["date"])
    tmpdata=tmpdata.set_index(tmpdata["date"])
    tmpdata=tmpdata[["open","high","low","close","volume"]]
    return tmpdata
def getStockList():
    bakfile="TSE_StockList.csv"
    if(os.path.exists(bakfile)):
        df=pd.read_csv(bakfile)
    else:
        res=requests.get("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
        df=pd.read_html(res.text)[0]
        df.columns=df.iloc[0]
        df=df.iloc[2:]
        df=df.dropna(thresh=3,axis=0).dropna(thresh=3,axis=1)
        df.to_csv(bakfile)
    return df
    
