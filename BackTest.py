import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt
import lineTool
def ChartTrade(data,trade=pd.DataFrame(),addp=[],v_enable=True): 
    addp=addp.copy()
    data1=data.copy()
    if(trade.shape[0]>0):
        trade1=trade.copy()
        buy_order_trade=trade1[[2,3]]
        buy_order_trade=buy_order_trade.set_index(2)
        buy_order_trade.columns=["buy_order"]
        buy_order_trade=buy_order_trade.drop_duplicates()
        buy_cover_trade=trade1[[4,5]]
        buy_cover_trade=buy_cover_trade.set_index(4)
        buy_cover_trade.columns=["buy_cover"]
        buy_cover_trade=buy_cover_trade.drop_duplicates()
        data1=pd.concat([data1,buy_order_trade,buy_cover_trade],axis=1)
        addp.append(mpf.make_addplot(data1["buy_order"],type="scatter",color="#FF4500",marker="^",markersize=50))
        addp.append(mpf.make_addplot(data1["buy_cover"],type="scatter",color="#16982B",marker="v",markersize=50))
    mcolor=mpf.make_marketcolors(up="r",down="g",inherit=True)
    mstyle=mpf.make_mpf_style(base_mpf_style="yahoo",marketcolors=mcolor)
    mpf.plot(data1,addplot=addp,style=mstyle,type="candle",volume=v_enable)
def  Performance(trade=pd.DataFrame(),prodtype="ETF"): 
    if(trade.shape[0]==0):
        print("沒有交易紀錄")
        return False
    if(prodtype=="ETF"):
        cost=0.001+0.00285 #ETF稅金0.1%
    elif(prodtype=="Stock"):
        cost=0.003+0.00285 #股票稅金
    else:
        return False
    trade1=trade.copy()
    trade1=trade1.sort_values(2)
    trade1=trade1.reset_index(drop=True)
    trade1.columns=["products","bs","order_time","order_price","cover_time","cover_price","order_unit"]
    trade1["ret"]=(((trade1["cover_price"]-trade1["order_price"])/trade1["order_price"])-cost)*trade1["order_unit"] #每筆交易報酬率
    print("交易次數(回測的交易紀錄筆數)",trade.shape[0],"次",sep="")
    print("總績效(整個回測期間的總報酬率)",trade1["ret"].sum().round(4),"%",sep="")
    print("平均績效",trade1["ret"].mean().round(4),"%",sep="")
    onopen_day=(trade1["cover_time"]-trade1["order_time"]).mean()
    print("平均持有天數",onopen_day.days,"天",sep="")
    earn_trade=trade1[trade1["ret"]>0]
    loss_trade=trade1[trade1["ret"]<0]
    if(earn_trade.shape[0]==0 or loss_trade.shape[0]==0): #判斷是否賺賠皆有績效
        print("交易資料樣本不足(交易資料須有賺有賠)")
        return False
    earn_ratio=earn_trade.shape[0]/trade.shape[0]
    print("勝率(獲利次數的佔比)",round(earn_ratio,2),"%",sep="")
    avg_earn=earn_trade["ret"].mean().round(4)
    print("平均獲利(平均每一次獲利的金額)",avg_earn,"元",sep="")
    avg_loss=loss_trade["ret"].mean().round(4)
    print("平均虧損(平均每一次虧損的金額)",avg_loss,"元",sep="")
    odds=abs(avg_earn/avg_loss)
    print("賺賠比(平均獲利/平均虧損)",odds.round(4))
    print("期望值(每投入的金額可能會回報多少倍的金額)",((earn_ratio*odds)-(1-earn_ratio)).round(4))
    earn_onopen_day=(earn_trade["cover_time"]-earn_trade["order_time"]).mean()
    print("獲利平均持有天數",earn_onopen_day.days,"天",sep="")
    loss_onopen_day=(loss_trade["cover_time"]-loss_trade["order_time"]).mean()
    print("虧損平均持有天數",loss_onopen_day.days,"天",sep="")
    tmp_accloss=0
    max_accloss=0
    for ret in trade1["ret"].values:
        if(ret<=0):
            tmp_accloss*=ret
            max_accloss=min(max_accloss,tmp_accloss)
        else:
            tmp_accloss=0
    trade1["acc_ret"]=(1+trade1["ret"]).cumprod()
    trade1.loc[-1,"acc_ret"]=1
    trade1.index=trade1.index+1
    trade1.sort_index(inplace=True)
    trade1["acc_max_cap"]=trade1["acc_ret"].cummax()
    trade1["dd"]=trade1["acc_ret"]/trade1["acc_max_cap"]
    trade1.loc[trade1["acc_ret"]==trade1["acc_max_cap"],"new_high"]=trade1["acc_ret"]
    print("最大資金回落(資金從最高點回落至最低點的幅度)",round(1-trade1["dd"].min(),4),"%",sep="")
    ax=plt.subplot(111)
    ax.plot(trade1["acc_ret"],"b-",label="Profit")
    ax.plot(trade1["dd"],"-",color="#00A600",label="MDD")
    ax.plot(trade1["new_high"],"o",color="#FF0000",label="Equity high")
    ax.legend()
    plt.show()
token="hbgaVZxmMax8ja6n7TKC7wBPbQ5qkT9rdsTS4T6Ftv9"
def line_print(msg):
    print(msg)
    try:
        lineTool.lineNotify(token,msg)
    except:
        print("line notify 失效")
        pass
    
