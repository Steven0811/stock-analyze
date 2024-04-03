import mplfinance as mpf
def chartCandle(data,addp=[]):
    mcolor=mpf.make_marketcolors(up="r",down="g",inherit=True)
    mstyle=mpf.make_mpf_style(base_mpf_style="yahoo",marketcolors=mcolor)
    mpf.plot(data,addplot=addp,style=mstyle,type="candle",volume=True)




