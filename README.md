# 前置函式
## Data: 利用yfinance或FiMind抓取股票資料。

## BackTest: 繪製權益曲線圖、分析各項指標、LINEBOT訊號推播。

## Chart: 繪製K線圖。
---
# 各項交易策略
## Basic strategy: 當天K線為紅K，且下引線為實體紅K的兩倍則進場，最低持有三日，三日後只要當日為紅K則出場。

## Trend breakout strategy: 收盤價突破前三根K線的最高價則進場，進場後最高價低於壓力線則出場。

## EMA strategy: 利用Talib計算時間周期為120天的移動平均線，當收盤價大於均線加上1%時進場，收盤價小於均線減去0.5%出場。

## Stop-Loss strategy: 收盤價突破前三根K線的最高價時進場，當價格下降超過進場的「最高的收盤價」回落的5%則停損出場。
